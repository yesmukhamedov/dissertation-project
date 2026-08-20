> Rewritten to the council's measured norms. Source: superseded 7 (1,616 words). Budget 900.
> The hypothesis-by-hypothesis recital becomes a statement of what was found; each verdict is
> reached in the section that reports it. Provenance: `outline/REWRITE_MAP.md`.

## PART 1: SECTION TEXT

This dissertation set out to establish whether the preparation of a fundus image before it reaches a
convolutional network belongs to the specification of the diagnostic model or beside it.

The question is not rhetorical. If the transform applied before the first convolution determines the
feature space the network operates in, then a model reported without that transform specified has not
been fully described, and a comparison between two such models is a comparison between partly unknown
systems.

The work therefore specified an eight-stage pipeline as a binding part of the model and placed the
resulting configuration under controlled contrast against an equivalent configuration lacking it. It
then asked what difference the specification makes to classification, to transfer, to what the model
attends to, and to behaviour across imaging devices.

Every criterion was fixed before the experiment that tested it, and each outcome is reported at the
strength that criterion supports, with the qualification inseparable from it.

The integrated configuration exceeded the baseline on all three components of the conjunctive
criterion, on both architectures, surviving correction for multiplicity and showing no interaction
with architecture. That is a property of the configuration, which differs from the baseline in
initialisation as well as preprocessing. A cumulative ablation under a single initialisation later
recovered the whole in-domain gain, decomposing that composite without dissolving it.

Every stage transition contributed more than the noise of its level, and the contributions separate
into groups with the two photometric stages leading. That is a grouping and not an ordering, since
adjacent ranks lie within noise. Both photometric parameters have interior optima confirmed on
held-out data.

The distance between the training distribution and each of six target distributions fell, without any
target statistic entering the transform, so the mechanism the argument postulates was measured rather
than inferred. The magnitude of that reduction does not track the magnitude of the corresponding
performance gain, and no argument here rests on such a correspondence.

Competence transferred to every external corpus examined, with the integrated configuration higher on
each. Two of the criteria were cleared by both configurations, so there the evidence lies in the
comparison and not in the criterion. On the external clinical corpora the claim is about absolute
performance and not about resistance to degradation, since relative to their own in-domain levels the
two configurations declined almost identically, and the margin on the second is four thousandths.

Attention overlapped expert-annotated lesions more under the integrated configuration on all four
annotated types and on both measures. What that establishes is alignment between model evidence and
expert annotation, not localisation, and the qualitative examination on the clinical corpus that the
hypothesis also contemplates was not carried out.

A preregistered evaluation in a data-scarce regime found the integrated configuration again the
stronger, by a margin comparable to, and not larger than, the one measured with abundant data.

Taken together these outcomes describe an effect whose notable property is not its size. The
principal finding is consistency: the advantage is present in-domain, decomposable across the
pipeline's stages, traceable to a measured reduction in distributional distance, and observable on
every corpus and every camera grouping examined, in both an abundant and a scarce training regime.

An effect that survives that many changes of condition is more plausibly a property of the feature
space the model is given than an artefact of any one evaluation. That is what supports treating
preprocessing as a component of the model rather than as preparation of the data.

What the consistency does not license should be said with equal directness. It is not evidence of
clinical validity, of readiness for unsupervised deployment, or of device certification. It
establishes no superiority over any published system, the placement against the literature having
been made deliberately without ranking. And it does not extend beyond the corpora, devices and
populations on which it was obtained.

The contributions are of four kinds. The conceptual contribution is the reframing itself, which
changes what counts as a complete description of a diagnostic model of this class and with it what
counts as a fair comparison. It is a methodological position rather than an empirical finding, and
the results are consistent with it under the conditions tested rather than establishing it
universally.

The engineering contribution is the pipeline as a specified and reproducible object: geometry-preserving
resize, the explicit mask as an input channel, illumination correction scaled to per-image geometry,
normalisation from valid fundus pixels, and canonical orientation with adaptive augmentation.

The metrological contributions are two. An asymmetric measure of overlap between model attention and
expert annotation, whose asymmetry is argued from what is clinically meaningful rather than adopted
by convention. And the direct measurement of source-to-target distance under a source-statistics
condition, which supplies the middle term of the causal chain instead of leaving it to be inferred
from the chain's endpoints.

