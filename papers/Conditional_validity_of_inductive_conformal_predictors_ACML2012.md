Asian Conference on Machine Learning 

JMLR: Workshop and Conference Proceedings 25:475–490, 2012 

# **Conditional validity of inductive conformal predictors** 

### **Vladimir Vovk** 

v.vovk@rhul.ac.uk 

_Computer Learning Research Centre, Department of Computer Science, Royal Holloway, University of London, Egham, Surrey TW20 0EX, UK_ 

**Editors:** Steven C. H. Hoi and Wray Buntine 

## **Abstract** 

Conformal predictors are set predictors that are automatically valid in the sense of having coverage probability equal to or exceeding a given confidence level. Inductive conformal predictors are a computationally efficient version of conformal predictors satisfying the same property of validity. However, inductive conformal predictors have been only known to control unconditional coverage probability. This paper explores various versions of conditional validity and various ways to achieve them using inductive conformal predictors and their 

**Keywords:** Inductive conformal predictors, conditional validity, batch mode of learning, boosting, MART, spam detection 

## **1. Introduction** 

This paper continues study of the method of conformal prediction (Vovk et al. 2005, Chapter 2). An advantage of the method is that its predictions (which are set rather than point predictions) automatically satisfy a finite-sample property of validity. Its disadvantage is its relative computational inefficiency in many situations. A modification of conformal predictors, called inductive conformal predictors (Vovk et al. 2005, Section 4.1) aims at improving on the computational efficiency of conformal predictors. 

Most of the literature on conformal prediction studies the behavior of set predictors in the online mode of prediction, perhaps because the property of validity can be stated in an especially strong form in the on-line mode (Vovk et al. 2005, Proposition 2.3). The online mode, however, is much less popular in applications of machine learning than the batch mode of prediction. This paper follows the recent papers by Lei et al. (2011), Lei and Wasserman (2012), and Lei et al. (2012) studying properties of conformal prediction in the batch mode; we, however, concentrate on inductive conformal prediction (also considered in Lei et al. 2012). Its full version is published as Vovk (2012). 

We will usually be making the _assumption of randomness_ , which is standard in machine learning and nonparametric statistics: the available data is a sequence of _examples_ generated independently from the same probability distribution _P_ . (In some cases we will make the weaker assumption of exchangeability; for some of our results even weaker assumptions, such as conditional randomness or exchangeability, would have been sufficient.) Each example consists of two components: an _object_ and a _label_ . We are given a _training set_ of examples and a new object, and our goal is to predict the label of the new object. (If we have a whole 

_⃝_ c 2012 V. Vovk. 

Vovk 


![](Conditional_validity_of_inductive_conformal_predictors_ACML2012_images/Conditional_validity_of_inductive_conformal_predictors_ACML2012.pdf-0002-01.png)


Figure 1: Eight notions of conditional validity. The visible vertices of the cube are U (unconditional), T (training conditional), O (object conditional), L (label conditional), OL (example conditional), TL (training and label conditional), TO (training and object conditional). The invisible vertex is TOL (and corresponds to conditioning on everything). 

_test set_ of new objects, we can apply the procedure for predicting one new object to each of the objects in the test set.) 

The two desiderata for inductive conformal predictors are their validity and efficiency: validity requires that the coverage probability of the prediction sets should be at least equal to a preset confidence level, and efficiency requires that the prediction sets should be as small as possible. However, there is a wide variety of notions of validity, since the “coverage probability” is, in general, conditional probability. The simplest case is where we condition on the trivial _σ_ -algebra, i.e., the probability is in fact unconditional probability, but several other notions of conditional validity are depicted in Figure 1, where T refers to conditioning on the training set, O to conditioning on the test object, and L to conditioning on the test label. The arrows in Figure 1 lead from stronger to weaker notions of conditional validity; U is the sink and TOL is the source (the latter is not shown). 

Inductive conformal predictors will be defined in Section 2. They are automatically valid, in the sense of unconditional validity. It should be said that, in general, the unconditional error probability is easier to deal with than conditional error probabilities; e.g., the standard statistical methods of cross-validation and bootstrap provide decent estimates of the unconditional error probability but poor estimates for the training conditional error probability: see Hastie et al. (2009), Section 7.12. 

In Section 3 we explore training conditional validity of inductive conformal predictors. Our simple results (Propositions 2a and 2b) are of the PAC type, involving two parameters: the target training conditional coverage probability 1 _− ϵ_ and the probability 1 _− δ_ with which 1 _− ϵ_ is attained. They show that inductive conformal predictors achieve training conditional validity automatically (whereas for other notions of conditional validity the method has to be modified). We give self-contained proofs of Propositions 2a and 2b, but Appendix A of Vovk (2012) explains how they can be deduced from classical results about tolerance regions. 

In the following section, Section 4, we introduce a conditional version of inductive conformal predictors and explain, in particular, how it achieves label conditional validity. Label conditional validity is important as it allows the learner to control the set-prediction analogues of false positive and false negative rates. Section 5 is about object conditional validity 

476 

Conditional validity of inductive conformal predictors 

and its main result (a version of a lemma in Lei and Wasserman 2012) is negative: precise object conditional validity cannot be achieved in a useful way unless the test object has a positive probability. Whereas precise object conditional validity is usually not achievable, we should aim for approximate and asymptotic object conditional validity when given enough data (cf. Lei and Wasserman 2012). 

Section 6 reports on the results of empirical studies for the standard `Spambase` data set (see, e.g., Hastie et al. 2009, Chapter 1, Example 1, and Section 9.1.2). Section 7 discusses close connections between an important class of ICPs and ROC curves. Section 8 concludes. 

## **2. Inductive conformal predictors** 

The example space will be denoted **Z** ; it is the Cartesian product **X** _×_ **Y** of two measurable spaces, the object space and the label space. In other words, each example _z ∈_ **Z** consists of two components: _z_ = ( _x, y_ ), where _x ∈_ **X** is its object and _y ∈_ **Y** is its label. Two important special cases are the problem of _classification_ , where **Y** is a finite set (equipped with the discrete _σ_ -algebra), and the problem of _regression_ , where **Y** = R. 

