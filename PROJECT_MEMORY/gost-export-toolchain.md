---
name: gost-export-toolchain
description: What md2gost.py can now render (Mermaid, appendix-letter markers, print-resolution images), what the export needs installed, and the three defects the first real re-export uncovered
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
