"""Per-slide analysis PDFs (Russian): one file per slide in build/analysis/.

Each PDF:
  page 1      — our slide, taken from build/presentation_ru.pdf (the PowerPoint render);
  next pages  — slides/NN-id/analysis.md rendered to A4 landscape (headless Chrome/Edge);
  then        — every slide of another council candidate that analysis.md names as a sample
                or mentions, cut from council/Образцы документов/_video/<slug>/presentation.pdf,
                with a caption strip: author, slide number, rubric, and the analysis line that cites it.

Which sample slides are taken, per author, in order of priority:
  1. slide numbers given explicitly — the «Слайд» column of a «## Образцы» table row whose first cell
     names the author, or inline «Автор сл. 9–12» / «(Автор, сл. 4)»;
  2. a rubric in guillemets right after the name — «Әйтім «Интерфейс»» → the author's slides of that rubric;
  3. a bare mention — the author's slides whose rubric matches our slide's rubric (FALLBACK_RUBRIC),
     at most FALLBACK_MAX of them.
Slides that cannot be resolved are listed on the last analysis page, not silently dropped.

Run after any change to slides or analysis.md:
    python report/build_analysis_pdf.py              # all slides, uses the existing build/presentation_ru.pdf
    python report/build_analysis_pdf.py 02 29        # only these slides
    python report/build_analysis_pdf.py --rebuild    # first re-render the ru deck (build/build_pptx.py ru, needs PowerPoint)
"""
from __future__ import annotations

import argparse
import html
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

import fitz  # PyMuPDF
import markdown

