"""Slide 09: fundus-camera brands in Central Asian clinics vs in the training corpora — two donuts, kk/ru/en.

Counts: the archived slide script defense/_archive/presentation_2026-09-26/scripts/generate_camera_alignment.py
(CA_DATA — primary brand of 36 clinics from demo/web/public/camera/central_asia.md; DS_DATA — brand mentions over the
corpora). central_asia.md itself says most clinics do not publish the model and part of the rows give the most typical
brand — hence the source note under the figure. Replaces a11_1 (country bars unreadable, «H-6 негіздемесі» label).
Run: python make_cameras.py  ->  cameras_<lang>.png
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))
from figlib import INK, INK2, LANGS, save  # noqa: E402

CLINICS = {"Topcon": 19, "Canon": 11, "Zeiss": 5, "Other": 1}
CORPORA = {"Topcon": 4, "Canon": 4, "Zeiss": 1, "Kowa": 2}
COL = {"Topcon": "#7a5bd6", "Canon": "#2a78d6", "Zeiss": "#d0603a", "Kowa": "#2e9e6b", "Other": "#b9b8b3"}
T = {"kk": ("Орталық Азия клиникалары", "клиника", "Оқыту корпустары", "бренд атауы", "басқа",
            "Клиникалар: сайттар мен жабдық жеткізушілерінің деректері, бір бөлігі — ең тән бренд (central_asia.md)"),
     "ru": ("Клиники Центральной Азии", "клиник", "Обучающие корпуса", "упоминаний бренда", "другие",
            "Клиники: данные сайтов и поставщиков оборудования, часть строк — наиболее типичный бренд (central_asia.md)"),
     "en": ("Central Asian clinics", "clinics", "Training corpora", "brand mentions", "other",
            "Clinics: clinic websites and equipment suppliers; some rows give the most typical brand (central_asia.md)")}


def donut(ax, data: dict, title: str, unit: str, other: str) -> None:
    """One donut with brand labels outside, percentages inside and the total in the centre."""
    names = list(data)
    vals = list(data.values())
    wedges, _, pct = ax.pie(vals, colors=[COL[n] for n in names], startangle=90, counterclock=False,
                            labels=[other if n == "Other" else n for n in names], labeldistance=1.12,
                            autopct=lambda p: f"{p:.0f} %" if p >= 8 else "", pctdistance=0.78,
                            wedgeprops=dict(width=0.42, edgecolor="white", linewidth=2),
                            textprops=dict(fontsize=13, color=INK))
    for p in pct:
        p.set_color("white")
        p.set_fontweight("bold")
        p.set_fontsize(12)
    ax.text(0, 0.08, str(sum(vals)), ha="center", va="center", fontsize=26, fontweight="bold", color=INK)
    ax.text(0, -0.2, unit, ha="center", va="center", fontsize=11, color=INK2)
    ax.set_title(title, fontsize=14, color=INK, pad=14)


def main() -> None:
    """Write cameras_{lang}.png."""
    for lang in LANGS:
        t = T[lang]
        fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 5.2))
        donut(a1, CLINICS, t[0], t[1], t[4])
        donut(a2, CORPORA, t[2], t[3], t[4])
        fig.text(0.5, 0.03, t[5], ha="center", fontsize=10, color=INK2, style="italic")
        fig.subplots_adjust(left=0.04, right=0.96, top=0.88, bottom=0.08, wspace=0.35)
        save(fig, HERE / f"cameras_{lang}.png")


if __name__ == "__main__":
    main()
