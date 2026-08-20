> Rewritten to the council's measured norms. Sources: all sixteen superseded introduction
> sections (10,003 words). Budget 1,900. Eleven bold run-in rubrics, unnumbered, not listed in
> the contents; the hypothesis and empirical-basis rubrics are dissolved, having no precedent in
> the corpus. The page count in the closing rubric is set from the exported volume.
> Provenance: `outline/REWRITE_MAP.md`.

## PART 1: SECTION TEXT

**Relevance of the research.** Diabetic retinopathy is a microvascular complication of diabetes and
one of the leading causes of preventable vision loss among adults of working age. Its earliest
stages, in which microaneurysms and small haemorrhages appear without affecting acuity, are
asymptomatic, so a patient has no reason to seek care during precisely the interval in which
intervention is most effective.

Detection therefore cannot depend on presentation. It depends on scheduled imaging of a cohort
defined by a systemic diagnosis, most of whom will be found to have nothing requiring treatment.
Screening is, before it is a diagnostic problem, a problem of volume, and volume is what makes the
capacity constraint binding: manual grading scales linearly with specialist time, which is finite and
geographically concentrated.

That automation is technically feasible has been established for a decade, so the relevance of this
work cannot rest on a claim that automated screening remains undemonstrated. It rests on the
conditions under which the demonstrations were obtained. Reported performance has been shown to be
unevenly robust, and the images are not a stable substrate: photographs acquired by different
cameras, operators and dilation states vary systematically. Where screening capacity is scarcest,
acquisition conditions are least controlled.

This is where the methodological question arises, and it concerns how models of this kind are
specified rather than how well any one performs. Preprocessing may be treated as ancillary data
preparation not requiring methodological discussion, or as an integral component of the model,
because the transform applied before the first convolution determines the feature space the network
is obliged to operate in. If the second is right, a model reported without its preprocessing
specified has not been fully described, and comparisons between such models are comparisons between
partly unknown systems.

What makes the question answerable now is the evidence base. Public corpora exist with documented
camera provenance, independent grading protocols and, in one case, pixel-level lesion annotation.
Their joint availability permits the two treatments to be placed in controlled contrast under the
constraints that obtain where screening is scarce.

**Research aim and objectives.** The aim is to develop and experimentally validate an integrated
fundus image enhancement and convolutional classification framework for automated five-class
diabetic retinopathy diagnosis. In it an eight-stage preprocessing pipeline is specified as an
integral component of the model rather than as preparation of the data. The aim is then to establish,
under controlled contrast against an equivalent configuration trained without that pipeline, what
difference the specification makes to performance, transferability and interpretability under
constrained computational conditions.

Four objectives decompose that aim, each discharged in a named chapter.

1. To analyse the problem domain and formulate the research problem: the clinical grading of the
   disease, the screening requirements of resource-limited settings, the sources and measured impact
   of image-quality loss, its device-specific component, and the methodological practice of existing
   automated systems (Chapter 1).
2. To specify the integrated methodology: the eight-stage pipeline stage by stage with the
   theoretical foundations of each, the classification architectures and their adaptation, the
   pretraining and fine-tuning strategy, the explainability formalism and the evaluation and
   statistical protocol (Chapter 2).
3. To evaluate the framework experimentally: an in-domain factorial contrast, a stage decomposition
   with parameter sweeps, a direct measurement of source-to-target distance in feature space,
   cross-corpus and external clinical transfer, attention alignment against expert annotation,
   behaviour across camera groupings and in a data-scarce regime, together with the statistical
   validation and comparative placement of the results (Chapter 3).
4. To build and describe a screening system around the model, suited to settings without inference
   acceleration and with intermittent connectivity, and to state what of it exists and what remains
   specification (Chapter 4).

**Object and subject of research.** The object is the process of automated multi-stage diagnosis of
diabetic retinopathy from colour fundus photographs by means of convolutional networks. It is studied
in its entirety, from the image as it leaves the camera to the grade the model assigns, rather than in
the classification step alone. The subject is the set of methods by which preprocessing is integrated
with classification, together with the properties the resulting configuration exhibits: its
diagnostic performance, its transferability, the alignment of its attention with annotated pathology,
and its behaviour across camera domains.

**Theoretical and methodological framework.** The framework is controlled experimental comparison.
Configurations are contrasted with everything outside the manipulated factor held fixed, so that a
difference in outcome is interpretable as a difference between configurations rather than between the
conditions under which they were obtained.

Its instruments are drawn from image processing, learning and inference. Orientation is normalised by
a pre-trained, frozen landmark detector, and geometry is preserved by isotropic rescaling with the
padding made explicit to the network as a mask channel. Illumination is corrected at a scale
proportional to the per-image field diameter, local contrast is enhanced under a dual-constraint clip
limit, and intensities are standardised from statistics computed on valid fundus pixels.

Classification uses two convolutional backbones of differing family, and class imbalance is addressed
at the objective by a weighted focal loss. Evaluation follows a fixed hierarchy of measures under
patient-level stratified cross-validation, with paired testing, bootstrap intervals and fold-level
modelling.

