---
slide: 05
id: novelty
lang: en
status: draft
seconds: 45
source: архив сл. 34 — переработан и перенесён во вводный блок
terms: [novelty, preprocessing_pipeline, clip_limit, fov_mask, flat_field, alo, domain_distance]
---

# Scientific novelty

## На слайде

1. **Conceptual:** preprocessing is moved from ancillary preparation to a component of the diagnostic model, ŷ = CNN_θ(𝒫(I)), and put into a controlled experimental contrast
2. **Engineering:** five elements combined for the first time — isotropic scaling with centred padding; field-of-view mask as a fourth channel; illumination correction scaled to each image's geometry and applied only inside the mask; channel statistics over valid fundus pixels; canonical orientation whose augmentation spread follows landmark-localisation uncertainty. The clip limit is the **minimum of two constraints** (histogram- and tile-relative), stochastic at training
3. **Metrological:** an **asymmetric overlap measure** between model attention and expert annotation (ALO); **direct measurement of the distance** from the source to the target domains — the mechanism is measured, not inferred
4. **Analytical:** widely used transfer measures (G, Δ_drop) are shown to penalise a configuration for its in-domain strength

## Речь

The novelty lies on four levels. The main one is conceptual: preprocessing as a model component became an object of experiment. In engineering terms, five pipeline elements are combined for the first time and the clip limit is formalised as the minimum of two constraints. Metrologically, an asymmetric measure of attention alignment is proposed and domain distance is measured directly. Analytically, widely used transfer measures are shown to be non-neutral.
