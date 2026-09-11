Journal of Process Control 152 (2025) 103495 


![](Reducing_false_alarms_in_fault_detection-_a_comparative_analysis_between_conformal_prediction_and_classical_methods_applied_to_PCA_and_autoencoders_images/conv_f4a22b1a51a40923.pdf-0001-01.png)


Contents lists available at ScienceDirect 

# Journal of Process Control 

journal homepage: www.elsevier.com/locate/jprocont 


![](Reducing_false_alarms_in_fault_detection-_a_comparative_analysis_between_conformal_prediction_and_classical_methods_applied_to_PCA_and_autoencoders_images/conv_f4a22b1a51a40923.pdf-0001-05.png)


## Reducing false alarms in fault detection: A comparative analysis between conformal prediction and classical methods applied to PCA and autoencoders 


![](Reducing_false_alarms_in_fault_detection-_a_comparative_analysis_between_conformal_prediction_and_classical_methods_applied_to_PCA_and_autoencoders_images/conv_f4a22b1a51a40923.pdf-0001-07.png)


### Abdoul Rahime Diallo<sup>*</sup> , Lazhar Homri , Jean-Yves Dantan 

_Arts et Metiers Institute of Technology, Universit_ ´ _e de Lorraine, LCFC, Metz, France_ 

|A R T I C L E I N F O|A B S T R A C T|
|---|---|
|_Keywords:_<br>Fault detection<br>Threshold setting<br>Conformal prediction<br>False alarm rate control<br>Tennessee Eastman process|Setting detection thresholds in data-driven fault detection is a critical challenge, particularly in ensuring a<br>reliable balance between false alarm rate and fault detection capability. Although conformal prediction has been<br>applied to various domains including medicine, fnance, and the monitoring of physical systems, its use in in-<br>dustrial fault detection remains underexplored. This study compares conformal prediction methods with classical<br>threshold-setting techniques used in Principal Component Analysis (PCA) and Autoencoder (AE) based fault<br>detection, using extensive experiments on the Tennessee Eastman Process (TEP). The analysis considers<br>conformal prediction strategies, with marginal and conditional validity alongside traditional parametric ap-<br>proaches for PCA and non-parametric methods for AE. The results highlight the sensitivity of false alarm rates to<br>training data availability, with both traditional and marginal conformal methods often exceeding the targeted<br>false alarm risk when training data are limited. In this context, approaches with conditional validity provide a<br>reliable estimation of the uncertainty associated with the false alarm rate. When suffcient training data are<br>available, conditional conformal methods, particularly those based on the Dvoretzky-Kiefer-Wolfowitz (DKW)<br>and Simes adjustments, provide stricter false alarm rate control, systematically remaining below the predefned<br>risk levels. While this comes at the cost of a slight decrease in fault detection rates, the trade-off is particularly<br>relevant in industrial settings where normal operation is overwhelmingly more frequent than fault occurrences.<br>Overall, conformal prediction demonstrates competitive performance compared to analytically established PCA-<br>based thresholds and the widely used Kernel Density Estimation (KDE) for AE-based fault detection.|



#### **1. Introduction** 

Data-driven methods for fault detection can be divided into two categories. The first one includes supervised methods, which require labeled data for training. However, in industrial applications, labeled data are scarce and, when available, are highly imbalanced: normal operating data vastly outnumber faulty data [1–3]. As a result, supervised methods tend to be biased toward the dominant class [4]. To address this issue, the second category, semi-supervised (or, for some authors, unsupervised) methods, which require only normal operating data for training, is widely used in fault detection. A complementary strategy that has recently gained attention is transfer learning, where a model trained on a data-rich source domain (another process, a simulator, or a publicly available dataset) is adapted to a target process with limited faulty data [5–7]. 

In this article, we focus on semi-supervised methods, whose most well-known tools include control charts [8], multivariate statistical process control techniques such as Principal Component Analysis (PCA) [9], Autoencoders (AE) [10], One-Class Support Vector Machines (OCSVM) [11], and Isolation Forest [12]. Among these methods, PCA and AE, along with their numerous variants, are particularly used [3, 13–16]. 

The development of these techniques for industrial production system monitoring typically follows four main steps. The first step consists of training the data model. The second step involves selecting a detection index, which can be defined in the reduced space, the original data space, or a combination of both. The most commonly used indices are the reconstruction error in the original space, also known as Squared Prediction Error (SPE) or Q-statistic in PCA, and Hotelling T<sup>2</sup> statistic in the reduced space [14,17,18]. The third step concerns the setting of the 

* Corresponding author. 

_E-mail addresses:_ abdoul-rahime.diallo@ensam.eu (A.R. Diallo), Lazhar.homri@ensam.eu (L. Homri), jean-yves.dantan@ensam.eu (J.-Y. Dantan). 

https://doi.org/10.1016/j.jprocont.2025.103495 

Received 10 April 2025; Received in revised form 24 June 2025; Accepted 27 June 2025 Available online 2 July 2025 

0959-1524/© 2025 Elsevier Ltd. All rights are reserved, including those for text and data mining, AI training, and similar technologies. 

> _A.R. Diallo et al.                                                                                                                                                                                                                                Journal of Process Control 152 (2025) 103495_ 

detection threshold, while the fourth step involves implementing fault isolation techniques. This article does not address the last step. 

The third step, determining the detection threshold, is particularly critical. If the threshold is set too high, the model will detect very few faults; conversely, if it is set too low, the false alarm rate will be excessively high. False alarms pose a challenge in fault detection systems, particularly in contexts where faults occur far less frequently than normal system operations. In such cases, excessive false alarms can overshadow the rare occurrences of actual faults [19], leading to alarm fatigue or the "cry-wolf" effect. This phenomenon, well documented in medical alert systems [20,21] and ergonomics [22,23], is rarely considered in fault detection. Its consequence is a loss of trust in the alert system, causing operators to ignore all alarms over time [19]. 

Threshold determination typically involves estimating the statistical distribution of the detection index for normal operating data. A statistical test is then performed on new observations to determine whether they belong to this distribution, with a significance level _α_ controlling the risk of incorrectly rejecting the null hypothesis [1]. For PCA, the detection index distributions are well-defined under certain assumptions about normal operating data [18,24,25]. However, it may happen that the false alarm rate on the evaluation data is higher than the selected risk of false alarm rate [17,26,27]. This observation underscores the need for threshold-setting approaches that provide formal, data-driven guarantees on the empirical false alarm rate. For Autoencoders, no such known distribution exists, and KDE is commonly used to approximate it [14,28]. However, KDE does not provide any explicit measure of uncertainty associated with the estimated distribution. 

One potential approach for setting detection thresholds is conformal prediction with marginal validity, as proposed by Laxhammar, (2014) [19]. This method offers several advantages [29]: it is model-agnostic, requires minimal assumptions, and provides formal statistical validity at the marginal level, ensuring that the expected proportion of false alarms does not exceed a predefined risk level. This validity is guaranteed under the assumption that the calibration data and the new normal operating conditions data are independently and identically distributed (IID). More recently, Bates et al., (2023) [30] introduced an approach that ensures conditional validity, offering stricter control over the false alarm rate. This approach maintains the same IID assumption between calibration and new normal operating conditions data but strengthens the validity guarantee by ensuring that the false alarm rate remains controlled with high probability across different realizations of the training data, thereby improving robustness in real-world applications. Conformal prediction has been applied to anomaly detection in various domains, including medicine and finance [30]. Conformal prediction has also been utilized for the monitoring of complex physical systems with the objective of reducing false alarm rates while maintaining an acceptable anomaly detection rate. Laxhammar, (2014) [19] introduced the marginal approach for detecting abnormal maritime trajectories, while Smith, (2016) [31] extended this work by first segmenting the fleet into homogeneous subgroups before applying the same approach. Similarly, Farouq et al., (2021), (2022) [32,33] employed the marginal approach to monitor district heating substations, subdividing them into homogeneous units to enhance anomaly detection accuracy. Cai & Koutsoukos, (2020) [34] applied the marginal approach to detect anomalies in advanced emergency braking systems and self-driving end-to-end control vehicles. More recently, Kundacina et al., (2025) [35] implemented the conditional approach for monitoring a thermal power plant, demonstrating its effectiveness in detecting faults while reducing false alarms. These studies rely on a variety of detection models, such as k-nearest-neighbors, OCSVM, Isolation Forest, Variational AE, local outlier factor and support vector data description. The two studies that implement the conditional approach employ non-conformity scores for which lower values correspond to a higher likelihood of abnormality, which is the opposite of the conventional “higher-is-worse” orientation of indices like SPE or Hotelling’s T² commonly used in industrial process monitoring. A systematic search 

revealed no prior work that applies conformal prediction for threshold setting to fault detection in industrial production, leaving a clear gap that our study seeks to fill. 

As emphasized by Chandola et al., (2009) [36], transferring an anomaly-detection technique from one domain to another is rarely straightforward. In particular, the conformal prediction studies cited above adopt a decision logic based on p-values, whereas industrial fault detection typically relies on detection indices and explicit thresholds. This methodological divergence underscores the need to investigate conformal prediction within the specific context of industrial production systems. 

Thus, this study aims to investigate the applicability and effectiveness of conformal prediction for the monitoring of industrial production systems. Specifically, we seek to answer the following research questions: 

- How can conformal prediction be used to set a detection threshold that provides a statistical guarantee on the false alarm rate, irrespective of the underlying data-driven fault-detection model? 

- How does this conformal thresholding strategy perform when compared with the benchmark threshold schemes currently accepted by the industrial fault detection community? 

To address these questions, we conduct a comparative analysis using the well-established TEP benchmark. 

Consequently, the remainder of the paper is structured as follows. Section 2 presents the principles of PCA and AE-based fault detection. Section 3 introduces conformal prediction for fault detection. The methodology used to compare the approaches is presented in Section 4. The results of applying this methodology to the TEP are given in Section 5 . The final section provides conclusions. 

#### **2. Classical methods for fault detection** 

#### _2.1. PCA based fault detection_ 

The aim of PCA is to find a new coordinate system whose axes are aligned with the directions of greatest variance in the data. These axes, called principal components, are orthogonal to each other. To achieve this, the covariance matrix _S_ of the reduced centered training data _X_ ∈ R<sup>_n_×</sup><sup>_m_</sup> is first calculated by [17]: 


![](Reducing_false_alarms_in_fault_detection-_a_comparative_analysis_between_conformal_prediction_and_classical_methods_applied_to_PCA_and_autoencoders_images/conv_f4a22b1a51a40923.pdf-0002-15.png)


