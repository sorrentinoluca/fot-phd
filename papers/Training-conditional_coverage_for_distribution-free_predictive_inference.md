# Training-conditional coverage for distribution-free predictive inference 

Michael Bian<sup>∗</sup> Rina Foygel Barber<sup>∗</sup> 

January 19, 2023 

##### **Abstract** 

The field of distribution-free predictive inference provides tools for provably valid prediction without any assumptions on the distribution of the data, which can be paired with any regression algorithm to provide accurate and reliable predictive intervals. The guarantees provided by these methods are typically marginal, meaning that predictive accuracy holds on average over both the training data set and the test point that is queried. However, it may be preferable to obtain a stronger guarantee of training-conditional coverage, which would ensure that most draws of the training data set result in accurate predictive accuracy on future test points. This property is known to hold for the split conformal prediction method. In this work, we examine the training-conditional coverage properties of several other distribution-free predictive inference methods, and find that training-conditional coverage is achieved by some methods but is impossible to guarantee without further assumptions for others. 

## **1 Introduction** 

Distribution-free predictive inference provides a set of methods for constructing predictive confidence intervals with minimal assumptions about the underlying distribution. Specifically, in the case of regression, suppose we are given i.i.d. training points ( _Xi, Yi_ ) _∈X ×_ R, _i_ = 1 _, ..., n_ , and a regression algorithm _A_ that maps training points � to prediction rules _µ_ : _X →_ R. Given a new feature vector _Xn_ +1, we would like to predict the unseen response _Yn_ +1. A predictive interval _C_<sup>�</sup> _n_ , trained on these _n_ training data points using this regression algorithm _A_ , returns an interval (or more generally, a subset) _C_<sup>�</sup> _n_ ( _Xn_ +1) _⊆_ R, with the goal that _C_<sup>�</sup> _n_ ( _Xn_ +1) should contain the response value _Yn_ +1 for this test point. We say that _C_<sup>�</sup> _n_ is a _distribution-free predictive interval_ if, for every distribution _P_ on _X ×_ R it holds that 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0001-08.png)


> ∗Department of Statistics, University of Chicago 

1 

Here the notation P _P n_ +1 _{·}_ denotes that the probability is computed with respect to iid ( _X_ 1 _, Y_ 1) _, ...,_ ( _Xn, Yn_ ) _,_ ( _Xn_ +1 _, Yn_ +1) _∼ P_ . 

In practice, we are often interested in the coverage rate for test points once we fit a regression algorithm to a particular training set. However, the guarantee in (1) does not directly address this. Rather, it bounds the miscoverage rate _on average_ over possible sets of training data and test points. As a result, if there is high variability in the coverage rate as a function of the training data, the test coverage rate may be substantially below 1 _− α_ for a particular training set. In this case, while (1) is satisfied on average, after fitting on the realized draw of the training set distribution the practitioner may be left with prediction intervals which drastically undercover. 

To formalize this intuition, let _Dn_ = �( _X_ 1 _, Y_ 1) _, ...,_ ( _Xn, Yn_ )� be the training data set. Then, define the miscoverage rate as a function of the training data: 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0002-03.png)


where the probability is now only with respect to the test point ( _Xn_ +1 _, Yn_ +1) drawn from _P_ . Then, the guarantee in (1) can be re-written as 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0002-05.png)


where the expectation is with respect to the training data _Dn ∼ P_<sup>_n_</sup> (and, in order to be distribution-free, this bound is again required to hold for every distribution _P_ on _X ×_ R). 

While this expectation is bounded, _αP_ ( _Dn_ ) may have high variance over the training data. In particular, we can consider a worst-case scenario where 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0002-08.png)


which trivially satisfies the marginal coverage guarantee (1) since E _P n_ [ _αP_ ( _Dn_ )] = _α_ . In other words, in this worst-case scenario, a nonnegligible proportion of training sets might result in 0% training-conditional coverage even though the average coverage is still 1 _− α_ , which may be highly problematic in practice. On the other hand, if we instead had _αP_ ( _Dn_ ) _≈ α_ with high probability over _Dn ∼ P_<sup>_n_</sup> , this would be ideal, since it ensures that for nearly every possible draw of the training data, the resulting coverage over future test points should be _≈_ 1 _− α_ . 

The variability of training-conditional miscoverage level _αP_ ( _Dn_ ) will in general depend on the distribution _P_ , the regression algorithm _A_ , and the particular distributionfree method that is used to generate _C_<sup>�</sup> _n_ ( _Xn_ +1). In this paper, we examine the variability of coverage for popular distribution-free methods for arbitrary _P_ and _A_ . In particular, we seek to provide guarantees of the form 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0002-11.png)


also known as a “Probably Approximately Correct” (PAC) predictive interval. This type of guarantee turns out to be possible for some distribution-free methods and 

2 

impossible for others. In addition, we demonstrate empirically that methods without guarantees of this form can exhibit highly variable training-conditional miscoverage rates in low stability regimes. 

## **2 Background** 

In this section, we will briefly review four related methods for distribution-free predictive inference, to introduce the methods that we will study in this work. Consider an algorithm _A_ that maps datasets (consisting of ( _X, Y_ ) pairs, with features _X ∈X_ and a real-valued response _Y ∈_ R), to fitted regression functions _µ_ � : _X →_ R. 

For a new data point whose features _Xn_ +1 _∈X_ are observed, we would like to predict the unseen response _Yn_ +1 _∈_ R. Given a model _µ_ � obtained by training some algorithm _A_ on the available training data ( _X_ 1 _, Y_ 1) _, . . . ,_ ( _Xn, Yn_ ), can we construct a prediction interval for _Yn_ +1 around the estimate _µ_ �( _Xn_ +1)? In many practical settings, the distribution of the data is likely unknown, and the regression algorithm _A_ may be a complex “black box” methods whose theoretical properties are not well understood, and therefore it may be challenging to guarantee a particular error bound for _µ_ �( _Xn_ +1) as an estimator of the unseen response _Yn_ +1. 

### **2.1 Distribution-free methods** 

#### **2.1.1 Conformal prediction** 

The conformal prediction framework [Vovk et al., 2005], which includes the full and split conformal methods (also called “transductive” and “inductive” conformal, respectively), provides a mechanism for constructing prediction intervals in this challenging setting, with distribution-free coverage guarantees. (See also Lei et al. [2018] for additional background on these methods.) 

To run the split conformal method, we first partition the _n_ available labeled data points into a training set of size _n_ 0 and a holdout set of size _n_ 1 = _n − n_ 0. After � running the regression algorithm on the training data to obtain the fitted model _µn_ 0 = _A_ �( _X_ 1 _, Y_ 1) _, . . . ,_ ( _Xn_ 0 _, Yn_ 0)�, the prediction interval is defined as 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0003-08.png)


