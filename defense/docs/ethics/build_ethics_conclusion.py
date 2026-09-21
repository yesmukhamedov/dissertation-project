"""Собрать заключение этической комиссии МУИТ (Приложение 2) — RU и KZ.

Оформление — не наше: его задаёт бланк, который выдаёт МУИТ. Бланк разобран
скриптом `parse_form.py` в `form_layout.json` (поля, кегли, интервалы, ширины
колонок, тексты строк, подписанты), и этот генератор воссоздаёт документ из
той спецификации. Данные докторанта берутся из `council/METADATA.toml`, поэтому
дословность реестра гарантируется построением. Тексты, которых в реестре нет
(объекты исследования, защита прав), лежат в `conclusion.toml`.

Незаполненное поле печатается плейсхолдером `<…>` — документ остаётся пригодным
для распечатки, пока значение не известно. Пустые бланки-образцы генератор не
читает и не изменяет.

Режим `--blank` воспроизводит бланк дословно, без подстановок. Он нужен для
проверки: рендер такого документа обязан совпасть с рендером самого бланка.

Использование:
    python defense/docs/ethics/build_ethics_conclusion.py
    python defense/docs/ethics/build_ethics_conclusion.py --only ru --no-pdf
    python defense/docs/ethics/build_ethics_conclusion.py --blank --out <каталог>
"""
from __future__ import annotations

import argparse
import copy
import json
import re
import sys
import tomllib
from pathlib import Path
from typing import Any

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, Twips
from docx.text.paragraph import Paragraph

HERE = Path(__file__).resolve().parent
ROOT = HERE
while ROOT.parent != ROOT and not (ROOT / "defense").is_dir():
    ROOT = ROOT.parent

REGISTRY = ROOT / "council/METADATA.toml"
LAYOUT = HERE / "form_layout.json"
DATA = HERE / "conclusion.toml"
TIMES_BOLD = Path(r"C:\Windows\Fonts\timesbd.ttf")

PLACEHOLDER = "<…>"
EXPECTED_PAGES = 1
# Ширина колонки с номерами строк, twips. Нужна только русской версии: в казахском
# бланке такая колонка есть (704), в русском её нет. Ровно 704 помещается впритык —
# подпись строки 9 переходит на шестую строку и до низа полосы остаётся ~3 pt, так что
# любая будущая правка выдавит дату на вторую страницу. 640 уже этого не делает и от
# казахской колонки отличается на 1 мм. Если строки формы изменятся, сборка об этом скажет.
NUMBER_COL_W = 640
# Пустые абзацы в конец ячейки-ответа: ими добирается высота строки, если таблица
# не добивает страницу до подписей. Ключ — строка формы (1-based), значение —
# сколько абзацев. С колонкой номеров таблица и так высокая, добивка не нужна;
# словарь оставлен как ручка на случай, если состав строк изменится.
ANSWER_PADDING: dict[int, int] = {}

JC = {"center": WD_ALIGN_PARAGRAPH.CENTER, "both": WD_ALIGN_PARAGRAPH.JUSTIFY}
# Строка формы, чей ответ печатает сам бланк, а не докторант: это вывод комиссии.
FINDING_ROWS = (6, 7)  # 0-based: строки 7 и 8 («Нарушения не выявлены»)
PROTECTION_ROW = 8  # строка 9 — защита прав объектов исследования
MARKERS = {"ru": "полностью соответствует", "kz": "толық сәйкес"}
DATE_MARKERS = {"ru": "Дата выдачи", "kz": "Берілген күні"}
SIGN_RE = re.compile(r"_{5,}\s+(?P<name>\S.*)$")
DATE_BLANK = re.compile(r"_{5,}\s+2026")


# --------------------------------------------------------------------------- #
# Низкоуровневое оформление
# --------------------------------------------------------------------------- #

