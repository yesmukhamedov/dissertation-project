# TAB-4.6 — Experiment 3: Cross-Dataset Transfer to APTOS 2019 (H-4)

EyePACS → APTOS 2019 (n = 3 662), zero-shot. EfficientNet-B3.
Threshold: **G = F1_APTOS / F1_EyePACS ≥ 0.85**. Source: the **2026-08-03** run (`VALUES.md` §4).

| Arm | In-domain wF1 (EyePACS) | APTOS wF1 | APTOS ROC-AUC | APTOS κ | APTOS Acc | macro-F1 | **G** | G ≥ 0.85 |
|-----|------------------------:|----------:|--------------:|--------:|----------:|---------:|------:|:--------:|
| C — Baseline (3ch) | 0.7538 | 0.6465 | 0.7940 | 0.7887 | 0.6338 | 0.4649 | **0.8577** | ✓ |
| D — Full pipeline (4ch) | 0.8193 | **0.7354** | **0.8263** | **0.8874** | **0.7272** | **0.5666** | **0.8976** | ✓ |

## Pairwise differences (§4.2)

| Metric | Δ (D − C) | 95% CI (Δ) | CI excludes 0 |
|---------|----------:|------------|:--------------:|
| wF1 | +0.0889 | [+0.0681, +0.1197] | ✓ |
| ROC-AUC | +0.0323 | [+0.0224, +0.0482] | ✓ |

## Per-class F1 on APTOS (§4.3)

| Arm | DR0 | DR1 | DR2 | DR3 | DR4 | macro-F1 |
|-----|----:|----:|----:|----:|----:|---------:|
| C | 0.8554 | 0.1395 | 0.5747 | 0.2438 | 0.5113 | 0.4649 |
| D | **0.9152** | **0.2720** | **0.6931** | **0.3252** | **0.6275** | **0.5666** |

The pipeline wins **on all five grades**; the largest relative gains are DR1 (×1.95) and DR3 (×1.33).

## Confusion matrices — APTOS, n = 3 662 (§4.4)

Class sizes: DR0 1 805 · DR1 370 · DR2 999 · DR3 193 · DR4 295.

**Config C (baseline)**

| true \ pred | DR0 | DR1 | DR2 | DR3 | DR4 |
|------------|----:|----:|----:|----:|----:|
| DR0 | 1570 | 186 | 39 | 8 | 2 |
| DR1 | 184 | 63 | 98 | 21 | 4 |
| DR2 | 96 | 245 | 500 | 131 | 27 |
| DR3 | 10 | 24 | 62 | 64 | 33 |
| DR4 | 6 | 15 | 42 | 108 | 124 |

**Config D (full pipeline)**

| true \ pred | DR0 | DR1 | DR2 | DR3 | DR4 |
|------------|----:|----:|----:|----:|----:|
| DR0 | 1678 | 111 | 14 | 2 | 0 |
| DR1 | 150 | 108 | 99 | 12 | 1 |
| DR2 | 33 | 192 | 630 | 129 | 15 |
| DR3 | 1 | 10 | 56 | 87 | 39 |
| DR4 | 0 | 3 | 20 | 112 | 160 |

## Referable DR on APTOS (§4.5)

| Arm | Sensitivity | Specificity | PPV | NPV | Referable AUC |
|-----|------------:|------------:|----:|----:|--------------:|
| C | 0.7337 | 0.9209 | 0.8638 | 0.8349 | 0.8944 |
| D | **0.8393** | **0.9411** | **0.9070** | **0.8955** | **0.9346** |

## Verdict: `h4_supported = true`

Both parts of the hypothesis are met:

1. **The threshold is cleared.** G_D = 0.8976 ≥ 0.85, with a margin of 0.048.
2. **The pipeline transfers better than baseline.** G_D 0.8976 against G_C 0.8577; the absolute APTOS
   wF1 is higher by +0.0889 (CI [+0.0681, +0.1197]).

An important nuance: **the baseline also clears the threshold** (G_C = 0.8577). That is, the "G ≥ 0.85"
part of H-4 does not discriminate between the arms — what discriminates them is the "better than
baseline" part, and that is met convincingly. This is worth stating when writing the text: the
pipeline does not rescue transfer, it improves transfer that is already acceptable.

Mechanism: the pipeline holds on to the **intermediate grades**. Class DR2 — F1 0.5747 → 0.6931; in
the confusion matrix the mass of DR2 → DR1 falls from 245 to 192 instances, and DR2 → DR0 from 96 to
33. Errors remain adjacent on the scale, which is what explains the large κ gain (0.7887 → 0.8874).

Binary "refer / do not refer" triage transfers well for both arms (referable AUC 0.894 and 0.935),
but the pipeline's sensitivity is higher by +10.6 pp with simultaneously higher specificity.

## Caveats

- Evaluation uses **fold 0** checkpoints; there is no between-fold variance for this experiment, so
  the 95% CIs of the differences are per-instance (bootstrap), not per-fold.
- G is computed relative to each arm's own in-domain wF1 (C: 0.7538, D: 0.8193), so the arm with the
  higher in-domain score has the larger denominator — the gain in G (+0.040) is by construction more
  conservative than the gain in absolute APTOS wF1 (+0.089).

APTOS clinical metrics in consolidated form — `TAB-5.4_clinical_referable.md`.
Domain distances (MMD/KL) — `H-3_domain_distance.md`.
