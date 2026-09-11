# **Between Resolution Collapse and Variance Inflation: Weighted Conformal Anomaly Detection in Low-Data Regimes** 

### **Oliver Hennhöfer**<sup>1</sup> 

### **Christine Preisach**<sup>1</sup> 

1Intelligent Systems Research Group (ISRG), Karlsruhe University of Applied Sciences, Germany 

## **Abstract** 

Standard conformal anomaly detection provides marginal finite-sample guarantees under the assumption of exchangeability . However, real-world data often exhibit distribution shifts, necessitating a weighted conformal approach to adapt to local nonstationarity. We show that this adaptation induces a critical trade-off between the minimum attainable _p_ -value and its stability. As importance weights localize to relevant calibration instances, the effective sample size decreases. This can render standard conformal _p_ -values overly conservative for effective error control, while the smoothing technique used to mitigate this issue introduces conditional variance, potentially masking anomalies. We propose a continuous inference relaxation that resolves this dilemma by decoupling local adaptation from tail resolution via continuous weighted kernel density estimation. While relaxing finite-sample exactness to asymptotic validity, our method eliminates Monte Carlo variability and recovers the statistical power lost to discretization. Empirical evaluations confirm that our approach not only restores detection capabilities where discrete baselines yield zero discoveries, but outperforms standard methods in statistical power while maintaining valid marginal error control in practice. 

## **1 INTRODUCTION** 

Anomaly detection aims to identify observations that deviate significantly from the majority of observations or do otherwise not _conform_ to an expected state of normality, indicating a distinct underlying data-generating mechanism at work Hawkins [1980]. Yet, standard detection approaches often lack statistical guarantees regarding the false alarm rate, which is problematic in safety-critical applications. 

Conformal Anomaly Detection (CAD) addresses this by offering a distribution-free framework to transform heuristic anomaly scores into valid _p_ -values, enabling False Discovery Rate (FDR) control procedures Bates et al. [2023]. 

Conformal validity assumes data exchangeability. In dynamic environments where the data distribution shifts over time, this assumption is violated. Weighted conformal approaches mitigate distribution shift by assigning higher importance to calibration samples resembling current test instances via likelihood ratios ( _covariate shift adaptation_ ). This localization induces a critical dilemma. As weights concentrate on a smaller effective sample size, empirical _p_ -values become discretely coarse, leading to _resolution collapse_ , where the minimum _p_ -value fails to meet the discovery threshold required for e.g. the Benjamini–Hochberg (BH) procedure Benjamini and Hochberg [1995]. 

While standard conformal theory proposes _randomized smoothing_ to resolve this granularity Jin and Candès [2025], we demonstrate that this theoretical fix comes at a practical cost in weighted regimes. When a test point is assigned a large weight (common under shift), smoothing introduces significant uniform noise to maintain exact validity. We show that this _variance inflation_ decreases the signal-tonoise ratio and degrades statistical power. Consequently, practitioners are (at worst) trapped between the zero power of the discrete estimator (due to inflated minimum attainable _p_ -values) and low statistical efficiency of the randomized estimator (due to noise masking). 

In this work, we address this conflict between local adaptation, resolution, and stability. Our contributions are: 

- **The Resolution–Variance Dilemma:** We formalize two failure modes of weighted CAD. As weight localization strength under covariate shift adaptation increases, the standard weighted conformal _p_ -value method exhibits lower-bound _p_ -values ( _resolution collapse_ ), while the randomized variant shows rejection inconsistency ( _variance inflation_ ). Both can severely reduce statistical power, particularly in low-data regimes. 

- **Stabilized Continuous Inference:** We propose a continuous inference relaxation that decouples local adaptation from tail resolution via continuous weighted kernel density estimation. This approach eliminates the lower _p_ -value bound without introducing the same degree of Monte Carlo noise of the randomized approach. 

- **Empirical Validation:** We demonstrate that our approach restores detection capabilities in pathological regimes where discrete baselines yield zero discoveries, and significantly outperforms randomized baselines in statistical power by mitigating variance, all while maintaining valid marginal error control. 

## **2 PRIOR WORKS** 

Conformal prediction under covariate shift was established by Tibshirani et al. [2019], introducing the weighted exchangeability framework to correct for distribution shifts using importance weights ( _Radon–Nikodým_ ). For CAD under covariate shift, Jin and Candès [2025] extended this to multiple testing via _Weighted Conformalized Selection_ (WCS), necessitated by the failure of weighted conformal _p_ -values to satisfy Positive Regression Dependence on a Subset (PRDS), under which BH guarantees FDR control. 

## **3 PRELIMINARIES** 

We consider the unsupervised anomaly detection setting. Let _D_ cal = _{z_ 1 _, . . . , zN }_ be a calibration set of _N_ observations drawn from a training distribution _P_ . We evaluate a test batch _Z_ test = _{zN_ +1 _, . . . , zN_ + _m}_ of _m_ instances drawn from a (possibly shifted) distribution _Q_ . We fit a scoring function _s_ : _Z →_ R on _P_ , where larger scores indicate greater deviation from normality. Let _si_ = _s_ ( _zi_ ) denote the score for the _i_ -th calibration observation, _i ∈{_ 1 _, . . . , N }_ . 

### **3.1 WEIGHTED CONFORMAL ANOMALY DETECTION** 

Standard conformal prediction assumes exchangeability between calibration and test data ( _P_ = _Q_ ). To accommodate covariate shift, we employ the weighted conformal framework Tibshirani et al. [2019], which reweighs observations by the likelihood ratio _w_ ( _z_ ) = _dQ/dP_ ( _z_ ) as estimated by a density estimator, see Section 5.1. 

There are two standard approaches to constructing the weighted _p_ -value for a test point _zj_ with score _sj_ : 

**1. The Deterministic Estimator.** The standard discrete _p_ -value is conservative and includes the test point weight _wj_ in the numerator to ensure validity without randomization: 


![](Between_Resolution_Collapse_and_Variance_Inflation-_Weighted_Conformal_Anomaly_Detection_in_Low-Data_Regimes_images/conv_df19cafceda30860.pdf-0002-10.png)


This guarantees marginal super-uniformity P� _p_<sup>disc</sup> _j ≤ α_ � _≤ α, ∀α ∈_ [0 _,_ 1], with a minimum attainable _p_ -value _p_<sup>disc</sup> _j_ =<sup>_wj_</sup> _/_<sup>�</sup> _i_<sup>_N_</sup> =1<sup>_wi_+</sup><sup>_wj_, even if</sup><sup>_sj→∞_.</sup> 

**2. The Randomized Estimator.** To remove discretization effects, weighted conformal _p_ -values introduce auxiliary randomness _Uj ∼_ Unif[0 _,_ 1] as in Jin and Candès [2025]. In the unweighted exchangeable setting ( _w ≡_ 1), the standard randomized conformal _p_ -value is (marginally) valid and, under continuity/no-ties conditions, is exactly Unif[0 _,_ 1] under the null. In the weighted covariate-shift setting, the same randomized construction yields marginal super-uniformity: 


![](Between_Resolution_Collapse_and_Variance_Inflation-_Weighted_Conformal_Anomaly_Detection_in_Low-Data_Regimes_images/conv_df19cafceda30860.pdf-0002-13.png)


The randomization spreads the mass of the test point’s own weight _wj_ , together with any calibration mass tied at _sj_ , uniformly over an interval. Hence, even if there are no calibration ties (e.g., for extreme scores outside the calibration range), the term _Ujwj_ randomizes _p_<sup>rand</sup> _j_ . If the scores are continuous (so that<sup>�</sup> _i_<sup>_wi_I(</sup><sup>_si_=</sup><sup>_sj_)=0), (2) reduces to</sup> the simpler expression with _Ujwj_ . In all cases, the smoothed estimator can take values arbitrarily close to zero, eliminating the lower _p_ -value bound of the deterministic estimator. 

### **3.2 FALSE DISCOVERY RATE CONTROL** 

For the batch _Z_ test, we test _m_ null hypotheses _H_ 0 _,j_ : _zj_ is an inlier and aim to control the FDR at level _α_ . 

**Multiple Testing.** In the unweighted setting ( _w ≡_ 1), we apply the BH procedure. In the weighted setting, we apply WCS, which wraps the weighted _p_ -values (discrete or randomized) to guarantee finite-sample FDR control despite complex dependencies induced by weight estimation. WCS relies on a self-consistency condition where the number of rejected hypotheses must support the rejection threshold. 

## **4 THE DILEMMA** 

In dynamic environments, the weights _w_ ( _z_ ) adapt to local distribution shifts. We demonstrate that this adaptation forces a critical trade-off between resolution ( _rejection ability_ ) and stability ( _rejection consistency_ ), see Figure 1. 

**Failure Mode A: Resolution Collapse (Discretization).** For the conservative estimator (Eq. 1), the smallest _p_ -value is lower-bounded by the test point’s relative weight, 


![](Between_Resolution_Collapse_and_Variance_Inflation-_Weighted_Conformal_Anomaly_Detection_in_Low-Data_Regimes_images/conv_df19cafceda30860.pdf-0002-21.png)



![](Between_Resolution_Collapse_and_Variance_Inflation-_Weighted_Conformal_Anomaly_Detection_in_Low-Data_Regimes_images/conv_df19cafceda30860.pdf-0003-00.png)


Figure 1: **The Resolution–Variance Dilemma.** Under distribution shift, high importance weights create large steps in the conservative estimator, imposing a _resolution floor_ of minimum attainable _p_ -values that prevents rejection even for extreme scores. Standard randomization resolves the floor but introduces _variance inflation_ via noise that can mask the signal. The proposed Weighted KDE decouples resolution from sample size, enabling rejection below the floor without stochastic noise. 