where _Q_<sup>�</sup> _n_ 1 is defined as the _⌈_ (1 _− α_ )( _n_ 1 + 1) _⌉_ -th smallest value of the holdout resid� � uals _|Yn_ 0+1 _− µn_ 0( _Xn_ 0+1) _|, . . . , |Yn − µn_ 0( _Xn_ ) _|_ . This method satisfies the marginal distribution-free predictive coverage guarantee (1) [Vovk et al., 2005]. 

While split conformal offers both computational efficiency and distribution-free coverage, its precision may suffer from the loss of sample size incurred by splitting the data set. In contrast, full conformal uses all the available training data for model fitting, but comes at a high computational cost. Specifically, for every _y ∈_ R, define _µ_ �<sup>_y_</sup> _n_ +1<sup>=</sup> _A_ �( _X_ 1 _, Y_ 1) _, . . . ,_ ( _Xn, Yn_ ) _,_ ( _Xn_ +1 _, y_ )�, the fitted model obtained by running algorithm 

3 

_A_ on the training data together with the hypothesized test point ( _Xn_ +1 _, y_ ). Then construct the prediction set 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0004-01.png)


where _Q_<sup>�</sup><sup>_y_</sup> _n_ +1<sup>isdefinedasthe</sup><sup>_⌈_(1</sup><sup>_−α_)(</sup><sup>_n_+1)</sup><sup>_⌉_-thsmallestvalueoftheresiduals</sup> _|Y_ 1 _− µ_ �<sup>_y_</sup> _n_ +1<sup>(</sup><sup>_X_1)</sup><sup>_|, . . . , |Yn−µ_�</sup><sup>_y_</sup> _n_ +1<sup>(</sup><sup>_Xn_)</sup><sup>_|, |y −µ_�</sup> _n_<sup>_y_</sup> +1<sup>(</sup><sup>_Xn_+1)</sup><sup>_|_.Fullconformalpredictionalso</sup> offers the distribution-free coverage guarantee (1) [Vovk et al., 2005], under one additional assumption—the algorithm _A_ needs to be _symmetric_ in the training data points, meaning that for any _m ≥_ 1, any permutation _σ_ on [ _m_ ] := _{_ 1 _, . . . , m}_ , and any data points ( _x_ 1 _, y_ 1) _, . . . ,_ ( _xm, ym_ ) _∈X ×_ R, 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0004-03.png)


Full conformal prediction is generally more statistically efficient than split conformal (i.e., will provide narrower prediction intervals) since we do not need to split the training data. On the other hand, the computational cost is high—aside from special cases (e.g., choosing _A_ to be the Lasso [Lei, 2019]), the prediction interval can only be calculated by running the regression algorithm _A_ for every possible _y ∈_ R, or in practice, for a very fine grid of _y_ values (theoretical guarantees for this discretized setting can also be obtained, as shown by Chen et al. [2018]). 

#### **2.1.2 Jackknife+ and CV+** 

The jackknife+ and CV+ methods proposed by Barber et al. [2021b] offer a compromise between the computational efficiency of split conformal and the statistical efficiency of full conformal. These methods, which are closely related to the cross-conformal procedure of Vovk [2015], Vovk et al. [2018], use a cross-validation type approach. 

For jackknife+, let _µ_ �[ _n_ ] _\{i}_ denote the model fitted to the training data with data point _i_ removed, 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0004-08.png)


Then the jackknife+ prediction interval is defined as 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0004-10.png)


� where _Ri_ = _|Yi − µ_ [ _n_ ] _\{i}_ ( _Xi_ ) _|_ for _i ∈_ [ _n_ ] := _{_ 1 _, . . . , n}_ . The jackknife+ method offers a weaker distribution-free coverage guarantee [Barber et al., 2021b, Theorem 1]: for every distribution _P_ on _X ×_ R, assuming _A_ is symmetric as in (6), 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0004-12.png)


4 

Note that, in this theoretical guarantee, noncoverage may be as high as 2 _α_ , rather than the target level _α_ . However, empirically the method typically achieves coverage at level 1 _− α_ , and indeed, under algorithmic stability assumptions, e.g., 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0005-01.png)


the predictive coverage guarantee can be improved to 1 _−α −_ o(1) [Barber et al., 2021b, Theorem 5]. 

While jackknife+ requires only _n_ many calls to the regression algorithm _A_ (in contrast to full conformal, which in theory requires infinitely many calls), for a large sample size _n_ this computational cost may still be too high. CV+ extends the jackknife+ method to _K_ -fold cross-validation (where we can view jackknife+ as _n_ -fold cross-validation, i.e., _K_ = _n_ ). Let [ _n_ ] = _S_ 1 _∪· · · ∪ SK_ be a partition of the training data into _K_ subsets of size _n/K_ , and write _µ_ �[ _n_ ] _\Sk_ as the fitted model when the _k_ -th fold _Sk_ is removed from the _n_ training data points. The CV+ prediction interval is as 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0005-04.png)


� where now _Ri_ = _|Yi − µ_ [ _n_ ] _\Sk_ ( _i_ )( _Xi_ ) _|_ for _i ∈_ [ _n_ ], and where _k_ ( _i_ ) denotes the fold to which data point _i_ belongs, i.e., _i ∈ Sk_ ( _i_ ). The CV+ method’s coverage guarantee is given by Barber et al. [2021b, Theorem 4] (see also Vovk et al. [2018] for a partial version of this result): for every distribution _P_ on _X ×_ R, assuming _A_ is symmetric as in (6), 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0005-06.png)


As for jackknife+, the CV+ method typically achieves coverage near or above the target level 1 _− α_ in practice. 

#### **2.1.3 A note on randomized algorithms** 

The background given above implicitly treats the algorithm _A_ as a _deterministic_ function of the training data—that is, we view _A_ as a function �( _X_ 1 _, Y_ 1) _, . . . ,_ ( _Xn, Yn_ )� _�→ µ_ �. In many settings, however, it is common to use a _randomized_ regression algorithm—for instance, stochastic gradient descent. In this setting, we can formally view _A_ as a function �( _X_ 1 _, Y_ 1) _, . . . ,_ ( _Xn, Yn_ ) _, ξ_ � _�→ µ_ �, where the term _ξ_ introduces stochastic noise (effectively, a random seed). All the results described above hold for both the deterministic and randomized settings. (For results that assume _A_ is symmetric, the symmetry condition (6) should be understood in the distributional sense—that is, the training data points are treated symmetrically with respect to the randomized training procedure. For example, for stochastic gradient descent, if data points are drawn uniformly at random during the training epochs, then symmetry is satisfied.) 

5 

### **2.2 Marginal or conditional validity** 

The predictive coverage bound (1) achieved by split and full conformal, or the bounds (8) and (11) for the jackknife+ and CV+ methods, are all _marginal_ guarantees. This means that the probability is calculated over a random draw of both the training and test data. However, this may be unsatisfactory for practical purposes, in several ways. 

