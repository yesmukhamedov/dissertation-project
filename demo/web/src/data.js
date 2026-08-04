// src/data.js — Canonical data for DR Diagnosis Dashboard
//
// SOURCE OF TRUTH: the results/ knowledge base (VALUES.md → results/tables/).
// Every number below is traceable to a table in results/tables/ (referenced per constant).
// Do NOT hand-edit numbers without updating results/ first.
//
// Configs: A = baseline(3ch)+ResNet-50 · B = pipeline(4ch)+ResNet-50
//          C = baseline(3ch)+EffNet-B3 · D = pipeline(4ch)+EffNet-B3
// Where a panel shows a single "baseline vs pipeline" pair, it is C vs D (EfficientNet-B3),
// which is the arm used for all transfer/device/explainability experiments.

// Colour palette
export const C = {
  blue: '#378ADD', teal: '#1D9E75', coral: '#D85A30', purple: '#7F77DD',
  amber: '#EF9F27', gray: '#888780', green: '#639922', red: '#E24B4A',
  blueBg: '#E6F1FB', tealBg: '#E1F5EE', coralBg: '#FAECE7', purpleBg: '#EEEDFE',
  amberBg: '#FAEEDA', grayBg: '#F1EFE8', greenBg: '#EAF3DE', redBg: '#FCEBEB',
  blueT: '#0C447C', tealT: '#085041', coralT: '#712B13', purpleT: '#3C3489',
  amberT: '#633806', grayT: '#444441', greenT: '#27500A', redT: '#791F1F',
};

// Exp 1: 4 configurations (A–D) — results/tables/TAB-4.2_exp1_factorial.md
// EyePACS 100% (n=35,126), 5-fold patient-level CV. mean ± std.
export const CONFIGS = {
  A: { f1: 0.7518, f1s: 0.0110, auc: 0.8300, aucs: 0.0140, k: 0.7410, ks: 0.0350, acc: 0.7247, macroF1: 0.4281, lbl: 'Baseline (3ch) + ResNet-50', preprocessing: 'Baseline (3ch)', cnn: 'ResNet-50' },
  B: { f1: 0.8172, f1s: 0.0090, auc: 0.8620, aucs: 0.0110, k: 0.8539, ks: 0.0260, acc: 0.8027, macroF1: 0.5322, lbl: 'Pipeline (4ch) + ResNet-50', preprocessing: 'Pipeline', cnn: 'ResNet-50' },
  C: { f1: 0.7538, f1s: 0.0120, auc: 0.8210, aucs: 0.0150, k: 0.7468, ks: 0.0330, acc: 0.7273, macroF1: 0.4300, lbl: 'Baseline (3ch) + EfficientNet-B3', preprocessing: 'Baseline (3ch)', cnn: 'EfficientNet-B3' },
  D: { f1: 0.8193, f1s: 0.0100, auc: 0.8570, aucs: 0.0120, k: 0.8571, ks: 0.0270, acc: 0.8052, macroF1: 0.5355, lbl: 'Pipeline (4ch) + EfficientNet-B3', preprocessing: 'Pipeline', cnn: 'EfficientNet-B3' },
};

// Exp 1: paired differences with 95% CI — TAB-4.2 §1.2
export const CONFIG_DELTAS = [
  { pair: 'B − A (ResNet-50)', metric: 'Weighted F1', delta: 0.0654, ci: [0.0521, 0.0873] },
  { pair: 'B − A (ResNet-50)', metric: 'ROC-AUC', delta: 0.0320, ci: [0.0175, 0.0419] },
  { pair: 'B − A (ResNet-50)', metric: 'Cohen κ', delta: 0.1129, ci: [0.0780, 0.1414] },
  { pair: 'D − C (EfficientNet-B3)', metric: 'Weighted F1', delta: 0.0655, ci: [0.0423, 0.0801] },
  { pair: 'D − C (EfficientNet-B3)', metric: 'ROC-AUC', delta: 0.0360, ci: [0.0204, 0.0462] },
  { pair: 'D − C (EfficientNet-B3)', metric: 'Cohen κ', delta: 0.1103, ci: [0.0829, 0.1453] },
];

// Exp 2: Cumulative ablation — 8 levels (L0…L7) — results/tables/TAB-4.4_exp2_ablation.md
// EyePACS 100%, 5 folds, EfficientNet-B3, SINGLE initialization across all levels.
// L0 reproduces Config C (0.7538) and L7 reproduces Config D (0.8193).
export const ABL = [
  { n: 'Baseline (stretch-resize + ImageNet norm, 3ch)', f1: 0.7538, auc: 0.8210, k: 0.7468, acc: 0.7273, sigmaFold: 0.0025 },
  { n: '+Canonical flip (Stage 0)', f1: 0.7609, auc: 0.8260, k: 0.7590, acc: 0.7356, sigmaFold: 0.0024 },
  { n: '+OD-fovea rotation (Stage 1)', f1: 0.7677, auc: 0.8299, k: 0.7701, acc: 0.7456, sigmaFold: 0.0021 },
  { n: '+Isotropic resize + FOV mask (Stages 2–3)', f1: 0.7759, auc: 0.8360, k: 0.7818, acc: 0.7561, sigmaFold: 0.0024 },
  { n: '+Flat-field correction (Stage 4)', f1: 0.7902, auc: 0.8436, k: 0.8038, acc: 0.7738, sigmaFold: 0.0030 },
  { n: '+CLAHE enhancement (Stage 5)', f1: 0.8027, auc: 0.8505, k: 0.8267, acc: 0.7899, sigmaFold: 0.0028 },
  { n: '+Augmentation (Stage 6)', f1: 0.8128, auc: 0.8541, k: 0.8426, acc: 0.7977, sigmaFold: 0.0027 },
  { n: 'Full pipeline (all stages)', f1: 0.8193, auc: 0.8570, k: 0.8571, acc: 0.8052, sigmaFold: 0.0021 },
];

// Exp 2: marginal contribution of each stage (Δⱼ, pp) vs the 2·σ_fold significance band.
// All 7 transitions clear the band, and the hierarchy IS resolvable: Δⱼ spans 0.65–1.43pp,
// a spread of ≈3·σ_fold. The two photometric stages (flat-field, CLAHE) lead and together
// carry 41% of the +6.55pp total. What the data resolve is the grouping, not a strict 1–7
// order — adjacent ranks (e.g. Stage 1 at 0.68 vs Stage 7 at 0.65) sit inside the noise.
export const STAGE_CONTRIB = [
  { stage: 'Canonical flip (Stage 0)', delta_f1: 0.71, band: 0.48, rank: 5, share: 11, significant: true },
  { stage: 'OD-fovea rotation (Stage 1)', delta_f1: 0.68, band: 0.42, rank: 6, share: 10, significant: true },
  { stage: 'FOV crop + mask (Stages 2–3)', delta_f1: 0.82, band: 0.48, rank: 4, share: 13, significant: true },
  { stage: 'Flat-field correction (Stage 4)', delta_f1: 1.43, band: 0.60, rank: 1, share: 22, significant: true },
  { stage: 'CLAHE enhancement (Stage 5)', delta_f1: 1.25, band: 0.56, rank: 2, share: 19, significant: true },
  { stage: 'Augmentation (Stage 6)', delta_f1: 1.01, band: 0.54, rank: 3, share: 15, significant: true },
  { stage: 'Dataset-specific normalize (Stage 7)', delta_f1: 0.65, band: 0.42, rank: 7, share: 10, significant: true },
];

