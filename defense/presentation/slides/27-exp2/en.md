---
slide: 27
id: exp2
lang: en
status: final
seconds: 35
source: архив сл. 25 — без изменений
terms: [ablation, flat_field, clahe, clip_limit]
---

# Experiment 2: H-2 — ablation of pipeline components

## На слайде

Figures: cumulative ablation, marginal stage contributions, CLAHE parameter sensitivity map for DR1 / DR2 (`img/a25_*.png`)

## Речь

The second experiment adds the stages in turn under a single initialisation. F1 rises from 0.754 to 0.819 monotonically in each of the five folds — the first experiment's gain is fully reproduced by preprocessing. Every step exceeds noise; illumination correction and CLAHE contribute most, 41 percent together. Their parameters have an interior optimum: clip factor 2.5, threshold 0.03, correction scale 0.07.