**Training-conditional coverage** First, as discussed in Section 1 above, we may be interested in _training-conditional coverage_ , which ensures that the predictive coverage guarantees hold (at least approximately) even after conditioning on the training data set _Dn_ = �( _X_ 1 _, Y_ 1) _, . . . ,_ ( _Xn, Yn_ )�. For the split conformal method described in (4), Vovk [2012, Proposition 2a] establishes training-conditional coverage through a Hoeffding bound: 

**Theorem 1** (Vovk [2012, Proposition 2a]) **.** _Consider the split conformal method defined in_ (4) _with sample size n_ = _n_ 0+ _n_ 1 _, where n_ 0 _≥_ 1 _many data points are used for training the fitted model_ � _µn_ 0 _(with an arbitrary algorithm) while the remaining n_ 1 _≥_ 1 _data points are used as the holdout set. Then, for any distribution P and any δ ∈_ (0 _,_ 0 _._ 5] _,_ 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0006-04.png)


This result holds for both deterministic and randomized algorithms _A_ . Note that it is not necessary to assume that _A_ is symmetric. 

In other words, the probability that a training set results in a significantly higher training-conditional miscoverage rate than the nominal rate, is vanishingly small under the split conformal method. Of course, by running split conformal at a modified value log(1 _<u>/δ</u>_ <u>)</u> _α_<sup>_′_</sup> := _α −_ ~~�~~ 2 _n_ 1 , we would obtain a slightly more conservative prediction interval that would then satisfy 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0006-07.png)


This type of guarantee (i.e., with probability at least 1 _− δ_ , we obtain at least 1 _− α_ coverage, where _α_ and _δ_ are specified by the user) is often referred to as a _probably approximately correct_ (PAC) guarantee. This style of inference guarantee dates back to the work of Wilks [1941], Wald [1943] on setting “tolerance limits”, i.e., a prediction interval (in the univariate case) or prediction region (in the multivariate case), for a iid random variable� _Y ∼ P_ , given _n_ i.i.d. draws _Y_ 1 _, . . . , Yn ∼ P_ (that is, a prediction region _Cn_ for _Y_ without any covariate _X_ , such that _P_ ( _C_ � _n_ ) _≥_ 1 _− α_ holds with probability at least 1 _− δ_ , for user-specified parameters _α_ and _δ_ ). More recent results offering PAC-style training-conditional coverage guarantees for the regression setting, via split conformal and related methods, can be found in the work of Kivaranovic et al. [2020], Bates et al. [2021], Yang and Kuchibhotla [2021], Park et al. [2020]; see also Park et al. 

6 

[2021], Qiu et al. [2022], Yang et al. [2022] for training-conditional coverage under covariate shift. 

No analogous finite-sample results are known for distribution-free prediction methods beyond split conformal, although Steinberger and Leeb [2018] analyze asymptotic training-conditional validity for the jackknife and for cross-validation under algorithmic stability type assumptions such as (9). In this work, our goal will be to examine the finite-sample training-conditional coverage properties of distribution-free methods beyond split conformal. 

**Object-conditional or label-conditional coverage** As a second way in which marginal coverage may not be sufficient for practical utility, we may also be interested in coverage at a particular new test feature vector _Xn_ +1 (referred to in Vovk [2012] as _object-conditional coverage_ )—for instance, if the data points correspond to individual patients in a clinical setting, is it true that a given patient with a particular feature vector _Xn_ +1 = _x_ has a 1 _− α_ probability of a correct predictive interval? That is, we would like to show that the conditional coverage probability P _P n_ +1 _Yn_ +1 _∈ C_<sup>�</sup> _n_ ( _Xn_ +1) _Xn_ +1 = _x_ is _≥_ 1 _− α_ , at least approximately. However, � ��� � Vovk [2012], Lei and Wasserman [2014] show that this type of guarantee is impossible under any distribution _P_ for which _X_ is nonatomic (i.e., P _P {X_ = _x}_ = 0 for all _x ∈ X_ —for instance, this is satisfied by any continuous distribution on R<sup>_d_</sup> ); see also Barber et al. [2021a]. A third type of conditional guarantee is that of _label-conditional coverage_ [Vovk, 2012, L¨ofstr¨om et al., 2015] for the setting where the response _Y_ is categorical, requiring accuracy conditional on the class, i.e., P _P n_ +1 _Yn_ +1 _∈ C_<sup>�</sup> _n_ ( _Xn_ +1) _Yn_ +1 = _y ≥_ � ��� � 1 _− α_ for each category _y_ . Both of these type of conditional guarantees are fundamentally very different from training-conditional coverage, and we will not address these further in this work. 

## **3 Theoretical results** 

As shown in Theorem 1 above, a training-conditional guarantee of the form (3) was established by Vovk [2012] for the split conformal method. In our work, we find that a guarantee of the form (3) can also be shown for the _K_ -fold CV+ method (as long as _n/K_ , the number of data points in each fold, is sufficiently large), but no such guarantees are possible for the full conformal or jackknife+ methods. In this section, we present the main results for each of the three previously unstudied methods. The proofs will be given in Section 4 below. 

First, we consider the full conformal prediction method. In contrast to split conformal, it is impossible to guarantee training-conditional coverage for the full conformal method without further assumptions. 

**Theorem 2.** _For any sample size n ≥_ 2 _and any distribution P for which the marginal PX is nonatomic, there exists a symmetric and deterministic regression algorithm A_ 

7 

_such that the full conformal prediction method defined in_ (5) _satisfies_ 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0008-01.png)


In other words, without placing assumptions on the distribution _P_ and/or the algorithm _A_ (beyond the standard symmetry assumption), we cannot avoid the worst-case scenario (2), where the marginal guarantee of 1 _− α_ coverage stated in (1) is achieved only because the training data set yields _≈_ 100% coverage with probability _≈_ 1 _− α_ , and _≈_ 0% coverage with probability _≈ α_ . (Our result holds only for distributions _P_ where _X_ is nonatomic, i.e., P _P {X_ = _x}_ = 0 for all _x ∈X_ —this condition appears also in the impossibility results for object-conditional coverage as described earlier in Section 2.2.) 

Next, for the jackknife+, the same worst-case result holds. 

**Theorem 3.** _For any sample size n ≥_ 2 _and any distribution P for which the marginal PX is nonatomic, there exists a symmetric and deterministic regression algorithm A such that the jackknife+ prediction interval defined in_ (7) _satisfies_ 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0008-05.png)


Thus, as for full conformal, without placing assumptions on _P_ and/or _A_ (beyond the standard symmetry assumption), we cannot ensure that the jackknife+ method will avoid the worst-case scenario (2). 

