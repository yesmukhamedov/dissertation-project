# SSL-инициализация интегрированного арма + linear-probe гейт (Premise 4 / CFC-2.8)

Governance (`HYPOTHESIS.md` Premise 4): интегрированный арм (Config B/D) инициализируется
in-domain SSL на неразмеченном EyePACS-«test» (53 576 изображений, дизъюнктен с Exp-1 корпусом,
SB-2.4), **BYOL primary, from-scratch на 4-канальном тензоре**, и допуск в Exp-1 **гейтится
linear-probe критерием**. Ниже — фактические результаты гейта.

## Этап 1 — from-scratch SSL: ПРОВАЛЕН (COMPARISON.txt)

Референс: random κ 0.00 / AUC 0.50; ImageNet κ 0.32 / AUC 0.71.

| Метод (from-scratch, 4ch) | эпохи | κ_SSL | passed |
|---------------------------|-------|-------|--------|
| BYOL (primary по governance) | 50 | ~0.000 (коллапс) | ✗ |
| MoCo-v2 | 50 / 100 | 0.112 / 0.109 | ✗ |
| DINO | 50 / 100 | 0.075 / 0.061 | ✗ |

Ни один from-scratch метод не превзошёл ImageNet → пивот на **continual-SSL fallback**
(governance-санкционированный, CFC-2.8): ImageNet→MoCo-v2, ep50, на 4-канальном тензоре.

## Этап 2 — continual-SSL: ПРОШЁЛ гейт (linear-probe, patient-level holdout, n_test=8036)

Это и есть инициализация, реально используемая в Config B/D. Тестируется linear-probe (заморожённый
бэкбон + линейная голова). Источник: `data/ssl_gate_continual_{resnet50,efficientnet_b3}.json`
(+ второй прогон `ssl_gate_run2_*` — подтверждает).

### ResNet-50 (Config B) — крупный выигрыш

| Init | wF1 | ROC-AUC | κ (quad) |
|------|-----|---------|----------|
| random | 0.624 | 0.50 | 0.000 |
| ImageNet | 0.666 | 0.742 | 0.340 |
| **Continual-SSL** | **0.743** | **0.772** | **0.659** |
| Δ (continual − ImageNet) | +0.077 | +0.030 | **+0.319** |

Второй прогон: ImageNet κ 0.357, Continual κ 0.605 → **Δκ +0.248**. Оба прогона: **+0.25…0.32 κ** —
устойчивый крупный выигрыш от in-domain инициализации для ResNet-50.

### EfficientNet-B3 (Config D) — БЕЗ in-domain выигрыша (честная оговорка)

| Init | wF1 | ROC-AUC | κ (quad) |
|------|-----|---------|----------|
| random | 0.624 | 0.52 | 0.000 |
| ImageNet | 0.683 | 0.739 | 0.445 |
| **Continual-SSL** | 0.686 | 0.753 | **0.435** |
| Δ (continual − ImageNet) | +0.003 | +0.014 | **−0.010** |

Второй прогон: ImageNet κ 0.435, Continual κ 0.431 → **Δκ −0.004**. Оба прогона: continual ≈ ImageNet.
**EfficientNet-B3 не получает in-domain выигрыша** от continual-SSL — инициализация Config D фактически
эквивалентна ImageNet; выбор continual для D — симметрия/консистентность, а не прирост (детерм. probe, не шум).

## Гейт-вердикт (оба бэкбона)

`passed=true` для обоих: beats_random ✓, competitive_with_imagenet ✓, not_collapsed ✓.
Т.е. continual-SSL допущена в Exp-1 как инициализация B/D.

## Связь с результатами

- **CFC-2.8:** B/D = композит (препроцессинг × инициализация). Гейт показывает, что инициализация
  реально «ретина-осведомлённая» только у ResNet-50; у EffNet-B3 она ≈ ImageNet. Это объясняет, почему
  в exp1 прирост AUC есть у обоих (D-vs-C DeLong +0.027, p<10⁻⁴), но у D он не может идти от init
  (init ≈ ImageNet) → согласуется с exp2 (препроцессинг-only тоже не улучшает) — эффект нераздельно
  композитный. Связь: [[continual-ssl-init-decision]], `findings/exp1.md`, `hypotheses/H-1.md`.
- **SIP-альтернатива** (`gate_report_SIP_resnet50.json`, κ 0.658) построена, но НЕ выбрана — B/D используют continual.
- Траектории обучения continual: `experiments/outputs/ssl_run_artifacts/continual_trajectory{,_eff}.json` (для FIG при желании).

Данные: `data/ssl_gate_continual_*.json`, `data/ssl_gate_run2_*.json`, `data/ssl_COMPARISON.txt`.
Чекпойнты B/D-init: `experiments/outputs/ssl/v4.0/ssl_mocov2_{resnet50,efficientnet_b3}_4ch_256_ep50.pt`.
