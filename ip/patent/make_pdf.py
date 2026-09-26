"""Render both patent applications (utility model, invention) as submission PDFs.

For each application directory (um/, inv/) four documents are produced in build/<app>/:
opisanie.pdf, formula.pdf, referat.pdf and figures.pdf (one drawing per page, "Фиг. N").
Fonts, inline markup and tables are shared with ../kazpatent/make_pdf.py; this
module only adds bullet lists, HTML-comment skipping and the drawings sheet.

Usage (from the repo root):
    python ip/patent/make_pdf.py            # both applications
    python ip/patent/make_pdf.py --only um
"""

from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from pathlib import Path

from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
)

BASE = Path(__file__).resolve().parent
BUILD = BASE / "build"


def _load_kazpatent():
    """Import the sibling copyright-package renderer for its fonts, markup and tables."""
    spec = importlib.util.spec_from_file_location("kp_pdf", BASE.parent / "kazpatent" / "make_pdf.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["kp_pdf"] = mod
    spec.loader.exec_module(mod)
    return mod


kp = _load_kazpatent()

MARGINS = dict(left=25 * mm, right=20 * mm, top=20 * mm, bottom=20 * mm)
FRAME_W = kp.PAGE_W - MARGINS["left"] - MARGINS["right"]
FRAME_H = kp.PAGE_H - MARGINS["top"] - MARGINS["bottom"]


def _styles() -> dict:
    """Patent-document styles: 12 pt Times, 1.5 line spacing, first-line indent."""
    s = kp.referat_styles()
    for key in ("p", "h2"):
        s[key].leading = 18
    s["p"].firstLineIndent = 10 * mm
    s["li"] = ParagraphStyle("li", parent=s["p"], firstLineIndent=0, leftIndent=10 * mm,
                             bulletIndent=4 * mm)
    s["meta"] = ParagraphStyle("meta", parent=s["p"], firstLineIndent=0, fontSize=10.5)
    s["cap"] = ParagraphStyle("cap", parent=s["p"], firstLineIndent=0, alignment=TA_CENTER)
    return s


def _doc(target: Path, title: str) -> BaseDocTemplate:
    """A4 document with page numbers centred at the bottom."""
    def footer(canvas, doc) -> None:
        canvas.saveState()
        canvas.setFont(kp.SERIF, 10)
        canvas.drawCentredString(kp.PAGE_W / 2, MARGINS["bottom"] / 2, str(doc.page))
        canvas.restoreState()

    doc = BaseDocTemplate(str(target), pagesize=kp.A4, leftMargin=MARGINS["left"],
                          rightMargin=MARGINS["right"], topMargin=MARGINS["top"],
                          bottomMargin=MARGINS["bottom"], title=title, author="Есмухамедов Н.С.")
    frame = Frame(MARGINS["left"], MARGINS["bottom"], FRAME_W, FRAME_H, id="body")
    doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=footer)])
    return doc


def render_markdown(source: Path, target: Path, title: str) -> int:
    """Render one application document (description, claims or abstract); return page count."""
    styles = _styles()
    story: list = []
    para: list[str] = []
    bullet: list[str] = []
    rows: list[list[str]] = []

    def flush() -> None:
        nonlocal para, bullet, rows
        if para:
            story.append(Paragraph(kp.inline(" ".join(para)), styles["p"]))
        if bullet:
            story.append(Paragraph(kp.inline(" ".join(bullet)), styles["li"], bulletText="–"))
        if rows:
            story.append(Spacer(1, 4))
            story.append(kp.build_table(rows, styles, FRAME_W))
            story.append(Spacer(1, 8))
        para, bullet, rows = [], [], []

    for raw in source.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        stripped = line.strip()
        if stripped.startswith("<!--"):
            continue
        if stripped.startswith("|"):
            if para or bullet:
                flush()
            if not kp.is_separator(stripped):
                rows.append(kp.split_row(stripped))
            continue
        if rows:
            flush()
        if not stripped:
            flush()
        elif stripped.startswith("# "):
            flush()
            story.append(Paragraph(kp.inline(stripped[2:]), styles["h1"]))
        elif stripped.startswith("## "):
            flush()
            story.append(Paragraph(kp.inline(stripped[3:]), styles["h2"]))
        elif stripped.startswith("МПК"):
            flush()
            story.append(Paragraph(kp.inline(stripped), styles["meta"]))
        elif stripped.startswith("- "):
            flush()
            bullet = [stripped[2:]]
        elif re.match(r"\d+\. ", stripped):
            flush()
            para = [stripped]
        elif bullet:
            bullet.append(stripped)
        else:
            para.append(stripped)
    flush()

    doc = _doc(target, title)
    doc.build(story)
    return doc.page


def render_figures(fig_dir: Path, target: Path, title: str) -> int:
    """One drawing per page, scaled to the frame, captioned «Фиг. N»."""
    styles = _styles()
    story: list = []
    figs = sorted(fig_dir.glob("fig*.png"), key=lambda p: int(p.stem[3:]))
    for i, path in enumerate(figs):
        img = Image(str(path))
        scale = min(FRAME_W / img.imageWidth, (FRAME_H - 30 * mm) / img.imageHeight)
        img.drawWidth, img.drawHeight = img.imageWidth * scale, img.imageHeight * scale
        story += [img, Spacer(1, 6 * mm), Paragraph(f"Фиг. {path.stem[3:]}", styles["cap"])]
        if i < len(figs) - 1:
            story.append(PageBreak())
    doc = _doc(target, title)
    doc.build(story)
    return doc.page


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", choices=["um", "inv"])
    args = ap.parse_args()
    kp.register_fonts()
    for app in ([args.only] if args.only else ["um", "inv"]):
        src, out = BASE / app, BUILD / app
        out.mkdir(parents=True, exist_ok=True)
        for name, title in [("opisanie", "Описание"), ("formula", "Формула"), ("referat", "Реферат")]:
            n = render_markdown(src / f"{name}.md", out / f"{name}.pdf", title)
            print(f"{app}/{name}.pdf: {n} с.")
        n = render_figures(src / "figures", out / "figures.pdf", "Чертежи")
        print(f"{app}/figures.pdf: {n} с.")


if __name__ == "__main__":
    main()