In contrast, for CV+, we will now see that the lower bound on marginal coverage, which is ⪆ 1 _−_ 2 _α_ as shown in (11), can also be obtained as a training-conditional guarantee. 

**Theorem 4.** _For any integers K ≥_ 2 _and m ≥_ 1 _, and let n_ = _Km. Suppose CV+ is run with K folds each of size m. Then, for any regression algorithm A and any distribution P , the K-fold CV+ method_ (10) _satisfies_ 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0008-09.png)


_for any δ >_ 0 _._ 

As long as the size of each fold, _m_ = _n/K_ , is large, the bound on _αP_ ( _Dn_ ) is approximately 2 _α_ . Comparing to the marginal result (11) for the CV+ method, we see that the conditional coverage guarantee (for “most” training data sets _Dn_ ) essentially matches the marginal coverage guarantee, and thus could not be improved. Note also that, as in Theorem 1 for split conformal, we do not need to assume _A_ is symmetric, and the result holds regardless of whether _A_ is deterministic or randomized. 

8 

## **4 Proofs** 

Before proceeding to the proofs, we give some brief intuition for why the split conformal and CV+ methods offer training-conditional coverage guarantees, while full conformal and jackknife+ do not. For split conformal, the _n_ 1 residuals on the holdout set 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0009-02.png)


� are i.i.d. after conditioning on the fitted model _µn_ 0, and therefore, for large _n_ 1, their sample quantiles concentrate around the corresponding population quantiles. Similarly, for CV+, for each fold _k_ = 1 _, . . . , K_ we have _m_ = _n/K_ many residuals 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0009-04.png)


that are again i.i.d. conditional on the _k_ -th fitted model _µ_ �[ _n_ ] _\Sk_ , and thus again their sample quantiles concentrate as long as the fold size _m_ = _n/K_ is large. This concentration of the sample quantiles (which we formalize in Lemma 1 below) is the key ingredient for establishing training-conditional coverage. On the other hand, for both full conformal and jackknife+, there is no independence among residuals calculated in each method—for example, for jackknife+, in the leave-one-out residuals � _Ri_ = _|Yi − µ_ [ _n_ ] _\{i}_ ( _Xi_ ) _|_ , for two data points _i_ = _j_ , data point ( _Xi, Yi_ ) is used for training when computing the _j_ -th residual _Rj_ , and vice versa. 

### **4.1 Proofs for split conformal and CV+** 

We begin by considering the split conformal and CV+ methods, which both achieve training-conditional coverage. Both the split conformal result, Theorem 1 [Vovk, 2012, Proposition 2a], and the CV+ result, Theorem 4, can be proved as consequences of the following lemma. 

� **Lemma 1.** _Let n ≥_ 2 _and choose a holdout set A with ∅_ ⊊ _A_ ⊊ [ _n_ ] _. Let µ_ [ _n_ ] _\A_ = _A_ �( _Xi, Yi_ ) : _i ∈_ [ _n_ ] _\A_ � _, where A is any algorithm and may be deterministic or randomized. Define_ 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0009-09.png)


_and_ 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0009-11.png)


_Then p_<sup>_∗_</sup> _A_<sup>(</sup><sup>_Xn_+1</sup><sup>_, Yn_+1)</sup><sup>_isavalidp-valueconditionalonthetrainingdata,i.e.,_</sup> 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0009-13.png)



![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0009-14.png)


9 

Next we will see how this lemma implies the two theorems. First, for split conformal, Theorem 1 is proved by Vovk [2012, Proposition 2a], but here we reformulate the proof in terms of the above lemma, to set up intuition for our CV+ proof later on. 

_Proof of Theorem 1 [Vovk, 2012, Proposition 2a]._ By definition of the split conformal method (4), we have 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0010-02.png)


where _p_ [ _n_ ] _\_ [ _n_ 0]( _x, y_ ) is defined as in Lemma 1 by choosing the holdout set _A_ = [ _n_ ] _\_ [ _n_ 0]. Therefore, we have 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0010-04.png)


Next, fixing any ∆ _>_ 0, consider the event that sup( _x,y_ ) _∈X×_ R � _p_<sup>_∗_</sup> [ _n_ ] _\_ [ _n_ 0]<sup>(</sup><sup>_x, y_)</sup><sup>_−p_[</sup><sup>_n_]</sup><sup>_\_[</sup><sup>_n_</sup> 0<sup>](</sup><sup>_x, y_)</sup> � _≤_ ∆, which is a function of the training data _Dn_ . On this event, we have 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0010-06.png)


where the last step holds by (12). In other words, so far we have shown that 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0010-08.png)


log(1 _<u>/δ</u>_ <u>)</u> Finally, applying (13), this probability is bounded by _δ_ when we choose ∆= ~~�~~ 2 _n_ 1 . 

Next, we prove Theorem 4 for the CV+ method. 

_Proof of Theorem 4._ As in the definition of the CV+ method (10), we let _Ri_ = _|Yi − µ_ �[ _n_ ] _\Sk_ ( _i_ )( _Xi_ ) _|_ for each _i ∈_ [ _n_ ]. Following Barber et al. [2021b, Proof of Theorem 4], the 

10 

CV+ prediction interval defined in (10) deterministically satisfies 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0011-01.png)


where for each fold _k_ , _pSk_ ( _x, y_ ) is defined as in Lemma 1 by choosing the holdout set _A_ = _Sk_ . Therefore, we have 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0011-03.png)


Next, fixing any ∆ _>_ 0, consider the event that max _k_ sup( _x,y_ ) _∈X×_ R � _p_<sup>_∗_</sup> _Sk_<sup>(</sup><sup>_x, y_)</sup><sup>_−pS_</sup> _k_<sup>(</sup><sup>_x, y_)</sup> � _≤_ ∆, which is a function of the training data _Dn_ . On this event, we have 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0011-05.png)


where the last step holds because each _p_<sup>_∗_</sup> _Sk_<sup>(</sup><sup>_Xn_+1</sup><sup>_, Yn_+1)isavalidp-valueconditional</sup> on _Dn_ by (12), and the average of valid p-values is itself a p-value up to a factor of 2 [R¨uschendorf, 1982, Vovk and Wang, 2020]. Combining everything so far, we have shown that 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0011-07.png)


where for the last step we take a union bound. Finally, applying (13) to bound this probability for each fold _k_ , the above quantity is bounded by _δ_ when we choose ∆= log( _K/δ_ <u>)</u> ~~�~~ 2 _m_ . 

To conclude this section, we now prove the supporting lemma. 

11 

_Proof of Lemma 1._ First, for any fixed function _µ_ : _X →_ R, define 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0012-01.png)


In other words, _F_<sup>¯</sup> _µ_ is right-tailed CDF of _|Y − µ_ ( _X_ ) _|_ under ( _X, Y_ ) _∼ P_ . We can therefore write 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0012-03.png)


