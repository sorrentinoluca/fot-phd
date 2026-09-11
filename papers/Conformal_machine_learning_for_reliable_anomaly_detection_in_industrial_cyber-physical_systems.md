Reliability Engineering and System Safety 274 (2026) 112417 


![](Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems_images/Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems.pdf-0001-01.png)


Contents lists available at ScienceDirect 

# Reliability Engineering and System Safety 

journal homepage: www.elsevier.com/locate/ress 


![](Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems_images/Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems.pdf-0001-05.png)


## Conformal machine learning for reliable anomaly detection in industrial cyber-physical systems 


![](Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems_images/Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems.pdf-0001-07.png)


### Shuaiqi Yuan<sup>a</sup> , Jipu Li<sup>a</sup> , Chunjin Wang<sup>a</sup> , Xiaoge Zhang<sup>a,b,*</sup> 


![](Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems_images/Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems.pdf-0001-09.png)


a _Department of Industrial and Systems Engineering, The Hong Kong Polytechnic University, Hong Kong Special Administrative Region of China_ b _State Key Laboratory of Ultra-precision Machining Technology, Department of Industrial and Systems Engineering, The Hong Kong Polytechnic University, Hong Kong Special Administrative Region of China_ 

|A R T I C L E I N F O|A B S T R A C T|
|---|---|
|_Keywords:_<br>Anomaly detection<br>Industrial cyber-physical systems<br>Deep learning<br>Conformal prediction<br>Trustworthy AI<br>Uncertainty quantifcation<br>Safety and security|Although machine learning (ML) and deep learning (DL) methods are increasingly used for anomaly detection in<br>industrial cyber-physical systems, their adoption is hindered by concerns about model trustworthiness, especially<br>high false alarm rates (FARs). Excessive false alarms overwhelm operators, cause unnecessary shutdowns, and<br>reduce operational effciency. This study addresses these challenges by proposing a novel framework that in-<br>tegrates ML-based anomaly detectors with conformal prediction (CP), a model-agnostic uncertainty quantifca-<br>tion technique. To handle distribution shifts in time-series data, our framework incorporates a temporal quantile<br>adjustment method with a sliding calibration set, ensuring statistical guarantees on predefned FARs. A rejection<br>mechanism is further integrated by excluding signifcant anomalies from the calibration set, improving detection<br>capability while maintaining FAR guarantees. For real-time anomaly monitoring, two P-value-based indicators<br>generated from CP are developed to track anomalous trends and enhance model interpretability. The framework<br>is evaluated by comparing several baseline ML and DL methods to their conformalized counterparts using a<br>public ICPS dataset. Comparative results based on Precision, Recall, F1, and AUROC validate the framework's<br>compatibility with various ML models and its effectiveness in improving anomaly detection performance by<br>reducing false alarms and guaranteeing FARs across a range of predefned values.|



#### **1. Introduction** 

Industrial Cyber-Physical Systems (ICPSs), also known as industrial control systems (ICSs), have been increasingly deployed across various industrial sectors for digitalization and automation [1]. However, the occurrence of various undesirable events—both accidental and intentional/malicious—can induce dangerous deviations and disruptive events in these industrial systems, leading to catastrophic outcomes and significant economic loss [2]. Real-time anomaly detection plays a pivotal role in safeguarding ICPSs. By promptly identifying crucial anomalies or outliers in the data stream, anomaly detection serves as an early-warning technique to prevent initial events from escalating into disastrous scenarios. To enable real-time performance monitoring of — ICPSs, a variety of sensors such as pressure, temperature, and — gas-concentration sensors are typically deployed to produce multivariate time-series data that comprehensively characterize the system’s operational behavior and state [3]. 

A wide range of methods has been utilized for anomaly detection in 

industrial systems, and they can be roughly categorized into three classes: statistical methods, machine learning (ML) methods, and deep learning (DL) methods [4]. Classical statistical methods have long formed the foundation for anomaly detection. Statistical methods assume that anomalies follow a specific statistical distribution and rely on underlying assumptions about the distribution of data [4]. These methods, including ARIMA (Autoregressive Integrated Moving Average)-based techniques [5] and Principal Component Analysis (PCA) [6,7], offer significant advantages in terms of theoretical foundation and the transparency of their decision-making process [4]. However, these methods can be computationally expensive when handling high-dimensional data due to the need for parameter estimation and matrix operations requirements. Moreover, these methods are limited in their ability to capture complex non-linear relationships, non-stationary patterns, or might fail to detect anomalies that appear as subtle deviations in multivariate correlations rather than as simple statistical outliers. Consequently, they are best suited for scenarios where: i) low-dimensional data exhibit normal behavior following well-defined 

- Corresponding author. 

_E-mail address:_ xiaoge.zhang@polyu.edu.hk (X. Zhang). 

https://doi.org/10.1016/j.ress.2026.112417 

Received 4 May 2025; Received in revised form 19 January 2026; Accepted 12 February 2026 Available online 13 February 2026 

0951-8320/© 2026 Elsevier Ltd. All rights are reserved, including those for text and data mining, AI training, and similar technologies. 

_Reliability Engineering and System Safety 274 (2026) 112417_ 

statistical distributions, and ii) theoretical interpretability and regulatory compliance are essential [8]. In contrast, machine learning (ML) and deep learning (DL) methods learn informative representations directly from time-series data for generating anomaly scores to characterize the system behavior. Anomalies are subsequently identified when these scores exceed a predefined threshold. In particular, unsupervised learning approaches have been widely adopted for anomaly detection in industrial cyber-physical systems [9]. Compared to classical statistical methods, ML/DL approaches exhibit superior performance in detecting anomalies within multivariate time-series data, rather than merely identifying isolated point deviations. Consequently, these methods have become increasingly prevalent in anomaly detection applications for industrial control systems [10,11]. 

Classical ML methods—such as support vector machines (SVMs) [12], Isolation Forest (IF) [13], and k-nearest neighbors (k-NN) [14]— have shown strong performance for anomaly detection in industrial settings using multivariate time-series data. Deep learning (DL) methods have likewise gained prominence for their ability to learn discriminative patterns from multivariate time series with inherent spatiotemporal dependencies, typically detecting anomalies via thresholds on prediction errors, reconstruction errors, dissimilarity measures, or combinations thereof [15]. Researchers have explored a range of DL architectures for anomaly detection in industrial multivariate time series. Convolutional neural networks (CNNs) [16,17], long short‑term memory (LSTM) networks [18], generative adversarial networks (GANs) [19], deep autoencoders and their variants [20–22], and graph neural networks (GNNs) [23] have all demonstrated strong performance in industrial control systems. Hybrid and advanced architectures—such as parallel graph attention layers [24], deep convolutional autoencoders with memory networks [25], and deep convolutional autoencoders with transformer components [11]—have also shown promising results for anomaly detection in industrial environments. 

While ML- and DL-based anomaly detection has shown potential in industrial applications, there have been significant concerns about the deployability of these methods in safety- and security-critical environments. These concerns primarily stem from their "black-box" nature and the lack of confidence calibration [26]. In particular, the excessive false alarm rates frequently observed in practice substantially undermine the utility of ML/DL-based anomaly detection systems. High false alarm rates may overwhelm operators, reduce operational efficiency, and lead to unnecessary system shutdowns, inspections or maintenance [27]. The integration of uncertainty quantification (UQ) techniques offers a promising solution to improving the trustworthiness and reliability of ML/DL models by accounting for both aleatory and epistemic uncertainties in the model predictions. Uncertainty-aware ML methods—including Bayesian neural networks, Gaussian process regression, Monte Carlo dropout, ensemble techniques, and hybrid methods—have been extensively investigated in engineering design and health prognostics domains [28]. In industrial anomaly detection, methods such as Bayesian autoencoders and uncertainty-based prediction rejection mechanisms have been developed to improve the reliability of ML-based anomaly detectors [27,29]. However, these approaches are still unable to offer rigorous statistical guarantees for critical metrics such as false alarm rates. 

Conformal prediction emerges as a distribution-free uncertainty quantification method that enables statistically valid uncertainty quantification under the mild assumption of data exchangeability [30]. This approach holds significant potential for reliable uncertainty quantification in anomaly detection by providing statistical guarantees on false alarm rates. Notably, conformal prediction operates as a post-processing step that can be seamlessly integrated with any existing ML/DL model without requiring architectural modifications [31]. Previous studies have explored conformal prediction for anomaly detection across various application domains. For instance, Laxhammar and Falkman [32] employed conformal prediction for anomaly detection in streaming vessel data. Later, Laxhammar [33] extended this approach to 

detect abnormal trajectories in surveillance applications. More recently, Saboury and Uyguroglu [34] combined unsupervised autoencoders with conformal prediction for autonomous navigation in dynamic indoor environments for controlling false alarm rates. However, these studies operate under the assumption of data exchangeability, which may be violated in dynamic environments where temporal distribution shifts are — prevalent particularly in industrial time series data. To overcome this limitation, several methods have been proposed to adapt CP for handling distribution shifts in time-series data. Xu and Xie [35] developed a general framework for constructing prediction intervals in time series data by relaxing the data exchangeability assumption required for CP. Lin et al. [36] introduced Temporal Quantile Adjustment (TQA) to construct valid prediction intervals for cross-sectional time series regression by extending beyond the regular exchangeability requirements. Zhang and Zhou [37] integrated global and local nonconformity score information within a CP framework to adjust confidence levels and provided effective prediction intervals for industrial time series while adapting to distribution shifts. Nevertheless, these augmented CP methods focus primarily on time series prediction rather than anomaly detection. The applicability and effectiveness of leveraging CP for anomaly detection in industrial control systems—while accommodating distribution shifts and providing robust false alarm rate guarantees with real-time deployment capability—remains a challenging and largely unexplored research area. 

To address this challenge, we propose a conformal machine learning framework for anomaly detection in industrial systems that provides formal statistical guarantees on predefined false alarm rates while effectively handling temporal distribution shifts in multivariate timeseries data. The main contributions of this study are summarized as follows: 

- i) This study establishes a conformal prediction-based framework for reliable anomaly detection in industrial cyber-physical systems. To this end, our method exploits deep learning to capture the complex spatial-temporal dependency in multivariate timeseries data and leverages conformal prediction to provide formal statistical guarantees on the false alarm rate. These characteristics make the proposed framework particularly wellsuited for a wide range of safety-critical industrial applications. 

- ii) We introduce an integrated approach that combines Temporal Quantile Adjustment (TQA), a sliding calibration set, and a rejection mechanism to effectively address distribution shifts in multivariate time-series data. In doing so, we maintain a formal statistical guarantee on the false alarm rate while preserving robust anomaly detection capability under non-stationary environments. 

