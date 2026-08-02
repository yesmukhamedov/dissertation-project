# Conclusions — Experiment 1 (2×2 factorial, H-1) → §4.2

**What was done.** A full 2×2 factorial design on EyePACS (100%, n = 35 126, 5-fold patient-level CV):
{baseline 3ch / full pipeline 4ch} × {ResNet-50 / EfficientNet-B3} = configurations A, B, C, D.
A test of EH-3 dominance of the pipeline over baseline. Source of the numbers: the **2026-08-02** run.

## What was found

**1. The pipeline dominates under the strict criterion, on both backbones.** All three components of
EH-3 are met with margin: ΔwF1 +6.54 pp (B−A) and +6.55 pp (D−C) against a 5 pp threshold; ΔAUC +0.032
and +0.036 against a 0.02 threshold; Δκ +0.113 and +0.110 against a requirement of merely "does not
degrade". `h1_supported = true`.

**2. The effect is significant and architecture-independent.** DeLong on referable AUC: p = 0.0041
and 0.0028; McNemar: p = 0.0057 and 0.0041; after the Holm correction over 4 configurations — 0.0082
and 0.0056, both below α = 0.05. The mixed-effects ANOVA finds no "arm × backbone" interaction
(p = 0.31) — the effect size for ResNet-50 and EfficientNet-B3 is statistically the same, which is
also confirmed numerically (6.54 vs 6.55 pp). The cross-validation intervals of baseline and pipeline
**do not overlap on any of the four primary metrics**.

**3. The gain is concentrated on the minority classes.** macro-F1 rises more than weighted-F1: +0.104
against +0.065 (A→B) and +0.106 against +0.066 (C→D). The F1 of class DR1 (mild NPDR) doubles:
0.0999 → 0.2141 and 0.0976 → 0.2188. The absolute DR1 level remains low (≈0.21) — early, subtle signs
remain the main source of error; the pipeline mitigates them but does not solve them.

**4. Errors become "near" ones.** In the confusion matrices the distant cells almost empty out:
DR0 → DR4 falls from 26 to 4 instances (A→B) and DR0 → DR3 from 127 to 33. The bulk of false
positives on healthy images (DR0 → DR1) shrinks from ≈2 950 to ≈1 890. This is precisely what
produces the large quadratic-κ gain, since κ penalizes distant errors more heavily than near ones.

**5. Clinically: higher sensitivity at higher specificity.** Referable DR (grade ≥ 2):
Sens 0.6865 → 0.7982 and 0.6891 → 0.8007 (+11.2 pp), with Spec rising at the same time 0.944 → 0.963
and 0.946 → 0.964. This is a shift of the ROC curve itself (referable AUC +0.041 / +0.042), not a
movement of the operating point along it. PPV +9 pp, NPV +2.6 pp — both missed cases and false
referrals decrease.

**6. Calibration improves.** ECE 0.0712 → 0.0418 and 0.0691 → 0.0402 (roughly 1.7×), with Brier lower
on both backbones. ⚠️ **A sign change relative to the previous run**, where calibration was the
pipeline's only systematic drawback (ECE ~3× worse) and was carried into §5.4 as a mandatory caveat.
Formulations that relied on "the pipeline degrades calibration" must be replaced.

**7. The pipeline acts as a regularizer.** The pipeline arms converge 6–7 epochs earlier (best epochs
7–10 against 14–17) with a loss gap 2.5× smaller (0.021–0.022 against 0.052–0.054). The mechanism is
legible from the components: B/D have a **higher** train_loss (0.126–0.131 against 0.098–0.102) at a
comparable val_loss — the model fits the training set less closely but generalizes no worse. The
spread of best epochs within an arm is small (±1–1.5), so the regime is reproducible across folds.

## Limitation (mandatory in the text) — CFC-2.8 in modified form

The B/D arm is initialized with continual-SSL, so Config B/D formally measure the composite
"preprocessing × initialization". **But the composite is now decomposable:** the exp2 cumulative
ablation on the same corpus, the same split and under **a single initialization at all eight levels**
yields ΔwF1 = +0.0655 from L0 to L7, with L0 = 0.7538 numerically coinciding with Config C and
L7 = 0.8193 with Config D (`tables/TAB-4.4_exp2_ablation.md`). That is, the entire D-vs-C gain is
reproduced by preprocessing at fixed initialization, and the contribution of preprocessing has been
measured separately.

CFC-2.8 goes into the text as a note about a feature of the design, with an immediate reference to
exp2, and **not** as a limitation on the conclusion. This is a substantial change relative to the
previous revision, where H-1 was considered incapable of isolating preprocessing.

## Formulation of the contribution

"The integrated configuration with the 8-stage pipeline dominates baseline on all three components of
the EH-3 criterion on both backbones (ΔwF1 +6.5 pp, ΔAUC +0.032…0.036, Δκ +0.11); the effect is
significant after correction for multiplicity (Holm p ≤ 0.0082), does not depend on the choice of
architecture (interaction p = 0.31) and is reproduced component by component by the cumulative
ablation at fixed initialization."

Tables: `tables/TAB-4.2_exp1_factorial.md`, `TAB-4.3_exp1_calibration.md`, `exp1_per_class.md`,
`exp1_clinical_indomain.md`, `exp1_convergence_ci.md`, `TAB-5.1_statistical.md`.
Card: `hypotheses/H-1.md`.
