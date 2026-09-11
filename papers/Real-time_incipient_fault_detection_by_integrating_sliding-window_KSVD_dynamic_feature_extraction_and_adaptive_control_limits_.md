Journal of the Franklin Institute 363 (2026) 109034 


![](Real-time_incipient_fault_detection_by_integrating_sliding-window_KSVD_dynamic_feature_extraction_and_adaptive_control_limits__images/conv_1eabdae0f26ef3eb.pdf-0001-01.png)


Contents lists available at ScienceDirect of the Franklin journal homepage: www.elsevier.com/locate/fi 

# Journal of the Franklin Institute 


![](Real-time_incipient_fault_detection_by_integrating_sliding-window_KSVD_dynamic_feature_extraction_and_adaptive_control_limits__images/conv_1eabdae0f26ef3eb.pdf-0001-04.png)


## Real-time incipient fault detection by integrating sliding-window KSVD dynamic feature extraction and adaptive control limits 


![](Real-time_incipient_fault_detection_by_integrating_sliding-window_KSVD_dynamic_feature_extraction_and_adaptive_control_limits__images/conv_1eabdae0f26ef3eb.pdf-0001-06.png)


### Zhu Wang<sup>a</sup> , Jianqiao Zhou a,∗, Decheng Liu b 

a _Department of Automation, College of Artificial Intelligence, China University of Petroleum Beijing, No.18 Fuxue Road, Changping District, Beijing, 102249, China_ 

b _People’s Government of Nanjing, No. 41, East Beijing Road, Nanjing, 210008, Jiangsu Province, China_ 

|a r t i c l e i n f o|a b s t r a c t|
|---|---|
|_Keywords:_<br>|Accurate real-time fault detection is crucial for the safe operation of industrial processes. How-|
|Incipient fault detection<br>Data stream<br>Kernel singular value<br>Adaptive control limits|ever, the timely identifcation of incipient faults remains a major challenge. This paper proposes<br>a real-time incipient fault detection method with two key features. First, key dynamic process<br>features, namely singular values, are extracted in real time from sliding windows of data streams<br>using Kernel Singular Value Decomposition (KSVD). Specifcally, the sliding-window data matrix<br>is frst mapped into a high-dimensional feature space through a kernel function, and then SVD-<br>based feature extraction is performed. The extracted features directly refect the real-time process<br>states and dynamic variations. Second, a novel adaptive control limit (ACL) mechanism is devel-<br>oped for real-time incipient fault detection. This mechanism uses the extracted kernel singular<br>values as the monitoring statistics and explicitly accounts for the intrinsic temporal correlations<br>in industrial data. As a result, the control limit can be dynamically updated to accommodate<br>normal process variations. Simulation and industrial case studies demonstrate the efectiveness<br>of the proposed method. By combining dynamic feature extraction with adaptive control limits,<br>the proposed method can reliably detect early-stage incipient faults in real-time data streams and<br>shows superior sensitivity and adaptability compared with conventional approaches.|



#### **1. Introduction** 

With the continuous expansion of the modern petrochemical industry, ensuring its safe and efficient operation has become a major challenge [1–5]. Refining and chemical plants are indispensable components of the petrochemical industry. Owing to the complexity of refining and chemical processes and their reliance on a large number of sensors, the number of internal control loops and process parameters increases significantly, thereby increasing the probability of fault occurrence. In refining and chemical plants, control loops play an important role. Their operating status can affect the stable operation of the plant, improve production efficiency, and reduce the risks of equipment damage and production accidents [6]. At present, early fault warning for control loops faces several challenges, including difficulties in detecting and classifying operating states and in locating the causes of faults [7,8]. These difficulties may be caused by noise interference, operating-condition migration, and abnormalities in measurement instruments and actuators [9]. To address these problems, it is necessary to develop real-time and accurate fault detection methods to ensure the safe and efficient operation of industrial processes. 

- ∗ Corresponding author. 

_E-mail address:_ jianqiaozhou_cup@163.com (J. Zhou). 

https://doi.org/10.1016/j.jfranklin.2026.109034 

Received 23 January 2026; Received in revised form 12 June 2026; Accepted 1 September 2026 

Available online 2 September 2026 

0016-0032/© 2026 The Franklin Institute. Published by Elsevier Inc. All rights are reserved, including those for text and data mining, AI training, and similar technologies. 

_Journal of the Franklin Institute 363 (2026) 109034_ 

_Z. Wang et al._ 

Since the 1980s, researchers have developed numerous fault detection methodologies [10–17]. Due to the high complexity of industrial processes [18,19], it is difficult to obtain accurate mathematical models. Therefore, data-driven fault detection methods have been widely used [20–24]. Among these methods, multivariate statistical process monitoring (MSPM) is a commonly used datadriven approach [17]. With the development of information technology in the 21st century, data-driven methods based on machine learning and deep learning have also been widely applied to fault detection. Typical machine learning methods for fault detection include k-nearest neighbor (KNN) [25–27], support vector data description (SVDD) [28], and manifold learning [29]. These methods are not limited by the non-Gaussianity and nonlinearity of process data and can improve fault detection performance. Deep learningbased fault detection methods mainly include two categories: one uses neural networks as the main framework [30,31], and the other extends multivariate statistical analysis methods into deep multilevel structures [32]. In neural network-based fault detection methods, data dimensionality reduction and feature extraction are often based on the minimization of reconstruction errors, and detection indices are designed accordingly. The autoencoder (AE) is one of the methods used for data dimensionality reduction, as it can extract latent spatial representations of sample data through encoding and decoding [33]. Long short-term memory (LSTM) networks are often used to extract temporal features from data [34]. Based on AE feature extraction, Lu et al. [35] combined AE with LSTM and proposed a deep fault detection architecture for extracting the temporal dependence of high-dimensional sequence data. Another approach is to extend multivariate statistical analysis methods to deep multilevel structures. Deep Principal Component Analysis (Deep PCA) [36] is a fault detection method that uses PCA as the basic structure and multilevel spatial decomposition as its core characteristic. A large number of data-driven fault detection methods have been successfully applied in industrial fields such as electric pumps, blast furnaces, power plants, and high-speed railways [2,37–39]. 

From the perspective of system engineering, the objective of fault detection is not limited to identifying whether an abnormal condition has occurred. More importantly, it provides essential diagnostic information for subsequent fault estimation, fault-tolerant control, and control decision-making. Accurate and timely fault detection can help determine the occurrence time and evolution trend of faults, thereby supporting the design of compensation strategies and maintaining system stability and operational safety under faulty conditions. In this regard, data-driven modeling and optimization-based control methods have attracted increasing attention for faulty dynamic systems. For example, adaptive iterative learning has been investigated for spatiotemporal fault estimation in switched nonlinear reaction-diffusion systems [40], while robust _𝐻_ ∞ optimization and linear quadratic fault-tolerant control have been developed for uncertain batch processes [41]. These studies indicate that fault detection, fault estimation, and control decisionmaking are closely connected in practical engineering systems. Motivated by this consideration, this paper focuses on real-time incipient fault detection from streaming process data, aiming to provide reliable early-warning information for subsequent monitoring and control decisions. 

In real industrial processes, serious accidents usually evolve from incipient faults [42]. Such faults do not cause immediate system collapse or significant performance degradation, but may gradually develop into serious faults through long-term accumulation or coupling with other factors. An incipient fault refers to an early abnormal state with low amplitude, slow variation, and hidden characteristics, which makes it difficult for most fault detection methods to detect effectively [1,13]. Taking the Tennessee Eastman process (TEP) as an example, TEP contains 21 types of faults [43]. Fault 3 is a step fault, fault 9 is a random variation fault, and fault 15 is a valve sticking fault [24]. These three types of faults are widely recognized as typical incipient faults [44]. Due to the presence of feedback control, these small-amplitude faults have limited influence on the overall process data. The mean and variance of the observations corresponding to these faults change only slightly before and after fault occurrence [12]. In recent years, the detection of incipient faults has become a hot research topic in the field of fault detection [14]. 

Modern industrial processes generate a large amount of operational data at every moment, and process data can be regarded as real-time data streams [45]. It should be noted that data streams in real industrial processes are usually non-stationary. The operating conditions corresponding to process data are not necessarily the same [46]. When an industrial process enters a new operating condition, most detection methods have difficulty achieving optimal detection performance due to the lack of training data for the corresponding condition. Therefore, this paper aims to propose a method that can directly detect faults in industrial processes in real time. 

