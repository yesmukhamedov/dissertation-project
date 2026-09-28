---
slide: 11
id: pipeline-overview
lang: en
status: final
seconds: 25
source: архив сл. 13 — без изменений
terms: [preprocessing_pipeline, fov_mask]
---

# Preprocessing stages: input

## На слайде

Figure: one eye (DR03, left) through all 8 stages — the pipeline strip, groups colour-coded (`img/strip_en.png`)

## Речь

The slide groups the eight preprocessing stages by function: green — four geometric stages, orange — two photometric stages, dashed purple — augmentation, used only in training, red — normalisation and mask append. The pipeline outputs three RGB channels and a binary field-of-view mask.
