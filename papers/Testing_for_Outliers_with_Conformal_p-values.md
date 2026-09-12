# Testing for Outliers with Conformal p-values 

### Stephen Bates<sup>_∗_1</sup> , Emmanuel Cand`es<sup>2</sup> , Lihua Lei<sup>3</sup> , Yaniv Romano<sup>4</sup> , Matteo Sesia<sup>5</sup> 

May 26, 2022 

##### **Abstract** 

This paper studies the construction of p-values for nonparametric outlier detection, taking a multiple-testing perspective. The goal is to test whether new independent samples belong to the same distribution as a reference data set or are outliers. We propose a solution based on conformal inference, a broadly applicable framework which yields p-values that are marginally valid but mutually dependent for different test points. We prove these p-values are positively dependent and enable exact false discovery rate control, although in a relatively weak marginal sense. We then introduce a new method to compute p-values that are both valid conditionally on the training data and independent of each other for different test points; this paves the way to stronger type-I error guarantees. Our results depart from classical conformal inference as we leverage concentration inequalities rather than combinatorial arguments to establish our finitesample guarantees. Furthermore, our techniques also yield a uniform confidence bound for the false positive rate of any outlier detection algorithm, as a function of the threshold applied to its raw statistics. Finally, the relevance of our results is demonstrated by numerical experiments on real and simulated data. 

**_Keywords—_** Conformal inference, out-of-distribution testing, false discovery rate, positive dependence. 

## **1 Introduction** 

### **1.1 Problem statement and motivation** 

We consider an outlier detection problem in which one observes a data set _D_ = _{Xi}_<sup>2</sup> _i_ =1<sup>_n_containing2</sup><sup>_n_</sup> independent and identically distributed points _Xi ∈_ R<sup>_d_</sup> drawn from an unknown distribution _PX_ (which may be continuous, discrete, or mixed). The goal is to test which among a new set of _n_ test _≥_ 1 independent observations _D_<sup>test</sup> = _{X_ 2 _n_ + _i}_<sup>_n_</sup> _i_ =1<sup>test</sup> are _outliers_ , in the sense that they were not drawn from the same distribution _PX_ . By contrast, we refer to points drawn from _PX_ as _inliers_ . This problem has applications in many domains, including medical diagnostics [1], spotting frauds or intrusions [2], forensic analysis [3], monitoring engineering systems for failures [4], and _out-of-distribution_ detection in machine learning [5–8]. A variety of machine-learning tools have been developed to address this classification task, which is sometimes referred to as _one-class classification_ [9, 10] because the data in _D_ do not contain any outliers. However, 

> _∗_ Authors listed alphabetically. 

> 1Departments of Statistics and of EECS, UC Berkeley. 

> 2Departments of Statistics and of Mathematics, Stanford University. 

> 3Department of Statistics, Stanford University. 

> 4Departments of Electrical Engineering and of Computer Science, Technion—Israel Institute of Technology. 

> 5Department of Data Sciences and Operations, University of Southern California. 

1 

such algorithms are often complex and their outputs are not directly covered by any precise statistical guarantees. Fortunately, conformal inference [11, 12] allows one to practically convert the output of any one-class classifier (if it is invariant to the ordering of the training observations) into a provably valid p-value for the null hypothesis _H_ 0 _,i_ : _Xi ∼ PX_ , for any _Xi ∈D_<sup>test</sup> . 

In many applications, the number of outlier tests, _n_ test, is large and, therefore, it may be necessary to account for multiple comparisons to avoid making an excessive number of false discoveries. A meaningful error rate in this setting is the false discovery rate (FDR) [13]: the expected proportion of true inliers among the test points reported as outliers. For example, if a particular financial transaction is labeled by an automated system as likely to be fraudulent (i.e., unusual, or out-of-distribution compared to a data set of normal transactions), someone may then need to review it manually, and possibly contact the involved customer. Since these follow-up procedures have a cost, controlling the FDR may be a sensible solution to ensure resources are allocated efficiently. From a statistical perspective, multiple testing in this setting requires some care because classical conformal p-values corresponding to different values of _i >_ 2 _n_ are independent of each other only conditional on _D_ , although they are valid only marginally over _D_ . This situation is delicate because FDR control typically requires p-values that either are mutually independent or follow certain patterns of dependence [14, 15]. Similarly, global testing (i.e., aggregating evidence from multiple observations to test weaker batch-level hypotheses) may also require independent p-values. This paper addresses the above issues by carefully studying the theoretical properties of some standard multiple testing procedures applied to conformal p-values, and by developing new methods to compute p-values with stronger validity properties. 

The conformal inference methods studied in this paper are statistical wrappers for one-class classifiers. The latter are algorithms trained on data clean of any outliers to compute a score function _s_ ˆ : R<sup>_d_</sup> _→_ R assigning a scalar value to any future data point, so that smaller (for example) values of _s_ ˆ( _X_ ) provide evidence that _X_ may be an outlier. By design, the classifier attempts to construct scores that separate outliers from inliers effectively, by learning from the data what inliers typically look like, and it may be based on sophisticated black-box models to maximize power. While often effective in practice, these machinelearning algorithms have the drawback of not offering any clear guarantees about the quality of their output. For example, they do not directly provide a null distribution for the classification scores _s_ ˆ evaluated on true inliers, or any particular threshold to limit the rate of false positives. This is where conformal inference ˆ comes to help. After training _s_ on a subset of the observations in _D_ , namely those in _D_<sup>train</sup> = _{X_ 1 _, . . . , Xn}_ , the scores are evaluated on the remaining _n_ hold-out samples in _D_<sup>cal</sup> = _{Xn_ +1 _, . . . , X_ 2 _n}_ . (Note that _D_<sup>train</sup> and _D_<sup>cal</sup> do not need to contain the same number of observations, although the current choice simplifies the notation without loss of generality). Let us assume, for simplicity, that _s_ ˆ( _X_ ) has a continuous distribution ˆ if _X ∼ PX_ is independent of the data used to train _s_ , although this assumption could be relaxed at the cost of some additional technical details. Then, define _F_ as the cumulative distribution function (CDF) of _s_ ˆ( _X_ ). If we knew _F_ , we could utilize _F_ (ˆ _s_ ( _Xi_ )) as an exact p-value for the null hypothesis _H_ 0 _,i_ : _Xi ∼ PX_ , for any _Xi ∈D_<sup>test</sup> , in the sense that _F_ (ˆ _s_ ( _Xi_ )) would be uniformly distributed if _H_ 0 _,i_ is true. In practice, however, we do not have direct access to _F_ because _PX_ is unknown and the machine-learning algorithm upon which _s_ ˆ depends is assumed to be a black-box. Instead, we can evaluate the empirical CDF of _s_ ˆ( _Xi_ ) for all _Xi ∈D_<sup>cal</sup> , which we denote as _F_<sup>ˆ</sup> _n_ . In the following, we will discuss how to construct provably valid conformal p-values for a future observation _X_ 2 _n_ +1 by evaluating 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0002-03.png)


where _g_ is a suitable _adjustment function_ , and the symbol _◦_ denotes a composition; i.e., ( _f ◦ g_ )( _x_ ) = _f_ ( _g_ ( _x_ )). Note that, hereafter, we will treat the observations in _D_<sup>train</sup> as fixed and focus on the randomness in the calibration ( _D_<sup>cal</sup> ) and test ( _D_<sup>test</sup> ) data, upon which conformal inferences are generally based. 

2 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0003-00.png)


Figure 1: Visualization of the joint distribution of the conformal p-values. The distribution of _s_ ˆ( _x_ ) is the same for calibration and inlier test points. The conformal p-value for each test point is the number of calibration points to its left, divided by the total number of calibration points plus one, as in (3). 

### **1.2 Preview of contributions** 

In Section 2, we will focus on the classical conformal inference methods, which produce _marginally superuniform_ (conservative) p-values _u_ ˆ<sup>(marg)</sup> ( _X_ 2 _n_ +1) satisfying 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0003-04.png)


for any _t ∈_ (0 _,_ 1), whenever _X_ 2 _n_ +1 is an inlier. We say these p-values are marginally valid because they depend on the calibration data in _D_<sup>cal</sup> , and both _D_<sup>cal</sup> and _X_ 2 _n_ +1 are random in (2). In particular, the classical _u_ ˆ<sup>(marg)</sup> is computed by applying the adjustment function _g_<sup>(marg)</sup> ( _x_ ) = ( _nx_ + 1) _/_ ( _n_ + 1) to (1), i.e., 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0003-06.png)


Note that (2) is implied by (3) because when _s_ ˆ( _X_ ) follows a continuous distribution, _u_ ˆ<sup>(marg)</sup> ( _X_ ) is uniformly distributed on _{_ 1 _/_ ( _n_ + 1) _,_ 2 _/_ ( _n_ + 1) _, . . . ,_ 1 _}_ if _X ∼ PX_ independently of the data in _D_<sup>train</sup> [11, 12]. (If _s_ ˆ( _X_ ) is not continuous, one can still verify that _u_ ˆ<sup>(marg)</sup> ( _X_ ) is super-uniform in distribution.) However, this ˆ is not necessarily true if one conditions on _D_ = _D_<sup>train</sup> _∪D_<sup>cal</sup> , in which case _u_<sup>(marg)</sup> ( _X_ ) may become anticonservative due to random fluctuations in the distribution of scores within _D_<sup>cal</sup> . Intuitively, this means the marginal p-values in (3) are only valid _on average_ if data in _D_<sup>cal</sup> are treated as random. Unfortunately, this guarantee may be too weak to be satisfactory for a practitioner who wants to compute p-values for a large number of test points but is constrained to working with a single calibration data set. Indeed, the numerical experiments presented in Section 5.2 will show that inferences based on marginal conformal p-values may be systematically invalid for a large fraction of practitioners working with “unlucky” calibration data sets. 

ˆ Furthermore, marginal p-values corresponding to different test points, _{u_<sup>(marg)</sup> ( _X_ ) _}X∈D_ test, are not mutually independent because they are all affected by _D_<sup>cal</sup> ; see Figure 1 for a visualization of this dependence. This should be taken into account when adjusting for multiplicity in outlier detection applications because some common testing procedures are not generally valid for dependent p-values. For example, we will prove in Section 2 that the dependence among marginal p-values invalidates Fisher’s combination test [16] for the global null that there are no outliers in _D_<sup>test</sup> , even if the calibration data in _D_<sup>cal</sup> are treated as random, although this can be easily fixed by suitably adjusting the critical value. By contrast, we can prove the dependence between conformal p-values does not break the _average_ FDR control of the Benjamini-Hochberg (BH) procedure [13], even if the latter is applied with Storey’s correction [17]. The behaviours of additional multiple testing procedures, such as the harmonic mean [18], Simes method [19], and Stouffer’s method [20], applied to conformal p-values will be investigated empirically in Section 5. 

In any case, regardless of whether the mutual dependence among marginal p-values theoretically invalidates the average inferences of a particular multiple-testing procedure, one may sometimes be interested in obtaining stronger guarantees conditional on the calibration data. Consider for instance the following prototypical scenario. A researcher, or a company, acquires an expensive data set _D_ containing clean examples of some variable _X_ of interest, and wishes to leverage that information to construct a system to detect outliers in future test points, while avoiding an excess of false positives. Assuming the stakes in this application are sufficiently high, the researcher may need clear statistical guarantees about the output of such procedure (as opposed to blindly trusting a black-box model), and thus decides to employ conformal inference. Unfortunately, the marginal validity property in (2) tells us very little about how this outlier detection system may 

3 

perform in the future for _this particular researcher relying on this particular data set D_ . Instead, marginal validity suggests the system will work _on average_ for different researchers starting from different data sets; of course, that may not feel fully satisfactory for any one of them. 

Therefore, we will construct in Section 3 conformal p-values satisfying a stronger property, which we call _calibration-conditional validity_ (CCV). Formally, the novel p-values _u_ ˆ<sup>(ccv)</sup> ( _x_ ) will satisfy 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0004-02.png)


if _X_ 2 _n_ +1 _∼ PX_ , for any value of _δ ∈_ (0 _,_ 1) pre-specified by the user. The crucial difference between (4) and (2) is that the latter intuitively guarantees the p-values are valid for at least a fraction 1 _− δ_ of researchers; this can give a precise measure of confidence to each one of them. Furthermore, calibration-conditional p-values have the advantage of making multiple testing straightforward. In fact, these p-values are still trivially independent of one another conditional on the calibration data, so their high-probability guarantee of validity will immediately extend to the output of any downstream multiple-testing procedure that assumes independence. 

While most of this paper focuses on the validity of conformal p-values from a multiple-testing perspective, we will see in Section 4 that our high-probability results can also be utilized to construct a uniform upper confidence bound for the false positive rate of any machine-learning algorithm for outlier detection, as a function of the threshold applied to its raw output scores. This may help practitioners interpret the output of black-box methods directly, without necessarily operating in terms of p-values. (However, as statisticians, we prefer the p-value approach because it is more versatile.) Furthermore, our results can be easily leveraged to obtain predictive sets with stronger coverage guarantees compared to existing conformal methods. 

Finally, in Section 5, we will compare the performance of marginal and calibration-conditional conformal p-values on simulated as well as real data, in combination with different multiple testing procedures. These numerical experiments will provide an empirical confirmation of our theoretical results, and also highlight how stronger guarantees sometimes come at the cost of lower power. 

### **1.3 Related work** 

The outlier detection problem considered in this paper is fully non-parametric, in the sense that we leverage the information contained in an external clean data set, and nothing else, to infer whether a future test point may be an outlier. This is in contrast with the more classical problem of multivariate outlier detection within a single data set, leveraging modeling assumptions rather than clean external samples [21–24]. A wealth of data mining and machine-learning methods have been developed to address our non-parametric task [25–29]; these do not provide precise finite-sample guarantees on their own, but we can leverage them to compute scoring functions that powerfully separate outliers from inliers. 

Our paper is based on conformal inference [11, 12], which has been applied before in the context of outlier detection [30–35]. However, previous works did not study the implications of marginal p-values on the validity of multiple outlier testing procedures, nor did they seek the conditional guarantees obtained here. Another line of work applied conformal inference to test the global null for streaming data [36–40]. However, the guarantee no longer holds in the offline setting or beyond the global null. The most closely related work is that of [41], which extends conformal inference to provide a form of calibration-conditional coverage. That paper focused explicitly on the prediction setting rather than on outlier detection, but is also directly relevant in our context, as discussed in Section 3.1. The main difference is that our novel high-probability bounds in Section 3 hold simultaneously for all possible coverage levels (in the language of [41]) not just for a pre-specified one—this feature being necessary to obtain conditionally valid p-values for multiple outlier testing. 

Other works on conformal inference focused on different types of conditional coverage. For example, [42] studied the difficulty of computing valid conformal predictions (in a supervised setting) conditional on the features of a new test point, while we are interested in conditioning on the calibration data (in an outlier detection setting). Other works have focused on seeking approximate feature-conditional coverage 

4 

in multi-class classification [43–46] or in regression problems [47–51]. This paper is orthogonal, in the sense that our results could be applied to strengthen their coverage guarantees by conditioning on the calibration data. It should be noted that, although conformal inference can be based on different data holdout strategies [52–54], our paper focuses on sample splitting [55, 56]. The latter has the advantage of being the most computationally efficient option, and is necessary for us in theory because our high-probability bounds require the independence of the data points in addition to their exchangeability. 

Further, the problem we consider is related to classical two-sample testing [57], although we take a different perspective. Two-sample testing compares two data sets to determine whether they were sampled from the same distribution, while our goal is to contrast many independent test points (or batches thereof) to the same reference set accounting for multiplicity. In any case, several recent works have explored the use of machine-learning and data hold-out methods for two-sample testing [58–62], which reinforces the connection with our work. 

Finally, the duality between hypothesis testing and confidence intervals connects our conditionally calibrated p-values to the classical statistical topic of _tolerance regions_ , which goes back to Wilks [63, 64], Wald [65], and Tukey [66]. See [67] for a overview of the subject, [41] for a discussion of their connection with conformal inference, and [68, 69] for modern examples using tolerance regions for predictive inference with neural networks. (Tolerance regions are predictive sets with a high-probability guarantee to contain the desired fraction of the population. For example, one can generate a tolerance region guaranteed to contain at least 80% of the population with probability 99%.) The construction of predictive intervals with (asymptotic) conditional validity in the aforementioned sense was also recently studied in [70] with bootstrap rather than conformal inference methods. 

## **2 Marginal conformal inference for outlier detection** 

Before turning to calibration-conditional inferences, we carefully study the marginal validity of multiple tests based on split-conformal outlier detection p-values. The conformal p-values defined in (3) are marginally valid for the hypothesis that a single test point follows the distribution _PX_ , see (2), but they are not independent of each other when considering multiple test points. Consequently, we show they cannot be naively used to test a global null hypothesis that no points in a particular test set are outliers, with Fisher’s combination test [16] for example. The failure of Fisher’s test is caused by the particular dependence induced by the shared calibration data set, although other procedures turn out to be robust to such dependence. In particular, we then prove conformal p-values are _positive regression dependent on a subset_ (PRDS), which combined with the results of [14], implies the BH procedure will control the FDR. 

### **2.1 A negative result: global testing with conformal p-values can fail** 

Fisher’s combination test [16] is a widely-used method to test the global null, in our case 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0005-07.png)


The idea is to aggregate the evidence from the individual tests, as follows. Given a p-value _pi_ for each null hypothesis _i_ , Fisher’s test rejects the global null at level _α_ if 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0005-09.png)


where _χ_<sup>2</sup> (2 _m_ ; 1 _−α_ ) is the (1 _−α_ )-th quantile of the chi-square distribution with 2 _m_ degrees of freedom. This test is valid if the p-values stochastically dominate Unif([0 _,_ 1]) and are independent of each other. However, we prove in the following lemma that the standard (marginal) conformal p-values are positively correlated under arbitrary transformations, suggesting an inflation of the variance of the combination statistics. 

5 

**Lemma 1.** _Assume that s_ ˆ( _X_ ) _is continuously distributed. Then, for any finite-valued function G_ : [0 _,_ 1] _�→_ R _, and for any pair of nulls_ ( _i, j_ ) _,_ 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0006-01.png)


Motivated by Lemma 1 (see Appendix A.1 for a detailed discussion), we obtain the following result which shows Fisher’s combination test becomes invalid when applied to marginal conformal p-values. In particular, we characterize its type-I error in the asymptotic regime where _|D_<sup>test</sup> _|_ is proportional to _|D_<sup>cal</sup> _|_ . 

**Theorem 1** (Type-I error of Fisher’s combination test) **.** _Assume that s_ ˆ( _X_ ) _is continuously distributed. Then, under the global null, if m_ = _⌊γn⌋ for some γ ∈_ (0 _, ∞_ ) _, as n tends to infinity,_ 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0006-04.png)


_where z_ 1 _−α and_ Φ<sup>¯</sup> _denote the_ (1 _− α_ ) _-th quantile and survival function of the standard normal distribution, respectively. Furthermore, under the same asymptotic regime, for W ∼ N_ (0 _,_ 1) _,_ 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0006-06.png)


Note that the above asymptotic limits are independent of the distribution of _s_ ˆ( _X_ ). In Appendix A, we prove that Theorem 1 holds for a broad class of combination tests based on<sup>�</sup><sup>_n_</sup> _i_ =1<sup>_G_(ˆ</sup><sup>_u_(marg)(</sup><sup>_X_2</sup><sup>_n_+</sup><sup>_i_)),</sup> provided that _G_ ( _U_ ) has finite moments for _U ∼_ Unif([0 _,_ 1]); Fisher’s combination test is a special case with _G_ ( _u_ ) = _−_ 2 log _u_ and _G_ ( _U_ ) _∼ χ_<sup>2</sup> (2). 

Since _γ >_ 0, the marginal type-I error is always larger than _α_ whenever _α <_ 0 _._ 5. For illustration, consider _α_ = 5%. When _γ_ = 3, the marginal type-I error is as large as 20 _._ 5%; when _γ →∞_ , the marginal type-I error is approaching 50%. Similarly, by (5), the 90-th percentile of the conditional type-I error converges to the 90-th percentile of Φ(<sup>¯</sup> _z_ 1 _−q_ +<sup>_√_</sup> _<u>γW</u>_ ), which is Φ(<sup>¯</sup> _z_ 0 _._ 95 +<sup>_√_</sup> _<u>γz</u>_ 0 _._ 1). When _γ_ = 3, the limit is 71 _._ 7%; when _γ →∞_ , the limit is approaching 100%. This demonstrates the substantial adverse effect of dependence among marginal conformal p-values for Fisher’s combination test. 

Corrections of Fisher’s combination test are possible for some dependence structures. By Lemma 1, the variance of the combination statistic is inflated by a factor (1 + _γ_ ) compared to that of the _χ_<sup>2</sup> (2 _m_ ; 1 _− α_ ) distribution (see Appendix A.1 for details). This yields an intuitive correction which divides the combination statistic by<sup>_√_</sup> 1 + _γ_ . Surprisingly, this correction is asymptotically too conservative for marginal conformal p-values. We prove in Appendix A.2 (Theorem 6) that a valid correction rejects the global null if 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0006-10.png)


In Appendix A.2, we also confirm the validity of (6) via Monte-Carlo simulations and show this is asymptotically equivalent to the correction proposed by [71, 72] to address p-value dependence in more general contexts. 

### **2.2 A positive result: conformal p-values are positively dependent** 

Certain multiple testing methods, such as the BH procedure, are known to be robust to a particular type of mutual p-value dependence called _positive regression dependent on a subset_ (PRDS) [14]. 

**Definition 1.** _A random vector X_ = ( _X_ 1 _, . . . , Xm_ ) _is PRDS on a set I_ 0 _⊂{_ 1 _, . . . , m} if for any i ∈ I_ 0 _and any increasing set A, the probability_ P[ _X ∈ A | Xi_ = _x_ ] _is increasing in x._ 

6 

In the multiple testing literature, _X_ is often said to be PRDS if it is PRDS on the set of nulls. Above, for vectors _a_ and _b_ of equal dimension, we say _a ⪰ b_ if every coordinate of _a_ is no smaller than the corresponding coordinate of _b_ , and a set _A ⊂_ R<sup>_m_</sup> is _increasing_ if _a ∈ A_ and _b ⪰ a_ implies _b ∈ A_ . The PRDS property is a demanding form of positive dependence which can be interpreted, loosely speaking, as saying all pairwise correlations are positive. In view of the definition of marginal p-values in (3) and the result in Lemma 1, it should be intuitive that larger scores in the calibration set make the p-values for all test points simultaneously smaller, and vice-versa. This idea is formalized by the following result proving marginal conformal p-values are PRDS. 

**Theorem 2** (Conformal p-values are PRDS) **.** _Assume that s_ ˆ( _X_ ) _is continuously distributed. Consider m test points X_ 2 _n_ +1 _, . . . , X_ 2 _n_ + _m such that the inliers are jointly independent of each other and of the data in D. Then, the marginal conformal p-values_ (ˆ _u_<sup>(marg)</sup> ( _X_ 2 _n_ +1) _, . . . ,_ ˆ _u_<sup>(marg)</sup> ( _X_ 2 _n_ + _m_ )) _are PRDS on the set of inliers._ 

When _s_ ˆ( _X_ ) is not continuous, we can also prove the PRDS property by modifying the definition (3) of marginal conformal p-values; see Appendix A.3 for details. It follows from Theorem 2 that marginal conformal p-values can be used to control the FDR with the BH procedure for the null hypotheses 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0007-03.png)


**Corollary 1** (Benjamini and Yekutieli [14]) **.** _In the setting of Theorem 2, the BH procedure applied at level α ∈_ (0 _,_ 1) _to_ (ˆ _u_<sup>(marg)</sup> ( _X_ 2 _n_ +1) _, . . . ,_ ˆ _u_<sup>(marg)</sup> ( _X_ 2 _n_ + _m_ )) _controls the FDR at level π_ 0 _α, where π_ 0 _is the proportion of true nulls. That is,_ 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0007-05.png)


_where H_ 0 = _{i_ : _H_ 0 _,i holds} ⊆{_ 2 _n_ + 1 _, . . . ,_ 2 _n_ + _m} is the subset of true inliers in the test set, and R ⊆{_ 2 _n_ + 1 _, . . . ,_ 2 _n_ + _m} is the subset of test points reported as likely outliers._ 

