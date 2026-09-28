"""Step 1 of the termbase: pull EN->KZ pairs out of GLOSSARY_KZ.md (sections A, B, C and the
pretraining addendum) and measure how each Kazakh form is actually used in the chapter
translations. Writes terms_raw.json; the RU column and corrections are added by termbase_fill.py.

usage-rate = share of aligned TM pairs whose EN side contains the term and whose KZ side
contains the glossary form (prefix match). Low rate => the glossary form is stale."""
import json, os, re
from lib import HERE, THESIS, read, write, term_hits

GLOSS = os.path.join(THESIS, "glossary", "GLOSSARY_KZ.md")


def clean(s):
    s = re.sub(r"\*\*|`", "", s)
    s = re.sub(r"\s*\[(ӨЗГЕРТІЛДІ|ҚОСЫЛДЫ|DEPRECATED)[^\]]*\]", "", s)
    return s.strip()


def parse():
    lines = read(GLOSS).split("\n")
    sec, terms = None, []
    for l in lines:
        m = re.match(r"^#{1,2} ([A-G])\. |^## (АЛДЫН АЛА ОҚЫТУ)|^## (ЕСКІРГЕН)|^## (PIPELINE-КОМПОНЕНТ)", l)
        if m:
            sec = m.group(1) or ("P" if m.group(2) else "X" if m.group(3) else "Q")
            continue
        if sec == "A" and l.strip().rstrip("\\").strip() and not l.startswith(("#", "-", "|", "*")):
            t = clean(l.strip().rstrip("\\"))
            if 1 < len(t) < 60:
                terms.append(dict(en=t, kz=t, rule="keep", sec="A"))
        elif sec in ("B", "C", "P", "Q") and l.startswith("|") and not re.match(r"^\|\s*-", l):
            cells = [clean(c) for c in l.strip().strip("|").split("|")]
            if len(cells) < 2 or cells[0].startswith(("Ағылшын", "Термин", "Компонент")):
                continue
            en, kz = cells[0], cells[1]
            note = cells[2] if len(cells) > 2 else ""
            if sec == "C":
                rule, note = "bilingual-first", f"first use: {kz}; later: {note}"
                kz = re.sub(r"\s*\([^)]*\)\s*$", "", kz).strip() or kz
            else:
                rule = "translate"
            terms.append(dict(en=en, kz=kz, rule=rule, sec=sec, note=note[:160]))
    return terms


def usage(terms):
    tm = [json.loads(l) for l in read(os.path.join(HERE, "tm", "tm.jsonl")).split("\n") if l.strip()]
    tm = [r for r in tm if "kz" in r]
    for t in terms:
        en_form = re.sub(r"\s*\[[^\]]*\]|\s*\([^)]*\)", "", t["en"]).strip()
        row = dict(en=en_form, kz=t["kz"].split(";")[0].split("/")[0].strip())
        with_en = [r for r in tm if term_hits(r["en"], [row], "en")]
        t["en_form"] = en_form
        t["n_en"] = len(with_en)
        t["n_both"] = sum(bool(term_hits(r["kz"], [row], "kz")) for r in with_en)
    return terms


def main():
    terms = usage(parse())
    seen, out = set(), []
    for t in terms:
        k = t["en_form"].lower()
        if k and k not in seen:
            seen.add(k)
            out.append(t)
    write(os.path.join(HERE, "work", "terms_raw.json"), json.dumps(out, ensure_ascii=False, indent=1))
    by = {}
    for t in out:
        by.setdefault(t["sec"], []).append(t)
    for s, ts in by.items():
        used = [t for t in ts if t["n_en"]]
        ok = [t for t in used if t["n_both"] / t["n_en"] >= 0.5]
        print(f"sec {s}: {len(ts)} terms, {len(used)} occur in EN chapters, {len(ok)} with glossary KZ form confirmed")
    stale = [t for t in out if t["n_en"] >= 2 and t["n_both"] / t["n_en"] < 0.5 and t["rule"] != "keep"]
    print(f"stale candidates: {len(stale)}")
    for t in stale[:25]:
        print(f"  {t['en_form'][:40]:40} -> {t['kz'][:40]:40} {t['n_both']}/{t['n_en']}")


if __name__ == "__main__":
    main()
