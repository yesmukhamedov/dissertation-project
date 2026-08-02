# TODO — что сделать ДО написания диссертации (рабочий чеклист)

> Временный рабочий файл, чтобы не забыть. Удалить/архивировать, когда всё закрыто и начато
> написание глав. Текущая фаза: **собираем только текстовые данные по экспериментам** — прозу
> глав ещё НЕ пишем. Полный разбор — в [GAP_ANALYSIS.md](GAP_ANALYSIS.md); статусы — в
> [STATUS.md](STATUS.md); что нужно главам — в [CHAPTER_STATUS.md](CHAPTER_STATUS.md).

## Уже сделано ✅

- [x] Собраны первичные результаты 5 завершённых экспериментов (exp1, exp3, exp5, exp6, exp7 + SSL):
      реальные метрики, таблицы (`tables/`), карточки гипотез (`hypotheses/`), словесные выводы (`findings/`).
- [x] Зафиксировано расхождение демо/защиты с реальными данными ([INTEGRITY_NOTE.md](INTEGRITY_NOTE.md)).
- [x] Составлен gap-анализ требований диссертации/презентации/демо ([GAP_ANALYSIS.md](GAP_ANALYSIS.md)).
- [x] Скопированы канонические JSON в `data/`; указатель в `PROJECT_MEMORY.md`.

---

## ФАЗА 1 — досбор текстовых данных (делаем сейчас, до написания)

### Категория A — выводится сейчас (без обучения и ре-инференса) — ✅ ЗАКРЫТА (2026-07-24)

- [x] **A1.** Клинические метрики (Sens/Spec/PPV/NPV, referable-AUC) exp3+exp6 → `tables/TAB-5.4_clinical_referable.md`. (exp1 in-domain — остаётся B3.)
- [x] **A2.** Per-class F1 + матрицы ошибок exp3, exp6 → `tables/per_class_and_confusion.md`. (exp1 — остаётся B1.)
- [x] **A3.** Сила утверждений PC-0…PC-10 из вердиктов → `tables/TAB-5.2_claim_strength.md` (4/6 эмпирич. PC = REFUTED).
- [x] **A4.** Сводка гипотез + сквозной механизм + данные радара → `findings/summary-and-dominance.md`.
- [x] **A5/A6.** Сходимость, переобучение (loss-gap baseline 0.25 vs pipeline 0.02), best-эпохи → `tables/exp1_convergence_ci.md`.
- [x] **A7.** ✅ ЗАКРЫТ ПОЛНОСТЬЮ 2026-07-28. Params (ResNet-50 23.52M, EffNet-B3 10.70M; демо 25.6/12.2M — неверно)
      **+ FLOPs/latency/VRAM измерены на RTX 3060** (`scripts/benchmark_compute.py` → `outputs/compute_benchmark.{json,md}`)
      → `tables/computational_and_iq.md`. Находки: 4-й канал стоит +0.9% FLOPs и +24 МиБ (тезис «дешёвый априор»);
      EffNet-B3 дешевле по FLOPs в 4.3×, но по latency НЕ быстрее (bs=1 медленнее); VRAM обучения EffNet 13.7 ГиБ
      против 3.7 ГиБ у ResNet — batch=16 ограничен активациями fp32 при 512², а не размером модели.
- [x] **A8.** Качество изображения — **закрыто через exp2**: реальные CNR/Entropy/SSIM по всем 6 уровням
      (`tables/TAB-4.5_exp2_image_quality.md`, восстановлено 2026-07-28). Находка: flat-field CNR 20→42,
      CLAHE возвращает к 21.8 → у full прироста CNR нет, а SSIM минимален (0.599); связи IQ↔wF1 нет.
      VVI не реализован (в демо выдуман). Демо-`IQ` не использовать.
- [x] **A9.** CV 95% CI по фолдам exp1 (AUC-интервалы pipeline не пересекаются с baseline) → `tables/exp1_convergence_ci.md`.
      Строгий по-объектный bootstrap — остаётся B4.

### Категория B — один прогон ре-инференса чекпойнтов exp1

- [x] **B0.** ✅ ЗАВЕРШЁН 2026-07-27: `predictions.npz` содержит A–D × 5 фолдов (проверено).
      **Уточнение: эта машина И ЕСТЬ GPU-бокс** — RTX 3060
      доступна через **WSL Ubuntu + conda `dr-classifier`** (torch 2.5.1+cu121). Никакой отдельный
      бокс не нужен; ошибка была в том, что Bash/PowerShell звали системный Python (CPU-torch).
      Дамп запущен: `configs/_run_exp1_wsl_e.yaml` (пути `/mnt/e`, cache null → live препроцессинг),
      `--configs A,C,B,D`, `--out outputs/exp1/predictions.npz`, resume-safe + инкрементальный save.
      Лог: `outputs/exp1/dump_gpu.log`. По завершении → шаг B1–B4 (`analyze_exp1_predictions.py`).
