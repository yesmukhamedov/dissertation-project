"""Slide 21 (and R1): experiment 1 — weighted F1 of the four configurations and per-grade F1, kk/ru/en.

Numbers: results/tables/TAB-4.2_exp1_factorial.md (wF1 mean ± SD over 5 folds, Δ with 95 % CI) and
results/tables/exp1_per_class.md (per-grade F1, configs C and D). Replaces a24_1 … a24_3 (the old run: 0.727 / 0.780,
«V5 Pipeline»); ΔAUC and Δκ are said in the talk, not drawn.
Run: python make_exp1.py  ->  exp1_<lang>.png, and ../../R1-limitations/img/perclass_<lang>.png
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))
from figlib import ARM, BLUE, GRAY, INK, INK2, LANGS, WF1, clean, commas, dec, md_table, num, save  # noqa: E402

T = {"kk": ("Төрт конфигурацияның салмақталған F1-і", "EfficientNet-B3: ДР дәрежелері бойынша F1", "п.п."),
     "ru": ("Взвешенный F1 четырёх конфигураций", "EfficientNet-B3: F1 по степеням ДР", "п.п."),
     "en": ("Weighted F1 of the four configurations", "EfficientNet-B3: F1 by DR grade", "pp")}


def load() -> tuple[dict, list, list, dict]:
    """Return {config: (mean, sd)}, per-grade F1 of C and D, and {pair: Δ} from the results tables."""
    wf1 = {r["Config"]: (num(r["Weighted F1"]), num(r["Weighted F1"].split("±")[1])) for r in
           md_table("TAB-4.2_exp1_factorial.md", "Config")}
    c = [num(r["F1"]) for r in md_table("exp1_per_class.md", "Class", 2)]
    d = [num(r["F1"]) for r in md_table("exp1_per_class.md", "Class", 3)]
    delta = {r["Pair"]: num(r["Δ"]) for r in md_table("TAB-4.2_exp1_factorial.md", "Pair") if r["Metric"] == "wF1"}
    return wf1, c, d, delta


def bars_wf1(ax, lang: str, wf1: dict, delta: dict) -> None:
    """Grouped bars: two backbones × two arms, SD whiskers, Δ above each pair."""
    base, integ = ARM[lang]
    for g, (arch, (b, i)) in enumerate((("ResNet-50", ("A", "B")), ("EfficientNet-B3", ("C", "D")))):
        for k, (cfg, col, lab) in enumerate(((b, GRAY, base), (i, BLUE, integ))):
            m, sd = wf1[cfg]
            x = g + (k - 0.5) * 0.38
            ax.bar(x, m, 0.34, color=col, label=lab if g == 0 else None)
            ax.errorbar(x, m, sd, color=INK2, capsize=4, lw=1.2)
            ax.text(x, m + sd + 0.006, f"{cfg}\n{dec(m, lang)}", ha="center", va="bottom", fontsize=12, color=INK)
        dd = delta[f"{i} − {b}"] * 100
        ax.text(g, 0.99, f"+{dec(dd, lang, 2)} {T[lang][2]}", ha="center", fontsize=13, color=BLUE, fontweight="bold")
    ax.set_xticks([0, 1], ["ResNet-50", "EfficientNet-B3"])
    ax.set_ylim(0, 1.05)
    ax.set_ylabel(WF1[lang])
    ax.set_title(T[lang][0], fontsize=13, color=INK, pad=10)
    ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=2, fontsize=11)
    clean(ax)
    commas(ax, lang)


def bars_grade(ax, lang: str, c: list, d: list) -> None:
    """Per-grade F1 of C and D with the gain in pp above each pair."""
    x = np.arange(5)
    ax.bar(x - 0.19, c, 0.36, color=GRAY, label=ARM[lang][0])
    ax.bar(x + 0.19, d, 0.36, color=BLUE, label=ARM[lang][1])
    for i in x:
        ax.text(i + 0.19, d[i] + 0.015, dec(d[i], lang, 2), ha="center", fontsize=11, color=INK)
        ax.text(i - 0.19, c[i] + 0.015, dec(c[i], lang, 2), ha="center", fontsize=11, color=INK2)
        ax.text(i, max(c[i], d[i]) + 0.09, f"+{dec((d[i] - c[i]) * 100, lang, 1)}", ha="center", fontsize=11,
                color=BLUE, fontweight="bold")
    ax.set_xticks(x, [f"DR{i}" for i in x])
    ax.set_ylim(0, 1.1)
    ax.set_ylabel("F1")
    ax.set_title(T[lang][1], fontsize=13, color=INK, pad=10)
    ax.legend(frameon=False, loc="upper right", fontsize=11)
    clean(ax)
    commas(ax, lang)


def main() -> None:
    """Write exp1_{lang}.png (two panels) and R1's perclass_{lang}.png."""
    wf1, c, d, delta = load()
    for lang in LANGS:
        fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 5), gridspec_kw={"width_ratios": [1, 1.3]})
        bars_wf1(a1, lang, wf1, delta)
        bars_grade(a2, lang, c, d)
        fig.tight_layout(w_pad=3)
        save(fig, HERE / f"exp1_{lang}.png")
        fig, ax = plt.subplots(figsize=(7.5, 4.8))
        bars_grade(ax, lang, c, d)
        fig.tight_layout()
        save(fig, HERE.parents[1] / "R1-limitations" / "img" / f"perclass_{lang}.png")


if __name__ == "__main__":
    main()
