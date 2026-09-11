IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE, VOL. 36, NO. 6, JUNE 2014 

1158 

# Online Learning and Sequential Anomaly Detection in Trajectories 

## Rikard Laxhammar and Göran Falkman, _Member, IEEE,_ 

**Abstract** —Detection of anomalous trajectories is an important problem in the surveillance domain. Various algorithms based on learning of normal trajectory patterns have been proposed for this problem. Yet, these algorithms typically suffer from one or more limitations: They are not designed for sequential analysis of incomplete trajectories or online learning based on an incrementally updated training set. Moreover, they typically involve tuning of many parameters, including ad-hoc anomaly thresholds, and may therefore suffer from overfitting and poorly-calibrated alarm rates. In this article, we propose and investigate the Sequential Hausdorff Nearest-Neighbor Conformal Anomaly Detector (SHNN-CAD) for online learning and sequential anomaly detection in trajectories. This is a parameter-light algorithm that offers a well-founded approach to the calibration of the anomaly threshold. The discords algorithm, originally proposed by Keogh _et al_ ., is another parameter-light anomaly detection algorithm that has previously been shown to have good classification performance on a wide range of time-series datasets, including trajectory data. We implement and investigate the performance of SHNN-CAD and the discords algorithm on four different labeled trajectory datasets. The results show that SHNN-CAD achieves competitive classification performance with minimum parameter tuning during unsupervised online learning and sequential anomaly detection in trajectories. 

**Index Terms** —Anomaly detection, trajectory data, online learning, conformal prediction 

## **1 INTRODUCTION** 

NOMALOUS behaviour may indicate important objects A and events in a wide variety of domains. One such domain is surveillance where there is a clear trend towards more and more advanced sensor systems producing huge amounts of geo-spatial _trajectory data_ from moving objects, such as people, vehicles, vessels and animals. In video surveillance of ground activities, for example, anomalous trajectories may be indicative of illegal and adverse activity related to personal assault, robbery, burglary, infrastructural sabotage etc. Timely detection of these relatively infrequent events, which is critical for enabling pro-active measures, requires careful analysis of all moving objects at all times; this is typically a great challenge to human analysts due to information overload, fatigue and inattention. Thus, there is a need for automated trajectory analysis. 

This article is concerned with algorithms for automated detection of anomalous trajectories. Various algorithms based on learning of normal trajectory patterns from historical data have previously been proposed for this problem [1]. However, these algorithms typically suffer from one or more limitations: They are primarily designed for offline anomaly detection in databases and do not support 

- _R. Laxhammar is with the Saab AB, Järfälla 175 41, Sweden. E-mail: rikard.laxhammar@saabgroup.com._ 

- _G. Falkman is with the University of Skövde, Skövde 541 28, Sweden. E-mail: goran.falkman@his.se._ 

_Manuscript received 14 Nov. 2012; revised 15 May 2013; accepted 22 Aug. 2013. Date of publication 12 Sep. 2013; date of current version 12 May 2014. Recommended for acceptance by F. Fleuret._ 

_For information on obtaining reprints of this article, please send e-mail to: reprints@ieee.org, and reference the Digital Object Identifier below. Digital Object Identifier 10.1109/TPAMI.2013.172_ 

_sequential anomaly detection_ in incomplete trajectories or _online learning_ based on an incrementally updated training set. Moreover, they typically involve tuning of many parameters, including ad-hoc anomaly thresholds, and may therefore suffer from overfitting and poorly-calibrated alarm rates. 

In our previous work [2], we introduced the _Conformal Anomaly Detector_ (CAD), which is a general algorithm for anomaly detection that is based on the framework of Conformal prediction [3]. The main idea of CAD is to estimate the _p_ -value for new data based on a specified _NonConformity Measure_ (NCM) [3]. Intuitively, the _p_ -value corresponds to the probability of observing data that appears to be at least as extreme as the data that was actually observed. If the _p_ -value is below a predefined anomaly threshold, the new data is considered very unlikely and, therefore, classified as anomalous. A key property of CAD is that it offers a well-founded approach to the tuning of the anomaly threshold that guarantees that the alarm rate will be wellcalibrated under relatively weak statistical assumptions. Apart from the anomaly threshold, the only design parameter of CAD is the specified NCM. We previously proposed a novel NCM based on the _Directed Hausdorff Distance_ (DHD) [4] for sequential conformal anomaly detection in trajectories [2]. The intuition of DHD is that it measures the degree to which an object resembles some _part_ of another object. This key property makes DHD well-suited for measuring the distance from an incomplete trajectory to other trajectories. 

### **1.1 Main Contributions** 

This article deepens and expands on our previous results [2]. In particular, we: 

Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on September 11,2026 at 17:32:55 UTC from IEEE Xplore.  Restrictions apply. 0162-8828 ⃝c 2013 IEEE. Personal use is permitted, but republication/redistribution requires IEEE permission. See http://www.ieee.org/publications_standards/publications/rights/index.html for more information. 

LAXHAMMAR AND FALKMAN: ONLINE LEARNING AND SEQUENTIAL ANOMALY DETECTION IN TRAJECTORIES 

1159 

- Present an extensive discussion of limitations of previous algorithms for anomaly detection in general and the detection of anomalous trajectories in particular. 

known as data point or object, either belongs to the _normal class_ or the _abnormal class_ . However, unlike traditional supervised classification, available training data is typically unlabelled or assumed to only include examples labelled normal [7] _._ That is, there are no labelled examples of the abnormal class available for training. When training data is labelled normal, anomaly detection algorithms typically focus on learning one-class classifiers [8], probability density functions [9] or other types of models, which are used for determining whether unlabelled test examples belong to the normal class or not; such approaches are referred to as _semi-supervised anomaly detection_ [7]. When training data is unlabelled, there is usually no distinction between training and test data; the training set is assumed to include a small minority of abnormal examples, which are discriminated from the normal examples by using unsupervised learning techniques, such as clustering. Such approaches may be refereed to as _unsupervised anomaly detection_ [7]. 

- Formalise CAD and the concepts of offline vs. online and unsupervised vs. semi-supervised conformal anomaly detection. This includes the statement and proof of a theorem regarding the property of wellcalibrated alarm rate of CAD. 

- Formalise the _Directed Hausdorff k-Nearest Neighbour Non-Conformity Measure_ (DH-kNN NCM). This includes the statement and proof of a theorem regarding the monotonicity of the _p_ -values during sequential update of an incomplete trajectory, which further implies that the alarm rate of CAD is wellcalibrated during sequential anomaly detection in incomplete trajectories. 

- Re-introduce our algorithm for sequential anomaly in trajectories [2] as the _Sequential Hausdorff Nearest Neighbour Conformal Anomaly Detector_ (SHNN-CAD). This includes a more detailed description of the algorithm, a discussion of its properties and implementation and an analysis of its time complexity. 

### **2.2 Detection of Anomalous Trajectories** 

A trajectory is modelled as a finite sequence of data points: 


![](Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories_images/Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories.pdf-0002-09.png)


- Extend the empirical investigation of DH-kNN NCM and SHNN-CAD by including new experiments on new trajectory datasets and comparing it with the discords approach [5]. 

where each _χi_ ∈ R<sup>_d_</sup> is a multi-dimensional feature vector at time point _ti_ and where the total length in time of the trajectory is _tL_ − _t_ 1 [1]. In the simple case, _χi_ ∈ R<sup>2</sup> represents an object’s (estimated) location in the two-dimensional spatial plane at time point _ti_ . Depending on the application, the feature space may be extended by, e.g., a third spatial dimension or the velocity. 

### **1.2 Outline** 

The outline of the article is as follows: First we introduce the problem of anomaly detection and present an overview of previous work related to detection of anomalous trajectories (Section 2). Next, we identify and discuss some general limitations of previously proposed algorithms (Section 3). In Section 4, we first present some key results of conformal prediction [3] that underpin CAD. This is followed by the formalisation of CAD and discussions of its properties and operating modes. In Section 5, we are concerned with the problem of sequential anomaly detection in trajectories: We first introduce DHD [4] before formalising DH-kNN NCM. In the remainder of the section, we present SHNN-CAD, discuss its properties and implementation and analyse its time complexity. In Section 6, we implement DH-kNN NCM and SHNN-CAD and evaluate their performance on four trajectory datasets. For comparative purposes, we also implement and evaluate performance of the discords algorithm [5], which has previously been proposed for detecting anomalous trajectories [6]. Future work and generalisations are discussed in Section 7. Finally, we conclude the article in Section 8. 

### _2.2.1 Clustering-Based Approaches_ 

A large amount of work related to anomaly detection in trajectories has been published in the video surveillance domain [1], [10], [11]. Most of these methods involve _trajectory clustering_ , where cluster models corresponding to normal paths are learnt from historical trajectories. This process typically consists of three steps that are sometimes mixed: preprocessing of raw trajectories, clustering of preprocessed trajectories and modelling of trajectory clusters [1]. New trajectories are then typically classified as normal or abnormal based on the distance to the closest cluster, or the likelihood of the most probable cluster. 

Two main techniques are used for preprocessing trajectories: _normalisation_ and _dimensionality reduction_ [1]. Normalisation techniques ensure that trajectories are of equal length, for example by extending short trajectories using zero padding [10] or by re-sampling trajectories. Dimensionality reduction techniques, such as vector quantisation, discrete Fourier transforms [12], parametrised spline models [13], wavelets, Hidden Markov Models (HMM) [14], principal component analysis and spectral methods [15], all map trajectories into a lower dimensional feature space that is computationally more manageable [1].1].]. 

## **2 BACKGROUND** 

### **2.1 Anomaly Detection** 

According to Chandola _et al_ . [7], “anomalies are patterns is computationally more manageable [1].1].]. in data that do not conform to a well-defined notion of All clustering algorithms require that an appropriate normal behaviour”. These patterns typically correspond to _similarity measure_ , also known as a distance measure, is new, rare, unknown or otherwise extreme behaviour and defined. Euclidian distance (ED) (e.g., [16]) is perhaps may therefore be of particular interest. From an application the simplest and most intuitive similarity measure. Other owners point of view, _anomaly detection_ may be considered similarity measures and modifications of ED have been as a binary classification problem where each _example_ , also proposed for relaxing alignment and length constraints, Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on September 11,2026 at 17:32:55 UTC from IEEE Xplore.  Restrictions apply. 

IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE, VOL. 36, NO. 6, JUNE 2014 

1160 

ability to automatically detect and remove anomalies in the training data. Yankov _et al_ . [6] proposed the application of _time-series discords_ [5] for detecting anomalous trajectories in a database. Assuming preprocessed trajectories of equal length, the _k_ th discord corresponds to the trajectory with the _k_ th largest ED to its nearest neighbour trajectory in the database. Owens and Hunter [22] proposed an algorithm based on a Self-Organising Map (SOM) that is appropriate for learning and sequential anomaly detection in trajectories. Each data point from a trajectory is represented by a fixed-length feature vector encompassing the current location, velocity and acceleration together with information on the recent position. Lee _et al_ . [23] proposed a _partition-and-detect_ framework for detection of anomalous sub-trajectories in a trajectory database. A twostep anomaly (outlier) detection algorithm is proposed, which first partitions each trajectory into a number of line segments. Next, anomalous trajectory partitions, i.e., line segments, are detected according to a combination of distance and density-based analysis. 

