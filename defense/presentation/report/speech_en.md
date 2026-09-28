# Defence talk

Собрано из `slides/*/en.md` скриптом `report/build.py`. Не править руками.

**Итого:** 33 слайдов · бюджет 1033 с (17.2 мин) · 2038 слов · при 90 сл/мин ≈ 22.6 мин · регламент 20 мин

| № | Слайд | Бюджет, с | Слов | При 90 сл/мин, с |
|---|---|---|---|---|
| 01 | Title | 20 | 31 | 21 |
| 02 | Relevance of the research | 55 | 101 | 67 |
| 03 | Research aim and objectives | 55 | 72 | 48 |
| 04 | Provisions submitted for defence | 75 | 102 | 68 |
| 05 | Analysis of existing approaches | 35 | 56 | 37 |
| 06 | Mathematical formulation and architecture of the model | 45 | 96 | 64 |
| 07 | Experimental design: 2 × 2 factorial | 40 | 80 | 53 |
| 08 | Datasets | 35 | 64 | 43 |
| 09 | Distribution by camera | 25 | 45 | 30 |
| 10 | Datasets by experiment | 30 | 53 | 35 |
| 11 | Preprocessing stages: input | 25 | 42 | 28 |
| 12 | Canonical flip | 15 | 38 | 25 |
| 13 | Rotation by optic disc and fovea (midpoint) | 15 | 42 | 28 |
| 14 | Crop & resize, field-of-view (FOV) mask | 20 | 54 | 36 |
| 15 | Flat-field correction and polar CLAHE | 35 | 68 | 45 |
| 16 | Augmentation: rotation | 20 | 54 | 36 |
| 17 | Augmentation: scale and shear | 20 | 33 | 22 |
| 18 | Augmentation: colour, brightness, contrast, noise | 25 | 78 | 52 |
| 19 | Dataset-specific normalisation | 15 | 46 | 31 |
| 20 | Training parameters: focal loss, optimiser, 5-fold CV; metrics: F1, AUC, Cohen's κ, G, ALO | 38 | 68 | 45 |
| 21 | Experiment 1: contribution of preprocessing across two architectures | 40 | 70 | 47 |
| 22 | Experiment 2: ablation of pipeline stages | 40 | 89 | 59 |
| 23 | Domain distance in feature space | 35 | 80 | 53 |
| 24 | Experiment 3: transfer to another dataset | 30 | 77 | 51 |
| 25 | Experiment 4: interpretability (ALO, Grad-CAM) | 35 | 64 | 43 |
| 26 | Experiment 5: accuracy on external clinical data | 25 | 53 | 35 |
| 27 | Experiment 6: robustness to camera change | 25 | 46 | 31 |
| 28 | Experiment 7: small-data training | 30 | 56 | 37 |
| 29 | Screening system | 35 | 80 | 53 |
| 30 | Conclusion | 60 | 117 | 78 |
| 31 | Publications | 20 | 50 | 33 |
| 32 | Copyright certificate | 10 | 17 | 11 |
| 33 | Closing title | 5 | 16 | 11 |

## 01. Title

*20 с · 31 слов*

Dear Chair, dear members of the dissertation council! Allow me to present the dissertation "Information system for automatic detection of retinal diseases based on deep learning using optical coherence tomography images".

## 02. Relevance of the research

*55 с · 101 слов*

Registered diabetes patients in Kazakhstan doubled in ten years to 517 thousand, and early retinopathy is asymptomatic, so every patient needs an annual fundus examination. The country has about one and a half thousand ophthalmologists — some three hundred and forty patients per doctor — and in rural areas, home to a third of the population, only a tenth of ophthalmologists work. The answer is automated screening from fundus images. But the accuracy of published models is unstable across cameras and acquisition conditions, and preprocessing is usually treated as preparation outside the model and left undescribed. This is the problem the research addresses.

## 03. Research aim and objectives

*55 с · 72 слов*

