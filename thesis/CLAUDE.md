# thesis/ — Dissertation Text and Governance

Doctoral dissertation: "Automated Diabetic Retinopathy Diagnosis via Fundus Image Enhancement and CNN Classification"
Candidate: Yesmukhamedov N.S., IITU, Almaty, Kazakhstan.

## Structure

```
governance/          — SINGLE SOURCE OF TRUTH for all project claims
  INVARIANTS.md        v7.0.0 — scope, forbidden claims, binding constraints
  HYPOTHESIS.md        v7.1.0 — H-1 through H-7 formal definitions
  ARGUMENT_MAP.md      v7.1.0 — claim-evidence dependency DAG (PC-0…PC-11, PC-3 unused)
  CENTRAL_THESIS.md    v7.1.0 — one-paragraph thesis statement
  CORE_OBJECTIVE.md    v7.1.0 — research goal (derived from §0.3, which is authoritative)
  CONTRIBUTIONS.md     v7.1.0 — 4 primary + supporting contributions (SC-A…SC-I)
  RESEARCH_ARCHITECTURE.md  v7.0.0 — full experimental design
  VERSION_SYNC.md      v7.1.2 — cross-file version register
  VERSIONING_POLICY.md        — bump scheme, detection regexes, containment scan
  CHANGELOG.md                — amendment history

chapters/            — 9 directories (00–08: introduction, six body chapters,
                       conclusion, appendices), each with:
  briefs/              section briefs (writing specs)
  drafts/              generated text
  reviews/             review feedback
  sessions/            session transcripts
  continuity/          continuity notes between sections
  translations/        Kazakh translations

literature/
  external/            36 literature cards (structured 18-section format)
  self/                6 self-citations (yesmukhamedov-*.md)
  non-peer-reviewed/   1 card (wikipedia-clahe.md)
  LITERATURE_INDEX.md  master index of all sources

glossary/
  GLOSSARY_EN.md       canonical English terms
  GLOSSARY_KZ.md       Kazakh translations

outline/
  MASTER_OUTLINE.md    chapter-by-chapter content specification
  TABLE_OF_CONTENTS_EN.md
  TABLE_OF_CONTENTS_KZ.md

methods/
  preprocessing-pipeline.md   pipeline full specification
  implementation.md           implementation details

prompts/              AI writing session templates
  writing-session-system-prompt.md  — fixed system prompt for all writing sessions
  section-brief-template.md
  continuity-note-template.md
  revision-session-template.md
  literature-card-review.md
  and others...

experiments/
  experimental-protocol.md    detailed scientific protocol
```

## Governance Hierarchy

INVARIANTS.md is the supreme authority. If any document conflicts with INVARIANTS, INVARIANTS wins. The hierarchy:

1. INVARIANTS.md — defines what can and cannot be claimed
2. HYPOTHESIS.md — formal hypothesis definitions (must match INVARIANTS)
3. ARGUMENT_MAP.md — claim-evidence structure (must match INVARIANTS)
4. CENTRAL_THESIS.md / CORE_OBJECTIVE.md — thesis statement and goal
5. CONTRIBUTIONS.md — what the dissertation contributes
6. RESEARCH_ARCHITECTURE.md — experimental design details

## Writing Workflow

1. Prepare a Section Brief (from `prompts/section-brief-template.md`)
2. Load the system prompt (`prompts/writing-session-system-prompt.md`)
3. Load INVARIANTS.md + relevant governance docs
4. Load relevant literature cards
5. Load continuity note from preceding section (if any)
6. Generate section text
7. Review against governance constraints
8. Produce continuity note for next section

## Key Governance Rules

- Every empirical claim must cite its evidence source by Literature Card filename
- Forbidden claims (CFC-2.x) must not appear in any form
- Non-claims (NC-x) must not be asserted
- Scope boundaries (SB/DGL) must be stated where relevant claims first appear
- Self-citations must be identified as prior own work (SIR-4)
- No source amplification — only attribute conclusions explicitly in the literature card (SIR-1)
- Terminology must match GLOSSARY_EN canonical forms

## Chapter Status

