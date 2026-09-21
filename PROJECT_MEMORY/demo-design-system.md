---
name: demo-design-system
description: "Visual identity of the demo dashboard and the PDF case report (redesigned 2026-09-21): tokens, typeface, the ICDR grade scale as signature element, and the rules that keep web and print in step"
metadata:
  type: project
---

**2026-09-21 the dashboard (`demo/web`) and the case PDF (`demo/server/app/report.py`) were
redesigned as one system.** Direction: an ophthalmic instrument, not a SaaS dashboard.

- **Tokens** live in `web/src/index.css` `:root`. Every tab's inline styles already read
  `var(--color-text-secondary, …)` etc., so those variables re-theme all 21 tabs; the fallbacks
  in the inline styles are dead code now. Interface colour = slit-lamp cobalt `#2340B8` on cool
  slate ink `#16212C` / page `#F4F6F7`.
- **ICDR grade ramp** 0→4 `#3E7C74 #8A9A3B #C98A1B #C4521F #9E1F24` (healthy-retina teal to
  haemorrhage red) + darkened text variants. **Three copies must stay equal:** `--grade-*` in
  `index.css`, `GRADE_COLORS`/`GRADE_INK` in `data.js`, `_GRADE`/`_GRADE_INK` in `report.py`.
- `C` in `data.js` was retuned, keys and meanings unchanged (teal = pipeline arm, gray = baseline).
- **Typeface: Golos Text** (OFL), web via Google Fonts, PDF via TTFs bundled in
  `server/app/fonts/` (full static files from `googlefonts/golos-text` — the Google Fonts CSS
  API hands out Latin-only subsets, don't re-download from there). It covers all Kazakh letters
  but **has no ✓ ✗ σ** — the PDF draws verdict marks as vectors (`_Mark`) and writes "SD".
- **Signature element: the ICDR grade scale** — `GradeScale` in `Demo.js`, `_GradeScale` in
  `report.py`: probability columns on the five ramp steps, referral threshold dashed between 1
  and 2. Empty image slots are drawn as fundus reticles labelled OD/OS.
- **"Lite"/"Full" keep those words** in the mode chip: the invitations to the ophthalmologists
  ([[ophthalmologist-expert-reviews]]) say «режим Full».
- PDF page 1 = finding (reviewer's grade set largest; model grade before a verdict, marked
  "awaiting review") + OD/OS photos + grade scale + facts + provenance; evidence pages follow,
  "Page n of m" via a two-pass canvas. `_CONTENT_W` subtracts the frame's 6 pt paddings — the
  old report overran the right margin by 12 pt.
- The matplotlib PNGs under `web/public/results/` were **not** recoloured (still the old palette
  and old numbers — see `web/CLAUDE.md`).

Related: [[demo-patient-case-store]] (the report's content rules), [[demo-stack]].
