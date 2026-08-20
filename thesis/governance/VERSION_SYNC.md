# VERSION SYNCHRONIZATION REGISTER

**Version:** 7.2.0 | **Date:** 2026-08-20

## v7.2.0 Sync Scope — restructuring to the council's measured norms (one boundary amended)

The volume is being rebuilt to the shape measured across all 16 dissertations published by this
council (`council/en/10-dissertation/peer-norms.md`): four chapters, two numbering levels, and
about 28,000 words of main text against the 101,459 it carried. One binding is amended and nothing
is reversed. **MINOR** per VERSIONING_POLICY §4.

| File | Was | Now | What changed |
|---|---|---|---|
| `INVARIANTS.md` | 7.0.0 | **7.1.0** | SB-4.1 amended — a deployed demonstrator exists; SB-4.2/4.3 stand. Chapter references renumbered for four chapters. |
| `outline/MASTER_OUTLINE.md` | 7.1.0 | **8.0.0** | Rewritten as the structural specification of the four-chapter volume; superseded planning lists removed. |
| `outline/TABLE_OF_CONTENTS_EN.md` | 7.1.0 | **8.0.0** | Four chapters, 24 second-level subsections, no codes in headings. |
| `outline/TABLE_OF_CONTENTS_KZ.md` | 7.1.0 | **8.0.0** | Same, plus appendix lettering А, Ә, Б, В, Г. |
| `outline/REWRITE_MAP.md` | — | **new** | All 98 drafted sections mapped to destination or CUT, with word budgets. |

**Pending in this line, not yet done:** the body itself (Phase 2), the Kazakh edition (Phase 4),
the trilingual annotation (Phase 5), and the abbreviations list, from which the governance codes
must be removed once they no longer appear in the text. `HYPOTHESIS.md`, `ARGUMENT_MAP.md`,
`CONTRIBUTIONS.md`, `CENTRAL_THESIS.md`, `CORE_OBJECTIVE.md` and `RESEARCH_ARCHITECTURE.md` are
**unaffected** — they define what may be claimed, and the restructuring changes where a claim is
made, not what it is.

---

## v7.1.2 Sync Scope — register repair + chapter currency (no new binding)

A consistency audit of `thesis/chapters/` against governance and `results/` closed the last places where the
H-3 / H-7 line had not landed, and repaired this register itself, which had drifted from the files it tracks.
**No binding is created, reversed or reinterpreted. PATCH-level** per VERSIONING_POLICY §4.

**Chapter corrections.**

- **`§5.2.2` did not classify PC-11 at all** — the one section the H-3 restoration never reached. It recorded
  "ten primary claims — seven empirical" and Table 5.4 had no PC-11 row, while `ARGUMENT_MAP.md` v7.1.0,
  `results/tables/TAB-5.2_claim_strength.md`, §0.8 (provision 5) and §7 all carry PC-11. Since §0.8 derives its
  ceiling from §5.2.2, provision 5 was submitted without a classification behind it. PC-11 is now a table row at
  **STRONG (direction only)**, the tally reads **eight empirical claims**, and the direction-only bound —
  no magnitude correspondence, separate representation spaces per arm, mechanistic scope — is set out with the
  other travelling qualifications.
