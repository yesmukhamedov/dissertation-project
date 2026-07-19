# figures_mine/

Generated figures (analogs of Omarov's figures). See `../TASK.md` for the full plan.

**Dataset-illustration figures use IDRiD** (not EyePACS). The grade montage, the
per-class grid, the dataset-contents grid and its distribution CSV are all rebuilt
from the authoritative IDRiD "B. Disease Grading" set (`D:/datasets/IDRiD`, 516
graded images) by `_make_idrid_figures.py`. `fig2_lesion_overlays.png` already
uses IDRiD segmentation groundtruth.

| File                                    | How it is produced                                  | Status |
|-----------------------------------------|-----------------------------------------------------|--------|
| `fig1_1_dr_grades_idrid.png`            | `_make_idrid_figures.py` (1×5 IDRiD grade montage)  | done (IDRiD) |
| `fig1_per_class.png`                    | `_make_idrid_figures.py` (5×4 IDRiD grid)           | done (IDRiD) |
| `fig2_lesion_overlays.png`              | `../scripts/fig2_lesion_overlays.py` (IDRiD masks)  | done (IDRiD) |
| `fig3_dataset_contents.png`             | `_make_idrid_figures.py` (3×5 IDRiD grid + CSV)     | done (IDRiD) |
| `fig4_flowchart.png`                    | draw.io / Excalidraw / Mermaid (manual)             | TODO   |
| `fig5_architecture_artistic.png`        | NN-SVG / PlotNeuralNet (manual)                     | TODO   |
| `fig6_model_graph.png`                  | `../scripts/fig6_model_graph.py` (torchviz/Netron)  | TODO   |
| `fig7_pr_curves.png`                    | `../scripts/fig7_pr_curves.py` (needs `predictions.npz`) | TODO |
| `fig8_training_curves.png`              | `../scripts/copy_ready_figures.py` (copies `exp1/19_*`) | ready as `exp1/19_training_curves.png` |
| `fig9_confusion_matrix.png`             | `../scripts/copy_ready_figures.py` (copies `exp1/20_*`) | ready as `exp1/20_confusion_matrix.png` |
| `fig10_webapp_screenshot_1.png`         | Manual screenshot of the **top** of the demo page (upload form + walk-through cases + Run inference button) | TO RENAME from `image copy.png` |
| `fig10_webapp_screenshot_2.png`         | Manual screenshot of the **bottom** of the demo page (Model result + Per-eye prediction + Grad-CAM/attention + Confirm/Reject + Relabeling buffer) | TO RENAME from `image.png` |

## Renaming the current screenshots

```powershell
# from PowerShell in this folder:
Rename-Item ".\image copy.png" "fig10_webapp_screenshot_1.png"
Rename-Item ".\image.png"      "fig10_webapp_screenshot_2.png"
```

## Language policy

All generated images and scripts use **English only** (labels, captions, titles, comments). This matches the language used in the rest of the demo (`demo/src/tabs/*.js` defaults to English).
