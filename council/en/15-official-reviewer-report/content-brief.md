# What goes in each row — content brief for this dissertation

> Companion to [[form-blank]] (the fixed column-2 text) and [[structure]] (genre, deadlines, signature).
> This file says **what column 3 must actually assert** for
> «Computer System for Processing and Analysis of Eye Data to Support Laser Coagulation in the Treatment of Diabetic Retinopathy»,
> and which option in column 2 is the honest one to underline.
>
> Facts are taken from `results/STATUS.md` (run of record) and `thesis/output/abstract_en.md`.
> **Never take numbers from `demo/web/data.js`.**

## Standing constraints — a reviewer's report inherits every fence the volume carries

A report that praises the work beyond what §0.8 submits is not a favour: it invites exactly the
question the candidate has already fenced off. Six things must never appear:

1. **H-7 is not "resistance to degradation".** It is *higher absolute external performance*
   (Δ wF1 ≥ MCID 0.050 with CI⁻ > 0 on each corpus separately). Relative to their own in-domain levels
   the two arms decline almost identically.
2. **The Kazakh clinical corpus was not a validation set.** It is the held-out corpus of the
   data-scarce training experiment (60 images, 30 patients × 2 eyes) and cannot be redistributed. The
   qualitative Grad-CAM examination on it **was not carried out**.
3. **The screening architecture is a design contribution only** — no prototype, no field testing,
   GDPR/HIPAA *alignment by design*, not certified compliance; the clinician retains the diagnosis.
4. **The two arms differ in initialisation as well as in preprocessing.** Every "the pipeline caused
   X" phrasing must be "the integrated configuration attained X".
5. **Grad-CAM is attention alignment, not clinical localisation of pathology.**
6. **No internal document names, no run dates, no artefact paths, no version markers.** Say
   "pre-registered criteria", "declared scope boundaries", "openly reported negative results" —
   never the names of the governing files. Image quality is **CNR, entropy, SSIM**.

## Row by row

### 1 — topic ↔ directions of science / state programmes
**Underline option 3** (priority direction approved by the Higher Scientific and Technical Commission).
**Not** options 1 or 2: the work was **not** funded from the state budget and **not** performed under a
state programme, and the volume says so explicitly. What column 3 names, as *correspondence of
direction* rather than mandate:
- Concept for the Development of Artificial Intelligence for 2024–2029;
- Address of the President of the RK «Kazakhstan in the Era of Artificial Intelligence» (8 Sept 2025);
- Law of the RK «On Artificial Intelligence» No. 230-VIII of 17 Nov 2025;
- subpara. 2, para. 3, art. 20 of the Law of the RK «On Science»;
- healthcare digitalisation priorities and the national eHealth platform.

### 2 — importance for science
**Underline** "makes a significant contribution … well-disclosed". Substance: the reframing of
preprocessing from ancillary data preparation into a binding component of the diagnostic model that
co-determines the CNN's feature space (P1 → P2), placed under direct experimental test rather than
asserted; and the fact that the mechanism usually *invoked* to explain transfer gains is here
*measured* at the penultimate layer.

### 3 — self-reliance
**Underline "high"**. Supporting points: a single-author formalisation of the 8-stage pipeline; all
seven experiments designed, run and analysed by the candidate; the acceptance gate that rejected the
candidate's own from-scratch self-supervision — a negative result reported rather than buried — and
the analytic identification of a defect in three robustness measures the field uses, which rehabilitates
none of his own numbers. Publications 1, 2 and 5 are co-authored; 3 and 4 are led by the candidate.

### 4 — internal unity
**4.1 justified · 4.2 reflects · 4.3 correspond · 4.4 completely interconnected · 4.5 there is a
critical analysis.** Substance: Ch. 1 states the problem, Ch. 2 the mathematical foundations, Ch. 3
the formalised pipeline and architectures, Ch. 4 the eight investigations, Ch. 5 the reliability
apparatus and limits, Ch. 6 the system architecture — each hypothesis (H-1…H-7) is stated before the
experiment that tests it and answered by it, with the negative and partial outcomes carried through to
the statements for defence rather than dropped.

### 5 — scientific novelty
**5.1 completely new · 5.2 completely new · 5.3 new and justified** (EN) / соответствующий вариант.
Column 3 should pick **four or five** of the twelve novelty items, not recite all twelve:
- the 8-stage pipeline formalised as a model component (4 input channels: RGB + FOV mask);
- dual-constraint stochastic CLAHE on the LAB L-channel — CL = min(clip_factor · tile_area / 256,
  global_threshold · tile_area), 80% train-time probability — serving at once as enhancement and as
  regularisation. ⚠ It *extends the candidate's own published work*; new here are its formalisation,
  its embedding in a specified pipeline and its five-class validation;
