
![](RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process_images/RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process.pdf-0001-00.png)


## **Connection Science** 

**ISSN: 0954-0091 (Print) 1360-0494 (Online) Journal homepage: www.tandfonline.com/journals/ccos20** 


![](RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process_images/RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process.pdf-0001-03.png)


# **RBC-AD: conformal anomaly detection with explicit false-alarm control for the Tennessee Eastman Process** 

#### **Muhammad Mudasir , Yousef Asiri , Iqra Ameer , Mana Saleh Al Reshan , Hamad Almansour , Kamran Ahmad Awan & Asadullah Shaikh** 

**To cite this article:** Muhammad Mudasir , Yousef Asiri , Iqra Ameer , Mana Saleh Al Reshan , Hamad Almansour , Kamran Ahmad Awan & Asadullah Shaikh (2026) RBC-AD: conformal anomaly detection with explicit false-alarm control for the Tennessee Eastman Process, Connection Science, 38:1, 2707826, DOI: 10.1080/09540091.2026.2707826 

**To link to this article:** <u>https://doi.org/10.1080/09540091.2026.2707826</u> 


![](RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process_images/RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process.pdf-0001-08.png)



![](RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process_images/RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process.pdf-0001-09.png)



![](RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process_images/RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process.pdf-0001-10.png)



![](RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process_images/RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process.pdf-0001-11.png)



![](RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process_images/RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process.pdf-0001-12.png)



![](RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process_images/RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process.pdf-0001-13.png)


© 2026 The Author(s). Published by Informa UK Limited, trading as Taylor & Francis Group. 

Published online: 26 Jul 2026. 


![](RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process_images/RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process.pdf-0001-16.png)


Submit your article to this journal 

Article views: 355 


![](RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process_images/RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process.pdf-0001-19.png)


View related articles 


![](RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process_images/RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process.pdf-0001-21.png)


View Crossmark data 

Full Terms & Conditions of access and use can be found at https://www.tandfonline.com/action/journalInformation?journalCode=ccos20 

CONNECTION SCIENCE 2026, VOL. 38, NO. 1, 2707826 https://doi.org/10.1080/09540091.2026.2707826 

###### RESEARCH ARTICLE 


![](RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process_images/RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process.pdf-0002-02.png)


### **RBC-AD: conformal anomaly detection with explicit false-alarm control for the Tennessee Eastman Process** 

Muhammad Mudasir<sup>a</sup> , Yousef Asiri<sup>b</sup> , Iqra Ameer<sup>c</sup> , Mana Saleh Al Reshan<sup>d,e</sup> , Hamad Almansour<sup>f</sup> , Kamran Ahmad Awan<sup>a</sup> and Asadullah Shaikh<sup>d,e</sup> 

aFaculty of Information Technology & Numerical Sciences, The University of Haripur, Haripur, Pakistan; bDepartment of Computer Science, Najran University, Najran, Saudi Arabia;<sup>c</sup> Division of Science, Engineering, and Technology, The Pennsylvania State University, Pennsylvania, PA, USA;<sup>d</sup> Department of Information Systems, Najran University, Najran, Saudi Arabia;<sup>e</sup> Emerging Technologies Research Lab (ETRL), Najran University, Najran, Saudi Arabia;<sup>f</sup> Department of Information Systems, Applied College, Najran University, Saudi Arabia 

###### **ABSTRACT** 

Fault detection in the Tennessee Eastman Process (TEP) is challenged by transient dynamics, post-injection regime transitions, and score drift that destabilize fixedthreshold detectors and increase false alarms. In the proposed Risk-Budgeted Conformal Anomaly Detection (RBC-AD) framework, a calibration-based anomaly detector integrates a causal forecasting backbone, frequency-aware scoring, and conformal decisioning. The forecaster is a dilated temporal convolutional network with causal selfattention, trained on fault-free runs to predict one-step-ahead Gaussian parameters by minimizing negative log-likelihood. Detection then scores each window using a fused nonconformity measure that combines the window-averaged predictive log-likelihood with an FFT-based frequency deviation term, using robust normalization fitted on a held-out calibration split and tuning the fusion weight under leakage-controlled splits. Conformal quantiles at miscoverage level = 0.05 define normal, uncertain, and anomaly states with finite-sample correction. Run-level partitioning over 500 runs per split and post-injection sampling (3,000 normal windows, 8,000 fault windows) achieves ROC-AUC = 1.000 and PR-AUC = 1.000 under the post-injection-only protocol; fullstream results provide the deployment-relevant assessment. Static conformal thresholds ( _u_ = 0.1977, _a_ = 0.3033) yield F1 = 0.9989 and F1 = 0.9999. Deployment selects an uncertainty threshold to satisfy an empirical normal alarm-rate target of 0.05. Fullstream evaluation reports uncertainty rate and detection delay under _k_ -consecutive alarm logic, with optional drift-triggered recalibration using normal-stream scores. 

###### **ARTICLE HISTORY** 

Received 12 May 2026 Accepted 17 July 2026 

###### **KEYWORDS** 

Tennessee Eastman Process; anomaly detection; conformal prediction; FAR control; temporal convolutional network 

##### **1. Introduction** 

Chemical and industrial plants rely on dense instrumentation and automated control loops that connect process sensors, manipulated variables, and supervisory controllers within continuous monitoring and actuation infrastructures (Colosimo et al., 2024; Vermesan et al., 2022). These infrastructures generate highfrequency measurements of plant state and support control actions needed to maintain product quality, safety constraints, and throughput under time-varying operating loads (Chen et al., 2020; Li et al., 2022). As automation shifts toward distributed and edge-enabled architectures, fault detection becomes a core requirement for streaming process telemetry (Chiang et al., 2022; Liu et al., 2025). Process-monitoring research has moved from single-model statistical schemes toward hybrid fusion paradigms that combine data-driven learning, process knowledge, uncertainty handling, and multi-source information for more reliable detection in complex industrial systems (Ali et al., 2025). The same review identifies calibration, uncertainty quantification, fusion architecture design, and deployment governance as unresolved requirements for advanced process monitoring. These requirements are directly connected to false-alarm control and stream-level validation in industrial anomaly detection. Sensor noise, cross-variable dependence, 

