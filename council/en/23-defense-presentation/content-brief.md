# Slide-by-slide Defense Presentation Draft

## Slide 1
**Section:** Title
**Title:** Information system for automatic detection of retinal diseases based on deep learning using optical coherence tomography images
**Slide text:**
- **Candidate:** Yesmukhamedov Nurmaganbet Seitkaliuly
- **Supervisors:** Sapakova Saya Zamanbekovna, Prof. Dr. Syed Abdul Rahman Al-Haddad
- **Program:** 8D06102 — Computer and Software Engineering
- **Institution:** International Information Technology University
**Speech:** Dear Chairman, dear members of the dissertation council! Let me present to your attention the dissertation work on the topic "Information system for automatic detection of retinal diseases based on deep learning using optical coherence tomography images".
**Seconds:** 30
**Visual:** None (Title Slide)
**SOURCE:** METADATA.toml

## Slide 2
**Section:** Relevance
**Title:** The Diabetic Retinopathy Screening Challenge
**Slide text:**
- DR is a leading cause of preventable blindness among working-age adults.
- Early stages are asymptomatic (microaneurysms, small hemorrhages).
- Screening is fundamentally a volume problem.
- Manual grading is limited and geographically concentrated.
**Speech:** Diabetic retinopathy is a leading cause of preventable blindness. Its asymptomatic early stages mean that detection relies on high-volume screening, which creates a bottleneck because manual grading requires specialized time that is scarce and geographically concentrated.
**Seconds:** 45
**Visual:** None
**SOURCE:** Введение_по_рубрикам.txt (Актуальность темы)

## Slide 3
**Section:** Relevance
**Title:** The Impact of Image Quality and Domain Shift
**Slide text:**
- Fundus images are not a stable substrate.
- Variability arises from different cameras, operators, and pupil dilation states.
- Domain shift degrades the performance of automated models.
- The methodological question is how to characterize preprocessing.
**Speech:** Furthermore, fundus images captured in screening environments vary significantly due to different cameras and operators. This introduces a domain shift that limits model robustness. The core methodological question becomes how to characterize the preprocessing needed to handle this variance.
**Seconds:** 45
**Visual:** None
**SOURCE:** Введение_по_рубрикам.txt (Актуальность темы)

## Slide 4
**Section:** Relevance
**Title:** The Methodological Gap
**Slide text:**
- Dominant paradigm (P1): Preprocessing is viewed as ancillary data preparation.
- Alternative paradigm (P2): Preprocessing is an integral component of the diagnostic model.
- Preprocessing defines the feature space available to the convolutional network.
**Speech:** Traditionally, preprocessing is treated as ancillary data preparation. Our research positions it as an integral component of the diagnostic model, as the transformations applied before the first convolution strictly define the feature space the network is forced to operate within.
**Seconds:** 45
**Visual:** None
**SOURCE:** Введение_по_рубрикам.txt (Актуальность темы)

## Slide 5
**Section:** Goal and Objectives
**Title:** Goal of the Research
**Slide text:**
- Develop and experimentally validate an integrated framework.
- Combine fundus image enhancement and CNN classification for 5-class DR diagnosis.
- Specify an 8-stage preprocessing pipeline as an integral model component.
- Compare with 11 equivalent baseline configurations trained without the pipeline.
**Speech:** The goal of this research is to develop and experimentally validate an integrated framework for 5-class DR diagnosis, specifying an 8-stage preprocessing pipeline as an integral model component, and to evaluate its impact compared to baseline configurations.
**Seconds:** 45
**Visual:** None
**SOURCE:** Введение_по_рубрикам.txt (Цель и задачи)