def _set_lang(run, lang: str | None) -> None:
    """Проставить язык прогона (`w:lang`), как в бланке."""
    if not lang:
        return
    rpr = run._r.get_or_add_rPr()
    el = rpr.find(qn("w:lang"))
    if el is None:
        el = OxmlElement("w:lang")
        rpr.append(el)
    el.set(qn("w:val"), lang)


def _add_run(par: Paragraph, text: str, props: dict[str, Any], default_pt: float, font: str):
    """Добавить прогон с кеглем, жирностью и языком из спецификации."""
    run = par.add_run(text)
    run.font.name = font
    rpr = run._r.get_or_add_rPr()
    fonts = rpr.find(qn("w:rFonts"))
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        fonts.set(qn(attr), font)
    run.font.size = Pt(props.get("pt", default_pt))
    if props.get("b"):
        run.font.bold = True
    if props.get("i"):
        run.font.italic = True
    _set_lang(run, props.get("lang"))
    return run


def _format_paragraph(par: Paragraph, spec: dict[str, Any]) -> None:
    """Выравнивание, интервалы и отступы абзаца по спецификации."""
    if spec.get("jc") in JC:
        par.alignment = JC[spec["jc"]]
    pf = par.paragraph_format
    pf.space_before = pf.space_after = Pt(0)
    spacing = spec.get("spacing") or {}
    if "before" in spacing:
        pf.space_before = Twips(int(spacing["before"]))
    if "after" in spacing:
        pf.space_after = Twips(int(spacing["after"]))
    ind = spec.get("ind") or {}
    if "firstLine" in ind:
        pf.first_line_indent = Twips(int(ind["firstLine"]))
    mark = spec.get("mark")
    if mark and "pt" in mark:
        # Кегль знака абзаца задаёт высоту пустой строки; без него пустые ячейки
        # и отбивки ниже бланка на пункт-два, и к концу страницы всё уезжает.
        rpr = OxmlElement("w:rPr")
        for tag in ("w:b", "w:bCs"):
            if mark.get("b"):
                rpr.append(OxmlElement(tag))
        for tag in ("w:sz", "w:szCs"):
            el = OxmlElement(tag)
            el.set(qn("w:val"), str(int(mark["pt"] * 2)))
            rpr.append(el)
        par._p.get_or_add_pPr().append(rpr)


def _fill_paragraph(par: Paragraph, spec: dict[str, Any], runs: list[list[Any]] | None,
                    layout: dict[str, Any]) -> None:
    """Оформить абзац и набрать в нём прогоны (свои или подставленные)."""
    _format_paragraph(par, spec)
    for text, props in (runs if runs is not None else spec["runs"]):
        _add_run(par, text, props, layout["default_pt"], layout["font"])


def _border_el(tag: str, val: str, sz: int, color: str) -> Any:
    el = OxmlElement(f"w:{tag}")
    el.set(qn("w:val"), val)
    el.set(qn("w:sz"), str(sz))
    el.set(qn("w:space"), "0")
    el.set(qn("w:color"), color)
    return el


