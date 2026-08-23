#!/usr/bin/env python3
"""Stage-G FINAL pass: convert working author-year citations to GOST numbered
[N] form on BOTH the EN and KZ assembled manuscripts (2026-06-17), with ONE
shared numbering, and build the "List of references used" in each language.

Per thesis/prompts/citation-assembly.md:
  * Numbering is assigned ONCE, by first appearance in the EN manuscript
    (GOST 7.32-2001 §6.11) -> authoritative card -> [N] map.
  * The SAME map is applied to KZ (rule #7, language invariance). KZ keeps Latin
    author surnames but uses Kazakh connectors ("X т.б." = et al., "X пен/мен Y"
    = "X and Y") and the Kazakh page form "699-б.". The word-for-word calque
    "X және әріптестері(нің)" is still parsed, because a draft may reach here
    carrying it, but it is no longer written: it was replaced across all 35
    translation sources on 2026-08-23 and conformance.py fails the volume on it.
  * Resolution is surname-based and language-agnostic: surnames_of() strips every
    non-[a-z] char (so accents AND all Cyrillic connectors fall away), then
    resolve() tries candidate keys full-join -> first-author -> pairs -> singles,
    matching the literature-card map. This handles comma lists, "et al.", accented
    names (González-Díaz), and Kazakh declensions uniformly.
  * Self-citations (#19-24, Cyrillic in KZ / SELF-set in EN) and Appendix-D
    publication records resolve to no external card and are LEFT author-year
    (SIR-4 prose framing preserved); flagged for manual per-section disambiguation.

Outputs (thesis/assembly/): DISSERTATION_EN_GOST_<date>.md,
DISSERTATION_KZ_GOST_<date>.md, _citation_resolution_final_<date>.md
"""
from __future__ import annotations
import re, sys, unicodedata
from pathlib import Path
from datetime import date

HERE = Path(__file__).resolve().parent


def latest(prefix: str) -> Path:
    """Newest DISSERTATION_<lang>_partial_<date>.md. Pinning a date here is how
    the June run silently kept converting a stale 53-section manuscript."""
    cands = sorted(HERE.glob(f"{prefix}_partial_*.md"))
    if not cands:
        raise SystemExit(f"no {prefix}_partial_*.md in {HERE}")
    return cands[-1]


SRC_EN = latest("DISSERTATION_EN")

# The Kazakh manuscript is converted with the SAME numbers, but only when it is
# a translation of the SAME English tree. The four-chapter rewrite left
# chapters/**/translations/ empty, so the newest KZ partial is still the
# six-chapter volume: converting it here would have produced a Kazakh thesis
# whose [N] point into an English list built from different chapters. Pairing on
# the date suffix is the cheap check that they are the same tree.
_STAMP = SRC_EN.stem.rsplit("_", 1)[-1]
_KZ = HERE / f"DISSERTATION_KZ_partial_{_STAMP}.md"
SRC_KZ = _KZ if _KZ.exists() else None

BIB = HERE / "_card_bib.tsv"
GOST = HERE / "_card_gost.tsv"
OUT_EN = HERE / f"DISSERTATION_EN_GOST_{date.today()}.md"
OUT_KZ = HERE / f"DISSERTATION_KZ_GOST_{date.today()}.md"
OUT_QA = HERE / f"_citation_resolution_final_{date.today()}.md"

YEAR = r"(?:19|20)\d{2}[a-z]?"
STOP = {"and", "the", "in", "of", "by", "et", "al"}

