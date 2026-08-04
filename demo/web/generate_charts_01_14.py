"""
Generate result charts 01–14 for the DR Diagnosis Dashboard.
All data from data.js constants. Output: demo/web/public/results/
"""
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, 'public', 'results')
os.makedirs(OUT, exist_ok=True)
DPI = 200

# ─── Color Palette (from data.js C) ───
BLUE = '#378ADD'
TEAL = '#1D9E75'
CORAL = '#D85A30'
PURPLE = '#7F77DD'
AMBER = '#EF9F27'
GRAY = '#888780'
GREEN = '#639922'
RED = '#E24B4A'

# ─── Data (mirrors src/data.js, sourced from results/tables/) ───
CONFIGS = {
    'A': {'f1': 0.7518, 'f1s': 0.0110, 'auc': 0.8300, 'aucs': 0.0140, 'k': 0.7410, 'ks': 0.0350, 'acc': 0.7247,
          'lbl': 'A: Baseline + ResNet-50'},
    'B': {'f1': 0.8172, 'f1s': 0.0090, 'auc': 0.8620, 'aucs': 0.0110, 'k': 0.8539, 'ks': 0.0260, 'acc': 0.8027,
          'lbl': 'B: Pipeline + ResNet-50'},
    'C': {'f1': 0.7538, 'f1s': 0.0120, 'auc': 0.8210, 'aucs': 0.0150, 'k': 0.7468, 'ks': 0.0330, 'acc': 0.7273,
          'lbl': 'C: Baseline + EfficientNet-B3'},
    'D': {'f1': 0.8193, 'f1s': 0.0100, 'auc': 0.8570, 'aucs': 0.0120, 'k': 0.8571, 'ks': 0.0270, 'acc': 0.8052,
          'lbl': 'D: Pipeline + EfficientNet-B3'},
}

# 8-level cumulative ablation, EyePACS 100%, 5 folds, single shared initialization.
# L0 reproduces Config C (0.7538) and L7 reproduces Config D (0.8193).
ABL = [
    {'n': 'Baseline', 'f1': 0.7538, 'auc': 0.8210},
    {'n': '+Canonical flip', 'f1': 0.7609, 'auc': 0.8260},
    {'n': '+OD-fovea rot.', 'f1': 0.7677, 'auc': 0.8299},
    {'n': '+FOV crop + mask', 'f1': 0.7759, 'auc': 0.8360},
    {'n': '+Flat-field', 'f1': 0.7902, 'auc': 0.8436},
    {'n': '+CLAHE', 'f1': 0.8027, 'auc': 0.8505},
    {'n': '+Augmentation', 'f1': 0.8128, 'auc': 0.8541},
    {'n': 'Full pipeline', 'f1': 0.8193, 'auc': 0.8570},
]

# Marginal contribution of each stage (pp). All 7 exceed the 2*sigma_fold band, and the
# spread (0.65-1.43pp, about 3*sigma_fold) makes the hierarchy resolvable: the two
# photometric stages lead and together carry 41% of the +6.55pp total.
ABL_INDIV = [
    {'stage': 'Stage 0: Canonical flip', 'f1': 0.71},
    {'stage': 'Stage 1: OD-fovea rot.', 'f1': 0.68},
    {'stage': 'Stages 2-3: FOV crop+mask', 'f1': 0.82},
    {'stage': 'Stage 4: Flat-field', 'f1': 1.43},
    {'stage': 'Stage 5: CLAHE', 'f1': 1.25},
    {'stage': 'Stage 6: Augmentation', 'f1': 1.01},
    {'stage': 'Stage 7: Normalize', 'f1': 0.65},
]

# All 54 mask-carrying IDRiD images, tau = 0.5. All four types significant.
ALO = [
    {'l': 'Microaneurysms', 'ab': 0.2126, 'ap': 0.3160},
    {'l': 'Hemorrhages', 'ab': 0.2794, 'ap': 0.4011},
    {'l': 'Hard exudates', 'ab': 0.3502, 'ap': 0.4790},
    {'l': 'Soft exudates', 'ab': 0.2318, 'ap': 0.3310},
]

IOU = [
    {'l': 'Microaneurysms', 'b': 0.1065, 'p': 0.1694},
    {'l': 'Hemorrhages', 'b': 0.1516, 'p': 0.2229},
    {'l': 'Hard exudates', 'b': 0.1944, 'p': 0.2830},
    {'l': 'Soft exudates', 'b': 0.1183, 'p': 0.1775},
]

