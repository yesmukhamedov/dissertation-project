---
slide: 22
id: exp2
lang: en
status: final
seconds: 40
source: архив сл. 25 — без изменений
terms: [ablation, flat_field, clahe, clip_limit]
---

# Experiment 2: ablation of pipeline stages

## На слайде

Figure: left — stages added one at a time (waterfall, Δ pp); right — optimum of CLAHE (clip factor 2.5, threshold 0.03) and of flat-field (σ/D = 0.07) (`img/exp2_en.png`)

## Речь

The second experiment adds the stages in turn under a single initialisation. F1 rises from 0.754 to 0.819 monotonically in each of the five folds — the first experiment's gain is fully reproduced by preprocessing. Every step exceeds noise; illumination correction and CLAHE contribute most, 41 percent together. Their parameters have an interior optimum: clip factor 2.5, threshold 0.03, correction scale 0.07. The main configurations were trained at 2.0 and 0.01 — off the optimum, so the result is not inflated by tuning.
