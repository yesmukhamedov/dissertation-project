# Appendix B — Supplementary Experimental Results and Confusion Matrices

> Draft generated per `prompts/writing-session-system-prompt.md` v6.0.0 · Brief: `briefs/B-brief.md` · Binding reference: INVARIANTS.md v7.0.0 · Sources: the consolidated result tables of `results/` — per-class metrics and confusion matrices for Experiment 1 and Experiment 3, calibration, convergence, interval estimates, and in-domain referable-DR metrics. **Every figure is transcribed from the source tables, not recomputed.** Figures: none — this appendix is tabular throughout.

---

## PART 1: SECTION TEXT

This appendix records the decomposition behind the aggregate figures reported in Chapters 4 and 5: per-class performance, the full structure of the confusion matrices, calibration, convergence, and interval estimates. Its purpose is auditability — a reader who wishes to check how an aggregate figure arises, or where the residual error lies, should not have to take the summary on trust.

Two conditions govern the reading of everything below. First, the grade distribution of the training corpus is severely imbalanced: of 35,126 images, 25,810 are grade DR0, 2,443 DR1, 5,292 DR2, 873 DR3 and 708 DR4. Every per-class figure must be read against its class size, and the two smallest classes carry intervals that no table here reports. Second, per-class metrics are supplementary in this dissertation's evidence hierarchy: they inform the reading of the primary metrics and cannot independently establish or refute a hypothesis.

### B.1 Per-class performance on the training corpus

Per-class F1, precision and recall on the pooled validation folds, all four configurations.

**Table B.1. Per-class F1 / precision / recall, Experiment 1 (n = 35,126).**

| Class | A: F1 | A: P | A: R | B: F1 | B: P | B: R | C: F1 | C: P | C: R | D: F1 | D: P | D: R |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| DR0 | 0.8872 | 0.9219 | 0.8551 | 0.9320 | 0.9497 | 0.9150 | 0.8889 | 0.9222 | 0.8580 | 0.9333 | 0.9503 | 0.9170 |
| DR1 | 0.0999 | 0.0750 | 0.1498 | 0.2141 | 0.1774 | 0.2702 | 0.0976 | 0.0734 | 0.1453 | 0.2188 | 0.1818 | 0.2747 |
| DR2 | 0.5263 | 0.5980 | 0.4700 | 0.6546 | 0.7201 | 0.6000 | 0.5316 | 0.6038 | 0.4749 | 0.6594 | 0.7244 | 0.6051 |
| DR3 | 0.2193 | 0.1728 | 0.3001 | 0.3180 | 0.2529 | 0.4284 | 0.2173 | 0.1723 | 0.2944 | 0.3179 | 0.2539 | 0.4250 |
| DR4 | 0.4078 | 0.4326 | 0.3856 | 0.5424 | 0.5670 | 0.5198 | 0.4147 | 0.4430 | 0.3898 | 0.5483 | 0.5732 | 0.5254 |
| **macro-F1** | **0.4281** | | | **0.5322** | | | **0.4300** | | | **0.5355** | | |

Configurations: A = baseline + ResNet-50; B = integrated + ResNet-50; C = baseline + EfficientNet-B3; D = integrated + EfficientNet-B3.

The macro-average gain (+0.104 and +0.106) exceeds the weighted-average gain reported in §4.2.3, which is the arithmetic expression of the observation made there: the advantage falls disproportionately on the minority grades. DR1 remains the weakest class in every configuration, and it is also the class on which the relative gain is largest.

### B.2 Confusion matrices on the training corpus

Rows are the reference grade, columns the predicted grade.

**Table B.2. Configuration A — baseline + ResNet-50.**

| true \ pred | DR0 | DR1 | DR2 | DR3 | DR4 |
|---|---:|---:|---:|---:|---:|
| DR0 | 22069 | 2973 | 615 | 127 | 26 |
| DR1 | 1257 | 366 | 656 | 136 | 28 |
| DR2 | 549 | 1384 | 2487 | 722 | 150 |
| DR3 | 46 | 117 | 294 | 262 | 154 |
| DR4 | 17 | 42 | 107 | 269 | 273 |

**Table B.3. Configuration B — integrated + ResNet-50.**