// Exp 4: ALO + IoU by lesion type — results/tables/TAB-4.7_exp4_alo_iou.md
// EfficientNet-B3, fold 0, all 54 IDRiD images with lesion masks, τ = 0.5.
// ab/ap = ALO baseline/pipeline; ib/ip = IoU baseline/pipeline. All 4 types significant.
export const ALO = [
  { l: 'Microaneurysms', n: 54, ab: 0.2126, ap: 0.3160, ib: 0.1065, ip: 0.1694, p: 0.0033, pIou: 0.0053, ci: [0.0331, 0.1587] },
  { l: 'Hemorrhages', n: 53, ab: 0.2794, ap: 0.4011, ib: 0.1516, ip: 0.2229, p: 0.0016, pIou: 0.0029, ci: [0.0485, 0.1739] },
  { l: 'Hard exudates', n: 54, ab: 0.3502, ap: 0.4790, ib: 0.1944, ip: 0.2830, p: 0.0007, pIou: 0.0011, ci: [0.0735, 0.2007] },
  { l: 'Soft exudates', n: 26, ab: 0.2318, ap: 0.3310, ib: 0.1183, ip: 0.1775, p: 0.0148, pIou: 0.0189, ci: [0.0401, 0.1969] },
];

// Exp 4: IoU by lesion type (secondary metric)
export const IOU = [
  { l: 'Microaneurysms', baseline: 0.1065, pipeline: 0.1694, p: 0.0053 },
  { l: 'Hemorrhages', baseline: 0.1516, pipeline: 0.2229, p: 0.0029 },
  { l: 'Hard exudates', baseline: 0.1944, pipeline: 0.2830, p: 0.0011 },
  { l: 'Soft exudates', baseline: 0.1183, pipeline: 0.1775, p: 0.0189 },
];

// Exp 4: per-image direction of the effect (↑ better with pipeline / ↓ worse / = unchanged)
export const ALO_DIRECTION = [
  { l: 'Microaneurysms', n: 54, up: 38, down: 7, same: 9 },
  { l: 'Hemorrhages', n: 53, up: 36, down: 8, same: 9 },
  { l: 'Hard exudates', n: 54, up: 41, down: 5, same: 8 },
  { l: 'Soft exudates', n: 26, up: 17, down: 4, same: 5 },
];

// Exp 4: robustness of the ALO result to the heat-map binarization threshold
export const ALO_THRESHOLD = [
  { tau: 0.2, improved: 4, significant: 4 },
  { tau: 0.3, improved: 4, significant: 4 },
  { tau: 0.5, improved: 4, significant: 4 },
  { tau: 0.7, improved: 4, significant: 3 },
];

// H-3: domain distance — results/tables/H-3_domain_distance.md
// MMD over penultimate-layer features (lower = closer to the source domain) and
// KL over per-channel histograms. BASE = baseline arm, INT = integrated (pipeline) arm.
export const DOMAIN_DIST = [
  { domain: 'APTOS 2019', mmdBase: 0.1910, mmdInt: 0.1178, dDelta: 0.0732, ci: [0.0380, 0.0996], klBase: 0.0894, klInt: 0.0588 },
  { domain: 'IDRiD', mmdBase: 0.2211, mmdInt: 0.1395, dDelta: 0.0816, ci: [0.0530, 0.1228], klBase: 0.1171, klInt: 0.0725 },
  { domain: 'Messidor-2', mmdBase: 0.1768, mmdInt: 0.1068, dDelta: 0.0700, ci: [0.0475, 0.1031], klBase: 0.0905, klInt: 0.0575 },
  { domain: 'DDR', mmdBase: 0.2098, mmdInt: 0.1314, dDelta: 0.0784, ci: [0.0387, 0.1061], klBase: 0.1067, klInt: 0.0658 },
  { domain: 'ODIR-5K', mmdBase: 0.2387, mmdInt: 0.1599, dDelta: 0.0788, ci: [0.0371, 0.1089], klBase: 0.1282, klInt: 0.0817 },
  { domain: 'RFMiD', mmdBase: 0.2606, mmdInt: 0.1675, dDelta: 0.0931, ci: [0.0489, 0.1245], klBase: 0.1370, klInt: 0.0899 },
];

// Exp 3: APTOS 2019 transferability (H-4) — results/tables/TAB-4.6_exp3_transfer.md
// EfficientNet-B3, fold-0 checkpoints, zero-shot. Configs A/B were not evaluated on APTOS.
export const APTOS = {
  C: { f1: 0.6465, auc: 0.7940, k: 0.7887, acc: 0.6338, macroF1: 0.4649, G: 0.8577, eyepacsF1: 0.7538 },
  D: { f1: 0.7354, auc: 0.8263, k: 0.8874, acc: 0.7272, macroF1: 0.5666, G: 0.8976, eyepacsF1: 0.8193 },
  deltaF1: 0.0889, deltaF1Ci: [0.0681, 0.1197],
  deltaAuc: 0.0323, deltaAucCi: [0.0224, 0.0482],
  threshold: 0.85,
};

// Exp 3/5: Cross-dataset generalization — weighted F1 (Config C vs D)
export const GEN = [
  { d: 'EyePACS (train)', fb: 0.7538, fp: 0.8193 },
  { d: 'APTOS 2019', fb: 0.6465, fp: 0.7354, Gb: 0.8577, Gp: 0.8976 },
  { d: 'IDRiD', fb: 0.5938, fp: 0.6627, Gb: 0.7877, Gp: 0.8089 },
  { d: 'Messidor-2', fb: 0.6282, fp: 0.6823, Gb: 0.8334, Gp: 0.8328 },
];

// Exp 3/5: Cross-dataset generalization — ROC-AUC
// IDRiD / Messidor-2 AUC come from the exp6 camera groups kowa_idrid / topcon_messidor2.
export const GEN_AUC = [
  { dataset: 'EyePACS (train)', baseline: 0.8210, pipeline: 0.8570 },
  { dataset: 'APTOS 2019', baseline: 0.7940, pipeline: 0.8263 },
  { dataset: 'IDRiD', baseline: 0.8195, pipeline: 0.8627 },
  { dataset: 'Messidor-2', baseline: 0.8407, pipeline: 0.8729 },
];

// Exp 3/5: Generalization ratio G = F1_external / F1_EyePACS (own arm's in-domain F1).
// NOTE: the G ≥ 0.85 threshold belongs to H-4 (APTOS) only. For IDRiD/Messidor-2 the
// applicable floor is the H-6 device floor of 0.70 — both arms clear it on every dataset.
export const G_RATIO = [
  { dataset: 'APTOS 2019', G_baseline: 0.8577, G_pipeline: 0.8976, threshold: 0.85 },
  { dataset: 'IDRiD', G_baseline: 0.7877, G_pipeline: 0.8089, threshold: 0.70 },
  { dataset: 'Messidor-2', G_baseline: 0.8334, G_pipeline: 0.8328, threshold: 0.70 },
];

// Exp 5: H-7 External Clinical Performance — results/tables/TAB-4.8_exp5_degradation.md.
// OPERATIVE criterion (form S, both sets mandatory): Δ wF1(D−C) ≥ MCID 0.050 AND CI⁻ > 0.
// Both sets pass → H-7 CONFIRMED (2/2). Caveat: the Messidor-2 margin over MCID is 0.0041.
// Δ_drop (dropBase/dropPipe) is RETIRED and kept as a reference quantity only: it is
// algebraically degenerate — Δ_drop(D) − Δ_drop(C) ≡ 0.0655 − Δ wF1(X) — so it demands the
// pipeline beat baseline more abroad than at home and penalizes its in-domain win.
export const DEGRADATION = [
  { dataset: 'IDRiD', n: 413, extBaseline: 0.5938, extPipeline: 0.6627, deltaF1: 0.0689, ci: [0.0494, 0.0968], p: 0.0021,
    mcid: 0.050, margin: 0.0189, passS: true,
    dropBase: 16.00, dropPipe: 15.66, relBase: 21.2, relPipe: 19.1 },
  { dataset: 'Messidor-2', n: 1744, extBaseline: 0.6282, extPipeline: 0.6823, deltaF1: 0.0541, ci: [0.0362, 0.0814], p: 0.0138,
    mcid: 0.050, margin: 0.0041, passS: true,
    dropBase: 12.56, dropPipe: 13.70, relBase: 16.7, relPipe: 16.7 },
];

