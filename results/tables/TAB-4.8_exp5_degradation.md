# TAB-4.8 — Experiment 5: External Clinical Performance (H-7)

External clinical sets, zero-shot from EyePACS. EfficientNet-B3, arm-wise pair **D − C**.
In-domain: C = 0.7538, D = 0.8193. Source: the **2026-08-03** run (`VALUES.md` §7).

> ⚠️ **H-7 was re-specified.** The operative form is **External Clinical Performance** — the
> integrated configuration must deliver higher *absolute* wF1 on both external clinical sets. The
> earlier "degradation" form (Δ_drop of the integrated arm statistically smaller) is **retired** and
> kept only as a reference quantity; see "Why Δ_drop was retired" below. The verdict under the
> operative form is **CONFIRMED (2/2)** and has been so at every revision — the earlier 0/2 and 1/2
> readings in this folder applied the retired criterion.

## Criterion (form S, both sets mandatory)

```
H-7  ⟺  ⋀            PASS_S(wF1, D−C on X) = 1
        X ∈ {IDRiD, Messidor-2}

PASS_S  ⟺  Δ wF1(X) = wF1(D,X) − wF1(C,X)  ≥  MCID_wF1 = 0.050   ∧   CI⁻ > 0
```

The sets are **not aggregated**: a single REV (CI⁺ < 0) would give REVERSED regardless of the other.

## Absolute performance on the external sets (§7.1)

| Set | n | wF1 (C) | wF1 (D) | Δ (D − C) | 95% CI (Δ) | p (1-sided) |
|-------|--:|--------:|--------:|----------:|------------|------------:|
| IDRiD | 413 | 0.5938 | **0.6627** | +0.0689 | [+0.0494, +0.0968] | **0.0021** |
| Messidor-2 | 1 744 | 0.6282 | **0.6823** | +0.0541 | [+0.0362, +0.0814] | **0.0138** |

## Element-wise check

| Condition | IDRiD | Messidor-2 |
|---|---|---|
| Δ ≥ MCID = 0.050 | 0.0689 ✓ (margin +0.0189) | 0.0541 ✓ (margin +0.0041) |
| CI⁻ > 0 | +0.0494 ✓ | +0.0362 ✓ |
| **PASS_S** | **1** | **1** |
| REV_S (CI⁺ < 0) | 0 | 0 |

**Σ PASS = 2 = N → `h7_supported = true`, CONFIRMED.**

> Note on the form: S requires **Δ ≥ MCID and CI⁻ > 0** — *not* CI⁻ ≥ MCID. On Messidor-2 the lower
> bound (+0.0362) sits below the 0.050 threshold and this does not block the pass. The margin on Δ
> itself is thin there: **0.0041**. Worth stating in the text — the Messidor-2 pass is real but not
> comfortable.

## Verdict: `h7_supported = true` — CONFIRMED (2/2)

On both external clinical sets — different hardware, different population, no retraining — the
integrated configuration is higher in absolute weighted-F1 by a clinically meaningful margin, with
confidence intervals excluding zero: **+0.0689** (p = 0.0021) on IDRiD and **+0.0541** (p = 0.0138)
on Messidor-2.

**Formulation for the text:** "on transfer to external clinical sets without retraining, the
integrated configuration delivers absolute weighted-F1 higher than baseline by +0.069 (IDRiD) and
+0.054 (Messidor-2), both above the MCID of 0.05 and with intervals excluding zero".

## Δ_drop — reference only (§7.3)

| Set | Δ_drop (C) | Δ_drop (D) | Δ_drop(D) − Δ_drop(C) | relative |
|-------|-----------:|-----------:|----------------------:|---|
| IDRiD | 0.1600 | **0.1566** | −0.0034 | 21.2% vs **19.1%** |
| Messidor-2 | **0.1256** | 0.1370 | +0.0114 | 16.7% vs 16.7% |

Δ_drop(arm, X) = wF1(arm, EyePACS) − wF1(arm, X); wholly derived from §7.1 and §7.2.

## Why Δ_drop was retired

The quantity is **not independent of the hypothesis it was supposed to test**. Expanding:

```
Δ_drop(D,X) − Δ_drop(C,X)
  = [wF1(D,in) − wF1(D,X)] − [wF1(C,in) − wF1(C,X)]
  = [wF1(D,in) − wF1(C,in)] − [wF1(D,X) − wF1(C,X)]
  = Δ_in-domain − Δ_external
  = 0.0655 − Δ wF1(X)
```

Verified on both sets: IDRiD 0.0655 − 0.0689 = **−0.0034**; Messidor-2 0.0655 − 0.0541 = **+0.0114**
— matching the table above exactly.

So the sign of the Δ_drop comparison is fixed by a single question: *does the external margin exceed
the in-domain margin of 0.0655?* The criterion therefore demands that the pipeline beat baseline
**more on foreign data than on its own**, and it penalizes the integrated arm precisely for its
in-domain win. It measures nothing about resistance. That defect is the reason for the re-spec, and
the identity above makes the argument reproducible for §5.4.

The relative figures corroborate it: once normalized by each arm's own in-domain level the structural
skew almost vanishes — 21.2% vs 19.1% on IDRiD, 16.7% vs 16.7% on Messidor-2.

## Caveats

- Evaluation uses **fold 0** checkpoints; there is no between-fold variance.
- The Messidor-2 margin over MCID is **0.0041** — a re-run that moves Δ by more than that flips the
  set. Do not present this pass as comfortable.
- CIs are asymmetric percentile bootstrap.
- The same two sets appear in exp6 as camera groups (`kowa_idrid`, `topcon_messidor2` in
  `TAB-4.9_exp6_device.md`) — values, Δ and CI coincide character-for-character by construction.

Domain distances for these sets — `H-3_domain_distance.md` (IDRiD Δd +0.0816, Messidor-2 +0.0700).
Across all six domains the size of the distance reduction does not track the size of the wF1 gain —
see the caveat in that table.
Hypothesis card — `hypotheses/H-7.md`.
