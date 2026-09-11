
![](Anomaly_Detection_in_Streams_with_Extreme_Value_Theory_images/Anomaly_Detection_in_Streams_with_Extreme_Value_Theory.pdf-0001-00.png)


## **Anomaly Detection in Streams with Extreme Value Theory** 

Alban Siffer, Pierre-Alain Fouque, Alexandre Termier, Christine Largouët 


![](Anomaly_Detection_in_Streams_with_Extreme_Value_Theory_images/Anomaly_Detection_in_Streams_with_Extreme_Value_Theory.pdf-0001-03.png)


### **To cite this version:** 

Alban Siffer, Pierre-Alain Fouque, Alexandre Termier, Christine Largouët. Anomaly Detection in Streams with Extreme Value Theory. KDD 2017 - Proceedings of the 23rd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, Aug 2017, Halifax, Canada. ⟨10.1145/3097983.3098144⟩. ⟨hal01640325⟩ 

### **HAL Id: hal-01640325 https://hal.science/hal-01640325v1** 

Submitted on 20 Nov 2017 

**HAL** is a multi-disciplinary open access archive for the deposit and dissemination of scientific research documents, whether they are published or not. The documents may come from teaching and research institutions in France or abroad, or from public or private research centers. 

L’archive ouverte pluridisciplinaire **HAL** , est destinée au dépôt et à la diffusion de documents scientifiques de niveau recherche, publiés ou non, émanant des établissements d’enseignement et de recherche français ou étrangers, des laboratoires publics ou privés. 


![](Anomaly_Detection_in_Streams_with_Extreme_Value_Theory_images/Anomaly_Detection_in_Streams_with_Extreme_Value_Theory.pdf-0001-10.png)


HAL Authorization 

# **Anomaly Detection in Streams with Extreme Value Theory** 

#### A. Siffer 

Amossys, Inria, IRISA `alban.siffer@irisa.fr` 

#### A. Termier 

Univ. Rennes 1, IRISA `alexandre.termier@irisa.fr` 

#### P.A. Fouque 

Univ. Rennes 1, IUF, IRISA `pierre-alain.fouque@inria.fr` 

#### C. Largouet 

AgroCampus, IRISA `christine.largouet@irisa.fr` 

#### **ABSTRACT** 

Anomaly detection in time series has attracted considerable attention due to its importance in many real-world applications including intrusion detection, energy management and finance. Most approaches for detecting outliers rely on either manually set thresholds or assumptions on the distribution of data according to Chandola, Banerjee and Kumar. 

Here, we propose a new approach to detect outliers in streaming univariate time series based on Extreme Value Theory that does not require to hand-set thresholds and makes no assumption on the distribution: the main parameter is only the risk, controlling the number of false positives. Our approach can be used for outlier detection, but more generally for automatically setting thresholds, making it useful in wide number of situations. We also experiment our algorithms on various real-world datasets which confirm its soundness and efficiency. 

#### **CCS Concepts** 

- **Computing methodologies** _→_ **Anomaly detection;** 

- _•_ **Mathematics of computing** _→ Time series analysis;_ 

- **Information systems** _→_ Data stream mining; 

#### **Keywords** 

Outliers in time series, Extreme Value Theory, Streaming 

#### **1. INTRODUCTION** 

Anomaly detection is an important research area in data mining. Many types of anomalies, or _outliers_ , are described in the literature [23]. One of the most fundamental type of anomalies are the extreme values (maximum and minimum). 

Many work have been proposed for solving this problem. However, they require some knowledges about the data: either they make assumptions on the underlying distribution or they need manually set thresholds. When the data is static, or is a stream coming from an extremely controlled 

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for components of this work owned by others than ACM must be honored. Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. Request permissions from permissions@acm.org. 

_KDD ’17_ 

_⃝_ c 2017 ACM. ISBN . 

DOI: 

environment, such assumptions can safely be made. But in the general case of streaming data from an open environment, these assumptions are no longer true. They may fail in unexpected cases. 

The issue is that nowadays, more and more critical applications rely on _high throughput streaming numerical data_ like energy management [30], cyber-security [32] or finance [26]. For example, in intrusion detection, some network attack techniques rely on intensive scans of the network, which are characterized by an unusually high number of SYN packets [32]. The main challenge is to learn “normality” in an ever changing environment and to automatically adapt the detection method accordingly. 

The problem of detecting extreme values in streams can be expressed as follows: Let ( _Xt_ ) _t≥_ 0 be a streaming time series of iid observations. Can we set a threshold _zq_ such that for any _t ≥_ 0, the probability to observe _Xt > zq_ is lower than _q_ (for _q_ as small as desired) ? 

To solve this problem, we use the statistical powerful tool of _Extreme Value Theory_ (EVT). This theory was developed to study the law of extreme values in a distribution function after the following dramatic event. In the night of January 31 to February 1 of the year 1953, a set of rare conditions occurred in the North Sea, leading to a “perfect storm” scenario. On the coast of Netherlands, the waves generated overwhelmed the dikes, causing extensive flooding. The flooding led to the death of 1800+ people in the Netherlands alone. In the dike case, _Xt_ is the height of the waves, and _zq_ is the height of the dike. 

In the aftermath of this disaster, scientists were tasked to determine a minimal dike height such that the probability for waves to exceed this height is extremely low. Statisticians devised an elegant theory for the study of such rare events [10]. One of the most elegant result of EVT is that the distribution of the extreme values is almost independent of the distribution of the data with a theorem similar to the central limit theorem, for min _,_ max instead of the mean value. 

The main contribution of this paper is to propose an approach for outlier detection in high throughput streaming univariate and unimodal time series. Thanks to EVT, our approach makes no distribution assumption on the data: it is thus a solution to “Research Issue 6” for outlier detection in data streams as stated by Sadik and Gruenwald [29] in _SIGKDD Explorations 2014_ . We decline our approach into two algorithms: SPOT for streaming data having any stationary distribution, and DSPOT for streaming data that can be subject to concept drift. Through detailed exper- 

1 

iments on synthetic and real data, we show that our approach is accurate for detecting outliers, is computationally efficient, and for DSPOT reacts quickly to any change in the stream. For instance, we decide to test our algorithm on incoming streams without knowledge on their distribution. We show that we detect very efficiently and accurately: ( _i_ ) network SYN attacks on a labeled data stream and ( _ii_ ) peaks that allows to take decision on stock market (quickly react for buying or selling shares). Our experiments also confirm the EVT theory with accuracy and fast convergence. 