such as Dynamic Time Warping (DTW) [1] and Longest Common Sub-Sequence (LCSS) [17]. Different algorithms have been proposed for creating and updating trajectory clusters based on a specified similarity measure [1]. Once trajectories have been clustered, appropriate cluster models, sometimes referred to as _path models_ [1] or _motion patterns_ [10], are defined. Two main types of path models have been adopted: The first considers a complete path, from the starting point to the endpoint. The second decomposes a path into smaller atomic parts called _subpaths_ [1]. Complete path models are typically based on a _centroid_ representation of the cluster, which corresponds to the “average” trajectory [1]. The centroid is sometimes complemented by an _envelope_ , which captures the extension and variance of the trajectories [1]. Hu _et al_ . [10] model each path as a chain of Gaussian distributions. Morris and Trivedi [18] proposed the modelling of each path by a HMM, where each hidden state is modelled by a Gaussian mixture model. Subpath models can be further defined in terms of probabilistic connections [1]. An example of a subpath structure was proposed by Piciarelli [19], where each subpath is modelled as a node in a tree-like structure augmented with probabilities for node transitions. 

## **3 LIMITATIONS OF PREVIOUS ALGORITHMS** 

This section presents in more detail some of the main limitations of previous algorithms for anomalous trajectory detection, which motives the proposal of SHNN-CAD. In the first subsection, we discuss issues that are related to anomaly detection in general. The second subsection is more focused towards problems that are specific for the trajectory domain. 

For complete trajectories, anomaly detection is typically carried out by first determining the path model that best explains the new trajectory, i.e., having the maximum likelihood or minimal distance to the new trajectory. The distance or likelihood is then compared to an anomaly threshold. Some algorithms, but far from all, support _sequential,_ also known as _online_ [1] or _incremental_ [10], anomaly detection in _incomplete_ trajectories. Morris and Trivedi [18] proposed an algorithm that monitors the likelihood for the part of the trajectory that is within a sliding window of a fixed size. If this likelihood drops below a specified threshold, the trajectory is classified as anomalous. Hu _et al_ . [10] proposed an algorithm for sequential anomaly detection in incomplete trajectories. For each new data point, the algorithm first updates the most probable path model (motion pattern) given the part of the trajectory observed so far. The likelihood for the new point is then calculated relative the most probable path model and the point is classified as anomalous if its likelihood is below a specified threshold. If a series of points are classified as anomalous, the trajectory is classified as anomalous. Fu _et al_ . [20] proposed an algorithm that incrementally determines the Maximum A Posterior (MAP) path model (trajectory cluster) as more data points are observed from an incomplete trajectory. The incomplete trajectory is classified as anomalous if it leaves the envelope of the current MAP path model, or if the velocity of the trajectory deviates from the velocity of the MAP path model. 

### **3.1 Anomaly Detection in General** _3.1.1 Invalid Statistical Assumptions_ 

Parameterised statistical models, such as the Gaussian distribution, are attractive because parameter estimation is rather straightforward and because there exist statistical tests that provide well-founded confidence for anomaly detection [7]. However, accuracy of estimated models, and robustness of anomaly detection, depend on whether the structural assumptions are valid. For example, fitting a Gaussian model to data generated from an approximately uniform distribution will result in overestimation and underestimation of the probability density at the centre (mean) and at the tails of the distribution, respectively [24]. In case of underestimation, examples of the normal class will be assigned a lower likelihood and, hence, are more likely to be classified as abnormal. In case of overestimation, the sensitivity to abnormal examples will decrease as there is an increased risk that subtle anomalies will be erroneously classified as normal. In many real world applications, such as traffic surveillance, where behaviour is governed by social systems and structures rather than by physical laws, the Gaussian assumption may indeed be questioned (see [25]).25]).]). 

### _2.2.2 Non-Clustering-Based Approaches_ 

Other approaches to detecting anomalous trajectories have questioned (see [25]).25]).]). been proposed that do not involve clustering of trajectories as presented above (e.g., [21]). Piciarelli _et al_ . [16] _3.1.2 Parameter-Laden Algorithms_ proposed a trajectory learning and anomaly detection algoMost anomaly detection algorithms require careful preprorithm based on a one-class Support Vector Machine (SVM), cessing and setting of multiple application specific paramewhere each trajectory is represented by a fixed-dimensional ters and detection thresholds in order to achieve (near) optifeature vector of evenly sampled points from the raw tramal performance; trajectory anomaly detection is no excepjectory. One of the main novelties of this algorithm is its tion to this. In fact, Keogh _et al_ . [26] argue that most data Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on September 11,2026 at 17:32:55 UTC from IEEE Xplore.  Restrictions apply. 

LAXHAMMAR AND FALKMAN: ONLINE LEARNING AND SEQUENTIAL ANOMALY DETECTION IN TRAJECTORIES 

1161 

mining algorithms are more or less _parameter-laden_ , which is undesirable for several reasons. In an extensive empirical study, they showed that “in case of anomaly detection, parameter-laden algorithms are particularly vulnerable to overfitting” [26]. The risks of overfitting parameter-laden models in real world applications were also discussed by Hand [27], who showed empirically that “the marginal gain from complicated models is typically small compared to the predictive power of the simpler models”. According to Markou and Sing [28], “an [anomaly] detection method should aim to minimise the number of parameters that are user set”. Indeed, one may argue that use of few parameters suppresses bias towards particular types of anomalies and makes the method easier to implement for different applications. 

parameters are introduced at specific time points. For example, some authors discuss regular batch-learning repetitions using an updated training set [18]. However, it is not clear how to determine the appropriate time point for such an update. On the one hand, minimising the learning delay, i.e., the time between successive model updates, may be desirable in order to maintain a more timely and accurate model. But on the other hand, computational complexity of offline learning algorithms, which is typically higher than for online algorithms, may impose restrictions on how small delay that can be achieved in a practical application. 

### _3.2.2 Offline Anomaly Detection_ 

Previously proposed algorithms are mainly designed for anomaly detection in databases and, hence, it is often explicitly or implicitly assumed that the _complete_ trajectory (from start to end points) is available prior to classification. This is true for, e.g., algorithms based on dimensionality reduction and other normalisation techniques [12]–[15] _._ Moreover, most of the proposed trajectory similarity measures, including ED, DTW and LCSS (Section 2.2), are essentially designed for complete trajectories, even though some of them (e.g., LCSS) are more robust to missing data points than others. In surveillance applications where trajectories are sequentially updated in real-time, anomaly detection is delayed until the trajectory has terminated and, thus, the ability to react to impending events is limited. 

### _3.1.3 Ad-Hoc Anomaly Thresholds_ 

A key parameter in most, if not all, anomaly detection algorithms is the _anomaly threshold._ It regulates the balance between the _sensitivity_ [29], i.e., the fraction of the abnormal examples that are successfully detected, and the _false alarm rate_ [29], i.e., the fraction of normal examples that are erroneously detected as anomalous. Most algorithms define the threshold in terms of a distance, density or data likelihood [7]. These measures are typically not normalised and the procedures for setting the thresholds seem to be more or less ad-hoc. In particular, their interpretation are not very intuitive to, e.g., an operator of a surveillance system and it may be difficult to predict the actual anomaly detection rate on future data. In case of modern classification-based methods, such as one-class SVM, it has been argued that ”while these approaches provide impressive computationally efficient solutions on real data, it is generally difficult to precisely relate tuning parameter choices to desired false alarm probability” [30]. The difficulty of tuning the anomaly threshold may result in high false alarm rates and low precision, which is critical to the usability of the system [31]. More specifically, a low precision will increase the workload of an operator of a surveillance system. This increases the risk that the anomaly detector is considered a nuisance and, hence, is ignored or turned off [32]. 

In contrast, algorithms that are designed for _sequential anomaly detection_ in _incomplete_ trajectories (also known as trajectory streams [33]) enable timely detection of anomalies as they evolve. Examples of such algorithms include various point-based anomaly detectors where a low-dimensional feature model of the current and previous trajectory states is considered (e.g., [21], [22]). Yet, an obvious limitation of such algorithms is that they do not capture more long-term trajectory behaviour. A compromise between a point-based approach and a traditional model of complete trajectories is to consider a sub-trajectory model. Hu _et al_ . [10] proposed an algorithm where each trajectory is divided into a number of fixed length and non-overlapping subsequences of data points. Each such subsequence is then represented as a high-dimensional feature vector. However, such methods typically involves more preprocessing, such as alignment and interpolation, and more parameters, such as size of the subsequence; it may not be obvious how the size of the subsequence should be chosen. Moreover, there will still be a delay in anomaly detection that is bounded by the length of the subsequence. Bu _et al_ . [33] developed an algorithm for online learning and33] developed an algorithm for online learning and] developed an algorithm for online learning and sequential anomaly detection in a single continuous trajectory stream. However, this algorithm has at least four free parameters and it is not clear how different values affect the expected anomaly detection rate. 

### **3.2 Anomalous Trajectory Detection** _3.2.1 Offline Learning_ 

With a few exceptions (notably [19]), previous algorithms detection that is bounded by the length of the subsequence. (e.g., [6], [23]) are designed for _offline learning_ in the sense Bu _et al_ . [33] developed an algorithm for online learning and33] developed an algorithm for online learning and] developed an algorithm for online learning and that all training trajectories are assumed to be available sequential anomaly detection in a single continuous trajecfrom the outset; fixed model parameters and thresholds tory stream. However, this algorithm has at least four free are estimated or tuned once based on a batch of training parameters and it is not clear how different values affect data and are then repeatedly used for anomaly detecthe expected anomaly detection rate. tion. In contrast, algorithms designed for _online learning_ incrementally updates the model parameters as each new **4 CONFORMAL ANOMALY DETECTION** training trajectory is observed. The need for online learning was highlighted by Piciarelli _et al_ ., who proposed an effiIn the previous section, we discussed a number of gencient online trajectory clustering algorithm [19]. It may be eral limitations of previous anomaly detection algorithms counter-argued that taking the system offline is not strictly that need to be addressed. In this section, we introduce necessary in case of an offline learning process that runs in and discuss conformal anomaly detection, which is a novel parallel with the anomaly detector, where updated model approach to anomaly detection that addresses these issues. Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on September 11,2026 at 17:32:55 UTC from IEEE Xplore.  Restrictions apply. 

IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE, VOL. 36, NO. 6, JUNE 2014 

1162 

_smoothed p_ -values according to (5) is that the probability of error is now _exactly_ equal to _ϵ_ [3]: 

Conformal anomaly detection is an extension of the framework of conformal prediction. Therefore, we will first give a brief overview of conformal prediction and its main results. 


![](Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories_images/Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories.pdf-0005-04.png)


One of the most important properties of conformal predictors based on (5) is that successive prediction errors are _independent_ during online learning and prediction [34], i.e., when the training set is updated with the true label for the current test example before predicting the label of the next example: Assume a sequence of test examples _zl_ +1 _, . . . , zN_ . For each _n_ = _l_ + 1 _, . . . , N_ , the online conformal predictor outputs a prediction set for _yn_ based on the observed features _xn_ and the _updated_ training set _z_ 1 _, . . . , zn_ −1. Let err<sup>_ϵ_</sup> _n_<sup>∈{0</sup><sup>_,_1} be an indicator variable for the</sup> event that _yn_ ∈ _/ �n_<sup>_ϵ_.Then,thesequenceofrandomvariables</sup> err<sup>_ϵ_</sup> _l_ +1<sup>_, . . . ,_err</sup> _N_<sup>_ϵ_areindependentandwilleachtakevalue1</sup> with probability _ϵ_ [34]. This implies that the empirical error rate of the online conformal predictor is guaranteed to be _well-calibrated_ : 

### **4.1 Preliminaries: Conformal Prediction** 

Conformal prediction is a technique for providing valid measures of _confidence_ for individual predictions made by machine learning algorithms [34]. Assume a training set _z_ 1 _, . . . , zl_ where each example _zi_ = � _xi, yi_ � : _i_ = 1 _, . . . , l_ consist of features _xi_ ∈ **X** and label _yi_ ∈ **Y** . Given a new example with observed features _xl_ +1 and predefined _significance level ϵ_ ∈ _(_ 0 _,_ 1 _)_ , a conformal predictor outputs a _prediction set �l_<sup>_ϵ_</sup> +1<sup>⊆</sup><sup>**Y**fortheunknownlabel</sup><sup>_yl_+1.Thepredictionset</sup> is _valid_ at the specified significance level in the sense that the probability of an _error_ , i.e., the event that the prediction set does _not_ include the true label, is guaranteed to be less or equal to _ϵ_ : 


