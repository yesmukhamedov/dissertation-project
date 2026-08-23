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
#
# The appendices heading ends the main text as surely as the reference list does.
# It has to be listed, because the intermediate assembly carries no reference list
# — citations are resolved in a later pass — and without it the appendices were
# counted into the volume, failing the word and table gates on a manuscript that
# passes both.
_MAIN_START = re.compile(r"^#+\s+(?:INTRODUCTION|КІРІСПЕ)\s*$", re.IGNORECASE)
_MAIN_END = re.compile(
    r"^#+\s+(?:LIST\s+OF\s+REFERENCES|ПАЙДАЛАНЫЛҒАН\s+ӘДЕБИЕТТЕР"
    r"|APPENDICES|APPENDIX\b|ҚОСЫМШАЛАР"
    # The umbrella "APPENDICES"/"ҚОСЫМШАЛАР" divider was dropped from the
    # manuscript (it rendered as a lone word on a blank page), so the KZ
    # appendices open at their first appendix heading; match that form too —
    # "ҚОСЫМША А" as the corpus sets it, and the superseded "А қосымшасы".
    r"|ҚОСЫМША\s+[А-ЯЁӘҒҚҢӨҰҮҺІ]\b"
    r"|\S+\s+ҚОСЫМШАСЫ\b)", re.IGNORECASE
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

# The same vocabulary in the *unnumbered* form a glossary entry gives it — "PC-n",
# "SB-n". The body check above never saw those, and nor did anything else: the front
# matter is authored in thesis/output/ and inserted by the assemblers ahead of the
# Introduction, which is exactly where `split_sections` starts reading. So eight
# governance labels (PC/CFC/EH/SIR/DGL/SB/NC/OD-n) sat defined in "Designations and
# abbreviations" of both editions, used nowhere in either volume, until an external
# reader of the Kazakh PDF asked where the apparatus they describe is written down
# (2026-08-23). They are rules for how the text may make claims — not terms of the
# subject — and a reader who meets one in the abbreviations list is owed the
# apparatus itself. They were removed; this is what keeps them out.
_GOVERNANCE_LABEL = re.compile(
    r"\b(?:H|SB|OD|SIR|NC|CFC|SC|AOQ|IT|EH|DIA|PC|DGL)-(?:\d+(?:\.\d+)*|n)\b"
)

# Front matter and the council deliverables beside it. None is inside the assembled
# main text, so all of it is checked from source rather than from the manuscript.
_FRONT_MATTER = ("normative_references", "definitions", "abbreviations", "abstract")

# `[FIG-…]` / `[TAB-…]` are asset markers, not residue: md2gost resolves each to
# its image or table at conversion. They are reported separately rather than
# failed, because their presence in the Markdown is normal — but one md2gost
# cannot resolve is printed verbatim, which is how a marker reaches the PDF.
_ASSET_MARKER = re.compile(r"\[(?:TAB|FIG)-[\w.]+")

# The whole bracketed span. md2gost replaces an inline marker with a
# cross-reference ("Figure 3.1") and emits the image after the paragraph, so
# for measurement the marker stands for two printed words, not for its own
# caption text and file path. Counting those would inflate the word count and
# charge the prose for a dash that never reaches the page.
_ASSET_SPAN = re.compile(r"\[(?:TAB|FIG)-[^\]]*\]")

# --- Kazakh register: is the volume written in Kazakh, or carried over from English?
#
# The Kazakh edition is the volume actually defended, and it is a translation of the
# English one. That makes one failure mode specific to it: English syntax surviving
# the translation under Kazakh words. Two constructions carry it, and both were
# measured against two other Kazakh-language dissertations of this council (Ибраева,
# Тоқтарова) in an external reading of the 2026-08-23 PDF:
#
#   * `et al.` rendered word-for-word as "және әріптестері" — 77 uses, against 0 in
#     either comparator, while the Kazakh norm "т.б." appeared 0 times against their
#     18 and 12. The literature list itself carried Latin "[et al.]" throughout. The
#     norm is "т.б."; `_finalize_citations.py` has always parsed both.
#   * "…, сондықтан …" mid-sentence — 121 uses against 6 and 11. In Kazakh
#     "сондықтан" opens a sentence; joined to the previous clause by a comma it is
#     English "…, so …" with Kazakh vocabulary. The idiomatic forms are the causal
#     suffix (-дықтан/-діктен) or a new sentence.
#
# Both were repaired on 2026-08-23. The ceiling below is the comparators' own range,
# not zero: the construction is not ungrammatical, only foreign in that density.
_KZ_ETAL_CALQUE = re.compile(r"және\s+әріптестер\w*")
_KZ_MIDSENTENCE_SO = re.compile(r",\s*сондықтан\b")

# The third finding of the same reading was uniformity: one connective doing all the
# work. "Демек," ran to 35 uses with no alternative anywhere in the volume, which is
# the signature of a text produced in one pass rather than written. Kazakh has a full
# set here; the check asks that no single member take more than half the family.
_KZ_CONNECTIVES = {
    "Сондықтан": r"\bСондықтан\b",
    "Демек": r"\bДемек,",
    "Сол себепті": r"[Сс]ол себепті",
    "Тиісінше": r"\bТиісінше,",
    "Сонымен": r"\bСонымен,",
    "Осылайша": r"\bОсылайша,",
    "Яғни": r"\bЯғни,",
}

# A sentence ends at . ! ? followed by whitespace and a capital letter.
#
# Two earlier guards were wrong and both inflated the measurement. Refusing to
# break after a digit was meant to protect decimals, but a decimal has no
# whitespace after its point, so the trailing `\s+` already protects it; what the
# guard actually did was weld every sentence ending in a number onto the next one
# ("… gave p = 0.0056. The corresponding z values …" measured as one 56-word
# sentence). And refusing to break after any capital was meant to protect
# initials, but it also welded every sentence ending in EyePACS, IDRiD or CNN.
# The initials case is handled by requiring the capital to be a lone one, and a
# new sentence is required to open with a capital rather than merely with a
# non-lowercase character, which keeps "Porwal et al. (2018)" whole.
_SENTENCE_SPLIT = re.compile(
    r"(?<!\s[A-Z])[.!?]+[)\"'»]?\s+(?=[A-ZА-ЯӘӨҰҮҚҒҢҺ])"
)


@dataclass
class Check:
    name: str
    value: object
    ok: bool
    norm: str

    def line(self) -> str:
        mark = "PASS" if self.ok else "FAIL"
        return f"  [{mark}] {self.name:<34} {str(self.value):>12}   norm: {self.norm}"


# Drafts carry citations as `Gulshan et al. (2016)` or `(Zhou et al., 2022; Wang
# and Deng, 2018)`, and the citation pass (thesis/prompts/citation-assembly.md,
# step 4) converts them before the volume is typeset. Counting the working form
# measures text that is never printed, so each is rewritten here into the form
# the reader gets.
#
# The two forms do NOT converge on one token, and treating them as if they did
# understated the volume by 261 words — enough to report a manuscript inside the
# corpus cap that is over it once the citations are in print. A parenthetical
# collapses to a bare `[12]`, however many sources it names; a narrative citation
# KEEPS its author phrase as the sentence subject and only the year becomes the
# bracket, so `Gulshan et al. (2016)` prints as four words, not one.
_CITE_NARR = re.compile(
    r"\b([A-Z][A-Za-z'’\-]+"
    r"(?:\s+(?:and|&)\s+[A-Z][A-Za-z'’\-]+)?"
    r"(?:\s+et\s+al\.)?)\s+\((?:19|20)\d{2}[a-z]?\)"
)
_CITE_PAREN = re.compile(r"\(\s*[^()]*?(?:19|20)\d{2}[a-z]?\s*(?:[;,][^()]*?)?\)")


def _collapse_citations(text: str) -> str:
    """Every working citation in the shape the printed volume gives it."""
    text = _CITE_NARR.sub(r"\1 [CITE]", text)
    return _CITE_PAREN.sub("[CITE]", text)


def _words(text: str) -> int:
    return len(_collapse_citations(text).split())


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
        buf.append(_ASSET_SPAN.sub("Figure 0.0", s))
    flush()
    return paras


def sentences(paragraphs: list[str]) -> list[str]:
    """Split into sentences, with emphasis markers removed first.

    The Introduction's rubrics are bold run-in headings — `**Relevance.** The …` —
    and the closing `**` sits between the full stop and the space, so the splitter
    saw no sentence boundary and measured the rubric and its first sentence as one.
    The markers are not printed, so they are removed before splitting. Bold share
    is measured separately, on the unstripped prose, and is unaffected.
    """
    out: list[str] = []
    for p in paragraphs:
        p = p.replace("**", "").replace("__", "")
        out.extend(s for s in (x.strip() for x in _SENTENCE_SPLIT.split(p)) if s)
    return out


def contents_entries(lang: str) -> list[str] | None:
    """Main-text heading texts promised by the contents, or None if unreadable.

    Scoped to the main text on the same boundaries the body is, because that is
    what it is compared against: the front matter above the Introduction, the
    reference list and the appendices are structural elements the body scan stops
    at, and leaving them in the promise makes nine entries permanently unmatched.
    """
    path = ROOT / "thesis" / "output" / f"contents_{lang}.md"
    if not path.is_file():
        return None
    entries: list[str] = []
    started = False
    for ln in path.read_text(encoding="utf-8").splitlines():
        s = ln.strip()
        # Numbered subsections are heading lines, not bullets, and they are the
        # entries this check exists for: the promise the body has to keep. Only
        # the document title (a single '# ') is skipped.
        if s.startswith("##"):
            s = s.lstrip("#").strip()
        elif s.startswith("#"):
            continue
        s = s.lstrip("-*").strip()
        if not s or s.startswith("|"):
            continue
        s = re.sub(r"\s*\.{2,}\s*\d+\s*$", "", s)      # dot leaders + page number
        s = re.sub(r"\s*\t\s*\d+\s*$", "", s)
        s = s.strip("* ").strip()
        if not s:
            continue
        if not started:
            started = bool(_MAIN_START.match(f"# {s}"))
            continue
        if _MAIN_END.match(f"# {s}"):
            break
        entries.append(s)
    return entries or None


def front_matter_labels(lang: str) -> list[tuple[str, str]]:
    """Governance labels found in the front matter, as (file stem, label).

    The assembled manuscript begins at the Introduction, so nothing above it is ever
    reached by the body checks. These files are read from `thesis/output/` instead.
    """
    out: list[tuple[str, str]] = []
    for stem in _FRONT_MATTER:
        path = ROOT / "thesis" / "output" / f"{stem}_{lang}.md"
        if not path.is_file():
            continue
        for label in _GOVERNANCE_LABEL.findall(path.read_text(encoding="utf-8")):
            out.append((path.stem, label))
    return out


def kazakh_register(prose: str) -> list[Check]:
    """The three register checks that apply only to the Kazakh edition."""
    etal = len(_KZ_ETAL_CALQUE.findall(prose))
    mid_so = len(_KZ_MIDSENTENCE_SO.findall(prose))
    counts = {name: len(re.findall(pat, prose)) for name, pat in _KZ_CONNECTIVES.items()}
    total = sum(counts.values())
    top, top_n = max(counts.items(), key=lambda kv: kv[1]) if total else ("—", 0)
    share = top_n / total if total else 0.0
    return [
        Check("«және әріптестері» (et al. calque)", etal, etal == 0,
              "0 — the Kazakh norm is «т.б.» (comparators: 0 and 0)"),
        Check("«, сондықтан» mid-sentence", mid_so, mid_so <= 12,
              "<= 12 (comparators 6 and 11; this volume once had 121)"),
        Check(f"top connective share ({top})", f"{share * 100:.0f}%",
              share <= 0.55,
              "<= 55% of the connective family — one doing all the work reads as one pass"),
    ]


def analyse(md_path: Path, lang: str) -> list[Check]:
    md = md_path.read_text(encoding="utf-8")
    main_lines, headings = split_sections(md)
    main = "\n".join(main_lines)
    paras = prose_paragraphs(main_lines)
    sents = sentences(paras)
    total_words = sum(_words(p) for p in paras)

    para_words = [_words(p) for p in paras] or [0]
    sent_words = [_words(s) for s in sents] or [0]
    # Over prose only: captions and asset markers are not running text, and both
    # may legitimately carry bold and a dash.
    prose = "\n".join(paras)
    bold_words = sum(_words(m) for m in _BOLD.findall(prose))
    em_dashes = prose.count("—")

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
        # The ceiling was the corpus maximum (31,000, rounded from Наименко's
        # 30,9xx). It is raised to 31,500 by decision of the candidate: the
        # English edition measures 31,263 — 263 words over — and the volume
        # actually defended is the Kazakh one, which sits at 25,157. The corpus
        # range in the label stays what it is; the norm is now deliberately a
        # little wider than it, and the label says so rather than implying the
        # corpus reaches 31,500.
        Check("main-text words", total_words,
              22_000 <= total_words <= 31_500,
              "22,000–31,500 (corpus 15,200–31,000)"),
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

    fm = front_matter_labels(lang)
    checks.append(Check("governance labels in front matter", len(fm), not fm,
                        "0 — defined-but-unused apparatus is a finding, not a glossary"))
    if fm:
        checks.append(Check(f"  first is {fm[0][1]}", f"in {fm[0][0]}", False, ""))

    if lang == "kz":
        checks.extend(kazakh_register(prose))

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


# --- Per-section mode ---------------------------------------------------------
# A chapter is rewritten one subsection at a time, and a defect is cheapest to see
# in the section that carries it. This mode measures a single draft's PART-1 body
# against the same norms, so a section can be signed off before the next is begun.
_PART1 = re.compile(r"^##\s+PART 1\b", re.IGNORECASE)
_PART_END = re.compile(r"^(##\s+PART [23]\b|###\s+Word count\b|###\s+Norm compliance\b)",
                       re.IGNORECASE)


def section_body(path: Path) -> list[str]:
    """The PART-1 body lines of a draft, as the assembler would extract them."""
    lines = path.read_text(encoding="utf-8").splitlines()
    start = next((i + 1 for i, l in enumerate(lines) if _PART1.match(l)), 0)
    out = []
    for l in lines[start:]:
        if _PART_END.match(l):
            break
        out.append(l)
    return out


def _em_dash_captions(lines: list[str]) -> int:
    """Captions that separate label from title with an em dash instead of an en dash."""
    return sum(
        1 for l in lines
        if (_TABLE_CAPTION.match(l.strip()) or _FIGURE_CAPTION.match(l.strip()))
        and "—" in l.split("**")[1] if l.count("**") >= 2
    )


def analyse_section(path: Path, budget: int | None) -> list[Check]:
    body_lines = section_body(path)
    body = "\n".join(body_lines)
    paras = prose_paragraphs(body_lines)
    sents = sentences(paras)
    words = sum(_words(p) for p in paras)
    para_words = [_words(p) for p in paras] or [0]
    sent_words = [_words(s) for s in sents] or [0]
    prose = "\n".join(paras)
    bold_words = sum(_words(m) for m in _BOLD.findall(prose))
    em = prose.count("—")
    headings = [l for l in body_lines if _HEADING.match(l)]
    depth = 0
    for h in headings:
        m = _NUMBERED.match(_HEADING.match(h).group(2))
        if m:
            depth = max(depth, m.group(1).count(".") + 1)

    checks = [
        Check("prose words", words,
              budget is None or abs(words - budget) <= max(60, budget * 0.15),
              f"{budget} ± 15%" if budget else "no budget given"),
        Check("median words / paragraph", round(statistics.median(para_words), 1),
              statistics.median(para_words) <= 60, "<= 60 (corpus median 36)"),
        Check("longest paragraph", max(para_words),
              max(para_words) <= 173, "<= 173 (corpus 99th percentile)"),
        Check("median words / sentence", round(statistics.median(sent_words), 1),
              statistics.median(sent_words) <= 25, "<= 25 (corpus median 18)"),
        Check("longest sentence", max(sent_words),
              max(sent_words) <= 45, "<= 45"),
        Check("section signs", body.count("§"), body.count("§") == 0, "0"),
        Check("internal codes", len(_INTERNAL_CODE.findall(body)),
              not _INTERNAL_CODE.search(body), "0"),
        Check("editorial markers", len(_EDITORIAL.findall(body)),
              not _EDITORIAL.search(body), "0"),
        Check("em dashes", em, em == 0, "0 (<= 0.7 per 1,000 words)"),
        Check("bold share of words", f"{bold_words / max(words, 1) * 100:.2f}%",
              bold_words / max(words, 1) <= 0.014, "<= 1.4%"),
        Check("max heading depth", depth, depth <= 3, "<= 3"),
        Check("tables", sum(1 for l in body_lines if _TABLE_CAPTION.match(l.strip())),
              True, "informational — <= 20 in the body overall"),
        Check("captions using an em dash", _em_dash_captions(body_lines),
              _em_dash_captions(body_lines) == 0,
              "0 — the corpus dash in a caption is the en dash"),
    ]
    return checks


def show_offenders(path: Path, sent_max: int = 45, para_max: int = 100) -> None:
    """Print the sentences and paragraphs a rewrite still has to bring down.

    A failing median says a section is out of register; it does not say where. This
    names the units to fix, which is the whole difference between a gate and a
    diagnostic.
    """
    paras = prose_paragraphs(section_body(path))
    long_s = [(len(x.split()), x) for x in sentences(paras) if len(x.split()) > sent_max]
    long_p = [(len(x.split()), x) for x in paras if len(x.split()) > para_max]
    if long_s:
        print()
        print(f"  sentences over {sent_max} words:")
        for n, x in sorted(long_s, reverse=True):
            print(f"    [{n}] {x}")
    if long_p:
        print()
        print(f"  paragraphs over {para_max} words:")
        for n, x in sorted(long_p, reverse=True):
            print(f"    [{n}] {x[:160]}…")
    if not long_s and not long_p:
        print()
        print("  nothing over the per-unit limits.")


def newest(lang: str) -> Path:
    files = sorted(ASSEMBLY.glob(f"DISSERTATION_{lang.upper()}_GOST_*.md"))
    if not files:
        raise SystemExit(f"no assembled {lang.upper()} manuscript in {ASSEMBLY}")
    return files[-1]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("path", nargs="?", type=Path, help="manuscript .md (default: newest pair)")
    ap.add_argument("--lang", choices=["en", "kz"], help="restrict to one edition")
    ap.add_argument("--section", action="store_true",
                    help="measure one draft's PART-1 body instead of a whole manuscript")
    ap.add_argument("--budget", type=int, default=None,
                    help="word budget for --section, from outline/REWRITE_MAP.md")
    ap.add_argument("--show", action="store_true",
                    help="with --section, print the sentences and paragraphs that miss the norm")
    args = ap.parse_args()

    if args.section:
        if not args.path:
            raise SystemExit("--section needs a draft path")
        print(f"\n{args.path.name}")
        checks = analyse_section(args.path, args.budget)
        for c in checks:
            print(c.line())
        n_bad = sum(1 for c in checks if not c.ok)
        print(f"  {len(checks) - n_bad}/{len(checks)} pass")
        if args.show:
            show_offenders(args.path)
        sys.exit(1 if n_bad else 0)

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