Analyzing streaming data require the computation of EVT to be fast and resilient: as a secondary contribution, we propose two improvements on the general method for solving the EVT problem, that improve both its speed and its robustness. They are used in our algorithms, but they are not specific to streaming data and can immediately be applied to most algorithms using EVT. 

#### **2. RELATED WORK** 

Classically, anomaly detectors have to highlight what will be considered as an anomaly, also called _outlier_ . As we propose a statistical method to find anomalies, we rely on the assumption given by Chandola, Banerjee and Kumar in [13]: “Normal data instances occur in high probability regions of a stochastic model, while anomalies occur in the low probability regions of the stochastic model”. 

A great deal of algorithms for static outlier detection are given in the literature. The main approaches are distance based [7], nearest-neighbor based [11] or clustering based [14] and are very well detailed in [13]. Nonetheless, as mentioned in [31], most existing outlier detection methods need to scan several times the data and/or have high time complexity, thus they cannot be used in data streams. 

In [28, 29], Sadik details the specificities of the stream environment and the hardships of outlier detection in this context. The main constraints are the following: data cannot be scanned twice and new concepts may keep evolving. 

Many works which address the streaming case present distance based algorithms for outlier detection (STORM [8], CORM [15], DBOD-DS [28], attributes weighting [31]). These methods are able to work on multidimensional streams with categorical features but they need user defined thresholds which could be a real hindrance in practice. 

Current statistical approaches to perform outlier detection in data stream suffer from the inherent problem, namely the distribution assumption. In [6], Agarwal assumes a gaussian model to detect anomalies in multidimensional arrays and recommends a Box-Cox transformation if it is not the case. In [16], a more general mixture model is presented by Eskin, based on a majority distribution and an anomaly one. However both models need to be learned, so data of each distribution are required. In [24], the authors use a probabilist threshold _ϵ_ to discriminate normal or abnormal data (observations with probability lower than _ϵ_ are anomalies), but its possible values are lower-bounded by 1 _/_ ( _k_ +1) where _k_ is the number of training elements. Thus it needs a huge training sample if we want a very low false positive rate. 

In our work, we do not assume the distribution of the value we monitor but we rely on powerful theoretical results to estimate accurately low probability areas and then discriminate outliers. With our single parameter algorithms, we are able to detect outliers in both stationary and drifting contexts. 

#### **3. BACKGROUND** 

In this section we describe the theoretical background of the Extreme Value Theory (EVT). We try to explain the main results and how they could be used to address our problem (the reader could refer to the rich reference of Beirlant _et al._ [10] for more details). This part is not a prerequisite to understand the purpose of our algorithm but it gathers some elements to precise its fundamental basis. 

Many techniques allow the scientist to find statistical thresholds (quantiles). For instance, we can compute them empirically or assume a distribution. However data do not necessarily follow well-known distributions (Gaussian, uniform, exponential etc.) so the model step (the choice of the distribution) could be hard, even inappropriate. Moreover, if we want to predict _extreme_ events, like rare or unprecedented events (as tidal waves), the empirical method will not give accurate estimation (an unprecedented event would have a probability equal to zero). The extreme value theory addresses these problems by inferring the distribution of the extreme events we might monitor, without strong hypothesis on the original distribution. 

Mathematically, _X_ is a random variable and _F_ its cumulative¯ distribution function: _F_ ( _x_ ) =¯ P( _X ≤ x_ ). We denote by _F_ the “tail” of the distribution: _F_ ( _x_ ) = 1 _− F_ ( _x_ ) = P( _X > x_ ). We use _Xi_ to denote both random variables and their outcomes, however the context will precise their meanings. For a random variable _X_ and a given probability _q_ we note _zq_ its quantile at level 1 _− q_ , i.e. _zq_ is the smallest value s.t. P( _X ≤ zq_ ) _≥_ 1 _− q_ i.e. P( _X > zq_ ) _< q_ . 

#### **3.1 Extreme value distributions** 

The goal of the extreme value theory is to find the law of extreme events (e.g. the law of the daily maximum of temperature, or the law of the monthly maximal tide height). A beautiful result from Fisher, Tippett [18] and later Gnedenko [20] states that, under a weak condition, these extreme events have the same kind of distribution, regardless of the original one. For instance the maximum of temperatures or tide heights have more or less the same distribution whereas the distributions of the temperatures and the tide heights are not likely to be the same. This extreme laws are called the Extreme Value Distributions (EVD) and they have the following form : 


![](Anomaly_Detection_in_Streams_with_Extreme_Value_Theory_images/Anomaly_Detection_in_Streams_with_Extreme_Value_Theory.pdf-0003-15.png)


All the extremes of common standard distributions follow such a distribution and the _extreme value index γ_ depends on this original law. For example, if _X_ 1 _, . . . Xn_ are _n_ iid variables (e.g. gaussian _N_ (0 _,_ 1)) then _Mn_ = max1 _≤i≤n Xi_ is likely to follow an EVD which extreme value index _γ_ is given by the initial distribution (for the Gaussian distribution _γ_ = 0). 

This result may seem very counterintuitive but we can give some elements to catch the idea. Indeed, we can easily imagine that for most distributions the probabilities decrease when events are extreme, ie P( _X > x_ ) _→_ 0 when _x_ increases. The function _F_<sup>¯</sup> ( _x_ ) = P( _X > x_ ) represents the _tail_ of the distribution of _X_ . Actually, there are not many possible shapes for this tail and _Gγ_ tries to fit them. The table 1 presents the three possible shapes of the tail and the link with the extreme value index _γ_ . It gives also an example of standard distribution which follows each tail behavior. The 

2 

parameter _τ_ represents the bound of the initial distribution, so it could be finite (ex: uniform cdf) or infinite (ex: normal cdf). The figure 1 depicts an example of the three behaviors. 

|Tail behavior (_x →τ_)<br>|Domain|Example|
|---|---|---|
|Heavy tail, P(_X > x_)_≃x_<sup>_−_1</sup><br>_γ_|_γ >_0|Frechet|
|Exponential tail, P(_X > x_)_≃e_<sup>_−x_</sup>|_γ_ = 0|Gamma|
|Bounded, P(_X > x_) =<br>_x≥τ_ <sup>0</sup>|_γ <_0|Uniform|