- 00-introduction: ✅ APPROVED (16/16 — 13 sections drafted here + 3 front-matter units already complete as EN/KZ deliverables in `thesis/output/`, not re-drafted). **Section identifiers are stable (§0.8 = Provisions Submitted for Defence); manuscript order is the TOC's and differs from numeric order** — see `chapters/00-introduction/README.md`. The nine short apparatus sections are verified as one block (`reviews/0.apparatus-review.md`)
- 01-problem-domain: ✅ APPROVED (11/11)
- 02-theoretical-foundations: ✅ APPROVED (15/15)
- 03-methodology: ✅ APPROVED (13/13)
- 04-experiments: ✅ APPROVED (20/20 — §4.1.1–§4.C)
- 05-validation: ✅ APPROVED (7/7 — §5.1, §5.2.1, §5.2.2, §5.3.1, §5.3.2, §5.4, §5.C). TAB-5.3 assembled in §5.3.1 from the literature cards; §5.1 written in its quantitative part only (clinical overlays absent, G-3, stated as an absence)
- 06-system-architecture: ✅ APPROVED (9/9)
- 08-appendices: ✅ APPROVED (6/6 — A, B, C, D, E, F). **App C discharges DIA-6.3**, the last asset task in Ch 6. B and F are transcription-only from `results/`, verified mechanically value by value. E reproduces the complete 54-plate annotated subset, no selection.
- 07-conclusion: ✅ APPROVED (1/1). Bounded by two ceilings — §5.C behind it, §0.8 in front; the review carries a provision-by-provision ceiling audit and a fence audit (8/8 intact). No metric value appears in the chapter.

Experimental chapters are written from `results/` (`findings/`, `tables/`, `hypotheses/`), which is the
single source of truth for every number and verdict. Where an earlier draft conflicts with `results/`,
`results/` wins and the draft is revised. `results/` provenance (run dates, recomputation history,
artifact paths) never enters the prose — system-prompt rule 16.

## Hypotheses

- H-1: Integrated Pipeline Dominance (Exp 1, EyePACS 100%; integrated arm = ophthalmology-SSL, composite IV, CFC-2.8)
- H-2: Component Ablation + CLAHE/σ sweeps (Exp 2, EyePACS)
- H-3: **Domain-Shift Reduction** (§4.4) — MMD/FID over penultimate-layer features (**primary**, sole basis of the criterion) + KL over channel histograms (**secondary, informational only**), six target domains. Criterion: **Σ PASS_S ≥ K = 5 of n = 6**, with `PASS_S ⟺ Δd(X) ≥ MCID_d = 0.0 ∧ CI⁻(Δd) > 0`; 1 000 bootstrap resamples; arms D − C (EfficientNet-B3); forward passes only, no training. **Mandatory protocol condition:** Stage 7 must use source-domain statistics — computing it from the target makes the test incomparable with H-4/H-6/H-7. **Restored in governance v7.1.0** — the label formerly denoted a *training-method comparison* dropped in V3; **that retirement stands and the label is reused**, so "H-3 dropped" in §2.3.2/§3.3.3 refers to the retired hypothesis, not this one. Mechanistic, not clinical: it measures the middle term of the causal chain that H-4/H-6/H-7 approach only through its consequence.
- H-4: Cross-Dataset Transferability on APTOS 2019 (Exp 3, G ≥ 0.85)
- H-5: Explainability — Grad-CAM ALO/IoU (Exp 4, IDRiD + Clinical)
- H-6: Device Domain Shift (Exp 6, DDR/ODIR-5K/RFMiD)
- H-7: **External Clinical Performance** (Exp 5, IDRiD + Messidor-2) — reformulated in governance v7.0.0 from "Clinical Degradation Resistance". Criterion (form S): Δ wF1(integrated − baseline) ≥ MCID 0.050 with CI⁻ > 0 on **each** set. The retired Δ_drop form is descriptive only; no verdict may rest on it.

## Language

- Dissertation text: formal academic English
- Translations: Kazakh (in translations/ subdirectories)
- All governance docs: English
- Register: third person, past tense for results, present tense for definitions
