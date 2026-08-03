# ASSET INVENTORY — Dissertation Figures, Tables & Experimental Results

**Document type:** Resource inventory (prerequisite for the chapter-by-chapter writing PLAN)
**Candidate:** Yesmukhamedov N.S.
**Compiled:** 2026-06-08
**Revised:** 2026-08-03 — reconciled against the **2026-08-02 experimental run** (all 7 experiments executed) and the regenerated demo figures.
**Scope:** Full monorepo scan (`experiments/`, `demo/`, `defense/`, `thesis/assets/`) reconciled against the required figures/tables derived from `thesis/outline/MASTER_OUTLINE.md`, every chapter `README.md`, `thesis/governance/RESEARCH_ARCHITECTURE.md` (v6.0.0), and `HYPOTHESIS.md`.

---

## 0. Provenance Policy (read first)

This inventory distinguishes three things that are easy to conflate:

1. **A file existing on disk** (a PNG, a CSV, a JSON).
2. **A real experimental result** produced by running the dr-classifier pipeline.
3. **A demo or slide preview figure** rendered for the *defense slides* or the *demo dashboard* to illustrate the intended layout of a result.

**Hard rule applied throughout:** A figure or JSON existing in `defense/` or `demo/` does **NOT** by itself mean the underlying experiment has been run.

**Amendment 2026-08-03.** The situation has changed but the rule has not. All 7 experiments were executed in the 2026-08-02 run, and the demo figures and JSONs have been regenerated from that run's numbers — they are no longer invented placeholders. **However**, the run's raw artifacts (`summary.json`, `*_results.json`, `metrics.csv`, `predictions.npz`) are **still absent from `experiments/outputs/`**; the numbers currently reach the repository only through `VALUES.md` → `results/` → `demo/`. Two consequences:

1. A demo PNG is **still not a citable primary source.** It is now a faithful *rendering* of the run rather than a preview of an imagined one, but the chain back to a machine-produced output file is broken.
2. `results/data/*.json` and `experiments/outputs/` still hold the **previous** run and will contradict the demo. Do not cross-check one against the other until the artifacts are published.

Tracked as **NEW-1** in `results/HYPOTHESIS_COVERAGE.md`; see also `results/INTEGRITY_NOTE.md` §1.

**Status legend:**
- `✅ AVAILABLE` — a real, citable artifact verified to exist at the stated path (real fundus image, real preprocessing render, real metrics from a training run, real validation JSON, or a conceptual/architecture diagram).
- `🟡 RENDERED (provenance pending)` — the experiment has been run and the figure/table is rendered from its numbers via `results/`, but the raw output artifact is not yet in `experiments/outputs/`. Usable for writing; **not** yet citable as a primary source.
- `⏳ PENDING` — partial real data exists on disk but the full required result set is not yet complete; or the artifact is derivable now from existing data but not yet rendered.
- `❌ MISSING` — no real result artifact on disk yet.

---

## 1. Gap-Analysis Summary

### 1.1 Experiment result status (real data on disk)

**Superseded by the 2026-08-02 run.** The table below now reflects that run. Numbers and verdicts are
consolidated in `results/STATUS.md`; per-experiment tables in `results/tables/`.

| Exp | Hypothesis | Required | State after the 2026-08-02 run | Verdict |
|-----|-----------|----------|--------------------------------|---------|
| **Exp 1** | H-1 | 2×2 factorial A–D, EyePACS 100%, 5-fold CV, full metric suite | Complete A–D × 5 folds at 100%; per-class, confusion, calibration, clinical metrics, DeLong/McNemar/Holm/ANOVA | **✅ RUN** — `h1_supported = true`; EH-3 met on both backbones (ΔF1 +6.54/+6.55pp) |
| **Exp 2** | H-2 | ablation + CLAHE sweep + σ sweep + image-quality metrics | 8-level cumulative ablation on full EyePACS × 5 folds under one initialization; joint CLAHE grid 8×5 on EyePACS; **σ sweep now run**; per-level IQ | **✅ RUN** — PC-2 confirmed on both sweeps; PC-8: contributions significant but **near-uniform, stages not rankable** |
| **Exp 3** | H-4 | APTOS 2019 zero-shot transfer, G ratio | C vs D on fold-0 checkpoints; per-class, confusion, referable metrics, bootstrap CIs | **✅ RUN** — `h4_supported = true` (G_D = 0.8976); caveat: baseline also clears 0.85 |
| **Exp 4** | H-5 | Grad-CAM ALO/IoU on IDRiD + Clinical | All 54 mask-carrying IDRiD images, paired Wilcoxon + bootstrap CI + τ sweep | **✅ RUN (IDRiD)** — `h5_alo_supported = true`, 4/4 types significant. **Clinical (KZ) overlays still missing** (gap G-3) |
| **Exp 5** | H-7 | Clinical degradation Δ on IDRiD + Messidor-2 | Both sets, Δ_drop + absolute external F1 with CIs | **✅ RUN** — **◐ H-7 PARTIAL (1 of 2)**: criterion as written holds only on IDRiD; absolute external F1 significantly higher on both |
| **Exp 6** | H-6 | Device domain shift on DDR/ODIR-5K/RFMiD | 5 camera groups, g-ratio, between-group spread, per-class F1 | **✅ RUN** — `h6_supported = true`; substantive result is std(F1) narrowing 2.6× |
| **H-3** | H-3 | *(not previously inventoried — recorded as dropped)* | MMD over penultimate-layer features + KL over channel histograms, 6 target domains | **✅ RUN** — `h3_supported = true`, 6/6 domains, all CIs exclude 0. **⚠️ Conflicts with `thesis/CLAUDE.md` "H-3: DROPPED in V3"** — governance decision required |
| **Exp 7** | — | Small-data 5-fold IDRiD → Clinical | 5-fold IDRiD CV + clinical hold-out n=60, paired CIs; **preregistered** | **✅ RUN** — positive: +0.079 wF1, +0.122 κ, +0.051 AUC |
| **SSL** | — (Premise 4) | in-domain SSL linear-probe gate | from-scratch BYOL/MoCo-v2/DINO + SIP; continual-SSL on both backbones, 2 runs | **✅ RUN** — gate passed; SIP now passes from scratch; both backbones gain from continual-SSL |
| **Validation** | — (supporting Ch 3/Exp 4) | OD/fovea detector accuracy on IDRiD | **Real** `od_fovea_idrid_metrics.json` + montage (516 imgs) | **✅ COMPLETE** |
| **Preproc artifacts** | — (Ch 3) | norm stats | **Real** EyePACS + IDRiD norm stats | **✅ COMPLETE** |

⚠️ **All rows marked ✅ RUN carry the provenance caveat in §0:** the run's raw output files are not yet in `experiments/outputs/`, so these results are usable for writing but not yet citable as primary sources.

### 1.2 Resource tally

