#!/usr/bin/env python3
"""Section-by-section Kazakh style report for a dissertation .docx or text file.

Wraps :mod:`kk_style_check`: extracts paragraph text from a .docx without
external dependencies, splits it into the GOST structural sections (front
matter, KIRISPE, numbered chapters and their subsections, QORYTYNDY,
bibliography, appendices), runs the style heuristic over the whole document
and over each section, and writes a Markdown report.

Density is reported per 1000 Cyrillic word tokens, so tables of numbers and
Latin-script bibliography entries dilute rather than inflate it — read the
per-section table, not only the document total.

Usage:
    python kk_style_report.py FULL_DISSERTATION_KZ.docx -o report.md
    python kk_style_report.py chapter3.md -o report.md --context 4
"""

from __future__ import annotations

import argparse
import re
import sys
import zipfile
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from xml.etree import ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parent))

from kk_style_check import (  # noqa: E402
    MARKERS,
    Report,
    analyze,
    context_of,
    normalize,
)

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

# Top-level unnumbered sections of a GOST dissertation, in body order.
FRONT_ANCHORS = (
    "НОРМАТИВТІК СІЛТЕМЕЛЕР",
    "БЕЛГІЛЕУЛЕР МЕН ҚЫСҚАРТУЛАР",
    "АНЫҚТАМАЛАР",
    "КІРІСПЕ",
)
BACK_ANCHORS = ("ҚОРЫТЫНДЫ", "ПАЙДАЛАНЫЛҒАН ӘДЕБИЕТТЕР ТІЗІМІ")

CHAPTER_RE = re.compile(r"^(\d+)\s+[А-ЯЁӘҒҚҢӨҰҮҺІ][А-ЯЁӘҒҚҢӨҰҮҺІ\s,\-–—()]{6,}$")
# A subsection number is "N.M " followed by a capitalized Kazakh word. The
# capital letter is what separates a heading from a table cell such as
# "0.7247 ± 0.0180" or "3.2 сурет".
SUBSECTION_RE = re.compile(r"^(\d{1,2}\.\d{1,2})\s+[А-ЯЁӘҒҚҢӨҰҮҺІ].{3,120}$")
CHAPTER_SUMMARY_RE = re.compile(r"^(\d+)-бөлім бойынша қорытындылар$")
APPENDIX_RE = re.compile(r"^ҚОСЫМША\s+[А-ЯЁӘҒҚҢӨҰҮҺІ]\b")
FIGURE_TABLE_RE = re.compile(r"^\d+\.\d+\s*[-–—]?\s*(сурет|кесте)", re.IGNORECASE)

# Sections that are lists, formulas or Latin-script references rather than
# prose: reported, but excluded from the "prose corpus" totals.
NON_PROSE = re.compile(
    r"^(Титул және мазмұны|\(преамбула\)|НОРМАТИВТІК СІЛТЕМЕЛЕР"
    r"|БЕЛГІЛЕУЛЕР МЕН ҚЫСҚАРТУЛАР|АНЫҚТАМАЛАР"
    r"|ПАЙДАЛАНЫЛҒАН ӘДЕБИЕТТЕР ТІЗІМІ|ҚОСЫМША)"
)

DENSITY_WARN = 12.0   # markers/1000 words worth a second read
DENSITY_HIGH = 20.0   # markers/1000 words worth a rewrite pass
MIN_WORDS = 150       # below this a density figure is statistical noise
DOMINANT_SHARE = 0.08  # a stem above this share of all hits is likely a term


@dataclass
class Section:
    """One structural unit of the document.

    Args:
        title: Heading line as it appears in the document.
        level: 0 for unnumbered top sections, 1 for chapters, 2 for subsections.
        text: Body text of the section, heading excluded.
    """

    title: str
    level: int
    text: str


