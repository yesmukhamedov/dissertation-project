---
slide: 25
id: training-metrics
lang: en
status: final
seconds: 30
source: архив сл. 23 — без изменений
terms: [focal_loss, patient_level_cv, weighted_f1, roc_auc, kappa, generalization_ratio, alo]
---

# Training parameters: focal loss, optimiser, 5-fold CV; metrics: F1, AUC, Cohen's κ, G, ALO

## На слайде

Figures: 5-fold split diagram, focal loss, definitions of F1/κ, AUC, G, ALO (`img/a23_*.png`)

## Речь

Evaluation uses patient-level stratified 5-fold cross-validation, which closes data leakage. The classes are imbalanced, so the loss is inverse-frequency-weighted focal loss. The primary metric is weighted F1, then AUC and quadratic kappa; on external corpora, the generalisation ratio G; for attention, ALO.
