# -*- coding: utf-8 -*-
"""Redraw the schematic manuscript figures as vector PDF + print-resolution PNG.

Only figures whose content is fully specified by the manuscript text are regenerated
here (Fig. 1 pipeline flowchart, Fig. 3 network architecture). Figures carrying measured
data or photographs are NOT regenerated - see figures_hires/README.md.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle

OUT = Path(r"D:\dissertation-project\defense\manuscript\figures_hires")
OUT.mkdir(exist_ok=True)

MM = 1 / 25.4
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "svg.fonttype": "none",
})

EDGE = "#3C3C3C"
BLUE, GREEN, ORANGE, PURPLE = "#D6E5F5", "#D3EAD8", "#FBE0C8", "#E7D8F0"


def save(fig, name, dpi):
    fig.savefig(OUT / f"{name}.pdf", format="pdf", bbox_inches="tight", pad_inches=0.02)
    fig.savefig(OUT / f"{name}.png", format="png", dpi=dpi, bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)


# ----------------------------------------------------------------- Figure 1
def figure_1():
    """End-to-end system pipeline. Single-column width, 1000 dpi (line drawing)."""
    boxes = [
        (["Browse Left + Right Fundus"], BLUE),
        (["Preprocessing",
          "flip \u2192 OD\u2013fovea rotation \u2192 crop \u2192 mask",
          "\u2192 flat-field \u2192 polar CLAHE \u2192 normalize"], GREEN),
        (["EfficientNet-B3 / Config D"], GREEN),
        (["Per-eye softmax (5 classes)"], GREEN),
        (["Patient-level aggregation", "worst-eye rule"], GREEN),
        (["Result: DR grade + referable + confidence"], ORANGE),
        (["Grad-CAM + attention overlay"], ORANGE),
        (["Ophthalmologist review",
          "confirm / reject + corrected grade"], PURPLE),
    ]

    x0, x1 = 4, 96
    gap = 11.0          # vertical space between boxes
    base = 14.0         # height of a single-line box
    extra = 6.5         # added height per additional text line
    text_line = 5.4     # spacing between text lines inside a box
    heights = [base + extra * (len(lines) - 1) for lines, _ in boxes]
    total = sum(heights) + gap * (len(boxes) - 1)

    w_mm = 85
    h_mm = w_mm * total / 100
    fig = plt.figure(figsize=(w_mm * MM, h_mm * MM))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, total)
    ax.axis("off")
    y = total

    for i, ((lines, colour), h) in enumerate(zip(boxes, heights)):
        top, bottom = y, y - h
        ax.add_patch(FancyBboxPatch(
            (x0, bottom), x1 - x0, h,
            boxstyle="round,pad=0,rounding_size=2.2",
            linewidth=0.9, edgecolor=EDGE, facecolor=colour, mutation_aspect=1))
        cy = (top + bottom) / 2
        first = len(lines) > 1
        for j, line in enumerate(lines):
            ly = cy + (len(lines) - 1) * text_line / 2 - j * text_line
            ax.text((x0 + x1) / 2, ly, line, ha="center", va="center",
                    fontsize=7.4 if (j == 0 and first) else 7.0,
                    color="#111111")
        if i < len(boxes) - 1:
            ny = bottom - gap
            ax.add_patch(FancyArrowPatch(
                ((x0 + x1) / 2, bottom), ((x0 + x1) / 2, ny + 0.15),
                arrowstyle="-|>", mutation_scale=7, linewidth=0.9,
                color="#4A4A4A", shrinkA=0, shrinkB=0))
        y = bottom - gap

    save(fig, "Figure_1", 1100)
    return w_mm


# ----------------------------------------------------------------- Figure 3
def figure_3():
    """EfficientNet-B3 backbone. Full page width, 1000 dpi (line drawing)."""
    w_mm, h_mm = 190, 62
    fig = plt.figure(figsize=(w_mm * MM, h_mm * MM))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    stem_c, mb_c, head_c, tail_c = "#8FB3D9", "#8CC79B", "#E08A76", "#C3A5DA"
    # name, sub-label, relative height, relative width, colour
    blocks = [
        ("Input",     "512\u00d7512\u00d74", 1.00, 1.00, stem_c),
        ("Stem",      "conv 3\u00d73 s2",     0.93, 1.00, stem_c),
        ("MBConv1",   "256\u00d7256, 24",     0.86, 1.15, mb_c),
        ("MBConv2",   "128\u00d7128, 32",     0.75, 1.30, mb_c),
        ("MBConv3",   "64\u00d764, 48",       0.66, 1.45, mb_c),
        ("MBConv4",   "32\u00d732, 96",       0.58, 1.60, mb_c),
        ("MBConv5",   "16\u00d716, 136",      0.50, 1.75, mb_c),
        ("MBConv6",   "8\u00d78, 232",        0.44, 1.90, mb_c),
        ("MBConv7",   "8\u00d78, 384",        0.40, 2.05, mb_c),
        ("1\u00d71 conv", "8\u00d78, 1536",   0.36, 2.20, head_c),
        ("GAP",       "1\u00d71\u00d71536",   0.18, 1.20, tail_c),
    ]

    base_h, base_w = 46.0, 2.6
    depth_x, depth_y = 1.9, 2.6
    gapx = 1.7
    baseline = 34.0
    x = 3.0
    for name, sub, hh, ww, colour in blocks:
        h = base_h * hh
        w = base_w * ww
        # front face
        ax.add_patch(Rectangle((x, baseline), w, h, linewidth=0.7,
                               edgecolor=EDGE, facecolor=colour, zorder=3))
        # top face
        ax.add_patch(Polygon([(x, baseline + h), (x + depth_x, baseline + h + depth_y),
                              (x + w + depth_x, baseline + h + depth_y), (x + w, baseline + h)],
                             closed=True, linewidth=0.7, edgecolor=EDGE,
                             facecolor=colour, alpha=0.72, zorder=2))
        # right face
        ax.add_patch(Polygon([(x + w, baseline), (x + w + depth_x, baseline + depth_y),
                              (x + w + depth_x, baseline + h + depth_y), (x + w, baseline + h)],
                             closed=True, linewidth=0.7, edgecolor=EDGE,
                             facecolor=colour, alpha=0.55, zorder=2))
        ax.text(x + w / 2 + depth_x / 2, baseline + h + depth_y + 2.4, name,
                ha="center", va="bottom", fontsize=6.2, color="#111111")
        ax.text(x + w / 2 + depth_x / 2, baseline - 2.6, sub,
                ha="center", va="top", fontsize=5.2, color="#333333")
        x_next = x + w + depth_x + gapx
        ax.add_patch(FancyArrowPatch((x + w + depth_x, baseline + h / 2),
                                     (x_next - 0.25, baseline + h / 2),
                                     arrowstyle="-|>", mutation_scale=5.5,
                                     linewidth=0.7, color="#4A4A4A",
                                     shrinkA=0, shrinkB=0, zorder=4))
        x = x_next

    for label, sub in (("FC", "5 logits"), ("softmax", "DR 0\u20134")):
        ax.text(x + 3.0, baseline + 10.0, label, ha="center", va="bottom",
                fontsize=6.2, color="#111111")
        ax.text(x + 3.0, baseline + 4.0, sub, ha="center", va="top",
                fontsize=5.2, color="#333333")
        ax.add_patch(FancyArrowPatch((x + 6.2, baseline + 8.0), (x + 8.6, baseline + 8.0),
                                     arrowstyle="-|>", mutation_scale=5.5, linewidth=0.7,
                                     color="#4A4A4A", shrinkA=0, shrinkB=0))
        x += 9.0

    legend = [(stem_c, "input / stem"), (mb_c, "MBConv stages 1\u20137"),
              (head_c, "1\u00d71 head conv (1,536)"), (tail_c, "GAP / FC / softmax")]
    widths = [4.0 + len(t) * 0.78 + 5.0 for _, t in legend]
    lx = (100 - sum(widths)) / 2
    for (colour, text), wgt in zip(legend, widths):
        ax.add_patch(Rectangle((lx, 6.0), 2.8, 3.2, linewidth=0.7,
                               edgecolor=EDGE, facecolor=colour))
        ax.text(lx + 3.8, 7.6, text, ha="left", va="center", fontsize=5.6, color="#111111")
        lx += wgt

    save(fig, "Figure_3", 1000)
    return w_mm


w1 = figure_1()
w3 = figure_3()

from PIL import Image
for n, wmm in (("Figure_1", w1), ("Figure_3", w3)):
    im = Image.open(OUT / f"{n}.png")
    size_kb = (OUT / f"{n}.png").stat().st_size // 1024
    pdf_kb = (OUT / f"{n}.pdf").stat().st_size // 1024
    print(f"{n}: PNG {im.size[0]}x{im.size[1]} px ({size_kb} KB) at {wmm} mm wide "
          f"-> {im.size[0] / (wmm / 25.4):.0f} dpi | PDF vector {pdf_kb} KB")