# token key -> card filename (external). MULTI splits a combined "(…, 2015, 2016)".
K2C = {
 "kusuhara|2018":"kusuhara-2018.md","morya|2024":"morya-2024.md",
 "wang-lo|2018":"wang-lo-2018.md","gettinger|2025":"gettinger-2025.md",
 "kesharwani|2021":"kesharwani-2021.md","porwal|2018":"porwal-2018-idrid-dataset.md",
 "shen|2020":"shen-2020-cofe-net.md","fu|2020":"fu-2020-eyeq-riqa.md",
 "zago|2018":"zago-2018-riqa.md","dai|2021":"dai-2021-deepdr.md",
 "rakhlin|2017":"rakhlin-2017.md","voets|2019":"voets-2019.md",
 "gulshan|2016":"gulshan-2016.md","beede|2020":"beede-2020-human-centered-dr.md",
 "liu|2022":"liu-2022.md","zhou|2022":"zhou-2022-domain-generalization-survey.md",
 "wang-deng|2018":"wang-2018-deep-visual-domain-adaptation-survey.md",
 "litjens|2017":"litjens-2017-medical-dl-survey.md","krizhevsky|2012":"krizhevsky-2012-alexnet.md",
 "simonyan-zisserman|2015":"simonyan-2015-vgg.md",
 "szegedy|2015":"MULTI:szegedy-2015-googlenet.md,szegedy-2016-inception-v3.md",
 "he|2016":"he-2016-deep-residual-learning.md","huang|2017":"huang-2017-densenet.md",
 "tan-le|2019":"tan-2019-efficientnet.md","tan-le|2021":"tan-2021-efficientnetv2.md",
 "pratt|2016":"pratt-2016.md","xu|2024":"xu-2024-hybrid.md",
 "gargeya-leng|2017":"gargeya-2017-automated-dr.md","quellec|2017":"quellec-2017-deep-image-mining.md",
 "arora|2024":"arora-2024-efficientnet.md","sharma|2025":"sharma-2025-vit-capsule.md",
 "wan|2021":"wan-2021-ead-net.md","zhou|2020":"zhou-2020-fgadr-benchmark.md",
 "khosravi|2025":"khosravi-2025.md","ryu|2021":"ryu-2021-octa.md",
 "esteva|2017":"esteva-2017-skin-cancer.md","burlina|2017":"burlina-2017-amd-dcnn.md",
 "dosovitskiy|2021":"dosovitskiy-2021-vision-transformer.md","goh|2024":"goh-2024-vit-vs-cnn.md",
 "liu|2021":"liu-2021-swin-transformer.md","geetha-hema|2026":"geetha-hema-2026.md",
 "saxena|2020":"saxena-2020.md","cheplygina|2018":"cheplygina-2018-not-so-supervised-survey.md",
 "zhou|2023":"zhou-2023-retfound.md","azizi|2021":"azizi-2021-micle.md",
 "tjoa-guan|2020":"tjoa-2020-xai-survey.md","samek|2017":"samek-2017-explainable-ai.md",
 "zhou|2016":"zhou-2016-cam.md","selvaraju|2017":"selvaraju-2017-grad-cam.md",
 "chattopadhyay|2018":"chattopadhyay-2018-grad-cam-plus-plus.md",
 "lundberg-lee|2017":"lundberg-2017-shap.md","ribeiro|2016":"ribeiro-2016-lime.md",
 "abr-moff|2018":"abramoff-2018-clinical-ai-validation.md","ting|2017":"ting-2017.md",
 "bellemo|2019":"bellemo-2019-ai-dr-africa.md","zhang|2022":"zhang-2022-multicentre.md",
 "ruamviboonsuk|2022":"ruamviboonsuk-2022.md","nchez-guti-rrez|2022":"sanchez-gutierrez-2022.md",
 "sanchez-gutierrez|2022":"sanchez-gutierrez-2022.md",
 "baget-bernaldiz|2021":"baget-bernaldiz-2021.md","wewetzer|2021":"wewetzer-2021.md",
 "senapati|2024":"senapati-2024.md","ting|2019":"ting-2019-dl-ophthalmology-review.md",
 "de-fauw|2018":"defauw-2018-retinal-oct.md","fauw|2018":"defauw-2018-retinal-oct.md",
 "pizer|1987":"pizer-1987-adaptive-histogram-equalization.md",
 "zuiderveld|1994":"zuiderveld-1994-clahe.md","hayati|2023":"hayati-2023.md",
 "shaout-han|2025":"shaout-han-2025.md","shaout|2025":"shaout-han-2025.md","chakka|2023":"chakka-2023.md",
 "tomasi-manduchi|1998":"tomasi-1998-bilateral-filtering.md","tomasi|1998":"tomasi-1998-bilateral-filtering.md",
 "morel|2011":"buades-2011-non-local-means.md","buades|2011":"buades-2011-non-local-means.md",
 "sun|2016":"he-2016-deep-residual-learning.md","weinberger|2017":"huang-2017-densenet.md",
 "cui|2019":"cui-2019-class-balanced-loss.md","chairi|2024":"araf-2024.md","araf|2024":"araf-2024.md",
 "lin|2017":"lin-2017-focal-loss.md","srivastava|2014":"srivastava-2014-dropout.md",
 "ioffe-szegedy|2015":"ioffe-2015-batch-normalization.md","ioffe|2015":"ioffe-2015-batch-normalization.md",
 "shorten-khoshgoftaar|2019":"shorten-2019-augmentation-survey.md",
 "shorten|2019":"shorten-2019-augmentation-survey.md",
 "zhang|2018":"zhang-2018-mixup.md","cubuk|2020":"cubuk-2020-randaugment.md",
 "buda|2018":"buda-2018-class-imbalance.md","pan-yang|2010":"pan-2010-transfer-learning-survey.md",
 "pan|2010":"pan-2010-transfer-learning-survey.md",
 "lipson|2014":"yosinski-2014-transferability-features.md","yosinski|2014":"yosinski-2014-transferability-features.md",
 "le|2019":"tan-2019-efficientnet.md",
 "pluim|2018":"cheplygina-2018-not-so-supervised-survey.md","arrieta|2022":"arrieta-2022.md",
 "kornblith|2019":"kornblith-2019-transferability.md",
 "ganin|2016":"ganin-2016-dann.md","shurrab-duwairi|2022":"shurrab-2022-ssl-medical-survey.md",
 "shurrab|2022":"shurrab-2022-ssl-medical-survey.md",
 "chen|2020":"chen-2020-simclr.md","he|2020":"he-2020-moco.md","grill|2020":"grill-2020-byol.md",
 "chen-he|2021":"chen-2021-simsiam.md","caron|2021":"caron-2021-dino.md","he|2022":"he-2022-mae.md",
 "everingham|2010":"everingham-2010-pascal-voc.md","rezatofighi|2019":"rezatofighi-2019-giou.md",
 "szegedy|2016":"szegedy-2016-inception-v3.md",
 "buda-maki-mazurowski|2018":"buda-2018-class-imbalance.md","krause|2018":"krause-2018-grader-variability.md",
 "kingma-ba|2015":"kingma-2015-adam.md","kingma|2015":"kingma-2015-adam.md",
 "cuadros-bresnick|2009":"cuadros-2009-eyepacs.md","cuadros|2009":"cuadros-2009-eyepacs.md",
 "decenci-re|2014":"decenciere-2014-messidor.md","decenciere|2014":"decenciere-2014-messidor.md",
 "nandal|2024":"nandal-2024.md","guo|2017":"guo-2017-calibration.md","wang|2004":"wang-2004-ssim.md",
 "hinton|2012":"krizhevsky-2012-alexnet.md","gonzalez-diaz|2024":"gonzalez-diaz-2024.md",
 "abramoff|2018":"abramoff-2018-clinical-ai-validation.md",
}

