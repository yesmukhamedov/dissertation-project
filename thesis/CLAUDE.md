# thesis/ — Dissertation Text and Governance

Doctoral dissertation: "Automated Diabetic Retinopathy Diagnosis via Fundus Image Enhancement and CNN Classification"
Candidate: Yesmukhamedov N.S., IITU, Almaty, Kazakhstan.

## Structure

```
governance/          — SINGLE SOURCE OF TRUTH for all project claims
  INVARIANTS.md        v7.1.0 — scope, forbidden claims, binding constraints
  HYPOTHESIS.md        v7.1.0 — H-1 through H-7 formal definitions
  ARGUMENT_MAP.md      v7.1.0 — claim-evidence dependency DAG (PC-0…PC-11, PC-3 unused)
  CENTRAL_THESIS.md    v7.1.0 — one-paragraph thesis statement
  CORE_OBJECTIVE.md    v7.1.0 — research goal (derived from the aim rubric of the Introduction, which is authoritative)
  CONTRIBUTIONS.md     v7.1.0 — 4 primary + supporting contributions (SC-A…SC-I)
  RESEARCH_ARCHITECTURE.md  v7.0.0 — full experimental design
  VERSION_SYNC.md      v7.1.2 — cross-file version register
  VERSIONING_POLICY.md        — bump scheme, detection regexes, containment scan
  CHANGELOG.md                — amendment history

chapters/            — 7 directories: 00-introduction, four body chapters
                       (01-review, 02-methodology, 03-experiments, 04-system),
                       05-conclusion, 06-appendices. Each with:
  briefs/              section briefs (writing specs)
  drafts/              generated text
  reviews/             review feedback
  translations/        Kazakh translations
  _superseded/         the six-chapter tree the volume was rebuilt from.
                       Not assembled; kept because REWRITE_MAP.md points every
                       new subsection back at the sections it replaces.

outline/
  MASTER_OUTLINE.md    what each chapter contains and may not claim
  REWRITE_MAP.md       the rewrite contract: provenance and word budget per
                       section, and the rules every section is held to
  TABLE_OF_CONTENTS_{EN,KZ}.md

literature/
  external/            36 literature cards (structured 18-section format)
  self/                6 self-citations (yesmukhamedov-*.md)
  non-peer-reviewed/   1 card (wikipedia-clahe.md)
  LITERATURE_INDEX.md  master index of all sources

glossary/
  GLOSSARY_EN.md       canonical English terms
  GLOSSARY_KZ.md       Kazakh translations

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

**The volume was restructured from six chapters to four** and rewritten against the norms measured
across the 16 dissertations this council has published (`council/en/10-dissertation/peer-norms.md`).
Main text 31,258 words, 24 second-level subsections, 19 tables, 16 figures, five appendices, 99
sources. The gate is `scripts/conformance.py`; it passes 15 of 16 over the assembled manuscript, and
a chapter is not finished until it does.

- 00-introduction: written last, as the map requires. One continuous section, eleven bold run-in
  rubrics, unnumbered and not listed in the contents. No hypothesis rubric and no separate
  empirical-basis rubric: neither has a precedent in the corpus, and both are dissolved into prose.
- 01-review → 05-conclusion: written in the order 3 → 2 → 1 → 4 → introduction → conclusion, so the
  chapter carrying the results fixed the register and the table budget for the rest.
- 06-appendices: A source code · B supplementary results · C architecture diagrams · D attention-map
  gallery · E device supplementary tables. Kazakh lettering А, Ә, Б, В, Г. The old publication
  appendix is deleted: reprints and indexing screenshots appear in none of the 16.

**Two things bind anything written from here.** The main text is **258 words over** the corpus
ceiling of 31,000, so anything entering the body has to displace more than itself. The three words
of headroom this file used to record were an artefact of the gate: it modelled a printed citation as
one word, but a narrative citation keeps its author phrase and prints as four (`Gulshan et al.
[13]`), so the volume was 261 words longer than measured all along. The gate now counts the printed
form, and `conformance.py` is where to look for what to cut. And every claim taken from a source
names it — the compression pass dropped 90 per cent of the attribution once already, and restoring
it was a separate pass over every section.

Kazakh translations of the new tree are not yet written. The superseded volume's are under
`chapters/_superseded/**/translations/`; the new `translations/` directories are empty, and
`assembly/_assemble_kz.py` reads those.

Experimental chapters are written from `results/` (`findings/`, `tables/`, `hypotheses/`), which is the
single source of truth for every number and verdict. Where an earlier draft conflicts with `results/`,
`results/` wins and the draft is revised. `results/` provenance (run dates, recomputation history,
artifact paths) never enters the prose — system-prompt rule 16.

## Hypotheses

- H-1: Integrated Pipeline Dominance (Exp 1, EyePACS 100%; integrated arm = ophthalmology-SSL, composite IV, CFC-2.8)
- H-2: Component Ablation + CLAHE/σ sweeps (Exp 2, EyePACS)
- H-3: **Domain-Shift Reduction** (section 3.4) — MMD/FID over penultimate-layer features (**primary**, sole basis of the criterion) + KL over channel histograms (**secondary, informational only**), six target domains. Criterion: **Σ PASS_S ≥ K = 5 of n = 6**, with `PASS_S ⟺ Δd(X) ≥ MCID_d = 0.0 ∧ CI⁻(Δd) > 0`; 1 000 bootstrap resamples; arms D − C (EfficientNet-B3); forward passes only, no training. **Mandatory protocol condition:** Stage 7 must use source-domain statistics — computing it from the target makes the test incomparable with H-4/H-6/H-7. **Restored in governance v7.1.0** — the label formerly denoted a *training-method comparison* dropped in V3; **that retirement stands and the label is reused**, so "H-3 dropped" in the superseded sections 2.3.2 and 3.3.3 refers to the retired hypothesis, not this one. Mechanistic, not clinical: it measures the middle term of the causal chain that H-4/H-6/H-7 approach only through its consequence.
- H-4: Cross-Dataset Transferability on APTOS 2019 (Exp 3, G ≥ 0.85)
- H-5: Explainability — Grad-CAM ALO/IoU (Exp 4, IDRiD + Clinical)
- H-6: Device Domain Shift (Exp 6, DDR/ODIR-5K/RFMiD)
- H-7: **External Clinical Performance** (Exp 5, IDRiD + Messidor-2) — reformulated in governance v7.0.0 from "Clinical Degradation Resistance". Criterion (form S): Δ wF1(integrated − baseline) ≥ MCID 0.050 with CI⁻ > 0 on **each** set. The retired Δ_drop form is descriptive only; no verdict may rest on it.

## Language

- Dissertation text: formal academic English
- Translations: Kazakh (in translations/ subdirectories)
- All governance docs: English
- Register: third person, past tense for results, present tense for definitions
