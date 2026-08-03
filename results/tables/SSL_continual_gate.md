# SSL initialization of the integrated arm + linear-probe gate (Premise 4 / CFC-2.8)

Governance (`HYPOTHESIS.md` Premise 4): the integrated arm (Config B/D) is initialized with in-domain
SSL on the unlabeled EyePACS "test" split (n = 53 576, disjoint from the Exp-1 corpus, SB-2.4),
BYOL protocol, 4-channel tensor, and admission into Exp-1 is **gated by a linear-probe criterion**.
Source: the **2026-08-03** run (`VALUES.md` §A1).

## Stage 1 — from-scratch SSL (§A1.1)

Reference: random κ ≈ 0.00; ImageNet κ ≈ 0.32–0.45.

| Method (from scratch, 4ch) | epochs | κ | passed |
|---------------------------|------:|--:|--------|
| BYOL (primary per governance) | 50 | 0.0023 | ✗ (collapse) |
| MoCo-v2 | 50 | 0.1113 | ✗ |
| MoCo-v2 | 100 | 0.1092 | ✗ |
| DINO | 50 | 0.0787 | ✗ |
| DINO | 100 | 0.0632 | ✗ |
| **SIP** | 100 | **0.6530** | **✓** |

**Change relative to the previous run.** Previously from-scratch SSL failed the gate entirely, and
the only remaining option was the continual-SSL fallback. Now **SIP (100 epochs) passes the gate**
(κ = 0.6530) — i.e. from-scratch in-domain initialization is in principle achievable within the
project's budget. The classical contrastive methods (BYOL/MoCo-v2/DINO) still fail, and increasing
from 50 to 100 epochs **does not save them** (MoCo 0.111 → 0.109, DINO 0.079 → 0.063 — a slight
deterioration). The negative result for BYOL/MoCo/DINO stands and remains substantive.

> SIP κ = 0.6530 practically coincides with continual-SSL on ResNet-50 (0.6591). The initialization
> actually used in Config B/D is **continual-SSL**; SIP remains a constructed but unselected
> alternative.

## Stage 2 — continual-SSL, linear-probe gate (§A1.2)

Patient-level holdout, n_test = 8 036. Frozen backbone + linear head.

### ResNet-50 (Config B)

| Init | wF1 | ROC-AUC | κ | kNN | feat_std |
|------|----:|--------:|--:|----:|---------:|
| random | 0.6212 | 0.5030 | 0.0043 | 0.3131 | 0.0081 |
| ImageNet | 0.6675 | 0.7388 | 0.3249 | 0.5556 | 0.0418 |
| **Continual-SSL** | **0.7419** | **0.7725** | **0.6591** | **0.6869** | **0.0566** |
| Δ (continual − ImageNet) | +0.0744 | +0.0337 | **+0.3342** | +0.1313 | +0.0148 |

### EfficientNet-B3 (Config D)

| Init | wF1 | ROC-AUC | κ | kNN | feat_std |
|------|----:|--------:|--:|----:|---------:|
| random | 0.6281 | 0.5142 | 0.0045 | 0.3083 | 0.0078 |
| ImageNet | 0.6804 | 0.7396 | 0.4479 | 0.5885 | 0.0394 |
| **Continual-SSL** | **0.7554** | **0.7733** | **0.6827** | **0.7013** | **0.0569** |
| Δ (continual − ImageNet) | +0.0750 | +0.0337 | **+0.2348** | +0.1128 | +0.0175 |

### Second run (§A1.3)

| Backbone | ImageNet κ | Continual κ | Δκ |
|--------|-----------:|------------:|---:|
| ResNet-50 | 0.3549 | 0.6440 | **+0.2891** |
| EfficientNet-B3 | 0.4388 | 0.6607 | **+0.2219** |

## Gate verdict (§A1.4)

| Backbone | beats_random | competitive_with_imagenet | not_collapsed | passed |
|--------|--------------|---------------------------|---------------|--------|
| ResNet-50 | true | true | true | **true** |
| EfficientNet-B3 | true | true | true | **true** |

## Interpretation

1. **Continual-SSL delivers a large in-domain gain on both backbones** — Δκ +0.334 / +0.235 in the
   first run and +0.289 / +0.222 in the second. The direction and order of magnitude reproduce across
   runs.
2. **A change of picture for EfficientNet-B3.** In the previous run continual-SSL gave EfficientNet-B3
   no gain at all (κ 0.435 against ImageNet's 0.445, Δ ≈ 0), and this was reported as an honest
   asymmetry — "retina-aware initialization only for ResNet-50". Per the current data there is no
   asymmetry: **both backbones receive a comparable gain** (+0.235 and +0.334). Formulations that
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
