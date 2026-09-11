Reliability Engineering and System Safety 267 (2026) 111890 


![](Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems_images/Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems.pdf-0001-01.png)


Contents lists available at ScienceDirect 

# Reliability Engineering and System Safety 

journal homepage: www.elsevier.com/locate/ress 


![](Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems_images/Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems.pdf-0001-05.png)


## Quantifying and mitigating alarm fatigue caused by fault detection systems 


![](Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems_images/Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems.pdf-0001-07.png)


Abdoul Rahime Diallo<sup>a,*</sup> , Lazhar Homri<sup>a</sup> , Thomas Boeuf<sup>b</sup> , Jean-Yves Dantan<sup>a</sup> , Fr´ed´eric Bonnet<sup>b</sup> 

a _Arts et Metiers Institute of Technology, Universit_ ´ _e de Lorraine, LCFC, Metz F-57070, France_ b _ArcelorMittal Maizi_ ` _eres Research, Voie Romaine, Maizi_ ` _eres-l_ ` _es-Metz 57240, France_ 

|A R T I C L E I N F O|A B S T R A C T|
|---|---|
|_Keywords:_|Data-driven methods for detecting faults have attracted considerable interest within the scientifc community.|
|Process monitoring<br>Fault detection<br>Conformal prediction<br>Evaluation metrics<br>False discovery rate|<br>One of the challenges in applying these methods in industry remains the scarcity of faulty data. While this<br>constraint is considered during model training, it is rarely taken into account during evaluation. This study<br>demonstrates that the most commonly used evaluation metrics, namely false alarm rate (FAR) and fault detection<br>rate, are insuffcient to assess a key phenomenon known as the cry-wolf effect. This effect, caused by repeated<br>false alarms, erodes operator trust and vigilance, ultimately leading to alarm fatigue and reducing the usability of<br>detection systems over time. To address this limitation, we propose the false discovery rate (FDR) as a quanti-<br>tative indicator of the cry-wolf effect. Furthermore, we introduce a methodology based on FDR control to<br>mitigate this phenomenon. The benefts of this approach are demonstrated on both an academic benchmark, the<br>Tennessee Eastman Process (TEP), and an industrial case study involving a galvanizing line.|



### **1. Introduction** 

Customer satisfaction is a key factor in an industrial context characterized by intense competition among companies. This requires delivering products that meet customer expectations in terms of quality. Achieving this goal necessitates the early detection of quality issues and faults in the production system. Various data-driven methods, from statistical process control techniques to deep learning models, have been proposed in the literature for this purpose. The development of these methods for industrial deployment typically involves two main phases: model training using historical data, followed by model evaluation. 

The greatest challenge during the training phase remains the scarcity of faulty data [1]. Preventive maintenance and regular sensor recalibration have further reduced fault occurrence [2]. Three main approaches have been proposed to address this issue. The first, and most common, relies exclusively on normal operating conditions (NOC) data. Early examples include univariate control charts and multivariate control charts such as the Hotelling chart. With the increasing number of sensors, dimension reduction methods such as principal component analysis (PCA) were developed [3]. Other dimension reduction methods such as partial least squares, which take into account the impact on product quality, have also been used for fault detection [4]. The autoencoder (AE) was then proposed by Kramer as a non-linear version 

of PCA [5]. Numerous variants have since been introduced to account for process non-linearity and temporal dynamics. Other semi-supervised methods trained on NOC data include isolation forest [6] based on decision trees and the One-class support vector machine [7]. The second approach is transfer learning [8–10], where models are pre-trained on generic labeled data and fine-tuned with limited fault data. The third involves data augmentation and resampling for imbalanced datasets [2, 11,12]. Simulation also provides labeled data when system models are available [1,13], enabling both supervised training and the demonstration of the three previous approaches. 

Although many studies have focused on the first phase of development, the second phase, namely model evaluation, has received comparatively less attention [14–16]. This gap has important consequences, as it leads to biased comparisons between proposed detection techniques [14]. The present work addresses this issue by examining model evaluation in contexts characterized by strong imbalance between the probability of normal operation and that of fault occurrence. In practice, the effectiveness of models is often demonstrated using simulation data. Yet, even when training relies solely on normal operating conditions (NOC) data, this imbalance is rarely reflected at the evaluation stage, since NOC and fault datasets are typically constructed with comparable sample sizes. We show that this artificial balance significantly distorts model evaluation. Furthermore, we demonstrate 

* Corresponding author. 

_E-mail address:_ abdoul-rahime.diallo@ensam.eu (A.R. Diallo). 

https://doi.org/10.1016/j.ress.2025.111890 Received 10 June 2025; Received in revised form 20 September 2025; Accepted 31 October 2025 Available online 4 November 2025 

0951-8320/© 2025 Elsevier Ltd. All rights are reserved, including those for text and data mining, AI training, and similar technologies. 

> _A.R. Diallo et al.                                                                                                                                                                                                                                Reliability Engineering and System Safety 267 (2026) 111890_ 

that the most commonly used performance criteria in this phase, namely the fault detection rate and the false alarm rate (FAR) [17–19], are insufficient to ensure the acceptability of detection models to end users. 

They do not capture the so-called cry-wolf effect. This effect was first introduced by Breznitz (1984) [20], who demonstrated that repeated false alarms can induce physiological and behavioral changes such as reduced vigilance. Later experiments investigated operator responses under different levels of alarm reliability, defined as the proportion of alarms that correctly signal the presence of a true event. Participants performed demanding tasks while exposed to alarms of varying reliabilities and urgencies. The results showed that most participants adjusted their response behavior to the expected probability of true alarms, a strategy known as probability matching, while some adopted extreme all-or-none strategies [21]. Similar results were reported by Getty et al. (1995) [22]. These findings indicated that degraded alarm response speed, frequency, and accuracy are the main manifestations of the cry-wolf effect. This interpretation differed from the earlier model of Pat´e-Cornell (1986) [23], which predicted that alarm mistrust would simply stop responses altogether [24]. Bliss & Dunn (2000) [24] extended this research by showing that alarm response performance degrades further under high workload, and that operators tend to probability-match their responses to the perceived reliability of the system. Together, these studies provide strong empirical evidence that repeated false alarms erode trust and vigilance. The cry-wolf effect has also been documented in healthcare alarm systems. In patient monitoring and diabetes alert systems, frequent false alarms have been shown to cause desensitization and delayed responses to true alarms [25,26]. In fault detection, the cry-wolf effect is particularly critical. As we demonstrate in Section 4, when faults are rare, false alarms can outnumber true alarms even for models with high detection rates and low FAR. This highlights the severity of relying solely on FAR and fault detection rate in sparse fault scenarios, since these metrics do not capture the disproportionate impact of false alarms under class imbalance. 

Although related, the cry-wolf effect and alarm flooding (also called alarm overload) describe different phenomena. In the literature, alarm flooding is defined as episodes in which the alarm rate exceeds human handling capacity over short intervals [27–29]. Alarm flooding can result in catastrophic outcomes, such as explosions and substantial costs [30]. Prior work reports floods with several hundred alarms within minutes during upsets and shows adverse cascading effects on plant operation. Benchmarks suggest that operators can handle about 10 to 11 alarms per 10 min [28]. We distinguish this quantitative notion from the cry-wolf effect, which arises from low alarm reliability when faults are rare. 

A consolidated view of alarm flooding mitigation in process industries can be found in three surveys [27,28,31]. At design time, work focuses on configuration quality: alarm rationalization and prioritization; removal of redundant and nuisance alarms; tuning of dead bands and delay timers; and state- or mode-based alarming. Reported techniques include statistical clustering of alarm populations, time-series analysis for band and timer setting, and Markov or probabilistic models to compute expected dead bands and delays. During operation, the aim is early recognition and containment of floods. Techniques include online or early-stage flood classification, streaming classifiers, and workflow or operator-support models that route attention under load. A third-stream mines alarm logs to discover flood motifs and causal structure. Methods include sequence alignment, frequent itemset mining, sequential pattern discovery such as PrefixSpan, association-rule learning, and causal connectivity analyses based on transfer entropy or related measures. 

Other studies very close to ours, particularly in relation to the mitigation of the cry-wolf effect, adapt or dynamically adjust detection thresholds to reduce false alarms. Examples include adaptive limits on the SPE or on the T² of Hotelling for PCA [32,33] and dynamic thresholds on autoencoder reconstruction error [34]. Kaced et al. (2021) [30] proposed a related approach where alarm activation is conditioned not 

only on the PCA statistics but also on a nonlinear combination of alarm duration and deviation, followed by a delay timer. This design significantly reduced nuisance alarms while preserving fault sensitivity in a cement process case study. While these works are close in spirit, our objective differs. We use the false discovery rate (FDR) as the primary criterion and control it at each prediction. The idea of monitoring the proportion of false discoveries was first introduced by Sori´c (1989) [35], who showed that controlling only the false positive rate is insufficient when many decisions are made, since the proportion of false discoveries among all discoveries may still be large. Benjamini & Hochberg (1995) [36] subsequently proposed a practical procedure to control this criterion. In our setting, discoveries correspond to detected faults, and the FDR expresses the expected proportion of false alarms among all declared faults. This provides an interpretable and scalable measure of alarm reliability, particularly relevant in fault detection where faults occur with low probability compared to normal operation. 

Building on these insights, we therefore propose to combine the fault detection rate and the FAR with the FDR. 

Thus, this article investigates the quantification and the mitigation of alarm fatigue, with a particular focus on the cry-wolf effect in fault detection. To guide this investigation, we address the following research questions: 

- Which indicators are currently used to evaluate fault detection models? 

- Do these indicators adequately capture the cry-wolf effect? 

- If not, how can the cry-wolf effect be quantified more appropriately? 

- How can the cry-wolf effect be mitigated in practice? 

The main contributions of this article can be summarized as follows: 

- A review of the evaluation indicators most commonly used for fault detection models, with an emphasis on their limitations in capturing the cry-wolf effect. 

The introduction of the FDR as a relevant metric for quantifying the cry-wolf effect in fault detection. 

- A method for controlling FDR at each prediction, providing a practical strategy to mitigate the cry-wolf effect. 

Consequently, the rest of this article is organized as follows. Section 2 recalls the basic principle of dimension reduction methods for fault detection, illustrated with PCA and AE methods, which serve as illustrative tools in our case studies. Section 3 provides a brief literature review of evaluation metrics used for fault detection. Section 4, highlights the limitations of the most commonly used evaluation criteria and motivates the usefulness of the FDR. 5 presents our method for reducing the risk of the cry-wolf effect by controlling FDR. Section 6 reports results on an academic case study and an industrial application. Section 7 concludes the article with a discussion and perspectives for future work. 

### **2. Background on dimension reduction methods for fault detection** 

These methods are also known as latent variable models [4] as well as reconstruction methods. Two families of approaches can be distinguished. In the first family, dimension reduction is supervised by one or more variables related to the quality of the product, as in partial least squares. In the second family, dimension reduction is unsupervised. Examples of techniques in this family include PCA, independent component analysis or AE. Numerous variants of these models have been proposed in the literature to better address non-linearity, dynamics and noise in the data. In this study, we focus on PCA and AE as representative linear and nonlinear approaches. PCA has long been widely used in industrial monitoring applications and remains a reference method in 

2 

> _A.R. Diallo et al.                                                                                                                                                                                                                                Reliability Engineering and System Safety 267 (2026) 111890_ 

practice [30]. It is also the standard baseline on the Tennessee Eastman Process. AE is included as a flexible nonlinear alternative that is also increasingly adopted in industrial monitoring applications [37,38]. 

The implementation of PCA and AE for fault detection and diagnosis follows a four-step procedure, illustrated in Fig. 1. 

First, the dimension reduction model is trained. This stage often includes a data transformation phase prior to model training. PCA, for example, requires centered and, if necessary, reduced data. Standardization is therefore applied before PCA training. Second, a detection index is selected. This index can be defined either in the reduced space, or in the reconstruction space, or as a combination of the two. The two most common indices are Hotelling’s T<sup>2</sup> in the reduced space and the reconstruction error [37–39]. Third, a detection threshold is set. To this end, the distribution of the detection index for NOC data is either estimated empirically or assumed to follow a known distribution. The threshold is then defined as the quantile of the distribution associated with a risk _α_ of FAR, corresponding to the probability that the model wrongly signals a fault. Finally, fault diagnosis is performed to locate the faulty variables in the production system. This last step is not considered in this work. In the remainder of this section, we detail the PCA and AE training process used in this article. 

PCA is a dimensionality reduction technique that transforms the original data into a new coordinate system, where the axes, referred to as principal components, correspond to the directions of maximum variance. These components are mutually orthogonal and uncorrelated. 

The implementation begins by standardizing the training data and computing its covariance matrix. An eigenvalue decomposition of this matrix yields two key matrices: an orthogonal matrix _P_ , known as the loading matrix, which contains the principal components expressed in the original feature space, and a diagonal matrix Λ of eigenvalues, each representing the variance captured by the corresponding principal component. 

Although the number of principal components equals the number of original variables, in practice, especially for fault detection purposes, it is crucial to retain only a subset of components that capture the most significant variance. Several standard criteria guide this selection: cumulative explained variance, parallel analysis, the scree plot method, and the Prediction Residual Sum of Squares (PRESS) statistic [40]. 

After selecting the optimal number _k_ of components, one constructs the reduced matrices _Pk_ and Λ _k_ , which contain only the retained principal directions and their associated variances. These are used to calculate two monitoring statistics for each sample: 

- Hotelling’s T² statistic, which measures the projection of a sample onto the retained principal subspace; 

- Reconstruction error or squared prediction error (SPE) also known as Q-statistic, which quantifies the residual variance not explained by the selected components. 


![](Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems_images/Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems.pdf-0003-10.png)


|and_λj _are the trace of the matrixΛsuch that:|
|---|




![](Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems_images/Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems.pdf-0003-12.png)



![](Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems_images/Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems.pdf-0003-13.png)


An AE is a neural network architecture designed to learn efficient representations of input data through unsupervised learning. Its primary goal is to reconstruct the input data after compressing it into a lowerdimensional latent space. Throughout this work, all input variables are standardized (per feature, zero mean and unit variance computed on the training data) to ensure scale consistency and stable optimization. The model consists of two components: an encoder and a decoder. 

The encoder maps each input sample _x_ ∈ R<sup>_m_</sup> to a lowerdimensional representation _z_ = _f_ ( _x_ ) ∈ R<sup>_k_</sup> , where _k < m_ , using a non-linear transformation _f_ . The decoder attempts to reconstruct the original input from this latent representation by applying a non-linear function _g_ , yielding _x_ = _g_ ( _z_ ) ∈ R<sup>_m_</sup> . 

The encoder and decoder are jointly trained by minimizing a reconstruction loss function. Among the most commonly employed loss functions is the mean squared error: 


![](Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems_images/Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems.pdf-0003-17.png)


The reconstruction error, also referred to as the SPE, serves as a key detection index in AE-based monitoring systems. For a given input sample _xi_ , the SPE is computed as the squared Euclidean norm between the input and its reconstruction: _SPE_ ( _xi_ )= ‖ _xi_ − _xi_ ‖<sup>2</sup> (7) 


![](Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems_images/Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems.pdf-0003-19.png)


**Fig. 1.** Training process of dimension reduction models for fault detection and diagnosis. 

3 

> _A.R. Diallo et al.                                                                                                                                                                                                                                Reliability Engineering and System Safety 267 (2026) 111890_ 

In analogy with PCA, some studies also introduce a T²-like statistic computed in the latent space [37,38]. It is defined as: 


![](Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems_images/Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems.pdf-0004-02.png)


where _zi_ = _f_ ( _xi_ ), _Z_ and Σ are the mean and the covariance matrix of the latent representations over the training data. In some works, this index is alternatively denoted as H² and may also be defined simply as the Euclidean norm of _zi_ in latent space. Unlike PCA, which relies on parametric assumptions to derive detection thresholds, AE-based detection generally employs non-parametric approaches. In particular, kernel density estimation is widely used to estimate the distribution of the detection index under NOC. 

### **3. Overview of evaluation metrics in the fault detection literature** 

In this section, we provide an overview of the performance indicators used to evaluate fault detection models in 32 studies. The focus is on models employing only data from normal operation during training, with particular interest in recently published papers and seminal articles from the early 2000s. For each article, the case study and the metrics used are indicated. Below, we outline the methods used to calculate the main indicators found in these papers. We have adopted the convention given in Table 1. Process operation under normal conditions is considered to be the negative class, while faults are considered to be the positive class. 

In this context, the first indicator we can calculate is the FAR: 


![](Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems_images/Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems.pdf-0004-07.png)


A second frequently encountered indicator is the fault detection rate. To avoid confusion in this article with the False Discovery Rate (FDR), we will use the abbreviation TPR (for True Positive Rate, its equivalent used in some communities). However, in the text we will continue to use the term fault detection rate, which is more widely used in the process monitoring community. It is calculated by: 


![](Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems_images/Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems.pdf-0004-09.png)


From time to time, its complementary Missed Detection Rate (MDR) is encountered: 


![](Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems_images/Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems.pdf-0004-11.png)


The complementary of the FAR can also be encountered much more rarely: 


![](Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems_images/Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems.pdf-0004-13.png)


One of the indicators that can be calculated from the confusion matrix is precision. It quantifies the proportion of true alarms among all alarms triggered. It is the complement of the FDR: 


![](Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems_images/Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems.pdf-0004-15.png)


The F1-score combines fault detection rate and precision. It is defined as their harmonic mean: 

#### **Table 1** 

Confusion matrix for a predictor. 

|||Prediction<br>Positive|Negative|
|---|---|---|---|
|Actual|Positive|True Positive (TP)|False Negative (FN)|
||Negative|False Positive (FP)|True Negative (TN)|




![](Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems_images/Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems.pdf-0004-20.png)



![](Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems_images/Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems.pdf-0004-21.png)


Several synonyms are sometimes used to designate the same indicator. To facilitate analysis, we have decided to use just one. This has been done while ensuring that these synonyms do indeed designate the same indicator. We have also chosen to consider the Average Run Length during normal process operation (ARL0), which is the average time (or number of samples) before the occurrence of a false alarm, as a synonym for FAR. However, this subjective choice has very little influence on the results, since ARL0 appears in only one study. ARL1, which is the equivalent of ARL0 when a fault occurs, was grouped with Detection Time Delay (DTD). The synonyms considered for each indicator are given in Table 2. Details of the evaluation metrics for each item and the case study are given in Table 3. 

Fig. 2 shows the total occurrence of each indicator. We have chosen to group together FAR and its complement, as well as the fault detection rate and MDR. The receiver operating characteristic (ROC) curve and the area under the curve (AUC) calculated from the ROC curve were counted together. 

It can be noticed that the fault detection rate (with its complement MDR) is the most frequently used indicator. It appears in 29 of the 32 articles considered. In the three articles where it does not appear, it is supplanted by control charts in two articles and by DTD in the third. FAR (with its complement) is the second most widely used. It appears in 25 articles, where it is always accompanied by the fault detection rate. There are also 7 indicators that appear only once. These include precision, indicators relating to training time, inference time, storage space required and two indicators combining several others. This is the case for the pre-alarm rate (PAR) proposed by Cheng et al. (2019) [71] which combines FAR and MDR: 


![](Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems_images/Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems.pdf-0004-25.png)


where _Y_ ∈[0 _,_ 1] determines the tradeoff between the FAR and the fault detection rate. In Lakshmi Priya Palla & Kumar Pani (2023) [53] where this metric was used, _Y_ is set to 0.6 meaning that the fault detection rate was considered to be more important than the FAR. The second indicator that combines other metrics is _J_ : 


![](Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems_images/Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems.pdf-0004-27.png)


where RFAR, RMDR and RDTD are the targeted values for FAR, MDR, and DTD respectively, _w_ 1, _w_ 2, and _w_ 3 are the weights of each of the indicators. In Kaced et al. (2021) [30] where that metric was used, the three indicators were considered to be equally important, hence _w_ 1 = _w_ 2 = _w_ 3 = 1 _._ 

#### **Table 2** 

Standardization and grouping of indicators. 

|FAR|TPR|MDR|DTD|
|---|---|---|---|
|False alarm rate,<br>False detection<br>rate,<br>ARL0|Fault detection<br>rate,<br>True positive<br>rate,<br>Detection rate,<br>Recall|Missed detection<br>rate,<br>Non-detection<br>rate,<br>Missed alarm<br>rate|ARL1<br>Detection Time Delay<br>(DTD),<br>Detection time,<br>Fault detection delay,<br>Time of frst<br>detection,<br>Average alarm delay,<br>Detection latency,<br>Detection delays|



4 

_Reliability Engineering and System Safety 267 (2026) 111890_ 

The ROC curve and AUC were found in two studies, and in one of them both measures were present. The ROC curve is used to represent the trade-off between TPR and FAR, starting from a very high threshold for which there are no false alarms but also for which no occurrence of the fault has been detected, to a very low threshold for which all occurrences of the fault have been detected. It is therefore first and foremost a tool for setting the detection threshold before being an evaluation metric. It is very often associated with the AUC, which calculates the area under the ROC curve. The AUC assigns the same weight to the detection of a fault as to the triggering of a false alarm, whereas in reality these two situations rarely have the same cost. Depending on the field of application, one may be more important than the other. For example, a survey revealed that patients and healthcare professionals would be prepared to accept an extra 2250 false positives for one more true cancer detection [72]. In fault detection, on the other hand, the risk of false alarms is usually set at 1 % and 5 %. Furthermore, according to Hand (2009) [73], using the AUC to compare two models is unfair because the AUC uses two different cost distributions for the two models. 

#### **Table 3** 

Overview of evaluation metrics used in the literature. 

|Article|Case study|Evaluation metric|the trade-off between TPR and FAR, starting from a very high threshol<br>f hih h   fl l b l f hih|
|---|---|---|---|
|[42]|Vinyl acetate monomer process|FAR, TPR|or wc tere are no ase aarms ut aso or wc no occurrence<br>|
|[43]|<br>TEP, wastewater treatment process<br>(WWTP)<br>|<br>FAR, TPR|the fault has been detected, to a very low threshold for which all oc<br>currences of the fault have been detected. It is therefore frst and fore|
|[44]|Coal-fred power units, thyroid dataset,<br>magic dataset, electrical dataset, motor<br>d|TPR, TNR, G-mean|<br>most a tool for setting the detection threshold before being an evaluatio<br>metric. It is very often associated with the AUC, which calculates th|
|[45]|ataset<br>TEP|FAR, TPR, DTD|area under the ROC curve. The AUC assigns the same weight to th<br>|
|[46]|ethanol-water mixture distillation<br>|<br>FAR, TPR, Precision, F1-|detection of a fault as to the triggering of a false alarm, whereas in realit<br>|
||column, Three-Phase fow facility|score|these two situations rarely have the same cost. Depending on the feld o|
|[17]|TEP|FAR, TPR, AUC, ROC|<br>application, one may be more important than the other. For example,|
|[47]|CSTR|FAR, TPR|ld h  d hlh fl ld b|
|[48]|TEP, Cement plant|<br>FAR, MDR, DTD, gained<br>execution time, storage|survey reveae tat patients an eatcare proessionas wou<br>prepared to accept an extra 2250 false positives for one more true cance<br>|
|||space|detection [72]. In fault detection, on the other hand, the risk of fals|
|[49]|TEP, cement clinker production process|FAR, TPR|alarms is usually set at 1 % and 5 %. Furthermore, according to Han|
|[50]<br>|TEP<br>|TPR, F1-score, DTD<br>|(2009) [73], using the AUC to compare two models is unfair because th|
|[51]|catalytic rod, snap curing oven|FAR, TPR, DTD|AC   diff  diibi f h  dl|
|[52]|TEP tail gas treatment process|MDR|U uses two erent cost strutons or te two moes.|
|[53]|,<br>Multiphase fow system|FAR, MDR, PAR|Precision, which is the complement to FDR, has only been used by A|
|[54]|<br>TEP|FAR, TPR, DTD|et al. (2025) [46]. However, the imbalance between normal operatin|
|[55]|TEP|TPR|conditions and occurrence of faults was not taking into account. Firstly|
|[56]|TEP, Fed-batch fermentation penicillin<br>process, manufacturing process of<br>conveyor belt|FAR, TPR, ROC|<br>the FAR is calculated by fault. Then, for the three faults for which faul<br>simulation details are provided, there is one for which there is a balanc|
|[57]|<br>TEP|FAR, TPR, F1-score|between NOC and faulty data, one for which there are 600 NOC sample|
|[58]|Case Western Reserve University bearing|FAR, TPR, G-mean|and 400 faulty samples while for the third fault, there are far more fault|
||dataset, the Intelligent Maintenance<br>System bearing datasets, TEP||samples than NOC samples. In fact, there are 1875 NOC sample<br>|
|[59]|<br>TEP|FAR TPR|compared with 7216 faulty samples.|
|[60]|TEP|,<br>TPR, training time, time|In the next section, we will take a closer look at fault detection rate<br>|
|||consumption|and FAR, the most widely used indicators.|
|[61]|TEP, CSTR|FAR, TPR||
|[30]|Cement Plant|FAR, MDR, DTD, J||
|||<br>|**4Limitations of common evaluation criteria and motivation for**|
|[62]|Pump system|charts|**. **<br>|
|[63]|TEP|FAR, TPR|**FDR**|
|[64]|TEP, CSTR|FAR, TPR||
|[65]<br>|TEP<br>|FAR, TPR<br>|As discussed in the introduction, repeated false alarms can erod|
|[19]<br>[66]|TEP<br>TEP semiconductor etch process|FAR, TPR<br>FAR TPR DTD|operator trust and vigilance, a phenomenon known as the cry-wolf ef|
|[67]|,<br>WWTP, TEP, semiconductor etch process|, ,<br>FAR, TPR|fect. Traditional metrics such as the FAR and the fault detection rate d<br>|
|[68]|WWTP|charts|not capture this risk. To illustrate this limitation, it is suffcient to sho|
|[69]<br>|CSTR|DTD|that these two criteria can appear optimal while still allowing condition|
|[70]|TEP|FAR, MDR, DTD|under which the cry-wolf effect emerges.|



Precision, which is the complement to FDR, has only been used by Ali et al. (2025) [46]. However, the imbalance between normal operating conditions and occurrence of faults was not taking into account. Firstly, the FAR is calculated by fault. Then, for the three faults for which fault simulation details are provided, there is one for which there is a balance between NOC and faulty data, one for which there are 600 NOC samples and 400 faulty samples while for the third fault, there are far more faulty samples than NOC samples. In fact, there are 1875 NOC samples compared with 7216 faulty samples. 

In the next section, we will take a closer look at fault detection rates and FAR, the most widely used indicators. 

As discussed in the introduction, repeated false alarms can erode operator trust and vigilance, a phenomenon known as the cry-wolf effect. Traditional metrics such as the FAR and the fault detection rate do not capture this risk. To illustrate this limitation, it is sufficient to show that these two criteria can appear optimal while still allowing conditions under which the cry-wolf effect emerges. 

Let us consider a hypothetical “perfect” (in terms of FAR and fault detection rate) detection model such as a PCA or an AE trained only with NOC data. The detection threshold of this model is set as explained in 


![](Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems_images/Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems.pdf-0005-10.png)


**Fig. 2.** Number of occurrences of the evaluation metrics. 

5 

> _A.R. Diallo et al.                                                                                                                                                                                                                                Reliability Engineering and System Safety 267 (2026) 111890_ 

Section 2. This model is then deployed in industry and retains the same performance as when it was evaluated off-line, with a perfect fault detection rate (TPR=100 %) and an FAR in production equal to the risk α. An alarm is triggered each time the model detects a fault. The cry-wolf effect occurs when the model triggers several alarms to warn of the occurrence of a fault and, after each check, operators find that the production system is operating normally. Therefore, one measure of the cry-wolf effect is the probability of the production system being in normal operating conditions given that an alarm has been triggered. The event “The production system is in normal operating conditions” is denoted as NOC and the event “An alarm has been triggered” is denoted as A. The probability of a false alarm is therefore P( _A_ | _NOC_ ) while the probability of a real fault being detected is P( _A_ | _NOC_ ). The risk of the cry-wolf effect is P( _NOC_ | _A_ ) and can be calculated using Bayes’ theorem: 


![](Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems_images/Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems.pdf-0006-02.png)


By breaking down the probability of an alarm being triggered, (18) can be rewritten as follows: 


![](Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems_images/Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems.pdf-0006-04.png)



![](Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems_images/Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems.pdf-0006-05.png)


The measurement of the cry-wolf effect now depends solely on the probability of a false alarm, the probability of detecting a fault or a defect, and the imbalance _r_ . Accordingly, _Fig. 3_ illustrates the cry-wolf effect for the hypothetical “perfect” model defined above. Two scenarios are considered, where the probability of a false alarm is 1 % and 5 %, respectively. 

Fig. 3 demonstrates the following: 

The imbalance _r_ significantly impacts the cry-wolf effect. When the production system is equally likely to operate under normal conditions as it is to experience faults, the cry-wolf effect is very low. In such cases, the cry-wolf effect measurement is even slightly lower than _α_ , and the FAR serves as a good approximation of it. However, when the imbalance is pronounced, as is typically observed in industrial reality, the cry-wolf effect measurement far exceeds the FAR. This underscores the necessity 

of considering imbalance when evaluating detection models. 

In the region of the curve where _r_ is low, corresponding to the context of this study, even though the model detects every fault and the FAR is optimal, the risk of the cry-wolf effect remains very high. This illustrates that these two criteria alone are insufficient for assessing detection models intended for industrial deployment. 

The probability of the process being in normal operating conditions given that an alarm has been triggered is equivalent to the FDR introduced by Benjamini & Hochberg (1995) [36] in the context of multiple comparisons. It is therefore referred to as such in the remainder of this article. 

### **4. Controlling the false discovery rate to mitigate the cry-wolf effect** 

The measure of the cry-wolf effect adopted in this study is defined as the ratio of false alarms to the total number of alarms triggered. Therefore, as a first step in reducing the cry-wolf effect, the numerator can be reduced by ensuring that the empirical FAR does not exceed the predefined risk level. However, this condition alone is not sufficient to prevent the cry-wolf effect. As previously shown, even a “perfect” model can still generate the cry-wolf effect. Therefore, a second step involves the application of p-value adjustment techniques aimed at controlling the FDR. For this stage, it is necessary to use p-values and a statistical test rather than a detection threshold on the detection index. For PCA, where the theoretical distribution of T² and SPE are known, the p-value for each sample _x_ can be calculated as follows: 


![](Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems_images/Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems.pdf-0006-14.png)


where _F_ is the Cumulative Distribution Function (CDF) of the detection index and _s_ ( _x_ ) is the value of the detection index of the sample _x_ . However, in the case of AE and other fault detection models, the theoretical distributions of the detection indices remain unknown. Therefore, we rely on conformal prediction throughout the remainder of this article. This framework enables the computation of p-values for any fault detection model without requiring strong distributional assumptions [74]. Specifically, it only assumes that the calibration data and the future NOC data are independent and identically distributed [75]. Moreover, some theoretical guarantees of this approach remain valid 


![](Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems_images/Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems.pdf-0006-16.png)


**Fig. 3.** Quantifying the cry-wolf effect of a perfect detection model. 

6 

> _A.R. Diallo et al.                                                                                                                                                                                                                                Reliability Engineering and System Safety 267 (2026) 111890_ 

under the weaker assumption of exchangeability between the calibration and normal data sets [76]. Calibration data are a part of the training data that are not used to train the detection model and are used to calculate the p-value of any new sample. For any detection index for which the higher the value of a sample, the higher the probability that the sample is a fault, the p-value of any sample _x_ is calculated as follows: 


![](Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems_images/Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems.pdf-0007-02.png)


where _Xcalib_ are the calibration data, _n_ is the number of calibration samples. Any sample _x_ is considered as a fault by the fault detection system if: 


![](Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems_images/Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems.pdf-0007-04.png)


By proceeding in this way, the conformal prediction guarantees that for any sample _x_ belonging to the NOC data: P[ _p_ ( _x_ ) ≤ _α_ ] ≤ _α._ (23) 

However, this guarantee is only marginally valid, i.e. it is only valid on average. A higher probability of obtaining a false alarm rate lower than the risk _α_ can be obtained by using the proposal of Bates et al. (2023) [75]. This involves adjusting the p-values to obtain a conditional guarantee on the FAR, which can be written as follows for any _δ_ ∈(0 _,_ 1) and for any sample belonging to the NOC data: 


![](Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems_images/Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems.pdf-0007-07.png)


where _p_<sup>ʹ</sup> ( _x_ ) is the adjustment of _p_ ( _x_ ). To perform this adjustment, it is _h_ sufficient to determine a piecewise constant function defined by Bates et al. (2023) [75]: 

_h_ ( _t_ ) = _b_ ⌈( _n_ +1) _t_ ⌉ (25) 

where the real _bi_ are chosen on the one hand such that _b_ 0 = 1, _bn_ +1 = 1, 0 ≤ _b_ 1 ≤ _b_ 2 ≤ _…_ ≤ _bn_ ≤ 1 and on the other hand such that for _U_ 1 _, …, Un_ ∼ _Unif_ ([0 _,_ 1]) with order statistics _U_ (1) ≤ _U_ (2) ≤ _…_ ≤ _U_ ( _n_ ), we have: 


![](Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems_images/Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems.pdf-0007-11.png)


Thus, we can adjust the p-value associated with a sample _x_ by _p_<sup>ʹ</sup> ( _x_ ) = _h_ ( _p_ ( _x_ )). Several approaches can be used to construct the _bi_ sequence. A first one is to use the upper bound of the Dvoretzky-Kiefer-Wolfowitz (DKW) inequality [77]: 


![](Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems_images/Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems.pdf-0007-13.png)


where _C_ = 2 as shown by Massart (1990) [78]. Another possible approach is to exploit generalized Simes inequality [75,79]: 


![](Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems_images/Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems.pdf-0007-15.png)


where _k_ = ⌈ _n/_ 2⌉ for the specific case of anomaly detection [75]. Both approaches effectively control the FAR, but can be very conservative, providing a FAR well below the risk _α_ , but at the expense of the fault detection rate. An asymptotic approach can be used, which is much less conservative, but whose guarantee is only valid with a very large calibration data size [75,80]: 


![](Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems_images/Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems.pdf-0007-17.png)


The aim of this first adjustment step was to ensure that the FAR is less than or equal to the risk _α_ . A second adjustment step is necessary this time to ensure that the FDR is below a predefined threshold _q_ . One 

possible approach is the Benjamini-Hochberg procedure [36]. Given _m_ p-values _p_ 1 _, p_ 2 _,_ ⋯ _, pm_ the first step in this procedure is to arrange them in ascending order such that _p_ (1) _< p_ (2) ≤ ⋯ ≤ _p_ ( _m_ ). Next, find _j_ such that: 


![](Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems_images/Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems.pdf-0007-20.png)



![](Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems_images/Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems.pdf-0007-21.png)


the sample associated with _p_ ( _i_ ) is considered as faulty if _p_ ( _i_ ) ≤ _q_ . By proceeding in this way, the FDR, in average, will be less than or equal to _q_ . 

As described in Section 2 , the first two steps concern the training of the detection model and the choice of a detection index. Building on these foundations, Fig. 4 summarizes the steps involved in reducing the cry-wolf effect. These can be outlined as follows: 

**Computation of p-values.** For each sample, the detection index is converted into a p-value. If the cumulative distribution function of the detection index under NOC data is known, it can be used directly. Otherwise, conformal prediction provides a model-agnostic way to obtain valid p-values. 

**Optional adjustment step.** In some cases, it may be desirable to adjust the p-values to ensure that the empirical FAR does not exceed the predefined risk level _α_ . Several approaches are available, such as the DKW bound, the generalized Simes inequality, or asymptotic approximations. However, this step is not mandatory and can be skipped if the FAR is already well controlled by construction. 

**FDR control.** The Benjamini–Hochberg procedure is then applied to the (possibly adjusted) p-values in order to control the FDR at a predefined level _q_ . 

**Fault declaration.** Samples with adjusted p-values below the threshold _q_ are declared as faults, ensuring that the expected proportion of false alarms among all alarms remains below _q_ . 

### **5. Case studies** 

To illustrate the limitations of the FAR and the detection rate, while also emphasizing the importance of the FDR and reducing the cry-wolf effect, we will examine two case studies. The first is the TEP, widely recognized in the fault detection community, and the second is a galvanizing line. 

### _5.1. Academic case study_ 

The TEP proposed in [81] simulates an industrial chemical process which produces two products G and H from four reactants A, C, D, and E, with the presence of an inert B and a by-product F. The production system which is schematized by Fig. 5 can be affected by 20 faults. Their description and many more details can be found in [81]. 

Several versions of data related to this benchmark can be found in the literature. However, they all share the same simulation principle. Indeed, there is a training set and an evaluation set. In each of these sets, there is a simulation of the production system under NOC and a simulation of each of the faults. In the training set, each simulation corresponds to 25 h of process operation and 500 samples are collected. In the evaluation set, the simulation corresponds to 48 h of operation and 960 samples are collected. When a fault is simulated, it is introduced after 1 h in the training set and 8 h in the evaluation set. The version of data used in this study was published in [82]. For more robust training and evaluation of detection models, that version repeats the simulation of the NOC and each fault 500 times in both the training set and the evaluation 

7 

> _A.R. Diallo et al.                                                                                                                                                                                                                                Reliability Engineering and System Safety 267 (2026) 111890_ 


![](Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems_images/Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems.pdf-0008-01.png)


**Fig. 4.** Flowchart for reducing the cry-wolf effect in fault detection. 


![](Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems_images/Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems.pdf-0008-03.png)


**Fig. 5.** Schematic description of the TEP. 

set thanks to a change in the random number generator. 

A PCA is trained by using only the NOC data of the training set (corresponding to 250,000 samples). All variables are standardized per feature (zero mean, unit variance computed on the training data). Twelve principal components are retained following the application of the parallel analysis method. The SPE is used as the detection index. This ’s T<sup>2</sup> tends to cause more false choice is justified by the fact that Hotelling alarms without improving the fault detection rate [83,84]. Two detection limits are considered and are calculated by applying the proposal of Jackson & Mudholkar, (1979) [3]: 


![](Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems_images/Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems.pdf-0008-07.png)


where _cα_ is the normal deviate corresponding to the upper (1 − _α_ ) percentile. 

The first threshold, noted as _T_ 1, is associated with _α_ = 1% while the second one, noted as _T_ 2, is associated with _α_ = 5%. We will refer to this model as the traditional model in the rest of this article. A second PCA is trained by following the conformal prediction procedure. Hence, 400 

8 

> _A.R. Diallo et al.                                                                                                                                                                                                                                Reliability Engineering and System Safety 267 (2026) 111890_ 

simulations (corresponding to 200,000 samples) of the NOC training data randomly selected are used for training the PCA whereas the 100 remaining simulations (corresponding to 50,000 samples) are used as calibration data. The NOC training data are standardized using statistics fitted on the PCA training subset only; the calibration simulations are not used to fit the standardizer. Twelve principal components are retained (as in the first PCA, via parallel analysis). The conformal prediction approach with marginal validity, which we will refer to as the marginal model, has also been applied with an associated threshold of 1 % and another of 5 % false alarms. Similarly, approaches with conditional validity are also applied with the same risk of false alarms. Three approaches (Simes, DKW and asymptotic) were applied for _δ_ = 0 _._ 1, i. e., with a 90 % probability of obtaining a FAR less than or equal to the risk _α_ . 

To reproduce the disparity that exists in the industrial reality between the probability of the production system being in NOC and the probability of the occurrence of a fault, a single simulation for each fault is randomly selected in the evaluation set, while the 500 simulations of the NOC are retained. In this way, there are 800 samples of each fault and 480,000 samples of normal operating conditions in the evaluation set. The fault detection rate on the evaluation set is presented in Table 4. 

The fault detection rates achieved for each fault are comparable to those reported in the state of the art, and the FARs on the test set are below _α_ = 1% and _α_ = 5% respectively except for the Marginal model which yielded 1.02 % and 5.10 % FARs, as shown in Table 5. However, the FDR remains very high for all the models. With the threshold _T_ 1, the probability of a false alarm given that an alarm is triggered ranges from 18.91 % to 32.93 %, depending on the model. This probability increases significantly with threshold _T_ 2, where the FDR is between 61.77 % and 69.51 %. Note that for threshold _T_ 1 the DKW method achieved the lowest FAR and consequently the lowest FDR, while for threshold _T_ 2 the Simes method yielded the lowest FDR. In all cases, the FAR is markedly different from the FDR for all the models. This highlights the importance of complementing the traditional indicators with the FDR to provide a more comprehensive evaluation of the detection models, particularly in contexts where the faults are rare. 

To lower the FDR, a p-values adjustment using the BenjaminiHochberg procedure was realised. An FDR less than or equal to 10 % is targeted ( _q_ = 0 _._ 1). Fig. 6 shows the FDR of the models under thresholds _T_ 1 and _T_ 2 and after the Benjamini-Hochberg procedure aimed at reducing the cry-wolf effect. It can be noted that the FDR is _<_ 10 % for all models after the Benjamini-Hochberg procedure. The DKW method even has a null FDR. 

However, reducing the FDR may come at the expense of fault detection capability. For completeness, FAR and, most importantly, the – fault detection rate after the Benjamini Hochberg procedure are reported in Table 6. 

There is a reduction in FAR for all models compared with the _T_ 1 and _T_ 2 thresholds. The DKW method produces no false alarms. However, it also fails to detect any fault occurrence, which makes it unusable in practice. This behavior is explained by the conservative nature of the – DKW adjustment combined with the Benjamini Hochberg procedure. For any new sample _x_ , the adjusted p-value is defined as: 


![](Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems_images/Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems.pdf-0009-07.png)


As a consequence, any DKW-adjusted p-value satisfies _p_<sup>ʹ</sup> ( _x_ ) ≥ _εn_ . On – the other hand, the Benjamini Hochberg procedure applied to the prediction batch of size _m_ requires that the smallest p-value satisfies _p_ (1) ≤ _q/m_ in order to trigger at least one alarm. In our setting, _m_ = 496000, and for _q_ = 0 _._ 1, the threshold is _q/m_ ≈ 2 × 10<sup>−7</sup> . With the calibration size _n_ = 50000 and _δ_ = 0 _._ 1, _εn_ = 5 _._ 47 × 10<sup>−3</sup> , which is several orders of magnitude larger than _q/m_ . Therefore, no DKW-adjusted p-value can fall below the BH rejection threshold, which explains why this method does not trigger any detection. 

For the other models, the reduction in the fault detection rate is limited and not comparable to that of the DKW method. Table 7 provides details of the fault detection rate. Excluding DKW, the impact of FDR control is not the same across all faults: in particular, detection of Faults 6 and 14 is not degraded, and Faults 1 and 2 are also unaffected compared with models using threshold _T_ 1, whereas Fault 18 exhibits a sharp decline when switching from _T_ 1 to FDR control. 

To further characterize the overall trade-off between FDR, FAR and fault detection rate reduction, the percentage of reduction in each metric is calculated. The results presented in Table 8 show that, with the exception of the DKW method, the decreases in FAR and FDR are not comparable to those in the mean fault detection rate. In fact, compared with threshold _T_ 1, the reductions in FAR and FDR are of the order of 80 % and 75 % respectively, while the drop in the mean fault detection rate is _<_ 5 %. Compared with threshold _T_ 2, the reductions in FAR and FDR are of the order of 95 % and 90 % respectively, while the drop in the mean fault detection rate is _<_ 12 %. 

To further assess the stability of the proposed approach under extreme class imbalance, an additional experiment was conducted by considering only Fault 1 (800 samples) against the entire set of normal 

**Table 4** 

Fault detection rate (%) on the evaluation set. 

||Traditional||Marginal||Simes||DKW||Asymptotic||
|---|---|---|---|---|---|---|---|---|---|---|
|Fault|_T_1|_T_2|_T_1|_T_2|_T_1|_T_2|_T_1|_T_2|_T_1|_T_2|
|Fault 1|99.62|99.88|99.62|99.88|99.62|99.88|99.62|99.88|99.62|99.88|
|Fault 2|98.75|98.88|98.75|98.75|98.75|98.75|98.75|98.75|98.75|98.75|
|Fault 3|1.25|6.12|1.38|6.25|1.12|4.50|0.88|5.50|1.25|6.00|
|Fault 4|98.50|99.62|98.75|99.62|98.38|99.25|97.25|99.50|98.50|99.50|
|Fault 5|11.12|19.12|11.75|19.38|10.12|17.50|8.88|18.62|10.75|19.00|
|Fault 6|100.00|100.00|100.00|100.00|100.00|100.00|100.00|100.00|100.00|100.00|
|Fault 7|99.88|100.00|99.88|100.00|99.88|100.00|99.75|100.00|99.88|100.00|
|Fault 8|97.38|98.12|97.38|98.12|97.38|98.12|97.25|98.12|97.38|98.12|
|Fault 9|1.38|5.88|1.50|5.88|0.88|4.12|0.88|5.25|1.25|5.75|
|Fault 10|23.62|43.00|25.12|44.38|22.12|37.38|19.25|41.00|23.38|43.00|
|Fault 11|70.25|79.38|70.50|79.38|68.88|77.62|66.62|78.88|69.62|79.38|
|Fault 12|88.25|92.50|88.50|92.62|87.75|91.88|86.75|92.38|88.25|92.38|
|Fault 13|93.12|94.00|93.12|94.00|92.75|93.62|92.75|93.88|92.88|94.00|
|Fault 14|100.00|100.00|100.00|100.00|100.00|100.00|100.00|100.00|100.00|100.00|
|Fault 15|1.25|6.00|1.62|6.00|1.12|4.50|0.88|5.25|1.25|5.62|
|Fault 16|9.25|24.00|9.75|24.25|8.62|20.12|7.38|22.88|9.25|23.62|
|Fault 17|89.00|93.00|89.25|92.88|88.88|92.00|87.75|92.75|89.00|92.75|
|Fault 18|93.50|93.62|93.50|93.62|93.38|93.50|93.38|93.62|93.50|93.62|
|Fault 19|15.38|34.00|16.50|34.88|14.12|29.88|10.88|33.25|15.00|34.12|
|Fault 20|44.75|53.50|45.00|53.75|43.62|50.75|42.25|52.25|44.38|53.00|



9 

> _A.R. Diallo et al.                                                                                                                                                                                                                                Reliability Engineering and System Safety 267 (2026) 111890_ 

**Table 5** 

Performances (%) of the models on the test set. 

||Traditional||Marginal||Simes||DKW||Asymptotic||
|---|---|---|---|---|---|---|---|---|---|---|
|Metric|_T_1|_T_2|_T_1|_T_2|_T_1|_T_2|_T_1|_T_2|_T_1|_T_2|
|FAR|0.94|4.96|1.02|5.10|0.75|3.54|0.47|4.49|0.87|4.79|
|Mean TPR|61.81|67.03|62.09|67.18|61.37|65.67|60.56|66.59|61.69|66.92|
|FDR|31.39|68.96|32.93|69.51|26.94|61.77|18.91|66.92|29.80|68.24|




![](Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems_images/Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems.pdf-0010-04.png)


**Fig. 6.** FDR before and after the FDR control _._ 

#### **Table 6** 

Performances (%) of the models on the test set after the FDR control. 

|Metric|Traditional|Marginal|Simes|DKW|Asymptotic|
|---|---|---|---|---|---|
|FAR|0.18|0.21|0.13|0|0.14|
|Mean TPR|59.29|59.46|58.48|0|58.96|
|FDR|8.53|9.56|6.28|0|6.75|



#### **Table 7** 

#### **Table 8** 

Percentage of reduction in evaluation metrics after the FDR control. 

||_T_1|||_T_2|||
|---|---|---|---|---|---|---|
|Approach|FAR|Mean TPR|FDR|FAR|Mean TPR|FDR|
|Traditional|80.85|4.08|72.83|96.37|11.55|87.63|
|Marginal|79.41|4.24|70.97|95.88|11.49|86.25|
|Simes|82.67|4.12|76.69|96.33|10.4|89.83|
|Asymptotic|83.91|4.49|77.35|97.08|11.95|90.11|
|DKW|100|100|100|100|100|100|



Fault detection rate (%) on the test set after the FDR control. 

|Fault|Traditional|Marginal|Simes|DKW|Asymptotic|
|---|---|---|---|---|---|
|Fault 1|99.62|99.62|99.62|0|99.62|
|Fault 2|98.75|98.75|98.75|0|98.75|
|Fault 3|0.38|0.38|0.25|0|0.25|
|Fault 4|95.75|96.25|94.38|0|94.75|
|Fault 5|7.50|7.75|7.12|0|7.12|
|Fault 6|100.00|100.00|100.00|0|100.00|
|Fault 7|99.50|99.50|99.38|0|99.38|
|Fault 8|96.62|96.75|96.25|0|96.25|
|Fault 9|0.50|0.50|0.25|0|0.25|
|Fault 10|15.75|16.12|14.75|0|15.12|
|Fault 11|62.12|62.75|61.00|0|61.00|
|Fault 12|84.38|84.50|84.00|0|84.00|
|Fault 13|92.75|92.75|92.75|0|92.75|
|Fault 14|100.00|100.00|100.00|0|100.00|
|Fault 15|0.50|0.50|0.25|0|0.25|
|Fault 16|5.38|5.62|4.75|0|5.00|
|Fault 17|86.25|86.25|85.38|0|85.50|
|Fault 18|93.38|93.38|93.38|0|93.38|
|Fault 19|6.75|7.50|6.00|0|6.25|
|Fault 20|39.88|40.25|38.50|0|38.75|



samples (480,000). Table 9 reports the results obtained for thresholds _T_ 1 and _T_ 2, as well as after FDR control. In this setting, FDR control becomes more conservative: the true positive rate for Fault 1 decreases only marginally, from 99.62 % to 99.5 %, while both FAR and FDR are substantially reduced. Before correction, the imbalance considerably –97 % amplifies the risk of the cry-wolf effect: FDR values reach up to 85 at thresholds _T_ 1 and _T_ 2, meaning that the vast majority of alarms would be false. This observation is consistent with Fig. 3, which illustrated that increasing imbalance strongly elevates the risk of cry-wolf effect. After correction, however, FDR is brought down to levels below 10 % for all methods, thereby effectively mitigating the problem. These results reinforce the necessity of applying FDR control in fault detection contexts characterized by severe class imbalance. 

Although the FAR values reported after correction are equal to 0.00 % in some cases, this reflects rounding relative to the large number of normal samples. The absolute counts of false alarms are not zero. They are 67 for the Traditional method, 81 for Marginal, 20 for Simes, 20 for Asymptotic, and 0 for DKW. This confirms that, under severe imbalance, 

10 

> _A.R. Diallo et al.                                                                                                                                                                                                                                Reliability Engineering and System Safety 267 (2026) 111890_ 

**Table 9** 

Performance (%) of the different approaches under an extreme imbalance scenario (480,000 normal samples vs 800 samples of fault 1). 

||_T_1|||_T_2|||FDR contro|l (_q_= 10 %)||
|---|---|---|---|---|---|---|---|---|---|
|Approach|FAR|FDR|TPR|FAR|FDR|TPR|FAR|FDR|TPR|
|Traditional|0.94|85.02|99.62|4.96|96.75|99.88|0.01|7.76|99.5|
|Marginal|1.02|85.95|99.62|5.10|96.84|99.88|0.02|9.24|99.5|
|Simes|0.75|81.96|99.62|3.54|95.5|99.88|0.00|2.45|99.5|
|Asymptotic|0.87|84.02|99.62|4.79|96.64|99.88|0.00|2.45|99.5|
|DKW|0.47|73.92|99.62|4.49|96.42|99.88|0.00|0.00|0.00|



the correction step effectively drives the number of false alarms to negligible levels while maintaining a high detection capability. 

### _5.2. Industrial application- a galvanising line_ 

The galvanising line represents the final stage in the steel production value chain, which begins with the blast furnace and includes continuous casting, hot rolling, and cold rolling. This process aims to enhance mechanical properties through continuous annealing and to protect the steel with a thin zinc coating. Mechanical properties cannot be measured in real time; they are only assessed after the galvanizing process is complete, following laboratory tests conducted hours or even days later. This delay means decisions about whether the steel meets customer requirements are deferred. 

The relationships between mechanical properties and process as well as product parameters are complex, and in some cases are formalised in the form of Model Predictive Control (MPC) for galvanizing line management. In other cases, operators rely on setting tables and personal expertise. The chemical composition of the steel is a critical factor for production controls and is measured during continuous casting with sensors calibrated regularly. 

However, sensor drifts between calibration can lead to erroneous measurements of the chemical composition. These errors have a direct impact on the final mechanical properties but are difficult to detect on the galvanizing line. Additionally, since continuous casting supplies several galvanizing lines and steel coils are not necessarily processed in arrival order, errors in chemical composition measurements can cause intermittent faults on a specific galvanizing line. In this study, we focus on three faults. The first two relate to the measurement of the chemical composition of the steel, while the third corresponds to a situation where the steel does not exhibit the expected thermodynamic properties. However, these thermodynamic properties cannot be measured on the production line. 

In this context, an AE was used to detect these faults. It was trained by following the conformal prediction framework.28,400 samples from the NOC data were used to train the AE while 7100 samples from the NOC data were used are used as calibration data. All input variables were standardized per feature using statistics fitted on the AE training subset only; the calibration data were not used to fit the standardizer. The AE architecture included an input layer of 52 neurons representing the steel characteristics, process parameters, actuator commands and internal variables of the MPC as recommended in [85]. It featured two intermediate layers with 32 neurons each and an output layer with 52 neurons. The hidden layers used ReLU activations and the output layer was linear. Training relied on the Adam optimizer with a learning rate of 0.001, mean squared error as the loss function, a batch size of 128, and a maximum of 100 epochs. Early stopping with a patience of 10 was applied, using 20 % of the training data (5680 samples) as a validation set. The reconstruction error was used as the detection index, and two detection thresholds were set to correspond to 1 % and 5 % of FARs on the training set. 

This model was developed for continuously operating galvanising lines that process steel coils up to 1.5 km long. These coils are welded together at the line inlet and separated at the outlet. The model was evaluated over 63 days of continuous operation. It generated a 

prediction (NOC or occurrence of a fault) at the end of the galvanisation of each coil, with an average interval of 10 min between predictions. During this evaluation, the line processed 210 faulty coils, representing a cumulative processing time of approximately one day and a half. However, these faulty coils were not processed consecutively; at least two fault-free coils were galvanized between any two faulty coils. 

The fault detection rate of the AE as a function of the calibration method is shown in Table 10. Firstly, it can be seen that with the DKW method, using the _T_ 1 threshold, not a single occurrence of a fault is detected. This is in contrast to the other approaches, for which all occurrences of Faults 1 and 2 were detected for this same threshold. Fault 3, on the other hand, has a fault detection rate of over 85 %. By lowering the detection threshold, the DKW method, like the other approaches, detects all occurrences of Faults 1 and 2, and has a 95.71 % detection rate for Fault 3. Overall, the marginal method has the best average fault detection rate for the higher threshold. For threshold _T_ 2, all four methods have the same average. 

These fault detection rates were obtained for the FARs and FDRs provided in Table 11. In particular, it can be seen that for threshold _T_ 1, the FARs for all methods are lower than the risk _α_ . Particularly with the DKW method, for which no faults were detected, no false alarms were triggered either. For the _T_ 2 threshold, however, the marginal approach has a FAR higher than the risk, without this translating into a higher fault detection rate. The FDR illustrates the trade-off between fault detection rate and false alarm rate, particularly in this context of data imbalance. The marginal approach has the highest FDRs, while the DKW approach has the lowest. However, for the _T_ 1threshold, the DKW approach is useless as it detects no faults. The same is true for threshold _T_ 2, where despite this approach having the lowest FDR, it is large enough to cause the cry-wolf effect. In fact, more than one out of every two alarms triggered was actually false. 

To reduce the FDR, a p-value adjustment was applied with the objective of obtaining an FDR of less than or equal to 10 %. Table 12 reports the fault detection rates by fault type. The FDR correction had no effect on the detection of faults 1 and 2. As with threshold _T_ 1, the DKW method failed to detect any of these faults, while the other three methods detected all of them. In contrast, a drastic reduction is observed for fault 3. This reduction, which naturally affects the mean fault detection rate, should be considered in light of the decreases in FAR and FDR reported in Table 13. 

For all methods, the FAR has fallen and the FDR is now below 10 %. Fig. 7 illustrates the evolution of the FDR as a function of the chosen threshold. 

As for the academic case study, we calculated the percentage of reduction for each indicator. The results are presented in Table 14. 

It can be seen that, apart from the DKW method which no longer detects faults, the reductions in FDR and FAR are not of the same order of magnitude as the reduction in the mean fault detection rate. The decreases in the fault detection rate are about 15 % and 18 % for _T_ 1 and _T_ 2 respectively, whereas the FDR decreases by just over 70 % and 85 % respectively. An even greater reduction is observed for the FAR. 

### **6. Conclusions and perspectives** 

Numerous fault detection models have been proposed in the 

11 

> _A.R. Diallo et al.                                                                                                                                                                                                                                Reliability Engineering and System Safety 267 (2026) 111890_ 

#### **Table 10** 

Fault detection rate (%) of the AE on the evaluation set. 

||Marginal||Simes||Asymptotic||DKW||
|---|---|---|---|---|---|---|---|---|
|Fault|_T_1|_T_2|_T_1|_T_2|_T_1|_T_2|_T_1|_T_2|
|Fault 1|100|100|100|100|100|100|0|100|
|Fault 2|100|100|100|100|100|100|0|100|
|Fault 3|88.57|95.71|85.71|95.71|85.71|95.71|0|95.71|
|**Mean**|**96.19**|**98.57**|**95.24**|**98.57**|**95.24**|**98.57**|**0**|**98.57**|



#### **Table 11** 

FAR (%) and FDR (%) of the AE on the evaluation set. 

||FAR||FDR||
|---|---|---|---|---|
|Approach|_T_1|_T_2|_T_1|_T_2|
|Marginal|0.96|5.26|29.62|69.29|
|Simes|0.69|3.74|23.37|61.60|
|Asymptotic|0.70|4.46|23.66|65.67|
|DKW|0|3.68|0|61.24|



#### **Table 12** 

Fault detection rate (%) after the FDR control. 

|Fault|Marginal|Simes|Asymptotic|DKW|
|---|---|---|---|---|
|Fault 1|100|100|100|0|
|Fault 2|100|100|100|0|
|Fault 3|45.71|44.29|42.86|0|
|**Mean**|**81.90**|**81.43**|**80.95**|**0**|



literature. Nevertheless, the deployment of such models in industrial contexts continues to be hindered by the limited availability of faulty data. While this constraint is often taken into account during the training phase, it remains insufficiently addressed at the evaluation stage. In this study, we demonstrated that conventional performance metrics are inadequate for evaluating detection models in settings characterized by rare fault occurrences. These metrics fail to reflect the operational burden induced by the cry-wolf effect, a phenomenon better captured by the false discovery rate (FDR), as evidenced by the academic and industrial case studies. The cry-wolf effect represents a major obstacle to the adoption and long-term use of alarm systems; its quantification is thus essential for any detection model intended for real-world deployment. However, concrete methodologies to control or mitigate this phenomenon in fault detection are still lacking. 

To address this limitation, we incorporated FDR control into the evaluation and threshold calibration of detection models. This approach led to a marked reduction in both the FAR and the FDR, which jointly reflect the false alarm load imposed on operators. While a decrease in fault detection rate was observed, it remained comparatively minor. In 

#### **Table 13** 

Performance (%) of the AE after the FDR control. 

|Metric|Marginal|Simes|Asymptotic|DKW|
|---|---|---|---|---|
|FAR|0.19|0.1|0.10|0|
|FDR|8.99|5|5.03|0|
|Mean TPR|81.9|81.43|80.95|0|



#### **Table 14** 

Percentage of decrease in each metric after the FDR control. 

||_T_1|||_T_2|||
|---|---|---|---|---|---|---|
|Approach|FAR|FDR|Mean TPR|FAR|FDR|Mean TPR|
|Marginal|80.21|69.65|14.86|96.39|87.03|16.91|
|Simes|85.51|78.61|14.50|97.33|91.88|17.39|
|Asymptotic|85.71|78.74|15|97.76|92.34|17.88|
|DKW|0|0|0|100|100|100|




![](Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems_images/Quantifying_and_mitigating_alarm_fatigue_caused_by_fault_detection_systems.pdf-0012-18.png)


**Fig. 7.** FDR of the AE before and after the cry-wolf effect mitigation. 

12 

> _A.R. Diallo et al.                                                                                                                                                                                                                                Reliability Engineering and System Safety 267 (2026) 111890_ 

both case studies, the reduction in detection performance was outweighed by the substantial improvements in alarm relevance. Beyond these specific applications, our findings highlight a more general lesson: the cry-wolf effect emerges whenever faults are rare, regardless of the detection model considered. The FDR therefore provides an interpretable and scalable indicator of alarm reliability that can be applied to a wide range of approaches, including dimension reduction models as well as other one-class or statistical fault detection methods such as independent component analysis, One-class support vector machine and isolation forest. More broadly, the conclusions regarding model evaluation are also valid for supervised learning methods, where class imbalance likewise undermines the reliability of FAR and fault detection rate as performance metrics. It should be noted, however, that the FDR control procedure proposed in this work applies primarily to methods whose detection decisions can be framed as statistical tests. In contrast, while FDR itself remains a relevant indicator for supervised approaches, recent statistical advances have begun to explore how FDR control can be adapted to supervised learning settings, and these developments could be extended to fault detection in future work. 

A limitation of the proposed approach is that FDR control depends on the reliability of the underlying detection model. If the model fails to account for process variability, the correction will not prevent spurious alarms. However, it will typically reduce their frequency compared with the base model, since alarms are only triggered when they pass the FDR threshold. This highlights the importance of training and calibration data that are sufficiently diverse and representative of normal operation. 

The implementation of the Benjamini-Hochberg procedure requires a batch of p-values to perform FDR control. In practice, this means that the detection system must wait for a set of samples to be collected before the corresponding p-values can be computed, potentially introducing a delay in fault detection. This delay can be mitigated by choosing an optimal batch size or by using the p-values from the previous time horizon while incorporating the newly obtained p-value from the latest measurement. Another alternative is to reuse a batch of p-values obtained from offline test data to enable real-time FDR control with each new sample. 

It is also worth noting that in this study, we implicitly assigned a higher cost to false alarms than to missed fault detections. This assumption is appropriate in many industrial monitoring contexts, where frequent false alarms can erode operator trust and system usability. However, in scenarios where certain faults have severe consequences, and the cost of missed detection far outweighs the cost of false positives, FDR control may not be the appropriate strategy. For instance, as highlighted by a survey cited in this article, both patients and healthcare professionals were willing to accept up to 2250 false positives in exchange for the correct detection of one additional cancer case. Such findings emphasize that the relevance of FDR control is contextdependent and must be aligned with domain-specific risk perceptions and priorities. 

Finally, the FDR threshold used in this study, set at 10 %, was selected arbitrarily, in the absence of a validated standard for an acceptable level of the cry-wolf effect. Determining a context-dependent acceptable FDR level remains an open question. This threshold will necessarily vary depending on factors such as the severity of faults, the criticality and urgency of interventions, and other operational constraints specific to each industrial process. Future work should therefore aim to define acceptable FDR levels grounded in human factors and process requirements. 

### **CRediT authorship contribution statement** 

**Abdoul Rahime Diallo:** Writing – review & editing, Writing – original draft, Visualization, Validation, Software, Methodology, Investigation, Formal analysis, Data curation, Conceptualization. **Lazhar Homri:** Writing – review & editing, Validation, Supervision, Methodology, Investigation, Conceptualization. **Thomas Boeuf:** 

Writing – review & editing, Validation, Project administration, Methodology, Data curation. **Jean-Yves Dantan:** Writing – review & editing, Validation, Supervision, Project administration, Methodology, Funding acquisition, Formal analysis, Conceptualization. **Fred** ´ **eric Bonnet:** ´ Supervision, Project administration, Methodology, Funding acquisition, Data curation. 

### **Declaration of competing interest** 

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper. 

### **Acknowledgements** 

This paper has been supported by CaM´eX-IA, R´egion Grand Est, and Arcelor Mittal Global R&D, which is gratefully acknowledged by the authors. 

### **Data availability** 

Data will be made available on request. 

### **References** 

- [1] Sanchez L, Costa N, Couso I. Addressing data scarcity in industrial reliability assessment with physically informed Echo State Networks. Reliab Eng Syst Saf Sep. 2025;261:111135. https://doi.org/10.1016/j.ress.2025.111135. 

- [2] Tian J, Jiang Y, Zhang J, Luo H, Yin S. A novel data augmentation approach to fault diagnosis with class-imbalance problem. Reliab Eng Syst Saf Mar. 2024;243. https://doi.org/10.1016/j.ress.2023.109832. 

- [3] Jackson JE, Mudholkar GS. Control procedures for residuals associated with principal component analysis. Technometrics Aug. 1979;21(3):341. https://doi. 

- [4] org/10.2307/1267757Macgregor JF, Yu H, García Mu. noz S, Flores-Cerrillo J. Data-based latent variable ˜ methods for process analysis, monitoring and control. Comput Chem Eng 2005;29: 1217–23. https://doi.org/10.1016/j.compchemeng.2005.02.007. 

- [5] Kramer MA. Nonlinear principal component analysis using autoassociative neural networks. AIChE J Feb. 1991;37(2):233–43. https://doi.org/10.1002/ aic.690370209. 

- [6] Liu FT, Ting KM, Zhou Z-H. Isolation Forest. In: 2008 Eighth IEEE International Conference on Data Mining. IEEE; Dec. 2008. p. 413–22. https://doi.org/10.1109/ ICDM.2008.17. 

- [7] Scholkopf B, Platt JC, Shawe-Taylor J, Smola AJ, Williamson RC. Estimating the ¨ support of a high-dimensional distribution. Neural Comput Jul. 2001;13(7): 1443–71. https://doi.org/10.1162/089976601750264965. 

- [8] Zhao C, Shen W. Dual adversarial network for cross-domain open set fault diagnosis. Reliab Eng Syst Saf May 2022;221:108358. https://doi.org/10.1016/j. ress.2022.108358. 

- [9] Zhao C, Zio E, Shen W. Domain generalization for cross-domain fault diagnosis: an application-oriented perspective and a benchmark study. Reliab Eng Syst Saf May 2024;245:109964. https://doi.org/10.1016/j.ress.2024.109964. 

- [10] Wang W, Li C, Zhang Z, Chen J, He S, Feng Y. Pseudo-label assisted contrastive learning model for unsupervised open-set domain adaptation in fault diagnosis. Reliab Eng Syst Saf Feb. 2025;254. https://doi.org/10.1016/j.ress.2024.110650. 

- [11] Wang W, Song H, Si S, Lu W, Cai Z. Data augmentation based on diffusion probabilistic model for remaining useful life estimation of aero-engines. Reliab Eng Syst Saf Dec. 2024;252. https://doi.org/10.1016/j.ress.2024.110394. 

- [12] Dong H, Peng C, Chen L, Hao K. Dynamic ensemble fault diagnosis framework with adaptive hierarchical sampling strategy for industrial imbalanced and overlapping data. Reliab Eng Syst Saf Aug. 2025;260:110979. https://doi.org/10.1016/j. ress.2025.110979. 

- [13] Li W, Gu S, Zhang X, Chen T. Transfer learning for process fault diagnosis: knowledge transfer from simulation to physical processes. Comput Chem Eng Aug. 2020;139:106904. https://doi.org/10.1016/j.compchemeng.2020.106904. 

- [14] Colosimo BM, Jones-Farmer LA, Megahed FM, Paynabar K, Ranjan C, Woodall WH. Statistical process monitoring from industry 2.0 to industry 4.0: insights into research and practice. Technometrics Oct. 2024;66(4):507–30. https://doi.org/ 10.1080/00401706.2024.2327341. 

- [15] Engbers H, Alla AA, Kreutz M, Freitag M. Applicability of algorithm evaluation metrics for predictive maintenance in production systems. In: 2020 6th IEEE Congress on Information Science and Technology (CiSt). IEEE; Jun. 2020. p. 413–8. https://doi.org/10.1109/CiSt49399.2021.9357277. 

- [16] Frank S, Lin G, Jin X, Singla R, Farthing A, Granderson J. A performance evaluation framework for building fault detection and diagnosis algorithms. Energy Build Jun. 2019;192:84–92. https://doi.org/10.1016/j.enbuild.2019.03.024. 

13 

_Reliability Engineering and System Safety 267 (2026) 111890_ 

- [17] Spina DE, et al. Comparison of autoencoder architectures for fault detection in industrial processes. Digit Chem Eng Sep. 2024;12:100162. https://doi.org/ 10.1016/j.dche.2024.100162. 

- [18] Rieth CA, Amsel BD, Tran R, Cook MB. Issues and advances in anomaly detection evaluation for joint human-automated systems. Advances in intelligent systems and computing. Springer Verlag; 2018. p. 52–63. https://doi.org/10.1007/978-3319-60384-1_6. 

- [19] Yin S, Ding SX, Haghani A, Hao H, Zhang P. A comparison study of basic datadriven fault diagnosis and process monitoring methods on the benchmark Tennessee Eastman process. J Process Control Oct. 2012;22(9):1567–81. https:// doi.org/10.1016/j.jprocont.2012.06.009. 

- [20] Breznitz S. Cry wolf: the psychology of false alarms. Hillsdale: Lawrence Erlbaum associates; 1984. 

- [21] Bliss JP, Gilson RD, Deaton JE. Human probability matching behaviour in response to alarms of varying reliability. Ergonomics Nov. 1995;38(11):2300–12. https:// doi.org/10.1080/00140139508925269. 

- [22] Getty DJ, Swets JA, Pickett RM, Gonthier D. System operator response to warnings of danger: a laboratory investigation of the effects of the predictive value of a warning on human response time. J Exp Psychol Appl 1995;1(1):19. 

- [23] Pat´e-Cornell ME. Warning Systems in Risk Management. Risk Anal Jun. 1986;6(2): 223–34. https://doi.org/10.1111/J.1539-6924.1986.TB00210.X. 

- [24] Bliss JP, Dunn MC. Behavioural implications of alarm mistrust as a function of task workload. Ergonomics Sep. 2000;43(9):1283–300. https://doi.org/10.1080/ 001401300421743. 

- [25] Shivers JP, Mackowiak L, Anhalt H, Zisser H. Turn it off!’: diabetes device alarm fatigue considerations for the present and the future.  J Diabetes Sci Technol May 2013;7(3):789–94. https://doi.org/10.1177/193229681300700324. 

- [26] Cvach M. Monitor alarm fatigue: an integrative review. Biomed Instrum Technol Jul. 2012;46(4):268–77. https://doi.org/10.2345/0899-8205-46.4.268. 

- [27] Goel P, Datta A, Mannan MS. Industrial alarm systems: challenges and opportunities. J Loss Prev Process Ind Nov. 2017;50:23–36. https://doi.org/ 10.1016/j.jlp.2017.09.001. 

- [28] Mustafa FE, et al. A review on effective alarm management systems for industrial process control: barriers and opportunities. Elsevier B.V; 2023. https://doi.org/ 10.1016/j.ijcip.2023.100599. Jul. 01. 

- [29] Wang J, Yang F, Chen T, Shah SL. An overview of industrial alarm systems: main causes for alarm overloading, research status, and open problems. Institute of Electrical and Electronics Engineers Inc; 2016. https://doi.org/10.1109/ TASE.2015.2464234. Apr. 01. 

- [30] Kaced R, Kouadri A, Baiche K, Bensmail A. Multivariate nuisance alarm management in chemical processes. J Loss Prev Process Ind Sep. 2021;72:104548. https://doi.org/10.1016/J.JLP.2021.104548. 

- [31] Arunthavanathan R, Khan F, Ahmed S, Imtiaz S. An analysis of process fault diagnosis methods from safety perspectives. Elsevier Ltd; 2021. https://doi.org/ 10.1016/j.compchemeng.2020.107197. Feb. 01. 

- [32] Bakdi A, Kouadri A. A new adaptive PCA based thresholding scheme for fault detection in complex systems. Chemom Intell Lab Syst Mar. 2017;162:83–93. https://doi.org/10.1016/j.chemolab.2017.01.013. 

- [33] Bakdi A, Kouadri A. An improved plant-wide fault detection scheme based on PCA and adaptive threshold for reliable process monitoring: application on the new revised model of Tennessee Eastman process. J Chemom May 2018;32(5). https:// doi.org/10.1002/cem.2978. 

- [34] Ko JU, Na K, Oh JS, Kim J, Youn BD. A new auto-encoder-based dynamic threshold to reduce false alarm rate for anomaly detection of steam turbines. Expert Syst Appl 

- [35] Mar. 2022;189. Sori´c B. Statistical ‘discoverieshttps://doi.org/10.1016/j.eswa.2021.116094’ and effect-size estimation. J Am Stat Assoc Jun. . 1989;84(406):608–10. https://doi.org/10.1080/01621459.1989.10478811. 

- [36] Benjamini Y, Hochberg Y. Controlling the false discovery rate: a practical and powerful approach to multiple testing. J R Stat Soc B Stat Methodol Jan. 1995;57 (1):289–300. https://doi.org/10.1111/j.2517-6161.1995.tb02031.x. 

- [37] Qian J, Song Z, Yao Y, Zhu Z, Zhang X. A review on autoencoder based representation learning for fault detection and diagnosis in industrial processes. Chemom Intell Lab Syst Dec. 2022;231:104711. https://doi.org/10.1016/j. chemolab.2022.104711. 

- [38] Yu J, Zhang Y. Challenges and opportunities of deep learning-based process fault detection and diagnosis: a review. Neural Comput Appl Jan. 2023;35(1):211–52. https://doi.org/10.1007/s00521-022-08017-3. 

- [39] Qin SJ. Survey on data-driven industrial process monitoring and diagnosis. Annu Rev Control Dec. 2012;36(2):220–34. https://doi.org/10.1016/j. arcontrol.2012.09.004. 

- [40] Chiang LH, Russell EL, Braatz RD. Fault detection and diagnosis in industrial systems. Springer Science & Business Media; 2000. 

- [41] Tracy ND, Young JC, Mason RL. Multivariate control charts for individual observations. J Qual Technol Apr. 1992;24(2):88–95. https://doi.org/10.1080/ 00224065.1992.12015232. 

- [42] Li Q, Wan J, Yang X, Huang J, Cui J, Yan Q. Two-stage stacked autoencoder monitoring model based on deep slow feature representation for dynamic processes. J Process Control Mar. 2025;147:103389. https://doi.org/10.1016/j. jprocont.2025.103389. 

- [43] Ni Y, Jiang C. Ensemble quality-Aware slow feature Analysis for decentralized dynamic process monitoring. J Process Control Apr. 2025;148:103400. https://doi. org/10.1016/j.jprocont.2025.103400. 

- [44] Hu D, Zhang C, Yang T, Fang Q. A deep autoencoder with structured latent space for process monitoring and anomaly detection in coal-fired power units. Reliab Eng Syst Saf Sep. 2025;261:111060. https://doi.org/10.1016/j.ress.2025.111060. 

- [45] Dong J, Li D, Cong Z, Peng K. A new fault detection method based on an updatable hybrid model for hard-to-detect faults in nonstationary processes. Reliab Eng Syst Saf Jul. 2025;259:110920. https://doi.org/10.1016/j.ress.2025.110920. 

- [46] Ali H, et al. Intelligent machine learning-based multi-model fusion monitoring: application to industrial physio-chemical systems. Control Eng Pr Sep. 2025;162: 106361. https://doi.org/10.1016/j.conengprac.2025.106361. 

- [47] Ali H, et al. Fault detection using machine learning based dynamic ICA-distributed CCA: application to industrial chemical process. Digit Chem Eng Jun. 2024;11: 100156. https://doi.org/10.1016/J.DCHE.2024.100156. 

- [48] Attouri K, et al. Improved fault detection based on kernel PCA for monitoring industrial applications. J Process Control Jan. 2024;133:103143. https://doi.org/ 10.1016/j.jprocont.2023.103143. 

- [49] Zhang Z, Wei L, Hao X, Wang Y, Li Y, Hu J. Monitoring method and application of transition process with nonstationary conditions based on stability factor partitioning and RSFA. J Process Control Jun. 2024;138. https://doi.org/10.1016/ j.jprocont.2024.103209. 

- [50] Allen L, Lu H, Cordiner J. Knowledge-enhanced spatiotemporal analysis for anomaly detection in process manufacturing. Comput Ind Oct. 2024;161:104111. https://doi.org/10.1016/J.COMPIND.2024.104111. 

- [51] Luo ZD, Li HX. A fast data-driven fault detection and location method for unknown distributed thermal processes. Measurement Aug. 2024;236:115118. https://doi. org/10.1016/J.MEASUREMENT.2024.115118. 

- [52] Jin W, Wang W, Wang Y, Cao Z, Jiang Q. Distributed monitoring of nonlinear plant-wide processes based on GA-regularized kernel canonical correlation analysis. Reliab Eng Syst Saf Dec. 2024;252:110421. https://doi.org/10.1016/j. ress.2024.110421. 

- [53] Lakshmi Priya Palla G, Kumar Pani A. Independent component analysis application for fault detection in process industries: literature review and an application case study for fault detection in multiphase flow systems. Measurement Mar. 2023;209: 112504. https://doi.org/10.1016/j.measurement.2023.112504. 

- [54] Xiao Z, Kordon A, Sen S. Fault detection and diagnosis in Tennessee Eastman process with deep autoencoder. Annu Conf PHM Soc Oct. 2023;15(1). https://doi. org/10.36001/phmconf.2023.v15i1.3578. 

- [55] Peng K, Guo Y. Fault detection and quantitative assessment method for process industry based on feature fusion. Measurement 2022;197:111267. https://doi.org/ 10.1016/j.measurement.2022.111267. 

- [56] Yu J, Liu X. One-dimensional residual convolutional auto-encoder for fault detection in complex industrial processes. Int J Prod Res Sep. 2022;60(18): 5655–74. https://doi.org/10.1080/00207543.2021.1968061. 

- [57] Li S, Luo J, Hu Y. Toward interpretable process monitoring: slow feature analysisaided autoencoder for spatiotemporal process feature learning. IEEE Trans Instrum Meas 2022;71. https://doi.org/10.1109/TIM.2021.3127284. 

- [58] Plakias S, Boutalis YS. A novel information processing method based on an ensemble of Auto-encoders for unsupervised fault detection. Comput Ind Nov. 2022;142:103743. https://doi.org/10.1016/J.COMPIND.2022.103743. 

- [59] Reinartz C, Kulahci M, Ravn O. An extended Tennessee Eastman simulation dataset for fault-detection and decision support systems. Comput Chem Eng Jun. 2021; 149. https://doi.org/10.1016/j.compchemeng.2021.107281. 

- [60] Li Z, Tian L, Jiang Q, Yan X. Distributed-ensemble stacked autoencoder model for non-linear process monitoring. Inf Sci Jan. 2021;542:302–16. https://doi.org/ 10.1016/j.ins.2020.06.062. 

- [61] Liu X, Yu J, Ye L. Residual attention convolutional autoencoder for feature learning and fault detection in nonlinear industrial processes. Neural Comput Appl Oct. 2021;33(19):12737–53. https://doi.org/10.1007/s00521-021-05919-6. 

- [62] Yoo YJ. Data-driven fault detection process using correlation based clustering. Comput Ind Nov. 2020;122:103279. https://doi.org/10.1016/J. COMPIND.2020.103279. 

- [63] Yan S, Yan X. Design teacher and supervised dual stacked auto-encoders for quality-relevant fault detection in industrial process. Appl Soft Comput Aug. 2019; 81:105526. https://doi.org/10.1016/j.asoc.2019.105526. 

- [64] Chen Z, Zhang K, Ding SX, Shardt YAW, Hu Z. Improved canonical correlation analysis-based fault detection methods for industrial processes. J Process Control 2016;41:26–34. https://doi.org/10.1016/j.jprocont.2016.02.006. 

- [65] Rato TJ, Reis MS. Fault detection in the Tennessee Eastman benchmark process using dynamic principal components analysis based on decorrelated residuals (DPCA-DR). Chemom Intell Lab Syst Jun. 2013;125:101–8. https://doi.org/ 10.1016/j.chemolab.2013.04.002. 

- [66] Mahadevan S, Shah SL. Fault detection and diagnosis in process data using oneclass support vector machines. J Process Control Dec. 2009;19(10):1627–39. https://doi.org/10.1016/j.jprocont.2009.07.011. 

- [67] Lee JM, Qin SJ, Lee IB. Fault detection and diagnosis based on modified independent component analysis. AIChE J Oct. 2006;52(10):3501–14. https://doi. org/10.1002/AIC.10978. 

- [68] Lee JM, Yoo CK, Lee IB. Statistical process monitoring with independent component analysis. J Process Control Aug. 2004;14(5):467–85. https://doi.org/ 10.1016/j.jprocont.2003.09.004. 

- [69] Kano M, Tanaka S, Hasebe S, Hashimoto I, Ohno H. Monitoring independent components for fault detection. AIChE J Apr. 2003;49(4):969–76. https://doi.org/ 10.1002/AIC.690490414. 

- [70] Russell EL, Chiang LH, Braatz RD. Fault detection in industrial processes using canonical variate analysis and dynamic principal component analysis. Chemom Intell Lab Syst 2000;51:81–93. Accessed: Feb. 26, 2025. [Online]. Available: www. elsevier.comrlocaterchemometrics. 

- [71] Cheng H, Liu Y, Huang D, Liu B. Optimized forecast components-SVM-based fault diagnosis with applications for wastewater treatment. IEEE Access 2019;7: 128534–43. https://doi.org/10.1109/ACCESS.2019.2939289. 

14 

_Reliability Engineering and System Safety 267 (2026) 111890_ 

- [72] Halligan S, Altman DG, Mallett S. Disadvantages of using the area under the receiver operating characteristic curve to assess imaging tests: a discussion and proposal for an alternative approach. Eur Radiol Mar. 2015;25(4):932. https://doi. org/10.1007/S00330-014-3487-0. 

- [73] Hand DJ. Measuring classifier performance: a coherent alternative to the area under the ROC curve. Mach Learn Oct. 2009;77(1):103–23. https://doi.org/ 10.1007/s10994-009-5119-5. 

- [74] Laxhammar R, Falkman G. Inductive conformal anomaly detection for sequential detection of anomalous sub-trajectories. Ann Math Artif Intell Jun. 2015;74(1–2): 67–94. https://doi.org/10.1007/s10472-013-9381-7. 

- [75] Bates S, Cand`es E, Lei L, Romano Y, Sesia M. Testing for outliers with conformal p- values. Ann Stat Feb. 2023;51(1). https://doi.org/10.1214/22-AOS2244. 

