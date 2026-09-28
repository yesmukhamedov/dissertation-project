# Defence talk

Собрано из `slides/*/en.md` скриптом `report/build.py`. Не править руками.

**Итого:** 42 слайдов · бюджет 1155 с (19.2 мин) · 2242 слов · при 90 сл/мин ≈ 24.9 мин · регламент 20 мин

| № | Слайд | Бюджет, с | Слов | При 90 сл/мин, с |
|---|---|---|---|---|
| 01 | Title | 20 | 31 | 21 |
| 02 | Relevance of the research | 55 | 100 | 67 |
| 03 | Research aim and objectives | 40 | 53 | 35 |
| 04 | Object, subject and methods of research | 30 | 49 | 33 |
| 05 | Scientific novelty | 45 | 71 | 47 |
| 06 | Provisions submitted for defence | 80 | 122 | 81 |
| 07 | Analysis of existing approaches | 35 | 56 | 37 |
| 08 | Methodology | 5 | 13 | 9 |
| 09 | Overall architecture of the model | 35 | 62 | 41 |
| 10 | Experimental design: 2 × 2 factorial | 40 | 80 | 53 |
| 11 | Data | 5 | 15 | 10 |
| 12 | Datasets | 35 | 64 | 43 |
| 13 | Distribution by camera | 25 | 45 | 30 |
| 14 | Datasets by experiment | 30 | 53 | 35 |
| 15 | Preprocessing stages: input | 25 | 42 | 28 |
| 16 | Canonical flip | 15 | 38 | 25 |
| 17 | Rotation by optic disc and fovea (midpoint) | 15 | 42 | 28 |
| 18 | Crop & resize, field-of-view (FOV) mask | 20 | 54 | 36 |
| 19 | Adaptive CLAHE | 20 | 51 | 34 |
| 20 | Augmentation: rotation | 20 | 54 | 36 |
| 21 | Augmentation: translation, scale, shear | 20 | 32 | 21 |
| 22 | Augmentation: colour, brightness and contrast | 20 | 54 | 36 |
| 23 | Dataset-specific normalisation | 15 | 46 | 31 |
| 24 | Results | 10 | 30 | 20 |
| 25 | Training parameters: focal loss, optimiser, 5-fold CV; metrics: F1, AUC, Cohen's κ, G, ALO | 30 | 47 | 31 |
| 26 | Experiment 1: H-1 — dominance of preprocessing | 40 | 70 | 47 |
| 27 | Experiment 2: H-2 — ablation of pipeline components | 35 | 67 | 45 |
| 28 | Domain distance in feature space (H-3) | 35 | 80 | 53 |
| 29 | Experiment 3: H-4 — cross-dataset generalisation | 30 | 77 | 51 |
| 30 | Experiment 4: H-5 — interpretability (ALO/IoU + Grad-CAM) | 35 | 64 | 43 |
| 31 | Experiment 5: H-7 — external clinical performance | 25 | 53 | 35 |
| 32 | Experiment 6: H-6 — camera domain shift | 25 | 46 | 31 |
| 33 | Experiment 7: small-data training | 30 | 56 | 37 |
| 34 | Discussion | 5 | 14 | 9 |
| 35 | Synthesis: preprocessing as a model component | 30 | 61 | 41 |
| 36 | Limitations of the study | 30 | 61 | 41 |
| 37 | Theoretical significance | 25 | 38 | 25 |
| 38 | Practical significance | 35 | 73 | 49 |
| 39 | Conclusion | 50 | 95 | 63 |
| 40 | Publications | 20 | 50 | 33 |
| 41 | Copyright certificate | 10 | 17 | 11 |
| 42 | Closing title | 5 | 16 | 11 |

## 01. Title

*20 с · 31 слов*

Dear Chair, dear members of the dissertation council! Allow me to present the dissertation "Information system for automatic detection of retinal diseases based on deep learning using optical coherence tomography images".

## 02. Relevance of the research

*55 с · 100 слов*

The relevance has two sides. Clinically, diabetic retinopathy is a leading cause of vision loss in working-age adults, and its early stages are silent. The whole diabetic cohort must therefore be screened on schedule, while Kazakhstan has about twelve hundred ophthalmologists and rural access to them is limited.
Automation was shown feasible ten years ago, but published accuracy is unstable when the camera and acquisition conditions change. Preprocessing is usually treated as ancillary preparation outside the model and goes unreported. If it defines the network's feature space, such models are only partly specified. The research answers this question.