**Table 1: Relation between** _F_ **and** _γ_ 


![](Anomaly_Detection_in_Streams_with_Extreme_Value_Theory_images/Anomaly_Detection_in_Streams_with_Extreme_Value_Theory.pdf-0004-03.png)



![](Anomaly_Detection_in_Streams_with_Extreme_Value_Theory_images/Anomaly_Detection_in_Streams_with_Extreme_Value_Theory.pdf-0004-04.png)


**Figure 1: Tail distribution** _G_<sup>¯</sup> _γ_ **according to** _γ_ 

#### **3.2 Power of EVT** 

This phenomenon allows us to accurately compute probabilities without inferring the initial law that can be really complex. It“regularizes”the initial distribution. Indeed, the central limit theorem states that the mean of _n_ iid random variables converges in distribution to a normal distribution. The EVT theorem states the same result for the maximum. 

By fitting an EVD to ¯ the unknown input distri- _F_ = 1 _− F_ bution tail (see figure 2), it unknown is then possible to evaluate the probability of potential extreme events. In particular, from a given probabil¯ ity _q_ it is possible to cal- _Gγ_ culate _zq_ such that P( _X > zq_ ) _< q_ . To solve this prob- **EVD fit of an** lem, the natural way will be **cdf** to estimate _γ_ . Several estimates exist such as Hill’s 

**Figure 2: EVD fit of an unknown cdf** 

estimate [22] and Pickands’ estimate [27] but they give good results only for certain tail behaviors. Its estimation is hard and nowadays we do not know a general and efficient method to compute it (i.e. for all _γ ∈_ R). 

Another way exists to fit the tail of the distribution: the Peaks-Over-Threshold (POT) approach. 

#### **3.3 Peaks-Over-Threshold (POT) approach** 

The Peaks-Over-Threshold (POT) approach relies on the Pickands-Balkema-de Haan theorem [9, 27] (also called _second theorem_ in EVT in comparison to the initial result of Fisher, Tippett and Gnedenko) given below. 

Theorem 1 (Pickands-Balkema-de Haan). _The cumulative distribution function F ∈Dγ_ 1 _if and only if a function σ exists, for all x ∈_ R _s.t._ 1 + _γx >_ 0 _:_ 


![](Anomaly_Detection_in_Streams_with_Extreme_Value_Theory_images/Anomaly_Detection_in_Streams_with_Extreme_Value_Theory.pdf-0004-15.png)


A clearer view of the theorem is the following: 


![](Anomaly_Detection_in_Streams_with_Extreme_Value_Theory_images/Anomaly_Detection_in_Streams_with_Extreme_Value_Theory.pdf-0004-17.png)


This result shows that the excess over a threshold _t_ , written _X − t_ , are likely to follow a Generalized Pareto Distribution (GPD) with parameters _γ, σ_ . In fact, the GPD needs a third parameter, the location _µ_ , but it is null in our case. Rather than fitting an EVD to the extreme values of _X_ , the POT approach tries to fit a GPD to the excesses _X − t_ . 

In the case we get estimates _γ_ ˆ and _σ_ ˆ (our method will be described in 3.4), the quantile can be computed through : 


![](Anomaly_Detection_in_Streams_with_Extreme_Value_Theory_images/Anomaly_Detection_in_Streams_with_Extreme_Value_Theory.pdf-0004-20.png)


where _t_ is a“high”threshold (details will be given in 4.3.3), _q_ the desired probability, _n_ the total number of observations, _Nt_ the number of _peaks_ i.e the number of _Xi_ s.t. _Xi > t_ . 

Some classical methods can be used to perform the estimation of _γ_ and _σ_ , as the Method of Moments (MOM) or the Probability Weigted Moments (PWM) but they are less efficient and robust than the maximum likelihood estimation [10] that we describe below. 

#### **3.4 Maximum likelihood estimation** 

##### _3.4.1 Likelihood expression_ 

The maximum likelihood estimation remains a natural way to evaluate the parameters through observations. If _X_ 1 _, . . . Xn_ are _n_ independent realizations of the random variable _X_ which density (noted _fθ_ ) is parametrized by _θ_ (possibly a vector), the likelihood function is defined by: 


![](Anomaly_Detection_in_Streams_with_Extreme_Value_Theory_images/Anomaly_Detection_in_Streams_with_Extreme_Value_Theory.pdf-0004-26.png)


It represents joint density of these _n_ observations. As _X_ 1 _, . . . Xn_ are fixed in our context, we try to find the parameter _θ_ such that the likelihood is maximized. It means that we are looking for the value of _θ_ which makes our observations the most probable. Practically, we work on the log-likelihood, so in our case (GPD fit) we have to maximize : 


![](Anomaly_Detection_in_Streams_with_Extreme_Value_Theory_images/Anomaly_Detection_in_Streams_with_Extreme_Value_Theory.pdf-0004-28.png)


where _Yi >_ 0 are the excesses of _Xi_ over _t_ ( _Yi_ = _Xi − t_ for _Xi > t_ ). Unfortunately, the optimization must be done numerically, implying the classical numerical issues. To perform it, the procedure of Grimshaw [21] can be used. 

In a strict GPD case (if the _Yi_ follow exactly a GPD), the Maximum Likelihood Estimate (MLE) has some good convergence properties in comparison to other estimates (MOM 

> 1It means that the extrema of the distribution of _F_ converge in distribution to _Gγ_ . 

3 

or PWM). It converges in distribution to a Gaussian distribution when the number of peaks _Nt →∞_ when _γ > −_<sup><u>1</u></sup> 2 (with a rate of consistency<sup>_~~√~~_</sup> _Nt_ ) and is superefficient when _−_ 1 _< γ < −_ 2<sup><u>1</u>witharateofconsistency</sup><sup>_N_</sup> _t_<sup>_−γ_</sup> . 

##### _3.4.2 The Grimshaw’s trick_ 

The trick of the Grimshaw’s procedure is to reduce the two variables optimization problem to a single variable equation. Let us write _ℓ_ ( _γ, σ_ ) = log _L_ ( _γ, σ_ ). As we find an extremum of _ℓ_ , we look for solutions of the system _∇ℓ_ ( _γ, σ_ ) = 0. Grimshaw has shown that if we get a solution ( _γ_<sup>_∗_</sup> _, σ_<sup>_∗_</sup> ) of this system then the variable _x_<sup>_∗_</sup> = _γ_<sup>_∗_</sup> _/σ_<sup>_∗_</sup> is solution of the scalar equation _u_ ( _x_ ) _v_ ( _x_ ) = 1 where: 


