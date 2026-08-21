#!/usr/bin/env python3
"""Assemble the intermediate EN manuscript from approved PART 1 draft bodies.

Per thesis/prompts/citation-assembly.md INPUTS#1: concatenate PART 1 section
bodies only, in Table-of-Contents order; omit the draft header blockquote, the
PART 3 Compliance Checklist, and the Word-count block. Citations are LEFT in
their working author-year form (Stage G conversion is deferred until the full
manuscript is assembled). This is a reversible, read-only-source operation.

--------------------------------------------------------------------------
TWO DEFECTS FIXED 2026-08-11 (both would have produced a silently wrong book)
--------------------------------------------------------------------------
1. **Missing PART-1 markers.** The original extractor returned an empty body
   for any draft lacking a literal ``## PART 1`` line. Chapters 1/2/3/6/0/7
   carry that marker; **Chapter 4 carries it in only 3 of 20 drafts and
   Chapter 5 in none of 7** — those drafts open directly with their own ``##``
   section heading. 24 sections would have assembled as empty, and nothing in
   the output would have said so. ``extract()`` now falls back to "start at the
   top, after any ``# `` title line and ``> `` header blockquote", and the run
   reports any section whose body comes out suspiciously short.

2. **Chapter 0 cannot be ordered numerically.** Section *identifiers* in
   Chapter 0 are stable and deliberately do not follow manuscript order
   (§0.8 = Provisions Submitted for Defence, referenced across governance).
   The manuscript order is ``outline/TABLE_OF_CONTENTS_EN.md``'s. For every
   other chapter numeric sort == TOC order; **for Chapter 0 it does not**, so
   Chapter 0 is assembled from the explicit list in ``ORDER_OVERRIDE`` and a
   mismatch between that list and the files on disk is a hard error.

Also added in the same pass: Chapters 0, 5 and 7 to ``CHAPTERS`` (previously
absent, so the assembler could not produce a complete manuscript at all), and
the three front-matter units from ``thesis/output/``, which are authored there
as council deliverables and are not re-drafted under ``chapters/``.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path
from datetime import date

THESIS = Path(__file__).resolve().parent.parent
CH_ROOT = THESIS / "chapters"
OUT_DIR = THESIS / "output"
OUT = Path(__file__).resolve().parent / f"DISSERTATION_EN_partial_{date.today()}.md"

# Front matter, authored in thesis/output/ as council deliverables (EN/KZ,
# exported to GOST docx/pdf) and NOT re-drafted under chapters/00-introduction.
# Inserted ahead of the Introduction, in house order.
FRONT_MATTER = [
    "normative_references_en.md",
    "definitions_en.md",
    "abbreviations_en.md",
]

# Chapter dir -> TOC chapter heading, in manuscript order.
# Four chapters, in the order review -> methods -> experiments -> system, which is
# the shape 15 of 16 dissertations published by this council use. The superseded
# six-chapter tree is kept under chapters/_superseded/ and is not assembled.
CHAPTERS = [
    ("00-introduction", "INTRODUCTION"),
    ("01-review", "1 AUTOMATED DIABETIC RETINOPATHY SCREENING"),
    ("02-methodology", "2 METHODOLOGY OF THE INTEGRATED PIPELINE"),
    ("03-experiments", "3 EXPERIMENTAL RESULTS"),
    ("04-system", "4 THE SCREENING SYSTEM"),
    ("05-conclusion", "CONCLUSION"),
    # No umbrella heading: an "APPENDICES"/"ҚОСЫМШАЛАР" divider is the only
    # top-level heading with no body of its own, so it printed as a lone word on
    # an otherwise blank page, and contents_*.md lists the appendices
    # individually with no such entry. The appendices open straight at Appendix A.
    ("06-appendices", None),
]

# Chapters whose manuscript order is NOT the numeric order of their section
# identifiers. The Introduction is now a single continuous section with bold
# run-in rubrics, so it no longer needs an order override; none of the four body
# chapters does either, because their identifiers sort into manuscript order.
# The dict is kept so a future exception has somewhere to go.
ORDER_OVERRIDE: dict[str, list[str]] = {}

BODY_END = re.compile(r"^(## PART [23]\b|### Word count\b|## ⚠ PHASE-3 OBLIGATION\b)", re.I)
PART1_HDR = re.compile(r"^## PART 1\b", re.I)
SHORT_BODY_WORDS = 60  # below this, a body is almost certainly a mis-extraction


def section_key(p: Path):
    stem = p.name.replace("-draft.md", "")
    toks = []
    for t in stem.split("."):
        if t.isdigit():
            toks.append((0, int(t), ""))
        else:  # 'C' (conclusion) and appendix letters sort after numerics
            toks.append((1, 0, t))
    return toks


def ordered_files(cdir: str, d: Path) -> list[Path]:
    """Files in manuscript order, honouring ORDER_OVERRIDE."""
    files = list(d.glob("*-draft.md"))
    if cdir not in ORDER_OVERRIDE:
        return sorted(files, key=section_key)

    by_id = {f.name.replace("-draft.md", ""): f for f in files}
    want = ORDER_OVERRIDE[cdir]
    missing = [s for s in want if s not in by_id]
    extra = [s for s in by_id if s not in want]
    if missing or extra:
        raise SystemExit(
            f"ORDER_OVERRIDE for {cdir} does not match the drafts on disk.\n"
            f"  listed but absent: {missing or 'none'}\n"
            f"  present but unlisted: {extra or 'none'}\n"
            "Chapter 0 must not be assembled by numeric sort — update the list."
        )
    return [by_id[s] for s in want]


def extract(p: Path):
    """Return (title, body, word_count).

    Prefers an explicit '## PART 1' marker. Falls back to the top of the file
    when the draft has none, skipping a leading '# ' title line and a leading
    '> ' header blockquote. `title` is returned only when the draft carries a
    '# ' line; drafts without one already open with their own '##' heading and
    must not have anything prepended.
    """
    lines = p.read_text(encoding="utf-8").splitlines()
    title = next((l for l in lines if l.startswith("# ")), None)

    marker = next((i for i, l in enumerate(lines) if PART1_HDR.match(l)), None)
    if marker is not None:
        start = marker + 1
    else:
        # No PART-1 marker (Chapter 4 / Chapter 5 house style): start at the
        # top, skipping a title line and a header blockquote if present.
        start = 0
        while start < len(lines):
            s = lines[start].strip()
            if s == "" or s == "---" or s.startswith("> ") or lines[start].startswith("# "):
                start += 1
                continue
            break

    body = []
    for l in lines[start:]:
        if BODY_END.match(l):
            break
        body.append(l)

    # trim leading/trailing blanks and stray '---' separators
    while body and body[0].strip() in ("", "---"):
        body.pop(0)
    while body and body[-1].strip() in ("", "---"):
        body.pop()

    text = "\n".join(body)
    words = len(re.findall(r"\S+", text))
    return title, text, words


def main():
    out = []
    manifest = []
    suspect = []

    out.append("# Automated Diabetic Retinopathy Diagnosis via Fundus Image "
               "Enhancement and CNN Classification")
    out.append("")
    out.append(f"> **Intermediate EN assembly — {date.today()}.** Concatenation of "
               "PART 1 draft bodies in Table-of-Contents order, preceded by the "
               "three front-matter units authored in `thesis/output/`. Four "
               "chapters, review to system, with five appendices. Working "
               "author-year citations are unconverted (GOST `[N]` is a deferred "
               "single pass). Compliance checklists, draft headers, and word-count "
               "blocks are excluded. **NOT the final bound thesis:** figure and "
               "table markers are unresolved, and the page, figure, table and "
               "source counts declared in the Introduction's closing rubric are "
               "set from the exported volume rather than from this file.")
    out.append("")

    # ---- front matter -----------------------------------------------------
    for fname in FRONT_MATTER:
        fm = OUT_DIR / fname
        if not fm.exists():
            suspect.append((fname, "MISSING front-matter file"))
            continue
        out.append("\n---\n")
        out.append(fm.read_text(encoding="utf-8").strip())
        out.append("")

    total_words = 0
    for cdir, heading in CHAPTERS:
        d = CH_ROOT / cdir / "drafts"
        if not d.is_dir():
            continue
        files = ordered_files(cdir, d)
        if not files:
            continue
        out.append("\n---\n")
        if heading:
            out.append(f"# {heading}")
            out.append("")
        for f in files:
            title, text, words = extract(f)
            total_words += words
            manifest.append((f"{cdir}/{f.name}", words))
            if words < SHORT_BODY_WORDS:
                suspect.append((f.name, f"body extracted as {words} words"))
            # Drafts without a '# ' title line already carry their own heading.
            out.append(text if (title is None or title in text) else f"{title}\n\n{text}")
            out.append("")

    OUT.write_text("\n".join(out), encoding="utf-8")
    print(f"WROTE {OUT}")
    print(f"Sections: {len(manifest)} | Total PART-1 words: {total_words:,}")

    if suspect:
        print("\n!! SUSPECT EXTRACTIONS — check before using this assembly:")
        for name, why in suspect:
            print(f"   {name}: {why}")
        print("   (a near-empty body usually means the draft's structure differs "
              "from both supported house styles)")
    else:
        print("\nNo suspect extractions.")

    print("\n# file -> words")
    for name, w in manifest:
        print(f"  {name:46s} {w:6,d}")

    return 1 if suspect else 0


if __name__ == "__main__":
    sys.exit(main())