// Exp 7 / E-7: Small data training (IDRiD → Clinical KZ). Preregistered.
// results/tables/TAB-4.10_exp7_smalldata.md
export const SMALL_DATA = [
  { condition: 'Baseline (3ch)', idrid_f1: 0.5850, idrid_std: 0.0380, clinical_f1: 0.5134, clinical_f1_std: 0.0450, clinical_auc: 0.7417, clinical_k: 0.4876 },
  { condition: 'Pipeline (4ch)', idrid_f1: 0.6520, idrid_std: 0.0310, clinical_f1: 0.5932, clinical_f1_std: 0.0400, clinical_auc: 0.7899, clinical_k: 0.6121 },
];

// Exp 7: paired differences (the unpaired bootstrap CIs overlap at n=60 — significance
// comes from the PAIRED test, where both arms are scored on the same 60 images).
export const SMALL_DATA_DELTAS = [
  { metric: 'Weighted F1', delta: 0.0798, ci: [0.0350, 0.1106] },
  { metric: 'Cohen κ', delta: 0.1245, ci: [0.0782, 0.1960] },
  { metric: 'ROC-AUC', delta: 0.0482, ci: [0.0183, 0.0707] },
];

// Exp 7: unpaired bootstrap 95% CI per arm on the clinical hold-out (n=60, 1000 resamples).
// These OVERLAP — quote the paired CIs above; these only with that caveat.
export const SMALL_DATA_UNPAIRED = { baseline: [0.4511, 0.6007], pipeline: [0.5338, 0.6742] };

// Exp 2: Flat-field σ sweep — results/tables/exp2_flatfield_sigma_sweep.md
// Strictly unimodal, interior optimum at σ* = 0.07·D. Range R = 0.052.
export const FF_SWEEP = [
  { sigma: 0.05, f1: 0.7662, cnr: 3.24 },
  { sigma: 0.06, f1: 0.7883, cnr: 3.47 },
  { sigma: 0.07, f1: 0.8089, cnr: 3.93 },
  { sigma: 0.08, f1: 0.7930, cnr: 3.66 },
  { sigma: 0.09, f1: 0.7774, cnr: 3.35 },
  { sigma: 0.10, f1: 0.7577, cnr: 3.10 },
];
export const FF_HELDOUT = { off: 0.7513, optimal: 0.8087, delta: 0.0574, ci: [0.0428, 0.0806], sigmaStar: 0.07 };
export const CLAHE_HELDOUT = { off: 0.7538, optimal: 0.8137, delta: 0.0599, ci: [0.0388, 0.0770],
  dr1Off: 0.0976, dr1Opt: 0.2091, dr2Off: 0.5316, dr2Opt: 0.6477, clipStar: 2.5, threshStar: 0.03, pApply: 0.80 };

// Exp 6: Cross-device performance — results/tables/TAB-4.9_exp6_device.md
// All 5 groups clear the g_floor = 0.70 for BOTH arms; the real result is the
// collapse of the between-device spread (see DEVICE_SPREAD).
export const DEV = [
  { c: 'Canon CR-1 (EyePACS, in-domain)', fb: 0.7538, fp: 0.8193, n: 35126 },
  { c: 'Topcon (Messidor-2)', fb: 0.6282, fp: 0.6823, gb: 0.8334, gp: 0.8328, n: 1744 },
  { c: 'Kowa (IDRiD)', fb: 0.5938, fp: 0.6627, gb: 0.7877, gp: 0.8089, n: 413 },
  { c: 'Canon+Topcon (DDR)', fb: 0.6154, fp: 0.6671, gb: 0.8164, gp: 0.8142, n: 1200 },
  { c: 'Canon+Zeiss (ODIR-5K)', fb: 0.5700, fp: 0.6581, gb: 0.7562, gp: 0.8032, n: 950 },
  { c: 'Topcon+Kowa (RFMiD)', fb: 0.5434, fp: 0.6421, gb: 0.7209, gp: 0.7837, n: 640 },
];

// Exp 6: between-device spread across the 5 external camera groups
export const DEVICE_SPREAD = [
  { metric: 'std (weighted F1)', baseline: 0.0306, pipeline: 0.0130, delta: -0.0176, ci: [-0.0253, -0.0062], factor: 2.4 },
  { metric: 'std (ROC-AUC)', baseline: 0.0214, pipeline: 0.0070, delta: -0.0144, ci: [-0.0233, -0.0072], factor: 3.1 },
];

// Per-class F1 (Config C vs D, EyePACS val, n=35,126) — results/tables/exp1_per_class.md
export const CLS = [
  { g: 'DR 0', b: 0.8889, pp: 0.9333, n: 25810 },
  { g: 'DR 1', b: 0.0976, pp: 0.2188, n: 2443 },
  { g: 'DR 2', b: 0.5316, pp: 0.6594, n: 5292 },
  { g: 'DR 3', b: 0.2173, pp: 0.3179, n: 873 },
  { g: 'DR 4', b: 0.4147, pp: 0.5483, n: 708 },
];

// Per-class precision / recall (Config C vs D)
export const CLS_PR = [
  { g: 'DR 0', precB: 0.9222, recB: 0.8580, precP: 0.9503, recP: 0.9170 },
  { g: 'DR 1', precB: 0.0734, recB: 0.1453, precP: 0.1818, recP: 0.2747 },
  { g: 'DR 2', precB: 0.6038, recB: 0.4749, precP: 0.7244, recP: 0.6051 },
  { g: 'DR 3', precB: 0.1723, recB: 0.2944, precP: 0.2539, recP: 0.4250 },
  { g: 'DR 4', precB: 0.4430, recB: 0.3898, precP: 0.5732, recP: 0.5254 },
];

// Confusion matrices, EyePACS val n=35,126 (rows = truth, cols = prediction)
export const CONFUSION = {
  C: [[22145, 2939, 586, 117, 23], [1273, 355, 658, 131, 26], [535, 1385, 2513, 716, 143], [45, 116, 300, 257, 155], [16, 40, 105, 271, 276]],
  D: [[23667, 1872, 237, 30, 4], [1016, 671, 661, 84, 11], [211, 1085, 3202, 705, 89], [10, 52, 267, 371, 173], [2, 10, 53, 271, 372]],
};

// Clinical metrics, referable DR (grade ≥ 2), EyePACS in-domain (Config C vs D)
// results/tables/exp1_clinical_indomain.md
export const CLIN = [
  { m: 'Sensitivity', b: 0.6891, v: 0.8007 },
  { m: 'Specificity', b: 0.9455, v: 0.9636 },
  { m: 'PPV', b: 0.7545, v: 0.8427 },
  { m: 'NPV', b: 0.9259, v: 0.9521 },
  { m: 'Referable ROC-AUC', b: 0.8680, v: 0.9100 },
];

// Calibration — results/tables/TAB-4.3_exp1_calibration.md (Config C vs D).
// The pipeline improves calibration on both metrics.
export const CALIBRATION = [
  { metric: 'ECE', baseline: 0.0691, pipeline: 0.0402, improvement: '-42%' },
  { metric: 'Brier Score', baseline: 0.0715, pipeline: 0.0598, improvement: '-16%' },
];

// Image quality, ablation level L0 (baseline) vs L7 (full pipeline), n=100 images.
// results/tables/TAB-4.5_exp2_image_quality.md
// SSIM is measured against the ORIGINAL frame, so a lower value means "further from the
// original" — that is expected for the pipeline, not a regression.
export const IQ = [
  { m: 'CNR', b: 20.43, a: 24.02, pct: '+18%' },
  { m: 'Image Entropy (bits)', b: 5.502, a: 5.901, pct: '+7%' },
  { m: 'SSIM (vs original)', b: 1.000, a: 0.865, pct: '−14% (by design)' },
];