## 03. Research aim and objectives

*40 с · 53 слов*

The aim is to develop an integrated model in which the eight-stage preprocessing pipeline is a model component, and to establish experimentally what it contributes by comparison with an equivalent configuration without the pipeline. The aim is reached through four objectives, one per chapter: analysis, methodology, experimental evaluation and the screening system.

## 04. Object, subject and methods of research

*30 с · 49 слов*

The object is the process of automated retinopathy diagnosis from colour fundus images, as a whole, starting at the camera. The subject is the methods for integrating preprocessing with classification and the properties of the configuration. The main method is controlled comparison: everything but the studied factor is fixed.

## 05. Scientific novelty

*45 с · 71 слов*

The novelty lies on four levels. The main one is conceptual: preprocessing as a model component became an object of experiment. In engineering terms, five pipeline elements are combined for the first time and the clip limit is formalised as the minimum of two constraints. Metrologically, an asymmetric measure of attention alignment is proposed and domain distance is measured directly. Analytically, widely used transfer measures are shown to be non-neutral.

## 06. Provisions submitted for defence

*80 с · 122 слов*

Four provisions are submitted for defence.
First, the eight-stage pipeline formalised as a model component. Stage contributions are separable: adding the stages one by one raises F1 from 0.754 to 0.819 monotonically in all five folds, and the two photometric stages give 41 percent of the gain.
Second, on both architectures the integrated configuration beats the baseline by 6.5 percentage points in F1, 0.03 in AUC and 0.11 in kappa, independently of the architecture.
Third, the pipeline provides transferability: the distance to six external corpora shrinks, and on unseen, device and clinical corpora the integrated configuration is higher.
Fourth, an asymmetric measure of attention–annotation alignment; by it, alignment is higher for all four lesion types.

## 07. Analysis of existing approaches

*35 с · 56 слов*

Existing work was analysed along five directions. Most raise accuracy through architectural complexity and apply preprocessing with default parameters and no ablation; the transfer mechanism is not measured; interpretability stops at qualitative maps; deployed systems do not disclose preprocessing. So preprocessing is written into the model expression and its effect is tested in a controlled experiment.

## 08. Methodology

*5 с · 13 слов*

Next, the methodology: the overall architecture of the model and the experimental design.

## 09. Overall architecture of the model

*35 с · 62 слов*

The input image first passes the eight-stage pipeline: deterministic at inference, with stochastic contrast and augmentation in training. The output is a four-channel tensor: three colour channels and the field-of-view mask. The network returns one of five grades, with referral from grade two. The two eyes are combined at patient level, and Grad-CAM gives the attention map.

## 10. Experimental design: 2 × 2 factorial

*40 с · 80 слов*

The main experiment is a two-by-two factorial: preprocessing is baseline or eight-stage, the architecture is ResNet-50 or EfficientNet-B3. The four cells are trained identically on five patient-level folds, so the difference reads as the factor's effect. The dominance criterion was fixed in advance: at least five percentage points in F1, 0.02 in AUC, no drop in kappa. The baseline is not a copy of a published system but an internal reference point.

## 11. Data

*5 с · 15 слов*

Next, the data: the corpora, their role in each experiment and their distribution by camera.

## 12. Datasets

*35 с · 64 слов*

The eight corpora are grouped by their role in the evidence. Training uses EyePACS only. On APTOS and Messidor-2 the model is tested without retraining. IDRiD is the only corpus with lesion masks; the Kazakhstan clinical set has sixty images. The three device corpora come from cameras absent in training. EyePACS is dominated by the healthy grade — hence focal loss and weighted F1.

## 13. Distribution by camera

*25 с · 45 слов*

The slide compares the distribution of fundus cameras in Central Asian clinics with the cameras of the training corpora. Topcon and Canon dominate in the clinics, and the same two manufacturers dominate the training corpora — so the training distribution largely covers the regional clinical domain.

## 14. Datasets by experiment

*30 с · 53 слов*

The matrix links the seven experiments to the corpora. The first six train on EyePACS and transfer to the other corpora without retraining: one and two — dominance and ablation, three — APTOS, four — attention alignment, five — external clinical performance, six — camera shift. The seventh trains on IDRiD and tests on the local clinical set.

## 15. Preprocessing stages: input

*25 с · 42 слов*

The slide groups the eight preprocessing stages by function: green — four geometric stages, orange — two photometric stages, dashed purple — augmentation, used only in training, red — normalisation and mask append. The pipeline outputs three RGB channels and a binary field-of-view mask.

