"""Measure how well Qwen translates, against approved human translations it has never seen.

  python eval.py --tag it1                 # EN->KZ on held-out sections + EN->RU on abstract paragraphs
  python eval.py --tag it1 --only ru       # just one part
  python eval.py --compare                 # table of all past runs (work/eval/results.tsv)
  python eval.py --set council --tag c0    # council documents: 6 directions on held-out human texts

Council set (corpus/ from extract_body.py; the items are held out of the TM by build_tm.COUNCIL_HOLDOUT
and GD01_SPLIT): GD_01 regulation RU<->KZ and trilingual dissertation abstracts, ~700 source words per
item. Two references: the human text (chrF++) and, where it exists, Opus's corrected version
work/gold/<item>.<tgt>.md (chrF_gold) - the human council translations are loose, so chrF_gold is the
main quality number for the council set.

EN->KZ: held-out sections (excluded from the TM by build_tm.HOLDOUT), reference = translations/.
EN->RU: EVAL_RU abstract paragraphs, reference = output/abstract_ru.md; the abstract is excluded from
the examples, so this is the no-example (zero-shot + rules + terms) condition that most RU chapter
text will be in.
Metric: chrF++ (character 1-6-grams + word 1-2-grams, beta 2), document level, plus check.py
errors per chunk and the share of chunks accepted on the first try."""
import argparse, collections, json, os, re, time
from lib import HERE, THESIS, CHAPTERS, read, write, split_parts, blocks, kind, align, ensure_server, load_termbase
from translate import translate_file, load_tm
from build_tm import COUNCIL_HOLDOUT, GD01_SPLIT, keep_council, corpus_blocks

EVAL_KZ = ["3.4", "4.2", "1.3"]
EVAL_RU_PARAS = 4          # first N abstract rubric paragraphs with a Russian counterpart
RES = os.path.join(HERE, "work", "eval", "results.tsv")
GOLD = os.path.join(HERE, "work", "gold")
COUNCIL_WORDS = 700
# (item, source doc, src, tgt): GD_01 both ways, abstracts in every other direction, spread over the 3 held-out docs
COUNCIL_ITEMS = [("gd01-ru-kz", "gd01", "ru", "kz"), ("gd01-kz-ru", "gd01", "kz", "ru"),
                 ("bazarbekov-ru-kz", "bazarbekov", "ru", "kz"), ("toktarova-kz-ru", "toktarova", "kz", "ru"),
                 ("bakirova-en-ru", "bakirova", "en", "ru"), ("bazarbekov-ru-en", "bazarbekov", "ru", "en"),
                 ("bakirova-en-kz", "bakirova", "en", "kz"), ("bakirova-kz-en", "bakirova", "kz", "en")]
# validation: never read by Opus while tuning rules; measures whether the rules generalise beyond COUNCIL_ITEMS
COUNCIL_VALID = [("olzhayev-ru-kz", "olzhayev", "ru", "kz"), ("olzhayev-kz-en", "olzhayev", "kz", "en"),
                 ("mukhanov-en-ru", "mukhanov", "en", "ru"), ("mukhanov-kz-ru", "mukhanov", "kz", "ru")]


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


