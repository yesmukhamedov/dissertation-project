---
slide: 19
id: normalization
lang: en
status: final
seconds: 15
source: архив сл. 21 — без изменений
terms: [dataset_normalization]
---

# Dataset-specific normalisation

## На слайде

Figure: the network input — a 4 × 512 × 512 tensor: normalised R, G, B and the mask; x′_c = (x_c − μ_c) / σ_c (`img/normalize_en.png`)

**Bottom (italic):** *Published: Yesmukhamedov N.S. et al. // Herald of KBTU, 2025 [KOKSNVO]*

## Речь

This is the last stage of the pipeline: pixel values are normalised by the mean and deviation computed over valid fundus pixels. The statistics come only from the training corpus and are never recomputed on a target corpus. The tensor is then passed to the network.
