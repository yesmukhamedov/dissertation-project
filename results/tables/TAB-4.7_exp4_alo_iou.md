# TAB-4.7 — Experiment 4: Attention–Lesion Overlap (ALO, primary) + IoU (secondary) (H-5)

Grad-CAM against the IDRiD pixel-level lesion masks. Backbone EfficientNet-B3, baseline (Config C, 3ch)
against full pipeline (Config D, 4ch). **ALO = area(GradCAM ∩ lesion)/area(lesion)** is the primary
metric; **IoU** is secondary. The heatmap is binarized at the threshold τ = 0.5 (the canonical one).
The analysis covers **all 54** IDRiD images that have lesion masks.
Source: the **2026-08-03** run (`VALUES.md` §5).

## ALO (primary) — paired comparison, τ = 0.5

| Lesion type | n | ALO (C) | ALO (D) | Δ | 95% CI (Δ) | p (Wilcoxon, 1-sided) |
|---|--:|---:|---:|---:|---|---:|
| Microaneurysms (MA) | 54 | 0.2126 | **0.3160** | +0.1034 | [+0.0331, +0.1587] | **0.0033** |
| Haemorrhages (HE) | 53 | 0.2794 | **0.4011** | +0.1217 | [+0.0485, +0.1739] | **0.0016** |
| Hard exudates (EX) | 54 | 0.3502 | **0.4790** | +0.1288 | [+0.0735, +0.2007] | **0.0007** |
| Soft exudates (SE) | 26 | 0.2318 | **0.3310** | +0.0992 | [+0.0401, +0.1969] | **0.0148** |

## IoU (secondary)

| Lesion type | n | IoU (C) | IoU (D) | Δ | 95% CI (Δ) | p (Wilcoxon, 1-sided) |
|---|--:|---:|---:|---:|---|---:|
| Microaneurysms | 54 | 0.1065 | **0.1694** | +0.0629 | [+0.0304, +0.1042] | **0.0053** |
| Haemorrhages | 53 | 0.1516 | **0.2229** | +0.0713 | [+0.0166, +0.1050] | **0.0029** |
| Hard exudates | 54 | 0.1944 | **0.2830** | +0.0886 | [+0.0318, +0.1256] | **0.0011** |
| Soft exudates | 26 | 0.1183 | **0.1775** | +0.0592 | [+0.0223, +0.1155] | **0.0189** |

## Direction of the effect on individual images (§5.3)

| Type | n | ↑ (better with the pipeline) | ↓ (worse) | = (unchanged) | share ↑ |
|---|--:|--:|--:|--:|---:|
| MA | 54 | 38 | 7 | 9 | 70% |
| HE | 53 | 36 | 8 | 9 | 68% |
| EX | 54 | 41 | 5 | 8 | 76% |
| SE | 26 | 17 | 4 | 5 | 65% |

The effect does not rest on individual observations: improvement is seen on 65–76% of images against
9–15% of deteriorations. The mean shifts are the result of a coherent movement of the majority, not
of outliers.

## Floor effect (§5.4)

| Quantity | Value |
|----------|---------:|
| f₀ — share of images with ALO = 0 in **both** arms (τ = 0.5) | 6 / 54 = **0.1111** |

Only 11% of images sit at the floor of the metric. Measurement takes place in the working range of
ALO/IoU, not at the edge of sensitivity.

## Robustness to the binarization threshold (§5.5)

| τ | Types with Δ > 0 | Significant (p < 0.05) |
|---|--------------:|-------------------:|
| 0.2 | 4 / 4 | 4 / 4 |
| 0.3 | 4 / 4 | 4 / 4 |
| **0.5** (canonical) | **4 / 4** | **4 / 4** |
| 0.7 | 4 / 4 | 3 / 4 |

The direction holds at all four thresholds; significance is lost for only one type at the strictest
τ = 0.7 (the smallest activation area). The result is not explained by the threshold.

## Verdict: `h5_alo_supported = true`

The wording of H-5 requires ALO for the preprocessed model to be **significantly** higher. This is met:

- the directional criterion — **4/4** lesion types (≥3/4 required);
- the statistical one — **4/4** types significant (p from 0.0007 to 0.0148), all 95% CIs excluding zero;
- the secondary metric IoU gives the same result on all four types (p 0.0011–0.0189);
- the result is robust to the binarization threshold (4/4 directionally at τ = 0.2…0.7).

Relative effect size: ALO rises by 37–49% (e.g. EX 0.3502 → 0.4790) and IoU by 46–59%. The largest
absolute gain is for hard exudates (+0.1288); the weakest significance is for soft exudates
(p = 0.0148), where the sample is three times smaller (n = 26).

## Mandatory caveats

1. **INVARIANTS NC-14 remains in force:** Grad-CAM activation **is not** clinical localization of
   pathology. The correct formulation is "the model's attention is better aligned with the annotated
   lesions", not "the model finds the lesions".
2. One model per arm (**fold 0**); there is no cross-validation for this analysis.
3. Masks are available only for the IDRiD segmentation subset (54 images); SE is annotated on only 26
   of them.
4. Classification of the same arms — `exp4_classification.md`.
5. **The clinical (KZ) qualitative overlays are still not produced** — the wording of H-5 requires
   them; see gap G-3 in `HYPOTHESIS_COVERAGE.md`.

Hypothesis card — `hypotheses/H-5.md`. Conclusions — `findings/exp4.md`.
