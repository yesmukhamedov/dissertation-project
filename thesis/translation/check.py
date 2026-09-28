"""Mechanical acceptance of a translation chunk (no model involved).
Errors must be fixed (they trigger a retry); warnings are listed for the reviewer.

  python check.py <source.md> <translation.md> [--src en --tgt ru]   -> checks two whole files"""
import argparse, collections, re
from lib import read, split_parts, numbers, detect_lang, term_hits, load_termbase, LANG_NAME

LEN_RATIO = (0.65, 1.5)          # chars(tgt)/chars(src); measured medians 0.95-1.0, p5-p95 0.82-1.11
EN_FUNCTION = re.compile(r"\b(the|and|of|which|that|with|is|are|was|were|this|from|by|for)\b", re.I)
KZ_ONLY = re.compile(r"[әғқңөұүһіӘҒҚҢӨҰҮҺІ]")
CYR = re.compile(r"[А-Яа-яЁё]")
NAME_RE = re.compile(r"\b(?=[A-Za-z0-9\-]*[A-Z][A-Za-z0-9\-]*[A-Z0-9])[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9]\b")
AUTHOR_RE = re.compile(r"\b([A-Z][a-z]+(?:[- ][A-Z][a-z]+)?)(?= (?:et al\.|and [A-Z]|и др\.|т\.б\.|и [A-Z]|(?:пен|мен|бен) [A-Z])|,? \(?(?:19|20)\d\d)")
META_RE = re.compile(r"^\s*(here is|translation:|перевод:|аударма:|```|note:|примечание:)", re.I)
FORBIDDEN = {
    "kz": [("және әріптестері", "calque for et al.; use т.б."), (" — ", "long dash; Kazakh copula dash is ' – '"),
           ("et al", "use т.б.")],
    "ru": [("et al", "use и др."), ("и коллеги", "use и др."), ("т.б.", "Kazakh abbreviation in Russian text"),
           (" — ", "long dash; the volume uses ' – '")],
    "en": [("т.б.", "use et al."), ("и др.", "use et al."), (" — ", "long dash; the volume uses ' – '")],
}
SOFT = {  # allowed in small numbers (conformance.py: <= 12 per volume), so a warning, not an error
    "kz": [(", сондықтан", "«сондықтан» after a comma; prefer -дықтан/-діктен or a new sentence")],
}


UNIT_ABBR = {"GB", "MB", "MiB", "GiB", "KB", "CI", "DR", "OD", "CPU", "GPU", "RAM", "PDF", "USB"}
MONTHS = set("January February March April May June July August September October November December".split())


def names(text):
    """Latin identifiers that must survive translation: model/dataset/metric names and codes."""
    return collections.Counter(m for m in NAME_RE.findall(text) if not m.isdigit())


def authors(text):
    """Author surnames in citations. Kazakh authors may be transliterated to Cyrillic -> warning only."""
    return collections.Counter(a for a in AUTHOR_RE.findall(text) if a not in MONTHS)


def struct(text):
    lines = text.split("\n")
    heads = [re.match(r"^(#+)\s*([\dA-ZА-ЯӘ.]*)", l).groups() for l in lines if l.startswith("#")]
    rows = sum(1 for l in lines if l.lstrip().startswith("|"))
    cols = [l.count("|") for l in lines if l.lstrip().startswith("|")]
    return heads, rows, cols