The methodological contribution is analytic. Three measures in common use for expressing external
robustness each normalise or difference an arm's external performance against that same arm's
in-domain performance, and therefore penalise a configuration for its in-domain strength. That
analysis holds wherever those measures are used; it is descriptive, and it rehabilitates no result
of this work.

One outcome that ran against expectation is recorded here rather than omitted. Label-free
self-supervised initialisation trained from scratch on the in-domain corpus failed the frozen-backbone
acceptance gate, across several protocols of the same family and without improvement from longer
training, and was therefore not admitted.

The initialisation ultimately used was selected by that gate rather than assumed. The gate exists
precisely so that an initialisation may fail it, and a conclusion reporting only the branch that
succeeded would misrepresent the record.

The limitations are set out in full where each arose. They concern what was measured and what was
not; the corpora, devices and populations the evidence reaches; the instruments' own interpretive
limits; the design's confounds and the single-fold evaluations that carry no between-fold variance;
and the reproducibility of one experiment whose corpus cannot be redistributed. None is softened
here and none is added.

Eight questions remain open, and they are worth stating in the order of what closing them would cost.
Four could be answered without training a new model. Whether the attention alignment demonstrated on
annotated public data also holds on the clinical corpus, and whether attention is consistent across
corpora, both need only overlays and a comparison protocol. What the mask channel contributes in
isolation needs one further ablation level, since the present one introduces it jointly with the
crop. And what an end-to-end system costs needs the preprocessing stages themselves timed, the
present analysis having measured only the network.

Three would require new experiments or new data. Whether the two photometric parameters interact
needs a joint sweep rather than two independent ones. Whether the composition of errors differs
across camera groupings needs per-grouping confusion matrices. And whether any of this holds beyond
the corpora and devices used here needs independent validation this work does not provide.

The eighth is of a different kind and no measurement can close it. Each of the differenced and
ratio-based transfer measures examined here penalises a configuration for its own in-domain strength,
so whether they should serve as criteria of external quality at all is a question about what the
field should measure. It is answered by argument or not at all.

The position this dissertation ends on can be stated briefly and checked against the record. Under
matched conditions, on eight corpora spanning four camera manufacturers, an integrated
preprocessing-classification configuration outperformed an equivalent configuration without the
pipeline, consistently and in every regime examined. The mechanism proposed to explain that advantage
was measured directly rather than inferred, and the advantage decomposes across the pipeline's stages.

The work does not show that this configuration is clinically valid, deployable, certifiable, or
better than any published system, and it does not show that these results hold beyond the conditions
under which they were obtained. Those are the boundaries within which the contribution stands, and
they are not incidental to it: a claim narrow enough to be checked is the only kind worth defending.

---

## PART 3: COMPLIANCE CHECKLIST

**No claim exceeds the body** — ✅ Every outcome is stated as the section that reported it stated it,
with its qualification. The conclusion is bounded above by the chapter-3 conclusions and by the
provisions submitted for defence, and it promotes nothing.

**No metric value appears** — ✅ Except the four thousandths of the thin margin, which is a bound on a
claim rather than a performance figure, and which would be misrepresented by the word "narrow".

**The failed branch is reported** — ✅ *"a conclusion reporting only the branch that succeeded would
misrepresent the record."* This is the single most easily omitted item in the whole volume.

**The consistency finding and its limits** — ✅ Both, adjacently: what an effect surviving that many
changes of condition supports, and the four things it does not license.

**The eighth open question is marked as unanswerable by measurement** — ✅ Kept, because it is the
one that identifies a problem in the field rather than in this work.

**The hypothesis-by-hypothesis recital is dropped** — the superseded conclusion restated each verdict
with its identifier and its numbers, duplicating the sections that reached them. What survives is
what the chapter conclusions cannot show individually.

**Rule 16** — ✅ Satisfied.

### Norm compliance

Section signs 0 · internal codes 0 · em dashes 0 · tables 0. Corpus closing sections run 1 to 11
pages with a median of 2; this one is about 4.
