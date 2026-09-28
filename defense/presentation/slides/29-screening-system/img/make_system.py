"""Slide 29: the screening system — browser client, inference service with the same pipeline code, doctor in the loop,
kk/ru/en.

Content: demo/CLAUDE.md (FastAPI inference backend on CUDA + React dashboard; public route Cloudflare Pages + tunnel,
https://dr-classification.pages.dev) and the slide text (RTX 3060 12 GB). The CNN box names EfficientNet-B3 (config D) —
the checkpoint the demo must serve before the screenshots are taken (TODO.md §1).
Replaces a36_1 (a generated stock illustration with garbled labels). 𝒫 via mathtext (no glyph in DejaVu Sans).
Run: python make_system.py  ->  system_<lang>.png
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))
from figlib import BLUE, INK2, LANGS, arrow, box, save  # noqa: E402

P = r"$\mathcal{P}$"
T = {"kk": {"doc": "Дәрігер", "cli": "Браузер\nклиенті\n(React)", "srv": "Шығару сервисі (FastAPI, GPU RTX 3060)",
            "p": f"{P} — 8 кезең\n(эксперименттер\nкоды)", "cnn": "CNN\nEfficientNet-B3", "cam": "Grad-CAM", "up": "кескін",
            "down": "дәреже, ықтималдықтар,\nкезеңдер, назар картасы", "ok": "растайды\nнемесе түзетеді"},
     "ru": {"doc": "Врач", "cli": "Браузерный\nклиент\n(React)", "srv": "Сервис вывода (FastAPI, GPU RTX 3060)",
            "p": f"{P} — 8 этапов\n(код\nэкспериментов)", "cnn": "CNN\nEfficientNet-B3", "cam": "Grad-CAM", "up": "снимок",
            "down": "степень, вероятности,\nэтапы, карта внимания", "ok": "подтверждает\nили исправляет"},
     "en": {"doc": "Doctor", "cli": "Browser\nclient\n(React)", "srv": "Inference service (FastAPI, GPU RTX 3060)",
            "p": f"{P} — 8 stages\n(the experiments'\ncode)", "cnn": "CNN\nEfficientNet-B3", "cam": "Grad-CAM", "up": "image",
            "down": "grade, probabilities,\nstages, attention map", "ok": "confirms\nor corrects"}}


def main() -> None:
    """Write system_{lang}.png."""
    for lang in LANGS:
        t = T[lang]
        fig, ax = plt.subplots(figsize=(14, 4.8))
        fig.subplots_adjust(0.005, 0.005, 0.995, 0.995)
        ax.set_xlim(-0.01, 1.01)
        ax.set_ylim(0, 1)
        ax.axis("off")
        box(ax, 0.0, 0.38, 0.1, 0.24, t["doc"], fc="#f7e7e1", bold=True, size=13)
        box(ax, 0.16, 0.26, 0.15, 0.48, t["cli"], fc="#e4eefb", size=12.5)
        ax.text(0.235, 0.2, "dr-classification.pages.dev", ha="center", fontsize=10.5, color=INK2)
        ax.add_patch(plt.Rectangle((0.43, 0.1), 0.565, 0.8, fill=False, ec=BLUE, lw=1.8, ls=(0, (5, 3))))
        ax.text(0.7125, 0.83, t["srv"], ha="center", fontsize=12.5, color=BLUE, fontweight="bold")
        box(ax, 0.455, 0.28, 0.2, 0.44, t["p"], fc="#e3f1ea", size=12, bold=True)
        box(ax, 0.685, 0.28, 0.16, 0.44, t["cnn"], fc="#e4eefb", size=12, bold=True)
        box(ax, 0.87, 0.28, 0.11, 0.44, t["cam"], fc="#f4f3f0", size=12)
        arrow(ax, (0.1, 0.55), (0.16, 0.55))
        arrow(ax, (0.16, 0.45), (0.1, 0.45))
        ax.text(0.13, 0.2, t["ok"], ha="center", fontsize=10.5, color=INK2)
        arrow(ax, (0.31, 0.62), (0.455, 0.62), t["up"])
        arrow(ax, (0.455, 0.38), (0.31, 0.38))
        ax.text(0.37, 0.12, t["down"], ha="center", fontsize=10.5, color=INK2)
        arrow(ax, (0.655, 0.5), (0.685, 0.5))
        arrow(ax, (0.845, 0.5), (0.87, 0.5))
        save(fig, HERE / f"system_{lang}.png")


if __name__ == "__main__":
    main()