# ---- the candidate's own publications (SIR-4) -----------------------------
# Numbered like any other source: GOST requires them in the reference list, and
# the "prior own work" framing lives in the prose, not in the bracket, so it
# survives conversion untouched.
#
# The June run left these author-year, calling the mapping ambiguous. It is not:
# every occurrence resolves on evidence, and the ambiguity was an artefact of
# matching on first author alone.
#   * "Yesmukhamedov et al., 2025" carries page locators 74, 77, 78-79, 83, 85,
#     86, 87, 88, 90 -- every one inside the NAS RK article's span 74-91, and
#     inside no other self-work's span. -> nan-rk.
#   * "Sapakova, Yesmukhamedov & Sapakov, 2025" is cited in 2.1.2 for
#     "Eq. 1/Eq. 2, p. 5"; the EEJET card records exactly those two equations
#     (CL = ceil(L/T) + beta(phi - ceil(L/T)) and CLIP LIMIT = T/80) at its p. 5.
#   * The three remaining works appear with full author lists (Appendix D
#     Table D.1), so they resolve on the full-join key before any fallback.
#   * 2.4.1 cites the laser-modelling work by venue rather than by author, in
#     both languages ("the modeling study reported in the Herald of KazUTB,
#     2025"); "kazutb|2025" catches it through resolve()'s single-surname tier.
# scopus-q2 and scopus-q3 are two literature cards for ONE article, exactly as
# 0.12 discloses ("five distinct works, not six"), so both map to one entry.
SELF_K2C = {
 "yesmukhamedov|2025": "yesmukhamedov-nan-rk.md",
 "yesmukhamedov-sapakova-al-haddad-daniyarova|2025": "yesmukhamedov-nan-rk.md",
 "yesmukhamedov-sapakova-haddad-daniyarova|2025": "yesmukhamedov-nan-rk.md",
 "yesmukhamedov-sapakova-kozhamkulova-daniyarova-armankyzy|2025": "yesmukhamedov-kbtu.md",
 "sapakova-yesmukhamedov-sapakov|2025": "yesmukhamedov-scopus-q2.md",
 # The four-chapter rewrite renders the same EEJET article by two of its three
 # authors, in 2.1 ("conventional preprocessing raised validation accuracy ...
 # an upgraded equalisation variant ... on a different retinal database") and in
 # 2.2 ("replaced the derived clip with a single controllable global threshold
 # ... the two literature records drawn from it describe one" article). Both
 # passages descend from superseded 3.1.1 / 2.1.2, which cite the EEJET work.
 # Without this key the pair resolves on the first surname alone to the NAS RK
 # article, which has no Sapakov among its authors and no CLAHE result in it.
 "yesmukhamedov-sapakov|2025": "yesmukhamedov-scopus-q2.md",
 # 2.2.2 cites the same article in the short form "Sapakova et al., 2025", in a
 # pair the draft itself calls "a single prior-work thread"; 1.2.2 attributes
 # that experiment (APTOS 2019, ROC-AUC 0.9638) to the EEJET article. Safe as a
 # first-author fallback: the one other Sapakova-2025 work, the Procedia paper,
 # is only ever cited with its full author list, which resolves first.
 "sapakova|2025": "yesmukhamedov-scopus-q2.md",
 "sapakova-yesmukhamedov-sapakov-yemberdiyeva-kozhamkulova|2025": "yesmukhamedov-conf.md",
 "sapakova-daniyarova-yesmukhamedov-armankyzy-emberdieva-kaldybaeva|2025": "yesmukhamedov-kazutb.md",
 "kazutb|2025": "yesmukhamedov-kazutb.md",
}
K2C.update(SELF_K2C)
SELF_SUR = {"yesmukhamedov", "sapakova", "sapakov", "kazutb"}  # candidate's own work -> keep author-year
APPD_SUR = {"yemberdiyeva", "kozhamkulova", "daniyarova", "armankyzy", "emberdieva",
            "kaldybaeva", "haddad", "altimemy", "procedia", "ds", "istanbul"}

