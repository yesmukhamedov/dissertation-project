"""Build the translation memory tm/tm.jsonl from the existing parallel texts:
chapter drafts (EN) <-> translations (KZ), and output/abstract_{en,ru,kz}.md (EN/RU/KZ).
Held-out eval sections (eval.py) are excluded so evaluation never sees its own reference."""
import json, os, re
from lib import HERE, THESIS, read, write, split_parts, blocks, kind, align, section_pairs

HOLDOUT = {"1.3", "2.3", "3.4", "4.2", "conclusion"}
MAX_COST = 2.2          # alignment links costlier than this are dropped as unreliable
MIN_CHARS = 40


def keep(s, t, c):
    return c <= MAX_COST and min(len(s), len(t)) >= MIN_CHARS and kind(s) == "text" == kind(t)


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

    write(os.path.join(HERE, "tm", "tm.jsonl"), "\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n")
    print("\n".join(stats))
    print(f"TM rows: {len(rows)} (abstract {n_ab})")


if __name__ == "__main__":
    main()