**Reconciliation table (§2) — required dissertation resources:** 78 catalogued. *(Revised 2026-08-03.)*
- **✅ AVAILABLE (real, citable):** 33 — unchanged: **preprocessing stage renders, dataset sample images, conceptual/architecture diagrams, the OD/fovea validation, norm-stat artifacts, source code, and publication certificates**.
- **🟡 RENDERED (provenance pending):** 30 — essentially **every result table and figure for Exp 1–7**, now rendered from the 2026-08-02 run via `results/`. Writable against; not yet citable (see §0).
- **⏳ PENDING:** 5 — TAB-5.3 (SOTA comparison, literature-bound), FIG-5.4 (PR curves — need `predictions.npz`), App B partial, plus per-group confusion matrices and per-class ROC-AUC that the run did not record.
- **❌ MISSING (real result):** 10 — clinical (KZ) Grad-CAM gallery (gap G-3), UML diagrams (App C), and the App E/F supplements that depend on them.

**Demo web asset manifest (§4) — files present in `demo/web/public/`:** 471 files. `results/` (33 files: 30 PNG + 3 JSON — **27 PNGs regenerated 2026-08-03** from the current run; 3 pipeline/Grad-CAM illustrations left untouched, see below), `diagrams/` (4), `pipeline/` (430 PNG + 1 helper JSON). The `pipeline/` preprocessing renders are real pipeline outputs. The `results/` figures are **no longer previews** — they are rendered from the run's numbers, subject to the §0 provenance caveat.

**Not regenerated (deliberately):** `results/general/25_pipeline_stages_real.png`, `…/26_bilateral_pair.png`, `results/exp4/27_gradcam_overlay.png`. These are pipeline/Grad-CAM *illustrations* that display no metric from any run, so they are not stale. Their source images (`demo/web/public/fundus-examples/dr04/{right,left}_eye.jpeg`) are absent from this checkout, so they are also not currently reproducible. See `demo/TASK.md` §1.3.

### 1.3 Implication for writing order

**Writable now (no result dependency):**
- **Chapter 1 (Problem Domain)** — literature review; dataset sample montages available for context.
- **Chapter 2 (Theoretical Foundations)** — pure theory; some diagrams reusable, others to draw.
- **Chapter 3 (Methodology)** — ✅ **fully unblocked.** Every pipeline stage has a real render; OD/fovea validation, norm stats, training-config and evaluation-framework tables all exist. (FIG-3.8 Stage-6 render to be regenerated for the ColorJitter/noise/JPEG augmentation.)
- **Chapter 6 (System Architecture)** — design-only chapter; system diagram + webapp screenshots available. **Only blocker:** UML diagrams (component/sequence/class/activity/ER) are not on disk.
- **§4.1 (Datasets & Configuration)** — dataset architecture table + class distribution + samples available.

**Unblocked by the 2026-08-02 run (revised 2026-08-03):**
- **§4.2 (Exp 1)** — ✅ writable. Full 100% A–D × 5-fold suite, statistical layer, calibration, per-class, clinical metrics. Material in `results/findings/exp1.md` + `results/tables/`.
- **§4.3 (Exp 2)** — ✅ writable, all three parts (ablation, CLAHE sweep, σ sweep) closed.
- **§4.4 (Exp 3), §4.6 (Exp 5), §4.7 (Exp 6), §4.8 (Exp 7)** — ✅ writable.
- **§4.5 (Exp 4) + §5.1** — 🟡 quantitative part writable; the clinical (KZ) Grad-CAM overlays that H-5 also calls for are still missing (gap G-3).
- **Chapter 5 (Validation)** — ✅ §5.2.1/§5.2.2 writable (`results/tables/TAB-5.1`, `TAB-5.2`); §5.3 still needs the literature-side TAB-5.3.
- **Chapter 0 (§0.8) & Chapter 7 (Conclusion)** — ✅ unblocked; all verdicts are final.
- **Appendices B, E, F** — data exists; App B needs `predictions.npz` for PR/ROC curves, App E needs G-3, App F needs a per-group confusion-matrix dump.
- **Appendix C (UML)** — ❌ still missing; asset task, not experiment-gated.

**Two decisions the candidate must make before writing:**
1. **Where H-3 goes.** The run measures and confirms it, but `thesis/CLAUDE.md` still records "H-3: DROPPED in V3" and Chapter 4 has no section for it. Its placement changes the numbering of §4.x and of the TAB/FIG identifiers downstream.
2. **Provenance.** Publishing the run's raw artifacts into `experiments/outputs/` before the defense — otherwise no result in Chapters 4–5 traces to a primary output file.

---

## 2. Master Reconciliation Table