- [x] **B1.** exp1 per-class F1/precision/recall + матрицы ошибок → `tables/exp1_per_class.md` (конвейер тянет меньшинства: класс1 F1 0.212→0.280, macro-F1 A 0.536→B 0.561).
- [x] **B2.** exp1 калибровка ECE/Brier → `tables/TAB-4.3_exp1_calibration.md`. **Находка: конвейер хуже калиброван** (ECE A/C 0.06–0.07 → B/D 0.19–0.21).
- [x] **B3.** exp1 клиника in-domain (referable Sens/Spec/PPV/NPV/AUC) → `tables/exp1_clinical_indomain.md` (Sens A→B 0.675→0.717; C→D 0.698→0.756).
- [x] **B4.** Парные стат-тесты: **DeLong B-vs-A ΔAUC +0.036 z=17.2 p<10⁻⁴; D-vs-C +0.027 z=14.0 p<10⁻⁴**; McNemar p<10⁻⁴ → `tables/TAB-5.1_statistical.md`. Прирост AUC ПОДТВЕРЖДЁН.
  (ROC/PR-кривые как рисунки — опционально позже из `predictions.npz`; mixed-effects — опционально.)

---

## ФАЗА 2 — данные из незавершённых экспериментов (Категория C, по готовности)

> ⚠️ Сверка с буквой `thesis/governance/HYPOTHESIS.md` (2026-07-28) нашла пробелы **шире**
> категории C — см. **[HYPOTHESIS_COVERAGE.md](HYPOTHESIS_COVERAGE.md)** (G-1…G-12, 3 волны).
> Критично до написания §4.4 и §4.5: **G-4** (exp3 считан ДО фикса Stage-2 → вердикт H-4 под
> вопросом) и **G-1** (exp4 оценён на n=5 масках вместо доступных 54).

- [x] **C1.** exp2 аблация собрана → `tables/TAB-4.4_exp2_ablation.md`, `data/exp2_*`,
      `hypotheses/H-2.md`, `findings/exp2.md`. **Пересчитана 2026-07-28** после дообучения
      `full`/fold2 (был оборван на 2-й эпохе): `full` = 0.7463 ± 0.0136 (−1.5пп) вместо −4.1пп.
      ⚠️ Оговорки: 15%/3-fold, ImageNet-init, нет уровня +OD-fovea rotation, различия между
      уровнями внутри шума. Находка: стадии по отдельности wF1 не улучшают (подтверждает CFC-2.8),
      но и не ухудшают значимо → **PC-8 = NOT ESTABLISHED**, не «REFUTED».
- [~] **C2.** exp2 CLAHE-свип → `tables/exp2_clahe_sweep.md` (профиль с оптимумом ✓); per-stage
      image-quality **по всем 6 уровням** → `tables/TAB-4.5_exp2_image_quality.md` (восстановлено
      2026-07-28). ⚠️ **σ-свип flat-field НЕ прогнан** (открыто для §4.3.3).
- [ ] **C2b.** σ-свип flat-field (0.05–0.10·D) для полного PC-2. ⚠️ Это НЕ «допрогнать»: Part C
      в `src/experiments/exp2_ablation.py` не реализована (есть только строка в докстринге, функции
      нет — в отличие от `_run_clahe_sweep`). Либо писать код, либо оставлять заявленным ограничением.
- [x] **C3.** exp4 собран → `tables/TAB-4.7_exp4_alo_iou.md`, `tables/exp4_classification.md`,
      `hypotheses/H-5.md`, `findings/exp4.md`. **ПЕРЕСЧИТАН 2026-07-28 (G-1/G-2):** анализ на всех
      **54** изображениях IDRiD с масками (было 5 — артефакт сэмплирования) + парные тесты →
      **H-5 НЕ подтверждена** (2/4 типов, p ≥ 0.38, значимости нет ни при каком пороге).
      Канон: `data/exp4_iou_results_maskset.json`; 54 overlay в `outputs/exp4/gradcam_maskset/`.
      Остаётся открытым G-3: клинические (KZ) overlay, которых требует формулировка H-5.

---

## ФАЗА 3 — синхронизация потребителей (после сбора, параллельно с/перед написанием)

- [ ] **S1.** Обновить `thesis/ASSET_INVENTORY.md` под реальные статусы (exp1/3/5/6/7 ✅, вердикты false).
- [ ] **S2.** Пересобрать `demo/web/src/data.js` из реальных чисел (убрать выдуманные `IQ`/`COMPUTE`;
      `HYPOTHESES` — реальные вердикты). Пересобрать `demo/web/generate_charts_*.py` от `outputs/`.
- [ ] **S3.** Обновить слайды защиты `defense/presentation/slides/33–43_*` и нарративные скрипты
      (убрать «растайды/дәлелдейді» там, где гипотеза не подтверждена).

---

## ФАЗА 4 — только после сбора: НАЧАТЬ ПИСАТЬ

Порядок (из `CHAPTER_STATUS.md`): §4.4(H-4) · §4.6(H-7) · §4.7(H-6) · §4.8(exp7) · §4.2(H-1 с
оговоркой CFC-2.8) → §5.2 (TAB-5.1/5.2) → §4.3(H-2 после exp2) · §4.5(H-5 после exp4)+§5.1 →
§4.C · §5.4 · §5.3 · гл.7 · гл.0/§0.8. Workflow: brief→draft→continuity→review→translation.

**Правило:** любые числа — только из `results/` (= из `experiments/outputs/`), НИКОГДА из `demo/web/data.js`.
