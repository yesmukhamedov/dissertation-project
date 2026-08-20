"""Measure an assembled manuscript against the council's observed norms.

The norms are not the Instruction's ceilings but what the council actually
receives: measured across all 16 dissertations it has published and recorded in
`council/en/10-dissertation/peer-norms.md` (sections 1, 6, 7, 8). This script
turns that file into a gate, so "the volume is in genre" is a check that runs
rather than a judgement made by eye.

It reads the assembled Markdown — `thesis/assembly/DISSERTATION_{EN,KZ}_GOST_*.md`
— which is the last artefact before Word, and therefore the last point at which a
defect is cheap to fix.

    python thesis/scripts/conformance.py                # newest EN + KZ pair
    python thesis/scripts/conformance.py --lang en
    python thesis/scripts/conformance.py path/to/manuscript.md

Exit status is 1 if any metric fails, so it can gate a build.
"""
from __future__ import annotations

import argparse
import re
import statistics
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ASSEMBLY = ROOT / "thesis" / "assembly"

# --- Where the main text starts and stops ------------------------------------
# The corpus measures "main text" as Introduction → the last page before the
# reference list; the reference list and the appendices are counted separately
# and the appendices do not enter the declared volume at all.
_MAIN_START = re.compile(r"^#+\s+(?:INTRODUCTION|КІРІСПЕ)\s*$", re.IGNORECASE)
_MAIN_END = re.compile(
    r"^#+\s+(?:LIST\s+OF\s+REFERENCES|ПАЙДАЛАНЫЛҒАН\s+ӘДЕБИЕТТЕР)", re.IGNORECASE
)

_HEADING = re.compile(r"^(#+)\s+(.*?)\s*$")
_NUMBERED = re.compile(r"^(?:§\s*)?(\d+(?:\.\d+)*)\.?\s+(.*)$")
# Captions are authored in an English prefix form ("**Table 4.4. Title**") and
# a Kazakh postfix form ("**2.1-кесте. Атауы**"); md2gost normalises them at
# conversion, but the source shape is what is seen here.
_TABLE_CAPTION = re.compile(
    r"^\*\*(?:(?:Table|Кесте|Таблица)\s+[\w.]+|[\w.]+-кесте)", re.IGNORECASE
)
_FIGURE_CAPTION = re.compile(r"^\*\*(?:Figure|Сурет|[\w.]+-сурет)\b", re.IGNORECASE)
_BOLD = re.compile(r"\*\*(.+?)\*\*", re.DOTALL)
_FENCE = re.compile(r"^\s*```")

# Internal notation that no sample in the corpus prints. The prefixes are this
# project's own governance vocabulary (hypotheses, scope boundaries, operational
# definitions, source-integrity rules, non-claims, contributions).
_INTERNAL_CODE = re.compile(r"\b(?:H|SB|OD|SIR|NC|CFC|SC|AOQ|IT|EH|DIA|PC)-\d+(?:\.\d+)*\b")
_EDITORIAL = re.compile(r"\[VERIFY\b|\bTODO\b|\bTBD\b|\bFIXME\b")

# `[FIG-…]` / `[TAB-…]` are asset markers, not residue: md2gost resolves each to
# its image or table at conversion. They are reported separately rather than
# failed, because their presence in the Markdown is normal — but one md2gost
# cannot resolve is printed verbatim, which is how a marker reaches the PDF.
_ASSET_MARKER = re.compile(r"\[(?:TAB|FIG)-[\w.]+")

# A sentence ends at . ! ? followed by whitespace and something that starts a new
# sentence. Decimal numbers, "e.g." and initials would otherwise each end one, so
# the split refuses to break after a digit or a single capital.
_SENTENCE_SPLIT = re.compile(r"(?<![0-9])(?<![A-ZА-ЯӘ])[.!?]+[)\"'»]?\s+(?=[^a-zа-яәөұүқғңһ])")


@dataclass
class Check:
    name: str
    value: object
    ok: bool
    norm: str

    def line(self) -> str:
        mark = "PASS" if self.ok else "FAIL"
        return f"  [{mark}] {self.name:<34} {str(self.value):>12}   norm: {self.norm}"