The aim is to develop an integrated model in which the preprocessing pipeline is a model component, and to establish experimentally what it contributes by comparison with an equivalent configuration without the pipeline. The object is the process of automated retinopathy diagnosis from colour fundus images; the subject is preprocessing methods and their integration with convolutional networks. The aim is reached through four objectives: analysis, methodology, experimental evaluation and the screening system.

## 04. Provisions submitted for defence

*75 с · 102 слов*

The scientific novelty: for the first time, fundus image preprocessing is formalised as a model component and studied in a controlled factorial experiment.
Four provisions are submitted for defence. First, the eight-stage preprocessing pipeline as a model component; it provides independence from orientation, geometry, illumination and camera, as the ablation and the experiments on external corpora show. Second, the integrated model with a four-channel input; its advantage over the baseline does not depend on the network architecture. Third, the ALO measure, which compares model attention with expert annotation. Fourth, the screening system, for which a copyright certificate has been obtained.

## 05. Analysis of existing approaches

*35 с · 56 слов*

Existing work was analysed along five directions. Most raise accuracy through architectural complexity and apply preprocessing with default parameters and no ablation; the transfer mechanism is not measured; interpretability stops at qualitative maps; deployed systems do not disclose preprocessing. So preprocessing is written into the model expression and its effect is tested in a controlled experiment.

## 06. Mathematical formulation and architecture of the model

*45 с · 96 слов*

Formally the model is a composition: the network is applied to the pipeline output and its parameters are trained on that output, so the pipeline belongs to the definition of the model. The input image first passes the eight-stage pipeline: deterministic at inference, with stochastic contrast and augmentation in training. The output is a four-channel tensor: three colour channels and the field-of-view mask. The network returns one of five grades, with referral from grade two. The patient's grade is that of the worse eye, and Grad-CAM gives the attention map.

## 07. Experimental design: 2 × 2 factorial

*40 с · 80 слов*

The main experiment is a two-by-two factorial: preprocessing is baseline or eight-stage, the architecture is ResNet-50 or EfficientNet-B3. The four cells are trained identically on five patient-level folds, so the difference reads as the factor's effect. The dominance criterion was fixed in advance: at least five percentage points in F1, 0.02 in AUC, no drop in kappa. The baseline is not a copy of a published system but an internal reference point.

## 08. Datasets

*35 с · 64 слов*

The eight corpora are grouped by their role in the evidence. Training uses EyePACS only. On APTOS and Messidor-2 the model is tested without retraining. IDRiD is the only corpus with lesion masks; the Kazakhstan clinical set has sixty images. The three device corpora come from cameras absent in training. EyePACS is dominated by the healthy grade — hence focal loss and weighted F1.

## 09. Distribution by camera

*25 с · 45 слов*

The slide compares the distribution of fundus cameras in Central Asian clinics with the cameras of the training corpora. Topcon and Canon dominate in the clinics, and the same two manufacturers dominate the training corpora — so the training distribution largely covers the regional clinical domain.

## 10. Datasets by experiment

*30 с · 53 слов*

The matrix links the seven experiments to the corpora. The first six train on EyePACS and transfer to the other corpora without retraining: one and two — dominance and ablation, three — APTOS, four — attention alignment, five — external clinical performance, six — camera shift. The seventh trains on IDRiD and tests on the local clinical set.

## 11. Preprocessing stages: input

*25 с · 42 слов*

The slide groups the eight preprocessing stages by function: green — four geometric stages, orange — two photometric stages, dashed purple — augmentation, used only in training, red — normalisation and mask append. The pipeline outputs three RGB channels and a binary field-of-view mask.

## 12. Canonical flip

*15 с · 38 слов*

At this stage the left-eye image is flipped horizontally and the right-eye image is left as is. All images thus share one orientation, and the model does not have to learn left and right eyes separately.

## 13. Rotation by optic disc and fovea (midpoint)

*15 с · 42 слов*

At this stage the image is rotated so that the line joining the optic disc and the fovea points in one direction. The landmarks are found by a pretrained frozen detector. Every patient's image is thus brought to one geometric norm.

