> English translation by the local model (Qwen). Source: `translation/work/eval/c1/council/src/bakirova-kz-en.kz.md`. Terminology: `translation/termbase.tsv`.

## PART 1: SECTION TEXT

4. Conducting an experimental evaluation of the efficiency, stability, and convergence of the developed models under various non-IID data conditions.

2. Data preprocessing and transformation methods: cleaning, validation, anomaly handling, feature encoding, and temporal feature transformation.

3. Ensemble and federated machine learning methods based on the aggregation of statistical representations of local models.

2. Federated machine learning models and methods were developed for analyzing distributed private data, ensuring local data processing, global model stability, and data confidentiality when operating in real-world distributed educational centers.

3. A federated learning architecture was proposed that ensures the construction of a global model based on local updates without transmitting clients' raw data to the server, thereby enabling compliance with privacy and personal data protection requirements.

Theoretical significance of the research: investigating problems of distributed data analysis based on machine learning theory. During the research, FedAvg, FedOpt, and FedProx were used as federated learning algorithms for a decentralized dataset, while Random Forest Regression was employed as the ensemble machine learning model for predictions. Additionally, classical statistical analysis methods and data preprocessing were utilized as the primary techniques. The work followed the standard stages of machine learning, from data preparation to result evaluation. It was implemented in Python using the scikit-learn, pandas, NumPy, and matplotlib libraries, which facilitated experiments and clarified visualization.

Practical significance of the research: the study aims to develop and expand federated machine learning methods by developing and implementing an approach adapted to the use of a non-differentiable ensemble Random Forest Regression model. The work proposes replacing the classical aggregation of model parameters with the aggregation of statistical representations of local models, namely feature importance vectors, which ensures the stability of the learning process in the case of heterogeneous (non-uniformly distributed) distributed data.

• FedAvg, FedOpt, and FedProx federated learning algorithms were adapted to a non-differentiable Random Forest regression model by shifting from weight aggregation to the aggregation of statistical metrics – feature importance vectors, which ensured the stability of training with heterogeneous (non-IID) data.

Within the scope of the research, a federated learning architecture for analyzing distributed data indicating students' psycho-emotional state was developed and implemented. Let us examine the architecture in detail: it consists of local models trained using the Random Forest Regression method on the client side, which ensures high prediction accuracy and robustness to data noise, while the global models trained on the server side perform aggregation without the server component accessing the raw data.

Data collection was conducted over a two-month period from 1 September to 30 October via a web platform distributed to all clients. The information base received data on nutrition, physical activity, sleep and rest, psycho-emotional state, as well as temporal and matching features. Data were collected from several educational institutions, which made it possible to model real heterogeneous conditions. Preprocessing of the data involved cleaning erroneous records, filtering outliers, converting temporal attributes to a numeric format, and encoding the student_id categorical identifier using the One-Hot Encoding method. We verified the consistency of the feature space across local datasets, which is necessary for correct federated aggregation.

The FedAvg, FedOpt, and FedProx federated learning algorithms were adapted to a non-differentiable Random Forest regression model: instead of aggregating model weights, the aggregation of statistical representatives, namely feature importance vectors, was employed. This approach preserves the mathematical logic of federated learning while ensuring the stability of the global model.

Chapter 1 examines the main approaches to federated learning and justifies the choice of synchronous horizontal Cross-Silo federated learning. The use of a unified feature space enabled the correct aggregation of local results without transmitting raw data. The architecture ensures the stable convergence of the global model, maintains privacy, and guarantees training efficiency under heterogeneous data conditions, thereby confirming the feasibility of applying the proposed solution in an educational environment.

Chapter 2 reviews federated learning algorithms and architectures. It demonstrates that the primary FedAvg and FedSGD methods ensure data privacy but lose stability in the case of non-uniform (non-IID) distributions. In contrast, FedOpt and FedProx enhance stability and accelerate convergence through proximal regularization and server-side optimization. Consequently, the selection of FedAvg, FedOpt, and FedProx methods represents the most balanced solution for analyzing distributed private data.

Chapter 4 presents a comparative analysis of the FedAvg, FedOpt, and FedProx federated learning algorithms for predicting students’ psycho-emotional stress. FedAvg exhibits limited efficiency with independent non-uniform (non-IID) data. FedOpt ensures faster and more stable convergence through server-side optimization. FedProx increases training stability via proximal regularization, although its convergence is slower. As a result, FedOpt was selected as the primary algorithm, FedProx as a stable solution for highly heterogeneous data, and FedAvg as the baseline.

In the Conclusion, the implementation and study of a federated learning architecture for analyzing students’ psycho-emotional state on distributed private data are described. It is considered that adapting the FedAvg, FedOpt, and FedProx algorithms to a non-differentiable Random Forest regression model ensures the stable convergence of the global model in the case of non-IID data. The results confirm the practical application of federated learning in an educational environment while preserving data privacy.

Structure and scope. The dissertation consists of an Introduction, five main chapters, a Conclusion, and a list of references. The total volume of the dissertation is 144 pages, including 46 figures and 14 tables. The bibliography comprises 105 titles.