> Paths are relative to repo root `E:\dissertation-project\`. Every `✅ AVAILABLE` row points to a file verified to exist during this scan.

### 2.1 Chapter 1 — Problem Domain

| ID | Type | Description / caption | Target § | Source | File path | Status |
|----|------|----------------------|----------|--------|-----------|--------|
| FIG-1.1 | figure | Representative fundus images across DR grades 0–4 (clinical grading context) | §1.1.1 | EyePACS samples (demo) | `demo/web/public/datasets/eyepacs/samples/dr{0..4}/` | ✅ AVAILABLE |
| FIG-1.2 | figure | Cross-dataset / multi-camera landscape comparison | §1.2.3, §1.4 | defense | `defense/presentation/assets/datasets/27_overview/cross_dataset_comparison.png` | ✅ AVAILABLE |
| TAB-1.1 | table | Survey of existing automated DR systems (IDx-DR, EyeNuk, DeepMind, Gulshan et al.) | §1.4 | literature cards | `thesis/literature/external/` (text, not rendered) | ⏳ PENDING |

### 2.2 Chapter 2 — Theoretical Foundations

| ID | Type | Description / caption | Target § | Source | File path | Status |
|----|------|----------------------|----------|--------|-----------|--------|
| FIG-2.1 | diagram | Histogram equalization → CLAHE intensity redistribution concept | §2.1.1 | — | — | ❌ MISSING |
| FIG-2.2 | diagram | CNN feature-hierarchy / convolution-pooling schematic | §2.2.1 | defense | `defense/presentation/assets/architecture/07_cnn/cnn_architecture.png` | ✅ AVAILABLE |
| FIG-2.3 | diagram | Grad-CAM mathematical formulation schematic | §2.5.1 | — | — | ❌ MISSING |
| FIG-2.4 | diagram | Coupled thermal-optical laser-tissue model | §2.4.1 | — | — | ❌ MISSING |
| FIG-2.5 | diagram | Image-quality metrics (CNR/VVI/Entropy/SSIM) illustration | §2.6 | — | — | ❌ MISSING |
| TAB-2.1 | table | CLAHE clip-limit formulations (conventional vs T/80 vs dual-constraint) | §2.1.2 | governance (RESEARCH_ARCHITECTURE §3.2) | text | ✅ AVAILABLE |

### 2.3 Chapter 3 — Methodology (fully unblocked)

| ID | Type | Description / caption | Target § | Source | File path | Status |
|----|------|----------------------|----------|--------|-----------|--------|
| FIG-3.1 | diagram | 8-stage preprocessing pipeline overview (vertical) | §3.1.1 | defense | `defense/presentation/assets/preprocessing/10_input/04_preprocessing_pipeline_vertical.png` | ✅ AVAILABLE |
| FIG-3.2 | figure | Stage 0 — Canonical flip (L→R) | §3.1.1 | defense / demo | `defense/presentation/assets/preprocessing/11_canonical_flip/stage0_canonical_flip.png`; `demo/web/public/pipeline/dr04/preprocessing/stage_0_canonical_flip/` | ✅ AVAILABLE |
| FIG-3.3 | figure | Stage 1 — OD-fovea rotation normalization | §3.1.1 | defense / demo | `defense/presentation/assets/preprocessing/12_od_fovea_rotation/stage1_od_fovea_rotation.png`; `demo/web/public/pipeline/dr04/preprocessing/stage_1_od_fovea_rotation/` | ✅ AVAILABLE |
| FIG-3.4 | figure | Stage 2 — FOV crop + isotropic resize | §3.1.1 | defense / demo | `defense/presentation/assets/preprocessing/13_crop_resize/stage2_fov_crop_resize.png` | ✅ AVAILABLE |
| FIG-3.5 | figure | Stage 3 — FOV mask (4th channel) | §3.1.1 | defense / demo | `defense/presentation/assets/preprocessing/14_fov_mask/stage3_fov_mask.png` | ✅ AVAILABLE |
| FIG-3.6 | figure | Stage 4 — Adaptive flat-field correction | §3.1.1 | defense / demo | `defense/presentation/assets/preprocessing/15_flatfield/stage4_flatfield.png` | ✅ AVAILABLE |
| FIG-3.7 | figure | Stage 5 — Dual-constraint CLAHE (incl. polar variant + vessel maps) | §3.1.1, §3.1.2 | defense / demo | `defense/presentation/assets/preprocessing/17_clahe_polar/stage5_clahe.png`; `demo/web/public/pipeline/dr04/preprocessing/stage_5_clahe/polar/` | ✅ AVAILABLE |
| FIG-3.8 | figure | Stage 6 — Augmentation (rotation/translation/scale/shear/ColorJitter/Gaussian-noise/JPEG) | §3.1.3 | defense / demo | `defense/presentation/assets/preprocessing/19_aug_rotation/ … 24_aug_brightness_contrast/stage6_augmentation.png` | ⚠️ REGENERATE (current render depicts the superseded PCA-colour aug) |
| FIG-3.9 | figure | Stage 7 — Dataset-specific normalization | §3.1.1 | defense / demo | `defense/presentation/assets/preprocessing/25_normalization/stage7_normalize.png` | ✅ AVAILABLE |
| FIG-3.10 | figure | OD/fovea detector validation montage (IDRiD, 516 imgs) | §3.1.1 (Stage 1) | **Exp validation (real)** | `experiments/outputs/validation/od_fovea_idrid_montage.png` | ✅ AVAILABLE |
| FIG-3.11 | diagram | ResNet-50 / EfficientNet-B3 backbone architecture | §3.2.1 | defense | `defense/presentation/assets/architecture/08_comparison/01_abstract_model_architecture.png`; `defense/figures/figures_mine/fig5_architecture_artistic.png` | ✅ AVAILABLE |
| FIG-3.12 | diagram | Focal-loss weighting schematic | §3.3.4 | defense | `defense/presentation/assets/architecture/09_training/focal_loss.png` | ✅ AVAILABLE |
| FIG-3.13 | diagram | 5-fold patient-level CV split | §3.4.2 | defense | `defense/presentation/assets/architecture/09_training/cv_5fold.png` | ✅ AVAILABLE |
| FIG-3.14 | diagram | End-to-end pipeline flowchart (model = preprocessing + CNN) | §3.1, §3.2 | defense | `defense/figures/figures_mine/fig4_flowchart.png`; `defense/figures/figures_mine/fig6_model_graph.png` | ✅ AVAILABLE |
| TAB-3.1 | table | Standardized training configuration (optimizer, batch, epochs, loss, seed) | §3.4 / §4.1.3 | governance (RESEARCH_ARCHITECTURE §4.0) | text | ✅ AVAILABLE |
| TAB-3.2 | table | Multi-metric evaluation framework & diagnostic thresholds (EH-1, OD-5) | §3.4.1 | governance | text | ✅ AVAILABLE |
| TAB-3.3 | table | Image-quality metrics definitions (CNR/VVI/Entropy/SSIM) | §3.4.1 | governance (RESEARCH_ARCHITECTURE §3.3) | text | ✅ AVAILABLE |
| RES-NORM | result-set | Per-dataset normalization stats (EyePACS, IDRiD) — Stage 7 | §3.1.1 | **Exp (real)** | `experiments/data/processed/eyepacs_norm_stats.json`, `experiments/data/processed/idrid_norm_stats.json` | ✅ AVAILABLE |
| RES-PCA | result-set | ~~EyePACS PCA color-jitter basis (Stage 6)~~ | — | — | — | ❌ RETIRED (2026-06-26 — Stage 6 chromatic aug replaced by ColorJitter; no PCA basis used) |
| RES-VAL | result-set | OD/fovea detector accuracy metrics (IDRiD train/test) | §3.1.1 | **Exp (real)** | `experiments/outputs/validation/od_fovea_idrid_metrics.json` | ✅ AVAILABLE |

### 2.4 Chapter 4 — Experimental Research

| ID | Type | Description / caption | Target § | Source | File path | Status |
|----|------|----------------------|----------|--------|-----------|--------|
| TAB-4.1 | table | Tiered dataset architecture (8 datasets, roles, sizes, cameras) | §4.1.1 | governance (RESEARCH_ARCHITECTURE §2.1) | text | ✅ AVAILABLE |
| FIG-4.1 | figure | EyePACS class-distribution chart | §4.1.2 | defense | `defense/presentation/assets/datasets/27_overview/12_dataset_class_distribution.png` (+`.svg`); data `defense/figures/figures_mine/fig3_dataset_distribution.csv` | ✅ AVAILABLE |
| FIG-4.2 | figure | Sample fundus per DR grade — EyePACS (+ APTOS/IDRiD/Messidor2/DDR/ODIR5K/RFMiD/Clinical) | §4.1.1 | demo | `demo/web/public/datasets/<ds>/samples/dr{0..4}/` | ✅ AVAILABLE |
| FIG-4.3 | figure | Cross-dataset comparison / datasets matrix | §4.1.1 | defense | `defense/presentation/assets/datasets/28_experiments/datasets_matrix.png`; `…/29_cameras/cameras_alignment.png` | ✅ AVAILABLE |
| RES-EXP1 | result-set | Exp 1 metrics — A–D × 5 folds, EyePACS 100% | §4.2 | **Run 2026-08-02** | `results/STATUS.md`; `results/tables/TAB-4.2_exp1_factorial.md`, `exp1_per_class.md`, `exp1_convergence_ci.md` | 🟡 RENDERED |
| TAB-4.2 | table | **Exp 1 2×2 factorial results** — F1/ROC-AUC/κ/Acc (mean±std), configs A–D, EH-3 verdict | §4.2.3 | Exp 1 | `results/tables/TAB-4.2_exp1_factorial.md`; figure `demo/web/public/results/exp1/02_exp1_all_metrics.png` | 🟡 RENDERED |
| FIG-4.4 | figure | Exp 1 factorial weighted-F1 bar chart (A–D) | §4.2.3 | Exp 1 | `demo/web/public/results/exp1/01_exp1_factorial_f1.png`, `…/03_exp1_delta.png`, `…/22_exp1_all_6_configs.png` | 🟡 RENDERED |
| FIG-4.5 | figure | Exp 1 training/validation convergence curves (A–D) | §4.2.2 | Exp 1 | `…/results/exp1/19_training_curves.png` — ⚠️ **schematic**: anchored to measured endpoints (final val F1, best-epoch val loss); per-epoch history not exported by the run. Numeric table: `results/tables/exp1_convergence_ci.md` | ⏳ PENDING |
| FIG-4.6 | figure | Exp 1 confusion matrices (per config) | §4.2.3 / App B | Exp 1 | `…/results/exp1/20_confusion_matrix.png`; numeric matrices in `results/tables/exp1_per_class.md` (n = 35,126) | 🟡 RENDERED |
| FIG-4.7 | figure | Exp 1 per-class discrimination | §4.2.3 | Exp 1 | `…/results/exp1/24_roc_curves.png` — **now plots per-class recall**: per-class ROC-AUC was not recorded in this run (only macro 0.8210 → 0.8570). True ROC curves need `predictions.npz` | ⏳ PENDING |
| FIG-4.8 | figure | Exp 1 per-class F1 under class imbalance | §4.2.3 | Exp 1 | `…/results/exp1/18_per_class_f1.png`; `results/tables/exp1_per_class.md` | 🟡 RENDERED |
| TAB-4.3 | table | Exp 1 calibration (ECE, Brier) per config | §4.2.2 | Exp 1 | `results/tables/TAB-4.3_exp1_calibration.md`; figure `…/results/general/15_calibration.png`. ⚠️ Sign reversed vs earlier run — the pipeline now **improves** calibration | 🟡 RENDERED |
| TAB-4.4 | table | **Exp 2 cumulative ablation (L0–L7)** — weighted F1 per level, single shared init | §4.3.1 | Exp 2 | `results/tables/TAB-4.4_exp2_ablation.md`; figures `…/results/exp2/04_exp2_ablation.png`, `…/05_exp2_per_stage.png`, `…/23_exp2_individual_ablation.png` | 🟡 RENDERED |
| FIG-4.9 | figure | Exp 2 CLAHE sensitivity — joint grid (clip_factor × global_threshold), 8×5, on EyePACS | §4.3.2 | Exp 2 | `results/tables/exp2_clahe_sweep.md`; figure `…/results/exp2/13_exp2_clahe_sensitivity.png` | 🟡 RENDERED |
| FIG-4.10 | figure | Exp 2 flat-field σ sweep (0.05–0.10·D) | §4.3.3 | Exp 2 | **newly run** — `results/tables/exp2_flatfield_sigma_sweep.md`; data `demo/web/public/results/exp2/exp2_ff_sweep.json`. σ* = 0.07·D, held-out Δ +0.0570 | 🟡 RENDERED |
| TAB-4.5 | table | Exp 2 image-quality per ablation level (CNR/Entropy/SSIM) | §4.3.3 | Exp 2 | `results/tables/TAB-4.5_exp2_image_quality.md`; figure `…/results/general/16_image_quality.png`. **VVI dropped — not implemented in `image_quality.py`** | 🟡 RENDERED |
| TAB-4.6 | table | **Exp 3 APTOS transfer** — G = F1_APTOS/F1_EyePACS, C vs D | §4.4 | Exp 3 | `results/tables/TAB-4.6_exp3_transfer.md`; data `…/results/exp3/exp3_aptos_transfer.json` (G_D = 0.8976, G_C = 0.8577) | 🟡 RENDERED |
| FIG-4.11 | figure | Exp 3 cross-dataset transfer chart | §4.4 | Exp 3 | `…/results/exp3/29_exp3_aptos_transfer.png` (rendered directly from the JSON) | 🟡 RENDERED |
| FIG-4.12 | figure | **Exp 4 Grad-CAM overlays** per DR class, baseline vs integrated (IDRiD) | §4.5.1 / App E | Exp 4 | 54 real overlays at `experiments/outputs/exp4/gradcam_maskset/*.png`; demo illustration `…/results/exp4/27_gradcam_overlay.png` (not regenerated — source image missing) | ⏳ PENDING |
| TAB-4.7 | table | **Exp 4 ALO (primary) + IoU (secondary)** per lesion type, n = 54 masks | §4.5.2 | Exp 4 | `results/tables/TAB-4.7_exp4_alo_iou.md`; figures `…/results/exp4/06_exp4_alo.png`, `…/07_exp4_iou.png`. 4/4 types significant; **stays within NC-14** | 🟡 RENDERED |
| FIG-4.13 | figure | Exp 4 per-image direction of the ALO effect | §4.5.3 | Exp 4 | `…/results/exp4/28_attention_consistency.png` — **repurposed**: cross-dataset attention consistency was never measured; the figure now shows improved/unchanged/worsened counts per lesion type | 🟡 RENDERED |
| FIG-4.14 | figure | Exp 4 lesion-overlay reference (IDRiD masks) | §4.5.2 | Exp 4 | demo asset: `defense/figures/figures_mine/fig2_lesion_overlays.png` | ❌ MISSING |
| TAB-4.8 | table | **Exp 5 clinical degradation** Δ_drop (IDRiD, Messidor-2) | §4.6 | Exp 5 | `results/tables/TAB-4.8_exp5_degradation.md`; data `…/results/exp5/exp5_degradation.json`. **◐ H-7 partial (1 of 2)** — see the metric critique in that table | 🟡 RENDERED |
| FIG-4.15 | figure | Exp 5 degradation / generalization chart | §4.6 | Exp 5 | `…/results/exp5/08_exp5_generalization.png`, `…/09_exp5_G_ratio.png` | 🟡 RENDERED |
| TAB-4.9 | table | **Exp 6 device domain shift** — per-camera F1/AUC/κ + between-group spread | §4.7 / App F | Exp 6 | `results/tables/TAB-4.9_exp6_device.md`; figure `…/results/exp6/10_exp6_device_shift.png`. Per-group confusion matrices **not recorded** (App F gap) | 🟡 RENDERED |
| TAB-4.10 | table | **Exp 7 small-data** 5-fold IDRiD→Clinical (baseline vs integrated), preregistered | §4.8 | Exp 7 | `results/tables/TAB-4.10_exp7_smalldata.md`; data `…/results/exp7/exp7_small_data.json` | 🟡 RENDERED |
| FIG-4.16 | figure | Exp 7 small-data performance chart | §4.8 | Exp 7 | `…/results/exp7/30_exp7_small_data.png` (rendered directly from the JSON) | 🟡 RENDERED |

### 2.5 Chapter 5 — Reliability Validation

| ID | Type | Description / caption | Target § | Source | File path | Status |
|----|------|----------------------|----------|--------|-----------|--------|
| FIG-5.1 | figure | Grad-CAM gallery (representative per class, baseline vs integrated) | §5.1 / App E | Exp 4 | 54 IDRiD overlays at `experiments/outputs/exp4/gradcam_maskset/`; **clinical (KZ) overlays missing — gap G-3** | ⏳ PENDING |
| TAB-5.1 | table | Statistical tests (DeLong, McNemar, Holm, bootstrap 95% CI, mixed-effects) | §5.2.1 | Exp 1–7 | `results/tables/TAB-5.1_statistical.md`; figure `…/results/general/21_statistical_tests.png` | 🟡 RENDERED |
| TAB-5.2 | table | Final claim-strength classification PC-0…PC-10 | §5.2.2 | governance + results | `results/tables/TAB-5.2_claim_strength.md` — 5 STRONG, 2 MODERATE, 0 REFUTED | 🟡 RENDERED |
| TAB-5.3 | table | Comparative analysis vs published systems (IDx-DR, EyeNuk, DeepMind, Gulshan — contextual only) | §5.3.1 | literature cards | text (numbers pending own results) | ⏳ PENDING |
| FIG-5.2 | figure | Performance–complexity trade-off | §5.3.2 | Exp 1/6 | `results/tables/computational_and_iq.md` (measured on RTX 3060); figure `…/results/general/17_computational.png` | 🟡 RENDERED |
| FIG-5.3 | figure | Summary radar across hypotheses / EH-3 dominance | §5.2 | all Exp | radar data in `results/findings/summary-and-dominance.md`; figures `…/results/general/11_summary_radar.png`, `…/12_eh3_dominance.png` | 🟡 RENDERED |
| TAB-5.4 | table | Clinical screening metrics (Sens/Spec/PPV/NPV, referable DR) across 3 scenarios | §5.2 | Exp 1/3/6 | `results/tables/TAB-5.4_clinical_referable.md`; figure `…/results/general/14_clinical_metrics.png` | 🟡 RENDERED |
| FIG-5.4 | figure | Precision–recall curves | §5.2 / App B | Exp 1 | demo asset: `defense/figures/figures_mine/fig7_pr_curves.png` | ❌ MISSING |

### 2.6 Chapter 6 — System Architecture (design-only)

| ID | Type | Description / caption | Target § | Source | File path | Status |
|----|------|----------------------|----------|--------|-----------|--------|
| DIA-6.1 | diagram | Modular system architecture (capture→preprocess→inference→report) | §6.1.2 | defense | `defense/presentation/assets/architecture/06_system/02_system_architecture.png` | ✅ AVAILABLE |
| DIA-6.2 | diagram | Preprocessing engine (configurable pipeline) | §6.2.1 | defense (reuse FIG-3.1) | `defense/presentation/assets/preprocessing/10_input/04_preprocessing_pipeline_vertical.png` | ✅ AVAILABLE |
| FIG-6.1 | figure | Deployed web-app / dashboard screenshots | §6.2, §6.3 | defense | `defense/figures/figures_mine/fig10_webapp_screenshot_1.png`, `…_2.png` | ✅ AVAILABLE |
| DIA-6.3 | diagram | UML component / sequence / class / activity / ER diagrams | §6.1.2 / App C | — | — | ❌ MISSING |

### 2.7 Appendices & Front Matter

| ID | Type | Description / caption | Target § | Source | File path | Status |
|----|------|----------------------|----------|--------|-----------|--------|
| APP-A | result-set | Source code of preprocessing pipeline | App A | experiments | `experiments/src/preprocessing/` (+ `experiments/src/`) | ✅ AVAILABLE |
| APP-B | figure-set | Supplementary confusion matrices & training curves | App B | Exp 1–7 | partial (Exp1 curves derivable); rest ❌ | ⏳ PENDING |
| APP-C | diagram-set | System architecture UML diagrams | App C | — | — | ❌ MISSING |
| APP-D | figure-set | Certificates / publication confirmations (Scopus, KBTU, KazUTB, NAS RK) | App D | defense | `defense/presentation/assets/publications/SCOPUS.png`, `…/PUBLICATIONS.png`, `…/KBTU.png`, `…/KAZTBU.png`, `…/AKADEMY.png`, `…/SCOPUS_CONF.png` | ✅ AVAILABLE |
| APP-E | figure-set | Grad-CAM visualization gallery (per class, both pipelines) | App E | Exp 4 | — | ❌ MISSING |
| APP-F | table-set | Device domain-shift supplementary per-camera tables/heatmaps | App F | Exp 6 | — | ❌ MISSING |

---

## 3. Real Result Files On Disk (verified manifest)

The complete set of **real, machine-produced result artifacts** found in `experiments/` (the demo-dashboard preview assets under `demo/`+`defense/` are catalogued separately in §4):

```
experiments/outputs/backup_exp1_full/metrics.csv                       # Exp1 Config A, fold 0, 19 epochs (full-data)
experiments/outputs/backup_exp1_abc_40pct_20260324/metrics.csv         # Exp1 A/B/C folds 0–2 (partial) @40% + broken D f0
experiments/outputs/kaggle_config_d_v2/outputs/exp1/metrics.csv        # Exp1 Config D, fold 0, 10 epochs (clean, EyePACS)
experiments/outputs/kaggle_config_d_v2/outputs/exp1/checkpoints/D_fold0/best_model.pt   # + epoch_05..09, last_checkpoint
experiments/outputs/kaggle_config_d/outputs/exp1/metrics.csv           # header-only (empty run)
experiments/outputs/validation/od_fovea_idrid_metrics.json             # OD/fovea detector accuracy (real)
experiments/outputs/validation/od_fovea_idrid_montage.png              # OD/fovea overlay montage (real)
experiments/data/processed/eyepacs_norm_stats.json                     # Stage-7 norm stats (real)
experiments/data/processed/idrid_norm_stats.json                       # Stage-7 norm stats (real)
experiments/logs/exp1_*.log, smoke_test_*.log, exp2_remaining_smoke.log  # training/smoke logs
```

> ⚠️ **The listing above is the state as of 2026-06-08 and is now itself stale.** It predates both the
> 2026-07 re-runs and the 2026-08-02 run. The files listed still exist, but they are **not** the current
> results. Nothing in `experiments/outputs/` has been written since **2026-07-30**, i.e. the 2026-08-02
> run has not been published into this directory at all.

**Key honesty notes carried into the PLAN (revised 2026-08-03):**
1. **All 7 experiments have now been run** (2026-08-02) and every result table/figure is derived from
   that run through `results/`. The old note that "Exp 1 is the only experiment with any real metrics"
   is superseded.
2. **But the run's raw artifacts are not on disk.** `experiments/outputs/` still holds the *previous*
   run, and so does `results/data/*.json`. The current numbers reach the repository only via
   `VALUES.md` → `results/` → `demo/`. **This is the single most important open item before the
   defense** — until it is closed, no Chapter 4–5 number is traceable to a machine-produced file, and
   the two sources will actively contradict each other. Tracked as NEW-1 in
   `results/HYPOTHESIS_COVERAGE.md`.
3. **What the 2026-08-02 run did not record**, and therefore cannot be cited: per-class ROC-AUC
   (macro only), per-camera-group confusion matrices (per-class F1 only), per-epoch training history
   (endpoints only — FIG-4.5 is schematic), MMD kernel/sample-size parameters, and CPU preprocessing
   wall-clock.
4. **Chapter 3 and §4.1 remain the safest starting points** — their assets are real, on disk, and
   independent of the run.

---

## 4. Demo Web Asset Manifest (`demo/web/public/`)

Complete enumeration of every PNG/JSON under `demo/web/public/results`, `demo/web/public/diagrams`, and `demo/web/public/pipeline`. All paths below are relative to `demo/web/public/` and all files were verified to exist during this scan. **Status `✅ AVAILABLE`** means the file is present on disk; for the `results/` group it does **not** assert that the depicted numbers are traceable to a primary output file (see §0 and the Status column of §2.4–§2.5).

### 4.1 `results/` — dashboard result figures (33 files)

> **Regenerated 2026-08-03** from the 2026-08-02 run — 27 of the 30 PNGs plus all 3 JSONs.
> Regeneration procedure and its prerequisites: `demo/TASK.md`.
> Rendered by `demo/web/generate_charts_{01_14,15_28,29_30}.py`; the numbers come from
> `demo/web/src/data.js` (charts 01–28) and from the JSONs in this directory (charts 29–30).
>
> **Three files intentionally NOT regenerated** — DEMO-R-05 is regenerated but schematic; the three
> below were skipped entirely: `results/general/25_pipeline_stages_real.png`,
> `results/general/26_bilateral_pair.png`, `results/exp4/27_gradcam_overlay.png`. They are
> pipeline/Grad-CAM *illustrations* carrying no metric from any run, so they are not stale; their
> source fundus images are absent from the checkout, so they are also not reproducible here.
>
> **Four figures changed meaning**, because the run does not contain what they previously plotted:
> `05`/`23` (per-stage contribution → marginal Δ against the noise band; stages are not rankable),
> `16` (VVI dropped — never implemented), `24` (synthesized ROC curves → measured per-class recall),
> `28` (attention consistency → per-image direction of the ALO effect).

| ID | Path (`demo/web/public/`) | Type | Linked resource | Status |
|----|---------------------------|------|-----------------|--------|
| DEMO-R-01 | `results/exp1/01_exp1_factorial_f1.png` | png | FIG-4.4 | 🔄 REGENERATED 2026-08-03 |
| DEMO-R-02 | `results/exp1/02_exp1_all_metrics.png` | png | TAB-4.2 | 🔄 REGENERATED 2026-08-03 |
| DEMO-R-03 | `results/exp1/03_exp1_delta.png` | png | FIG-4.4 | 🔄 REGENERATED 2026-08-03 |
| DEMO-R-04 | `results/exp1/18_per_class_f1.png` | png | FIG-4.8 | 🔄 REGENERATED 2026-08-03 |
| DEMO-R-05 | `results/exp1/19_training_curves.png` | png | FIG-4.5 | 🔄 REGENERATED 2026-08-03 — ⚠️ **schematic**: per-epoch history not exported; anchored to measured endpoints |
| DEMO-R-06 | `results/exp1/20_confusion_matrix.png` | png | FIG-4.6 | 🔄 REGENERATED 2026-08-03 |
| DEMO-R-07 | `results/exp1/22_exp1_all_6_configs.png` | png | TAB-4.2 | 🔄 REGENERATED 2026-08-03 |
| DEMO-R-08 | `results/exp1/24_roc_curves.png` | png | FIG-4.7 | 🔄 REGENERATED 2026-08-03 — **repurposed**: now per-class recall; per-class ROC-AUC not recorded |
| DEMO-R-09 | `results/exp2/04_exp2_ablation.png` | png | TAB-4.4 | 🔄 REGENERATED 2026-08-03 |
| DEMO-R-10 | `results/exp2/05_exp2_per_stage.png` | png | TAB-4.4 | 🔄 REGENERATED 2026-08-03 — marginal Δ vs the 2·σ_fold band; stages **not rankable** |
| DEMO-R-11 | `results/exp2/13_exp2_clahe_sensitivity.png` | png | FIG-4.9 | 🔄 REGENERATED 2026-08-03 |
| DEMO-R-12 | `results/exp2/23_exp2_individual_ablation.png` | png | TAB-4.4 | 🔄 REGENERATED 2026-08-03 — same marginal-Δ framing as DEMO-R-10 |
| DEMO-R-13 | `results/exp2/exp2_ff_sweep.json` | json | FIG-4.10 | 🔄 REGENERATED 2026-08-03 |
| DEMO-R-14 | `results/exp3/29_exp3_aptos_transfer.png` | png | FIG-4.11 | 🔄 REGENERATED 2026-08-03 |
| DEMO-R-15 | `results/exp3/exp3_aptos_transfer.json` | json | TAB-4.6 | 🔄 REGENERATED 2026-08-03 |
| DEMO-R-16 | `results/exp4/06_exp4_alo.png` | png | TAB-4.7 | 🔄 REGENERATED 2026-08-03 |
| DEMO-R-17 | `results/exp4/07_exp4_iou.png` | png | TAB-4.7 | 🔄 REGENERATED 2026-08-03 |
| DEMO-R-18 | `results/exp4/27_gradcam_overlay.png` | png | FIG-4.12 | ⏸️ KEPT (pre-run illustration) — illustration, no run metric; source image missing |
| DEMO-R-19 | `results/exp4/28_attention_consistency.png` | png | FIG-4.13 | 🔄 REGENERATED 2026-08-03 — **repurposed**: per-image direction of the ALO effect |
| DEMO-R-20 | `results/exp5/08_exp5_generalization.png` | png | FIG-4.15 | 🔄 REGENERATED 2026-08-03 |
| DEMO-R-21 | `results/exp5/09_exp5_G_ratio.png` | png | FIG-4.15 | 🔄 REGENERATED 2026-08-03 |
| DEMO-R-22 | `results/exp5/exp5_degradation.json` | json | TAB-4.8 | 🔄 REGENERATED 2026-08-03 |
| DEMO-R-23 | `results/exp6/10_exp6_device_shift.png` | png | TAB-4.9 | 🔄 REGENERATED 2026-08-03 |
| DEMO-R-24 | `results/exp7/30_exp7_small_data.png` | png | FIG-4.16 | 🔄 REGENERATED 2026-08-03 |
| DEMO-R-25 | `results/exp7/exp7_small_data.json` | json | TAB-4.10 | 🔄 REGENERATED 2026-08-03 |
| DEMO-R-26 | `results/general/11_summary_radar.png` | png | FIG-5.3 | 🔄 REGENERATED 2026-08-03 |
| DEMO-R-27 | `results/general/12_eh3_dominance.png` | png | FIG-5.3 | 🔄 REGENERATED 2026-08-03 |
| DEMO-R-28 | `results/general/14_clinical_metrics.png` | png | TAB-5.4 | 🔄 REGENERATED 2026-08-03 |
| DEMO-R-29 | `results/general/15_calibration.png` | png | TAB-4.3 | 🔄 REGENERATED 2026-08-03 |
| DEMO-R-30 | `results/general/16_image_quality.png` | png | TAB-4.5 | 🔄 REGENERATED 2026-08-03 — **VVI dropped** (not implemented); L0 vs L7 |
| DEMO-R-31 | `results/general/17_computational.png` | png | FIG-5.2 | 🔄 REGENERATED 2026-08-03 |
| DEMO-R-32 | `results/general/21_statistical_tests.png` | png | TAB-5.1 | 🔄 REGENERATED 2026-08-03 |
| DEMO-R-33 | `results/general/25_pipeline_stages_real.png` | png | FIG-3.1 | ⏸️ KEPT (pre-run illustration) — no run metric; source image missing |
| DEMO-R-34 | `results/general/26_bilateral_pair.png` | png | FIG-4.2 | ⏸️ KEPT (pre-run illustration) — no run metric; source image missing |

> Note: `results/exp3/exp3_aptos_transfer.json`, `results/exp5/exp5_degradation.json`, `results/exp7/exp7_small_data.json`, and `results/exp2/exp2_ff_sweep.json` contain dashboard preview numbers; the matching dissertation results remain `❌ MISSING` (§2.4) until the experiments are run.

### 4.2 `diagrams/` — architecture & pipeline diagrams (4 files)

| ID | Path (`demo/web/public/`) | Type | Linked resource | Status |
|----|---------------------------|------|-----------------|--------|
| DEMO-D-01 | `diagrams/01_abstract_model_architecture.png` | png | FIG-3.11 | ✅ AVAILABLE |
| DEMO-D-02 | `diagrams/02_system_architecture.png` | png | DIA-6.1 | ✅ AVAILABLE |
| DEMO-D-03 | `diagrams/03_preprocessing_stages_detailed.png` | png | FIG-3.1 | ✅ AVAILABLE |
| DEMO-D-04 | `diagrams/04_preprocessing_pipeline_vertical.png` | png | FIG-3.1 / DIA-6.2 | ✅ AVAILABLE |

### 4.3 `pipeline/` — per-DR-grade preprocessing renders (430 PNG + 1 JSON)

Real renders of the full preprocessing pipeline applied to one bilateral fundus pair (`left`/`right`) per DR grade. The directory holds **5 grade folders** — `dr00`, `dr01`, `dr02`, `dr03`, `dr04` — **each containing the identical 86-file structure** listed below (so 5 × 86 = 430 PNGs), plus one shared helper JSON. These back the Chapter 3 stage figures (FIG-3.2…FIG-3.9) and the Exp 4 Grad-CAM/attention previews.

**Shared helper:**

| ID | Path (`demo/web/public/`) | Type | Status |
|----|---------------------------|------|--------|
| DEMO-P-COORDS | `pipeline/helpers/coords.json` | json | ✅ AVAILABLE |

**Per-grade 86-file template** (shown for `dr04`; the same relative paths exist under `pipeline/dr00/`, `pipeline/dr01/`, `pipeline/dr02/`, `pipeline/dr03/`). Linked resource shown per stage group; all `✅ AVAILABLE`.

```
# input (2) — raw bilateral pair                                  [→ FIG-3.1]
pipeline/dr04/input/left.png
pipeline/dr04/input/right.png

# Stage 0 — canonical flip (2)                                    [→ FIG-3.2]
pipeline/dr04/preprocessing/stage_0_canonical_flip/left.png
pipeline/dr04/preprocessing/stage_0_canonical_flip/right.png

# Stage 1 — OD-fovea rotation (10: final + od/fovea/midpoint/image overlays) [→ FIG-3.3]
pipeline/dr04/preprocessing/stage_1_od_fovea_rotation/left.png
pipeline/dr04/preprocessing/stage_1_od_fovea_rotation/right.png
pipeline/dr04/preprocessing/stage_1_od_fovea_rotation/od/left.png
pipeline/dr04/preprocessing/stage_1_od_fovea_rotation/od/right.png
pipeline/dr04/preprocessing/stage_1_od_fovea_rotation/fovea/left.png
pipeline/dr04/preprocessing/stage_1_od_fovea_rotation/fovea/right.png
pipeline/dr04/preprocessing/stage_1_od_fovea_rotation/midpoint/left.png
pipeline/dr04/preprocessing/stage_1_od_fovea_rotation/midpoint/right.png
pipeline/dr04/preprocessing/stage_1_od_fovea_rotation/image/left.png
pipeline/dr04/preprocessing/stage_1_od_fovea_rotation/image/right.png

# Stage 2 — FOV crop + resize (2)                                 [→ FIG-3.4]
pipeline/dr04/preprocessing/stage_2_fov_crop_resize/left.png
pipeline/dr04/preprocessing/stage_2_fov_crop_resize/right.png

# Stage 3 — FOV mask (2)                                          [→ FIG-3.5]
pipeline/dr04/preprocessing/stage_3_fov_mask/left.png
pipeline/dr04/preprocessing/stage_3_fov_mask/right.png

# Stage 4 — flat-field correction (2)                            [→ FIG-3.6]
pipeline/dr04/preprocessing/stage_4_flatfield/left.png
pipeline/dr04/preprocessing/stage_4_flatfield/right.png

# Stage 5 — CLAHE: final + cv2 + polar variants (16)             [→ FIG-3.7]
pipeline/dr04/preprocessing/stage_5_clahe/left.png
pipeline/dr04/preprocessing/stage_5_clahe/right.png
pipeline/dr04/preprocessing/stage_5_clahe/cv2/left.png
pipeline/dr04/preprocessing/stage_5_clahe/cv2/right.png
pipeline/dr04/preprocessing/stage_5_clahe/polar/left.png
pipeline/dr04/preprocessing/stage_5_clahe/polar/right.png
pipeline/dr04/preprocessing/stage_5_clahe/polar/1_vessel_detection/left.png
pipeline/dr04/preprocessing/stage_5_clahe/polar/1_vessel_detection/right.png
pipeline/dr04/preprocessing/stage_5_clahe/polar/2_vessel_density/left.png
pipeline/dr04/preprocessing/stage_5_clahe/polar/2_vessel_density/right.png
pipeline/dr04/preprocessing/stage_5_clahe/polar/3_polar_grid_adaptive/left.png
pipeline/dr04/preprocessing/stage_5_clahe/polar/3_polar_grid_adaptive/right.png
pipeline/dr04/preprocessing/stage_5_clahe/polar/4_density_grid_adaptive/left.png
pipeline/dr04/preprocessing/stage_5_clahe/polar/4_density_grid_adaptive/right.png
pipeline/dr04/preprocessing/stage_5_clahe/polar/5_clahe_no_interpolation/left.png
pipeline/dr04/preprocessing/stage_5_clahe/polar/5_clahe_no_interpolation/right.png

# Stage 6 — augmentation (42)                                    [→ FIG-3.8]
#   1_rotation (22)
pipeline/dr04/preprocessing/stage_6_augmentation/1_rotation/distribution.png
pipeline/dr04/preprocessing/stage_6_augmentation/1_rotation/distribution_adaptive.png
pipeline/dr04/preprocessing/stage_6_augmentation/1_rotation/left.png
pipeline/dr04/preprocessing/stage_6_augmentation/1_rotation/left_contours.png
pipeline/dr04/preprocessing/stage_6_augmentation/1_rotation/left_distribution_normal.png
pipeline/dr04/preprocessing/stage_6_augmentation/1_rotation/left_distribution_step.png
pipeline/dr04/preprocessing/stage_6_augmentation/1_rotation/left_distribution_step_mono.png
pipeline/dr04/preprocessing/stage_6_augmentation/1_rotation/left_peaks.png
pipeline/dr04/preprocessing/stage_6_augmentation/1_rotation/left_sectors.png
pipeline/dr04/preprocessing/stage_6_augmentation/1_rotation/left_sectors_mono.png
pipeline/dr04/preprocessing/stage_6_augmentation/1_rotation/left_variant_A.png
pipeline/dr04/preprocessing/stage_6_augmentation/1_rotation/left_variant_B.png
pipeline/dr04/preprocessing/stage_6_augmentation/1_rotation/right.png
pipeline/dr04/preprocessing/stage_6_augmentation/1_rotation/right_contours.png
pipeline/dr04/preprocessing/stage_6_augmentation/1_rotation/right_distribution_normal.png
pipeline/dr04/preprocessing/stage_6_augmentation/1_rotation/right_distribution_step.png
pipeline/dr04/preprocessing/stage_6_augmentation/1_rotation/right_distribution_step_mono.png
pipeline/dr04/preprocessing/stage_6_augmentation/1_rotation/right_peaks.png
pipeline/dr04/preprocessing/stage_6_augmentation/1_rotation/right_sectors.png
pipeline/dr04/preprocessing/stage_6_augmentation/1_rotation/right_sectors_mono.png
pipeline/dr04/preprocessing/stage_6_augmentation/1_rotation/right_variant_A.png
pipeline/dr04/preprocessing/stage_6_augmentation/1_rotation/right_variant_B.png
#   2_scale (5)
pipeline/dr04/preprocessing/stage_6_augmentation/2_scale/distribution.png
pipeline/dr04/preprocessing/stage_6_augmentation/2_scale/left_max.png
pipeline/dr04/preprocessing/stage_6_augmentation/2_scale/left_min.png
pipeline/dr04/preprocessing/stage_6_augmentation/2_scale/right_max.png
pipeline/dr04/preprocessing/stage_6_augmentation/2_scale/right_min.png
#   3_shear (5)
pipeline/dr04/preprocessing/stage_6_augmentation/3_shear/distribution.png
pipeline/dr04/preprocessing/stage_6_augmentation/3_shear/left_max.png
pipeline/dr04/preprocessing/stage_6_augmentation/3_shear/left_min.png
pipeline/dr04/preprocessing/stage_6_augmentation/3_shear/right_max.png
pipeline/dr04/preprocessing/stage_6_augmentation/3_shear/right_min.png
#   4_pca_color_jitter (5)
pipeline/dr04/preprocessing/stage_6_augmentation/4_pca_color_jitter/distribution.png
pipeline/dr04/preprocessing/stage_6_augmentation/4_pca_color_jitter/left_max.png
pipeline/dr04/preprocessing/stage_6_augmentation/4_pca_color_jitter/left_min.png
pipeline/dr04/preprocessing/stage_6_augmentation/4_pca_color_jitter/right_max.png
pipeline/dr04/preprocessing/stage_6_augmentation/4_pca_color_jitter/right_min.png
#   5_brightness_contrast (5)
pipeline/dr04/preprocessing/stage_6_augmentation/5_brightness_contrast/distribution.png
pipeline/dr04/preprocessing/stage_6_augmentation/5_brightness_contrast/left_max.png
pipeline/dr04/preprocessing/stage_6_augmentation/5_brightness_contrast/left_min.png
pipeline/dr04/preprocessing/stage_6_augmentation/5_brightness_contrast/right_max.png
pipeline/dr04/preprocessing/stage_6_augmentation/5_brightness_contrast/right_min.png

# Stage 7 — normalize (2)                                         [→ FIG-3.9]
pipeline/dr04/preprocessing/stage_7_normalize/left.png
pipeline/dr04/preprocessing/stage_7_normalize/right.png

# results — gradcam / attention / prediction overlays (6)        [→ FIG-4.12 / FIG-4.13]
pipeline/dr04/results/gradcam/left.png
pipeline/dr04/results/gradcam/right.png
pipeline/dr04/results/attention_overlay/left.png
pipeline/dr04/results/attention_overlay/right.png
pipeline/dr04/results/prediction/left.png
pipeline/dr04/results/prediction/right.png
```

> The `pipeline/dr0X/preprocessing/` renders (Stages 0–7) are **real pipeline outputs** and directly back Chapter 3's stage figures. The `pipeline/dr0X/results/` overlays (gradcam/attention/prediction) are dashboard previews; the corresponding quantitative Exp 4 results remain `❌ MISSING` (§2.4).
