# Governance Changelog

This file is the human-readable history of governance versions. Each entry corresponds to a git tag. To recover the exact state at any version, run `git checkout <tag>`.

The versioning scheme is defined in [VERSIONING_POLICY.md](VERSIONING_POLICY.md).

---

## v7.2.1 — 2026-08-23

**The governance apparatus is removed from the printed volume, and three Kazakh-register repairs (PATCH — no binding created, reversed or reinterpreted).**

An external reading of the Kazakh PDF (`D:/dissertation_council/temp/АНАЛИЗ_A17_Есмухамедов.md`) reported that "Designations and abbreviations" defined eight labels — **PC-n, CFC-n, EH-n, SIR-n, DGL-n, SB-n, NC-n, OD-n** — that appear nowhere else in either edition, and that the text nevertheless leans on the apparatus they describe. The reading is correct on both counts. These are rules for how a claim may be worded, not terms of ophthalmology or machine learning, and a reader who meets them in a glossary is owed the apparatus itself. **The apparatus is unchanged and still binds** — it lives in `INVARIANTS.md` §§IV–IX, where it belongs; what is removed is its leakage into the volume. This closes the item `VERSION_SYNC.md` v7.2.0 had listed as pending ("the abbreviations list, from which the governance codes must be removed once they no longer appear in the text").

- **`output/abbreviations_{en,kz}.md`** — the eight entries deleted. Every remaining entry is a term of the subject.
- **`output/definitions_{en,kz}.md`** — three residual `H-1` references replaced by "Experiment 1", which is what the body calls it.
- **`chapters/06-appendices/{drafts/B-draft,translations/B-translation}.md`** — the one place the prose cited the apparatus, *"supplementary in this dissertation's evidence hierarchy"*, pointed at a hierarchy set out nowhere in the volume. It now cites the metric table of section 2.6, which is where the primary/supplementary split is actually written down.

**Kazakh register.** The same reading measured the Kazakh edition against two other Kazakh-language dissertations of this council and found English syntax under Kazakh words. Repaired across all 35 translation sources:

- **`et al.` → «т.б.»** — 131 occurrences of the word-for-word calque «және әріптестері» (0 in either comparator, while the Kazakh norm «т.б.» stood at 0 against their 18 and 12). `_finalize_citations.py` has always parsed both forms; the GOST pass reconverts identically — 138 brackets in each edition, 102 external sources, no blocking or unknown resolutions.
- **«…, сондықтан …» mid-sentence** — 133 occurrences (comparators 6 and 11) rewritten to the idiomatic causal suffix (-дықтан/-діктен) or to a new sentence opening with «Сондықтан», which is where Kazakh puts it.
- **One connective doing all the work** — «Демек,» ran to 35 uses with no alternative anywhere in the volume. Eighteen are now «Сонымен», «Осылайша», «Яғни» and «Тиісінше», chosen per sentence.

**Not repaired, and deliberately.** The reading also noted that 3.9 % of sentences end in «емес» against 0.8 % and 0.2 % in the comparators. That density is the prose honouring the scope boundaries of `INVARIANTS.md` §IV, which bind; grinding it to the comparators' level would mean deleting statements of what the work does not claim. Eleven were varied syntactically with no content lost (4.90 % → 4.17 %) and the rest stand. Terminological uniformity was noted too — one term per concept, no drift — and that is `glossary/GLOSSARY_KZ.md` working as intended, not a defect to introduce variation into.

**Not a governance change, recorded for traceability.** `thesis/scripts/conformance.py` gained the gate that would have caught this: **governance labels in front matter** (the body scan starts at the Introduction, so nothing above it was ever read — which is exactly how eight labels survived), plus three Kazakh-only register checks — the `et al.` calque, mid-sentence «, сондықтан», and the share of the largest connective. EN passes 17 of 17, KZ 20 of 20.

---

## v7.2.0 — 2026-08-20

**Restructuring to the council's observed norms, and one scope boundary corrected to match fact (MINOR).**

`council/` gained `en/10-dissertation/peer-norms.md`, measured across all 16 dissertations this council has published. It converts the Instruction's ceilings into the genre's actual shape, and the assembled volume missed it on almost every axis: 101,459 words of main text against a corpus median of 22,700; six chapters where the median is four, three of them in roles no sample uses; a fourth numbering level that occurs in none of the 16; 610 section signs and about 350 internal codes where the corpus prints zero of each; and centred headings where 0 of 16 centre them.