def _build_table(doc, spec: dict[str, Any], layout: dict[str, Any],
                 answers: dict[int, list[str]] | None):
    """Воссоздать таблицу формы; `answers` — подстановки в последнюю колонку по строкам."""
    n_cols = len(spec["grid"])
    table = doc.add_table(rows=len(spec["rows"]), cols=n_cols)
    tbl = table._tbl
    pr = tbl.tblPr
    for child in list(pr):
        pr.remove(child)
    w = OxmlElement("w:tblW")
    w.set(qn("w:w"), str(spec["width"]))
    w.set(qn("w:type"), "dxa")
    pr.append(w)
    borders = OxmlElement("w:tblBorders")
    for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
        b = spec["border"][side]
        borders.append(_border_el(side, b["val"], b["sz"], "auto"))
    pr.append(borders)
    mar = OxmlElement("w:tblCellMar")
    for side in ("left", "right"):
        m = OxmlElement(f"w:{side}")
        m.set(qn("w:w"), str(spec["cell_margin"][side]))
        m.set(qn("w:type"), "dxa")
        mar.append(m)
    pr.append(mar)
    look = OxmlElement("w:tblLook")
    look.set(qn("w:val"), "0000")
    pr.append(look)
    for gc, width in zip(tbl.tblGrid.findall(qn("w:gridCol")), spec["grid"]):
        gc.set(qn("w:w"), str(width))

    for r, row_spec in enumerate(spec["rows"]):
        for c, cell_spec in enumerate(row_spec["cells"]):
            cell = table.cell(r, c)
            tcpr = cell._tc.get_or_add_tcPr()
            for child in list(tcpr):
                tcpr.remove(child)
            tcw = OxmlElement("w:tcW")
            tcw.set(qn("w:w"), str(cell_spec["width"]))
            tcw.set(qn("w:type"), "dxa")
            tcpr.append(tcw)
            tcb = OxmlElement("w:tcBorders")
            for side in ("top", "left", "bottom", "right"):
                tcb.append(_border_el(side, "single", 4, "000000"))
            tcpr.append(tcb)
            if cell_spec["margin"]:
                tcm = OxmlElement("w:tcMar")
                for side in ("top", "left", "bottom", "right"):
                    m = OxmlElement(f"w:{side}")
                    m.set(qn("w:w"), str(cell_spec["margin"][side]))
                    m.set(qn("w:type"), "dxa")
                    tcm.append(m)
                tcpr.append(tcm)
            # В бланке ячейки центрированы по вертикали, и в строках с длинным
            # ответом подпись слева «плавает» посередине. В заполненном документе
            # текст прижимается к верху — так в образцах совета и так его правил
            # кандидат вручную. `--blank` остаётся дословной копией бланка.
            valign = cell_spec["valign"] if answers is None else "top"
            if valign:
                va = OxmlElement("w:vAlign")
                va.set(qn("w:val"), valign)
                tcpr.append(va)

            is_answer = c == n_cols - 1 and answers is not None and r in answers
            first = cell.paragraphs[0]
            if is_answer:
                props = {"pt": 11.0, "lang": _lang_of(layout)}
                lines = list(answers[r]) + [""] * ANSWER_PADDING.get(r + 1, 0)
                for i, line in enumerate(lines):
                    par = first if i == 0 else cell.add_paragraph()
                    _format_paragraph(par, {"mark": {"pt": 11.0}})
                    for text, bold in _segments(line):
                        _add_run(par, text, {**props, "b": bold},
                                 layout["default_pt"], layout["font"])
            else:
                # В бланке за текстом подписи строки 9 идёт пустой абзац — след
                # правки формы, а не её элемент. В пустом бланке он безвреден,
                # в заполненном съедает ту самую строку, которой не хватает
                # до одной страницы. `--blank` его сохраняет.
                paragraphs = cell_spec["paragraphs"]
                if answers is not None:
                    while len(paragraphs) > 1 and not paragraphs[-1]["runs"]:
                        paragraphs = paragraphs[:-1]
                for i, pspec in enumerate(paragraphs):
                    par = first if i == 0 else cell.add_paragraph()
                    _fill_paragraph(par, pspec, None, layout)
    return table


def _segments(line: "str | list[tuple[str, bool]]") -> list[tuple[str, bool]]:
    """Ответ — либо строка целиком обычным, либо куски вида (текст, жирный)."""
    return [(line, False)] if isinstance(line, str) else list(line)


