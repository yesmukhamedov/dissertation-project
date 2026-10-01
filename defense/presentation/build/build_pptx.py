# -*- coding: utf-8 -*-
"""Сборка презентации защиты (kk / ru / en) из slides/NN-*/{kk,ru,en}.md.

Запуск (из любой папки):
    python build/build_pptx.py              # три языка, pptx + pdf (если есть PowerPoint)
    python build/build_pptx.py ru --no-pdf  # один язык, без pdf
    python build/build_pptx.py --png DIR    # + png каждого слайда из pdf (для проверки глазами)

Источники (только чтение): PLAN.md (порядок), slides/*/<lang>.md («## На слайде», «## Речь»),
slides/*/img/*, report/captions_<lang>.md (подписи и плашки), архивная презентация (шаблон, титул).
Результат: build/presentation_<lang>.pptx (+ .pdf). Руками не править — перезапускать скрипт.
"""
import copy
import re
import sys
from pathlib import Path

from lxml import etree
from PIL import Image, ImageFont
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent                                   # presentation/
SLIDES = ROOT / "slides"
REPORT = ROOT / "report"
ARCHIVE = ROOT.parent / "_archive" / "presentation_2026-09-26" / "presentation.pptx"
LANGS = ["kk", "ru", "en"]

# ---------------------------------------------------------------- оформление
FONT = "Times New Roman"          # §9 п. 6: одна гарнитура, как в диссертации
NAVY = RGBColor(0x0E, 0x28, 0x41)  # цвет шапки архивной презентации
RED = RGBColor(0x9B, 0x1B, 0x30)   # красный МУИТ (логотип) — плашка задачи
TEXT = RGBColor(0x1A, 0x1A, 0x1A)
GREY = RGBColor(0x40, 0x40, 0x40)
TINT = RGBColor(0xE8, 0xEE, 0xF5)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

SW, SH = 13.333, 7.5
HEAD_H = 1.10                      # высота шапки
X0, X1 = 0.45, 12.88               # поля контента
Y0, Y1 = 1.30, 6.72                # верх/низ контента (ниже — строка апробации и номер)
TITLE_PT = 28                      # §9 п. 7: заголовок 28–32
BODY_MAX, BODY_MIN = 20, 16        # текст ≥ 18, минимум 16
CAP_PT = 14                        # подписи ≥ 12
TABLE_MAX, TABLE_MIN = 16, 12
APPROB_PT = 14                     # строка публикации ≥ 11–12
LINE = 1.17                        # межстрочный множитель TNR в PowerPoint (одинарный)

FIG_WORDS = ("Сурет", "Рисунок", "Figure")
TAB_WORDS = ("Кесте", "Таблица", "Table")

REPORT_LOG = []                    # что пришлось ужать / чего не хватило


def log(msg):
    REPORT_LOG.append(msg)


# ---------------------------------------------------------------- измерение текста
_FONT_FILES = {(False, False): "times.ttf", (True, False): "timesbd.ttf",
               (False, True): "timesi.ttf", (True, True): "timesbi.ttf"}
_font_cache = {}


def _font(b, i):
    key = (bool(b), bool(i))
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype("C:/Windows/Fonts/" + _FONT_FILES[key], 100)
    return _font_cache[key]


def text_w(s, pt, b=False, i=False):
    """Ширина строки в дюймах."""
    return _font(b, i).getlength(s) / 100.0 * pt / 72.0


def wrap_lines(runs, pt, width):
    """Число строк абзаца (runs: [(text,b,i)]) при ширине width дюймов."""
    tokens = []
    for t, b, i in runs:
        for part in re.split(r"( +)", t):
            if part:
                tokens.append((part, b, i))
    lines, cur = 1, 0.0
    for part, b, i in tokens:
        w = text_w(part, pt, b, i)
        if part.isspace():
            cur += w
            continue
        if cur + w > width and cur > 0:
            lines += 1
            cur = w
        else:
            cur += w
        while cur > width:          # слово шире строки — перенос внутри слова
            lines += 1
            cur -= width
    return lines


def para_h(p, pt, width):
    ind = p.get("indent", 0.0)
    n = wrap_lines(p["runs"], p.get("pt", pt), width - ind)
    size = p.get("pt", pt)
    return n * size * LINE / 72.0 + p.get("after", 0.0) * size / 72.0


def paras_h(paras, pt, width):
    return sum(para_h(p, pt, width) for p in paras)


def fit_pt(paras, width, height, hi=BODY_MAX, lo=BODY_MIN, where=""):
    width -= 0.12          # внутренние поля рамки + запас
    for pt in range(hi, lo - 1, -1):
        if paras_h(paras, pt, width) * 1.04 <= height:
            return pt
    log(f"{where}: текст не влез даже при {lo} pt (нужно {paras_h(paras, lo, width):.2f}″ при {height:.2f}″)")
    return lo


# ---------------------------------------------------------------- markdown
def inline_runs(s, b=False, i=False):
    """**жирный**, *курсив* → [(text,b,i)]."""
    out = []
    for tok in re.split(r"(\*\*.+?\*\*|(?<!\*)\*[^*\s][^*]*?\*(?!\*))", s):
        if not tok:
            continue
        if tok.startswith("**") and tok.endswith("**") and len(tok) > 4:
            out += inline_runs(tok[2:-2], True, i)
        elif tok.startswith("*") and tok.endswith("*") and len(tok) > 2:
            out += inline_runs(tok[1:-1], b, True)
        else:
            out.append((nbsp(tok.replace("`", "")), b, i))
    return out