> © 2026 The Author(s). Published by Informa UK Limited, trading as Taylor & Francis Group. This is an Open Access article distributed under the terms of the Creative Commons Attribution License (http://creativecommons.org/licenses/by/4.0/), which permits unrestricted use, distribution, and reproduction in any medium, provided the original work is properly cited. The terms on which this article has been published allow the posting of the Accepted Manuscript in a repository by the author(s) or with their consent. 

**CONTACT** Iqra Ameer iqa5148@psu.edu Division of Science, Engineering, and Technology, The Pennsylvania State University, Pennsylvania, PA, USA 

2 M. MUDASIR ET AL. 

controller compensation, and scheduled setpoint changes produce multivariate dynamics in which abnormal behaviour can overlap with admissible transient responses (Ren et al., 2023; Wu et al., 2021; Yerimah et al., 2022). Fault signatures may appear gradually, change after injection, or propagate indirectly through coupled variables, which constrains fixed-threshold detectors and pointwise alarm rules (Ahmed et al., 2025; Chen et al., 2020). Missed detections can lead to unsafe operation and equipment damage, whereas excessive false alarms increase operator workload, create alarm fatigue, and delay corrective action (Jalilibal et al., 2023). Industrial fault detection therefore requires temporal modelling, stable behaviour across regime transitions, calibrated uncertainty handling, and explicit control of false-alarm behaviour during continuous-stream deployment (Farzaneh & Simeone, 2025; Tajmouati et al., 2024). 

###### **_1.1. Motivation and problem statement_** 

The Tennessee Eastman Process (TEP) is a benchmark chemical process widely used to evaluate fault detection and process monitoring methods (Downs & Vogel, 1993; Reinartz et al., 2021). It represents a closed-loop industrial plant with interconnected units, including a reactor, condenser, vapour-liquid separator, stripper, compressor, recycle loop, feed streams, and product streams (Downs & Vogel, 1993; Ricker, 1996). The process contains strong interactions between measured process variables and manipulated control variables. A fault introduced in one unit may therefore propagate through several units before it becomes clearly observable (Ricker, 1996; Tian & Hoo, 2005). This structure makes TEP suitable for evaluating anomaly detection under nonlinear dynamics, controller compensation, delayed fault propagation, and transient operating behaviour (Reinartz et al., 2021; Tian & Hoo, 2005). 

TEP formalises recurring difficulties in industrial fault monitoring, including high-dimensional sensing, cross-variable coupling, delayed fault effects, and regime transitions (Andersen et al., 2022; Reinartz et al., 2021). Measured departures from baseline behaviour often occur together with control-driven or loaddriven transients, which makes separation between abnormal dynamics and nominal process responses difficult (Heo & Lee, 2019; Xu et al., 2022). Recent integrated machine-learning monitoring for physiochemical process safety combines distributed correlation modelling, locality-preserving projection, and entropy-based information measures, with validation on distillation and TEP benchmarks (Ali et al., 2024). Multi-model fusion monitoring has also been proposed to combine DCCA, autoencoder representations, and reconstruction-based contribution analysis for complex physio-chemical systems (Ali et al., 2025). These studies indicate that current monitoring research increasingly uses fused learning structures for nonlinear, dynamic, and safety-critical processes. 

These developments leave several deployment-level limitations unresolved. Many deep-learning and machine-learning detectors still rely on fixed thresholds, implicit test-dependent tuning, or sampledwindow evaluation protocols that do not characterise continuous-stream alarm behaviour (Bakdi & Kouadri, 2018; Zhang et al., 2024). These choices can obscure false-alarm behaviour, reduce reproducibility, and inflate reliability estimates under deployment-relevant conditions (Zhou et al., 2024). Benchmark results therefore need to be interpreted with respect to threshold selection, calibration-data separation, and continuous alarm formation rather than isolated classification scores. In operating plants, alarm flooding and threshold instability reduce operator trust, particularly under regime shifts and distributional change (Huang et al., 2022; Yang et al., 2022). Practical monitoring systems require explicit false-alarm control, calibrated uncertainty states, and robustness to post-injection regime transitions without dependence on test-set tuning (Chakraborty & Finkelstein, 2024; Yang & Kuchibhotla, 2025). Existing approaches address these requirements only partially, leaving a gap between benchmark performance and deployable fault detection. 

###### **_1.2. Overview of Risk-Budgeted Conformal Anomaly Detection (RBC-AD)_** 

The RBC-AD framework combines probabilistic forecasting with calibrated scoring to support leakage-free fault detection under explicit alarm constraints in multivariate process streams (see Figure 1). One-stepahead dynamics are modelled using a causal dilated temporal convolutional network with residual blocks that outputs Gaussian parameters, enabling window-level likelihood scoring through negative loglikelihood (NLL). A frequency feature bank is fitted on calibration-normal windows to compute spectral 

CONNECTION SCIENCE 3 


![](RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process_images/RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process.pdf-0004-01.png)


**Figure 1.** Overview of the proposed RBC-AD framework for leakage-controlled fault detection under false-alarm constraints. 

deviation scores from windowed signals. These features are robustly normalised using median and MAD statistics estimated on the calibration-normal split. A fused detection score is defined as a weighted combination of normalised NLL and normalised frequency deviation, parameterised by a mixing weight selected on a dedicated tuning split to avoid calibration leakage. Conformal quantiles computed on calibration-normal windows determine an uncertainty threshold and an anomaly threshold, producing a three-state decision space (normal, uncertain, anomaly) for risk-aware monitoring. 

Deployment behaviour is specified through a false-alarm-rate (FAR) operating point derived from a normal-only stream. A FAR-controlled threshold is selected on calibration-normal trajectories using stream scoring with a fixed detection stride and optional smoothing, preserving separation between threshold selection and final reporting. During inference, sliding windows generate score sequences that are aggregated using _k_ -consecutive alarm logic to suppress spurious triggers and enable delay trade-offs. Root-cause attribution uses per-feature NLL contributions computed during inference. These contributions are then contextualised using a sparse dependency graph estimated from calibration-normal contribution statistics. This enables ranked variable reporting while accounting for correlation structure among process variables, rather than treating feature scores independently. The evaluation protocol reports sampledwindow discrimination and full-stream behaviour, including uncertainty rates, FAR compliance, and detection delay under post-injection trajectories. 

###### **_1.3. Contributions of this study_** 

This study provides methodological and evaluation contributions for fault detection in the Tennessee Eastman Process (TEP) under operational false-alarm constraints. This paper is classified as an original research article in applied process monitoring and industrial anomaly detection. Methodologically, it presents a calibration-based unsupervised anomaly detection framework for multivariate time-series process monitoring, with emphasis on false-alarm control, uncertainty-aware decisioning, and deployment-oriented evaluation. The contributions are as follows: 

4 

###### M. MUDASIR ET AL. 

- A risk-budgeted detection pipeline is presented that couples a causal dilated TCN forecaster with an auxiliary FFT-based frequency deviation module. Window-level Gaussian NLL and frequency scores are robustly normalised on calibration-normal data and fused into a single detection score using a tuned mixing weight, supporting consistent scoring across process variables and operating regimes. 

- A conformal calibration and decision layer is formulated to map the fused score to a three-state output (normal, uncertain, anomaly) with finite-sample correction at a specified significance level. A FARcontrolled deployment threshold is selected on a normal-only calibration stream to meet a target alarm rate, separating threshold selection from final test reporting and aligning the decision rule with alarm-management requirements. 

- A leakage-controlled run-level protocol is specified for fitting, validation, tuning, and calibration, with standardisation fitted on training-normal runs only. The evaluation reports sampled-window discrimination metrics, including ROC-AUC and PR-AUC, and full-stream behaviour, including precision, recall, uncertainty rates, and detection delay under _k_ -consecutive logic, enabling reproducible assessment under stream-like conditions. 

###### **_1.4. Structure of the article_** 

The remainder of this article is structured as follows. Section 2 surveys related work in industrial anomaly detection. Section 3 specifies the proposed RBC-AD framework. Section 4 details the experimental configuration and reports results on the TEP benchmark. Section 5 presents comparative analysis with existing approaches. Section 6 closes the paper. 

##### **2. Related work & background analysis** 

Fault and anomaly detection in the Tennessee Eastman Process (TEP) remain technically challenging because process variables are coupled, process dynamics are nonlinear, and fault effects may propagate with delay. Classical multivariate statistical monitoring methods, including PCA and distributed PCA variants, estimate dominant variance subspaces and detect deviations through SPE and _T_<sup>2</sup> statistics (Gao et al., 2022). These methods provide a linear variance-subspace formulation, but their linear and quasistationary assumptions can limit sensitivity to nonlinear faults and transient operating regimes. Qualityoriented Recursive-CPLS separates process-relevant and quality-relevant variation and supports recursive model updating; its decision layer, however, remains tied to linear latent structure and fixed decision rules (Hu et al., 2019). Graph-based predictable feature analysis represents multivariate temporal relations under correlated dynamics, although threshold stability under operating shifts remains unresolved (Fan et al., 2023). 

Deep learning methods address nonlinear sequence representation in process monitoring. Unsupervised deep anomaly detection benchmarks on TEP report F1 and AUPRC for reconstruction, forecasting, generative, and hybrid model families, but deployment calibration and stream-level false-alarm-rate control are not standardised (Hartung et al., 2023). LSTM-attention and dual-attention autoencoder models capture temporal and feature dependencies; most reported evaluations, however, use sampled windows and fixed operating points (Zeng et al., 2024; Zhao et al., 2025). Real-time schemes target low-latency detection, and dynamic-loss VAE models address sensitivity under heterogeneous conditions, but both remain dependent on method-specific thresholding (Attouri et al., 2024; Vijai & P, 2025). Fuzzy neural fault-detection models and adversarial TEP benchmarks extend robustness analysis, although uncertainty-aware calibration and nominal deployment control are treated as separate issues (Adeli & Mazinan, 2020; Pozdnyakov et al., 2024). 

Recent process-monitoring research has moved toward fusion-based and explainable learning structures. A hybrid causal-inference and neuro-fuzzy framework combines causal structure with adaptive neurofuzzy reasoning for advanced process monitoring, supporting interpretability while retaining modeldependent alarm selection (Ali et al., 2026). The DiGLPP–Kolmogorov–Arnold network framework develops fault representation for industrial chemical processes, although explicit conformal uncertainty and stream FAR control are not central components of its decision layer (Ali et al., 2026). Dynamic explainable fusion monitoring combines machine-learning fusion with contribution analysis for industrial and chemical processes, but deployment thresholds remain separate from finite-sample calibration (Ali et al., 2025). A 

CONNECTION SCIENCE 5 

**Table 1.** Comparison of representative TEP fault and anomaly detection approaches. 

|Ref.|Method|Key Limitation|
|---|---|---|
|Gao et al. (2022)|PCA-based distributed monitoring|Linear modelling assumption and fxed<br>thresholds|
|Hu et al. (2019)|Recursive-CPLS monitoring with model updating|Linear latent structure and limited<br>uncertainty handling|
|Fan et al. (2023)|Graph-based predictable feature analysis|<br>Threshold stability under operating shifts<br>not guaranteed|
|Hartung et al. (2023)|Deep anomaly detection benchmark on TEP|<br>Calibration and stream FAR control not<br>standardised|
|(Zeng et al.,2024; Zhao<br>et al.,2025)|Attention-based recurrent and autoencoder models|Sampled-window evaluation and fxed<br>operating points|
|(Attouri et al.,2024; Vijai &<br>P,2025)|Real-time and VAE-based anomaly detection|Deployment thresholding remains method-<br>dependent|
|<br>Ali et al. (2026)|Causal-inference and neuro-fuzzy monitoring|Alarm calibration remains model-dependent|
|Ali et al. (2026)|<br>DiGLPP–Kolmogorov–Arnold network fault detection|<br>Conformal uncertainty and stream FAR<br>control not addressed|
|Ali et al. (2025)|Dynamic explainable fusion monitoring|Explanation emphasised, with limited<br>bounded alarm control|
|Ali et al. (2025)|Reconstruction-based Bayesian dynamic fusion|Three-state deployment decisioning not<br>provided|
|**RBC-AD**|Probabilistic temporal model + frequency fusion + conformal<br>calibration|FAR-controlled, uncertainty-aware, stream-<br>evaluated|



reconstruction-based Bayesian fusion framework models dynamic industrial systems through probabilistic reconstruction, yet its evaluation does not directly address three-state alarm decisioning under leakagecontrolled calibration splits (Ali et al., 2025). This comparison indicates that recent fusion methods mainly address feature representation, diagnostic explanation, and model integration, whereas the alarm threshold is rarely formulated as an explicitly budgeted deployment parameter. For operator-facing monitoring, this distinction matters because high discrimination scores do not by themselves define acceptable alarm rates, uncertainty handling, or detection persistence in continuous streams. Table 1 summarises representative TEP fault and anomaly detection approaches. Existing methods address representation, fusion, diagnosis, and interpretability, but three deployment gaps remain: threshold selection is often fixed or implicitly tuned, uncertainty states are seldom formalised, and reported performance commonly emphasises window-level metrics without full-stream validation. RBC-AD targets these gaps through probabilistic temporal scoring, frequency-domain deviation cues, conformal calibration, FAR-controlled threshold selection, and continuous-stream evaluation. 

##### **3. Proposed methodology** 

This work implements a leakage-aware fault detection pipeline over Tennessee Eastman Process (TEP) multivariate time series, combining (i) windowed one-step-ahead probabilistic forecasting using a temporal convolution and causal self-attention model, (ii) a calibrated frequency-domain deviation score, (iii) robust score normalisation and convex score fusion, and (iv) conformal quantile thresholds with a three-state decision rule and a deployment operating point selected to satisfy an empirical false-alarm-rate (FAR) target on a normal score stream. Evaluation modules quantify detection delay, perform drift-triggered threshold recalibration, and compute feature-level root-cause rankings from per-sensor negative log-likelihood (NLL) contributions. 

###### **_3.1. Leakage-aware preprocessing, run-level splitting, and window reservoir sampling_** 

Each record contains metadata columns `simulationRun` , `sample` , and `faultNumber` , plus numeric sensor and actuator features identified by the prefix rule `xmeas` _ or `xmv` _, with a numeric fallback. For each dataframe, metadata columns are enforced, feature values are coerced to numeric, and duplicate keys `(simulationRun, sample)` are removed while preserving stable ordering by `(simulationRun, sample)` . 

Missing values are imputed using per-feature medians computed on the normal `train_fit` split only. Let _xr_ , _t_ , _f_<sup>denote feature</sup><sup>_f_at sample index</sup><sup>_t_in run</sup><sup>_r_. Let D</sup> fit<sup>be the set of rows in the normal training data</sup> restricted to runs assigned to `train_fit` . Define 

6 M. MUDASIR ET AL. 


![](RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process_images/RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process.pdf-0007-01.png)


In implementation, ± values are replaced with NaN before imputation. The imputation median for feature _f_ is 


![](RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process_images/RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process.pdf-0007-03.png)


All feature columns are stored as `float32` . Normal runs are partitioned into four disjoint run sets Rtrain, Rval, Rcal_thr, and Rcal_lam by shuffling unique run identifiers with a fixed random seed and applying the ratio tuple `NORMAL_RUN_SPLIT_TRAIN` . A feature standardiser is fit on cleaned normal `train_fit` data _F_ only. For feature vector **x** , scaling applies 


![](RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process_images/RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process.pdf-0007-05.png)


where ( , ) are the per-feature mean and standard deviation estimated on `train_fit` , and denotes elementwise division. A window extractor produces overlapping windows of length _W_ with stride _s_ . For a scaled run matrix **X** Û _r Tr_ × _F_ , windows are 

with 


![](RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process_images/RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process.pdf-0007-08.png)


To cap memory usage while preserving an unbiased sample of the window stream, normal windows are selected with reservoir sampling to a fixed capacity _N_ per split. Let { **X** _j_ } _Mj_ =1<sup>be the stream of candidate</sup> windows. For _j_ > _N_ , sample _u_ Unif{0, …, _j_ 1} and replace reservoir element _u_ if _u_ < _N_ . Fault datasets are stored by run. For each fault trajectory, window labels use the known injection time `INJECTION_ SAMPLE` . If a window start index is _ti_ , the binary label is 


![](RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process_images/RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process.pdf-0007-10.png)


The fault sampler optionally filters to post-injection windows only. Algorithm 1 formalises schema enforcement, leakage-safe imputation and scaling, run-level splitting, and window reservoir sampling. 

**Algorithm 1.** Leakage-aware preprocessing and window sampling. 


![](RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process_images/RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process.pdf-0007-13.png)


CONNECTION SCIENCE 7 

###### **_3.2. Probabilistic temporal forecaster and NLL training objective_** 

The temporal forecaster maps each window **X** _W_ × _F_ to one-step-ahead heteroscedastic Gaussian parameters aligned to next-step targets. The backbone comprises a causal temporal convolutional network (TCN) followed by causal multi-head self-attention. The TCN uses three `TemporalBlock` modules with channel widths (96, 96, 96), kernel size _k_ = 5, and dilations (1, 2, 4). Each block uses left padding and a Chomp1d operation to remove the padded suffix and enforce causality. After the TCN, a 1 × 1 convolution maps to attention width _D_ (ATTN_DIM), yielding latent sequence **Z** _B_ × _W_ × _D_ . Causal self-attention applies a boolean mask blocking access to future indices. For sequence length _T_ = _W_ , the mask is: **M** _ij_ = 1[ _j_ > _i_ ], _i_ , _j_ {1 ,…, _T_ }. (6) The final latent state is discarded to enforce one-step-ahead prediction over _t_ {1 ,…, _W_ 1}. Let _D_ **z** _t_ denote the attention output at time _t_ . Linear heads output _t_ = **W z** _t_ + **b** _F_ , _lt_ = **W** _l_ **z** _t_ + **b** _l F_ , _lt_ clip( _lt_ , _l_ min , _l_ max). (7) Training minimises Gaussian negative log-likelihood (NLL) averaged over batch, time, and feature dimensions. For a single time step and feature, with target _x_ and parameters ( , _l_ ) where _l_ = log 2, the per-datum NLL term is Lnll( _x_ ; , _l_ ) =<sup>1</sup> _l_ + exp( _l_ )( _x_ )2) +<sup>1).</sup> (8) 2<sup>(</sup> 2<sup>log(2</sup> 

**z** _t_ 

###### **_3.3. Dual-view anomaly scoring: temporal NLL, frequency deviation, robust normalisation, and fusion_** 


![](RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process_images/RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process.pdf-0008-05.png)


Calibration fits per-band mean and standard deviation on `X_cal_thr` , producing ( _b_ , _b_ )<sup>. Two addi-</sup> tional scalar frequency features are used. Half-spectrum flux compares magnitudes computed on the first and second halves of the window: 

_K F_ flux( **X** ) = _KF_<sup>1</sup> _k_ =1 _f_ =1 max (0, _Ak_ (2), _f Ak_ (1), _f_ ), (13) where _A_<sup>(1)</sup> and _A_<sup>(2)</sup> are FFT magnitudes computed from **X** 1:d _W_ /2t,: and **X** d _W_ /2t+1: _W_ ,:, respectively. Spectral entropy computes _pk_ , _f_ = _Ak_ , _f_ /( _k Ak_ , _f_ + ) and then averages 

8 M. MUDASIR ET AL. 


![](RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process_images/RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process.pdf-0009-01.png)


Equations (13) and (14) are standardised using `CAL_THR` mean and standard deviation. The frequency score is a fixed convex combination: 


![](RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process_images/RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process.pdf-0009-03.png)


Temporal and frequency scores are normalised using median and median absolute deviation (MAD) fit on `cal_thr` scores. For a score stream { _si_ } _ni_ =1<sup>, define</sup> 


![](RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process_images/RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process.pdf-0009-05.png)


Let _z_ temp ( **X** ) and _z_ freq ( **X** ) be the robust-normalised temporal and frequency scores. The fused score is a convex mixture with parameter [0, 1]: 


![](RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process_images/RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process.pdf-0009-07.png)


Optionally, a smoothing operator applies a moving average of width _L_ to the fused score sequence: 


![](RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process_images/RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process.pdf-0009-09.png)


When _L_ > 1, smoothing is implemented via convolution in `same` mode. The fusion weight is selected by grid search over {0, 0.05 ,…, 1}. For each candidate , an uncertainty threshold is computed on cal_thr fused scores and evaluated on a disjoint tuning set formed by concatenating normal windows from `cal_lam` and postinjection fault windows sampled from the fault training runs. The selection objective is fixed _a priori_ : 


![](RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process_images/RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process.pdf-0009-11.png)


where predictions are obtained by thresholding the fused score at the threshold computed for the same . Coefficients are held fixed across experiments. Algorithm 2 summarises dual-view scoring, robust normalisation, and convex fusion. 

**Algorithm 2.** Dual- view anomaly scoring and fusion. 


![](RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process_images/RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process.pdf-0009-14.png)


###### **_3.4. Conformal decisioning, FAR-controlled deployment threshold, and drift-triggered recalibration_** 

Let { _ui_ } _ni_ =1<sup>be calibration scores computed on</sup><sup>`cal_thr`using</sup> . Finite-sample corrected quantiles are computed via order statistics: 

CONNECTION SCIENCE 9 

(20) 

_k_ = min(max(`( _n_ + 1) _q_ p, 1), _n_ ), _Q_ ˆ ( _q_ ) = _u_ ( _k_ ), 


![](RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process_images/RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process.pdf-0010-03.png)


For fused score _s_ , the three-state prediction is 


![](RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process_images/RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process.pdf-0010-05.png)


corresponding to `normal` , `uncertain` , and `anomaly` . Binary views are reported via 1[ˆ _y_ (3) 1] and 1[ˆ _y_ (3) = 2]. Deployment adjusts the uncertainty threshold to satisfy an empirical FAR target on a normalonly score stream derived from `cal_thr` runs under fixed detection settings. An optional rolling maximum aggregator of width _K_ is 


![](RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process_images/RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process.pdf-0010-07.png)


This FAR-based selection defines a deployment operating point under a fixed detector configuration and does not add a conformal guarantee beyond the quantile computation on calibration scores. Calibration scores used for quantiles are computed on overlapping windows and are not independent; exchangeability is not enforced. In this work, thresholds are treated as finite-sample quantiles computed on the calibration score set under fixed preprocessing, windowing, and scoring settings, and their empirical behaviour is reported under the evaluation protocols. 

An optional drift mechanism updates the deployed uncertainty threshold along a test normal score stream using a two-sample Kolmogorov-Smirnov (KS) test on a sliding window of size `DRIFT_KS_WINDOW` . Let **s** ref denote the reference score stream from `cal_thr` normals under detection settings, and let **s** win be the most recent window of test-normal scores. A drift event triggers when 


![](RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process_images/RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process.pdf-0010-10.png)


where ( _p_ 0, _d_ 0)<sup>correspond to</sup><sup>`DRIFT_KS_P_THRESH`and</sup><sup>`DRIFT_KS_D_THRESH`. Scores are buffered for</sup> recalibration using only windows predicted as normal, implemented as _s_ [ _t_ ] < _u_ [ _t_ ] when `DRIFT_ONLY_USE_PRED_NORMAL=True` . When a drift trigger occurs and the buffer size is at least `DRIFT_MIN_BUFFER_FOR_RECAL` , a new threshold is computed on buffered scores and blended into the current threshold using an exponential moving average (EMA), while restricting downward shifts: 


![](RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process_images/RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process.pdf-0010-12.png)


###### **_3.5. Interpretability and evaluation: root-cause ranking, delay computation, and full-stream protocols_** 

Root-cause analysis (RCA) uses per-feature NLL contribution vectors from Equation (10), standardised using calibration statistics computed on `cal_thr` . Contribution statistics are 

10 M. MUDASIR ET AL. 


![](RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process_images/RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process.pdf-0011-01.png)


Let **Z** _n_ × _F_ stack clipped standardised vectors. A sparse precision matrix _F_ × _F_ is estimated by Graphical Lasso with regularisation `RCA_GLASSO_ALPHA` , yielding a sparse conditional-association proxy over contribution coordinates under nominal data. Graph edges are retained when | ij| `RCA` _ `GRAPH` _ `MIN` _ `ABS` _W. At inference, a contribution vector **c** is transformed to standardised magnitudes **b** = | **z** |. A propagated score combines direct magnitudes with a single propagation step using the absolute precision matrix: **p** = **b** + Wb, **W** = | |, = `RCA` _PROPAGATION_ `GAMMA` , (29) with diagonal entries of **W** set to zero. Rankings are reported for top- _K_ features under **b** and **p** with _K =_ `RCA` _ `TOPK` . This RCA layer is interpretive and does not affect scoring, calibration, threshold selection, or decision logic. Detection delay is evaluated on fault trajectories from the test fault dataset. Each trajectory produces a sequence of scored windows with detection stride `DETECT_STRIDE` , optional far smoothing, and optional rolling maximum aggregation. Using the deployed uncertainty threshold _u_ , define a binary alarm stream _a_ [ _t_ ] = 1[ _s_ [ _t_ ] _u_ far] aligned to window start samples { _ti_ }. Let _k_ be the required number of consecutive alarms. The first index achieving _k_ consecutive alarms is 


![](RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process_images/RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process.pdf-0011-03.png)


Delay in samples is computed relative to the injection time, while enforcing post-injection detection: 

= _t i t_ inj, _t_ inj = INJECTION_ `SAMPLE` . (31) 

The procedure returns no detection if no post-injection _k_ -consecutive segment exists. Two operating points are reported, `DELAY_K_BALANCED` and `DELAY_K_RECALL` . 

##### **4. Simulation and performance evaluation** 

Experiments were conducted in Google Colab using Python, with PyTorch for model training and PyArrow for Parquet-backed access to Tennessee Eastman Process streams. The dataset represents TEP plant-wide process streams, where fault effects may appear through reactor dynamics, separation behaviour, recycle interactions, and closed-loop control responses. Fault-free and faulty trajectories (500 simulation runs per split) were processed by standardising metadata to `faultNumber` , `simulation_Run` , and `sample` , coercing non-numeric entries to numeric values, filtering invalid or missing sensor readings, and sorting each run by sample index to preserve temporal order. After preprocessing, 52 process variables ( `xmeas` _, `xmv` _) were retained. Fault-free runs were partitioned at the run level into `train_fit` (325), `val_fit` (50), `cal_thr` (75), and `cal_lam` (50) to avoid leakage; standardisation parameters were fit using `train_fit` only. Windows with length _W_ = 100 and stride 10 were generated by reservoir sampling, producing _X_ train (12000), _X_ val (2050), _X_ cal_thr (3075), and _X_ test (11000; 3000 normal, 8000 post-injection fault). A causal dilated TCN with residual blocks and multi-head causal self-attention predicted Gaussian parameters and minimised Gaussian NLL using AdamW (lr 2 × 10 4, weight decay 10 4), gradient clipping (1.0), `ReduceLROnPlateau` , and early stopping (patience 10); the model contained 392264 parameters. Detection combined window-averaged NLL with an FFT-based frequency score normalised on `cal_thr` ; = 0.95 was tuned and conformal quantiles defined thresholds at = 0.05, yielding sampled ROC AUC and PR AUC of 1.0, with FAR control at 0.05 and delay measured after injection at sample 160 for _k_ {1, 3}. 

###### **_4.1. Training evolution and performance convergence analysis_** 

Training and validation represents the stable optimisation and convergence of the probabilistic forecaster used in RBC-AD. As shown in Figure 2, Gaussian negative log-likelihood (NLL) decreased from 1.4074 at epoch 1 to 1.1309 at epoch 50, and validation NLL decreased from 1.3217 to 1.1289; the curves remained 

CONNECTION SCIENCE 11 


![](RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process_images/RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process.pdf-0012-01.png)


**Figure 2.** Epoch-wise training and validation Gaussian NLL with proxy detection accuracy, proxy F1-score, and proxy precision computed from thresholded NLL scores as training diagnostics; these proxy metrics are not used as supervised learning objectives. 

closely aligned without late-epoch divergence. Proxy detection metrics are reported as diagnostics computed from fixed-threshold NLL scores and were not used as optimisation targets; training minimises Gaussian NLL exclusively. Training proxy accuracy increased from 0.9795 to 0.9922, whereas validation proxy accuracy remained within 0.9795–0.9863 across the reported checkpoints. Training proxy precision increased from 0.9606 to 0.9846, while validation proxy precision remained within 0.9606–0.9734. Training proxy F1-score increased from 0.9799 to 0.9922, and validation proxy F1-score remained within 0.9799–0.9865. After approximately 15–20 epochs, metric trajectories showed limited variation, and the retained checkpoint at epoch 50 corresponds to the minimum validation loss (1.1289), consistent with convergence under AdamW with gradient clipping, `ReduceLROnPlateau` , and the specified earlystopping criterion. 

###### **_4.2. Sampled-window test performance_** 

The sampled-window protocol assesses separability of the continuous combined score _s_ ( ) between faultfree operation and post-injection faulty operation. The test set comprises 11, 000 windows, including 3, 000 fault-free windows drawn from normal test runs and 8, 000 windows sampled exclusively from the postinjection segment of faulty runs with window start 160, using window length _W_ = 100 and stride 10. Labels are assigned as _y_ = 0 for fault-free windows and _y_ = 1 for post-injection fault windows, and the preinjection segment is excluded. This diagnostic does not characterise online detection on mixed trajectories and is complemented by FAR-controlled streaming and delay analyses (Section 4.3 and subsequent 

12 M. MUDASIR ET AL. 

**Table 2.** Sampled post-injection window test results under static conformal thresholds ( _u_ = 0.1977, _a_ = 0.3033). Metrics are reported for the conservative ( _s u_<sup>) and strict (</sup><sup>_s_</sup> _a_<sup>) operating points;</sup> “Unc.” denotes the fraction of windows assigned to the _Uncertain_ state, reported for all windows and stratified by true normal/fault. 

|Setting|Acc.|Prec.|_F_1|Unc. (all)|Unc. (N/F)|
|---|---|---|---|---|---|
|Conservative (_s_<br>_u_<sup>)</sup>|0.9985|0.9979|0.9989|0.001364|0.005000/0.000000|
|Strict (_s_<br>_a_<sup>)</sup>|0.9998|0.9998|0.9999|0.001364|0.005000/0.000000|




![](RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process_images/RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process.pdf-0013-03.png)


**Figure 3.** ROC and PR curves computed from continuous combined scores _s_ ( ) under the sampled post-injection window protocol (3,000 fault-free and 8,000 post-injection fault windows). ROC-AUC and PR-AUC equal 1.000 under this separability diagnostic and should not be interpreted as full-stream mixed-trajectory performance. 

sections). The fusion weight combining temporal and frequency scores was tuned without leakage using disjoint normal and post-injection fault windows, yielding = 0.95 with tuning _F_ 1 = 0.9867 and precision 0.9737. Static conformal thresholds computed on the held-out calibration-normal split at = 0.05 with finite-sample correction yielded _u_ = 0.1977 and _a_ = 0.3033. Under the conservative operating point ( _s u_<sup>), accuracy was0.9985, precision0.9979, and</sup><sup>_F_</sup> 1<sup>was0.9989; under the strict operating point</sup> ( _s a_<sup>), accuracy was0.9998, precision0.9998, and</sup><sup>_F_</sup> 1<sup>was0.9999as shown byTable 2. The three-state</sup> decision assigned 15 windows to _Uncertain_ (0.001364 of all windows), with all assignments on fault-free windows (0.0050 of true normal windows) and none on post-injection fault windows. Continuous-score separability under this post-injection-only protocol yields ROC-AUC = 1.000 and PR-AUC = 1.000, as shown by the ROC curve in Figure 3(a) and the PR curve in Figure 3(b). These values quantify separability under the diagnostic sampling procedure and do not imply equivalent performance for full-stream trajectories containing both pre-injection and post-injection segments. 

###### **_4.3. FAR-controlled operating point on test windows_** 

A deployment operating point is defined by selecting an uncertainty threshold _u_ ,deploy<sup>to satisfy an</sup> _empirical_ normal alarm-rate target of 0.05 on a held-out calibration-normal score stream constructed from the CAL_THR normal runs under the specified detection windowing configuration. This procedure is restricted to operating-point selection and does not alter model fitting, fusion-weight tuning, or conformal calibration. Using 6, 075 CAL_THR stream windows, the selected threshold is _u_ ,deploy = 0.2546, which yields an alarm rate of 0.04988 on the selection stream, while the anomaly threshold remains fixed at _a_ = 0.3033. When applied to the sampled test windows, the FAR-selected threshold produces 2 _Uncertain_ assignments (0.000182 overall), all on fault-free windows (0.000667 of true normal windows) and none on post-injection fault windows. Under _u_ ,deploy<sup>, the conservative operating point (</sup><sup>_s_</sup> _u_ ,deploy<sup>) yields accuracy</sup> 

CONNECTION SCIENCE 13 

|**Table 3.** Sampled-window<br>0.2546,<br>= 0.3033<br>_a_<br>). “Unc.”<br>reported for all windows and|test resul<br>denotes<br>stratifed|ts under FAR-controlled<br>the fraction of windows<br>bytrue normal/fault.|deployment threshold (<br>=<br>_u_,deploy<br>assigned to the_Uncertain_state,|
|---|---|---|---|
|Setting|Acc.|Prec.<br>_F_1|Unc. (all)<br>Unc. (N/F)|
|Conservative (_s_<br>_u_,deploy<sup>)</sup>|0.9996|0.9995<br>0.9998|0.000182<br>0.000667/0.000000|
|Strict (_s_<br>_a_<sup>)</sup>|0.9998|0.9998<br>0.9999|0.000182<br>0.000667/0.000000|



|**Table 4.** Fu<br>10,smoothin|ll-stream test performance under static<br> gwindow3. “Unc.” denotes the overall|thresholds (<br>_u_<br>uncertain-rate|= 0.1977<br>,<br>= 0.3033<br>_a_<br>),_W_ = 100, stride<br>under the three-state decision rule.|
|---|---|---|---|
|Protocol|Setting<br>Acc.|Prec.|Rec.<br>_F_1<br>Unc. (all)|
|Post_only|Conservative (≥<br>_u_<sup>)</sup><br>0.8643|0.9974|0.8582<br>0.9226<br>0.0100|
|Post_only|Strict (≥<br>_a_<sup>)</sup><br>0.8574|0.9994|0.8492<br>0.9182<br>0.0100|
|Mixed|Conservative (≥<br>_u_<sup>)</sup><br>0.8133|0.8971|0.8582<br>0.8772<br>0.0133|
|Mixed|Strict (≥<br>_a_<sup>)</sup><br>0.8126|0.9039|0.8492<br>0.8757<br>0.0133|



0.9996, precision 0.9995, and _F_ 1 0.9998, while the strict operating point ( _s a_<sup>) yields accuracy0.9998,</sup> precision 0.9998, and _F_ 1 0.9999 as shown by Table 3. ROC-AUC and PR-AUC are invariant to operating-point selection because they are computed from the continuous score _s_ ( ) rather than thresholded decisions. 

###### **_4.4. Full-stream test evaluation_** 

Full-stream performance is evaluated using static conformal thresholds derived from calibration-normal data, with _u_ = 0.1977, _a_ = 0.3033, window length _W_ = 100, stride 10, and score-smoothing window 3. Results are reported under two labelling protocols: **post_only** , which restricts faulty trajectories to postinjection windows and pairs them with normal trajectories, and **mixed** , which includes both pre-injection and post-injection windows from faulty trajectories as shown by Table 4. Under **post_only** (753, 500 windows), the conservative operating point ( _s u_<sup>) yields accuracy0.8643, precision0.9974, recall</sup> 0.8582, and _F_ 1 0.9226, with specificity 0.9639 (FPR 0.0361) and FNR 0.1418; the strict operating point ( _s a_<sup>) yields accuracy0.8574, precision0.9994, recall0.8492, and</sup><sup>_F_</sup> 1<sup>0.9182, with specificity0.9911 (FPR</sup> 0.00894) and FNR 0.1508. The three-state decision yields an uncertain rate of 0.0100 overall, with 0.0271 on true normal windows and 0.00895 on true fault windows. Under **mixed** (913, 500 windows), the conservative operating point yields accuracy 0.8133, precision 0.8971, recall 0.8582, and _F_ 1 0.8772, with specificity 0.6567 (FPR 0.3433) and FNR 0.1418; the strict operating point yields accuracy 0.8126, precision 0.9039, recall 0.8492, and _F_ 1 0.8757, with specificity 0.6850 (FPR 0.3150) and FNR 0.1508. The uncertain rate under the mixed protocol is 0.0133 overall, with 0.0283 on true normal windows and 0.00895 on true fault windows. The increase in false positives under **mixed** is primarily attributable to scoring pre-injection segments of faulty runs, where early transient behaviour overlaps with normal operating dynamics under thresholds fixed from calibration-normal scores. 

###### **_4.5. Detection delay and fault-wise miss-rate diagnostics_** 

Detection delay is evaluated on 2, 000 test fault trajectories using the FAR-controlled deployment threshold _u_ ,deploy = 0.2546 with detection stride 5, smoothing window 1, and score aggregation window 1. Delay is measured in samples after the injection point using the first post-injection window that satisfies a _k_ -consecutive alarm rule. The balanced configuration ( _k_ = 3) yields median delay 1 and P95 215, with 178 trajectories never detected; the recall-oriented configuration ( _k_ = 1) yields median delay 1 and P95 286, with 45 trajectories never detected as shown in Table 5. Figure 4(a) shows that both configurations concentrate a large proportion of detections at minimal delay, with a right-skewed distribution and a long tail corresponding to late detections. The _k_ = 3 configuration exhibits a comparatively shorter upper tail than _k_ = 1, consistent with the lower P95 value, while _k_ = 1 produces fewer never-detected trajectories at the expense of heavier tail behaviour. A trajectory is classified as never detected when no post-injection window satisfies the _k_ -consecutive alarm criterion. Fault-wise miss rate is defined as the fraction of trajectories for a given fault ID that are never detected. Under the balanced configuration, nonzero miss rates are concentrated on faults 3, 9, and 15, as illustrated in Figure 4(b), while other faults have near-zero miss rates under the 

14 M. MUDASIR ET AL. 

**Table 5.** Detection delay statistics on 2, 000 test fault trajectories under _u_ ,deploy = 0.2546, detection stride 5, smoothing window 1, and score aggregation window 1. 


![](RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process_images/RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process.pdf-0015-02.png)



![](RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process_images/RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process.pdf-0015-03.png)


**Figure 4.** Delay and fault-wise miss-rate diagnostics under _u_ ,deploy = 0.2546 with detection stride 5. 

evaluated setting. This behaviour is consistent with the physical characteristics of these TEP faults. Faults 3 and 9 correspond to changes in the D-feed temperature, where the resulting process deviations can be weakly expressed in the measured variables because closed-loop control compensates part of the disturbance. Fault 15 corresponds to condenser cooling water valve sticking, which can produce intermittent or slowly developing effects rather than a sharp post-injection deviation. These fault mechanisms reduce the persistence of the anomaly score and make it harder to satisfy the balanced _k_ = 3 consecutive-alarm rule. Therefore, the higher miss rates for faults 3, 9, and 15 are attributed to weak observability, controller compensation, and non-persistent score excursions rather than random model failure. 

###### **_4.6. Normal-stream alarm-rate reporting and drift-triggered threshold adaptation_** 

Normal-stream deployment behaviour is evaluated under the detection configuration (stride 5, smoothing window 1, score aggregation window 1) using _u_ ,deploy = 0.2546 selected on the CAL_THR normal stream to meet an empirical normal alarm-rate target of 0.05. On the held-out test normal stream, the achieved alarm rate is 0.03976, which is below the selection-stream alarm rate 0.04988 and below the FAR target. A KS-test drift monitor is applied to the normal score stream to trigger updates of the uncertainty threshold _u_ ( _t_ ) while holding _a_<sup>fixed; Figure 5 depicts the score stream, detected drift events, and the resulting threshold</sup> timeline used for optional adaptation under fault-free operation. Drift detection and threshold updates use only normal-stream scores under the configured KS windows and decision thresholds, without access to test labels. 

###### **_4.7. Root-cause dependency graph analysis_** 

Root-cause attribution is supported by a sparse dependency graph estimated from _per-feature Gaussian NLL contribution_ statistics computed on the CAL_THR normal split and held fixed in all subsequent experiments to avoid test leakage. Per-feature contributions are defined as the time-average of Gaussian negative loglikelihood terms for each variable within a window, producing a feature-wise NLL contribution vector. 

CONNECTION SCIENCE 15 


![](RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process_images/RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process.pdf-0016-01.png)


**Figure 5.** Normal-stream drift adaptation timeline showing the score stream, drift events, and the time-varying uncertainty threshold _u_ ( _t_ ) under KS-test triggering; _a_<sup>is held fixed.</sup> 

Edges represent conditional dependencies under nominal operation through absolute precision-matrix coefficients fitted on standardised NLL contributions using GraphicalLasso. Low-magnitude edges are removed for visualisation; the reported graph retains 591 undirected edges as shown in Figure 6, and node size scales with weighted degree to emphasise variables exhibiting high aggregate connectivity across `xmeas/xmv` groups. Root-cause reporting is performed post hoc on 500 test fault trajectories by selecting, for each trajectory, the first post-injection window assigned _Anomaly_ (or _Uncertain_ if no anomaly occurs) under the FAR-controlled deployment threshold _u_ ,deploy = 0.2546 with fixed anomaly threshold _a_ = 0.3033. Within each selected window, variables are ranked by standardised NLL contribution and interpreted using immediate graph neighbourhoods to identify co-deviating variable sets consistent with the learned nominal dependency structure. The dependency graph does not participate in scoring, threshold selection, calibration, or decision logic and serves exclusively as an interpretability layer for organising NLL-based per-feature attributions. 

##### **5. Comparison against existing approaches** 

Published studies on Tennessee Eastman Process (TEP) monitoring span latent-variable statistical monitoring, deep unsupervised anomaly detection, supervised fault diagnosis, and robustness-oriented evaluation as shown by Table 6. Recursive-CPLS (RCPLS) addresses online model updating and reports monitoring measures including fault detection rate (FDR), false alarm rate (FAR), and detection delay, without ROC-AUC or AUPRC (Hu et al., 2019). Graph-based predictable feature analysis (GPFA) reports per-fault and averaged FDR/FAR under _T_<sup>2</sup> and SPE statistics and benchmarks against PCA and dynamic variants, emphasising behaviour under dynamic regimes (Fan et al., 2023). Unsupervised deep anomaly detection benchmarks on TEP report F1 and AUPRC across reconstruction, forecasting, generative, and hybrid model families, supporting ranking under class imbalance (Hartung et al., 2023). A distributed PCA monitoring study reports fault detection rates for selected TEP faults under PCA variants and related statistics, without ROCAUC or AUPRC (Gao et al., 2022). 

Supervised LSTM-attention fault diagnosis reports training and validation accuracy together with macro and micro ROC-AUC for multiclass fault identification on enriched TEP, which is not directly comparable to 

16 M. MUDASIR ET AL. 


![](RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process_images/RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process.pdf-0017-01.png)


**Figure 6.** Dependency graph estimated from CAL_THR normal per-feature Gaussian NLL contributions; nodes denote process variables, edges encode conditional dependencies under nominal operation weighted by absolute precisionmatrix magnitudes, node size denotes weighted degree, and edges below a fixed weight threshold are pruned (591 retained undirected edges). 

**Table 6.** Comparison of existing models with the <u>proposed RBC-AD framework.</u> 

|Ref.|Method|Dataset|Metrics|Best reported values|
|---|---|---|---|---|
|Hu et al. (2019)|RCPLS (online CPLS update)|TEP|FDR, FAR, delay|FDR (RCPLS):_Tcnew_<br>2<br>= 40.54–98.55,_Txnew_<br>2<br>= 94.39–99.79;<br>FAR (RCPLS):_Tcnew_<br>2<br>= 3.53–18.29,_Txnew_<br>2<br>= 11.02–99.79;<br>delay (RCPLS):_Tcnew_<br>2<br>= 0–94,_Txnew_<br>2<br>= 0–19|
|Hartung<br>et al. (2023)|Unsupervised AD<br>benchmark|TEP|F1, AUPRC|<br><br>Best F1: BeatGAN = 0.9699; best AUPRC: TCN-S2S-<br>AE = 0.9914|
|Fan et al. (2023)|GPFA (dynamic monitoring)|TEP|FDR, FAR|Avg (selected params):_T_<sup>2 </sup>FDR = 80.20, FAR = 2.71; SPE<br>FDR = 79.16, FAR = 2.38|
|Gao et al. (2022)|NewPCA (distributed PCA)|TEP|Fault<br>detection rate|Selected faults:_ST_<sup>2 </sup>= 0.0–99.3%,_SSPE_ = 55.4–99.2%;<br>example summary:_ST_<sup>2 </sup>= 75.5%,_SSPE_= 77.5%|
|Zhao et al. (2025)|LSTM-Attention (supervised<br>diagnosis)|Enriched TEP|Acc., ROC-AUC|<br>Training/validation accuracy reported as<br>95.43% after<br>early epochs; macro ROC-AUC = 0.98, micro ROC-<br>AUC = 0.98 (17 faults)|
|Vijai and P (2025)|BiLSTM-VAE + dynamic loss|TEP|Acc., F1|Mean Acc = 0.92; Mean F1 = 0.85|
|<br>Pozdnyakov<br>et al. (2024)|<br>Adversarial benchmark<br>(attack/defence)|TEP|Acc.|Nominal examples reported: TCN = 0.90; Quantisation<br>(_n_ = 8) = 0.89; AE = 0.75|
|Adeli and<br>Mazinan (2020)|Fuzzy NN + fault-tolerant<br>control|TEP|Multi-class<br>accuracy|Overall accuracy<br>90.1% (confusion-matrix evaluation)|
|**Ours**|**RBC-AD (conformal + FAR**<br>**control)**|**TEP**|**ROC-AUC, PR-**<br>**AUC; stream F1;**<br>**delay**|**Sampled windows: ROC-AUC = 1.0000,**<br>**PR-AUC = 1.0000; full-stream F1 (post-fault only/**<br>**mixed) and delay statistics reported inTables 4**<br>**and5.**|



unsupervised anomaly scoring (Zhao et al., 2025). A VAE-based method with dynamic loss weighting reports mean accuracy and mean F1 for multiclass anomaly classification on TEP (Vijai & P, 2025). Adversarial benchmarking evaluates accuracy under attack and defence settings for TEP fault detection models, focusing on robustness rather than nominal separability (Pozdnyakov et al., 2024). A fuzzy neural- 

CONNECTION SCIENCE 17 

network fault detection and fault-tolerant control study reports multiclass classification accuracy derived from confusion-matrix evaluation and control-oriented behaviour, without ROC-AUC or AUPRC (Adeli & Mazinan, 2020). RBC-AD reports sampled-window separability metrics (ROC-AUC, PR-AUC) and full-stream operational metrics (F1, uncertainty rate, detection delay), and comparisons are limited to metric families explicitly reported without introducing unreported measures. 

##### **6. Conclusion** 

This study introduced Risk-Budgeted Conformal Anomaly Detection (RBC-AD) for industrial fault monitoring on the Tennessee Eastman Process. The approach couples a causal probabilistic forecaster with frequency-domain deviation features and uses conformal calibration to generate a three-state decision output (normal, uncertain, anomaly) at a specified miscoverage level. Model fitting, fusion-weight tuning, and calibration are separated at the run level to avoid leakage, and deployment thresholds are selected using normal-only calibration streams. 

Under the sampled-window protocol restricted to post-injection fault segments, the continuous combined score attained ROC-AUC and PR-AUC of 1.000, reflecting complete separability under that diagnostic protocol. Fullstream evaluation provides a deployment-relevant assessment: under static thresholds, the conservative operating point yielded _F_ 1 = 0.9226 on post_only trajectories and _F_ 1 = 0.8772 on mixed trajectories, with uncertainty rates near 1%. A FAR-controlled deployment threshold selected to satisfy an empirical normal alarm-rate target generalised conservatively on the held-out normal stream. Detection-delay statistics and fault-wise miss rates further quantify timeliness and failure cases associated with difficult fault modes. 

Future trends in industrial anomaly detection are expected to move toward adaptive calibration, process-aware model updating, uncertainty-aware alarm management, and operator-facing explanation systems. In this direction, future work should refine drift-triggered recalibration so that thresholds can adapt to gradual distributional changes without increasing false alarms. Further work should also improve graph-based root-cause attribution by integrating physical process knowledge and plant connectivity information with learned dependency structures. 

For practical deployment, we recommend validating RBC-AD under longer continuous streams, multiple operating modes, and plant-specific alarm constraints before online use. Faults with weak observability or intermittent behaviour should be handled with fault-specific delay analysis, adaptive consecutive-alarm rules, and process-informed feature interpretation. Future studies may also evaluate the framework on additional industrial benchmarks and real plant data to assess generalisation, computational cost, and operator usability under realistic monitoring conditions. 

##### **Author contributions** 

CRediT: **Muhammad Mudasir:** Conceptualization, Formal analysis, Investigation, Methodology, Software, Visualization, Writing – original draft; **Yousef Asiri:** Investigation, Resources, Supervision, Validation, Writing – review & editing; **Iqra Ameer:** Conceptualization, Methodology, Validation, Visualization, Writing – review & editing; **Mana Saleh Al Reshan:** Resources, Supervision, Validation, Visualization, Writing – review & editing; **Hamad Almansour:** Investigation, Software, Validation, Writing – review & editing; **Kamran Ahmad Awan:** Conceptualization, Formal analysis, Investigation, Methodology, Writing – review & editing; **Asadullah Shaikh:** Methodology, Supervision, Validation, Visualization, Writing – review & editing. 

##### **Disclosure statement** 

No potential conflict of interest was reported by the author(s). 

##### **Funding** 

This research received no external funding. 

##### **Data availability statement** 

The data supporting the findings of this study are publicly available in the Harvard Dataverse repository as _Additional Tennessee Eastman Process Simulation Data for Anomaly Detection Evaluation_ at https://doi.org/10.7910/DVN/6C3JR1doi:10.791 0/DVN/6C3JR1. This study used the Tennessee Eastman Process (TEP) fault-free training, fault-free testing, faulty training, 

18 M. MUDASIR ET AL. 

and faulty testing files, provided as `TEP_FaultFree_Training.RData` , `TEP_FaultFree_Testing.RData` , `TEP_Faulty_Training.RData` , and `TEP_Faulty_Testing.RData` . The same dataset files are also available through the Kaggle repository titled _Tennessee Eastman Process Simulation Dataset_ at https://www.kaggle.com/datasets/averkij/ tennessee-eastman-process-simulation-datasetKaggle: Tennessee Eastman Process Simulation Dataset. The datasets were last accessed on 26 January 2026. The processed experimental outputs, trained model artifacts, configuration files, figures, and evaluation reports generated during this study are available from the corresponding author upon reasonable request. 

##### **List of acronyms** 

|AUC|Area Under the Curve|
|---|---|
|AUPRC|Area Under the Precision-Recall Curve|
|CAL_LAM|Calibration Split for Fusion-Weight Tuning|
|CAL_THR|Calibration Split for Threshold Estimation|
|CPLS|Concurrent Projection to Latent Structures|
|DL|Deep Learning|
|EMA|Exponential Moving Average|
|FAR|False Alarm Rate|
|FDR|Fault Detection Rate|
|FFT|Fast Fourier Transform|
|FNR|False Negative Rate|
|FPR|False Positive Rate|
|FTC|Fault-Tolerant Control|
|GPFA|Graph-Based Predictable Feature Analysis|
|IIoT|Industrial Internet of Things|
|IoT|Internet of Things|
|KS|Kolmogorov-Smirnov|
|LSTM|Long Short-Term Memory|
|MAD|Median Absolute Deviation|
|ML|Machine Learning|
|NLL|Negative Log-Likelihood|
|NN|Neural Network|
|PCA|Principal Component Analysis|
|PR-AUC|Precision-Recall Area Under the Curve|
|RBC-AD|Risk-Budgeted Conformal Anomaly Detection|
|RCA|Root-Cause Attribution|
|RCPLS|Recursive Concurrent Projection to Latent Structures|
|ROC-AUC|Receiver Operating Characteristic Area Under the Curve|
|SPE|Squared Prediction Error|
|TCN|Temporal Convolutional Network|
|TEP|Tennessee Eastman Process|
|VAE|Variational Autoencoder|



##### **References** 

Adeli, M., & Mazinan, A. (2020). High efficiency fault-detection and fault-tolerant control approach in Tennessee Eastman Process via fuzzy-based neural network representation. _Complex & Intelligent Systems_ , _6_ , 199–212. https://doi.org/ 10.1007/s40747-019-0094-3 

Ahmed, F., Mahmood, T., Riaz, M., & Abbas, N. (2025). Comprehensive review of high-dimensional monitoring methods: Trends, insights, and interconnections. _Quality Technology & Quantitative Management_ , _22_ , 727–751. https://doi.org/ 10.1080/16843703.2024.2395745 

- Ali, H., Liu, J., & Gao, F. (2026). A hybrid causal-inference and neuro-fuzzy framework for advanced process monitoring. _Journal of Process Control_ , _162_ , 103724. https://doi.org/10.1016/j.jprocont.2026.103724 

- Ali, H., Safdar, R., Ding, W., Zhou, Y., Yao, Y., Yao, L., & Gao, F. (2025). Intelligent machine learning-based multi-model fusion monitoring: Application to industrial physio-chemical systems. _Control Engineering Practice_ , _162_ , 106361. https://doi.org/10.1016/j.conengprac.2025.106361 

- Ali, H., Safdar, R., Rasool, M. H., Anjum, H., Zhou, Y., Yao, Y., Yao, L., & Gao, F. (2024). Advance industrial monitoring of physio-chemical processes using novel integrated machine learning approach. _Journal of Industrial Information Integration_ , _42_ , 100709. https://doi.org/10.1016/j.jii.2024.100709 

- Ali, H., Safdar, R., Liu, J., Binti Abd Manan, T. S., Hu, G., Rasool, M. H., Yao, Y., & Gao, F. (2025). Hybrid fusion paradigm in advanced process monitoring: A panoramic review and future perspectives. _Industrial & Engineering Chemistry Research_ , _64_ , 22465–22514. https://doi.org/10.1021/acs.iecr.5c02759 

CONNECTION SCIENCE 19 

Ali, H., Safdar, R., Zhou, Y., Yao, Y., Yao, L., Zhang, Z., Ding, W., & Gao, F. (2025). A novel dynamic machine learning-based explainable fusion monitoring: Application to industrial and chemical processes. _Machine Learning: Science and Technology_ , _6_ , 015005. 

- Ali, H., Safdar, R., Liu, J., Asif, M. B., Zhang, X., Rasool, M. H., Yao, Y., Yao, L., Ding, J., & Gao, F. (2025). Process monitoring and dynamic fusion of complex industrial systems: A reconstruction-based Bayesian framework. _Computers & Chemical Engineering_ , _203_ , 109352. https://doi.org/10.1016/j.compchemeng.2025.109352 

- Ali, H., Andriani, D. P., Safdar, R., Abd Manan, T. S. B., Hu, G., Zhou, Y., Zhang, X., Yao, Y., Cao, Z., Liu, J., Manan, T. S. B. A., & Gao, F. (2026). A hybrid DiGLPP–Kolmogorov–Arnold network framework for robust fault detection in industrial chemical processes. _Process Safety and Environmental Protection_ , _212_ , 108854. https://doi.org/10.1016/j.psep.2026.108854 

- Andersen, E. B., Udugama, I. A., Gernaey, K. V., Khan, A. R., Bayer, C., & Kulahci, M. (2022). An easy to use gui for simulating big data using Tennessee Eastman Process. _Quality and Reliability Engineering International_ , _38_ , 264–282. https://doi.org/10.1002/qre.2975 

- Attouri, K., Mansouri, M., Hajji, M., Kouadri, A., Bouzrara, K., & Nounou, H. (2024). Real-time fault detection scheme for industrial chemical Tennessee Eastman Process, _2024 10th International Conference on Control, Decision and Information Technologies (CoDIT)_ (pp. 3015–3020). IEEE. https://doi.org/10.1109/CoDIT62066.2024.10708317 

- Bakdi, A., & Kouadri, A. (2018). An improved plant-wide fault detection scheme based on pca and adaptive threshold for reliable process monitoring: Application on the new revised model of Tennessee Eastman Process. _Journal of Chemometrics_ , _32_ , e2978. https://doi.org/10.1002/cem.2978 

- Chakraborty, N., & Finkelstein, M. (2024). Distribution-free multivariate process monitoring: A rank-energy statistic-based approach. _Quality and Reliability Engineering International_ , _40_ , 4068–4087. https://doi.org/10.1002/qre.3619 

- Chen, S., Wu, Z., & Christofides, P. D. (2020). A cyber-secure control-detector architecture for nonlinear processes. _AIChE Journal_ , _66_ , e16907. https://doi.org/10.1002/aic.16907 

- Chen, S., Wu, Z., Rincon, D., & Christofides, P. D. (2020). Machine learning-based distributed model predictive control of nonlinear processes. _AIChE Journal_ , _66_ , e17013. https://doi.org/10.1002/aic.17013 

- Chiang, L. H., Braun, B., Wang, Z., & Castillo, I. (2022). Towards artificial intelligence at scale in the chemical industry. _AIChE Journal_ , _68_ , e17644. https://doi.org/10.1002/aic.17644 

- Colosimo, B. M., Jones-Farmer, L. A., Megahed, F. M., Paynabar, K., Ranjan, C., & Woodall, W. H. (2024). Statistical process monitoring from industry 2.0 to industry 4.0: Insights into research and practice. _Technometrics_ , _66_ , 507–530. https:// doi.org/10.1080/00401706.2024.2327341 

- Downs, J. J., & Vogel, E. F. (1993). A plant-wide industrial process control problem. _Computers & Chemical Engineering_ , _17_ , 245–255. https://doi.org/10.1016/0098-1354(93)80018-I 

- Fan, W., Zhu, Q., Ren, S., Xu, B., & Si, F. (2023). Multivariate temporal process monitoring with graph-based predictable feature analysis. _The Canadian Journal of Chemical Engineering_ , _101_ , 909–924. https://doi.org/10.1002/cjce.24415 

- Farzaneh, A., & Simeone, O. (2025). Simeone, Context-aware online conformal anomaly detection with predictionpowered data acquisition, arXiv preprint arXiv:2505.01783. 

- Gao, S. w., Tian, R., & Chen, P. (2022). Principal component analysis for process monitoring in distributed system environment. _Concurrency and Computation: Practice and Experience_ , _34_ , e5309. https://doi.org/10.1002/cpe.5309 

- Hartung, F., Franks, B. J., Michels, T., Wagner, D., Liznerski, P., Reithermann, S., Fellenz, S., Jirasek, F., Rudolph, M., Neider, D., Leitte, H., Song, C., Kloepper, B., Mandt, S., Bortz, M., Burger, J., Hasse, H., & Kloft, M. (2023). Deep anomaly detection on Tennessee Eastman Process data. _Chemie Ingenieur Technik_ , _95_ , 1077–1082. https://doi.org/10.1002/ cite.202200238 

- Heo, S., & Lee, J. H. (2019). Statistical process monitoring of the Tennessee Eastman Process using parallel autoassociative neural networks and a large dataset. _Processes_ , _7_ , 411. https://doi.org/10.3390/pr7070411 

- Hu, C., Xu, Z., Kong, X., & Luo, J. (2019). Recursive-cpls-based quality-relevant and process-relevant fault monitoring with application to the Tennessee Eastman Process. _IEEE Access_ , _7_ , 128746–128757. https://doi.org/10.1109/ACCESS.2019.2939163 

- Huang, K., Zhang, L., Yang, C., Gui, W., & Hu, S. (2022). Unified stationary and nonstationary data representation for process monitoring in IIoT. _IEEE Transactions on Instrumentation and Measurement_ , _71_ , 1–12. 

- Jalilibal, Z., Karavigh, M. H. A., Amiri, A., & Khoo, M. B. (2023). Run rules schemes for statistical process monitoring: A literature review. _Quality Technology & Quantitative Management_ , _20_ , 21–52. https://doi.org/10.1080/16843703.2022.2084281 

- Li, S., Yang, S., Cao, Y., & Ji, Z. (2022). Nonlinear dynamic process monitoring using deep dynamic principal component analysis. _Systems Science & Control Engineering_ , _10_ , 55–64. https://doi.org/10.1080/21642583.2021.2024915 

- Liu, Y., Zhao, B., & Kumar, S. (2025). Edge-computing enabled anomaly detection in industrial IoT: Framework, challenges, and future directions. _International Journal of Computer Integrated Manufacturing_ , _38_ , 412–430. 

- Pozdnyakov, V., Kovalenko, A., Makarov, I., Drobyshevskiy, M., & Lukyanov, K. (2024). Adversarial attacks and defenses in fault detection and diagnosis: A comprehensive benchmark on the Tennessee Eastman Process. _IEEE Open Journal of the Industrial Electronics Society_ , _5_ , 428–440. https://doi.org/10.1109/OJIES.2024.3401396 

- Reinartz, C., Kulahci, M., & Ravn, O. (2021). An extended Tennessee eastman simulation dataset for fault-detection and decision support systems. _Computers & chemical engineering_ , _149_ , 107281. https://doi.org/10.1016/j.compchemeng.2021.107281 

- Ren, J., Tang, L., & Zou, H. (2023). A comparative study of different data representations under CNN and a novel integrated FDD architecture. _The Canadian Journal of Chemical Engineering_ , _101_ , 4571–4586. https://doi.org/10.1002/ cjce.24810 

20 M. MUDASIR ET AL. 

Ricker, N. L. (1996). Decentralized control of the Tennessee Eastman challenge process. _Journal of Process Control_ , _6_ , 205–221. https://doi.org/10.1016/0959-1524(96)00031-5 

- Tajmouati, S., Wahbi, B. E., & Dakkon, M. (2024). Applying regression conformal prediction with nearest neighbors to time series data. _Communications in Statistics-Simulation and Computation_ , _53_ , 1768–1778. https://doi.org/10.1080/ 03610918.2022.2057538 

- Tian, Z., & Hoo, K. A. (2005). Multiple model-based control of the Tennessee- eastman process. _Industrial & Engineering Chemistry Research_ , _44_ , 3187–3202. https://doi.org/10.1021/ie0496939 

- Vermesan, O., Coppola, M., Bahr, R., Bellmann, R. O., Martinsen, J. E., Kristoffersen, A., Hjertaker, T., Breiland, J., Andersen, K., Sand, H. E., & Lindberg, D. (2022). An intelligent real-time edge processing maintenance system for industrial manufacturing, control, and diagnostic. _Frontiers in Chemical Engineering_ , _4_ , 900096. https://doi.org/10.3389/fceng.2022.900096 

- Vijai, P., & P, B. S. (2025). Anomaly detection solutions: The dynamic loss approach in VAE for manufacturing and iot environment. _Results in Engineering_ , _25_ , 104277. https://doi.org/10.1016/j.rineng.2025.104277 

- Wu, Z., Rincon, D., Luo, J., & Christofides, P. D. (2021). Machine learning modeling and predictive control of nonlinear processes using noisy data. _AIChE Journal_ , _67_ , e17164. https://doi.org/10.1002/aic.17164 

- Xu, H., Ren, T., Mo, Z., & Yang, X. (2022). A fault diagnosis model for Tennessee Eastman Processes based on feature selection and probabilistic neural network. _Applied Sciences_ , _12_ , 8868. https://doi.org/10.3390/app12178868 

- Yang, Y., & Kuchibhotla, A. K. (2025). Selection and aggregation of conformal prediction sets. _Journal of the American Statistical Association_ , _120_ , 435–447. https://doi.org/10.1080/01621459.2024.2344700 

- Yang, F., Wang, J., Asaadi, M., Hu, W., Wang, Z., & Zhang, Y. (2022). Alarm management techniques to improve process safety, _Methods in chemical process safety_ (Vol. 6, pp. 227–280). Elsevier. https://doi.org/10.1016/bs.mcps.2022.04.009 

- Yerimah, L. E., Ghosh, S., Wang, Y., Cao, Y., Flores-Cerrillo, J., & Bequette, B. W. (2022). Process prediction and detection of faults using probabilistic bidirectional recurrent neural networks on real plant data. _Journal of Advanced Manufacturing and Processing_ , _4_ , e10124. https://doi.org/10.1002/amp2.10124 

- Zeng, L., Jin, Q., Lin, Z., Zheng, C., Wu, Y., Wu, X., & Gao, X. (2024). Dual-attention LSTM autoencoder for fault detection in industrial complex dynamic processes. _Process Safety and Environmental Protection_ , _185_ , 1145–1159. https://doi.org/ 10.1016/j.psep.2024.02.042 

- Q, Lv, Yu, X, & H, Ma, et al. (2025). Anomaly detection for compressor systems under variable operating conditions. _Process safety and Environmental Protection_ , _194_ , 761–772. 10.1016/j.psep.2024.12.068 

- Zhao, S., Duan, Y., Roy, N., & Zhang, B. (2025). A novel fault diagnosis framework empowered by lstm and attention: A case study on the Tennessee Eastman Process. _The Canadian Journal of Chemical Engineering_ , _103_ , 1763–1785. https:// doi.org/10.1002/cjce.25460 

- Zhou, S., Zhou, X., & Liu, H. (2024). Process monitoring and fault diagnosis method combining bagging dpca-ica with moving window Kolmogorov–Smirnov test. _The Canadian Journal of Chemical Engineering_ , _102_ , 2495–2510. https:// doi.org/10.1002/cjce.25211 

