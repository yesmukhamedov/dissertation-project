---
name: council-reviews-currency
description: The two council reviews (supervisor KZ, foreign consultant EN) were rewritten 2026-08-13 against the finished manuscript; what was stale and what must never drift back
metadata:
  type: project
---

`thesis/output/supervisor_review_kz.md` and `foreign_consultant_review_en.md` had sat unchanged
since 2026-06-16 — written *before* the results run, before the governance v7.0.0/v7.1.0
re-specifications and before the manuscript was finished. On **2026-08-13** both were rewritten
against the currency-passed abstracts (`abstract_{en,kz}.md`, see
[[abstract-annotation-alignment]]) and `results/STATUS.md`, then rebuilt via
[[council-docs-skill]] → `defense/docs/reviews/` (6 pp each: EN 2253 words, KZ 1558).

## The `council/en/` review templates do NOT match what candidates submit

The first rewrite followed `council/en/13-…` and `14-…` literally and was **wrong in genre** — the
candidate caught it. Checked against the real peer submissions in
`D:/dissertation_council/Образцы документов/авторы/` (Момынқулова, Әйтім, Бакирова, Дауренбаева),
the same lesson as [[abstract-annotation-alignment]] holds here: **trust the samples, not the
template.** What the samples actually show:

| | Real samples | The template says |
|---|---|---|
| Supervisor review | **1–2 pp, no headings at all**, 6–8 flowing paragraphs | 7 numbered sections |
| Foreign review | 1–4 pp, free prose *or* **named** headings ("Relevance of the Research Topic", "Novelty and Contribution", "Degree of Reliability…") | fixed **5 numbered** sections |
| Tone | uniformly laudatory; limitations are **not** enumerated | — |
| Signatory | position / organisation down the left, name flush right | `Signature: /signature/`, `Date: "__"`, `Stamp: /…/` placeholders |
| Bilingual | common — same text EN+RU in one file | — |

Numbered `## 1. …` sections, bullet lists and the `Signature:/Stamp:` placeholder fields are all
template-isms that no real submission carries. Final shape: **KZ 3 pp / 893 words, heading-free
prose; EN 4 pp / 1590 words, named headings** (the UNITEN/Bakirova pattern, closest analogue since
Al-Haddad is likewise a Malaysian professor).

⚠ **Genre vs. governance.** Real reviews carry no fences at all, but a review that contradicted the
volume's own qualifications would be worse than one that is merely conventional. Resolution: state
the results positively and **mention the candidate's delimitation once, as a virtue**, instead of
auditing every fence. Do not reinstate the fence-by-fence enumeration — that was the defect, not the
fix.

## Defects fixed — do not let these drift back

Shared by both documents:
1. **Reviews stated no outcomes at all.** They described the *design* as if the experiments were
   still pending. Both now carry the seven hypothesis verdicts *with their fences* — H-3 in
   direction only, H-5 in its quantitative half only, H-7 as absolute external performance.
2. **H-7 was still "clinical degradation resistance"** — retired in governance v7.0.0 in favour of
   *external clinical performance* (form S, Δ wF1 ≥ MCID 0.050 with CI⁻ > 0 on each set). Messidor-2
   as "for clinical degradation" went with it.
3. **The Kazakh clinical set was labelled "qualitative validation"** — the same defect the abstracts
   carried. That examination was never done (G-3); its real use is training in a data-scarce regime
   (Exp 7), 60 images / 30 patients × 2 eyes, not redistributable.
4. **H-3 was absent entirely** (reinstated in v7.1.0 — direct penultimate-layer distance measurement
   over six corpora under the source-domain-statistics condition), as were the in-domain
   pretraining + linear-probe gate (with the negative from-scratch-SSL result), the cumulative
   ablation under a single initialisation, and the robustness-measure defect analysis.
5. **The architecture was described as deployable** ("directly applicable", "ұсынды" with no fence).
   It is a *design contribution only* — no prototype, no field testing, GDPR/HIPAA alignment by
   design not certified compliance, clinician retains the diagnosis.
6. Missing qualifications now present: the two arms differ in **initialisation as well as
   preprocessing**; the baseline **also** clears G ≥ 0.85; the Messidor-2 MCID margin is thin;
   correction for multiple comparisons is scoped per experiment; single-fold intervals understate
   uncertainty; the EyePACS ~53,576-image unlabelled pretraining split is disjoint by image and patient.

EN-only: image quality is **CNR, entropy, SSIM** — *VVI was never used*; IDRiD is external clinical
evaluation + explainability, not "clinical validation".

KZ-only: **the review named the internal governance documents** ("инварианттар, гипотезалар тізілімі,
дәлел картасы") as evidence of the candidate's rigour. That is exactly the process metadata
[[no-process-history-in-deliverables]] and [[manuscript-text-hygiene]] forbid in a council document —
rephrased as pre-registered criteria, declared scope boundaries and openly reported negative results.
Also Latin "pipeline" → **"конвейер"** throughout, per the same KZ terminology rule as the abstracts.

## Converter change this required

`md2gost.py` joined every buffered line with a space, so a signatory block collapsed into one
justified paragraph. Added `_line_block()` + a `_HARD_BREAK` sentinel: a **Markdown hard break (two
trailing spaces)** now opts a block into signature shape — one paragraph per line, left aligned, no
first-line indent, and a run of **3+ spaces inside a line becomes a right tab stop** so the name
lands at the right margin. Regression-checked against `abstract_en` (13 pp / 5054 words, unchanged).
Both review sources use this convention in their closing block.

## Standing rule

A review is a *judgement on the finished volume*, so it inherits every fence the volume carries.
Whenever §0.8 (statements for defence) or a hypothesis verdict moves, these two files move with it —
they are not write-once documents. Unlike the abstracts, **no page cap binds them** (§6.9 governs the
аннотация only), so a needed qualification is never traded away for space here.