Since ( _Xn_ +1 _, Yn_ +1) _∼ P_ (and is independent of _µ_ �[ _n_ ] _\A_ ), this is clearly a valid p-value by definition of _F_<sup>¯</sup> _µ_ �[ _n_ ] _\A_ , and so we have proved (12). 

Next, for any ( _x, y_ ) _∈X ×_ R, we can calculate 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0012-06.png)


Finally, since _<u>{</u>_ <u>(</u> _Xi, Yi_ ) _}i∈A_ are drawn i.i.d. from _P_ and are independent from _µ_ �[ _n_ ] _\A_ , for any�∆ _≥_ � lo2 _|_ <u>g</u> _A_ 2 _|_<sup>theDvoretzky–Kiefer–Wolfowitzinequalityimpliesthat,conditional</sup> on _µ_ [ _n_ ] _\A_ , 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0012-08.png)


holds with probability at least 1 _−e_<sup>_−_2</sup><sup>_|A|_∆2</sup> . The same bound therefore holds marginally as well. This proves (13). 

### **4.2 Proofs for full conformal and jackknife+** 

Next, we turn to the results for full conformal and for jackknife+, where we show that training-conditional coverage cannot be guaranteed without further assumptions. The proofs for the two methods are closely related and share the same structure. 

First, fix some large integer _M_ (which we will specify later), and partition _X_ into <u>1</u> _M_ sets, _X_ = _A_ 0 _∪A_ 1 _∪· · ·∪AM −_ 1, where P _P {X ∈ Am}_ = _M_<sup>for each</sup><sup>_m_= 0</sup><sup>_, . . . , M −_1</sup> (since we have assumed _X_ is nonatomic under the distribution _P_ , such a partition exists by Dudley and Norvaiˇsa [2011, Proposition A.1]). Define a map _a_ : _X →{_ 0 _, . . . , M −_ 1 _}_ , 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0012-13.png)


12 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0013-00.png)


Figure 1: Representation of mod(<sup>�</sup><sup>_n_</sup> _i_ =1<sup>_a_(</sup><sup>_Xi_)</sup><sup>_, M_) for</sup><sup>_n_= 3, when</sup><sup>_a_(</sup><sup>_X_1) = 4,</sup><sup>_a_(</sup><sup>_X_2) =</sup><sup>_M −_3,</sup> and _a_ ( _X_ 3) = 1. The left plot shows moving from 0 to mod( _a_ ( _X_ 1) _, M_ ), the middle plot shows moving from mod( _a_ ( _X_ 1) _, M_ ) to mod( _a_ ( _X_ 1) + _a_ ( _X_ 2) _, M_ ), and the right plot shows moving from mod( _a_ ( _X_ 1) + _a_ ( _X_ 2) _, M_ ) to mod( _a_ ( _X_ 1) + _a_ ( _X_ 2) + _a_ ( _X_ 3) _, M_ ). 

assigning each _x ∈X_ to a particular set in the partition. Then, by our choice of the _Am_ ’s, we see that 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0013-03.png)


under the distribution _P_ . By extension, mod(<sup>�</sup><sup>_n_</sup> _i_ =1<sup>_a_(</sup><sup>_Xi_)</sup><sup>_, M_)</sup><sup>_∼_Unif</sup><sup>_{_0</sup><sup>_, ..., M−_1</sup><sup>_}_.</sup> For the sake of illustration, consider a “clock” partitioned into _M_ segments and a hand whose position represents the value of the modulo. In this case, the hand moves forward by _a_ ( _Xi_ ) segments when the _i_ -th term is added inside the modulo—see Figure 1 for an illustration. 

Next, we will define three events, _E_ max, _E_ mod, and _E_ unif, which are all functions of the training data _Dn_ . Define 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0013-06.png)


and let 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0013-08.png)


(Note that we can assume _n_ is sufficiently large so that _α −_ � 2 lo _n_ <u>g</u> _n − n_<sup><u>2</u></sup><sup>_>_0,andthus</sup> _M_ 1 _≥_ 0, since if this does not hold then the results of the theorems hold trivially.) With these values fixed, the three events are defined as follows: 

- Let _E_ max be the event that max _i∈_ [ _n_ ] _|Yi| < y∗_ . 

- Let _E_ mod be the event that mod(<sup>�</sup><sup>_n_</sup> _i_ =1<sup>_a_(</sup><sup>_Xi_)</sup><sup>_, M_)</sup><sup>_< M_1.</sup> 

- Let _E_ unif be the event that<sup>�</sup><sup>_n_</sup> _i_ =1<sup>1</sup><sup>_{_mod(</sup><sup>_a_(</sup><sup>_Xi_) +</sup><sup>_m, M_)</sup><sup>_< M−M_1</sup><sup>_}≥⌈_(1</sup><sup>_−_</sup> _α_ )( _n_ + 1) _⌉_ for all integers _m_ . 

13 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0014-00.png)


Figure 2: An illustration of the event _E_ mod, which is the event that mod(<sup>�</sup><sup>_n_</sup> _i_ =1<sup>_a_(</sup><sup>_Xi_)</sup><sup>_, M_)</sup><sup>_<_</sup> _M_ 1 for _M_ 1 _≈ αM_ . In the figure, the event _E_ mod holds if and only if the value mod(<sup>�</sup><sup>_n_</sup> _i_ =1<sup>_a_(</sup><sup>_Xi_)</sup><sup>_, M_)landsintheshadedregionofthe“clock”.</sup> 

Figures 2 and 3 illustrate the events _E_ mod and _E_ unif, respectively. 

The following result shows that, with probability at least _≈ α_ , all three events occur: 

iid **Lemma 2.** _Under the definitions and notation above, for_ ( _X_ 1 _, Y_ 1) _, . . . ,_ ( _Xn, Yn_ ) _∼ P , we have_ 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0014-05.png)


_and therefore,_ 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0014-07.png)


By choosing _M_ to be sufficiently large, then, we obtain 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0014-09.png)


Now it remains to be shown that, for both full conformal prediction and for jackknife+, we can find an algorithm _A_ such that, if the events _E_ max, _E_ mod, and _E_ unif all hold, then the training-conditional miscoverage rate _αP_ ( _Dn_ ) is close to 1. 

_Proof of Theorem 2._ For full conformal, we define a symmetric regression algorithm _A_ that maps a data set _{_ ( _x_ 1 _, y_ 1) _, . . . ,_ ( _xn_ +1 _, yn_ +1) _}_ to the fitted function 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0014-12.png)


14 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0015-00.png)


