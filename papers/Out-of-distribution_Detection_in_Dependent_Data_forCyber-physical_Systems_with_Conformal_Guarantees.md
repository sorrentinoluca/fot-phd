# **Out-of-distribution Detection in Dependent Data for Cyber-physical Systems with Conformal Guarantees** 

RAMNEET KAUR, University of Pennsylvania, Philadelphia, USA YAHAN YANG, University of Pennsylvania, Philadelphia, USA OLEG SOKOLSKY, University of Pennsylvania, Philadelphia, USA INSUP LEE, University of Pennsylvania, Philadelphia, USA 

Uncertainty in the predictions of learning-enabled components hinders their deployment in safety-critical cyber-physical systems (CPS). A shift from the training distribution of a learning-enabled component (LEC) is one source of uncertainty in the LEC’s predictions. Detection of this shift or out-of-distribution (OOD) detection on individual datapoints has therefore gained attention recently. But in many applications, inputs to CPS form a temporal sequence. Existing techniques for OOD detection in time-series data for CPS either do not exploit temporal relationships in the sequence or do not provide any guarantees on detection. We propose using deviation from the in-distribution temporal equivariance as the non-conformity measure in conformal anomaly detection framework for OOD detection in time-series data for CPS. Computing independent predictions from multiple conformal detectors based on the proposed measure and combining these predictions by Fisher’s method leads to the proposed detector CODiT with bounded false alarms. 

CODiT performs OOD detection on fixed-length windows of consecutive time-series datapoints by using Fisher value of the input window. We further propose performing OOD detection on real-time time-series traces of variable lengths with bounded false alarms. This can be done by using CODiT to compute Fisher values of the sliding windows in the input trace and combining these values by a merging function. Merging functions such as Harmonic Mean, Arithmetic Mean, Geometric Mean, Bonferroni Method, and so on, can be used to combine Fisher values of the sliding windows in the input trace, and the combined value can be used for OOD detection on the trace with bounded false alarm rate guarantees. 

We illustrate the efficacy of CODiT by achieving state-of-the-art results in two case studies for OOD detection on fixed-length windows. The first one is on an autonomous driving system with perception (or vision) LEC. The second case study is on a medical CPS for walking pattern or GAIT analysis where physiological (non-vision) data is collected with force-sensitive resistors attached to the subject’s body. For OOD detection on variable length traces, we consider the same case studies on the autonomous driving system and medical CPS for GAIT analysis. We report our results with four merging functions on the Fisher values computed by CODiT on the sliding windows of the input trace. We also compare the false alarm rate guarantees by these four merging functions in the autonomous driving system case study. Code, data, and trained models are available at https://github.com/kaustubhsridhar/time-series-OOD. 

### CCS Concepts: • **Computing methodologies** → **Temporal reasoning** 

This work was sponsored in part by the Army Research Office and was accomplished under Grant Number W911NF-20-10080. 

Authors’ address: R. Kaur, Y. Yang, O. Sokolsky, and I. Lee, University of Pennsylvania, Philadelphia, PA, 19104-6221; e-mails: ramneetk@seas.upenn.edu, yangy96@seas.upenn.edu, sokolsky@seas.upenn.edu, lee@seas.upenn.edu. Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for components of this work owned by others than the author(s) must be honored. Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. Request permissions from permissions@acm.org. © 2024 Copyright held by the owner/author(s). Publication rights licensed to ACM. ACM 2378-962X/2024/10-ART46 https://doi.org/10.1145/3648005 

ACM Trans. Cyber-Phys. Syst., Vol. 8, No. 4, Article 46. Publication date: October 2024. 

R. Kaur et al. 

46:2 

Additional Key Words and Phrases: Learning-enabled components, cyber-physical systems, time-series, outof-distribution, dependent data, conformal detection, false alarms guarantees 

### **ACM Reference Format:** 

Ramneet Kaur, Yahan Yang, Oleg Sokolsky, and Insup Lee. 2024. Out-of-distribution Detection in Dependent Data for Cyber-physical Systems with Conformal Guarantees. _ACM Trans. Cyber-Phys. Syst._ 8, 4, Article 46 (October 2024), 27 pages. https://doi.org/10.1145/3648005 

## **1 INTRODUCTION** 

With remarkable performance-levels of machine learning across different domains [13, 32], there is much interest in using these **learning-enabled components (LEC)** in **cyber-physical systems (CPS)** . A prime example of this trend is autonomous driving, where a car would be equipped with the capability to autonomously perform certain operations, such as adaptive cruise control, emergency braking, or lane following [4]. These autonomous features aim to enhance the safety of the vehicle and its occupants. But as drivers rely on them more and more, a malfunction in such a feature would be detrimental to safety. The black-box nature of LEC makes it difficult to interpret their uncertain predictions on perturbed inputs [20, 27, 38] or even inputs from novel environments from training [46]. For instance, Yang et al. (2022) show that an ego vehicle that uses a perception LEC to estimate the following distance to a car in front of it crashes when the car is replaced by a bike. This is because the LEC was trained with cars in front of the ego vehicle and could not correctly estimate distance from bikes (novel object from training). Deployment of LEC in safetycritical CPS such as autonomous driving [4], and healthcare [8], therefore, requires providing a certain level of assurance [21, 25]. This work focuses on the detection of shift in the distribution of the LEC’s inputs from its training distribution for providing evidence-based assurance on the decisions made by LEC in safety-critical CPS. 

Detection of shift from the training distribution of LEC or **out-of-distribution (OOD)** detection on individual datapoints has received broad attention [16, 23, 26, 40]. But this problem of OOD detection in time-series data for CPS is less explored. In time-series data, OOD detection aims at detecting those inputs of time-series datapoints that are outside the training distribution of LEC [5, 10, 35, 46]. In this case, the distribution of interest is not just of individual datapoints, but the distribution of sequences in which these datapoints occur in the time-series data. We propose CODiT, a novel algorithm for OOD detection with a bounded false alarm rate on fixed-length time-series windows for CPS. 

Most of the existing approaches for OOD detection in time-series data for CPS are _point-based_ , i.e., they independently consider each datapoint in the input, such as individual frames in a video clip. In other words, these approaches do not exploit time-dependency among the datapoints in the input to detect if the input is OOD. An example of an OOD input in a driving scenario is a car drifting video clip due to slippery ground or loss of control, given normal driving video clips as **in-distribution (iD)** data. As shown in Figure 1, we cannot tell from a single frame if the car has drifted, since drift is defined based on the relative relation between frames (e.g., a trajectory of a car). We define these OOD inputs as _temporal OODs_ , which require considering the sequence of datapoints in the input for detection. In contrast to the existing point-based approaches for detection in time-series data for CPS, we propose using time-dependency among the datapoints in the input for detection of temporal OODs. 

Specifically, we propose _using deviation from the iD temporal equivariance_ , i.e., equivariance with respect to a set of temporal transformations learned by a model on windows drawn from the training distribution of LEC, _for OOD detection in time-series data_ . This is because a model trained to learn equivariance with respect to temporal transformations on data drawn from the 

ACM Trans. Cyber-Phys. Syst., Vol. 8, No. 4, Article 46. Publication date: October 2024. 

OOD Detection in Dependent Time-Series Data for CPS with Conformal Guarantees 

46:3 


![](Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees_images/Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees.pdf-0003-02.png)


Fig. 1. Drift in cars as temporal OODs in driving scenario. This trace is taken from the drift dataset by Noor et al. [33]. 

training distribution might not generalize or exhibit equivariance on OOD inputs dissimilar to the training distribution. To bound false alarms on the iD data, we leverage **inductive conformal anomaly detection (ICAD)** [1]. ICAD is a general framework for testing if an input conforms to the training distribution by computing quantitative scores defined by a non-conformity measure. A _p_ -value, computed by comparing non-conformity score of the input with these scores on the data drawn from training distribution, indicates anomalous behavior of the input. The detection performance of ICAD, however, depends on the choice of the non-conformity measure used in the framework [1]. We propose using _deviation from the expected temporal equivariant behavior of a model learned on data drawn from training distribution of LEC_ as the non-conformity measure in ICAD for OOD detection in the time-series data for CPS. 

ICAD computes a single _p_ -value of the input to detect its anomalous behavior. To enhance detection performance, we propose using multiple ( _n_ > 1) _p_ -values computed from _n_ transformations sampled as **independent and identically distributed (IID)** variables from a distribution over the set of temporal transformations. The intuition for using multiple transformations is that an OOD window might behave as a transformed iD window with one transformation, but the likelihood of this decreases with the number of temporal transformations. Using Fisher’s method [42] to combine these _n_ independent _p_ -values leads to the proposed detector CODiT for conformal OOD detection in time-series data for CPS with a bounded false alarm rate. We call the combined _p_ -value by using Fisher’s method as the Fisher _p_ -value.<sup>1</sup> 

CODiT performs OOD detection on fixed-length windows of time-series data. For OOD detection on inputs or traces of variable lengths, we propose using CODiT on sliding windows of the input trace. Specifically, we propose using CODiT for computing Fisher _p_ -values of sliding windows in the trace and combining these values via merging functions defined by Vovk and Wang [45]. These merging functions can be used to combine dependent _p_ -values (such as the Fisher _p_ - values of sliding windows in the trace) while still preserving the false alarm rate guarantees from the ICAD framework. 

The contributions can be summarized as: 

- (1) **Novel Measure for OOD Detection in Time-series Data for CPS.** To our knowledge, all the existing non-conformity measures for OOD detection are defined on individual datapoints. We propose a measure that is defined on the window containing information about the sequence of time-series datapoints for enhancing detection of the temporal OODs. We leverage a model trained to learn iD temporal equivariance via the auxiliary task of predicting an applied temporal transformation on the windows drawn from the training distribution of LEC. And we propose using error in the model’s prediction of the applied transformation as the non-conformity measure in ICAD for OOD detection in time-series data for CPS. 

- (2) **Enhanced Detection Performance.** To enhance the detection performance, we propose to use Fisher’s method as an ensemble approach for combining predictions from multiple conformal detectors based on the proposed measure. 

- (3) **CODiT: OOD Detection on Fixed-length Time-series Inputs to CPS.** Computing _n_ independent _p_ -values of the input window from the proposed measure in the ICAD framework 

> 1We use the terms “Fisher _p_ -value” and “Fisher-value” interchangeably in the article. 

ACM Trans. Cyber-Phys. Syst., Vol. 8, No. 4, Article 46. Publication date: October 2024. 

R. Kaur et al. 

46:4 

and combining these values by Fisher’s method leads to the proposed detector CODiT with a bounded false alarm rate for OOD detection on fixed-length windows of time-series data for CPS. 

- (4) **CODiT-v: OOD Detection on Variable-length Time-series Inputs to CPS.** We propose using CODiT for computing Fisher _p_ -values of the sliding windows in a trace and combining these dependent _p_ -values via merging functions defined by Vovk and Wang [45]. The combined _p_ -value can be used to perform OOD detection on variable-length traces with false alarm rate guarantees. We call the proposed algorithm as CODiT-v: using CODiT for OOD detection on **v** ariable-length traces. 

- (5) **Evaluation.** 

- (a) For comparison of CODiT with the point-based detectors on fixed-length input windows, we perform experiments on weather and night OOD windows in an autonomous driving system with perception LEC, achieving **state-of-the-art (SOTA)** results. We outperform the existing non-point-based SOTA [10] on temporal OOD windows in driving scenario. To illustrate that CODiT can be used for OOD detection beyond vision, we also perform experiments on medical CPS for walking pattern or GAIT analysis where physiological (non-vision) time-series data is collected with force-sensitive resistors attached to the subject’s body [15]. 

- (b) For OOD detection on variable-length traces, we use the same case studies as described above: an autonomous driving system with perception LEC and medical CPS for GAIT analysis. We report our results with four merging functions in CODiT-v, namely, Harmonic Mean, Arithmetic Mean, Geometric Mean, and Bonferroni Method from Reference [45]. We also compare the false alarm rate guarantees on traces by these four merging functions. 

