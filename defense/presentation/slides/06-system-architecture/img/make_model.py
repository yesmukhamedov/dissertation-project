"""Slide 06: the model as a composition — 𝒫 (eight stages) → CNN with a 4-channel first layer → softmax → grade;
Grad-CAM → ALO; two eyes → one patient-level decision, kk/ru/en.

Content: thesis ch. 2 and the slide's formulation block; the 4-channel conv1 of both backbones comes from the archived
a08_2 (slide 07), which this figure absorbs. Replaces a07_1 (English, tall, unreadable) and a08_2.
The rule that merges the two eyes is not named here — TODO.md §3 (check demo/server before naming it).
𝒫 is drawn with mathtext ($\\mathcal{P}$): DejaVu Sans has no glyph for U+1D4AB.
Run: python make_model.py  ->  model_<lang>.png
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))
from figlib import BLUE, INK2, LANGS, arrow, box, save  # noqa: E402

P = r"$\mathcal{P}$"
X = r"$x \in \mathbb{R}^{4 \times 512 \times 512}$"
PIPE, CNN, OUT = "#e3f1ea", "#e4eefb", "#f7e7e1"
T = {"kk": {"in": "Көз түбі\nкескіні I,\nкөз жағы s", "p": f"Алдын ала\nөңдеу {P}\n8 кезең",
            "x": f"{X}\nRGB +\nкөру алаңының\nмаскасы", "cnn": "CNN$_\\theta$\nResNet-50 /\nEfficientNet-B3\n1-қабат — 4 арна",
            "sm": "softmax\nŷ ∈ {0, …, 4}", "ref": "ŷ ≥ 2 →\nдәрігерге жолдама", "pat": "Екі көз →\nпациент бойынша\nшешім",
            "cam": "Grad-CAM → ALO", "model": f"Модель = {P} + CNN: θ {P} шығысында оқытылады"},
     "ru": {"in": "Снимок\nглазного дна I,\nсторона глаза s", "p": f"Предобработка\n{P}\n8 этапов",
            "x": f"{X}\nRGB +\nмаска поля\nзрения", "cnn": "CNN$_\\theta$\nResNet-50 /\nEfficientNet-B3\n1-й слой — 4 канала",
            "sm": "softmax\nŷ ∈ {0, …, 4}", "ref": "ŷ ≥ 2 →\nнаправление к врачу", "pat": "Два глаза →\nрешение\nпо пациенту",
            "cam": "Grad-CAM → ALO", "model": f"Модель = {P} + CNN: θ обучается на выходе {P}"},
     "en": {"in": "Fundus\nimage I,\neye side s", "p": f"Preprocessing\n{P}\n8 stages",
            "x": f"{X}\nRGB +\nFOV mask", "cnn": "CNN$_\\theta$\nResNet-50 /\nEfficientNet-B3\n1st layer — 4 channels",
            "sm": "softmax\nŷ ∈ {0, …, 4}", "ref": "ŷ ≥ 2 →\nrefer to a doctor", "pat": "Two eyes →\npatient-level\ndecision",
            "cam": "Grad-CAM → ALO", "model": f"Model = {P} + CNN: θ is trained on the output of {P}"}}


def main() -> None:
    """Write model_{lang}.png."""
    for lang in LANGS:
        t = T[lang]
        fig, ax = plt.subplots(figsize=(14, 5.6))
        fig.subplots_adjust(0.005, 0.005, 0.995, 0.995)
        ax.set_xlim(-0.01, 1.01)
        ax.set_ylim(0, 1)
        ax.axis("off")
        ax.add_patch(plt.Rectangle((0.125, 0.37), 0.585, 0.52, fill=False, ec=BLUE, lw=1.8, ls=(0, (5, 3))))
        ax.text(0.4175, 0.915, t["model"], ha="center", fontsize=12.5, color=BLUE, fontweight="bold")
        y, h = 0.43, 0.4
        box(ax, 0.0, y, 0.105, h, t["in"], size=11)
        box(ax, 0.14, y, 0.15, h, t["p"], fc=PIPE, bold=True, size=12)
        box(ax, 0.32, y, 0.165, h, t["x"], size=11)
        box(ax, 0.515, y, 0.18, h, t["cnn"], fc=CNN, size=11, bold=True)
        box(ax, 0.735, y, 0.1, h, t["sm"], size=11)
        box(ax, 0.865, 0.66, 0.135, 0.22, t["ref"], fc=OUT, size=10.5)
        box(ax, 0.865, 0.36, 0.135, 0.24, t["pat"], fc=OUT, size=10.5)
        box(ax, 0.525, 0.04, 0.16, 0.14, t["cam"], fc=OUT, size=11.5)
        ym = y + h / 2
        for a, b in (((0.105, ym), (0.14, ym)), ((0.29, ym), (0.32, ym)), ((0.485, ym), (0.515, ym)),
                     ((0.695, ym), (0.735, ym)), ((0.835, ym + 0.05), (0.865, 0.76)), ((0.835, ym - 0.05), (0.865, 0.48)),
                     ((0.605, y), (0.605, 0.18))):
            arrow(ax, a, b)
        ax.text(0.615, 0.26, r"$\partial \hat{y} / \partial A$", fontsize=11, color=INK2)
        save(fig, HERE / f"model_{lang}.png")


if __name__ == "__main__":
    main()
