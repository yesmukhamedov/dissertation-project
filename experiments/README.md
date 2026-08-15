# dr-classifier

Research codebase for the PhD dissertation **"Automated Diabetic Retinopathy Diagnosis via Fundus Image Enhancement and CNN Classification"** (Yesmukhamedov N.S., IITU, Almaty).

Classifies fundus photographs into five DR severity grades (0–4) per the International Clinical DR Disease Severity Scale. The core thesis: the integrated 8-stage preprocessing pipeline is an integral model component — `model = preprocessing + CNN` — and it, not architectural complexity, is the primary driver of classification improvement.

> **Provenance.** All seven experiments have been run and all seven hypotheses are supported. The numbers of record live in `results/` (the portable knowledge base), **not** in `experiments/outputs/`, which still holds an earlier run that disagrees with the current one — in sign, on IDRiD. Do not cross-check one against the other; see `results/INTEGRITY_NOTE.md`.

## Pipeline Architecture

Eight stages, all always-on except augmentation:

| Stage | Operation | Always On | Description |
|-------|-----------|-----------|-------------|
| 0 | Canonical flip | Yes | Left→right eye orientation |
| 1 | OD–fovea rotation normalization | Yes | Rotation to a canonical optic-disc/fovea axis |
| 2 | FOV crop + resize | Yes | FOV detection, isotropic resize to 512×512, zero-padded |
| 3 | FOV mask generation | Yes | Binary 1.0/0.0 mask → 4th channel |
| 4 | Flat-field correction | Yes | Adaptive Gaussian, σ = 0.07·D_FOV, to normalize illumination gradients |
| 5 | Dual-constraint CLAHE | Yes | LAB L-channel, stochastic at train time (p=0.8), clip_factor × tile_area/256 capped by a global threshold |
| 6 | Augmentation | Train only | Unified affine (truncated Gaussian rotation σ=13°, zoom, shear, stretch) + ColorJitter + Gaussian noise + JPEG compression |
| 7 | Dataset-specific normalize | Yes (last) | Channel-wise mean/std from the training set → float32 tensor |

The full pipeline outputs a 4-channel tensor `(4, 512, 512)`: RGB + binary FOV mask. The mask channel informs the CNN where real image data exists vs. zero-padding from isotropic resize. The first Conv2d layer of both architectures is replaced with a 4-channel variant (pretrained RGB weights copied, channel 4 initialized with the RGB mean). The baseline arm is stretch-resize to 512×512 + ImageNet normalize, 3 channels.

**PCA colour jitter was retired on 2026-06-26** and replaced by ColorJitter in Stage 6; no PCA basis is used anywhere in the current pipeline.

## Experiments

Seven experiments, plus the H-3 domain-distance block, which is measurement over trained models rather than a training run:

| Experiment | Hypothesis | Design | Dataset |
|------------|-----------|--------|---------|
| **Exp 1** — Factorial | H-1: Integrated Pipeline Dominance | 2×2 factorial: {ResNet-50, EfficientNet-B3} × {baseline 3ch, full pipeline 4ch}, configs A–D | EyePACS 100% (~35,126) |
| **Exp 2** — Component Ablation | H-2 | Cumulative 8-level stage ablation + two-dimensional CLAHE sweep + flat-field σ sweep | EyePACS |
| **Exp 3** — Transferability | H-4: Cross-dataset transfer (G ≥ 0.85) | Train on EyePACS → zero-shot evaluation, source-domain normalization statistics | APTOS 2019 |
| **Exp 4** — Explainability | H-5: Grad-CAM ALO/IoU | Attention–Lesion Overlap against pixel-level lesion masks | IDRiD (54 masks) + Clinical |
| **Exp 5** — External Clinical Performance | H-7 | Δ wF1(integrated − baseline) ≥ MCID 0.050 with CI⁻ > 0 on **each** set | IDRiD + Messidor-2 |
| **Exp 6** — Device Shift | H-6: Camera robustness | Cross-device evaluation over five camera groupings, DR labels only | DDR, ODIR-5K, RFMiD |
| **Exp 7** — Small Data | — | 5-fold CV under scarcity, both arms from the same initialization | IDRiD → Clinical |
| — | H-3: Domain-Shift Reduction | MMD over penultimate-layer features (primary) + KL over channel histograms (secondary); forward passes only | Six target domains |