During the operation of industrial processes, a fixed control limit cannot effectively handle the dynamic and non-stationary characteristics of process data [47]. Actual industrial process data contain temporal correlations, and the corresponding monitoring statistics should also exhibit temporal relationships. This means that the monitoring statistic at the current sampling instant is closely related to the statistics at neighboring sampling instants. The temporal relationship among the statistics is determined by the temporal relationship among the process data. This highlights the necessity of updating control limits in real time. 

The core contribution of this work lies in proposing a real-time incipient fault detection framework, with key improvements in two critical aspects: (1) A sliding-window kernel singular-value feature extraction strategy is developed for streaming process data. In each sliding window, the process data are mapped into a high-dimensional feature space through a kernel function, and the singular values of the corresponding kernel matrix are extracted as monitoring features. These kernel singular values can characterize nonlinear correlation structures and local dynamic variations within the data window. Therefore, they provide fault-sensitive indicators for detecting weak changes caused by incipient faults. (2) An adaptive control-limit updating mechanism is incorporated into the kernel singular-value monitoring framework. Different from a fixed control limit, the adaptive control limit is updated according to the temporal evolution of the extracted singular-value statistics. This design enables the monitoring scheme to better accommodate time-varying behavior and non-stationary fluctuations in industrial data streams. 

The paper is organized as follows. Section 2 introduces the industrial background of incipient fault detection. Section 3 focuses on data-stream sliding-window kernel singular values, including data-stream normalization and kernel singular-value computation. Section 4 proposes the adaptive control limit updating algorithm and the real-time incipient fault detection method based on data- 

2 

_Journal of the Franklin Institute 363 (2026) 109034_ 

_Z. Wang et al._ 


![](Real-time_incipient_fault_detection_by_integrating_sliding-window_KSVD_dynamic_feature_extraction_and_adaptive_control_limits__images/conv_1eabdae0f26ef3eb.pdf-0003-02.png)


**Fig. 1.** Flow diagram of catalytic cracking process unit. 


![](Real-time_incipient_fault_detection_by_integrating_sliding-window_KSVD_dynamic_feature_extraction_and_adaptive_control_limits__images/conv_1eabdae0f26ef3eb.pdf-0003-04.png)


**Fig. 2.** Flow diagram of catalytic cracking process unit. 

stream sliding-window kernel singular values. Based on the adaptive control limits and kernel singular values, Section 5 presents a data simulation example to verify the necessity of control limit updating and the effectiveness of real-time fault detection. Section 6 validates the effectiveness of the proposed methodology through a comparative study based on the industrial boiler dataset. Finally, Section 7 concludes the paper. 

#### **2. Description of the industrial boiler system** 

In the chemical and petroleum refining industries, industrial boilers are critical units that provide stable thermal energy and steam to various process sections, with their operational state directly affecting energy efficiency, product quality, and plant safety [48]. Industrial boilers are often integrated into continuous process chains for material heating and temperature regulation. For example, in the atmospheric distillation section, the preheated initial bottoms must be heated by the industrial boiler to an appropriate temperature before entering the main distillation column, ensuring efficient separation under atmospheric conditions, as shown in Fig. 1. In the vacuum distillation section, the bottoms from the atmospheric column are further heated by the industrial boiler, enabling deep separation under reduced pressure by leveraging the lower boiling points in a vacuum environment, as shown in Fig. 2. 

During long-term operation, industrial boilers are susceptible to performance degradation or faults caused by various factors, such as reduced combustion efficiency, fouling of heat transfer surfaces, drift in air-fuel ratio, valve stiction, and sensor accuracy deterioration. Among these, incipient faults often manifest in their early stage as low-magnitude, slowly evolving anomalies, such as minor deviations in blowdown flow or slight drift in temperature measurement elements. These faults tend to be particularly inconspicuous in closed-loop temperature control systems, as negative feedback control mechanisms may treat them as external disturbances and suppress their direct impact, significantly weakening their visibility in process variables. Consequently, conventional monitoring methods struggle to identify such faults at an early stage. Persistent and accumulated faults of this nature can lead to reduced boiler efficiency, deterioration in steam quality, and even potential safety risks. 

3 

_Journal of the Franklin Institute 363 (2026) 109034_ 

_Z. Wang et al._ 


![](Real-time_incipient_fault_detection_by_integrating_sliding-window_KSVD_dynamic_feature_extraction_and_adaptive_control_limits__images/conv_1eabdae0f26ef3eb.pdf-0004-02.png)


**Fig. 3.** Data stream sliding-window singular value real-time incipient fault detection framework. 

Industrial boiler operation data are inherently multivariate, nonlinear, and non-stationary, with significant variability across operating conditions. Fixed control limits are often inadequate in adapting to these dynamics, and traditional monitoring techniques face limitations in detecting subtle incipient faults. In the chemical process context, developing methods capable of capturing real-time fault trends in industrial boilers and adaptively updating detection thresholds can enhance the operational reliability of blowdown systems and, more broadly, safeguard plant safety and energy efficiency. 

#### **3. Data stream sliding-window kernel singular value** 

In this section, a real-time fault detection method based on kernel-mapped data stream sliding-window singular value is proposed, and its main framework is shown in Fig. 3. In this framework, the main parts include data stream sliding-window, kernel mapping, sliding-window normalization, singular value computation, control limit updating and online detection. The following sections provide a systematic elaboration of this framework. 

#### _3.1. Description of the problem_ 

For a real-time data stream **_𝒙_** 1 _,_ **_𝒙_** 2 _,_ ⋯ _,_ **_𝒙_** _𝑞_ − _𝑤_ +1 _,_ **_𝒙_** _𝑞_ − _𝑤_ +2 _,_ ⋯ _,_ **_𝒙_** _𝑞,_ **_𝒙_** _𝑞_ +1 _,_ **_𝒙_** _𝑞_ +2 _,_ …, where _𝑞_ denotes the current sampling instant and _𝑤_ denotes the sliding-window length, i.e., the number of most recent samples used to characterize the current process state, it is difficult for most detection methods to achieve optimal detection performance when sufficient training data under the corresponding operating condition are unavailable. In this case, real-time fault detection for streaming process data is particularly necessary. For complex industrial processes, the variations of multiple process variables further require timely monitoring and online analysis of the actual process data. 

#### _3.2. Normalization of data stream sliding-window._ 

The process data are obtained in real time as data streams, and _𝑤_ successive samples are selected to form the data stream slidingwindow matrix. For real-time data **_𝒙_** _𝑞_ ∈ ℝ<sup>_𝑚_</sup> , where _𝑞_ is the sampling instant and _𝑚_ is the number of process variables, the corresponding sliding-window matrix **_𝑿_** _𝑞_ is given by 


![](Real-time_incipient_fault_detection_by_integrating_sliding-window_KSVD_dynamic_feature_extraction_and_adaptive_control_limits__images/conv_1eabdae0f26ef3eb.pdf-0004-11.png)



![](Real-time_incipient_fault_detection_by_integrating_sliding-window_KSVD_dynamic_feature_extraction_and_adaptive_control_limits__images/conv_1eabdae0f26ef3eb.pdf-0004-12.png)


with **_𝑺_** _𝑞_ = diag( _𝑠𝑞_ (1) _, 𝑠𝑞_ (2) _,_ … _, 𝑠𝑞_ ( _𝑚_ )). Here, _𝜇𝑞_ ( _𝑗_ ) and _𝑠𝑞_ ( _𝑗_ ) denote the mean and standard deviation of the _𝑗_ th process variable in the _𝑞_ th sliding window. 

4 

_Journal of the Franklin Institute 363 (2026) 109034_ 

_Z. Wang et al._ 

#### _3.3. Data stream sliding-window kernel singular value_ 

This section focuses on the kernel-based singular value decomposition of the normalized sliding-window data matrix **_𝑿_** _𝑞_ . First, **_𝑿_** _𝑞_ is mapped into a kernel representation by the Radial Basis Function (RBF) kernel. Specifically, the kernel matrix **_𝑲_** _𝑞_ ∈ ℝ<sup>_𝑤_×</sup><sup>_𝑤_</sup> is constructed as 