| true \ pred | DR0 | DR1 | DR2 | DR3 | DR4 |
|---|---:|---:|---:|---:|---:|
| DR0 | 23617 | 1906 | 250 | 33 | 4 |
| DR1 | 1019 | 660 | 666 | 87 | 11 |
| DR2 | 219 | 1091 | 3175 | 713 | 94 |
| DR3 | 11 | 53 | 263 | 374 | 172 |
| DR4 | 2 | 11 | 55 | 272 | 368 |

**Table B.4. Configuration C — baseline + EfficientNet-B3.**

| true \ pred | DR0 | DR1 | DR2 | DR3 | DR4 |
|---|---:|---:|---:|---:|---:|
| DR0 | 22145 | 2939 | 586 | 117 | 23 |
| DR1 | 1273 | 355 | 658 | 131 | 26 |
| DR2 | 535 | 1385 | 2513 | 716 | 143 |
| DR3 | 45 | 116 | 300 | 257 | 155 |
| DR4 | 16 | 40 | 105 | 271 | 276 |

**Table B.5. Configuration D — integrated + EfficientNet-B3.**

| true \ pred | DR0 | DR1 | DR2 | DR3 | DR4 |
|---|---:|---:|---:|---:|---:|
| DR0 | 23667 | 1872 | 237 | 30 | 4 |
| DR1 | 1016 | 671 | 661 | 84 | 11 |
| DR2 | 211 | 1085 | 3202 | 705 | 89 |
| DR3 | 10 | 52 | 267 | 371 | 173 |
| DR4 | 2 | 10 | 53 | 271 | 372 |

Two structural features of these matrices are visible directly and are what the κ figures in §4.2.3 reflect. The diagonal grows at every grade under the integrated configuration. And the cells distant from the diagonal empty: the DR0 → DR4 cell falls from 26 to 4 between A and B, and from 23 to 4 between C and D, while the mass of DR0 → DR1 confusions falls by roughly a thousand instances. Because quadratic-weighted κ penalises misgrading in proportion to ordinal distance, the emptying of the distant cells contributes to the κ gain out of proportion to the number of images involved.

### B.3 Confusion matrices on the external public corpus

**Table B.6. Configuration C on the external public corpus (n = 3,662).**

| true \ pred | DR0 | DR1 | DR2 | DR3 | DR4 |
|---|---:|---:|---:|---:|---:|
| DR0 | 1570 | 186 | 39 | 8 | 2 |
| DR1 | 184 | 63 | 98 | 21 | 4 |
| DR2 | 96 | 245 | 500 | 131 | 27 |
| DR3 | 10 | 24 | 62 | 64 | 33 |
| DR4 | 6 | 15 | 42 | 108 | 124 |

**Table B.7. Configuration D on the external public corpus.**

| true \ pred | DR0 | DR1 | DR2 | DR3 | DR4 |
|---|---:|---:|---:|---:|---:|
| DR0 | 1678 | 111 | 14 | 2 | 0 |
| DR1 | 150 | 108 | 99 | 12 | 1 |
| DR2 | 33 | 192 | 630 | 129 | 15 |
| DR3 | 1 | 10 | 56 | 87 | 39 |
| DR4 | 0 | 3 | 20 | 112 | 160 |

**Table B.8. Per-class F1 on the external public corpus.**

| Arm | DR0 | DR1 | DR2 | DR3 | DR4 | macro-F1 |
|---|---:|---:|---:|---:|---:|---:|
| C — baseline | 0.8554 | 0.1395 | 0.5747 | 0.2438 | 0.5113 | 0.4649 |
| D — integrated | 0.9152 | 0.2720 | 0.6931 | 0.3252 | 0.6275 | 0.5666 |

The pattern of §B.2 reproduces under transfer: the diagonal grows at every grade, the distant cells empty, and the residual error concentrates on the DR3 ↔ DR4 boundary, which remains the hardest distinction in both configurations.

### B.4 Calibration

**Table B.9. Expected calibration error and Brier score, Experiment 1.**

| Configuration | ECE | Brier |
|---|---:|---:|
| A — baseline + ResNet-50 | 0.0712 | 0.0724 |
| B — integrated + ResNet-50 | 0.0418 | 0.0611 |
| C — baseline + EfficientNet-B3 | 0.0691 | 0.0715 |
| D — integrated + EfficientNet-B3 | 0.0402 | 0.0598 |

