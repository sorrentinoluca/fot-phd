
![](CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems_images/CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems.pdf-0001-00.png)



![](CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems_images/CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems.pdf-0001-01.png)


# **CODiT: Conformal Out-of-Distribution Detection in Time-Series Data for Cyber-Physical Systems** 

## Kaustubh Sridhar 

Sangon Park sangdon@gatech.edu Georgia Institute of Technology Atlanta, Georgia, USA 

Ramneet Kaur 

ramneetk@seas.upenn.edu University of Pennsylvania Philadelphia, Pennsylvania, USA 

ksridhar@seas.upenn.edu University of Pennsylvania Philadelphia, Pennsylvania, USA 

Yahan Yang yangy96@seas.upenn.edu University of Pennsylvania Philadelphia, Pennsylvania, USA 

## Susmit Jha 

Anirban Roy anirban.roy@sri.com SRI International Menlo Park, California, USA 

susmit.jha@sri.com SRI International Menlo Park, California, USA 

Oleg Sokolsky sokolsky@seas.upenn.edu University of Pennsylvania Philadelphia, Pennsylvania, USA 

Insup Lee 

lee@seas.upenn.edu University of Pennsylvania Philadelphia, Pennsylvania, USA 

### **KEYWORDS** 

### **ABSTRACT** 

Uncertainty in the predictions of learning enabled components hinders their deployment in safety-critical cyber-physical systems (CPS). A shift from the training distribution of a learning enabled component (LEC) is one source of uncertainty in the LEC’s predictions. Detection of this shift or out-of-distribution (OOD) detection on individual datapoints has therefore gained attention recently. But in many applications, inputs to CPS form a temporal sequence. Existing techniques for OOD detection in time-series data for CPS either do not exploit temporal relationships in the sequence or do not provide any guarantees on detection. We propose using deviation from the in-distribution temporal equivariance as the non-conformity measure in conformal anomaly detection framework for OOD detection in time-series data for CPS. Computing independent predictions from multiple conformal detectors based on the proposed measure and combining these predictions by Fisher’s method leads to the proposed detector CODiT with bounded false alarms. We illustrate the efficacy of CODiT by achieving state-of-the-art results in autonomous driving systems with perception (or vision) LEC. We also perform experiments on medical CPS for GAIT analysis where physiological (nonvision) data is collected with force-sensitive resistors attached to the subject’s body. Code, data, and trained models are available at _https://github.com/kaustubhsridhar/time-series-OOD_ 

Learning Enabled Components, Uncertainty, Cyber-Physical Systems, Time-Series, Out-of-Distribution, Conformal Detection 

##### **ACM Reference Format:** 

Ramneet Kaur, Kaustubh Sridhar, Sangon Park, Yahan Yang, Susmit Jha, Anirban Roy, Oleg Sokolsky, and Insup Lee. 2023. CODiT: Conformal Outof-Distribution Detection in Time-Series Data for Cyber-Physical Systems. In _ACM/IEEE 14th International Conference on Cyber-Physical Systems (with CPS-IoT Week 2022) (ICCPS ’23), May 9–12, 2023, San Antonio, TX, USA._ ACM, New York, NY, USA, 12 pages. https://doi.org/10.1145/3576841.3585931 

### **1 INTRODUCTION** 

With remarkable performance-levels of machine learning across different domains [13, 24], there is much interest in using these learning-enabled components (LEC) in cyber-physical systems (CPS). A prime example of this trend is autonomous driving, where a car would be equipped with the capability to autonomously perform certain operations, such as adaptive cruise control, emergency braking or lane following [4]. These autonomous features aim to enhance the safety of the vehicle and its occupants. But as drivers rely on them more and more, a malfunction in such a feature would be detrimental to safety. The black-box nature of LEC makes it difficult to interpret their uncertain predictions on perturbed inputs [18] or even inputs from novel environments from training [36]. For instance, Yang et al. (2022) show that an ego vehicle that uses a perception LEC to estimate following distance to a car in front of it crashes when the car is replaced by a bike. This is because the LEC was trained with cars in front of the ego vehicle and could not correctly estimate distance from bikes (novel object from training). Deployment of LEC in safety-critical CPS such as autonomous driving [4], and healthcare [8], therefore, requires detection of shift in the distribution of the LEC’s inputs from its training distribution. 

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for components of this work owned by others than the author(s) must be honored. Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. Request permissions from permissions@acm.org. _ICCPS ’23, May 9–12, 2023, San Antonio, TX, USA_ 

Detection of shift from the training distribution of LEC or out-ofdistribution (OOD) detection on individual datapoints has received broad attention [16, 20, 31]. But this problem of OOD detection in time-series data for CPS is less explored. In time-series data, 

> © 2023 Copyright held by the owner/author(s). Publication rights licensed to ACM. ACM ISBN 979-8-4007-0036-1/23/05...$15.00 https://doi.org/10.1145/3576841.3585931 

120 

ICCPS ’23, May 9–12, 2023, San Antonio, TX, USA 

Kaur et al. 

**Table 1: Capabilities of detectors in time-series data for CPS.** 

|OOD|False Alarm Rate|Temporal|Non-vision|
|---|---|---|---|
|Detector|Guarantees|OODs|Data|
|VAE [5]|✓|**?**|✓|
|_𝛽_-VAE[27]|✓|**?**|✓|
|Memory [36]|✗|**?**|✓|
|Feng et al.’s [10]|✗|✓|✗|
|CODiT(Ours)|✓|✓|✓|



OOD detection aims at detecting those windows of time-series datapoints that are outside the training distribution of LEC. In this case, the distribution of interest is not just of individual datapoints, but the distribution of sequences in which these datapoints occur in the time-series data. In this paper, we propose CODiT, a novel algorithm for OOD detection in time-series data for CPS with a bounded false alarm rate. 

Most of the existing approaches for OOD detection in time-series data for CPS are _point-based_ , i.e., they independently consider each datapoint in the window, such as individual frames in a video clip. In other words, these approaches do not exploit time-dependency among the datapoints in a window to detect if the window is OOD. An example of an OOD window in a driving scenario is a car drifting video clip due to slippery ground or loss of control, given normal driving video clips as in-distribution (iD) data. As shown in Fig. 1, we cannot tell from a single frame if the car has drifted since drift is defined based on the relative relation between frames (e.g., a trajectory of a car). We define these OOD windows as _temporal OODs_ , which require considering the sequence of datapoints in the window for detection. In contrast to the existing point-based approaches for detection in time-series data for CPS, we propose using time-dependency among the datapoints in a window for detection of temporal OODs. 

Specifically, we propose _using deviation from the iD temporal equivariance_ , i.e. equivariance with respect to a set of temporal transformations learned by a model on windows drawn from the training distribution of LEC, _for OOD detection in time-series data_ . This is because a model trained to learn equivariance with respect to temporal transformations on data drawn from the training distribution might not generalize or exhibit equivariance on OOD inputs dissimilar to the training distribution. 

To bound false alarms on the iD data, we leverage inductive conformal anomaly detection (ICAD) [1]. ICAD is a general framework for testing if an input conforms to the training distribution by computing quantitative scores defined by a non-conformity measure. A _𝑝_ -value, computed by comparing non-conformity score of the input with these scores on the data drawn from training distribution, indicates anomalous behavior of the input. The detection performance of ICAD, however, depends on the choice of the non-conformity measure used in the framework [1]. We propose using _deviation from the expected temporal equivariant behavior of a model learned on data drawn from training distribution of LEC_ as the non-conformity measure in ICAD for OOD detection in the time-series data for CPS. 

ICAD computes a single _𝑝_ -value of the input to detect its anomalous behavior. To enhance detection performance, we propose using multiple ( _𝑛 >_ 1) _𝑝_ -values computed from _𝑛_ transformations sampled as independent and identically distributed (IID) variables from 

a distribution over the set of temporal transformations. The intuition for using multiple transformations is that an OOD window might behave as a transformed iD window with one transformation but the likelihood of this decreases with the number of temporal transformations. Using Fisher’s method [33] to combine these _𝑛_ independent _𝑝_ -values leads to the proposed detector CODiT for conformal OOD detection in time-series data for CPS with a bounded false alarm rate. The contributions can be summarized as: 

- (1) **Novel Measure for OOD Detection in Time-Series Data for CPS.** To our knowledge, all the existing non-conformity measures for OOD detection are defined on individual datapoints. We propose a measure that is defined on the window containing information about the sequence of time-series datapoints for enhancing detection of the temporal OODs. With a model trained to learn iD temporal equivariance via the auxiliary task of predicting an applied transformation on windows drawn from training distribution of LEC, we propose using error in this prediction as the non-conformity measure in ICAD for detection in time-series data for CPS. 

- (2) **Enhanced detection performance.** To enhance the detection performance, we propose to use Fisher’s method as an ensemble approach for combining predictions from multiple conformal detectors based on the proposed measure. 