To quantify when discretization prevents discoveries, we compare the minimum attainable _p_ -value (for _sj >_ max _i si_ ) to a _heuristic_ BH scale at target FDR level _α_ . If BH ends up making _R_ rejections, its cutoff is ( _R/m_ ) _α_ . Motivated by this, we define a detectability ratio _δ_ ( _r_ ) relative to a _putative_ rejection count _r ∈{_ 1 _, . . . , m}_ as 


![](Between_Resolution_Collapse_and_Variance_Inflation-_Weighted_Conformal_Anomaly_Detection_in_Low-Data_Regimes_images/conv_df19cafceda30860.pdf-0003-03.png)


If _δj_ ( _r_ ) _>_ 1, then even the most extreme right-tail score ( _sj >_ max _i si_ ) cannot produce _p_<sup>disc</sup> _j ≤_ ( _r/m_ ) _α_ , so BH cannot reach _r_ rejections using the discrete weighted _p_ -values on this realized weight configuration. 

In the unweighted setting ( _w ≡_ 1), the minimum attainable _p_ -value in the numerator of Eq. 3 reduces to 1 _/_ ( _N_ + 1). 

### **Failure Mode B: Variance Inflation (Randomization).** 

The randomized estimator (Eq. 2) replaces the discrete step at the test point by spreading a deterministic mass uniformly over an interval. Let _W_ cal =<sup>�</sup><sup>_N_</sup> _i_ =1<sup>_wi_so that</sup> 


![](Between_Resolution_Collapse_and_Variance_Inflation-_Weighted_Conformal_Anomaly_Detection_in_Low-Data_Regimes_images/conv_df19cafceda30860.pdf-0003-08.png)


Then conditional on the realized scores and respective weights, _p_<sup>rand</sup> _j_ is uniform on an interval of deterministic width 


![](Between_Resolution_Collapse_and_Variance_Inflation-_Weighted_Conformal_Anomaly_Detection_in_Low-Data_Regimes_images/conv_df19cafceda30860.pdf-0003-10.png)


Equivalently, one may write the randomization contribution as 


![](Between_Resolution_Collapse_and_Variance_Inflation-_Weighted_Conformal_Anomaly_Detection_in_Low-Data_Regimes_images/conv_df19cafceda30860.pdf-0003-12.png)


so the _amplitude_ is width _j_ and the _random noise_ is the uniform draw on [0 _,_ width _j_ ]. 

In the extreme-right-tail, no-ties case _sj >_ max _i si_ and with _W_ =( _sj_ ) = 0, we have 


![](Between_Resolution_Collapse_and_Variance_Inflation-_Weighted_Conformal_Anomaly_Detection_in_Low-Data_Regimes_images/conv_df19cafceda30860.pdf-0003-15.png)


Thus, if the relative test weight _wj/_ ( _W_ cal + _wj_ ) is large, the randomized _p_ -value exhibits substantial conditional variability even for extremely large scores. A true anomaly might fail to be rejected, simply due to an unlucky draw of _Uj_ . 

### **4.1 EFFECTIVE SAMPLE SIZE** 

Key driver of both _collapse_ (discrete floor) and _variance inflation_ (randomization amplitude) is the concentration of calibration weights. Following Kish [1965], for nonnegative weights _w_ 1 _, . . . , wN_ , define the effective sample size as 


![](Between_Resolution_Collapse_and_Variance_Inflation-_Weighted_Conformal_Anomaly_Detection_in_Low-Data_Regimes_images/conv_df19cafceda30860.pdf-0003-19.png)


When _N_ eff is small, a few calibration instances carry most of the mass. The test point’s relative weight _wj/W_ total tends to increase, raising the minimum attainable conformal _p_ -value. The randomized conformal _p_ -value interval width scales like width _j_ , increasing their conditional variance. 

## **5 CONTINUOUS WEIGHTED CONFORMAL INFERENCE** 

We propose an inference procedure that first adapts to covariate shift via density ratio estimation, and then constructs high-resolution _p_ -values using weighted kernel density estimation (KDE). By modelling the underlying score distribution rather than counting discrete exceedances, we decouple the ability to reject from the effective sample size. 

### **5.1 COVARIATE SHIFT ADAPTATION** 

To account for distribution shift between the calibration distribution _P_ and the test distribution _Q_ , we estimate the likelihood ratio _w_ ( _z_ ) = _dQ/dP_ ( _z_ ). Following the _density ratio trick_ (i.e., importance weighting) Sugiyama et al. [2008], Sugiyama and Kawanabe [2012], we reduce this to a probabilistic classification problem. We train a classifier (e.g. Random Forest) to discriminate between calibration samples ( _Y_ = 0, _X ∼ P_ ) and test samples ( _Y_ = 1, _X ∼ Q_ ). Weights for any test or calibration instance _zi_ are given by 


![](Between_Resolution_Collapse_and_Variance_Inflation-_Weighted_Conformal_Anomaly_Detection_in_Low-Data_Regimes_images/conv_df19cafceda30860.pdf-0004-02.png)


We apply winsorization to mitigate the effect of extreme importance weights from limited support overlap between _P_ and _Q_ , clipping weights to the [ _γ,_ 1 _− γ_ ] quantiles of the observed weight distribution ( _γ_ = 0 _._ 05). The procedure assumes covariate shift is invariant across domains and the support of _Q_ is sufficiently contained in that of _P_ . 

### **5.2 WEIGHTED KERNEL DENSITY ESTIMATION** 

Standard weighted conformal _p_ -values are discrete. Canonical weighted conformal methods add randomization to interpolate weighted ranks yielding continuous _p_ -values, introducing Monte Carlo noise. To avoid discretization and Monte Carlo randomization, we instead approximate the weighted score distribution using kernel density estimation. 

ˆ Let _si_ = _s_ ( _zi_ ) be calibration scores and _wi ≥_ 0 be calibration weights. Define the weighted KDE 


![](Between_Resolution_Collapse_and_Variance_Inflation-_Weighted_Conformal_Anomaly_Detection_in_Low-Data_Regimes_images/conv_df19cafceda30860.pdf-0004-07.png)


where _K_ ( _·_ ) is a symmetric kernel function satisfying �R<sup>_K_(</sup><sup>_u_)</sup><sup>_du_=1,withbandwidth</sup><sup>_h>_0(e.g.,theGaus-</sup> sian kernel). Let 


![](Between_Resolution_Collapse_and_Variance_Inflation-_Weighted_Conformal_Anomaly_Detection_in_Low-Data_Regimes_images/conv_df19cafceda30860.pdf-0004-09.png)


denote the CDF associated with _K_ . 

**Bandwidth Selection.** We select bandwidth _h_ via leaveone-out cross-validation to maximize the weighted loglikelihood. This data-driven approach adapts smoothness to _N_ eff, balancing the risk of over-smoothing (bias) against spurious modes (variance). 

### **5.3 CONTINUOUS** _p_ **-VALUE CONSTRUCTION** 

For a test score _sj_ , define the right-tail _p_ -value under the fitted weighted calibration score density _f_<sup>ˆ</sup><sup>_w_</sup> as 


![](Between_Resolution_Collapse_and_Variance_Inflation-_Weighted_Conformal_Anomaly_Detection_in_Low-Data_Regimes_images/conv_df19cafceda30860.pdf-0004-14.png)


_t_ With Φ _K_ ( _t_ ) = � _−∞_<sup>_K_(</sup><sup>_u_)</sup><sup>_du_, this equals</sup> 


![](Between_Resolution_Collapse_and_Variance_Inflation-_Weighted_Conformal_Anomaly_Detection_in_Low-Data_Regimes_images/conv_df19cafceda30860.pdf-0004-16.png)


**Granularity and Stability.** The estimator _p_ ˆKDE( _s_ ) maps continuously to [0 _,_ 1], eliminating the discrete floor _wj/W_ total inherent in weighted rank-based _p_ -values. Unlike the canonical randomized weighted conformal _p_ -value— which uses _Uj ∼_ Unif[0 _,_ 1] to randomize the weighted rank (not only to break ties, but also to interpolate in extreme tail/out-of-range cases)—our KDE smoothing removes the auxiliary tie-breaking and interpolation randomness ( _Uj_ ) used by randomized conformal _p_ -values, yielding deterministic _p_ -values conditional on the fitted KDE. This does not remove statistical estimation errors (finite-sample KDE error, weight-estimation error, and bandwidth-selection variability), but it removes the additional noise by _Uj_ . 

### **5.4 INTEGRATION WITH MULTIPLE TESTING** 

The proposed continuous estimator _p_ ˆ acts as a continuous surrogate for empirical conformal _p_ -values in downstream multiple-testing pipelines. However, we emphasize that it is not guaranteed to inherit the finite-sample conformal validity properties of weighted conformal _p_ -values. 

- **Unweighted Regime:** In the absence of shift, substituting continuous estimates into the BH procedure mitigates discretization conservatism in small- _N_ settings. 

- **Weighted Regime:** Under covariate shift, applying BH directly to discrete weighted conformal _p_ -values is not theoretically justified in general because their dependence can violate PRDS when weights are datadependent. Weighted Conformalized Selection (WCS) is designed to restore finite-sample FDR control in this setting and operates in two stages: 

   1. **Selection:** A preliminary rejection set is formed using a leave-one-out self-consistency check. 

   2. **Pruning:** The set is reduced to control finitesample FDR via three possible pruning strategies: _Deterministic_ (strict counting), _Homogeneous_ (shared randomization _ξ ∼ U_ [0 _,_ 1]), and _Heterogeneous_ (individual randomization _ξj ∼ U_ [0 _,_ 1]). 

