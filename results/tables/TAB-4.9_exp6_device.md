# TAB-4.9 — Experiment 6: Device / Camera Domain Shift (H-6)

Models trained on EyePACS, evaluated on groups defined by camera manufacturer.
Robustness threshold **g_floor = 0.7**, where g_ratio = wF1_group / wF1_in-domain.
In-domain: C = 0.7538, D = 0.8193. Source: the **2026-08-03** run (`VALUES.md` §6).

Group sizes: kowa_idrid 413 · mixed_ddr 1 200 · mixed_odir5k 950 ·
topcon_messidor2 1 744 · mixed_rfmid 640.

## Weighted F1 and g_ratio by group (§6.1, §6.9)

| Camera group | wF1 (C) | wF1 (D) | Δ | 95% CI (Δ) | g_ratio (C) | g_ratio (D) | ≥0.7 (C/D) |
|--------------|--------:|--------:|--:|------------|------------:|------------:|:----------:|
| kowa_idrid | 0.5913 | **0.6613** | +0.0700 | [+0.0526, +0.1000] | 0.7844 | 0.8072 | ✓ / ✓ |
| mixed_ddr | 0.6111 | **0.6693** | +0.0582 | [+0.0296, +0.0760] | 0.8107 | 0.8169 | ✓ / ✓ |
| mixed_odir5k | 0.5729 | **0.6565** | +0.0836 | [+0.0522, +0.1040] | 0.7600 | 0.8013 | ✓ / ✓ |
| topcon_messidor2 | 0.6280 | **0.6840** | +0.0560 | [+0.0355, +0.0807] | 0.8331 | 0.8349 | ✓ / ✓ |
| mixed_rfmid | 0.5544 | **0.6442** | +0.0898 | [+0.0659, +0.1203] | 0.7355 | 0.7863 | ✓ / ✓ |

## ROC-AUC and κ by group (§6.2, §6.3)

| Group | AUC (C) | AUC (D) | Δ AUC | 95% CI (Δ) | κ (C) | κ (D) |
|--------|--------:|--------:|------:|------------|------:|------:|
| kowa_idrid | 0.8194 | **0.8580** | +0.0386 | [+0.0210, +0.0506] | 0.6873 | **0.7722** |
| mixed_ddr | 0.8333 | **0.8681** | +0.0348 | [+0.0194, +0.0458] | 0.7008 | **0.7811** |
| mixed_odir5k | 0.7982 | **0.8531** | +0.0549 | [+0.0386, +0.0764] | 0.6424 | **0.7524** |
| topcon_messidor2 | 0.8428 | **0.8670** | +0.0242 | [+0.0143, +0.0381] | 0.7209 | **0.7896** |
| mixed_rfmid | 0.7870 | **0.8536** | +0.0666 | [+0.0428, +0.0832] | 0.6244 | **0.7440** |

## Between-group spread (§6.8) — the key result

| Quantity | C | D | Δ (D − C) | 95% CI (Δ) | CI excludes 0 |
|----------|--:|--:|----------:|------------|:--------------:|
| std (wF1, 5 groups) | 0.0262 | **0.0133** | −0.0129 | [−0.0186, −0.0049] | ✓ |
| std (ROC-AUC, 5 groups) | 0.0209 | **0.0064** | −0.0145 | [−0.0247, −0.0085] | ✓ |

The pipeline reduces the between-camera spread of weighted-F1 by **a factor of 2.0** and the spread
of ROC-AUC by **a factor of 3.3**, and both reductions are statistically significant (the CIs exclude
zero).

## Referable AUC by group (§6.4)

| Group | Referable AUC (C) | Referable AUC (D) |
|--------|------------------:|------------------:|
| kowa_idrid | 0.8891 | **0.9333** |
| mixed_ddr | 0.9038 | **0.9372** |
| mixed_odir5k | 0.8639 | **0.9171** |
| topcon_messidor2 | 0.9097 | **0.9455** |
| mixed_rfmid | 0.8510 | **0.9104** |

## Verdict: `h6_supported = true`

1. **The generalization floor is cleared by every group and both arms.** The pipeline's minimum
   g_ratio is 0.7863 (mixed_rfmid), a margin of 0.086 over the 0.7 threshold.
2. **The pipeline reduces the between-device spread significantly** (std wF1 0.0262 → 0.0133,
   CI [−0.0186, −0.0049]). This — and not the mere fact of clearing the threshold — is the
   substantive result: baseline clears the threshold too, but its quality depends noticeably more on
   the camera.
3. **The g_ratio range contracts:** for C it is 0.7355–0.8331 (span 0.098), for D 0.7863–0.8349
   (span 0.049). The pipeline levels out the model's behaviour across devices.
4. **The gain is larger the worse the group performed under baseline.** The largest Δ wF1 are for
   mixed_rfmid (+0.0898, C's worst group) and mixed_odir5k (+0.0836, the second worst); the smallest
   is topcon_messidor2 (+0.0560, C's best group). That is exactly what produces the contraction of
   the spread.
5. **g_ratio now rises in all five groups**, including topcon_messidor2 (0.8331 → 0.8349), where the
   previous run showed an inversion. On that group the g_ratio gain is nonetheless marginal (+0.0018)
   against a clear absolute gain (wF1 0.6280 → 0.6840): the ratio is damped by the pipeline's larger
   denominator (in-domain 0.8193 against 0.7538). Flag this in the text — g_ratio understates the
   pipeline's advantage by construction.

## Caveats

- Evaluation uses **fold 0** checkpoints; the std in the spread table is **between-group** (over the
  5 camera groups), not between-fold.
- The `mixed_rfmid` group is evaluated on the 5-class scale in this run, like the others (in the
  previous run it was binary only) — the numbers are not comparable with the previous version.
- The groups overlap with the exp5 sets: `kowa_idrid` = IDRiD, `topcon_messidor2` = Messidor-2
  (`TAB-4.8_exp5_degradation.md`); the values coincide.

Per-class F1 by group — `per_class_and_confusion.md`. Clinical metrics — `TAB-5.4_clinical_referable.md`.
Domain distances — `H-3_domain_distance.md`. Hypothesis card — `hypotheses/H-6.md`.
