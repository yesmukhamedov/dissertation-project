# Dissertation Repository

**Automated Diabetic Retinopathy Diagnosis via Fundus Image Enhancement and CNN Classification**

Candidate: Yesmukhamedov N.S. | IITU Doctoral Programme

**Status: written, translated and exported.** 98 sections in each language, all approved.
The council-ready pair is built into `defense/docs/` — see `thesis/CLAUDE.md` for the
per-chapter status, which is the live record.

---

## Directory Map

| Directory | Purpose |
|-----------|---------|
| `governance/` | Epistemic constraint system — invariants, hypotheses, argument map, contributions. **Binding** |
| `methods/` | Methodology specifications — preprocessing pipeline, implementation details |
| `outline/` | Table of contents (EN + KZ) and master structural outline |
| `glossary/` | Terminological resources — English glossary and EN→KZ translation control |
| `literature/` | Source corpus — external cards, self-citation cards, and the master index |
| `literature/external/` | Third-party literature cards (`author-year[-qualifier].md`) |
| `literature/self/` | Own publications (`yesmukhamedov-venue.md`) |
| `chapters/` | Chapter drafts, one subdirectory per chapter, each with the brief/draft/continuity/review/translation quintet |
| `assembly/` | Assembly scripts (`_assemble_en.py`, `_assemble_kz.py`), citation application, and the dated citation-resolution records |
| `output/` | Council deliverables staged as Markdown — abstracts (EN/RU/KZ), front matter, reviewer reports, publications list. Rendered to GOST `.docx`/`.pdf` by the `council-docs` skill |
| `experiments/` | Experimental protocol and design documents |
| `prompts/` | AI pipeline templates — section briefs, writing prompts, verification, translation, revision (see `prompts/README.md`) |
| `assets/` | Figures, diagrams, exported images |

## Governance Files

INVARIANTS is the supreme authority: if any document conflicts with it, INVARIANTS wins.

| File | Purpose |
|------|---------|
| `governance/INVARIANTS.md` | Master constraint document (v7.0.0) — scope boundaries, forbidden claims, binding constraints |
| `governance/HYPOTHESIS.md` | Formal definitions of H-1 … H-7 (v7.1.0) |
| `governance/ARGUMENT_MAP.md` | Claim-evidence dependency DAG (v7.1.0) — PC-0 … PC-11, with PC-3 deliberately unused |
| `governance/CENTRAL_THESIS.md` | Single-paragraph thesis formulation with the `model = preprocessing + CNN` framing |
| `governance/CORE_OBJECTIVE.md` | Research objective, derived from §0.3 (which is authoritative) |
| `governance/CONTRIBUTIONS.md` | Contributions register (v7.1.0) — 4 primary + supporting SC-A … SC-I |
| `governance/RESEARCH_ARCHITECTURE.md` | Methodological blueprint (v7.0.0) |
| `governance/VERSION_SYNC.md` | Cross-file version register (v7.1.2) |
| `governance/VERSIONING_POLICY.md` | Bump scheme, detection regexes, containment scan |
| `governance/CHANGELOG.md` | Amendment history |

## Methods Files

| File | Purpose |
|------|---------|
| `methods/preprocessing-pipeline.md` | The canonical **8-stage** pipeline specification, with the design principle and the pipeline-as-model assertion |
| `methods/implementation.md` | Software stack, hardware config, training config, model definition, Grad-CAM with ALO |

## Naming Conventions

- **Literature cards**: `author-year[-qualifier].md` → `gulshan-2016.md`, `porwal-2018-idrid-dataset.md`
- **Self-citations**: `yesmukhamedov-venue.md` → `yesmukhamedov-scopus-q2.md`
- **All filenames**: lowercase, hyphens only, no spaces, no version suffixes (use git)
- **Governance files**: UPPER_CASE permitted (they act as project constants)

## Writing Pipeline

Every section was produced through the same loop:

1. **Section Brief** (planning) → compact instruction per section with governance bindings and source mappings
2. **Writing Session** (generation) → section text + Continuity Note + Compliance Checklist
3. **Verification** (review) → governance compliance audit, ending in an APPROVED verdict
4. **Revision** (if needed) → targeted fixes with continuity preservation
5. **Translation** (EN→KZ) → controlled translation per GLOSSARY_KZ.md
6. **Translation Review** → terminology and register verification

Templates are in `prompts/`. Assembly input builder: `scripts/assemble-session-input.py`;
manuscript assembly: `assembly/_assemble_{en,kz}.py`.

Experimental chapters are written from `results/`, which is the single source of truth for
every number and verdict. Where a draft conflicts with `results/`, `results/` wins.