- iii) We introduce P-value-based indicators generated by the conformal prediction for enhanced anomaly monitoring. These indicators provide interpretable, probabilistic measures of anomalousness for individual data instances and effectively capture anomalous trends in the time-series data. Compared to traditional anomaly scores, they provide superior interpretability by quantifying how statistically unusual each observation is relative to the normal data distribution. 

The remainder of this paper is organized as follows: Section 2 introduces key concepts and methods for anomaly detection and conformal prediction. Section 3 outlines the methodology for developing conformal machine learning framework for anomaly detection. Section 4 details computational experiments conducted on a publicly available ICS dataset to evaluate the framework's compatibility with various machine learning models and assess the impact of conformal prediction-based anomaly thresholding on model performance. Section 5 evaluates the effectiveness of the proposed method in delivering robust false alarm rate (FAR) guarantees across a range of predefined FAR levels, with comparisons to conventional methods and practices for 

2 

> _S. Yuan et al.                                                                                                                                                                                                                                    Reliability Engineering and System Safety 274 (2026) 112417_ 

anomaly thresholding. Section 6 discusses a rejection mechanism for the sliding calibration set within the conformal prediction pipeline, while Section 7 examines the use of P-value–based measurements as indicators for anomaly monitoring. Finally, Section 8 presents the conclusions. 

#### **2. Preliminaries** 

#### _2.1. Anomaly detection in multivariate time series_ 

Typically, multi-sensor data is collected and managed through Supervisory Control and Data Acquisition (SCADA) systems within Industrial Cyber-Physical Systems (ICPS) to support anomaly detection. Considering time-series data, anomalies are defined as data points at specific time steps that exhibit unexpected behaviors by deviating significantly from patterns observed in previous time steps. Multivariate time series introduce additional complexity due to interdependencies — among observed variables often termed as spatio-temporal relation— ships and anomalies in such data are commonly categorized as point, contextual, collective, and other types [15]. These spatio-temporal dependencies pose significant challenges for anomaly detection in multivariate time series. 

Formally, given a multivariate time-series dataset represented as _X_ ∈ R<sup>_N_×</sup><sup>_T_</sup> : 


![](Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems_images/Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems.pdf-0003-06.png)


where _T_ indicates the number of time steps considered, _N_ is the number of variables under monitoring, and _x_<sup>_j_</sup> _i_<sup>denotes the observation of variable</sup> _i_ at the time step _j_ . The goal is to develop an anomaly score that captures inherent patterns in the multivariate time series across both temporal and spatial dimensions. These scores characterize system behavior, enabling threshold-based detection, with anomalies expected to yield higher anomaly scores than normal instances. 

In practice, anomaly scores can be obtained using various approaches, including prediction errors [38], reconstruction errors [39, 40], dissimilarity-based measures—such as Euclidean distance [41], Minkowski distance [42], and cosine similarity [43]—or hybrid metrics that combine multiple metrics [44]. Here, we illustrate with an autoencoder (AE), using reconstruction error as the anomaly score. Autoencoders are neural networks designed for unsupervised learning, commonly used for dimensionality reduction, anomaly detection, and feature extraction [45]. They comprise an encoder that compresses input data into a low-dimensional latent representation and a decoder that reconstructs the original data from the compressed representation. 

In anomaly detection applications, an AE is typically trained on a dataset of representative normal samples (e.g., the aforementioned training dataset) with the objective of minimizing reconstruction error. Suppose the training set ( _X_<sup>_T_</sup> ) consists of _n_ normal instances, let _x_<sup>_T_</sup> _i_ represent _i_ th sample from the training set. The encoder is denoted as _E_ (⋅) parameterized by _θe_ representing model weights and biases. _h_<sup>_T_</sup> _i_<sup>repre-</sup> sents the latent representation corresponding to the data sample _x_<sup>_T_</sup> _i_<sup>. The</sup> decoder is denoted as _D_ (⋅) with its parameters denoted as _θd_ . The reconstructed _i_ th sample is denoted as _x_<sup>_T_</sup> _i_<sup>. The autoencoder is trained to</sup> minimize the reconstruction error with the loss function **L** _ae_ defined as the mean squared error (MSE) between the original and reconstructed data samples, as shown in Eq. (4). 


![](Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems_images/Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems.pdf-0003-10.png)



![](Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems_images/Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems.pdf-0003-11.png)



![](Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems_images/Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems.pdf-0003-12.png)


Intuitively, when an anomalous instance is presented, the trained autoencoder often struggles to accurately reconstruct it from its latent representation, leading to a higher reconstruction error compared to normal instances. For an unseen test instance _xtest_ , anomaly detection is performed by comparing the reconstruction error ‖ _xtest_ − _xtest_ ‖<sup>2</sup> to a predefined threshold _τ_ , where _xtest_ represents the reconstructed version of _xtest_ . As illustrated in Eq. (5), the model _C_ (⋅) outputs 1 if the test instance is classified as an anomaly, and 0 otherwise. 

#### _2.2. Conformal prediction_ 

Conformal Prediction (CP) offers distribution-free statistical guarantees based on the assumption of data exchangeability and functions as a postprocessing step that can be applied to any machine learning model. CP methods are generally classified into full conformal prediction and split (or inductive) conformal prediction. Due to its lower computational cost and preserved statistical validity [31], split conformal prediction is adopted here and referred to simply as CP by default. 

Here, we introduce conformal prediction using a classification _K_ classes. problem as an example. Consider a classification problem with Let _f_ ( _x_ ) ∈[0 _,_ 1]<sup>_K_</sup> denote a classifier that outputs estimated probabilities for each of the _K_ class. Given _f_ and a calibration set containing _n_ data samples, our goal is to construct a prediction set of possible labels _C_ ( _xtest_ )⊂{1 _, …, K_ } such that the following statistical guarantee is satisfied: 


![](Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems_images/Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems.pdf-0003-17.png)


where ( _xtest, ytest_ ) is a new test sample drawn from the same data distribution, and _α_ is a user-defined significance level (error rate). In other words, CP guarantees that the prediction set contains the true label with a probability of at least 1 − _α_ . To construct the prediction set, a calibration step is required for creating a nonconformity score, _si_ , defined as follows: 


![](Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems_images/Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems.pdf-0003-19.png)


where _f_ ( _xi_ ) _yi_ denotes the probability of the trained model _f_ in assigning the true class _yi_ to the input _xi_ . Next, we compute the nonconformity score for each data point in the calibration set, obtaining a set of calibration scores { _s_ 1 _, …, sn_ }. These scores are then ranked in ascending order, and the threshold _q_ is determined as the ⌈( _n_ +1)(1 − _α_ )⌉ _/n_ quantile of the ranked nonconformity scores. Finally, for a new test data point where _xtest_ is known but _ytest_ is unknown, the prediction set is defined as: 


![](Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems_images/Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems.pdf-0003-21.png)


By following the steps outlined above, CP guarantees the generation of statistically valid prediction sets that contain the true label with a prespecified coverage of 1 − _α_ . Remarkably, this method ensures this guarantee regardless of the underlying model or the unknown data distribution. 

#### **3. Methodology** 

In this paper, we develop a novel methodology for reliable anomaly detection in the context of ICPS by integrating machine learning with a 

3 

> _S. Yuan et al.                                                                                                                                                                                                                                    Reliability Engineering and System Safety 274 (2026) 112417_ 

unified conformal prediction framework. The proposed approach is featured by its high anomaly detection accuracy, a controllable false alarm rate and computational efficiency, making it ideal for a wide range of industrial applications. At a high level, the proposed approach comprises three main steps: data preprocessing, model training, and conformal prediction for anomaly thresholding. Fig. 1 provides an overview of the proposed methodology, with detailed explanations of each component presented in the following sub-sections. 

#### _3.1. Anomaly detection as a conformal machine learning problem_ 

In industrial cyber-physical systems (ICPSs), multiple sensors are typically deployed to monitor diverse industrial process parameters such as temperature, pressure, flow rate, and other vital indicators. An important step in building machine learning (ML) or deep learning (DL) models for anomaly detection is to establish an anomaly score to accurately characterize the behavior of ICPSs by learning from the multivariate time-series data. The learned score represents the behavior of the system under various operation conditions and enables the identification of abnormal system behavior by thresholding. To facilitate the construction of an anomaly score, it is essential to address the following data-related issues to ensure the data is ready for ML or DL model development: 

- i) Since the time series data from different sensors may have inconsistent temporal resolutions, the multivariate time-series data needs to be downsampled or upsampled to ensure a 

unified temporal scale, ensuring a good alignment across all sensors with consistent timestamps. 

- ii) Due to the diverse units and scales of measurements from multiple sensors, a normalization method, such as min-max normalization, should be applied to transform the data into a uniform scale, thereby enabling more effective and efficient model training. 

- iii) To capture temporal patterns effectively, a sliding time window with a fixed time step is used to continuously generate data samples in the form of multivariate data sequences, as illustrated at the top center of Fig. 1. 

After data preprocessing, we partition the processed samples into three datasets: a training set, a calibration set, and a test set. The training set consists exclusively of normal data and is used for model training. The test set contains both normal and anomalous instances, enabling comprehensive assessment of the model's anomaly detection capability. Additionally, we reserve an independent calibration set containing only normal data for conformalizing the trained anomaly detector. Crucially, the calibration set is kept separate from both the training and test sets to ensure unbiased threshold determination in conformal prediction. The methodology proceeds as follows: First, an ML/DL model is trained on the training set to learn to estimate anomaly scores. Next, conformal prediction is applied to determine a cutoff threshold using the calibration set, thereby conformalizing the anomaly scores generated by the model. Finally, the test set is used to evaluate overall model performance using metrics that reflect detection accuracy, false alarm rates, and other 


![](Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems_images/Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems.pdf-0004-09.png)


**Fig. 1.** An overview of the proposed methodology. 

4 

_Reliability Engineering and System Safety 274 (2026) 112417_ 

_S. Yuan et al.                                                                                                                                                                                                                                    and_ 

relevant measures. The proposed conformal prediction framework is generic and can be combined with any ML/DL model for reliable anomaly detection. For demonstration purposes, we employ reconstruction-error-based anomaly detection using autoencoders due to their popularity, strong performance, simplicity, and scalability [46], as illustrated in the middle section of Fig. 1. 

#### _3.2. Conformal prediction for reliable anomaly detection_ 

Given the need to provide statistical guarantees on false alarm rates, we exploit conformal prediction (CP) to wrap around ML- and DL-based anomaly detectors for reliable anomaly detection. In CP, an essential step is to construct the nonconformity score. Notably, any anomaly score tailored explicitly to and produced by the chosen ML/DL model can, in principle, serve as the nonconformity score within the CP framework. Suppose we use the reconstruction error defined below as the nonconformity score function. 


