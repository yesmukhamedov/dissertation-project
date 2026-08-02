# TAB-4.8 — Experiment 5: Clinical Degradation Resistance (H-7)

Метрика: `delta_f1 = F1_EyePACS_val − F1_external` (меньше = устойчивее). EfficientNet-B3.
In-domain: full 0.7952, baseline 0.7819. Источник: `data/exp5_clinical_degradation_results.json`.

| Dataset | n | F1_full | F1_base | Δ_full | Δ_baseline | diff (full−base) | 95% CI | p (1-sided) | Supported |
|---------|---|---------|---------|--------|-----------|------------------|--------|-------------|-----------|
| IDRiD | 413 | 0.5388 | 0.6154 | 0.2564 | 0.1665 | **−0.0897** | [−0.160, −0.017] | 0.99 | ✗ |
| Messidor-2 | 1744 | 0.6920 | 0.6781 | 0.1032 | 0.1038 | +0.0010 | [−0.027, +0.028] | 0.482 | ✗ |

**Verdict:** `h7_supported = false`. Гипотеза о большей устойчивости full-конвейера не
подтверждена: на IDRiD full деградирует статистически значимо БОЛЬШЕ (diff −0.090, CI не
включает 0), на Messidor-2 армы неотличимы (diff ≈ 0, p 0.48).
