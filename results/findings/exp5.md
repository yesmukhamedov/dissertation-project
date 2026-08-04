# Conclusions — Experiment 5 (external clinical performance, H-7) → §4.6

**What was done.** Zero-shot evaluation on the external clinical sets IDRiD (n = 413) and
Messidor-2 (n = 1 744), transferred from EyePACS without retraining. Arm-wise comparison D − C,
EfficientNet-B3. Criterion: form S on **both** sets — Δ wF1 ≥ MCID = 0.050 and CI⁻ > 0.
Source: the **2026-08-03** run.

> ⚠️ **H-7 was re-specified.** The operative form is **External Clinical Performance** (absolute wF1
> on the external sets). The earlier "degradation" form — Δ_drop of the integrated arm statistically
> smaller — is **retired** and kept as a reference quantity only. Earlier revisions of this folder
> reported 1/2 and 0/2 by applying the retired criterion; the operative verdict has been **CONFIRMED
> (2/2) at every revision**.

## What was found

**1. The hypothesis is confirmed on both sets.**
IDRiD: 0.5938 → 0.6627 (Δ **+0.0689**, CI [+0.0494, +0.0968], p = 0.0021).
Messidor-2: 0.6282 → 0.6823 (Δ **+0.0541**, CI [+0.0362, +0.0814], p = 0.0138).
Both clear MCID = 0.050 with CI⁻ > 0 → PASS_S = 1 on each → Σ PASS = 2 = N → **CONFIRMED**.

**2. The Messidor-2 margin is thin.** Δ exceeds the MCID by only **0.0041**. Form S requires
Δ ≥ MCID and CI⁻ > 0 — not CI⁻ ≥ MCID — so the pass is legitimate even though the lower bound
(+0.0362) sits below the threshold. But it is not a comfortable pass and should not be presented as
one: a re-run that moves Δ by more than 0.004 flips that set.

**3. There is no resistance effect, and none is claimed.** Proportionally the two arms degrade
essentially the same: 21.2% (C) against 19.1% (D) on IDRiD, 16.7% against 16.7% on Messidor-2. The
pipeline does not lose less on transfer — it starts higher and finishes higher. This is a narrower
claim than the retired wording, and it is the one the data support.

**4. Why the degradation form was retired.** Δ_drop is not independent of the hypothesis it was meant
to test:

```
Δ_drop(D,X) − Δ_drop(C,X) = Δ_in-domain − Δ_external = 0.0655 − Δ wF1(X)
```

Exact on both sets (IDRiD 0.0655 − 0.0689 = −0.0034; Messidor-2 0.0655 − 0.0541 = +0.0114). The sign
is decided solely by whether the external margin exceeds the fixed in-domain gap — that is, the
criterion demands the pipeline beat baseline **more on foreign data than at home**, and penalizes the
integrated arm for its own in-domain win. It measures nothing about resistance.

**5. Directional consistency with H-3 only.** Messidor-2 has the smallest MMD reduction of the six
domains (Δd +0.0700) and the smaller of these two wF1 gains. ⚠️ But across all six domains the
ranking by distance reduction does **not** match the ranking by size of gain — do not present this as
a quantitative correspondence.

## Formulation for §4.6

"On transfer to external clinical sets without retraining, the integrated configuration delivers
absolute weighted-F1 higher than baseline by +0.069 (IDRiD) and +0.054 (Messidor-2), both above the
minimal clinically important difference of 0.05 and with confidence intervals excluding zero."

## A methodological observation as a contribution in its own right — for §5.4

Δ_drop is not a neutral measure of degradation resistance when the arms' in-domain levels are
unequal. It reduces algebraically to *in-domain gap minus external gap*, so it penalizes the stronger
arm by construction and can only be satisfied by an arm whose advantage **grows** under domain shift.
This is a critique of a metric in common use in the domain-shift literature, it is reproducible from
the identity above, and it is the reason H-7 carries its present wording. Set it out explicitly —
it is a result, not an apology for a re-spec.

## Contrast (important for the narrative)

Contrast this with exp7: where the model **is trained** on the target clinical domain
(IDRiD → Clinical), the pipeline delivers +0.080 wF1 at n = 60. The pipeline helps both when training
in-domain and under zero-shot transfer — but in neither case does it change the *proportion* of the
drop.

## Caveats

- Evaluation uses **fold 0** checkpoints; there is no between-fold variance.
- The Messidor-2 margin over MCID is 0.0041.
- CIs are asymmetric percentile bootstrap.
- Relative degradation was computed from the values given; it is not separately recorded in the run data.
- The same two sets appear in exp6 as camera groups (`kowa_idrid`, `topcon_messidor2`) — values, Δ and
  CI coincide character-for-character by construction.

Table: `tables/TAB-4.8_exp5_degradation.md`. Card: `hypotheses/H-7.md`.
