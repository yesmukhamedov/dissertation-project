---
name: council-docs
description: Convert dissertation-council Markdown documents (abstracts, supervisor/foreign-consultant reviews) from thesis/output/ into GOST-formatted .docx and .pdf, following the templates and formatting rules in council/en/. Use whenever the user asks to export, render, or produce council deliverables as Word/PDF.
---

# council-docs — GOST .docx / .pdf export

Render the council Markdown sources in `thesis/output/` into Word and PDF
deliverables (output to `defense/docs/`) that satisfy the IITU/HAC GOST formatting rules.

## Metadata registry — the single source of truth

Every name, position, degree, e-mail, ORCID, the department, the programme code
and name, the dissertation titles (EN/RU/KZ), the volume figures and the
publication list live in **`council/METADATA.toml`** and nowhere else. Documents
reproduce those values; they never define their own. `build_title.py` reads the
registry directly, so the title page cannot drift from the abstracts.

Before and after touching any council document, run the checker — it verifies
each deliverable against the registry, catches previously fixed wrong forms
coming back, and lists registry fields still empty with the document each is
needed for:

```powershell
python .claude/skills/council-docs/scripts/check_metadata.py
```

## Authoritative references (read before editing output)

- Metadata values: `council/METADATA.toml` (human pointer: `council/PEOPLE.md`)
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

## Inline markup the converter understands

`**bold**`, `*italic*`, `` `code` ``, `$math$`, and `<u>underline</u>`. The last
exists for the official reviewer's report, whose form is filled in by
**underlining** the chosen answer option inside column 2 while the unchosen
options stay visible; the HTML tag is used rather than `__…__` because the
latter collides with identifiers such as `__init__` in the appendix listings.
`<br>` inside a table cell opens a new paragraph — the form stacks its answer
options one per line and numbers its enumerations that way.

Pipe tables render as bordered Word tables with a bold header row. The
Appendix-3 reviewer form is recognised by its header (`№` / `№ п/п` / `р/н №`
plus Criteria/Критерии/Критерийлер, four columns) and then gets the layout the
real submissions use: **landscape** page, column widths 4/17/25/54 % of the text
block, and **vertical merging** — a row whose first cell is empty continues the
row above it, so every empty cell in it joins the block started there. That is
how the numbered sub-criteria (4.1…4.5, 8.1…8.5, 9.1…9.3) and the eleven
provisions of criterion 7 each get a row of their own. Nothing else in any
deliverable matches that header, so other tables are untouched.

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
| `reviewer_{1,2}_review_{en,ru,kz}` | Reviewers' reports (Appendix 3) | 15-official-reviewer-report | `defense/docs/reviews/` |
| `predefense_protocol_ru` / `predefense_protocol_kz` | Extended department meeting protocol (§5 pre-defense), both editions | 22-extended-meeting-protocol | `defense/docs/reviews/` |

The protocol exists in two editions. Russian is the form of the genre — the
department secretary writes it, and both council samples are Russian — and it
stays the primary file. Kazakh is carried alongside because the defense is held
in Kazakh; the candidate keeps the protocol in the language of the defense.

The dissertation title inside **both** editions is given in Kazakh, for the same
reason, so `check_metadata.py` verifies each against `dissertation.title_kz`.
The Kazakh edition translates the running text but keeps the technical
terminology, dataset and model names, metric names and the publication entries
in their original form; DOIs are what the publication check compares.

Neither edition is in `build_all.py`. Render them with:

```powershell
python .claude/skills/council-docs/scripts/md2gost.py thesis/output/predefense_protocol_ru.md -o defense/docs/reviews/PREDEFENSE_PROTOCOL_RU_GOST.docx --pdf
python .claude/skills/council-docs/scripts/md2gost.py thesis/output/predefense_protocol_kz.md -o defense/docs/reviews/PREDEFENSE_PROTOCOL_KZ_GOST.docx --pdf
```

Two conventions the protocol relies on: `<!-- center -->` above an all-caps
sub-heading centres it (КҮН ТӘРТІБІ, ТАЛҚЫЛАУ, ШЕШІМ, ҚОРЫТЫНДЫ, ҚАУЛЫ and
their Russian counterparts), and a two-column pipe table whose header row is
empty renders as a borderless bold signature block, set off by two empty lines.

Two official reviewers are appointed, and the **language of a report follows the
reviewer, not the defense**, so all six stems are carried until the reviewers
are known; build only the two that apply.

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