Next, it is a matter of finding a matrix _P_ and a diagonal matrix _Λ_ such that: 


![](Reducing_false_alarms_in_fault_detection-_a_comparative_analysis_between_conformal_prediction_and_classical_methods_applied_to_PCA_and_autoencoders_images/conv_f4a22b1a51a40923.pdf-0002-17.png)


The _P_ matrix is called Loadings and contains the coordinates of the principal components in the original coordinate system. The Λ matrix contains the eigenvalues that make up the variance explained by each principal component _λj_ such that: 


![](Reducing_false_alarms_in_fault_detection-_a_comparative_analysis_between_conformal_prediction_and_classical_methods_applied_to_PCA_and_autoencoders_images/conv_f4a22b1a51a40923.pdf-0002-19.png)


There are as many principal components and eigenvalues as there are variables in the _X_ data. However, in fault detection, an important step is to select a number of principal components that is smaller than the number of variables in the data. To do this, four main methods are applied: percentage of explained variance, parallel analysis, scree test and the Prediction Residual Sum of Squares (PRESS) statistics [26]. 

If _P_ ʹ and Λʹ denote the matrices obtained by eliminating the nonretained components, the T² of each sample _xi_ can be calculated as follows: _T_<sup>2</sup> ( _xi_ ) = _xiTP_ ʹΛʹ− 1 _P_ ʹ _Txi._ (4) 

2 

> _A.R. Diallo et al.                                                                                                                                                                                                                                Journal of Process Control 152 (2025) 103495_ 

Similarly, the SPE of the sample _xi_ can be calculated as follows: 


![](Reducing_false_alarms_in_fault_detection-_a_comparative_analysis_between_conformal_prediction_and_classical_methods_applied_to_PCA_and_autoencoders_images/conv_f4a22b1a51a40923.pdf-0003-02.png)


Once the number _p_ of principal components to be retained has been chosen with _p < m_ , the detection limits of SPE and T² statistic can be calculated. Let us define: 


![](Reducing_false_alarms_in_fault_detection-_a_comparative_analysis_between_conformal_prediction_and_classical_methods_applied_to_PCA_and_autoencoders_images/conv_f4a22b1a51a40923.pdf-0003-04.png)



![](Reducing_false_alarms_in_fault_detection-_a_comparative_analysis_between_conformal_prediction_and_classical_methods_applied_to_PCA_and_autoencoders_images/conv_f4a22b1a51a40923.pdf-0003-05.png)


where _Q_ is the distribution of the SPE of normal operating data. Thus, for a risk _α_ of false alarm rate, a detection threshold _Qα_ for SPE is: 


![](Reducing_false_alarms_in_fault_detection-_a_comparative_analysis_between_conformal_prediction_and_classical_methods_applied_to_PCA_and_autoencoders_images/conv_f4a22b1a51a40923.pdf-0003-07.png)


where _cα_ is the (1 − _α_ ) quantile of the normal distribution. This result is obtained by assuming that the data follow a multivariate normal distribution, and _θ_ 1 is very large but remains true regardless of the number of principal components retained [18]. 

As for T² statistic, Tracy et al., (1992) [38] have shown that when the data follow a multivariate normal distribution, then: 


![](Reducing_false_alarms_in_fault_detection-_a_comparative_analysis_between_conformal_prediction_and_classical_methods_applied_to_PCA_and_autoencoders_images/conv_f4a22b1a51a40923.pdf-0003-10.png)


with _Fp,n_ − _p_ the Fisher-Snedecor distribution with _p_ and _n_ − _p_ degrees of freedom. In the same way, for a risk _α_ of false alarm rate, a detection threshold can be set as follows: 


![](Reducing_false_alarms_in_fault_detection-_a_comparative_analysis_between_conformal_prediction_and_classical_methods_applied_to_PCA_and_autoencoders_images/conv_f4a22b1a51a40923.pdf-0003-12.png)


with _Fp,n_ − _p_ ; _α_ being the (1 − _α_ ) quantile of the _Fp,n_ − _p_ distribution. While the above detection limits are still the most widely used for PCA, there are others based on other assumptions. A more complete review of these detection limits can be found in [18]. 

#### _2.2. AE based fault detection_ 

AE is a neural network whose objective is to reconstruct input data after a phase of data dimension reduction. It consists of an encoder and a decoder. The encoder reduces the dimension of the data by finding a non-linear function _f_ that associates each sample _x_ ∈ R<sup>m</sup> with a sample _z_ = _f_ ( _x_ ) with _z_ ∈ R<sup>_q_</sup> such that _q < m_ . The decoder reconstructs the data from this reduced space by finding a non-linear function _g_ which allows for calculating an _x_ ∈ R<sup>m</sup> for any _z_ ∈ R<sup>_q_</sup> such that _x_ = _g_ ( _z_ ) _._ The parameters of functions _f_ and _g_ are learned simultaneously by minimizing a loss function. Several loss functions can be used to achieve this. One of the most commonly used is: 


![](Reducing_false_alarms_in_fault_detection-_a_comparative_analysis_between_conformal_prediction_and_classical_methods_applied_to_PCA_and_autoencoders_images/conv_f4a22b1a51a40923.pdf-0003-16.png)


PCA, is the detection index most associated with AE [14,28]. For any sample, it is defined as the Euclidian norm (or its square) of the difference between the sample _xi_ and its reconstruction _xi_ by the AE: 


![](Reducing_false_alarms_in_fault_detection-_a_comparative_analysis_between_conformal_prediction_and_classical_methods_applied_to_PCA_and_autoencoders_images/conv_f4a22b1a51a40923.pdf-0003-18.png)


Similarly, some authors have defined a T² index for AE in reduced space as follows [14,28]: _T_<sup>2</sup> ( _xi_ ) = ( _zi_ − _Z_ )<sup>_T_</sup> Σ<sup>−1</sup> ( _zi_ − _Z_ ) (14) 

where _zi_ = _f_ ( _xi_ ), _Z_ and Σ are the mean and the covariance of the prediction of the training data by the encoder. In some studies, however, it is denoted as H² and is sometimes defined as the Euclidean norm in reduced space [14]. 

Unlike PCA, where a parametric approach is adopted for setting the detection threshold, for AE no assumptions are made about the detection index distribution. In the majority of studies, KDE is used to estimate the distribution of the normal operating data of the selected detection index [14,28]. Let _I_ ( _xi_ ) denote the detection index of the sample _xi_ belonging to the normal operating data used to train the AE. The probability density _ph_ of this detection index, when the process is operating normally, can be estimated by [1]: 


![](Reducing_false_alarms_in_fault_detection-_a_comparative_analysis_between_conformal_prediction_and_classical_methods_applied_to_PCA_and_autoencoders_images/conv_f4a22b1a51a40923.pdf-0003-22.png)


where _K_ is a kernel function and _h_ is the bandwidth that needs to be optimized. 

#### **3. Conformal prediction for fault detection** 

Conformal prediction is an approach to quantify uncertainties through prediction sets for any prediction model [39,40]. It has the advantage of making no assumptions about data distribution and is applicable to any prediction model. It provides a statistical guarantee on the prediction sets created [39]. Originally founded for classification and regression problems, it was adapted for anomaly detection by Laxhammar, (2014) [19]. In the remainder of this article, we focus on conformal prediction for anomaly detection. 

Unlike fault detection, where the detection threshold is calculated with the same data used to train the machine learning model, conformal prediction recommends reserving part of the training data for threshold estimation. This part of the training data, called calibration data, is crucial for achieving the statistical validity provided by the conformal prediction framework. Another difference between conformal prediction and fault detection is the use of the p-value rather than a detection threshold. However, using either the p-value or a threshold leads to the same result if calculated on the same data. 

The conformal prediction approach recommends subdividing the _X_ data from the previous section into _Xtrain_ and _Xcalib_ . The _Xtrain_ data are used for machine learning models, such as a PCA or AE or any other anomaly detection model. This model is associated with a detection index called a non-conformity score in the lexicon of conformal prediction. It measures how different a sample is from a reference set. We use here the convention of Bates et al., (2023) [30] where a small non-conformity score characterizes an outlier sample. It is worth mentioning that, as the non-conformity measure is thus defined, it is the opposites of the SPE and T² statistic that can constitute non-conformity scores. The p-value _p_ ( _x_ ) for any sample _x_ is calculated by: 


![](Reducing_false_alarms_in_fault_detection-_a_comparative_analysis_between_conformal_prediction_and_classical_methods_applied_to_PCA_and_autoencoders_images/conv_f4a22b1a51a40923.pdf-0003-28.png)


where the operator |E| denotes the cardinal of the set E and _s_ ( _x_ ) is the nonconformity score assigned to sample _x_ by the detection model. For a tolerated false alarm rate _α_ , a fault is detected if _p_ ( _x_ ) ≤ _α_ . This is 

The reconstruction error, often noted as SPE by analogy with the 

3 

> _A.R. Diallo et al.                                                                                                                                                                                                                                Journal of Process Control 152 (2025) 103495_ 

equivalent to setting a detection threshold _q_ as follows [39]: 


![](Reducing_false_alarms_in_fault_detection-_a_comparative_analysis_between_conformal_prediction_and_classical_methods_applied_to_PCA_and_autoencoders_images/conv_f4a22b1a51a40923.pdf-0004-02.png)


where a quantile is a cutoff value that splits a data set so that a chosen proportion of the samples lies below it, _si_ = _s_ ( _Xi_ ) for _Xi_ ∈ _Xcalib_ and _nc_ = | _Xcalib_ |. A fault is detected if _s_ ( _x_ ) ≤ _q_ . Proceeding in this way yields an explicit finite-sample guarantee on false alarms: under normal operating conditions, the probability that a new observation is erroneously flagged as faulty does not exceed _α_ : 


![](Reducing_false_alarms_in_fault_detection-_a_comparative_analysis_between_conformal_prediction_and_classical_methods_applied_to_PCA_and_autoencoders_images/conv_f4a22b1a51a40923.pdf-0004-04.png)


However, this guarantee is “marginal”, i.e., Eq. (18) is only valid on average [30]. In fact, the false alarm rate, as a function of _α_ risk and calibration data size, follows a beta distribution with parameters _l_ = ⌊( _nc_ +1) _α_ ⌋ and _nc_ + 1 − _l_ : _FAR_ ( _α_ ; _nc_ ) ∼ _Beta_ ( _l, nc_ +1 − _l_ ) [30,40]. Fig. 1 shows this distribution for different sizes of calibration data and for the two false alarm risks most commonly used in fault detection. Beyond the greater dispersion observed for the threshold corresponding to a 1 % false alarm risk, we can see that with a small amount of calibration data, the false alarm rate is, on average, more tightly controlled. However, this comes at the cost of a higher probability of generating extreme false alarms that significantly exceed the target. 