def _words(text: str) -> int:
    return len(text.split())


def split_sections(md: str) -> tuple[list[str], list[tuple[int, str]]]:
    """(main-text lines, headings as (level, text)) for the whole document."""
    lines = md.splitlines()
    headings: list[tuple[int, str]] = []
    for ln in lines:
        m = _HEADING.match(ln)
        if m:
            headings.append((len(m.group(1)), m.group(2)))

    start = end = None
    for i, ln in enumerate(lines):
        if start is None and _MAIN_START.match(ln):
            start = i
        elif start is not None and _MAIN_END.match(ln):
            end = i
            break
    if start is None:
        raise SystemExit("could not find the Introduction heading — is this an assembled manuscript?")
    return lines[start:end if end is not None else len(lines)], headings


def prose_paragraphs(main_lines: list[str]) -> list[str]:
    """Body paragraphs only — headings, tables, captions, code and quotes excluded.

    These are the units the corpus's 36-word median is a median of, so anything
    that is not running prose has to stay out or the figure is not comparable.
    """
    paras: list[str] = []
    buf: list[str] = []
    in_fence = False

    def flush() -> None:
        if buf:
            text = " ".join(buf).strip()
            if text:
                paras.append(text)
            buf.clear()

    for ln in main_lines:
        if _FENCE.match(ln):
            in_fence = not in_fence
            flush()
            continue
        if in_fence:
            continue
        s = ln.strip()
        if not s:
            flush()
            continue
        if (s.startswith("#") or s.startswith("|") or s.startswith(">")
                or s.startswith("---") or s.startswith("![")
                or _TABLE_CAPTION.match(s) or _FIGURE_CAPTION.match(s)
                or re.match(r"^[-*+]\s|^\d+[.)]\s", s)):
            flush()
            continue
        buf.append(s)
    flush()
    return paras


def sentences(paragraphs: list[str]) -> list[str]:
    out: list[str] = []
    for p in paragraphs:
        out.extend(s for s in (x.strip() for x in _SENTENCE_SPLIT.split(p)) if s)
    return out


def contents_entries(lang: str) -> list[str] | None:
    """Heading texts promised by the contents file, or None if it cannot be read."""
    path = ROOT / "thesis" / "output" / f"contents_{lang}.md"
    if not path.is_file():
        return None
    entries: list[str] = []
    for ln in path.read_text(encoding="utf-8").splitlines():
        s = ln.strip().lstrip("-*").strip()
        if not s or s.startswith("#") or s.startswith("|"):
            continue
        s = re.sub(r"\s*\.{2,}\s*\d+\s*$", "", s)      # dot leaders + page number
        s = re.sub(r"\s*\t\s*\d+\s*$", "", s)
        s = s.strip("* ").strip()
        if s:
            entries.append(s)
    return entries or None


