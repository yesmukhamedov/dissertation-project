---
slide: 32
id: practical-significance
lang: en
status: draft
seconds: 35
source: архив сл. 36 — переработан (рисунок TELEMED оставлен)
terms: [practical, screening_system, inference_service]
---

# Practical significance

## На слайде

Figure: telemedicine screening scheme (`img/a36_1.png`)

1. **A fully specified preprocessing regime** — code in Appendix A; parameters are re-tuned for each corpus
2. **Screening system:** inference service + browser client, 8 modules; the same pipeline code as in the experiments; stage-by-stage visualisation and Grad-CAM; demonstrator at dr-classification.pages.dev
3. **On consumer hardware:** RTX 3060 12 GB; the 4th channel adds only **+0.9 %** FLOPs and **+24 MiB** memory
4. **An intake protocol for external images** and applicability to national screening
5. **Copyright certificate No. 78109** (04.09.2026) — the software package

## Речь

In practice: first, a preprocessing regime with its full code, whose parameters are re-tuned per corpus. Second, a screening system: the inference service and browser client use the same pipeline code as the experiments and show every stage and the attention map. It runs on a consumer graphics card, and the fourth channel adds under one percent of compute. A copyright certificate was obtained. A clinical field trial is the next step.
