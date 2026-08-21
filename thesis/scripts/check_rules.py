"""Find stray horizontal rules — black stripes — in an exported PDF.

A Markdown `---` reaches `md2gost.py` as a real paragraph with a bottom border
and prints as a black line across the text block. Because every `# ` heading
opens a page of its own, such a rule lands at the foot of the *previous* part,
which is where the defect was found on 2026-08-21: seven of them, one after the
Introduction, each of the four chapters, the Conclusion and the reference list.
The assemblers no longer emit those separators; this script is the gate that
keeps them from coming back, and it works on the shipped PDF rather than on the
Markdown, so it also catches a rule introduced anywhere else in the toolchain.

Table frames are horizontal lines too. A rule is reported only when no vertical
stroke touches it and no other horizontal stroke sits within `V_GAP` points of
it — a table border always has both.

    python thesis/scripts/check_rules.py                    # the newest export
    python thesis/scripts/check_rules.py path/to/file.pdf   # one file

Needs `pymupdf`. Exit status is 1 if any stray rule is found, so it can gate a build.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "defense" / "docs"

# The one rule that is meant to be there: the abstracts divide the masthead from
# "General characteristics of the research" with a line. It sits on page 1, above
# the body, and is nothing like the stripe this script hunts.
ALLOWED: set[tuple[str, int]] = {
    ("abstract_en.pdf", 1),
    ("abstract_ru.pdf", 1),
    ("abstract_kz.pdf", 1),
}

_STAMP = re.compile(r"_GOST_(\d{4}-\d{2}-\d{2})\.pdf$")

MIN_WIDTH_FRAC = 0.35  # of page width — narrower is a fragment, not a rule
MAX_THICK = 6.0        # pt — a taller filled rect is a figure, not a rule
V_GAP = 24.0           # pt — a table frame always has a neighbour closer than this
TOUCH = 3.0            # pt — tolerance for "a vertical stroke meets this line"


def _segments(page: pymupdf.Page) -> tuple[list[tuple[float, float, float]],
                                            list[tuple[float, float, float]]]:
    """Split a page's vector drawings into horizontal and vertical strokes.

    Args:
        page: The page to read.

    Returns:
        (horizontals, verticals) as (x0, x1, y) and (y0, y1, x) tuples.
    """
    horizontals: list[tuple[float, float, float]] = []
    verticals: list[tuple[float, float, float]] = []
    for drawing in page.get_drawings():
        for item in drawing["items"]:
            if item[0] == "l":
                p, q = item[1], item[2]
                if abs(p.y - q.y) <= 1.0:
                    horizontals.append((min(p.x, q.x), max(p.x, q.x), (p.y + q.y) / 2))
                elif abs(p.x - q.x) <= 1.0:
                    verticals.append((min(p.y, q.y), max(p.y, q.y), (p.x + q.x) / 2))
            elif item[0] == "re":
                r = item[1]
                if r.height <= MAX_THICK and r.width > r.height:
                    horizontals.append((r.x0, r.x1, (r.y0 + r.y1) / 2))
                elif r.width <= MAX_THICK and r.height > r.width:
                    verticals.append((r.y0, r.y1, (r.x0 + r.x1) / 2))
    return horizontals, verticals


def _text_above(page: pymupdf.Page, y: float) -> str:
    """Return the text block closest above `y`, trimmed for reporting.

    Args:
        page: The page the rule was found on.
        y: Vertical position of the rule, in points.

    Returns:
        Up to 90 characters of the nearest text above, or "" if there is none.
    """
    best, best_distance = "", float("inf")
    for _, y0, _, y1, text, *_ in page.get_text("blocks"):
        distance = y - (y0 + y1) / 2
        if 0 < distance < best_distance:
            best_distance, best = distance, " ".join(text.split())[:90]
    return best


def scan(path: Path) -> list[tuple[int, float, str]]:
    """Find every stray horizontal rule in one PDF.

    Args:
        path: The PDF to scan.

    Returns:
        One (page number, y, text above) triple per stray rule, in reading order.
    """
    hits: list[tuple[int, float, str]] = []
    with pymupdf.open(path) as doc:
        for pno, page in enumerate(doc, start=1):
            width = page.rect.width
            horizontals, verticals = _segments(page)
            for x0, x1, y in horizontals:
                if (x1 - x0) < MIN_WIDTH_FRAC * width:
                    continue
                if any(v0 - TOUCH <= y <= v1 + TOUCH and x0 - TOUCH <= vx <= x1 + TOUCH
                       for v0, v1, vx in verticals):
                    continue
                if any(0.5 < abs(oy - y) < V_GAP and not (ox1 < x0 - 5 or ox0 > x1 + 5)
                       for ox0, ox1, oy in horizontals):
                    continue
                hits.append((pno, round(y, 1), _text_above(page, y)))
    return hits


def current_build() -> list[Path]:
    """Every PDF of the newest dated export, plus the undated deliverables.

    Earlier dated builds are shipped history and are left alone: they carry the
    stripes this script was written for, and re-exporting them would rewrite
    documents the council has already been given.

    Returns:
        The PDFs to scan, in path order.
    """
    stamps = {m.group(1) for p in DOCS.rglob("*.pdf") if (m := _STAMP.search(p.name))}
    newest = max(stamps, default=None)
    return sorted(p for p in DOCS.rglob("*.pdf")
                  if (m := _STAMP.search(p.name)) is None or m.group(1) == newest)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("pdfs", type=Path, nargs="*",
                    help="PDFs to scan (default: the newest export under defense/docs)")
    args = ap.parse_args()

    targets = args.pdfs or current_build()
    if not targets:
        sys.exit("no PDFs to scan")

    total = 0
    for pdf in targets:
        hits = [h for h in scan(pdf) if (pdf.name, h[0]) not in ALLOWED]
        total += len(hits)
        if hits:
            print(pdf.relative_to(ROOT) if ROOT in pdf.parents else pdf)
            for pno, y, above in hits:
                print(f"  p.{pno:<4} y={y:<7} after: {above}")
    print(f"{len(targets)} file(s) scanned, {total} stray rule(s)")
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
