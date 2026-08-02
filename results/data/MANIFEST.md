# data/ MANIFEST — канонические файлы результатов

> 🔴 **ВНИМАНИЕ: файлы в этой папке относятся к ПРЕДЫДУЩЕМУ прогону (снимок 2026-07-24…28).**
> Таблицы и вердикты в `results/tables/`, `results/hypotheses/`, `results/findings/` и
> `results/STATUS.md` обновлены под прогон **2026-08-02** (источник — `VALUES.md`), а сырые
> артефакты того прогона в репозиторий ещё не выложены — ни сюда, ни в `experiments/outputs/`
> (последние файлы там от 2026-07-30).
>
> **Пока это не закрыто, JSON ниже НЕ являются подтверждением чисел из таблиц** — они дадут
> другие значения и противоположные вердикты (`h1_supported=false` и т.д.). Использовать их для
> перекрёстной проверки нельзя. Пункт **NEW-1** в `HYPOTHESIS_COVERAGE.md`.

Источник истины — всегда `experiments/outputs/`; эта папка — снимок для переносимости.

## Что нужно сделать для восстановления провенанса

1. Выложить сырые артефакты прогона 2026-08-02 в `experiments/outputs/exp{1..7}/` и
   `outputs/ssl*/` (`summary.json`, `*_results.json`, `metrics.csv`, `predictions.npz`,
   артефакты σ-свипа и двумерной сетки CLAHE, результаты MMD/KL по H-3).
2. Обновить копии в этой папке и переписать таблицу ниже.
3. Сверить числа `results/tables/` с новыми JSON и снять предупреждение выше.
4. Попутно закрывается **G-10** (проверка, что офлайн-предсказания B/D воспроизводят обучение).

## Текущее содержимое (устаревшее — прогон до 2026-07-28)

| Файл | Источник | Эксперимент | Ключевое содержимое | Статус |
|------|----------|-------------|---------------------|--------|
| `exp1_summary.json` | `outputs/exp1/summary.json` | exp1 (H-1) | 4 конфига × метрики, `dominance_tests`, `h1_supported=false` | ⚠️ устарел |
| `exp2_ablation_summary.json` | `outputs/exp2/ablation_summary.json` | exp2 (H-2) | индивидуальная аблация 6 уровней + quality; 15% / 3 фолда | ⚠️ устарел (новый прогон — 8 уровней, 100% / 5 фолдов) |
| `exp2_clahe_sweep.json` | `outputs/exp2/clahe_sweep.json` | exp2 (H-2) | одномерный свип clip на IDRiD | ⚠️ устарел (новый — двумерная сетка на EyePACS) |
| `exp3_transferability_results.json` | `outputs/exp3/transferability_results.json` | exp3 (H-4) | APTOS, `h4_supported=false` | ⚠️ устарел |
| `exp4_iou_results_maskset.json` | `outputs/exp4/iou_results_maskset.json` | exp4 (H-5) | ALO/IoU по 54 маскам, `h5_alo_supported=false` | ⚠️ устарел |
| `exp4_iou_results.json` | `outputs/exp4/iou_results.json` | exp4 (H-5) | та же метрика на n_масок = 5 (артефакт сэмплирования) | ⚠️ давно устарел |
| `exp5_clinical_degradation_results.json` | `outputs/exp5/clinical_degradation_results.json` | exp5 (H-7) | IDRiD/Messidor-2, `h7_supported=false` | ⚠️ устарел |
| `exp6_device_shift_results.json` | `outputs/exp6/device_shift_results.json` | exp6 (H-6) | 5 групп камер, `h6_supported=false`; RFMiD бинарно | ⚠️ устарел |
| `exp7_small_data_results.json` | `outputs/exp7/small_data_results.json` | exp7 | baseline/full пофолдово, `full_minus_baseline_weighted_f1=0.0899` | ⚠️ устарел |
| `ssl_COMPARISON.txt` | `outputs/ssl/COMPARISON.txt` | SSL | from-scratch probe-гейт: BYOL/MoCo-v2/DINO — все passed=False | 🟡 частично актуален (в новом прогоне добавлен SIP, passed=True) |
| `ssl_gate_continual_{resnet50,efficientnet_b3}.json` | `outputs/ssl_run_artifacts/sip/v1.0/gate_report_CONTINUAL_*.json` | SSL-continual | linear-probe гейт init B/D | ⚠️ устарел (в новом прогоне EffNet-B3 даёт выигрыш, ранее — нет) |
| `ssl_gate_run2_{resnet50,efficientnet_b3}.json` | `outputs/ssl_run_artifacts/sip/v1.0/gate_report_*.json` | SSL-continual | второй прогон probe-гейта | ⚠️ устарел |

## Чего в снимке нет вообще (новое в прогоне 2026-08-02)

- **H-3** — MMD по признакам предпоследнего слоя и KL по канальным гистограммам для 6 доменов
  (`tables/H-3_domain_distance.md`). Файла-источника нет.
- **σ-свип flat-field** — 6 точек 0.05–0.10·D + CNR (`tables/exp2_flatfield_sigma_sweep.md`).
- **Двумерная сетка CLAHE** (clip × global_threshold) и отдельные сетки F1(DR1) / F1(DR2).
- **Кумулятивная аблация 8 уровней** с пофолдовыми значениями и σ_fold.
- **Holm-поправка и смешанная ANOVA** по exp1 (`tables/TAB-5.1_statistical.md`).

## Пофолдовые CSV (не копировались — ссылки на источник)

- exp1: `experiments/outputs/exp1/metrics.csv` — история по 4 конфигам × 5 фолдов.
- exp2: `experiments/outputs/exp2/metrics.csv`, `metrics_clahe_sweep.csv`.
- exp4: `experiments/outputs/exp4/metrics_{baseline,full_pipeline}.csv`; overlays —
  `outputs/exp4/gradcam_maskset/*.png` (54 шт., все с масками).
- exp7: `experiments/outputs/exp7/metrics.csv`.
- exp3/5/6: `metrics.csv` содержат только заголовок (это eval-эксперименты).