Let ( _z_ 1 _, . . . , zl_ ) be the training set, _zi_ = ( _xi, yi_ ) _∈_ **Z** . We split it into two parts, the _proper training set_ ( _z_ 1 _, . . . , zm_ ) of size _m < l_ and the _calibration set_ of size _l − m_ . An _inductive conformity m-measure_ is a measurable function _A_ : **Z**<sup>_m_</sup> _×_ **Z** _→_ R; the idea behind the _conformity score A_ (( _z_ 1 _, . . . , zm_ ) _, z_ ) is that it should measure how well _z_ conforms to the proper training set. A standard choice is 


![](Conditional_validity_of_inductive_conformal_predictors_ACML2012_images/Conditional_validity_of_inductive_conformal_predictors_ACML2012.pdf-0003-06.png)


where _f_ : **X** _→_ **Y**<sup>_′_</sup> is a prediction rule found from ( _z_ 1 _, . . . , zm_ ) as the training set and ∆: **Y** _×_ **Y**<sup>_′_</sup> _→_ R is a measure of similarity between a label and a prediction. Allowing **Y**<sup>_′_</sup> to be different from **Y** (often **Y**<sup>_′_</sup> _⊃_ **Y** ) may be useful when the underlying prediction method gives additional information to the predicted label; e.g., the MART procedure used in Section 6 gives the logit of the predicted probability that the label is 1. 

The _inductive conformal predictor_ (ICP) corresponding to _A_ is defined as the set predictor 


![](Conditional_validity_of_inductive_conformal_predictors_ACML2012_images/Conditional_validity_of_inductive_conformal_predictors_ACML2012.pdf-0003-09.png)


where _ϵ ∈_ [0 _,_ 1] is the chosen _significance level_ (1 _− ϵ_ is known as the _confidence level_ ), the _p-values p_<sup>_y_</sup> , _y ∈_ **Y** , are defined by 


![](Conditional_validity_of_inductive_conformal_predictors_ACML2012_images/Conditional_validity_of_inductive_conformal_predictors_ACML2012.pdf-0003-11.png)


and 


![](Conditional_validity_of_inductive_conformal_predictors_ACML2012_images/Conditional_validity_of_inductive_conformal_predictors_ACML2012.pdf-0003-13.png)


are the conformity scores. Given the training set and a new object _x_ the ICP predicts its label _y_ ; it _makes an error_ if _y ∈/_ Γ<sup>_ϵ_</sup> ( _z_ 1 _, . . . , zl, x_ ). 

The random variables whose realizations are _xi_ , _yi_ , _zi_ , _z_ will be denoted by the corresponding upper case letters ( _Xi_ , _Yi_ , _Zi_ , _Z_ , respectively). The following proposition of validity is almost obvious. 

477 

Vovk 

**Proposition 1 (Vovk et al., 2005, Proposition 4.1)** _If random examples Zm_ +1 _, . . . , Zl, Zl_ +1 = ( _Xl_ +1 _, Yl_ +1) _are exchangeable (i.e., their distribution is invariant under permutations), the probability of error Yl_ +1 _∈/_ Γ<sup>_ϵ_</sup> ( _Z_ 1 _, . . . , Zl, Xl_ +1) _does not exceed ϵ for any ϵ and any inductive conformal predictor_ Γ _._ 

In practice the probability of error is usually close to _ϵ_ (as we will see in Section 6). 

## **3. Training conditional validity** 

As discussed in Section 1, the property of validity of inductive conformal predictors is unconditional. The property of conditional validity can be formalized using a PAC-type 2-parameter definition. It will be convenient to represent the ICP (2) in a slightly different form downplaying the structure ( _xi, yi_ ) of _zi_ . Define Γ<sup>_ϵ_</sup> ( _z_ 1 _, . . . , zl_ ) := _{_ ( _x, y_ ) _| p_<sup>_y_</sup> _> ϵ}_ , where _p_<sup>_y_</sup> is defined, as before, by (3) and (4) (therefore, _p_<sup>_y_</sup> depends implicitly on _x_ ). Proposition 1 can be restated by saying that the probability of error _Zl_ +1 _∈/_ Γ<sup>_ϵ_</sup> ( _Z_ 1 _, . . . , Zl_ ) does not exceed _ϵ_ provided _Z_ 1 _, . . . , Zl_ +1 are exchangeable. 

We consider a canonical probability space in which _Zi_ = ( _Xi, Yi_ ), _i_ = 1 _, . . . , l_ + 1, are i.i.d. random examples. A set predictor Γ (outputting a subset of **Z** given _l_ examples and measurable in a suitable sense) is ( _ϵ, δ_ ) _-valid_ if, for any probability distribution _P_ on **Z** , 


![](Conditional_validity_of_inductive_conformal_predictors_ACML2012_images/Conditional_validity_of_inductive_conformal_predictors_ACML2012.pdf-0004-06.png)


It is easy to see that ICPs satisfy this property for suitable _ϵ_ and _δ_ . 

**Proposition 2a** _Suppose ϵ, δ ∈_ [0 _,_ 1] _,_ 


![](Conditional_validity_of_inductive_conformal_predictors_ACML2012_images/Conditional_validity_of_inductive_conformal_predictors_ACML2012.pdf-0004-09.png)


_where n_ := _l − m is the size of the calibration set, and_ Γ _is an inductive conformal predictor. The set predictor_ Γ<sup>_ϵ_</sup> _is then_ ( _E, δ_ ) _-valid. Moreover, for any probability distribution P on_ **Z** _and any proper training set_ ( _z_ 1 _, . . . , zm_ ) _∈_ **Z**<sup>_m_</sup> _,_ 


![](Conditional_validity_of_inductive_conformal_predictors_ACML2012_images/Conditional_validity_of_inductive_conformal_predictors_ACML2012.pdf-0004-11.png)


This proposition gives the following recipe for constructing ( _ϵ, δ_ )-valid set predictors. The recipe only works if the training set is sufficiently large; in particular, its size _l_ should significantly exceed _N_ := ( _−_ ln _δ_ ) _/_ (2 _ϵ_<sup>2</sup> ) _._ Choose an ICP Γ with the size _n_ of the calibration set exceeding _N_ . Then the set predictor Γ<sup>_ϵ−√_</sup> ( _−_ ln _δ_ ) _/_ (2 _n_ ) will be ( _ϵ, δ_ )-valid. 

