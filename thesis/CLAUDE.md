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
Main text 31,496 words, 24 second-level subsections, 19 tables, 16 figures, six appendices, 102
sources. The gate is `scripts/conformance.py`, and a chapter is not finished until it passes.
Both editions pass in full: English 17 of 17, Kazakh — the defended edition — 20 of 20. The Kazakh
em-dash failure this file used to record is closed: the copula is written with the short dash the
corpus uses, and the check now reads 0.0 per 1,000 words.

**Four checks were added on 2026-08-23** after an external reading of the Kazakh PDF
(`D:/personal/phd/council/temp/АНАЛИЗ_A17_Есмухамедов.md`); see governance CHANGELOG v7.2.1.

- **governance labels in front matter.** The body scan starts at the Introduction, so everything
  above it — normative references, definitions, abbreviations — was never read by anything. Eight
  labels (PC/CFC/EH/SIR/DGL/SB/NC/OD-n) survived there, defined and used nowhere. The apparatus
  binds from `governance/INVARIANTS.md`; it does not appear in the volume. Nothing above the
  Introduction may carry a code.
- **Kazakh register (KZ only).** `et al.` is **«т.б.»**, never the calque «және әріптестері»;
  «сондықтан» opens a sentence rather than following a comma (the idiomatic join is the causal
  suffix -дықтан/-діктен); and no single connective may take more than half the family
  («Демек», «Сондықтан», «Сонымен», «Осылайша», «Яғни», «Тиісінше», «сол себепті»). The Kazakh
  edition is a translation of the English one, which is precisely why English syntax can survive
  under Kazakh words — these three are where it showed.

The GOST export was run on 2026-08-23 and the council pair is
`defense/docs/FULL_DISSERTATION_{EN,KZ}_GOST_2026-08-23.{docx,pdf}` — **130 pages EN / 143 KZ**,
102 and 113 of them ahead of the appendices. Each edition's Introduction states its own page count,
so the counts and the export are a fixed point: change one and the other has to be re-measured; this
run was done twice and the second pass reproduced the counts the Introduction now declares. The
volume lost five pages per edition against 2026-08-21 (107/118) when the illustration height was
capped — eleven of the twenty-seven figures had been taking a page each; the four structural
Mermaid views of Appendix C keep the full-page allowance.
The umbrella `APPENDICES`/`ҚОСЫМШАЛАР` divider is no longer assembled — it was the one top-level
heading with no body of its own and printed as a lone word on a blank page — so the appendices
open straight at Appendix A, and the main text is bounded by that heading rather than by a divider.
Rebuild it with the eight builders in `.claude/skills/council-docs/scripts/`, in the order recorded
in `PROJECT_MEMORY/gost-export-toolchain.md`.

- 00-introduction: written last, as the map requires. One continuous section, eleven bold run-in
  rubrics, unnumbered and not listed in the contents. No hypothesis rubric and no separate
  empirical-basis rubric: neither has a precedent in the corpus, and both are dissolved into prose.
  **Re-aligned to the corpus on 2026-08-22** against `D:/personal/phd/council/temp/` (the sixteen
  introductions and `АНАЛИЗ_ВВЕДЕНИЙ.md`): the provisions and novelty rubrics carried **no digits at
  all** where the corpus median is 5.0 and 1.8 per 1,000 characters, so every provision now states
  the effect size its criterion was fixed on, from `results/`. The evidential bounds moved to the
  reliability rubric — the corpus hedges a provision in 1 of 16, and the provisions now read as
  assertions with nothing dropped. A personal-contribution sentence was added (all five publications
  are co-authored, the candidate is not first author on two, and 3 of 16 give the statement its own
  rubric); the publications gained journal, volume, pages and indexing status, which took them from
  the thinnest record in the corpus to its norm and resolved all five to `[1]`–`[5]`; and the chapter
  overview roughly doubled, against a corpus median of 14.1 per cent of the introduction. The
  additions were paid for inside the introduction, out of the four rubrics measured furthest above
  the corpus — novelty, provisions, framework, significance — so the volume did not grow.
- 01-review → 05-conclusion: written in the order 3 → 2 → 1 → 4 → introduction → conclusion, so the
  chapter carrying the results fixed the register and the table budget for the rest.
- 06-appendices: A source code · B supplementary results · C system architecture **and the working
  demonstrator** · D attention-map plates · E device supplementary tables · **F the certificate of
  state registration of the software complex** (added 2026-09-06; scan in
  `ip/kazpatent/certificate/`, plates `defense/figures/certificate_{kz,ru}.png`). Kazakh lettering
  А, Ә, Б, В, Г, Ғ. The old publication appendix is deleted: reprints and indexing screenshots appear
  in none of the 16. **Reworked 2026-08-22** against `D:/personal/phd/council/temp/АНАЛИЗ_ПРИЛОЖЕНИЙ.md`
  (10 of the 16 have appendices at all; 5–28 pages; the median single appendix is **one** page):
  Appendix D went from 54 plates to **four** (IDRiD_007, 017, 020, 050) and its exhaustiveness
  argument was replaced by a declared selection, and Appendix C gained **C.5**, three screenshots of
  the demonstrator (`defense/figures/1–3.png`) — the corpus's "screenshots of the delivered system"
  type, which 3 of the 10 use. The block fell from 39/40 pages to 29/30. ⚠ The Kazakh figure markers
  keep Latin letters (`FIG-D.n`, `FIG-C.n`), so appendix В prints "Сурет D.1": `md2gost._FIG` matches
  `[A-Za-z]` only and a Cyrillic letter in a marker would print raw.

**Two things bind anything written from here.** The gate ceiling is **31,500** words of main text
(raised from 31,000 by the candidate on 2026-08-21) and the English edition stands at **31,496** —
**4 words of headroom**, so anything entering the body has to displace very nearly itself. The
certificate line added to the Introduction on 2026-09-06 cost +1 word net: it was paid for by
merging three restatements (the novelty opener, the significance opener and the closing sentence of
the personal-contribution paragraph), which is the only kind of room left.
`conformance.py` counts a printed citation the way it prints: a parenthetical collapses to `[12]`,
but a narrative citation keeps its author phrase and prints as four words (`Gulshan et al. [13]`).
It is where to look for what to cut. And every claim taken from a source names it — the compression
pass dropped 90 per cent of the attribution once already, and restoring it was a separate pass over
every section.

Kazakh translations of the new tree are written: 35 files under `chapters/**/translations/`, one per
draft, assembled by `assembly/_assemble_kz.py` (34,963 PART-1 words, no suspect extractions).
Terminology follows `outline/TABLE_OF_CONTENTS_KZ.md` rather than the superseded tree — the
preprocessing pipeline is "алдын ала өңдеу конвейері", not the Latin "pipeline" the old volume kept,
and the arms are "базалық / интеграцияланған конфигурация". Numbers keep the old Kazakh volume's
conventions: decimal point, space as thousands separator. Citations stay in working author-year form
with Kazakh connectors (`т.б.` for *et al.*, `пен/мен/бен` for *and*), which
`_finalize_citations.py` already parses: a run over both partials converts 138 brackets in each and
reports no blocking or unknown resolutions. The calque `және әріптестері` is **not** the form —
it was replaced everywhere on 2026-08-23 and `conformance.py` now fails on it. Mermaid diagram source is left in English, as the superseded Kazakh volume left it.

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
