# Computational benchmarks (A7) + image quality (A8)

## A7 — Parameters, FLOPs, latency, VRAM

Measured on an RTX 3060 12 GB, input 512×512, fp32 inference.
Source: the **2026-08-02** run (`VALUES.md` §A7.1); the values match the 2026-07-28 measurement
(`experiments/outputs/compute_benchmark.{json,md}`, script `scripts/benchmark_compute.py`) —
**this block was not changed by the run**.

| Config | Model | Ch | Params | GFLOPs/img | Latency bs=1 (ms) | bs=16 (ms/img) | Throughput bs=16 (img/s) | VRAM inference bs=16 (MiB) | VRAM train-step bs=16 (MiB) |
|---|---|---|---|---|---|---|---|---|---|
| A | ResNet-50 | 3 | 23.52M | 42.7 | 10.5 | 8.2 | 121.6 | 978 | 3724 |
| B | ResNet-50 | 4 | 23.52M | 43.1 | 10.5 | 8.3 | 120.5 | 1002 | 3748 |
| C | EfficientNet-B3 | 3 | 10.70M | 10.0 | 12.8 | 7.5 | 132.8 | 1515 | 13726 |
| D | EfficientNet-B3 | 4 | 10.70M | 10.1 | 14.5 | 7.6 | 132.3 | 1531 | 13742 |

Measurement conditions: torch 2.5.1+cu121, 50 iterations after 10 warm-up ones; train-step = fwd +
bwd + optimizer.step under the same mixed-precision setting the configuration was trained with (AMP
enabled for ResNet-50, disabled for EfficientNet). Optimizer AdamW (memory-identical to the
protocol's Adam).

### Observations (for §5.3.2 / FIG-5.2)

- **The cost of the 4th channel is close to zero:** +0.4 GFLOPs (+0.9%), +24 MiB VRAM, +~3k
  parameters in the stem (which rounds to the same 23.52M / 10.70M), and latency within noise.
  Together with the +6.55 pp wF1 gain (`TAB-4.2_exp1_factorial.md`) this gives a quantitative
  formulation of the central thesis: **the pipeline is a cheap prior**. Its entire computational cost
  lies in CPU preprocessing, not in the network.
- **FLOPs ≠ latency.** EfficientNet-B3 is **4.3× cheaper in FLOPs** (10 against 43 GFLOPs) and 2.2×
  lighter in parameters, yet in wall-clock time it is only ~9% faster at bs=16 and **slower** at bs=1
  (12.8–14.5 against 10.5 ms): depthwise convolutions utilize tensor cores poorly. The
  performance–complexity trade-off argument must be made from measured time, not from FLOPs.
- **Training VRAM is the bottleneck for EfficientNet:** 13.7 GiB against 3.7 GiB for ResNet-50 (fp32
  without AMP + large activation maps at 512²). That exceeds the RTX 3060's physical 12 GiB — the
  measurement went through only thanks to "sharing" into system memory (WSL2/WDDM). **Conclusion for
  the text:** the batch_size = 16 limit is dictated by fp32 activations at 512², not by model size
  (10.7M parameters).
- ⚠️ The demo (`data.js` `COMPUTE`) shows **25.6M / 12.2M** — this does not match the real
  **23.52M / 10.70M**. Do not use the demo numbers.

## A8 — Image-quality metrics (CNR / Entropy / SSIM)

**Closed via exp2.** Real values across all 8 levels of the cumulative ablation, computed on the
float outputs of the pipeline (not on display PNGs), sample n = 100 →
**`TAB-4.5_exp2_image_quality.md`**. A second independent slice is the CNR within the flat-field σ
sweep (`exp2_flatfield_sigma_sweep.md`).

Summary of findings:

| Finding | Where |
|---|---|
| Flat-field is the only stage that noticeably raises CNR (20.38 → 28.60) | `TAB-4.5` |
| CLAHE lowers CNR (28.60 → 24.15) but produces peak entropy (5.884) | `TAB-4.5` |
| Geometric stages 0–3 leave CNR/Entropy unchanged yet deliver +2.85 pp wF1 | `TAB-4.5` |
| Within the flat-field stage, CNR and wF1 move together (both peak at σ = 0.07) | `exp2_flatfield_sigma_sweep` |
| Across stages there is no IQ ↔ wF1 correspondence | `TAB-4.5` |

**Final formulation:** the IQ metrics capture the photometric part of the pipeline's mechanism but do
not exhaust it — the gain from geometric canonicalization and augmentation is invisible to them. As
predictors of the classification gain, CNR/Entropy/SSIM are insufficient.

**Residual gap:** **VVI is not implemented** in `src/utils/image_quality.py`. The `VVI` value in the
demo `data.js` has no source in the code — do not use it.