![](Anomaly_Detection_in_Streams_with_Extreme_Value_Theory_images/Anomaly_Detection_in_Streams_with_Extreme_Value_Theory.pdf-0005-03.png)


Moreover, by finding a solution _x_<sup>_∗_</sup> of this equation, we can retrieve _γ_<sup>_∗_</sup> = _v_ ( _x_<sup>_∗_</sup> ) _−_ 1 and _σ_<sup>_∗_</sup> = _γ_<sup>_∗_</sup> _/x_<sup>_∗_</sup> . Nevertheless, the solutions of this equation give only possible candidates for the maximum of _ℓ_ , so we have to get all the roots, to calculate the corresponding likelihood and keep the best tuple (ˆ _γ,_ ˆ _σ_ ) as our final estimates. 

We have to pay attention to how this numerical root search is done. In fact, the values 1+ _xYi_ must be strictly positives. As the _Yi_ are positive, we must find _x_<sup>_∗_</sup> on � _−_ **Y** <u>1</u><sup>_M,_+</sup><sup>_∞_</sup> � where **Y**<sup>_M_</sup> = max _Yi_ . Grimshaw calculates also an upperbound _x_<sup>_∗_</sup> max<sup>forthisrootsearch:</sup> 


![](Anomaly_Detection_in_Streams_with_Extreme_Value_Theory_images/Anomaly_Detection_in_Streams_with_Extreme_Value_Theory.pdf-0005-06.png)


where **Y**<sup>_m_</sup> = min _Yi_ and **Y** is the mean of the _Yi_ . Finally, the number of roots is not known and 0 is always a solution so the implementation must find all the solutions and pick up those which maximizes the likelihood. 

#### **4. OUR CONTRIBUTION** 

The extreme value theory, through the POT approach, gives us a way to estimate _zq_ such that P( _X > zq_ ) _< q_ without any strong assumption on the distribution of _X_ and without any clear knowledge about its distribution. 

In this section we use this result to build a streaming outlier detector. First we present the initialization step which computes an threshold _zq_ from _n_ observations _X_ 1 _, . . . Xn_ . Then, we detail our two streaming algorithms which update _zq_ with the incoming data and use it as a decision bound. We propose SPOT which works in stationary cases, and DSPOT which takes into account a drift component. Finally we give some theoretical and technical improvements making our bound update fast and sturdy. 

#### **4.1 Initialization step** 

Let us sum up the basic idea of our algorithm. We have _n_ observations _X_ 1 _, . . . Xn_ , and we have fixed a risk _q_ . The goal is to compute a first threshold _zq_ verifying P( _X > zq_ ) _< q_ . The figure 3 shows what we do on this initial batch (calibration). The idea is to set a high threshold _t_ (e.g. a high empirical quantile practically), retrieve the _peaks_ (the excesses over _t_ ) and fit a GPD (Generalized Pareto Distribution) to them. So that we infer the distribution of the extreme values and we can compute the threshold _zq_ . 

This initialization step is summarized in the algorithm 1. The choice of _t_ will be discussed in 4.3.3. The set **Y** _t_ is the _peaks set_ where we store the observed excesses over _t_ . The GPD fit is performed with the Grimshaw trick (we detail our likelihood optimization in 4.3.2) and then we can compute _zq_ with equation 1. 

**Algorithm 1 POT** <u>(Peaks-over-Threshold)</u> 


![](Anomaly_Detection_in_Streams_with_Extreme_Value_Theory_images/Anomaly_Detection_in_Streams_with_Extreme_Value_Theory.pdf-0005-15.png)


#### **4.2 Finding anomalies in a stream** 

The POT primitive returns a threshold _zq_ which we use to define a ”normality bound” (figure 3). In our streaming algorithms the POT primitive (algorithm 1) is used as an initialization step. 

The POT primitive may be seen as a _training_ step but this is partly wrong because the initial batch _X_ 1 _, . . . Xn_ is not labeled and is not considered as a ground truth in our algorithm. The initialization is more a _calibration_ step. Our streaming anomaly detector uses the next observations to both detect anomalies and refine the anomaly threshold _zq_ . 

##### _4.2.1 Stationary case_ 

The way how the POT estimate is built is really streamready. As we do not have to store the whole time series (only the peaks), it requires low memory so we can use it in a stream. However, the stream must contain values from the same distribution, so this distribution cannot been time-dependent (what we call _stationary_ ). In case of timedependency, we will show that our algorithm can be adapted to drifting cases (see 4.2.2). 

The principle of the SPOT algorithm is the following : we want to detect abnormal events in a stream ( _Xi_ ) _i>_ 0 in a blind way (without knowledge about the distribution). Firstly, we perform a POT estimate on the _n_ first values ( _n ∼_ 1000) and we get an initial threshold _zq_ (initialization). Then for all the next observed values we can flag the events or update the threshold (see figure 3). If a value exceeds our threshold _zq_ then we consider it as abnormal (we can retrieve this anomaly in a list **A** ). The anomalies are not taken into account for the model update. In the other cases, either _Xi_ is greater than the initial threshold (peak case) either it is a “common” value (normal case). In the peak case, we add the excess to the peaks set and we update the threshold _zq_ . 

In this algorithm we perform the maximum number of threshold updates but it is possible to do it off-line at fixed time interval. Of course we illustrate the principle only with upper-bound thresholds but the method is the same for lower-bound ones and we can even combine both (performances will be presented in 5.4). 

##### _4.2.2 Drifting case_ 

SPOT assumes that the distribution of the _Xi_ does not change over time but it might be restrictive. For instance, a mid-term seasonality cannot be taken into account, making 

4 

**Algorithm 2 SPOT** <u>(Streaming</u> POT) 