// Per-level image quality across the 8 ablation levels
export const IQ_LEVELS = [
  { level: 'L0 baseline', cnr: 20.43, entropy: 5.502, ssim: 1.000, f1: 0.7538 },
  { level: 'L1 +Stage 0', cnr: 20.43, entropy: 5.502, ssim: 0.998, f1: 0.7609 },
  { level: 'L2 +Stage 1', cnr: 20.41, entropy: 5.508, ssim: 0.981, f1: 0.7677 },
  { level: 'L3 +Stages 2–3', cnr: 20.38, entropy: 5.514, ssim: 0.964, f1: 0.7759 },
  { level: 'L4 +Stage 4', cnr: 28.60, entropy: 5.596, ssim: 0.912, f1: 0.7902 },
  { level: 'L5 +Stage 5', cnr: 24.15, entropy: 5.884, ssim: 0.878, f1: 0.8027 },
  { level: 'L6 +Stage 6', cnr: 24.15, entropy: 5.884, ssim: 0.871, f1: 0.8128 },
  { level: 'L7 +Stage 7', cnr: 24.02, entropy: 5.901, ssim: 0.865, f1: 0.8193 },
];

// CLAHE parameter grids — results/tables/exp2_clahe_sweep.md
// Rows: clip_factor 0.5…4.0 (see CLAHE_CLIP). Cols: global_threshold 0.01…0.05.
// Train-fold values, used to select θ*; held-out confirmation is in CLAHE_HELDOUT.
export const CLAHE_CLIP = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0];
export const CLAHE_THRESH = [0.01, 0.02, 0.03, 0.04, 0.05];
export const CLAHE1 = [
  [.2696, .2895, .3128, .2986, .2807],
  [.3176, .3524, .3689, .3567, .3396],
  [.3593, .3910, .4094, .4026, .3820],
  [.3788, .4183, .4393, .4299, .4091],
  [.4011, .4390, .4693, .4584, .4292],
  [.3911, .4329, .4497, .4381, .4191],
  [.3715, .4101, .4299, .4168, .3978],
  [.3516, .3791, .4003, .3903, .3719],
];
export const CLAHE2 = [
  [.4415, .4587, .4785, .4680, .4492],
  [.4792, .5102, .5295, .5189, .4987],
  [.5187, .5489, .5794, .5734, .5389],
  [.5406, .5822, .6219, .6090, .5700],
  [.5315, .5697, .5968, .5879, .5585],
  [.5119, .5478, .5705, .5586, .5427],
  [.4906, .5296, .5478, .5387, .5201],
  [.4725, .4998, .5180, .5087, .4886],
];
export const CLAHE_WF1 = [
  [.7478, .7508, .7537, .7513, .7474],
  [.7549, .7606, .7651, .7616, .7612],
  [.7691, .7741, .7780, .7736, .7696],
  [.7798, .7873, .7917, .7878, .7806],
  [.7863, .7986, .8136, .8005, .7912],
  [.7820, .7920, .7992, .7930, .7842],
  [.7734, .7815, .7838, .7834, .7768],
  [.7647, .7710, .7754, .7710, .7644],
];

// Pipeline stages — 8-stage pipeline + raw input = 9 entries
export const PIPE = [
  { id: 0, nm: 'Raw input', desc: 'Original fundus photographs. Variable illumination, vignetting, different eye orientations. Canon CR-1 at EyePACS.', detail: 'Resolution: 3888×2592, 8-bit RGB JPEG' },
  { id: 1, nm: 'Stage 0: Canonical flip', desc: 'Left eyes (OS) horizontally flipped to right-eye (OD) orientation. Optic disc consistently on the right side. Deterministic — not random augmentation.', detail: 'If OS detected → np.fliplr(). OD → passthrough.' },
  { id: 2, nm: 'Stage 1: OD-fovea rotation', desc: 'Detect optic disc (brightest region) and fovea (darkest in annular zone). Rotate so OD→fovea axis is horizontal. Normalizes retinal orientation across cameras.', detail: 'OD: Gaussian-blurred green ch, 97th percentile. Fovea: annular search 1.5–3.5× OD-radius. Fallback if low confidence.' },
  { id: 3, nm: 'Stage 2: FOV crop + isotropic resize', desc: 'Detect circular FOV boundary, crop and resize to 512×512 with zero-padding to preserve aspect ratio. Eliminates device-specific border artifacts.', detail: 'Green channel threshold → largest contour → bounding circle. Isotropic resize + zero-pad to 512×512 (replaces stretch-resize).' },
  { id: 4, nm: 'Stage 3: FOV mask generation', desc: 'Generate binary FOV mask (1=retinal pixels, 0=background). Used as the 4th input channel to the CNN — provides spatial boundary information.', detail: 'Binary mask from Stage 2 FOV detection. Appended to RGB → 4-channel (RGBM) tensor input.' },
  { id: 5, nm: 'Stage 4: Adaptive flat-field correction', desc: 'Remove illumination gradients using adaptive Gaussian σ = 0.07×D (D = FOV diameter). Preserves vessel and lesion detail while normalizing device-specific illumination.', detail: 'σ = 0.07 × FOV_diameter. Adaptive σ proportional to FOV size (replaces fixed σ=45).' },
  { id: 6, nm: 'Stage 5: CLAHE (dual-constraint)', desc: 'Adaptive histogram equalization on LAB L-channel. clip_limit = min(clip_factor×tile_area/256, global_threshold×tile_area). Stochastic 80% during training.', detail: 'Tile: 8×8. Parameters from Exp 2 sweep. Stochastic = regularization. Dual-constraint prevents OD over-enhancement.' },
  { id: 7, nm: 'Stage 6: Augmentation (train only)', desc: 'On-the-fly: integrated affine (360° rotation on circular FOV, scale, shear), then ColorJitter (brightness/contrast/saturation/hue, each p=0.5), Gaussian noise (σ∈[2,6], p=0.15), and JPEG compression (quality∈[70,100], p=0.20). Applied only during training, never at inference.', detail: '360° rotation valid because circular FOV. Rotation magnitude σ_θ adapted from Stage 1 OD-fovea detection confidence. Noise + JPEG simulate acquisition variability.' },
  { id: 8, nm: 'Stage 7: Dataset-specific normalize → 4ch', desc: 'Dataset-specific channel-wise normalization statistics (not fixed ImageNet stats). Stack RGB + FOV mask → 4-channel tensor input to CNN.', detail: 'Dataset-specific mean/std computed from EyePACS training set. Output: 4ch (RGBM) tensor at 512×512.' },
  { id: 9, nm: 'Results: CNN output', desc: 'Final outputs of the trained CNN on the preprocessed 4-channel input: predicted DR grade with class probabilities, Grad-CAM heatmap localizing the regions driving the prediction, and an attention overlay highlighting attended lesions on the original fundus.', detail: 'Prediction: softmax over 5 ICDR classes. Grad-CAM: last conv layer of the backbone. Attention overlay: Grad-CAM × FOV mask, blended over RGB.' },
];

// Computational benchmarks — RTX 3060 12 GB, 512×512 input, fp32 inference.
// results/tables/computational_and_iq.md. The 4th channel costs +0.4 GFLOPs (+0.9%)
// and +24 MiB — essentially free.
export const COMPUTE = [
  { metric: 'Parameters', resnet: '23.52M', effnet: '10.70M', unit: '' },
  { metric: 'GFLOPs/image (baseline 3ch)', resnet: '42.7', effnet: '10.0', unit: 'GFLOPs' },
  { metric: 'GFLOPs/image (pipeline 4ch)', resnet: '43.1', effnet: '10.1', unit: 'GFLOPs' },
  { metric: 'Latency bs=1 (baseline)', resnet: '10.5', effnet: '12.8', unit: 'ms/img' },
  { metric: 'Latency bs=1 (pipeline)', resnet: '10.5', effnet: '14.5', unit: 'ms/img' },
  { metric: 'Latency bs=16 (pipeline)', resnet: '8.3', effnet: '7.6', unit: 'ms/img' },
  { metric: 'Throughput bs=16 (pipeline)', resnet: '120.5', effnet: '132.3', unit: 'img/s' },
  { metric: 'VRAM inference bs=16 (pipeline)', resnet: '1002', effnet: '1531', unit: 'MiB' },
  { metric: 'VRAM train-step bs=16 (pipeline)', resnet: '3748', effnet: '13742', unit: 'MiB' },
  { metric: 'Batch size', resnet: '16', effnet: '16', unit: 'images' },
];

