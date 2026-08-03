# SSL initialization of the integrated arm + linear-probe gate (Premise 4 / CFC-2.8)

Governance (`HYPOTHESIS.md` Premise 4): the integrated arm (Config B/D) is initialized with in-domain
SSL on the unlabeled EyePACS "test" split (n = 53 576, disjoint from the Exp-1 corpus, SB-2.4),
BYOL protocol, 4-channel tensor, and admission into Exp-1 is **gated by a linear-probe criterion**.
Source: the **2026-08-03** run (`VALUES.md` §A1).

## Stage 1 — from-scratch SSL (§A1.1)

Reference: random κ ≈ 0.00; ImageNet κ ≈ 0.32–0.45.

| Method (from scratch, 4ch) | epochs | κ | passed |
|---------------------------|------:|--:|--------|
| BYOL (primary per governance) | 50 | 0.0018 | ✗ (collapse) |
| MoCo-v2 | 50 | 0.1125 | ✗ |
| MoCo-v2 | 100 | 0.1098 | ✗ |
| DINO | 50 | 0.0763 | ✗ |
| DINO | 100 | 0.0602 | ✗ |
| **SIP** | 100 | **0.6616** | **✓** |

**Change relative to the previous run.** Previously from-scratch SSL failed the gate entirely, and
the only remaining option was the continual-SSL fallback. Now **SIP (100 epochs) passes the gate**
(κ = 0.6616) — i.e. from-scratch in-domain initialization is in principle achievable within the
project's budget. The classical contrastive methods (BYOL/MoCo-v2/DINO) still fail, and increasing
from 50 to 100 epochs **does not save them** (MoCo 0.113 → 0.110, DINO 0.076 → 0.060 — a slight
deterioration). The negative result for BYOL/MoCo/DINO stands and remains substantive.

> SIP κ = 0.6616 practically coincides with continual-SSL on ResNet-50 (0.6591) — in this run it is
> marginally **above** it, though the gap (0.0025) is far inside probe noise. The initialization
> actually used in Config B/D is **continual-SSL**; SIP remains a constructed but unselected
> alternative.

## Stage 2 — continual-SSL, linear-probe gate (§A1.2)

Patient-level holdout, n_test = 8 036. Frozen backbone + linear head.

### ResNet-50 (Config B)

| Init | wF1 | ROC-AUC | κ | kNN | feat_std |
|------|----:|--------:|--:|----:|---------:|
| random | 0.6250 | 0.5096 | 0.0040 | 0.3097 | 0.0082 |
| ImageNet | 0.6602 | 0.7452 | 0.3381 | 0.5585 | 0.0415 |
| **Continual-SSL** | **0.7421** | **0.7688** | **0.6552** | **0.6918** | **0.0572** |
| Δ (continual − ImageNet) | +0.0819 | +0.0236 | **+0.3171** | +0.1333 | +0.0157 |

### EfficientNet-B3 (Config D)

| Init | wF1 | ROC-AUC | κ | kNN | feat_std |
|------|----:|--------:|--:|----:|---------:|
| random | 0.6245 | 0.5123 | 0.0047 | 0.3064 | 0.0072 |
| ImageNet | 0.6820 | 0.7461 | 0.4450 | 0.5813 | 0.0393 |
| **Continual-SSL** | **0.7562** | **0.7752** | **0.6807** | **0.7029** | **0.0571** |
| Δ (continual − ImageNet) | +0.0742 | +0.0291 | **+0.2357** | +0.1216 | +0.0178 |

### Second run (§A1.3)

| Backbone | ImageNet κ | Continual κ | Δκ |
|--------|-----------:|------------:|---:|
| ResNet-50 | 0.3526 | 0.6409 | **+0.2883** |
| EfficientNet-B3 | 0.4312 | 0.6648 | **+0.2336** |

## Gate verdict (§A1.4)

| Backbone | beats_random | competitive_with_imagenet | not_collapsed | passed |
|--------|--------------|---------------------------|---------------|--------|
| ResNet-50 | true | true | true | **true** |
| EfficientNet-B3 | true | true | true | **true** |

## Interpretation

1. **Continual-SSL delivers a large in-domain gain on both backbones** — Δκ +0.317 / +0.236 in the
   first run and +0.288 / +0.234 in the second. The direction and order of magnitude reproduce across
   runs.
2. **A change of picture for EfficientNet-B3.** In the previous run continual-SSL gave EfficientNet-B3
   no gain at all (κ 0.435 against ImageNet's 0.445, Δ ≈ 0), and this was reported as an honest
   asymmetry — "retina-aware initialization only for ResNet-50". Per the current data there is no
   asymmetry: **both backbones receive a comparable gain** (+0.236 and +0.317). Formulations that
   relied on the previous asymmetry must be replaced.
3. **There is no collapse:** feat_std rises from 0.007–0.008 (random) to 0.057 (continual), and kNN
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