GEN = [
    {'d': 'EyePACS (train)', 'fb': 0.7538, 'fp': 0.8193},
    {'d': 'APTOS 2019', 'fb': 0.6465, 'fp': 0.7354},
    {'d': 'IDRiD', 'fb': 0.5938, 'fp': 0.6627},
    {'d': 'Messidor-2', 'fb': 0.6282, 'fp': 0.6823},
]
# IDRiD / Messidor-2 AUC come from the exp6 camera groups kowa_idrid / topcon_messidor2.
GEN_AUC = [
    {'d': 'EyePACS (train)', 'b': 0.8210, 'p': 0.8570},
    {'d': 'APTOS 2019', 'b': 0.7940, 'p': 0.8263},
    {'d': 'IDRiD', 'b': 0.8195, 'p': 0.8627},
    {'d': 'Messidor-2', 'b': 0.8407, 'p': 0.8729},
]

# G is normalized by each arm's own in-domain F1. The 0.85 threshold belongs to H-4 (APTOS);
# for the clinical sets the applicable floor is the H-6 device floor of 0.70.
G_RATIO = [
    {'d': 'APTOS 2019', 'Gb': 0.8577, 'Gp': 0.8976},
    {'d': 'IDRiD', 'Gb': 0.7877, 'Gp': 0.8089},
    {'d': 'Messidor-2', 'Gb': 0.8334, 'Gp': 0.8328},
]

DEV = [
    {'c': 'Canon CR-1\n(EyePACS)', 'fb': 0.7538, 'fp': 0.8193},
    {'c': 'Topcon\n(Messidor-2)', 'fb': 0.6282, 'fp': 0.6823},
    {'c': 'Kowa\n(IDRiD)', 'fb': 0.5938, 'fp': 0.6627},
    {'c': 'Canon+Topcon\n(DDR)', 'fb': 0.6154, 'fp': 0.6671},
    {'c': 'Canon+Zeiss\n(ODIR-5K)', 'fb': 0.5700, 'fp': 0.6581},
    {'c': 'Topcon+Kowa\n(RFMiD)', 'fb': 0.5434, 'fp': 0.6421},
]

# Referable DR (grade >= 2), EyePACS in-domain, Config C vs D.
CLIN = [
    {'m': 'Sensitivity', 'b': 0.6891, 'v': 0.8007},
    {'m': 'Specificity', 'b': 0.9455, 'v': 0.9636},
    {'m': 'PPV', 'b': 0.7545, 'v': 0.8427},
    {'m': 'NPV', 'b': 0.9259, 'v': 0.9521},
]

# Joint CLAHE grid on EyePACS: rows = clip_factor 0.5..4.0, cols = global_threshold 0.01..0.05.
CLAHE_CLIP = ['0.5', '1.0', '1.5', '2.0', '2.5', '3.0', '3.5', '4.0']
CLAHE1 = [
    [.2696, .2895, .3128, .2986, .2807],
    [.3176, .3524, .3689, .3567, .3396],
    [.3593, .3910, .4094, .4026, .3820],
    [.3788, .4183, .4393, .4299, .4091],
    [.4011, .4390, .4693, .4584, .4292],
    [.3911, .4329, .4497, .4381, .4191],
    [.3715, .4101, .4299, .4168, .3978],
    [.3516, .3791, .4003, .3903, .3719],
]
CLAHE2 = [
    [.4415, .4587, .4785, .4680, .4492],
    [.4792, .5102, .5295, .5189, .4987],
    [.5187, .5489, .5794, .5734, .5389],
    [.5406, .5822, .6219, .6090, .5700],
    [.5315, .5697, .5968, .5879, .5585],
    [.5119, .5478, .5705, .5586, .5427],
    [.4906, .5296, .5478, .5387, .5201],
    [.4725, .4998, .5180, .5087, .4886],
]


def setup_style():
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': ['DejaVu Sans', 'Helvetica', 'Arial'],
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.grid': False,
        'figure.facecolor': 'white',
    })

setup_style()


# Chart number -> subdirectory under public/results/. The dashboard loads figures from these
# per-experiment subdirectories (e.g. '/results/exp2/04_exp2_ablation.png'), so writing flat
# into public/results/ would leave the app serving the previous render.
ROUTE = {
    '01': 'exp1', '02': 'exp1', '03': 'exp1', '18': 'exp1',
    '19': 'exp1', '20': 'exp1', '22': 'exp1', '24': 'exp1',
    '04': 'exp2', '05': 'exp2', '13': 'exp2', '23': 'exp2',
    '29': 'exp3',
    '06': 'exp4', '07': 'exp4', '27': 'exp4', '28': 'exp4',
    '08': 'exp5', '09': 'exp5',
    '10': 'exp6',
    '30': 'exp7',
    '11': 'general', '12': 'general', '14': 'general', '15': 'general',
    '16': 'general', '17': 'general', '21': 'general', '25': 'general', '26': 'general',
}