**Remark 1.** _It turns out that the BH procedure applied to the marginal conformal p-values is equivalent to the semi-supervised BH procedure proposed by [73] (posted on arXiv two months after our paper), which was first studied by [74] and later generalized by [75] and [76]. These works employ a martingale-based technique to prove the FDR control without relying on the PRDS property. Theorem 3.1 in [73] also proves a lower bound showing that the FDR is almost exactly π_ 0 _α._ 

This proves the FDR can be controlled, although only on average over the calibration data because the above expectation is taken over both _D_ and the future test points. While such marginal guarantee may be satisfactory for someone carrying out several independent applications, individual practitioners committed to a single calibration data set may prefer stronger results. 

### **2.3 A positive result: Storey’s correction does not break FDR control** 

When the proportion of nulls is much smaller than 1, as it may be the case in many out-of-distribution detection problems, the BH procedure is conservative, as shown in Corollary 1. If _π_ 0 is known, a simple remedy is to replace the target FDR level with _α/π_ 0. However, _π_ 0 is rarely known in practice and hence it needs to be estimated. Given p-values _pi_ for all null hypotheses, it was proposed by Storey et al. in [17, 77] to estimate _π_ 0 as 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0007-11.png)


and then to apply the BH procedure at level _α/π_ ˆ0; see Appendix A.4 for details. If the null p-values are super-uniform in the sense of (2), mutually independent, and independent of the non-null p-values, this provably controls the FDR in finite samples [17]. However, unlike in its standard version, the BH procedure with Storey’s correction may fail to control the FDR if the p-values are PRDS; see Section 6.3 of [78]. 

7 

Surprisingly, we show below that the positive correlation (Lemma 1) among the marginal conformal p-values does not break the FDR control at all. The proof of Theorem 3 rests on a novel FDR bound for the BH procedure with Storey’s correction applied to any type of super-uniform p-values that are PRDS and almost-surely bounded from below by a constant; see Theorem 7 in Appendix A.4. Note that this result is not limited to conformal p-values and may also be useful for other multiple testing problems, such as those involving permutation p-values. 

**Theorem 3** (Storey’s BH with conformal p-values controls the FDR) **.** _Set λ_ = _K/_ ( _n_ + 1) _for any integer K. Assume s_ ˆ( _X_ ) _is continuously distributed. In the setting of Corollary 1, the BH procedure with Storey’s correction applied at level α ∈_ (0 _,_ 1) _to the marginal p-values_ (ˆ _u_<sup>(marg)</sup> ( _X_ 2 _n_ +1) _, . . . ,_ ˆ _u_<sup>(marg)</sup> ( _X_ 2 _n_ + _m_ )) _controls the FDR at level α. That is,_ 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0008-02.png)


## **3 Calibration-conditional conformal p-values** 

### **3.1 Warm up: analyzing the false positive rate** 

Having noted that conformal inferences hold in theory only marginally over the calibration data, the first question one may ask is: how bad can these inferences be conditional on a particular calibration set? We will address this question by developing high-probability bounds for the conditional deviation from uniformity of marginal p-values, starting here from the simplest case of pointwise bounds. The purpose of a pointwise bound is to control the probability that a null p-value (corresponding to a true inlier) is smaller than _α_ , conditional on _D_ , for some _fixed_ threshold _α ∈_ (0 _,_ 1). In other words, we wish to understand the conditional false positives rate (FPR) corresponding to the threshold _α_ , 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0008-06.png)


beyond what we know from the marginal guarantee in (2), which is E [FPR( _α_ ; _D_ )] _≤ α_ . The quantity in (9) can be studied precisely with existing results due to [41]. We revisit this topic here because it serves as an intuitive introduction to the more involved high-probability bounds that we will propose later. 

Looking at the definition of _u_ ˆ<sup>(marg)</sup> ( _X_ ) in (3), we see that, if _s_ ˆ( _X_ ) has a continuous distribution, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0008-09.png)


where _F_ and _F_<sup>ˆ</sup> _n_ are, respectively, the true and empirical (evaluated on the calibration data) CDF of _s_ ˆ( _X_ ). Therefore, the deviation of FPR( _α_ ; _D_ ) (a random variable depending on _D_ ) from _α_ depends on the quality of _F_<sup>ˆ</sup> _n_<sup>_−_1((</sup><sup>_n_+ 1)</sup><sup>_α/n_)asanapproximationof</sup><sup>_F −_1(</sup><sup>_α_),whichcanbeunderstoodthroughclassicalresultsfor</sup> the order statistics of uniform variables. 

ˆ **Proposition 1** (Pointwise FPR of marginal conformal p-values, from [41]) **.** _Let ℓ_ = _⌊_ ( _n_ + 1) _α⌋. If s_ ( _X_ ) _is continuously distributed,_ FPR( _α_ ; _D_ ) _follows a_ Beta( _ℓ, n_ + 1 _− ℓ_ ) _distribution._ 

Figure 2 visualizes the FPR distribution from Proposition 1, due to [41], for different values of the calibration set size. This shows precisely how a smaller _D_<sup>cal</sup> makes marginal p-values more conservative on average, but also more likely to be overly liberal on occasion. For example, we can see there is a nonnegligible probability that FPR(0 _._ 1; _D_ ) _>_ 0 _._ 15 with 100 calibration points, whereas it seems very unlikely that FPR(0 _._ 1; _D_ ) _>_ 0 _._ 12 with 1600 calibration points. However, it is still quite possible that FPR(0 _._ 01; _D_ ) _>_ 0 _._ 015 even with 1600 calibration points. In general, Proposition 1 implies the coefficient of variation (relative spread) of the FPR is approximately proportional to ( _|D_<sup>cal</sup> _|α_ )<sup>_−_1</sup><sup>_/_2</sup> . While this result is informative and it is broadly relevant to the issue of how to best choose the number of calibration data points for split-conformal inference [79], it is limited for our purposes. In fact, it provides only a pointwise bound—it takes _α_ as fixed—whereas uniform bounds are needed to construct conditionally valid p-values that can be safely used with any multiple-testing procedure, as discussed in the next section. 

8 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0009-00.png)


Figure 2: Distribution of the false positive rate obtained by thresholding marginal conformal p-values at levels _α_ = 0 _._ 01 and _α_ = 0 _._ 1, as a function of the number of calibration points. 

### **3.2 A generic strategy to adjust marginal conformal p-values** 

Proposition 1 implies marginal conformal p-values may be anti-conservative conditional on _D_ . Therefore, in the language of (1), our goal is to find an adjustment function leading to conditionally valid p-values, i.e., satisfying (4). The following theorem suggests a generic strategy through a simultaneous upper confidence bound for order statistics. 

i _._ i _._ d _._ **Theorem 4** (Conditional p-value adjustment) **.** _Let U_ 1 _, . . . , Un ∼_ Unif([0 _,_ 1]) _, with order statistics U_ (1) _≤ U_ (2) _≤ . . . ≤ U_ ( _n_ ) _, and fix any δ ∈_ (0 _,_ 1) _. Suppose_ 0 _≤ b_ 1 _≤ b_ 2 _≤ . . . ≤ bn ≤_ 1 _are n reals such that_ 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0009-05.png)


_Let also b_ 0 = 0 _, bn_ +1 = 1 _, and h_ : [0 _,_ 1] _�→_ [0 _,_ 1] _be a piece-wise constant function such that_ 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0009-07.png)


ˆ ˆ ˆ _Then, u_<sup>(ccv)</sup> = _h ◦ u_<sup>(marg)</sup> _satisfies_ (4) _, i.e., u_<sup>(ccv)</sup> ( _X_ 2 _n_ +1) _is a calibration-conditional valid p-value._ 

Figure 3 illustrates the idea of Theorem 4. Here, we set _n_ = 1000 and generate 100 independent realizations of the order statistics ( _U_ (1) _, . . . , U_ ( _n_ )). Each of the 100 blue curves corresponds to a sample path, plotted against the normalized index _i/n_ . The black curve tracks the theoretical mean of ( _U_ (1) _, . . . , U_ ( _n_ )), while the orange and yellow curves correspond to two particular sequences of _bi_ values derived from the generalized Simes inequality for _δ_ = 0 _._ 1 and the DKWM [80, 81] inequality, detailed in the next subsection. We observe relatively few paths cross the orange curve, and all crossings occur at small indices. This suggests the upper confidence bounds provided by Theorem 4 can be especially tight for lower indices of the order statistics, which is essential to obtain reasonably powerful CCV p-values for outlier detection. Of course, calibration-conditional validity still necessarily comes at some power cost. For example, a marginal p-value of _u_ ˆ<sup>(marg)</sup> ( _X_ ) = 25 _/_ ( _n_ + 1) _≈_ 0 _._ 025 results in a CCV p-value of _h_ (25 _/_ ( _n_ + 1)) = _b_ 25 _≈_ 0 _._ 0377 in this case. 

### **3.3 Simes adjustment of marginal conformal p-values** 

The larger p-values typically do not matter in multiple testing problems, as it is the small ones that determine which hypotheses are rejected. Therefore, to maximize power, we would like the _bi_ values in Theorem 4 to be as small as possible for low indices _i_ , while we may be satisfied with letting _bi_ = 1 for large _i_ . The generalized Simes inequality yields a desirable class of ( _b_ 1 _, . . . , bn_ ) sequences with this property. 

9 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0010-00.png)


Figure 3: Illustration of Theorem 4 with _n_ = 1000 and _δ_ = 0 _._ 1. The orange and yellow curves give the sequences derived by the generalized Simes inequality with _k_ = 500 and the DKWM inequality, respectively. The blue and green curves (very close to each other) give the corresponding sequences obtained with the asymptotic and Monte Carlo adjustments described below. The right panel zooms in on small indices. 

**Proposition 2** (Generalized Simes Inequality, from Equation (3.5) in [82]) **.** _For any positive integer k ≤ n, the uniform bound_ (10) _in Theorem 4 holds with_ 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0010-03.png)


The original motivation of [82] was to compute thresholds for step-up procedure to achieve _k_ -FWER control; there, the parameter _k_ was set to be a small integer. Here, we exploit Proposition 2 differently, choosing _k_ = _n/_ 2 so that the _b_<sup>s</sup> _i_<sup>valueswithlowerindices</sup><sup>_i_areassmallaspossiblewhilethosewithlarger</sup> indices _i_ may be uninformative (note that _b_<sup>s</sup> _n−k_ +2<sup>=</sup><sup>_. . ._=</sup><sup>_b_</sup> _n_<sup>s= 1).Inparticular,ourchoicecorrespondsto</sup> 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0010-05.png)


Therefore, the smallest possible marginal p-value equal to 1 _/_ ( _n_ + 1) would be mapped to _h_ (1 _/_ ( _n_ + 1)) _≈_ ˆ 2 log(10) _/n_ = 4 _._ 61 _/n_ , if _δ_ = 0 _._ 1, for example, since _u_<sup>(ccv)</sup> ( _X_ ) = _h_ (ˆ _u_<sup>(marg)</sup> ( _X_ )). If _n_ = 1000, then _h_ (1 _/_ ( _n_ + 1)) _≈_ 0 _._ 0046, which is larger than the marginal p-value, but much smaller than what one would obtain from other standard uniform bounds. For example, the DKWM inequality [80, 81] would imply a result similar to that of Proposition 2 but with 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0010-07.png)


this would map the smallest possible marginal p-value to 1 _/_ ( _n_ + 1) + �log(2 _/δ_ ) _/_ 2 _n >_ 0 _._ 1, in the above example. The comparison between the generalized Simes inequality and the DKWM inequality is expanded in Appendix C, where we also consider an additional uniform bound based on the linear-boundary crossing probability for the empirical CDF [83]. This comparison confirms the generalized Simes inequality yields the most powerful adjustment for our multiple testing purposes. In practice, we find that _k_ = _n/_ 2 works well, as motivated empirically in Appendix D. (Note that larger values of _k_ would lower further the smallest possible adjusted p-value, but at the cost of raising other small p-values). 

### **3.4 Asymptotic adjustment of marginal conformal p-values** 

The Simes adjustment with _k_ = _n/_ 2 leads to p-values satisfying (4) exactly; however, this causes the smallest possible marginal conformal p-values to be inflated by a factor of order 1 _/n_ , and larger ones may be inflated even more. A natural question at this point is whether this approach is statistically efficient or whether more powerful alternatives may be available to achieve (4). We begin to address this matter by comparing the Simes adjustment to an alternative _asymptotic_ approach that provides a natural benchmark; this solution will 

10 

be valid in the limit of large _n_ but does not guarantee (4) exactly in finite samples. Recall Donsker’s theorem, the classical result from empirical process theory stating that, in the large- _n_ limit, the rescaled difference between the true and the empirical CDFs of the calibration scores, respectively _F_ and _F_<sup>ˆ</sup> _n_ , converges in distribution to a standard Brownian Bridge. Precisely,<sup>_√_</sup> _<u>n</u>_ <u>(</u> _F_<sup>ˆ</sup> _n − F_ ) _→d_ G, where G is the Gaussian process on [0 _,_ 1] with mean zero and covariance E[G( _t_ 1)G( _t_ 2)] = _t_ 1 _∧ t_ 2 _− t_ 1 _t_ 2, for all _t_ 1 _, t_ 2 _∈_ [0 _,_ 1]. This result suggests the following _asymptotic adjustment_ of marginal conformal p-values. 

As a starting point, note that sup _t∈_ [0 _,_ 1] _|_ G( _t_ ) _|_ follows the Kolmogorov distribution [84], whose 1 _− δ_ quantile, namely _qδ_<sup>K,canbecomputed.Therefore,asimplewayofconstructingapproximatelyvalidcon-</sup> ditional conformal p-values would be to add _qδ_<sup>K</sup><sup>_/√_</sup> _<u>n</u>_ to the marginal p-values. Unfortunately, this naive solution would suffer from the same limitation of the DKWM approach mentioned in the previous section: it is a correction of constant size which is not very attractive for multiple testing because it is extremely conservative for small p-values of order 1 _/n_ . Instead, a more useful solution is suggested by the adaptive bound of [85], which proved that the empirical process _V_<sup>ˆ</sup> _n_ ( _t_ ) defined as 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0011-02.png)


satisfies lim _n→∞_ P[sup _t∈_ [0 _,_ 1] _V_<sup>ˆ</sup> _n_ ( _t_ ) _≤ cn_ ( _δ_ )] _≥_ 1 _− δ_ , where _cn_ ( _δ_ ) is defined as 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0011-04.png)


This yields a straightforward asymptotic simultaneous upper confidence bound for _F_ ( _t_ ) and, in light of Theorem 4, it suggests the following approximately valid adjustment of marginal conformal p-values: 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0011-06.png)


where _h_<sup>a</sup> is the piece-wise constant function on [0 _,_ 1] defined such that _h_<sup>a</sup> ( _t_ ) = _b_<sup>a</sup> _⌈_ ( _n_ +1) _t⌉_<sup>,for</sup><sup>_t∈_[0</sup><sup>_,_1],with</sup> _b_<sup>a</sup> 0<sup>= 0,</sup><sup>_b_a</sup> _n_ +1<sup>= 1,and</sup> 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0011-08.png)


In Appendix B.1.1, we will show that _b_<sup>a</sup> 1<sup>_≤b_a</sup> 2<sup>_≤. . .≤b_a</sup> _n_<sup>,asrequiredbyTheorem4.SeeFigure3for</sup> a visualization of the simultaneous CDF bound corresponding to this adjustment function. The smallest possible marginal p-value is mapped by this function to _h_<sup>a</sup> (1 _/_ ( _n_ +1)) _≈_ (1+ _cn_ ( _δ_ )) _/n_ . For example, if _δ_ = 0 _._ 1 and _n_ = 1000, this is approximately 4 _._ 09 _/n ≈_ 0 _._ 0041, which is very similar to the corresponding constant ˆ 0 _._ 0046 obtained with the Simes adjustment. However, _u_<sup>(a-ccv)</sup> has the advantage of being reasonably tight for all p-values, not just the smallest ones, and thus it will generally allow for higher power compared to the Simes adjustment when _n_ is large. 

### **3.5 Monte Carlo adjustment of marginal conformal p-values** 

Although the Simes adjustment is more conservative than the asymptotic one in the limit of large _n_ , it has two distinct advantages in finite samples. First, it leads to p-values satisfying (4) exactly, with no asymptotic approximations. Second, the peculiar shape of its uniform empirical CDF envelope allows it to apply smaller corrections to relatively low p-values, possibly yielding higher power in multiple-testing applications; see Figure 4 for an illustration. These observations motivate the development of the following new type of adjustment function, which is based on _Monte Carlo_ rather than analytical calculations and is designed to combine the strengths of the two aforementioned approaches. In particular, the Monte Carlo solution proposed here is based on a uniform empirical CDF bound that is (a) theoretically valid in finite samples and (b) whose shape mimics that of the Simes approach for very small p-values while tracking the asymptotic envelope relatively closely for larger ones; see Figure 4 for a preview. 

11 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0012-00.png)


Figure 4: Comparison of different adjustment functions, with _n_ = 1000 and _δ_ = 0 _._ 1. In the zoomed-in panel on the right-hand-side, the Simes (orange) and Monte Carlo (green) curves cannot be distinguished. 

Having fixed any _n_ and _δ_ , denote by _h_<sup>s</sup> : [0 _,_ 1] _→_ [0 _,_ 1] the Simes piece-wise constant function obtained by combining (11) with (12), using _k_ = _n/_ 2. Recall that this satisfies (10) exactly. Let also _h_<sup>a</sup><sup>_,δ_ˆ</sup> : [0 _,_ 1] _→_ [0 _,_ 1] denote the asymptotic piece-wise constant function obtained by combining (11) with (15), after replacing the pre-specific parameter _δ_ with a variable _δ_<sup>ˆ</sup> , which can take any values in (0 _,_ 1). Note that it will be useful to keep the dependence of this function on _δ_<sup>ˆ</sup> explicit. Recall that _h_<sup>a</sup><sup>_,δ_ˆ</sup> satisfies (10) approximately if _n_ is large and _δ_<sup>ˆ</sup> = _δ_ . Next, define a new piece-wise constant function _h_<sup>m</sup><sup>_,δ_ˆ</sup> : [0 _,_ 1] _→_ [0 _,_ 1] as: 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0012-03.png)


Note that this function can be conveniently written in the form of (11) with a suitable choice of _b_ 1 _, . . . , bn_ . Now, the goal is to find the smallest possible _δ_<sup>ˆ</sup> , as a function of _n_ and _δ_ , such that the _b_ 1 _, . . . , bn_ sequence corresponding to the function _h_<sup>m</sup><sup>_,δ_ˆ</sup> defined in (16) satisfies (10). The problem can be solved with a bisection search for _δ_<sup>ˆ</sup> on (0 _,_ 1), approximating the probability in (10) through a simple Monte Carlo simulation—it suffices to generate a sufficiently large number of independent random samples of size _n_ from a uniform distribution. A feasible solution always exists because _h_<sup>m</sup><sup>_,δ_ˆ</sup> reduces to _h_<sup>s</sup> as _δ_<sup>ˆ</sup> _→_ 1, and _h_<sup>s</sup> satisfies (10). This Monte Carlo simulation is not computationally expensive for reasonable values of _n_ , as long as _δ_ is not tooˆ small; for example, it takes a few seconds on a personal computer to obtain a very accurate estimate of _δ_ with _δ_ = 0 _._ 1 and _n_ as large as 10 _,_ 000. Of course, if _n_ is extremely large, the Monte Carlo simulation is not even needed, as in that case one could just rely directly on the asymptotic adjustment. See Figure 3 for a visualization of the simultaneous CDF bound corresponding to this adjustment function. 

While the Monte Carlo adjustment approaches the asymptotic one in the limit of large _n_ , it may lead to more powerful p-values for multiple testing if _n_ is small. In fact, the Simes function _h_<sup>s</sup> ( _t_ ) can be lower than the asymptotic _h_<sup>a</sup><sup>_,δ_</sup> ( _t_ ) for values of _t_ very close to 0, and _h_<sup>m</sup><sup>_,δ_ˆ</sup> ( _t_ ) inherits this ability of preserving very small p-values relatively intact, as shown in the right-hand-side panel of Figure 4. At the same time, as it will be demonstrated shortly, the Monte Carlo adjustment tends to be more powerful than the Simes adjustment when testing a single hypothesis, or when dealing with many non-null hypotheses, because _h_<sup>a</sup><sup>_,δ_</sup> ( _t_ ) is lower than _h_<sup>s</sup> ( _t_ ) for moderately small values of _t_ ; see the left-hand-side panel of Figure 4. Additional figures in Appendix C show that this relative advantage grows even larger as _n_ increases. 

The Monte Carlo adjustment applied in this paper and implemented in the accompanying software package involves an additional modification to the expression in (16), whose discussion has been postponed until now to simplify the explanation. In practice, _h_<sup>m</sup><sup>_,δ_ˆ</sup> ( _t_ ) is defined as in (16) only for _t ≤_ 1 _/_ 2; then, for _t >_ 1 _/_ 2, the function is extended it as a tangent straight line because there would be little point in tightening the CDF envelope above 1 _/_ 2, as that region involves p-values unlikely to be rejected anyway. The advantage of this approach is that it decreases the boundary crossing probability of the empirical CDF for all _t >_ 1 _/_ 2 compared to the asymptotic solution, allowing a slightly more liberal adjustment for the more interesting p-values below 1/2; see Figure A4 in Appendix C. 

12 

### **3.6 Power analyses of conformal p-value adjustments** 

As marginal p-values are smaller than calibration-conditional p-values, the latter tend to involve some loss of power, while the former are not always valid, depending on the multiple testing procedure utilized. In this section, we would like to study the power gap between the marginal and calibration-conditional approaches within settings in which both types of conformal p-values lead to valid tests. However, traditional power analyses require stronger modeling assumptions (i.e., the distributions of inliers and outliers) and the specification of additional algorithmic details (i.e., the form of the conformity score functions) compared to the framework followed in this paper; in fact, conformal p-values are extremely flexible and can be applied in fully non-parametric settings with any conformity score function. We overcome this hurdle by analyzing the _effective level_ of a test applied to calibration-conditional p-values as a proxy for a power analysis. More precisely, a test at level _α_ applied to calibration-conditional p-values is generally equivalent to an analogous test at level _α_<sup>_′_</sup> applied to marginal p-values, for some _α_<sup>_′_</sup> _< α_ . Comparing _α_ to _α_<sup>_′_</sup> gives a measure of the loss in power incurred by calibration-conditional p-values that is specific to a particular testing procedure, but requires no assumptions about either the machine learning model utilized to compute conformity scores or the inlier and outlier distributions. Thus, _α_<sup>_′_</sup> is studied below for different testing procedures. 

#### **3.6.1 Testing a single hypothesis** 

Consider the problem in which a marginal conformal p-value _u_ ˆ<sup>(marg)</sup> ( _X_ 2 _n_ +1) for a single test point _X_ 2 _n_ +1 is available, and we wish to test whether _X_ 2 _n_ +1 is an outlier. The level- _α_ test based on the marginal p- value rejects when _u_ ˆ<sup>(marg)</sup> ( _X_ 2 _n_ +1) _≤ α_ . We will compare this to a test based on a calibration-conditional p-value. That is, we take the marginal p-value and adjust it with a generic piece-wise constant function _h_ : [0 _,_ 1] _→_ [0 _,_ 1] in the form of (11). Then, we reject the null if _h ◦ u_ ˆ<sup>(marg)</sup> _≤ α_ , or, equivalently, if 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0013-04.png)


where _i_<sup>_∗_</sup> ( _α_ ; _h_ ) = max _{i ∈{_ 1 _, . . . , n}_ : _bi ≤ α}_ and _b_ 1 _, . . . , bn_ indicate the step positions defining _h_ in (11). Since _u_ ˆ<sup>(marg)</sup> is uniformly distributed, _i_<sup>_∗_</sup> ( _α_ ; _h_ ) _/_ ( _n_ + 1) is the effective level of the analogous marginal test. 

With the asymptotic adjustment _h_<sup>a</sup> , the threshold for the calibration-conditional test can be calculated explicitly by solving a quadratic equation, and the solution in the large- _n_ limit take the following form: 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0013-07.png)


