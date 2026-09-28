---
slide: 24
id: exp3
lang: en
status: final
seconds: 30
source: архив сл. 26 — без изменений
terms: [generalization_ratio, zero_shot, cross_corpus_transfer]
---

# Experiment 3: transfer to another dataset

## На слайде

Figure: weighted F1 on EyePACS and APTOS 2019; generalisation ratio G, threshold 0.85 (`img/exp3_en.png`)

## Речь

In the third experiment the model trained on EyePACS was tested on APTOS 2019 without any retraining. Weighted F1 of the integrated configuration is 0.735, of the baseline 0.647 — a difference of 0.089 whose interval excludes zero. The generalisation ratio is 0.898 against 0.858. Both configurations pass the 0.85 threshold, so the evidence lies not in the threshold but in the comparison: on an unseen corpus the integrated configuration is higher.
