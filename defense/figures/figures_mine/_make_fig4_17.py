#!/usr/bin/env python3
"""FIG-4.17  §4.4.2  Domain-distance reduction across the six target domains.

Discharges the last `ASSET TO BE CREATED` in the manuscript. Three panels, one
per claim the section actually makes:

  (a) MMD over penultimate-layer features, baseline arm vs integrated arm, as a
      paired dumbbell -- carries both the level and the reduction, and shows
      that the ordering of the domains survives preprocessing.
  (b) The reduction itself with its 95 % bootstrap interval against MCID_d = 0
      -- the panel that carries the verdict, since PASS_S requires the interval
      to exclude zero.
  (c) The pixel-level KL reduction as a percentage, against the 34-38 % band --
      the panel that carries the *proportional compression* reading.

Values are parsed from `results/tables/H-3_domain_distance.md`, the single
source of truth, rather than transcribed, so the figure cannot drift from the
table printed above it in the text.

Deliberately NOT drawn here: any pairing of distance reduction with transfer
gain. The correspondence is weak (Spearman rho ~ 0.49) and the section states
the result as direction only; a scatter of the two would invite exactly the
magnitude reading the text forecloses.

Style: serif, print-first, grayscale-legible (marker shape carries the arm as
well as colour). Run: python _make_fig4_17.py
"""
from __future__ import annotations

import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    "font.size": 10,
    "axes.linewidth": 0.8,
    "savefig.dpi": 200,
})

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SRC = ROOT / "results/tables/H-3_domain_distance.md"
OUT = HERE / "fig4_17_domain_distance.png"

INK = "#1a1a1a"
MUTED = "#6b6b6b"
GRID = "#dcdcdc"
# House accents nudged just past the chroma floor: the thesis pair (#37618e,
# #8c4a3b) reads as gray under validation. Separation is comfortable in both
# normal vision and simulated CVD.
BASE_C = "#2f639b"
INT_C = "#9c4a34"


def parse() -> tuple[list[dict], list[dict]]:
    """Return (mmd_rows, kl_rows) from the results table."""
    text = SRC.read_text(encoding="utf-8")

    def rows_after(heading: str) -> list[list[str]]:
        i = text.index(heading)
        block = text[i : text.index("\n## ", i + 1) if "\n## " in text[i + 1 :] else len(text)]
        out = []
        for ln in block.split("\n"):
            ln = ln.strip()
            if not ln.startswith("|") or set(ln) <= set("|-: "):
                continue
            cells = [c.strip() for c in ln.strip("|").split("|")]
            if cells and cells[0] not in ("Target domain X",) and not cells[0].startswith("---"):
                out.append(cells)
        return out

    mmd = []
    for c in rows_after("## MMD over penultimate-layer features"):
        lo, hi = re.findall(r"[+-]?\d*\.\d+", c[4])
        mmd.append({"domain": c[0], "base": float(c[1]), "int": float(c[2]),
                    "delta": float(c[3]), "lo": float(lo), "hi": float(hi)})

    kl = []
    for c in rows_after("## KL over per-channel histograms"):
        kl.append({"domain": c[0], "base": float(c[1]), "int": float(c[2]),
                   "red": abs(float(re.findall(r"-?\d+", c[3])[0]))})

    if len(mmd) != 6 or len(kl) != 6:
        raise SystemExit(f"expected 6 rows per measure, parsed {len(mmd)}/{len(kl)}")
    return mmd, kl