// Statistical tests — results/tables/TAB-5.1_statistical.md
export const STAT_TESTS = [
  { test: 'DeLong (referable ROC-AUC)', resnet: 'ΔAUC +0.0410, z=2.87, p=0.0041 ✓', effnet: 'ΔAUC +0.0420, z=2.99, p=0.0028 ✓' },
  { test: 'McNemar (correct-prediction rate)', resnet: 'χ²=7.63, p=0.0057 ✓', effnet: 'χ²=8.23, p=0.0041 ✓' },
  { test: 'Bootstrap 95% CI (ΔF1)', resnet: '[+5.21, +8.73]pp ✓', effnet: '[+4.23, +8.01]pp ✓' },
  { test: 'Holm-corrected p (4 configs)', resnet: 'p_adj=0.0082 ✓', effnet: 'p_adj=0.0056 ✓' },
  { test: 'Mixed-effects ANOVA', resnet: '—', effnet: 'interaction p=0.31 (n.s.)' },
];

// Convergence and overfitting — results/tables/exp1_convergence_ci.md
// Loss-gap = val_loss − train_loss at the best epoch. The pipeline arms converge ~6–7
// epochs earlier with a 2.5× smaller gap AND a HIGHER train loss — regularizer behaviour.
export const TRAIN_TEST_GAP = [
  { config: 'A', arm: 'baseline, ResNet-50', bestEpochs: '16, 14, 17, 15, 16', trainLoss: 0.098, valLoss: 0.150, gap: 0.052 },
  { config: 'B', arm: 'pipeline, ResNet-50', bestEpochs: '9, 8, 10, 9, 9', trainLoss: 0.126, valLoss: 0.147, gap: 0.021 },
  { config: 'C', arm: 'baseline, EffNet-B3', bestEpochs: '15, 17, 14, 16, 15', trainLoss: 0.102, valLoss: 0.156, gap: 0.054 },
  { config: 'D', arm: 'pipeline, EffNet-B3', bestEpochs: '8, 9, 7, 9, 8', trainLoss: 0.131, valLoss: 0.153, gap: 0.022 },
];

// SSL linear-probe gate — results/tables/SSL_continual_gate.md
export const SSL_GATE = {
  fromScratch: [
    { method: 'BYOL (governance primary)', epochs: 50, kappa: 0.0018, passed: false, note: 'collapse' },
    { method: 'MoCo-v2', epochs: 50, kappa: 0.1125, passed: false },
    { method: 'MoCo-v2', epochs: 100, kappa: 0.1098, passed: false },
    { method: 'DINO', epochs: 50, kappa: 0.0763, passed: false },
    { method: 'DINO', epochs: 100, kappa: 0.0602, passed: false },
    { method: 'SIP', epochs: 100, kappa: 0.6616, passed: true },
  ],
  continual: [
    { backbone: 'ResNet-50 (Config B)', random: 0.0040, imagenet: 0.3381, continual: 0.6552, delta: 0.3171, run2Delta: 0.2883, passed: true },
    { backbone: 'EfficientNet-B3 (Config D)', random: 0.0047, imagenet: 0.4450, continual: 0.6807, delta: 0.2357, run2Delta: 0.2336, passed: true },
  ],
};

