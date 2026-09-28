# Figure / Table — сквозная нумерация (en)

Собрано `report/build.py` из `slides/*/en.md`. Не править руками: номера пересчитываются при каждой сборке.

| № | Плашка | Подписи |
|---|---|---|
| 02 | Task 1 | Figure 1 – Registered diabetes patients, 2014–2024<br>Figure 2 – Rural share: population 36 % / ophthalmologists ≈ 10 % |
| 05 | Task 1 | Table 1 – Analysis of existing approaches |
| 06 | Task 2 | Figure 3 – The model as the composition 𝒫 + CNN, Grad-CAM → ALO, two eyes → grade of the worse eye<br>Table 2 – Mathematical formulation and architecture of the model |
| 07 | Task 2 | Table 3 – Experimental design: 2 × 2 factorial |
| 08 | Task 2 | Figure 4 – Top — examples of DR grades 0–4, bottom — grade shares in the five-grade corpora<br>Table 4 – Datasets |
| 09 | Task 2 | Figure 5 – Two donut charts — camera brands in Central Asian clinics and in the training corpora, with a source note below |
| 10 | Task 2 | Figure 6 – Matrix of 7 experiments × 8 corpora; blue — training, green — evaluation without fine-tuning |
| 11 | Task 2 | Figure 7 – One eye (DR03, left) through all 8 stages — the pipeline strip, groups colour-coded |
| 12 | Task 2 | Figure 8 – The left eye — input (disc on the left) and after the flip (disc on the right) |
| 13 | Task 2 | Figure 9 – The detected disc and fovea and the image rotated about the midpoint of the axis, θ = 8.2° |
| 14 | Task 2 | Figure 10 – The baseline stretch (the fundus becomes an ellipse) · stage 2 — isotropic crop · stage 3 — FOV mask |
| 15 | Task 2 | Figure 11 – After cropping → stage 4, flat-field correction (σ = 0.07·D) → stage 5, polar CLAHE |
| 16 | Task 2 | Figure 12 – Uncertainty of the disc and fovea positions · a sample rotated by +σ · angle distribution: adaptive σ = 9.1° vs fallback 13°, clip ±40° |
| 17 | Task 2 | Figure 13 – Zoom 0.9 / 1.1 and shear ±2° — extreme samples (dashed — the original field of view) and distributions |
| 18 | Task 2 | Figure 14 – Original · colour jitter min / max · noise + JPEG (4× zoom) |
| 19 | Task 2 | Figure 15 – The network input — a 4 × 512 × 512 tensor: normalised R, G, B and the mask; x′_c = (x_c − μ_c) / σ_c |
| 20 | Task 3 | Figure 16 – Focal loss (γ = 2 vs cross-entropy) and 5 patient-level folds |
| 21 | Task 3 | Figure 17 – Weighted F1 of the four configurations (A–D, SD over 5 folds); right — EfficientNet-B3, F1 by DR grade |
| 22 | Task 3 | Figure 18 – Stages added one at a time (waterfall, Δ pp); right — optimum of CLAHE (clip factor 2.5, threshold 0.03) and of flat-field (σ/D = 0.07) |
| 23 | Task 3 | Figure 19 – MMD to six corpora — baseline and integrated; at the right Δd [95 % CI] and the KL reduction |
| 24 | Task 3 | Figure 20 – Weighted F1 on EyePACS and APTOS 2019; generalisation ratio G, threshold 0.85 |
| 25 | Task 3 | Figure 21 – ALO by lesion type and the ALO definition<br>Figure 22 – The Grad-CAM pair: baseline · integrated · expert mask, IDRiD_007 — fig. D.1 of the volume |
| 26 | Task 3 | Figure 23 – Weighted F1 on IDRiD and Messidor-2, Δ and 95 % CI; MCID = 0.05 |
| 27 | Task 3 | Figure 24 – Weighted F1 by the five camera groups and the spread between groups |
| 28 | Task 3 | Figure 25 – IDRiD, 5 folds and the Kazakhstani clinical hold-out (n = 60): weighted F1, paired Δ and 95 % CI |
| 29 | Task 4 | Figure 26 – System diagram: doctor ↔ browser client ↔ inference service (𝒫 → CNN → Grad-CAM)<br>Figure 27 – Two screenshots of the browser client: (a) grade, class probabilities and Grad-CAM; (b) preprocessing stages |
| 32 | Task 4 | Figure 28 – Certificate of registration of copyright No. 78109, 04.09.2026 — software package |
| R1 | — | Figure 29 – EfficientNet-B3, F1 by DR grade |