- (3) **CODiT.** Computing _𝑛_ independent _𝑝_ -values of the input from the proposed measure in the ICAD framework, and combining these values by Fisher’s method leads to the proposed detector CODiT with a bounded false alarm rate for OOD detection in time-series data for CPS. 

- (4) **Evaluation.** For comparison with the point-based detectors, we perform experiments on weather and night OODs in an autonomous driving system with perception LEC, achieving state-of-the-art (SOTA) results. We outperform the existing non-point based SOTA [10] on temporal OODs in driving scenario. To illustrate that CODiT can be used for OOD detection beyond vision, we also perform experiments on medical CPS for GAIT analysis where physiological (non-vision) data is collected with force-sensitive resistors attached to the subject’s body [15]. 

### **2 PROBLEM STATEMENT AND MOTIVATION 2.1 Problem Statement** 

OOD detection in time-series data for CPS takes in a window _𝑋𝑡,𝑤_ of consecutive time-series datapoints ( _𝑥𝑡 ,𝑥𝑡_ +1 _, . . . ,𝑥𝑡_ + _𝑤_ −1) to the LEC in the system, and labels _𝑋𝑡,𝑤_ as iD or OOD. Here _𝑡_ is the starting time of the window and _𝑤_ is the window length. 

### **2.2 Motivation of the Proposed OOD Detection Measure** 

The existing point-based detectors for OOD detection in time-series data might not be able to detect temporal OODs to the system. An example of a temporal OOD in driving scenario, as shown in Fig. 2, is the replay window where camera gets stuck at a single frame and starts generating the same image over and over again. We need to consider the sequence of same image in a replay window to detect the window as OOD. Detection results on replay dataset in Fig. 3 

121 

ICCPS ’23, May 9–12, 2023, San Antonio, TX, USA 

CODiT: Conformal OOD Detection in Time-Series Data for CPS 


![](CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems_images/CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems.pdf-0003-02.png)


**Figure 1: Drift in cars as temporal OODs in driving scenario. This trace is taken from the drift dataset by Noor et al. [25].** 

shows that all the existing point-based detectors, namely variational autoencoder (VAE) based Cai et al.’s [5], _𝛽_ VAE-based Ramakrishna et al.’s [27], and memory-based Yang et al’s [36] detectors perform poorly in the detection of these temporal OODs. We, therefore, propose using time-dependency among the datapoints in a window for OOD detection in time-series data for CPS. 

To our knowledge, Feng et al.’s detector [10] is the only existing OOD detector that takes into account time-dependency among the individual datapoints in a window. It does so by extracting optical flow information from consecutive frames in a video clip. As shown in Fig. 8 of Section 6, Feng et al.’s detector can thus be used to detect temporal OODs. However, since this detector depends on the optical flow information, it is restricted to vision data. In contrast, CODiT can be used to detect temporal OODs across domains (vision or nonvision) without relying on any domain-specific features. Table 1 compares the detection capabilities of CODiT with the existing OOD detectors in time-series data. 


![](CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems_images/CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems.pdf-0003-06.png)


**Figure 2: Replay window: An example of the temporal OOD where camera gets stuck and generates the same image in the entire window. This trace is generated by CARLA, an opensource simulator for autonomous driving research [9].** 


![](CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems_images/CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems.pdf-0003-08.png)


**Figure 3: ROC curves (left), TNR (with detection threshold at 95% TPR on right) results on replay OODs by the existing point-based OOD detectors in time-series data for CPS. These approaches perform poorly in the detection of these temporal OODs. We call iD as positive and OOD as negative.** 

### **3 RELATED WORK** 

OOD detection in non time-series datasets such as German Traffic Sign Recognition (GTSRB) [30] has been extensively studied. Details about these detectors on non time-series (or individual) datapoints are included in Appendix. OOD detection in CPS with 

low-dimensional input space through envelopes has also been studied in the past [32]. 

Recently, there has been interest in leveraging ICAD for OOD detection with guarantees on false alarm rate on high dimensional input space [5, 14, 19, 27]. While iDECODe [19], and Haroush et al.’s [14] are OOD detectors for individual datapoints, Cai et al.’s [5], and Ramakrishna et al.’s [27] are detectors for time-series data. iDECODe uses error in the equivariance learned by a model with respect to a transformation set on individual datapoints as the non-conformity measure (NCM) in ICAD for detection in non timeseries data. Haroush et al. propose using a combined _𝑝_ -value from different channels and layers of convolutional neural networks (CNN) for detection. It is not clear how to directly apply individual point detectors to time-series data with the ICAD guarantees due to the following two reasons. First, even if we apply these detectors to individual datapoints in the time-series window independently, we do not know how to combine detection verdicts on these datapoints for detection on the window. Second, for detection guarantees by ICAD, it is required that all non-conformity scores for _𝑝_ -value computation to be IID [22]. Since these detectors are not solving OOD detection problem in time-series data it is not clear how to apply them to time-series while preserving the IID assumption on the time-series data. Also, iDECODe uses a single _𝑝_ -value for detection and we propose using multiple ( _𝑛 >_ 1) independent _𝑝_ - values to be combined by the Fisher’s method for preserving the detection guarantees. In contrast to [14], our approach is not limited to CNN and can be used for other predictive models as well. 

Cai et al. [5] propose using reconstruction error by VAE on an input image as the NCM in the ICAD framework. Martingale formula [35] is used to combine multiple _𝑝_ -values computed on multiple samples of the input in the latent space of VAE. The detection score on a time-series window is then computed by applying cumulative sum procedure [2] on the martingale values of all images in the window. Ramakrishna et al. [27] propose using KL-divergence between the disentangled feature space of _𝛽_ -VAE on an input image and the normal distribution, as the NCM in ICAD. They also use the martingale formula to combine _𝑝_ -values of all the images in the window for detection. Recently, Yang et al. [36] propose computing few prototypes (or memories) from the training data and using distance of an input image with these prototypes for detection on the input. The time-series window to the CPS is labeled as OOD if majority datapoints in the window are detected as OOD. Unlike the other two detectors [5, 27], this approach does not provide false alarm rate guarantees on detection. All of these three OOD detectors [5, 27, 36] on time-series data are point-based, and as shown by the experiments on replay OODs, these might perform poorly in the detection of temporal OODs. CODiT computes the _𝑝_ -value of the window (and not individual datapoints in the window) in the ICAD framework. It is, therefore, a non-point based approach that can be used to detect temporal OODs (Section 6.2, 6.3). 

122 

ICCPS ’23, May 9–12, 2023, San Antonio, TX, USA 

Kaur et al. 

To our knowledge, the only non-point based approach for OOD detection in time-series data is by Feng et al. [10]. They propose extracting optical flow information from a time-series window and training a VAE on this information. KL-divergence between the trained VAE and a specified prior is used as the OOD score. This detector uses optical flow to extract time-dependency in the frames of a window and thus can be used to detect temporal OODs. However, this approach does not provide any guarantees on detection and will not work on non-vision datasets as it relies on optical flows. As shown in the experiments on the GAIT dataset in medical CPS, CODiT can be used for OOD detection in non-vision domain. 

### **4 BACKGROUND AND NOTATIONS** 

CODiT uses error in the temporal equivariance learned by a model on windows drawn from the training distribution of LEC as the non-conformity measure in the inductive conformal anomaly detection (ICAD) framework. With multiple _𝑝_ -values obtained from the proposed measure in ICAD, the final OOD detection score is computed by combining these values by Fisher’s method. Here we provide the background on equivariance, ICAD, and Fisher’s method required for technical details of the proposed OOD detector, CODiT. We also define the notations used in the rest of the paper. 

### **4.1 Equivariance** 

A function _𝑓_ is equivariant with respect to a transformation _𝑔_ if we know how the output of _𝑓_ changes if we transform its input from _𝑥_ to _𝑔_ ( _𝑥_ ). Invariance is a special case of equivariance where the output of _𝑓_ does not change by the transformation _𝑔_ on its input. Invariance with respect to geometric transformations such as rotation, tilt, scale, etc. is a desired property of the machine learning classifiers. For example, classification results on the straight images of planes should not change with a tilt in these images. 

Definition 1 (Schmidt and Roth, 2012). _For a set 𝑋 , a function 𝑓 is defined to be equivariant with respect to a set of transformations 𝐺, if there exists the following relationship between any transformation 𝑔_ ∈ _𝐺 of the function’s input and the corresponding transformation 𝑔_<sup>′</sup> _of the function’s output:_ 


![](CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems_images/CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems.pdf-0004-08.png)


Invariance is a special case of equivariance where _𝑔_<sup>′</sup> is the identity function, i.e., the output of _𝑓_ remains unchanged by the transformation _𝑔_ on its input. 

