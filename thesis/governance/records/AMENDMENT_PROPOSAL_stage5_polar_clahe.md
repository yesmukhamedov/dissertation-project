# AMENDMENT PROPOSAL — OD-3 Stage 5: admit the polar CLAHE variant

**Status:** PROPOSED, NOT APPLIED · **Raised:** 2026-08-12 · **Against:** INVARIANTS.md v7.0.0 (OD-3 Stage 5)
**Requested bump:** MINOR (a new operational variant is admitted; no hypothesis, scope boundary, forbidden
claim or factorial design changes) per VERSIONING_POLICY §4.

---

## 1. The defect

OD-3 is internally inconsistent about Stage 5, and has been since v6.1.0.

**Stage 1** (as amended in v6.1.0) specifies the low-confidence fallback as: *"skip rotation when confidence is
below threshold (and pivot Stage-5 **polar CLAHE** on the FOV-mask centroid rather than the detected fovea)."*

**Stage 5** specifies: *"Dual-constraint clip limit on LAB L-channel: CL = min(clip_factor × tile_area / 256,
global_threshold × tile_area). **Tile grid 8×8.** Stochastic at train time (p = 0.8); deterministic at
inference."*

A rectilinear 8×8 tile grid has no pivot. Stage 1's fallback therefore references a Stage-5 behaviour that
Stage 5 does not define, and the two clauses cannot both describe the same transform.

## 2. What the implementation does

The polar variant is the operational default, not an alternative:

- `configs/default.yaml`: `clahe_mode: polar` — commented *"(adaptive polar, thesis-faithful)"* — with
  `clahe_radial_rings: 8`, `clahe_radial_exponent: 1.5`, `clahe_fine_bins: 72`,
  `clahe_min_sector_area_frac: 0.01`. The rectilinear path is the non-default `tiles` mode, for which
  `clahe_tile_grid_size: [8, 8]` applies.
- All **sixteen** run configurations in `experiments/configs/` set `clahe_mode: polar`. No config in the
  repository selects `tiles`.
- `src/preprocessing/pipeline.py` calls `maybe_apply_polar_clahe` on the training path and `apply_polar_clahe`
  on the cache path; `upgraded_clahe.maybe_apply_clahe` is imported for the `tiles` branch only.
- Design note: `experiments/docs/polar_clahe_design.md` — fovea-centred polar grid, per-sector dual-constraint
  LUTs, polar bilinear interpolation between sectors, motivated by grid artifacts and radial fundus geometry.

**Consequence:** every experimental result in the programme was produced with polar CLAHE, while the binding
definition of Stage 5 describes the variant that produced none of them.

## 3. Where the divergence is already recorded

- **§3.1.2** carries an open `[VERIFY]` flag naming it: *"Governance/implementation divergence on Stage 5
  default (OD-3 8×8 tile-grid dual-constraint CLAHE vs shipped polar variant). Draft follows governance
  (canonical); flagged for governance reconciliation."*
- **Appendix A** reproduces both modules and states the fact plainly: *"the pipeline ships with a polar variant
  of the dual-constraint CLAHE as its current default (`polar_clahe.py`), alongside the rectilinear tile-based
  formulation (`upgraded_clahe.py`); both are present in the versioned source."*
- **`PROJECT_MEMORY/preprocessing-od-fovea-polar.md`** records the switch and its consequence — checkpoints
  trained before it must be retrained.

## 4. Proposed amendment

Replace the OD-3 Stage 5 clause with a formulation that fixes the dual-constraint clip rule as the invariant
and the grid as a selectable geometry, naming the polar geometry as the default:

> **Stage 5: CLAHE** — Dual-constraint clip limit on the LAB L-channel:
> CL = min(clip_factor × cell_area / 256, global_threshold × cell_area), where a *cell* is a member of the
> partition of the field of view fixed by the selected grid geometry. Two geometries are defined.
> **Polar (default):** a fovea-centred polar partition — the pivot being the Stage-1 detected fovea when
> confident and the FOV-mask centroid otherwise — with radial rings and angular sectors, and bilinear
> interpolation between neighbouring sectors. **Rectilinear:** an 8×8 tile grid. The dual-constraint rule,
> the LAB L-channel, stochastic application at train time (p = 0.8) and deterministic application at
> inference are invariant across both. Always on.

The clip factor and global threshold remain free hyperparameters fixed empirically, as §3.1.2 states and
§4.3.2 determines; this amendment does not fix their values.

## 5. Why it is not applied unilaterally

Two consequences belong to the candidate, not to a documentation pass.

1. **Checkpoint validity.** Naming polar as the operational default makes the rectilinear formulation the
   variant, which changes what a reader takes the reported results to be results *of*. That is the correct
   reading — but it should be ratified deliberately, not acquired as a side effect of a sync.
2. **Narrative reach.** §3.1.2 currently follows governance and describes the rectilinear formulation as
   canonical, with the polar variant presented as an exploration ("spatially-adaptive refinement"). If the
   amendment is adopted, §3.1.2 must be rewritten so that the *default* is described as the default, and the
   `[VERIFY]` flag discharged. §3.1.1's Stage-5 pivot sentence and Appendix A's Stage-5 note then become
   consistent with it rather than exceptions to it.

## 6. Alternative, if the amendment is rejected

Change the code default to `clahe_mode: tiles` and retrain. This is the more expensive branch and it discards
the anatomical motivation recorded in the design note, but it would make the shipped pipeline match the
binding definition instead of the reverse. It is stated here only so that the decision is between two options
rather than one.

## 7. Related open item

The **fallback rotation σ** in the v6.1.0 amendment summary is separately wrong and needs a PATCH-level
correction to INVARIANTS: the summary states σ was reconciled to 15.0° "the code/eval value", but
`fallback_rotation_sigma: 13.0` holds in `default.yaml` and in all sixteen run configurations. The 15.0°
constants in `src/preprocessing/od_fovea_detect.py` are a Gaussian `blur_sigma` and `_MAX_ROTATION_SIGMA`,
the hard cap on the *adaptive* σ — neither is the fallback. See `VERSION_SYNC.md` v7.1.2 and the `[VERIFY]`
flag in §3.1.1.