![](Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories_images/Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories.pdf-0005-08.png)



![](Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories_images/Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories.pdf-0005-09.png)


under the relatively weak statistical assumption that _z_ 1 _, . . . , zl_ +1 are _Independent and Identically Distributed_ (IID) [3]. For example, setting _ϵ_ = 0 _._ 05, we know that the probability that a prediction set includes the true label is at least 95%, regardless of the underlying probability distribution, which may be unknown. That is, we have 95% confidence in the prediction set. The basic idea of conformal prediction is to estimate the _p-value py_ for each possible label _y_ ∈ **Y** for the new example and exclude from the prediction set those labels where _py < ϵ_ [34]. In order to estimate _p_ -values, the concept of a _Non-Conformity Measure_ (NCM) is introduced, which measures how “different” an example is relative a set of examples. Formally, an NCM is a real-valued function _A_ � _B, z_ � that returns a _nonconformity score α_ measuring how different an example _z_ is from the examples in the _bag_ (also known as multi-set) _B_ [35]. By calculating the nonconformity score for each example _zi_ : _i_ = 1 _, . . . , n_ relative the rest of the examples _Bi_ = � _zj_ : _j_ = 1 _, . . . , n, j_ = _i_ �, the _p_ -value _pi_ for _zi_ can be estimated as the ratio of the nonconformity scores _α_ 1 _, . . . , αn_ that are at least as large as _αi_ : 

A conformal predictor will produce valid prediction sets that satisfy (2) using any real-valued function _A_ � _B, z_ � as the NCM. However, the prediction sets will only be small and, thus, informative if an appropriate NCM is chosen. If available, domain knowledge regarding, e.g., the structure of the data generating process should be exploited when defining nonconformity measures. Nevertheless, several general NCMs based on standard machine learning algorithms have been proposed that do not require any particular domain knowledge, e.g., the k-nearest neighbours algorithm, (kernel) ridge regression, SVM and neural networks [3]. 

### **4.2 The Conformal Anomaly Detector** 

The framework of conformal prediction was originally developed for supervised learning and prediction applications [3]. However, theoretical results from conformal prediction are also highly relevant for the problem of anomaly detection. The key observation is that the estimated _p_ -value (3) is a general and useful measure of anomaly. Based on the idea of estimating _p_ -values using a NCM, we define the Conformal Anomaly Detector (CAD) as follows: 


![](Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories_images/Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories.pdf-0005-14.png)


Given a new example with observed features _xl_ +1 and hypothetical label _Y_ , it is expected that any _Y_ = _yl_ +1, i.e., any label other than the true label, would result in the corresponding _αl_ +1 being relatively large compared to _α_ 1 _, . . . , αl_ . This would imply that _pY_ is small and that the corresponding example constitutes an outlier. Hence, the prediction set is formed by estimating _pY_ for each _Y_ ∈ **Y** and including in the prediction set those _Y_ for which _pY_ ≥ _ϵ_ : 

Given a training set _(z_ 1 _, . . . , zl)_ , a NCM _A_ and predefined anomaly threshold _ϵ_ , CAD (Algorithm 1) classifies an unlabelled test example _zl_ +1 based on its _p_ -value _pl_ +1. That is, the nonconformity score is calculated for each example relative the rest using using _A_ (lines 1–3 of Algorithm 1) and _pl_ +1 estimated for _zl_ +1 according to (3) (line 4). If _pl_ +1 _< ϵ_ , then _zl_ +1 is classified as a _conformal anomaly_ : Anom<sup>_ϵ_</sup> _l_ +1<sup>= 1</sup><sup>_._</sup> Otherwise, _zl_ +1 is classified as _normal_ : Anom<sup>_ϵ_</sup> _l_ +1<sup>= 0</sup><sup>_._</sup> 

The definition of a conformal anomaly is consistent with the statistical definition of an _outlier_ given by Hawkins [36]. That is, a conformal anomaly corresponds to a test example _zl_ +1 that deviates so much from _(z_ 1 _, . . . , zl)_ as to arouse suspicion that it was _not_ generated according to the same mechanism as _(z_ 1 _, . . . , zl)_ . Analogously to statistical hypothesis testing, _ϵ_ corresponds to an upper bound of the probability of erroneously rejecting the null hypothesis that _zll_ +11 and _(zz_ 1 _, . . . , zl) zl)l))_ are independent and random samples 


![](Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories_images/Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories.pdf-0005-18.png)


The validity property of conformal predictors (2) can be further strengthened by slightly modifying (3): 


![](Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories_images/Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories.pdf-0005-20.png)


where _τi_ ∈ [0 _,_ 1] is an independent and random sample probability of erroneously rejecting the null hypothesis that from the uniform distribution [3]. The result of estimating _zll_ +11 and _(zz_ 1 _, . . . , zl) zl)l))_ are independent and random samples Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on September 11,2026 at 17:32:55 UTC from IEEE Xplore.  Restrictions apply. 

LAXHAMMAR AND FALKMAN: ONLINE LEARNING AND SEQUENTIAL ANOMALY DETECTION IN TRAJECTORIES 

1163 

offline CAD may be significantly higher than _ϵ_ since the sequence of random variables Anom<sup>_ϵ_</sup> _l_ +1<sup>_, . . . ,_Anom</sup> _N_<sup>_ϵ_are</sup><sup>_not_</sup> independent. In the online framework, though, the rate of detected anomalies will, with high probability, be less or approximately equal to _ϵ_ . This non-asymptotic property, which we refer to as _well-calibrated alarm rate_ , is formalised by Theorem 2: 

**Algorithm 1:** Conformal Anomaly Detector (CAD) 

|**Inp**<br>|**ut:** NCM _A_, anomaly threshold _ϵ_, training set<br>_(z_1_, . . . , zl)_ and test example _zl_+1.<br>|
|---|---|
|**Ou**<br>|**tput:** Indicator variable Anom<sup>_ϵ_</sup><br>_l_+1 <sup>∈{0</sup><sup>_,_ 1}.</sup><br>|
|1:|**for** _i_←1 to _l_+1 **do**<br><br><br>|
|2:<br>|_αi_ ←_A_<br>��<br>_z_1_, . . . , zl_+1<br>�<br>\_zi, zi_<br>�<br>|
|3: <br>4: <br>|**end for**<br> _pl_+1 ←<sup>|{</sup><sup>_i_=1</sup><sup>_,...,l_+1:</sup><sup>_αi_≥</sup><sup>_αl_+1}|</sup><br>_l_+1<br>|
|5:|**if** _pl_+1 _< ϵ_ **then**|
|6:<br>|Anom<sup>_ϵ_</sup><br>_l_+1 <sup>←1</sup><br>|
|7:|**else**|
|8:<br>|Anom<sup>_ϵ_</sup><br>_l_+1 <sup>←0</sup><br>|
|9:|**end if**|



- **Theorem 2.** _Assume that the sequence of examples z_ 1 _, . . . , zN are IID and that N_ − _l is large. For any choice of NCM A and anomaly threshold ϵ, the rate of detected conformal anomalies will, with very high probability, be less or approximately equal to ϵ for the online CAD:_ 


![](Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories_images/Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories.pdf-0006-06.png)


**Proof.** Let us temporarily assume that the deterministic _p_ -value (3) for each test example _zn_ : _n_ = _l_ + 1 _, . . . , N_ is replaced by the corresponding smoothed _p_ -value (5). This would imply that _Pr_ �Anom<sup>_ϵ_</sup> _n_<sup>= 1</sup> � = _ϵ_ , i.e., that the probability of the event that _zn_ is classified as a conformal anomaly is exactly _ϵ_ . Since the smoothed _p_ -values _pl_ +1 _, . . . , pN_ are independent in the online framework [3, Theorem8.2],therandomvariablesAnom<sup>_ϵ_</sup> _l_ +1<sup>_, . . . ,_Anom</sup> _N_<sup>_ϵ_</sup> are also independent. Therefore, if _N_ − _l_ is large, it follows from the law of large numbers that the rate of detected conformal anomalies will, with very high probability, be approximately equal to _ϵ_ . Now, since the probability of a conformal anomaly is less or equal to _ϵ_ in the case of deterministic _p_ -values (Proposition 1), the rate of detected conformal anomalies for the online CAD will, with very high probability, be less or approximately equal to _ϵ_ . 

from the same probability distribution [35]. Hence, the following proposition regarding the probability of a conformal anomaly can be stated: 

**Proposition 1.** _Assume that z_ 1 _, . . . , zl_ +1 _are IID. For any choice of NCM A, the specified anomaly threshold ϵ corresponds to an upper bound of the probability of the event that zl_ +1 _is classified as a conformal anomaly by CAD:_ 


![](Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories_images/Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories.pdf-0006-10.png)


The larger the value of _ϵ_ , the higher the expected rate of detected conformal anomalies. 

From an application perspective, there are at least three different explanations for a conformal anomaly. Firstly, it may correspond to a relatively rare or previously unseen example generated from the same probability distribution as _(z_ 1 _, . . . , zl)_ . Secondly and thirdly, it may be a “true” anomaly in the sense that it was not generated according to the same probability distribution as _(z_ 1 _, . . . , zl)_ ; either _zl_ +1 is a true novelty, or _(z_ 1 _, . . . , zl)_ itself is in fact not IID. A nonIID training set may be explained by incomplete or biased data collection. In a public video surveillance application, e.g., observed behaviour during early morning or late afternoon may appear anomalous if the training set is based on data recorded during a limited time of the day, e.g., 10 a.m. to 2 p.m. Another possible reason for a non-IID training set is that the underlying probability distribution has actually changed. In maritime surveillance, for example, new vessel trajectories may arise as a result of new traffic regulations. If the rate of detected conformal anomalies suddenly starts to deteriorate from _ϵ_ in an online application, there may be reasons to suspect that the underlying probability distribution has changed recently. 

### **4.4 Unsupervised and Semi-Supervised Conformal Anomaly Detection** 

The conformal anomaly detection framework is essentially based on an unsupervised learning paradigm where there is no explicit notion of normal and abnormal classes. Nevertheless, in anomaly detection applications, each example is often considered to belong to either a normal or an abnormal class (Section 2.1). Similar to Eskin [37], let us therefore assume that examples of the normal and abnormal classes are generated according to the unknown probability distributions _PNormal_ and _PAbnormal_ , respectively, and that the unknown prior probability of the abnormal class is equal to _λ_ . The generative distribution for _unlabelled_ examples can then be modelled as a _mixture model_ : 


![](Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories_images/Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories.pdf-0006-15.png)


Depending on whether the training set is assumed to be unlabelled or labelled normal, CAD can be considered to operate in an unsupervised or semi-supervised anomaly detection mode, respectively (Section 2.1).). 

### **4.3 Offline vs. Online Conformal Anomaly Detection** 