because 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0013-09.png)


In words, the cost in power of the asymptotic p-value adjustment from Section 3.4 can be understood by noting that the significance threshold _α_ is effectively decreased by a factor of order <u>(log log</u> _n_ ) _/n_ . Similarly, the effective _α_ -level with the DKWM adjustment _h_<sup>d</sup> , given by (13), is _α − O_ (1 _/_<sup>_√_</sup> _<u>n</u>_ <u>).</u> By contrast, for the Simes adjustment, we can show the effective _α_ -level is strictly below _α_ when _k_ = _⌈ζn⌉_ for some _ζ >_ 0. In fact, using the concavity of the mapping _a_ ( _x_ ) = log(1 _−_ 1 _/x_ ), Jensen’s inequality implies 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0013-11.png)


As a result, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0013-13.png)


In this sense, the asymptotic and DKWM adjustment are nearly as efficient as the marginal test for a single hypothesis, though the former is more powerful, while the Simes adjustment is asymptotically inefficient. 

13 

Analogous threshold calculations for the Monte Carlo adjustments in the same setting cannot be performed analytically because _i_<sup>_∗_</sup> ( _α_ ; _h_<sup>m</sup><sup>_,δ_ˆ</sup> ) no longer has a simple expression for the sequences _b_ corresponding to those functions _h_ . However, these analyses are easy to carry out numerically. Figure 5 (a) summarizes the results of these power analyses by comparing the effective significance levels obtained with these three alternative adjustment functions, as a function of _n_ . The results show the Monte Carlo adjustment behaves very similarly to the efficient asymptotic solution in the limit of large _n_ , but it can be even more powerful when the sample size is small thanks to the shape of its CDF envelope, which reduces the inflation of smaller p-values. The Simes adjustment behaves similarly to the Monte Carlo one when the sample size is small, but it is not efficient in the large- _n_ limit. In that case, the effective significance level for testing a single hypothesis does not converge at all to the nominal level _α_ in the large- _n_ limit. 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0014-01.png)


Figure 5: Power analysis of different adjustments for marginal conformal p-values under 3 alternative settings. The effective level resulting from the p-value adjustment for a test at nominal level _α_ = 0 _._ 05 (dashed horizontal line) is plotted as a function of the number of calibration samples, assuming the number of test points _m_ grows as<sup>_√_</sup> _<u>n</u>_ <u>.</u> (a) Testing a single hypothesis. (b) FWER control with a single strong signal (here the values for DKWM are all equal to 0). (c) Testing a global null with Fisher’s combination test. 

#### **3.6.2 Needle in a haystack** 

Consider a multiple testing problem in which there are _m_ possible outliers to be tested: the first one of these data points, _X_ 2 _n_ +1, is an outlier (a false null hypothesis), while the remaining _m −_ 1, _X_ 2 _n_ +2 _, . . . , X_ 2 _n_ + _m_ , are inliers (true nulls). The goal is to identify the outlier, controlling the family-wise error rate below _α_ . To further simplify the problem, imagine the signal strength for the true outlier is so high that the marginal conformal p-value for this point takes its minimal value with probability one: 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0014-05.png)


Then, we reject the null if the adjusted p-value for the outlier is below the Bonferroni level: 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0014-07.png)


In the case of the asymptotic adjustment function, the rejection event can be written as: 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0014-09.png)


Thus, the calibration-conditional test at level _α_ is equivalent to the marginal test at level ( _α_ +∆ _α_ ) _/m_ , where 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0014-11.png)


14 

In this regime, the calibration-conditional and marginal tests only differ by a<sup>_√_</sup> log log _n_ factor. In the case of the Simes adjustment with _k_ = _n/_ 2, the rejection event is 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0015-01.png)


which implies the equivalent level for the test is ( _α_ + ∆ _α_ ) _/m_ , with 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0015-03.png)


Similarly, for the DKWM adjustment, it is easy to see that 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0015-05.png)


Therefore, in the large- _n_ limit, the Simes adjustment is even more powerful than the asymptotic correction for this problem because it does not involve the slightly sub-optimal<sup>_√_</sup> log log _n_ factor. Unsurprisingly, the large additive inflation by the DKWM adjustment results in a large power loss. Although the Monte Carlo method is not as amenable to analytical calculations, it is easy to verify numerically that its power is almost the same as that of the asymptotic correction in this setting; see Figure 5 (b). Interestingly, the numerical power analysis in Figure 5 (b) also highlights that the asymptotic adjustment, although slightly less powerful in the large- _n_ limit, tends to be more powerful than the Simes adjustment for this problem. In fact,<sup>_√_</sup> log log _n <_ (2 log(1 _/δ_ ) _−_ 1) unless _n_ is extremely large or _δ_ is extremely small. 

#### **3.6.3 Fisher’s combination test of the global null** 

Consider a multiple testing problem in which there are _m_ test data points _X_ 2 _n_ +1 _, . . . , X_ 2 _n_ + _m_ and none of them are outliers. The goal is to test the global null by applying Fisher’s combination test to conformal p-values modified by an adjustment function _h_ , for different choices of the latter. Intuitively, the effective _α_ -level of this test will depend on the expected value of Fisher’s combination statistic under the null—a ˆ smaller E _H_ 0[ _−_ log( _h ◦ u_<sup>(marg)</sup> )] yields a more conservative test. Therefore, we begin by deriving this quantity analytically for the asymptotic, DKWM, and Simes adjustments; see Appendix B for further details. 

**Theorem 5** (Expected value of Fisher’s combination statistic with conformal p-values) **.** _Fixing δ >_ 0 _and letting n →∞,_ 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0015-10.png)



![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0015-11.png)



![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0015-12.png)


All three adjustments yield conservative tests because E _H_ 0[<sup>�</sup><sup>_m_</sup> _i_ =1<sup>_−_2 log(</sup><sup>_h◦u_ˆ(marg)(</sup><sup>_X_2</sup><sup>_n_+</sup><sup>_i_))]</sup><sup>_<_2</sup><sup>_m_asymp-</sup> totically. The gap is _O_ ( _m_<sup>_√_</sup> log log _n/_<sup>_√_</sup> _<u>n</u>_ <u>) for the asymptotic adjustment (the most efficient one in this case),</u> _O_ ( _m_ log _n/_<sup>_√_</sup> _<u>n</u>_ <u>)</u> for the DKWM adjustment, and _O_ ( _m_ ) for the Simes adjustment (the least efficient one in this case). In Appendix B, we compute the effective _α_ -level for each adjustment in different regimes. As those derivations are lengthy, we summarize the results below. 

> • For the asymptotic adjustment, the effective _α_ -level is _α_ (1+ _o_ (1)) if _m_ = _o_ ( _n/_ log log _n_ ), and _O_ (1 _/_ log<sup>_c_</sup> _n_ ) for some constant _c_ when _m_ = _γn_ for some _γ ∈_ (0 _,_ 1). 

15 

- For the DKWM adjustment, the effective _α_ -level is _α_ (1+ _o_ (1)) if _m_ = _o_ ( _n/_ log<sup>2</sup> _n_ ), and exp _{−O_ (log<sup>2</sup> _n_ ) _}_ when _m_ = _γn_ for some _γ ∈_ (0 _,_ 1). 

- For the Simes adjustment, the effective _α_ -level is exp _{−O_ (min _{m, n}/_ log _n_ ) _}_ if _m/_ log _n →∞_ . 

In Figure 5 (c), we compare the effective _α_ -levels computed numerically with _m_ =<sup>_√_</sup> _<u>n</u>_ <u>,</u> including also the theoretically intractable Monte Carlo adjustment. These results confirm the Simes method becomes extremely conservative for large _n_ , as its effective level tends to 0 instead of _α_ . By contrast, the Monte Carlo adjustment yields approximately the same effective significance threshold as the asymptotic method. 

Finally, it is interesting to compare these power analyses for calibration-conditional p-values with the exact adjustment of Fisher’s combination test from Theorem 1. Under a regime in which _m_ = _γn_ for some _γ ∈_ (0 _,_ 1), it follows from (5) that Fisher’s combination test applied to marginal conformal p-values is valid at level _α_ , conditional on the calibration data, if its nominal significance level is lowered by a factor that depends on _δ_ —the proportion of calibration data sets for which the test is allowed to be invalid—but remains constant with respect to _n_ . By contrast, applying Fisher’s combination test to calibration-conditional p- values results in an effective level _α_ that at best _decreases_ as 1 _/_ polylog( _n_ ), for the asymptotic adjustment. Therefore, calibration-conditional p-values are not always optimal with Fisher’s combination test, at least not compared to the ad-hoc correction of the latter presented in Theorem 1 when _m_ = _γn_ , but they have the advantage of flexibility. In fact, calibration-conditional p-values can be utilized by any multiple testing algorithm, including for example the BH procedure, whose power analysis is discussed next. 

#### **3.6.4 Testing multiple hypotheses by the BH procedure** 

Consider a multiple testing problem in which there are _m_ test data points _X_ 2 _n_ +1 _, . . . , X_ 2 _n_ + _m_ and the goal is to detect outliers with FDR control. If the BH procedure is applied to the adjusted p-values, all hypotheses with _h ◦ u_ ˆ<sup>(marg)</sup> ( _X_ 2 _n_ + _i_ ) _≤ αR_ ( _α_ ; _h_ ) _/m_ are rejected, where 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0016-06.png)


As a benchmark, we consider the number of rejections obtained with the marginal p-values: 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0016-08.png)


In the case of the asymptotic adjustment, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0016-10.png)


This quantity is decreasing in _i_ , implying that 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0016-12.png)


Therefore, all hypotheses rejected by the BH procedure applied to marginal p-values at a lower level _α/_ (<sup>_√_</sup> 2 log log _n_ + _o_ (1)) would be guaranteed to be rejected by the BH procedure applied to adjusted p-values, implying the effective FDR level for _h_<sup>a</sup> is at least _α/_ (<sup>_√_</sup> 2 log log _n_ + _o_ (1)). If<sup>_√_</sup> 2 log log _n <<_ log _m_ , this is more powerful than the Benjamini-Yekutieli procedure [14], whose effective FDR level is _α/_ (log _m_ + _O_ (1)). Further, the ratio given by (20) is 1+ _o_ (1) if _i/_ log log _n →∞_ , implying that, in the limit of _R_ marg( _α_ ) _/_ log log _n →∞_ , all marginal rejections are also rejected by the BH procedure applied to adjusted p-values with the target FDR level _α_ (1+ _o_ (1)). In summary, the cost of the asymptotic adjustment never exceeds<sup>_√_</sup> 2 log log _n_ + _o_ (1), and it is negligible if the number of rejections made by the marginal BH procedure grows faster than log log _n_ . 

In the case of the DKWM adjustment, the maximal ratio between the adjusted and marginal p-values is as large as _O_ (<sup>_√_</sup> _<u>n</u>_ <u>),</u> though the ratio becomes 1 + _o_ (1) when _i/_<sup>_√_</sup> _<u>n</u> →_ 0. Thus, unless the marginal BH 

16 

procedure can reject many more than<sup>_√_</sup> _<u>n</u>_ hypotheses, the power cost of the DKWM adjustment will be much higher than that of the asymptotic adjustment. 

In the case of the Simes adjustment, we can show that, if _k_ = _⌈ζn⌉_ for some _ζ ∈_ (0 _,_ 1), the ratio between the adjusted and marginal p-values is bounded by a constant that depends on _δ_ and _ζ_ . Analogous to (17), the concavity of _a_ ( _x_ ) implies 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0017-02.png)


Since _k_ = _⌈ζn⌉_ , 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0017-04.png)


and 

above, all _o_ (1 _/n_ ) terms are uniform over _i_ . Then, 

and for any _i_ , 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0017-08.png)


Thus, the power cost of the Simes adjustment does not grow with _n_ , which is more appealing compared to the asymptotic adjustment in the worst case. However, (18) indicates the cost is never negligible even if _R_ marg( _α_ ) is large, consistent with the behaviour of the Simes adjustment observed in Section 3.6.1 for the case of a single hypothesis tested without multiplicity corrections. Thus, the asymptotic adjustment (and the substantially similar Monte Carlo approach) can be expected to be more powerful in practical applications involving FDR control, as long as a reasonably large number of discoveries is expected. 

## **4 Extensions beyond conformal p-values** 

### **4.1 Simultaneous confidence bounds for the false positive rate** 

Some practitioners may be accustomed to thinking about outlier detection in terms of FPR—the probability of incorrectly reporting as outlier any true inlier—rather than p-values. In particular, they may wonder what the FPR can be if they report _X_ 2 _n_ +1 as likely to be an outlier whenever the classification score _s_ ˆ( _X_ 2 _n_ +1) (computed by some black-box outlier detection algorithm) is below a threshold _t_ , as a function of _t_ , so that they may choose a posteriori which value of _t_ to adopt. This question is closely related to the problem of constructing CCV p-values, so our method provides an answer. In fact, the next result shows Theorem 4 also yields a simultaneous upper confidence bound for the CDF. 

**Proposition 3** (Simultaneous confidence bounds for the FPR) **.** _Let F denote the true CDF of some distribution from which n i.i.d. samples, Z_ 1 _, . . . , Zn, are drawn, and denote by F_<sup>ˆ</sup> _n the corresponding empirical CDF. With the same notation as in Theorem 4,_ 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0017-14.png)


17 

Applying Proposition 3 to the CDF of the scores _s_ ˆ computed by any one-class classification algorithm provides a uniform upper confidence bound for its FPR, namely FPR( _t_ ) := P [ˆ _s_ ( _X_ 2 _n_ +1) _≤ t_ ], as a function of the detection threshold _t_ . In other words, this guarantees that reporting as outliers an observation with black-box score equal to _z_ is likely (with probability at least 1 _− δ_ ) to result in a FPR no greater than _h_ ( _F_<sup>ˆ</sup> _n_ ( _z_ )), where _F_<sup>ˆ</sup> _n_ ( _z_ ) is the empirical CDF of the analogous scores computed on a calibration data set of size _n_ . Figure 6 shows a practical example of this upper bound based on the empirical distribution of scores evaluated on 1000 calibration points, with _δ_ = 0 _._ 1 and _k_ = _n/_ 2 (the exact details of this example are the same as those of the numerical experiments presented later in Section 5.2). For instance, this plot informs us that reporting as outliers future samples with scores below -0.5 is likely to result in an FPR below 0.025. 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0018-01.png)


Figure 6: FPR calibration curves obtained with different adjustment methods for an isolation forest one-class classifier on simulated data, as a function of the reporting threshold for the classification scores. Each upper bound (solid) is guaranteed to lie above the true FPR curve (dotted) with probability 90%. The dashed curve corresponds to the empirical FPR. The panel on the right zooms in on small values (likely outliers). 

Note that the construction of a uniform confidence band for an unknown CDF is a widely studied problem. For example, the DKWM inequality [80, 81] implies the bound in (21) with _h_ ( _z_ ) = min _{z_ +�log(2 _/δ_ ) _/_ 2 _n,_ 1 _}_ . However, the DKWM bound is tightest at _z_ = 1 _/_ 2 and loose near 0, which would limit the power to detect outliers. Therefore, it is preferable for our purposes to have a function _h_ ( _z_ ) that is as close as possible to the identity for small values of _z_ , as discussed earlier in Section 3.3. 

### **4.2 Simultaneously-valid prediction sets** 

Lastly, CCV p-values can be easily re-purposed to strengthen the marginal guarantees generally obtainable for conformal predictions. In particular, for each _α ∈_ (0 _,_ 1), one can define a predictive set 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0018-06.png)


These sets are simultaneously valid for all _α_ , conditional on the calibration data. That is, they satisfy 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0018-08.png)


In other words, if we use CCV p-values to construct prediction sets, the probability that a new observation falls within _C_<sup>ˆ</sup><sup>_α_</sup> is at least 1 _− α_ , simultaneously for all _α ∈_ (0 _,_ 1) with high probability. This is stronger than the usual conformal guarantee, as the latter holds marginally over _D_ and only for a single pre-specified _α_ . 

18 

## **5 Numerical experiments** 

### **5.1 Setup** 

The following experiments are designed to simulate a world in which our methods are independently applied by _J_ practitioners. Each practitioner _j ∈_ [ _J_ ] has an independent data set _Dj_ (to train and calibrate the method), and _L_ test sets _Dj,l_<sup>test</sup> (to compute p-values and evaluate performance), each corresponding to different possible future scenarios _l ∈_ [ _L_ ]. The data sets contain 2 _n_ observations each ( _|Dj|_ = 2 _n_ ), and the test sets contain _n_ test observations each ( _|Dj,l_<sup>test</sup><sup>_|_=</sup><sup>_n_test).Imaginethat,fromthepractitioner’spresent</sup> point of view, the data set _Dj_ is fixed but the test set is random, so that _Dj,l_<sup>test</sup> represents the test set for practitioner _j_ under future scenario _l_ . Then, as discussed in Section 1.2, practitioner _j_ is most interested in the FDR (or other measures of type-I errors, alternatively) conditional on _Dj_ , i.e., in the random variable 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0019-03.png)


where FDP( _D_<sup>test</sup> ; _Dj_ ) is the proportion of inliers among the test points reported as outliers, based on the procedure calibrated on _Dj_ . This motivates the definition of the following performance measures. For any _j ∈_ [ _J_ ], we compute 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0019-05.png)


where Power( _Dj,l_<sup>test;</sup><sup>_Dj_)istheproportionofoutliersin</sup><sup>_D_</sup> _j,l_<sup>test</sup> correctly identified as such by practitioner _j_ . 

Our experiments will demonstrate that the proposed simultaneous calibration method leads to sufficiently small cFDR(<sup>�</sup> _Dj_ ) for the desired fraction of practitioners, while the traditional point-wise calibration generally only leads to small values of the marginal FDR, namely mFDR :=<sup>�</sup> _J_<sup><u>1</u></sup> � _Jj_ =1 cFDR(<sup>�</sup> _Dj_ ). 

### **5.2 Outlier detection on simulated data** 

#### **5.2.1 Data description** 

We begin to investigate the empirical performance of different methods for calibrating conformal p-values on synthetic data. The data are generated by sampling each data point _Xi ∈_ R<sup>50</sup> from a multivariate Gaussian mixture model _PX_<sup>_a_,suchthat</sup><sup>_Xi_=</sup><sup>_√_</sup> _<u>a Vi</u>_ + _Wi_ , for some constant _a ≥_ 1 and appropriate random vectors _Vi, Wi ∈_ R<sup>50</sup> . Here, _Vi_ has independent standard Gaussian components, and each coordinate of _Wi_ is independent and uniformly distributed on a discrete set _W ⊆_ R<sup>50</sup> with cardinality _|W|_ = 50. The vectors in _W_ are sampled independently from the uniform distribution on [ _−_ 3 _,_ 3]<sup>50</sup> , before the beginning of our experiments, and then held constant thereafter. (Therefore, each coordinate of _Wi_ is uniformly distributed on [ _−_ 3 _,_ 3], but it is not the case that the different _Wi_ ’s are independent and identically distributed on [ _−_ 3 _,_ 3]<sup>50</sup> ; instead, the fixed set _W_ makes this a mixture model.) 

The data sets _Dj_ are sampled from _PX_<sup>_a_with</sup><sup>_a_= 1and</sup><sup>_n_= 1000.Thetotal2</sup><sup>_n_observationsineach</sup><sup>_Dj_</sup> ˆ are further divided into _n_ train = 1000 observations used to fit a one-class SVM classifier scoring function _s_ (implemented in the Python package `scikit-learn` [86]), and _n_ cal = 1000 observations used to calibrate the conformal p-values, as in (1), leading to a valid p-value _u_ ˆ( _Xn_ +1) _∈_ [0 _,_ 1] for any new data point _Xn_ +1. The total number of data sets is _J_ = 100, each of which is associated with _L_ = 100 test sets. A random subset of the observations in each test set _Dj,l_<sup>test</sup> is sampled from _PX_<sup>_a_with</sup><sup>_a_=1,whiletheothersareoutliers,inthe</sup> sense that they are sampled from _PX_<sup>_a_with</sup><sup>_a >_1,asspecifiedbelow.</sup> 

#### **5.2.2 Individual outlier detection** 

First, we focus on a data generating model under which 90% of the _n_ test = 1000 observations in each _Dj,l_<sup>test</sup> are sampled from _PX_<sup>_a_with</sup><sup>_a_=1,andweseektoidentifytheremaining10%ofoutliers.Forthispurpose,</sup> 

19 

we calibrate a conformal p-value for all observations in _Dj,l_<sup>test,andthenweapplytheBHprocedureatsome</sup> nominal FDR level _α_ to account for the multiple comparisons, with and without Storey’s correction based on the estimated null proportion. In the following, we apply our conditional calibration method with the parameters _δ_ = 0 _._ 1 and _k_ = _n_ cal _/_ 2 (see below for comments about the choice of _k_ ). 

Figure 7 shows the distribution of cFDR(<sup>�</sup> _Ds_ ) and cPower(<sup>�</sup> _Ds_ ), corresponding to _α_ = 0 _._ 1, for different values of the signal strength _a_ (recall that here _a_ = 1 corresponds to no signal), when the BH procedure is utilized to account for the multiple comparisons. The results confirm the calibration-conditional p-values control the conditional FDR for at least 90% of practitioners, while the marginal p-values do not. In fact, marginal p-values only control the conditional FDR if the number of samples in the calibration data set is very large; see Figure A5, Appendix D. Among the three conditional calibration alternatives, the Monte Carlo and Simes methods yield slightly higher power than the asymptotic approximation in this setting. Note that all methods control the marginal FDR, as also predicted by our theoretical results. Figure A7 presents the results obtained by applying Storeys’ correction to the BH procedure, while Figure A8 summarizes additional experiments in which the conditional calibration is applied with _δ_ = 0 _._ 25. Finally, Figure A9 visualizes the effect of different values of the _k_ on the conditional p-values calibrated with the Simes method, showing that _k_ = _n_ cal _/_ 2 works relatively well, although the performance does not appear to be extremely sensitive to this choice. 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0020-02.png)


Figure 7: Performance of different methods for calibrating conformal p-values in a simulated outlier detection problem, as a function of the signal strength. The box plots visualize the distribution of FDR and power, as defined in (24), conditional on 100 independent data sets. The solid curves indicate the 90-th quantile of the conditional FDR distribution. The nominal FDR 0 _._ 1, and the conditional method is applied with _δ_ = 0 _._ 1. 

#### **5.2.3 Batch outlier detection** 

We now consider the global testing problem of detecting whether a batch of new observations contains any outliers. For this purpose, we follow the same approach as before, with the only difference that the _n_ test = 1000 observations in each test set are now sub-divided into 100 batches of size 10. The 10 calibrated p-values in each batch are combined with Fisher’s method to test the batch-specific global null. Then, the BH procedure with Storey’s correction is applied to control the FDR over all batches. This simulation is designed such that 90% of the batches contain no outliers (i.e., all samples are drawn from _PX_<sup>_a_with</sup><sup>_a_= 1),</sup> while 50% of the samples in the remaining batches are outliers (i.e., they are drawn from _PX_<sup>_a_with</sup><sup>_a_= 1</sup><sup>_._75).</sup> Of course, batched testing is less informative than the precise identification of outliers discussed in the previous section, but the advantage now is that we can achieve higher power. Figure 8 shows that, even though this problem is relatively easy (the power is close to 1), the use of marginal p-values may still lead to a conditional FDR that is noticeably higher than expected for many researchers. By contrast, simultaneous calibration appears to be conservative for all of them, without much power loss. Among the three conditional calibration alternatives, the Monte Carlo method and the asymptotic approximation yield higher power in this setting. 

20 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0021-00.png)


Figure 8: Performance of different methods for calibrating conformal p-values in a simulated outlier batch detection problem, as a function of the nominal FDR level. The excess FDR is defined as the difference between the empirical FDR and the nominal FDR. Other details are as in Figure 7. 

Next, we study the effect of the batch size on the performance of different calibration methods under the global null hypothesis (i.e., when there are no outliers in the test set). As before, the p-values in each batch are combined with Fisher’s method and the global null is rejected if the resulting p-value is smaller than 0.1. As before, the experiment is repeated for 100 independent data sets and 1000 test sets. Figure 9 shows that marginal p-values do not lead to valid inferences, especially if the batch size is large. By contrast, the tests based on calibration-conditional p-values always remain valid. 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0021-03.png)