**Extension to the Existing Work:** This article is an extension of our ICCPS work: “CODiT: Conformal Out-of-Distribution Detection in Time-Series Data for Cyber-Physical Systems” [28]. In this article, we extend the existing algorithm CODiT for OOD detection on fixed-length timeseries inputs to CODiT-v: an OOD detection on **v** ariable-length time-series inputs. We provide alternatives to the proposed algorithm for varying length inputs and motivation for CODiT-v. We prove that the false alarm rate by CODiT-v is bounded by the desired detection threshold specified by the user. We, further, illustrate the efficacy of CODiT-v by experimental results on two case studies: autonomous driving systems with temporal and non-temporal OODs, and medical CPS with temporal OODs. We also empirically evaluate the false alarm rate guarantees by CODiTv in the autonomous driving system case study with temporal OODs. The main contribution in this extension is the application of merging functions from Reference [45] for solving the problem of dependent _p_ -values for OOD detection on variable length trace with false detection rate guarantees. 

The article is organized as follows: We begin with the problem statement and motivation for CODiT and CODiT-v in Section 2. Section 3 sheds light on the related work for OOD detection in standalone deep learning models, OOD detection in time-series data for learning-enabled components in CPS, as well as anomaly detection in time-series data. We provide a background on the existing concepts and frameworks on which the proposed tools are built, namely, temporal equivariance, inductive conformal anomaly detection, and multiple testing of the same hypothesis in Section 4. Section 5 is the main technical section of the article, providing details about CODiT and CODiT-v. Details about the two case studies and experimental results on these are presented in Section 6. Finally, the article concludes with a summary and time-complexity analysis of both the tools in Section 7. 

ACM Trans. Cyber-Phys. Syst., Vol. 8, No. 4, Article 46. Publication date: October 2024. 

OOD Detection in Dependent Time-Series Data for CPS with Conformal Guarantees 

46:5 


![](Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees_images/Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees.pdf-0005-02.png)


Fig. 2. Replay window: An example of the temporal OOD where camera gets stuck and generates the same image in the entire window. This trace is generated by CARLA, an open-source simulator for autonomous driving research [9]. 


![](Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees_images/Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees.pdf-0005-04.png)


Fig. 3. ROC curves (left), TNR (with detection threshold at 95% TPR on right) results on replay OOD windows by the existing point-based OOD detectors in time-series data for CPS. These approaches perform poorly in the detection of these temporal OOD windows. We call iD as positive and OOD as negative. 

## **2 PROBLEM STATEMENT AND MOTIVATION** 

## **2.1 Problem Statement** 

In this article, we consider the following two settings for OOD in time-series data for CPS: 

_2.1.1 OOD Detection on Fixed-length Windows of Time-series Data._ In this setting, the input is the fixed-length ( _w_ ) window _Xt_ , _w_ of consecutive time-series datapoints ( _xt_ , _xt_ +1, . . . , _xt_ + _w_ −1) to the LEC in the system, and output is the label for _Xt_ , _w_ as iD or OOD. Here, _t_ is the starting time of the window. 

_2.1.2 OOD Detection on Variable-length Traces of Time-series Data._ In this setting, the input is a variable-length trace _Xt_ of consecutive time-series datapoints ( _xt_ , _xt_ +1, . . . , _xt_ + | _Xt_ |−1) to the LEC in the system, and output is the label for _Xt_ as iD or OOD. Here, _t_ is the starting time of the trace. 

## **2.2 Motivation of the Proposed OOD Detection Measure in CODiT** 

The existing point-based detectors for OOD detection in time-series data might not be able to detect temporal OOD windows to the system. An example of a temporal OOD in driving scenario, as shown in Figure 2, is the replay window where camera gets stuck at a single frame and starts generating the same image over and over again. We need to consider the sequence of same image in a replay window to detect the window as OOD. Detection results on replay dataset in Figure 3 shows that all the existing point-based detectors, namely, **variational autoencoder (VAE)** -based Cai et al.’s Reference [5], _β_ VAE-based Ramakrishna et al.’s Reference [35], and memory-based Yang et al.’s Reference [46] detectors perform poorly in the detection of these temporal OOD windows. We, therefore, propose using time-dependency among the datapoints in a window for OOD detection in time-series data for CPS. 

To our knowledge, Feng et al.’s detector [10] is the only existing OOD detector that takes into account time-dependency among the individual datapoints in a window. It does so by extracting optical flow information from consecutive frames in a video clip. As shown in Figure 15 of Section 6, Feng et al.’s detector can thus be used to detect temporal OOD windows. However, since this detector depends on the optical flow information, it is restricted to vision data. In contrast, CODiT can be used to detect temporal OOD windows across domains (vision or non-vision) without relying on any domain-specific features. Table 1 compares the detection capabilities of CODiT with the existing OOD detectors in time-series data. 

ACM Trans. Cyber-Phys. Syst., Vol. 8, No. 4, Article 46. Publication date: October 2024. 

R. Kaur et al. 

46:6 

Table 1. Capabilities of Detectors in Time-series Data for CPS 

|OOD|False Alarm Rate|Temporal|Non-vision|
|---|---|---|---|
|Detector|Guarantees|OODs|Data|
|VAE [5]|✓|**?**|✓|
|_β_-VAE[35]|✓|**?**|✓|
|Memory [46]|✗|**?**|✓|
|Feng et al.’s [10]|✗|✓|✗|
|CODiT/CODiT-v(Ours)|✓|✓|✓|



## **2.3 Motivation for CODiT-v: The Proposed Algorithm for OOD Detection on Variable-length Inputs** 

CODiT-v combines the Fisher _p_ -values computed by CODiT on the sliding windows in the trace for OOD detection on the trace. These Fisher _p_ -values are combined via merging functions defined by Vovk and Wang [45] for OOD detection with bounded false alarm rate guarantees on traces of variable lengths. There can be other ways for adapting the existing detectors such as CODiT that are defined on fixed-length inputs for detection on variable-length inputs. A straightforward alternative would be setting the window length equal to the trace length and utilizing these detectors for OOD detection on traces. This, however, requires training models used in these detectors such as VAE on all possible input lengths and choosing the appropriate model at runtime based on the input length. 

Another alternative could be running CODiT on the sliding windows of the input trace and raising an alarm on the detection of an OOD window. This, however, limits the bounded false alarm rate guarantees to the windows of the input trace, and not the entire trace. 

## **3 RELATED WORK** 

OOD detection in non-time-series datasets such as **German Traffic Sign Recognition (GTSRB)** [39] has been extensively studied and detectors with OOD scores based on the difference in statistical, geometrical, or topological properties of the individual iD and OOD datapoints have been proposed. These detectors can be classified into supervised [24], self-supervised [40], and unsupervised [16] categories. Unsupervised approaches do not require access to any OOD data for training the detector, while supervised approaches do. Self-supervised approaches are the current SOTA for OOD detection, which require a self-labeled dataset for training the detector. This dataset is created by applying transformations to the training data and labeling the transformed data with the applied transformation. CODiT, an OOD detector on time-series data, is a self-supervised OOD detection approach, where the self-labeled dataset is created by applying temporal transformations on the windows drawn from the training distribution. OOD detection in CPS with low-dimensional input space through envelopes has also been studied in the past [41]. 

Recently, there has been interest in leveraging ICAD for OOD detection with guarantees on false alarm rate on high-dimensional input space [5, 14, 22, 35]. While iDECODe [22] and Haroush et al.’s Reference [14] are OOD detectors for individual datapoints, Cai et al.’s Reference [5] and Ramakrishna et al.’s Reference [35] are detectors for time-series data. iDECODe uses error in the equivariance learned by a model with respect to a transformation set on individual datapoints as the **non-conformity measure (NCM)** in ICAD for detection in non-time-series data. Haroush et al. propose using a combined _p_ -value from different channels and layers of **convolutional neural networks (CNN)** for detection. It is not clear how to directly apply individual point detectors to time-series data with the ICAD guarantees due to the following two reasons: First, even if we apply these detectors to individual datapoints in the time-series window independently, we do 

ACM Trans. Cyber-Phys. Syst., Vol. 8, No. 4, Article 46. Publication date: October 2024. 

OOD Detection in Dependent Time-Series Data for CPS with Conformal Guarantees 

46:7 

not know how to combine detection verdicts on these datapoints for detection on the window. Second, for detection guarantees by ICAD, it is required that all non-conformity scores for _p_ -value computation to be IID [29]. Since these detectors are not solving OOD detection problem in timeseries data it is not clear how to apply them to time-series while preserving the IID assumption on the time-series data. Also, iDECODe uses a single _p_ -value for detection and we propose using multiple ( _n_ > 1) independent _p_ -values to be combined by the Fisher’s method for preserving the detection guarantees. In contrast to Reference [14], our approach is not limited to CNN and can be used for other predictive models as well. 

Cai et al. [5] propose using reconstruction error by VAE on an input image as the NCM in the ICAD framework. Martingale formula [44] is used to combine multiple _p_ -values computed on multiple samples of the input in the latent space of VAE. The detection score on a time-series window is then computed by applying cumulative sum procedure [2] on the martingale values of all images in the window. Ramakrishna et al. [35] propose using KL-divergence between the disentangled feature space of _β_ -VAE on an input image and the normal distribution, as the NCM in ICAD. They also use the martingale formula to combine _p_ -values of all the images in the window for detection. Recently, Yang et al. [46] proposed computing few prototypes (or memories) from the training data and using distance of an input image with these prototypes for detection on the input. The time-series window to the CPS is labeled as OOD if majority datapoints in the window are detected as OOD. Unlike the other two detectors [5, 35], this approach does not provide false alarm rate guarantees on detection. All of these three OOD detectors [5, 35, 46] on time-series data are point-based, and as shown by the experiments on replay OOD windows, these might perform poorly in the detection of temporal OODs. CODiT computes the _p_ -value of the window (and not individual datapoints in the window) in the ICAD framework. It is, therefore, a non-point-based approach that can be used to detect temporal OOD windows (Sections 6.1.2, 6.1.3). 

To our knowledge, the only non-point-based approach for OOD detection in time-series data is by Feng et al. [10]. They propose extracting optical flow information from a time-series window and training a VAE on this information. KL-divergence between the trained VAE and a specified prior is used as the OOD score. This detector uses optical flow to extract time-dependency in the frames of a window and thus can be used to detect temporal OODs. However, this approach does not provide any guarantees on detection and will not work on non-vision datasets, as it relies on optical flows. As shown in the experiments on the GAIT dataset in medical CPS, CODiT can be used for OOD detection in non-vision domain. 

Anomaly detection in time-series data is also a closely related and an active research area [12, 18, 19, 31]. In this article, we consider the detection of a special class of anomalous data, the OOD data (data lying outside the training distribution). For instance, let us consider the case where most of the training data is clean and the rest is adversarially perturbed.<sup>2</sup> Here, the rare adversarial inputs are anomalous with respect to the training data, where most of the training data is drawn from the training distribution of clean data. However, adversarial inputs are not OOD, as some of the training data is sampled from the training distribution of these adversarially perturbed data. 

## **4 BACKGROUND AND NOTATIONS** 

CODiT uses error in the temporal equivariance learned by a model on windows drawn from the training distribution of LEC as the non-conformity measure in the **inductive conformal anomaly detection (ICAD)** framework. With multiple _p_ -values obtained from the proposed measure in ICAD, the final OOD detection score is computed by combining these values by Fisher’s method. 

> 2By adversarial perturbations, we mean that physical distortions or digital noise are added to the input for changing the prediction of the LEC from the ground truth to the desired one. For more details, please refer to References [27, 38]. 

ACM Trans. Cyber-Phys. Syst., Vol. 8, No. 4, Article 46. Publication date: October 2024. 

R. Kaur et al. 

46:8 

Here, we provide the background on equivariance, ICAD, and Fisher’s method required for technical details of the proposed OOD detector, CODiT for OOD detection on fixed-length inputs. We also provide details about the merging functions that can be used in CODiT-v for combining the Fisher _p_ -values (computed by CODiT) on sliding windows of an input trace for OOD detection on varying-length inputs. In this section, we also define the notations used in the rest of the article. 

