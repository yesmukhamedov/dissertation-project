# Kuwait Journal of Science (KJS) — Manuscript Preparation Template

Working specification for bringing `Article manuscript_01.docx` into the form required by the journal.
**Stage 1 — norms only. No edits are made to the `.docx` until a separate instruction is given.**

## Sources (verified 2026-08-12)

| ID | Source | URL |
|---|---|---|
| **S1** | Guide for Authors (Elsevier / ScienceDirect) — **authoritative** | https://www.sciencedirect.com/journal/kuwait-journal-of-science/publish/guide-for-authors |
| **S2** | Open access information / APC (Elsevier / ScienceDirect) | https://www.sciencedirect.com/journal/kuwait-journal-of-science/publish/open-access-options |
| **S3** | Submission Preparation Checklist + Author Guidelines page (Kuwait University journal portal) | https://journals.ku.edu.kw/kjs/index.php/KJS/about/submissions |
| **S4** | Aims and Scope | Reproduced verbatim inside S1, section "About the journal" |

Every rule below is tagged with the source it comes from. Where two sources touch the same
subject, see §2 (Source reconciliation) — no rule in this document is stated without a source.

---

## 1. Journal profile

| Parameter | Value | Source |
|---|---|---|
| Publisher | Elsevier, on behalf of Kuwait University (Academic Publication Council) | S1, S3 |
| ISSN | 2307-4108 | S1 |
| Subject areas | Mathematics, **Computer Science**, Physics, Statistics, Operations Research, Biology, Chemistry, Earth & Environmental Sciences | S1/S4 |
| Expected submissions | Original manuscripts containing analysis and solutions about important theoretical, empirical, and normative issues | S1/S4 |
| Peer review | Single anonymized; editor screening first, then a minimum of two reviewers; decision made by the editors | S1 |
| Appeals | One appeal per submission, per Elsevier's Appeal Policy; the appeal decision is final | S1 |
| Access model | Peer reviewed, **open access** | S2 |
| Licences offered | CC BY, CC BY-NC-ND | S2 |
| **APC** | **USD 1100 (excl. taxes), all article types** | S2 |
| APC waivers | Automatic waiver/discount if **all** authors are based in a Research4Life-eligible country; a personalized APC is shown during submission via OACS ("best price promise"); institutional open access agreements may also apply | S2 |
| Submission system | Editorial Manager — https://www.editorialmanager.com/kjs/default2.aspx | S1 |
| Proof turnaround | Corrections requested **within two days** | S1 |

**Scope fit.** The article belongs to the **Computer Science** subject area (deep learning, medical
image processing, explainable AI, web-based decision support). The journal has no clinical
ophthalmology section, so the cover letter should position the work as Computer Science.

**APC note.** Third-party sites claim KJS charges no fee, or that the APC is covered by Kuwait
University. That is **not** what the official Elsevier open access page states (S2: USD 1100).
Treat USD 1100 as the working figure and read the personalized quote presented by OACS during
submission before committing.

---

## 2. Source reconciliation — no conflicting rules

S3 (the Kuwait University portal) explicitly defers to S1:

> "**UPDATE ON GUIDE FOR AUTHORS.** Please refer to the updated guide for authors on the Elsevier page."

**Precedence rule adopted in this document: S1 governs. S3 remains binding only for the items it
states that S1 is silent about (file set, typography) and for its own stricter submission-portal
undertakings (withdrawal).** Every point where the two sources touch is listed below.