**Proof of Proposition 2a** Let _E ∈_ ( _ϵ,_ 1) (not necessarily satisfying (5)). Fix the proper training set ( _z_ 1 _, . . . , zm_ ). By (2) and (3), the set predictor Γ<sup>_ϵ_</sup> makes an error, _zl_ +1 _∈/_ Γ<sup>_ϵ_</sup> ( _z_ 1 _, . . . , zl_ ), if and only if the number of _i_ = _m_ + 1 _, . . . , l_ such that _αi ≤ α_<sup>_y_</sup> is at most _⌊ϵ_ ( _n_ +1) _−_ 1 _⌋_ ; in other words, if and only if _α_<sup>_y_</sup> _< α_ ( _k_ ), where _α_ ( _k_ ) is the _k_ th smallest _αi_ and _k_ := _⌊ϵ_ ( _n_ + 1) _−_ 1 _⌋_ + 1. Therefore, the _P_ -probability of the complement of Γ<sup>_ϵ_</sup> ( _z_ 1 _, . . . , zl_ ) is _P_ ( _A_ (( _z_ 1 _, . . . , zm_ ) _, Z_ ) _< α_ ( _k_ )), where _A_ is the inductive conformity _m_ -measure. Set 


![](Conditional_validity_of_inductive_conformal_predictors_ACML2012_images/Conditional_validity_of_inductive_conformal_predictors_ACML2012.pdf-0004-14.png)


478 

Conditional validity of inductive conformal predictors 

The _σ_ -additivity of measures implies that _E_<sup>_′_</sup> _≤ E ≤ E_<sup>_′′_</sup> , and _E_<sup>_′_</sup> = _E_ = _E_<sup>_′′_</sup> unless _α_<sup>_∗_</sup> is an atom of _A_ (( _z_ 1 _, . . . , zm_ ) _, Z_ ). Both when _E_<sup>_′_</sup> = _E_ and when _E_<sup>_′_</sup> _< E_ , the probability of error will exceed _E_ if an only if _α_ ( _k_ ) _> α_<sup>_∗_</sup> . In other words, if only if we have at most _k −_ 1 of the _αi_ below or equal to _α_<sup>_∗_</sup> . The probability that at most _k −_ 1 = _⌊ϵ_ ( _n_ + 1) _−_ 1 _⌋_ values of the _αi_ are below or equal to _α_<sup>_∗_</sup> equals P( _Bn_<sup>_′′≤⌊ϵ_(</sup><sup>_n_+ 1)</sup><sup>_−_1</sup><sup>_⌋_)</sup><sup>_≤_P(</sup><sup>_Bn≤⌊ϵ_(</sup><sup>_n_+ 1)</sup><sup>_−_1</sup><sup>_⌋_),where</sup> _Bn_<sup>_′′∼_bin</sup><sup>_n,E′′_,</sup><sup>_Bn∼_bin</sup><sup>_n,E_,andbin</sup><sup>_n,p_standsforthebinomialdistributionwith</sup><sup>_n_trials</sup> and probability of success _p_ . By Hoeffding’s inequality (see, e.g., Vovk et al. 2005, p. 287), the probability of error will exceed _E_ with probability at most 


![](Conditional_validity_of_inductive_conformal_predictors_ACML2012_images/Conditional_validity_of_inductive_conformal_predictors_ACML2012.pdf-0005-02.png)


Solving _e_<sup>_−_2(</sup><sup>_E−ϵ_)2</sup><sup>_n_</sup> = _δ_ we obtain that Γ<sup>_ϵ_</sup> is ( _E, δ_ )-valid whenever (5) is satisfied. 

The inequality (5) in Proposition 2a is simple but somewhat crude as its derivation uses Hoeffding’s inequality. The following proposition is the more precise version of Proposition 2a that stops short of that last step. 

**Proposition 2b** _Let ϵ, δ, E ∈_ [0 _,_ 1] _. If_ Γ _is an inductive conformal predictor, the set predictor_ Γ<sup>_ϵ_</sup> _is_ ( _E, δ_ ) _-valid provided_ 


![](Conditional_validity_of_inductive_conformal_predictors_ACML2012_images/Conditional_validity_of_inductive_conformal_predictors_ACML2012.pdf-0005-06.png)


_where n_ := _l − m is the size of the calibration set and_ bin _n,E is the cumulative binomial distribution function with n trials and probability of success E. If the random variable A_ (( _z_ 1 _, . . . , zm_ ) _, Z_ ) _is continuous,_ Γ<sup>_ϵ_</sup> _is_ ( _E, δ_ ) _-valid if and only if (7) holds._ 

**Proof** See the left-most expression in (3) and remember that _E_<sup>_′′_</sup> = _E_ unless _α_<sup>_∗_</sup> is an atom of _A_ (( _z_ 1 _, . . . , zm_ ) _, Z_ ). 

## **4. Conditional inductive conformal predictors** 

The motivation behind conditional inductive conformal predictors is that ICPs do not always achieve the required probability _ϵ_ of error _Yl_ +1 _∈/_ Γ<sup>_ϵ_</sup> ( _Z_ 1 _, . . . , Zl, Xl_ +1) conditional on ( _Xl_ +1 _, Yl_ +1) _∈ E_ for important sets _E ⊆_ **Z** . This is often undesirable. If, e.g., our set predictor is valid at the significance level 5% but makes an error with probability 10% for men and 0% for women, both men and women can be unhappy with calling 5% the probability of error. Moreover, in many problems we might want different significance levels for different regions of the example space: e.g., in the problem of spam detection (considered in Section 6) classifying spam as email usually makes much less harm than classifying email as spam. 

An _inductive m-taxonomy_ is a measurable function _K_ : **Z**<sup>_m_</sup> _×_ **Z** _→_ **K** , where **K** is a measurable space. Usually the _category K_ (( _z_ 1 _, . . . , zm_ ) _, z_ ) of an example _z_ is a kind of classification of _z_ , which may depend on the proper training set ( _z_ 1 _, . . . , zm_ ). 

479 

Vovk 

The _conditional inductive conformal predictor_ (conditional ICP) corresponding to _K_ and an inductive conformity _m_ -measure _A_ is defined as the set predictor (2), where the p-values _p_<sup>_y_</sup> are now defined by 


