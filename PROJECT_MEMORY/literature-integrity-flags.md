---
name: literature-integrity-flags
description: "Known mismatches/gaps in thesis/literature corpus found during Ch1 drafting (2026-06-09)"
metadata:
  type: project
---

Corpus-integrity issues found while drafting Chapter 1 (2026-06-09), flagged not fixed:

1. **FIXED:** `external/schmidt-erfurth-2018.md` actually contained Kusuhara et al. (2018) "Pathophysiology of DR" (DMJ, DOI 10.4093/dmj.2018.0182) — Schmidt-Erfurth was only a paper cited inside it. Renamed → `kusuhara-2018.md`; updated 1.1.1 draft + brief; LITERATURE_INDEX #32 already read "Kusuhara et al. (2018)" so no index edit needed. Zero stale `schmidt-erfurth-2018` refs remain.

2. **RESOLVED (2026-06-16):** All dataset-descriptor cards now exist. **#46 (Grad-CAM/Selvaraju), #47 (EyePACS/Cuadros & Bresnick 2009), #48 (Messidor/Decencière 2014)** were written 2026-06-12 from PDFs in `C:\Users\yesmu\Downloads\litres` (`selvaraju-2017-grad-cam.md`, `cuadros-2009-eyepacs.md`, `decenciere-2014-messidor.md`). **#49 (RFMiD/Pachade 2021) `pachade-2021-rfmid.md`, #50 (DDR/Li 2019) `li-2019-ddr.md`, #51 (ODIR-2019/ODIR-5K) `odir-2019-dataset.md`** written 2026-06-16 from open-access sources (no PDFs on disk; `litres` folder gone) — each carries a Source-access note + `[NOT REPORTED]`/`[VERIFY]` flags. **#51 "TO BE IDENTIFIED" is resolved:** ODIR-5K has NO peer-reviewed descriptor; carded/cited as the ODIR-2019 challenge **electronic resource** (GOST online-resource form). **Residual:** #50 DDR card is abstract+repo-based (full Elsevier text was paywalled) — upgrade from the full PDF when available. EyePACS card clarifies the ~35,126-image count is a *Kaggle-competition* attribute, not from Cuadros & Bresnick; Messidor card flags Messidor (1,200) vs Messidor-2 (1,748). See [[literature-corpus-120]]. The #46/#47/#48 cards were integrated into approved drafts (#46→§2.5.1, #47→§1.2.3+§4.1.1, #48→§4.1.1); #49/#50/#51 are still cited only at index-only camera-attribute level in §1.2.3+§4.1.1 — full-depth use is §4.7 (Phase 2, unwritten). See [[thesis-writing-status]].

3-bis. **ANSWERED 2026-08-25 — `scopus-q2.md` is NOT the candidate's paper.** Checked against the
publishers. The card's content (STARE, 157/152 images, five classes BDR/CRVO/CNV/PDR/Normal,
upgraded CLAHE `CLIP LIMIT = T/80`, fine-tuned RESNET50 224×224, 100 epochs, 100% acc/sens/spec,
page locators to p. 12) is the **external** paper *«Retinal disease identification using upgraded
CLAHE filter and transfer convolution neural network»*, **ICT Express 8(1):142–150, 2022**
(ScienceDirect S2405959521000564) — not the EEJET article whose citation line is pasted at the top
of the card. So of the two readings in note 3 the second is right: a wrong citation line, not a
duplicate. The ID `LC-AlTimemy-2021` was therefore **correct in substance** (governance already
treats it as an external source in INVARIANTS SB-1.2 / CFC-1.4 / CFC-2.5 / SIR-3, ARGUMENT_MAP,
both glossaries, `methods/implementation.md`) and must NOT be renamed — a rename attempted on
2026-08-25 was reverted for exactly that reason. ⚠ The author attribution behind the label is a
second open question: the search result names the ICT Express authors as S. S. M. Muhammad, T. S.
Tan, M. A. Ansari, W. H. W. Hitam, J. S. Y. Sia, so "AlTimemy" may itself be wrong.

**Consequence in the printed volume — NOT yet fixed, needs the candidate.** `_finalize_citations.py`
maps the EEJET author keys and the §2.2 T/80 passage onto this card, so the volume attributes an
external contribution to the candidate as own prior work: §2.2 («The candidate's prior work [1]
replaced the derived clip with a single controllable global threshold»), the §2.1 clause «an
upgraded equalisation variant was studied on a different retinal database», and §1.2 («preprocessing
raised validation accuracy from 71 to 86 per cent») all print `[1]` = EEJET. The EEJET landing page
states a **proprietary** dataset and **88% → 91%**, while card `scopus-q3.md` records APTOS 2019 and
**71% → 86%** — a third thing to settle from the offprint. See [[self-citation-compliance]].

3. **OPEN — self-card ID anomaly:** `self/yesmukhamedov-scopus-q2.md` carries Unique ID `LC-AlTimemy-2021` but its bibliographic-citation line shows the Sapakova/Yesmukhamedov/Sapakov (2025) EEJET paper (DOI 10.15587/1729-4061.2025.335570) — same paper as `scopus-q3.md` (`LC-SAPAKOVA-2025-01`, the real #24). INVARIANTS treats LC-AlTimemy-2021 as a *distinct* STARE/T-80 CLAHE study (100% acc, sensitivity-formula anomaly). Possible mislabel: scopus-q2 may be the AlTimemy card with a wrong citation line, or a duplicate. Verify which paper scopus-q2 actually analyses before citing #23 vs the AlTimemy STARE study in Ch 2/3. See [[strip-version-markers]].

4. **RESOLVED (2026-06-16) — #52/#53 cards written; Hinton-2012 still open.** The Stage-G citation preview found **#52 Guo et al. (2017) "On Calibration of Modern Neural Networks"** and **#53 Wang et al. (2004) SSIM** cited (§2.6/§3.1/§3.4.1/§5.2) but uncarded. Both cards now written from open sources: `guo-2017-calibration.md` (ECE/reliability diagrams/temperature scaling; arXiv:1706.04599) and `wang-2004-ssim.md` (SSIM luminance×contrast×structure; IEEE TIP 13(4):600–612, DOI 10.1109/TIP.2003.819861) — each with a Source-access note + `[VERIFY]` where worked from abstract+canon. LITERATURE_INDEX rows #52/#53 updated. **"Hinton (2012)" RESOLVED 2026-06-16 — not a gap:** both in-text occurrences (§2.2.2 + §2.2.3) are the full phrase **"Krizhevsky, Sutskever, and Hinton (2012)" = AlexNet** (carded `krizhevsky-2012-alexnet.md`, #65); the flag was a Stage-G extractor artifact (comma-separated author list truncated to the last surname). Drafts are correct — no change needed; the conversion map collapses `hinton|2012`→AlexNet. **No corpus gaps remain from the assembly/Stage-G review.** See [[thesis-assembly]].

Source-number map confirmed during drafting: #24 = `scopus-q3.md` (LC-SAPAKOVA-2025-01, val-acc 71%→86%, ROC-AUC 0.9638); #22 = `nan-rk.md` (LC-2025-Yesmukhamedov-01, system architecture).
