# TODO — what to do BEFORE writing the dissertation (working checklist)

> Temporary working file. Delete/archive once everything is closed out and chapter writing has begun.
> State — after the **2026-08-03** run. Full analysis in [GAP_ANALYSIS.md](GAP_ANALYSIS.md);
> experiment statuses in [STATUS.md](STATUS.md); what the chapters need in
> [CHAPTER_STATUS.md](CHAPTER_STATUS.md); the letter of the hypotheses in
> [HYPOTHESIS_COVERAGE.md](HYPOTHESIS_COVERAGE.md).

## Already done ✅

- [x] The results layer for all experiments is assembled: metrics, tables (`tables/`), hypothesis
      cards (`hypotheses/`), narrative conclusions (`findings/`).
- [x] **Category A** (derivable without training) — closed: clinical metrics, per-class, claim
      strength, summary/radar, convergence and CIs, computational benchmarks, image quality.
- [x] **Category B** (per-instance quantities from exp1) — closed: per-class/confusion, calibration,
      in-domain clinical metrics, paired statistical tests (DeLong, McNemar, **Holm**,
      **mixed-effects ANOVA**), bootstrap CIs.
- [x] **Category C** (unfinished experiments) — closed: 8-level cumulative ablation on
      EyePACS 100% × 5 folds; two-dimensional CLAHE sweep on EyePACS; **flat-field σ sweep** (had not
      been implemented); Grad-CAM ALO/IoU on all 54 masks with paired tests and a threshold sweep.
- [x] **Gaps G-1, G-2, G-4, G-5, G-6, G-7, G-9, G-11, G-12** — closed.
- [x] The new **H-3** block (domain distance, MMD/KL) is assembled: `tables/H-3_domain_distance.md`,
      `hypotheses/H-3.md`.
- [x] All values and verdicts in `results/` have been rewritten for the 2026-08-03 run, preserving
      the structure.

---

## PHASE 1 — blocking

- [ ] 🔴 **NEW-1. Restore provenance.** Publish the raw artifacts of the 2026-08-03 run into
      `experiments/outputs/exp{1..7}/` and `outputs/ssl*/`: `summary.json`, `*_results.json`,
      `metrics.csv`, `predictions.npz`, the σ-sweep and two-dimensional CLAHE grid artifacts, and the
      MMD/KL results for H-3. Then update `results/data/*.json` and remove the warnings in
      `data/MANIFEST.md` and `INTEGRITY_NOTE.md` §1.
      **Why it blocks:** right now `results/data/` and `experiments/outputs/` contain numbers from the
      PREVIOUS run with the opposite verdicts — cross-checking is impossible and the numbers in the
      chapters cannot be traced back to a source.
      This also closes **G-10** along the way (reconciling the offline B/D predictions with training).

---

## PHASE 2 — close the letter of the hypotheses

- [ ] 🔴 **G-3. Grad-CAM overlays on the clinical (KZ) dataset.** `exp4_explainability.py` has no
      clinical branch at all (the word `clinical` appears only in comments about NC-14).
      The dataset is available: `E:/datasets/clinical` (used by exp7). What is needed is a block that
      "runs both models on N clinical images and saves the overlays" — no separate training required.
      Estimate ~2 h. **The only gap still open for H-5.**
- [ ] 🟡 **NEW-2. MMD parameters.** Extract the MMD kernel, the per-domain sample size and the number
      of bootstrap iterations from the experiment configuration — needed for the methodological part
      of §4/§5 on H-3.
- [ ] 🟡 **G-8 (remainder). Isolate Stage 3 (FOV mask).** Level L3 currently adds Stages 2–3 jointly:
      `PreprocessingConfig` has no mask toggle, and the 4th channel is present at every level above
      L3. Requires a flag + a 3-channel model variant + one ablation level. The most expensive item;
      if time is short, declare it as a limitation.

---

## PHASE 3 — computations and exports from existing data (no runs required)

- [ ] **R1.** Relative degradation (Δ_drop / in-domain) for H-7 — arithmetic over `TAB-4.8`.
      Needed for an honest formulation of §4.6 and the methodological critique of the Δ_drop metric in §5.4.
- [ ] **R2.** ROC/PR curves as figures — from the `predictions.npz` of the new run (after NEW-1).
- [ ] **R3.** Confusion matrices for the 5 camera groups (exp6) — the run data record only per-class
      F1; an additional export is needed for App F.
- [ ] **TAB-5.3.** Comparison with published systems (IDx-DR, EyeNuk, DeepMind) — a literature task,
      not an experiment.

---

## PHASE 4 — synchronize the consumers

- [ ] **S1.** Update `thesis/ASSET_INVENTORY.md` to the real statuses (all exp ✅; 6 hypotheses
      confirmed, H-7 partial; the H-3 block added).
- [ ] **S2.** Rebuild `demo/web/src/data.js` from the real numbers; remove the invented `IQ` (VVI)
      and the incorrect `COMPUTE` (25.6M/12.2M → 23.52M/10.70M); `HYPOTHESES` — real verdicts
      including H-3 and the partial status of H-7. Rebuild `demo/web/generate_charts_*.py` from `outputs/`.
- [ ] **S3.** Update the defense slides `defense/presentation/slides/33–43_*` and the narrative
      scripts to the real values.

---

## PHASE 5 — write

- [ ] **Decide where H-3 goes** in the structure of chapter 4 (its own section, or part of §4.4) —
      this affects section numbering and TAB/FIG numbering.
- [ ] Order (from `CHAPTER_STATUS.md`): §4.2 · §4.3 · §4.4 · H-3 · §4.6 · §4.7 · §4.8 →
      §5.2.1/§5.2.2 → §4.5 + §5.1 (after G-3) → §4.C · §5.4 · §5.3 · ch. 7 · ch. 0/§0.8.
      Workflow: brief→draft→continuity→review→translation.

**Rules:**
- Any numbers come only from `results/`, NEVER from `demo/web/data.js`.
- 🚫 **Provenance does not carry into the text.** Run dates, the history of recomputations, artifact
  paths (`experiments/outputs/**`, `VALUES.md`, `*.log`), checkpoints/epochs and process metadata
  stay in `results/`. In the chapters and in `defense/`, a result is a property of the experiment,
  not of a dated run. Methodological facts (folds, sample sizes, stopping rule, single-fold
  evaluation as a limitation) must be carried over. Rule:
  `thesis/prompts/writing-session-system-prompt.md` §16. This applies to **S3** as well — the defense
  slides are built on values, without references to runs and logs.
- The list of formulations that need to be replaced relative to the previous revision is in
  `CHAPTER_STATUS.md`, table "What changed in the content".
- Confirmation of the hypotheses **does not repeal** `INVARIANTS.md`: NC-14 is in force for H-5; the
  H-4/H-6 thresholds are met by both arms; H-7 is partial. The list of limitations is in
  `findings/summary-and-dominance.md`.