**Robustness:** Discrete weighted estimators are sensitive to the pruning method. As noted in Jin and Candès [2025], 

_deterministic_ pruning may yield low power due to coarse resolution, requiring _homogeneous_ or _heterogeneous_ randomization to smooth threshold effects. In contrast, our KDE-based surrogate _p_ -values are continuous and do not cluster at the discrete mass points _wj/W_ total. Consequently, the choice of WCS pruning strategy becomes asymptotically equivalent, as the probability of a _p_ -value falling exactly on the rejection threshold is zero. We nevertheless retain the WCS wrapper with homogeneous pruning for all evaluated methods to ensure a uniform experimental pipeline. 

_Remark on Dependence and Guarantees:_ Weighted conformal _p_ -values may violate the PRDS property, so applying BH directly is not covered by standard finite-sample theory. WCS attains finite-sample FDR control under _H_ 0 (and suitable covariate-shift weights) by calibrating each test unit via auxiliary (leave-one-out) _p_ -values Jin and Candès [2025]. When we replace discrete weighted conformal _p_ -values with our surrogate _p_ -values, these guarantees do not automatically carry over: the KDE bandwidth and weight selection introduces global dependencies across calibration scores. Furthermore, when WCS is applied to our surrogate conformal _p_ -values (without recomputing candidate-dependent auxiliary _p_ -values), it often behaves similarly to the BH procedure on the same surrogate _p_ -values. We assess the robustness of this approximation empirically in Section 7. 

## **6 THEORETICAL ANALYSIS** 

Standard CAD provides _finite-sample_ marginal validity under exchangeability. In weighted settings, strictly maintaining this guarantee prompts a choice: the _resolution floor_ of the discrete estimator or the _variance inflation_ induced by randomization. We analyze these trade-offs, framing it as a trilemma among _validity_ (finite-sample guarantee), _stability_ (rejection consistency), and _resolution_ (rejection ability). 

### **6.1 ASYMPTOTIC MARGINAL VALIDITY** 

Let _Q_ 0 denote the inlier distribution of the test points. For each test unit _j_ , consider the null hypothesis _H_ 0 _,j_ : _zj ∼ Q_ 0, i.e., that test point _j_ is an inlier. A natural marginal validity target for a _p_ -value _p_ ˆ( _z_ ) is 


![](Between_Resolution_Collapse_and_Variance_Inflation-_Weighted_Conformal_Anomaly_Detection_in_Low-Data_Regimes_images/conv_df19cafceda30860.pdf-0005-06.png)


where the probability is over the calibration sample used to ˆ construct _p_ , and an independent null test point _Z ∼ Q_ 0. Let _F_ 0<sup>_w_denote the (weighted) CDF of the null score</sup><sup>_s_(</sup><sup>_Z_) under</sup> _Z ∼ Q_ 0. The ideal probability integral transform yields 


![](Between_Resolution_Collapse_and_Variance_Inflation-_Weighted_Conformal_Anomaly_Detection_in_Low-Data_Regimes_images/conv_df19cafceda30860.pdf-0005-08.png)


which is exactly Unif[0 _,_ 1] under _H_ 0 _,j_ when _F_ 0<sup>_w_iscon-</sup> tinuous. Our estimator _p_ ˆ( _z_ ) approximates this target via estimated weights _w_ ˆ and a weighted KDE. 

**Theorem 1** (Consistency and asymptotic marginal validity of KDE _p_ -values) **.** _Assume (i) F_ 0<sup>_wiscontinuous;(ii)_</sup> sup _z |_ ˆ _w_ ( _z_ ) _−w_ ( _z_ ) _| −→p_ 0 _and standard regularity conditions ensuring weighted KDE consistency; (iii) K is bounded with_ � _K_ = 1 _, the bandwidth hN →_ 0 _, and NhN /_ log _N →∞. Let Z ∼ Q_ 0 _be independent of the calibration data used to_ ˆ _construct w, F_<sup>�</sup> 0<sup>_w, andp_ˆ</sup><sup>_. Then_</sup> 


![](Between_Resolution_Collapse_and_Variance_Inflation-_Weighted_Conformal_Anomaly_Detection_in_Low-Data_Regimes_images/conv_df19cafceda30860.pdf-0005-11.png)


_Moreover, for each fixed u ∈_ [0 _,_ 1] _,_ 


![](Between_Resolution_Collapse_and_Variance_Inflation-_Weighted_Conformal_Anomaly_Detection_in_Low-Data_Regimes_images/conv_df19cafceda30860.pdf-0005-13.png)



![](Between_Resolution_Collapse_and_Variance_Inflation-_Weighted_Conformal_Anomaly_Detection_in_Low-Data_Regimes_images/conv_df19cafceda30860.pdf-0005-14.png)


**Remark.** KDE-based _p_ -values _p_ ˆKDE are <u>not</u> conformal and <u>not</u> finite-sample valid. Conformal _p_ -values satisfy finite-sample _marginal_ super-uniformity over the joint randomness of the calibration set and test point, but not conditional on a fixed calibration set. WCS achieves finite-sample FDR control with weighted conformal _p_ -values satisfying its leave-one-out structure—substituting KDE surrogates does not preserve this guarantee. We therefore treat WCSon-surrogates as a heuristic and evaluate it empirically, using smoothing and bandwidth selection to stabilize tail estimation and reduce discretization-induced Type II errors. 

### **6.2 BIAS–VARIANCE–RESOLUTION TRILEMMA** 

We compare deterministic _p_ ˆ<sup>disc</sup> (1), randomized _p_ ˆ<sup>rand</sup> (2), and KDE surrogate _p_ ˆKDE (7) _p_ -value construction. 

1. **Deterministic (discrete).** _p_ ˆ<sup>disc</sup> is deterministic but has a floor min ˆ _p_<sup>disc</sup> = _wj/_ (<sup>�</sup><sup>_N_</sup> _i_ =1<sup>_wi_+</sup><sup>_wj_)(attained</sup> when _sj >_ max _i si_ ), which can exceed the multipletesting cutoff and cause power collapse. 

2. **Randomized.** _p_ ˆ<sup>rand</sup> is conditionally uniform on an interval of width width _j_ = ( _wj_ +<sup>�</sup><sup>_N_</sup> _i_ =1<sup>_wi_I(</sup><sup>_si_=</sup> _sj_ )) _/_ (<sup>�</sup><sup>_N_</sup> _i_ =1<sup>_wi_+</sup><sup>_wj_) (via</sup><sup>_Uj∼_Unif[0</sup><sup>_,_1]). This re-</sup> moves the floor (unbounded resolution) but introduces conditional variance Var(ˆ _p_<sup>rand</sup> _| ·_ ) = width<sup>2</sup> _j_<sup>_/_12,</sup> which is large when the relative test mass is large. 

3. **Continuous (KDE).** _p_ ˆKDE replaces _Uj_ -randomization by deterministic smoothing of the weighted calibration score distribution, yielding continuous _p_ -values (no discrete floor) without auxiliary Monte Carlo variability, at the cost of replacing finite-sample exactness by asymptotic approximation (Theorem 1). 

### **6.3 FORMALIZING THE DILEMMA** 

We now formalize the limitations of the two standard weighted conformal _p_ -values. 

- 1A proof sketch is provided in Appendix C. 

**Proposition 1** (Resolution Collapse through Discreteness) **.** _Consider the deterministic weighted conformal p-value p_<sup>disc</sup> _j (Eq. 1). Conditional on the realized calibration scores {si}_<sup>_N_</sup> _i_ =1<sup>_and weights {wi}N_</sup> _i_ =1<sup>_, the smallest attainable value_</sup> _of the random variable p_<sup>disc</sup> _j over all possible test scores sj occurs when sj >_ max _i si, and equals_ 


![](Between_Resolution_Collapse_and_Variance_Inflation-_Weighted_Conformal_Anomaly_Detection_in_Low-Data_Regimes_images/conv_df19cafceda30860.pdf-0006-01.png)


**Implication.** If _wj/W_ total exceeds the multiple-testing threshold even arbitrarily extreme test scores cannot be rejected using the deterministic weighted conformal _p_ -value. 

**Proposition 2** (Conditional Variance through Randomness) **.** _Let p_<sup>rand</sup> _j be the randomized weighted conformal p-value (Eq. 2). Conditional on the realized calibration scores, weights and sj, the randomness in p_<sup>rand</sup> _j comes from Uj ∼_ Unif(0 _,_ 1) _and yields an interval of width_ width _j. Consequently,_ 


![](Between_Resolution_Collapse_and_Variance_Inflation-_Weighted_Conformal_Anomaly_Detection_in_Low-Data_Regimes_images/conv_df19cafceda30860.pdf-0006-04.png)


> _Proof._ Conditional on _{si, wi}_<sup>_N_</sup> _i_ =1<sup>and</sup><sup>_sj_, the randomized</sup> _p_ -value has the form _p_<sup>rand</sup> _j_ = _aj_ + _Uj ·_ width _j_ for some deterministic _aj_ (the left endpoint of the interval). Since Var( _Uj_ ) = 1 _/_ 12, the stated variance follows. 

**Implication:** The variance of the _p_ -value scales with the test weight fraction. If _N_ eff is low ( _wj_ is large), the _p_ -value becomes a noisy estimate. This noise acts as a regularizer, potentially masking anomalies and reducing statistical power. 

## **7 EVALUATION** 