## Slide 6
**Section:** Goal and Objectives
**Title:** Objectives (1-2)
**Slide text:**
- 1. Analyze the domain, clinical grading, and formulate the scientific problem.
- 2. Specify the integrated framework methodology.
- Pipeline stages, classification architectures.
- Pre-training strategy, interpretability formalism, evaluation protocol.
**Speech:** To achieve this goal, we first analyze the problem domain and requirements of resource-constrained screening. Secondly, we specify the methodology, including the 8-stage pipeline, CNN architectures, interpretability metrics, and evaluation protocols.
**Seconds:** 45
**Visual:** None
**SOURCE:** Введение_по_рубрикам.txt (Цель и задачи)

## Slide 7
**Section:** Goal and Objectives
**Title:** Objectives (3-4)
**Slide text:**
- 3. Experimentally evaluate the framework in-domain and on 7 external corpora.
- Conduct statistical validation and establish limitations.
- 4. Construct a screening system architecture.
- Designed for resource-constrained environments without inference accelerators.
**Speech:** The third objective is the rigorous experimental evaluation of the framework across one in-domain and seven external datasets. The final objective is constructing a screening system architecture suitable for disconnected and resource-constrained environments.
**Seconds:** 45
**Visual:** None
**SOURCE:** Введение_по_рубрикам.txt (Цель и задачи)

## Slide 8
**Section:** Object and Subject
**Title:** Object and Subject of Research
**Slide text:**
- **Object:** Automated multi-stage DR diagnosis process via CNNs on color fundus photos.
- Evaluated from camera output to final grade.
- **Subject:** Methods of integrating preprocessing with classification.
- Properties: diagnostic performance, transferability, attention alignment.
**Speech:** The object of our study is the end-to-end automated multi-stage DR diagnosis process. The subject encompasses the methods of integrating preprocessing with CNN classification and the resulting properties such as transferability and attention alignment.
**Seconds:** 30
**Visual:** None
**SOURCE:** Введение_по_рубрикам.txt (Объект исследования, Предмет исследования)

## Slide 9
**Section:** Provisions / Novelty
**Title:** Scientific Novelty: Paradigm P2
**Slide text:**
- Main contribution is conceptual: repositioning preprocessing.
- Preprocessing is a formalizable and experimentally verifiable model component.
- The pipeline itself is the object of experiment, not just a descriptive form.
- Five engineering implementation elements integrated uniquely.
**Speech:** Moving to our novelty and defense provisions. The main conceptual contribution is repositioning preprocessing from a supplementary step to a formal model component, making it the direct object of experimental validation through an integrated paradigm.
**Seconds:** 45
**Visual:** None
**SOURCE:** Аннотация_по_рубрикам.txt (Научная новизна, пункт 1)

## Slide 10
**Section:** Provisions / Novelty
**Title:** Provisions on In-Domain Dominance
**Slide text:**
- Integrated configuration dominates baseline in 5-class DR classification.
- Validated on EyePACS for both ResNet-50 and EfficientNet-B3.
- Met predefined criteria across three metrics.
- Result withstands correction for multiple comparisons.
**Speech:** We assert that our integrated configuration significantly dominates the baseline on the EyePACS dataset. It met predefined superiority criteria across three different performance metrics for both ResNet-50 and EfficientNet-B3 architectures.
**Seconds:** 45
**Visual:** None
**SOURCE:** Аннотация_по_рубрикам.txt (Положения, выносимые на защиту, пункт 2)

## Slide 11
**Section:** Provisions / Novelty
**Title:** Provisions on Pipeline Stages
**Slide text:**
- Contributions of individual pipeline stages are separable and monotonic.
- Two photometric stages lead the performance gain.
- Parameters demonstrate internal optima (clip-factor 2.5, flat-field 0.07).
- Mask FOV channel successfully informs the CNN of valid pixel regions.
**Speech:** Furthermore, we demonstrate that the contributions of individual preprocessing stages are distinct and separable. The photometric stages provided the largest gains, and their key parameters demonstrated clear internal optima within the evaluated ranges.
**Seconds:** 45
**Visual:** None
**SOURCE:** Аннотация_по_рубрикам.txt (Положения, выносимые на защиту, пункты 3-4)

