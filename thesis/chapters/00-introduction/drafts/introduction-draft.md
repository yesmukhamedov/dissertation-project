> Rewritten to the council's measured norms. Sources: all sixteen superseded introduction
> sections (10,003 words). Budget 1,900. Eleven bold run-in rubrics, unnumbered, not listed in
> the contents; the hypothesis and empirical-basis rubrics are dissolved, having no precedent in
> the corpus. The page count in the closing rubric is set from the exported volume.
> Provenance: `outline/REWRITE_MAP.md`.

## PART 1: SECTION TEXT

**Relevance of the research.** Diabetic retinopathy is a microvascular complication of diabetes and
one of the leading causes of preventable vision loss among adults of working age. Its earliest
stages, in which microaneurysms and small haemorrhages appear without affecting acuity, are
asymptomatic, so a patient has no reason to seek care during the interval in which intervention is
most effective.

Detection therefore cannot depend on presentation. It depends on scheduled imaging of a cohort
defined by a systemic diagnosis, most of whom will be found to have nothing requiring treatment.
Screening is, before it is a diagnostic problem, a problem of volume, and volume is what makes the
capacity constraint binding: manual grading scales linearly with specialist time, which is finite
and geographically concentrated.

That automation is technically feasible has been established for a decade, so the relevance of this
work cannot rest on a claim that automated screening remains undemonstrated, but on the conditions
under which the demonstrations were obtained. Reported performance has been shown to be unevenly
robust, and the images are not a stable substrate: photographs acquired by different cameras,
operators and dilation states vary systematically. Where screening capacity is scarcest, acquisition
conditions are least controlled.

The methodological question follows: it concerns how models of this kind are specified rather than
how well any one performs. Preprocessing may be treated as ancillary data preparation not requiring
methodological discussion, or as an integral component of the model, because the transform applied
before the first convolution determines the feature space the network is obliged to operate in. If
the second is right, a model reported without its preprocessing specified has not been fully
described, and comparisons between such models are comparisons between partly unknown systems.

What makes the question answerable now is the evidence base. Public corpora exist with documented
camera provenance, independent grading protocols and, in one case, pixel-level lesion annotation.
Their joint availability permits the two treatments to be placed in controlled contrast under the
constraints of a setting where screening is scarce.

**Research aim and objectives.** The aim is to develop and experimentally validate an integrated
fundus image enhancement and convolutional classification framework for automated five-class
diabetic retinopathy diagnosis, in which an eight-stage preprocessing pipeline is specified as an
integral component of the model rather than as preparation of the data, and to establish, under
controlled contrast against an equivalent configuration trained without that pipeline, what
difference the specification makes to performance, transferability and interpretability under
constrained computational conditions.

Four objectives decompose that aim, each discharged in a named chapter.

1. To analyse the problem domain and formulate the research problem: the clinical grading of the
   disease, the screening requirements of resource-limited settings, the sources of image-quality
   loss and the methodological practice of existing automated systems (Chapter 1).
2. To specify the integrated methodology: the pipeline, the classification architectures, the
   pretraining strategy, the explainability formalism and the evaluation protocol (Chapter 2).
3. To evaluate the framework experimentally, in domain and on seven external corpora, and to validate
   the results statistically (Chapter 3).
4. To build and describe a screening system around the model, suited to settings without inference
   acceleration and with intermittent connectivity (Chapter 4).

**Object and subject of research.** The object is the process of automated multi-stage diagnosis of
diabetic retinopathy from colour fundus photographs by means of convolutional networks, studied in
its entirety from the image as it leaves the camera to the grade the model assigns rather than in
the classification step alone. The subject is the set of methods by which preprocessing is
integrated with classification, together with the properties the configuration exhibits: its
diagnostic performance, its transferability, the alignment of its attention with annotated
pathology, and its behaviour across camera domains.

**Theoretical and methodological framework.** The framework is controlled experimental comparison.
Configurations are contrasted with everything outside the manipulated factor held fixed, so a
difference in outcome is a difference between configurations rather than between the conditions
under which they were obtained.

Its instruments are drawn from image processing, learning and inference. Orientation is normalised
by a pre-trained, frozen landmark detector, and geometry is preserved by isotropic rescaling with
the padding made explicit to the network as a mask channel. Illumination, local contrast and
intensity scale are set by the photometric stages of the pipeline.

Classification uses two convolutional backbones of differing family, and class imbalance is
addressed at the objective by a weighted focal loss. Evaluation follows a fixed hierarchy of
measures under patient-level stratified cross-validation, with paired testing, bootstrap intervals
and fold-level modelling.

