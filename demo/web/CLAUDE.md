# demo/web/ — DR Diagnosis Dashboard

## TODO

- [ ] Regenerate all pipeline demonstration images using full pipeline (isotropic resize + padding + adaptive flat-field). Current images show old stretch-resize.

---

Interactive React dashboard for PhD dissertation defense. Visualises all experiment results, hypothesis status, and the preprocessing pipeline walkthrough.

## Stack

React 19 (Create React App), single-page app, no router, no external UI library.
Runs at localhost:3000 (`npm start`).

## Architecture

```
src/
├── App.js           — Shell: sidebar nav (192px) + tab routing (~100 lines)
├── data.js          — ALL data constants (single source of truth for metrics)
├── components.js    — Reusable UI: Card, Note, Hbar, Paired, Sec, DataTable, ImageFigure, DiagramViewer, LangSwitcher
├── i18n.js          — EN/KZ internationalization (LangContext + useLang hook)
├── index.js         — CRA entry point
├── index.css        — Base styles
└── tabs/            — 17 tab components (one file each)
    ├── Overview.js
    ├── ModelArchitecture.js, ModelPipeline.js, ModelMethods.js, ModelExplainability.js
    ├── Datasets.js
    ├── ExpH1.js, ExpH2.js, ExpH4.js, ExpH5.js, ExpH6.js
    ├── ResultsMain.js, ResultsBestConfig.js, ResultsStatistical.js
    └── ValClinical.js, ValQuality.js, ValComputational.js

public/
├── results/         — 28 PNG result charts (01–28)
├── pipeline/        — 17 PNG pipeline stage illustrations
├── diagrams/        — SVG + spec files for system and pipeline architecture
├── fundus-examples/ — Example fundus images by DR grade (dr00, dr02, dr03)
└── RESULTS.md       — Results summary document
```

## Data Flow

`experiments/` runs → `results/` knowledge base → numbers transcribed into `src/data.js` → tabs render them.

All experiment metrics come from `src/data.js`. When experiment results update, edit data.js — tabs read from it automatically. **Every constant in data.js carries a comment naming the `results/tables/*.md` file it came from; keep that link when editing.**

**Current data: synced to `results/` (`VALUES.md` → `results/tables/`), the revision that re-specified H-7 and resolved the H-2 stage hierarchy.**
⚠️ The raw artifacts of that run are not yet in `experiments/outputs/` — see `results/INTEGRITY_NOTE.md` §1. Do not cross-check numbers against `experiments/outputs/` or `results/data/*.json` until that is resolved; they hold the *previous* run.

The chart scripts (`generate_charts_*.py`) and the JSONs under `public/results/{exp2,exp3,exp5,exp7}/` keep their own copies of these constants and were updated in step with data.js. **The PNGs under `public/results/` have NOT been regenerated** (matplotlib is not installed in this environment) — rerun the three scripts on a machine that has it, otherwise the figures still show the previous numbers while the tables show the current ones.

## Key Data Constants in data.js

- `C` — colour palette (blue/teal/coral/purple/amber/gray/green/red + backgrounds + text variants)
- `CONFIGS` (A–D), `CONFIG_DELTAS` — Experiment 1 results + paired differences with 95% CI
- `ABL` (8 levels), `STAGE_CONTRIB` — Experiment 2 cumulative ablation + per-stage marginal Δ vs the 2·σ_fold band
- `CLAHE1`, `CLAHE2`, `CLAHE_WF1`, `CLAHE_CLIP`, `CLAHE_THRESH`, `CLAHE_HELDOUT` — joint CLAHE grid (8×5) + held-out confirmation
- `FF_SWEEP`, `FF_HELDOUT` — flat-field σ sweep
- `ALO`, `IOU`, `ALO_DIRECTION`, `ALO_THRESHOLD` — Experiment 4 explainability (+ per-image direction, threshold robustness)
- `DOMAIN_DIST` — H-3 domain distance (MMD / KL over 6 domains)
- `APTOS`, `GEN`, `GEN_AUC`, `G_RATIO` — Experiment 3 transfer + cross-dataset generalization
- `DEGRADATION` — Experiment 5 clinical degradation (H-7, partial)
- `DEV`, `DEVICE_SPREAD` — Experiment 6 device shift + between-device spread
- `SMALL_DATA`, `SMALL_DATA_DELTAS` — Experiment 7 small-data training
- `CLS`, `CLS_PR`, `CONFUSION` — per-class F1, precision/recall, confusion matrices
- `CLIN`, `CALIBRATION` — clinical validation
- `IQ`, `IQ_LEVELS` — image quality (L0 vs L7, and per level)
- `PIPE` — pipeline stage definitions
- `COMPUTE` — computational benchmarks
- `STAT_TESTS`, `TRAIN_TEST_GAP` — statistical tests; convergence / loss-gap by config
- `SSL_GATE` — SSL linear-probe gate (from-scratch + continual)
- `DATASETS` — 8 datasets
- `HYPOTHESES` — H-1…H-7 (6 confirmed, H-7 partial); `EXTRA_RESULTS` — E-7 and A-1

**Removed as unsourced:** `ATTENTION_CONSISTENCY` (cross-dataset attention consistency was never measured) and `CLS_AUC` (per-class ROC-AUC not recorded in this run). `IQ` no longer contains VVI — it is not implemented in `src/utils/image_quality.py`. Do not reintroduce these without a real measurement.

## Design Decisions

- All inline styles (CSS-in-JS). No external CSS framework. **The one exception is
  `src/index.css`**, which carries the shell (sidebar/topbar/drawer) and the whole
  responsive layer — see *Responsive / mobile* below.
