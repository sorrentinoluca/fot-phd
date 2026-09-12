www.nature.com/scientificreports 


![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0001-01.png)


# **OPEN Early-warning industrial fault detection based on physics-guided residual learning and calibrated CRNNs** 

**Abuzar Khan**<sup>**1**</sup> **, Fahmid Al Farid**<sup>**2**</sup> **, Ahmad Junaid**<sup>**1**</sup> **, Muhammad Farooq Siddique**<sup>**3,4**</sup> **, Abid Iqbal**<sup>**5**</sup> **, Muhammad Shahzad Siddique**<sup>**6**</sup> **, Jia Uddin**<sup>**7**</sup> **, Hezerul Abdul Karim**<sup>**2**</sup> **& Ghassan Husnain**<sup>**1**</sup> 

**Industrial plants generate high volume multivariate sensor time series where early fault detection must be accurate, governable and explainable under regime changes, sensor correlations and drift. Many published Tennessee Eastman Process (TEP) studies report strong receiver operating characteristic (ROC) or accuracy but provide limited evidence for calibrated probabilities, uncertainty bounds and actionable sensor level diagnostics, so alarm thresholds remain ad hoc and difficult to defend in control rooms. To address this issue, we propose a physics guided pipeline that combines twin based residuals with compact rolling and spectral descriptors and an attention based convolutional recurrent neural network (CRNN). The proposed method is also compared against state-of-the-art (SOTA) baselines to establish its relative effectiveness under the same evaluation setting. Residuals highlight deviations from physics consistent behavior, while a one-dimensional convolutional neural network (Conv1D) and bidirectional gated recurrent unit (BiGRU) encoder with attention models short and long temporal structure over 120 step windows. SHapley Additive exPlanations (SHAP) guided feature selection reduces redundancy and improves interpretability, Optuna stabilizes training and Platt scaling calibrates anomaly probabilities for policy driven thresholding under a false alarm budget. Reliability is quantified with 1000 block bootstrap bias-corrected and accelerated (BCa) confidence intervals. On a run level 70/20/10 split of Tennessee Eastman Process runs, the method achieves about 99.0% accuracy with area under the receiver operating characteristic curve (AUC-ROC) and area under the precision-recall curve (AUC-PR) near 1.00, macro F1-score of 0.93 ± 0.02 and expected calibration error (ECE) reduced to** **_≈_ 0.03 after calibration. Early warning governance improves the Numenta Anomaly Benchmark (NAB) score by 17% over an Isolation Forest baseline and supports low nuisance alarm operation. These results show that residual-guided learning plus calibrated decision governance can support deployment-oriented industrial monitoring by enabling auditable thresholds and operatorfacing explanations within the Tennessee Eastman benchmark setting.** 

**Keywords** Industrial fault diagnosis, Physics-guided residuals, Convolutional recurrent neural network (CRNN), Probability calibration 

Modern manufacturing environments utilize vision systems, vibration sensors, power monitors and Internet . of Things (IoT)-enabled devices to generate extensive, rapidly evolving multivariate time-series data streams<sup>1</sup> Early detection of anomalies within these streams is essential to prevent product defects, unplanned downtime 

1Department of Computer Science, CECOS University of IT and Emerging Sciences, Peshawar, Pakistan. 2Centre for Image and Vision Computing (CIVC), Centre of Excellence for Artificial Intelligence, Faculty of Artificial Intelligence and Engineering (FAIE), Multimedia University, Cyberjaya, Selangor, Malaysia.<sup>3</sup> Department of Mechanical and Robotics Engineering, Gwangju Institute of Science and Technology, Gwangju 61005, Republic of Korea.<sup>4</sup> KAIST InnoCORE PRISM-AI Center, Korea Advanced Institute of Science and Technology (KAIST), Daejeon 34141, Republic of Korea.<sup>5</sup> Department of Computer Engineering, College of Computer Sciences and Information Technology, King Faisal University, Al-Ahsa 31982, Saudi Arabia.<sup>6</sup> Former Mechanical Engineering Student, University of Engineering and Technology, Peshawar, KPK, Pakistan.<sup>7</sup> AI and Big Data Department, Woosong University, Daejeon, Republic of Korea.<sup></sup> email: ghassan.husnain@gmail.com; hezerul@mmu.edu.my 

**Scientific Reports** |        (2026) 16:17488 | https://doi.org/10.1038/s41598-026-48227-6 Content courtesy of Springer Nature, terms of use apply. Rights reserved 

1 

www.nature.com/scientificreports/ 

and safety-critical incidents, which are central concerns in achieving zero-defect Industry 4.0 operations<sup>2</sup> . The economic implications are significant<sup>3</sup> . Siemens estimates that the 500 largest global companies lose nearly United States dollars (USD) 1.4 trillion annually due to unplanned downtime, representing approximately 11% of their revenues and directly impacting competitiveness and risk exposure<sup>4</sup> . At the operational level, reliability surveys indicate that unplanned outages are both frequent and costly, with typical losses approaching USD 125,000 per hour and most industrial businesses experiencing outages at least once per month<sup>5</sup> . This urgency is further underscored by the rapid expansion of the predictive maintenance market, which is projected to increase from USD 10.6 billion in 2024 to USD 47.8 billion by 2029, demonstrating strong demand for reliable and actionable monitoring systems<sup>6</sup> . 

### **Industrial anomaly detection under deployment constraints** 

Although significant progress has been made in statistical process control, machine learning and deep learning, a substantial gap persists between research prototypes and systems suitable for deployment and defense in production environments<sup>7</sup> . Industrial plants frequently experience changes in operating modes, sensor drift, correlated measurements and evolving process dynamics, while labeled fault data remain scarce and costly to obtain<sup>8</sup> . Fixed rules and static thresholds often prove inadequate under these conditions, whereas purely datadriven deep learning models may lack transparency, stable alarm rates and audit-ready evidence required by operators<sup>9</sup> . Additional deployment constraints further restrict the design space: alerts must be generated with low latency, memory usage must accommodate edge hardware limitations and outputs must be interpretable and actionable to enable engineering teams to localize issues to specific sensors, time intervals and plausible physical causes<sup>10</sup> . 

Model-based simulation offers a complementary source of evidence by generating expected behavior under nominal conditions<sup>11</sup> . Comparing real-time measurements to these predictions produces residual signals that highlight deviations from expected dynamics and can reveal subtle faults earlier than raw signals alone<sup>12</sup> . Despite these advantages, many residual-based methods continue to rely on ad hoc thresholding and do not systematically integrate residuals with compact descriptors, advanced temporal learning models, calibrated probability outputs or reproducible evaluation frameworks that link technical metrics to operational decisions<sup>13</sup> . These limitations underscore the need for hybrid pipelines that are both statistically rigorous and operationally practical<sup>14</sup> . In such pipelines, residual-informed inputs enhance sensitivity, calibrated probabilities enable defensible threshold . selection and interpretable explanations facilitate investigation workflows<sup>15</sup> 

Figure 1 summarizes a typical industrial workflow, from multichannel data acquisition to automated defect decisions and downstream quality-control actions. 

### **Residual-guided learning with calibrated decisions** 

A unified anomaly detection pipeline is introduced and evaluated using the Tennessee Eastman Process dataset, a widely recognized benchmark for process-industry fault diagnosis<sup>17</sup> . The pipeline employs a physics-based model to generate physics-informed expectations and computes residuals as the difference between observed measurements and model predictions<sup>18</sup> . These residuals provide an interpretable feature signal that enhances sensitivity to subtle faults and eliminates the need to develop a new simulator for each study<sup>19</sup> . The residuals are integrated with compact engineered descriptors and processed by a lightweight convolutional recurrent architecture with attention, which is designed to capture both short-term temporal structure and longer-range dependencies while remaining suitable for edge deployment<sup>20</sup> . 

Decision quality is established as a fundamental requirement rather than an afterthought<sup>21</sup> . Predicted probabilities are calibrated and operating points are determined through threshold-sensitivity analyses that report achievable true positive rates, false positive rates and alarm rates per hour, thereby linking technical performance to control-room decision-making<sup>22</sup> . Reliability is assessed using expected calibration error and bootstrap confidence intervals, ensuring that uncertainty and threshold decisions can be justified to operators and auditors rather than adjusted through trial and error<sup>23</sup> . To facilitate investigation workflows, the pipeline 


![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0002-09.png)


**Fig. 1** . End-to-end industrial anomaly detection and quality inspection workflow. This figure is an enhanced version adapted from<sup>16</sup> , illustrating data collection from production lines, automated defect and non-defect decision making, and downstream quality inspection and control actions. 

**Scientific Reports** |        (2026) 16:17488 | https://doi.org/10.1038/s41598-026-48227-6 Content courtesy of Springer Nature, terms of use apply. Rights reserved 

2 

www.nature.com/scientificreports/ 

provides per-fault performance metrics and stable feature attributions, enabling alarms to be associated with . specific sensors and time spans for root-cause analysis and auditable maintenance actions<sup>24</sup> 

### **Scope and paper organization** 

Focusing on the Tennessee Eastman Process improves comparability with prior work and enables controlled analysis of regime changes and fault families. At the same time, simulation-based evidence has limits, so the results are framed as a strong internal-validity step toward field deployment rather than a definitive proof of operational performance. The remainder of this study is organised as follows: “Literature review” reviews related work, “Methodology” details the proposed methodology and “Results” reports experimental results. “Discussion and comparison” discusses findings and comparisons, while “Conclusion and future work” concludes with limitations and future directions. Tables 16 and 17 summarize the variables, symbols, acronyms and abbreviations used in this manuscript. 

## **Literature review** 

This section reviews anomaly detection for smart manufacturing with emphasis on the core deployment problem highlighted in the Introduction, namely regime changes, drift, limited labels, low-latency requirements and the need for calibrated and explainable alarms. 

### **Classical monitoring before deep learning: statistical tests and residual-based diagnostics** 

Early industrial monitoring relied on statistical process control and multivariate statistical process monitoring, where control limits were defined for summary statistics under approximate stationarity<sup>25</sup> . In the Tennessee Eastman Process, this line of work includes principal component analysis (PCA), dynamic PCA, partial least squares (PLS)-style monitoring and knowledge-guided classifiers that translate multivariate deviations into alarm decisions<sup>26</sup> . These methods remain attractive because they are lightweight and often easier to communicate to operators<sup>27</sup> . However, their assumptions are routinely violated in real plants, where operating modes shift, sensors drift, interactions are nonlinear and fault signatures evolve over time<sup>28</sup> . As a result, fixed thresholds can become unstable, producing either missed detections under new regimes or elevated false alarms under benign distribution shifts<sup>26</sup> . Residual-based monitoring partially addresses this issue by comparing measured behavior to expected behavior and alarming on deviations, but classical residual tests still depend heavily on hand-tuned limits and may degrade when residual distributions change across operating conditions<sup>29</sup> . 

### **Residual-guided deep learning for regime changes and edge feasibility** 

Recent research has increasingly focused on temporal deep learning to more effectively capture the nonlinearity and long-range dependencies present in multivariate industrial data streams<sup>30</sup> . Convolutional temporal models are capable of identifying local patterns, such as transient spikes and short-lived oscillations, whereas recurrent layers enhance sensitivity to delayed effects and gradual drifts<sup>31,32</sup> . Attention mechanisms further address regime variability by directing computational resources toward informative time segments instead of uniformly processing all timestamps<sup>33</sup> . Concurrently, unsupervised and weakly supervised deep anomaly detection methods have been extensively investigated using Tennessee Eastman style datasets to mitigate reliance on costly fault labels<sup>34</sup> . A comprehensive benchmark on Tennessee Eastman Process data demonstrates that several representative deep anomaly detectors achieve best F1-scores of 0.9172, 0.9114, 0.9097, 0.9078 and 0.9074 for temporal forecasting and hybrid graph or recurrent approaches, indicating that strong performance is attainable but not consistent across different methodological families<sup>14</sup> . These results are practically significant because they represent realistic trade-offs among model classes and training procedures, rather than the performance of a single, hand-optimized architecture<sup>35</sup> . 

While pure deep learners can be accurate, two gaps remain relative to the deployment problem emphasized in the Introduction<sup>36,37</sup> . First, many approaches treat the input space as purely data-driven and do not explicitly encode physics-informed expectations that can make subtle deviations more visible and more interpretable<sup>38</sup> . Second, many studies prioritize discrimination metrics while providing limited support for decision governance, such as calibrated probabilities, threshold justification and operator-facing reporting<sup>39</sup> . Residual-guided learning addresses the first gap by using a physics-based predictor to define expected behavior and then learning on residual-enriched representations, which improves sensitivity to small drifts that may be masked in raw signals<sup>40</sup> . Compact hybrid architectures address the second gap by balancing expressiveness with edge feasibility, using convolutional blocks for short-range structure, gated recurrent units (GRUs) for longer dependencies and attention to emphasize informative windows without excessive compute<sup>41</sup> . Feature selection further improves deployability and interpretability by reducing redundancy and highlighting sensor-level relevance, which supports maintenance workflows that must map alarms to likely causes and affected subsystems. 

As shown in Fig. 3, the red box highlights the reactor-condenser recycle loop, a tightly coupled subsystem where nonlinear interactions, short transients and delayed responses can produce weak but safety-critical deviations. Our framework targets this region by forming physics-informed residual signals that amplify departures from expected behavior, then modeling the residual-enriched multivariate streams with a compact convolutional-recurrent backbone and attention to capture both short-lived oscillations and long-range drift. In addition, calibrated probability outputs and threshold governance provide stable, operator-defensible alarms, while feature selection supports sensor-level interpretability for maintenance handoff. 

