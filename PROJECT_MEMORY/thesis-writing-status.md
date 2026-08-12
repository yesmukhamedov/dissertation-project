---
name: thesis-writing-status
description: "Dissertation COMPLETE and EXPORTED — 98 sections EN + 98 KZ, citations done, assets closed, council-ready GOST docx+pdf built 2026-08-13. Remaining: governance-code decision (356 codes), trim queue, stale abstract/TOC exports, NEW-1 traceability, §2.1.2 locators"
metadata:
  type: project
---

Consolidates the former `phase1-writing-complete` + `chapter3-methodology-drafted` memories. Live tracker is `thesis/PLAN.md`; supervisor role/protocol in `SUPERVISOR_HANDOFF.md` (kept current). Trust real files (drafts/ + reviews/ §H verdict), not tracker checkboxes — the executor (separate chat) writes faster than PLAN.md updates.

## Phase 1 COMPLETE (2026-06-10)

All writable-now sections drafted and APPROVED on disk (each with brief/draft/continuity/review):
- **Ch 1** Problem Domain — 11/11 ✅
- **Ch 2** Theoretical Foundations — **14/14 ✅ COMPLETE** (2026-06-16). **§2.3.3** in-domain SSL DRAFTED & APPROVED 2026-06-16 (deferral lifted: SSL-on-fundus corpus #84–#92 now present; brief/draft/continuity/review saved; DGL-6 + CFC-2.8 composite-IV; CNN-vs-ViT nuance; CNN-native-on-4ch-V5 kept spec-not-result → §3.3.2/§4.2). **§2.4.2 was consolidated into §2.4.1** (phantom TOC/outline entry removed 2026-06-16; the earlier "14/15" wrongly assumed §2.4.2 existed). Ch 2 = 14 numbered subsections + §2.C, all drafted. See [[thesis-assembly]].
- **Ch 3** Methodology — 13/13 ✅
- **Ch 6** System Architecture — 9/9 ✅ (committed 4b6898f, 04fa027; §6.1.2 carries deferred DIA-6.3 UML placeholder)
- **§4.1** Datasets & Configuration — 3/3 ✅ (commit 71723a5)
- **App A** (preprocessing source code) + **App D** (certificates & publications) ✅ — under `thesis/chapters/08-appendices/`

## Phase 2 — Ch 4 and Ch 5 COMPLETE

The experiment gate is closed: all seven experiments ran, all seven hypotheses are supported, and the
experimental chapters are written from `results/` (the single source of truth for every number).

- **Ch 4** Experiments — **20/20 ✅** (§4.1.1–§4.C). H-3 reinstated as its own **§4.4**; Exp 3–7 shifted to §4.5–§4.9.
- **Ch 5** Reliability Validation — **7/7 ✅** (§5.1, §5.2.1, §5.2.2, §5.3.1, §5.3.2, §5.4, §5.C).
  **TAB-5.3 was assembled inside §5.3.1 from the literature cards** — it was never an experiment gate.

**The eight fences that bind everything downstream (Ch 0 §0.8, Ch 7, defence, demo)** — compression is
where they get lost, so restate them, never paraphrase them upward:
CFC-2.8 (the composite is **decomposable, not dissolved** — the ablation under one initialization
reproduces the whole in-domain gain, but B/D remain differently initialized); PC-8 at **grouping
resolution only**; H-3 **direction only** (ρ ≈ 0.49 — magnitude does not track transfer gain); H-5
**quantitative half only** (G-3: clinical overlays never produced); H-7 **performance, not resistance**,
Messidor-2 margin **0.0041** with CI⁻ below the MCID; H-4/H-6 thresholds cleared by **both** arms;
E-7 **comparable, not larger** than the abundant-data gain; two camera groupings are the external
corpora themselves, so not independent replication.

**Two Chapter-5 items worth carrying as contributions/limits:** (1) the **normalization defect** —
generalization ratio, retired Δ_drop form and retention ratio all normalize external performance
against an arm's *own* in-domain performance, so each penalizes in-domain strength;
`Δ_drop(D) − Δ_drop(C) ≡ Δ_in-domain − Δ_external` makes it exact. Stated in §5.4 as a **secondary
methodological contribution, strictly descriptive — it rehabilitates no result**. (2) **Inference
uncertainty is understated outside Exp 1**: only Exp 1 has fold-level replication, so Exp 3–6
intervals quantify evaluation-corpus sampling alone, and Holm correction is scoped to Exp 1 —
**no dissertation-wide error rate is claimed**.

## Sync + repair pass, 2026-08-11 — three items closed

**1. Trilingual abstract synced** (`thesis/output/abstract_{en,kz,ru}.md`, all three now 153 lines, parallel).
Four defects closed: "seven experiments" → **eight investigations**; **H-3 added** as objective, novelty item,
result and provision; statements-for-defence **6 → 11 provisions + one observation + an explicit non-claims
paragraph**, each provision carrying its fence, with the retired Δ_drop item replaced by the External Clinical
Performance form; and **VVI removed from the methods** — §4.3.3 excluded it for want of an implementation and
a source, so that one was an *error*, not staleness. Also corrected in the same pass: SC-H stated as fundus-SSL
→ gate-selected in-domain initialisation (v6.3.0 generalisation, with the negative gate result reported);
the Messidor-2 tier label "clinical degradation"; the reliability section now carries the pre-specification
argument, placement-not-ranking **with its reason**, and both aggregate concessions.

**2. Governance synced → VERSION_SYNC v7.1.1 / CHANGELOG entry (PATCH, no new binding).**
`CORE_OBJECTIVE.md` 5.0→7.1.0 and `CENTRAL_THESIS.md` 6.0.0→7.1.0 (H-7 form; H-3 added).
`MASTER_OUTLINE.md` 6.0.0→7.1.0 — four currency defects: **object of research stated as the images rather
than the process** (category error), H-3 recorded as dropped, H-7 in its retired form, and a **duplicated
objective number**; its Novelty and Provisions lists are **marked superseded by §0.2 / §0.8** rather than
rewritten. `TAB-5.2` — domain distance moved from "outside the formal PCs" into the register as **PC-11**,
matching ARGUMENT_MAP v7.1.0; tally becomes **8 of 8** empirical primary claims.
**Two further errors found during the pass:** CENTRAL_THESIS cited *qualitative Grad-CAM overlays on the
Kazakh clinical dataset* as substantiating evidence — they were **never produced** (G-3), so the text asserted
evidence that does not exist; and `abbreviations_{en,kz}.md` expanded **ALO as "Activation–Lesion Overlap"**
where it is **Attention–Lesion Overlap** everywhere else. Both fixed.
**New standing rule recorded in VERSION_SYNC §2a:** the drafted sections now outrank the planning documents
on content — §0.3 goal, §0.5 object/subject, §0.6 hypotheses, §0.2 novelty, §0.8 provisions, §7 conclusion;
`MASTER_OUTLINE.md` is authoritative for *structure* only.

**3. Both assemblers repaired.** `_assemble_en.py` extracted only text under a literal `## PART 1` marker —
Ch 4 carries it in **3 of 20** drafts and Ch 5 in **none of 7**, so **24 sections assembled as empty and
nothing said so**. Fixed with a top-of-file fallback plus a **suspect-extraction report**. Chapter 0 is now
assembled from an **explicit ordered list** (its identifiers deliberately do not follow manuscript order), and
a list/disk mismatch is a hard error. Chapters **0, 5 and 7 were missing from the chapter list entirely**, and
the three front-matter units from `thesis/output/` are now inserted ahead of the Introduction. Same two fixes
applied to `_assemble_kz.py`. **Verified: EN → 94 sections / ≈94,200 words, no suspect extractions**
(previously 53 with 24 empty); KZ → 53 translations, clean.

## APPENDICES A–F COMPLETE — the written text is finished

**App B** — 13 tables decomposing Ch 4–5 to the class and the confusion cell. **Transcription verified
mechanically**: 168 distinct 3–4 dp values + 184 confusion-matrix integers, none absent from `results/`,
nothing recomputed. §B.8 states three absences with a reason and a consequence each.
**App C** — **DIA-6.3 DISCHARGED**, the last asset task in Ch 6. Four views as Mermaid source + a
module → FR → NFR traceability table. **New conversion requirement: the Mermaid source must be rendered at
conversion, or the converter must handle fenced Mermaid.**
**App E** — the **complete** 54-plate annotated subset, no selection, floor cases retained; NC-14 before the
first plate; plates declared illustration carrying no measurement; G-3 stated as an absence.
**App F** — 8 tables; three qualifications stated *before* the tables; §F.8 explains the retention-ratio
artefact as an instance of the §5.4 normalisation defect, bounded as descriptive.

⚠ **Correction worth remembering:** an initial asset search was built wrongly and reported *no* Grad-CAM
overlays on disk. **They exist** — 54 paired plates at `experiments/outputs/exp4/gradcam_maskset/`, exactly
where `ASSET_INVENTORY.md` records them. Repo-wide asset searches on this tree must not use
`find -path X -prune -o -name Y -print` casually; it silently under-reports.

**Assembly re-run: 98 sections / ~101,050 words, no suspect extractions.**

## Completion pass, 2026-08-12 — PLAN.md rewritten as a completion board; four items closed

`thesis/PLAN.md` no longer tracks writing. It now carries a **CURRENT STATE** table (verified on disk,
not from checkboxes), a Phase-4 KZ-translation tracker, and §11 as the live completion board.
**Verified counts to reuse instead of re-deriving:** EN = 98 sections / **101,459 body words**
(103,147 by `wc -w`, which also counts headings and banner — quote the body figure); KZ = 53 / 41,605.
Of 90 `[FIG/TAB/DIA]` placeholders carrying 80 distinct paths, **76 resolve to files that exist**.

**1. `_assemble_kz.py` had no `FRONT_MATTER` block** — the 2026-08-11 repair added it to the EN
assembler only, so the KZ manuscript opened straight at Chapter 1 for months while EN carried normative
references / definitions / abbreviations. The three `thesis/output/*_kz.md` sources existed; only the
insertion was absent. Ported, missing file now reported as suspect, verified.

**2. FIG-1.1 named the wrong corpus.** The placeholder pointed at `fig1_1_dr_grades_eyepacs.png`, which
**does not exist**; `figures_mine/README.md` records a deliberate decision that dataset-illustration
figures are rebuilt from IDRiD, and **the plate carries "(IDRiD)" in its own rendered title** — so the
caption contradicted the image itself. Path and caption corrected in the EN draft *and* the KZ
translation. The EyePACS generator `_make_dataset_montages.py` is still on disk but its output was
never kept — do not "restore" the EyePACS path.

**3. DIA-6.3 needed more than re-pointing.** §6.1.2 called it a deferred asset *and* promised
component/sequence/**class/activity/ER** diagrams, whereas App C delivers component/deployment/sequence/
**data**. Repointing alone would have left three promised diagram kinds that do not exist; the sentence
was rewritten to the four views actually supplied, SB-4.1 framing retained.

**4. `ASSET_INVENTORY.md` staleness closed** for APP-B/C/E/F + DIA-6.3 + FIG-1.1.

## Citation pass — DONE 2026-08-12 (`_finalize_citations.py`, re-runnable)

**107 sources, numbered once by first appearance in EN and reused verbatim in KZ.** EN 292 brackets,
KZ 230; 107 reference entries per language; no `[card not found]`; **BLOCKING 0, residual self-citations
0, UNKNOWN 1** — the §0.15 legal-act number `(No. 230-VIII …)`, correctly not a citation.

**Five defects found and fixed; three would have shipped a wrong book:**
1. The script was **pinned to `..._partial_2026-06-17.md`** — re-running it would have silently
   reconverted the stale 53-section manuscript and printed success. Now resolves the newest assembly.
2. **`split_body()` started the body at `^# 1 `**, correct only while Ch 0 was unwritten. With Ch 0
   assembled ahead of Ch 1, every Introduction citation would have been left unconverted *and* dropped
   from the numbering, shifting every later number. Now starts at the Introduction, Ch 1 as fallback.
3. **Self-citation bibliography was broken**: 3 of 6 self cards were `[NO APA LINE]` in `_card_bib.tsv`
   and `yesmukhamedov-nan-rk.md` held an entry for a *different paper* (Pallavi et al. 2022 — extraction
   artefact). All six rewritten from the cards.
4. **Self-citations were never actually ambiguous** — the ambiguity was an artefact of matching on first
   author alone. `Yesmukhamedov et al., 2025` locators (74–90) fall only inside NAS RK's 74–91;
   `Sapakova, Yesmukhamedov & Sapakov, 2025` matches the EEJET card's two recorded equations. Now
   numbered like any source (GOST requires it); two Scopus cards = **one** number per §0.12's "five
   distinct works, not six"; SIR-4 framing lives in the prose, so conversion leaves it intact.
5. **⚠ OPEN FOR THE CANDIDATE — §2.1.2 cited pages that do not exist in the cited article.** Locators
   read p. 5 (×3) / p. 9 (×1); those are the card's *internal PDF* pages, but the article is published
   at **EEJET 4(9(136)), pp. 79–88**. Card pages 1–10 map onto exactly ten journal pages ⇒ offset 78, so
   p. 5 → **83**, p. 9 → **87**. Remapped in EN draft + KZ translation, recorded in the §2.1.2 checklist.
   **Forced only if the PDF has no cover page — verify against the published article.**

## Assets — ALL CLOSED 2026-08-12; `ASSET TO BE CREATED` is now zero

**Verified on both assembled manuscripts: every referenced asset path resolves to a file on disk.**

- **FIG-4.17** (the manuscript's last outstanding asset) rendered by
  `defense/figures/figures_mine/_make_fig4_17.py`, which **parses `results/tables/H-3_domain_distance.md`
  rather than transcribing it** — the figure cannot drift from the table printed above it. Three panels:
  distance per arm (ordering visibly preserved), Δd vs MCID_d = 0 (all six intervals clear of zero), KL
  reduction vs its 34–38 % band. **Deliberately not drawn:** any pairing of Δd with transfer gain
  (ρ ≈ 0.49 — a scatter would invite the magnitude reading §4.4.2 forecloses).
- **FIG-3.8** re-rendered by `defense/presentation/scripts/render_stage6_card.py`. The old card showed the
  retired **PCA colour jitter** *and* a **"horizontal re-flip"** step `augmentation_unified.py` does not
  perform. The source SVG had already been re-specified — only the six PNG copies lagged; the script now
  writes all six from one source. **Layout defect fixed in the same pass:** the re-specification put a 4th
  PARAMETERS line at the y the fixed panel grid reserves for OUTPUT. Parameters verified against
  `config.py`; rotation σ fallback stays **13.0°** per [[governance-implementation-divergences]].
- **Two FIG-3.8 placeholders contained a literal ellipsis** in their path
  (`19_aug_rotation/…/stage6_augmentation.png`) in §3.1.1 and §3.1.3, EN and KZ — they resolved to no file
  at all. Fixed in all four.
- ⚠️ Folder `defense/presentation/assets/preprocessing/23_aug_pca_color/` still carries the retired name.
  Path only, contents current; renaming would ripple into demo assets, so it was left.

**Gotcha:** rendering an SVG via headless Chrome from Git Bash — build the file URI with
`Path.as_uri()`, never `file:///$PWD/...`. The malformed form silently screenshots Chrome's
*"file not found"* error page **over the target PNG** (recoverable here only because it was git-tracked).

## KZ TRANSLATION COMPLETE — 98 of 98 (2026-08-12)

**All 45 outstanding units translated in one day**: Ch 4 (17), Ch 0 (16), Ch 5 (7), Ch 7 (1),
App B/C/E/F (4). **KZ assembly emits 98 sections / 81,438 body words** against the English
98 / 101,575; every chapter is 100 % (0: 16/16 · 1: 11/11 · 2: 15/15 · 3: 13/13 · 4: 20/20 ·
5: 7/7 · 6: 9/9 · 7: 1/1 · App: 6/6). No suspect extractions, every KZ asset path resolves, citation
pass clean in both languages (107 sources, BLOCKING 0, KZ 267 brackets).
**Chapter 0 verified to assemble in manuscript order, not numeric** (§0.6 before §0.2, §0.8 before §0.7).

**Phase 4 is closed. The critical path is now §11.4, the EN + KZ GOST re-export** — `defense/docs/`
still holds only June builds of the 53-section manuscript.

**Transcription-only appendices must be built programmatically, not retyped.** App B and F carry
mechanically verified values (168 + 184 in B, 159 in F), and re-typing them into a translation would
put that guarantee at risk. Both Kazakh bodies were derived from the English drafts by substituting
only prose, headings, captions and column labels, leaving every numeric cell byte-for-byte; the
builders live in the session scratchpad. **Verified afterwards: B = 529 numeric tokens identical /
84 table rows; F = 295 identical / 53 rows.** ⚠ The numeric comparison must normalise **both**
thousands conventions (EN `35,126` vs KZ `35 126`) or it reports a false mismatch. Group identifiers
like `mixed_ddr` are data keys and stay untranslated.

**Ch 7 audited: the only decimal in the body is `5.4`, a section reference** — identical to the English,
so its "no metric value anywhere" property survived translation.

**App C and App E were built the same programmatic way, each with its own fidelity check.**
App C: the **four Mermaid blocks are byte-identical** to the English and deliberately untranslated —
the appendix calls the source "the definition of the diagram", the node labels are technical terms and
governance codes the directive keeps in English, and an identical source makes both editions render
the same figure. App E: the **54 plate lines** were rewritten by one regex translating only the caption;
**all 54 image paths and all 54 `FIG-E.*` identifiers verified identical and in the same order**.

**Two Chapter-0 invariants are machine-checkable and were checked after translation — re-run both after
any future edit in either language:**
- **§0.6** — the section body must contain only thresholds. Measured: exactly four decimals,
  `0.0, 0.02, 0.050, 0.85`, all thresholds, no outcome. §5.2.2's pre-specification argument depends on it.
- **§0.8** — measured: **exactly one metric value (`0.0041`)** in the body and **no `PC-3`**, so the
  Introduction cannot be used to re-adjudicate Chapter 4 and the deliberate identifier gap stays open.
- **§5.2.2** — the same PC-3 rule takes a *different* form here and the two must not be conflated:
  §5.2.2 **names PC-3 in prose** as the unused identifier (the English draft does too), so a naive
  "PC-3 must not appear" check false-alarms. The real invariant is the **table**: 11 claim rows,
  `PC-0, PC-1, PC-2, PC-4 … PC-11`, **no PC-3 row** — verified identical in both languages.

**`_assemble_kz.py` blocked incremental Chapter-0 work and was fixed.** Its `ORDER_OVERRIDE` check
hard-errored when *any* listed Ch-0 translation was absent, so translating one section broke the entire
KZ build. Missing is not the dangerous case — a file present but **unlisted** is, since it would fall
back to numeric sort, which is the wrong order for Chapter 0. Now: unlisted extras stay fatal, existing
sections are emitted in listed order, and a `PARTIAL` report names what is still missing.

**§0.6 audited after translation: the body carries exactly four decimals — 0.0, 0.02, 0.050, 0.85 — and
every one is a threshold.** No outcome leaked, so §5.2.2's pre-specification argument still holds. Re-run
that check after any future edit to §0.6 in either language.

**House format for a Ch-4 translation** (Ch 4 drafts have no `# ` title line — they open at their own
`##`/`###` heading, and the assembler must not prepend anything): metadata blockquote → `---` →
`## 1-БӨЛІК: БӨЛІМ МӘТІНІ` → the `##`/`###` headings and body → `## 2-БӨЛІК: ТЕРМИН ҚОЛДАНЫСЫ ЕСЕБІ` →
`### Аудармашы ескертуі`. `BODY_END` cuts at `## 2-БӨЛІК`, so the term report and note stay out of the
manuscript. Verify each batch with `_assemble_kz.py` — "No suspect extractions" plus a plausible word
delta is the check.

**Fences verified as surviving translation**, section by section: CFC-2.8 in §4.2.1/§4.2.3 and its
**discharge** in §4.3.1 (single-initialization premise stated *before* the claim, with the "does not
retroactively make Experiment 1 single-factor" sentence in the same paragraph); PC-8
grouping-resolution-only; §4.3.2's selection-surface-vs-held-out rule and the open DR1 discrepancy
(0.2091 vs 0.4693); §4.3.3's "tracks the photometric part and does not exhaust it" plus VVI's exclusion;
§4.4.1's MMD-primary/KL-secondary asymmetry and the source-domain-statistics condition; **§4.4.2's
ρ ≈ 0.49 and direction-only**; §4.5.1's both-arms-clear qualification and the G-denominator asymmetry;
**NC-14 stated before the method in §4.6.1**; §4.6.2's IoU-as-corroboration status and the τ = 0.7
exception; **G-3 as an absence, not a negative result, in §4.6.3**; §4.7's **bold 0.0041 Messidor-2
margin**, the non-aggregation rule and the full Δ_drop identity; §4.8's retention-ratio inversions as a
denominator artefact plus NC-16; §4.9's **E-7 comparable-not-larger** and the unpaired-interval overlap;
and **all eight fences restated in §4.C without softening**. Governance codes, `[VERIFY]` markers,
formulas and every table value pass through untranslated.

## RE-EXPORT DONE 2026-08-13 — the critical path is closed

`defense/docs/` now carries `FULL_DISSERTATION_{EN,KZ}_GOST_2026-08-13` as **docx + pdf**, plus
`DISSERTATION_{EN,KZ}` (docx) and `FRONT_MATTER_{EN,KZ}` (docx + pdf), all built from the current
98-section text. **§0.16 is filled and verified: EN 239 pages / KZ 266, 42 tables, 29 figures,
107 sources** (excluding appendices, which is the volume the council rule measures). Six commits on
2026-08-12/13 carried it: Mermaid rendering + appendix asset markers → front matter/full build/§0.16 →
FIG-5.1 closed against the council's own samples → diagram captions below the image, label-first →
resource IDs replaced by reader-facing references (40 occurrences) → governance document names and
stray version markers removed (27 + `v6.0.0`/`v6.1.0`).

⚠ `PLAN.md` §11.4 records the §0.16 page fill as **240 EN**, but the assembled manuscript and the
built document say **239** — one of the two is stale; re-read the count off the final PDF before
submission.

**Still open after the export:**
1. ~~The 356 governance codes are undefined for the reader.~~ ✅ **CLOSED 2026-08-13 — declared, not
   stripped.** All eight families carry a row in `DESIGNATIONS AND ABBREVIATIONS` (EN + KZ), written in
   the numbered form `SB-n` … `CFC-n`, each saying what the family *is* rather than where it is
   recorded. The `OD` collision is resolved by putting `OD-n` directly after `OD` (Optic Disc) and
   stating that the optic disc is never written with a number. **Three further families were removed
   rather than declared** — `IT-1` ×4, `SC-1.4` ×3, `AOQ-2` ×2, all bare provenance parentheticals, and
   `(AOQ-2 simplified)` was process history besides; §3.3.1's "the five-class taxonomy of IT-1" was
   reworded to "the dissertation's five-class taxonomy". Compliance checklists (PART 2/3) keep their
   code references — only PART 1 was touched. `FR-n`/`NFR-n` stay undeclared by decision: §6.1.1 defines
   each in its own table where it first appears. See [[manuscript-text-hygiene]].
2. **Trim queue (§11.3b)** — never run; both editions clear the 300-page rule with room, so it is
   optional, but any trim moves pagination and therefore §0.16.
3. **Council deliverables lag the manuscript**: `abstract_{en,kz,ru}.docx/pdf` are **June 18** builds
   while the Markdown was re-synced 2026-08-11, and the standalone `TABLE_OF_CONTENTS_*` exports are
   still June (the current contents ships inside `FULL_DISSERTATION_*`). Re-export via the
   `council-docs` skill. Supervisor/foreign-consultant reviews are June and unchanged in source.
4. **NEW-1 traceability** and the `TAB-5.2` PC-11 register position — see below.

**Remaining:** (App B/C/E/F now done — historical note: B was bounded by
unrecorded per-epoch/per-class curves; E is IDRiD-only per G-3; F lacks per-group confusion matrices;
C needs the DIA-6.3 UML). **KZ translations are now the largest remaining task — 45 units: Ch 0 (16), Ch 4 (17 of 20), Ch 5 (7), Ch 7 (1), App B/C/E/F (4).**
Phase 3 = assemble → resolve placeholders → single `.docx`.
See [[results-knowledge-base]], [[no-process-history-in-deliverables]].

## CHAPTER BODY COMPLETE — Chapters 0–7 all approved

**Ch 7 (Conclusion) ✅ APPROVED**, ~1,610 w, **inside band, no flags** — the first chapter-scale front/back-matter
section to land in band without a mandatory-content exemption. Six movements; principal finding stated as
**consistency, not effect size**; four kinds of contribution with the methodological one **strictly
descriptive**; eight open questions sorted by closing cost incl. **one measurement cannot close**.
Three audits recorded in `reviews/7-review.md`: **fence audit 8/8 intact** through the document's most
compressive section, **ceiling audit against §0.8 provision by provision — no promotion**, and **VCR-3
discharged** (the initialisation branch that failed its acceptance gate is reported, not omitted).
**No metric value anywhere in Ch 7** — the thin external margin is stated in words, per §5.C's precedent.
One **deliberate omission**, recorded so it is not read as an oversight: §0.8's provisions 11 (thermal-optical
model, screening architecture) are not restated among the conclusion's contributions, because doing so would
imply an empirical standing they do not have.

**Ch 7 is bounded by two ceilings and exceeds neither** — §5.C behind it, **§0.8 in front**. If the two ever
disagree, one is wrong and it must be resolved, not averaged. That rule binds any future edit to either.

## Chapter 0 (Introduction) — ✅ COMPLETE, 16/16

**Gate discharged** — §0.8 was the last block and §5.2.2 (TAB-5.2) supplied it. All thirteen sections
drafted here are approved; the three front-matter units were already complete in `thesis/output/`.

**Artifact-set deviation, deliberate:** the seven substantive sections (§0.1–0.6, §0.8) each carry their own
continuity + review file; the nine short apparatus sections are verified and handed off **as one block** —
`reviews/0.apparatus-review.md` + `continuity/0.apparatus-continuity.md` — since they share one binding set.
Precedent: §6.3.1. The governing constraint held across all nine: **no apparatus section states an outcome
§0.8 has not submitted** (verified per section, incl. the two predicted drift points §0.9 and §0.10, where
§0.10 deliberately omits the measured computational cost because §0.8 did not submit it).

**§0.8 is the section to protect.** Eleven provisions; fence audit 8/8 intact; promotion audit against
TAB-5.2 shows no promotion and no softened qualification; the Messidor-2 margin 0.0041 disclosed *with* its
sub-threshold lower bound (a fence stronger than the table's); exactly one metric value in the whole section
and no table reproduced, so the Introduction cannot be used to re-adjudicate Ch 4. **PC-3 stays unused.**

**§0.6 leaks no outcome** — every numeral in it is a threshold. That property is what §5.2.2's
pre-specification argument depends on and it must survive any later edit.

Front matter §0.FM1–FM3 is **already done
outside `chapters/`** as EN/KZ deliverables in `thesis/output/` (normative refs, definitions,
abbreviations) — not re-drafted. See [[front-matter-deliverables]].

**Two orderings, both binding — do not conflate.** Section *identifiers* are stable and are what governance,
this memory and `5.C-continuity.md` reference (**§0.8 = Provisions Submitted for Defence**). *Manuscript
order* is `outline/TABLE_OF_CONTENTS_EN.md`'s and is NOT the numeric order; four TOC items lacked an
identifier and got §0.13 Reliability, §0.14 Empirical Basis, §0.15 Scientific Programmes, §0.16 Structure.
**Phase-3 consequence:** `assembly/_assemble_en.py` sorts numerically, which equals TOC order for every
chapter except Ch 0 — Ch 0 needs an explicit ordered list.

**Three project documents are stale and must not be followed when writing Ch 7 or the council deliverables:**
`governance/CORE_OBJECTIVE.md` v5.0 (retired H-7 "clinical degradation resistance"; no H-3);
`outline/MASTER_OUTLINE.md` v6.0.0 (H-3 recorded as dropped; retired H-7 form; two objectives numbered "8";
**object of research given as the images rather than the process** — a category error);
`thesis/output/abstract_en.md` ("seven experiments" — the programme is **eight** investigations; H-3 absent;
provision 5 still in the retired Δ_drop form; **and it lists the Vessel Visibility Index as a method — §4.3.3 excluded VVI for want of an implementation and a source, so this one is an ERROR, not merely stale**). **The abstract sync pass is now DUE** — §0.2, §0.6 and §0.8
have landed and are what it must be rewritten against; its statements-for-defence list has six items where
§0.8 submits eleven provisions plus one observation. A governance-sync pass on the first two is also due.

A fourth divergence surfaced while writing §0.8: **`results/tables/TAB-5.2_claim_strength.md` lags
`ARGUMENT_MAP.md` v7.1.0** — it files the domain-distance result under "additional empirical results outside
the formal PCs", while the argument map carries it as **PC-11**, a first-class node depending on PC-1 and
feeding PC-6/PC-9/PC-10. Substance and strength agree (STRONG, direction only); only the register position
differs. §0.8 submits it as PC-11.

**Chapter 0 is running long — six of seven sections over band** (§0.1 ~1,125/800–1,000; §0.2 ~1,205/800–1,000;
§0.3 ~535/300–500; §0.4 ~695/400–600; §0.6 ~1,205/600–900; §0.8 ~1,255/700–900; only §0.5 ~290 is in band).
Cause is consistent and legitimate — mandatory disclosures, inventories and qualifications that cannot be
compressed. Each draft's word-count note names its own compressible material. **Excluded from the trim in
every case:** §0.6's four mandatory disclosures, §0.8's qualifications, and the §0.3 goal sentence (quoted
verbatim in the abstract and defence materials).

**Latent Phase-3 defect found while reading the assembler:** `_assemble_en.py` extracts only text under a
`## PART 1` marker, but most Ch 4 and all Ch 5 drafts were written **without** that marker (body starts at
the section heading). Verified: Ch 1 = 11/11 have it, Ch 4 = **3/20**, Ch 5 = **0/7** — so **24 sections
would assemble as empty**. Fix at Phase 3 (either add the markers or relax the extractor). Ch 0 drafts use
the marker.

## Chapter 3 (Methodology) detail — drafted & APPROVED 2026-06-09

All 13 sections (§3.1.1–§3.1.4, §3.2.1–§3.2.2, §3.3.1–§3.3.4, §3.4.1–§3.4.2, §3.C) under `thesis/chapters/03-methodology/`. Real artifacts cited (verified on disk): RES-VAL `od_fovea_idrid_metrics.json` (OD within-1-OD-radius 0.673 train/0.612 test; fovea ~0% — honest disclosure in §3.1.1); RES-NORM `eyepacs_norm_stats.json` (mean ≈[0.506,0.505,0.504], std ≈[0.090,0.074,0.058]).

**Stage-6 augmentation redefined (2026-06-26):** §3.1.3 no longer uses PCA colour jitter — replaced by **ColorJitter** (brightness/contrast/saturation ∈ [0.9,1.1], hue ∈ [−0.02,0.02], each component p=0.5) plus **acquisition-variability** augmentations **Gaussian noise** (σ∈[2,6], p=0.15) and **JPEG compression** (quality∈[70,100], p=0.20). Final on-the-fly order: affine → ColorJitter → Gaussian noise → JPEG. RES-PCA artifact **retired** (no estimated colour basis); `scripts/compute_pca_eigvecs.py` deleted; OD-3 Stage 6 updated in INVARIANTS v6.1.0. Code: `experiments/src/data/augmentation_unified.py`, `config.py`, `configs/default.yaml`. ⚠️ FIG-3.8 render + demo `stage_6_augmentation` images still depict the old PCA aug — regenerate.

**Carry-forward flags for Ch 4 / corpus completion:**
- CFC-2.8 composite IV binds §4.2 (integrated-config only, never preprocessing-alone). See [[config-d-pretraining]].
- SSL B/D arm UNTRAINED (shipped Config-D = retired ImageNet artifact) → §4.2 stays blocked; §3.3.2 written as spec-not-result. See [[preprocessing-od-fovea-polar]].
- [VERIFY] Stage-5 governance/implementation divergence: OD-3 says 8×8 tile-grid CLAHE; shipped default is polar. Drafts follow governance.
- ✅ RESOLVED 2026-06-12 — corpus gaps closed & **integrated into approved drafts** after the 81→120 expansion ([[literature-corpus-120]]): focal-loss primary Lin et al. 2017 (#96) now cited in §2.2.2 + §3.3.4 ([VERIFY] cleared); in-domain retinal SSL primaries (#84 RETFound, #85 MICLe, #86–#91 methods, #92 survey) now cited in §3.3.2; Grad-CAM card #46 now cited in §2.5.1 (missing-card parenthetical removed); EyePACS #47 + Messidor-2 #48 cards now cited in §1.2.3 + §4.1.1 (EyePACS ~35,126 attributed to Kaggle partition, not Cuadros & Bresnick). Still missing: #49 RFMiD / #50 DDR / #51 ODIR-5K cards (drafts hold these at index-only camera-attribute level).
- **§2.3.3 now UNBLOCKED** (its deferral condition — SSL-on-fundus cards — is met) but still UNWRITTEN; needs its own writing session (brief→draft→review). Flagged in §3.3.2 deferred-asset log.
- **Coverage-Matrix reconciliation pass (started 2026-06-12):** the LITERATURE_INDEX Coverage Matrix is a *relevance* map, not a citation log; many #83–#121 additions are mapped to already-approved drafts but were not woven into prose. **Done:** §2.2.3 (added #98/#100/#101/#102/#103/#104 — its three named techniques' primaries; ~915 words, upper edge); §1.3.1 (added #83/#105/#106/#107/#108/#110/#111/#112/#120/#121; ~1,325 words, slightly over the 1,300 cap — light trim queued; #116 Dai + #114 Son deferred to §4.4/§4.5/§4.7); §1.4 (added #115 Bellemo [+TAB-1.1 row], #118 Ting-2019, #117 De Fauw off-modality; ~1,585 words); §6.3.1 (added #115 Bellemo, #119 Beede, #118 Ting-2019, #117 De Fauw — all qualitative/no-metric deployment precedents; ~1,295 words; §6.3.2 left unchanged — no natural home); §3.2.1 (added #100 BatchNorm [intrinsic to ResNet-50, small-batch caveat] + #107 Inception-v3 [situate-only]; ~1,085 words); §3.4.2 (added #99 Adam at TAB-3.1's first prose mention — placed here, the optimizer's config home, rather than §2.2.2/§3.2 where the matrix nominally maps it); §3.4.1 (added #98 Buda [accuracy-distortion-under-imbalance] + #113 Krause [reference-standard/grader-variability limitation]; ~1,290 words); §2.1.1 + §2.1.2 (added #95 Zuiderveld canonical CLAHE alongside #54 Pizer; ~1,045/~1,425 words); §2.3.1 (added #109 Pan&Yang taxonomy + #121 Esteva cross-domain transfer; ~865 words — §2.3.2's #109 mapping satisfied by this citation, not re-cited); §2.6 (added #94 Zago fundus RIQA, partially lifting the THIN flag; ~1,070 words); §1.2.2 (added #94 Zago + #116 Dai [¶2, quality→performance] + #119 Beede [¶5, gating nuance]; ~1,130 words, slightly over cap — trim queued). **Coverage-Matrix reconciliation COMPLETE for drafted sections (2026-06-12).** Every v6.1.0 source mapped to a drafted section is now cited in ≥1 drafted section. Final catch: #97 Cui (class-balanced loss) mapped ONLY to §2.2.2 and was added there. One deliberate exception: #114 Son's §1.3.1 mapping is intentionally left to its experiment home §4.7 (undrafted), like #116 Dai which landed in §1.2.2 instead of §1.3.1. Residual matrix entries are re-mappings of sources already cited elsewhere — §1.5 (#113 Krause, cited §3.4.1), §6.1 (#119 Beede, cited §6.3.1+§1.2.2), §2.3.2 (#109, cited §2.3.1) — satisfied at corpus level, optional to re-cite. **True remaining gaps are NOT citation backlog:** unwritten §2.3.3 (now unblocked) + Phase-2 §4.2–§4.8/Ch5 (experiment-gated), and missing cards #49 RFMiD / #50 DDR / #51 ODIR-5K. Several reconciled sections sit at/slightly over their word-count upper band (§1.3.1 ~1,325, §1.4 ~1,585, §1.2.2 ~1,130, §2.2.3 ~915) — light trims queued for Phase-3 assembly.
- Two intentional [UNSOURCED CLAIM] markers kept (§3.1.4 ingestion, §3.3.2 SSL) — candidate methodological positions, keep through assembly. The §3.3.2 marker was **narrowed** to the untrained CNN-native-on-4-channel-V5 configuration (general in-domain-SSL direction now sourced by RETFound/MICLe).

Open corpus-hygiene flags for Phase-3 bibliography (non-blocking): see [[literature-integrity-flags]].