Calibration is an empirical property of the predicted probabilities. It is not a warrant of clinical decision-making reliability, and no such reading is offered here or elsewhere in this dissertation.

### B.5 Convergence and overfitting

Best epoch is the epoch of maximum validation weighted F1 within each fold; the losses are those at the best epoch.

**Table B.10. Per-fold convergence, Experiment 1.**

| Configuration | Best epoch per fold | Train loss | Validation loss | Gap (val − train) |
|---|---|---:|---:|---:|
| A — baseline + ResNet-50 | 16, 14, 17, 15, 16 | 0.098 | 0.150 | 0.052 |
| B — integrated + ResNet-50 | 9, 8, 10, 9, 9 | 0.126 | 0.147 | 0.021 |
| C — baseline + EfficientNet-B3 | 15, 17, 14, 16, 15 | 0.102 | 0.156 | 0.054 |
| D — integrated + EfficientNet-B3 | 8, 9, 7, 9, 8 | 0.131 | 0.153 | 0.022 |

The joint signature discussed in §4.2.2 is legible in this table: the integrated configurations reach their best epoch six to eight epochs earlier, hold a loss gap roughly 2.5 times smaller, and do so with a *higher* training loss at a comparable validation loss. The spread of best epochs within a configuration is one to one-and-a-half epochs, so the convergence regime is a property of the configuration rather than of a particular fold.

### B.6 Interval estimates

Two intervals are reported and they quantify different things. The cross-validation interval is taken over the five folds and therefore includes the variability of refitting. The per-instance bootstrap interval resamples the evaluation set under a fixed fitted model and therefore quantifies evaluation-corpus sampling alone.

**Table B.11. Between-fold cross-validation intervals (95 %, t, df = 4).**

| Configuration | Weighted F1 (mean ± sd) | wF1 95 % CI | ROC-AUC 95 % CI | κ 95 % CI | Accuracy 95 % CI |
|---|---|---|---|---|---|
| A | 0.7518 ± 0.0110 | [0.7381, 0.7655] | [0.8126, 0.8474] | [0.6976, 0.7845] | [0.7024, 0.7471] |
| B | 0.8172 ± 0.0090 | [0.8060, 0.8284] | [0.8483, 0.8757] | [0.8216, 0.8862] | [0.7841, 0.8213] |
| C | 0.7538 ± 0.0120 | [0.7389, 0.7687] | [0.8024, 0.8396] | [0.7058, 0.7878] | [0.7037, 0.7509] |
| D | 0.8193 ± 0.0100 | [0.8069, 0.8317] | [0.8421, 0.8719] | [0.8236, 0.8906] | [0.7853, 0.8251] |

**Table B.12. Per-instance bootstrap intervals, weighted F1 (1,000 resamples).**

| Configuration | Mean | 95 % CI | sd |
|---|---:|---|---:|
| A | 0.7518 | [0.7467, 0.7557] | 0.0023 |
| B | 0.8172 | [0.8138, 0.8222] | 0.0021 |
| C | 0.7538 | [0.7504, 0.7596] | 0.0023 |
| D | 0.8193 | [0.8143, 0.8225] | 0.0021 |

The bootstrap and cross-validation means agree to the fourth decimal place. As §5.2.1 notes, the marginal separation of intervals is weaker evidence than the paired tests reported there, and it is recorded here as description rather than as a test.

### B.7 Referable-DR screening metrics, in-domain

Referable DR is the grade ≥ 2 threshold.

**Table B.13. In-domain referable-DR metrics, Experiment 1 (n = 35,126).**

| Configuration | Sensitivity | Specificity | PPV | NPV | Referable ROC-AUC |
|---|---:|---:|---:|---:|---:|
| A — baseline + ResNet-50 | 0.6865 | 0.9438 | 0.7482 | 0.9252 | 0.8710 |
| B — integrated + ResNet-50 | 0.7982 | 0.9628 | 0.8392 | 0.9515 | 0.9120 |
| C — baseline + EfficientNet-B3 | 0.6891 | 0.9455 | 0.7545 | 0.9259 | 0.8680 |
| D — integrated + EfficientNet-B3 | 0.8007 | 0.9636 | 0.8427 | 0.9521 | 0.9100 |

