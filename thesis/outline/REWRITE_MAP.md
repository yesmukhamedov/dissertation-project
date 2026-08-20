# REWRITE MAP — where every existing section goes

**Binding contract for the rewrite.** The volume is being rebuilt to the norms measured across all
16 dissertations this council has published (`council/en/10-dissertation/peer-norms.md`): six
chapters become four, the numbering stops at two levels, and the main text comes down from
101,459 words to ≈ 28,000 — the top of the observed band (corpus 15,200 – 22,700 – 31,000), chosen
so that the whole argument survives in compressed form rather than being cut away.

Every one of the 98 drafted sections has a line here. Nothing is rewritten without one, so nothing
is silently lost, and the word budgets sum to the target rather than being decided section by
section as the work goes.

Source paths are `thesis/chapters/_superseded/<chapter>/drafts/<file>`; destinations are
subsections of the new tree. **Words** columns are the source's PART-1 body and the budget for the
text that replaces it.

---

## Totals

| New unit | Sources | Source words | Budget |
|---|---:|---:|---:|
| Introduction | 16 | 10,003 | 1,900 |
| 1 Automated diabetic retinopathy screening | 12 | 13,143 | 4,500 |
| 2 Methodology of the integrated pipeline | 26 | 27,281 | 6,500 |
| 3 Experimental results | 30 | 51,232 | 10,100 |
| 4 The screening system | 9 | 8,238 | 4,500 |
| Conclusion | 1 | 1,616 | 900 |
| **Main text** | **94** | **111,513** | **28,400** |
| Appendices (not in the declared volume) | 6 → 5 | 8,705 | ≈ 6,000 |

Compression is ≈ 4:1 and is achieved on the paragraph, not by dropping findings: the corpus
paragraph is 36 words and ours is 115, the corpus sentence 18 and ours 30. A paragraph rewritten to
two or three sentences making one point carries the same claim at a third of the length. Sections
marked **CUT** are the exception and are listed with the reason.

---

## Introduction — 1,900 words

Eleven **bold run-in rubrics**, unnumbered, not listed in the contents (corpus: 8–11 rubrics, all
16 samples). The current sixteen numbered sections are merged down. Two rubrics have no precedent
anywhere in the corpus and are dissolved rather than renamed: a named *Research hypothesis* item and
a separate *Empirical basis*.

| Source | Words | → Rubric | Budget |
|---|---:|---|---:|
| `0.1-draft.md` Relevance of the Research | 1,134 | **Relevance of the research** | 260 |
| `0.3-draft.md` Research Goal | 542 | **Research aim and objectives** — aim and the numbered objectives under one heading | 240 |
| `0.4-draft.md` Research Objectives | 701 | ↑ same rubric | — |
| `0.5-draft.md` Object and Subject | 295 | **Object and subject of research** — two sentences | 70 |
| `0.7-draft.md` Methodological Basis | 630 | **Theoretical and methodological framework** | 180 |
| `0.14-draft.md` Empirical (Experimental) Basis | 502 | ↑ folded in — no sample heads this separately | — |
| `0.2-draft.md` Scientific Novelty | 1,213 | **Scientific novelty** | 280 |
| `0.8-draft.md` Provisions Submitted for Defence | 1,262 | **Provisions submitted for defence** | 340 |
| `0.6-draft.md` Research Hypothesis | 1,209 | ↑ dissolved into novelty and provisions **as prose** — the corpus uses *hypothesis* only in its statistical sense, never as a labelled system carried through the body | — |
| `0.9-draft.md` Theoretical Significance | 501 | **Theoretical and practical significance** — one rubric, not two | 180 |
| `0.10-draft.md` Practical Significance | 449 | ↑ same rubric | — |
| `0.13-draft.md` Reliability of the Results | 486 | **Reliability of the results** | 120 |
| `0.11-draft.md` Approbation of Research Results | 280 | **Approbation of results and publications** — one rubric, not two | 130 |
| `0.12-draft.md` Publications | 226 | ↑ same rubric | — |
| `0.15-draft.md` Connection with Scientific Programmes | 194 | **Connection with state programmes** | 70 |
| `0.16-draft.md` Structure and Length | 379 | **Structure and volume of the work** — rewritten to four chapters; declares main text excluding appendices, with figures, tables and sources in the same sentence | 230 |