def save(fig, name):
    subdir = ROUTE.get(name[:2], '')
    out_dir = os.path.join(OUT, subdir) if subdir else OUT
    os.makedirs(out_dir, exist_ok=True)
    fig.savefig(os.path.join(out_dir, name), dpi=DPI, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close(fig)
    print(f"  [OK] {subdir}/{name}" if subdir else f"  [OK] {name}")


# ─── Chart 01 ───
def chart_01():
    fig, ax = plt.subplots(figsize=(8, 5))
    labels = ['A', 'B', 'C', 'D']
    vals = [CONFIGS[k]['f1'] for k in labels]
    errs = [CONFIGS[k]['f1s'] for k in labels]
    colors = [GRAY, BLUE, GRAY, TEAL]
    x = np.arange(len(labels))
    bars = ax.bar(x, vals, yerr=errs, capsize=4, color=colors, width=0.6, edgecolor='white', linewidth=0.5)
    for i, bar in enumerate(bars):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + errs[i] + 0.005,
                f'{vals[i]:.3f}\n({CONFIGS[labels[i]]["f1s"]:.3f})',
                ha='center', va='bottom', fontsize=9)
    # Threshold lines: +5pp above each baseline
    ax.axhline(y=CONFIGS['A']['f1'] + 0.05, color=RED, linestyle='--', linewidth=1, alpha=0.7)
    ax.text(3.45, CONFIGS['A']['f1'] + 0.05 + 0.003, 'EH-3: +5pp (ResNet)', fontsize=7, color=RED, ha='right')
    ax.axhline(y=CONFIGS['C']['f1'] + 0.05, color=RED, linestyle='--', linewidth=1, alpha=0.5)
    ax.text(3.45, CONFIGS['C']['f1'] + 0.05 + 0.003, 'EH-3: +5pp (EffNet)', fontsize=7, color=RED, ha='right')
    ax.set_xticks(x)
    ax.set_xticklabels([CONFIGS[k]['lbl'] for k in labels], fontsize=8, rotation=15, ha='right')
    ax.set_ylabel('Weighted F1-Score', fontsize=11)
    ax.set_ylim(0.65, 0.85)
    ax.set_title('Experiment 1: 2x2 Factorial Design -- Weighted F1', fontsize=13, fontweight='bold')
    legend_patches = [
        mpatches.Patch(color=GRAY, label='Baseline (3ch)'),
        mpatches.Patch(color=BLUE, label='Pipeline + ResNet-50'),
        mpatches.Patch(color=TEAL, label='Pipeline + EfficientNet-B3'),
    ]
    ax.legend(handles=legend_patches, fontsize=8, loc='upper left')
    save(fig, '01_exp1_factorial_f1.png')


# ─── Chart 02 ───
def chart_02():
    metrics = [('Weighted F1', 'f1', 'f1s'), ('ROC-AUC', 'auc', 'aucs'),
               ("Cohen's kappa", 'k', 'ks'), ('Accuracy', 'acc', None)]
    fig, axes = plt.subplots(1, 4, figsize=(16, 4.5))
    fig.suptitle('Experiment 1 -- All Primary Metrics by Configuration', fontsize=14, fontweight='bold')
    labels = ['A', 'B', 'C', 'D']
    colors = [GRAY, BLUE, GRAY, TEAL]
    for idx, (title, key, std_key) in enumerate(metrics):
        ax = axes[idx]
        vals = [CONFIGS[k][key] for k in labels]
        errs = [CONFIGS[k][std_key] for k in labels] if std_key else [0]*4
        x = np.arange(4)
        bars = ax.bar(x, vals, yerr=errs if std_key else None, capsize=3, color=colors, width=0.6, edgecolor='white')
        for i, bar in enumerate(bars):
            yoff = errs[i] + 0.005 if std_key else 0.005
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + yoff,
                    f'{vals[i]:.3f}', ha='center', va='bottom', fontsize=8)
        ax.set_xticks(x)
        ax.set_xticklabels(labels, fontsize=9)
        ax.set_title(title, fontsize=11)
        ax.set_ylim(0.55, 0.95)
    plt.tight_layout(rect=[0, 0, 1, 0.92])
    save(fig, '02_exp1_all_metrics.png')