![](Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems_images/Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems.pdf-0005-05.png)


where s( _x_<sup>_c_</sup> _i_ ) denotes the nonconformity score for the _i_ th sample _x_<sup>_c_</sup> _i_<sup>in the</sup> calibration set with _k_ samples. _x_<sup>_c_</sup> _i_<sup>represents the corresponding recon-</sup> structed version of data sample _x_<sup>_c_</sup> _i_<sup>. Each data sample is a multivariate</sup> time series sequence with _m_ variables _and n_ time steps, where _x_<sup>_c_</sup> _i_<sup>(</sup><sup>_j,t_)</sup> represents the _j_ th variable at time step _t_ in the original sample _x_<sup>_c_</sup> _i_<sup>, and</sup> _x_<sup>_c_</sup> _i_<sup>(</sup><sup>_j,t_)represents the</sup><sup>_j_th variable at time step</sup><sup>_t_in the reconstructed</sup> sample _x_<sup>_c_</sup> _i_<sup>. The nonconformity score is calculated as the mean squared</sup> error between the original and reconstructed sequences. 

To ensure a statistical guarantee on the false positive rate, it is necessary to maintain the false positive rate below a predefined significance level _α_ specified by end user, e.g., _α_ = 0 _._ 05. As outlined by Angelopoulos and Bates [31], we have: 


![](Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems_images/Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems.pdf-0005-08.png)


where _x_<sup>ʹ</sup> is a data sample from the normal dataset _Xnormal_ . _C_ (⋅) output anomaly detection result (e.g., 1 or 0) with the help of CP for thresholding. To achieve this, it is necessary to query the quantile of nonconformity scores using an independent calibration set with _k_ samples, as shown below. 


![](Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems_images/Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems.pdf-0005-10.png)



![](Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems_images/Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems.pdf-0005-11.png)


where the nonconformity scores of the calibration set, {s( _x_<sup>_c_</sup> 1) _, …,_ s( _x_<sup>_c_</sup> _k_ )}, are ranked in an ascending order to determine the ⌈( _k_ +1)(1 − _α_ )⌉ _/k_ quantile of the nonconformity score. The identified nonconformity score _q_ corresponding to the ⌈( _k_ +1)(1 − _α_ )⌉ _/k_ quantile is then used as the threshold for anomaly detection. For instance, given an unseen data instance _x_<sup>∗</sup> , its nonconformity score is derived as _s_ ( _x_<sup>∗</sup> ). The established cutoff value _q_ is then used to decide whether _x_<sup>∗</sup> is anomalous or not. As shown in Eq. (12), if the nonconformity score of _x_<sup>∗</sup> is no less than _q_ , then we will label _x_<sup>∗</sup> as anomalous; otherwise, not. 

Moreover, the p-value in conformal prediction indicates the proportion of calibration scores (nonconformity scores of samples in the calibration set) that are greater than or equal to the nonconformity score of a test sample. From this perspective, CP provides a quantitative measure of anomalous level for data samples. Given an unseen test instance _x_<sup>∗</sup> , the anomaly detection can be performed using a p-value method, which is equivalent to above-described CP thresholding approach, as shown below: 


![](Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems_images/Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems.pdf-0005-14.png)



![](Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems_images/Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems.pdf-0005-15.png)


where _p_ ( _x_<sup>∗</sup> ) is the p-value for the test instance _x_<sup>∗</sup> , _s_ ( _x_<sup>_c_</sup> _i_ ) are nonconformity scores from the calibration set {s( _x_<sup>_c_</sup> 1) _, …,_ s( _x_<sup>_c_</sup> _k_ )}, and I{ _s_ ( _x_<sup>_c_</sup> _i_ ) ≥ _s_ ( _x_<sup>∗</sup> )} is an indicator function that equals 1 if _s_ ( _x_<sup>_c_</sup> _i_ ) ≥ _s_ ( _x_<sup>∗</sup> ) and 0 otherwise. 

#### _3.3. Conformal prediction for anomaly detection under distribution shift_ 

While conformal prediction (CP) provides a rigorous statistical guarantee on model coverage, this guarantee is only valid under the assumption of data exchangeability. However, time-series industrial data violates the assumption of data exchangeability due to the inherent temporal dependency in the observed data. To tackle this challenge, additional adjustments are necessary to guarantee the model coverage in the context of distribution shift. To tackle this problem, we employ the – Temporal Quantile Adjustment Quantile Budgeting method (referred to as TQA in this paper) proposed by Lin et al. [36] to establish an adaptive threshold for reliable anomaly detection using multivariate time-series data. 

The core concept of TQA is to adjust the quantile of the nonconformity score by introducing an adjustment parameter _δ_ such that the desired significance level is guaranteed by adjusting the target coverage as _α_ = _α_ − _δ_ . Considering the incorporation of the temporal dimension in TQA method, we assign _t_ = 1 to the beginning of the calibration set, with the calibration set extending up to the present time. Since _δ_ is unknown, we learn _δ_ as a prediction of _δ_ and estimate the value of _δ_ via a mapping function: _δt_ ← _g_ ( _rt_ ; _α_ ), where _rt_ denotes the rank of nonconformity scores within the calibration set at time _t_ , and _rt_ is designed to predict _rt_ , described as below. 


![](Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems_images/Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems.pdf-0005-20.png)



![](Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems_images/Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems.pdf-0005-21.png)


> where _~~ε~~ t_ represents the exponentially weighted nonconformity score at time _t_ , with _β_ being a decay factor (e.g. set as 0.8 in this study). _st_ ʹ denotes the nonconformity score at time _t_<sup>ʹ</sup> . _rt_ represents the quantile of _~~ε~~ t_ within the set of weighted nonconformity scores { _~~ε~~ t_ <u>}. The function</u> _Q_<sup>−1</sup> is the inverse quantile function, and it computes the quantile _~~ε~~ t_ of within 

> <u>{</u> _~~ε~~_ <u>}. Finally, the adjusted quantile</u> _δt_ is calculated as follows: 


![](Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems_images/Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems.pdf-0005-23.png)



![](Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems_images/Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems.pdf-0005-24.png)


where _M_ is a constant that can be calculated using Eq. (18). 

The updated target coverage _α_ , _α_ = _α_ − _δ,_ is used to query the quantile, instead of using _α_ in the original approach. Since _α_ tends to approach 0, this can lead to overly conservative guarantees on the false alarm rate (e.g., a false positive rate of 0 but at the cost of a significantly reduced true positive rate). Empirically, bounding away from 0 has been shown to enhance anomaly detection performance. To overcome this problem, a scaling factor _λ_ is introduced to adjust _δ_ , as suggested by Lin et al. [36]. For instance, if we impose a restriction of _α_ ≥ 0 _._ 01, we have: 

_α_ = _α_ − _λδ_ ≥ 0 _._ 01 (19) 

5 

_Reliability Engineering and System Safety 274 (2026) 112417_ 

_S. Yuan et al.                                                                                                                                                                                                                                    and_ 

Considering Eqs. (16) to (18), _λ_ can be derived given the value of _α_ . 

outlining the procedure is presented in Fig. 2. 

#### **4. Experiments and result** 

#### _3.4. Sliding calibration set and anomaly rejection mechanism_ 

#### _4.1. System description and data preparation_ 

As illustrated at the bottom left of Fig. 1, we use a sliding time window to maintain a calibration set with a fixed size. Essentially, this operates by gradually incorporating newly test instances into the calibration set while simultaneously removing the earliest instances. In principle, the calibration set should contain only normal data. However, due to the sliding window operation, a significant number of anomalous instances may be included in the calibration set, which can degrade the detector's anomaly detection performance. To address this issue and balance maintaining false alarm rate (FAR) guarantees with preserving detection capabilities, an additional rejection criterion is applied. This criterion excludes clearly anomalous data while retaining in-distribution and slightly anomalous data, as outlined below. 


![](Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems_images/Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems.pdf-0006-08.png)



![](Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems_images/Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems.pdf-0006-09.png)


where _T_ represents the threshold that determines whether the test instance is added to the calibration set. The threshold _T_ is determined based on _γ_ quantile of the nonconformity scores from the initial calibration set ( _Sinitial_ ) and an inflation factor, _μ_ . If the nonconformity score of a new test instance, _s_ ( _x_ ), is below the threshold _T_ , calibration set slides by incorporating the new test instance and removing the oldest one in the set. Otherwise, the calibration set remains unchanged. This sliding mechanism is formalized in Eq. (21), where _St_ is the calibration set at time _t_ and _St_ +1 represents the calibration set at time _t_ + 1. 

The inclusion of anomalous instances in the calibration set presents a critical challenge: while it does not compromise FAR guarantees (as higher anomaly scores raise the detection threshold), it can undermine detection capability by contaminating the distribution of the calibration set. To maintain false alarm rate (FAR) guarantees while preserving detection capabilities, two parameters control this rejection mechanism: _γ_ (rejection quantile) and _μ_ (inflation factor). The rejection quantile _γ_ determines the initial threshold for identifying suspected anomalies in the calibration set, based on the underlying detector's capability to distinguish anomalies from normal instances. In principle, _γ_ should satisfy _γ_ ≥ 1− _α_ (where _α_ is the significance level) to ensure proper mechanism function. Higher _γ_ values (e.g., 0.99 vs. 0.95) provide more permissive rejection criteria, accepting more borderline instances as normal. The inflation factor _μ_ serves as a safety margin that deliberately raises the rejection threshold above the _γ_ -quantile of the initial calibration set. This margin provides a dual benefit: it accommodates moderate distribution shifts and reduces false rejections of new normal patterns, while still protecting against anomaly contamination. Larger _μ_ values (e.g., 0.05 vs. 0.01) increase tolerance for new normal patterns but may also permit more anomaly contamination. 

The configuration for those two parameters requires balancing tradeoffs based on detector quality and anticipated distribution shift severity. In this study, we set _γ_ = 1 and _μ_ = 0.01 to ensure inclusion of indistribution data while allowing limited incorporation of borderline instances from the test set. This conservative configuration prioritizes maintaining detection capability while providing basic protection against calibration contamination. For practical deployment, practitioners should adapt these parameters to their operational context. Applications anticipating abrupt distribution changes can implement periodic recalibration of the nonconformity scores using recent normal operational data, or temporarily increase _μ_ during known transition periods (e.g., seasonal changes, operational mode switches). Further discussion on the impact of this rejection mechanism is provided in Section 6. To summarize and clarify the implementation of the proposed conformal prediction method for anomaly detection, a pseudocode 