def _with_number_column(spec: dict[str, Any], layout: dict[str, Any]) -> dict[str, Any]:
    """Добавить слева колонку с номерами строк — её нет только в русском бланке.

    Казахский бланк нумерует строки, русский — нет. Кандидат попросил нумерацию
    в обеих версиях, поэтому колонка достраивается здесь, а не правится в бланке:
    `--blank` обязан оставаться дословной копией выданной формы.

    Args:
        spec: Спецификация таблицы из `form_layout.json`.
        layout: Спецификация языка (нужен язык прогонов).

    Returns:
        Копия спецификации с тремя колонками; двухколоночную возвращает как есть.
    """
    if len(spec["grid"]) != 2:
        return spec
    spec = copy.deepcopy(spec)
    label_w, answer_w = spec["grid"]
    # Ширина колонки номеров берётся из колонки подписей, а не делится между двумя:
    # подписи — короткие служебные фразы, их лишний перенос дешевле, чем перенос
    # в ответах (тема, консультанты), где строка тянет всю высоту таблицы. При
    # пропорциональном делении документ не помещается на страницу.
    label_w = spec["width"] - NUMBER_COL_W - answer_w
    spec["grid"] = [NUMBER_COL_W, label_w, answer_w]
    lang = _lang_of(layout)
    for i, row in enumerate(spec["rows"]):
        row["cells"][0]["width"], row["cells"][1]["width"] = label_w, answer_w
        row["cells"].insert(0, {
            "width": NUMBER_COL_W,
            "valign": None,
            "margin": None,
            "paragraphs": [{
                "jc": "center",
                "mark": {"pt": 11.0, "lang": lang},
                "runs": [[str(i + 1), {"pt": 11.0, "lang": lang}]],
            }],
        })
    return spec


def _lang_of(layout: dict[str, Any]) -> str:
    """Язык документа — по первому прогону с языком в теле бланка."""
    for item in layout["body"]:
        for p in item.get("paragraphs", []) if item["type"] == "tbl" else [item]:
            for _, props in p.get("runs", []):
                if "lang" in props:
                    return props["lang"]
    return "ru-RU"


# --------------------------------------------------------------------------- #
# Данные
# --------------------------------------------------------------------------- #

def _get(reg: dict[str, Any], dotted: str) -> str:
    """Значение реестра по `секция.поле` либо плейсхолдер, если пусто."""
    node: Any = reg
    for key in dotted.split("."):
        node = node.get(key, "") if isinstance(node, dict) else ""
    return str(node).strip() or PLACEHOLDER


def _measure_pt(text: str, size: float = 12.0) -> float:
    """Ширина строки полужирным Times New Roman, pt (для позиции табуляции подписей)."""
    from PIL import ImageFont
    scale = 100
    font = ImageFont.truetype(str(TIMES_BOLD), int(size * scale))
    return font.getlength(text) / scale


def _consultant_rows(reg: dict[str, Any], data: dict[str, Any],
                     lang: str) -> list[list[tuple[str, bool]]]:
    """Строка 5: оба научных консультанта — по абзацу на каждого, имя жирным.

    Степень и должность сокращены, место работы — без города, гражданство —
    «РК»/«ҚР»: так строка 5 заполнена во всех 16 заключениях других докторантов
    (степень аббревиатурой — 23 случая из 24, город не указывает никто). Полные
    формы из реестра остаются для документов, где они уместны.
    """
    sup, foreign, d = reg["supervisor"], reg["foreign_consultant"], data[lang]
    if lang == "ru":
        dept = sup["department_ru"].replace("кафедра", "кафедры")
        names = (sup["name_ru"], foreign["name_ru"])
        first = (f", {sup['degree_ru_short']}, {sup['title_ru_short']} {dept} "
                 f"{d['org']}, {d['supervisor_place']};")
        second = f", {foreign['title_ru']}, {foreign['org_en']}, {foreign['country_ru']}"
    else:
        # «кафедрасының … профессоры»: после изафета должность требует -ы.
        dept = sup["department_kz"].replace("кафедрасы", "кафедрасының")
        names = (sup["name_kz"], foreign["name_ru"])
        first = (f", {sup['degree_kz_short']}, {d['org']} {dept} "
                 f"{sup['title_kz']}ы, {d['supervisor_place']};")
        second = f", {foreign['title_kz']}, {foreign['org_en']}, {d['foreign_place']}"
    return [[(names[0], True), (first, False)], [(names[1], True), (second, False)]]


