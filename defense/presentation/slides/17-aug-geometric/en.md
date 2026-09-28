---
slide: 17
id: aug-geometric
lang: en
status: final
seconds: 20
source: архив сл. 19 — без изменений
terms: [augmentation]
---

# Augmentation: scale and shear

## На слайде

Figure: zoom 0.9 / 1.1 and shear ±2° — extreme samples (dashed — the original field of view) and distributions (`img/aug_geometric_en.png`)

Parameters: zoom — log-uniform [0.9, 1.1], stretch [1/1.05, 1.05]; shear — uniform [−2°, 2°], p = 0.3

## Речь

In training the image is randomly scaled, slightly stretched and sheared. As a result the model learns to grade correctly even when the central region is off-centre or the crop is imprecise.