Consequently, Bates et al., (2023) [30] proposed a stronger guarantee called “conditional”. The proposal of these authors makes it possible to construct an upper confidence limit with a certain probability of being greater than the empirical false alarm rate. Thus, by using this upper confidence limit to set the detection threshold, we are guaranteed that a significant proportion of normal data will have a non-conformity score above this threshold. 

The empirical Cumulative Distribution Function (CDF) _F_ of the nonconformity scores, which gives the empirical false alarm rate on the calibration data if _s_ is set as the detection threshold, is given by: 


![](Reducing_false_alarms_in_fault_detection-_a_comparative_analysis_between_conformal_prediction_and_classical_methods_applied_to_PCA_and_autoencoders_images/conv_f4a22b1a51a40923.pdf-0004-08.png)


where 1( • ) is the indicator function. The objective is to find a piecewise constant adjustment function _h_ ∶ [0 _,_ 1]↦ [0 _,_ 1] such that for _δ_ ∈(0 _,_ 1): 

ℙ[ _F_ ( _s_ ( _x_ )) ≤ _h_ ( _F_ ( _s_ ( _x_ ))) | _x belongs to the normal data_ ] ≥ 1 − _δ_ (20) 

where _F_ and _s_ are respectively the true CDF and the true non-conformity 

score, which are estimated on the calibration data by _F_ and by _s_ respectively [30]. The function _h_ can be defined using, for example, the upper bound of the DKW inequality [41]: 


![](Reducing_false_alarms_in_fault_detection-_a_comparative_analysis_between_conformal_prediction_and_classical_methods_applied_to_PCA_and_autoencoders_images/conv_f4a22b1a51a40923.pdf-0004-13.png)


> where _ε_ = <u>√2l</u> ~~n~~ _n_ <u>2</u> _<u>δc</u>_ and _C_ = 2 as shown by Massart, (1990) [42]. The DKW approach offers very strict false alarm rate control for small false alarm rates (which are generally used to set the detection threshold), especially for relatively small calibration data sizes. However, this is at the expense of the ability of the model to detect faults. A less stringent method in this context is the Simes method [30,43]. The Simes adjustment is defined for all _t_ = _F_ ( _s_ ) by: _<u>j</u>_ ⋯( _<u>j</u>_ − _k_ + 1) 1 _/k h_ (1 − _t_ ) = 1 − _δ_<sup>1</sup><sup>_/k_</sup> [ _n_ ⋯( _n_ − _k_ + 1) ] _, j_ = ⌈( _n_ + 1) _t_ ⌉ _._ (22) For the specific purpose of anomaly detection, Bates et al., (2023) [30] set _k_ = ⌈ _<u>n</u>_ 2 _<u>c</u>_<sup>~~⌉~~unlike Sarkar, (2008) [43]where it was set to a small</sup> integer [30]. However, as the empirical false alarm rate increases, or even for certain sizes of calibration data, this method may prove to be more conservative than the DKW approach. For this reason, Bates et al., (2023) [30], have proposed an asymptotic method, which is less conservative, but whose guarantee is only valid for large calibration data sizes. It is defined by: 


![](Reducing_false_alarms_in_fault_detection-_a_comparative_analysis_between_conformal_prediction_and_classical_methods_applied_to_PCA_and_autoencoders_images/conv_f4a22b1a51a40923.pdf-0004-15.png)


where 


![](Reducing_false_alarms_in_fault_detection-_a_comparative_analysis_between_conformal_prediction_and_classical_methods_applied_to_PCA_and_autoencoders_images/conv_f4a22b1a51a40923.pdf-0004-17.png)


where _h_ ∘ _F_ denotes the composition of the adjustment function _h_ with the empirical CDF _F_ . 

A fault is detected if _s_ ( _x_ ) ≤ _q_<sup>ʹ</sup> . 

These methods can be adapted to match the SPE and T² where, unlike the non-conformity score defined in Bates et al., (2023) [30], a large value characterizes the occurrence of a fault. This involves changing the direction of the inequality in (16) while (17) becomes: 


![](Reducing_false_alarms_in_fault_detection-_a_comparative_analysis_between_conformal_prediction_and_classical_methods_applied_to_PCA_and_autoencoders_images/conv_f4a22b1a51a40923.pdf-0004-21.png)


**Fig. 1.** Distribution of false alarm rate as a function of the _nc_ and _α_ (adapted from [30]). 

4 

_Journal of Process Control 152 (2025) 103495_ 

> _A.R. Diallo et al.                                                                                                                                                                                                                                Journal Process Control_ 


![](Reducing_false_alarms_in_fault_detection-_a_comparative_analysis_between_conformal_prediction_and_classical_methods_applied_to_PCA_and_autoencoders_images/conv_f4a22b1a51a40923.pdf-0005-02.png)


The marginal threshold can also be determined from the empirical CDF: 


![](Reducing_false_alarms_in_fault_detection-_a_comparative_analysis_between_conformal_prediction_and_classical_methods_applied_to_PCA_and_autoencoders_images/conv_f4a22b1a51a40923.pdf-0005-04.png)


Similarly, the empirical false alarm rate of the calibration data as a function of the threshold _s_ is now given by the empirical Survival Function (SF) of calibration SPE or T² instead of the CDF. For instance, by using the DKW inequality, an upper confidence bound for the SF of T² or SPE can be constructed with conditional validity. In fact: 


![](Reducing_false_alarms_in_fault_detection-_a_comparative_analysis_between_conformal_prediction_and_classical_methods_applied_to_PCA_and_autoencoders_images/conv_f4a22b1a51a40923.pdf-0005-06.png)


Because the SF satisfies _S_ ( _s_ ) = 1 − _F_ ( _s_ ) and the empirical SF satisfies _S_ ( _s_ ) = 1 − _F_ ( _s_ ), we substitute these identities into the inequality: 


![](Reducing_false_alarms_in_fault_detection-_a_comparative_analysis_between_conformal_prediction_and_classical_methods_applied_to_PCA_and_autoencoders_images/conv_f4a22b1a51a40923.pdf-0005-08.png)


− Next, we multiply each term by 1, which reverses the direction of the inequalities: 


![](Reducing_false_alarms_in_fault_detection-_a_comparative_analysis_between_conformal_prediction_and_classical_methods_applied_to_PCA_and_autoencoders_images/conv_f4a22b1a51a40923.pdf-0005-10.png)


Finally, simplifying each side of the inequality yields: 


![](Reducing_false_alarms_in_fault_detection-_a_comparative_analysis_between_conformal_prediction_and_classical_methods_applied_to_PCA_and_autoencoders_images/conv_f4a22b1a51a40923.pdf-0005-12.png)


Which shows that the DKW inequality holds for the SF as well. 

The flowchart in Fig. 2 summarizes the complete procedure for nonconformity scores such as SPE or T². The offline modeling phase begins with model training on fault-free data, followed by the selection of an independent calibration set and the computation of the conformal quantile that defines the detection threshold. The online monitoring phase shows how each incoming sample is scored, compared with the calibrated threshold, and then either accepted as normal or flagged as a fault. 

#### **4. Comparison Methodology** 

To ensure a fair and rigorous comparison between the traditional threshold-setting approaches and the conformal prediction-based approach, an evaluation framework is established. Both methods are systematically applied to the same dataset, ensuring that any differences in performance are solely attributable to the thresholding technique rather than variations in input data. Fig. 3 provides a visual representation of the two approaches, highlighting their respective training processes while emphasizing their shared training and testing datasets. 

The approaches are compared for setting the detection threshold for PCA and AE. For PCA, the SPE and T² are used as detection indices, while for AE the reconstruction error is employed. To evaluate the performance of the two threshold-setting approaches, we rely on two key indicators: the false alarm rate and the fault detection rate. The false alarm rate (FAR) measures the proportion of normal operating instances that are incorrectly flagged as faults: 


![](Reducing_false_alarms_in_fault_detection-_a_comparative_analysis_between_conformal_prediction_and_classical_methods_applied_to_PCA_and_autoencoders_images/conv_f4a22b1a51a40923.pdf-0005-18.png)


> Ideally, this rate should be less than or equal to the risk level α defined when setting the detection threshold. The fault detection rate (FDR), on the other hand, quantifies the proportion of actual faults that are correctly identified by the model: 


![](Reducing_false_alarms_in_fault_detection-_a_comparative_analysis_between_conformal_prediction_and_classical_methods_applied_to_PCA_and_autoencoders_images/conv_f4a22b1a51a40923.pdf-0005-20.png)


The goal is to maximize this detection rate while maintaining the false alarm rate within acceptable limits. 

These two indicators inherently involve a trade-off: lowering the detection threshold may increase fault detection but at the cost of a higher false alarm rate, while raising the threshold reduces false alarms but may also lead to undetected faults. Therefore, a fair comparison between models must take both metrics into account. Directly 


![](Reducing_false_alarms_in_fault_detection-_a_comparative_analysis_between_conformal_prediction_and_classical_methods_applied_to_PCA_and_autoencoders_images/conv_f4a22b1a51a40923.pdf-0005-23.png)


**Fig. 2.** Workflow of conformal prediction-based threshold setting. 

5 

> _A.R. Diallo et al.                                                                                                                                                                                                                                Journal of Process Control 152 (2025) 103495_ 


![](Reducing_false_alarms_in_fault_detection-_a_comparative_analysis_between_conformal_prediction_and_classical_methods_applied_to_PCA_and_autoencoders_images/conv_f4a22b1a51a40923.pdf-0006-01.png)


**Fig. 3.** Comparison methodology. 

comparing the fault detection rates of two models with very different false alarm rates can be misleading, as a model with a high detection rate may achieve this at the expense of an unacceptably high false alarm rate. 

#### **5. Comparison on the Tennessee Eastman process** 

The Tennessee Eastman Process (TEP) benchmark is widely used for fault detection and diagnosis in industrial systems. Originally introduced by Downs & Vogel, (1993) [44], the TEP is a chemical process designed to simulate a complex industrial plant with multiple interacting components. It consists of five main units: a reactor, a condenser, a compressor, a vapor-liquid separator, and a product stripper as can be 

