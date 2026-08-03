# Conclusions — Experiment 5 (clinical degradation, H-7) → §4.6

**What was done.** An assessment of resistance to degradation on the external clinical sets IDRiD
(n = 413) and Messidor-2 (n = 1 744), zero-shot from EyePACS. The drop metric:
Δ_drop = wF1_in-domain − wF1_external (smaller = more resistant). Hypothesis H-7: full degrades less
than baseline. Source: the **2026-08-03** run.

## What was found

**1. Absolute performance on the external sets is significantly higher for the pipeline on both.**
IDRiD: 0.5913 → 0.6613 (Δ +0.0700, CI [+0.0526, +0.1000], p = 0.0021).
Messidor-2: 0.6280 → 0.6840 (Δ +0.0560, CI [+0.0355, +0.0807], p = 0.0138).

**2. But the hypothesis as written is met on only one set of two, and within noise.**
Δ_drop: IDRiD 0.1625 → 0.1580 (−0.0045, ✓ but the margin is negligible); Messidor-2 0.1258 → 0.1353
(+0.0095, ✗ — the sign is reversed). `h7_supported` — **partial, 1/2**.

**3. The reason for the discrepancy is a property of the metric itself.** Δ_drop is measured from each
arm's **own** in-domain level, and the pipeline's is 6.55 pp higher (0.8193 against 0.7538). An arm
with a higher starting point is bound to lose more in absolute units to arrive at the same external
level. **Δ_drop systematically penalizes the stronger arm.** Relative degradation confirms this: on
Messidor-2 baseline loses 16.7% of its level and the pipeline 16.5% (on IDRiD, 21.6% against 19.3%),
i.e. proportionally the arms degrade the same or slightly in the pipeline's favour.

**4. Consistent with the H-3 mechanism.** The smallest MMD-distance reduction among all six domains
is precisely for Messidor-2 (Δd +0.0586); the same set has the smallest wF1 gain (+0.056) and is the
only case where the pipeline's Δ_drop is worse. The ranking by distance reduction agrees with the
ranking by size of gain.

## Honest interpretation (the key point)

The pipeline **does not make the model more resistant to a change of clinical domain** — it makes it
**better at every point**, including the external sets. This is a weaker claim than H-7, but a
confirmed and practically useful one: on deployment at a new clinic the expected quality is higher,
even though the relative drop from in-domain stays the same.

**Formulation for §4.6:** "the integrated configuration does not reduce the absolute size of the drop
on transfer to external clinical sets, but delivers statistically significantly higher absolute
performance on both (+0.070, p = 0.0021 and +0.056, p = 0.0138)".

**A methodological observation as a contribution in its own right for §5.4:** Δ_drop is not a neutral
measure of resistance when the baseline levels are unequal. It is more correct to compare relative
degradation (Δ_drop / in-domain) or absolute external quality. This is worth setting out separately —
a critique of a metric widely used in the domain-shift literature.

## Contrast (important for the narrative)

Contrast this with exp7: where the model **is trained** on the target clinical domain
(IDRiD → Clinical), the pipeline delivers +0.079 wF1 at n = 60. That is, the pipeline helps both when
training in-domain and under zero-shot transfer — but in the first case it raises quality, while in
the second it **does not change the proportion** of the drop.

## Caveats

- Evaluation uses **fold 0** checkpoints; there is no between-fold variance.
- Relative degradation was computed here from the values given; it is not separately recorded in the
  run data.
- The same two sets appear in exp6 as camera groups (`kowa_idrid`, `topcon_messidor2`) — the numbers
  coincide.

Table: `tables/TAB-4.8_exp5_degradation.md`. Card: `hypotheses/H-7.md`.