![](Conditional_validity_of_inductive_conformal_predictors_ACML2012_images/Conditional_validity_of_inductive_conformal_predictors_ACML2012.pdf-0006-02.png)


the categories _κ_ are defined by 


![](Conditional_validity_of_inductive_conformal_predictors_ACML2012_images/Conditional_validity_of_inductive_conformal_predictors_ACML2012.pdf-0006-04.png)


and the conformity scores _α_ are defined as before by (4). A _label conditional ICP_ is a conditional ICP with the inductive _m_ -taxonomy _K_ ( _·,_ ( _x, y_ )) := _y_ . 

The following proposition is the conditional analogue of Proposition 1; in particular, it shows that in classification problems label conditional ICPs achieve label conditional validity. 

**Proposition 3** _If random examples Zm_ +1 _, . . . , Zl, Zl_ +1 = ( _Xl_ +1 _, Yl_ +1) _are exchangeable, the probability of error Yl_ +1 _∈/_ Γ<sup>_ϵ_</sup> ( _Z_ 1 _, . . . , Zl, Xl_ +1) _given the category K_ (( _Z_ 1 _, . . . , Zm_ ) _, Zl_ +1) _of Zl_ +1 _does not exceed ϵ for any ϵ and any conditional inductive conformal predictor_ Γ _corresponding to K._ 

## **5. Object conditional validity** 

In this section we prove a negative result (a version of Lemma 1 in Lei and Wasserman 2012) which says that the requirement of precise object conditional validity cannot be satisfied in a non-trivial way for rich object spaces (such as R). If _P_ is a probability distribution on **Z** , we let _P_ **X** stand for its marginal distribution on **X** : _P_ **X** ( _A_ ) := _P_ ( _A ×_ **Y** ). Let us say that a set predictor Γ _has_ 1 _− ϵ object conditional validity_ , where _ϵ ∈_ (0 _,_ 1), if, for all probability distributions _P_ on **Z** and _P_ **X** -almost all _x ∈_ **X** , 


![](Conditional_validity_of_inductive_conformal_predictors_ACML2012_images/Conditional_validity_of_inductive_conformal_predictors_ACML2012.pdf-0006-10.png)


The Lebesgue measure on R will be denoted Λ. If _Q_ is a probability distribution, we say that a property _F_ holds for _Q-almost all_ elements of a set _E_ if _Q_ ( _E \ F_ ) = 0; a _Q-non-atom_ is an element _x_ such that _Q_ ( _{x}_ ) = 0. 

**Proposition 4** _Suppose_ **X** _is a separable metric space equipped with the Borel σ-algebra. Let ϵ ∈_ (0 _,_ 1) _. Suppose that a set predictor_ Γ _has_ 1 _− ϵ object conditional validity. In the case of regression, we have, for all P and for P_ **X** _-almost all P_ **X** _-non-atoms x ∈_ **X** _,_ 


![](Conditional_validity_of_inductive_conformal_predictors_ACML2012_images/Conditional_validity_of_inductive_conformal_predictors_ACML2012.pdf-0006-13.png)


_In the case of classification, we have, for all P , all y ∈_ **Y** _, and P_ **X** _-almost all P_ **X** _-nonatoms x,_ 


![](Conditional_validity_of_inductive_conformal_predictors_ACML2012_images/Conditional_validity_of_inductive_conformal_predictors_ACML2012.pdf-0006-15.png)


480 

Conditional validity of inductive conformal predictors 

We are mainly interested in the case of a small _ϵ_ (corresponding to high confidence), and in this case (10) implies that, in the case of regression, prediction intervals (i.e., the convex hulls of prediction sets) can be expected to be infinitely long unless the new object is an atom. In the case of classification, (11) says that each particular _y ∈_ **Y** is likely to be included in the prediction set, and so the prediction set is likely to be large. In particular, (11) implies that the expected size of the prediction set is a least (1 _− ϵ_ ) _|_ **Y** _|_ . 

Of course, the condition that _x_ be a non-atom is essential: if _P_ **X** ( _{x}_ ) _>_ 0, an inductive conformal predictor that ignores all examples with objects different from _x_ will have 1 _− ϵ_ object conditional validity and can give narrow predictions if the training set is big enough to contain many examples with _x_ as their object. 

**Proof of Proposition 4** The proof will be based on the ideas of Lei and Wasserman (2012, the proof of Lemma 1). 

Suppose (10) does not hold on a measurable set _E_ of _P_ **X** -non-atoms _x ∈_ **X** such that _P_ **X** ( _E_ ) _>_ 0. Shrink _E_ in such a way that _P_ **X** ( _E_ ) _>_ 0 still holds but there exists _δ >_ 0 and _C >_ 0 such that, for each _x ∈ E_ , 


![](Conditional_validity_of_inductive_conformal_predictors_ACML2012_images/Conditional_validity_of_inductive_conformal_predictors_ACML2012.pdf-0007-05.png)


Let _V_ be the total variation distance between probability measures, _V_ ( _P, Q_ ) := sup _A |P_ ( _A_ ) _− Q_ ( _A_ ) _|_ ; we then have 


![](Conditional_validity_of_inductive_conformal_predictors_ACML2012_images/Conditional_validity_of_inductive_conformal_predictors_ACML2012.pdf-0007-07.png)


(this follows from the connection of _V_ with the Hellinger distance: see, e.g., Tsybakov 2010, Section 2.4). Shrink _E_ further so that _P_ **X** ( _E_ ) _>_ 0 still holds but 


![](Conditional_validity_of_inductive_conformal_predictors_ACML2012_images/Conditional_validity_of_inductive_conformal_predictors_ACML2012.pdf-0007-09.png)


(This can be done under our assumption that **X** is a separable metric space: we can take the intersection of _E_ and some neighbourhood of any element of **X** for which all such intersections have a positive _P_ **X** -probability.) Define another probability distribution _Q_ on **Z** by the requirements that _Q_ ( _A × B_ ) = _P_ ( _A × B_ ) for all measurable _A ⊆_ ( **X** _\ E_ ), _B ⊆_ R and _Q_ ( _A × B_ ) = _P_ **X** ( _A_ ) _× U_ ( _B_ ) for all measurable _A ⊆ E_ , _B ⊆_ R, where _U_ is the uniform probability distribution on the interval [ _−DC, DC_ ] and _D >_ 0 will be chosen below. Since _V_ ( _P, Q_ ) _≤ P_ **X** ( _E_ ), we have _V_ ( _P_<sup>_l_</sup> _, Q_<sup>_l_</sup> ) _≤ δ/_ 2; therefore, by (12), 


