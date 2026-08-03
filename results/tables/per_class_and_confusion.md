# Per-class F1 + confusion matrices (external sets)

ICDR classes: DR0 = no DR, DR1 = mild NPDR, DR2 = moderate NPDR, DR3 = severe NPDR, DR4 = PDR.
Source: the **2026-08-03** run (`VALUES.md` §4.3–4.4, §6.6–6.7).
Per-class figures for EyePACS (exp1) are in `exp1_per_class.md`.

## exp3 — APTOS 2019, n = 3 662

| Arm | DR0 | DR1 | DR2 | DR3 | DR4 | macro-F1 |
|-----|----:|----:|----:|----:|----:|---------:|
| C — baseline | 0.8554 | 0.1395 | 0.5747 | 0.2438 | 0.5113 | 0.4649 |
| D — full pipeline | **0.9152** | **0.2720** | **0.6931** | **0.3252** | **0.6275** | **0.5666** |

The pipeline wins on all five grades; macro-F1 +0.102 against wF1 +0.089 — the gain is
disproportionately larger on the minority classes.

### Confusion matrix — Config C (APTOS), rows = truth, columns = prediction

| true \ pred | DR0 | DR1 | DR2 | DR3 | DR4 |
|------------|----:|----:|----:|----:|----:|
| DR0 | 1570 | 186 | 39 | 8 | 2 |
| DR1 | 184 | 63 | 98 | 21 | 4 |
| DR2 | 96 | 245 | 500 | 131 | 27 |
| DR3 | 10 | 24 | 62 | 64 | 33 |
| DR4 | 6 | 15 | 42 | 108 | 124 |

### Confusion matrix — Config D (APTOS)

| true \ pred | DR0 | DR1 | DR2 | DR3 | DR4 |
|------------|----:|----:|----:|----:|----:|
| DR0 | 1678 | 111 | 14 | 2 | 0 |
| DR1 | 150 | 108 | 99 | 12 | 1 |
| DR2 | 33 | 192 | 630 | 129 | 15 |
| DR3 | 1 | 10 | 56 | 87 | 39 |
| DR4 | 0 | 3 | 20 | 112 | 160 |

**Observation.** The diagonal grows at every grade (e.g. DR2: 500 → 630, DR1: 63 → 108). Distant
errors almost disappear: the DR0 → DR4 cell is 2 for C and 0 for D; DR0 → DR3 goes 8 → 2. The
residual error mass concentrates in the adjacent DR3↔DR4 cells (112 instances for D) — the "severe
NPDR / PDR" boundary remains the hardest.

## exp6 — per-class F1 by camera group

**Config C (baseline)**

| Group | DR0 | DR1 | DR2 | DR3 | DR4 | macro-F1 |
|--------|----:|----:|----:|----:|----:|---------:|
| kowa_idrid | 0.8294 | 0.2237 | 0.5348 | 0.3368 | 0.5031 | 0.4856 |
| mixed_ddr | 0.8502 | 0.2235 | 0.5598 | 0.3149 | 0.5083 | 0.4913 |
| mixed_odir5k | 0.7842 | 0.1940 | 0.5172 | 0.3206 | 0.4366 | 0.4505 |
| topcon_messidor2 | 0.8652 | 0.2309 | 0.5628 | 0.3266 | 0.5475 | 0.5066 |
| mixed_rfmid | 0.7356 | 0.2001 | 0.5035 | 0.2705 | 0.4771 | 0.4374 |

**Config D (full pipeline)**

| Group | DR0 | DR1 | DR2 | DR3 | DR4 | macro-F1 |
|--------|----:|----:|----:|----:|----:|---------:|
| kowa_idrid | 0.8617 | 0.2894 | 0.6259 | 0.4314 | 0.5841 | 0.5585 |
| mixed_ddr | 0.8605 | 0.2912 | 0.6393 | 0.4062 | 0.6051 | 0.5605 |
| mixed_odir5k | 0.8570 | 0.2845 | 0.6119 | 0.4470 | 0.5348 | 0.5470 |
| topcon_messidor2 | 0.8927 | 0.3037 | 0.6277 | 0.4163 | 0.6142 | 0.5709 |
| mixed_rfmid | 0.8193 | 0.2726 | 0.6245 | 0.4042 | 0.5619 | 0.5365 |

Class sizes by group (DR0…DR4):
kowa_idrid 168 / 54 / 131 / 34 / 26 · mixed_ddr 496 / 142 / 378 / 104 / 80 ·
mixed_odir5k 402 / 108 / 290 / 88 / 62 · topcon_messidor2 723 / 201 / 548 / 152 / 120 ·
mixed_rfmid 268 / 71 / 197 / 60 / 44.

## Observations by group

- **The pipeline wins in all 25 cells** (5 groups × 5 classes) — there are no exceptions.
  macro-F1 rises by +0.064…+0.099 across the groups.
- **The between-group spread contracts on every one of the five classes** (the DR0 exception seen in
  the previous revision has gone):

  | Class | C span | D span |
  |---|---:|---:|
  | DR0 | 0.1296 | **0.0734** |
  | DR1 | 0.0369 | **0.0311** |
  | DR2 | 0.0593 | **0.0274** |
  | DR3 | 0.0663 | **0.0428** |
  | DR4 | 0.1109 | **0.0794** |

  This is the same device-levelling effect visible in wF1 in `TAB-4.9_exp6_device.md`, and it now runs
  uniformly across the whole grading scale rather than only the pathological grades.
- **The difficulty ordering of the classes is the same for both arms and in every group:**
  DR0 ≫ DR2 > DR4 > DR3 ≫ DR1. Mild NPDR remains the hardest class everywhere (F1 ≈ 0.19–0.23 for C,
  ≈ 0.27–0.30 for D) — early, subtle signs are not solved by preprocessing, only mitigated.
- **The ordering of the groups by quality is preserved as well:** the best is topcon_messidor2 and
  the worst is mixed_rfmid, for both arms and on both weighted-F1 and macro-F1. The residual
  difference between sets is not eliminated by the pipeline (consistent with
  `H-3_domain_distance.md`: the ranking of domains by MMD is preserved).

> Confusion matrices by camera group are not recorded in the run's source data — only per-class F1 is
> given. If they are needed for App F, an additional export will be required.