def main() -> None:
    mmd, kl = parse()

    # One shared vertical order for all three panels, so a row means the same
    # domain everywhere: baseline MMD remoteness, most distant at the top.
    order = sorted(mmd, key=lambda r: r["base"])
    names = [r["domain"] for r in order]
    y = list(range(len(names)))
    klmap = {r["domain"]: r for r in kl}

    fig, axes = plt.subplots(1, 3, figsize=(12.6, 4.2), sharey=True,
                             gridspec_kw={"width_ratios": [1.15, 1.0, 1.0], "wspace": 0.18})
    ax_a, ax_b, ax_c = axes

    # ---- (a) MMD, baseline vs integrated -------------------------------
    for yi, r in zip(y, order):
        ax_a.plot([r["int"], r["base"]], [yi, yi], color=MUTED, lw=1.1, zorder=1,
                  solid_capstyle="round")
        ax_a.plot(r["base"], yi, "o", ms=7, color=BASE_C, zorder=3,
                  mec="white", mew=1.0)
        ax_a.plot(r["int"], yi, "s", ms=6.5, color=INT_C, zorder=3,
                  mec="white", mew=1.0)
    ax_a.set_xlabel("MMD to the source domain (lower = closer)")
    ax_a.set_title("(a)  Representational distance", fontsize=10.5, loc="left", color=INK)
    ax_a.set_xlim(0.08, 0.29)
    ax_a.legend(handles=[
        Line2D([], [], marker="o", ls="", ms=7, color=BASE_C, mec="white", label="baseline arm"),
        Line2D([], [], marker="s", ls="", ms=6.5, color=INT_C, mec="white", label="integrated arm"),
    ], loc="lower right", frameon=False, fontsize=9, handletextpad=0.4)

    # ---- (b) reduction with 95 % interval ------------------------------
    for yi, r in zip(y, order):
        ax_b.plot([r["lo"], r["hi"]], [yi, yi], color=MUTED, lw=1.6, zorder=2,
                  solid_capstyle="round")
        ax_b.plot(r["delta"], yi, "D", ms=6, color=INT_C, zorder=3, mec="white", mew=1.0)
    ax_b.axvline(0.0, color=INK, lw=1.0, ls="--", zorder=1)
    ax_b.text(0.004, -0.85, "MCID$_d$ = 0", fontsize=9, color=INK,
              ha="left", va="center")
    ax_b.set_xlabel(r"$\Delta d$ with 95 % interval")
    ax_b.set_title("(b)  Reduction, against the criterion", fontsize=10.5, loc="left", color=INK)
    ax_b.set_xlim(-0.012, 0.14)

    # ---- (c) KL reduction against the band -----------------------------
    reds = [klmap[n]["red"] for n in names]
    lo_b, hi_b = min(reds), max(reds)
    ax_c.axvspan(lo_b, hi_b, color=INT_C, alpha=0.10, zorder=0, lw=0)
    for yi, n in zip(y, names):
        ax_c.plot(klmap[n]["red"], yi, "s", ms=6.5, color=INT_C, zorder=3,
                  mec="white", mew=1.0)
    ax_c.set_xlabel("pixel-level KL divergence, reduction (%)")
    ax_c.set_title("(c)  Proportional compression", fontsize=10.5, loc="left", color=INK)
    ax_c.set_xlim(0, 45)
    ax_c.text((lo_b + hi_b) / 2, -0.85, f"all six within {lo_b:.0f}–{hi_b:.0f} %",
              fontsize=9, color=INK, ha="center", va="center")

    for ax in axes:
        ax.set_yticks(y)
        ax.set_yticklabels(names)
        ax.set_ylim(-1.25, len(names) - 0.35)
        ax.grid(axis="x", color=GRID, lw=0.6, zorder=0)
        ax.set_axisbelow(True)
        ax.tick_params(colors=INK, labelsize=9.5)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        for s in ("left", "bottom"):
            ax.spines[s].set_color("#b5b5b5")

    fig.suptitle("Domain-distance reduction across the six target domains",
                 fontsize=12, color=INK, x=0.007, ha="left", y=0.985)
    fig.tight_layout(rect=(0, 0, 1, 0.945))
    fig.savefig(OUT, bbox_inches="tight", facecolor="white")
    print(f"WROTE {OUT}")
    print("order (most to least distant, baseline MMD):", ", ".join(reversed(names)))


if __name__ == "__main__":
    main()