Figure 9: Family-wise error rate (FWER) in a simulated outlier batch detection problem under the global null hypothesis, using different calibration methods for the conformal p-values. The results are shown as a function of the batch size. The global null is rejected if the Fisher’s combined p-value is below 0.1, which means the nominal FWER is 10% (horizontal dashed line). 

Finally, Figure A11 compares the performances of different global testing methods for combining the p-values in each batch (in addition to Fisher’s combination test), in the same experiments as in Figure 8. The alternative combinations we consider are the harmonic mean with equal weights [18], Simes’ [19], and Stouffer’s [20] p-values. The results show that the harmonic mean and Simes’ p-values yield no discoveries. This should be unsurprising because those methods are designed to have power against an alternative in which the signals are few and strong (e.g., a single outlier in each non-null batch), which is not the case here because each non-null batch contains several outliers and marginal conformal p-values can never be smaller than 1 _/n_ . Fisher’s marginal conformal p-values appear to be more powerful than Stouffer’s in these experiments, even if the former are simultaneously adjusted with our Monte Carlo method and the latter are not. It is worth emphasizing that, unlike Fisher’s combination test, not all global testing methods may become invalid on average when applied to positively dependent p-values. For example, the harmonic mean [18] and Simes’s p-values are known to be robust to positive dependencies [87], and Stouffer’s combination p-value can also be modified to account for known dependencies [88]. Yet, our simultaneous adjustment for conformal p-values remains useful even with combination tests that are robust to positive dependency because this adjustment happens to be necessary to guarantee valid inferences conditional on the calibration data; see Figure A11. 

21 

### **5.3 Outlier detection on real data** 

#### **5.3.1 Data description** 

Table 1: Summary of the benchmark data sets for outlier detection utilized in our applications. 

||ALOI<br>[89, 90]|Cover<br>[91]|Credit card<br>[92]|KDDCup99<br>[89, 93]|Mammography<br>[94]|Digits<br>[95]|Shuttle<br>[96]|
|---|---|---|---|---|---|---|---|
|Features _d_|27|10|30|40|6|16|9|
|Inliers _n_inliers|283301|286048|284315|47913|10923|6714|45586|
|Outliers _n_outliers|1508|2747|492|200|260|156|3511|



We turn to study the performance of the calibration schemes from Section 5.2 on several benchmark data sets for outlier detection, summarized in Table 1. The conditional p-values are calibrated with _δ_ = 0 _._ 1 using the Monte Carlo method, which is valid in finite samples and has demonstrated in the previous sections to be more powerful than other two alternatives. We utilize an isolation forest [97] machine-learning algorithms _s_ ˆ as the base method for detecting anomalies, available in the Python `sklearn` package. We rely on the default hyper-parameters, except for the ‘contamination’ parameter which we set equal to 0 _._ 1. Additional experiments based on one-class SVM and Local Outlier Factor (LOF) algorithms are presented in Appendix D (Tables A2–A3). 

#### **5.3.2 Individual outlier detection** 

Here, we follow the experimental setup of Section 5.2.2. The difference is that we need to construct multiple training, calibration, and test sets by randomly splitting the _n_ inlier inlier examples into three disjoint subsets of size _n_ train, _n_ cal and _n_ test, respectively. A total of _n_ inlier _/_ 2 data points is used for training and calibration, i.e., _n_ train + _n_ cal = _n_ inlier _/_ 2 with _n_ cal = min _{_ 2000 _, n_ train _/_ 2 _}_ , while outlier examples are only included in the test sets. For each training/calibration data subset, we sample 100 test sets of size _n_ test = min _{_ 2000 _, n_ train _/_ 3 _}_ . Each test set contains 90% of randomly chosen inliers, and 10% of outliers. It should be noted that, in contrast to the simulated experiments of Section 5.2.2 in which the data were effectively infinitely abundant, there is some overlap between the samples in different test sets. 

Figure 10 compares the performance of marginal and simultaneously calibrated p-values on the credit card data set [92], as a function of the nominal FDR level. Here, the BH procedure is applied with Storey’s correction. Note that the proposed Monte Carlo simultaneous calibration leads to FDR control for at least 90% of simulated practitioners, as expected. This stands in contrast with the marginal calibration approach, which controls the FDR only marginally. 

Consistent conclusion can be drawn from Table 2, which compares the two calibration procedures on all benchmark data sets at the nominal FDR level of 0.2. Additional results corresponding to different outlier detection algorithms (one-class SVM and LOF) can be found in Table A1, Appendix D.2. In all cases, we adopt the `sklearn` default parameters. Finally, Table A2 summarizes the performance of different calibration and detection methods across all data sets when the BH procedure is applied without Storey’s correction. 

#### **5.3.3 Batch outlier detection** 

We now focus on global testing for outlier batch detection, similarly to Section 5.2.3. The available data are divided into training, calibration, and test sets according to the same scheme as in Section 5.3.2; the only difference is that the size of the test sets is now equal to 1000, so as to follow as closely as possible the same experimental protocol as in Section 5.2.3. 

Figure 11 compares the performance of the different calibration methods as a function of the nominal FDR level. The p-values in each batch are combined with Fisher’s method, and then the BH procedure is 

22 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0023-00.png)


Figure 10: Outlier detection performance on credit card fraud data. Conformal p-values based on an isolation forest model are calibrated using different methods. The Benjamini-Hochberg procedure with Storey’s correction is then applied to control the FDR over the set of test points. The results are shown as a function of the nominal FDR level. Other details are as in Figure 7. 

Table 2: Outlier detection performance on different data sets, using alternative methods for calibrating conformal p-values. The FDR and power diagnostics are defined conditional on the training and calibration data, as explained in Section 5.1. The nominal marginal FDR level is 0.2. Empirical FDR values larger than the nominal level are colored in orange; values at least one standard deviation above it are colored in red. 

|||F|DR|||Po|wer||
|---|---|---|---|---|---|---|---|---|
||Me|an|90th pe|rcentile|M|ean|90-th|quantile|
|Dataset|Marg.|Cond.|Marg.|Cond.|Marg.|Cond.|Marg.|Cond.|
|ALOI|0.025|0.001|0.048|0|0|0|0|0|
|Cover|0.099|0.044|0.297|0.148|0.012|0.006|0.038|0.02|
|Credit card|0.191|0.162|0.228|0.202|0.679|0.611|0.782|0.746|
|KDDCup99|0.194|0.131|0.23|0.168|0.754|0.684|0.825|0.753|
|Mammography|0.187|0.056|0.286|0.17|0.176|0.059|0.337|0.22|
|Digits|0.202|0.052|0.266|0.173|0.417|0.096|0.629|0.355|
|Shuttle|0.196|0.163|0.228|0.198|0.981|0.98|0.984|0.983|



applied with Storey’s correction. Again, we observe that simultaneous calibration is required to ensure the conditional FDR is controlled in at least 90% of the applications, although it involves some power loss. Both calibration methods control the marginal FDR. 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0023-05.png)


Figure 11: Outlier batch detection performance on credit card fraud data. Conformal p-values are computed based on an isolation forest model and calibrated using different methods. Other details are as in Figure 8. 

23 

Table 3: Outlier batch detection performance on different data sets, using alternative methods for calibrating conformal p-values. The nominal FDR level is 0.1. Other details are as in Table 2. 

|||FD|R|||Po|wer||
|---|---|---|---|---|---|---|---|---|
||Me|an|90-th q|uantile|Me|an|90-th q|uantile|
|Data set|Marg.|Cond.|Marg.|Cond.|Marg.|Cond.|Marg.|Cond.|
|ALOI|0.07|0.016|0.2|0.081|0.001|0|0.004|0.002|
|Cover|0.08|0.05|0.158|0.12|0.184|0.132|0.333|0.243|
|Credit card|0.086|0.059|0.126|0.094|0.981|0.973|0.992|0.987|
|KDDCup99|0.091|0.044|0.145|0.08|1|0.998|1|1|
|Mammography|0.069|0.014|0.116|0.03|0.599|0.334|0.742|0.521|
|Digits|0.084|0.016|0.141|0.033|0.968|0.814|0.995|0.926|
|Shuttle|0.094|0.047|0.142|0.087|1|1|1|1|



Table 3 summarizes the performance of the two alternative calibration methods on all data sets. Here, the nominal FDR level is 0.1 and the BH procedure is applied with the Storey correction. Again, the results show that the Monte Carlo method controls the conditional FDR 90% of the time, although at some cost in power, while the marginal calibration method does not. See Table A3, Appendix D.2 for additional results that, in addition to the isolation forest, include also the one-class SVM and LOF algorithms for outlier detection. Finally, Table A4 summarizes performance of the different methods on all data sets when the BH procedure is applied without the Storey correction. 

## **6 Discussion** 

This paper has studied the multiple testing problem for outlier detection using conformal p-values. Conformal p-values provide a natural approach to outlier detection (when clean training data are available) with the advantage of being able to leverage any black-box machine-learning tool, producing fully non-parametric inferences that are provably valid in finite samples and require no modeling beyond the i.i.d. assumption. Of course, a possible limitation (or perhaps strength, depending on the viewpoint) of conformal inference is that its agnosticism prevents very confident statements, as conformal p-values can never be smaller than 1 _/_ ( _n_ + 1), where _n_ is the number of clean data points available for calibration. Therefore, this solution may not be as powerful as likelihood-based approaches, especially if the signals are strong but sparse. However, it does seem preferable if clean data are available but accurate models are not. 

Whenever the conformal framework is appropriate for a particular outlier detection application, the problem of multiple testing considered in this paper is likely to be relevant, as possible outliers are often to be detected among many possible inlier test points, and reporting an excess of false discoveries would be undesirable. Our work brings attention to the delicacy of such task, showing that the mutual dependence of conformal p-values breaks certain methods (e.g., Fisher’s combination test) and makes the validity of others (e.g., the BH procedure) not obvious. In particular, we find our PRDS result interesting because this property is well-known as a theoretical assumption for FDR control, but it is typically difficult to verify in practical applications [14, 15]. 

Our methodological contribution is a technique based on high-probability bounds to compute calibrationconditional conformal p-values that are mutually independent and can thus be directly trusted in any multiple testing procedure. Our bounds are stronger than those in the previous conformal inference literature because they are simultaneous in nature and, consequently, they can also be useful for practitioners to tune a posteriori the significance threshold for machine-learning statistics above which to report their discoveries. Unsurprisingly, our simulations demonstrate that calibration-conditional inferences are less powerful on average than marginal conformal inferences; therefore, the additional comfort of their stronger guarantees should be weighted against the potential loss of some interesting findings. Nonetheless, we prefer to leave 

24 

such considerations to practitioners on a case-by-case basis, as our objective here was simply to explain the theoretical properties and general relative advantages of different statistical methods. 

Finally, this work opens new directions for future research. For example, focusing on split-conformal p-values, we did not study other hold-out approaches, such as the jackknife+ [53] or bootstrap sampling [54], that may practically yield higher power, although they are also more computationally expensive. A separate line of research may focus on relaxing the i.i.d. assumption to improve power in a multiple testing setting with structured outliers [98]. In fact, our theory only requires the calibration and test inliers to be exchangeable and mutually independent, while the outliers in the test data may have dependencies with one another. Furthermore, we mentioned but did not explore the possible connection between our multiple outlier testing problem (especially regarding our results on Fisher’s combination method) and classical two-sample testing. Finally, the high-probability bounds developed here may prove useful for purposes other than the calibration of conformal p-values; for instance, we already discussed a straightforward extension to obtain simultaneously valid prediction sets, but other possible applications may involve predictive distributions [99] and functionals thereof [100], or the comparison of different machine-learning algorithms in terms of estimated generalization error [101, 102], for example. 

## **Software availability** 

A software implementation of the methods described in this paper is available online, in the form of a Python package, at `https://github.com/msesia/conditional-conformal-pvalues.git` , along with usage examples and notebooks to reproduce our numerical experiments. 

## **Acknowledgements** 

S.B. gratefully acknowledges the support of the Ric Weiland fellowship. E.C. was supported by Office of Naval Research grant N00014-20-12157, by the National Science Foundation grants OAC 1934578 and DMS 2032014, by the Army Research Office (ARO) under grant W911NF-17-1-0304, and by the Simons Foundation under award 814641. L.L. gratefully acknowledges the support of the National Science Foundation grants OAC 1934578, the Discovery Innovation Fund for Biomedical Data Sciences, and the NIH grant R01MH113078. Y.R. was supported by the ISRAEL SCIENCE FOUNDATION (grant No. 729/21) and by the Career Advancement Fellowship of the Technion. We are grateful to the anonymous referees and associate editor for their helpful comments and suggestions. 

## **References** 

- [1] L. Tarassenko, P. Hayton, N. Cerneaz, and M. Brady. “Novelty detection for the identification of masses in mammograms”. In: _1995 Fourth International Conference on Artificial Neural Networks_ . IET. 1995, pp. 442–447. 

- [2] A. Patcha and J.-M. Park. “An overview of anomaly detection techniques: Existing solutions and latest technological trends”. In: _Computer networks_ 51.12 (2007), pp. 3448–3470. 

- [3] F. Fortunato, L. Anderlucci, and A. Montanari. “One-class classification with application to forensic analysis”. In: _Journal of the Royal Statistical Society: Series C (Applied Statistics)_ 69.5 (2020), pp. 1227–1249. 

- [4] L. Tarassenko, D. A. Clifton, P. R. Bannister, S. King, and D. King. “Novelty Detection”. In: _Encyclopedia of Structural Health Monitoring_ . American Cancer Society, 2009. 

25 

- [5] D. Hendrycks and K. Gimpel. “A Baseline for Detecting Misclassified and Out-of-Distribution Examples in Neural Networks”. In: _Proceedings of International Conference on Learning Representations_ (2017). 

- [6] S. Liang, Y. Li, and R. Srikant. “Enhancing the reliability of out-of-distribution image detection in neural networks”. In: _arXiv preprint arXiv:1706.02690_ (2017). 

- [7] K. Lee, K. Lee, H. Lee, and J. Shin. “A Simple Unified Framework for Detecting Out-ofDistribution Samples and Adversarial Attacks”. In: _NeurIPS_ . 2018. 

- [8] K. Lee, H. Lee, K. Lee, and J. Shin. “Training Confidence-calibrated Classifiers for Detecting Out-of-Distribution Samples”. In: _International Conference on Learning Representations_ . 2018. 

- [9] M. M. Moya, M. W. Koch, and L. D. Hostetler. “One-class classifier networks for target recognition applications”. In: _NASA STI/Recon Technical Report N_ 93 (1993), p. 24043. 

- [10] M. A. Pimentel, D. A. Clifton, L. Clifton, and L. Tarassenko. “A review of novelty detection”. In: _Signal Processing_ 99 (2014), pp. 215–249. 

- [11] V. Vovk, A. Gammerman, and C. Saunders. “Machine-learning applications of algorithmic randomness”. In: _International Conference on Machine Learning_ . 1999, pp. 444–453. 

- [12] V. Vovk, A. Gammerman, and G. Shafer. _Algorithmic learning in a random world_ . Springer, 2005. 

- [13] Y. Benjamini and Y. Hochberg. “Controlling the false discovery rate: a practical and powerful approach to multiple testing”. In: _Journal of the Royal statistical society: series B (Methodological)_ 57.1 (1995), pp. 289–300. 

- [14] Y. Benjamini and D. Yekutieli. “The control of the false discovery rate in multiple testing under dependency”. In: _Annals of Statistics_ (2001), pp. 1165–1188. 

- [15] S. Clarke and P. Hall. “Robustness of multiple testing procedures against dependence”. In: _Annals of Statistics_ 37.1 (2009), pp. 332–358. 

- [16] R. Fisher. _Statistical methods for research workers_ . Oliver & Boyd (Edinburgh), 1925. 

- [17] J. D. Storey, J. E. Taylor, and D. Siegmund. “Strong control, conservative point estimation and simultaneous conservative consistency of false discovery rates: a unified approach”. In: _Journal of the Royal Statistical Society: Series B (Statistical Methodology)_ 66.1 (2004), pp. 187–205. 

- [18] D. J. Wilson. “The harmonic mean p-value for combining dependent tests”. In: _Proceedings of the National Academy of Sciences_ 116.4 (2019), pp. 1195–1200. 

- [19] R. J. Simes. “An improved Bonferroni procedure for multiple tests of significance”. In: _Biometrika_ 73.3 (1986), pp. 751–754. 

- [20] S. A. Stouffer, E. A. Suchman, L. C. DeVinney, S. A. Star, and R. M. Williams Jr. “The american soldier: Adjustment during army life.(studies in social psychology in world war II), vol. 1”. In: (1949). 

- [21] S. S. Wilks. “Multivariate statistical outliers”. In: _Sankhy¯a: The Indian Journal of Statistics, Series A_ (1963), pp. 407–426. 

- [22] D. M. Hawkins. _Identification of outliers_ . Vol. 11. Springer, 1980. 

- [23] M. Riani, A. C. Atkinson, and A. Cerioli. “Finding an unknown number of multivariate outliers”. In: _Journal of the Royal Statistical Society: series B (statistical methodology)_ 71.2 (2009), pp. 447–466. 

26 

- [24] A. Cerioli. “Multivariate outlier detection with high-breakdown estimators”. In: _Journal of the American Statistical Association_ 105.489 (2010), pp. 147–156. 

- [25] S. S. Khan and M. G. Madden. “One-class classification: taxonomy of study and review of techniques”. In: _The Knowledge Engineering Review_ 29.3 (2014), pp. 345–374. 

- [26] S. Agrawal and J. Agrawal. “Survey on anomaly detection using data mining techniques”. In: _Procedia Computer Science_ 60 (2015), pp. 708–713. 

- [27] C. C. Aggarwal. “Outlier analysis”. In: _Data mining_ . Springer. 2015, pp. 237–263. 

- [28] M. Sabokrou, M. Khalooei, M. Fathy, and E. Adeli. “Adversarially learned one-class classifier for novelty detection”. In: _Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition_ . 2018, pp. 3379–3388. 

- [29] R. Chalapathy and S. Chawla. “Deep learning for anomaly detection: A survey”. In: _preprint at arXiv:1901.03407_ (2019). 

- [30] R. Laxhammar and G. Falkman. “Inductive conformal anomaly detection for sequential detection of anomalous sub-trajectories”. In: _Annals of Mathematics and Artificial Intelligence_ 74.1-2 (2015), pp. 67–94. 

- [31] J. Smith, I. Nouretdinov, R. Craddock, C. Offer, and A. Gammerman. “Conformal anomaly detection of trajectories with a multi-class hierarchy”. In: _International symposium on statistical learning and data sciences_ . Springer. 2015, pp. 281–290. 

- [32] V. Ishimtsev, A. Bernstein, E. Burnaev, and I. Nazarov. “Conformal _k_ -NN Anomaly Detector for Univariate Data Streams”. In: _Conformal and Probabilistic Prediction and Applications_ . PMLR. 2017, pp. 213–227. 

- [33] L. Guan and R. Tibshirani. “Prediction and outlier detection in classification problems”. In: _arXiv preprint arXiv:1905.04396_ (2019). 

- [34] F. Cai and X. Koutsoukos. “Real-time Out-of-distribution Detection in Learning-Enabled Cyber-Physical Systems”. In: _2020 ACM/IEEE 11th International Conference on CyberPhysical Systems (ICCPS)_ . IEEE. 2020, pp. 174–183. 

- [35] M. Haroush, T. Frostig, R. Heller, and D. Soudry. “Statistical Testing for Efficient Out of Distribution Detection in Deep Neural Networks”. In: _arXiv preprint arXiv:2102.12967_ (2021). 

- [36] V. Vovk, I. Nouretdinov, and A. Gammerman. “Testing Exchangeability On-Line.” In: Jan. 2003, pp. 768–775. 

- [37] V. Fedorova, A. Gammerman, I. Nouretdinov, and V. Vovk. “Plug-in Martingales for Testing Exchangeability on-Line”. In: _Proceedings of the 29th International Coference on International Conference on Machine Learning_ . ICML’12. Edinburgh, Scotland: Omnipress, 2012, pp. 923–930. 

- [38] V. Vovk. “Testing Randomness Online”. In: _Statistical Science_ 36.4 (2021), pp. 595–611. 

- [39] V. Vovk. “Testing for concept shift online”. In: _arXiv preprint arXiv:2012.14246_ (2020). 

- [40] V. Vovk, I. Petej, I. Nouretdinov, E. Ahlberg, L. Carlsson, and A. Gammerman. “Retrain or not retrain: Conformal test martingales for change-point detection”. In: _Conformal and Probabilistic Prediction and Applications_ . PMLR. 2021, pp. 191–210. 

- [41] V. Vovk. “Conditional Validity of Inductive Conformal Predictors”. In: _Proceedings of the Asian Conference on Machine Learning_ . Vol. 25. 2012, pp. 475–490. 

27 

- [42] R. Foygel Barber, E. J. Candes, A. Ramdas, and R. J. Tibshirani. “The limits of distributionfree conditional predictive inference”. In: _Information and Inference: A Journal of the IMA_ 10.2 (2021), pp. 455–482. 

- [43] Y. Hechtlinger, B. P´oczos, and L. Wasserman. _Cautious Deep Learning_ . arXiv:1805.09460. 2018. 

- [44] Y. Romano, M. Sesia, and E. J. Cand`es. “Classification with Valid and Adaptive Coverage”. In: _Advances in Neural Information Processing Systems_ 33 (2020). 

- [45] M. Cauchois, S. Gupta, and J. C. Duchi. “Knowing what You Know: valid and validated confidence sets in multiclass and multilabel prediction”. In: _Journal of Machine Learning Research_ 22.81 (2021), pp. 1–42. 

- [46] A. N. Angelopoulos, S. Bates, J. Malik, and M. I. Jordan. “Uncertainty Sets for Image Classifiers using Conformal Prediction”. In: _preprint at arXiv:2009.14193_ (2020). 

- [47] Y. Romano, E. Patterson, and E. Cand`es. “Conformalized Quantile Regression”. In: _Advances in Neural Information Processing Systems 32_ . 2019, pp. 3543–3553. 

- [48] R. Izbicki, G. Shimizu, and R. Stern. “Flexible distribution-free conditional predictive bands using density estimators”. In: _International Conference on Artificial Intelligence and Statistics_ . PMLR. 2020, pp. 3068–3077. 

- [49] V. Chernozhukov, K. W¨uthrich, and Y. Zhu. “Distributional conformal prediction”. In: _Proceedings of the National Academy of Sciences_ 118.48 (2021). 

- [50] D. Kivaranovic, K. D. Johnson, and H. Leeb. “Adaptive, Distribution-Free Prediction Intervals for Deep Networks”. In: _International Conference on Artificial Intelligence and Statistics_ . PMLR. 2020, pp. 4346–4356. 

- [51] C. Gupta, A. K. Kuchibhotla, and A. K. Ramdas. “Nested conformal prediction and quantile out-of-bag ensemble methods”. In: _Pattern Recognition_ (2021), p. 108496. 

- [52] V. Vovk. “Cross-conformal predictors”. In: _Annals of Mathematics and Artificial Intelligence_ 74.1-2 (2015), pp. 9–28. 