def nbsp(s):
    """Неразрывные пробелы: «p = 0,3», «10 %», «≈ 340», «103 млн» не разрываются строкой."""
    NB = "\u00a0"
    s = re.sub(r"(?<=[\w)\]|′’]) ([=≈≥≤<>×→]) (?=\S)", NB + r"\1" + NB, s)
    s = re.sub(r"(\d) (%|п\.п\.|pp|млн|мың|тыс\.|млрд|million|thousand|МиБ|ГБ|GB|MiB)", r"\1" + NB + r"\2", s)
    s = re.sub(r"(^|\s)([≈≥≤~±]) (?=\d)", r"\1\2" + NB, s)
    s = re.sub(r"(№) (?=\d)", r"\1" + NB, s)
    s = re.sub(r"(\d) (?=\d{3}\b)", r"\1" + NB, s)          # 35 126, 1 500
    return s


def plain(s):
    return "".join(t for t, _, _ in inline_runs(s))


def read_md(folder, lang):
    txt = (SLIDES / folder / f"{lang}.md").read_text(encoding="utf-8")
    txt = re.sub(r"^---\n.*?\n---\n", "", txt, flags=re.S)
    title = re.search(r"^# (.+)$", txt, re.M).group(1).strip()
    secs = {}
    for m in re.finditer(r"^## (.+?)\n(.*?)(?=^## |\Z)", txt, re.M | re.S):
        secs[m.group(1).strip()] = m.group(2).strip()
    return title, secs.get("На слайде", ""), secs.get("Речь", "")


APPROB_RE = re.compile(r"^\*\*(Внизу|Төменде|Bottom) \((курсив|italic)\):\*\*\s*(.*)$")
NOTE_RE = re.compile(r"^(Без рисунка|Суретсіз|No figure|Повтор|Титул слайды|Repeat of|Текст слайда|Slide text)")


def parse_blocks(body):
    """→ список блоков: ('table',rows) ('bullets',[..]) ('num',[..]) ('fig',groups) ('approb',s)
    ('source',s) ('para',s)."""
    blocks = []
    lines = body.split("\n")
    i = 0
    while i < len(lines):
        ln = lines[i].rstrip()
        if not ln.strip():
            i += 1
            continue
        if ln.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-+:?", c) for c in cells if c):
                    rows.append(cells)
                i += 1
            blocks.append(("table", rows))
            continue
        if ln.startswith("- "):
            items = []
            while i < len(lines) and lines[i].startswith("- "):
                items.append(lines[i][2:].strip())
                i += 1
            blocks.append(("bullets", items))
            continue
        if re.match(r"^\d+\. ", ln):
            items = []
            while i < len(lines) and re.match(r"^\d+\. ", lines[i]):
                items.append(re.sub(r"^\d+\. ", "", lines[i]).strip())
                i += 1
            blocks.append(("num", items))
            continue
        para = [ln.strip()]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"^(\||- |\d+\. )", lines[i]):
            para.append(lines[i].strip())
            i += 1
        s = " ".join(para)
        m = APPROB_RE.match(s)
        if m:
            blocks.append(("approb", m.group(3).strip().strip("*").strip()))
        elif "`img/" in s:
            groups = []
            for seg in s.split(";"):
                imgs = re.findall(r"`img/([^`]+)`", seg)
                if imgs:
                    groups.append(imgs)
            blocks.append(("fig", groups))
        elif NOTE_RE.match(s):
            pass
        elif s.startswith("*") and s.endswith("*") and not s.startswith("**"):
            blocks.append(("source", s.strip("*")))
        else:
            blocks.append(("para", s))
    return blocks


def read_plan():
    order = []
    for m in re.finditer(r"^\| (\d\d|R\d) \| `([^`]+)` \|", (ROOT / "PLAN.md").read_text(encoding="utf-8"), re.M):
        order.append((m.group(1), m.group(2)))
    return order


def read_captions(lang):
    res = {}
    for m in re.finditer(r"^\| (\d\d|R\d) \| ([^|]+) \| (.+) \|$",
                         (REPORT / f"captions_{lang}.md").read_text(encoding="utf-8"), re.M):
        badge = m.group(2).strip()
        caps = [c.strip() for c in m.group(3).split("<br>")]
        res[m.group(1)] = {
            "badge": None if badge in ("—", "-", "") else badge,
            "fig": [c for c in caps if c.startswith(FIG_WORDS)],
            "tab": [c for c in caps if c.startswith(TAB_WORDS)],
        }
    return res


# ---------------------------------------------------------------- примитивы pptx
def _set_run(r, text, pt, b=False, i=False, color=TEXT):
    r.text = text
    f = r.font
    f.name = FONT
    f.size = Pt(pt)
    f.bold = bool(b)
    f.italic = bool(i)
    f.color.rgb = color
    rpr = r._r.get_or_add_rPr()
    for tag in ("a:ea", "a:cs"):
        el = rpr.find(qn(tag))
        if el is None:
            el = etree.SubElement(rpr, qn(tag))
        el.set("typeface", FONT)


def _bullet(p, kind, indent_in):
    pPr = p._p.get_or_add_pPr()
    emu = int(Inches(indent_in))
    pPr.set("marL", str(emu))
    pPr.set("indent", str(-emu))
    for tag in ("a:buNone", "a:buChar", "a:buAutoNum", "a:buFont"):
        for el in pPr.findall(qn(tag)):
            pPr.remove(el)
    if kind == "bullet":
        bf = etree.SubElement(pPr, qn("a:buFont"))
        bf.set("typeface", "Arial")
        bc = etree.SubElement(pPr, qn("a:buChar"))
        bc.set("char", "•")
    elif kind == "num":
        bf = etree.SubElement(pPr, qn("a:buFont"))
        bf.set("typeface", FONT)
        an = etree.SubElement(pPr, qn("a:buAutoNum"))
        an.set("type", "arabicPeriod")
        if p.__dict__.get("_start"):
            an.set("startAt", str(p._start))
    else:
        etree.SubElement(pPr, qn("a:buNone"))


