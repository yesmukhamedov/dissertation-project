> Ported from the superseded appendices, re-lettered, with the provenance banner,
> section signs and internal codes removed and cross-references renumbered to the
> four-chapter body. Transcription content is unchanged. Provenance: `outline/REWRITE_MAP.md`.

# APPENDIX B – Supplementary results and confusion matrices

---

## PART 1: SECTION TEXT

This appendix records the decomposition behind the aggregate figures reported in chapter 3:
per-class performance, the full structure of the confusion matrices, calibration, convergence, and
interval estimates. Its purpose is auditability. A reader who wishes to check how an aggregate
figure arises, or where the residual error lies, should not have to take the summary on trust.

Two conditions govern the reading of everything below. First, the grade distribution of the training
corpus is severely imbalanced: of 35,126 images, 25,810 are grade DR0, 2,443 DR1, 5,292 DR2, 873 DR3
and 708 DR4. Every per-class figure must be read against its class size, and the two smallest
classes carry intervals that no table here reports. Second, per-class metrics are marked
supplementary in the metric table of section 2.6: they inform the reading of the primary metrics
and cannot independently establish or refute a hypothesis.

### B.1 Per-class performance on the training corpus

Per-class F1, precision and recall on the pooled validation folds, all four configurations.

**Table B.1 – Per-class F1, precision and recall on the training corpus (n = 35,126).**

| Arm | Measure | DR0 | DR1 | DR2 | DR3 | DR4 | macro-F1 |
|---|---|---:|---:|---:|---:|---:|---:|
| Baseline, residual | F1 | 0.8872 | 0.0999 | 0.5263 | 0.2193 | 0.4078 | 0.4281 |
| | precision | 0.9219 | 0.0750 | 0.5980 | 0.1728 | 0.4326 | |
| | recall | 0.8551 | 0.1498 | 0.4700 | 0.3001 | 0.3856 | |
| Integrated, residual | F1 | 0.9320 | 0.2141 | 0.6546 | 0.3180 | 0.5424 | 0.5322 |
| | precision | 0.9497 | 0.1774 | 0.7201 | 0.2529 | 0.5670 | |
| | recall | 0.9150 | 0.2702 | 0.6000 | 0.4284 | 0.5198 | |
| Baseline, efficient | F1 | 0.8889 | 0.0976 | 0.5316 | 0.2173 | 0.4147 | 0.4300 |
| | precision | 0.9222 | 0.0734 | 0.6038 | 0.1723 | 0.4430 | |
| | recall | 0.8580 | 0.1453 | 0.4749 | 0.2944 | 0.3898 | |
| Integrated, efficient | F1 | 0.9333 | 0.2188 | 0.6594 | 0.3179 | 0.5483 | 0.5355 |
| | precision | 0.9503 | 0.1818 | 0.7244 | 0.2539 | 0.5732 | |
| | recall | 0.9170 | 0.2747 | 0.6051 | 0.4250 | 0.5254 | |

The macro-average gain (+0.104 and +0.106) exceeds the weighted-average gain reported in section
3.2, which is the arithmetic expression of the observation made there: the advantage falls
disproportionately on the minority grades. DR1 remains the weakest class in every configuration, and
it is also the class on which the relative gain is largest.

### B.2 Confusion matrices on the training corpus

Rows are the reference grade, columns the predicted grade.

**Table B.2 – Confusion matrix, baseline residual.**

| true \ pred | DR0 | DR1 | DR2 | DR3 | DR4 |
|---|---:|---:|---:|---:|---:|
| DR0 | 22069 | 2973 | 615 | 127 | 26 |
| DR1 | 1257 | 366 | 656 | 136 | 28 |
| DR2 | 549 | 1384 | 2487 | 722 | 150 |
| DR3 | 46 | 117 | 294 | 262 | 154 |
| DR4 | 17 | 42 | 107 | 269 | 273 |

**Table B.3 – Confusion matrix, integrated residual.**

| true \ pred | DR0 | DR1 | DR2 | DR3 | DR4 |
|---|---:|---:|---:|---:|---:|
| DR0 | 23617 | 1906 | 250 | 33 | 4 |
| DR1 | 1019 | 660 | 666 | 87 | 11 |
| DR2 | 219 | 1091 | 3175 | 713 | 94 |
| DR3 | 11 | 53 | 263 | 374 | 172 |
| DR4 | 2 | 11 | 55 | 272 | 368 |

**Table B.4 – Confusion matrix, baseline efficient.**

