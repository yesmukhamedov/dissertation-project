#!/usr/bin/env python3
"""Assemble the intermediate KZ manuscript from approved translation bodies.

Mirror of `_assemble_en.py` for the Kazakh translations under
`chapters/**/translations/*-translation.md`. For each file it keeps the
`# §x Title` line plus the **1-БӨЛІК: БӨЛІМ МӘТІНІ** body only, dropping the
`> Қазақ тіліндегі аударма…` blockquote and the trailing `### Аудармашы ескертуі`
note. Chapters are concatenated in Table-of-Contents order
(outline/TABLE_OF_CONTENTS_KZ.md). Working author-year citations are left
unconverted (GOST `[N]` is a deferred single pass on the final manuscript).
This is a reversible, read-only-source operation.

--------------------------------------------------------------------------
TWO DEFECTS FIXED 2026-08-11 — the same pair repaired in `_assemble_en.py`
--------------------------------------------------------------------------
1. **Missing PART-1 markers.** The extractor returned an *empty body* for any
   file lacking a literal ``## 1-БӨЛІК`` line, and said nothing about it. In
   the EN tree this silently emptied 24 of 94 sections. It now falls back to
   "start at the top, after any ``# `` title line and ``> `` header
   blockquote", and reports any section whose body comes out suspiciously
   short instead of emitting it quietly.

2. **Chapter 0 cannot be ordered numerically.** Section *identifiers* in
   Chapter 0 are stable and deliberately do not follow manuscript order
   (§0.8 = Қорғауға ұсынылатын тұжырымдар). For every other chapter numeric
   sort == TOC order; **for Chapter 0 it does not**, so Chapter 0 is assembled
   from the explicit list in ``ORDER_OVERRIDE`` and any mismatch between that
   list and the files on disk is a hard error rather than a reordering.

Chapters 0, 5 and 7 were also absent from ``CHAPTERS`` and are added. **Their
Kazakh translations do not exist yet** (Ch 0: 0/16, Ch 4: 3/20, Ch 5: 0/7,
Ch 7: 0/1) — the script simply skips a chapter with no files, so fixing it now
means the defects cannot bite when those translations land.

3. **Front matter was missing (added 2026-08-12).** The same repair added a
   ``FRONT_MATTER`` block to ``_assemble_en.py`` but not here, so the Kazakh
   manuscript opened straight at Chapter 1 while the English one carried
   normative references, definitions and abbreviations ahead of the
   Introduction. The three ``thesis/output/*_kz.md`` sources already existed;
   only the insertion was absent. A missing file is now reported as suspect.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path
from datetime import date

THESIS = Path(__file__).resolve().parent.parent
CH_ROOT = THESIS / "chapters"
OUT_DIR = THESIS / "output"
OUT = Path(__file__).resolve().parent / f"DISSERTATION_KZ_partial_{date.today()}.md"

# Front matter, authored in thesis/output/ as council deliverables (EN/KZ,
# exported to GOST docx/pdf) and NOT re-drafted under chapters/00-introduction.
# Inserted ahead of the Introduction, in house order. Mirrors FRONT_MATTER in
# _assemble_en.py -- the 2026-08-11 repair added it there but not here, so the
# KZ manuscript opened straight at Chapter 1.
FRONT_MATTER = [
    "normative_references_kz.md",
    "definitions_kz.md",
    "abbreviations_kz.md",
]

# Chapter dir -> TOC chapter heading (KZ), in manuscript order.
CHAPTERS = [
    ("00-introduction", "КІРІСПЕ"),
    ("01-problem-domain",
     "1 ДИАБЕТТІК РЕТИНОПАТИЯНЫ АВТОМАТТАНДЫРЫЛҒАН ДИАГНОСТИКАЛАУДЫҢ "
     "ПРОБЛЕМАЛЫҚ САЛАСЫН ТАЛДАУ ЖӘНЕ ҚАЗІРГІ ЖАЙ-КҮЙІ"),
    ("02-theoretical-foundations",
     "2 FUNDUS IMAGE ТАЛДАУЫ ҮШІН IMAGE PREPROCESSING ЖӘНЕ DEEP LEARNING "
     "ТЕОРИЯЛЫҚ НЕГІЗДЕРІ"),
    ("03-methodology",
     "3 ИНТЕГРАЦИЯЛАНҒАН PREPROCESSING-CNN PIPELINE ЖОБАЛАУ ӘДІСТЕМЕСІ"),
    ("04-experiments",
     "4 ЭКСПЕРИМЕНТТІК ЗЕРТТЕУ — PREPROCESSING-ТІҢ CNN ДИАГНОСТИКАЛЫҚ "
     "ӨНІМДІЛІГІНЕ ӘСЕРІ"),
    ("05-validation",
     "5 СЕНІМДІЛІКТІ ВАЛИДАЦИЯЛАУ ЖӘНЕ САЛЫСТЫРМАЛЫ ТАЛДАУ"),
    ("06-system-architecture",
     "6 РЕСУРСТАРЫ ШЕКТЕУЛІ ОРТАҒА АРНАЛҒАН DR АВТОМАТТАНДЫРЫЛҒАН СКРИНИНГ "
     "ЖҮЙЕСІНІҢ АРХИТЕКТУРАСЫ"),
    ("07-conclusion", "ҚОРЫТЫНДЫ"),
    ("08-appendices", "ҚОСЫМШАЛАР"),
]

# Chapters whose manuscript order is NOT the numeric order of their section
# identifiers. Values are section ids in outline/TABLE_OF_CONTENTS_KZ.md order.
ORDER_OVERRIDE = {
    "00-introduction": [
        "0.1",   # Зерттеу тақырыбының өзектілігі
        "0.3",   # Зерттеу мақсаты
        "0.4",   # Зерттеу міндеттері
        "0.5",   # Зерттеу нысаны мен пәні
        "0.6",   # Зерттеу гипотезасы
        "0.2",   # Ғылыми жаңалығы
        "0.8",   # Қорғауға ұсынылатын тұжырымдар
        "0.7",   # Әдіснамалық негізі
        "0.9",   # Теориялық маңыздылығы
        "0.10",  # Практикалық маңыздылығы
        "0.13",  # Нәтижелердің сенімділігі
        "0.14",  # Эмпирикалық (эксперименттік) базасы
        "0.11",  # Зерттеу нәтижелерінің апробациясы
        "0.15",  # Ғылыми бағдарламалармен байланысы
        "0.12",  # Жарияланымдар
        "0.16",  # Диссертацияның құрылымы мен көлемі
    ],
}

# body ends at the translator note or a PART-2/PART-3 style block
BODY_END = re.compile(r"^(### Аудармашы ескертуі|## 2-БӨЛІК|## PART [23]\b|## 3-БӨЛІК)", re.I)
PART1_HDR = re.compile(r"^## 1-БӨЛІК\b", re.I)
SHORT_BODY_WORDS = 60  # below this, a body is almost certainly a mis-extraction

# Chapters listed in ORDER_OVERRIDE that are only partially translated. Filled
# by ordered_files(); reported at the end so an incomplete chapter is visible
# without being fatal.
PARTIAL: list[tuple[str, list[str]]] = []


def section_key(p: Path):
    stem = p.name.replace("-translation.md", "")
    toks = []
    for t in stem.split("."):
        if t.isdigit():
            toks.append((0, int(t), ""))
        else:  # 'C' (conclusion) and appendix letters sort after numerics
            toks.append((1, 0, t))
    return toks


def ordered_files(cdir: str, d: Path) -> list[Path]:
    """Files in manuscript order, honouring ORDER_OVERRIDE."""
    files = list(d.glob("*-translation.md"))
    if cdir not in ORDER_OVERRIDE or not files:
        return sorted(files, key=section_key)

    by_id = {f.name.replace("-translation.md", ""): f for f in files}
    want = ORDER_OVERRIDE[cdir]
    extra = [s for s in by_id if s not in want]
    if extra:
        # An unlisted file is the dangerous case: it would have to be placed by
        # numeric sort, which for Chapter 0 is the wrong order. Still fatal.
        raise SystemExit(
            f"ORDER_OVERRIDE for {cdir} does not cover the translations on disk.\n"
            f"  present but unlisted: {extra}\n"
            "Chapter 0 must not be assembled by numeric sort - update the list."
        )
    # A *missing* translation is not dangerous, only incomplete: the sections
    # that do exist are still emitted in listed order. Erroring on this made a
    # partially translated Chapter 0 break the whole KZ build, which blocks
    # incremental translation for no safety gain. Report it instead.
    present = [s for s in want if s in by_id]
    missing = [s for s in want if s not in by_id]
    if missing:
        PARTIAL.append((cdir, missing))
    return [by_id[s] for s in present]


def extract(p: Path):
    """Return (title, body, word_count).

    Prefers an explicit '## 1-БӨЛІК' marker; falls back to the top of the file
    when the translation has none, skipping a leading '# ' title line and a
    leading '> ' header blockquote. `title` is returned only when the file
    carries a '# ' line; files without one already open with their own '##'
    heading and must not have anything prepended.
    """
    lines = p.read_text(encoding="utf-8").splitlines()
    title = next((l for l in lines if l.startswith("# ")), None)

    marker = next((i for i, l in enumerate(lines) if PART1_HDR.match(l)), None)
    if marker is not None:
        start = marker + 1
    else:
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

    out.append("# Көз түбі кескінін жақсарту және CNN жіктеуі арқылы диабеттік "
               "ретинопатияны автоматтандырылған диагностикалау")
    out.append("")
    out.append(f"> **Аралық қазақ тіліндегі жинақ — {date.today()}.** Бекітілген "
               "аудармалардың 1-БӨЛІК мәтіндерін Мазмұн ретімен біріктіру. Жұмыстық "
               "автор-жыл дәйексөздері түрлендірілмеген (GOST `[N]` — түпкі жинақтаудағы "
               "жалғыз шегерілген өту). Аудармашы ескертулері, аударма тақырыпшалары мен "
               "тексеру тізімдері қосылмаған. Бұл — түпкі түптелген диссертация ЕМЕС: "
               "төмендегі манифест қай тараулардың аудармасы бар екенін көрсетеді.")
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
        d = CH_ROOT / cdir / "translations"
        if not d.is_dir():
            continue
        files = ordered_files(cdir, d)
        if not files:
            continue
        out.append("\n---\n")
        out.append(f"# {heading}")
        out.append("")
        for f in files:
            title, text, words = extract(f)
            total_words += words
            manifest.append((f"{cdir}/{f.name}", words))
            if words < SHORT_BODY_WORDS:
                suspect.append((f.name, f"body extracted as {words} words"))
            out.append(text if (title is None or title in text) else f"{title}\n\n{text}")
            out.append("")

    OUT.write_text("\n".join(out), encoding="utf-8")

    # ASCII-safe stdout (Windows console may be cp1251 and cannot encode Cyrillic)
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    print(f"WROTE {OUT}")
    print(f"Sections: {len(manifest)} | Total PART-1 (1-BOLIK) words: {total_words:,}")

    if suspect:
        print("\n!! SUSPECT EXTRACTIONS - check before using this assembly:")
        for name, why in suspect:
            print(f"   {name}: {why}")
    else:
        print("\nNo suspect extractions.")

    for cdir, missing in PARTIAL:
        print(f"\n-- {cdir}: PARTIAL, {len(missing)} translation(s) still missing "
              f"(emitted sections are in listed order):")
        print("   " + ", ".join(missing))

    print("\n# file -> words")
    for name, w in manifest:
        print(f"  {name:46s} {w:6,d}")

    return 1 if suspect else 0


if __name__ == "__main__":
    sys.exit(main())
