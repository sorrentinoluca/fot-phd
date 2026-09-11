Published as a conference paper at ICLR 2026 

# ADAPTIVE CONFORMAL ANOMALY DETECTION WITH TIME SERIES FOUNDATION MODELS FOR SIGNAL MONITORING 

**Natalia Martinez Gil Fearghal O’Donncha Wesley M. Gifford Nianjun Zhou Dhaval C. Patel Roman Vaculin** 

IBM Research 

natalia.martinez.gil@ibm.com 

## ABSTRACT 

We propose a post-hoc adaptive conformal anomaly detection method for monitoring time series that leverages predictions from pre-trained foundation models without requiring additional fine-tuning. Our method yields an interpretable anomaly score directly interpretable as a false alarm rate (p-value), facilitating transparent and actionable decision-making. It employs weighted quantile conformal prediction bounds and adaptively learns optimal weighting parameters from past predictions, enabling calibration under distribution shifts and stable false alarm control, while preserving out-of-sample guarantees. As a model-agnostic solution, it integrates seamlessly with foundation models and supports rapid deployment in resource-constrained environments. This approach addresses key industrial challenges such as limited data availability, lack of training expertise, and the need for immediate inference, while taking advantage of the growing accessibility of time series foundation models. Experiments on both synthetic and real-world datasets show that the proposed approach delivers strong performance, combining simplicity, interpretability, robustness, and adaptivity.<sup>1</sup> 

## 1 INTRODUCTION 

A common challenge in industrial applications such as predictive maintenance and signal monitoring is the scarcity of sufficient quality data and infrastructure to train robust models Cook et al. (2019); Ajami & Daneshvar (2012); Kanawaday & Sane (2017); Beghi et al. (2016); Shah & Tiwari (2018); Moghaddass & Wang (2017). This limitation can hinder the ability to make accurate and reliable predictions, which are essential to detect anomalies and ensure operational efficiency. Foundation models, particularly in the time series domain Liang et al. (2024), offer a promising solution. These models excel at leveraging prior knowledge and historical observations, enabling them to provide good enough initial estimates of expected values and statistical characteristics of monitored signals, even in data-scarce environments. This capability is invaluable for industries aiming to enhance their monitoring systems without the need for extensive datasets. 

In the context of time series anomaly detection, an adaptive approach is crucial for monitoring and maintaining the reliability of signals. Anomalies, or deviations from expected behavior, can manifest in different forms, such as point anomalies, where an individual observation significantly deviates from normal patterns, and contextual anomalies, where a value is only considered anomalous within a specific temporal context Boniol et al. (2024). Detecting these effectively requires models that capture underlying temporal dependencies and adapt to non-stationary data distributions. 

A prominent class of anomaly detection methods relies on predictive modeling, where a forecasting model learns normal time series behavior, and deviations between predicted and actual values could indicate anomalies in operations or shifts in operational modes that require expert attention Basseville (1993); Choudhary et al. (2017); Gama et al. (2014); Saurav et al. (2018). However, many existing approaches assume access to large amounts of training data, making them impractical in settings where only a few samples are initially available. This motivates the use of pretrained 

> 1Code: https://github.com/ibm-granite/granite-tsfm/tree/main/notebooks/ hfdemo/adaptive_conformal_tsad 

1 

Published as a conference paper at ICLR 2026 

Time Series Foundation Models (TSFMs) Rasul et al. (2023; 2024); Ansari et al. (2024); Liang et al. (2024), which have been trained on large-scale datasets and can generalize to new time series with minimal adaptation. Furthermore, existing anomaly detection systems often lack interpretability, relying on thresholding mechanisms that assume a fixed data distribution Schmidl et al. (2022); Paparrizos et al. (2022b); Goswami et al. (2022), which limits their adaptability to evolving time series data. In this setting, a robust system must balance sensitivity and adaptability, minimizing false alarms while effectively detecting significant behavioral transitions. This ensures timely identification of suspicious patterns without overwhelming experts with noise, fostering a more efficient and reliable monitoring framework Cook et al. (2019). 

To address these limitations, we propose a conformal-based anomaly detection method that integrates the predictions of pretrained TSFMs with conformal prediction techniques Vovk et al. (2005); Angelopoulos & Bates (2021) to produce an interpretable, adaptive anomaly score directly linked to a desired alarm rate. Conformal methods offer model-agnostic and distribution-free uncertainty quantification with finite-sample guarantees, making them highly suitable for real-world anomaly detection. However, standard conformal approaches rely on the assumption of exchangeability, which is often violated in time series due to temporal dependencies. Furthermore, existing conformal methods for anomaly detection primarily focus on thresholding arbitrary anomaly scores derived from non-anomalous data while assuming exchangeability Angelopoulos & Bates (2021); Guan (2019); Bates et al. (2023), limiting their applicability in dynamic, non-stationary settings. 

**Main Contributions** We propose _W_ 1-ACAS, a post-hoc adaptive conformal anomaly detection framework that leverages predictions from pretrained forecasters (e.g., TSFMs) to monitor signals without requiring fine-tuning. This is particularly valuable in industrial settings, where users often lack sufficient data, data-cleaning pipelines, or specialized expertise Cook et al. (2019). Our approach provides a practical solution for immediate anomaly monitoring. Figure 1 illustrates the method: (a) anomaly scores are derived as conformal _p_ -values from forecaster errors across multiple horizons and aggregated into a single score; (b) anomalies are flagged when adaptive _p_ -values fall below a threshold on real signals; and (c) the learned adaptive weights emphasize past errors with similar distributions, capturing recurring patterns such as periodicity, thereby improving detection while offering direct control over the alarm rate. Our framework offers the following properties: 

- **Interpretability:** The anomaly score corresponds directly to an alarm rate ( _p_ -value), providing a transparent and probabilistic basis for decisions. 

- **Distribution-Agnostic:** Built on quantile conformal prediction, the method is robust to heavy-tailed and complex error distributions. 

- **Adaptivity:** By weighting past nonconformity scores via the Wasserstein distance, the framework adapts online to distribution shifts, reducing false alarms while preserving calibration Barber et al. (2023). 

- **Post-Hoc and Model-Agnostic:** The method applies directly to pretrained TSFMs or any anomaly score, requiring no retraining while inheriting the guarantees of weighted conformal prediction. Its effectiveness is proved through integration with TSFM forecasters. 

## 2 RELATED WORK 

**Time Series Anomaly Detection** Prediction-based methods detect anomalies by comparing observed values against forecasts (Giannoni et al., 2018; Boniol et al., 2024). Recent TSFMs (Rasul et al., 2023; 2024; Ansari et al., 2024; Liang et al., 2024) are well suited for online detection in datascarce scenarios, offering accurate zero-shot forecasting performance. Recent benchmark studies (Paparrizos et al., 2022b; Liu & Paparrizos, 2024) show that classical distance- and density-based methods (Li et al., 2007; Ramaswamy et al., 2000; Aggarwal & Aggarwal, 2017; Paparrizos & Gravano, 2015; 2017; Boniol et al., 2021) often outperform more complex models, but they typically require access to the full dataset (non-causal), lack robustness across temporal patterns, and are unsuitable for streaming settings. Moreover, many anomaly scores lack clear probabilistic meaning, and common thresholding strategies rely on full-dataset statistics (Ahmad et al., 2017), limiting realtime applicability. In practice, anomaly detection systems must not only achieve high accuracy but also provide interpretable confidence scores while maintaining low false alarm rates (Cook et al., 2019). Our work addresses these challenges by combining TSFMs with adaptive conformal scoring, yielding interpretable and calibrated thresholds for reliable streaming anomaly detection. 

2 

Published as a conference paper at ICLR 2026 


![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0003-01.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0003-02.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0003-03.png)


Figure 1: Illustration of our proposed _W_ 1-ACAS method. (a) Anomaly scoring pipeline: conformal _p_ -values are computed across forecast horizons from forecaster errors and aggregated. The mapping is adapted online by weighting past nonconformity scores, with weights evolving to capture distributional shifts or recurring patterns. (b) Example signal (blue) with ground-truth anomaly labels, where detected outliers (red dots) occur when adaptive _p_ -values (orange) fall below a threshold. (c) Converged adaptive weights (orange) over past errors (blue), averaged across horizons, shows how _W_ 1-ACAS captures error patterns with similar distributions, here reflecting its periodic behavior. 

