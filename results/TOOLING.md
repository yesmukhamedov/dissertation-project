# TOOLING — инструментарий для таблиц/рисунков/статистики

Что переиспользовать при сборке результатных материалов диссертации, и где пробелы.
Состояние — после прогона **2026-08-02**.

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

1. 🔴 **Артефакты прогона 2026-08-02 не выложены** в `experiments/outputs/` — все скрипты ниже
   читают оттуда и сейчас вернут числа **предыдущего** прогона. Закрыть первым делом
   (пункт NEW-1 в `GAP_ANALYSIS.md`), иначе любая перекрёстная проверка вводит в заблуждение.
2. **Мост outputs→рисунки** — нет скрипта, который читает `experiments/outputs/exp*/{summary.json,
   *_results.json, metrics.csv}` и рисует публикационные фигуры. Построить (переиспользуя палитру),
   чтобы убрать ручную транскрипцию как класс.
3. **`predictions.npz` нового прогона** — нужен для ROC/PR-кривых и confusion-матриц
   (`fig7_pr_curves.py` его требует). Источник: `infer_dataset` на лучших чекпойнтах;
   процедура — `CATEGORY_B_RUNBOOK.md`.
4. **Матрицы ошибок по группам камер (exp6)** — в данных прогона зафиксированы только per-class F1;
   нужна доп. выгрузка для App F (пункт R3).
5. **Не реализовано в коде:** σ-свип flat-field теперь прогнан, но функции Part C в
   `src/experiments/exp2_ablation.py` по-прежнему нет — если понадобится воспроизвести, писать
   код; **VVI** отсутствует в `src/utils/image_quality.py`; **переключателя FOV-маски** нет в
   `PreprocessingConfig` (блокирует изоляцию Stage 3, пункт G-8); **ветки clinical** нет в
   `exp4_explainability.py` (блокирует G-3).
6. **GOST-таблицы** — `generate_report.py` даёт только Markdown; для .docx/.pdf есть навык
   `council-docs` / `md2gost.py` (`.claude/skills/council-docs/`) как целевой конвертер.

## Что уже посчитано (код применён, результаты в `results/tables/`)

- `statistical_tests.py` — bootstrap CI, DeLong, McNemar, **Holm-поправка**, **смешанная ANOVA**
  → `TAB-5.1_statistical.md`.
- `calibration.py` — ECE/Brier → `TAB-4.3_exp1_calibration.md`.
- `metrics.py` — per-class, confusion, клинические метрики → `exp1_per_class.md`,
  `exp1_clinical_indomain.md`, `TAB-5.4_clinical_referable.md`.
- `image_quality.py` — CNR/Entropy/SSIM по уровням аблации → `TAB-4.5_exp2_image_quality.md`.

## Форматы и расположение выходов

- Пофолдовые метрики → CSV: `outputs/exp{1..7}/metrics.csv` (колонки: `epoch,fold,config,
  train_loss,val_loss,weighted_f1,roc_auc,kappa,accuracy`). exp2 также `metrics_clahe_sweep.csv`;
  exp4 также `metrics_baseline.csv`, `metrics_full_pipeline.csv`.
- Агрегаты → JSON: `outputs/exp1/summary.json`, `exp3/transferability_results.json`,
  `exp5/clinical_degradation_results.json`, `exp6/device_shift_results.json`,
  `exp7/small_data_results.json`. SSL: `outputs/ssl*/**/gate_report*.json`, `ssl/COMPARISON.txt`.
- Исходники экспериментов: `experiments/src/experiments/exp{1..7}_*.py`.
