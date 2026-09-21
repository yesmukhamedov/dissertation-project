"""Разобрать пустые бланки заключения этической комиссии МУИТ в `form_layout.json`.

Бланки (`Заключение_Этической_комиссии_бланк_{рус,каз}.docx`) лежат в каталоге
материалов совета, вне репозитория, и на другой машине их может не быть. Поэтому
всё, что определяет оформление — поля страницы, шрифты и кегли, интервалы,
ширины колонок таблицы, тексты строк формы, подписанты, — снимается один раз
этим скриптом и хранится в репозитории как `form_layout.json`. Генератор
`build_ethics_conclusion.py` читает только этот файл; бланки ему не нужны.

Источники открываются ТОЛЬКО на чтение (`zipfile`, режим `r`) и не изменяются.

Использование:
    python defense/docs/ethics/parse_form.py
    python defense/docs/ethics/parse_form.py --rus PATH --kaz PATH
"""
from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path
from typing import Any

from lxml import etree

HERE = Path(__file__).resolve().parent
ROOT = HERE
while ROOT.parent != ROOT and not (ROOT / "defense").is_dir():
    ROOT = ROOT.parent

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}
COUNCIL_DIR = ROOT.parent / "council"
DEFAULT_RUS = COUNCIL_DIR / "Заключение_Этической_комиссии_бланк_рус.docx"
DEFAULT_KAZ = COUNCIL_DIR / "Заключение_Этической_комиссии_бланк_каз.docx"
OUT = HERE / "form_layout.json"

# Кегль, который Word подставляет, когда в docDefaults и стиле его нет: в бланках
# он не задан, а пустые абзацы (отбивки) как раз им и набраны.
WORD_DEFAULT_PT = 10.0


def _q(tag: str) -> str:
    return f"{{{W}}}{tag}"


def _attr(el: etree._Element | None, path: str, attr: str = "val") -> str | None:
    """Атрибут первого потомка по пути `path` или None.

    Args:
        el: Родительский элемент (может быть None).
        path: Путь вида `w:jc`.
        attr: Локальное имя атрибута.

    Returns:
        Значение атрибута либо None.
    """
    if el is None:
        return None
    found = el.find(path, NS)
    return None if found is None else found.get(_q(attr))


def _attrs(el: etree._Element | None) -> dict[str, str] | None:
    """Все атрибуты элемента с локальными именами."""
    if el is None:
        return None
    return {k.split("}")[1]: v for k, v in el.attrib.items()}


def _run_props(run: etree._Element) -> dict[str, Any]:
    """Свойства прогона: полужирный, кегль, язык."""
    rpr = run.find("w:rPr", NS)
    return {} if rpr is None else _rpr_props(rpr)


def _rpr_props(rpr: etree._Element) -> dict[str, Any]:
    """Свойства из элемента `w:rPr` (прогона либо знака абзаца)."""
    props: dict[str, Any] = {}
    if rpr.find("w:b", NS) is not None:
        props["b"] = True
    if rpr.find("w:i", NS) is not None:
        props["i"] = True
    size = _attr(rpr, "w:sz")
    if size:
        props["pt"] = int(size) / 2
    lang = _attr(rpr, "w:lang")
    if lang:
        props["lang"] = lang
    return props


def _paragraph(p: etree._Element) -> dict[str, Any]:
    """Абзац: выравнивание, интервалы, отступы и слитые одинаковые прогоны."""
    out: dict[str, Any] = {}
    ppr = p.find("w:pPr", NS)
    if ppr is not None:
        if _attr(ppr, "w:jc"):
            out["jc"] = _attr(ppr, "w:jc")
        if ppr.find("w:spacing", NS) is not None:
            out["spacing"] = _attrs(ppr.find("w:spacing", NS))
        if ppr.find("w:ind", NS) is not None:
            out["ind"] = _attrs(ppr.find("w:ind", NS))
        # Кегль знака абзаца задаёт высоту пустых строк (пустая ячейка ответа, отбивки)
        mark = ppr.find("w:rPr", NS)
        if mark is not None:
            out["mark"] = _rpr_props(mark)
    runs: list[list[Any]] = []
    for run in p.findall("w:r", NS):
        text = "".join(t.text or "" for t in run.findall("w:t", NS))
        if not text:
            continue
        props = _run_props(run)
        if runs and runs[-1][1] == props:
            runs[-1][0] += text
        else:
            runs.append([text, props])
    out["runs"] = runs
    return out


