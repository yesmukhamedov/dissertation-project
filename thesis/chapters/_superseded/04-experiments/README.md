# Chapter 4: Experimental Research

**Status:** §4.1 approved; §4.2–§4.C in drafting (all experiments run; every section unblocked except the clinical Grad-CAM overlays of §4.6, gap G-3)
**Chapter function:** Experiments 1–7 + the H-3 domain-distance analysis — execution, results, analysis
**Governance bindings:** H-1, H-2, **H-3**, H-4, H-5, H-6, **H-7 (v7.0.0 External Clinical Performance)**, PC-1, PC-2, PC-6, PC-7, PC-8, PC-9, PC-10, EH-3, EH-4, **SB-1.12, CFC-2.9, PC-0 (v5.3)**

> **§4.4 (H-3) inserted; §4.4–§4.8 renumbered to §4.5–§4.9.** H-3 (domain distance) was recorded as dropped in earlier versions but was measured and confirmed on 6/6 target domains. It is placed before every external-generalization section because it states the mechanism those sections test the consequences of. Chapter-4 numbering downstream of §4.3 shifts by one.
**Key sources:** dr-classifier experiment outputs (training logs, metrics, confusion matrices)

## Paradigmatic framing insertion (v5.3) — Task 2.6

### §4.2 (Experiment 1 — Causal Improvement) — Task 2.6
- **2.6.1 — Configs A/C (baseline arm).** In the configuration description, state explicitly: *"The baseline configuration of Experiment 1 (configs A and C) operationally instantiates the end-to-end CNN classification paradigm (P1), of which Gulshan et al. (2016) is the canonical representative in this dissertation. It is not Gulshan's system; it is an internal operational construct defined by OD-3 (stretch-resize + ImageNet normalize, 3 channels)."*
- **2.6.2 — Configs B/D (integrated arm).** State: *"The integrated configuration of Experiment 1 (configs B and D) operationalises the integrated preprocessing-CNN paradigm (P2), in which preprocessing is treated as an integral model component co-determining the feature space available to the CNN. The 8 stages of OD-3 are the engineering realisation of this paradigm."*
- **2.6.3 — Discussion.** State explicitly that the A-vs-B (and C-vs-D) result is interpreted as an **empirical contrast between two paradigms under matched conditions**, *not* as a numerical comparison against Gulshan's reported figures. Per CFC-2.2 and SB-1.12, no direct numerical claim against Gulshan is permissible. Per CFC-2.8 v5.1, the A-vs-B difference reflects the joint contribution of preprocessing and pretraining source.

### Cross-cutting forbidden phrasings
"Gulshan is our baseline" / "we outperform Gulshan" / "configs A/C reproduce Gulshan." The operational baseline must always be referred to as "configs A/C" or "the baseline configuration" (operational, OD-3) — never as "Gulshan."

## Sections (per outline/TABLE_OF_CONTENTS_EN.md, v6.0.0)

# 4 EXPERIMENTAL RESEARCH — PREPROCESSING IMPACT ON CNN DIAGNOSTIC PERFORMANCE

## 4.1 Datasets and Experimental Configuration
- 4.1.1 Tiered Dataset Architecture
- 4.1.2 Class Distribution Analysis and Data Partitioning Strategy
- 4.1.3 Hardware Specification and Reproducibility Protocol

## 4.2 Experiment 1: Integrated Pipeline Dominance — Pipeline + In-Domain Pretraining vs. Baseline on EyePACS (H-1)
- 4.2.1 Restored 2×2 Factorial Design (Configurations A–D)
- 4.2.2 Training Dynamics and Convergence Analysis
- 4.2.3 Quantitative Comparison of Diagnostic Metrics

## 4.3 Experiment 2: Stage Ablation + CLAHE/σ Sweeps (H-2)
- 4.3.1 Cumulative Ablation Design (Levels L0–L7)
- 4.3.2 CLAHE Threshold Sensitivity Analysis (H-2 Sub-Analysis)
- 4.3.3 Flat-Field σ Sweep and Image Quality Metrics

## 4.4 Domain Distance Reduction Across Six Target Domains (H-3)
- 4.4.1 Measurement Protocol: MMD over Representations and KL over Channel Histograms
- 4.4.2 Distance Reduction Results and Their Interpretive Limits

## 4.5 Experiment 3: Cross-Dataset Transferability on APTOS 2019 (H-4)
- 4.5.1 Zero-Shot Transfer to APTOS 2019
- 4.5.2 Baseline vs Pipeline Comparison

## 4.6 Experiment 4: Grad-CAM Explainability on IDRiD + Clinical (H-5)
- 4.6.1 Grad-CAM Generation Protocol
- 4.6.2 Quantitative ALO and IoU with IDRiD Lesion Masks
- 4.6.3 Per-Image Consistency of the Attention Effect and Limits of the Present Evidence

## 4.7 Experiment 5: External Clinical Performance on IDRiD + Messidor-2 (H-7)

## 4.8 Experiment 6: Device Domain Shift on DDR + ODIR-5K + RFMiD (H-6)

## 4.9 Experiment 7: Small Data Training (IDRiD → Clinical)

- Conclusions to Chapter 4