_4.1.1 Learning Equivariance: Autoencoding Variational Transformations (AVT)._ Augmenting training data with transformations from the set _𝐺_ of geometric transformations is a common approach to learning invariance with respect to _𝐺_ [6, 7]. The auxiliary task of predicting an applied transformation from _𝐺_ on the training data also encourages the model to learn equivariance with respect to _𝐺_ [26]. Qi et al.’s 2019 “Autoencoding Variational Transformations” (AVT) framework trains a VAE to learn a latent space that is equivariant to transformations. For the set _𝑋_ of training images and the set _𝐺_ of geometric transformations, a VAE is trained to predict the applied transformation from _𝐺_ on an input _𝑥_ ∈ _𝑋_ . Equivariance between the latent space of VAE and _𝐺_ is learned by maximizing mutual information between the latent space and _𝐺_ . 

Definition 2 (Jenni and Jin, 2021). _Temporal equivariance of a function 𝑓 from equation 1 is defined on a set 𝑋 of windows of consecutive time-series datapoints and with respect to a set 𝐺 of temporal transformations._ 

Some examples of temporal transformations on video clips are skipping every second frame in the clip (2x speed), shuffling frames in the clip (shuffle), reversing the order of frames in the clip (reverse), and reversing the order of the second half frames in the clip (periodic). In the rest of the paper, we will use the notation _𝐺𝑇_ to represent a set of temporal transformations and call the function _𝑓_ from Def. 2 as _𝐺𝑇_ -equivariant if it learns equivariance w.r.t _𝐺𝑇_ on windows drawn from the training distribution of LEC. We refer to the deviation from the expected result of this function _𝑓_ on a transformed input (transformed with a _𝑔_ ∈ _𝐺𝑇_ ) as deviation from the iD _𝐺𝑇_ -equivariance. 

### **4.2 Inductive Conformal Anomaly detection** 

Inductive Conformal Anomaly Detection (ICAD) [22] is a general framework for testing if an input conforms to the training distribution. It is based on a non-conformity measure (NCM), which is a real-valued function that assigns a non-conformity score _𝛼_ to the input. This score indicates non-conformance of the input with data drawn from the training distribution. The higher the score is, the more non-conforming or anomalous the input is with respect to training data. An example of the non-conformity score is the reconstruction error by a VAE trained on data drawn from the training distribution. 

The training dataset _𝑋_ of size _𝑙_ is split into a _proper training set 𝑋_ tr = { _𝑥 𝑗_ : _𝑗_ = 1 _, . . . ,𝑚_ } and a _calibration set 𝑋_ cal = { _𝑥 𝑗_ : _𝑗_ = _𝑚_ + 1 _, . . . ,𝑙_ }. Proper training set _𝑋_ tr is used in defining NCM. In the example of reconstruction error by a VAE as the non-conformity score, the VAE trained on _𝑋𝑡𝑟_ is used for computing the error. Calibration set _𝑋_ cal is a held-out training set that is used for computing _𝑝_ -value of an input. _𝑝_ -value of an input _𝑥_ is computed by comparing its non-conformity score _𝛼_ ( _𝑥_ ) with these scores on the calibration datapoints: 


![](CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems_images/CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems.pdf-0004-16.png)


If _𝑥_ is drawn from the training distribution, then its non-conformity score is expected to lie within the range of scores for the calibration datapoints and thus higher _𝑝_ -values for the iD datapoints. With _𝜖_ ∈(0 _,_ 1) as the anomaly detection threshold, _𝑥_ is therefore detected as an anomalous input if the _𝑝_ -value of _𝑥_ is less than _𝜖_ . 

_4.2.1 False Alarm Rate Guarantees._ The false anomalous detection on an input drawn from the training distribution is upper bounded by the specified detection threshold _𝜖_ in ICAD. 

Lemma 1 (Balasubramanian et al., 2014). _If an input 𝑥 and the calibration datapoints 𝑥𝑚_ +1 _, . . . ,𝑥𝑙 are independent and identically distributed (IID), then for any choice of the NCM defined on the proper training set 𝑋tr, the 𝑝-value(𝑥) in_ (2) _is uniformly distributed. Moreover, we have 𝑃𝑟_ ( _𝑝-value_ ( _𝑥_ ) _< 𝜖_ ) ≤ _𝜖, where the probability is taken over 𝑥𝑚_ +1 _, . . . ,𝑥𝑙 , and 𝑥._ 

From Lemma 1, we know that if _𝑥_ and the datapoints in the calibration set _𝑋_ cal are IID, then the _𝑝_ -value( _𝑥_ ) from (2) is uniformly 

123 

ICCPS ’23, May 9–12, 2023, San Antonio, TX, USA 

CODiT: Conformal OOD Detection in Time-Series Data for CPS 

distributed over {1/( _𝑙_ − _𝑚_ +1) _,_ 2/( _𝑙_ − _𝑚_ +1) _, . . . ,_ 1}. The probability of _𝑝_ -value( _𝑥_ ) less than _𝜖_ or misclassifying _𝑥_ as anomalous is, therefore, �1≤ _𝑖_ ≤( _𝑙_ − _𝑚_ +1) _𝜖_<sup>1/(</sup><sup>_𝑙_−</sup><sup>_𝑚_+ 1)=⌊(</sup><sup>_𝑙_−</sup><sup>_𝑚_+ 1)</sup><sup>_𝜖_⌋/(</sup><sup>_𝑙_−</sup><sup>_𝑚_+ 1)≤</sup><sup>_𝜖._</sup> 

### **4.3 Fisher’s Method** 

The same hypothesis can be tested by multiple conformal predictors and an ensemble approach for combining these predictions can be used to improve upon the performance of individual predictors. Fisher’s method is one of these approaches for combining multiple conformal predictions or _𝑝_ -values of an input from (2). Fisher value of an input _𝑥_ from _𝑛𝑝_ -values is computed as follows: 


![](CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems_images/CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems.pdf-0005-05.png)


Lemma 2 (Toccaceli and Gammerman, 2017). _If 𝑛𝑝-values, 𝑝_ 1 _, . . . , 𝑝𝑛, are independently drawn from a uniform distribution of these values, then_ −2<sup>�</sup><sup>_𝑛_</sup> _𝑖_ =1<sup>log</sup><sup>_𝑝𝑖followsachi-squaredistribution_</sup> _with_ 2 _𝑛 degrees of freedom. Thus, the combined p-value is_ 


![](CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems_images/CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems.pdf-0005-07.png)


_where 𝑟_ =<sup>�</sup><sup>_𝑛_</sup> _𝑘_ =1<sup>_𝑝𝑘,𝑦is a random variable following a chi-square dis-_</sup> _tribution with_ 2 _𝑛 degrees of freedom, and the probability is taken over 𝑦. Moreover, the combined p-value follows the uniform distribution._ 

### **5 TEMPORAL EQUIVARIANCE FOR CONFORMAL OOD DETECTION IN TIME-SERIES DATA FOR CPS** 

Here, we first classify OOD windows in time-series data into two types, and then provide details of the proposed detector CODiT. 

### **5.1 OOD Data Types in Time-Series** 

We classify OOD windows in time-series data into two types: _temporal_ OODs and _non-temporal_ OODs. 

A crucial property of the temporal OODs compared to the nontemporal OODs is that it is hard to detect temporal OODs by looking at individual datapoints within the window without considering time-dependency between these datapoints. Examples of temporal OODs in driving scenario are car drifting video clips (Fig. 1), and replay OODs (Fig. 2). An example of the temporal OOD in medical CPS is the GAIT (or waking pattern) of patients with neurodegenerative diseases. With the GAIT of healthy individuals as iD data, the GAIT of patients with neurodegenerative diseases, such as Parkinson’s disease (PD), Huntington’s disease (HD), and Amyotrophic Lateral Sclerosis (ALS), are examples of temporal OODs. Fig. 9 (in Appendix) shows dynamics of the stride time (one of the walking pattern features) of a healthy control person and patients with PD, HD, and ALS disease. As shown in the Figure, we need a sequence of time-series datapoints to determine whether the walking pattern is from a healthy individual or a patient. In contrast to the temporal OODs, the non-temporal OODs can be detected by looking at individual datapoints. Examples of non-temporal OODs include driving video clips under rainy, foggy, or snowy weather, given the driving video clips under clear sunny weather as iD data. We can detect weather OODs by looking at images in the window independently. 

Based on these observations, we call a window _𝑋𝑡,𝑤_ as a temporal OOD if _𝑋𝑡,𝑤_ is drawn from OOD but confused to be drawn from iD by removing the time-dependency of individual datapoints within _𝑋𝑡,𝑤_ (e.g., randomly shuffling the order of video clip frames). As shown in the experimental section 6, CODiT can be used to detect both temporal and non-temporal OODs in time-series data for CPS. 

### **5.2 CODiT** 

CODiT uses an OOD detection score based on multiple _𝑝_ -values from ICAD. Here, we first define the proposed NCM to be used in the ICAD framework for computing a _𝑝_ -value along with the final detection score, and then formalize CODiT’s algorithm with a bounded false alarm rate. 

_5.2.1 Proposed NCM and OOD Detection Score._ 