def _programme_rows(reg: dict[str, Any], lang: str) -> list[str]:
    """Строка 2: научно-педагогическое направление, под ним — код и имя ОП."""
    prog = reg["programme"]
    name = prog["name_ru"] if lang == "ru" else prog["name_kz"]
    direction = _get(reg, f"programme.direction_name_{lang}")
    return [f"{prog['direction_code']} – {direction}", f"{prog['code']} – {name}"]


def _approval(reg: dict[str, Any], lang: str) -> str:
    """Реквизиты приказа об утверждении темы для строки 4."""
    dis = reg["dissertation"]
    number = re.search(r"№\s*(\S+)", dis["topic_approval_order"]).group(1)
    date = dis["topic_approval_date"]
    if lang == "ru":
        return f"приказ № {number} от {date}"
    return f"№ {number} бұйрығы, {date} ж."


def _study_period(reg: dict[str, Any], lang: str) -> str:
    """Строка 3: в реестре лежит голый диапазон, суффикс — по языку документа."""
    period = _get(reg, "candidate.study_period")
    if period == PLACEHOLDER:
        return period
    return f"{period} гг." if lang == "ru" else f"{period} жж."


def _answers(reg: dict[str, Any], data: dict[str, Any], lang: str,
             layout: dict[str, Any]) -> dict[int, list["str | list[tuple[str, bool]]"]]:
    """Ответы докторанта на строки 1–6 и 9; строки 7–8 — вывод комиссии, их печатает сам бланк."""
    cand, dis, d = reg["candidate"], reg["dissertation"], data[lang]
    table = next(i for i in layout["body"] if i["type"] == "tbl")
    printed = {r: row["cells"][-1]["paragraphs"][0]["runs"] for r, row in enumerate(table["rows"])}
    # строки 7–8: у казахского бланка ответ в строке 8 не проставлен — берём формулу строки 7
    finding = "".join(t for t, _ in printed[FINDING_ROWS[0]])
    if lang == "ru":
        name, title = cand["name_ru"], dis["title_ru"]
    else:
        name, title = cand["name_kz"], dis["title_kz"]
    return {
        0: [[(name, True)]],
        1: _programme_rows(reg, lang),
        2: [_study_period(reg, lang)],
        3: [f"«{title}» ({_approval(reg, lang)})"],
        4: _consultant_rows(reg, data, lang),
        5: [d["objects"].strip() or PLACEHOLDER],
        FINDING_ROWS[0]: [finding],
        FINDING_ROWS[1]: [finding],
        PROTECTION_ROW: [d["protection"].strip() or PLACEHOLDER],
    }


def _closing_runs(reg: dict[str, Any], lang: str, spec: dict[str, Any]) -> list[list[Any]]:
    """Заключительная фраза: имя докторанта (жирным, как в бланке) и тема."""
    cand, dis = reg["candidate"], reg["dissertation"]
    base = {"pt": 12.0}
    if lang == "ru":
        return [
            ["Научные исследования докторанта ", dict(base)],
            [f"{cand['name_ru_gen']} ", {**base, "b": True}],
            [f"на тему «{dis['title_ru']}» полностью соответствует этическим нормам "
             "и может быть реализовано в нынешнем виде.", dict(base)],
        ]
    base["lang"] = "kk-KZ"
    return [
        ["Докторант ", dict(base)],
        [f"{cand['name_kz_gen']} ", {**base, "b": True}],
        [f"«{dis['title_kz']}» тақырыбындағы ғылыми зерттеулері әдеп нормаларына толық сәйкес келеді "
         "және қазіргі нұсқасында жүзеге асырылуы мүмкін.", dict(base)],
    ]


# --------------------------------------------------------------------------- #
# Сборка
# --------------------------------------------------------------------------- #

