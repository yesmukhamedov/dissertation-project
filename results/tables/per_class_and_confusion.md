# Per-class F1 + confusion matrices (external sets)

ICDR classes: DR0 = no DR, DR1 = mild NPDR, DR2 = moderate NPDR, DR3 = severe NPDR, DR4 = PDR.
Source: the **2026-08-02** run (`VALUES.md` §4.3–4.4, §6.6–6.7).
Per-class figures for EyePACS (exp1) are in `exp1_per_class.md`.

## exp3 — APTOS 2019, n = 3 662

| Arm | DR0 | DR1 | DR2 | DR3 | DR4 | macro-F1 |
|-----|----:|----:|----:|----:|----:|---------:|
| C — baseline | 0.8554 | 0.1394 | 0.5747 | 0.2443 | 0.5113 | 0.4650 |
| D — full pipeline | **0.9150** | **0.2717** | **0.6931** | **0.3271** | **0.6287** | **0.5671** |

The pipeline wins on all five grades; macro-F1 +0.102 against wF1 +0.089 — the gain is
disproportionately larger on the minority classes.

### Confusion matrix — Config C (APTOS), rows = truth, columns = prediction

| true \ pred | DR0 | DR1 | DR2 | DR3 | DR4 |
|------------|----:|----:|----:|----:|----:|
| DR0 | 1570 | 186 | 39 | 8 | 2 |
| DR1 | 184 | 63 | 98 | 21 | 4 |
| DR2 | 96 | 245 | 500 | 131 | 27 |
| DR3 | 10 | 24 | 62 | 64 | 33 |
| DR4 | 6 | 16 | 42 | 107 | 124 |

### Confusion matrix — Config D (APTOS)

| true \ pred | DR0 | DR1 | DR2 | DR3 | DR4 |
|------------|----:|----:|----:|----:|----:|
| DR0 | 1679 | 111 | 13 | 2 | 0 |
| DR1 | 149 | 108 | 100 | 12 | 1 |
| DR2 | 34 | 192 | 630 | 128 | 15 |
| DR3 | 2 | 10 | 56 | 87 | 38 |
| DR4 | 1 | 4 | 20 | 110 | 160 |

**Observation.** The diagonal grows at every grade (e.g. DR2: 500 → 630, DR1: 63 → 108). Distant
errors almost disappear: the DR0 → DR4 cell is 2 for C and 0 for D; DR0 → DR3 goes 8 → 2. The
residual error mass concentrates in the adjacent DR3↔DR4 cells (110 instances for D) — the "severe
NPDR / PDR" boundary remains the hardest.

## exp6 — per-class F1 by camera group

**Config C (baseline)**

| Group | DR0 | DR1 | DR2 | DR3 | DR4 | macro-F1 |
|--------|----:|----:|----:|----:|----:|---------:|
| kowa_idrid | 0.8230 | 0.2140 | 0.5432 | 0.3457 | 0.4526 | 0.4757 |
| mixed_ddr | 0.8468 | 0.2202 | 0.5589 | 0.3557 | 0.4658 | 0.4895 |
| mixed_odir5k | 0.7792 | 0.2026 | 0.5142 | 0.3272 | 0.4285 | 0.4504 |
| topcon_messidor2 | 0.8632 | 0.2244 | 0.5697 | 0.3625 | 0.4748 | 0.4989 |
| mixed_rfmid | 0.7569 | 0.1968 | 0.4996 | 0.3179 | 0.4163 | 0.4375 |

**Config D (full pipeline)**

| Group | DR0 | DR1 | DR2 | DR3 | DR4 | macro-F1 |
|--------|----:|----:|----:|----:|----:|---------:|
| kowa_idrid | 0.8615 | 0.2929 | 0.6375 | 0.4480 | 0.5427 | 0.5565 |
| mixed_ddr | 0.8672 | 0.2949 | 0.6417 | 0.4510 | 0.5464 | 0.5602 |
| mixed_odir5k | 0.8443 | 0.2871 | 0.6248 | 0.4390 | 0.5319 | 0.5454 |
| topcon_messidor2 | 0.8749 | 0.2975 | 0.6474 | 0.4549 | 0.5512 | 0.5652 |
| mixed_rfmid | 0.8347 | 0.2838 | 0.6177 | 0.4341 | 0.5259 | 0.5392 |

Class sizes by group (DR0…DR4):
kowa_idrid 168 / 54 / 131 / 34 / 26 · mixed_ddr 496 / 142 / 378 / 104 / 80 ·
mixed_odir5k 402 / 108 / 290 / 88 / 62 · topcon_messidor2 723 / 201 / 548 / 152 / 120 ·
mixed_rfmid 268 / 71 / 197 / 60 / 44.

## Observations by group

- **The pipeline wins in all 25 cells** (5 groups × 5 classes) — there are no exceptions.
  macro-F1 rises by +0.081…+0.102 across the groups.
- **The between-group spread contracts on every class.** DR0: for C the span is 0.7569–0.8632 (0.106),
  for D it is 0.8347–0.8749 (0.040). DR2: 0.4996–0.5697 (0.070) → 0.6177–0.6474 (0.030).
  This is the same device-levelling effect visible in wF1 in `TAB-4.9_exp6_device.md`.
- **The difficulty ordering of the classes is the same for both arms and in every group:**
  DR0 ≫ DR2 > DR4 > DR3 ≫ DR1. Mild NPDR remains the hardest class everywhere (F1 ≈ 0.20 for C,
  ≈ 0.29 for D) — early, subtle signs are not solved by preprocessing, only mitigated.
- **The ordering of the groups by quality is preserved as well:** the best is topcon_messidor2 and
  the worst is mixed_rfmid, for both arms. The residual difference between sets is not eliminated by
  the pipeline (consistent with `H-3_domain_distance.md`: the ranking of domains by MMD is preserved).

> Confusion matrices by camera group are not recorded in the run's source data — only per-class F1 is
> given. If they are needed for App F, an additional export will be required.
