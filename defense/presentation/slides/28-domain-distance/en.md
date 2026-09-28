---
slide: 28
id: domain-distance
lang: en
status: draft
seconds: 35
source: нового слайда в архиве не было; рисунок — рис. 3.x диссертации (fig4_17)
terms: [domain_distance, mmd, kl_divergence, penultimate_layer]
---

# Domain distance in feature space (H-3)

## На слайде

Figure: MMD to six target corpora, Δd with 95 % interval, KL reduction (`img/fig4_17_domain_distance.png`)

- Distance is measured at the penultimate layer (MMD) and at pixel level (KL)
- It falls on **6 / 6** corpora: Δd = **0.070…0.093**, every 95 % interval excludes zero; KL **−34…−38 %**
- Normalisation uses source-domain statistics only → the convergence is a property of preprocessing, not of adaptation

## Речь

The claim that preprocessing improves robustness across domains is usually backed only by external accuracy. We measured the mechanism itself: the distance from the training corpus to six external ones at the penultimate layer falls on all six by 0.070–0.093, with intervals excluding zero, and by 34–38 percent at pixel level. The transform never saw the target corpora. Caveat: the size of the reduction does not predict the size of the gain — only the direction holds.
