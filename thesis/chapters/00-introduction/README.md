# Introduction

**Status:** ✅ COMPLETE — 16/16 sections (13 drafted here + 3 front-matter units already complete in `thesis/output/`)
**Depends on:** Chapters 1–6 drafted and approved; final claim strengths from §5.2.2 (TAB-5.2)
**Chapter function:** Synthesis — relevance, novelty, goal, objectives, hypotheses, provisions for defence
**Governance bindings:** IT-1, H-1…H-7, PC-0…PC-11, all SB/DGL constraints, **SB-1.12 / CFC-2.9 / SIR-9**, **CFC-2.8**, **SIR-4/SIR-5/SIR-8**, **PC-0**

---

## Section register — identifiers and manuscript order

Two orderings are in play and they differ; both are recorded here so neither is lost.

- **Section identifiers** (`0.N`) follow `thesis/PLAN.md` and are **stable**. In particular **§0.8 = Provisions Submitted for Defence**, which is how the gate is referenced in `PLAN.md`, in `governance/`, in `PROJECT_MEMORY/`, and in `continuity/5.C-continuity.md`. Identifiers are not renumbered.
- **Manuscript order** follows `outline/TABLE_OF_CONTENTS_EN.md`, which is house-aligned to the IITU samples and is authoritative for the assembled document. It is **not** the numeric order of the identifiers.

`MASTER_OUTLINE.md`'s Introduction ordering matches the identifiers, not the TOC; the TOC is the later and house-verified artifact and wins for the manuscript. Four TOC items had no identifier in `PLAN.md` and receive §0.13–§0.16.

| Manuscript position | Section | ID | Words | Status |
|---|---|---|---|---|
| — | NORMATIVE REFERENCES | §0.FM1 | — | ✅ exists as `thesis/output/normative_references_{en,kz}.md` |
| — | DEFINITIONS | §0.FM2 | — | ✅ exists as `thesis/output/definitions_{en,kz}.md` |
| — | DESIGNATIONS AND ABBREVIATIONS | §0.FM3 | — | ✅ exists as `thesis/output/abbreviations_{en,kz}.md` |
| 1 | Relevance of the Research | §0.1 | 800–1,000 | ✅ drafted |
| 2 | Research Goal | §0.3 | 300–500 | ✅ drafted |
| 3 | Research Objectives | §0.4 | 400–600 | ✅ drafted |
| 4 | Object and Subject of Research | §0.5 | 200–400 | ✅ drafted |
| 5 | Research Hypothesis | §0.6 | 600–900 | ✅ drafted |
| 6 | Scientific Novelty | §0.2 | 800–1,000 | ✅ drafted |
| 7 | Provisions Submitted for Defence | §0.8 | 700–900 | ✅ drafted |
| 8 | Methodological Basis | §0.7 | 400–600 | ✅ drafted |
| 9 | Theoretical Significance | §0.9 | 300–500 | ✅ drafted |
| 10 | Practical Significance | §0.10 | 300–500 | ✅ drafted |
| 11 | Reliability of the Results | §0.13 | 300–500 | ✅ drafted |
| 12 | Empirical (Experimental) Basis | §0.14 | 300–500 | ✅ drafted |
| 13 | Approbation of Research Results | §0.11 | 200–300 | ✅ drafted |
| 14 | Connection with Scientific Programmes | §0.15 | 150–250 | ✅ drafted |
| 15 | Publications | §0.12 | 200–300 | ✅ drafted |
| 16 | Structure and Length of the Dissertation | §0.16 | 250–400 | ✅ drafted |

**Front matter is not re-written here.** The three front-matter units already exist as EN/KZ deliverables in
`thesis/output/`, verified against the real IITU samples and exported to GOST `.docx`/`.pdf`. Phase 3
inserts them ahead of the Introduction; no draft is produced under `drafts/`.

**Phase-3 assembly note.** `assembly/_assemble_en.py` orders drafts by numeric section key. For every
other chapter that equals TOC order; **for Chapter 0 it does not**. Chapter 0 must be assembled from an
explicit ordered list matching the table above, not from a numeric sort.

**Artifact-set note.** Every section has its own `briefs/` and `drafts/` file. The seven substantive
sections (§0.1, §0.2, §0.3, §0.4, §0.5, §0.6, §0.8) each carry their own `continuity/` and `reviews/` file.
The nine short apparatus sections (§0.7, §0.9, §0.10, §0.11, §0.12, §0.13, §0.14, §0.15, §0.16) are verified
and handed off **as one block** — `reviews/0.apparatus-review.md` and `continuity/0.apparatus-continuity.md`
— because they share one binding set and the risks that matter run across them rather than within any one.
Precedent: §6.3.1, verified as a single unit covering three subsections. The block review carries a
per-section traceability table.

