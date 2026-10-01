"""Translate dissertation sections between English, Russian and Kazakh with the local Qwen.

  python translate.py --tgt ru chapters/04-system/drafts/4.4-draft.md
  python translate.py --tgt ru "chapters/*/drafts/*-draft.md"            # whole volume, resumable
  python translate.py --src kz --tgt ru chapters/03-experiments/translations/3.4-translation.md
  python translate.py --tgt en --out C:/tmp/x some_russian_text.md        # any markdown file

Per chunk (~450 words, tables and code never split) the prompt carries: the fixed rules
(common + target language), the termbase rows that occur in the chunk, the two most similar
translation-memory examples, the English original when translating between RU and KZ (pivot),
and the tail of the previous translated chunk. Every chunk goes through check.py; on errors it is
re-translated once with the error list, and the better version is kept.

Output for a chapter file: chapters/<ch>/translations-<tgt>/<id>-<tgt>.md (the Kazakh edition keeps
its own translations/ folder and is never overwritten). Chunk cache: <out>.parts/ -> reruns resume.
Report: <out>.report.json and a summary line; chunks that still fail are listed as NEEDS_REVIEW."""
import argparse, glob, hashlib, json, os, re, sys, time
from lib import (HERE, THESIS, CHAPTERS, LANG_NAME, read, write, split_parts, blocks, kind, translatable,
                 detect_lang, align, load_termbase, term_hits, ensure_server, chat)
from check import check

PART1 = {"en": "## PART 1: SECTION TEXT", "kz": "## 1-БӨЛІК: БӨЛІМ МӘТІНІ", "ru": "## ЧАСТЬ 1: ТЕКСТ РАЗДЕЛА"}
NOTE = {"en": "> English translation by the local model (Qwen). Source: `{src}`. Terminology: `translation/termbase.tsv`.",
        "kz": "> Жергілікті модель (Qwen) жасаған қазақша аударма. Бастапқы мәтін: `{src}`. Терминология: `translation/termbase.tsv`.",
        "ru": "> Перевод на русский язык выполнен локальной моделью (Qwen). Исходный текст: `{src}`. Терминология: `translation/termbase.tsv`."}
MAX_WORDS = 450
WORD = re.compile(r"[\wӘәҒғҚқҢңӨөҰұҮүҺһІі]+")


# ---------- context pieces ----------
GENRES = ("thesis", "council")


def rules(tgt, genre="thesis"):
    """common + target language + genre rules. rules/genre-<genre>.md (optional) begins with a role paragraph
    that replaces the dissertation role of common.md; the rest of it goes last and overrides earlier rules."""
    common, lang = read(os.path.join(HERE, "rules", "common.md")), read(os.path.join(HERE, "rules", f"{tgt}.md"))
    g = os.path.join(HERE, "rules", f"genre-{genre}.md")
    if not os.path.exists(g):
        return common + "\n" + lang
    role, rest = read(g).split("\n\n", 1)
    return "\n".join([role + "\n\n" + common.split("\n\n", 1)[1], lang, rest])


def load_postfix(tgt):
    """rules/postfix-<tgt>.tsv: regex -> replacement, applied to every output (unambiguous lexical errors only)."""
    p = os.path.join(HERE, "rules", f"postfix-{tgt}.tsv")
    rows = [l.split("\t") for l in read(p).split("\n") if l.strip() and not l.startswith("#")] if os.path.exists(p) else []
    return [(re.compile(a), b) for a, b in rows]


def postfix(txt, fixes):
    for rx, rep in fixes:
        txt = rx.sub(rep, txt)
    return txt


def load_tm():
    p = os.path.join(HERE, "tm", "tm.jsonl")
    return [json.loads(l) for l in read(p).split("\n") if l.strip()] if os.path.exists(p) else []