## **4.1 Equivariance** 

A function _f_ is equivariant with respect to a transformation _д_ if we know how the output of _f_ changes if we transform its input from _x_ to _д_ ( _x_ ). 

Invariance is a special case of equivariance where the output of _f_ does not change by the transformation _д_ on its input. Invariance with respect to geometric transformations such as rotation, tilt, scale, and so on, is a desired property of the machine learning classifiers. For example, classification results on the straight images of planes should not change with a tilt in these images. 

_Definition 1 (Schmidt and Roth [37])._ For a set _X_ , a function _f_ is defined to be equivariant with respect to a set of transformations _G_ if there exists the following relationship between any transformation _д_ ∈ _G_ of the function’s input and the corresponding transformation _д_<sup>′</sup> of the function’s output: 


![](Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees_images/Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees.pdf-0008-07.png)


Invariance is a special case of equivariance where _д_<sup>′</sup> is the identity function, i.e., the output of _f_ remains unchanged by the transformation _д_ on its input. 

_4.1.1 Learning Equivariance:_ **Autoencoding Variational Transformations (AVT)** _._ Augmenting training data with transformations from the set _G_ of geometric transformations is a common approach to learning invariance with respect to _G_ [6, 7]. The auxiliary task of predicting an applied transformation from _G_ on the training data also encourages the model to learn equivariance with respect to _G_ [34]. Qi et al.’s 2019 “Autoencoding Variational Transformations” (AVT) framework trains a VAE to learn a latent space that is equivariant to transformations. For the set _X_ of training images and the set _G_ of geometric transformations, a VAE is trained to predict the applied transformation from _G_ on an input _x_ ∈ _X_ . Equivariance between the latent space of VAE and _G_ is learned by maximizing mutual information between the latent space and _G_ . 

_Definition 2 (Jenni and Jin [17])._ Temporal equivariance of a function _f_ from (1) is defined on a set _X_ of windows of consecutive time-series datapoints and with respect to a set _G_ of temporal transformations. 

Some examples of temporal transformations on video clips are skipping every second frame in the clip (2× speed), shuffling frames in the clip (shuffle), reversing the order of frames in the clip (reverse), and reversing the order of the second half frames in the clip (periodic). In the rest of the article, we will use the notation _GT_ to represent a set of temporal transformations and call the function _f_ from Definition 2 as _GT_ -equivariant if it learns equivariance w.r.t. _GT_ on windows drawn from the training distribution of LEC. We refer to the deviation from the expected result of this function _f_ on a transformed input (transformed with a _д_ ∈ _GT_ ) as deviation from the iD _GT_ -equivariance. 

## **4.2 Inductive Conformal Anomaly Detection** 

**Inductive Conformal Anomaly Detection (ICAD)** [29] is a general framework for testing if an input conforms to the training distribution. It is based on a **non-conformity measure (NCM)** , which is a real-valued function that assigns a non-conformity score _α_ to the input. This score 

ACM Trans. Cyber-Phys. Syst., Vol. 8, No. 4, Article 46. Publication date: October 2024. 

OOD Detection in Dependent Time-Series Data for CPS with Conformal Guarantees 

46:9 

indicates non-conformance of the input with data drawn from the training distribution. The higher the score is, the more non-conforming or anomalous the input is with respect to training data. An example of the non-conformity score is the reconstruction error by a VAE trained on data drawn from the training distribution. 

The training dataset _X_ of size _l_ is split into a _proper training set X_ tr = { _xj_ : _j_ = 1, . . . , _m_ } and a _calibration set X_ cal = { _xj_ : _j_ = _m_ + 1, . . . , _l_ }. Proper training set _X_ tr is used in defining NCM. In the example of reconstruction error by a VAE as the non-conformity score, the VAE trained on _Xtr_ is used for computing the error. Calibration set _X_ cal is a held-out training set that is used for computing _p_ -value of an input. _p_ -value of an input _x_ is computed by comparing its non-conformity score _α_ ( _x_ ) with these scores on the calibration datapoints: 


![](Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees_images/Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees.pdf-0009-04.png)


If _x_ is drawn from the training distribution, then the expected value of its non-conformity score would lie within the range of scores for the calibration datapoints, and therefore uniform distribution of _p_ -values for iD datapoints. With _ϵ_ ∈(0, 1) as the anomaly detection threshold, _x_ is detected as an anomalous input if the _p_ -value of _x_ is less than _ϵ_ . 

_4.2.1 False Alarm Rate Guarantees._ The false anomalous detection on an input drawn from the training distribution is upper bounded by the specified detection threshold _ϵ_ in ICAD. 

Lemma 1 (Balasubramanian et al. [1]). _If an input x and the calibration datapoints xm_ +1, . . . , _xl are independent and identically distributed (IID), then for any choice of the NCM defined on the proper training set Xtr, the p-value(x) in Equation_ (2) _is uniformly distributed. Moreover, we have Pr_ ( _p-value_ ( _x_ ) < _ϵ_ ) ≤ _ϵ, where the probability is taken over xm_ +1, . . . , _xl , and x._ 

From Lemma 1, we know that if _x_ and the datapoints in the calibration set _X_ cal are IID, then the _p_ - value( _x_ ) from Equation (2) is uniformly distributed over {1/( _l_ − _m_ +1), 2/( _l_ − _m_ +1), . . . , 1}. The probability of _p_ -value( _x_ ) less than _ϵ_ or misclassifying _x_ as anomalous is, therefore,<sup>�</sup> 1≤ _i_ ≤( _l_ − _m_ +1) _ϵ_<sup>1/(</sup><sup>_l_−</sup> _m_ + 1) = ⌊( _l_ − _m_ + 1) _ϵ_ ⌋/( _l_ − _m_ + 1) ≤ _ϵ_ . 

## **4.3 Multiple Testing of the Same Hypothesis** 

The same hypothesis can be tested by multiple conformal predictors, and an ensemble approach for combining these predictions can be used to improve upon the performance of individual predictors. Fisher’s method is one of these approaches for combining multiple conformal predictions or _p_ - values of an input from Equation (2). Fisher’s method, however, requires all the _p_ -values used in testing the hypothesis to be independent for preserving the false alarm rate guarantees from ICAD. Recently, Vovk and Wang [45] proposed a number of merging functions that can be used to combine dependent _p_ -values for testing the hypothesis without violating detection guarantees from ICAD. Here, we first provide background about Fisher’s method used in CODiT and then details about the merging functions that can be used in CODiT-v for combining the dependent Fisher _p_ -values of the sliding windows in an input trace. 

_4.3.1 Fisher’s Method [42]._ Fisher’s method can be used for combining independent _p_ -values of an input from Equation (2). Fisher-value of an input _x_ from _n p_ -values is computed as: 


![](Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees_images/Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees.pdf-0009-12.png)


Lemma 2 (Toccaceli and Gammerman [42]). _If n p-values, p_ 1, . . . , _pn, are independently drawn from a uniform distribution of these values, then_ −2<sup>�</sup><sup>_n_</sup> _i_ =1<sup>log</sup><sup>_pifollows a chi-square distribution with_</sup> 

ACM Trans. Cyber-Phys. Syst., Vol. 8, No. 4, Article 46. Publication date: October 2024. 

R. Kaur et al. 

46:10 

2 _n degrees of freedom. Thus, the combined p-value is_ 


![](Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees_images/Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees.pdf-0010-03.png)


_where r_ =<sup>�</sup><sup>_n_</sup> _k_ =1<sup>_pk, yisarandomvariablefollowingachi-squaredistributionwith_2</sup><sup>_ndegreesof_</sup> _freedom, and the probability is taken over y. Moreover, the combined p-value follows the uniform distribution._ 

_CODiT uses Fisher’s method for combining multiple (n) IID p-values from ICAD on the input window Xt_ , _w for OOD detection on Xt_ , _w ._ 

_4.3.2 Merging Functions [45]._ Multiple _p_ -values ( _p_ 1, . . . , _pK_ ) of an input from Equation (2) can be combined via the following averaging function _Mr_ , _K_ : 


![](Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees_images/Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees.pdf-0010-07.png)


with the special cases of _r_ = 0, ∞, and −∞ defined as follows: 


![](Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees_images/Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees.pdf-0010-09.png)



![](Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees_images/Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees.pdf-0010-10.png)



![](Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees_images/Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees.pdf-0010-11.png)


Vovk and Wang [45] define _merging functions of the form:_ 


![](Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees_images/Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees.pdf-0010-13.png)


Here, _ar_ , _K_ is a constant required for making the merging function valid. The value obtained by applying a _valid merging function_ on the _K_ uniformly distributed _p_ -values is also uniformly distributed. 

We consider the following four merging functions from Reference [45] for combining Fisher _p_ -values in CODiT-v on sliding windows of the input trace. These functions vary in the value of _r_ : 


![](Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees_images/Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees.pdf-0010-16.png)


- (4) **Bonferroni Method (BM)** : With _r_ = −∞, _a_ −∞, _K_ = _K_ , and _M_ −∞, _K_ ( _p_ 1, . . . , _pK_ ) is as defined in Equation (5). 

Lemma 3 (Vovk and Wang [45]). _For all the K p-values uniformly distributed in_ [0, 1] _, the value obtained by applying merging function from Equation_ (6) _on these K p-values is a valid p-value, i.e., the combined p-value is also uniformly distributed in_ [0, 1] _, and therefore Pr_ ( _combined p-value_ < _ϵ_ ) ≤ _ϵ_ , ∀ _ϵ_ ∈(0, 1) _. Validity of the combined p-value holds true without assuming any dependence structure among the K p-values._ 

To avoid confusion, in the rest of the article, we call the combined _p_ -value obtained by applying Fisher’s method from Section 4.3.1 as the Fisher _p_ -value, and the combined _p_ -value obtained by applying merging functions from Section 4.3.2 as the merged _p_ -value. 

ACM Trans. Cyber-Phys. Syst., Vol. 8, No. 4, Article 46. Publication date: October 2024. 

OOD Detection in Dependent Time-Series Data for CPS with Conformal Guarantees 

46:11 


![](Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees_images/Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees.pdf-0011-02.png)


Fig. 4. Walking pattern or GAIT in patients with neurodegenerative diseases [15] as temporal OODs in medical CPS. 

## **5 TEMPORAL EQUIVARIANCE FOR CONFORMAL OOD DETECTION IN TIME-SERIES DATA FOR CPS** 

Here, we first classify OOD data in time-series data into two types and then provide technical details about the proposed detectors CODiT and CODiT-v for OOD detection on fixed and variable length time-series inputs to CPS, respectively. 

## **5.1 OOD Data Types in Time-series** 

We classify OOD data in time-series data into two types: _temporal_ OODs and _non-temporal_ OODs. A crucial property of the temporal OODs compared to the non-temporal OODs is that it is hard to detect temporal OODs by looking at individual datapoints within the window (or the trace) without considering time-dependency between these datapoints. Examples of temporal OODs in driving scenario are car drifting video clips (Figure 1) and replay OODs (Figure 2). An example of the temporal OOD in medical CPS is the GAIT (or waking pattern) of patients with neurodegenerative diseases. With the GAIT of healthy individuals as iD data, the GAIT of patients with neurodegenerative diseases such as **Parkinson’s disease (PD), Huntington’s disease (HD)** , and **Amyotrophic Lateral Sclerosis (ALS)** are examples of temporal OODs. Figure 4 shows dynamics of the stride time (one of the walking pattern features) of a healthy control person and patients with PD, HD, and ALS disease. As shown in the figure, we need a sequence of time-series datapoints to determine whether the walking pattern is from a healthy individual or a patient. In contrast to the temporal OODs, the non-temporal OODs can be detected by looking at individual datapoints. Examples of non-temporal OODs include driving video clips under rainy, foggy, or snowy weather, given the driving video clips under clear sunny weather as iD data. We can detect weather OODs by looking at images in the window independently. 

