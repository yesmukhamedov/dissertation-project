---
slide: 23
id: normalization
lang: en
status: final
seconds: 15
source: архив сл. 21 — без изменений
terms: [dataset_normalization]
---

# Dataset-specific normalisation

## На слайде

Figure: stage 7 card (`img/a21_1.png`); right / left after normalisation

## Речь

This is the last stage of the pipeline: pixel values are normalised by the mean and deviation computed over valid fundus pixels. The statistics come only from the training corpus and are never recomputed on a target corpus. The tensor is then passed to the network.
