> English translation by the local model (Qwen). Source: `translation/work/eval/v3/council-valid/src/olzhayev-kz-en.kz.md`. Terminology: `translation/termbase.tsv`.

## PART 1: SECTION TEXT

In recent days, the automated detection of road defects using computer vision is considered one of the relevant tasks, and we observe an exponential growth of interest in this field. Analyzing the specialized literature, we can clearly see this growth in scientific activity: if there were only about 50 relevant publications in 2015, by 2025 their number exceeded 900 works. Such dynamics are related to three factors: the widespread introduction of high-resolution sensors, the formation of large-scale representative datasets, and the availability of high-performance computing power required for training multi-layer neural networks.

Analysis of the visual features and characteristics of pavement images. • A deep learning model for classifying and segmenting road damage

Scientific propositions put forward for defense: • Simultaneous detection of pavement damage in real-time mode,

Main results of the research: • Using computer vision and deep learning methods, real-time

enabled improving the stability of recognizing complex damage; • Efficient spatial dependencies between objects of different scales

demonstrated the possibility of operation; • Maintaining the high performance of the system, the accuracy of defect detection

dataset (dataset) was developed and labeled. • The impact of seasonal conditions and the variability of dynamic lighting

a comprehensive system of automated monitoring was developed.

The validity of the obtained results is ensured by the application of modern methods of computer vision and deep learning, the use of convolutional neural networks (CNN) and transformer attention mechanisms, as well as by conducting computational experiments on a labeled video dataset of road pavement collected in actual usage conditions. The reliability of the results is confirmed by a comparative analysis with existing architectures and road defect detection algorithms, the use of generally accepted quality assessment metrics (mAP, IoU, Precision, Recall, F1-Score), the stable convergence of the model during the training process, and the reproducibility of the results obtained under various lighting conditions, weather factors, and background noise.

The main results of the work were presented and discussed at the seminars of the Department of "Mathematical and Computer Modeling" of JSC "IITU" (2024–2026), Asia Metropolitan University, Malaysia (2026). Four publications on the dissertation topic were made, including 2 publications in rated scientific journals indexed in the Scopus database; 2 publications in the materials of international conferences; 1 author's certificate was obtained.

In all the mentioned publications, the applicant holds the leading role, and conclusions are drawn based on the main results of the research, the analyses performed by the author, the models, the programs, and the results obtained from the applicant's work and research.

The second chapter provides a comprehensive literature review covering the classification of road defect types and the analysis of the evolution of their detection methods. The historical transition from classical computer vision algorithms to modern deep learning architectures (convolutional networks, YOLO detectors, visual transformers) is considered. Fundamental gaps in existing research, such as the complexity of processing continuous video streams due to temporal misalignment, the lack of imaging datasets, and the problem of adapting heavy models to peripheral computing, justify the algorithmic direction of the current work.

The third section describes the research materials and methods in detail. It presents the process of collecting, preprocessing, and accurately annotating a unique set of video data recorded in real-world usage scenarios. Particular attention is paid to the mathematical and structural design of the TCR-RoadNet innovative multi-task neural network architecture. The operation of the multi-scale convolutional backbone, the Context Refinement Module based on cross-scale transformer attention (TCR), and the three specialized Output arms is described in detail: the separate detection module, the classification refinement block, and the segmentation arm accounting for boundaries. The optimization strategy and multi-task loss functions (CIoU, Focal Loss, and a combination of BCE+Dice) are additionally described.

The total length of the dissertation is 104 pages, including 28 illustrations, 8 tables, and a list of references drawn from 154 sources.