- [76] A.N. Angelopoulos and S. Bates, “A gentle introduction to conformal prediction and distribution-free uncertainty quantification,” Jul. 2021, Accessed: Jan. 09, 2024. [Online]. Available: http://arxiv.org/abs/2107.07511. 

- [77] Dvoretzky A, Kiefer J, Wolfowitz J. Asymptotic minimax character of the sample distribution function and of the classical. Ann Math Stat 1956;27(3):642–69. Accessed: Feb. 24, 2025. [Online]. Available: https://www.jstor.org/stable/ 2237374. 

- [78] Massart P. The tight constant in the Dvoretzky-Kiefer-Wolfowitz inequality. Ann Probab 1990;18(3):1269–83. Accessed: Feb. 24, 2025. [Online]. Available: https:// www.jstor.org/stable/2244426. 

- [79] Sarkar SK. Generalizing Simes’ test and Hochberg’s stepup procedure. Ann Stat Feb. 2008;36(1):337–63. https://doi.org/10.1214/009053607000000550. 

- [80] Eicker F. The asymptotic distribution of the suprema of the standardized empirical processes. Ann Stat Jan. 1979;7(1). https://doi.org/10.1214/aos/1176344559. 

- [81] Downs JJ, Vogel EF. A plant-wide industrial process control problem. Comput Chem Eng Mar. 1993;17(3):245–55. https://doi.org/10.1016/0098-1354(93) 80018-I. 

- [82] Rieth CA, Amsel BD, Tran R, Cook MB. Additional Tennessee Eastman process simulation data for anomaly detection evaluation. Harv Dataverse 2017. https:// doi.org/10.7910/DVN/6C3JR1. 

- [83] Qin SJoe. Statistical process monitoring: basics and beyond. J Chemom Aug. 2003; 17(8–9):480–502. https://doi.org/10.1002/cem.800. 

- [84] Tan R, Ottewill JR, Thornhill NF. Monitoring statistics and tuning of kernel principal component analysis with radial basis function kernels. IEEE Access 2020; 8:198328–42. https://doi.org/10.1109/ACCESS.2020.3034550. 

- [85] Diallo AR, Homri L, Dantan J-Y, Bonnet F, Boeuf T. Enhancing fault diagnosis in process industries with internal variables of model predictive control. IFAC-Pap 2024;58(4):538–43. https://doi.org/10.1016/j.ifacol.2024.07.274. 

15 

