# SECTION BRIEF
## Appendix E — Grad-CAM Visualization Gallery

**Chapter:** Appendices (back matter)
**Section Function:** reproduce the paired attention overlays behind §4.6 and §5.1, in full and without selection
**Word Count Target:** prose 700–1,000 words; the plates carry the appendix

> **Gate check:** PASSED, bounded. **54 paired comparison plates exist on disk** for the annotated mask
> subset — the gallery is real, not a placeholder. What does **not** exist is the qualitative examination
> on the clinical corpus that H-5 also contemplates: those overlays were never produced (gap G-3), so the
> appendix is confined to the annotated public corpus and says so.

---

### GOVERNANCE BINDINGS

**Primary claims:** PC-7 — STRONG **within NC-14**, one annotated corpus, one fold, qualitative half unevaluated.
**Non-claims:** **NC-14** — the governing constraint of this appendix.
**Forbidden claims:** CFC-2.4, CFC-2.5, CFC-2.2, CFC-2.1.
**Scope boundaries:** SB-1.11 (Grad-CAM is not clinical validation of the model's reasoning), SB-2.3, SB-3.1.
**Source rules:** SIR-1, SIR-2.
**Evidence thresholds:** EH-2 — explainability metrics are supplementary.

---

### CONTENT SPECIFICATION

**Section objective:** Let a reader look at the material the ALO and IoU figures were computed on, under a
reading rule stated before the first plate.

**Structure:**
- **E.1 What the gallery is, and the reading rule first.** NC-14 before anything else: an activation map
  indicates where gradient-weighted activation is high in the final convolutional layer. It is **not** a
  delineation of pathology, and a plate in which attention sits over a lesion is not a detection.
  **The plates carry no measurement**; the measurement is §4.6.2's, and a reader who forms an impression
  from the images has not thereby checked the result.
- **E.2 Composition and the reason it is exhaustive.** All 54 plates of the annotated subset are
  reproduced — the entire subset, not a selection. State why: a gallery that selects is a gallery that
  can flatter, and the exhaustiveness is what makes it inspectable. Each plate pairs the same image under
  both configurations against the expert annotation.
- **E.3 The subset and what bounds it.** 54 images of 516 carry pixel-level annotation; per-type
  availability differs (54 / 53 / 54 / 26), and the smallest type is the one whose per-type figure is
  least stable. The floor case — images on which neither configuration's attention meets the annotation
  at the operating threshold — is 6 of 54, leaving 48 informative pairs; those 6 plates are included, not
  dropped, and are identified as such.
- **E.4 Plate index.** The 54 plates, by identifier, as figure markers resolved at conversion.
- **E.5 What is absent, and its consequence.** The qualitative examination on the clinical corpus was not
  carried out; H-5 is supported in its quantitative half only. State the four consequences §4.6.3
  records: the evidence rests on one public corpus, this appendix is confined to it, closing the gap
  requires no retraining, and the absence is an absence rather than a negative result.

---

### SOURCE MAPPING

| Source | Role | Content |
|---|---|---|
| §4.6.1 | binding | paired design, mask subset and per-type counts, τ sweep, floor control |
| §4.6.2 | binding | the ALO/IoU measurement the plates illustrate |
| §4.6.3 | binding | per-image direction counts; the G-3 absence and its four consequences |
| §5.1 | binding | the corroboration argument and the ceiling NC-14 imposes |
| `experiments/outputs/exp4/gradcam_maskset/` | asset | the 54 paired comparison plates |

**⚠️ Rule-16 note.** Artifact paths are forbidden in prose **except inside figure markers**, which
legitimately carry an image path and are resolved at conversion. Paths appear only there.

---

### BOUNDARY WARNINGS

1. **NC-14 before the first plate**, not after the last.
2. **The plates are illustration, not evidence.** Say it explicitly; a gallery invites the opposite reading.
3. **No per-plate interpretation.** Commenting on individual images would be exactly the post-hoc
   pattern-finding §4.6.3 refuses; the appendix indexes, it does not narrate.
4. **No metric value** beyond the counts already established (54, 53, 26, 6, 48, 516).
5. **The floor cases stay in.** Removing them would make the gallery a selection.
6. **G-3 stated as an absence**, in its own passage, with its consequences.

---

### ACCEPTANCE CRITERIA

- [ ] NC-14 stated before any plate is described.
- [ ] Exhaustiveness stated with the reason for it.
- [ ] Subset bounds present: 54 of 516; per-type 54/53/54/26; floor 6 of 54 → 48 informative.
- [ ] All 54 plates indexed as figure markers.
- [ ] G-3 absence with its four consequences.
- [ ] No per-plate commentary; no new number.

---

### WRITING DIRECTIVES

- **Tense:** present for what a plate shows; past for what was measured.
- **Register:** restrained. The risk of a figure gallery is that it persuades more than it demonstrates.