def council_pair(doc, src, tgt):
    """Held-out aligned paragraphs (source text, human reference) of about COUNCIL_WORDS source words,
    taken from the middle of the document (the start is the rubric boilerplate).
    Once frozen in work/gold/_draft/ (the texts the gold translations were written for), those files are used."""
    item = next(i for i, d, s, t in COUNCIL_ITEMS + COUNCIL_VALID if (d, s, t) == (doc, src, tgt))
    fs, fr = (os.path.join(GOLD, "_draft", f"{item}.{k}.md") for k in (f"src.{src}", f"ref.{tgt}"))
    if os.path.exists(fs) and os.path.exists(fr):
        return read(fs).strip(), read(fr).strip()
    base = os.path.join(HERE, "corpus")
    if doc == "gd01":
        ru, kz = (corpus_blocks(os.path.join(base, "gd01", f"gd01.{l}.md")) for l in ("ru", "kz"))
        links = [(s, t, c) for s, t, c in align(ru, kz) if keep_council(s, t, c)]
        links = links[:int(len(links) * GD01_SPLIT)]
        pairs = [(s, t) if src == "ru" else (t, s) for s, t, _ in links]
    else:
        assert doc in COUNCIL_HOLDOUT
        a, b = (corpus_blocks(os.path.join(base, "abstracts", f"{doc}.{l}.md")) for l in (src, tgt))
        links = [(s, t) for s, t, c in align(a, b) if keep_council(s, t, c)]
        biblio = re.compile(r"\b[A-ZА-ЯӘҒҚҢӨҰҮҺІ]\.\s?[A-ZА-ЯӘҒҚҢӨҰҮҺІ]\.|\b(?:19|20)\d\d\)|doi|ISSN|№\s?\d")
        links = [(s, t) for s, t in links if not biblio.search(s)]      # publication lists are not prose
        words = [len(s.split()) for s, _ in links]
        start = len(links) // 4
        while start > 0 and sum(words[start:]) < COUNCIL_WORDS:
            start -= 1
        pairs = links[start:]
    out, n = [], 0
    for s, t in pairs:
        if n >= COUNCIL_WORDS:
            break
        out.append((s, t))
        n += len(s.split())
    return "\n\n".join(s for s, _ in out), "\n\n".join(t for _, t in out)


def run_council(tag, termbase, tm, log, only=None, items=COUNCIL_ITEMS, sub="council"):
    out = os.path.join(HERE, "work", "eval", tag, sub)
    by_dir = collections.defaultdict(list)
    for item, doc, sl, tl in items:
        if only and only not in item:
            continue
        s, ref = council_pair(doc, sl, tl)
        src = os.path.join(out, "src", f"{item}.{sl}.md")
        write(src, s + "\n")
        write(os.path.join(out, "ref", f"{item}.{tl}.md"), ref + "\n")
        r = translate_file(src, sl, tl, termbase, tm, out, 1, log, genre="council")
        hyp = body_text(r["out"] if os.path.isabs(r["out"]) else os.path.join(THESIS, r["out"]))
        g = os.path.join(GOLD, f"{item}.{tl}.md")
        gold = read(g).strip() if os.path.exists(g) else None
        cg = chrf(hyp, gold) if gold else None
        log(f"  {item}: chrF++ {chrf(hyp, ref):.1f}" + (f", chrF_gold {cg:.1f}" if gold else ""))
        by_dir[f"{sl}>{tl}"].append((r, hyp, ref, gold))
    rows = []
    for d, xs in by_dir.items():
        s = summarise([x[0] for x in xs])
        s["chrf"] = round(chrf("\n".join(x[1] for x in xs), "\n".join(x[2] for x in xs)), 1)
        golds = [x for x in xs if x[3]]
        s["gold"] = round(chrf("\n".join(x[1] for x in golds), "\n".join(x[3] for x in golds)), 1) if golds else ""
        rows.append((sub + " " + d, s))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--set", choices=["thesis", "council", "council-valid"], default="thesis")
    ap.add_argument("--item", help="council set: only items containing this text (e.g. gd01, ru-kz)")
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
    if a.set == "council":
        rows = run_council(a.tag, termbase, tm, log, a.item)
    if a.set == "council-valid":
        rows = run_council(a.tag, termbase, tm, log, a.item, COUNCIL_VALID, "council-valid")
    if a.set == "thesis" and a.only in (None, "kz"):
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

    if a.set == "thesis" and a.only in (None, "ru"):
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
            f.write("tag\tdir\tchrF++\tchunks\tfirst_try\tclean_after_retry\twarnings\tminutes\ttop_errors\tchrF_gold\n")
        for d, s in rows:
            f.write(f"{a.tag}\t{d}\t{s['chrf']}\t{s['chunks']}\t{s['first_try']}\t{s['clean']}\t{s['warnings']}\t"
                    f"{s['minutes']}\t{json.dumps(s['top_errors'], ensure_ascii=False)}\t{s.get('gold', '')}\n")
    for d, s in rows:
        log(f"{a.tag} {d}: chrF++ {s['chrf']}" + (f", chrF_gold {s['gold']}" if s.get("gold") else "") + f", chunks {s['chunks']}, first-try {s['first_try']}, "
            f"clean {s['clean']}, {s['minutes']} min, errors {s['top_errors']}")


if __name__ == "__main__":
    main()