# ---- surname extraction (language-agnostic: folds accents to ASCII, drops Cyrillic) ----
def surnames_of(author: str):
    a = unicodedata.normalize("NFKD", author)  # González -> Gonzalez, Abràmoff -> Abramoff
    a = "".join(c for c in a if not unicodedata.combining(c)).lower().replace("&", " and ")
    a = re.sub(r"\bet al\.?\b", " ", a)
    a = re.sub(r"[^a-z\s]", " ", a)
    a = re.sub(r"\s+", " ", a).strip()
    return [w for w in a.split() if len(w) > 1 and w not in STOP]


def resolve(author: str, year: str):
    """Return K2C value (card or 'MULTI:...') or None, by candidate-key priority."""
    sl = surnames_of(author)
    if not sl:
        return None
    y = year[:4]
    cands = ["-".join(sl), sl[0]]
    cands += [f"{sl[i]}-{sl[i+1]}" for i in range(len(sl) - 1)]
    cands += sl
    for c in cands:
        v = K2C.get(f"{c}|{y}")
        if v:
            return v
    return None


def classify(author: str):
    sl = set(surnames_of(author))
    if sl & SELF_SUR:
        return "self"
    if sl & APPD_SUR:
        return "appd"
    return "unknown"


# ---- regexes -------------------------------------------------------------
SUR = r"[A-ZÀ-ÖØ-Þ][A-Za-zÀ-ÿ'’\-]+"
INIT = r"[A-Z]\."
KZC = r"(?:және\s+әріптестер[Ѐ-ӿ]*|әріптестер[Ѐ-ӿ]*|және|пен|мен|бен|т\.б\.)"
SEP = r"(?:\s*,\s*|\s+&\s+|\s+and\s+|\s+et\s+al\.?\s*|\s+" + KZC + r"\s*)"
TAIL = r"(?:\s+et\s+al\.?|\s+" + KZC + r")?"
AUTHORS = SUR + r"(?:" + SEP + r"(?:" + SUR + r"|" + INIT + r"))*" + TAIL
# narrative: author block + "(year[, page])"
NARR = re.compile(r"(" + AUTHORS + r")\s*\((" + YEAR + r")((?:,\s*[^)]*)?)\)")
# parenthetical: requires a Latin letter + a 4-digit year inside
PAREN = re.compile(r"\(([^()]*?[A-Za-z][^()]*?(?:19|20)\d{2}[a-z]?[^()]*?)\)")
# page tail inside a citation: "p. 370" / "pp. 79-88" (EN) or "699-б." / "699 б." (KZ)
PAGE = re.compile(r"((?:p{1,2}\.\s*[\dIVxiv–\-]+)|(?:\d+\s*-?\s*б\.))\s*$", re.I)