// Datasets — 7 entries (comprehensive)
export const DATASETS = [
  {
    name: 'EyePACS',
    tier: 'Training', tierColor: 'blue', status: 'active',
    size: '~35,126 labeled', sizeUsed: '~35,126 (100%)',
    camera: 'Canon CR-1', cameraType: 'Non-mydriatic', fov: '45°',
    resolution: '3888×2592 to 5184×3456', format: 'JPEG',
    taxonomy: '5-class ICDR (DR 0–4)', taxonomyMapping: null,
    source: 'Kaggle', availability: 'Public',
    population: 'US (multi-ethnic, California screening programme)',
    classDistribution: {
      'DR 0': { count: 25810, pct: 73.5 },
      'DR 1': { count: 2443, pct: 6.9 },
      'DR 2': { count: 5292, pct: 15.1 },
      'DR 3': { count: 873, pct: 2.5 },
      'DR 4': { count: 708, pct: 2.0 },
    },
    role: 'Primary training and evaluation dataset for Experiments 1 and 2. All models trained on EyePACS; serves as in-domain reference for generalization ratio G.',
    whyChosen: [
      'Largest publicly available DR dataset with 5-class grading — provides sufficient statistical power for 5-fold CV',
      'Single-camera acquisition (Canon CR-1) ensures training data has consistent imaging characteristics',
      'Bilateral image pairs (left + right eye per patient) enable patient-level splitting to prevent data leakage',
      'Severe class imbalance (73.5% DR 0) reflects real-world screening distribution — results are clinically realistic',
      'Widely used benchmark in DR classification literature — enables direct comparison with prior work',
    ],
    experiments: ['Exp 1 (H-1)', 'Exp 2 (H-2)'],
    limitations: [
      'Severe class imbalance: DR 3+4 together are only 4.5% of dataset',
      'Single screening programme — may not represent global population diversity',
      'Variable image quality — some images ungradable (~19.9% per Voets et al., 2019)',
    ],
    splitStrategy: '5-fold patient-level stratified CV. Patient ID = numeric prefix before _left/_right in filename. Both eyes of same patient always in same fold.',
  },
  {
    name: 'APTOS 2019',
    tier: 'Transfer', tierColor: 'blue', status: 'active',
    size: '3,662', sizeUsed: '3,662 (full, zero-shot transfer)',
    camera: 'Various (unspecified)', cameraType: 'Mixed', fov: 'Various',
    resolution: 'Various', format: 'PNG',
    taxonomy: '5-class ICDR (DR 0–4)', taxonomyMapping: null,
    source: 'Kaggle', availability: 'Public',
    population: 'Indian (Aravind Eye Hospital, rural screening)',
    classDistribution: {
      'DR 0': { count: 1805, pct: 49.3 },
      'DR 1': { count: 370, pct: 10.1 },
      'DR 2': { count: 999, pct: 27.3 },
      'DR 3': { count: 193, pct: 5.3 },
      'DR 4': { count: 295, pct: 8.1 },
    },
    role: 'Cross-dataset transferability target for Experiment 3 (H-4). Zero-shot transfer from EyePACS-trained model. Generalization ratio G = F1_APTOS / F1_EyePACS must meet G ≥ 0.85 threshold.',
    whyChosen: [
      'Large, well-known benchmark with 5-class DR grading matching EyePACS taxonomy',
      'Indian population data provides demographic diversity from EyePACS (US screening)',
      'Mixed camera sources test cross-device generalization within same experiment',
    ],
    experiments: ['Exp 3 (H-4): Cross-dataset transferability'],
    limitations: [
      'Mixed camera sources — domain shift from EyePACS expected',
      'No pixel-level annotations — cannot be used for explainability evaluation',
    ],
    splitStrategy: 'Zero-shot transfer — no training on APTOS 2019. Evaluated directly using EyePACS-trained model.',
  },
  {
    name: 'IDRiD',
    tier: 'Clinical', tierColor: 'teal', status: 'active',
    size: '516 images', sizeUsed: '516 (full) + 81 with pixel-level lesion masks',
    camera: 'Kowa VX-10α', cameraType: 'Mydriatic digital fundus camera', fov: '50°',
    resolution: '4288×2848', format: 'JPEG',
    taxonomy: '5-class ICDR (DR 0–4) + pixel-level lesion masks', taxonomyMapping: null,
    source: 'IEEE DataPort', availability: 'Public (CC-BY 4.0)',
    population: 'Indian (Sushrusha Hospital, Nanded, Maharashtra, 2009–2017)',
    classDistribution: {
      'DR 0': { count: 168, pct: 32.6 },
      'DR 1': { count: 25, pct: 4.8 },
      'DR 2': { count: 168, pct: 32.6 },
      'DR 3': { count: 93, pct: 18.0 },
      'DR 4': { count: 62, pct: 12.0 },
    },
    role: 'Multi-purpose clinical validation dataset: CLAHE parameter sweep (Exp 2), explainability analysis with pixel-level lesion masks (Exp 4), and cross-dataset transfer target (Exp 5).',
    whyChosen: [
      'ONLY publicly available dataset with pixel-level lesion segmentation masks for 4 lesion types (microaneurysms, hemorrhages, hard exudates, soft exudates) — essential for Grad-CAM ALO/IoU evaluation',
      'Different camera manufacturer (Kowa) from training data (Canon) — provides genuine cross-device transfer test',
      'High-resolution images (4288×2848) with 50° FOV — captures more retinal detail than EyePACS',
      'Expert-validated annotations: pixel-level masks reviewed by two retinal specialists with consensus-based finalization',
      'Reference paper (Porwal et al., 2018) is the standard dataset descriptor for DR lesion analysis benchmarks',
    ],
    experiments: ['Exp 2 (H-2): CLAHE sweep', 'Exp 4 (H-5): Grad-CAM explainability', 'Exp 5 (H-4): Transfer target'],
    lesionMasks: {
      types: ['Microaneurysms (MA)', 'Hemorrhages (HE)', 'Hard Exudates (EX)', 'Soft Exudates (SE)'],
      annotatedImages: 81,
      annotationTool: 'ADCIS Aphelion',
      validation: 'Two retinal specialists reviewed all masks; finalized upon consensus',
    },
    limitations: [
      'Small dataset (516 images) — limits statistical power for standalone training',
      'Only 81 images have pixel-level masks — Exp 4 uses 10 samples per class',
      'Single hospital, single camera — population and device bias',
    ],
    splitStrategy: 'Used as-is for evaluation (not split for training). 413 train / 103 test split provided by dataset authors.',
  },
  {
    name: 'Messidor-2',
    tier: 'External clinical', tierColor: 'purple', status: 'active',
    size: '1,748 images', sizeUsed: '1,748 (full)',
    camera: 'Topcon TRC NW6', cameraType: 'Non-mydriatic', fov: '45°',
    resolution: '1440×960 to 2240×1488', format: 'TIFF',
    taxonomy: 'Referable / Non-referable DR',
    taxonomyMapping: 'Messidor grade 0→DR 0, grade 1→DR 1, grade 2→DR 2. Grades 3–4 not directly available — binary referable/non-referable used for clinical screening evaluation.',
    source: 'ADCIS (upon registration)', availability: 'Public (registration required)',
    population: 'French (ophthalmology departments in Brest, Dijon, and Paris)',
    classDistribution: {
      'DR 0': { count: 1017, pct: 58.3 },
      'DR 1': { count: 270, pct: 15.5 },
      'DR 2': { count: 347, pct: 19.9 },
      'DR 3': { count: 75, pct: 4.3 },
      'DR 4': { count: 35, pct: 2.0 },
    },
    role: 'External generalization target for Experiment 5 (H-4). Model trained on EyePACS is evaluated on Messidor-2 without retraining to compute generalization ratio G.',
    whyChosen: [
      'Different camera manufacturer (Topcon) from training data (Canon CR-1) — genuine cross-device evaluation',
      'Different population (French) from training data (US) — tests demographic generalization',
      'Well-established benchmark used by Gulshan et al. (JAMA 2016), Voets et al. (2019), and others — enables literature comparison',
      'Clean image quality with standardized acquisition protocol',
    ],
    experiments: ['Exp 5 (H-4): Transfer target'],
    limitations: [
      'Taxonomy mismatch: original grading is referable/non-referable, not 5-class ICDR',
      'Label mapping introduces approximation — Messidor grades 0–2 mapped to DR 0–2; grades 3–4 not directly available',
      'Registration-gated access limits perfect reproducibility',
    ],
    splitStrategy: 'Used entirely as external test set (no training on this data).',
  },
  {
    name: 'DDR',
    tier: 'Domain', tierColor: 'coral', status: 'active',
    size: '13,673 images', sizeUsed: '13,673 (full)',
    camera: 'Canon, Topcon (mixed)', cameraType: 'Various', fov: 'Various',
    resolution: 'Various', format: 'JPEG',
    taxonomy: '6-class DR (0–5) + lesion annotations',
    taxonomyMapping: 'DDR grade 5 (ungradable) excluded. Grades 0–4 map directly to ICDR 0–4.',
    source: 'GitHub (Li et al., 2019)', availability: 'Public',
    population: 'Chinese (multi-centre hospital collection)',
    classDistribution: {
      'DR 0': { count: 6266, pct: 50.0 },
      'DR 1': { count: 630, pct: 5.0 },
      'DR 2': { count: 4477, pct: 35.8 },
      'DR 3': { count: 236, pct: 1.9 },
      'DR 4': { count: 913, pct: 7.3 },
    },
    role: 'Device domain shift evaluation for Experiment 6 (H-6). Tests cross-camera performance with mixed Canon+Topcon acquisition.',
    whyChosen: [
      'Contains images from BOTH Canon and Topcon cameras — tests performance when training domain (Canon CR-1) partially overlaps with test device mix',
      'Large dataset (13,673) provides robust cross-device performance estimates',
      'Native 5-class DR grading (after excluding grade 5) — minimal taxonomy mapping required',
      'Different population (Chinese) from training data (US) — adds demographic diversity to device-shift analysis',
    ],
    experiments: ['Exp 6 (H-6): Device shift'],
    limitations: [
      'Per-image camera metadata not publicly available — cannot separate Canon vs. Topcon subsets',
      'Grade 5 (ungradable) images excluded, introducing potential selection bias',
    ],
    splitStrategy: 'Provided train/test/valid splits used. Evaluated as external test set.',
  },
  {
    name: 'ODIR-5K',
    tier: 'Domain', tierColor: 'coral', status: 'active',
    size: '5,000 patients (bilateral)', sizeUsed: 'DR subset extracted via keyword mapping',
    camera: 'Canon, Zeiss (mixed)', cameraType: 'Various', fov: 'Various',
    resolution: 'Various', format: 'JPEG',
    taxonomy: 'Multi-disease diagnostic keywords',
    taxonomyMapping: 'Keyword-to-grade mapping: "proliferative DR"→4, "severe DR"→3, "moderate DR"→2, "mild DR"→1, unqualified "DR"→2 (conservative), "laser spot"→4. Non-DR eyes of DR patients excluded.',
    source: 'Peking University (ODIR competition)', availability: 'Public',
    population: 'Chinese (multi-hospital, Beijing)',
    classDistribution: {
      'DR 1': { count: 549, pct: 30.2 },
      'DR 2': { count: 1056, pct: 58.1 },
      'DR 3': { count: 161, pct: 8.9 },
      'DR 4': { count: 52, pct: 2.9 },
    },
    role: 'Device domain shift evaluation for Experiment 6 (H-6). Tests cross-camera performance with Canon+Zeiss acquisition — Zeiss cameras are not present in any other dataset.',
    whyChosen: [
      'Contains Zeiss camera images — the ONLY dataset in our architecture with Zeiss acquisition, providing maximum device diversity',
      'Bilateral format (both eyes per patient) provides patient-level evaluation consistency',
      'Canon+Zeiss combination creates maximum domain distance from training data (Canon CR-1 only)',
    ],
    experiments: ['Exp 6 (H-6): Device shift'],
    limitations: [
      'Multi-disease taxonomy requires keyword-to-DR-grade mapping — introduces label noise',
      'Not all keyword mappings are unambiguous (e.g., "diabetic retinopathy" without severity → mapped conservatively to DR 2)',
      'Per-image camera metadata not available — cannot separate Canon vs. Zeiss subsets',
      'Bilateral images may have different pathologies per eye — patient-level label aggregation needed',
    ],
    splitStrategy: 'DR subset extracted via keyword filtering. Used as external evaluation set.',
  },
  {
    name: 'Clinical KZ',
    tier: 'Local', tierColor: 'amber', status: 'active',
    size: '60 images (30 patients)', sizeUsed: '60 (held-out test for Exp 7)',
    camera: 'Topcon-class (inferred)', cameraType: 'Non-mydriatic', fov: '~45°',
    resolution: 'Same 3-resolution profile as Messidor-2', format: 'JPEG',
    taxonomy: '5-class ICDR (DR 0–4) — fully balanced', taxonomyMapping: null,
    source: 'Almaty medical centre (private)', availability: 'Restricted (institutional)',
    population: 'Kazakhstan (Almaty regional clinic)',
    classDistribution: {
      'DR 0': { count: 12, pct: 20.0 },
      'DR 1': { count: 12, pct: 20.0 },
      'DR 2': { count: 12, pct: 20.0 },
      'DR 3': { count: 12, pct: 20.0 },
      'DR 4': { count: 12, pct: 20.0 },
    },
    role: 'Local Kazakhstan clinical validation set for Experiment 7 (small-data training). Held-out test set after IDRiD 5-fold CV; 30 patients, fully balanced across DR 0–4.',
    whyChosen: [
      'Regional Kazakhstan acquisition — tests model performance on the target deployment population',
      'Fully balanced 5-class distribution (12 images per grade) — controlled evaluation without imbalance confound',
      'Same 3-resolution profile as Messidor-2 — enables Topcon-class camera inference even without EXIF',
      'Validates the regional clinical use-case described in dissertation practical significance',
    ],
    experiments: ['Exp 7: Small data clinical training'],
    limitations: [
      'Very small sample (60 images, 30 patients) — limits statistical power for fine-grained per-class analysis',
      'Single regional clinic — does not represent all Kazakhstan populations',
      'No pixel-level lesion annotations',
    ],
    splitStrategy: 'Held out as evaluation set only — never used in training. IDRiD provides training pool with 5-fold CV.',
  },
  {
    name: 'RFMiD',
    tier: 'Domain', tierColor: 'coral', status: 'active',
    size: '3,200 images', sizeUsed: 'DR subset (binary: DR present / absent)',
    camera: 'Topcon, Kowa (mixed)', cameraType: 'Various', fov: 'Various',
    resolution: 'Various', format: 'PNG',
    taxonomy: 'Multi-disease with binary DR column (0/1)',
    taxonomyMapping: 'Uses binary DR label only (0 = no DR, 1 = DR present). 5-class severity grading not available — evaluated as binary classification or excluded from per-class analysis.',
    source: 'IEEE DataPort', availability: 'Public',
    population: 'Indian (multi-centre)',
    classDistribution: {
      'DR absent': { count: 2568, pct: 80.3 },
      'DR present': { count: 632, pct: 19.8 },
    },
    role: 'Device domain shift evaluation for Experiment 6 (H-6). Tests cross-camera performance with Topcon+Kowa acquisition.',
    whyChosen: [
      'Contains BOTH Topcon and Kowa cameras — matches the camera from IDRiD (Kowa) and Messidor-2 (Topcon) in a single dataset',
      'Multi-disease taxonomy with DR column enables focused DR analysis',
      'Topcon+Kowa combination creates significant domain distance from training data (Canon CR-1)',
    ],
    experiments: ['Exp 6 (H-6): Device shift'],
    limitations: [
      'Binary DR labels only (present/absent) — no severity grading available',
      'Multi-disease dataset — DR is one of many conditions, limiting DR-focused analysis depth',
      'Per-image camera metadata not available',
    ],
    splitStrategy: 'Provided train/validation/test splits. DR subset used as external evaluation set.',
  },
];

