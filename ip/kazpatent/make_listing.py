"""Build the source-code listing submitted to NIIS with the copyright application.

The Rules require the application to carry the program's source text. This walks the
registered scope (demo/ + experiments/) and emits one UTF-8 listing with a title block,
a file inventory and the code itself. Page counts come from make_pdf.py, which lays the
listing out for real — do not estimate them here.

Usage (from the repo root):
    python ip/kazpatent/make_listing.py            # full listing
    python ip/kazpatent/make_listing.py --core     # curated core modules only
    python ip/kazpatent/make_listing.py --head 25 --tail 25   # first/last N pages
"""

from __future__ import annotations

import argparse
import textwrap
from datetime import date
from pathlib import Path

# Must match, word for word, the Name field of the portal application and п. 1 of the
# abstract — the submission checklist is explicit that all three have to agree.
PROGRAM_NAME = (
    "Программный комплекс автоматизированной диагностики диабетической ретинопатии "
    "по изображениям глазного дна на основе конвейера предобработки изображений "
    "и свёрточной нейронной сети"
)

REPO = Path(__file__).resolve().parents[2]
OUT_DIR = Path(__file__).resolve().parent / "build"

LINES_PER_PAGE = 50

EXTENSIONS = {".py", ".js", ".jsx", ".css", ".yaml", ".yml", ".ps1"}

EXCLUDE_PARTS = {
    ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache", ".wrangler",
    "build", "dist", "outputs", "logs", "data", ".git", "checkpoints",
}

# Roots walked in order; the listing follows this order.
ROOTS = [
    Path("demo/server/app"),
    Path("demo/server/__version__.py"),
    Path("demo/web/src"),
    Path("experiments/src"),
    Path("experiments/run_experiment.py"),
    Path("experiments/od_fovea_detector"),
]

# --core: the modules that carry the claimed method, without the dashboard chrome.
CORE = [
    Path("experiments/src/preprocessing"),
    Path("experiments/src/models"),
    Path("experiments/src/training"),
    Path("experiments/src/explainability"),
    Path("demo/server/app"),
]


def is_excluded(path: Path) -> bool:
    """Return True when any path component is a build/vendor directory."""
    return any(part in EXCLUDE_PARTS for part in path.parts)


def collect(roots: list[Path]) -> list[Path]:
    """Collect repo-relative source files under the given roots, in root order."""
    files: list[Path] = []
    for root in roots:
        absolute = REPO / root
        if absolute.is_file():
            if absolute.suffix in EXTENSIONS:
                files.append(root)
            continue
        if not absolute.is_dir():
            continue
        for candidate in sorted(absolute.rglob("*")):
            if not candidate.is_file() or candidate.suffix not in EXTENSIONS:
                continue
            relative = candidate.relative_to(REPO)
            if is_excluded(relative):
                continue
            files.append(relative)
    return files


def render(files: list[Path], title: str) -> tuple[str, int]:
    """Render the listing text and return it with its total line count."""
    body: list[str] = []
    total = 0
    for relative in files:
        text = (REPO / relative).read_text(encoding="utf-8", errors="replace")
        lines = text.splitlines()
        total += len(lines)
        body.append("")
        body.append("=" * 78)
        body.append(f"ФАЙЛ: {relative.as_posix()}    ({len(lines)} строк)")
        body.append("=" * 78)
        body.extend(lines)

    inventory = [f"{i + 1:>4}. {p.as_posix()}" for i, p in enumerate(files)]
    header = [
        title,
        "",
        "Название программы:",
        *textwrap.wrap(PROGRAM_NAME, width=78),
        "",
        "Автор: Есмухамедов Нурмаганбет Сейткалиулы",
        f"Дата формирования листинга: {date.today().strftime('%d.%m.%Y')}",
        f"Файлов: {len(files)}    Строк исходного текста: {total}",
        "",
        "ПЕРЕЧЕНЬ ФАЙЛОВ",
        "-" * 78,
        *inventory,
        "",
        "ИСХОДНЫЙ ТЕКСТ",
    ]
    return "\n".join(header + body) + "\n", total


def clip(text: str, head_pages: int, tail_pages: int) -> str:
    """Keep the first and last N pages of the listing, marking the omission."""
    lines = text.splitlines()
    head = head_pages * LINES_PER_PAGE
    tail = tail_pages * LINES_PER_PAGE
    if len(lines) <= head + tail:
        return text
    omitted = len(lines) - head - tail
    marker = [
        "",
        "=" * 78,
        f"[ ОПУЩЕНО {omitted} строк исходного текста ]",
        "=" * 78,
        "",
    ]
    return "\n".join(lines[:head] + marker + lines[-tail:]) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--core", action="store_true", help="core modules only")
    parser.add_argument("--head", type=int, default=0, help="keep first N pages")
    parser.add_argument("--tail", type=int, default=0, help="keep last N pages")
    args = parser.parse_args()

    roots = CORE if args.core else ROOTS
    title = (
        "ЛИСТИНГ ИСХОДНОГО ТЕКСТА ПРОГРАММЫ (основные модули)"
        if args.core
        else "ЛИСТИНГ ИСХОДНОГО ТЕКСТА ПРОГРАММЫ (полный)"
    )

    files = collect(roots)
    text, total = render(files, title)
    if args.head or args.tail:
        text = clip(text, args.head, args.tail)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    suffix = "core" if args.core else "full"
    if args.head or args.tail:
        suffix += f"_{args.head}+{args.tail}p"
    out = OUT_DIR / f"listing_{suffix}.txt"
    out.write_text(text, encoding="utf-8")

    print(f"Файлов: {len(files)}")
    print(f"Строк: {total}  (~{-(-total // LINES_PER_PAGE)} страниц)")
    print(f"Записано: {out}")


if __name__ == "__main__":
    main()