# ─── Chart 03 ───
def chart_03():
    fig, ax = plt.subplots(figsize=(8, 5))
    metrics = ['dF1', 'dAUC', 'dk']
    metric_labels = ['$\\Delta$F1 (pp)', '$\\Delta$AUC (pp)', '$\\Delta\\kappa$ (pp)']
    resnet = [5.2, 3.3, 8.0]
    effnet = [5.3, 4.4, 8.0]
    thresholds = [5.0, 2.0, 0.0]
    x = np.arange(len(metrics))
    w = 0.3
    b1 = ax.bar(x - w/2, resnet, w, color=BLUE, label='ResNet-50 (B-A)', edgecolor='white')
    b2 = ax.bar(x + w/2, effnet, w, color=TEAL, label='EfficientNet-B3 (D-C)', edgecolor='white')
    for i, (bar, val) in enumerate(zip(b1, resnet)):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2, f'+{val:.1f}',
                ha='center', va='bottom', fontsize=10, fontweight='bold', color=BLUE)
    for i, (bar, val) in enumerate(zip(b2, effnet)):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2, f'+{val:.1f}',
                ha='center', va='bottom', fontsize=10, fontweight='bold', color=TEAL)
    # Threshold lines
    for i, t in enumerate(thresholds):
        xmin = (x[i] - 0.4) / (len(x) - 1 + 0.8) + 0.4/(len(x)-1+0.8) if len(x) > 1 else 0.1
    ax.axhline(y=5.0, color=RED, linestyle='--', linewidth=1, alpha=0.7)
    ax.text(2.55, 5.15, 'EH-3: 5pp ($\\Delta$F1)', fontsize=7, color=RED)
    ax.axhline(y=2.0, color=RED, linestyle='--', linewidth=1, alpha=0.5)
    ax.text(2.55, 2.15, 'EH-3: 2pp ($\\Delta$AUC)', fontsize=7, color=RED)
    ax.axhline(y=0.0, color=RED, linestyle='--', linewidth=1, alpha=0.3)
    ax.text(2.55, 0.15, 'EH-3: 0pp ($\\Delta\\kappa$)', fontsize=7, color=RED)
    ax.set_xticks(x)
    ax.set_xticklabels(metric_labels, fontsize=11)
    ax.set_ylabel('Improvement (percentage points)', fontsize=11)
    ax.set_ylim(-0.5, 10.5)
    ax.set_title('Preprocessing Effect: $\\Delta$ (Pipeline - Baseline)', fontsize=13, fontweight='bold')
    ax.legend(fontsize=9)
    save(fig, '03_exp1_delta.png')


# ─── Chart 04 ───
def chart_04():
    fig, ax = plt.subplots(figsize=(10, 5))
    names = [a['n'] for a in ABL]
    vals = [a['f1'] for a in ABL]
    n = len(vals)
    colors_list = [GRAY] + [BLUE]*(n-2) + [TEAL]
    x = np.arange(n)
    bars = ax.bar(x, vals, color=colors_list, width=0.65, edgecolor='white')
    # Marginal deltas
    for i in range(1, n):
        delta = (vals[i] - vals[i-1]) * 100
        ax.annotate(f'+{delta:.1f}pp', xy=(i, vals[i] + 0.003),
                    fontsize=8, ha='center', va='bottom', color=CORAL, fontweight='bold')
    for i, bar in enumerate(bars):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.012,
                f'{vals[i]:.3f}', ha='center', va='bottom', fontsize=8)
    ax.set_xticks(x)
    ax.set_xticklabels(names, fontsize=8, rotation=25, ha='right')
    ax.set_ylabel('Weighted F1-Score', fontsize=11)
    ax.set_ylim(0.70, 0.82)
    ax.set_title('Experiment 2: Cumulative Ablation -- Pipeline Stages', fontsize=13, fontweight='bold')
    save(fig, '04_exp2_ablation.png')


