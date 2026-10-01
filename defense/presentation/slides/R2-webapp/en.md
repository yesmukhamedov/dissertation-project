---
slide: R2
id: webapp
lang: en
status: draft
seconds: 30
source: new (2026-09-30) — reserve after "Limitations", the web application dr-classification.pages.dev
terms: [screening_system, inference_service, grad_cam]
---

# Web application: dr-classification.pages.dev

## На слайде

Figure: three screens of the web application: (a) uploading both eyes of one patient; (b) grade, class probabilities and Grad-CAM; (c) the doctor's confirmation and the relabelling buffer (`img/app_upload.png`, `img/app_result_en.png`, `img/app_confirm.png`)

1. **Runs in the browser:** nothing to install; Kazakh and English interface
2. **Workflow:** images of both eyes → preprocessing stages → grade, probabilities, attention map
3. **The doctor decides:** confirms or corrects the result; corrections collect in a buffer for retraining
4. **Inference** — on an RTX 3060 GPU server through a Cloudflare tunnel; a research prototype, not a medical device

## Речь

The system's web application runs at dr-classification.pages.dev. The doctor uploads images of both eyes of a patient, sees the preprocessing stages, the grade and the attention map, and then confirms or corrects the result. Corrections are collected for retraining the model. It is a research prototype, not a medical device.