- adaptive flat-field correction with σ scaling to the per-image FOV diameter (σ = 0.07·D), applied
  only inside the mask so the padding is not corrupted;
- **ALO (Attention–Lesion Overlap)** as a primary asymmetric explainability metric, IoU secondary;
- direct measurement of source-to-target distance at the penultimate layer over six external corpora
  under the source-domain-statistics condition — falsifiability recorded before the measurement.

⚠ Two contributions are **non-empirical by design** and must be named as such: the coupled
thermal-optical model of laser exposure (theoretical/computational only) and the screening-system
architecture (design only).

### 6 — validity of the main conclusions
**Underline "are based"**. Substance: 5-fold patient-level stratified cross-validation with leakage
control on ~35,126 EyePACS training images; every primary metric reported as mean ± SD over four
metrics (weighted F1, ROC-AUC, quadratic-weighted κ, accuracy); McNemar and DeLong tests, bootstrap
intervals ≥ 1000 resamples, Holm/Bonferroni correction, mixed-effects modelling across folds; and
criteria fixed **before** the experiments that tested them.

### 7 — provisions submitted for defense
This is the longest row. The volume submits **eleven** statements; the reviewer answers 7.1–7.5 for
each, or groups them. Defensible answers with their fences:

| # | Statement | 7.1 | 7.2 | 7.3 | 7.4 | 7.5 | Fence that must travel with it |
|---|---|---|---|---|---|---|---|
| 1 | Preprocessing is a model component (P1 → P2) | rather proven | no | yes | wide | yes | methodological and non-empirical; results are *consistent with* it, do not establish it universally |
| 2 | Integrated dominates baseline (H-1) | proven | no | yes | wide | yes | the arms differ in initialisation too; the claim is about the configuration as a whole |
| 3 | Interior optima for CLAHE and σ (H-2) | proven | no | yes | medium | yes | bounded to the ranges swept; the values are corpus properties, not portable constants |
| 4 | Stage contributions separable, monotone, orderable (H-2) | proven | no | yes | medium | yes | at the resolution of *groupings* only; adjacent ranks lie within noise; the mask channel was not isolated |
| 5 | Source–target distance falls on every external corpus (H-3) | proven | no | yes | medium | yes | **direction only** — magnitude does not track any performance gain |
| 6 | Transfer to APTOS clears G ≥ 0.85 (H-4) | proven | no | yes | wide | yes | the baseline also clears it; the evidence is in the comparison, not the threshold |
| 7 | Attention aligns better with lesion masks (H-5) | proven | no | yes | medium | yes | alignment, **not** localisation; one corpus, one fold; the clinical qualitative half not carried out |
| 8 | Performance held across camera groupings, dispersion reduced (H-6) | proven | no | yes | medium | yes | both arms clear the floor; 2 of 5 groupings are the external clinical corpora; no device certification |
| 9 | Higher absolute external wF1 on both clinical corpora (H-7) | proven | no | yes | wide | yes | absolute performance, **not** degradation resistance; the Messidor-2 margin over MCID is 0.0041 |
| 10 | Structural defect shared by three robustness measures | proven | no | yes | wide | yes | analytic and strictly descriptive; rehabilitates no result of this work |
| 11 | Thermal-optical model + screening architecture | rather proven | no | yes | medium | yes | theoretical and design contributions; not clinically validated, not prototyped, not field-tested |

Numbers available for column 3: EH-3 met on both backbones — B vs A ΔwF1 **+6.54 pp**, ΔAUC +0.0320,
Δκ +0.1129; D vs C **+6.55 pp**, +0.0360, +0.1103; DeLong p = 0.0041/0.0028, McNemar p = 0.0057/0.0041,
Holm-corrected 0.0082/0.0056; arm × backbone interaction p = 0.31.

### 8 — reliability
**8.1 yes · 8.2 yes · 8.3 yes · 8.4 supported · 8.5 sufficient.** Substance for column 3:
- 8.2 — five-class grading, Focal loss (γ = 2, α = inverse frequency), 512×512 input, mixed precision
  for ResNet-50 and disabled for EfficientNet, 5-fold patient-level stratification;
- 8.3 — every stage transition in the cumulative ablation exceeded the between-fold dispersion of its
  level, and monotonicity held **in each of the five folds**; the ablation recovered the whole
  in-domain gain (L0 0.7538 → L7 0.8193, **+0.0655**); the two photometric stages lead (flat-field
  +0.0143, CLAHE +0.0125 — together 41% of the gain);
- 8.5 — **107 sources**.

