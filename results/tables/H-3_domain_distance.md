# H-3 — Domain Distance: MMD and KL between the source and target domains

A test that preprocessing **brings the domain distributions closer together**. Two independent
measures: MMD over penultimate-layer features (representational level) and KL over per-channel
histograms (pixel level). BASE = the baseline arm (3ch), INT = the integrated arm (4ch, full pipeline).
Source: the **2026-08-03** run (`VALUES.md` §3).

> A block introduced in the 2026-08-02 run — before it, domain distances were not measured. The
> values below are from the 2026-08-03 re-run.

## MMD over penultimate-layer features (§3.1)

Smaller = closer to the source domain (EyePACS). Δd = d_BASE − d_INT; Δd > 0 means the pipeline
reduces the distance.

| Target domain X | d(BASE, X) | d(INT, X) | Δd | 95% CI (Δd) | CI excludes 0 |
|---|---:|---:|---:|---|:---:|
| APTOS | 0.1886 | 0.1139 | +0.0747 | [+0.0375, +0.0991] | ✓ |
| IDRiD | 0.2272 | 0.1456 | +0.0816 | [+0.0403, +0.1101] | ✓ |
| Messidor-2 | 0.1717 | 0.1131 | +0.0586 | [+0.0367, +0.0923] | ✓ |
| DDR | 0.2070 | 0.1322 | +0.0748 | [+0.0497, +0.1171] | ✓ |
| ODIR-5K | 0.2474 | 0.1537 | +0.0937 | [+0.0536, +0.1254] | ✓ |
| RFMiD | 0.2563 | 0.1699 | +0.0864 | [+0.0387, +0.1143] | ✓ |

## KL over per-channel histograms (§3.2)

| Target domain X | d_KL(BASE, X) | d_KL(INT, X) | Reduction |
|---|---:|---:|---:|
| APTOS | 0.0916 | 0.0611 | −33% |
| IDRiD | 0.1162 | 0.0753 | −35% |
| Messidor-2 | 0.0852 | 0.0554 | −35% |
| DDR | 0.1055 | 0.0656 | −38% |
| ODIR-5K | 0.1273 | 0.0829 | −35% |
| RFMiD | 0.1330 | 0.0899 | −32% |

The Stage 7 normalization uses source-domain statistics (the target domains do not recompute their
own statistics), so the reduction in distance is achieved by stages 0–6 rather than by fitting the
normalization to the target set.

## Verdict: `h3_supported = true`

1. **The direction is the same for all six target domains** on both measures, with no exceptions.
2. **All six 95% CIs on Δd exclude zero** — the effect is statistically stable at the
   representational level.
3. **The KL reduction lies in a narrow band (−32…−38%)** regardless of how far the domain was to begin
   with. This points to a multiplicative character of the normalization: the pipeline compresses the
   photometric spread by a roughly fixed proportion rather than "pulling" distant domains up to
   nearby ones.
4. **The ranking of the domains is preserved** after preprocessing: RFMiD remains the most distant
   (0.2563 → 0.1699) and Messidor-2 the closest (0.1717 → 0.1131). That is, the residual difference
   between the sets is substantive in nature (population composition, imaging protocol) and does not
   reduce to illumination and contrast.

## Relation to the transfer results

The size of the MMD reduction agrees with the size of the transfer gain:

| Domain | Δd (MMD) | Δ wF1 (D − C) on transfer | Source |
|---|---:|---:|---|
| ODIR-5K | +0.0937 | +0.0836 | `TAB-4.9_exp6_device.md` |
| RFMiD | +0.0864 | +0.0898 | `TAB-4.9_exp6_device.md` |
| IDRiD | +0.0816 | +0.0700 | `TAB-4.8_exp5_degradation.md` |
| DDR | +0.0748 | +0.0582 | `TAB-4.9_exp6_device.md` |
| APTOS | +0.0747 | +0.0887 | `TAB-4.6_exp3_transfer.md` |
| Messidor-2 | +0.0586 | +0.0560 | `TAB-4.8_exp5_degradation.md` |

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