**TTPE NCM.** We propose to use time-dependency between datapoints in a time-series window for detection on the window. Unlike all the existing NCMs defined on individual datapoints, we propose an NCM that is defined on the window containing information about the sequence of datapoints in the window. Specifically, we propose using deviation from the expected iD _𝐺𝑇_ -equivariance learned by a model on windows drawn from the training distribution of LEC as an NCM in ICAD for OOD detection in time-series data for CPS. Learning _𝐺𝑇_ -equivariance via an auxiliary task of predicting the applied temporal transformation (such as shuffle, reverse, etc.) on a window requires learning changes in the original sequence of the datapoints in a predictable way. For a VAE model _𝑀_ trained to learn _𝐺𝑇_ -equivariance on windows of proper training data in the AVT framework, we propose to use error in the prediction of the applied temporal transformation _𝑔_ ∈ _𝐺𝑇_ on an input window _𝑋𝑡,𝑤_ as the NCM: 

PredictionError( _𝑔, 𝑀_ ( _𝑔_ ( _𝑋𝑡,𝑤_ ))) _._ 

We call the proposed NCM as the **Temporal Transformation Prediction Error (TTPE)** NCM. 

The existing AVT framework [26] is defined to learn equivariance with respect to geometric transformations on images. We extend it to learn _𝐺𝑇_ -equivariance by: 

- (1) Modifying VAE’s architecture to accept windows of consecutive time-series datapoints as inputs. The time-series can be on vision (e.g. drift car video clip) or non-vision (e.g., GAIT) datapoints. 

- (2) Modifying the auxiliary task to predict the applied temporal transformation from a set _𝐺𝑇_ on windows of time-series datapoints. 

**Motivation for TTPE-NCM.** _𝐺𝑇_ -equivariance learned by a model on windows drawn from the training distribution of LEC is more likely to work on iD data and is not guaranteed to generalize to OOD data dissimilar to that used for training. With the set _𝐺𝑇_ = {2x _𝑠𝑝𝑒𝑒𝑑,𝑠ℎ𝑢𝑓𝑓𝑙𝑒,𝑟𝑒𝑣𝑒𝑟𝑠𝑒, 𝑝𝑒𝑟𝑖𝑜𝑑𝑖𝑐,𝑖𝑑𝑒𝑛𝑡𝑖𝑡𝑦_ }, we train a VAE model on the proper training data of the drift dataset to predict an applied transformation _𝑔_ sampled independently from a uniform distribution over _𝐺𝑇_ . With _𝐺𝑇_ as the set of five classes of temporal transformations, we use CrossEntropyLoss( _𝑔, 𝑀_ ( _𝑔_ ( _𝑋𝑡,𝑤_ ))) as the TTPE-NCM. Fig. 4 shows that the model has much higher prediction errors on the OOD windows than on the test iD windows on all the five ground truth transformations in _𝐺𝑇_ . This supports our 

124 

ICCPS ’23, May 9–12, 2023, San Antonio, TX, USA 

Kaur et al. 

hypothesis that _𝐺𝑇_ -equivariance learned on data drawn the training distribution is not likely to generalize on data drawn from OOD, and therefore higher prediction errors on OOD windows than on the iD windows. 

**OOD Detection Score.** Instead of using a single _𝑝_ -value from the TTPE-NCM in ICAD, we propose using multiple ( _𝑛 >_ 1) _𝑝_ -values to enhance detection. We require _𝑛_ non-conformity scores for both the input and the calibration datapoints for computing _𝑛𝑝_ -values. These scores are computed from _𝑛_ transformations sampled independently from a distribution _𝑄𝐺𝑇_ over _𝐺𝑇_ for both the input and the calibration datapoints: 

#### _𝛼𝑖_ ( _𝑋𝑡,𝑤_ ) = PredictionError( _𝑔𝑖, 𝑀_ ( _𝑔𝑖_ ( _𝑋𝑡,𝑤_ ))) : 1 ≤ _𝑖_ ≤ _𝑛,𝑔𝑖_ ∼ _𝑄𝐺𝑇 ,_ 

where _𝑋𝑡,𝑤_ is the input or a calibration datapoint. Using Fisher’s method to combine these _𝑛𝑝_ -values gives us the fisher-value of input from equation (3). This value is expected to be higher for iD datapoints than OOD datapoints [11], and therefore we perform detection by using a threshold on the fisher-value of input. In other words, CODiT uses fisher-value of the input as the final OOD detection score. 

**Motivation for multiple** _𝑝_ **-values for OOD Detection.** A single _𝑝_ -value measures deviation from the iD _𝐺𝑇_ -equivariance of the input with respect to one transformation _𝑔_ ∼ _𝑄𝐺𝑇_ . With multiple _𝑝_ -values, we test this deviation with respect to multiple transformations sampled independently from _𝑄𝐺𝑇_ . We hypothesize that under one transformation, an OOD window might behave as the transformed iD window but the likelihood of this decreases with the number of transformations. For testing this hypothesis, we train three VAE models with the set _𝐺𝑇_ equal to _{_ 2 _x speed, reverse, identity}_ , _{_ 2 _x speed, shuffle, periodic, identity}_ , and _{_ 2 _x speed, reverse, shuffle, periodic, identity}_ , respectively. These models are trained on the proper training set of the drift dataset to predict an applied transformation _𝑔_ sampled independently from a uniform distribution over _𝐺𝑇_ . Again, we use CrossEntropyLoss( _𝑔, 𝑀_ ( _𝑔_ ( _𝑋𝑡,𝑤_ ))) as the TTPE-NCM. Fig. 5 shows that the detection performance (in AUROC and TNR) of CODiT increases as we increase the number _𝑛_ of _𝑝_ -values used in the final OOD detection score (or the fishervalue) for all of the three cases (| _𝐺𝑇_ | = 3 _,_ 4 _,_ and 5). This supports our hypothesis on using multiple _𝑝_ -values for enhancing detection. 

_5.2.2 Algorithm and Guarantee for OOD Detection._ For the ICAD guarantees from Lemma 1 to hold on a _𝑝_ -value for an input sampled from the training distribution of LEC, we require the calibration set used in the _𝑝_ -value computation to be IID. With time-series calibration traces, we propose to create an IID calibration set by using exactly one calibration window from each calibration trace. For each calibration trace, this window is sampled independently from a uniform distribution over the sliding windows in the trace. With _𝑄𝐺𝑇_ as the distribution over the set _𝐺𝑇_ of temporal transformations, non-conformity scores on the windows in the calibration set are computed from the TTPE-NCM by sampling a transformation independently from _𝑄𝐺𝑇_ for each window in the set. _𝑛_ such sets of non-conformity scores computed on the _𝑛_ (IID) calibration sets are passed as an input to the proposed Algorithm 1 for OOD detection in time-series data for CPS. 

Line 4 of the Algorithm samples a transformation _𝑔_ independently from _𝑄𝐺𝑇_ . The transformed input _𝑔_ ( _𝑋𝑡,𝑤_ ) is passed through 

the VAE model _𝑀_ trained to learn _𝐺𝑇_ -equivariance on the windows drawn from the proper training data of LEC (Line 5). Line 6 computes the non-conformity score _𝛼_ of _𝑋𝑡,𝑤_ from the TTPE-NCM, which is the prediction error function _𝑓_ over the applied transformation _𝑔_ on _𝑋𝑡,𝑤_ and the transformation _𝑔_ ˆ predicted by _𝑀_ . _𝑝_ -value of _𝑋𝑡,𝑤_ is computed in Line 7 by comparing its non-conformity score with these scores on the calibration windows. This process from sampling a transformation from _𝑄𝐺𝑇_ to computing the _𝑝_ -value of _𝑋𝑡,𝑤_ is repeated _𝑛_ times to compute _𝑛𝑝_ -values of _𝑋𝑡,𝑤_ (Lines 3 to 8). _𝑋𝑡,𝑤_ is detected as OOD if the fisher-value computed from its _𝑛 𝑝_ -values is less than the desired false alarm rate _𝜖_ (Line 10). 

#### **Algorithm 1** CODiT: OOD Detection in Time-Series Data for CPS 

- 1: **Input:** a window _𝑋𝑡,𝑤_ of time-series data, VAE model _𝑀_ trained on proper training set of the iD windows for LEC, distribution _𝑄𝐺𝑇_ over the set _𝐺𝑇_ of temporal transformations, prediction error function _𝑓_ , _𝑛_ sets of calibration set alphas { _𝛼_<sup>_𝑘_</sup> _𝑗_<sup>: 1≤</sup><sup>_𝑘_≤</sup> _𝑛,𝑚_ + 1 ≤ _𝑗_ ≤ _𝑙_ }, and desired false alarm rate _𝜖_ ∈(0 _,_ 1) 


![](CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems_images/CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems.pdf-0006-12.png)


Theorem 1. _The probability of false OOD detection on 𝑋𝑡,𝑤 by Algorithm 1 is upper bounded by 𝜖._ 

The proof of Theorem 1 is included in Appendix. 