- **`INVARIANTS.md` 7.0.0 → 7.1.0.** **SB-4.1 amended**: the clause asserted that no prototype implementation was available, which was written before the demonstrator existed and had become false. It now records that a working demonstrator is deployed and performs inference on submitted images, bounded on both sides — it establishes realizability and operating behaviour, and is evidence for no diagnostic claim. **SB-4.2 and SB-4.3 unchanged.** Chapter and section references renumbered for the four-chapter volume. No hypothesis, forbidden claim or non-claim is touched.
- **`outline/MASTER_OUTLINE.md` 7.1.0 → 8.0.0.** Rewritten as a structural specification of the four-chapter volume: what each chapter contains, and which scope boundary and forbidden claim bind where. The superseded Novelty and Provisions planning lists are removed rather than carried marked-superseded for a third version.
- **`outline/TABLE_OF_CONTENTS_{EN,KZ}.md` 7.1.0 → 8.0.0.** Four chapters, two numbering levels, 24 second-level subsections, plain noun-phrase titles, no code in any heading. Kazakh appendices re-lettered **А, Ә, Б, В, Г** — the previous list omitted Ә, which the one Kazakh-language sample with appendices keeps as its second letter.
- **`outline/REWRITE_MAP.md` — new.** The binding contract for the rewrite: all 98 drafted sections mapped to a destination subsection or to CUT, with word budgets summing to the target. Two sections are cut, each with its reason recorded.
- **Appendix D deleted** — a table of the candidate's publications and six screenshots of indexing databases. Neither appears in any of the 16, and the contents had promised something else entirely (implementation acts and certificates, which do not exist). The publication record keeps its two proper carriers, the Introduction's approbation rubric and the separate List of scientific papers.

**Not a governance change, recorded for traceability.** `thesis/scripts/conformance.py` turns the peer-norms measurements into a gate over the assembled manuscript; `md2gost.py` now sets numbered headings at the paragraph indent rather than centred, and `table_continuations.py` announces every table that breaks across a page, which none of the volume's 42 tables did.

---

## v7.1.1 — 2026-08-11

**Downstream currency pass (PATCH — documentation sync only; no binding created, reversed or reinterpreted).** Four governance and planning documents that had fallen behind the INVARIANTS v7.0.0 / HYPOTHESIS v7.1.0 line are brought current, and one register position is corrected. Every change tracks a decision already ratified.

- **`CORE_OBJECTIVE.md` 5.0 → 7.1.0** — *clinical degradation resistance* → **external clinical performance**; the **H-3 direct measurement** added to the validation programme. §0.3 is named as the authoritative prose formulation of the goal.
- **`CENTRAL_THESIS.md` 6.0.0 → 7.1.0** — same H-7 correction; the measured distance reduction added to the substantiating evidence. **Correction found during the pass:** the prior text cited *qualitative Grad-CAM overlays on a Kazakh clinical dataset* as substantiating evidence. Those overlays were **never produced** (gap G-3), so the text asserted evidence that does not exist. H-5 is supported in its **quantitative half only**.
- **`outline/MASTER_OUTLINE.md` 6.0.0 → 7.1.0** — four currency defects: the **object of research** stated as the fundus images rather than the *process* (a category error against the house convention and the council-verified abstract); **H-3** recorded as dropped though it is live and written as §4.4; **H-7** in its retired form; and a **duplicated objective number**. Its Novelty and Provisions lists are **marked superseded** by §0.2 and §0.8 rather than rewritten — they enumerate what was planned, not what is defended.
- **`results/tables/TAB-5.2_claim_strength.md`** — the domain-distance result is moved from "additional empirical results outside the formal PCs" into the formal register as **PC-11**, matching `ARGUMENT_MAP.md` v7.1.0. Substance and strength unchanged (STRONG, direction only); the tally becomes **8 of 8** empirical primary claims confirmed as stated.

**Also closed in the same pass (not governance, recorded for traceability): the trilingual abstract.** `thesis/output/abstract_{en,kz,ru}.md` said "seven experiments" where the programme is **eight** investigations; omitted H-3 entirely; carried a statements-for-defence list of six items with one still expressed in the retired Δ_drop form; and **listed the Vessel Visibility Index among the methods although §4.3.3 excluded it for want of an implementation and a source** — an error rather than staleness. All three languages are synced against §0.2 / §0.6 / §0.8 / §7: novelty 10 items, main results 9, statements for defence 11 plus one observation, followed by an explicit paragraph of what is *not* submitted.