Laso et al. [47] designed and carried out experiments on an industrial cyber-physical system platform comprised of two liquid containers intended for either fuel or water, integrated with an advanced automated control and data acquisition infrastructure. The system features two storage tanks of distinct volumes (7 L and 9 L respectively), functioning as storage and distribution units; one ultrasound depth sensor for liquid level measurements; four discrete sensors to monitor critical states; and two pumps to regulate fluid dynamics. All hardware components are controlled by a logic controller (PLC), which is seamlessly connected to a monitoring network, enabling real-time monitoring and data collection, as shown in Fig. 3. 

The researchers gathered data across 15 distinct real-world operational scenarios, capturing a diverse range of system behaviors. The resulting dataset is well-suited for benchmarking anomaly detection techniques in multivariate time series contexts. It encompasses ten monitored variables and includes not only data representing normal operation, but also a wide variety of anomaly scenarios. These anomalies—induced by both accidental and deliberate actions—comprise events such as component failures, physical sabotage, and cyberattacks. 

Following the data preprocessing method described in Section 3.1, all data was first resampled to a time step of 0.05 s considering the differing temporal resolutions of the monitored variables. Next, the data was normalized using the min-max normalization technique, ensuring that all features were scaled to the range [0, 1]. To better capture the inherent temporal dependencies in the dataset, a sliding time window of 50 time steps was applied continuously to generate sequential data samples, which were subsequently used for dataset splitting. Given that unsupervised learning is employed in this study, a training set was created using 60 % of the normal data. Additionally, a calibration set containing 30 % of the normal data was constructed to facilitate conformal prediction and derive nonconformity scores. The remaining 10 % of the normal data was combined with the anomalous data to form the test set, which was then used for model evaluation. 

Due to the relatively large amount of anomalous data available in the dataset, including all anomalous instances in the test set would result in anomalies approaching or even exceeding the number of normal data instances. Such an imbalance would distort evaluation results, as the ratio between normal and anomalous data would significantly differ from real-world scenarios. To maintain a reasonable ratio between normal and anomalous samples and ensure the inclusion of all available anomalous classes in the test set, a balanced sampling strategy was applied. For anomalous classes with fewer than 500 samples, all data instances were included in the test set. Conversely, for anomalous classes with _>_ 500 samples, a random selection of 500 consecutive instances was made. This random sampling process for anomalous data is repeated 20 times to provide robust and varied test sets. As a result, 20 test sets were generated for repeated tests, each containing the same normal data samples but differing in the selection of anomalous data. This approach ensures a comprehensive evaluation by fully leveraging the available anomalous data while preserving a more realistic normalto-anomalous ratio in the test sets. Details of the training set, calibration set, and test set are summarized in Table 1 below. 

#### _4.2. Model training_ 

Due to the model-agnostic nature, the conformal prediction method can be wrapped around any machine learning or deep learning model to support reliable anomaly detection. Given the inherent complex spatiotemporal characteristics of multivariate time series data, we develop a deep autoencoder architecture that combines convolutional neural 

6 

> _S. Yuan et al.                                                                                                                                                                                                                                    Reliability Engineering and System Safety 274 (2026) 112417_ 


![](Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems_images/Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems.pdf-0007-01.png)


**Fig. 2.** Pseudocode of the conformal anomaly detection method. 

network (CNN) layers [48] with long short-term memory (LSTM) layers [49]. The autoencoder architecture is designed to capture the inherent spatio-temporal dependencies present in the multivariate time series data (Fig. 4). The encoder employs three Conv1D layers with progressively decreasing filter sizes (128→64→32) and increasing kernel sizes (3→7→11) to establish a hierarchical feature extraction mechanism that captures both fine-grained local patterns and broader temporal contexts. The extracted spatial features are then processed by two LSTM layers (32→16 units) to learn temporal dependencies, and are ultimately compressed into an 8-dimensional latent space via a dense layer. The decoder mirrors this structure in reverse, reconstructing the input passing the latent representation through LSTM layers (16→32 units), followed by Conv1DTranspose layers that restore the original dimensionality. 

The architectural hyperparameters were determined based on the model performance on a validation subset. The filter progression (128/ 64/32) aligns with established practices for constructing feature hierarchies, while the increasing kernel sizes facilitate multi-scale pattern recognition. The LSTM units (32/16) are selected to balance model expressiveness with computational efficiency while the 8-dimensional bottleneck ensures sufficient compression without compromising reconstruction quality. All CNN layers incorporate BatchNorm, ReLU 

activation, and a dropout rate of 0.3 for regularization based on the model performance on the validation data. 

The autoencoder is trained using Mean Squared Error (MSE) as its — reconstruction loss function. The hyperparameters including the Adam optimizer (learning rate = 0.001), a batch size of 128, and 100 epochs—are optimized to minimize the reconstruction loss. The loss converges after 100 epochs. Once trained, the autoencoder serves as the basis for conformal prediction, where its reconstruction error functions as the _α_ = 0 _._ nonconformity score. A significance level, 05, is configured as the target coverage in conformal prediction. 

To evaluate our proposed method, we benchmark it against several baseline models using the same training and test datasets. These include statistical methods, shallow machine learning methods, and deep learning models as follows: 

Statistical Method Baselines: 

- **Vector Autoregressive (VAR):** VAR modeling captures temporal dependencies and inter-variable relationships by representing each variable as a linear combination of lagged values of all variables in the system. Prediction errors, calculated as the residual between observed and those predicted by the VAR model, serve as anomaly scores [50]. Anomalies are detected using a threshold value set at the 

7 

> _S. Yuan et al.                                                                                                                                                                                                                                    Reliability Engineering and System Safety 274 (2026) 112417_ 


![](Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems_images/Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems.pdf-0008-01.png)


**Fig. 3.** The industrial cyber-physical system under study (adapted from [47], CC BY 4.0). 

**Table 1** 

Details of the split datasets. 

|Names of data sets|Data categories|Numbers of data samples|
|---|---|---|
|Training set|normal|81,660|
|Calibration set|normal|40,830|
|Test set|normal|13,611|
||Anomalous (bad_conection)|500|
||Anomalous (blocked_1)|451|
||Anomalous (blocked_2)|251|
||Anomalous (DoS_attack)|500|
||Anomalous (high_blocked)|500|
||Anomalous (hits_1)|500|
||Anomalous (hits_2)|500|
||Anomalous (hits_3)|500|
||Anomalous (plastic_bag)|500|
||Anomalous (poly_2)|500|
||Anomalous (poly_7)|500|
||Anomalous (second_blocked)<br>|500|
||Anomalous (spoofng)|500|
||Anomalous (wet_sensor)|251|



95th percentile of the prediction errors in the training dataset. The VAR model order is optimized to maximize the F1-score. 

- **Principal Component Analysis (PCA) with Hotelling's T² statistic:** PCA is applied for dimensionality reduction while preserving the essential variability of the original data. Hotelling's T² statistic measures the statistical distance of each observation from the center of the principal component space, following an F-distribution under multivariate Gaussian assumptions [7]. Anomalies are detected using a theoretical threshold calculated from the F-distribution at a 95 % confidence level. The number of principal components is optimized to maximize the F1-score. 

- **PCA with SPE (Squared Prediction Error):** Following PCA dimensionality reduction, the SPE (also known as Q-statistic) quantifies the reconstruction error in the residual space that is not captured by the selected principal components. SPE values are computed as the sum of squared residuals and follow established statistical distributions under normality assumptions [7]. Anomalies are identified using a threshold value calculated via the Jackson-Mudholkar approximation method at a 95 % confidence level. The number of principal components is fine-tuned to maximize the F1-score. 

- Shallow Machine Learning Baselines: 

- **PCA as a reconstructor (using reconstruction error):** PCA is applied for dimensionality reduction while preserving the essential variability of the data [51]. The reduced feature space is then used to reconstruct the time series, and reconstruction errors are calculated as anomaly scores. Anomalies are identified using a threshold set at the 95th percentile of the reconstruction error in the training dataset. The number of PCA components is optimized to maximize the F1-score. 

- **k-Nearest Neighbors (k-NN):** Euclidean distance is used as the similarity metric in k-NN due to its suitability for continuous attributes and computational efficiency [52]. Anomalies are detected by thresholding distances at the 95th percentile of the training set, while the number of neighbors (k) is fine-tuned to maximize the F1-score. 

- **OC-SVM (One-Class Support Vector Machine):** A One-Class SVM from the scikit-learn library [53] is used, with decision scores serving as anomaly scores and the 95th percentile of the training set as the anomaly threshold. The hyperparameters `nu' and `gamma' are optimized for the highest F1-score. 

- **IF (Isolation Forest):** The IF algorithm from the scikit-learn library [53] is employed, using decision scores as anomaly scores and the 95th percentile threshold. The contamination hyperparameter is tuned to maximize the F1-score. 

Deep Learning Baselines: 

- **CNN-LSTM prediction model:** This method [38] uses CNN layers to extract spatial features from the input data, followed by LSTM layers to capture the temporal dependency in the time-series data. Anomalies are detected by thresholding prediction errors at the 95th percentile of the training set. All hyperparameters, including the number of layers and units, learning rate, and dropout rates—were carefully tuned to maximize the F1 score, ensuring a fair comparison. 

- **Deep autoencoder:** A CNN-LSTM autoencoder, identical to the component used in our conformal anomaly detection method, is employed as a baseline model. For this conventional autoencoder baseline, the calibration set is excluded since conformal prediction is not applied. The anomaly detection threshold is set at the 95th percentile of the nonconformity scores computed from the training set. 

- **Graph Deviation Network (GDN):** A graph neural network-based anomaly detection method is included as a baseline, following the 

8 

> _S. Yuan et al.                                                                                                                                                                                                                                    Reliability Engineering and System Safety 274 (2026) 112417_ 


![](Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems_images/Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems.pdf-0009-01.png)


**Fig. 4.** Structure of the developed deep autoencoder. 

Graph Deviation Network (GDN) framework proposed by Deng and Hooi [54]. The GDN method explicitly models inter-sensor dependencies by learning a directed graph structure from multivariate time-series data. Using sensor embeddings and a graph attention mechanism, the model performs one-step-ahead forecasting for each sensor. Anomalies are identified by computing normalized prediction errors across sensors and aggregating them using the maximum function to produce an anomaly score for each time step. The anomaly detection threshold is set at the 95th percentile of the anomaly scores computed from the training set. All key hyperparameters—including embedding dimensions, number of graph neighbors, attention parameters, and network depth—were tuned to maximize the F1 score, ensuring a fair comparison with other baseline models. 