## Slide 12
**Section:** Provisions / Novelty
**Title:** Provisions on Transferability
**Slide text:**
- Reduces source-target distance in feature space on 6 external corpora.
- Uses only source domain statistics.
- Transfers to APTOS 2019 without retraining, exceeding G ≥ 0.85 (achieved 0.898).
- Attention aligns more closely with expert pixel-level annotations on IDRiD.
**Speech:** The integrated configuration measurably reduces domain shift distance in the feature space across six external corpora, ensuring the model effectively transfers to datasets like APTOS 2019 without retraining, while maintaining higher attention alignment with clinical annotations.
**Seconds:** 50
**Visual:** None
**SOURCE:** Аннотация_по_рубрикам.txt (Положения, выносимые на защиту, пункты 5-7)

## Slide 13
**Section:** Architecture / Methods
**Title:** Integrated 8-Stage Pipeline: Geometric Stages
**Slide text:**
- Stage 0: Canonical flip (left to right eye).
- Stage 1: OD-fovea rotation normalization via frozen landmark detector.
- Stage 2: FOV crop + isotropic resize to 512x512.
- Stage 3: FOV mask generation, passed as 4th input channel.
**Speech:** The proposed 8-stage preprocessing pipeline begins with geometric normalization. We align images using a canonical flip and rotation based on the optic disc and fovea, then perform isotropic resizing while explicitly passing the field-of-view mask as a 4th channel.
**Seconds:** 50
**Visual:** Figure 2.1 — "Сурет 2.1 – Сегіз кезеңді алдын ала өңдеу конвейері" (Eight-stage preprocessing pipeline) [source: 07_Глава_2.txt]
**SOURCE:** Аннотация_по_рубрикам.txt (Научная новизна, пункт 1)

## Slide 14
**Section:** Architecture / Methods
**Title:** Integrated 8-Stage Pipeline: Photometric Stages
**Slide text:**
- Stage 4: Adaptive flat-field correction (sigma scales with FOV diameter).
- Stage 5: Dual-constraint LAB CLAHE.
- Stage 6: Unified augmentation (affine, ColorJitter, noise, JPEG).
- Stage 7: Dataset-specific per-channel normalization.
**Speech:** The photometric stages include an adaptive flat-field correction scaled to the FOV diameter, followed by a dual-constraint CLAHE algorithm. Finally, unified augmentation and dataset-specific normalization prepare the four-channel tensor for classification.
**Seconds:** 50
**Visual:** Figure 2.1 — "Сурет 2.1 – Сегіз кезеңді алдын ала өңдеу конвейері" (Eight-stage preprocessing pipeline; same diagram, continued for photometric stages 4–7) [source: 07_Глава_2.txt]
**SOURCE:** Аннотация_по_рубрикам.txt (Научная новизна, пункт 1)

## Slide 15
**Section:** Architecture / Methods
**Title:** Evaluation Methodology
**Slide text:**
- Backbone Architectures: ResNet-50 and EfficientNet-B3.
- Loss function: Focal Loss to compensate for class imbalance.
- Experimental Design: Controlled 2x2 factorial comparison (Baseline vs Integrated).
- Validation: 5-fold patient-level stratified cross-validation.
**Speech:** Our methodology utilizes ResNet-50 and EfficientNet-B3 architectures with Focal Loss. The core evaluation is a controlled two-by-two factorial design, validated through a rigorous 5-fold patient-level stratified cross-validation to isolate the effect of the pipeline.
**Seconds:** 45
**Visual:** None
**SOURCE:** Аннотация_по_рубрикам.txt (Методология и методы исследования)