Assume an initial training set _(z_ 1 _, . . . , zl)_ and a sequence operate in an unsupervised or semi-supervised anomaly of new test examples _zl_ +1 _, . . . , zN_ . The _offline_ CAD classidetection mode, respectively (Section 2.1).). fies each _zn_ : _n_ = _l_ + 1 _, . . . , N_ based on the initial training The unsupervised online CAD is perhaps the most interset _(z_ 1 _, . . . , zl)_ . In contrast, the _online_ CAD classifies each esting from both a theoretical and practical point of view; _zn_ based on the _updated_ training set _(z_ 1 _, . . . , zn_ −1 _)_ . That is, it does not require any label feedback and the overall rate _zn_ −1 is appended to the training set _(z_ 1 _, . . . , zn_ −2 _)_ before of detected conformal anomalies is well-calibrated, regardthe classification of _zn_ . If _z_ 1 _, . . . , zn_ are IID, we know less of _PNormal_ , _PAbnormal_ and _λ_ . The only assumption is from Proposition 1 that the _unconditional_ probability that that _(z_ 1 _, . . . , zN)_ constitute an IID sample from _PData_ , which _zn_ is classified as a conformal anomaly is bounded by _ϵ_ . does not seem to be an impractical or otherwise unreNevertheless, the actual rate of detected anomalies for the alistic assumption. The semi-supervised online CAD also Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on September 11,2026 at 17:32:55 UTC from IEEE Xplore.  Restrictions apply. 

IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE, VOL. 36, NO. 6, JUNE 2014 

1164 

each example represents a complete trajectory, most, if not all, of the previously proposed trajectory similarity measures (Section 2.2) would be applicable as NCMs for offline conformal anomaly detection in a trajectory database. However, the application of CAD for sequential anomaly detection in trajectories imposes some further requirements on the NCM. That is, it should enable the computation of a _preliminary_ nonconformity score for a partially observed trajectory; otherwise, anomaly detection is delayed until the complete trajectory has been observed. Further, the _p_ -value for an incomplete trajectory should _monotonically decrease_ as the trajectory is sequentially updated; if this is not true, then the property well-calibrated alarm rate (Theorem 2) will no longer be valid. These properties are not fulfilled by previous NCMs (e.g., [3]) or other trajectory similarity measures proposed for anomaly detection. 

has a similar notion of well-calibrated alarm rate: Assume that � _z_<sup>′</sup> _l_ +1<sup>_, . . . , z_′</sup> _Q_<sup>:</sup><sup>_Q_≤</sup><sup>_N_</sup> � corresponds to the subsequence of normal test examples of the full sequence � _zl_ +1 _, . . . , zN_ � and that each _z_<sup>′</sup> _n_<sup>:</sup><sup>_n_=</sup><sup>_l_+2</sup><sup>_, . . . , Q_isclassifiedbasedon</sup> the updated training set � _z_ 1 _, . . . , zl, z_<sup>′</sup> _l_ +1<sup>_, . . . , z_</sup> _n_<sup>′</sup> −1�. Further, assume that _Q_ − _l_ is large and that � _z_ 1 _, . . . , zl, z_<sup>′</sup> _l_ +1<sup>_, . . . , z_′</sup> _Q_ � constitute an IID sample from _PNormal_ . Then, the rate of the normal test examples � _z_<sup>′</sup> _l_ +1<sup>_, . . . , z_′</sup> _Q_ � that are erroneously classified as anomalous, i.e., the _false alarm rate_ , will be well-calibrated. The semi-supervised approach is, however, less practical in the online mode since it requires label feedback for each _zn_ : _n_ = _l_ + 1 _, . . . , N_ in order to know whether _zn_ is part of � _z_<sup>′</sup> _l_ +1<sup>_, . . . , z_′</sup> _Q_ � and, hence, should be added to the training set before the classification of _zn_ +1. The semi-supervised offline CAD mitigates this practical problem at the cost of losing the theoretical guarantee of a well-calibrated false alarm rate. 

In Section 5.2, we propose the Directed Hausdorff k- nearest Neighbour (DH-kNN) NCM for sequential conformal anomaly detection in trajectories. It is based on a nearest neighbour NCM (Section 5.1.1) in combination with the directed Hausdorff distance (DHD) (Section 5.1.2). One of the key properties of DHD is that examples, in our case trajectories, are represented as _point sets_ of arbitrary size, which may be incrementally updated. That is, trajectories are not required to be complete or normalised to fixed-dimensional feature vectors. Moreover, DHD has some properties that can be used for proving the monotonicity of the _p_ -values during sequential update of an incomplete trajectory using DH-kNN NCM (Theorem 3). 

Regardless of whether CAD operates in the unsupervised or semi-supervised mode, classification performance is obviously dependent on the chosen NCM and how well it discriminates between examples from _PAbnormal_ and _PNormal_ . In the unsupervised mode, classification performance is further dependent on the character of _PAbnormal_ ; intuitively, if the abnormal examples vary greatly, i.e., _PAbnormal_ has high entropy, then performance in the unsupervised mode should not be worse than in the semi-supervised mode. However, if abnormal examples vary relatively little from each other, i.e., _PAbnormal_ has very small entropy, then performance in the unsupervised mode may suffer as new abnormal examples might not differ significantly from the abnormal examples in the training set. 

### **5.1 Preliminaries** _5.1.1 Nearest Neighbour Nonconformity Measures_ 

NCMs based on the nearest neighbour principle have previously been proposed for supervised classification [3] and anomaly detection [38]. The intuition is that examples of the same class are close to each other in feature space, while examples of different classes are further away from each other. Nearest neighbour methods are relatively easy to implement, require little in the way of tuning and often perform quite well [39]. In particular, nearest neighbour methods are appropriate for online learning since they do not require extensive update of model parameters when new training data is added (compared to, e.g., neural networks and SVMs). Moreover, nearest neighbour algorithms have some strong consistency results: The asymptotic error rate is less than twice the Bayes error rate, which corresponds to the minimum achievable error rate given the distribution of the data [40]. 

### **4.5 Tuning of the Anomaly Threshold** 

In the case of the unsupervised CAD, _ϵ_ should generally be close to _λ_ in order to achieve a good balance between the sensitivity and precision. Indeed, assuming an ideal NCM such that _αi > αj_ for any pair of examples _zi_ and _zj_ belonging to the abnormal and normal classes, respectively, it is intuitively clear that _ϵ_ = _λ_ would result in sensitivity and precision both being close to 100%. Considering the semi-supervised CAD, _ϵ_ corresponds the expected false alarm rate (Section 4.4) and should therefore be set as low as possible while still maintaining reasonable sensitivity. <u>1</u> Nevertheless, setting _ϵ < l_<sup>shouldalwaysbeavoided</sup> for both the unsupervised and semi-supervised CAD and regardless of the NCM, since the sensitivity to abnormal examples will then be zero. To see this, assume we observe an abnormal example _zl_ +1 such that _αl_ +1 ≫ _αi_ : _i_ = 1 _, . . . , l_ . From line 4 of Algorithm 1, it is clear that _pl_ +1 = _l_ +11<sup>. Hence,</sup> <u>1</u> if _ϵ < l_ +1<sup>,</sup><sup>_zl_+1willnotbeclassifiedasanomalous,even</sup> though it is very extreme. 

### _5.1.2 Hausdorff Distance_ 

Generally speaking, the Hausdorff distance is a dissimilarity measure for two sets of points in a metric space. It is a well known distance measure in the field of computational geometry and image processing, where it has been applied for shape matching and shape recognition [4]. Given two sets of points _A, B_ ⊆ R<sup>_d_</sup> , DHD,<sup>−→</sup> _δ H_ , from A to B is as: 

## **5 SEQUENTIAL CONFORMAL ANOMALY DETECTION IN TRAJECTORIES** 

The only design parameter of CAD is the NCM. In principle, any real-valued function _A_ � _B, z_ � that accurately discriminates between examples from the normal and abnormal classes would be appropriate. Assuming that 


![](Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories_images/Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories.pdf-0007-14.png)


Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on September 11,2026 at 17:32:55 UTC from IEEE Xplore.  Restrictions apply. 

LAXHAMMAR AND FALKMAN: ONLINE LEARNING AND SEQUENTIAL ANOMALY DETECTION IN TRAJECTORIES 

1165 

Fig. 1. Illustration of the directed Hausdorff distances between two polygonal curves _A_ and _B_ . 

where distance between points is measures by some metric _dist (a, b)_ , typically ED. That is,<sup>−→</sup> _δH (A, B)_ corresponds to the maximum distance from a point in _A_ to the closest point in _B_ . Assuming that the point sets represent different shapes, the DHD captures the degree to which shape _A_ resembles some _part_ of shape _B_ . Hence, it is a natural distance measure when _A_ is incomplete, since it does not require that every part of _B_ is matched with some part of _A_ . The DHD between two polygonal curves are illustrated in Fig. 1. It should be noted that the DHD is not a metric since it is not symmetric; the reverse<sup>−→</sup> _δH (B, A)_ is in general different from<sup>−→</sup> _δH (A, B)_ . 

### **5.2 The Directed Hausdorff k-Nearest Neighbours Nonconformity Measure** 

We propose combining the previously proposed nearest neighbour NCM for anomaly detection [38] with the DHD as follows: Assume a bag of unlabelled examples { _z_ 1 _, . . . , zn_ } where each _zi_ ⊆ R<sup>_d_</sup> : _i_ = 1 _, . . . , n_ is represented by a non-empty set of points in a _d_ -dimensional space. DH-kNN NCM for _zi_ relative { _z_ 1 _, . . . , zn_ } \ _zi_ is defined as: 


![](Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories_images/Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories.pdf-0008-06.png)


where _NN_ � _zi,_ { _z_ 1 _, . . . , zn_ } \ _zi, j_ � ∈{ _z_ 1 _, . . . , zn_ } \ _zi_ corresponds to the _j_ th nearest neighbour to _zi_ according to (10). One of the key properties of (11) is that the preliminary _p_ -value _p_ ˆ _l_ +1 for an incomplete test example _z_<sup>∗</sup> _l_ +1<sup>⊂</sup><sup>_zl_+1</sup> monotonically decreases as more points are included from _zl_ +1; this property is formalised by Theorem 3, which is proven below: 

- **Theorem 3.** _Assume that z_<sup>∗</sup> _i_<sup>_and z_∗∗</sup> _i are non-empty subsets of zi suchp-valuesthatp_ ˆ _zi_<sup>∗</sup> _iand_<sup>⊂</sup><sup>_z_</sup> _p_ ˆ<sup>∗∗</sup> _i_<sup>′</sup> _i_<sup>_and_</sup> ⊂ _zi_<sup>_the_</sup> _. Then,_<sup>_final_</sup> _the_<sup>_p-value_</sup> _corresponding_<sup>_piforthe_</sup> _preliminary_<sup>_ithexample_</sup> _relative_ { _z_ 1 _, . . . , zn_ } \ _zi, estimated according to (11), must satisfy p_ ˆ _i_ ≥ˆ _p_<sup>′</sup> _i_<sup>≥</sup><sup>_pi.Thatis,thep-valueforasubsetofzi_</sup> _monotonically decreases as more points are included in the subset._ 

- **Proof.** From (10) it is clear that<sup>−→</sup> _δH_ � _z_<sup>∗</sup> _i_<sup>_, z_</sup> � ≤<sup>−→</sup> _δH_ � _z_<sup>∗∗</sup> _i_<sup>_, z_</sup> � ≤ −→ _δH (zi, z)_ for any _z_ ∈{ _z_ 1 _, . . . , zn_ }; the maximum distance from any point _a_ ∈ _A_ to the closest point in _B_ monotonically increases as more points are added to _A_ . Thus, the sum in (11) also monotonically increases as more points are considered from _zi_ . The preliminary nonconformity scores _α_ ˆ _i_ and _α_ ˆ _i_<sup>′andthefinalnonconformityscore</sup><sup>_αi_</sup> for the _i_ th example relative { _z_ 1 _, . . . , zn_ } \ _zi_ , calculated according to (11), must therefore satisfy: 