![](Conditional_validity_of_inductive_conformal_predictors_ACML2012_images/Conditional_validity_of_inductive_conformal_predictors_ACML2012.pdf-0007-11.png)


for each _x ∈ E_ . The last inequality implies, by Fubini’s theorem, 


![](Conditional_validity_of_inductive_conformal_predictors_ACML2012_images/Conditional_validity_of_inductive_conformal_predictors_ACML2012.pdf-0007-13.png)


where _Q_ **X** ( _E_ ) = _P_ **X** ( _E_ ) _>_ 0 is the marginal _Q_ -probability of _E_ . When _D_ = _D_ ( _δQ_ **X** ( _E_ ) _, C_ ) is sufficiently large this in turn implies 


![](Conditional_validity_of_inductive_conformal_predictors_ACML2012_images/Conditional_validity_of_inductive_conformal_predictors_ACML2012.pdf-0007-15.png)


481 

Vovk 

However, the last inequality contradicts 


![](Conditional_validity_of_inductive_conformal_predictors_ACML2012_images/Conditional_validity_of_inductive_conformal_predictors_ACML2012.pdf-0008-02.png)


which follows from Γ having 1 _−ϵ_ object conditional validity and the definition of conditional probability. 

It remains to consider the case of classification. Suppose (11) does not hold on a measurable set _E_ of _P_ **X** -non-atoms _x ∈_ **X** such that _P_ **X** ( _E_ ) _>_ 0. Shrink _E_ in such a way that _P_ **X** ( _E_ ) _>_ 0 still holds but there exists _δ >_ 0 such that, for each _x ∈ E_ , 


![](Conditional_validity_of_inductive_conformal_predictors_ACML2012_images/Conditional_validity_of_inductive_conformal_predictors_ACML2012.pdf-0008-05.png)


Without loss of generality we further assume that (13) also holds. Define a probability distribution _Q_ on **Z** by the requirements that _Q_ ( _A × B_ ) = _P_ ( _A × B_ ) for all measurable _A ⊆_ ( **X** _\ E_ ) and all _B ⊆_ **Y** and that _Q_ ( _A × {y}_ ) = _P_ **X** ( _A_ ) for all measurable _A ⊆ E_ (i.e., modify _P_ setting the conditional distribution of _Y_ given _X ∈ E_ to the unit mass concentrated at _y_ ). Then for each _x ∈ E_ we have 


![](Conditional_validity_of_inductive_conformal_predictors_ACML2012_images/Conditional_validity_of_inductive_conformal_predictors_ACML2012.pdf-0008-07.png)


which implies 


![](Conditional_validity_of_inductive_conformal_predictors_ACML2012_images/Conditional_validity_of_inductive_conformal_predictors_ACML2012.pdf-0008-09.png)


The last inequality contradicts Γ having 1 _− ϵ_ object conditional validity. 

Proposition 4 can be extended to randomized set predictors Γ (in which case _P_<sup>_l_</sup> and _P_<sup>_l_+1</sup> in expressions such as (9) and (10) should be replaced by the probability distribution comprising both _P_ and the internal coin tossing of Γ). This clarifies the provenance of _ϵ_ in (10) and (11): _ϵ_ cannot be replaced by a smaller constant since the set predictor predicting **Y** with probability 1 _− ϵ_ and _∅_ with probability _ϵ_ has 1 _− ϵ_ object conditional validity. 

Proposition 4 does not prevent the existence of efficient set predictors that are conditionally valid in an asymptotic sense; indeed, the paper by Lei and Wasserman (2012) is devoted to constructing asymptotically efficient and asymptotically conditionally valid set predictors in the case of regression. 

## **6. Experiments** 

This section describes some simple experiments on the well-known `Spambase` data set contributed by George Forman to the UCI Machine Learning Repository (Frank and Asuncion, 2010). Its overall size is 4601 examples and it contains examples of two classes: `email` (also written as 0) and `spam` (also written as 1). Hastie et al. (2009) report results of several machine-learning algorithms on this data set split randomly into a training set of size 3065 and test set of size 1536. The best result is achieved by MART (multiple additive regression tree; 4 _._ 5% error rate according to the second edition of Hastie et al. 2009). 

482 

Conditional validity of inductive conformal predictors 

We randomly permute the data set and divide it into 2602 examples for the proper training set, 999 for the calibration set, and 1000 for the test set. We consider the ICP whose conformity measure is defined by (1) where _f_ is output by MART and 


![](Conditional_validity_of_inductive_conformal_predictors_ACML2012_images/Conditional_validity_of_inductive_conformal_predictors_ACML2012.pdf-0009-02.png)


MART’s output _f_ ( _x_ ) models the log-odds of `spam` vs `email` , 


![](Conditional_validity_of_inductive_conformal_predictors_ACML2012_images/Conditional_validity_of_inductive_conformal_predictors_ACML2012.pdf-0009-04.png)


which makes the interpretation of (14) as conformity score very natural. 

The upper left plot in Figure 2 is the scatter plot of the pairs ( _p_<sup>email</sup> _, p_<sup>spam</sup> ) produced by the ICP for all examples in the test set. Email is shown as green noughts and spam as red crosses (and it is noticeable that the noughts were drawn after the crosses). The other two plots in the upper row are for email and spam separately. Ideally, email should be close to the horizontal axis and spam to the vertical axis; we can see that this is often true, with a few exceptions. The picture for the label conditional ICP looks almost identical: see the lower row of Figure 2. 

Table 1 gives some statistics for the numbers of errors, multiple, and empty set predictions in the case of the (unconditional) ICP Γ<sup>5%</sup> at significance level 5% (we obtain different numbers not only because of different splits but also because MART is randomized; the columns of the table correspond to the pseudorandom number generator seeds 0, 1, 2, etc.). The table demonstrates the validity, (lack of) conditional validity, and efficiency of the algorithm (the latter is of course inherited from the efficiency of MART). We give two kinds of conditional figures: the percentages of errors, multiple, and empty predictions for different labels and for two different kinds of objects. The two kinds of objects are obtained by splitting the object space **X** by the value of an attribute that we denote $: it shows the percentage of the character $ in the text of the message. The condition $ _<_ 5 _._ 55% was the root of the decision tree chosen both by Hastie et al. (2009, Section 9.2.5), who use all attributes in their analysis, and by Maindonald and Braun (2007, Chapter 11), who use 6 attributes chosen by them manually. (Both books use the `rpart` R package for decision trees.) 