def add_text(slide, x, y, w, h, paras, pt, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
             color=TEXT, fill=None, margin=0.05):
    """paras: [{runs, kind: plain|bullet|num, indent, after, align, pt, color}]"""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is not None:
        tb.fill.solid()
        tb.fill.fore_color.rgb = fill
    tf = tb.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    for side in ("margin_left", "margin_right", "margin_top", "margin_bottom"):
        setattr(tf, side, Inches(margin))
    tf.vertical_anchor = anchor
    first = True
    for p in paras:
        para = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        para.alignment = p.get("align", align)
        size = p.get("pt", pt)
        if p.get("after"):
            para.space_after = Pt(p["after"] * size)
        kind = p.get("kind", "plain")
        _bullet(para, kind, p.get("indent", 0.0) if kind != "plain" else 0.0)
        for t, b, i in p["runs"]:
            _set_run(para.add_run(), t, size, b, i, p.get("color", color))
    return tb


def add_poly(slide, pts, color):
    ff = slide.shapes.build_freeform(pts[0][0], pts[0][1], scale=Inches(1))
    ff.add_line_segments(pts[1:], close=True)
    shp = ff.convert_to_shape()
    shp.fill.solid()
    shp.fill.fore_color.rgb = color
    shp.line.fill.background()
    shp.shadow.inherit = False
    return shp


def img_size(path):
    with Image.open(path) as im:
        return im.size


def add_image(slide, path, x, y, w, h):
    """Картинка по центру рамки (x,y,w,h) без искажения пропорций; → фактический прямоугольник."""
    iw, ih = img_size(path)
    k = min(w / iw, h / ih)
    pw, ph = iw * k, ih * k
    px, py = x + (w - pw) / 2, y + (h - ph) / 2
    slide.shapes.add_picture(str(path), Inches(px), Inches(py), Inches(pw), Inches(ph))
    return px, py, pw, ph


def P(s, **kw):
    d = {"runs": inline_runs(s) if isinstance(s, str) else s}
    d.update(kw)
    return d


# ---------------------------------------------------------------- каркас слайда
def chrome(slide, title, number, badge, approb):
    add_poly(slide, [(0, 0), (11.97, 0), (11.62, HEAD_H), (0, HEAD_H)], NAVY)
    tp = [P(title, color=WHITE)]
    pt = TITLE_PT
    while pt > 24 and paras_h([{"runs": [(title, True, False)]}], pt, 11.0 - 0.12) > HEAD_H - 0.1:
        pt -= 1
    if pt < TITLE_PT:
        log(f"сл. {number}: заголовок ужат до {pt} pt")
    add_text(slide, 0.40, 0.0, 11.1, HEAD_H, [{"runs": [(title, True, False)]}], pt,
             anchor=MSO_ANCHOR.MIDDLE, color=WHITE)
    if badge:
        bx = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(12.03), Inches(0.30),
                                    Inches(1.20), Inches(0.50))
        bx.fill.solid()
        bx.fill.fore_color.rgb = RED
        bx.line.fill.background()
        bx.shadow.inherit = False
        tf = bx.text_frame
        for side in ("margin_left", "margin_right", "margin_top", "margin_bottom"):
            setattr(tf, side, Inches(0.03))
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.word_wrap = False
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        _set_run(p.add_run(), badge, 16, True, False, WHITE)
    if number is not None:
        add_poly(slide, [(12.28, 6.76), (SW, 6.76), (SW, SH), (12.0, SH)], NAVY)
        add_text(slide, 12.15, 6.76, 1.15, 0.74, [P(str(number))], 24, align=PP_ALIGN.CENTER,
                 anchor=MSO_ANCHOR.MIDDLE, color=WHITE)
        # номер жирный
        for r in slide.shapes[-1].text_frame.paragraphs[0].runs:
            r.font.bold = True
    if approb:
        pa = [P(approb, color=GREY)]
        for r in range(len(pa[0]["runs"])):
            t, b, _ = pa[0]["runs"][r]
            pa[0]["runs"][r] = (t, b, True)
        pt = APPROB_PT
        while pt > 12 and paras_h(pa, pt, 11.3) > 0.42:
            pt -= 1
        add_text(slide, X0, 6.86, 11.35, 0.5, pa, pt, anchor=MSO_ANCHOR.MIDDLE, color=GREY)


def caption_paras(text, align=PP_ALIGN.CENTER):
    return [{"runs": [(text, False, False)], "align": align}]


def cap_h(text, width, pt=CAP_PT):
    return paras_h(caption_paras(text), pt, width - 0.12) + 0.08


def fig_stack(slide, x, y, w, h, groups, caps, folder, lang, gap=0.12, valign="middle"):
    """Группы картинок (каждая — ряд) с подписями под каждой, вписанные в рамку."""
    rows = []
    for gi, g in enumerate(groups):
        paths = [SLIDES / folder / "img" / f for f in g]
        for p in paths:
            if not p.exists():
                log(f"{folder} [{lang}]: нет картинки {p.name}")
        paths = [p for p in paths if p.exists()]
        asp = [img_size(p)[0] / img_size(p)[1] for p in paths]
        cap = caps[gi] if gi < len(caps) else None
        rows.append((paths, asp, cap))
    capsum = sum(cap_h(c, w) for _, _, c in rows if c) + gap * (len(rows) - 1)
    hgap = 0.15
    # высота ряда при полной ширине
    base = [(w - hgap * (len(p) - 1)) / sum(a) for p, a, _ in rows]
    k = min(1.0, (h - capsum) / sum(base))
    heights = [b * k for b in base]
    total = sum(heights) + capsum
    cy = y + (h - total) / 2 if valign == "middle" else y
    for (paths, asp, cap), rh in zip(rows, heights):
        rw = sum(a * rh for a in asp) + hgap * (len(paths) - 1)
        cx = x + (w - rw) / 2
        for p, a in zip(paths, asp):
            add_image(slide, p, cx, cy, a * rh, rh)
            cx += a * rh + hgap
        cy += rh
        if cap:
            ch = cap_h(cap, w)
            add_text(slide, x, cy, w, ch, caption_paras(cap), CAP_PT)
            cy += ch
        cy += gap
    return total