1: **procedure** SPOT(( _Xi_ ) _i>_ 0 _, n, q_ ) 2: **A** _←∅ ▷_ `set of the anomalies` 3: _zq, t ←_ POT( _X_ 1 _, . . . Xn, q_ ) 4: _k ← n_ 5: **for** _i > n_ **do** 6: **if** _Xi > zq_ **then** _▷_ `anomaly case` 7: Add ( _i, Xi_ ) in **A** 8: **else if** _Xi > t_ **then** _▷_ `real peak case` 9: _Yi ← Xi − t_ 10: Add _Yi_ in **Y** _t_ 11: _Nt ← Nt_ + 1 12: _k ← k_ + 1 13: _γ,_ ˆ ˆ _σ ←_ Grimshaw( **Y** _t_ ) 14: _zq ←_ CalcThreshold( _q,_ ˆ _γ,_ ˆ _σ, k, Nt, t_ ) 15: **else** _▷_ `normal case` 16: _k ← k_ + 1 17: **end if** 18: **end for** 19: **end procedure** 


![](Anomaly_Detection_in_Streams_with_Extreme_Value_Theory_images/Anomaly_Detection_in_Streams_with_Extreme_Value_Theory.pdf-0006-02.png)


local peaks undetectable. In this section we overcome this issue by modeling an average local behavior and applying SPOT on relative gaps. 

We propose Drift SPOT (DSPOT) which makes SPOT run not on the absolute values _Xi_ but on the relative ones. We use the variable change _Xi_<sup>_′_=</sup><sup>_Xi−Mi_where</sup><sup>_Mi_models</sup> the local behavior at time _i_ (see figure 4). In our implementation we used a moving average _Mi_ = (1 _/d_ ) _·_<sup>�</sup><sup>_d_</sup> _k_ =1<sup>_X_</sup> _i_<sup>_∗_</sup> _−k_ with _Xi_<sup>_∗_</sup> _−_ 1<sup>_, . . . X_</sup> _i_<sup>_∗_</sup> _−d_<sup>thelast</sup><sup>_d_”normal” observations(so</sup><sup>_d_is</sup> a window parameter). In this new context we assume that the local variations _Xi_<sup>_′_comefromasamestationarydis-</sup> tribution (the hypothesis assumed for _Xi_ in SPOT is now assumed for _Xi_<sup>_′_).</sup> 

This variant uses an additional parameter _d_ , which can be viewed as a window size. The distinctive features of this window (noted _W_<sup>_∗_</sup> ) are the following: it might be non continuous and it does not contain abnormal values. 

The algorithm 3 shows our method to capture the local model and perform SPOT thresholding on local variations. It contains some additional steps so as to compute variable changes. For these stages, we principally use a sliding windows over normal observations _W_<sup>_∗_</sup> (lines 3, 7, 24 and 28) in order to calculate a local normal behavior _Mi_ (lines 4, 8, 25 and 29) through averaging. We logically update the local behavior only in normal or peak cases (lines 25 and 29). We can retrieve sequentially the “real” extreme quantiles by adding _Mi_ to the calculated _zq_ . Such a choice to model the local behavior is a very efficient way to adapt 


![](Anomaly_Detection_in_Streams_with_Extreme_Value_Theory_images/Anomaly_Detection_in_Streams_with_Extreme_Value_Theory.pdf-0006-07.png)


**Figure 4: Anomaly detection with drift** 

**Algorithm 3 DSPOT** <u>(Streaming</u> POT with drift) 


![](Anomaly_Detection_in_Streams_with_Extreme_Value_Theory_images/Anomaly_Detection_in_Streams_with_Extreme_Value_Theory.pdf-0006-10.png)


SPOT to drifting contexts. As mentioned in the previous paragraph, DSPOT can be adapted to compute upper and lower bounds. 

#### **4.3 Numerical optimization** 

The streaming context requests fast and resilient algorithms. In this part, we optimize the GPD fit by reducing the search of optimal parameters and making it more robust to common numerical stability problems (divergence, absurd values). The proposition 1 gives a general result for EVT, improving the Grimshaw’s trick. In 4.3.2, we detail how we perform the likelihood optimization and finally we give some details about the initial threshold _t_ . 

##### _4.3.1 Reduction of the optimal parameters search_ 

5 

As we have seen in section 3.4.2, the Grimshaw’s method for the maximum likelihood estimation requires a numerical root search in a bounded interval. In this paragraph we show that we can reduce this interval. 

Gathering the following result and the previous bounds (section 3.4.2), the possible solutions of _u_ ( _x_ ) _v_ ( _x_ ) = 1 stand in the two intervals 


![](Anomaly_Detection_in_Streams_with_Extreme_Value_Theory_images/Anomaly_Detection_in_Streams_with_Extreme_Value_Theory.pdf-0007-02.png)


Proposition 1. _If x_<sup>_∗_</sup> _is a solution of u_ ( _x_ ) _v_ ( _x_ ) = 1 _,_ 


![](Anomaly_Detection_in_Streams_with_Extreme_Value_Theory_images/Anomaly_Detection_in_Streams_with_Extreme_Value_Theory.pdf-0007-04.png)



![](Anomaly_Detection_in_Streams_with_Extreme_Value_Theory_images/Anomaly_Detection_in_Streams_with_Extreme_Value_Theory.pdf-0007-05.png)


Then applying Jensen’s inequality on the convex function _x �→_ 1+1 _x_<sup>weget:</sup> 


![](Anomaly_Detection_in_Streams_with_Extreme_Value_Theory_images/Anomaly_Detection_in_Streams_with_Extreme_Value_Theory.pdf-0007-07.png)


so that 

If _x_<sup>_∗_</sup> is a solution of the equation _u_ ( _x_ ) _v_ ( _x_ ) = 1, we must have 


![](Anomaly_Detection_in_Streams_with_Extreme_Value_Theory_images/Anomaly_Detection_in_Streams_with_Extreme_Value_Theory.pdf-0007-10.png)


Simplifying this inequality, we get 


![](Anomaly_Detection_in_Streams_with_Extreme_Value_Theory_images/Anomaly_Detection_in_Streams_with_Extreme_Value_Theory.pdf-0007-12.png)


And a simple sign study gives the result. 

##### _4.3.2 How can we maximize the likelihood function?_ 

Finding the maximum of the likelihood boils down to apply a root search. But this is not a trivial task: we do not know the number of roots and all the roots are potential candidates to maximize this function. 

In [21], Grimshaw gives an analytic-based routine using root-finding algorithm is given however the needed condition _f_ ( _a_ ) _f_ ( _b_ ) _<_ 0 is not emphasized leading to uncertain results. For this reason we decide to use another method to find these roots. 

In our implementation, we set a very small _ϵ >_ 0 ( _∼_ 10<sup>_−_8</sup> ) and we look for the roots of the function _w_ : _x �→ u_ ( _x_ ) _v_ ( _x_ ) _−_ 1 in both intervals 