seen in Fig. 4. The process takes in four reactants (A, C, D and E) and produces two main products (G and H), along with a byproduct (F) and an inert component (B). The highly nonlinear and dynamic nature of the system, along with its multiple control loops, makes it a challenging benchmark for fault detection and diagnosis. The selection of this benchmark is further motivated by the strong fault detection performance of traditional approaches, allowing for a rigorous comparison with conformal prediction methods. However, in certain versions of the benchmark, where the number of available training samples is relatively limited, the observed false alarm rate on the test data is very much higher than the targeted false alarm rate [27]. This enables the evaluation of the behavior of conformal prediction within that context. 


![](Reducing_false_alarms_in_fault_detection-_a_comparative_analysis_between_conformal_prediction_and_classical_methods_applied_to_PCA_and_autoencoders_images/conv_f4a22b1a51a40923.pdf-0006-07.png)


**Fig. 4.** Diagram of the TEP benchmark. 

6 

_Journal of Process Control 152 (2025) 103495_ 

> _A.R. Diallo et al.                                                                                                                                                                                                                                Journal Process Control_ 

Over the years, multiple versions of TEP datasets have been released. In this article, we utilize two versions of the TEP dataset. The first version, proposed by Chiang et al., (2000) [26] consists of simulations of the TEP under normal and faulty conditions, with separate training and test sets for normal operation and each of the 21 predefined faults affecting process variables and control loops. The simulations use a sampling interval of 3 min. Each training simulation runs for 25 h, resulting in 500 samples, while each test simulation lasts 48 h, yielding 960 samples. In the training phase, faults are introduced at the 20th sample (1 h after the start), whereas in the test phase, faults are introduced later, at the 160th sample (8 h after the start). This version of the dataset is the most widely used, and we will refer to it as the standard version. In this dataset, the normal operation as well as each fault are simulated once for both training and testing. 

The second version, proposed by Rieth et al., (2017) [45] follows the same simulation methodology, but each simulation is repeated 500 times with different random seeds to ensure variability in the data. Additionally, only 20 faults are considered instead of the 21 included in the standard version. The fault introduction times remain unchanged (20th sample in training, 160th sample in testing). This version, which we will refer to as the extended version, was generated to enable a more rigorous evaluation of fault detection models. Using a single simulation for training and a single simulation for evaluation can result in a biased evaluation [27]. 

In the remainder of this article, we compare the traditional threshold-setting approach with the conformal prediction approach. This comparison is mainly based on the false alarm rate. In a second step, we will also provide the fault detection rate. 

#### _5.1. PCA trained on the normal operating conditions of the standard version_ 

A PCA model was trained using the normal operating conditions simulation from the training data of the standard version (500 samples). The parallel analysis method was applied to determine the optimal number of principal components, leading to the selection of 11 components. Traditional threshold-setting approaches described in 2.1 were employed to fault detection, considering two detection indices: SPE and T² statistic. For each index, two thresholds were defined: one corresponding to a 1 % false alarm risk and the other to a 5 % false alarm risk. 

Additionally, a second PCA model was trained using the conformal prediction approach. In this case, 20 % of the normal operation training data (100 samples) were randomly selected and used as a calibration set, while the remaining 80 % were used for training (400 samples). The parallel analysis method was again applied, leading to the retention of 11 principal components. 

Both PCA models were evaluated on the normal operating conditions simulation (500 samples) from the test data of the standard version to assess their performance under fault-free conditions. The obtained false alarm rates for each detection index and threshold, are presented in Table 1. 

The results presented in Table 1 indicate that for both PCA models, the observed false alarm rates at each threshold largely exceed the expected α-risk levels. The only exception is observed for the 1 % false alarm risk threshold based on T² statistic, where the marginal conformal prediction approach achieves a false alarm rate of 0.94 %. On the one hand, this exception is consistent with the theoretical result presented in Section 3, which indicated that a limited size of calibration data can 

**Table 1** 

FAR (%) of the PCA models trained with limited data (500 samples). 

||**_α_** = **_1_**%||**_α_** =**_5_**%||
|---|---|---|---|---|
|Approach|SPE|T²|SPE|T²|
|Traditional|7.08|1.67|20.10|7.60|
|Marginal|7.19|0.94|14.79|12.29|



produce an empirical false alarm rate below the target. On the other hand, these results are consistent with previous studies [27], such as Chiang et al., (2000) [26] and Yin et al., (2012) [17], where empirical false alarm rates were also reported to be higher than the target. One potential explanation is that the training data may not be sufficient to fully capture the complexity of the TEP, leading to an underestimation of process variability in the normal operating conditions. 

Before assessing this hypothesis, we first tested the usefulness of conditional methods of conformal prediction in this context. Fig. 5 illustrates the empirical survival function estimated using the calibration data, which corresponds to the false alarm rate as a function of the detection threshold when using the SPE. The survival function obtained from the test data is also plotted for comparison. Additionally, the SPE values for each sample from the training, calibration, and test datasets are displayed on the figure. To enhance readability, these three groups of samples are represented arbitrarily at different positions along the false alarm rate axis. 

Using the calibration samples, upper confidence bounds for the empirical survival function were constructed based on the three methods presented in Section 3: an asymptotic approach, Simes method, and the DKW method. These bounds were computed to contain the true survival function with a probability of 90 % (i.e., δ = 0.1). It can be seen that the survival function obtained from the test data is consistently distant from that of the calibration data, and in certain segments, it even exceeds the upper confidence bounds. That upward excursions are chiefly a consequence of the limited training sample: with too few normal samples, the PCA model cannot fully capture the true operating variability of the process. This mismatch shifts the distribution of the SPE in the test data relative to the calibration data, causing occasional boundary violations. The same pattern, false alarm rates well above the target level α, appears for the classical threshold-setting rules (Table 1), indicating that the root cause is the quality of the normal model under data scarcity, not a failure of the conformal bounds themselves. 

Focusing specifically on the low false alarm rate region, which is particularly relevant for setting detection thresholds, it is observed that the asymptotic upper bound lies below the test data survival function. This can be explained by the fact that the asymptotic bound is only valid when a sufficiently large calibration dataset is available. Similarly, the upper bound obtained using Simes method also falls below the survival function of the test data in this region. However, in contrast to the asymptotic method, Simes approach indicates that, given the available calibration data, setting the detection threshold at the maximum SPE value observed in the calibration set provides a 90 % probability that the actual false alarm rate does not exceed 4.5 %. The DKW method, which is more conservative, yields an upper bound that is closer to the survival function of the test samples. It suggests that, with a 90 % probability, the actual false alarm rate remains below 12 % when using the maximum calibration SPE as the detection threshold. 

Empirically, setting the detection threshold at the maximum SPE value observed in the calibration set results in a false alarm rate of 7.19 %, which is higher than the guarantee provided by the Simes bound but lower than that of the DKW bound. This result highlights that, despite the limited availability of both training and calibration data, the DKW method provides a reliable false alarm rate guarantee. Furthermore, unlike traditional method, which does not offer confidence guarantees before evaluating the false alarm rate on test data, the conformal calibration approach allows for an estimation of the expected variability in false alarm rates, thereby offering a more informed threshold setting process. 

To further investigate the hypothesis that the low quantity of training data is the cause of the high false alarm rate, we will increase the training dataset by randomly selecting five normal operating conditions simulations from the 500 available simulations in the training set of the extended version. This strategy aims to assess whether a larger and more diverse training dataset can improve the generalization capabilities of the PCA models and yield false alarm rates that more closely 

7 

> _A.R. Diallo et al.                                                                                                                                                                                                                                Journal of Process Control 152 (2025) 103495_ 


![](Reducing_false_alarms_in_fault_detection-_a_comparative_analysis_between_conformal_prediction_and_classical_methods_applied_to_PCA_and_autoencoders_images/conv_f4a22b1a51a40923.pdf-0008-01.png)


**Fig. 5.** Upper confidence bound for the FAR with limited training data (500 samples). 

align with the expected α-risk levels. 

#### _5.2. PCA trained on five simulations from the extended version_ 

Five normal operation simulations from the extended version are randomly selected, each containing 500 samples, and used in both the traditional approach and the conformal prediction approach. In the traditional approach, all five simulations (2500 samples) are used to train the PCA model and establish detection thresholds. 

In the conformal prediction approach, the PCA model is trained using only three of these five simulations (1500 samples), while the remaining two simulations (1000 samples) are used for calibration. The assignment of simulations to the training and calibration sets is randomly determined to ensure a fair evaluation of both approaches. 

Both PCA models are then evaluated on the same normal operation simulation from the test data of the standard version (500 samples) as in the previous subsection, allowing for a direct comparison of the results. The obtained false alarm rates, summarized in Table 2, provide insights into the impact of using a bigger training dataset. 

Indeed, the results presented in Table 2 indicate a huge reduction in false alarm rates across all detection thresholds compared to the previous experiment. This improvement is particularly noticeable for the 1 % false alarm risk thresholds, where the observed false alarm rates, although still slightly exceeding the expected risk level, are now much closer to it. For instance, in the traditional approach, the false alarm rate for the SPE-based threshold at 1 % risk decreased from 7.08 % to 1.67 %, while in the conformal prediction approach, it dropped from 7.19 % to 1.46 %. 

These results suggest that both approaches benefit from the increased amount of training data, leading to a better characterization of the normal operating conditions of the process. This improvement is also noticeable in Fig. 6, which presents upper confidence bounds for the 

##### **Table 2** 

FAR (%) of the new PCA models on the test set of the standard version. 

||**_α_** =**_1_**%||**_α_** = **_5_**%||
|---|---|---|---|---|
|Approach|SPE|T²|SPE|T²|
|Traditional|1.67|1.56|7.50|6.35|
|Marginal|1.46|1.88|6.56|7.60|
|Asymptotic (_δ_=0_._2)|0.94|0.83|5.62|5.83|



empirical survival function of the SPE statistics computed on the calibration data. Compared to the previous case, the gap between the survival function of the test data and that of the calibration data has narrowed, indicating a better alignment between the two distributions. Additionally, the asymptotic and Simes bounds are now much closer to the empirical survival function of the test data. 