Notice that the numbers of errors, multiple predictions, and empty predictions tend to be greater for spam than for email. Somewhat counter-intuitively, they also tend to be greater for “email-like” objects containing few $ characters than for “spam-like” objects. The percentage of multiple and empty predictions is relatively small since the error rate of the underlying predictor happens to be close to our significance level of 5%. 

In practice, using a fixed significance level (such as the standard 5%) is not a good idea; we should at least pay attention to what happens at several significance levels. However, experimenting with prediction sets at a fixed significance level facilitates a comparison with theoretical results. 

Table 2 gives similar statistics in the case of the label conditional ICP. The error rates are now about equal for email and spam, as expected. We refrain from giving similar predictable results for “object conditional” ICP with $ _<_ 5 _._ 55% and $ _>_ 5 _._ 55% as categories. 

483 

Vovk 


![](Conditional_validity_of_inductive_conformal_predictors_ACML2012_images/Conditional_validity_of_inductive_conformal_predictors_ACML2012.pdf-0010-01.png)


Figure 2: Scatter plots of the pairs ( _p_<sup>email</sup> _, p_<sup>spam</sup> ) for all examples in the test set (left plots), for email only (middle), and for spam only (right). The three upper plots are for the ICP and the three lower ones are for the label conditional ICP. 

Figure 3 gives the calibration plots of the ICP for the test set. It shows approximate validity even for email and spam separately, except for the all-important lower-left corners. The latter are shown separately in Figure 4, where the lack of conditional validity becomes evident; cf. Figure 5 for the label conditional ICP. 

From the numbers given in the “errors overall” row of Table 1 we can extract the corresponding confidence intervals for the probability of error conditional on the training set and MART’s internal coin tosses; these are shown in Figure 6. It can be seen that training conditional validity is not grossly violated. (Notice that the 8 training sets used for producing this figure are not completely independent. Besides, the assumption of randomness might not be completely satisfied: permuting the data set ensures exchangeability but not necessarily randomness.) It is instructive to compare Figure 6 with the “theoretical” Figure 7 obtained from Propositions 2b (the thick blue line) and 2a (the thin red line). The dotted green line corresponds to the significance level 5%, and the black dot roughly corresponds to the maximal expected probability of error among 8 randomly chosen training sets. (It might appear that there is a discrepancy between Figures 6 and 7, but choosing different seeds usually leads to smaller numbers of errors than in Figure 6.) 

484 

Conditional validity of inductive conformal predictors 

|RNG seed|0|1|2|3|4|5|6|7|Average|
|---|---|---|---|---|---|---|---|---|---|
|errors overall|4.1%|6.9%|4.6%|5.4%|5.3%|6.1%|7.7%|5.9%|5.75%|
|for email|2.44%|4.61%|2.26%|3.10%|4.49%|3.98%|5.02%|3.22%|3.64%|
|for spam|6.77%|10.43%|8.42%|9.02%|6.53%|9.32%|11.69%|10.29%|9.06%|
|for $_<_5_._55%|4.36%|7.91%|5.15%|6.21%|6.27%|7.89%|8.79%|7.04%|6.70%|
|for $_>_5_._55%|3.29%|4.12%|2.69%|2.64%|2.40%|1.13%|4.42%|2.15%|2.86%|
|multiple overall|2.7%|0%|0.1%|0%|0%|0.5%|0%|0%|0.41%|
|for email|2.11%|0%|0.16%|0%|0%|0.33%|0%|0%|0.33%|
|for spam|3.65%|0%|0%|0%|0%|0.76%|0%|0%|0.55%|
|for $_<_5_._55%|3.04%|0%|0.13%|0%|0%|0.68%|0%|0%|0.48%|
|for $_>_5_._55%|1.65%|0%|0%|0%|0%|0%|0%|0%|0.21%|
|empty overall|0%|2.7%|0%|1.2%|0.8%|0%|2.5%|0.4%|0.95%|
|for email|0%|1.48%|0%|0.65%|0.83%|0%|1.51%|0.64%|0.64%|
|for spam|0%|4.58%|0%|2.06%|0.75%|0%|3.98%|0%|1.42%|
|for $_<_5_._55%|0%|3.14%|0%|1.55%|0.80%|0%|3.06%|0.52%|1.13%|
|for $_>_5_._55%|0%|1.50%|0%|0%|0.80%|0%|0.80%|0%|0.39%|



Table 1: Percentage of errors, multiple predictions, and empty predictions on the full test set and separately on email and spam. The results are given for various values of the seed for the R (pseudo)random number generator (RNG); column “Average” gives the average values for all 8 seeds 0–7. 

|RNG seed|0|1|2|3|4|5|6|7|Average|
|---|---|---|---|---|---|---|---|---|---|
|errors overall|3.4%|6.0%|3.8%|4.8%|5.7%|5.3%|6.5%|5.4%|5.11%|
|for email|3.73%|6.92%|3.87%|4.90%|6.64%|4.98%|5.85%|3.86%|5.10%|
|for spam|2.86%|4.58%|3.68%|4.64%|4.27%|5.79%|7.46%|7.92%|5.15%|
|multiple overall|4.2%|0%|4.0%|0%|0%|0.5%|0%|0.5%|1.15%|
|for email|3.90%|0%|5.48%|0%|0%|0.66%|0%|0.48%|1.32%|
|for spam|4.69%|0%|1.58%|0%|0%|0.25%|0%|0.53%|0.88%|
|empty overall|0%|1.0%|0%|0%|0.6%|0%|1.0%|0%|0.33%|
|for email|0%|1.48%|0%|0%|0.83%|0%|0.67%|0%|0.37%|
|for spam|0%|0.25%|0%|0%|0.25%|0%|1.49%|0%|0.25%|



Table 2: The analogue of a subset of Table 1 in the case of the label conditional ICP. 