The unconditional probability that an input _𝑋𝑡,𝑤_ sampled from the training distribution _𝐷_ is classified as OOD by Algorithm 1 is bounded by _𝜖_ . For this guarantee to hold for a sequence of input windows, we require an independent calibration set for every input in the sequence. This is computationally inefficient for real-time applications and therefore a fixed calibration set is used for all the inputs in the offline version of the ICAD algorithm [22]. The average false alarm rate on the sequence of inputs drawn from _𝐷_ in this setting is expected to be empirically calibrated with or even higher than _𝜖_ . We also fix the _𝑛_ sets of IID calibration datapoints and pass it as an input to the Algorithm 1 on sliding windows of OOD traces from the drift dataset. Box plots in Fig. 5 (right) on the drift dataset shows that the false alarm rate of CODiT is empirically bounded by _𝜖_ on average. Details about these plots are in Appendix. 

### **6 EXPERIMENTAL RESULTS** 

We perform the following experiments: 

- (1) **Comparison with the point-based approaches.** With images taken in clear daytime weather as iD for perception LEC in an autonomous car, existing approaches report their results on weather OODs. So, we perform experiments on weather and night OODs for the closed-loop of advanced 

125 

CODiT: Conformal OOD Detection in Time-Series Data for CPS 

ICCPS ’23, May 9–12, 2023, San Antonio, TX, USA 


![](CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems_images/CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems.pdf-0007-02.png)


**Figure 4: Higher values of TTPE-NCM** = **CrossEntropyLoss** ( _𝑔, 𝑀_ ( _𝑔_ ( _𝑋𝑡,𝑤_ ))) **on OOD windows than on the test iD windows of the drift dataset. This shows that** _𝐺𝑇_ **-equivariance learned on the windows drawn from the training distribution of LEC is less likely to generalize on the windows drawn from OOD.** 


![](CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems_images/CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems.pdf-0007-04.png)



![](CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems_images/CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems.pdf-0007-05.png)



![](CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems_images/CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems.pdf-0007-06.png)


**Figure 5: AUROC vs.** _𝑛_ **(left), TNR (with detection threshold at 95% TPR) vs.** _𝑛_ **(center) shows that the performance of CODiT increases with the increase in the number** _𝑛_ **of** _𝑝_ **-values used in the fisher-value for detection. False Alarm Rate (FDR) of CODiT is empirically bounded by** _𝜖_ **on average (right). The yellow line in the box plot indicates the median.** 


![](CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems_images/CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems.pdf-0007-08.png)


**Figure 6: Closed-loop of Advanced Emergency Braking System (AEBS) with perception LEC from [36].** 


![](CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems_images/CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems.pdf-0007-10.png)


**Figure 7: Medical CPS with the LEC to classify walking pattern or GAIT of a young or an elderly person.** 

emergency braking system (AEBS) with perception LEC from [36]. This system is shown in Fig. 6. Here, we compare CODiT’s performance with all the existing detectors. 

- (2) **Temporal OODs for perception LEC.** We perform experiments on replay OODs for the AEBS with perception LEC in Fig. 6. We also perform experiments on videos from drift 

dataset [25] as temporal OODs in driving scenario. Here, we compare CODiT’s performance with the existing state-ofthe-art (SOTA) non-point approach by Feng et al. [10]. 

- (3) **Temporal OODs in Medical CPS.** We consider temporal OODs for the walking pattern or GAIT classification problem in medical CPS from [3]. As shown in Fig. 7, a LEC is trained on sensory readings collected with force-sensitive resistors attached to the subject’s body for classifying the GAIT from a young or an elderly person. With the training data collected from healthy participants (without any injuries or diseases), input from patients with neurogenerative diseases are OODs for this LEC. We show that CODiT can be used to detect these temporal OODs in non-vision domain. 

We also perform parameter analysis for CODiT on the drift dataset. 

### **6.1 Weather OODs in AEBS with Perception LEC** 

**System Description.** The closed-loop of advanced emergency braking system (AEBS) with perception LEC is shown in Fig. 6. The perception LEC is used to estimate distance to the front obstacle from the ego vehicle. This distance is fed to the emergency braking controller that issues braking commands to the vehicle for stopping at a safe distance from the front obstacle. The LEC is trained on images captured by the front camera on the vehicle in a clear daytime weather. This closed-loop system is simulated in CARLA [9], an open-source simulator for autonomous driving research. For more details about this system, please refer to [36]. 

**In-Distribution Data.** We generate 33 driving traces of varying lengths in clear day weather as the iD training traces for the AEBS 

126 

ICCPS ’23, May 9–12, 2023, San Antonio, TX, USA 

Kaur et al. 

in CARLA. We randomly split these into 20 traces of the proper training set _𝑋𝑡𝑟_ and 13 traces of the calibration set _𝑋𝑐𝑎𝑙_ . Windows from _𝑋𝑡𝑟_ are sampled for training the perception LEC. Windows from _𝑋𝑐𝑎𝑙_ are sampled _𝑛_ = 20 times (with one window from each calibration trace at a time to make each window in the set independent) for calculating the 20 sets of calibration non-conformity scores. We generate another set of 27 traces of varying lengths in clear weather as the iD test traces. 

**OOD Data.** Weather (rainy, foggy, and snowy) and night time OOD traces are generated by using the automold software [28] on the 27 iD test traces. OOD traces start from iD and gradually become OOD, i.e., the intensity of rain, fog, snow, or low brightness (for night) starts increasing gradually turning into the OOD traces. Examples of windows from these OOD traces are shown in Appendix. 

**Implementation Details of Algorithm 1.** We train a VAE model _𝑀_ with the R3D network architecture [34] on the windows of length _𝑤_ = 16 from _𝑋𝑡𝑟_ . R3D network is the 3D CNN with residual connections and thus can be used on the 3D time-series input data. We use _𝐺𝑇_ = { _2x Speed, Shuffle, Periodic, Reverse, Identity_ } and train _𝑀_ to predict the applied transformation _𝑔_ ∈ _𝐺𝑇_ with crossentropy loss between the applied and the predicted transformations. The value of the CrossEntropyLoss( _𝑔, 𝑀_ ( _𝑔_ ( _𝑋𝑡,𝑤_ ))) is used as the non-conformity score _𝛼_ for computing _𝑝_ -value of an input _𝑋𝑡,𝑤_ . 

**Results.** We report results on the sliding windows ( _𝑤_ = 16) of the test iD and OOD traces. We call iD as positive and OOD as negative. We report area under receiving operator curve (AUROC), and the detection delay (with detection threshold _𝜖_ at 95% True Positive Rate) in Table 2. Details about these evaluation metrics are in Appendix. ‘NA’ in the table means that the approach could not detect any OOD window with detection threshold at 95% TPR. 

For CODiT, we report mean and variance from five runs with random sampling of calibration windows from the calibration traces. For AUROC, CODiT outperforms other approaches, except for Snowy OODs, where our results are comparable with the best results by the memory detector. For detection delay, while we outperform other approaches on Foggy and Night OODs, our results on Rainy and Snowy OODs are comparable with the best results. 

### **6.2 Temporal OODs in Driving Scenario** 

We compare CODiT’s performance with the current non-point based SOTA OOD detector, i.e., Feng et al. [10]’s on the replay and drift datasets as temporal OODs for perception LEC: 

**Replay Dataset.** Replay traces are generated from the 27 iD test traces in CARLA for AEBS by randomly sampling a position in each trace. All images from the sampled position in the trace are replaced with the image at the sampled position in the original trace. Again, results are reported for _𝑛_ = 20, and on the sliding windows of replay OODs. 

**Drift Dataset.** We split 72 iD video traces of cars driving straight without any drift from the drift dataset [25] into 24 for _𝑋𝑡𝑟_ , 14 for _𝑋𝑐𝑎𝑙_ , and 34 for test iD traces. Windows from _𝑋𝑡𝑟_ are sampled for training the VAE. Windows from _𝑋𝑐𝑎𝑙_ are sampled _𝑛_ = 20 times 

(with one window from each calibration trace at a time to make each window in the set independent) for calculating the 20 sets of calibration non-conformity scores. We report results on the sliding windows of 34 iD test and 100 OOD drift traces. 

**Results.** We use the same VAE model’s architecture, _𝐺𝑇_ , and nonconformity score as described in Section 6.1. Fig. 8 (left) compares the ROC, AUROC and TNR (@95% TPR) results of CODiT with Feng et al.’s detector on the replay and drift OODs. We achieve SOTA results on both temporal OODs for perception LEC. 

**Parameter Analysis on drift.** We perform the following parameter analysis on the drift dataset. All VAE models used in these studies are trained on the proper training set of the drift dataset with the same model architecture, _𝐺𝑇_ , and non-conformity score from Section 6.1. 

(1) **Performance of CODiT with Different Window Lengths** _𝑤_ **:** We train two VAE models with _𝑤_ = 18 _,_ 20 and compare the performance of CODiT ( _𝑛_ = 20) with Feng et al.’s detector on these window lengths. Fig 8 (right) shows that with both _𝑤_ = 18 and 20, CODiT performs consistently well. 