# ─── Chart 05 ───
def chart_05():
    fig, ax = plt.subplots(figsize=(8, 5))
    stages = [a['stage'] for a in ABL_INDIV]
    vals = [a['f1'] for a in ABL_INDIV]
    # Sort by value
    sorted_pairs = sorted(zip(vals, stages), reverse=True)
    vals_s = [v for v, _ in sorted_pairs]
    stages_s = [s for _, s in sorted_pairs]
    colors_list = []
    for v in vals_s:
        if v >= 1.4:
            colors_list.append(TEAL)
        elif v >= 0.8:
            colors_list.append(BLUE)
        else:
            colors_list.append(GRAY)
    y = np.arange(len(stages_s))
    bars = ax.barh(y, vals_s, color=colors_list, height=0.6, edgecolor='white')
    for i, bar in enumerate(bars):
        ax.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height()/2,
                f'+{vals_s[i]:.1f}pp', ha='left', va='center', fontsize=10, fontweight='bold')
    ax.set_yticks(y)
    ax.set_yticklabels(stages_s, fontsize=9)
    ax.set_xlabel('Marginal $\\Delta$F1 (pp)', fontsize=11)
    ax.set_title('Per-Stage Marginal Contribution to F1', fontsize=13, fontweight='bold')
    ax.invert_yaxis()
    save(fig, '05_exp2_per_stage.png')


# ─── Chart 06 ───
def chart_06():
    fig, ax = plt.subplots(figsize=(9, 5))
    lesions = [a['l'] for a in ALO]
    base = [a['ab'] for a in ALO]
    pipe = [a['ap'] for a in ALO]
    pct_improve = ['+61%', '+48%', '+31%', '+47%']
    x = np.arange(len(lesions))
    w = 0.3
    b1 = ax.bar(x - w/2, base, w, color=GRAY, label='Baseline', edgecolor='white')
    b2 = ax.bar(x + w/2, pipe, w, color=TEAL, label='Pipeline', edgecolor='white')
    for i, bar in enumerate(b2):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.015,
                pct_improve[i], ha='center', va='bottom', fontsize=9, fontweight='bold', color=CORAL)
    for bars, vals in [(b1, base), (b2, pipe)]:
        for bar, val in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
                    f'{val:.2f}', ha='center', va='bottom', fontsize=8)
    ax.set_xticks(x)
    ax.set_xticklabels(lesions, fontsize=10)
    ax.set_ylabel('ALO Score', fontsize=11)
    ax.set_ylim(0, 0.9)
    ax.set_title('Attention-Lesion Overlap (ALO) by Lesion Type', fontsize=13, fontweight='bold')
    ax.legend(fontsize=9)
    save(fig, '06_exp4_alo.png')


# ─── Chart 07 ───
def chart_07():
    fig, ax = plt.subplots(figsize=(9, 5))
    lesions = [a['l'] for a in IOU]
    base = [a['b'] for a in IOU]
    pipe = [a['p'] for a in IOU]
    pct_improve = ['+83%', '+75%', '+50%', '+78%']
    x = np.arange(len(lesions))
    w = 0.3
    b1 = ax.bar(x - w/2, base, w, color=GRAY, label='Baseline', edgecolor='white')
    b2 = ax.bar(x + w/2, pipe, w, color=PURPLE, label='Pipeline', edgecolor='white')
    for i, bar in enumerate(b2):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.015,
                pct_improve[i], ha='center', va='bottom', fontsize=9, fontweight='bold', color=CORAL)
    for bars, vals in [(b1, base), (b2, pipe)]:
        for bar, val in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
                    f'{val:.2f}', ha='center', va='bottom', fontsize=8)
    ax.set_xticks(x)
    ax.set_xticklabels(lesions, fontsize=10)
    ax.set_ylabel('IoU Score', fontsize=11)
    ax.set_ylim(0, 0.6)
    ax.set_title('IoU by Lesion Type', fontsize=13, fontweight='bold')
    ax.legend(fontsize=9)
    save(fig, '07_exp4_iou.png')