| # | Subject | S1 (Elsevier GFA) | S3 (KJS portal) | Status | Rule applied here |
|---|---|---|---|---|---|
| 1 | File format | Editable source required, `.doc`/`.docx`; "A PDF is not an acceptable source file" | "The submission file should be in Microsoft Word **and** PDF document file format" | **No conflict.** S1 forbids PDF *as the source file*; S3 requires a PDF *in addition*. | Submit both: `.docx` as the source + `.pdf` alongside it |
| 2 | Column layout | Word files must be **single-column**; double-column only for LaTeX | silent | No conflict | Single column |
| 3 | Font, size, spacing, margins | silent | Times New Roman, 12 pt, **double** spacing, 25 mm margins on all sides | No conflict — S1 does not specify | Apply S3 values |
| 4 | Prior publication | Not published previously **except as a preprint, abstract, published lecture, academic thesis or registered report**; not under consideration elsewhere | "The submission has not been previously published nor has it been submitted to another journal, website, or publisher for consideration" | **Apparent tension.** S3 states the rule absolutely; S1 carves out explicit exceptions and is the updated authoritative version. | Rely on the S1 exception (this work derives from an academic thesis), **and disclose it in the cover letter** so the checkbox in S3 is not signed misleadingly |
| 5 | Withdrawal | S1 has a "Withdrawal, correction or retraction" section (body not retrievable — see §12) | "This manuscript cannot be withdrawn or submitted to another Journal once it is reviewed. If so, KJS has the right to take the proper action according to its bylaws" | **S3 is stricter and journal-specific** | Treat S3 as binding: once review starts, withdrawal is not available |
| 6 | Author guidelines in general | Full guidance | Defers to S1 | No conflict | S1 |
| 7 | APC | — | silent | No conflict | S2: USD 1100 |
| 8 | Reference style | Numbered, square brackets, Elsevier format | "The text adheres to the stylistic and bibliographic requirements outlined in the Author Guidelines" → which point to S1 | No conflict | S1 numbered style (§7) |
| 9 | Abstract length | ≤ 250 words | silent | No conflict | 250 words |
| 10 | Manuscript length | No limit stated | No limit stated | **Neither source sets a limit** | No limit is imposed; keep to a normal research-article length. This document does not invent one |

**Conclusion: there is no rule in S1 that S3 contradicts.** Items 4 and 5 are the only two that
require a decision, and both are resolved above.

---

## 3. File set for submission

The submission is a **set of files**, not one document. A PDF is never the source file (S1).

| # | File | Required? | Format | Source |
|---|---|---|---|---|
| 1 | Manuscript (full text incl. tables and captions) | Required | `.doc`/`.docx`, single column | S1, S3 |
| 2 | Manuscript PDF | Required | `.pdf` | S3 |
| 3 | Title page information | Required (as part of the manuscript or a separate file) | `.docx` | S1 |
| 4 | Highlights (3–5 bullets) | Encouraged | `.docx`, with "highlights" in the file name | S1 |
| 5 | Graphical abstract | Encouraged | TIFF/EPS/PDF/MS Office | S1 |
| 6 | Figures — **one file per figure** (`Figure_1`, `Figure_2`, …) | Required | See §6 | S1 |
| 7 | Declaration of interest output from https://declarations.elsevier.com/ | Required | `.doc`/`.docx`, no signatures needed | S1 |
| 8 | Supplementary material | Optional | Published exactly as received, not typeset | S1 |
| 9 | Cover letter | Per journal practice | `.docx` | — |

File hygiene (S1):
- Cite every figure and table in the text; number them in order of appearance.
- Remove all strikethrough and underlined text unless scientifically meaningful.
- Remove reference-manager field codes before submission.
- Run spell-check and grammar-check.
- Supplementary files can only be added or replaced at the revision stage after submission.

---

## 4. Manuscript skeleton — order of blocks

```
[TITLE PAGE]
  Article title
  Author names (superscript letters for affiliations, * for the corresponding author)
  Affiliations (full institution name + full postal address + country + e-mail per author)
  Corresponding author: name, full postal address, e-mail, phone
  Present/permanent address (superscript Arabic numeral footnote, if applicable)

Abstract                       ← unnumbered, ≤ 250 words
Keywords                       ← 1 to 7

1. Introduction
2. Material and methods
   2.1. …
   2.2. …
3. Results
   3.1. …
4. Discussion
5. Conclusion

CRediT authorship contribution statement
Declaration of competing interest
Declaration of generative AI and AI-assisted technologies in the manuscript preparation process
Funding
Data availability
Acknowledgements               ← must sit directly before References
References                     ← numbered list [1], [2], …
Appendix A. …                  ← if any
```