def add_table(slide, x, y, w, rows, fracs, pt, header=True, bold_first_col=False, align_center_cols=()):
    nr, nc = len(rows), len(rows[0])
    colw = [w * f for f in fracs]
    rh = table_row_heights(rows, colw, pt)
    gt = slide.shapes.add_table(nr, nc, Inches(x), Inches(y), Inches(w), Inches(sum(rh)))
    tbl = gt.table
    tblPr = tbl._tbl.tblPr
    tblPr.set("bandRow", "0")
    tblPr.set("firstRow", "0")
    for ci, cw in enumerate(colw):
        tbl.columns[ci].width = Inches(cw)
    for ri, row in enumerate(rows):
        tbl.rows[ri].height = Inches(rh[ri])
        for ci, cell_txt in enumerate(row):
            cell = tbl.cell(ri, ci)
            cell.margin_left = cell.margin_right = Inches(0.06)
            cell.margin_top = cell.margin_bottom = Inches(0.03)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            is_head = header and ri == 0
            cell.fill.fore_color.rgb = NAVY if is_head else (TINT if ri % 2 == 0 else WHITE)
            tf = cell.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER if (is_head or ci in align_center_cols) else PP_ALIGN.LEFT
            runs = inline_runs(cell_txt)
            for t, b, i in runs:
                _set_run(p.add_run(), t, pt, b or is_head or (bold_first_col and ci == 0), i,
                         WHITE if is_head else TEXT)
    return sum(rh)


def table_row_heights(rows, colw, pt):
    res = []
    for ri, row in enumerate(rows):
        hmax = 0
        for ci, c in enumerate(row):
            runs = [(t, b or ri == 0, i) for t, b, i in inline_runs(c)] or [(" ", False, False)]
            n = wrap_lines(runs, pt, colw[ci] - 0.12 - 0.04)
            hmax = max(hmax, n * pt * LINE / 72.0)
        res.append(hmax + 0.08)
    return res


def fit_table(rows, colw_total, fracs, height, hi=TABLE_MAX, lo=TABLE_MIN, where=""):
    for pt in range(hi, lo - 1, -1):
        if sum(table_row_heights(rows, [colw_total * f for f in fracs], pt)) * 1.05 <= height:
            return pt
    log(f"{where}: таблица не влезла даже при {lo} pt")
    return lo


def notes(slide, speech):
    txt = re.sub(r"\n{2,}", "\n\n", speech.strip())
    slide.notes_slide.notes_text_frame.text = plain_speech(txt)


def plain_speech(s):
    return re.sub(r"\*\*(.+?)\*\*|\*(.+?)\*", lambda m: m.group(1) or m.group(2), s)


# ---------------------------------------------------------------- титул
TITLE_SRC = 0   # индекс титульного слайда в архиве


def clone_title(prs, src, dst_layout, logo_path):
    s = prs.slides.add_slide(dst_layout)
    for ph in list(s.placeholders):
        ph._element.getparent().remove(ph._element)
    img_part, rid = s.part.get_or_add_image_part(str(logo_path))
    tree = s.shapes._spTree
    for el in src.shapes._spTree:
        if el.tag in (qn("p:nvGrpSpPr"), qn("p:grpSpPr")):
            continue
        new = copy.deepcopy(el)
        for blip in new.iter(qn("a:blip")):
            blip.set(qn("r:embed"), rid)
        tree.append(new)
    return s


def _set_para(p, runs, pt_default=None, keep_fmt=True):
    """Заменить текст абзаца, сохранив формат первого run'а-образца по типу (жирный / курсив)."""
    rs = p.runs
    proto_b = next((r for r in rs if r.font.bold), rs[0] if rs else None)
    proto_i = next((r for r in rs if r.font.italic), proto_b)
    size_b = proto_b.font.size if proto_b is not None else Pt(pt_default)
    size_i = proto_i.font.size if proto_i is not None else size_b
    color = None
    for r in rs:
        r._r.getparent().remove(r._r)
    for t, b, i in runs:
        r = p.add_run()
        proto = proto_i if i else proto_b
        if proto is not None:
            r._r.insert(0, copy.deepcopy(proto._r.find(qn("a:rPr"))))
        r.text = t
        r.font.bold = b
        r.font.italic = i
        r.font.size = size_i if i else size_b
        r.font.name = FONT


