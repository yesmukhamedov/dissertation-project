---
slide: 18
id: crop-fov-mask
lang: en
status: final
seconds: 20
source: архив сл. 16 — без изменений
terms: [fov_crop, fov_mask, isotropic_scaling]
---

# Crop & resize, field-of-view (FOV) mask

## На слайде

Figure: stage 2 card (`img/a16_1.png`); cropped image and field-of-view mask

## Речь

At this stage the black borders around the image are cropped, leaving only the circular fundus region. The image is scaled isotropically, without distorting proportions, to 512 by 512. The field-of-view mask is fed to the network as a separate fourth channel, so the model knows explicitly where the valid pixels are.
