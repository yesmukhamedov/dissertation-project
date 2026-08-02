# TAB-4.2 — Experiment 1: 2×2 Factorial Diagnostic Metrics (H-1)

EyePACS 100%, 5-fold patient-level CV. Mean ± std. Источник: `data/exp1_summary.json`.

| Config | Arm | Backbone | Weighted F1 | ROC-AUC (macro-OvR) | Cohen κ (quadratic) | Accuracy |
|--------|-----|----------|-------------|---------------------|---------------------|----------|
| A | Baseline (3ch) | ResNet-50 | 0.7769 ± 0.0181 | 0.8429 ± 0.0097 | 0.6992 ± 0.0032 | 0.7835 ± 0.0341 |
| B | Pipeline (4ch) | ResNet-50 | 0.7810 ± 0.0232 | 0.8801 ± 0.0123 | 0.7523 ± 0.0270 | 0.7706 ± 0.0399 |
| C | Baseline (3ch) | EfficientNet-B3 | 0.7754 ± 0.0070 | 0.8337 ± 0.0192 | 0.7074 ± 0.0206 | 0.7789 ± 0.0157 |
| D | Pipeline (4ch) | EfficientNet-B3 | 0.7702 ± 0.0159 | 0.8783 ± 0.0084 | 0.7396 ± 0.0228 | 0.7530 ± 0.0284 |

## TAB-4.3 — Dominance Assessment (EH-3)

Критерий доминирования (все три обязательны): ΔF1 ≥ 5пп · ΔAUC ≥ 0.02 · Δκ ≥ 0 (без деградации).

| Comparison | ΔF1 (пп) | ΔAUC | Δκ | F1 crit | AUC crit | κ crit | **Dominant** |
|------------|----------|------|-----|---------|----------|--------|--------------|
| B vs A (pipeline effect, ResNet-50) | +0.41 | +0.0372 | +0.0531 | ✗ | ✓ | ✓ | **NO** |
| D vs C (pipeline effect, EfficientNet-B3) | −0.51 | +0.0446 | +0.0322 | ✗ | ✓ | ✓ | **NO** |

**Verdict:** `h1_supported = false`. Конвейер последовательно повышает AUC и κ на обоих
бэкбонах, но не достигает 5-пунктового порога доминирования по F1.

> Оговорка CFC-2.8: интегрированный арм (B/D) инициализируется continual-SSL, поэтому эффект
> «препроцессинг × инициализация» связан — H-1 не изолирует один только препроцессинг.
