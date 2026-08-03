# TASK — Regenerate demo result figures for the 2026-08-02 run

**Goal.** The dashboard's numbers (`src/data.js`, `public/RESULTS.md`, `public/results/**/*.json`)
were updated to the 2026-08-02 run, but the ~30 result PNGs under `public/results/` were still
rendered from the *previous* run. This task brings the images in line, then points
`thesis/ASSET_INVENTORY.md` at them.

**Definition of done**
1. All result PNGs regenerated from the current constants — no figure shows a superseded number.
2. `demo/` is internally consistent: figure ↔ caption ↔ table ↔ JSON all agree.
3. `thesis/ASSET_INVENTORY.md` reflects the real status of the run and points at the new figures.

---

## 0. Environment

`generate_charts_*.py` need: `numpy`, `matplotlib`, `scipy`, `opencv-python(-headless)`, `Pillow`.

```powershell
python -m pip install matplotlib scipy opencv-python-headless Pillow
```

Verified working set (Windows, Python 3.13.14):
matplotlib 3.11.1 · scipy 1.18.0 · opencv-python-headless 5.0.0.93 · Pillow 12.3.0 · numpy 2.5.1

- [x] **0.1** Dependencies installed.

---

## 1. Blockers that had to be fixed before anything could be rendered

Installing matplotlib was necessary but **not sufficient** — three separate faults would have made
the regeneration fail or silently write to the wrong place.

- [x] **1.1 Output routing.** `generate_charts_01_14.py` and `_15_28.py` both define
  `OUT = public/results` and `save(fig, name)` writes **flat** into that directory. The dashboard,
  however, loads from per-experiment subdirectories (`/results/exp1/01_...png`,
  `/results/general/21_...png`, …), which is where the existing 30 PNGs live. Running the scripts
  unmodified would have deposited 28 new files at the top level while the app kept serving the old
  ones from the subdirectories — a silent no-op.
  *Fix:* added a `ROUTE` map (chart number → subdirectory) and made `save()` resolve it, matching
  the layout already on disk. `generate_charts_29_30.py` already took an explicit `subdir` argument
  and needed no change.

- [x] **1.2 `generate_charts_29_30.py` vs the new JSON schema.** This script is the only one that
  *reads* its data from `public/results/**/*.json` rather than hardcoding it. The updated JSONs
  dropped keys it depended on, so it would have raised `KeyError` on the first chart:
  - `exp3_aptos_transfer.json` — `Config_A` / `Config_B` no longer exist (Exp 3 ran on
    EfficientNet-B3 fold-0 only, so Configs A/B were never evaluated on APTOS); `aptos_f1_std`,
    `statistical_tests.delong_auc_config_d` and `bootstrap_delta_g_95ci` are gone (the run reports
    per-instance bootstrap CIs on ΔF1/ΔAUC instead).
  - `exp7_small_data.json` — the `improvement` block was replaced by `paired_differences`.
  *Fix:* rewrote both chart functions against the current schema — chart 29 now plots C vs D with
  the ΔF1/ΔAUC bootstrap CIs, chart 30 uses `paired_differences` and states that significance comes
  from the paired test (the unpaired per-arm CIs overlap at n = 60).

- [x] **1.3 Charts 25/26/27 have no source images.** They call
  `generate_pipeline_images.load_image('right_eye.jpeg' / 'left_eye.jpeg')` from
  `public/fundus-examples/dr04/`, and that directory does not exist in this checkout
  (`public/fundus-examples/` holds only loose working files).
  *Decision:* **skip, do not regenerate.** These three are pipeline/Grad-CAM *illustrations* — they
  display no metric from any run, so their existing PNGs are not stale and nothing is lost. The
  scripts now skip them with a warning instead of crashing the whole batch.
  *To restore them later:* place `right_eye.jpeg` and `left_eye.jpeg` in
  `public/fundus-examples/dr04/` and rerun `generate_charts_15_28.py`.

---

## 2. Regeneration

```powershell
cd D:\dissertation-project\demo\web
python generate_charts_01_14.py
python generate_charts_15_28.py
python generate_charts_29_30.py
```

- [x] **2.1** Charts 01–14 rendered.
- [x] **2.2** Charts 15–28 rendered (25/26/27 skipped, see 1.3).
- [x] **2.3** Charts 29–30 rendered from the updated JSONs.
- [x] **2.4** Every PNG written into its correct subdirectory; file count unchanged at 30.
- [x] **2.5** Layout defects found on visual inspection and re-rendered: chart 13 (the optimum star
  covered the very cell value it marks — moved to the cell corner), chart 29 (threshold label sat on
  the bar), chart 16 (change annotation collided with the panel title — added y-headroom), chart 30
  (summary box covered a value label — added y-headroom). Data unchanged; layout only.

