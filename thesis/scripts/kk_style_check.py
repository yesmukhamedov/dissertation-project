#!/usr/bin/env python3
"""Heuristic style checker for Kazakh (Cyrillic) academic text.

Scans a text for lexical patterns that machine-generated Kazakh prose
over-produces: evaluative filler adjectives ("маңызды", "елеулі"), stock
discourse connectives ("сонымен қатар", "қорытындылай келе"), impersonal
passive verb frames ("жүзеге асырылады"), plus structural signals
(sentence-length uniformity, lexical diversity, invisible Unicode,
Cyrillic/Latin homoglyph mixing).

This is a STYLE heuristic, not a watermark detector and not proof of
authorship. Statistical watermarks (SynthID-Text style) are invisible to
frequency analysis and need the vendor's key. Treat every number here as a
prompt to reread a passage, never as a verdict.

Kazakh is agglutinative, so markers are matched as stems with a tolerated
suffix tail: "маңызды" also matches "маңыздылығының".

Usage:
    python kk_style_check.py chapter3.md
    python kk_style_check.py *.md --json > report.json
    cat text.txt | python kk_style_check.py -
    python kk_style_check.py chapter3.md --context --top 15
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

# Kazakh Cyrillic alphabet (lowercase), including the nine Kazakh-only letters.
KZ_LETTERS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяәғқңөұүһі"

# Latin characters visually identical to Cyrillic ones. Inside a Cyrillic word
# they are either sloppy copy-paste or deliberate evasion of text matching;
# either way worth reporting.
HOMOGLYPHS = {
    "a": "а", "c": "с", "e": "е", "o": "о", "p": "р", "x": "х", "y": "у",
    "A": "А", "B": "В", "C": "С", "E": "Е", "H": "Н", "K": "К", "M": "М",
    "O": "О", "P": "Р", "T": "Т", "X": "Х", "Y": "У",
    "i": "і", "I": "І",
}
LATIN_LOOKALIKES = "".join(HOMOGLYPHS)

# Zero-width and unusual-space characters. Not watermarks, but they betray
# machine assembly or an attempt to break string matching.
INVISIBLES = {
    " ": "NBSP",
    "­": "SOFT HYPHEN",
    "​": "ZERO WIDTH SPACE",
    "‌": "ZERO WIDTH NON-JOINER",
    "‍": "ZERO WIDTH JOINER",
    " ": "THIN SPACE",
    " ": "NARROW NBSP",
    "⁠": "WORD JOINER",
    "﻿": "BOM / ZWNBSP",
}

MAX_SUFFIX = 14  # longest agglutinative tail tolerated after a stem


@dataclass(frozen=True)
class Marker:
    """One lexical marker to look for.

    Args:
        stem: Lowercase stem or multi-word phrase (spaces match any whitespace).
        gloss: Short Russian gloss shown in the report.
        exact: If True the stem must be a whole word — used for short or
            ambiguous stems where a suffix tail would cause false positives.
        not_suffix: Suffix that turns the stem into a different lexeme rather
            than an inflected form of it. "үлес" + "тір" is "үлестірім"
            (распределение), not "вклад"; such a tail rejects the match.
    """

    stem: str
    gloss: str
    exact: bool = False
    not_suffix: str = ""


MARKERS: dict[str, list[Marker]] = {
    "Оценочные прилагательные": [
        Marker("маңызды", "важный"),
        Marker("елеулі", "значимый"),
        Marker("айтарлықтай", "существенный"),
        Marker("түбегейлі", "фундаментальный"),
        Marker("өзекті", "актуальный"),
        Marker("ерекше", "особый", not_suffix="лен"),  # ерекшелену = отличаться
        Marker("жан-жақты", "всесторонний"),
        Marker("кешенді", "комплексный"),
        Marker("ауқымды", "масштабный"),
        Marker("тиімді", "эффективный"),
        Marker("нәтижелі", "результативный"),
        Marker("сапалы", "качественный", not_suffix="қ"),  # сапалық = качественный (vs количественный)
        Marker("зор", "огромный", exact=True),
        Marker("терең", "глубокий", exact=True),
    ],
    "Абстрактные существительные": [
        Marker("рөл", "роль"),
        Marker("үлес", "вклад", not_suffix="тір"),  # үлестірім = распределение
        Marker("әлеует", "потенциал"),
        Marker("мүмкіндік", "возможность"),
        Marker("үдеріс", "процесс"),
        Marker("аспект", "аспект"),
        Marker("фактор", "фактор", not_suffix="лық"),  # факторлық жоспар = факторный план
        Marker("механизм", "механизм"),
        Marker("тұрғы", "ракурс / точка зрения", not_suffix="н"),  # тұрғын = житель
        Marker("маңыздылық", "важность"),
        Marker("тұжырымдама", "концепция"),
    ],
    "Штампованные глагольные рамки": [
        Marker("рөл атқарады", "играет роль"),
        Marker("рөл атқаруда", "играет роль"),
        Marker("үлес қосады", "вносит вклад"),
        Marker("қамтамасыз етеді", "обеспечивает"),
        Marker("ықпал етеді", "оказывает влияние"),
        Marker("жүзеге асырылады", "осуществляется"),
        Marker("жүзеге асыру", "осуществление"),
        Marker("назар аудару қажет", "необходимо обратить внимание"),
        Marker("атап өту керек", "следует отметить"),
        Marker("атап өткен жөн", "стоит отметить"),
        Marker("айта кету керек", "нужно сказать"),
        Marker("деп айтуға болады", "можно сказать"),
        Marker("деуге болады", "можно назвать"),
    ],
    "Связки-коннекторы": [
        Marker("сонымен қатар", "кроме того"),
        Marker("сондай-ақ", "а также"),
        Marker("бұдан басқа", "помимо этого"),
        Marker("осыған байланысты", "в связи с этим"),
        Marker("осылайша", "таким образом"),
        Marker("атап айтқанда", "а именно"),
        Marker("бір сөзбен айтқанда", "одним словом"),
        Marker("қорытындылай келе", "подводя итог"),
        Marker("қорыта айтқанда", "в заключение"),
        Marker("түйіндей келе", "резюмируя"),
        Marker("жоғарыда айтылғандай", "как сказано выше"),
    ],
    "Хеджи (смягчители)": [
        Marker("мүмкін", "возможно", exact=True),
        Marker("сияқты", "подобно", exact=True),
        Marker("әдетте", "обычно", exact=True),
        Marker("жалпы алғанда", "в целом"),
    ],
}

# "не только X, но и Y" — the Kazakh twin of the "it's not X, it's Y" tic.
PHRASE_PATTERNS: dict[str, re.Pattern[str]] = {
    "тек ... емес, сонымен қатар (не только … но и)": re.compile(
        r"тек\b.{0,80}?\bемес\s*,\s*(сонымен қатар|сондай-ақ|сол сияқты)",
        re.IGNORECASE | re.DOTALL,
    ),
    "бір жағынан ... екінші жағынан (с одной … с другой)": re.compile(
        r"бір жағынан\b.{0,200}?\bекінші жағынан", re.IGNORECASE | re.DOTALL
    ),
}


@dataclass
class Hit:
    """A single marker match.

    Args:
        category: Marker category name.
        stem: The marker stem that matched.
        gloss: Gloss of the marker.
        surface: The actual inflected form found in the text.
        position: Character offset of the match start in the normalized text.
        end: Character offset just past the match.
    """

    category: str
    stem: str
    gloss: str
    surface: str
    position: int
    end: int


@dataclass
class Report:
    """Full analysis of one text.

    Args:
        source: File name or "<stdin>".
        words: Token count (Cyrillic words only).
        sentences: Sentence count.
        hits: Every marker match found.
        structural: Structural metrics (sentence uniformity, TTR).
        anomalies: Invisible-character, homoglyph and dash counts.
    """

    source: str
    words: int
    sentences: int
    hits: list[Hit] = field(default_factory=list)
    structural: dict[str, float] = field(default_factory=dict)
    anomalies: dict[str, int] = field(default_factory=dict)

    @property
    def per_1000(self) -> float:
        """Marker density per 1000 words.

        Returns:
            Hits per 1000 word tokens, 0.0 for an empty text.
        """
        return 1000.0 * len(self.hits) / self.words if self.words else 0.0


def build_pattern(marker: Marker) -> re.Pattern[str]:
    """Compile a suffix-tolerant regex for one marker.

    Args:
        marker: The marker to compile.

    Returns:
        Compiled pattern matching the stem plus, unless ``exact``, up to
        ``MAX_SUFFIX`` trailing Kazakh letters (agglutinative endings), and
        rejecting the tail named by ``not_suffix``.
    """
    body = r"\s+".join(re.escape(part) for part in marker.stem.split())
    tail = "" if marker.exact else rf"[{KZ_LETTERS}\-]{{0,{MAX_SUFFIX}}}"
    block = rf"(?!{re.escape(marker.not_suffix)})" if marker.not_suffix else ""
    return re.compile(rf"(?<!\w){body}{block}{tail}(?!\w)", re.IGNORECASE)


COMPILED: list[tuple[str, Marker, re.Pattern[str]]] = [
    (category, marker, build_pattern(marker))
    for category, markers in MARKERS.items()
    for marker in markers
]

MIXED_SCRIPT = re.compile(
    rf"[{KZ_LETTERS}]+[{LATIN_LOOKALIKES}]|[{LATIN_LOOKALIKES}][{KZ_LETTERS}]+",
    re.IGNORECASE,
)


def scan_anomalies(text: str) -> dict[str, int]:
    """Count invisible characters, homoglyphs and long dashes in raw text.

    Args:
        text: Raw text, before normalization.

    Returns:
        Mapping of anomaly label to occurrence count; zero counts are omitted.
    """
    found: dict[str, int] = {}
    for char, label in INVISIBLES.items():
        count = text.count(char)
        if count:
            found[label] = count

    mixed = MIXED_SCRIPT.findall(text)
    if mixed:
        found["Латиница внутри кириллических слов"] = len(mixed)

    for char, label in (("—", "Em dash (—)"), ("–", "En dash (–)")):
        count = text.count(char)
        if count:
            found[label] = count
    return found


def normalize(text: str) -> str:
    """Normalize text for matching.

    Args:
        text: Raw input text.

    Returns:
        NFC-normalized lowercase text with Latin homoglyphs folded to Cyrillic
        and invisible characters neutralized, so markers are still found in
        obfuscated text.
    """
    text = unicodedata.normalize("NFC", text)
    for char in INVISIBLES:
        text = text.replace(char, "" if char == "­" else " ")
    for latin, cyrillic in HOMOGLYPHS.items():
        text = text.replace(latin, cyrillic)
    return text.lower()


def tokenize(text: str) -> list[str]:
    """Split normalized text into Cyrillic word tokens.

    Args:
        text: Normalized text.

    Returns:
        List of word tokens; digits and punctuation are dropped.
    """
    return re.findall(rf"[{KZ_LETTERS}]+(?:-[{KZ_LETTERS}]+)*", text)


def split_sentences(text: str) -> list[str]:
    """Split text into sentences.

    Args:
        text: Normalized text.

    Returns:
        Non-empty sentences, split on terminal punctuation and blank lines.
    """
    raw = re.split(r"[.!?…]+[\s\"»)]*|\n{2,}", text)
    return [chunk.strip() for chunk in raw if chunk.strip()]


def structural_stats(text: str, tokens: list[str]) -> tuple[dict[str, float], int]:
    """Compute sentence-rhythm and vocabulary metrics.

    Args:
        text: Normalized text.
        tokens: Word tokens of the same text.

    Returns:
        Tuple of (metrics mapping, sentence count). ``length_cv`` is the
        coefficient of variation of sentence length — low values mean an
        unusually even rhythm. ``ttr`` is the type-token ratio.
    """
    lengths = [len(tokenize(s)) for s in split_sentences(text)]
    lengths = [n for n in lengths if n]
    stats: dict[str, float] = {}
    if lengths:
        mean = statistics.fmean(lengths)
        stdev = statistics.pstdev(lengths) if len(lengths) > 1 else 0.0
        stats["mean_sentence_words"] = round(mean, 1)
        stats["length_cv"] = round(stdev / mean, 3) if mean else 0.0
    if tokens:
        stats["ttr"] = round(len(set(tokens)) / len(tokens), 3)
    return stats, len(lengths)


def analyze(text: str, source: str) -> Report:
    """Run the full analysis over one text.

    Args:
        text: Raw text to analyze.
        source: Label for the text (file name or "<stdin>").

    Returns:
        Populated :class:`Report`.
    """
    anomalies = scan_anomalies(text)
    norm = normalize(text)
    tokens = tokenize(norm)
    stats, n_sentences = structural_stats(norm, tokens)

    lexical: list[Hit] = []
    for category, marker, pattern in COMPILED:
        for match in pattern.finditer(norm):
            lexical.append(
                Hit(category, marker.stem, marker.gloss, match.group(0),
                    match.start(), match.end())
            )

    # Long-span constructions are counted alongside the words inside them, so
    # they take no part in the overlap resolution below.
    hits = dedupe(lexical)
    for label, pattern in PHRASE_PATTERNS.items():
        for match in pattern.finditer(norm):
            hits.append(
                Hit("Штампованные конструкции", label, "", match.group(0)[:60],
                    match.start(), match.end())
            )
    hits.sort(key=lambda hit: hit.position)

    return Report(source, len(tokens), n_sentences, hits, stats, anomalies)


def dedupe(hits: list[Hit]) -> list[Hit]:
    """Drop matches swallowed by a longer overlapping match.

    A phrase marker such as "рөл атқарады" also triggers the bare noun "рөл";
    counting both would inflate the density. The longest match at each span
    wins, and anything contained in an already-kept span is discarded.

    Args:
        hits: All raw matches, in any order.

    Returns:
        Surviving hits, sorted by position.
    """
    ordered = sorted(hits, key=lambda hit: (hit.position, -(hit.end - hit.position)))
    kept: list[Hit] = []
    covered_until = -1
    for hit in ordered:
        if hit.end <= covered_until:
            continue
        kept.append(hit)
        covered_until = max(covered_until, hit.end)
    return kept


def context_of(text: str, position: int, width: int = 40) -> str:
    """Extract a one-line snippet around a match.

    Args:
        text: Normalized text the position refers to.
        position: Character offset of the match.
        width: Characters of context on each side.

    Returns:
        Single-line snippet with surrounding whitespace collapsed.
    """
    start, end = max(0, position - width), min(len(text), position + width)
    return "…" + re.sub(r"\s+", " ", text[start:end]).strip() + "…"


def render(report: Report, norm_text: str, top: int, show_context: bool) -> str:
    """Format a report as plain text.

    Args:
        report: The analysis to render.
        norm_text: Normalized text, used for context snippets.
        top: How many distinct markers to list.
        show_context: Whether to print snippets for each listed marker.

    Returns:
        Multi-line report string.
    """
    out: list[str] = [
        f"=== {report.source} ===",
        f"Слов: {report.words}   Предложений: {report.sentences}   "
        f"Маркеров: {len(report.hits)}   Плотность: {report.per_1000:.1f} / 1000 слов",
    ]

    by_category: dict[str, int] = {}
    by_stem: dict[tuple[str, str], list[Hit]] = {}
    for hit in report.hits:
        by_category[hit.category] = by_category.get(hit.category, 0) + 1
        by_stem.setdefault((hit.stem, hit.gloss), []).append(hit)

    if by_category:
        out.append("\nПо категориям:")
        for category, count in sorted(by_category.items(), key=lambda kv: -kv[1]):
            density = 1000.0 * count / report.words if report.words else 0.0
            out.append(f"  {count:>4}  ({density:5.1f}/1000)  {category}")

    if by_stem:
        out.append("\nТоп маркеров:")
        for (stem, gloss), hits in sorted(by_stem.items(), key=lambda kv: -len(kv[1]))[:top]:
            forms = ", ".join(sorted({hit.surface for hit in hits})[:4])
            label = f"{stem} ({gloss})" if gloss else stem
            out.append(f"  {len(hits):>4}  {label}  —  формы: {forms}")
            if show_context:
                for hit in hits[:3]:
                    out.append(f"        {context_of(norm_text, hit.position)}")

    if report.structural:
        out.append("\nСтруктура:")
        out.append(
            f"  Средняя длина предложения: "
            f"{report.structural.get('mean_sentence_words', 0)} слов"
        )
        cv = report.structural.get("length_cv")
        if cv is not None:
            note = "   ← подозрительно ровный ритм" if cv < 0.35 else ""
            out.append(f"  Разброс длин (CV): {cv}{note}")
        if "ttr" in report.structural:
            out.append(f"  Лексическое разнообразие (TTR): {report.structural['ttr']}")

    if report.anomalies:
        out.append("\nАномалии символов:")
        for label, count in sorted(report.anomalies.items(), key=lambda kv: -kv[1]):
            out.append(f"  {count:>4}  {label}")

    out.append(
        "\nЭто стилевая эвристика, а не детектор водяных знаков "
        "и не доказательство авторства."
    )
    return "\n".join(out)


def to_json(report: Report) -> dict[str, object]:
    """Convert a report to a JSON-serializable mapping.

    Args:
        report: The analysis to serialize.

    Returns:
        Nested dict with counts, densities, metrics and every hit.
    """
    return {
        "source": report.source,
        "words": report.words,
        "sentences": report.sentences,
        "markers": len(report.hits),
        "per_1000": round(report.per_1000, 2),
        "by_category": {
            category: sum(1 for hit in report.hits if hit.category == category)
            for category in list(MARKERS) + ["Штампованные конструкции"]
        },
        "structural": report.structural,
        "anomalies": report.anomalies,
        "hits": [
            {
                "stem": hit.stem,
                "surface": hit.surface,
                "category": hit.category,
                "position": hit.position,
            }
            for hit in report.hits
        ],
    }


def main(argv: list[str] | None = None) -> int:
    """CLI entry point.

    Args:
        argv: Argument vector; defaults to ``sys.argv[1:]``.

    Returns:
        Process exit code: 1 if any file exceeds ``--fail-over`` density, else 0.
    """
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("paths", nargs="+", help="файлы для проверки, или - для stdin")
    parser.add_argument("--top", type=int, default=20, help="сколько маркеров показать")
    parser.add_argument("--context", action="store_true", help="показать примеры употребления")
    parser.add_argument("--json", action="store_true", help="машиночитаемый вывод")
    parser.add_argument(
        "--fail-over",
        type=float,
        default=None,
        help="ненулевой код возврата, если плотность выше порога (на 1000 слов)",
    )
    args = parser.parse_args(argv)

    reports: list[tuple[Report, str]] = []
    for raw_path in args.paths:
        if raw_path == "-":
            text, source = sys.stdin.read(), "<stdin>"
        else:
            path = Path(raw_path)
            if not path.is_file():
                print(f"пропущено (не файл): {path}", file=sys.stderr)
                continue
            text, source = path.read_text(encoding="utf-8"), path.name
        reports.append((analyze(text, source), normalize(text)))

    if not reports:
        print("нет файлов для анализа", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps([to_json(r) for r, _ in reports], ensure_ascii=False, indent=2))
    else:
        print("\n\n".join(render(r, n, args.top, args.context) for r, n in reports))

    if args.fail_over is not None and any(r.per_1000 > args.fail_over for r, _ in reports):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
