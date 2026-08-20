# MASTER OUTLINE
## Doctoral Dissertation: Automated Diabetic Retinopathy Diagnosis via Fundus Image Enhancement and CNN Classification

**Candidate:** Yesmukhamedov N.S.
**Document type:** structural specification of the volume — what each chapter contains, what it must state, and what it may not claim.
**Version:** 8.0.0
**Binding references:** INVARIANTS.md v7.1.0 · HYPOTHESIS.md v7.1.0 · ARGUMENT_MAP.md v7.1.0 · `council/en/10-dissertation/peer-norms.md`

> **This document specifies structure, not content.** The content of every section lives in its
> draft; where a draft and this outline disagree, the draft wins. Provenance — which superseded
> section feeds which new subsection, and at what word budget — is in
> [REWRITE_MAP.md](REWRITE_MAP.md). The heading list is [TABLE_OF_CONTENTS_EN.md](TABLE_OF_CONTENTS_EN.md).
>
> **Superseded planning material removed in this version.** Earlier revisions carried Scientific
> Novelty and Provisions lists that predated the experimental results and enumerated what was
> *planned* rather than what is defended. Those lists are gone; the drafted introduction rubrics are
> authoritative.

---

## The shape of the volume

Four chapters, in the order the corpus uses — review → methods → experiments → system — with two
levels of numbering and no third. Chapter architecture, heading depth and title length follow the
measured norms; the reasoning is in `council/en/10-dissertation/peer-norms.md`, sections 4 to 6.

| Unit | Subsections | Words | Pages |
|---|---:|---:|---:|
| Introduction | 11 run-in rubrics, unnumbered | 1,900 | ≈ 6 |
| 1 Automated diabetic retinopathy screening | 5 | 4,500 | ≈ 18 |
| 2 Methodology of the integrated pipeline | 6 | 6,500 | ≈ 26 |
| 3 Experimental results | 9 | 10,100 | ≈ 40 |
| 4 The screening system | 4 | 4,500 | ≈ 18 |
| Conclusion | — | 900 | ≈ 3 |
| **Main text** | **24** | **28,400** | **≈ 111** |

Declared volume is the main text excluding appendices, stated once in the Introduction's *Structure
and volume* rubric and repeated identically in the annotation, together with the figure, table and
source counts.

**Ceilings that bind the whole volume:** at most 20 tables in the body; the reference list at
100–150 sources over 8–11 pages; per-chapter numbering of figures and tables, one scheme
throughout; no section sign, no internal identifier, no editorial marker on any page.

---

## FRONT MATTER

**Normative references** — kept. The corpus omits this element in 10 of 16 and the norm is to drop
it unless the work genuinely cites standards; this one does, in the system chapter (the ST RK 34.0xx
automated-systems series, HL7) and in the front matter (GOST 7.32, GOST 7.1).

**Definitions** — from `glossary/GLOSSARY_EN.md`. The operationally defined terms carry their
verbatim definitions. Their internal identifiers do not appear.

**Designations and abbreviations** — the real abbreviations only. The governance codes declared here
in the previous version are removed along with the codes themselves; with none of them printed in
the body there is nothing left to gloss.

---

## INTRODUCTION — 1,900 words

Continuous prose with **bold run-in rubrics**, unnumbered, and absent from the contents below its
own line. Eleven rubrics in this order:

1. **Relevance of the research** — the clinical and epidemiological case, the Kazakhstan framing,
   the technical gap, closing on the link to the state programme.
2. **Research aim and objectives** — the aim, then the numbered objectives, under one heading. Each
   objective names the chapter that discharges it.
3. **Object and subject of research** — two sentences. The object is the process, not the images.
4. **Theoretical and methodological framework** — including the empirical basis: the corpora, their
   sizes and their provenance. No sample heads an "empirical basis" item separately.
5. **Scientific novelty.**
6. **Provisions submitted for defence** — each with the qualification inseparable from it, at the
   strength the pre-specified criterion supports.
