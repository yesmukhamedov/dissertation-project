---
slide: 07
id: factorial-design
lang: en
status: draft
seconds: 40
source: архив сл. 8 — переработан
terms: [factorial_design, baseline_configuration, integrated_configuration, weighted_f1, focal_loss, patient_level_cv]
---

# Experimental design: 2 × 2 factorial

## На слайде

No figure: the 2 × 2 table is the main element (the 4-channel first layer is on the figure of slide 06)

| | ResNet-50 | EfficientNet-B3 |
|---|---|---|
| **Baseline**: stretch to 512 × 512 + ImageNet normalisation, 3 channels | A | C |
| **Integrated**: 8-stage pipeline, 4 channels | B | D |

- Fixed training: Adam 1·10⁻⁴, batch 16, 20 epochs (early stopping 5), focal loss γ = 2, 5 patient-level folds, seed 42
- Dominance criterion (fixed in advance): ΔF1 ≥ 5 pp **and** ΔAUC ≥ 0.02 **and** no drop in κ
- Evaluation: DeLong, McNemar + Holm correction, mixed-effects ANOVA (arm × architecture)

## Речь

The main experiment is a two-by-two factorial: preprocessing is baseline or eight-stage, the architecture is ResNet-50 or EfficientNet-B3. The four cells are trained identically on five patient-level folds, so the difference reads as the factor's effect. The dominance criterion was fixed in advance: at least five percentage points in F1, 0.02 in AUC, no drop in kappa. The baseline is not a copy of a published system but an internal reference point.