def analyse(md_path: Path, lang: str) -> list[Check]:
    md = md_path.read_text(encoding="utf-8")
    main_lines, headings = split_sections(md)
    main = "\n".join(main_lines)
    paras = prose_paragraphs(main_lines)
    sents = sentences(paras)
    total_words = sum(_words(p) for p in paras)

    para_words = [_words(p) for p in paras] or [0]
    sent_words = [_words(s) for s in sents] or [0]
    bold_words = sum(_words(m) for m in _BOLD.findall(main))
    em_dashes = main.count("—")

    # Headings inside the main text only — the appendices carry their own scheme.
    main_headings = [h for h in
                     (_HEADING.match(ln) for ln in main_lines) if h]
    numbered = []
    max_depth = 0
    for h in main_headings:
        m = _NUMBERED.match(h.group(2))
        if not m:
            continue
        depth = m.group(1).count(".") + 1
        max_depth = max(max_depth, depth)
        numbered.append((depth, m.group(2)))
    second_level = [t for d, t in numbered if d == 2]
    sl_words = [_words(t) for t in second_level] or [0]

    tables = sum(1 for ln in main_lines if _TABLE_CAPTION.match(ln.strip()))

    checks = [
        Check("main-text words", total_words,
              22_000 <= total_words <= 31_000, "22,000–31,000 (corpus 15,200–31,000)"),
        Check("median words / paragraph", round(statistics.median(para_words), 1),
              statistics.median(para_words) <= 60, "<= 60 (corpus median 36)"),
        Check("median words / sentence", round(statistics.median(sent_words), 1),
              statistics.median(sent_words) <= 25, "<= 25 (corpus median 18)"),
        Check("paragraphs over 173 words",
              sum(1 for w in para_words if w > 173),
              sum(1 for w in para_words if w > 173) <= len(para_words) * 0.02,
              "<= 2% (corpus 99th percentile is 173)"),
        Check("section signs", main.count("§"), main.count("§") == 0,
              "0 (corpus: 0 in 6.16M characters)"),
        Check("internal codes", len(_INTERNAL_CODE.findall(main)),
              not _INTERNAL_CODE.search(main), "0 (corpus: none printed)"),
        Check("editorial markers", len(_EDITORIAL.findall(main)),
              not _EDITORIAL.search(main), "0 — none survive into any of the 16"),
        Check("asset markers (resolved at export)", len(_ASSET_MARKER.findall(main)),
              True, "informational — verify none reaches the PDF"),
        Check("max heading depth", max_depth, 0 < max_depth <= 3,
              "<= 3 levels (4th in 0 of 16)"),
        Check("second-level subsections", len(second_level),
              13 <= len(second_level) <= 34, "13–34 (corpus median 21)"),
        Check("median words / 2nd-level title", round(statistics.median(sl_words), 1),
              statistics.median(sl_words) <= 6, "<= 6 (corpus median 5)"),
        Check("longest 2nd-level title", max(sl_words),
              max(sl_words) <= 13, "<= 13 words"),
        Check("em dashes per 1,000 words",
              round(em_dashes / max(total_words, 1) * 1000, 2),
              em_dashes / max(total_words, 1) * 1000 <= 0.7,
              "<= 0.7 (13 of 16 samples)"),
        Check("bold share of words",
              f"{bold_words / max(total_words, 1) * 100:.2f}%",
              bold_words / max(total_words, 1) <= 0.014, "<= 1.4%"),
        Check("tables in the body", tables, tables <= 20, "<= 20 (corpus max 19)"),
    ]

    entries = contents_entries(lang)
    if entries is not None:
        body_titles = {re.sub(r"\s+", " ", h.group(2)).strip() for h in main_headings}
        promised = {re.sub(r"\s+", " ", e).strip() for e in entries}
        missing = sorted(p for p in promised
                         if p not in body_titles
                         and not any(p in b or b in p for b in body_titles))
        checks.append(Check("contents entries absent from body", len(missing),
                            not missing, "0 — the contents must reproduce the body"))
        if missing:
            checks.append(Check("  first missing entry", missing[0][:40], False, ""))
    return checks


def newest(lang: str) -> Path:
    files = sorted(ASSEMBLY.glob(f"DISSERTATION_{lang.upper()}_GOST_*.md"))
    if not files:
        raise SystemExit(f"no assembled {lang.upper()} manuscript in {ASSEMBLY}")
    return files[-1]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("path", nargs="?", type=Path, help="manuscript .md (default: newest pair)")
    ap.add_argument("--lang", choices=["en", "kz"], help="restrict to one edition")
    args = ap.parse_args()

    if args.path:
        targets = [(args.path, args.lang or ("kz" if "_KZ_" in args.path.name else "en"))]
    else:
        langs = [args.lang] if args.lang else ["en", "kz"]
        targets = [(newest(l), l) for l in langs]

    failed = False
    for path, lang in targets:
        print(f"\n{path.name}  [{lang.upper()}]")
        checks = analyse(path, lang)
        for c in checks:
            print(c.line())
        n_bad = sum(1 for c in checks if not c.ok)
        failed |= bool(n_bad)
        print(f"  {len(checks) - n_bad}/{len(checks)} pass")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
