"""Extract the main body text (no title blocks, headings, running heads, tables, page numbers) of the
council documents into corpus/ as markdown, one paragraph per block.

  python extract_body.py            # all abstracts (16 x ru/kz/en) + GD_01 (ru/kz) -> corpus/
  python extract_body.py doc.docx [out.md]   # one document -> doc.body.md, then translate.py --genre council

Sources (read only): C:/VirtualD/council/Образцы документов/_text/<slug>/abstract_{ru,kz,en}.txt
(pdftotext layout: hard-wrapped lines, a paragraph starts with an indented line) and
C:/VirtualD/council/GD_01_Путеводитель_соискателя_степени_PhD_{русс,каз}.docx (only body paragraphs:
no Heading*/Title styles, nothing inside tables, no header/footer parts)."""
import os, re, zipfile
from lib import HERE, write

COUNCIL = r"C:\VirtualD\council"
TEXT = os.path.join(COUNCIL, "Образцы документов", "_text")
OUT = os.path.join(HERE, "corpus")
GD01 = {"ru": "GD_01_Путеводитель_соискателя_степени_PhD_русс.docx",
        "kz": "GD_01_Путеводитель_соискателя_степени_PhD_каз.docx"}

# Latin look-alikes that PDF fonts put into Kazakh text
KZ_FIX = str.maketrans({"ə": "ә", "Ə": "Ә", "\u04d9": "ә", "\u04d8": "Ә"})
TITLE_MARK = re.compile(r"(АННОТАЦИЯ|АҢДАТПА|ABSTRACT|А\s?Н\s?Н\s?О\s?Т|на соискание|алу үшін ұсынылған|"
                        r"submitted for the degree|for the degree of|диссертациялық жұмысына|диссертационной работы|"
                        r"PhD thesis|dissertation (?:work|research) (?:of|by)|тақырыбындағы|по (?:ОП|образовательной)|"
                        r"білім беру бағдарламасы|educational program|\bEP\b|8D\d{5}|6D\d{6})", re.I)
# the body usually starts with the rubric "relevance of the topic"
BODY_START = re.compile(r"^(Актуальность|Зерттеу(?:дің)? тақырыбының өзектілігі|Тақырыптың өзектілігі|Өзектілігі|"
                        r"Relevance|The relevance|Topicality|Actuality|Общая характеристика|Жұмыстың жалпы|General)", re.I)
# trailing matter that is not running prose (publication lists)
TAIL_START = re.compile(r"^(Список (?:опубликованных|публикаций|работ)|Публикации|Жарияланымдар|Жарияланған|"
                        r"List of (?:publications|published)|Publications)", re.I)


def paragraphs(txt):
    """pdftotext layout -> paragraphs: an indented line (2..14 spaces) starts a new paragraph,
    page numbers and form feeds are dropped, hyphenated line breaks are rejoined."""
    paras, cur = [], []
    for raw in txt.replace("\r", "").replace("\f", "\n").split("\n"):
        line = raw.rstrip()
        s = line.strip()
        if not s or re.fullmatch(r"\d{1,3}", s):
            continue
        indent = len(line) - len(line.lstrip())
        centered = indent >= 15
        if cur and (2 <= indent < 15 or centered or cur[-1][1]):
            paras.append(cur)
            cur = []
        cur.append((s, centered))
    if cur:
        paras.append(cur)
    out = []
    for p in paras:
        t = ""
        for s, _ in p:
            if t.endswith("-") and re.search(r"[а-яёәғқңөұүһіa-z]-$", t) and s[:1].islower():
                t = t[:-1] + s          # soft hyphenation at a line end
            else:
                t = (t + " " + s).strip()
        out.append((re.sub(r"\s+", " ", t), p[0][1]))
    return out


def is_heading(t, centered):
    return (centered and len(t) < 160) or (len(t) < 90 and not re.search(r"[.:;]$", t)) or \
        (t.upper() == t and len(t) < 160)


def abstract_body(path, lang):
    txt = open(path, encoding="utf-8").read()
    if lang == "kz":
        txt = txt.translate(KZ_FIX)
    ps = paragraphs(txt)
    start = next((i for i, (t, c) in enumerate(ps) if BODY_START.match(t) and not c), None)
    if start is None:     # no rubric: skip the leading title block
        start = next((i for i, (t, c) in enumerate(ps) if not c and not TITLE_MARK.search(t) and len(t) > 200), 0)
    body = []
    for t, c in ps[start:]:
        if TAIL_START.match(t) and len(t) < 200:
            break
        if is_heading(t, c):
            continue
        body.append(t)
    return body


def docx_body(path):
    x = zipfile.ZipFile(path).read("word/document.xml").decode("utf-8")
    x = re.sub(r"<w:tbl>.*?</w:tbl>", "", x, flags=re.S)                 # tables: blanks, forms, signatures
    out = []
    for p in re.findall(r"<w:p\b.*?</w:p>", x, flags=re.S):
        st = re.search(r'<w:pStyle w:val="([^"]+)"', p)
        if st and re.match(r"(Heading|Title|Subtitle|TOC|Header|Footer)", st.group(1), re.I):
            continue
        t = re.sub(r"\s+", " ", "".join(re.findall(r"<w:t(?:\s[^>]*)?>([^<]*)</w:t>", p))).strip()
        t = t.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"')
        if len(t) < 40 or is_heading(t, False) and not re.search(r"[.;:]$", t):
            continue
        if "____" in t and len(t) < 100:          # signature lines: position ______ Surname I.O.
            continue
        out.append(t)
    return out


def extract_one(path, out=None):
    """Any single .docx / .txt (pdftotext layout) / .md -> body-only markdown next to it or at out."""
    ext = os.path.splitext(path)[1].lower()
    if ext == ".docx":
        body = docx_body(path)
    else:
        txt = open(path, encoding="utf-8").read()
        body = abstract_body(path, "kz" if len(re.findall("[әғқңөұүһі]", txt)) > 20 else "ru")
    from lib import detect_lang
    if detect_lang("\n".join(body)) == "kz":
        body = [b.translate(KZ_FIX) for b in body]
    out = out or os.path.splitext(path)[0] + ".body.md"
    write(out, "\n\n".join(body) + "\n")
    print(f"{path} -> {out}: {len(body)} paragraphs, {sum(len(b.split()) for b in body)} words")
    return out


def main():
    import sys
    if len(sys.argv) > 1:          # python extract_body.py file.docx [out.md]
        extract_one(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
        return
    os.makedirs(OUT, exist_ok=True)
    for slug in sorted(os.listdir(TEXT)):
        for lang in ("ru", "kz", "en"):
            p = os.path.join(TEXT, slug, f"abstract_{lang}.txt")
            if os.path.exists(p):
                body = abstract_body(p, lang)
                write(os.path.join(OUT, "abstracts", f"{slug}.{lang}.md"), "\n\n".join(body) + "\n")
                print(f"{slug:14} {lang}: {len(body):3} paragraphs, {sum(len(b.split()) for b in body):5} words")
    for lang, f in GD01.items():
        body = docx_body(os.path.join(COUNCIL, f))
        if lang == "kz":
            body = [b.translate(KZ_FIX) for b in body]
        write(os.path.join(OUT, "gd01", f"gd01.{lang}.md"), "\n\n".join(body) + "\n")
        print(f"gd01           {lang}: {len(body):3} paragraphs, {sum(len(b.split()) for b in body):5} words")


if __name__ == "__main__":
    main()
