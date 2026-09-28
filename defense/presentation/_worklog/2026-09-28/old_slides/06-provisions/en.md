---
slide: 06
id: provisions
lang: en
status: draft
seconds: 80
source: нового слайда в архиве не было — написан заново
terms: [provisions, provision_n, integrated_configuration, baseline_configuration, weighted_f1, domain_distance, generalization_ratio, alo, mcid]
---

# Provisions submitted for defence

## На слайде

1. **An eight-stage fundus preprocessing pipeline** formalised as a model component (canonical orientation, isotropic scaling, field-of-view mask as a 4th channel, illumination correction σ = 0.07·D, CLAHE with the clip limit as the minimum of two constraints, θ* = (2.5; 0.03)); stage contributions are separable: weighted F1 rises monotonically **0.754 → 0.819**, **41 %** of the gain comes from the two photometric stages *(H-2)*
2. **The integrated "pipeline + CNN" configuration** outperforms the baseline on 35,126 EyePACS images for both architectures: weighted F1 **+6.5 pp**, ROC-AUC **+0.03**, κ **+0.11** (p < 0.01, Holm-corrected), with no interaction with the architecture *(H-1)*
3. **The pipeline provides transferability:** the distance to each of six external corpora shrinks (MMD **−0.070…−0.093**); on APTOS F1 **+0.089** (G 0.898 vs 0.858); the spread across five camera groups is **2.4× narrower**; on IDRiD and Messidor-2 **+0.069 / +0.054** (above the MCID of 0.05) *(H-3, H-4, H-6, H-7)*
4. **An asymmetric measure of attention–annotation alignment (ALO):** higher in the integrated configuration for all four lesion types, **+0.099…+0.129**, p ≤ 0.015 *(H-5)*

## Речь

Four provisions are submitted for defence.
First, the eight-stage pipeline formalised as a model component. Stage contributions are separable: adding the stages one by one raises F1 from 0.754 to 0.819 monotonically in all five folds, and the two photometric stages give 41 percent of the gain.
Second, on both architectures the integrated configuration beats the baseline by 6.5 percentage points in F1, 0.03 in AUC and 0.11 in kappa, independently of the architecture.
Third, the pipeline provides transferability: the distance to six external corpora shrinks, and on unseen, device and clinical corpora the integrated configuration is higher.
Fourth, an asymmetric measure of attention–annotation alignment; by it, alignment is higher for all four lesion types.
