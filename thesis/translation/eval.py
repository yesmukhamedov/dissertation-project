"""Measure how well Qwen translates, against approved human translations it has never seen.

  python eval.py --tag it1                 # EN->KZ on held-out sections + EN->RU on abstract paragraphs
  python eval.py --tag it1 --only ru       # just one part
  python eval.py --compare                 # table of all past runs (work/eval/results.tsv)

EN->KZ: held-out sections (excluded from the TM by build_tm.HOLDOUT), reference = translations/.
EN->RU: EVAL_RU abstract paragraphs, reference = output/abstract_ru.md; the abstract is excluded from
the examples, so this is the no-example (zero-shot + rules + terms) condition that most RU chapter
text will be in.
Metric: chrF++ (character 1-6-grams + word 1-2-grams, beta 2), document level, plus check.py
errors per chunk and the share of chunks accepted on the first try."""
import argparse, collections, json, os, time
from lib import HERE, THESIS, CHAPTERS, read, write, split_parts, blocks, kind, align, ensure_server, load_termbase
from translate import translate_file, load_tm

EVAL_KZ = ["3.4", "4.2", "1.3"]
EVAL_RU_PARAS = 4          # first N abstract rubric paragraphs with a Russian counterpart
RES = os.path.join(HERE, "work", "eval", "results.tsv")


def ngrams(seq, n):
    return collections.Counter(tuple(seq[i:i + n]) for i in range(len(seq) - n + 1))


def chrf(hyp, ref, beta=2, cn=6, wn=2):
    """chrF++ (Popovic 2017), sacrebleu-compatible definition, 0-100."""
    def stats(h, r):
        m = sum((h & r).values())
        return m, sum(h.values()), sum(r.values())
    hs, rs = hyp.replace(" ", ""), ref.replace(" ", "")
    hw, rw = hyp.split(), ref.split()
    scores = []
    for n in range(1, cn + 1):
        scores.append(stats(ngrams(hs, n), ngrams(rs, n)))
    for n in range(1, wn + 1):
        scores.append(stats(ngrams(hw, n), ngrams(rw, n)))
    p = sum(m / h for m, h, _ in scores if h) / len(scores)
    r = sum(m / rr for m, _, rr in scores if rr) / len(scores)
    if p + r == 0:
        return 0.0
    return 100 * (1 + beta ** 2) * p * r / (beta ** 2 * p + r)


def body_text(path):
    return "\n\n".join(b for b in blocks(split_parts(read(path))[1]) if kind(b) in ("text", "heading", "table"))


def find_pair(sid):
    for ch in os.listdir(CHAPTERS):
        en = os.path.join(CHAPTERS, ch, "drafts", f"{sid}-draft.md")
        if os.path.exists(en):
            return en, os.path.join(CHAPTERS, ch, "translations", f"{sid}-translation.md")


def summarise(reports):
    ch = [c for r in reports for c in r["detail"]]
    errs = collections.Counter(e.split(":")[0] for c in ch for e in c["errors"])
    return dict(chunks=len(ch), first_try=sum(1 for c in ch if not c["errors"] and c["attempts"] == 1),
                clean=sum(1 for c in ch if not c["errors"]), minutes=round(sum(r["minutes"] for r in reports), 1),
                warnings=sum(len(c["warnings"]) for c in ch), top_errors=dict(errs.most_common(5)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", default=time.strftime("run-%m%d-%H%M"))
    ap.add_argument("--only", choices=["kz", "ru"])
    ap.add_argument("--compare", action="store_true")
    a = ap.parse_args()
    if a.compare:
        print(read(RES) if os.path.exists(RES) else "no runs yet")
        return
    if not ensure_server():
        raise SystemExit("Qwen server did not start")
    termbase, tm = load_termbase(), load_tm()
    out = os.path.join(HERE, "work", "eval", a.tag)

    def log(m):
        print(time.strftime("%H:%M:%S"), m, flush=True)

    rows = []
    if a.only in (None, "kz"):
        reps, hyp_all, ref_all = [], [], []
        for sid in EVAL_KZ:
            en, kz = find_pair(sid)
            r = translate_file(en, "en", "kz", termbase, tm, os.path.join(out, "kz"), 1, log)
            reps.append(r)
            hyp, ref = body_text(os.path.join(THESIS, r["out"])), body_text(kz)
            hyp_all.append(hyp)
            ref_all.append(ref)
            log(f"  {sid}: chrF++ {chrf(hyp, ref):.1f}")
        s = summarise(reps)
        s["chrf"] = round(chrf("\n".join(hyp_all), "\n".join(ref_all)), 1)
        rows.append(("en>kz", s))

    if a.only in (None, "ru"):
        ab = {l: [b for b in blocks(read(os.path.join(THESIS, "output", f"abstract_{l}.md"))) if kind(b) == "text"]
              for l in ("en", "ru")}
        pairs = [(s, t) for s, t, c in align(ab["en"], ab["ru"]) if c < 2.2 and len(s) > 300][:EVAL_RU_PARAS]
        src = os.path.join(out, "abstract_en_sample.md")
        write(src, "\n\n".join(s for s, _ in pairs) + "\n")
        r = translate_file(src, "en", "ru", termbase, tm, os.path.join(out, "ru"), 1, log, exclude="output/abstract")
        hyp = body_text(os.path.join(THESIS, r["out"]) if not os.path.isabs(r["out"]) else r["out"])
        s = summarise([r])
        s["chrf"] = round(chrf(hyp, "\n\n".join(t for _, t in pairs)), 1)
        rows.append(("en>ru", s))

    new = not os.path.exists(RES)
    with open(RES, "a", encoding="utf-8") as f:
        if new:
            f.write("tag\tdir\tchrF++\tchunks\tfirst_try\tclean_after_retry\twarnings\tminutes\ttop_errors\n")
        for d, s in rows:
            f.write(f"{a.tag}\t{d}\t{s['chrf']}\t{s['chunks']}\t{s['first_try']}\t{s['clean']}\t{s['warnings']}\t"
                    f"{s['minutes']}\t{json.dumps(s['top_errors'], ensure_ascii=False)}\n")
    for d, s in rows:
        log(f"{a.tag} {d}: chrF++ {s['chrf']}, chunks {s['chunks']}, first-try {s['first_try']}, "
            f"clean {s['clean']}, {s['minutes']} min, errors {s['top_errors']}")


if __name__ == "__main__":
    main()
