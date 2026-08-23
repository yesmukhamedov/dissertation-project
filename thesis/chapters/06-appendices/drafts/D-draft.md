> Ported from the superseded appendices, re-lettered, with the provenance banner,
> section signs and internal codes removed and cross-references renumbered to the
> four-chapter body. Transcription content is unchanged. Provenance: `outline/REWRITE_MAP.md`.

# APPENDIX D – Attention-map gallery

---

## PART 1: SECTION TEXT

### D.1 What this gallery is, and how it must be read

The reading rule comes before the plates, because a gallery of attention maps is more persuasive
than it is probative and the distinction matters here.

A gradient-weighted class activation map indicates where activation in the final convolutional layer
is high, weighted by its gradient with respect to the predicted class. It is a post-hoc
interpretability instrument. **It is not a delineation of pathology.** A plate in which the
attention region overlaps an annotated lesion does not show that the model detected that lesion,
does not show that the model reasoned from it, and does not constitute clinical localisation. What
such an overlap can support is a claim about *alignment* between model evidence and expert
annotation, and even that is a claim about the aggregate rather than about any individual image.

It follows that **these plates are illustration and carry no measurement**. The measurement is the
one reported in section 3.6: Attention–Lesion Overlap as the primary quantity and
Intersection-over-Union as the secondary, computed per lesion type over the whole annotated subset
with interval estimates and a threshold sweep. A reader who forms an impression from the images in
this appendix has not thereby checked that result, and a reader who wishes to check it should read
section 3.6 and Appendix B rather than these pages. These plates exist so that the reader can see
what the measurement was made on, not so that the measurement can be re-made by eye.

### D.2 The four plates, and how they were chosen

Four plates are printed. Each pairs the same fundus image under both configurations, the baseline arm
on the left and the integrated arm on the right, against the expert pixel-level annotation.

The four are a selection, and are declared as one. The annotated subset comprises 54 images, the
measurement reported in section 3.6 was made over all 54, and the overlay was produced for every one
of them; what is printed here illustrates what such a plate looks like and is not the material the
measurement rests on. Two properties of the selection are stated so that the reader knows what it is
not. The four images carry grades 4, 4, 2 and 2, so the selection is not confined to the severe end
of the scale. And between them they carry every one of the four annotated lesion types: two are
annotated for all four, and two for three of them, soft exudates being annotated on 26 of the 54.

No property of the aggregate may be read off four plates, and none is asserted from them. A reader
who wants the aggregate has it in section 3.6, with its interval estimates and its threshold sweep,
and in Appendix B.

### D.3 The subset, and what bounds it

Of the 516 images in the annotated corpus, 54 carry pixel-level lesion annotation and constitute the
subset on which the explainability measurement was performed. Availability differs by lesion type,
at 54, 53, 54 and 26 images respectively for the four annotated types. The per-type figure for the
least-represented type therefore rests on roughly half the images of the others and is the least
stable of the four.

One further property of the subset is recorded here because it bounds what any plate can show. On 6
of the 54 images neither configuration's attention meets the annotation at the operating threshold,
leaving 48 informative pairs. That is a property of the subset the measurement was made on, and it
holds whether or not such an image is among the four printed here.

The evidence in this appendix rests on a single annotated corpus and on the models of a single
cross-validation fold. Neither the corpus nor the fold is varied anywhere in the explainability
analysis, and no between-fold variation is available for it.

### D.4 Plates

The plates follow. Each is resolved to its image during document conversion, and each caption names
the image it was produced from, so a plate can be matched against the run outputs.

- `[FIG-D.1: Paired attention overlay, IDRiD_007, baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_007_comparison.png]`
- `[FIG-D.2: Paired attention overlay, IDRiD_017, baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_017_comparison.png]`
- `[FIG-D.3: Paired attention overlay, IDRiD_020, baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_020_comparison.png]`
- `[FIG-D.4: Paired attention overlay, IDRiD_050, baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_050_comparison.png]`

### D.5 What is absent, and what follows from it

The hypothesis under which these plates were produced contemplates two halves: a quantitative
comparison against pixel-level annotation, and a qualitative examination of overlays on the clinical
corpus. **The second half was not carried out.** The clinical overlays were never produced, and this
appendix is therefore confined to the annotated public corpus.

Four consequences follow, and they are the same four recorded in section 3.6. The explainability
evidence of this dissertation rests on one public corpus. This appendix is limited to that corpus
and contains no clinical plate. Closing the gap would require no retraining of any model, only the
generation of the overlays and their review by a qualified reader. And the gap is an **absence
rather than a negative result**: nothing was examined on the clinical corpus and found wanting; the
examination was not performed, and no inference about what it would have shown is available in
either direction.

Accordingly, the claim these plates accompany is supported in its quantitative half only, within the
boundary that separates alignment from localisation, on one annotated corpus and one fold.

---