# Body starts at the Introduction when one is assembled, else at Chapter 1.
# Front matter (normative references / definitions / abbreviations) stays in the
# head: it is authored in thesis/output/ and carries no author-year citations.
# NOTE: the June run hard-coded '^# 1 ', which was correct only while Chapter 0
# was unwritten. With Chapter 0 assembled ahead of Chapter 1 that pattern would
# have dropped the whole Introduction from BOTH numbering and conversion.
BODY_START = [r"(?m)^# INTRODUCTION\s*$", r"(?m)^# КІРІСПЕ\s*$", r"(?m)^# 1 "]


def split_body(path: Path):
    text = path.read_text(encoding="utf-8")
    hits = [m.start() for p in BODY_START for m in [re.search(p, text)] if m]
    if not hits:
        raise SystemExit(f"{path.name}: no body-start heading found")
    i = min(hits)
    return text[:i], text[i:]


# ---------- PASS 1: assign [N] from EN, by first appearance ----------
head_en, body_en = split_body(SRC_EN)
events = []  # (pos, K2C-value)
for m in NARR.finditer(body_en):
    v = resolve(m.group(1), m.group(2))
    if v:
        events.append((m.start(), v))
for m in PAREN.finditer(body_en):
    inner = m.group(1)
    if not re.search(r"[A-Za-z]", re.sub(YEAR, "", inner)):
        continue
    for part in inner.split(";"):
        ym = re.search(r"(" + YEAR + r")", part)
        author = part[:ym.start()].strip().strip(",").strip() if ym else ""
        if ym and author:
            v = resolve(author, ym.group(1))
            if v:
                events.append((m.start(), v))
events.sort(key=lambda e: e[0])

cardN, N = {}, 0
def assign(card):
    global N
    if card not in cardN:
        N += 1
        cardN[card] = N
for _, v in events:
    if v.startswith("MULTI:"):
        for c in v[6:].split(","):
            assign(c)
    else:
        assign(v)


def value_to_nums(v):
    if v.startswith("MULTI:"):
        return ", ".join(str(cardN[c]) for c in v[6:].split(","))
    return str(cardN[v])


# ---------- replacement (shared by EN and KZ) ----------
def repl_narr(m):
    author, year, rest = m.group(1), m.group(2), m.group(3)
    v = resolve(author, year)
    if not v:
        return m.group(0)
    nn = value_to_nums(v)
    pg = PAGE.search(rest)
    return f"{author} [{nn}, {pg.group(1).strip()}]" if pg else f"{author} [{nn}]"


