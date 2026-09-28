"""Step 2 of the termbase: for every candidate term, Qwen reads how the term was actually
rendered in the aligned EN-KZ chapter paragraphs and proposes the Russian equivalent (with the
Russian abstract as the style reference). Each Kazakh form is checked mechanically against the
evidence text; unconfirmed forms are flagged for review.

  python termbase_fill.py            -> work/terms_filled.json, termbase.tsv (only if absent), work/review.tsv
  python termbase_fill.py --limit 12 -> dry run on the first batch"""
import argparse, json, os, re, time
from lib import HERE, THESIS, read, write, term_hits, ensure_server, chat

BATCH = 10
SCHEMA = {"type": "array", "items": {"type": "object", "properties": {
    "en": {"type": "string"},
    "kz": {"type": "string"},
    "kz_keeps_latin": {"type": "boolean"},
    "ru": {"type": "string"},
    "note": {"type": "string"}},
    "required": ["en", "kz", "kz_keeps_latin", "ru", "note"]}}

SYSTEM = """You build a trilingual (English / Russian / Kazakh) terminology base for a PhD dissertation
on automated diabetic retinopathy diagnosis (fundus image preprocessing + CNN classification).
You are precise: the Kazakh form must be copied from the evidence, never invented.

RUSSIAN STYLE REFERENCE - the approved Russian abstract of the same dissertation:
<<<
{abstract_ru}
>>>"""

TASK = """For each TERM below you get aligned paragraph pairs (EN = original, KZ = the approved
Kazakh translation of that paragraph).

For each term return one JSON object:
- en: the term exactly as given.
- kz: the Kazakh rendering actually used in the KZ paragraphs, in dictionary (nominative) form,
  e.g. "интеграцияланған конфигурация". Copy the words from the KZ text; only drop case endings.
  If the KZ text keeps the term in Latin script, give it as it appears (e.g. "Grad-CAM") and set kz_keeps_latin=true.
  If no pair is given or the term is not visible in KZ, write your best academic Kazakh form and start note with "GUESS".
- ru: the standard Russian scientific term (nominative). Prefer the form used in the Russian abstract when it
  occurs there. Keep in Latin what Russian ML/ophthalmology papers keep in Latin (model names, metrics like F1, Grad-CAM).
- note: at most 12 words; mention a second accepted variant or a trap. Empty string if nothing to add.
Return a JSON array in the same order as the terms. No other text.

{items}"""


def load_candidates():
    terms = [l.strip() for l in read(os.path.join(HERE, "work", "candidates.txt")).split("\n")
             if l.strip() and not l.startswith("#")]
    raw = json.loads(read(os.path.join(HERE, "work", "terms_raw.json")))
    seen = {t.lower() for t in terms}
    for t in raw:
        if t["n_en"] and t["en_form"].lower() not in seen:
            terms.append(t["en_form"])
            seen.add(t["en_form"].lower())
    return terms


def evidence(term, tm):
    rows = [r for r in tm if "kz" in r and term_hits(r["en"], [dict(en=term)], "en")]
    rows.sort(key=lambda r: len(r["en"]))
    return rows[:2]


def confirmed(kz, rows):
    if not kz:
        return False
    return any(term_hits(r["kz"], [dict(kz=kz)], "kz") for r in rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int)
    a = ap.parse_args()
    tm = [json.loads(l) for l in read(os.path.join(HERE, "tm", "tm.jsonl")).split("\n") if l.strip()]
    terms = load_candidates()[:a.limit] if a.limit else load_candidates()
    out_path = os.path.join(HERE, "work", "terms_filled.json")
    done = {d["en"].lower(): d for d in json.loads(read(out_path))} if os.path.exists(out_path) else {}
    todo = [t for t in terms if t.lower() not in done]
    print(f"{len(terms)} terms, {len(todo)} to do, {(len(todo) + BATCH - 1) // BATCH} calls")
    if todo and not ensure_server():
        raise SystemExit("Qwen server did not start")
    system = SYSTEM.format(abstract_ru=read(os.path.join(THESIS, "output", "abstract_ru.md")))
    for i in range(0, len(todo), BATCH):
        batch = todo[i:i + BATCH]
        ev = {t: evidence(t, tm) for t in batch}
        items = []
        for n, t in enumerate(batch, 1):
            items.append(f"TERM {n}: {t}")
            for r in ev[t]:
                items.append(f"EN: {r['en']}\nKZ: {r['kz']}")
            if not ev[t]:
                items.append("(no aligned pair)")
            items.append("")
        text, info = chat(system, TASK.format(items="\n".join(items)), max_tokens=2500, temperature=0.2, schema=SCHEMA)
        try:
            res = json.loads(text)
        except json.JSONDecodeError:
            print(f"batch {i // BATCH}: BAD_JSON finish={info['finish']}")
            continue
        for t, r in zip(batch, res):
            r["en"] = t
            r["n_ev"] = len(ev[t])
            r["kz_confirmed"] = r["kz_keeps_latin"] or confirmed(r["kz"], ev[t])
            done[t.lower()] = r
        write(out_path, json.dumps(list(done.values()), ensure_ascii=False, indent=1))
        print(f"batch {i // BATCH + 1}: {len(res)} terms, {info['sec']}s, prompt {info['p_tok']} tok "
              f"@{info['pp_tps']}/s, gen {info['c_tok']} @{info['tg_tps']}/s", flush=True)

    # review table + termbase
    rows = list(done.values())
    rev = ["en\tru\tkz\tkz_confirmed\tn_ev\tnote"]
    rev += [f"{r['en']}\t{r['ru']}\t{r['kz']}\t{int(r['kz_confirmed'])}\t{r['n_ev']}\t{r['note']}" for r in rows]
    write(os.path.join(HERE, "work", "review.tsv"), "\n".join(rev) + "\n")
    print(f"confirmed KZ: {sum(r['kz_confirmed'] for r in rows)}/{len(rows)}; "
          f"with evidence: {sum(r['n_ev'] > 0 for r in rows)}")


if __name__ == "__main__":
    main()
