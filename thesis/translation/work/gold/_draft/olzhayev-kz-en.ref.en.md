Automated road defect detection using computer vision is currently considered a hot topic, and interest in this field is growing exponentially. An analysis of relevant literature clearly demonstrates this surge in scientific activity: while in 2015 there were only about 50 relevant publications, by 2025 their number exceeded 900. This growth is driven by three factors: the widespread adoption of high-resolution sensors, the development of large-scale representative datasets, and the availability of high-performance computing power necessary for training multilayer neural networks.

to various shooting conditions. • integrate the trained model into an application for automatic road condition monitoring,

detection, classification, and segmentation of road surface damage in real time. • a developed contextual feature refinement module based on cross-scale transformer

robustness to changes in illumination, background noise, and weather conditions.

and robustness of complex damage recognition. • a contextual feature refinement module based on a transformer attention mechanism was

including longitudinal and transverse cracks, mesh damage, and potholes, recorded in real-

real-world transport infrastructure operating conditions was developed and labeled. • additional visual features, such as the influence of seasonal conditions and dynamic lighting

of processing continuous video streams in hard real-time and providing analytical reporting

The reliability of the obtained results is ensured using modern computer vision and deep learning methods, the application of convolutional neural networks (CNNs) and transformer attention mechanisms, as well as computational experiments on a labeled dataset of road surface video collected under real-world operating conditions. The reliability of the results is confirmed by a comparative analysis with existing architectures and algorithms for road defect detection, the use of generally accepted quality assessment metrics (mAP, IoU, Precision, Recall, F1-score), stable model convergence during training, and the reproducibility of the obtained results under various lighting conditions, weather factors, and background noise.

The main results of the work were presented and discussed at seminars of the Department of Mathematical and Computer Modeling of JSC IITU (2024–2026) and Asia Metropolitan University, Malaysia (2026). Four publications on the topic of the dissertation have been published, including two in top-ranked scientific journals indexed in the Scopus database; two publications in the proceedings of international conferences; and one author's certificate has been received.

In all the listed publications, the applicant plays a leading role, and the main research results, analyses, models, and programs are created by the author, and the conclusions are based on the results obtained from the applicant's work and research.

The second section provides a comprehensive literature review, including a systematization of road defect types and an analysis of the evolution of detection methods. The historical transition from classical computer vision algorithms to modern deep learning architectures (convolutional networks, YOLO detectors, visual transformers) is examined. Fundamental gaps in existing research are identified, such as the difficulty of processing continuous video streams due to temporal inconsistency, the lack of representative video datasets, and the challenge of adapting heavyweight models to edge computing, which algorithmically justifies the current research direction.

The third section describes the research materials and methods in detail. The process of collecting, preprocessing, and precision annotation of a unique video dataset captured in realworld conditions is presented. The focus is on the mathematical and structural design of the innovative multi-task neural network architecture, TCR-RoadNet. The operation of the multiscale convolutional backbone, the contextual refinement module based on cross-scale transformer attention (TCR), and three specialized inference branches: a separate detection module, a classification refinement block, and an edge-aware segmentation branch are described in detail. The optimization strategy and multi-task loss functions (a combination of CIoU, Focal Loss, and BCE+Dice) are also presented.

The total volume of the dissertation is 104 pages, including 28 illustrations, 8 tables and a list of 154 references.