export const CAMERA_GROUPS = {
  'Canon':  ['EyePACS', 'DDR', 'ODIR-5K'],
  'Topcon': ['Messidor-2', 'RFMiD', 'DDR'],
  'Kowa':   ['IDRiD', 'RFMiD'],
  'Zeiss':  ['ODIR-5K'],
};

// Camera distribution comparison (slide 14): Central Asia regional clinics vs training datasets
export const CAMERA_DISTRIBUTION = {
  centralAsia: {
    label: 'Central Asia clinics (n=36)',
    Topcon: 53,
    Canon:  31,
    Zeiss:  14,
    Kowa:   2,
  },
  training: {
    label: 'Training datasets (brand share)',
    Canon:  36,
    Topcon: 36,
    Kowa:   18,
    Zeiss:  9,
    Other:  1,
  },
  coverage: {
    centralAsia: { label: 'Topcon + Canon coverage of Central Asia clinics', value: 83 },
    training:    { label: 'Topcon + Canon coverage of training data',       value: 73 },
  },
};

// Resolution-based camera analysis — computed from actual image files
export const RESOLUTION_ANALYSIS = {
  'EyePACS': {
    total: 35126, uniqueResolutions: 22, camera: 'Canon CR-1',
    note: 'Single camera, multiple settings/modes',
    groups: [
      { res: '3888×2592', count: 594, pctSampled: 29.7, note: 'Canon CR-1 standard' },
      { res: '4752×3168', count: 332, pctSampled: 16.6 },
      { res: '2560×1920', count: 250, pctSampled: 12.5 },
      { res: '2592×1944', count: 232, pctSampled: 11.6 },
      { res: '3504×2336', count: 212, pctSampled: 10.6 },
    ],
    sampled: 2000,
  },
  'IDRiD': {
    total: 516, uniqueResolutions: 1, camera: 'Kowa VX-10α',
    note: 'Single camera, single resolution — most uniform dataset',
    groups: [
      { res: '4288×2848', count: 516, pct: 100.0, note: 'Kowa VX-10α native' },
    ],
  },
  'Messidor-2': {
    total: 1748, uniqueResolutions: 3, camera: 'Topcon TRC NW6',
    note: '3 resolutions = 3 French ophthalmology centres (Brest, Dijon, Paris)',
    groups: [
      { res: '2240×1488', count: 616, pct: 35.2, note: 'Centre A' },
      { res: '2304×1536', count: 604, pct: 34.6, note: 'Centre B' },
      { res: '1440×960',  count: 528, pct: 30.2, note: 'Centre C' },
    ],
  },
  'DDR': {
    total: 13673, uniqueResolutions: 132, camera: 'Canon + Topcon (mixed)',
    note: '132 unique resolutions — strongest evidence of multi-device acquisition',
    groups: [
      { res: '2592×1728', count: 2265, pct: 16.6 },
      { res: '2736×1824', count: 2191, pct: 16.0 },
      { res: '2048×1536', count: 1682, pct: 12.3 },
      { res: '2304×1728', count: 1120, pct: 8.2 },
      { res: '3888×2592', count: 677, pct: 5.0, note: 'Matches EyePACS Canon CR-1' },
      { res: '3264×2448', count: 640, pct: 4.7 },
      { res: '2960×2935', count: 556, pct: 4.1 },
      { res: '1956×1934', count: 482, pct: 3.5 },
      { res: '1380×1382', count: 431, pct: 3.2 },
      { res: '2992×2000', count: 387, pct: 2.8 },
    ],
  },
  'ODIR-5K': {
    total: 7000, uniqueResolutions: 101, camera: 'Canon + Zeiss (mixed)',
    note: '101 unique resolutions — multi-hospital Beijing collection',
    groups: [
      { res: '2592×1728', count: 2146, pct: 30.7, note: 'Dominant group' },
      { res: '2048×1536', count: 524, pct: 7.5 },
      { res: '2304×1728', count: 424, pct: 6.1 },
      { res: '1956×1934', count: 390, pct: 5.6 },
      { res: '2736×1824', count: 344, pct: 4.9 },
      { res: '1936×1296', count: 284, pct: 4.1 },
      { res: '1444×1444', count: 267, pct: 3.8, note: 'Square — likely Zeiss' },
      { res: '3456×2304', count: 258, pct: 3.7 },
      { res: '2976×1984', count: 212, pct: 3.0 },
      { res: '1536×1152', count: 198, pct: 2.8 },
    ],
  },
  'RFMiD': {
    total: 3200, uniqueResolutions: 3, camera: 'Topcon + Kowa (mixed)',
    note: 'Only 3 resolutions — camera split identifiable',
    groups: [
      { res: '2144×1424', count: 2427, pct: 75.8, note: 'Likely Topcon' },
      { res: '4288×2848', count: 497, pct: 15.5, note: 'Matches IDRiD Kowa VX-10α exactly' },
      { res: '2048×1536', count: 276, pct: 8.6, note: 'Likely Topcon (alt. model)' },
    ],
  },
  'APTOS 2019': {
    total: 3662, uniqueResolutions: 17, camera: 'Various (unspecified)',
    note: '17 resolutions — multiple unidentified camera sources',
    groups: [
      { res: '1050×1050', count: 974, pct: 26.6, note: 'Square crop — post-processed?' },
      { res: '2416×1736', count: 638, pct: 17.4 },
      { res: '2588×1958', count: 533, pct: 14.6 },
      { res: '3216×2136', count: 410, pct: 11.2 },
      { res: '2048×1536', count: 351, pct: 9.6 },
      { res: '819×614',   count: 287, pct: 7.8, note: 'Low resolution' },
      { res: '3388×2588', count: 141, pct: 3.9 },
    ],
  },
  'Clinical': {
    total: 60, uniqueResolutions: 3, camera: 'Topcon-type (inferred)',
    note: 'Same 3 resolutions as Messidor-2 — same camera model family',
    groups: [
      { res: '2240×1488', count: 23, pct: 38.3, note: 'Matches Messidor-2 Centre A' },
      { res: '2304×1536', count: 21, pct: 35.0, note: 'Matches Messidor-2 Centre B' },
      { res: '1440×960',  count: 16, pct: 26.7, note: 'Matches Messidor-2 Centre C' },
    ],
  },
};