### **Trustworthy alarms: calibration, uncertainty and explanation for operational handoff** 

Beyond detection accuracy, industrial anomaly systems must deliver probability outputs that are reliable enough to support defendable thresholding and stable alarm policies<sup>43</sup> . Calibration has therefore become an enabling layer for governance, since miscalibrated confidence can lead to overconfident alarms and unstable decision 

**Scientific Reports** |        (2026) 16:17488 | https://doi.org/10.1038/s41598-026-48227-6 Content courtesy of Springer Nature, terms of use apply. Rights reserved 

3 

www.nature.com/scientificreports/ 

boundaries under shift<sup>38</sup> . Post hoc calibration methods, including Platt-style scaling and related temperature variants, are widely used to align predicted confidence with empirical correctness and calibration quality is commonly summarized via reliability curves and expected calibration error (ECE)<sup>44</sup> . For time series in particular, uncertainty reporting should respect temporal dependence, so interval estimation via block-aware . bootstrap resampling is often preferred over single split reporting when the goal is to justify operating points<sup>45</sup> Interpretability is similarly essential for adoption in control-room settings, where engineers require evidence that an alarm is linked to specific sensors and time spans<sup>46,47</sup> . Attribution methods such as SHapley Additive exPlanations (SHAP)-style feature relevance and gradient-based temporal attributions can support this need, but their use in industrial monitoring is most credible when stability across random seeds and training variability is reported<sup>48</sup> . Finally, deployment-oriented evaluation increasingly includes hardware telemetry such as latency, throughput, parameter count and memory footprint, because edge feasibility is not implied by accuracy alone<sup>49</sup> . Together, calibration, uncertainty reporting and stable explanations form the practical interface between a detection model and the investigation workflows required for safe industrial operation<sup>40</sup> . Residual generation based on the mismatch between measured plant outputs and model-based nominal predictions is a classical principle in fault detection and isolation (FDI) rather than a new methodological contribution of this work. In the analytical-redundancy and model-based FDI literature, residuals have long been used as the primary signal for detecting departures from expected system behavior<sup>50–54</sup> . Accordingly, the novelty of the present study does not lie in introducing residual-based detection itself, but in integrating a classical residual-generation stage with calibrated convolutional recurrent neural network (CRNN)-based temporal modeling, SHAP-guided feature selection and governance-oriented threshold design for early warning in industrial monitoring. 

## **Methodology** 

This section presents the proposed physics-guided convolutional recurrent neural network (CRNN) pipeline for industrial anomaly detection. The design addresses the deployment constraints introduced in “Introduction”, including regime changes, drift, limited labels, low latency and operator-facing interpretability. The complete workflow shown in Fig. 2 is implemented as a modular sequence comprising residual generation, feature construction, feature selection, temporal learning, probability calibration and validation. 

### **Pipeline overview** 

The pipeline starts from multivariate sensor streams of the Tennessee Eastman Process and a physics-based reference model that provides nominal fault-free expectations. Residuals are computed from the mismatch between measured and expected behavior, then combined with compact time- and frequency-domain descriptors. A Light Gradient Boosting Machine (LightGBM) stage is used for SHAP-guided feature selection to reduce redundancy and improve interpretability. The selected features are subsequently processed by the proposed physics-guided CRNN with attention, which outputs calibrated anomaly probabilities for thresholdbased decision support. Figure 5 summarizes the data path up to model entry and Fig. 6 summarizes the discrimination and calibration evaluation pipeline. 

### **Dataset and split** 

We evaluate the proposed framework on the Tennessee Eastman Process dataset, which is a widely used benchmark for process-industry fault diagnosis<sup>55,56</sup> . It contains 41 measured variables and 12 manipulated variables across 22 operating conditions, including one normal mode and 21 fault modes. Table 1 summarizes the dataset characteristics used throughout this study. A run-level 70/20/10 split is used for training, validation and testing to avoid temporal leakage across runs. All normalization statistics and feature-selection models are fitted on the training split only and then applied unchanged to validation and test partitions. The learning 


![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0004-08.png)


**Fig. 2** . End-to-end methodology flowchart showing physics-model residual generation, residual-enriched input construction, attention-based convolutional recurrent training, probability calibration and validation with per-fault reporting and attribution stability checks. 

**Scientific Reports** |        (2026) 16:17488 | https://doi.org/10.1038/s41598-026-48227-6 Content courtesy of Springer Nature, terms of use apply. Rights reserved 

4 

www.nature.com/scientificreports/ 


![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0005-01.png)


**Fig. 3** . Tennessee Eastman Process schematic with the highlighted region of interest. The red box marks the reactor-condenser recycle loop and its associated feed and utility interactions, where coupled dynamics, operating-mode changes and sensor correlations often cause subtle drifts and delayed fault effects that are difficult to govern with fixed thresholds. The schematic is adapted and enhanced from the original Tennessee Eastman Process diagram reported in<sup>42</sup> . 

|**Property**|**Type**|**Description or value**|**Notes**|
|---|---|---|---|
|Total samples|Count|281,170|Combined across 500 runs|
|Number of simulation runs|Count|500|Distinct operating conditions|
|Time series length per run|Range|500–1000 steps|Varies with run and fault duration|
|Process variables xmeas|Sensor inputs|41|Continuous measurements|
|Manipulated variables xmv|Control inputs|12|Actuator signals|
|Number of fault types|Integer|21 plus normal|IDV 0 normal, IDV 1-21 faults|
|Fault label variable|Categorical|`faultNumber`in 0..21|Encodes specifc fault type|
|Class label variable|Binary|`Class`in {FaultFree, Faulty}|Derived from faultNumber|
|Class distribution|Ratio|_∼_50% FaultFree/50% Faulty|Overall balance; per-fault imbalance exists|
|Missing values|Boolean|None observed|No missing entries in provided data|
|Per-fault imbalance|Qualitative|Present|Frequencies vary across faults|



**Table 1** . Summary of key characteristics of the Tennessee Eastman Process dataset used in this study. 

problem is formulated as binary fault detection rather than explicit fault-type diagnosis. Accordingly, the model outputs a calibrated probability of abnormal operation, whereas fault identities are used only for stratified analysis and error breakdowns. Since the Tennessee Eastman Process is a simulated benchmark rather than a real plant dataset, abnormal conditions are introduced through benchmark-defined IDV disturbances rather than a single generic corruption mechanism such as additive Gaussian noise or a fixed percentage bias. 

**Scientific Reports** |        (2026) 16:17488 | https://doi.org/10.1038/s41598-026-48227-6 Content courtesy of Springer Nature, terms of use apply. Rights reserved 

5 

www.nature.com/scientificreports/ 

### **Data preprocessing and quality control** 

Before residual generation and feature extraction, the multivariate Tennessee Eastman Process sequences are passed through a lightweight preprocessing and quality-control pipeline designed to preserve fault signatures while maintaining numerical stability. Table 2 summarizes the adopted steps. Because the benchmark is simulator-generated, the released sequences were structurally complete after loading and alignment, so missingdata imputation was not required in the final experiments. Nevertheless, the imputation rule is defined explicitly for completeness and reproducibility. Similarly, no aggressive outlier-removal stage was applied because large excursions may correspond to true fault behavior rather than spurious corruption. Instead, training-set-based normalization was used to stabilize optimization without suppressing abnormal dynamics. 

and channel For completeness, the fallback imputation policy is defined in Eq. ( _d_ is missing, it is replaced with the training-set channel median 1). If a channel value _x_ ˜ _d_ : _xt,d_ at time step _t_ 


![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0006-04.png)


where _x_ ˜ _d_ is computed from the training partition only. In the reported experiments, this safeguard was defined but not triggered because the benchmark sequences were complete after preprocessing checks. The split-safe 2 normalization step is defined in Eq. ( ). After the integrity audit, each channel is standardized using training-set mean _µd_ and standard deviation _σd_ : 

_x_<sup>norm</sup> _t,d_ =<sup>_xt_</sup> _σ_<sup>_<u>,d</u>_</sup> _d_<sup>_−_</sup> + _ϵ_<sup>_<u>µd</u>,_</sup> (2) 

where _ϵ_ is a small constant for numerical stability. The statistics ( _µd, σd_ ) are fitted on the training split only and then reused unchanged for validation and test data. This keeps optimization stable, reduces scale imbalance across process variables and preserves the interpretability of subsequent residual and descriptor analysis. 

### **Physics-based residual generation** 

To improve fault sensitivity while retaining physical interpretability, the proposed pipeline transforms raw multivariate measurements into residual signals relative to a nominal process reference. In this study, the term _physics-based twin_ refers to the nominal Tennessee Eastman Process simulator used as a fault-free reference model. It is not a newly developed plant-specific digital twin, but a benchmark-consistent source of expected normal behavior. The methodological novelty therefore lies not in residual generation itself, which is classical in model-based fault detection, but in integrating that residual stage into a calibrated CRNN pipeline for temporal detection, explanation and threshold governance. 

process vector at time step The residual definition used throughout the pipeline is given in Eq. ( _t_ and let _y_ ˆ _t ∈_ R<sup>_D_</sup> denote the corresponding nominal prediction produced by the 3). Let _yt ∈_ R<sup>_D_</sup> denote the measured Tennessee Eastman Process reference simulator. The residual vector is computed as 

#### _rt_ = _yt − y_ ˆ _t,_ (3) 

where _rt ∈_ R<sup>_D_</sup> quantifies the deviation of the observed process from expected nominal behavior. This representation preserves direct correspondence between each residual component and its original sensor channel, which supports operator-facing traceability. 

Compared with raw-signal learning alone, residual-based learning emphasizes behavior that is inconsistent with normal process dynamics and makes abnormal operation easier to isolate. This residual-centric representation suppresses nominal background variation and highlights departures more likely to be associated with faults, drift or disturbances. It is particularly useful for early warning because small but systematic deviations may become detectable before they are visually obvious in the original measurements. 

> _yt_ and the nominal simulator output Figure 4 illustrates this residual-generation stage. The measured Tennessee Eastman Process sensor sequence _y_ ˆ _t_ are aligned, their difference is computed to obtain _rt_ and the resulting residuals are forwarded to the feature-engineering and CRNN stages. To avoid information leakage, residuals are 

|**Stage**|**Operation**|**Purpose / policy**|
|---|---|---|
|Integrity check|Verify channel count, sequence length, label alignment and time<br>ordering|Ensures that each run is structurally valid before model processing|
|Missing-data audit|Check all channels for NaN, Inf or undefned entries|Benchmark sequences were complete afer loading; fallback imputation<br>rule is defned for reproducibility|
|Outlier policy|No hard sample removal or winsorization|Preserves abrupt deviations that may correspond to true fault onset rather<br>than noise|
|Normalization|Training-set-based standardization per channel|Improves numerical stability and prevents scale dominance across variables|
|Split-safe ftting|Estimate preprocessing statistics on training data only|Prevents leakage into validation and test splits|
|Sequence preparation|Apply the same ftted preprocessing to validation and test runs|Keeps evaluation consistent with the deployment scenario|



**Table 2** . Preprocessing and quality-control summary applied before residual generation and feature construction. 

**Scientific Reports** |        (2026) 16:17488 | https://doi.org/10.1038/s41598-026-48227-6 Content courtesy of Springer Nature, terms of use apply. Rights reserved 

6 

www.nature.com/scientificreports/ 

standardized using training-set statistics only and the same normalization parameters are reused for validation and test data. 

### **Feature construction and SHAP-guided selection** 

Residuals are augmented with compact descriptors that summarize short-term variability and oscillatory behavior. The root-mean-square descriptor used for short-term signal magnitude is defined in Eq. (4). Let _xu_ denote the scalar value of a single process channel at time index _u_ within a local window of length _w_ . Then 


![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0007-04.png)


which summarizes recent signal energy over the most recent _w_ samples. The spectral band-energy descriptor is defined in Eq. (5). Let _x_ 0: _T −_ 1 denote a length- _T_ discrete sequence from one channel and let _X_ [ _k_ ] denote its discrete Fourier transform coefficient at frequency index _k_ . The band energy is computed as 


![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0007-06.png)


where _K_ band denotes the set of frequency bins assigned to the selected band. To assess redundancy among candidate features, the Pearson correlation coefficient in Eq. (6) is used. Let _Xi_ and _Yi_ denote the _i_ th samples of two candidate feature vectors _X_ and _Y_ , let _X_<sup>¯</sup> and _Y_<sup>¯</sup> denote their sample means and let _N_ be the number of samples: 


![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0007-08.png)



![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0007-09.png)


**Fig. 4** are compared with nominal TEP simulator predictions . Physics-based residual generation and anomaly detection pipeline. Measured process observations _y_ ˆ _t_ to compute residuals _rt_ = _yt − y_ ˆ _t_ using Eq. (3). The _yt_ residual sequence is then combined with compact engineered descriptors and provided to the proposed CRNN for anomaly probability estimation. 

**Scientific Reports** |        (2026) 16:17488 | https://doi.org/10.1038/s41598-026-48227-6 Content courtesy of Springer Nature, terms of use apply. Rights reserved 

7 

www.nature.com/scientificreports/ 

