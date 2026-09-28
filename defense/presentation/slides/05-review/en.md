---
slide: 05
id: review
lang: en
status: draft
seconds: 35
source: архив сл. 5 — переработан
terms: [preprocessing, domain_shift, grad_cam]
---

# Analysis of existing approaches

## На слайде

| Direction | What is done | Gap |
|---|---|---|
| Architectural (ensembles, CNN+ViT, attention) | accuracy grows through architectural complexity | preprocessing is neither controlled nor reported |
| Preprocessing (CLAHE, normalisation) | data preparation; default parameters | no ablation, parameters not formalised |
| Cross-corpus transfer | adaptation on target-domain data | the mechanism is not measured, only its consequence |
| Interpretability (Grad-CAM) | qualitative heat maps | no quantitative measure of agreement with annotation |
| Deployed systems [58], [62] | prospective trials (sensitivity 87.2 %, specificity 90.7 %) | preprocessing not disclosed |

**Common practice:** 𝒫(I) → data → ŷ = CNN(data)   **Proposed:** ŷ = CNN_θ(𝒫(I)), 𝒫 a model component

**Bottom (italic):** *Published: Sapakova S.Z. et al. // Вестник КазУТБ, 2025 [KOKSNVO]*

## Речь

Existing work was analysed along five directions. Most raise accuracy through architectural complexity and apply preprocessing with default parameters and no ablation; the transfer mechanism is not measured; interpretability stops at qualitative maps; deployed systems do not disclose preprocessing. So preprocessing is written into the model expression and its effect is tested in a controlled experiment.