---

## Binding content constraints for this chapter

### Position ceiling (from `continuity/5.C-continuity.md`)

The Introduction may not exceed the position Chapter 5 fixed. What the evidence supports: a controlled
comparison between two configurations under identical conditions, replicated across architectures,
decomposed across stages, accompanied by a measured reduction in distributional distance, and consistent
on every corpus and camera grouping examined in both training regimes. What it does not support: clinical
validity, deployment readiness, device certification, lesion localization, superiority over any published
system, or extension beyond the corpora and hardware used.

### The eight fences

Every one of them must survive into the Introduction, and compression is where they are lost:

1. **CFC-2.8** — the composite is *decomposable, not dissolved*: the cumulative ablation under one
   initialization reproduces the whole in-domain gain, but configurations B/D remain differently
   initialized from A/C. No preprocessing-alone attribution under H-1.
2. **PC-8** — the stage hierarchy holds at **grouping resolution only**, never as a strict 1-to-7 ranking.
3. **H-3** — **direction only**; magnitude does not track transfer gain.
4. **H-5** — **quantitative half only**; the clinical overlays were never produced (G-3).
5. **H-7** — **performance, not resistance**; the Messidor-2 margin over the MCID is thin.
6. **H-4 / H-6** — the thresholds are cleared by **both** arms; the evidence is in the comparison.
7. **E-7** — the small-data gain is **comparable to, not larger than**, the abundant-data gain.
8. Two of the five camera groupings **are** the external corpora themselves — not independent replication.

### Paradigmatic framing (Task 2.8, retained from the original chapter spec)

- **Landmark mention.** Gulshan et al. (2016, *JAMA*) is introduced as the *landmark study that opened the
  era of CNN-based diabetic retinopathy screening*. This is permissible under SB-1.12 because it
  characterises the source's historical position, not its numerical figures.
- **Pre-introduction of P1/P2.** The Introduction pre-introduces the P1 vs P2 contrast at a high level in
  one short paragraph, so the reader arrives at §1.4 already primed. The methodological-practice grounds
  belong to §1.4 and the Gulshan card §15, not here.
- **Forbidden phrasings** (CFC-2.9, SB-1.12, CFC-2.2): "Gulshan is our baseline"; "we outperform Gulshan";
  "Gulshan claimed preprocessing is unimportant"; "the present work surpasses Gulshan"; any framing that
  conflates Gulshan with the operational baseline of OD-3.
- **Permitted phrasings:** "Gulshan et al. (2016) is taken in this dissertation as the canonical
  representative of the end-to-end CNN paradigm (P1)"; "the present dissertation reframes preprocessing as
  an integral model component, operationalising the integrated preprocessing-CNN paradigm (P2)"; "the
  principal conceptual contribution of this work is the P1 → P2 paradigm shift, supported empirically by
  Experiment 1 under matched conditions."

### Governance currency

Where `outline/MASTER_OUTLINE.md` (v6.0.0) conflicts with the current governance, the current governance
wins and the outline is stale. Three known instances bind this chapter:

- **H-3 is live**, as *Domain-Shift Reduction* (HYPOTHESIS v7.1.0). The outline's "H-3 [DROPPED V3]" refers
  to the retired **training-method** hypothesis and must not be carried into §0.6.
- **H-7 is the External Clinical Performance form** (INVARIANTS v7.0.0). The retired Δ_drop degradation
  form is descriptive only and may not appear as a provision or a hypothesis statement.
- The **novelty list and provisions list in the outline predate the results** and both omit H-3; §0.2 and
  §0.8 are written from `governance/CONTRIBUTIONS.md` v7.1.0 and `results/tables/TAB-5.2` instead.

---

## Sections (per outline/TABLE_OF_CONTENTS_EN.md, v6.0.0)

Front matter precedes the Introduction: NORMATIVE REFERENCES · DEFINITIONS · DESIGNATIONS AND ABBREVIATIONS.

# INTRODUCTION
- Relevance of the Research
- Research Goal
- Research Objectives
- Object and Subject of Research
- Research Hypothesis
- Scientific Novelty
- Provisions Submitted for Defense
- Methodological Basis
- Theoretical Significance
- Practical Significance
- Reliability of the Results
- Empirical (Experimental) Basis
- Approbation of Research Results
- Connection with Scientific Programmes
- Publications
- Structure and Length of the Dissertation