![](Real-time_incipient_fault_detection_by_integrating_sliding-window_KSVD_dynamic_feature_extraction_and_adaptive_control_limits__images/conv_1eabdae0f26ef3eb.pdf-0005-04.png)


where **_𝑿_** _𝑞_ ( _𝑖,_ ∶) and **_𝑿_** _𝑞_ ( _𝑗,_ ∶) denote the _𝑖_ th and _𝑗_ th samples in the normalized sliding-window matrix, respectively, and _𝛿_ is the bandwidth parameter of the RBF kernel. 

The constructed kernel matrix **_𝑲_** _𝑞_ characterizes the nonlinear similarity relationships among the samples within the current sliding window. Then, singular value decomposition is directly performed on **_𝑲_** _𝑞_ : 


![](Real-time_incipient_fault_detection_by_integrating_sliding-window_KSVD_dynamic_feature_extraction_and_adaptive_control_limits__images/conv_1eabdae0f26ef3eb.pdf-0005-07.png)


where **_𝑼_** _𝑞,_ **_𝑽_** _𝑞_ ∈ ℝ<sup>_𝑤_×</sup><sup>_𝑤_</sup> are orthogonal matrices, and **_𝑴_** _𝑞_ ∈ ℝ<sup>_𝑤_×</sup><sup>_𝑤_</sup> is a diagonal matrix whose diagonal entries are the non-negative singular values of **_𝑲_** _𝑞_ . 

Since the RBF kernel matrix is symmetric and positive semi-definite, its singular values can be directly obtained from the diagonal elements of **_𝑴_** _𝑞_ . Therefore, the kernel singular values corresponding to the current sliding window are denoted as 


![](Real-time_incipient_fault_detection_by_integrating_sliding-window_KSVD_dynamic_feature_extraction_and_adaptive_control_limits__images/conv_1eabdae0f26ef3eb.pdf-0005-10.png)


where _𝑟_ = rank( **_𝑲_** _𝑞_ ). In this paper, the selected kernel singular values { _𝜎𝑞,𝑗_ }<sup>_𝑝_</sup> _𝑗_ =1<sup>areusedasdetectionindicatorsforreal-timeincipient</sup> fault detection, where _𝑝_ denotes the number of singular-value features used for monitoring. 

#### **4. Real-time incipient fault detection framework** 

#### _4.1. Adaptive control limit_ 

In real industrial processes, the detection indicators are temporally correlated. The detection indicators at the current sampling instant are usually correlated with those obtained at adjacent sampling instants. Therefore, to obtain reliable control limits under time-varying operating conditions, an adaptive control limit (ACL) updating method is introduced in this section. 

For the sample **_𝒙_** _𝑞_ , the normalized sliding-window matrix is first mapped into an RBF kernel matrix, and singular value decomposition is then performed. The selected kernel singular values are directly used as the detection indicator vector: 


![](Real-time_incipient_fault_detection_by_integrating_sliding-window_KSVD_dynamic_feature_extraction_and_adaptive_control_limits__images/conv_1eabdae0f26ef3eb.pdf-0005-16.png)


where _𝐷𝑞,𝑗_ = _𝜎𝑞,𝑗_ is the _𝑗_ th selected kernel singular value. A larger deviation of _𝐷𝑞,𝑗_ from its normal historical level indicates a higher possibility that the current process state is affected by an abnormal condition. 

For the _𝑗_ th detection indicator, let 

**_𝒛_** _𝑞,𝑗_ = [ _𝑧_ 1 _,𝑗 , 𝑧_ 2 _,𝑗 ,_ ⋯ _, 𝑧𝑛𝑧,𝑗_ ] (9) 

denote the reference sequence used to estimate the adaptive control limit before judging **_𝒙_** _𝑞_ , where _𝑛𝑧_ is the number of retained normal indicators. Each element _𝑧𝑖,𝑗_ is a historical value of the _𝑗_ th detection indicator corresponding to a sample that has been identified as normal. These elements are arranged in chronological order, where _𝑧_ 1 _,𝑗_ is the oldest retained normal indicator and _𝑧𝑛𝑧,𝑗_ is the most recent retained normal indicator. The initial reference sequence is constructed from confirmed normal samples, and during online monitoring it is updated only when the newly observed sample is judged as normal. 

Here, a forgetting factor _𝛼_ with 0 _< 𝛼_ ⩽ 1 and a control factor _𝜈_ with 0 _< 𝜈_ ⩽ 1 are introduced. Based on **_𝒛_** _𝑞,𝑗_ , the exponentially weighted mean of the _𝑗_ th normal detection indicator is calculated as 


![](Real-time_incipient_fault_detection_by_integrating_sliding-window_KSVD_dynamic_feature_extraction_and_adaptive_control_limits__images/conv_1eabdae0f26ef3eb.pdf-0005-22.png)


where 


![](Real-time_incipient_fault_detection_by_integrating_sliding-window_KSVD_dynamic_feature_extraction_and_adaptive_control_limits__images/conv_1eabdae0f26ef3eb.pdf-0005-24.png)


is the normalization factor. A larger _𝛼_ assigns relatively similar weights to historical indicators, whereas a smaller _𝛼_ emphasizes more recent normal indicators. 

The adaptive upper and lower control limits for the _𝑗_ th detection indicator are defined as 


![](Real-time_incipient_fault_detection_by_integrating_sliding-window_KSVD_dynamic_feature_extraction_and_adaptive_control_limits__images/conv_1eabdae0f26ef3eb.pdf-0005-27.png)


5 

_Journal of the Franklin Institute 363 (2026) 109034_ 

_Z. Wang et al._ 

where _𝜈_ controls the admissible fluctuation range around the weighted mean of normal detection indicators. 

For the current sample **_𝒙_** _𝑞_ , the detection result is determined by comparing all selected kernel singular-value indicators with their corresponding adaptive control limits: 


![](Real-time_incipient_fault_detection_by_integrating_sliding-window_KSVD_dynamic_feature_extraction_and_adaptive_control_limits__images/conv_1eabdae0f26ef3eb.pdf-0006-04.png)


For online updating, let **_𝒛_**<sup>_𝑜𝑙𝑑_</sup> _𝑞,𝑗_<sup>denotethereferencesequencebeforejudging</sup><sup>**_𝒙_**</sup><sup>_𝑞_.Thecorrespondingweightedmean,normalization</sup> factor, upper control limit, and lower control limit are denoted by _𝐷𝜇,𝑞,𝑗_<sup>_𝑜𝑙𝑑_,</sup><sup>_𝜗𝑜𝑙𝑑_</sup> _𝑞_<sup>,</sup><sup>_𝐷_</sup> _𝑎𝑑𝑎,𝑞,𝑗_<sup>_ℎ𝑖𝑔ℎ,𝑜𝑙𝑑_,and</sup><sup>_𝐷_</sup> _𝑎𝑑𝑎,𝑞,𝑗_<sup>_𝑙𝑜𝑤,𝑜𝑙𝑑_,respectively.</sup> If **_𝒙_** _𝑞_ is judged as normal, each current detection indicator _𝐷𝑞,𝑗_ is accepted as a new normal indicator for the corresponding reference sequence: 


![](Real-time_incipient_fault_detection_by_integrating_sliding-window_KSVD_dynamic_feature_extraction_and_adaptive_control_limits__images/conv_1eabdae0f26ef3eb.pdf-0006-06.png)


The reference sequence is then updated by appending _̃𝑧𝑞,𝑗_ to the end of the sequence and removing the oldest element, so that the number of retained normal indicators remains _𝑛𝑧_ : 


![](Real-time_incipient_fault_detection_by_integrating_sliding-window_KSVD_dynamic_feature_extraction_and_adaptive_control_limits__images/conv_1eabdae0f26ef3eb.pdf-0006-08.png)


For the updated sequence, the weighted mean is recalculated as 


![](Real-time_incipient_fault_detection_by_integrating_sliding-window_KSVD_dynamic_feature_extraction_and_adaptive_control_limits__images/conv_1eabdae0f26ef3eb.pdf-0006-10.png)


Further, the adaptive upper and lower control limits are updated as 

