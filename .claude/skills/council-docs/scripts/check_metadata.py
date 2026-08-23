"""Check every council/defense document against the single metadata registry.

The registry is `council/METADATA.toml` — the only place where names, positions,
the department, the programme code, the dissertation titles, the volume figures
and the publication list are allowed to live. Documents must reproduce those
values verbatim; this script is what makes "verbatim" verifiable.

Three checks run over the deliverables:

1. **forbidden** — strings recorded in `[check.forbidden]` (each one was a real
   defect at some point: a wrong patronymic, a superseded Kazakh title, the
   "assistant professor" variant) must not reappear anywhere.
2. **required** — each document must contain the canonical form of every field
   it is supposed to carry (map `REQUIRED` below). Comparison normalises dash
   and quote variants, non-breaking spaces and runs of whitespace, so a document
   is not flagged for typography — only for a different value.
3. **missing** — registry fields left empty, with the document that needs them.

Usage:
    python check_metadata.py            # full report, exit 1 if anything failed
    python check_metadata.py --quiet    # only failures
"""
from __future__ import annotations

import argparse
import re
import sys
import tomllib
from pathlib import Path

_HERE = Path(__file__).resolve().parent
ROOT = _HERE
while ROOT.parent != ROOT and not (ROOT / "defense").is_dir():
    ROOT = ROOT.parent

REGISTRY = ROOT / "council/METADATA.toml"

# Documents scanned for forbidden strings (globs, relative to ROOT).
SCAN_GLOBS = [
    "thesis/output/*.md",
    "council/*.md",
    "council/en/**/*.md",
    "council/ru/**/*.md",
    "defense/presentation/slides/*.md",
    "defense/presentation/*.md",
]

# Templates in council/en and council/ru are deliberately anonymised (they carry
# `<Фамилия И.О.>` placeholders and the full 8D061XX programme list), so the
# forbidden-string scan skips the two entries that legitimately appear there.
TEMPLATE_EXEMPT = {"8D06101", "International University of Information Technology"}