def examples(chunk, tm, src, tgt, k=2, exclude=None, genre="thesis"):
    """k TM rows with both languages, most similar to the chunk by shared content words;
    rows of the same genre (row["domain"], default thesis) are preferred."""
    words = {w.lower() for w in WORD.findall(chunk) if len(w) > 3}
    scored = []
    for r in tm:
        if src not in r or tgt not in r or (exclude and r["src"] == exclude) or len(r[src]) > 1400:
            continue
        rw = {w.lower() for w in WORD.findall(r[src]) if len(w) > 3}
        if rw:
            same = r.get("domain", "thesis") == genre
            scored.append((len(words & rw) / (len(rw) ** 0.5) + (1.0 if same else 0), r))
    scored.sort(key=lambda x: -x[0])
    return [r for _, r in scored[:k]]


def terms_block(chunk, termbase, src, tgt):
    lines = []
    for r in term_hits(chunk, termbase, src):
        a, b = r[src].split(";")[0].strip(), r[tgt].strip()
        if not b or b == "?":
            continue
        extra = " (keep in Latin)" if r["rule"] == "keep" else ""
        if r["rule"] == "bilingual-first" and tgt == "kz":
            extra = f" (first use in a section: {r['note'].split('first use: ')[-1].split(';')[0]})"
        lines.append(f"- {a} = {b}{extra}")
    return "\n".join(dict.fromkeys(lines))


def build_prompt(chunk, src, tgt, termbase, tm, prev, pivot, exclude, fix=None, genre="thesis"):
    parts = []
    t = terms_block(chunk + "\n" + (pivot or ""), termbase, src, tgt)
    if pivot and src != "en":
        t = "\n".join(filter(None, [t, terms_block(pivot, termbase, "en", tgt)]))
    if t:
        parts.append(f"TERMINOLOGY ({LANG_NAME[src]} = {LANG_NAME[tgt]}), use exactly:\n{t}")
    ex = examples(chunk, tm, src, tgt, exclude=exclude, genre=genre)
    if ex:
        what = "from this dissertation" if genre == "thesis" else "of similar documents"
        parts.append(f"EXAMPLES of approved translations {what} (style and terminology):\n" +
                     "\n\n".join(f"[{LANG_NAME[src]}]\n{r[src]}\n[{LANG_NAME[tgt]}]\n{r[tgt]}" for r in ex))
    if pivot and src != "en":
        parts.append("ENGLISH ORIGINAL of the source chunk (authoritative for meaning; translate the SOURCE, "
                     f"use this to resolve ambiguity):\n<<<\n{pivot}\n>>>")
    if prev:
        parts.append(f"PREVIOUS TRANSLATED TEXT (context only, do not repeat it):\n{prev}")
    if fix:
        parts.append("A previous attempt had these problems - avoid them:\n" + "\n".join(f"- {e}" for e in fix))
    parts.append(f"SOURCE ({LANG_NAME[src]}) - translate into {LANG_NAME[tgt]}:\n<<<\n{chunk}\n>>>")
    return "\n\n".join(parts)


# ---------- chunking ----------
def segments(body):
    """-> list of (is_translatable, text); consecutive translatable blocks grouped up to MAX_WORDS."""
    segs, cur, n = [], [], 0
    for b in blocks(body):
        m = re.match(r"(<!--.*?-->)\n(\S.*)", b, re.S)
        if m and kind(b) == "marker":          # <!-- center --> directly above a title block: the text is its own chunk
            if cur:
                segs.append((True, "\n\n".join(cur)))
                cur, n = [], 0
            segs += [(False, m.group(1)), (True, m.group(2))]
            continue
        if not translatable(b):
            if cur:
                segs.append((True, "\n\n".join(cur)))
                cur, n = [], 0
            segs.append((False, b))
            continue
        w = len(WORD.findall(b))
        if cur and n + w > MAX_WORDS and kind(b) != "heading" or cur and kind(b) == "heading" and n > MAX_WORDS * 0.6:
            segs.append((True, "\n\n".join(cur)))
            cur, n = [], 0
        cur.append(b)
        n += w
    if cur:
        segs.append((True, "\n\n".join(cur)))
    return segs


