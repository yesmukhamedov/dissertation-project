---
slide: 04
id: provisions
lang: en
status: draft
seconds: 75
source: новый слайд + архив сл. 34 (новизна) — объединены по образцу Базарбекова (сл. 4)
terms: [provisions, novelty, preprocessing_pipeline, fov_mask, clip_limit, alo, screening_system]
---

# Provisions submitted for defence

## На слайде

**Scientific novelty:** for the first time, fundus image preprocessing is formalised as a component of the diagnostic model, ŷ = CNN_θ(𝒫(I)), and studied in a controlled factorial experiment: an eight-stage pipeline with a field-of-view mask as the fourth channel and a CLAHE clip limit defined as the minimum of two constraints is proposed, together with an asymmetric measure of agreement between model attention and expert annotation (ALO); the integrated model raises weighted F1 by 6.5 pp on both architectures studied.

**Provisions submitted for defence:**
1. An eight-stage preprocessing pipeline for colour fundus images, formalised as a component of the diagnostic model and reducing differences between images in orientation, geometry, illumination and camera
2. An integrated "preprocessing pipeline + convolutional neural network" model with a four-channel input (RGB + field-of-view mask) for five-class diagnosis of diabetic retinopathy that improves accuracy on both architectures studied
3. An asymmetric measure of agreement between model attention and expert lesion annotation (ALO) for quantitative assessment of interpretability
4. A software system for diabetic retinopathy screening that reproduces the experimental pipeline and visualises the processing stages and attention maps

## Речь

The scientific novelty: for the first time, fundus image preprocessing is formalised as a model component and studied in a controlled factorial experiment.
Four provisions are submitted for defence. First, the eight-stage preprocessing pipeline as a model component; it reduces differences between images in orientation, geometry, illumination and camera, as the ablation and the experiments on external corpora show. Second, the integrated model with a four-channel input; its advantage over the baseline holds on both architectures studied. Third, the ALO measure, which compares model attention with expert annotation. Fourth, the screening system, for which a copyright certificate has been obtained.
