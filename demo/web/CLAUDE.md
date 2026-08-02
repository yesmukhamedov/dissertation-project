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

**Current data: run of 2026-08-02.** Source of truth is `results/` (see `results/STATUS.md`).
⚠️ The raw artifacts of that run are not yet in `experiments/outputs/` — see `results/INTEGRITY_NOTE.md` §1. Do not cross-check numbers against `experiments/outputs/` or `results/data/*.json` until that is resolved; they hold the *previous* run.

The chart scripts (`generate_charts_*.py`) keep their own copies of these constants and were updated in step with data.js. **The PNGs under `public/results/` have NOT been regenerated** (matplotlib is not installed in this environment) — rerun the three scripts on a machine that has it.

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

- All inline styles (CSS-in-JS). No external CSS framework.
- No external charting library — all charts are hand-rolled divs.
- No status badges/labels — everything presented as completed work. Exception: H-7 is shown as `◐ Partial`, because it is confirmed on only 1 of 2 datasets and presenting it as confirmed would be false.
- Tab IDs: exph1, exph2, exph3, exph4, exph5, exph6, exph7. Note the tab labels do not map one-to-one onto hypothesis numbers (exph3 → H-4/APTOS, exph4 → Exp 5 external clinical sets). **H-3 is no longer dropped** — the 2026-08-02 run measured domain distance (MMD/KL) and it is confirmed; the data lives in `DOMAIN_DIST` but has no dedicated tab yet.
- Images use `process.env.PUBLIC_URL` prefix for CRA compatibility.
- Numbers: 3 decimal places for metrics, percentages as `pp`.

## Governance Alignment

Dashboard data must match `../../thesis/governance/` invariants exactly:
- Pipeline: 8-stage
- EyePACS: ~35,126 labeled images; Exp 1: 100%, 5-fold CV
- Hypotheses: H-1 … H-7 (H-3 = domain distance, measured and confirmed in the 2026-08-02 run)
- ALO is primary explainability metric; IoU is secondary
- EH-3 threshold: ΔF1 ≥ 5pp, ΔAUC ≥ 2pp, no κ degradation
- H-4 threshold: generalization ratio G ≥ 0.85; H-6 device floor: g ≥ 0.70

**Claims that must not be overstated** (see `results/findings/summary-and-dominance.md`):
- **NC-14** — Grad-CAM is attention alignment, not clinical localization of pathology. H-5 being confirmed does not relax this.
- The H-4 and H-6 thresholds are cleared by the **baseline** as well, so those criteria alone do not separate the arms — the discriminating evidence is the comparison against baseline and the narrowed between-device spread.
- **H-7 is partial.** Δ_drop penalizes the stronger arm; the supportable claim is higher absolute external performance, not greater degradation resistance.
- Stage contributions in the ablation are near-uniform — **the stages cannot be ranked**. Never write "the leading stage is X".
- Clinical metrics are operating characteristics on annotated datasets, not a clinical validation.

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