# ─── Chart 08 ───
def chart_08():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('Cross-Dataset Generalization -- F1 and AUC', fontsize=14, fontweight='bold')
    datasets = [g['d'] for g in GEN]
    x = np.arange(len(datasets))
    w = 0.3
    # Left: F1
    fb = [g['fb'] for g in GEN]
    fp = [g['fp'] for g in GEN]
    b1 = ax1.bar(x - w/2, fb, w, color=GRAY, label='Baseline', edgecolor='white')
    b2 = ax1.bar(x + w/2, fp, w, color=TEAL, label='Pipeline', edgecolor='white')
    for bars, vals in [(b1, fb), (b2, fp)]:
        for bar, val in zip(bars, vals):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
                     f'{val:.3f}', ha='center', va='bottom', fontsize=8)
    ax1.set_xticks(x)
    ax1.set_xticklabels(datasets, fontsize=9, rotation=15, ha='right')
    ax1.set_ylabel('Weighted F1', fontsize=11)
    ax1.set_ylim(0.5, 0.85)
    ax1.set_title('Weighted F1', fontsize=11)
    ax1.legend(fontsize=8)
    # Right: AUC
    ab = [g['b'] for g in GEN_AUC]
    ap = [g['p'] for g in GEN_AUC]
    b1 = ax2.bar(x - w/2, ab, w, color=GRAY, label='Baseline', edgecolor='white')
    b2 = ax2.bar(x + w/2, ap, w, color=TEAL, label='Pipeline', edgecolor='white')
    for bars, vals in [(b1, ab), (b2, ap)]:
        for bar, val in zip(bars, vals):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
                     f'{val:.3f}', ha='center', va='bottom', fontsize=8)
    ax2.set_xticks(x)
    ax2.set_xticklabels(datasets, fontsize=9, rotation=15, ha='right')
    ax2.set_ylabel('ROC-AUC', fontsize=11)
    ax2.set_ylim(0.7, 0.92)
    ax2.set_title('ROC-AUC', fontsize=11)
    ax2.legend(fontsize=8)
    plt.tight_layout(rect=[0, 0, 1, 0.93])
    save(fig, '08_exp5_generalization.png')


# ─── Chart 09 ───
def chart_09():
    fig, ax = plt.subplots(figsize=(9, 5))
    datasets = [g['d'] for g in G_RATIO]
    gb = [g['Gb'] for g in G_RATIO]
    gp = [g['Gp'] for g in G_RATIO]
    x = np.arange(len(datasets))
    w = 0.3
    b1 = ax.bar(x - w/2, gb, w, color=GRAY, label='Baseline G', edgecolor='white')
    b2 = ax.bar(x + w/2, gp, w, color=TEAL, label='Pipeline G', edgecolor='white')
    for bar, val in zip(b1, gb):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
                f'{val:.2f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    for bar, val in zip(b2, gp):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
                f'{val:.2f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    ax.axhline(y=0.85, color=RED, linestyle='--', linewidth=1.5)
    ax.text(2.45, 0.853, 'H-4 threshold: G = 0.85', fontsize=8, color=RED, ha='right')
    ax.set_xticks(x)
    ax.set_xticklabels(datasets, fontsize=10)
    ax.set_ylabel('Generalization Ratio G', fontsize=11)
    ax.set_ylim(0.75, 0.95)
    ax.set_title('Generalization Ratio G = F1_external / F1_EyePACS', fontsize=13, fontweight='bold')
    ax.legend(fontsize=9)
    save(fig, '09_exp5_G_ratio.png')


# ─── Chart 10 ───
def chart_10():
    fig, ax = plt.subplots(figsize=(11, 5.5))
    cameras = [d['c'] for d in DEV]
    fb = [d['fb'] for d in DEV]
    fp = [d['fp'] for d in DEV]
    x = np.arange(len(cameras))
    w = 0.3
    b1 = ax.bar(x - w/2, fb, w, color=GRAY, label='Baseline', edgecolor='white')
    b2 = ax.bar(x + w/2, fp, w, color=CORAL, label='Pipeline', edgecolor='white')
    for bars, vals in [(b1, fb), (b2, fp)]:
        for bar, val in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
                    f'{val:.3f}', ha='center', va='bottom', fontsize=8)
    ax.set_xticks(x)
    ax.set_xticklabels(cameras, fontsize=8)
    ax.set_ylabel('Weighted F1', fontsize=11)
    # Headroom above the tallest bar so the legend and the spread inset do not sit on the data.
    ax.set_ylim(0.45, 0.92)
    ax.set_title('Cross-Device Performance (H-6)', fontsize=13, fontweight='bold')
    ax.legend(fontsize=9, loc='upper right')
    # Between-device spread inset (5 external camera groups, EyePACS excluded)
    textstr = ('Between-device spread (5 groups):\n'
               'std(F1): 0.0306 $\\rightarrow$ 0.0130  (2.4$\\times$)\n'
               'std(AUC): 0.0214 $\\rightarrow$ 0.0070  (3.1$\\times$)\n'
               'both 95% CIs exclude zero')
    props = dict(boxstyle='round,pad=0.5', facecolor='#E1F5EE', alpha=0.9, edgecolor=TEAL)
    ax.text(0.98, 0.74, textstr, transform=ax.transAxes, fontsize=9, verticalalignment='top',
            horizontalalignment='right', bbox=props)
    save(fig, '10_exp6_device_shift.png')