The empirical material is a tiered corpus of eight public and clinical fundus datasets, from cameras
of four manufacturers and several independent grading protocols, of which one supplies training and
the remaining seven external, clinical and device-shift evaluation.

**Scientific novelty.** The principal contribution is conceptual: the reframing of preprocessing
from ancillary preparation to an integral component of the diagnostic model. Preprocessing is
formalised as a binding part of the model specification and placed under controlled experimental
contrast, so what is new is not the existence of a pipeline but the treatment of one as an object of
experiment rather than of description. Each item below is at once an engineering result about a
particular pipeline and evidence bearing on that stance.

Five elements of its engineering realisation are specified in forms not previously combined:
isotropic resize with centred padding; a field-of-view mask supplied as a fourth input channel;
illumination correction scaled to per-image geometry and applied inside the mask only; channel
statistics computed from valid fundus pixels; and canonical orientation whose augmentation
dispersion derives from the uncertainty of the landmark localisation.

The clip limit of the contrast stage is the minimum of a histogram-relative and a tile-relative
constraint, applied stochastically at training time so the stage serves as both enhancement and
regularisation. Attention alignment is measured by the fraction of an annotated lesion that model
attention covers, on the reasoning that lesion coverage is the clinically meaningful direction.

The postulated mechanism is measured rather than inferred. Work asserting that preprocessing
improves cross-domain robustness ordinarily demonstrates it through its consequence, external
accuracy, and leaves the mechanism unmeasured; here source-to-target distance is computed at the
penultimate layer under both configurations across six external corpora, and falls on all six by
0.070 to 0.093 with every interval excluding zero. Normalisation uses source statistics and is never
recomputed on the target, so the convergence is a property of the preprocessing rather than of a
procedure fitted to it.

A final contribution is analytic. A family of measures in common use for external robustness
normalises an arm's external performance against its own in-domain performance, and so penalises a
configuration for its in-domain strength wherever it is used.

**Provisions submitted for defence.** Each proposition is submitted at the strength the evidence
supports, against a condition fixed before the experiment that tested it. The conditions bounding
each of them are set out under the reliability of the results, and they are not detachable: a
provision read without its bound is a stronger proposition than the evidence supports and is not the
one defended.

Preprocessing of fundus images is a formalisable and experimentally testable component of the
diagnostic model rather than ancillary preparation. This provision is methodological: no experiment
promotes or refutes it, and the results are consistent with it under the conditions tested.

The integrated configuration exceeds the baseline on the training corpus of 35,126 images, on both
architectures, in all three components of the conjunctive criterion: weighted F1 by 6.54 and 6.55
percentage points, area under the curve by 0.032 and 0.036, and quadratic kappa by 0.11. Every
interval excludes zero, every comparison survives correction for multiplicity, and there is no
interaction between arm and architecture. The provision concerns the configuration: the arms differ
in initialisation as well as preprocessing, so no part of the effect is attributed to preprocessing
alone. The ablation decomposes that composite under a single initialisation and recovers the whole
in-domain gain of 0.0655, but decomposition is not dissolution.

The contributions of the individual stages are separable. Cumulative ablation over eight levels
under one initialisation raises weighted F1 from 0.7538 to 0.8193, monotonically and without a
single inversion in any of the five folds, each of the seven transitions contributing between 0.0065
and 0.0143 against a between-fold dispersion of 0.0042 to 0.0060. The two photometric stages lead
and together carry 41% of the total. Both parameters exhibit an interior optimum confirmed on
held-out data, at a clip factor of 2.5 with a histogram threshold of 0.03 and at a correction scale
of 0.07 of the field diameter.

Distance from the training distribution falls on every one of six external corpora, by 0.070 to
0.093 at the penultimate layer with every interval excluding zero and by 34% to 38% at the pixel
level, achieved without the transform observing any target corpus.

Competence transfers to corpora not seen in training. On the cross-corpus set it reaches a
generalisation ratio of 0.898 against 0.858 and a weighted F1 higher by 0.089; across five camera
groupings it is higher on every one, and the spread between them contracts by a factor of 2.4 in
weighted F1 and 3.1 in area under the curve, both intervals excluding zero. On two external clinical
corpora it exceeds the baseline by 0.069 and 0.054 in weighted F1, both above the minimal clinically
important difference of 0.050.

Model attention overlaps expert-annotated lesions more under the integrated configuration on all
four annotated lesion types, by 0.099 to 0.129 in the overlap measure at p ≤ 0.0148, and the
direction holds at every binarisation threshold tested. This is defended as alignment and not as
localisation.

