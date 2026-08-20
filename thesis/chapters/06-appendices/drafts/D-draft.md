> Ported from the superseded appendices, re-lettered, with the provenance banner,
> section signs and internal codes removed and cross-references renumbered to the
> four-chapter body. Transcription content is unchanged. Provenance: `outline/REWRITE_MAP.md`.

# Appendix D — Attention-map gallery

---

## PART 1: SECTION TEXT

### E.1 What this gallery is, and how it must be read

The reading rule comes before the plates, because a gallery of attention maps is more persuasive than it is probative and the distinction matters here.

A gradient-weighted class activation map indicates where activation in the final convolutional layer is high, weighted by its gradient with respect to the predicted class. It is a post-hoc interpretability instrument. **It is not a delineation of pathology.** A plate in which the attention region overlaps an annotated lesion does not show that the model detected that lesion, does not show that the model reasoned from it, and does not constitute clinical localisation. What such an overlap can support is a claim about *alignment* between model evidence and expert annotation — and even that is a claim about the aggregate, not about any individual image.

It follows that **these plates are illustration and carry no measurement**. The measurement is the one reported in section 3.6: Attention–Lesion Overlap as the primary quantity and Intersection-over-Union as the secondary, computed per lesion type over the whole annotated subset with interval estimates and a threshold sweep. A reader who forms an impression from the images in this appendix has not thereby checked that result, and a reader who wishes to check it should read section 3.6 and Appendix B rather than these pages. The gallery exists so that the material behind the measurement can be inspected, not so that the measurement can be re-made by eye.

### E.2 Composition, and why the gallery is exhaustive

The gallery reproduces **all 54 plates of the annotated subset — the entire subset, not a selection**. Each plate pairs the same fundus image under both configurations, the baseline arm on the left and the integrated arm on the right, against the expert pixel-level annotation.

Exhaustiveness is the point rather than a convenience. A gallery that selects its plates can flatter the result it accompanies, and no reader can detect the selection from inside the gallery. Reproducing the subset entire removes that possibility: whatever the plates show, favourable or otherwise, they show for every image on which the measurement was made.

### E.3 The subset, and what bounds it

Of the 516 images in the annotated corpus, 54 carry pixel-level lesion annotation and constitute the subset on which the explainability measurement was performed. Availability differs by lesion type — 54, 53, 54 and 26 images respectively for the four annotated types — so the per-type figure for the least-represented type rests on roughly half the images of the others and is correspondingly the least stable of the four.

One further property of the subset is recorded here because it affects what the plates show. On 6 of the 54 images neither configuration's attention meets the annotation at the operating threshold, leaving 48 informative pairs. **Those 6 plates are included in the gallery, not dropped.** Removing them would convert the gallery into a selection of exactly the kind section D.2 refuses, and their presence is part of what the reader is entitled to see.

The evidence in this appendix rests on a single annotated corpus and on the models of a single cross-validation fold. Neither the corpus nor the fold is varied anywhere in the explainability analysis, and no between-fold variation is available for it.

### E.4 Plate index

The plates follow in identifier order. Each is resolved to its image during document conversion.