Section numbering rules (S1):
- Number sections `1.`, subsections `1.1.`, `1.1.1.`, then `1.2.`, etc.
- Headings appear on a separate line; subsections may carry a brief heading.
- The abstract is **excluded** from section numbering.
- Cross-reference by section number ("as described in Section 2.3"); never "as described above / in the text".
- Appendices: `Appendix A`, `Appendix B`; separate numbering inside them — `Eq. (A.1)`, `Table A.1`, `Fig. A.1`.
- Footnotes: use sparingly, numbered consecutively; either automatic footnotes or a separate section at the end.
- Acknowledgements go in their own section immediately before the reference list — **never** on the title page, as a title footnote, or anywhere else.

---

## 5. File formatting

| Parameter | Requirement | Source |
|---|---|---|
| Format | `.docx` (editable) + `.pdf` | S1, S3 |
| Columns | **Single column** (double column allowed for LaTeX only) | S1 |
| Font | Times New Roman, 12 pt | S3 |
| Line spacing | **Double** | S3 |
| Margins | 25 mm on all sides | S3 |
| Language | American **or** British English, not a mixture | S1 |
| Manuscript length | Not specified by either source | S1, S3 |
| Line/page numbering | Not required by either source | S1, S3 |

The current file appears to use single spacing and a non-Times font — to be corrected at Stage 2.

---

## 6. Text blocks — detailed requirements (all from S1)

### 6.1. Title page
- **Article title** — concise and informative; avoid abbreviations and formulae unless established and widely understood (e.g. DNA).
- **Author names** — given name(s) + family name(s); the order must match the order entered in the submission system; names may additionally be given in parentheses in the author's own script after the English transliteration.
- **Affiliations** — lower-case superscript letter immediately after the author's name and in front of the corresponding address; full name and postal address of each affiliation, including the **country**, and the e-mail address of each author if available.
- **Corresponding author** — clearly indicated; handles correspondence at all stages including post-publication; e-mail and contact details must be kept up to date. Only the corresponding author's affiliation determines publishing-agreement eligibility and any APC discount.
- **Present/permanent address** — footnote to the author's name using superscript Arabic numerals; the address where the work was carried out remains the main affiliation.

### 6.2. Abstract
- **Maximum 250 words**; concise and factual.
- States the purpose of the research, the principal results, and the major conclusions.
- Must stand alone (abstracts are often presented separately from the article).
- Avoid references; if one is essential, cite author(s) and year(s) **in full**.
- Avoid non-standard or uncommon abbreviations; if essential, define at first mention inside the abstract.
- Structured labels (`Background:`, `Objective:`, `Methods:`, `Results:`, `Conclusion:`) are neither required nor prohibited by S1.

### 6.3. Keywords
- **1 to 7** keywords, in English, for indexing.
- Avoid keywords made of multiple words joined by "and" or "of".
- Use abbreviations only if firmly established in the field.

### 6.4. Highlights (encouraged)
- **3 to 5 bullet points, each a maximum of 85 characters including spaces.**
- Separate editable file with "highlights" in the file name.
- Capture the novel results and any new methods.

### 6.5. Graphical abstract (encouraged)
- One image summarising the article for an interdisciplinary audience.
- **531 × 1328 pixels (h × w)** or proportionally more; readable at 5 × 13 cm.
- TIFF, EPS, PDF or MS Office file, submitted separately.
- Permission required for any third-party material; genAI use must follow Elsevier's GenAI policies.