Written **last**, because it must describe what the body ended up being.

---

## 1 Automated diabetic retinopathy screening — 4,500 words

The review chapter, ending in the problem statement — the shape 15 of 16 samples give Chapter 1.
Absorbs the background half of the old Chapter 2.

| New subsection | Budget | Sources | Words |
|---|---:|---|---:|
| **1.1 Diabetic retinopathy and screening demand** | 900 | `1.1.1` Pathophysiology and grading · `1.1.2` Screening in resource-limited settings · **`2.4.1` Coupled thermal-optical model → ≈ 300 w of therapeutic context** | 1,338 · 1,043 · 1,087 |
| **1.2 Fundus image quality and variability** | 900 | `1.2.1` Sources of degradation · `1.2.2` Quality and model performance · `1.2.3` Device-specific variability | 983 · 1,278 · 1,014 |
| **1.3 Convolutional networks for retinal images** | 1,000 | `1.3.1` CNN architectures · `1.3.2` Transfer and self-supervised pretraining · `1.3.3` Explainability methods | 1,352 · 1,046 · 857 |
| **1.4 Existing automated screening systems** | 900 | `1.4` Critical analysis | 1,720 |
| **1.5 Problem statement and research direction** | 500 | `1.5` Formulation of the research problem | 856 |
| *Conclusions on section 1* | 300 | `1.C` | 569 |

**The laser–tissue model stays, compressed.** The approved defence topic names support for laser
coagulation, and this is the volume's only laser content; cutting it would widen a gap already on
record. It moves out of the methodology — no experiment uses it — into 1.1, as the therapy that
grading and referral feed. SB-1.5 binds: qualitative computational grounding, cited to its source,
never an experimentally validated clinical model.

---

## 2 Methodology of the integrated pipeline — 6,500 words

The old Chapter 3 with the theory of the old Chapter 2 folded in. No sample gives theory a chapter
of its own: it sits inside the review chapter or inside the methods chapter, and here it is the
latter, next to the method each piece of it grounds.

| New subsection | Budget | Sources | Words |
|---|---:|---|---:|
| **2.1 Preprocessing pipeline formalisation** | 1,600 | `3.1.1` Eight-stage specification · `3.1.3` Augmentation strategy · `3.1.4` External ingestion protocol · `2.1.3` Spatial filtering and noise reduction | 2,631 · 936 · 818 · 845 |
| **2.2 Contrast enhancement and flat-field correction** | 1,100 | `2.1.2` Dual-constraint CLAHE formalisation **+** `3.1.2` the modified algorithm — theory and method merged, they state one thing twice · `2.1.1` Histogram equalisation | 1,535 · 997 · 1,485 |
| **2.3 Classification architectures and adaptation** | 900 | `3.2.1` ResNet-50 and EfficientNet-B3 · `3.3.1` Five-class adaptation · `2.2.1` Convolution and pooling · `2.2.3` Regularisation | 1,036 · 537 · 1,088 · 889 |
| **2.4 Pretraining and fine-tuning strategy** | 1,100 | `3.3.2` In-domain self-supervised pretraining · `3.3.3` Two-stage fine-tuning · `3.3.4` Weighted loss · `2.2.2` Loss functions for imbalanced data · `2.3.1` Feature transferability · `2.3.2` Frozen versus progressive · `2.3.3` In-domain SSL theory | 1,307 · 556 · 613 · 1,151 · 918 · 776 · 962 |
| **2.5 Explainability and quality metrics** | 800 | `2.5.1` Grad-CAM formalisation · `2.5.2` Attention-map interpretation · `2.5.3` ALO and IoU · `2.6` CNR, VVI, entropy, SSIM | 831 · 675 · 764 · 1,030 |
| **2.6 Evaluation and statistical protocol** | 700 | `3.4.1` Multi-metric framework · `3.4.2` Cross-validation and reliability | 1,300 · 866 |
| *Conclusions on section 2* | 300 | `2.C` + `3.C` merged | 601 · 624 |