def pivot_for(chunks, en_body):
    """English text aligned to each source chunk (for RU<->KZ), by aligning chunk blocks to EN blocks."""
    en_b = [b for b in blocks(en_body) if translatable(b)]
    src_b, owner = [], []
    for i, c in enumerate(chunks):
        for b in blocks(c):
            src_b.append(b)
            owner.append(i)
    links = align(src_b, en_b)
    res = [[] for _ in chunks]
    pos = 0
    for s, t, _ in links:
        first = s.split("\n\n")[0]
        while pos < len(src_b) and src_b[pos] != first:
            pos += 1
        if pos < len(src_b):
            res[owner[pos]].append(t)
    return ["\n\n".join(r) or None for r in res]


# ---------- paths ----------
def chapter_ids(path):
    p = os.path.abspath(path).replace("\\", "/")
    m = re.search(r"/chapters/([^/]+)/(drafts|translations|translations-\w\w)/(.+?)-(draft|translation|en|ru|kz)\.md$", p)
    return (m.group(1), m.group(3)) if m else (None, None)


def english_original(path):
    ch, sid = chapter_ids(path)
    p = os.path.join(CHAPTERS, ch, "drafts", f"{sid}-draft.md") if ch else None
    return p if p and os.path.exists(p) else None


def out_path(path, tgt, out_dir):
    ch, sid = chapter_ids(path)
    if out_dir:
        base = f"{sid}-{tgt}.md" if sid else re.sub(r"\.md$", "", os.path.basename(path)) + f".{tgt}.md"
        return os.path.join(out_dir, base)
    if ch:
        return os.path.join(CHAPTERS, ch, f"translations-{tgt}", f"{sid}-{tgt}.md")
    return re.sub(r"\.md$", "", path) + f".{tgt}.md"