Based on these observations, we call a window (or a trace) _Xt_ , _w_ (or _Xt_ ) as a temporal OOD if _Xt_ , _w_ (or _Xt_ ) is drawn from OOD but confused to be drawn from iD by removing the time-dependency of individual datapoints within _Xt_ , _w_ (or _Xt_ ). e.g., randomly shuffling the order of video clip frame. As shown in the Experimental Section 6, CODiT and CODiT-v can be used to detect both temporal and non-temporal OODs in time-series data for CPS. 

## **5.2 CODiT: OOD Detection on Fixed-length Windows** _Xt_ , _w_ **of Time-series Data** 

CODiT uses an OOD detection score based on multiple _p_ -values from ICAD. Here, we first define the proposed NCM to be used in the ICAD framework for computing a _p_ -value along with the final detection score and then formalize CODiT’s algorithm with a bounded false alarm rate. 

ACM Trans. Cyber-Phys. Syst., Vol. 8, No. 4, Article 46. Publication date: October 2024. 

R. Kaur et al. 

46:12 

_5.2.1 Proposed NCM and OOD Detection Score._ **TTPE NCM.** We propose to use timedependency between datapoints in a time-series window for detection on the window. Unlike all the existing NCMs defined on individual datapoints, we propose an NCM that is defined on the window containing information about the sequence of datapoints in the window. Specifically, we propose using deviation from the expected iD _GT_ -equivariance learned by a model on windows drawn from the training distribution of LEC as an NCM in ICAD for OOD detection in time-series data for CPS. Learning _GT_ -equivariance via an auxiliary task of predicting the applied temporal transformation (such as shuffle, reverse, etc.) on a window requires learning changes in the original sequence of the datapoints in a predictable way. For a VAE model _M_ trained to learn _GT_ -equivariance on windows of proper training data in the AVT framework, we propose to use error in the prediction of the applied temporal transformation _д_ ∈ _GT_ on an input window _Xt_ , _w_ as the NCM: 

## PredictionError( _д_ , _M_ ( _д_ ( _Xt_ , _w_ ))). 

We call the proposed NCM as the **Temporal Transformation Prediction Error (TTPE)** NCM. 

The existing AVT framework [34] is defined to learn equivariance with respect to geometric transformations on images. We extend it to learn _GT_ -equivariance by: 

- (1) Modifying VAE’s architecture to accept windows of consecutive time-series datapoints as inputs. The time-series can be on vision (e.g., drift car video clip) or non-vision (e.g., GAIT) datapoints. 

- (2) Modifying the auxiliary task to predict the applied temporal transformation from a set _GT_ on windows of time-series datapoints. 

**Motivation for TTPE-NCM.** _GT_ -equivariance learned by a model on windows drawn from the training distribution of LEC is more likely to work on iD data and is not guaranteed to generalize to OOD data dissimilar to that used for training. With the set _GT_ = {2x _speed_ , _shuf f le_ , _reverse_ , _period_ - _ic_ , _identity_ }, we train a VAE model on the proper training data of the drift dataset to predict an applied transformation _д_ sampled independently from a uniform distribution over _GT_ . With _GT_ as the set of five classes of temporal transformations, we use CrossEntropyLoss( _д_ , _M_ ( _д_ ( _Xt_ , _w_ ))) as the TTPE-NCM. Figure 5 shows that the model has much higher prediction errors on the OOD windows than on the test iD windows on all the five ground truth transformations in _GT_ . This supports our hypothesis that _GT_ -equivariance learned on data drawn the training distribution is not likely to generalize on data drawn from OOD, and therefore higher prediction errors on OOD windows than on the iD windows. 

**OOD Detection Score.** Instead of using a single _p_ -value from the TTPE-NCM in ICAD, we propose using multiple ( _n_ > 1) _p_ -values to enhance detection. We require _n_ non-conformity scores for both the input and the calibration windows for computing _n p_ -values. These scores are computed from _n_ transformations sampled independently from a distribution _QGT_ over _GT_ for both the input and the calibration windows: 


![](Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees_images/Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees.pdf-0012-10.png)


where _Xt_ , _w_ is the input or a calibration window. Using Fisher’s method to combine these _n p_ - values gives us the Fisher-value of input from Equation (3). This value is expected to be higher for iD windows than OOD windows [11], and therefore, we perform detection by using a threshold on the Fisher-value of input. In other words, CODiT uses Fisher-value of the input as the final OOD detection score. 

**Motivation for multiple** _p_ **-values for OOD Detection.** A single _p_ -value measures deviation from the iD _GT_ -equivariance of the input with respect to one transformation _д_ ∼ _QGT_ . With 

ACM Trans. Cyber-Phys. Syst., Vol. 8, No. 4, Article 46. Publication date: October 2024. 

OOD Detection in Dependent Time-Series Data for CPS with Conformal Guarantees 46:13 


![](Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees_images/Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees.pdf-0013-01.png)


Fig. 5. Higher values of TTPE-NCM = CrossEntropyLoss( _д_ , _M_ ( _д_ ( _Xt_ , _w_ ))) on OOD windows than on the test iD windows of the drift dataset. This shows that _GT_ -equivariance learned on the windows drawn from the training distribution of LEC is less likely to generalize on the windows drawn from OOD. 


![](Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees_images/Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees.pdf-0013-03.png)


Fig. 6. AUROC vs. _n_ (left), TNR (with detection threshold at 95% TPR) vs. _n_ (center) shows that the performance of CODiT increases with the increase in the number _n_ of _p_ -values used in the Fisher-value for detection. False Alarm Rate (FDR) on fixed-length windows of time-series data by CODiT is empirically bounded by _ϵ_ on average (right). The yellow line in the box-plot indicates the median. 

multiple _p_ -values, we test this deviation with respect to multiple transformations sampled independently from _QGT_ . We hypothesize that under one transformation, an OOD window might behave as the transformed iD window but the likelihood of this decreases with the number of transformations. For testing this hypothesis, we train three VAE models with the set _GT_ equal to _{_ 2 _x speed, reverse, identity}_ , _{_ 2 _x speed, shuffle, periodic, identity}_ , and _{_ 2 _x speed, reverse, shuffle, periodic, identity}_ , respectively. These models are trained on the proper training set of the drift dataset to predict an applied transformation _д_ sampled independently from a uniform distribution over _GT_ . Again, we use CrossEntropyLoss( _д_ , _M_ ( _д_ ( _Xt_ , _w_ ))) as the TTPE-NCM. Figure 6 shows that the detection performance (in AUROC and TNR) of CODiT increases as we increase the number _n_ of _p_ -values used in the final OOD detection score (or the Fisher-value) for all of the three cases (| _GT_ | = 3, 4, and 5). This supports our hypothesis on using multiple _p_ -values for enhancing detection. 

_5.2.2 Algorithm and Guarantee for OOD Detection on Fixed-length Windows._ For the ICAD guarantees from Lemma 1 to hold on a _p_ -value for a window sampled from the training distribution of LEC, we require the calibration set used in the _p_ -value computation to be IID. With time-series calibration traces, we propose to create an IID calibration set by using exactly one calibration window from each calibration trace. For each calibration trace, this window is sampled independently from a uniform distribution over the sliding windows in the trace. With _QGT_ as the distribution over the set _GT_ of temporal transformations, non-conformity scores on the windows in the calibration set are computed from the TTPE-NCM by sampling a transformation independently from _QGT_ for each window in the set. _n_ such sets of non-conformity scores computed on the _n_ (IID) calibration sets are passed as an input to the proposed Algorithm 1 for OOD detection in time-series data for CPS. 

Line 4 of the algorithm samples a transformation _д_ independently from _QGT_ . The transformed input _д_ ( _Xt_ , _w_ ) is passed through the VAE model _M_ trained to learn _GT_ -equivariance on the windows 

ACM Trans. Cyber-Phys. Syst., Vol. 8, No. 4, Article 46. Publication date: October 2024. 

R. Kaur et al. 

46:14 

drawn from the proper training data of LEC (Line 5). Line 6 computes the non-conformity score _α_ of _Xt_ , _w_ from the TTPE-NCM, which is the prediction error function _f_ over the applied transformation _д_ on _Xt_ , _w_ and the transformation _д_ ˆ predicted by _M_ . _p_ -value of _Xt_ , _w_ is computed in Line 7 by comparing its non-conformity score with these scores on the calibration windows. This process from sampling a transformation from _QGT_ to computing the _p_ -value of _Xt_ , _w_ is repeated _n_ times to compute _n p_ -values of _Xt_ , _w_ (Lines 3 to 8). _Xt_ , _w_ is detected as OOD if the Fisher-value computed from its _n p_ -values is less than the desired false alarm rate _ϵ_ (Line 10). 

**ALGORITHM 1:** CODiT: OOD Detection on Fixed-length ( _w_ ) windows of Time-series Data for <u>CPS</u> 

1: **Input:** a window _Xt_ , _w_ of time-series data, VAE model _M_ trained on proper training set of the iD windows for LEC, distribution _QGT_ over the set _GT_ of temporal transformations, prediction error function _f_ , _n_ sets of calibration set alphas { _αj_<sup>_k_:1≤</sup><sup>_k_≤</sup><sup>_n_,</sup><sup>_m_+ 1≤</sup><sup>_j_≤</sup><sup>_l_}, and desired</sup> false alarm rate _ϵ_ ∈(0, 1) 

2: **Output:** “1” if _Xt_ , _w_ is detected as OOD; “0” otherwise 3: **for** _k_ ← 1, . . . , _n_ **do** 4: _д_ ∼ _QGT_ 5: _д_ ˆ ← _M_ ( _д_ ( _Xt_ , _w_ )) 6: _α_ ← _f_ ( _д_ , _д_ ˆ) 7: _pk_ ← |{ _j_ = _m_ +1,..., _l_ − _ml_ :+ _α_ 1 ≤ _α_ _<u>j</u>_<sup>_k_}|+1</sup> 8: **end for** 9: _r_ ←<sup>�</sup><sup>_n_</sup> _k_ =1<sup>_pk_</sup> <u>(−</u> log _r_ <u>)</u><sup>_i_</sup> 10: **if** _r_<sup><u>�</u></sup><sup>_n_</sup> _i_ =<sup>−</sup> 0<sup>1</sup> _i_ ! < _ϵ_ **then return** 1 **else return** 0 

Theorem 1. _The probability of false OOD detection on Xt_ , _w by Algorithm 1 is upper bounded by the detection threshold ϵ._ 

Proof. An IID calibration set is used for a _p_ -value computation in Algorithm 1. If the input window _Xt_ , _w_ is sampled from the training distribution of LEC, then _Xt_ , _w_ and windows in the calibration set are also IID. The non-conformity scores of _Xt_ , _w_ and calibration windows used in the _p_ -value computation of Line 7 of the Algorithm 1 are, therefore, IID conditioned on the proper training set and the set of temporal transformations _GT_ . With the _n_ IID calibration sets sampled independently from the calibration traces, _n_ non-conformity scores computed from _n_ transformations sampled independently from _QGT_ for both the input and the calibration windows, and Lemma 1, the _n p_ -values ( _p_ 1, _p_ 2, . . . , _pn_ ) of _Xt_ , _w_ computed in Algorithm 1 are independent and uniformly distributed. Due to this property on the _n p_ -values and Lemma 2, the Fisher _p_ -value in Line 10 of Algorithm 1 is also uniformly distributed. Fisher _p_ -value is uniformly distributed, because it is the CDF of _t_ = −2<sup>�</sup><sup>_n_</sup> _i_<sup>(</sup><sup>_loд_(</sup><sup>_pi_)) and</sup><sup>_t_is guaranteed to be chi-squared. Therefore, the</sup> probability of falsely detecting _Xt_ , _w_ as OOD from the Fisher _p_ -value( _Xt_ , _w_ )) is upper bounded by _ϵ_ due to Lemma 1. □ 

