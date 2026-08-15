---
name: abstract-annotation-alignment
description: thesis/output abstracts (EN/RU/KZ) restructured to match REAL IITU peer authorefarat samples (not just the council template)
metadata:
  type: project
---

The trilingual аннотация/abstract (`thesis/output/abstract_{en,ru,kz}.md`) was aligned on
2026-06-18 to the **real authorefarat samples** of IITU doctoral candidates in
`D:/dissertation_council/Образцы документов/авторы/` (Tokhtakhunov, Daurenbayeva, et al.),
**not just** the council template `council/en/11-abstract-annotation/structure.md`. The template
diverged from what candidates actually submit — trust the real samples for the section set/order.

Canonical structure now (all 3 languages, kept fully parallel — 20 `##` sections, identical order):
title (`# ABSTRACT` / `# АННОТАЦИЯ` / `# АҢДАТПА` — **no "(АВТОРЕФЕРАТ)"**) + bold descriptor →
General characteristics of the research → Relevance → Aim → Objectives → Object → Subject →
Methodology and methods → Empirical (experimental) basis → Scientific novelty → Main results →
Statements for defense → Theoretical significance → Practical significance → Reliability →
Approbation + connection with scientific programmes → **Publications (with the numbered works list
folded inline)** → Main content of the work (chapter overview) → Author's personal contribution →
**ends on Structure and length of the dissertation**.

Removed as отсебятина / template-isms that real samples don't have (flagged by the candidate):
- `(АВТОРЕФЕРАТ)` subtitle (was pre-existing in RU/KZ, not from samples).
- Umbrella `# GENERAL CHARACTERISTICS OF THE WORK` heading.
- Separate `# CONCLUSION` / `ЗАКЛЮЧЕНИЕ` / `ҚОРЫТЫНДЫ` section.
- Trailing standalone `LIST OF PUBLISHED WORKS` section (list moved into Publications, in the body).

Content added per samples + real RK normative docs: state-programmes (AI Concept 2024–2029,
President's Address «Kazakhstan in the Era of AI» 8 Sep 2025, Law «On AI» No. 230-VIII 17 Nov 2025,
Law «On Science» art. 20); "Author's personal contribution" section; "General characteristics" lead
para. KZ terminology fixed: Latin "pipeline" → "конвейер" (correct case forms; sentence-start caps).

OUTSTANDING: Scopus **percentile** (have Q3 only). Build via [[council-docs-skill]] → `defense/docs/abstracts/`.
NOTE: `defense/docs/**/*.docx` lock if open in Word — close before rebuild.

## Currency pass against the finished manuscript — 2026-08-13

The abstracts were resynchronised against the approved Chapter-0 sections (§0.2–§0.16) and §7, which are
authoritative; **six factual defects** were fixed, in all three languages at the same line positions:
1. **The Aim asserted its own result** ("producing a statistically measurable and reproducible improvement").
   §0.3 states the goal neutrally — *what difference the specification makes*. An aim that presupposes the
   finding contradicts the pre-registration argument the whole reliability section rests on.
2. **"Classical computer-vision detection" for OD/fovea** — the detector is a pre-trained, frozen
   heatmap-regression model, not co-trained with the classifier ([[od-fovea-heatmap-detector-plan]], §0.7).
3. **"Implementation acts and approbation certificates: see appendices"** — *no such documents exist*.
   Appendices are A–F and App D holds only the publication/indexing record. Replaced with an App-D pointer.
4. **The Kazakh clinical set was described as "qualitative validation"** — that examination was never carried
   out (G-3); its real use is training in a data-scarce regime (Exp 7).
5. **Structure-and-length gave no volume at all** — the template requires it. Now carries §0.16's figures.
6. Missing: the ~53,576-image unlabelled pretraining split (SB-2.4 disjointness), the §0.15 "correspondence,
   not funding/commission/mandate" disclaimer, and §0.13's third reliability qualification.
Also: Main results now state the seven hypothesis outcomes with their fences (they previously said only that
each was "evaluated"); novelty gained the cumulative-ablation item, the two non-empirical contributions, and
the SIR-4 lineage on CLAHE; the H-7 margin is given as 0.0041 per §0.8.

**Page figures stated: 265 pp in ALL THREE abstracts** (264 until the 2026-08-14 rebuild; source of record is `council/METADATA.toml`), with 42 tables, 26 figures, 2 diagrams and 107
sources, all excluding appendices. The defense is held in Kazakh, so the Kazakh edition is the defended
volume and every abstract cites *its* extent regardless of the abstract's own language — the English one
included. See [[defense-language-kazakh]] for why §0.16 of the English manuscript still says 238 and must
not be synced to this figure.

⚠ **The 15-page cap (§6.9 of the Statute) is the binding constraint on any edit.** Density differs sharply
by language: EN ≈ 400 words/page, **RU/KZ ≈ 285–290**. The first, fuller revision produced 15/18/17 pages and
had to be cut back twice. Final: **EN 13 pp / RU 15 / KZ 15** at 5110 / 4572 / 4375 words. RU and KZ are **at
the cap** — any future addition there must be paid for by a cut. Enrichment that was dropped for space (kept
in this note so it is not re-attempted blindly): the expanded five-part theoretical significance, the
four-part practical significance with the ingestion protocol and the disowned national projections, and the
"principal finding is consistency" closing paragraph from §7.
