# Exp 7 (E-7) + SSL (A1) — verdicts

## Exp 7 / E-7 — Small-Data Trainability (IDRiD → Clinical) — POSITIVE, SIGNIFICANT

Not tied to any of the formal hypotheses H-1…H-7 (it compares the trainability of the baseline vs
full arms on small data). **Preregistered** (`preregistered = true`) — the criteria and metrics were
fixed before the run.

**Outcome (2026-08-03 run).** Clinical hold-out, n = 60:

| Metric | C (baseline) | D (full) | Δ (D − C) | 95% CI (Δ) |
|---------|-------------:|---------:|----------:|------------|
| Weighted F1 | 0.5157 ± 0.0450 | 0.5951 ± 0.0400 | +0.0794 | [+0.0471, +0.1227] |
| Cohen κ | 0.4848 ± 0.0440 | 0.6075 ± 0.0438 | +0.1227 | [+0.0747, +0.1925] |
| ROC-AUC | 0.7464 ± 0.0380 | 0.7962 ± 0.0320 | +0.0498 | [+0.0165, +0.0689] |
| Accuracy | 0.5264 ± 0.0410 | 0.5968 ± 0.0370 | — | — |

Internal CV on IDRiD (n = 516, 5 folds): C 0.5850 ± 0.0380 against D 0.6520 ± 0.0310 — the pipeline
is higher **in 4 of the 5 folds**; on fold 2 it is marginally lower (0.6352 against 0.6466, −0.0114),
a single-fold fluctuation of magnitude comparable to the between-fold std.

> ⚠️ The unpaired per-arm bootstrap intervals **overlap** (C [0.4601, 0.6097],
> D [0.5433, 0.6837]) — at n = 60 they are wide. Significance comes from the **paired** test of the
> difference, where both arms are evaluated on the same 60 images. Carry the paired CIs into the text.

**Significance for the thesis.** The target operating scenario is training on a small clinical sample
and deployment at a different clinic. The result substantiates the practical contribution
"preprocessing as an effective prior under data scarcity". An important refinement relative to the
earlier interpretation: the gain here (+0.079) is **comparable** to the gain on full EyePACS
(+0.0655, [[H-1]]), i.e. the pipeline's advantage **is not specific to small data** and does not
vanish as the sample grows. The former formulation "the work's only clean positive; preprocessing is
valuable precisely on small data" is obsolete — this is now one of several consistent results, not an
exception.

The κ gain (+0.123) is over 1.5× the wF1 gain — the same picture as in every experiment: the pipeline
primarily removes distant grading errors.

---

## SSL / A1 — In-Domain Self-Supervised Pretraining

### Stage 1 — from scratch: failed by the classical methods, **passed by SIP**

| Method (from scratch, 4ch) | epochs | κ | passed |
|---------------------------|------:|--:|--------|
| BYOL (primary per governance) | 50 | 0.0023 | ✗ (collapse) |
| MoCo-v2 | 50 / 100 | 0.1113 / 0.1092 | ✗ |
| DINO | 50 / 100 | 0.0787 / 0.0632 | ✗ |
| **SIP** | 100 | **0.6530** | **✓** |

The negative result for BYOL/MoCo-v2/DINO **stands and remains substantive**: increasing the budget
from 50 to 100 epochs does not save them (MoCo 0.111 → 0.109, DINO 0.079 → 0.063). What is new
relative to the previous run is that **SIP passes the gate** (κ 0.6530 ≈ the continual-SSL level),
i.e. from-scratch in-domain initialization is in principle achievable within the project's budget.
In practice Config B/D use **continual-SSL**; SIP remains a constructed but unselected alternative.

### Stage 2 — continual-SSL: the gate is passed by both backbones, both gain

| Backbone | ImageNet κ | Continual κ | Δκ (run 1) | Δκ (run 2) |
|--------|-----------:|------------:|--------------:|--------------:|
| ResNet-50 | 0.3249 | 0.6591 | **+0.3342** | +0.2891 |
| EfficientNet-B3 | 0.4479 | 0.6827 | **+0.2348** | +0.2219 |

Both `passed = true` (beats_random ✓, competitive_with_imagenet ✓, not_collapsed ✓). There is no
collapse: feat_std 0.008 (random) → 0.056–0.057 (continual), kNN 0.31 → 0.69–0.70.

**A change of picture.** In the previous run EfficientNet-B3 gained nothing from continual-SSL
(κ 0.435 against ImageNet's 0.445), and this was reported as an honest asymmetry — "retina-aware
initialization only for ResNet-50". Per the current data **there is no asymmetry** — both backbones
receive a comparable gain. Formulations that relied on the previous asymmetry must be replaced.

### CFC-2.8 — the status has changed

The "preprocessing × initialization" confound in Config B/D formally remains, but it is
**decomposable**: the cumulative ablation under **a single initialization at all eight levels** yields
ΔwF1 = +0.0655 from L0 to L7 — exactly the D-vs-C magnitude in exp1, with L0 = Config C and
L7 = Config D coinciding numerically ([[H-2]], `tables/TAB-4.4_exp2_ablation.md`). That is, the
contribution of preprocessing has been measured independently of the contribution of initialization.
In §4.2, CFC-2.8 goes in as a note about a feature of the design and **not** as a limitation on the
conclusion that "the gain comes from preprocessing".

**Significance for the thesis (Premise 4).** The two-stage SSL narrative is preserved, but its moral
changes: (1) classical contrastive methods trained from scratch on a fundus corpus of this scale are
not competitive with ImageNet; (2) the specialized SIP and continual-SSL are competitive and deliver
a large in-domain gain on both backbones. Links: [[continual-ssl-init-decision]], [[H-1]], [[H-2]].

Tables: `tables/SSL_continual_gate.md`, `tables/TAB-4.10_exp7_smalldata.md`.
