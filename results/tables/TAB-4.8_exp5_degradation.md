# TAB-4.8 — Experiment 5: Clinical Degradation Resistance (H-7)

External clinical sets, zero-shot from EyePACS. EfficientNet-B3.
Degradation metric: `Δ_drop = wF1_in-domain − wF1_external` (smaller = more resistant).
In-domain: C = 0.7538, D = 0.8193. Source: the **2026-08-02** run (`VALUES.md` §7).

## Absolute performance on the external sets (§7.1)

| Set | n | wF1 (C) | wF1 (D) | Δ (D − C) | 95% CI (Δ) | p (1-sided) |
|-------|--:|--------:|--------:|----------:|------------|------------:|
| IDRiD | 413 | 0.5920 | **0.6620** | +0.0700 | [+0.0463, +0.0937] | **0.0021** |
| Messidor-2 | 1 744 | 0.6270 | **0.6780** | +0.0510 | [+0.0284, +0.0736] | **0.0138** |

## Size of the degradation relative to in-domain (§7.3)

| Set | Δ_drop (C) | Δ_drop (D) | Δ_drop(D) − Δ_drop(C) | Δ_full < Δ_base? |
|-------|-----------:|-----------:|----------------------:|:----------------:|
| IDRiD | 0.1618 | **0.1573** | −0.0045 | ✓ (negligibly) |
| Messidor-2 | **0.1268** | 0.1413 | +0.0145 | ✗ |

## Verdict: `h7_supported` — PARTIAL (1 of 2 sets), with an unambiguous win in absolute terms

Two formulations must be strictly separated here, because they give **different** answers:

**(a) The hypothesis as written — "Δ_full < Δ_base" — is confirmed only on IDRiD, and by a negligible
margin.** On IDRiD the pipeline loses 0.1573 against baseline's 0.1618 (a difference of −0.0045 — an
order of magnitude smaller than the width of the CIs on the absolute metrics). On Messidor-2 the sign
is **reversed**: the pipeline loses MORE (0.1413 against 0.1268). By the strict criterion: **1 of 2**,
and on IDRiD the difference is within noise. It is **not permissible** to claim that "the pipeline is
more resistant to clinical degradation".

**(b) The practically meaningful claim — "the pipeline performs better on external clinical sets" —
is confirmed on both sets and statistically.** wF1 is higher by +0.0700 (p = 0.0021) and +0.0510
(p = 0.0138), and both CIs exclude zero.

The reason for the discrepancy is formal: Δ_drop is measured from each arm's **own** in-domain level,
and the pipeline's is 6.55 pp higher. An arm with a higher starting point is bound to lose more in
absolute units to arrive at the same external level. Relative degradation confirms this: on
Messidor-2 C loses 16.8% of its in-domain level and D loses 17.2%, i.e. **proportionally the arms
degrade identically**, and the pipeline simply starts higher and finishes higher.

**Formulation for the text:** "the integrated configuration does not reduce the *relative* size of
the drop on transfer to external clinical sets, but delivers statistically significantly higher
absolute performance on both (Δ wF1 +0.070 and +0.051)". Hypothesis H-7 in its original wording
should be reported as **partially confirmed**, with an explicit note that the Δ_drop metric
systematically penalizes the stronger arm.

## Caveats

- Evaluation uses **fold 0** checkpoints; there is no between-fold variance.
- Δ_drop as a resistance metric is poorly defined when the in-domain levels are unequal (see above);
  relative degradation (Δ_drop / in-domain) is the fairer quantity and is given in the text above,
  but it is not separately recorded in the run's source data.
- The same two sets appear in exp6 as camera groups (`TAB-4.9_exp6_device.md`) — the numbers there are the same.

Domain distances for these sets — `H-3_domain_distance.md` (IDRiD Δd +0.0830, Messidor-2 +0.0630:
the smallest reduction in distance falls on the set with the smallest wF1 gain).
Hypothesis card — `hypotheses/H-7.md`.