## 14. Crop & resize, field-of-view (FOV) mask

*20 с · 54 слов*

At this stage the black borders around the image are cropped, leaving only the circular fundus region. The image is scaled isotropically, without distorting proportions, to 512 by 512. The field-of-view mask is fed to the network as a separate fourth channel, so the model knows explicitly where the valid pixels are.

## 15. Flat-field correction and polar CLAHE

*35 с · 68 слов*

Stage four evens out the illumination: a blurred copy is subtracted from the image, at a scale of 0.07 of the field-of-view diameter. Stage five is polar CLAHE: contrast is enhanced locally in rings and sectors around the fovea, finer where vessels are denser; the clip limit is the minimum of two constraints. Fine vessels and microaneurysms — the early signs of retinopathy — become clearly visible.

## 16. Augmentation: rotation

*20 с · 54 слов*

In training the image is rotated by a random angle, with the spread of the angle set by the uncertainty in locating the optic disc and fovea. So even when the orientation at the rotation stage is imprecise, the model learns to recognise retinal structure and becomes robust to images taken at different angles.

## 17. Augmentation: scale and shear

*20 с · 33 слов*

In training the image is randomly scaled, slightly stretched and sheared. As a result the model learns to grade correctly even when the central region is off-centre or the crop is imprecise.

## 18. Augmentation: colour, brightness, contrast, noise

*25 с · 78 слов*

This augmentation slightly and randomly changes the colour channels, brightness and contrast. Since every camera renders colour a little differently, the model learns to rely not on colour but on the structural features of the retina. In addition, noise and JPEG compression are added with a small probability — as with an inexpensive camera and an image sent over a network. Light and colour are the most variable acquisition factor, so this is the strongest part of the augmentation.

## 19. Dataset-specific normalisation

*15 с · 46 слов*

This is the last stage of the pipeline: pixel values are normalised by the mean and deviation computed over valid fundus pixels. The statistics come only from the training corpus and are never recomputed on a target corpus. The tensor is then passed to the network.

## 20. Training parameters: focal loss, optimiser, 5-fold CV; metrics: F1, AUC, Cohen's κ, G, ALO

*38 с · 68 слов*

Seven experiments and the domain-distance measurement test seven hypotheses; the acceptance criterion of each was fixed before its experiment started. Evaluation uses patient-level stratified 5-fold cross-validation, which closes data leakage. The classes are imbalanced, so the loss is inverse-frequency-weighted focal loss. The primary metric is weighted F1, then AUC and quadratic kappa; on external corpora, the generalisation ratio G; for attention, ALO.

## 21. Experiment 1: contribution of preprocessing across two architectures

*40 с · 70 слов*

In the first experiment the integrated configuration is higher on both architectures: on ResNet-50 F1 rose from 0.752 to 0.817, on EfficientNet-B3 from 0.754 to 0.819 — 6.5 percentage points. AUC rose by 0.03 and kappa by 0.11. All three pre-fixed conditions hold on both architectures, significant after Holm correction, with no interaction. The largest gain is in the minority classes.

## 22. Experiment 2: ablation of pipeline stages

*40 с · 89 слов*

The second experiment adds the stages in turn under a single initialisation. F1 rises from 0.754 to 0.819 monotonically in each of the five folds — the first experiment's gain is fully reproduced by preprocessing. Every step exceeds noise; illumination correction and CLAHE contribute most, 41 percent together. Their parameters have an interior optimum: clip factor 2.5, threshold 0.03, correction scale 0.07. The main configurations were trained at 2.0 and 0.01 — off the optimum, so the result is not inflated by tuning.

## 23. Domain distance in feature space

*35 с · 80 слов*

The claim that preprocessing improves robustness across domains is usually backed only by external accuracy. We measured the mechanism itself: the distance from the training corpus to six external ones at the penultimate layer falls on all six by 0.070–0.093, with intervals excluding zero, and by 34–38 percent at pixel level. The transform never saw the target corpora. Caveat: the size of the reduction does not predict the size of the gain — only the direction holds.