To further quantify this improvement, the detection thresholds were computed using the asymptotic method with δ = 0.2, resulting in false alarm rates below 1 % for both the SPE and Hotelling’s T² statistics at the 1 % target risk level (Table 2). However, the confidence bounds displayed in Fig. 5 were constructed with δ = 0.1 to allow for a direct comparison with Fig. 4. This improvement in data availability is also reflected in the guarantees provided by the Simes and DKW methods when setting the detection threshold at the maximum SPE value observed in the calibration data, which now ensure that the false alarm rate remains below 0.46 % and 3.87 %, respectively. Notably, the observed false alarm rate when applying this threshold is 0.21 %, which remains well below the upper bounds provided by these two methods. These results highlight how increasing the amount of training data reduces the uncertainty in false alarm rate estimation and enhances the reliability of threshold setting. 

#### _5.3. PCA and AE trained on the whole extended version_ 

In this section, a PCA model is trained on all 500 normal operation simulations (250000 samples) from the training set of the extended version. For the conformal prediction approach, 400 simulations (200000 samples) are randomly selected for training, while the remaining 100 simulations (50000 samples) are reserved as calibration data for threshold setting. 

Unlike previous experiments, the number of retained principal components is varied to assess its impact on the false alarm rate. Specifically, the 11 components used in earlier subsections are tested, along with those determined by parallel analysis, which now suggests 12 components based on the extended dataset. Additionally, a varianceexplained criterion is applied, selecting the number of components that account for 75 %, 80 %, 85 %, and 90 % of the total variance, corresponding to 22, 25, 28, and 31 components, respectively. 

All models are evaluated on the 500 normal operation simulations (480000 samples) from the test set of the extended version, and the 

8 

_Journal of Process Control 152 (2025) 103495_ 

> _A.R. Diallo et al.                                                                                                                                                                                                                                Journal Process Control_ 


![](Reducing_false_alarms_in_fault_detection-_a_comparative_analysis_between_conformal_prediction_and_classical_methods_applied_to_PCA_and_autoencoders_images/conv_f4a22b1a51a40923.pdf-0009-02.png)


**Fig. 6.** Upper confidence bound for the FAR when 5 simulations (2500 samples) are used for the training. 


![](Reducing_false_alarms_in_fault_detection-_a_comparative_analysis_between_conformal_prediction_and_classical_methods_applied_to_PCA_and_autoencoders_images/conv_f4a22b1a51a40923.pdf-0009-04.png)


**Fig. 7.** Boxplot of false alarm rates (%) (α = 1 %, δ = 0.2 for Conditional Methods). 

**Table 3** 

Impact of the number of retained PCs on the FAR (%). 

|||**_α_** =**_1_**%||**_α_** = **_5_**%||
|---|---|---|---|---|---|
|Approach|Components|SPE|T²|SPE|T²|
|Traditional|11|0.96|1.15|4.98|5.46|
||12|0.94|1.12|4.96|5.49|
||22|0.96|1.05|4.98|5.28|
||25|0.95|1.05|4.99|5.28|
||28|0.92|1.04|4.94|5.29|
||31|0.92|1.04|5.01|5.24|
|Marginal|11|1.11|1.11|5.05|5.22|
||12|1.02|1.14|5.10|5.35|
||22|0.98|1.17|4.93|5.27|
||25|0.95|1.15|5.06|5.23|
||28|0.99|1.12|4.86|5.19|
||31|0.99|1.12|4.86|5.19|



results are summarized in Table 3. Notably, in the traditional approach, when using SPE as the detection index, the empirical false alarm rate remains below the nominal risk level ( _α_ ) for most models. The only exception is the model retaining 31 components (90 % variance explained), where the false alarm rate for the 5% risk threshold slightly exceeds the expected value. 

When using Hotelling’s T² statistic, the false alarm rate consistently exceeds α, though to a lesser extent than in previous experiments. This observation aligns with findings in the literature, where T² is known to be more prone to false alarms than SPE [18,46]. A similar trend is observed in the marginal conformal prediction approach, where T² leads to false alarm rates above _α_ for all models, whereas SPE exhibits fluctuations around _α_ . 

The PCA model with 12 principal components, selected via parallel analysis, was applied to compute the false alarm rate on the test data of the extended version (Table 4). In addition to the traditional approach 

9 

_Journal of Process Control 152 (2025) 103495_ 

> _A.R. Diallo et al.                                                                                                                                                                                                                                Journal Process Control_ 

##### **Table 4** 

FAR (%) on the test set of the extended version. 

||**_α_** = **_1_**%||**_α_** =**_5_**%||
|---|---|---|---|---|
|Approach|SPE|T²|SPE|T²|
|Traditional|0.94|1.12|4.96|5.49|
|Marginal|1.02|1.14|5.10|5.35|
|DKW (δ=0.2)|0.55|0.62|4.56|4.83|
|Asymptotic (δ=0.2)|0.90|1.02|4.84|5.09|
|Simes (δ=0.2)|0.75|0.83|3.54|3.84|



and the marginal conformal approach, the conditional conformal approach was also employed, comparing three adjustment functions: DKW, asymptotic, and Simes. With this model, the marginal conformal method consistently resulted in false alarm rates exceeding the target for both detection indices (SPE and T² statistic) and for both false alarm risk levels, thus underscoring the potential benefits of the conditional approach. In particular, the conditional methods using DKW and Simes achieved a very strict control, yielding false alarm rates consistently below the nominal risk, whereas the asymptotic method proved more lenient, yielding a false alarm rate slightly above the target when using T². It is important to note that this tighter control of false alarms naturally comes at the expense of a modest reduction in fault detection rates as we will see later (Table 7); however, the differences are not substantial, especially when considering the inherent imbalance between normal operation and the rare occurrence of faults in the industrial reality. 

To evaluate the confidence level associated with the guarantees in Eq. (20) we used the same test dataset as in Table 4. Rather than aggregating all samples, we now compute the FAR for every simulation individually and record the proportion of simulation whose FAR exceeds the nominal risk level _α_ = _δ_ = 1%. With the confidence parameter set to 0 _._ 2 for the conditional rules, the exceedance frequencies are 

- Traditional: 41.2 % 

- Marginal: 48.2 % 

- Asymptotic: 36.4 % 

- Simes: 24.0 % 

- DKW: 8.4 % 

These findings show that the non-asymptotic conditional methods (Simes and DKW) provide better control of the FAR variability, with DKW offering a conservative control compatible with δ= 0.2. In contrast, the asymptotic conditional method exceeds the expected bound more frequently, which is coherent with the fact that its guarantee only holds for very large calibration sets. Importantly, the traditional method, commonly used for threshold setting performs worse in terms of FAR control than the conditional method. The marginal conformal method still respects its theoretical guarantee on average since the mean FAR across all simulations remains close to _α_ = 1%; nevertheless 48.2 % of the individual simulations violate the target, illustrating the limitation of a purely marginal guarantee when stricter control is required. Fig. 6 shows box plots of the FAR distributions for all five methods and confirms the superior stability of the finite-sample conditional approaches. 

The impact of calibration data in the marginal approach on the false alarm rate is summarized in Table 5 for the PCA model with 12 principal components. By randomly splitting the training data into proper training and calibration sets ten times, we assessed the stability of false alarm rates obtained using conformal prediction. The computed means and standard deviations reveal some variability in the results depending on the data partitioning. For a detection threshold corresponding to α = 1 %, the mean false alarm rate is 1.03 % for SPE and 1.09 % for Hotelling’s T², with standard deviations of 0.07 % and 0.08 %, respectively. For α = 5 %, the mean rates are 5.13 % and 5.24 %, with standard deviations of 0.17 % and 0.18 %. These results show that the 

##### **Table 5** 

Impact of data splitting on the FAR (%) in marginal conformal prediction. 

||**_α_** = **_1_**%||**_α_** = **_5_**%||
|---|---|---|---|---|
|Random split|SPE|T²|SPE|T²|
|1|1.02|1.14|5.10|5.35|
|2|1.04|1.07|4.89|5.12|
|3|1.11|0.96|5.30|4.93|
|4|1.08|1.13|5.08|5.33|
|5|0.95|1.20|5.22|5.57|
|6|0.96|1.03|5.00|5.15|
|7|1.07|1.04|5.26|5.02|
|8|1.16|1.19|5.46|5.28|
|9|0.92|1.15|5.01|5.40|
|10|1.00|1.02|4.94|5.21|
|**Mean**|**1.03**|**1.09**|**5.13**|**5.24**|
|**Standard deviation**|**0.07**|**0.08**|**0.17**|**0.18**|
|**Best relative gap**|**8.00**|**4.00**|**2.20**|**1.40**|
|**Worst relative gap**|**¡16.00**|**¡20.00**|**¡9.20**|**¡11.40**|



calibration data in marginal conformal prediction introduce additional variability in threshold estimation. To better characterize this variability, we will express it as a percentage of the target false alarm rate. We thus introduced two additional indicators beyond the mean and standard deviation of the observed false alarm rates: the best and the worst relative gaps. These metrics respectively quantify how much lower or higher the empirical false alarm rate deviates from the target, expressed as a percentage of the target. A positive best relative gap indicates that the false alarm rate is safely below the target in the most favorable case, while a negative worst relative gap reveals how much the method can exceed the target in the least favorable case. A negative best relative gap indicates that the false alarm rate was higher than the target in the most favorable case, while a positive worst relative gap indicates that the false alarm rate was lower than the target in the least favorable case. They are computed as follows: 


![](Reducing_false_alarms_in_fault_detection-_a_comparative_analysis_between_conformal_prediction_and_classical_methods_applied_to_PCA_and_autoencoders_images/conv_f4a22b1a51a40923.pdf-0010-18.png)


As shown in Table 5, the best relative gaps are consistently positive across all configurations, with values up to 8 % for the SPE and 4 % for the T² statistic at the 1 % target, and 2.2 % for SPE and 1.4 % for T² at the 5 % target. These values confirm that the conformal approach can, under certain calibrations, achieve very conservative false alarm control. However, the worst relative gaps reveal the potential risks: at the 1 % target, false alarm rates exceeded the target by up to 16 % for SPE and 20 % for T², while at the 5 % level, the exceedances were 9.2 % and 11.4 %, respectively. These results highlight the sensitivity of the marginal conformal method to the specific calibration subset used and reinforce the importance of considering uncertainty when setting the detection threshold. 

Following the previous analysis of calibration data influence, we now examine the impact of calibration data size on the stability of false alarm rate estimates. Table 6 presents the false alarm rates obtained using the marginal conformal prediction approach for different numbers of principal components and varying sizes of the calibration dataset. 

