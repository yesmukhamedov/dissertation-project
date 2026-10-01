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
           ("et al", "use т.б."), ("қисым астындағы", "AUC is «қисық астындағы аудан»"),
           ("иілу астындағы", "AUC is «қисық астындағы аудан»"), (" өлген", "«өлген» means 'died'; 'measured' is «өлшенген»"),
           ("корпусар", "plural of корпус is «корпустар»"), ("корпусал", "plural of корпус is «корпустар»"),
           ("сынып", "a class (of DR) is «класс», «сынып» is a school class"),
           ("лезия", "lesion is «зақымдану»"), ("шәкіл", "pupil is «қарашық»"),
           ("бастық", "«бастық» = boss; a network head is «бас»"), ("ыдыс", "«ыдыс» = dish; a blood vessel is «тамыр»"),
           ("көз қарн", "retinal is «торқабық»"), ("Бейбітшілік", "adversarial is «адверсариалды»"),
           (" есік", "threshold is «табалдырық», gate is «қақпа»"), (" еден", "floor (lower bound) is «төменгі шек»"),
           ("ахир", "posterior is «апостериорлық ықтималдық»"), ("сущност", "entity is «мән»"),
           ("прирост", "increment is «өсім»"), ("прогон", "run is «іске қосу»"), ("микрососуд", "microvascular is «микротамырлық»"),
           ("пайыздық пункт", "percentage points is «пайыздық тармақ»"), ("батч", "batch is «топтама»"),
           ("корпустаралық", "cross-corpus is «корпусаралық»"),
           ("ұздатыл", "frozen (backbone/layers) is «қатырылған»"),
           ("таралым", "distribution is «үлестірім»"),
           ("отбасы", "family (of architectures, methods, perturbations) is «тұқымдас»"),
           ("тірек желі", "backbone stays Latin: «backbone», «backbone-да»")],
    "ru": [("et al", "use и др."), ("и коллеги", "use и др."), ("т.б.", "Kazakh abbreviation in Russian text"),
           (" — ", "long dash; the volume uses ' – '")],
    "en": [("т.б.", "use et al."), ("и др.", "use et al."), (" — ", "long dash; the volume uses ' – '")],
}
SOFT = {  # allowed in small numbers (conformance.py: <= 12 per volume), so a warning, not an error
    "kz": [(", сондықтан", "«сондықтан» after a comma; prefer -дықтан/-діктен or a new sentence")],
}


# official documents: "(далее – X)" must come out as the target language's definition formula
HEREINAFTER = {"ru": r"\(далее\s*[–-]", "kz": r"\(бұдан әрі\s*[–-]", "en": r"\(hereinafter\b"}
# Kazakh compounds written with a spaced dash instead of a hyphen (сондай – ақ, профессор – оқытушылар)
KZ_SPACED_HYPHEN = re.compile(r"\b(сондай|профессор|ғылыми|практик|оқу|әлеуметтік|физика|техника)\s+[–—-]\s+(?=[а-яәғқңөұүһі])")
# Russian calques and Russian abbreviations that Qwen leaves in Kazakh (rules/kz.md)
KZ_CALQUE = re.compile(r"(?i:нейросет|сверткал|свёрткал|машиналық оқу(?!ы)|\bрывок|\bлокальд|детекциял|"
                       r"компенсацияла|жазу қолы)|\bЗРК\b|\bБА\b|\bИМУ\b|\bИИ\b")
# appendix letters: A->А, B->Ә, C->Б, D->В, E->Г, F->Ғ; markers like [FIG-C.1] stay Latin and are skipped
KZ_APPENDIX = dict(zip("ABCDEF", "АӘБВГҒ"))
EN_APPX = re.compile(r"(?<![\w.\[-])([A-F])(?=\.\d)|\bAppendix ([A-F])\b")
KZ_APPX = re.compile(r"(?<![\w.\[-])([A-ZА-ЯӘҒҚҢӨҰҮҺІ])(?=\.\d|\s+қосымша)")
LIST_MARK = re.compile(r"^\s*(\d{1,2}[.)]|[а-яa-zәғқ]\)|[•·▪\-–])\s", re.M)


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


