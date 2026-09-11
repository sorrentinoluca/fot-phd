# **Structure-Aware Unsupervised Anomaly Detection for Spacecraft Telemetry with Adaptive EVT Thresholding** 

Óscar Alcarria<sup>∗1</sup> , Rafael Sánchez<sup>†1</sup> , Javier Sempere<sup>2</sup> , Pablo Torrijos<sup>1</sup> , Juan C. Alfaro<sup>1</sup> , Juan M. Auñón<sup>3</sup> , José A. Gámez<sup>1</sup> , José M. Puerta<sup>1</sup> 

> 1 _Universidad de Castilla-La Mancha, Albacete, Spain_ 

> 2 _GMV GmbH, Darmstadt, Germany_ 

> 3 _GMV, Madrid, Spain_ 

**Operational anomaly detection in spacecraft telemetry typically requires labeled historical anomalies or extended warm-up periods. These requirements are rarely met in practice. We propose an unsupervised, deployment-ready framework that produces predictions from the second month of operation without any labels, prior fault knowledge, or mission-specific tuning. The approach combines incremental monthly retraining, statistical model selection, and adaptive Extreme Value Theory (EVT) thresholding for false alarm control. On the ESA Anomalies Dataset (ESAAD), it achieves** _F_ 0 _._ 5 = 0 _._ 700 **on Mission 1 and** _F_ 0 _._ 5 = 0 _._ 698 **on Mission 2 under strict chronological evaluation.** 

## **1 Introduction** 

Anomaly detection in spacecraft telemetry involves identifying off-nominal behavior in multivariate, non-stationary time series under strict operational constraints. In practice, mission control environments rarely provide complete labeled fault histories, dedicated GPU hardware, or years of accumulated telemetry before monitoring must begin. 

The European Space Agency (ESA) Anomalies Dataset (ESA-AD) [1] is the most comprehensive publicly available benchmark for anomaly detection in spacecraft telemetry, providing expert-annotated data from three complete ESA missions with a hierarchical event-wise evaluation pipeline. Two missions are used for benchmarking: Mission 1 (M1) features 76 telemetry channels (58 target) with 118 anomalies and 78 rare nominal events; Mission 2 (M2) features 100 channels (47 target) with 31 anomalies and 613 rare nominal events. 

An exploratory analysis of the ESA-AD reveals marked statistical differences across missions, suggesting that a single modeling strategy may not generalize consistently. We propose a structure-aware framework that: (1) selects the detection paradigm based on mission-level statistical properties; (2) integrates incremental monthly retraining for deployment from the second month of operation; and (3) applies adaptive Extreme Value Theory (EVT)-based thresholding for robust, precision-oriented event-wise anomaly 

> ∗Corresponding author. E-Mail: oscar.alcarria@uclm.es 

> †Corresponding author. E-Mail: rafael.sanchez@uclm.es 

detection. Without labels, GPU hardware, or extensive historical data, the framework matches or surpasses industrial supervised baselines on ESA-AD. 

## **2 Methodology** 

### **2.1 Problem Definition and Constraints** 

We address the detection of anomalous events in multivariate satellite telemetry under fully anonymized conditions, preventing the use of mission-specific semantics or physicsbased priors. Following the ESA Benchmark for Anomaly Detection in Satellite Telemetry (ESA-ADB) [1] definition, anomalies are modeled as contiguous off-nominal temporal segments rather than isolated outliers. To reflect realistic deployment constraints [2], our framework operates without labels or GPU hardware and is evaluated under a chronological incremental setup that preserves temporal causality and avoids information leakage. Performance is measured using the corrected event-wise _F_ 0 _._ 5 score [1], where _β_ = 0 _._ 5 weights precision higher than recall and the event-wise precision is corrected by the sample-level true negative rate to penalize algorithms that over-flag nominal periods. 

Figure 1 summarizes the proposed workflow, from preprocessing and monthly incremental learning to structureaware model selection, adaptive EVT thresholding, and post-detection anomaly grouping. 

### **2.2 Data Preprocessing** 