_𝐷𝑎𝑑𝑎,𝑞_<sup>_ℎ𝑖𝑔ℎ_</sup> +1 _,𝑗_<sup>= (1 +</sup><sup>_𝜈_)</sup><sup>_𝐷𝜇,𝑞_+1</sup><sup>_,𝑗_</sup> (19) _𝐷𝑎𝑑𝑎,𝑞_<sup>_𝑙𝑜𝑤_</sup> +1 _,𝑗_<sup>= (1 −</sup><sup>_𝜈_)</sup><sup>_𝐷𝜇,𝑞_+1</sup><sup>_,𝑗_</sup> (20) 

Eqs. (19) and (20) show that the adaptive control limits are updated using the most recent confirmed normal indicators. When _𝛼_ is larger, historical normal indicators have relatively greater influence on the updated control limits. Conversely, when _𝛼_ is smaller, recent normal indicators have a greater influence on the updated control limits. 

If **_𝒙_** _𝑞_ is judged as fault data, the current indicators are not added to the reference sequences, and the adaptive control limits remain unchanged. 

The proposed ACL method has time-varying adaptability. By continuously updating the reference sequences with newly confirmed normal kernel singular-value indicators, the method can track gradual changes in normal operating conditions and reduce false alarms caused by fixed thresholds. 

#### _4.2. Real-time detection_ 

When a new sample **_𝒙_** _𝑞_ +1 is obtained in real time, the sliding-window data matrix is updated by removing the oldest sample and adding the newly collected sample. The updated sliding-window matrix is constructed by combining the most recent _𝑤_ samples: 


![](Real-time_incipient_fault_detection_by_integrating_sliding-window_KSVD_dynamic_feature_extraction_and_adaptive_control_limits__images/conv_1eabdae0f26ef3eb.pdf-0006-18.png)


where _𝑤_ is the sliding-window length and _𝑚_ is the number of monitored process variables. 

As in Eq. (2), **_𝑿_** _𝑞_ +1 is normalized to obtain **_𝑿_** _𝑞_ +1. Then, the RBF kernel mapping is performed on **_𝑿_** _𝑞_ +1 to construct the kernel matrix **_𝑲_** _𝑞_ +1. By applying singular value decomposition to **_𝑲_** _𝑞_ +1, the selected kernel singular values { _𝜎𝑞_ +1 _,𝑗_ }<sup>_𝑝_</sup> _𝑗_ =1<sup>areobtainedand</sup> directly used as the detection indicator vector: 


![](Real-time_incipient_fault_detection_by_integrating_sliding-window_KSVD_dynamic_feature_extraction_and_adaptive_control_limits__images/conv_1eabdae0f26ef3eb.pdf-0006-21.png)



![](Real-time_incipient_fault_detection_by_integrating_sliding-window_KSVD_dynamic_feature_extraction_and_adaptive_control_limits__images/conv_1eabdae0f26ef3eb.pdf-0006-22.png)


The state of **_𝒙_** _𝑞_ +1 is then determined according to the adaptive control limit decision rule in Eq. (14). 

In real-time detection, the proposed method consists of two stages: the offline training stage and the online detection stage, as shown in Fig. 4. In the offline training stage, historical dynamic data with fault labels are used to initialize the sliding-window length _𝑤_ , the forgetting factor _𝛼_ , the control factor _𝜈_ , and the number of selected kernel singular values _𝑝_ . Before singular value computation, 

6 

_Journal of the Franklin Institute 363 (2026) 109034_ 

_Z. Wang et al._ 


![](Real-time_incipient_fault_detection_by_integrating_sliding-window_KSVD_dynamic_feature_extraction_and_adaptive_control_limits__images/conv_1eabdae0f26ef3eb.pdf-0007-02.png)


**Fig. 4.** Flowchart of offline training and online detection. 

the normalized sliding-window data are transformed into a kernel matrix through RBF kernel mapping, so that the extracted singular values can better characterize nonlinear and incipient fault information. 

The rationality of the selected parameters is verified using the kernel singular-value indicators and the adaptive control limit method. When the parameter selection is inappropriate, the parameters can be adjusted according to the following offline debugging rules: 

(1) When the diagnostic object is in a stable process, the sliding-window length _𝑤_ can be appropriately reduced to improve diagnostic sensitivity. When the diagnostic object is in a dynamic transition process, the sliding-window length _𝑤_ should be increased to cover the transition process and avoid treating normal dynamic changes as fault alarms. 

(2) When the working condition is stable, the forgetting factor _𝛼_ can be increased. When the working condition changes, the forgetting factor _𝛼_ can be reduced so that the algorithm pays more attention to recent normal detection indicators. 

(3) When there are too many false alarms, the control factor _𝜈_ can be appropriately increased. When there are too many missed detections, the control factor _𝜈_ can be appropriately reduced. 

In the online detection stage, recent process data are collected to construct the current sliding-window matrix. Then, RBF kernel mapping and singular value decomposition are performed to obtain the kernel singular-value indicators. Finally, real-time detection is carried out using the initialized parameters and the adaptive control limit method. 

#### **5. Numerical simulation** 

This section uses the following multivariate process data generation model: 


![](Real-time_incipient_fault_detection_by_integrating_sliding-window_KSVD_dynamic_feature_extraction_and_adaptive_control_limits__images/conv_1eabdae0f26ef3eb.pdf-0007-12.png)


where **_𝒙_** = [ _𝑥_ 1 _, 𝑥_ 2 _, 𝑥_ 3 _, 𝑥_ 4 _, 𝑥_ 5] ∈ ℝ<sup>5</sup> is the process data and **𝐬** = [ _𝑠_ 1 _, 𝑠_ 2] ∈ ℝ<sup>2</sup> is the signal source. **_𝒔_** obeys the following Gaussian distributions: _𝑠_ 1 ∼  (1 _._ 2 _,_ 1) and _𝑠_ 2 ∼  (0 _._ 8 _,_ 1). And, _𝑒𝑖_ ( _𝑖_ = 1 _,_ 2 _,_ ⋯ _,_ 5) is the noise signal in the process data obeying a Gaussian distribution with zero mean and standard deviation of [0 _._ 1168 _,_ 0 _._ 0658 _,_ 0 _._ 0114 _,_ 0 _._ 0682 _,_ 0 _._ 034]<sup>_𝑇_</sup> respectively. During online testing, 5000 samples are 

7 

_Journal of the Franklin Institute 363 (2026) 109034_ 

_Z. Wang et al._ 

**Table 1** 

Comparison of PCA, DPCA and MD performance for fault detection in numerical simulation (%). 

|Malfunctions|Type|Location|Parameter|PCA||DPCA||MD|
|---|---|---|---|---|---|---|---|---|
|||||_𝑇_<sup>2</sup>|_𝑄_|_𝑇_<sup>2</sup>|_𝑄_||
|0|Normal|-|-|1.00|0.75|1.00|0.75|0.75|
|1|Sensor constant value deviation fault|_𝑥_1|_𝑓_= 0_._20|1.00|13.50|1.25|1.00|6.50|
|2|Sensor constant value deviation fault|_𝑥_1|_𝑓_= 0_._40|1.00|68.00|1.25|1.00|44.50|
|3|Sensor constant value deviation fault|_𝑥_2|_𝑓_= 0_._20|1.00|16.75|1.00|1.00|13.50|
|4|Sensor constant value deviation fault|_𝑥_2|_𝑓_= 0_._40|0.75|86.75|2.00|1.25|84.75|
|5|Sensor constant value deviation fault|_𝑥_3|_𝑓_= 0_._20|1.00|10.50|1.50|1.00|18.25|
|6|Additive process failures|_𝑠_1|_𝑓_= 1_._40|8.25|0.75|13.00|1.00|3.25|
|7|Additive process failures|_𝑠_1|_𝑓_= 1_._40|10.25|0.75|19.00|1.00|5.00|
|8|Additive process failures|_𝑠_2|_𝑓_= 1_._60|14.25|0.50|20.50|0.75|5.75|
|9|Sensor gain degradation fault|_𝑥_1|_𝜂_= 0_._95|1.00|1.75|1.00|0.75|1.50|
|10|Sensor gain degradation fault|_𝑥_1|_𝜂_= 0_._90|0.75|10.25|1.00|1.00|4.75|
|11|Sensor gain degradation fault|_𝑥_2|_𝜂_= 0_._90|1.00|5.50|0.75|0.75|5.75|



generated. The first 4600 samples are normal data, and at the 4601st sampling moment a fault occurs. The methodology in this paper considers the following three types of faults: 

- (1) Sensor constant value deviation fault: _𝑥_ = _𝑥_<sup>∗</sup> + _𝑓_ 