# ---------- main loop ----------
def translate_file(path, src, tgt, termbase, tm, out_dir, retries, log, exclude=None, genre=None):
    text = read(path)
    head, body, _tail = split_parts(text)
    src = src or detect_lang(body)
    if src == tgt:
        log(f"skip {path}: already {tgt}")
        return None
    out = out_path(path, tgt, out_dir)
    cache = out + ".parts"
    os.makedirs(cache, exist_ok=True)
    segs = segments(body)
    chunks = [t for ok, t in segs if ok]
    en_p = english_original(path) if src != "en" and tgt != "en" else None
    pivots = pivot_for(chunks, split_parts(read(en_p))[1]) if en_p else [None] * len(chunks)
    ch, sid = chapter_ids(path)
    genre = genre or ("thesis" if ch else "council")
    exclude = exclude or (f"chapters/{sid}" if sid else None)   # never show a chunk its own reference translation
    sysmsg = rules(tgt, genre)
    fixes = load_postfix(tgt)
    termbase = [r for r in termbase if r.get("domain", "all") in ("all", genre)]
    res, report, prev, ci = [], [], "", 0
    t_file = time.time()
    for ok, seg in segs:
        if not ok:
            res.append(seg)
            continue
        key = hashlib.sha1(f"{src}>{tgt}\n{seg}".encode()).hexdigest()[:16]
        cp = os.path.join(cache, key + ".json")
        if os.path.exists(cp):
            r = json.loads(read(cp))
        else:
            best = None
            for attempt in range(retries + 1):
                fix = best["errors"] if best else None
                user = build_prompt(seg, src, tgt, termbase, tm, prev, pivots[ci], exclude, fix, genre)
                words = len(WORD.findall(seg))
                txt, info = chat(sysmsg, user, max_tokens=min(8000, 400 + words * 6), temperature=0.3 if not fix else 0.2)
                txt = txt.strip().replace(" — ", " – ")   # the volume gate forbids the long dash
                txt = postfix(txt, fixes)
                errs, warns = check(seg, txt, src, tgt, termbase, genre)
                if info["finish"] == "length":
                    errs.insert(0, "output truncated")
                cand = dict(out=txt, errors=errs, warnings=warns, attempts=attempt + 1, info=info)
                if best is None or len(errs) < len(best["errors"]):
                    best = cand
                log(f"  chunk {ci + 1}/{len(chunks)} try {attempt + 1}: {words} w, {info['sec']}s, "
                    f"pp {info['pp_tps']}/s tg {info['tg_tps']}/s, {len(errs)} err, {len(warns)} warn"
                    + (f" | {errs[0][:90]}" if errs else ""))
                if info["pp_tps"] and info["pp_tps"] < 100 and info["p_tok"] and info["p_tok"] > 2000:
                    log("  WARN: prompt speed < 100 t/s - another app holds VRAM; close browsers/games")
                if not errs:
                    break
            r = best
            write(cp, json.dumps(r, ensure_ascii=False, indent=1))
        res.append(r["out"])
        report.append(dict(chunk=ci + 1, words=len(WORD.findall(seg)), errors=r["errors"], warnings=r["warnings"],
                           attempts=r["attempts"], sec=r["info"]["sec"], src_head=seg[:80]))
        prev = r["out"][-700:]
        ci += 1
    rel = os.path.relpath(path, THESIS).replace("\\", "/")
    doc = NOTE[tgt].format(src=rel) + "\n\n" + PART1[tgt] + "\n\n" + "\n\n".join(res).strip() + "\n"
    write(out, doc)
    bad = [c for c in report if c["errors"]]
    summ = dict(file=rel, genre=genre, out=os.path.relpath(out, THESIS).replace("\\", "/"), src=src, tgt=tgt, chunks=len(report),
                clean_first_try=sum(1 for c in report if not c["errors"] and c["attempts"] == 1),
                needs_review=[c["chunk"] for c in bad], warnings=sum(len(c["warnings"]) for c in report),
                minutes=round((time.time() - t_file) / 60, 1), detail=report)
    write(out + ".report.json", json.dumps(summ, ensure_ascii=False, indent=1))
    log(f"{rel} -> {summ['out']}: {len(report)} chunks, {summ['clean_first_try']} clean first try, "
        f"NEEDS_REVIEW {summ['needs_review'] or 'none'}, {summ['warnings']} warnings, {summ['minutes']} min")
    return summ


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="+", help="files or globs (relative to thesis/ or absolute)")
    ap.add_argument("--src", choices=["en", "ru", "kz"], help="source language (default: detected)")
    ap.add_argument("--tgt", required=True, choices=["en", "ru", "kz"])
    ap.add_argument("--out", help="output directory (default: chapters/<ch>/translations-<tgt>/)")
    ap.add_argument("--retries", type=int, default=1)
    ap.add_argument("--no-tm", action="store_true", help="no translation-memory examples (for ablation)")
    ap.add_argument("--exclude", help="TM source never shown as an example (e.g. output/abstract when translating "
                    "the abstract, so Qwen does not copy the approved reference)")
    ap.add_argument("--genre", choices=GENRES, help="thesis (chapter files) or council (official documents, "
                    "abstracts, regulations); default: thesis for chapter files, council otherwise")
    a = ap.parse_args()
    files = []
    for p in a.inputs:
        if not os.path.isabs(p) and not glob.glob(p):
            p = os.path.join(THESIS, p)       # thesis-relative paths work from any directory
        files += sorted(glob.glob(p)) or [p]
    files = [f for f in files if os.path.isfile(f)]
    if not files:
        sys.exit("no input files")
    if not ensure_server():
        sys.exit("Qwen server did not start (C:\\AI\\start-qwen.ps1)")
    termbase, tm = load_termbase(), [] if a.no_tm else load_tm()

    def log(m):
        print(time.strftime("%H:%M:%S"), m, flush=True)

    log(f"{len(files)} file(s) -> {LANG_NAME[a.tgt]}; termbase {len(termbase)} rows, TM {len(tm)} rows")
    allr = [translate_file(f, a.src, a.tgt, termbase, tm, a.out, a.retries, log, exclude=a.exclude, genre=a.genre) for f in files]
    allr = [r for r in allr if r]
    n = sum(r["chunks"] for r in allr)
    log(f"DONE {len(allr)} files, {n} chunks, {sum(r['clean_first_try'] for r in allr)} clean first try, "
        f"{sum(len(r['needs_review']) for r in allr)} need review, {sum(r['minutes'] for r in allr):.0f} min")


if __name__ == "__main__":
    main()