Following the preprocessing protocol in [2], the asynchronous and irregularly sampled telemetry channels are first combined over their original timestamps, producing a sparse multivariate time series. Each channel is then processed independently: missing entries are discarded and the remaining observations are projected onto a missionspecific uniform grid with sampling intervals of 30 s for M1 and 18 s for M2. Zero-order hold interpolation is applied, such that each grid timestamp receives the most recently observed channel value. To prevent short annotated 

> © 2026 Ó. Alcarria, R. Sánchez et al., licenced via CC BY 4.0. 

3<sup>rd</sup> Conference on AI in and for Space (SPAICE 2026) 


![](Structure-Aware_Unsupervised_Anomaly_Detection_for_Spacecraft_Telemetry_with_Adaptive_EVT_Thresholding_images/Structure-Aware_Unsupervised_Anomaly_Detection_for_Spacecraft_Telemetry_with_Adaptive_EVT_Thresholding.pdf-0002-00.png)


**Figure 1:** Overview of the proposed structure-aware anomaly detection framework. 

events from disappearing during temporal discretization, a channel-aware preservation procedure is applied after resampling. For each grid interval overlapping an event annotation, the last original telemetry value recorded within the annotated interval is copied to the following grid timestamp. The resampled channels are subsequently aligned on the common temporal grid and concatenated into a single multivariate series. Finally, event labels are assigned using inclusive start and end times, with samples encoded as normal ( _y_ = 0), rare event ( _y_ = 1), or anomaly ( _y_ = 2); anomalies take precedence when annotated intervals overlap. The resulting dataset is verified to contain a regular datetime index and no missing values. 

### **2.3 Incremental Learning Setup** 

Instead of relying on the static partitioning from ESA-ADB, we implement an incremental learning strategy utilizing a monthly sliding window. In this setup, the model is trained exclusively on the previous month’s data and evaluated on the subsequent month, allowing for deployment from the very first available period without the need for large historical datasets. This strategy is well suited to operational environments, as it allows the detector to adapt progressively to changes in telemetry behavior over time and aligns with the update cycles typically found in production monitoring systems. 

### **2.4 Mission Characterization** 

To characterize the missions and guide the selection of appropriate anomaly detection models, we conducted a 

comparative statistical analysis on the complete datasets of both missions from the ESA-ADB benchmark, including nominal, rare, and anomalous events. 

First, the Energy Distance [3] between M1 and M2 is 4 _._ 33, indicating substantial multivariate distributional differences. Statistical significance was assessed via a permutation test (200 permutations) [4], in which mission labels were randomly reassigned while preserving sample sizes. No permuted statistic exceeded the observed value ( _p <_ 0 _._ 005), confirming the absence of a shared statistical structure between missions. For each mission, the coefficient of variation (CV) was computed independently for each sensor as the ratio of its standard deviation to its absolute mean, and subsequently averaged across all numerical variables. This analysis reveals low variability in M1 (CV= 0 _._ 13), consistent with relatively stable dynamics, whereas M2 exhibits markedly higher variability (CV= 1 _._ 27), reflecting greater overall dispersion across sensors. 

Clustering structure was evaluated using K-means [5] with Euclidean distance on standardized features, exploring multiple values of _k_ . The Silhouette coefficient [6] (inset in Fig. 2) yields consistently higher scores for M2, suggesting more compact and well-separated clusters, while M1 displays weaker intrinsic segmentation. Principal Component Analysis (PCA) projections [7] (Fig. 2) obtained by fitting PCA on M1 and applying the transformation to both missions, further reinforce this distinction. The first two principal components explain 33.35% and 19.14% of the total variance, respectively. In this shared subspace, M1 presents a largely continuous and overlapping distribution structured around a limited number of principal lin- 

3<sup>rd</sup> Conference on AI in and for Space (SPAICE 2026) © 2026 Ó. Alcarria, R. Sánchez et al., licenced via CC BY 4.0. 

ear directions, whereas M2 exhibits more separated dense regions and isolated low-density areas, consistent with stronger local clustering structure and variance distributed across multiple dimensions. 