7. **Theoretical and practical significance** — one rubric, not two.
8. **Reliability of the results.**
9. **Approbation of results and publications** — one rubric, not two.
10. **Connection with state programmes.**
11. **Structure and volume of the work** — the volume sentence plus a paragraph-per-chapter
    walkthrough.

**No hypothesis rubric.** The corpus uses the word only in its statistical sense and never carries a
labelled system of research hypotheses through a volume. The hypotheses are stated as prose inside
novelty and provisions — "the first hypothesis holds that…" — and the formal definitions stay in
`governance/HYPOTHESIS.md`, where they remain binding on what may be claimed.

---

## 1 AUTOMATED DIABETIC RETINOPATHY SCREENING — 4,500 words

The review chapter. It ends in the problem statement, which is the shape 15 of 16 samples give
Chapter 1. It absorbs the background half of the superseded theory chapter; no chapter of this
volume is given over to theory alone, because none of the 16 does that.

- **1.1 Diabetic retinopathy and screening demand** — pathophysiology, the clinical grading scales,
  and the screening requirement in resource-limited settings. Closes on the therapy the screening
  feeds: grading determines referral, referral determines laser coagulation, and about 300 words
  give the thermal-optical grounding of that therapy. **SB-1.5 binds** — qualitative computational
  grounding, cited to its source, never an experimentally validated clinical model.
- **1.2 Fundus image quality and variability** — sources of degradation in practice, the effect of
  quality on model performance, and the device-specific component.
- **1.3 Convolutional networks for retinal images** — architectures, transfer and in-domain
  pretraining, explainability methods.
- **1.4 Existing automated screening systems** — critical analysis. **CFC-2.9 binds**: the sources
  that leave preprocessing unformalised may be described by that methodological practice and never
  credited with a theoretical statement they do not make.
- **1.5 Problem statement and research direction.**
- *Conclusions on section 1.*

---

## 2 METHODOLOGY OF THE INTEGRATED PIPELINE — 6,500 words

The methods chapter, with the theory that grounds each method folded in beside it rather than
gathered into a chapter of its own.

- **2.1 Preprocessing pipeline formalisation** — the eight stages, stage by stage; the augmentation
  strategy; the external ingestion protocol; spatial filtering and noise reduction. **NC-15 binds**:
  the ingestion protocol is validated only on the named clinical corpus.
- **2.2 Contrast enhancement and flat-field correction** — histogram equalisation, the
  dual-constraint clip limit formalised, and the modified algorithm as implemented. Theory and
  method are one subsection here because separately they state the same thing twice.
- **2.3 Classification architectures and adaptation** — the two backbones, convolution and pooling,
  regularisation, and the adaptation to five-class output.
- **2.4 Pretraining and fine-tuning strategy** — feature transferability, in-domain self-supervised
  pretraining, the two-stage protocol, and the weighted loss for the ordinal class structure.
- **2.5 Explainability and quality metrics** — the attention-map formalism, its interpretation, the
  overlap measures, and the image-quality metrics. **NC-14 binds**: an attention map is an
  interpretability tool, not a pixel-level diagnostic delineation.
- **2.6 Evaluation and statistical protocol** — the multi-metric framework, the acceptance
  thresholds, cross-validation and the reliability protocol.
- *Conclusions on section 2.*

---

## 3 EXPERIMENTAL RESULTS — 10,100 words

The results chapter, carrying the statistical validation and the comparison against published work
as subsections. No sample has a validation chapter, and comparative analysis is a subsection
everywhere it occurs.

- **3.1 Datasets and experimental configuration** — the corpora, class distribution, partitioning,
  hardware and the reproducibility protocol.
- **3.2 Effect of the pipeline on accuracy** — the factorial contrast, training dynamics, and the
  quantitative comparison. **CFC-2.8 binds and must be stated where the result is stated**: the two
  arms differ in initialisation as well as preprocessing, so the effect belongs to the integrated
  configuration as a whole and never to preprocessing alone.
