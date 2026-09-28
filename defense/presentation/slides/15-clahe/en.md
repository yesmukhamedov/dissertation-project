---
slide: 15
id: clahe
lang: en
status: draft
seconds: 35
source: архив сл. 17 — изменён: GIF удалён, добавлен этап 4 (коррекция освещённости)
terms: [flat_field, clahe, clip_limit]
---

# Flat-field correction and polar CLAHE

## На слайде

Figure: after cropping → stage 4, flat-field correction (σ = 0.07·D) → stage 5, polar CLAHE (`img/stages45_en.png`)

**Bottom (italic):** *Published: Sapakova S., Yesmukhamedov N., Sapakov A. // Eastern-European J. of Enterprise Technologies, 2025 [Scopus Q3]*

## Речь

Stage four evens out the illumination: a blurred copy is subtracted from the image, at a scale of 0.07 of the field-of-view diameter. Stage five is polar CLAHE: contrast is enhanced locally in rings and sectors around the fovea, finer where vessels are denser; the clip limit is the minimum of two constraints. Fine vessels and microaneurysms — the early signs of retinopathy — become clearly visible.