We compare our proposed method against standard conformal procedures by a two-phase experimental protocol. All experiments are conducted on standard anomaly detection benchmark datasets Han et al. [2022] (see Table 3). The anomaly rate of each test set is controlled at _π ≈_ 0 _._ 05. All features are z-score standardized, with parameters fitted on the training splits for each randomized trial. 

### **7.1 PHASE 1: MODEL SELECTION** 

CAD requires a suitable scoring function to produce informative _p_ -values. To this end, we employ model selection for each experimental trial (so _per random seed_ ). 

For each of the _N_ seeds = 20 trials: 

1. We randomly partition the available data into a **Training Set** ( _D_ train), a **Validation Set** ( _D_ val), and a **Test Set** ( _D_ test). 

2. We train candidate detectors (see Table 2) on _D_ train with default hyperparameters, using _Jackknife+-afterBootstrap_ calibration Kim et al. [2020], Hennhöfer and Preisach [2024] that integrates training and calibration by bootstrap sampling to make more efficient use of the data without requiring a disjoint _D_ calib via splits. 

3. We evaluate these candidates on _D_ val (containing both inliers and anomalies). A model is then selected based on a lexicographical hierarchy: maximizing PR-AUC, then ROC-AUC, then minimizing Brier Score. 

4. The selected model is fixed for this trial for _all_ evaluated methods. Crucially, _D_ val is then discarded and _not_ used for further evaluation to prevent _data leakage_ . 

### **7.2 PHASE 2: MODEL INFERENCE** 

Using the fixed seed–model pairs from Phase 1, we compare the proposed method with four standard approaches (unweighted and weighted, each in deterministic and randomized variants). 

Specifically, we consider: (i) the deterministic EDF-based procedure, which isolates the effect of resolution collapse, (ii) the randomized variant, which isolates the effect of variance inflation and (iii) our proposed continuous relaxation leveraging both unweighted and weighted KDE. 

Weighted procedures employ WCS with _homogeneous_ pruning while unweighted procedures employ the BH method. All weights are estimated by a probabilistic Random Forest classifier<sup>2</sup> . The nominal FDR is controlled at _α_ = 0 _._ 1. 

### **7.3 EVALUATION METRICS** 

For a test batch, let _H_ 0 denote the set of true inliers and _H_ 1 the set of true anomalies. Let _R_ be the set of indices rejected. We evaluate performance using two metrics: 

**False Discovery Proportion (FDP).** The empirical fraction of false alarms among the reported discoveries: 


![](Between_Resolution_Collapse_and_Variance_Inflation-_Weighted_Conformal_Anomaly_Detection_in_Low-Data_Regimes_images/conv_df19cafceda30860.pdf-0006-23.png)