![](Structure-Aware_Unsupervised_Anomaly_Detection_for_Spacecraft_Telemetry_with_Adaptive_EVT_Thresholding_images/Structure-Aware_Unsupervised_Anomaly_Detection_for_Spacecraft_Telemetry_with_Adaptive_EVT_Thresholding.pdf-0003-01.png)


**Figure 2:** PCA projection of Mission 1 (M1) and Mission 2 (M2). The model is fitted exclusively on M1 using all its variables, which are common to M2. The inset shows the Silhouette score as a function of the number of clusters ( _k_ ). 

Overall, these observations motivate the hypothesis that in M1 anomalous behavior may manifest as subtle deviations embedded within stable dynamics, whereas in M2 anomalies may align with clearer structural separations. The statistical analysis rules out a single-model approach and motivates a structure-driven selection. Generic standalone models (e.g. single local-density detector or autoencoder) performed poorly in preliminary experiments, confirming that tailored strategies are required to accommodate mission variability. 

### **2.5 Model Selection and Training** 

The model selection strategy is directly informed by the statistical characterization presented in the previous phase. Since the two missions exhibit fundamentally different statistical structures, distinct modeling approaches are adopted within the same methodological framework. 

#### **2.5.1 Temporal Reconstruction Model** 

M1 is characterized by low variability and a weak intrinsic clustering structure. These properties suggest that anomalies are likely to manifest as subtle temporal deviations embedded within otherwise stable signals. Accordingly, an unsupervised Long Short-Term Memory (LSTM) autoencoder [8] is employed. This architecture enables the capture of both temporal dynamics and nonlinear relationships among variables, which is essential in scenarios characterized by stable signals and low-magnitude anomalies. For each input sequence **x** _t ∈_ R<sup>_L×F_</sup> , where _L_ is the sequence length and _F_ is the number of features, the model reconstructs the input as **x** ˆ _t_ . 

To comply with CPU-only constraints and monthly incremental retraining, a lightweight LSTM autoencoder is adopted. Sequences of length _L_ = 64 are processed by a single-layer architecture with 64 hidden units and a 16dimensional latent space, limiting model capacity to reduce overfitting and ensure efficient retraining. The model is optimized with Adam (learning rate 10<sup>_−_3</sup> ) for up to 30 epochs, with a batch size of 128. Early stopping (patience = 3) monitors the training reconstruction loss and triggers in most monthly windows, indicating that convergence typically occurs before the epoch limit. Prior to each training cycle, robust sample-level filtering based on the Median Absolute Deviation (MAD) is applied to reduce the influence of outliers on the learned reconstruction patterns. 

The reconstruction error for each sequence is quantified as mean squared error (MSE): 


![](Structure-Aware_Unsupervised_Anomaly_Detection_for_Spacecraft_Telemetry_with_Adaptive_EVT_Thresholding_images/Structure-Aware_Unsupervised_Anomaly_Detection_for_Spacecraft_Telemetry_with_Adaptive_EVT_Thresholding.pdf-0003-10.png)


The resulting anomaly scores _{st}_ may shift across temporal windows due to non-stationary system dynamics, making fixed thresholds unreliable. An initial threshold is set at the 98th percentile of the training reconstruction error and subsequently refined through the adaptive EVTbased procedure described in Section 2.6. 

#### **2.5.2 Clustering-Based Framework** 

M2 exhibits high variability, pronounced clustering structure, and variance distributed across multiple dimensions. These characteristics indicate the presence of well-defined operational regimes and locally structured state spaces. To exploit this structure, a clustering-based anomaly detection framework is adopted. The pipeline consists of: (1) Robust scaling and preliminary unsupervised filtering of extreme outliers as in the previous model; (2) PCA-based dimensionality reduction to learn a compact representation of nominal behavior; (3) K-means clustering to model operational regimes in the reduced subspace; (4) Local Outlier Factor (LOF) [9] to quantify local density deviations; and (5) a combined anomaly score integrating regime proximity and local density information. 

PCA reduces dimensionality while preserving the dominant structure of normal operation. K-means captures recurrent operational modes, and LOF evaluates the degree of local deviation within each regime. The anomaly score combines the LOF novelty score with the distance to the nearest cluster centroid in the PCA subspace, giving LOF (0.7) a higher weight than centroid distance (0.3), thereby prioritizing local density distortions while retaining sensitivity to global regime shifts. 

