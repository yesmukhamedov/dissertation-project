# TAB-4.6 — Experiment 3: Cross-Dataset Transfer to APTOS 2019 (H-4)

EyePACS → APTOS 2019 (n = 3 662), zero-shot. EfficientNet-B3.
Threshold: **G = F1_APTOS / F1_EyePACS ≥ 0.85**. Source: the **2026-08-03** run (`VALUES.md` §4).

| Arm | In-domain wF1 (EyePACS) | APTOS wF1 | APTOS ROC-AUC | APTOS κ | APTOS Acc | macro-F1 | **G** | G ≥ 0.85 |
|-----|------------------------:|----------:|--------------:|--------:|----------:|---------:|------:|:--------:|
| C — Baseline (3ch) | 0.7538 | 0.6459 | 0.7903 | 0.7865 | 0.6333 | 0.4640 | **0.8569** | ✓ |
| D — Full pipeline (4ch) | 0.8193 | **0.7346** | **0.8271** | **0.8834** | **0.7267** | **0.5658** | **0.8966** | ✓ |

## Pairwise differences (§4.2)

| Metric | Δ (D − C) | 95% CI (Δ) | CI excludes 0 |
|---------|----------:|------------|:--------------:|
| wF1 | +0.0887 | [+0.0572, +0.1088] | ✓ |
| ROC-AUC | +0.0368 | [+0.0211, +0.0469] | ✓ |

## Per-class F1 on APTOS (§4.3)

| Arm | DR0 | DR1 | DR2 | DR3 | DR4 | macro-F1 |
|-----|----:|----:|----:|----:|----:|---------:|
| C | 0.8554 | 0.1375 | 0.5736 | 0.2443 | 0.5092 | 0.4640 |
| D | **0.9147** | **0.2710** | **0.6920** | **0.3239** | **0.6275** | **0.5658** |

The pipeline wins **on all five grades**; the largest relative gains are DR1 (×1.97) and DR3 (×1.33).

## Confusion matrices — APTOS, n = 3 662 (§4.4)

Class sizes: DR0 1 805 · DR1 370 · DR2 999 · DR3 193 · DR4 295.

**Config C (baseline)**

| true \ pred | DR0 | DR1 | DR2 | DR3 | DR4 |
|------------|----:|----:|----:|----:|----:|
| DR0 | 1570 | 186 | 39 | 8 | 2 |
| DR1 | 183 | 62 | 99 | 21 | 5 |
| DR2 | 96 | 245 | 499 | 131 | 28 |
| DR3 | 10 | 24 | 62 | 64 | 33 |
| DR4 | 7 | 15 | 42 | 107 | 124 |

**Config D (full pipeline)**

| true \ pred | DR0 | DR1 | DR2 | DR3 | DR4 |
|------------|----:|----:|----:|----:|----:|
| DR0 | 1679 | 111 | 13 | 2 | 0 |
| DR1 | 149 | 108 | 99 | 12 | 2 |
| DR2 | 35 | 193 | 628 | 128 | 15 |
| DR3 | 2 | 11 | 56 | 86 | 38 |
| DR4 | 1 | 4 | 20 | 110 | 160 |

## Referable DR on APTOS (§4.5)

| Arm | Sensitivity | Specificity | PPV | NPV | Referable AUC |
|-----|------------:|------------:|----:|----:|--------------:|
| C | 0.7330 | 0.9200 | 0.8623 | 0.8344 | 0.8902 |
| D | **0.8346** | **0.9411** | **0.9065** | **0.8927** | **0.9338** |

## Verdict: `h4_supported = true`

Both parts of the hypothesis are met:

1. **The threshold is cleared.** G_D = 0.8966 ≥ 0.85, with a margin of 0.047.
2. **The pipeline transfers better than baseline.** G_D 0.8966 against G_C 0.8569; the absolute APTOS
   wF1 is higher by +0.0887 (CI [+0.0572, +0.1088]).

An important nuance: **the baseline also clears the threshold** (G_C = 0.8569). That is, the "G ≥ 0.85"
part of H-4 does not discriminate between the arms — what discriminates them is the "better than
baseline" part, and that is met convincingly. This is worth stating when writing the text: the
pipeline does not rescue transfer, it improves transfer that is already acceptable.

Mechanism: the pipeline holds on to the **intermediate grades**. Class DR2 — F1 0.5736 → 0.6920; in
the confusion matrix the mass of DR2 → DR1 falls from 245 to 193 instances, and DR2 → DR0 from 96 to
35. Errors remain adjacent on the scale, which is what explains the large κ gain (0.7865 → 0.8834).

Binary "refer / do not refer" triage transfers well for both arms (referable AUC 0.890 and 0.934),
but the pipeline's sensitivity is higher by +10.2 pp with simultaneously higher specificity.

## Caveats

- Evaluation uses **fold 0** checkpoints; there is no between-fold variance for this experiment, so
  the 95% CIs of the differences are per-instance (bootstrap), not per-fold.
- G is computed relative to each arm's own in-domain wF1 (C: 0.7538, D: 0.8193), so the arm with the
  higher in-domain score has the larger denominator — the gain in G (+0.040) is by construction more
  conservative than the gain in absolute APTOS wF1 (+0.089).

APTOS clinical metrics in consolidated form — `TAB-5.4_clinical_referable.md`.
Domain distances (MMD/KL) — `H-3_domain_distance.md`.