## 16. Canonical flip

*15 с · 38 слов*

At this stage the left-eye image is flipped horizontally and the right-eye image is left as is. All images thus share one orientation, and the model does not have to learn left and right eyes separately.

## 17. Rotation by optic disc and fovea (midpoint)

*15 с · 42 слов*

At this stage the image is rotated so that the line joining the optic disc and the fovea points in one direction. The landmarks are found by a pretrained frozen detector. Every patient's image is thus brought to one geometric norm.

## 18. Crop & resize, field-of-view (FOV) mask

*20 с · 54 слов*

At this stage the black borders around the image are cropped, leaving only the circular fundus region. The image is scaled isotropically, without distorting proportions, to 512 by 512. The field-of-view mask is fed to the network as a separate fourth channel, so the model knows explicitly where the valid pixels are.

## 19. Adaptive CLAHE

*20 с · 51 слов*

CLAHE is a local contrast enhancement method, applied to the lightness channel of LAB space. The clip limit is computed as the minimum of two constraints — histogram- and tile-relative — and is applied stochastically in training. After processing, fine vessels and microaneurysms are clearly distinguishable — the key signs of early retinopathy.

## 20. Augmentation: rotation

*20 с · 54 слов*

In training the image is rotated by a random angle, with the spread of the angle set by the uncertainty in locating the optic disc and fovea. So even when the orientation at the rotation stage is imprecise, the model learns to recognise retinal structure and becomes robust to images taken at different angles.

## 21. Augmentation: translation, scale, shear

*20 с · 32 слов*

In training the image is randomly translated, scaled and sheared. As a result the model learns to grade correctly even when the central region is off-centre or the crop is imprecise.

## 22. Augmentation: colour, brightness and contrast

*20 с · 54 слов*

This augmentation slightly and randomly changes the colour channels, brightness and contrast. Since every camera renders colour a little differently, the model learns to rely not on colour but on the structural features of the retina. Light and colour are the most variable acquisition factor, so this is the strongest part of the augmentation.

## 23. Dataset-specific normalisation

*15 с · 46 слов*

This is the last stage of the pipeline: pixel values are normalised by the mean and deviation computed over valid fundus pixels. The statistics come only from the training corpus and are never recomputed on a target corpus. The tensor is then passed to the network.

## 24. Results

*10 с · 30 слов*

Let us turn to the results: seven experiments and the domain-distance measurement test seven hypotheses in all. The acceptance criterion of each hypothesis was fixed before its experiment started.

## 25. Training parameters: focal loss, optimiser, 5-fold CV; metrics: F1, AUC, Cohen's κ, G, ALO

*30 с · 47 слов*

Evaluation uses patient-level stratified 5-fold cross-validation, which closes data leakage. The classes are imbalanced, so the loss is inverse-frequency-weighted focal loss. The primary metric is weighted F1, then AUC and quadratic kappa; on external corpora, the generalisation ratio G; for attention, ALO.

## 26. Experiment 1: H-1 — dominance of preprocessing

*40 с · 70 слов*

In the first experiment the integrated configuration is higher on both architectures: on ResNet-50 F1 rose from 0.752 to 0.817, on EfficientNet-B3 from 0.754 to 0.819 — 6.5 percentage points. AUC rose by 0.03 and kappa by 0.11. All three pre-fixed conditions hold on both architectures, significant after Holm correction, with no interaction. The largest gain is in the minority classes.

## 27. Experiment 2: H-2 — ablation of pipeline components

*35 с · 67 слов*

The second experiment adds the stages in turn under a single initialisation. F1 rises from 0.754 to 0.819 monotonically in each of the five folds — the first experiment's gain is fully reproduced by preprocessing. Every step exceeds noise; illumination correction and CLAHE contribute most, 41 percent together. Their parameters have an interior optimum: clip factor 2.5, threshold 0.03, correction scale 0.07.

## 28. Domain distance in feature space (H-3)

*35 с · 80 слов*

The claim that preprocessing improves robustness across domains is usually backed only by external accuracy. We measured the mechanism itself: the distance from the training corpus to six external ones at the penultimate layer falls on all six by 0.070–0.093, with intervals excluding zero, and by 34–38 percent at pixel level. The transform never saw the target corpora. Caveat: the size of the reduction does not predict the size of the gain — only the direction holds.

## 29. Experiment 3: H-4 — cross-dataset generalisation

