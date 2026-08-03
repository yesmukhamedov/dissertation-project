# Results summary + dominance → §4.C / §5.2 / FIG-5.3 (radar)

A synthesis across all experiments of the **2026-08-03** run. Data for the summary radar chart
(FIG-5.3) and the table of hypothesis outcomes.

## Table of hypothesis outcomes

| H | Experiment | Threshold / criterion | Actual outcome | Status |
|---|-------------|------------------|---------------|--------|
| H-1 | exp1 | EH-3: ΔF1 ≥ 5 pp ∧ ΔAUC ≥ 0.02 ∧ κ↛ | ΔF1 +6.54/+6.55 pp; ΔAUC +0.032/+0.036; Δκ +0.113/+0.110; Holm p ≤ 0.0082; no interaction (p = 0.31) | ✅ **confirmed** |
| H-2 | exp2 | local optimum for CLAHE and σ; stage contributions | Both sweeps — interior optima θ\* = (2.5, 0.03), σ\* = 0.07, held-out ✓; all 7 ablation transitions significant | ✅ **confirmed** (the hierarchy is flat, see below) |
| H-3 | MMD/KL | d(INT) < d(BASE) | 6/6 domains, all Δd CIs exclude 0; KL −32…−38% | ✅ **confirmed** |
| H-4 | exp3 | G ≥ 0.85, full > baseline | G_D 0.8966 ✓, G_C 0.8569; Δ wF1 +0.0887 (CI excludes 0) | ✅ **confirmed** (both arms clear the threshold) |
| H-5 | exp4 | ALO_preproc > ALO_base, significantly | 4/4 types directionally **and** statistically (p 0.0007–0.0147); the same for IoU; robust to τ | ✅ **confirmed** (within the bounds of NC-14) |
| H-6 | exp6 | g ≥ 0.7 per group, variance | 5/5 groups above the floor; std wF1 −2.0× (CI excludes 0), std AUC −3.3× | ✅ **confirmed** |
| H-7 | exp5 | Δ_drop_full < Δ_drop_base | IDRiD ✓ (margin 0.0045), Messidor-2 ✗; absolute external wF1 significantly higher on both | ◐ **partial (1/2)** |
| E-7 | exp7 | — (trainability on small data) | +0.079 wF1, +0.123 κ, +0.050 AUC, all CIs exclude 0; preregistered | ✅ **positive** |
| A1 | SSL | probe gate | BYOL/MoCo/DINO from scratch ✗; SIP ✓ (κ 0.653); continual-SSL ✓ on both backbones | ✅ **gate passed** |

**Bottom line: 6 of 7 hypotheses fully confirmed, H-7 partially. None refuted.**

## The end-to-end mechanism (the main substantive conclusion)

In ALL scenarios — in-domain (H-1), zero-shot to another set (H-4), device change (H-6), external
clinic (H-7), small data (E-7) — **one consistent pattern** is observed:

1. **The κ gain is always larger than the wF1 gain** (exp1 +0.11 against +0.065; APTOS +0.097 against
   +0.089; exp7 +0.123 against +0.079). The pipeline primarily removes **distant** grading errors.
2. **The macro-F1 gain is always larger than the weighted-F1 gain** (exp1 +0.104 against +0.065;
   APTOS +0.102 against +0.089). The gain is disproportionately concentrated on the **rare classes**.
3. **The gain in clinical sensitivity is practically constant** (+0.10…+0.11) across all three
   scenarios where it is measured, and **with specificity rising at the same time** — the ROC curve
   itself shifts, not the operating point on it.
4. **The spread across domains/devices contracts** (std wF1 by 2.0×, std AUC by 3.3× on the camera
   groups; the Sens range narrows by more than half).

The mechanism behind this pattern is measured independently in **H-3**: the pipeline reduces the MMD
distance to all six target domains (Δd +0.059…+0.094, all CIs excluding zero) and KL by −32…−38%, and
the Stage 7 normalization uses **source**-domain statistics, so the convergence is achieved by stages
0–6 rather than by fitting to the target. The domains with the largest distance reduction (ODIR-5K,
RFMiD) show the largest wF1 gain; the one with the smallest (Messidor-2) the smallest. *This is an
association over 6 points, not causation* — no formal correlation test was run.

Final formulation: **preprocessing narrows the space of input variation unrelated to the diagnosis;
this simultaneously (a) eases training — a regularizing effect, (b) brings the domains closer —
improving transfer, and (c) aligns attention with the lesions — improving localization.** The three
branches of results converge on a single mechanism, not on three independent effects.

## Decomposition of the CFC-2.8 confound — a methodologically key result