(2) **Performance of CODiT with Different** |GT| **:** We compare the performance of CODiT with different sizes of the transformation set. Table 3 shows that the performance of CODiT ( _𝑛_ = 5) increases with | _𝐺𝑇_ |. 

(3) **Using Deviation from iD** _𝐺𝑇_ **-equivariance as NCM:** With _𝐺𝑇_ = {2x _𝑠𝑝𝑒𝑒𝑑,𝑠ℎ𝑢𝑓𝑓𝑙𝑒,𝑟𝑒𝑣𝑒𝑟𝑠𝑒, 𝑝𝑒𝑟𝑖𝑜𝑑𝑖𝑐,𝑖𝑑𝑒𝑛𝑡𝑖𝑡𝑦_ }, and for all ground truth temporal transformations in _𝐺𝑇_ , Fig. 4 shows that the non-conformity score from the TTPE-NCM is much higher for OOD windows than the test iD windows. This justifies our hypothesis that _𝐺𝑇_ -equivariance learned by a model on windows drawn from training distribution is not likely to generalize on windows drawn from OOD. 

(4) **CODiT’s Performance Increases with** _𝑛_ **:** We train three VAE models with _𝐺𝑇_ equal to _{_ 2 _x speed, reverse, identity}_ , _{_ 2 _x speed, shuffle, periodic, identity}_ , and _{_ 2 _x speed, reverse, shuffle, periodic, identity}_ . Results on AUROC and detection rate in Fig. 5 shows that the performance of CODiT improves with the number _𝑛_ of _𝑝_ -values used for detection in all the three cases (| _𝐺𝑇_ | = 3 _,_ 4 _,_ and 5). This justifies our hypothesis that under one transformation an OOD window might behave as a transformed iD window but the likelihood of that decreases with the number of transformations. 

(5) **Bounded FDR:** With _𝜖_ = 0 _._ 05 _. 𝑘,𝑘_ = 1 _, . . . ,_ 10, Fig. 5 (right) shows that the false alarm rate of CODiT ( _𝑛_ = 5) is empirically calibrated with _𝜖_ (on average) for the VAE model with | _𝐺𝑇_ | = 5 as described above. We also compare with the FDR guarantees of related work [5, 27] in Appendix. 

### **6.3 Temporal OODs in Medical CPS** 

**System Description.** Walking pattern (or GAIT) analysis data is collected from healthy (young and elderly) subjects walking on treadmill with force-sensitive resistors (FSR) attached to their bodies. As shown in Fig. 7, this data from the FSR is used to train a LEC to classify GAIT of a young or a elderly person [3]. 

**Dataset.** GAIT dataset [15] consists of records on 16 healthy subjects. We split these into 6 for _𝑋𝑡𝑟_ , 5 for _𝑋𝑐𝑎𝑙_ , and 5 for test iD 

127 

ICCPS ’23, May 9–12, 2023, San Antonio, TX, USA 

CODiT: Conformal OOD Detection in Time-Series Data for CPS 

− **Table 2: Comparison of CODiT with the point-based detectors: Cai et al.’s (VAE), Ramakrishna et al.’s (** _𝛽_ **VAE), Yang et al.’s (Memory), and the non-point based detector by Feng et al. on weather and night OODs from the CARLA dataset in AEBS.** 

|OOD||AUROC|(↑)|||Detectio|n Delayi|n Seco|nds(↓)|
|---|---|---|---|---|---|---|---|---|---|
|VAE|_𝛽_−VAE|Memory|Feng’s|CODiT|VAE|_𝛽_−VAE|Memory|Feng’s|CODiT|
|Rainy<br>53.56|92.07|97.56|84.21|**99.68**±**0.00**|NA|0.92|**0.80**|5.06|0.86±0.00|
|Foggy<br>52.02|41.02|85.33|86.09|**99.70**±**0.00**|27.24|16.52|5.15|5.10|**0.84**±**0.00**|
|Snowy<br>53.23|97.52|**97.56**|95.91|97.00±0.05|NA|1.06|**0.80**|**0.80**|0.89±0.01|
|Night<br>50.86|95.57|94.70|75.07|**98.69**±**0.03**|59.04|4.06|5.72|69.12|**2.17**±**0.14**|




![](CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems_images/CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems.pdf-0009-04.png)



![](CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems_images/CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems.pdf-0009-05.png)


**Figure 8: CODiT outperforms SOTA detector by Feng et al. [10] on temporal OODs in driving scenarios with the window length** _𝑤_ = 16 **(left). CODiT performs consistently well with different window lenghts of** _𝑤_ = 18 _,_ **and** 20 **on drift dataset (right).** 

**Table 3: Performance of CODiT increases with the size of the transformation set** _𝐺𝑇_ **.** 

||_𝐺𝑇_||Transformations|AUROC|
|---|---|---|
||Speed, Identity, Shufe|84.78|
|3|Reverse, Shufe, Identity|85.47|
||Speed, Reverse, Identity|87.67|
||Speed, Shufe, Periodic, Identity|88.08|
|4|Speed, Identity, Shufe, Reverse|88.76|
||Speed, Reverse, Periodic, Identity|89.56|
|5|Speed, Shufe, Reverse, Periodic, Identity|90.78|



records. We use 27 records from the severe patient group with neurodegenerative diseases as OOD records. These 27 records contain 9 records from patients of the three diseases: Amyotrophic Lateral Sclerosis (ALS), Parkinson’s (PD), and Huntington’s disease (HD). 

**Impementation Details of Algorithm 1.** We use the 1D derived time-series features from the dataset (the .ts files) to train a VAE model with the Lenet5 architecture [23] on windows sampled from _𝑋𝑡𝑟_ . Lenet5 uses 2D CNN that can be used on the time-series data of 1D feature space. We use _𝐺𝑇_ = {high-pass filter, high-low filter, low-high filter, identity}. By high-low (or low-high) filter, we mean that we apply high (or low)-pass filter to the first half features and low (or high)-pass filter to the last half features of the dataset. Again, we use the value of the cross entropy-loss between the applied and predicted transformations as the non-conformity score. 

**Baseline and Results.** Since Feng et al.’s approach is not applicable for detection on non-vision datasets, we generate a non-point baseline for comparing CODiT’s results. We train a one-class SVM on the auto-correlated features in the time dimension of all the sliding windows in _𝑋𝑡𝑟_ as the baseline. We report results on the sliding windows of the test iD and OODs records. Again, for CODiT, we report mean and variance from five runs with random sampling 

**Table 4: AUROC of baseline/CODiT for OOD detection on GAIT dataset with different window lengths** _𝑤_ **.** 

|OOD|_𝑤_|=16||_𝑤_=18|_𝑤_|=20|
|---|---|---|---|---|---|---|
||Baseline|CODiT<br>|Baseline|CODiT|Baseline|CODiT|
|ALS|**78.25**|67.27±0.63|77.73|**79.54**±**0.00**|77.99|**80.65**±**0.00**|
|PD|74.11|**85.33**±**0.20**|74.18|**84.18**±**0.01**|74.52|**84.12**±**0.02**|
|HD|76.97|**93.72**±**0.13**|76.64|**95.59**±**0.01**|76.68|**93.52**±**0.02**|
|ALL|76.23|**83.71**±**0.41**|75.99|**87.01**±**0.03**|76.21|**86.57**±**0.01**|



of calibration windows from the calibration traces. Table 4 compares the AUROC performance of CODiT ( _𝑛_ = 100) with baseline on individual and all (ALS, PD, and HD) OODs with different sliding window lengths _𝑤_ (16, 18, and 20). As can be seen, CODiT consistently performs well. 

### **7 CONCLUSION AND DISCUSSION** 

We propose to use time-dependency between the datapoints in a time-series window for OOD detection on the window. Specifically, we propose using deviation from the temporal equivariance learned by a model on windows drawn from training distribution of LEC as an NCM in the conformal prediction framework for OOD detection in time-series data for CPS. Computing independent predictions from multiple conformal detectors from the proposed measure and combining these predictions by Fisher’s method leads to the proposed detector CODiT with guarantees on false alarms. We illustrate the efficacy of CODiT by achieving SOTA results in autonomous driving, and GAIT analysis in medical CPS. 

The time complexity analysis of CODiT is as follows. At inference time, ICAD computes the non-conformity score of an input and compares it with the scores of the pre-computed (in offline settings) calibration datapoints for anomaly detection. The time-complexity of ICAD is therefore O(non-conformity score computation of the 

128 

ICCPS ’23, May 9–12, 2023, San Antonio, TX, USA 

Kaur et al. 

input+|calibration set|). Non-conformity score computation in our case is the output generation (i.e., prediction of the applied transformation) by the VAE model. We found it to be approximately 0.003 seconds in our experiments. The time-complexity of ICAD is for calculating one _𝑝_ -value of the input. CODiT uses multiple ( _𝑛_ ) _𝑝_ -values and combine them using Fisher’s test for OOD detection. So, the time-complexity of CODiT = _𝑛_ × time-complexity of the ICAD framework, where _𝑛_ is the number of _𝑝_ -values. Therefore the time-complexity of CODiT increases linearly with the number _𝑛_ of _𝑝_ -values used for detection. As seen from Fig. 5, detection performance of CODiT improves with _𝑛_ . So, it is a trade-off between time-complexity and detection performance. We also observe that the performance of CODiT improves with the number of transformations in the set of temporal transformations. So, using all (instead of choosing a subset) of temporal transformations suitable for the application works better for CODiT. As a future work, we plan to explore the performance of CODiT with non-temporal transformations on the windows of time-series datapoints as these windows capture the temporal aspect of the input data. 

