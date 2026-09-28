"""Shared helpers for the EN/RU/KZ translation kit: section extraction, block splitting,
paragraph alignment, language detection, term lookup, Qwen API access."""
import json, os, re, subprocess, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
THESIS = os.path.dirname(HERE)
CHAPTERS = os.path.join(THESIS, "chapters")
BASE = "http://127.0.0.1:8080"
LANGS = ("en", "ru", "kz")
LANG_NAME = {"en": "English", "ru": "Russian", "kz": "Kazakh"}

for s in (sys.stdout, sys.stderr):
    s.reconfigure(encoding="utf-8")

PART1_RE = re.compile(r"^## (PART 1\b|1-БӨЛІК\b|ЧАСТЬ 1\b)")
NOTE_RE = re.compile(r"^#{2,4} (Аудармашы ескертуі|Translator'?s note|Примечание переводчика)", re.I)
PARTN_RE = re.compile(r"^## (PART [2-9]\b|[2-9]-БӨЛІК\b|ЧАСТЬ [2-9]\b)")


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read().replace("\r\n", "\n")


def write(path, text):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def split_parts(text):
    """-> (head, body, tail). body = the PART 1 section text; head/tail are kept verbatim.
    A file without a PART 1 marker is all body."""
    lines = text.split("\n")
    start = next((i for i, l in enumerate(lines) if PART1_RE.match(l)), None)
    if start is None:
        return "", text, ""
    end = next((i for i in range(start + 1, len(lines)) if PARTN_RE.match(lines[i])
                or NOTE_RE.match(lines[i])), len(lines))
    while end > start + 1 and re.fullmatch(r"\s*(-{3,})?\s*", lines[end - 1]):
        end -= 1
    return "\n".join(lines[:start + 1]), "\n".join(lines[start + 1:end]), "\n".join(lines[end:])


def blocks(body):
    """Split markdown into blocks on blank lines; tables and fenced code stay whole."""
    out, cur, fence = [], [], False
    for line in body.split("\n"):
        if line.strip().startswith("```"):
            fence = not fence
            cur.append(line)
            continue
        if not fence and not line.strip():
            if cur:
                out.append("\n".join(cur))
                cur = []
            continue
        cur.append(line)
    if cur:
        out.append("\n".join(cur))
    return out


def kind(block):
    s = block.lstrip()
    if s.startswith("```"):
        return "code"
    if s.startswith("#"):
        return "heading"
    if s.startswith("|"):
        return "table"
    if re.fullmatch(r"-{3,}|\*{3,}", s.strip()):
        return "hr"
    if s.startswith("<!--") or re.fullmatch(r"\[?FIG-[\w.\-]+\]?.*", s.strip()) and len(s) < 80:
        return "marker"
    return "text"


def translatable(block):
    return kind(block) in ("heading", "table", "text")


# ---------- language detection / numbers ----------
KZ_LETTERS = set("әғқңөұүһіӘҒҚҢӨҰҮҺІ")
CYR = re.compile(r"[А-Яа-яЁёӘәҒғҚқҢңӨөҰұҮүҺһІі]")
LAT = re.compile(r"[A-Za-z]")


def detect_lang(text):
    cyr, lat = len(CYR.findall(text)), len(LAT.findall(text))
    if lat > cyr:
        return "en"
    kz = sum(ch in KZ_LETTERS for ch in text)
    return "kz" if kz > 0.01 * max(cyr, 1) else "ru"


NUM_RE = re.compile(r"\d+(?:[.,]\d+)*")
# decimal and thousands separators per language: EN 35,126 / 0.75; RU 35 126 / 0,75; KZ 35 126 / 0.75
DEC = {"en": ".", "ru": ",", "kz": "."}


def numbers(text, lang):
    """Multiset of numbers as canonical strings, independent of the language's separators.
    Digits glued to letters (EfficientNet-B3, H-1, 8D06102) count too - they must survive as well."""
    t = re.sub(r"(?<=\d)[\u00a0\u202f\u2009 ](?=\d{3}(?!\d))", "", text)
    out = []
    for n in NUM_RE.findall(t):
        if lang == "en":
            n = re.sub(r",(?=\d{3}(?!\d))", "", n)
        elif DEC[lang] == ",":
            n = n.replace(",", ".") if n.count(",") == 1 else n
        n = n.rstrip(".,")
        out.append(n)
    return sorted(out)


# ---------- alignment ----------
def _sig(block):
    return set(numbers(block, detect_lang(block))) |set(re.findall(r"\b[A-Z][A-Za-z0-9\-]{2,}\b", block))