- (2) Additive process fault: _𝑠_ = _𝑠_<sup>∗</sup> + _𝑓_ 

- (3) Sensor gain degradation fault: _𝑥_ = _𝜂𝑥_<sup>∗</sup> 

where _𝑓_ and _𝜂_ are fault magnitude parameters. It should be noted that the fault magnitude parameters _𝑓_ and _𝜂_ represent the nominal injected fault intensity in the simulation model, rather than the final observable deviation amplitude of each measured variable. In practical closed-loop industrial processes, fault-induced deviations can be partially compensated or suppressed by feedback control loops. As a result, the observable changes in process variables and their correlation structure may remain weak at the early stage of a fault. Therefore, the incipient nature of the simulated faults is evaluated not only from the nominal parameter values, but also from their statistical detectability. As shown in Table 1, conventional MSPM methods such as PCA, DPCA, and MD show low detection rates for most of the considered faults, indicating that these faults present weak statistical variations in the monitored data. In addition, the gain degradation faults with _𝜂_ = 0 _._ 95 and _𝜂_ = 0 _._ 90 correspond to 5% and 10% gain changes, respectively, which are consistent with commonly used settings for incipient fault simulation. 

In order to compare the detection performance with the MSPM method, another 5000 normal samples are generated as training data for principal component analysis (PCA), dynamic principal component analysis (DPCA), and Mahalanobis distance (MD). 

Here, the cumulative percent variance (CPV) of PCA and DPCA is set to 90% and the maximum delay of DPCA is set to 2. The confidence level of PCA, DPCA and MD is set to 99%. The width of the data stream window used in the proposed method is set to 500, and the forgetting factor _𝛼_ = 0 _._ 99 is used for adaptive control limit updating. 

For the RBF kernel mapping, the kernel width _𝛿_ is selected according to the median heuristic based on the normal sliding-window samples before fault occurrence. Specifically, _𝛿_ is determined as 


![](Real-time_incipient_fault_detection_by_integrating_sliding-window_KSVD_dynamic_feature_extraction_and_adaptive_control_limits__images/conv_1eabdae0f26ef3eb.pdf-0008-13.png)



![](Real-time_incipient_fault_detection_by_integrating_sliding-window_KSVD_dynamic_feature_extraction_and_adaptive_control_limits__images/conv_1eabdae0f26ef3eb.pdf-0008-14.png)


where the pairwise distances are calculated from the normalized samples in the normal reference sliding windows. This selection strategy provides a balance between local and global similarity descriptions. If _𝛿_ is too small, the RBF kernel matrix tends to be close to an identity matrix, which may weaken the discrimination of the singular-value features. Conversely, if _𝛿_ is too large, the kernel matrix tends to be close to a constant matrix, which may reduce the sensitivity to incipient changes. Therefore, the median-distance rule is adopted in this numerical simulation, and the obtained kernel width is fixed during online detection. 

In addition, since the process data in this numerical simulation contain five measured variables, the first five dominant kernel singular values, i.e., _𝜎_ 1 _, 𝜎_ 2 _, 𝜎_ 3 _, 𝜎_ 4, and _𝜎_ 5, are selected as candidate detection indicators. These leading kernel singular values reflect the main nonlinear correlation structure and dynamic variations in the sliding-window data. Higher-order singular values are generally small and more sensitive to noise, and thus they are not used as the main monitoring indicators in this case. In Table 2, the detection performance of each selected singular value is reported separately to show the sensitivity of different singular-value features to different incipient faults. For different faults, the control factor _𝜈_ is adjusted in a small range according to the offline parameter tuning rule described in Section 4, and its value is listed in Table 2. 

To clearly quantify the monitoring performance, the detection rate and false alarm rate are used as evaluation metrics in the numerical simulation. Let _𝐽_ ( _𝑡_ ) denote the monitoring statistic at sampling time _𝑡_ , and let _𝐽_ lim( _𝑡_ ) denote the corresponding control limit. The alarm indicator is defined as 


![](Real-time_incipient_fault_detection_by_integrating_sliding-window_KSVD_dynamic_feature_extraction_and_adaptive_control_limits__images/conv_1eabdae0f26ef3eb.pdf-0008-18.png)


8 

_Journal of the Franklin Institute 363 (2026) 109034_ 

_Z. Wang et al._ 


![](Real-time_incipient_fault_detection_by_integrating_sliding-window_KSVD_dynamic_feature_extraction_and_adaptive_control_limits__images/conv_1eabdae0f26ef3eb.pdf-0009-02.png)


**Fig. 5.** Effectiveness of PCA, DPCA, MD and the methods in this paper on the detection of fault 1 in numerical simulation. 

For a faulty testing sequence, the fault detection rate (FDR) is calculated as 


![](Real-time_incipient_fault_detection_by_integrating_sliding-window_KSVD_dynamic_feature_extraction_and_adaptive_control_limits__images/conv_1eabdae0f26ef3eb.pdf-0009-05.png)


where _𝑡𝑓_ is the fault occurrence time and _𝑁_ is the total number of testing samples. In this numerical simulation, _𝑡𝑓_ = 4601 and _𝑁_ = 5000 for the faulty cases. For the normal case, the false alarm rate (FAR) is calculated as 


![](Real-time_incipient_fault_detection_by_integrating_sliding-window_KSVD_dynamic_feature_extraction_and_adaptive_control_limits__images/conv_1eabdae0f26ef3eb.pdf-0009-07.png)


where _𝑁𝑛_ is the number of normal testing samples used for false alarm evaluation. Therefore, in Table 1 and Table 2, the row corresponding to the normal case reports the FAR, while the rows corresponding to fault cases report the FDR. 

9 

_Journal of the Franklin Institute 363 (2026) 109034_ 

_Z. Wang et al._ 

**Table 2** 

Comparison of the performance of the methods in this paper for detecting faults in numerical simulation (%). 

|Malfunctions|Type|Location|Parameter|_𝜈_|Met|hods i|n this pape|r||
|---|---|---|---|---|---|---|---|---|---|
||||||_𝜎_1|_𝜎_2|_𝜎_3|_𝜎_4|_𝜎_5|
|0|Normal|-|-|_𝜈_= 0_._05|0|0|0|0.75|0|
|1|Sensor constant value deviation fault|_𝑥_1|_𝑓_= 0_._20|_𝜈_= 0_._12|0|0|0|0|84.75|
|2|Sensor constant value deviation fault|_𝑥_1|_𝑓_= 0_._40|_𝜈_= 0_._12|0|0|0|90.75|97.50|
|3|Sensor constant value deviation fault|_𝑥_2|_𝑓_= 0_._20|_𝜈_= 0_._11|0|0|0|98.00|0|
|4|Sensor constant value deviation fault|_𝑥_2|_𝑓_= 0_._40|_𝜈_= 0_._12|0|0|4.75|98.00|0|
|5|Sensor constant value deviation fault|_𝑥_3|_𝑓_= 0_._20|_𝜈_= 0_._11|0|0|0|69.25|96.50|
|6|Additive process failures|_𝑠_1|_𝑓_= 1_._40|_𝜈_= 0_._11|0|0|3.00|83.25|8.75|
|7|Additive process failures|_𝑠_1|_𝑓_= 1_._40|_𝜈_= 0_._12|0|0|92.00|90.00|0.50|
|8|Additive process failures|_𝑠_2|_𝑓_= 1_._60|_𝜈_= 0_._05|0|0|68.00|11.00|90.25|
|9|Sensor gain degradation fault|_𝑥_1|_𝜂_= 0_._95|_𝜈_= 0_._08|0|0|80.25|8.5|87.50|
|10|Sensor gain degradation fault|_𝑥_1|_𝜂_= 0_._90|_𝜈_= 0_._10|0|0|0|62.25|91.75|
|11|Sensor gain degradation fault|_𝑥_2|_𝜂_= 0_._90|_𝜈_= 0_._10|0|0|0|86.25|1.25|
||**Table** **3**<br>Boiler fault detection dataset.|||||||||
||Characteristic parameters||||Fau|lty lab|el|||
||1. Boiler Number|12. Scale Tem|perature|||||||
||2. Time|13. External|Temperature|||||||
||3. Steam Pressure in Main Header|14. Operating|Status|||||||
||4. Outdoor Temperature|15. Operating|Code|||||||
||5. Concentrated Water Temperature|16. Input Stat|us|||||||
||6. Feed Water Operating Time<br> 7. Exhaust Gas Temperature|17. Power Us<br> 18. Steam Pr|age Meter<br>essure||Ab|normal|Blow Do|wn||
||8. Feed Water Volume Delta|19. Chemical|Injection Oper|ating Time||||||
||9. Feed Water Temperature|20. Combusti|on Time|||||||
||10. Tube Wall Temperature|21. Number o|f Ignitions|||||||
||11. Damper Angle|22. Gas Cons|umption|||||||