- [53] R. F. Barber, E. J. Cand`es, A. Ramdas, R. J. Tibshirani, et al. “Predictive inference with the jackknife+”. In: _Annals of Statistics_ 49.1 (2021), pp. 486–507. 

- [54] B. Kim, C. Xu, and R. Foygel Barber. “Predictive inference is free with the jackknife+after-bootstrap”. In: _Advances in Neural Information Processing Systems_ 33 (2020). 

- [55] H. Papadopoulos, K. Proedrou, V. Vovk, and A. Gammerman. “Inductive Confidence Machines for Regression”. In: _Machine Learning: European Conference on Machine Learning ECML 2002_ . 2002, pp. 345–356. 

- [56] J. Lei, A. Rinaldo, and L. Wasserman. “A Conformal Prediction Approach to Explore Functional Data”. In: _Annals of Mathematics and Artificial Intelligence_ 74 (Feb. 2013). 

- [57] F. Wilcoxon. “Individual comparisons by ranking methods”. In: _Breakthroughs in statistics_ . Springer, 1992, pp. 196–202. 

- [58] J. Friedman. _On multivariate goodness-of-fit and two-sample testing_ . Tech. rep. No. SLACPUB-10325. Stanford Linear Accelerator Center, Menlo Park, CA (US), 2004. 

- [59] D. Lopez-Paz and M. Oquab. “Revisiting classifier two-sample tests”. In: _International Conference on Learning Representations_ . 2017. 

28 

- [60] A. K. Kuchibhotla. “Exchangeability, Conformal Prediction, and Rank Tests”. In: _arXiv preprint arXiv:2005.06095_ (2020). 

- [61] X. Hu and J. Lei. “A Distribution-Free Test of Covariate Shift Using Conformal Prediction”. In: _arXiv preprint arXiv:2010.07147_ (2020). 

- [62] I. Kim, A. Ramdas, A. Singh, L. Wasserman, et al. “Classification accuracy as a proxy for two-sample testing”. In: _Annals of Statistics_ 49.1 (2021), pp. 411–434. 

- [63] S. S. Wilks. “Determination of Sample Sizes for Setting Tolerance Limits”. In: _Ann. Math. Statist._ 12.1 (Mar. 1941), pp. 91–96. 

- [64] S. S. Wilks. “Statistical Prediction with Special Reference to the Problem of Tolerance Limits”. In: _Ann. Math. Statist._ 13.4 (Dec. 1942), pp. 400–409. 

- [65] A. Wald. “An Extension of Wilks’ Method for Setting Tolerance Limits”. In: _Ann. Math. Statist._ 14.1 (Mar. 1943), pp. 45–55. 

- [66] J. W. Tukey. “Non-Parametric Estimation II. Statistically Equivalent Blocks and Tolerance Regions–The Continuous Case”. In: _Ann. Math. Statist._ 18.4 (Dec. 1947), pp. 529–539. 

- [67] K. Krishnamoorthy and T. Mathew. _Statistical Tolerance Regions: Theory, Applications, and Computation_ . Wiley Series in Probability and Statistics. Wiley, 2009. 

- [68] S. Park, O. Bastani, N. Matni, and I. Lee. “PAC Confidence Sets for Deep Neural Networks via Calibrated Prediction”. In: _International Conference on Learning Representations_ . 2020. 

- [69] S. Bates, A. Angelopoulos, L. Lei, J. Malik, and M. Jordan. “Distribution-free, risk-controlling prediction sets”. In: _Journal of the ACM (JACM)_ 68.6 (2021), pp. 1–34. 

- [70] Y. Zhang and D. N. Politis. “Bootstrap prediction intervals with asymptotic conditional validity and unconditional guarantees”. In: _arXiv preprint arXiv:2005.09145_ (2020). 

- [71] M. B. Brown. “400: A method for combining non-independent, one-sided tests of significance”. In: _Biometrics_ (1975), pp. 987–992. 

- [72] J. T. Kost and M. P. McDermott. “Combining dependent P-values”. In: _Statistics & Probability Letters_ 60.2 (2002), pp. 183–190. 

- [73] D. Mary and E. Roquain. “Semi-supervised multiple testing”. In: _arXiv preprint arXiv:2106.13501_ (2021). 

- [74] A. Weinstein, R. Barber, and E. Candes. “A power and prediction analysis for knockoffs with lasso statistics”. In: _arXiv preprint arXiv:1712.06465_ (2017). 

- [75] C.-Y. Yang, L. Lei, N. Ho, and W. Fithian. “BONuS: Multiple multivariate testing with a data-adaptive test statistic”. In: _arXiv preprint arXiv:2106.15743_ (2021). 

- [76] B. Rava, W. Sun, G. M. James, and X. Tong. “A Burden Shared is a Burden Halved: A Fairness-Adjusted Approach to Classification”. In: _arXiv preprint arXiv:2110.05720_ (2021). 

- [77] J. D. Storey. “A direct approach to false discovery rates”. In: _Journal of the Royal Statistical Society: Series B (Statistical Methodology)_ 64.3 (2002), pp. 479–498. 

- [78] Y. Benjamini, A. M. Krieger, and D. Yekutieli. “Adaptive linear step-up procedures that control the false discovery rate”. In: _Biometrika_ 93.3 (2006), pp. 491–507. 

- [79] M. Sesia and E. J. Cand`es. “A comparison of some conformal quantile regression methods”. In: _Stat_ 9.1 (2020). 

29 

- [80] A. Dvoretzky, J. Kiefer, and J. Wolfowitz. “Asymptotic minimax character of the sample distribution function and of the classical multinomial estimator”. In: _Ann. Math. Stat._ (1956), pp. 642–669. 

- [81] P. Massart. “The tight constant in the Dvoretzky-Kiefer-Wolfowitz inequality”. In: _Annals of Probability_ (1990), pp. 1269–1283. 

- [82] S. K. Sarkar. “Generalizing Simes’ test and Hochberg’s stepup procedure”. In: _Annals of Statistics_ 36.1 (2008), pp. 337–363. 

- [83] A. Dempster. “Generalized _Dn_<sup>+Statistics”.In:</sup><sup>_Ann.Math.Stat._30.2(1959),pp.593–597.</sup> 

- [84] A. Kolmogorov. “Sulla determinazione empirica di una legge di distribuzione”. In: _Inst. Ital. Attuari, Giorn._ 4 (1933), pp. 83–91. 

- [85] F. Eicker. “The asymptotic distribution of the suprema of the standardized empirical processes”. In: _Annals of Statistics_ (1979), pp. 116–138. 

- [86] F. Pedregosa, G. Varoquaux, A. Gramfort, V. Michel, B. Thirion, O. Grisel, M. Blondel, P. Prettenhofer, R. Weiss, V. Dubourg, J. Vanderplas, A. Passos, D. Cournapeau, M. Brucher, M. Perrot, and E. Duchesnay. “Scikit-learn: Machine Learning in Python”. In: _Journal of Machine Learning Research_ 12 (2011), pp. 2825–2830. 

- [87] S. K. Sarkar and C.-K. Chang. “The Simes method for multiple hypothesis testing with positively dependent test statistics”. In: _Journal of the American Statistical Association_ 92.440 (1997), pp. 1601–1608. 

- [88] M. J. Strube. “Combining and comparing significance levels from nonindependent hypothesis tests.” In: _Psychological bulletin_ 97.2 (1985), p. 334. 

- [89] G. O. Campos, A. Zimek, J. Sander, R. J. Campello, B. Micenkov´a, E. Schubert, I. Assent, and M. E. Houle. “On the evaluation of unsupervised outlier detection: measures, datasets, and an empirical study”. In: _Data mining and knowledge discovery_ 30.4 (2016), pp. 891–927. 

- [90] _Amsterdam Library of Object Images (ALOI) Data Set_ . `https://www.dbs.ifi.lmu. de/research/outlier- evaluation/DAMI/literature/ALOI` . Not normalized, without duplicates. Accessed: January, 2021. 

- [91] _Covertype Data Set_ . `http://odds.cs.stonybrook.edu/forestcovercovertype-dataset` . Accessed: January, 2021. 

- [92] _Credit Card Fraud Detection Data Set_ . `https://www.kaggle.com/mlg-ulb/creditcardfraud` . Accessed: January, 2021. 

- [93] _KDD Cup 1999 Data Set_ . `https://www.kaggle.com/mlg-ulb/creditcardfraud` . Not normalized, without duplicates, categorial attributes removed. Accessed: January, 2021. 

- [94] _Mammography Data Set_ . `http://odds.cs.stonybrook.edu/mammography- dataset/` . Accessed: January, 2021. 

- [95] _Pen-Based Recognition of Handwritten Digits Data Set_ . `http://odds.cs.stonybrook. edu/pendigits-dataset` . Accessed: January, 2021. 

- [96] _Statlog (Shuttle) Data Set_ . `http://odds.cs.stonybrook.edu/shuttle-dataset` . Accessed: January, 2021. 

- [97] F. T. Liu, K. M. Ting, and Z.-H. Zhou. “Isolation forest”. In: _2008 eighth ieee international conference on data mining_ . IEEE. 2008, pp. 413–422. 

30 

- [98] A. Li and R. F. Barber. “Multiple testing with the structure-adaptive Benjamini–Hochberg algorithm”. In: _Journal of the Royal Statistical Society: Series B (Statistical Methodology)_ 81.1 (2019), pp. 45–74. 

- [99] V. Vovk, I. Nouretdinov, V. Manokhin, and A. Gammerman. “Cross-conformal predictive distributions”. In: _Conformal and Probabilistic Prediction and Applications_ . PMLR. 2018, pp. 37–51. 

- [100] W. Wisniewski, D. Lindsay, and S. Lindsay. “Application of conformal prediction interval estimations to market makers’ net positions”. In: _Conformal and Probabilistic Prediction and Applications_ . PMLR. 2020, pp. 285–301. 

- [101] M. J. Holland. “Making learning more transparent using conformalized performance prediction”. In: _arXiv preprint arXiv:2007.04486_ (2020). 

- [102] P. Bayle, A. Bayle, L. Mackey, and L. Janson. “Cross-validation confidence intervals for test error”. In: _Advances in Neural Information Processing Systems_ 33 (2020). 

- [103] T. Lipt´ak. “On the combination of independent tests”. In: _Magyar Tud Akad Mat Kutato Int Kozl_ 3 (1958), pp. 171–197. 

- [104] W. Van Zwet and J. Oosterhoff. “On the combination of independent test statistics”. In: _Ann. Math. Stat._ 38.3 (1967), pp. 659–680. 

- [105] V. Vovk and R. Wang. “Combining p-values via averaging”. In: _Biometrika_ 107.4 (2020), pp. 791–808. 

- [106] V. Petrov. “Sums of Independent Random Variables”. In: _Yu. V. Prokhorov. V. StatuleviCius (Eds.)_ (1975). 

- [107] P. Moran. “The random division of an interval”. In: _Supplement to the Journal of the Royal Statistical Society_ 9.1 (1947), pp. 92–98. 

- [108] B. C. Arnold, N. Balakrishnan, and H. N. Nagaraja. _A first course in order statistics_ . SIAM, 2008. 

- [109] M. J. Wainwright. _High-dimensional statistics: A non-asymptotic viewpoint_ . Vol. 48. Cambridge University Press, 2019. 

- [110] N. Ross. “Fundamentals of Stein’s method”. In: _Probability Surveys_ 8 (2011), pp. 210–293. 

- [111] S. Boucheron, G. Lugosi, and P. Massart. _Concentration inequalities: A nonasymptotic theory of independence_ . Oxford university press, 2013. 

- [112] J. Durbin. _Distribution Theory for Tests Based on Sample Distribution Function_ . Vol. 9. SIAM, 1973. 

- [113] V. Kotel’Nikova and E. Chmaladze. “On computing the probability of an empirical process not crossing a curvilinear boundary”. In: _Theory of probability & its applications_ 27.3 (1983), pp. 640–648. 

- [114] D. Siegmund. “Boundary crossing probabilities and statistical applications”. In: _Annals of Statistics_ (1986), pp. 361–404. 

31 

## **A Technical proofs** 

### **A.1 Correlation structure of null marginal conformal p-values** 

For notational convenience, we write _pi_ instead of _u_ ˆ<sup>(marg)</sup> ( _X_ 2 _n_ + _i_ ). When _X_ 2 _n_ +1 _, . . . , X_ 2 _n_ + _m_ are all inliers which are drawn from _PX_ , the conformal p-values _p_ 1 _, . . . , pm_ are exchangeable. Lemma 1 suggests that the variance of the combination statistic with any transformation _G_ ( _·_ ) is (1 + _γ_ ) times as large as that when the p-values are i.i.d.. In fact, under the global null, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0032-03.png)


_Proof of Lemma 1._ Without loss of generality, assume _i_ = 1 and _j_ = 2. Let ( _R_ 1 _, . . . , Rn, Rn_ +1 _, Rn_ +2) _d_ be the rank of ( _S_ 1 _, . . . , Sn_ +2) = (ˆ _s_ ( _Xn_ +1) _, . . . ,_ ˆ _s_ ( _X_ 2 _n_ ) _,_ ˆ _s_ ( _X_ 2 _n_ +1) _,_ ˆ _s_ ( _X_ 2 _n_ +2)) in the ascending order. Then _S_ 1 _, . . . , Sn_ +2 are i.i.d. draws from a non-atomic distribution, ( _R_ 1 _, . . . , Rn_ +2) are mutually distinct almost surely and for any permutation _π_ : _{_ 1 _, . . . , n_ + 2 _} �→{_ 1 _, . . . , n_ + 2 _}_ , 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0032-05.png)


Therefore, ( _R_ 1 _, . . . , Rn_ +2) is uniformly distributed over all permutations of _{_ 1 _, . . . , n_ + 2 _}_ . By definition, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0032-07.png)


Thus, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0032-09.png)


Similarly, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0032-11.png)


For any _j ∈{_ 1 _, . . . , n_ + 1 _}_ , 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0032-13.png)


For any 1 _≤ j < k ≤ n_ + 1, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0032-15.png)


By symmetry, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0032-17.png)


32 

As a result, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0033-01.png)


On the other hand, since _p_ 1 is uniformly distributed on _{_ 1 _/_ ( _n_ + 1) _,_ 2 _/_ ( _n_ + 1) _, . . . ,_ 1 _}_ , 

Note that E[ _G_<sup>2</sup> ( _p_ 1)] _< ∞_ since _G_ ( _i/_ ( _n_ + 1)) _∈_ R. As a result, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0033-04.png)


Therefore, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0033-06.png)


### **A.2 Failure of type-I error control with combination tests** 

We state a theorem for general (adjusted) combination tests which reject the global null if 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0033-09.png)


where _ξ >_ 0 is a pre-specified constant and 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0033-11.png)


ˆ **Theorem 6.** _Assume s_ ( _X_ ) _is continuously distributed and G_ ( _·_ ) : [0 _,_ 1] _�→_ R _is a non-constant function satisfying_ 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0033-13.png)


_Then, under the global null, if m_ = _⌊γn⌋ for some γ ∈_ (0 _, ∞_ ) _, as n →∞,_ 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0033-15.png)


_where z_ 1 _−α and_ Φ<sup>¯</sup> _denote the_ (1 _−α_ ) _-th quantile and the survival function of the standard normal distribution, respectively. Furthermore, under the same asymptotic regime, for W ∼ N_ (0 _,_ 1) _,_ 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0033-17.png)


33 

**Remark 2.** _For Fisher’s combination test, G_ ( _u_ ) = _−_ 2 log _u. Since G_ ( _U_ ) _∼ χ_<sup>2</sup> (2) _, condition (i) is clearly satisfied. To verify (ii), we note that G_ ( _u_ ) _is decreasing and |G_<sup>_′_</sup> ( _u_ ) _|_ = 2 _/u is decreasing. Thus, for u ∈_ [( _j −_ 1) _/_ ( _n_ + 1) _, j/_ ( _n_ + 1)] _, for k ∈{_ 1 _,_ 2 _},_ 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0034-01.png)


_As a result,_ 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0034-03.png)


_Thus, (ii) is proved. Finally, (iii) is satisfied because G_ ( _j/_ ( _n_ + 1)) _≤ G_ (1 _/_ ( _n_ + 1)) = _O_ (log _n_ ) _. Therefore, Theorem 1 is a special case of Theorem 6 with ξ_ = 1 _. In general, it is easy to verify (i)–(iii) for various other combination functions [103–105]._ 

**Remark 3.** _By_ (25) _, the limiting marginal type-I error is α when ξ_ =<sup>_<u>√</u>_</sup> 1 + _γ. This implies_ (6) _by noting that_ 1 �0<sup>(</sup><sup>_−_2 log</sup><sup>_u_)</sup><sup>_du_= 2</sup><sup>_.By_(26)</sup><sup>_,sincetherandomvariable_¯Φ(</sup><sup>_ξz_1</sup><sup>_−α_+</sup><sup>_√_</sup> _<u>γW</u>_ ) _has a positive density everywhere, the_ (1 _− δ_ ) _-th quantile of the conditional type-I error converges to the_ (1 _− δ_ ) _-th quantile of_ Φ(<sup>¯</sup> _ξz_ 1 _−α_ +<sup>_√_</sup> _<u>γW</u>_ ) _, which is_ Φ(<sup>¯</sup> _ξz_ 1 _−α −_<sup>_√_</sup> _<u>γz</u>_ 1 _−δ_ ) _. Thus, the conditional type-I error is controlled at level α with probability at least_ 1 _− δ asymptotically if ξ_ = 1 +<sup>_√_</sup> _<u>γz</u>_ 1 _−δ/z_ 1 _−α._ 

**Remark 4.** _To confirm our theory, we run Monte-Carlo simulations with n_ = 10<sup>5</sup> _and γ ∈{_ 2<sup>_−_3</sup> _,_ 2<sup>_−_2</sup> _, . . . ,_ 2<sup>3</sup> _}, estimating the average type-I error across_ 10<sup>4</sup> _samples. Since s_ ˆ( _X_ ) _is continuously distributed, we can assume that s_ ˆ( _X_ ) _∼_ Unif([0 _,_ 1]) _without loss of generality, as we will show in the proof. Figure A1 presents the simulated and asymptotic type-I errors for both the unadjusted (ξ_ = 1 _) and adjusted (ξ_ =<sup>_√_</sup> 1 + _γ) Fisher’s combination test given by_ (6) _._ 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0034-07.png)


Figure A1: Type-I errors of unadjusted and adjusted Fisher’s combination test. 

**Remark 5.** _If the pi’s are dependent, [71] and [72] approximate the null distribution by a rescaled chi-square distribution cχ_<sup>2</sup> ( _f_ ) _, where c and f are chosen to match the mean and variance of the Fisher’s combination statistic S_ Fisher _. Specifically,_ 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0034-10.png)


34 

_In our case, it is easy to see that_ 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0035-01.png)


_As a result, the null distribution is approximated by_ (1+ _γ_ ) _χ_<sup>2</sup> (2 _m/_ (1+ _γ_ )) _. The central limit theorem implies that χ_<sup>2</sup> ( _f_ ) _≈ N_ ( _f,_ 2 _f_ ) _when f is large. Thus, the critical value for this approximation is_ 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0035-03.png)


_Similarly, the critical value for our correction_ (6) _is_ 

�1 + _γχ_<sup>2</sup> (2 _m_ ; 1 _−α_ ) _−_ 2( ~~�~~ 1 + _γ−_ 1) _m ≈_ ~~�~~ 1 + _γ_ (2 _m_ + _√_ 2 _mz_ 1 _−α_ ) _−_ 2( ~~�~~ 1 + _γ−_ 1) _m ≈_ 2 _m_ +�2 _m_ (1 + _γ_ ) _z_ 1 _−α. Therefore, both corrections are asymptotically equivalent._ 

To prove Theorem 6, we start by stating two lemmas. The first lemma is a general Berry-Esseen bound for sums of independent (but not necessarily identically distributed) random variables with potentially infinite third moments. 

**Lemma 2.** _[[106], p. 112, Theorem 5] Let X_ 1 _, X_ 2 _, . . . , Xn be independent random variables such that_ E[ _Xj_ ] = 0 _, for all j. Assume also_ E[ _Xj_<sup>2</sup><sup>_g_(</sup><sup>_Xj_)]</sup><sup>_< ∞for some function gthat is non-negative, even, and non-decreasing_</sup> _in the interval x >_ 0 _, with x/g_ ( _x_ ) _being non-decreasing for x >_ 0 _. Write Bn_ =<sup>�</sup> _j_<sup>Var[</sup><sup>_Xj_]</sup><sup>_.Then,_</sup> 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0035-08.png)


_where A is a universal constant, L_ ( _·_ ) _denotes the probability law, dK denotes the Kolmogorov-Smirnov distance (i.e., the ℓ∞-norm of the difference of CDFs)_ 

The second lemma is a well-known representation of the spacing between consecutive order statistics. 

_i.i.d._ **Lemma 3** (From [107]; see also Section 4 of [108]) **.** _Let U_ 1 _, . . . , Un ∼_ Unif([0 _,_ 1]) _and U_ (1) _≤ U_ (2) _≤ . . . ≤ U_ ( _n_ ) _be their order statistics. Then_ 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0035-12.png)



![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0035-13.png)


**_Proof of Theorem 6_** _._ We first prove the limiting conditional type-I error (26). For convenience, we write _pi_ instead of _u_ ˆ<sup>(marg)</sup> ( _X_ 2 _n_ + _i_ ) and _Sj_ instead of _s_ ˆ( _Xn_ + _j_ ). Since _s_ ˆ( _X_ ) is continuously distributed, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0035-15.png)


where _FS_ denotes the CDF of _s_ ˆ( _X_ ) conditional on _D_ . As a result, we can assume _s_ ˆ( _X_ ) _∼_ Unif([0 _,_ 1]) without loss of generality. Conditional on _D_ , _p_ 1 _, . . . , pm_ are i.i.d. random variables with 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0035-17.png)


where _S_ (1) _< S_ (2) _< . . . < S_ ( _n_ ) denote the order statistics of ( _S_ 1 _, . . . , Sn_ ), and _S_ (0) = 0 _, S_ ( _n_ +1) = 1. By Lemma 3, we can reformulate the distribution of _pi_ conditional on _D_ as 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0035-19.png)


35 

As a result, for _k ∈{_ 1 _,_ 2 _}_ , 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0036-01.png)


By the strong law of large number, 

Let _gn_ = max _j∈{_ 1 _,...,n_ +1 _} G_ ( _j/_ ( _n_ + 1)). Since _V_ 1 _, . . . , Vn_ +1 are independent, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0036-04.png)


By condition (ii), 

and thus 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0036-07.png)


By condition (iii), _gn_ = _o_ (<sup>_√_</sup> _<u>n</u>_ <u>).</u> Together with (30), we obtain that for _k ∈{_ 1 _,_ 2 _}_ , 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0036-09.png)


By Chebyshev’s inequality, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0036-11.png)


Applying the condition (ii) again, we arrive at 

By (28), 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0036-14.png)


Let _an_ be a deterministic sequence such that _an <_ 1 _/_ 2, and _U ∼_ Unif([0 _,_ 1]). Let also _En_ be the event that _D_ is such that 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0036-16.png)


Since _G_ is a non-constant function, Var[ _G_ ( _U_ )] _>_ 0. By (31), we can choose _an_ = _o_ (1) such that 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0036-18.png)


Let 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0036-20.png)


36 

By Lemma 2 with _g_ ( _x_ ) = _x_ , 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0037-01.png)


where _A_ is a universal constant. Since _G_ ( _pi_ ) _≤ gn_ almost surely, by condition (iii), 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0037-03.png)


Thus, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0037-05.png)


On the event _En_ , the condition (iii) and that _n_ = _O_ ( _m_ ) imply that 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0037-07.png)


Since the Kolmogorov distance is invariant under rescalings, we have 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0037-09.png)


Since Var[ _G_ ( _pi_ ) _| D_ ] _/_ Var[ _G_ ( _U_ )] _∈_ [1 _− an,_ 1 + _an_ ] _→_ 1, 

Let 

The above arguments show that _Kn_ = _o_ (1) on the event _En_ . 

On the other hand, let 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0037-14.png)


and 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0037-16.png)


Then 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0037-18.png)


Since _Kn_ = _o_ (1) on _En_ and P[ _En_<sup>_c_] =</sup><sup>_o_(1),weobtainthat</sup> 

Since Φ<sup>¯</sup> is a continuous function and _m/n → γ_ , to prove (26), it remains to prove 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0038-01.png)


Without loss of generality, we assume that _η ≤_ 1 in the condition (i). By Lemma 2 with _g_ ( _x_ ) = _x_<sup>_η_</sup> , which clearly fulfills the criteria, we have that 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0038-03.png)


_m_ By definition, _cm_ is the (1 _− α_ )-th quantile of �� _j_ =1<sup>_G_(</sup><sup>_Ui_)</sup><sup>_−_E[</sup><sup>_G_(</sup><sup>_U_)]</sup> � _/_ � _m_ Var[ _G_ ( _U_ )]. By (36), 

_|_ Φ(<sup>¯</sup> _cm_ ) _− α|_ = _|_ Φ(<sup>¯</sup> _cm_ ) _−_ Φ(<sup>¯</sup> _z_ 1 _−α_ ) _|_ = _o_ (1) _._ 