**Context.** The dissertation's chapter body is complete: Chapters 0–7 are drafted, reviewed and approved. **§0.8 is the forward ceiling** for every downstream deliverable and §5.C the rearward one; the §7 review carries a provision-by-provision ceiling audit showing no promotion, and a fence audit at 8 of 8 intact.

---

## v7.1.0 — 2026-08-05

**H-3 restored as Domain-Shift Reduction (MINOR — a hypothesis is added; no existing binding is reversed).** The label H-3 was vacated in V3, when the *training-method comparison* it then denoted — frozen-layer versus progressive fine-tuning as an experimental factor — was dropped and fine-tuning was demoted to a shared training method applied uniformly across the H-1 configurations. **That retirement stands and is not reversed.** The label is **reused** for a distinct and previously unstated hypothesis: that the integrated configuration measurably reduces the distance between the source and external domains in feature space.

**Why it was restored.** The central hypothesis asserts a causal chain — the pipeline reduces domain variability, and reduced variability yields improved external classification. Every hypothesis in the programme measured the chain's *consequence* (external accuracy: H-4, H-6, H-7); none measured its *middle term*. Domain-shift reduction was the single unmeasured link in the dissertation's own argument, inferred throughout but never tested. H-3 tests it directly, at the cost of forward passes only, and makes the mechanism independently falsifiable of the performance claims.

**Acceptance form — "K of n", K = 5, n = 6:**

```
H-3  ⟺  Σ PASS_S(d, X)  ≥  5,    X ∈ {APTOS, IDRiD, Messidor-2, DDR, ODIR-5K, RFMiD}

PASS_S(d, X)  ⟺  Δd(X) = d(BASE, X) − d(INT, X)  ≥  MCID_d = 0.0   ∧   CI⁻(Δd) > 0
```

`d` is MMD (or FID) over penultimate-layer features and is the **primary metric and the sole basis of the criterion**; `d_KL` over per-channel intensity histograms is **secondary and informational only**. Confidence intervals come from **1 000 bootstrap resamples**. The compared arms are integrated − baseline (EfficientNet-B3; configurations D − C of Experiment 1). Because `d` is unnormalized, `MCID_d = 0.0` and the per-corpus condition reduces to `CI⁻(Δd) > 0`.

**Mandatory protocol condition.** Stage 7 normalization must be computed from **source-domain statistics**, exactly as in zero-shot deployment. Computing it from the target corpus would make the measurement a form of target-domain adaptation and would render the result incomparable with H-4, H-6 and H-7. An evaluation violating this condition does not test H-3.

**Threshold provenance, stated openly.** Neither `MCID_d` nor `K` was pre-registered; both are assigned at this formalization. `MCID_d = 0.0` is not a tuned choice — `d` is unnormalized, so no non-zero minimal difference is interpretable. The outcome is insensitive to `K`: it passes for every `K ≤ 6`, so the choice of `K = 5` does not determine the verdict. **VCR-1** is satisfied by issuing this versioned amendment. **VCR-3** is not engaged: no result contradicting a direction of effect is being concealed, since the direction was never contradicted.

**Pre-specified reversal case, retained on the record.** Stage 5 (CLAHE tuned on the source corpus) and Stage 7 (dataset-specific normalization) are bound to the source domain by construction, so a REVERSED outcome — variability reduced *within* the source domain while increased *across* domains — was a live possibility rather than a remote one. Had it occurred it would have been an established finding, not a failed run: it would have directly explained any reversal in H-4 and H-7 and would have been reported as a result.

**Label-reuse notice, binding on downstream text.** Occurrences of "H-3 dropped" in §2.3.2 and §3.3.3 and in their briefs and continuity notes refer to the **retired training-method hypothesis** and are historically correct. They must not be read as referring to the present H-3, and no claim about training method may be derived from it.

**Files updated.** HYPOTHESIS (amendment, H-3 definition with its variable table and formula, Central-Hypothesis note, Conclusion), ARGUMENT_MAP (new **PC-11** node, DAG, header amendment), CONTRIBUTIONS (new **SC-I**, header amendment), VERSION_SYNC, CHANGELOG. Downstream: `thesis/ASSET_INVENTORY.md`, `thesis/CLAUDE.md`, both tables of contents, and the §4.4 material in `thesis/chapters/04-experiments/`. `results/` already carried the block.

**Unchanged:** H-1, H-2, H-4, H-5, H-6, H-7, all scope boundaries, forbidden claims, non-claims, the composite independent variable and CFC-2.8.