def align(src_blocks, tgt_blocks):
    """Monotone DP alignment (1-1, 1-2, 2-1, 1-0, 0-1) on length ratio + shared numbers/Latin names.
    Returns list of (src_text, tgt_text, score) for the 1-1/1-2/2-1 links."""
    ls = [len(b) for b in src_blocks]
    lt = [len(b) for b in tgt_blocks]
    ratio = (sum(lt) or 1) / (sum(ls) or 1)
    n, m = len(src_blocks), len(tgt_blocks)
    INF = float("inf")
    D = [[INF] * (m + 1) for _ in range(n + 1)]
    P = [[None] * (m + 1) for _ in range(n + 1)]
    D[0][0] = 0

    def cost(si, sj, ti, tj):
        a = sum(ls[si:sj]) * ratio
        b = sum(lt[ti:tj])
        c = abs(a - b) / max(a, b, 1) * 3
        sa = set().union(*[_sig(x) for x in src_blocks[si:sj]])
        sb = set().union(*[_sig(x) for x in tgt_blocks[ti:tj]])
        if sa or sb:
            c += 2 * (1 - len(sa & sb) / max(len(sa | sb), 1))
        ka = {kind(x) for x in src_blocks[si:sj]}
        kb = {kind(x) for x in tgt_blocks[ti:tj]}
        if ka != kb:
            c += 3
        return c + (0.6 if (sj - si) + (tj - ti) > 2 else 0)

    moves = [(1, 1), (1, 2), (2, 1), (1, 0), (0, 1)]
    for i in range(n + 1):
        for j in range(m + 1):
            if D[i][j] == INF:
                continue
            for di, dj in moves:
                a, b = i + di, j + dj
                if a > n or b > m:
                    continue
                c = 4.5 if 0 in (di, dj) else cost(i, a, j, b)
                if D[i][j] + c < D[a][b]:
                    D[a][b] = D[i][j] + c
                    P[a][b] = (i, j)
    out, i, j = [], n, m
    while (i, j) != (0, 0):
        pi, pj = P[i][j]
        if i > pi and j > pj:
            s, t = "\n\n".join(src_blocks[pi:i]), "\n\n".join(tgt_blocks[pj:j])
            out.append((s, t, cost(pi, i, pj, j)))
        i, j = pi, pj
    return out[::-1]


# ---------- sources ----------
def section_pairs():
    """[(section_id, en_path, kz_path)] for every draft with a Kazakh translation."""
    res = []
    for ch in sorted(os.listdir(CHAPTERS)):
        d = os.path.join(CHAPTERS, ch, "drafts")
        if ch.startswith("_") or not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            if f.endswith("-draft.md"):
                sid = f[:-len("-draft.md")]
                kz = os.path.join(CHAPTERS, ch, "translations", sid + "-translation.md")
                res.append((sid, os.path.join(d, f), kz if os.path.exists(kz) else None))
    return res


# ---------- termbase ----------
def load_termbase():
    rows = []
    path = os.path.join(HERE, "termbase.tsv")
    if not os.path.exists(path):
        return rows
    for line in read(path).split("\n")[1:]:
        if line.strip() and not line.startswith("#"):
            c = (line.split("\t") + [""] * 5)[:5]
            rows.append(dict(en=c[0], ru=c[1], kz=c[2], rule=c[3], note=c[4]))
    return rows


def _stem(word, lang):
    w = word.lower()
    if lang == "en":
        return re.sub(r"(ies|es|s|ing|ed)$", "", w) if len(w) > 4 else w
    return w[:max(4, int(len(w) * 0.7))] if len(w) > 5 else w


def term_hits(text, termbase, lang):
    """Rows whose `lang` form occurs in text (prefix match per word, so inflected forms hit)."""
    low = text.lower()
    hits = []
    for r in termbase:
        form = r.get(lang, "").split(";")[0].strip()
        if not form or form == "?":
            continue
        words = re.findall(r"[\wӘәҒғҚқҢңӨөҰұҮүҺһІі\-]+", form)
        if not words:
            continue
        if len(form) <= 5 or re.fullmatch(r"[A-Z0-9\-]+", form):     # abbreviations: whole word, exact case
            if re.search(r"(?<![\w\-])" + re.escape(form) + (r"(?:s|es)?" if form.islower() else "") + r"(?![\w])", text):
                hits.append(r)
            continue
        pat = r"\b" + r"\W+".join(re.escape(_stem(w, lang)) + r"[\wӘәҒғҚқҢңӨөҰұҮүҺһІі\-]*" for w in words)
        if re.search(pat, low):
            hits.append(r)
    return hits


# ---------- Qwen ----------
def http(path, body=None, timeout=10):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(BASE + path, data, {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def ensure_server():
    try:
        if http("/health", timeout=3).get("status") == "ok":
            return True
    except Exception:
        pass
    running = "llama-server" in subprocess.run(["tasklist", "/FI", "IMAGENAME eq llama-server.exe"],
                                               capture_output=True, text=True).stdout
    if not running:
        subprocess.Popen(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command",
                          r"& C:\AI\start-qwen.ps1 *> C:\AI\server.log"],
                         creationflags=subprocess.CREATE_NO_WINDOW)
    for _ in range(120):
        try:
            if http("/health", timeout=3).get("status") == "ok":
                return True
        except Exception:
            pass
        time.sleep(2)
    return False


def chat(system, user, max_tokens=3000, temperature=0.3, schema=None, think=False):
    """One completion (non-thinking by default). Returns (text, info)."""
    body = {"model": "qwen", "messages": [{"role": "system", "content": system},
                                          {"role": "user", "content": user}],
            "max_tokens": max_tokens, "temperature": temperature, "top_p": 0.8, "top_k": 20, "min_p": 0,
            "chat_template_kwargs": {"enable_thinking": think}, "cache_prompt": True}
    if think:
        body.update(temperature=1.0, top_p=0.95)
    if schema:
        body["response_format"] = {"type": "json_schema", "json_schema": {"name": "result", "schema": schema}}
    t0 = time.time()
    r = http("/v1/chat/completions", body, timeout=3600)
    ch = r["choices"][0]
    text = ch["message"].get("content") or ""
    text = re.sub(r"^\s*<think>.*?</think>\s*", "", text, flags=re.S)
    tm = r.get("timings", {})
    info = dict(sec=round(time.time() - t0, 1), finish=ch.get("finish_reason"),
                p_tok=r.get("usage", {}).get("prompt_tokens"), c_tok=r.get("usage", {}).get("completion_tokens"),
                pp_tps=round(tm.get("prompt_per_second", 0)), tg_tps=round(tm.get("predicted_per_second", 0), 1))
    return text, info
