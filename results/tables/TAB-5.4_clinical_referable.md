# TAB-5.4 — Clinical screening metrics (referable DR, grade ≥ 2)

Referable DR = the grade ≥ 2 threshold (moderate NPDR and worse). Sens/Spec/PPV/NPV + binary ROC-AUC.
Source: the **2026-08-03** run (`VALUES.md` §1.8, §4.5, §6.5).

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
| C — baseline (3ch) | 0.7330 | 0.9200 | 0.8623 | 0.8344 | 0.8902 |
| D — full pipeline (4ch) | **0.8346** | **0.9411** | **0.9065** | **0.8927** | **0.9338** |

**Observation.** The same picture as in-domain: +10.2 pp Sens at +2.1 pp Spec. Binary "refer / do not
refer" triage transfers to APTOS for both arms (AUC 0.89 and 0.93), but the pipeline gives a
clinically more favourable operating point.

## Device shift — by camera group (exp6)

| Camera group | Sens (C) | Spec (C) | PPV (C) | NPV (C) | Sens (D) | Spec (D) | PPV (D) | NPV (D) |
|--------------|---------:|---------:|--------:|--------:|---------:|---------:|--------:|--------:|
| kowa_idrid | 0.7120 | 0.9099 | 0.8718 | 0.7860 | **0.8168** | **0.9414** | **0.9231** | **0.8566** |
| mixed_ddr | 0.7313 | 0.9232 | 0.8935 | 0.7959 | **0.8256** | **0.9483** | **0.9336** | **0.8606** |
| mixed_odir5k | 0.6727 | 0.8941 | 0.8457 | 0.7600 | **0.7932** | **0.9353** | **0.9136** | **0.8398** |
| topcon_messidor2 | 0.7500 | 0.9318 | 0.9071 | 0.8077 | **0.8341** | **0.9491** | **0.9357** | **0.8657** |
| mixed_rfmid | 0.6545 | 0.8909 | 0.8419 | 0.7438 | **0.7940** | **0.9233** | **0.9019** | **0.8347** |

Referable AUC for the same groups — `TAB-4.9_exp6_device.md` §6.4 (C 0.851–0.910, D 0.910–0.946).

**Observation.** The pipeline improves **all four** clinical quantities in **all five** camera groups,
without a single exception. The sensitivity range narrows from 0.655–0.750 (span 0.096) to
0.793–0.834 (span 0.041): the operating point becomes not only better but also **more stable across
devices** — the same contraction of spread that is visible in wF1 and AUC in `TAB-4.9`.

## Summary across the three scenarios

| Scenario | Sens (baseline) | Sens (pipeline) | ΔSens | Spec (baseline) | Spec (pipeline) |
|----------|----------------:|----------------:|------:|----------------:|----------------:|
| In-domain EyePACS (C→D) | 0.6891 | 0.8007 | +0.1116 | 0.9455 | 0.9636 |
| APTOS zero-shot (C→D) | 0.7330 | 0.8346 | +0.1016 | 0.9200 | 0.9411 |
| Camera groups (mean) | 0.7041 | 0.8127 | +0.1086 | 0.9100 | 0.9395 |

The sensitivity gain is practically constant (+0.10…+0.11) across all three scenarios — in-domain,
zero-shot to another set, and device change. This is the most reproducible clinical effect of the
pipeline across the entire experiment suite.

> **NC-14 / INVARIANTS:** the values presented are operating characteristics of the model on
> annotated datasets, not indicators of clinical validation. Statements of the form "the system is
> suitable for screening" do not follow from them.