# ─── Chart 11 ───
def chart_11():
    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
    categories = ['Weighted F1', 'ROC-AUC', "Cohen's $\\kappa$", 'Generalization\n(G ratio)', 'ALO', 'Device\nRobustness']
    N = len(categories)
    # Normalize each to [0, 1] range for radar
    # Config C vs D. Axes: in-domain wF1 / in-domain AUC / in-domain kappa /
    # APTOS G ratio / mean ALO over the 4 lesion types / min g_ratio across camera groups.
    baseline_raw = [0.7538, 0.8210, 0.7468, 0.8577, 0.2685, 0.7209]
    pipeline_raw = [0.8193, 0.8570, 0.8571, 0.8976, 0.3818, 0.7837]
    # Scale to 0-1 for display (min-max per axis)
    mins = [0.70, 0.78, 0.68, 0.80, 0.20, 0.68]
    maxs = [0.88, 0.90, 0.90, 0.95, 0.50, 0.88]
    baseline = [(v - mi) / (ma - mi) for v, mi, ma in zip(baseline_raw, mins, maxs)]
    pipeline = [(v - mi) / (ma - mi) for v, mi, ma in zip(pipeline_raw, mins, maxs)]
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    baseline += baseline[:1]
    pipeline += pipeline[:1]
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_rlabel_position(0)
    plt.xticks(angles[:-1], categories, fontsize=9)
    ax.fill(angles, baseline, alpha=0.15, color=GRAY)
    ax.plot(angles, baseline, 'o-', color=GRAY, linewidth=1.5, markersize=5, label='Baseline')
    ax.fill(angles, pipeline, alpha=0.15, color=TEAL)
    ax.plot(angles, pipeline, 'o-', color=TEAL, linewidth=1.5, markersize=5, label='Pipeline')
    ax.set_ylim(0, 1)
    ax.set_yticks([0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(['', '', '', ''], fontsize=7)
    ax.legend(loc='upper right', bbox_to_anchor=(1.25, 1.1), fontsize=9)
    ax.set_title('Overall Performance: Baseline vs Full Pipeline', fontsize=13, fontweight='bold', y=1.08)
    save(fig, '11_summary_radar.png')


# ─── Chart 12 ───
def chart_12():
    fig, ax = plt.subplots(figsize=(8, 5))
    metrics = ['$\\Delta$F1 (pp)', '$\\Delta$AUC (pp)', '$\\Delta\\kappa$ (pp)']
    resnet = [5.2, 3.3, 8.0]
    effnet = [5.3, 4.4, 8.0]
    x = np.arange(len(metrics))
    w = 0.3
    b1 = ax.bar(x - w/2, resnet, w, color=BLUE, label='ResNet-50', edgecolor='white')
    b2 = ax.bar(x + w/2, effnet, w, color=TEAL, label='EfficientNet-B3', edgecolor='white')
    for bar, val in zip(b1, resnet):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2, f'+{val:.1f}',
                ha='center', va='bottom', fontsize=10, fontweight='bold', color=BLUE)
    for bar, val in zip(b2, effnet):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2, f'+{val:.1f}',
                ha='center', va='bottom', fontsize=10, fontweight='bold', color=TEAL)
    ax.axhline(y=5.0, color=RED, linestyle='--', linewidth=1.5)
    ax.text(2.55, 5.15, 'EH-3: 5pp ($\\Delta$F1)', fontsize=8, color=RED, ha='right')
    ax.axhline(y=2.0, color=RED, linestyle='--', linewidth=1)
    ax.text(2.55, 2.15, 'EH-3: 2pp ($\\Delta$AUC)', fontsize=8, color=RED, ha='right')
    ax.axhline(y=0.0, color=RED, linestyle='--', linewidth=0.8, alpha=0.5)
    ax.text(2.55, 0.15, 'EH-3: 0pp ($\\Delta\\kappa$)', fontsize=8, color=RED, ha='right')
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, fontsize=11)
    ax.set_ylabel('Improvement (pp)', fontsize=11)
    ax.set_ylim(-0.5, 10.5)
    ax.set_title('EH-3 Dominance Criterion Check', fontsize=13, fontweight='bold')
    ax.legend(fontsize=9)
    # Green check annotations
    ax.text(0, -0.3, 'PASS', ha='center', fontsize=9, fontweight='bold', color=GREEN)
    ax.text(1, -0.3, 'PASS', ha='center', fontsize=9, fontweight='bold', color=GREEN)
    ax.text(2, -0.3, 'PASS', ha='center', fontsize=9, fontweight='bold', color=GREEN)
    save(fig, '12_eh3_dominance.png')


