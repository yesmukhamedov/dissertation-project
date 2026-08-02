# TAB-5.4 — Clinical screening metrics (referable DR, grade ≥ 2)

Referable DR = the grade ≥ 2 threshold (moderate NPDR and worse). Sens/Spec/PPV/NPV + binary ROC-AUC.
Source: the **2026-08-02** run (`VALUES.md` §1.8, §4.5, §6.5).

## In-domain — EyePACS, n = 35 126 (exp1)

| Config | Sensitivity | Specificity | PPV | NPV | Referable ROC-AUC |
|--------|------------:|------------:|----:|----:|------------------:|
| A — baseline + ResNet-50 | 0.6865 | 0.9438 | 0.7482 | 0.9252 | 0.8710 |
| B — pipeline + ResNet-50 | **0.7982** | **0.9628** | **0.8392** | **0.9515** | **0.9120** |
| C — baseline + EffNet-B3 | 0.6891 | 0.9455 | 0.7545 | 0.9259 | 0.8680 |
| D — pipeline + EffNet-B3 | **0.8007** | **0.9636** | **0.8427** | **0.9521** | **0.9100** |

**Observation.** The pipeline raises sensitivity by +11.2 pp with a **simultaneous** rise in
specificity (+1.9 pp) — the curve itself shifts, not the operating point on it (referable AUC
+0.041 / +0.042, DeLong p = 0.0041 / 0.0028).

## External transfer — APTOS 2019, n = 3 662 (exp3)

| Arm | Sensitivity | Specificity | PPV | NPV | Referable ROC-AUC |
|-----|------------:|------------:|----:|----:|------------------:|
| C — baseline (3ch) | 0.7330 | 0.9209 | 0.8637 | 0.8346 | 0.8930 |
| D — full pipeline (4ch) | **0.8366** | **0.9411** | **0.9067** | **0.8939** | **0.9340** |

**Observation.** The same picture as in-domain: +10.4 pp Sens at +2.0 pp Spec. Binary "refer / do not
refer" triage transfers to APTOS for both arms (AUC 0.89 and 0.93), but the pipeline gives a
clinically more favourable operating point.

## Device shift — by camera group (exp6)

| Camera group | Sens (C) | Spec (C) | PPV (C) | NPV (C) | Sens (D) | Spec (D) | PPV (D) | NPV (D) |
|--------------|---------:|---------:|--------:|--------:|---------:|---------:|--------:|--------:|
| kowa_idrid | 0.7120 | 0.9180 | 0.8940 | 0.7640 | **0.8140** | **0.9430** | **0.9290** | **0.8420** |
| mixed_ddr | 0.7340 | 0.9260 | 0.9020 | 0.7810 | **0.8290** | **0.9480** | **0.9330** | **0.8560** |
| mixed_odir5k | 0.6710 | 0.8940 | 0.8580 | 0.7280 | **0.7980** | **0.9310** | **0.9110** | **0.8290** |
| topcon_messidor2 | 0.7480 | 0.9310 | 0.9080 | 0.7930 | **0.8360** | **0.9510** | **0.9360** | **0.8630** |
| mixed_rfmid | 0.6540 | 0.8870 | 0.8490 | 0.7150 | **0.7910** | **0.9280** | **0.9070** | **0.8230** |

Referable AUC for the same groups — `TAB-4.9_exp6_device.md` §6.4 (C 0.853–0.908, D 0.914–0.942).

**Observation.** The pipeline improves **all four** clinical quantities in **all five** camera groups,
without a single exception. The sensitivity range narrows from 0.654–0.748 (span 0.094) to
0.791–0.836 (span 0.045): the operating point becomes not only better but also **more stable across
devices** — the same contraction of spread that is visible in wF1 and AUC in `TAB-4.9`.

## Summary across the three scenarios

| Scenario | Sens (baseline) | Sens (pipeline) | ΔSens | Spec (baseline) | Spec (pipeline) |
|----------|----------------:|----------------:|------:|----------------:|----------------:|
| In-domain EyePACS (C→D) | 0.6891 | 0.8007 | +0.1116 | 0.9455 | 0.9636 |
| APTOS zero-shot (C→D) | 0.7330 | 0.8366 | +0.1036 | 0.9209 | 0.9411 |
| Camera groups (mean) | 0.7038 | 0.8136 | +0.1098 | 0.9112 | 0.9402 |

The sensitivity gain is practically constant (+0.10…+0.11) across all three scenarios — in-domain,
zero-shot to another set, and device change. This is the most reproducible clinical effect of the
pipeline across the entire experiment suite.

> **NC-14 / INVARIANTS:** the values presented are operating characteristics of the model on
> annotated datasets, not indicators of clinical validation. Statements of the form "the system is
> suitable for screening" do not follow from them.
