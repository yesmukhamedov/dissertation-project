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
| C — baseline (3ch) | 0.7337 | 0.9209 | 0.8638 | 0.8349 | 0.8944 |
| D — full pipeline (4ch) | **0.8393** | **0.9411** | **0.9070** | **0.8955** | **0.9346** |

**Observation.** The same picture as in-domain: +10.6 pp Sens at +2.0 pp Spec. Binary "refer / do not
refer" triage transfers to APTOS for both arms (AUC 0.89 and 0.93), but the pipeline gives a
clinically more favourable operating point.

## Device shift — by camera group (exp6)

| Camera group | Sens (C) | Spec (C) | PPV (C) | NPV (C) | Sens (D) | Spec (D) | PPV (D) | NPV (D) |
|--------------|---------:|---------:|--------:|--------:|---------:|---------:|--------:|--------:|
| kowa_idrid | 0.7016 | 0.9189 | 0.8816 | 0.7816 | **0.8115** | **0.9414** | **0.9226** | **0.8531** |
| mixed_ddr | 0.7313 | 0.9279 | 0.8993 | 0.7968 | **0.8292** | **0.9483** | **0.9339** | **0.8631** |
| mixed_odir5k | 0.6682 | 0.8980 | 0.8497 | 0.7583 | **0.8023** | **0.9314** | **0.9098** | **0.8452** |
| topcon_messidor2 | 0.7476 | 0.9307 | 0.9055 | 0.8060 | **0.8354** | **0.9502** | **0.9371** | **0.8667** |
| mixed_rfmid | 0.6512 | 0.8820 | 0.8305 | 0.7401 | **0.7940** | **0.9233** | **0.9019** | **0.8347** |

Referable AUC for the same groups — `TAB-4.9_exp6_device.md` §6.4 (C 0.855–0.906, D 0.930–0.946).

**Observation.** The pipeline improves **all four** clinical quantities in **all five** camera groups,
without a single exception. The sensitivity range narrows from 0.651–0.748 (span 0.096) to
0.794–0.835 (span 0.041): the operating point becomes not only better but also **more stable across
devices** — the same contraction of spread that is visible in wF1 and AUC in `TAB-4.9`.

## Summary across the three scenarios

| Scenario | Sens (baseline) | Sens (pipeline) | ΔSens | Spec (baseline) | Spec (pipeline) |
|----------|----------------:|----------------:|------:|----------------:|----------------:|
| In-domain EyePACS (C→D) | 0.6891 | 0.8007 | +0.1116 | 0.9455 | 0.9636 |
| APTOS zero-shot (C→D) | 0.7337 | 0.8393 | +0.1056 | 0.9209 | 0.9411 |
| Camera groups (mean) | 0.7000 | 0.8145 | +0.1145 | 0.9115 | 0.9389 |

The sensitivity gain is practically constant (+0.10…+0.11) across all three scenarios — in-domain,
zero-shot to another set, and device change. This is the most reproducible clinical effect of the
pipeline across the entire experiment suite.

> **NC-14 / INVARIANTS:** the values presented are operating characteristics of the model on
> annotated datasets, not indicators of clinical validation. Statements of the form "the system is
> suitable for screening" do not follow from them.
