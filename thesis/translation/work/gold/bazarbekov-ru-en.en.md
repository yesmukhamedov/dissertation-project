2) To develop the architecture and prototype of a sensor device for recording kinematic characteristics of graphomotor activity reflecting motor control disorders;

3) To form an experimental sample by collecting handwriting kinematic parameters in clinical conditions from representative groups of subjects, including patients diagnosed with Alzheimer’s disease and healthy volunteers;

4) To investigate and quantitatively evaluate specific kinematic differences in handwriting (for example, speed, acceleration and tremor) between patients with AD and cognitively healthy people from the control group;

5) To implement and evaluate a method for generating synthetic data based on mathematical modeling of pathological patterns to solve the problem of limited clinical datasets by generating synthetic data based on physical models that simulate AD symptoms;

6) To conduct a comparative study of neural network architectures based on recurrent and transformer models (LSTM, LSTM with attention mechanism, Transformer Encoder), as well as to design a hybrid CNN-BiLSTM deep learning architecture and determine the best classification quality among all studied approaches in the task of detecting cognitive decline at an early stage.

2) The method of forming an 18-channel feature space based on biomechanical time series of IMU signals, including derivative and integral kinematic characteristics (jerk, velocity, angular accelerations, orientation), the statistical analysis of which confirms the diagnostic significance of the identified intergroup differences between patients with Alzheimer’s disease and healthy subjects (p < 0.05).

3) A method for generating synthetic data based on mathematical modeling of pathological patterns, including algorithms for stochastic noise injection (to simulate tremor) and nonlinear temporal deformation (to simulate bradykinesia), the application of which makes it possible to compensate for the deficit of clinical samples and prevent model overfitting.

1) A comparative analysis of modern methods for diagnosing neurodegenerative diseases was carried out, which revealed significant limitations of current approaches (high cost of neuroimaging, subjectivity of clinical scales) and substantiated the need to develop accessible instrumental screening tools based on objective analysis of fine motor skills.

2) A sensor device was developed for recording handwriting kinematic parameters, including a combined inertial sensor (accelerometer, gyroscope) and specialized software, which makes it possible to conduct non-invasive data collection in natural writing conditions, eliminating stress effects on the patient typical for laboratory tests.

3) An experimental database of 3D handwriting kinematics was collected, characterized by high resolution and inclusion of dynamic parameters (jerk, microtremor), which ensures the necessary representativeness of the sample for identifying hidden patterns of neurodegeneration and verifying deep learning models.

4) A data augmentation method was applied for training neural networks under small sample conditions, based on mathematical modeling of pathological motor patterns (tremor and bradykinesia) using stochastic algorithms and nonlinear time scale deformation, which makes it possible to compensate for the lack of clinical examples and increase the generalization ability of models.

5) A comparative study of neural network architectures based on recurrent and transformer models was conducted: basic LSTM achieved AUC 0.7779, LSTM+Attention model – AUC 0.9597, Transformer Encoder – AUC 0.9268; a hybrid CNN-BiLSTM architecture was designed and validated, which demonstrated the best results among all studied approaches (AUC 0.963, Recall 0.930), which confirms the superiority of hybrid architectures over both classical machine learning algorithms and recurrent neural networks.

6) A set of kinematic indicators was identified, consisting of jerk, tremor and acceleration parameters, which allows diagnosing early stages of cognitive impairment with a sensitivity of 93.4 percent, outperforming standard clinical tests in effectiveness.

The scientific novelty of the research lies in the development of a hybrid neural network architecture (CNN-BiLSTM) for analyzing dynamic time series of handwriting kinematics, as well as a method for generating synthetic samples based on mathematical modeling of pathological symptoms (tremor and bradykinesia), which supplemented a unique experimental database, formed for the first time, of labeled fine motor signals in network training. This approach makes it possible to compensate for the lack of clinical data and achieve high predictive accuracy (AUC 0.96) compared to classical machine learning methods.

First, a sensor device based on inertial measurement units was developed. The device is a cost-effective and portable solution that enables non-invasive mass screening of the population in primary health care settings without requiring special technical training from medical staff.

In all listed publications, the applicant has a leading role in problem formulation, conducting research, and preparing the main text of the articles.

In the fourth section, classical and deep machine learning methods are implemented and experimentally investigated. Tuning and comparative analysis of SVM, Random Forest, k-NN, and logistic regression algorithms are performed. A comparative study of neural network architectures based on recurrent and transformer models is conducted: basic LSTM, LSTM with soft attention mechanism, and Transformer Encoder. A hybrid CNN-BiLSTM architecture for analyzing spatiotemporal patterns of biomechanical time series of IMU signals is substantiated and developed, which demonstrated the best results among all studied approaches. Hyperparameter optimization and evaluation of model performance using standardized quality metrics are carried out.

In the conclusion, the main results of the study are formulated, scientific and practical conclusions are summarized, and promising directions for further research in the field of applying artificial intelligence methods for diagnosing cognitive impairments are determined.

The full volume of the dissertation is 101 pages, including 21 figures, 12 tables, and 2 appendices. The list of references contains 132 sources.
