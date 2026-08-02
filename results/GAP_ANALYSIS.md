# GAP_ANALYSIS — что собрано, чего не хватает (диссертация + презентация + demo)

Сверка требований трёх потребителей против собранного в `results/`.
Требования взяты из `thesis/ASSET_INVENTORY.md` (мастер-список TAB/FIG/RES; датирован 2026-06-08,
до прогонов — статусы в нём устарели, но перечень нужного актуален), `demo/web/src/data.js`
(константы дашборда) и `defense/presentation/slides/*` (слайды результатов 32–43).

## Короткий ответ

`results/` **полностью покрывает** первичные результаты 5 завершённых экспериментов
(exp1, exp3, exp5, exp6, exp7 + SSL): метрики, вердикты, таблицы, словесные выводы. Но
демо/защита/гл.5 требуют ещё **8 блоков** результатного контента, которых в собранном наборе нет.
Хорошая новость: **бóльшая часть выводится уже сейчас** — без ожидания exp2/exp4.

⚠️ И отдельно: демо/защита не просто «не хватает» — они **противоречат** реальным данным
(все гипотезы показаны «подтверждёнными»). См. `INTEGRITY_NOTE.md`.

## Что УЖЕ собрано (✅)

| Величина | Эксперимент | Где в results/ |
|----------|-------------|----------------|
| Факторные F1/AUC/κ/Acc (A–D) + EH-3 доминирование | exp1 | `tables/TAB-4.2`, `findings/exp1`, `hypotheses/H-1` |
| APTOS-трансфер + G | exp3 | `tables/TAB-4.6`, `findings/exp3`, `hypotheses/H-4` |
| Клиническая деградация Δ + CI + p | exp5 | `tables/TAB-4.8`, `findings/exp5`, `hypotheses/H-7` |
| Сдвиг устройства (5 групп) + дисперсия | exp6 | `tables/TAB-4.9`, `findings/exp6`, `hypotheses/H-6` |
| Малодатное IDRiD→Clinical (единственный позитив) | exp7 | `tables/TAB-4.10`, `findings/exp7-and-ssl` |
| SSL probe-гейт + continual fallback | SSL | `hypotheses/exp7-and-SSL`, `findings/exp7-and-ssl` |

## Чего НЕ хватает — по способу получения

### Категория A — выводится СЕЙЧАС (без нового обучения, без ре-инференса)

| # | Блок | Источник | Целевой ассет |
|---|------|----------|---------------|
| A1 | Клинические метрики (Sens/Spec/PPV/NPV, referable-AUC) для exp3 и exp6 | **уже в JSON** (`exp3_*`, `exp6_*` содержат sensitivity/specificity/ppv/npv/binary_roc_auc) | TAB-5.4 (частично) |
| A2 | Per-class F1 + матрицы ошибок для exp3, exp6 | **уже в JSON** (`per_class_f1`, `confusion_matrix`) | FIG-4.6/4.8 (частично), `CLS` |
| A3 | Классификация силы утверждений PC-1…PC-10 (STRONG/MODERATE/…) | из вердиктов гипотез (H-1/4/6/7=false, exp7=poz) | TAB-5.2 |
| A4 | Сводная радар-диаграмма / EH-3-доминирование | из вердиктов | FIG-5.3 |
| A5 | Train-test gap (переобучение) | `outputs/exp1/metrics.csv` (train vs val по эпохам) | `TRAIN_TEST_GAP` |
| A6 | Кривые обучения (данные) A–D, exp7 | `outputs/exp{1,7}/metrics.csv` (полная история по фолдам) | FIG-4.5, FIG-4.16 |
| A7 | Вычислительные бенчмарки (params/FLOPs/latency/VRAM) | статически из `src/models/factory.py` + быстрый прогон | FIG-5.2, `COMPUTE` |
| A8 | Метрики качества изображения (CNR/VVI/Entropy/SSIM) | `src/utils/image_quality.py` на препроц. образцах | TAB-4.5(частично), `IQ` — **сейчас в демо чисто выдуманы** |
| A9 | Bootstrap-CI по первичным метрикам (exp5, exp7 уже есть; добавить exp1 из по-фолдовых) | `statistical_tests.py::bootstrap_ci` | часть TAB-5.1 |

### Категория B — ✅ ЗАКРЫТА (2026-07-27): ре-инференс A–D×5 фолдов (n=35126) → `predictions.npz`

Готово: `tables/{exp1_per_class, TAB-4.3_exp1_calibration, exp1_clinical_indomain, TAB-5.1_statistical}.md`.
**Итог:** прирост AUC от конвейера стат. подтверждён (DeLong p<10⁻⁴); +macro-F1/referable-sensitivity;
калибровка хуже (ECE ~3×). Детали — `findings/exp1.md` (раздел «Категория B»). Ниже — исходный список (все закрыты):

Первичные прогоны сохранили только по-эпизодные агрегаты, НЕ по-объектные вероятности. Чтобы
получить, нужно один раз прогнать инференс лучших чекпойнтов (`infer_dataset`) и сохранить y_prob.

| # | Блок | Целевой ассет |
|---|------|---------------|
| B1 | exp1 per-class F1/AUC, матрицы ошибок, ROC, PR-кривые | FIG-4.6/4.7/4.8, FIG-5.4, `CLS`/`CLS_AUC` |
| B2 | exp1 калибровка (ECE, Brier) по конфигам | TAB-4.3, `CALIBRATION` (`calibration.py` готов) |
| B3 | exp1 клинические метрики in-domain (referable Sens/Spec/PPV/NPV) | TAB-5.4 (полностью), `CLIN` |
| B4 | Парные стат-тесты exp1 (DeLong по AUC, McNemar) + mixed-effects | TAB-5.1, `STAT_TESTS` |