- No external charting library — all charts are hand-rolled divs.
- No status badges/labels — everything presented as completed work. All 7 hypotheses are confirmed, so no `◐ Partial` marker is in use; the caveats live in the section notes instead (H-7's thin Messidor-2 margin, the g_ratio inversions, NC-14).
- Tab IDs: exph1, exph2, exph3, exph4, exph5, exph6, exph7. Note the tab labels do not map one-to-one onto hypothesis numbers (exph3 → H-4/APTOS, exph4 → Exp 5 external clinical sets). **H-3 is not dropped** — domain distance (MMD/KL) is measured and confirmed; the data lives in `DOMAIN_DIST` but has no dedicated tab yet.
- Images use `process.env.PUBLIC_URL` prefix for CRA compatibility.
- Numbers: 3 decimal places for metrics, percentages as `pp`.

## Governance Alignment

Dashboard data must match `../../thesis/governance/` invariants exactly:
- Pipeline: 8-stage
- EyePACS: ~35,126 labeled images; Exp 1: 100%, 5-fold CV
- Hypotheses: H-1 … H-7 (H-3 = domain distance, measured and confirmed)
- ALO is primary explainability metric; IoU is secondary
- EH-3 threshold: ΔF1 ≥ 5pp, ΔAUC ≥ 2pp, no κ degradation
- H-4 threshold: generalization ratio G ≥ 0.85; H-6 device floor: g ≥ 0.70

**Claims that must not be overstated** (see `results/findings/summary-and-dominance.md`):
- **NC-14** — Grad-CAM is attention alignment, not clinical localization of pathology. H-5 being confirmed does not relax this.
- The H-4 and H-6 thresholds are cleared by the **baseline** as well, so those criteria alone do not separate the arms — the discriminating evidence is the comparison against baseline and the narrowed between-device spread.
- **H-7 claims external performance, not resistance.** It is confirmed 2/2 under the operative form (Δ wF1 ≥ MCID 0.050, CI⁻ > 0), but never write "the pipeline degrades less": proportionally the arms drop almost equally. The Δ_drop form is retired and algebraically degenerate; the same defect drives the H-6 g_ratio inversions. Always carry the Messidor-2 caveat — the margin over the MCID is 0.0041.
- Stage contributions **can** be ranked as a grouping: flat-field (+1.43pp) and CLAHE (+1.25pp) lead with 41% of the gain between them. But adjacent ranks sit within noise, so never write "stage X ranks above stage Y" outside the photometric-vs-rest split, and note that the hierarchy has not yet been shown to reproduce across runs.
- Clinical metrics are operating characteristics on annotated datasets, not a clinical validation.

## Responsive / mobile

Every tab is authored at desktop density: 9-12px inline font sizes laid out for an
820px column. Rather than restyle thousands of inline rules, `index.css` scales the
whole content column with `zoom` and then fixes the handful of layouts that cannot
survive a narrow column. Breakpoints:

| Width | `--content-zoom` | Layout width it buys | Shell |
|---|---|---|---|
| >=1024px | 1 (no zoom) | 820px column | sticky 192px sidebar |
| 768-1023px | 1.55 | ~485px | top bar + drawer |
| 360-767px | 1.25 | ~310px on a 390px phone | top bar + drawer |
| <360px | 1.1 | ~290px | top bar + drawer |

`--content-zoom` is a variable rather than a literal so anything measured against the
*unzoomed* viewport can divide it back out (`.tooltip-bubble` does).

What the mobile block does beyond scaling, and why each piece exists:

- **Flex rows wrap.** `.main-content div[style*="display: flex"]` gets
  `flex-wrap: wrap !important` — the card and metric rows are written for an 820px
  column and have to stack below it. Two escape hatches: `.keep-row` for rows whose
  children already shrink with `flex: 1` (segmented controls, the pipeline progress
  strip, the Datasets stacked bar) and `.stack-sm` for side-by-side prose blocks that
  should become one column rather than two narrow ones (the *standard approach vs. our
  adaptation* pairs in `ModelMethods.js`).
- **Oversized `minWidth` is capped.** Blocks carrying `minWidth: 150...240` are switched
  to `border-box` and capped at `100%`; the app sets no global `border-box`, so those
  content-box minimums plus padding and an accent border overhang the screen edge.
- **Tables scroll instead of crushing.** `DataTable` renders into `.table-scroll`
  (`min-width: max-content`, `nowrap`, sticky first column so the row label survives a
  swipe). The eight hand-rolled tables already sit in an `overflowX: auto` wrapper and
  get a 460px floor instead — their cells hold prose, so `nowrap` would run them several
  screens wide.
- **The two fundus slots stay side by side** (`.eye-slot-row` / `.eye-slot`). They are
  1:1 squares; stacked at full width they push the Run button a screen and a half down.
- Touch targets are >=44px, `env(safe-area-inset-*)` is honoured on the top bar, drawer
  and content padding, and `100dvh` is used for the shell and drawer.

Verified with no horizontal overflow on all 21 tabs at 320/360/390/414/768/1440px in
both EN and KZ. When adding a tab, re-check it at 390px — the usual failure is a new
`display: flex` row with a `minWidth` above ~150px, or a table outside `DataTable`.

## Common Tasks

**Update experiment data:** Edit constants in `src/data.js`.

**Add a new tab:**
1. Create `src/tabs/NewTab.js`
2. Import in App.js
3. Add to NAV array and COMPONENTS map in App.js
4. Use components from components.js

**Add result images:** Place PNG in `public/results/`, reference with `ImageFigure` component.

## Commands

```bash
npm start     # dev server → localhost:3000
npm run build # production build → build/
```