def extract_docx(path: Path) -> str:
    """Pull paragraph and table-cell text out of a .docx.

    Args:
        path: Path to the .docx file.

    Returns:
        Document text, one paragraph per line, in document order.
    """
    with zipfile.ZipFile(path) as archive:
        root = ET.fromstring(archive.read("word/document.xml"))
    body = root.find(f"{W}body")
    if body is None:
        return ""

    lines: list[str] = []
    for paragraph in body.iter(f"{W}p"):
        parts: list[str] = []
        for node in paragraph.iter():
            if node.tag == f"{W}t":
                parts.append(node.text or "")
            elif node.tag == f"{W}tab":
                parts.append("\t")
            elif node.tag in (f"{W}br", f"{W}cr"):
                parts.append("\n")
        text = "".join(parts).strip()
        if text:
            lines.append(text)
    return "\n".join(lines)


def load_text(path: Path) -> str:
    """Read a document as plain text.

    Args:
        path: A .docx file or any UTF-8 text file.

    Returns:
        The document's text content.
    """
    if path.suffix.lower() == ".docx":
        return extract_docx(path)
    return path.read_text(encoding="utf-8")


def strip_front_matter(lines: list[str]) -> tuple[list[str], list[str]]:
    """Separate the title page and table of contents from the body.

    The table of contents repeats every heading with a trailing page number,
    which would otherwise be counted as prose and would break sectioning.

    Args:
        lines: All document lines.

    Returns:
        Tuple of (front-matter lines, body lines).
    """
    for index, line in enumerate(lines):
        if line.strip() == FRONT_ANCHORS[0]:
            return lines[:index], lines[index:]
    return [], lines


def is_heading(line: str) -> tuple[int, str] | None:
    """Classify a line as a section heading.

    Args:
        line: A single stripped document line.

    Returns:
        Tuple of (level, title) if the line opens a section, else ``None``.
    """
    stripped = line.strip()
    if stripped in FRONT_ANCHORS or stripped in BACK_ANCHORS:
        return 0, stripped
    if APPENDIX_RE.match(stripped):
        return 0, stripped
    if CHAPTER_RE.match(stripped):
        return 1, stripped
    if CHAPTER_SUMMARY_RE.match(stripped):
        return 2, stripped
    if SUBSECTION_RE.match(stripped) and not FIGURE_TABLE_RE.match(stripped):
        return 2, stripped
    return None


def split_sections(text: str) -> tuple[list[Section], list[str]]:
    """Split document text into structural sections.

    Args:
        text: Full document text, one paragraph per line.

    Returns:
        Tuple of (sections in document order, front-matter lines).
    """
    lines = [line for line in text.splitlines() if line.strip()]
    front, body = strip_front_matter(lines)

    sections: list[Section] = []
    if front:
        sections.append(Section("Титул және мазмұны", 0, "\n".join(front)))

    current = Section("(преамбула)", 0, "")
    buffer: list[str] = []
    for line in body:
        heading = is_heading(line)
        if heading is not None:
            current.text = "\n".join(buffer)
            sections.append(current)
            level, title = heading
            current = Section(title, level, "")
            buffer = []
        else:
            buffer.append(line)
    current.text = "\n".join(buffer)
    sections.append(current)

    # Chapter headings are kept even when empty: in this layout a chapter
    # heading is immediately followed by its first subsection, and the row
    # still serves as a group separator in the report table.
    return [s for s in sections if s.text.strip() or s.level == 1], front


def flag(report: Report) -> str:
    """Severity marker for one section's density.

    Args:
        report: Analysis of the section.

    Returns:
        A short flag string.
    """
    if report.words < MIN_WORDS:
        return "—"
    if report.per_1000 >= DENSITY_HIGH:
        return "**жоғары**"
    if report.per_1000 >= DENSITY_WARN:
        return "назар аудару"
    return "қалыпты"