- `[FIG-D.1: Paired attention overlay, IDRiD_001 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_001_comparison.png]`
- `[FIG-D.2: Paired attention overlay, IDRiD_002 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_002_comparison.png]`
- `[FIG-D.3: Paired attention overlay, IDRiD_003 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_003_comparison.png]`
- `[FIG-D.4: Paired attention overlay, IDRiD_004 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_004_comparison.png]`
- `[FIG-D.5: Paired attention overlay, IDRiD_005 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_005_comparison.png]`
- `[FIG-D.6: Paired attention overlay, IDRiD_006 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_006_comparison.png]`
- `[FIG-D.7: Paired attention overlay, IDRiD_007 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_007_comparison.png]`
- `[FIG-D.8: Paired attention overlay, IDRiD_008 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_008_comparison.png]`
- `[FIG-D.9: Paired attention overlay, IDRiD_009 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_009_comparison.png]`
- `[FIG-D.10: Paired attention overlay, IDRiD_010 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_010_comparison.png]`
- `[FIG-D.11: Paired attention overlay, IDRiD_011 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_011_comparison.png]`
- `[FIG-D.12: Paired attention overlay, IDRiD_012 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_012_comparison.png]`
- `[FIG-D.13: Paired attention overlay, IDRiD_013 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_013_comparison.png]`
- `[FIG-D.14: Paired attention overlay, IDRiD_014 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_014_comparison.png]`
- `[FIG-D.15: Paired attention overlay, IDRiD_015 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_015_comparison.png]`
- `[FIG-D.16: Paired attention overlay, IDRiD_016 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_016_comparison.png]`
- `[FIG-D.17: Paired attention overlay, IDRiD_017 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_017_comparison.png]`
- `[FIG-D.18: Paired attention overlay, IDRiD_018 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_018_comparison.png]`
- `[FIG-D.19: Paired attention overlay, IDRiD_019 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_019_comparison.png]`
- `[FIG-D.20: Paired attention overlay, IDRiD_020 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_020_comparison.png]`
- `[FIG-D.21: Paired attention overlay, IDRiD_021 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_021_comparison.png]`
- `[FIG-D.22: Paired attention overlay, IDRiD_022 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_022_comparison.png]`
- `[FIG-D.23: Paired attention overlay, IDRiD_023 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_023_comparison.png]`
- `[FIG-D.24: Paired attention overlay, IDRiD_024 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_024_comparison.png]`
- `[FIG-D.25: Paired attention overlay, IDRiD_025 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_025_comparison.png]`
- `[FIG-D.26: Paired attention overlay, IDRiD_026 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_026_comparison.png]`
- `[FIG-D.27: Paired attention overlay, IDRiD_027 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_027_comparison.png]`
- `[FIG-D.28: Paired attention overlay, IDRiD_028 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_028_comparison.png]`
- `[FIG-D.29: Paired attention overlay, IDRiD_029 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_029_comparison.png]`
- `[FIG-D.30: Paired attention overlay, IDRiD_030 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_030_comparison.png]`
- `[FIG-D.31: Paired attention overlay, IDRiD_031 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_031_comparison.png]`
- `[FIG-D.32: Paired attention overlay, IDRiD_032 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_032_comparison.png]`
- `[FIG-D.33: Paired attention overlay, IDRiD_033 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_033_comparison.png]`
- `[FIG-D.34: Paired attention overlay, IDRiD_034 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_034_comparison.png]`
- `[FIG-D.35: Paired attention overlay, IDRiD_035 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_035_comparison.png]`
- `[FIG-D.36: Paired attention overlay, IDRiD_036 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_036_comparison.png]`
- `[FIG-D.37: Paired attention overlay, IDRiD_037 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_037_comparison.png]`
- `[FIG-D.38: Paired attention overlay, IDRiD_038 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_038_comparison.png]`
- `[FIG-D.39: Paired attention overlay, IDRiD_039 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_039_comparison.png]`
- `[FIG-D.40: Paired attention overlay, IDRiD_040 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_040_comparison.png]`
- `[FIG-D.41: Paired attention overlay, IDRiD_041 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_041_comparison.png]`
- `[FIG-D.42: Paired attention overlay, IDRiD_042 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_042_comparison.png]`
- `[FIG-D.43: Paired attention overlay, IDRiD_043 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_043_comparison.png]`
- `[FIG-D.44: Paired attention overlay, IDRiD_044 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_044_comparison.png]`
- `[FIG-D.45: Paired attention overlay, IDRiD_045 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_045_comparison.png]`
- `[FIG-D.46: Paired attention overlay, IDRiD_046 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_046_comparison.png]`
- `[FIG-D.47: Paired attention overlay, IDRiD_047 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_047_comparison.png]`
- `[FIG-D.48: Paired attention overlay, IDRiD_048 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_048_comparison.png]`
- `[FIG-D.49: Paired attention overlay, IDRiD_049 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_049_comparison.png]`
- `[FIG-D.50: Paired attention overlay, IDRiD_050 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_050_comparison.png]`
- `[FIG-D.51: Paired attention overlay, IDRiD_051 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_051_comparison.png]`
- `[FIG-D.52: Paired attention overlay, IDRiD_052 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_052_comparison.png]`
- `[FIG-D.53: Paired attention overlay, IDRiD_053 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_053_comparison.png]`
- `[FIG-D.54: Paired attention overlay, IDRiD_054 — baseline (left) and integrated (right) against the expert annotation — experiments/outputs/exp4/gradcam_maskset/IDRiD_054_comparison.png]`

### E.5 What is absent, and what follows from it

The hypothesis under which these plates were produced contemplates two halves: a quantitative comparison against pixel-level annotation, and a qualitative examination of overlays on the clinical corpus. **The second half was not carried out.** The clinical overlays were never produced, and this appendix is therefore confined to the annotated public corpus.

Four consequences follow, and they are the same four recorded in section 3.6. The explainability evidence of this dissertation rests on one public corpus. This appendix is limited to that corpus and contains no clinical plate. Closing the gap would require no retraining of any model — only the generation of the overlays and their review by a qualified reader. And the gap is an **absence rather than a negative result**: nothing was examined on the clinical corpus and found wanting; the examination was not performed, and no inference about what it would have shown is available in either direction.

Accordingly, the claim these plates accompany is supported in its quantitative half only, within the boundary that separates alignment from localisation, on one annotated corpus and one fold.

---
