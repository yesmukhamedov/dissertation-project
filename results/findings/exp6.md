# Conclusions — Experiment 6 (device/camera shift, H-6) → §4.7

**What was done.** Models trained on EyePACS were evaluated on five groups defined by camera
manufacturer (IDRiD/Kowa, DDR, ODIR-5K, Messidor-2/Topcon, RFMiD). The metric is g_ratio against each
arm's own in-domain wF1 (C: 0.7538, D: 0.8193), with a floor of g_floor = 0.7. Source: the
**2026-08-02** run.

## What was found

**1. The generalization threshold is cleared by every group and both arms.** The pipeline's minimum
g_ratio is 0.7909 (mixed_rfmid), a margin of 0.09 over the threshold. `h6_supported = true`.

**2. The main result is not the threshold but the spread.** Since both arms clear the threshold, the
mere fact of "g ≥ 0.7" does not discriminate between them. The substantive difference is the
**significant reduction in between-camera spread**: std(wF1) 0.0281 → 0.0106 (a factor of 2.6,
CI [−0.0268, −0.0082]), std(ROC-AUC) 0.0210 → 0.0068 (a factor of 3.1, CI [−0.0221, −0.0063]). Both
CIs exclude zero. The g_ratio range contracts from 0.7310–0.8318 (span 0.101) to 0.7909–0.8275
(span 0.037).

**3. The levelling mechanism: the pipeline raises the floor rather than the ceiling.** The gain is
larger the worse a group performed under baseline: the largest Δ wF1 are for mixed_rfmid (+0.0970,
C's worst group) and mixed_odir5k (+0.0880, the second worst); the smallest is topcon_messidor2
(+0.0510, C's best group). It is exactly this negative relationship "gain ↔ initial quality" that
produces the contraction of the spread.

**4. Consistent with the measured domain distance.** The largest MMD reductions are likewise for
RFMiD (Δd +0.0880) and ODIR-5K (+0.0850), and the smallest for Messidor-2 (+0.0630). The ordering of
the groups by size of gain matches the ordering by distance reduction
(`tables/H-3_domain_distance.md`).

**5. Improvement on every metric and every class.** ROC-AUC rises in all five groups (+0.029…+0.065),
κ in all five (+0.074…+0.123), and referable AUC in all five (0.853–0.908 → 0.914–0.942). Per-class
F1: the pipeline wins in **all 25 cells** (5 groups × 5 classes), without exception.

**6. Clinically — the operating point is both better and more stable.** Sens/Spec/PPV/NPV improve in
all five groups. The sensitivity range narrows from 0.654–0.748 (span 0.094) to 0.791–0.836
(span 0.045).

**7. The only exception is topcon_messidor2**, where the pipeline's g_ratio is slightly lower (0.8275
against 0.8318). Its absolute wF1 is nevertheless higher (0.6780 against 0.6270); the drop in g_ratio
is entirely explained by the larger denominator (in-domain 0.8193 against 0.7538). Flag it as a
normalization artifact, not as a counterexample.

**8. What the pipeline does not change.** The difficulty ordering of the classes is the same for both
arms and in every group (DR0 ≫ DR2 > DR4 > DR3 ≫ DR1), and the ordering of the groups by quality is
also preserved (best — topcon_messidor2, worst — mixed_rfmid). The residual difference between the
sets is substantive in nature (population composition, imaging protocol) and is not eliminated by
preprocessing — consistent with the preservation of the domain ranking by MMD.

## For the thesis

Formulation: "the pipeline preserves performance above the generalization floor on every camera group
and **significantly reduces the between-camera spread** (std wF1 by 2.6×, std AUC by 3.1×), lifting
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
