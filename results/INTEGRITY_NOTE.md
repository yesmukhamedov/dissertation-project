# ⚠️ INTEGRITY_NOTE — provenance and the divergence of demo/defense from the real data

**Read before using any numbers or figures.**

## 1. Provenance of the current `results/` revision (important)

The values and verdicts in this folder were taken from **`VALUES.md` (the 2026-08-03 run)**.

⚠️ **The raw artifacts of that run are absent from the repository.** In `experiments/outputs/` the
latest files are dated 2026-07-30; what is stored there are the results of the **previous** run. The
same applies to `results/data/*.json` — those are copies of the old artifacts.

Consequences:

| What | State |
|-----|-----------|
| `results/STATUS.md`, `tables/`, `hypotheses/`, `findings/` | ✅ the 2026-08-03 run |
| `results/data/*.json` | ⚠️ **previous run** — the numbers do not match the tables above |
| `experiments/outputs/**` | ⚠️ **previous run** |
| `demo/web/`, `defense/figures/` | ❌ a third, even older set of numbers (see §2) |

**Rule until synchronization:** take the numbers for the chapters from `results/tables/` and
`results/STATUS.md`; **do not use** `results/data/*.json` and `experiments/outputs/` **as a
cross-check** — they belong to a different run and will disagree. Item **NEW-1** in
`HYPOTHESIS_COVERAGE.md`; it blocks traceability of the numbers in the dissertation.

## 2. Demo and defense — they diverge from the real data

The demo dashboard (`demo/web/`) and the defense figures (`defense/figures/`) are built on
**manually transcribed** numbers that do not read `outputs/`. They present every hypothesis as
confirmed — which, per the 2026-08-03 run, is **close to the truth on verdicts but wrong on
magnitudes**. That does not make them usable: agreement of the conclusion under wrong numbers is a
coincidence, not correctness.

### The main example — exp1, Weighted F1

| Config | Demo (`data.js`) | 2026-08-03 run |
|--------|------------------|-------------------|
| A | 0.724 | **0.7518** |
| B | 0.776 | **0.8172** |
| C | 0.727 | **0.7538** |
| D | 0.780 | **0.8193** |
| "gain" B−A | +5.2 pp | **+6.54 pp** |
| "gain" D−C | +5.3 pp | **+6.55 pp** |

The demo understates both arms and underestimates the size of the effect by roughly 1.3 pp.

### What is contaminated and must be rebuilt

- **`demo/web/src/data.js`** — the single source of the dashboard's numbers. All the constants
  (`CONFIGS`, `ABL`, `ALO`, `IOU`, `GEN`, `G_RATIO`, `DEV`, `CLS`, `STAT_TESTS`, `HYPOTHESES`) were
  transcribed by hand and do not match the real ones. Separately: `IQ` contains **VVI**, which is
  **not implemented** in the code (`src/utils/image_quality.py`) — that value is invented. `COMPUTE`
  shows 25.6M / 12.2M parameters against the real **23.52M / 10.70M**.
- **`demo/web/generate_charts_01_14.py` / `_15_28.py` / `_29_30.py`** — ~30 PNGs built on hardcoded
  numbers (`CONFIGS = {'A': {'f1': 0.724, ...}}`); they do not read `outputs/`.
- **`defense/figures/scripts/fig9_confusion_matrix.py`** — the `CM_C`/`CM_D` matrices are hardcoded
  by hand.
- **`defense/figures/figures_mine/fig8_training_curves.png`, `fig9_confusion_matrix.png`** — copied
  from the demo PNGs, i.e. based on the demo numbers.
- **`demo/web/CLAUDE.md`** declares "HYPOTHESES — 6 confirmed hypotheses". Per the 2026-08-03 run
  all 7 are in fact confirmed (H-7 under its re-specified External Clinical Performance form) — but the
  demo's list does not include H-3 and rests on incorrect values. The wording still has to be
  replaced during the rebuild.

## 3. What is NOT contaminated (can be trusted)

- `experiments/src/evaluation/metrics.py`, `statistical_tests.py`, `calibration.py` — correct
  computation (the code itself, not the numbers).
- The text of the already approved chapters (1/2/3/6 + §4.1) — by construction they contain no
  experimental metrics (they were written before the runs).
- `experiments/outputs/compute_benchmark.{json,md}` — the computational benchmarks (params, FLOPs,
  latency, VRAM) were **not changed** by the run and agree with `VALUES.md` §A7.

## 4. Rule going forward

Every table/figure in the dissertation, the defense and the demo must be derived from
`experiments/outputs/` (or from `results/`, which consolidates them) — **never** from
`demo/web/data.js`. A bridge script outputs→figures is needed (see `TOOLING.md`) to eliminate manual
transcription as a class of error. The first step is to close NEW-1 and restore
`experiments/outputs/` to the status of sole source of truth.
