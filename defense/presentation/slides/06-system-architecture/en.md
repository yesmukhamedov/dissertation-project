---
slide: 06
id: system-architecture
lang: en
status: draft
seconds: 45
source: архив сл. 7 — переработан (таблица исправлена, диаграмма та же; добавлена математическая постановка)
terms: [preprocessing_pipeline, focal_loss, fov_mask, backbone, referable_dr, grad_cam, alo]
---

# Mathematical formulation and architecture of the model

## На слайде

Figure: the model as the composition 𝒫 + CNN, Grad-CAM → ALO, two eyes → grade of the worse eye (`img/model_en.png`)

| # | Block | Content |
|---|---|---|
| 1 | Input | fundus image, left / right eye (s) |
| 2 | Preprocessing 𝒫 | 8 stages; deterministic at inference, stages 5–6 stochastic in training; output — 4 × 512 × 512 tensor (RGB + field-of-view mask) |
| 3 | CNN backbone | ResNet-50 (23.5 M) or EfficientNet-B3 (10.7 M), 4-channel first layer |
| 4 | Classification | softmax, K = 5 grades; referral: ŷ ≥ 2 |
| 5 | Patient level | the patient's grade is the grade of the worse eye: ŷ = max(ŷ_left, ŷ_right) |
| 6 | Interpretation | Grad-CAM (post hoc) → ALO, IoU |

**Mathematical formulation**

- 𝒫 = T₇ ∘ … ∘ T₀ : (I, s) ↦ x ∈ ℝ^(4×512×512)  (1)
- ŷ = argmax_k softmax(CNN_θ(𝒫(I, s)))_k, k ∈ {0, …, 4}; referral: ŷ ≥ 2  (2)
- θ* = argmin_θ Σᵢ FL_γ(CNN_θ(𝒫(Iᵢ, sᵢ)), yᵢ), γ = 2 — 𝒫 belongs to the model, not to the data  (3)
- ALO = |A ∩ L| / |L|, where A is the Grad-CAM attention area and L the lesion mask  (4)

## Речь

Formally the model is a composition: the network is applied to the pipeline output and its parameters are trained on that output, so the pipeline belongs to the definition of the model. The input image first passes the eight-stage pipeline: deterministic at inference, with stochastic contrast and augmentation in training. The output is a four-channel tensor: three colour channels and the field-of-view mask. The network returns one of five grades, with referral from grade two. The patient's grade is that of the worse eye, and Grad-CAM gives the attention map.