def _table(tbl: etree._Element) -> dict[str, Any]:
    """Таблица: ширина, сетка, поля ячеек, рамки и содержимое построчно."""
    pr = tbl.find("w:tblPr", NS)
    mar = pr.find("w:tblCellMar", NS)
    borders = pr.find("w:tblBorders", NS)
    out: dict[str, Any] = {
        "width": int(_attr(pr, "w:tblW", "w") or 0),
        "grid": [int(g.get(_q("w"))) for g in tbl.findall("w:tblGrid/w:gridCol", NS)],
        "cell_margin": {etree.QName(m).localname: int(m.get(_q("w"))) for m in mar} if mar is not None else {},
        "border": {etree.QName(b).localname: {"val": b.get(_q("val")), "sz": int(b.get(_q("sz")))} for b in borders},
        "rows": [],
    }
    for tr in tbl.findall("w:tr", NS):
        cells = []
        for tc in tr.findall("w:tc", NS):
            tcpr = tc.find("w:tcPr", NS)
            cmar = tcpr.find("w:tcMar", NS) if tcpr is not None else None
            cells.append({
                "width": int(_attr(tcpr, "w:tcW", "w") or 0),
                "valign": _attr(tcpr, "w:vAlign"),
                "margin": {etree.QName(m).localname: int(m.get(_q("w"))) for m in cmar} if cmar is not None else None,
                "paragraphs": [_paragraph(p) for p in tc.findall("w:p", NS)],
            })
        cells_out = {"cells": cells}
        out["rows"].append(cells_out)
    return out


def parse_form(path: Path) -> dict[str, Any]:
    """Разобрать один бланк.

    Args:
        path: Путь к .docx (открывается только на чтение).

    Returns:
        Словарь: страница, тело документа (абзацы и таблицы по порядку).
    """
    with zipfile.ZipFile(path, "r") as z:
        doc = etree.fromstring(z.read("word/document.xml"))
        styles = etree.fromstring(z.read("word/styles.xml"))
    fonts = styles.find("w:docDefaults/w:rPrDefault/w:rPr/w:rFonts", NS)
    body = doc.find("w:body", NS)
    sect = body.find("w:sectPr", NS)
    items: list[dict[str, Any]] = []
    for el in body:
        tag = etree.QName(el).localname
        if tag == "p":
            items.append({"type": "p", **_paragraph(el)})
        elif tag == "tbl":
            items.append({"type": "tbl", **_table(el)})
    return {
        "source_file": path.name,
        "font": fonts.get(_q("ascii")) if fonts is not None else "Times New Roman",
        "default_pt": WORD_DEFAULT_PT,
        "page": {
            "width": int(_attr(sect, "w:pgSz", "w")),
            "height": int(_attr(sect, "w:pgSz", "h")),
            "margins": {k: int(v) for k, v in _attrs(sect.find("w:pgMar", NS)).items()},
        },
        "body": items,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--rus", type=Path, default=DEFAULT_RUS)
    ap.add_argument("--kaz", type=Path, default=DEFAULT_KAZ)
    ap.add_argument("--out", type=Path, default=OUT)
    args = ap.parse_args()

    layout = {"ru": parse_form(args.rus), "kz": parse_form(args.kaz)}
    args.out.write_text(json.dumps(layout, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for lang, form in layout.items():
        table = next(i for i in form["body"] if i["type"] == "tbl")
        print(f"{lang}: {form['source_file']} — {len(form['body'])} блоков, "
              f"таблица {table['width']} twips, колонки {table['grid']}, строк {len(table['rows'])}")
    print(f"→ {args.out}")


if __name__ == "__main__":
    main()