### 6.6. Math formulae
- Submit equations as **editable text**, not images.
- Present simple formulae in line with normal text where possible.
- Use the solidus (`/`) instead of a horizontal line for small fractional terms (`X/Y`).
- Variables in *italics*; denote powers of e by `exp`.
- Display equations separately, numbered consecutively in order of reference.

---

## 7. Tables and figures (all from S1)

### Tables
- **Editable text only**, never images.
- Place next to the relevant text, or on separate page(s) at the end of the article.
- Cite every table in the text; number consecutively by appearance.
- Provide a caption with each table; place table notes **below** the table body.
- **No vertical rules and no cell shading.**
- Use tables sparingly; do not duplicate data already described elsewhere.

### Figures
- Supply each image as a **separate file**, using a logical naming convention (`Figure_1`, `Figure_2`, …).
- Cite every image in the text; number in order of appearance.
- Every piece of artwork must have a caption: a brief title (not displayed on the figure itself) plus a description; explain every symbol and abbreviation.
- Keep text inside images to a minimum; text must not be disproportionately small.
- Do **not** combine different images or graphs into one file — it harms accessibility.
- Colour figures appear in colour online; ensure the palette is accessible to readers with impaired colour vision.
- Text graphics may be embedded in the text at the appropriate position.

**Resolution requirements:**

| Type | Format | Minimum |
|---|---|---|
| Vector drawings | EPS or PDF, fonts embedded or text saved as graphics | — |
| Colour or grayscale photographs (halftones) | TIFF, JPG, PNG | **300 dpi** (single column ≥ 1063 px; full page width ≥ 2244 px) |
| Bitmapped line drawings | TIFF, JPG, PNG | **1000 dpi** (≥ 3543 px; ≥ 7480 px) |
| Combination line/halftone | TIFF, JPG, PNG | **500 dpi** (≥ 1772 px; ≥ 3740 px) |

**Generative AI in figures and artwork:**
- **Allowed** — explanatory images (flow charts, conceptual diagrams, schematic illustrations) and data visualisations (plots, charts, graphs, heatmaps) when the output derives directly from underlying data by reproducible analytical, computational or statistical methods.
- **Not allowed** — creating or altering images that represent primary observed or experimental data (e.g. microscopy, histology, patient images) that were not directly obtained in the research; this includes brightness, contrast and colour-balance adjustments, which may only be done with established image-processing software.
- The policy does **not** restrict AI used in formal research design or research methods — our preprocessing pipeline, CNN classifier and Grad-CAM belong in Methods, not in this disclosure.
- If genAI produced an image, disclose it **in the figure caption and** in the general generative AI statement.

---

## 8. References — numbered style, square brackets (S1)

### 8.1. In-text citation
- Number in square brackets: `as demonstrated [3,6]`, `Barnaby and Jones [8] obtained a different result …`.
- Number references **in the order they appear** in the article.
- Abbreviate journal names per the **List of Title Word Abbreviations (LTWA)** — https://portal.issn.org/ltwa.
- Every in-text citation must appear in the reference list and vice versa.
- References cited in the abstract must be given in full.
- DOIs are encouraged as reference links.
- Unpublished results and personal communications are best kept out of the reference list (mention them in the text); if listed, replace the publication date with "unpublished results" or "personal communication".
- "in press" means the item has been accepted for publication.
- Verify all reference data before submission — incorrect surnames, journal or book titles, years or pagination break linking to Scopus, Crossref and PubMed.

### 8.2. Reference formats — the journal's own examples

