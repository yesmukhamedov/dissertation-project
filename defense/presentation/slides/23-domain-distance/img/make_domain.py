"""Slide 23: domain distance — MMD from EyePACS to six target corpora, baseline vs integrated arm, kk/ru/en.

Numbers: results/tables/H-3_domain_distance.md (MMD table: d(BASE, X), d(INT, X), Δd, 95 % CI; KL table: reduction).
One dumbbell per corpus; Δd with its CI and the KL reduction are printed at the right edge.
Replaces fig4_17_domain_distance.png (three small panels, English, unreadable at slide size).
Run: python make_domain.py  ->  domain_<lang>.png
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))
from figlib import ARM, BLUE, GRAY, INK, INK2, LANGS, clean, commas, dec, md_table, num, save  # noqa: E402

T = {"kk": ("EyePACS-тен MMD қашықтығы (кем — жақынырақ)", "Δd [95 % СА]", "KL"),
     "ru": ("MMD до EyePACS (меньше — ближе)", "Δd [95 % ДИ]", "KL"),
     "en": ("MMD to EyePACS (lower is closer)", "Δd [95 % CI]", "KL")}


def main() -> None:
    """Write domain_{lang}.png."""
    mmd = md_table("H-3_domain_distance.md", "Target domain X", 0)
    kl = {r["Target domain X"]: r["Reduction"] for r in md_table("H-3_domain_distance.md", "Target domain X", 1)}
    mmd.sort(key=lambda r: num(r["d(BASE, X)"]))
    for lang in LANGS:
        t = T[lang]
        fig, ax = plt.subplots(figsize=(11, 4.9))
        for y, r in enumerate(mmd):
            b, i = num(r["d(BASE, X)"]), num(r["d(INT, X)"])
            ax.plot([i, b], [y, y], color=INK2, lw=1.5, zorder=1)
            ax.scatter([b], [y], s=110, color=GRAY, zorder=2, label=ARM[lang][0] if y == 0 else None)
            ax.scatter([i], [y], s=110, color=BLUE, zorder=3, label=ARM[lang][1] if y == 0 else None)
            lo, hi = [num(v) for v in r["95% CI (Δd)"].strip("[]").split(",")]
            ax.text(0.285, y, f"{dec(num(r['Δd']), lang)} [{dec(lo, lang)}; {dec(hi, lang)}]", va="center", fontsize=11.5,
                    color=INK)
            ax.text(0.357, y, kl[r["Target domain X"]].replace("%", " %"), va="center", fontsize=11.5, color=INK)
        ax.text(0.285, len(mmd) - 0.35, t[1], fontsize=11.5, color=INK2, fontweight="bold")
        ax.text(0.357, len(mmd) - 0.35, t[2], fontsize=11.5, color=INK2, fontweight="bold")
        ax.set_yticks(range(len(mmd)), [r["Target domain X"] for r in mmd])
        ax.set_xlim(0.09, 0.28)
        ax.set_ylim(-0.6, len(mmd) - 0.1)
        ax.set_xlabel(t[0])
        clean(ax, left=False)
        ax.tick_params(labelleft=True)
        ax.xaxis.grid(True, color="#e6e5e1")
        ax.set_xticks([0.10, 0.15, 0.20, 0.25])
        commas(ax, lang, 2, "x")
        ax.legend(frameon=False, loc="lower left", fontsize=11, ncol=2, bbox_to_anchor=(0, -0.32))
        fig.subplots_adjust(left=0.12, right=0.6, top=0.95, bottom=0.25)
        save(fig, HERE / f"domain_{lang}.png")


if __name__ == "__main__":
    main()