**Theoretical and practical significance.** The theoretical significance lies in how the problem is
posed and measured. The reframing changes what counts as a complete description of a diagnostic
model of this class, and with it what counts as a fair comparison. Five formalisations make
previously informal choices explicit and testable: the clip limit, the illumination correction,
attention agreement as an asymmetric overlap, the postulated mechanism as a measurable distance, and
the non-neutrality of a family of robustness measures in common use.

Four things the work makes practically available, each with its limit. A fully specified
preprocessing regime, reproduced in the appendices, whose parameter values should be re-established
rather than inherited. A screening system built around the model, whose realised and unrealised
parts are distinguished throughout. A protocol for ingesting externally sourced images, validated
only against the clinical source it was built for. And an argument of applicability to the national
screening context, bounded by the absence of field testing there.

**Reliability of the results.** Reliability rests on procedure rather than on magnitude.
Partitioning is patient-level and grade-stratified, so a model cannot be credited for recognising a
patient it has already seen. Performance is reported on a hierarchy of measures fixed in advance
rather than selected once outcomes were visible. Differences are assessed by paired testing on
identical cases, their uncertainty quantified by resampling, and where folds replicate a
mixed-effects model separates fold variation from the effect under test.

The strongest of these grounds is not visible in a table and is therefore stated: the acceptance
criterion for each hypothesis was fixed before the experiment that tested it, and a criterion
written once a result is known can always be satisfied.

Three qualifications bound it in general. Correction for multiplicity is scoped to the single
experiment within which the comparisons were planned, so no error rate is controlled over the
evidence base as a whole. Several evaluations rest on the models of one fitted fold, so their
intervals understate total uncertainty in a known direction. And one experiment depends on a
clinical corpus that cannot be redistributed.

Four bounds attach to particular provisions. The stage ranking holds at the resolution of groupings
only, since adjacent ranks lie within noise and the mask channel was not isolated, and the two
parameter optima are properties of this corpus rather than portable constants. The reduction in
distance holds in direction only: its size predicts no gain, and each arm is measured within its own
representation space. Neither the generalisation ratio nor the camera-group floor discriminates
between the arms, so the transfer evidence lies in the comparison and in the reduction of spread,
and on the second external clinical corpus the margin over that difference is four thousandths. The
attention result rests on one annotated public corpus, and the qualitative half of that hypothesis
was not evaluated.

**Approbation of results and publications.** The components of this research were disseminated
progressively before being integrated here. The work was reported at the 3rd International Workshop
on Digital Society, held in Istanbul on 28–30 October 2025. The main results are published in five
peer-reviewed works. Two are indexed in Scopus: an article in Eastern-European Journal of Enterprise
Technologies, 4(9), 79–88, third quartile and indexed in Web of Science as well (Sapakova,
Yesmukhamedov and Sapakov, 2025), and a conference paper in Procedia Computer Science, volume 272,
496–501 (Sapakova, Yesmukhamedov, Sapakov, Yemberdiyeva and Kozhamkulova, 2025).

Three are articles in journals recommended by the national committee for quality assurance in
science and higher education: News of the National Academy of Sciences of the Republic of
Kazakhstan, Physico-Mathematical Series, 2(354), 74–91 (Yesmukhamedov, Sapakova, Al-Haddad and
Daniyarova, 2025); Herald of the Kazakh-British Technical University, 22(4), 119–130 (Yesmukhamedov,
Sapakova, Kozhamkulova, Daniyarova and Armankyzy, 2025); and Herald of KazUTB, 2(27-740), 20–30
(Sapakova, Daniyarova, Yesmukhamedov, Armankyzy, Emberdieva and Kaldybaeva, 2025).

All five are co-authored and are treated throughout as prior own work. In each the candidate
contributed the part on which this dissertation rests: the formulation of the preprocessing problem,
the design and implementation of the pipeline, the conduct of the classification experiments, the
analysis of the results and the writing of the corresponding sections. The experimental programme
reported here, its protocol and its statistical validation were carried out by the candidate.

Publications reporting the same experimental material are never cited as independent corroboration
of one another, and the performance figures stated inside them are not imported as findings: where
the same questions arise here they are re-examined on this work's own material.

**Connection with state programmes.** The direction of this research corresponds to the state
priorities of the Republic of Kazakhstan in the digitalisation of healthcare and the development of
artificial-intelligence technologies. It accords in particular with the Concept for the Development
of Artificial Intelligence for 2024–2029, with the Address of the President "Kazakhstan in the Era
of Artificial Intelligence" of 8 September 2025, and with the Law "On Artificial Intelligence" of 17
November 2025. The research is carried out in accordance with subparagraph 2 of paragraph 3 of
article 20 of the Law "On Science".

