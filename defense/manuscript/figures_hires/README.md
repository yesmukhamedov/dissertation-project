# figures_hires — print-resolution artwork for the KJS submission

Companion to `../figures/` (the images extracted as-is from `Article manuscript_01.docx`).
Nothing in `../figures/` is modified or deleted; this folder holds only new, higher-quality files.

Resolution targets come from `../KJS_TEMPLATE.md` §7 (Elsevier artwork instructions):
vector EPS/PDF is preferred and carries no resolution requirement; bitmap line drawings need
≥ 1000 dpi, combined line/halftone ≥ 500 dpi, photographs and other halftones ≥ 300 dpi.

## Regenerated here

| File | Content | Format | Size | Status |
|---|---|---|---|---|
| `Figure_1.pdf` / `.png` | End-to-end system pipeline (Fig. 1) | vector PDF + PNG | 3725 × 7958 px at 85 mm wide ≈ **1113 dpi** | ✅ meets the 1000 dpi line-drawing threshold |
| `Figure_3.pdf` / `.png` | EfficientNet-B3 backbone (Fig. 3) | vector PDF + PNG | 7520 × 2480 px at 190 mm wide ≈ **1005 dpi** | ✅ meets the 1000 dpi line-drawing threshold |

Both are redrawn from scratch by `make_figures.py`; **submit the PDF versions** — they are vector and
scale without loss. The PNGs are provided only as a fallback for systems that reject PDF artwork.

Changes made while redrawing (content unchanged):
- The in-figure title of Fig. 3 ("EfficientNet-B3 (Config D) — 4-channel Diabetic Retinopathy
  Classifier") was **removed**: the guide requires the figure title to live in the caption, not on
  the image.
- Fig. 3 colour coding and legend were made consistent — in the original, MBConv1 was drawn in the
  "input/stem" colour and MBConv5–7 in a colour absent from the legend.
- ASCII arrows `->` in Fig. 1 replaced with `→`; typeface matched to the manuscript (Times New Roman).

## NOT regenerated — source material is missing

| Fig. | Content | Why it cannot be regenerated here | What is needed |
|---|---|---|---|
| 2 | Representative fundus photographs, DR0–DR4 | Requires the source images from `E:/datasets/` (EyePACS); that drive is not mounted on this machine, and the identity of the exact frames used is not recorded | Mount the dataset drive and re-export the montage at ≥ 300 dpi; note that different representative frames would change the figure content |
| 4 | Validation loss and weighted F1 over 20 epochs, Config A/C/D | The per-epoch training history behind these curves is **not present in the repository** — see the note below | The original run's `metrics.csv` (or equivalent history) for the Config A/C/D 20-epoch run |
| 5 | Normalised confusion matrices, Config C and D | The full 5 × 5 matrices are not recorded anywhere; the manuscript reports only the DR3 and DR4 diagonals | The run's saved predictions for the held-out test split |
| 6 | Per-class precision–recall curves | Only the AP scalars are recorded, not the curves | The run's saved prediction scores |
| 7 | Dashboard image-intake screen | A screenshot of the live application | Re-capture from a running demo at ≥ 300 dpi (e.g. 2× device pixel ratio) |
| 8 | Dashboard results screen | A screenshot of the live application | Re-capture as above. **Caveat:** the caption and §3.3 quote specific on-screen values (confidence 76.3 %, latency 397 ms); a new capture will show different values, so the text must be updated to match |

### Note on the missing run artifacts (Fig. 4–6)

The manuscript reports validation loss 0.39 / 0.42 / 0.32 and weighted F1 0.73 / 0.72 / 0.77 at
epoch 20 for Config A / C / D. No file under `experiments/outputs/` reproduces those values:
`outputs/exp1/metrics.csv` is a different run, the `backup_exp1_*` histories differ, and the Kaggle
Config-D run is APTOS with 10 epochs. The `results/` knowledge base likewise carries different
numbers. The figures therefore cannot be redrawn from data held in this repository — they must
either be located in the original (external) run environment, or the figures and the corresponding
numbers in the manuscript must be re-derived from a run whose artifacts are retained.

## Reproducing

```bash
python make_figures.py     # writes Figure_1.{pdf,png} and Figure_3.{pdf,png} into this folder
```

Requires `matplotlib` and `pillow`.
