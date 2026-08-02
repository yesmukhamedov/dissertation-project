# GAP_ANALYSIS — что собрано, чего не хватает (диссертация + презентация + demo)

Сверка требований трёх потребителей против собранного в `results/`. Состояние на прогон
**2026-08-02**. Требования взяты из `thesis/ASSET_INVENTORY.md` (перечень нужного актуален,
статусы устарели), `demo/web/src/data.js` и `defense/presentation/slides/*`.

## Короткий ответ

`results/` **полностью покрывает** результатный слой всех экспериментов: метрики, вердикты,
таблицы, словесные выводы по exp1–exp7, SSL и новому блоку H-3. Категории A, B, C закрыты.

Осталось три вещи, и первая — блокирующая:

1. 🔴 **Провенанс.** Числа взяты из `VALUES.md`; сырых артефактов прогона нет ни в
   `experiments/outputs/`, ни в `results/data/` (там числа предыдущего прогона).
   → `INTEGRITY_NOTE.md` §1, `HYPOTHESIS_COVERAGE.md` NEW-1.
2. 🔴 **G-3** — качественные Grad-CAM overlay на клиническом (KZ) датасете (требует формулировка H-5).
3. 🟡 **G-8 остаток** — Stage 3 (FOV-маска) не изолирована в аблации.

⚠️ И отдельно: демо/защита построены на третьем, ещё более старом наборе чисел — см.
`INTEGRITY_NOTE.md` §2.

## Что УЖЕ собрано (✅)

| Величина | Эксперимент | Где в results/ |
|----------|-------------|----------------|
| Факторные F1/AUC/κ/Acc (A–D) + EH-3 доминирование | exp1 | `tables/TAB-4.2`, `findings/exp1`, `hypotheses/H-1` |
| exp1 per-class F1/precision/recall + матрицы ошибок | exp1 | `tables/exp1_per_class.md` |
| exp1 калибровка ECE/Brier | exp1 | `tables/TAB-4.3_exp1_calibration.md` |
| exp1 клинические метрики in-domain | exp1 | `tables/exp1_clinical_indomain.md` |
| exp1 сходимость, loss-gap, CV-CI, bootstrap-CI | exp1 | `tables/exp1_convergence_ci.md` |
| Стат-тесты: DeLong, McNemar, **Holm**, **смешанная ANOVA** | exp1 | `tables/TAB-5.1_statistical.md` |
| Кумулятивная аблация 8 уровней + пофолдовые значения | exp2 | `tables/TAB-4.4_exp2_ablation.md` |
| Per-stage image quality (CNR/Entropy/SSIM) по 8 уровням | exp2 | `tables/TAB-4.5_exp2_image_quality.md` |
| Двумерный свип CLAHE + сетки F1(DR1)/F1(DR2) | exp2 | `tables/exp2_clahe_sweep.md` |
| **σ-свип flat-field** (новое) | exp2 | `tables/exp2_flatfield_sigma_sweep.md` |
| **Дистанция доменов MMD/KL, 6 доменов** (новое) | H-3 | `tables/H-3_domain_distance.md`, `hypotheses/H-3.md` |
| APTOS-трансфер + G + per-class + матрицы + referable | exp3 | `tables/TAB-4.6`, `per_class_and_confusion`, `findings/exp3` |
| Grad-CAM ALO/IoU + свип порога + эффект пола | exp4 | `tables/TAB-4.7_exp4_alo_iou.md` |
| Классификация арок B4 | exp4 | `tables/exp4_classification.md` |
| Клиническая деградация Δ + CI + p + Δ_drop | exp5 | `tables/TAB-4.8`, `hypotheses/H-7` |
| Сдвиг устройства (5 групп) + разброс + per-class | exp6 | `tables/TAB-4.9`, `per_class_and_confusion` |
| Малодатное IDRiD→Clinical + preregistered | exp7 | `tables/TAB-4.10_exp7_smalldata.md` |
| SSL probe-гейт (from-scratch + SIP + continual) | SSL | `tables/SSL_continual_gate.md` |
| Клинические метрики referable по трём сценариям | 1/3/6 | `tables/TAB-5.4_clinical_referable.md` |
| Сила утверждений PC-0…PC-10 | все | `tables/TAB-5.2_claim_strength.md` |
| Сводка гипотез + сквозной механизм + данные радара | все | `findings/summary-and-dominance.md` |
| Вычислительные бенчмарки (params/FLOPs/latency/VRAM) | — | `tables/computational_and_iq.md` |

## Чего НЕ хватает

### Блокирующее

| # | Блок | Как получить | Что блокирует |
|---|------|--------------|---------------|
| **NEW-1** | Сырые артефакты прогона 2026-08-02 в `experiments/outputs/` + обновление `results/data/*.json` | выложить файлы прогона; затем сверить с `results/tables/` | прослеживаемость чисел в главах; перекрёстную проверку; закрытие G-10 |

