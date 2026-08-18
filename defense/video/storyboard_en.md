# Demonstration video — silent screencast storyboard (EN)

For Prof. Dr. Syed Abdul Rahman Al-Haddad bin Syed Mohamed (UPM), foreign consultant.
He asked for a recording of **the eight-stage preprocessing pipeline** and **the Grad-CAM attention
maps**. No voice-over: the captions below are the whole commentary, burned into the picture.

**Patient:** EyePACS **294** - a genuine bilateral pair, both eyes graded **4 (proliferative)** by
the dataset's readers. Files already on disk:

```
demo\web\public\datasets\eyepacs\pairs\dr4\294_right.jpeg   -> right-eye slot (shown left)
demo\web\public\datasets\eyepacs\pairs\dr4\294_left.jpeg    -> left-eye slot  (shown right)
```

Chosen by running the live backend over every bilateral pair on disk. It is the only patient that
clears all four conditions at once:

- the left image is a **true left eye**, so Stage 0 visibly mirrors it, while the right eye passes
  through unchanged, which is exactly what Stage 0 should do;
- the OD/fovea detector is **confident on both eyes** (0.56), so Stage 1 actually rotates; on a
  low-confidence image the rotation is skipped and that slide shows nothing;
- flat-field and CLAHE both change the picture strongly;
- the model returns **grade 4 for both eyes** (confidence 0.61 and 0.69), agreeing with the
  dataset's readers, so the "confirm" beat is honest.

Both eyes carry peripheral photocoagulation scars alongside the retinopathy, which is what treated
proliferative disease looks like. The captions therefore say **where** attention lands, and do not
name lesion types the picture does not show.

Rejected alternatives, for the record: **163** (3/3) - the detector is not confident on its left eye,
so Stage 1 is a no-op there; **352**, **328**, **78**, **15** - the model under-calls one or both
eyes. **79** (2/2) is correct but hazy and low in contrast; it is the fallback if a
non-proliferative case is preferred.

**Upload the two files by hand — do not use "Test with Random Patient Images".** Only a manual
upload runs the **live Grad-CAM from the checkpoint**; the bundled walk-through cases carry
pre-generated proxy heat maps that are not a real Grad-CAM, and the video must not show those.

## How this file is used

`build_video.py` reads it and writes two things:

- `subtitles_en.srt` — the captions, timed exactly as specified here;
- `shotlist.md` — the same beats with **absolute timecodes**, i.e. the sheet to record against.

Syntax per beat: `**Hold:** N` = N seconds of picture with no caption (that is where the action
happens); each `> [N] text` line is one caption shown for N seconds. Time is cumulative — change a
number and every following timecode moves with it. Captions are written to stay under ~13 characters
per second, which is a comfortable reading pace for a non-native reader.

## Recording

1080p, browser at 100 % zoom, no other tabs, notifications off. Unlock the PIN gate **before**
recording starts. Move the mouse slowly; every click in `**Do:**` should land inside its Hold window.

---

# PART 1 — Lite mode (what a clinician sees)

## B01 · Opening

**Do:** demo open in Lite mode, top of the page, nothing loaded yet.
**Hold:** 1

**Caption:**

> [4.5] Dear Professor Al-Haddad — the demonstration you asked for.
> [3.5] No sound: the captions are the commentary.
> [4.5] First the eight-stage pipeline, then the Grad-CAM maps.

## B02 · The two views

**Do:** point at the Lite / Full switch in the top bar, do not click it yet.
**Hold:** 1

**Caption:**

> [6] This is Lite mode — the clinician's screen. The research view comes later.

## B03 · Loading the patient

**Do:** drop `294_right.jpeg` into the right-eye slot, then `294_left.jpeg` into the left-eye slot.
**Hold:** 6

**Caption:**

> [4] One patient, both eyes, uploaded as ordinary files.
> [4.5] EyePACS case 294 - proliferative retinopathy in both eyes.
> [4.5] The system is not told that grade. We compare against it.

## B04 · The case opens

**Do:** let the two thumbnails settle; the case note appears under the slots.
**Hold:** 2

**Caption:**

> [7] Each image is checked to be a fundus photograph, then a patient case opens on the server.

## B05 · Entering the pipeline

**Do:** on the left-eye card, click **"Show preprocessing stages"**.
**Hold:** 3

**Caption:**

> [4.5] Every stage can now be inspected one by one, on this eye.

## B06 · Stage 0 — original

**Do:** stop on slide **"0. Original"**.
**Hold:** 1

**Caption:**

> [5] The image as it left the camera: a left eye, disc on the left.

## B07 · Stage 0 — canonical flip

**Do:** click ▸ to **"0. Canonical flip"**. Step back and forward once so the mirroring is visible.
**Hold:** 2

**Caption:**