• **Deep Support Vector Data Description (DeepSVDD):** The DeepSVDD method combines deep neural networks with Support Vector Data Description to learn a hypersphere in the latent feature space that encloses normal samples [55]. We include an augmented DeepSVDD variant introduced by Peng et al. [45] in our comparison. This approach employs an autoencoder as a feature extractor to map input data into a latent representation and utilizes a joint optimization mechanism that simultaneously minimizes both the reconstruction error of the autoencoder and the hypersphere volume in the latent space, thereby resolving the hypersphere collapse issue observed in conventional DeepSVDD. The squared Euclidean distance between the latent feature representation of a test instance and the hypersphere center is employed as the anomaly score. The anomaly detection threshold is determined using the quantile method, specifically set at the 95th percentile of the anomaly scores computed from the training set. All hyperparameters, including network architecture, learning rate, and the number of training epochs, were carefully tuned to maximize the F1 score, ensuring a fair comparison. 

#### _4.3. Model evaluation_ 

The experiments are designed to demonstrate the proposed framework’s compatibility with various ML and DL models, as well as its ability to guarantee a user-specified false alarm rate. We begin our 

evaluation by comparing all baseline methods described in the previous section. Subsequently, we integrate the ML and DL baselines into our proposed conformal prediction framework, utilizing their respective anomaly scores as nonconformity scores for conformalized anomaly detection. This integration strategy enables us to systematically evaluate how the incorporation of conformal prediction impacts the performance of the ML- and DL-based anomaly detection models. 

To assess the performance of those methods, widely used metrics for binary classification are employed. These include Precision, Recall, F1Score, AUROC (Area Under the Receiver Operating Characteristic Curve), and False Positive Rate (also known as false alarm rate), as outlined below. 


![](Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems_images/Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems.pdf-0009-09.png)



![](Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems_images/Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems.pdf-0009-10.png)



![](Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems_images/Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems.pdf-0009-11.png)


where _TP_ represents true positives, which are correctly identified anomalies; _FP_ denotes false positives, referring to normal instances incorrectly classified as anomalies; and _FN_ refers to false negatives, which are anomalies incorrectly classified as normal. _TN_ represents true negatives, referring to normal instances correctly classified as normal. _FPR_ represents false positive rate. 

The AUROC (Area Under the Receiver Operating Characteristic Curve) assesses the performance of a classifier by quantifying the tradeoff between the true positive rate (Recall) and the false positive rate [56]. An AUROC value of 1 indicates perfect discrimination, whereas a value of 0.5 reflects performance equivalent to random guessing. It condenses the Receiver Operating Characteristic (ROC) curve into a single quantitative metric, providing a comprehensive evaluation of the model's performance across all classification thresholds. 

Table 2 summarizes the evaluation metrics for those methods. The 

9 

> _S. Yuan et al.                                                                                                                                                                                                                                    Reliability Engineering and System Safety 274 (2026) 112417_ 

##### **Table 2** 

Evaluation metrics for the methods included in the comparison. 

|Models|Precision|Recall|AUROC|F1|False alarm rate (_α_=0.05)|
|---|---|---|---|---|---|
|VAR<br>|0.7087±0.0133|0.7265±0.0431|0.8795±0.0357|0.7172±0.0273|0.0565|
|PCA (T<sup>2</sup>)|0.9270±0.0057|0.6637±0.0560|0.8802±0.0339|0.7724±0.0399|0.0246|
|PCA (SPE)|0.3508±0.0070|**0.9800±0.0298**|0.8960±0.0390|0.5167±0.0118|0.8595|
|PCA (reconstruction error)|0.8317±0.0100|0.7924±0.0558|0.8961±0.0390|0.8109±0.0342|0.0757|
|Conformal PCA|0.9726±0.0022|0.7259±0.0606|0.8961±0.0390|0.8300±0.0402|0.0096|
|k-NN|0.8648±0.0079|0.8000±0.0525|**0.9190±0.0358**|0.8305±0.0323|0.0591|
|Conformal k-NN|0.9707±0.0020|0.7883±0.0529|**0.9190±0.0358**|0.8691±0.0335|0.0112|
|OC-SVM|0.8855±0.0073|0.8006±0.0548|0.8858±0.0438|0.8401±0.0342|0.0489|
|Conformal OC-SVM|0.9494±0.0033|0.7685±0.0524|0.8858±0.0438|0.8486±0.0333|0.0193|
|Isolation Forest|0.8313±0.0139|0.5173±0.0509|0.8158±0.0336|0.6367±0.0428|0.0494|
|Conformal Isolation Forest|0.7943±0.0144|0.2734±0.0249|0.8158±0.0336|0.4063±0.0292|0.0334|
|CNN-LSTM|0.8831±0.0078|0.8054±0.0590|0.8978±0.0434|0.8416±0.0361|0.0503|
|Conformal CNN-LSTM|**0.9805±0.0013**|0.7450±0.0530|0.8978±0.0434|0.8457±0.0345|0.0070|
|GDN|0.9187±0.0044|0.7105±0.0426|0.8440±0.0487|0.8007±0.0285|0.0297|
|Conformal GDN|0.9597±0.0018|0.6989±0.0331|0.8440±0.0487|0.8084±0.0227|0.0139|
|DeepSVDD|0.8864±0.0070|0.7700±0.0521|0.8936±0.0331|0.8234±0.0332|0.0466|
|Conformal DeepSVDD|0.9508±0.0032|0.7422±0.0482|0.8936±0.0331|0.8328±0.0321|0.0181|
|Autoencoder|0.8811±0.0065|0.8038± 0.0475|0.9008±0.0336|0.8401±0.0294|0.0513|
|Conformal autoencoder|0.9759±0.0016|0.7889± 0.0529|0.9008±0.0336|**0.8716±0.0335**|0.0092|



best-performing model is highlighted in bold, while the second-best results are underlined. Fig. 5 compares the false alarm rates of different models against the target threshold of 0.05 ( _α_ = 0 _._ 05). Fig. 6 shows the impact of applying conformal prediction on the performance metrics of the original ML and DL models. 

As shown in Table 2, most ML and DL methods outperform the statistical baselines, with all obtaining F1 score above 0.8, except for Isolation Forest, which achieves an F1 score of 0.64 and fails to surpass the statistical baselines. The three statistical baselines obtain F1 scores of approximately 0.72 (VAR), 0.77 (PCA-T<sup>2</sup> ), and 0.52 (PCA-SPE), respectively. This indicates that most ML and DL baselines excel over the classical statistical baselines, as statistical methods have difficulties handling the complex high-dimensional spatial-temporal patterns present in the data. 

According to the comparison between ML and DL methods and their conformalized counterparts in Table 2 and Fig. 5, integrating conformal prediction into ML and DL methods significantly reduces the false alarm rate (FAR) while maintaining statistical validity under the predefined significance level of 0.05. This comparison clearly demonstrates the generalizability and effectiveness of the proposed framework. Specifically, the conformal autoencoder (CAE) achieves the highest F1-score (0.87) while ranking second in precision (0.98). Among baseline 

methods, PCA (SPE) and CNN-LSTM achieve the highest (0.98) and second-highest (0.81) recall, respectively. Meanwhile, conformal CNNLSTM secures the best precision (0.98), and conformal k-NN attains the highest AUROC (0.92) alongside the second-highest F1-score (0.87). Notably, AUROC values remain unchanged between baseline methods and their conformalized counterparts because this metric is thresholdindependent. Since conformal prediction primarily adjusts decision thresholds rather than altering model predictions, AUROC scores remain consistent across baseline and conformalized versions of the same method. 

Fig. 6 highlights that conformal prediction generally improves the F1-scores of most models, primarily driven by increases in precision. However, this improvement comes at the cost of slight drop in recall. This trade-off is seen in models such as PCA (reconstruction error), k- NN, OC-SVM, CNN-LSTM, GDN, DeepSVDD, and autoencoder. On the other hand, the integration of conformal prediction does not enhance the performance of the Isolation Forest (IF) model. This is due to IF's inherent tendency to produce overlapping anomaly scores for normal and anomalous data classes. Consequently, the stricter thresholds introduced by conformal prediction disproportionately exclude true positives, negatively impacting both Recall and Precision. This trade-off underscores the balance between FAR guarantees and detection 


![](Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems_images/Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems.pdf-0010-09.png)


**Fig. 5.** Comparison of false alarm (false positive) rate with and without conformal prediction. 

10 

> _S. Yuan et al.                                                                                                                                                                                                                                    Reliability Engineering and System Safety 274 (2026) 112417_ 


![](Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems_images/Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems.pdf-0011-01.png)


**Fig. 6.** Impact assessment of conformal prediction on the model performance. 

capability, with the conformal approach prioritizing false alarm control over other performance criteria in certain models. In practice, models capable of capturing complex spatiotemporal dependencies and pro— ducing well-separated anomaly scores such as deep learning archi— tectures like autoencoders, CNN-LSTM, GDN, and DeepSVDD integrate particularly well with conformal prediction pipelines. The strong separation these methods achieve between normal and anomalous instances enables conformal prediction to effectively enhance their overall performance. 

#### **5. Robust guarantee on false alarm rates** 

This section evaluates and discusses the robustness of the proposed method in providing a statistical guarantee on a wide range of predefined false alarm rates. We conducted the evaluation by comparing the proposed method against several conventional methods that aim to achieve the same objective, but fail to provide valid statistical guarantees. Specifically, two PCA-based approaches are included in the comparison: one using Hotelling’s T² and the other using Q-statistics (also known as the Squared Prediction Error, SPE) as anomaly detection indices for thresholding anomalies [7]. These methods are widely adopted in practice [57] and are capable of controlling false alarm rates under specific assumptions, such as linearly correlated Gaussian data, making them suitable baselines for comparison. Additionally, the quantile method, a widely used and straightforward approach, is also evaluated. This method determines anomaly thresholds based on the quantile value of anomaly scores [55]. 

To understand the role of Conformal Prediction (CP) and Temporal Quantile Adjustment (TQA) in guaranteeing false alarm rates (FAR), we 

include four distinct anomaly thresholding schemes based on the same autoencoder: (i) determining the threshold based on the quantile of anomaly scores from the training set; (ii) determining the threshold based on the quantile of anomaly scores from an independent validation set (of the same size as the calibration set in CP); (iii) using the conventional conformal prediction method without TQA-B or a sliding calibration set; and (iv) our proposed method, which combines conformal prediction with TQA-B for adaptive thresholding. This comparison enables us to isolate and evaluate the specific impact of TQA-B on the overall framework. 

