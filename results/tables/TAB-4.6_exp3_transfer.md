# TAB-4.6 — Experiment 3: Cross-Dataset Transfer to APTOS 2019 (H-4)

EyePACS → APTOS 2019 (n = 3 662), zero-shot. EfficientNet-B3.
Threshold: **G = F1_APTOS / F1_EyePACS ≥ 0.85**. Source: the **2026-08-02** run (`VALUES.md` §4).

| Arm | In-domain wF1 (EyePACS) | APTOS wF1 | APTOS ROC-AUC | APTOS κ | APTOS Acc | macro-F1 | **G** | G ≥ 0.85 |
|-----|------------------------:|----------:|--------------:|--------:|----------:|---------:|------:|:--------:|
| C — Baseline (3ch) | 0.7538 | 0.6465 | 0.7920 | 0.7879 | 0.6338 | 0.4650 | **0.8577** | ✓ |
| D — Full pipeline (4ch) | 0.8193 | **0.7354** | **0.8290** | **0.8848** | **0.7275** | **0.5671** | **0.8976** | ✓ |

## Pairwise differences (§4.2)

| Metric | Δ (D − C) | 95% CI (Δ) | CI excludes 0 |
|---------|----------:|------------|:--------------:|
| wF1 | +0.0889 | [+0.0631, +0.1147] | ✓ |
| ROC-AUC | +0.0370 | [+0.0241, +0.0499] | ✓ |

## Per-class F1 on APTOS (§4.3)

| Arm | DR0 | DR1 | DR2 | DR3 | DR4 | macro-F1 |
|-----|----:|----:|----:|----:|----:|---------:|
| C | 0.8554 | 0.1394 | 0.5747 | 0.2443 | 0.5113 | 0.4650 |
| D | **0.9150** | **0.2717** | **0.6931** | **0.3271** | **0.6287** | **0.5671** |

The pipeline wins **on all five grades**; the largest relative gains are DR1 (×1.95) and DR3 (×1.34).

## Confusion matrices — APTOS, n = 3 662 (§4.4)

Class sizes: DR0 1 805 · DR1 370 · DR2 999 · DR3 193 · DR4 295.

**Config C (baseline)**

| true \ pred | DR0 | DR1 | DR2 | DR3 | DR4 |
|------------|----:|----:|----:|----:|----:|
| DR0 | 1570 | 186 | 39 | 8 | 2 |
| DR1 | 184 | 63 | 98 | 21 | 4 |
| DR2 | 96 | 245 | 500 | 131 | 27 |
| DR3 | 10 | 24 | 62 | 64 | 33 |
| DR4 | 6 | 16 | 42 | 107 | 124 |

**Config D (full pipeline)**

| true \ pred | DR0 | DR1 | DR2 | DR3 | DR4 |
|------------|----:|----:|----:|----:|----:|
| DR0 | 1679 | 111 | 13 | 2 | 0 |
| DR1 | 149 | 108 | 100 | 12 | 1 |
| DR2 | 34 | 192 | 630 | 128 | 15 |
| DR3 | 2 | 10 | 56 | 87 | 38 |
| DR4 | 1 | 4 | 20 | 110 | 160 |

## Referable DR on APTOS (§4.5)

| Arm | Sensitivity | Specificity | PPV | NPV | Referable AUC |
|-----|------------:|------------:|----:|----:|--------------:|
| C | 0.7330 | 0.9209 | 0.8637 | 0.8346 | 0.8930 |
| D | **0.8366** | **0.9411** | **0.9067** | **0.8939** | **0.9340** |

## Verdict: `h4_supported = true`

Both parts of the hypothesis are met:

1. **The threshold is cleared.** G_D = 0.8976 ≥ 0.85, with a margin of 0.048.
2. **The pipeline transfers better than baseline.** G_D 0.8976 against G_C 0.8577; the absolute APTOS
   wF1 is higher by +0.0889 (CI [+0.0631, +0.1147]).

An important nuance: **the baseline also clears the threshold** (G_C = 0.8577). That is, the "G ≥ 0.85"
part of H-4 does not discriminate between the arms — what discriminates them is the "better than
baseline" part, and that is met convincingly. This is worth stating when writing the text: the
pipeline does not rescue transfer, it improves transfer that is already acceptable.

Mechanism: the pipeline holds on to the **intermediate grades**. Class DR2 — F1 0.5747 → 0.6931; in
the confusion matrix the mass of DR2 → DR1 falls from 245 to 192 instances, and DR2 → DR0 from 96 to
34. Errors remain adjacent on the scale, which is what explains the large κ gain (0.7879 → 0.8848).

Binary "refer / do not refer" triage transfers well for both arms (referable AUC 0.893 and 0.934),
but the pipeline's sensitivity is higher by +10.4 pp with simultaneously higher specificity.

## Caveats

- Evaluation uses **fold 0** checkpoints; there is no between-fold variance for this experiment, so
  the 95% CIs of the differences are per-instance (bootstrap), not per-fold.
- G is computed relative to each arm's own in-domain wF1 (C: 0.7538, D: 0.8193), so the arm with the
  higher in-domain score has the larger denominator — the gain in G (+0.040) is by construction more
  conservative than the gain in absolute APTOS wF1 (+0.089).

APTOS clinical metrics in consolidated form — `TAB-5.4_clinical_referable.md`.
Domain distances (MMD/KL) — `H-3_domain_distance.md`.