# ─── Chart 13 ───
def chart_13():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('CLAHE Parameter Sensitivity -- DR Grade 1 vs DR Grade 2', fontsize=14, fontweight='bold')
    cf_labels = CLAHE_CLIP
    gt_labels = ['0.01', '0.02', '0.03', '0.04', '0.05']
    data1 = np.array(CLAHE1)
    data2 = np.array(CLAHE2)
    # DR Grade 1
    im1 = ax1.imshow(data1, cmap='YlOrRd', aspect='auto', vmin=0.26, vmax=0.48)
    ax1.set_xticks(range(5))
    ax1.set_xticklabels(gt_labels, fontsize=9)
    ax1.set_yticks(range(len(cf_labels)))
    ax1.set_yticklabels(cf_labels, fontsize=9)
    ax1.set_xlabel('global_threshold', fontsize=10)
    ax1.set_ylabel('clip_factor', fontsize=10)
    ax1.set_title('DR Grade 1 (Mild)', fontsize=11)
    for i in range(len(cf_labels)):
        for j in range(5):
            ax1.text(j, i, f'{data1[i,j]:.2f}', ha='center', va='center', fontsize=8,
                     color='white' if data1[i,j] > 0.43 else 'black')
    # Optimum star (clip_factor=2.5 = row 4, threshold=0.03 = col 2)
    ax1.plot(2.34, 3.66, marker='*', color='white', markersize=16, markeredgecolor='black', markeredgewidth=0.6)
    plt.colorbar(im1, ax=ax1, fraction=0.046, pad=0.04)
    # DR Grade 2
    im2 = ax2.imshow(data2, cmap='YlGnBu', aspect='auto', vmin=0.42, vmax=0.64)
    ax2.set_xticks(range(5))
    ax2.set_xticklabels(gt_labels, fontsize=9)
    ax2.set_yticks(range(len(cf_labels)))
    ax2.set_yticklabels(cf_labels, fontsize=9)
    ax2.set_xlabel('global_threshold', fontsize=10)
    ax2.set_ylabel('clip_factor', fontsize=10)
    ax2.set_title('DR Grade 2 (Moderate)', fontsize=11)
    for i in range(len(cf_labels)):
        for j in range(5):
            ax2.text(j, i, f'{data2[i,j]:.2f}', ha='center', va='center', fontsize=8,
                     color='white' if data2[i,j] > 0.58 else 'black')
    # Optimum star (clip_factor=2.0 = row 3, threshold=0.03 = col 2)
    ax2.plot(2.34, 2.66, marker='*', color='white', markersize=16, markeredgecolor='black', markeredgewidth=0.6)
    plt.colorbar(im2, ax=ax2, fraction=0.046, pad=0.04)
    plt.tight_layout(rect=[0, 0, 1, 0.93])
    save(fig, '13_exp2_clahe_sensitivity.png')


# ─── Chart 14 ───
def chart_14():
    fig, ax = plt.subplots(figsize=(9, 5))
    metrics = [c['m'] for c in CLIN]
    base = [c['b'] for c in CLIN]
    pipe = [c['v'] for c in CLIN]
    x = np.arange(len(metrics))
    w = 0.3
    b1 = ax.bar(x - w/2, base, w, color=GRAY, label='Baseline', edgecolor='white')
    b2 = ax.bar(x + w/2, pipe, w, color=TEAL, label='Pipeline', edgecolor='white')
    for bars, vals in [(b1, base), (b2, pipe)]:
        for bar, val in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
                    f'{val:.2f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    ax.axhline(y=0.80, color=RED, linestyle=':', linewidth=1.5)
    ax.text(3.45, 0.805, 'WHO screening: 0.80', fontsize=8, color=RED, ha='right')
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, fontsize=11)
    ax.set_ylabel('Score', fontsize=11)
    ax.set_ylim(0.65, 1.02)
    ax.set_title('Clinical Screening Metrics -- Referable DR (Grade >= 2)', fontsize=13, fontweight='bold')
    ax.legend(fontsize=9)
    save(fig, '14_clinical_metrics.png')


# ─── Main ───
if __name__ == '__main__':
    print("Generating charts 01-14...")
    chart_01()
    chart_02()
    chart_03()
    chart_04()
    chart_05()
    chart_06()
    chart_07()
    chart_08()
    chart_09()
    chart_10()
    chart_11()
    chart_12()
    chart_13()
    chart_14()
    print("[OK] Charts 01-14 complete!")