| true \ pred | DR0 | DR1 | DR2 | DR3 | DR4 |
|---|---:|---:|---:|---:|---:|
| DR0 | 22145 | 2939 | 586 | 117 | 23 |
| DR1 | 1273 | 355 | 658 | 131 | 26 |
| DR2 | 535 | 1385 | 2513 | 716 | 143 |
| DR3 | 45 | 116 | 300 | 257 | 155 |
| DR4 | 16 | 40 | 105 | 271 | 276 |

**Table B.5 – Confusion matrix, integrated efficient.**

| true \ pred | DR0 | DR1 | DR2 | DR3 | DR4 |
|---|---:|---:|---:|---:|---:|
| DR0 | 23667 | 1872 | 237 | 30 | 4 |
| DR1 | 1016 | 671 | 661 | 84 | 11 |
| DR2 | 211 | 1085 | 3202 | 705 | 89 |
| DR3 | 10 | 52 | 267 | 371 | 173 |
| DR4 | 2 | 10 | 53 | 271 | 372 |

Two structural features of these matrices are visible directly and are what the κ figures in section
3.2 reflect. The diagonal grows at every grade under the integrated configuration. And the cells
distant from the diagonal empty. The DR0 to DR4 cell falls from 26 to 4 on the residual backbone and
from 23 to 4 on the compound-scaled one, while the mass of DR0 to DR1 confusions falls by roughly a
thousand instances. Because quadratic-weighted κ penalises misgrading in proportion to ordinal
distance, the emptying of the distant cells contributes to the κ gain out of proportion to the
number of images involved.

### B.3 Confusion matrices on the external public corpus

**Table B.6 – Confusion matrix, baseline efficient, external public corpus (n = 3,662).**

| true \ pred | DR0 | DR1 | DR2 | DR3 | DR4 |
|---|---:|---:|---:|---:|---:|
| DR0 | 1570 | 186 | 39 | 8 | 2 |
| DR1 | 184 | 63 | 98 | 21 | 4 |
| DR2 | 96 | 245 | 500 | 131 | 27 |
| DR3 | 10 | 24 | 62 | 64 | 33 |
| DR4 | 6 | 15 | 42 | 108 | 124 |

**Table B.7 – Confusion matrix, integrated efficient, external public corpus.**

| true \ pred | DR0 | DR1 | DR2 | DR3 | DR4 |
|---|---:|---:|---:|---:|---:|
| DR0 | 1678 | 111 | 14 | 2 | 0 |
| DR1 | 150 | 108 | 99 | 12 | 1 |
| DR2 | 33 | 192 | 630 | 129 | 15 |
| DR3 | 1 | 10 | 56 | 87 | 39 |
| DR4 | 0 | 3 | 20 | 112 | 160 |

**Table B.8 – Per-class F1 on the external public corpus.**

| Arm | DR0 | DR1 | DR2 | DR3 | DR4 | macro-F1 |
|---|---:|---:|---:|---:|---:|---:|
| Baseline, efficient | 0.8554 | 0.1395 | 0.5747 | 0.2438 | 0.5113 | 0.4649 |
| Integrated, efficient | 0.9152 | 0.2720 | 0.6931 | 0.3252 | 0.6275 | 0.5666 |

The pattern of section B.2 reproduces under transfer: the diagonal grows at every grade, the distant
cells empty, and the residual error concentrates on the DR3 ↔ DR4 boundary, which remains the
hardest distinction in both configurations.

### B.4 Calibration

**Table B.9 – Expected calibration error and Brier score on the training corpus.**

| Configuration | ECE | Brier |
|---|---:|---:|
| Baseline, residual | 0.0712 | 0.0724 |
| Integrated, residual | 0.0418 | 0.0611 |
| Baseline, efficient | 0.0691 | 0.0715 |
| Integrated, efficient | 0.0402 | 0.0598 |

Calibration is an empirical property of the predicted probabilities. It is not a warrant of clinical
decision-making reliability, and no such reading is offered here or elsewhere in this dissertation.

### B.5 Convergence and overfitting

Best epoch is the epoch of maximum validation weighted F1 within each fold; the losses are those at
the best epoch.

**Table B.10 – Per-fold convergence on the training corpus.**

| Configuration | Best epoch per fold | Train loss | Validation loss | Gap (val − train) |
|---|---|---:|---:|---:|
| Baseline, residual | 16, 14, 17, 15, 16 | 0.098 | 0.150 | 0.052 |
| Integrated, residual | 9, 8, 10, 9, 9 | 0.126 | 0.147 | 0.021 |
| Baseline, efficient | 15, 17, 14, 16, 15 | 0.102 | 0.156 | 0.054 |
| Integrated, efficient | 8, 9, 7, 9, 8 | 0.131 | 0.153 | 0.022 |