> [4.5] Stage 0 mirrors every left eye into right-eye orientation.
> [5] After it, the optic disc sits on the same side in every image.

## B08 · OD and fovea detection

**Do:** click ▸ to the **"OD · fovea detection"** slide. Show the confidence chip; toggle the
probability heat map on and off; drag the fovea marker slightly, then undo the drag (do not save).
**Hold:** 3

**Caption:**

> [5] A trained heat-map detector finds the optic disc and the fovea.
> [4.5] It reports its confidence and can show its probability map.
> [5.5] A clinician who disagrees drags the markers; the pipeline re-runs.

## B09 · Stage 1 — rotation

**Do:** click ▸ to **"1. OD-fovea rotation"**.
**Hold:** 2

**Caption:**

> [4] Stage 1 rotates the disc-to-fovea axis horizontal.
> [4] Camera tilt stops being a difference between images.

## B10 · Stage 2 — FOV crop and resize

**Do:** click ▸ to **"2. FOV crop + resize"**.
**Hold:** 2

**Caption:**

> [4.5] Stage 2 crops the field of view and resizes to 512 by 512.
> [4] The resize is isotropic — nothing is stretched.

## B11 · Stage 3 — FOV mask

**Do:** click ▸ to **"3. FOV mask"**.
**Hold:** 2

**Caption:**

> [4] Stage 3 builds a binary mask of the field of view.
> [4.5] The mask becomes the fourth input channel of the network.

## B12 · Stage 4 — flat-field

**Do:** click ▸ to **"4. Flat-field"**. Step back to Stage 2 and forward again once.
**Hold:** 3

**Caption:**

> [4] Stage 4 removes the camera's illumination gradient.
> [4.5] The dark corners lift; lesions stop competing with shading.

## B13 · Stage 5 — CLAHE

**Do:** click ▸ to **"5. CLAHE"**. Step back and forward once.
**Hold:** 3

**Caption:**

> [4.5] Stage 5 is dual-constraint CLAHE on the lightness channel.
> [5] The second constraint keeps the optic disc from burning out.
> [5] These two photometric stages carry 41 % of the measured gain.

## B14 · What the network receives

**Do:** scroll to the channel row under the CLAHE slide — R, G, B, FOV.
**Hold:** 2

**Caption:**

> [4.5] The channels of the final stage are the CNN input itself.
> [3.5] Red, green, blue — and the field-of-view mask.

## B15 · The two stages you cannot see here

**Do:** stay on the same screen.
**Hold:** 1

**Caption:**

> [5.5] Two stages are absent by design: augmentation runs only in training,
> [4.5] and Stage 7 is the normalisation that produces the tensor.

## B16 · Inference

**Do:** click **"Run inference"**; wait for the result card.
**Hold:** 5

**Caption:**

> [5] The classifier: EfficientNet-B3, five grades, four channels.
> [5.5] Patient grade, class probabilities, referable flag, measured latency.

## B17 · Per eye

**Do:** point at the per-eye panel.
**Hold:** 1

**Caption:**

> [5.5] Each eye is graded on its own; either eye can make a patient referable.

## B18 · Grad-CAM

**Do:** scroll to the attention overlays; let both eyes finish rendering.
**Hold:** 6

**Caption:**

> [5] Grad-CAM, computed live from the model checkpoint, for each eye.
> [5] Attention gathers on the affected periphery, away from disc and vessels.
> [4] The line below it is generated from the map geometry.

## B19 · The limit of that claim

**Do:** point at the note under the overlays.
**Hold:** 1

**Caption:**

> [5.5] This is attention alignment, not clinical localisation of pathology.
> [4] An interpretability tool, never a diagnostic output.

## B20 · The ophthalmologist agrees

**Do:** click **"Confirm prediction"**; the standing verdict replaces the buttons.
**Hold:** 3

**Caption:**

> [5.5] Here the model's grade matches the dataset's, and the reviewer confirms it.
> [4.5] One verdict per prediction, with an undo.

## B21 · The ophthalmologist disagrees

**Do:** click undo; then **"Reject — provide correct grade"**, choose a different grade, click
**"Add to training buffer"**.
**Hold:** 5

**Caption:**

> [5] A disagreement is recorded the same way, with the correct grade.
> [5] It is stored in the patient case and in a buffer for retraining.

## B22 · What survives the session

**Do:** scroll to the relabeling buffer and the statistics panel; hover **"Export JSONL"** without
clicking.
**Hold:** 2

**Caption:**

> [7] The buffer exports as JSONL; the totals are read from disk, so a disagreement survives a reload.

---

# PART 2 — Full mode (the research view)

## B23 · Switching

**Do:** click the switch to **Full**; the sidebar appears.
**Hold:** 3

**Caption:**

> [4.5] The same page in Full mode: everything behind the demo.

## B24 · Overview

**Do:** **Overview** tab; scroll slowly once.
**Hold:** 2