def _signature_parts(spec: dict[str, Any]) -> tuple[list[list[Any]], str, dict[str, Any]] | None:
    """Разобрать подписную строку на подпись-метку, «____ Фамилия И.О.» и свойства шрифта.

    Returns:
        (прогоны метки, хвост «_____  Фамилия», свойства хвоста) либо None, если это не подписная строка.
    """
    text = "".join(t for t, _ in spec["runs"])
    m = SIGN_RE.search(text)
    if not m:
        return None
    label = [[t, p] for t, p in spec["runs"] if p.get("b")]
    tail_props = next(p for _, p in spec["runs"] if not p.get("b") and p.get("pt"))
    tail = "_" * 17 + "  " + m.group("name").strip()
    return label, tail, tail_props


def build(lang: str, layout: dict[str, Any], reg: dict[str, Any], data: dict[str, Any],
          out_docx: Path, blank: bool) -> None:
    """Собрать один документ.

    Args:
        lang: `ru` или `kz`.
        layout: Спецификация из `form_layout.json` для этого языка.
        reg: Реестр `council/METADATA.toml`.
        data: Содержимое `conclusion.toml`.
        out_docx: Куда писать.
        blank: Воспроизвести бланк дословно, без подстановок.
    """
    doc = Document()
    normal = doc.styles["Normal"]
    normal.font.name = layout["font"]
    normal.font.size = Pt(layout["default_pt"])
    normal.paragraph_format.space_before = normal.paragraph_format.space_after = Pt(0)
    normal.paragraph_format.line_spacing = 1.0
    nrpr = normal.element.get_or_add_rPr()
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        nrpr.find(qn("w:rFonts")).set(qn(attr), layout["font"])

    # Режим совместимости Word 2013+, как в бланке. В шаблоне python-docx его нет,
    # Word работает в старом режиме и сдвигает таблицу влево на поле ячейки.
    settings = doc.settings.element
    compat = settings.find(qn("w:compat"))
    if compat is None:
        compat = OxmlElement("w:compat")
        settings.append(compat)
    setting = OxmlElement("w:compatSetting")
    setting.set(qn("w:name"), "compatibilityMode")
    setting.set(qn("w:uri"), "http://schemas.microsoft.com/office/word")
    setting.set(qn("w:val"), "15")
    compat.append(setting)

    sec = doc.sections[0]
    page = layout["page"]
    sec.page_width, sec.page_height = Twips(page["width"]), Twips(page["height"])
    m = page["margins"]
    sec.top_margin, sec.bottom_margin = Twips(m["top"]), Twips(m["bottom"])
    sec.left_margin, sec.right_margin = Twips(m["left"]), Twips(m["right"])
    sec.header_distance, sec.footer_distance = Twips(m["header"]), Twips(m["footer"])

    answers = None if blank else _answers(reg, data, lang, layout)
    chair = data["signatories"]["chair"] or None
    secretary = data["signatories"]["secretary"] or None
    sign_lines: list[tuple[Paragraph, list[list[Any]], str, dict[str, Any], dict[str, Any]]] = []

    prev_empty = False
    for item in layout["body"]:
        if item["type"] == "tbl":
            spec = item if blank else _with_number_column(item, layout)
            _build_table(doc, spec, layout, answers)
            continue
        text = "".join(t for t, _ in item["runs"])
        # В казахском бланке перед заключительной фразой стоит абзац из пяти пробелов —
        # след правки, не элемент формы; в собранном документе он лишь двоит отбивку.
        if not blank and text.strip() == "" and text and item.get("spacing"):
            continue
        if blank:
            _fill_paragraph(doc.add_paragraph(), item, None, layout)
            continue
        # Две пустые строки подряд (перед датой выдачи) в собранном документе — одна
        empty = text == "" and not item.get("spacing")
        if empty and prev_empty:
            continue
        prev_empty = empty
        if text == "" and item.get("spacing"):
            # Пустой абзац-распорка между заключением и подписями (15+15 pt отбивки и строка).
            # С реальными данными (тема повторяется в заключительной фразе, консультанты
            # в две строки) он выталкивает подписи и дату выдачи на вторую страницу;
            # зазор остаётся за счёт отбивки самой заключительной фразы.
            continue
        par = doc.add_paragraph()
        if MARKERS[lang] in text:
            _fill_paragraph(par, item, _closing_runs(reg, lang, item), layout)
            # В бланке абзацный отступ набран шестью пробелами (6 × 3 pt при TNR 12 pt)
            par.paragraph_format.first_line_indent = Pt(18)
            continue
        if text.startswith(DATE_MARKERS[lang]):
            when = _get(reg, "ethics.conclusion_date")
            runs = item["runs"]
            if when != PLACEHOLDER:  # дата выдачи известна — она заменяет «_____ 2026»
                runs = [[DATE_BLANK.sub(when, t), p] for t, p in runs]
            _fill_paragraph(par, item, runs, layout)
            continue
        sig = _signature_parts(item)
        if sig:
            label, tail, tail_props = sig
            _format_paragraph(par, item)
            sign_lines.append((par, label, tail, tail_props, item))
            continue
        _fill_paragraph(par, item, None, layout)

    # Подписи: метка полужирным, затем табуляция к общей позиции, чтобы линии подписи
    # обоих подписантов стояли на одной вертикали (в бланке это набрано пробелами).
    if sign_lines:
        widest = max(_measure_pt("".join(t for t, _ in label)) for _, label, *_ in sign_lines)
        stop = widest + 6 * 3.0  # шесть пробелов TNR 12 pt — как зазор в бланке
        overrides = (chair, secretary)  # порядок в бланке: председатель, затем секретарь
        for (par, label, tail, tail_props, _), override in zip(sign_lines, overrides):
            par.paragraph_format.tab_stops.add_tab_stop(Pt(stop))
            for t, p in label:
                _add_run(par, t, p, layout["default_pt"], layout["font"])
            name = override or tail.split("  ", 1)[1]
            _add_run(par, "\t" + "_" * 17 + "  " + name, tail_props, layout["default_pt"], layout["font"])

    doc.core_properties.author = ""
    doc.core_properties.title = "Заключение этической комиссии" if lang == "ru" else "Әдеп комиссиясының қорытындысы"
    out_docx.parent.mkdir(parents=True, exist_ok=True)
    doc.save(out_docx)