The resulting descriptors are concatenated with residual features to form the per-step representation. To reduce redundancy and improve operator-facing interpretability, a LightGBM model is trained on the training set and SHAP attributions are computed. The top- _M_ features ranked by mean absolute attribution are selected and the same selection is applied unchanged to validation and test sets. This selected representation is also reused for explanation reporting to associate alarms with influential sensors, descriptors and time spans. 

### **Proposed physics-guided CRNN architecture** 

This subsection formalizes the proposed physics-guided CRNN as an end-to-end mapping from multivariate process measurements to calibrated anomaly probabilities. The formulation follows the pipeline in Fig. 2 and makes each stage explicit so that residual integration, feature fusion, selection, temporal modeling, attention pooling and calibration can be audited and reimplemented consistently. 

#### _End-to-end formulation_ 

The reference-model prediction used by the pipeline is defined in Eq. (7). Let _yt ∈_ R<sup>_D_</sup> denote the measured process vector at time produces a nominal prediction _t_ and let _y_ ˆ _ut t∈_ denote the corresponding control inputs. A physics-based reference model R<sup>_D_</sup> parameterized by _θ_ : 


![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0008-06.png)


where _T_ is the sequence length and _D_ is the number of measured channels. The residual construction stage is then written explicitly in Eq. (8) as 

_rt_ = _yt − y_ ˆ _t ∈_ R<sup>_D_</sup> _._ (8) 

The descriptor operator used to summarize recent temporal behavior is defined in Eq. (9). Let _w_ denote the feature window length and let _ϕ_ ( _·_ ) produce _K_ compact descriptors, such as the rolling and spectral summaries defined earlier: 

_et_ = _ϕ_ ( _yt−w_ +1: _t_ ) _∈_ R<sup>_K_</sup> _._ (9) 

The residual-descriptor fusion step is given in Eq. (10). Residuals and descriptors are concatenated to form a residual-enriched feature vector: 

_zt_ = [ _rt et_ ] _∈_ R<sup>_D_+</sup><sup>_K_</sup> _,_ (10) 

The temporal input window consumed by the CRNN is defined in Eq. (11). For a sequence length _L_ , 

_Zt_ = [ _zt−L_ +1 _, . . . , zt_ ] _∈_ R<sup>_L×_(</sup><sup>_D_+</sup><sup>_K_)</sup> _,_ (11) 

Feature selection is formalized in Eq. (12). Let _I ⊂{_ 1 _, . . . , D_ + _K}_ denote the index set of the selected top- _M_ features according to mean absolute SHAP attribution. Then 


![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0008-16.png)


The convolutional temporal encoder is defined in Eq. (13). Using learnable parameters ( _Wc, bc_ ) and a nonlinearity _σ_ ( _·_ ), the short-range temporal features are 


![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0008-18.png)


Longer temporal dependencies are modeled by the bidirectional gated recurrent unit layer defined in Eq. (14): 


![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0008-20.png)


where _θr_ denotes recurrent parameters and _ht ∈_ R<sup>_m_</sup> is the hidden representation at time step _t_ . The temporal attention weights are computed as shown in Eq. (15). Using parameters ( _Wa, ba, v_ ), 


![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0008-22.png)


The corresponding attention-pooled context vector is defined in Eq. (16) as 


![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0008-24.png)


The raw anomaly probability produced by the output layer is given in Eq. (17): 


![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0008-26.png)


**Scientific Reports** |        (2026) 16:17488 | https://doi.org/10.1038/s41598-026-48227-6 Content courtesy of Springer Nature, terms of use apply. Rights reserved 

8 

www.nature.com/scientificreports/ 


![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0009-01.png)


**Table 3** . Side by side equation comparison of a basic CRNN and the proposed physics guided CRNN pipeline. 


![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0009-03.png)


**Fig. 5** . Pipeline up to model entry, showing residual generation, preprocessing, feature engineering and construction of model-ready windows. 

where _wo_ and _bo_ are output-layer parameters and _σ_ ( _·_ ) denotes the logistic sigmoid. To support defendable thresholding, the post hoc calibration step is defined in Eq. (18). Using Platt-style scaling with parameters ( _a_ , _b_ ) learned on the validation set, 


![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0009-06.png)


The final calibrated decision rule is defined in Eq. (19). A binary alarm is produced by thresholding the calibrated probability: 


![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0009-08.png)


where _y_ ˆ = 1 denotes `Faulty` and _y_ ˆ = 0 denotes `FaultFree` . Together, Eqs. (18) and (19) ensure that the operating thresholds reported later are tied to calibrated probabilities rather than raw scores. 

#### _Relation to the baseline CRNN_ 

Table 3 situates the proposed formulation relative to a basic CRNN by highlighting the three additions that define the proposed method: physics-based reference prediction and residual construction in Eqs. (7–8), SHAPguided feature selection in Eq. (12) and calibration with a governance-ready decision rule in Eqs. (18–19). These modifications shift the model from a purely data-driven temporal classifier to a residual-centric, interpretable and deployment-oriented detector. 

Figure 5 provides an implementation-level view of the preprocessing and feature-construction blocks that produce the model-ready tensor. After this transformation, the CRNN applies temporal convolutions to capture local structure, bidirectional gated recurrent unit layers to capture longer dependencies and attention pooling to focus on informative intervals. 

Algorithm 1 summarizes the forward path from residual-enriched windows to calibrated probabilities. 5 Placing the algorithm after Fig. keeps each computational block traceable to the end-to-end workflow. 

**Scientific Reports** |        (2026) 16:17488 | https://doi.org/10.1038/s41598-026-48227-6 Content courtesy of Springer Nature, terms of use apply. Rights reserved 

9 

www.nature.com/scientificreports/ 


![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0010-01.png)


**Algorithm 1** . Physics-guided CRNN anomaly detection pipeline with selection, calibration and validation 

### **Early warning metrics and threshold governance** 

In addition to discrimination and calibration, deployment readiness is evaluated through early-warning and alarm-governance metrics. The objective is to quantify how quickly the first alarm is raised after fault injection and how frequently nuisance alarms occur during fault-free operation. All alarm decisions use the calibrated decision rule in Eq. (run, let _t_ 0 be the known fault injection step and let 19). The first-alarm time is defined before the detection-delay equation in Eq. ( _y_ ˆ _t_ denote the binary alarm at time _t_ . The first alarm time is21). For each 


![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0010-05.png)


The detection delay is then defined in Eq. (21) as 


![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0010-07.png)


and the delay in minutes is _d ·_ ∆ _t_ , where ∆ _t_ denotes the sampling period. The early-warning rate used for fixed response horizons is defined in Eq. (22). For a chosen horizon _X_ , the percentage of runs that trigger an alarm within _X_ steps after fault injection is 


![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0010-09.png)


where _N_ is the number of runs for a given fault IDV or fault family. We report EW@100, EW@200 and EW@300 to reflect fast, moderate and conservative response policies. The nuisance-alarm metric is defined in Eq. (23). Let _H_ be the total fault-free duration in hours and let _A_ be the number of alarm events under a threshold _δ_ . The false alarm rate per hour is 


![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0010-11.png)


**Scientific Reports** |        (2026) 16:17488 | https://doi.org/10.1038/s41598-026-48227-6 Content courtesy of Springer Nature, terms of use apply. Rights reserved 

10 

www.nature.com/scientificreports/ 

where an alarm event is counted as a maximal contiguous sequence of _y_ ˆ _t_ = 1 so that a prolonged excursion is treated as one operational alert. The threshold-governance policy used to select a recommended operating point is formalized in Eq. (24). The selected threshold _δ_<sup>_⋆_</sup> maximizes recall under a false-alarm budget: 

_δ_<sup>_⋆_</sup> = arg max _δ_ TPR( _δ_ ) subject to FAR _/_ h( _δ_ ) _≤ τ,_ (24) 

where _τ_ denotes the maximum allowable false alarm rate, such as _τ_ = 1 alarm per hour for aggressive early warning or _τ_ = 0 _._ 1 alarms per hour for conservative monitoring. 

### **Robustness evaluation under shift and sensor noise** 

To assess deployment stability under realistic disturbances, robustness is evaluated through two controlled perturbations applied at test time: additive Gaussian noise and sensor dropout. Let time _t_ after preprocessing and feature selection and let _x_ ˜ _t_ denote the perturbed input. The Gaussian perturbation _xt_ denote the model input at model is defined in Eq. (25) as 

_x_ ˜ _t_ = _xt_ + _ϵ, ϵ ∼ N_ (0 _, σ_<sup>2</sup> ) _,_ (25) 

where _σ_ controls the perturbation magnitude. The sensor-dropout perturbation is defined in Eq. (26). A fraction _p_ of input channels is randomly masked after normalization: 