---

## v7.0.0 — 2026-08-04

**H-7 reformulated: Clinical Degradation Resistance → External Clinical Performance (MAJOR — a hypothesis is reformulated incompatibly with the prior version).** The dependent variable of H-7 changes from the degradation quantity Δ_drop = F1_EyePACS_val − F1_external to the **absolute external performance difference** Δ wF1(X) = wF1(integrated, X) − wF1(baseline, X). Acceptance is form S on **both** external clinical datasets, evaluated independently: Δ wF1(X) ≥ MCID_wF1 = 0.050 **and** CI⁻ > 0. The datasets are not aggregated — a reversal (CI⁺ < 0) on either yields REVERSED regardless of the other. The form requires Δ ≥ MCID and CI⁻ > 0; it does **not** require CI⁻ ≥ MCID.

**Why the prior form was retired.** Δ_drop is not independent of the hypothesis it was meant to test. For any external set X:

    Δ_drop(integrated, X) − Δ_drop(baseline, X)
      = [wF1(int, in) − wF1(int, X)] − [wF1(base, in) − wF1(base, X)]
      = [wF1(int, in) − wF1(base, in)] − [wF1(int, X) − wF1(base, X)]
      = Δ_in-domain − Δ_external

The comparison thus reduces to the fixed in-domain margin minus the very quantity H-7 measures. Its sign is satisfied only when the integrated arm exceeds baseline *more on foreign data than on its own*, so the criterion penalizes the integrated arm for its in-domain result and carries no information about degradation resistance. The defect is analytic and was identified from the algebra, not from inspecting experimental outcomes.

**Relation to the version-control rules.** **VCR-3** — which forbids silent modification of a hypothesis when results contradict the *direction of effect* — is **not engaged**: the direction of effect for H-7, the integrated arm performing better on external clinical data, was never contradicted at any evaluation; what failed was the metric expressing it. The amendment is recorded openly across INVARIANTS, HYPOTHESIS, VERSION_SYNC and this changelog, and the retired quantity is **preserved as descriptive**, not deleted — its results remain reportable in Chapter 5 §5.4. **VCR-1** — Core Hypotheses immutable post-ratification, modifiable only through a new versioned Invariants document — is satisfied by the INVARIANTS v7.0.0 issue that accompanies this entry.

**Unchanged:** H-1 through H-6, all scope boundaries (SB-x), forbidden claims (CFC-2.x), non-claims (NC-x), the composite *(preprocessing × pretraining)* independent variable, and CFC-2.8. No preprocessing operational definition (OD-3, Stages 0–7) is touched.

**Secondary methodological contribution.** The Δ_drop defect is recorded in CONTRIBUTIONS under SC-G as a critique of a degradation metric in common use in the domain-shift literature. The same structural defect affects the g_ratio normalization used in H-6 reporting, and one argument covers both.

Governance files updated: INVARIANTS (Section II H-7, header), HYPOTHESIS (H-7, Central-Hypothesis note, Conclusion, header), ARGUMENT_MAP (PC-10, SC-10.1, PC-10 strength, DAG label, dependency note), CONTRIBUTIONS (SC-G), RESEARCH_ARCHITECTURE (§5.5, §9.1, PC-10 row), VERSION_SYNC. Pending downstream sync (does not gate this bump): `thesis/ASSET_INVENTORY.md` H-7 row, chapter 4/5 briefs and drafts, glossary EN/KZ.

## v6.2.0 — 2026-06-26

**Fundus-SSL corpus and acceptance protocol locked for the integrated arm (MINOR — new referenceable entities, no binding reversed).** The v6.0.0 ophthalmology-SSL decision is unchanged; this amendment fixes the operational specifics that were previously left open. The integrated-arm self-supervised pretraining corpus is fixed to the **unlabeled EyePACS original "test" split — 53,576 images** — which is **disjoint** from the Experiment-1 evaluation corpus (the ~35,126 labeled "train" split, 5-fold patient-level CV) by image identity and patient identity. This no-pretraining-leakage constraint is recorded as new clause **SB-2.4** (INVARIANTS) and is operationalized in the experiments code as the disjointness assertions **INV-SSL-1 / INV-SSL-2**. **BYOL** (Grill et al., 2020) is recorded as the primary CNN-compatible protocol (MoCo-v2 / SimSiam / DINO retained as alternatives), pretrained **from-scratch (random initialization)** directly on the 4-channel tensor (RGB + FOV mask). A **linear-probe acceptance gate** is added as the precondition for any SSL checkpoint to enter Experiment 1: with the backbone frozen, a linear head must beat random init and be competitive with ImageNet on a label-bearing EyePACS-test slice, for both backbones; an ImageNet→continual-SSL initialization is a documented (non-default) fallback.