The experiments were conducted using two schemes with different proportions of normal data in the test sets: one with 10 % of total normal data and another with 25 % of total normal data. Computational results comparing metrics such as precision, recall, AUROC, F1-score, and FAR, are summarized in Table 3. The evaluations were performed at predefined targeted FAR/significance levels ranging from 0.01 to 0.1. In Table 3, cases that successfully meet the target FAR levels are marked in bold. Furthermore, Fig. 7 presents a comparison of FAR compliance across the different methods, showcasing the effectiveness of each method in guaranteeing pre-defined FARs. 

As observed in Table 3 and Fig. 7, both PCA (T<sup>2</sup> ) and PCA (SPE) demonstrate an inconsistent performance in guaranteeing FARs when the target FAR values vary. Thresholding methods based on quantiles derived from the validation set and the calibration set using the conventional conformal prediction (CP) method perform better than those relying on thresholds determined from the training set. This is primarily because the use of an independent dataset (separate from the training data) avoids overfitting to the training distribution and provides a more accurate reflection of unseen data. However, when the test set is 

11 

> _S. Yuan et al.                                                                                                                                                                                                                                    Reliability Engineering and System Safety 274 (2026) 112417_ 

##### **Table 3** 

Comparison of different anomaly thresholding methods at different significance levels. 

|Models|Pre-<br>|Scheme 1 (|10 % normal d|ata for testing)|||Scheme 2 (|25 % normal d|ata for testing|)||
|---|---|---|---|---|---|---|---|---|---|---|---|
||defned<br>FAR|Precision|Recall|AUROC|F1|Actual<br>FAR|Precision|Recall|AUROC|F1|Actual<br>FAR|
|PCA (T²)|0.1|0.9284|0.6800|0.8802|0.7837|**0.0247**|0.8359|0.6800|0.8797|0.7489|**0.0252**|
|||±0.0059|±0.0609|±0.0339|±0.0424||±0.0121|±0.0609|±0.0340|±0.0416||
||0.08|0.9282|0.6753|0.8802|0.7806|**0.0246**|0.8354|0.6753|0.8797|0.7459|**0.0251**|
|||±0.0057|±0.0586|±0.0339|±0.0410||±0.0118|±0.0586|±0.0340|±0.0403||
||0.05|0.9270|0.6637|0.8802|0.7724|**0.0246**|0.8331|0.6637|0.8797|0.7379|**0.0251**|
|||±0.0057|±0.0560|±0.0339|±0.0399||±0.0117|±0.0560|±0.0340|±0.0392||
||0.02|0.9272|0.6538|0.8802|0.7656|0.0242|0.8329|0.6538|0.8797|0.7316|0.0247|
|||±0.0061|±0.0583|±0.0339|±0.0422||±0.0125|±0.0583|±0.0340|±0.0414||
||0.01|0.9272|0.6538|0.8802|0.7656|0.0242|0.8329|0.6538|0.8797|0.7316|0.0247|
|||±0.0061|±0.0583|±0.0339|±0.0422||±0.0125|±0.0583|±0.0340|±0.0414||
|PCA (SPE)|0.1|0.3216|1.0000|0.8960|0.4867|1.0000|0.1922|0.9581|0.8950|0.3202|0.7633|
|||±0.0000|±0.0000|±0.0390|±0.0000||±0.0084|±0.0515|±0.0386|±0.0146||
||0.08|0.3256|0.9992|0.8960|0.4911|0.9813|0.2311|0.9182|0.8950|0.3692|0.5789|
|||±0.0008|±0.0036|±0.0390|±0.0013||±0.0124|±0.0636|±0.0386|±0.0210||
||0.05|0.3508|0.9800|0.8960|0.5167|0.8595|0.5932|0.8104|0.8950|0.6847|0.1051|
|||±0.0070|±0.0298|±0.0390|±0.0118||±0.0164|±0.0530|±0.0386|±0.0301||
||0.02|0.7597|0.8008|0.8960|0.7790|0.1195|1.0000|0.6294|0.8950|0.7723|**0.0000**|
|||±0.0143|±0.0631|±0.0390|±0.0373||±0.0000|±0.0256|±0.0386|±0.0189||
||0.01|0.9842|0.7000|0.8960|0.8166|**0.0053**|1.0000|0.6126|0.8950|0.7598|**0.0000**|
|||±0.0014|±0.0615|±0.0390|±0.0422||±0.0000|±0.0000|±0.0386|±0.0000||
|AE with quantile method|0.1|0.8003|0.8104|0.9008|0.8050|**0.0957**|0.5767|0.8104|0.8970|0.6737|0.1126|
|on training set||±0.0087|±0.0432|±0.0336|±0.0259||±0.0132|±0.0432|±0.0341|±0.0240||
||0.08|0.8294|0.8089|0.9008|0.8186|**0.0787**|0.6241|0.8089|0.8970|0.7044|0.0922|
|||±0.0081|±0.0450|±0.0336|±0.0273||±0.0133|±0.0450|±0.0341|±0.0257||
||0.05|0.8811|0.8038|0.9008|0.8401|0.0513|0.7199|0.8038|0.8970|0.7592|0.0592|
|||±0.0065|±0.0475|±0.0336|±0.0294||±0.0123|±0.0475|±0.0341|±0.0283||
||0.02|0.9459|0.7920|0.9008|0.8613|0.0214|0.8654|0.7920|0.8970|0.8264|0.0233|
|||±0.0035|±0.0528|±0.0336|±0.0332||±0.0080|±0.0528|±0.0341|±0.0328||
||0.01|0.9750|0.7892|0.9008|0.8714|**0.0096**|0.9349|0.7892|0.8970|0.8551|0.0104|
|||±0.0017|±0.0530|±0.0336|±0.0336||±0.0042|±0.0530|±0.0341|±0.0335||
|AE with quantile method|0.1|0.8202|0.8095|0.9008|0.8144|**0.0839**|0.5848|0.8102|0.8970|0.6791|0.1089|
|on an independent||±0.0083|±0.0444|±0.0336|±0.0268||±0.0133|±0.0435|±0.0341|±0.0243||
|validation set|0.08|0.8530|0.8070|0.9008|0.8288|**0.0658**|0.6555|0.8076|0.8970|0.7234|0.0803|
|||±0.0075|±0.0466|±0.0336|±0.0285||±0.0133|±0.0461|±0.0341|±0.0268||
||0.05|0.8999|0.8010|0.9008|0.8469|**0.0421**|0.7501|0.8015|0.8970|0.7746|0.0505|
|||±0.0056|±0.0480|±0.0336|±0.0298||±0.0116|±0.0480|±0.0341|±0.0289||
||0.02|0.9505|0.7915|0.9008|0.8628|**0.0195**|0.8673|0.7919|0.8970|0.8272|0.0229|
|||±0.0033|±0.0533|±0.0336|±0.0336||±0.0080|±0.0530|±0.0341|±0.0330||
||0.01|0.9763|0.7890|0.9008|0.8718|**0.0090**|0.9341|0.7893|0.8970|0.8547|0.0105|
|||±0.0016|±0.0530|±0.0336|±0.0336||±0.0043|±0.0531|±0.0341|±0.0335||
|Conformal AE without|0.1|0.8202|0.8095|0.9008|0.8144|**0.0839**|0.5852|0.8100|0.8970|0.6794|0.1087|
|TQA||±0.0083|±0.0444|±0.0336|±0.0268||±0.0133|±0.0437|±0.0341|±0.0244||
||0.08|0.8531|0.8070|0.9008|0.8289|**0.0657**|0.6557|0.8076|0.8970|0.7235|0.0802|
|||±0.0075|±0.0466|±0.0336|±0.0285||±0.0133|±0.0461|±0.0341|±0.0268||
||0.05|0.9001|0.8010|0.9008|0.8470|**0.0420**|0.7510|0.8015|0.8970|0.7750|0.0503|
|||±0.0056|±0.0480|±0.0336|±0.0298||±0.0116|±0.0480|±0.0341|±0.0289||
||0.02|0.9505|0.7915|0.9008|0.8628|**0.0195**|0.8677|0.7918|0.8970|0.8273|0.0228|
|||±0.0033|±0.0533|±0.0336|±0.0336||±0.0080|±0.0531|±0.0341|±0.0330||
||0.01|0.9763|0.7890|0.9008|0.8718|**0.0090**|0.9351|0.7892|0.8970|0.8551|0.0103|
|||±0.0016|±0.0530|±0.0336|±0.0336||±0.0042|±0.0530|±0.0341|±0.0335||
|Conformal AE with TQA|0.1|0.9513|0.7912|0.9008|0.8630|**0.0191**|0.8691|0.7906|0.8970|0.8273|**0.0225**|
|||±0.0032|±0.0532|±0.0336|±0.0335||±0.0080|±0.0534|±0.0341|±0.0333||
||0.08|0.9641|0.7906|0.9008|0.8678|**0.0139**|0.8959|0.7900|0.8970|0.8388|**0.0173**|
|||±0.0024|±0.0535|±0.0336|±0.0338||±0.0065|±0.0535|±0.0341|±0.0335||
||0.05|0.9759|0.7889|0.9008|0.8716|**0.0092**|0.9287|0.7886|0.8970|0.8521|**0.0114**|
|||±0.0016|±0.0529|±0.0336|±0.0335||±0.0046|±0.0530|±0.0341|±0.0334||
||0.02|0.9920|0.7877|0.9008|0.8771|**0.0030**|0.9710|0.7876|0.8970|0.8688|**0.0044**|
|||±0.0006<br>|±0.0531<br>|±0.0336<br>|±0.0338<br>||±0.0020<br>|±0.0531<br>|±0.0341<br>|±0.0337<br>||
||0.01|0.9976|0.7873|0.9008|0.8791|**0.0009**|0.9887|0.7874|0.8970|0.8756|**0.0017**|
|||±0.0002|±0.0531|±0.0336|±0.0338||±0.0008|±0.0531|±0.0341|±0.0338||



expanded in the second scheme (with larger proportions of normal data), both the quantile-based method on the validation set and the conformal autoencoder (CAE) without TQA fail to consistently meet the FAR guarantees. In contrast, our proposed method (CAE with TQA) is the only approach that consistently satisfies all the target FAR guarantees across all tests. This result underscores the necessity and effectiveness of implementing TQA, as it enhances the robustness of CP by dynamically adjusting to temporal and distributional changes within the data. Moreover, the CAE with TQA is the only method that achieves F1- 

scores above 0.8 across all test scenarios, emphasizing its potential as an adaptive thresholding method for anomaly detection. This demonstrates not only its ability to provide robust FAR guarantees but also its effectiveness in improving anomaly detection performance. By balancing precision and recall while ensuring compliance with predefined FAR levels, CAE with TQA presents itself as a reliable and practical solution for adaptive anomaly detection in ICPS environments. 

