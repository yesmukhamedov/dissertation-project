# TAB-4.3 — exp1 calibration (ECE, Brier)

Source: the **2026-08-02** run (`VALUES.md` §1.5). n = 35 126, pooled val folds.

| Config | Arm | ECE | Brier |
|---|---|---|---|
| A | baseline + ResNet-50 | 0.0712 | 0.0724 |
| B | pipeline + ResNet-50 | **0.0418** | **0.0611** |
| C | baseline + EffNet-B3 | 0.0691 | 0.0715 |
| D | pipeline + EffNet-B3 | **0.0402** | **0.0598** |

**Observation.** The pipeline arms are **better** calibrated than baseline on both backbones: ECE
falls by roughly a factor of 1.7 (0.0712 → 0.0418 and 0.0691 → 0.0402), and Brier by 0.011–0.012.
That is, the integrated configuration improves not only ranking (AUC) and agreement (κ) but also the
reliability of the probabilities themselves.

> **Sign change relative to the previous run.** In the run prior to 2026-07-28, calibration was the
> pipeline's only systematic drawback (ECE for B/D 0.19–0.21 against 0.06–0.07 for A/C, ~3× worse),
> and this was carried into §5.4 as a mandatory caveat that "recalibration is required before
> deployment". Per the 2026-08-02 run this drawback has **disappeared and turned into an advantage**.
> Formulations in chapters 4/5 that relied on "the pipeline degrades calibration" must be replaced.

Consistency with the operating point: the improved calibration is accompanied by a rise in referable
Sens with no drop in Spec (`exp1_clinical_indomain.md`) — there is no shift of the threshold toward
hypersensitivity.
