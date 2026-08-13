"""Build all council deliverables from thesis/output/*.md into GOST .docx + .pdf.

Discovers the known council source documents (abstracts + reviews) under
thesis/output/ and renders each to <out_dir>/<name>.docx and .pdf. Documents
listed in SUBDIRS land in a sub-folder of <out_dir> instead (the trilingual
abstracts in <out_dir>/abstracts/, the two reviews in <out_dir>/reviews/).

Usage:
    python build_all.py [--src DIR] [--out DIR] [--no-pdf] [--only NAME ...]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import md2gost

# Council source documents living in thesis/output/ (stem -> human label).
DOCS = {
    "abstract_en": "Abstract (English)",
    "abstract_ru": "Abstract (Russian)",
    "abstract_kz": "Abstract (Kazakh)",
    "supervisor_review_kz": "Supervisor review (Kazakh)",
    "foreign_consultant_review_en": "Foreign consultant review (English)",
}

# Stems collected into a sub-folder of the output directory (stem -> sub-folder).
SUBDIRS = {
    "abstract_en": "abstracts",
    "abstract_ru": "abstracts",
    "abstract_kz": "abstracts",
    "supervisor_review_kz": "reviews",
    "foreign_consultant_review_en": "reviews",
}


def main() -> None:
    repo = Path(__file__).resolve().parents[4]
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--src", type=Path, default=repo / "thesis" / "output")
    ap.add_argument("--out", type=Path, default=repo / "defense" / "docs")
    ap.add_argument("--no-pdf", action="store_true", help="skip PDF rendering")
    ap.add_argument("--only", nargs="*", default=None, help="build only these stems")
    args = ap.parse_args()

    stems = args.only or list(DOCS)
    built: list[Path] = []
    missing: list[str] = []

    for stem in stems:
        md = args.src / f"{stem}.md"
        if not md.exists():
            missing.append(stem)
            continue
        docx = args.out / SUBDIRS.get(stem, "") / f"{stem}.docx"
        md2gost.convert(md, docx)
        print(f"[docx] {DOCS.get(stem, stem):40s} -> {docx}")
        built.append(docx)

    if not args.no_pdf and built:
        from docx2pdf import convert as to_pdf

        # Convert per folder rather than per file (fewer Word round-trips);
        # docx2pdf does not recurse, so every folder that got a build is listed.
        for folder in dict.fromkeys(docx.parent for docx in built):
            to_pdf(str(folder))
        for docx in built:
            print(f"[pdf ] {docx.with_suffix('.pdf')}")

    if missing:
        print(f"\nWARNING: missing sources: {', '.join(missing)}", file=sys.stderr)

    print(f"\nDone. {len(built)} document(s) -> {args.out}")


if __name__ == "__main__":
    main()