ROOT = Path(__file__).resolve().parents[1]                      # defense/presentation
DISS = ROOT.parents[1]                                          # dissertation
COUNCIL_TEMP = DISS.parent / "council" / "temp"
COUNCIL_VIDEO = DISS.parent / "council" / "Образцы документов" / "_video"
DECK_RU = ROOT / "build" / "presentation_ru.pdf"
OUT_DIR = ROOT / "build" / "analysis"
FONT = Path("C:/Windows/Fonts/times.ttf")
BROWSERS = [Path("C:/Program Files/Google/Chrome/Application/chrome.exe"),
            Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe")]

# slug: (display name, regex of the surname stem as it appears in analysis.md, any case form)
AUTHORS: dict[str, tuple[str, str]] = {
    "alpar":         ("Алпар С.Д.",         r"Алпар"),
    "bazarbekov":    ("Базарбеков И.М.",    r"Базарбеков"),
    "bakirova":      ("Бакирова Г.С.",      r"Бакиров"),
    "daurenbayeva":  ("Дауренбаева Н.А.",   r"Дауренбаев"),
    "aitim":         ("Әйтім Ә.Қ.",         r"[ӘƏ]йтім"),
    "ibrayeva":      ("Ибраева Ж.Б.",       r"Ибраев"),
    "merembayev":    ("Мерембаев Т.Ж.",     r"Мерембаев"),
    "momynkulov":    ("Момынкулов З.З.",    r"Момын[кқ]улов"),
    "mukhanov":      ("Муханов С.Б.",       r"Муханов"),
    "myrzakerimova": ("Мырзакерімова А.Б.", r"Мырзакер[іи]мов"),
    "naumenko":      ("Науменко В.В.",      r"Науменко"),
    "olzhayev":      ("Олжаев О.М.",        r"Олжаев"),
    "toktarova":     ("Тоқтарова А.Б.",     r"То[қк]таров"),
    "tokhtakhunov":  ("Тохтахунов И.Т.",    r"Тохтахунов"),
    "chinibayev":    ("Чинибаев Е.Г.",      r"Чинибаев"),
    "quanyshbay":    ("Қуанышбай Д.Н.",     r"[ҚК]уанышбай"),
}

# Our slide → regex over the council rubrics, used only for a bare mention (rule 3).
FALLBACK_RUBRIC: dict[str, str] = {
    "01": r"Титул",
    "02": r"Актуальн|Relevance",
    "03": r"Цель|objectives|Объект",
    "04": r"Положения|новизн|novelty",
    "05": r"Обзор",
    "06": r"Архитектур|Математическ|постановк",
    "07": r"Этапы эксперимента|Эксперимент|Метод",
    "08": r"Данные|Сбор данных", "09": r"Данные|Сбор данных", "10": r"Данные|Сбор данных",
    "20": r"Метрики|Препроцессинг и обучение",
    **{f"{n:02d}": r"Результат" for n in range(21, 29)},
    "29": r"Интерфейс|Модули|Практическ|на устройствах|платформ",
    "30": r"Заключение|Conclusion",
    "31": r"Публикации",
    "32": r"Охранные документы|свидетельств|Патент|Акт внедрен",
    "33": r"Титул|Благодар",
    "R1": r"Ограничен",
    "R2": r"Интерфейс|Дашборд|платформ",
}
FALLBACK_MAX = 3
SKIP_RUBRICS = {"повтор", "служебный кадр"}

CSS = """
@page { size: A4 landscape; margin: 14mm 16mm; }
body { font-family: 'Times New Roman', serif; font-size: 11.5pt; line-height: 1.35; color: #111; }
h1 { font-size: 17pt; margin: 0 0 4pt; color: #1F3864; }
.sub { color: #555; margin-bottom: 10pt; font-size: 10.5pt; }
h2 { font-size: 13.5pt; color: #1F3864; border-bottom: 1px solid #bbb; margin: 14pt 0 5pt; }
h3 { font-size: 12pt; margin: 10pt 0 4pt; }
table { border-collapse: collapse; width: 100%; margin: 5pt 0; font-size: 10pt; }
th, td { border: 1px solid #999; padding: 3pt 5pt; vertical-align: top; }
th { background: #e8edf5; }
code { font-family: Consolas, monospace; font-size: 9.5pt; background: #f2f2f2; padding: 0 2px; }
pre { background: #f2f2f2; padding: 6pt; white-space: pre-wrap; font-size: 9.5pt; }
img { max-width: 100%; max-height: 120mm; }
ul, ol { margin: 3pt 0 3pt 18pt; padding: 0; }
.samples td:first-child { white-space: nowrap; }
"""


@dataclass
class Rubric:
    slides: dict[int, str] = field(default_factory=dict)   # slide number → rubric


@dataclass
class Pick:
    slug: str
    slide: int
    rubric: str
    rule: str           # «указан номер» / «рубрика» / «по рубрике нашего слайда»
    cite: str           # the analysis line that caused the pick


def read_plan() -> list[tuple[str, str]]:
    """Slides in deck order (as build/build_pptx.py): main slides, then the reserve R1, R2."""
    order = [(m.group(1), m.group(2)) for m in re.finditer(
        r"^\| (\d\d|R\d) \| `([^`]+)` \|", (ROOT / "PLAN.md").read_text(encoding="utf-8"), re.M)]
    return [o for o in order if not o[0].startswith("R")] + [o for o in order if o[0].startswith("R")]


def load_rubrics() -> dict[str, Rubric]:
    """slug → slide rubrics from council/temp/*/Презентация/00_Слайды_по_порядку.txt."""
    out: dict[str, Rubric] = {}
    for f in COUNCIL_TEMP.glob("*/Презентация/00_Слайды_по_порядку.txt"):
        text = f.read_text(encoding="utf-8")
        m = re.search(r"_video/(\w+)/presentation\.pdf", text)
        if not m:
            continue
        rub = Rubric()
        for sm in re.finditer(r"^=== Слайд (\d+)[^\n]*\nРубрика: ([^\n]*)", text, re.M):
            rub.slides[int(sm.group(1))] = sm.group(2).strip()
        out[m.group(1)] = rub
    return out


def parse_numbers(cell: str) -> list[int]:
    """«3–4», «9–12», «2, 5», «сл. 10» → [3, 4] …; non-numeric cells («Table 1», «—») → []."""
    cell = cell.replace("сл.", "").strip()
    if not re.fullmatch(r"[\d\s,–\-]+", cell):
        return []
    nums: list[int] = []
    for part in re.split(r",", cell):
        part = part.strip()
        if m := re.fullmatch(r"(\d+)\s*[–-]\s*(\d+)", part):
            a, b = int(m.group(1)), int(m.group(2))
            nums += list(range(a, b + 1)) if 0 < b - a < 10 else [a, b]
        elif part.isdigit():
            nums.append(int(part))
    return nums


def find_picks(slide_key: str, text: str, rubrics: dict[str, Rubric]) -> tuple[list[Pick], list[str]]:
    """Resolve every author mentioned in analysis.md to concrete sample slides."""
    explicit: dict[str, list[Pick]] = {}
    mentioned: dict[str, str] = {}                  # slug → first citing line (order of appearance)
    slide_col = None                                # index of the «Слайд» column in the current table
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if any(c == "Слайд" for c in cells):
                slide_col = cells.index("Слайд")
                continue
            if set("".join(cells)) <= set("-: "):
                continue
        else:
            slide_col = None
            cells = []
        for slug, (_, stem) in AUTHORS.items():
            if not re.search(stem, line):
                continue
            mentioned.setdefault(slug, line)
            nums: list[int] = []
            rule = "указан номер слайда"
            # 1a. table row whose first cell names the author, with a «Слайд» column
            if cells and slide_col is not None and re.search(stem, cells[0]) and slide_col < len(cells):
                nums = parse_numbers(cells[slide_col])
            # 1b. inline «Автор сл. 9–12» / «Автор, сл. 4»
            for m in re.finditer(stem + r"\w*,?\s*(?:—\s*)?сл\.\s*(\d+(?:\s*[–-]\s*\d+)?(?:,\s*\d+)*)", line):
                nums += parse_numbers(m.group(1))
            # 2. «Автор «Рубрика»»
            if not nums and slug in rubrics:
                for m in re.finditer(stem + r"\w*\s*«([^»]+)»", line):
                    want = m.group(1).lower()
                    nums += [n for n, r in rubrics[slug].slides.items()
                             if want in r.lower() or r.lower() in want]
                    rule = f"рубрика «{m.group(1)}»"
            for n in nums:
                rub = rubrics.get(slug, Rubric()).slides.get(n, "?")
                explicit.setdefault(slug, []).append(Pick(slug, n, rub, rule, line))

    picks: list[Pick] = []
    unresolved: list[str] = []
    fallback = FALLBACK_RUBRIC.get(slide_key)
    for slug, line in mentioned.items():
        if slug not in rubrics:
            unresolved.append(f"{AUTHORS[slug][0]} — презентации в council/temp нет")
            continue
        got = explicit.get(slug)
        if not got and fallback:
            got = [Pick(slug, n, r, "по рубрике нашего слайда", line)
                   for n, r in sorted(rubrics[slug].slides.items())
                   if r not in SKIP_RUBRICS and re.search(fallback, r, re.I)][:FALLBACK_MAX]
        if not got:
            unresolved.append(f"{AUTHORS[slug][0]} — упомянут, но слайд не определён "
                              f"(нет номера, рубрики в «…» и слайда рубрики нашего слайда)")
            continue
        seen: set[int] = set()
        for p in got:
            if p.slide not in seen and p.slide in rubrics[slug].slides:
                seen.add(p.slide)
                picks.append(p)
    return picks, unresolved


def slide_title_ru(folder: Path) -> str:
    ru = folder / "ru.md"
    if ru.exists():
        if m := re.search(r"^# (.+)$", ru.read_text(encoding="utf-8"), re.M):
            return m.group(1).strip()
    return folder.name


def browser() -> Path:
    for b in BROWSERS:
        if b.exists():
            return b
    sys.exit("Нужен Chrome или Edge для печати анализа в PDF.")


def render_analysis(folder: Path, key: str, title: str, picks: list[Pick], unresolved: list[str],
                    tmp: Path) -> Path:
    md_text = (folder / "analysis.md").read_text(encoding="utf-8")
    md_text = re.sub(r"^# .*\n", "", md_text, count=1)          # own header below
    body = markdown.markdown(md_text, extensions=["tables", "fenced_code", "sane_lists"])
    rows = "".join(
        f"<tr><td>{html.escape(AUTHORS[p.slug][0])}, сл. {p.slide}</td><td>{html.escape(p.rubric)}</td>"
        f"<td>{html.escape(p.rule)}</td></tr>" for p in picks)
    tail = ""
    if picks:
        tail += ("<h2>Слайды других авторов в этом файле</h2><table class='samples'>"
                 "<tr><th>Автор, слайд</th><th>Рубрика у автора</th><th>Почему взят</th></tr>" + rows + "</table>")
    if unresolved:
        tail += "<h2>Упомянуты, но не добавлены</h2><ul>" + "".join(
            f"<li>{html.escape(u)}</li>" for u in unresolved) + "</ul>"
    page = (f"<!doctype html><html lang='ru'><head><meta charset='utf-8'>"
            f"<base href='{folder.as_uri()}/'><style>{CSS}</style></head><body>"
            f"<h1>Слайд {key} · {html.escape(title)}</h1>"
            f"<div class='sub'>Анализ: как и почему — <code>slides/{folder.name}/analysis.md</code></div>"
            f"{body}{tail}</body></html>")
    src = tmp / f"{folder.name}.html"
    src.write_text(page, encoding="utf-8")
    out = tmp / f"{folder.name}.analysis.pdf"
    subprocess.run([str(browser()), "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={out}", src.as_uri()],
                   check=True, capture_output=True, timeout=120)
    return out


def add_sample_page(doc: fitz.Document, p: Pick, cache: dict[str, fitz.Document]) -> None:
    """The author's slide under a caption strip saying whose slide it is and why it is here."""
    if p.slug not in cache:
        cache[p.slug] = fitz.open(COUNCIL_VIDEO / p.slug / "presentation.pdf")
    src = cache[p.slug]
    r = src[p.slide - 1].rect
    strip = r.width * 0.075
    page = doc.new_page(width=r.width, height=r.height + strip)
    page.show_pdf_page(fitz.Rect(0, strip, r.width, r.height + strip), src, p.slide - 1)
    page.draw_rect(fitz.Rect(0, 0, r.width, strip), color=None, fill=(0.91, 0.93, 0.96))
    cite = re.sub(r"\*\*|`", "", p.cite).strip("| ").replace(" | ", " · ")
    cite = cite if len(cite) < 230 else cite[:227] + "…"
    fs = strip * 0.27
    page.insert_font(fontname="tnr", fontfile=str(FONT))
    page.insert_text((r.width * 0.015, strip * 0.38),
                     f"Образец: {AUTHORS[p.slug][0]}, слайд {p.slide} · «{p.rubric}» · {p.rule}",
                     fontname="tnr", fontsize=fs, color=(0.12, 0.22, 0.39))
    page.insert_textbox(fitz.Rect(r.width * 0.015, strip * 0.48, r.width * 0.985, strip),
                        f"В анализе: {cite}", fontname="tnr", fontsize=fs * 0.72, color=(0.3, 0.3, 0.3))


PAGE_W = fitz.paper_rect("a4-l").width  # 842 pt — ширина A4 альбомной, как у страниц analysis.md


def same_width(doc: fitz.Document) -> fitz.Document:
    """Все страницы — одной ширины PAGE_W, пропорции сохраняются (слайды 960/1280/1920 pt уменьшаются)."""
    out = fitz.open()
    for i, pg in enumerate(doc):
        r = pg.rect
        if abs(r.width - PAGE_W) < 0.5:
            out.insert_pdf(doc, from_page=i, to_page=i)
            continue
        h = r.height * PAGE_W / r.width
        out.new_page(width=PAGE_W, height=h).show_pdf_page(fitz.Rect(0, 0, PAGE_W, h), doc, i)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slides", nargs="*", help="номера слайдов (02 29 R1 R2); по умолчанию все")
    ap.add_argument("--rebuild", action="store_true", help="сначала пересобрать build/presentation_ru.pdf")
    args = ap.parse_args()

    if args.rebuild:
        subprocess.run([sys.executable, str(ROOT / "build" / "build_pptx.py"), "ru"], check=True)
    if not DECK_RU.exists():
        sys.exit(f"Нет {DECK_RU} — запустите с --rebuild (нужен PowerPoint).")
    deck = fitz.open(DECK_RU)
    order = read_plan()
    if deck.page_count != len(order):
        sys.exit(f"В {DECK_RU.name} {deck.page_count} стр., в PLAN.md {len(order)} слайдов — пересоберите (--rebuild).")

    rubrics = load_rubrics()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    cache: dict[str, fitz.Document] = {}
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        for idx, (key, name) in enumerate(order):
            if args.slides and key not in args.slides:
                continue
            folder = ROOT / "slides" / name
            if not (folder / "analysis.md").exists():
                print(f"{key}: нет analysis.md — пропуск")
                continue
            text = (folder / "analysis.md").read_text(encoding="utf-8")
            picks, unresolved = find_picks(key, text, rubrics)
            doc = fitz.open()
            doc.insert_pdf(deck, from_page=idx, to_page=idx)
            doc.insert_pdf(fitz.open(render_analysis(folder, key, slide_title_ru(folder), picks, unresolved, tmp)))
            for p in picks:
                add_sample_page(doc, p, cache)
            out = OUT_DIR / f"{name}.pdf"
            doc = same_width(doc)
            doc.save(out, garbage=3, deflate=True)
            note = f", не добавлены: {len(unresolved)}" if unresolved else ""
            print(f"{key}: {out.name} — {doc.page_count} стр., образцов {len(picks)}{note}")


if __name__ == "__main__":
    main()
