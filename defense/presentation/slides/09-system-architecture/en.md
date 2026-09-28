---
slide: 09
id: system-architecture
lang: en
status: draft
seconds: 35
source: архив сл. 7 — переработан (таблица исправлена, диаграмма та же)
terms: [preprocessing_pipeline, fov_mask, backbone, referable_dr, grad_cam, alo]
---

# Overall architecture of the model

## На слайде

Figure: left — architecture diagram (`img/a07_1.png`, from the archive)

| # | Block | Content |
|---|---|---|
| 1 | Input | fundus image, left / right eye (s) |
| 2 | Preprocessing 𝒫 | 8 stages; deterministic at inference, stages 5–6 stochastic in training; output — 4 × 512 × 512 tensor (RGB + field-of-view mask) |
| 3 | CNN backbone | ResNet-50 (23.5 M) or EfficientNet-B3 (10.7 M), 4-channel first layer |
| 4 | Classification | softmax, K = 5 grades; referral: ŷ ≥ 2 |
| 5 | Patient level | the two eyes' results are combined into one patient decision |
| 6 | Interpretation | Grad-CAM (post hoc) → ALO, IoU |

**Central idea:** ŷ = CNN_θ(𝒫(I, s)) — 𝒫 is an integral part of the expression

## Речь

The input image first passes the eight-stage pipeline: deterministic at inference, with stochastic contrast and augmentation in training. The output is a four-channel tensor: three colour channels and the field-of-view mask. The network returns one of five grades, with referral from grade two. The two eyes are combined at patient level, and Grad-CAM gives the attention map.