Since Φ<sup>¯</sup><sup>_′_</sup> ( _z_ 1 _−α_ ) _>_ 0, it implies the first part of (35). 

To prove the second part of (35), we recall (28) with _k_ = 1 that 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0038-08.png)



![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0038-09.png)



![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0038-10.png)


By the condition (ii), we have that 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0038-12.png)


By the condition (i), (iii) and (37), 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0038-14.png)


Let 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0038-16.png)


Then Lemma 2 implies that 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0038-18.png)


By definition, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0038-20.png)


38 

The condition (ii) with _k_ = 1 implies that 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0039-01.png)


By (29), (37), (38), (39) and Slutsky’s Lemma, we prove the second part of (35). Therefore, the limiting conditional type-I error (26) is proved. 

Next, we prove the limiting marginal type-I error (25). Since 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0039-04.png)


is bounded almost surely, the convergence in distribution implies the convergence in expectation. Therefore, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0039-06.png)


Let _W_<sup>_′_</sup> be an independent copy of _W_ . Then 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0039-08.png)


As a result, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0039-10.png)


The proof is completed by the fact that _W_<sup>_′_</sup> _−_<sup>_√_</sup> _<u>γW</u> ∼ N_ (0 _,_ 1 + _γ_ ). 

### **A.3 Conformal p-values are PRDS** 

_Proof of Theorem 2._ Let _Z_ = ( _S_ (1) _, . . . , S_ ( _n_ )) be the order statistics of (ˆ _s_ ( _Xi_ )) _i∈{n_ +1 _,...,_ 2 _n}_ , the conformal scores evaluated on the calibration set. Let _Y_ = ( _p_ 1 _, . . . , pm_ ) be the conformal p-values evaluated on the ˆ test set (i.e., _pj_ = _u_<sup>(marg)</sup> ( _X_ 2 _n_ + _j_ )). Then, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0039-14.png)


With this representation, the conclusion will be implied by the following two lemmas. 

**Lemma 4.** _For a non-decreasing set A and vectors z, z_<sup>_′_</sup> _such that z ⪯ z_<sup>_′_</sup> _, then_ 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0039-17.png)


**Lemma 5.** _For y ≥ y_<sup>_′_</sup> _, if i belongs to the set of inliers, there exists Z_ 1 _∼ Z | Yi_ = _y and Z_ 2 _∼ Z | Yi_ = _y_<sup>_′_</sup> _such that_ P [ _Z_ 1 _⪯ Z_ 2] = 1 _._ 

In other words, Lemma 4 states that the conformal p-values increase as the conformal scores on the calibration set decrease, while Lemma 5 states that a larger conformal p-value indicates the calibration conformal scores are smaller. The proof follows easily from these. Take any _y ≥ y_<sup>_′_</sup> and let _Z_ 1 and _Z_ 2 be as in the statement of Lemma 5. Then, for any _i_ belonging to the set of inliers, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0039-20.png)


The inequality follows from Lemma 4 and the fact that P [ _Z_ 1 _⪯ Z_ 2] = 1, which comes from Lemma 5. 

39 

Lemma 4 follows immediately from the definition of marginal conformal p-values in (3). Lemma 5 is proved below. 

_Proof of Lemma 5, continuous case._ As in the proof of Theorem 6, since _s_ ˆ( _X_ ) is continuously distributed, we can assume without loss of generality that the scores _Si_ follow the uniform distribution on [0 _,_ 1]. Let _S_ (1)<sup>_′≤S_</sup> (2)<sup>_′≤. . .≤S_</sup> (<sup>_′_</sup> _n_ +1)<sup>betheorderstatisticsof(ˆ</sup><sup>_s_(</sup><sup>_Xn_+1)</sup><sup>_, . . . ,_ˆ</sup><sup>_s_(</sup><sup>_X_2</sup><sup>_n_+1))and</sup><sup>_R_2</sup><sup>_n_+1betherankof</sup> _s_ ˆ( _X_ 2 _n_ +1) among these. By definition, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0040-02.png)


Since _s_ ˆ( _X_ ) is continuously distributed, _R_ 2 _n_ +1 is independent of ( _S_ (1)<sup>_′, S_</sup> (2)<sup>_′, . . . , S_</sup> (<sup>_′_</sup> _n_ +1)<sup>).Asaresult,forany</sup> positive integer _k ≤ n_ + 1, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0040-04.png)


The right-hand-side is clearly entry-wise non-increasing in _k_ . Since _p_ 1 = _R_ 2 _n_ +1 _/_ ( _n_ + 1), Lemma 5 is proved for _i_ = 1. The same proof carries over to other indices _i_ belonging to the set of inliers. 

**Extension to non-continuous scores.** When _s_ ˆ( _X_ ) has atoms, the set of conformity scores _{s_ ˆ( _Xi_ ) : _i ∈D_<sup>cal</sup> _}_ have ties with non-zero probability. In this case, we replace the marginal conformal p-value (2) by a randomized version, i.e., 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0040-07.png)


where _U_ 1 _, U_ 2 _, . . ._ are i.i.d. random variables drawn from Unif([0 _,_ 1]) which are independent of the data. Note that (40) is identical to (2) almost surely when _s_ ˆ( _X_ ) is continuously distributed. Now we prove that the marginal conformal p-values defined in (40) satisfy the PRDS property. 

ˆ **Proposition 4** (Theorem 2 for the non-continuous case) **.** _Consider the setting of Theorem 2, but where s_ ( _·_ ) _is not assumed to be continuous. Define the randomized marginal p-values as in_ (40) _. Then, the marginal conformal p-values_ ( _p_ 1 _, . . . , pm_ ) _are PRDS._ 

The proof follows as above, once we verify Lemma 4 and Lemma 5 in the more general setting. 

_Proof of Lemma 4, general case._ Let _U_ = ( _U_ 1 _, . . . , Um_ ). By definition, _U_ is independent of ( _Y, Z_ ), and thus 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0040-12.png)


Let _pj_ ( _x_ ; _z, u_ ) denote the mapping from ( _X_ 2 _n_ + _j, Z, U_ ) to _pj_ . Then 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0040-14.png)


where 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0040-16.png)



![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0040-17.png)


We consider three cases. 

40 

Case 1: if _m<_ ( _x, z_ ) = _m<_ ( _x, z_<sup>_′_</sup> ), (41) implies that _m_ =( _x, z_ ) _≥ m_ =( _x, z_<sup>_′_</sup> ). Thus, (42) is obviously true. Case 2: if _m<_ ( _x, z_ )+ _m_ =( _x, z_ ) = _m<_ ( _x, z_<sup>_′_</sup> )+ _m_ =( _x, z_<sup>_′_</sup> ), let _a_ = 1+ _m_ =( _x, z_ ) and _b_ = _m<_ ( _x, z_ ) _− m<_ ( _x, z_<sup>_′_</sup> ). Then (42) is equivalent to 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0041-01.png)


This can be proved using the fact that _⌈_ ( _a_ + _b_ ) _u⌉≤⌈au⌉_ + _⌈bu⌉_ . 

Case 3: if _m<_ ( _x, z_ ) _> m<_ ( _x, z_<sup>_′_</sup> ) and _m<_ ( _x, z_ ) + _m_ =( _x, z_ ) _> m<_ ( _x, z_<sup>_′_</sup> ) + _m_ =( _x, z_<sup>_′_</sup> ), then _m<_ ( _x, z_ ) _≥ m<_ ( _x, z_<sup>_′_</sup> )+1 and _m<_ ( _x, z_ )+ _m_ =( _x, z_ ) _≥ m<_ ( _x, z_<sup>_′_</sup> )+ _m_ =( _x, z_<sup>_′_</sup> )+1 since _m<_ ( _x, z_ ) _, m<_ ( _x, z_<sup>_′_</sup> ) _, m_ =( _x, z_ ), and _m_ =( _x, z_<sup>_′_</sup> ) are all integers. Then 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0041-04.png)


Therefore, (42) is proved. As a result, the mapping from ( _X_ 2 _n_ +1 _, . . . , X_ 2 _n_ + _m, Z, U_ ) to _Y_ is entry-wise non-increasing in _Z_ given ( _X_ 2 _n_ + _j, . . . , X_ 2 _n_ + _m, U_ ). Since _{X_ 2 _n_ + _j_ : _j_ = 1 _, . . . , m}_ , _Z_ , and _U_ are mutually independent, we arrive at 

P[ _Y ∈ A | Z_ = _z, U_ ] _≥_ P[ _Y ∈ A | Z_ = _z_<sup>_′_</sup> _, U_ ] _,_ a.s. _._ 

The independence between _U_ and _Z_ implies that ( _U | Z_ = _z_ ) = _d_ ( _U | Z_ = _z′_ ). Lemma 4 then follows from the above inequality. 

_Proof of Lemma 5, general case._ Let _R_ 2 _n_ + _j_ = ( _n_ + 1) _pj_ . Note that _R_ 2 _n_ + _j_ can be interpreted as the rank with ties broken randomly. As in the proof for the continuous case, we first prove that 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0041-09.png)


Let _k−_ = max _{ℓ_ : _S_ (<sup>_′_</sup> _ℓ_ )<sup>_<S_2</sup><sup>_n_+1</sup><sup>_}_and</sup><sup>_k_+=min</sup><sup>_{ℓ_:</sup><sup>_S_</sup> (<sup>_′_</sup> _ℓ_ )<sup>_>S_2</sup><sup>_n_+1</sup><sup>_}_.Then</sup><sup>_S_</sup> _ℓ_<sup>_′_=</sup><sup>_S_2</sup><sup>_n_+1forany</sup><sup>_k−<ℓ<k_+.</sup> Since there exists at least one _ℓ_ with _S_ (<sup>_′_</sup> _ℓ_ )<sup>=</sup><sup>_S_2</sup><sup>_n_+1, i.e., the index corresponding to</sup><sup>_S_2</sup><sup>_n_+1, we have</sup><sup>_k_+</sup><sup>_−k−≥_2.</sup> By definition, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0041-11.png)


As a result, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0041-13.png)


It remains to prove that _R_ 2 _n_ +1 is independent of ( _S_ (1)<sup>_′, S_</sup> (2)<sup>_′, . . . , S_</sup> (<sup>_′_</sup> _n_ +1)<sup>).For any non-decreasing sequence</sup> _a_ 1 _≤ . . . ≤ an_ +1, let 1 = _n_ 0 _< n_ 1 _< . . . < nm_ = _n_ + 1 be integers such that 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0041-15.png)


Let _π_ : _{_ 1 _, . . . , n_ + 1 _} �→{_ 1 _, . . . , n_ + 1 _}_ be a uniform random permutation. Since _Xn_ +1 _, . . . , X_ 2 _n_ +1 are i.i.d., Conditioning on the event that, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0041-17.png)


For any _j_ = 1 _, . . . , m −_ 1, if _π_ ( _n_ + 1) _∈_ [ _nj−_ 1 _, nj_ ), 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0041-19.png)


41 

and thus, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0042-01.png)


Similarly, if _π_ ( _n_ + 1) _∈_ [ _nm−_ 1 _, nm_ ], 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0042-03.png)


For any _k_ , let _jk_ = max _{j_ : _nj ≤ k}_ , and _Ik_ be the set _{njk−_ 1 _, . . . , njk −_ 1 _}_ if _jk < m_ and _{njk−_ 1 _, . . . , njk }_ otherwise. Then 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0042-05.png)


Therefore, _R_ 2 _n_ +1 is independent of ( _S_ (1)<sup>_′, . . . , S_</sup> (<sup>_′_</sup> _n_ +1)<sup>).TheproofofLemma5isthencompleted.</sup> 

### **A.4 Storey’s correction does not break FDR control** 

Given a p-value _pi_ for the _i_ -th null hypothesis, let _p_ (1) _≤ . . . ≤ p_ ( _m_ ) be the ordered statistics. Given a target FDR level _α_ and a scalar _λ ∈_ (0 _,_ 1), the rejection set of the Storey-BH procedure is 

where 

and 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0042-11.png)


The parameter _λ_ is often chosen as 0 _._ 5, _α_ or 1 _− α_ . 

We start with a novel FDR bound for this procedure applied to PRDS p-values. 

**Theorem 7.** _Assume that_ ( _p_ 1 _, . . . , pn_ ) _is PRDS and each null p-value is super-uniform with an almost sure lower bound p_ min _∈_ [0 _,_ 1] _. Then_ 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0042-15.png)


_where_ 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0042-17.png)


_Proof._ Let 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0042-19.png)


42 

Then 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0043-01.png)


Let _r_ 0( _a_ ) = max _{_ 1 _, ⌈_ (1 + _a_ ) _p_ min _/_ (1 _− λ_ ) _α⌉}_ . By definition, the summand for a given _a_ is non-zero only if _r ≥ r_ 0( _a_ ). Thus, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0043-03.png)


where (i) uses the super-uniformity of the null p-value. Let _T_ denote the set of all possible values that _r/_ (1 + _a_ ) can take such that P( _pi ≤ α_ (1 _− λ_ ) _r/_ (1 + _a_ )) _>_ 0, i.e. 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0043-05.png)


Clearly, _T_ is a finite set. Let _t_ 1 _≤ t_ 2 _≤ . . . ≤ tM_ denote the elements of _T_ . It is easy to see that 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0043-07.png)


Then, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0043-09.png)


43 

where _p_ = ( _p_ 1 _, . . . , pm_ ) and 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0044-01.png)


Since _A_ is an increasing function of _p_ (element-wise) and _R_ is a decreasing function of _p_ (element-wise), _Hj_ ( _p_ ) is decreasing in _p_ (element-wise). The PRDS property implies that for any _j_ = 1 _, . . . , M −_ 1, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0044-03.png)


Therefore, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0044-05.png)


where the last step follows from (44), the PRDS property, and the fact that _p �→_ 1 _/_ (1 + _A_ ) is decreasing element-wise. 

To prove Theorem 3, we present an additional lemma. 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0044-08.png)


_Proof of Theorem 3._ As in the proof of Theorem 6, since _s_ ˆ( _X_ ) is continuously distributed, we can assume ˆ ˆ _s_ ( _X_ ) _∼_ Unif([0 _,_ 1]) without loss of generality. We write _pi_ instead of _u_<sup>(marg)</sup> ( _X_ 2 _n_ + _i_ ) and _Sj_ instead of _s_ ˆ( _Xn_ + _j_ ). Then 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0044-10.png)


Then _pj ≥_ 1 _/_ ( _n_ + 1) almost surely. Let _m_ 0 = _|H_ 0 _|_ and we assume that _H_ 0 = _{_ 1 _, . . . , m_ 0 _}_ without loss of generality. Since _p_ = ( _p_ 1 _, . . . , pm_ ) are PRDS and exchangeable, Theorem 4 implies that 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0044-12.png)


Since 1 _/_ (1 + _A_ ) is decreasing in _p_ , using the PRDS property again, we have 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0044-14.png)



![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0044-15.png)


Let _S_ (1) _≤ S_ (2) _≤ . . . ≤ S_ ( _n_ +1) denote the order statistics of _S_ 1 _, . . . , Sn_ +1 and _Rn_ +1 denote the rank of _Sn_ +1. Since _S_ 1 _∼_ Unif([0 _,_ 1]), there is no tie almost surely. 

Now we compute 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0044-18.png)


44 

By definition, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0045-01.png)


where _U ∼_ Unif([0 _,_ 1]). Note that there is a bijection between ( _S_ 1 _, . . . , Sn_ +1) and ( _S_ (1) _, . . . , S_ ( _n_ +1) _, R_ 1 _, . . . , Rn_ +1) for vectors without ties. The above distributional equivalence can be rewritten as 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0045-03.png)


Since the RHS does not depend on ( _R_ 1 _, . . . , Rn_ ), ( _p_ 2 _, . . . , pm_ 0) is independent of ( _R_ 1 _, . . . , Rn_ ) conditional on ( _Rn_ +1 _, S_ (1) _, . . . , S_ ( _n_ +1)). As a result, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0045-05.png)


Recall _K_ = ( _n_ + 1) _λ ∈_ Z. Then 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0045-07.png)


Therefore, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0045-09.png)


This implies that 

By Lemma 6, 

Since _Rn_ +1 is independent of ( _S_ (1) _, . . . , S_ ( _n_ +1)), 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0045-13.png)


By symmetry and the property of order statistics, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0045-15.png)


Thus, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0045-17.png)


Putting (45), (47) and (48) together, we prove the result. 

45 

### **A.5 Conditional p-value adjustment** 

ˆ _Proof of Theorem 4._ Let _Si_ = _s_ ( _Xn_ + _i_ ) for _i_ = 1 _, . . . , n_ with _F_<sup>_−_</sup> ( _t_ ) = P[ _Si < t | D_<sup>train</sup> ], and _S_ (1) _≤ S_ (2) _≤ . . . ≤ S_ ( _n_ ) be the order statistics. Note that here we condition on the training data in _D_<sup>train</sup> , which makes the _Si_ are independent of another. Then it is easy to see that 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0046-02.png)


where _⪯_ denotes the entry-wise stochastic dominance in the sense that ( _A_ 1 _, . . . , An_ ) _⪯_ ( _B_ 1 _, . . . , Bn_ ) iff 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0046-04.png)


When _F_ is continuous, the equality in distribution holds. Let _En_ denote the event on which _F_<sup>_−_</sup> ( _S_ ( _i_ )) _≤ bi_ for all _i_ = 1 _, . . . , n_ . Then 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0046-06.png)


Now we prove the following claim, which directly yields the theorem: 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0046-08.png)


Note that the image of _u_ ˆ<sup>(ccv)</sup> is _{b_ 1 _, . . . , bn,_ 1 _}_ , it remains to prove (49) with _t ∈{b_ 1 _, . . . , bn,_ 1 _}_ . When _t_ = 1, it clearly holds. When _t_ = _bi_ , 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0046-10.png)


Thus, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0046-12.png)


By definition of _En_ , (49) holds for all _t ∈{b_ 1 _, . . . , bn}_ . 

### **A.6 Simultaneous confidence bounds for the false positive rate** 

_Proof of Proposition 3._ Note that _h_ ( _i/n_ ) = _b⌈i_ + _i/n⌉_ = _bi_ +1 where we let _bn_ +1 = 1 for convenience. Then, the event that _F_ ( _Z_ ( _i_ )) _≤ h_ (( _i −_ 1) _/n_ ) = _bi_ for all _i ∈{_ 1 _, . . . , n}_ occurs with probability at least 1 _− δ_ , where _Z_ (1) _≤ . . . ≤ Z_ ( _n_ ) are the order statistics. Under this event, for any _z ∈_ [ _Z_ ( _i−_ 1) _, Z_ ( _i_ )), where we let _Z_ (0) = _∞_ and _Z_ ( _n_ +1) = _∞_ for convenience, _F_<sup>ˆ</sup> _n_ ( _z_ ) = ( _i −_ 1) _/n_ and thus 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0046-16.png)


On the other hand, if _h_ : [0 _,_ 1] _→_ [0 _,_ 1] is a function such that _h_ ( _F_<sup>ˆ</sup> _n_ ( _z_ )) is a uniform upper confidence band of _F_ for any CDF _F_ , then (10) holds with _bi_ = _h_ ( _i/n_ ). 

## **B Power analysis of Fisher’s combination test** 

In this section, we investigate the effective _α_ -level of Fisher’s combination test applied to calibrationconditional conformal p-values _u_ ˆ<sup>(ccv)</sup> _i ≡ h◦u_ ˆ<sup>(marg)</sup> _i_ , for different adjustment functions _h_ . To be self-contained, we summarize the three calibration-conditional adjustments as follows. 

- Asymptotic adjustment: 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0046-21.png)



![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0046-22.png)


46 

- DKWM adjustment: 

- Simes adjustment: 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0047-02.png)


where _k_ is chosen to be 0 _._ 5 _n_ in the experiments. 

Throughout the section, we will treat _δ ∈_ (0 _,_ 1) as a constant that does not vary with _n_ or _m_ , though it is not hard to recover the dependence on _δ_ from the proofs. As a result, the big-O notation could hide constants that solely depend on _δ_ . 

### **B.1 Asymptotic adjustment** 

#### **B.1.1 Monotonicity of** _h_<sup>a</sup> 

For notational convenience, we write _an_ for _cn_ ( _δ_ ) _/_<sup>_√_</sup> _<u>n</u>_ throughout the subsection. It should be kept in mind that _an_ depends on _δ_ . We first prove that _h_<sup>a</sup> is non-decreasing. 

**Proposition 5.** _h_<sup>a</sup> _is non-decreasing for any n and δ. Furthermore,_ 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0047-09.png)


_Proof._ Let _gn_ ( _x_ ) = _x_ + _an_ ~~�~~ _x_ (1 _− x_ ). By definition, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0047-11.png)


It is left to prove min _{g_ ( _x_ ) _,_ 1 _}_ is non-decreasing on [0 _,_ 1]. Taking the derivative, we obtain that 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0047-13.png)


Clearly, _gn_<sup>_′_(</sup><sup>_x_)</sup><sup>_≥_0forany</sup><sup>_x ≤_1</sup><sup>_/_2.When</sup><sup>_x >_1</sup><sup>_/_2,</sup> 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0047-15.png)


As a result, _gn_ ( _x_ ) is increasing on [0 _, dn_ ] and decreasing on [ _dn,_ 1]. On the other hand, 

and 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0047-18.png)


47 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0048-00.png)


Therefore, min _{gn_ ( _x_ ) _,_ 1 _}_ is increasing and, when _i ≥ tn_ , 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0048-02.png)


#### **B.1.2 Mean of Fisher’s combination statistic** 

As a stepping stone to analyze the effective _α_ -level, we will first compute the mean of Fisher’s combination statistic under the null, which roughly measures the conservatism of the test. 

**Lemma 7.** _Let_ � _f_ ( _x_ ) _dx denote the indefinite integral of f_ ( _x_ ) _. Then_ 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0048-06.png)


_Proof._ 

Let 

Then 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0048-10.png)


and 

Therefore, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0048-13.png)


which implies the lemma. 

**Theorem 8** (Part (a) of Theorem 5) **.** 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0048-16.png)


_Proof._ Let _gn_ ( _x_ ) = _x_ + _an_ ~~�~~ _x_ (1 _− x_ ). Since _−_ log(1) = 0, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0048-18.png)


We have shown in the proof of Proposition 5 that _gn_ ( _x_ ) is increasing on [0 _, tn/n_ ]. Thus, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0048-20.png)


48 

Now we calculate the indefinite integral of _−_ log _{gn_ ( _x_ ) _}_ . Using integration by parts, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0049-01.png)


Applying this to (51), by Newton-Leibniz formula, 

By definition, 

Then 

and 

Thus, 

Similarly, 

Next, 

and 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0049-10.png)


49 

Thus, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0050-01.png)


Finally, 

and 

As a result, 

Putting (52) - (55) together, we obtain that 

Similarly, 

The proof is then completed. 

#### **B.1.3** _α_ **-level** 

The next result shows the distributional approximation for Fisher’s combination statistic. The proof is involved and thus relegated to Section B.1.4. 

**Lemma 8.** _Under the global null, as m, n →∞,_ 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0050-11.png)


We apply Lemma 8 to derive the effective _α_ -level in two practically relevant regimes. 

**Theorem 9.** _Assume that m_ = _γn for some γ ∈_ (0 _, ∞_ ) _. The type-I error of Fisher’s combination test applied to h_<sup>a</sup> _◦ u_ ˆ<sup>(marg)</sup> _i ’s_ 

_where_ 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0050-15.png)


50 

**Remark 6.** _When γ_ = 1 _, α_ = 0 _._ 05 _,_ 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0051-01.png)


_and thus the type-I error is approximately_ 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0051-03.png)


_Proof._ Choose _αn ∈_ (0 _,_ 1) such that 

The standard CLT implies that 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0051-06.png)


Then 

Since _z_ 1 _−αn →∞_ , 

Clearly, _αn_ decays more slowly than any polynomial of 1 _/n_ . By Lemma 8, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0051-10.png)


**Theorem 10.** _Assume that m →∞ and m_ = _o_ ( _n/_ log log _n_ ) _. The type-I error of Fisher’s combination test applied to h_<sup>a</sup> _◦ u_ ˆ<sup>(marg)</sup> _i ’s_ 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0051-12.png)


