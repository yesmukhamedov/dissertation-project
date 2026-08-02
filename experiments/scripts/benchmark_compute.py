"""Computational benchmark for the Exp-1 configurations (A7).

Measures, for each of the four Exp-1 configurations (A/B = ResNet-50 3ch/4ch,
C/D = EfficientNet-B3 3ch/4ch) at the protocol input size 512x512:

* parameter count (total / trainable) — hardware independent;
* forward FLOPs per image via ``torch.utils.flop_counter.FlopCounterMode``
  (native to torch >= 2.0, no thop/fvcore dependency);
* inference latency (batch 1 and batch 16, fp32, CUDA-synchronised);
* peak VRAM for inference and for a full training step (fwd + bwd + optimizer),
  using the same mixed-precision setting each configuration was trained with
  (AMP on for ResNet-50, off for EfficientNet — fp16 overflow).

Results are written as JSON and as a Markdown table.

Usage:
    python scripts/benchmark_compute.py --out outputs/compute_benchmark
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
from pathlib import Path

import torch
import torch.nn as nn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.models.factory import create_model  # noqa: E402

# Exp-1 configurations: (config letter, model name, in_channels, mixed_precision-as-trained)
_CONFIGS: list[tuple[str, str, int, bool]] = [
    ("A", "resnet50", 3, True),
    ("B", "resnet50", 4, True),
    ("C", "efficientnet_b3", 3, False),
    ("D", "efficientnet_b3", 4, False),
]


def _build(model_name: str, in_channels: int) -> nn.Module:
    """Build a model exactly as the experiments do, without pretrained weights.

    Args:
        model_name: Factory name ("resnet50" / "efficientnet_b3").
        in_channels: 3 for the baseline arm, 4 for the integrated arm.

    Returns:
        The instantiated model (on CPU).
    """
    return create_model(
        model_name,
        {"pretrained": False, "num_classes": 5, "dropout": 0.4,
         "freeze_base": False, "in_channels": in_channels},
    )


def _count_params(model: nn.Module) -> tuple[int, int]:
    """Return (total, trainable) parameter counts."""
    total = sum(p.numel() for p in model.parameters())
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    return total, trainable


def _count_flops(model: nn.Module, in_channels: int, image_size: int,
                 device: torch.device) -> float | None:
    """Count forward FLOPs for a single image.

    Args:
        model: Model in eval mode on ``device``.
        in_channels: Input channel count.
        image_size: Square input side.
        device: Device to run the counting pass on.

    Returns:
        FLOPs for batch size 1, or None if the counter is unavailable.
    """
    try:
        from torch.utils.flop_counter import FlopCounterMode
    except ImportError:
        return None
    x = torch.randn(1, in_channels, image_size, image_size, device=device)
    counter = FlopCounterMode(display=False)
    with counter, torch.no_grad():
        model(x)
    return float(counter.get_total_flops())


def _sync(device: torch.device) -> None:
    if device.type == "cuda":
        torch.cuda.synchronize()


def _latency(model: nn.Module, in_channels: int, image_size: int, batch_size: int,
             device: torch.device, iters: int, warmup: int) -> dict:
    """Time fp32 inference over ``iters`` forward passes.

    Args:
        model: Model in eval mode on ``device``.
        in_channels: Input channel count.
        image_size: Square input side.
        batch_size: Batch size to time.
        device: Device to benchmark on.
        iters: Number of timed iterations.
        warmup: Number of untimed warm-up iterations.

    Returns:
        Dict with per-batch latency stats (ms) and throughput (images/s).
    """
    x = torch.randn(batch_size, in_channels, image_size, image_size, device=device)
    with torch.no_grad():
        for _ in range(warmup):
            model(x)
        _sync(device)
        samples: list[float] = []
        for _ in range(iters):
            t0 = time.perf_counter()
            model(x)
            _sync(device)
            samples.append((time.perf_counter() - t0) * 1000.0)
    mean_ms = statistics.mean(samples)
    return {
        "batch_size": batch_size,
        "latency_ms_mean": round(mean_ms, 3),
        "latency_ms_median": round(statistics.median(samples), 3),
        "latency_ms_std": round(statistics.pstdev(samples), 3),
        "latency_ms_per_image": round(mean_ms / batch_size, 3),
        "throughput_img_s": round(batch_size / (mean_ms / 1000.0), 2),
    }


def _peak_vram_inference(model: nn.Module, in_channels: int, image_size: int,
                         batch_size: int, device: torch.device) -> float | None:
    """Peak allocated VRAM (MiB) for one inference batch, or None on CPU."""
    if device.type != "cuda":
        return None
    torch.cuda.empty_cache()
    torch.cuda.reset_peak_memory_stats()
    x = torch.randn(batch_size, in_channels, image_size, image_size, device=device)
    with torch.no_grad():
        model(x)
    _sync(device)
    return round(torch.cuda.max_memory_allocated() / 2 ** 20, 1)


def _peak_vram_train_step(model: nn.Module, in_channels: int, image_size: int,
                          batch_size: int, device: torch.device,
                          mixed_precision: bool) -> float | None:
    """Peak allocated VRAM (MiB) for a full fwd+bwd+step, or None on CPU.

    Args:
        model: Model on ``device`` (switched to train mode here).
        in_channels: Input channel count.
        image_size: Square input side.
        batch_size: Training batch size (protocol: 16).
        device: Device to benchmark on.
        mixed_precision: Use AMP, matching how the configuration was trained.

    Returns:
        Peak allocated MiB, or None on CPU.
    """
    if device.type != "cuda":
        return None
    model.train()
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)
    scaler = torch.amp.GradScaler("cuda", enabled=mixed_precision)
    criterion = nn.CrossEntropyLoss()
    x = torch.randn(batch_size, in_channels, image_size, image_size, device=device)
    y = torch.randint(0, 5, (batch_size,), device=device)

    torch.cuda.empty_cache()
    torch.cuda.reset_peak_memory_stats()
    optimizer.zero_grad(set_to_none=True)
    with torch.amp.autocast("cuda", enabled=mixed_precision):
        loss = criterion(model(x), y)
    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()
    _sync(device)
    peak = round(torch.cuda.max_memory_allocated() / 2 ** 20, 1)
    model.eval()
    del optimizer, x, y
    torch.cuda.empty_cache()
    return peak


def _to_markdown(results: list[dict], meta: dict) -> str:
    """Render the benchmark results as a Markdown report."""
    lines = [
        "# A7 — Вычислительные бенчмарки (params / FLOPs / latency / VRAM)",
        "",
        f"Замерено {meta['timestamp']} на **{meta['device_name']}** "
        f"(torch {meta['torch_version']}, CUDA {meta['cuda_version']}), "
        f"вход {meta['image_size']}×{meta['image_size']}, fp32-инференс, "
        f"{meta['iters']} итераций после {meta['warmup']} прогревочных.",
        "",
        "| Config | Модель | Ch | Params | GFLOPs/изобр. | Latency bs=1 (мс) | "
        "Latency bs=16 (мс/изобр.) | Throughput bs=16 (изобр./с) | VRAM инференс bs=16 (МиБ) | "
        "VRAM train-step bs=16 (МиБ) | AMP при обучении |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in results:
        lat1 = next(b for b in r["latency"] if b["batch_size"] == 1)
        lat16 = next((b for b in r["latency"] if b["batch_size"] == 16), None)
        gflops = f"{r['flops'] / 1e9:.1f}" if r["flops"] else "н/д"
        lines.append(
            f"| {r['config']} | {r['model']} | {r['in_channels']} | "
            f"{r['params_total'] / 1e6:.2f}M | {gflops} | "
            f"{lat1['latency_ms_mean']:.1f} | "
            f"{lat16['latency_ms_per_image']:.1f} | {lat16['throughput_img_s']:.1f} | "
            f"{r['vram_inference_mib']} | {r['vram_train_step_mib']} | "
            f"{'да' if r['mixed_precision_as_trained'] else 'нет'} |"
        )
    lines += [
        "",
        "FLOPs — прямой проход на одно изображение, `torch.utils.flop_counter` "
        "(умножение-сложение считается за 2 операции). VRAM — "
        "`torch.cuda.max_memory_allocated`; train-step = fwd+bwd+optimizer.step "
        "с тем же mixed-precision, с каким конфигурация обучалась.",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    """Run the benchmark for all four Exp-1 configurations."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("outputs/compute_benchmark"),
                        help="Output path stem (writes .json and .md)")
    parser.add_argument("--image-size", type=int, default=512)
    parser.add_argument("--batch-sizes", type=str, default="1,16")
    parser.add_argument("--iters", type=int, default=50)
    parser.add_argument("--warmup", type=int, default=10)
    parser.add_argument("--device", type=str, default="cuda")
    args = parser.parse_args()

    device = torch.device(args.device if torch.cuda.is_available() or args.device == "cpu"
                          else "cpu")
    batch_sizes = [int(b) for b in args.batch_sizes.split(",")]
    results: list[dict] = []

    for cfg, model_name, in_ch, amp in _CONFIGS:
        print(f"[{cfg}] {model_name} in_channels={in_ch} …", flush=True)
        model = _build(model_name, in_ch).to(device).eval()
        total, trainable = _count_params(model)
        entry = {
            "config": cfg,
            "model": model_name,
            "in_channels": in_ch,
            "params_total": total,
            "params_trainable": trainable,
            "flops": _count_flops(model, in_ch, args.image_size, device),
            "latency": [_latency(model, in_ch, args.image_size, bs, device,
                                 args.iters, args.warmup) for bs in batch_sizes],
            "vram_inference_mib": _peak_vram_inference(model, in_ch, args.image_size,
                                                       16, device),
            "vram_train_step_mib": _peak_vram_train_step(model, in_ch, args.image_size,
                                                         16, device, amp),
            "mixed_precision_as_trained": amp,
        }
        results.append(entry)
        print(f"    params {total/1e6:.2f}M · "
              f"{(entry['flops'] or 0)/1e9:.1f} GFLOPs · "
              f"VRAM train {entry['vram_train_step_mib']} MiB", flush=True)
        del model
        if device.type == "cuda":
            torch.cuda.empty_cache()

    meta = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "device_name": (torch.cuda.get_device_name(0) if device.type == "cuda" else "CPU"),
        "torch_version": torch.__version__,
        "cuda_version": torch.version.cuda or "—",
        "image_size": args.image_size,
        "iters": args.iters,
        "warmup": args.warmup,
    }

    out = args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out.with_suffix(".json"), "w", encoding="utf-8") as f:
        json.dump({"_meta": meta, "results": results}, f, indent=2, ensure_ascii=False)
    with open(out.with_suffix(".md"), "w", encoding="utf-8") as f:
        f.write(_to_markdown(results, meta))
    print(f"\nSaved: {out.with_suffix('.json')} and {out.with_suffix('.md')}")


if __name__ == "__main__":
    main()