# Which canonical values each deliverable must carry.
# Keys are dotted paths into the registry; `pub:N` means publication N's DOI.
REQUIRED: dict[str, list[str]] = {
    "thesis/output/titlepage_en.md": [
        "organization.name_en", "dissertation.udc", "candidate.name_upper_en",
        "dissertation.title_en", "programme.code", "programme.name_en",
        "supervisor.short_en", "foreign_consultant.short_en",
    ],
    "thesis/output/titlepage_kz.md": [
        "organization.name_kz", "dissertation.udc", "candidate.name_upper_kz",
        "dissertation.title_kz", "programme.code", "programme.name_kz",
        "supervisor.short_kz", "foreign_consultant.short_en",
    ],
    "thesis/output/abstract_en.md": [
        "candidate.name_en", "dissertation.title_en",
        "programme.code", "programme.name_en",
        "pub:1", "pub:2", "pub:3", "pub:4", "pub:5",
    ],
    "thesis/output/abstract_ru.md": [
        "candidate.name_ru_gen", "dissertation.title_ru",
        "programme.code", "programme.name_ru",
        "pub:1", "pub:2", "pub:3", "pub:4", "pub:5",
    ],
    "thesis/output/abstract_kz.md": [
        "candidate.name_kz_gen", "dissertation.title_kz",
        "programme.code", "programme.name_kz",
        "pub:1", "pub:2", "pub:3", "pub:4", "pub:5",
    ],
    "thesis/output/publications_list_ru.md": [
        "candidate.position_ru_gen", "candidate.name_ru_gen", "candidate.short_ru",
        "programme.code", "programme.name_ru",
        "organization.academic_secretary_short_ru",
        "pub:1", "pub:2", "pub:3", "pub:4", "pub:5",
    ],
    "thesis/output/supervisor_review_kz.md": [
        "candidate.name_kz_gen", "dissertation.title_kz",
        "programme.code", "programme.name_kz",
        "supervisor.short_kz", "supervisor.degree_kz", "supervisor.title_kz",
        "organization.name_kz",
    ],
    "thesis/output/foreign_consultant_review_en.md": [
        "candidate.name_en", "dissertation.title_en",
        "programme.code", "programme.name_en",
        "foreign_consultant.name_en", "foreign_consultant.title_en",
        "foreign_consultant.department_en", "foreign_consultant.faculty_en",
        "foreign_consultant.org_en", "foreign_consultant.address_en",
    ],
    "thesis/output/official_reviewer_1_review_en.md": [
        "candidate.name_en", "dissertation.title_en",
        "programme.code", "programme.name_en",
        "official_reviewer_1.name_en", "official_reviewer_1.degree_en",
        "official_reviewer_1.title_en", "official_reviewer_1.department_en",
        "official_reviewer_1.org_en",
    ],
    "thesis/output/official_reviewer_1_review_ru.md": [
        "candidate.name_ru_gen", "dissertation.title_ru",
        "programme.code", "programme.name_ru",
        "official_reviewer_1.name_ru", "official_reviewer_1.degree_ru",
        "official_reviewer_1.title_ru", "official_reviewer_1.department_ru",
        "official_reviewer_1.org_ru",
    ],
    "thesis/output/official_reviewer_1_review_kz.md": [
        "candidate.name_kz_gen", "dissertation.title_kz",
        "programme.code", "programme.name_kz",
        "official_reviewer_1.name_kz", "official_reviewer_1.degree_kz",
        "official_reviewer_1.title_kz", "official_reviewer_1.department_kz",
        "official_reviewer_1.org_kz",
    ],
    "thesis/output/official_reviewer_2_review_en.md": [
        "candidate.name_en", "dissertation.title_en",
        "programme.code", "programme.name_en",
        "official_reviewer_2.name_en", "official_reviewer_2.degree_en",
        "official_reviewer_2.title_en", "official_reviewer_2.position_en",
        "official_reviewer_2.org_en",
    ],
    "thesis/output/official_reviewer_2_review_ru.md": [
        "candidate.name_ru_gen", "dissertation.title_ru",
        "programme.code", "programme.name_ru",
        "official_reviewer_2.name_ru", "official_reviewer_2.degree_ru",
        "official_reviewer_2.title_ru", "official_reviewer_2.position_ru",
        "official_reviewer_2.org_ru",
    ],
    "thesis/output/official_reviewer_2_review_kz.md": [
        "candidate.name_kz_gen", "dissertation.title_kz",
        "programme.code", "programme.name_kz",
        "official_reviewer_2.name_kz", "official_reviewer_2.degree_kz",
        "official_reviewer_2.title_kz", "official_reviewer_2.department_kz",
        "official_reviewer_2.org_kz",
    ],
    "defense/presentation/slides/01_TITLE.md": [
        "organization.name_en", "dissertation.title_kz",
        "candidate.name_kz", "supervisor.name_kz",
        "supervisor.degree_kz", "supervisor.title_kz",
    ],
    "defense/presentation/slides/49_FINAL.md": [
        "organization.name_en", "dissertation.title_kz", "candidate.name_kz",
    ],
}

# Registry fields that must not be empty for the run to pass. Everything else in
# [missing] is reported as an open item rather than an error, because the defense
# date, the protocol number and the candidate's personal data arrive later.
BLOCKING_EMPTY: set[str] = set()

_DASHES = dict.fromkeys(map(ord, "‐‑‒–—―−"), "-")
_QUOTES = {
    ord("«"): '"', ord("»"): '"', ord("„"): '"', ord("“"): '"', ord("”"): '"',
    ord("‘"): "'", ord("’"): "'",
}


def normalise(text: str) -> str:
    """Fold typography that legitimately varies between documents."""
    text = text.translate(_DASHES).translate(_QUOTES)
    text = text.replace(" ", " ").replace(" ", " ").replace("﻿", "")
    # Emphasis markers are markup, not text. A registry value may be split by
    # them in the source — the abstract masthead sets each of its centred lines
    # bold on its own, so the topic runs across two `**...**` spans — and the
    # value is still carried correctly. Dropping them also stops a forbidden
    # form from hiding behind a bold run in the middle of a word.
    text = text.replace("**", "")
    return re.sub(r"\s+", " ", text)


def load_registry() -> dict:
    with REGISTRY.open("rb") as fh:
        return tomllib.load(fh)