**Caption:**

> [5.5] The claim of the work: the model is preprocessing plus the network.
> [5] The pipeline is a component of it, not preparation of the data.

## B25 · Pipeline

**Do:** **Model → Pipeline**; scroll through the stage diagram to the end.
**Hold:** 3

**Caption:**

> [5] All eight stages, including the two the live strip cannot show.
> [5.5] Stage 6 — affine, colour jitter, noise, JPEG — training time only.
> [4.5] Stage 7 — dataset-specific normalisation into the tensor.

## B26 · Architecture and explainability

**Do:** **Model → Architecture**, stop on the 4-channel stem; then **Model → Explainability**.
**Hold:** 3

**Caption:**

> [5] The only change to the backbone is a fourth channel in the stem.
> [4.5] And this is how the attention maps are produced and scored.

## B27 · Datasets

**Do:** **Datasets**; scroll once.
**Hold:** 2

**Caption:**

> [6.5] Eight datasets: EyePACS for training, the rest for transfer and external clinics.

## B28 · Experiment 1

**Do:** **Exp 1 (H-1): Factorial**; stop on the A–D table.
**Hold:** 3

**Caption:**

> [5.5] Two backbones by two arms, 35,126 images, five-fold cross-validation.
> [5.5] Weighted F1 rises from 0.754 to 0.819 — the same on both backbones.
> [6.5] The arms differ in pipeline and initialisation, so the gain is the configuration's.

## B29 · Experiment 2

**Do:** **Exp 2 (H-2): Ablation**; stop on the cumulative chart, then the per-stage contributions.
**Hold:** 3

**Caption:**

> [5.5] Experiment 2 adds the stages one at a time, under one initialisation.
> [5.5] Each contributes significantly; together they reproduce the whole gain.
> [3.5] Flat-field and CLAHE lead — that is the 41 %.

## B30 · Experiment 4 — explainability

**Do:** **Exp 4 (H-5): Explainability**; stop on the ALO table.
**Hold:** 3

**Caption:**

> [5.5] The attention claim, measured on 54 IDRiD images with lesion masks.
> [5.5] Overlap rises for all four lesion types; every interval excludes zero.

## B31 · Transfer and external clinics

**Do:** **Exp 3 (H-4): APTOS**, then **Exp 5 (H-4/H-7): Transfer**.
**Hold:** 3

**Caption:**

> [5] Zero-shot transfer to APTOS, then two external clinical sets.
> [4] Plus 6.9 points on IDRiD, plus 5.4 on Messidor-2.

## B32 · Devices and small data

**Do:** **Exp 6 (H-6): Devices**, then **Exp 7: Small Data**.
**Hold:** 3

**Caption:**

> [5] Across five camera groups the spread between devices narrows.
> [4] On a small clinical set the pipeline still wins.

## B33 · Results

**Do:** **Results → Main Metrics**, then **Statistical Tests**.
**Hold:** 3

**Caption:**

> [5.5] The headline metrics, and the tests behind them: DeLong, McNemar, Holm.

## B34 · The cost

**Do:** **Validation → Computational**.
**Hold:** 2

**Caption:**

> [5] The fourth channel costs under 1 % in FLOPs and 24 megabytes.
> [3.5] The pipeline is a cheap prior.

## B35 · Closing

**Do:** back to **Overview**, then to the Lite demo screen.
**Hold:** 2

**Caption:**

> [5] The demo is online; I will keep the backend running to suit you.
> [3.5] Thank you for your time and for your review.

---

## Numbers in the captions — provenance

All from `results/` (the single source of truth), never from the demo's own constants:

| Caption | Value | Source |
|---|---|---|
| 0.754 → 0.819 | Config C → D, weighted F1 | `results/STATUS.md` exp1 |
| same on both backbones | +6.54 / +6.55 pp | `results/STATUS.md` exp1 |
| 41 % from two photometric stages | 0.0143 + 0.0125 of 0.0655 | `results/STATUS.md` exp2 |
| stages reproduce the whole gain | L0 → L7 = +0.0655, one initialisation | `results/STATUS.md` exp2 |
| 4/4 lesion types, 54 images | ALO, τ = 0.5 | `results/STATUS.md` exp4 |
| +6.9 / +5.4 points | IDRiD +0.0689, Messidor-2 +0.0541 | `results/STATUS.md` exp5 |
| under 1 %, 24 MB | +0.4 GFLOPs (+0.9 %), +24 MiB | `results/tables/computational_and_iq.md` |
| 35,126 images, five-fold | Experiment 1 protocol | `results/STATUS.md` |

Governance kept in the wording: the Experiment-1 gain is attributed to the configuration as a whole
(the arms differ in initialisation too); Grad-CAM is attention alignment, never clinical
localisation; nothing claims clinical validation or a medical device.