```
Journal publication:
[1] J. van der Geer, T. Handgraaf, R.A. Lupton, The art of writing a scientific article,
    J. Sci. Commun. 163 (2020) 51–59. https://doi.org/10.1016/j.sc.2020.00372.

Journal publication with an article number:
[2] J. van der Geer, T. Handgraaf, R.A. Lupton, 2022. The art of writing a scientific article.
    Heliyon. 19, e00205. https://doi.org/10.1016/j.heliyon.2022.e00205.

Book:
[3] W. Strunk Jr., E.B. White, The Elements of Style, fourth ed., Longman, New York, 2000.

Chapter in a book:
[4] G.R. Mettam, L.B. Adams, How to prepare an electronic version of your article,
    in: B.S. Jones, R.Z. Smith (Eds.), Introduction to the Electronic Age,
    E-Publishing Inc., New York, 2020, pp. 281–304.

Website:
[5] Cancer Research UK, Cancer statistics reports for the UK.
    http://www.cancerresearchuk.org/aboutcancer/statistics/cancerstatsreport/,
    2023 (accessed 13 March 2023).

Dataset:
[6] M. Oguro, S. Imahiro, S. Saito, T. Nakashizuka, Mortality data for Japanese oak wilt disease
    and surrounding forest compositions [dataset], Mendeley Data, v1, 2015.
    https://doi.org/10.1234/abc12nb39r.1.

Software:
[7] E. Coon, M. Berndt, A. Jan, …, Advanced Terrestrial Simulator (ATS) v0.88 [software],
    Zenodo, March 25, 2020. https://doi.org/10.1234/zenodo.3727209.
```

Note: examples [1] and [2] use different punctuation in the source itself ([1] comma-separated,
[2] with the year after the authors). **[1] is the pattern to follow** — it matches the reference
style paragraph; [2] is the article-number variant as printed by the journal.

- **Web references** — minimum: full URL + date last accessed; add DOI, authors, dates if known. May be listed under a separate heading directly after the reference list, or inside it.
- **Data references** — author name(s), dataset title, repository, version (if any), year, global persistent identifier; prefix with `[dataset]`, which does not appear in the published article.
- **Preprint references** — mark clearly with the word "preprint" or the preprint server name plus the preprint DOI; if the preprint has since been formally published, cite the publication instead.
- **Reference managers** — CSL-based tools (e.g. Mendeley Reference Manager) may carry the journal template; if none is available, follow the examples above. Remove all field codes before submitting.

### 8.3. ⚠️ Conversion required for the current reference list

The 33 references in `Article manuscript_01.docx` are currently in **Vancouver/AMA** style
(family name before initials, full stops between blocks, `Year;Vol(Issue):pages`). This is **not**
the KJS style. Every entry needs rewriting:

| Element | Current (Vancouver) | Required (Elsevier numbered) |
|---|---|---|
| Name order | `Gulshan V, Peng L,` | `V. Gulshan, L. Peng,` |
| Separators | full stops between blocks | commas between blocks |
| Article title | `… photographs.` | `… photographs,` |
| Journal block | `JAMA. 2016;316(22):2402-2410.` | `JAMA 316 (2016) 2402–2410.` — LTWA abbreviation, volume, year in parentheses, issue number dropped |
| Page range dash | hyphen `2402-2410` | en dash `2402–2410` |
| DOI | absent | append `https://doi.org/…` |

Worked example on a real entry:

```
BEFORE:
[1] Gulshan V, Peng L, Coram M, Stumpe MC, Wu D, Narayanaswamy A, et al. Development and
    validation of a deep learning algorithm for detection of diabetic retinopathy in retinal
    fundus photographs. JAMA. 2016;316(22):2402-2410.

AFTER:
[1] V. Gulshan, L. Peng, M. Coram, M.C. Stumpe, D. Wu, A. Narayanaswamy, et al., Development and
    validation of a deep learning algorithm for detection of diabetic retinopathy in retinal
    fundus photographs, JAMA 316 (2016) 2402–2410. https://doi.org/10.1001/jama.2016.17216.
```

Entry `[3] World Health Organization. Diabetes. Fact sheet. Geneva: WHO; 14 November 2024.`
must be re-cast as a web reference (URL + `(accessed …)`).

---

## 9. Mandatory declarations — ready-to-paste blocks

Placed at the end of the manuscript, before the reference list, in the order given in §4.