Figure 3: An illustration of the event _E_ unif, which is the event that mod( _a_ ( _Xi_ ) + _m, M_ ) _< M − M_ 1 holds for at least _⌈_ (1 _− α_ )( _n_ + 1) _⌉_ many training data points _i_ , for every integer _m_ . In the figure, the shaded region _{a ∈{_ 0 _, . . . , M −_ 1 _}_ : mod( _a_ + _m, M_ ) _< M − M_ 1 _}_ is shown for _m_ = 0 (left figure), _m_ = 1 (center figure), and _m_ = 2 (right figure). The event holds if and only if at least _⌈_ (1 _− α_ )( _n_ + 1) _⌉_ many training data points _i ∈_ [ _n_ ] have _a_ ( _Xi_ ) lying in the shaded region, for each integer _m_ (i.e., for each of the three displayed figures, as well as all other possible values of _m_ ). 

Below, we will show that, for any training data set _Dn_ , 

If _E_ max _∩E_ mod _∩E_ unif holds, then _C_<sup>�</sup> _n_ ( _Xn_ +1) _⊆_ ( _y∗, ∞_ ) almost surely over _Xn_ +1. (15) By definition of _y∗_ , we therefore have 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0015-04.png)


for any _Dn_ such that _E_ max _∩E_ mod _∩E_ unif holds. Combining this with the bound (14), log _n_ we have proved that P _P n {αP_ ( _Dn_ ) _≥_ 1 _− n_<sup>_−_2</sup> _} ≥ α −_ 6� _n_<sup>,asdesired.</sup> To complete the proof, we now verify (15). Condition on the training data _Dn_ , and assume _E_ max _∩E_ mod _∩E_ unif holds. First, by _E_ mod, we have 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0015-06.png)


for any value of _Xn_ +1, and therefore, for any _y ∈_ R, 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0015-08.png)


where as before, _µ_ �<sup>_y_</sup> _n_ +1<sup>=</sup><sup>_A_</sup> �( _X_ 1 _, Y_ 1) _, . . . ,_ ( _Xn, Yn_ ) _,_ ( _Xn_ +1 _, y_ )�. On the other hand, for any _i ∈_ [ _n_ ], define 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0015-10.png)


15 

where the last step holds since mod( _k, M_ ) = _M −_ 1 _−_ mod( _−k −_ 1 _, M_ ) for all integers _k_ . By the event _E_ unif (applied with _m_ = _−_<sup>�</sup><sup>_n_</sup> _j_ =1<sup>+1</sup><sup>_a_(</sup><sup>_Xj_)</sup><sup>_−_1),wesee</sup> �<sup>that</sup><sup>_Mi≥M_1for</sup> at least _⌈_ (1 _− α_ )( _n_ + 1) _⌉_ many _i ∈_ [ _n_ ]. Therefore, for all _y ∈_ R, _µ_<sup>_y_</sup> _n_ +1<sup>(</sup><sup>_Xi_)=0forat</sup> least _⌈_ (1 _− α_ )( _n_ + 1) _⌉_ many _i ∈_ [ _n_ ]. Next, by _E_ max, we have _|Yi| < y∗_ for all _i ∈_ [ _n_ ], and therefore, for all _y ∈_ R, _Ri_<sup>_y< y∗_foratleast</sup><sup>_⌈_(1</sup><sup>_−α_)(</sup><sup>_n_+ 1)</sup><sup>_⌉_many</sup><sup>_i ∈_[</sup><sup>_n_].</sup> 

Returning to the definition of full conformal prediction given in (5), we therefore have _Q_<sup>�</sup><sup>_y_</sup> _n_ +1<sup>_<y∗_.Therefore,</sup><sup>_y∈C_�</sup><sup>_n_(</sup><sup>_Xn_+1)canholdonlyif</sup><sup>_|y−µ_�</sup><sup>_y_</sup> _n_ +1<sup>(</sup><sup>_Xn_+1)</sup><sup>_|<y∗_,</sup> which implies _C_<sup>�</sup> _n_ ( _Xn_ +1) _⊆_ ( _y∗,_ 3 _y∗_ ) _⊆_ ( _y∗, ∞_ ). This verifies (15), and thus completes the proof of the theorem. 

_Proof of Theorem 3._ For jackknife+, we define a symmetric regression algorithm _A_ that maps a data set _{_ ( _x_ 1 _, y_ 1) _, . . . ,_ ( _xn−_ 1 _, yn−_ 1) _}_ to the fitted function 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0016-03.png)


As in the proof of Theorem 2, it is sufficient to verify that (15) again holds in this case. 

Condition on the training data _Dn_ , and assume _E_ max _∩E_ mod _∩E_ unif holds. First, by _E_ mod, for all _i ∈_ [ _n_ ], we have 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0016-06.png)


and therefore 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0016-08.png)


� By _E_ max, we have _|Yi| < y∗_ for all _i ∈_ [ _n_ ], and therefore, _Ri_ = _|Yi − µ_ [ _n_ ] _\{i}_ ( _Xi_ ) _| < y∗_ for all _i ∈_ [ _n_ ]. 

On the other hand, for any _i ∈_ [ _n_ ], define 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0016-11.png)


Exactly as in the proof of Theorem 2, by the event _E_ unif we see that _Mi ≥ M_ 1 for � at least _⌈_ (1 _− α_ )( _n_ + 1) _⌉_ many _i ∈_ [ _n_ ]. Therefore, _µ_ [ _n_ ] _\{i}_ ( _Xn_ +1) = 2 _y∗_ for at least _⌈_ (1 _− α_ )( _n_ + 1) _⌉_ many _i ∈_ [ _n_ ]. 

� Combining these calculations, we see that _µ_ [ _n_ ] _\{i}_ ( _Xn_ +1) _− Ri > y∗_ for at least _⌈_ (1 _− α_ )( _n_ + 1) _⌉_ many _i ∈_ [ _n_ ]. Thus, by definition of the jackknife+ predictive interval given in (7), we have _C_<sup>�</sup> _n_ ( _Xn_ +1) _⊆_ ( _y∗, ∞_ ). This verifies (15), and thus completes the proof of the theorem. 

Finally, we need to prove Lemma 2. 

16 

_Proof of Lemma 2._ First, since _y∗_ is chosen to be the (1 _− n_<sup>_−_2</sup> ) quantile of _|Y |_ under the distribution _P_ , we have 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0017-01.png)


and thus P _P n {E_ max _} ≥_ 1 _− n_<sup><u>1</u>asdesired.</sup> 

iid Next, since _a_ ( _Xi_ ) _∼_ Unif _{_ 0 _, . . . , M −_ 1 _}_ for _i ∈_ [ _n_ ], it follows immediately that mod( _a_ ( _X_ 1) + _· · ·_ + _a_ ( _Xn_ ) _, M_ ) _∼_ Unif _{_ 0 _, . . . , M −_ 1 _}_ also, and so by definition of _M_ 1 we have 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0017-04.png)


