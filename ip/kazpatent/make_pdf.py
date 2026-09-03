"""Render the NIIS submission documents as PDF.

Two targets, two very different shapes:
  * the reflect/abstract — Markdown with headings, bold runs and one table, set in
    Times New Roman, the same face the thesis uses;
  * the source listing — 10k lines of code that must stay column-aligned, set in
    Consolas and drawn straight onto the canvas (Platypus would crawl at this size).

Both fonts are taken from C:/Windows/Fonts because the base-14 PDF fonts carry no
Cyrillic — Courier would silently render the Russian headers as black boxes.

Usage (from the repo root):
    python ip/kazpatent/make_pdf.py                 # both documents
    python ip/kazpatent/make_pdf.py --only referat
    python ip/kazpatent/make_pdf.py --only listing --listing build/listing_full.txt
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

BASE = Path(__file__).resolve().parent
WIN_FONTS = Path("C:/Windows/Fonts")

SERIF, SERIF_BOLD, SERIF_ITALIC = "TimesNR", "TimesNR-Bold", "TimesNR-Italic"
MONO, MONO_BOLD = "Consolas", "Consolas-Bold"

PAGE_W, PAGE_H = A4


def register_fonts() -> None:
    """Register the Cyrillic-capable TrueType faces the two documents need."""
    faces = [
        (SERIF, "times.ttf"),
        (SERIF_BOLD, "timesbd.ttf"),
        (SERIF_ITALIC, "timesi.ttf"),
        (MONO, "consola.ttf"),
        (MONO_BOLD, "consolab.ttf"),
    ]
    for name, filename in faces:
        path = WIN_FONTS / filename
        if not path.exists():
            raise SystemExit(f"Не найден шрифт: {path}")
        pdfmetrics.registerFont(TTFont(name, str(path)))
    pdfmetrics.registerFontFamily(
        SERIF, normal=SERIF, bold=SERIF_BOLD, italic=SERIF_ITALIC, boldItalic=SERIF_BOLD
    )


# --------------------------------------------------------------------------- referat

INLINE_CODE = re.compile(r"`([^`]+)`")
BOLD = re.compile(r"\*\*(.+?)\*\*")
ITALIC = re.compile(r"(?<!\*)\*([^*]+)\*(?!\*)")
STRIKE = re.compile(r"~~(.+?)~~")


def inline(text: str) -> str:
    """Convert the Markdown inline subset used in these documents to reportlab markup."""
    out = escape(text)
    out = INLINE_CODE.sub(rf'<font face="{MONO}" size="9">\1</font>', out)
    out = BOLD.sub(r"<b>\1</b>", out)
    out = ITALIC.sub(r"<i>\1</i>", out)
    out = STRIKE.sub(r"<strike>\1</strike>", out)
    return out


def split_row(line: str) -> list[str]:
    """Split one Markdown table row into its cells."""
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_separator(line: str) -> bool:
    """True for the |---|---| rule that follows a table header."""
    cells = split_row(line)
    return bool(cells) and all(set(cell) <= set("-: ") and "-" in cell for cell in cells)


def build_table(rows: list[list[str]], styles: dict, width: float) -> Table:
    """Lay out a Markdown table, sizing columns by their longest cell."""
    header, body = rows[0], rows[1:]
    weights = [
        max(len(row[i]) for row in rows) if len(rows[0]) > i else 1
        for i in range(len(header))
    ]
    total = sum(weights) or 1
    # Keep any single column from collapsing below 15% of the table width.
    fractions = [max(w / total, 0.15) for w in weights]
    scale = sum(fractions)
    col_widths = [width * f / scale for f in fractions]

    data = [[Paragraph(inline(c), styles["th"]) for c in header]]
    data += [[Paragraph(inline(c), styles["td"]) for c in row] for row in body]

    table = Table(data, colWidths=col_widths, repeatRows=1, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.5, "#666666"),
                ("BACKGROUND", (0, 0), (-1, 0), "#eeeeee"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    return table


def referat_styles() -> dict:
    """Paragraph styles for the abstract, sized to the thesis conventions."""
    base = dict(fontName=SERIF, fontSize=12, leading=15.5)
    return {
        "h1": ParagraphStyle(
            "h1", **{**base, "fontName": SERIF_BOLD, "fontSize": 15, "leading": 19,
                     "alignment": TA_CENTER, "spaceAfter": 10},
        ),
        "h2": ParagraphStyle(
            "h2", **{**base, "fontName": SERIF_BOLD, "fontSize": 13, "leading": 16,
                     "spaceBefore": 12, "spaceAfter": 6},
        ),
        "p": ParagraphStyle("p", **{**base, "alignment": TA_JUSTIFY, "spaceAfter": 6}),
        "note": ParagraphStyle(
            "note", **{**base, "fontName": SERIF_ITALIC, "fontSize": 10.5,
                       "leading": 13, "alignment": TA_CENTER, "spaceAfter": 10},
        ),
        "th": ParagraphStyle("th", **{**base, "fontName": SERIF_BOLD, "fontSize": 10.5,
                                      "leading": 13}),
        "td": ParagraphStyle("td", **{**base, "fontSize": 10.5, "leading": 13}),
    }


def render_referat(source: Path, target: Path) -> int:
    """Render the abstract Markdown to PDF and return the page count."""
    styles = referat_styles()
    margin_l, margin_r, margin_t, margin_b = 30 * mm, 15 * mm, 20 * mm, 20 * mm
    frame_w = PAGE_W - margin_l - margin_r

    story: list = []
    paragraph: list[str] = []
    table_rows: list[list[str]] = []
    in_note = False

    def flush_paragraph() -> None:
        nonlocal paragraph, in_note
        if not paragraph:
            return
        text = " ".join(paragraph).strip()
        style = styles["note"] if in_note else styles["p"]
        if in_note:
            text = text.strip("*")
        story.append(Paragraph(inline(text) if not in_note else escape(text), style))
        paragraph, in_note = [], False

    def flush_table() -> None:
        nonlocal table_rows
        if table_rows:
            story.append(Spacer(1, 4))
            story.append(build_table(table_rows, styles, frame_w))
            story.append(Spacer(1, 8))
            table_rows = []

    for raw in source.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()

        if line.startswith("|"):
            flush_paragraph()
            if not is_separator(line):
                table_rows.append(split_row(line))
            continue
        flush_table()

        if not line.strip():
            flush_paragraph()
            continue
        if line.strip() == "---":
            flush_paragraph()
            continue
        if line.startswith("## "):
            flush_paragraph()
            story.append(Paragraph(inline(line[3:]), styles["h2"]))
            continue
        if line.startswith("# "):
            flush_paragraph()
            story.append(Paragraph(inline(line[2:]), styles["h1"]))
            continue
        if line.startswith("*") and not line.startswith("**") and not paragraph:
            in_note = True
        paragraph.append(line.strip())

    flush_paragraph()
    flush_table()

    def footer(canvas: pdfcanvas.Canvas, doc: BaseDocTemplate) -> None:
        canvas.saveState()
        canvas.setFont(SERIF, 10)
        canvas.drawCentredString(PAGE_W / 2, margin_b / 2, str(doc.page))
        canvas.restoreState()

    doc = BaseDocTemplate(
        str(target),
        pagesize=A4,
        leftMargin=margin_l,
        rightMargin=margin_r,
        topMargin=margin_t,
        bottomMargin=margin_b,
        title="Реферат",
        author="Есмухамедов Н.С.",
    )
    frame = Frame(margin_l, margin_b, frame_w, PAGE_H - margin_t - margin_b, id="body")
    doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=footer)])
    doc.build(story)
    return doc.page


# --------------------------------------------------------------------------- listing

FILE_HEADER = re.compile(r"^ФАЙЛ: (.+?)\s+\(\d+ строк\)$")


def render_listing(source: Path, target: Path, font_size: float = 8.0) -> int:
    """Draw the source listing onto the canvas, one text line per line, and paginate."""
    leading = font_size * 1.2
    margin_l, margin_r, margin_t, margin_b = 20 * mm, 12 * mm, 15 * mm, 15 * mm
    usable_w = PAGE_W - margin_l - margin_r
    top = PAGE_H - margin_t
    lines_per_page = int((top - margin_b - 6 * mm) / leading)

    char_w = pdfmetrics.stringWidth("M", MONO, font_size)
    max_chars = int(usable_w / char_w)

    canvas = pdfcanvas.Canvas(str(target), pagesize=A4)
    canvas.setTitle("Листинг исходного текста программы")
    canvas.setAuthor("Есмухамедов Н.С.")

    current_file = ""
    row = 0
    page = 1

    def start_page() -> None:
        canvas.setFont(MONO, font_size - 1)
        canvas.setFillGray(0.35)
        if current_file:
            canvas.drawString(margin_l, top + 4, current_file[:max_chars])
        canvas.drawRightString(PAGE_W - margin_r, margin_b - 10, f"с. {page}")
        canvas.setFillGray(0)
        canvas.setFont(MONO, font_size)

    start_page()
    text = canvas.beginText(margin_l, top - leading)
    text.setFont(MONO, font_size)

    for raw in source.read_text(encoding="utf-8").splitlines():
        match = FILE_HEADER.match(raw)
        if match:
            current_file = match.group(1)

        # Hard-wrap anything wider than the frame instead of letting it run off the page.
        chunks = [raw[i : i + max_chars] for i in range(0, len(raw), max_chars)] or [""]
        for chunk in chunks:
            if row >= lines_per_page:
                canvas.drawText(text)
                canvas.showPage()
                page += 1
                row = 0
                start_page()
                text = canvas.beginText(margin_l, top - leading)
                text.setFont(MONO, font_size)
            text.textLine(chunk)
            row += 1

    canvas.drawText(text)
    canvas.showPage()
    canvas.save()
    # The abstract has to state the листинг's page count, so leave it where fill.py
    # can pick it up instead of making someone transcribe it by hand.
    target.with_suffix(".pages").write_text(str(page), encoding="utf-8")
    return page


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--only", choices=["referat", "listing"], help="render one target")
    parser.add_argument("--referat", default="filled/referat.md", help="abstract source")
    parser.add_argument("--listing", default="build/listing_core.txt", help="listing source")
    parser.add_argument("--font-size", type=float, default=8.0, help="listing font size")
    args = parser.parse_args()

    register_fonts()

    if args.only != "listing":
        source = BASE / args.referat
        target = source.with_suffix(".pdf")
        pages = render_referat(source, target)
        print(f"Реферат:  {target}  ({pages} стр.)")

    if args.only != "referat":
        source = BASE / args.listing
        target = source.with_suffix(".pdf")
        pages = render_listing(source, target, args.font_size)
        print(f"Листинг:  {target}  ({pages} стр.)")


if __name__ == "__main__":
    main()
