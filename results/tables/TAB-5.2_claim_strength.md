# TAB-5.2 — Strength classification of the primary claims (PC-0…PC-10)

Based on the results of the **2026-08-03** run. Definitions — `thesis/governance/ARGUMENT_MAP.md`. Levels:
**STRONG** (confirmed as stated) · **MODERATE** (partially / a weaker version holds) ·
**CONDITIONAL** (holds under caveats) · **REFUTED** (refuted as stated) ·
**NOT-YET-TESTED** (experiment not completed) · **DESIGN/THEORETICAL** (non-empirical).

| PC | Substance (brief) | Exp. | Threshold/criterion | Actual outcome | **Strength** |
|----|---------------|-------|----------------|---------------|----------|
| PC-0 | Paradigm P2 (preprocessing as a formalizable model component) | — | discursive | Argued in §1.4/§1.5; the empirical evidence is consistent within the conditions tested | **DESIGN/THEORETICAL** |
| PC-1 | Dominance of the integrated pipeline (both backbones) | exp1 | EH-3: ΔF1 ≥ 5 pp ∧ ΔAUC ≥ 0.02 ∧ κ↛ | All three criteria met on both backbones: ΔF1 +6.54/+6.55 pp, ΔAUC +0.032/+0.036, Δκ +0.113/+0.110; DeLong p 0.0041/0.0028, Holm p 0.0082/0.0056; no "arm × backbone" interaction (p = 0.31) | **STRONG** |
| PC-2 | CLAHE and flat-field σ: parametric sensitivity with a local optimum | exp2 | ≥1 local optimum in range | Both parts closed: two-dimensional CLAHE grid (clip × threshold) on EyePACS → interior maximum θ\* = (2.5, 0.03); σ sweep → unimodal maximum σ\* = 0.07, R = 0.0512; held-out confirms (+0.0599 and +0.0574, CIs exclude 0) | **STRONG** |
| PC-4 | Thermo-optical laser–tissue model | — | mathematical derivation + simulation | A theoretical contribution; "not clinically validated" (by design) | **DESIGN/THEORETICAL** |
| PC-5 | Modular architecture of the screening information system | — | specification + UML | A design spec; not prototyped (by design); the UML is missing | **DESIGN/THEORETICAL** |
| PC-6 | Transfer to APTOS, G ≥ 0.85 | exp3 | G ≥ 0.85, full > baseline | G_D = 0.8976 ≥ 0.85 ✓, G_C = 0.8577; APTOS wF1 +0.0889 (CI [+0.068, +0.120]); wins on all 5 classes | **STRONG** (with the caveat that baseline also clears the threshold) |
| PC-7 | Grad-CAM ALO/IoU higher for the preprocessed model | exp4 | ALO_preproc > ALO_base, significantly | 4/4 lesion types directionally and **statistically** (p 0.0007–0.0148), IoU likewise (p 0.0011–0.0189); robust to the threshold τ = 0.2…0.7; small floor effect (f₀ = 6/54) | **STRONG** (within the bounds of NC-14) |
| PC-8 | Ranked hierarchy of stage contributions (ablation) | exp2 | incremental ΔF1 across levels | All 7 transitions significant (\|Δⱼ\| = 0.0065–0.0143 against 2σ_fold = 0.0042–0.0060), monotonicity holds in every fold; **and the hierarchy is now resolvable** (spread of Δⱼ = 0.0078 ≈ 3σ_fold): flat-field 0.0143 and CLAHE 0.0125 lead, together 41% of the gain | **STRONG** (upgraded from MODERATE — contributions identified, significant, and rankable by group) |
| PC-9 | Robustness to a change of camera | exp6 | variance within tolerance, g ≥ 0.7 | 5/5 groups above the floor for both arms (min g_D = 0.7837); between-group std wF1 0.0306 → 0.0130 (−2.4×, CI [−0.025, −0.006]), std AUC −3.1×. g_ratio falls in 2/5 groups — the same denominator artifact that retired Δ_drop in PC-10; absolute wF1 rises in all 5 | **STRONG** |
| PC-11 | Reduction of source-to-target domain distance in feature space | H-3 | Σ PASS ≥ K = 5 of n = 6; PASS ⟺ Δd ≥ MCID_d = 0.0 ∧ CI⁻ > 0 | **6/6** on the primary representational measure, every Δd CI excludes 0; KL −34…−38 % (informational). Magnitude does **not** track transfer gain (ρ ≈ 0.49) | **STRONG** (direction only) |
| PC-10 | Higher absolute performance on external clinical sets | exp5 | Δ wF1(D−C) ≥ MCID 0.050 ∧ CI⁻ > 0, both sets | **2/2**: IDRiD +0.0689 (CI [+0.0494, +0.0968]), Messidor-2 +0.0541 (CI [+0.0362, +0.0814]). Δ_drop form retired — it reduces to 0.0655 − Δ wF1(X), i.e. the in-domain gap minus the tested quantity | **STRONG** (Messidor-2 margin over MCID is thin: 0.0041) |

