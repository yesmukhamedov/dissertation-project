# A7 — Вычислительные бенчмарки (params / FLOPs / latency / VRAM)

Замерено 2026-07-28 18:50:31 на **NVIDIA GeForce RTX 3060** (torch 2.5.1+cu121, CUDA 12.1), вход 512×512, fp32-инференс, 50 итераций после 10 прогревочных.

| Config | Модель | Ch | Params | GFLOPs/изобр. | Latency bs=1 (мс) | Latency bs=16 (мс/изобр.) | Throughput bs=16 (изобр./с) | VRAM инференс bs=16 (МиБ) | VRAM train-step bs=16 (МиБ) | AMP при обучении |
|---|---|---|---|---|---|---|---|---|---|---|
| A | resnet50 | 3 | 23.52M | 42.7 | 10.5 | 8.2 | 121.6 | 978.1 | 3724.4 | да |
| B | resnet50 | 4 | 23.52M | 43.1 | 10.5 | 8.3 | 120.5 | 1002.2 | 3747.5 | да |
| C | efficientnet_b3 | 3 | 10.70M | 10.0 | 12.8 | 7.5 | 132.8 | 1515.0 | 13726.1 | нет |
| D | efficientnet_b3 | 4 | 10.70M | 10.1 | 14.5 | 7.6 | 132.3 | 1531.0 | 13742.1 | нет |

FLOPs — прямой проход на одно изображение, `torch.utils.flop_counter` (умножение-сложение считается за 2 операции). VRAM — `torch.cuda.max_memory_allocated`; train-step = fwd+bwd+optimizer.step с тем же mixed-precision, с каким конфигурация обучалась.
