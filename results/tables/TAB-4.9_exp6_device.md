# TAB-4.9 — Experiment 6: Device / Camera Domain Shift (H-6)

Full pipeline (EffNet-B3) обучен на EyePACS (Canon), оценён на группах камер. Порог **g_floor = 0.7**.
In-domain canon_eyepacs wF1 = 0.7952. Источник: `data/exp6_device_shift_results.json`.

| Camera group | Datasets | wF1 | ROC-AUC | κ (quad) | Referable AUC | **g_ratio** | ≥0.7 |
|--------------|----------|-----|---------|----------|---------------|-------------|------|
| kowa_idrid | IDRiD, RFMiD | 0.5097 | 0.8855 | 0.8216 | 0.9869 | 0.641 | ✗ |
| mixed_ddr | DDR (Canon/Topcon) | 0.6597 | 0.9073 | 0.7459 | 0.9354 | 0.830 | ✓ |
| mixed_odir5k | ODIR-5K (Canon/Zeiss) | 0.4984 | 0.7949 | 0.4025 | 0.7636 | 0.627 | ✗ |
| topcon_messidor2 | Messidor-2 | 0.6968 | 0.9162 | 0.8045 | 0.9651 | 0.876 | ✓ |
| mixed_rfmid (binary) | RFMiD (Topcon/Kowa) | 0.4175 | 0.9632 | — | 0.9632 | 0.525 | ✗ |

Межгрупповая дисперсия: wF1_std = 0.1051, ROC-AUC_std = 0.0554 (n_groups = 5).

**Verdict:** `h6_supported = false`. Ниже пола генерализации 3 из 5 групп (kowa_idrid,
mixed_odir5k, mixed_rfmid).

> Ключевой нюанс: **ROC-AUC остаётся высоким (0.79–0.96)** даже там, где wF1 обваливается.
> Модель сохраняет ранжирующую способность при смене устройства, но теряет калибровку
> порогов — сдвиг проявляется как ошибка порога, а не потеря дискриминации. Это опора для
> честной трактовки: препроцессинг стабилизирует ранжирование (AUC), не мультиклассовую точность.