The unconditional probability that an input window _Xt_ , _w_ sampled from the training distribution _D_ is classified as OOD by Algorithm 1 is bounded by _ϵ_ . For this guarantee to hold for a sequence of input windows, we require an independent calibration set for every input in the sequence. This is computationally inefficient for real-time applications, and therefore a fixed calibration set is used for all the inputs in the offline version of the ICAD algorithm [29]. The average false alarm rate on the sequence of inputs drawn from _D_ in this setting is expected to be empirically calibrated with 

ACM Trans. Cyber-Phys. Syst., Vol. 8, No. 4, Article 46. Publication date: October 2024. 

OOD Detection in Dependent Time-Series Data for CPS with Conformal Guarantees 

46:15 


![](Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees_images/Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees.pdf-0015-02.png)


Fig. 7. Flow diagram of CODiT-v for OOD detection on an input trace _Xt_ . Fisher _p_ -values, _p_ 1, . . . , _pk_ , on the sliding windows of _Xt_ are computed using CODiT and combined via merging function _Mr_ , _k_ for OOD detection on _Xt_ . 

or even higher than _ϵ_ . We also fix the _n_ sets of IID calibration datapoints and pass it as an input to the Algorithm 1 on sliding windows of OOD traces from the drift dataset. Box-plots in Figure 6 (right) on the drift dataset shows that the false alarm rate of CODiT is empirically bounded by _ϵ_ , on average. Details about these plots are included in the Experimental Section 6.1.2. 

## **5.3 CODiT-v: OOD Detection on Variable-length Traces** _Xt_ **of Time-series Data** 

With the dependent time-series data in the sliding windows of a trace _Xt_ , the Fisher _p_ -values for these windows also exhibit dependency. Merging functions defined by Vovk and Wang [45] can be used to combine these dependent Fisher _p_ -values for generating a valid merged _p_ -value. In other words, the probability of falsely labeling an iD trace as OOD from the merged _p_ -value is upper bounded by the detection threshold _ϵ_ . Algorithm 2 is the proposed algorithm CODiT-v for OOD detection on variable-length traces of time-series data to CPS with a bounded false alarm rate. For each sliding window of length _w_ in the input trace _Xt_ , Fisher _p_ -value for the window is generated by running CODiT (or Algorithm 1) on the window (Lines 4 to 6). Line 7 of the algorithm combines the Fisher _p_ -values of all the sliding windows in _Xt_ by using one of the merging functions _MF_ from the set { _HM_ , _AM_ , _GM_ , _BM_ }. If the merged _p_ -value is less than the detection threshold _ϵ_ , then the trace is detected as OOD (Line 8). Figure 7 shows the flow diagram of OOD detection on an input trace _Xt_ by CODiT-v. 

**ALGORITHM 2:** CODiT-v: OOD Detection on Variable-length Traces of Time-series Data for CPS 

- 1: **Input:** a trace _Xt_ of time-series data, merging function _MF_ ∈{HM, AM, GM, BM}, sliding window length _w_ , and the desired false alarm rate _ϵ_ ∈(0, 1) 

- 2: **Parameter:** Inputs required for running CODiT (Algorithm 1) on the sliding windows of _Xt_ 

- 3: **Output:** “1” if _Xt_ is detected as OOD; “0” otherwise 

- 4: **for** _i_ ← _t_ , . . . , | _Xt_ | − _w_ + 1 **do** 

- 5: _ri_ = Fisher _p_ -value for the window _Xt_ [ _i_ , _i_ + _w_ − 1] returned by Line 9 of Algorithm 1 

- 6: **end for** 

- 7: merged _p_ -value = _MF_ { _i_ = _t_ , . . . , | _Xt_ | − _w_ + 1 : _ri_ } 

- 8: **if** merged _p_ -value < _ϵ_ **then return** 1 **else return** 0 

ACM Trans. Cyber-Phys. Syst., Vol. 8, No. 4, Article 46. Publication date: October 2024. 

R. Kaur et al. 

46:16 


![](Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees_images/Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees.pdf-0016-02.png)


Fig. 8. Closed-loop of Advanced Emergency Braking System (AEBS) with perception LEC from Reference [46]. 

Theorem 2. _The probability of false OOD detection on Xt by Algorithm 2 is upper bounded by the detection threshold ϵ._ 

Proof. For a trace _Xt_ drawn from iD data, the Fisher _p_ -values of the sliding windows in _Xt_ from Algorithm 1 are uniformly distributed according to Theorem 1. The merged _p_ -value obtained by applying a valid merging function on these uniformly distributed _p_ -values is also uniformly distributed according to Lemma 3. Therefore, the probability of falsely detecting _Xt_ as OOD from the merged _p_ -value from Algorithm 2 is upper bounded by detection threshold _ϵ_ . □ 

## **6 EXPERIMENTAL RESULTS** 

**Evaluation Metrics Used in the Experiments** : We call iD as positives and OOD as negatives. We abbreviate by TP, FN, TN, and FP the notions of true positive, false negative, true negative and false positive. We use **True Negative Rate (TNR)** at 95% **True Positive Rate (TPR)** , the **Area under Receiver Operating characteristic curve (AUROC)** for evaluation. The first metric is TNR = TN/(TN+FP) when TPR = TP/(TP+FN) is 95%. It indicates the percentage of OOD inputs (windows or traces) detected correctly when 95% of the iD inputs (windows or traces) are detected correctly. AUROC plots TPR against the false positive rate FP/(FP+TN) by varying detection thresholds. Higher TNR and AUROC scores indicate a good detection performance of the detector. 

## **6.1 Results for OOD Detection on Fixed-length Windows of Time-series Data by CODiT (Algorithm 1)** 

We perform the following experiments: 

- (1) **Comparison with the point-based approaches.** With images taken in clear daytime weather as iD for perception LEC in an autonomous car, existing approaches report their results on weather OODs. So, we perform experiments on weather and night OOD windows for the closed-loop of **advanced emergency braking system (AEBS)** with perception LEC from Reference [46]. This system is shown in Figure 8. Here, we compare CODiT’s performance with all the existing detectors on fixed-length input windows. 

- (2) **Temporal OODs for perception LEC.** We perform experiments on replay OOD windows for the AEBS with perception LEC in Figure 8. We also perform experiments on drift dataset [33] as temporal OOD windows in driving scenarios. Here, we compare CODiT’s performance with the existing **state-of-the-art (SOTA)** non-point approach by Feng et al. [10]. 

- (3) **Temporal OODs in Medical CPS.** We consider temporal OODs for the walking pattern or GAIT classification problem in medical CPS from Reference [3]. As shown in Figure 9, a 

ACM Trans. Cyber-Phys. Syst., Vol. 8, No. 4, Article 46. Publication date: October 2024. 

OOD Detection in Dependent Time-Series Data for CPS with Conformal Guarantees 

46:17 


![](Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees_images/Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees.pdf-0017-02.png)


Fig. 9. Medical CPS with the LEC to classify walking pattern or GAIT of a young or an elderly person. 


![](Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees_images/Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees.pdf-0017-04.png)


Fig. 10. A window from an iD trace of the CARLA dataset: driving in the clear daytime weather. 

LEC is trained on sensory readings collected with force-sensitive resistors attached to the subject’s body for classifying the GAIT from a young or an elderly person. With the training data collected from healthy participants (without any injuries or diseases), input from patients with neurogenerative diseases are OODs for this LEC. We show that CODiT can be used to detect these temporal OOD windows in non-vision domain. 

We also perform parameter analysis for CODiT on the drift dataset. 

_6.1.1 Weather OODs in AEBS with Perception LEC._ **System Description.** The closed-loop of **advanced emergency braking system (AEBS)** with perception LEC is shown in Figure 8. The perception LEC is used to estimate distance to the front obstacle from the ego vehicle. This distance is fed to the emergency braking controller that issues braking commands to the vehicle for stopping at a safe distance from the front obstacle. The LEC is trained on images captured by the front camera on the vehicle in clear daytime weather. This closed-loop system is simulated in CARLA [9], an open-source simulator for autonomous driving research. For more details about this system, please refer to Reference [46]. 

**In-distribution Data.** We generate 33 driving traces of varying lengths in clear day weather as the iD training traces for the AEBS in CARLA. We randomly split these into 20 traces of the proper training set _Xtr_ and 13 traces of the calibration set _Xcal_ . Windows from _Xtr_ are sampled for training the perception LEC. Windows from _Xcal_ are sampled _n_ = 20 times (with one window from each calibration trace at a time to make each window in the set independent) for calculating the 20 sets of calibration non-conformity scores. We generate another set of 27 traces of varying lengths in clear weather as the iD test traces. 

**OOD Data.** Weather (rainy, foggy, and snowy) and night time OOD traces are generated by using the automold software [36] on the 27 iD test traces. OOD traces start from iD and gradually become OOD, i.e., the intensity of rain, fog, snow, or low brightness (for night) starts increasing gradually turning into the OOD traces. 

Examples of windows from these iD and rainy, foggy, snowy, and night OOD traces are shown in Figures 10, 11, 12, 13, 14, respectively. 

**Implementation Details of Algorithm 1.** We train a VAE model _M_ with the R3D network architecture [43] on the windows of length _w_ = 16 from _Xtr_ . R3D network is the 3D CNN with 

ACM Trans. Cyber-Phys. Syst., Vol. 8, No. 4, Article 46. Publication date: October 2024. 

R. Kaur et al. 

46:18 


![](Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees_images/Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees.pdf-0018-02.png)


Fig. 11. An OOD window from the rainy trace. The intensity of rain gradually increases in these OOD traces. 


![](Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees_images/Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees.pdf-0018-04.png)


Fig. 12. An OOD window from the foggy trace. The intensity of fog gradually increases in these OOD traces. 


![](Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees_images/Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees.pdf-0018-06.png)


Fig. 13. An OOD window from the snowy trace. The intensity of snow gradually increases in these OOD traces. 


![](Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees_images/Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees.pdf-0018-08.png)


Fig. 14. An OOD window from the night trace. The intensity of brightness gradually decreases in these OOD traces. 

residual connections and thus can be used on the 3D time-series input data. We use _GT_ = { _2x Speed, Shuffle, Periodic, Reverse, Identity_ } and train _M_ to predict the applied transformation _д_ ∈ _GT_ with a cross-entropy loss between the applied and the predicted transformations. The value of the CrossEntropyLoss( _д_ , _M_ ( _д_ ( _Xt_ , _w_ ))) is used as the non-conformity score _α_ for computing _p_ -value of an input _Xt_ , _w_ . 

**Results.** The ground truth of a window from an iD trace is iD and the ground truth of a window from an OOD trace is OOD. We report OOD detection results on the sliding windows ( _w_ = 16) of the test iD and OOD traces. We report AUROC, and the detection delay (with detection threshold _ϵ_ at 95% True Positive Rate) in Table 2. Starting from the first ground truth OOD window in a trace, the time (in seconds) required to detect the first OOD window in the trace is used as the detection delay. This number is averaged over the total number of OOD traces and reported in the Table. A lower detection delay is desired for real-time deployment of the detector. “NA” in the table means that the approach could not detect any OOD window with detection threshold at 95% TPR. 

For CODiT, we report mean and variance from five runs with random sampling of calibration windows from the calibration traces. For AUROC, CODiT outperforms other approaches, except for Snowy OOD windows, where our results are comparable with the best results by the memory detector. For detection delay, while we outperform other approaches on Foggy and Night OOD windows, our results on Rainy and Snowy OOD windows are comparable with the best results. 

_6.1.2 Temporal OODs in Driving Scenario._ We compare CODiT’s performance with the current non-point-based SOTA OOD detector, i.e., Feng et al. [10]’s on the replay and drift datasets as temporal OOD windows for perception LEC: 

ACM Trans. Cyber-Phys. Syst., Vol. 8, No. 4, Article 46. Publication date: October 2024. 

OOD Detection in Dependent Time-Series Data for CPS with Conformal Guarantees 

46:19 

Table 2. Comparison of CODiT with the Point-based Detectors 