def repl_paren(m):
    inner = m.group(1)
    if not re.search(r"[A-Za-z]", re.sub(YEAR, "", inner)):
        return m.group(0)
    nums, leftovers = [], []
    for part in inner.split(";"):
        ym = re.search(r"(" + YEAR + r")", part)
        author = part[:ym.start()].strip().strip(",").strip() if ym else ""
        if not ym or not author:
            leftovers.append(part.strip()); continue
        v = resolve(author, ym.group(1))
        if not v:
            leftovers.append(part.strip()); continue
        pg = PAGE.search(part)
        entry = value_to_nums(v) + (", " + pg.group(1).strip() if pg else "")
        if entry not in nums:
            # One source cited twice at one point - the rewrite names the EEJET
            # article by two different author sets in 2.1 - is one reference,
            # not "[16, 16]". Collapsing here is also what SIR-5 requires: two
            # cards describing one article may not read as two confirmations.
            nums.append(entry)
    if not nums:
        return m.group(0)
    # Ascending inside one bracket (step 4 of the protocol). Reading order is
    # not ascending whenever a source cited here appeared earlier in the volume:
    # "(Gulshan et al., 2016; Voets et al., 2019)" is [12, 13] by number and
    # [13, 12] by the order the sentence names them.
    nums.sort(key=lambda s: int(re.match(r"\d+", s).group(0)))
    out = "[" + ", ".join(nums) + "]"
    if leftovers:
        out += " (" + "; ".join(leftovers) + ")"
    return out


def convert(body):
    return NARR.sub(repl_narr, PAREN.sub(repl_paren, body))


conv_en = convert(body_en)
conv_kz = convert(split_body(SRC_KZ)[1]) if SRC_KZ else None

# ---------- reference list (cards in [N] order) ----------
# Described per GOST 7.1-2003 (`_card_gost.tsv`, built by `_gost_bib.py` from the
# cards' APA-7 field). The APA strings remain the fallback so a card added to
# `_card_bib.tsv` and not yet converted still yields a visible, if unformatted,
# entry rather than "[card not found]"; the QA report names any such entry.
gost_bib, apa_bib, external = {}, {}, set()
for ln in GOST.read_text(encoding="utf-8").splitlines():
    p = ln.split("\t")
    if len(p) >= 2:
        gost_bib[p[0]] = p[1]
        if len(p) >= 3 and p[2].strip() == "#pinned-external":
            external.add(p[0])
for ln in BIB.read_text(encoding="utf-8").splitlines():
    p = ln.split("\t")
    if len(p) >= 2:
        apa_bib[p[0]] = re.sub(r"\[https?://[^\]]+\]\([^)]+\)",
                               lambda x: x.group(0).split("]")[0][1:], p[1])
inv = {v: k for k, v in cardN.items()}
undescribed = [inv[n] for n in range(1, N + 1) if inv[n] not in gost_bib]
# "Arabic numerals WITHOUT a trailing dot" (GOST 7.32-2001, 6.11; step 5 of the
# protocol; and 16 of 16 samples). Every build so far emitted "1." — which
# md2gost also reads as a Markdown ordered list and re-renders with its own
# marker, so the dot survived into the printed volume.
refs = [f"{n} {re.sub(r'[*]', '', gost_bib.get(inv[n], apa_bib.get(inv[n], '[card not found]')))}"
        for n in range(1, N + 1)]

# ---------- exhaustive QA: every remaining author-year token ----------
def residual(conv):
    blocking, selfk, appdk, unknown = [], [], [], []
    for m in NARR.finditer(conv):
        cls = ("blocking" if resolve(m.group(1), m.group(2)) else classify(m.group(1)))
        {"blocking": blocking, "self": selfk, "appd": appdk, "unknown": unknown}[cls].append(("narr", m.group(0)[:70]))
    for m in PAREN.finditer(conv):
        inner = m.group(1)
        if not re.search(r"[A-Za-z]", re.sub(YEAR, "", inner)):
            continue
        for part in inner.split(";"):
            ym = re.search(r"(" + YEAR + r")", part)
            a = part[:ym.start()].strip().strip(",").strip() if ym else ""
            if not ym or not a:
                continue
            cls = ("blocking" if resolve(a, ym.group(1)) else classify(a))
            {"blocking": blocking, "self": selfk, "appd": appdk, "unknown": unknown}[cls].append(("paren", m.group(0)[:70]))
    return blocking, selfk, appdk, unknown