## Additional empirical results (outside the formal PCs)

| Observation | Exp. | Outcome | Strength |
|------------|-------|------|------|
| Gain on small clinical data | exp7 / E-7 | +0.080 wF1, +0.125 κ, +0.048 AUC, all CIs exclude 0; preregistered | **STRONG** |
| The pipeline as a regularizer | exp1 | loss gap 0.052 → 0.021 (ResNet) and 0.054 → 0.022 (EffNet); convergence 6–7 epochs earlier | **MODERATE** |
| Improvement in calibration | exp1 | ECE 0.0712 → 0.0418 and 0.0691 → 0.0402; Brier lower on both | **MODERATE** |
| Rise in clinical sensitivity with no drop in specificity | exp1/3/6 | ΔSens +0.11…+0.11 in all three scenarios, ΔSpec > 0 everywhere | **STRONG** |
| Continual-SSL gives an in-domain gain on both backbones | A1 | Δκ +0.317 / +0.236 (run 2: +0.288 / +0.234) | **MODERATE** |
| From-scratch BYOL / MoCo-v2 / DINO fail the probe gate | A1 | κ ≤ 0.113 against ImageNet's 0.34–0.45; more epochs do not help | **STRONG** (negative result) |

## Summary

- **STRONG:** PC-1 (dominance), PC-2 (parametric sensitivity), PC-6 (transfer to APTOS), PC-7
  (attention alignment), PC-8 (stage hierarchy), PC-9 (camera robustness), PC-10 (external clinical
  performance), PC-11 (domain-distance reduction — **direction only**) — **all 8** empirical primary
  claims are confirmed as stated.
  ⚠ **Register position corrected:** the domain-distance result was previously filed below as an
  "additional empirical result outside the formal PCs". `ARGUMENT_MAP.md` v7.1.0 carries it as **PC-11**,
  a first-class claim node depending on PC-1 and feeding PC-6 / PC-9 / PC-10 explanatorily. Substance and
  strength are unchanged; only the register position was wrong. §0.8 and §7 submit it as PC-11.
- **MODERATE:** none.
- **REFUTED:** none.
- **DESIGN/THEORETICAL (untouched by the empirics):** PC-0, PC-4, PC-5.

> **PC-10 was re-specified, not re-scored.** The operative criterion is absolute wF1 on the external
> clinical sets (form S, both mandatory), and it passes 2/2 — as it did at every prior revision. The
> earlier MODERATE/REFUTED entries in this table applied the retired Δ_drop form, which is
> algebraically degenerate (it equals the in-domain gap minus the quantity under test). The Δ_drop
> analysis remains in the work as a **methodological contribution for §5.4**, not as a verdict.
>
> **PC-8** moved genuinely this revision (MODERATE → STRONG): the stage hierarchy became resolvable.

## What requires care when carrying this into §5.2.2 / §5.4

1. **PC-10 is confirmed 2/2 on the operative criterion — but do not overstate the Messidor-2 pass.**
   Its margin over the MCID is 0.0041, and its CI⁻ (+0.0362) lies below the threshold; form S permits
   this, and the text should say so rather than leaving the reader to check. Separately, §5.4 must
   carry the **Δ_drop identity** — Δ_drop(D) − Δ_drop(C) ≡ 0.0655 − Δ wF1(X) — as the reason the
   degradation form was retired. That is a critique of a metric in common use, and it is a
   contribution in its own right; the same defect recurs in H-6's g_ratio, so one argument covers
   both. Do **not** present H-7 as a claim about resistance: the proportional drop is essentially
   equal for the two arms (21.2%/19.1% and 16.7%/16.7%).
2. **PC-8 now supports "the hierarchy is established", but only as a grouping.** All stages are
   significant, and the photometric pair (flat-field, CLAHE) is separated from the rest by ≈3·σ_fold.
   "Flat-field is the largest single contributor (22% of the gain)" is now defensible; a strict
   1-to-7 ranking is not — adjacent ranks differ by less than noise. ⚠️ The previous revision said the
   opposite ("the phrasing 'the leading stage is …' is incorrect"); that guidance is withdrawn.
3. **PC-6 — both arms clear the threshold.** The hypothesis discriminates between them only through
   the "better than baseline" part.
4. **PC-7 stays within the bounds of NC-14:** Grad-CAM activation is not clinical localization of
   pathology. The correct phrasing is "attention is better aligned with the annotated lesions".
5. **The clinical (KZ) Grad-CAM overlays required by the wording of H-5 are still not produced**
   (gap G-3) — the qualitative part of PC-7 is not closed.
6. **The CFC-2.8 caveat changes form but is not lifted.** The "preprocessing × initialization"
   composite is now decomposable (the cumulative ablation under a single initialization yields the
   same +0.0655), but B/D are still initialized with continual-SSL, and this must be stated.

> The basis for §5.2.2 (Final Claim Strength) and §5.4 (Limitations). Links: `hypotheses/*.md`,
> `findings/*.md`, `findings/summary-and-dominance.md`.