def render_markdown(
    source: Path,
    whole: Report,
    whole_norm: str,
    prose: Report,
    per_section: list[tuple[Section, Report, str]],
    top: int,
    context: int,
) -> str:
    """Build the Markdown report.

    Args:
        source: Path of the analyzed document.
        whole: Analysis of the entire document.
        whole_norm: Normalized text of the entire document.
        prose: Analysis of the prose-only corpus.
        per_section: Per-section (section, report, normalized text) triples.
        top: How many distinct markers to list document-wide.
        context: How many usage snippets to show per listed marker.

    Returns:
        The report as a Markdown string.
    """
    out: list[str] = [
        f"# Стилевой отчёт — {source.name}",
        "",
        f"- **Источник:** `{source}`",
        "- **Инструмент:** `thesis/scripts/kk_style_check.py` "
        "(обёртка `thesis/scripts/kk_style_report.py`)",
        f"- **Дата проверки:** {date.today().isoformat()}",
        "",
        "> Это **стилевая эвристика для казахского академического текста**, "
        "а не детектор водяных знаков и не доказательство авторства. "
        "Каждое число — повод перечитать абзац, а не вердикт.",
        "",
        "---",
        "",
        "## 1. Сводка",
        "",
        "| Корпус | Слов (кириллица) | Предложений | Маркеров | Плотность /1000 |",
        "|---|---:|---:|---:|---:|",
        f"| Весь документ | {whole.words} | {whole.sentences} | {len(whole.hits)} "
        f"| {whole.per_1000:.1f} |",
        "| Только проза (без титула, списков сокращений, литературы, приложений) "
        f"| {prose.words} | {prose.sentences} | {len(prose.hits)} | {prose.per_1000:.1f} |",
        "",
        f"Пороги, принятые в этом отчёте: < {DENSITY_WARN:.0f}/1000 — норма, "
        f"{DENSITY_WARN:.0f}–{DENSITY_HIGH:.0f} — «назар аудару» (перечитать), "
        f"≥ {DENSITY_HIGH:.0f} — «жоғары» (нужна правка). Разделы короче "
        f"{MIN_WORDS} слов не оцениваются — цифра там статистический шум.",
        "",
    ]

    by_category: dict[str, int] = {}
    for hit in prose.hits:
        by_category[hit.category] = by_category.get(hit.category, 0) + 1
    if by_category:
        out += [
            "### Категории маркеров (корпус прозы)",
            "",
            "| Категория | Совпадений | /1000 слов |",
            "|---|---:|---:|",
        ]
        for category, count in sorted(by_category.items(), key=lambda kv: -kv[1]):
            density = 1000.0 * count / prose.words if prose.words else 0.0
            out.append(f"| {category} | {count} | {density:.1f} |")
        out.append("")

    out += [
        "---",
        "",
        "## 2. По разделам",
        "",
        "| Раздел | Слов | Предл. | Маркеров | /1000 | Оценка |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for section, report, _ in per_section:
        indent = "&nbsp;&nbsp;" * section.level
        title = section.title if len(section.title) <= 70 else section.title[:67] + "…"
        if section.level == 1 and not report.words:
            out.append(f"| {indent}**{title}** | | | | | |")
            continue
        density = f"{report.per_1000:.1f}" if report.words >= MIN_WORDS else "—"
        out.append(
            f"| {indent}{title} | {report.words} | {report.sentences} "
            f"| {len(report.hits)} | {density} | {flag(report)} |"
        )
    out.append("")

    hot = [
        (section, report)
        for section, report, _ in per_section
        if report.words >= MIN_WORDS and report.per_1000 >= DENSITY_WARN
    ]
    hot.sort(key=lambda pair: -pair[1].per_1000)
    out += ["### Разделы, требующие перечитывания", ""]
    if hot:
        for section, report in hot:
            out.append(
                f"- **{section.title}** — {report.per_1000:.1f}/1000 "
                f"({len(report.hits)} маркеров на {report.words} слов)"
            )
    else:
        out.append(
            f"Ни один раздел не превысил порог {DENSITY_WARN:.0f} маркеров "
            "на 1000 слов."
        )
    out.append("")

    out += ["---", "", "## 3. Топ маркеров по всему тексту", ""]
    by_stem: dict[tuple[str, str], list] = {}
    for hit in whole.hits:
        by_stem.setdefault((hit.stem, hit.gloss), []).append(hit)
    for (stem, gloss), hits in sorted(by_stem.items(), key=lambda kv: -len(kv[1]))[:top]:
        label = f"`{stem}` ({gloss})" if gloss else f"`{stem}`"
        forms = ", ".join(sorted({hit.surface for hit in hits})[:6])
        out.append(f"**{len(hits)}× {label}** — формы: {forms}")
        out.append("")
        for hit in hits[:context]:
            out.append(f"  - {context_of(whole_norm, hit.position, 55)}")
        out.append("")

    dominant = [
        (stem, gloss, hits)
        for (stem, gloss), hits in by_stem.items()
        if whole.hits and len(hits) / len(whole.hits) >= DOMINANT_SHARE
    ]
    dominant.sort(key=lambda item: -len(item[2]))
    out += ["---", "", "## 4. Возможные ложные срабатывания", ""]
    if dominant:
        residual = len(whole.hits) - sum(len(hits) for _, _, hits in dominant)
        out += [
            "Эти основы дают непропорционально большую долю всех совпадений. "
            "В специальном тексте такая частота обычно означает не штамп, а "
            "термин: посмотрите контексты в разделе 3 и убедитесь, в каком "
            "значении слово употребляется, прежде чем править.",
            "",
            "| Основа | Совпадений | Доля всех маркеров |",
            "|---|---:|---:|",
        ]
        for stem, gloss, hits in dominant:
            share = 100.0 * len(hits) / len(whole.hits)
            label = f"`{stem}` ({gloss})" if gloss else f"`{stem}`"
            out.append(f"| {label} | {len(hits)} | {share:.0f}% |")
        adjusted = 1000.0 * residual / whole.words if whole.words else 0.0
        ignore_flags = " ".join(f"--ignore-stem {stem}" for stem, _, _ in dominant)
        out += [
            "",
            f"Без этих основ по всему документу остаётся {residual} маркеров — "
            f"{adjusted:.1f} на 1000 слов против {whole.per_1000:.1f}. "
            f"Пересчитать отчёт без них: `{ignore_flags}`.",
            "",
        ]
    else:
        out += [
            "Ни одна основа не даёт непропорционально большой доли совпадений "
            f"(порог — {DOMINANT_SHARE * 100:.0f}% всех маркеров).",
            "",
        ]

    out += [
        "---",
        "",
        "## 5. Структура текста",
        "",
        "| Метрика | Весь документ | Проза |",
        "|---|---:|---:|",
        "| Средняя длина предложения, слов "
        f"| {whole.structural.get('mean_sentence_words', 0)} "
        f"| {prose.structural.get('mean_sentence_words', 0)} |",
        f"| Разброс длин, CV | {whole.structural.get('length_cv', 0)} "
        f"| {prose.structural.get('length_cv', 0)} |",
        f"| Лексическое разнообразие, TTR | {whole.structural.get('ttr', 0)} "
        f"| {prose.structural.get('ttr', 0)} |",
        "",
    ]
    prose_cv = prose.structural.get("length_cv", 1.0)
    if prose_cv and prose_cv < 0.35:
        out.append(
            f"CV длин предложений в прозе — **{prose_cv}**, ниже 0.35: ритм "
            "подозрительно ровный. Стоит намеренно разбить часть длинных "
            "предложений и слить часть коротких."
        )
    else:
        out.append(
            f"CV длин предложений в прозе — {prose_cv} (порог 0.35): ритм "
            "неровный, признаков машинной равномерности нет."
        )
    out.append("")

    out += ["---", "", "## 6. Аномалии символов", ""]
    if whole.anomalies:
        out += ["| Аномалия | Вхождений |", "|---|---:|"]
        for label, count in sorted(whole.anomalies.items(), key=lambda kv: -kv[1]):
            out.append(f"| {label} | {count} |")
        out.append("")
        if "Латиница внутри кириллических слов" in whole.anomalies:
            out.append(
                "Латиница внутри кириллических слов чаще всего означает копипаст "
                "или соседство с англоязычными терминами и формулами. В тексте "
                "с латинскими терминами (ResNet, CLAHE, AUC) часть срабатываний "
                "ожидаема — проверьте выборочно."
            )
            out.append("")
    else:
        out.append("Невидимых символов и смешения алфавитов не обнаружено.")
        out.append("")

    out += [
        "---",
        "",
        "## 7. Как читать этот отчёт",
        "",
        "1. Начните с раздела 2 — он показывает, где плотность штампов выше "
        "средней по тексту. Правьте разделы сверху вниз по списку «требующие "
        "перечитывания».",
        "2. Раздел 3 показывает конкретные слова и контексты. Частый маркер не "
        "всегда плох: `тиімді`, `кешенді`, `механизм` могут быть точными "
        "терминами. Плохо, когда они стоят как оценочная вода "
        "(«маңызды рөл атқарады»).",
        "3. Связки-коннекторы (`сонымен қатар`, `осылайша`) — первый кандидат на "
        "вычёркивание: в большинстве случаев предложение читается лучше без них.",
        "4. Пассивные рамки (`жүзеге асырылады`, `қамтамасыз етіледі`) уместны в "
        "разделах методики; в обсуждении результатов они почти всегда заменяются "
        "активным глаголом с явным субъектом.",
        "",
        "Категории маркеров, заложенные в проверку: "
        + ", ".join(f"«{name}»" for name in MARKERS)
        + ", «Штампованные конструкции».",
        "",
    ]
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    """CLI entry point.

    Args:
        argv: Argument vector; defaults to ``sys.argv[1:]``.

    Returns:
        Process exit code, 0 on success.
    """
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("path", help=".docx или текстовый файл диссертации")
    parser.add_argument("-o", "--output", required=True, help="куда записать отчёт (.md)")
    parser.add_argument("--top", type=int, default=25, help="сколько маркеров показать")
    parser.add_argument("--context", type=int, default=3, help="примеров на маркер")
    parser.add_argument("--dump-text", help="сохранить извлечённый текст в файл")
    parser.add_argument(
        "--ignore-stem",
        action="append",
        default=[],
        metavar="ОСНОВА",
        help="не считать эту основу маркером (для терминов); можно повторять",
    )
    args = parser.parse_args(argv)

    ignored = {stem.lower() for stem in args.ignore_stem}

    def scan(text: str, label: str) -> Report:
        """Analyze a text, dropping hits for stems listed in ``--ignore-stem``.

        Args:
            text: Text to analyze.
            label: Source label for the resulting report.

        Returns:
            The analysis with ignored stems removed from its hit list.
        """
        report = analyze(text, label)
        if ignored:
            report.hits = [hit for hit in report.hits if hit.stem not in ignored]
        return report

    source = Path(args.path)
    text = load_text(source)
    if args.dump_text:
        Path(args.dump_text).write_text(text, encoding="utf-8")

    sections, _ = split_sections(text)
    per_section = [
        (section, scan(section.text, section.title), normalize(section.text))
        for section in sections
    ]
    prose_text = "\n".join(
        section.text for section in sections if not NON_PROSE.match(section.title)
    )

    whole = scan(text, source.name)
    prose = scan(prose_text, "проза")

    report = render_markdown(
        source, whole, normalize(text), prose, per_section, args.top, args.context
    )
    if ignored:
        report += (
            "\n> Из подсчёта исключены основы (`--ignore-stem`): "
            + ", ".join(f"`{stem}`" for stem in sorted(ignored))
            + ".\n"
        )
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(report, encoding="utf-8")

    print(f"Разделов: {len(sections)}")
    print(
        f"Весь документ: {whole.words} слов, {len(whole.hits)} маркеров, "
        f"{whole.per_1000:.1f}/1000"
    )
    print(
        f"Проза: {prose.words} слов, {len(prose.hits)} маркеров, "
        f"{prose.per_1000:.1f}/1000"
    )
    print(f"Отчёт: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
