#!/usr/bin/env python3
"""Re-render the Stage-6 augmentation card (FIG-3.8) from the source SVG.

Why this exists: the shipped `stage6_augmentation.png` copies still depicted the
PCA colour jitter that Stage 6 dropped on 2026-06-26 in favour of ColorJitter +
Gaussian noise + JPEG compression, and also listed a "horizontal re-flip" step
that the implementation does not perform. The source SVG had already been
re-specified; only the renders lagged.

This is a narrowed sibling of `split_preprocessing_svg.py` (which does all eight
stages, and whose paths still point at the retired E: drive). It extracts the
Stage-6 group, wraps it in a standalone SVG with the sheet's own <defs>/styles,
renders via headless Chrome, and writes the PNG over every copy on disk so they
cannot drift apart again.

Run: python render_stage6_card.py
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SRC_SVG = ROOT / "demo/web/public/diagrams/03_preprocessing_stages_detailed.svg"
TARGET_GLOB = "defense/presentation/assets/preprocessing/*/stage6_augmentation.png"
CHROME = Path(r"C:/Program Files/Google/Chrome/Application/chrome.exe")

STAGE_X, STAGE_Y = 940, 590
PANEL_W, PANEL_H = 440, 500
PAD = 24
PAD_BOTTOM_EXTRA = 40  # Chrome loses a few px of the window to its own frame
CARD_W = PANEL_W + 2 * PAD
CARD_H = PANEL_H + 2 * PAD + PAD_BOTTOM_EXTRA
RENDER_SCALE = 3


def extract_stage6(text: str) -> str:
    """Return the Stage-6 <g …> block, matched by its translate() origin."""
    start = text.find(f'<g transform="translate({STAGE_X}, {STAGE_Y})">')
    if start < 0:
        raise SystemExit("stage-6 group not found")
    depth, i = 0, start
    while i < len(text):
        if text.startswith("<g", i):
            depth += 1
        elif text.startswith("</g>", i):
            depth -= 1
            if depth == 0:
                return text[start : i + 4]
        i += 1
    raise SystemExit("unbalanced <g> around stage 6")


def main() -> None:
    if not CHROME.exists():
        raise SystemExit(f"headless Chrome not found at {CHROME}")
    svg = SRC_SVG.read_text(encoding="utf-8")

    defs = "".join(re.findall(r"<defs>.*?</defs>", svg, re.S))
    styles = "".join(re.findall(r"<style[^>]*>.*?</style>", svg, re.S))
    block = extract_stage6(svg)
    # Re-origin the panel at the card's padding instead of its sheet position.
    block = block.replace(f'translate({STAGE_X}, {STAGE_Y})', f"translate({PAD}, {PAD})", 1)

    standalone = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{CARD_W}" height="{CARD_H}" '
        f'viewBox="0 0 {CARD_W} {CARD_H}">{defs}{styles}'
        f'<rect width="100%" height="100%" fill="#ffffff"/>{block}</svg>'
    )

    tmp = Path(tempfile.mkdtemp(prefix="stage6_"))
    try:
        (tmp / "card.svg").write_text(standalone, encoding="utf-8")
        out = tmp / "card.png"
        subprocess.run(
            [str(CHROME), "--headless", "--disable-gpu", "--hide-scrollbars",
             f"--force-device-scale-factor={RENDER_SCALE}",
             f"--window-size={CARD_W},{CARD_H}",
             f"--screenshot={out}", (tmp / "card.svg").as_uri()],
            check=True, capture_output=True,
        )
        if not out.exists():
            raise SystemExit("Chrome produced no screenshot")
        targets = sorted(ROOT.glob(TARGET_GLOB))
        if not targets:
            raise SystemExit(f"no targets matched {TARGET_GLOB}")
        for t in targets:
            shutil.copyfile(out, t)
            print(f"WROTE {t.relative_to(ROOT)}")
        print(f"\n{len(targets)} copies updated from {SRC_SVG.name}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