- **3.3 Stage ablation and parameter sensitivity** — cumulative ablation and the two parameter
  sweeps. **NC-17 binds**: the component hierarchy is bounded to the tested architectures and
  corpus.
- **3.4 Domain distance in feature space** — the measurement protocol and what the reduction does
  and does not license. Mechanistic, not clinical.
- **3.5 Cross-dataset and external transfer** — the external corpora, written once as one protocol
  with three sets of results rather than three times over. **NC-16 binds**: cross-device results are
  not device certification.
- **3.6 Attention maps and lesion agreement** — generation, the overlap measures against expert
  annotation, and per-image consistency.
- **3.7 Training on small clinical samples.**
- **3.8 Statistical validation and comparative analysis** — intervals, the mixed-effects model, the
  strength assigned to each claim, the placement against published systems, and the
  performance–cost relation. **CFC-2.2 binds**: placement, never ranking, absent a direct controlled
  comparison under identical conditions.
- **3.9 Limitations and boundary conditions.**
- *Conclusions on section 3.*

Forbidden throughout: universal generalisation (CFC-2.1), deployment outcomes stated as results
(CFC-2.3), validated clinical claims (CFC-2.4), perfect-performance generalisation (CFC-2.5),
amplification of a source beyond its own text (CFC-2.6), and retroactive re-characterisation of
prior self-publications (CFC-2.7).

---

## 4 THE SCREENING SYSTEM — 4,500 words

**What was built**, not what was required. The corpus's system chapter describes architecture,
interface, deployment and screenshots; none of the 16 specifies requirements, and a requirements
chapter placed after the experiments has no precedent at all.

- **4.1 System architecture and modules** — the modules as built, and their integration surfaces.
- **4.2 Preprocessing and inference services** — the configurable preprocessing engine and the
  inference service with model selection.
- **4.3 Clinical workflow and operator interface** — the physician-in-the-loop interface, the case
  record it keeps, and support for telemedicine and portable devices. The three fourth-level items
  of the superseded chapter are dissolved into prose: a fourth numbering level occurs in 0 of 16.
- **4.4 Deployment and data protection.**
- *Conclusions on section 4.*

**SB-4.1, as amended:** a working demonstrator is deployed and performs inference on submitted
images. **SB-4.2 stands** — the compliance framing is a design specification, not a certified
compliance status. **SB-4.3 stands** — applicability to Kazakhstan healthcare infrastructure is
bounded by the absence of field testing in Kazakhstan clinical settings. Both must be stated where
the corresponding claims appear.

---

## CONCLUSION — 900 words

Outcomes, contributions and directions for further work. Bounded above by the conclusions of
Chapter 3 and by the provisions submitted for defence: the conclusion may not exceed either. No
metric value appears in it.

---

## APPENDICES

A source code · B supplementary results and confusion matrices · C system architecture diagrams ·
D attention-map gallery · E device domain-shift supplementary tables. Kazakh lettering **А, Ә, Б,
В, Г**.

Appendix B grows, taking the per-class and per-run detail displaced from Chapter 3 by the 20-table
ceiling.

**Nothing about the publication record goes here** — no reprints of the candidate's own articles, no
screenshots of indexing databases, no restatement of the list of publications. None of the 16 does
any of these. The record is carried by the *Approbation and publications* rubric of the Introduction
and of the annotation, and by the separate List of scientific papers, which is what the council
reads for indexing and quartile.

---

## Related

- [REWRITE_MAP.md](REWRITE_MAP.md) — section-by-section provenance and word budgets.
- [TABLE_OF_CONTENTS_EN.md](TABLE_OF_CONTENTS_EN.md) · [TABLE_OF_CONTENTS_KZ.md](TABLE_OF_CONTENTS_KZ.md)
- `../scripts/conformance.py` — the gate that measures a built manuscript against the norms.
- `../governance/INVARIANTS.md` — supreme authority on what may be claimed.