### Figure → subdirectory map (as implemented in `ROUTE`)

| Subdir | Charts |
|--------|--------|
| `exp1/` | 01, 02, 03, 18, 19, 20, 22, 24 |
| `exp2/` | 04, 05, 13, 23 |
| `exp3/` | 29 |
| `exp4/` | 06, 07, 27\*, 28 |
| `exp5/` | 08, 09 |
| `exp6/` | 10 |
| `exp7/` | 30 |
| `general/` | 11, 12, 14, 15, 16, 17, 21, 25\*, 26\* |

\* not regenerated — see 1.3.

---

## 3. Content changes carried into the figures

Beyond the numeric refresh, four figures changed **meaning**, because the previous versions plotted
quantities the 2026-08-02 run does not contain. Recording them here so the captions in
`public/RESULTS.md` and the dashboard stay honest:

| Chart | Was | Now | Why |
|-------|-----|-----|-----|
| 05 / 23 | per-stage contribution with CLAHE as the clear leader (+1.4pp) | marginal Δ per stage against the 2·σ_fold band | contributions are near-uniform (+0.90…+1.00pp); the stages **cannot be ranked** |
| 16 | CNR / **VVI** / Entropy / SSIM | CNR / Entropy / SSIM at level L0 vs L7 | VVI is not implemented in `src/utils/image_quality.py` — the old value had no source |
| 24 | per-class ROC curves synthesized from per-class AUC | measured per-class recall | per-class ROC-AUC was not recorded in this run |
| 28 | cross-dataset attention consistency | per-image direction of the ALO effect | attention consistency was never measured; the old values had no source |

Also: chart 10's inset now reports the between-device **spread** (std 0.0281 → 0.0106, 2.6×) instead
of the superseded "variance −46%"; chart 17 panel 1 shows GFLOPs instead of training time per epoch
(never measured).

- [x] **3.1** Captions in `public/RESULTS.md` §4 match the new figure content.
- [x] **3.2** Dashboard captions (`src/tabs/*.js`) match.

---

## 4. `thesis/ASSET_INVENTORY.md`

The inventory is dated **2026-06-08**, i.e. *before* any experiment ran. It therefore states
"Exp 2–7 ❌ NOT RUN" and flags the demo JSONs as placeholder previews. That is now wrong on both counts.

- [x] **4.1** §1.1 experiment status table updated to the real post-run state.
- [x] **4.2** §1.2 resource tally updated.
- [x] **4.3** §1.3 writing-order implications updated (chapters unblocked).
- [x] **4.4** Result figure/table rows in §2 repointed at the regenerated PNGs and at `results/tables/`.
- [x] **4.5** Provenance policy (§0) amended: demo figures are now rendered from the run's numbers,
  **but** the run's raw artifacts are still absent from `experiments/outputs/` — so a demo PNG is
  still not a citable primary source. This distinction must survive the update.

---

## 5. Verification

- [x] **5.1** All 30 PNGs present, 27 with a fresh timestamp, 3 intentionally untouched.
- [x] **5.2** Scripts exit 0 and are re-runnable (idempotent).
- [x] **5.3** No superseded value remains in `demo/` outside `build/` — checked with a pattern sweep
  for the old headline numbers (`0.724`, `0.780`, `0.865`, `+5.2pp`, `+5.3pp`, `25.6M`, `12.2M`,
  `VVI`, `p=0.006`, `−46%`).
- [x] **5.4** `build/` re-synced from `public/`.

---

## 6. Known limits after this task

These are **not** fixed here and must not be presented as fixed:

1. **Provenance.** All numbers still originate from `VALUES.md`. The raw artifacts of the
   2026-08-02 run are absent from `experiments/outputs/`, and `results/data/*.json` still holds the
   *previous* run. Until that is resolved, no demo figure is traceable to a primary output file.
   See `results/INTEGRITY_NOTE.md` §1 and the NEW-1 item in `results/HYPOTHESIS_COVERAGE.md`.
2. **Charts 25/26/27** are from the earlier render (source fundus images missing). They carry no
   metrics, so they are not stale — but they are also not reproducible from this checkout.
3. **Chart 19 (training curves)** is a schematic anchored to measured endpoints only (final val F1
   per config, best-epoch val loss). The per-epoch history is not exported by the run, so the
   intermediate epochs are interpolation, not data. The script says so in a comment; keep it.
4. **`thesis/` governance is untouched.** `thesis/CLAUDE.md` still records "H-3: DROPPED in V3",
   while the 2026-08-02 run measures H-3 (domain distance) and confirms it. That contradiction is a
   governance decision for the candidate, not an inventory edit — flagged, not resolved.