A key observation is that reducing the number of calibration samples leads to an increase in the variability of the false alarm rate. This is reflected in the standard deviations, which are higher for smaller calibration datasets. For instance, when using only 50 calibration simulations (25000 samples), the standard deviation of the false alarm rate at the 1 % risk level is 0.08 % for SPE and 0.03 % for T². These values decreased to 0.03 % and 0.02 % respectively, when 250 calibration simulations (125000 samples) were used, demonstrating improved stability in the empirical false alarm rates. 

As for the mean, no clear trend emerged. Indeed, for the 5 % threshold on the SPE, the model with the least calibration data had the 

10 

_Journal of Process Control 152 (2025) 103495_ 

> _A.R. Diallo et al.                                                                                                                                                                                                                                Journal Process Control_ 

##### **Table 6** 

Impact of the calibration data size on the FAR (%) in marginal conformal prediction. 

|Calibration size||**_α_** =**_1_**%||**_α_** = **_5_**%||
|---|---|---|---|---|---|
|250 simulations|Number of|SPE|T²|SPE|T²|
|(125000 samples)|PCs|||||
||11|1.06|1.11|5.10|5.20|
||12|1.02|1.11|5.08|5.26|
||22|0.98|1.08|5.06|5.19|
||25|0.97|1.07|5.05|5.21|
||28|1.02|1.06|5.05|5.22|
||31|1.02|1.06|5.05|5.22|
||**Mean**|**1.01**|**1.08**|**5.07**|**5.22**|
||**Standard**<br>**deviation**|**0.03**|**0.02**|**0.02**|**0.02**|
||**Best relative**<br>**gap**|**3.00**|**¡6.00**|**¡1.00**|**¡3.80**|
||**Worst**|**¡6.00**|**¡11.00**|**¡2.00**|**¡5.20**|
||**relative gap**|||||
|100 simulations|11|1.11|1.11|5.05|5.22|
|(50000 samples)|12|1.02|1.14|5.10|5.35|
||22|0.98|1.17|4.93|5.27|
||25|0.95|1.15|5.06|5.23|
||28|0.99|1.12|4.86|5.19|
||31|0.99|1.12|4.86|5.19|
||**Mean**|**1.01**|**1.14**|**4.98**|**5.24**|
||**Standard**<br>**deviation**|**0.05**|**0.02**|**0.10**|**0.06**|
||**Best relative**|**5.00**|**¡11.00**|**2.80**|**¡3.80**|
||**gap**|||||
||**Worst**<br>**relative gap**|**¡11.00**|**¡17.00**|**¡2.00**|**¡7.00**|
|50 simulations|11|1.15|1.14|5.12|5.52|
|(25000 samples)|12|1.01|1.19|5.19|5.60|
||22|0.91|1.21|4.92|5.44|
||25|0.94|1.15|5.06|5.56|
||28|1.01|1.20|4.96|5.48|
||31|1.01|1.20|4.96|5.48|
||**Mean**|**1.01**|**1.18**|**5.04**|**5.51**|
||**Standard**|**0.08**|**0.03**|**0.10**|**0.05**|
||**deviation**|||||
||**Best relative**<br>**gap**|**9.00**|**¡14.00**|**1.60**|**¡8.80**|
||**Worst**|**¡15.00**|**¡21.00**|**¡3.80**|**¡12.00**|
||**relative gap**|||||



lowest mean of 5.04 %, while the model with the most calibration data had a mean of 5.07 %. This contrasts with the T² thresholds, where the means decreased as the size of the calibration data increased. For the 1 % threshold on the SPE, the three scenarios had the same mean. As in the previous analysis concerning the impact of calibration data selection, we computed the best and worst relative gaps to further evaluate the influence of calibration data size on the control of false alarm rates. The results show that with 50 calibration simulations, the marginal conformal approach remains more conservative in some cases than when using larger calibration sets. This is illustrated by the best relative gap observed for the SPE at the 1 % target level, which reaches 9 %. In comparison, the best relative gaps at the same risk level for calibration sizes of 100 and 250 simulations are 5 % and 3 %, respectively. Such conservatism aligns with conformal prediction theory, which anticipates that smaller calibration sets yield more conservative decisions but with greater uncertainty and variability. This trade-off becomes clear when we look at the worst relative gaps of the same risk level. Using a calibration set of 50 simulations results in a worst-case relative gap of − 15 %, meaning that the false alarm rate can climb up to 1.15 %. By contrast, the worst relative gaps decrease to − 11 % and − 6 % when the calibration size increases to 100 and 250 simulations, respectively. 

In summary, increasing the size of the calibration dataset enhances the stability of false alarm rate estimates by reducing the likelihood of extreme deviations from the target. This supports the idea that calibration data plays a critical role in enabling reliable threshold selection and effective false alarm control. However, in practical industrial 

settings, expanding the calibration set often comes at the cost of reducing the training data, given the limited availability of historical samples. This trade-off was also present in our study, where larger calibration sets meant fewer samples for training. Although this had a minimal impact in our case, thanks to the relatively large total dataset available, such a compromise can significantly affect the ability of the model to accurately learn the normal operating conditions of the process when data are scarce. Indeed, as shown in Section 5.1, when the model is insufficiently trained, refining the detection threshold using the marginal conformal prediction method offers little benefit. 

The PCA model with 12 principal components, for which 100 simulations were used for calibration, is employed to calculate the fault detection rate using the test data from the extended version. The results are shown in Table 7. An important observation from Table 7 is that, despite T² generating higher false alarm rates for both approaches, it does not lead to improved fault detection performance for 12 out of the 20 faults. This suggests that the additional variability captured by T² does not systematically translate into better fault sensitivity. Moreover, this behavior is consistent across both approaches, indicating that the relative effectiveness of T² and SPE (at least for this case study) remains stable regardless of the methodology used for threshold setting. 

Following the same methodology, an AE was trained for fault detection. The implementation was performed using the PyOD library [47]. The model was trained with default hyperparameters and for both the traditional approach and the conformal prediction approach, the same random seed was used. For the traditional approach, a KDE was applied to the training data to estimate the distribution of reconstruction errors. This was implemented using the statsmodels library [48], employing a Gaussian kernel. The optimal bandwidth was used to ensure an appropriate balance between bias and variance in density estimation [1]. 

The results presented in Table 8 indicate that the KDE method yields a false alarm rate slightly higher than the target risk level for both thresholds considered. Similarly, the marginal conformal prediction approach also produces false alarm rates that exceed the expected risk, but they remain consistently lower than those obtained with KDE for both the 1% and 5% thresholds. In contrast, the conditional conformal prediction approaches successfully provide false alarm rates below the target level, demonstrating their ability to effectively control the false alarm rate. 

The results in Table 9 highlight the trade-off between false alarm rate control and fault detection performance. As expected, the KDE-based method, which exhibits a higher false alarm rate, achieves the highest detection rates across all 20 faults. The marginal conformal prediction approach provides a better balance, yielding detection rates that remain competitive with KDE while maintaining a lower false alarm rate. On the other hand, the DKW-based conditional conformal prediction approach, which enforces the strictest false alarm rate control, exhibits the lowest fault detection rates. However, the differences remain relatively small, particularly when considering the low probability of fault occurrence compared to normal operation. This result suggests that while tighter control of false alarms may lead to a slight reduction in detection performance, the impact remains limited in practical scenarios where normal operation is overwhelmingly more frequent. 

#### **6. Conclusion** 

This study investigated the use of conformal prediction as a reliable and practical method for setting detection thresholds in PCA and AEbased fault detection systems in the context of production systems. The performance of this approach was systematically compared to traditional thresholding methods, with a focus on false alarm rate control and fault detection capability. The results highlight that the size of the training dataset significantly impacts the false alarm rate, with smaller datasets leading to higher-than-expected false alarm rates, regardless of the thresholding approach used. When the dataset was 

11 

_Journal of Process Control 152 (2025) 103495_ 

> _A.R. Diallo et al.                                                                                                                                                                                                                                Journal Process Control_ 

##### **Table 7** 

Fault detection rate (%) on the test dataset of the extended version. 

||Traditional||Marginal||DKW (δ=0.|2)|Asymptotic|(δ=0.2)|Simes (δ=0|.2)|
|---|---|---|---|---|---|---|---|---|---|---|
||SPE|T²|SPE|T²|SPE|T²|SPE|T²|SPE|T²|
|Fault 1|99.65|99.24|99.65|99.23|99.62|99.19|99.64|99.23|99.64|99.21|
|Fault 2|98.65|98.45|98.65|98.46|98.59|98.39|98.64|98.45|98.62|98.43|
|Fault 3|0.99|1.24|1.07|1.26|0.57|0.69|0.94|1.12|0.79|0.92|
|Fault 4|98.75|10.18|98.86|10.18|97.84|6.93|98.69|9.45|98.42|8.35|
|Fault 5|12.00|24.59|12.43|24.61|10.45|23.36|11.98|24.32|11.39|23.92|
|Fault 6|100.00|98.93|100.00|98.94|100.00|98.86|100.00|98.92|100.00|98.89|
|Fault 7|99.96|100.00|99.96|100.00|99.92|100.00|99.95|100.00|99.94|100.00|
|Fault 8|95.74|96.33|95.80|96.34|95.34|96.13|95.70|96.30|95.57|96.23|
|Fault 9|1.02|1.32|1.10|1.34|0.59|0.72|0.97|1.20|0.81|0.97|
|Fault 10|15.38|21.56|16.35|21.58|12.25|17.65|15.42|20.75|14.18|19.45|
|Fault 11|67.52|30.70|67.96|30.71|64.84|27.21|67.31|29.97|66.38|28.83|
|Fault 12|94.78|97.71|94.96|97.71|94.12|97.42|94.78|97.65|94.55|97.56|
|Fault 13|94.01|93.41|94.04|93.43|93.80|93.19|93.99|93.38|93.92|93.29|
|Fault 14|99.94|95.37|99.94|95.34|99.93|94.13|99.94|95.11|99.94|94.72|
|Fault 15|1.06|1.56|1.15|1.57|0.62|0.88|1.01|1.40|0.85|1.17|
|Fault 16|8.94|7.56|9.56|7.59|6.60|5.34|8.86|7.09|7.96|6.33|
|Fault 17|87.81|72.66|87.93|72.75|86.87|71.08|87.71|72.40|87.39|71.87|
|Fault 18|93.34|92.70|93.37|92.70|93.24|92.56|93.34|92.67|93.30|92.63|
|Fault 19|14.76|3.39|15.70|3.24|11.51|1.98|14.76|2.94|13.50|2.51|
|Fault 20|42.60|25.84|42.99|25.82|40.72|23.00|42.50|25.23|41.82|24.28|



