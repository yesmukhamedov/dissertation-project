# Conclusions — Experiment 6 (device/camera shift, H-6) → §4.7

**What was done.** Models trained on EyePACS were evaluated on five groups defined by camera
manufacturer (IDRiD/Kowa, DDR, ODIR-5K, Messidor-2/Topcon, RFMiD). The metric is g_ratio against each
arm's own in-domain wF1 (C: 0.7538, D: 0.8193), with a floor of g_floor = 0.7. Source: the
**2026-08-03** run.

## What was found

**1. The generalization threshold is cleared by every group and both arms.** The pipeline's minimum
g_ratio is 0.7837 (mixed_rfmid), a margin of 0.084 over the threshold. `h6_supported = true`.

**2. The main result is not the threshold but the spread.** Since both arms clear the threshold, the
mere fact of "g ≥ 0.7" does not discriminate between them. The substantive difference is the
**significant reduction in between-camera spread**: std(wF1) 0.0307 → 0.0127 (a factor of 2.4,
CI [−0.0253, −0.0062]), std(ROC-AUC) 0.0214 → 0.0070 (a factor of 3.1, CI [−0.0233, −0.0072]). Both
CIs exclude zero. The g_ratio range contracts from 0.7209–0.8335 (span 0.113) to 0.7837–0.8311
(span 0.047).

**3. The levelling mechanism: the pipeline raises the floor rather than the ceiling.** The gain is
larger the worse a group performed under baseline: the largest Δ wF1 are for mixed_rfmid (+0.0987,
C's worst group) and mixed_odir5k (+0.0881, the second worst); the smallest are mixed_ddr (+0.0517)
and topcon_messidor2 (+0.0526, C's best group). It is exactly this negative relationship
"gain ↔ initial quality" that produces the contraction of the spread.

**4. Directionally consistent with the measured domain distance.** RFMiD has both the largest MMD
reduction (Δd +0.0931) and the largest gain. ⚠️ Beyond that extreme the two orderings **do not** track
each other — DDR has a middling Δd (+0.0784) but the smallest gain of the six domains, and IDRiD is
2nd on Δd but 4th on gain (`tables/H-3_domain_distance.md`). Do not claim that the ordering by gain
matches the ordering by distance reduction; it did in the previous revision, and no longer does.

**5. Improvement on every metric and every class.** ROC-AUC rises in all five groups (+0.026…+0.063),
κ in all five (+0.073…+0.117), and referable AUC in all five (0.855–0.906 → 0.930–0.946). Per-class
F1: the pipeline wins in **all 25 cells** (5 groups × 5 classes), without exception, and the
between-group spread now contracts on **all five** classes.

**6. Clinically — the operating point is both better and more stable.** Sens/Spec/PPV/NPV improve in
all five groups. The sensitivity range narrows from 0.651–0.748 (span 0.096) to 0.794–0.835
(span 0.041).

**7. g_ratio falls in 2 of 5 groups — a normalization artifact.** mixed_ddr (0.8164 → 0.8142) and
topcon_messidor2 (0.8335 → 0.8311) are the two groups with the smallest absolute gains; absolute wF1
rises in both (0.6154 → 0.6671 and 0.6283 → 0.6809). g_ratio divides by each arm's own in-domain wF1,
and the pipeline's denominator is 6.55 pp larger, so a group must gain ~8% relative just to hold its
ratio. Flag explicitly that g_ratio understates the advantage by construction; the H-6 verdict rests
on the floor criterion and the spread reduction, not on the ratio rising everywhere.

**8. What the pipeline does not change.** The difficulty ordering of the classes is the same for both
arms and in every group (DR0 ≫ DR2 > DR4 > DR3 ≫ DR1), and the ordering of the groups by quality
is also preserved (best — topcon_messidor2, worst — mixed_rfmid). The residual difference between the
sets is substantive in nature (population composition, imaging protocol) and is not eliminated by
preprocessing — consistent with the preservation of the domain ranking by MMD.

## For the thesis

Formulation: "the pipeline preserves performance above the generalization floor on every camera group
and **significantly reduces the between-camera spread** (std wF1 by 2.4×, std AUC by 3.1×), lifting
the most problematic devices above all". Practical implication for deployment: device-specific
threshold recalibration ceases to be mandatory — the former recommendation, derived from the previous
run, is withdrawn. → App F, §5.4.

## Caveats

- Evaluation uses **fold 0** checkpoints; the std in the spread table is **between-group** (over the
  5 groups), not between-fold.
- The `mixed_rfmid` group was evaluated on the 5-class scale in this run (previously binary only) —
  it is not comparable with the earlier numbers.
- The groups overlap with the exp5 sets (`kowa_idrid` = IDRiD, `topcon_messidor2` = Messidor-2); the
  values coincide.

Table: `tables/TAB-4.9_exp6_device.md`. Per-class: `tables/per_class_and_confusion.md`.
Clinical metrics: `tables/TAB-5.4_clinical_referable.md`. Card: `hypotheses/H-6.md`.