We report the marginal FDR, estimated by averaging the FDP over all _N_ seeds trials, as FDR<sup>�</sup> _≈_ E[FDP]. A method is FDR) considered _valid_ if FDR<sup>�</sup> _≤ α_ + _t_ 0 _._ 995 _×_<sup>_σ_</sup><sup><u>(</u></sup> _~~√~~_<sup>�</sup> 20<sup>.</sup> 

**Statistical Power.** The proportion of true anomalies correctly identified: 


![](Between_Resolution_Collapse_and_Variance_Inflation-_Weighted_Conformal_Anomaly_Detection_in_Low-Data_Regimes_images/conv_df19cafceda30860.pdf-0006-26.png)


We report the mean Power over the same _N_ seeds trials. 

2Estimates are stabilized via bagging; see Appendix D. 

Table 1: **Performance of conformal inference strategies across anomaly detection benchmarks.** All weighted methods employ WCS with _homogeneous pruning_ to guarantee finite-sample FDR control. Values represent the mean _±_ standard deviation of the empirical marginal FDR and statistical power aggregated over 20 independent trials with randomized splits. We compare deterministic and randomized baselines against the proposed continuous (KDE-based) approach. The calibration and test set sizes are denoted by _n_ train and _n_ test. Underlined values indicate validity violations (see Section 7.3). 

|**Dataset**|**Method**|**Deter**|**ministic**|**Rando**|**mized**|_n_train|_n_test|
|---|---|---|---|---|---|---|---|
||_Homogeneous_|**FDR**|**Power**|**FDR**|**Power**|||
||EDF|0_._000_±_0_._000|0_._000_±_0_._000|0_._062_±_0_._129|0_._200_±_0_._332|||
|WBC|Weighted EDF<br>**KDE**|0_._000_±_0_._000<br>0_._095_±_0_._152|0_._000_±_0_._000<br>0_._500_±_0_._351|0_._075_±_0_._245<br>—|0_._100_±_0_._244<br>|106|56|
||**Weighted KDE**|0_._078_±_0_._142|0_._417_±_0_._373|—||||
||EDF|0_._000_±_0_._000|0_._000_±_0_._000|0_._076_±_0_._199|0_._150_±_0_._221|||
|Ionosphere|Weighted EDF<br>**KDE**<br>**Weighted KDE**|0_._000_±_0_._000<br>0_._081_±_0_._150<br>0_._047_±_0_._119|0_._000_±_0_._000<br>0_._300_±_0_._434<br>0_._138_±_0_._339|0_._042_±_0_._131<br>—<br>—|0_._075_±_0_._143<br><br>|112|88|
||EDF|0_._098_±_0_._165|0_._280_±_0_._442|0_._166_±_0_._197|0_._440_±_0_._452|||
|WDBC|Weighted EDF<br>**KDE**|0_._000_±_0_._000<br>0_._086_±_0_._135|0_._000_±_0_._000<br>0_._390_±_0_._402|0_._108_±_0_._197<br>—|0_._090_±_0_._152<br>|178|92|
||**Weighted KDE**|0_._095_±_0_._164|0_._350_±_0_._383|—||||
||EDF|0_._000_±_0_._000|0_._000_±_0_._000|0_._000_±_0_._000|0_._094_±_0_._145|||
|Breast Cancer|Weighted EDF|0_._000_±_0_._000|0_._000_±_0_._000|0_._000_±_0_._000|0_._044_±_0_._084|222|171|
|(Wisconsin)|**KDE**|0_._046_±_0_._074|0_._350_±_0_._296|—||||
||**Weighted KDE**|0_._027_±_0_._066|0_._267_±_0_._218|—||||
||EDF|0_._000_±_0_._000|0_._000_±_0_._000|0_._017_±_0_._074|0_._067_±_0_._071|||
|Vowels|Weighted EDF<br>**KDE**|0_._000_±_0_._000<br>0_._035_±_0_._109|0_._000_±_0_._000<br>0_._122_±_0_._082|0_._000_±_0_._000<br>—|0_._014_±_0_._040<br>|703|364|
||**Weighted KDE**|0_._035_±_0_._109|0_._117_±_0_._082|—||||
||EDF|0_._034_±_0_._091|0_._039_±_0_._097|0_._119_±_0_._250|0_._067_±_0_._096|||
|Cardio|Weighted EDF<br>**KDE**|0_._018_±_0_._081<br>0_._066_±_0_._149|0_._015_±_0_._068<br>0_._089_±_0_._079|0_._031_±_0_._072<br>—|0_._030_±_0_._072<br>|827|458|
||**Weighted KDE**|0_._035_±_0_._098|0_._087_±_0_._080|—||||
||EDF|0_._102_±_0_._060|1_._000_±_0_._000|0_._105_±_0_._060|1_._000_±_0_._000|||
|Musk|Weighted EDF<br>**KDE**|0_._096_±_0_._056<br>0_._084_±_0_._060|1_._000_±_0_._000<br>1_._000_±_0_._000|0_._103_±_0_._056<br>—|1_._000_±_0_._000<br>|1,482|766|
||**Weighted KDE**|0_._082_±_0_._060|1_._000_±_0_._000|—||||
||EDF|0_._109_±_0_._107|0_._259_±_0_._082|0_._108_±_0_._105|0_._267_±_0_._085|||
|Satellite|Weighted EDF<br>**KDE**|0_._104_±_0_._099<br>0_._117_±_0_._103|0_._249_±_0_._085<br>0_._291_±_0_._087|0_._107_±_0_._103<br>—|0_._259_±_0_._083<br>|2,199|1,609|
||**Weighted KDE**|0_._112_±_0_._098|0_._284_±_0_._070|—||||
||EDF|0_._019_±_0_._037|0_._052_±_0_._057|0_._026_±_0_._040|0_._069_±_0_._053|||
|Mammography|Weighted EDF<br>**KDE**|0_._017_±_0_._037<br>0_._045_±_0_._060|0_._038_±_0_._049<br>0_._085_±_0_._050|0_._017_±_0_._037<br>—|0_._043_±_0_._046<br>|5,461|2,796|
||**Weighted KDE**|0_._037_±_0_._051|0_._077_±_0_._048|—||||




![](Between_Resolution_Collapse_and_Variance_Inflation-_Weighted_Conformal_Anomaly_Detection_in_Low-Data_Regimes_images/conv_df19cafceda30860.pdf-0008-00.png)


Figure 2: **Statistical power of weighted and randomized conformal methods with WCS pruning strategies, including the weighted KDE-based approach.** Labels refer to the WCS pruning method. Results for _Musk_ are omitted due to ceiling performance across all strategies. Error bars denote mean _±_ standard error over 20 randomized trials. 

## **8 RESULTS** 

Table 1 and Figure 2 show the evaluation results based on the described protocol. The results provide empirical validation of the theoretical dilemmas posed in Section 6, demonstrating that continuous inference relaxation is often a prerequisite for weighted CAD in low-data regimes. 

### **8.1 THE INABILITY TO REJECT** 

Smaller datasets ( _N ≪_ 1000) illustrate the inflation of the minimum attainable _p_ -values of discrete estimators. 

- **Failure through Discreteness:** Both standard discrete methods yield few to no discoveries. The sample size is insufficient to generate a _p_ -value below the detection threshold. Randomization recovers some of the lost ability to make discoveries. 

- **Recovery through Continuity:** The KDE approach successfully extrapolates the tail behaviour, recovering significant statistical power while maintaining valid marginal FDR control. 

Larger calibration sets ( _N >_ 1000) reduce kernel-induced bias, so all methods converge in performance as _N →∞_ . 

### **8.2 THE COST OF IMPORTANCE WEIGHTING** 

The dataset _WDBC_ clearly demonstrates how covariate shift adaptation via importance weighting affects _N_ eff. 

- **Uniform Weighting:** For both standard (unweighted) conformal methods _D_ calib is sufficient to achieve discoveries. However, note the validity violation of the unweighted, randomized approach in Table 1. 

- **Importance Weighting:** After adaption to covariate shift, higher weighted calibration instances dominate the mass, decreasing _N_ eff and leading to a severe loss in statistical power for the EDF-based weighted methods. 

The weighted KDE-based approach maintains its statistical power by decoupling its ability to reject from _N_ eff. 

### **8.3 FDR CONTROL AND VALIDITY** 

With one mild violation, the KDE-based approaches maintain valid marginal FDR control. In our experiments, the asymptotic approximation underlying the KDE does not systematically affect error control. Figure 2 illustrates the impact of the pruning method on the randomized variants, which are less powerful than the KDE-based approach. 

## **9 CONCLUSION** 

We formalized the _Resolution–Variance Dilemma_ in weighted CAD. As importance weights of calibration and test instances localize under covariate shift adaption, the effective sample size of the calibration set decreases, trapping inference in low-data regimes between discrete EDFs that become incapable of rejection in multiple testing ( _resolution collapse_ ) and a randomized variant that regains continuity by noise injection, degrading the signal ( _variance inflation_ ). 

To break this trade-off, we proposed a continuous weighted inference scheme via weighted KDE. Empirically, it (1) restores detection in data-scarce regimes where discrete baselines yield zero discoveries, (2) improves efficiency over stochastic smoothing by replacing it with deterministic smoothing, and (3) matches discrete performance as calibration data grows, consistent with asymptotic convergence. 

Conceptually, our framework is best viewed as a pragmatic extension of rigorous CAD: finite-sample exactness is theoretically strongest, but becomes operationally vacuous when discreteness prevents rejections. By accepting an _asymptotic_ validity target, continuous smoothing decouples rejection ability from calibration set size and extends CAD to settings where finite-sample exactness guarantees under (weighted) exchangeability yield no utility. 

### **Acknowledgements** 

This work was conducted as part of the research project _Biflex Industrie_ (grant number 01MV23020A), funded by the German Federal Ministry for Economic Affairs and Climate Action (BMWK). 

### **References** 

- D Ayres-de Campos, J Bernardes, A Garrido, J Marquesde Sá, and L Pereira-Leite. SisPorto 2.0: a program for automated analysis of cardiotocograms. <u>J. Matern. Fetal. Med., 9(5):311–318, September 2000.</u> 

- Tharindu R Bandaragoda, Kai Ming Ting, David Albrecht, Fei Tony Liu, Ye Zhu, and Jonathan R Wells. Isolationbased anomaly detection using nearest-neighbor ensembles. <u>Comput. Intell., 34(4):968–998, November 2018.</u> 

- Stephen Bates, Emmanuel Candès, Lihua Lei, Yaniv Romano, and Matteo Sesia. Testing for outliers with conformal p-values. <u>The Annals of Statistics, 51(1), February</u> 2023. ISSN 0090-5364. doi: 10.1214/22-aos2244. URL http://dx.doi.org/10.1214/22-AOS2244. 

- Yoav Benjamini and Yosef Hochberg. Controlling the false discovery rate: A practical and powerful approach to multiple testing. <u>Journal of the Royal Statistical Society. Series B (Methodological),</u> 57(1): 289–300, 1995. ISSN 00359246. URL http://www. jstor.org/stable/2346101. 

- Thomas G. Dietterich, Ajay N. Jain, Richard H. Lathrop, and Tomas Lozano-Perez. A comparison of dynamic reposing and tangent distance for drug activity prediction. In <u>Neural Information Processing Systems,</u> 1993. URL https://api.semanticscholar. org/CorpusID:9572004. 

- Markus Goldstein and Andreas Dengel. Histogram-based outlier score (hbos): A fast unsupervised anomaly detection algorithm. <u>KI-2012: Poster and Demo Track, 1:</u> 59–63, 2012. 

- Songqiao Han, Xiyang Hu, Hailiang Huang, Minqi Jiang, and Yue Zhao. Adbench: anomaly detection benchmark. In <u>Proceedings of the 36th International Conference on Neural Information Processing Systems, NIPS ’22, Red</u> Hook, NY, USA, 2022. Curran Associates Inc. ISBN 9781713871088. 

- D. M. Hawkins. <u>Identifcation of Outliers.</u> Springer Netherlands, 1980. ISBN 9789401539944. doi: 10.1007/ 978-94-015-3994-4. URL http://dx.doi.org/ 10.1007/978-94-015-3994-4. 

- Oliver Hennhöfer and Christine Preisach. Leave-oneout-, bootstrap- and cross-conformal anomaly detectors. 

In <u>2024 IEEE International Conference on Knowledge Graph (ICKG), pages 110–119, Dec 2024.</u> doi: 10.1109/ ICKG63256.2024.00022. 

- Ying Jin and Emmanuel J Candès. Model-free selective inference under covariate shift via weighted conformal p-values. <u>Biometrika,</u> page asaf066, 09 2025. ISSN 1464-3510. doi: 10.1093/biomet/asaf066. URL https: //doi.org/10.1093/biomet/asaf066. 

- Byol Kim, Chen Xu, and Rina Foygel Barber. Predictive inference is free with the jackknife+-after-bootstrap. In <u>Proceedings of the 34th International Conference on Neural Information Processing Systems, NIPS ’20, Red</u> Hook, NY, USA, 2020. Curran Associates Inc. ISBN 9781713829546. 

- L. Kish. <u>Survey Sampling.</u> Wiley, 1965. ISBN 9780471489009. 

- Mineichi Kudo, Jun Toyama, and Masaru Shimbo. Multidimensional curve classification using passing—through regions. <u>Pattern Recogn. Lett.,</u> 20(11–13):1103–1111, November 1999. ISSN 0167-8655. doi: 10.1016/ S0167-8655(99)00077-X. URL https://doi.org/ 10.1016/S0167-8655(99)00077-X. 

- Zheng Li, Yue Zhao, Nicola Botta, Cezar Ionescu, and Xiyang Hu. COPOD: Copula-Based outlier detection. In <u>2020 IEEE International Conference on Data Mining (ICDM). IEEE, November 2020.</u> 

- Zheng Li, Yue Zhao, Xiyang Hu, Nicola Botta, Cezar Ionescu, and George H Chen. ECOD: Unsupervised outlier detection using empirical cumulative distribution functions. <u>IEEE Trans. Knowl. Data Eng., 35(12):12181–</u> 12193, December 2023. 

- Fei Tony Liu, Kai Ming Ting, and Zhi-Hua Zhou. Isolation forest. In <u>2008 Eighth IEEE International Conference on Data Mining. IEEE, December 2008.</u> 

- Olvi L Mangasarian, W Nick Street, and William H Wolberg. Breast cancer diagnosis and prognosis via linear programming. <u>Oper. Res., 43(4):570–577, August 1995.</u> 

- Tomáš Pevný. Loda: Lightweight on-line detector of anomalies. <u>Mach. Learn., 102(2):275–304, February 2016.</u> 

Shebuti Rayana. ODDS library, 2016. URL https://shebuti.com/ outlier-detection-datasets-odds/. 

- Vincent G. Sigillito, Simon Wing, Larrie V. Hutton, and K. L. Baker. Classification of radar returns from the ionosphere using neural networks. 1989. URL https://api. semanticscholar.org/CorpusID:18522381. 

- Masashi Sugiyama and Motoaki Kawanabe. <u>Machine Learning in Non-Stationary Environments: Introduction to Covariate Shift Adaptation.</u> The MIT Press, March 2012. ISBN 9780262301220. doi: 10.7551/mitpress/9780262017091.001.0001. URL http://dx.doi.org/10.7551/mitpress/ 9780262017091.001.0001. 

- Masashi Sugiyama, Taiji Suzuki, Shinichi Nakajima, Hisashi Kashima, Paul von Bünau, and Motoaki Kawanabe. Direct importance estimation for covariate shift adaptation. <u>Annals of the Institute of Statistical Mathematics,</u> 60(4):699–746, August 2008. ISSN 1572-9052. doi: 10.1007/s10463-008-0197-x. URL http://dx.doi. org/10.1007/s10463-008-0197-x. 

- Ryan J. Tibshirani, Rina Foygel Barber, Emmanuel J. Candès, and Aaditya Ramdas. <u>Conformal prediction under covariate shift.</u> Curran Associates Inc., Red Hook, NY, USA, 2019. 

- W H Wolberg and O L Mangasarian. Multisurface method of pattern separation for medical diagnosis applied to breast cytology. <u>Proc. Natl. Acad. Sci. U. S. A., 87(23):</u> 9193–9196, December 1990. 

- Kevin S Woods, Jeffrey L Solka, Carey E Priebe, Chris C Doss, Kevin W Bowyer, and Laurence P Clarke. Comparative evaluation of pattern recognition techniques for detection of microcalcifications. In Raj S Acharya and Dmitry B Goldgof, editors, <u>Biomedical Image Processing and Biomedical Visualization.</u> SPIE, July 1993. 

# **Between Resolution Collapse and Variance Inflation: Weighted Conformal Anomaly Detection in Low-Data Regimes (Supplementary Material)** 

**Oliver Hennhöfer**<sup>1</sup> **Christine Preisach**<sup>1</sup> 

1Intelligent Systems Research Group (ISRG), Karlsruhe University of Applied Sciences, Germany 

## **A IMPLEMENTATION AND REPRODUCIBILITY DETAILS** 

All experiments reported in this paper can be reproduced end-to-end from code provided on https://github.com/OliverHennhoefer/wkde-cad. This environment fully specifies the Python version, and all required dependencies. Executing the provided configuration files and experiment scripts reproduces the complete experimental pipeline, including data preprocessing, model selection, model training and evaluation procedures as presented in the main text and supplementary material. 

All conformal methods as well as the method proposed in this work are implemented in the publicly available Python package nonconform, available on PyPI. The implementations are compatible with standard scikit-learn interfaces, as well as pyod and custom detector classes, and operate on data represented as either numpy arrays or pandas data frames. 

The package itself focuses exclusively on providing reusable method implementations for personal use. It does not include the experimental protocol, benchmarking framework, or evaluation pipeline used to produce the results in this paper. These components are provided separately within the reproducibility environment described above. This separation ensures that the methodological contributions can be applied independently to user-provided datasets while maintaining full reproducibility of the reported empirical results. 

## **B EVALUATION** 

Table 2: **Overview of the models used for evaluation, their abbreviations, categories, and references.** 

|**Model**|**Category**|**Reference**|
|---|---|---|
|Isolation Forest (**IForest**)|Tree-based|Liu et al. [2008]|
|Lightweight Online Detector of Anomalies (**LODA**)|Projection-based|Pevný [2016]|
|Isolation Nearest Neighbor Ensemble (**INNE**)|Neighbor-based|Bandaragoda et al. [2018]|
|Histogram-Based Outlier Score (**HBOS**)|Density/Distance-based|Goldstein and Dengel [2012]|
|Copula-Based OD (**COPOD**)|Copula-based|Li et al. [2020]|
|Empirical Cumulative Distribution OD (**ECOD**)|Distribution-based|Li et al. [2023]|



Table 3: **Overview of datasets used for evaluation, their categories, and references.** 

|**Dataset**|**Category**|**Reference**|
|---|---|---|
|WBC|Healthcare|Mangasarian et al. [1995]|
|Ionosphere|Oryctognosy|Sigillito et al. [1989]|
|WDBC|Healthcare|Mangasarian et al. [1995]|
|Breast Cancer|Healthcare|Wolberg and Mangasarian [1990]|
|Vowels|Linguistics|Kudo et al. [1999]|
|Cardio|Healthcare|Ayres-de Campos et al. [2000]|
|Musk|Chemistry|Dietterich et al. [1993]|
|Satellite|Astronautics|Rayana [2016]|
|Mammography|Healthcare|Woods et al. [1993]|



Table 4: **Per-dataset detector comparison (mean** _±_ **std over 20 seeds).** Results are aggregated across independent trials with per-seed model selection. **Wins** counts how often (out of 20) a detector is selected for the dataset according to the lexicographic rule PR-AUC _↑_ , ROC-AUC _↑_ , Brier _↓_ . 

|**Dataset**|**Model**|**PR-AUC (mean**_±_**std)**|**ROC-AUC (mean**_±_**std)**|**Brier (mean**_±_**std)**|**Wins**|
|---|---|---|---|---|---|
||**IForest**|0.987_±_0.009|0.993_±_0.004|0.051_±_0.005|12/20|
||**COPOD**|0.984_±_0.008|0.992_±_0.004|0.048_±_0.011|3/20|
|WBC|**ECOD**|0.984_±_0.008|0.992_±_0.004|0.049_±_0.012|2/20|
||**HBOS**|0.972_±_0.014|0.988_±_0.006|0.050_±_0.006|3/20|
||LODA|0.913_±_0.029|0.962_±_0.011|0.071_±_0.009|0/20|
||INNE|0.908_±_0.042|0.954_±_0.019|0.219_±_0.011|0/20|
||**INNE**|0.952_±_0.020|0.960_±_0.017|0.214_±_0.018|20/20|
||IForest|0.859_±_0.034|0.898_±_0.027|0.142_±_0.012|0/20|
|Ionoshere|ECOD|0.775_±_0.032|0.825_±_0.028|0.158_±_0.011|0/20|
|p|LODA|0.757_±_0.037|0.841_±_0.022|0.166_±_0.010|0/20|
||COPOD|0.756_±_0.033|0.833_±_0.024|0.162_±_0.013|0/20|
||HBOS|0.534_±_0.051|0.685_±_0.045|0.271_±_0.019|0/20|
||**COPOD**|0.985_±_0.012|0.996_±_0.003|0.053_±_0.004|11/20|
||**INNE**|0.976_±_0.019|0.994_±_0.005|0.223_±_0.012|8/20|
|WDBC|**IForest**|0.973_±_0.016|0.992_±_0.004|0.070_±_0.008|1/20|
||HBOS|0.959_±_0.024|0.988_±_0.006|0.090_±_0.009|0/20|
||ECOD|0.922_±_0.027|0.975_±_0.008|0.090_±_0.007|0/20|
||LODA|0.898_±_0.029|0.974_±_0.008|0.066_±_0.009|0/20|
||**IForest**|0.990_±_0.004|0.995_±_0.002|0.041_±_0.004|13/20|
||**COPOD**|0.987_±_0.004|0.994_±_0.002|0.047_±_0.003|5/20|
|Breast Cancer|**ECOD**|0.987_±_0.004|0.994_±_0.002|0.049_±_0.003|2/20|
|(Wisconsin)|HBOS|0.978_±_0.008|0.991_±_0.003|0.043_±_0.003|0/20|
||LODA|0.950_±_0.016|0.983_±_0.005|0.059_±_0.006|0/20|
||INNE|0.939_±_0.017|0.974_±_0.006|0.237_±_0.010|0/20|



Table 5: **Per-dataset detector comparison (mean** _±_ **std over 20 seeds).** Results are aggregated across independent trials with per-seed model selection. **Wins** counts how often (out of 20) a detector is selected for the dataset according to the lexicographic rule PR-AUC _↑_ , ROC-AUC _↑_ , Brier _↓_ . 

|**Dataset**|**Model**|**PR-AUC (mean**_±_**std)**|**ROC-AUC (mean**_±_**std)**|**Brier (mean**_±_**std)**|**Wins**|
|---|---|---|---|---|---|
||**INNE**|0.594_±_0.092|0.913_±_0.028|0.176_±_0.012|20/20|
||IForest|0.312_±_0.087|0.783_±_0.049|0.188_±_0.013|0/20|
|Vowels|LODA|0.243_±_0.065|0.696_±_0.057|0.204_±_0.012|0/20|
||HBOS|0.240_±_0.076|0.701_±_0.053|0.236_±_0.015|0/20|
||ECOD|0.227_±_0.070|0.628_±_0.066|0.228_±_0.017|0/20|
||COPOD|0.114_±_0.028|0.526_±_0.061|0.221_±_0.010|0/20|
||**ECOD**|0.752_±_0.039|0.962_±_0.007|0.089_±_0.006|18/20|
||**INNE**|0.707_±_0.038|0.955_±_0.009|0.249_±_0.006|2/20|
|Cardio|IForest|0.692_±_0.044|0.947_±_0.011|0.097_±_0.008|0/20|
||COPOD|0.654_±_0.047|0.939_±_0.010|0.090_±_0.012|0/20|
||LODA|0.620_±_0.059|0.920_±_0.017|0.077_±_0.009|0/20|
||HBOS|0.522_±_0.053|0.840_±_0.024|0.134_±_0.012|0/20|
||**HBOS**|1.000_±_0.000|1.000_±_0.000|0.070_±_0.005|20/20|
||ECOD|1.000_±_0.000|1.000_±_0.000|0.088_±_0.005|0/20|
|Mk|INNE|1.000_±_0.000|1.000_±_0.000|0.146_±_0.004|0/20|
|us|LODA|0.959_±_0.025|0.998_±_0.001|0.082_±_0.009|0/20|
||COPOD|0.497_±_0.044|0.959_±_0.006|0.193_±_0.006|0/20|
||IForest|0.449_±_0.157|0.944_±_0.027|0.221_±_0.012|0/20|
||**HBOS**|0.815_±_0.012|0.866_±_0.009|0.135_±_0.003|20/20|
||INNE|0.788_±_0.011|0.839_±_0.012|0.166_±_0.003|0/20|
|Stllit|IForest|0.773_±_0.016|0.804_±_0.018|0.139_±_0.005|0/20|
|aee|LODA|0.716_±_0.018|0.698_±_0.019|0.166_±_0.005|0/20|
||COPOD|0.679_±_0.016|0.695_±_0.017|0.181_±_0.005|0/20|
||ECOD|0.645_±_0.016|0.650_±_0.019|0.190_±_0.005|0/20|
||**ECOD**|0.504_±_0.053|0.912_±_0.017|0.067_±_0.005|17/20|
||**COPOD**|0.502_±_0.053|0.911_±_0.018|0.077_±_0.006|3/20|
|Mh|LODA|0.349_±_0.040|0.887_±_0.017|0.043_±_0.007|0/20|
|ammograpy|IForest|0.294_±_0.048|0.882_±_0.017|0.099_±_0.006|0/20|
||INNE|0.275_±_0.036|0.842_±_0.019|0.289_±_0.003|0/20|
||HBOS|0.146_±_0.026|0.844_±_0.018|0.106_±_0.009|0/20|



Table 6: **Performance of conformal inference strategies across anomaly detection benchmarks.** All weighted methods employ WCS with _deterministic pruning_ to guarantee finite-sample FDR control. Values represent the mean _±_ standard deviation of the empirical marginal FDR and statistical power aggregated over 20 independent trials with randomized splits. We compare deterministic and randomized baselines against the proposed continuous (KDE-based) approach. The calibration and test set sizes are denoted by _n_ train and _n_ test. Underlined values indicate validity violations (see Section 7.3). 

|**Dataset**|**Method**|**Deter**|**ministic**|**Rando**|**mized**|_n_train|_n_test|
|---|---|---|---|---|---|---|---|
||_Deterministic_|**FDR**|**Power**|**FDR**|**Power**|||
||EDF|0_._000_±_0_._000|0_._000_±_0_._000|0_._062_±_0_._129|0_._200_±_0_._332|||
|WBC|Weighted EDF<br>**KDE**|0_._000_±_0_._000<br>0_._095_±_0_._152|0_._000_±_0_._000<br>0_._500_±_0_._351|0_._050_±_0_._224<br>—|0_._017_±_0_._074<br>|106|56|
||**Weighted KDE**|0_._078_±_0_._142|0_._417_±_0_._373|—||||
||EDF|0_._000_±_0_._000|0_._000_±_0_._000|0_._076_±_0_._199|0_._150_±_0_._221|||
|Ionosphere|Weighted EDF<br>**KDE**<br>**Weighted KDE**|0_._000_±_0_._000<br>0_._081_±_0_._150<br>0_._047_±_0_._119|0_._000_±_0_._000<br>0_._300_±_0_._434<br>0_._138_±_0_._339|0_._000_±_0_._000<br>—<br>—|0_._025_±_0_._077<br><br>|112|88|
||EDF|0_._098_±_0_._165|0_._280_±_0_._442|0_._166_±_0_._197|0_._440_±_0_._452|||
|WDBC|Weighted EDF<br>**KDE**|0_._000_±_0_._000<br>0_._086_±_0_._135|0_._000_±_0_._000<br>0_._390_±_0_._402|0_._000_±_0_._000<br>—|0_._010_±_0_._045<br>|178|92|
||**Weighted KDE**|0_._095_±_0_._164|0_._350_±_0_._383|—||||
||EDF|0_._000_±_0_._000|0_._000_±_0_._000|0_._000_±_0_._000|0_._094_±_0_._145|||
|Breast Cancer|Weighted EDF|0_._000_±_0_._000|0_._000_±_0_._000|0_._000_±_0_._000|0_._006_±_0_._025|222|171|
|(Wisconsin)|**KDE**|0_._046_±_0_._074|0_._350_±_0_._296|—||||
||**Weighted KDE**|0_._027_±_0_._066|0_._267_±_0_._218|—||||
||EDF|0_._000_±_0_._000|0_._000_±_0_._000|0_._017_±_0_._074|0_._067_±_0_._071|||
|Vowels|Weighted EDF<br>**KDE**|0_._000_±_0_._000<br>0_._035_±_0_._109|0_._000_±_0_._000<br>0_._122_±_0_._082|0_._000_±_0_._000<br>—|0_._000_±_0_._000<br>|703|364|
||**Weighted KDE**|0_._035_±_0_._109|0_._117_±_0_._082|—||||
||EDF|0_._034_±_0_._091|0_._039_±_0_._097|0_._119_±_0_._250|0_._067_±_0_._096|||
|Cardio|Weighted EDF<br>**KDE**|0_._018_±_0_._081<br>0_._066_±_0_._149|0_._015_±_0_._068<br>0_._089_±_0_._079|0_._018_±_0_._081<br>—|0_._024_±_0_._068<br>|827|458|
||**Weighted KDE**|0_._035_±_0_._098|0_._087_±_0_._080|—||||
||EDF|0_._102_±_0_._060|1_._000_±_0_._000|0_._105_±_0_._060|1_._000_±_0_._000|||
|Musk|Weighted EDF<br>**KDE**|0_._090_±_0_._060<br>0_._084_±_0_._060|0_._950_±_0_._224<br>1_._000_±_0_._000|0_._100_±_0_._057<br>—|1_._000_±_0_._000<br>|1,482|766|
||**Weighted KDE**|0_._082_±_0_._060|1_._000_±_0_._000|—||||
||EDF|0_._109_±_0_._107|0_._259_±_0_._082|0_._108_±_0_._105|0_._267_±_0_._085|||
|Satellite|Weighted EDF<br>**KDE**|0_._094_±_0_._105<br>0_._117_±_0_._103|0_._214_±_0_._124<br>0_._291_±_0_._087|0_._099_±_0_._104<br>—|0_._233_±_0_._113<br>|2,199|1,609|
||**Weighted KDE**|0_._112_±_0_._098|0_._284_±_0_._070|—||||
||EDF|0_._019_±_0_._037|0_._052_±_0_._057|0_._026_±_0_._040|0_._069_±_0_._053|||
|Mammography|Weighted EDF<br>**KDE**|0_._017_±_0_._037<br>0_._045_±_0_._060|0_._038_±_0_._049<br>0_._085_±_0_._050|0_._017_±_0_._037<br>—|0_._039_±_0_._048<br>|5,461|2,796|
||**Weighted KDE**|0_._037_±_0_._051|0_._077_±_0_._048|—||||



Table 7: **Performance of conformal inference strategies across anomaly detection benchmarks.** All weighted methods employ WCS with _heterogeneous pruning_ to guarantee finite-sample FDR control. Values represent the mean _±_ standard deviation of the empirical marginal FDR and statistical power aggregated over 20 independent trials with randomized splits. We compare deterministic and randomized baselines against the proposed continuous (KDE-based) approach. The calibration and test set sizes are denoted by _n_ train and _n_ test. Underlined values indicate validity violations (see Section 7.3). 

|**Dataset**|**Method**|**Deter**|**ministic**|**Rando**|**mized**|_n_train|_n_test|
|---|---|---|---|---|---|---|---|
||_Heterogeneous_|**FDR**|**Power**|**FDR**|**Power**|||
||EDF|0_._000_±_0_._000|0_._000_±_0_._000|0_._062_±_0_._129|0_._200_±_0_._332|||
|WBC|Weighted EDF<br>**KDE**|0_._000_±_0_._000<br>0_._095_±_0_._152|0_._000_±_0_._000<br>0_._500_±_0_._351|0_._075_±_0_._245<br>—|0_._083_±_0_._183<br>|106|56|
||**Weighted KDE**|0_._078_±_0_._142|0_._417_±_0_._373|—||||
||EDF|0_._000_±_0_._000|0_._000_±_0_._000|0_._076_±_0_._199|0_._150_±_0_._221|||
|Ionosphere|Weighted EDF<br>**KDE**<br>**Weighted KDE**|0_._000_±_0_._000<br>0_._081_±_0_._150<br>0_._047_±_0_._119|0_._000_±_0_._000<br>0_._300_±_0_._434<br>0_._138_±_0_._339|0_._042_±_0_._131<br>—<br>—|0_._075_±_0_._143<br><br>|112|88|
||EDF|0_._098_±_0_._165|0_._280_±_0_._442|0_._166_±_0_._197|0_._440_±_0_._452|||
|WDBC|Weighted EDF|0_._000_±_0_._000|0_._000_±_0_._000|0_._142_±_0_._231|0_._100_±_0_._138|178|92|
||**KDE**|0_._086_±_0_._135|0_._390_±_0_._402|—||||
||**Weighted KDE**|0_._095_±_0_._164|0_._350_±_0_._383|—||||
||EDF|0_._000_±_0_._000|0_._000_±_0_._000|0_._000_±_0_._000|0_._094_±_0_._145|||
|Breast Cancer|Weighted EDF|0_._000_±_0_._000|0_._000_±_0_._000|0_._000_±_0_._000|0_._044_±_0_._084|222|171|
|(Wisconsin)|**KDE**|0_._046_±_0_._074|0_._350_±_0_._296|—||||
||**Weighted KDE**|0_._027_±_0_._066|0_._267_±_0_._218|—||||
||EDF|0_._000_±_0_._000|0_._000_±_0_._000|0_._017_±_0_._074|0_._067_±_0_._071|||
|Vowels|Weighted EDF<br>**KDE**|0_._000_±_0_._000<br>0_._035_±_0_._109|0_._000_±_0_._000<br>0_._122_±_0_._082|0_._000_±_0_._000<br>—|0_._011_±_0_._029<br>|703|364|
||**Weighted KDE**|0_._035_±_0_._109|0_._117_±_0_._082|—||||
||EDF|0_._034_±_0_._091|0_._039_±_0_._097|0_._119_±_0_._250|0_._067_±_0_._096|||
|Cardio|Weighted EDF<br>**KDE**<br>**Weighted KDE**|0_._018_±_0_._081<br>0_._066_±_0_._149<br>0_._035_±_0_._098|0_._015_±_0_._068<br>0_._089_±_0_._079<br>0_._087_±_0_._080|0_._035_±_0_._107<br>—<br>—|0_._028_±_0_._069<br><br>|827|458|
||EDF|0_._102_±_0_._060|1_._000_±_0_._000|0_._105_±_0_._060|1_._000_±_0_._000|||
|Musk|Weighted EDF<br>**KDE**|0_._096_±_0_._056<br>0_._084_±_0_._060|1_._000_±_0_._000<br>1_._000_±_0_._000|0_._103_±_0_._056<br>—|1_._000_±_0_._000<br>|1,482|766|
||**Weighted KDE**|0_._082_±_0_._060|1_._000_±_0_._000|—||||
||EDF|0_._109_±_0_._107|0_._259_±_0_._082|0_._108_±_0_._105|0_._267_±_0_._085|||
||Weighted EDF|0_._104_±_0_._099|0_._249_±_0_._085|0_._107_±_0_._103|0_._261_±_0_._081|||
|Satellite|**KDE**|0_._117_±_0_._103|0_._291_±_0_._087|—||2,199|1,609|
||**Weighted KDE**|0_._112_±_0_._098|0_._284_±_0_._070|—||||
||EDF|0_._019_±_0_._037|0_._052_±_0_._057|0_._026_±_0_._040|0_._069_±_0_._053|||
|Mammography|Weighted EDF<br>**KDE**|0_._017_±_0_._037<br>0_._045_±_0_._060|0_._038_±_0_._049<br>0_._085_±_0_._050|0_._017_±_0_._037<br>—|0_._045_±_0_._045<br>|5,461|2,796|
||**Weighted KDE**|0_._037_±_0_._051|0_._077_±_0_._048|—||||



## **C PROOF SKETCH OF THEOREM 1** 

_Proof sketch of Theorem 1._ The argument proceeds in three steps. 

**Step 1 (Uniform CDF consistency).** Decompose via the triangle inequality: 


![](Between_Resolution_Collapse_and_Variance_Inflation-_Weighted_Conformal_Anomaly_Detection_in_Low-Data_Regimes_images/conv_df19cafceda30860.pdf-0017-03.png)


where _F_<sup>�</sup> 0<sup>_w_denotes the oracle weighted kernel CDF estimator using the true weights</sup><sup>_w_.</sup> For term (II), write 


![](Between_Resolution_Collapse_and_Variance_Inflation-_Weighted_Conformal_Anomaly_Detection_in_Low-Data_Regimes_images/conv_df19cafceda30860.pdf-0017-05.png)


Under standard regularity conditions for weighted smoothed empirical distribution estimators (e.g. bounded oracle weights, � _i_<sup>(</sup><sup>_wi/_�</sup> _k_<sup>_wk_)2=</sup><sup>_Op_(</sup><sup>_N −_1), and a bounded monotone kernel CDF Φ</sup><sup>_K_), the stochastic term is</sup><sup>_Op_(</sup><sup>_N −_1</sup><sup>_/_2) uniformly in</sup> _t_ . If the weighted null density _f_ 0<sup>_w_= (</sup><sup>_F_</sup> 0<sup>_w_)</sup><sup>_′_has</sup><sup>_r_derivatives and the kernel is of order</sup><sup>_r_, then the bias term is</sup><sup>_O_(</sup><sup>_hr_</sup> _N_<sup>), hence</sup> vanishes when _hN →_ 0. Therefore 


![](Between_Resolution_Collapse_and_Variance_Inflation-_Weighted_Conformal_Anomaly_Detection_in_Low-Data_Regimes_images/conv_df19cafceda30860.pdf-0017-07.png)


For term (I), since Φ _K ∈_ [0 _,_ 1], 


![](Between_Resolution_Collapse_and_Variance_Inflation-_Weighted_Conformal_Anomaly_Detection_in_Low-Data_Regimes_images/conv_df19cafceda30860.pdf-0017-09.png)


Hence it suffices that the normalized weight vectors are _ℓ_ 1-consistent; for example, this holds if 


![](Between_Resolution_Collapse_and_Variance_Inflation-_Weighted_Conformal_Anomaly_Detection_in_Low-Data_Regimes_images/conv_df19cafceda30860.pdf-0017-11.png)


Thus (I) _−→p_ 0 as well. 


![](Between_Resolution_Collapse_and_Variance_Inflation-_Weighted_Conformal_Anomaly_Detection_in_Low-Data_Regimes_images/conv_df19cafceda30860.pdf-0017-13.png)


**Step 3 (Asymptotic super-uniformity).** Under _H_ 0, _Z ∼ Q_ 0 is independent of the calibration data. Since _F_ 0<sup>_w_is continuous,</sup> the probability integral transform gives _p_<sup>_∗_</sup> ( _Z_ ) _∼_ Unif[0 _,_ 1]. Conditional on the calibration sample: 

ˆ ˆ ˆ P _Z_ � _p_ ( _Z_ ) _≤ u |_ cal� _≤_ P _Z_ � _p_<sup>_∗_</sup> ( _Z_ ) _≤ u_ + _∥p − p_<sup>_∗_</sup> _∥∞ |_ cal� = _u_ + _∥p − p_<sup>_∗_</sup> _∥∞._ 

ˆ Taking expectations over the calibration data and applying dominated convergence (since _∥p − p_<sup>_∗_</sup> _∥∞ ≤_ 1): 


![](Between_Resolution_Collapse_and_Variance_Inflation-_Weighted_Conformal_Anomaly_Detection_in_Low-Data_Regimes_images/conv_df19cafceda30860.pdf-0017-17.png)


## **D STABILIZING WEIGHT ESTIMATION** 

When _|D_ calib _|_ and _|D_ test _|_ differ strongly, classifier-based density-ratio (importance-weight) estimation can become highvariance, yielding _spiky_ weight distributions. As discussed in Section 4, excessively large test weights inflate the lower bound of the conservative weighted conformal _p_ -value and can lead to strict power loss. To mitigate this instability, we use a balanced bootstrap bagging scheme followed by mild clipping. 

**Balanced bootstrap bagging.** Let _B_ be the number of bootstrap iterations and define the balanced sample size 


![](Between_Resolution_Collapse_and_Variance_Inflation-_Weighted_Conformal_Anomaly_Detection_in_Low-Data_Regimes_images/conv_df19cafceda30860.pdf-0018-03.png)


For each bootstrap iteration _b ∈{_ 1 _, . . . , B}_ , we sample with replacement _S_ points from _D_ calib and _S_ points from _D_ test, forming a balanced training set _D_<sup>(</sup><sup>_b_)</sup> . We train a probabilistic classifier _g_<sup>(</sup><sup>_b_)</sup> to distinguish test versus calibration membership, and then evaluate it on the full original pool 


![](Between_Resolution_Collapse_and_Variance_Inflation-_Weighted_Conformal_Anomaly_Detection_in_Low-Data_Regimes_images/conv_df19cafceda30860.pdf-0018-05.png)


We intentionally evaluate on all of _Z_ (rather than using out-of-bag predictions), prioritizing estimator stability over the potential bias reduction of out-of-bag aggregation. 

Let _g_<sup>(</sup><sup>_b_)</sup> ( _z_ ) denote the predicted probability of the test label, i.e. _g_<sup>(</sup><sup>_b_)</sup> ( _z_ ) _≈_ P( _Y_ = 1 _| Z_ = _z_ ) under the bootstrap training mixture in iteration _b_ (with _Y_ = 1 indicating test and _Y_ = 0 indicating calibration). Under standard density-ratio modeling, Bayes’ rule yields 


![](Between_Resolution_Collapse_and_Variance_Inflation-_Weighted_Conformal_Anomaly_Detection_in_Low-Data_Regimes_images/conv_df19cafceda30860.pdf-0018-08.png)


Because _D_<sup>(</sup><sup>_b_)</sup> is class-balanced, P( _Y_ = 1) = P( _Y_ = 0) = 1 _/_ 2 in training, and the prior-ratio factor equals 1. Hence, the per-bootstrap weight estimate simplifies to 


![](Between_Resolution_Collapse_and_Variance_Inflation-_Weighted_Conformal_Anomaly_Detection_in_Low-Data_Regimes_images/conv_df19cafceda30860.pdf-0018-10.png)


This is a special case of the general density ratio estimate in Section 5.1: since _D_<sup>(</sup><sup>_b_)</sup> is class-balanced, the prior correction factor _N_ cal _/N_ test reduces to unity. If a bootstrap replicate is not exactly balanced, we include the corresponding correction factor P( _Y_ = 0) _/_ P( _Y_ = 1). 

**Aggregation across bootstrap replicas.** We aggregate the bootstrap estimates via geometric averaging (equivalently, averaging in log-space): 


![](Between_Resolution_Collapse_and_Variance_Inflation-_Weighted_Conformal_Anomaly_Detection_in_Low-Data_Regimes_images/conv_df19cafceda30860.pdf-0018-13.png)


This aggregation is natural for positive, multiplicative quantities such as density ratios and reduces the effect of rare extreme values produced by individual bootstrap classifiers. 

ˆ **Winsorization for numerical stability.** Finally, we winsorize _w_ bag by clipping to empirical quantiles. Let _qγ_ and _q_ 1 _−γ_ be the empirical _γ_ and (1 _− γ_ ) quantiles of _{w_ ˆbag( _z_ ) : _z ∈ Z}_ . Define 


![](Between_Resolution_Collapse_and_Variance_Inflation-_Weighted_Conformal_Anomaly_Detection_in_Low-Data_Regimes_images/conv_df19cafceda30860.pdf-0018-16.png)


This step should be viewed as a variance-reduction regularization layer: it limits extreme weights in highly skewed settings at the possible cost of a small clipping-induced bias. 

**Fairness across methods.** Crucially, for all weighted methods we reuse the <u>exact same</u> stabilized weights _w_ ˆfinal( _z_ ) (from the same bagging and winsorization procedure) across evaluations, ensuring strictly comparable results that are not confounded by method-specific weight estimation noise. 