**Conformal Prediction.** Conformal prediction provides distribution-free uncertainty quantification with finite-sample guarantees (Vovk et al., 2005; Shafer & Vovk, 2008; Angelopoulos & Bates, 2021). A widely used variant, split conformal prediction (SCP) (Papadopoulos et al., 2002), is post-hoc and model-agnostic, relying only on model predictions and a calibration set. While effective under exchangeability<sup>2</sup> , this assumption is often violated in time series settings, motivating adaptive extensions. Recent works (Gibbs & Candes, 2021; Zaffran et al., 2022; Gibbs & Cand`es, 2024) adjust conformal quantiles online to handle distribution shifts, but typically optimize for a single error rate. Weighted conformal methods offer adaptation by reweighting calibration or past scores based on some notion of similarity to new observations (Lei & Wasserman, 2014; Guan, 2019; Tibshirani et al., 2019; Sesia & Romano, 2021; Han et al., 2022; Guan, 2023; Ghosh et al., 2023; Mao et al., 2024) improving local coverage. Bounds for non-exchangeable sequences (Barber et al., 2023) further suggest emphasizing calibration samples that are nearly exchangeable with the test point. This motivates our approach, which leverages weighted adaptive conformal quantiles to remain calibrated across time. Conformal prediction has also been applied to anomaly detection by thresholding arbitrary anomaly scores under exchangeability (Angelopoulos & Bates, 2021; Guan, 2019; Bates et al., 2023). However, existing methods do not simultaneously provide interpretable, distribution-agnostic anomaly scores, directly control alarm rates, and adapt robustly to non-exchangeable time series. Our work addresses this gap by developing a conformal anomaly detection framework that is both interpretable and resilient to real-world distribution shifts. 

> 2informally, a sequence of observations is exchangeable if any permutation of the observations has the same joint probability 

3 

Published as a conference paper at ICLR 2026 

## 3 BACKGROUND 

Consider _S ∈_ R a nonconformity score variable that quantifies the performance of a predictive model _h_ : _X → Y_<sup>ˆ</sup> on a joint distribution _PX,Y_ using a nonconformity function _e_ : _Y × Y_<sup>ˆ</sup> _→_ R. The input _Y_ ˆ corresponds to the output space of the model, which may include predictions or derived statistics _X ∈X_ represents the model’s input space, _Y ∈Y_ denotes the true target variable, and over _Y_ . The nonconformity function _e_ measures the degree of disagreement between the true target and the model’s predictions, enabling _S_ = _e_ ( _Y, h_ ( _X_ )) to capture how atypical a prediction is within the given distribution. An example of a nonconformity function for a point prediction model is absolute error _e_ ( _Y, Y_<sup>ˆ</sup> ) = _|Y − Y_<sup>ˆ</sup> _|_ . 

### 3.1 CONFORMAL OUTLIER DETECTION. 

In the context of anomaly detection we characterize the distribution of the non-conformity score variable _S ∼ PS_ where _S_ = _e_ ( _Y, h_ ( _X_ )) _∈_ R under non-anomalous conditions _X, Y ∼ PX,Y_ . 3 Observations are flagged as outliers (or anomalies) when the composition of the nonconformity function _e_ and the predictive model _h_ produces unusually high scores.<sup>4</sup> Given a significance level _α_ , which controls the tolerated false positive rate, an anomaly detection function _Cα_ : _X , Y →{_ 0 _,_ 1 _}_ should satisfy the following property: 

P( _Cα_ ( _Xn_ +1 _, Yn_ +1) = 1) _≤ α_ (1) 

where P is the probability over unseen test data sampled from the non-anomalous distribution, _Xn_ +1 _, Yn_ +1 _∼ PX,Y_ . In the standard split-conformal setting, we observe **s** = _S_ 1 _, . . . , Sn_ nonconformity scores derived from non-anomalous data, _Si_ = _e_ ( _Yi, h_ ( _Xi_ )) with _Xi, Yi ∼ PX,Y_ . Non-conformity scores need not be independent of each other; the following conformal anomaly detection function satisfies, under echangeability conditions<sup>5</sup> , the false positive bound in equation 1: 

_Cα_ ( _Xn_ +1 _, Yn_ +1) = **1** [ _Sn_ +1 _> q_ ˆ _α_ ] _, q_ ˆ _α_ = _Q_ 1 _−α_ (<sup>�</sup><sup>_n_</sup> _i_ =1 _n_ +11<sup>_δSi_+</sup> _n_ +11<sup>_δ∞_)</sup><sup>_._</sup> (2) Here _q_ ˆ _α_ is the empirical conformal quantile, conservatively adjusted with a point mass at infinity. 

**Conformal Outlier Detection Beyond Exchangeability** To account for heterogeneity in the nonconformityweighted conformal quantile estimatescores across the input space _q_ ˆ _α_<sup>_w_=</sup> or<sup>Q</sup> potential<sup>1</sup><sup>_−α_(</sup><sup>**s**</sup><sup>_,_</sup><sup>**w**</sup> temporal<sup>) defined as:</sup> drift, we consider the generalized 


![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0004-09.png)


where **w** = _{wi ∈_ [0 _,_ 1] _}_<sup>_n_</sup> _i_ =1<sup>is a weighting vector applied to the calibration points.The standard</sup> result in Eq. 2 is recovered when _wi_ = 1 _, ∀i_ = 1 _, . . . , n_ . 

This weighted conformal quantile estimate produces a generalization of the conformal anomaly detector from equation 2. This conformal anomaly detection has false alarm rate guarantees even in non-exchangeable settings as described in the following proposition 3.1. 

**Proposition 3.1.** _(Direct application of Theorem 2 and 3 in Barber et al. (2023) Given α ∈_ (0 _,_ 1) _,_ **s** = _{Si}_<sup>_n_</sup> _i_ =1<sup>+1</sup><sup>_a set of non-conformity scores where Sn_+1</sup><sup>_corresponds to the test point, and a vector_</sup> _of weights_ **w** = _{wi ∈_ [0 _,_ 1] _}_<sup>_n_</sup> _i_ =1<sup>_for the previous n observations the detector_</sup> 


![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0004-13.png)


_based on the weighted conformal quantile estimate in Eq.3 satisfies the false alarm rate guarantees_ 


![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0004-15.png)


_Here dT V_ ( **_s_** _,_ **_s_**<sup>_i_</sup> ) _is the distance in total variation between the sequence_ **_s_** _(n previously observed point and the test point n_ + 1 _) and_ **_s_**<sup>_i_</sup> _which denotes the sequence of non-conformity scores after swapping the test point n_ + 1 _with the i-th previously observation. The lower bound is valid under the assumption that the non-conformity scores take equal values with probability 0._ 

> 3Although _X_ and _Y_ are treated as separate spaces, they may overlap, as in reconstruction-error-based scores where _Y_ = _X_ . 

> 4Unusually low scores can be handled similarly, nonconformity scores need not be positive 

> 5The sequence _S_ 1 _, . . . , Sn_ +1 is exchangeable if _P_ ( _S_ 1 _, . . . , Sn_ +1) = _P_ ( _Sσ_ (1) _, . . . , Sσ_ ( _n_ +1)) for any permutation _σ_ 

4 

Published as a conference paper at ICLR 2026 

Intuitively, Proposition 3.1 indicates that one would like to assign higher weights to previous observations that are, pairwise, most exchangeable with the test sample (i.e., _P_ ( _S_ 1 _, . . . , Si, . . . , Sn_ +1) _≃ P_ ( _S_ 1 _, . . . , Sn_ +1 _, . . . , Si_ ), and lower weights otherwise. Additionally, the lower bound encourages the maximization of _||_ **w** _||_ 1 and therefore keeping the weights as close to one as possible. One could decide **w** if given access to prior knowledge about the values or reasonable upper bounds of _dT V_ ( **s** _,_ **s**<sup>_i_</sup> ). In the context of time series, previous works such as Barber et al. (2023) have set **w** to exponentially decay with time ( _wi_ = _γ_<sup>_n−i_</sup> ); in non-time-series settings, other works such as (Lei & Wasserman, 2014; Guan, 2019; Sesia & Romano, 2021; Han et al., 2022; Guan, 2023; Ghosh et al., 2023; Mao et al., 2024) decide the weights based on criteria such as distance in covariate space, or optimize them to guarantee a particular false positive rate coverage _α_ , (Han et al., 2022; Amoukou & Brunel, 2023). Next, we present our adaptive conformal score method, which learns **w** with the objective of providing scores that are calibrated for every feasible false alarm across time. 

## 4 ADAPTIVE CONFORMAL ANOMALY SCORE 

The conformal outlier detection framework provides a principled way to define a binary anomaly decision variable based on a preselected _α_ with generalization guarantees. However, the underlying nonconformity score _S_ may not itself be an interpretable indicator of anomaly, particularly in sequential settings where its distribution may drift over time. To address this, we aim to learn an adaptive mapping that assigns each score an approximate probability of observing a more extreme value under prior (ideally normal) conditions, yielding a distribution-agnostic _p_ -value estimate. Formally, we consider a time series setting with a sequence of nonconformity scores _S_ 1 _, . . . , St_ . In predictionbased anomaly detection, these are derived from a forecasting model _h_ : R<sup>_nc×nf_</sup> _→Y_<sup>_d_</sup> , which maps a context of length _nc_ with _nf_ features to a _d_ -step-ahead forecast _Y_<sup>ˆ</sup> _t_<sup>_d_</sup> +1<sup>=</sup><sup>_hd_(</sup><sup>_Xt−n_</sup> _c_<sup>_−d_:</sup><sup>_t−d_+1).The</sup> nonconformity score for sample _t_ + 1 at horizon _d_ is _St_<sup>_d_</sup> +1<sup>=</sup><sup>_|Yt_+1</sup><sup>_−Y_ˆ</sup> _t_<sup>_d_</sup> +1<sup>_|_.For clarity, we omit the</sup> index _d_ in the following section, since the analysis applies independently to each prediction horizon, and reintroduce it later when needed. 

### 4.1 CONFORMAL ANOMALY SCORE 

We wish to learn a parametric mapping _β_ **w** : R _,_ R<sup>_t_</sup> _→_ [0 _,_ 1] of the previous nonconformity scores **s** = _{Si}_<sup>_t_</sup> _i_ =1<sup>and the test sample</sup><sup>_St_+1; this mapping</sup><sup>_β_</sup><sup>**w**should be such that it can be directly com-</sup> pared to any _α_ threshold to produce an anomaly detector with the same false alarm rate guarantees as the one described in equations equation 1 and equation 2. Given a set of non-conformity scores derived from past, ideally non-anomalous data<sup>6</sup> , their associated weights _⃗w_ = _{wi ∈_ [0 _,_ 1] _}_<sup>_t_</sup> _i_ =1<sup>,</sup> and a non-conformity score test sample _St_ +1 we propose the following score normalization _β_ **w** ( _St_ +1) = sup _{α ∈_ [0 _,_ 1] : _St_ +1 _≤_ Q1 _−α_ ( **s** _,_ **w** ) _}._ (6) Here _β_ **w** ( _St_ +1) can be interpreted as the weighted, conformalized p-value, _β_ **w** ( _St_ +1) = _βt_ +1 (we omit the explicit dependence on **s** for clarity). The proposed function automatically maps an anomaly score _S_ , which can take arbitrary real values, into a normalized score that directly relates to the desired false alarm rate. The decision of an anomaly detection threshold becomes interpretable for the end user (it directly translates into the desired false alarm level) and preserves the guarantees of the original conformal outlier detector as shown in Proposition 4.1. 

**Proposition 4.1.** _Given α ∈_ [0 _,_ 1] _, {Si}_<sup>_t_</sup> _i_ =1<sup>+1</sup><sup>_a set of exchangeable non-conformity scores, and their_</sup> _weights_ **_w_** = _{wi_ = _∈_ [0 _,_ 1] _}_<sup>_t_</sup> _i_ =1<sup>_thedetectorCβ_</sup> **_w_**<sup>(</sup><sup>_Xt_+1</sup><sup>_, Yt_+1)=</sup><sup>**1**[</sup><sup>_β_</sup><sup>**_w_**(</sup><sup>_St_+1)</sup><sup>_<α_]</sup><sup>_basedonthe_</sup> _β_ **_w_** ( _·_ ) _mapping defined in equation 6 is equivalent to equation 4 and therefore satisfies the conformal false alarm rate guarantees presented in equation 5 in Proposition 3.1 . Proof in Appendix B._ 

### 4.2 ADAPTIVE WEIGHTED ANOMALY SCORES UNDER NON-EXCHANGEABILITY 

Our proposed conformal anomaly score mapping _β_ **w** ( _·_ ) in equation 6 depends on the weights **w** assigned to the previously observed scores. Therefore, given a new observation _St_ +1 the mapping can be directly expressed as a function of **w** , _β_ **w** ( _St_ +1) = _βt_ +1( **w** ) such that 


![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0005-09.png)


> 6 _′_ For sequences containing a known fraction of anomalous samples below some upper bound _α_ , the derivation follows similarly, but the interpretation of _β_ **w** ( _St_ +1) is _α_ + _α_<sup>_′_</sup> where _α_ is the lower bound of the p-value of the sample. 

5 

Published as a conference paper at ICLR 2026 

Where _π_ : [ _n_ ] _→_ [ _n_ ] represents a sorted mapping of the previous _n_ nonconformity scores such that _π_ ( _i_ ) = _k ∈_ [ _n_ ] _, ∀i ∈_ [ _n_ ] where _π_ ( _i_ ) _< π_ ( _j_ ) if _Si ≤ Sj, ∀i_ = _j_ . _π_<sup>_−_1</sup> ( _k_ ) is the inverse sorting operation, mapping _k_ to the index of the observation corresponding to the _k_ largest value. 

We want our proposed conformal score to be well calibrated across time, meaning P( _β_ **w** ( _St_ +1) _≤ α_ ) _≈ α_ , for all _α ∈_ [0 _,_ 1] and _t_ . In lieu of that, we require _β_ **w** ( _St_ +1) to be a conservative estimate such that P( _β_ **w** ( _St_ +1) _≤ α_ ) _≤ α_ . Such calibration ensures that the conformalized scores adapts effectively to distributional shifts over time. The ideal condition under non-anomalous distributions for _St_ +1, P( _β_ **w** ( _St_ +1) _≤ α_ ) = _α, ∀α ∈_ [0 _,_ 1] is achieved when _β_ **w** ( _St_ +1) _∼ U_ [0 _,_ 1]. We also note that _β_ **w** ( _St_ +1) cannot produce non-trivial quantile estimates below its effective sample size _αc_ = _|_ **w** _|_ <u>1+1</u><sup>.</sup> We therefore seek to learn a set of feasible weights **w** satisfying these conditions by minimizing the 1-Wasserstein distance ( _W_ 1) between the cumulative density function (CDF) of the proposed score variable _Fβt_ +1( **w** ), where _βt_ +1( **w** ) = _β_ **w** ( _St_ +1) as in equation 7, and the CDF of the uniform distribution _FU_ , subject to an effective sample size constraint determined by our critical false alarm rate _αc_ . Namely 


![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0006-03.png)


Here _αc_ is the user-defined critical false alarm rate. From the dual definition of _W_ 1 we have 


![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0006-05.png)


which indicates that minimizing _W_ 1( _Fβt_ +1( **w** ) _, FU_ ) is equivalent to minimizing the calibration gap _|_ P( _βt_ +1( **w** ) _≤ α_ ) _− α|_ uniformly across all false alarm rates. We next approximate the objective in equation 8 using finite samples and give the corresponding algorithm. 

## 5 OPTIMIZATION 

In practice, we need to approximate _Fβt_ +1( **w** )( _α_ ) in equation 8 with a finite number of samples _nb_ , which results in the following empirical CDF based on the scores _{βt_ + _j}_<sup>_n_</sup> _j_ =1<sup>_b_</sup> 


![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0006-09.png)


Then, the _W_ 1 objective in equation 8 can be empirically approximated as follows 


![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0006-11.png)


where _π_ ˆ is the sort mapping of _{βt_ + _j_ ( **w** ) _}_<sup>_n_</sup> _j_ =1<sup>_b_scoressuchthat</sup><sup>_βt_+ˆ</sup><sup>_π−_1(</sup><sup>_k_)(</sup><sup>**w**)</sup><sup>_≤βt_+ˆ</sup><sup>_π−_1(</sup><sup>_k_+1)(</sup><sup>**w**).</sup> Note that the expression in equation 11 is a sum of integrals of piecewise linear functions. Therefore, it is differentiable w.r.t. to each _βt_ + _j_ ( **w** ), and consequenlty w.r.t. to each **w** (see equation 4) and also computable in closed form. Then the weights can be updated using projected gradient descent 


![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0006-13.png)


Note that here **w** _t_ denotes our current estimate of the entire weighting vector **w** at time _t_ . The partial derivatives can be expressed in closed form as 


![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0006-15.png)


and 


![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0006-17.png)


6 

Published as a conference paper at ICLR 2026 

The derivatives themselves have a simple interpretation. The derivative of _∂β_<sup>_<u>∂W</u>_</sup> _t_ +<sup><u>1</u></sup> _i_<sup>pushes a normalized</sup> score _βt_ + _i_ to lie within the ranges of its empirical quantile bucket [<sup>_π_ˆ(</sup> _n_<sup>_i_</sup><sup><u>)</u></sup> _b_<sup>_−_1</sup> _,_<sup>_π_ˆ</sup> _n_<sup><u>(</u></sup> _b_<sup>_i_</sup><sup><u>)</u>], and is minimized</sup> when _βt_ + _i_ =<sup>2 ˆ</sup><sup>_π_</sup> 2<sup><u>(</u></sup> _n_<sup>_i_</sup><sup><u>)</u></sup> _b_<sup>_−_1</sup> . The derivative<sup>_∂β_</sup> _∂w_<sup>_t_</sup><sup><u>+</u></sup><sup>_i_</sup> _k_<sup><u>(</u></sup><sup>**w**</sup><sup><u>)</u></sup> establishes that one can increase _βt_ + _i_ by decreasing the weight of scores higher than the currently-observed score _St_ +1 or by globally decreasing the overall sample size _||_ **w** _||_ 1. 

**Algorithm 1** 1-Wasserstein Adaptive Conformal Anomaly Score 

**Require:** _{St}_<sup>_T_</sup> _t_ =1<sup>:Scores,</sup><sup>_αc_:min false alarm rate,</sup><sup>_n_max past samples,</sup><sup>_nb_min batch size</sup> **Output:** : **_β_** _∈_ [0 _,_ 1]<sup>_T −nc_</sup> normalized score vector _nc_ = _α_ <u>1</u> _c_<sup>_−_1,</sup><sup>**w**=</sup><sup>_{wi_=</sup><sup>**1**[</sup><sup>_i ≤nc_]</sup><sup>_}n_</sup> _i_ =1<sup>.# Compute critical samples and init weights</sup> **J** **_β_** ( **w** ) _←{_ 0 _}_<sup>_nb×n_</sup> , _ib_ = 0, **_β_** _←{}_ # Initialize score Jacobian, batch counter and output **for** _t_ = _nc_ : _T − nc_ **do s** = _{Si}_<sup>_t_</sup> _i_ =max( _t−n,_ 1)<sup>,</sup><sup>**w**ˆ=</sup><sup>_{_ˆ</sup><sup>_wi_=</sup><sup>_w|_</sup><sup>**s**</sup><sup>_|_+1</sup><sup>_−i}|_</sup> _i_<sup>**s**</sup> =1<sup>_|_# Get past scores and corresponding weights</sup> _π ←_ ARGSORT( **s** ) # sort past scores in ascending order _jt_ +1 =<sup>�</sup> _s∈_ **s**<sup>**1**[</sup><sup>_St_+1</sup><sup>_< s_] ,</sup><sup>_βt_+1=</sup> <u>�</u> _|k_ **s** = _| jt||_ <u>+</u> **w** ˆ1 _||w_<sup>ˆ</sup> 1 _π_ +1 _−_ 1( _k_ )+1 # Compute p-value score for _St_ +1 **_β_** _←_ **_β_** _∪ βt_ +1, _ib ← ib_ + 1 **J** **_β_** ( **w** ) _ib,n−k_ = _{_<sup>_∂_</sup> _∂_<sup>_<u>β</u>_</sup> _w_<sup>_t_</sup> ˆ<sup><u>+</u></sup> _k_<sup>1</sup><sup>_}_for</sup><sup>_k_= 1</sup><sup>_, ..., |s|_, using equation 14 # Compute partial derivatives</sup> **if** _ib_ = _nb_ **then** ˆ _π ←_ ARGSORT( **_β_** _t_ +1 _−nb_ : _t_ +1) #Sort last _nb_ normalized scores and compute gradient Compute _{ ∂β_<sup>_<u>∂W</u>_</sup> _t_ +<sup><u>1</u></sup> _i_<sup>_}_</sup> _i_<sup>_n_</sup> =1<sup>_b_using</sup><sup>_π_ˆ, equation 13,</sup><sup>_∇W_1(</sup><sup>**w**) =</sup><sup>_{_�</sup><sup>_n_</sup> _i_ =1<sup>_b_</sup> _∂β∂Wt_ +1 _i_<sup>**J**</sup><sup>**_β_**(</sup><sup>**w**)</sup><sup>_i,k}_</sup> _k_<sup>_n_</sup> =1 **w** _←_<sup>�</sup> **w** _∈_ [0 _,_ 1]<sup>_n_</sup> _,|_ **w** _|>nc_ � **w** _− γ∇W_ 1( **w** )� , _ib ←_ 0 **end if end for** 

We propose _W_ 1-ACAS (Algorithm 1), which operates by sequentially estimating normalized scores _βt_ using the current weight estimates. The weights **w** are then periodically updated to minimize the objective in Eq. 8, based on the online sample buffer and the update rules in Eqs. 12, 13 and 14. 

**Aggregation Across Multiple Forecast Horizons** We extend Algorithm 1 to operate across multiple forecast horizons. Specifically, we runa _d_ -step ahead prediction error, _St_<sup>_d_</sup> +1<sup>=</sup> �� _Y Dt_ +1 parallel instances of the algorithm, each associated with _− Y_ ˆ _td_ +1��, with _Y_ ˆ _td_ +1<sup>=</sup><sup>_hd_(</sup><sup>_Yt−n_</sup> _c_<sup>_−d_:</sup><sup>_t−d_+1)</sup><sup>_,d ∈_[</sup><sup>_D_]</sup><sup>_._</sup> This produces a set of _D_ conformal _p_ -values for each observation _t_ + 1, denoted _{βt_<sup>_d_</sup> +1<sup>_}_</sup> _d∈_ [ _D_ ]<sup>.The</sup> final anomaly score is the median across horizons, 

_β_ ¯ _t_ +1 = median _d∈_ [ _D_ ] _βt_<sup>_d_</sup> +1<sup>_,_</sup> _βt_<sup>_d_</sup> +1<sup>=</sup><sup>_β_</sup> **w**<sup>_d_(</sup><sup>_S_</sup> _t_<sup>_d_</sup> +1<sup>)</sup><sup>_._</sup> (15) This requires an observation to be identified as a significant outlier by more than half of the horizonspecific detectors. In the streaming setting, we maintain a buffer of forecasts at different horizons. When a new sample _Yt_ +1 is observed, we collect its aligned forecasts _{Y_<sup>ˆ</sup> _t_<sup>_d_</sup> +1<sup>_}_</sup> _d∈_ [ _D_ ]<sup>,computethe</sup> corresponding errors _{St_<sup>_d_</sup> +1<sup>_}_</sup> _d∈_ [ _D_ ]<sup>,andupdateeachhorizon-specificinstanceofAlgorithm1to</sup> obtain the adaptive _p_ -values, _{βt_<sup>_d_</sup> +1<sup>_}_</sup> _d∈_ [ _D_ ]<sup>. In Appendix C.2.4 we describe how Algorithm 1 extends</sup> to multivariate time series anomaly detection in a similar manner. We also outline several standard p- value combination techniques, which can also be applied to aggregate the horizon-specific p-values. 

## 6 EXPERIMENTS 

We evaluate the proposed conformalized anomaly score _W_ 1-ACAS (Algorithm 1) by analyzing its calibration and anomaly detection performance on time series data. Synthetic experiments (Appendix C.1) validate its ability to remain calibrated under both gradual and abrupt distribution shifts, where ground-truth _p_ -values are available. Our main empirical study focuses on real-world anomaly detection datasets, where we assess detection accuracy using both threshold-independent and threshold-dependent metrics. 

**Anomaly Detection Datasets.** We evaluated the performance of our proposed method ( _W_ 1- ACAS, Algorithm 1) for unsupervised univariate time series anomaly detection when applied to a 

7 

Published as a conference paper at ICLR 2026 

pre-trained time series foundation model. Experiments are conducted on seven benchmark datasets: YAHOO (Laptev et al., 2015), NEK (Si et al., 2024), NAB (Ahmad et al., 2017), MSL (Lai et al., 2021), IOPS (IOPS, n.d.), STOCK (Tran et al., 2016), and WSD (Zhang et al., 2022), all part of the curated anomaly detection benchmark of Liu & Paparrizos (2024). For the multivariate experiments, we additionally use the curated subsets of TAO (Laboratory, 2024), GECCO (Rehbach et al., 2018), LTDB (Goldberger et al., 2000), and Genesis (von Birgelen & Niggemann, 2018) released as part of the benchmark in Liu & Paparrizos (2024). Each dataset consists of an initial segment without anomalies used for training or calibration, followed by a test split that may contain anomalies. 

_W_ 1 **-ACAS + TSFM.** We integrate _W_ 1-ACAS with three pre-trained TSFMs: Tiny Time Mixers (TTM) (Ekambaram et al., 2024), Chronos-Bolt-Small (Chronos) (Ansari et al., 2024), and TiRex (Auer et al., 2025). All models use a context length of 52 and a forecast horizon of _D_ = 15. For Algorithm 1, we set the critical false alarm rate to _αc_ = 0 _._ 01, batch size _nb_ = 10, and learning rate _γ_ = 0 _._ 001. We use ADAM (Kingma & Ba, 2015) to perform an adaptive gradient descent on the weights **w** . Appendix C.2.3, Fig. 8, analyzes the impact of aggregating forecast horizons, showing that _D_ = 15 provides a reasonable balance between performance and sample efficiency. Figures 9, 10, and 11 show the sensitivity of _W_ 1-ACAS to the learning rate _γ_ , batch size _nb_ , and _αc_ . The method shows low variability for small _γ_ and _nb_ . The parameter _αc_ controls the maximum acceptable _p_ -value resolution: smaller values require a larger number of in-distribution past observations _nc_ , but do not impose a lower bound on the detectable anomaly level. 

**Baseline Methods.** We compare _W_ 1-ACAS against two TSFM-based baselines: a **Gaussian** model that fits the mean absolute forecast error across _d_ steps using calibration data, and a **Conformal** offline approach that learns _p_ -value mappings per horizon and aggregates them by the median. We also include top-performing classical methods from Liu & Paparrizos (2024): **KShape** (Paparrizos & Gravano, 2015; 2017; Boniol et al., 2021), **POLY** (Li et al., 2007), **Sub-PCA** (Aggarwal & Aggarwal, 2017), **Sub-KNN** (Ramaswamy et al., 2000), and **SAND** (Boniol et al., 2021). We further include strong semi-supervised deep learning–based anomaly detection methods (Audibert et al., 2022), namely **CNN** (Munir et al., 2018), **USAD** (Audibert et al., 2020), and **OmniAnomaly** (Su et al., 2019), as well as the recent general purpose TSFM **MOMENT** (Goswami et al., 2024), which provides zero-shot anomaly scoring. Additional details are provided in Appendix C.2.1. 

**Evaluation Metrics.** We report both point-wise (AUC, PA-F1) (Wu et al., 2022; Wang et al., 2024; Liu & Paparrizos, 2024) and range-wise metrics (VUS (Paparrizos et al., 2022a), AffiliationF1 (Huet et al., 2022)). For threshold-dependent scores (PA-F1, Affiliation-F1), we follow the oracle strategy of Liu & Paparrizos (2024), selecting the best threshold in [0 _,_ 1] and reporting the associated False Positive Rate (FPR) and calibration error (CalErr). Further details are in Appendix C.2.2. 

**Results** Table 1 reports the average performance of _W_ 1-ACAS, applied to different TSFM models, compared against the described baselines on the univariate datasets. Our method achieves the strongest performance on threshold-dependent metrics (PA-F1, Affiliation-F), including when compared with semi-supervised methods such as CNN, USAD, and OmniAnomaly, while remaining competitive on threshold-independent metrics (AUC, VUS). When conditioned on the same TSFM model, _W_ 1-ACAS shows clear improvements over the Gaussian and Conformal baselines. Figure 2 shows the average performance per univariate dataset for a subset of the methods, extended per-dataset results are provided in Tables 2, 3 and 4 in Appendix C.2.3. Table 5 shows that TSFM models have similar prediction errors across datasets, consistent with their comparable anomaly detection performance. Results for the multivariate datasets are presented in Table 6 in Appendix C.2.4, where we demonstrate how our approach naturally extends to the multivariate setting via _p_ -value aggregation, achieving top performance relative to the corresponding baselines. 

Figure 3 shows the FPR–threshold curves in the low-FPR regime, where _W_ 1-ACAS (blue) yields the most conservative thresholds, staying closer to or below the identity line compared to competing methods, while also exhibiting the lowest variance. Figure 4 shows representative detection examples along with the final learned weights. We observe that _W_ 1-ACAS is adapted to capture underlying temporal patterns in errors if present. Moreover, our method effectively identifies a transition in score distributions (e.g., in the vicinity of an anomalous region) but then quickly adapts to the new anomalous distribution; this helps minimize the number of alarms in the end-to-end system. 

Additional examples are provided in Appendix C.2.3: Figure 6 shows more detection cases, and Figure 7 illustrates the trade-offs between FPR and F1 scores (PA-F1, Affiliation-F) across datasets. The operating points of _W_ 1-ACAS (blue), in most cases, achieve both the highest F1 score and 

8 

Published as a conference paper at ICLR 2026 

Table 1: **Performance Summary across univariate datasets.** Entries indicate the mean _±_ standard deviation computed by first averaging within each dataset group, then averaging across groups (equal weight). Higher numbers are better for PA-F1, Affiliation-F, AUC-PR, VUS-PR; lower numbers are better for FPR, and calibration error (CalErr). Underlined results indicate best post-hoc methods applied to the same base forecaster, while bold indicate best results overall. Methods marked with * denote deep learning semi-supervised approaches. 

|Forecaster|AD Method|PA-F1_↑_|Affliation-F_↑_|FPR_↓_|CalErr_↓_|AUC-PR_↑_|VUC-PR_↑_|
|---|---|---|---|---|---|---|---|
|Chronos|_W_1-ACAS|0.912 ± 0.066|0.893 ± 0.060|**0.077 ± 0.114**|**0.025 ± 0.029**|**0.355 ± 0.261**|0.440 ± 0.272|
|Chronos|Conformal|0.863 ± 0.109|0.891 ± 0.063|0.111 ± 0.130|0.038 ± 0.055|0.310 ± 0.240|0.420 ± 0.248|
|Chronos|Gaussian|0.716 ± 0.260|0.842 ± 0.066|0.123 ± 0.109|0.075 ± 0.061|0.265 ± 0.250|0.438 ± 0.245|
|TTM|_W_1-ACAS|0.889 ± 0.108|0.886 ± 0.058|0.082 ± 0.120|0.029 ± 0.031|0.342 ± 0.261|0.449 ± 0.245|
|TTM|Conformal|0.851 ± 0.124|0.885 ± 0.062|0.120 ± 0.145|0.044 ± 0.056|0.317 ± 0.247|0.448 ± 0.250|
|TTM|Gaussian|0.733 ± 0.240|0.849 ± 0.067|0.128 ± 0.115|0.081 ± 0.065|0.270 ± 0.261|0.450 ± 0.249|
|TiRex|_W_1-ACAS|**0.925 ± 0.048**|**0.897 ± 0.064**|0.084 ± 0.113|0.025 ± 0.031|0.344 ± 0.269|0.438 ± 0.272|
|TiRex|Conformal|0.878 ± 0.085|0.890 ± 0.063|0.107 ± 0.137|0.038 ± 0.055|0.308 ± 0.257|0.429 ± 0.256|
|TiRex|Gaussian|0.714 ± 0.264|0.837 ± 0.068|0.119 ± 0.103|0.090 ± 0.071|0.270 ± 0.264|0.432 ± 0.250|
|-|POLY|0.527 ± 0.276|0.848 ± 0.072|0.334 ± 0.269|0.282 ± 0.130|0.044 ± 0.031|0.377 ± 0.207|
|-|Sub-KNN|0.479 ± 0.291|0.786 ± 0.074|0.451 ± 0.276|0.174 ± 0.124|0.118 ± 0.106|0.321 ± 0.234|
|-|KShape|0.533 ± 0.299|0.789 ± 0.096|0.508 ± 0.291|0.176 ± 0.132|0.125 ± 0.135|0.303 ± 0.262|
|-|PCA|0.536 ± 0.332|0.826 ± 0.097|0.374 ± 0.297|0.248 ± 0.131|0.100 ± 0.093|0.417 ± 0.274|
|-|SAND|0.460 ± 0.309|0.790 ± 0.079|0.511 ± 0.296|0.134 ± 0.048|0.101 ± 0.117|0.289 ± 0.190|
|-|CNN|0.858 ± 0.138|0.881 ± 0.059|0.083 ± 0.103|0.643 ± 0.227|0.269 ± 0.292|0.423 ± 0.289|
|-|OmniAnomaly|0.674 ± 0.282|0.855 ± 0.068|0.209 ± 0.171|0.571 ± 0.187|0.166 ± 0.087|0.429 ± 0.317|
|-|USAD|0.498 ± 0.333|0.809 ± 0.099|0.425 ± 0.298|0.324 ± 0.161|0.088 ± 0.088|0.398 ± 0.262|
|-|MOMENT<br>~~Z~~S|0.596 ± 0.305|0.867 ± 0.088|0.261 ± 0.292|0.417 ± 0.198|0.110 ± 0.075|**0.461 ± 0.162**|




![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0009-03.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0009-04.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0009-05.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0009-06.png)


Figure 2: **Performance across univariate datasets for a subset of anomaly detection methods.** Heatmaps show the average per-dataset performance for PA-F1, Affiliation-F, AUC-PR, and Calibration Error (CalErr) across a selected subset of methods. Higher values indicate better performance for PA-F1, Affiliation-F, and AUC-PR, while lower values are preferred for CalErr. Overall, the proposed _W_ 1-ACAS combined with Chronos, TiRex or TTM yields consistently low calibration error while remaining among the top-performing approaches. Note that CNN, OmniAnomaly and USAD are semi-supervised methods trained on the non-anomalous training datasplit. 

lowest FPR, especially for PA-F1. Within each TSFM model, our method dominates its Gaussian (green) and Conformal (orange) counterparts in nearly all cases. Furthermore, it produces bettercalibrated scores (low CalErr), making threshold selection more reliable in practice. 

9 

Published as a conference paper at ICLR 2026 


![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0010-01.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0010-02.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0010-03.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0010-04.png)


Figure 3: **FPR vs. threshold in the low-FPR regime.** Curves shows the mean false positive rate (FPR) across datasets for a given method, with shaded inter-quartile range (IQR) bands. The dashed gray line indicates ideal calibration ( _FPR_ = _β_ ). Curves above the line reflect over-confident scoring (FPR larger than threshold), while curves below the line reflect conservative scoring. In most cases, _W_ 1-ACAS (blue) yields the most conservative thresholds, staying closer to or below the identity line compared to competing methods, while also having the lowest variance. 


![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0010-06.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0010-07.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0010-08.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0010-09.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0010-10.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0010-11.png)


Figure 4: Example signals (blue) with ground-truth anomaly labels (red shading) are shown in the first row, where detected outliers (red dots) occur when adaptive _p_ -values (orange) fall below a threshold under our proposed _W_ 1-ACAS method. The second row shows the final adaptive weights (orange) over past errors (blue), averaged across horizons, illustrating how _W_ 1-ACAS adapts to and captures underlying error patterns 

## 7 CONCLUSION 

In this paper, we presented _W_ 1-ACAS, a post-hoc adaptive conformal anomaly detection framework that leverages predictions from pretrained TSFMs to provide interpretable, distribution-agnostic, and well-calibrated anomaly scores without requiring retraining or large datasets. Experiments on benchmark datasets show that our method consistently outperforms competing baselines. _W_ 1-ACAS yields more conservative and stable thresholds, its a principled and easily applicable approach that adapts online to temporal error patterns, and minimizes false alarms by adjusting to distributions shifts. These properties make it especially suited for online monitoring in industrial and data-scarce environments. Future work will explore refining conformal weighting with contextual features, with straightforward extensions to multivariate anomalies via horizon-style aggregation. 

## REFERENCES 

Charu C Aggarwal and Charu C Aggarwal. _An introduction to outlier analysis_ . Springer, 2017. 

- Subutai Ahmad, Alexander Lavin, Scott Purdy, and Zuha Agha. Unsupervised real-time anomaly detection for streaming data. _Neurocomputing_ , 262:134–147, 2017. 

> Ali Ajami and Mahdi Daneshvar. Data driven approach for fault detection and diagnosis of turbine in thermal power plant using independent component analysis (ica). _International Journal of Electrical Power & Energy Systems_ , 43(1):728–735, 2012. 

10 

Published as a conference paper at ICLR 2026 

- Salim I Amoukou and Nicolas JB Brunel. Adaptive conformal prediction by reweighting nonconformity score. _arXiv preprint arXiv:2303.12695_ , 2023. 

- Anastasios N Angelopoulos and Stephen Bates. A gentle introduction to conformal prediction and distribution-free uncertainty quantification. _arXiv preprint arXiv:2107.07511_ , 2021. 

- Abdul Fatir Ansari, Lorenzo Stella, Caner Turkmen, Xiyuan Zhang, Pedro Mercado, Huibin Shen, Oleksandr Shchur, Syama Sundar Rangapuram, Sebastian Pineda Arango, Shubham Kapoor, et al. Chronos: Learning the language of time series. _arXiv preprint arXiv:2403.07815_ , 2024. 

- Julien Audibert, Pietro Michiardi, Fr´ed´eric Guyard, S´ebastien Marti, and Maria A Zuluaga. Usad: Unsupervised anomaly detection on multivariate time series. In _Proceedings of the 26th ACM SIGKDD international conference on knowledge discovery & data mining_ , pp. 3395–3404, 2020. 

- Julien Audibert, Pietro Michiardi, Fr´ed´eric Guyard, S´ebastien Marti, and Maria A Zuluaga. Do deep neural networks contribute to multivariate time series anomaly detection? _Pattern Recognition_ , 132:108945, 2022. 

- Andreas Auer, Patrick Podest, Daniel Klotz, Sebastian B¨ock, G¨unter Klambauer, and Sepp Hochreiter. Tirex: Zero-shot forecasting across long and short horizons with enhanced in-context learning. _arXiv preprint arXiv:2505.23719_ , 2025. 

- Rina Foygel Barber, Emmanuel J Candes, Aaditya Ramdas, and Ryan J Tibshirani. Conformal prediction beyond exchangeability. _The Annals of Statistics_ , 51(2):816–845, 2023. 

- Michele Basseville. Detection of abrupt changes: Theory and application. _Prentice-Hall google schola_ , 2:3–11, 1993. 

- Stephen Bates, Emmanuel Cand`es, Lihua Lei, Yaniv Romano, and Matteo Sesia. Testing for outliers with conformal p-values. _The Annals of Statistics_ , 51(1):149–178, 2023. 

- A Beghi, R Brignoli, Luca Cecchinato, Gabriele Menegazzo, Mirco Rampazzo, and F Simmini. Data-driven fault detection and diagnosis for hvac water chillers. _Control Engineering Practice_ , 53:79–91, 2016. 

- Paul Boniol, John Paparrizos, Themis Palpanas, and Michael J Franklin. Sand: streaming subsequence anomaly detection. _Proceedings of the VLDB Endowment_ , 14(10):1717–1729, 2021. 

- Paul Boniol, Qinghua Liu, Mingyi Huang, Themis Palpanas, and John Paparrizos. Dive into timeseries anomaly detection: A decade review. _arXiv preprint arXiv:2412.20512_ , 2024. 

- Dhruv Choudhary, Arun Kejariwal, and Francois Orsini. On the runtime-efficacy trade-off of anomaly detection techniques for real-time streaming data. _arXiv preprint arXiv:1710.04735_ , 2017. 

- Andrew A Cook, G¨oksel Mısırlı, and Zhong Fan. Anomaly detection for iot time-series data: A survey. _IEEE Internet of Things Journal_ , 7(7):6481–6494, 2019. 

- Vijay Ekambaram, Arindam Jati, Nam H Nguyen, Pankaj Dayama, Chandra Reddy, Wesley M Gifford, and Jayant Kalagnanam. Ttms: Fast multi-level tiny time mixers for improved zero-shot and few-shot forecasting of multivariate time series. _arXiv preprint arXiv:2401.03955_ , 2024. 

- Ronald Aylmer Fisher. Statistical methods for research workers. In _Breakthroughs in statistics: Methodology and distribution_ , pp. 66–70. Springer, 1970. 

- Jo˜ao Gama, Indr˙e Zliobait˙e,<sup>ˇ</sup> Albert Bifet, Mykola Pechenizkiy, and Abdelhamid Bouchachia. A survey on concept drift adaptation. _ACM computing surveys (CSUR)_ , 46(4):1–37, 2014. 

- Subhankar Ghosh, Taha Belkhouja, Yan Yan, and Janardhan Rao Doppa. Improving uncertainty quantification of deep classifiers via neighborhood conformal prediction: Novel algorithm and theoretical analysis. _arXiv preprint arXiv:2303.10694_ , 2023. 

- Federico Giannoni, Marco Mancini, and Federico Marinelli. Anomaly detection models for iot time series data. _arXiv preprint arXiv:1812.00890_ , 2018. 

- Isaac Gibbs and Emmanuel Candes. Adaptive conformal inference under distribution shift. _Advances in Neural Information Processing Systems_ , 34:1660–1672, 2021. 

11 

Published as a conference paper at ICLR 2026 

- Isaac Gibbs and Emmanuel J Cand`es. Conformal inference for online prediction with arbitrary distribution shifts. _Journal of Machine Learning Research_ , 25(162):1–36, 2024. 

- Isaac Gibbs, John J Cherian, and Emmanuel J Cand`es. Conformal prediction with conditional guarantees. _arXiv preprint arXiv:2305.12616_ , 2023. 

- Ary L Goldberger, Luis AN Amaral, Leon Glass, Jeffrey M Hausdorff, Plamen Ch Ivanov, Roger G Mark, Joseph E Mietus, George B Moody, Chung-Kang Peng, and H Eugene Stanley. Physiobank, physiotoolkit, and physionet: components of a new research resource for complex physiologic signals. _circulation_ , 101(23):e215–e220, 2000. 

- Mononito Goswami, Cristian Challu, Laurent Callot, Lenon Minorics, and Andrey Kan. Unsupervised model selection for time-series anomaly detection. _arXiv preprint arXiv:2210.01078_ , 2022. 

- Mononito Goswami, Konrad Szafer, Arjun Choudhry, Yifu Cai, Shuo Li, and Artur Dubrawski. Moment: A family of open time-series foundation models. _arXiv preprint arXiv:2402.03885_ , 2024. 

- Leying Guan. Conformal prediction with localization. _arXiv preprint arXiv:1908.08558_ , 2019. 

- Leying Guan. Localized conformal prediction: A generalized inference framework for conformal prediction. _Biometrika_ , 110(1):33–50, 2023. 

- Xing Han, Ziyang Tang, Joydeep Ghosh, and Qiang Liu. Split localized conformal prediction. _arXiv preprint arXiv:2206.13092_ , 2022. 

- Nicholas A Heard and Patrick Rubin-Delanchy. Choosing between methods of combining-values. _Biometrika_ , 105(1):239–246, 2018. 

- Alexis Huet, Jose Manuel Navarro, and Dario Rossi. Local evaluation of time series anomaly detection algorithms. In _Proceedings of the 28th ACM SIGKDD Conference on Knowledge Discovery and Data Mining_ , pp. 635–645, 2022. 

- IOPS. IOPS Dataset, n.d. URL http://iops.ai/dataset_detail/?id=10. Accessed: [DATE]. 

- Ameeth Kanawaday and Aditya Sane. Machine learning for predictive maintenance of industrial machines using iot sensor data. In _2017 8th IEEE international conference on software engineering and service science (ICSESS)_ , pp. 87–90. IEEE, 2017. 

- Diederik P Kingma and Jimmy Ba. Adam: A method for stochastic optimization. _International Conference on Learning Representations (ICLR)_ , 2015. 

- NOAA Pacific Marine Environmental Laboratory. Tropical atmosphere ocean (TAO) project dataset. https://www.pmel.noaa.gov/, 2024. Data retrieved from the TAO Project maintained by NOAA PMEL. 

- Kwei-Herng Lai, Daochen Zha, Junjie Xu, Yue Zhao, Guanchu Wang, and Xia Hu. Revisiting time series outlier detection: Definitions and benchmarks. In _Thirty-fifth conference on neural information processing systems datasets and benchmarks track (round 1)_ , 2021. 

- N. Laptev, S. Amizadeh, and Y. Billawala. S5 - A Labeled Anomaly Detection Dataset, version 1.0(16M), March 2015. 

- Jing Lei and Larry Wasserman. Distribution-free prediction bands for non-parametric regression. _Journal of the Royal Statistical Society Series B: Statistical Methodology_ , 76(1):71–96, 2014. 

- Zhi Li, Hong Ma, and Yongbing Mei. A unifying method for outlier and change detection from data streams based on local polynomial fitting. In _Advances in Knowledge Discovery and Data Mining: 11th Pacific-Asia Conference, PAKDD 2007, Nanjing, China, May 22-25, 2007. Proceedings 11_ , pp. 150–161. Springer, 2007. 

- Yuxuan Liang, Haomin Wen, Yuqi Nie, Yushan Jiang, Ming Jin, Dongjin Song, Shirui Pan, and Qingsong Wen. Foundation models for time series analysis: A tutorial and survey. In _Proceedings of the 30th ACM SIGKDD conference on knowledge discovery and data mining_ , pp. 6555–6565, 2024. 

12 

Published as a conference paper at ICLR 2026 

- Qinghua Liu and John Paparrizos. The elephant in the room: Towards a reliable time-series anomaly detection benchmark. In _The Thirty-eight Conference on Neural Information Processing Systems Datasets and Benchmarks Track_ , 2024. 

- Huiying Mao, Ryan Martin, and Brian J Reich. Valid model-free spatial prediction. _Journal of the American Statistical Association_ , 119(546):904–914, 2024. 

- Ramin Moghaddass and Jianhui Wang. A hierarchical framework for smart grid anomaly detection using large-scale smart meter data. _IEEE Transactions on Smart Grid_ , 9(6):5820–5830, 2017. 

- Mohsin Munir, Shoaib Ahmed Siddiqui, Andreas Dengel, and Sheraz Ahmed. Deepant: A deep learning approach for unsupervised anomaly detection in time series. _Ieee Access_ , 7:1991–2005, 2018. 

- Harris Papadopoulos, Kostas Proedrou, Volodya Vovk, and Alex Gammerman. Inductive confidence machines for regression. In _Machine Learning: ECML 2002: 13th European Conference on Machine Learning Helsinki, Finland, August 19–23, 2002 Proceedings 13_ , pp. 345–356. Springer, 2002. 

- John Paparrizos and Luis Gravano. k-shape: Efficient and accurate clustering of time series. In _Proceedings of the 2015 ACM SIGMOD international conference on management of data_ , pp. 1855–1870, 2015. 

- John Paparrizos and Luis Gravano. Fast and accurate time-series clustering. _ACM Transactions on Database Systems (TODS)_ , 42(2):1–49, 2017. 

- John Paparrizos, Paul Boniol, Themis Palpanas, Ruey S Tsay, Aaron Elmore, and Michael J Franklin. Volume under the surface: a new accuracy evaluation measure for time-series anomaly detection. _Proceedings of the VLDB Endowment_ , 15(11):2774–2787, 2022a. 

- John Paparrizos, Yuhao Kang, Paul Boniol, Ruey S Tsay, Themis Palpanas, and Michael J Franklin. Tsb-uad: an end-to-end benchmark suite for univariate time-series anomaly detection. _Proceedings of the VLDB Endowment_ , 15(8):1697–1711, 2022b. 

- Sridhar Ramaswamy, Rajeev Rastogi, and Kyuseok Shim. Efficient algorithms for mining outliers from large data sets. In _Proceedings of the 2000 ACM SIGMOD international conference on Management of data_ , pp. 427–438, 2000. 

- Kashif Rasul, Arjun Ashok, Andrew Robert Williams, Arian Khorasani, George Adamopoulos, Rishika Bhagwatkar, Marin Biloˇs, Hena Ghonia, Nadhir Hassen, Anderson Schneider, et al. Lagllama: Towards foundation models for time series forecasting. In _R0-FoMo: Robustness of Fewshot and Zero-shot Learning in Large Foundation Models_ , 2023. 

- Kashif Rasul, Arjun Ashok, Andrew Robert Williams, Hena Ghonia, Rishika Bhagwatkar, Arian Khorasani, Mohammad Javad Darvishi Bayazi, George Adamopoulos, Roland Riachi, Nadhir Hassen, et al. Lag-llama: Towards foundation models for probabilistic time series forecasting. _Preprint_ , 2024. 

- Frederik Rehbach, Steffen Moritz, Sowmya Chandrasekaran, Margarita Rebolledo, Martina Friese, and Thomas Bartz-Beielstein. Gecco 2018 industrial challenge: Monitoring of drinking-water quality. _Accessed: Feb_ , 19:2019, 2018. 

- Sakti Saurav, Pankaj Malhotra, Vishnu TV, Narendhar Gugulothu, Lovekesh Vig, Puneet Agarwal, and Gautam Shroff. Online anomaly detection with concept drift adaptation using recurrent neural networks. In _Proceedings of the acm india joint international conference on data science and management of data_ , pp. 78–87, 2018. 

- Sebastian Schmidl, Phillip Wenig, and Thorsten Papenbrock. Anomaly detection in time series: a comprehensive evaluation. _Proceedings of the VLDB Endowment_ , 15(9):1779–1797, 2022. 

- Matteo Sesia and Yaniv Romano. Conformal prediction using conditional histograms. _Advances in Neural Information Processing Systems_ , 34:6304–6315, 2021. 

- Glenn Shafer and Vladimir Vovk. A tutorial on conformal prediction. _Journal of Machine Learning Research_ , 9(3), 2008. 

13 

Published as a conference paper at ICLR 2026 

- Gauri Shah and Aashis Tiwari. Anomaly detection in iiot: A case study using machine learning. In _Proceedings of the ACM India joint international conference on data science and management of data_ , pp. 295–300, 2018. 

- Haotian Si, Jianhui Li, Changhua Pei, Hang Cui, Jingwen Yang, Yongqian Sun, Shenglin Zhang, Jingjing Li, Haiming Zhang, Jing Han, et al. Timeseriesbench: An industrial-grade benchmark for time series anomaly detection models. In _2024 IEEE 35th International Symposium on Software Reliability Engineering (ISSRE)_ , pp. 61–72. IEEE, 2024. 

- Ya Su, Youjian Zhao, Chenhao Niu, Rong Liu, Wei Sun, and Dan Pei. Robust anomaly detection for multivariate time series through stochastic recurrent neural network. In _Proceedings of the 25th ACM SIGKDD international conference on knowledge discovery & data mining_ , pp. 2828–2837, 2019. 

- Ryan J Tibshirani, Rina Foygel Barber, Emmanuel Candes, and Aaditya Ramdas. Conformal prediction under covariate shift. _Advances in neural information processing systems_ , 32, 2019. 

- Luan Tran, Liyue Fan, and Cyrus Shahabi. Distance-based outlier detection in data streams. _Proceedings of the VLDB Endowment_ , 9(12):1089–1100, 2016. 

- Alexander von Birgelen and Oliver Niggemann. Anomaly detection and localization for cyberphysical production systems with self-organizing maps. In _IMPROVE-Innovative Modelling Approaches for Production Systems to Raise Validatable Efficiency: Intelligent Methods for the Factory of the Future_ , pp. 55–71. Springer Berlin Heidelberg Berlin, Heidelberg, 2018. 

- Vladimir Vovk, Alexander Gammerman, and Glenn Shafer. _Algorithmic learning in a random world_ , volume 29. Springer, 2005. 

- Yuxuan Wang, Haixu Wu, Jiaxiang Dong, Yong Liu, Mingsheng Long, and Jianmin Wang. Deep time series models: A comprehensive survey and benchmark. _arXiv preprint arXiv:2407.13278_ , 2024. 

- Daniel J Wilson. The harmonic mean p-value for combining dependent tests. _Proceedings of the National Academy of Sciences_ , 116(4):1195–1200, 2019. 

- Haixu Wu, Tengge Hu, Yong Liu, Hang Zhou, Jianmin Wang, and Mingsheng Long. Timesnet: Temporal 2d-variation modeling for general time series analysis. _arXiv preprint arXiv:2210.02186_ , 2022. 

- Margaux Zaffran, Olivier F´eron, Yannig Goude, Julie Josse, and Aymeric Dieuleveut. Adaptive conformal predictions for time series. In _International Conference on Machine Learning_ , pp. 25834–25866. PMLR, 2022. 

- Shenglin Zhang, Zhenyu Zhong, Dongwen Li, Qiliang Fan, Yongqian Sun, Man Zhu, Yuzhi Zhang, Dan Pei, Jiyan Sun, Yinlong Liu, et al. Efficient kpi anomaly detection through transfer learning for large-scale web services. _IEEE Journal on Selected Areas in Communications_ , 40(8):2440– 2455, 2022. 

14 

Published as a conference paper at ICLR 2026 

## A RELATED WORK EXTENDED 

**Time Series Anomaly Detection** A key class of anomaly detection methods is prediction-based Giannoni et al. (2018), where anomalies are identified by deviations between predicted and observed values. These approaches assume that a well-trained forecaster captures normal temporal patterns, and significant prediction errors indicate potential anomalies Boniol et al. (2024). Such methods can in principle capture both point anomalies, where individual values deviate sharply, and contextual anomalies, where deviations only emerge relative to surrounding context Boniol et al. (2024). Given our focus on unsupervised settings with limited historical data, we build on pretrained forecasting models. Recent Time Series Foundation Models (TSFMs), trained at scale for forecasting, are particularly well suited for online detection in data-scarce scenarios Rasul et al. (2023; 2024); Ansari et al. (2024); Liang et al. (2024). In this work, we leverage three representative TSFMs: Tiny Time Mixers (TTM) (Ekambaram et al., 2024), based on the TSMixer architecture; Chronos-Bolt-Small (Chronos) (Ansari et al., 2024), a transformer-based model; and TiRex (Auer et al., 2025), which leverages an xLSTM architecture. 

Recent benchmarks have evaluated the effectiveness of time series anomaly detection methods. The study by Liu & Paparrizos (2024) found that in unsupervised settings, classical distance-based and density-based approaches Li et al. (2007); Ramaswamy et al. (2000); Aggarwal & Aggarwal (2017); Paparrizos & Gravano (2015; 2017); Boniol et al. (2021) often outperform more complex models. However, these methods typically require access to the entire dataset (i.e., anomaly detections are non-causal and occur after the fact) and are not inherently designed for streaming applications Boniol et al. (2024). They may also struggle to capture richer temporal structures in the data, which limits their effectiveness in dynamic environments. Another critical challenge concerns the interpretability of anomaly scores and the choice of thresholds. Many evaluation studies emphasize threshold-independent metrics Schmidl et al. (2022); Paparrizos et al. (2022b); Goswami et al. (2022), yet the scores themselves often lack clear probabilistic meaning. Common thresholding strategies, such as standard deviation-based rules, depend on statistics computed over the entire dataset, making them impractical for streaming scenarios Ahmad et al. (2017). 

In real-world deployments, an anomaly detection system must not only detect anomalies but also provide interpretable confidence scores while minimizing false alarms Cook et al. (2019). A high false alarm rate can overwhelm monitoring systems, reducing their practical utility. Our work addresses these challenges by developing an approach that enables adaptive thresholding in streaming environments while ensuring reliable anomaly detection, regardless of whether the anomalies are point-based or contextual. 

**Conformal Prediction** Conformal prediction methods Vovk et al. (2005) have gained significant attention for their ability to provide distribution-free uncertainty quantification with finite-sample generalization guarantees Shafer & Vovk (2008); Angelopoulos & Bates (2021). Among these, split conformal prediction (SCP) Papadopoulos et al. (2002) is a particularly appealing post-hoc, model-agnostic technique that requires only the model’s predictions and a calibration dataset. SCP estimates an empirical quantile of a nonconformity score measuring how well the model’s predictions align with the data to construct prediction sets that achieve the desired coverage. However, these guarantees rely on the exchangeability assumption<sup>7</sup> between calibration and test observations, which often does not hold in time series settings. 

For non-exchangeable data, particularly time series, several adaptive conformal prediction methods have been proposed Gibbs & Candes (2021); Zaffran et al. (2022); Gibbs & Cand`es (2024). These approaches dynamically adjust the estimated quantile to correct for distribution shifts and achieve the target coverage level. However, they are typically designed for a single error rate objective, often optimizing the pinball loss or a surrogate function. In contrast, our work focuses on an adaptive method that remains effective across all error rates and desired alarm rate. 

Weighted conformal quantile estimation Gibbs et al. (2023), where the calibration or past nonconformity scores are weighted differently has been used to achieve local coverage when the distribution of the error differs across the input space. Essentially, for any given observation, scores of samples that are similar to that observation get up-weighted, usually based on some metric (e.g., proximity in the covariate space) (Lei & Wasserman, 2014; Guan, 2019; Tibshirani et al., 2019; Sesia & Romano, 2021; Han et al., 2022; Guan, 2023; Ghosh et al., 2023; Mao et al., 2024), weights 

> 7informally, a sequence of observations is exchangeable if any permutation of the observations has the same joint probability 

15 

Published as a conference paper at ICLR 2026 

can also be optimized to capture the variance of the non-conformity score across the input space (Han et al., 2022; Amoukou & Brunel, 2023). In the context of non-exchangeable data, Barber et al. (2023) derived a coverage bound linking the weights associated with a calibration sample and the total variation distance between the observed sequence and one where the calibration sample is swapped with the test sample. This bound suggests one should up-weight samples that are ‘nearly exchangeable’ with the new observation on a pairwise basis. This is the main inspiration for our proposed approach. 

Conformal prediction has been explored for anomaly detection by setting thresholds on arbitrary anomaly scores from non-anomalous data while assuming exchangeability Angelopoulos & Bates (2021); Guan (2019); Bates et al. (2023). However, to the best of our knowledge, there is no existing method that simultaneously (i) seamlessly applies these techniques to generate interpretable, distribution-agnostic anomaly scores, (ii) directly translates scores into a desired alarm rate, and (iii) is inherently adapted to operate under non-exchangeability assumptions. Our work aims to bridge this gap by developing a conformal anomaly detection framework that is both interpretable and robust to real-world time series shifts. 

## B PROOFS 

**Proof Proposition 4.1** We show the equivalence of the detector _Cβ_ **w** and the conformal outlier detector in equation 2 over the non-conformity scores _S_ by proving the following 


![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0016-05.png)


which involves proving that the events _β_ **w** ( _St_ +1) _< α_ and _St_ +1 _>_ Q1 _−α_ ( **s** _,_ **w** ) are equivalent. 

If _β_ **w** ( _St_ +1) = _βt_ +1 _< α_ then _St_ +1 _>_ Q1 _−α_ ( **s** _,_ **w** ) since by definition of _β_ **w** ( _·_ ) in equation 6 then _βt_ +1 is the maximum value in [0,1] that satisfies the quantile upper bound. 

If _β_ **w** ( _St_ +1) = _βt_ +1 _≥ α_ and since _Sn_ +1 _≤_ Q1 _−βt_ +1( **s** _,_ **w** ) _≤_ Q1 _−α′_ ( **s** _,_ **w** ) _, ∀α_<sup>_′_</sup> _≤ βt_ +1 we have that _St_ +1 _≤_ Q1 _−α_ ( **s** _,_ **w** ). 

## C ADDITIONAL EXPERIMENTS 

### C.1 SIMULATED EXAMPLES 

We consider a similar simulated setting as Gibbs et al. (2023) to empirically evaluate the performance of the proposed method across time. We analyze a simple scenario where we observe a sequence of random variables _{Yt}_<sup>_T_</sup> _t_ =1<sup>, where</sup><sup>_Yt∼N_(</sup><sup>_µt,_1).We assume that our predictive model</sup> _h_ outputs a constant _Y_<sup>ˆ</sup> _t_ = 0 _, ∀t_ . Then the error is _ϵt_ = _Yt − Y_<sup>ˆ</sup> _t ∼N_ ( _µt,_ 1) and its distribution changes across time based on _µt_ . The nonconformity score is _st_ = _|ϵt|, ∀t_ . We consider two different settings for the sequence of means _{µt}_<sup>_T_</sup> _t_ =1<sup>:</sup> 

- **Random shift setting:** _µt_ drifts continuously across time. Specifically, we set _µ_ 0 = 0 and 


![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0016-13.png)


- **Jump shift setting:** _µt_ undergoes abrupt discontinuities every 500 time steps where _µt_ increases by one step 15 times, and then starts decreasing by 1, 


![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0016-15.png)


Given an observed non-conformity score _st_ = _|ϵt|_ we can compute its corresponding p-value _αt_ such that P **_ϵ_** _t∼N_ ( _µ⊔,∞_ )( _|_ **_ϵ_** _t| > st_ ) = _αt_ = 1 _−_ Φ( _st − µt_ ) + Φ( _−st − µt_ ) and compare it with the one estimated by the proposed normalized anomaly score _β_ **w** ( _st_ ). 

Figures 5.a and 5.b illustrate a sample of the generated signals under the Random Shift and Jump Shift settings. Each sequence consists of _T_ = 6000 time steps, and our results are averaged over 15 independent realizations. We assess the performance of our proposed approach, Algorithm 1, referred to as _W_ 1-ACAS, with parameters _n_ = 2000, _αc_ = 0 _._ 01, and _nb_ = _nc_ = _⌈ α_<sup><u>1</u></sup> _c_<sup>_−_1</sup><sup>_⌉_.</sup> We compare it against two baseline methods: (i) an adaptive conformal approach that assigns equal 

16 

Published as a conference paper at ICLR 2026 

weights of 1 to the most recent 2000 samples (ACAS with a fixed window) and (ii) a naive split conformal approach that computes scores using only the initial 100 samples (Split Conformal with fixed calibration). 

In Figures 5.c and 5.d, we compare the empirical CDFs of each method against the empirical CDF of the ground truth p-values (denoted as Ground Truth), which naturally aligns with the identity line (reference). Notably, _W_ 1-ACAS demonstrates superior calibration, consistently aligning closely with the ground truth CDF and outperforming the other approaches. 

Figures 5.e and 5.f present the average error of the scores of each method with respect to the ground truth p-values, across different bucket ranges of size 0.1 within [0 _,_ 1]. Specifically, we evaluate E[ _|β_ **w** ( _st_ +1) _− αt_ +1 _| | αt ∈_ [ _αl, αu_ ]], where _αt_ +1 represents the ground truth p-value for observation _t_ + 1. The results indicate that _W_ 1-ACAS consistently outperforms the baseline methods, highlighting the advantages of an adaptive approach that dynamically learns how to weight past observations in a principled manner, rather than relying on a fixed number of past samples. 


![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0017-04.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0017-05.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0017-06.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0017-07.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0017-08.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0017-09.png)


Figure 5: Figures (a) and (d) show an example of a generated signal under the random shift and jump shift settings with a sequence length of _T_ = 6000. _µt_ is the expected value of the observed signal, _Yt_ is the observed signal _Yt ∼N_ ( _µt,_ 1), and _Y_<sup>ˆ</sup> _t_ = 0 the predicted value of a naive constant forecaster. Figures (b) and (e) show the empirical cumulative distribution functions (CDFs) of the various calibration approaches compared to the ground truth p-values (Ground Truth), which aligns with the idealized uniform CDF (reference). Results are averaged over 15 realizations. _W_ 1-ACAS demonstrates superior calibration, closely matching the ground truth distribution and improving upon the reference split conformal method (computed over calibration samples) and a fixed window ACAS method. Figures (c) and (f) show the average absolute error of the scores of the different methods with respect to the ground truth p-values, evaluated across bucket ranges of size 0 _._ 1 in [0 _,_ 1]. _W_ 1-ACAS consistently achieves lower estimation errors, highlighting the effectiveness of its adaptive weighting strategy with minimum parameters. 

17 

Published as a conference paper at ICLR 2026 

### C.2 ANOMALY DETECTION REAL DATASETS 

### C.2.1 BASELINE METHODS 

We compare _W_ 1-ACAS against two TSFM-based baselines. The first fits a **Gaussian** distribution to the mean absolute forecast error across _d_ steps using the calibration portion and assigns anomaly scores via the resulting _p_ -values. The second applies a **Conformal** offline approach that learns a _p_ - value mapping from the calibration split for each _d_ and aggregates the scores by the median. These baselines provide simple references built directly on TSFM errors. 

We additionally consider several classic anomaly detection methods reported as top-performing in Liu & Paparrizos (2024): 

- **KShape** (Paparrizos & Gravano, 2015; 2017; Boniol et al., 2021), which clusters subsequences via the k-Shape algorithm and scores anomalies by their distance to cluster centroids; 

- **POLY** (Li et al., 2007), which fits a polynomial to the series and applies a GARCH model to residuals to estimate volatility; 

- **Sub-PCA** (Aggarwal & Aggarwal, 2017), which projects subsequences onto a lowerdimensional hyperplane and scores deviations; 

- **Sub-KNN** (Ramaswamy et al., 2000), which scores each instance by its distance to the _k_ -th nearest neighbor; 

- **SAND** (Boniol et al., 2021), an online method that adaptively down-weights older subsequences. 

- **CNN** (Munir et al., 2018), is a causal convolutional forecasting model, the anomaly score is the prediction error. It is trained on non-anomalous data. 

- **USAD** (Audibert et al., 2020) is an adversarially trained dual–autoencoder model learned on non-anomalous data, where anomaly scores are computed from a weighted reconstruction loss. 

- **OmniAnomaly** (Su et al., 2019) is a stochastic recurrent VAE that incorporates GRU dynamics, planar normalizing flows, and temporal latent stochasticity; anomaly scores are derived from reconstruction probabilities. It is trained on non-anomalous data. 

- **MOMENT** (Goswami et al., 2024) is a general-purpose TSFM based on a T5-style encoder trained via masked time-series modeling. It supports zero-shot anomaly scoring using masked-token reconstruction error and is pretrained on a broad corpus including anomaly detection datasets (Liu & Paparrizos, 2024). 

For these approaches we adopt the implementations from Liu & Paparrizos (2024) with the best reported hyperparameters and their default [0 _,_ 1] min–max normalization fitted on the full dataset. For consistency with our _p_ -value scoring (where lower values indicate greater anomaly), we take one minus the reported score. Unlike our method, these baselines require access to the full test set, whereas ours supports adaptive, causal anomaly detection without full-dataset access. 

### C.2.2 METRICS 

**Threshold-dependent metrics.** We follow the evaluation pipeline provided in Liu & Paparrizos (2024). Given anomaly scores _{βi ∈_ [0 _,_ 1] _}_<sup>_t_</sup> _i_ =1<sup>(interpretedas</sup><sup>_p_-values,wheresmallerval-</sup> ues indicate stronger outliers) and ground-truth labels _{ℓi ∈{_ 0 _,_ 1 _}}_<sup>_t_</sup> _i_ =1<sup>,weevaluatemetrics</sup> _M_ ( _{ℓi}, {ℓ_<sup>ˆ</sup> _i}_ ) _∈_ [0 _,_ 1] where larger is better. Examples include Affiliation-F and PA-F1. For a family of thresholds _{αj ∈_ [0 _,_ 1] _}_<sup>_k_</sup> _j_ =1<sup>, we select the best score</sup> 


![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0018-17.png)


and report the corresponding false positive rate _FPR_ ( _αj∗_ ) = P[ _βi ≤ αj∗ | ℓi_ = 0] _,_ as well as the calibration error _CalErr_ ( _αj∗_ ) = �� _FPR_ ( _αj∗_ ) _− αj∗_ �� _._ Thresholds are evaluated on a uniform grid (linspace) with finer resolution at small _p_ -values: 21 values in [0 _._ 001 _,_ 0 _._ 01], 21 values in [0 _._ 02 _,_ 0 _._ 1], and 21 values in [0 _._ 2 _,_ 1]. 

**Threshold-independent metrics.** We also report AUC and VUS-PR. In both cases, integration is performed using 250 quantiles of each method’s calibration score distribution. 

18 

Published as a conference paper at ICLR 2026 


![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0019-01.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0019-02.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0019-03.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0019-04.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0019-05.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0019-06.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0019-07.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0019-08.png)


Figure 6: Example signals (blue) with ground-truth anomaly labels (red areas), detected outliers (red dots) occur when adaptive _p_ -values (orange) fall below a threshold under our proposed _W_ 1-ACAS method. 

### C.2.3 ADDITIONAL RESULTS 

Figure 6 provides additional detection examples, while Figure 7 illustrates the trade-offs between FPR and F1 scores (PA-F1 and Affiliation-F) at the operating points that maximize the respective F1 metric, as defined in Appendix C.2.2. For PA-F1, _W_ 1-ACAS consistently dominates competing approaches. For Affiliation-F, _W_ 1-ACAS yields operating points that are rarely dominated and is the top-performing method in several datasets. 

19 

Published as a conference paper at ICLR 2026 


![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0020-01.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0020-02.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0020-03.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0020-04.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0020-05.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0020-06.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0020-07.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0020-08.png)


Figure 7: **Trade-offs between false positive rate and detection performance across datasets.** Left column: PA-F1 vs FPR (log scale). Right column: Affiliation-F vs FPR (log scale). Each point uses color for AD method and marker for forecast model. The operating points of _W_ 1-ACAS (blue), in most cases, achieve both the highest F1 score and lowest FPR, especially for PA-F1. Within the same TSFM model, _W_ 1-ACAS is better than the alternatives, and in general dominate most of the alternatives. 

**Hyperparameter Sensitivity.** Figure 8 examines the effect of aggregating different numbers of forecast horizons. Performance generally stabilizes once more than 10 horizons are included, with 

20 

Published as a conference paper at ICLR 2026 


![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0021-01.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0021-02.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0021-03.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0021-04.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0021-05.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0021-06.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0021-07.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0021-08.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0021-09.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0021-10.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0021-11.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0021-12.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0021-13.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0021-14.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0021-15.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0021-16.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0021-17.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0021-18.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0021-19.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0021-20.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0021-21.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0021-22.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0021-23.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0021-24.png)


Figure 8: Performance of _W_ 1-ACAS when aggregating different forecast steps. Rows correspond to datasets (NAB, NEK, MSL, YAHOO, Stock, WSD) and columns to metrics (PA-F1, Affiliation-F, AUC-PR, VUS-PR). 

limited gains beyond this point. Figure 9 shows the sensitivity of _W_ 1-ACAS to the learning rate _γ_ (with _αc_ = 0 _._ 01 and _nb_ = 10). Since the weights are updated using ADAM, _γ_ must remain sufficiently small; empirically, the method exhibits no significant variability for small learning rates. Figure 10 illustrates the effect of the batch size _nb_ (with _γ_ = 0 _._ 001 and _αc_ = 0 _._ 01). This parameter controls the number of samples used in the Wasserstein distance computation: if the distribution of nonconformity scores changes over time, _nb_ should not be too large. In practice, the method is only mildly sensitive to _nb_ , with smaller values performing slightly better on some datasets. Finally, Figure 11 examines the sensitivity to the critical alarm rate _αc_ . This parameter determines the maximum acceptable _p_ -value resolution: smaller values require a larger number of in-distribution past observations _nc_ for stable quantile estimation, but do not impose a lower bound on the smallest detectable anomaly level. 

**Per-dataset performance** Tables 2, 3, and 4 report per-dataset metrics, which align with and reinforce the trends discussed in the main Experimental section. Table 5 summarizes the forecasting performance of the TSFM models across datasets. Overall, the models exhibit broadly similar MAE/RMSE values, which aligns with their comparable anomaly-detection performance once fore- 

21 

Published as a conference paper at ICLR 2026 


![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0022-01.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0022-02.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0022-03.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0022-04.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0022-05.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0022-06.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0022-07.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0022-08.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0022-09.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0022-10.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0022-11.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0022-12.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0022-13.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0022-14.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0022-15.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0022-16.png)


Figure 9: Performance of _W_ 1-ACAS when aggregating different learning rate. Rows correspond to datasets (NAB, NEK, MSL, YAHOO, Stock, WSD) and columns to metrics (PA-F1, Affiliation-F, AUC-PR, VUS-PR). 

cast errors are properly calibrated online using _W_ 1-ACAS. Notably, the slightly higher forecasting error of TTM on YAHOO corresponds to its lower anomaly-detection performance in Table 2, suggesting a consistent relationship between forecast quality and downstream AD results. 

**Computation Time.** The average per-sample computation time of _W_ 1-ACAS with a 15-step forecast is 0.025 ± 0.012 seconds per sample per feature on a single V100 32 GB GPU. Note that this implementation updates weights for all 15 predictors serially, these updates are independent and can be parallelized to further reduce runtime. 

### C.2.4 EXTENSION TO MULTIVARIATE TIME SERIES ANOMALY DETECTION. 

_W_ 1 **-ACAS via** _p_ **-value aggregation.** . Lets consider a multivariate time series with features _fβ_ ¯<sup>_f_</sup> _∈t_ + 1[ _nf_ at time], we can run Algorithm 1 independently on each dimension to obtain per-feature _t_ + 1 (as defined in Eq. 15). These are then combined into a single anomaly score _p_ -values using standard _p_ -value combination methods Heard & Rubin-Delanchy (2018): 


![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0022-22.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0022-23.png)


We refer to these variants as _W_ 1-ACAS-F and _W_ 1-ACAS-H, respectively. 

**Experiments and Results.** We adopt the curated subsets from the TSB-AD benchmark (Liu & Paparrizos, 2024): TAO (Laboratory, 2024) (13 curated series, each with _∼_ 10k samples and 3 features, containing both sequential and point anomalies), GECCO (Rehbach et al., 2018) (a single long sequence with 9 features and over 138k samples), Genesis (von Birgelen & Niggemann, 2018) 

22 

Published as a conference paper at ICLR 2026 


![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0023-01.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0023-02.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0023-03.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0023-04.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0023-05.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0023-06.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0023-07.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0023-08.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0023-09.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0023-10.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0023-11.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0023-12.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0023-13.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0023-14.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0023-15.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0023-16.png)


Figure 10: Performance of _W_ 1-ACAS when aggregating different batch size update _nb_ . Rows correspond to datasets (NAB, NEK, MSL, YAHOO, Stock, WSD) and columns to metrics (PA-F1, Affiliation-F, AUC-PR, VUS-PR). 

(1 sequence with 18 features and over 16k samples), and LTDB (Goldberger et al., 2000) (5 curated sequences, each with 2 features and approximately 100k samples). 

We evaluate our multivariate extensions, _W_ 1-ACAS-F and _W_ 1-ACAS-H, combined with Chronos and TiRex forecasters that leverage all available historical context (up to their maximum context window, with a minimum of 52 past points). These are compared against strong semi-supervised deep anomaly detection baselines (Liu & Paparrizos, 2024): CNN (Munir et al., 2018), OmniAnomaly (Su et al., 2019), and USAD (Audibert et al., 2020), which benefit from being trained directly on non-anomalous segments. As reported in Table 6, both _W_ 1-ACAS-F and _W_ 1-ACAS-H achieve the best or highly competitive performance across all multivariate datasets, demonstrating the effectiveness of our _p_ -value aggregation extension in this setting. 

## D THE USE OF LARGE LANGUAGE MODELS (LLMS) 

We used large language models (LLMs) to assist with improving the readability and clarity of the manuscript. LLMs were used to improve and summarize the language in certain paragraphs, and to refine code for generating plots. 

23 

Published as a conference paper at ICLR 2026 


![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0024-01.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0024-02.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0024-03.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0024-04.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0024-05.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0024-06.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0024-07.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0024-08.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0024-09.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0024-10.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0024-11.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0024-12.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0024-13.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0024-14.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0024-15.png)



![](Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring_images/Adaptive_Conformal_Anomaly_Detection_with_Time_Series_Foundation_Models_for_Signal_Monitoring.pdf-0024-16.png)


Figure 11: Performance of _W_ 1-ACAS when aggregating different critical alarm rate _αc_ . Rows correspond to datasets (NAB, NEK, MSL, YAHOO, Stock, WSD) and columns to metrics (PA-F1, Affiliation-F, AUC-PR, VUS-PR). 

24 

Published as a conference paper at ICLR 2026 

|Dataset|Forecaster|AD Model|PA-F1_↑_|Affliation-F_↑_|FPR_↓_|CalErr_↓_|AUC-PR_↑_|VUC-PR_↑_|
|---|---|---|---|---|---|---|---|---|
|YAHOO|-|KShapeAD|0.523 ± 0.430|0.860 ± 0.151|0.359 ± 0.437|0.119 ± 0.183|0.036 ± 0.110|0.220 ± 0.225|
|YAHOO|-|POLY|0.102 ± 0.217|0.831 ± 0.126|0.387 ± 0.367|0.244 ± 0.240|0.037 ± 0.127|0.139 ± 0.125|
|YAHOO|-|Sub-KNN|0.161 ± 0.273|0.895 ± 0.109|0.158 ± 0.222|0.157 ± 0.161|0.016 ± 0.043|0.260 ± 0.197|
|YAHOO|-|Sub-PCA|0.112 ± 0.261|0.750 ± 0.115|0.677 ± 0.410|0.099 ± 0.163|0.056 ± 0.134|0.125 ± 0.199|
|YAHOO|-|SAND|0.398 ± 0.416|0.837 ± 0.147|0.409 ± 0.434|0.097 ± 0.114|0.024 ± 0.071|0.198 ± 0.180|
|YAHOO|-|CNN*|0.596 ± 0.438|0.853 ± 0.146|0.242 ± 0.407|0.240 ± 0.321|0.053 ± 0.147|0.160 ± 0.258|
|YAHOO|-|OmniAnomaly*|0.272 ± 0.381|0.791 ± 0.136|0.384 ± 0.446|0.313 ± 0.318|0.195 ± 0.255|0.351 ± 0.378|
|YAHOO|-|USAD*|0.113 ± 0.287|0.736 ± 0.098|0.610 ± 0.381|0.154 ± 0.187|0.068 ± 0.160|0.201 ± 0.288|
|YAHOO|-|MOMENT<br>~~Z~~S|0.134 ± 0.222|0.832 ± 0.121|0.215 ± 0.325|0.195 ± 0.193|0.086 ± 0.188|0.233 ± 0.235|
|YAHOO|Chronos|_W_1-ACAS|0.798 ± 0.323|0.947 ± 0.091|0.074 ± 0.253|0.007 ± 0.017|**0.330 ± 0.259**|0.679 ± 0.332|
|YAHOO|Chronos|conformal|0.652 ± 0.361|0.936 ± 0.091|0.088 ± 0.258|0.015 ± 0.028|0.147 ± 0.224|0.485 ± 0.347|
|YAHOO|Chronos|gaussian|0.317 ± 0.284|0.846 ± 0.098|0.123 ± 0.265|0.044 ± 0.066|0.028 ± 0.100|0.511 ± 0.345|
|YAHOO|Tirex|_W_1-ACAS|**0.869 ± 0.244**|**0.968 ± 0.068**|**0.069 ± 0.253**|**0.003 ± 0.007**|0.267 ± 0.280|**0.699 ± 0.331**|
|YAHOO|Tirex|conformal|0.730 ± 0.310|0.928 ± 0.091|0.074 ± 0.252|0.009 ± 0.015|0.176 ± 0.259|0.559 ± 0.317|
|YAHOO|Tirex|gaussian|0.302 ± 0.269|0.825 ± 0.101|0.105 ± 0.252|0.041 ± 0.062|0.030 ± 0.114|0.546 ± 0.310|
|YAHOO|TTM|_W_1-ACAS|0.651 ± 0.395|0.912 ± 0.121|0.141 ± 0.343|0.034 ± 0.057|0.277 ± 0.261|0.676 ± 0.324|
|YAHOO|TTM|conformal|0.607 ± 0.413|0.916 ± 0.108|0.113 ± 0.273|0.052 ± 0.082|0.172 ± 0.230|0.611 ± 0.350|
|YAHOO|TTM|gaussian|0.417 ± 0.334|0.870 ± 0.113|0.124 ± 0.276|0.050 ± 0.104|0.028 ± 0.099|0.560 ± 0.331|
|NEK|-|KShapeAD|0.602 ± 0.292|0.708 ± 0.043|0.807 ± 0.284|0.077 ± 0.118|0.216 ± 0.179|0.152 ± 0.138|
|NEK|-|POLY|0.848 ± 0.149|0.936 ± 0.066|0.073 ± 0.058|0.478 ± 0.135|0.063 ± 0.073|0.616 ± 0.162|
|NEK|-|Sub-KNN|0.738 ± 0.307|0.779 ± 0.098|0.561 ± 0.451|0.054 ± 0.086|0.172 ± 0.068|0.321 ± 0.131|
|NEK|-|Sub-PCA|0.933 ± 0.107|**0.980 ± 0.022**|0.041 ± 0.068|0.393 ± 0.190|0.007 ± 0.013|0.705 ± 0.230|
|NEK|-|SAND|0.718 ± 0.340|0.829 ± 0.105|0.312 ± 0.338|0.201 ± 0.135|0.325 ± 0.196|0.214 ± 0.203|
|NEK|-|CNN*|0.996 ± 0.006|0.965 ± 0.078|**0.000 ± 0.000**|0.859 ± 0.046|**0.438 ± 0.197**|0.730 ± 0.218|
|NEK|-|OmniAnomaly*|**0.998 ± 0.005**|0.968 ± 0.077|0.001 ± 0.001|0.875 ± 0.033|0.195 ± 0.189|**0.872 ± 0.132**|
|NEK|-|USAD*|0.785 ± 0.295|0.933 ± 0.058|0.179 ± 0.162|0.440 ± 0.124|0.006 ± 0.015|0.555 ± 0.174|
|NEK|-|MOMENT<br>~~Z~~S|0.849 ± 0.200|0.942 ± 0.028|0.125 ± 0.095|0.496 ± 0.165|0.046 ± 0.041|0.583 ± 0.138|
|NEK|Chronos|_W_1-ACAS|0.995 ± 0.006|0.924 ± 0.066|0.003 ± 0.005|**0.004 ± 0.003**|0.408 ± 0.073|0.447 ± 0.079|
|NEK|Chronos<br>|conformal<br>|0.979 ± 0.012<br>|0.934 ± 0.067<br>|0.007 ± 0.006<br>|0.007 ± 0.004<br>|0.418 ± 0.104<br>|0.490 ± 0.092<br>|
|NEK|Chronos|gaussian|0.890 ± 0.021|0.860 ± 0.069|0.047 ± 0.028|0.045 ± 0.025|0.347 ± 0.054|0.519 ± 0.093|
|NEK|Tirex|_W_1-ACAS|0.995 ± 0.006|0.927 ± 0.067|0.006 ± 0.015|0.005 ± 0.003|0.421 ± 0.063|0.453 ± 0.077|
|NEK|Tirex|conformal|0.971 ± 0.011|0.934 ± 0.066|0.011 ± 0.007|0.009 ± 0.004|0.421 ± 0.097|0.496 ± 0.097|
|NEK|Tirex|gaussian|0.890 ± 0.027|0.865 ± 0.064|0.044 ± 0.021|0.043 ± 0.021|0.354 ± 0.056|0.513 ± 0.099|
|NEK|TTM|_W_1-ACAS|0.993 ± 0.007|0.921 ± 0.065|0.004 ± 0.007|0.005 ± 0.003|0.384 ± 0.043|0.426 ± 0.043|
|NEK|TTM|conformal|0.977 ± 0.016|0.931 ± 0.067|0.008 ± 0.007|0.008 ± 0.005|0.417 ± 0.047|0.471 ± 0.057|
|NEK|TTM|gaussian|0.895 ± 0.012|0.871 ± 0.068|0.059 ± 0.045|0.040 ± 0.019|0.337 ± 0.060|0.501 ± 0.064|



Table 2: **Performance Summary per datasets.** Entries indicate the mean _±_ standard deviation computed by averaging within each dataset group. Higher numbers are better for PA-F1, AffiliationF, AUC-PR, VUS-PR; lower numbers are better for FPR, and calibration error (CalErr). Methods marked with * denote deep learning semi-supervised approaches; the best overall method is shown in **bold** , and the best non–semi-supervised method is underlined when different from the bold one. 

25 

Published as a conference paper at ICLR 2026 

|Dataset|Forecaster|AD Model|PA-F1_↑_|Affliation-F_↑_|FPR_↓_|CalErr_↓_|AUC-PR_↑_|VUC-PR_↑_|
|---|---|---|---|---|---|---|---|---|
|MSL|-|KShapeAD|0.854 ± 0.207|0.915 ± 0.113|0.116 ± 0.154|0.188 ± 0.131|0.108 ± 0.119|0.260 ± 0.163|
|MSL|-|POLY|0.619 ± 0.330|0.881 ± 0.114|0.248 ± 0.339|0.076 ± 0.108|0.077 ± 0.106|0.353 ± 0.187|
|MSL|-|Sub-KNN|0.685 ± 0.379|0.835 ± 0.124|0.293 ± 0.411|0.137 ± 0.099|0.132 ± 0.164|0.179 ± 0.153|
|MSL|-|Sub-PCA|0.683 ± 0.354|0.882 ± 0.110|0.175 ± 0.248|0.145 ± 0.185|0.056 ± 0.071|0.371 ± 0.329|
|MSL|-|SAND|0.655 ± 0.328|0.877 ± 0.122|0.242 ± 0.251|0.176 ± 0.153|0.064 ± 0.068|0.303 ± 0.179|
|MSL|-|CNN*|0.826 ± 0.225|0.885 ± 0.099|0.096 ± 0.217|0.460 ± 0.407|0.105 ± 0.105|0.308 ± 0.264|
|MSL|-|OmniAnomaly*|0.818 ± 0.257|0.879 ± 0.106|0.038 ± 0.063|0.588 ± 0.409|0.121 ± 0.133|0.344 ± 0.262|
|MSL|-|USAD*|0.667 ± 0.349|0.881 ± 0.108|0.133 ± 0.197|0.384 ± 0.288|0.060 ± 0.095|0.415 ± 0.389|
|MSL|-|MOMENT<br>~~Z~~S|0.799 ± 0.300|**0.905 ± 0.128**|0.151 ± 0.375|0.429 ± 0.328|0.134 ± 0.093|**0.501 ± 0.290**|
|MSL|Chronos|_W_1-ACAS|**0.928 ± 0.104**|0.876 ± 0.115|0.033 ± 0.062|0.022 ± 0.027|0.282 ± 0.127|0.400 ± 0.050|
|MSL|Chronos|conformal|0.829 ± 0.318|0.813 ± 0.122|0.310 ± 0.472|0.159 ± 0.370|0.308 ± 0.159|0.306 ± 0.175|
|MSL|Chronos|gaussian|0.854 ± 0.126|0.842 ± 0.101|0.180 ± 0.363|0.074 ± 0.151|0.262 ± 0.124|0.368 ± 0.157|
|MSL|Tirex|_W_1-ACAS|0.905 ± 0.113|0.888 ± 0.113|0.152 ± 0.374|**0.017 ± 0.020**|0.225 ± 0.158|0.380 ± 0.062|
|MSL|Tirex|conformal|0.826 ± 0.315|0.816 ± 0.121|0.312 ± 0.471|0.158 ± 0.371|0.226 ± 0.160|0.299 ± 0.171|
|MSL|Tirex|gaussian|0.856 ± 0.124|0.841 ± 0.100|0.187 ± 0.362|0.131 ± 0.182|0.267 ± 0.118|0.378 ± 0.170|
|MSL|TTM|_W_1-ACAS|0.901 ± 0.114|0.879 ± 0.113|**0.023 ± 0.039**|**0.017 ± 0.026**|0.227 ± 0.157|0.396 ± 0.056|
|MSL|TTM|conformal|0.803 ± 0.308|0.812 ± 0.120|0.319 ± 0.467|0.165 ± 0.368|0.243 ± 0.196|0.396 ± 0.181|
|MSL|TTM|gaussian|0.855 ± 0.118|0.849 ± 0.104|0.180 ± 0.364|0.074 ± 0.133|0.286 ± 0.174|0.416 ± 0.122|
|NAB|-|KShapeAD|0.835 ± 0.222|0.833 ± 0.141|0.341 ± 0.424|0.195 ± 0.250|0.123 ± 0.162|0.272 ± 0.220|
|NAB|-|POLY|0.863 ± 0.203|0.900 ± 0.109|0.136 ± 0.251|0.232 ± 0.248|0.087 ± 0.073|0.322 ± 0.189|
|NAB|-|Sub-KNN|0.810 ± 0.257|0.819 ± 0.124|0.272 ± 0.383|0.273 ± 0.318|0.153 ± 0.150|0.304 ± 0.283|
|NAB|-|Sub-PCA|0.905 ± 0.185|0.923 ± 0.100|0.082 ± 0.223|0.341 ± 0.320|0.199 ± 0.245|0.427 ± 0.286|
|NAB|-|SAND|0.785 ± 0.245|0.809 ± 0.130|0.340 ± 0.422|0.151 ± 0.140|0.130 ± 0.131|0.296 ± 0.207|
|NAB|-|CNN*|0.982 ± 0.054|**0.937 ± 0.077**|**0.008 ± 0.034**|0.468 ± 0.420|0.194 ± 0.115|0.260 ± 0.146|
|NAB|-|OmniAnomaly*|0.977 ± 0.082|0.925 ± 0.091|0.068 ± 0.231|0.506 ± 0.366|0.201 ± 0.071|0.274 ± 0.139|
|NAB|-|USAD*|0.927 ± 0.139|0.926 ± 0.101|0.123 ± 0.263|0.473 ± 0.314|0.200 ± 0.206|**0.445 ± 0.237**|
|NAB|-|MOMENT<br>~~Z~~S|0.958 ± 0.115|0.931 ± 0.103|0.129 ± 0.315|0.490 ± 0.341|0.220 ± 0.218|0.407 ± 0.216|
|NAB|Chronos|_W_1-ACAS|0.983 ± 0.044|0.855 ± 0.092|0.054 ± 0.208|0.012 ± 0.028|0.205 ± 0.089|0.224 ± 0.101|
|NAB<br>|Chronos<br>|conformal<br>|0.978 ± 0.057<br>|0.880 ± 0.089<br>|0.048 ± 0.208<br>|0.013 ± 0.011<br>|0.205 ± 0.094<br>|0.232 ± 0.108<br>|
|NAB|Chronos|gaussian|0.941 ± 0.051|0.800 ± 0.103|0.149 ± 0.328|0.077 ± 0.097|0.201 ± 0.094|0.223 ± 0.098|
|NAB|Tirex|_W_1-ACAS|**0.985 ± 0.030**|0.851 ± 0.095|0.049 ± 0.208|0.011 ± 0.027|0.201 ± 0.087|0.217 ± 0.088|
|NAB|Tirex|conformal|0.977 ± 0.057|0.876 ± 0.090|0.052 ± 0.207|0.012 ± 0.017|0.201 ± 0.097|0.228 ± 0.096|
|NAB|Tirex|gaussian|0.935 ± 0.059|0.792 ± 0.095|0.154 ± 0.331|0.085 ± 0.105|0.195 ± 0.097|0.218 ± 0.086|
|NAB|TTM|_W_1-ACAS|0.980 ± 0.057|0.858 ± 0.093|0.050 ± 0.207|**0.010 ± 0.019**|**0.220 ± 0.110**|0.225 ± 0.118|
|NAB|TTM|conformal|0.976 ± 0.058|0.881 ± 0.087|0.050 ± 0.207|0.008 ± 0.011|0.217 ± 0.115|0.231 ± 0.125|
|NAB|TTM|gaussian|0.945 ± 0.064|0.815 ± 0.103|0.140 ± 0.310|0.078 ± 0.109|0.203 ± 0.104|0.235 ± 0.124|



Table 3: **Performance Summary per datasets.** Entries indicate the mean _±_ standard deviation computed by averaging within each dataset group. Higher numbers are better for PA-F1, AffiliationF, AUC-PR, VUS-PR; lower numbers are better for FPR, and calibration error (CalErr). Methods marked with * denote deep learning semi-supervised approaches; the best overall method is shown in **bold** , and the best non–semi-supervised method is underlined when different from the bold one. 

26 

Published as a conference paper at ICLR 2026 

|Dataset|Forecaster|AD Model|PA-F1_↑_|Affliation-F_↑_|FPR_↓_|CalErr_↓_|AUC-PR_↑_|VUC-PR_↑_|
|---|---|---|---|---|---|---|---|---|
|WSD|-|KShapeAD|0.117 ± 0.210|0.722 ± 0.084|0.469 ± 0.361|0.162 ± 0.133|0.011 ± 0.023|0.061 ± 0.116|
|WSD|-|POLY|0.475 ± 0.337|0.862 ± 0.138|0.199 ± 0.333|0.281 ± 0.240|0.006 ± 0.010|0.226 ± 0.223|
|WSD|-|Sub-KNN|0.195 ± 0.237|0.755 ± 0.088|0.312 ± 0.422|0.054 ± 0.071|0.026 ± 0.066|0.103 ± 0.135|
|WSD|-|Sub-PCA|0.208 ± 0.296|0.747 ± 0.093|0.479 ± 0.393|0.205 ± 0.212|0.040 ± 0.110|0.102 ± 0.135|
|WSD|-|CNN*|**0.980 ± 0.038**|**0.970 ± 0.061**|**0.001 ± 0.001**|0.712 ± 0.287|0.033 ± 0.035|0.216 ± 0.200|
|WSD|-|OmniAnomaly*|0.414 ± 0.431|0.804 ± 0.134|0.471 ± 0.470|0.328 ± 0.353|0.047 ± 0.116|0.090 ± 0.116|
|WSD|-|USAD*|0.102 ± 0.210|0.711 ± 0.061|0.602 ± 0.335|0.269 ± 0.209|0.009 ± 0.011|0.041 ± 0.059|
|WSD|-|MOMENT<br>~~Z~~S|0.568 ± 0.238|0.944 ± 0.078|0.059 ± 0.194|0.504 ± 0.284|0.030 ± 0.061|**0.394 ± 0.248**|
|WSD|Chronos|_W_1-ACAS|0.868 ± 0.175|0.890 ± 0.096|0.096 ± 0.292|0.007 ± 0.016|0.224 ± 0.192|0.230 ± 0.226|
|WSD|Chronos|conformal|0.810 ± 0.193|0.882 ± 0.086|0.098 ± 0.292|0.006 ± 0.009|0.105 ± 0.120|0.227 ± 0.172|
|WSD|Chronos|gaussian|0.387 ± 0.207|0.788 ± 0.072|0.111 ± 0.283|0.025 ± 0.025|0.079 ± 0.085|0.226 ± 0.173|
|WSD|Tirex|_W_1-ACAS|0.882 ± 0.159|0.891 ± 0.090|0.048 ± 0.210|0.007 ± 0.022|0.222 ± 0.190|0.239 ± 0.228|
|WSD<br>|Tirex<br>|conformal<br>|0.841 ± 0.173<br>|0.886 ± 0.087<br>|0.052 ± 0.222<br>|0.006 ± 0.006<br>|0.119 ± 0.115<br>|0.238 ± 0.208<br>|
|WSD|Tirex|gaussian|0.393 ± 0.210|0.783 ± 0.074|0.110 ± 0.283|0.023 ± 0.023|0.067 ± 0.074|0.231 ± 0.202|
|WSD|TTM|_W_1-ACAS|0.868 ± 0.172|0.882 ± 0.089|0.064 ± 0.228|**0.005 ± 0.012**|**0.225 ± 0.198**|0.236 ± 0.229|
|WSD<br>|TTM<br>|conformal<br>|0.812 ± 0.174<br>|0.879 ± 0.084<br>|0.067 ± 0.229<br>|0.007 ± 0.006<br>|0.191 ± 0.146<br>|0.237 ± 0.194<br>|
|WSD|TTM|gaussian|0.389 ± 0.212|0.782 ± 0.076|0.112 ± 0.292|0.026 ± 0.032|0.063 ± 0.066|0.230 ± 0.196|
|Stock|-|KShapeAD|0.135 ± 0.072|0.680 ± 0.010|0.951 ± 0.095|0.081 ± 0.060|0.060 ± 0.036|0.603 ± 0.342|
|Stock|-|POLY|0.201 ± 0.089|0.720 ± 0.082|0.805 ± 0.360|0.245 ± 0.248|0.000 ± 0.000|0.615 ± 0.350|
|Stock<br>|-|Sub-KNN<br>|0.150 ± 0.087<br>|0.678 ± 0.008<br>|0.979 ± 0.027<br>|0.175 ± 0.136<br>|0.083 ± 0.067<br>|0.627 ± 0.369<br>|
|Stock|-|Sub-PCA|0.199 ± 0.086|0.726 ± 0.090|0.792 ± 0.335|0.128 ± 0.199|0.117 ± 0.068|0.844 ± 0.087|
|Stock|-|SAND|0.174 ± 0.100|0.687 ± 0.001|0.933 ± 0.086|0.137 ± 0.192|0.071 ± 0.027|0.549 ± 0.549|
|Stock|-|CNN*|**0.996 ± 0.003**|**0.999 ± 0.001**|**0.001 ± 0.000**|0.872 ± 0.066|0.900 ± 0.105|0.980 ± 0.027|
|Stock|-|OmniAnomaly*|0.372 ± 0.038|0.886 ± 0.046|0.242 ± 0.122|0.688 ± 0.160|0.284 ± 0.054|0.962 ± 0.026|
|Stock|-|USAD*|0.146 ± 0.070|0.676 ± 0.008|0.983 ± 0.019|**0.021 ± 0.027**|0.068 ± 0.043|0.747 ± 0.149|
|Stock|-|MOMENT<br>~~Z~~S|0.163 ± 0.071|0.680 ± 0.006|0.931 ± 0.045|0.049 ± 0.024|0.093 ± 0.051|0.598 ± 0.365|
|Stock|Chronos|_W_1-ACAS|0.959 ± 0.031|0.985 ± 0.008|0.009 ± 0.012|0.074 ± 0.040|0.973 ± 0.020|**0.998 ± 0.001**|
|Stock|Chronos|conformal|0.959 ± 0.039|0.990 ± 0.009|0.009 ± 0.010|0.072 ± 0.043|0.841 ± 0.151|0.968 ± 0.034|
|Stock|Chronos|gaussian|0.958 ± 0.037|0.990 ± 0.008|0.006 ± 0.007|0.175 ± 0.081|0.799 ± 0.197|0.974 ± 0.027|
|Stock|Tirex|_W_1-ACAS|0.955 ± 0.027|0.983 ± 0.008|0.010 ± 0.009|0.072 ± 0.043|**0.984 ± 0.010**|0.985 ± 0.024|
|Stock<br>|Tirex<br>|conformal<br>|0.947 ± 0.039<br>|0.985 ± 0.006<br>|0.010 ± 0.007<br>|0.079 ± 0.047<br>|0.880 ± 0.104<br>|0.987 ± 0.017<br>|
|Stock|Tirex|gaussian|0.964 ± 0.034|0.989 ± 0.007|0.006 ± 0.005|0.179 ± 0.084|0.855 ± 0.133|0.986 ± 0.018|
|Stock|TTM|_W_1-ACAS|0.967 ± 0.028|0.989 ± 0.008|0.009 ± 0.011|0.074 ± 0.041|0.963 ± 0.053|0.991 ± 0.015|
|Stock|TTM|conformal|0.963 ± 0.030|0.989 ± 0.007|0.008 ± 0.009|0.071 ± 0.046|0.825 ± 0.184|0.975 ± 0.031|
|Stock|TTM|gaussian|0.965 ± 0.018|0.988 ± 0.005|0.004 ± 0.004|0.182 ± 0.087|0.818 ± 0.164|0.974 ± 0.028|
|IOPS|-|KShapeAD|0.365 ± 0.358|0.703 ± 0.064|0.699 ± 0.337|0.171 ± 0.149|0.025 ± 0.028|0.049 ± 0.044|
|IOPS|-|POLY|0.493 ± 0.410|0.854 ± 0.113|0.214 ± 0.318|0.442 ± 0.308|0.042 ± 0.067|0.230 ± 0.121|
|IOPS|-|Sub-KNN|0.334 ± 0.342|0.695 ± 0.038|0.693 ± 0.378|0.137 ± 0.187|0.021 ± 0.029|0.073 ± 0.095|
|IOPS<br>|-|Sub-PCA<br>|0.497 ± 0.432<br>|0.780 ± 0.112<br>|0.360 ± 0.341<br>|0.352 ± 0.236<br>|0.059 ± 0.070<br>|0.206 ± 0.158<br>|
|IOPS|-|SAND|0.052 ± 0.038|0.703 ± 0.039|0.808 ± 0.196|0.091 ± 0.056|0.008 ± 0.004|0.082 ± 0.055|
|IOPS|-|CNN*|0.865 ± 0.224|0.870 ± 0.091|0.018 ± 0.040|0.800 ± 0.271|0.102 ± 0.071|0.285 ± 0.165|
|IOPS|-|OmniAnomaly*|0.734 ± 0.275|0.803 ± 0.113|0.161 ± 0.261|0.639 ± 0.286|0.044 ± 0.038|0.207 ± 0.129|
|IOPS<br>|-|USAD*<br><br>|0.493 ± 0.348<br>|0.771 ± 0.113<br>|0.387 ± 0.314<br>|0.402 ± 0.278<br>|0.041 ± 0.044<br>|0.130 ± 0.077<br>|
|IOPS|-|MOMENT<br>~~Z~~S|0.565 ± 0.347|0.870 ± 0.098|0.074 ± 0.124|0.665 ± 0.293|0.052 ± 0.060|**0.337 ± 0.261**|
|IOPS|Chronos|_W_1-ACAS|0.886 ± 0.147|0.882 ± 0.062|0.004 ± 0.008|**0.005 ± 0.014**|0.158 ± 0.143|0.291 ± 0.151|
|IOPS|Chronos|conformal|0.850 ± 0.175|0.884 ± 0.067|0.008 ± 0.013|0.006 ± 0.013|0.151 ± 0.160|0.298 ± 0.208|
|IOPS|Chronos|gaussian|0.543 ± 0.217|0.811 ± 0.035|0.024 ± 0.019|0.021 ± 0.020|0.109 ± 0.087|0.308 ± 0.208|
|IOPS|Tirex|_W_1-ACAS|**0.921 ± 0.073**|**0.889 ± 0.061**|**0.003 ± 0.007**|0.007 ± 0.014|**0.184 ± 0.144**|0.296 ± 0.167|
|IOPS|Tirex|conformal|0.875 ± 0.126|0.888 ± 0.061|0.007 ± 0.013|0.006 ± 0.012|0.151 ± 0.140|0.301 ± 0.207|
|IOPS|Tirex|gaussian|0.528 ± 0.232|0.800 ± 0.035|0.026 ± 0.020|0.023 ± 0.019|0.113 ± 0.089|0.304 ± 0.207|
|IOPS<br>IOPS|TTM<br>TTM|_W_1-ACAS<br>conformal|0.871 ± 0.203<br>0826 ± 0212|0.870 ± 0.075<br>0875 ± 0084|0.009 ± 0.029<br>0019 ± 0050|**0.005 ± 0.012**<br>0007 ± 0013|0.167 ± 0.136<br>0123 ± 0102|0.304 ± 0.153<br>0313 ± 0224|
|IOPS|TTM|gaussian|.  .<br>0.558 ± 0.228|.  .<br>0.809 ± 0.045|.  .<br>0.032 ± 0.048|.  .<br>0.021 ± 0.024|.  .<br>0.109 ± 0.092|.  .<br>0.309 ± 0.215|



Table 4: **Performance Summary per datasets.** Entries indicate the mean _±_ standard deviation computed by averaging within each dataset group. Higher numbers are better for PA-F1, AffiliationF, AUC-PR, VUS-PR; lower numbers are better for FPR, and calibration error (CalErr). Methods marked with * denote deep learning semi-supervised approaches; the best overall method is shown in **bold** , and the best non–semi-supervised method is underlined when different from the bold one. 

27 

Published as a conference paper at ICLR 2026 

|Dataset<br>Forecaster|IOPS|MSL|NAB|NEK|Stock|WSD|YAHOO|
|---|---|---|---|---|---|---|---|
|MAE||||||||
|Chronos|1.50_±_1.83|0.06_±_0.06|244.96_±_1108.10|0.38_±_0.21|6.81_±_3.89|149.73_±_200.81|280.75_±_232.69|
|TiRex|1.45_±_1.77|0.06_±_0.05|234.95_±_1063.39|0.37_±_0.22|6.85_±_4.00|138.51_±_182.07|250.80_±_220.62|
|TTM|1.45_±_1.74|0.09_±_0.07|267.97_±_1219.00|0.59_±_0.41|7.59_±_4.74|139.11_±_183.01|481.91_±_252.17|
|RMSE||||||||
|Chronos|2.38_±_2.87|0.20_±_0.19|341.38_±_1487.54|0.75_±_0.38|15.33_±_9.43|212.32_±_286.53|461.99_±_433.56|
|TiRex|2.31_±_2.78|0.20_±_0.19|326.81_±_1426.95|0.75_±_0.39|15.40_±_9.53|198.23_±_261.90|417.93_±_411.42|
|TTM|2.30_±_2.74|0.22_±_0.21|373.15_±_1654.63|0.94_±_0.54|15.37_±_9.53|196.56_±_262.49|683.50_±_429.53|



Table 5: **TSFM Forecasting Performance (MAE and RMSE) per Multivariate Dataset.** Mean Absolute Error and Root Mean Squared Error for each TSFM model on the anomaly detection datasets, computed using a 15-step-ahead forecast and a context length of 52 past observations. Entries report mean _±_ standard deviation across all series within each dataset. Overall, forecasting performance is similar across models; the slightly higher error of TTM on YAHOO aligns with its correspondingly lower AD performance in Table 2. 

|Dataset|Forecaster|AD Model|PA-F1_↑_|Affliation-F_↑_|FPR_↓_|CalErr_↓_|AUC-PR_↑_|VUC-PR_↑_|
|---|---|---|---|---|---|---|---|---|
|TAO|-|CNN*|0.998 ± 0.001|0.999 ± 0.000|**0.000 ± 0.000**|0.612 ± 0.044|0.895 ± 0.094|0.999 ± 0.001|
|TAO|-|OmniAnomaly*|0.377 ± 0.021|0.863 ± 0.053|0.321 ± 0.153|0.497 ± 0.136|0.311 ± 0.039|0.940 ± 0.051|
|TAO|-|USAD*|0.172 ± 0.061|0.679 ± 0.006|0.986 ± 0.018|0.033 ± 0.027|0.018 ± 0.005|0.097 ± 0.017|
|TAO<br>TAO|Chronos<br>allctx<br>Chronos<br>allctx|_W_1-ACAS-F<br>_W_1-ACAS-H|**1.000 ± 0.000**<br>0.999 ± 0.001|**1.000 ± 0.000**<br>**1.000 ± 0.000**|**0.000 ± 0.000**<br>**0.000 ± 0.000**|0.029 ± 0.028<br>0.251 ± 0.110|0.901 ± 0.085<br>**0.945 ± 0.047**|0.998 ± 0.003<br>0.999 ± 0.001|
|TAO<br>TAO|Tirex<br>~~a~~llctx<br>Tirex-allctx|_W_1-ACAS-F<br>_W_1-ACAS-H|**1.000 ± 0.000**<br>0.999 ± 0.000|**1.000 ± 0.000**<br>**1.000 ± 0.000**|**0.000 ± 0.000**<br>**0.000 ± 0.000**|**0.026 ± 0.023**<br>0.257 ± 0.109|0.907 ± 0.100<br>0.938 ± 0.060|**1.000 ± 0.001**<br>0.998 ± 0.003|
|GECCO|-|CNN*|0.583|0.875|0.139|0.860|**0.294**|0.152|
|GECCO|-|OmniAnomaly*|0.579|0.840|0.206|0.792|0.216|0.186|
|GECCO|-|USAD*|0.561|0.772|0.353|0.643|0.038|0.091|
|GECCO|Chronos-allctx|_W_1-ACAS-F|0.704|**0.882**|**0.030**|**0.014**|0.231|0.236|
|GECCO|Chronos-allctx|_W_1-ACAS-H|0.606|0.835|0.044|0.316|0.110|0.127|
|GECCO|Tirex-allctx|_W_1-ACAS-F|**0.742**|0.864|0.034|0.026|0.237|**0.241**|
|GECCO|Tirex-allctx|_W_1-ACAS-H|0.587|0.842|0.039|0.320|0.124|0.136|
|LTDB|-|CNN*|0.910 ± 0.137|**0.837 ± 0.105**|0.228 ± 0.404|0.657 ± 0.368|**0.247 ± 0.191**|0.343 ± 0.272|
|LTDB|-|OmniAnomaly*|0.875 ± 0.184|0.830 ± 0.106|0.297 ± 0.471|0.511 ± 0.445|0.211 ± 0.176|0.272 ± 0.204|
|LTDB|-|USAD*|0.639 ± 0.380|0.866 ± 0.126|0.280 ± 0.481|0.540 ± 0.363|0.178 ± 0.277|**0.453 ± 0.385**|
|LTDB|Chronos-allctx|_W_1-ACAS-F|0.845 ± 0.142|0.792 ± 0.056|0.065 ± 0.054|0.038 ± 0.039|0.227 ± 0.161|0.265 ± 0.187|
|LTDB|Chronos-allctx|_W_1-ACAS-H|0.910 ± 0.054|0.816 ± 0.024|0.068 ± 0.070|0.162 ± 0.119|0.170 ± 0.116|0.263 ± 0.185|
|LTDB|Tirex-allctx|_W_1-ACAS-F|0.888 ± 0.101|0.814 ± 0.096|**0.047 ± 0.050**|**0.026 ± 0.029**|0.227 ± 0.157|0.260 ± 0.183|
|LTDB|Tirex-allctx|_W_1-ACAS-H|**0.937 ± 0.041**|0.829 ± 0.067|0.060 ± 0.067|0.134 ± 0.108|0.171 ± 0.114|0.263 ± 0.181|
|Genesis|-|CNN*|0.649|0.852|0.004|0.896|0.031|0.045|
|Genesis|-|OmniAnomaly*|0.473|0.873|0.009|0.784|0.018|0.028|
|Genesis|-|USAD*|0.094|0.864|0.088|0.272|0.031|**0.074**|
|Genesis|Chronos-allctx|_W_1-ACAS-F|0.793|0.891|**0.002**|0.001|0.075|0.066|
|Genesis|Chronos-allctx|_W_1-ACAS-H|0.850|0.903|**0.002**|0.058|**0.084**|0.066|
|Genesis|Tirex-allctx|_W_1-ACAS-F|0.850|**0.912**|**0.002**|**0.000**|0.039|0.029|
|Genesis|Tirex-allctx|_W_1-ACAS-H|**0.873**|0.897|0.004|0.116|0.058|0.046|



Table 6: **Performance Summary per Multivariate Dataset.** Entries indicate the mean _±_ standard deviation computed by averaging within each dataset group. Higher numbers are better for PA-F1, Affiliation-F, AUC-PR, VUS-PR; lower numbers are better for FPR, and calibration error (CalErr). Standard deviations are omitted for GECCO and Genesis, as each corresponds to a single multivariate time series (9 features, 138k samples for GECCO; 18 features, 16k samples for Genesis). Methods marked with * denote deep learning semi-supervised approaches; the best overall method is shown in **bold** . 

28 