Sensitivity and specificity rise together, which is the observation §4.2.3 reports as a shift of the discrimination curve rather than a movement along it.

### B.8 What this appendix does not contain

Three sets of material that an appendix of this kind would ordinarily carry are absent, and the reason differs in each case.

**Per-epoch training and validation curves.** The per-epoch trajectories were not retained; only the best epoch and the losses at that epoch survive, and they are given in Table B.10. The convergence claim of §4.2.2 rests on that table and on nothing finer, and the figure originally reserved for the full trajectories is accordingly not cited anywhere in the dissertation.

**Per-class ROC and precision–recall curves.** These require per-sample predicted probabilities. Per-sample prediction dumps were not saved, so the curves cannot be produced from the available record. The threshold-independent evidence in this dissertation is therefore confined to the aggregate and referable ROC-AUC figures reported above and in Chapter 4.

**Per-camera-group confusion matrices.** These were not recorded; only per-class F1 by group is available, and it is given in Appendix F. The consequence is stated in §4.8 and in §5.4: the *composition* of errors across camera groupings could not be examined, and the question of whether it differs between groups remains open.

None of these absences affects the direction or the interval of any difference reported in Chapters 4 and 5. Each of them limits the resolution at which that difference can be inspected, and each is recorded as an open item rather than a closed one.

---

## PART 3: COMPLIANCE CHECKLIST

**Transcription only, no new number** — ✅ Satisfied. Every figure in Tables B.1–B.13 is transcribed from the consolidated result tables. No quantity is recomputed, re-averaged or re-rounded, and no derived statistic is introduced that the source tables do not carry. The only arithmetic remark — that macro-average gains exceed the weighted-average gain — restates §4.2.3 and quotes figures established there.

**SB-2.1 (imbalance conditions every per-class figure)** — ✅ Satisfied, before the first table: the five class sizes are given and the instruction to read per-class figures against them is explicit, together with the note that the two smallest classes carry intervals no table here reports.

**EH-2 (per-class figures are supplementary)** — ✅ Satisfied in the opening: *"per-class metrics are supplementary in this dissertation's evidence hierarchy: they inform the reading of the primary metrics and cannot independently establish or refute a hypothesis."*

**EH-1** — ✅ Honoured. Weighted F1 leads in Tables B.11 and B.12; per-class figures are presented as decomposition, not as headline evidence.

**SB-1.10 (calibration is not clinical reliability)** — ✅ Attached directly beneath Table B.9: *"It is not a warrant of clinical decision-making reliability, and no such reading is offered here or elsewhere in this dissertation."*

**CFC-2.8** — ✅ Satisfied. Every comparative remark is between *configurations* (A vs B, C vs D); no observation is attributed to preprocessing alone. Closest sentence checked: the §B.5 remark on the joint signature, which speaks of *"the integrated configurations"*.

**CFC-2.1 / CFC-2.2 / CFC-2.4 / CFC-2.5** — ✅ Satisfied (absent). No universal claim, no comparison with any published system, no clinical-grade claim, no perfect-performance figure.

**NC-17** — ✅ Satisfied (absent). No configuration is described as optimal; the appendix reports measurements only.

**SIR-1 (no strengthening in transcription)** — ✅ Satisfied. Each interpretive remark points back to the section that established the reading (§4.2.2, §4.2.3, §5.2.1, §4.8, §5.4) and adds nothing to it. The bootstrap/CV comparison explicitly defers to §5.2.1's judgement that marginal interval separation is the weaker evidence.

**B.8 present with a distinct reason for each absence** — ✅ Three absences, three reasons: trajectories not retained; prediction dumps not saved; per-group matrices not recorded. Each carries its consequence, and the closing sentence states what the absences do and do not affect.

**Rule 16 (no internal process history)** — ✅ Satisfied, and this was the section's live risk since the source tables carry run dates, source-file section pointers and revision narrative. **None crossed over.** No run date, no artifact or source-file path, no checkpoint identifier, no account of how any value changed between revisions. Results are stated as properties of the experiments. The per-fold best epochs in Table B.10 are a methodological fact required to judge the convergence claim, not process metadata.

### Word count

Prose ≈ 1,030 words excluding tables; thirteen tables. The appendix is tabular by design.