In Table 1 and Table 2, the comparisons of fault amplitudes and detection performances for 11 faults are listed. As shown in Table 1, PCA, DPCA, and MD have difficulty in obtaining satisfactory detection results for most incipient faults. Taking fault 1 as an example, fault 1 is a sensor constant value deviation fault occurring in _𝑥_ 1 with a magnitude of 0.20. The detection performance of different methods for fault 1 is shown in Fig. 5, where the detection rates of PCA, DPCA, and MD are all less than 15%. In contrast, as shown in Table 2, the 5th kernel singular value _𝜎_ 5 achieves a detection rate of 84.75% for fault 1, which is much higher than those of PCA, DPCA, and MD. 

For fault 4, which is a sensor constant value deviation fault occurring in _𝑥_ 2 with a magnitude of 0.40, the _𝑄_ statistic of PCA achieves a detection rate of 86.75%. However, the proposed method achieves a detection rate of 98.00% using the 4th kernel singular value _𝜎_ 4, further demonstrating the effectiveness of the kernel sliding-window singular-value features. Fig. 6 shows the detection results of PCA, DPCA, MD, and the proposed method for fault 4, where the 3rd, 4th, and 5th kernel singular values are sensitive to the fault. 

It can also be observed from Table 2 that different kernel singular values show different sensitivities to different incipient faults. The first two singular values, _𝜎_ 1 and _𝜎_ 2, mainly represent the dominant normal correlation structure in the sliding-window kernel matrix, and thus they are less sensitive to small fault-induced variations in this numerical example. By contrast, _𝜎_ 3, _𝜎_ 4, and _𝜎_ 5 contain more detailed variations of the nonlinear correlation structure and are therefore more effective for detecting weak changes caused by incipient faults. This result also supports the choice of using the first five dominant kernel singular values as candidate monitoring indicators rather than relying on a single singular value. 

#### **6. Industrial case** 

This paper validates the fault detection capability of the sliding-window singular value method for data streams based on adaptive control limits using industrial boiler fault detection dataset [48]. The boiler data consists of sensor data from three boilers from 2014/3/24 to 2016/11/30. There are 3 boilers in this dataset and each boiler is independent of the others. This dataset covers a variety of parameters and environmental data during boiler operation (including 22 characteristic parameters and 1 fault label). The testing task is to determine if each boiler has a faulty blowdown. The Table 3 is a brief description of each column in the dataset: 

The main purpose of boiler blow down is to prevent scaling and corrosion due to steam evaporation by discharging sludge with a high concentration of minerals. Abnormal blow down usually manifests itself as a deviation in the frequency or volume of discharge. In the case of too little blow down, the concentration of minerals in the water is slightly increased in the short term, which may lead to a slow decline in thermal efficiency, but does not immediately cause serious problems such as pipe rupture. In the case of too much discharge, water and heat are wasted, but the boiler can still maintain basic operation if the redundant design of the system is not exceeded. The slowness of this initial impact causes it to be categorised as a minor failure. 

10 

_Journal of the Franklin Institute 363 (2026) 109034_ 

_Z. Wang et al._ 


![](Real-time_incipient_fault_detection_by_integrating_sliding-window_KSVD_dynamic_feature_extraction_and_adaptive_control_limits__images/conv_1eabdae0f26ef3eb.pdf-0011-02.png)


**Fig. 6.** Effectiveness of PCA, DPCA, MD and the methods in this paper on the detection of fault 4 in numerical simulation. 

In this experiment, we evaluated the detection performance of our proposed method by comparing it with an adaptive threshold method [49]. Specifically, the method first captures the rate of change of the characteristic parameters. Then, adaptive thresholds are determined based on a moving window approach. Finally, the thresholds are used to distinguish between faulty and non-faulty cases. This method is mainly used to identify faults in which the feature undergoes parameter jumps, which is similar to the application scenario of the method in this paper, and can be used for comparative experiments. 

In this paper, Boiler No. 8 was selected for the experiment. Firstly, stable operating conditions were filtered by selecting data with the following criteria: Operating Code = 0, Operating Status = 0, Input Status = 0, Damper Angle = 0, and Steam Pressure = 0. This ensured that the algorithmic of fault detection would not be affected by operational mode transitions. Secondly, eight variables (numbered 3, 4, 5, 7, 9, 10, 12, and 13) were identified as feature parameters for abnormal blowdown detection. Subsequently, sampling points 15,000 to 17,750 were extracted, and outliers (including zero and constant values) were removed. The resulting dataset comprised 2742 samples, with a fault occurring at the 2,417th sampling point. 

11 

_Journal of the Franklin Institute 363 (2026) 109034_ 

_Z. Wang et al._ 


![](Real-time_incipient_fault_detection_by_integrating_sliding-window_KSVD_dynamic_feature_extraction_and_adaptive_control_limits__images/conv_1eabdae0f26ef3eb.pdf-0012-02.png)


**Fig. 7.** Effectiveness of the methods of adaptive threshold for detecting abnormal blow down in industrial cases. 

For the industrial boiler case, the detection rate and detection time are used to evaluate the fault detection performance. The alarm indicator _𝐼_ ( _𝑡_ ) is defined in the same way as in Eq. (25). Since the abnormal blowdown fault occurs at _𝑡𝑓_ = 2417 and the total number of samples is _𝑁_ = 2742, the detection rate is calculated as 


![](Real-time_incipient_fault_detection_by_integrating_sliding-window_KSVD_dynamic_feature_extraction_and_adaptive_control_limits__images/conv_1eabdae0f26ef3eb.pdf-0012-05.png)


The detection time is defined as the first sampling point at which an alarm is triggered after the fault occurrence: 


![](Real-time_incipient_fault_detection_by_integrating_sliding-window_KSVD_dynamic_feature_extraction_and_adaptive_control_limits__images/conv_1eabdae0f26ef3eb.pdf-0012-07.png)


The corresponding detection delay can be further expressed as 


![](Real-time_incipient_fault_detection_by_integrating_sliding-window_KSVD_dynamic_feature_extraction_and_adaptive_control_limits__images/conv_1eabdae0f26ef3eb.pdf-0012-09.png)


If no effective alarm is triggered after the fault occurrence, the detection time is denoted by “-”. These metrics are used in Table 4 to compare the effects of different forgetting factors and control factors on the detection performance. Finally, algorithmic parameters were configured: the sliding window size for the data stream was set to 1,700. 

In this paper, we analyse the effect of forgetting factor and control factor on the detection effect through comparative experiments, as shown in Table 4. The forgetting factor indicates how much importance the algorithm attaches to the dynamic performance of the recent process, too large or too small will affect the detection effect, and the best value of the influence factor should be adjusted 

12 

_Journal of the Franklin Institute 363 (2026) 109034_ 

_Z. Wang et al._ 

**Table 4** 

Effect of forgetting factor _𝛼_ and control factor _𝜈_ on the performance of detection methods. 

|Ablation Study|Forgetting Factor|Control Factor|Detection t|ime||||||Detection rate|
|---|---|---|---|---|---|---|---|---|---|---|
||||_𝜎_1<br>_𝜎_2|_𝜎_3|_𝜎_4|_𝜎_5|_𝜎_6|_𝜎_7|_𝜎_8||
|1|0.95|0.18|-<br> -|-|-|-|2422|2428|2430|98.46%|
|2|0.90|0.18|-<br> -|-|-|-|2422|2427|2431|98.46%|
|3|0.99|0.18|-<br> -|-|-|-|2422|2348|1984|-|
|4|0.95|0.10|-<br> -|-|-|-|2421|2355|2325|-|
|5|0.95|0.25|-<br> -|-|-|-|2422|2433|-|98.46%|



with the dynamic order of the process model. A decreasing control factor increases the false alarm rate of detection, while too large a control factor affects the detection performance. 