![](Anomaly_Detection_in_Streams_with_Extreme_Value_Theory_images/Anomaly_Detection_in_Streams_with_Extreme_Value_Theory.pdf-0007-18.png)


The real _ϵ_ is used to avoid both cases _x_ = **Y** <u>1</u><sup>_M_(where</sup><sup>_w_is</sup> not defined) and _x_ = 0 (which is always a solution). 

Many methods exist to find multiple roots of polynomials (such as Sturm method) but not for the general case of scalar functions. Furthermore, finding a root needs a sign change which may be difficult to detect. Thus we have reduced our root search to a function minimization which requires less assumptions. 

To find the zeros of _w_ we solve numerically the following optimization problem in both intervals (that we note _I_ ): 


![](Anomaly_Detection_in_Streams_with_Extreme_Value_Theory_images/Anomaly_Detection_in_Streams_with_Extreme_Value_Theory.pdf-0007-22.png)


The minimization can be done with a classical algorithm (e.g. L-BFGS-B [12]) starting with _k_ points _x_<sup>0</sup> 1<sup>_, ...x_0</sup> _k_<sup>(</sup><sup>_k≃_</sup> 10) distributed over _I_ . We use this procedure for three reasons: the optimal configuration ( _x_<sup>_∗_</sup> 1<sup>_, ..x∗_</sup> _k_<sup>) is likelytocontain</sup> the zeros of _w_ in _I_ , we can retrieve several roots (according to _k_ ) and optimizing procedures do not require sign change between the bounds. 

We perform this optimization in both intervals so we get a list of candidates to maximize the likelihood (the case _x_ = 0 is also treated). We keep the best of them and we retrieve the best parameters for the GPD fit. 

##### _4.3.3 Initial threshold_ 

We have detailed the Grimshaw procedure (3.4.2 and 4.3) and how the final threshold _zq_ is calculated (equation 1) but we have not dealt with the initial threshold _t_ . In practice, its value is not paramount except that it must be“high”enough. The higher is _t_ , the more relevant will be the GPD fit (low bias). However, if _t_ is too high, the peaks set **Y** _t_ would be little filled in, so the model would be more variable (high variance). The only important condition is to ensure that _t_ is lower than _zq_ , meaning that the probability associated to _t_ must be lower than 1 _− q_ . In practice we set _t_ to a high empirical quantile (98%). 

A method based on the _mean excess plot_ [10] could be used to set _t_ in a smarter way but it is less stable and likely to output absurd values. 

#### **5. EXPERIMENTS** 

In this section we apply both our algorithms SPOT and DSPOT on several contexts. First, we compare the computed threshold _zq_ with the theoretical ones through experiments on synthetic data. Then we use real world datasets from several fields (network, physics, finance) to highlight the properties of our algorithms. Finally we present the performance of our implementation. 

The real world datasets used in these experiments are all available on the Internet and we do our utmost to detail experimental protocols making them totally reproducible. Our `python3` implementation is available at [1]. 

#### **5.1 (D)SPOT reliability** 

In this section, we compare our computed threshold _zq_ to the theoretical one. In other words, we want to check if _zq_ is the desired threshold (which verifies P( _X > zq_ ) _< q_ ). In the same time we evaluate the impact of the number of observations _n_ in the initial batch. 

In the following experiments we set _q_ = 10<sup>_−_3</sup> and we run SPOT on Gaussian white noises of 15000 values, i.e. 15000 independent values from a standard normal distribution ( _µ_ = 0 _, σ_<sup>2</sup> = 1). For different values of _n_ (300, 500, 1000, 2000 and 5000), we run SPOT _k_ = 100 times and we retrieve the averaged error made in comparison to the theoretical threshold: 


![](Anomaly_Detection_in_Streams_with_Extreme_Value_Theory_images/Anomaly_Detection_in_Streams_with_Extreme_Value_Theory.pdf-0007-34.png)


6 

Here, _z_<sup>th</sup> is the quantile of the standard normal distribution at level 1 _−q_ , so _z_<sup>th</sup> _≃_ 3 _._ 09. The figure 5 presents the results. 

First of all the curves show that, for all initial batch sizes _n_ , the error is low and decreases when the number of observations increases. It means that the computed threshold _z_<sup>SPOT</sup> is close to the theoretical one and tends to it. 

Secondly, we have to notice that the error curves all converge to the same value regardless of _n_ . Therefore, _n_ is not a paramount parameter. In our experiments, we just have to ensure that _n_ is not too small, otherwise the initialization step is likely to fail because of a lack of peaks to perform the GPD fit. Generally, we use _n ≃_ 1000. 


![](Anomaly_Detection_in_Streams_with_Extreme_Value_Theory_images/Anomaly_Detection_in_Streams_with_Extreme_Value_Theory.pdf-0008-03.png)


**Figure 5: Error rate with the number of observations according to the batch size** _n_ 

#### **5.2 Finding anomalies with SPOT** 

##### _5.2.1 Intrusion detection example_ 

SPOT computes a robust threshold estimation ( _zq_ ): the more data we monitor, the more accurate the estimation is. So having a lot of data from the same and unknown distribution, SPOT can gradually adapt this threshold in order to detect anomalies. Cyber-security is a typical field where such configurations appear. 

To test our algorithm we use real data from the MAWI repository which contains daily network captures (15 minutes a day stored in a `.pcap` file). In these captures, MAWIlab [19] finds anomalies and labels them with the taxonomy proposed by Mazel _et al._ [25]. The anomalies are referred through detailed patterns. To be close to real monitoring systems we converted raw `.pcap` files into NetFlow format, which aggregates packets and retrieves meta-data only, and is commonly used to measure network activity. Then we labeled the flows according to the patterns given by the MAWIlab. In this experiment we use the two captures from the 17/08/2012 and the 18/08/2012. 

Classical attacks are network scans where many SYN packets are sent in order to find open and potentially vulnerable ports on several machines. A relevant feature to detect such attack is the ratio of SYN packets in a given time window [17]. From our NetFlow records we compute this feature on successive 50 ms time windows and we try to find extreme events. To initialize SPOT we use the last 1000 values of the 17/08 record and we let the algorithm working on the 18/08 capture. 


