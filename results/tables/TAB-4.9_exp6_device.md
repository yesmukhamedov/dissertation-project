# TAB-4.9 — Experiment 6: Device / Camera Domain Shift (H-6)

Models trained on EyePACS, evaluated on groups defined by camera manufacturer.
Robustness threshold **g_floor = 0.7**, where g_ratio = wF1_group / wF1_in-domain.
In-domain: C = 0.7538, D = 0.8193. Source: the **2026-08-02** run (`VALUES.md` §6).

Group sizes: kowa_idrid 413 · mixed_ddr 1 200 · mixed_odir5k 950 ·
topcon_messidor2 1 744 · mixed_rfmid 640.

## Weighted F1 and g_ratio by group (§6.1, §6.9)

| Camera group | wF1 (C) | wF1 (D) | Δ | 95% CI (Δ) | g_ratio (C) | g_ratio (D) | ≥0.7 (C/D) |
|--------------|--------:|--------:|--:|------------|------------:|------------:|:----------:|
| kowa_idrid | 0.5920 | **0.6620** | +0.0700 | [+0.0463, +0.0937] | 0.7854 | 0.8080 | ✓ / ✓ |
| mixed_ddr | 0.6140 | **0.6710** | +0.0570 | [+0.0338, +0.0802] | 0.8145 | 0.8190 | ✓ / ✓ |
| mixed_odir5k | 0.5680 | **0.6560** | +0.0880 | [+0.0621, +0.1139] | 0.7535 | 0.8007 | ✓ / ✓ |
| topcon_messidor2 | 0.6270 | **0.6780** | +0.0510 | [+0.0284, +0.0736] | 0.8318 | 0.8275 | ✓ / ✓ |
| mixed_rfmid | 0.5510 | **0.6480** | +0.0970 | [+0.0698, +0.1242] | 0.7310 | 0.7909 | ✓ / ✓ |

## ROC-AUC and κ by group (§6.2, §6.3)

| Group | AUC (C) | AUC (D) | Δ AUC | 95% CI (Δ) | κ (C) | κ (D) |
|--------|--------:|--------:|------:|------------|------:|------:|
| kowa_idrid | 0.8210 | **0.8620** | +0.0410 | [+0.0262, +0.0558] | 0.6840 | **0.7710** |
| mixed_ddr | 0.8340 | **0.8680** | +0.0340 | [+0.0208, +0.0472] | 0.7020 | **0.7830** |
| mixed_odir5k | 0.7960 | **0.8560** | +0.0600 | [+0.0411, +0.0789] | 0.6410 | **0.7540** |
| topcon_messidor2 | 0.8420 | **0.8710** | +0.0290 | [+0.0171, +0.0409] | 0.7180 | **0.7920** |
| mixed_rfmid | 0.7880 | **0.8530** | +0.0650 | [+0.0448, +0.0852] | 0.6230 | **0.7460** |

## Between-group spread (§6.8) — the key result

| Quantity | C | D | Δ (D − C) | 95% CI (Δ) | CI excludes 0 |
|----------|--:|--:|----------:|------------|:--------------:|
| std (wF1, 5 groups) | 0.0281 | **0.0106** | −0.0175 | [−0.0268, −0.0082] | ✓ |
| std (ROC-AUC, 5 groups) | 0.0210 | **0.0068** | −0.0142 | [−0.0221, −0.0063] | ✓ |

The pipeline reduces the between-camera spread of weighted-F1 by **a factor of 2.6** and the spread
of ROC-AUC by **a factor of 3.1**, and both reductions are statistically significant (the CIs exclude
zero).

## Referable AUC by group (§6.4)

| Group | Referable AUC (C) | Referable AUC (D) |
|--------|------------------:|------------------:|
| kowa_idrid | 0.8940 | **0.9310** |
| mixed_ddr | 0.9010 | **0.9370** |
| mixed_odir5k | 0.8620 | **0.9180** |
| topcon_messidor2 | 0.9080 | **0.9420** |
| mixed_rfmid | 0.8530 | **0.9140** |

## Verdict: `h6_supported = true`

1. **The generalization floor is cleared by every group and both arms.** The pipeline's minimum
   g_ratio is 0.7909 (mixed_rfmid), a margin of 0.09 over the 0.7 threshold.
2. **The pipeline reduces the between-device spread significantly** (std wF1 0.0281 → 0.0106,
   CI [−0.0268, −0.0082]). This — and not the mere fact of clearing the threshold — is the
   substantive result: baseline clears the threshold too, but its quality depends noticeably more on
   the camera.
3. **The g_ratio range contracts:** for C it is 0.7310–0.8318 (span 0.101), for D 0.7909–0.8275
   (span 0.037). The pipeline levels out the model's behaviour across devices.
4. **The gain is larger the worse the group performed under baseline.** The largest Δ wF1 are for
   mixed_rfmid (+0.0970, C's worst group) and mixed_odir5k (+0.0880, the second worst); the smallest
   is topcon_messidor2 (+0.0510, C's best group). That is exactly what produces the contraction of
   the spread.
5. **The only exception is topcon_messidor2**, where the pipeline's g_ratio is slightly lower
   (0.8275 against baseline's 0.8318). Its absolute wF1 is nevertheless higher (0.6780 against
   0.6270); the drop in g_ratio is a consequence of the larger denominator (in-domain 0.8193 against
   0.7538), not of worse performance. Flag it in the text as a normalization artifact.

## Caveats

- Evaluation uses **fold 0** checkpoints; the std in the spread table is **between-group** (over the
  5 camera groups), not between-fold.
- The `mixed_rfmid` group is evaluated on the 5-class scale in this run, like the others (in the
  previous run it was binary only) — the numbers are not comparable with the previous version.
- The groups overlap with the exp5 sets: `kowa_idrid` = IDRiD, `topcon_messidor2` = Messidor-2
  (`TAB-4.8_exp5_degradation.md`); the values coincide.

Per-class F1 by group — `per_class_and_confusion.md`. Clinical metrics — `TAB-5.4_clinical_referable.md`.
Domain distances — `H-3_domain_distance.md`. Hypothesis card — `hypotheses/H-6.md`.
