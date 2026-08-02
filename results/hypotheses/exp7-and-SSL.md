# Exp 7 (без гипотезы) + SSL — вердикты

## Exp 7 — Small-Data Trainability (IDRiD → Clinical) — ПОЗИТИВ

Не привязан к формальной гипотезе (сравнение обучаемости арма baseline vs full на малых данных).

**Исход.** full − baseline = **+0.0899 weighted-F1** (0.3052 vs 0.2153), +0.1142 κ, +0.0410 AUC.
Full стабильно ≥ baseline и по внутреннему IDRiD-val F1.

**Значение для тезиса.** Единственный чёткий позитив для конвейера и **самый важный
конструктивный результат**: когда обучающих данных мало (клинический сценарий Казахстана — как
раз целевой), 4-канальный препроцессинг даёт ощутимый выигрыш. Формирует главный практический
вклад: «препроцессинг — эффективный априор при нехватке данных». Контраст с [[H-7]] (zero-shot
перенос) объясняет, КОГДА препроцессинг помогает: при обучении в целевом домене, не при переносе.

---

## SSL — In-Domain Self-Supervised Pretraining — все гейты провалены

**Исход.** From-scratch in-domain SSL (BYOL/MoCo-v2/DINO) не прошёл linear-probe гейт:
BYOL κ≈0.00 (коллапс), MoCo-v2 κ 0.112, DINO κ 0.075 — все ниже ImageNet (κ 0.32).

**Решение (принято ранее).** Пивот на **continual-SSL fallback** (ImageNet→MoCo-v2, ep50).
Linear-probe гейт (patient-level holdout, n=8036), два прогона → **полная таблица в
`tables/SSL_continual_gate.md`** (собрано 2026-07-28 из `data/ssl_gate_continual_*.json`):
- **ResNet-50:** continual κ **0.659/0.605** vs ImageNet **0.340/0.357** → **Δκ +0.25…0.32 (крупный выигрыш)**;
- **EfficientNet-B3:** continual κ **0.435/0.431** vs ImageNet **0.445/0.435** → **Δκ ≈ 0 (без in-domain выигрыша)**.
- Оба `passed=true` (beats_random ✓, competitive_with_imagenet ✓, not_collapsed ✓) → допущены в Exp-1 как init B/D.

**Значение для тезиса.** Двухэтапный SSL-нарратив (Premise 4): (1) from-scratch BYOL/MoCo/DINO
провалили гейт → (2) continual-SSL fallback прошёл. Честная асимметрия: ResNet-50 получает реальную
«ретина-осведомлённую» инициализацию, EfficientNet-B3 — нет (≈ ImageNet). Config B/D используют
continual-ep50. Confound CFC-2.8 связывает это с [[H-1]]: инициализация — часть «интегрированной
конфигурации» (см. `findings/exp1.md` — прирост AUC D-vs-C значим, но у D не может идти от init).
