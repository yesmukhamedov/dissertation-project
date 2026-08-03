# Conclusions — Experiment 6 (device/camera shift, H-6) → §4.7

**What was done.** Models trained on EyePACS were evaluated on five groups defined by camera
manufacturer (IDRiD/Kowa, DDR, ODIR-5K, Messidor-2/Topcon, RFMiD). The metric is g_ratio against each
arm's own in-domain wF1 (C: 0.7538, D: 0.8193), with a floor of g_floor = 0.7. Source: the
**2026-08-03** run.

## What was found

**1. The generalization threshold is cleared by every group and both arms.** The pipeline's minimum
g_ratio is 0.7863 (mixed_rfmid), a margin of 0.086 over the threshold. `h6_supported = true`.

**2. The main result is not the threshold but the spread.** Since both arms clear the threshold, the
mere fact of "g ≥ 0.7" does not discriminate between them. The substantive difference is the
**significant reduction in between-camera spread**: std(wF1) 0.0262 → 0.0133 (a factor of 2.0,
CI [−0.0186, −0.0049]), std(ROC-AUC) 0.0209 → 0.0064 (a factor of 3.3, CI [−0.0247, −0.0085]). Both
CIs exclude zero. The g_ratio range contracts from 0.7355–0.8331 (span 0.098) to 0.7863–0.8349
(span 0.049).

**3. The levelling mechanism: the pipeline raises the floor rather than the ceiling.** The gain is
larger the worse a group performed under baseline: the largest Δ wF1 are for mixed_rfmid (+0.0898,
C's worst group) and mixed_odir5k (+0.0836, the second worst); the smallest is topcon_messidor2
(+0.0560, C's best group). It is exactly this negative relationship "gain ↔ initial quality" that
produces the contraction of the spread.

**4. Consistent with the measured domain distance.** The largest MMD reductions are likewise for
ODIR-5K (Δd +0.0937) and RFMiD (+0.0864), and the smallest for Messidor-2 (+0.0586). The ordering of
the groups by size of gain matches the ordering by distance reduction
(`tables/H-3_domain_distance.md`).

**5. Improvement on every metric and every class.** ROC-AUC rises in all five groups (+0.024…+0.067),
κ in all five (+0.069…+0.120), and referable AUC in all five (0.851–0.910 → 0.910–0.946). Per-class
F1: the pipeline wins in **all 25 cells** (5 groups × 5 classes), without exception.

**6. Clinically — the operating point is both better and more stable.** Sens/Spec/PPV/NPV improve in
all five groups. The sensitivity range narrows from 0.655–0.750 (span 0.096) to 0.793–0.834
(span 0.041).

**7. No exceptions in this run.** g_ratio rises in **all five** groups, including topcon_messidor2
(0.8331 → 0.8349), where the previous run showed an inversion. There the g_ratio gain is marginal
(+0.0018) against a clear absolute gain (wF1 0.6280 → 0.6840) — the ratio is damped by the pipeline's
larger denominator (in-domain 0.8193 against 0.7538). Flag that g_ratio understates the advantage by
construction.

**8. What the pipeline does not change.** The difficulty ordering of the classes is the same for both
arms and in every group (DR0 ≫ DR2 > DR4 > DR3 ≫ DR1), and the ordering of the groups by weighted-F1
is also preserved (best — topcon_messidor2, worst — mixed_rfmid). The residual difference between the
sets is substantive in nature (population composition, imaging protocol) and is not eliminated by
preprocessing — consistent with the preservation of the domain ranking by MMD.

## For the thesis

Formulation: "the pipeline preserves performance above the generalization floor on every camera group
and **significantly reduces the between-camera spread** (std wF1 by 2.0×, std AUC by 3.3×), lifting
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