- **`§3.1.1` and `§3.1.3` described the retired classical Stage-1 detector**, listed as pending narrative sync
  since v6.1.0 but never done, and the chapter was approved over it. §3.1.1 now describes the pre-trained,
  **frozen** U-Net + DSNT heatmap detector, and its reliability paragraph reports the held-out IDRiD **test**
  split (103 images, disjoint from the detector's training): OD median **0.066 R** with every image inside one
  optic-disc radius, fovea median **0.105 R** with **99.0%** inside one radius, and a confidence flag that
  **discriminates** (declines on 9.7% of images, whose fovea error runs ≈4× the median of the rest). The
  superseded figures it replaced — fovea inside one radius in 0.0%/0.97% of images, a median error of ~5 radii,
  and a `confident` flag asserted on 100% of images and therefore uninformative — had been carried as the
  dissertation's own analysis and as the justification for the stage's design.
- **`§4.1.1` Table 4.1** labelled the roles of Messidor-2 and IDRiD with the retired *clinical degradation
  resistance* form of H-7; both now read **external clinical performance**, as does the inherited-limitation
  sentence that follows the table.
- **`§7`** opened "Seven questions remain open" and then enumerated four, three, and "the eighth question" —
  now **eight**, matching its own checklist.
- **`§5.2.1`** described the apparatus as spanning "the seven experiments" while §4.C reports **eight
  experimental investigations** and §5.2.1's own apparatus table carries the H-3 row; corrected to eight.
- **`§0.8`** recorded a divergence — TAB-5.2 filing the domain-distance result outside the formal claim
  register — that v7.1.1 closed. The checklist now records the register as uniform across all four sources.
  The corresponding brief, continuity note and review are left as written: they are session records of a
  divergence that was real when they were made.

**Register repair.** The File Version Status table contradicted both the files it tracks and this document's own
amendment prose: `CONTRIBUTIONS.md` appeared **twice** (7.0.0 and 6.3.0) against an actual 7.1.0;
`LITERATURE_INDEX.md` **twice** (v5.3 ✅ and 5.0 ❌) against an actual 6.1.0; `gulshan-2016.md` **twice** with
opposite verdicts; `VERSION_SYNC.md`'s own row read 7.0.0 at file version 7.1.1; `HYPOTHESIS.md` and
`ARGUMENT_MAP.md` read 7.0.0 at actual 7.1.0; both glossaries read 6.2.0 although the v7.0.0 scope above
records them bumped to 7.0.0, which they are; and `TABLE_OF_CONTENTS_KZ.md` read "5.0 ⚠️ verify" — verified,
it is current. Duplicates removed, versions reconciled, one stale ⚠️ discharged.

**Two defects found in the pass and left open, because closing either is a decision and not a sync:**

1. **The fallback rotation σ in the v6.1.0 amendment summary is wrong.** It states that σ was "reconciled to
   15.0° (the code/eval value; the prior 13.0° text is corrected)". The implementation does not bear this out:
   `fallback_rotation_sigma: 13.0` in `configs/default.yaml` and in all sixteen run configurations, with
   `rotation_sigma: 13.0` likewise. The two 15.0° constants in the detector source are a Gaussian `blur_sigma`
   and `_MAX_ROTATION_SIGMA`, the **hard cap on the adaptive σ** — neither is the fallback. The 13.0° chapter
   text was therefore correct and the amendment summary conflated cap with fallback. §3.1.1 retains 13.0°,
   reports 15.0° as the cap, and carries a `[VERIFY]` flag naming this; INVARIANTS needs the correction.
2. **OD-3 is internally inconsistent about Stage 5.** The Stage-1 fallback clause pivots "Stage-5 **polar**
   CLAHE" on the FOV centroid, but the Stage-5 definition specifies a rectilinear 8×8 tile grid and defines no
   polar variant — while Appendix A records the polar variant as the shipped default. §3.1.2 has carried a
   `[VERIFY]` on exactly this since it was drafted. A proposed amendment is filed at
   `records/AMENDMENT_PROPOSAL_stage5_polar_clahe.md`; it is **not applied**, because admitting the polar
   variant as the operational default bears on which checkpoints remain valid.

## v7.1.1 Sync Scope — downstream currency pass (no new binding)

Four documents that had fallen behind the INVARIANTS v7.0.0 / HYPOTHESIS v7.1.0 line are brought current,
plus one register-position correction. **No binding is created, reversed or reinterpreted**; every change
tracks a decision already ratified. **PATCH-level** per VERSIONING_POLICY §4 (documentation sync only).

- **`CORE_OBJECTIVE.md` 5.0 → 7.1.0.** *Clinical degradation resistance* → **external clinical performance**;
  the **H-3 direct measurement** added to the validation programme — the one element this document predated
  entirely. Authoritative prose is now §0.3, from which the statement is derived; the two must agree.
- **`CENTRAL_THESIS.md` 6.0.0 → 7.1.0.** Same H-7 correction; the directly measured distance reduction added
  to the substantiating evidence. **Plus a correction found during the pass:** the prior text listed
  *qualitative Grad-CAM overlays on a Kazakh clinical dataset* among the substantiating evidence. Those
  overlays were **never produced** (gap G-3), so citing them as substantiation asserted evidence that does
  not exist. H-5 is supported in its **quantitative half only**.
- **`outline/MASTER_OUTLINE.md` 6.0.0 → 7.1.0.** Four currency defects corrected: the **object of research**
  (a category error — the images were named as the object rather than the *process*, contradicting the
  house convention and the council-verified abstract); **H-3** recorded as dropped, whereas it is live and
  written as §4.4; **H-7** in its retired form; and a **duplicated objective number** (two items numbered 8).
  The Novelty and Provisions lists are **marked superseded** by §0.2 and §0.8 rather than rewritten — they
  enumerate what was planned, not what is defended, and where outline and drafted sections disagree the
  drafted sections win.
- **`results/tables/TAB-5.2_claim_strength.md` — register position corrected.** The domain-distance result
  was filed as an "additional empirical result outside the formal PCs"; `ARGUMENT_MAP.md` v7.1.0 carries it
  as **PC-11**, a first-class node depending on PC-1 and feeding PC-6 / PC-9 / PC-10 explanatorily. Substance
  and strength unchanged (STRONG, direction only); the tally becomes **8 of 8** empirical primary claims.
  §0.8 and §7 already submit it as PC-11.

**Chapter body complete.** Chapters 0–7 are drafted, reviewed and approved. §0.8 (Provisions Submitted for
Defence) is the forward ceiling for every downstream deliverable, and §5.C the rearward one; the §7 review
carries the provision-by-provision ceiling audit. **A fifth defect closed in the same pass:** the trilingual
abstract (`thesis/output/abstract_{en,kz,ru}.md`) said "seven experiments" (the programme is **eight**
investigations), omitted H-3, carried a statements-for-defence list of six items with one still in the
retired Δ_drop form, and **listed the Vessel Visibility Index among the methods although §4.3.3 excluded it
for want of an implementation and a source** — an error, not merely stale. All three languages are now
synced against §0.2 / §0.6 / §0.8 / §7: novelty 10 items, results 9, statements 11 + one observation + an
explicit non-claims paragraph.

## v7.1.0 Amendment Scope

**H-3 restored as *Domain-Shift Reduction* (MINOR — a hypothesis is added; no binding is reversed).** The label H-3 was vacated in V3 when the *training-method comparison* it then denoted was dropped; **that retirement stands** and the label is **reused** for a distinct hypothesis. H-3 now asserts that the integrated configuration reduces the distance between source and external domains in penultimate-layer feature space.

**Acceptance form — "K of n", K = 5, n = 6:**

```
H-3  ⟺  Σ PASS_S(d, X)  ≥  5,    X ∈ {APTOS, IDRiD, Messidor-2, DDR, ODIR-5K, RFMiD}

PASS_S(d, X)  ⟺  Δd(X) = d(BASE, X) − d(INT, X)  ≥  MCID_d = 0.0   ∧   CI⁻(Δd) > 0
```

`d` = MMD (or FID) over penultimate-layer features — **primary, and the sole basis of the criterion**. `d_KL` over per-channel intensity histograms is **secondary and informational only**. Confidence intervals from **1 000 bootstrap resamples**. Arms = the integrated − baseline pair (EfficientNet-B3; configurations D − C of Experiment 1). **Cost: forward passes only, no training.**

**Rationale.** The central hypothesis asserts a causal chain — the pipeline reduces domain variability, and reduced variability improves external classification. Every prior hypothesis measured the chain's *consequence* (H-4, H-6, H-7); none measured its *middle term*. H-3 measures it directly, making the mechanism independently falsifiable of the performance claims.

**Mandatory protocol condition.** Stage 7 normalization **must** use source-domain statistics, as in zero-shot deployment. Computing it from the target corpus would make the measurement a form of target-domain adaptation and would render it incomparable with H-4/H-6/H-7. An evaluation violating this condition does not test H-3.

**Threshold provenance — stated openly.** Neither MCID_d nor K was pre-registered; **both are assigned at this formalization**. MCID_d = 0.0 is not a tuned choice — d is unnormalized, so no non-zero minimal difference is interpretable and the per-corpus condition degenerates to CI⁻(Δd) > 0, a bare directional-significance test. The outcome is **insensitive to K**: it passes for every K ≤ 6, so the choice K = 5 does not determine the verdict. **VCR-1** is satisfied by this versioned amendment; **VCR-3** is not engaged — the direction of effect was never contradicted.

**Pre-specified reversal case, retained.** Stage 5 (CLAHE tuned on the source corpus) and Stage 7 (dataset-specific normalization) are source-bound by construction, so a REVERSED outcome — variability reduced *within* the source domain while increased *across* domains — was a live possibility. It would have been an established finding, not a failed run, and would have explained any corresponding reversal in H-4 and H-7.

**Label-reuse notice (binding downstream).** "H-3 dropped" in §2.3.2 and §3.3.3 and in their briefs and continuity notes refers to the **retired training-method hypothesis** and is historically correct; it must not be read as referring to the present H-3.

**Governance files updated:** HYPOTHESIS (amendment, H-3 definition, Central-Hypothesis note, Conclusion), ARGUMENT_MAP (**PC-11** node + DAG), CONTRIBUTIONS (**SC-I**), VERSION_SYNC, CHANGELOG. **Downstream sync completed 2026-08-05:** `thesis/ASSET_INVENTORY.md` (H-3 row; open decision 3 closed), `thesis/CLAUDE.md`, `thesis/outline/TABLE_OF_CONTENTS_EN.md` and `TABLE_OF_CONTENTS_KZ.md` (§4.4), and `thesis/chapters/04-experiments/` (§4.4.1 / §4.4.2 drafts, briefs, continuity notes and reviews). `results/` already carried the block. **Still pending, and not gating this bump:** FIG-4.17 to be rendered; the MMD kernel and the per-domain sample size remain unrecorded and are `[VERIFY]`-flagged in §4.4.1.

**H-1 through H-7 (other than the H-3 addition), all scope boundaries, forbidden claims, non-claims, the composite independent variable and CFC-2.8 are unchanged.**

## v7.0.0 Amendment Scope

**H-7 reformulated: Clinical Degradation Resistance → External Clinical Performance.** The dependent variable changes from the degradation quantity Δ_drop = F1_EyePACS_val − F1_external to the **absolute external performance difference** Δ wF1(X) = wF1(integrated, X) − wF1(baseline, X), with acceptance form S — Δ wF1(X) ≥ MCID_wF1 = 0.050 **and** CI⁻ > 0 — required on **both** external clinical sets, evaluated independently (no aggregation; a reversal on either set yields REVERSED). Note the form requires Δ ≥ MCID and CI⁻ > 0, **not** CI⁻ ≥ MCID.

**Rationale.** The retired dependent variable is not independent of the hypothesis it was meant to test: Δ_drop(integrated) − Δ_drop(baseline) ≡ [wF1(int,in) − wF1(base,in)] − [wF1(int,X) − wF1(base,X)] = Δ_in-domain − Δ_external. The comparison is therefore the fixed in-domain margin minus the quantity under test, satisfiable only when the integrated arm exceeds baseline *more on foreign data than on its own* — it penalizes the integrated arm for its in-domain result and measures nothing about resistance. Identified analytically, not by inspection of outcomes.

**VCR-3 is not engaged:** it governs results contradicting the *direction of effect*, and that direction — the integrated arm performing better on external clinical data — was never contradicted at any evaluation; the failure was in the metric expressing it. The retired form is preserved as a descriptive quantity in HYPOTHESIS/INVARIANTS and its results remain reportable in Chapter 5 §5.4 as a critique of a degradation metric in common use (a secondary methodological contribution, SC-G). **VCR-1 is satisfied** by issuing a new versioned Invariants document (this bump).

**A hypothesis is reformulated incompatibly with the prior version → MAJOR bump** per VERSIONING_POLICY §4. H-1 through H-6, all scope boundaries, forbidden claims, non-claims, the composite IV and CFC-2.8 are unchanged. Governance files updated: INVARIANTS (Section II H-7, header), HYPOTHESIS (H-7, Central-Hypothesis note, Conclusion, header), ARGUMENT_MAP (PC-10, SC-10.1, PC-10 strength, DAG label, dependency note), CONTRIBUTIONS (SC-G + secondary methodological contribution), RESEARCH_ARCHITECTURE (§5.5, §9.1 bullet, PC-10 row), VERSION_SYNC, CHANGELOG. **Downstream sync completed 2026-08-04:** `thesis/ASSET_INVENTORY.md` (Exp-5 row, TAB-4.8, FIG-4.15, TAB-5.2 tally, header provenance; Exp-2/6/7 verdict rows also refreshed to the current run), `thesis/glossary/GLOSSARY_EN.md` and `GLOSSARY_KZ.md` (both → v7.0.0: H-7 entry renamed and redefined, **MCID** added as a new operational term, "Clinical Degradation Resistance" and "Δ_drop" moved to Deprecated Terms with Superseded-By pointers, Messidor-2 entry corrected). `results/` was already aligned.

**Still pending** (does not gate this bump): chapter 4/5 briefs and drafts referring to "clinical degradation resistance"; FIG-4.15 needs regeneration and re-captioning; artifact filenames (`TAB-4.8_exp5_degradation.md`, `exp5_degradation.json`, `08_exp5_generalization.png`) retain the old term — paths, not prose, and renaming them is optional. **CENTRAL_THESIS.md (v6.0.0) and CORE_OBJECTIVE.md (v5.0)** both contain the phrase "clinical degradation resistance" in prose enumerations of the validation programme; they were **not** bumped here because neither states a criterion — the wording should be changed to "external clinical performance" in their next revision, and both were already behind the INVARIANTS line before this amendment.

## v6.3.0 Amendment Scope

**Supervised in-domain pretraining (SIP) added as a gate-selected integrated-arm initialization.** From-scratch label-free CNN-SSL (BYOL / MoCo-v2 / DINO) **failed** the linear-probe acceptance gate on the EyePACS-test corpus — best quadratic-κ ≈0.11 vs ImageNet ≈0.30, flat/declining ep50→ep100, a robust negative result (`experiments/outputs/ssl/COMPARISON.txt`). In response, **SIP** is admitted alongside fundus-SSL and the ImageNet→continual-SSL fallback: the same CNN backbone is supervised on the 53,576-image EyePACS-test corpus **using its DR grades** (started from ImageNet, adapted), then transferred to Experiment 1, with the final choice among the three inits made by the existing linear-probe acceptance gate on a **patient-level holdout**. This **(1) relaxes SB-2.4** to permit supervised use of the EyePACS-test grades for a distinct in-domain *pretraining* stage — the corpus stays disjoint from the Experiment-1 35,126 CV set by image + patient identity (INV-SSL-1/2) and is still not folded into Experiment-1 training; **(2) extends CFC-2.8** to list SIP as a gate-selected init while retaining its core confound caveat (the integrated arm still differs from baseline along both preprocessing and initialization); **(3) generalizes SC-H** from "self-supervised" to "in-domain initialization (self-supervised OR supervised), gate-selected," recording the SSL negative result as evidence. The label-free SSL objective is unchanged; SIP is a separate objective. **Adds an allowed initialization + relaxes one operational restriction; reverses no hypothesis, scope boundary, or forbidden-claim → MINOR bump** per VERSIONING_POLICY §4. Governance files updated: INVARIANTS (header, SB-2.4, CFC-2.8), CONTRIBUTIONS (SC-H), VERSION_SYNC. **Pending downstream sync** (does not gate this bump): HYPOTHESIS Premise-4/Conclusion wording, RESEARCH_ARCHITECTURE §4.2bis/§9.1, glossary EN/KZ. Implementation: `experiments/scripts/run_sip_pretrain.py`, spec `experiments/docs/supervised_indomain_pretraining_brief.md`, proposal `thesis/governance/records/GOVERNANCE_AMENDMENT_PROPOSAL.md`.

## v6.2.0 Amendment Scope

**Fundus-SSL corpus + acceptance protocol locked for the integrated arm.** The v6.0.0 ophthalmology-SSL decision is unchanged; v6.2.0 fixes the operational specifics that were previously left open. (1) The integrated-arm SSL corpus is the **unlabeled EyePACS "test" split — 53,576 images**, **disjoint** from the Experiment-1 evaluation corpus (the ~35,126 labeled "train" split, 5-fold patient-level CV) by image identity *and* patient identity. This no-pretraining-leakage constraint is recorded as new clause **SB-2.4** (INVARIANTS) and operationalized in the experiments code as the disjointness assertions **INV-SSL-1 / INV-SSL-2**. (2) **BYOL** (Grill et al., 2020) is recorded as the **primary** CNN-compatible protocol (MoCo-v2 / SimSiam / DINO retained as alternatives), pretrained **from-scratch** on the 4-channel tensor. (3) A **linear-probe acceptance gate** is added: an SSL checkpoint enters Experiment 1 only after it beats random init and is competitive with ImageNet, for both backbones. **Adds new referenceable entities (SB-2.4, the linear-probe acceptance gate), reverses no binding → MINOR bump** per VERSIONING_POLICY §4. CFC-2.8 (baseline ⟹ ImageNet, integrated ⟹ fundus-SSL) and the composite IV are retained; no SSL performance is asserted (the integrated arm is specified, not yet trained). Governance files updated: INVARIANTS (SB-2.4, DGL-6, header), HYPOTHESIS (Premise 4 + Conclusion RETFound→SSL sync; specifics), RESEARCH_ARCHITECTURE (§4.2bis, §9.1), CONTRIBUTIONS (SC-H), VERSION_SYNC, CHANGELOG. Narrative sync: methodology §3.3.2 draft + KZ translation + continuity; glossary EN/KZ (linear-probe gate term + SSL-entry refinements). Literature: SSL cards #84–#92 already registered (no new card needed); LITERATURE_INDEX notes BYOL as the selected primary.

## v6.1.0 Amendment Scope

**OD-3 Stage-1 detector: classical CV → pre-trained, frozen learned detector.** The Stage-1 OD/fovea detector is replaced by a pre-trained, **frozen** heatmap-regression detector (U-Net encoder + DSNT head, trained on IDRiD localization ground-truth) that predicts OD/fovea probability heatmaps on the FOV-cropped frame with sub-pixel centers and a genuine per-landmark confidence. It meets the held-out IDRiD-test acceptance bar (OD median 0.066 R / 100 % within 1 R; fovea median 0.107 R / 99 % within 1 R; informative fovea confidence, Spearman ρ ≈ 0.44). The fallback rotation **σ is reconciled to 15.0°** (the code/eval value; the prior 13.0° text is corrected). The detector is **pre-trained and frozen — not co-trained with the DR classifier** — so preprocessing remains a fixed transform and `model = preprocessing + CNN` holds. **Adds a new substantive entity (the learned Stage-1 detector), reverses no binding → MINOR bump** per VERSIONING_POLICY §4. No hypothesis, scope boundary, factorial design, or other operational definition (Stages 0, 2–7) changes.

In-repo integration (Phase 2): the learned detector lives at `experiments/src/preprocessing/od_fovea_net/` behind the unchanged `detect_od_fovea(image_rgb) → ODFoveaResult` facade (additive confidence/heatmap fields); the live pipeline pivots Stage-5 polar CLAHE on the detected fovea when confident (else FOV centroid), with the pivot cached for the training path. `scripts/validate_od_fovea_idrid.py` reproduces the acceptance numbers on the IDRiD test split inside the monorepo. **Pending downstream (narrative) sync:** chapter drafts (3.1.1, 3.1.3, 1.1.1, 2.2.1), assembled dissertation bundles, abstracts, and glossary entries that still describe the classical Stage-1 detector are regenerated artifacts and remain a separate documentation pass (they do not gate this governance bump).

## v6.0.0 Amendment Scope

**RETFound replaced by ophthalmology-specific self-supervised pretraining.** The integrated arm of Experiment 1 no longer initializes from the RETFound ViT-Large foundation model; instead the existing CNN backbones (ResNet-50 / EfficientNet-B3) are initialized from a CNN-compatible domain-adaptive self-supervised learning protocol (DINO / BYOL / SimCLR / MoCo family, selected empirically) pretrained on an unlabeled retinal fundus corpus. Rationale: RETFound changes both architecture and initialization, confounding the preprocessing contribution; a CNN-native SSL initialization changes only the initialization stage. **This reverses the v5.1–v5.2 RETFound binding → MAJOR bump per VERSIONING_POLICY §4.**

Resolutions: **AOQ-1 → option (b)** (CNN-compatible SSL); **AOQ-4 resolved** (the 2×2 *(preprocessing × architecture)* factorial symmetry is restored — both backbones in both arms; configs **B and D reinstated**, config **B′ retired**); **AOQ-3 retired** (RETFound license moot); **AOQ-2 simplified** (SSL pretrained directly on the 4-channel tensor). The composite *(preprocessing × pretraining)* independent variable and **CFC-2.8 are retained** (baseline ⟹ ImageNet, integrated ⟹ ophthalmology-SSL), so the H-1 effect remains non-attributable to preprocessing alone. EH-4 cross-architecture replication is reinstated. A new supporting contribution **SC-H** records the SSL initialization (bounded by CFC-2.8). No preprocessing operational definitions (OD-3, Stages 0–7) are modified. The v5.3 paradigmatic framing (P1/P2, SB-1.12, CFC-2.9, SIR-9) is retained unchanged.

## v5.3 Amendment Scope

Paradigmatic framing introduced. Two paradigms recognised: **P1** (end-to-end CNN; preprocessing as ancillary data preparation) and **P2** (integrated preprocessing-CNN; preprocessing as integral model component). Gulshan et al. (2016) designated canonical representative of P1 (per the methodological-practice criterion in SIR-9). New governance clauses: **SB-1.12** (Gulshan is not a numerical benchmark, baseline is operational construct per OD-3), **CFC-2.9** (forbids false attribution of "preprocessing is unimportant" claim to Gulshan or other P1 sources), **SIR-9** (paradigmatic-attribution rule). PC-0 (Paradigmatic Framing Claim) added to ARGUMENT_MAP as a non-empirical methodological claim feeding into IT-1. CENTRAL_THESIS gains an introductory paradigmatic-framing paragraph. CONTRIBUTIONS gains an introductory conceptual-framing block and a reframed C-1 novelty statement. No operational definitions, hypotheses, or experimental protocols are modified. The integration tracker is `GULSHAN_PARADIGM_INTEGRATION_PLAN.md` at the repository root.

## v5.2 Amendment Scope

Refinement of the RETFound pretraining-corpus description. The integrated arm of Experiment 1 is now described as initialized from RETFound, a foundation model **MAE-pretrained on a multi-modal retinal imaging corpus** comprising ≈904K color fundus photographs (CFP) + ≈736K optical coherence tomography (OCT) scans (~1.6M total) per Zhou et al. 2023, Nature. The dissertation's integrated arm loads the **CFP-pretrained checkpoint** specifically; the multi-modal description characterizes the foundation model at the publication level and does not extend the dissertation's input domain to OCT (SB-1.4 in INVARIANTS.md remains in force). The composite independent variable, CFC-2.8, and the AOQ-1 through AOQ-4 open questions from v5.1 are unchanged.

## v5.1 Amendment Scope (historical)

Pretraining source amendment: integrated arm of Experiment 1 uses RETFound; baseline arm retains ImageNet. H-1 reformulated as Integrated Pipeline Dominance with composite independent variable. See INVARIANTS.md v5.1 Section X for open operational questions (AOQ-1 through AOQ-4).

## File Version Status

| File | Version | Synced |
|------|---------|--------|
| governance/INVARIANTS.md | 7.0.0 | ✅ — v7.0.0: H-7 reformulated (Section II) Clinical Degradation Resistance → External Clinical Performance; Δ_drop retired to descriptive; header summary added — completed 2026-08-04. v6.3.0: SB-2.4 relaxed + CFC-2.8 extended to admit SIP as a gate-selected integrated-arm init |
| governance/HYPOTHESIS.md | 7.1.0 | ✅ — v7.1.0: **H-3 restored** as Domain-Shift Reduction (K = 5 of n = 6, MMD primary, source-statistics protocol condition, label-reuse notice) — completed 2026-08-05. v7.0.0: H-7 reformulated (form S, MCID 0.050, CI⁻ > 0, both sets); Conclusion + Central-Hypothesis note synced. v6.2.0: Premise 4 + Conclusion RETFound→ophthalmology-SSL |
| governance/RESEARCH_ARCHITECTURE.md | 7.0.0 | ✅ — v7.0.0: §5.5 purpose + acceptance rewritten, §9.1 H-7 bullet, PC-10 row — completed 2026-08-04. v6.2.0: §4.2bis extended; §9.1 pretraining-leakage bullet |
| governance/CONTRIBUTIONS.md | 7.1.0 | ✅ — v7.1.0: **SC-I** added for the direct domain-distance measurement (H-3 restoration) — completed 2026-08-05. v7.0.0: SC-G reframed to external clinical performance + secondary methodological contribution (Δ_drop defect) — completed 2026-08-04. v6.3.0: SC-H generalized to "in-domain initialization (self-supervised OR supervised), gate-selected" — SIP admitted, SSL negative result recorded. v6.2.0: SC-H refined with locked SSL specifics; CFC-2.8 boundary unchanged |
| governance/VERSION_SYNC.md | 7.1.1 | ✅ — this document; v7.1.1 is the downstream-currency pass recorded above |
| governance/ARGUMENT_MAP.md | 7.1.0 | ✅ — v7.1.0: **PC-11** node (Domain-Shift Reduction, mechanistic) + DAG edge, depends on PC-1, feeds PC-6/PC-9/PC-10 explanatorily; magnitude-correspondence boundary — completed 2026-08-05. v7.0.0: PC-10 formal statement, SC-10.1, PC-10 strength criteria, DAG label and dependency note — completed 2026-08-04 |
| governance/CENTRAL_THESIS.md | 7.1.0 | ✅ — v7.1.1 sync: H-7 → external clinical performance; H-3 mechanism added to the substantiating evidence; **the clinical Grad-CAM overlays removed from the substantiation** (never produced, G-3 — H-5 is supported in its quantitative half only) |
| literature/external/gulshan-2016.md | v5.3 sync ✅ | ✅ — v5.3: §15 Paradigmatic Role block + §16 Paradigmatic citation-ready statements + §18 Paradigmatic Synthesis — completed 2026-05-28 |
| literature/external/pratt-2016.md | v5.3 sync ✅ | ✅ — v5.3: P1 position-in-paradigm-space line added to §15 |
| literature/external/rakhlin-2017.md | v5.3 sync ✅ | ✅ — v5.3: P1 position-in-paradigm-space line added to §15 |
| literature/external/saxena-2020.md | v5.3 sync ✅ | ✅ — v5.3: P1 position-in-paradigm-space line added to §15 |
| literature/external/ting-2017.md | v5.3 sync ✅ | ✅ — v5.3: P1 position-in-paradigm-space line added to §15 |
| literature/external/voets-2019.md | v5.3 sync ✅ | ✅ — v5.3: P1 position-in-paradigm-space line added to §15 |
| literature/LITERATURE_INDEX.md | 6.1.0 | ✅ — v6.1.0: corpus expanded 81 → 120 sources (#83–#121), incl. the ophthalmology-SSL / foundation-model family, fundus degradation & quality, and the missing cards for #46 Grad-CAM, #47 EyePACS, #48 Messidor; resolves the §1.2.1 and §2.3.3/§3.3.2 gaps. v5.3: Paradigm column added to the Source Index with the classification rule documented in Notes. **Open items:** DDR full-PDF upgrade; the `yesmukhamedov-scopus-q2` identifier mismatch |
| chapters/00-introduction/README.md | v5.3 spec ✅ | ✅ — Task 2.8 paradigmatic-framing block added |
| chapters/01-problem-domain/README.md | v5.3 spec ✅ | ✅ — Tasks 2.1–2.4 paradigmatic-framing block added (primary site for paradigmatic discussion) |
| chapters/02-theoretical-foundations/README.md | v5.3 spec ✅ | ✅ — v5.3 paradigmatic-framing note added |
| chapters/03-methodology/README.md | v5.3 spec ✅ | ✅ — Task 2.5 paradigmatic-framing block added |
| chapters/04-experiments/README.md | v5.3 spec ✅ | ✅ — Task 2.6 paradigmatic-framing block added (Experiment 1 A/C and B/D paradigmatic labelling) |
| chapters/05-validation/README.md | v5.3 spec ✅ | ✅ — Task 2.7 paradigmatic-framing block added (§5.5 caveat block for Gulshan numerical figures) |
| defense/slides/05a_PARADIGMATIC_POSITIONING.md | v5.3 ✅ NEW | ✅ — Task 3.1 new paradigmatic positioning slide created |
| defense/slides/44_NOVELTY.md | v5.3 ✅ | ✅ — Task 3.1.3 novelty slide updated with P1 → P2 framing |
| defense/slide_plan.md | v5.3 ✅ | ✅ — paradigmatic positioning slide registered in plan |
| defense/paradigmatic_speech.md | v5.3 ✅ NEW | ✅ — Task 3.3 defense speech + anticipated Q&A created |
| demo/src/tabs/Overview.js | v5.3 ✅ | ✅ — Task 3.2.1 paradigmatic context block added |
| demo/src/tabs/ExpH1.js | v5.3 ✅ | ✅ — Task 3.2.2 P1/P2 paradigm column added to factorial table |
| demo/src/i18n.js | v5.3 ✅ | ✅ — Task 3.2.3 paradigm.* keys added in EN and KZ |
| governance/CORE_OBJECTIVE.md | 7.1.0 | ✅ — v7.1.1 sync: H-7 → external clinical performance; H-3 measurement added; §0.3 named as the authoritative prose formulation |
| outline/MASTER_OUTLINE.md | 7.1.0 | ✅ — v7.1.1 sync: object-of-research category error; H-3 restored; H-7 reformulated; duplicated objective number; Novelty + Provisions lists marked **superseded by §0.2 / §0.8**. Remains a *structural* spec — the drafted sections win on content |
| outline/TABLE_OF_CONTENTS_EN.md | 7.1.0 | ✅ — verified: §4.4 (H-3) present; the Introduction ordering here is **authoritative for the manuscript** and differs from MASTER_OUTLINE's identifier ordering (see `chapters/00-introduction/README.md`) |
| outline/TABLE_OF_CONTENTS_KZ.md | 7.1.0 | ✅ — verified 2026-08-12: §4.4 (H-3) present with both sub-sections, §4.9 present, chapter structure mirrors the EN TOC |
| glossary/GLOSSARY_EN.md | 7.0.0 | ✅ — v7.0.0: H-7 entry renamed and redefined to External Clinical Performance, **MCID** added as an operational term, "Clinical Degradation Resistance" and "Δ_drop" moved to Deprecated Terms with Superseded-By pointers, Messidor-2 entry corrected — completed 2026-08-04. v6.2.0: Linear-Probe Acceptance Gate + Fundus-SSL Pretraining Corpus terms added; SSL-Method-Family (BYOL primary) and Ophthalmology-SSL refined |
| glossary/GLOSSARY_KZ.md | 7.0.0 | ✅ — v7.0.0: Kazakh mirror of the H-7 rename, the MCID entry and the two deprecations — completed 2026-08-04. v6.2.0: Kazakh equivalents mirrored for the new/refined SSL terms |
| experiments/experimental-protocol.md | 5.0 | ❌ — v6.0.0: Exp 1 protocol must reflect the restored A/B/C/D factorial (integrated arm = ophthalmology-SSL); AOQ-1/3/4 resolved, AOQ-2 simplified |
| methods/preprocessing-pipeline.md | 6.1.0 (Stage 1) | ✅ — v6.1.0: Stage-1 description updated to the frozen learned heatmap detector (σ = 15.0°); other stages still pending the v6.0.0 pretrain-reference review |
| methods/implementation.md | 5.0 | ❌ — v6.0.0: model loading code paths must load an in-house ophthalmology-SSL CNN checkpoint (no RETFound/ViT-Large loader needed) |

## Downstream Code Status (not part of governance, listed for completeness)

| Path | Sync status |
|------|-------------|
| experiments/configs/default.yaml | Out of sync — integrated-arm config must point at an in-house ophthalmology-SSL CNN checkpoint (not ImageNet, not RETFound) |
| experiments/src/models/factory.py | Out of sync — needs an SSL-pretrained-CNN checkpoint loader for the integrated arm |
| experiments/src/models/resnet.py | In sync re: backbone (AOQ-1 resolved to option (b) — CNN unchanged); only the init-weights source changes |
| experiments/src/models/efficientnet.py | In sync re: backbone (AOQ-1 resolved to option (b) — CNN unchanged); only the init-weights source changes |
| demo/src/tabs/ModelArchitecture.js | ✅ Synced 2026-06-01 (v6.0.0) — integrated-arm row + note now ophthalmology-specific SSL on ResNet-50/EfficientNet-B3 (configs B/D); RETFound removed |
| defense/slides/08_CNN_ARCHITECTURE.md | ✅ Synced 2026-06-01 (v6.0.0) — bullet → ophthalmology-SSL; AOQ-1 note replaced with "symmetry restored" |
| defense/slides/09_ARCHITECTURE_COMPARISON.md | ✅ Synced 2026-06-01 (v6.0.0) — factorial table restored to A/B/C/D; B′ retired; Factor 2 + speech → SSL |
| defense/paradigmatic_speech.md | ✅ Synced 2026-06-01 (v6.0.0) — Gulshan caveat pretraining-source line → ImageNet / ophthalmology-SSL |
| thesis/chapters/01-problem-domain/README.md | ✅ Synced 2026-06-01 (v6.0.0) — §1.3.2 in-domain-pretraining contrast → ophthalmology-SSL (RETFound demoted to related work) |
| thesis/chapters/05-validation/README.md | ✅ Synced 2026-06-01 (v6.0.0) — Gulshan caveat-block pretraining-source item → ophthalmology-SSL |
| thesis/literature/external/gulshan-2016.md | ✅ Synced 2026-06-01 (v6.0.0) — § unsound-comparison pretraining-source line → ophthalmology-SSL (separate from the still-pending Paradigmatic Role block) |

Version history: v5.1 (2026-05-14) adopted RETFound for the integrated arm; v5.2 (2026-05-28) refined the RETFound corpus to multi-modal CFP + OCT; v5.3 (2026-05-28) introduced the paradigmatic framing (P1 / P2; Gulshan as canonical representative of P1). **v6.0.0 (2026-06-01) reverses the RETFound adoption** in favour of ophthalmology-specific self-supervised pretraining of the existing CNN backbones (MAJOR bump). The dependent governance and downstream files marked ❌/Out-of-sync above must be brought to v6.0.0 in subsequent passes; once governance is stable, the version-marker scan (VERSIONING_POLICY.md §6) enforces version containment outside `thesis/`.

**Note — Config-D naming divergence:** the *shipped* demo/training artifact "Config D" is the retired ImageNet pipeline (EfficientNet-B3 + ImageNet); governance **Config D** is now full pipeline + EfficientNet-B3 + ophthalmology-SSL. These must not be silently merged — the shipped demo predates this amendment.

## Sync Protocol

Before any chapter-writing session:
1. Verify all governance files marked ✅ are at the **v7.x** line (INVARIANTS v7.0.0 / HYPOTHESIS v7.1.0 /
   ARGUMENT_MAP v7.1.0 are the current authoritative versions).
2. Files marked ❌ must not be cited as authoritative until brought to the v7.x line.
2a. **The drafted dissertation sections now outrank the planning documents on content.** §0.3 is the
   authoritative goal, §0.5 the object and subject, §0.6 the hypothesis register in prose, §0.2 the novelty,
   §0.8 the provisions with their fences, and §7 the conclusion. `MASTER_OUTLINE.md` remains authoritative
   for *structure* only.
3. AOQ-1/AOQ-3/AOQ-4 are resolved and AOQ-2 simplified in v6.0.0 (INVARIANTS Section X); the integrated arm uses ophthalmology-specific SSL on the existing CNN backbones.
4. The v5.3 paradigmatic-framing constraints (SB-1.12, CFC-2.9, SIR-9) remain binding on every chapter, slide, and demo update.
5. After any governance update, re-verify dependent files.