### **8 ACKNOWLEDGEMENT** 

This work was supported in part by ARO W911NF-20-1-0080, AFRL and DARPA FA8750-18-C-0090, and U.S. Army Research Laboratory Cooperative Research Agreement W911NF-17-2-0196. Any opinions, findings and conclusions or recommendations expressed in this material are those of the authors and do not necessarily reflect the views of the Army Research Office (ARO), the Air Force Research Laboratory (AFRL), the Defense Advanced Research Projects Agency (DARPA), or the Department of Defense, or the United States Government. 

### **REFERENCES** 

- [1] Vineeth Balasubramanian, Shen-Shyang Ho, and Vladimir Vovk. 2014. _Conformal prediction for reliable machine learning: theory, adaptations and applications_ . Newnes. 

- [2] Michele Basseville, Igor V Nikiforov, et al. 1993. _Detection of abrupt changes: theory and application_ . Vol. 104. prentice Hall Englewood Cliffs. 

- [3] Rezaul Begg and Joarder Kamruzzaman. 2006. Neural networks for detection and classification of walking pattern changes due to ageing. _Australasian Physics & Engineering Sciences in Medicine_ 29, 2 (2006), 188–195. 

- [4] Mariusz Bojarski, Davide Del Testa, Daniel Dworakowski, Bernhard Firner, Beat Flepp, Prasoon Goyal, Lawrence D Jackel, Mathew Monfort, Urs Muller, Jiakai Zhang, et al. 2016. End to end learning for self-driving cars. _arXiv preprint arXiv:1604.07316_ (2016). 

- [5] Feiyang Cai and Xenofon Koutsoukos. 2020. Real-time out-of-distribution detection in learning-enabled cyber-physical systems. In _2020 ACM/IEEE 11th International Conference on Cyber-Physical Systems (ICCPS)_ . IEEE, 174–183. 

- [6] Evangelos Chatzipantazis, Stefanos Pertigkiozoglou, Kostas Daniilidis, and Edgar Dobriban. 2021. Learning Augmentation Distributions using Transformed Risk Minimization. _arXiv preprint arXiv:2111.08190_ (2021). 

- [7] Shuxiao Chen, Edgar Dobriban, and Jane H Lee. 2020. A group-theoretic framework for data augmentation. _JMLR_ 21, 245 (2020), 1–71. 

- [8] Jeffrey De Fauw, Joseph R Ledsam, Bernardino Romera-Paredes, Stanislav Nikolov, Nenad Tomasev, Sam Blackwell, Harry Askham, Xavier Glorot, Brendan O’Donoghue, Daniel Visentin, et al. 2018. Clinically applicable deep learning for diagnosis and referral in retinal disease. _Nature medicine_ 24, 9 (2018), 1342–1350. 

- [9] Alexey Dosovitskiy, German Ros, Felipe Codevilla, Antonio Lopez, and Vladlen Koltun. 2017. CARLA: An open urban driving simulator. In _Conference on robot learning_ . PMLR, 1–16. 

- [10] Yeli Feng, Daniel Jun Xian Ng, and Arvind Easwaran. 2021. Improving Variational Autoencoder based Out-of-Distribution Detection for Embedded Real-time Applications. _ACM Transactions on Embedded Computing Systems (TECS)_ 20, 5s (2021), 1–26. 

- [11] RA Fisher. 1932. Statistical Methods for Research Workers. 4* Edition Oliver & Boyd. 

- [12] Jingkun Gao, Xiaomin Song, Qingsong Wen, Pichao Wang, Liang Sun, and Huan Xu. 2020. Robusttad: Robust time series anomaly detection via decomposition 

   - and convolutional neural networks. _arXiv preprint arXiv:2002.09545_ (2020). 

- [13] Georgia Gkioxari, Ross Girshick, and Jitendra Malik. 2015. Contextual action recognition with r* cnn. In _Proceedings of the IEEE international conference on computer vision_ . 1080–1088. 

- [14] Matan Haroush, Tzviel Frostig, Ruth Heller, and Daniel Soudry. 2021. A Statistical Framework for Efficient Out of Distribution Detection in Deep Neural Networks. In _International Conference on Learning Representations_ . 

- [15] Jeffrey M Hausdorff, Apinya Lertratanakul, Merit E Cudkowicz, Amie L Peterson, David Kaliton, and Ary L Goldberger. 2000. Dynamic markers of altered gait rhythm in amyotrophic lateral sclerosis. _Journal of applied physiology_ (2000). 

- [16] Dan Hendrycks and Kevin Gimpel. 2017. A Baseline for Detecting Misclassified and Out-of-Distribution Examples in Neural Networks. In _International Conference on Learning Representations_ . 

- [17] Simon Jenni and Hailin Jin. 2021. Time-equivariant contrastive video representation learning. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ . 9970–9980. 

- [18] Yiannis Kantaros, Taylor Carpenter, Kaustubh Sridhar, Yahan Yang, Insup Lee, and James Weimer. 2021. Real-time detectors for digital and physical adversarial inputs to perception systems. In _Proceedings of the ACM/IEEE 12th International Conference on Cyber-Physical Systems_ . 67–76. 

- [19] Ramneet Kaur, Susmit Jha, Anirban Roy, Sangdon Park, Edgar Dobriban, Oleg Sokolsky, and Insup Lee. 2022. iDECODe: In-distribution Equivariance for Conformal Out-of-distribution Detection, Association for the Advancement of Artificial Intelligence. arXiv:2201.02331 [cs.LG] 

- [20] Ramneet Kaur, Susmit Jha, Anirban Roy, Sangdon Park, Oleg Sokolsky, and Insup Lee. 2021. Detecting oods as datapoints with high uncertainty. _arXiv preprint arXiv:2108.06380_ (2021). 

- [21] Ramneet Kaur, Susmit Jha, Anirban Roy, Oleg Sokolsky, and Insup Lee. 2021. Are all outliers alike? On Understanding the Diversity of Outliers for Detecting OODs. _arXiv preprint arXiv:2103.12628_ (2021). 

- [22] Rikard Laxhammar and Göran Falkman. 2015. Inductive conformal anomaly detection for sequential detection of anomalous sub-trajectories. _Annals of Mathematics and Artificial Intelligence_ 74, 1 (2015), 67–94. 

- [23] Yann LeCun, Léon Bottou, Yoshua Bengio, and Patrick Haffner. 1998. Gradientbased learning applied to document recognition. _Proc. IEEE_ 86, 11 (1998), 2278– 2324. 

- [24] Navonil Majumder, Soujanya Poria, Alexander Gelbukh, and Erik Cambria. 2017. Deep learning-based document modeling for personality detection from text. _IEEE Intelligent Systems_ 32, 2 (2017), 74–79. 

- [25] Alam Noor, Bilel Benjdira, Adel Ammar, and Anis Koubaa. 2020. DriftNet: Aggressive Driving Behavior Classification using 3D EfficientNet Architecture. _arXiv preprint arXiv:2004.11970_ (2020). 

- [26] Guo-Jun Qi, Liheng Zhang, Chang Wen Chen, and Qi Tian. 2019. Avt: Unsupervised learning of transformation equivariant representations by autoencoding variational transformations. In _Proceedings of the IEEE International Conference on Computer Vision_ . 8130–8139. 

- [27] Shreyas Ramakrishna, Zahra Rahiminasab, Gabor Karsai, Arvind Easwaran, and Abhishek Dubey. 2021. Efficient Out-of-Distribution Detection Using Latent Space of _𝛽_ -VAE for Cyber-Physical Systems. _arXiv preprint:2108.11800_ (2021). 

- [28] Ujjwal Saxena. 2018. Automold. https://github.com/UjjwalSaxena/Automold-Road-Augmentation-Library. 

- [29] Uwe Schmidt and Stefan Roth. 2012. Learning rotation-aware features: From invariant priors to equivariant descriptors. In _2012 IEEE Conference on Computer Vision and Pattern Recognition_ . IEEE, 2050–2057. 

- [30] Johannes Stallkamp, Marc Schlipsing, Jan Salmen, and Christian Igel. 2012. Man vs. computer: Benchmarking machine learning algorithms for traffic sign recognition. _Neural networks_ 32 (2012), 323–332. 

- [31] Jihoon Tack, Sangwoo Mo, Jongheon Jeong, and Jinwoo Shin. 2020. Csi: Novelty detection via contrastive learning on distributionally shifted instances. _Advances in Neural Information Processing Systems_ 33 (2020). 