Dominance criterion (EH-3): Δ weighted-F1 ≥ 5 pp **AND** Δ ROC-AUC ≥ 0.02 **AND** no Cohen's κ degradation, validated independently for both architectures.

**The integrated arm varies pretraining and preprocessing together** (ImageNet→continual-SSL initialization), so it is a composite factor. Exp 2's cumulative ablation, run under a single initialization, is what decomposes it — its L0→L7 span reproduces the whole Exp-1 gain.

## Project Structure

```
dr-classifier/
├── run_experiment.py            # CLI entry point for all experiments
├── configs/
│   └── default.yaml             # Master config (pipeline, training, evaluation)
│
├── src/
│   ├── preprocessing/           # The 8-stage pipeline
│   │   ├── pipeline.py          #   Pipeline orchestrator
│   │   ├── canonical_flip.py    #   Stage 0
│   │   ├── canonical_orientation.py
│   │   ├── od_fovea_detect.py   #   OD/fovea detection for Stage 1
│   │   ├── crop_resize.py       #   Stages 2–3: FOV crop + isotropic resize + mask
│   │   ├── flat_field.py        #   Stage 4: adaptive Gaussian flat-field correction
│   │   ├── upgraded_clahe.py    #   Stage 5: dual-constraint stochastic CLAHE
│   │   ├── polar_clahe.py       #   Polar CLAHE variant
│   │   ├── imagenet_normalize.py#   Stage 7
│   │   └── config.py            #   PreprocessingConfig dataclass + presets
│   ├── data/                    # Dataset classes & augmentation
│   │   ├── datasets.py          #   EyePACS, IDRiD, APTOS, Messidor-2, DDR, ODIR, RFMiD, Clinical
│   │   ├── augmentation_unified.py   #   Stage 6
│   │   ├── splits.py            #   Patient-level stratified k-fold
│   │   └── label_harmonization.py
│   ├── models/                  # CNN architectures
│   │   ├── factory.py           #   Model factory (ResNet-50, EfficientNet-B0/B3/B4)
│   │   ├── resnet.py
│   │   └── efficientnet.py
│   ├── ssl/                     # Self-supervised pretraining + the linear-probe gate
│   ├── training/                # Training infrastructure
│   │   ├── trainer.py           #   AMP, early stopping, k-fold CV, metrics CSV
│   │   ├── losses.py            #   FocalLoss(γ=2, α=inv-freq) + weighted CE
│   │   └── checkpoint.py        #   Best/last checkpoint management
│   ├── evaluation/              # Metrics & statistical testing
│   │   ├── metrics.py           #   Primary (F1, AUC, κ, acc), secondary, clinical
│   │   ├── statistical_tests.py #   McNemar, DeLong, bootstrap CI, Holm-Bonferroni
│   │   └── calibration.py
│   ├── experiments/             # Experiment runners (exp1–exp7)
│   │   ├── exp1_factorial.py
│   │   ├── exp2_ablation.py
│   │   ├── exp3_transferability.py
│   │   ├── exp4_explainability.py
│   │   ├── exp5_clinical_degradation.py
│   │   ├── exp6_device_shift.py
│   │   ├── exp7_clinical.py
│   │   └── _eval_utils.py
│   ├── explainability/          # Grad-CAM + ALO/IoU
│   └── utils/                   # Config loader, seed, image quality
├── docs/                        # experimental_protocol.md (quick-start) + design briefs
├── scripts/                     # Utilities, precompute caches, verification
├── od_fovea_detector/           # OD/fovea heatmap detector
├── colab/, kaggle/              # Remote-runner harnesses
├── tests/                       # Unit tests
├── environment.yml              # Conda environment (Python 3.10, PyTorch 2.5.1, CUDA 12.1)
└── requirements.txt             # Pip dependencies
```

