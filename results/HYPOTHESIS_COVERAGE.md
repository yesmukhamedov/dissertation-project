# HYPOTHESIS_COVERAGE — coverage of the HYPOTHESIS.md requirements by the real data

A reconciliation of the **literal text** of `thesis/governance/HYPOTHESIS.md` (v6.2.0) with what the
**2026-08-03** run delivers. The aim is a list of what still has to be run in `experiments/` so that
`results/` closes the hypotheses as worded, not merely "in spirit".

Updated 2026-08-03. Complements `GAP_ANALYSIS.md` (which reconciles the needs of the
chapters/demo/defense; this one covers the requirements of the hypotheses).

> `thesis/` is read-only. No edits to the text of the hypotheses are proposed here; this file covers
> only what can be resolved by running experiments or by code in `experiments/`.

---

## Summary: state of the gaps after the 2026-08-03 run

| # | Hypothesis | Gap | Status |
|---|----------|--------|--------|
| ~~G-1~~ | H-5 | Evaluation on 5 masks instead of 54 | ✅ closed 2026-07-28; the 2026-08-03 run confirms it on n = 54 |
| ~~G-2~~ | H-5 | No paired significance test | ✅ closed — Wilcoxon + bootstrap CIs + threshold sweep; **4/4 types significant** |
| **G-3** | H-5 | No qualitative Grad-CAM overlays on the **clinical (KZ) dataset** — `exp4_explainability.py` has no clinical branch | 🔴 **OPEN** — the only one left for H-5 · code + run, ~2 h |
| ~~G-4~~ | H-4 | exp3 was computed before the Stage-2 fix | ✅ closed; the 2026-08-03 run was executed on the corrected code |
| ~~G-5~~ | H-2 | Flat-field σ sweep not implemented | ✅ **CLOSED BY THE RUN** — 6 points 0.05–0.10·D, σ\* = 0.07, held-out +0.0574 |
| ~~G-6~~ | H-2 | Sweep only over `clahe_clip_factor`; combinations with `global_threshold` needed | ✅ **CLOSED BY THE RUN** — 7 × 5 two-dimensional grid, θ\* = (2.5, 0.03) |
| ~~G-7~~ | H-2 | Sweep performed on IDRiD, the hypothesis says "on EyePACS" | ✅ **CLOSED BY THE RUN** — sweeps and ablation on EyePACS 100% |
| **G-8** | H-2 | Stage 1 and Stage 3 not isolated | 🟡 **PARTIAL** — Stage 1 is isolated (level L2); **Stage 3 (FOV mask) is not**: L3 adds Stages 2–3 jointly. Requires a flag + a 3-channel model variant |
| ~~G-9~~ | H-1 | `C`/fold3 truncated at ep13 | ✅ **CLOSED BY THE RUN** — best epochs of C per fold are 15, 17, 14, 16, 15; no anomalies |
| **G-10** | H-1 | Offline B/D predictions did not reproduce training (cache vs live pipeline) | 🟡 **NEEDS VERIFICATION** — in the new run the per-class/confusion figures agree with the summary metrics, but this can only be confirmed against the raw artifacts, which are not yet available |
| ~~G-11~~ | H-1 | Significance only on referable AUC, no test on wF1 | ✅ **CLOSED BY THE RUN** — McNemar on the fraction correct + Holm correction + per-instance bootstrap CIs on wF1 for all 4 configs |
| ~~G-12~~ | H-7 | exp5 predated the fix | ✅ **CLOSED BY THE RUN** — the whole experiment suite was recomputed |
| **NEW-1** | all | **The raw artifacts of the 2026-08-03 run are absent from `experiments/outputs/`**; `results/data/*.json` contain numbers from the previous run | 🔴 **OPEN** — blocks carrying numbers into the chapters |
| **NEW-2** | H-3 | The MMD kernel, per-domain sample size and number of bootstrap iterations are not recorded in the run data | 🟡 must be extracted from the experiment configuration before writing §4.4/§5 |

**Open in total: G-3, G-8 (remainder), NEW-1, NEW-2**; under verification — G-10.

---

## H-1 — Integrated Pipeline Dominance (exp1)

**Requires:** accuracy, precision, recall, F1 (macro **and** weighted), ROC-AUC, κ(quadratic);
"statistically significantly higher"; the dominance criterion ΔwF1 ≥ 5 pp ∧ ΔAUC ≥ 0.02 ∧ no
degradation in κ; the integrated arm to be initialized with ophthalmological SSL that has passed the
linear-probe gate.

**Available:** all 4 primary metrics × A–D × 5 folds; macro-F1, per-class precision/recall, confusion
matrices, ECE/Brier, clinical metrics; DeLong + McNemar + **Holm correction** + mixed-effects ANOVA;
per-instance bootstrap CIs; the continual-SSL probe gate passed on both backbones.
**Verdict `h1_supported = true`** — all three components of EH-3 are met on both backbones.

**Closed:** G-9 (convergence normal in all folds), G-11 (significance shown not only on referable AUC
but also on the fraction of correct predictions, with correction for multiplicity).

**Open / changed:**
- **G-10** — requires verification against the raw artifacts once they are available (NEW-1).
- **Protocol deviation — the status has softened.** The hypothesis names BYOL from scratch on a
  4-channel tensor; BYOL still collapses, but **SIP from scratch passes the gate** (κ 0.653). In
  practice continual-SSL is used. This goes into the text as a caveat about the choice of method,
  not as an admission that the from-scratch approach failed.
- **CFC-2.8 — its form has changed.** The composite "preprocessing × initialization" is now
  **decomposable**: under a single initialization the exp2 ablation yields the same +0.0655, and its
  endpoints numerically coincide with Config C and D. H-1 no longer rests on an indivisible composite.

