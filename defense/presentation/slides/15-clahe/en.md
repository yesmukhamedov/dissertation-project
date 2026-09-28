---
slide: 15
id: clahe
lang: en
status: draft
seconds: 30
source: архив сл. 17 — изменён: GIF удалён, добавлен этап 4 (коррекция освещённости)
terms: [flat_field, clahe, clip_limit]
---

# Flat-field correction and adaptive CLAHE

## На слайде

Figure: after cropping → stage 4, flat-field correction (σ = 0.07·D) → stage 5, CLAHE (`img/stages45_en.png`)

**Bottom (italic):** *Published: Sapakova S., Yesmukhamedov N., Sapakov A. // Eastern-European J. of Enterprise Technologies, 2025 [Scopus Q3]*

## Речь

Stage four evens out the illumination: a blurred copy of the image is subtracted from it, with the blur scale at 0.07 of the field-of-view diameter, so the correction is the same at any resolution. Stage five is CLAHE. CLAHE is a local contrast enhancement method, applied to the lightness channel of LAB space. The clip limit is computed as the minimum of two constraints — histogram- and tile-relative — and is applied stochastically in training. After processing, fine vessels and microaneurysms are clearly distinguishable — the key signs of early retinopathy.