### Требуется прогон/код

| # | Блок | Статус | Целевой ассет |
|---|------|--------|---------------|
| **G-3** | Grad-CAM overlay на клиническом (KZ) датасете | 🔴 в `exp4_explainability.py` нет ветки clinical; датасет доступен (`E:/datasets/clinical`) | качественная часть H-5, App E, FIG-4.13/4.14 |
| **G-8 ост.** | Изоляция Stage 3 (FOV-маска) в аблации | 🟡 нужен флаг в `PreprocessingConfig` + 3-канальный вариант модели + уровень | полнота TAB-4.4 |
| **NEW-2** | Параметры MMD (ядро, размер выборки, число bootstrap-итераций) | 🟡 извлечь из конфигурации эксперимента | методологическая часть §4/§5 по H-3 |

### Расчёты по имеющимся числам (прогона не требуют)

| # | Блок | Как получить |
|---|------|--------------|
| R1 | Относительная деградация (Δ_drop / in-domain) для H-7 | арифметика по `TAB-4.8`; нужна для честной формулировки §4.6 и §5.4 |
| R2 | ROC/PR-кривые как рисунки | из `predictions.npz` нового прогона (после NEW-1) |
| R3 | Матрицы ошибок по группам камер (exp6) | в данных прогона зафиксированы только per-class F1 → нужна доп. выгрузка для App F |

### Известные пробелы реализации

| # | Блок | Статус |
|---|------|--------|
| VVI | Не реализован в `src/utils/image_quality.py`; в демо-`data.js` — выдуманная величина | заявить как ограничение либо реализовать |

## Сводный чеклист (величина → статус)

| Результатная величина | Собрано? | Где / как получить |
|-----------------------|----------|--------------------|
| Факторные метрики A–D + EH-3 | ✅ | `TAB-4.2` |
| exp1 per-class / confusion / калибровка / клиника | ✅ | `exp1_per_class`, `TAB-4.3`, `exp1_clinical_indomain` |
| Стат-тесты (DeLong/McNemar/Holm/ANOVA) | ✅ | `TAB-5.1` |
| Аблация (кумулятивная, 8 уровней) | ✅ | `TAB-4.4` — ⚠️ Stage 3 не изолирована |
| CLAHE-свип (двумерный, на EyePACS) | ✅ | `exp2_clahe_sweep` |
| σ-свип flat-field | ✅ | `exp2_flatfield_sigma_sweep` |
| Per-stage image quality | ✅ | `TAB-4.5` — ⚠️ VVI не реализован |
| Дистанция доменов MMD/KL | ✅ | `H-3_domain_distance` — ⚠️ NEW-2 |
| APTOS G + per-class + матрицы | ✅ | `TAB-4.6`, `per_class_and_confusion` |
| Grad-CAM ALO/IoU (IDRiD) | ✅ | `TAB-4.7` |
| Grad-CAM overlay (Clinical KZ) | ❌ | **G-3** |
| Клиническая деградация Δ | ✅ | `TAB-4.8` — ⚠️ R1 |
| Сдвиг устройства + разброс | ✅ | `TAB-4.9` — ⚠️ R3 (матрицы) |
| Малодатное обучение | ✅ | `TAB-4.10` |
| SSL probe-гейт | ✅ | `SSL_continual_gate` |
| Вычислительные бенчмарки | ✅ | `computational_and_iq` |
| Сила утверждений PC-0…10 | ✅ | `TAB-5.2` |
| Сводный радар / доминирование | ✅ | `findings/summary-and-dominance` |
| Вердикты гипотез | ✅ | `STATUS.md` — ⚠️ демо/защита противоречат |
| Прослеживаемость до `outputs/` | ❌ | **NEW-1** |

## Рекомендованный порядок закрытия

1. **NEW-1** — восстановить провенанс. Без этого остальное носит характер черновика.
2. **G-3** (~2 ч) и **NEW-2** (минуты) — закрывают букву H-5 и H-3.
3. **R1, R3** — расчёты/выгрузки по имеющимся данным для §4.6 и App F.
4. **G-8 остаток** — дорогое обучение, можно заявить как ограничение, если сроки поджимают.
5. Затем — **пересинхронизировать `demo/web/data.js` + defense/slides** на реальные числа
   и вердикты (`INTEGRITY_NOTE.md` §2).

## Замечание по ASSET_INVENTORY.md

`thesis/ASSET_INVENTORY.md` датирован до прогонов и помечает exp1–7 как ⏳/❌ NOT RUN. По факту
все завершены. Инвентарь стоит обновить (RES-EXP1 ✅, TAB-4.2…4.10 ✅ с реальными числами,
вердикты гипотез — 6 подтверждены, H-7 частично, добавился блок H-3) — отдельный шаг после NEW-1.
