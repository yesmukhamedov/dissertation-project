---
name: abstract-annotation-alignment
description: thesis/output abstracts (EN/RU/KZ) restructured to real IITU peer samples, and resynced 2026-08-20 to the four-chapter volume (117 pp / 19 tables / 16 figures / 99 sources)
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

## Resync to the four-chapter volume — 2026-08-20

All three abstracts were brought level with the rewritten volume ([[four-chapter-rewrite]]).
Seven classes of desync were closed, at identical positions in EN/RU/KZ:

1. **Volume figures** — 265 pp / 42 tables / 26 figures / 2 diagrams / 107 sources →
   **117 pp / 19 tables / 16 figures / 99 sources**, diagrams dropped (the four structural
   views live in an appendix and the counts exclude appendices). The Kazakh figure still
   governs all three abstracts, per [[defense-language-kazakh]]; registry `council/METADATA.toml`.
2. **Objectives** — six, one per old chapter → **four**, mirroring the introduction.
3. **Main content of the work** — six chapter paragraphs → **four**, titled from
   `outline/TABLE_OF_CONTENTS_{EN,KZ}.md` (RU titles translated to match).
4. **Structure rubric** — six chapters and six appendices (A–F) → four chapters and five
   appendices; EN «A–E», KZ «А, Ә, Б, В, Г», RU unlettered (Russian letters would clash with Ә).
5. **The publication/approbation appendix no longer exists** — both pointers to «Appendix D»
   removed (Practical significance, Approbation); the five works stay listed in Publications.
6. **«No prototype was implemented» is now false** — SB-4.1 was amended in INVARIANTS v7.1.0
   and Chapter 4 describes a **deployed working demonstrator**. Fixed in four places per
   language (novelty 12, main result 9, provision 11, Practical significance), each keeping
   the bound: it establishes realisability and operating behaviour, is evidence for no
   diagnostic claim, and the deployment-oriented parts remain specification.
7. **Governance codes H-1…H-7 removed** (24 per language) — the rewritten volume carries
   **zero** of them (the hypothesis rubric was dissolved as having no corpus precedent), so
   each «(H-5)» pointed at nothing a council reader could find. The outcomes and their
   qualifications stay; only the labels went. **P1/P2 were kept** — the abstract defines
   those itself, so they are not dangling; removing them is available but was not done.

Also KZ only: **«біріктірілген» → «интеграцияланған»** throughout (26 occurrences) — the
translated volume settled on the latter for the integrated arm, and keeps «біріктірілген»
for its other sense, *pooled* (pooled folds).

**The 15-page cap still binds and is still met**: rebuilt EN 13 / RU 15 / KZ 15 pp
(5241 / 4652 / 4427 words) via `build_all.py --only abstract_en abstract_ru abstract_kz`,
run under **system Python 3.13**, not the demo venv. `check_metadata.py` reports nothing new.

⚠ **The same desync is still open in the council reviews**: both official reviewers reports
(six files) and the supervisor review describe a six-chapter volume of 265 pp with 42 tables,
26 figures and 107 sources, and reason chapter by chapter over the old structure — a rewrite,
not a numeric patch. The foreign consultant review is **signed and dispatched**
([[foreign-consultant-dispatch]]) and must not be re-edited.
