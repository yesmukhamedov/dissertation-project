"""Charts for slide 02 (relevance), kk/ru/en. Data and sources: ../analysis.md, section «Числа».

Run: python make_charts.py  -> chart1_<lang>.png, chart2_<lang>.png next to this file.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
BLUE, GRAY, INK, INK2, SURFACE = "#2a78d6", "#b9b8b3", "#0b0b0b", "#52514e", "#ffffff"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 13, "axes.edgecolor": INK2})

# Ministry of Health RK via baq.kz, 13.12.2024 — registered diabetes patients, thousands (2024 = 9 months)
YEARS = list(range(2014, 2025))
KZ_DM = [261.1, 272.6, 293.0, 311.4, 329.4, 367.8, 377.3, 406.2, 425.4, 467.3, 516.7]

T = {
    "kk": {"c1": "Қазақстандағы есепте тұрған қант диабеті\nнауқастары, мың адам", "n": "2024 — 9 ай",
           "c2": "Ауылдағы үлес, %", "pop": "Халық", "oph": "Офтальмологтар"},
    "ru": {"c1": "Больные сахарным диабетом на учёте\nв Казахстане, тыс. человек", "n": "2024 — 9 мес.",
           "c2": "Доля на селе, %", "pop": "Население", "oph": "Офтальмологи"},
    "en": {"c1": "Registered diabetes patients\nin Kazakhstan, thousands", "n": "2024: 9 months",
           "c2": "Rural share, %", "pop": "Population", "oph": "Ophthalmologists"},
}


def clean(ax) -> None:
    """Recessive axes: no top/right spines, no y-axis, light baseline."""
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.tick_params(left=False, labelleft=False, colors=INK2)


def chart1(lang: str) -> None:
    """Bar chart of the registered-patient series with direct labels on the ends."""
    t = T[lang]
    fig, ax = plt.subplots(figsize=(6.4, 3.8), dpi=200, facecolor=SURFACE)
    bars = ax.bar(YEARS, KZ_DM, color=BLUE, width=0.72)
    for i in (0, len(YEARS) - 1):
        ax.text(YEARS[i], KZ_DM[i] + 8, f"{KZ_DM[i]:.0f}", ha="center", va="bottom", color=INK, fontweight="bold")
    ax.set_xticks(YEARS[::2] + [2024])
    ax.set_ylim(0, 600)
    ax.set_title(t["c1"], loc="left", color=INK, fontsize=13)
    ax.text(1.0, -0.16, t["n"], transform=ax.transAxes, ha="right", color=INK2, fontsize=10)
    clean(ax)
    fig.tight_layout()
    fig.savefig(HERE / f"chart1_{lang}.png", facecolor=SURFACE)
    plt.close(fig)


def chart2(lang: str) -> None:
    """Two horizontal bars: rural share of population vs of ophthalmologists."""
    t = T[lang]
    fig, ax = plt.subplots(figsize=(6.4, 2.6), dpi=200, facecolor=SURFACE)
    labels, vals, cols = [t["oph"], t["pop"]], [20, 36], [BLUE, GRAY]
    ax.barh(labels, vals, color=cols, height=0.55)
    for y, v in enumerate(vals):
        ax.text(v + 1, y, f"{v} %", va="center", color=INK, fontweight="bold")
    ax.set_xlim(0, 45)
    ax.set_title(t["c2"], loc="left", color=INK, fontsize=13)
    for s in ("top", "right", "bottom"):
        ax.spines[s].set_visible(False)
    ax.tick_params(bottom=False, labelbottom=False, left=False, colors=INK)
    fig.tight_layout()
    fig.savefig(HERE / f"chart2_{lang}.png", facecolor=SURFACE)
    plt.close(fig)


if __name__ == "__main__":
    for lang in T:
        chart1(lang)
        chart2(lang)