The empirical material is a tiered corpus of eight public and clinical fundus datasets, acquired with
cameras of four manufacturers and graded under several independent protocols, of which one supplies
training and the remaining seven external, clinical and device-shift evaluation.

**Scientific novelty.** The principal contribution is conceptual: the reframing of preprocessing from
ancillary preparation to an integral component of the diagnostic model. Each item below is at once an
engineering result about a particular pipeline and evidence bearing on that stance.

Preprocessing is formalised as a binding part of the model specification and placed under controlled
experimental contrast. What is new is not the existence of a pipeline but the treatment of one as an
object of experiment rather than of description.

Five elements of its engineering realisation are specified in forms not previously combined.
Isotropic resize with centred padding; a field-of-view mask supplied as a fourth input channel;
illumination correction scaled to per-image geometry and applied inside the mask only. Channel
statistics computed from valid fundus pixels; and canonical orientation whose augmentation dispersion
derives from the uncertainty of the landmark localisation.

The clip limit of the contrast stage is the minimum of a histogram-relative and a tile-relative
constraint, applied stochastically at training time so the stage serves as both enhancement and
regularisation. Attention alignment is measured by the fraction of an annotated lesion that model
attention covers, on the reasoning that lesion coverage is the clinically meaningful direction.

The postulated mechanism is measured rather than inferred. Work asserting that preprocessing improves
cross-domain robustness ordinarily demonstrates it through its consequence, external accuracy, and
leaves the mechanism unmeasured; here source-to-target distance is computed at the penultimate layer
under both configurations across six external corpora. Two features carry the novelty. Normalisation uses
source statistics and is never recomputed on the target, so any convergence is a property of the
preprocessing rather than of a procedure fitted to it. And the measurement's falsifiability was
recorded before it was made, since a reversal was a live possibility and would have been a finding.

A final contribution is analytic. A family of measures in common use for expressing external
robustness normalises an arm's external performance against its own in-domain performance, and such
measures penalise a configuration for its in-domain strength. The analysis holds wherever those
measures are used.

**Provisions submitted for defence.** Each proposition is submitted at the strength the evidence
supports, against a condition fixed before the experiment that tested it. Every empirical provision
carries a qualification, and the qualification is not detachable: a provision stated without it is a
stronger proposition than the evidence supports and is not the one defended.

Preprocessing of fundus images is a formalisable and experimentally testable component of the
diagnostic model rather than ancillary preparation. This provision is methodological: no experiment
promotes or refutes it, the results are consistent with it under the conditions tested, and
consistency under tested conditions is not a universal demonstration.

The integrated configuration dominates the baseline on the training corpus, on both architectures,
under a conjunctive criterion in all three of its components, surviving correction for multiplicity
and showing no interaction with architecture. The provision concerns the configuration: the arms
differ in initialisation as well as preprocessing, so no part of the effect is attributed to
preprocessing alone. The ablation decomposes that composite under a single initialisation and recovers
the whole in-domain gain, but decomposition is not dissolution.

The contributions of the individual stages are separable, each exceeding the between-fold dispersion
of its level and monotone across every fold, with the two photometric stages leading. This is defended
at the resolution of groupings only, since adjacent ranks lie within noise and the mask channel was
not isolated. Both photometric parameters exhibit an interior optimum confirmed on held-out data, and
those optima are properties of this corpus rather than portable constants.

Distance from the training distribution falls on every one of six external corpora with every
interval excluding zero, achieved without the transform observing any target corpus. This is defended
in direction only: the size of the reduction does not predict the size of any performance gain, and
each arm is measured within its own representation space.

Competence transfers to corpora not seen in training, with the integrated configuration higher on
every one, and performance varies less across camera groupings under it. Neither threshold
discriminates between the arms, so the evidence lies in the comparison and in the reduction of spread.
On two external clinical corpora the integrated configuration exceeds the baseline by at least the
minimal clinically important difference, the margin on the second being four thousandths.

Model attention overlaps expert-annotated lesions more under the integrated configuration on all four
annotated lesion types, robustly across the attention threshold. This is defended as alignment and
not as localisation, on one annotated public corpus, with the qualitative half of that hypothesis not
evaluated.

**Theoretical and practical significance.** The theoretical significance lies in how the problem is
posed and measured. The reframing changes what counts as a complete description of a diagnostic model
of this class, and with it what counts as a fair comparison. Three formalisations make previously
informal choices explicit and testable: the clip limit as the minimum of two constraints, illumination
correction as a function of per-image geometry, and attention agreement as an asymmetric overlap. A
fourth renders a postulated mechanism measurable, and a fifth shows a family of robustness measures in
common use to be not neutral.

Four things the work makes practically available, each with the limit attaching to it. A fully
specified preprocessing regime, reproduced in the appendices, whose parameter values were fixed on
particular corpora and should be re-established rather than inherited. A screening system built
around the model, whose realised and unrealised parts are distinguished throughout.

A protocol for ingesting externally sourced images, validated only against the clinical source it was
built for. And an argument of applicability to the national screening context, as a fit between a
documented deployment situation and a computational envelope stated in advance, bounded by the
absence of field testing there.

