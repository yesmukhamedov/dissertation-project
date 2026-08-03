# Conclusions — Experiment 5 (clinical degradation, H-7) → §4.6

**What was done.** An assessment of resistance to degradation on the external clinical sets IDRiD
(n = 413) and Messidor-2 (n = 1 744), zero-shot from EyePACS. The drop metric:
Δ_drop = wF1_in-domain − wF1_external (smaller = more resistant). Hypothesis H-7: full degrades less
than baseline. Source: the **2026-08-03** run.

## What was found

**1. Absolute performance on the external sets is significantly higher for the pipeline on both.**
IDRiD: 0.5957 → 0.6592 (Δ +0.0635, CI [+0.0445, +0.0919], p = 0.0021).
Messidor-2: 0.6283 → 0.6809 (Δ +0.0526, CI [+0.0264, +0.0716], p = 0.0138).

**2. But the hypothesis as written now fails on both sets.**
Δ_drop: IDRiD 0.1581 → 0.1601 (+0.0020, ✗); Messidor-2 0.1255 → 0.1384 (+0.0129, ✗).
`h7_supported` — **not supported, 0/2**. ⚠️ **This changes the previous revision**, where IDRiD passed
by −0.0045 and the verdict was "partial, 1/2". Neither gap is large — the IDRiD one sits far inside
the CIs on the absolute metrics — but both now point the wrong way.

**3. The reason is a property of the metric itself.** Δ_drop is measured from each arm's **own**
in-domain level, and the pipeline's is 6.55 pp higher (0.8193 against 0.7538). An arm with a higher
starting point is bound to lose more in absolute units to arrive at the same external level.
**Δ_drop structurally penalizes the stronger arm.** Relative degradation shows how little is at
stake: IDRiD 21.0% (C) against 19.5% (D) — favouring the pipeline; Messidor-2 16.6% against 16.9% —
favouring baseline by a fraction of a point. Proportionally the arms degrade almost identically, one
set leaning each way; there is no resistance effect in either direction.

**4. Consistency with H-3 is directional only.** Messidor-2 has the smallest MMD reduction of the six
domains (Δd +0.0700) and the smaller of these two wF1 gains. ⚠️ But across all six domains the
ranking by distance reduction **no longer** matches the ranking by size of gain (DDR has a middling
Δd and the smallest gain of all) — do not present this as a quantitative correspondence.

## Honest interpretation (the key point)

The pipeline **does not make the model more resistant to a change of clinical domain** — it makes it
**better at every point**, including the external sets. This replaces H-7 rather than qualifying it,
and it is confirmed and practically useful: on deployment at a new clinic the expected quality is
higher, even though the proportional drop from in-domain is unchanged.

**Formulation for §4.6:** "the integrated configuration does not reduce the size of the drop on
transfer to external clinical sets — on the Δ_drop criterion it is marginally worse on both sets —
but delivers statistically significantly higher absolute performance on both (+0.064, p = 0.0021 and
+0.053, p = 0.0138)".

**A methodological observation as a contribution in its own right for §5.4:** Δ_drop is not a neutral
measure of resistance when the baseline levels are unequal. It is more correct to compare relative
degradation (Δ_drop / in-domain) or absolute external quality. This is worth setting out separately —
a critique of a metric widely used in the domain-shift literature. Presenting it this way turns the
negative result into a contribution: the criterion, not the pipeline, is what these two sets expose.
Do not minimize the failure or report it as "partial" — it is 0/2, and the analysis is what carries
the value.

## Contrast (important for the narrative)

Contrast this with exp7: where the model **is trained** on the target clinical domain
(IDRiD → Clinical), the pipeline delivers +0.080 wF1 at n = 60. That is, the pipeline helps both when
training in-domain and under zero-shot transfer — but in the first case it raises quality, while in
the second it **does not change the proportion** of the drop.

## Caveats

- Evaluation uses **fold 0** checkpoints; there is no between-fold variance.
- Relative degradation was computed here from the values given; it is not separately recorded in the
  run data.
- The same two sets appear in exp6 as camera groups (`kowa_idrid`, `topcon_messidor2`) — the numbers
  coincide.

Table: `tables/TAB-4.8_exp5_degradation.md`. Card: `hypotheses/H-7.md`.
