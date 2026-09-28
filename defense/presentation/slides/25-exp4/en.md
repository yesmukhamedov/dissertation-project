---
slide: 25
id: exp4
lang: en
status: final
seconds: 35
source: архив сл. 27 — без изменений
terms: [alo, grad_cam, attention_alignment, lesion_types]
---

# Experiment 4: interpretability (ALO, Grad-CAM)

## На слайде

Figures: left — ALO by lesion type and the ALO definition (`img/exp4_en.png`); right — Grad-CAM comparison (`img/a27_2.png` — ⚠ old run, re-capture from the Config D checkpoint)

## Речь

The fourth experiment compares model attention with the expert masks of IDRiD. ALO is the fraction of a lesion covered by attention; it is asymmetric because lesion coverage is what matters clinically. In the integrated configuration ALO is higher for all four types by 0.099–0.129, p below 0.015, regardless of threshold. This is alignment of attention with annotation, not localisation.
