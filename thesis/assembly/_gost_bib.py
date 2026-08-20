#!/usr/bin/env python3
"""Stage-G helper: derive GOST 7.1-2003 bibliographic entries from the APA-7
citations recorded on the literature cards (`_card_bib.tsv`).

The reference list of the bound thesis is described per GOST 7.1-2003, not APA
(council/en/02-formatting/gost-formatting.md, sections 6.9/6.11). Every earlier
build shipped the APA strings and deferred the description to "final
typesetting"; this module is that step, done once and written to
`_card_gost.tsv` so the result is reviewable and reproducible rather than
re-derived silently inside each build.

Shape produced, per thesis/prompts/citation-assembly.md step 5:

    Surname A. A. Title / A. A. Surname, B. B. Surname, C. C. Surname [et al.]
        // Venue. - Year. - Vol. NN, No. M. - P. start-end. - DOI: 10.x/y.

Conversion is mechanical and therefore fallible: entries whose APA source lacks
a venue, volume or page span come out short, and the generator flags them so the
QA report can list them rather than let them pass as complete. Hand corrections
belong in `_card_gost.tsv` itself: a row whose third column reads `#pinned` is
carried through untouched on the next run.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BIB = HERE / "_card_bib.tsv"
OUT = HERE / "_card_gost.tsv"

DASH = "–"          # en dash: the corpus dash, and the GOST area separator
ELLIPSIS = ("…", "...")


def _is_initials(tok: str) -> bool:
    """'V.' / 'M. C.' / 'S.-I.' / 'K.-R.' - an APA given-name field."""
    return bool(re.fullmatch(r"(?:[A-ZÀ-Ü]\.(?:-[A-ZÀ-Ü]\.)*\s*)+",
                             tok.strip()))


def split_authors(seg: str):
    """APA author area -> ([(surname, initials)], elided).

    APA writes 'Surname, A. B., Surname2, C., & Surname3, D.' - surnames and
    initials are both separated by ', ', so the list is walked pairwise rather
    than split. An ellipsis marks an author list the card itself abbreviated;
    that matters because it decides whether '[et al.]' is owed.
    """
    elided = any(e in seg for e in ELLIPSIS)
    for e in ELLIPSIS:
        seg = seg.replace(e, ",")
    seg = seg.replace("&", ",").replace(" and ", ",")
    toks = [t.strip() for t in seg.split(",")]
    toks = [t for t in toks if t]
    out, i = [], 0
    while i < len(toks):
        sur = toks[i].strip(". ")
        if not sur:
            i += 1
            continue
        if i + 1 < len(toks) and _is_initials(toks[i + 1]):
            out.append((sur, re.sub(r"\s+", " ", toks[i + 1].strip())))
            i += 2
        else:
            out.append((sur, ""))          # mononym, e.g. 'Roslidar', 'Rishu'
            i += 1
    return out, elided


def sur_first(a) -> str:
    """'Gulshan V.' - the heading form, surname then initials."""
    sur, ini = a
    return f"{sur} {ini}".strip()


def ini_first(a) -> str:
    """'V. Gulshan' - the responsibility-area form.

    A particle stays welded to the surname ('L. van der Maaten'), which is why
    the surname is moved whole rather than token by token.
    """
    sur, ini = a
    return f"{ini} {sur}".strip()


def responsibility(authors, elided: bool) -> str:
    """The area after '/': the first three authors, then [et al.] if more."""
    shown = authors[:3]
    tail = " [et al.]" if (len(authors) > 3 or elided) else ""
    return ", ".join(ini_first(a) for a in shown) + tail


TITLE_END = re.compile(r"([.?!])\s+(?=[A-ZÀ-Ü\[“\"(])")


def parse(apa: str):
    """APA string -> the fields a GOST description needs, or None."""
    s = re.sub(r"\s+", " ", apa.strip()).rstrip()
    s = s.replace("*", "")                          # markdown emphasis
    m = re.search(r"\((\d{4})[a-z]?\)\.\s*", s)
    if not m:
        return None
    authors, elided = split_authors(s[:m.start()])
    year = m.group(1)
    rest = s[m.end():]

    doi = ""
    dm = re.search(r"https?://doi\.org/(?:doi:)?(10\.[^\s,;]+)", rest)
    if dm:
        doi = dm.group(1).rstrip(".")
        rest = rest[:dm.start()].rstrip() + rest[dm.end():]
    else:
        dm = re.search(r"\bDOI[:\s]\s*(10\.[^\s,;]+)", rest, re.I)
        if dm:
            doi = dm.group(1).rstrip(".")
            rest = rest[:dm.start()] + rest[dm.end():]

    arxiv = ""
    am = (re.search(r"arXiv[:\s]\s*(\d{4}\.\d{4,5}(?:v\d+)?)", rest, re.I)
          or re.search(r"arxiv\.org/abs/(\d{4}\.\d{4,5}(?:v\d+)?)", rest, re.I))
    if am:
        arxiv = am.group(1)
    rest = re.sub(r"\(?\s*arXiv preprint\s*", "", rest, flags=re.I)
    rest = re.sub(r"\(?\s*arXiv[:\s]\s*\d{4}\.\d{4,5}(?:v\d+)?\s*\)?\.?", "", rest, flags=re.I)
    rest = re.sub(r"https?://arxiv\.org/abs/\S+", "", rest, flags=re.I)
    rest = re.sub(r"\[Preprint\]\.?", "", rest, flags=re.I)
    rest = re.sub(r"\s+\.", ".", rest).strip()

    tm = TITLE_END.search(rest)
    if tm:
        title = rest[:tm.start()] + ("" if tm.group(1) == "." else tm.group(1))
        venue = rest[tm.end():]
    else:
        title, venue = rest, ""
    return {"authors": authors, "elided": elided, "year": year,
            "title": title.strip().rstrip("."), "venue": venue.strip(),
            "doi": doi, "arxiv": arxiv}


VOLNO = re.compile(r"(?<![\w.])(\d+)\s*\(([^)]+)\)\s*,")
VOLONLY = re.compile(r",\s*(\d+(?:\s*[–—-]\s*\d+)?)\s*,")
PAGES = re.compile(r"(?:pp?\.\s*)?(e?\d+)\s*[–—-]\s*(e?\d+)\s*\.?\s*$")
ARTNO = re.compile(r"\b(?:Article\s+)?(e?\d{2,7})\s*\.?\s*$", re.I)
# APA parks a proceedings' page span mid-string, '(pp. 770-778). IEEE.', where a
# journal keeps it at the end. Peeled separately, or the publisher tail hides it.
INNER_PAGES = re.compile(r"\(\s*pp?\.\s*(\d+)\s*[–—-]\s*(\d+)\s*\)\s*\.?")


def gost(apa: str):
    """-> (entry, flags). `flags` names what the APA source did not supply."""
    p = parse(apa)
    if not p:
        return apa, ["unparsed"]
    if not p["authors"]:
        return apa, ["no-authors"]
    flags = []
    authors, year, title = p["authors"], p["year"], p["title"]

    head = f"{sur_first(authors[0])} {title}"
    resp = responsibility(authors, p["elided"])

    # Venue area: peel the volume/issue/page block off the end of the name.
    v = p["venue"].rstrip().rstrip(".")
    vol = issue = pages = artno = publisher = ""
    m = INNER_PAGES.search(v)
    if m:
        pages = f"{m.group(1)}{DASH}{m.group(2)}"
        publisher = v[m.end():].strip(" .")     # '… (pp. 770-778). IEEE.'
        v = v[:m.start()].rstrip().rstrip(",")
    else:
        m = PAGES.search(v)
        if m:
            pages = f"{m.group(1)}{DASH}{m.group(2)}"
            v = v[:m.start()].rstrip().rstrip(",")
        else:
            m = ARTNO.search(v)
            if m:
                artno = m.group(1)
                v = v[:m.start()].rstrip().rstrip(",")
    m = VOLNO.search(v + ",")
    if m:
        vol, issue = m.group(1), m.group(2)
        v = (v[:m.start()] + v[m.start() + len(m.group(0)) - 1:]).rstrip().rstrip(",")
    else:
        m = VOLONLY.search(v + ",")
        if m:
            vol = m.group(1)
            v = (v[:m.start()] + v[m.end() - 1:]).rstrip().rstrip(",")
    v = re.sub(r",\s*,", ",", v)
    v = re.sub(r"^In\s+", "", v.strip().strip(",").strip())

    if not v and p["arxiv"]:
        v = "arXiv preprint"                    # a venue the card does supply
    if not v:
        flags.append("no-venue")
    areas = [f"{DASH} {publisher}, {year}." if publisher else f"{DASH} {year}."]
    if vol and issue:
        areas.append(f"{DASH} Vol. {vol}, No. {issue}.")
    elif vol:
        areas.append(f"{DASH} Vol. {vol}.")
    if pages:
        areas.append(f"{DASH} P. {pages}.")
    elif artno:
        areas.append(f"{DASH} Art. No. {artno}.")
    else:
        flags.append("no-pages")
    if p["arxiv"]:
        areas.append(f"{DASH} arXiv:{p['arxiv']}.")
    if p["doi"]:
        areas.append(f"{DASH} DOI: {p['doi']}.")
    elif not p["arxiv"]:
        flags.append("no-doi")

    venue_part = f" // {v}. " if v else " "
    entry = re.sub(r"\s+", " ", f"{head} / {resp}{venue_part}" + " ".join(areas)).strip()
    entry = entry.replace("—", DASH)            # the corpus dash, throughout
    return entry, flags


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    # `#pinned` — hand-corrected, from the card's own data.
    # `#pinned-external` — the card carries no venue, so the entry was completed
    # against the published record; the QA report lists these separately.
    pinned = {}
    if OUT.exists():
        for ln in OUT.read_text(encoding="utf-8").splitlines():
            parts = ln.split("\t")
            if len(parts) >= 3 and parts[2].strip().startswith("#pinned"):
                pinned[parts[0]] = (parts[1], parts[2].strip())
    rows = []
    for ln in BIB.read_text(encoding="utf-8").splitlines():
        parts = ln.split("\t")
        if len(parts) < 2:
            continue
        card, apa = parts[0], parts[1]
        if card in pinned:
            rows.append((card, pinned[card][0], pinned[card][1]))
            continue
        entry, flags = gost(apa)
        rows.append((card, entry, ",".join(flags)))
    OUT.write_text("\n".join("\t".join(r) for r in rows) + "\n", encoding="utf-8")
    bad = [r for r in rows if r[2] and not r[2].startswith("#pinned")]
    print(f"WROTE {OUT.name}: {len(rows)} entries, {len(pinned)} pinned, {len(bad)} flagged")
    for card, _entry, flag in bad:
        print(f"  [{flag}] {card}")


if __name__ == "__main__":
    main()
