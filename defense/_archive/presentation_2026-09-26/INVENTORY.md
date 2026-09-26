# Опись архивной презентации

> Перенесена из `defense\presentation\` 2026-09-26: презентация пересобирается заново на трёх языках
> (новая — `defense\presentation\`). Опись составлена agy (gemini-3.1-pro-high); выборочная проверка Claude:
> надёжны — список файлов (51 = 51), существование картинок, неиспользуемые картинки.
> **Ненадёжны:** «Языки текста» (у всех en/kk/ru, фактически текст казахский с английскими терминами),
> «Годится для новой» (у всех одно и то же), «Ключевые числа» (выхвачены отдельные цифры без смысла),
> счёт терминов в п. 5 (G — 224 «вхождения» = подсчёт буквы). Числа брать только из `dissertation\results\`.

## 1. Таблица слайдов

| Файл | Рубрика | Языки текста | Есть речь? | Картинки | Ключевые числа | Годится для новой? |
|---|---|---|---|---|---|---|
| 01_TITLE.md | Title | en/kk/ru | да, ~21 слов | LOGO.png (существует), AVATAR.png (существует) | 2026 | частично (требует перевода) |
| 02_RELEVANCE.md | Relevance | en/kk/ru | да, ~96 слов | нет | 8, 5, 6 | частично (требует перевода) |
| 03_AIM_OBJECTIVES.md | Aim_objectives | en/kk/ru | да, ~104 слов | нет | 6, 7, 8, 0.02, 0, 0.85 | частично (требует перевода) |
| 04_OBJECT_SUBJECT.md | Object_subject | en/kk/ru | да, ~63 слов | нет | 0 | частично (требует перевода) |
| 05_LITERATURE_REVIEW.md | Literature_review | en/kk/ru | да, ~77 слов | нет | 50 | частично (требует перевода) |
| 05a_PARADIGMATIC_POSITIONING.md | Paradigmatic_positioning | en/kk/ru | да, ~138 слов | нет | 2016, 2016, 2017, 2020, 2017, 2019 | частично (требует перевода) |
| 06_SECTION_METHODOLOGY.md | Section_methodology | en/kk/ru | да, ~9 слов | нет | нет | частично (требует перевода) |
| 07_SYSTEM_ARCHITECTURE.md | System_architecture | en/kk/ru | да, ~45 слов | architecture/06_system/02_system_architecture.png (существует) | 8, 5, 6, 512, 512, 50 | частично (требует перевода) |
| 08_CNN_ARCHITECTURE.md | Cnn_architecture | en/kk/ru | да, ~132 слов | architecture/07_cnn/cnn_architecture.png (существует) | 50, 512, 512, 50, 512, 512 | частично (требует перевода) |
| 09_ARCHITECTURE_COMPARISON.md | Architecture_comparison | en/kk/ru | да, ~187 слов | architecture/08_comparison/01_abstract_model_architecture.png (существует) | 50, 50, 50, 8, 50, 8 | частично (требует перевода) |
| 10_TRAINING_PARAMS.md | Training_params | en/kk/ru | да, ~89 слов | architecture/09_training/focal_loss.png (существует), architecture/09_training/cv_5fold.png (существует) | 5, 5, 5, 80, 20 | частично (требует перевода) |
| 11_SECTION_DATA.md | Section_data | en/kk/ru | да, ~20 слов | нет | нет | частично (требует перевода) |
| 12_DATASETS.md | Datasets | en/kk/ru | да, ~126 слов | datasets/27_overview/12_dataset_class_distribution.svg (существует), datasets/27_overview/cross_dataset_comparison.svg (существует) | 8, 74, 5, 5, 8, 5 | частично (требует перевода) |
| 13_DATASETS_EXPERIMENTS.md | Datasets_experiments | en/kk/ru | да, ~136 слов | datasets/28_experiments/datasets_matrix.png (существует) | 7, 8, 6, 0.85, 5, 5 | частично (требует перевода) |
| 14_CAMERAS_DISTRIBUTION.md | Cameras_distribution | en/kk/ru | да, ~65 слов | datasets/29_cameras/cameras_alignment.png (существует) | 36, 53, 31, 14, 36, 36 | частично (требует перевода) |
| 15_PREPROCESS_INPUT.md | Preprocess_input | en/kk/ru | да, ~56 слов | preprocessing/10_input/04_preprocessing_pipeline_vertical.png (существует), preprocessing/10_input/right.png (существует), preprocessing/10_input/left.png (существует) | 8, 8 | частично (требует перевода) |
| 16_PREPROCESS_CANONICAL_FLIP.md | Preprocess_canonical_flip | en/kk/ru | да, ~39 слов | preprocessing/11_canonical_flip/stage0_canonical_flip.png (существует), preprocessing/11_canonical_flip/left.png (существует), preprocessing/11_canonical_flip/right.png (существует) | 0 | частично (требует перевода) |
| 17_PREPROCESS_FOVEA_OD_ROTATION.md | Preprocess_fovea_od_rotation | en/kk/ru | да, ~32 слов | preprocessing/12_od_fovea_rotation/stage1_od_fovea_rotation.png (существует), preprocessing/12_od_fovea_rotation/left.png (существует), preprocessing/12_od_fovea_rotation/left_rotated.png (существует) | 0, 0 | частично (требует перевода) |
| 18_PREPROCESS_CROP_RESIZE.md | Preprocess_crop_resize | en/kk/ru | да, ~34 слов | preprocessing/13_crop_resize/stage2_fov_crop_resize.png (существует), preprocessing/13_crop_resize/left.png (существует) | 512, 512 | частично (требует перевода) |
| 19_PREPROCESS_FOV_MASK.md | Preprocess_fov_mask | en/kk/ru | да, ~33 слов | preprocessing/14_fov_mask/stage3_fov_mask.png (существует), preprocessing/14_fov_mask/left.png (существует) | нет | частично (требует перевода) |
| 20_PREPROCESS_FLATFIELD.md | Preprocess_flatfield | en/kk/ru | да, ~35 слов | preprocessing/15_flatfield/stage4_flatfield.png (существует), preprocessing/15_flatfield/left.png (существует) | 0.07 | частично (требует перевода) |
| 21_PREPROCESS_CLAHE_VESSEL.md | Preprocess_clahe_vessel | en/kk/ru | да, ~38 слов | preprocessing/16_clahe_vessel/stage5_clahe.png (существует), preprocessing/16_clahe_vessel/left-density.png (существует), preprocessing/16_clahe_vessel/left-detection.png (существует) | 5 | частично (требует перевода) |
| 22_PREPROCESS_CLAHE_POLAR.md | Preprocess_clahe_polar | en/kk/ru | да, ~35 слов | preprocessing/17_clahe_polar/stage5_clahe.png (существует), preprocessing/17_clahe_polar/left-grid.png (существует), preprocessing/17_clahe_polar/left-adaptive.png (существует) | 5 | частично (требует перевода) |
| 23_PREPROCESS_CLAHE_SV2.md | Preprocess_clahe_sv2 | en/kk/ru | да, ~35 слов | preprocessing/18_clahe_sv2/stage5_clahe.png (существует), preprocessing/18_clahe_sv2/left.png (существует), preprocessing/18_clahe_sv2/left-interpolation.png (существует) | 5 | частично (требует перевода) |
| 24_PREPROCESS_AUG_ROTATION.md | Preprocess_aug_rotation | en/kk/ru | да, ~37 слов | preprocessing/19_aug_rotation/stage6_augmentation.png (существует), preprocessing/19_aug_rotation/left_contours.png (существует), preprocessing/19_aug_rotation/left_sectors_mono.png (существует), preprocessing/19_aug_rotation/left_peaks.png (существует), preprocessing/19_aug_rotation/left_distribution_step.png (существует), preprocessing/19_aug_rotation/distribution_adaptive.png (существует) | 6 | частично (требует перевода) |
| 25_PREPROCESS_AUG_TRANSLATION.md | Preprocess_aug_translation | en/kk/ru | да, ~27 слов | preprocessing/20_aug_translation/stage6_augmentation.png (существует), preprocessing/20_aug_translation/left_min.png (существует), preprocessing/20_aug_translation/left_max.png (существует), preprocessing/20_aug_translation/distribution.png (существует) | 6 | частично (требует перевода) |
| 26_PREPROCESS_AUG_SCALE.md | Preprocess_aug_scale | en/kk/ru | да, ~22 слов | preprocessing/21_aug_scale/stage6_augmentation.png (существует), preprocessing/21_aug_scale/left_min.png (существует), preprocessing/21_aug_scale/left_max.png (существует), preprocessing/21_aug_scale/distribution.png (существует) | 6 | частично (требует перевода) |
| 27_PREPROCESS_AUG_SHEAR.md | Preprocess_aug_shear | en/kk/ru | да, ~20 слов | preprocessing/22_aug_shear/stage6_augmentation.png (существует), preprocessing/22_aug_shear/left_min.png (существует), preprocessing/22_aug_shear/left_max.png (существует), preprocessing/22_aug_shear/distribution.png (существует) | 6 | частично (требует перевода) |
| 28_PREPROCESS_AUG_COLORJITTER.md | Preprocess_aug_colorjitter | en/kk/ru | да, ~68 слов | preprocessing/23_aug_pca_color/stage6_augmentation.png (существует), preprocessing/23_aug_pca_color/left_min.png (существует), preprocessing/23_aug_pca_color/left_max.png (существует), preprocessing/23_aug_pca_color/distribution.png (существует) | 6, 0.9, 1.1, 0.02, 0.02, 50 | частично (требует перевода) |
| 29_PREPROCESS_AUG_ACQUISITION.md | Preprocess_aug_acquisition | en/kk/ru | да, ~66 слов | preprocessing/24_aug_brightness_contrast/stage6_augmentation.png (существует), preprocessing/24_aug_brightness_contrast/left_min.png (существует), preprocessing/24_aug_brightness_contrast/left_max.png (существует), preprocessing/24_aug_brightness_contrast/distribution.png (существует) | 6, 6, 15, 70, 100, 20 | частично (требует перевода) |
| 30_PREPROCESS_NORMALIZATION.md | Preprocess_normalization | en/kk/ru | да, ~35 слов | preprocessing/25_normalization/stage7_normalize.png (существует), preprocessing/25_normalization/right.png (существует), preprocessing/25_normalization/left.png (существует) | 7 | частично (требует перевода) |
| 31_SECTION_RESULTS.md | Section_results | en/kk/ru | да, ~17 слов | нет | нет | частично (требует перевода) |
| 32_METRICS.md | Metrics | en/kk/ru | да, ~57 слов | metrics/def_f1_kappa.png (существует), metrics/def_auc.png (существует), metrics/def_g.png (существует), metrics/def_alo.png (существует) | нет | частично (требует перевода) |
| 33_RESULTS_EXP1.md | Results_exp1 | en/kk/ru | да, ~63 слов | results/exp1/01_exp1_factorial_f1.png (существует), results/exp1/03_exp1_delta.png (существует), results/exp1/18_per_class_f1.png (существует) | нет | частично (требует перевода) |
| 34_RESULTS_EXP2.md | Results_exp2 | en/kk/ru | да, ~57 слов | results/exp2/04_exp2_ablation.png (существует), results/exp2/05_exp2_per_stage.png (существует), results/exp2/13_exp2_clahe_sensitivity.png (существует) | нет | частично (требует перевода) |
| 35_RESULTS_EXP3.md | Results_exp3 | en/kk/ru | да, ~50 слов | results/exp3/29_exp3_aptos_transfer.png (существует), results/exp3/09_exp5_G_ratio.png (существует) | 2019, 0.85, 2019 | частично (требует перевода) |
| 36_RESULTS_EXP4.md | Results_exp4 | en/kk/ru | да, ~64 слов | results/exp4/06_exp4_alo.png (существует), results/exp4/27_gradcam_overlay.png (существует), results/exp4/28_attention_consistency.png (существует) | 5 | частично (требует перевода) |
| 37_RESULTS_EXP5.md | Results_exp5 | en/kk/ru | да, ~41 слов | results/exp5/08_exp5_generalization.png (существует) | 5, 7, 5 | частично (требует перевода) |
| 38_RESULTS_EXP6.md | Results_exp6 | en/kk/ru | да, ~48 слов | results/exp6/10_exp6_device_shift.png (существует) | 6, 6, 6 | частично (требует перевода) |
| 39_RESULTS_EXP7.md | Results_exp7 | en/kk/ru | да, ~49 слов | results/exp7/30_exp7_small_data.png (существует) | 7, 7, 5 | частично (требует перевода) |
| 40_SECTION_DISCUSSION.md | Section_discussion | en/kk/ru | да, ~12 слов | нет | нет | частично (требует перевода) |
| 41_DISCUSSION_SYNTHESIS.md | Discussion_synthesis | en/kk/ru | да, ~101 слов | discussion/synthesis/11_summary_radar.png (существует), discussion/synthesis/16_image_quality.png (существует), discussion/synthesis/21_statistical_tests.png (существует) | 6 | частично (требует перевода) |
| 42_DISCUSSION_SOTA.md | Discussion_sota | en/kk/ru | да, ~72 слов | discussion/sota/14_clinical_metrics.png (существует), discussion/sota/15_calibration.png (существует), discussion/sota/17_computational.png (существует) | 80 | частично (требует перевода) |
| 43_DISCUSSION_LIMITATIONS.md | Discussion_limitations | en/kk/ru | да, ~65 слов | discussion/limitations/18_per_class_f1.png (существует), discussion/limitations/dr01_gradcam_right.png (существует) | нет | частично (требует перевода) |
| 44_NOVELTY.md | Novelty | en/kk/ru | да, ~67 слов | нет | 2016, 8, 8, 6, 46, 0.85 | частично (требует перевода) |
| 45_THEORETICAL_SIGNIFICANCE.md | Theoretical_significance | en/kk/ru | да, ~70 слов | нет | 0.85, 8, 0.85 | частично (требует перевода) |
| 46_PRACTICAL_SIGNIFICANCE.md | Practical_significance | en/kk/ru | да, ~66 слов | TELEMED.png (существует) | 3060, 19, 27, 5, 42 | частично (требует перевода) |
| 47_CONCLUSIONS.md | Conclusions | en/kk/ru | да, ~66 слов | нет | 8, 5.2, 5, 0.001, 0.85, 46 | частично (требует перевода) |
| 48_PUBLICATIONS.md | Publications | en/kk/ru | да, ~20 слов | publications/PUBLICATIONS.png (существует), publications/SCOPUS.png (существует), publications/SCOPUS_CONF.png (существует), publications/KBTU.png (существует), publications/AKADEMY.png (существует), publications/KAZTBU.png (существует) | 5, 2025, 9, 136, 79, 88 | частично (требует перевода) |
| 49_FINAL.md | Final | en/kk/ru | да, ~6 слов | LOGO.png (существует) | 2026 | частично (требует перевода) |
| slide_plan.md | Plan | en/kk/ru | нет | нет | 47, 01, 02, 03, 04, 21 | частично (требует перевода) |

## 2. Неиспользуемые картинки

- datasets/27_overview/12_dataset_class_distribution.png
- datasets/27_overview/cross_dataset_comparison.png

## 3. Скрипты (scripts\*.py)

- **generate_metric_definitions.py**: входные пути: Landis & Koch (1977):\n.
- **generate_kz_class_distribution.py**: входные пути: assets" / "datasets" / "27_overview" / "12_dataset_class_distribution.svg.
- **fix_slides_27_28.py**: входные пути: 28_experiments" / "datasets_matrix.png, 27_overview" / "cross_dataset_comparison.svg.
- **generate_camera_alignment.py**: входные пути: assets" / "datasets" / "29_cameras" / "cameras_alignment.png.
- **generate_empty_slide_images.py**: входные пути: preprocessing" / "22_aug_shear" / "left_min.png, left_min.png, preprocessing" / "20_aug_translation" / "distribution.png, architecture" / "09_training" / "cv_5fold.png, left_max.png, architecture" / "09_training" / "focal_loss.png, architecture" / "07_cnn" / "cnn_architecture.png.
- **split_preprocessing_svg.py**: входные пути: E:/dissertation-project/defense/scripts/_tmp_preproc, C:/Program Files/Google/Chrome/Application/chrome.exe, E:/dissertation-project/defense/assets/preprocessing/stages, E:/dissertation-project/demo/public/diagrams/03_preprocessing_stages_detailed.svg.
- **render_stage6_card.py**: входные пути: demo/web/public/diagrams/03_preprocessing_stages_detailed.svg, card.svg").write_text(standalone, encoding="utf-8, C:/Program Files/Google/Chrome/Application/chrome.exe, defense/presentation/assets/preprocessing/*/stage6_augmentation.png, card.png.

## 4. Парадигматическая речь

Файл `paradigmatic_speech.md`: содержит парадигматическую речь. Язык: en/kk/ru.

## 5. Термины

- **G (generalization ratio)**: 224 вхождений (файлы: 02_RELEVANCE.md, 46_PRACTICAL_SIGNIFICANCE.md, 45_THEORETICAL_SIGNIFICANCE.md, 07_SYSTEM_ARCHITECTURE.md, 10_TRAINING_PARAMS.md, 12_DATASETS.md, 13_DATASETS_EXPERIMENTS.md, 14_CAMERAS_DISTRIBUTION.md, 17_PREPROCESS_FOVEA_OD_ROTATION.md, 18_PREPROCESS_CROP_RESIZE.md, 19_PREPROCESS_FOV_MASK.md, 20_PREPROCESS_FLATFIELD.md, 21_PREPROCESS_CLAHE_VESSEL.md, 22_PREPROCESS_CLAHE_POLAR.md, 24_PREPROCESS_AUG_ROTATION.md, 25_PREPROCESS_AUG_TRANSLATION.md, 26_PREPROCESS_AUG_SCALE.md, 27_PREPROCESS_AUG_SHEAR.md, 30_PREPROCESS_NORMALIZATION.md, 16_PREPROCESS_CANONICAL_FLIP.md, 06_SECTION_METHODOLOGY.md, 32_METRICS.md, 33_RESULTS_EXP1.md, 35_RESULTS_EXP3.md, 36_RESULTS_EXP4.md, 37_RESULTS_EXP5.md, 38_RESULTS_EXP6.md, 39_RESULTS_EXP7.md, 41_DISCUSSION_SYNTHESIS.md, 42_DISCUSSION_SOTA.md, 43_DISCUSSION_LIMITATIONS.md, 23_PREPROCESS_CLAHE_SV2.md, 03_AIM_OBJECTIVES.md, 05_LITERATURE_REVIEW.md, 05a_PARADIGMATIC_POSITIONING.md, 08_CNN_ARCHITECTURE.md, 09_ARCHITECTURE_COMPARISON.md, 15_PREPROCESS_INPUT.md, 34_RESULTS_EXP2.md, 44_NOVELTY.md, 47_CONCLUSIONS.md, 28_PREPROCESS_AUG_COLORJITTER.md, 29_PREPROCESS_AUG_ACQUISITION.md, 01_TITLE.md, 49_FINAL.md, slide_plan.md)
- **Препроцессинг (preprocessing)**: 51 вхождений (файлы: 45_THEORETICAL_SIGNIFICANCE.md, 07_SYSTEM_ARCHITECTURE.md, 13_DATASETS_EXPERIMENTS.md, 30_PREPROCESS_NORMALIZATION.md, 33_RESULTS_EXP1.md, 35_RESULTS_EXP3.md, 41_DISCUSSION_SYNTHESIS.md, 03_AIM_OBJECTIVES.md, 05_LITERATURE_REVIEW.md, 05a_PARADIGMATIC_POSITIONING.md, 08_CNN_ARCHITECTURE.md, 09_ARCHITECTURE_COMPARISON.md, 15_PREPROCESS_INPUT.md, 44_NOVELTY.md, 47_CONCLUSIONS.md, slide_plan.md)
- **Pipeline**: 46 вхождений (файлы: 46_PRACTICAL_SIGNIFICANCE.md, 30_PREPROCESS_NORMALIZATION.md, 33_RESULTS_EXP1.md, 36_RESULTS_EXP4.md, 37_RESULTS_EXP5.md, 38_RESULTS_EXP6.md, 41_DISCUSSION_SYNTHESIS.md, 03_AIM_OBJECTIVES.md, 05_LITERATURE_REVIEW.md, 05a_PARADIGMATIC_POSITIONING.md, 08_CNN_ARCHITECTURE.md, 09_ARCHITECTURE_COMPARISON.md, 15_PREPROCESS_INPUT.md, 34_RESULTS_EXP2.md, 44_NOVELTY.md, 47_CONCLUSIONS.md, slide_plan.md)
- **ALO (Attention–Lesion Overlap)**: 29 вхождений (файлы: 46_PRACTICAL_SIGNIFICANCE.md, 45_THEORETICAL_SIGNIFICANCE.md, 07_SYSTEM_ARCHITECTURE.md, 13_DATASETS_EXPERIMENTS.md, 32_METRICS.md, 36_RESULTS_EXP4.md, 03_AIM_OBJECTIVES.md, 44_NOVELTY.md, 47_CONCLUSIONS.md, slide_plan.md)
- **Grad-CAM (Gradient-weighted Class Activation Mapping)**: 22 вхождений (файлы: 46_PRACTICAL_SIGNIFICANCE.md, 45_THEORETICAL_SIGNIFICANCE.md, 07_SYSTEM_ARCHITECTURE.md, 12_DATASETS.md, 32_METRICS.md, 36_RESULTS_EXP4.md, 43_DISCUSSION_LIMITATIONS.md, 03_AIM_OBJECTIVES.md, 05_LITERATURE_REVIEW.md, 09_ARCHITECTURE_COMPARISON.md, 44_NOVELTY.md, slide_plan.md)
- **Cross-dataset**: 15 вхождений (файлы: 45_THEORETICAL_SIGNIFICANCE.md, 12_DATASETS.md, 13_DATASETS_EXPERIMENTS.md, 35_RESULTS_EXP3.md, 37_RESULTS_EXP5.md, 03_AIM_OBJECTIVES.md, 05_LITERATURE_REVIEW.md, 44_NOVELTY.md, slide_plan.md)
- **Факторлық дизайн (factorial design)**: 10 вхождений (файлы: 33_RESULTS_EXP1.md, 03_AIM_OBJECTIVES.md, 05_LITERATURE_REVIEW.md, 09_ARCHITECTURE_COMPARISON.md, 44_NOVELTY.md)
- **FOV mask (Field of View mask)**: 9 вхождений (файлы: 19_PREPROCESS_FOV_MASK.md, 08_CNN_ARCHITECTURE.md, 09_ARCHITECTURE_COMPARISON.md, 44_NOVELTY.md, slide_plan.md)
- **Backbone**: 6 вхождений (файлы: 03_AIM_OBJECTIVES.md, 08_CNN_ARCHITECTURE.md, 09_ARCHITECTURE_COMPARISON.md)
- **Fundus**: 4 вхождений (файлы: 04_OBJECT_SUBJECT.md, 07_SYSTEM_ARCHITECTURE.md)
- **GAP (Global Average Pooling)**: 4 вхождений (файлы: 32_METRICS.md, slide_plan.md)
- **Domain shift**: 3 вхождений (файлы: 03_AIM_OBJECTIVES.md, 05_LITERATURE_REVIEW.md, 44_NOVELTY.md)
- **Explainability**: 2 вхождений (файлы: 03_AIM_OBJECTIVES.md, 05_LITERATURE_REVIEW.md)
