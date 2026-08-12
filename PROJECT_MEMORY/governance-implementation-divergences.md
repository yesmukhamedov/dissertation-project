---
name: governance-implementation-divergences
description: Two places where INVARIANTS OD-3 does not describe what the code actually runs — polar CLAHE as the real Stage-5 default, and the fallback rotation σ that v6.1.0 "reconciled" to a wrong value
metadata:
  type: project
---

INVARIANTS OD-3 diverges from `experiments/` in two ways, both verified against the configs and
the pipeline source on 2026-08-12. Neither is a stale label — in both cases governance describes a
transform that produced none of the reported results.

**1. Polar CLAHE is the operational Stage-5 default; OD-3 defines the rectilinear one.**
`configs/default.yaml` sets `clahe_mode: polar` (commented "adaptive polar, thesis-faithful"), and
**all sixteen** run configs do the same — no config in the repo selects `tiles`.
`src/preprocessing/pipeline.py` calls `maybe_apply_polar_clahe` / `apply_polar_clahe`;
`upgraded_clahe.maybe_apply_clahe` serves the non-default branch. OD-3 Stage 5 nonetheless specifies
"Tile grid 8×8" and defines no polar geometry — while OD-3 **Stage 1** already references pivoting
"Stage-5 polar CLAHE" on the FOV centroid, so OD-3 contradicts itself. Proposed amendment (MINOR,
not applied) at `thesis/governance/records/AMENDMENT_PROPOSAL_stage5_polar_clahe.md`; §3.1.2 carries
the open `[VERIFY]`. Applying it bears on checkpoint validity, so it is the candidate's call.

**2. The fallback rotation σ is 13.0°, not 15.0° — the v6.1.0 amendment summary is wrong.**
It claims σ was "reconciled to 15.0° (the code/eval value; the prior 13.0° text is corrected)".
The code says otherwise: `fallback_rotation_sigma: 13.0` in `default.yaml` and in all sixteen run
configs, `rotation_sigma: 13.0` likewise. The two 15.0° constants in
`src/preprocessing/od_fovea_detect.py` are a Gaussian `blur_sigma` and `_MAX_ROTATION_SIGMA` — the
**hard cap on the adaptive σ**, not the fallback. So the amendment conflated cap with fallback, and
the original 13.0° chapter text was right. **Do not "fix" 13.0° → 15.0° in the chapters.** §3.1.1
keeps 13.0°, reports 15.0° as the cap, and flags this; INVARIANTS needs a PATCH.

Related: every run used `clahe_clip_factor: 2.0` / `clahe_global_threshold: 0.01`, whereas §4.3.2's
swept optimum is θ* = (2.5, 0.03). The thesis is self-consistent here (§3.1.2 leaves the two free,
§4.3.2 selects them), but the shipped configs are not at the selected optimum.

See [[stage2-fov-crop-fix]], [[preprocessing-od-fovea-polar]], [[od-fovea-heatmap-detector-plan]],
[[thesis-writing-status]].