### 9.1. CRediT authorship contribution statement (required, S1)
Corresponding authors **are required** to acknowledge co-author contributions using CRediT roles:
Conceptualization, Data curation, Formal analysis, Funding acquisition, Investigation, Methodology,
Project administration, Resources, Software, Supervision, Validation, Visualization,
Writing – original draft, Writing – review and editing. Not all roles apply to every manuscript,
and one author may hold several.

```
CRediT authorship contribution statement

<Author 1>: <Role>, <Role>, <Role>.
<Author 2>: <Role>, <Role>.
<Author 3>: <Role>, <Role>, <Role>.
```

### 9.2. Declaration of competing interest (required, S1)
Disclose any financial and personal relationships that could inappropriately influence or bias the
work: employment, consultancies, stock ownership, honoraria, paid expert testimony, patent
applications or registrations, grants or any other funding, affiliation with the journal as an
Editor or Advisory Board Member. **The declarations tool at https://declarations.elsevier.com/ must
always be completed**, and the resulting `.doc`/`.docx` uploaded at the "attach/upload files" step.
Author signatures are not required. Authors with nothing to declare select "I have nothing to declare".

```
Declaration of competing interest

The authors declare that they have no known competing financial interests or personal
relationships that could have appeared to influence the work reported in this paper.
```

### 9.3. Funding (required, S1)
Disclose funding sources and the role of the sponsor in study design; collection, analysis and
interpretation of data; writing of the report; and the decision to submit. If sponsors had no such
involvement, state that. Detailed programme or grant-type descriptions are not needed; for block
grants, name the institution that provided the funding.

```
Funding

This work was supported by <FUNDER> [grant number xxxx].
The funder had no role in study design, data collection and analysis, interpretation of data,
writing of the report, or the decision to submit the article for publication.
```

If there was no funding, the journal's recommended sentence is:

```
Funding

This research did not receive any specific grant from funding agencies in the public,
commercial, or not-for-profit sectors.
```

### 9.4. Declaration of generative AI use (required on first submission if applicable, S1)
A new section placed before the reference list. Journal wording:

```
Declaration of generative AI and AI-assisted technologies in the manuscript preparation process

During the preparation of this work the author(s) used <NAME OF TOOL / SERVICE> in order to
<REASON>. After using this tool/service, the author(s) reviewed and edited the content as needed
and take(s) full responsibility for the content of the published article.
```

Qualifications (S1):
- **Not** required for basic tools that check grammar, spelling and references.
- **Not** required for AI features inside specialist disability-related assistive technology used solely for accessibility.
- If there is nothing to disclose, omit the section entirely.
- AI tools must **never** be listed or cited as an author or co-author.
- AI tools may not substitute for human critical thinking, expertise and evaluation; they may only be applied with human oversight and control.
- Authors remain accountable for: verifying accuracy, comprehensiveness and impartiality of all AI output (including checking sources, since AI-generated references can be incorrect or fabricated); editing all material so the manuscript is the authors' authentic original contribution; ensuring accuracy, originality and attribution of AI-generated images; making any tool use transparent to readers; and safeguarding data privacy and IP by checking the tool's terms.
- AI used as part of the research method itself (our CNN, preprocessing, Grad-CAM) is described in Methods, not in this declaration.

### 9.5. Data availability (S1 — journal applies **Option B**)
Authors are **encouraged** to deposit research data in a relevant repository, cite and link to the
dataset in the article, or — if that is not possible — make a statement explaining why the data
cannot be shared. In-text data identifiers use the format `Database: 12345` (e.g. `PDB: 1XFN`).

```
Data availability

The public datasets analysed in this study are available at <REPO / URL>.
<Trained model weights and inference code are available at …> /
<The clinical data cannot be shared publicly because …>
```

### 9.6. Acknowledgements (S1)
Own section, immediately before the reference list. Include anyone who provided help during the
research, including help with language, writing or proofreading. Never on the title page, as a
footnote to the title, or anywhere else.

---

## 10. Ethics and policy requirements (S1)