Further, considering (10) we see that the distance from each point _a_ from a fixed set _A_ to the closest point in _B_ monotonically decreases as more points are added to _B_ . Hence, it follows that<sup>−→</sup> _δH_ � _zj, z_<sup>∗</sup> _i_ � ≥<sup>−→</sup> _δH_ � _zj, z_<sup>∗∗</sup> _i_ � ≥<sup>−→</sup> _δH_ � _zj, zi_ � for any _zj_ ∈{ _z_ 1 _, . . . , zn_ }. Consequently, the sum in (11) also monotonically decreases as more points are considered from _zi_ . This implies that preliminary nonconformity scores _α_ ˆ _j_ and _α_ ˆ _j_<sup>′andthefinalnonconformity</sup> score _αj_ for any other example _zj_ ∈{ _z_ 1 _, . . . , zn_ } \ _zi_ relative { _z_ 1 _, . . . , zn_ } \ _zj_ , calculated according to (11), must satisfy: 


![](Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories_images/Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories.pdf-0008-11.png)


From (12) and (13), it follows that: 


![](Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories_images/Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories.pdf-0008-13.png)


As a consequence of Theorem 3, well-calibrated alarm rate is maintained for any conformal anomaly detector based on (11) when the new example is sequentially updated with new points. Note that this would not be the case if we used another NCM based on, for example, the _average_ (instead of maximum) distance to the closest point of the other set. 

### **5.3 The Sequential Hausdorff Nearest Neighbours Conformal Anomaly Detector** 

Based on (11), we propose SHNN-CAD (Algorithm 2) for sequential anomaly detection applications. Given: 

- the anomaly threshold _ϵ_ , 

- the number of nearest neighbours _k_ , 

- • the training set _(z_ 1 _, . . . , zl)_ , 

- the distance matrix _H_ , where each element _Hi,j_ : _i_ = 1 _, . . . , l, j_ = 1 _, . . . , k_ corresponds to the DHD from _zi_ to its _j_ th-nearest neighbour among � _z_ 1 _, . . . , zi_ −1 _, zi_ +1 _, . . . , zl_ �, 

- • the empty priority queue _Q_ [41], 

- the test example _zl_ +1 = { _x_ 1 ∪ _x_ 2 ∪· · · ∪ _xL_ } observed as a sequence of disjunct subsets _x_ 1 _, . . . , xL_ such that _xi_ ∩ _xj_ = ∅: _i, j_ = 1 _, . . . , L_ & _j_ = _i_ , 

SHNN-CAD sequentially updates the classification of _zl_ +1 and outputs: 

   - the sequence of indicator variables Anom<sup>_ϵ_</sup> where each _l_ +1 _,_ 1<sup>_, . . . ,_Anom</sup><sup>_ϵ_</sup> _l_ +1 _,L_<sup>,</sup> 

   - Anom<sup>_ϵ_</sup> _l_ +1 _,i_<sup>:</sup><sup>_i_</sup> = 1 _, . . . , L_ − 1 corresponds the preliminary classification of _zl_ +1 based on the subset { _x_ 1 ∪· · · ∪ _xi_ } ⊂ _zl_ +1, and Anom<sup>_ϵ_</sup> _l_ +1 _,L_<sup>correspondsto</sup> the final classification of _zl_ +1, 

   - the vector _(h_ 1 _, . . . , hl)_ where _hi_ : _i_ = 1 _, . . . , l_ corresponds to the DHD from _zl_ +1 to _zi_ , 

   - • the vector _h_<sup>′</sup> where _h_<sup>′=1</sup><sup>_, . . . , l_corre-</sup> � 1<sup>_, . . . , h_′</sup> _l_ � _i_<sup>:</sup><sup>_i_</sup> 

   - sponds to the DHD from _zi_ to _zl_ +1. 

- The algorithm works as follows: For each _zi_ : _i_ = 1 _, . . . , l_ , the DHD from _zl_ +1 to _zi_ , _hi_ , is initialised to zero and the sum of the distances to the _(k_ − 1 _)_ -nearest neighbours of _zi_ is precomputed (lines 1–4 of Algorithm 2). The following nested loops (lines 5–31) are then repeated for each 

_α_ ˆ _i_ ≤ˆ _αi_<sup>′≤</sup><sup>_αi._</sup> (12) ing nested loops (lines 5–31) are then repeated for each Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on September 11,2026 at 17:32:55 UTC from IEEE Xplore.  Restrictions apply. 

IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE, VOL. 36, NO. 6, JUNE 2014 

1166 

_xj_ : _j_ = 1 _, . . . , L_ and _zi_ : _i_ = 1 _, . . . , l_ : First, _hi_ is updated as the DHD from � _x_ 1 ∪· · · ∪ _xj_ � to _zi_ , which is calculated in an incremental manner based on the distance from � _x_ 1 ∪· · · ∪ _xj_ −1� to _zi_ calculated in the previous iteration (line 7). If _Q_ , which stores the current _k_ -nearest neighbour distances to � _x_ 1 ∪· · · ∪ _xj_ �, contains less than _k_ distance values, _hi_ is simply inserted into _Q_ (line 9). If _Q_ contains _k_ distance values and _hi_ is less than the current _k_ th nearest neighbour distance, the maximum distance value in _Q_ is removed and _hi_ is inserted into _Q_ (lines 12–13). The DHD from _zi_ to _zl_ +1, _h_<sup>′</sup> _i_<sup>,isupdatedasthedistance</sup> scorefrom _αz_ ˆ _ii_ forto � _zxi_ 1is ∪· · · ∪then updated _xj_ �. The dependingpreliminaryonnonconformitywhether _h_<sup>′</sup> _i_<sup>is</sup> smaller than the DHD from _zi_ to its _k_ th-nearest neighbour in the training set (lines 16–21). Next, the _k_ distance values are extracted from _Q_ and _α_ ˆ _l_ +1 is updated as the sum of these distances (lines 23–24). Finally, the preliminary _p_ - value and the classification of the test example are updated (lines 25–30). 

**Algorithm 2:** The Sequential Hausdorff Nearest Neighbours Conformal Anomaly Detector (SHNNCAD) 

|**Inp**|**ut:** Anomaly threshold _ϵ_, number of nearest|
|---|---|
||neighbours _k_, training set _(z_1_, . . . , zl)_, distance matrix|
||_H_, empty priority queue _Q_, sequence of updates<br>|
||_x_1_, . . . , xL_ of test example _zl_+1|
|**Ou**|**tput:** Seq. of ind. variables Anom<sup>_ϵ_</sup><br>_l_+1_,_1<sup>_, . . . ,_ Anom</sup><sup>_ϵ_</sup><br>_l_+1_,L_<sup>,</sup>|
||distance vectors _(h_1_, . . . , hl)_ and<br>�<br>_h_<sup>′</sup><br>1<sup>_, . . . , h_′</sup><br>_l_<br>�<br>.|
|1:|**for** _i_←1 to _l_ **do**<br><br>|
|2:|_vi_ ←sum<br>�<br>_Hi,_1_, . . . , Hi,k_−1<br>�|
|3:|_hi_ ←0|
|4:|**end for**|
|5:|**for** _j_←1 to _L_ **do**|
|6:|**for** _i_←1 to _l_ **do**<br>−→<br>|
|7:|_hi_ ←max<br>�<br>_δH_<br>�<br>_xj, zi_<br>�<br>_, hi_<br>�|
|8:|**if** _i_≤_k_ **then**|
|9:|_Q_.insertElement_(hi)_|
|10:|**else**|
|11:|**if** _Q_.maxElement_() > hi_ **then**|
|12:|_Q_.removeMaxElement_()_|
|13:|_Q_.insertElement_(hi)_|
|14:|**end if**|
|15:|**end if**<br><sup>−→</sup>|
|16:|_h_<sup>′</sup><br>_i_ <sup>←</sup><br>_δH_<br>�<br>_zi,_<br>�<br>_x_1∪· · · ∪_xj_<br>��|
|17:|**if** _h_<sup>′</sup><br>_i _<sup>_< Hi,k_</sup> <sup>**then**</sup>|
|18:|ˆ_αi_ ←_vi_+_h_<sup>′</sup><br>_i_|
|19:|**else**|
|20:|ˆ_αi_ ←_vi_+_Hi,k_|
|21:|**end if**|
|22:|**end for**<br><br>|
|23:|�<br>_h_<sup>∗</sup><br>1<sup>_, . . . , h_∗</sup><br>_k_<br>�<br>←_Q_.removeAllElements_()_<br><br>|
|24:|ˆ_αl_+1 ←sum<br>�<br>_h_<sup>∗</sup><br>1<sup>_, . . . , h_∗</sup><br>_k_<br>�|
||ˆ<sup>|{</sup><sup>_i_=1</sup><sup>_,...,l_+1:ˆ</sup><sup>_αi_≥ˆ</sup><sup>_αl_+1}|</sup>|
|25:|_pl_+1 ←<br>_l_+1<br>|
|26:|**if** ˆ_pl_+1 _< ϵ_ **then**|
|27:|Anom<sup>_ϵ_</sup><br>_l_+1_,j_ <sup>←1</sup>|
|28:|**else**|
|29:|Anom<sup>_ϵ_</sup><br>_l_+1_,j_ <sup>←0</sup>|
|30:|**end if**|
|31:|**end for**|



In the case of the unsupervised online SHNN-CAD, _zl_ +1 is added to the training set when _x_ 1 _, . . . , xL_ have been observed. This is also true for the semi-supervised online SHNN-CAD if _zl_ +1 is assumed to belong to the normal class. If _zl_ +1 is added to the training set, then: 

- 1) the sorted distances to the _k_ -nearest neighbours of each _z_ 1 _, . . . , zl_ , i.e., rows 1– _l_ of _H_ , are updated based on _h_<sup>′</sup> , 

- 2) the sorted distances to the _k_ -nearest neighbours of _zl_ +1 are extracted from _h_ and appended as the last row of _H_ . 

The updated training set � _z_ 1 _, . . . , zl_ +1� and the updated distance matrix _H_ are then provided as input to SHNN-CAD when classifying the next test example _zl_ +2. 

### _5.3.1 Implementation and Complexity Analysis_ 