**Governance lives in `../thesis/governance/`** — INVARIANTS, HYPOTHESIS, ARGUMENT_MAP, RESEARCH_ARCHITECTURE and the rest. There are no governance copies here; `docs/` holds only the quick-start protocol and design briefs.

## Quickstart

### Prerequisites

- Python 3.10+
- NVIDIA GPU with CUDA 12.1 (tested on RTX 3060 12GB)
- Datasets placed according to paths in `configs/default.yaml`

### Installation

```bash
# Option A: Conda (recommended)
conda env create -f environment.yml
conda activate dr-classifier

# Option B: Pip
pip install -r requirements.txt
pip install timm>=0.9.12 pytorch-grad-cam>=1.4.8 scipy>=1.11.0 statsmodels>=0.14.0
```

### Running Experiments

```bash
# Full Experiment 1 (configs A–D, 5-fold CV)
python run_experiment.py exp1 --config configs/default.yaml

# Selected configs
python run_experiment.py exp1 --config configs/default.yaml --configs A,B

# Single fold
python run_experiment.py exp1 --configs D --fold 0

# Resume from checkpoint
python run_experiment.py exp1 --configs D --resume

# Other experiments
python run_experiment.py exp2
python run_experiment.py exp4
```

Exp 1 needs a 512² Stage 0–4 cache; the SSL 256² cache is not reusable for it.

## Datasets

| Dataset | Role | Size | Camera | Tier |
|---------|------|------|--------|------|
| **EyePACS** | Primary training (Exp 1, 2) | ~35,126 | Canon CR-1 | Training |
| **APTOS 2019** | Cross-dataset transfer (Exp 3) | ~3,662 | Mixed | External |
| **IDRiD** | Lesion localization (Exp 4), external performance (Exp 5), small data (Exp 7) | ~516 (81 with pixel masks, 54 used) | Kowa | Clinical |
| **Messidor-2** | External clinical performance (Exp 5) | ~1,748 | Topcon | External |
| **RFMiD** | Device domain shift (Exp 6) | ~3,200 | Topcon, Kowa | Device |
| **DDR** | Device domain shift (Exp 6) | ~13,673 | 42 camera types | Device |
| **ODIR-5K** | Device domain shift (Exp 6) | ~5,000 | Canon, Zeiss, Kowa | Device |
| **Clinical (KZ)** | Small data training (Exp 7) | — | — | Clinical |

All datasets use five-class DR staging (Grade 0–4); Exp 6 uses DR labels only. Cross-validation: 5-fold, patient-level stratified split (no patient's images in both train and val within a fold).

## Evaluation

**Primary metrics** (EH-1 priority order): weighted F1-score → ROC-AUC (macro, OvR) → Cohen's κ (quadratic) → accuracy.

**Statistical testing**: McNemar test (paired classifier comparison), DeLong test (AUC comparison), bootstrap 95% CI (≥1,000 iterations), Holm-Bonferroni correction, mixed-effects ANOVA.

**Clinical metrics**: sensitivity, specificity, PPV, NPV at the referable DR threshold (Grade ≥ 2).

## Hardware

Developed and tested on: WSL2 Ubuntu, NVIDIA RTX 3060 12GB, conda environment `dr-classifier`. Datasets stored on the external drive, `E:/datasets/` (`/mnt/e/datasets/` under WSL), with every path read from `configs/default.yaml` — none is hardcoded. Mixed precision is enabled for ResNet-50 and **disabled** for EfficientNet (fp16 overflow).

## License

This repository is part of a doctoral dissertation and is not licensed for redistribution.
