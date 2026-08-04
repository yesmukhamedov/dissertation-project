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
| APTOS | 0.1910 | 0.1178 | +0.0732 | [+0.0380, +0.0996] | ✓ |
| IDRiD | 0.2211 | 0.1395 | +0.0816 | [+0.0530, +0.1228] | ✓ |
| Messidor-2 | 0.1768 | 0.1068 | +0.0700 | [+0.0475, +0.1031] | ✓ |
| DDR | 0.2098 | 0.1314 | +0.0784 | [+0.0387, +0.1061] | ✓ |
| ODIR-5K | 0.2387 | 0.1599 | +0.0788 | [+0.0371, +0.1089] | ✓ |
| RFMiD | 0.2606 | 0.1675 | +0.0931 | [+0.0489, +0.1245] | ✓ |

## KL over per-channel histograms (§3.2)

| Target domain X | d_KL(BASE, X) | d_KL(INT, X) | Reduction |
|---|---:|---:|---:|
| APTOS | 0.0894 | 0.0588 | −34% |
| IDRiD | 0.1171 | 0.0725 | −38% |
| Messidor-2 | 0.0905 | 0.0575 | −36% |
| DDR | 0.1067 | 0.0658 | −38% |
| ODIR-5K | 0.1282 | 0.0817 | −36% |
| RFMiD | 0.1370 | 0.0899 | −34% |

The Stage 7 normalization uses source-domain statistics (the target domains do not recompute their
own statistics), so the reduction in distance is achieved by stages 0–6 rather than by fitting the
normalization to the target set.

## Verdict: `h3_supported = true`

1. **The direction is the same for all six target domains** on both measures, with no exceptions.
2. **All six 95% CIs on Δd exclude zero** — the effect is statistically stable at the
   representational level.
3. **The KL reduction lies in a narrow band (−34…−38%)** regardless of how far the domain was to begin
   with. This points to a multiplicative character of the normalization: the pipeline compresses the
   photometric spread by a roughly fixed proportion rather than "pulling" distant domains up to
   nearby ones.
4. **The ranking of the domains is preserved** after preprocessing: RFMiD remains the most distant
   (0.2606 → 0.1675) and Messidor-2 the closest (0.1768 → 0.1068). That is, the residual difference
   between the sets is substantive in nature (population composition, imaging protocol) and does not
   reduce to illumination and contrast.

## Relation to the transfer results

The size of the MMD reduction agrees with the size of the transfer gain:

| Domain | Δd (MMD) | Δ wF1 (D − C) on transfer | Source |
|---|---:|---:|---|
| RFMiD | +0.0931 | +0.0987 | `TAB-4.9_exp6_device.md` |
| IDRiD | +0.0816 | +0.0689 | `TAB-4.8_exp5_degradation.md` |
| ODIR-5K | +0.0788 | +0.0881 | `TAB-4.9_exp6_device.md` |
| DDR | +0.0784 | +0.0517 | `TAB-4.9_exp6_device.md` |
| APTOS | +0.0732 | +0.0889 | `TAB-4.6_exp3_transfer.md` |
| Messidor-2 | +0.0700 | +0.0541 | `TAB-4.8_exp5_degradation.md` |

**The correspondence is weaker than in the previous revision and should be stated cautiously.** The
one clean match is at the top: RFMiD has both the largest distance reduction and the largest wF1 gain.
Below that the two orderings diverge — IDRiD is 2nd on Δd but only 4th on gain, DDR is 4th on Δd yet
has the **smallest** gain of all six, and APTOS is 5th on Δd with the 2nd-largest gain. Rank
correlation over the six points is weak-to-moderate (Spearman ρ ≈ 0.49).

The earlier formulation — "the smallest reduction (Messidor-2) corresponds to the smallest gain" — is
**no longer true** and must not be carried into the text: the smallest gain now belongs to DDR, at a
middling Δd.

**This is an association over 6 points, not causation**, and a loose one. Carry it into the text only
as qualitative consistency of the mechanism (distance falls everywhere, quality rises everywhere),
explicitly **without** claiming that the size of the distance reduction predicts the size of the gain.

## Caveats

- MMD is computed over penultimate-layer features and therefore **depends on the model itself** —
  d(BASE, X) and d(INT, X) are measured in different feature spaces. Strictly speaking, what is
  compared is not "distances in a single space" but "the relative remoteness of the target domain
  within each arm's own space". This is standard practice, but it requires a caveat in the text.
- The MMD kernel, the per-domain sample size and the number of bootstrap iterations for the CIs are
  not recorded in the run's source data — **when carrying this into the chapter, they must be stated
  from the experiment configuration**.