A natural approach to implementing SHNN-CAD for sequential anomaly detection in trajectories is to adopt a polyline representation; each trajectory (1) is represented by an example _zi_ = � _x_ 1 ∪ _x_ 2 ∪· · · ∪ _xLi_ � where _x_ 1 = _χ_ 1 and _xj_ = � _χj_ −1 + _s_ · � _χj_ − _χj_ −1� : _s_ ∈ _(_ 0 _,_ 1]� for _j_ = 2 _, . . . , Li_ . That is, the first subset _x_ 1 represents the first trajectory point and each remaining subset _xj_ represent the set of all points along the line segment that connects _χj_ −1 and _χj_ . This approach allows for efficient compression of trajectories and exact calculation of (10) with time complexity _O_ �� _Li_ + _Lj_ � _log_ � _Li_ + _Lj_ �� based on algorithms from computational geometry [4], where _Li_ and _Lj_ are the number of line segments of the corresponding trajectories. Moreover, assuming that _Q_ is implemented as a heap based on a binary tree, the time complexity of insertElement _()_ , removeMaxElement _()_ , maxElement _()_ and removeAllElements _()_ in Algorithm 2 are _O_ �log _(k)_ �, _O_ �log _(k)_ �, _O (_ 1 _)_ , and _O (k)_ , respectively, where _k_ is the number of elements of the queue [41]. Based on the assumptions above, the time complexity of Algorithm 2 can be analysed as follows: The sections corresponding to lines 7, 8–15, 16 and 17–21 have complexity _O_ � _Li_ log _(Li)_ �, _O_ �log _(k)_ �, _O_ �� _Li_ + _j_ � log � _Li_ + _j_ �� and _O ( (_ 1 _)_ , respectively. Thus, the overall complexity of the inner loop (lines 6–22) is: 


![](Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories_images/Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories.pdf-0009-11.png)


where _Lmax_ is the maximum number of line segments among all of the trajectories. The sections corresponding to lines 23, 24 and 25 have complexity _O (k)_ , _O (k)_ and _O (l)_ , respectively. Since _l > k_ , the complexity of each iteration of the outer loop (lines 5–31), i.e., the update of the classification of _zn_ based on _xj_ , is equivalent to (14). Further, the pre-computations (lines 1–4) have complexity _O (l_ · _k)_ . Thus, the overall time complexity of Algorithm 2 is: 


![](Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories_images/Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories.pdf-0009-13.png)


and _O ( (_ 1 _)_ , respectively. Thus, the overall complexity Assuming that _Lmax > k_ , which is typically the case, (15) of the inner loop (lines 6–22) is: is reduced to _O_ � _l_ · _L_<sup>2</sup> _max_<sup>log</sup><sup>_(Lmax)_</sup> �. Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on September 11,2026 at 17:32:55 UTC from IEEE Xplore.  Restrictions apply. 

LAXHAMMAR AND FALKMAN: ONLINE LEARNING AND SEQUENTIAL ANOMALY DETECTION IN TRAJECTORIES 

1167 

An alternative approach to the continuous polyline representation is to only consider the end points of the line segments, i.e., assume that _xj_ = � _χj_ � : _j_ = 1 _, . . . , L_ . This representation corresponds to a less detailed model of the actual trajectory, but allows for a more simple implementation of the DHD. 

### **5.4 Discussion** 

Compared to previously proposed algorithms (Section 3), SHNN-CAD and the framework of conformal anomaly detection have some principal advantages: 

- there are no assumptions regarding the structure of the probability distribution, 

- it is parameter-light, i.e., there is only one free parameter _k_ apart from the anomaly threshold, 

- it requires no particular preprocessing or normalisation of trajectories, 

- it supports sequential anomaly detection in incomplete trajectories, 

- it supports online learning, 

- it offers a well-founded approach to the tuning of the anomaly threshold _ϵ_ (Section 4.5) with well-calibrated alarm rate in the online mode (Theorem 2 and 3). 

The property that trajectories need not be complete has in fact more general implications. It may be argued that the DHD is not only robust to future data points that have not yet been observed; it also robust to previous data points that are missing due to delayed track initialisation, re-initialisation of a previous track that was lost, etc. 

The DHD is by definition insensitive to the ordering of the data points. Thus, if only position is included in the point feature model, this may result in contraintuitive matching. An example is two objects that follow the same path but travel in opposite direction. This could be addressed by simply extending the point feature model to also include the current course or velocity vector, which would also capture the speed of the object. 

## **6 EMPIRICAL INVESTIGATIONS** 

In this section, we implement DH-kNN NCM (Section 5.2) and investigate its accuracy on three different datasets of labelled trajectories (Section 6.1). Moreover, we implement the unsupervised online SHNN-CAD (Section 4.3–4.4 and 5.3) and investigate its classification performance (Section 6.2). For simplicity, we implement an algorithm for calculating (10) that only considers the finite set of points of the trajectories. That is, we do not implemented an algorithm for calculating the exact distance between two trajectories represented as polylines, where all the intermediate points along the line segments are considered (Section 5.4). 

For comparative purposes, we also implement and investigate the performance of the time-series discords algorithm [5], which was originally proposed by Keogh _et al_ . for detecting anomalies in time-series data. The discords algorithm is parameter-light and has been demonstrated to have competitive classification performance on a wide 

Fig. 2. Plot of trajectories from one of the 1000 subsets of synthetic trajectories used for evaluating the accuracy of different trajectory outlier measures (Section 6.1.1). Grey trajectories (250) are labelled normal and black trajectories (10) are labelled abnormal. 

range of time-series databases (e.g., [5]), including trajectory datasets [6], [16]. Hence, we use the discords algorithm as a benchmark for evaluating the relative performance of DH-kNN NCM and SHNN-CAD in all of the following experiments. 

All algorithms are implemented in Java and executed on a Macbook Pro 2 _._ 66 GHz Intel Core 2 Duo processor with 8 GB of RAM. 

### **6.1 Accuracy of Trajectory Outlier Measures** 

We investigate the accuracy of DH-kNN NCM and the discords algorithm by reproducing three previously published experiments on three different datasets of labelled trajectories (Section 6.1.2–6.1.3). The main objective is to investigate how accurately DH-kNN NCM discriminates complete abnormal trajectories from complete normal trajectories, compared to previously proposed trajectory outlier measures. 

### _6.1.1 Synthetic Trajectories_ 

The first experiment was originally published by Piciarelli _et al_ . who investigated the accuracy of an outlier measure based on one-class SVM on a synthetic dataset [16]. The dataset<sup>1</sup> was created by the authors and consists of 1000 randomly generated trajectory subsets. Each subset contains 260 two-dimensional trajectories of length 16 without any time information. Of the 260 trajectories, 250 belong to five different clusters and are labelled normal. The remaining 10 are stray trajectories that do not belong to any cluster and are labelled abnormal (see Fig. 2 for a plot of one of the subsets). For each of the 1000 subsets, the authors calculated the outlier score for each of the 260 trajectories relative the remaining 259. The _error rate_ was calculated by averaging over the number of normal trajectories among the top-10 trajectories with highest outlier scores. We repeat this procedure for DH-kNN NCM by calculating the outlier score for each trajectory according to (11). Moreover, we calculate the top-ten discords [5], where each trajectory corresponds to a subsequence. The average accuracy, i.e. 1 minus the 

1. http://avires.dimi.uniud.it/papers/trclust/ 

Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on September 11,2026 at 17:32:55 UTC from IEEE Xplore.  Restrictions apply. 

IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE, VOL. 36, NO. 6, JUNE 2014 

1168 

TABLE 1 

Average Accuracy on the Synthetic Trajectories (Section 6.1.1) 


![](Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories_images/Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories.pdf-0011-04.png)


_Note that accuracy results for SVM are 1 minus the corresponding error rate reported by Piciarelli et al. [16]._ 


![](Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories_images/Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories.pdf-0011-06.png)


Fig. 4. Plot of the recorded video trajectories from the LAB-dataset [12] (Section 6.1.3). Grey trajectories (152) are labelled normal and black trajectories (8) are labelled abnormal. 

Fig. 3. Plot of the 239 trajectories from the first set of recorded video trajectories (Section 6.1.2). Grey corresponds to normal trajectories and solid and dashed black correspond to the two abnormal trajectories. 

corresponding average error rate, for all three algorithms are summarised in Table 1. 

### _6.1.2 First Set of Recorded Video Trajectories_ 

In the second experiment, we investigate accuracy on a public dataset of 239 recorded video trajectories<sup>2</sup> that were extracted from IR surveillance videos using a motion detection and tracking algorithm [42]. The trajectories are three-dimensional including time stamps and each have length five. Of the 239 trajectories, 237 are labelled normal and two are labelled abnormal (see Fig. 3). We calculate the nonconformity score for each of the 239 trajectories relative the rest according to (11) for _k_ = 1 _, . . . ,_ 5. However, in contrast to Pokrajac [42], we only consider the twodimensional spatial location of each trajectory point, i.e., we do not use the time information. Sorting the resulting nonconformity scores, we observe that the two trajectories labelled abnormal have the top-two largest nonconformity scores, regardless of _k_ . Moreover, we observe that the toptwo discords (for the two-dimensional representation) also correspond to the abnormal trajectories. Hence, similar to previous algorithms [42], DH-kNN NCM and discords achieve perfect accuracy on this dataset. 

### _6.1.3 Second Set of Recorded Video Trajectories_ 

The second set, which is known at the LAB-dataset [12], consists of 152 trajectories labelled normal and 8 trajectories labelled abnormal. The trajectories contain no time stamps and are of varying length, where the maximum and average length is 425 and 192 points, respectively (Fig. 4). The trajectories were extracted from a video recording where people were tracked in a controlled laboratory environment. Movements were planned so that normal trajectories can be grouped into four clusters and the abnormal trajectories varied deliberately from the normal trajectories. Analogously to the experimental setup described by 

Khalid [12], we evaluate accuracy of DH-kNN and the discords algorithm as follows: We first construct a training set by randomly sampling without replacement half of the 152 normal trajectories. The remaining 76 normal trajectories and the eight abnormal trajectories are used as the test set. For each test trajectory, the nonconformity score relative the training set is estimated according to (11). Moreover, the top-eight discords among the test trajectories are calculated relative the training set, where each trajectory in the training and test sets is normalised to length 50 based on linear interpolation; note that the discords algorithm require that the trajectories have the same length. Analogously to the previous experiments (Section 6.1.1–6.1.3), accuracy is calculated as the fraction of the top-eight nonconforming test trajectories and the top-eight discords that are labelled abnormal. This procedure is repeated 100 times. Average accuracy for DH-kNN NCM with _k_ = 1 _, . . . ,_ 5 and the discords algorithm are summarised in Table 2. Note that the results reported by Khalid [12] are based on a single run, i.e., not the average of 100 experiments. 

### **6.2 Unsupervised Online Learning and Sequential Anomaly Detection** 

In this experiment, we investigate the sequential classification performance of the unsupervised online SHNN-CAD and the discords algorithm on a relatively large synthetic dataset. The objectives of the experiment are to: 

- 1) Investigate how the sensitivity and precision depends on the size of training set and the value of _ϵ_ . 

#### TABLE 2 

Avg. Accuracy on 100 Test Sets of Labelled Video Trajectories (Section 6.1.3) 


![](Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories_images/Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories.pdf-0011-20.png)


_Note that results for_ m _-Mediods were reported by Khalid [12] and are based on a single test set._ 

2. www.cs.umn.edu/~aleks/inclof 

Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on September 11,2026 at 17:32:55 UTC from IEEE Xplore.  Restrictions apply. 

LAXHAMMAR AND FALKMAN: ONLINE LEARNING AND SEQUENTIAL ANOMALY DETECTION IN TRAJECTORIES 

1169 

- 2) Investigate how the _detection delay_ , i.e., the number of observed trajectory points prior to the detection of an abnormal trajectory, depends on the size of the training set and the value of _ϵ_ . Recall that a low detection delay is advantageous since it enables earlier response in a realtime surveillance application (Section 3.2.2). 

- 3) Investigate the relative performance of SHHN-CAD vs. discords. 

- 4) Validate that the rate of detected anomalies (both normal and abnormal trajectories) is indeed wellcalibrated for SHNN-CAD. 

### _6.2.1 Dataset_ 

For this experiment, a dataset of synthetic trajectories<sup>3</sup> was generated by ourselves using the publicly available trajectory generator software<sup>4</sup> written by Piciarelli. The dataset, which is previously unpublished, contains 100 random trajectory sequences, where each sequence consists of 2000 two-dimensional trajectories of length 16 that are labelled normal or abnormal. Each sequence, which is independent of the other 99 sequences, was created as follows: First, a set of 2000 normal trajectories from 10 different trajectory clusters and another set of 1000 abnormal trajectories from 1000 different “clusters” were created using the trajectory generator with the randomness parameter set to the default value 0 _._ 7. Next, a sequence of 2000 trajectories was created by random sampling without replacement from the set of normal trajectories. Finally, each normal trajectory in the sequence was independently and with probability 1% replaced by an abnormal trajectory, which was randomly sampled without replacement from the set of abnormal trajectories. Hence, the trajectory generation process is consistent with (9) with _λ_ = 0 _._ 01. A subset of the normal trajectories and all abnormal trajectories from the first sequence are shown in Fig. 5. 

### _6.2.2 Design_ 

