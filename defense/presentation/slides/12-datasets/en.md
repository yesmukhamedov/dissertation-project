---
slide: 12
id: datasets
lang: en
status: draft
seconds: 35
source: архив сл. 10 — переработан (рисунки те же, добавлена таблица корпусов)
terms: [corpus, icdr, class_imbalance]
---

# Datasets

## На слайде

Figures: DR 0–4 examples, class distribution (`img/a10_1.png`), corpus comparison (`img/a10_2.png`)

| Corpus | Group | Role | Size | Camera |
|---|---|---|---|---|
| EyePACS | training | tuning, in-domain evaluation | ~35,126 | Canon CR-1 |
| APTOS 2019 | external | cross-corpus transfer | ~3,662 | mixed |
| Messidor-2 | external | external clinical performance | ~1,748 | Topcon TRC-NW6 |
| IDRiD | clinical | attention alignment, small sample | 516 (81 with masks) | Kowa VX-10α |
| Kazakhstan clinical | clinical | held-out test | 60 | — |
| DDR / ODIR-5K / RFMiD | device | camera shift | ~13,673 / ~5,000 pat. / ~3,200 | Canon, Topcon, Zeiss, Kowa |

8 corpora · 4 camera manufacturers · DR 0 dominates EyePACS → focal loss, weighted F1

## Речь

The eight corpora are grouped by their role in the evidence. Training uses EyePACS only. On APTOS and Messidor-2 the model is tested without retraining. IDRiD is the only corpus with lesion masks; the Kazakhstan clinical set has sixty images. The three device corpora come from cameras absent in training. EyePACS is dominated by the healthy grade — hence focal loss and weighted F1.
