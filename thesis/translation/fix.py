"""Correction round: the reviewer (Opus) writes a task, Qwen applies it. The reviewer never edits translations.

  python fix.py --show <translation.md> [chunk ...]      # source chunk | translation, numbered, for review
  python fix.py <tasks.json>                              # Qwen rewrites the listed chunks, check.py runs

tasks.json - a list of tasks, one per chunk (or "all" chunks of a file):
  [{"out": "chapters/05-conclusion/translated-kk-qwen/conclusion-kz.md", "chunk": 3,
    "issues": ["the clause 'and the qualitative examination ... was not carried out' is missing - translate it",
               "«дегенде бірдей түсті» is wrong for 'declined almost identically' - «дерлік бірдей төмендеді»"]}]
Each issue: what is wrong, where (quote the Kazakh/Russian text), and what the source says or the fix is.
The corrected chunk replaces the cached one in <out>.parts/ (the previous version is kept in "history"),
then the output file and its report are rebuilt from the cache (no other chunk is re-translated).
Report of the round: <tasks>.result.json - per task: applied / rejected (more check errors than before) + errors."""
import argparse, hashlib, json, os, sys
from lib import THESIS, LANG_NAME, read, write, split_parts, load_termbase, ensure_server, chat
from check import check
from translate import (rules, segments, load_postfix, postfix, terms_block, translate_file, load_tm, WORD)


def abs_(p):
    return p if os.path.isabs(p) else os.path.join(THESIS, p)


def chunks_of(out):
    """-> (report, [(chunk_no, source_text, cache_path)])"""
    rep = json.loads(read(abs_(out) + ".report.json"))
    body = split_parts(read(abs_(rep["file"])))[1]
    res, ci = [], 0
    for ok, seg in segments(body):
        if ok:
            ci += 1
            key = hashlib.sha1(f"{rep['src']}>{rep['tgt']}\n{seg}".encode()).hexdigest()[:16]
            res.append((ci, seg, os.path.join(abs_(out) + ".parts", key + ".json")))
    return rep, res


def show(out, which):
    rep, ch = chunks_of(out)
    for n, seg, cp in ch:
        if which and n not in which:
            continue
        r = json.loads(read(cp))
        print(f"\n===== chunk {n}  errors {r['errors']}  warnings {len(r['warnings'])}")
        print(f"--- SOURCE ({rep['src']})\n{seg}\n--- TRANSLATION ({rep['tgt']})\n{r['out']}")


def fix_prompt(seg, cur, issues, src, tgt, termbase):
    parts = []
    t = terms_block(seg, termbase, src, tgt)
    if t:
        parts.append(f"TERMINOLOGY ({LANG_NAME[src]} = {LANG_NAME[tgt]}), use exactly:\n{t}")
    parts.append(f"SOURCE ({LANG_NAME[src]}):\n<<<\n{seg}\n>>>")
    parts.append(f"CURRENT TRANSLATION ({LANG_NAME[tgt]}):\n<<<\n{cur}\n>>>")
    parts.append("A REVIEWER FOUND THESE ERRORS in the current translation. Fix every one of them:\n" +
                 "\n".join(f"- {e}" for e in issues))
    parts.append(f"Output the whole corrected {LANG_NAME[tgt]} translation of the source chunk, text only. "
                 "Keep everything the reviewer did not mention exactly as it is; change only what the errors require.")
    return "\n\n".join(parts)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", help="tasks.json, or a translation .md with --show")
    ap.add_argument("chunks", nargs="*", type=int)
    ap.add_argument("--show", action="store_true")
    a = ap.parse_args()
    if a.show:
        return show(a.path, set(a.chunks))
    tasks = json.loads(read(a.path))
    if not ensure_server():
        sys.exit("Qwen server did not start (C:\\AI\\start-qwen.ps1)")
    termbase, results, tm = load_termbase(), [], load_tm()
    for t in tasks:
        rep, ch = chunks_of(t["out"])
        genre = rep.get("genre", "thesis")
        sysmsg, fixes = rules(rep["tgt"], genre), load_postfix(rep["tgt"])
        tb = [r for r in termbase if r.get("domain", "all") in ("all", genre)]
        want = None if t["chunk"] == "all" else {t["chunk"]} if isinstance(t["chunk"], int) else set(t["chunk"])
        for n, seg, cp in ch:
            if want and n not in want:
                continue
            r = json.loads(read(cp))
            words = len(WORD.findall(seg))
            txt, info = chat(sysmsg, fix_prompt(seg, r["out"], t["issues"], rep["src"], rep["tgt"], tb),
                             max_tokens=min(8000, 400 + words * 6), temperature=0.2)
            txt = postfix(txt.strip().replace(" — ", " – "), fixes)
            errs, warns = check(seg, txt, rep["src"], rep["tgt"], tb, genre)
            if info["finish"] == "length":
                errs.insert(0, "output truncated")
            r["errors"], r["warnings"] = check(seg, r["out"], rep["src"], rep["tgt"], tb, genre)   # current checker
            ok = len(errs) <= len(r["errors"])
            if ok:
                hist = r.get("history", []) + [dict(out=r["out"], errors=r["errors"], warnings=r["warnings"])]
                r.update(out=txt, errors=errs, warnings=warns, history=hist,
                         fixed_by=r.get("fixed_by", []) + [t["issues"]])
            else:   # keep the old text and the rejected attempt
                r["rejected"] = r.get("rejected", []) + [dict(out=txt, errors=errs, issues=t["issues"])]
            write(cp, json.dumps(r, ensure_ascii=False, indent=1))
            results.append(dict(out=t["out"], chunk=n, applied=ok, errors=errs, warnings=warns, sec=info["sec"]))
            print(f"{t['out']} chunk {n}: {'applied' if ok else 'REJECTED'}, {len(errs)} err, {len(warns)} warn, "
                  f"{info['sec']}s" + (f" | {errs[0][:90]}" if errs else ""), flush=True)
        # rebuild the file from the cache after every task (no model call), so an interrupted round loses nothing
        translate_file(abs_(rep["file"]), rep["src"], rep["tgt"], termbase, tm, os.path.dirname(abs_(t["out"])), 0,
                       lambda m: None, genre=rep.get("genre"))
        write(a.path.rsplit(".", 1)[0] + ".result.json", json.dumps(results, ensure_ascii=False, indent=1))
    write(a.path.rsplit(".", 1)[0] + ".result.json", json.dumps(results, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