For SHNN-CAD, we fix _k_ = 2 since it was shown to give the best accuracy results for DH-kNN NCM on all of the previous datasets (Tables 1 and 2). For each of the 100 sequences of 2000 trajectories, we allocate the first three trajectories as initial training set and calculate the corresponding distance matrix _M_ of size 3 × 3 (Section 5.3); note that three is the minimum size of the training set for which (11) is defined when _k_ = 2. The remaining 1997 trajectories are sequentially classified by the unsupervised online SHNN-CAD (Algorithm 2). The whole process is repeated for three different anomaly thresholds: _ϵ_ = 0 _._ 005 _,_ 0 _._ 01 and 0 _._ 02. The choice of _ϵ_ = 0 _._ 01 is motivated by the discussion in Section 4.5, i.e., that the anomaly threshold should be set close to _λ_ . Nevertheless, the exact value of _λ_ may be unknown and, hence, we also investigate the performance for _ϵ_ = 0 _._ 005 and 0 _._ 02. Moreover, in order to avoid the problem of zero sensitivity when the size of training set is relatively small (Section 4.5), the anomaly threshold is dynamically re-tuned to _(l_ + 1 _)_<sup>−1</sup> as long as _l < ϵ_<sup>−1</sup> . 

3. https://www.researchgate.net/profile/Rikard_Laxhammar/ 

Fig. 5. Plot of trajectories from the first sequence of synthetic trajectories used in the online learning and sequential anomaly detection experiments (Section 6.2). Grey trajectories (300) are labelled normal and black trajectories (17) are labelled abnormal. Note that for clarity, only 300 of the total 1983 normal trajectories are plotted. 

The experiment is also reproduced for a brute-force implementation of an online version of the top- _k_ discords algorithm. According to the general definition [5], the top- _k_ discords of a time-series correspond to the top- _k_ non-overlapping subsequences of predefined length _m_ that have the largest distances to their nearest non-overlapping match. In previous work [6], [16] and in the previous experiments of this paper, each subsequence simply corresponds to a complete and normalised trajectory of fixed length _m_ . However, since we are now concerned with sequential anomaly detection in incomplete trajectories, we need to consider a subsequence length that is less than the full length of the trajectories. Setting _m_ to a low value may decrease the detection delay but may also decrease the sensitivity to abnormal trajectories when the length of the abnormal part is greater than _m_ . In these experiments, we consider _m_ = 4 _,_ 8 and 12, which correspond to a quarter, a half and three quarters of the full trajectory, respectively. For each update _j_ = _m, . . . ,_ 16 of trajectory _i_ = 4 _, . . . ,_ 2000, the subsequence _χj_<sup>_i_</sup> − _m_ +1<sup>_, . . . , χ_</sup> _j_<sup>_i_isextracted,addedtothe</sup> training set of previous subsequences and classified as abnormal or normal depending on whether it is among the top- _k_ discords of the updated training set. Intuitively, _k_ should be chosen depending on the expected number of discords in the training set. Assuming that approximately 1% of all trajectories are abnormal and that each abnormal trajectory corresponds to one discord, _k_ is dynamically tuned based on the number of trajectories observed so far, i.e., _k_ = ⌈0 _._ 01 _i_ ⌉. Nevertheless, the prior probability of an abnormal trajectory may be unknown and abnormal trajectories may include more than one discord, in particular when _m_ is relatively small. Hence, we also investigate performance when _k_ = ⌈0 _._ 005 _i_ ⌉ and ⌈0 _._ 02 _i_ ⌉. 

### _6.2.3 Results_ 

In order to evaluate the relative performance of SHNNCAD vs. discords (objective 3), we calculate the average 

4. http://avires.dimi.uniud.it/papers/trclust/create_ts2.m CAD vs. discords (objective 3), we calculate the average Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on September 11,2026 at 17:32:55 UTC from IEEE Xplore.  Restrictions apply. 

IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE, VOL. 36, NO. 6, JUNE 2014 

1170 

TABLE 3 

Average _F_ 1-Score and Mean Detection Delay for the Online Learning and Sequential Anomaly Detection Experiments (Section 6.2.3) 


![](Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories_images/Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories.pdf-0013-04.png)



![](Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories_images/Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories.pdf-0013-05.png)


_Note that the maximum possible detection delay is_ 16 _, since this is the length of each trajectory._ 


![](Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories_images/Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories.pdf-0013-07.png)


_F_ 1-score and the average detection delay for each combination of the detectors’ parameters (Table 3). The _F_ 1-score corresponds to an evenly weighted combination of precision and recall: 


![](Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories_images/Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories.pdf-0013-09.png)



![](Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories_images/Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories.pdf-0013-10.png)


and it is therefore useful for comparing the overall classification performance of multiple anomaly detectors. In order to address objective 1, we estimate logistic regression models for the sensitivity and precision, respectively, dependent on the size of the training set (Fig. 6). The coefficients of the logistic regression models for the sensitivity are estimated based on the final classification results for the subset of trajectories that are labelled abnormal. In case of the precision, the coefficients are estimated based on the true label for those trajectories that are detected as anomalous. Further, in order to address objective 2, we estimate a linear regression model for the detection delay dependent on the current size of the training set (Fig. 7). Finally, a histogram of the overall alarm rate for SHNN-CAD _ϵ_ = 0 _._ 01 is shown in Fig. 8 (objective 4). The average processing time on each sequence of 2000 trajectories was 19 _._ 1 seconds for SHNN-CAD with _ϵ_ = 0 _._ 01 and 45 _._ 0 seconds for discords with _m_ = 8 and _k_ = ⌈0 _._ 01 _i_ ⌉. 

Fig. 6. Plots of the sensitivity (upper plot) and precision (lower plot) dependent on the size of the training set according to the logistic regression models, which are estimated based on the online learning and sequential anomaly detection results (Section 6.2). 

best results for discords: _F_ 1 = 0 _._ 74 and _F_ 1 = 0 _._ 76 when _k_ = ⌈0 _._ 01 _i_ ⌉ and _m_ = 8 _,_ 12, respectively. The detection delay for SHNN-CAD with _ϵ_ = 0 _._ 01 is also similar to that of discords with _m_ = 8 (10 _._ 3 and 9 _._ 7 points, respectively). However, the detection delay for discords with _m_ = 12 is considerably higher (12 _._ 3 points). Hence, we select _k_ = ⌈0 _._ 01 _i_ ⌉ and _m_ = 8 when further investigating how sensitivity, precision and detection delay depend on the size of the training set<sup>5</sup> (Figs. 6 and 7). 

### **6.3 Discussion** 

For the first two datasets (Section 6.1.1–6.1.2), it is clear that DH-kNN NCM is an accurate outlier measure, regardless of _k_ (Table 1). On the third dataset, however, results for DH-kNN NCM were slightly worse compared to discords (Table 2), which indicate that the latter has some edge over the former in the case of complete trajectories. Nevertheless, the advantage of DH-kNN NCM becomes more clear when we consider the results for SHNNCAD during online learning and sequential anomaly detection: 

Examining Fig. 6, it is clear that the sensitivity and precision improve as more unlabelled training data is accumulated. In particular, there is generally a large increase in precision. Moreover, the expected detection delay generally decreases as more the training is accumulated, with the exception of SHNN-CAD with _ϵ_ = 0 _._ 005. The explanation for this exception does not seem obvious. Nevertheless, a similar pattern was in fact observed for discords with _k_ = ⌈0 _._ 005 _i_ ⌉, which suggests that for low anomaly thresholds, 

Considering Table 3, it is clear that the best classification performance for SHHN-CAD ( _F_ 1 = 0 _._ 75) is achieved when _ϵ_ = 0 _._ 01. This confirms our hypothesis that _ϵ_ should be close to _λ_ (Section 4.5). The best classification performance for SHNN-CAD is approximately the same as the 

5. For clarity and brevity, we omit more detailed results for the mance for SHNN-CAD is approximately the same as the remaining parameter values of discords in Figs. 6 and 7. Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on September 11,2026 at 17:32:55 UTC from IEEE Xplore.  Restrictions apply. 

LAXHAMMAR AND FALKMAN: ONLINE LEARNING AND SEQUENTIAL ANOMALY DETECTION IN TRAJECTORIES 

1171 


![](Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories_images/Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories.pdf-0014-02.png)



![](Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories_images/Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories.pdf-0014-03.png)


Fig. 7. Plot of the mean detection delay dependent on the size of the training set according to the linear regression models, which are estimated based on the online learning sequential anomaly detection results (Section 6.2). The variable _s_ in the legend is an unbiased estimate of the standard deviation of the error term of the linear regression model. 

the detection delay generally _increases_ as the training set grows. Considering the end of the curves, i.e., at the point where the size of the training set approaches 2000, we see that the sensitivity and precision in most cases are still increasing, albeit at a slower rate. This indicates that the anomaly detectors may still benefit from more training data but are approaching the point where they may be considered fully trained. 

Comparing the sensitivity for SHNN-CAD _ϵ_ = 0 _._ 01 and discords, we see that the latter initially has a slight advantage until the size of the training set is 700. From that point, the sensitivity of SHNN-CAD becomes superior and increases more rapidly than for discords. When the size of the training set has reached 2000, the sensitivity of SHNN-CAD and discords are approximately 0 _._ 9 and 0 _._ 8, respectively. In case of the precision, the difference is more subtle; SHNN-CAD has initial advantage but it is passed by discords after the size of the training set has reached 400. When the size of training set reaches 2000, the precision of SHNN-CAD and discords are both close to 1 with a small advantage to discords. 

It should be noted that all the parameter values have a significant impact on performance for both SHNN-CAD and discords. However, the discords algorithm involves tuning of one more parameter than SHNN-CAD, i.e., the length of the subsequence _m_ . Moreover, the choice of _k_ for discords may not be as straightforward as the choice of _ϵ_ for SHNN-CAD, since the optimal value of the former may depend on _m_ . For example, the best classification performance for _m_ = 8 _,_ 12 is achieved with _k_ = ⌈0 _._ 01 _i_ ⌉. But for _m_ = 4, the classification performance and the detection delay are both superior with _k_ = ⌈0 _._ 02 _i_ ⌉. 

Finally, considering Fig. 8, we see that the alarm rate on each of the 100 sequences is close to the specified anomaly threshold. Hence, the alarm rate of the online unsupervised SHNN-CAD is indeed well-calibrated in practice. 

Fig. 8. Histogram of the overall alarm rate (normal and abnormal trajectories) for the unsupervised online SHNN-CAD with _ϵ_ = 0 _._ 01. Each data point corresponds to the average anomaly detection rate on one of the 100 random sequences of trajectories (Section 6.2). 

## **7 GENERALISATION AND FUTURE WORK** 

In the empirical investigations, we have only considered two-dimensional trajectories. Nevertheless, SHNN-CAD should be applicable to higher-dimensional trajectories including, e.g., velocity features, assuming that the different dimensions are properly normalised. Thus, future work includes investigating different normalisation techniques and performance on higher-dimensional trajectory datasets. 

Assuming that an appropriate NCM is defined, CAD is applicable in virtually any unsupervised or semisupervised, online or offline, anomaly detection problem. In fact, any existing anomaly or outlier detection algorithm, which has shown good classification performance in the current application domain, may potentially be adopted as a NCM in the conformal anomaly detection framework. The main benefit of such “wrapper” strategy is that it mitigates the problems with ad-hoc anomaly thresholds and offers theoretical guarantees regarding the calibration of the alarm rate. Hence, an interesting path for future work would be to investigate NCMs that are appropriate for other data types than trajectories. 

An important aspect that has not yet been addressed in this work is how to deal with a continually increasing training set; if no pruning strategy is used, the size of the training set might eventually render online anomaly detection unfeasible. Moreover, there is the risk that the underlying distribution for normal data will change, known as _population drift_ [27]. Hence, long-term learning strategies for pruning and determining when the training set is no longer valid should be investigated in future work. 

## **8 CONCLUSION** 