- [32] Ashish Tiwari, Bruno Dutertre, Dejan Jovanović, Thomas de Candia, Patrick D Lincoln, John Rushby, Dorsa Sadigh, and Sanjit Seshia. 2014. Safety envelope for security. In _Proceedings of the 3rd international conference on High confidence networked systems_ . 85–94. 

- [33] Paolo Toccaceli and Alexander Gammerman. 2017. Combination of conformal predictors for classification. In _Conformal and Probabilistic Prediction and Applications_ . PMLR, 39–61. 

- [34] Du Tran, Heng Wang, Lorenzo Torresani, Jamie Ray, Yann LeCun, and Manohar Paluri. 2018. A closer look at spatiotemporal convolutions for action recognition. In _Proceedings of the IEEE conference on Computer Vision and Pattern Recognition_ . 6450–6459. 

- [35] Vladimir Vovk, Ilia Nouretdinov, and Alexander Gammerman. 2003. Testing exchangeability on-line. In _Proceedings of the 20th International Conference on Machine Learning (ICML-03)_ . 768–775. 

- [36] Yahan Yang, Ramneet Kaur, Souradeep Dutta, and Insup Lee. 2022. Interpretable Detection of Distribution Shifts in Learning Enabled Cyber-Physical Systems. In _ACMIEEE International Conference on CyberPhysical Systems_ . 

129 

ICCPS ’23, May 9–12, 2023, San Antonio, TX, USA 

CODiT: Conformal OOD Detection in Time-Series Data for CPS 

### **A APPENDIX** 


![](CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems_images/CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems.pdf-0011-03.png)


**Figure 9: GAIT in patients with neurodegenerative diseases [15] as temporal OODs in medical CPS.** 

**Evaluation metrics** : We call iD as positives and OOD as negatives. We abbreivate by TP, FN, TN, and FP the notions of true positive, false negative, true negative and false positive. We use True Negative Rate (TNR) at 95% True Positive Rate (TPR), the Area under Receiver Operating characteristic curve (AUROC), and detection delay for evaluation. The first metric is TNR = TN/(TN+FP), when TPR = TP/(TP+FN) is 95%. It indicates the percentage of OOD windows detected correctly when 95% of the iD windows are detected correctly. AUROC plots TPR against the false positive rate FP/(FP+TN) by varying detection thresholds. Higher TNR and AUROC scores indicate a good detection performance of the detector. Starting from the first ground truth OOD window in a trace, the time (in seconds) required to detect the first OOD window in the trace is used as the detection delay. This number is averaged over the total number of OOD traces and reported in Table 2. A lower detection delay is desired for real-time deployment of the detector. 

**Proof of Theorem 1** . An IID calibration set is used for a _𝑝_ - value computation in Algorithm 1. If an input _𝑋𝑡,𝑤_ is sampled from the training distribution of LEC, then _𝑋𝑡,𝑤_ and datapoints in the calibration set are also IID. The non-conformity scores of _𝑋𝑡,𝑤_ and calibration datapoints used in the _𝑝_ -value computation of Line 7 of the Algorithm 1 are therefore IID conditioned on the proper training set and the set of temporal transformations _𝐺𝑇_ . With the _𝑛_ IID calibration sets sampled independently from the calibration traces, _𝑛_ non-conformity scores computed from _𝑛_ transformations sampled independently from _𝑄𝐺𝑇_ for both the input and the calibration datapoints, and Lemma 1, the _𝑛𝑝_ -values of _𝑋𝑡,𝑤_ computed in Algorithm 1 are independent and uniformly distributed. Due to this property on the _𝑛𝑝_ -values and Lemma 2, the combined _𝑝_ -value in Line 10 of Algorithm 1 is also uniformly distributed. Therefore, the probability of falsely detecting _𝑋𝑡,𝑤_ as OOD from the combined _𝑝_ -value (or fisher-value( _𝑋𝑡,𝑤_ )) is upper bounded by _𝜖_ due to Lemma 1. □ 

#### **False Alarm Rate (FDR) Guarantees** 

_Details about the box-plots in Fig. 5 of the paper._ We increase the number of calibration datapoints to empirically check the FDR with respect to _𝜖_ . We increase the number of calibration traces from 14 to 34 and include all sliding windows on all the calibration traces in the 

calibration set. This gives us a calibration set with a larger number of approximately 862 calibration datapoints. 34 calibration traces are randomly selected from the set of 48 in-distribution traces and the rest 14 are used as test traces. This is repeated 5 times and the generated box-plot of CODiT ( _𝑛_ = 5) for | _𝐺𝑇_ | = 5 is shown in Fig. 5 (right) of the paper. For all the values of _𝜖_ = 0 _._ 05 _.𝑘,𝑘_ = 1 _, . . . ,_ 10 in the plot, the average FDR is better aligned with _𝜖_ . 

_Comparison of FDR with the related work_ : Two of the existing detectors, i.e. VAE-based Cai et al.’s detector [5], and _𝛽_ VAE-based Ramakrishna et al.’s detector [27] are also based on the ICAD framework. Since both of these approaches are point-based (i.e. treat each point in the window independently), we compare them with CODiT ( _𝑛_ = 5) on CARLA’s weather OODs. Fig. 10 shows the box-plots for CODiT (left) the existing detectors (center and right) on the CARLA dataset. Again, these box plots are reported on 5 trials with randomly sampled 27 calibration and 13 test traces from 40 in-distribution traces in each trial. Using all the sliding windows of the 27 calibration traces in this experiment gives us a total of approximately 2800 calibration datapoints. We observe that the quartile range for Ramakrishna et al.’s method increases with _𝜖_ . For Cai et al.’s method, the average FDR is always much lower than _𝜖_ , i.e., average FDR is not calibrated with _𝜖_ . Average FDR for CODiT is aligned with _𝜖_ for all the values of _𝜖_ and has a much lower quartile ranges than Ramakrishna’s method. 

#### **Related work on OOD Detection on Individual datapoints and** 

**Anomaly Detection.** OOD detection in non time-series datasets such as GTSRB has been extensively studied and detectors with OOD scores based on the difference in statistical, geometrical or topological properties of the individual iD and OOD datapoints have been proposed. These detectors can be classified into supervised [21], self-supervised [31], and unsupervised [16] categories. Unsupervised approaches do not require access to any OOD data for training the detector, while supervised approaches do. Selfsupervised approaches are the current SOTA for OOD detection which require a self-labeled dataset for training the detector. This dataset is created by applying transformations to the training data and labeling the transformed data with the applied transformation. CODiT, an OOD detector on time-series data, is a self-supervised OOD detection approach, where the self-labeled dataset is created by applying temporal transformations on the windows drawn from the training distribution. Anomaly detection in time-series data is also a closely related and an active research area [12]. In this paper, we consider the detection of a special class of anomalous data, the OOD data (data lying outside the training distribution). For instance, let us consider the case where most of the training data is clean and the rest is adversarially perturbed. Here, the rare adversarial inputs are anomalous with respect to the training data, where most of the training data is drawn from the training distribution of clean data. However, adversarial inputs are not OOD as some of the training data is sampled from the training distribution of these adversarially perturbed data. 

**Examples of iD and OOD windows.** Here we show: (1) A window from the iD trace of the drift dataset, (2) A window from the iD trace of the CARLA dataset in AEBS, and (3) Windows from the weather and night OOD traces from the CARLA dataset in AEBS. 

130 

ICCPS ’23, May 9–12, 2023, San Antonio, TX, USA 

Kaur et al. 


![](CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems_images/CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems.pdf-0012-02.png)



![](CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems_images/CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems.pdf-0012-03.png)



![](CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems_images/CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems.pdf-0012-04.png)


**Figure 10: Box-plots on False Alarm Rate (FDR) vs detection threshold** _𝜖_ **for CODiT (left) and existing detectors (center and right) on the CARLA dataset in AEBS.** 


![](CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems_images/CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems.pdf-0012-06.png)


**Figure 11: A window from an iD trace of the drift dataset: car driving straight without any drift.** 


![](CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems_images/CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems.pdf-0012-08.png)


**Figure 12: A window from an iD trace of the CARLA dataset: driving in the clear daytime weather.** 


![](CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems_images/CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems.pdf-0012-10.png)


**Figure 13: An OOD window from the foggy trace. The intensity of fog gradually increases in these OOD traces.** 


![](CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems_images/CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems.pdf-0012-12.png)


**Figure 14: An OOD window from the night trace. The intensity of brightness gradually decreases in these OOD traces.** 


![](CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems_images/CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems.pdf-0012-14.png)


**Figure 15: An OOD window from the snowy trace. The intensity of snow gradually increases in these OOD traces.** 


![](CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems_images/CODiT_Conformal_Out-of-Distribution_Detection_in_Time-SeriesData_for_Cyber-Physical_Systems.pdf-0012-16.png)


**Figure 16: An OOD window from the rainy trace. The intensity of rain gradually increases in these OOD traces.** 

131 