## Slide 16
**Section:** Experiments / Results
**Title:** Exp 1: Baseline vs Integrated (In-Domain)
**Slide text:**
- Factorial 2x2 design on EyePACS (35,126 images).
- Surpassed baseline by 6.54 and 6.55 percentage points in weighted F1.
- Surpassed baseline by 0.032 and 0.036 in ROC-AUC.
- Dominance confirmed for both architectures.
**Speech:** Moving to the results, Experiment 1 evaluated in-domain performance on EyePACS. The integrated configuration decisively surpassed the baseline by 6.54 and 6.55 percentage points in weighted F1, and improved ROC-AUC without interaction with the architecture choice.
**Seconds:** 55
**Visual:** Table 3.4 — "Кесте 3.4 – Ұяшық бойынша диагностикалық өлшемдер, EyePACS-те бес фолдты кросс-валидация, орташа ± стандартты ауытқу" (Per-cell diagnostic metrics, EyePACS 5-fold cross-validation, mean ± SD) [source: 08_Глава_3.txt]
**SOURCE:** Аннотация_по_рубрикам.txt (Основные результаты исследования, пункт 3)

## Slide 17
**Section:** Experiments / Results
**Title:** Exp 2: Cumulative Component Ablation
**Slide text:**
- Evaluated contributions of individual stages under unified initialization.
- Monotonically raised weighted F1 from 0.7538 to 0.8193.
- Each transition contributed beyond inter-fold variance.
- Confirmed internal optima for CLAHE (2.5) and flat-field (0.07).
**Speech:** Experiment 2 performed cumulative component ablation. The pipeline monotonically raised the weighted F1 score from 0.7538 to 0.8193. Each stage contributed to the gain, with the two photometric stages leading the improvements.
**Seconds:** 50
**Visual:** Table 3.7 — "Кесте 3.7 – EyePACS-тегі кумулятивті кезеңдік абляция, бес фолдты кросс-валидация, EfficientNet-B3, әр деңгейде бір инициализация" (Cumulative stage-wise ablation on EyePACS, 5-fold CV, EfficientNet-B3, one initialization per level) [source: 08_Глава_3.txt]
**SOURCE:** Аннотация_по_рубрикам.txt (Основные результаты исследования, пункт 4)

## Slide 18
**Section:** Experiments / Results
**Title:** Exp 3: Source-Target Distance Reduction
**Slide text:**
- Measured distance in penultimate layer feature space.
- Evaluated across 6 external corpora.
- Only source domain statistics utilized; no target adaptation.
- Distance reduced on every evaluated corpus.
**Speech:** In Experiment 3, we directly measured a reduction in feature space distance across 6 external corpora. This reduction was achieved using only source domain statistics, confirming it is an intrinsic property of the preprocessing pipeline.
**Seconds:** 45
**Visual:** Figure 3.4 — "Сурет 3.4 – Әр тармақтағы бастапқы корпустан қашықтық, алты нысаналы корпус" (Distance from source corpus per branch, six target corpora) [source: 08_Глава_3.txt]
**SOURCE:** Аннотация_по_рубрикам.txt (Основные результаты исследования, пункт 5)

