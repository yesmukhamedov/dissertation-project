---
slide: 15
id: pipeline-overview
lang: en
status: final
seconds: 25
source: архив сл. 13 — без изменений
terms: [preprocessing_pipeline, fov_mask]
---

# Preprocessing stages: input

## На слайде

Figure: vertical diagram of the 8 stages (`img/a13_1.png`); input images DR03 right / DR03 left

## Речь

The slide groups the eight preprocessing stages by function: green — four geometric stages, orange — two photometric stages, dashed purple — augmentation, used only in training, red — normalisation and mask append. The pipeline outputs three RGB channels and a binary field-of-view mask.
