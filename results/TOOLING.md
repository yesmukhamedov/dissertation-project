# TOOLING — инструментарий для таблиц/рисунков/статистики

Что переиспользовать при сборке результатных материалов диссертации, и где пробелы.

## Переиспользовать как есть

| Модуль | Что даёт |
|--------|----------|
| `experiments/src/evaluation/metrics.py` | `compute_primary_metrics` (weighted_f1, roc_auc macro-OvR robust к отсутствующим классам, cohen_kappa_quadratic, accuracy); `compute_secondary_metrics` (per-class f1/prec/recall, macro_f1, confusion_matrix); `compute_clinical_metrics` (sensitivity/specificity/ppv/npv, referable≥2); `check_dominance` (EH-3: ΔF1≥0.05, ΔAUC≥0.02, Δκ≥0); `check_overfitting`. |
| `experiments/src/evaluation/statistical_tests.py` | `mcnemar_test`, `delong_test` (полная DeLong-дисперсия для сравнения AUC), `bootstrap_ci` / `bootstrap_ci_all_primary` (95% CI, 1000 итер.), `holm_bonferroni_correction`, `compute_mixed_effects_summary`. |
| `experiments/src/evaluation/calibration.py` | ECE, Brier score. |
| `experiments/src/explainability/visualization.py` | `overlay_gradcam`, `create_comparison_figure` — реальный рендер Grad-CAM (для exp4). |
| `experiments/src/experiments/_eval_utils.py` | `evaluate_dataset`, `infer_dataset` (сырые y_true/y_pred/y_prob для парных тестов), `evaluate_dataset_binary` (RFMiD). |

## Скрипты-агрегаторы

- `experiments/scripts/generate_report.py` — JSON→Markdown таблицы гипотез/claim'ов →
  `outputs/final_report.md`. **Есть рассинхрон имён файлов:** скрипт ждёт
  `degradation_results.json` / `generalization_results.json` / `iou_results.json` /
  `ablation_summary.json`, а на диске — `transferability_results.json` /
  `clinical_degradation_results.json` / `device_shift_results.json` / `small_data_results.json`.
  → Починить маппинг имён, прежде чем запускать как перекрёстную проверку `results/tables/`.
- `experiments/scripts/verify_exp1.py … verify_exp5_exp6.py` — верификация прогонов.

## ⚠️ НЕ переиспользовать напрямую (заражено зашитыми числами — см. INTEGRITY_NOTE.md)

- `demo/web/generate_charts_01_14.py` / `_15_28.py` / `_29_30.py` — рисунки на константах из `data.js`.
- `defense/figures/scripts/fig9_confusion_matrix.py` — матрицы зашиты.
- Полезное из них: **палитра дома** (`BLUE #378ADD`, `TEAL #1D9E75`, `CORAL #D85A30`,
  `PURPLE #7F77DD`, `AMBER #EF9F27`, `GRAY #888780`, `GREEN #639922`, `RED #E24B4A`) — можно
  сохранить как единый стиль, перепривязав данные к `outputs/`.

## Пробелы (построить/починить)

1. **Мост outputs→рисунки** — нет скрипта, который читает `experiments/outputs/exp*/{summary.json,
   *_results.json, metrics.csv}` и рисует публикационные фигуры. Построить (переиспользуя палитру),
   чтобы убрать ручную транскрипцию как класс.
2. **`predictions.npz`** (сырые y_prob) — не сгенерирован; нужен для реальных ROC/PR-кривых и
   confusion-матриц (`fig7_pr_curves.py` его требует). Источник: `infer_dataset` на лучших чекпойнтах.
3. **Статистический слой гл.5** — bootstrap CI + DeLong + McNemar на exp1 (TAB-5.1) и классификация
   силы утверждений (TAB-5.2) ещё не посчитаны/не сведены. Код готов (`statistical_tests.py`).
4. **GOST-таблицы** — `generate_report.py` даёт только Markdown; для .docx/.pdf есть навык
   `council-docs` / `md2gost.py` (`.claude/skills/council-docs/`) как целевой конвертер.

## Форматы и расположение выходов

- Пофолдовые метрики → CSV: `outputs/exp{1..7}/metrics.csv` (колонки: `epoch,fold,config,
  train_loss,val_loss,weighted_f1,roc_auc,kappa,accuracy`). exp2 также `metrics_clahe_sweep.csv`;
  exp4 также `metrics_baseline.csv`, `metrics_full_pipeline.csv`.
- Агрегаты → JSON: `outputs/exp1/summary.json`, `exp3/transferability_results.json`,
  `exp5/clinical_degradation_results.json`, `exp6/device_shift_results.json`,
  `exp7/small_data_results.json`. SSL: `outputs/ssl*/**/gate_report*.json`, `ssl/COMPARISON.txt`.
- Исходники экспериментов: `experiments/src/experiments/exp{1..7}_*.py`.