def fill_title(slide, blocks, number=None):
    items = [plain(s) for s in next(b for k, b in blocks if k == "bullets")]
    uni, topic, prog, degree, doc, cons, fcons, place = items[:8]
    uni = re.sub(r";\s*(логотип|logo)\s*$", "", uni)
    u1, u2 = uni.split(", ", 1)
    u2 = u2[0].upper() + u2[1:]
    shapes = {sh.name: sh for sh in slide.shapes}
    by_text = {}
    for sh in slide.shapes:
        if sh.has_text_frame and sh.text_frame.text.strip():
            by_text[sh.text_frame.text.strip()[:12]] = sh
    uni_sh = next(sh for sh in slide.shapes if sh.has_text_frame and "университет" in sh.text_frame.text)
    place_sh = next(sh for sh in slide.shapes if sh.has_text_frame and "2026" in sh.text_frame.text
                    and len(sh.text_frame.text) < 40)
    ppl_sh = next(sh for sh in slide.shapes if sh.has_text_frame and "Докторант" in sh.text_frame.text)
    top_sh = next(sh for sh in slide.shapes if sh.has_text_frame and "8D06102" in sh.text_frame.text)

    ps = uni_sh.text_frame.paragraphs
    _set_para(ps[0], [(u1, True, False)])
    _set_para(ps[1], [(u2, True, False)])
    uw = uni_sh.width / 914400 - 0.3
    upt = 28
    while upt > 18 and max(text_w(u1, upt, True), text_w(u2, upt, True)) > uw:
        upt -= 1
    if upt < 28:
        for p in ps:
            for r in p.runs:
                r.font.size = Pt(upt)
        log(f"титул: название вуза/кафедры ужато до {upt} pt, чтобы уместилось в две строки шапки")

    _set_para(place_sh.text_frame.paragraphs[0], [(place, True, False)])
    # надпись «МУИТ, Алматы, 2026» — по правому краю, в одну строку
    right = place_sh.left + place_sh.width
    place_sh.width = Inches(3.6)
    place_sh.left = right - place_sh.width
    place_sh.text_frame.paragraphs[0].alignment = PP_ALIGN.RIGHT
    place_sh.text_frame.word_wrap = False
    if number is not None:   # на повторе титула номер ставим внизу справа — надпись сдвигаем левее
        place_sh.left = Inches(8.4)
        place_sh.width = Inches(3.45)
        place_sh.text_frame.paragraphs[0].alignment = PP_ALIGN.RIGHT

    tps = top_sh.text_frame.paragraphs
    # тема — абзацы 0–1 (две строки), 2 — пустой, 3 — ОП, 4 — степень
    _set_para(tps[0], [(topic, True, False)])
    tps[1]._p.getparent().remove(tps[1]._p)
    tps = top_sh.text_frame.paragraphs
    _set_para(tps[2], [(prog, True, False)])
    _set_para(tps[3], [(degree, True, False)])

    def lv(s):
        lab, val = s.split(": ", 1)
        return lab, val
    pps = ppl_sh.text_frame.paragraphs
    (l1, v1), (l2, v2), (l3, v3) = lv(doc), lv(cons), lv(fcons)
    # образец: P0 — «Докторант: имя» + «Консультант: …» в одном абзаце через <a:br/>? — пересобираем по абзацам
    p0 = pps[0]
    for br in p0._p.findall(qn("a:br")):
        p0._p.remove(br)
    _set_para(p0, [(l1 + ": ", True, False), (v1, False, True)])
    # второй абзац (консультант) — копия P0
    p_cons = copy.deepcopy(p0._p)
    p0._p.addnext(p_cons)
    from pptx.text.text import _Paragraph
    pc = _Paragraph(p_cons, p0._parent)
    _set_para(pc, [(l2 + ": ", True, False), (v2, False, True)])
    pps = ppl_sh.text_frame.paragraphs
    # pps: [doc, cons, fcons-label, fcons-org, fcons-name]
    _set_para(pps[2], [(l3 + ":", True, False)])
    m = re.match(r"^(.*?,\s*)(Prof\..*)$", v3)
    org, name = (m.group(1).strip().rstrip(","), m.group(2)) if m else (v3, "")
    _set_para(pps[3], [(org + ",", False, True)])
    _set_para(pps[4], [(name, False, True)])
    # ужать, если длинно (ru/en)
    total = sum(len(p.text) for p in ppl_sh.text_frame.paragraphs)
    runs_all = [[(r.text, r.font.bold, r.font.italic) for r in p.runs] for p in ppl_sh.text_frame.paragraphs]
    for scale in (1.0, 0.95, 0.9, 0.85, 0.8):
        h = sum(paras_h([{"runs": rr}], 17 * scale, ppl_sh.width / 914400 - 0.2) for rr in runs_all)
        if h <= ppl_sh.height / 914400 - 0.1:
            break
    if scale < 1.0:
        for p in ppl_sh.text_frame.paragraphs:
            for r in p.runs:
                r.font.size = Pt(round(r.font.size.pt * scale, 1))
        log(f"титул: блок «Докторант / консультанты» ужат до {scale:.0%} (16 pt → {16*scale:.1f} pt)")
    return slide


# ---------------------------------------------------------------- слайды
def blocks_of(blocks, kind):
    return [b for k, b in blocks if k == kind]


def first(blocks, kind, default=None):
    r = blocks_of(blocks, kind)
    return r[0] if r else default


def list_paras(items, kind, pt_after=0.25, indent=0.32):
    return [P(s, kind=kind, indent=indent, after=pt_after) for s in items]


def text_paras(blocks, skip=("fig", "approb", "table", "source")):
    out = []
    for k, b in blocks:
        if k in skip:
            continue
        if k == "para":
            out.append(P(b, after=0.3))
        elif k == "bullets":
            out += list_paras(b, "bullet")
        elif k == "num":
            out += list_paras(b, "num")
    if out:
        out[-1]["after"] = 0
    return out


def split_params(s):
    """«Параметры: a; b; c» → заголовок + пункты (разрез по «; » вне скобок)."""
    lab, rest = s.split(":", 1)
    items, depth, cur = [], 0, ""
    for ch in rest:
        if ch in "[(":
            depth += 1
        elif ch in "])":
            depth -= 1
        if ch == ";" and depth == 0:
            items.append(cur.strip())
            cur = ""
        else:
            cur += ch
    if cur.strip():
        items.append(cur.strip())
    return lab.strip() + ":", items


def L_text(slide, ctx):
    """Только текст (03, 04, 30)."""
    paras = []
    for k, b in ctx["blocks"]:
        if k == "para":
            paras.append(P(b, after=0.35))
        elif k in ("bullets", "num"):
            paras += list_paras(b, "bullet" if k == "bullets" else "num", pt_after=0.2)
            paras[-1]["after"] = 0.4
    paras[-1]["after"] = 0
    h = Y1 + 0.1 - Y0
    pt = fit_pt(paras, X1 - X0, h, hi=22, where=ctx["where"])
    ctx["pt"] = pt
    add_text(slide, X0, Y0, X1 - X0, h, paras, pt)