## **7. ICPs and ROC curves** 

This section will discuss a close connection between an important class of ICPs (“probabilitytype” label conditional ICPs) and ROC curves. (For a previous study of connection between conformal prediction and ROC curves, see Vanderlooy and Sprinkhuizen-Kuyper 2007.) Let us say that an ICP or a label conditional ICP is _probability-type_ if its inductive conformity measure is defined by (1) where _f_ takes values in R and ∆is defined by (14). 

The reader might have noticed that the two leftmost plots in Figure 2 look similar to a ROC curve. The following proposition will show that this is not coincidental in the case of the lower left one. However, before we state it, we need a few definitions. We will now consider a general binary classification problem and will denote the labels as 0 and 1. For 

485 

Vovk 


![](Conditional_validity_of_inductive_conformal_predictors_ACML2012_images/Conditional_validity_of_inductive_conformal_predictors_ACML2012.pdf-0012-01.png)


Figure 3: The calibration plot for the test set overall, the email in the test set, and the spam in the test set (for the first 8 seeds, 0–7). 


![](Conditional_validity_of_inductive_conformal_predictors_ACML2012_images/Conditional_validity_of_inductive_conformal_predictors_ACML2012.pdf-0012-03.png)


Figure 4: The lower left corners of the plots in Figure 3. 

a threshold _c ∈_ R, the _type I error on the calibration set_ is 


![](Conditional_validity_of_inductive_conformal_predictors_ACML2012_images/Conditional_validity_of_inductive_conformal_predictors_ACML2012.pdf-0012-06.png)



![](Conditional_validity_of_inductive_conformal_predictors_ACML2012_images/Conditional_validity_of_inductive_conformal_predictors_ACML2012.pdf-0012-07.png)


Figure 5: The analogue of Figure 4 for the label conditional ICP. 

486 

Conditional validity of inductive conformal predictors 


![](Conditional_validity_of_inductive_conformal_predictors_ACML2012_images/Conditional_validity_of_inductive_conformal_predictors_ACML2012.pdf-0013-01.png)


Figure 6: Confidence intervals for training conditional error probabilities: 95% in black (thin lines) and 80% in blue (thick lines). The 5% significance level is shown as the horizontal red line. 


![](Conditional_validity_of_inductive_conformal_predictors_ACML2012_images/Conditional_validity_of_inductive_conformal_predictors_ACML2012.pdf-0013-03.png)


Figure 7: The probability of error _E_ vs _δ_ from Propositions 2b (the thick blue line) and 2a (the thin red line), where _ϵ_ = 0 _._ 05 and _n_ = 999. 

and the _type II error on the calibration set_ is 


![](Conditional_validity_of_inductive_conformal_predictors_ACML2012_images/Conditional_validity_of_inductive_conformal_predictors_ACML2012.pdf-0013-06.png)


(with 0 _/_ 0 set, e.g., to 1 _/_ 2). Intuitively, these are the error rates for the classifier that predicts 1 when _f_ ( _x_ ) _> c_ and predicts 0 when _f_ ( _x_ ) _< c_ ; our definition is conservative in that it counts the prediction as error whenever _f_ ( _x_ ) = _c_ . The _ROC curve_ is the parametric curve 


![](Conditional_validity_of_inductive_conformal_predictors_ACML2012_images/Conditional_validity_of_inductive_conformal_predictors_ACML2012.pdf-0013-08.png)


(Our version of ROC curves is the original version reflected in the line _y_ = 1 _/_ 2; in our sloppy terminology we follow Hastie et al. 2009, whose version is the original one reflected in the line _x_ = 1 _/_ 2, and many other books and papers.) 

487 

Vovk 

**Proposition 5** _In the case of a probability-type label conditional ICP, for any object x ∈_ **X** _, the distance between the pair_ ( _p_<sup>0</sup> _, p_<sup>1</sup> ) _(see (8)) and the ROC curve is at most_ 


![](Conditional_validity_of_inductive_conformal_predictors_ACML2012_images/Conditional_validity_of_inductive_conformal_predictors_ACML2012.pdf-0014-02.png)


_where n_<sup>_y_</sup> _is the number of examples in the calibration set labelled as y._ 

**Proof** Let _c_ := _f_ ( _x_ ). Then we have 


![](Conditional_validity_of_inductive_conformal_predictors_ACML2012_images/Conditional_validity_of_inductive_conformal_predictors_ACML2012.pdf-0014-05.png)


where _n_<sup>0</sup> _≥_<sup>isthenumberofexamples(</sup><sup>_xi, yi_)inthecalibrationsetsuchthat</sup><sup>_yi_=0and</sup> _f_ ( _xi_ ) _≥ c_ and _n_<sup>1</sup> _≤_<sup>isthenumberofexamplesinthecalibrationsetsuchthat</sup><sup>_yi_=1</sup> and _f_ ( _xi_ ) _≤ c_ . It remains to notice that the point � _n_<sup>0</sup> _≥_<sup>_/n_0</sup><sup>_, n_1</sup> _≤_<sup>_/n_1�</sup> belongs to the ROC curve: the horizontal (resp. vertical) distance between this point and (19) does not exceed 1 _/_ ( _n_<sup>0</sup> +1) (resp. 1 _/_ ( _n_<sup>1</sup> +1)), and the overall Euclidean distance does not exceed (18). 

So far we have discussed the _empirical ROC curve_ : (15) and (16) are the empirical probabilities of errors of the two types on the calibration set. It corresponds to the estimate _k/n_ of the parameter of the binomial distribution based on observing _k_ successes out of _n_ . The minimax estimate is ( _k_ + 1 _/_ 2) _/_ ( _n_ + 1), and the corresponding ROC curve (17) where _α_ ( _c_ ) and _β_ ( _c_ ) are defined by (15) and (16) with the numerators increased by<sup><u>1</u></sup> 2<sup>andthe</sup> denominators increased by 1 will be called the _minimax ROC curve_ . Notice that for the minimax ROC curve we can put a coefficient of<sup><u>1</u></sup> 2<sup>infrontof(18).Similarly,whenusing</sup> the Laplace estimate ( _k_ + 1) _/_ ( _n_ + 2), we obtain the _Laplace ROC curve_ . See Figure 8 for the lower left corner of the lower left plot of Figure 2 with different ROC curves added to it. 