Finally, we turn to _E_ unif. This is the event that<sup>�</sup><sup>_n_</sup> _i_ =1<sup>1</sup><sup>_{_mod(</sup><sup>_a_(</sup><sup>_Xi_) +</sup><sup>_m, M_)</sup><sup>_< M−M_1</sup><sup>_} ≥_</sup> _⌈_ (1 _− α_ )( _n_ +1) _⌉_ for all integers _m_ , but by definition of the modulo function, it is equivalent to requiring that this bound holds only for all integers _m_ = 0 _, . . . , M −_ 1, i.e., 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0017-06.png)


iid iid Now let _U_ 1 _, . . . , Un ∼_ Unif[0 _,_ 1]. Then _⌊MUi⌋ ∼_ Unif _{_ 0 _, . . . , M −_ 1 _}_ , and so 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0017-08.png)


Next, suppose it holds that 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0017-10.png)


17 

Then, for each _m ∈{_ 0 _,_ 1 _, . . . , M − M_ 1 _−_ 1 _}_ , we have 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0018-01.png)


where the last step holds by definition of _M_ 1. Next, for each _m ∈{M −M_ 1 _, . . . , M −_ 1 _}_ , we have 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0018-03.png)


Therefore, returning to (16), we have 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0018-05.png)


where the lasts step holds by the Dvoretzky–Kiefer–Wolfowitz inequality. This completes the proof. 

18 

## **5 Empirical results** 

The theoretical results above suggest that we should be concerned about the training conditional coverage of the full conformal and jackknife+ prediction intervals. However, the algorithms used as counterexamples in the proof are extremely unrealistic. In particular, the constructions appearing in the proofs display an extremely high amount of instability, since the inclusion of a single training point can greatly impact the output of the regression function. 

Therefore, a natural question is how large the variability of _αP_ ( _Dn_ ) is in practice, particularly in unstable environments. In our simulation, we will examine the empirical performance of the training-conditional miscoverage rate _αP_ ( _Dn_ ) for the four distribution-free predictive inference tools studied in this work, for a linear regression task where high dimensionality may cause some instability in the regression algorithm.<sup>1</sup> 

### **5.1 Setting** 

We choose a target coverage rate of 90%, i.e., _α_ = 0 _._ 1, and will compare the performance of split conformal (with _n_ 0 = _n_ 1 = _n/_ 2), full conformal, jackknife+, and CV+ (with _K_ = 20 folds). 

We use sample size _n_ = 500 for the training set, and _n_ test = 1000 for the test set. For each trial, we generate i.i.d. data points ( _Xi, Yi_ ), _i_ = 1 _, . . . , n_ + _n_ test, from the following distribution: 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0019-06.png)


where _β_ = _√_ 10 _· U_ for a random unit vector _U_ drawn uniformly from the unit sphere in _X_ = R<sup>_d_</sup> . We repeat the experiment for each dimension _d_ = 125 _,_ 250 _,_ 500 _,_ 1000, with 200 independent trials for each dimension. 

Our algorithm _A_ is given by ridge regression with penalty parameter _λ_ = 0 _._ 0001, i.e., for any data set ( _x_ 1 _, y_ 1) _, . . . ,_ ( _xN , yN_ ), the fitted model � _µ_ = _A_ �( _x_ 1 _, y_ 1) _, . . . ,_ ( _xN , yN_ )� is given by 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0019-09.png)


Finally, we estimate the training-conditional miscoverage rate _αP_ ( _Dn_ ) for each of the four methods, by computing the empirical coverage over the _n_ test many test points: 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0019-11.png)


> 1Code to reproduce the experiment is available at `http://rinafb.github.io/code/training_ conditional.zip` . 

19 

**Instability of the algorithm** In this simulation, we apply the ridge regression algorithm to a training set where the _xi_ ’s are standard Gaussian, with a penalty parameter _λ ≈_ 0. This optimization problem is extremely poorly conditioned when the training set size is _≈ d_ , but is well-behaved if the number of training points is _either_ sufficiently large or sufficiently small relative to _d_ (see Hastie et al. [2022] for an analysis of “ridgeless” regression, i.e., taking _λ →_ 0, in the overparametrized setting). As a result, if the number of training points is _≈ d_ , the outcome of the algorithm may be highly unstable—the stability assumption (9) will not hold, and in general, predictions _µ_ �( _x_ ) will vary greatly with a new draw of the training set. However, instability will not occur if the training set size is substantially smaller than _d_ or larger than _d_ . 

For split conformal, since the model is trained on _n_ 0 = _n/_ 2 = 250 many data points, this instability will be high for _d_ = 250 (but not for _d_ = 125 _,_ 500 _,_ 1000). In contrast, when running full conformal or jackknife+ or CV+, the models are trained on _n_ +1 = 501 or _n−_ 1 = 499 or _n−n/K_ = 475 many data points, respectively. Therefore, for these three methods, we expect instability to be high for dimension _d_ = 500 (but not for _d_ = 125 _,_ 250 _,_ 1000). 

### **5.2 Results** 

The results of the simulations are displayed in Figure 4. For both split conformal and CV+, as the theory suggests, the training-conditional miscoverage rate _αP_ ( _Dn_ ) is consistently near or below the nominal level _α_ = 0 _._ 1. This is the case even for dimensions where the trained models for split conformal or for CV+ are likely to exhibit instability, as discussed above. Specifically, for split conformal, the _αP_ ( _Dn_ ) values concentrate around _α_ for each choice of dimension _d_ . For CV+, the same is true for dimensions _d_ = 125 _,_ 250 _,_ 1000 where the algorithm is fairly stable, while in the unstable regime _d_ = 500, CV+ appears to be highly conservative, with _αP_ ( _Dn_ ) values consistently much lower than _α_ . (The same outcome occurs if we repeat the experiment with dimension _d_ = 475, where instability for CV+ is highest, but for brevity we do not show results for this value of _d_ .) 

In contrast, for full conformal and for jackknife+, we see that at _d_ = 500 (where the trained models for these two methods are likely to be unstable), the training-conditional miscoverage rate _αP_ ( _Dn_ ) is highly variable—specifically, we see that _αP_ ( _Dn_ ) is substantially higher than nominal level _α_ = 0 _._ 1 for a large fraction of the trials. On the other hand, the training-conditional miscoverage rate _αP_ ( _Dn_ ) concentrates near _α_ = 0 _._ 1 for both methods, for all other values of _d_ . This is true both for a low-dimensional setting when _d_ = 125 _,_ 250 and a high-dimensional (i.e., overparameterized) setting when _d_ = 1000, suggesting that algorithmic stability may play a key role in understanding training-conditional coverage, as we discuss further below. 

20 


![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0021-00.png)



![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0021-01.png)



![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0021-02.png)



![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0021-03.png)



![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0021-04.png)



![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0021-05.png)



![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0021-06.png)