Therefore, the forgetting factor in this section is 0.95 and the control factor is 0.18. In order to ensure fairness, the length of the data stream sliding-window in the comparative test is also set to 1700. For the adaptive threshold method, the coefficient _𝑧_ is set to 3. Here, _𝑧_ denotes the threshold scaling coefficient used to determine the allowable fluctuation range around the moving-window mean. Specifically, the adaptive threshold is commonly constructed as the moving-window mean plus or minus _𝑧_ times the corresponding standard deviation. A larger _𝑧_ leads to a wider threshold range and thus reduces false alarms, but it may decrease the sensitivity to weak faults. Conversely, a smaller _𝑧_ gives a narrower threshold range and may improve fault sensitivity, but it may also increase the false alarm rate. In this case, _𝑧_ = 3 is adopted according to the classical three-sigma rule, which provides a relatively conservative threshold setting for the comparative method. 

In Fig. 7, the effectiveness of the adaptive threshold method for the boiler fault detection dataset is demonstrated, and it can be seen that this method is less effective in detecting the faults. 

In Fig. 8, the effectiveness of the proposed method for the boiler fault detection dataset is demonstrated, where the 6th, 7th, and 8th kernel singular values of the data stream sliding-window are effective in detecting the faults. 

Fig. 9(a) and Fig. 9(b) show the monitoring results of KPCA based on the _𝑇_<sup>2</sup> and _𝑄_ statistics, respectively, while Fig. 9(c) and Fig. 9(d) show the corresponding results of DKPCA. It can be observed that KPCA and DKPCA can characterize the nonlinear variations of the boiler process to a certain extent. However, for the abnormal blowdown fault considered in this case, the fault evolves slowly and its influence on the process variables is relatively weak. Therefore, the monitoring statistics of KPCA and DKPCA do not provide sufficiently sensitive and stable fault detection performance. This comparison further demonstrates the effectiveness and advancement of the proposed method for industrial incipient fault detection. 

The reason why the later singular values are more sensitive in this industrial case is similar to that in the numerical simulation. In this case, eight variables are selected as feature parameters for abnormal blowdown detection, and thus the first eight kernel singular values are considered as candidate detection indicators. The first few singular values mainly reflect the dominant operating variations of the boiler system under normal conditions. However, abnormal blowdown is an incipient fault with slow evolution and weak influence, and its effect may be masked by the dominant normal operating patterns. Therefore, the first few singular values may not show obvious abnormal deviations. In contrast, the 6th, 7th, and 8th singular values describe more detailed changes in the nonlinear correlation structure among the selected boiler variables, making them more sensitive to the weak variations caused by abnormal blowdown. 

13 

_Journal of the Franklin Institute 363 (2026) 109034_ 

_Z. Wang et al._ 


![](Real-time_incipient_fault_detection_by_integrating_sliding-window_KSVD_dynamic_feature_extraction_and_adaptive_control_limits__images/conv_1eabdae0f26ef3eb.pdf-0014-02.png)


**Fig. 8.** Effectiveness of the methods in this paper for detecting abnormal blow down in industrial cases. 

14 

_Journal of the Franklin Institute 363 (2026) 109034_ 

_Z. Wang et al._ 


![](Real-time_incipient_fault_detection_by_integrating_sliding-window_KSVD_dynamic_feature_extraction_and_adaptive_control_limits__images/conv_1eabdae0f26ef3eb.pdf-0015-02.png)


**Fig. 9.** Monitoring results of KPCA and DKPCA in the industrial boiler case. 

#### **7. Conclusions** 

This paper proposes a real-time incipient fault detection method for streaming process data. In the proposed framework, RBF kernel mapping is introduced before singular value computation, so that nonlinear correlation structures and weak fault-related variations can be better characterized. To cope with large-scale and time-varying industrial data streams, the kernel singular values are extracted from normalized sliding windows in real time. This design reduces the dependence on sufficient training data under specific operating conditions and enables the monitoring model to utilize the temporal characteristics of process data and the corresponding statistics. Furthermore, an adaptive control-limit updating mechanism is developed based on the extracted kernel singular values. By incorporating a forgetting factor and a control factor, the control limits can be dynamically adjusted according to realtime process variations, thereby improving the detectability of incipient faults. The numerical simulation and industrial boiler case study demonstrate that the proposed method has good sensitivity to weak faults and adaptability to dynamic non-stationary process data. 

Future work will focus on further exploiting the temporal characteristics of the detection features. Since the kernel singular values form time-series monitoring features, regression and prediction techniques can be introduced to model their temporal evolution. In this way, the control limits of the corresponding monitoring statistics can be continuously updated based on real-time data, which may further improve the monitoring performance for dynamic industrial processes. 

15 

_Journal of the Franklin Institute 363 (2026) 109034_ 

_Z. Wang et al._ 

#### **CRediT authorship contribution statement** 

**Zhu Wang:** Supervision, Resources, Project administration, Methodology, Funding acquisition, Conceptualization; **Jianqiao Zhou:** Writing - review & editing, Visualization, Validation, Software, Methodology, Investigation, Formal analysis, Data curation, Conceptualization; **Decheng Liu:** Writing - original draft, Software, Data curation. 

#### **Declaration of competing interest** 

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper. 

#### **References** 