The joint signature discussed in section 3.2 is legible in this table: the integrated configurations
reach their best epoch six to eight epochs earlier, hold a loss gap roughly 2.5 times smaller, and
do so with a *higher* training loss at a comparable validation loss. The spread of best epochs
within a configuration is one to one-and-a-half epochs, so the convergence regime is a property of
the configuration rather than of a particular fold.

### B.6 Interval estimates

Two intervals are reported and they quantify different things. The cross-validation interval is
taken over the five folds and therefore includes the variability of refitting. The per-instance
bootstrap interval resamples the evaluation set under a fixed fitted model and therefore quantifies
evaluation-corpus sampling alone.

**Table B.11 – Between-fold cross-validation intervals (95 %, t, df = 4).**

| Configuration | Weighted F1 (mean ± sd) | wF1 95 % CI | ROC-AUC 95 % CI | κ 95 % CI | Accuracy 95 % CI |
|---|---|---|---|---|---|
| Baseline, residual | 0.7518 ± 0.0110 | [0.7381, 0.7655] | [0.8126, 0.8474] | [0.6976, 0.7845] | [0.7024, 0.7471] |
| Integrated, residual | 0.8172 ± 0.0090 | [0.8060, 0.8284] | [0.8483, 0.8757] | [0.8216, 0.8862] | [0.7841, 0.8213] |
| Baseline, efficient | 0.7538 ± 0.0120 | [0.7389, 0.7687] | [0.8024, 0.8396] | [0.7058, 0.7878] | [0.7037, 0.7509] |
| Integrated, efficient | 0.8193 ± 0.0100 | [0.8069, 0.8317] | [0.8421, 0.8719] | [0.8236, 0.8906] | [0.7853, 0.8251] |

**Table B.12 – Per-instance bootstrap intervals, weighted F1 (1,000 resamples).**

| Configuration | Mean | 95 % CI | sd |
|---|---:|---|---:|
| Baseline, residual | 0.7518 | [0.7467, 0.7557] | 0.0023 |
| Integrated, residual | 0.8172 | [0.8138, 0.8222] | 0.0021 |
| Baseline, efficient | 0.7538 | [0.7504, 0.7596] | 0.0023 |
| Integrated, efficient | 0.8193 | [0.8143, 0.8225] | 0.0021 |

The bootstrap and cross-validation means agree to the fourth decimal place. As section 3.8 notes,
the marginal separation of intervals is weaker evidence than the paired tests reported there, and it
is recorded here as description rather than as a test.

### B.7 Referable-DR screening metrics, in-domain

Referable DR is the grade ≥ 2 threshold.

**Table B.13 – In-domain referable-disease metrics (n = 35,126).**

| Configuration | Sensitivity | Specificity | PPV | NPV | Referable ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Baseline, residual | 0.6865 | 0.9438 | 0.7482 | 0.9252 | 0.8710 |
| Integrated, residual | 0.7982 | 0.9628 | 0.8392 | 0.9515 | 0.9120 |
| Baseline, efficient | 0.6891 | 0.9455 | 0.7545 | 0.9259 | 0.8680 |
| Integrated, efficient | 0.8007 | 0.9636 | 0.8427 | 0.9521 | 0.9100 |

Sensitivity and specificity rise together, which is the observation section 3.2 reports as a shift
of the discrimination curve rather than a movement along it.

### B.8 What this appendix does not contain

Three sets of material that an appendix of this kind would ordinarily carry are absent, and the
reason differs in each case.

**Per-epoch training and validation curves.** The per-epoch trajectories were not retained; only the best epoch and the losses at that epoch survive, and they are given in Table B.10. The convergence claim of section 3.2 rests on that table and on nothing finer, and the figure originally reserved for the full trajectories is accordingly not cited anywhere in the dissertation.

**Per-class ROC and precision–recall curves.** These require per-sample predicted probabilities. Per-sample prediction dumps were not saved, so the curves cannot be produced from the available record. The threshold-independent evidence in this dissertation is therefore confined to the aggregate and referable ROC-AUC figures reported above and in chapter 3.

**Per-camera-group confusion matrices.** These were not recorded; only per-class F1 by group is available, and it is given in Appendix E. The consequence is stated in section 3.5 and in section 3.9. The *composition* of errors across camera groupings could not be examined, and whether it differs between groups remains open.

None of these absences affects the direction or the interval of any difference reported in chapter
3. Each of them limits the resolution at which that difference can be inspected, and each is
recorded as an open item rather than a closed one.

---