Previous algorithms for detecting anomalous trajectories typically suffer from one or more limitations that have been identified and discussed in this article, i.e., they are primarily designed for offline anomaly detection and suffer from tuning of many parameters, including ad-hoc anomaly thresholds. In this article, we have proposed and investigated SHNN-CAD for online learning and sequential anomaly detection in trajectories. This is a parameter-light algorithm that offers a well-founded approach to tuning the anomaly threshold according to the desired alarm rate 

Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on September 11,2026 at 17:32:55 UTC from IEEE Xplore.  Restrictions apply. 

IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE, VOL. 36, NO. 6, JUNE 2014 

1172 

or the expected frequency of anomalies. We have implemented and evaluated the classification performance of SHNN-CAD and, for comparative purposes, the discords algorithm on four different trajectory datasets. In particular, we have investigated the performance during unsupervised online learning and sequential anomaly detection on a relatively large set of synthetic trajectories. The results showed that SHNN-CAD achieved competitive classification performance with minimum parameter tuning. Future work includes investigating the application of SHNN-CAD on higher-dimensional trajectories with velocity features and long-term learning strategies for pruning the training set. The results regarding conformal anomaly detection generalises beyond the problem of detecting anomalous trajectories; assuming that an appropriate NCM is defined, CAD is applicable in virtually any unsupervised or semisupervised, online or offline, anomaly detection problem. 

- [13] R. R. Sillito and R. B. Fisher, “Semi-supervised learning for anomalous trajectory detection,” in _Proc. BMVC_ , 2008, pp. 1034–1044. 

- [14] F. Porikli, “Trajectory distance metric using hidden Markov model based representation,” in _Proc. 6th IEEE Int. Workshop PETS_ , 2004. 

- [15] S. Atev, G. Miller, and N. Papanikolopoulos, “Clustering of vehicle trajectories,” _IEEE Trans. Intell. Transp. Syst._ , vol. 11, no. 3, pp. 647–657, Sept. 2010. 

- [16] C. Piciarelli, C. Micheloni, and G. Foresti, “Trajectory-based anomalous event detection,” _IEEE Trans. Circuits Syst. Video Technol._ , vol. 18, no. 11, pp. 1544–1554, Nov. 2008. 

- [17] M. Vlachos, G. Kollios, and D. Gunopoulos, “Discovering similar multidimensional trajectories,” in _Proc. 18th IEEE Int. Conf. Data Eng._ , San Jose, CA, USA, 2002. 

- [18] B. Morris and M. Trivedi, “Learning and classification of trajectories in dynamic scenes: A general framework for live video analysis,” in _Proc. IEEE 5th Int. Conf. AVSS_ , Santa Fe, NM, USA, 2008. 

- [19] C. Piciarelli and G. Foresti, “On-line trajectory clustering for anomalous events detection,” _Pattern Recognit. Lett._ , vol. 27, no. 15, pp. 1835–1842, Nov. 2006. 

- [20] Z. Fu, W. Hu, and T. Tan, “Similarity based vehicle trajectory clustering and anomaly detection,” in _Proc. IEEE ICIP_ , 2005. 

## **ACKNOWLEDGMENTS** 

This work has been supported in part by Saab AB and in part by the Swedish Knowledge Foundation in cooperation with University of Skövde. The authors would like to thank K. Wallenius and E. Sviestins for providing valuable feedback regarding the manuscript of this article and V. Vovk for valuable feedback regarding conformal anomaly detection. Moreover, the authors would like to acknowledge C. Piciarelli and A. Lazarevi´c for making their datasets publicly available, and S. Khalid for kindly providing the LAB-dataset. 

## **REFERENCES** 

- [1] B. Morris and M. Trivedi, “A survey of vision-based trajectory learning and analysis for surveillance,” _IEEE Trans. Circuits Syst. Video Technol._ , vol. 18, no. 8, pp. 1114–1127, Aug. 2008. 

- [2] R. Laxhammar and G. Falkman, “Sequential conformal anomaly detection in trajectories based on Hausdorff distance,” in _Proc. 14th Int. Conf. Inform. Fusion_ , Chicago, IL, USA, 2011. 

- [3] V. Vovk, A. Gammerman, and G. Shafer, _Algorithmic Learning in a Random World_ . New York, NY, USA: Springer-Verlag, Inc., 2005. 

- [4] H. Alt, “The computational geometry of comparing shapes,” in _Efficient Algorithms._ Berlin, Germany: Springer, 2009, pp. 235–248, LNCS 5760. 

- [5] E. Keogh, J. Lin, and A. Fu, “HOT SAX: Efficiently finding the most unusual time series subsequence,” in _Proc. 5th IEEE ICDM_ , Washington, DC, USA, 2005. 

- [6] D. Yankov, E. Keogh, and U. Rebbapragada, “Disk aware discord discovery: Finding unusual time series in terabyte sized datasets,” _Knowl. Inf. Syst._ , vol. 17, no. 2, pp. 241–262, 2008. 

- [7] V. Chandola, A. Banerjee, and V. Kumar, “Anomaly detection: A survey,” _ACM CSUR_ , vol. 41, no. 3, pp. 1–58, 2009. 

- [8] B. Schölkopf, R. Williamson, A. Smola, J. Shawe-Taylor, and J. Platt, “Support vector method for novelty detection,” in _Proc. NIPS_ , vol. 12. 2000. 

- [9] L. J. Latecki, A. Lazarevic, and D. Pokrajac, “Outlier detection with kernel density functions,” in _Proc 5th Int. Conf. MLDM_ , Leipzig, Germany, 2007. 

- [10] W. Hu _et al_ ., “A system for learning statistical motion patterns,” _IEEE Trans. Pattern Anal. Mach. Intell._ , vol. 28, no. 9, pp. 1450–1464, Sept. 2006. 

- [11] H. Dee and S. Velastin, “How close are we to solving the problem of automated visual surveillance? A review of real-world surveillance, scientific progress and evaluative mechanisms,” _Mach. Vis. Appl._ , vol. 19, no. 5–6, pp. 329–343, 2008. 

- [12] S. Khalid, “Motion-based behaviour learning, profiling and classification in the presence of anomalies,” _Pattern Recognit._ , vol. 43, no. 1, pp. 173–186, 2010. 

- [21] C. Brax, L. Niklasson, and M. Smedberg, “Finding behavioral anomalies in public areas using video surveillance data,” in _Proc. 11th Int. Conf. Inform. Fusion_ , Cologne, Germany, 2008. 

- [22] J. Owens and A. Hunter, “Application of the self-organising map to trajectory classification,” in _Proc. 3rd IEEE Int. Workshop VS_ , Dublin, Ireland, 2000. 

- [23] J.-G. Lee, J. Han, and X. Li, “Trajectory outlier detection: A partition-and-detect framework,” in _Proc. 24th ICDE_ , Washington, DC, USA, 2008. 

- [24] R. Laxhammar, G. Falkman, and E. Sviestins, “Anomaly detection in sea traffic - A comparison of the Gaussian mixture model and the kernel density estimator,” in _Proc. 12th Int. Conf. Inform. Fusion_ , Washington, DC, USA, 2009. 

- [25] N. Taleb, _Fooled by Randomness: The Hidden Role of Chance in the Markets and in Life_ . London, U.K.: Penguin Books, 2004. 

- [26] E. Keogh _et al_ ., “Compression-based data mining of sequential data,” _Data Min. Knowl. Discov._ , vol. 14, no. 1, pp. 99–129, 2007. 

- [27] D. Hand, “Classifier technology and the illusion of progress,” _Statist. Sci._ , vol. 21, no. 1, pp. 1–14, 2006. 

- [28] M. Markou and S. Singh, “Novelty detection: A review - Part 1: Statistical approaches,” _Sig. Process._ , vol. 83, no. 12, pp. 2481–2497, 2003. 

- [29] T. Fawcett, “An introduction to ROC analysis,” _Pattern Recognit. Lett._ , vol. 27, no. 8, pp. 861–874, Jun. 2006. 

- [30] M. Zhao and V. Saligrama, “Anomaly detection with score functions based on nearest neighbor graphs,” in _Proc. NIPS_ , 2009, pp. 2250–2258. 

- [31] S. Axelsson, “The base-rate fallacy and the difficulty of intrusion detection,” _ACM TISSEC_ , vol. 3, no. 3, pp. 186–205, Aug. 2000. 

- [32] M. Riveiro, “Visual analytics for maritime anomaly detection,” PhD thesis, Örebo Univ., Sweden, 2011. 

- [33] Y. Bu, L. Chen, and D. Wai-Chee Fu, A. Liu, “Efficient anomaly monitoring over moving object trajectory streams,” in _Proc. 15th ACM SIGKDD_ , New York, NY, USA, 2009. 

- [34] A. Gammerman and V. Vovk, “Hedging predictions in machine learning,” _Comput. J._ , vol. 50, no. 2, pp. 151–163, 2007. 

- [35] G. Shafer and V. Vovk, “A tutorial on conformal prediction,” _J. Mach. Learn. Res._ , vol. 9, pp. 371–421, Mar. 2008. 

- [36] D. Hawkins, _Identification of Outliers_ . New York, NY, USA: Chapman Hall, 1980. 

- [37] E. Eskin, “Anomaly detection over noisy data using learned probability distributions,” in _Proc. 17th ICML_ , San Francisco, CA, USA, 2000. 

- [38] R. Laxhammar and G. Falkman, “Conformal prediction for distribution-independent anomaly detection in streaming vessel data,” in _Proc. 1st Int. Workshop StreamKDD_ , New York, NY, USA, 2010. 

- [39] S. Russel and P. Norvig, _Artificial Intelligence: A Modern Approach_ , 2nd ed. Upper Saddle River, NJ, USA: Pearson Education, 2003. 

- [40] R. Duda and P. Hart, _Pattern Classification and Scene Analysis_ . New York, NY, USA: Wiley, 1973. 

- [41] M. Goodrich and R. Tamassia, _Data Structures and Algorithms in Java_ . New York, NY, USA: Wiley, 1998. 

Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on September 11,2026 at 17:32:55 UTC from IEEE Xplore.  Restrictions apply. 

LAXHAMMAR AND FALKMAN: ONLINE LEARNING AND SEQUENTIAL ANOMALY DETECTION IN TRAJECTORIES 

1173 

- [42] D. Pokrajac, A. Lazarevic, and L. Latecki, “Incremental local outlier detection for data streams,” in _Proc. IEEE Symp. CIDM_ , Honolulu, HI, USA, 2007. 


![](Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories_images/Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories.pdf-0016-03.png)


**Rikard Laxhammar** received the Ph.D. degree in computer science at University of Skövde, Skövde, Sweden, in 2014. He is employed by Saab AB, Järfälla, Sweden, since 2007, where he works as a software engineer. His main research interests are machine learning and anomaly detection. In his previous research, he has investigated different algorithms for anomaly detection in trajectory data. 


![](Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories_images/Online_Learning_and_Sequential_Anomaly_Detection_in_Trajectories.pdf-0016-05.png)


**Göran Falkman** received the Ph.D. degree in computing science from Chalmers University of Technology, Sweden, in 2003. He holds a position as an Associate Professor in Computer Science, with a speciality in interactive knowledge systems, at the University of Skövde, Skövde, Sweden, where he works as a Researcher at the Informatics Research Centre. His current research interests include intersection of applied artificial intelligence, knowledge systems, interaction design, and information fusion. This includes work on the design, implementation, and use of formal knowledge representation and knowledge-based systems, as well as the use of interactive visualization for supporting knowledge-based reasoning processes. 

▷ **For more information on this or any other computing topic, please visit our Digital Library at** www.computer.org/publications/dlib. 

Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on September 11,2026 at 17:32:55 UTC from IEEE Xplore.  Restrictions apply. 