Hyperparameters are automatically inferred from each training window without supervised tuning. PCA dimensionality is set to explain 95% cumulative variance. The number of clusters is estimated using the Gap Statistic [10] within a data-dependent range, and the LOF neighborhood 

3<sup>rd</sup> Conference on AI in and for Space (SPAICE 2026) © 2026 Ó. Alcarria, R. Sánchez et al., licenced via CC BY 4.0. 

size scales with<sup>_√_</sup> _<u>n</u>_ and the reduced dimensionality to ensure stable density estimation. Anomaly scores are first calibrated using the 98th percentile before applying the dynamic thresholding procedure described in Section 2.6. 

### **2.6 EVT-Based Dynamic Thresholding** 

Because anomaly-score distributions may vary across temporal windows, fixed thresholds can become unreliable. We therefore apply a peaks-over-threshold EVT procedure [11], which adapts the threshold to the upper tail of the calibration-score distribution. 

For window _k_ , let _Sk_ = _{sk,_ 1 _, . . . , sk,nk }_ denote the calibration scores and define the preliminary threshold as _uk_ = _Qq_ ( _Sk_ ), where _Qq_ is the empirical quantile of order _q_ . The excesses _Yk_ = _{sk,i − uk | sk,i > uk}_ are fitted by maximum likelihood to a Generalized Pareto Distribution (GPD) with shape _ξk_ and scale _σk >_ 0, provided that _nu,k_ = _|Yk| ≥ N_ min. Let _pu,k_ = _nu,k/nk_ be the empirical probability of exceeding _uk_ . For a target upper-tail probability _α_ , the resulting threshold is 


![](Structure-Aware_Unsupervised_Anomaly_Detection_for_Spacecraft_Telemetry_with_Adaptive_EVT_Thresholding_images/Structure-Aware_Unsupervised_Anomaly_Detection_for_Spacecraft_Telemetry_with_Adaptive_EVT_Thresholding.pdf-0004-04.png)


cision with moderate recall, yielding _F_ 0 _._ 5 = 0 _._ 700. This conservative behavior is operationally desirable: the framework flags fewer events but with high confidence, minimizing unnecessary operator interventions. In M2, the tradeoff is more balanced ( _F_ 0 _._ 5 = 0 _._ 698), detecting a larger proportion of anomalies at the cost of lower precision. 

|**Metric**|**Mission 1 (M1)**|**Mission 2 (M2)**|
|---|---|---|
|Event-wise Precision|0.852|0.721|
|Event-wise Recall|0.408|0.621|
|Event-wise_F_0_._5|0.700|0.698|
|True Negative Rate|0.977|0.801|



**Table 1:** Global event-wise performance for M1 and M2. 

Figs. 3 and 4 show the temporal evolution of the cumulative corrected _F_ 0 _._ 5. In M1, anomalous and rare events concentrate heavily in 2000, predominantly in event class 22 [1, Fig 1], and become sparser afterwards. The _F_ 0 _._ 5 curve reflects this: scores above 0.9 during the initial dense period, gradually stabilizing between 0.7 and 0.8 as anomalies disperse across classes. In M2, event classes are more constant throughout the mission. The cumulative _F_ 0 _._ 5 drops briefly during the first months but recovers quickly, stabilizing around 0.7 with narrower oscillations. 

where _ε_ handles the limiting case _ξk ≈_ 0. If fewer than 

_N_ min excesses are available or the GPD fit is invalid, the empirical quantile _Q_ 1 _−α_ ( _Sk_ ) is used as fallback. 

To prevent abrupt variations between consecutive windows, we first compute the exponentially smoothed threshold _T_<sup>�</sup> _k_ = _λT_ EVT _,k_ + (1 _− λ_ ) _Tk−_ 1. Its relative change is then limited to _δ_ : 


![](Structure-Aware_Unsupervised_Anomaly_Detection_for_Spacecraft_Telemetry_with_Adaptive_EVT_Thresholding_images/Structure-Aware_Unsupervised_Anomaly_Detection_for_Spacecraft_Telemetry_with_Adaptive_EVT_Thresholding.pdf-0004-12.png)