- The work has not been published previously **except** as a preprint, an abstract, a published lecture, an **academic thesis** or a registered report; it is not under consideration elsewhere; publication is approved by all authors and by the responsible authorities where the work was carried out; if accepted, it will not be published elsewhere in the same form, in any language, without the copyright holder's written consent. → **See §2 item 4 for how this interacts with the S3 checkbox.**
- Manuscripts may be screened with the publisher's compliance tools.
- **Authorship** requires substantial contributions to all of: (1) conception and design, or acquisition of data, or analysis and interpretation of data; (2) drafting the article or revising it critically for important intellectual content; (3) final approval of the version to be submitted. All authors are accountable for all aspects of the work.
- A **single corresponding author** must be appointed.
- **Changes to authorship**: generally not considered once submitted. Changes are possible **only before acceptance**, only with editor approval, and only via the Authorship Change Request form with written confirmation from all authors including those added or removed. Review may be paused while a request is considered. **After acceptance no authorship change is allowed at all** — including changing the corresponding author. Changes made without the form or without editor approval may lead to rejection, or retraction if already published. → The author list and order must therefore be final at submission.
- **Inclusive language**: nothing implying one individual is superior to another on grounds of age, gender, race, ethnicity, culture, sexual orientation, disability or health condition. Avoid descriptors of personal attributes unless relevant and valid. Write for gender neutrality using plural nouns by default; avoid "he, she" and "he/she". No assumptions about readers' beliefs; free of bias, stereotypes, slang and cultural assumptions.
- **Sex- and gender-based analyses**: integrate SGBA into research design where research involves or pertains to humans, animals or eukaryotic cells; address sex/gender dimensions in the article or declare them as a limitation on generalisability; state explicitly the definitions of sex and/or gender applied. See the SAGER guidelines and checklist.
- **Jurisdictional claims**: maps must show only the area actually studied, must be locatable on common mapping platforms, and must carry the note "*map lines delineate study areas and do not necessarily depict accepted national boundaries*". Use the full standard institution title or its standard abbreviation so affiliations can be independently verified.
- **Editor conflicts**: editors do not decide on papers they authored, papers by family members or colleagues, or papers relating to products/services in which they have an interest.
- **Delayed publication**: contact the editorial office as early as possible; timing cannot be guaranteed.
- **Permissions**: written permission from the copyright owner is required for excerpts from other copyrighted works, credited in the article, using Elsevier's permission request and license form.

---

## 11. Submission checklist (S1 + S3)

- [ ] One author designated corresponding author, with full contact details (e-mail, full postal address, phone numbers)
- [ ] All files uploaded — artwork, videos, supplementary materials; tables and footnotes included in the files; captions submitted
- [ ] Spelling and grammar checks carried out
- [ ] All references cited in the text appear in the reference list, and vice versa
- [ ] Permission obtained for any copyrighted material from other sources, including the Web
- [ ] All authors understand they are responsible for payment of the APC if the manuscript is accepted
- [ ] Reference-manager field codes removed
- [ ] Strikethrough and underlining removed
- [ ] Manuscript supplied in **both** Word and PDF (S3)
- [ ] Times New Roman 12 pt, double spacing, 25 mm margins on all sides (S3)
- [ ] Declarations tool completed and the `.docx` attached

After a final decision: publishing agreement signed by the corresponding author; open access
licence selected; **proof corrections returned within two days**. Alt text added by the publisher
with AI assistance must be checked in the proofs. Significant changes at proof stage require
editor approval.

---

## 12. Coverage gaps — verify on the live page before submission

Four entries appear in the S1 table of contents but their bodies did not render in the captured
version of the page. Nothing in this document depends on them, but they should be read directly
on the live Guide for Authors before submitting:

1. **Ethics in publishing** (under "Ethics and policies")
2. **Open access** (under "About the journal")
3. **Preprints** (under "Ethics and policies")
4. **Withdrawal, correction or retraction** (under "Ethics and policies") — cross-check against S3's stricter no-withdrawal undertaking, §2 item 5