_x_ ˜ _t,d_ = { 0 _x,t,d,_ withotherwise,probability _p,_ (26) 

where _d_ indexes the selected features. The relative degradation metrics used to summarize robustness are defined in Eq. (27). For each perturbation level, we report the changes in discrimination and calibration relative to the clean test set: 

∆F1 = F1pert _−_ F1clean _,_ ∆ECE = ECEpert _−_ ECEclean _._ (27) Here, _t_ 0 denotes the simulator-defined fault injection time for a given Tennessee Eastman Process run, namely the time step at which the benchmark disturbance becomes active. For the empirical threshold sweep, the binary decision rule is restated in Eq. (28) for calibrated probabilities _pt_ : 


![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0011-11.png)


12 This threshold sweep is used to generate Fig. . The constrained threshold-selection rule used in that sweep is defined in Eq. (29): 

_δ_<sup>_⋆_</sup> = arg _δ_ max _∈_ [0 _,_ 1]<sup>TPR(</sup><sup>_δ_)</sup> s.t. FARhour( _δ_ ) _≤ τ_ FAR _,_ (29) 

The false-alarm budget used for the empirical threshold analysis is specified in Eq. (30): 

_τ_ FAR = 0 _._ 1 h<sup>_−_1</sup> _._ (30) 

#### _Robustness to reference-model mismatch_ 

In practical industrial deployment, the nominal reference model used for residual generation may be imperfect because of model-plant mismatch, parameter drift, sensor bias or unmodeled dynamics. Such errors can distort the residual signal and thereby affect both discrimination and threshold governance. To assess this sensitivity, we deliberately perturb the nominal reference-model prediction before residual computation. Let the nominal reference prediction used in Eq. (8). The perturbed prediction _y_ ˜ _t_ is defined in Eq. (31 _y_ ˆ _t_ ), where _∈_ R<sup>_D_</sup> denote _λ ≥_ 0 controls the mismatch magnitude, _σy_ is the per-channel standard deviation estimated from the training split, _⊙_ denotes elementwise multiplication and _b ∈_ R<sup>_D_</sup> is an optional bias term. In the main protocol, we set _b_ = 0 and vary _λ ∈{_ 0 _._ 00 _,_ 0 _._ 05 _,_ 0 _._ 10 _,_ 0 _._ 20 _}_ to represent clean, mild, moderate and stronger mismatch conditions: 


![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0011-18.png)


The resulting residual under mismatch is then given by Eq. (32), which makes explicit that degradation in the nominal reference is transferred directly into the residual channel consumed by the downstream detector: 


![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0011-20.png)


For completeness, the injected mismatch strength is also quantified by the normalized perturbation magnitude in Eq. (33): 


![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0011-22.png)


**Scientific Reports** |        (2026) 16:17488 | https://doi.org/10.1038/s41598-026-48227-6 Content courtesy of Springer Nature, terms of use apply. Rights reserved 

11 

www.nature.com/scientificreports/ 

where _ε >_ 0 is a small numerical-stability constant. To isolate the effect of reference-model quality, the trained detection model, the post hoc calibration mapping and the threshold-selection protocol are kept unchanged and only the nominal prediction used in residual generation is perturbed at test time. Performance is then reevaluated using the same deployment-oriented metrics as in “Early warning metrics and threshold governance” and “subsec:robustnessspsmethod”, namely F1-score, expected calibration error (ECE), false alarm rate per hour (FAR/h), area under the receiver operating characteristic curve (AUC) and median detection delay. Relative degradation with respect to the clean-reference case is summarized in Eq. (34): 


![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0012-02.png)


where the subscript 0 denotes evaluation with the unperturbed nominal reference model. This protocol directly tests how sensitive the residual-guided pipeline is to degradation in the underlying nominal reference and whether calibration and threshold governance remain stable when the residual input is contaminated by reference-model error. 

### **Training, hyperparameter search and calibration** 

Hyperparameters were selected with Optuna using validation loss as the optimization objective and early 4 stopping was used to reduce overfitting and terminate training after convergence. Table reports the final training configuration used to generate the results in “Results”, together with runtime-related details that clarify the computational cost of model development. In particular, the table records the stopping criterion, the number of optimization trials and the observed training time on the hardware platform summarized in Table 6. This also fixes the architecture footprint used for latency, memory and deployment-related claims. 

After checkpoint selection, raw model outputs were calibrated to produce probabilities suitable for thresholding and operational decision support. Figure 6 summarizes the validation suite used to assess both discrimination and probability reliability. The calibration stage was applied after hyperparameter selection and checkpoint selection on the validation split so that the final test results reflect the full trained-and-calibrated pipeline rather than raw classifier scores alone. 

### **Baseline models and comparative training protocol** 

To contextualize the performance of the proposed framework, we evaluate a set of baseline models under the same binary detection setting. In all cases, IDV 0 is treated as the normal class and all fault modes are grouped into the faulty class, so each model solves the same `FaultFree` / `Faulty` decision problem. Unless noted otherwise, all baselines use the same train/validation/test partition and the same preprocessing pipeline described in “Data preprocessing and quality control”. 

The comparison set includes both classical machine-learning and deep-learning baselines in order to cover a representative range of temporal and non-temporal detection paradigms. Specifically, the evaluated models are Logistic Regression (LR), Support Vector Machine (SVM), Random Forest (RF), LightGBM, Long Short- 

|**Property**|**Type**|**Value**|**Notes**|
|---|---|---|---|
|Learning rate|Continuous|0.0012|Log-scale Optuna search|
|Batch size|Discrete|64|Candidate range: 16-128|
|Optimizer|Categorical|Adam|Stable convergence in preliminary trials|
|Weight decay|Continuous|1_×_10<sup>_−_5</sup>|Regularization|
|Conv blocks|Integer|2|Number of Conv1D layers|
|Filters per block|List[int]|[32, 64]|Progressive channel depth|
|Kernel size|Integer|5|Temporal receptive feld|
|Dropout (Conv)|Continuous|0.30|Regularization|
|RNN type|Categorical|GRU|Lower latency than LSTM|
|Hidden size|Integer|128|Latent dimension|
|RNN layers|Integer|2|Model depth|
|Dropout (RNN)|Continuous|0.20|Applied between recurrent layers|
|Sequence window|Integer|120|Input sequence length|
|Maximum epochs|Integer|100|Upper bound before early stopping|
|Early stopping patience|Integer|10|Stop if validation loss does not improve|
|Best epoch|Integer|15|Epoch of selected checkpoint|
|Optuna trials|Integer|50|Number of hyperparameter search trials|
|Training seeds|Integer|3|Independent runs for stability check|
|Total training time|Runtime|1.6 hours|End-to-end training including Optuna search|
|Average time per epoch|Runtime|36 s|Mean epoch duration on reported hardware|
|Data split|Ratio|70/20/10|Train/validation/test|
|Training platform|Text|Table6|Hardware/sofware reported separately|



**Table 4** . Final training configuration and runtime summary for the proposed CRNN. 

**Scientific Reports** |        (2026) 16:17488 | https://doi.org/10.1038/s41598-026-48227-6 Content courtesy of Springer Nature, terms of use apply. Rights reserved 

12 

www.nature.com/scientificreports/ 


![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0013-01.png)


**Fig. 6** . Model evaluation summary, including discrimination curves and calibration reliability analysis for probability quality. 

|**Model**|**Type**|**Final hyperparameter setting**|
|---|---|---|
|Logistic regression|Classical ML|Penalty = L2,_C_= 1.0, solver = lbfgs|
|Support vector machine|Classical ML|Kernel = RBF,_C_= 10, gamma = scale|
|Random forest|Classical ML|Trees = 300, max depth = 20, min samples leaf = 2|
|LightGBM|Gradient boosting|Estimators = 500, learning rate = 0.05, num leaves = 64, max depth = 10|
|LSTM|Deep sequential|Hidden size = 128, layers = 2, dropout = 0.2, learning rate =1_×_10<sup>_−_3</sup>|
|CNN-LSTM|Hybrid sequential|Conv flters = 64, kernel size = 5, LSTM hidden size = 128, dropout = 0.2|
|Proposed physics-guided CRNN|Proposed model|See Table4; calibration = Platt scaling, threshold policy = Eq. (24)|



**Table 5** . Baseline models and final hyperparameter settings used for comparative evaluation. 

Term Memory (LSTM), CNN-LSTM and the proposed Physics-Guided CRNN. For non-sequential baselines, window-level descriptors are flattened into fixed-dimensional vectors. For sequential baselines, the same sequence-construction policy used by the proposed model is retained for fairness. 

Table 5 summarizes the final hyperparameter settings used for comparative evaluation. These settings are intended to provide a fair and reproducible reference point rather than an exhaustive search over every possible baseline architecture. 

For fairness, all models are trained once under the same global binary labeling protocol rather than as separate detectors for individual fault modes. The per-fault analysis reported later therefore reflects fault-wise evaluation of globally trained detectors rather than fault-specific retraining. 

### **Evaluation protocol and deployment reporting** 

Model performance is reported using per-fault breakdowns and time-sensitive scoring and statistical reliability is quantified using bootstrap confidence intervals computed with the bias-corrected and accelerated (BCa) procedure. The BCa adjustment used in this study is defined in Eq. (35): 


![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0013-10.png)


This links the reported metrics in “Results” to uncertainty-aware interval estimates rather than single-split point values. 

To support edge-feasibility claims, latency, throughput, parameter count and memory footprint are reported 6 using a fixed benchmark setup and the minimum requirements listed in Table . The table also specifies the software versions required to reproduce the pipeline end to end. 

## **Results** 

This section reports the empirical performance of the proposed physics-guided convolutional recurrent neural network (CRNN) introduced in “Methodology”. Unlike studies that report discrimination alone, the evaluation follows the full pipeline defined in Algorithm 1: residuals are formed by Eq. (8), residual-enriched inputs are constructed by Eqs. (10)–(11), feature selection follows “Feature construction and SHAP-guided selection” and calibrated probabilities are obtained through Eq. (18) before thresholding by Eq. (19). Unless stated otherwise, all results use the run-level split described in “Dataset and split” and calibration parameters are fitted on the validation set as described in “Training, hyperparameter search and calibration”. 

**Scientific Reports** |        (2026) 16:17488 | https://doi.org/10.1038/s41598-026-48227-6 Content courtesy of Springer Nature, terms of use apply. Rights reserved 

13 

www.nature.com/scientificreports/ 

|**Property**|**Type**|**Description or value**|**Notes**|
|---|---|---|---|
|CPU|Hardware|Quad core x86 or ARM|Recommended: Eight core with AVX or ARM big cores|
|Memory|Hardware|8 GB RAM|Recommended: 16-32 GB|
|Storage|Hardware|20 GB SSD|Recommended: 100 GB NVMe|
|Operating system|Sofware|Ubuntu 22.04 LTS or Windows 11|Primary runtime|
|Python|Sofware|3.10|Pipeline and training|
|PyTorch|Sofware|2.3|Training and export|



**Table 6** . Minimal hardware and software requirements. 


![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0014-03.png)



![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0014-04.png)


**Fig. 7** . Optimization dynamics for the proposed physics-guided CRNN under the run-level split in “Dataset and split”. 

### **Training dynamics and convergence stability** 

We first examine whether the proposed architecture in “Proposed physics-guided CRNN architecture” trains stably under the run-aware split in “Dataset and split”. Stable optimization is important in industrial settings because unstable retraining can translate into inconsistent alarm behavior across operating regimes. Figure 7 summarizes the optimization trajectory. The loss curves show rapid convergence with a small train-validation gap and validation accuracy remains stable across epochs. This behavior is consistent with the hyperparameters selected by Optuna in Table 4 and indicates that the temporal encoder and attention mechanism in Eqs. (15)–(16) provide sufficient capacity without severe overfitting. The absence of oscillatory or divergent loss patterns further suggests stable gradient propagation through the convolutional and recurrent blocks despite the long temporal windows. 

### **Representation separability under regime variability** 

To assess whether residual-enriched learning improves separation between `FaultFree` and `Faulty` states, we analyze hidden representations produced by the encoder defined in Eqs. (13)–(16). Because the model ingests residual-enriched features built from Eqs. (8) and (10), separability in the latent space provides indirect evidence that physics-informed deviations create a cleaner decision boundary than raw signals alone. 

Figure 8a shows a t-SNE projection of hidden states, where the normal and faulty samples form two relatively compact regions with limited overlap. Figure 8b presents the corresponding confusion matrix on the held-out test set. The remaining errors are sparse and concentrate near ambiguous boundaries, which is consistent with the weak and irregular signatures of random-variation faults discussed in “Literature review”. 

### **Discrimination performance and operating flexibility** 

We next report threshold-independent discrimination metrics commonly used in Tennessee Eastman Process studies. Figure 9a shows the precision-recall curve and Fig. 9b shows the receiver operating characteristic (ROC) 18 curve, both computed from calibrated probabilities obtained after Eq. ( ) and before fixing a threshold in Eq. (19). Both curves remain close to their ideal envelopes, indicating strong separability and suggesting that multiple operating thresholds are feasible with only limited performance loss. 

### **Calibration reliability and statistical stability** 

Threshold governance depends on probability outputs that reflect empirical correctness, so that the decision threshold in Eq. (19) functions as a policy variable rather than an arbitrary tuning knob. To quantify stability 

**Scientific Reports** |        (2026) 16:17488 | https://doi.org/10.1038/s41598-026-48227-6 Content courtesy of Springer Nature, terms of use apply. Rights reserved 

14 

www.nature.com/scientificreports/ 


![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0015-01.png)



![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0015-02.png)


**Fig. 8** . Representation quality and classification behavior of the proposed physics-guided CRNN learned from residual-enriched inputs. 


![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0015-04.png)



![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0015-05.png)


**Fig. 9** . Discrimination diagnostics for the proposed physics-guided CRNN under the protocol in Algorithm 1. 

beyond a single split, we additionally report bootstrap uncertainty using the bias-corrected and accelerated (BCa) procedure defined in Eq. (35). Figure 10 shows bootstrap distributions for accuracy, area under the curve (AUC) and F1-score. The relatively narrow spreads indicate that the reported performance is not driven by a single favorable partition. 

Figure 11 compares reliability curves before and after Platt scaling, where calibration follows Eq. (18) and is fitted on the validation set as described in “Training, hyperparameter search and calibration”. Before calibration, the model is overconfident in some probability regions. After calibration, the curve moves closer to the diagonal, indicating improved alignment between predicted confidence and observed correctness. 

### **Ablation evidence for residuals, attention and calibration** 

To connect the empirical results to the methodological claims in “Methodology”, we isolate the effects of residual enrichment, attention pooling and calibration. Table 7 reports the ablation study across accuracy, F1-score, AUC and expected calibration error (ECE). 

Residual enrichment improves discrimination relative to the base CRNN, which is consistent with the residual construction in Eq. (8) and the fusion stage in Eq. (10). Calibration produces the largest reduction in ECE, consistent with the reliability improvement observed in Figure 11. The full configuration, which matches 

**Scientific Reports** |        (2026) 16:17488 | https://doi.org/10.1038/s41598-026-48227-6 Content courtesy of Springer Nature, terms of use apply. Rights reserved 

15 

www.nature.com/scientificreports/ 


![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0016-01.png)



![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0016-02.png)



![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0016-03.png)


**Fig. 10** . Bootstrap reliability of discrimination metrics using the BCa procedure in Eq. (35). 


![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0016-05.png)



![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0016-06.png)


**Fig. 11** . Probability calibration behavior before and after applying Eq. (18). 

|**Confguration**|**Type/variation**|**Description or value**|**Notes**|
|---|---|---|---|
|Base CRNN|Baseline model|Accuracy 0.95, F1 0.90, AUC 0.95, ECE 0.07|Without residual features|
|CRNN + Residual features|Architecture variant|Accuracy 0.97, F1 0.92, AUC 0.96, ECE 0.05|Residual enrichment improves detection|
|CRNN + Residual (no calibration)|Variant w/o post-calibration|Accuracy 0.97, F1 0.92, AUC 0.96, ECE 0.08|Discrimination holds, calibration degrades|
|CRNN + Residual + Attention|Full model|**Accuracy 0.98**,**F1 0.94**,**AUC 0.97**,**ECE 0.03**|Best overall and lowest calibration error|



**Table 7** . Ablation of key components with accuracy, F1 score, area under the ROC curve (AUC) and expected calibration error (ECE). 

Algorithm 1 and the architecture in “Proposed physics-guided CRNN architecture”, provides the strongest overall balance between discrimination and probability quality. 

### **Per-fault detection performance and fault-family patterns** 

To provide a more detailed view of model behavior across the Tennessee Eastman benchmark, we analyze detection performance at the level of individual fault modes and broader fault families. The model outputs a calibrated abnormality probability through Eq. (18), which is mapped to a binary decision using Eq. (19). Table 8 therefore summarizes performance for each fault mode in terms of F1-score, AUC, ECE and support. 8 The values in Table are obtained by applying the final trained detector to fault-specific evaluation subsets derived from the test partition. For each fault IDV _j_ , the corresponding subset contains normal samples together with samples from that fault mode. The same trained model, calibration mapping and decision policy are used throughout, which makes it possible to assess how the learned boundary transfers across different abnormal operating conditions while remaining consistent with the global binary training setup. 

**Scientific Reports** |        (2026) 16:17488 | https://doi.org/10.1038/s41598-026-48227-6 Content courtesy of Springer Nature, terms of use apply. Rights reserved 

16 

www.nature.com/scientificreports/ 

|**Fault or Group**|**Category**|**F1-score**|**AUC**|**ECE**|**Support**|**Notes**|
|---|---|---|---|---|---|---|
|Normal|||||||
|IDV 0|Baseline|0.99|1.00|0.01|145000|Reference operating mode|
|Feed and compos<br>|ition<br>|||||<br>|
|IDV 1|Process|0.93|0.97|0.03|7300|Strong detection against IDV 0|
|IDV 2|Process|0.91|0.96|0.03|7200|Reliable separation from normal|
|IDV 3|Sensor|0.89|0.95|0.04|7100|Mild degradation under binary evaluation|
|IDV 8|Process|0.89|0.95|0.04|7100|Composition-dependent separation|
|IDV 9|Sensor|0.87|0.94|0.05|6900|Reduced confdence stability|
|Utilities and cooli<br>|ng<br>|||||<br>|
|IDV 4|Utility|0.92|0.96|0.03|7200|Cooling anomaly detected reliably|
|IDV 5|Utility|0.89|0.95|0.04|7000|Cooling deviation vs normal|
|IDV 10|Utility|0.93|0.97|0.03|7200|Clear thermal separation|
|IDV 11|Utility|0.90|0.95|0.04|7100|Similar thermal signature|
|IDV 14|Utility|0.91|0.96|0.04|7100|Flow disruption detected well|
|Supply and pressu|re||||||
|IDV 6|Process|**0.94**|**0.98**|**0.02**|7400|High separability from normal|
|IDV 7|Pressure|0.91|0.96|0.03|7100|Stable binary detection|
|Reaction and con|trol||||||
|IDV 12|Chemical|0.90|0.95|0.04|7000|Nonlinear deviation remains detectable|
|IDV 13|Mechanical|**0.94**|**0.98**|**0.02**|7400|High binary reliability|
|Random variation|family||||||
|IDV 15|Noise|0.86|0.93|0.05|6800|Lower separability from normal|
|IDV 16|Noise|0.83|0.92|0.06|6700|Weak abnormal signal|
|IDV 17|Noise|0.87|0.94|0.05|6900|Slight improvement over IDV 16|
|IDV 18|Noise|0.90|0.95|0.04|7000|Better calibrated separation|
|IDV 19|Noise|0.89|0.94|0.04|7000|Low-amplitude deviation|
|IDV 20|Noise|0.87|0.93|0.05|6900|Reduced discriminability|
|Macro average|Aggregate|**0.91**|**0.96**|**0.04**|–|Unweighted mean across fault-specifc binary evaluations<br>|
|Weighted average|Aggregate|**0.94**|**0.97**|**0.03**|–|Weighted by fault-specifc support|



**Table 8** . Per-fault _detection_ performance of the proposed binary detector, grouped by fault family. Each row is obtained by evaluating the same trained `FaultFree` / `Faulty` model on a binary test subset containing IDV 0 normal samples and one fault mode IDV _j_ . 

The results show that detection quality varies across fault families. Supply-, pressure- and mechanically related faults are generally more separable from normal operation, whereas the random-variation family remains more difficult. This suggests that some fault modes generate clearer residual and temporal signatures than others, which is reflected in both discrimination and calibration behavior. 

Table 8 therefore does not represent multiclass diagnosis; instead, it shows how well the same globally trained binary detector separates normal operation from each fault mode when evaluated one fault at a time. Because these families differ in both separability and calibration, the final threshold still requires explicit governance. 

### **Early warning quality and threshold governance** 

Industrial monitoring requires alarm decisions that are not only accurate, but also timely, stable and operationally controllable. Following “Early warning metrics and threshold governance”, we quantify detection delay using Eq. (21), early-warning rate using Eq. (22) and nuisance alarms using the false alarm rate per hour in Eq. (23). 24 The operating threshold is selected using the governance rule in Eq. ( ), so that the final alarm policy remains reproducible and auditable. 

Figure 12 summarizes the threshold-sensitivity analysis performed on calibrated probabilities. The threshold _δ_ is swept over the admissible interval _δ ∈_ [0 _,_ 1] according to Eq. (28). For each candidate threshold, three quantities are evaluated: the true-positive rate TPR( _δ_ ), precision and the false-alarm rate per hour FARhour( _δ_ ). The selected operating point is determined by Eq. (29) under the false-alarm budget defined in Eq. (30), yielding _δ_<sup>_⋆_</sup> = 0 _._ 55. 

As expected, increasing _δ_ reduces nuisance alarms, whereas very small thresholds lead to higher falsealarm burden. At the same time, the detector maintains strong true-positive behavior across a broad operating range before performance begins to decline under overly strict thresholds. This behavior supports the use of a governance-based operating point instead of heuristic threshold selection. Using _δ_<sup>_⋆_</sup> , the resulting early-warning behavior is summarized in Table 9 . The median and 90th percentile delays indicate how quickly the first alarm is raised after fault injection, while FAR/h measures nuisance alarms during nominal operation. The F1-score column links the selected governance policy back to detection quality. 

**Scientific Reports** |        (2026) 16:17488 | https://doi.org/10.1038/s41598-026-48227-6 Content courtesy of Springer Nature, terms of use apply. Rights reserved 

17 

www.nature.com/scientificreports/ 


![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0018-01.png)


**Fig. 12** . Threshold-sensitivity analysis on calibrated probabilities. The horizontal axis shows the decision threshold _δ ∈_ [0 _,_ 1] and the vertical axis shows the corresponding metric values for FARhour( _δ_ ), TPR( _δ_ ) and precision. The dashed vertical line marks the selected operating threshold _δ_<sup>_⋆_</sup> = 0 _._ 55, obtained from Eq. (29) and the dotted horizontal line marks the false-alarm budget _τ_ FAR = 0 _._ 1 h<sup>_−_1</sup> from Eq. (30). 

|**Fault IDV**|**Median delay**|**90th pct delay**|**FAR/h**|**F1**|
|---|---|---|---|---|
|IDV 1|16 steps|48 steps|0.08|0.93|
|IDV 2|18 steps|52 steps|0.08|0.91|
|IDV 3|22 steps|60 steps|0.08|0.89|
|IDV 4|17 steps|50 steps|0.08|0.92|
|IDV 5|24 steps|65 steps|0.08|0.89|
|IDV 6|12 steps|36 steps|0.08|0.94|
|IDV 7|15 steps|45 steps|0.08|0.91|
|IDV 15|40 steps|120 steps|0.08|0.86|
|IDV 16|55 steps|160 steps|0.08|0.83|
|IDV 17|46 steps|140 steps|0.08|0.87|
|IDV 18|30 steps|95 steps|0.08|0.90|
|IDV 19|34 steps|110 steps|0.08|0.89|
|IDV 20|44 steps|130 steps|0.08|0.87|
|Macro average|28 steps|86 steps|0.08|0.91|
|Weighted average|21 steps|62 steps|0.08|0.94|



**Table 9** . Early-warning and governance metrics at the selected operating threshold _δ_<sup>_⋆_</sup> obtained from Eq. (24). 

|**Output type**|**ECE**|**Brier**|**NLL**|**MCE**|**Reliability slope**|
|---|---|---|---|---|---|
|Uncalibrated CRNN|0.07|0.06|0.18|0.14|1.42|
|CRNN + Temperature scaling|0.05|0.05|0.15|0.10|1.18|
|CRNN + Isotonic regression|0.04|0.05|0.14|0.09|1.10|
|CRNN + Platt scaling (proposed)|0.03|0.04|0.12|0.06|1.03|



**Table 10** . Calibration quality before and after post-hoc probability calibration. 

Taken together, Fig. 12 and Table 9 show that calibrated probabilities can be translated into an explicit and auditable alarm policy. We next examine calibration quality beyond ECE and then present explanation evidence to clarify why alarms are produced. 

### **Calibration metrics beyond ECE and operator-facing explanation evidence** 

Expected calibration error does not fully characterize probability quality, so we additionally report Brier score and negative log-likelihood for the calibrated outputs obtained through Eq. (18). Table 10 compares the uncalibrated 

**Scientific Reports** |        (2026) 16:17488 | https://doi.org/10.1038/s41598-026-48227-6 Content courtesy of Springer Nature, terms of use apply. Rights reserved 

18 

www.nature.com/scientificreports/ 

model with several post hoc calibration strategies. Consistent with Fig. 11, Platt scaling improves ECE, Brier score and negative log-likelihood simultaneously, indicating better alignment between predicted probabilities and empirical correctness. This directly strengthens the threshold-governance procedure in Eq. (24). 

Beyond these global summaries, explanation evidence is needed to identify which variables drive alarm decisions. Figure 13 shows representative fault-wise local explanation snapshots. Each color-coded block corresponds to one selected fault example and highlights the channels or descriptors receiving the strongest attribution for that individual alarm decision. The figure contrasts selected supply-, pressure- and randomvariation-related examples to illustrate how local explanation profiles differ across fault families. 

Figure 14, by contrast, provides a global summary across the evaluation set. It reports the top-10 most influential operator-facing features ranked under the SHAP-guided feature-selection framework described in “Feature construction and SHAP-guided selection”. Whereas Fig. 13 explains individual alarm cases, Fig. 14 identifies the features that matter most consistently across many decisions. 

Together, Figs. 13 and 14 support both alarm interpretation and maintenance handoff by showing why specific alarms arise and which variables matter most overall. 

### **Robustness under perturbations and sensor loss** 

We finally evaluate deployment stability under controlled disturbances using the protocol in “Robustness evaluation under shift and sensor noise”. Additive noise is applied according to Eq. (25), sensor dropout follows Eq. (26) and performance changes are summarized using Eq. (27). 

Table 11 shows that moderate perturbations cause only small decreases in F1-score and limited increases in ECE, indicating that calibrated probabilities remain usable for decision governance under realistic noise and partial sensor loss. Heavier corruption produces larger degradation, which motivates drift monitoring and periodic recalibration as part of operational deployment. 

Overall, these results show that the residual-guided and calibrated pipeline remains stable under moderate perturbations and degrades in a predictable manner under stronger disturbances. 

### **Robustness under reference-model mismatch** 

In addition to the disturbance results reported in “Robustness under perturbations and sensor loss”, we evaluate robustness to controlled reference-model mismatch using the protocol in “3.8”. Whereas the previous analysis perturbs the observed input stream through additive noise and sensor loss, the present experiment perturbs the nominal prediction used for residual generation before applying Eq. (31). The trained CRNN, the post hoc calibration mapping and the threshold-selection policy are kept unchanged. This design isolates the effect of degraded reference quality from the remaining stages of the detection pipeline. 

Table 12 summarizes the resulting performance as the mismatch magnitude increases. At low mismatch levels, the proposed framework remains relatively stable, indicating that the residual-guided representation does not require a perfectly accurate nominal reference in order to remain informative. As the mismatch grows, however, discrimination weakens, calibration quality deteriorates and nuisance alarms become more frequent. 


![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0019-12.png)


**Fig. 13** . Representative per-fault local explanation snapshots for selected fault families. Each color-coded block corresponds to one selected fault example and shows the channels and descriptors that contribute most strongly to the corresponding alarm decision. Exact fault IDs and families are indicated in the legend. 

**Scientific Reports** |        (2026) 16:17488 | https://doi.org/10.1038/s41598-026-48227-6 Content courtesy of Springer Nature, terms of use apply. Rights reserved 

19 

www.nature.com/scientificreports/ 


![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0020-01.png)


**Fig. 14** . Global top-10 operator-facing feature-importance summary under the SHAP-guided selection procedure in “Feature construction and SHAP-guided selection”. Unlike Fig. 13, which shows local faultspecific explanations, this figure ranks the features that contribute most consistently across the evaluation set. 

|**Perturbation**|**Level**|**∆ F1**|**∆ ECE**|**Interpretation**|
|---|---|---|---|---|
|Gaussian noise|_σ_ = 0_._05|_−_0_._01|+0_._01|Mild degradation|
|Gaussian noise|_σ_ = 0_._10|_−_0_._03|+0_._02|Stable under moderate noise|
|Gaussian noise|_σ_ = 0_._20|_−_0_._06|+0_._04|Larger impact at high noise|
|Sensor dropout|_p_ = 0_._10|_−_0_._02|+0_._01|Graceful degradation|
|Sensor dropout|_p_ = 0_._20|_−_0_._04|+0_._02|Moderate loss tolerated|
|Sensor dropout|_p_ = 0_._30|_−_0_._08|+0_._05|Performance drops with heavy masking|



**Table 11** . Robustness to controlled perturbations using the protocol in “Robustness evaluation under shift and sensor noise”. 

|**Mismatch level**|**F1**|**ECE**|**FAR/h**|**AUC**|**Interpretation**|
|---|---|---|---|---|---|
|Clean reference,_λ_ = 0_._00|0.93|0.03|0.08|1.00|Baseline condition|
|Low mismatch,_λ_ = 0_._05|0.92|0.04|0.09|0.99|Mild degradation with stable operation|
|Moderate mismatch,_λ_ = 0_._10|0.90|0.05|0.11|0.97|Noticeable degradation but still usable|
|High mismatch,_λ_ = 0_._20|0.87|0.07|0.14|0.94|Strong degradation with increased threshold sensitivity|



**Table 12** . Robustness under controlled reference-model mismatch. The nominal reference prediction is perturbed according to Eq. (31) before residual computation. 

This behavior is consistent with the fact that residuals under model-plant mismatch contain both genuine fault information and spurious deviation introduced by reference error. 

Figure 15 provides a visual summary of the same trend using side-by-side line plots versus mismatch magnitude. Panel (a) reports the discrimination-related metrics F1 and AUC, while panel (b) reports the calibration and false-alarm metrics ECE and FAR/h. Similar to the controlled perturbation results in “Robustness under perturbations and sensor loss”, the framework remains tolerant to modest degradation, but not insensitive to it. This is an important practical finding because it indicates that the method can still operate when the nominal model is only approximate, while also confirming that calibration and threshold governance become increasingly important as mismatch grows. 

Taken together, these results show that the proposed residual-guided and calibrated detector does not depend on perfect model-plant agreement, but its performance degrades progressively as the nominal reference becomes less accurate. This supports the view that residuals should be treated as informative but imperfect signals whose operational usefulness depends on both reference quality and downstream decision governance. 

**Scientific Reports** |        (2026) 16:17488 | https://doi.org/10.1038/s41598-026-48227-6 Content courtesy of Springer Nature, terms of use apply. Rights reserved 

20 

www.nature.com/scientificreports/ 


![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0021-01.png)



![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0021-02.png)



![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0021-03.png)



![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0021-04.png)



![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0021-05.png)



![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0021-06.png)



![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0021-07.png)



![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0021-08.png)


**Fig. 15** . Performance under controlled reference-model mismatch. The horizontal axis shows the mismatch magnitude _λ_ defined in Eq. (31). Panel ( **a** ) shows progressive degradation in F1 and AUC as mismatch increases, while panel ( **b** ) shows worsening calibration and increased nuisance alarms through ECE and FAR/h. 

|**Model**|**F1-score**|**AUC**|**ECE**|**FAR/h**|**Median delay**|**Notes**|
|---|---|---|---|---|---|---|
|Logistic regression|0.84|0.90|0.11|0.15|60 steps|Linear baseline|
|Support vector machine|0.87|0.93|0.09|0.13|48 steps|Margin-based classifer|
|Random forest|0.89|0.94|0.08|0.11|40 steps|Nonlinear tree ensemble|
|LightGBM|0.91|0.96|0.07|0.10|36 steps|Strong tabular baseline|
|LSTM|0.90|0.95|0.08|0.10|35 steps|Sequential baseline|
|CNN-LSTM|0.92|0.97|0.06|0.09|32 steps|Hybrid temporal baseline|
|Proposed physics-guided CRNN|0.93|1.00|0.03|0.08|28 steps|Residual-guided + calibrated|



**Table 13** . Comparison of baseline models and the proposed method under the same binary fault-detection protocol. Bold values indicate the best performance across models. 

### **Comparison with baseline models** 

To assess the effectiveness of the proposed framework, we compare it against the baseline models introduced in “Baseline models and comparative training protocol”. Table 13 reports discrimination, calibration and governance-oriented metrics for all methods. In addition to F1-score and AUC, we report ECE to assess probability quality, FAR/h to quantify nuisance alarms and median detection delay to reflect early-warning usefulness. 

The proposed Physics-Guided CRNN provides the most balanced performance across discrimination, calibration and operational alarm control. Classical baselines remain competitive in simpler cases but have limited capacity to model longer temporal dependencies. Sequential deep baselines improve detection quality, but they still lack the explicit residual guidance, calibration layer or threshold-governance structure of the proposed framework. 

All models in Table 13 were trained under the same global binary labeling protocol rather than separately for each fault mode. Their reported scores therefore reflect evaluation under the same partition and decision policy, so the observed differences are attributable to the modeling approach rather than to different training regimes. 

### **Summary of findings** 

Across the evaluation suite, the proposed physics-guided CRNN shows stable training dynamics (Fig. 7), strong latent separability (Fig. 8) and near-ideal discrimination behavior (Fig. 9). Calibration through Eq. (18) improves reliability (Fig. 11) and strengthens probability quality under multiple metrics (Table 10), which in turn enables auditable threshold governance through Eq. (24) as illustrated in Fig. 12. Per-fault results in Table 8 show strongest performance for supply, pressure and mechanical faults, while random variation remains the most challenging family. Operator-facing explanations in Figs. 13 and 14 further support practical handoff by linking alarms to dominant sensors and residual descriptors and the robustness analysis in Table 11 shows graceful degradation under moderate noise and partial sensor loss. 

**Scientific Reports** |        (2026) 16:17488 | https://doi.org/10.1038/s41598-026-48227-6 Content courtesy of Springer Nature, terms of use apply. Rights reserved 

21 

www.nature.com/scientificreports/ 

## **Discussion and comparison** 

This section interprets the reported results in relation to prior Tennessee Eastman Process studies, practical deployment requirements and the limitations of residual-centric, calibrated anomaly detection for industrial monitoring. 

### **Comparison with literature** 

To contextualize the proposed physics-guided convolutional recurrent neural network (CRNN), Table 14 summarizes representative Tennessee Eastman Process studies spanning compact networks, attention-based convolutional neural network (CNN) variants and incipient-fault-focused designs. Reported performance varies with window length, preprocessing, class definition and whether the evaluation targets all faults or only weak incipient regimes such as IDV3, IDV9 and IDV15. These protocol differences reinforce the need to report deployment-relevant metrics and fault-wise behavior rather than relying on a single aggregate score. 

Across recent deep baselines, compressed feedforward networks typically report accuracy in the mid-90% range, whereas recurrent and autoencoder-based hybrids often improve temporal modeling but remain sensitive to excitation assumptions and horizon design. Attention-based CNN pipelines that encode temporal windows into richer representations generally report stronger aggregate performance under fixed split protocols. This pattern is consistent with the latent separability in Fig. 8 and the stable optimization behavior in Fig. 7. 

Under the split and end-to-end pipeline adopted in this work, the proposed CRNN achieves the strongest overall accuracy among the compared studies while avoiding image conversion and external excitation. More importantly, it augments strong discrimination with calibrated probabilities for auditable thresholding. The main contribution is therefore not only improved benchmark performance, but a more deployment-oriented combination of residual-guided learning and decision governance. 

### **Overview** 

The results show that combining physics-based residual evidence with a lightweight convolutional-recurrent backbone yields strong and stable anomaly detection on the Tennessee Eastman Process. Residual construction directs learning toward deviations from expected behavior while preserving channel-level interpretability and the Conv1D-bidirectional gated recurrent unit (BiGRU)-attention encoder captures both short- and long-range temporal structure under regime variability. As a result, the framework supports not only accurate detection but also probability outputs that are suitable for operational decision-making. 

### **Implications for practice** 

For practical deployment, the main lesson is that performance depends on the discipline of the full pipeline rather than on a single model block. Residual-enriched inputs improve separability and provide clearer operator-facing deviation signals, which is consistent with the gains reported in Table 7 and the family-wise trends in Table 8. Calibration then converts these scores into probabilities that support policy-driven threshold selection under explicit nuisance-alarm budgets, as shown in Fig. 12. Together, these design choices support an alarm workflow that is both accurate and governable. 

### **Limitations and threats to validity** 

The evaluation is anchored to a single simulated benchmark and a binary detection objective, which limits external validity. Although the proposed pipeline combines residual generation, temporal modeling and calibration, as formalized in Eqs. (8), (18) and (24), the reported results should be interpreted within the scope of the Tennessee Eastman benchmark rather than as direct proof of field-ready deployment. Real industrial plants may exhibit unmodeled disturbances, actuator nonlinearities, parameter drift, sensor degradation, operatingmode transitions and control interactions that are not fully captured in the present experiments. 

An important practical limitation concerns the quality of the nominal reference model used for residual 8 generation. As defined by Eq. ( ), the residual is formed as the difference between the measured process output and the nominal reference-model prediction, but in real plants such a reference is rarely perfect. Model-plant mismatch, unmodeled dynamics, sensor bias, initialization error and external disturbances can all produce nonzero residuals even under healthy operation, thereby increasing nuisance alarms or weakening 

|**Method/study**|**Year**|**Model family**|**Reported overall result**|
|---|---|---|---|
|Temporal DL for TE fault detection<sup>58</sup>|2021|Temporal deep model|Fault detection focus, metric per study|
|Hierarchical Deep LSTM<sup>59</sup>|2022|Long short-term memory (LSTM) hierarchical<br>model|Acc._≈_93.4% on all faults|
|CNN with attention mechanism<sup>60</sup>|2023|CNN + attention|Acc._≈_98.46% on all faults|
|Dense feature ensemble net for incipient fault detection<sup>61</sup>|2024|Dense feature ensemble network|Incipient fault detection focus, metric<br>per study|
|Granger-causal GAT for FD and RCD<sup>62</sup>|2024|Graph attention network|Fault detection and root-cause<br>diagnosis focus, metric per study|
|CRNN (Tis work)|2026|Residual-guided CRNN + calibration|Acc. = 99.0% under this protocol|



**Table 14** . Comparison of representative Tennessee Eastman Process reports. The reported metric is taken as stated in each source. When a study targets only incipient faults or reports a different primary metric, this is stated explicitly to avoid overstating comparability. 

**Scientific Reports** |        (2026) 16:17488 | https://doi.org/10.1038/s41598-026-48227-6 Content courtesy of Springer Nature, terms of use apply. Rights reserved 

22 

www.nature.com/scientificreports/ 

fault sensitivity. To examine this issue more directly, we introduced a controlled reference-model mismatch experiment in “Robustness under reference-model mismatch”. The results in Table 12 and Fig. 15 show that the proposed detector remains relatively stable under low mismatch levels, but discrimination, calibration quality and nuisance-alarm control degrade progressively as reference error increases. The proposed framework therefore does not assume that residuals are fault-exclusive signals; instead, it treats them as informative but imperfect inputs whose usefulness depends on the quality of the nominal reference together with downstream temporal modeling, post hoc calibration in Eq. (18) and operating-threshold selection in Eq. (24). 

This point is important when interpreting the governance and calibration results in “Early warning quality and threshold governance” and “Calibration metrics beyond ECE and operator-facing explanation evidence”. The threshold sweep in Figure 12 and the operating-point summary in Table 9 show that explicit threshold governance is necessary because alarms are influenced by nuisance deviations as well as genuine fault signatures. Likewise, the calibration improvements reported in Table 10 should be interpreted as improving probability quality under imperfect residual conditions, not as evidence of perfect model-plant agreement. 

Finally, calibration is performed offline and may drift during operation, especially under regime shifts, sensor aging or maintenance-related changes in process behavior. The explanation results in Figs. 13 and 14 improve interpretability, but they do not remove the underlying dependence of the framework on the quality of the nominal reference model and the representativeness of the benchmark data. These limitations motivate future work on adaptive recalibration, drift monitoring and evaluation under stronger plant-model mismatch conditions. 

### **Operational guidance** 

In deployment, thresholds should be selected from calibrated probabilities using an explicit nuisance-alarm budget and verified through threshold-sensitivity analysis. A practical default is to operate at the selected _δ_<sup>_⋆_</sup> , monitor early-warning delay and nuisance alarms per hour as routine health indicators and update thresholds or recalibrate when drift is detected. A conservative rollout strategy is to begin in shadow mode and promote the system to action-triggering workflows only after stability has been confirmed under noise and partial sensor loss. 

Table 15 summarizes the main method-to-evidence-to-next-step mapping. Residual evidence strengthens sensitivity and interpretability, calibrated threshold governance makes alarm policies reproducible and explanation summaries support rapid operator triage. The most important next steps are extending beyond the benchmark setting, strengthening drift monitoring and evaluating robustness under broader shift conditions. 

## **Conclusion and future work** 

This work addressed key deployment barriers in industrial anomaly detection by developing and validating a calibrated, physics-guided pipeline on the Tennessee Eastman Process benchmark. The framework integrates twin-based residual construction with compact rolling and spectral descriptors and then models the resulting residual-enriched windows using an attention-based convolutional recurrent neural network (CRNN). SHapley Additive exPlanations (SHAP)-guided feature selection reduces redundancy and improves sensor-level interpretability, while Optuna-based tuning stabilizes training and yields a compact configuration suitable for practical monitoring. Under the run-level evaluation protocol, the method delivers strong discrimination and consistent fault-family behavior, with the largest gains observed for supply, pressure and mechanical regimes, while random-variation faults remain the most challenging. 

Beyond discrimination, the study emphasizes decision governance and audit readiness. Platt scaling improves probability reliability, enabling explicit threshold selection under a nuisance-alarm budget and supporting earlywarning operation with controlled false alarms. Statistical validation via block bootstrap confidence intervals provides uncertainty-aware evidence for the reported performance and explanation outputs from SHAP and Integrated Gradients connect alarms to dominant sensors for operator triage. Overall, the results show that 

|**Aspect/theme**|**Type**|**Evidence in this study**|**Next step/extension**|
|---|---|---|---|
|Residual evidence and|modeling|<br>|<br>|
|Residual enrichment|Physics-informed|Improves detection versus the base model and supports clearer fault-family<br>separation|Track residual drif and reft the reference<br>model and scalers under controlled procedures|
|Temporal encoder|Deep temporal|Captures short- and long-range temporal structure and yields stable<br>optimization behavior|Stress-test window length and add mode-<br>aware validation where possible|
|Calibration, governance|and explanations|||
|Probability calibration|Governance layer|Improves reliability and enables stable, policy-driven operating thresholds|Monitor calibration drif and schedule<br>periodic recalibration|
|Treshold policy|Risk control|Treshold sweep exposes FAR-TPR trade-ofs and supports auditable_δ_<sup>_⋆_</sup><br>selection|Use mode- or family-specifc alarm budgets<br>if required|
|Operator explanations|Interpretability|Top-feature and per-fault snapshots identify dominant channels for<br>investigation|Test attribution stability and group features by<br>subsystem for triage|
|Deployment and extern|al validity|||
|Robustness|Shif tolerance|Controlled perturbations show graceful degradation under moderate noise<br>and dropout|Add drif detection and sensor-health<br>monitoring in production|
|Scope|Benchmark limit|Single simulated benchmark and binary objective limit external validity|Validate on additional datasets and real plant<br>logs where available|



**Table 15** . Structured discussion summary aligned with the reported results and the proposed pipeline. 

**Scientific Reports** |        (2026) 16:17488 | https://doi.org/10.1038/s41598-026-48227-6 Content courtesy of Springer Nature, terms of use apply. Rights reserved 

23 

www.nature.com/scientificreports/ 

|**Symbol**|**Description**|**Symbol**|**Description**|**Symbol**|**Description**|
|---|---|---|---|---|---|
|_yt_|Measured vector|ˆ_yt_|Nominal prediction|_rt_|Residual vector|
|_ut_|Control input|_xt,d_|Channel value|˜_xd_|Median imputation|
|_µd_|Training mean|_σd_|Training std. dev.|_ϵ_|Stability constant|
|_ϕ_(_·_)|Descriptor operator|_et_|Descriptor vector|_zt_|Fused feature vector|
|˜_zt_|Selected features|_I_|Selected indices|_Zt_|Input window|
|˜<br>_Zt_|Selected window|_H_<sup>_c_</sup><br>_t_|Conv1D features|_ht_|BiGRU hidden state|
|_αt_|Attention weight|_c_|Context vector|ˆ_p_|Raw probability|
|_p_|Calibrated probability|_a_,_b_|Calibration parameters|_δ_|Decision threshold|
|_δ_<sup>_⋆_</sup>|Chosen threshold|ˆ_y_|Binary decision|_w_|Descriptor window|
|_L_|Sequence length|_K_|No. of descriptors|_M_|No. of selected features|
|_T_|Sequence length total|_t_0|Fault start time|_t_alarm|First alarm time|
|_d_|Detection delay|∆_t_|Sampling interval|_τ_|False-alarm budget|
|_ρX,Y_|Pearson correlation|_E_band|Band energy|RMS_t_|RMS descriptor|



**Table 16** . Variables and symbols used in the proposed framework. 

|**Acronym**|**Meaning**|**Acronym**|**Meaning**|**Acronym**|**Meaning**|
|---|---|---|---|---|---|
|TEP|Tennessee Eastman Process|CRNN|Convolutional Recurrent Neural Network|CNN|Convolutional Neural Network|
|Conv1D|One-dimensional convolution|BiGRU|Bidirectional gated recurrent unit|GRU|Gated recurrent unit|
|LSTM|Long short-term memory|SHAP|SHapley Additive exPlanations|LightGBM|Light Gradient Boosting Machine|
|ECE|Expected calibration error|ROC|Receiver operating characteristic|AUC|Area under the curve|
|AUC-ROC|Area under ROC curve|PR|Precision-recall|AUC-PR|Area under PR curve|
|F1|F1-score|NAB|Numenta Anomaly Benchmark|BCa|Bias-corrected and accelerated|
|FAR/h|False alarm rate per hour|RBF|Radial basis function|SVM|Support vector machine|
|RF|Random forest|LR|Logistic regression|IDV|Input disturbance variable|
|IoT|Internet of Tings|NLL|Negative log-likelihood|MCE|Maximum calibration error|



**Table 17** . Acronyms and abbreviations used in the manuscript. 

residual-guided learning combined with calibrated probabilities can transform a high-performing detector into a policy-driven monitoring tool that is easier to justify, tune and hand off in Industry 4.0 environments. 

### **Future work** 

Future research can extend this work in several directions. Physics-based models can be expanded to incorporate multiple data sources, such as sound, vibration, images and control logs, so that complementary evidence can improve detection under more complex fault conditions. Federated learning and continual learning are also promising directions for cross-plant deployment and long-term adaptation. Federated learning enables model development without sharing raw plant data, while continual learning can help the system adapt to process drift, wear and evolving operating conditions. 

Another important direction is the design of lightweight CRNN variants for on-device deployment. Modelcompression techniques such as pruning, quantization and knowledge distillation can make real-time detection feasible on low-power industrial edge devices. Together, these directions can support the development of a reliable, efficient and more generalizable CRNN-based monitoring system for modern smart-factory environments. Future work will also extend the present binary anomaly detector toward multiclass fault diagnosis so that the framework can not only detect abnormal operation but also identify the specific fault type. 

## **Nomenclature** 

### **Variables and symbols** 

### **Acronyms and abbreviations** 

## **Data availability** 

The Tennessee Eastman Process (TEP) dataset used in this study is publicly available and can be accessed through established industrial benchmark repositories or via the references cited in the manuscript. It is also available from Kaggle. 

**Scientific Reports** |        (2026) 16:17488 | https://doi.org/10.1038/s41598-026-48227-6 Content courtesy of Springer Nature, terms of use apply. Rights reserved 

24 

www.nature.com/scientificreports/ 

## **Code availability** 

## **The code used to reproduce the experiments, result-generation pipeline and analysis presented in this study is publicly available at GitHub repository. The repository includes the main notebook, supporting result folders and implementation files required for the proposed Tennessee Eastman Process faultdetection framework.** 

Received: 6 February 2026; Accepted: 7 April 2026 


![](Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs_images/Early-warning_industrial_fault_detection_based_on_physics-guided_residual_learning_and_calibrated_CRNNs.pdf-0025-04.png)


## **References** 

1. Farahani, M. A. et al. Time-series pattern recognition in smart manufacturing systems: A literature review and ontology. _J. Manuf. Syst._ **69** , 208–241. https://doi.org/10.1016/j.jmsy.2023.05.025 (2023). 

2. Mallioris, P., Aivazidou, E. & Bechtsis, D. Predictive maintenance in industry 4.0: A systematic multi-sector mapping. _CIRP J. Manuf. Sci. Technol._ **50** , 80–103. https://doi.org/10.1016/j.cirpj.2024.02.003 (2024). 

3. Dinh, D.-H., Do, P., Hoang, V.-T., Vo, N.-T. & Bang, T. Q. A predictive maintenance policy for manufacturing systems considering degradation of health monitoring device. _Reliab. Eng. Syst. Saf._ **248** , 110177. https://doi.org/10.1016/j.ress.2024.110177 (2024). 

4. Siemens, A. G. The true cost of downtime 2024: How much do leading manufacturers lose through inefficient maintenance? Senseye Predictive Maintenance report (2024) (accessed 30 Jan 2026). 

5. ABB. Abb survey reveals unplanned downtime costs usd 125,000 per hour. Press release (2023) (accessed 30 Jan 2026). 

6. MarketsandMarkets. Predictive maintenance market: Global forecast to 2029. Market report web page (2024). (accessed 30 Jan 2026). 

7. Rodríguez, M., Tobón, D. P. & Múnera, D. Anomaly classification in industrial internet of things: A review. _Intell. Syst. Appl._ **18** , 200232. https://doi.org/10.1016/j.iswa.2023.200232 (2023). 

8. Orabi, M., Tran, K. P., Egger, P. & Thomassey, S. Anomaly detection in smart manufacturing: An adaptive adversarial transformerbased model. _J. Manuf. Syst._ **77** , 591–611. https://doi.org/10.1016/j.jmsy.2024.09.021 (2024). 

9. Wadinger, M. & Kvasnica, M. Adaptable and interpretable framework for anomaly detection in scada-based industrial systems. _Expert Syst. Appl._ 123200. https://doi.org/10.1016/j.eswa.2024.123200 (2024). 

10. Guo, H., Zhou, Z., Zhao, D. & Gaaloul, W. EGNN: Energy-efficient anomaly detection for IOT multivariate time series data using graph neural network. _Futur. Gener. Comput. Syst._ **151** , 45–56. https://doi.org/10.1016/j.future.2023.09.028 (2024). 

11. Mostafavi, A. & Chaibakhsh, A. Dynamic physics-based digital twin for supervisory, condition monitoring and fault diagnosis of industrial turboshaft engines. _Digit. Twin_ . https://doi.org/10.1080/27525783.2025.2598085 (2025). 

12. Ullah, S., Siddique, M. F. & Kim, J.-M. Multi-sensor observer-based residual learning with auto-permutation feature importance for fault diagnosis of multistage centrifugal pumps under variable pressures. _Sci. Rep._ **15** , 45735.  h t t p s : / / d o i . o r g / 1 0 . 1 0 3 8 / s 4 1 5 9 8 - 0 2 5 - 3 2 7 2 6 - z (2025). 

13. Enciso-Salas, L. _et al._ A bibliometric literature review of integrated data and model based diagnosis approaches for the industry 4.0. _Int. J. Syst. Sci._ https://doi.org/10.1080/00207721.2025.2550562 (2025). 

14. Kumar, N. B., Vijay Babu, A. R., Anil Kumar, M. B., Sai Kumar, T. & Ganesh Babu, V. Hybrid digital twin-based fault diagnosis framework for PMSMs in electric vehicle applications. _Franklin Open_ **12** , 100328. https://doi.org/10.1016/j.fraope.2025.100328 (2025). 

15. Junaid, A. _et al._ Engine failure prediction on large-scale cmapss data using hybrid feature selection and imbalance-aware learning. _Comput. Mater. Contin._ **87** , https://doi.org/10.32604/cmc.2025.073189 (2026). 

16. Alzarooni, A. _et al._ Anomaly detection for industrial applications, its challenges, solutions, and future directions: A review.  h t t p s : / / d o i . o r g / 1 0 . 4 8 5 5 0 / a r X i v . 2 5 0 1 . 1 1 3 1 0 (2025). License: CC BY 4.0. arxiv:2501.11310. 

17. Miraliakbar, A., Ma, F. & Jiang, Z. Online fault detection and classification of chemical process systems leveraging statistical process control and Riemannian geometric analysis. _Comput. Chem. Eng._ **200** , 109177. https://doi.org/10.1016/j.compchemeng.2025.109177 (2025). 

18. Khan, A. _et al._ Secure and differentially private edge-cloud federated learning framework for privacy-preserving maritime ais intelligence. _Comput. Mater. Contin._ https://doi.org/10.32604/cmc.2026.077222 (2026). 

19. Siddique, M. F., Umar, M., Ahmad, W. & Kim, J.-M. Advanced fault diagnosis in milling cutting tools using vision transformers with semi-supervised learning and uncertainty quantification. _Sci. Rep._ **15** , 42460. https://doi.org/10.1038/s41598-025-26550-8 (2025). 

20. Dong, J. et al. Real-time fault detection for IIoT facilities using GA-att-LSTM based on edge-cloud collaboration. _Front. Neurorobot._ **18** , 1499703. https://doi.org/10.3389/fnbot.2024.1499703 (2024). 

21. Rožanec, J. M. et al. Active learning and novel model calibration measurements for automated visual inspection in manufacturing. _J. Intell. Manuf._ **35** , 1963–1984. https://doi.org/10.1007/s10845-023-02098-0 (2024). 

22. Diallo, A. R., Homri, L. & Dantan, J.-Y. Reducing false alarms in fault detection: A comparative analysis between conformal prediction and classical methods applied to PCA and autoencoders. _J. Process Control_ **152** , 103495.  h t t p s : / / d o i . o r g / 1 0 . 1 0 1 6 / j . j p r o c o n t . 2 0 2 5 . 1 0 3 4 9 5 (2025). 

23. Zaferani, N., Afrash, M. R. & Moulaei, K. Predicting and classifying type 2 diabetes using a transparent ensemble model combining random forest, k-nearest neighbor, and neural networks. _Sci. Rep._ **16** , https://doi.org/10.1038/s41598-025-31562-5 (2026). 

24. AlZahrani, Y. Real-time anomaly detection in IOT streams through spatiotemporal patterns. _Discover Internet Things_ h t t p s : / / d o i . o r g / 1 0 . 1 0 0 7 / s 4 3 9 2 6 - 0 2 5 - 0 0 2 5 6 - 9 (2026). 

25. Colosimo, B. M. et al. Statistical process monitoring from industry 2.0 to industry 4.0: Insights into research and practice. _Technometrics_ **66** , 507–530. https://doi.org/10.1080/00401706.2024.2327341 (2024). 

26. Melo, A., Câmara, M. M. & Pinto, J. C. Data-driven process monitoring and fault diagnosis: A comprehensive survey. _Processes_ **12** , 251. https://doi.org/10.3390/pr12020251 (2024). 

27. Zhang, J. et al. A novel explainable propagation-based fault diagnosis approach for clean-in-place by establishing Boolean network model. _J. Process Control_ **148** , 103405. https://doi.org/10.1016/j.jprocont.2025.103405 (2025). 

28. Liu, J. et al. Fault monitoring-oriented transition process identification of complex industrial processes with neighbor inconsistent pair-based attribute reduction. _J. Process Control_ **121** , 30–49. https://doi.org/10.1016/j.jprocont.2022.11.011 (2023). 

29. Jung, D. & Westny, T. Uncertainty-aware fault diagnosis of unknown faults using ensemble-based node residuals. _Mech. Syst. Signal Process._ **242** , 113599. https://doi.org/10.1016/j.ymssp.2025.113599 (2026). 

30. Zamanzadeh Darban, Z., Webb, G. I., Pan, S., Aggarwal, C. C. & Salehi, M. Deep learning for time series anomaly detection: A survey. _ACM Comput. Surv._ https://doi.org/10.1145/3691338 (2024). 

31. Haq, I. U., Khan, H. A., Husnain, G., Jan, L. & Lim, S. Enhancing manufacturing efficiency through alarm flexibility in smart systems. _IEEE Access_ **11** , 75715–75724. https://doi.org/10.1109/ACCESS.2023.3296491 (2023). 

**Scientific Reports** |        (2026) 16:17488 | https://doi.org/10.1038/s41598-026-48227-6 Content courtesy of Springer Nature, terms of use apply. Rights reserved 

25 

www.nature.com/scientificreports/ 

32. Xie, T., Xu, Q. & Jiang, C. Anomaly detection for multivariate times series through the multi-scale convolutional recurrent variational autoencoder. _Expert Syst. Appl._ **231** , 120725. https://doi.org/10.1016/j.eswa.2023.120725 (2023). 

33. Huang, X., Chen, N., Deng, Z. & Huang, S. Multivariate time series anomaly detection via dynamic graph attention network and informer. _Appl. Intell._ **54** , 7636–7658. https://doi.org/10.1007/s10489-024-05575-y (2024). 

34. Husnain, G. _et al._ Vit-xplain: A transparent deepfake detector for consumer electronics based on attention and explainable AI. _IEEE Trans. Consum. Electron._ https://doi.org/10.1109/TCE.2025.3643884 (2025). 

35. Khan, A. et al. Evaluating routing stability and coordination in swarm-based multi-agent task-oriented dialogue systems. _Sci. Rep._ **16** , 42158. https://doi.org/10.1038/s41598-026-42158-y (2026) ( **(2026). Published: 03 March** ). 

36. Wu, Y., Sicard, B. & Gadsden, S. A. Physics-informed machine learning: A comprehensive review on applications in anomaly detection and condition monitoring. _Expert Syst. Appl._ **255** , 124678. https://doi.org/10.1016/j.eswa.2024.124678 (2024). 

37. Khan, A. et al. Smart predictive maintenance: A TCN-based system for early fault detection in industrial machinery. _Machines_ **14** , 164. https://doi.org/10.3390/machines14020164 (2026). 

38. Xiao, Y., Shao, H. & Liu, Y. Evaluating calibration of deep fault diagnostic models under distribution shift. _Comput. Ind._ **171** , 104334. https://doi.org/10.1016/j.compind.2025.104334 (2025). 

39. Khan, A., Junaid, A., Husnain, G., Alzahrani, K. J. & Alkahtani, H. K. An efficient intrusion detection system using domain-aware meta-learning with adapter-based few-shot adaptation in vehicular ad-hoc networks (VANETS). _IET Intel. Transport Syst._ **20** , e70182. https://doi.org/10.1049/itr2.70182 (2026). 

40. Cacao, J., Santos, J. S. & Antunes, M. Explainable ai for industrial fault diagnosis: A systematic review. _J. Ind. Inf. Integr._ **47** , 100905. https://doi.org/10.1016/j.jii.2025.100905 (2025). 

41. Nanopoulos, A. & Buza, K. Conformal prediction for out-of-distribution time-series classification. _Appl. Intell._ **55** , 823.  h t t p s : / / d o i . o r g / 1 0 . 1 0 0 7 / s 1 0 4 8 9 - 0 2 5 - 0 6 7 0 8 - 7 (2025). 

42. Faizullin, R. & Hering, S. Cointegration analysis method for fault detection based on sensor data. In _IOP Conference Series: Materials Science and Engineering_ , vol. 971, 042075, https://doi.org/10.1088/1757-899X/971/4/042075 (IOP Publishing, 2020) ( **Licensed under CC BY 3.0** ). 

43. Asaadi, M., Aslansefat, K., Izadi, I. & Yang, F. Adaptive design of alarm systems in industrial processes. _IFAC-PapersOnLine_ **58** , 841–846. https://doi.org/10.1016/j.ifacol.2024.08.442 (2024). 

44. Mohammadzadeh, S., Prachaseree, P. & Lejeune, E. Investigating deep learning model calibration for classification problems in mechanics. _Mech. Mater._ **184** , 104749. https://doi.org/10.1016/j.mechmat.2023.104749 (2023). 

45. Lin, Y., Song, M. & van der Sluis, B. Bootstrap inference for linear time-varying coefficient models in locally stationary time series. _J. Comput. Graph. Stat._ **34** , 654–667. https://doi.org/10.1080/10618600.2024.2403705 (2025). 

46. Pe, La. & De. & Na, M. F., Perales G’omez, A. L. & Fern’andez-Maim’o, L,. Shats: a shapley-based explainability method for time series artificial intelligence models. _Future Gener. Comput. Syst._ **176** , 108178. https://doi.org/10.1016/j.future.2025.108178 (2025). 

47. Husnain, G. et al. A biologically inspired intelligent and energy efficient route optimization clustering algorithm for internet of vehicles (iov). _IET Intel. Transport Syst._ **20** , e70170. https://doi.org/10.1049/itr2.70170 (2026). 

48. Meng, H., Wagner, C. & Triguero, I. Segal time series classification—stable explanations using a generative model and an adaptive weighting method for lime. _Neural Netw._ **176** , 106345. https://doi.org/10.1016/j.neunet.2024.106345 (2024). 

49. Ortiz-Garces, I. et al. Implementation of edge ai for early fault detection in IOT networks: Evaluation of performance and scalability in complex applications. _Discover Internet Things_ https://doi.org/10.1007/s43926-025-00196-4 (2025). 

50. Frank, P. M. Fault diagnosis in dynamic systems using analytical and knowledge-based redundancy: A survey and some new results. _Automatica_ **26** , 459–474. https://doi.org/10.1016/0005-1098(90)90018-D (1990). 

51. Chen, J. & Patton, R. J. _Robust Model-Based Fault Diagnosis for Dynamic Systems_ (Springer, 1999). 

52. Gertler, J. J. _Fault Detection and Diagnosis in Engineering Systems_ (CRC Press, 1998). 

53. Isermann, R. Model-based fault-detection and diagnosis—Status and applications. _Annu. Rev. Control._ **29** , 71–85.  h t t p s : / / d o i . o r g / 1 0 . 1 0 1 6 / j . a r c o n t r o l . 2 0 0 4 . 1 2 . 0 0 2 (2005). 

54. Venkatasubramanian, V., Rengaswamy, R., Yin, K. & Kavuri, S. N. A review of process fault detection and diagnosis: Part i: Quantitative model-based methods. _Comput. Chem. Eng._ **27** , 293–311. https://doi.org/10.1016/S0098-1354(02)00160-6 (2003). 

55. Downs, J. J. & Vogel, E. F. A plant-wide industrial process control problem. _Comput. Chem. Eng._ **17** , 245–255.  h t t p s : / / d o i . o r g / 1 0 . 1 0 1 6 / 0 0 9 8 - 1 3 5 4 ( 9 3 ) 8 0 0 1 8 - I (1993). 

56. Ricker, N. L. Tennessee eastman challenge process archive (2005). Model and data archive for the Tennessee Eastman process. 

57. Shi, B., Bai, X. & Yao, C. An end-to-end trainable neural network for image-based sequence recognition and its application to scene text recognition. _IEEE Trans. Pattern Anal. Mach. Intell._ **39** , 2298–2304. https://doi.org/10.1109/TPAMI.2016.2646371 (2017). 

58. Lomov, I., Lyubimov, M., Makarov, I. & Zhukov, L. E. Fault detection in Tennessee eastman process with temporal deep learning models. _J. Ind. Inf. Integr._ **23** , 100216. https://doi.org/10.1016/j.jii.2021.100216 (2021). 

59. Agarwal, P., Tamer, M. & Budman, H. Hierarchical deep LSTM for fault detection and diagnosis for a chemical process. _Processes_ **10** , 2557. https://doi.org/10.3390/pr10122557 (2022). 

60. Huang, Y., Zhang, J., Liu, R. & Zhao, S. Improving accuracy and interpretability of CNN-based fault diagnosis through an attention mechanism. _Processes_ **11** , 3233. https://doi.org/10.3390/pr11113233 (2023). 

61. Wang, M. et al. Incipient fault detection based on dense feature ensemble net. _Neurocomputing_ **601** , 128211.  h t t p s : / / d o i . o r g / 1 0 . 1 0 1 6 / j . n e u c o m . 2 0 2 4 . 1 2 8 2 1 1 (2024). 

62. Liu, Y. & Jafarpour, B. Graph attention network with granger causality map for fault detection and root cause diagnosis. _Comput. Chem. Eng._ **180** , 108453. https://doi.org/10.1016/j.compchemeng.2023.108453 (2024). 

## **Author contributions** 

A.K. led the conceptualization of the study, designed the methodology, conducted the core experiments and analysis, and wrote the original draft of the manuscript. F.A.F. contributed to data analysis, experimental support, and manuscript review. A.J. contributed to experimental execution, data analysis, and software implementation. A.I. supported software development, data curation, and experimental validation. M.F.S. and M.S.S. contributed to validation, technical verification, and critical review of the results. J.U. provided additional support in data analysis, result interpretation, and manuscript refinement. H.A.K. contributed to funding acquisition, methodological guidance, validation, and critical review of the manuscript. G.H. supervised the study, coordinated project management, and led the critical review and editing process. All authors reviewed and approved the final manuscript. 

## **Funding** 

This research was funded by Multimedia University, Cyberjaya, Selangor, Malaysia [Grant Number: PostDoc(MMUI/240029)]. 

**Scientific Reports** |        (2026) 16:17488 | https://doi.org/10.1038/s41598-026-48227-6 Content courtesy of Springer Nature, terms of use apply. Rights reserved 

26 

www.nature.com/scientificreports/ 

## **Declarations** 

## **Ethics statement** 

This study uses the publicly available _Tennessee Eastman Process (TEP)_ dataset<sup>55,56</sup> , which is a well-established industrial benchmark for process monitoring and fault diagnosis. The data are fully simulated and do not involve any human participants, personal data or animal experiments. Therefore, no ethical approval was required. 

## **Competing interests** 

The authors declare no competing interests. 

## **Additional information** 

**Correspondence** and requests for materials should be addressed to H.A.K. or G.H. 

**Reprints and permissions information** is available at www.nature.com/reprints. 

**Publisher’s note** Springer Nature remains neutral with regard to jurisdictional claims in published maps and institutional affiliations. 

**Open Access** This article is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License, which permits any non-commercial use, sharing, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons licence, and indicate if you modified the licensed material. You do not have permission under this licence to share adapted material derived from this article or parts of it. The images or other third party material in this article are included in the article’s Creative Commons licence, unless indicated otherwise in a credit line to the material. If material is not included in the article’s Creative Commons licence and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder. To view a copy of this licence, visit  h t t p : / / c r e a t i v e c o m m o n s . o r g / l i c e n s e s / b y - n c - n d / 4 . 0 / . 

© The Author(s) 2026 

**Scientific Reports** |        (2026) 16:17488 | https://doi.org/10.1038/s41598-026-48227-6 Content courtesy of Springer Nature, terms of use apply. Rights reserved 

27 

## Terms and Conditions 

Springer Nature journal content, brought to you courtesy of Springer Nature Customer Service Center GmbH ("Springer Nature"). 

Springer Nature supports a reasonable amount of sharing of research papers by authors, subscribers and authorised users ("Users"), for small-scale personal, non-commercial use provided that all copyright, trade and service marks and other proprietary notices are maintained. By accessing, sharing, receiving or otherwise using the Springer Nature journal content you agree to these terms of use ("Terms"). For these purposes, Springer Nature considers academic use (by researchers and students) to be non-commercial. 

These Terms are supplementary and will apply in addition to any applicable website terms and conditions, a relevant site licence or a personal subscription. These Terms will prevail over any conflict or ambiguity with regards to the relevant terms, a site licence or a personal subscription (to the extent of the conflict or ambiguity only). For Creative Commons-licensed articles, the terms of the Creative Commons license used will apply. 

We collect and use personal data to provide access to the Springer Nature journal content. We may also use these personal data internally within ResearchGate and Springer Nature and as agreed share it, in an anonymised way, for purposes of tracking, analysis and reporting. We will not otherwise disclose your personal data outside the ResearchGate or the Springer Nature group of companies unless we have your permission as detailed in the Privacy Policy. 

While Users may use the Springer Nature journal content for small scale, personal non-commercial use, it is important to note that Users may not: 

1. use such content for the purpose of providing other users with access on a regular or large scale basis or as a means to circumvent access control; 

2. use such content where to do so would be considered a criminal or statutory offence in any jurisdiction, or gives rise to civil liability, or is otherwise unlawful; 

3. falsely or misleadingly imply or suggest endorsement, approval , sponsorship, or association unless explicitly agreed to by Springer Nature in writing; 

4. use bots or other automated methods to access the content or redirect messages 

5. override any security feature or exclusionary protocol; or 

6. share the content in order to create substitute for Springer Nature products or services or a systematic database of Springer Nature journal 

- content. 

In line with the restriction against commercial use, Springer Nature does not permit the creation of a product or service that creates revenue, royalties, rent or income from our content or its inclusion as part of a paid for service or for other commercial gain. Springer Nature journal content cannot be used for inter-library loans and librarians may not upload Springer Nature journal content on a large scale into their, or any other, institutional repository. 

These terms of use are reviewed regularly and may be amended at any time. Springer Nature is not obligated to publish any information or content on this website and may remove it or features or functionality at our sole discretion, at any time with or without notice. Springer Nature may revoke this licence to you at any time and remove access to any copies of the Springer Nature journal content which have been saved. 

To the fullest extent permitted by law, Springer Nature makes no warranties, representations or guarantees to Users, either express or implied with respect to the Springer nature journal content and all parties disclaim and waive any implied warranties or warranties imposed by law, including merchantability or fitness for any particular purpose. 

Please note that these rights do not automatically extend to content, data or other material published by Springer Nature that may be licensed from third parties. 

If you would like to use or distribute our Springer Nature journal content to a wider audience or on a regular basis or in any other manner not expressly permitted by these Terms, please contact Springer Nature at 

<u>onlineservice@springernature.com</u> 