def to_pdf(docx_path: Path) -> Path:
    """Конвертировать через установленный MS Word и вернуть путь PDF."""
    from docx2pdf import convert
    pdf = docx_path.with_suffix(".pdf")
    convert(str(docx_path), str(pdf))
    return pdf


def count_pages(pdf: Path) -> int:
    """Число страниц PDF."""
    import pymupdf
    with pymupdf.open(pdf) as d:
        return d.page_count


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--only", choices=("ru", "kz"))
    ap.add_argument("--no-pdf", action="store_true")
    ap.add_argument("--blank", action="store_true", help="воспроизвести бланк дословно (для проверки)")
    ap.add_argument("--out", type=Path, default=HERE)
    args = ap.parse_args()

    layout = json.loads(LAYOUT.read_text(encoding="utf-8"))
    reg = tomllib.loads(REGISTRY.read_text(encoding="utf-8"))
    data = tomllib.loads(DATA.read_text(encoding="utf-8"))
    status = 0
    for lang in ("ru", "kz"):
        if args.only and lang != args.only:
            continue
        stem = ("BLANK_" if args.blank else "ETHICS_CONCLUSION_") + lang.upper()
        docx_path = args.out / f"{stem}.docx"
        build(lang, layout[lang], reg, data, docx_path, args.blank)
        line = f"{lang}: {docx_path}"
        if not args.no_pdf:
            pdf = to_pdf(docx_path)
            pages = count_pages(pdf)
            line += f"  ({pages} с.)"
            if pages != EXPECTED_PAGES and not args.blank:
                line += f"  ⚠ ожидалась {EXPECTED_PAGES}"
                status = 1
        print(line)
    return status


if __name__ == "__main__":
    sys.exit(main())