|[1] J. Shang, M. Chen, H. Ji, D. Zhou, Recursive transformed component statistical analysis for incipient fault detection, Automatica 80 (2017) 313–327.<br>2SCMiZHHZDhZHifLMiliIbdifdiillif|
|---|
|[] . Jun, . aoyn, . anwen, J. ongquan, . ongua, . aeng, . ngang, ncrement-ase recursve transorme component statstca anayss or<br>monitoring blast furnace iron-making processes: an index-switching scheme, Control Eng. Pract. 77 (2018) 190-200.|
|[3] T. Guo, D. Zhou, J. Zhang, M. Chen, X. Tai, Fault detection based on robust characteristic dimensionality reduction, Control Eng. Pract. 84 (MAR.) (2019)<br>125–138.|
|[4] M. Mythily, D. Manamalli, P. Manikandan, Dynamic modeling, simulation and multivariable control strategy applied to catalytic cracking unit, in: 2011 Inter-<br>national Conference on Process Automation, Control and Computing, IEEE, 2011, pp. 1–7.|
|[5] A. Boucheikhchoukh, V. Berger, C.L.E. Swartz, A. Deza, A. Nguyen, S. Jafer, Multiperiod refnery optimization for mitigating the impact of process unit shut-<br>|
|downs, Comput. Chem. Eng. 164 (2022) 107873.|
|[6] F.E. Mustafa, I. Ahmed, A. Basit, S.H. Malik, A. Mahmood, P.R. Ali, et al., A review on efective alarm management systems for industrial process control: barriers<br>and opportunities, Int. J. Crit. Infrastruct. Prot. 41 (2023) 100599.|
|[7] S.J. Qin, Survey on data-driven industrial process monitoring and diagnosis, Annu. Rev. Control 36 (2) (2012) 220–234.|
|[8] Z. Ge, Z. Song, F. Gao, Review of recent research on data-based process monitoring, Ind. Eng. Chem. Res. 52 (10) (2013) 3543–3562.|
|[9] J. Dong, L. Jiang, C. Zhang, K. Peng, A novel quality-related incipient fault detection method based on canonical variate analysis and kullback–Leibler divergence<br>for large-scale industrial processes, IEEE Trans. Instrum. Meas. 71 (2022) 1–10.|
|[10] B.M. Wise, D.J. Veltkamp, B. Davis, N.L. Ricker, B.R. Kowalski, Principal components analysis for monitoring the west valley liquid fed ceramic melter, in: Waste<br>Management’88, 1988.|
|[11] R. Isermann, P. Balle, Trends in the application of model-based fault detection and diagnosis of technical processes, Control Eng. Pract. 5 (5) (1997) 709–719.|
|[12] C. Zhang, Q. Guo, Y. Li, Fault detection in the tennessee eastman benchmark process using principal component diference based on k-nearest neighbors, IEEE<br>Access 8 (2020) 49999–50009.|
|[13] Y. Dong, S.J. Qin, A novel dynamic PCA algorithm for dynamic data modeling and process monitoring, J. Process Control 67 (2018) 1–11.|
|[14] Z. Li, L. Tian, Q. Jiang, X. Yan, Distributed-ensemble stacked autoencoder model for non-linear process monitoring, Inf. Sci. 542 (2021) 302–316.<br>|
|[15] K.E.S. Pilario, Y. Cao, Canonical variate dissimilarity analysis for process incipient fault detection, IEEE Trans. Ind. Inform. 14 (12) (2018) 5308–5315.|
|[16] H. Chen, B. Jiang, S.X. Ding, N. Lu, W. Chen, Probability-relevant incipient fault detection and diagnosis methodology with applications to electric drive systems,|
|IEEE Trans. Control Syst. Technol. 27 (6) (2018) 2766–2773.|
|[17] S.X. Ding, Data-driven design of fault diagnosis and fault-tolerant control systems, Springer, 2014.|
|[18] M.R. Guertler, D. Schneider, J. Heitfeld, N. Sick, Analysing industry 4.0 technology-solution dependencies: a support framework for successful industry 4.0<br>adoption in the product generation process, Res. Eng. Des. 35 (2) (2024) 115–136.|
|[19] V. Thielens, F. Demeyer, W. De Paepe, Performance comparison of sCO2 and steam cycles for waste heat recovery based on annual semi-transient modeling|
|under complex industrial constraints, Case Stud. Therm. Eng. 60 (2024) 104691.|
|[20] S. Joe Qin, Statistical process monitoring: basics and beyond, J. Chemom.: J. Chemom. Soc. 17 (8–9) (2003) 480–502.|
|[21] P. Geladi, B.R. Kowalski, Partial least-squares regression: a tutorial, Anal. Chim. Acta 185 (1986) 1–17.|
|[22] W. Ku, R.H. Storer, C. Georgakis, Disturbance detection and isolation by dynamic principal component analysis, Chemom. Intell. Lab. Syst. 30 (1) (1995)<br>179–196.|
|[23] J.-M. Lee, C. Yoo, S.W. Choi, P.A. Vanrolleghem, I.-B. Lee, Nonlinear process monitoring using kernel principal component analysis, Chem. Eng. Sci. 59 (1)<br>(2004) 223–234.|
|[24] S. Yin, S.X. Ding, A. Haghani, H. Hao, P. Zhang, A comparison study of basic data-driven fault diagnosis and process monitoring methods on the benchmark<br>tennessee eastman process, J. Process Control 22 (9) (2012) 1567–1581.|
|[25] Q.P. He, J. Wang, Fault detection using the k-nearest neighbor rule for semiconductor manufacturing processes, IEEE Trans. Semicond. Manuf. 20 (4) (2007)<br>345–354.|
|[26] C. Zhang, X. Gao, Y. Li, L. Feng, Fault detection strategy based on weighted distance of _𝑘_ nearest neighbors for semiconductor manufacturing processes, IEEE<br>|
|Trans. Semicond. Manuf. 32 (1) (2018) 75–81.|
|[27] Z. Sun, J. Yang, K. Zheng, A novel fault detection method for semiconductor manufacturing processes, in: 2019 IEEE International Instrumentation and Mea-<br>surement Technology Conference (I2MTC), IEEE, 2019, pp. 1–6.|
|[28] Z. Ge, F. Gao, Z. Song, Batch process monitoring based on support vector data description method, J. Process Control 21 (6) (2011) 949–959.|
|[29] J. Zhang, M. Chen, H. Chen, X. Hong, D. Zhou, Process monitoring based on orthogonal locality preserving projection with maximum likelihood estimation, Ind.<br>|
|Eng. Chem. Res. 58 (14) (2019) 5579–5587.|
|[30] S. Heo, J.H. Lee, Parallel neural networks for improved nonlinear principal component analysis, Comput. Chem. Eng. 127 (2019) 1–10.|
|[31] Q. Li, H. Luo, H. Cheng, Y. Deng, W. Sun, W. Li, Z. Liu, Incipient fault detection in power distribution system: a time–frequency embedded deep-learning-based<br>approach, IEEE Trans. Instrum. Meas. 72 (2023) 1–14.|
|[32] W. Yu, C. Zhao, B. Huang, Moninet with concurrent analytics of temporal and spatial information for fault detection in industrial processes, IEEE Trans. Cybern.|
|52 (8) (2021) 8340–8351.|
|[33] Z.-L. Ma, X.-J. Li, F.-Q. Nian, An interpretable fault detection approach for industrial processes based on improved autoencoder, IEEE Trans. Instrum. Meas.|
|(2025)|
|.<br>[34] N.-C. Yang, M. Faizan, Long short-term memory-based feedforward neural network algorithm for photovoltaic fault detection under irradiance conditions, IEEE<br>Trans. Instrum. Meas. (2024).|
|[35] W. Lu, Y. Li, Y. Cheng, D. Meng, B. Liang, P. Zhou, Early fault detection approach with deep architectures, IEEE Trans. Instrum. Meas. 67 (7) (2018) 1679–1689.|
|[36] H. Chen, B. Jiang, N. Lu, Z. Mao, Deep PCA based real-time incipient fault detection and diagnosis methodology for electrical drive in high-speed trains, IEEE<br>TVhThl67(6)(2018)48194830|
|rans. e. ecno.    –.<br>[37] Q. Li, K. Li, X. Gao, J. Fu, L. Zhang, Anomaly detection based on temporal attention network with adaptive threshold adjustment for electrical submersible pump,<br>IEEE Trans. Instrum. Meas. (2024).|



- [38] M. Wang, D. Zhou, M. Chen, Y. Wang, Anomaly detection in the fan system of a thermal power plant monitored by continuous and two-valued variables, Control Eng. Pract. 102 (4) (2020) 104522. 

16 

_Journal of the Franklin Institute 363 (2026) 109034_ 

##### _Z. Wang et al._ 

- [39] J. Sang, T. Guo, J. Zhang, D. Zhou, X. Tai, Incipient fault detection for air brake system of high-Speed trains, IEEE Trans. Control Syst. Technol. PP (99) (2020) 1–12. 

- [40] Z. Peng, X. Song, S. Song, V. Stojanovic, Spatiotemporal fault estimation for switched nonlinear reaction–diffusion systems via adaptive iterative learning, Int. J. Adapt. Control Signal Process. 38 (10) (2024) 3473–3483. 

- [41] P. Yuan, J. Bai, H. Zou, Two-dimensional iterative learning robust _𝐻_ ∞ optimization and linear quadratic fault-tolerant control design for uncertain batch processes, Can. J. Chem. Eng. (2026). 

- [42] K. Watanabe, I. Matsuura, M. Abe, M. Kubota, D.M. Himmelblau, Incipient fault diagnosis of chemical processes via artificial neural networks, Aiche J. 35 (11) (1989) 1803–1812. 

- [43] J.J. Downs, E.F. Vogel, A plant-wide industrial process control problem, Comput. Chem. Eng. 17 (3) (1993) 245–255. 

- [44] Q. Jiang, S. Yan, X. Yan, S. Chen, J. Sun, Data-driven individual–joint learning framework for nonlinear process monitoring, Control Eng. Pract. 95 (2020) 104235. 

- [45] T. Guo, D. Zhou, J. Zhang, M. Chen, X. Tai, Fault detection based on robust characteristic dimensionality reduction, Control Eng. Pract. 84 (2019) 125–138. 

- [46] D. Wu, D. Zhou, M. Chen, J. Zhu, F. Yan, S. Zheng, E. Guo, Output-relevant common trend analysis for KPI-related nonstationary process monitoring with applications to thermal power plants, IEEE Trans. Ind. Inform. 17 (10) (2020) 6664–6675. 

- [47] W. Zhao, Y. Guo, H. Sun, Research on an adaptive threshold setting method for aero-engine fault detection based on KDE-EWMA, J. Aerosp. Eng. 35 (6) (2022) 04022087. 

- [48] R. Cai, J. Chen, Z. Li, W. Chen, K. Zhang, J. Ye, Z. Li, X. Yang, Z. Zhang, Time series domain adaptation via sparse associative structure alignment, in: Proceedings of the AAAI Conference on Artificial Intelligence, 35, 2021, pp. 6859–6867. 

- [49] X. Li, M. Lyu, X. Gao, C. Yuan, D. Zhen, An adaptive threshold method for multi-faults diagnosis of lithium-ion batteries based on electro-thermal model, Measurement 222 (2023) 113671. 

17 