## 24. Experiment 3: transfer to another dataset

*30 с · 77 слов*

In the third experiment the model trained on EyePACS was tested on APTOS 2019 without any retraining. Weighted F1 of the integrated configuration is 0.735, of the baseline 0.647 — a difference of 0.089 whose interval excludes zero. The generalisation ratio is 0.898 against 0.858. Both configurations pass the 0.85 threshold, so the evidence lies not in the threshold but in the comparison: on an unseen corpus the integrated configuration is higher.

## 25. Experiment 4: interpretability (ALO, Grad-CAM)

*35 с · 64 слов*

The fourth experiment compares model attention with the expert masks of IDRiD. ALO is the fraction of a lesion covered by attention; it is asymmetric because lesion coverage is what matters clinically. In the integrated configuration ALO is higher for all four types by 0.099–0.129, p below 0.015, regardless of threshold. This is alignment of attention with annotation, not localisation.

## 26. Experiment 5: accuracy on external clinical data

*25 с · 53 слов*

The fifth experiment tests absolute performance on two external clinical corpora: on IDRiD F1 exceeds the baseline by 0.069, on Messidor-2 by 0.054, both above the minimal clinically important difference of 0.05. This is not robustness to degradation — relative to their own domain both configurations fall back almost equally.

## 27. Experiment 6: robustness to camera change

*25 с · 46 слов*

The sixth experiment covers five camera groups. The integrated configuration is higher in all five, with the largest gain in the weakest groups. The between-group spread narrows 2.4-fold in F1 and 3.1-fold in AUC: the model depends less on the camera.

## 28. Experiment 7: small-data training

*30 с · 56 слов*

The seventh experiment is the data-scarce regime: training on 516 IDRiD images, testing on the sixty-image Kazakhstan clinical set, with a pre-registered protocol. Here too F1 rose from 0.513 to 0.593 and kappa by 0.12. The gain is comparable to full data — the advantage is not specific to small data.

## 29. Screening system

*35 с · 80 слов*

The fourth result is the screening system. The inference service and the browser client use the same pipeline code as the experiments, so the clinician works with exactly the model we evaluated. The client shows every preprocessing stage, the grade and the attention map, and the clinician confirms or corrects the decision. The system runs on a consumer graphics processor, and the fourth channel adds less than one per cent of computation. A field clinical trial is the next step.

## 30. Conclusion

*60 с · 117 слов*

The conclusion follows the objectives. First: the problem was formulated. Second: the eight-stage pipeline was formalised and adapted to two architectures, with the protocol fixed before the experiments. Third: the integrated configuration is 6.5 percentage points higher in F1 in-domain, the gain decomposes by stage, the distance to six corpora shrinks, and on every external, device and clinical corpus and on small data the configuration is higher; attention agrees better with annotation. Fourth: the screening system was built. The main finding is consistency, and it supports treating preprocessing as a model component. Theoretically, this changes the full description of a model: preprocessing enters its specification, and attention agreement and domain distance become measurable quantities.

## 31. Publications

*20 с · 50 слов*

The results are published in five papers: one article in a third-quartile Scopus journal, three articles in journals recommended by the authorised body, and one paper at an international Scopus-indexed conference. The work was presented at the international workshop on the digital society in Istanbul in October 2025.

## 32. Copyright certificate

*10 с · 17 слов*

A certificate of entry into the state register of copyright was obtained for the developed software package.

## 33. Closing title

*5 с · 16 слов*

This concludes my presentation. Thank you for your attention! I am ready to answer your questions.

---

# Резерв — только на вопрос, в бюджет не входит

## R1. Limitations of the study

*61 слов*

Limitations: in the minority classes, especially the mild stage, F1 stays low; the model sometimes attends where there is no lesion, so an ophthalmologist checks the decision. External evaluations rely on single-fold models, the Kazakhstan corpus is closed, and the mask channel's isolated contribution was not measured. The results do not prove clinical validity and are not a certification.