**Reliability of the results.** Reliability rests on procedure rather than on magnitude. Partitioning
is patient-level and grade-stratified, so a model cannot be credited for recognising a patient it has
already seen. Performance is reported on a hierarchy of measures fixed in advance rather than
selected once outcomes were visible. Differences are assessed by paired testing on identical cases,
their uncertainty quantified by resampling, and where replication across folds exists a mixed-effects
model separates fold variation from the effect under test.

The strongest of these grounds cannot be confirmed from a table and is therefore stated: the
acceptance criterion for each hypothesis was fixed before the experiment that tested it. A criterion
written once a result is known can always be satisfied, and the ordering is what makes the outcome
informative.

Three qualifications bound that reliability. Correction for multiplicity is scoped to the single
experiment within which the comparisons were planned, so no error rate is controlled over the
evidence base as a whole. Several evaluations rest on the models of one fitted fold, so their
intervals understate total uncertainty in a known direction. And one experiment depends on a clinical
corpus that cannot be redistributed.

**Approbation of results and publications.** The components of this research were disseminated
progressively before being integrated here. The work was reported at the 3rd International Workshop
on Digital Society, held in Istanbul in October 2025. The main results are published in five
peer-reviewed works: one article in a journal indexed by Scopus and Web of Science, one paper in
Scopus-indexed conference proceedings, and three articles in journals recommended by the national
committee for quality assurance in science and higher education.

All five are co-authored and are treated throughout as prior own work. Publications reporting the
same experimental material are never cited as independent corroboration of one another, and the
performance figures stated inside them are not imported as findings: where the same questions arise
here they are re-examined on this work's own material.

**Connection with state programmes.** The direction of this research corresponds to the state
priorities of the Republic of Kazakhstan in the digitalisation of healthcare and the development of
artificial-intelligence technologies. It accords in particular with the Concept for the Development
of Artificial Intelligence for 2024–2029, with the Address of the President "Kazakhstan in the Era of
Artificial Intelligence" of 8 September 2025, and with the Law "On Artificial Intelligence" of
17 November 2025. The research is carried out in accordance with subparagraph 2 of paragraph 3 of
article 20 of the Law "On Science".

The nature of that connection should be stated precisely. It is a correspondence between the
direction of the research and published national priorities. It is not a statement that the work was
funded under a state programme or commissioned by any body, and not a claim that any policy objective
has been achieved through it.

**Structure and volume of the work.** The dissertation comprises front matter, an introduction, four
chapters, a conclusion, a list of references and five appendices.

Chapter 1 establishes the clinical and technical context of screening, characterises the sources of
image-quality loss and its device-specific component, reviews what the field has done with
convolutional networks, analyses the existing automated systems, and formulates the research problem.
Chapter 2 specifies the methodology: the eight-stage pipeline with the theory grounding each stage,
the clip limit formalised, the classification architectures and their adaptation, the pretraining and
fine-tuning strategy, the explainability formalism and the evaluation protocol. Chapter 3 reports the
experimental programme and its statistical validation, places the results against published systems,
and states the limitations. Chapter 4 describes the screening system built around the model,
distinguishing throughout what exists from what remains specification. The conclusion consolidates
the outcomes and the directions for further work.

Five appendices follow: the source code of the preprocessing pipeline, supplementary results and
confusion matrices, the system architecture diagrams, the attention-map gallery, and supplementary
tables for the device evaluation.

The dissertation is set out on 105 pages, excluding the appendices, and contains 19 tables and 16
figures. The list of references comprises 99 sources.

---

## PART 3: COMPLIANCE CHECKLIST

**Eleven run-in rubrics, unnumbered** — ✅ Against the corpus range of 8 to 11, all merged as the
norms record: aim with objectives, theoretical with practical significance, approbation with
publications.

**The hypothesis rubric is dissolved** — the corpus uses the word only in its statistical sense and
never carries a labelled system of hypotheses through a volume. The hypotheses appear as prose inside
novelty and provisions, and the formal definitions stay in the governance record where they remain
binding.

**The empirical-basis rubric is dissolved** — folded into the framework rubric, as the corpus does.

**CFC-2.8 in the provisions** — ✅ *"The provision concerns the configuration … decomposition is not
dissolution."*

**Every empirical provision carries its qualification** — ✅ Stated as a rule at the head of the rubric
and applied to each: grouping resolution, direction only, non-discriminating thresholds, the four
thousandths, alignment not localisation, the unevaluated qualitative half.

**SB-1.6 (no state-programme funding claimed)** — ✅ The correspondence is stated and then bounded.

**SIR-4 / SIR-5 (prior own work, single threads)** — ✅ *"never cited as independent corroboration of
one another"*, and figures not imported.

**The publication record does not point to an appendix** — old Appendix D held the publication table
and indexing screenshots and is deleted; the record lives here and in the separate List of scientific
papers, as the corpus does it.

**Volume declared as main text excluding appendices** — ✅ With figures, tables and sources in the same
sentence, as the norms require.

**Rule 16** — ✅ Satisfied.

### Norm compliance

Section signs 0 · internal codes 0 · em dashes 0 · numbered rubrics 0, down from sixteen · not listed
in the contents below its own line.
