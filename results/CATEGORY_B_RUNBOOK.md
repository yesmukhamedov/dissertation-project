# Категория B — runbook (ре-инференс exp1 → таблицы)

> **Статус на 2026-08-02.** Категория B как задача **закрыта** — все её величины (per-class,
> калибровка, клиника in-domain, парные стат-тесты) есть в `results/tables/` по прогону
> 2026-08-02. Этот runbook сохраняется как **процедура**: он понадобится, чтобы получить
> `predictions.npz` нового прогона для ROC/PR-кривых (пункт R2) и для сверки офлайн-предсказаний
> с обучением (пробел G-10) после того, как будут выложены артефакты прогона (NEW-1).
> Числовые ориентиры в разделе «Верификация» ниже относятся к прежнему прогону.

Категория B = величины, которых обучение exp1 НЕ сохранило (только по-эпизодные агрегаты):
per-class F1/AUC, матрицы ошибок, ROC/PR, калибровка ECE/Brier, клиника in-domain,
стат-тесты DeLong/McNemar. Все они требуют **по-объектных вероятностей** → нужен один прогон
инференса лучших чекпойнтов exp1 (A–D × 5 фолдов) по их val-выборкам.

## Почему на GPU-боксе

Полный ре-инференс = ~35 126 изображений × 4 конфига при 512². **Замер на этом CPU-окружении
(2026-07-27): 0.46 img/s** для config A (baseline, самый лёгкий) → ~21 час ТОЛЬКО на A; конфиги
B/D (полный пайплайн 4ch) ещё медленнее → полный прогон ≈ **несколько суток** и хрупко (фоновые
задачи здесь реапятся). На RTX 3060/WSL — порядка **минут–часа**. Поэтому шаг 1 (дамп) гоняем на
GPU-боксе; шаг 2 (анализ) — CPU-дёшев, где угодно.

## Скрипты (готовы, провалидированы smoke-тестом на CPU)

- `experiments/scripts/dump_exp1_predictions.py` — инференс чекпойнтов → `predictions.npz`
  (переиспользует точные сплиты/препроцессинг из `exp1_factorial`, поэтому val-выборки совпадают с обучением).
- `experiments/scripts/analyze_exp1_predictions.py` — `predictions.npz` → markdown-таблицы в `results/tables/`.

## Шаг 1 — дамп на GPU-боксе (RTX 3060/WSL), 3 запуска

Раздельно: baseline A/C (без кэша) и full B/D (каждый со своим `_run_exp1{B,D}.yaml`, где уже
прописан `paths.cache_dir: C:/ssl_data/cache_512` → стадии 0–4 из кэша). Все три конфига дают тот
же seed-42 5-fold сплит, что и обучение → val-фолды совпадают.

```bash
cd <repo>/experiments
conda activate dr-classifier
python scripts/dump_exp1_predictions.py --config configs/_run_exp1AC.yaml --configs A,C --out outputs/exp1/pred_AC.npz
python scripts/dump_exp1_predictions.py --config configs/_run_exp1B.yaml  --configs B   --out outputs/exp1/pred_B.npz
python scripts/dump_exp1_predictions.py --config configs/_run_exp1D.yaml  --configs D   --out outputs/exp1/pred_D.npz
```

Проверка: в логе для каждого `<cfg> foldN` wF1 должен совпасть с `exp1/summary.json` (±). Если нет —
см. раздел «Верификация» ниже (вероятно, 512²-кэш регенерирован после fix'а FOV-crop 2026-07-19).

Затем скопировать три файла в `E:\dissertation-project\experiments\outputs\exp1\`:
`pred_AC.npz`, `pred_B.npz`, `pred_D.npz`.

## Шаг 2 — анализ (CPU, быстро; на E:-машине)

```bash
python scripts/analyze_exp1_predictions.py \
    --pred outputs/exp1/pred_AC.npz outputs/exp1/pred_B.npz outputs/exp1/pred_D.npz
# --pred принимает несколько файлов и объединяет конфиги (для парных B-vs-A / D-vs-C).
# пишет в results/tables/: exp1_per_class.md, TAB-4.3_exp1_calibration.md,
#                          exp1_clinical_indomain.md, TAB-5.1_statistical.md
```

## Верификация

- Per-fold wF1 в логах ≈ `outputs/exp1/summary.json`. Если расходится: чекпойнты exp1 обучены
  10–14 июля (до fix'а FOV-crop 19 июля), а `cache_512` мог быть регенерирован ПОСЛЕ fix'а →
  препроцессинг B/D при инференсе ≠ обучению. Решение: (а) использовать кэш времени обучения, либо
  (б) принять ре-инференс как самосогласованную оценку и пометить оговоркой. A/C (baseline, без
  кэша) от этого не зависят.
- `analyze` проверяет выравнивание пар (`np.array_equal(y_true_a, y_true_b)`) и пропускает пару, если не сошлось.

## После получения таблиц — обновить

- `results/GAP_ANALYSIS.md` (категория B → закрыта), `results/TODO_BEFORE_WRITING.md` (B0–B4).
- `results/tables/TAB-5.4_clinical_referable.md` — дополнить exp1 in-domain строками (B3).
- `results/tables/TAB-5.2_claim_strength.md` — если DeLong покажет значимость ΔAUC (B vs A / D vs C),
  усилить формулировку по AUC-выигрышу (сейчас MODERATE по фолдовым CI).

## Замечания по корректности

- Пары **B vs A** и **D vs C** оцениваются на ОДНОЙ val-выборке по фолдам (сплиты идентичны между
  конфигами) → строки predictions.npz выровнены; `analyze_*` проверяет `np.array_equal(y_true_a,y_true_b)`
  перед парными тестами и пропускает пару, если не выровнены.
- DeLong тестирует referable-AUC (grade≥2); McNemar — долю верных предсказаний.
- Если для B/D задан `cache_dir` — дамп использует `CachedEyePACSDataset` (как в обучении).
- Smoke локально: `--smoke 64 --configs A --fold 0 --out outputs/exp1/predictions_smoke.npz` (≈14 img, CPU).