def check(src, tgt, sl, tl, termbase=None):
    """-> (errors, warnings), each a list of short strings."""
    err, warn = [], []
    if not tgt.strip():
        return ["empty output"], warn
    if META_RE.search(tgt):
        err.append("meta text or code fence around the translation")

    # numbers
    a, b = collections.Counter(numbers(src, sl)), collections.Counter(numbers(tgt, tl))
    miss, extra = a - b, b - a
    if miss:
        err.append("numbers missing: " + ", ".join(sorted(miss.elements())[:12]))
    if extra:
        warn.append("numbers added: " + ", ".join(sorted(extra.elements())[:12]))

    # Latin names / codes / authors
    na, nb = names(src), names(tgt)
    low = tgt.lower()
    lost = [n for n in na if nb[n] == 0 and n not in UNIT_ABBR
            and not all(p.lower() in low for p in re.findall(r"[A-Z]{2,}|[A-Za-z]*\d+[A-Za-z]*", n) or [n])]
    # Title-Case English compounds (Decision-Support, Kazakh-British) are ordinary words that get translated
    soft = [n for n in lost if re.fullmatch(r"[A-Z][a-z]+(?:-[A-Za-z][a-z]+)+", n)]
    lost = [n for n in lost if n not in soft]
    if soft:
        warn.append("hyphenated names translated (verify): " + ", ".join(soft[:8]))
    if lost:
        err.append("names/codes lost: " + ", ".join(lost[:12]))
    aa, ab = authors(src), authors(tgt) + names(tgt)
    lost = [n for n in aa if ab[n] == 0 and n not in na]
    if lost:
        warn.append("authors not found in Latin: " + ", ".join(lost[:8]))

    # citations [n]
    ca, cb = re.findall(r"\[\d+(?:[–,\-]\s*\d+)*\]", src), re.findall(r"\[\d+(?:[–,\-]\s*\d+)*\]", tgt)
    if sorted(ca) != sorted(cb):
        err.append(f"bracket citations differ: {sorted(set(ca) ^ set(cb))[:6]}")

    # markdown structure
    (ha, ra, cola), (hb, rb, colb) = struct(src), struct(tgt)
    if [h[0] for h in ha] != [h[0] for h in hb]:
        err.append(f"headings differ: {len(ha)} in source, {len(hb)} in translation")
    elif [h[1] for h in ha] != [h[1] for h in hb] and tl != "kz" and sl != "kz":
        warn.append("heading numbers differ")
    if ra != rb:
        err.append(f"table rows differ: {ra} vs {rb}")
    elif cola != colb:
        err.append("table columns differ")
    if src.count("**") != tgt.count("**"):
        warn.append(f"bold markers differ: {src.count('**')} vs {tgt.count('**')}")

    # script leaks / untranslated text
    if tl in ("ru", "kz"):
        eng = EN_FUNCTION.findall(re.sub(r"`[^`]*`|\([^)]*\d{4}[^)]*\)", "", tgt))
        if len(eng) > 2:
            err.append(f"English left untranslated ({len(eng)} function words, e.g. {', '.join(eng[:4])})")
    if tl == "ru" and len(KZ_ONLY.findall(tgt)) > 0:
        err.append(f"Kazakh letters in Russian text: {''.join(sorted(set(KZ_ONLY.findall(tgt))))}")
    if tl == "kz" and sl == "ru":
        pass  # Russian and Kazakh share Cyrillic; rely on length and terms
    if tl == "en":
        cyr = len(CYR.findall(tgt)) + len(KZ_ONLY.findall(tgt))
        if cyr > len(CYR.findall(src)) * 0.02 + 5:
            err.append(f"Cyrillic left in English text ({cyr} letters)")

    # forbidden forms
    for form, why in FORBIDDEN.get(tl, []):
        if form in tgt:
            err.append(f"forbidden «{form.strip()}»: {why}")
    for form, why in SOFT.get(tl, []):
        if form in tgt:
            warn.append(f"«{form.strip()}»: {why}")

    # length
    r = len(tgt) / max(len(src), 1)
    if len(src) > 200 and not LEN_RATIO[0] <= r <= LEN_RATIO[1]:
        err.append(f"length ratio {r:.2f} outside {LEN_RATIO} (dropped or invented text?)")

    # terminology (warning: inflection makes exact checking impossible)
    if termbase:
        for row in term_hits(src, termbase, sl):
            want = row.get(tl, "").split(";")[0].strip()
            if want and want != "?" and not term_hits(tgt, [{tl: want}], tl):
                warn.append(f"term «{row[sl].split(';')[0]}» not rendered as «{want}»")
    return err, warn


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("tgt")
    ap.add_argument("--src-lang")
    ap.add_argument("--tgt-lang")
    a = ap.parse_args()
    s, t = split_parts(read(a.src))[1], split_parts(read(a.tgt))[1]
    sl, tl = a.src_lang or detect_lang(s), a.tgt_lang or detect_lang(t)
    err, warn = check(s, t, sl, tl, load_termbase())
    print(f"{LANG_NAME[sl]} -> {LANG_NAME[tl]}: {len(err)} errors, {len(warn)} warnings")
    for e in err:
        print("  ERROR", e)
    for w in warn[:30]:
        print("  warn ", w)


if __name__ == "__main__":
    main()
