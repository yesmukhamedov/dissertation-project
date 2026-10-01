---
slide: 29
id: screening-system
lang: en
status: draft
seconds: 35
source: архив сл. 36 — переработан в слайд системы (рисунок TELEMED оставлен; скриншоты клиента сняты 2026-09-29)
terms: [screening_system, inference_service, grad_cam, fov_mask]
---

# Screening system

## На слайде

Figures: left — system diagram: doctor ↔ browser client ↔ inference service (𝒫 → CNN → Grad-CAM) (`img/system_en.png`); right — two screenshots of the browser client: (a) grade, class probabilities and Grad-CAM; (b) preprocessing stages (`img/ui_1_g4_en.png`, `img/ui_2_g4_en.png` — captured from the live demo 2026-09-30, EyePACS patient 294: both eyes DR4)

1. **Inference service + browser client**, 8 modules; the same pipeline code as in the experiments
2. **Shows every step:** preprocessing stages, grade, Grad-CAM attention map; the clinician confirms or corrects the decision
3. **On consumer hardware:** RTX 3060 12 GB; the 4th channel adds only **+0.9 %** FLOPs and **+24 MiB** memory
4. **Demonstrator:** dr-classification.pages.dev

**Bottom (italic):** *Published: Yesmukhamedov N.S. et al. // News of NAN RK, 2025 [KOKSNVO]*

## Речь

The fourth result is the screening system. The inference service and the browser client use the same pipeline code as the experiments, so the clinician works with exactly the model we evaluated. The client shows every preprocessing stage, the grade and the attention map, and the clinician confirms or corrects the decision. The system runs on a consumer graphics processor, and the fourth channel adds less than one per cent of computation. A field clinical trial is the next step.