**CUT — `3.2.2` Historical Reference Architectures (524 w).** Marked "reference only" in its own
title; it grounds no choice made in the work and no result reported from it.

---

## 3 Experimental results — 10,100 words

The old Chapter 4 with the whole of the old Chapter 5 folded in as subsections. No sample has a
validation chapter; comparative analysis against published work is always a subsection of the
experiments chapter, and statistical validation lives inside the results.

| New subsection | Budget | Sources | Words |
|---|---:|---|---:|
| **3.1 Datasets and experimental configuration** | 900 | `4.1.1` Dataset architecture · `4.1.2` Class distribution and partitioning · `4.1.3` Hardware and reproducibility | 1,473 · 920 · 809 |
| **3.2 Effect of the pipeline on accuracy** | 1,500 | `4.2.1` Factorial design · `4.2.2` Training dynamics · `4.2.3` Quantitative comparison | 1,948 · 1,926 · 2,692 |
| **3.3 Stage ablation and parameter sensitivity** | 1,600 | `4.3.1` Cumulative ablation · `4.3.2` CLAHE threshold sweep · `4.3.3` Flat-field sigma sweep | 2,300 · 2,232 · 2,169 |
| **3.4 Domain distance in feature space** | 900 | `4.4.1` Measurement protocol · `4.4.2` Results and interpretive limits | 1,861 · 2,571 |
| **3.5 Cross-dataset and external transfer** | 1,500 | `4.5.1`+`4.5.2` APTOS transfer · `4.7` IDRiD and Messidor-2 · `4.8` DDR, ODIR-5K, RFMiD — **three studies running one protocol three times, written once with three sets of results** | 1,447 · 1,395 · 1,745 · 1,713 |
| **3.6 Attention maps and lesion agreement** | 1,100 | `4.6.1` Generation protocol · `4.6.2` ALO and IoU against IDRiD masks · `4.6.3` Per-image consistency · `5.1` Explainability results | 1,574 · 1,685 · 1,421 · 2,117 |
| **3.7 Training on small clinical samples** | 600 | `4.9` Small-data training | 1,515 |
| **3.8 Statistical validation and comparative analysis** | 1,200 | `5.2.1` Bootstrap and mixed-effects · `5.2.2` Claim-strength classification · `5.3.1` Published systems · `5.3.2` Performance–complexity | 2,042 · 2,347 · 2,072 · 1,485 |
| **3.9 Limitations and boundary conditions** | 700 | `5.4` | 2,110 |
| *Conclusions on section 3* | 400 | `4.C` + `5.C` merged | 2,430 · 1,282 |

**Budget rebalanced during the rewrite.** 3.3 carries three studies — the ablation and both
parameter sweeps — and would not hold them at 1,300 without dropping either the grouping
argument or the image-quality counterexample. It takes 300 words from 3.5, where three
external-transfer studies running one protocol compress into a single account. The chapter
total is unchanged.

**Tables: 42 → 20.** This chapter holds nearly all of them. Per-class, per-run and per-fold detail
moves to Appendix B; the body keeps the table that carries the verdict. No sample in the corpus
prints more than 19.

---

## 4 The screening system — 4,500 words

The old Chapter 6, rewritten from a requirements specification into **what was built**: the corpus's
system chapter describes architecture, interface, deployment and screenshots, and never specifies
requirements. **SB-4.1 is amended** — a working demonstrator is deployed and performs inference on
submitted images. SB-4.2 (compliance framing is a design specification, not certified status) and
SB-4.3 (no field testing in Kazakhstan clinical settings) stand unchanged and must both be stated
where the corresponding claims appear.

