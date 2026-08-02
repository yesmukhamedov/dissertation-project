# exp4 — classification of the two arms (EfficientNet-B4, fold 0)

The trained arms on which the H-5 Grad-CAM analysis is built: baseline (3ch) against full pipeline
(4ch), EfficientNet-**B4**, a single fold. Best epoch by weighted-F1.
Source: the **2026-08-02** run (`VALUES.md` §5.6).

| Arm | best epoch | Weighted F1 | ROC-AUC | κ (quad) | Accuracy |
|-----|-----------:|------------:|--------:|---------:|---------:|
| baseline (3ch) | 17 | 0.7545 | 0.8307 | 0.6602 | 0.7569 |
| full pipeline (4ch) | 19 | **0.7766** | **0.8542** | **0.7075** | **0.7827** |
| **Δ (full − baseline)** | — | **+0.0221** | **+0.0235** | **+0.0473** | **+0.0258** |

**Observation.** On EfficientNet-B4 the pipeline beats baseline on all four metrics: +2.2 pp F1,
+0.024 AUC, +0.047 κ, +2.6 pp accuracy.

**Relation to exp1.** The gain here is noticeably **smaller** than on EfficientNet-B3 in exp1
(+6.55 pp F1, `TAB-4.2_exp1_factorial.md`). There are three protocol differences: a different backbone
(B4 vs B3), **one fold instead of five** (no averaging, no std), and a separate exp4 training
configuration. The magnitudes are therefore not directly comparable — the table shows the
**direction** of the effect on an independent backbone, not its size. Carry it into the text as
confirmation of consistency (the pipeline also wins on B4), without comparing absolute Δ values with exp1.

**Relation to H-5.** Both arms on which ALO/IoU were measured (`TAB-4.7_exp4_alo_iou.md`) differ in
classification as well as in attention alignment. The gain appears simultaneously along both
channels — the discriminative and the localizational — which makes the interpretation coherent:
improved classification is accompanied by improved spatial anchoring of attention.

**Caveats.** A single fold (fold 0), without cross-validation → no std; EfficientNet-B4 was chosen
per the H-5 specification for Grad-CAM, not per exp1; the initialization of the arms follows the exp4
configuration (keep CFC-2.8 in mind when interpreting).
