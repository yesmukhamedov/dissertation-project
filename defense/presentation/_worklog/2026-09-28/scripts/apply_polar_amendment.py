"""Apply the Stage-5 polar-CLAHE amendment (accepted by the candidate 2026-09-28). Run from the repo root."""
from pathlib import Path

DATE = "2026-09-28"


def sub(path: str, old: str, new: str) -> None:
    p = Path(path)
    t = p.read_text(encoding="utf-8")
    assert t.count(old) == 1, (path, t.count(old), old[:60])
    p.write_text(t.replace(old, new), encoding="utf-8")


# --- INVARIANTS: OD-3 Stage 5 + header -------------------------------------------------------------
sub("thesis/governance/INVARIANTS.md",
    "- **Stage 5: CLAHE** — Dual-constraint clip limit on LAB L-channel: CL = min(clip_factor × tile_area / 256, "
    "global_threshold × tile_area). Tile grid 8×8. Stochastic at train time (p = 0.8); deterministic at inference. Always on.",
    "- **Stage 5: CLAHE** — Dual-constraint clip limit on the LAB L-channel: CL = min(clip_factor × cell_area / 256, "
    "global_threshold × cell_area), where a *cell* is a member of the partition of the field of view fixed by the selected "
    "grid geometry. Two geometries are defined. **Polar (default):** a fovea-centred polar partition — the pivot being the "
    "Stage-1 detected fovea when confident and the FOV-mask centroid otherwise — with log-spaced radial rings, angular "
    "sectors set by vessel density, and bilinear interpolation between neighbouring cells. **Rectilinear:** an 8×8 tile "
    "grid. The dual-constraint rule, the LAB L-channel, stochastic application at train time (p = 0.8) and deterministic "
    "application at inference are invariant across both. The clip factor and global threshold remain free "
    "hyperparameters fixed empirically. Always on.")
sub("thesis/governance/INVARIANTS.md",
    "**Version:** 7.1.0 | **Date:** 2026-08-20\n",
    f"**Version:** 7.2.0 | **Date:** {DATE}\n\n"
    "**v7.2.0 Amendment Summary (vs v7.1.0):** **OD-3 Stage 5 admits the polar CLAHE geometry and names it the "
    "default.** The clause fixed an 8×8 tile grid, while every run configuration in `experiments/configs/` sets "
    "`clahe_mode: polar` and `src/preprocessing/pipeline.py` applies `polar_clahe`; every reported result was produced "
    "with the polar geometry, so the binding definition described a transform that produced none of them. OD-3 was also "
    "internally inconsistent: its Stage 1 already pivots \"Stage-5 polar CLAHE\" on the FOV-mask centroid. The "
    "amendment makes the dual-constraint clip rule the invariant and the grid a selectable geometry — polar (default) or "
    "rectilinear 8×8 — with the LAB L-channel, stochastic training-time application (p = 0.8) and deterministic "
    "inference unchanged; the clip factor and global threshold stay free, as before. **Ratified by the candidate on "
    f"{DATE}** (proposal `records/AMENDMENT_PROPOSAL_stage5_polar_clahe.md`, raised 2026-08-12). **Admits a new "
    "operational variant; reverses no hypothesis, scope boundary, forbidden claim or non-claim → MINOR bump** per "
    "VERSIONING_POLICY §4. Checkpoints and results are unaffected — they were always polar. Not in this amendment: the "
    "fallback rotation σ of Stage 1 (13.0° in code, 15.0° in the v6.1.0 text), which the proposal lists as a separate "
    "PATCH item.\n")

# --- chapters: §2.1 stage table ------------------------------------------------------------------
sub("thesis/chapters/02-methodology/drafts/2.1-draft.md",
    "| Clip factor and global threshold; 8 by 8 tiles |", "| Clip factor and global threshold; polar grid |")
sub("thesis/chapters/02-methodology/translations/2.1-translation.md",
    "| Клип-фактор және жаһандық табалдырық; 8-ге 8 торкөз |", "| Клип-фактор және жаһандық табалдырық; полярлы тор |")
sub("thesis/chapters/02-methodology/translations-ru/2.1-ru.md",
    "и глобальный порог; плитки 8 на 8 |", "и глобальный порог; полярная сетка |")

# --- chapters: §2.2 closing paragraph (the leading sentence is dropped to pay for the new words) ---
sub("thesis/chapters/02-methodology/drafts/2.2-draft.md",
    "The remainder of the stage follows the specification. The rule is applied to the luminance channel\n"
    "of a perceptual colour space over an eight-by-eight tile grid, with the clipped excess redistributed\n"
    "and bilinear interpolation across tile boundaries, stochastically during training and\n"
    "deterministically at inference.",
    "The rule is applied to the luminance channel of a perceptual colour space over a polar grid of\n"
    "rings and sectors around the fovea, with the clipped excess redistributed and bilinear interpolation\n"
    "between neighbouring cells, stochastically during training and deterministically at inference.")
sub("thesis/chapters/02-methodology/translations/2.2-translation.md",
    "Кезеңнің қалған бөлігі айқындамаға сай орындалады. Ереже перцептивті түс кеңістігінің жарықтық\n"
    "арнасына сегізге сегіз торкөз торы бойынша қолданылады, кесілген артық мөлшер қайта үлестіріледі\n"
    "әрі торкөз шекаралары бойынша билинеарлы интерполяция жүргізіледі; оқыту кезінде стохастикалық,\n"
    "инференс кезінде детерминацияланған түрде.",
    "Ереже перцептивті түс кеңістігінің жарықтық арнасына фовеаны айнала сақиналар мен секторлардан\n"
    "тұратын полярлы тор бойынша қолданылады, кесілген артық мөлшер қайта үлестіріледі әрі көрші\n"
    "ұяшықтар арасында билинеарлы интерполяция жүргізіледі; оқыту кезінде стохастикалық, инференс\n"
    "кезінде детерминацияланған түрде.")
sub("thesis/chapters/02-methodology/translations-ru/2.2-ru.md",
    "Остальная часть этапа следует спецификации. Правило применяется к каналу яркости в перцептивном цветовом "
    "пространстве на сетке плиток 8×8, с перераспределением обрезанного избытка и билинейной интерполяцией на "
    "границах плиток, стохастически при обучении и детерминированно при инференсе.",
    "Правило применяется к каналу яркости в перцептивном цветовом пространстве на полярной сетке из колец и "
    "секторов вокруг фовеа, с перераспределением обрезанного избытка и билинейной интерполяцией между соседними "
    "ячейками, стохастически при обучении и детерминированно при инференсе.")

# --- proposal status ------------------------------------------------------------------------------
sub("thesis/governance/records/AMENDMENT_PROPOSAL_stage5_polar_clahe.md",
    "**Status:** PROPOSED, NOT APPLIED · **Raised:** 2026-08-12",
    f"**Status:** APPLIED {DATE} (INVARIANTS v7.2.0, ratified by the candidate) · **Raised:** 2026-08-12")
print("ok")
