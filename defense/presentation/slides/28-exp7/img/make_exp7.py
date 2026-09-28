"""Slide 28: experiment 7 — training on IDRiD (n = 516): internal 5-fold CV and the Kazakhstani hold-out (n = 60), kk/ru/en.

Numbers: results/tables/TAB-4.10_exp7_smalldata.md (IDRiD CV wF1 mean ± SD; clinical hold-out wF1 ± SD and the paired Δ
with 95 % CI — the paired CI is the one to cite, see the table's note). Replaces a30_1 (old run: 0.608 / AUC 0.812).
Run: python make_exp7.py  ->  exp7_<lang>.png
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))
from figlib import ARM, BLUE, GRAY, INK, INK2, LANGS, WF1, clean, commas, dec, md_table, num, save  # noqa: E402

T = {"kk": ("IDRiD, 5 фолд\n(n = 516)", "Қазақстандық клиникалық\nіріктеме (n = 60)", "жұптасқан 95 % СА"),
     "ru": ("IDRiD, 5 фолдов\n(n = 516)", "Казахстанская клиническая\nвыборка (n = 60)", "парный 95 % ДИ"),
     "en": ("IDRiD, 5 folds\n(n = 516)", "Kazakhstani clinical\nhold-out (n = 60)", "paired 95 % CI")}


def main() -> None:
    """Write exp7_{lang}.png."""
    cv = md_table("TAB-4.10_exp7_smalldata.md", "Arm", 2)
    ho = md_table("TAB-4.10_exp7_smalldata.md", "Arm", 0)
    dl = [r for r in md_table("TAB-4.10_exp7_smalldata.md", "Metric") if r["Metric"] == "wF1"][0]
    groups = [[(num(r["wF1"]), num(r["wF1"].split("±")[1])) for r in cv],
              [(num(r["Weighted F1"]), num(r["Weighted F1"].split("±")[1])) for r in ho]]
    for lang in LANGS:
        t = T[lang]
        fig, ax = plt.subplots(figsize=(8.5, 4.9))
        for g, vals in enumerate(groups):
            for k, (m, sd) in enumerate(vals):
                x = g + (k - 0.5) * 0.38
                ax.bar(x, m, 0.34, color=(GRAY, BLUE)[k], label=ARM[lang][k] if g == 0 else None)
                ax.errorbar(x, m, sd, color=INK2, capsize=4, lw=1.2)
                ax.text(x, m + sd + 0.015, dec(m, lang), ha="center", fontsize=12, color=INK)
        lo, hi = [num(v) for v in dl["95% CI (Δ)"].strip("[]").split(",")]
        ax.text(1, 0.8, f"Δ = +{dec(num(dl['Δ (D − C)']), lang)}\n{t[2]} [{dec(lo, lang)}; {dec(hi, lang)}]", ha="center",
                fontsize=11.5, color=BLUE)
        ax.set_xticks([0, 1], t[:2])
        ax.set_ylim(0, 0.95)
        ax.set_ylabel(WF1[lang])
        ax.legend(frameon=False, loc="upper left", fontsize=11)
        clean(ax)
        commas(ax, lang)
        fig.tight_layout()
        save(fig, HERE / f"exp7_{lang}.png")


if __name__ == "__main__":
    main()