![](Anomaly_Detection_in_Streams_with_Extreme_Value_Theory_images/Anomaly_Detection_in_Streams_with_Extreme_Value_Theory.pdf-0008-10.png)


**Figure 6: SYN flood detection at level** _q_ = 10<sup>_−_4</sup> 

The figure 6 shows the alerts triggered by SPOT (red circles). We recall that each point represents a 50 ms window gathering several flows (possibly benign and malicious). The computed threshold (dashed line) seems nearly constant but this behavior is due to the stability of the measure we monitor (SPOT has quickly inferred the behavior of the feature). By flagging all the flows in the triggered windows, we get a true positive rate equal to 86% with less than 4% of false positives. 

##### _5.2.2 The parameter q as a false-positive regulator_ 

In the previous section we noticed that the size of the initial batch _n_ is not an important parameter insofar as it does not affect the overall behavior of SPOT. Here, we study the impact of the main parameter _q_ on the MAWI dataset. 

On the figure 7, the ROC curve shows the effect of _q_ on the False Positive rate (FPr). Values of _q_ between 10<sup>_−_3</sup> and 10<sup>_−_5</sup> allow to have a high TPr while keeping a low FPr: this leaves some room for error when setting _q_ . 


![](Anomaly_Detection_in_Streams_with_Extreme_Value_Theory_images/Anomaly_Detection_in_Streams_with_Extreme_Value_Theory.pdf-0008-16.png)


**Figure 7: ROC curves on MAWI dataset (the markers give the corresponding value of** _q_ **)** 

#### **5.3 Finding anomalies with DSPOT** 

##### _5.3.1 Measure of the magnetic field_ 

To show the wide variety of fields on which we can use DSPOT, we apply our algorithm on astrophysics measures 

7 

from the SPIDR (Space Physics Interactive Data Resource) [4]. SPIDR is an online platform which stores and manages historical space physics data for integration with environment models and space weather forecasts. 

Particularly we use a dataset available on Comp-Engine Time Series [3] which gathers some physical measures taken by the ACE satellite between 1/1/1995 and 1/6/1995. In the figure 8 we monitor a component of the magnetic field (in nT) during several minutes. 

This time series is very noisy and contains different complex behaviors. We calibrate DSPOT with the _n_ = 2000 first values and we run on the 15801 others with _q_ = 10<sup>_−_3</sup> and _d_ = 450. The results are depicted on the figure 8. 


![](Anomaly_Detection_in_Streams_with_Extreme_Value_Theory_images/Anomaly_Detection_in_Streams_with_Extreme_Value_Theory.pdf-0009-03.png)


**Figure 8: DSPOT run with** _q_ = 10<sup>_−_3</sup> _, d_ = 450 

At the first glance, the bounds are following the signal and some alarms are triggered by high peaks. After 9000 minutes, the upper bound seems higher than expected. 

To understand why, let us divide the signal into two parts: before and after 8000 minutes. Before 8000, we can observe that “peaks” lean upwards the trend although the opposite phenomenon appears after 8000. During these 8000 first minutes, DSPOT learns that peaks may lean upwards the trend and it keeps this information in memory. Hence after 8000 minutes, the upper bound stays high in order to accommodate for possible peaks above the trend. DSPOT has this behavior because it keeps a global memory of all peaks encountered. If it was not desired, un easy modification is to keep only the last _k_ peaks, for a fixed _k_ . 

##### _5.3.2 Stock prices_ 

On Thursday the 9th of February 2017, an explosion happened at Flamanville nuclear plant, in northern France. This power plant is managed by EDF, a French electricity provider. The incident was not in the nuclear zone and did not hurt people [5]. This incident was officially declared at 11:00 a.m. making the EDF stock price fall down. This recent event encouraged us to test DSPOT on EDF stock prices. 

Obviously, retrieving financial data with high resolution is not within ours grasp. However, some websites like Google Finance [2] propose intraday financial data with a record per minute. Google Finance keeps these records during 15 days, so we retrieve the records from the 6th to the 8th of February 2017 for calibration (1062 values) and ran DSPOT on the explosion day (379 values). 

On figure 9, we notice that DSPOT follows the average behavior and flags the drop around 11:00 a.m. This may help 

a trading system to quickly take actions or warn experts. 


![](Anomaly_Detection_in_Streams_with_Extreme_Value_Theory_images/Anomaly_Detection_in_Streams_with_Extreme_Value_Theory.pdf-0009-12.png)


**Figure 9: DSPOT run with** _q_ = 10<sup>_−_3</sup> _, d_ = 10 

#### **5.4 Performances** 

Here we give some details about the time and memory performances of our `python3` implementation. All these experiments have been made on a laptop with an Intel i5-5300U CPU @ 2.30GHz (4 cores) and 8 GB RAM. 

Both algorithms, SPOT and DSPOT require a fixed memory size for all the variables except for the peak set **Y** _t_ which may grow with the number of observations. To measure the memory performance of our algorithm we report the number of peaks we stored. 

To test the performances of our algorithms we run each of them on 100 Gaussian white noises of 15000 values (like the experiment in section 5.1). At every run we measure the averaged time to perform one iteration and the ratio of stored peaks, i.e. the number of peaks over the number of observations. 

For these experiments we set _q_ = 10<sup>_−_3</sup> and we use _n_ = 1000 values for the initial batch. We record these measures in four contexts: SPOT, SPOT both sides (bi-SPOT), DSPOT and DSPOT both sides (bi-DSPOT). The “both sides” runs take into account upper and lower thresholds updates. In drifting cases, we add a drift to the Gaussian white noise and we use a depth _d_ = 50. 

The table 2 presents the averaged time to perform one iteration (denoted T, measured in _µ_ s) and the ratio number of peaks over number of observations at the end of the run (denoted M, in %) in mean, best and worst cases. 

|Mthd|Wo|rst|M|ean|B|est|
|---|---|---|---|---|---|---|
|eo|T|M|T|M|T|M|
|SPOT|959|2,70|351|1,90|141|1,40|
|DSPOT|883|3,49|391|2,02|197|1,07|
|bi-SPOT|1733|5,58|772|4,18|373|2,79|
|bi-DSPOT|1053|5,79|591|4,02|272|2,74|



**Table 2: Time (T, in** _µ_ **s) and Memory (M, in** % **) performances** 

Our algorithm stores a little ratio of all the stream (few percents). Logically we store about twice more when we compute upper and lower thresholds. Even if the growth speed of the peaks sets size is low it could be an hindrance for a long term monitoring. However, the size of the peaks 