def resolve(reg: dict, path: str) -> str:
    """Look up a dotted registry path, or `pub:N[.field]` for publication N.

    `pub:N` yields the DOI, which is what the document scan compares against;
    `pub:N.field` reaches any other key of that publication, so a gap such as a
    missing page range can be tracked in [missing] like any other field.
    """
    if path.startswith("pub:"):
        spec = path.split(":", 1)[1]
        num_str, _, field = spec.partition(".")
        num = int(num_str)
        for item in reg["publications"]["items"]:
            if item["num"] == num:
                return str(item[field]) if field else item["doi"]
        raise KeyError(f"publication {num} not in registry")
    node = reg
    for part in path.split("."):
        node = node[part]
    return str(node)


def iter_files() -> list[Path]:
    seen: dict[Path, None] = {}
    for pattern in SCAN_GLOBS:
        for path in sorted(ROOT.glob(pattern)):
            if path.is_file():
                seen[path] = None
    return list(seen)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def check_forbidden(reg: dict, files: list[Path]) -> list[str]:
    check = reg.get("check", {})
    forbidden = check.get("forbidden", {})
    exempt = set(check.get("exempt_files", []))
    problems = []
    for path in files:
        if rel(path) in exempt:
            continue
        is_template = rel(path).startswith(("council/en/", "council/ru/"))
        text = path.read_text(encoding="utf-8", errors="replace")
        flat = normalise(text)
        for needle, why in forbidden.items():
            if is_template and needle in TEMPLATE_EXEMPT:
                continue
            if normalise(needle) in flat:
                line = next(
                    (i for i, ln in enumerate(text.splitlines(), 1)
                     if normalise(needle) in normalise(ln)),
                    0,
                )
                problems.append(f"{rel(path)}:{line}  «{needle}» — {why}")
    return problems


def check_required(reg: dict) -> tuple[list[str], list[str]]:
    problems, skipped = [], []
    for doc, fields in REQUIRED.items():
        path = ROOT / doc
        if not path.is_file():
            problems.append(f"{doc} — файл не найден")
            continue
        flat = normalise(path.read_text(encoding="utf-8", errors="replace"))
        for field in fields:
            value = resolve(reg, field)
            if not value:
                skipped.append(f"{doc} — {field} пусто в реестре, проверить нечем")
                continue
            if normalise(value) not in flat:
                problems.append(f"{doc} — нет канонического значения {field}: «{value}»")
    return problems, skipped


def check_empty(reg: dict) -> tuple[list[str], list[str]]:
    """Split the registry's [missing] map into blocking and open items."""
    blocking, open_items = [], []
    for field, where in reg.get("missing", {}).items():
        try:
            value = resolve(reg, field)
        except KeyError:
            blocking.append(f"{field} — записано в [missing], но такого поля в реестре нет")
            continue
        if value:
            continue
        (blocking if field in BLOCKING_EMPTY else open_items).append(f"{field} — нужно для: {where}")
    return blocking, open_items


def main() -> int:
    ap = argparse.ArgumentParser(description="Check documents against council/METADATA.toml")
    ap.add_argument("--quiet", action="store_true", help="print failures only")
    args = ap.parse_args()

    reg = load_registry()
    files = iter_files()
    forbidden = check_forbidden(reg, files)
    required, skipped = check_required(reg)
    blocking, open_items = check_empty(reg)

    if not args.quiet:
        print(f"[reg ] {rel(REGISTRY)} (schema {reg['schema_version']}, updated {reg['updated']})")
        print(f"[scan] {len(files)} файлов, {len(REQUIRED)} документов со сверкой значений")

    failed = forbidden or required or blocking

    if forbidden:
        print(f"\nЗАПРЕЩЁННЫЕ ФОРМЫ ({len(forbidden)}):")
        for item in forbidden:
            print("  ✗", item)
    if required:
        print(f"\nРАСХОЖДЕНИЯ С РЕЕСТРОМ ({len(required)}):")
        for item in required:
            print("  ✗", item)
    if blocking:
        print(f"\nПУСТЫЕ ОБЯЗАТЕЛЬНЫЕ ПОЛЯ ({len(blocking)}):")
        for item in blocking:
            print("  ✗", item)

    if not args.quiet:
        if skipped:
            print(f"\nНЕ ПРОВЕРЕНО — значение ещё не задано ({len(skipped)}):")
            for item in skipped:
                print("  ·", item)
        if open_items:
            print(f"\nОСТАЛОСЬ ЗАПОЛНИТЬ В РЕЕСТРЕ ({len(open_items)}):")
            for item in open_items:
                print("  ·", item)
        if not failed:
            print("\nOK — документы согласованы с реестром.")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
