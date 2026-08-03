# TAB-4.2 — Experiment 1: 2×2 Factorial Diagnostic Metrics (H-1)

EyePACS 100% (n = 35 126), 5-fold patient-level CV. Mean ± std. Source: the **2026-08-03** run
(`VALUES.md` §1.1).

| Config | Arm | Backbone | Weighted F1 | ROC-AUC (macro-OvR) | Cohen κ (quadratic) | Accuracy | macro-F1 |
|--------|-----|----------|-------------|---------------------|---------------------|----------|----------|
| A | Baseline (3ch) | ResNet-50 | 0.7518 ± 0.0110 | 0.8300 ± 0.0140 | 0.7410 ± 0.0350 | 0.7247 ± 0.0180 | 0.4281 |
| B | Pipeline (4ch) | ResNet-50 | **0.8172 ± 0.0090** | **0.8620 ± 0.0110** | **0.8539 ± 0.0260** | **0.8027 ± 0.0150** | **0.5322** |
| C | Baseline (3ch) | EfficientNet-B3 | 0.7538 ± 0.0120 | 0.8210 ± 0.0150 | 0.7468 ± 0.0330 | 0.7273 ± 0.0190 | 0.4300 |
| D | Pipeline (4ch) | EfficientNet-B3 | **0.8193 ± 0.0100** | **0.8570 ± 0.0120** | **0.8571 ± 0.0270** | **0.8052 ± 0.0160** | **0.5355** |

## Pairwise differences with 95% CIs (§1.2)

| Pair | Metric | Δ | 95% CI (Δ) | CI excludes 0 |
|------|---------|---|------------|----------------|
| B − A | wF1 | +0.0654 | [+0.0521, +0.0873] | ✓ |
| B − A | ROC-AUC | +0.0320 | [+0.0175, +0.0419] | ✓ |
| B − A | κ | +0.1129 | [+0.0780, +0.1414] | ✓ |
| D − C | wF1 | +0.0655 | [+0.0423, +0.0801] | ✓ |
| D − C | ROC-AUC | +0.0360 | [+0.0204, +0.0462] | ✓ |
| D − C | κ | +0.1103 | [+0.0829, +0.1453] | ✓ |

## TAB-4.3 — Dominance Assessment (EH-3)

Dominance criterion (all three mandatory): ΔF1 ≥ 5 pp · ΔAUC ≥ 0.02 · Δκ ≥ 0 (no degradation).

| Comparison | ΔF1 (pp) | ΔAUC | Δκ | F1 crit | AUC crit | κ crit | **Dominant** |
|------------|----------|------|-----|---------|----------|--------|--------------|
| B vs A (pipeline effect, ResNet-50) | **+6.54** | +0.0320 | +0.1129 | ✓ | ✓ | ✓ | **YES** |
| D vs C (pipeline effect, EfficientNet-B3) | **+6.55** | +0.0360 | +0.1103 | ✓ | ✓ | ✓ | **YES** |

**Verdict:** `h1_supported = true`. All three components of the EH-3 criterion are met **on both
backbones**: the weighted-F1 gain exceeds the 5 pp threshold with margin to spare (+6.5 pp), the AUC
gain exceeds the 0.02 threshold (+0.032…0.036), and κ not only fails to degrade but rises by +0.11.
The effect size is practically identical for ResNet-50 and EfficientNet-B3 (ΔwF1 6.54 vs 6.55 pp),
which is corroborated by the absence of an "arm × backbone" interaction in the mixed-effects ANOVA
(p = 0.31, `TAB-5.1_statistical.md`) — the pipeline effect does not depend on the choice of architecture.

Significance of the pairwise differences: DeLong p = 0.0041 / 0.0028, McNemar p = 0.0057 / 0.0041,
and after the Holm correction over 4 configurations p = 0.0082 / 0.0056 — see `TAB-5.1_statistical.md`.

> Caveat CFC-2.8 (still applies): the integrated arm (B/D) is initialized with continual-SSL, so the
> quantity being measured is the effect of the **integrated configuration** (preprocessing ×
> initialization), not of preprocessing in isolation. However, the cumulative ablation on the same
> corpus (`TAB-4.4_exp2_ablation.md`, all 8 levels under a single initialization) shows that
> **preprocessing on its own yields +6.55 pp** from L0 to L7 — that is, the composite is decomposable
> here and the contribution of preprocessing has been measured separately. This is a substantial
> difference from the previous run.

Source: `VALUES.md` §1.1–1.3 (the 2026-08-03 run).