*30 с · 77 слов*

In the third experiment the model trained on EyePACS was tested on APTOS 2019 without any retraining. Weighted F1 of the integrated configuration is 0.735, of the baseline 0.647 — a difference of 0.089 whose interval excludes zero. The generalisation ratio is 0.898 against 0.858. Both configurations pass the 0.85 threshold, so the evidence lies not in the threshold but in the comparison: on an unseen corpus the integrated configuration is higher.

## 30. Experiment 4: H-5 — interpretability (ALO/IoU + Grad-CAM)

*35 с · 64 слов*

The fourth experiment compares model attention with the expert masks of IDRiD. ALO is the fraction of a lesion covered by attention; it is asymmetric because lesion coverage is what matters clinically. In the integrated configuration ALO is higher for all four types by 0.099–0.129, p below 0.015, regardless of threshold. This is alignment of attention with annotation, not localisation.

## 31. Experiment 5: H-7 — external clinical performance

*25 с · 53 слов*

The fifth experiment tests absolute performance on two external clinical corpora: on IDRiD F1 exceeds the baseline by 0.069, on Messidor-2 by 0.054, both above the minimal clinically important difference of 0.05. This is not robustness to degradation — relative to their own domain both configurations fall back almost equally.

## 32. Experiment 6: H-6 — camera domain shift

*25 с · 46 слов*

The sixth experiment covers five camera groups. The integrated configuration is higher in all five, with the largest gain in the weakest groups. The between-group spread narrows 2.4-fold in F1 and 3.1-fold in AUC: the model depends less on the camera.

## 33. Experiment 7: small-data training

*30 с · 56 слов*

The seventh experiment is the data-scarce regime: training on 516 IDRiD images, testing on the sixty-image Kazakhstan clinical set, with a pre-registered protocol. Here too F1 rose from 0.513 to 0.593 and kappa by 0.12. The gain is comparable to full data — the advantage is not specific to small data.

## 34. Discussion

*5 с · 14 слов*

The discussion covers the synthesis of the results and the limitations of the study.

## 35. Synthesis: preprocessing as a model component

*30 с · 61 слов*

Taken together, the main finding is consistency: the advantage exists in-domain, decomposes across stages, goes with the measured distance and appears on every external corpus, in every camera group, with full and scarce data; the differences are confirmed by DeLong, McNemar and bootstrap. An effect surviving so many conditions is more likely a property of the model's feature space.

## 36. Limitations of the study

*30 с · 61 слов*

Limitations: in the minority classes, especially the mild stage, F1 stays low; the model sometimes attends where there is no lesion, so an ophthalmologist checks the decision. External evaluations rely on single-fold models, the Kazakhstan corpus is closed, and the mask channel's isolated contribution was not measured. The results do not prove clinical validity and are not a certification.

## 37. Theoretical significance

*25 с · 38 слов*

The theoretical significance lies in how the problem is posed and measured. Bringing preprocessing into the model changes what counts as a full model specification and a fair comparison, and five previously informal choices became explicit and testable.

## 38. Practical significance

*35 с · 73 слов*

In practice: first, a preprocessing regime with its full code, whose parameters are re-tuned per corpus. Second, a screening system: the inference service and browser client use the same pipeline code as the experiments and show every stage and the attention map. It runs on a consumer graphics card, and the fourth channel adds under one percent of compute. A copyright certificate was obtained. A clinical field trial is the next step.

## 39. Conclusion

*50 с · 95 слов*

The conclusion follows the objectives. First: the problem was formulated. Second: the eight-stage pipeline was formalised and adapted to two architectures, with the protocol fixed before the experiments. Third: the integrated configuration is 6.5 percentage points higher in F1 in-domain, the gain decomposes by stage, the distance to six corpora shrinks, and on every external, device and clinical corpus and on small data the configuration is higher; attention agrees better with annotation. Fourth: the screening system was built. The main finding is consistency, and it supports treating preprocessing as a model component.

## 40. Publications

*20 с · 50 слов*

The results are published in five papers: one article in a third-quartile Scopus journal, three articles in journals recommended by the authorised body, and one paper at an international Scopus-indexed conference. The work was presented at the international workshop on the digital society in Istanbul in October 2025.

## 41. Copyright certificate

*10 с · 17 слов*

A certificate of entry into the state register of copyright was obtained for the developed software package.

## 42. Closing title

*5 с · 16 слов*

This concludes my presentation. Thank you for your attention! I am ready to answer your questions.
