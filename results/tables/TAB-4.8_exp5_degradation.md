# TAB-4.8 — Experiment 5: Clinical Degradation Resistance (H-7)

External clinical sets, zero-shot from EyePACS. EfficientNet-B3.
Degradation metric: `Δ_drop = wF1_in-domain − wF1_external` (smaller = more resistant).
In-domain: C = 0.7538, D = 0.8193. Source: the **2026-08-03** run (`VALUES.md` §7).

## Absolute performance on the external sets (§7.1)

| Set | n | wF1 (C) | wF1 (D) | Δ (D − C) | 95% CI (Δ) | p (1-sided) |
|-------|--:|--------:|--------:|----------:|------------|------------:|
| IDRiD | 413 | 0.5957 | **0.6592** | +0.0635 | [+0.0445, +0.0919] | **0.0021** |
| Messidor-2 | 1 744 | 0.6283 | **0.6809** | +0.0526 | [+0.0264, +0.0716] | **0.0138** |

## Size of the degradation relative to in-domain (§7.3)

| Set | Δ_drop (C) | Δ_drop (D) | Δ_drop(D) − Δ_drop(C) | Δ_full < Δ_base? |
|-------|-----------:|-----------:|----------------------:|:----------------:|
| IDRiD | **0.1581** | 0.1601 | +0.0020 | ✗ |
| Messidor-2 | **0.1255** | 0.1384 | +0.0129 | ✗ |

## Verdict: `h7_supported` — NOT SUPPORTED as written (0 of 2 sets); unambiguous win in absolute terms

> ⚠️ **Change from the previous revision.** H-7 was reported there as **partial (1 of 2)** — IDRiD
> passed by a hair (−0.0045). In the current run IDRiD flips sign too (+0.0020), so the as-written
> criterion now fails on **both** sets. The verdict must be reported as **0/2**, not 1/2.

Two formulations must be strictly separated here, because they give **different** answers:

**(a) The hypothesis as written — "Δ_full < Δ_base" — fails on both sets.** IDRiD: the pipeline loses
0.1601 against baseline's 0.1581 (+0.0020). Messidor-2: 0.1384 against 0.1255 (+0.0129). Neither
difference is large — the IDRiD gap is far inside the width of the CIs on the absolute metrics — but
both point the wrong way. It is **not permissible** to claim in any form that "the pipeline is more
resistant to clinical degradation".

**(b) The practically meaningful claim — "the pipeline performs better on external clinical sets" —
is confirmed on both sets and statistically.** wF1 is higher by +0.0635 (p = 0.0021) and +0.0526
(p = 0.0138), and both CIs exclude zero.

The reason for the divergence is formal, and the same as before: Δ_drop is measured from each arm's
**own** in-domain level, and the pipeline's is 6.55 pp higher. An arm with a higher starting point
must lose more in absolute units to arrive at the same external level — **Δ_drop structurally
penalizes the stronger arm.** Relative degradation shows how little is actually at stake:

| Set | relative drop (C) | relative drop (D) | favours |
|---|---:|---:|---|
| IDRiD | 21.0% | **19.5%** | pipeline |
| Messidor-2 | **16.6%** | 16.9% | baseline (marginally) |

In proportional terms the two arms degrade almost identically, with IDRiD favouring the pipeline and
Messidor-2 the baseline by a fraction of a percentage point. There is no resistance effect in either
direction — what there is, is a uniformly higher level.

**Formulation for the text:** "the integrated configuration does not reduce the size of the drop on
transfer to external clinical sets — on the Δ_drop criterion it is marginally worse on both sets —
but delivers statistically significantly higher absolute performance on both (Δ wF1 +0.064 and
+0.053)". Hypothesis H-7 in its original wording should be reported as **not supported**, with the
Δ_drop bias analysis carried into §5.4 as a contribution in its own right.

## Caveats

- Evaluation uses **fold 0** checkpoints; there is no between-fold variance.
- Δ_drop as a resistance metric is poorly defined when the in-domain levels are unequal (see above);
  relative degradation (Δ_drop / in-domain) is the fairer quantity and is given in the text above,
  but it is not separately recorded in the run's source data.
- The same two sets appear in exp6 as camera groups (`TAB-4.9_exp6_device.md`) — the numbers there are the same.

Domain distances for these sets — `H-3_domain_distance.md` (IDRiD Δd +0.0816, Messidor-2 +0.0700).
Note that the ordering no longer lines up: IDRiD has the larger distance reduction *and* the larger
wF1 gain here, but across all six domains the two quantities do not track each other — see the
caveat in that table.
Hypothesis card — `hypotheses/H-7.md`.