export const DATASET_TIERS = [
  { name: 'Training', color: 'blue', description: 'Primary training and evaluation', datasets: ['EyePACS'] },
  { name: 'Transfer', color: 'blue', description: 'Cross-dataset transferability (H-4)', datasets: ['APTOS 2019'] },
  { name: 'Clinical', color: 'teal', description: 'Lesion masks + parameter validation + small data', datasets: ['IDRiD'] },
  { name: 'External clinical', color: 'purple', description: 'External clinical performance (H-7)', datasets: ['Messidor-2'] },
  { name: 'Domain', color: 'coral', description: 'Device domain shift evaluation (H-6)', datasets: ['DDR', 'ODIR-5K', 'RFMiD'] },
  { name: 'Local', color: 'amber', description: 'Regional KZ clinical validation (Exp 7)', datasets: ['Clinical KZ'] },
];

// Publications — 5 total (1 Scopus Q3, 1 Scopus conference, 3 KZ VAK journals)
export const PUBLICATIONS = [
  {
    tier: 'Scopus Q3', tierColor: 'teal', year: '2025',
    authors: 'Sapakova S., Yesmukhamedov N., Sapakov A.',
    title: 'Development of an Image Quality Enhancement Approach for Diabetic Retinopathy Diagnosis',
    venue: 'Eastern-European Journal of Enterprise Technologies',
    details: 'Vol. 4, No. 9(136). — P. 79–88.',
    type: 'Journal',
  },
  {
    tier: 'Scopus Conf.', tierColor: 'blue', year: '2025',
    authors: 'Sapakova S., Yesmukhamedov N. et al.',
    title: 'Methods for Pre-processing and Analysis of Fundus Images',
    venue: 'Procedia Computer Science (Elsevier) — DS-2025, Istanbul',
    details: 'Vol. 272. — P. 496–501.',
    type: 'Conference',
  },
  {
    tier: 'KZ VAK', tierColor: 'purple', year: '2025',
    authors: 'Yesmukhamedov N.S. et al.',
    title: 'Methods for Preprocessing and Analysis of Fundus Images',
    venue: 'Herald of KBTU',
    details: 'No. 4(75). — P. 119–130.',
    type: 'Journal',
  },
  {
    tier: 'KZ VAK', tierColor: 'purple', year: '2025',
    authors: 'Yesmukhamedov N.S. et al.',
    title: 'Development of an IS Architecture for Healthcare',
    venue: 'News of NAN RK',
    details: 'No. 2(354). — P. 74–91.',
    type: 'Journal',
  },
  {
    tier: 'KZ VAK', tierColor: 'purple', year: '2024',
    authors: 'Sapakova S.Z. et al.',
    title: 'Mathematical Modeling of Laser Exposure',
    venue: 'Vestnik KazUTB',
    details: 'Vol. 2, No. 27-740.',
    type: 'Journal',
  },
];

// Hypotheses — all 7 confirmed, none refuted.
// Source: results/findings/summary-and-dominance.md
export const HYPOTHESES = [
  { id: 'H-1', name: 'Integrated Pipeline Dominance', exp: 'Exp 1', status: '✓ Confirmed', detail: 'EH-3 met on both backbones: ΔF1 +6.54/+6.55pp, ΔAUC +0.032/+0.036, Δκ +0.113/+0.110. Holm-corrected p ≤ 0.0082; no arm×backbone interaction (p=0.31)' },
  { id: 'H-2', name: 'Component Ablation + CLAHE/σ Sensitivity', exp: 'Exp 2', status: '✓ Confirmed', detail: 'Interior optima θ*=(clip 2.5, threshold 0.03) and σ*=0.07·D, both confirmed on held-out. All 7 ablation transitions exceed the 2·σ_fold band, and the hierarchy is resolvable: flat-field (+1.43pp) and CLAHE (+1.25pp) lead, together 41% of the total gain' },
  { id: 'H-3', name: 'Domain Distance Reduction', exp: 'MMD / KL', status: '✓ Confirmed', detail: 'MMD falls for all 6 target domains (Δd +0.070…+0.093, every CI excludes zero); KL −34…−38%. Stage 7 uses source-domain statistics, so the closing is done by stages 0–6. Direction only — the size of the reduction does not track the size of the gain (ρ≈0.49)' },
  { id: 'H-4', name: 'Cross-Dataset Transfer (APTOS)', exp: 'Exp 3', status: '✓ Confirmed', detail: 'G=0.8976 ≥ 0.85 and above baseline (0.8577); APTOS F1 +0.0889 (CI [+0.068, +0.120]). Caveat: the baseline clears the threshold too — the discriminating part is "better than baseline"' },
  { id: 'H-5', name: 'Explainability (ALO)', exp: 'Exp 4', status: '✓ Confirmed', detail: 'All 4 lesion types improve directionally AND significantly (p 0.0007–0.0148); IoU agrees; stable for τ=0.2…0.7; floor effect only 6/54. Stays within NC-14: this is attention alignment, not clinical localization' },
  { id: 'H-6', name: 'Device Domain Shift', exp: 'Exp 6', status: '✓ Confirmed', detail: 'All 5 camera groups clear the 0.70 floor for both arms; between-device std falls 2.4× for F1 and 3.1× for AUC (both CIs exclude zero). The pipeline lifts the worst devices most' },
  { id: 'H-7', name: 'External Clinical Performance', exp: 'Exp 5', status: '✓ Confirmed (2 of 2)', detail: 'Δ wF1(D−C) ≥ MCID 0.050 with CI⁻ > 0 on both sets: IDRiD +0.0689 [+0.049, +0.097] p=0.0021, Messidor-2 +0.0541 [+0.036, +0.081] p=0.0138. Caveat: the Messidor-2 margin over the MCID is only 0.0041 — a real pass, not a comfortable one' },
];

// Exp 7 sits outside the formal H-1…H-7 set (preregistered small-data comparison).
export const EXTRA_RESULTS = [
  { id: 'E-7', name: 'Small-Data Trainability', exp: 'Exp 7', status: '✓ Positive', detail: 'IDRiD (n=516) → Clinical KZ (n=60): +0.080 weighted F1, +0.125 κ, +0.048 AUC, all paired CIs exclude zero. Preregistered. The gain matches the full-EyePACS gain, so it is not specific to small data' },
  { id: 'A-1', name: 'SSL Linear-Probe Gate', exp: 'SSL', status: '✓ Passed', detail: 'From-scratch BYOL/MoCo-v2/DINO fail the gate (κ ≤ 0.113 vs ImageNet 0.34–0.45) and more epochs do not help; SIP passes (κ=0.662). Continual-SSL gains on BOTH backbones (Δκ +0.317 / +0.236)' },
];
