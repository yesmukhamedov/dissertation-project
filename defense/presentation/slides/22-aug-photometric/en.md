---
slide: 22
id: aug-photometric
lang: en
status: final
seconds: 20
source: архив сл. 20 — без изменений
terms: [augmentation, color_jitter]
---

# Augmentation: colour, brightness and contrast

## На слайде

Figures: min / max examples and distributions (`img/a20_*.png`)

## Речь

This augmentation slightly and randomly changes the colour channels, brightness and contrast. Since every camera renders colour a little differently, the model learns to rely not on colour but on the structural features of the retina. Light and colour are the most variable acquisition factor, so this is the strongest part of the augmentation.
