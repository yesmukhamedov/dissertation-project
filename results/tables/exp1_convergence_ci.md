# Exp 1 — convergence, overfitting, confidence intervals

Source: the **2026-08-03** run (`VALUES.md` §1.9 — convergence; §1.1 — mean ± std; §1.4 —
per-instance bootstrap). Best epoch = max val weighted-F1.

## A5/A6 — Convergence and overfitting per fold (best epoch)

| Config | Arm | best epochs per fold | train_loss (best) | val_loss (best) | **loss gap (val − train)** |
|--------|-----|----------------------|-------------------|-----------------|-----------------------------|
| A | baseline, ResNet-50 | 16, 14, 17, 15, 16 | 0.098 | 0.150 | **0.052** |
| B | pipeline, ResNet-50 | 9, 8, 10, 9, 9 | 0.126 | 0.147 | **0.021** |
| C | baseline, EffNet-B3 | 15, 17, 14, 16, 15 | 0.102 | 0.156 | **0.054** |
| D | pipeline, EffNet-B3 | 8, 9, 7, 9, 8 | 0.131 | 0.153 | **0.022** |

**Key finding (the regularizing effect of the pipeline).** The pipeline arms (B/D) converge almost
**twice as early** (epochs 7–10 against 14–17) and keep a loss gap **2.5× smaller** (0.021–0.022
against 0.052–0.054). The mechanism is legible from the components: B/D have a **higher** train_loss
(0.126–0.131 against 0.098–0.102) at a **comparable** val_loss — the model fits the training set less
closely but generalizes as well or better. This is regularizer behaviour: the 4th channel (FOV mask)
plus illumination normalization narrow the hypothesis space, cutting away variability that carries no
diagnostic signal.

The spread of best epochs within an arm is small (±1–1.5 epochs), i.e. the convergence regime is
reproducible across folds rather than the result of a lucky seed.

This is consistent with exp7 (a gain in the data-scarce regime) and with the AUC/κ gains within exp1 itself.

## A9 — Confidence intervals

### Cross-validation CIs across folds (95%, t, df = 4)

CI ≈ mean ± 2.776·std/√5. This is an interval over the 5 folds, **not** a per-instance bootstrap.

| Config | wF1 (mean ± std) | wF1 95% CI | AUC 95% CI | κ 95% CI | Acc 95% CI |
|--------|------------------|------------|------------|----------|------------|
| A | 0.7518 ± 0.0110 | [0.7381, 0.7655] | [0.8126, 0.8474] | [0.6976, 0.7845] | [0.7024, 0.7471] |
| B | 0.8172 ± 0.0090 | [0.8060, 0.8284] | [0.8483, 0.8757] | [0.8216, 0.8862] | [0.7841, 0.8213] |
| C | 0.7538 ± 0.0120 | [0.7389, 0.7687] | [0.8024, 0.8396] | [0.7058, 0.7878] | [0.7037, 0.7509] |
| D | 0.8193 ± 0.0100 | [0.8069, 0.8317] | [0.8421, 0.8719] | [0.8236, 0.8906] | [0.7853, 0.8251] |

**Observation.** The baseline and pipeline intervals **do not overlap on any primary metric**:
on wF1, A [0.738, 0.766] against B [0.806, 0.828] and C [0.739, 0.769] against D [0.807, 0.832];
on AUC, A [0.813, 0.847] against B [0.848, 0.876] and C [0.802, 0.840] against D [0.842, 0.872];
the same holds for κ and Accuracy. The separation is complete, i.e. the pipeline effect exceeds the
between-fold variance on all four metrics at once.

### Per-instance bootstrap (weighted-F1, 1000 resamples)

| Config | mean | 95% CI | std |
|--------|-----:|--------|----:|
| A | 0.7518 | [0.7467, 0.7557] | 0.0023 |
| B | 0.8172 | [0.8138, 0.8222] | 0.0021 |
| C | 0.7538 | [0.7504, 0.7596] | 0.0023 |
| D | 0.8193 | [0.8143, 0.8225] | 0.0021 |

The bootstrap means agree with the CV means to the 4th decimal — the per-instance estimate does not
diverge from the per-fold one. The intervals separate with a large margin (≈0.058 between the top of
A and the bottom of B).

Paired tests (DeLong / McNemar / Holm / mixed-effects ANOVA) — `TAB-5.1_statistical.md`.
