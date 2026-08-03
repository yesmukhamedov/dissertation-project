# exp1 in-domain clinical metrics (referable ≥ 2)

Referable DR = grade ≥ 2 (moderate NPDR and worse). EyePACS-val, n = 35 126.
Source: the **2026-08-03** run (`VALUES.md` §1.8).

| Config | Sensitivity | Specificity | PPV | NPV | Referable AUC |
|---|---|---|---|---|---|
| A | 0.6865 | 0.9438 | 0.7482 | 0.9252 | 0.8710 |
| B | **0.7982** | **0.9628** | **0.8392** | **0.9515** | **0.9120** |
| C | 0.6891 | 0.9455 | 0.7545 | 0.9259 | 0.8680 |
| D | **0.8007** | **0.9636** | **0.8427** | **0.9521** | **0.9100** |

**Observation (clinically the key one).** The pipeline raises sensitivity to vision-threatening DR by
**+11.2 pp** (A→B 0.6865 → 0.7982) and **+11.2 pp** (C→D 0.6891 → 0.8007) — and it does so **not at
the expense of specificity**: Spec rises at the same time (0.944 → 0.963 and 0.946 → 0.964). This is
not a shift of the operating point along the curve, but a shift of the curve itself: referable AUC
+0.041 / +0.042.

PPV rises by ~9 pp (0.748 → 0.839; 0.755 → 0.843) and NPV by ~2.6 pp. For a screening scenario this
means a simultaneous reduction in both missed cases and false referrals.

The referable-AUC gain is statistically significant (DeLong p = 0.0041 / 0.0028) — see `TAB-5.1_statistical.md`.
External counterparts of these metrics: APTOS — `TAB-5.4_clinical_referable.md`; the camera groups
are covered there as well.