State plainly, as the volume does, the three limits of the apparatus: multiple-comparison correction
is scoped per experiment (no dissertation-wide error rate); several evaluations rest on one fitted
fold, so their intervals understate total uncertainty in a known direction; one experiment rests on a
non-redistributable clinical corpus and is therefore not externally reproducible. Naming these
*raises* the report's credibility — they are already in §0.8.

### 9 — practical value
**9.1 yes · 9.2 yes · 9.3 completely new.** Substance: a fully specified, reproducible preprocessing
regime — stage by stage, with operators, parameters and order of application, implementation in
Appendix A — usable under constrained computational conditions (single 12 GB GPU, batch 16); the
modular screening architecture with preprocessing-engine, inference, store-and-forward telemedicine and
physician-in-the-loop modules, integrable with PACS/EHR and the national eHealth platform, aimed at
rural and underserved regions of Kazakhstan.
⚠ Say **design specification**: no prototype, no clinical deployment test, alignment-by-design on data
protection, clinician retains the diagnosis. And the parameter values are corpus properties.

### 10 — quality of writing
**Underline "high"**. Points available: 238 pp. (EN edition) / 264 pp. (Kazakh edition, the defended
volume), 42 tables, 26 figures and two diagrams, 107 sources; consistent notation, a declared
abbreviations register, GOST-conformant formatting; every claim in the closing statements carries its
qualification inline.

### 11 — comments
**Mandatory and substantive — the two reviewers must not raise the same points.** Real, checkable
candidates, all of them already visible in the volume, which is what makes them fair:

- the Messidor-2 margin over the MCID is **0.0041**, and the lower bound of that interval (+0.0362)
  lies below the MCID — the pass rests on the form of the criterion (Δ ≥ MCID **and** CI⁻ > 0) and this
  deserves an explicit sentence in the text rather than only in the limitations;
- **Stage 3 is not isolated** in the ablation: level L3 applies Stages 2 and 3 jointly, so the FOV-mask
  channel has no separate contribution estimate;
- the ablation fixes the **stage order**, so each contribution is conditional on the preceding stages
  being applied — the reported ranking is not order-invariant and the text could say so more directly;
- several evaluations (transfer, explainability, external performance) rest on **fold-0 checkpoints**;
  the intervals therefore sample the evaluation corpus only;
- the correlation between distance reduction and transfer gain (ρ ≈ 0.49) is weak, which the volume
  states — but the mechanistic chapter would read more cleanly if the direction-only reading were
  restated at its own conclusion rather than only in the statements for defence;
- the qualitative Grad-CAM examination on the Kazakh clinical corpus is declared and then not carried
  out; the volume should mark it as future work at the point where it is introduced.

### 12 — scientific level of the articles
**5 publications**: 1 in Scopus/WoS (*Eastern-European Journal of Enterprise Technologies*, 2025,
Vol. 4 No. 9(136), pp. 79–88, **Q3**); 1 in Scopus-indexed conference proceedings (*Procedia Computer
Science*, 2025, Vol. 272, pp. 496–501 — DS 2025, Istanbul); 3 in KKSON-recommended journals (*News of
the NAS RK, Physico-Mathematical Series*; *Herald of the KBTU*; *Herald of KazUTB*).

⚠ **Two things to verify before writing this row:**
1. the mandatory threshold is **Scopus CiteScore percentile ≥ 25** in a matching area, *or* WoS Core
   Collection SCIE/SSCI/AHCI. The volume states the quartile (Q3) but **not** the percentile — the
   real samples quote it ("Q3, 47th percentile"). Get the current CiteScore percentile for EEJET and
   put the figure in this row.
2. the record contains **no copyright certificate / certificate of state registration** of a computer
   program. That category is not mandatory, but the peer samples carry one and it strengthens row 9;
   if one exists or is pending, name it — if not, do not invent it.

### 13 — decision
`To petition the Committee for the award of the degree of Doctor of Philosophy (PhD)` /
`Ходатайствовать перед Комитетом для присуждения докторанту степени доктора философии (PhD)` /
`Комитет алдында докторантқа философия докторы (PhD) дәрежесін беру туралы өтініш білдіру`.

## Splitting the two reports

The two official reviewers must not produce the same document. A workable division:

| | Reviewer 1 | Reviewer 2 |
|---|---|---|
| Centre of gravity | the methodological reframing and the in-domain evidence (rows 2, 5, 7 st. 1–4, 8) | external validity and applicability (rows 7 st. 5–10, 9, 10) |
| Comments (row 11) | Stage 3 not isolated; stage order fixed; fold-0 evaluations | Messidor-2 MCID margin; ρ ≈ 0.49 direction-only reading; declared-but-unperformed qualitative examination |
| Register | closer to the formal-methods reading | closer to the clinical-deployment reading |
