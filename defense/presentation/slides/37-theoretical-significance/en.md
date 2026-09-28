---
slide: 37
id: theoretical-significance
lang: en
status: draft
seconds: 25
source: архив сл. 35 — переработан
terms: [theoretical, alo, domain_distance, generalization_ratio]
---

# Theoretical significance

## На слайде

1. **The full specification of a model changes:** preprocessing is a mandatory part of the model specification; comparing without it compares partly unknown systems
2. **Informal choices are formalised:** the clip limit (minimum of two constraints), the illumination-correction scale (σ = 0.07·D)
3. **Attention alignment as asymmetric overlap (ALO):** Grad-CAM turns from a qualitative picture into a measure
4. **The mechanism is measured:** domain distance is measured directly at the penultimate layer, not inferred from external accuracy
5. **Transfer measures are not neutral:** G and Δ_drop penalise a configuration for its in-domain strength

## Речь

The theoretical significance lies in how the problem is posed and measured. Bringing preprocessing into the model changes what counts as a full model specification and a fair comparison, and five previously informal choices became explicit and testable.