| New subsection | Budget | Sources | Words |
|---|---:|---|---:|
| **4.1 System architecture and modules** | 1,200 | `6.1.2` Modular architecture with PACS and EHR · `6.1.1` Requirements → **recast as what the built system does** | 1,347 · 1,245 |
| **4.2 Preprocessing and inference services** | 1,100 | `6.2.1` Preprocessing engine · `6.2.2` Inference module | 925 · 782 |
| **4.3 Clinical workflow and operator interface** | 1,200 | `6.3.2` Physician-in-the-loop interface · `6.3.1` Telemedicine and portable devices — **the three fourth-level items 6.3.1.1–6.3.1.3 are dissolved into prose; a fourth level occurs in 0 of 16** | 711 · 1,352 |
| **4.4 Deployment and data protection** | 700 | `6.4.1` GDPR/HIPAA-aligned protocols · `6.4.2` Kazakhstan applicability | 699 · 661 |
| *Conclusions on section 4* | 300 | `6.C` | 516 |

---

## Conclusion — 900 words

`7-draft.md` (1,616 w), trimmed. Corpus closing sections run 1–2–11 pages, median 2.

---

## Appendices

Optional in practice — 6 of 16 have none. Ours stay, minus one.

| New | Was | Content |
|---|---|---|
| **A** | A | Source code of the preprocessing pipeline |
| **B** | B | Supplementary results and confusion matrices — **grows**, taking the per-class and per-run tables displaced from Chapter 3 |
| **C** | C | System architecture diagrams |
| **D** | E | Attention-map gallery |
| **E** | F | Device domain-shift supplementary tables |

**DELETED — old Appendix D, "Certificates and Publication Confirmations" (765 w).** A table of the
five publications plus six screenshots of indexing databases. Neither appears in any of the 16:
reprints of one's own articles and screenshots of Scopus or Web of Science pages are outside the
genre. The publication record has its two proper carriers — the *Approbation and publications*
rubric of the Introduction and of the annotation, and the separate **List of scientific papers**,
which is what the council actually reads for indexing and quartile.

The contents also promised something this appendix never contained — "Certificates of Implementation
and Approbation Acts", i.e. the implementation act and copyright certificate that the corpus does
accept and that **we do not have**. Deleting the appendix resolves the mismatch rather than
papering over it.

**Kazakh lettering: А, Ә, Б, В, Г.** Ә is restored as the second letter, which is what the one
Kazakh-language sample with appendices does, and what the current KZ contents omits.

---

## Rules that apply to every section

Measured by `thesis/scripts/conformance.py`; a chapter is not finished until it passes.

1. Paragraphs of **2–3 sentences, 35–60 words**; sentences of **18–25 words**.
2. **No section sign.** Cross-references are written out — "in section 2.4" — and kept rare; most
   samples have none at all, the most cross-referring has about 16 in a whole dissertation.
3. **No internal code** — no hypothesis, scope-boundary, operational-definition, source-integrity,
   non-claim or contribution identifier, no configuration letter, no "Experiment N" in a heading.
   Hypotheses become prose: "the first hypothesis holds that…". The governance apparatus stays
   authoritative in `thesis/governance/`; it no longer reaches the page.
4. **No editorial residue** — no `[VERIFY]`, `TODO`, `TBD`.
5. **Em dashes out** (10.3 per 1,000 words → ≤ 0.7). The parenthetical aside is what holds our
   sentences at 30 words; removing it does much of the compression by itself.
6. **Bold ≤ 1% of words.** Emphasis by sentence construction, not typography.
7. **Second-level headings appear in the body.** The current text jumps from the chapter heading
   straight to a third-level one, so the contents promises a level the text does not have — a formal
   defect, and all 16 samples are internally consistent on this point.
8. Subsection titles are plain noun phrases of about five words: no colons, no dashes, no codes.
9. Each chapter closes with an unnumbered **Conclusions on section N**, the same form throughout.
10. The PART-3 compliance checklist stays in the drafting file — it is what keeps the claims safe
    against `INVARIANTS.md` — and never reaches the assembled body.

## Order of work

**3 → 2 → 1 → 4 → Introduction → Conclusion.** Chapter 3 carries the results and the largest cut;
settling its compressed form first fixes the register and the table budget for everything else.