def check(src, tgt, sl, tl, termbase=None, genre="thesis"):
    """-> (errors, warnings), each a list of short strings. genre=council: official documents
    (decimal comma in Kazakh too, rules/genre-council.md)."""
    err, warn = [], []
    if not tgt.strip():
        return ["empty output"], warn
    if META_RE.search(tgt):
        err.append("meta text or code fence around the translation")

    # numbers
    a, b = collections.Counter(numbers(src, sl, genre)), collections.Counter(numbers(tgt, tl, genre))
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

    # Latin words that are not in the source (hallucinated names such as "vision transformer")
    if sl in ("ru", "kz") and tl in ("ru", "kz"):
        lat_s = {w.lower() for w in re.findall(r"[A-Za-z]{4,}", src)}
        new = sorted({w for w in re.findall(r"[A-Za-z]{4,}", tgt) if w.lower() not in lat_s})
        if new:
            err.append(f"Latin words not in the source: {', '.join(new[:6])} (added or invented?)")

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
    # a paragraph that starts with a capital letter in the source starts with one in the translation
    # (Qwen lowercases paragraphs that follow a list of lowercase items)
    pa, pb = [p.strip() for p in src.split("\n\n") if p.strip()], [p.strip() for p in tgt.split("\n\n") if p.strip()]
    if len(pa) == len(pb):
        first = lambda p: next((c for c in p if c.isalpha()), "")
        bad = [i + 1 for i, (x, y) in enumerate(zip(pa, pb))
               if first(x).isupper() and first(y).islower() and x[:1].isalpha() and y[:1].isalpha()]
        if bad:
            err.append(f"paragraphs {bad[:6]} start with a lowercase letter; the source starts them with a capital")
    if src.count("**") != tgt.count("**"):
        warn.append(f"bold markers differ: {src.count('**')} vs {tgt.count('**')}")

    # script leaks / untranslated text
    if tl in ("ru", "kz"):
        strip = lambda x: re.sub(r"`[^`]*`|\([^)]*\d{4}[^)]*\)", "", x)
        eng = EN_FUNCTION.findall(strip(tgt))
        if sl != "en":      # English copied from a non-English source (paper titles) is not a leftover
            eng = list((collections.Counter(w.lower() for w in eng)
                        - collections.Counter(w.lower() for w in EN_FUNCTION.findall(strip(src)))).elements())
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
    tgt_f = tgt.replace("корпусаралы", "")   # «корпусаралық» (cross-corpus) is correct, not a bad plural
    for form, why in FORBIDDEN.get(tl, []):
        if form in tgt_f:
            err.append(f"forbidden «{form.strip()}»: {why}")
    for form, why in SOFT.get(tl, []):
        if form in tgt:
            warn.append(f"«{form.strip()}»: {why}")

    # official documents (genre council)
    if genre == "council":
        if re.search(HEREINAFTER[sl], src) and not re.search(HEREINAFTER[tl], tgt):
            err.append(f"definition formula missing: source has «{HEREINAFTER[sl][2:8]}…», translation needs "
                       f"«{ {'ru': '(далее – X)', 'kz': '(бұдан әрі – X)', 'en': '(hereinafter – X)'}[tl]}»")
        la, lb = LIST_MARK.findall(src), LIST_MARK.findall(tgt)
        norm = lambda xs: [x if x[0].isdigit() else ("*" if x in "•·▪-–" else "a)") for x in xs]
        if norm(la) != norm(lb):
            err.append(f"list markers differ: {la[:6]} vs {lb[:6]}")
    if tl == "kz":
        if "ə" in tgt or "Ə" in tgt:
            err.append("Latin ə in Kazakh text: use Cyrillic ә")
        c = sorted({x.lower() for x in KZ_CALQUE.findall(tgt)} - {x.lower() for x in KZ_CALQUE.findall(src)}
                   if sl == "kz" else {x.lower() for x in KZ_CALQUE.findall(tgt)})
        if c:
            err.append(f"Russian calque/abbreviation in Kazakh: {', '.join(c[:5])} (see rules: нейрондық желі, "
                       f"конволюциялық, машиналық оқыту, АА, IMU, ҚРЗ)")
        if re.search(r"жасуша(?!лық)", tgt) and not re.search(r"cellular|pericyte", src, re.I):
            err.append("«жасуша» is a biological cell: a table/matrix/design cell is «ұяшық»")
        alien = re.findall(r"[֐-ۿ฀-๿぀-ヿ㐀-鿿가-힯]+", tgt)
        if alien:
            err.append(f"foreign-script characters in Kazakh text: {' '.join(alien[:5])}")
        mixed = re.findall(r"\b\w*(?:[A-Za-z][а-яәғқңөұүһі]|[а-яәғқңөұүһі][A-Za-z])\w*", re.sub(r"`[^`]*`", "", tgt))
        if mixed:
            err.append(f"Latin and Cyrillic letters mixed in one word: {', '.join(mixed[:4])}")
        if re.search(r"[A-Z][a-z]+ және [A-Z][a-z]+,? \(?(19|20)\d\d", tgt):
            err.append("citation joins the last two authors with «және»: use пен/мен/бен (Sapakov мен Kozhamkulova, 2025)")
        if re.search(r"дегенде (барл|бірдей|жой|толық|түгел|құнды)", tgt):
            err.append("«дегенде» used for 'almost': write «дерлік» (дерлік барлығы, дерлік бірдей)")
        m = KZ_SPACED_HYPHEN.findall(tgt)
        if m:
            err.append(f"spaced dash inside a compound word ({m[0]} – …): write a hyphen, e.g. сондай-ақ")
        if sl == "en":
            want = {KZ_APPENDIX[a or b] for a, b in EN_APPX.findall(src)}
            got = set(KZ_APPX.findall(tgt))
            if got - want:
                err.append(f"appendix letters {sorted(got - want)} do not match the source (A->А, B->Ә, C->Б, "
                           f"D->В, E->Г, F->Ғ; expected {sorted(want)}): «Ә қосымшасы», «Б.1-кесте»")
            elif want - got:
                warn.append(f"appendix references {sorted(want - got)} not found in the translation")

    # length
    r = len(tgt) / max(len(src), 1)
    if len(src) > 200 and not LEN_RATIO[0] <= r <= LEN_RATIO[1]:
        err.append(f"length ratio {r:.2f} outside {LEN_RATIO} (dropped or invented text?)")

    # terminology (warning: inflection makes exact checking impossible)
    if termbase:
        prose = re.sub(r"`[^`]*`|\[[A-Z]+-[^\]]*\]|\S+/\S+", " ", src)   # code, [FIG-..] markers, paths stay verbatim
        for row in term_hits(prose, termbase, sl):
            want = row.get(tl, "").split(";")[0].strip()
            if want and want != "?" and not term_hits(tgt, [{tl: row[tl]}], tl):   # any ";" variant counts
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