def L_02(slide, ctx):
    b = ctx["blocks"]
    items = first(b, "bullets")
    src = first(b, "source")
    lw = 7.25
    src_p = [P([(src, False, True)], color=GREY)]
    src_h = paras_h(src_p, 12, lw - 0.12) + 0.1
    paras = list_paras(items, "bullet", pt_after=0.45)
    paras[-1]["after"] = 0
    h = Y1 + 0.1 - Y0 - src_h - 0.1
    pt = fit_pt(paras, lw, h, hi=22, where=ctx["where"])
    ctx["pt"] = pt
    add_text(slide, X0, Y0, lw, h, paras, pt, anchor=MSO_ANCHOR.MIDDLE)
    add_text(slide, X0, Y1 + 0.1 - src_h, lw, src_h, src_p, 12, color=GREY)
    fx = X0 + lw + 0.25
    fig_stack(slide, fx, Y0, X1 - fx, Y1 + 0.1 - Y0, first(b, "fig"), ctx["caps"]["fig"],
              ctx["folder"], ctx["lang"])


def L_05(slide, ctx):
    b = ctx["blocks"]
    rows = first(b, "table")
    formula = first(b, "para")
    cap = ctx["caps"]["tab"][0]
    w = X1 - X0
    fp = [P(formula, align=PP_ALIGN.CENTER)]
    fh = paras_h(fp, 20, w - 0.4) + 0.25
    ch = cap_h(cap, w)
    avail = Y1 - Y0 - ch - fh - 0.25
    fr = [0.30, 0.36, 0.34]
    pt = fit_table(rows, w, fr, avail, hi=18, lo=TABLE_MIN, where=ctx["where"])
    ctx["pt"] = pt
    add_text(slide, X0, Y0, w, ch, caption_paras(cap, PP_ALIGN.LEFT), CAP_PT)
    th = add_table(slide, X0, Y0 + ch, w, rows, fr, pt, bold_first_col=True)
    fy = Y0 + ch + th + 0.25
    add_text(slide, X0 + 0.5, fy, w - 1.0, fh, fp, 20, fill=TINT, anchor=MSO_ANCHOR.MIDDLE, margin=0.1)


def L_06(slide, ctx):
    b = ctx["blocks"]
    lw = 6.3
    # слева: рисунок + постановка
    heading = [x for x in blocks_of(b, "para")][0]
    forms = first(b, "bullets")
    fpt = 16
    fw = lw - 0.55
    frows = []
    for s in forms:
        m = re.match(r"^(.*?)\s+\((\d+)\)\s*$", s)
        frows.append((m.group(1), m.group(2)) if m else (s, ""))
    fh_each = [paras_h([P(t)], fpt, fw - 0.12) + 0.06 for t, _ in frows]
    hh = 0.4
    block_h = hh + sum(fh_each)
    fig_h = Y1 + 0.05 - Y0 - block_h - 0.1
    fig_stack(slide, X0, Y0, lw, fig_h, first(b, "fig"), ctx["caps"]["fig"], ctx["folder"], ctx["lang"],
              valign="top")
    y = Y0 + fig_h + 0.1
    add_text(slide, X0, y, lw, hh, [P(heading)], 18)
    y += hh
    for (t, n), fh in zip(frows, fh_each):
        add_text(slide, X0, y, fw, fh, [P(t)], fpt)
        add_text(slide, X0 + fw, y, lw - fw, fh, [P(f"({n})", align=PP_ALIGN.RIGHT)], fpt)
        y += fh
    # справа: таблица
    rx = X0 + lw + 0.3
    rw = X1 - rx
    cap = ctx["caps"]["tab"][0]
    ch = cap_h(cap, rw)
    rows = first(b, "table")
    fr = [0.07, 0.30, 0.63]
    pt = fit_table(rows, rw, fr, Y1 - Y0 - ch, hi=15, where=ctx["where"])
    ctx["pt"] = min(pt, fpt)
    add_text(slide, rx, Y0, rw, ch, caption_paras(cap, PP_ALIGN.LEFT), CAP_PT)
    add_table(slide, rx, Y0 + ch, rw, rows, fr, pt, align_center_cols=(0,))


def L_07(slide, ctx):
    b = ctx["blocks"]
    rows = first(b, "table")
    items = first(b, "bullets")
    cap = ctx["caps"]["tab"][0]
    w = X1 - X0
    ch = cap_h(cap, w)
    fr = [0.50, 0.25, 0.25]
    # буквы A–D крупно
    rows = [r[:] for r in rows]
    for r in rows[1:]:
        r[1], r[2] = f"**{r[1]}**", f"**{r[2]}**"
    paras = list_paras(items, "bullet", pt_after=0.3)
    paras[-1]["after"] = 0
    tpt = 22
    th = sum(table_row_heights(rows, [w * f for f in fr], tpt))
    avail = Y1 - Y0 - ch - th - 0.45
    pt = fit_pt(paras, w, avail, hi=22, where=ctx["where"])
    ctx["pt"] = pt
    bh = paras_h(paras, pt, w - 0.12) * 1.04 + 0.1
    y = Y0 + max(0, (Y1 - Y0 - ch - th - 0.45 - bh) / 2)
    add_text(slide, X0, y, w, ch, caption_paras(cap, PP_ALIGN.LEFT), CAP_PT)
    th = add_table(slide, X0, y + ch, w, rows, fr, tpt, align_center_cols=(1, 2))
    add_text(slide, X0, y + ch + th + 0.45, w, bh, paras, pt)


