---
name: council-docs
description: Convert dissertation-council Markdown documents (abstracts, supervisor/foreign-consultant reviews) from thesis/output/ into GOST-formatted .docx and .pdf, following the templates and formatting rules in council/en/. Use whenever the user asks to export, render, or produce council deliverables as Word/PDF.
---

# council-docs — GOST .docx / .pdf export

Render the council Markdown sources in `thesis/output/` into Word and PDF
deliverables (output to `defense/docs/`) that satisfy the IITU/HAC GOST formatting rules.

## Authoritative references (read before editing output)

- Formatting: `council/en/02-formatting/gost-formatting.md`
- Abstract/annotation structure: `council/en/11-abstract-annotation/structure.md`
- Supervisor (domestic consultant) review: `council/en/13-supervisor-review/structure.md`
- Foreign consultant review: `council/en/14-foreign-consultant-review/structure.md`

## GOST parameters enforced by the converter

- A4, text on one side, single (1.0) line spacing.
- Times New Roman 14 pt (applied to Latin **and** Cyrillic ranges).
- Margins: left 30 mm, right 10 mm, top 20 mm, bottom 20 mm.
- Page numbers centered at the bottom; **not printed on the first page**.
- Justified body text, 1.25 cm first-line indent; bold headings (no dot).

## How to run

Requirements: `python-docx` and `docx2pdf` (PDF step drives installed MS Word).

Build everything (abstracts EN/RU/KZ + both reviews) to `defense/docs/` — the
three abstracts are collected in `defense/docs/abstracts/`, the two reviews in
`defense/docs/reviews/`:

```powershell
python .claude/skills/council-docs/scripts/build_all.py
```

Useful flags:

- `--no-pdf` — produce only .docx (no Word needed).
- `--only abstract_en foreign_consultant_review_en` — build a subset.
- `--out DIR` / `--src DIR` — override locations.

Single file (any Markdown):

```powershell
python .claude/skills/council-docs/scripts/md2gost.py thesis/output/abstract_en.md --pdf
```

## Source documents

| Stem (in thesis/output/) | Document | Template | Output |
|---|---|---|---|
| `abstract_en` / `abstract_ru` / `abstract_kz` | Trilingual abstract/annotation | 11-abstract-annotation | `defense/docs/abstracts/` |
| `supervisor_review_kz` | Supervisor (domestic) review | 13-supervisor-review | `defense/docs/reviews/` |
| `foreign_consultant_review_en` | Foreign consultant review | 14-foreign-consultant-review | `defense/docs/reviews/` |

The routing lives in `SUBDIRS` in `build_all.py`; `--out DIR` moves the whole
tree, sub-folders included.

## Layout of `defense/docs/`

The two assembled manuscripts stay at the top level; everything that feeds them
is grouped beside them:

```
defense/docs/
├── DISSERTATION_{EN,KZ}_GOST_<date>.docx/.pdf       manuscript body
├── FULL_DISSERTATION_{EN,KZ}_GOST_<date>.docx/.pdf  front matter + body
├── abstracts/     abstract_{en,ru,kz}                       build_all.py
├── front_matter/  TITLE_PAGE, TABLE_OF_CONTENTS,            build_title.py,
│                  NORMATIVE_REFERENCES, DEFINITIONS,        build_toc.py,
│                  DESIGNATIONS_AND_ABBREVIATIONS,           build_frontmatter*.py
│                  FRONT_MATTER (the assembled bundle)
└── reviews/       supervisor_review_kz,                     build_all.py
                   foreign_consultant_review_en
```

The date-stamp discovery in the builders globs `DISSERTATION_EN_GOST_*.docx` at
the **top level** of `defense/docs/` — keep the manuscripts there.

## Version-marker scrubbing (thesis/ boundary)

Deliverables land in `defense/docs/` — **outside `thesis/`**, where no version
marker may appear. `convert(...)` therefore strips version markers from the text
before rendering (`strip_version_markers()` in `md2gost.py`, on by default):
`(V5)` parentheticals, bare tokens (`V5`, `v5.2`, `V4`, `V3`), and word forms
(`version 5.x`, `версия 5`, `нұсқа 5`). The pipeline reads as "the pipeline" /
"8-stage pipeline" / "конвейер" in the output. **`V5` is a version marker** (fifth
version) and is scrubbed too — the source `thesis/output/*.md` keeps it, the
export does not. See `PROJECT_MEMORY/strip-version-markers.md`.

## Notes / limitations

- Markdown handled: `#`–`####` headings, `**bold**`, `*italic*`, `` `code` ``,
  numbered lists (literal numbering preserved), bullet lists, `---` rule.
- PDF rendering uses MS Word via `docx2pdf` (Windows only); close Word first to
  avoid COM contention. On a headless box, run with `--no-pdf`.
- The converter handles *formatting*, not *content compliance*. Before export,
  check each source against its template structure (sections, header block,
  signatory/reviewer-information block) in `council/en/`.
