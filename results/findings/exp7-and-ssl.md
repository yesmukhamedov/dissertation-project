# Conclusions — Experiment 7 / E-7 (small-data training) + SSL / A1 → §4.8 / §3.3.2

## Exp 7 / E-7 — IDRiD → Clinical (small data) → §4.8

**What was done.** Training on the small IDRiD set (n = 516, 5-fold CV), tested on the Kazakhstani
clinical hold-out (n = 60); a comparison of the baseline (3ch) and full (4ch) arms, EfficientNet-B3.
The experiment is **preregistered** (`preregistered = true`). Source: the **2026-08-03** run.

**What was found.**

1. **The pipeline significantly outperforms baseline on the clinical hold-out.** wF1 0.5157 → 0.5951
   (Δ +0.0794, CI [+0.0471, +0.1227]); κ 0.4848 → 0.6075 (Δ +0.1227, CI [+0.0747, +0.1925]);
   AUC 0.7464 → 0.7962 (Δ +0.0498, CI [+0.0165, +0.0689]). All three CIs exclude zero.
2. **Stability across folds.** On the internal IDRiD CV the pipeline is above baseline **in 4 of the
   5 folds** (0.6520 ± 0.0310 against 0.5850 ± 0.0380); on fold 2 it is marginally lower (0.6352
   against 0.6466, −0.0114) — a single-fold fluctuation comparable to the between-fold std, not a
   systematic exception.
3. **The κ gain is over 1.5× the wF1 gain** (+0.123 against +0.079) — the same picture as in every
   other experiment: the pipeline primarily removes distant grading errors.
4. ⚠️ **The unpaired bootstrap intervals overlap** (C [0.4601, 0.6097], D [0.5433, 0.6837]) — at
   n = 60 they are wide. Significance comes from the **paired** test of the difference, where both
   arms are evaluated on the same 60 images. Carry the paired CIs into the text; cite the unpaired
   ones only with this caveat.

**Significance (changed relative to the previous revision).** This is the target operating scenario —
training on a small clinical sample and deployment at a different clinic — and the result
substantiates the practical contribution "preprocessing as an effective prior". But the former
formulation "the work's only clean positive; preprocessing is valuable **precisely** on small data"
is **obsolete**: the gain here (+0.079) is comparable to the gain on full EyePACS (+0.0655), i.e. the
pipeline's advantage **is not specific to small data** and does not vanish as the sample grows. exp7
is now one of several consistent results, not an exception in a series of negatives.

**Caveats.** The absolute level (wF1 ≈ 0.52–0.60) is below in-domain EyePACS — as expected for
training on 516 images with testing at a different clinic; what is meaningful is the difference
between arms. The hold-out is small (n = 60). The ± in the summary table is the spread across the
5 training folds, not per-instance uncertainty on the hold-out.

---

## SSL / A1 — in-domain self-supervised pretraining → §3.3.2 / §4.2 caveat

**What was found.**

1. **Classical contrastive methods trained from scratch still fail the probe gate.**
   BYOL collapses (κ = 0.0023), MoCo-v2 κ = 0.111, DINO κ = 0.079 — all substantially below ImageNet
   (κ 0.32–0.45). Increasing the budget from 50 to 100 epochs **does not help**: MoCo 0.111 → 0.109,
   DINO 0.079 → 0.063. A robust negative result, substantive in its own right.
2. **New: SIP (100 epochs) passes the gate** — κ = 0.6530, practically at the continual-SSL level
   (0.6591). That is, from-scratch in-domain initialization is in principle achievable within the
   project's budget; what fails is particular methods, not the approach. SIP was built but **not
   selected** — Config B/D are initialized with continual-SSL.
3. **Continual-SSL delivers a large gain on both backbones.** ResNet-50: κ 0.3249 → 0.6591
   (Δ +0.3342; second run +0.2891). EfficientNet-B3: κ 0.4479 → 0.6827 (Δ +0.2348; second run
   +0.2219). Both `passed = true`. There is no collapse (feat_std 0.008 → 0.057, kNN 0.31 → 0.70).
4. ⚠️ **The between-backbone asymmetry has disappeared.** In the previous run EfficientNet-B3 gained
   nothing from continual-SSL (κ 0.435 against ImageNet's 0.445), and this was reported as an honest
   caveat. Now both backbones receive a comparable gain — formulations that relied on the previous
   asymmetry must be replaced.

**Significance for the thesis (Premise 4).** The two-stage SSL narrative is preserved, but its moral
changes: not "in-domain SSL does not work and we had to fall back", but "classical contrastive
methods on a fundus corpus of this scale are not competitive with ImageNet, whereas the specialized
SIP and continual-SSL are competitive and deliver a large in-domain gain on both backbones".

**CFC-2.8 — the status has changed.** The "preprocessing × initialization" confound in Config B/D
formally remains, but it is **decomposable**: the exp2 cumulative ablation under a single
initialization at all eight levels yields ΔwF1 = +0.0655 from L0 to L7 — exactly the D-vs-C magnitude
in exp1, with L0 and L7 numerically coinciding with Config C and D. The contribution of preprocessing
has been measured independently of the contribution of initialization. In §4.2, CFC-2.8 goes in as a
note about a feature of the design and **not** as a limitation on the conclusion.

Card: `hypotheses/exp7-and-SSL.md`. Tables: `tables/TAB-4.10_exp7_smalldata.md`,
`tables/SSL_continual_gate.md`.