## H-2 — CLAHE/σ Sensitivity + Component Ablation (exp2)

**Requires:** (a) varying **clip_factor and global_threshold** "across controlled values … on
EyePACS", per-class F1 for DR1 and DR2 with ≥1 local optimum; (b) a flat-field σ sweep over 0.05–0.10·D;
(c) a component ablation.

**Available:** (a) a 7 × 5 two-dimensional grid on EyePACS plus separate F1(DR1) and F1(DR2) grids,
interior optima θ\* = (2.5, 0.03), θ̂(DR1) = (2.5, 0.03), θ̂(DR2) = (2.0, 0.03), held-out +0.0599;
(b) a 6-point σ sweep with a unimodal maximum at σ\* = 0.07, held-out +0.0574; (c) an 8-level
cumulative ablation on EyePACS 100% × 5 folds, all 7 transitions significant **and rankable**
(Δⱼ 0.0065–0.0143, spread ≈3·σ_fold; flat-field and CLAHE lead with 41% of the gain between them).

**Closed by the run: G-5, G-6, G-7.** All three requirements in the letter of the hypothesis are met.

**Open:**
- **G-8 (remainder).** Stage 1 (OD-fovea rotation) is isolated by level L2 ✓. **Stage 3 (FOV mask) is
  not isolated**: level L3 adds Stages 2–3 jointly, because `PreprocessingConfig` has no mask toggle —
  the 4th channel is present at every level above L3. *Fix:* a flag + a 3-channel model variant,
  +1 ablation level. The most expensive remaining item.
- The discrepancy between the held-out F1(DR1) and the grid value at θ\* (0.2091 vs 0.4693) —
  needs an explanation when writing §4.3.2; use the held-out value in the text.

## H-3 — Domain Distance (MMD / KL) — new block

**Requires:** a reduction in the distance between the source and target domains.

**Available:** MMD over penultimate-layer features and KL over per-channel histograms for 6 domains;
Δd > 0 in all 6 cases, all 95% CIs exclude zero; KL −34…−38%. `h3_supported = true`.
⚠️ The magnitude of the reduction does not track the transfer gain across domains (ρ ≈ 0.49).

**Open — NEW-2.** The MMD kernel, the per-domain sample size and the number of bootstrap iterations
are not recorded in the run data. For §4/§5 they must be extracted from the experiment configuration.
A separate methodological caveat: MMD is computed in each arm's own feature space, which must be
stated explicitly.

## H-4 — Cross-Dataset Transferability (exp3)

**Requires:** G = F1_APTOS / F1_EyePACS ≥ 0.85 for models with the full pipeline.

**Available:** G_D = 0.8976 ≥ 0.85 ✓, G_C = 0.8577; Δ wF1 +0.0889 (CI excludes 0); per-class,
confusion matrices, referable metrics. `h4_supported = true`. **G-4 closed.**

**Caveat (not cheaply resolvable):** exp3/5/6 were computed from **fold0** checkpoints, so there is
no between-fold variance.

## H-5 — Explainability (exp4)

**Requires:** ALO as the **primary** metric, IoU as secondary; ALO_preproc **significantly** higher;
in addition — **qualitative Grad-CAM overlays on the Kazakhstani clinical dataset**.

**Available:** ALO/IoU over all 54 IDRiD images with masks; **4/4 types significant** (p 0.0007–0.0148),
the same for IoU; a threshold sweep τ = 0.2…0.7; a small floor effect (f₀ = 6/54); arm classification.
`h5_alo_supported = true`. **G-1, G-2 closed.**

**Open:**
- **G-3.** There is no clinical branch in `exp4_explainability.py`: the word `clinical` appears only
  in comments about NC-14. The dataset is available (`E:/datasets/clinical`, used by exp7). What is
  needed is a block that "runs both models on N clinical images and saves the overlays" — the
  qualitative part of H-5; no separate training required. **The only gap still open for this hypothesis.**

## H-6 — Device Robustness (exp6) — no gaps

5 camera groups, between-group variance, g_ratio; all 5 groups above the floor for both arms; std wF1
shrinks by a factor of 2.4 (CI excludes 0). `h6_supported = true`. Caveat: fold0 checkpoints.
Protocol change: `mixed_rfmid` is now evaluated on the 5-class scale (previously binary only).
Note: g_ratio falls in 2 of 5 groups — a denominator artifact, absolute wF1 rises in all five.

## H-7 — Clinical Degradation Resistance (exp5)

**Available:** Δ for IDRiD and Messidor-2, 95% CIs, p, Δ_drop for both arms. **G-12 closed.**

**The result is 0/2 — not supported as written — and this is not a data gap but a property of the
criterion.** Δ_drop is measured from each arm's own in-domain level and structurally penalizes the
stronger arm. An additional run will not change this; indeed the criterion has now failed on both
sets in the current run after passing on one in the previous. *What can be done:* record relative
degradation (Δ_drop / in-domain) as a supplementary quantity — a computation over existing numbers,
not a run.

---

## Recommended order of work

**Priority 1 — blocks chapter writing:**
**NEW-1** (publish the raw run artifacts into `experiments/outputs/`, update `results/data/`).
Without it, the numbers in the chapters will not be traceable to a source.

**Priority 2 — cheap, closes the letter of the hypotheses:**
**G-3** (clinical overlays, ~2 h, code + run) → **NEW-2** (extract the MMD parameters from the config).

**Priority 3 — expensive training:**
**G-8 remainder** (FOV-mask flag + 3-channel model variant + ablation level).

**G-10** gets verified along the way while closing NEW-1.

After each step — mark it here and in `TODO_BEFORE_WRITING.md`.