hdr_en = (f"# Automated Diabetic Retinopathy Diagnosis — EN manuscript with GOST [N] citations\n\n"
          f"> **STAGE-G (final pass) — {date.today()}.** Working author-year citations converted to "
          f"numbered `[N]` (GOST 7.32-2001 §6.11, by first appearance). {N} external sources numbered "
          f"[1]–[{N}]. Numbers are shared with the Kazakh manuscript (language invariance). Run over "
          f"the complete 98-section manuscript, Introduction included.\n")
hdr_kz = (f"# Диабеттік ретинопатияны автоматтандырылған диагностикалау — GOST [N] дәйексөздері бар "
          f"қазақ тіліндегі мәтін\n\n"
          f"> **STAGE-G (түпкі өту) — {date.today()}.** Жұмыстық автор-жыл дәйексөздері нөмірленген "
          f"`[N]` түріне түрлендірілді (GOST 7.32-2001 §6.11, алғаш кездесу ретімен). {N} сыртқы "
          f"дереккөз [1]–[{N}] болып нөмірленді. Нөмірлер ағылшын тіліндегі мәтінмен ортақ "
          f"(тіл-инварианттылық).\n")

# The first appendix heading, in either language. The corpus form leads with the
# word ("APPENDIX A" / "ҚОСЫМША А"); the superseded letter-first Kazakh form is
# kept so an older assembly still anchors.
_APPENDIX_A = re.compile(
    r"^#\s+(?:APPENDIX\s+A\b|ҚОСЫМША\s+А\b|А\s+қосымшасы)", re.M | re.I)
# The divider the assembler emits ahead of the appendix chapter.
_APPENDICES = re.compile(r"^#\s+(?:APPENDICES|ҚОСЫМШАЛАР)\s*$", re.M)


def place_references(body: str, block: str) -> str:
    """Insert the reference list between the Conclusion and the appendices.

    GOST 7.32-2001 orders the list of sources after the conclusion and before the
    appendices. Appending the block to the assembled text put it after Appendix F,
    which is where it sat in every build so far.

    The anchor is the APPENDICES divider where the assembler emits one, and the
    first appendix heading otherwise. Anchoring on Appendix A alone was correct
    only in the second case: with the divider present, the reference list landed
    *between* the divider and Appendix A, so the document announced its appendices
    and then delivered the bibliography.

    Structural elements are separated by a blank line only. A Markdown "---"
    reaches md2gost as a real bottom-bordered paragraph and prints as a black rule
    across the page; every "# " heading already opens a page of its own, so the
    rule bought nothing and left a stripe at the foot of the preceding part.
    """
    m = _APPENDICES.search(body) or _APPENDIX_A.search(body)
    if not m:
        return body + block
    return (body[:m.start()].rstrip() + "\n" + block.rstrip()
            + "\n\n" + body[m.start():])


# Entries are separated by a BLANK line, not a single newline. A single newline
# is a Markdown soft break, so md2gost buffered all 99 entries into ONE justified
# paragraph of 22,522 characters: the printed list was a wall of running text in
# which the numbers 1…99 sat inside the line as ordinary words. Every one of the
# 16 dissertations published by this council sets one source per paragraph.
#
# No explanatory blockquote under the heading and no closing note either: the
# corpus has neither, and "literature card" is internal machinery that peer-norms
# section 8 keeps off the printed page. The block carries no --- rule of its own,
# and none is emitted ahead of the appendices either: see place_references().
REFS_EN = "\n\n# LIST OF REFERENCES USED\n\n" + "\n\n".join(refs)
REFS_KZ = "\n\n# ПАЙДАЛАНЫЛҒАН ӘДЕБИЕТТЕР ТІЗІМІ\n\n" + "\n\n".join(refs)

OUT_EN.write_text(hdr_en + "\n" + place_references(conv_en, REFS_EN), encoding="utf-8")
if conv_kz is not None:
    OUT_KZ.write_text(hdr_kz + "\n" + place_references(conv_kz, REFS_KZ), encoding="utf-8")

# ---------- QA report ----------
b_en, s_en, a_en, u_en = residual(conv_en)
n_en = len(re.findall(r"\[\d+(?:,[^\]]*)?\]", conv_en))
if conv_kz is not None:
    b_kz, s_kz, a_kz, u_kz = residual(conv_kz)
    n_kz = len(re.findall(r"\[\d+(?:,[^\]]*)?\]", conv_kz))