|OOD|||AUROC|(↑)|||Detecti|on Delayi|n Second|s(↓)|
|---|---|---|---|---|---|---|---|---|---|---|
||VAE|_β_−VAE|Memory|Feng’s|CODiT|VAE|_β_−VAE|Memory|Feng’s|CODiT|
|Rainy|53.56|92.07|97.56|84.21|**99.68**±**0.00**|NA|0.92|**0.80**|5.06|0.86±0.00|
|Foggy|52.02|41.02|85.33|86.09|**99.70**±**0.00**|27.24|16.52|5.15|5.10|**0.84**±**0.00**|
|Snowy|53.23|97.52|**97.56**|95.91|97.00±0.05|NA|1.06|**0.80**|**0.80**|0.89±0.01|
|Night|50.86|95.57|94.70|75.07|**98.69**±**0.03**|59.04|4.06|5.72|69.12|**2.17**±**0.14**|



Cai et al.’s (VAE), Ramakrishna et al.’s ( _β_ –VAE), Yang et al.’s (Memory), and the non-point based detector by Feng et al. on weather and night OOD windows from the CARLA dataset in AEBS. 

**Replay Dataset.** Replay traces are generated from the 27 iD test traces in CARLA for AEBS by randomly sampling a position in each trace. All images from the sampled position in the trace are replaced with the image at the sampled position in the original trace. Again, results are reported for _n_ = 20, and on the sliding windows of replay OOD windows. 

**Drift Dataset.** We split 72 iD video traces of cars driving straight without any drift from the drift dataset [33] into 24 for _Xtr_ , 14 for _Xcal_ , and 34 for test iD traces. Windows from _Xtr_ are sampled for training the VAE. Windows from _Xcal_ are sampled _n_ = 20 times (with one window from each calibration trace at a time to make each window in the set independent) for calculating the 20 sets of calibration non-conformity scores. Again, the ground truth of a window from an iD trace is iD and the ground truth of a window from an OOD trace is OOD. We report results on the sliding windows of 34 iD test and 100 OOD drift traces. 

**Results.** We use the same VAE model’s architecture, _GT_ , and non-conformity score as described in Section 6.1.1. Figure 15 (left) compares the ROC, AUROC, and TNR (@95% TPR) results of CODiT with Feng et al.’s detector on the replay and drift OOD windows. We achieve SOTA results on both temporal OOD windows for perception LEC. 

**Parameter Analysis on drift.** We perform the following parameter analysis on the drift dataset: All VAE models used in these studies are trained on the proper training set of the drift dataset with the same model architecture, _GT_ , and non-conformity score from Section 6.1.1. 

(1) **Performance of CODiT with Different Window Lengths** _w_ **:** We train two VAE models with _w_ = 18, 20 and compare the performance of CODiT ( _n_ = 20) with Feng et al.’s detector on these window lengths. Figure 15 (right) shows that with both _w_ = 18 and 20, CODiT performs consistently well. 

(2) **Performance of CODiT with Different** |GT| **:** We compare the performance of CODiT with different sizes of the transformation set. Table 3 shows that the performance of CODiT ( _n_ = 5) increases with | _GT_ |. 

(3) **Using Deviation from iD** _GT_ **-equivariance as NCM:** With _GT_ = {2x _speed_ , _shuf f le_ , _reverse_ , _periodic_ , _identity_ }, and for all ground truth temporal transformations in _GT_ , Figure 5 shows that the non-conformity score from the TTPE-NCM is much higher for OOD windows than the test iD windows. This justifies our hypothesis that _GT_ -equivariance learned by a model on windows drawn from training distribution is not likely to generalize on windows drawn from OOD. 

(4) **CODiT’s Performance Increases with** _n_ **:** We train three VAE models with _GT_ equal to _{_ 2 _x speed, reverse, identity}_ , _{_ 2 _x speed, shuffle, periodic, identity}_ , and _{_ 2 _x speed, reverse, shuffle, periodic, identity}_ . Results on AUROC and detection rate in Figure 6 shows that the performance of CODiT improves with the number _n_ of _p_ -values used for detection in all the three cases (| _GT_ | = 3, 4, and 5). This justifies our hypothesis that under one transformation an OOD window might behave as a transformed iD window but the likelihood of that decreases with the number of transformations. (5) **Bounded FDR:** With _ϵ_ = 0.05 . _k_ , _k_ = 1, . . . , 10, Figure 6 (right) shows that the false alarm rate of CODiT ( _n_ = 5) is empirically calibrated with _ϵ_ (on average) for the VAE model with | _GT_ | = 5 as 

ACM Trans. Cyber-Phys. Syst., Vol. 8, No. 4, Article 46. Publication date: October 2024. 

R. Kaur et al. 

46:20 


![](Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees_images/Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees.pdf-0020-02.png)


Fig. 15. CODiT outperforms SOTA detector by Feng et al. [10] on temporal OOD windows in driving scenarios with the window length _w_ = 16 (left). CODiT performs consistently well with different window lengths of _w_ = 18, and 20 on drift dataset (right). 

Table 3. Performance of CODiT Increases with the Size of the Transformation Set _GT_ 

||_GT_||Transformations|AUROC|
|---|---|---|
||Speed,Identity,Shufe|84.78|
|3|Reverse,Shufe,Identity|85.47|
||Speed,Reverse,Identity|87.67|
||Speed,Shufe,Periodic,Identity|88.08|
|4|Speed,Identity,Shufe,Reverse|88.76|
||Speed,Reverse,Periodic,Identity|89.56|
|5|Speed,Shufe,Reverse,Periodic,Identity|90.78|



described above. The details of these box-plots are as follows: We increase the number of calibration windows to empirically check the false alarm rate (FDR) with respect to _ϵ_ . We increase the number of calibration traces from 14 to 34 and include all sliding windows on all the calibration traces in the calibration set. This gives us a calibration set with a larger number of approximately 862 calibration windows. Thirty-four calibration traces are randomly selected from the set of 48 in-distribution traces and the rest 14 are used as test traces. This is repeated 5 times and the generated box-plot of CODiT ( _n_ = 5) for | _GT_ | = 5 is shown in Figure 6 (right) of the article. For all the values of _ϵ_ = 0.05. _k_ , _k_ = 1, . . . , 10 in the plot, the average FDR is better aligned with _ϵ_ . 

_6.1.3 Temporal OODs in Medical CPS._ **System Description.** Walking pattern (or GAIT) analysis data is collected from healthy (young and elderly) subjects walking on treadmill with **forcesensitive resistors (FSR)** attached to their bodies. As shown in Figure 9, this data from the FSR is used to train a LEC to classify GAIT of a young or a elderly person [3]. 

**Dataset.** GAIT dataset [15] consists of records (or traces) on 16 healthy subjects. We split these into 6 for _Xtr_ , 5 for _Xcal_ , and 5 for test iD records. We use 27 records from the severe patient group with neurodegenerative diseases as OOD records. These 27 records contain 9 records from patients of the three diseases: **Amyotrophic Lateral Sclerosis (ALS), Parkinson’s (PD)** , and **Huntington’s disease (HD)** . 

**Implementation Details of Algorithm 1.** We use the 1D derived time-series features from the dataset (the .ts files) to train a VAE model with the Lenet5 architecture [30] on windows sampled from _Xtr_ . Lenet5 uses 2D CNN that can be used on the time-series data of 1D feature space. We use _GT_ = {high-pass filter, high-low filter, low-high filter, identity}. By high-low (or low-high) filter, we mean that we apply high (or low)-pass filter to the first half features and low 

ACM Trans. Cyber-Phys. Syst., Vol. 8, No. 4, Article 46. Publication date: October 2024. 

OOD Detection in Dependent Time-Series Data for CPS with Conformal Guarantees 

46:21 

Table 4. AUROC for Baseline(BL)/CODiT for OOD Detection on GAIT Dataset with Different Window Lengths _w_ 

|OOD||_w_ =16||_w_ =18||_w_ =20|
|---|---|---|---|---|---|---|
||BL|CODiT|BL|CODiT|BL|CODiT|
|ALS|**78.25**|67.27±0.63|77.73|**79.54**±**0.00**|77.99|**80.65**±**0.00**|
|PD|74.11|**85.33**±**0.20**|74.18|**84.18**±**0.01**|74.52|**84.12**±**0.02**|
|HD|76.97|**93.72**±**0.13**|76.64|**95.59**±**0.01**|76.68|**93.52**±**0.02**|
|ALL|76.23|**83.71**±**0.41**|75.99|**87.01**±**0.03**|76.21|**86.57**±**0.01**|



Higher AUROC indicates better performance. 

(or high)-pass filter to the last half features of the dataset. Again, we use the value of the cross entropy-loss between the applied and predicted transformations as the non-conformity score. 

**Baseline and Results.** Since Feng et al.’s approach is not applicable for detection on non-vision datasets, we generate a non-point baseline for comparing CODiT’s results. We train a one-class SVM on the auto-correlated features in the time dimension of all the sliding windows in _Xtr_ as the baseline. The ground truth of a window from an iD record is iD and the ground truth of a window from an OOD record is OOD. We report results on the sliding windows of the test iD and OOD records. Again, for CODiT, we report mean and variance from five runs with a random sampling of calibration windows from the calibration traces. Table 4 compares the AUROC performance of CODiT ( _n_ = 100) with **baseline (BL)** on individual and all (ALS, PD, and HD) OOD windows with different sliding window lengths _w_ (16, 18, and 20). As can be seen, CODiT consistently performs well. 

## **6.2 Results for OOD Detection on Variable-length Traces of Time-series Data by CODiT-v (Algorithm 2)** 

**Case Studies:** Here, we consider the same case studies as we performed for experiments for OOD detection on the fixed-length windows: 

- (1) Weather and night OODs in AEBS with perception LEC 

- (2) Temporal OODs (drift and replay) in driving scenarios 

- (3) Temporal OODs in medical CPS for GAIT analysis 

**Merging Functions:** We compare the performance of the four merging functions: **Harmonic Mean (HM), Arithmetic Mean (AM), Geometric Mean (GM)** , and **Bonferroni Method (BM)** in CODiT-v for OOD detection on variable-length time-series traces. 

**Baseline:** As a baseline, we run CODiT (Algorithm 1) from Section 6.1 on sliding windows of the input traces. A trace is labeled as OOD on the detection of an OOD window in the trace. Specifically, if the minimum Fisher _p_ -value of the sliding windows in the trace is below the detection threshold, then the trace is detected as OOD. 

The details and experimental results on OOD detection on variable length traces for the three case studies are as follows: 

_6.2.1 Weather and Night OODs in AEBS with Perception LEC._ We consider the same settings as described in Section 6.1.1. Here, we are interested in OOD detection of the input traces instead of the detection on sliding OOD windows in these traces. 

**Results:** The AUROC results with the sliding window length _w_ = 16 and _n_ = 5 for both the BL and CODiT-v are reported in Table 5. We report the mean and variance from five runs with a random sampling of calibration windows from the calibration traces for calculating the Fisher _p_ -value of the sliding windows in a trace. The performance of the four merging functions is 

ACM Trans. Cyber-Phys. Syst., Vol. 8, No. 4, Article 46. Publication date: October 2024. 

R. Kaur et al. 

46:22 

Table 5. AUROC Results of Baseline(BL)/CODiT-v with HM, AM, GM, and BM as Merging Functions for OOD Detection on Variable-length Traces for AEBS with Perception LEC 

|OOD|BL|HM|AM|GM|BM|
|---|---|---|---|---|---|
|Rainy|99.77±0.26|99.92±0.11|**99.98**±**0.02**|99.96±0.07|99.76±0.26|
|Foggy|99.27±0.98|99.65±0.58|**99.95**±**0.07**|99.90±0.17|99.27±0.99|
|Snowy|99.51±0.53|99.80±0.32|99.95±0.04|**99.98**±**0.04**|99.52±0.52|
|Night|96.99±3.52|98.16±2.73|**98.89**±**1.28**|98.85±1.64|97.00±3.52|



Higher AUROC indicates better performance 