### Категория C — нужны НЕЗАВЕРШЁННЫЕ эксперименты

| # | Блок | Статус | Целевой ассет |
|---|------|--------|---------------|
| C1 | exp2: индивидуальная аблация (baseline+стадия, full) | ✅ ЗАКРЫТО* (`TAB-4.4`) — ⚠️ 15%/3-fold, нет +OD-fovea rotation | TAB-4.4, `ABL_INDIV` |
| C2 | exp2: CLAHE-свип + per-stage image-quality | ✅ част. (`exp2_clahe_sweep`, `TAB-4.5`); IQ по всем 6 уровням (2026-07-28); ⚠️ **σ-свип НЕ прогнан** (не реализован в `exp2_ablation.py`) | TAB-4.5, `CLAHE1/2` (`FF_SWEEP` — открыт) |
| C3 | exp4: Grad-CAM overlays + ALO + IoU + attention-consistency | ✅ ЗАКРЫТО (`TAB-4.7`, `exp4_classification`, 50 overlays); ⚠️ n_масок=5, NC-14 | TAB-4.7 ✓, FIG-4.12 (overlays есть), `ALO`/`IOU` ✓ |

## Сводный чеклист (величина → категория)

| Результатная величина | Экспер. | Собрано? | Как получить |
|-----------------------|---------|----------|--------------|
| Факторные метрики A–D + EH-3 | exp1 | ✅ | — |
| APTOS G | exp3 | ✅ | — |
| Клиническая деградация Δ | exp5 | ✅ | — |
| Сдвиг устройства | exp6 | ✅ | — |
| Малодатное обучение | exp7 | ✅ | — |
| Клинич. метрики (Sens/Spec/PPV/NPV) exp3/exp6 | exp3,6 | ✅ A1 | `TAB-5.4_clinical_referable.md` |
| Per-class F1 + confusion exp3/exp6 | exp3,6 | ✅ A2 | `per_class_and_confusion.md` |
| Сила утверждений PC-1…10 | все | ✅ A3 | `TAB-5.2_claim_strength.md` |
| Сводный радар / доминирование | все | ✅ A4 | `findings/summary-and-dominance.md` |
| Train-test gap | exp1 | ✅ A5 | `exp1_convergence_ci.md` |
| Кривые обучения (данные) | exp1,7 | ✅ A6 | `exp1_convergence_ci.md` |
| Вычислит. бенчмарки | — | ✅ A7 | `computational_and_iq.md` (params + FLOPs/latency/VRAM, RTX 3060, 2026-07-28) |
| Качество изображения CNR/VVI/… | — | ✅ част. A8 | `TAB-4.5` все 6 уровней (2026-07-28); **VVI не реализован** |
| exp1 per-class/confusion/ROC/PR | exp1 | ✅ B1 | `exp1_per_class.md` (ROC/PR как рисунки — опц.) |
| exp1 калибровка ECE/Brier | exp1 | ✅ B2 | `TAB-4.3_exp1_calibration.md` |
| exp1 клинич. in-domain | exp1 | ✅ B3 | `exp1_clinical_indomain.md` |
| Стат-тесты DeLong/McNemar (TAB-5.1) | exp1 | ✅ B4 | `TAB-5.1_statistical.md` |
| Аблация (кум./инд.) | exp2 | ✅ C1 | все 6 уровней × 3 фолда закрыты (`full`/fold2 дообучен 2026-07-28); PC-8 = NOT ESTABLISHED |
| CLAHE/σ свипы + per-stage IQ | exp2 | ✅ част. C2 | CLAHE-свип + IQ есть; **σ-свип не прогнан** (нет в коде) |
| Grad-CAM ALO/IoU/attention | exp4 | ✅ C3 | `TAB-4.7_exp4_alo_iou.md`, 50 overlays; n масок = 5 |
| Вердикты гипотез | все | ✅ (реальные) | — (демо/защита противоречат) |

> Актуальный чеклист — [TODO_BEFORE_WRITING.md](TODO_BEFORE_WRITING.md); эта таблица отражает его состояние на 2026-07-28.

## Рекомендованный порядок закрытия

1. **Категория A целиком** — дёшево, разблокирует TAB-5.2/5.3/5.4, FIG-5.2/5.3, часть гл.5 и §4.
   Отдельно A8/A7 убирают из демо две чисто выдуманные величины (image-quality, compute).
2. **Категория B** — один скрипт ре-инференса лучших чекпойнтов exp1 → `predictions.npz` →
   разом закрывает B1–B4 (per-class, confusion, ROC/PR, калибровка, клиника, стат-тесты, TAB-5.1).
3. **Категория C** — по мере завершения exp2 и дообучения exp4.
4. Затем — **пересинхронизировать demo/web/data.js + defense/slides** на реальные числа и вердикты.

## Замечание по ASSET_INVENTORY.md

`thesis/ASSET_INVENTORY.md` датирован до прогонов: помечает exp1–7 как ⏳/❌ NOT RUN. По факту
exp1/3/5/6/7 завершены. Инвентарь стоит обновить (RES-EXP1 ✅, TAB-4.6/4.8/4.9/4.10 ✅ с реальными
числами, вердикты гипотез — false) — но это отдельный шаг после закрытия категории A/B.