12 

> _S. Yuan et al.                                                                                                                                                                                                                                    Reliability Engineering and System Safety 274 (2026) 112417_ 


![](Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems_images/Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems.pdf-0013-01.png)


**Fig. 7.** Comparison of false alarm rate compliance across different anomaly detection methods. 

#### **6. Sample rejection mechanism for sliding calibration set** 

The trade-off between detection capability (as measured by recall) and false alarm rate (FAR) is inherent to anomaly detection tasks, where achieving a lower FAR typically comes at the expense of reduced anomaly detection performance. This study aims to provide statistical guarantees on pre-specified FAR levels while accommodating temporal distribution shifts in time-series data. To this end, we propose a Temporal Quantile Adjustment (TQA) method with a sliding calibration set. However, anomalous test instances inevitably contaminate this calibration set during real-time deployment. While this does not compromise the FAR guarantees in practice, it can degrade the detector's anomaly detection capability, particularly when a large number of anomalous instances exist in the data stream. Therefore, a rejection mechanism is introduced and applied to the sliding calibration set operation within the CP pipeline, as detailed in Eqs. (20) and (21). This rejection mechanism excludes clearly anomalous data from the sliding calibration set, while retaining in-distribution and mildly anomalous data, thereby improving the balance between maintaining FAR guarantees and preserving detection sensitivity. Notably, the conformal prediction framework operates as a standalone post-processing thresholding method that is compatible with any anomaly detector. While it provides robust FAR guarantees, achieving strong recall fundamentally depends on the quality of the underlying detector. Conformal prediction calibrates decision thresholds for guaranteed FAR control, but does not enhance the detector's inherent discriminative ability. Therefore, strong recall requires a capable base detector, while our framework ensures a 

reliable FAR control. Practitioners can explicitly balance these objectives by adjusting the significance level α according to applicationspecific priorities. 

To assess the impact of this rejection mechanism, we artificially introduced additional anomalous instances into the test set and compared our proposed method (with the rejection mechanism) to the same method without it. The confusion matrices for both methods are shown in Fig. 8, while Fig. 9 presents the evaluation metrics for them. As shown in Fig. 8, implementing the rejection mechanism does not affect — false positives or true negatives the first rows of both confusion matrices are identical. However, it improves model performance by increasing true positives and reducing false negatives. This is consistent with the evaluation metrics in Fig. 9, which show that the method without the rejection mechanism struggles to detect many anomalies. In contrast, incorporating the rejection mechanism significantly enhances anomaly detection, especially when a large portion of highly anomalous data is present. At the same time, it maintains false alarm rate (FAR) guarantees, as demonstrated by the identical FAR values with and without the mechanism. These results underscore the rejection mechanism’s effectiveness in improving conformal anomaly detection performance while preserving reliable FAR guarantees. 

#### **7. Anomaly monitoring indicators** 

Targeting the limitations of conventional raw anomaly scores, such as mean squared error (MSE), we investigate how P-value based indicators derived from conformal prediction can offer a novel quantita- 


![](Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems_images/Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems.pdf-0013-09.png)


**Fig. 8.** Comparison of confusion matrices with and without the anomaly rejection mechanism applied to the sliding calibration set. 

13 

> _S. Yuan et al.                                                                                                                                                                                                                                    Reliability Engineering and System Safety 274 (2026) 112417_ 


![](Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems_images/Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems.pdf-0014-01.png)


**Fig. 9.** Comparison of evaluation metrics with and without the anomaly rejection mechanism applied to the sliding calibration set. 

tive measure of the degree of anomalousness for test instances in realtime deployment. Raw anomaly scores have significant drawbacks: their magnitude may vary significantly even among normal instances, and they do not directly reflect how anomalous a test instance is relative to normal instances. To address those limitations, we compare three indicators for real-time anomaly monitoring (results shown in Fig. 10): i) – raw anomaly scores (MSE), ii) 1 P-value with P-value calculated using Eq. (13), and iii) –log(P-value ratio), which is calculated as follows: 


![](Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems_images/Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems.pdf-0014-04.png)


where _Ptest, t_ and _Pthreshold, t_ represent the P-values of the test instance and the anomaly detection threshold at time _t_ , respectively. 

As shown in Fig. 10, the green and red shaded areas represent the true normal and anomalous regimes for the test instances, respectively. As seen in Fig. 10(a), the raw anomaly score (MSE) varies widely in magnitude, with both false positives (marked by red crosses) and false negatives (black circles) clustering within a similar value range, making it difficult to effectively differentiate the degree of anomalousness among those instances. By contrast, P-value based metrics effectively scale raw anomaly scores (MSE) into an appropriate range for easier anomaly monitoring and comparison. The 1–P-value metric demonstrates the capability to distinguish differences in anomaly severity among false positives, as shown in Fig. 10(b). Meanwhile, the –log(Pvalue ratio) clearly distinguishes between false positives and false negatives and their respective anomaly severities, as illustrated in Fig. 10 (c). Therefore, these P-value based approaches capture granular anomaly trends over time, and provide nuanced insights into fluctuations in the data behavior that may be obscured by raw scores alone. Additionally, P-value-based metrics offer a statistically meaningful measure of anomalousness for individual data instances with enhanced robustness and interpretability. The P-value derived from conformal prediction indicates the likelihood that a test instance belongs to the indistribution (normal) data by utilizing an independent calibration set for its calculation. In practical industrial settings, P-value-based indicators can be integrated into intuitive visualization and decisionsupport systems to translate statistical measures into actionable insights for operators. These systems reflect the degree of anomalousness for each data instance and capture anomalous trends in time series, enabling real-time anomaly monitoring and providing valuable operational insights. 

Furthermore, our proposed method is exceptionally well-suited for real-time deployment in industrial SCADA systems due to its computational efficiency. The CP framework eliminates the need for model 

retraining during deployment by requiring only incremental updates to the calibration set via a sliding window mechanism rather than model recalibration from scratch at each time step. This lightweight computational approach enables its deployment on resource-constrained industrial hardware while maintaining sub-second response times. Our computational efficiency analysis validates this real-time feasibility with a mean inference time of 98.96 ms with 99th percentile latency below 137.97 ms, resulting in a throughput of over 10.1 samples per second. These performance metrics were achieved on standard commodity hardware (Intel i7-10510U @ 1.80–2.30 GHz, 16 GB RAM) using integrated graphics and no GPU acceleration, demonstrating the method's accessibility for typical industrial computing environments. 

#### **8. Conclusion** 

This study investigates anomaly detection in industrial cyberphysical systems, with a particular focus on addressing the challenges of guaranteeing false alarm rates (FAR). We propose a novel framework that integrates machine learning methods with a conformal prediction pipeline, incorporating a Temporal Quantile Adjustment (TQA) method to accommodate distribution shifts in time-series data. The framework has been evaluated using several machine learning and deep learning models, with the integration of a deep autoencoder detailed as an example. The deep autoencoder achieves the best performance in terms of F1 score while providing robust guarantees on FAR. Comparisons with conventional anomaly thresholding approaches reveal that the proposed conformal prediction framework consistently delivers robust guarantees on a range of pre-defined FAR levels, outperforming other methods. For industrial cyber-physical system applications, successful implementation of this framework requires a well-trained machine learning model with the capability to capture complex spatiotemporal features in time-series data and effectively separate normal from anomalous data using anomaly scores. Then, the integration of the conformal machine learning framework further enhances anomaly detection performance by balancing FAR guarantees and detection capabilities, thereby improving the overall system performance. 

#### **CRediT authorship contribution statement** 

**Shuaiqi Yuan:** Writing – original draft, Visualization, Methodology, Investigation, Conceptualization. **Jipu Li:** Visualization, Validation, Formal analysis. **Chunjin Wang:** Writing – review & editing. **Xiaoge Zhang:** Writing – review & editing. 

14 

> _S. Yuan et al.                                                                                                                                                                                                                                    Reliability Engineering and System Safety 274 (2026) 112417_ 


![](Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems_images/Conformal_machine_learning_for_reliable_anomaly_detection_in_industrial_cyber-physical_systems.pdf-0015-01.png)


**Fig. 10.** Comparison of different indicators for anomaly monitoring. 

15 

> _S. Yuan et al.                                                                                                                                                                                                                                    Reliability Engineering and System Safety 274 (2026) 112417_ 

#### **Declaration of competing interest** 

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper. 

#### **Acknowledgments** 

This work was supported in part by a grant from the National Science Foundation of China (Grant No. 62406269), the Research Grants Council of the Hong Kong Special Administrative Region (Project No. PolyU 25206422), China, and the funding support to the State Key Laboratories in Hong Kong from the Innovation and Technology Commission (ITC) of the Government of the Hong Kong Special Administrative Region (HKSAR), China. The authors would also like to express their sincere thanks to the financial support from the Research and Innovation Office (Project code: BBRC) of The Hong Kong Polytechnic University. The dataset and souorce codes related to this paper are available at the GitHub repository: https://github.com/Yuan-shuaiqi/c onformal-autoencoder-anomaly-detection/. 

#### **Data availability** 

Data will be made available on request. 

#### **References** 

- [1] Bolbot V, Theotokatos G, Bujorianu LM, Boulougouris E, Vassalos D. Vulnerabilities and safety assurance methods in Cyber-Physical Systems: a comprehensive review. Reliab Eng Syst Saf 2019;182:179–93. 

- [2] Yuan S, Reniers G, Yang M. Integrated management of safety and security barriers in chemical plants to cope with emerging cyber-physical attack risks under uncertainties. Reliab Eng Syst Saf 2024;250:110320. 

- [3] Monzer MH, Beydoun K, Ghaith A, Flaus JM. Model-based IDS design for ICSs. Reliab Eng Syst Saf 2022;225:108571. 

- [4] Iliopoulos A, Violos J, Diou C, Varlamis I. Detection of anomalies in multivariate time series using ensemble techniques. In: 2023 _IEEE Ninth international conference on big data computing service and applications (BigDataService)_ . IEEE; 2023. p. 1–8. 

- [5] Akouemo HN, Povinelli RJ. Time series outlier detection and imputation. In: 2014 _IEEE PES General meeting| conference & exposition_ . IEEE; 2014. p. 1–5. 

- [6] Camacho J, P´erez-Villegas A, García-Teodoro P, Maci´a-Fernandez G. PCA-based ´ multivariate statistical network monitoring for anomaly detection. Comput Secur 2016;59:118–37. 

