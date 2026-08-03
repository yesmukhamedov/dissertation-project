# TAB-4.10 — Experiment 7: Small-Data Training (IDRiD → Clinical)

Training on the small IDRiD set (n = 516, 5-fold CV), tested on the Kazakhstani clinical hold-out
(n = 60). EfficientNet-B3. Source: the **2026-08-03** run (`VALUES.md` §E-7).

## Clinical hold-out, n = 60 (§E7.1)

| Arm | Weighted F1 | Cohen κ | ROC-AUC | Accuracy |
|-----|------------:|--------:|--------:|---------:|
| C — baseline (3ch) | 0.5157 ± 0.0450 | 0.4848 ± 0.0440 | 0.7464 ± 0.0380 | 0.5264 ± 0.0410 |
| D — full pipeline (4ch) | **0.5951 ± 0.0400** | **0.6075 ± 0.0438** | **0.7962 ± 0.0320** | **0.5968 ± 0.0370** |

## Pairwise differences (§E7.3)

| Metric | Δ (D − C) | 95% CI (Δ) | CI excludes 0 |
|---------|----------:|------------|:--------------:|
| wF1 | +0.0794 | [+0.0471, +0.1227] | ✓ |
| κ | +0.1227 | [+0.0747, +0.1925] | ✓ |
| ROC-AUC | +0.0498 | [+0.0165, +0.0689] | ✓ |

## Bootstrap 95% CI by arm, 1000 resamples (§E7.2)

| Arm | wF1 mean | 95% CI |
|-----|---------:|--------|
| C | 0.5157 | [0.4601, 0.6097] |
| D | 0.5951 | [0.5433, 0.6837] |

> ⚠️ **The unpaired intervals overlap** (C up to 0.6097, D from 0.5433) — at n = 60 the per-instance
> bootstrap of each arm taken separately is wide. Significance comes precisely from the **paired**
> test of the difference (§E7.3), where both arms are evaluated on the same 60 images and the common
> sample variance cancels. Carry the paired CIs into the text; cite the unpaired ones only with this
> caveat.

## Internal cross-validation on IDRiD, n = 516, 5 folds (§E7.4)

| Arm | wF1 | fold 1 | fold 2 | fold 3 | fold 4 | fold 5 |
|-----|----:|-------:|-------:|-------:|-------:|-------:|
| C | 0.5850 ± 0.0380 | 0.5757 | 0.6466 | 0.5702 | 0.5883 | 0.5442 |
| D | **0.6520 ± 0.0310** | 0.6754 | 0.6352 | 0.6790 | 0.6059 | 0.6645 |

The pipeline is above baseline **in 4 of the 5 folds** (margins +0.0997, +0.1088, +0.0176, +0.1203);
on **fold 2** it is marginally lower (0.6352 against 0.6466, −0.0114). Fold 2 is baseline's strongest
fold — the inversion is a single-fold fluctuation of magnitude comparable to the between-fold std
(0.031–0.038), not a systematic exception. The mean advantage (+0.0670 across folds) nevertheless
holds, and the per-image paired test on the clinical hold-out (§E7.3) is the primary evidence.

## Status (§E7.5)

| Field | Value |
|------|----------|
| preregistered | **true** |

The experiment is preregistered — the criteria and metrics were fixed before the run, which removes
any question of post-hoc metric selection for this result.

## Verdict: a positive for the pipeline, significant

On small clinical data the pipeline delivers **+0.079 weighted-F1**, **+0.123 κ** and **+0.050 AUC**
with intervals excluding zero. The κ gain (+0.123) is over 1.5× the wF1 gain — the same picture as in
every other experiment: the pipeline primarily removes distant grading errors.

**Significance for the thesis.** This is the target operating scenario — training on a small clinical
sample and deployment in a different clinic. The result substantiates the main practical
contribution: **preprocessing acts as an effective prior in the data-scarce regime**. At the same
time, the gain here (+0.079) is comparable to the gain on full EyePACS (+0.0655, `TAB-4.2`), i.e. the
pipeline's advantage **does not vanish** when moving to large data and **is not** an artifact of the
small sample.

## Caveats

- The absolute level (wF1 ≈ 0.52–0.60) is noticeably below in-domain EyePACS — as expected for
  training on 516 images with testing in a different clinic; what is meaningful is the difference
  between arms, not the absolute value.
- The clinical hold-out is small (n = 60) — hence the wide unpaired bootstrap intervals (see above).
- The ± in §E7.1 is the spread across the 5 training folds, not per-instance uncertainty on the hold-out.