![](Training-conditional_coverage_for_distribution-free_predictive_inference_images/Training-conditional_coverage_for_distribution-free_predictive_inference.pdf-0021-07.png)


Figure 4: Plots of the estimated training-conditional miscoverage level _αP_ ( _Dn_ ) for 200 independent trials of the simulation, at each dimension _d_ = 125 _,_ 250 _,_ 500 _,_ 1000. The gray vertical lines indicates the target miscoverage level _α_ = 0 _._ 1. For each _d_ , the empirical distribution of _αP_ ( _Dn_ ) is displayed as a histogram on the left, and as an empirical CDF on the right. 

21 

## **6 Conclusion** 

In this paper, we examine one form of conditional validity for methods of distributionfree predictive inference: training-conditional validity. While this form of validity has been previously established for the split conformal prediction method, here we examined whether this property holds for other distribution-free prediction tools. We showed that training conditional coverage guarantees can be ensured for the CV+ method, but are not possible for either the full conformal or jackknife+ methods without additional assumptions. In addition, we demonstrated empirically that training-conditional miscoverage rates far above the nominal level _α_ can occur in realistic data sets with the latter two methods. 

### **6.1 The role of algorithmic stability** 

An interesting open question is whether there are any mild assumptions that would ensure training-conditional coverage for full conformal and/or for jackknife+. One possibility is to consider algorithmic stability assumptions such as (9). In particular, our empirical results show that poor training-conditional coverage for these two methods is observed exactly in those settings where the behavior of the regression algorithm _A_ is highly unstable (specifically, when _d ≈ n_ , in our linear regression simulation). This suggests that assuming stability of _A_ could potentially be sufficient to ensure trainingconditional coverage for these methods. We leave this open question for future work. 

### **Acknowledgements** 

R.F.B. was supported by the National Science Foundation via grants DMS-1654076 and DMS-2023109, and by the Office of Naval Research via grant N00014-20-1-2337. The authors are grateful to Ruiting Liang for feedback on an earlier draft of this paper. 

## **References** 

- Rina Foygel Barber, Emmanuel J Cand`es, Aaditya Ramdas, and Ryan J Tibshirani. The limits of distribution-free conditional predictive inference. _Information and Inference: A Journal of the IMA_ , 10(2):455–482, 2021a. 

- Rina Foygel Barber, Emmanuel J Cand`es, Aaditya Ramdas, and Ryan J Tibshirani. Predictive inference with the jackknife+. _The Annals of Statistics_ , 49(1):486–507, 2021b. 

- Stephen Bates, Anastasios Angelopoulos, Lihua Lei, Jitendra Malik, and Michael Jordan. Distribution-free, risk-controlling prediction sets. _Journal of the ACM (JACM)_ , 68(6):1–34, 2021. 

22 

- Wenyu Chen, Kelli-Jean Chun, and Rina Foygel Barber. Discretized conformal prediction for efficient distribution-free inference. _Stat_ , 7(1):e173, 2018. 

- Richard M Dudley and Rimas Norvaiˇsa. _Concrete functional calculus_ . Springer, 2011. 

- Trevor Hastie, Andrea Montanari, Saharon Rosset, and Ryan J Tibshirani. Surprises in high-dimensional ridgeless least squares interpolation. _The Annals of Statistics_ , 50(2):949–986, 2022. 

- Danijel Kivaranovic, Kory D Johnson, and Hannes Leeb. Adaptive, distribution-free prediction intervals for deep networks. In _International Conference on Artificial Intelligence and Statistics_ , pages 4346–4356. PMLR, 2020. 

- Jing Lei. Fast exact conformalization of the lasso using piecewise linear homotopy. _Biometrika_ , 106(4):749–764, 2019. 

- Jing Lei and Larry Wasserman. Distribution-free prediction bands for non-parametric regression. _Journal of the Royal Statistical Society: Series B (Statistical Methodology)_ , 76(1):71–96, 2014. 

- Jing Lei, Max G’Sell, Alessandro Rinaldo, Ryan J Tibshirani, and Larry Wasserman. Distribution-free predictive inference for regression. _Journal of the American Statistical Association_ , 113(523):1094–1111, 2018. 

- Tuve L¨ofstr¨om, Henrik Bostr¨om, Henrik Linusson, and Ulf Johansson. Bias reduction through conditional conformal prediction. _Intelligent Data Analysis_ , 19(6):1355– 1375, 2015. 

- Sangdon Park, Shuo Li, Insup Lee, and Osbert Bastani. Pac confidence predictions for deep neural network classifiers. _arXiv preprint arXiv:2011.00716_ , 2020. 

- Sangdon Park, Edgar Dobriban, Insup Lee, and Osbert Bastani. PAC prediction sets under covariate shift. _arXiv preprint arXiv:2106.09848_ , 2021. 

- Hongxiang Qiu, Edgar Dobriban, and Eric Tchetgen Tchetgen. Distribution-free prediction sets adaptive to unknown covariate shift. _arXiv preprint arXiv:2203.06126_ , 2022. 

- Ludger R¨uschendorf. Random variables with maximum sums. _Advances in Applied Probability_ , 14(3):623–632, 1982. 

- Lukas Steinberger and Hannes Leeb. Conditional predictive inference for highdimensional stable algorithms. _arXiv preprint arXiv:1809.01412_ , 2018. 

- Vladimir Vovk. Conditional validity of inductive conformal predictors. In _Asian conference on machine learning_ , pages 475–490. PMLR, 2012. 

23 

- Vladimir Vovk. Cross-conformal predictors. _Annals of Mathematics and Artificial Intelligence_ , 74(1):9–28, 2015. 

- Vladimir Vovk and Ruodu Wang. Combining p-values via averaging. _Biometrika_ , 107 (4):791–808, 2020. 

- Vladimir Vovk, Alexander Gammerman, and Glenn Shafer. _Algorithmic learning in a random world_ . Springer Science & Business Media, 2005. 

- Vladimir Vovk, Ilia Nouretdinov, Valery Manokhin, and Alexander Gammerman. Cross-conformal predictive distributions. In _Conformal and Probabilistic Prediction and Applications_ , pages 37–51. PMLR, 2018. 

- Abraham Wald. An extension of wilks’ method for setting tolerance limits. _The Annals of Mathematical Statistics_ , 14(1):45–55, 1943. 

- Samuel S Wilks. Determination of sample sizes for setting tolerance limits. _The Annals of Mathematical Statistics_ , 12(1):91–96, 1941. 

- Yachong Yang and Arun Kumar Kuchibhotla. Finite-sample efficient conformal prediction. _arXiv preprint arXiv:2104.13871_ , 2021. 

- Yachong Yang, Arun Kumar Kuchibhotla, and Eric Tchetgen Tchetgen. Doubly robust calibration of prediction sets under covariate shift. _arXiv preprint arXiv:2203.01761_ , 2022. 

24 

