# Per-class F1 + confusion matrices (external sets)

ICDR classes: DR0 = no DR, DR1 = mild NPDR, DR2 = moderate NPDR, DR3 = severe NPDR, DR4 = PDR.
Source: the **2026-08-03** run (`VALUES.md` §4.3–4.4, §6.6–6.7).
Per-class figures for EyePACS (exp1) are in `exp1_per_class.md`.

## exp3 — APTOS 2019, n = 3 662

| Arm | DR0 | DR1 | DR2 | DR3 | DR4 | macro-F1 |
|-----|----:|----:|----:|----:|----:|---------:|
| C — baseline | 0.8554 | 0.1375 | 0.5736 | 0.2443 | 0.5092 | 0.4640 |
| D — full pipeline | **0.9147** | **0.2710** | **0.6920** | **0.3239** | **0.6275** | **0.5658** |

The pipeline wins on all five grades; macro-F1 +0.102 against wF1 +0.089 — the gain is
disproportionately larger on the minority classes.

### Confusion matrix — Config C (APTOS), rows = truth, columns = prediction

| true \ pred | DR0 | DR1 | DR2 | DR3 | DR4 |
|------------|----:|----:|----:|----:|----:|
| DR0 | 1570 | 186 | 39 | 8 | 2 |
| DR1 | 183 | 62 | 99 | 21 | 5 |
| DR2 | 96 | 245 | 499 | 131 | 28 |
| DR3 | 10 | 24 | 62 | 64 | 33 |
| DR4 | 7 | 15 | 42 | 107 | 124 |

### Confusion matrix — Config D (APTOS)

| true \ pred | DR0 | DR1 | DR2 | DR3 | DR4 |
|------------|----:|----:|----:|----:|----:|
| DR0 | 1679 | 111 | 13 | 2 | 0 |
| DR1 | 149 | 108 | 99 | 12 | 2 |
| DR2 | 35 | 193 | 628 | 128 | 15 |
| DR3 | 2 | 11 | 56 | 86 | 38 |
| DR4 | 1 | 4 | 20 | 110 | 160 |

**Observation.** The diagonal grows at every grade (e.g. DR2: 499 → 628, DR1: 62 → 108). Distant
errors almost disappear: the DR0 → DR4 cell is 2 for C and 0 for D; DR0 → DR3 goes 8 → 2. The
residual error mass concentrates in the adjacent DR3↔DR4 cells (110 instances for D) — the "severe
NPDR / PDR" boundary remains the hardest.

## exp6 — per-class F1 by camera group

**Config C (baseline)**

| Group | DR0 | DR1 | DR2 | DR3 | DR4 | macro-F1 |
|--------|----:|----:|----:|----:|----:|---------:|
| kowa_idrid | 0.8025 | 0.2214 | 0.5556 | 0.3423 | 0.4998 | 0.4843 |
| mixed_ddr | 0.8269 | 0.2212 | 0.5725 | 0.3322 | 0.5100 | 0.4926 |
| mixed_odir5k | 0.7872 | 0.2070 | 0.5205 | 0.3223 | 0.4214 | 0.4517 |
| topcon_messidor2 | 0.8570 | 0.2361 | 0.5744 | 0.3335 | 0.5220 | 0.5046 |
| mixed_rfmid | 0.7671 | 0.1934 | 0.4918 | 0.3020 | 0.4657 | 0.4440 |

**Config D (full pipeline)**

| Group | DR0 | DR1 | DR2 | DR3 | DR4 | macro-F1 |
|--------|----:|----:|----:|----:|----:|---------:|
| kowa_idrid | 0.8451 | 0.2946 | 0.6530 | 0.4296 | 0.5799 | 0.5604 |
| mixed_ddr | 0.8508 | 0.2889 | 0.6471 | 0.4561 | 0.6007 | 0.5687 |
| mixed_odir5k | 0.8482 | 0.2827 | 0.6234 | 0.4271 | 0.5445 | 0.5452 |
| topcon_messidor2 | 0.9080 | 0.2776 | 0.6256 | 0.4448 | 0.5843 | 0.5681 |
| mixed_rfmid | 0.8188 | 0.2851 | 0.6190 | 0.4290 | 0.5660 | 0.5436 |

Class sizes by group (DR0…DR4):
kowa_idrid 168 / 54 / 131 / 34 / 26 · mixed_ddr 496 / 142 / 378 / 104 / 80 ·
mixed_odir5k 402 / 108 / 290 / 88 / 62 · topcon_messidor2 723 / 201 / 548 / 152 / 120 ·
mixed_rfmid 268 / 71 / 197 / 60 / 44.

## Observations by group

- **The pipeline wins in all 25 cells** (5 groups × 5 classes) — there are no exceptions.
  macro-F1 rises by +0.064…+0.100 across the groups.
- **The between-group spread contracts on four of the five classes.** DR2: for C the span is
  0.4918–0.5744 (0.083), for D 0.6190–0.6530 (0.034). DR4: 0.4214–0.5220 (0.101) → 0.5445–0.6007
  (0.056). DR1 and DR3 contract similarly. **DR0 is the exception** — the span barely moves
  (0.7671–0.8570, 0.090 → 0.8188–0.9080, 0.089), because topcon_messidor2 gains disproportionately on
  that class (0.8570 → 0.9080). The levelling effect visible in wF1 in `TAB-4.9_exp6_device.md`
  therefore comes from the pathological grades, not from the negative class.
- **The difficulty ordering of the classes is the same for both arms and in every group:**
  DR0 ≫ DR2 > DR4 > DR3 ≫ DR1. Mild NPDR remains the hardest class everywhere (F1 ≈ 0.19–0.24 for C,
  ≈ 0.28–0.29 for D) — early, subtle signs are not solved by preprocessing, only mitigated.
- **The ordering of the groups by weighted-F1 is preserved as well:** the best is topcon_messidor2 and
  the worst is mixed_rfmid, for both arms. (By macro-F1 the top position changes hands under D —
  mixed_ddr 0.5687 against topcon_messidor2 0.5681 — a difference far inside noise.) The residual
  difference between sets is not eliminated by the pipeline (consistent with
  `H-3_domain_distance.md`: the ranking of domains by MMD is preserved).

> Confusion matrices by camera group are not recorded in the run's source data — only per-class F1 is
> given. If they are needed for App F, an additional export will be required.
