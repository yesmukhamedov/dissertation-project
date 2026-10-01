"""Build the translation memory tm/tm.jsonl from the existing parallel texts:
chapter drafts (EN) <-> translations (KZ), and output/abstract_{en,ru,kz}.md (EN/RU/KZ).
Held-out eval sections (eval.py) are excluded so evaluation never sees its own reference."""
import json, os, re
from lib import HERE, THESIS, read, write, split_parts, blocks, kind, align, section_pairs

HOLDOUT = {"1.3", "2.3", "3.4", "4.2", "conclusion"}
# council documents (corpus/, made by extract_body.py): test abstracts and the first half of GD_01 stay out
COUNCIL_HOLDOUT = {"bakirova", "bazarbekov", "toktarova",      # tuning test set (eval --set council)
                   "olzhayev", "mukhanov"}                   # untouched validation (eval --set council-valid)
GD01_SPLIT = 0.5
MAX_COST = 2.2          # alignment links costlier than this are dropped as unreliable
MIN_CHARS = 40


def keep(s, t, c):
    return c <= MAX_COST and min(len(s), len(t)) >= MIN_CHARS and kind(s) == "text" == kind(t)


def keep_council(s, t, c):
    """Human council texts are looser translations than the thesis: stricter cost and a length-ratio gate."""
    r = len(t) / max(len(s), 1)
    return keep(s, t, c) and c <= 1.5 and 0.6 <= r <= 1.7 and s.count("\n\n") == t.count("\n\n")


def corpus_blocks(path):
    return [b for b in blocks(read(path)) if kind(b) == "text"] if os.path.exists(path) else []


def council_rows(stats):
    """Bilingual rows from the trilingual council abstracts and GD_01 (RU/KZ), domain=council."""
    rows = []
    base = os.path.join(HERE, "corpus")
    ab = os.path.join(base, "abstracts")
    slugs = sorted({f.split(".")[0] for f in os.listdir(ab)}) if os.path.isdir(ab) else []
    for slug in slugs:
        if slug in COUNCIL_HOLDOUT:
            continue
        b = {l: corpus_blocks(os.path.join(ab, f"{slug}.{l}.md")) for l in ("ru", "kz", "en")}
        n = 0
        for x, y in (("ru", "kz"), ("en", "ru"), ("en", "kz")):
            for s, t, c in align(b[x], b[y]):
                if keep_council(s, t, c):
                    rows.append(dict(src="council/" + slug, domain="council", **{x: s, y: t}, cost=round(c, 2)))
                    n += 1
        stats.append(f"council {slug:14} rows={n}")
    ru, kz = (corpus_blocks(os.path.join(base, "gd01", f"gd01.{l}.md")) for l in ("ru", "kz"))
    links = [(s, t, c) for s, t, c in align(ru, kz) if keep_council(s, t, c)]
    cut = int(len(links) * GD01_SPLIT)
    rows += [dict(src="council/gd01", domain="council", ru=s, kz=t, cost=round(c, 2)) for s, t, c in links[cut:]]
    stats.append(f"council gd01           rows={len(links) - cut} (first {cut} links held out)")
    # the frozen eval texts (work/gold/_draft) never reach the TM, whatever the alignment does
    frozen = os.path.join(HERE, "work", "gold", "_draft")
    test = set()
    for f in os.listdir(frozen) if os.path.isdir(frozen) else []:
        test |= {b.strip() for b in blocks(read(os.path.join(frozen, f)))}
    before = len(rows)
    rows = [r for r in rows if not any(r.get(l, "").strip() in test for l in ("en", "ru", "kz"))]
    stats.append(f"council rows dropped as eval text: {before - len(rows)}")
    return rows


def main():
    rows, stats = [], []
    for sid, en_p, kz_p in section_pairs():
        if not kz_p or sid in HOLDOUT:
            continue
        en_b = [b for b in blocks(split_parts(read(en_p))[1]) if kind(b) != "hr"]
        kz_b = [b for b in blocks(split_parts(read(kz_p))[1]) if kind(b) != "hr"]
        links = align(en_b, kz_b)
        good = [(s, t, c) for s, t, c in links if keep(s, t, c)]
        stats.append(f"{sid:14} en={len(en_b):3} kz={len(kz_b):3} links={len(links):3} kept={len(good):3}")
        rows += [dict(src="chapters/" + sid, en=s, kz=t, cost=round(c, 2)) for s, t, c in good]

    # trilingual abstract: rubric paragraphs, aligned EN->RU and EN->KZ, joined on EN
    ab = {l: [b for b in blocks(read(os.path.join(THESIS, "output", f"abstract_{l}.md")))
              if kind(b) == "text"] for l in ("en", "ru", "kz")}
    en_ru = {s: t for s, t, c in align(ab["en"], ab["ru"]) if keep(s, t, c)}
    en_kz = {s: t for s, t, c in align(ab["en"], ab["kz"]) if keep(s, t, c)}
    n_ab = 0
    for s in ab["en"]:
        if s in en_ru or s in en_kz:
            r = dict(src="output/abstract", en=s)
            if s in en_ru:
                r["ru"] = en_ru[s]
            if s in en_kz:
                r["kz"] = en_kz[s]
            rows.append(r)
            n_ab += 1
    stats.append(f"abstract       en={len(ab['en'])} ru={len(ab['ru'])} kz={len(ab['kz'])} "
                 f"en-ru={len(en_ru)} en-kz={len(en_kz)}")

    rows += council_rows(stats)
    write(os.path.join(HERE, "tm", "tm.jsonl"), "\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n")
    print("\n".join(stats))
    print(f"TM rows: {len(rows)} (abstract {n_ab})")


if __name__ == "__main__":
    main()
