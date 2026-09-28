---
slide: 39
id: conclusion
lang: en
status: draft
seconds: 50
source: архив сл. 37 — переработан (по задачам)
terms: [conclusion, objectives]
---

# Conclusion

## На слайде

1. **Analysis (Ch. 1):** the research problem was formulated — preprocessing is not reported as part of the model; the requirements of resource-limited screening were defined
2. **Methodology (Ch. 2):** the 8-stage pipeline was formalised (clip limit, illumination correction), two architectures with 4-channel input, pretraining selected by a gate (κ 0.655 / 0.681), the evaluation protocol fixed before the experiments
3. **Experiments (Ch. 3):** F1 **+6.5 pp**; ablation 0.754 → 0.819; distance shrinks on 6 / 6 corpora; APTOS **+0.089**; camera spread **2.4×** narrower; IDRiD / Messidor-2 **+0.069 / +0.054**; ALO 4 / 4; small data **+0.080** — all 7 pre-registered hypotheses supported
4. **System (Ch. 4):** the inference service and browser client were built on the same pipeline code as the experiments; certificate No. 78109

**The main finding is consistency:** the advantage exists in-domain, decomposes across stages, goes with a measured distance and appears on every external corpus

## Речь

The conclusion follows the objectives. First: the problem was formulated. Second: the eight-stage pipeline was formalised and adapted to two architectures, with the protocol fixed before the experiments. Third: the integrated configuration is 6.5 percentage points higher in F1 in-domain, the gain decomposes by stage, the distance to six corpora shrinks, and on every external, device and clinical corpus and on small data the configuration is higher; attention agrees better with annotation. Fourth: the screening system was built. The main finding is consistency, and it supports treating preprocessing as a model component.