A score is classified as anomalous when _sk,t > Tk_ . All 

hyperparameters were fixed a priori without label-based optimization: _q_ = 0 _._ 98, _α_ = 0 _._ 01, _N_ min = 30, and _λ_ = _δ_ = 0 _._ 05. Thus, the GPD models the most extreme 2% of scores, requires at least 30 excesses, and limits threshold changes to 5% per window. Here, _α_ is a target upper-tail exceedance probability, not a guaranteed false-positive rate. 

### **2.7 Post-detection Anomaly Grouping** 

Following operational practice [2], detected anomalies separated by less than 6 hours are consolidated into a single event, reducing redundant alarms and improving diagnostic clarity. This threshold reflects expert recommendations from satellite operations centers. 

## **3 Results** 

Table 1 summarizes the global event-wise performance for both missions. In M1, the framework achieves high pre- 


![](Structure-Aware_Unsupervised_Anomaly_Detection_for_Spacecraft_Telemetry_with_Adaptive_EVT_Thresholding_images/Structure-Aware_Unsupervised_Anomaly_Detection_for_Spacecraft_Telemetry_with_Adaptive_EVT_Thresholding.pdf-0004-19.png)


**Figure 3:** Cumulative corrected _F_ 0 _._ 5 over time for Mission 1. The labels Anom., Rare, and Com. G. denote anomalous events, rare nominal events, and communication gaps, respectively. 

**Figure 4:** Cumulative corrected _F_ 0 _._ 5 over time for Mission 2. The labels Anom., Rare, and Com. G. denote anomalous events, rare nominal events, and communication gaps, respectively. 

3<sup>rd</sup> Conference on AI in and for Space (SPAICE 2026) © 2026 Ó. Alcarria, R. Sánchez et al., licenced via CC BY 4.0. 

**Comparison with existing baselines.** Within the ESAAD ecosystem, industrial unsupervised solutions such as [2] have reported event-wise _F_ 0 _._ 5 scores of 0.424 for Mission 1 and 0.882 for Mission 2 under static train/test configurations. In comparison, the proposed framework yields substantially improved results in Mission 1 while maintaining competitive performance in Mission 2. Importantly, these results are obtained under a strictly incremental monthly retraining scheme from the first available period, without reliance on extended historical partitions or mission-specific hyperparameter tailoring, and within a fully deployment-oriented configuration. 

For a broader context, [1] reports results under a static 50/50 train/test split. Using all channels, the best models achieve _F_ 0 _._ 5 = 0 _._ 061 for M1 and _F_ 0 _._ 5 = 0 _._ 241 for M2. Supervised approaches with channel-subset selection reach _F_ 0 _._ 5 = 0 _._ 786 and _F_ 0 _._ 5 = 0 _._ 949, respectively. Although not directly comparable, our framework achieves _F_ 0 _._ 5 = 0 _._ 700 and _F_ 0 _._ 5 = 0 _._ 698 without any label or channel selection, substantially narrowing the gap with supervised methods. This is particularly significant for M1, where existing unsupervised baselines struggle most. 

**Computational Cost.** Under identical hardware constraints, using CPU-only execution and 16 GB of RAM, M1 evaluation over 161 monthly windows required 27.5 epochs/window on average, with a mean retraining time of 1041.71 s/window (total: 46.64 h) and peak memory averaging 7.72 GB (max: 8.11 GB). M2 evaluation over 40 monthly windows required 214.65 s/window (total: 2.5 h) and peak memory averaging 0.54 GB (max: 1.09 GB). No inter-window memory accumulation was observed in either mission. 

## **4 Discussion** 

Although the framework is evaluated under a strictly incremental regime, the exploratory analysis in Section 2.4 is performed on the complete mission datasets exclusively for descriptive purposes, to evidence global statistical differences and justify the choice of different model families. It is not used for hyperparameter tuning, threshold calibration, or any label-dependent decision. In operational scenarios, a short warm-up phase with generic detectors can be used to accumulate historical data, after which a statistical assessment restricted to the observed period may guide model selection without introducing information leakage. This separation between statistical characterization and operational training preserves chronological validity while retaining the benefits of structure-aware model selection. 