_Proof._ Adopting the notation utilized in the proof of Theorem 9, by (57), 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0051-14.png)


51 

This implies _αn_ = _α_ + _o_ (1). By Lemma 8, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0052-01.png)


The proof is then completed. 

#### **B.1.4 Proof of Lemma 8** 

**Lemma 9.** _There exist universal constants C, c >_ 0 _and a constant C_ ( _δ_ ) _>_ 0 _that only depends on δ such that, with probability_ 1 _−_ exp _{−c_ (log _n_ )<sup>2</sup> _},_ 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0052-05.png)


_and_ 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0052-07.png)


_Proof._ Following [109], we call a random variable _V sub-exponential_ with parameters ( _ν, b_ ) if 

E[ _e_<sup>_λ_(</sup><sup>_V −_E[</sup><sup>_V_])</sup> ] _≤ e_<sup>_ν_2</sup><sup>_λ_2</sup><sup>_/_2</sup> _,_ for all _λ <_ 1 _/b._ 

If _V ∼_ Exp(1), then for any _λ <_ 1 _/_ 2, it is easy to verify that 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0052-11.png)


Thus, _V_ is sub-exponential with parameters (2 _,_ 2). 

Let _G_ ( _p_ ) = _−_ log( _h_<sup>a</sup> ( _p_ )). By (28) in the proof of Theorem 6, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0052-14.png)


_i.i.d._ where _V_ 1 _, . . . , Vn_ +1 _∼_ Exp(1). Let _En_ denote the event that 

Note that 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0052-17.png)


Then _G_<sup>_k_�</sup> _n_ +1 _<u>i</u>_ � ( _Vi−_ 1) is exponential with parameters (2 log<sup>4</sup> _n,_ 2 log<sup>4</sup> _n_ ) for _k ≤_ 4. By Bernstein’s inequality [e.g., 109, Proposition 2.9], 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0052-19.png)


Let _t_ =<sup>log6</sup><sup>_n_weobtainthat</sup> 5<sup>_~~√~~_</sup> _<u>n</u>_<sup>,</sup> 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0052-21.png)


Applying the union bound, there exists a universal constant _c >_ 0 such that 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0053-01.png)


Adopting the notation in Section B.1, we have 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0053-03.png)


We have shown in the proof of Proposition 5 that _gn_ ( _x_ ) _≤_ 1 is increasing on [0 _, tn/n_ ]. Then, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0053-05.png)


For any _x ∈_ (0 _,_ 1), 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0053-07.png)


Then 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0053-09.png)


where the last line uses the Cauchy-Schwarz inequality. Clearly, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0053-11.png)


and 

Using the same reasoning as in (52), 

where we use _oδ_ and _Oδ_ herein to hide the dependence on _δ_ . Therefore, 

Putting pieces together with (63), we have 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0053-16.png)


On the other hand, by Theorem 8, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0053-18.png)


53 

As a result, there exists a constant _C_ 1( _δ_ ) that only depends on _δ_ such that 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0054-01.png)


Putting (60), (61), and (65) together, on the event _En_ , for _k_ = 1 _,_ 2, 

As a result, for sufficiently large _n_ , 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0054-04.png)


This completes the proof of (58). 

To prove (59), note that 

By (60) and (61), on the event _En_ , for _k_ = 3 _,_ 4, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0054-08.png)


This proves (59). 

**Lemma 10.** _There exist a universal constant C >_ 0 _and a constant C_ ( _δ_ ) _>_ 0 _that only depends on δ such that,_ 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0054-11.png)


_and_ 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0054-13.png)


_Proof._ Let _En_ be the event defined in Lemma 9. By Lemma 9, P( _En_<sup>_c_)</sup><sup>_≤_exp</sup><sup>_{−c_(log</sup><sup>_n_)2</sup><sup>_}_.On</sup><sup>_E_</sup> _n_<sup>_c_.</sup> E _H_ 0 _| −_ log( _h_<sup>a</sup> _◦ u_ ˆ<sup>(marg)</sup> ) _|_<sup>_k_</sup> _| D ≤_ (log _n_ )<sup>_k_</sup> _._ � � 

Thus, for _k ≤_ 4, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0054-16.png)


By the triangle inequality, for _k_ = 1 _,_ 2, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0054-18.png)


54 

where the last line uses (58). Using a similar argument, we can also prove (67). **Lemma 11.** _For any µ ∈_ R _and σ_<sup>2</sup> _>_ 0 _,_ 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0055-01.png)


_Proof._ Let _W ∼ N_ (0 _,_ 1). By the triangle inequality, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0055-03.png)


For any _x ∈_ R, 

Similarly, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0055-06.png)


**Lemma 12.** _[Ross [110], Theorem 3.2 with D_ = 1 _] Let X_ 1 _, X_ 2 _, . . . , Xn be independent random variables such that_ E[ _Xj_ ] = 0 _and_ E[ _Xj_<sup>4]</sup><sup>_< ∞,forallj.WriteBn_= �</sup> _j_<sup>Var[</sup><sup>_Xj_]</sup><sup>_.Then_</sup> 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0055-08.png)


ˆ **_Proof of Lemma 8_** _._ Write _pi_ for _u_<sup>(marg)</sup> _i_ . Throughout the proof we suppress _H_ 0 from the expectation E _H_ 0 ˆ and P _H_ 0 because we will only consider the global null. This proof refines that of Theorem 6. Let _pi_ = _u_<sup>(marg)</sup> _i_ , _G_ ( _p_ ) = _−_ log( _h_<sup>a</sup> ( _p_ )), and _En_ be the event defined in (61). By Lemma 9, on the event _En_ , 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0055-10.png)


Recalling that we treat _δ_ as a constant and ignore all terms that solely depend on _δ_ in the big-O notation, we will simply write _C_ for _C_ ( _δ_ ) for the rest of the proof. 

Analogous to the proof of Theorem 6, we define 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0055-13.png)


By Lemma 2 with _g_ ( _x_ ) = _|x|_ , 

55 

where _A_ is a universal constant. By definition of _En_ , 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0056-01.png)


When _n_ is sufficiently large, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0056-03.png)


The scale-invariance of the Kolmogorov distance then implies 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0056-05.png)


By (68), Lemma 11 and the triangle inequality, for a sufficiently large _n_ , 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0056-07.png)


Since _W_<sup>˜</sup> _n_ is a function of _D_ , for any _t ∈_ R, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0056-09.png)


By (62), when _n_ is sufficiently large, 

Recall from (60) with _k_ = 1 that 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0056-12.png)


Let 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0056-14.png)



![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0056-15.png)


By (58) in Lemma 10, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0056-17.png)


Similarly, Lemma 10 implies that 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0056-19.png)


56 

where the first step applies Jensen’s inequality that 

and 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0057-02.png)


By Lemma 12, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0057-04.png)


As a result, 

Let _Z_ denotes a standard normal random variable. Using the coupling definition of the Wasserstein distance, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0057-07.png)


On the other hand, using the coupling definition of Wasserstein distance again, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0057-09.png)


Since _Vi ∼_ Exp(1) _∼_ Γ(1 _,_ 1), 

( _n_ + 1) _W_<sup>˜</sup> 2 _n ∼_ Γ( _n_ + 1 _,_ 1) _._ 

Using the properties of inverse-Gamma distributions, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0057-13.png)


By the triangle inequality and Cauchy-Schwarz inequality, 

57 

Note that 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0058-01.png)


and by Lemma 10, 

Thus, 

By the triangle inequality, (71), and (72) 

Note that 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0058-06.png)


Again, Let _Z_ denotes a standard normal random variable. Using the Kantorovich-Rubinstein dual representation of the Wasserstein’s distance, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0058-08.png)


Similar to the last step in the proof of Theorem 6, letting _Z_<sup>˜</sup> denote a standard normal random variable that is independent of _Z_ , 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0058-10.png)


Combining (70), (74), and (75), 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0058-12.png)


Note that _Wm_ + ~~�~~ _nm_ +1<sup>_W_˜</sup><sup>_n_= (1</sup><sup>_/√_</sup> _<u>m</u>_ <u>)</u><sup>�</sup><sup>_m_</sup> _i_ =1<sup>_{G_(</sup><sup>_pi_)</sup><sup>_−_E[</sup><sup>_G_(</sup><sup>_pi_)]</sup><sup>_}_.Let</sup> 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0058-14.png)


Then (76) implies that 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0058-16.png)


where 

58 

As shown in the previous steps, Φ<sup>¯</sup> is 1-Lipschitz. Thus, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0059-01.png)


By Theorem 8, 

Therefore, 

The proof is then completed. 

### **B.2 DKWM adjustment** 

#### **B.2.1 Mean of Fisher’s combination statistic** 

For notational convenience, let 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0059-08.png)


It should be kept in mind that _bn_ depends on _δ_ . 

**Theorem 11** (Part (b) of Theorem 5) **.** 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0059-11.png)


_Proof._ For notational convenience, let _tn_ = _⌊_ ( _n_ + 1)(1 _− bn_ ) _⌋_ . Since the mapping _x �→−_ log( _x_ + _bn_ ) is monotone decreasing, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0059-13.png)


Note that the indefinite integral of ( _−_ log _x_ ) is 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0059-15.png)


It is easy to see that 

and 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0059-18.png)


59 

By Newton-Leibniz formula, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0060-01.png)


The proof is then closed by (77). 

#### **B.2.2 Conditional moments of the adjusted p-values** 

**Lemma 13.** _There exist universal constants C, c >_ 0 _and a constant C_ ( _δ_ ) _>_ 0 _that only depends on δ such that, with probability_ 1 _−_ exp _{−c_ (log _n_ )<sup>2</sup> _},_ 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0060-05.png)


_and_ 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0060-07.png)


_Proof._ Let _G_ ( _p_ ) = _−_ log( _h_<sup>d</sup> ( _p_ )). Then 

where we use the fact that 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0060-10.png)


Using the same argument as in the proof of Lemma 9, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0060-12.png)


where _En_ denotes the event that 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0060-14.png)


Adopting the notation in Theorem 11, for any _k ≥_ 2, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0060-16.png)


Since the mapping _x �→_ log<sup>2</sup> ( _x_ + _bn_ ) is decreasing, 

Note that the indefinite integral of log<sup>2</sup> _x_ is 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0060-19.png)


60 

It is easy to see that 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0061-01.png)


where we use _Oδ_ herein to hide the dependence on _δ_ , and 

By Newton-Leibniz formula, 

This implies 

We have shown in Theorem 11 that 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0061-06.png)


Analogous to the proof of Lemma 9, on the event _En_ , 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0061-08.png)


To prove the bound for higher-order moments, note that 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0061-10.png)


By (60) and the definition of _En_ , on the event _En_ , for _k_ = 3 _,_ 4, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0061-12.png)


#### **B.2.3 Tail approximation for Fisher’s combination statistic** 

**Lemma 14.** _Under the global null, there exists a universal constant C >_ 0 _and n_ 0( _δ_ ) _that only depends on δ, such that for any n ≥ n_ 0( _δ_ ) _and t >_ 0 _,_ 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0061-15.png)


ˆ _Proof._ Let _G_ ( _p_ ) = _−_ log( _h_<sup>d</sup> ( _p_ )) and write _pi_ for _u_<sup>(marg)</sup> _i_ . Throughout the proof we suppress _H_ 0 from the expectation E _H_ 0 and P _H_ 0 because we will only consider the global null. By (60) , we can write 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0061-17.png)


61 

Then, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0062-01.png)


By (78) and Bernstein’s inequality [e.g., 111, equation (2.10)], 

By Lemma 9, with probability 1 _−_ exp _{−c_ (log _n_ )<sup>2</sup> _}_ , 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0062-04.png)


when _C_ ( _δ_ ) log<sup>6</sup> _n/_<sup>_√_</sup> _<u>n</u> ≤_ 1. Thus, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0062-06.png)


Moving to the second term of (79), we can use the fact that _Vi_ is sub-exponential with parameters (2 _,_ 2) as shown in the proof of Lemma 9 and apply Bernstein’s inequality for sums of exponential variables [e.g., 109, Proposition 2.9], 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0062-08.png)


By Lemma 13 and a similar argument for Lemma 10, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0062-10.png)


when _C_ ( _δ_ ) log<sup>6</sup> _n/_<sup>_√_</sup> _<u>n</u> ≤_ 1. Thus, 

62 

As for the third term of (79), we can apply Bernstein’s inequality for sums of sub-exponential random variables again and obtain that 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0063-01.png)


Piecing (80) - (82) together, the lemma is proved. 

**Lemma 15.** _Under the global null, as m, n →∞,_ 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0063-04.png)


_Proof._ Let _G_ ( _p_ ) = _−_ log � _h_<sup>d</sup> ( _p_ )�. Note that the proof of Lemma 8 only replies on two facts that (1) ˆ _−_ log _h_<sup>d</sup> _◦ u_<sup>(marg)</sup> _i ≤_ log _n_ , and (2) Lemma 9 holds for the first four conditional moments. Here, both � � continue to hold for DKWM-adjusted p-values. Following the steps in Section B.1.4, we can show that (76) continues to hold, i.e., 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0063-06.png)


By Theorem 11, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0063-08.png)


Using the same argument below (76) in the proof of Lemma 8, we can prove the result. 

#### **B.2.4** _α_ **-level** 

**Theorem 12.** _(a) Assume that m_ = _γn for some constant γ ∈_ (0 _, ∞_ ) _. The type-I error of Fisher’s combination test applied to h_<sup>d</sup> _◦ u_ ˆ<sup>(marg)</sup> _i ’s_ 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0063-12.png)


_for some constant C_ ( _γ, δ_ ) _>_ 0 _that only depends on γ and δ._ 

- _(b) Assume that m →∞ and m_ = _o_ ( _n/_ log<sup>2</sup> _n_ ) _. The type-I error of Fisher’s combination test applied to h_<sup>d</sup> _◦ u_ ˆ<sup>(marg)</sup> _i ’s_ 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0063-15.png)


_Proof._ Throughout the proof we suppress _H_ 0 from the expectation E _H_ 0 and P _H_ 0 because we will only consider the global null. 

- (a) Let 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0063-18.png)


63 

Then, by Lemma 14, 

By (56), 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0064-02.png)


By Theorem 11, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0064-04.png)


Since _m_ = _γn_ , there exists a constant _C_ ( _γ, δ_ ) _>_ 0 that only depends on _γ_ and _δ_ such that 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0064-06.png)


The proof is then completed. 

(b) Choose _αn ∈_ (0 _,_ 1) such that 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0064-09.png)


By Lemma 15, 

Note that _Am_ = _z_ 1 _−α_ + _o_ (1) and _m_ = _o_ ( _n/_ log<sup>2</sup> _n_ ), 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0064-12.png)


This implies _αn_ = _α_ + _o_ (1) and hence 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0064-14.png)


64 

### **B.3 Simes adjustment** 

#### **B.3.1 Mean of Fisher’s combination statistic** 

**Theorem 13** (Part (c) of Theorem 5) **.** _Assume that k_ = _⌈ζn⌉ for some ζ >_ 0 _. Then_ 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0065-03.png)


_Proof._ Since ( _i − j_ + 1) _/_ ( _n − j_ + 1) _≤ i/n_ for any _j_ = 1 _, . . . , k_ , 

Moreover, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0065-06.png)


Then 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0065-08.png)


where the last line uses the fact that _δ ≤_ 1. Since the mapping _x �→−_ log(1 _− x_ ) is increasing, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0065-10.png)


Thus, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0065-12.png)


The proof is completed by noting that 

#### **B.3.2 Conditional variance of adjusted p-values** 

**Lemma 16.** _There exist a universal constant c >_ 0 _and a constant n_ 0( _δ_ ) _that only depend on δ such that, for any n ≥ n_ 0( _δ_ ) _,_ 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0065-16.png)


_Proof._ Let _G_ ( _p_ ) = _−_ log( _h_<sup>s</sup> ( _p_ )). By (60), 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0065-18.png)



![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0065-19.png)


By (84), 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0066-01.png)


Analogous to the proof of Theorem 13, 

where we use _Oδ_ herein to hide the dependence on _δ_ . When _n ≥ n_ 0( _δ_ ) for some sufficiently large _n_ 0( _δ_ ) that only depends on _δ_ , 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0066-04.png)


By Bernstein’s inequality [e.g., 109, Proposition 2.9], 

Then, there exists a universal constant _c >_ 0 such that 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0066-07.png)


By (85) and Cauchy-Schwarz inequality, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0066-09.png)


Then, for any sufficiently large _n_ , 

By (82), 

The result is then proved by combining the above two inequalities. 

#### **B.3.3** _α_ **-level** 

**Lemma 17.** _Under the global null, there exists a universal constant C >_ 0 _and n_ 0( _δ_ ) _that only depends on δ, such that for any n ≥ n_ 0( _δ_ ) _and t >_ 0 _,_ 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0066-15.png)


66 

ˆ _Proof._ Let _G_ ( _p_ ) = _−_ log( _h_<sup>s</sup> ( _p_ )) and write _pi_ for _u_<sup>(marg)</sup> _i_ . Throughout the proof we suppress _H_ 0 from the expectation E _H_ 0 and P _H_ 0 because we will only consider the global null. Analogous to (79), 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0067-01.png)


By Lemma 16, with probability 1 _−_ exp _{−cn/_ log _n}_ , 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0067-03.png)


when _n_ is sufficiently large. By (86), 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0067-05.png)


when _n_ is sufficiently large. 

Similar to (81) and (82), we have 

for some universal constant _c >_ 0. The result is then proved by (87). 

**Theorem 14.** _Assume m/_ log _n →∞. The type-I error of Fisher’s combination test applied to h_<sup>s</sup> _◦ u_ ˆ<sup>(marg)</sup> _i ’s_ 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0067-10.png)


_for some constant C_ ( _ζ, δ_ ) _>_ 0 _that only depends on ζ and δ._ 

_Proof._ Let 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0067-13.png)


Then, by Lemma 17, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0067-15.png)


By (56), 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0067-17.png)


67 

By Theorem 13, 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0068-01.png)


Thus, there exists _C_ ( _ζ, δ_ ) _>_ 0 such that 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0068-03.png)


## **C Numerical comparisons of different adjustment functions** 

In addition to the adjustment functions derived from the generalized Simes inequality and the DKWM inequality, we consider here another class of simultaneous bounds based on the so-called _boundary crossing probability_ [83, 112–114]—the probability that _F_ ( _z_ ) ever crosses _h_ ( _F_<sup>ˆ</sup> _n_ ( _z_ )) for a fixed function _h_ ( _·_ ). This probability is generally difficult to compute analytically, but the special case of a linear _h_ ( _·_ ) is an exception. i _._ i _._ d _._ Assuming that _F_ is the CDF of Unif([0 _,_ 1]), let _F_<sup>ˆ</sup> _n_ ( _z_ ) is the empirical CDF of _S_ 1 _, . . . , Sn ∼_ Unif([0 _,_ 1]). Then, [83] proved that 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0068-06.png)


for any _a, b ∈_ (0 _,_ 1), where 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0068-08.png)


If we replace _Si_ with 1 _− Si_ , then _F_<sup>ˆ</sup> _n_ ( _z_ ) becomes 1 _− F_<sup>ˆ</sup> _n_ (1 _− z_ ). Further, replacing _z_ by 1 _− z_ leads to 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0068-10.png)


For any pair ( _a, b_ ) with ∆Dempster( _a, b_ ; _n_ ) = _δ_ , we obtain a function _h_ ( _z_ ) = _a_ + (1 _− a_ ) _z/_ (1 _− b_ ) satisfying (21), which yields the following sequence satisfying (10): 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0068-12.png)


Given any _a_ , it is easy to compute the corresponding _b_ such that ∆Dempster( _a, b_ ; _n_ ) = _δ_ via a binary search. Note that this leads to adjusted p-values that cannot be lower than _b_ 1 = _a_ +(1 _− a_ ) _/_ (1 _− b_ ) _n_ . To ensure a fair comparison with the method based on the generalized Simes inequality, we choose _a_ via another binary search such that the resulting _b_ 1 matches that given by the Simes inequality for a particular value of _k_ . If there exists no value of _a_ yielding the same _b_ 1 as the Simes method, we set _a_ as to minimize _b_ 1. Figure A2 compares the adjustment functions yielded by the generalized Simes inequality, the DKWM inequality, and the Dempster exact linear-boundary crossing probability with _k ∈{n/_ 4 _, n/_ 2 _}_ and _n ∈{_ 300 _,_ 1000 _,_ 3000 _,_ 10000 _}_ for small marginal p-values within [0 _,_ 0 _._ 05]. It is clear that the Simes adjustment function is the best option in most scenarios, except when _n_ = 10000 and _u_ ˆ<sup>(marg)</sup> ( _X_ ) _>_ 0 _._ 03, in which case the DKWM bound is tighter. Nonetheless, for the purpose of multiple testing, we would rarely expect p-values above 0 _._ 03 to be significant. 

68 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0069-00.png)


Figure A2: Comparison of different adjustment functions, with _n_ = 1000 and _δ_ = 0 _._ 1. 

69 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0070-00.png)


Figure A3: Comparison of different adjustment functions, with _n_ = 10000 and _δ_ = 0 _._ 1. Other details are as in Figure A2. 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0070-02.png)


Figure A4: Comparison of different adjustment functions, with _n_ = 1000 and _δ_ = 0 _._ 1. 

70 

## **D Numerical outlier detection experiments** 

### **D.1 Outlier detection on simulated data** 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0071-02.png)


Figure A5: FDR and power in a simulated outlier detection problem as a function of the number of samples in the data set (half of which are utilized for calibration). Other details are as in Figure 7. 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0071-04.png)


Figure A6: FDR and power in a simulated outlier detection problem, using the BH procedure with Storey’s correction. Other details are as in Figure A5. 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0071-06.png)


Figure A7: FDR and power in a simulated outlier detection problem, using the BH procedure with Storey’s correction. Other details are as in Figure 7. 

71 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0072-00.png)


Figure A8: FDR and power in a simulated outlier detection problem, using the BH procedure with Storey’s correction. The conditional calibration method is applied with _δ_ = 0 _._ 25 instead of _δ_ = 0 _._ 1. Other details are as in Figure 7. 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0072-02.png)


Figure A9: Performance of simultaneously calibrated conformal p-values as a function of the Simes parameter _n/k_ . The signal strength is equal to 2. Other details are as in Figure 7. 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0072-04.png)


Figure A10: Performance of different methods for calibrating conformal p-values in a simulated outlier batch detection problem, for different values of the signal strength. Other details are as in Figure A10. 

72 


![](Testing_for_Outliers_with_Conformal_p-values_images/Testing_for_Outliers_with_Conformal_p-values.pdf-0073-00.png)


Figure A11: Performance of different methods for combining p-values from the same batch for the purpose of global testing. Other details are as in Figure 8. 

73 

### **D.2 Outlier detection on real data** 

Table A1: Outlier detection performance on real data, using different data sets, machine learning models, and nominal FDR levels. The BH procedure is applied with Storey’s correction to control the FDR. Other details are as in Table 2. 

