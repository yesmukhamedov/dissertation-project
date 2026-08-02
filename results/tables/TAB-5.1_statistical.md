# TAB-5.1 — exp1 statistical tests

Source: the **2026-08-02** run (`VALUES.md` §1.3–1.4). The B-vs-A and D-vs-C pairs are evaluated on
the same val split per fold (the splits are identical across configurations), so paired tests apply.

## Bootstrap 95% CI (weighted-F1, 1000 resamples)

| Config | wF1 mean | 95% CI | std |
|---|---|---|---|
| A | 0.7518 | [0.7473, 0.7563] | 0.0023 |
| B | 0.8172 | [0.8130, 0.8214] | 0.0021 |
| C | 0.7538 | [0.7492, 0.7584] | 0.0023 |
| D | 0.8193 | [0.8152, 0.8234] | 0.0021 |

The baseline and pipeline intervals do not overlap (a gap of ≈0.057 between A and B, ≈0.057 between C and D).

## Paired tests

| Test | B vs A | D vs C | α |
|------|--------|--------|---|
| DeLong ΔAUC (referable, grade ≥ 2) | +0.0410 | +0.0420 | — |
| DeLong z | 2.8704 | 2.9889 | — |
| **DeLong p** | **0.0041** | **0.0028** | 0.05 |
| McNemar b / c | 2190 / 2010 | 2265 / 2075 | — |
| McNemar χ² | 7.6288 | 8.2306 | — |
| **McNemar p** | **0.0057** | **0.0041** | 0.05 |
| **Holm-corrected p** (4 configurations) | **0.0082** | **0.0056** | 0.05 |
| Mixed-effects ANOVA — "arm × backbone" interaction | — | 0.31 | 0.05 |

## Interpretation

1. **The referable-AUC gain is significant on both backbones** (DeLong p = 0.0041 and 0.0028) and it
   **survives correction for multiplicity**: Holm over the 4 configurations gives p = 0.0082 and
   0.0056, both below α = 0.05. The significance is not an artifact of repeated testing.
2. **The gain in the fraction of correct predictions is also significant** (McNemar p = 0.0057 /
   0.0041). The imbalance of the discordant pairs is moderate (2190/2010 and 2265/2075) — that is,
   the pipeline does not merely "rearrange" errors but produces a clean positive balance.
3. **There is no "arm × backbone" interaction** (p = 0.31). The pipeline effect is statistically the
   same for ResNet-50 and EfficientNet-B3, consistent with the nearly identical ΔwF1 (+6.54 vs +6.55 pp).
   This matters for the wording of H-1 — "on both backbones" is supported not only directionally but
   also by a test of effect homogeneity.
4. **The differences in the primary metrics with 95% CIs** (`TAB-4.2_exp1_factorial.md`, §1.2) — all
   six intervals exclude zero.

> A caveat about the magnitude of z: DeLong z ≈ 2.87–2.99 corresponds to a moderate but stable
> effect. It should be phrased as "significant at the 0.05 level after the Holm correction", without
> intensifiers such as "p < 10⁻⁴".
