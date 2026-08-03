# Conclusions — Experiment 3 (transfer EyePACS→APTOS, H-4) → §4.4

**What was done.** Zero-shot transfer of a model trained on EyePACS to APTOS 2019 (n = 3 662).
The metric is the generalization ratio G = F1_APTOS / F1_EyePACS. H-4 threshold: G ≥ 0.85 and
full > baseline. Source: the **2026-08-03** run.

## What was found

**1. The hypothesis is confirmed on both parts.** G_D = **0.8976** (the threshold cleared with a
margin of 0.048), G_C = 0.8577; the absolute APTOS wF1 is higher by **+0.0889** (CI [+0.0681,
+0.1197]) and AUC by +0.0323 (CI [+0.0224, +0.0482]). `h4_supported = true`.

**2. An important caveat: both arms clear the threshold.** Baseline also passes G ≥ 0.85 (0.8577).
So the "G ≥ 0.85" criterion on its own **does not discriminate** between the arms — what discriminates
them is the second part, "better than baseline", and that is met convincingly. It should be phrased
as "the pipeline does not rescue transfer, it improves transfer that is already acceptable", without
claiming that baseline transfers poorly.

**3. Mechanism: the intermediate grades are held.** That is exactly where transfer usually collapses.
F1(DR2) 0.5747 → 0.6931, F1(DR1) 0.1395 → 0.2720. In the confusion matrix the mass of DR2 → DR1 falls
from 245 to 192 instances and DR2 → DR0 from 96 to 33. There is a gain on **all five** grades;
macro-F1 rises more than weighted-F1 (+0.102 against +0.089) — the same "gain on the minority classes"
pattern as in exp1.

**4. Errors remain adjacent on the scale.** The DR0 → DR4 cell is 2 for baseline and 0 for the
pipeline; DR0 → DR3 goes 8 → 2. The residual error mass concentrates on the DR3↔DR4 boundary
(112 instances) — "severe NPDR vs PDR" remains the hardest boundary on APTOS too. This explains the
large κ gain (0.7887 → 0.8874), since κ penalizes precisely the distant errors.

**5. Clinically — the same gain as in-domain.** Referable DR: Sens 0.7337 → 0.8393 (+10.6 pp) **with
specificity rising at the same time** (0.9209 → 0.9411), referable AUC 0.8944 → 0.9346. The
sensitivity gain (+0.11) matches in-domain (+0.11) and the camera groups (+0.11) — the most
reproducible clinical effect of the pipeline across the entire experiment suite.

**6. Directionally consistent with the measured reduction in domain distance.** The EyePACS↔APTOS MMD
falls from 0.1910 to 0.1178 (Δd +0.0732, CI excludes zero) and KL from 0.0894 to 0.0588 (−34%). See
the H-3 section in `findings/summary-and-dominance.md` and `tables/H-3_domain_distance.md`. ⚠️ Only
the direction is consistent: across the six domains the *size* of the distance reduction does not
predict the size of the gain (APTOS has a below-median Δd but the second-largest gain). State the
mechanism as measured, not as a quantitative predictor.

## For the thesis

Report as a confirmed hypothesis with two explicit caveats: (a) the G ≥ 0.85 threshold is cleared by
both arms, and what discriminates them is the comparison with baseline; (b) evaluation uses fold-0
checkpoints. Substantive formulation: "preprocessing calibrated on the source domain **does not
impede** zero-shot multi-class transfer and improves it on every grade, with the improvement
consistent with the measured reduction in domain distance". This directly removes the former
limitation that was stated in §5.4 on the basis of the previous run.

## Caveats

- Evaluation uses **fold 0** checkpoints; there is no between-fold variance, and the 95% CIs are
  per-instance (bootstrap).
- G is normalized by each arm's **own** in-domain wF1 (C: 0.7538, D: 0.8193). The arm with the higher
  in-domain score has the larger denominator, so the gain in G (+0.040) is by construction more
  conservative than the gain in absolute APTOS wF1 (+0.089) — state this so that the modest ΔG is not
  read as a weak effect.

Table: `tables/TAB-4.6_exp3_transfer.md`. Per-class and matrices: `tables/per_class_and_confusion.md`.
Clinical metrics: `tables/TAB-5.4_clinical_referable.md`. Card: `hypotheses/H-4.md`.