The Aims and Scope standalone page was behind a bot challenge; its text was taken from the
identical "About the journal → Aims and scope" section inside S1.

---

## 13. Delta against `Article manuscript_01.docx` (Stage 2 work list)

> **Status:** `Article manuscript_02.docx` is the reworked copy built against this specification.
> Items 1–6, 8, 9, 13 (dashes) below are applied there; items 7, 10, 12 and the `[[FILL]]` blocks
> remain open. `Article manuscript_01.docx` is left untouched as the original.

Already compliant:
- Section structure 1–5 (Introduction / Material and Methods / Results / Discussion / Conclusion) with `2.1`, `2.2`, … subsection numbering
- Title block with superscript affiliations and a marked corresponding author
- In-text citations in square brackets `[1]`, `[3,6]`, numbered by order of appearance
- CRediT authorship contribution statement present
- Declaration of Competing Interest present
- Tables supplied as editable text with captions
- Figure captions `Fig. 1` … `Fig. 7b` present

Work list:
1. ✅ **Reference list** — all 33 entries converted to Elsevier numbered style, DOIs added (31 of 33; [3] and [27] carry verified URLs), LTWA journal abbreviations applied.
2. ✅ **File formatting** — Times New Roman 12 pt, double spacing, 25 mm margins, single column.
3. ✅ **Abstract** — condensed 274 → 248 words; structured labels kept (permitted).
4. ✅ **Keywords** — 6 keywords, within the 1–7 range, no "and"/"of" constructions; unchanged.
5. ✅ **Missing required sections** — `Declaration of generative AI…`, `Funding`, `Data availability`, `Acknowledgements` inserted with `[[FILL]]` placeholders where the answer depends on the authors.
6. ✅ **Order of end matter** — rearranged to §4; Acknowledgements sits directly before References.
7. ◐ **Figures** — exported to `figures/Figure_1…8.png`; all 8 were below the required resolution (§7). Fig. 1 and Fig. 3 are redrawn as vector PDF + ≥ 1000 dpi PNG in `figures_hires/`. Fig. 2, 4, 5, 6, 7, 8 cannot be regenerated from anything held in this repository — see `figures_hires/README.md` for what each one needs.
8. ✅ **Tables** — vertical rules removed; no cell shading; notes below the table body.
9. ✅ **Subsection numbering** — verified after edits.
10. ⬜ **Highlights** (3–5 bullets, ≤ 85 characters each) and **graphical abstract** — still to be created as separate files.
11. ✅ **Fig. 7a / Fig. 7b** — renumbered to `Fig. 7` and `Fig. 8`; both now cited in the body text.
12. ⬜ **Numerical values** — reconcile against `results/`, the single source of truth for every number, before submission.
13. ✅ **Typography** — 17 parenthetical en dashes converted to em dashes; en dashes kept in ranges and compounds.
14. ⬜ **English variant** — one variant (British or American) to be enforced throughout in a final language pass.
15. ✅ **Citation order** — references [28]–[30] renumbered so numbering follows first appearance in the text (SE net → [28], stochastic depth → [29], ResNet → [30]).

---

## 14. Open questions for the author

1. **Funding** — is there a grant or state programme to name, or do we use the "did not receive any specific grant" sentence?
2. **Generative AI in manuscript preparation** — was any used, and which tool? This determines whether §9.4 is included.
3. **Data availability** — what can be disclosed: public datasets, model weights, demo code?
4. **Author list and order** — final? No changes are possible after acceptance.
5. **Corresponding author e-mail** — the file gives `yesmukhamedov.yeskendyr@gmail.com`; will the same address be used in Editorial Manager?
6. **Highlights and graphical abstract** — produce them? Both are optional but improve visibility.
7. **APC of USD 1100** — is funding for it in place, and does any institutional agreement or waiver apply?
