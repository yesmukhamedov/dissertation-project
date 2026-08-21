---
name: gost-export-toolchain
description: What md2gost.py can now render (Mermaid, appendix-letter markers, print-resolution images), what the export needs installed, the run order of the eight builders, and the five defects the two real re-exports uncovered
metadata:
  type: project
---

The §11.4 GOST re-export ran for the first time against the current 98-section
manuscript on 2026-08-12. `md2gost.py` gained three capabilities it did not have
when the June builds were made, and each closed a defect that would have shipped.

**Mermaid.** A ```mermaid fence is rendered to a PNG and embedded; every other
fence still sets as monospace source. Without this, Appendix C's four structural
views reached the reader as code and the appendix failed to discharge DIA-6.3.
Renders are cached in `defense/figures/mermaid/` keyed by a hash of the diagram
source — **committed on purpose**, so a machine without Node still builds, and so
the byte-identical Kazakh source hits the same entry. A diagram that fails to
render is reported and exits non-zero; it is never silently shipped as source.

Rendering needs `@mermaid-js/mermaid-cli` (installed at the repo root,
`node_modules/` is gitignored) driving an installed Chrome — no Chromium
download. The resolver tries `$MMDC`, repo `node_modules/.bin`, `PATH`, then
`npx`. Chrome is found by `$PUPPETEER_EXECUTABLE_PATH` or the usual locations.

**Appendix-letter asset markers.** The marker regex matched digits only, so every
letter-numbered marker printed in the document as raw bracket text with its file
path showing — **all 54 Appendix-E plates, the 6 Appendix-D confirmations** and
the DIA references. It now covers `FIG/FIGURE/APP/DIA/TAB` with ids like `E.1` or
`D`, resolves markers inside list items and backticks, auto-numbers letter-only
ids (APP-D → D.1…D.6), and gives DIA its own "Diagram"/"Диаграмма" caption series
because `DIA-6.1` and `FIG-6.1` both exist and would otherwise collide. A marker
whose target is not an image is a cross-reference and is dropped from the prose,
not printed.

**Print resolution.** Images are downscaled to 300 dpi at their placed width and
re-encoded, keeping PNG unless JPEG is at least twice smaller. The Appendix-E
plates are 455 dpi natively and took the document to 86 MB; it is now ~18.7 MB
per language. Cache: `defense/docs/.print_cache/` (gitignored).

**The export also needs `pywin32` and `docx2pdf`** — neither was installed in the
current Python 3.13; Word itself is present. Page counting and the PDF step both
depend on them.

Two builder scripts pinned `--date` to `2026-06-17` and `build_full_dissertation.py`
cut the body at `^# 1 `, which would have dropped all sixteen §0.x sections now
that the Introduction is assembled ahead of Chapter 1 — the same defect class as
citation defect #2. Both now resolve the newest pair at run time, and the body
starts at the Introduction where one exists. See [[thesis-writing-status]].

**The four-chapter export (2026-08-20) sprang two more, both in the CONTENTS and
both silent** — the page numbers looked plausible, so only reading the assembled
contents back out of the .docx caught them. See [[four-chapter-rewrite]].

1. **Kazakh chapter conclusions took the chapter's opening page.** `build_toc.py`
   keyed a heading by its leading number, and `1-бөлім бойынша қорытындылар`
   leads with `1`, so it collided with chapter 1 and inherited page 18 instead of
   its own 31. Two causes, both fixed: `_LEADNUM` now requires the number to be a
   token of its own (`(?=\s|$)`), and `_CONCL_KZ` matches `N-бөлім` as well as the
   six-chapter tree's `N-тарау`. English escaped only by accident — "Conclusions
   on section 1" has no leading digit and fell through to the front-matter map.
2. **The contents listed DEFINITIONS before DESIGNATIONS AND ABBREVIATIONS**,
   while the bundle renders them the other way round (the house order verified
   against the IITU samples), so the page column ran 4, 7, 5. Fixed in the
   sources `thesis/output/contents_{en,kz}.md`, not in the builder.

Run order for a full re-export, each step feeding the next:
`_assemble_{en,kz}.py` → `_finalize_citations.py` → `md2gost.py` per language into
`defense/docs/DISSERTATION_{EN,KZ}_GOST_<date>.docx` → `build_title.py` →
`build_frontmatter.py` → `build_toc.py --date <date>` → `build_frontmatter_bundle.py`
→ `build_full_dissertation.py`. Use the system interpreter
`C:\Users\PC\AppData\Local\Programs\Python\Python313\python.exe` — the shell's
default `python` is the demo venv, which has neither `python-docx` nor `pywin32`.
Then `build_all.py` for the abstracts, reviews and papers list, and `check_metadata.py`
last. A same-day re-export overwrites in place: the builders stamp `date.today()`, so the
second run of a day replaces the first rather than branching.

**The run has to be done twice whenever the volume changes**, because the Introduction of
each edition prints its own page and source counts. Export, measure, write the measurement
into `chapters/00-introduction/{drafts,translations}/` and into `council/METADATA.toml`,
re-export, confirm the figure did not move. Measuring means opening
`FULL_DISSERTATION_<lang>_GOST_<date>.docx` in Word and taking the page on which the first
appendix heading falls — *skipping the contents*, where the same heading text appears on
page 3 and will silently give you a body length of 2.

**One Word at a time.** Every PDF step and the page count drive the same single Word COM
instance, so a second script that opens Word while a build is running kills the first: the build
raises `AttributeError: Word.Application.Documents` on the `.docx` → `.pdf` step, keeps going, and
**leaves the previous run's PDF in place next to a fresh `.docx`** — same filename, same date
stamp, an hours-old body. Nothing in the log says so unless you read the traceback, so after any
re-export compare the `.docx` and `.pdf` timestamps before shipping. Measure page counts only
between builds, never alongside one.

**There is no umbrella `APPENDICES` / `ҚОСЫМШАЛАР` heading any more** (2026-08-21). It was the
only top-level heading with no body of its own and printed as a lone word on a blank page, so
`_assemble_{en,kz}.py` now takes `None` for that chapter's heading and the appendices open at
`Appendix A` / `А қосымшасы`. `conformance.py` learned the Kazakh `<letter> ҚОСЫМШАСЫ` form as
a main-text terminator; anything else that keyed off the divider has to be checked against the
first appendix heading instead.
