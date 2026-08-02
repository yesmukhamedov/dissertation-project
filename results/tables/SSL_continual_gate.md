# SSL initialization of the integrated arm + linear-probe gate (Premise 4 / CFC-2.8)

Governance (`HYPOTHESIS.md` Premise 4): the integrated arm (Config B/D) is initialized with in-domain
SSL on the unlabeled EyePACS "test" split (n = 53 576, disjoint from the Exp-1 corpus, SB-2.4),
BYOL protocol, 4-channel tensor, and admission into Exp-1 is **gated by a linear-probe criterion**.
Source: the **2026-08-02** run (`VALUES.md` §A1).

## Stage 1 — from-scratch SSL (§A1.1)

Reference: random κ ≈ 0.00; ImageNet κ ≈ 0.32–0.45.

| Method (from scratch, 4ch) | epochs | κ | passed |
|---------------------------|------:|--:|--------|
| BYOL (primary per governance) | 50 | 0.0000 | ✗ (collapse) |
| MoCo-v2 | 50 | 0.1120 | ✗ |
| MoCo-v2 | 100 | 0.1090 | ✗ |
| DINO | 50 | 0.0750 | ✗ |
| DINO | 100 | 0.0610 | ✗ |
| **SIP** | 100 | **0.6580** | **✓** |

**Change relative to the previous run.** Previously from-scratch SSL failed the gate entirely, and
the only remaining option was the continual-SSL fallback. Now **SIP (100 epochs) passes the gate**
(κ = 0.6580) — i.e. from-scratch in-domain initialization is in principle achievable within the
project's budget. The classical contrastive methods (BYOL/MoCo-v2/DINO) still fail, and increasing
from 50 to 100 epochs **does not save them** (MoCo 0.112 → 0.109, DINO 0.075 → 0.061 — a slight
deterioration). The negative result for BYOL/MoCo/DINO stands and remains substantive.

> SIP κ = 0.6580 practically coincides with continual-SSL on ResNet-50 (0.6590). The initialization
> actually used in Config B/D is **continual-SSL**; SIP remains a constructed but unselected
> alternative.

## Stage 2 — continual-SSL, linear-probe gate (§A1.2)

Patient-level holdout, n_test = 8 036. Frozen backbone + linear head.

### ResNet-50 (Config B)

| Init | wF1 | ROC-AUC | κ | kNN | feat_std |
|------|----:|--------:|--:|----:|---------:|
| random | 0.6240 | 0.5000 | 0.0000 | 0.3120 | 0.0080 |
| ImageNet | 0.6660 | 0.7420 | 0.3400 | 0.5610 | 0.0410 |
| **Continual-SSL** | **0.7430** | **0.7720** | **0.6590** | **0.6880** | **0.0570** |
| Δ (continual − ImageNet) | +0.0770 | +0.0300 | **+0.3190** | +0.1270 | +0.0160 |

### EfficientNet-B3 (Config D)

| Init | wF1 | ROC-AUC | κ | kNN | feat_std |
|------|----:|--------:|--:|----:|---------:|
| random | 0.6240 | 0.5200 | 0.0000 | 0.3080 | 0.0075 |
| ImageNet | 0.6830 | 0.7390 | 0.4450 | 0.5840 | 0.0398 |
| **Continual-SSL** | **0.7560** | **0.7730** | **0.6820** | **0.7010** | **0.0562** |
| Δ (continual − ImageNet) | +0.0730 | +0.0340 | **+0.2370** | +0.1170 | +0.0164 |

### Second run (§A1.3)

| Backbone | ImageNet κ | Continual κ | Δκ |
|--------|-----------:|------------:|---:|
| ResNet-50 | 0.3570 | 0.6410 | **+0.2840** |
| EfficientNet-B3 | 0.4350 | 0.6580 | **+0.2230** |

## Gate verdict (§A1.4)

| Backbone | beats_random | competitive_with_imagenet | not_collapsed | passed |
|--------|--------------|---------------------------|---------------|--------|
| ResNet-50 | true | true | true | **true** |
| EfficientNet-B3 | true | true | true | **true** |

## Interpretation

1. **Continual-SSL delivers a large in-domain gain on both backbones** — Δκ +0.319 / +0.237 in the
   first run and +0.284 / +0.223 in the second. The direction and order of magnitude reproduce across
   runs.
2. **A change of picture for EfficientNet-B3.** In the previous run continual-SSL gave EfficientNet-B3
   no gain at all (κ 0.435 against ImageNet's 0.445, Δ ≈ 0), and this was reported as an honest
   asymmetry — "retina-aware initialization only for ResNet-50". Per the 2026-08-02 data there is no
   asymmetry: **both backbones receive a comparable gain** (+0.237 and +0.319). Formulations that
   relied on the previous asymmetry must be replaced.
3. **There is no collapse:** feat_std rises from 0.008 (random) to 0.056–0.057 (continual), and kNN
   from 0.31 to 0.69–0.70. The features are not degenerate.
4. **CFC-2.8 — the status has changed.** The "preprocessing × initialization" confound in Config B/D
   formally remains, but it is now **decomposable**: the cumulative ablation
   (`TAB-4.4_exp2_ablation.md`) under a **single** initialization at all eight levels yields
   ΔwF1 = +0.0655 from L0 to L7 — exactly the same gain as D-vs-C in exp1. That is, the contribution
   of preprocessing has been measured separately from the contribution of initialization, and H-1 no
   longer rests on an indivisible composite. This should be reflected in the caveat to §4.2 in place
   of the previous formulation that "the gain cannot be attributed to preprocessing".

Links: [[continual-ssl-init-decision]], `findings/exp1.md`, `hypotheses/H-1.md`,
`hypotheses/exp7-and-SSL.md`.
