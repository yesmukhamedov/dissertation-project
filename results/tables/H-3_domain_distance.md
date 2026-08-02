# H-3 — Domain Distance: MMD and KL between the source and target domains

A test that preprocessing **brings the domain distributions closer together**. Two independent
measures: MMD over penultimate-layer features (representational level) and KL over per-channel
histograms (pixel level). BASE = the baseline arm (3ch), INT = the integrated arm (4ch, full pipeline).
Source: the **2026-08-02** run (`VALUES.md` §3).

> A new block relative to the previous version of `results/` — before 2026-08-02 domain distances
> were not measured.

## MMD over penultimate-layer features (§3.1)

Smaller = closer to the source domain (EyePACS). Δd = d_BASE − d_INT; Δd > 0 means the pipeline
reduces the distance.

| Target domain X | d(BASE, X) | d(INT, X) | Δd | 95% CI (Δd) | CI excludes 0 |
|---|---:|---:|---:|---|:---:|
| APTOS | 0.1840 | 0.1120 | +0.0720 | [+0.0412, +0.1028] | ✓ |
| IDRiD | 0.2260 | 0.1430 | +0.0830 | [+0.0481, +0.1179] | ✓ |
| Messidor-2 | 0.1710 | 0.1080 | +0.0630 | [+0.0352, +0.0908] | ✓ |
| DDR | 0.2090 | 0.1310 | +0.0780 | [+0.0443, +0.1117] | ✓ |
| ODIR-5K | 0.2430 | 0.1580 | +0.0850 | [+0.0491, +0.1209] | ✓ |
| RFMiD | 0.2570 | 0.1690 | +0.0880 | [+0.0502, +0.1258] | ✓ |

## KL over per-channel histograms (§3.2)

| Target domain X | d_KL(BASE, X) | d_KL(INT, X) | Reduction |
|---|---:|---:|---:|
| APTOS | 0.0940 | 0.0610 | −35% |
| IDRiD | 0.1180 | 0.0740 | −37% |
| Messidor-2 | 0.0870 | 0.0560 | −36% |
| DDR | 0.1060 | 0.0680 | −36% |
| ODIR-5K | 0.1290 | 0.0820 | −36% |
| RFMiD | 0.1370 | 0.0890 | −35% |

The Stage 7 normalization uses source-domain statistics (the target domains do not recompute their
own statistics), so the reduction in distance is achieved by stages 0–6 rather than by fitting the
normalization to the target set.

## Verdict: `h3_supported = true`

1. **The direction is the same for all six target domains** on both measures, with no exceptions.
2. **All six 95% CIs on Δd exclude zero** — the effect is statistically stable at the
   representational level.
3. **The KL reduction is almost constant (−35…−37%)** regardless of how far the domain was to begin
   with. This points to a multiplicative character of the normalization: the pipeline compresses the
   photometric spread by a fixed proportion rather than "pulling" distant domains up to nearby ones.
4. **The ranking of the domains is preserved** after preprocessing: RFMiD remains the most distant
   (0.2570 → 0.1690) and Messidor-2 the closest (0.1710 → 0.1080). That is, the residual difference
   between the sets is substantive in nature (population composition, imaging protocol) and does not
   reduce to illumination and contrast.

## Relation to the transfer results

The size of the MMD reduction agrees with the size of the transfer gain:

| Domain | Δd (MMD) | Δ wF1 (D − C) on transfer | Source |
|---|---:|---:|---|
| ODIR-5K | +0.0850 | +0.0880 | `TAB-4.9_exp6_device.md` |
| RFMiD | +0.0880 | +0.0970 | `TAB-4.9_exp6_device.md` |
| IDRiD | +0.0830 | +0.0700 | `TAB-4.8_exp5_degradation.md` |
| DDR | +0.0780 | +0.0570 | `TAB-4.9_exp6_device.md` |
| APTOS | +0.0720 | +0.0889 | `TAB-4.6_exp3_transfer.md` |
| Messidor-2 | +0.0630 | +0.0510 | `TAB-4.8_exp5_degradation.md` |

The domains for which the pipeline reduces the distance most (ODIR-5K, RFMiD) are the same ones where
it produces the largest wF1 gain; the smallest reduction (Messidor-2) corresponds to the smallest
gain. **This is an association over 6 points, not causation:** no formal correlation test was run on
the available data, and the ordering does not match perfectly (APTOS stands out upward on gain at a
middling Δd). Carry this into the text as consistency of the mechanism, without quantitative claims
about the strength of the relationship.

## Caveats

- MMD is computed over penultimate-layer features and therefore **depends on the model itself** —
  d(BASE, X) and d(INT, X) are measured in different feature spaces. Strictly speaking, what is
  compared is not "distances in a single space" but "the relative remoteness of the target domain
  within each arm's own space". This is standard practice, but it requires a caveat in the text.
- The MMD kernel, the per-domain sample size and the number of bootstrap iterations for the CIs are
  not recorded in the run's source data — **when carrying this into the chapter, they must be stated
  from the experiment configuration**.
