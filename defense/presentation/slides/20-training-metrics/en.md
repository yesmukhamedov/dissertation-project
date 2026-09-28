---
slide: 20
id: training-metrics
lang: en
status: final
seconds: 38
source: архив сл. 23 — без изменений
terms: [focal_loss, patient_level_cv, weighted_f1, roc_auc, kappa, generalization_ratio, alo]
---

# Training parameters: focal loss, optimiser, 5-fold CV; metrics: F1, AUC, Cohen's κ, G, ALO

## На слайде

Figure: focal loss (γ = 2 vs cross-entropy) and 5 patient-level folds (`img/training_en.png`)

- Metrics: weighted F1 (primary), AUC, quadratic κ
- On external corpora: G = F1_ext / F1_EyePACS (threshold 0.85); attention: ALO = |A ∩ L| / |L|

## Речь

Seven experiments and the domain-distance measurement test seven hypotheses; the acceptance criterion of each was fixed before its experiment started. Evaluation uses patient-level stratified 5-fold cross-validation, which closes data leakage. The classes are imbalanced, so the loss is inverse-frequency-weighted focal loss. The primary metric is weighted F1, then AUC and quadratic kappa; on external corpora, the generalisation ratio G; for attention, ALO.
