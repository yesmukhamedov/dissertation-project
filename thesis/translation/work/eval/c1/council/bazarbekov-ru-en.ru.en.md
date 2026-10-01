> English translation by the local model (Qwen). Source: `translation/work/eval/c1/council/src/bazarbekov-ru-en.ru.md`. Terminology: `translation/termbase.tsv`.

## PART 1: SECTION TEXT

2) To develop the architecture and prototype of a sensor device for recording kinematic characteristics of graphomotor activity, reflecting impairments in motor control;

3) To form an experimental sample by collecting handwriting kinematic parameters under clinical conditions from representative groups of subjects, including patients with diagnosed Alzheimer's disease and healthy volunteers;

4) To investigate and quantitatively assess specific kinematic differences in handwriting (e.g., velocity, acceleration, and tremor) between patients with AD and cognitively healthy individuals from the control group;

5) To implement and evaluate a synthetic data generation method based on mathematical modelling of pathological patterns to address the problem of limited clinical datasets by generating synthetic data grounded in physical models and simulating AD symptoms;

6) To conduct a comparative study of neural network architectures based on recurrent and Transformer models (LSTM, LSTM with attention mechanism, Transformer Encoder), as well as to design a hybrid CNN-BiLSTM deep learning architecture and determine the best classification quality among all investigated approaches in the task of detecting early-stage cognitive decline.

2) A method for forming an 18-channel feature space based on biomechanical time series of IMU signals, including derivative and integral kinematic characteristics (jerk, velocity, angular accelerations, orientation), the statistical analysis of which confirms the diagnostic significance of the identified inter-group differences between patients with Alzheimer's disease and healthy subjects (p < 0.05).

3) A synthetic data generation method based on mathematical modelling of pathological patterns, including stochastic noise injection algorithms (to simulate tremor) and non-linear temporal deformation (to simulate bradykinesia), the application of which allows compensating for the deficit of the clinical sample and preventing model overfitting.

1) A comparative analysis of modern diagnostic methods for neurodegenerative diseases was performed, revealing significant limitations of current approaches (high cost of neuroimaging, subjectivity of clinical scales) and justifying the need to develop accessible screening tools based on the objective analysis of fine motor skills.

2) A sensor device for recording handwriting kinematic parameters was developed, including a combined inertial sensor (accelerometer, gyroscope) and specialised software, which enables non-invasive data collection in natural writing conditions, excluding the stressful impact on the patient characteristic of laboratory tests.

3) An experimental 3D handwriting kinematics database was collected, distinguished by high resolution and the inclusion of dynamic parameters (jerk, micro-tremor), which ensures the necessary sample representativeness for identifying hidden neurodegeneration patterns and verifying deep learning models.

4) A data augmentation method for training neural networks under small sample conditions was applied, based on mathematical modelling of pathological motor patterns (tremor and bradykinesia) using stochastic algorithms and non-linear time scale deformation, which allows compensating for the deficit of clinical examples and improving model generalisation.

5) A comparative study of neural network architectures based on recurrent and Transformer models was conducted: the basic LSTM achieved AUC 0.7779, the LSTM+Attention model – AUC 0.9597, the Transformer Encoder – AUC 0.9268; a hybrid CNN-BiLSTM architecture was designed and validated, demonstrating the best results among all investigated approaches (AUC 0.963, Recall 0.930), which confirms the superiority of hybrid architectures over both classical machine learning algorithms and recurrent neural networks.

6) A complex of kinematic indicators, consisting of jerk, tremor, and acceleration parameters, has been identified, which allows for the diagnosis of early stages of cognitive impairments with a sensitivity of 93.4 percent, outperforming standard clinical tests in terms of efficiency.

The scientific novelty of the research lies in the development of a hybrid neural network architecture (CNN-BiLSTM) for analyzing dynamic time series of handwriting kinematics, as well as a method for generating synthetic samples based on the mathematical modeling of pathological symptoms (tremor and bradykinesia). These samples supplemented the unique experimental database of labeled fine motor signals, formed for the first time, during network training. This approach allows compensating for the deficit of clinical data and achieving high predictive accuracy (AUC 0.96) compared to classical machine learning methods.

First, a sensor device functioning on the basis of inertial measurement units has been developed. This device represents a cost-effective and mobile solution that enables non-invasive mass screening of the population in primary healthcare settings, without requiring special technical training from medical personnel.

In all the listed publications, the applicant plays a leading role in setting the tasks, conducting the research, and preparing the main text of the articles.

In Chapter 4, classical and deep machine learning methods were implemented and experimentally investigated. The configuration and comparative analysis of SVM, Random Forest, k-NN, and logistic regression algorithms were performed. A comparative study of neural network architectures based on recurrent and Transformer models was conducted: the basic LSTM, LSTM with a soft attention mechanism, and Transformer Encoder. A hybrid CNN-BiLSTM architecture for analyzing spatiotemporal patterns of biomechanical time series of IMU signals was justified and developed, demonstrating the best results among all investigated approaches. Hyperparameter optimization and model performance evaluation using standardized quality metrics were carried out.

In the Conclusion, the main results of the research are formulated, scientific and practical conclusions are generalized, and promising directions for further research in the field of applying artificial intelligence methods for the diagnosis of cognitive impairments are defined.

The total volume of the dissertation is 101 pages, including 21 illustrations, 12 tables, and 2 appendices. The list of references consists of 132 publications.
