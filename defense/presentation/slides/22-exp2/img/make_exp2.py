"""Slide 22: experiment 2 — cumulative ablation as a waterfall, and the optima of CLAHE and flat-field, kk/ru/en.

Numbers: results/tables/TAB-4.4_exp2_ablation.md (L0 … L7 weighted F1), exp2_clahe_sweep.md (weighted-F1 grid,
clip factor × global threshold) and exp2_flatfield_sigma_sweep.md (σ / D grid). Replaces a25_1 (cumulative, old run),
a25_2 (marginal — the differences of the same bars) and a25_3 (per-grade heatmaps, unreadable at slide size).
Run: python make_exp2.py  ->  exp2_<lang>.png
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))
from figlib import ACCENT, BLUE, GRAY, INK, INK2, LANGS, WF1, clean, dec, md_table, num, save  # noqa: E402

STEPS = {"kk": ["базалық\nдеңгей", "+0\nайналдыру", "+1\nбұру", "+2–3\nкесу,\nмаска", "+4\nжарықты\nтүзету",
                "+5\nCLAHE", "+6\nаугм.", "+7\nнормалау"],
         "ru": ["базовая\nточка", "+0\nотражение", "+1\nповорот", "+2–3\nобрезка,\nмаска", "+4\nкоррекция\nосвещ.",
                "+5\nCLAHE", "+6\nаугм.", "+7\nнормализ."],
         "en": ["baseline\nlevel", "+0\nflip", "+1\nrotation", "+2–3\ncrop, mask", "+4 flat-\nfield", "+5\nCLAHE",
                "+6\naugm.", "+7\nnormalise"]}
T = {"kk": ("Кезеңдерді кезекпен қосу", "CLAHE: клип-фактор × шек", "Жарықтандыруды түзету: σ / D", "клип-фактор",
            "шек", "п.п."),
     "ru": ("Этапы добавляются по очереди", "CLAHE: клип-фактор × порог", "Коррекция освещённости: σ / D", "клип-фактор",
            "порог", "п.п."),
     "en": ("Stages added one at a time", "CLAHE: clip factor × threshold", "Flat-field: σ / D", "clip factor",
            "threshold", "pp")}


def main() -> None:
    """Write exp2_{lang}.png: waterfall (left), CLAHE grid and σ sweep (right)."""
    lv = [num(r["Weighted F1"]) for r in md_table("TAB-4.4_exp2_ablation.md", "Level")]
    grid_rows = md_table("exp2_clahe_sweep.md", "clip_factor \\ global_threshold")
    thr = [c for c in grid_rows[0] if c != "clip_factor \\ global_threshold"]
    clip = [num(r["clip_factor \\ global_threshold"]) for r in grid_rows]
    grid = np.array([[num(r[t]) for t in thr] for r in grid_rows])
    sig = md_table("exp2_flatfield_sigma_sweep.md", "σ / D_FOV")
    s_x, s_y = [num(r["σ / D_FOV"]) for r in sig], [num(r["Weighted F1"]) for r in sig]
    for lang in LANGS:
        t = T[lang]
        fig = plt.figure(figsize=(15, 5.4))
        ax = fig.add_axes([0.06, 0.2, 0.52, 0.68])
        x = np.arange(len(lv))
        ax.plot([-0.31, 0.31], [lv[0]] * 2, color=GRAY, lw=6, solid_capstyle="butt")
        for i in range(1, len(lv)):
            big = i in (4, 5)
            ax.bar(i, lv[i] - lv[i - 1], 0.62, bottom=lv[i - 1], color=BLUE if big else "#8fb8ea")
            ax.plot([i - 1 + 0.31, i - 0.31], [lv[i - 1]] * 2, color=INK2, lw=0.8)
            ax.text(i, lv[i] + 0.002, f"+{dec((lv[i] - lv[i - 1]) * 100, lang, 1)}", ha="center", fontsize=11,
                    color=INK, fontweight="bold" if big else "normal")
        ax.text(0, lv[0] + 0.003, dec(lv[0], lang), ha="center", fontsize=11, color=INK)
        ax.text(len(lv) - 1, lv[-1] + 0.009, dec(lv[-1], lang), ha="center", fontsize=12, color=BLUE, fontweight="bold")
        ax.set_xticks(x, STEPS[lang], fontsize=9.5)
        ax.set_ylim(0.74, 0.835)
        ax.set_ylabel(WF1[lang])
        ax.set_title(t[0] + f"  (Δ, {t[5]})", fontsize=13, color=INK)
        clean(ax)
        h = fig.add_axes([0.66, 0.53, 0.3, 0.36])
        h.imshow(grid, cmap="Blues", aspect="auto")
        i, j = np.unravel_index(grid.argmax(), grid.shape)
        h.plot(j, i, marker="*", ms=16, color=ACCENT, mec="white")
        h.set_xticks(range(len(thr)), [dec(float(v), lang, 2) for v in thr], fontsize=10)
        h.set_yticks(range(0, len(clip), 2), [dec(clip[k], lang, 1) for k in range(0, len(clip), 2)], fontsize=10)
        h.set_xlabel(t[4], fontsize=11)
        h.set_ylabel(t[3], fontsize=11)
        h.set_title(t[1] + f": ★ {dec(clip[i], lang, 1)} / {dec(float(thr[j]), lang, 2)}", fontsize=12, color=INK)
        s = fig.add_axes([0.66, 0.12, 0.3, 0.24])
        s.plot(s_x, s_y, color=BLUE, lw=2, marker="o", ms=6)
        k = int(np.argmax(s_y))
        s.plot(s_x[k], s_y[k], marker="*", ms=16, color=ACCENT, mec="white")
        s.set_xticks(s_x, [dec(v, lang, 2) for v in s_x], fontsize=10)
        s.tick_params(labelsize=10)
        s.set_title(t[2] + f": ★ {dec(s_x[k], lang, 2)}", fontsize=12, color=INK)
        clean(s)
        if lang != "en":
            s.yaxis.set_major_formatter(lambda v, _: f"{v:.2f}".replace(".", ","))
            ax.yaxis.set_major_formatter(lambda v, _: f"{v:.2f}".replace(".", ","))
        save(fig, HERE / f"exp2_{lang}.png")


if __name__ == "__main__":
    main()