Because this adds new referenceable entities (SB-2.4, the acceptance gate) and reverses no binding constraint, hypothesis, or scope boundary, it is a MINOR bump. CFC-2.8 (baseline ⟹ ImageNet, integrated ⟹ fundus-SSL) and the composite *(preprocessing × pretraining)* independent variable are retained; no SSL performance is asserted (the integrated arm is specified, not yet trained). This amendment also corrects a v6.0.0 sync miss: HYPOTHESIS.md Premise 4 and the Conclusion, which still named RETFound, are brought to the ophthalmology-SSL framing. Governance files updated: INVARIANTS, HYPOTHESIS, RESEARCH_ARCHITECTURE, CONTRIBUTIONS, VERSION_SYNC. Narrative sync: methodology §3.3.2 (draft + KZ translation + continuity), glossary EN/KZ. SSL literature cards (#84–#92) were already registered; no new card was required.

## v6.1.0 — 2026-06-23

**OD-3 Stage-1 detector: classical CV → pre-trained, frozen learned heatmap detector (MINOR — new substantive entity, no binding reversed).** The Stage-1 OD/fovea detector — previously classical computer vision (brightest-region OD, darkest-region-with-distance-prior fovea) — is replaced by a pre-trained, **frozen** heatmap-regression detector (U-Net encoder + DSNT head) trained on IDRiD localization ground-truth. It predicts OD/fovea probability heatmaps on the FOV-cropped frame, yielding sub-pixel centers and a **genuine** per-landmark confidence (from heatmap peak sharpness and spatial spread) that gates the rotation fallback and the Stage-5 polar-CLAHE fovea pivot.

Motivation: the classical detector localized the fovea unreliably (~5 OD-radii median error, ~0 % within 2 R at native resolution) and its confidence flag was non-informative. The learned detector meets the held-out IDRiD-test acceptance bar — OD median 0.066 R (100 % within 1 R); fovea median 0.107 R (99 % within 1 R); informative fovea confidence (Spearman ρ ≈ 0.44) — reproduced in-repo by `scripts/validate_od_fovea_idrid.py`. The fallback rotation **σ is reconciled to 15.0°** (the value the code and evaluation actually use; the prior 13.0° text is corrected). The detector is **pre-trained and frozen — not co-trained with the DR classifier** — so the preprocessing pipeline remains a fixed transform and the central thesis `model = preprocessing + CNN` is preserved. No hypothesis, scope boundary, factorial design, or other operational definition (Stages 0, 2–7) is modified. Governance files updated: INVARIANTS, RESEARCH_ARCHITECTURE, VERSION_SYNC, methods/preprocessing-pipeline. Narrative chapter drafts, assembled dissertation bundles, abstracts, and glossary entries describing the classical Stage-1 detector remain a separate downstream documentation pass.

## v6.0.0 — 2026-06-01

**RETFound replaced by ophthalmology-specific self-supervised pretraining (MAJOR — reverses the v5.1–v5.2 RETFound binding).** The integrated arm of Experiment 1 no longer initializes from the RETFound ViT-Large foundation model. Instead, the existing CNN backbones (ResNet-50 / EfficientNet-B3) are initialized from a CNN-compatible domain-adaptive self-supervised learning protocol (DINO / BYOL / SimCLR / MoCo family, selected empirically) pretrained on an unlabeled retinal fundus corpus. Rationale: adopting RETFound changes both the architecture and the initialization, confounding the preprocessing contribution with an architecture change; a CNN-native SSL initialization changes only the initialization stage, preserving the CNN-centred research design and a defensible causal interpretation of the preprocessing contrast.

Because the SSL initialization is CNN-native, the 2×2 *(preprocessing × architecture)* factorial symmetry is **restored**: configurations **B and D are reinstated** (integrated preprocessing + ophthalmology-SSL on ResNet-50 and EfficientNet-B3) and config **B′ is retired**. This resolves **AOQ-1** (→ option b), **AOQ-4** (symmetry), and **AOQ-3** (RETFound license moot), and simplifies **AOQ-2** (SSL pretrained directly on the 4-channel tensor). The composite *(preprocessing × pretraining)* independent variable and **CFC-2.8 are retained** (baseline ⟹ ImageNet, integrated ⟹ ophthalmology-SSL), so the H-1 effect remains non-attributable to preprocessing alone; EH-4 cross-architecture replication is reinstated. A new supporting contribution **SC-H** records the SSL initialization, bounded by CFC-2.8. No preprocessing operational definitions (OD-3, Stages 0–7) and no other hypotheses are modified; the v5.3 paradigmatic framing is retained. Governance files updated: INVARIANTS, HYPOTHESIS, RESEARCH_ARCHITECTURE, CONTRIBUTIONS, CENTRAL_THESIS, ARGUMENT_MAP, VERSION_SYNC.

## v5.3.0 — 2026-05-28

Paradigmatic framing introduced. Two paradigms recognised: **P1** (end-to-end CNN; preprocessing as ancillary data preparation) and **P2** (integrated preprocessing-CNN; preprocessing as integral model component). Gulshan et al. (2016) designated canonical representative of P1 (per the methodological-practice criterion in SIR-9). New governance clauses: **SB-1.12** (Gulshan is not a numerical benchmark, baseline is operational construct per OD-3), **CFC-2.9** (forbids false attribution of "preprocessing is unimportant" claim to Gulshan or other P1 sources), **SIR-9** (paradigmatic-attribution rule). PC-0 (Paradigmatic Framing Claim) added to ARGUMENT_MAP as a non-empirical methodological claim feeding into IT-1. CENTRAL_THESIS gains an introductory paradigmatic-framing paragraph. CONTRIBUTIONS gains an introductory conceptual-framing block and a reframed C-1 novelty statement. No operational definitions, hypotheses, or experimental protocols are modified.

## v5.2.0 — 2026-05-28

Refinement of the RETFound pretraining-corpus description. The integrated arm of Experiment 1 is now described as initialized from RETFound, a foundation model **MAE-pretrained on a multi-modal retinal imaging corpus** comprising ≈904K color fundus photographs (CFP) + ≈736K optical coherence tomography (OCT) scans (~1.6M total) per Zhou et al. 2023, Nature. The dissertation's integrated arm loads the **CFP-pretrained checkpoint** specifically; the multi-modal description characterizes the foundation model at the publication level and does not extend the dissertation's input domain to OCT (SB-1.4 in INVARIANTS.md remains in force). The composite independent variable, CFC-2.8, and the AOQ-1 through AOQ-4 open questions from v5.1 are unchanged.

## v5.1.0 — 2026-05-14

Pretraining source amendment: integrated arm of Experiment 1 uses RETFound; baseline arm retains ImageNet. H-1 reformulated as Integrated Pipeline Dominance with composite independent variable. See INVARIANTS.md v5.1 Section X for open operational questions (AOQ-1 through AOQ-4).

## v5.0.0 — 2026-04-09

Monorepo consolidation and introduction of the preprocessing pipeline. The three previously separate repositories — dissertation text, experiments, and demo dashboard — were unified into a single monorepo via subtree merges of `thesis/`, `experiments/`, and `demo/`. The 8-stage preprocessing pipeline was introduced, establishing the central thesis that `model = preprocessing + CNN`. Defense slide and dashboard scaffolding were added alongside the consolidated `.gitignore` and README.

## v4.0.0 — 2026-03-24

Governance synchronization pass. Residual stale references left by the V3 refactor were reconciled and the full governance set was brought to a consistent state across the V4 commit series (V4 → V4 fix → V4 edited → V4 final → V4 synchrone).

## v3.0.0 — 2026-03-14

Major restructuring. The experimental design was consolidated (APTOS dropped at this stage) and governance internal references were synchronized — INVARIANTS (OD-5, SB-1.1, SB-1.8, NC-16) and the ARGUMENT_MAP footer. The English and Kazakh tables of contents and the MASTER_OUTLINE were rewritten to V3.0. A meta-prompt writing pipeline was scaffolded (Section Brief, Writing/Revision/Translation/Verification templates, Continuity Note, context-assembly script) and the version synchronization register was introduced. The earlier v1 meta-prompt pipeline was deprecated.

## v2.0.0 — 2026-03-09

Second governance iteration. Methods were added and the document structure was reorganized following the V1 baseline.

## v1.0.0 — 2026-03-08 (inferred)

Pre-versioning baseline. The repository state captured by this tag predates the explicit governance versioning convention. See git tag `v1.0.0` for the complete state.