##### **Table 8** 

FAR (%) of the AE model on the normal operating test data of the extended version. 

|Approach|**_α_** = **_1_**%|**_α_** =**_5_**%|
|---|---|---|
|KDE|1.18|5.64|
|Marginal|1.04|5.09|
|DKW (_δ_=0_._2)|0.57|4.62|
|Asymptotic (_δ_=0_._2)|0.96|4.81|
|Simes (_δ_= 0_._2)|0.78|3.71|



##### **Table 9** 

Fault detection rate (%) of the AE on the test set of the extended version. 

|Fault|KDE|Marginal|DKW|Asymptotic|Simes|
|---|---|---|---|---|---|
|Fault 1|99.67|99.64|99.61|99.64|99.63|
|Fault 2|98.73|98.68|98.63|98.67|98.65|
|Fault 3|1.31|1.14|0.64|1.05|0.86|
|Fault 4|99.57|99.74|99.42|99.71|99.62|
|Fault 5|25.11|24.23|22.57|23.96|23.39|
|Fault 6|100.00|100.00|100.00|100.00|100.00|
|Fault 7|100.00|100.00|100.00|100.00|100.00|
|Fault 8|97.19|97.12|96.97|97.10|97.05|
|Fault 9|1.38|1.22|0.68|1.12|0.92|
|Fault 10|33.58|31.3|25.77|30.42|28.56|
|Fault 11|68.88|66.99|63.48|66.46|65.32|
|Fault 12|98.43|98.35|98.16|98.33|98.27|
|Fault 13|94.57|94.53|94.36|94.5|94.45|
|Fault 14|99.94|99.94|99.93|99.94|99.93|
|Fault 15|1.54|1.38|0.77|1.26|1.05|
|Fault 16|16.95|15.43|11.28|14.75|13.31|
|Fault 17|89.23|88.79|87.68|88.62|88.26|
|Fault 18|93.57|93.53|93.41|93.51|93.47|
|Fault 19|9.68|8.84|5.77|8.30|7.22|
|Fault 20|47.00|46.08|43.50|45.66|44.78|



particularly limited, conditional conformal approaches could still be applied, but the resulting confidence bounds did not extend to very low false alarm rates (e.g., 0.05 and 0.01). This indicates that, given the small amount of calibration data available, there is no statistical guarantee of achieving low empirical false alarm rates. Consequently, these methods provide a valuable framework for quantifying the uncertainty associated with limited calibration data. 

When sufficient calibration data were available, it was observed that classical thresholding methods and the marginal conformal approach could lead to empirical false alarm rates exceeding the target risk levels. 

In contrast, conditional conformal approaches, particularly those based on Simes and DKW adjustments, systematically maintained false alarm rates below the predefined thresholds. The asymptotic approach, while more flexible, provided less strict control and, in some cases, slightly exceeded the target risk level when using the T² statistic. This demonstrates that conditional conformal methods offer a valuable alternative for more precise control over false alarms, provided an adequate amount of calibration data is available. 

Conformal prediction proved to be a competitive and distributionfree alternative to classical methods. Despite making fewer assumptions about the data distribution, it performed comparably as well as analytically derived traditional PCA-based thresholding methods and was also highly competitive with KDE, the most widely used approach for threshold setting in AE-based fault detection. Furthermore, the ability of conditional conformal methods to strictly limit false alarms is particularly beneficial in industrial settings, where fault occurrences are rare compared to normal operation. In such scenarios, minimizing false alarms is crucial to prevent unnecessary interventions, reduce operational costs, and maintain confidence in monitoring systems. These findings demonstrate that conformal prediction provides a practical and flexible framework for fault detection, with strong control over false alarm rates while maintaining competitive fault detection performance. 

Building on the promising results obtained in this study, one key direction for future work involves the deployment and assessment of conformal prediction methods on real industrial datasets. A first application has already been conducted in collaboration with an industrial partner, demonstrating the practical applicability of the proposed approach. However, further investigations across diverse operational contexts are needed to evaluate its robustness and effectiveness under realistic conditions, which often include variable process dynamics, heterogeneous sensors, and evolving fault signatures. 

Another promising avenue lies in the integration of operational cost considerations into the design and evaluation of detection systems. While this study has already emphasized the asymmetric nature of false alarms and missed detections, highlighting the need to limit false alarms in settings where faults are rare, future work could explore how conformal methods can be extended or adapted to better reflect these asymmetries. This could include optimizing threshold selection under cost-based criteria, thereby aligning detection performance with the economic and safety priorities of industrial operations. 

12 

> _A.R. Diallo et al.                                                                                                                                                                                                                                Journal of Process Control 152 (2025) 103495_ 

#### **CRediT authorship contribution statement** 

**Lazhar Homri:** Writing – review & editing, Validation, Supervision, Methodology, Formal analysis, Conceptualization. **Jean-Yves Dantan:** Writing – review & editing, Validation, Supervision, Resources, Methodology, Investigation, Funding acquisition, Formal analysis, Conceptualization. **Abdoul Rahime Diallo:** Writing – review & editing, Writing – original draft, Visualization, Validation, Methodology, Investigation, Formal analysis, Data curation, Conceptualization. 

#### **Declaration of Competing Interest** 

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper. 

#### **Acknowledgments** 

This paper has been supported by CaM´eX-IA, R´egion Grand Est, and Arcelor Mittal Global R&D, which is gratefully acknowledged by the authors. 

#### **Appendix A. Theoretical elements that explain the observed performance differences between the marginal and conditional conformal methods** 

In the following, the nonconformity scores are monotonically increasing, as is typical for detection indices such as the SPE and Hotelling’s T². In this setting: 

• The marginal conformal threshold is defined by reformulating Eq. (25) as: 


![](Reducing_false_alarms_in_fault_detection-_a_comparative_analysis_between_conformal_prediction_and_classical_methods_applied_to_PCA_and_autoencoders_images/conv_f4a22b1a51a40923.pdf-0013-10.png)


The factor ( _nc_ +1) _/nc_ ensures finite-sample validity and is standard in conformal prediction literature. • The conditional conformal threshold is defined by adapting Eq. (24) to the behavior of SPE and T² as: 


![](Reducing_false_alarms_in_fault_detection-_a_comparative_analysis_between_conformal_prediction_and_classical_methods_applied_to_PCA_and_autoencoders_images/conv_f4a22b1a51a40923.pdf-0013-12.png)


A key theoretical property of the adjustment functions _h_ is that they satisfy: 


![](Reducing_false_alarms_in_fault_detection-_a_comparative_analysis_between_conformal_prediction_and_classical_methods_applied_to_PCA_and_autoencoders_images/conv_f4a22b1a51a40923.pdf-0013-14.png)


which implies: 


![](Reducing_false_alarms_in_fault_detection-_a_comparative_analysis_between_conformal_prediction_and_classical_methods_applied_to_PCA_and_autoencoders_images/conv_f4a22b1a51a40923.pdf-0013-16.png)



![](Reducing_false_alarms_in_fault_detection-_a_comparative_analysis_between_conformal_prediction_and_classical_methods_applied_to_PCA_and_autoencoders_images/conv_f4a22b1a51a40923.pdf-0013-17.png)


Therefore: 


![](Reducing_false_alarms_in_fault_detection-_a_comparative_analysis_between_conformal_prediction_and_classical_methods_applied_to_PCA_and_autoencoders_images/conv_f4a22b1a51a40923.pdf-0013-19.png)



![](Reducing_false_alarms_in_fault_detection-_a_comparative_analysis_between_conformal_prediction_and_classical_methods_applied_to_PCA_and_autoencoders_images/conv_f4a22b1a51a40923.pdf-0013-20.png)


Although the marginal method includes a small correction factor _<u>ncn</u>_ <u>+</u> _c_ 1<sup>~~,~~this factor tends to 1 as</sup><sup>_nc_increases. In contrast, the adjustment introduced</sup> by _h_ is more substantial, especially for practical values of _δ_ in [0.05, 0.2]. For instance, the Figure below compares the correction of (1 − _α_ ) by marginal and DKW methods. 


![](Reducing_false_alarms_in_fault_detection-_a_comparative_analysis_between_conformal_prediction_and_classical_methods_applied_to_PCA_and_autoencoders_images/conv_f4a22b1a51a40923.pdf-0013-22.png)


**Fig. 8.** Comparison of marginal and DKW correction ( _nc_ = 100 _, α_ = 0 _._ 01) 

Consequently, under realistic conditions (moderate to large calibration sizes and typical values of δ), the inequality: 

_q_ ≤ _q_<sup>ʹ</sup> (A6) 

holds in practice, meaning that the conditional methods use higher detection thresholds and are more conservative than the marginal method. This directly explains the consistently lower false alarm rates observed in our experiments. 

13 

> _A.R. Diallo et al.                                                                                                                                                                                                                                Journal of Process Control 152 (2025) 103495_ 

#### **Data availability** 

Data will be made available on request. 

#### **References** 

- [1] G. Li, S.J. Qin, Comparative study on monitoring schemes for non-Gaussian distributed processes, J. Process Control 67 (Jul. 2018) 69–82, https://doi.org/ 10.1016/J.JPROCONT.2016.08.007. 

- [2] A. Gay, A. Voisin, B. Iung, P. Do, R. Bonidal, A. Khelassi, Data augmentation-based prognostics for predictive maintenance of industrial system, CIRP Ann. 71 (1) (Jan. 2022) 409–412, https://doi.org/10.1016/j.cirp.2022.04.005. 

- [3] C. Zhao, Perspectives on nonstationary process monitoring in the era of industrial artificial intelligence, J. Process Control 116 (Aug. 2022) 255–272, https://doi. org/10.1016/j.jprocont.2022.06.011. 

- [4] B. Krawczyk, Learning from imbalanced data: open challenges and future directions, Prog. Artif. Intell. 5 (4) (Nov. 2016) 221–232, https://doi.org/10.1007/ S13748-016-0094-0. 

- [5] Z. Chai, C. Zhao, B. Huang, Cross-domain knowledge transfer in industrial process monitoring: A survey, J. Process Control 149 (May 2025) 103408, https://doi.org/ 10.1016/j.jprocont.2025.103408. 

- [6] B. Zhang, J. Zhao, X. Chen, J. Yue, C. Zhao, Category-tree-guided hierarchical knowledge transfer framework for zero-shot fault diagnosis, J. Process Control 141 (Sep. 2024) 103267, https://doi.org/10.1016/j.jprocont.2024.103267. 