def L_08(slide, ctx):
    b = ctx["blocks"]
    rows = first(b, "table")
    summary = first(b, "para")
    sp = [P(f"**{summary}**" if not summary.startswith("**") else summary, align=PP_ALIGN.CENTER)]
    sh_ = paras_h(sp, 18, X1 - X0 - 0.12) + 0.1
    top_h = Y1 + 0.05 - Y0 - sh_ - 0.1
    lw = 5.0
    fig_stack(slide, X0, Y0, lw, top_h, first(b, "fig"), ctx["caps"]["fig"], ctx["folder"], ctx["lang"])
    rx = X0 + lw + 0.25
    rw = X1 - rx
    cap = ctx["caps"]["tab"][0]
    ch = cap_h(cap, rw)
    fr = [0.20, 0.17, 0.25, 0.19, 0.19]
    pt = fit_table(rows, rw, fr, top_h - ch, hi=15, where=ctx["where"])
    ctx["pt"] = pt
    th = sum(table_row_heights(rows, [rw * f for f in fr], pt))
    ty = Y0 + max(0, (top_h - ch - th) / 2)
    add_text(slide, rx, ty, rw, ch, caption_paras(cap, PP_ALIGN.LEFT), CAP_PT)
    add_table(slide, rx, ty + ch, rw, rows, fr, pt)
    add_text(slide, X0, Y1 + 0.05 - sh_, X1 - X0, sh_, sp, 18, color=NAVY)


def L_fig(slide, ctx):
    """Рисунок(и) на всю ширину + текст (пункты/параметры) под ними."""
    b = ctx["blocks"]
    paras = []
    for k, v in b:
        if k == "para":
            if re.match(r"^(Параметр|Parameters)", v):
                lab, items = split_params(v)
                paras.append(P(f"**{lab}**", after=0.15))
                paras += list_paras(items, "bullet", pt_after=0.15)
            else:
                paras.append(P(v, after=0.3))
        elif k in ("bullets", "num"):
            paras += list_paras(v, "bullet" if k == "bullets" else "num", pt_after=0.2)
    w = X1 - X0
    y1 = Y1 + 0.08
    if paras:
        paras[-1]["after"] = 0
        pt = 18
        th = paras_h(paras, pt, w - 0.12) * 1.04 + 0.05
        ctx["pt"] = pt
        add_text(slide, X0, y1 - th, w, th, paras, pt)
        y1 -= th + 0.15
    fig_stack(slide, X0, Y0, w, y1 - Y0, first(b, "fig"), ctx["caps"]["fig"], ctx["folder"], ctx["lang"])


def L_side(slide, ctx):
    """Рисунок слева, параметры справа (17)."""
    b = ctx["blocks"]
    v = first(b, "para")
    lab, items = split_params(v)
    paras = [P(f"**{lab}**", after=0.3)] + list_paras(items, "bullet", pt_after=0.3)
    paras[-1]["after"] = 0
    lw = 7.6
    fig_stack(slide, X0, Y0, lw, Y1 + 0.05 - Y0, first(b, "fig"), ctx["caps"]["fig"], ctx["folder"], ctx["lang"])
    rx = X0 + lw + 0.3
    pt = fit_pt(paras, X1 - rx, Y1 - Y0, hi=20, where=ctx["where"])
    ctx["pt"] = pt
    add_text(slide, rx, Y0, X1 - rx, Y1 - Y0, paras, pt, anchor=MSO_ANCHOR.MIDDLE)


def L_29(slide, ctx):
    b = ctx["blocks"]
    groups = first(b, "fig")
    caps = ctx["caps"]["fig"]
    lw = 7.0
    items = first(b, "num")
    paras = list_paras(items, "num", pt_after=0.2)
    paras[-1]["after"] = 0
    # слева: схема сверху, пункты снизу
    sys_img = SLIDES / ctx["folder"] / "img" / groups[0][0]
    iw, ih = img_size(sys_img)
    fig_h = lw * ih / iw + cap_h(caps[0], lw)
    avail = Y1 + 0.05 - Y0 - fig_h - 0.15
    pt = fit_pt(paras, lw, avail, hi=18, where=ctx["where"])
    ctx["pt"] = pt
    fig_stack(slide, X0, Y0, lw, fig_h, [groups[0]], [caps[0]], ctx["folder"], ctx["lang"], valign="top")
    add_text(slide, X0, Y0 + fig_h + 0.15, lw, avail, paras, pt)
    rx = X0 + lw + 0.25
    fig_stack(slide, rx, Y0, X1 - rx, Y1 + 0.05 - Y0, [groups[1]], [caps[1]], ctx["folder"], ctx["lang"])


def L_31(slide, ctx):
    lang = ctx["lang"]
    _, kk_body, _ = read_md(ctx["folder"], "kk")
    kb = parse_blocks(kk_body)
    # kk: первый абзац «Жалпы … 5 · Сурет: …» разобран как fig — берём подпись итога из текста kk
    total_kk = re.match(r"^(.*?)\s*·", kk_body.strip()).group(1)
    groups = [b for k, b in kb if k == "fig"][0]
    # категории и записи
    cats = []   # (label, [entries])
    for k, v in kb:
        if k == "para":
            m = re.match(r"^\*\*(.+?)\*\*\s*(.*)$", v)
            cats.append([m.group(1), [m.group(2)] if m.group(2) else []])
        elif k == "bullets" and cats:
            cats[-1][1] += v
    if lang != "kk":
        _, body, _ = read_md(ctx["folder"], lang)
        labels = re.findall(r"[«\"“]([^»\"”]+)[»\"”]", body)
        for c, lab in zip(cats, labels[:3]):
            c[0] = lab + ":"
        total = labels[3] if len(labels) > 3 else total_kk
    else:
        total = total_kk
    paras = [P(f"**{total}**", after=0.5)]
    for lab, ents in cats:
        paras.append(P(f"**{lab}**", after=0.15, color=NAVY))
        paras += [P(e, kind="bullet", indent=0.28, after=0.15) for e in ents]
        paras[-1]["after"] = 0.45
    paras[-1]["after"] = 0
    lw = 8.9
    pt = fit_pt(paras, lw, Y1 + 0.05 - Y0, hi=18, lo=14, where=ctx["where"])
    ctx["pt"] = pt
    add_text(slide, X0, Y0, lw, Y1 + 0.05 - Y0, paras, pt, anchor=MSO_ANCHOR.MIDDLE)
    rx = X0 + lw + 0.25
    fig_stack(slide, rx, Y0, X1 - rx, Y1 + 0.05 - Y0, groups, [None], ctx["folder"], "kk")