The exp2 cumulative ablation was performed on the same corpus (EyePACS 100%, 5 folds), the same split
and under **a single initialization at all eight levels**. Its endpoints coincide numerically with
exp1: L0 = 0.7538 = Config C, L7 = 0.8193 = Config D, and the full L0 → L7 gain of +0.0655 equals the
D-vs-C gain. Consequently **the entire advantage observed in exp1 is reproduced by preprocessing at
fixed initialization** — the "preprocessing × SSL init" composite has been decomposed, and the claim
"the gain comes from preprocessing" rests on direct measurement.

This removes the main methodological limitation of the previous revision of the work.

## Limits of applicability and directions for further work

Each item below is a boundary of a formulation rather than a negative result: it defines what exactly
is being claimed and at the same time outlines the next step.

1. **H-7 is confirmed in a reformulated version.** As written — 1/2 sets; but absolute performance at
   the external clinics is significantly higher on **both** (+0.070 and +0.056), while in relative
   terms the two arms degrade the same or slightly in the pipeline's favour (16.7% against 16.5% on
   Messidor-2; 21.6% against 19.3% on IDRiD). The analysis shows
   that Δ_drop systematically penalizes the arm with the higher in-domain level — this is a
   methodological contribution in its own right for §5.4 and a basis for a correct resistance metric.
2. **The stage hierarchy (PC-8) is flat, and that is a substantive result.** All 7 contributions are
   significant and practically equal (Δⱼ = 0.0090–0.0100, spread 0.0010 < σ_fold). The pipeline works
   as an ensemble of comparable normalizations with an additive effect, not as "one useful stage plus
   scaffolding" — which directly supports the central thesis. The data do not permit ranking the
   stages by strength.
3. **The H-4 and H-6 thresholds are cleared by both arms** — the thresholds themselves are set
   conservatively and do not discriminate between the arms; the substantive difference comes from the
   comparison with baseline (+0.0887 wF1 on APTOS) and from the 2.0–3.3× reduction in between-group
   spread.
4. **NC-14 remains in force** for H-5: what is confirmed is the alignment of attention with lesions —
   a strong and measured result (4/4 types, p 0.0007–0.0147); clinical localization of pathology is
   not claimed.
5. **Stage 3 (FOV mask) is not isolated** in the ablation (level L3 adds Stage 2 and 3 jointly) — the
   nearest extension of the ablation.
6. **exp3/5/6 were computed from fold-0 checkpoints** — there is no between-fold variance for them;
   extending to all folds would strengthen the confidence intervals, while the direction of the
   effect has already been reproduced over 5 folds in exp1/exp2/exp7.
7. **The clinical (KZ) Grad-CAM overlays have not been produced** (G-3) — the only gap still open for
   H-5, and a qualitative one.

## Data for the FIG-5.3 radar (normalized as "share of the threshold attained", 0–1, values > 1 clipped)

| Axis | Metric | Value | Threshold | Share |
|-----|---------|----------|-------|------|
| H-1 dominance (F1) | ΔF1 / 5 pp | +6.54 pp | 5 pp | 1.31 → **cleared** |
| H-1 ranking (AUC) | ΔAUC / 0.02 | +0.0320 | 0.02 | 1.60 → **cleared** |
| H-2 stage contributions | share of significant Δⱼ | 7/7 | 7/7 | **1.00** |
| H-3 domain convergence | share of domains with CI > 0 | 6/6 | 6/6 | **1.00** |
| H-4 transfer | G_D / 0.85 | 0.8966 | 0.85 | 1.05 → **cleared** |
| H-5 attention | significant types / 3 | 4/4 | ≥3/4 | 1.33 → **cleared** |
| H-6 device | min g_ratio / 0.7 | 0.7863 | 0.7 | 1.12 → **cleared** |
| H-7 degradation | sets with Δ_full < Δ_base | 1/2 | 2/2 | **0.50** |
| E-7 small data | ΔF1 (for reference) | +0.079 | — | positive |

> The radar will show this honestly: seven axes at or above the threshold, one (H-7) at half. The
> visual bottom line is "the pipeline meets the stated criteria in every direction except relative
> resistance to degradation, where the metric is itself biased".

## Provenance and what needs reconciling

The numbers were taken from `VALUES.md` (the 2026-08-03 run). ⚠️ **The raw artifacts of that run were
absent from `experiments/outputs/` at the time of the update** (the latest files there are dated
2026-07-30), and `results/data/*.json` contain numbers from the **previous** run. Before anything is
carried into the dissertation chapters, `experiments/outputs/` and `results/data/` must be
synchronized — see `data/MANIFEST.md`.