- [7] Q.-X. Zhu, Y.-S. Qian, N. Zhang, Y.-L. He, Y. Xu, Multi-scale Transformer-CNN domain adaptation network for complex processes fault diagnosis, J. Process Control 130 (Oct. 2023) 103069, https://doi.org/10.1016/j. jprocont.2023.103069. 

- [8] W.A. Shewhart, Econ. Control Qual. Manuf. Prod. (1931). 

- [9] J.E. Jackson, Quality Control Methods for Several Related Variables, Technometrics 1 (4) (Nov. 1959) 359–377, https://doi.org/10.1080/ 00401706.1959.10489868. 

- [10] M.A. Kramer, Nonlinear principal component analysis using autoassociative neural networks, AIChE J. 37 (2) (Feb. 1991) 233–243, https://doi.org/10.1002/ aic.690370209. 

- [11] B. Scholkopf, J.C. Platt, J. Shawe-Taylor, A.J. Smola, R.C. Williamson, Estimating ¨ the Support of a High-Dimensional Distribution, Neural Comput. 13 (7) (Jul. 2001) 1443–1471, https://doi.org/10.1162/089976601750264965. 

- [12] F.T. Liu, K.M. Ting, Z.-H. Zhou, Isolation Forest. 2008 Eighth IEEE International Conference on Data Mining, IEEE, Dec. 2008, pp. 413–422, https://doi.org/ 10.1109/ICDM.2008.17. 

- [13] K. Tidriri, N. Chatti, S. Verron, T. Tiplica, Bridging data-driven and model-based approaches for process fault diagnosis and health monitoring: A review of researches and future challenges, Annu Rev. Control 42 (2016) 63–81, https://doi. org/10.1016/j.arcontrol.2016.09.008. 

- [14] J. Qian, Z. Song, Y. Yao, Z. Zhu, X. Zhang, A review on autoencoder based representation learning for fault detection and diagnosis in industrial processes, Chemom. Intell. Lab. Syst. 231 (Dec. 2022) 104711, https://doi.org/10.1016/j. chemolab.2022.104711. 

- [15] Z. Yang, B. Xu, W. Luo, F. Chen, Autoencoder-based representation learning and its application in intelligent fault diagnosis: A review, Measurement 189 (Feb. 2022) 110460, https://doi.org/10.1016/j.measurement.2021.110460. 

- [16] K. Attouri, et al., Improved fault detection based on kernel PCA for monitoring industrial applications, J. Process Control 133 (Jan. 2024) 103143, https://doi. org/10.1016/j.jprocont.2023.103143. 

- [17] S. Yin, S.X. Ding, A. Haghani, H. Hao, P. Zhang, A comparison study of basic datadriven fault diagnosis and process monitoring methods on the benchmark Tennessee Eastman process, J. Process Control 22 (9) (Oct. 2012) 1567–1581, https://doi.org/10.1016/j.jprocont.2012.06.009. 

- [18] S. Joe Qin, Statistical process monitoring: basics and beyond, J. Chemom. 17 (8–9) (Aug. 2003) 480–502, https://doi.org/10.1002/cem.800. 

- [19] R. Laxhammar, trajectories in surveillance applications,“CONFORMAL ANOMALY DETECTION Detecting abnormal ”, Univ. Sk. ovde (2014)¨ . 

- [20] J.P. Shivers, L. Mackowiak, H. Anhalt, H. Zisser, Turn it Off!’: Diabetes Device Alarm Fatigue Considerations for the Present and the Future, J. Diabetes Sci. Technol. 7 (3) (May 2013) 789–794, https://doi.org/10.1177/ 193229681300700324. 

- [21] M. Cvach, Monitor alarm fatigue: an integrative review, Biomed. Instrum. Technol. 46 (4) (Jul. 2012) 268–277, https://doi.org/10.2345/0899-8205-46.4.268. 

- [22] J.P. Bliss, M.C. Dunn, Behavioural implications of alarm mistrust as a function of task workload, Ergonomics 43 (9) (Sep. 2000) 1283–1300, https://doi.org/ 10.1080/001401300421743. 

- [23] J.P. Bliss, R.D. Gilson, J.E. Deaton, Human probability matching behaviour in response to alarms of varying reliability, Ergonomics 38 (11) (Nov. 1995) 2300–2312, https://doi.org/10.1080/00140139508925269. 

- [24] S.J. Qin, Survey on data-driven industrial process monitoring and diagnosis, Annu Rev. Control 36 (2) (Dec. 2012) 220–234, https://doi.org/10.1016/j. arcontrol.2012.09.004. 

- [25] C.F. Alcala, S.J. Qin, Reconstruction-based contribution for process monitoring, Automatica 45 (7) (Jul. 2009) 1593–1600, https://doi.org/10.1016/j. automatica.2009.02.027. 

- [26] L.H. Chiang, E.L. Russell, R.D. Braatz, Fault detection and diagnosis in industrial systems, Springer Science & Business Media, 2000. 

- [27] C.A. Rieth, B.D. Amsel, R. Tran, M.B. Cook, Issues and Advances in Anomaly Detection Evaluation for Joint Human-Automated Systems, in: Advances in Intelligent Systems and Computing, 595, Springer Verlag, 2018, pp. 52–63, https://doi.org/10.1007/978-3-319-60384-1_6. 

- [28] J. Yu, Y. Zhang, Challenges and opportunities of deep learning-based process fault detection and diagnosis: a review, Neural Comput. Appl. 35 (1) (Jan. 2023) 211–252, https://doi.org/10.1007/s00521-022-08017-3. 

- [29] V. Vovk, A. Gammerman, G. Shafer, Algorithmic Learning in a Random World, Springer, 2005. Vol. 29. 

- [30] S. Bates, E. Cand`es, L. Lei, Y. Romano, M. Sesia, Testing for outliers with conformal p-values, Ann. Stat. 51 (1) (Feb. 2023), https://doi.org/10.1214/22-AOS2244. 

- [31] J. Smith, “The efficiency of conformal predictors for anomaly detection,”, Univ. Lond. (2016). 

- [32] S. Farouq, S. Byttner, M.R. Bouguelia, H. Gadd, Mondrian conformal anomaly detection for fault sequence identification in heterogeneous fleets, Neurocomputing 462 (Oct. 2021) 591–606, https://doi.org/10.1016/J. NEUCOM.2021.08.016. 

- [33] S. Farouq, S. Byttner, M.R. Bouguelia, H. Gadd, A conformal anomaly detection based industrial fleet monitoring framework: A case study in district heating, Expert Syst. Appl. 201 (Sep. 2022), https://doi.org/10.1016/j.eswa.2022.116864. 

- [34] F. Cai, X. Koutsoukos, Real-time out-of-distribution detection in learning-enabled cyber-physical systems. 2020 ACM/IEEE 11th International Conference on CyberPhysical Systems (ICCPS, IEEE, Apr. 2020, pp. 174–183, https://doi.org/10.1109/ ICCPS48487.2020.00024. 

- [35] O. Kundacina, V. Vincan, G. Gojic, V. Ninkovic, D. Miskovic, Conformal anomaly detection for predictive maintenance in thermal power plants, IEEE Access 13 (2025) 39738–39752, https://doi.org/10.1109/ACCESS.2025.3546451. 

- [36] V. Chandola, A. Banerjee, V. Kumar, Anomaly detection, ACM Comput. Surv. 41 (3) (Jul. 2009) 1–58, https://doi.org/10.1145/1541880.1541882. 

- [37] J.E. Jackson, G.S. Mudholkar, Control Procedures for Residuals Associated with Principal Component Analysis, Technometrics 21 (3) (Aug. 1979) 341, https://doi. org/10.2307/1267757. 

- [38] N.D. Tracy, J.C. Young, R.L. Mason, Multivariate control charts for individual observations, J. Qual. Technol. 24 (2) (Apr. 1992) 88–95, https://doi.org/ 10.1080/00224065.1992.12015232. 

- [39] A.N. Angelopoulos and S. Bates, “A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification,” Jul. 2021, Accessed: Jan. 09, 2024. [Online]. Available: 〈http://arxiv.org/abs/2107.07511〉. 

- [40] V. Vovk, Conditional validity of inductive conformal predictors, Mach. Learn 92 (2–3) (Sep. 2012) 349–376, https://doi.org/10.1007/s10994-013-5355-6. 

- [41] A. Dvoretzky, J. Kiefer, J. Wolfowitz, Asymptotic minimax character of the sample distribution function and of the classical, Ann. Math. Stat. 27 (3) (1956) 642–669. 

   - 〈https://www.jstor.org/stable/2237374〉. Accessed: Feb. 24, 2025. [Online]. Available. 

- [42] P. Massart, The Tight Constant in the Dvoretzky-Kiefer-Wolfowitz Inequality, Ann. Probab. 18 (3) (1990) 1269–1283. 〈https://www.jstor.org/stable/2244426〉. Accessed: Feb. 24, 2025. [Online]. Available. 

- [43] S.K. Sarkar, Generalizing Simes’ test and Hochberg’s stepup procedure, Ann. Stat. 36 (1) (Feb. 2008) 337–363, https://doi.org/10.1214/009053607000000550. 

- [44] J.J. Downs, E.F. Vogel, A plant-wide industrial process control problem, Comput. Chem. Eng. 17 (3) (Mar. 1993) 245–255, https://doi.org/10.1016/0098-1354(93) 80018-I. 

- [45] C.A. Rieth, B.D. Amsel, R. Tran, M.B. Cook, Additional Tennessee Eastman Process Simulation Data for Anomaly Detection Evaluation, Harv. Dataverse (2017) doi: doi/10.7910/DVN/6C3JR1. 

- [46] R. Tan, J.R. Ottewill, N.F. Thornhill, Monitoring statistics and tuning of Kernel principal component analysis with radial basis function Kernels, IEEE Access 8 (2020) 198328–198342, https://doi.org/10.1109/ACCESS.2020.3034550. 

- [47] Y. Zhao, Z. Nasrullah, Z. Li, PyOD: a python toolbox for scalable outlier detection, J. Mach. Learn. Res. 20 (2019) 1–7. 〈https://pyod.readthedocs.io〉. Accessed: Mar. 25, 2025. [Online]. Available. 

- [48] S. Seabold, J. Perktold, Statsmodels: econometric and statistical modeling with python, Proc. 9th PYTHON Sci. CONF (2010). 〈http://statsmodels.sourceforge. net/〉. Accessed: Mar. 25, 2025. [Online]. Available. 

14 

