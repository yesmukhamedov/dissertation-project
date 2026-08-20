> Ported from the superseded appendices, re-lettered, with the provenance banner,
> section signs and internal codes removed and cross-references renumbered to the
> four-chapter body. Transcription content is unchanged. Provenance: `outline/REWRITE_MAP.md`.

# Appendix E — Device domain-shift supplementary tables

---

## PART 1: SECTION TEXT

This appendix records the per-group evidence behind the camera-grouping evaluation at the resolution the run's data support, including the per-class decomposition that section 3.5 summarises but does not display.

Three conditions govern every table below and are stated before the first of them, because without them five rows read as five independent observations and they are not.

**Two of the five groupings are the external clinical corpora.** The Kowa grouping is the first of those corpora and the Topcon grouping the second. Their values, differences and intervals coincide with the external clinical evaluation character for character, by construction rather than by replication. They are not independent evidence, and any count of "five groupings" should be read with that in mind.

**Three of the groupings aggregate more than one camera model.** They identify a device family and an acquisition context rather than a single instrument, so a per-group figure is not a per-device figure.

**The evaluation uses the models of a single cross-validation fold.** The dispersion reported in section E.7 is therefore *between groups*, not between folds, and no between-fold variance is available for any figure in this appendix.

A fourth condition applies to the whole: none of what follows constitutes device certification, regulatory compliance, or a claim of device-agnostic deployment readiness. These are empirical observations of cross-device performance variability and nothing more.

### F.1 Group composition

**Table E.1. Group sizes and per-group class sizes.**

| Camera group | n | DR0 | DR1 | DR2 | DR3 | DR4 |
|---|---:|---:|---:|---:|---:|---:|
| kowa_idrid | 413 | 168 | 54 | 131 | 34 | 26 |
| mixed_ddr | 1,200 | 496 | 142 | 378 | 104 | 80 |
| mixed_odir5k | 950 | 402 | 108 | 290 | 88 | 62 |
| topcon_messidor2 | 1,744 | 723 | 201 | 548 | 152 | 120 |
| mixed_rfmid | 640 | 268 | 71 | 197 | 60 | 44 |

The imbalance of the training corpus reproduces within every group: DR0 is the largest class everywhere and DR4 the smallest, so per-class figures in section E.5 must be read against these counts, and the DR3 and DR4 columns in particular rest on tens rather than hundreds of images.

### F.2 Weighted F1 and retention ratio by group

The retention ratio is the group's weighted F1 divided by the same arm's in-domain weighted F1; the floor against which it was assessed is 0.7.

**Table E.2. Weighted F1 by camera group, both configurations.**

| Camera group | wF1 (C) | wF1 (D) | Δ | 95 % CI (Δ) | ratio (C) | ratio (D) | ≥ 0.7 (C / D) |
|---|---:|---:|---:|---|---:|---:|:--:|
| kowa_idrid | 0.5938 | 0.6627 | +0.0689 | [+0.0494, +0.0968] | 0.7877 | 0.8089 | ✓ / ✓ |
| mixed_ddr | 0.6154 | 0.6671 | +0.0517 | [+0.0226, +0.0690] | 0.8164 | 0.8142 | ✓ / ✓ |
| mixed_odir5k | 0.5700 | 0.6581 | +0.0881 | [+0.0570, +0.1088] | 0.7562 | 0.8032 | ✓ / ✓ |
| topcon_messidor2 | 0.6282 | 0.6823 | +0.0541 | [+0.0362, +0.0814] | 0.8334 | 0.8328 | ✓ / ✓ |
| mixed_rfmid | 0.5434 | 0.6421 | +0.0987 | [+0.0680, +0.1224] | 0.7209 | 0.7837 | ✓ / ✓ |

Configurations: C = baseline + EfficientNet-B3; D = integrated + EfficientNet-B3.

Absolute weighted F1 is higher under the integrated configuration on every group, with every interval excluding zero. The floor is cleared by both configurations on all five groups, so — as section 3.5 states — the floor does not discriminate between them.

### F.3 ROC-AUC and Cohen's κ by group

**Table E.3. Threshold-independent performance and ordinal agreement by group.**

| Camera group | AUC (C) | AUC (D) | Δ AUC | 95 % CI (Δ) | κ (C) | κ (D) |
|---|---:|---:|---:|---|---:|---:|
| kowa_idrid | 0.8195 | 0.8627 | +0.0432 | [+0.0323, +0.0619] | 0.6841 | 0.7719 |
| mixed_ddr | 0.8392 | 0.8653 | +0.0261 | [+0.0159, +0.0423] | 0.7017 | 0.7863 |
| mixed_odir5k | 0.7965 | 0.8598 | +0.0633 | [+0.0462, +0.0840] | 0.6373 | 0.7547 |
| topcon_messidor2 | 0.8407 | 0.8729 | +0.0322 | [+0.0183, +0.0421] | 0.7152 | 0.7886 |
| mixed_rfmid | 0.7884 | 0.8516 | +0.0632 | [+0.0478, +0.0882] | 0.6254 | 0.7408 |

### F.4 Referable-DR AUC by group

**Table E.4. Binary referable-DR ROC-AUC (grade ≥ 2) by group.**

| Camera group | Referable AUC (C) | Referable AUC (D) |
|---|---:|---:|
| kowa_idrid | 0.8960 | 0.9302 |
| mixed_ddr | 0.9025 | 0.9368 |
| mixed_odir5k | 0.8655 | 0.9211 |
| topcon_messidor2 | 0.9064 | 0.9459 |
| mixed_rfmid | 0.8553 | 0.9114 |

