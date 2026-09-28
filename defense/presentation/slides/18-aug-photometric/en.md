---
slide: 18
id: aug-photometric
lang: en
status: final
seconds: 25
source: архив сл. 20 — без изменений
terms: [augmentation, color_jitter]
---

# Augmentation: colour, brightness, contrast, noise

## На слайде

Figure: original · colour jitter min / max · noise + JPEG (4× zoom) (`img/aug_photometric_en.png`)

Parameters: brightness, contrast, saturation ×[0.9, 1.1], hue ±0.02 (each p = 0.5); noise σ = 2–6 (p = 0.15); JPEG q = 70–100 (p = 0.2)

## Речь

This augmentation slightly and randomly changes the colour channels, brightness and contrast. Since every camera renders colour a little differently, the model learns to rely not on colour but on the structural features of the retina. In addition, noise and JPEG compression are added with a small probability — as with an inexpensive camera and an image sent over a network. Light and colour are the most variable acquisition factor, so this is the strongest part of the augmentation.
