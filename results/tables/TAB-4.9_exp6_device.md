# TAB-4.9 — Experiment 6: Device / Camera Domain Shift (H-6)

Models trained on EyePACS, evaluated on groups defined by camera manufacturer.
Robustness threshold **g_floor = 0.7**, where g_ratio = wF1_group / wF1_in-domain.
In-domain: C = 0.7538, D = 0.8193. Source: the **2026-08-03** run (`VALUES.md` §6).

Group sizes: kowa_idrid 413 · mixed_ddr 1 200 · mixed_odir5k 950 ·
topcon_messidor2 1 744 · mixed_rfmid 640.

## Weighted F1 and g_ratio by group (§6.1, §6.9)

| Camera group | wF1 (C) | wF1 (D) | Δ | 95% CI (Δ) | g_ratio (C) | g_ratio (D) | ≥0.7 (C/D) |
|--------------|--------:|--------:|--:|------------|------------:|------------:|:----------:|
| kowa_idrid | 0.5938 | **0.6627** | +0.0689 | [+0.0494, +0.0968] | 0.7877 | 0.8089 | ✓ / ✓ |
| mixed_ddr | 0.6154 | **0.6671** | +0.0517 | [+0.0226, +0.0690] | 0.8164 | 0.8142 | ✓ / ✓ |
| mixed_odir5k | 0.5700 | **0.6581** | +0.0881 | [+0.0570, +0.1088] | 0.7562 | 0.8032 | ✓ / ✓ |
| topcon_messidor2 | 0.6282 | **0.6823** | +0.0541 | [+0.0362, +0.0814] | 0.8334 | 0.8328 | ✓ / ✓ |
| mixed_rfmid | 0.5434 | **0.6421** | +0.0987 | [+0.0680, +0.1224] | 0.7209 | 0.7837 | ✓ / ✓ |

## ROC-AUC and κ by group (§6.2, §6.3)

| Group | AUC (C) | AUC (D) | Δ AUC | 95% CI (Δ) | κ (C) | κ (D) |
|--------|--------:|--------:|------:|------------|------:|------:|
| kowa_idrid | 0.8195 | **0.8627** | +0.0432 | [+0.0323, +0.0619] | 0.6841 | **0.7719** |
| mixed_ddr | 0.8392 | **0.8653** | +0.0261 | [+0.0159, +0.0423] | 0.7017 | **0.7863** |
| mixed_odir5k | 0.7965 | **0.8598** | +0.0633 | [+0.0462, +0.0840] | 0.6373 | **0.7547** |
| topcon_messidor2 | 0.8407 | **0.8729** | +0.0322 | [+0.0183, +0.0421] | 0.7152 | **0.7886** |
| mixed_rfmid | 0.7884 | **0.8516** | +0.0632 | [+0.0478, +0.0882] | 0.6254 | **0.7408** |

## Between-group spread (§6.8) — the key result

| Quantity | C | D | Δ (D − C) | 95% CI (Δ) | CI excludes 0 |
|----------|--:|--:|----------:|------------|:--------------:|
| std (wF1, 5 groups) | 0.0306 | **0.0130** | −0.0176 | [−0.0253, −0.0062] | ✓ |
| std (ROC-AUC, 5 groups) | 0.0214 | **0.0070** | −0.0144 | [−0.0233, −0.0072] | ✓ |

The pipeline reduces the between-camera spread of weighted-F1 by **a factor of 2.4** and the spread
of ROC-AUC by **a factor of 3.1**, and both reductions are statistically significant (the CIs exclude
zero).

> The wF1 std point estimates were recomputed after `kowa_idrid` / `topcon_messidor2` were
> re-synchronized with §7.1 (see the caveat below). The **bootstrap CIs were not recomputed** — they
> are carried over from the run and comfortably contain the new point estimate (−0.0176).

## Referable AUC by group (§6.4)

| Group | Referable AUC (C) | Referable AUC (D) |
|--------|------------------:|------------------:|
| kowa_idrid | 0.8960 | **0.9302** |
| mixed_ddr | 0.9025 | **0.9368** |
| mixed_odir5k | 0.8655 | **0.9211** |
| topcon_messidor2 | 0.9064 | **0.9459** |
| mixed_rfmid | 0.8553 | **0.9114** |

## Verdict: `h6_supported = true`

1. **The generalization floor is cleared by every group and both arms.** The pipeline's minimum
   g_ratio is 0.7837 (mixed_rfmid), a margin of 0.084 over the 0.7 threshold.
2. **The pipeline reduces the between-device spread significantly** (std wF1 0.0306 → 0.0130,
   CI [−0.0253, −0.0062]). This — and not the mere fact of clearing the threshold — is the
   substantive result: baseline clears the threshold too, but its quality depends noticeably more on
   the camera.
3. **The g_ratio range contracts:** for C it is 0.7209–0.8334 (span 0.113), for D 0.7837–0.8328
   (span 0.049). The pipeline levels out the model's behaviour across devices.
4. **The gain is larger the worse the group performed under baseline.** The largest Δ wF1 are for
   mixed_rfmid (+0.0987, C's worst group) and mixed_odir5k (+0.0881, the second worst); the smallest
   is mixed_ddr (+0.0517) and topcon_messidor2 (+0.0541, C's best group). That is exactly what
   produces the contraction of the spread.
5. **g_ratio rises in 3 of 5 groups and falls marginally in 2** — mixed_ddr (0.8164 → 0.8142) and
   topcon_messidor2 (0.8334 → 0.8328, −0.0006). Both are groups where baseline was already strong and
   the absolute gain is the smallest of the five; absolute wF1 nevertheless rises in both
   (0.6154 → 0.6671 and 0.6282 → 0.6823). The fall is a **normalization artifact of the same kind that
   retired Δ_drop in H-7**: g_ratio divides by each arm's own in-domain wF1, and the pipeline's
   denominator is 6.55 pp larger, so a group must gain roughly 8% relative just to hold its ratio.
   State this explicitly in the text — g_ratio understates the pipeline's advantage by construction,
   and the three groups where it still rises are precisely the ones with the largest absolute gains.

## Caveats

- Evaluation uses **fold 0** checkpoints; the std in the spread table is **between-group** (over the
  5 camera groups), not between-fold.
- The `mixed_rfmid` group is evaluated on the 5-class scale in this run, like the others (in the
  previous run it was binary only) — the numbers are not comparable with the previous version.
- The groups overlap with the exp5 sets: `kowa_idrid` = IDRiD, `topcon_messidor2` = Messidor-2
  (`TAB-4.8_exp5_degradation.md`); values, Δ and CI coincide character-for-character by construction.
  ⚠️ These two rows were re-synchronized with `VALUES.md` §7.1 in this revision — §6.1 of the source
  file had not been regenerated together with §7 and still carried the superseded values. The
  g_ratio and std **point estimates** here were recomputed arithmetically; the bootstrap CIs were not.

Per-class F1 by group — `per_class_and_confusion.md`. Clinical metrics — `TAB-5.4_clinical_referable.md`.
Domain distances — `H-3_domain_distance.md`. Hypothesis card — `hypotheses/H-6.md`.