In conclusion of our study of the `Spambase` data set, we will discuss the asymmetry of the two kinds of error in spam detection: classifying email as `spam` is much more harmful than letting occasional spam in. A reasonable approach is to start from a small number _ϵ >_ 0, the maximum tolerable percentage of email classified as `spam` , and then to try to minimize the percentage of spam classified as `email` under this constraint. The standard way of doing this is to classify a message _x_ as `spam` if and only if _f_ ( _x_ ) _≥ c_ , where _c_ is the point on the ROC curve corresponding to the type I error _ϵ_ . It is not clear what this means precisely, since we only have access to an estimate of the true ROC curve (and even on the true ROC curve such a point might not exist). But roughly, this means classifying _x_ as `spam` if _f_ ( _x_ ) exceeds the _k_ th largest value in the set _{αi | i ∈{m_ + 1 _, . . . , l}_ & _yi_ = `email` _}_ , where _k_ is close to _ϵn_<sup>0</sup> and _n_<sup>0</sup> is the size of this set (i.e., the number of email in the calibration, or validation, set). To make this more precise, we can use the “one-sided label conditional ICP” classifying _x_ as `spam` if and only if _p_<sup>0</sup> _≤ ϵ_ for _x_ . According to (19), this means that we classify _x_ as `spam` if and only if _f_ ( _x_ ) exceeds the _k_ th largest value in the set _{αi | i ∈{m_ + 1 _, . . . , l}_ & _yi_ = `email` _}_ , where _k_ := _⌊ϵ_ ( _n_<sup>0</sup> + 1) _⌋_ . The advantage of this version of the standard method is that it guarantees that the probability of mistaking email 

488 

Conditional validity of inductive conformal predictors 


![](Conditional_validity_of_inductive_conformal_predictors_ACML2012_images/Conditional_validity_of_inductive_conformal_predictors_ACML2012.pdf-0015-01.png)


Figure 8: The lower left corner of the lower left plot of Figure 2 with the empirical (solid blue), minimax (dashed blue), and Laplace (dotted blue) ROC curves. 

for spam is at most _ϵ_ (see Proposition 3) and also enjoys the training conditional version of this property given by Proposition 2a (more accurately, its version for label conditional ICPs). 

## **8. Conclusion** 

The goal of this paper has been to explore various versions of the requirement of conditional validity. With a small training set, we have to content ourselves with unconditional validity (or abandon any formal requirement of validity altogether). For bigger training sets training conditional validity will be approached by ICPs automatically, and we can approach example conditional validity by using conditional ICPs but making sure that the size of a typical category does not become too small (say, less than 100). In problems of binary classification, we can control false positive and false negative rates by using label conditional ICPs. 

The known property of validity of inductive conformal predictors (Proposition 1) can be stated in the traditional statistical language (see, e.g., Fraser 1957) by saying that they are 1 _− ϵ_ expectation tolerance regions, where _ϵ_ is the significance level. In classical statistics, however, there are two kinds of tolerance regions: 1 _− ϵ_ expectation tolerance regions and PAC-type 1 _− δ_ tolerance regions for a proportion 1 _− ϵ_ , in the terminology of Fraser (1957). We have seen (Proposition 2a) that inductive conformal predictors are tolerance regions in the second sense as well (cf. Vovk 2012, Appendix A). 

A disadvantage of inductive conformal predictors is their potential predictive inefficiency: indeed, the calibration set is wasted as far as the development of the prediction rule _f_ in (1) is concerned, and the proper training set is wasted as far as the calibration (3) of conformity scores into p-values is concerned. Conformal predictors use the full training set for both purposes, and so can be expected to be significantly more efficient. (There have been reports of comparable and even better predictive efficiency of ICPs as compared to conformal predictors but they may be unusual artefacts of the methods used and particular data sets.) It is an open question whether we can guarantee training conditional validity 

489 

Vovk 

under (5) or a similar condition for conformal predictors different from classical tolerance regions. Perhaps no universal results of this kind exist, and different families of conformal predictors will require different methods. 

## **Acknowledgments** 

The empirical studies described in this paper used the R system and the `gbm` package written by Greg Ridgeway. This work was partially supported by the Cyprus Research Promotion Foundation. Many thanks to the reviewers for their advice. 

## **References** 

- A. Frank and A. Asuncion. UCI machine learning repository, 2010. URL `http://archive. ics.uci.edu/ml` . 

- Donald A. S. Fraser. _Nonparametric Methods in Statistics_ . Wiley, New York, 1957. 

- Trevor Hastie, Robert Tibshirani, and Jerome Friedman. _The Elements of Statistical Learning: Data Mining, Inference, and Prediction_ . Springer, New York, second edition, 2009. 

- Jing Lei and Larry Wasserman. Distribution free prediction bands. Technical Report `arXiv:1203.5422 [stat.ME]` , `arXiv.org` e-Print archive, March 2012. 

- Jing Lei, James Robins, and Larry Wasserman. Efficient nonparametric conformal prediction regions. Technical Report `arXiv:1111.1418 [math.ST]` , `arXiv.org` e-Print archive, November 2011. 

- Jing Lei, Alessandro Rinaldo, and Larry Wasserman. Generalized conformal prediction for functional data. 2012. 

- Jon Maindonald and John Braun. _Data Analysis and Graphics Using R: An Example-Based Approach_ . Cambridge University Press, Cambridge, second edition, 2007. 

- Alexandre B. Tsybakov. _Introduction to Nonparametric Estimation_ . Springer, New York, 2010. 

- Stijn Vanderlooy and Ida G. Sprinkhuizen-Kuyper. A comparison of two approaches to classify with guaranteed performance. In _Proceedings of the Eleventh European Conference on Principles and Practice of Knowledge Discovery in Databases_ , volume 4702 of _Lecture Notes in Computer Science_ , pages 288–299, Berlin, 2007. Springer. 

- Vladimir Vovk. Conditional validity of inductive conformal predictors. Technical Report `arXiv:1209.2673` [cs.LG], `arXiv.org` e-Print archive, September 2012. 

- Vladimir Vovk, Alex Gammerman, and Glenn Shafer. _Algorithmic Learning in a Random World_ . Springer, New York, 2005. 

490 