else:
    b_kz = s_kz = a_kz = u_kz = []
    n_kz = 0

kz_line = (f"`{SRC_KZ.name}`" if SRC_KZ else
           f"**none** — no `DISSERTATION_KZ_partial_{_STAMP}.md`, so the Kazakh volume was "
           f"not converted on this run")

q = [f"# Stage-G citation conversion — FINAL resolution & QA ({date.today()})\n",
     f"Sources: `{SRC_EN.name}` + {kz_line}.",
     f"Outputs: `{OUT_EN.name}`" + (f", `{OUT_KZ.name}`" if SRC_KZ else "") + ".",
     "Numbering assigned ONCE by first appearance in EN, reused verbatim in KZ (rule #7).\n",
     "## Summary",
     f"- External sources numbered: **{N}**  |  Highest [N]: **{N}**",
     f"- Bracketed citations placed — EN: **{n_en}** | KZ: **{n_kz}**",
     f"- Residual *resolvable* author-year (BLOCKING) — EN: **{len(b_en)}** | KZ: **{len(b_kz)}**",
     f"- Left as author-year by policy — self EN/KZ: **{len(s_en)}/{len(s_kz)}** ; App-D EN/KZ: **{len(a_en)}/{len(a_kz)}**",
     f"- UNKNOWN author-year (needs a card or is non-citation prose) — EN: **{len(u_en)}** | KZ: **{len(u_kz)}**",
     f"- Numbered sources with no GOST description (falling back to APA): **{len(undescribed)}**"
     + (f" ({', '.join(undescribed)})" if undescribed else "") + "\n",
     "## BLOCKING — resolvable but still author-year (must be 0)",
     "### EN"] + ([f"- {t}: `{s}`" for t, s in b_en] or ["- none"]) + ["### KZ"] + ([f"- {t}: `{s}`" for t, s in b_kz] or ["- none"])
q += ["\n## UNKNOWN author-year (review — uncarded source or false positive)", "### EN"]
q += ([f"- {t}: `{s}`" for t, s in sorted(set(u_en))] or ["- none"])
q += ["### KZ"] + ([f"- {t}: `{s}`" for t, s in sorted(set(u_kz))] or ["- none"])
q += ["\n## Self-citations left author-year (policy) — distinct surface forms",
      "### EN"] + (sorted({s for _, s in s_en}) or ["- none"]) + ["### KZ"] + (sorted({s for _, s in s_kz}) or ["- none"])
q += ["\n## Entries completed against the published record",
      "The literature card for each of these names no publication venue, so the description could",
      "not be derived from the card alone (protocol rule 3 forbids inventing the missing area). The",
      "venue, volume and pages were taken from the published article; where the version of record",
      "postdates the card, the entry carries the published year and the in-text number is unaffected."]
q += [f"- [{cardN[c]}] `{c}`" for c in sorted(external, key=lambda c: cardN.get(c, 0))
      if c in cardN] or ["- none"]

carded = set(apa_bib) - {"wikipedia-clahe.md"}
uncited = sorted(carded - set(cardN))
q += ["\n## Carded but not cited (informational)",
      f"Cards in the corpus that the four-chapter volume never cites: **{len(uncited)}** of "
      f"{len(carded)}. Expected — the rewrite compressed six chapters into four — and allowed: a",
      "list of references used holds the sources the running text uses, not the corpus behind it.",
      ", ".join(uncited) or "none"]

q.append("\n## Reference list (in order of appearance)")
q += refs
OUT_QA.write_text("\n".join(q), encoding="utf-8")

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
print(f"WROTE {OUT_EN.name}  (brackets: {n_en})")
print(f"WROTE {OUT_KZ.name}  (brackets: {n_kz})" if SRC_KZ else
      f"SKIPPED KZ — no DISSERTATION_KZ_partial_{_STAMP}.md")
print(f"WROTE {OUT_QA.name}")
print(f"External sources numbered: {N}")
print(f"BLOCKING  EN={len(b_en)}  KZ={len(b_kz)}   UNKNOWN  EN={len(u_en)}  KZ={len(u_kz)}")