![](Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees_images/Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees.pdf-0022-05.png)


Fig. 16. TNR (@ 95 TPR) results on weather and night OOD traces for AEBS with Perception LEC. 

comparable for all but night OOD traces, where AM performs the best. The performance of the baseline is comparable to BM in all the cases. 

We also plot the mean TNR (@95% TPR). These results are reported in Figure 16. Similar to AUROC results, the performance of the baseline is comparable with BM in all the cases. AM performs best in the detection of rainy and foggy OOD traces, and GM performs the best in the detection of foggy (same performance as AM), snowy, and night OOD traces. 

_6.2.2 Temporal OODs in Driving Scenario._ We consider the same settings as described in Section 6.1.2 for detection of replay and drift traces as temporal OOD traces for perception LEC. Here, we are interested in OOD detection of the input traces instead of the detection on sliding windows in these traces. 

**Results:** The AUROC results with the sliding window length _w_ = 16 and _n_ = 5 for both the BL and CODiT-v are reported in Table 6. Again, we report the mean and variance from five runs with - a random sampling of calibration windows from the calibration traces for calculating the Fisher _p_ value of the sliding windows in a trace. With comparable performance to BM, the baseline performs 

ACM Trans. Cyber-Phys. Syst., Vol. 8, No. 4, Article 46. Publication date: October 2024. 

OOD Detection in Dependent Time-Series Data for CPS with Conformal Guarantees 

46:23 

Table 6. AUROC Results of Baseline(BL)/CODiT-v with HM, AM, GM, and BM as Merging Functions for OOD Detection on Variable-length Traces for Temporal OODs in Driving Scenarios 

|OOD|BL|HM|AM|GM|BM|
|---|---|---|---|---|---|
|Drift|**97.74**±**0.69**|96.24±0.39|93.83±0.24|95.13±0.34|97.12±0.60|
|Replay|99.63±0.74|**100.0**±**0.0**|**100.0**±**0.0**|**100.0**±**0.0**|99.62±0.74|



Higher AUROC indicates better performance 


![](Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees_images/Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees.pdf-0023-05.png)


Fig. 17. The performance of CODiT-v increases with the accuracy of the AVT model in predicting the applied temporal transformation. 

the best in the detection of OOD traces from the drift dataset. The other three merging functions, namely, HM, AM, and GM, perform the best in the detection of OOD traces from the replay dataset. 

**Ablation on Drift:** We also perform an ablation study on the drift dataset. We test the performance of CODiT-v with AVT models of varying accuracy in predicting the applied transformation on a validation set. Figure 17 shows that the performance of CODiT-v (generally) increases with the accuracy of the underlying model for all the four merging functions. 

**Box-plots on False Alarm Rate:** We also report the box-plots on false alarm rate (FDR) with respect to the detection threshold _ϵ_ by CODiT-v on the drift dataset. Similar to the settings of the box-plot in Figure 6 by CODiT, these plots are also generated with a random sampling of calibration and test iD traces five times. With _ϵ_ = 0.05 . _k_ , _k_ = 1, . . . , 10, Figure 18 shows these results with the four merging functions: HM, AM, GM, and BM. For AM and GM, the FDR is always below _ϵ_ , on average. For the other two merging functions (HM and BM), the FDR is less than or equal to _ϵ_ , on average, for most values of _ϵ_ . 

_6.2.3 Temporal OODs in Medical CPS._ We consider the same settings as described in Section 6.1.3 for the detection of temporal OOD records (or traces) in medical CPS for GAIT analysis. Here, we are interested in OOD detection of the input records instead of the detection on sliding windows in these records. 

**Results:** The AUROC results with the sliding window length _w_ = 16, 18, 20 and _n_ = 5 for both the BL and CODiT-v on individual and all (ALS, PD, HD) OOD records are reported in Table 7. Similar to the results in the previous two case studies, the performance of the baseline is comparable to the performance of BM in all the test cases. The best results on different test cases are from different merging functions. 

_6.2.4 Discussion on Experimental Results._ **(1) The performance of baseline (BL) is comparable to CODiT-v with BM as the merging function:** This is expected, because similar to BM (5), the baseline uses the minimum Fisher _p_ -value of the sliding windows in the trace for OOD 

ACM Trans. Cyber-Phys. Syst., Vol. 8, No. 4, Article 46. Publication date: October 2024. 

R. Kaur et al. 

46:24 


![](Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees_images/Out-of-distribution_Detection_in_Dependent_Data_forCyber-physical_Systems_with_Conformal_Guarantees.pdf-0024-02.png)


Fig. 18. Box-plots on False Alarm Rate (FDR) vs. detection threshold _ϵ_ by different merging functions (HM, AM, GM, BM) in CODiT-v for OOD detection on the variable-length traces from the drift dataset. The yellow line in the box plot indicates the median. 

Table 7. AUROC Results of Baseline(BL)/CODiT-v with HM, AM, GM, and BM as Merging Functions for OOD Detection on Variable-length Traces for Medical CPS with Different Window Lengths ( _w_ = 16, 18, 20) 

|OOD|||_w_ =16|||||_w_ =18|||||_w_ =20|||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||BL|HM|AM|GM|BM|BL|HM|AM|GM|BM|BL|HM|AM|GM|BM|
|ALS|68.15|71.46|71.65|**72.41**|68.15|**84.72**|84.31|82.64|83.33|**84.72**|76.26|79.76|**81.99**|81.25|76.26|
|PD|75.86|79.85|79.05|**80.37**|75.86|84.36|83.61|80.25|82.25|**84.37**|81.39|85.02|85.02|**86.11**|81.40|
|HD|86.20|**88.53**|88.39|88.39|86.21|95.20|**96.22**|94.77|95.74|95.20|90.31|93.46|92.91|**93.47**|90.32|
|ALL|76.61|79.99|**80.47**|80.37|76.62|86.15|**87.22**|86.20|87.04|86.15|82.35|84.89|84.38|**85.09**|82.36|



Higher AUROC indicates better performance 

detection on the input trace. Unlike the false alarm rate guarantees on the input traces by CODiT-v, the baseline, however, does not provide these guarantees on the variable-length traces. The baseline or CODiT’s guarantees are for the bounded false detection on the fixed-length windows. 

**(2) Best results on different test cases are by different merging functions:** The performance of different merging functions depends upon the dependence of the _p_ -values combined by the merging function [45]. According to Vovk and Wang, if there is a substantial dependence, then **Harmonic Mean (HM)** should be preferred over the **Bonferroni Method (BM)** . For even stronger dependence, **Arithmetic Mean (AM)** or **Geometric Mean (GM)** might be a better option. But how to check the dependence among the _p_ -values is still an open question, as looking into the data would violate the validity under heavy dependence. 

## **7 CONCLUSION AND DISCUSSION** 

We propose to use time-dependency between the datapoints in a time-series window for OOD detection on the window. Specifically, we propose using deviation from the temporal equivariance learned by a model on windows drawn from the training distribution of LEC as an NCM in the conformal prediction framework for OOD detection in time-series data for CPS. Computing 

ACM Trans. Cyber-Phys. Syst., Vol. 8, No. 4, Article 46. Publication date: October 2024. 

OOD Detection in Dependent Time-Series Data for CPS with Conformal Guarantees 

46:25 

independent predictions from multiple conformal detectors from the proposed measure and combining these predictions by Fisher’s method leads to the proposed detector CODiT for OOD detection on fixed-length time-series windows with guarantees on false alarms. We illustrate the efficacy of CODiT by achieving SOTA results in autonomous driving and GAIT analysis in medical CPS. 

The time complexity analysis of CODiT is as follows: At inference time, ICAD computes the non-conformity score of an input and compares it with the scores of the pre-computed (in offline settings) calibration datapoints for anomaly detection. The time complexity of ICAD is, therefore, O (non-conformity score computation of the input+|calibration set|). Non-conformity score computation in our case is the output generation (i.e., prediction of the applied transformation) by the VAE model. We found it to be approximately 3 milliseconds in our experiments. The time complexity of ICAD is for calculating one _p_ -value of the input. CODiT uses multiple ( _n_ ) _p_ -values and combines them using Fisher’s method for OOD detection. So, the time-complexity of CODiT = _n_ × time-complexity of the ICAD framework, where _n_ is the number of _p_ -values. Therefore, the time complexity of CODiT increases linearly with the number _n_ of _p_ -values used for detection. As seen from Figure 6, the detection performance of CODiT improves with _n_ . So, it is a tradeoff between time complexity and detection performance. We also observe that the performance of CODiT improves with the number of transformations in the set of temporal transformations. So, using all (instead of choosing a subset) of temporal transformations suitable for the application works better for CODiT. As a future work, we plan to explore the performance of CODiT with non-temporal transformations on the windows of time-series datapoints, as these windows capture the temporal aspect of the input data. 

In addition to CODiT: OOD detection algorithm on fixed-length time-series window, we further propose CODiT-v: an algorithm for OOD detection on variable-length traces with bounded false alarm rate guarantees. CODiT-v uses CODiT to compute Fisher _p_ -values of the sliding windows in the trace and combines these values by using valid merging functions defined for combining dependent _p_ -values. Instead of the merging functions, one could also use Fisher’s method to combine the _p_ -values of the sliding windows generated by CODiT for detection on the trace. With dependent time-series data in the sliding windows, however, the independence assumption required by Fisher’s method for false detection rate guarantees gets violated. The time complexity of CODiT-v is _m_ × the complexity of CODiT: _m_ × ( _n_ × time-complexity of ICAD), where _m_ is the number of sliding windows in the input trace, and _n_ is the number of _p_ -values used for computing Fisher’s _p_ -value on a sliding window. _n_ is equal to 5 in all the test cases for CODiT-v. For CODiT, _n_ = 20 in the autonomous driving system case study and _n_ = 100 in the medical CPS case study. We observe that the AUROC performance of CODiT-v is comparable or even better (except for a few cases in GAIT analysis) to the performance of CODiT with this smaller value of _n_ = 5. So, although the time complexity of CODiT-v increases with the number ( _m_ ) of sliding windows in the trace, it performs reasonably well even with a smaller number of _n_ in comparison to CODiT. We report the performance of CODiT-v with all four merging functions and observe that the best results on different test cases are by different merging functions. The choice of the merging function depends on the dependence structure between the _p_ -values combined by the function. Figuring out the dependence structure among the _p_ -values is still an open question, and we plan to explore it in our future work. 

## **ACKNOWLEDGEMENT** 

The views and conclusions contained in this document are those of the authors and should not be interpreted as representing the official policies, either expressed or implied, of the Army Research Office or the U.S. Government. 

ACM Trans. Cyber-Phys. Syst., Vol. 8, No. 4, Article 46. Publication date: October 2024. 

R. Kaur et al. 

46:26 

## **REFERENCES** 

- [1] Vineeth Balasubramanian, Shen-Shyang Ho, and Vladimir Vovk. 2014. _Conformal Prediction for Reliable Machine Learning: Theory, Adaptations and Applications_ . Newnes. 

- [2] Michele Basseville and Igor V. Nikiforov. 1993. _Detection of Abrupt Changes: Theory and Application_ . Vol. 104. Prentice Hall, Englewood Cliffs, NJ. 

- [3] Rezaul Begg and Joarder Kamruzzaman. 2006. Neural networks for detection and classification of walking pattern changes due to ageing. _Australas. Phys. Eng. Sci. Medic._ 29, 2 (2006), 188–195. 

- [4] Mariusz Bojarski, Davide Del Testa, Daniel Dworakowski, Bernhard Firner, Beat Flepp, Prasoon Goyal, Lawrence D. Jackel, Mathew Monfort, Urs Muller, Jiakai Zhang, Xin Zhang, and Jake Zhao. 2016. End to end learning for self-driving cars. _arXiv preprint arXiv:1604.07316_ (2016). 

- [5] Feiyang Cai and Xenofon Koutsoukos. 2020. Real-time out-of-distribution detection in learning-enabled cyberphysical systems. In _ACM/IEEE 11th International Conference on Cyber-Physical Systems (ICCPS’20)_ . IEEE, 174–183. 