That connection is a correspondence between the direction of the research and published national
priorities, not a statement that the work was funded under a state programme or commissioned by any
body, and not a claim that any policy objective has been achieved through it.

**Structure and volume of the work.** The dissertation comprises front matter, an introduction, four
chapters, a conclusion, a list of references and five appendices.

Chapter 1 establishes the clinical and technical context of screening. It characterises the grading
of the disease and what a screening programme demands of a resource-limited setting, identifies the
sources of image-quality loss and isolates its device-specific component, reviews what the field has
done with convolutional networks and what its automated systems assume about preprocessing, and
formulates the research problem that follows from that practice.

Chapter 2 specifies the methodology. It sets out the eight-stage pipeline with the theory grounding
each stage, formalises the clip limit and the illumination correction, describes the two
classification architectures and their adaptation to a four-channel input, states the pretraining
and fine-tuning strategy, defines the explainability formalism, and fixes the evaluation protocol
and the statistical procedures in advance of the experiments.

Chapter 3 reports the experimental programme: the in-domain factorial contrast, the stage
decomposition with its parameter sweeps, the direct measurement of source-to-target distance, the
cross-corpus and external clinical transfer, the alignment of attention with expert annotation and
the behaviour across camera groupings and in a data-scarce regime, and then the statistical
validation, the placement of the results against published systems and the limitations bounding
them. Chapter 4 describes the screening system built around the model, its architecture, its
inference behaviour without acceleration hardware and its ingestion protocol, distinguishing what
exists from what remains specification. The conclusion consolidates the outcomes and the directions
for further work.

Five appendices follow: the source code of the preprocessing pipeline, supplementary results and
confusion matrices, the system architecture with the working demonstrator, the attention-map
gallery, and supplementary tables for the device evaluation.

The dissertation is set out on 107 pages, excluding the appendices, and contains 19 tables and 16
figures. The list of references comprises 102 sources.

---

## PART 3: COMPLIANCE CHECKLIST

**Eleven run-in rubrics, unnumbered** — ✅ Against the corpus range of 8 to 11, all merged as the
norms record: aim with objectives, theoretical with practical significance, approbation with
publications. The chapter overview stays inside the closing rubric rather than taking a twelfth
lead-in of its own.

**The hypothesis rubric is dissolved** — the corpus uses the word only in its statistical sense and
never carries a labelled system of hypotheses through a volume. The hypotheses appear as prose inside
novelty and provisions, and the formal definitions stay in the governance record where they remain
binding.

**The empirical-basis rubric is dissolved** — folded into the framework rubric, as the corpus does.

**Every empirical provision states its effect size** — ✅ The corpus writes the provisions rubric with
figures in it (median 5.0 digits per 1,000 characters, up to 70.1); the rubric had none. Each
provision now carries the quantity its criterion was fixed on, taken from `results/`.

**CFC-2.8 in the provisions** — ✅ *"The provision concerns the configuration … decomposition is not
dissolution."* The dominance provision is worded in the permissible form of the clause: the
configuration exceeds the baseline by a stated margin on a stated metric.

**NC-14 in the provisions** — ✅ *"defended as alignment and not as localisation"*, stated where the
attention claim is made rather than deferred.

**Every empirical provision keeps its bound** — ✅ The bounds are stated under the reliability rubric
and the provisions rubric says so at its head, so the provisions read as assertions while nothing is
dropped: grouping resolution, non-portable optima, direction only, non-discriminating thresholds, the
four thousandths, one annotated corpus, the unevaluated qualitative half.

**Personal contribution is stated** — ✅ All five publications are co-authored and the candidate is not
first author on two, so the share is stated rather than left to be asked for.

**SB-1.6 (no state-programme funding claimed)** — ✅ The correspondence is stated and then bounded.

**SIR-4 / SIR-5 (prior own work, single threads)** — ✅ *"never cited as independent corroboration of
one another"*, and figures not imported.

**The publication record does not point to an appendix** — old Appendix D held the publication table
and indexing screenshots and is deleted; the record lives here, with journal, volume, pages and
indexing status in the running text, and in the separate List of scientific papers, as the corpus
does it.

**Volume declared as main text excluding appendices** — ✅ With figures, tables and sources in the same
sentence, as the norms require.

**Rule 16** — ✅ Satisfied.

### Norm compliance

Section signs 0 · internal codes 0 · em dashes 0 · numbered rubrics 0 · not listed in the contents
below its own line. The rubric shares that were furthest from the corpus — novelty, provisions,
framework, significance — paid for the additions, so the volume is unchanged at the gate ceiling.