## Slide 19
**Section:** Experiments / Results
**Title:** Exp 3: Cross-Dataset Transfer
**Slide text:**
- Evaluated transfer to APTOS 2019 without retraining.
- Exceeded predefined generalization ratio of 0.85.
- Achieved G ratio of 0.898 vs 0.858 for baseline.
- Outperformed baseline on every severity class.
**Speech:** The reduced distance enabled superior cross-dataset transfer. When applied to the APTOS 2019 dataset without any retraining, the integrated model achieved a generalization ratio of 0.898, outperforming the baseline across all severity classes.
**Seconds:** 45
**Visual:** Table 3.10 — "Кесте 3.10 – Нөлдік үйретумен сыртқы бағалау, EfficientNet-B3, домен ішіндегі тірек: базалық 0.7538, интеграцияланған 0.8193" (Zero-shot external evaluation, EfficientNet-B3, in-domain reference: baseline 0.7538, integrated 0.8193; the G=0.898 vs 0.858 ratios are derived from this table's APTOS 2019 row, discussed in body text immediately after) [source: 08_Глава_3.txt]
**SOURCE:** Аннотация_по_рубрикам.txt (Основные результаты исследования, пункт 6)

## Slide 20
**Section:** Experiments / Results
**Title:** Exp 4: Interpretability (Grad-CAM)
**Slide text:**
- Evaluated Attention-Lesion Overlap (ALO) on IDRiD pixel masks.
- Primary metric: ALO; Secondary metric: Intersection-over-Union (IoU).
- Improved alignment across all 4 annotated lesion types.
- Establishes model relies on valid pathological features.
**Speech:** Experiment 4 utilized our Attention-Lesion Overlap metric to analyze Grad-CAM outputs on IDRiD expert masks. The integrated configuration showed significantly closer alignment across all four lesion types, indicating the model relies on valid pathological features.
**Seconds:** 50
**Visual:** Figure 3.5 — "Сурет 3.5 – Сарапшы зақымдану аннотациясының үстіне қабатталған назар, кескін бойынша жұпталған" (Attention overlaid on expert lesion annotation, paired by image) [source: 08_Глава_3.txt]. Quantitative companion: Table 3.12 — "Кесте 3.12 – Назардың сарапшы зақымдану аннотациясымен беттесуі, IDRiD маска жиыны, EfficientNet-B4" (Attention overlap with expert lesion annotation, IDRiD mask set, EfficientNet-B4) [source: 08_Глава_3.txt]
**SOURCE:** Аннотация_по_рубрикам.txt (Основные результаты исследования, пункт 7)

## Slide 21
**Section:** Experiments / Results
**Title:** Exp 5 & 6: External Clinical Quality and Device Shift
**Slide text:**
- Exp 5: Absolute external clinical quality on Messidor-2.
- Difference exceeds minimum clinically significant magnitude.
- Exp 6: Evaluated across camera devices (DDR, ODIR-5K, RFMiD).
- Quality maintained across Canon, Topcon, Kowa, and Zeiss devices.
**Speech:** Experiment 5 confirmed higher absolute external clinical quality on the Messidor-2 corpus. Experiment 6 proved the model maintains performance and reduces variance across different camera manufacturers, including Canon, Topcon, Kowa, and Zeiss.
**Seconds:** 50
**Visual:** Table 3.11 — "Кесте 3.11 – Бес жабдықтық топ бойынша өнімділіктің топаралық шашырауы" (Cross-group performance dispersion across five equipment groups) [source: 08_Глава_3.txt] (no dedicated Figure exists for device shift in the dissertation; this is the closest matching item — a table, not a figure)
**SOURCE:** Аннотация_по_рубрикам.txt (Основные результаты исследования, пункт 8)

## Slide 22
**Section:** Experiments / Results
**Title:** Exp 7: Training under Data Scarcity
**Slide text:**
- Evaluated on Kazakhstan clinical set (60 images, 30 patients).
- 5-fold cross-validation in severe data deficit mode.
- Integrated configuration maintained its strong advantage.
- Proves efficiency of the pipeline with limited data.
**Speech:** In Experiment 7, the model was trained under a severe data deficit using a 60-image Kazakhstan clinical set. The integrated configuration retained a strong advantage over the baseline, proving the pipeline's efficiency even with limited data.
**Seconds:** 45
**Visual:** Table 3.13 — "Кесте 3.13 – IDRiD-те шағын іріктемеде оқыту, 60 кескіндік бөлек ұсталған клиникалық корпуста бағаланды. Бес фолд бойынша орташа ± стандартты ауытқу" (Small-sample training on IDRiD, evaluated on a held-out 60-image clinical corpus; mean ± SD over 5 folds) [source: 08_Глава_3.txt]
**SOURCE:** Аннотация_по_рубрикам.txt (Основные результаты исследования, пункт 8)

## Slide 23
**Section:** Implementation
**Title:** Practical Significance and Implementation
**Slide text:**
- Modular architecture of automated DR screening system designed.
- Operating demonstrator built and deployed.
- Evaluates full pipeline from start to finish.
- Architecture applicable to Kazakhstan health infrastructure.
**Speech:** In terms of practical significance, we designed a modular architecture for an automated screening system applicable to Kazakhstan's health infrastructure. We built an operating demonstrator that executes the full pipeline to validate this architectural design.
**Seconds:** 45
**Visual:** Figure 4.2 — "Сурет 4.2 – Оператор интерфейсі: кезең-бойынша көрініс және дәрежеленген нәтиже" (Operator interface: stage-by-stage view and graded result) [source: 09_Глава_4.txt]
**SOURCE:** Аннотация_по_рубрикам.txt (Основные результаты исследования, пункт 9)

## Slide 24
**Section:** Conclusion
**Title:** Conclusion
**Slide text:**
- Proposed formal 8-stage preprocessing pipeline as an integral model component.
- Demonstrated in-domain dominance over baseline configurations.
- Proved higher transferability and external clinical quality.
- Achieved closer alignment with expert pathological annotations.
**Speech:** In conclusion, the research successfully formalized an 8-stage preprocessing pipeline as an integral model component. This integration demonstrated clear in-domain dominance, higher transferability, and better alignment with expert annotations compared to standard baselines.
**Seconds:** 45
**Visual:** None
**SOURCE:** Аннотация_по_рубрикам.txt (Общая характеристика исследования, Научные результаты)

## Slide 25
**Section:** Publications
**Title:** Approbation and Publications
**Slide text:**
- 5 scientific publications total.
- 1 article in Scopus / Web of Science (Q3).
- 1 article in international conference proceedings (Scopus).
- 3 articles in CQASHE recommended journals.
**Speech:** The main results of the dissertation have been published in 5 scientific works, including one Q3 journal article in Scopus and Web of Science, one Scopus conference proceedings, and three articles in CQASHE recommended journals.
**Seconds:** 35
**Visual:** TODO(Cite publications screenshots) — kept: no captioned Figure/Table in the dissertation body matches "publications"; the 5-item list is structured data in METADATA.toml, `[publications]`/`[[publications.items]]` (lines ~704–798), not a numbered Figure/Table. Suggest building this slide's visual from that METADATA table directly, or using journal/conference cover-page screenshots.
**SOURCE:** METADATA.toml, content-brief.md (Блок 7 — справка о публикациях)

## Likely questions for our topic
1. **Methodology (Comparison):** What are the main advantages of your 8-stage pipeline compared to existing end-to-end models?
   - *Outline:* The pipeline reduces domain shift directly in the feature space without requiring target domain statistics, explicitly handles FOV geometry, and prevents the network from learning padding artifacts.
2. **Limitations and Conditions:** What are the operational conditions and limitations of your screening system?
   - *Outline:* The system is a design prototype without field clinical trials. The Kazakhstan clinical set is not for redistribution, and Grad-CAM evaluates attention overlap, not exact clinical localization.
3. **Data Cleaning and Volume:** How did you handle the variance across the ~35,126 images in EyePACS?
   - *Outline:* Variance in illumination and geometry was standardized through canonical flips, isotropic resizing, and adaptive flat-field correction, turning these variations into controlled inputs.
4. **Practical Significance / Implementation:** What is the practical meaning of the demonstrator if it is not a certified medical device?
   - *Outline:* The demonstrator proves the architectural feasibility of the system in resource-constrained environments and serves as a technical blueprint, leaving final diagnosis to the physician.
5. **Feature Combination:** You use both ResNet-50 and EfficientNet-B3. How do their representations differ?
   - *Outline:* The factorial design showed that the preprocessing benefit has no interaction with the architecture choice; it uniformly improves the feature space for both families.
6. **Quality Metrics:** Why do you emphasize the Attention-Lesion Overlap (ALO) over standard IoU?
   - *Outline:* ALO directly measures the proportion of the lesion covered by the model's attention, which is clinically more relevant for confirming that the model looks at the pathology, rather than expecting a segmentation-perfect boundary.
7. **Refining Details:** How do you account for differences in camera hardware?
   - *Outline:* The pipeline uses dataset-specific normalization based purely on the source domain statistics, maintaining performance across 4 distinct camera manufacturers (Canon, Topcon, Kowa, Zeiss) without retraining.
8. **Justification of the Problem:** Why is DR screening framed as a volume problem rather than just a diagnostic one?
   - *Outline:* Because early stages are asymptomatic, screening relies on massive planned imaging cohorts where most patients require no treatment, creating a severe bottleneck for limited specialist time.
9. **Implementation Setup:** Do the specific CLAHE and flat-field parameters generalize everywhere?
   - *Outline:* No, the parameters demonstrated internal optima on this specific pipeline and corpus. They are properties of the dataset and configuration, not universally transferable constants.
10. **Quantitative Data:** How significant is the 6.54 percentage point gain in weighted F1?
    - *Outline:* It is highly significant and exceeds the minimum clinically significant magnitude. It also survived Bonferroni/Holm corrections for multiple comparisons, proving robustness.
11. **Scope/Modality Mismatch (Approved Topic vs. Dissertation Content):** The approved topic names "optical coherence tomography images," but the dissertation only uses color fundus (retinal) photographs. How do you explain this?
    - *Outline (grounded strictly in METADATA.toml and the dissertation text; options marked "to confirm with supervisor" are not themselves justified by the sources and must not be presented as settled):*
      - The mismatch is real and already documented, not merely a wording slip to smooth over. METADATA.toml (`[dissertation]` section, comment above `title_en`/`title_ru`/`title_kz`, ~lines 207–215) states verbatim: "РАСХОЖДЕНИЕ ТЕМЫ С СОДЕРЖАНИЕМ ТОМА ... Приказ утверждает систему по изображениям ОПТИЧЕСКОЙ КОГЕРЕНТНОЙ ТОМОГРАФИИ; том написан и защищается по ЦВЕТНЫМ СНИМКАМ ГЛАЗНОГО ДНА (fundus): восемь корпусов — EyePACS, APTOS 2019, IDRiD, Messidor-2, DDR, ODIR-5K, RFMiD и клинический набор — ни одного ОКТ-снимка и ни одного эксперимента на ОКТ ... нужен либо приказ об изменении темы под содержание тома, либо решение совета. Вопрос будет задан на заседании."
      - Confirmed independently in the dissertation text itself: every corpus and every figure/table description uses "көз түбі" (fundus/eye-ground) imagery (e.g., 06_Глава_1.txt: "Сурет 1.1 – Бес дәреже бойынша көз түбінің репрезентативті кескіндері"; 05_Введение.txt: "...көз түбі кескінін жақсарту мен конволюциялық жіктеуді біріктіретін..."). The only occurrence of "optical coherence tomography" anywhere in the dissertation is a single bibliography entry for a third-party study ("...optical coherence tomography angiography...", 11_Список_литературы.txt) — it is a cited reference, not a description of the candidate's own data or method.
      - The approved topic itself comes from order № 7-D dated 27.08.2022 (METADATA.toml, `topic_approval_order`), and its OCT wording is carried unchanged into `title_en`/`title_ru`/`title_kz`.
      - Option A (to confirm with supervisor): obtain/register a topic-amendment order updating the modality wording from OCT to fundus photography ahead of, or as a condition of, the defense — this is the remedy path the METADATA comment itself names ("приказ об изменении темы под содержание тома").
      - Option B (to confirm with supervisor): ask the dissertation council for a formal resolution accepting the modality wording as a defect to be corrected administratively, without reopening the scientific content — again, the council decision path the METADATA comment names ("решение совета"), not something the sources pre-judge.
      - What must NOT be said: there is no statement anywhere in the dissertation or METADATA.toml that OCT and fundus photography are interchangeable or that the topic wording is merely stylistic; do not improvise that equivalence at the podium. The honest answer is that the topic wording is inaccurate for the modality actually used, the discrepancy is already flagged for the council, and it is being resolved through the order/decision path above.