def L_R2(slide, ctx):
    """Резерв R2: три экрана приложения в ряд сверху, пункты снизу."""
    b = ctx["blocks"]
    items = first(b, "num")
    paras = list_paras(items, "num", pt_after=0.15)
    paras[-1]["after"] = 0
    w = X1 - X0
    fig_h = (Y1 + 0.05 - Y0) * 0.60
    fig_stack(slide, X0, Y0, w, fig_h, first(b, "fig"), ctx["caps"]["fig"], ctx["folder"], ctx["lang"], valign="top")
    ty = Y0 + fig_h + 0.15
    pt = fit_pt(paras, w, Y1 + 0.05 - ty, hi=18, lo=14, where=ctx["where"])
    ctx["pt"] = pt
    add_text(slide, X0, ty, w, Y1 + 0.05 - ty, paras, pt)


LAYOUTS = {
    "02-relevance": L_02, "03-aim-objectives": L_text, "04-provisions": L_text, "05-review": L_05,
    "06-system-architecture": L_06, "07-factorial-design": L_07, "08-datasets": L_08,
    "17-aug-geometric": L_side, "29-screening-system": L_29, "30-conclusion": L_text,
    "31-publications": L_31, "R2-webapp": L_R2,
}


# ---------------------------------------------------------------- сборка
def open_template():
    prs = Presentation(str(ARCHIVE))
    return prs


def drop_slides(prs, keep_from):
    """Удалить исходные слайды архива (первые keep_from штук) из списка и связей."""
    sldIdLst = prs.slides._sldIdLst
    ids = list(sldIdLst)[:keep_from]
    for sid in ids:
        rid = sid.get(qn("r:id"))
        prs.part.drop_rel(rid)
        sldIdLst.remove(sid)


def build(lang):
    global REPORT_LOG
    order = read_plan()
    caps = read_captions(lang)
    prs = open_template()
    n_arch = len(prs.slides)
    src_title = prs.slides[TITLE_SRC]
    blank = next(l for l in prs.slide_layouts if l.name == "BLANK")
    logo = SLIDES / "01-title" / "img" / "a01_1.png"
    stats = []
    num = 0
    main = [o for o in order if not o[0].startswith("R")]
    reserve = [o for o in order if o[0].startswith("R")]
    for key, folder in main + reserve:
        num = key if key.startswith("R") else num + 1
        title, body, speech = read_md(folder, lang)
        blocks = parse_blocks(body)
        where = f"сл. {key} [{lang}]"
        cap = caps.get(key, {"badge": None, "fig": [], "tab": []})
        if folder in ("01-title", "33-final"):
            s = clone_title(prs, src_title, src_title.slide_layout, logo)
            if folder == "33-final":
                # повтор титула: данные — из 01-title того же языка
                _, b01, _ = read_md("01-title", lang)
                fill_title(s, parse_blocks(b01), number=num)
                _number_only(s, num)
            else:
                fill_title(s, blocks)
            notes(s, speech)
            stats.append((key, None))
            continue
        s = prs.slides.add_slide(blank)
        for ph in list(s.placeholders):
            ph._element.getparent().remove(ph._element)
        approb = first(blocks, "approb")
        if len(blocks_of(blocks, "approb")) > 1:
            log(f"{where}: больше одной строки апробации — поставлена первая")
        chrome(s, title, num, cap["badge"], approb)
        ctx = {"blocks": blocks, "caps": cap, "folder": folder, "lang": lang, "where": where, "pt": None}
        LAYOUTS.get(folder, L_fig)(s, ctx)
        notes(s, speech)
        stats.append((key, ctx["pt"]))
    drop_slides(prs, n_arch)
    out = HERE / f"presentation_{lang}.pptx"
    prs.save(str(out))
    return out, stats


def _number_only(s, num):
    add_poly(s, [(12.28, 6.76), (SW, 6.76), (SW, SH), (12.0, SH)], NAVY)
    add_text(s, 12.15, 6.76, 1.15, 0.74, [P(f"**{num}**")], 24, align=PP_ALIGN.CENTER,
             anchor=MSO_ANCHOR.MIDDLE, color=WHITE)


def to_pdf(pptx_paths):
    import win32com.client
    app = win32com.client.DispatchEx("PowerPoint.Application")
    res = []
    try:
        for p in pptx_paths:
            pres = app.Presentations.Open(str(p), True, False, False)
            pdf = p.with_suffix(".pdf")
            pres.SaveAs(str(pdf), 32)
            pres.Close()
            res.append(pdf)
    finally:
        app.Quit()
    return res


def to_png(pdf, outdir, zoom=1.5):
    import pymupdf
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    d = pymupdf.open(str(pdf))
    for i, pg in enumerate(d, 1):
        pg.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom)).save(str(outdir / f"{pdf.stem}_{i:02d}.png"))
    return len(d)


def main(argv):
    langs = [a for a in argv if a in LANGS] or LANGS
    want_pdf = "--no-pdf" not in argv
    png_dir = argv[argv.index("--png") + 1] if "--png" in argv else None
    outs = []
    for lang in langs:
        REPORT_LOG.clear()
        out, stats = build(lang)
        outs.append(out)
        small = [f"{k}:{pt}" for k, pt in stats if pt is not None and pt < 18]
        print(f"[{lang}] {out.name}: {len(stats)} слайдов; кегль основного текста < 18 pt: {', '.join(small) or 'нет'}")
        for m in REPORT_LOG:
            print(f"   ! {m}")
    if want_pdf:
        try:
            pdfs = to_pdf(outs)
            for p in pdfs:
                print("pdf:", p.name)
                if png_dir:
                    to_png(p, png_dir)
        except Exception as e:  # нет PowerPoint — только pptx
            print("PDF не сделан:", e)


if __name__ == "__main__":
    main(sys.argv[1:])