Hyperparameters were selected using standard practices rather than supervised optimization, consistent with the fully unsupervised deployment scenario. When labeled historical data are available, the framework could be extended using automated machine learning (AutoML) strate- 

gies [12] to jointly optimize model architectures, hyperparameters, and thresholds via systematic search procedures guided by event-wise _F_ 0 _._ 5. This would enable adaptive, reproducible model selection across missions, reducing manual-tuning bias. 

## **5 Acknowledgments** 

This work was carried out within the framework of the INCIBE project _AI- and ML-Based Behavioural Anomaly Detection Module_ , ref. 250120UCTR-INCIBE (SIMD-I3A Laboratory), with additional support through technical assistance contracts funded by GMV Soluciones Globales Internet, S.A. 

This work was also partially funded by the University of Castilla-La Mancha and the European Regional Development Fund (ERDF), ”A Way of Making Europe”, under project 2025-GRIN-38476. 

## **References** 

1. Kotowski, K. _et al. European Space Agency Benchmark for Anomaly Detection in Satellite Telemetry_ 2025. arXiv: 2406.17826 [cs.LG]. 

2. Tejedor, M., Jiménez, H., Pozo, J. A., Perea, I. & Auñón, J. M. _Enhancing Space Operations with Unsupervised Anomaly Detection: The PitIA System_ in _Proceedings of the 2025 conference on Big Data from Space (BiDS’25)_ (eds Kempeneers, P., Lumnitz, S. & Albani, S.) (Publications Office of the European Union, Luxembourg, 2025), 57–60. isbn: 978-92-68-31935-2. 

3. Székely, G. J. & Rizzo, M. L. Energy statistics: A class of statistics based on distances. _Journal of Statistical Planning and Inference_ **143,** 1249–1272. issn: 0378-3758 (2013). 

4. Good, P. I. _Permutation, Parametric and Bootstrap Tests of Hypotheses_ 3rd. isbn: 978-0-387-20279-2 (Springer, New York, 2005). 

5. MacQueen, J. _Some Methods for Classification and Analysis of Multivariate Observations_ in _Proceedings of the Fifth Berkeley Symposium on Mathematical Statistics and Probability_ **1** (University of California Press, Berkeley, CA, 1967), 281–297. 

6. Rousseeuw, P. J. Silhouettes: A graphical aid to the interpretation and validation of cluster analysis. _Journal of Computational and Applied Mathematics_ **20,** 53–65. issn: 0377-0427 (1987). 

7. Hotelling, H. Analysis of a Complex of Statistical Variables into Principal Components. _Journal of Educational Psychology_ **24,** 417– 441 (1933). 

8. Malhotra, P. _et al._ LSTM-based Encoder-Decoder for Multi-sensor Anomaly Detection. arXiv: 1607.00148 [cs.AI] (2016). 

9. Breunig, M., Kröger, P., Ng, R. & Sander, J. _LOF: Identifying DensityBased Local Outliers._ in. **29** (June 2000), 93–104. 

10. Tibshirani, R., Walther, G. & Hastie, T. Estimating the Number of Clusters in a Data Set Via the Gap Statistic. _Journal of the Royal Statistical Society Series B: Statistical Methodology_ **63,** 411–423. issn: 1369-7412 (Jan. 2002). 

11. Siffer, A., Fouque, P.-A., Termier, A. & Largouet, C. _Anomaly Detection in Streams with Extreme Value Theory_ in _Proceedings of the 23rd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining_ (Association for Computing Machinery, Halifax, NS, Canada, 2017), 1067–1075. isbn: 9781450348874. 

12. _Automated Machine Learning: Methods, Systems, Challenges_ (eds Hutter, F., Kotthoff, L. & Vanschoren, J.) isbn: 978-3-030-05317-8 (Springer International Publishing, Cham, 2019). 

3<sup>rd</sup> Conference on AI in and for Space (SPAICE 2026) © 2026 Ó. Alcarria, R. Sánchez et al., licenced via CC BY 4.0. 