8 

set could be upper-bounded (with a high bound) making it work like a wide sliding window (very old peaks would be dropped) without loss of accuracy. 

Finally the time performances of our algorithms show that our implementation is able to work on streams with more than 1000 values a second. 

#### **6. CONCLUSION** 

This paper has presented a novel approach to detect outliers in high throughput numerical time series. The key points of our approach is that it does not assume the data distribution, and it does not require manually set thresholds. It adapts on multiple and complex contexts, learning how the interest measure behaves. It achieves these results by using the Extreme Values Theory (EVT). To the best of our knowledge, it is the first time EVT has been used to detect outliers in streaming data. 

There are two kinds of perspectives. From the theoretical side, in this paper we only exploited a small part of EVT, we would like to extend this work to the multivariate case and to non-iid observations. 

From the practical side, one of the immediate application of our approach is _automatic thresholding_ : it can provide thresholds with strong statistical guarantees that can adapt to the evolution of a data stream. We wold like to explore the use of our approach as a building block into more complex systems that require thresholding. Also the EVT on multivariate cases could address our problem in more general contexts without independence condition 

#### **7. REFERENCES** 

- [1] git clone https://scm.gforge.inria.fr/ anonscm/git/siffer/siffer.git. 

- [2] Google finance. https://www.google.com/finance. 

- [3] Magnetic field time series. http://www.comp-engine. org/timeseries/time-serie ~~s d~~ ata/data-17481/. 

- [4] Space physics interactive data resource. http://spidr.ionosonde.net/spidr/home.do. 

- [5] http://www.webcitation.org/6oAxqoFkf. 

- [6] D. Agarwal. An empirical bayes approach to detect anomalies in dynamic multidimensional arrays. In _ICDM_ , 2005. 

- [7] F. Angiulli, S. Basta, and C. Pizzuti. Distance-based detection and prediction of outliers. _IEEE transactions on knowledge and data engineering_ , 2006. 

- [8] F. Angiulli and F. Fassetti. Detecting distance-based outliers in streams of data. In _Proceedings of the 16th ACM conference on Conference on information and knowledge management_ , 2007. 

- [9] A. A. Balkema and L. De Haan. Residual life time at great age. _The Annals of probability_ , 1974. 

- [10] J. Beirlant, Y. Goegebeur, J. Segers, and J. Teugels. _Statistics of extremes: theory and applications_ . John Wiley & Sons, 2006. 

- [11] M. M. Breunig, H.-P. Kriegel, R. T. Ng, and J. Sander. Lof: identifying density-based local outliers. In _ACM sigmod record_ , volume 29, pages 93–104. ACM, 2000. 

- [12] R. H. Byrd, P. Lu, J. Nocedal, and C. Zhu. A limited memory algorithm for bound constrained optimization. _SIAM J. on Scientific Computing_ , 1995. 

- [13] V. Chandola, A. Banerjee, and V. Kumar. Anomaly detection: A survey. _ACM computing surveys_ , 2009. 

- [14] L. Duan, L. Xu, Y. Liu, and J. Lee. Cluster-based outlier detection. _Annals of Operations Research_ , 168(1):151–168, 2009. 

- [15] M. Elahi, K. Li, W. Nisar, X. Lv, and H. Wang. Efficient clustering-based outlier detection algorithm for dynamic data stream. In _FSKD’08_ , 2008. 

- [16] E. Eskin. Anomaly detection over noisy data using learned probability distributions. In _ICML_ , 2000. 

- [17] G. Fernandes and P. Owezarski. Automated classification of network traffic anomalies. In _ICSPCS_ , 2009. 

- [18] R. A. Fisher and L. H. C. Tippett. Limiting forms of the frequency distribution of the largest or smallest member of a sample. In _Mathematical Proceedings of the Cambridge Philosophical Society_ , 1928. 

- [19] R. Fontugne, P. Borgnat, P. Abry, and K. Fukuda. MAWILab: Combining Diverse Anomaly Detectors for Automated Anomaly Labeling and Performance Benchmarking. In _ACM CoNEXT ’10_ , 2010. 

- [20] B. Gnedenko. Sur la distribution limite du terme maximum d’une serie aleatoire. _Annals of mathematics_ , pages 423–453, 1943. 

- [21] S. D. Grimshaw. Computing maximum likelihood estimates for the generalized pareto distribution. _Technometrics_ , 35(2):185–191, 1993. 

- [22] B. M. Hill. A simple general approach to inference about the tail of a distribution. _The annals of statistics_ , 3(5):1163–1174, 1975. 

- [23] L. I. Kuncheva. Classifier ensembles for detecting concept change in streaming data: Overview and perspectives. In _2nd Workshop SUEMA_ , 2008. 

- [24] R. Laxhammar and G. Falkman. Online learning and sequential anomaly detection in trajectories. _IEEE transactions on pattern analysis and machine intelligence_ , 36(6):1158–1173, 2014. 

- [25] J. Mazel, R. Fontugne, and K. Fukuda. A taxonomy of anomalies in backbone network traffic. In _IWCMC_ , 2014. 

- [26] E. Ngai, Y. Hu, Y. Wong, Y. Chen, and X. Sun. The application of data mining techniques in financial fraud detection: A classification framework and an academic review of literature. _Decision Support Systems_ , 50(3):559–569, 2011. 

- [27] J. Pickands III. Statistical inference using extreme order statistics. _the Annals of Statistics_ , 1975. 

- [28] M. S. Sadik and L. Gruenwald. Dbod-ds: Distance based outlier detection for data streams. In _International Conference on Database and Expert Systems Applications_ , pages 122–136. Springer, 2010. 

- [29] S. Sadik and L. Gruenwald. Research issues in outlier detection for data streams. _ACM SIGKDD Explorations Newsletter_ , 15(1):33–40, 2014. 

- [30] J. E. Seem. Using intelligent data analysis to detect abnormal energy consumption in buildings. _Energy and buildings_ , 39(1):52–58, 2007. 

- [31] D. Toshniwal. A framework for outlier detection in evolving data streams by weighting attributes in clustering. _Procedia Technology_ , 6:214–222, 2012. 

- [32] H. Wang, D. Zhang, and K. G. Shin. Detecting syn flooding attacks. In _INFOCOM_ , 2002. 

9 

