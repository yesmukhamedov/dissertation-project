# data/ MANIFEST — канонические файлы результатов

Копии реальных файлов результатов завершённых экспериментов, сведённые в одно место.
Источник истины — всегда `experiments/outputs/`; это снимок для переносимости (2026-07-24).

| Файл здесь | Источник | Эксперимент | Ключевое содержимое |
|------------|----------|-------------|---------------------|
| `exp1_summary.json` | `experiments/outputs/exp1/summary.json` | exp1 (H-1) | 4 конфига × метрики (mean±std), `dominance_tests`, `h1_supported=false` |
| `exp3_transferability_results.json` | `experiments/outputs/exp3/transferability_results.json` | exp3 (H-4) | full/baseline на APTOS, confusion, g_ratio, `h4_supported=false`. **Пересчитан 2026-07-28** после фикса Stage-2 (вердикт не изменился; до-фиксовая версия — `outputs/exp3/transferability_results_prefix_20260717.json`) |
| `exp5_clinical_degradation_results.json` | `experiments/outputs/exp5/clinical_degradation_results.json` | exp5 (H-7) | IDRiD/Messidor-2 delta_f1 + CI + p, `h7_supported=false` |
| `exp6_device_shift_results.json` | `experiments/outputs/exp6/device_shift_results.json` | exp6 (H-6) | 5 камер-групп, confusion, g_ratio, дисперсия, `h6_supported=false` |
| `exp7_small_data_results.json` | `experiments/outputs/exp7/small_data_results.json` | exp7 | baseline/full пофолдово + summary, `full_minus_baseline_weighted_f1=0.0899` |
| `exp2_ablation_summary.json` | `experiments/outputs/exp2/ablation_summary.json` | exp2 (H-2) | аблация все 6 уровней + quality (CNR/entropy/SSIM); 15%/3-fold. Пересобран 2026-07-28 из `metrics.csv` (`scripts/rebuild_exp2_summary.py`) после дообучения `full`/fold2; std = ddof=0 (в таблицах `results/` — ddof=1) |
| `exp2_clahe_sweep.json` | `experiments/outputs/exp2/clahe_sweep.json` | exp2 (H-2) | CLAHE-свип 7 значений на IDRiD, wF1 + dr1_f1/dr2_f1 |
| `exp4_iou_results_maskset.json` ⭐ | `experiments/outputs/exp4/iou_results_maskset.json` | exp4 (H-5) | **КАНОН (2026-07-28).** ALO/IoU по ВСЕМ 54 изображениям IDRiD с масками + парные тесты (Wilcoxon, bootstrap-CI) + свип порога бинаризации; `h5_alo_supported=false` |
| `exp4_iou_results.json` | `experiments/outputs/exp4/iou_results.json` | exp4 (H-5) | **УСТАРЕЛО** — та же метрика на n_масок=5 (артефакт сэмплирования), `h5_supported=true`. Хранится для сверки: новые числа побитово воспроизводятся на этих 5 изображениях |
| `ssl_COMPARISON.txt` | `experiments/outputs/ssl/COMPARISON.txt` | SSL | from-scratch probe-гейт: BYOL/MoCo-v2/DINO — все passed=False |
| `ssl_gate_continual_{resnet50,efficientnet_b3}.json` | `outputs/ssl_run_artifacts/sip/v1.0/gate_report_CONTINUAL_*.json` | SSL-continual | linear-probe гейт init B/D: continual vs ImageNet vs random (κ/AUC/wF1), passed=True |
| `ssl_gate_run2_{resnet50,efficientnet_b3}.json` | `outputs/ssl_run_artifacts/sip/v1.0/gate_report_*.json` | SSL-continual | второй прогон probe-гейта (подтверждает) |

## Пофолдовые CSV (НЕ скопированы — велики; ссылки на источник)

- exp1: `experiments/outputs/exp1/metrics.csv` (265 строк — вся история по 4 конфигам × 5 фолдов).
- exp7: `experiments/outputs/exp7/metrics.csv` (125 строк — оба арма × 5 фолдов).
- exp3/5/6: `metrics.csv` — только заголовок (это eval-эксперименты; реальные числа в JSON выше).

### Пофолдовые CSV exp2 (не скопированы — источник)

- `experiments/outputs/exp2/metrics.csv` — 6 уровней аблации × 3 фолда (baseline, +flip, +flat_field,
  +clahe, +augmentation, full). `metrics_clahe_sweep.csv` — 7 значений clip.

### exp4 CSV + overlays (не скопированы — источник)

- `experiments/outputs/exp4/metrics_{baseline,full_pipeline}.csv` — обе арки EffNet-B4, fold 0, 20 эп.
- `experiments/outputs/exp4/gradcam/*.png` — 50 качественных overlay-сравнений (для App E / FIG-4.12).

## Остаточные пробелы

- exp2 σ-свип flat-field — НЕ прогнан; уровень +OD-fovea rotation — отсутствует.
- Категория B (per-class/ROC/PR/калибровка/стат-тесты exp1) — нужен ре-инференс (скрипты готовы).
