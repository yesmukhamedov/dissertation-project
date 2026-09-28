"""Shared style and paths for the slide figures (slides/NN-id/img/make_*.py), kk/ru/en.

One look for every figure: baseline arm — gray, integrated arm — blue (as on slide 02), recessive axes,
text in ink colours, no chart titles inside the image (the slide title says it). Numbers are never typed
here — each make_*.py reads or copies them from dissertation/results/ and names the table it used.
"""
from __future__ import annotations

import re
from pathlib import Path

import matplotlib
import numpy as np
from PIL import Image

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]                      # dissertation/
RESULTS = ROOT / "results" / "tables"
DEMO = ROOT / "demo" / "web" / "public" / "pipeline"
LANGS = ("kk", "ru", "en")

BLUE, GRAY, INK, INK2, GRID, SURFACE = "#2a78d6", "#b9b8b3", "#0b0b0b", "#52514e", "#e6e5e1", "#ffffff"
ACCENT = "#c8442a"                          # thresholds / reference lines only
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 13, "axes.edgecolor": INK2,
                     "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2})

# Common words, glossary/terms.csv spelling
ARM = {"kk": ("Базалық", "Интеграцияланған"), "ru": ("Базовая", "Интегрированная"), "en": ("Baseline", "Integrated")}
WF1 = {"kk": "Салмақталған F1", "ru": "Взвешенный F1", "en": "Weighted F1"}


def clean(ax, left: bool = True) -> None:
    """Recessive axes: no top/right spines, light horizontal grid behind the marks.

    Args:
        ax: Matplotlib axes.
        left: Keep the y axis (False hides it — values are direct-labelled).
    """
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_visible(left)
    ax.tick_params(left=left, labelleft=left)
    ax.set_axisbelow(True)
    if left:
        ax.yaxis.grid(True, color=GRID, lw=0.8)


def commas(ax, lang: str, nd: int = 1, axis: str = "y") -> None:
    """Decimal comma on the tick labels for kk/ru (en keeps the point).

    Args:
        ax: Matplotlib axes.
        lang: kk / ru / en.
        nd: Decimal places on the ticks.
        axis: "y", "x" or "xy".
    """
    if lang == "en":
        return
    f = lambda v, _: f"{v:.{nd}f}".replace(".", ",").replace("-", "−")  # noqa: E731
    for a in axis:
        getattr(ax, f"{a}axis").set_major_formatter(f)


def dec(x: float, lang: str, nd: int = 3) -> str:
    """Format a number with a decimal comma for kk/ru and a point for en.

    Args:
        x: Value.
        lang: kk / ru / en.
        nd: Decimal places.

    Returns:
        Formatted string.
    """
    s = f"{x:.{nd}f}"
    return s if lang == "en" else s.replace(".", ",")


def img(rel: str) -> np.ndarray:
    """Load a demo pipeline image (dr03) as an RGB array.

    Args:
        rel: Path under demo/web/public/pipeline/dr03/, e.g. "preprocessing/stage_4_flatfield/left.png".

    Returns:
        uint8 array (H, W, 3).
    """
    return np.asarray(Image.open(DEMO / "dr03" / rel).convert("RGB"))


def fov_crop(a: np.ndarray, thr: int = 20) -> np.ndarray:
    """Crop an image to the bounding square of its non-black (field-of-view) pixels.

    Args:
        a: uint8 RGB array.
        thr: Brightness threshold separating the fundus from the black border.

    Returns:
        Square crop centred on the field of view.
    """
    ys, xs = np.nonzero(a.max(axis=2) > thr)
    cy, cx = (ys.min() + ys.max()) // 2, (xs.min() + xs.max()) // 2
    r = max(ys.max() - ys.min(), xs.max() - xs.min()) // 2 + 2
    pad = np.pad(a, ((r, r), (r, r), (0, 0)))
    return pad[cy:cy + 2 * r, cx:cx + 2 * r]


def show(ax, a: np.ndarray, title: str | None = None, size: int = 12) -> None:
    """Draw an image without axes, with an optional caption above it.

    Args:
        ax: Matplotlib axes.
        a: Image array (RGB or 2-D).
        title: Caption.
        size: Caption font size.
    """
    ax.imshow(a, cmap="gray" if a.ndim == 2 else None)
    ax.axis("off")
    if title:
        ax.set_title(title, fontsize=size, color=INK)


def md_table(name: str, header: str, nth: int = 0) -> list[dict[str, str]]:
    """Read one markdown table from results/tables/<name> — the numbers are never retyped.

    Args:
        name: File name in results/tables.
        header: Exact text of the table's first header cell.
        nth: Which table with that first cell (0 = first).

    Returns:
        Rows as {column: cell}, markdown bold removed.
    """
    lines = (RESULTS / name).read_text(encoding="utf-8").splitlines()
    starts = [i for i, s in enumerate(lines) if s.startswith("|") and s.strip("| ").split("|")[0].strip() == header]
    i = starts[nth]
    cols = [c.strip().replace("**", "") for c in lines[i].strip().strip("|").split("|")]
    rows = []
    for s in lines[i + 2:]:
        if not s.startswith("|"):
            break
        cells = [c.strip().replace("**", "") for c in s.strip().strip("|").split("|")]
        rows.append(dict(zip(cols, cells)))
    return rows


def num(cell: str) -> float:
    """First number in a table cell ("0.8172 ± 0.0090" → 0.8172, "−34%" → -34).

    Args:
        cell: Table cell text.

    Returns:
        The value.
    """
    return float(re.search(r"[+\-−]?\d+(?:\.\d+)?", cell).group().replace("−", "-"))


def box(ax, x: float, y: float, w: float, h: float, text: str, fc: str = "#f4f3f0", ec: str = INK2,
        size: float = 12, bold: bool = False, ls: str = "solid") -> None:
    """A rounded block with centred text for the block diagrams (axes in 0…1 data units).

    Args:
        ax: Matplotlib axes with an equal-free 0…1 coordinate system.
        x, y: Lower-left corner.
        w, h: Width and height.
        text: Label (may contain line breaks).
        fc, ec: Fill and edge colours.
        size: Font size.
        bold: Bold label.
        ls: Edge line style.
    """
    from matplotlib.patches import FancyBboxPatch
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.004,rounding_size=0.012", fc=fc, ec=ec, lw=1.6, ls=ls))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size, color=INK,
            fontweight="bold" if bold else "normal", linespacing=1.3)


def arrow(ax, p0: tuple[float, float], p1: tuple[float, float], text: str | None = None, color: str = INK2) -> None:
    """An arrow between two points of a block diagram, with an optional label at its middle.

    Args:
        ax: Matplotlib axes.
        p0, p1: Start and end points.
        text: Label.
        color: Arrow colour.
    """
    ax.annotate("", xy=p1, xytext=p0, arrowprops=dict(arrowstyle="-|>", color=color, lw=1.6, mutation_scale=16))
    if text:
        ax.text((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2 + 0.03, text, ha="center", va="bottom", fontsize=10.5, color=INK2)


def save(fig, path: Path) -> None:
    """Write the figure at 200 dpi on a white surface and close it.

    Args:
        fig: Matplotlib figure.
        path: Output PNG path.
    """
    fig.savefig(path, dpi=200, facecolor=SURFACE)
    plt.close(fig)
    print("wrote", path.relative_to(HERE))