### F.5 Per-class F1 by group

**Table E.5. Per-class F1 by group — configuration C (baseline).**

| Camera group | DR0 | DR1 | DR2 | DR3 | DR4 | macro-F1 |
|---|---:|---:|---:|---:|---:|---:|
| kowa_idrid | 0.8294 | 0.2237 | 0.5348 | 0.3368 | 0.5031 | 0.4856 |
| mixed_ddr | 0.8502 | 0.2235 | 0.5598 | 0.3149 | 0.5083 | 0.4913 |
| mixed_odir5k | 0.7842 | 0.1940 | 0.5172 | 0.3206 | 0.4366 | 0.4505 |
| topcon_messidor2 | 0.8652 | 0.2309 | 0.5628 | 0.3266 | 0.5475 | 0.5066 |
| mixed_rfmid | 0.7356 | 0.2001 | 0.5035 | 0.2705 | 0.4771 | 0.4374 |

**Table E.6. Per-class F1 by group — configuration D (integrated).**

| Camera group | DR0 | DR1 | DR2 | DR3 | DR4 | macro-F1 |
|---|---:|---:|---:|---:|---:|---:|
| kowa_idrid | 0.8617 | 0.2894 | 0.6259 | 0.4314 | 0.5841 | 0.5585 |
| mixed_ddr | 0.8605 | 0.2912 | 0.6393 | 0.4062 | 0.6051 | 0.5605 |
| mixed_odir5k | 0.8570 | 0.2845 | 0.6119 | 0.4470 | 0.5348 | 0.5470 |
| topcon_messidor2 | 0.8927 | 0.3037 | 0.6277 | 0.4163 | 0.6142 | 0.5709 |
| mixed_rfmid | 0.8193 | 0.2726 | 0.6245 | 0.4042 | 0.5619 | 0.5365 |

Two observations are legible from the pair of tables and neither goes beyond what section 3.5 established. The integrated configuration is higher in every one of the twenty-five cells, without exception. And the difficulty ordering of the classes is identical in both configurations and in every group — DR0 easiest, then DR2, DR4, DR3, with DR1 hardest everywhere. Mild non-proliferative disease remains the weakest class under every camera grouping and in both arms; the integrated configuration mitigates that weakness without removing it.

### F.6 Between-class dispersion

**Table E.7. Span of per-class F1 across the five groups (maximum − minimum), by class.**

| Class | Span (C) | Span (D) |
|---|---:|---:|
| DR0 | 0.1296 | 0.0734 |
| DR1 | 0.0369 | 0.0311 |
| DR2 | 0.0593 | 0.0274 |
| DR3 | 0.0663 | 0.0428 |
| DR4 | 0.1109 | 0.0794 |

The contraction of the between-group span holds on every one of the five grades, not only on the pathological ones — the same levelling visible in the aggregate figures of section E.7, resolved by class.

### F.7 Between-group dispersion

**Table E.8. Dispersion of performance across the five camera groups.**

| Quantity | C | D | Δ (D − C) | 95 % CI (Δ) | CI excludes zero |
|---|---:|---:|---:|---|:--:|
| Standard deviation of weighted F1 | 0.0306 | 0.0130 | −0.0176 | [−0.0253, −0.0062] | ✓ |
| Standard deviation of ROC-AUC | 0.0214 | 0.0070 | −0.0144 | [−0.0233, −0.0072] | ✓ |

This is the substantive result of the camera-grouping evaluation, and section 3.5 reports it as such: the dispersion of performance across camera groupings falls by roughly a factor of 2.4 on weighted F1 and 3.1 on ROC-AUC, with both intervals excluding zero. The range contracts rather than shifting — the largest gain falls on the grouping where the baseline was weakest.

### F.8 The retention ratio and why it moves against the absolute figures

Table E.2 contains an apparent inconsistency that is worth stating plainly rather than leaving to be noticed. On two groupings — `mixed_ddr` and `topcon_messidor2` — the retention ratio is marginally *lower* for the integrated configuration than for the baseline, while its absolute weighted F1 is higher on both.

The explanation is arithmetic, not empirical. The ratio divides a group's performance by the *same arm's* in-domain performance, and the integrated arm's in-domain figure is the higher of the two. Its denominator is therefore larger, and a group must gain proportionally more merely to hold its ratio constant. The two groupings where the ratio dips are precisely those where the baseline was already strongest and the absolute gain smallest.

This is one instance of a defect that recurs across three measures in this dissertation and is set out in section 3.9: the retention ratio here, the generalisation ratio of section 3.5, and the degradation form in which the external clinical hypothesis was originally expressed. Each normalises or differences an arm's external performance against that same arm's in-domain performance, and each therefore penalises a configuration for its in-domain strength. The observation is **descriptive**. It explains the shape of a column in Table E.2; it does not rehabilitate any result, and no claim in this dissertation is strengthened by it.

### F.9 What this appendix does not contain

**Per-group confusion matrices were not recorded.** The run's data carry per-class F1 by group, which section E.5 reproduces, but not the full confusion structure within each group. The consequence is the one stated in section 3.5 and again in section 3.9: it is not possible to say whether the *composition* of errors differs between camera groupings — whether, for instance, a grouping's weakness on a given grade arises from confusion with the adjacent grade or with a distant one. That the aggregate performance levels across groupings is established; that the error structure levels with it is not, and remains an open question that closing would require only an additional export rather than any new training.

None of what this appendix contains supports a claim of device compatibility, device certification or regulatory compliance, and none of it extends to camera models not represented in the corpora above.

---