[7] Hashim H, Ryan P, Clifford E. A statistically based fault detection and diagnosis approach for non-residential building water distribution systems. Adv Eng Inform 2020;46:101187. 

- [8] Schmidl S, Wenig P, Papenbrock T. Anomaly Detection in Time Series: A Comprehensive Evaluation. Proce of the VLDB Endowment 2022;15(9):1779–97. 

- [9] Zamanzadeh Darban Z, Webb GI, Pan S, Aggarwal C, Salehi M. Deep learning for time series anomaly detection: a survey. ACM Comput Surv 2024;57(1):1–42. 

[10] Gulzar Q, Mustafa K. Interdisciplinary framework for cyber-attacks and anomaly detection in industrial control systems using deep learning. Sci Rep 2025;15(1): 26575. 

[11] Shang W, Qiu J, Shi H, Wang S, Ding L, Xiao Y. An efficient anomaly detection method for industrial control systems: deep convolutional autoencoding transformer network. Int J Intell Syst 2024;1:5459452. 

[12] Anton SDD, Sinha S, Schotten HD. Anomaly-based intrusion detection in industrial data with SVM and random forests. In: 2019 _International Conference on software, telecommunications and computer networks (SoftCOM)_ . IEEE; 2019. p. 1–6. 

- [13] Panja S, Patowary N, Saha S, Nag A. Anomaly detection in iot using extended isolation forest. In: International symposium on artificial intelligence. Cham: Springer Nature Switzerland; 2022. p. 3–14. 

- [14] Pandey P. A KNN-based intrusion detection system for enhanced anomaly detection in Industrial IoT networks. Int J Innov Res Technol Sci 2024;12(6):1–7. 

- [15] Choi K, Yi J, Park C, Yoon S. Deep learning for anomaly detection in time-series data: review, analysis, and guidelines. IEEE Access 2021;9:120043–65. 

- [16] Kang J, Lv K, Sun Y, Li M. Predictive risk assessment framework for leakage accident of offshore LNG transfer system. Expert Syst Appl 2025;271:126580. 

- [17] Kravchik M, Shabtai A. Detecting cyber attacks in industrial control systems using convolutional neural networks. In: Proceedings of the 2018 workshop on cyberphysical systems security and privacy; 2018. p. 72–83. 

[18] Perales Gomez ´ AL, Fern<sup>´</sup> andez Maim´ o L, Huertas Celdr´ ´an A, García Clemente FJ. Madics: a methodology for anomaly detection in industrial control systems. Symmetry 2020;12(10):1583. 

[19] Li D, Chen D, Jin B, Shi L, Goh J, Ng S-K. MAD-GAN: multivariate anomaly detection for time series data with generative adversarial networks. In: International conference on artificial neural networks. Cham: Springer International Publishing; 2019. p. 703–16. 

[20] Hu D, Zhang C, Yang T, Fang Q. A deep autoencoder with structured latent space for process monitoring and anomaly detection in coal-fired power units. Reliab Eng Syst Saf 2025;261:111060. 

- [21] Liu S, Chen J, Liu Z, Wang J, Wang ZJ. Graph embedded patch-sense autoencoder with prior knowledge for multi-component system anomaly detection. Reliab Eng Syst Saf 2025;256:110784. 

- [22] Zhou H, Wang B, Zio E, Lei Z, Wen G, Chen X. Unsupervised anomaly detection of machines operating under time-varying conditions: DCD-VAE enabled feature disentanglement of operating conditions and states. Reliab Eng Syst Saf 2025;256: 110653. 

- [23] Wu Y, Dai HN, Tang H. Graph neural networks for anomaly detection in industrial Internet of Things. IEEE Internet Things J. 2021;9(12):9214–31. 

- [24] Zhao H, Wang Y, Duan J, Huang C, Cao D, Tong Y, Zhang Q. Multivariate timeseries anomaly detection via graph attention network. In: 2020 IEEE International conference on data mining (ICDM). IEEE; 2020. p. 841–50. 

- [25] Zhang Y, Chen Y, Wang J, Pan Z. Unsupervised deep anomaly detection for multisensor time-series signals. IEEE Trans Knowl Data Eng 2021;35(2):2118–32. 

- [26] Guo C, Pleiss G, Sun Y, Weinberger KQ. On calibration of modern neural networks. In: International conference on machine learning. PMLR; 2017. p. 1321–30. 

- [27] Yang T, Qiao Y, Lee B. Towards trustworthy cybersecurity operations using Bayesian Deep Learning to improve uncertainty quantification of anomaly detection. Comput Secur 2024;144:103909. 

[28] Nemani V, Biggio L, Huan X, Hu Z, Fink O, Tran A, Hu C. Uncertainty quantification in machine learning for engineering design and health prognostics: a tutorial. Mech Syst Signal Process 2023;205:110796. 

- [29] Yong BX, Brintrup A. Bayesian autoencoders with uncertainty quantification: towards trustworthy anomaly detection. Expert Syst Appl 2022;209:118196. 

- [30] Vovk V, Gammerman A, Shafer G. Algorithmic learning in a random world, Vol. 

   29. New York: Springer; 2005. 

[31] Angelopoulos, A.N., & Bates, S. (2021). A gentle introduction to conformal prediction and distribution-free uncertainty quantification. arXiv preprint arXiv:2 107.07511. 

[32] Laxhammar R, Falkman G. Conformal prediction for distribution-independent anomaly detection in streaming vessel data. In: Proceedings of the first international workshop on novel data stream pattern mining techniques; 2010. p. 47–55. 

- [33] Laxhammar R. Conformal anomaly detection: detecting abnormal trajectories in ¨ surveillance applications. University of Skovde; 2014. Doctoral dissertation. 

- [34] Saboury A, Uyguroglu MK. Uncertainty-aware real-time visual anomaly detection with conformal prediction in dynamic indoor environments. IEEE Robot Autom Lett 2025;10(5):4468–75. 

- [35] Xu C, Xie Y. Conformal prediction for time series. IEEE Trans Pattern Anal Mach Intell 2023;45(10):11575–87. 

- [36] Lin Z, Trivedi S, Sun J. Conformal prediction with temporal quantile adjustments. Adv Neural Inf Process Syst 2022;35:31017–30. 

[37] Zhang R, Zhou P. Uncertainty quantification based on conformal prediction for industrial time series with distribution shift. IEEE Trans Ind Inform 2025;21(5): 3676–85. 

- [38] Abdallah M, An Le Khac N, Jahromi H, Delia Jurcut A. A hybrid CNN-LSTM based approach for anomaly detection systems in SDNs. In: Proceedings of the 16th international conference on availability, reliability and security; 2021. p. 1–7. 

[39] Yan S, Shao H, Min Z, Peng J, Cai B, Liu B. FGDAE: a new machinery anomaly detection method towards complex operating conditions. Reliab Eng Syst Saf 2023; 236:109319. 

[40] Zhang C, Song D, Chen Y, Feng X, Lumezanu C, Cheng W, Chawla NV. A deep neural network for unsupervised anomaly detection and diagnosis in multivariate time series data. Proc AAAI Conf Artif Intell 2019;33(01):1409–16. 

- [41] Bergman, L., Cohen, N., & Hoshen, Y. (2020). Deep nearest neighbor anomaly detection. arXiv preprint arXiv:2002.10445. 

- [42] Lee H, Kim NW, Lee JG, Lee BT. A study on distance measure for effective anomaly detection using AutoEncoder. In: 2020 International conference on information and communication technology convergence (ICTC). IEEE; 2020. p. 1348. 

- [43] Kwak BI, Han ML, Kim HK. Cosine similarity based anomaly detection methodology for the CAN bus. Expert Syst Appl 2021;166:114066. 

- [44] Hojjati H, Armanfard N. DASVDD: deep autoencoding support vector data descriptor for anomaly detection. IEEE Trans Knowl Data Eng 2023;36(8): 3739–50. 

[45] Peng D, Desmet W, Gryllias K. Reconstruction-based deep unsupervised adaptive threshold support vector data description for wind turbine anomaly detection. Reliab Eng Syst Saf 2025;260:110995. 

- [46] Fan C, Xiao F, Zhao Y, Wang J. Analytical investigation of autoencoder-based methods for unsupervised anomaly detection in building energy data. Appl Energy 2018;211:1123–35. 

- [47] Laso PM, Brosset D, Puentes J. Dataset of anomalies and malicious acts in a cyberphysical subsystem. Data Br 2017;14:186–91. 

- [48] Tsai DM, Jen PH. Autoencoder-based anomaly detection for surface defect inspection. Adv Eng Inform 2021;48:101272. 

- [49] Hsieh RJ, Chou J, Ho CH. Unsupervised online anomaly detection on multivariate sensing time series data for smart manufacturing. In: 2019 IEEE 12th Conference on service-oriented computing and applications (SOCA). IEEE; 2019. p. 90–7. 

- [50] Abbracciavento F, Formentin S, Balocco J, Rota A, Manzoni V, Savaresi SM. Anomaly detection via distributed sensing: a VAR modeling approach. IFACPapersOnLine 2021;54(7):85–90. 

- [51] Dani SK, Thakur C, Nagvanshi N, Singh G. Anomaly detection using PCA in time series data. In: 2024 IEEE International conference on interdisciplinary approaches 

16 

_S. Yuan et al.                                                                                                                                                                                                                                    and_ 

_Reliability Engineering and System Safety 274 (2026) 112417_ 

in technology and management for social innovation (IATMSI). 2. IEEE; 2024. p. 1–6. 

- [52] Zhao M, Chen J, Li Yang. A review of anomaly detection techniques based on nearest neighbor. In: Proceedings of the 2018 international conference on computer modeling, simulation and algorithm. CMSA; 2018. https://doi.org/ 10.2991/cmsa-18.2018.65. 

- [53] Scikit, ”2.7. Novelty and outlier detection.” Accessed February 27, 2025. https://scikit-learn.org/stable/modules/outlier_detection.html#. 

- [54] Deng A, Hooi B. Graph neural network-based anomaly detection in multivariate time series. In: Proceedings of the AAAI conference on artificial intelligence. 35; 2021. p. 4027–35. 

- [55] Ruff L, Vandermeulen R, Goernitz N, Deecke L, Siddiqui SA, Binder A, Kloft M. Deep one-class classification. In: International conference on machine learning. PMLR; 2018. p. 4393–402. 

- [56] Bradley AP. The use of the area under the ROC curve in the evaluation of machine learning algorithms. Pattern Recognit 1997;30(7):1145–59. 

- [57] Li W, Peng M, Wang Q. False alarm reducing in PCA method for sensor fault detection in a nuclear power plant. Ann Nucl Energy 2018;118:131–9. 

17 