- [6] Evangelos Chatzipantazis, Stefanos Pertigkiozoglou, Kostas Daniilidis, and Edgar Dobriban. 2021. Learning augmentation distributions using transformed risk minimization. _arXiv preprint arXiv:2111.08190_ (2021). 

- [7] Shuxiao Chen, Edgar Dobriban, and Jane H. Lee. 2020. A group-theoretic framework for data augmentation. _J. Mach. Learn. Res._ 21, 245 (2020), 1–71. 

- [8] Jeffrey De Fauw, Joseph R Ledsam, Bernardino Romera-Paredes, Stanislav Nikolov, Nenad Tomasev, Sam Blackwell, Harry Askham, Xavier Glorot, Brendan O’Donoghue, Daniel Visentin, George van den Driessche, Balaji Lakshminarayanan, Clemens Meyer, Faith Mackinder, Simon Bouton, Kareem Ayoub, Reena Chopra, Dominic King, Alan Karthikesalingam, Cían O Hughes, Rosalind Raine, Julian Hughes, Dawn A Sim, Catherine Egan, Adnan Tufail, Hugh Montgomery, Demis Hassabis, Geraint Rees, Trevor Back, Peng T. Khaw, Mustafa Suleyman, Julien Cornebise, Pearse A. Keane, and Olaf Ronneberger. 2018. Clinically applicable deep learning for diagnosis and referral in retinal disease. _Nat. Medic._ 24, 9 (2018), 1342–1350. 

- [9] Alexey Dosovitskiy, German Ros, Felipe Codevilla, Antonio Lopez, and Vladlen Koltun. 2017. CARLA: An open urban driving simulator. In _Conference on Robot learning_ . PMLR, 1–16. 

- [10] Yeli Feng, Daniel Jun Xian Ng, and Arvind Easwaran. 2021. Improving variational autoencoder based out-ofdistribution detection for embedded real-time applications. _ACM Trans. Embed. Comput. Syst._ 20, 5s (2021), 1–26. 

- [11] R. A. Fisher. 1932. _Statistical Methods for Research Workers._ (4th ed.) Oliver & Boyd. 

- [12] Jingkun Gao, Xiaomin Song, Qingsong Wen, Pichao Wang, Liang Sun, and Huan Xu. 2020. RobustTAD: Robust time series anomaly detection via decomposition and convolutional neural networks. _arXiv preprint arXiv:2002.09545_ (2020). 

- [13] Georgia Gkioxari, Ross Girshick, and Jitendra Malik. 2015. Contextual action recognition with R*CNN. In _IEEE International Conference on Computer Vision_ . 1080–1088. 

- [14] Matan Haroush, Tzviel Frostig, Ruth Heller, and Daniel Soudry. 2021. A statistical framework for efficient out of distribution detection in deep neural networks. In _International Conference on Learning Representations_ . 

- [15] Jeffrey M. Hausdorff, Apinya Lertratanakul, Merit E. Cudkowicz, Amie L. Peterson, David Kaliton, and Ary L. Goldberger. 2000. Dynamic markers of altered gait rhythm in amyotrophic lateral sclerosis. _J. Appl. Physiol_ . 88 (2000), 2045–2053. 

- [16] Dan Hendrycks and Kevin Gimpel. 2017. A baseline for detecting misclassified and out-of-distribution examples in neural networks. In _International Conference on Learning Representations_ . 

- [17] Simon Jenni and Hailin Jin. 2021. Time-equivariant contrastive video representation learning. In _IEEE/CVF International Conference on Computer Vision_ . 9970–9980. 

- [18] Xiayan Ji, Hyonyoung Choi, Oleg Sokolsky, and Insup Lee. 2023. Incremental anomaly detection with guarantee in the internet of medical things. In _8th ACM/IEEE Conference on Internet of Things Design and Implementation_ . 327–339. 

- [19] Xiayan Ji, Xian Li, Ahhyun Yuh, Amanda Watson, Claire Kendell, James Weimer, Hajime Nagahara, Teruo Higashino, Teruhiro Mizumoto, Viktor Erdélyi, George Demiris, Oleg Sokolsky, and Insup Lee. 2023. Short: Integrated sensing platform for detecting social isolation and loneliness in the elderly community. In _IEEE/ACM Conference on Connected Health: Applications, Systems and Engineering Technologies (CHASE’23)_ . IEEE, 148–152. 

- [20] Yiannis Kantaros, Taylor Carpenter, Kaustubh Sridhar, Yahan Yang, Insup Lee, and James Weimer. 2021. Real-time detectors for digital and physical adversarial inputs to perception systems. In _ACM/IEEE 12th International Conference on Cyber-Physical Systems (ICCPS’21)_ . 67–76. 

- [21] Ramneet Kaur, Radoslav Ivanov, Matthew Cleaveland, Oleg Sokolsky, and Insup Lee. 2020. Assurance case patterns for cyber-physical systems with deep neural networks. In _International Conference on Computer Safety, Reliability, and Security_ . Springer, 82–97. 

- [22] Ramneet Kaur, Susmit Jha, Anirban Roy, Sangdon Park, Edgar Dobriban, Oleg Sokolsky, and Insup Lee. 2022. iDECODe: In-distribution Equivariance for Conformal Out-of-distribution Detection, Association for the Advancement of Artificial Intelligence. arXiv:2201.02331 [cs.LG] 

ACM Trans. Cyber-Phys. Syst., Vol. 8, No. 4, Article 46. Publication date: October 2024. 

OOD Detection in Dependent Time-Series Data for CPS with Conformal Guarantees 

46:27 

- [23] Ramneet Kaur, Susmit Jha, Anirban Roy, Sangdon Park, Oleg Sokolsky, and Insup Lee. 2021. Detecting oods as datapoints with high uncertainty. _arXiv preprint arXiv:2108.06380_ (2021). 

- [24] Ramneet Kaur, Susmit Jha, Anirban Roy, Oleg Sokolsky, and Insup Lee. 2021. Are all outliers alike? On understanding the diversity of outliers for detecting OODs. _arXiv preprint arXiv:2103.12628_ (2021). 

- [25] Ramneet Kaur, Susmit Jha, Anirban Roy, Oleg Sokolsky, and Insup Lee. 2023. Predicting out-of-distribution performance of deep neural networks using model conformance. In _IEEE International Conference on Assured Autonomy (ICAA’23)_ . IEEE, 19–28. 

- [26] Ramneet Kaur, Xiayan Ji, Souradeep Dutta, Michele Caprio, Yahan Yang, Elena Bernardis, Oleg Sokolsky, and Insup Lee. 2023. Using semantic information for defining and detecting OOD inputs. _arXiv preprint arXiv:2302.11019_ (2023). 

- [27] Ramneet Kaur, Yiannis Kantaros, Wenwen Si, James Weimer, and Insup Lee. 2023. Detection of adversarial physical attacks in time-series image data. _arXiv preprint arXiv:2304.13919_ (2023). 

- [28] Ramneet Kaur, Kaustubh Sridhar, Sangdon Park, Yahan Yang, Susmit Jha, Anirban Roy, Oleg Sokolsky, and Insup Lee. 2023. CODiT: Conformal out-of-distribution detection in time-series data for cyber-physical systems. In _ACM/IEEE 14th International Conference on Cyber-Physical Systems (with CPS-IoT Week’23)_ . 120–131. 

- [29] Rikard Laxhammar and Göran Falkman. 2015. Inductive conformal anomaly detection for sequential detection of anomalous sub-trajectories. _Ann. Math. Artif. Intell._ 74, 1 (2015), 67–94. 

- [30] Yann LeCun, Léon Bottou, Yoshua Bengio, and Patrick Haffner. 1998. Gradient-based learning applied to document recognition. _Proc. IEEE_ 86, 11 (1998), 2278–2324. 

- [31] Shuo Li, Xiayan Ji, Edgar Dobriban, Oleg Sokolsky, and Insup Lee. 2022. PAC-wrap: Semi-supervised PAC anomaly detection. In _28th ACM SIGKDD Conference on Knowledge Discovery and Data Mining_ . 945–955. 

- [32] Navonil Majumder, Soujanya Poria, Alexander Gelbukh, and Erik Cambria. 2017. Deep learning-based document modeling for personality detection from text. _IEEE Intelli. Syst._ 32, 2 (2017), 74–79. 

- [33] Alam Noor, Bilel Benjdira, Adel Ammar, and Anis Koubaa. 2020. DriftNet: Aggressive driving behavior classification using 3D EfficientNet architecture. _arXiv preprint arXiv:2004.11970_ (2020). 

- [34] Guo-Jun Qi, Liheng Zhang, Chang Wen Chen, and Qi Tian. 2019. AVT: Unsupervised learning of transformation equivariant representations by autoencoding variational transformations. In _IEEE International Conference on Computer Vision_ . 8130–8139. 

- [35] Shreyas Ramakrishna, Zahra Rahiminasab, Gabor Karsai, Arvind Easwaran, and Abhishek Dubey. 2021. Efficient outof-distribution detection using latent space of _β_ -VAE for cyber-physical systems. _arXiv preprint:2108.11800_ (2021). 

- [36] Ujjwal Saxena. 2018. Automold. Retrieved from https://github.com/UjjwalSaxena/Automold--Road-AugmentationLibrary 

- [37] Uwe Schmidt and Stefan Roth. 2012. Learning rotation-aware features: From invariant priors to equivariant descriptors. In _IEEE Conference on Computer Vision and Pattern Recognition_ . IEEE, 2050–2057. 

- [38] Kaustubh Sridhar, Souradeep Dutta, Ramneet Kaur, James Weimer, Oleg Sokolsky, and Insup Lee. 2022. Towards alternative techniques for improving adversarial robustness: Analysis of adversarial training at a spectrum of perturbations. _arXiv preprint arXiv:2206.06496_ (2022). 

- [39] Johannes Stallkamp, Marc Schlipsing, Jan Salmen, and Christian Igel. 2012. Man vs. computer: Benchmarking machine learning algorithms for traffic sign recognition. _Neural Netw._ 32 (2012), 323–332. 

- [40] Jihoon Tack, Sangwoo Mo, Jongheon Jeong, and Jinwoo Shin. 2020. CSI: Novelty detection via contrastive learning on distributionally shifted instances. _Adv. Neural Inf. Process. Syst._ 33 (2020). 

- [41] Ashish Tiwari, Bruno Dutertre, Dejan Jovanović, Thomas de Candia, Patrick D. Lincoln, John Rushby, Dorsa Sadigh, and Sanjit Seshia. 2014. Safety envelope for security. In _3rd International Conference on High Confidence Networked Systems_ . 85–94. 

- [42] Paolo Toccaceli and Alexander Gammerman. 2017. Combination of conformal predictors for classification. In _Conformal and Probabilistic Prediction and Applications_ . PMLR, 39–61. 

- [43] Du Tran, Heng Wang, Lorenzo Torresani, Jamie Ray, Yann LeCun, and Manohar Paluri. 2018. A closer look at spatiotemporal convolutions for action recognition. In _IEEE Conference on Computer Vision and Pattern Recognition_ . 6450– 6459. 

- [44] Vladimir Vovk, Ilia Nouretdinov, and Alexander Gammerman. 2003. Testing exchangeability on-line. In _20th International Conference on Machine Learning (ICML’03)_ . 768–775. 

- [45] Vladimir Vovk and Ruodu Wang. 2020. Combining p-values via averaging. _Biometrika_ 107, 4 (2020), 791–808. 

- [46] Yahan Yang, Ramneet Kaur, Souradeep Dutta, and Insup Lee. 2022. Interpretable detection of distribution shifts in learning enabled cyber-physical systems. In _ACM/IEEE International Conference on CyberPhysical Systems_ . 

Received 7 July 2023; revised 16 November 2023; accepted 24 January 2024 

ACM Trans. Cyber-Phys. Syst., Vol. 8, No. 4, Article 46. Publication date: October 2024. 