|||FDR||||Po|wer||
|---|---|---|---|---|---|---|---|---|
||M|ean|90th p|ercentile|M|ean|90-th|quantile|
|Model<br>Nominal|Marg.|Cond.|Marg.|Cond.|Marg.|Cond.|Marg.|Cond.|
|**ALOI**|||||||||
|0.05<br>IForest|0|0|0|0|0|0|0|0|
|0.10|0.001|0|0|0|0|0|0|0|
|0.20|0.025|0.001|0.048|0|0|0|0|0|
|0.05<br>Neighbors|0|0|0|0|0|0|0|0|
|0.10<br>|0.005|0|0|0|0|0|0|0|
|0.20|0.059|0.008|0.245|0.01|0.002|0|0.007|0|
|0.05<br>SVM|0|0|0|0|0|0|0|0|
|0.10|0.006|0|0.006|0|0|0|0.001|0|
|0.20|0.066|0.009|0.212|0.017|0.003|0|0.01|0.002|
|**Cover**|||||||||
|0.05<br>IForest|0.004|0.001|0|0|0.001|0|0|0|
|0.10|0.017|0.007|0.037|0.002|0.003|0.001|0.005|0|
|0.20|0.099|0.044|0.297|0.148|0.012|0.006|0.038|0.02|
|0.05<br>Neighbors|0.047|0.038|0.067|0.054|0.948|0.935|0.964|0.957|
|0.10<br>|0.096|0.081|0.124|0.106|0.972|0.968|0.98|0.976|
|0.20|0.195|0.174|0.231|0.207|0.987|0.985|0.99|0.989|
|0.05<br>SVM|0|0|0|0|0|0|0|0|
|0.10|0|0|0|0|0|0|0|0|
|0.20|0|0|0|0|0|0|0|0|
|**Credit card**|||||||||
|0.05<br>IForest|0.032|0.016|0.07|0.051|0.149|0.08|0.358|0.264|
|0.10|0.09|0.063|0.13|0.105|0.383|0.277|0.57|0.518|
|0.20|0.191|0.162|0.228|0.202|0.679|0.611|0.782|0.746|
|0.05<br>Neighbors|0|0|0|0|0|0|0|0|
|0.10|0.005|0.001|0|0|0.001|0|0|0|
|0.20|0.074|0.027|0.283|0.086|0.006|0.003|0.024|0.008|
|0.05<br>SVM|0|0|0|0|0|0|0|0|
|0.10|0|0|0|0|0|0|0|0|
|0.20|0|0|0|0|0|0|0|0|
|**KDDCup99**|||||||||
|0.05<br>IForest|0.039|0.02|0.076|0.047|0.359|0.216|0.51|0.465|
|0.10|0.096|0.059|0.129|0.098|0.598|0.452|0.715|0.644|
|0.20|0.194|0.131|0.23|0.168|0.754|0.684|0.825|0.753|
|0.05<br>Neighbors|0.006|0|0|0|0.001|0|0|0|
|0.10|0.03|0.009|0.147|0|0.009|0.002|0.049|0|
|0.20|0.125|0.042|0.274|0.17|0.033|0.011|0.068|0.056|



_(Continued on Next Page...)_ 

74 

Table A1: Outlier detection performance on real data, using different data sets, machine learning models, and nominal FDR levels. The BH procedure is applied with Storey’s correction to control the FDR. Other details are as in Table 2. _(continued)_ 

||||FDR||||Po|wer||
|---|---|---|---|---|---|---|---|---|---|
|||M|ean|90th p|ercentile|M|ean|90-th|quantile|
|Model<br>No|minal|Marg.|Cond.|Marg.|Cond.|Marg.|Cond.|Marg.|Cond.|
|SVM|0.05|0|0|0|0|0|0|0|0|
||0.10|0|0|0|0|0|0|0|0|
||0.20|0|0|0|0|0|0|0|0|
|**Mammography**||||||||||
|IForest|0.05|0.011|0|0.037|0|0.01|0|0.023|0|
||0.10|0.076|0.002|0.171|0|0.059|0.004|0.146|0|
||0.20|0.187|0.056|0.286|0.17|0.176|0.059|0.337|0.22|
|Neighbors|0.05|0|0|0|0|0|0|0|0|
||0.10|0.016|0|0.027|0|0.011|0|0.021|0|
||0.20|0.155|0.023|0.263|0.084|0.175|0.024|0.285|0.078|
|SVM|0.05|0.007|0|0.018|0|0.003|0|0.008|0|
||0.10|0.066|0|0.168|0|0.04|0|0.09|0|
||0.20|0.188|0.046|0.274|0.145|0.171|0.032|0.288|0.095|
|**Digits**||||||||||
|IForest|0.05|0.012|0|0.03|0|0.013|0|0.036|0|
||0.10|0.058|0.004|0.164|0|0.076|0.006|0.295|0|
||0.20|0.202|0.052|0.266|0.173|0.417|0.096|0.629|0.355|
|Neighbors|0.05|0.006|0|0.028|0|0.033|0.002|0.049|0|
||0.10|0.059|0.006|0.135|0.01|0.273|0.035|0.752|0.03|
||0.20|0.191|0.092|0.238|0.166|0.841|0.455|0.99|0.879|
|SVM|0.05|0.004|0|0.003|0|0.002|0|0.001|0|
||0.10|0.044|0|0.149|0|0.018|0|0.045|0|
||0.20|0.175|0.018|0.264|0.066|0.227|0.017|0.468|0.048|
|**Shuttle**||||||||||
|IForest|0.05|0.047|0.031|0.068|0.049|0.936|0.889|0.975|0.972|
||0.10|0.096|0.072|0.122|0.097|0.974|0.965|0.981|0.979|
||0.20|0.196|0.163|0.228|0.198|0.981|0.98|0.984|0.983|
|Neighbors|0.05|0.048|0.031|0.066|0.047|0.99|0.951|0.998|0.991|
||0.10|0.098|0.07|0.125|0.093|0.999|0.996|1|1|
||0.20|0.199|0.151|0.231|0.193|1|1|1|1|
|SVM|0.05|0.043|0.021|0.066|0.045|0.814|0.486|0.998|0.993|
||0.10|0.096|0.069|0.127|0.093|0.999|0.997|1|0.999|
||0.20|0.198|0.148|0.233|0.182|1|1|1|1|



75 

Table A2: Outlier detection performance on real data, using different data sets, machine learning models, and nominal FDR levels. The BH procedure is applied without Storey’s correction to control the FDR. Other details are as in Table A1. 

||||FDR||||Po|wer||
|---|---|---|---|---|---|---|---|---|---|
|||M|ean|90th p|ercentile|M|ean|90-th|quantile|
|Model|Nominal|Marg.|Cond.|Marg.|Cond.|Marg.|Cond.|Marg.|Cond.|
|**ALOI**||||||||||
|IForest|0.05|0|0|0|0|0|0|0|0|
||0.10|0.001|0|0|0|0|0|0|0|
||0.20|0.032|0.002|0.08|0|0|0|0|0|
|Neighbors|0.05|0|0|0|0|0|0|0|0|
||0.10|0.004|0|0|0|0|0|0|0|
||0.20|0.057|0.008|0.234|0.01|0.002|0|0.006|0|
|SVM|0.05|0|0|0|0|0|0|0|0|
||0.10|0.007|0|0.009|0|0|0|0.001|0|
||0.20|0.076|0.012|0.231|0.019|0.003|0.001|0.011|0.002|
|**Cover**||||||||||
|IForest|0.05|0.004|0|0|0|0.001|0|0|0|
||0.10|0.014|0.006|0.026|0|0.002|0.001|0.003|0|
||0.20|0.089|0.03|0.285|0.083|0.01|0.005|0.035|0.013|
|Neighbors|0.05|0.043|0.034|0.058|0.047|0.942|0.929|0.961|0.954|
||0.10|0.086|0.073|0.109|0.097|0.97|0.965|0.978|0.974|
||0.20|0.176|0.158|0.211|0.191|0.985|0.983|0.989|0.987|
|SVM|0.05|0|0|0|0|0|0|0|0|
||0.10|0|0|0|0|0|0|0|0|
||0.20|0|0|0|0|0|0|0|0|
|**Credit card**||||||||||
|IForest|0.05|0.027|0.013|0.065|0.047|0.125|0.066|0.332|0.248|
||0.10|0.082|0.057|0.122|0.099|0.351|0.249|0.542|0.482|
||0.20|0.173|0.146|0.212|0.186|0.642|0.57|0.763|0.712|
|Neighbors|0.05|0|0|0|0|0|0|0|0|
||0.10|0.005|0.001|0|0|0|0|0|0|
||0.20|0.072|0.021|0.292|0.062|0.006|0.002|0.024|0.006|
|SVM|0.05|0|0|0|0|0|0|0|0|
||0.10|0|0|0|0|0|0|0|0|
||0.20|0|0|0|0|0|0|0|0|
|**KDDCup99**||||||||||
|IForest|0.05|0.033|0.017|0.073|0.045|0.329|0.188|0.496|0.465|
||0.10|0.086|0.055|0.118|0.093|0.562|0.437|0.695|0.627|
||0.20|0.174|0.124|0.209|0.159|0.736|0.673|0.796|0.745|
|Neighbors|0.05|0.006|0|0|0|0.001|0|0|0|
||0.10|0.028|0.008|0.136|0|0.008|0.002|0.05|0|
||0.20|0.122|0.041|0.276|0.17|0.032|0.011|0.069|0.055|



_(Continued on Next Page...)_ 

76 

Table A2: Outlier detection performance on real data, using different data sets, machine learning models, and nominal FDR levels. The BH procedure is applied without Storey’s correction to control the FDR. Other details are as in Table A1. _(continued)_ 

|||FDR||||Po|wer||
|---|---|---|---|---|---|---|---|---|
||M|ean|90th p|ercentile|M|ean|90-th|quantile|
|Model<br>Nominal|Marg.|Cond.|Marg.|Cond.|Marg.|Cond.|Marg.|Cond.|
|0.05<br>SVM|0|0|0|0|0|0|0|0|
|0.10|0|0|0|0|0|0|0|0|
|0.20|0|0|0|0|0|0|0|0|
|**Mammography**|||||||||
|0.05<br>IForest|0.008|0|0.011|0|0.007|0|0.006|0|
|0.10|0.061|0.002|0.161|0|0.045|0.003|0.125|0|
|0.20|0.167|0.054|0.269|0.169|0.156|0.058|0.305|0.217|
|0.05<br>Neighbors|0|0|0|0|0|0|0|0|
|0.10|0.011|0|0.01|0|0.007|0|0.005|0|
|0.20|0.126|0.021|0.241|0.078|0.14|0.022|0.272|0.088|
|0.05<br>SVM|0.003|0|0.004|0|0.001|0|0.003|0|
|0.10|0.053|0|0.155|0|0.033|0|0.077|0|
|0.20|0.171|0.046|0.264|0.147|0.145|0.032|0.257|0.094|
|**Digits**|||||||||
|0.05<br>IForest|0.01|0|0.013|0|0.01|0|0.012|0|
|0.10|0.051|0.004|0.155|0|0.062|0.006|0.246|0|
|0.20|0.182|0.054|0.248|0.174|0.357|0.099|0.59|0.326|
|0.05<br>Neighbors|0.005|0|0.008|0|0.027|0.002|0.025|0|
|0.10|0.044|0.005|0.123|0.008|0.202|0.031|0.667|0.027|
|0.20|0.172|0.084|0.217|0.16|0.791|0.421|0.982|0.871|
|0.05<br>SVM|0.003|0|0|0|0.001|0|0|0|
|0.10|0.04|0|0.151|0|0.014|0|0.041|0|
|0.20|0.158|0.021|0.255|0.097|0.154|0.019|0.39|0.043|
|**Shuttle**|||||||||
|0.05<br>IForest|0.042|0.029|0.06|0.044|0.926|0.88|0.975|0.972|
|0.10|0.086|0.066|0.11|0.09|0.972|0.961|0.981|0.978|
|0.20|0.178|0.149|0.212|0.187|0.98|0.979|0.983|0.983|
|0.05<br>Neighbors|0.042|0.029|0.062|0.042|0.987|0.925|0.997|0.99|
|0.10<br>|0.087|0.065|0.111|0.085|0.998|0.995|1|1|
|0.20|0.178|0.139|0.208|0.174|1|0.999|1|1|
|0.05<br>SVM|0.038|0.019|0.06|0.045|0.792|0.462|0.997|0.993|
|0.10|0.087|0.064|0.112|0.086|0.999|0.996|1|0.999|
|0.20|0.178|0.138|0.208|0.168|1|1|1|1|



77 

Table A3: Outlier batch detection performance on real data, using Storey’s correction to control the FDR. Other details are as in Table A4. 

||||FDR||||Po|wer||
|---|---|---|---|---|---|---|---|---|---|
|||M|ean|90th p|ercentile|M|ean|90-th|quantile|
|Model<br>No|minal|Marg.|Cond.|Marg.|Cond.|Marg.|Cond.|Marg.|Cond.|
|**ALOI**||||||||||
|IForest|0.05|0.029|0.008|0.1|0.003|0|0|0.002|0|
||0.10|0.07|0.016|0.2|0.081|0.001|0|0.004|0.002|
||0.20|0.157|0.048|0.332|0.16|0.004|0.001|0.009|0.003|
|LOF|0.05|0.038|0.009|0.108|0.041|0.023|0.009|0.04|0.017|
||0.10|0.079|0.025|0.176|0.083|0.049|0.02|0.078|0.037|
||0.20|0.167|0.069|0.288|0.156|0.109|0.045|0.154|0.073|
|SVM|0.05|0.035|0.006|0.1|0.006|0.003|0.001|0.007|0.003|
||0.10|0.069|0.025|0.173|0.09|0.006|0.003|0.012|0.007|
||0.20|0.157|0.058|0.33|0.17|0.014|0.005|0.023|0.01|
|**Cover**||||||||||
|IForest|0.05|0.037|0.021|0.099|0.079|0.1|0.068|0.185|0.122|
||0.10|0.08|0.05|0.158|0.12|0.184|0.132|0.333|0.243|
||0.20|0.176|0.118|0.277|0.206|0.332|0.253|0.535|0.451|
|LOF|0.05|0.046|0.029|0.074|0.056|1|1|1|1|
||0.10|0.096|0.068|0.138|0.109|1|1|1|1|
||0.20|0.197|0.147|0.274|0.211|1|1|1|1|
|SVM|0.05|0|0|0|0|0|0|0|0|
||0.10|0|0|0|0|0|0|0|0|
||0.20|0|0|0|0|0|0|0|0|
|**Credit card**||||||||||
|IForest|0.05|0.04|0.026|0.064|0.049|0.965|0.951|0.983|0.972|
||0.10|0.086|0.059|0.126|0.094|0.981|0.973|0.992|0.987|
||0.20|0.179|0.131|0.251|0.184|0.992|0.988|0.998|0.996|
|LOF|0.05|0.039|0.022|0.1|0.085|0.034|0.022|0.055|0.037|
||0.10|0.081|0.048|0.179|0.11|0.062|0.043|0.097|0.066|
||0.20|0.17|0.112|0.309|0.208|0.122|0.084|0.178|0.135|
|SVM|0.05|0|0|0|0|0|0|0|0|
||0.10|0|0|0|0|0|0|0|0|
||0.20|0|0|0|0|0|0|0|0|
|**KDDCup99**||||||||||
|IForest|0.05|0.044|0.019|0.077|0.043|0.998|0.993|1|0.999|
||0.10|0.091|0.044|0.145|0.08|1|0.998|1|1|
||0.20|0.191|0.099|0.267|0.166|1|1|1|1|
|LOF|0.05|0.045|0.021|0.094|0.076|0.064|0.03|0.103|0.052|
||0.10|0.086|0.038|0.17|0.089|0.108|0.053|0.164|0.087|
||0.20|0.182|0.074|0.287|0.165|0.19|0.096|0.266|0.146|



_(Continued on Next Page...)_ 

78 

Table A3: Outlier batch detection performance on real data, using Storey’s correction to control the FDR. Other details are as in Table A4. _(continued)_ 

||||FDR||||Po|wer||
|---|---|---|---|---|---|---|---|---|---|
|||M|ean|90th p|ercentile|M|ean|90-th|quantile|
|Model|Nominal|Marg.|Cond.|Marg.|Cond.|Marg.|Cond.|Marg.|Cond.|
|SVM|0.05|0|0|0|0|0|0|0|0|
||0.10|0|0|0|0|0|0|0|0|
||0.20|0|0|0|0|0|0|0|0|
|**Mammog**|**raphy**|||||||||
|IForest|0.05|0.034|0.005|0.066|0.019|0.476|0.228|0.628|0.394|
||0.10|0.069|0.014|0.116|0.03|0.599|0.334|0.742|0.521|
||0.20|0.138|0.035|0.215|0.067|0.728|0.467|0.844|0.658|
|LOF|0.05|0.032|0.01|0.067|0.032|0.429|0.202|0.575|0.35|
||0.10|0.066|0.018|0.114|0.047|0.561|0.314|0.691|0.485|
||0.20|0.14|0.04|0.201|0.087|0.697|0.457|0.814|0.619|
|SVM|0.05|0.008|0|0.022|0|0.34|0.144|0.437|0.225|
||0.10|0.02|0.002|0.048|0.005|0.451|0.228|0.546|0.332|
||0.20|0.043|0.009|0.083|0.023|0.57|0.341|0.655|0.45|
|**Digits**||||||||||
|IForest|0.05|0.04|0.006|0.074|0.017|0.924|0.673|0.986|0.842|
||0.10|0.084|0.016|0.141|0.033|0.968|0.814|0.995|0.926|
||0.20|0.176|0.038|0.268|0.075|0.991|0.911|1|0.981|
|LOF|0.05|0.045|0.007|0.082|0.019|0.999|0.977|1|1|
||0.10|0.093|0.019|0.151|0.038|1|0.994|1|1|
||0.20|0.191|0.046|0.277|0.084|1|0.999|1|1|
|SVM|0.05|0.049|0.007|0.091|0.021|0.824|0.511|0.896|0.665|
||0.10|0.104|0.02|0.166|0.045|0.905|0.674|0.956|0.8|
||0.20|0.206|0.049|0.302|0.098|0.957|0.81|0.985|0.9|
|**Shuttle**||||||||||
|IForest|0.05|0.046|0.021|0.077|0.04|1|1|1|1|
||0.10|0.094|0.047|0.142|0.087|1|1|1|1|
||0.20|0.194|0.102|0.281|0.161|1|1|1|1|
|LOF|0.05|0.045|0.019|0.082|0.04|1|1|1|1|
||0.10|0.095|0.041|0.158|0.081|1|1|1|1|
||0.20|0.193|0.094|0.287|0.166|1|1|1|1|
|SVM|0.05|0.038|0.013|0.066|0.026|1|1|1|1|
||0.10|0.085|0.034|0.121|0.059|1|1|1|1|
||0.20|0.18|0.083|0.244|0.137|1|1|1|1|



79 

Table A4: Outlier batch detection performance on real data, using different data sets, machine learning models, and nominal FDR levels. Other details are as in Table A3. 

||||FDR||||Po|wer||
|---|---|---|---|---|---|---|---|---|---|
|||M|ean|90th p|ercentile|M|ean|90-th|quantile|
|Model<br>No|minal|Marg.|Cond.|Marg.|Cond.|Marg.|Cond.|Marg.|Cond.|
|**ALOI**||||||||||
|IForest|0.05|0.027|0.009|0.1|0.034|0|0|0.002|0|
||0.10|0.067|0.021|0.191|0.096|0.001|0|0.004|0.002|
||0.20|0.157|0.059|0.341|0.186|0.004|0.001|0.008|0.004|
|LOF|0.05|0.032|0.01|0.093|0.054|0.021|0.009|0.038|0.018|
||0.10|0.07|0.025|0.154|0.084|0.044|0.02|0.066|0.033|
||0.20|0.152|0.07|0.279|0.154|0.097|0.045|0.138|0.069|
|SVM|0.05|0.034|0.006|0.1|0.001|0.003|0.001|0.007|0.004|
||0.10|0.07|0.027|0.186|0.096|0.006|0.003|0.012|0.007|
||0.20|0.154|0.064|0.294|0.19|0.013|0.006|0.022|0.012|
|**Cover**||||||||||
|IForest|0.05|0.031|0.02|0.086|0.071|0.091|0.065|0.172|0.113|
||0.10|0.072|0.046|0.143|0.111|0.168|0.126|0.309|0.234|
||0.20|0.155|0.109|0.243|0.189|0.304|0.24|0.506|0.427|
|LOF|0.05|0.04|0.027|0.067|0.05|1|1|1|1|
||0.10|0.086|0.063|0.121|0.095|1|1|1|1|
||0.20|0.176|0.138|0.234|0.19|1|1|1|1|
|SVM|0.05|0|0|0|0|0|0|0|0|
||0.10|0|0|0|0|0|0|0|0|
||0.20|0|0|0|0|0|0|0|0|
|**Credit card**||||||||||
|IForest|0.05|0.035|0.025|0.058|0.042|0.963|0.951|0.983|0.972|
||0.10|0.077|0.056|0.116|0.087|0.98|0.973|0.992|0.986|
||0.20|0.16|0.124|0.223|0.17|0.992|0.988|0.998|0.995|
|LOF|0.05|0.035|0.021|0.097|0.085|0.031|0.022|0.047|0.037|
||0.10|0.072|0.047|0.168|0.107|0.057|0.04|0.087|0.062|
||0.20|0.153|0.103|0.276|0.2|0.11|0.08|0.159|0.12|
|SVM|0.05|0|0|0|0|0|0|0|0|
||0.10|0|0|0|0|0|0|0|0|
||0.20|0|0|0|0|0|0|0|0|
|**KDDCup99**||||||||||
|IForest|0.05|0.039|0.019|0.067|0.043|0.998|0.994|1|0.999|
||0.10|0.08|0.043|0.126|0.079|0.999|0.998|1|1|
||0.20|0.171|0.099|0.238|0.158|1|1|1|1|
|LOF|0.05|0.043|0.021|0.095|0.08|0.06|0.032|0.093|0.052|
||0.10|0.08|0.039|0.168|0.09|0.101|0.056|0.143|0.087|
||0.20|0.165|0.075|0.267|0.158|0.176|0.1|0.246|0.148|



_(Continued on Next Page...)_ 

80 

Table A4: Outlier batch detection performance on real data, using different data sets, machine learning models, and nominal FDR levels. Other details are as in Table A3. _(continued)_ 

||||FDR||||Po|wer||
|---|---|---|---|---|---|---|---|---|---|
|||M|ean|90th p|ercentile|M|ean|90-th|quantile|
|Model|Nominal|Marg.|Cond.|Marg.|Cond.|Marg.|Cond.|Marg.|Cond.|
|SVM|0.05|0|0|0|0|0|0|0|0|
||0.10|0|0|0|0|0|0|0|0|
||0.20|0|0|0|0|0|0|0|0|
|**Mammog**|**raphy**|||||||||
|IForest|0.05|0.035|0.007|0.066|0.022|0.482|0.259|0.63|0.433|
||0.10|0.069|0.018|0.111|0.044|0.606|0.376|0.736|0.56|
||0.20|0.14|0.045|0.209|0.079|0.735|0.517|0.846|0.694|
|LOF|0.05|0.032|0.011|0.062|0.035|0.435|0.232|0.577|0.373|
||0.10|0.067|0.022|0.108|0.05|0.571|0.354|0.694|0.52|
||0.20|0.142|0.05|0.194|0.093|0.705|0.505|0.803|0.656|
|SVM|0.05|0.012|0.001|0.028|0.002|0.382|0.189|0.472|0.272|
||0.10|0.027|0.004|0.056|0.013|0.497|0.29|0.585|0.39|
||0.20|0.057|0.015|0.1|0.038|0.62|0.418|0.69|0.515|
|**Digits**||||||||||
|IForest|0.05|0.035|0.007|0.057|0.018|0.92|0.719|0.985|0.876|
||0.10|0.075|0.019|0.118|0.037|0.966|0.851|0.994|0.952|
||0.20|0.156|0.047|0.223|0.081|0.99|0.935|1|0.987|
|LOF|0.05|0.04|0.008|0.071|0.02|0.999|0.984|1|1|
||0.10|0.083|0.022|0.137|0.041|1|0.996|1|1|
||0.20|0.169|0.055|0.242|0.092|1|1|1|1|
|SVM|0.05|0.043|0.009|0.078|0.025|0.811|0.55|0.883|0.689|
||0.10|0.089|0.023|0.138|0.048|0.898|0.712|0.94|0.813|
||0.20|0.179|0.056|0.251|0.104|0.953|0.841|0.979|0.912|
|**Shuttle**||||||||||
|IForest|0.05|0.041|0.02|0.068|0.042|1|1|1|1|
||0.10|0.084|0.046|0.131|0.084|1|1|1|1|
||0.20|0.172|0.103|0.236|0.155|1|1|1|1|
|LOF|0.05|0.041|0.019|0.073|0.039|1|1|1|1|
||0.10|0.084|0.042|0.132|0.078|1|1|1|1|
||0.20|0.17|0.095|0.237|0.161|1|1|1|1|
|SVM|0.05|0.034|0.014|0.056|0.027|1|1|1|1|
||0.10|0.074|0.035|0.11|0.059|1|1|1|1|
||0.20|0.16|0.085|0.22|0.134|1|1|1|1|



81 

