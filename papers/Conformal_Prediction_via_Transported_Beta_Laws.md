**Conformal Prediction via Transported Beta Laws** 

## **Thiago R. Ramos** 

thiagorr@ufscar.br 

_Federal University of S˜ao Carlos_ 

## **Helton Graziadei** 

helton@ufscar.br 

_Federal University of S˜ao Carlos_ 

## **Luben M. C. Cabezas** 

lucruz45.cab@gmail.com 

_Federal University of S˜ao Carlos, University of S˜ao Paulo, Inria and Universit´e Grenoble Alpes_ 

# **Abstract** 

Split conformal prediction provides finite-sample marginal coverage under exchangeability, but this guarantee averages over the random calibration sample. We study instead the law of the calibration-conditional coverage induced by a realized conformal threshold. In the continuous i.i.d. setting this law is exactly Beta( _k, n_ + 1 _− k_ ), so the usual marginal guarantee corresponds to its mean. We take this beta law as a finite-sample reference object and quantify departures from it using Wasserstein distances on [0 _,_ 1]. The framework yields direct bounds on marginal coverage gaps and on bad-calibration probabilities, and separates different sources of non-i.i.d. behavior according to how they deform the beta reference: test-side shift acts through a transport map on the coverage scale, while calibration dependence changes the order-statistic law itself. We instantiate the framework in scaleshift, clustered, and stationary mixing settings, where the induced deformations can be characterized explicitly or through Berry–Esseen approximations. Simulations on dependent processes confirm that the first-order approximation tracks the empirical Wasserstein distance even at moderate sample sizes. 

**Keywords:** conformal prediction, optimal transport, Wasserstein distance, distribution shift 

# **1. Introduction** 

Conformal prediction (CP) provides a general framework for constructing prediction sets with finite-sample coverage guarantees (Vovk et al., 2005; Papadopoulos et al., 2002; Lei and Wasserman, 2014). In split conformal prediction, a training sample is used to fit a prediction rule and a separate calibration sample is used to choose a score threshold. For calibration scores _S_ 1 _, . . . , Sn_ , with large scores indicating worse conformity, the usual threshold at nominal level _γ ∈_ (0 _,_ 1) is 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0001-16.png)


where _S_ (1) _≤· · · ≤ S_ ( _n_ ) are the order statistics and _S_ ( _k_ ) = + _∞_ for _k > n_ . Under exchangeability, this construction satisfies the familiar marginal guarantee 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0001-18.png)


This guarantee is intentionally marginal: the probability averages over the random calibration sample as well as the test score. Once a calibration sample has been drawn, the threshold is fixed; however, across realizations of the calibration sample, the resulting test coverage is itself a random quantity. By the tower property, 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0002-01.png)


We call the inner probability the _calibration-conditional coverage_ . The usual conformal guarantee controls its mean, but not its sampling distribution. 

In the continuous i.i.d. case this distribution has an exact and universal form. For 1 _≤ k ≤ n_ , define 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0002-04.png)


Then 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0002-06.png)


The beta law is therefore not only a route to the standard marginal coverage bound; it is the finite-sample law of the realized coverage itself (Vovk, 2012; Angelopoulos and Bates, 2021). In a single deployment, the practitioner draws one calibration sample, computes one threshold, and then uses that threshold for future predictions. The realized coverage is one draw from this beta law, while marginal validity constrains only its expectation. For example, with _n_ = 30 and _γ_ = 0 _._ 9, so that _kγ_ = 28, the reference law is Beta(28 _,_ 3); its lower tail assigns probability about 0 _._ 15 to realized coverage below 0 _._ 85, and about 0 _._ 04 to realized coverage below 0 _._ 80. These bad-calibration probabilities are invisible to a statement that only controls the mean. 

Figure 1 visualizes this lower-tail effect and its decay with the calibration size. 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0002-09.png)


Figure 1: Bad-calibration events under i.i.d. beta reference. Left: simulated draws of _Cn,k ∼_ Beta(28 _,_ 3) for _n_ = 30, _γ_ = 0 _._ 9, and _k_ = 28, with the lower tail _Cn,k ≤_ 0 _._ 85 shaded. Right: simulated lower-tail probabilities for _k_ = _⌈_ ( _n_ + 1) _γ⌉_ as the calibration size increases. 

This observation suggests a different way to study conformal prediction beyond the i.i.d. benchmark. Under distribution shift, dependence, or non-identical score distributions, the calibration-conditional coverage need not follow the beta law. Nevertheless, it plays the 

same structural role: marginal coverage is obtained by averaging this realized coverage. The central question is therefore how the law of the realized coverage departs from the beta reference, and how that departure translates into coverage degradation. 

We address this question using optimal transport on the coverage scale. Rather than transporting calibration and test score distributions directly, we compare the law of the calibration-conditional coverage variable with the beta benchmark on [0 _,_ 1]. Since the identity map on [0 _,_ 1] is 1-Lipschitz, a _W_ 1 comparison on this scale immediately controls the marginal coverage gap. In this sense, the beta law remains the reference object, and noni.i.d. mechanisms are understood through the way they transport or deform it. 

Our contributions are as follows. First, we formulate conformal validity through the law _νn,k_ of the realized calibration-conditional coverage and introduce Wasserstein beta neighborhoods around the i.i.d. benchmark _βn,k_ := Beta( _k, n_ + 1 _− k_ ). Second, we prove that _W_ 1( _νn,k, βn,k_ ) directly bounds the marginal coverage gap and derive corresponding bounds for bad-calibration probabilities. Third, we show how different departures from the i.i.d. benchmark act on the beta reference: test-side shift transports the law on the coverage scale, while calibration dependence changes the order-statistic law itself. Counting-process and Berry–Esseen arguments then provide concrete ways to quantify these deformations. The examples are used to illustrate this framework rather than to define separate procedures. 

## **1.1. Related work** 

**The beta law in conformal prediction.** Under continuous i.i.d. scores, the calibrationconditional coverage of split conformal prediction follows a beta distribution (Vovk, 2012; Angelopoulos and Bates, 2021). The i.i.d. assumption can be relaxed to exchangeability. Marques F. (2025) show that, for a test sample exchangeable with the calibration scores, the coverage indicators _Zi_ = **1** _{Sn_ + _i ≤ S_ ( _k_ ) _}_ form an exchangeable sequence; by de Finetti’s theorem, the empirical coverage converges almost surely as the test sample size grows to a random limit, which a combinatorial argument identifies as a beta law. We work in the i.i.d. framing for notational simplicity and because it gives the probability integral transform used in our Wasserstein analysis. 

**Conformal prediction and optimal transport.** A growing line of work applies optimal transport tools to conformal prediction under distribution shift, but the transported object differs from ours. Xu et al. (2025) bound the coverage gap under joint covariate and concept shift using the 1-Wasserstein distance between calibration and test score distributions, and use the bound as a training regularizer. Correia and Louizos (2025) derive coverage-gap bounds formulated via optimal transport distances on the score space and use unlabeled test data to attenuate the gap. Aolaritei et al. (2025) model distribution shift through Levy–Prokhorov ambiguity sets propagated through the score function, reducing a high-dimensional shift to a one-dimensional problem on the score scale. These approaches compare score laws, transported weights, or ambiguity sets. Our comparison takes place after calibration: the transported object is the law of the realized coverage itself on [0 _,_ 1]. This is what makes the Kantorovich–Rubinstein duality immediately yield a marginal coverage-gap bound, without an intermediate quantile-level argument. 

**Conformal prediction beyond exchangeability.** Several other lines of work quantify how violations of exchangeability affect split conformal coverage. Barber et al. (2023) 

develop non-exchangeable conformal prediction via weighted quantiles and nonsymmetric algorithms, with finite-sample bounds that degrade in the total variation distance to a reference exchangeable law. Oliveira et al. (2024) show that vanilla split conformal prediction remains valid for a broad class of non-exchangeable processes, including time series and spatiotemporal data, at the cost of a small coverage penalty controlled by concentration and decoupling arguments. In contrast, we replace total-variation or mixing-type penalties on the data-generating law with _W_ 1 distances between realized-coverage laws. 

A related asymptotic literature studies the joint behavior of conformal coverage across a test sample. Gazin et al. (2024) show that the joint distribution of conformal _p_ -values in a full conformal setting is a P´olya urn and prove a concentration inequality for their empirical c.d.f. under exchangeability. Gazin (2024) identify the asymptotic distribution of the false coverage proportion as _n, m →∞_ , recovering the Kolmogorov law after rescaling, with extensions to weighted conformal and covariate shift. By contrast, our object is finite-sample and fixed-quantile: the law of ( _Cn,k_ ), together with its non-i.i.d. analogue. The P´olya urn and Brownian bridge representations offer complementary large-test-sample descriptions; here we instead study how the finite-sample beta law itself is transported under shift and dependence. 

# **2. Background** 

This section develops the theoretical background required for the remainder of the paper. 

## **2.1. Conformal prediction** 

We recall the basic split conformal construction and the two classical facts that will serve as reference points throughout the paper. The first is the usual finite-sample marginal coverage guarantee. The second is a more refined description of the random coverage level induced by the realized calibration sample. 

Let _S ∼ FS_ be a continuous score distribution, and let _S_ 1 _, . . . , Sn_ denote calibration scores on this scale. In the i.i.d. case, these scores form an independent sample from _FS_ . Define the _adjusted empirical conformal γ-quantile_ as 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0004-07.png)


with the convention that _S_ ( _k_ ) = + _∞_ whenever _k > n_ .<sup>1</sup> 

The conformal threshold is therefore an empirical order statistic of the calibration scores. The use of _⌈γ_ ( _n_ + 1) _⌉_ rather than the usual empirical quantile index is the finite-sample correction that makes the split conformal guarantee hold without asymptotics. 

**Theorem 1 (Split Conformal Marginal Coverage)** _Assume that S_ 1 _, . . . , Sn, Sn_ +1 _are_ ˆ _exchangeable and that there are no ties almost surely. Let kγ_ = _⌈_ ( _n_ + 1) _γ⌉ and qn,γ_ = _S_ ( _kγ_ ) _, with the convention that S_ ( _k_ ) = + _∞ whenever k > n. Then_ 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0004-11.png)


> 1. This definition—using _n_ + 1 in place of _n_ —is standard in conformal prediction, as it guarantees finitesample marginal coverage of at least _γ_ : P ( _Sn_ +1 _≤ q_ ˆ _n,γ_ ) _≥ γ_ . 

The proof of this statement is elementary and relies on the uniformity of ranks. This is the classical finite-sample marginal coverage guarantee of split conformal prediction. It is the benchmark statement: under exchangeability, the conformal threshold covers a fresh score with probability at least _γ_ , up to the unavoidable discretization error of order ( _n_ +1)<sup>_−_1</sup> . 

For our purposes, however, the marginal guarantee is only the first layer of the story. Once the calibration sample is realized, the order statistic _S_ ( _k_ ) is fixed, and the coverage of this realized threshold is itself a random quantity as the calibration sample varies. We next describe the distribution of this calibration-conditional coverage for a fixed order statistic. 

**Proposition 2** _Let S ∼ FS be a continuous random variable and let {Si}_<sup>_n_</sup> _i_ =1<sup>_beani.i.d._</sup> _sample from FS. For_ 1 _≤ k ≤ n, define_ 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0005-03.png)


_Then_ 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0005-05.png)


The proof is given in Appendix A.1. This proposition gives a conditional refinement of the marginal CP guarantee. It says that, in the continuous i.i.d. setting, the realized coverage of the threshold _S_ ( _k_ ) is not arbitrary: its law is exactly the beta law associated with the corresponding order statistic. 

Throughout the paper, we write 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0005-08.png)


for this i.i.d. reference law. 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0005-10.png)



![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0005-11.png)


which recovers the classic CP upper and lower bounds. 

The same beta law also gives a precise way to discuss bad calibration. A bad calibration event occurs when the realized coverage produced by the calibration sample is substantially below the nominal level. The marginal split conformal guarantee controls only the mean of _Cn,k_ ; the lower tail of the beta law controls how often an unfavorable calibration sample occurs. 

**Theorem 3 (i.i.d. Bad Calibration Probabilities)** _Under the assumptions of Proposition 2, let Bn,k ∼ βn,k. Then, for every t ∈_ [0 _,_ 1] _,_ 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0005-15.png)



![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0005-16.png)



![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0005-17.png)


This follows immediately from Proposition 2. It identifies the beta lower tail as the i.i.d. reference probability of a bad calibration event. Later, when the realized coverage law is no longer exactly beta, our Wasserstein bounds will compare its lower tail to this same reference quantity. 

Thus, the classical split conformal guarantee is recovered as the mean of this beta law. The rest of the paper takes this beta distribution as the reference law: departures from the i.i.d. setting will be measured by how much the realized conditional coverage law deviates from this beta benchmark. 

## **2.2. Optimal Transport and Wasserstein Distance** 

We recall the few facts about Wasserstein distances that will be used below (Ambrosio et al., 2005; Villani, 2009; Peyr´e and Cuturi, 2019; Santambrogio, 2015). Let ( _X , d_ ) be a metric space. For _p ≥_ 1, the _p_ -Wasserstein distance between probability laws _µ_ and _ν_ is 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0006-04.png)


where Π( _µ, ν_ ) is the set of couplings with marginals _µ_ and _ν_ . On the space of probability laws with finite _p_ -th moment, _Wp_ is a metric. In particular, when _X_ = [0 _,_ 1], the moment condition is automatic. 

In this paper, the laws compared by Wasserstein distances are laws of calibrationconditional coverage variables, supported on [0 _,_ 1]. In this setting, with _d_ ( _u, v_ ) = _|u − v|_ , the definition becomes 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0006-07.png)


We first record two elementary consequences of the definition. 

**Proposition 4 (Coupling Upper Bound)** _Fix p ≥_ 1 _. Let µ and ν be probability laws on_ [0 _,_ 1] _. If X ∼ µ and Y ∼ ν are defined on the same probability space, then_ 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0006-10.png)


This bound is our basic way of turning a concrete coupling into a Wasserstein estimate. The next fact explains how estimates at different Wasserstein orders are related. 

**Proposition 5 (Monotonicity in** _p_ **)** _Let µ and ν be probability laws on_ [0 _,_ 1] _. If_ 1 _≤ p ≤ q, then_ 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0006-13.png)


This monotonicity lets us state some intermediate estimates in the Wasserstein order that is most convenient and then read them on the _W_ 1 scale used for coverage. 

For estimates involving expectations, we will also use the following dual form of _W_ 1. 

**Proposition 6 (Dual Representation and Mean Bound)** _If µ and ν are probability measures on_ [0 _,_ 1] _, then_ 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0007-01.png)


_In particular,_ 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0007-03.png)


The first identity in Proposition 6 is the Kantorovich–Rubinstein duality (Santambrogio, 2015, Eq. (3.1)). The second follows by taking the identity map _u �→ u_ , which is 1-Lipschitz on [0 _,_ 1]. Together with Proposition 5, this means that any _Wp_ bound with _p ≥_ 1 can be converted into the corresponding mean bound through _W_ 1 when needed. 

**Proposition 7 (Optimality of Monotone Transport)** _Fix p ≥_ 1 _. Let µ and ν be probability laws on_ R _with finite p-th moments. Assume that Fµ is continuous, and let Fν_<sup>_−_1</sup> _denote the generalized inverse of Fν. Define_ 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0007-06.png)



![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0007-07.png)



![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0007-08.png)


This is the one-dimensional monotone rearrangement theorem (Santambrogio, 2015, Thm. 2.9). It gives an explicit optimal map, which will be useful when a distorted realizedcoverage law can be transported back to its beta reference. 

**Proposition 8 (One-Dimensional Formula)** _Let µ and ν be probability laws on_ [0 _,_ 1] _, with distribution functions Fµ and Fν. Then_ 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0007-11.png)


Proposition 8 will be useful when the calibration-conditional coverage law is described through an order statistic or through the associated counting process. 

Although our main objects are supported on [0 _,_ 1], some asymptotic calculations below compare Gaussian limits on R. We will use the following closed form for centered normal laws, where _W_ 1 is computed with the Euclidean distance. 

**Lemma 9 (Centered Normal Laws)** _For any σ_ 1 _, σ_ 2 _≥_ 0 _,_ 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0007-15.png)


# **3. A Transportation Framework for Conformal Prediction** 

In the previous section, we identified _βn,k_ as the law of the realized coverage induced by the _k_ -th conformal order statistic in the continuous i.i.d. setting. We now use this beta law as a reference object. A calibration and test mechanism induces a law for its realized coverage, and the main question is how much this law differs from the i.i.d. beta benchmark. 

Fix 1 _≤ k ≤ n_ , and let 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0008-03.png)


be the calibration scores under a joint law _P_ . Let _T_<sup>�</sup> denote the test score.<sup>2</sup> This notation does not tie the test score to the next index after calibration; for example, in a time-series setting one may take _T_<sup>�</sup> = _Tn_ + _h_ , with _h_ fixed or depending on _n_ . Let the calibration order statistics be 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0008-05.png)


The marginal coverage of the threshold _T_ ( _k_ ) is 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0008-07.png)


We write it as the expectation of the coverage realized by the particular calibration sample: 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0008-09.png)


Thus 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0008-11.png)


The law of this random realized coverage is 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0008-13.png)


In the continuous i.i.d. reference case, Proposition 2 gives _νn,k_ = _βn,k_ . The framework below keeps _βn,k_ fixed as the benchmark and measures the deformation from _βn,k_ to _νn,k_ on the coverage scale [0 _,_ 1]. This leads to the following convenient notation. 

**Definition 10 (Wasserstein Beta Neighborhood)** _Let P_ ([0 _,_ 1]) _denote the set of probability laws on_ [0 _,_ 1] _. For p ≥_ 1 _and ρ ≥_ 0 _, define_ 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0008-16.png)


_We say that the realized coverage law is in the p-Wasserstein beta neighborhood of radius ρ when_ 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0008-18.png)


The radius _ρ_ quantifies how far the realized coverage law is from the i.i.d. beta law. When _ρ_ = 0, the realized coverage law is exactly the beta reference; for positive _ρ_ , it is a transported or perturbed version of that reference. To make this geometric picture concrete, consider the contaminated law _νπ,c_ = (1 _− π_ ) _βn,k_ + _πδc_ , which replaces a fraction _π_ of the 

> 2. Throughout the text, _Si_ denotes i.i.d. scores, while _Ti_ denotes scores that need not be i.i.d. 

beta mass by a point mass at coverage value _c ∈_ [0 _,_ 1]. A direct computation via Proposition 8 gives 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0009-01.png)


so the radius grows linearly in _π_ at a rate determined by how far _c_ sits from the bulk of _βn,k_ . Figure 2 displays this as a function of ( _π, c_ ), with each contour tracing the boundary of the Wasserstein ball _B_ 1( _βn,k, ρ_ ) for a different radius _ρ_ . The shape of these contours reflects the geometry of the contamination: for _c_ close to _γ_ , the point mass lands near the bulk of _βn,k_ and transport is cheap, so the contour allows a larger contamination fraction _π_ before the radius _ρ_ is exceeded. As _c_ moves away from _γ_ , the transport cost per unit of _π_ increases, and the contour bends inward, permitting only a smaller _π_ for the same budget _ρ_ . Each contour therefore defines a feasible region in ( _π, c_ ): staying inside it is precisely the condition _νπ,c ∈B_ 1( _βn,k, ρ_ ). 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0009-03.png)


Figure 2: Wasserstein radius _W_ 1( _νπ,c, βn,k_ ) for the contaminated law _νπ,c_ = (1 _−π_ ) _βn,k_ + _πδc_ , with _n_ = 50, _k_ = 46, and _γ_ = 0 _._ 9. Each white contour traces the boundary of _B_ 1( _βn,k, ρ_ ) for a given _ρ_ , defining the set of contaminations ( _π, c_ ) compatible with that transport budget. Contamination near _c_ = _γ_ allows a larger fraction _π_ for the same radius, while contamination away from _γ_ forces _π_ to be small — the contour shape directly encodes this trade-off. 

## **3.1. Coverage Guarantees** 

The first consequence of a Wasserstein comparison is a direct bound on marginal coverage. This is the basic reason for working on the coverage scale. 

**Theorem 11 (Wasserstein Coverage Gap)** _Fix_ 1 _≤ k ≤ n, and define Dn,k, νn,k, and_ Cov( _k_ ) _as above. Then_ 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0010-01.png)


_Consequently, if νn,k ∈Bp_ ( _βn,k, ρ_ ) _for some p ≥_ 1 _, then_ 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0010-03.png)


_If kγ_ = _⌈_ ( _n_ + 1) _γ⌉≤ n, then_ 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0010-05.png)


The proof is given in Appendix A.2. The theorem says that once the realized coverage law is close to the beta benchmark in Wasserstein distance, the usual conformal coverage level degrades by at most the same amount, up to the standard discretization term. 

The previous result controls the average of _Dn,k_ . We can also ask for the probability that a realized calibration sample produces unusually low coverage. A Wasserstein beta neighborhood gives a comparison with the lower tail of the beta reference. 

**Theorem 12 (Bad Calibration Probabilities)** _Let Bn,k ∼ βn,k. If_ 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0010-09.png)


_for some p ≥_ 1 _, then, for every t ∈_ [0 _,_ 1] _and every ε >_ 0 _,_ 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0010-11.png)


The proof is given in Appendix A.3. The beta term is the probability of a bad calibration event in the i.i.d. reference model; the additional term accounts for the transport needed to move the beta law to the realized coverage law. The Markov penalty is useful when only an average transport radius is available, but it can be conservative, especially on the _W_ 1 scale. 

When the deformation from the beta law can be bounded uniformly, the bad calibration comparison takes a sharper form. Let 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0010-14.png)


be the monotone transport map from _βn,k_ to _νn,k_ , and let _Bn,k ∼ βn,k_ . If 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0010-16.png)


then for every _t ∈_ [0 _,_ 1], 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0010-18.png)


_d_ Indeed, under this coupling _Dn,k_ = _T_ mon( _Bn,k_ ), and _T_ mon( _Bn,k_ ) _≤ t_ implies _Bn,k ≤ t_ + _ρ_ . Thus a uniform transport bound shifts the beta lower tail without the Markov penalty appearing in Theorem 12. This is the cleanest version of the transported-beta picture, and we use it whenever an explicit transport map is available. 

## **3.2. Decoupled Test Scores and Transported Beta Laws** 

A particularly useful simplification occurs when the test score is decoupled from the calibration sample. This assumption is natural in independent holdout evaluation and in distribution-shift settings with separate calibration and test batches. It is also a useful reduction for temporally dependent data when the test point is sufficiently separated from the calibration block and the dependence decays with the lag. 

**Proposition 13 (Decoupled Test Scores)** _Assume that T_<sup>�</sup> _is independent of Cn, and let FT_ � _be its distribution function. Then_ 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0011-03.png)


_Suppose that the calibration scores have a common continuous marginal distribution function FT , and let FT_<sup>_−_1</sup> _denote its generalized inverse. Define_ 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0011-05.png)


_Then the variables Ui are marginally uniform on_ [0 _,_ 1] _, possibly dependent, and, for h_ := _F_ � _T ◦ FT_<sup>_−_1</sup><sup>_,wehave_</sup> 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0011-07.png)


The proof is given in Appendix A.4. In the no-shift case _FT_ � = _FT_ , the map _h_ is the identity and _νn,k_ = _L_ ( _U_ ( _k_ )), so Theorem 11 reduces coverage analysis to 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0011-09.png)


The following proposition records the counting-process representation of this distance. 

**Proposition 14 (Counting Formula)** _Let U_ 1 _, . . . , Un be random variables on_ [0 _,_ 1] _. Assume each Ui is uniform; independence is not required. Let_ 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0011-12.png)


_Then, for every t ∈_ [0 _,_ 1] _and_ 1 _≤ k ≤ n,_ 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0011-14.png)


_Consequently, if Zn,t ∼_ Bin( _n, t_ ) _, then_ 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0011-16.png)


The proof is given in Appendix A.5. Thus the Wasserstein distance to the beta law is exactly the integrated difference between the dependent empirical-count tail and the binomial tail. 

## **3.3. Berry–Esseen Transport for Dependent Calibration** 

In many dependent calibration settings, the law of _U_ ( _k_ ) is not exactly beta, but it admits a Berry–Esseen approximation. This is enough to control its Wasserstein distance to the beta reference. 

Let _U_ 1 _, . . . , Un_ be marginally uniform random variables on [0 _,_ 1], not necessarily independent, and fix _γ ∈_ (0 _,_ 1). Here Φ denotes the standard normal distribution function. Suppose that, for some _τγ >_ 0 and some deterministic sequence _an →_ 0, 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0012-03.png)


This assumption says that the calibration order statistic has a Berry–Esseen law with asymptotic standard deviation _τγ_ . The i.i.d. beta reference has the same form with standard deviation ~~�~~ _γ_ (1 _− γ_ ). 

**Proposition 15 (Quantile-to-Beta Transport)** _If the preceding Berry–Esseen bound holds, then_ 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0012-06.png)


_In particular, if an_ = _O_ ( _n_<sup>_−_1</sup><sup>_/_2</sup> ) _, then_ 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0012-08.png)


The proof is given in Appendix A.7. 

In the next section, we apply this framework in several concrete settings. The examples differ in how the beta law is deformed, but the logic is the same: identify the realized coverage law, compare it with _βn,k_ , and translate that comparison into a coverage statement. 

# **4. Applications** 

## **4.1. Exact Transported Beta Laws under Distribution Shift** 

We first consider a decoupled distribution-shift setting. The calibration scores are i.i.d. from a continuous distribution function _FT_ , while the test score is independent of the calibration sample but follows a possibly different distribution function _FT_ � . Let _FT_<sup>_−_1</sup> denote the generalized inverse, or quantile function, of the calibration score distribution. The conformal threshold _T_ ( _k_ ) is therefore generated under the calibration law, but its coverage is evaluated under the test law. 

For a realized calibration sample, the realized test coverage is 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0012-15.png)


Since the calibration sample is i.i.d. with distribution function _FT_ , the probability integral transform gives 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0012-17.png)


Thus the shifted realized coverage can be written on the beta scale as 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0013-01.png)


Equivalently, if _h_ := _FT_ � _◦ FT_<sup>_−_1</sup><sup>_,_then</sup> 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0013-03.png)


Distribution shift therefore does not alter the beta order-statistic mechanism itself. It transports the beta law through the map relating calibration and test score distributions. When _FT_ � = _FT_ , the map _h_ is the identity and _νn,k_ = _βn,k_ , recovering the i.i.d. reference case. In general, the relevant comparison is 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0013-05.png)


We illustrate the distribution-shift mechanism in a setting where the transport map is explicit. 

## 4.1.1. Example: half-normal scale shift 

The example is motivated by the usual split conformal regression score 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0013-09.png)


If the prediction error is centered Gaussian, then _T_ has a half-normal distribution. Let 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0013-11.png)


with _T_<sup>�</sup> independent of the calibration sample, and define the scale ratio 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0013-13.png)


Writing _q_ ( _u_ ) := Φ<sup>_−_1�</sup><sup>_<u>u</u>_</sup><sup><u>+1</u></sup> 2 � _,_ the calibration-to-test transport map is 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0013-15.png)


Thus, if _Bn,k_ := _FσT_ ( _T_ ( _k_ )) _∼ βn,k,_ then the realized coverage under the shifted test distribution satisfies 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0013-17.png)


Therefore, in the half-normal scale-shift model, distribution shift does not alter the beta order-statistic law on the calibration scale; it transports this law through the deterministic map _hr_ . Details on the derivation of _hr_ , its inverse, and the corresponding density transformation are given in Appendix A.6. 

The direction of the deformation is determined by _r_ . If _r >_ 1, the test scores are more dispersed than the calibration scores and _hr_ ( _u_ ) _< u_ , leading to undercoverage. If _r <_ 1, then _hr_ ( _u_ ) _> u_ , leading to overcoverage. Moreover, 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0013-20.png)



![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0014-00.png)


Figure 3: Transported beta laws under half-normal scale shift for _n_ = 30, _γ_ = 0 _._ 9, and _k_ = 28, so that _Bn,k ∼_ Beta(28 _,_ 3). Under the scale ratio _r_ = _σT_ � _/σT_ , the _d_ realized coverage satisfies _Dn,k_ = _hr_ ( _Bn,k_ ). As _r_ increases above one, the law is transported to the left, increasing the probability of bad calibration. The vertical lines mark _γ_ = 0 _._ 90 and _γ − η_ = 0 _._ 85, with _η_ = 0 _._ 05. 

so that 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0014-03.png)


In this example, the Wasserstein coverage-gap bound is: 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0014-05.png)


Figure 3 illustrates the induced deformation for _n_ = 30, _γ_ = 0 _._ 9, and _k_ = _⌈_ ( _n_ +1) _γ⌉_ = 28, so that the i.i.d. reference law is Beta(28 _,_ 3). The curve _r_ = 1 corresponds to this reference law. As _r_ increases above one, the realized-coverage law is transported to the left, increasing the probability of low calibration-conditional coverage. The vertical lines mark the nominal level _γ_ = 0 _._ 9 and the bad-calibration threshold _γ − η_ = 0 _._ 85, with _η_ = 0 _._ 05. 

For small scale shifts, writing _r_ = _e_<sup>_δ_</sup> , the local approximation derived in Appendix A.6 gives 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0014-08.png)


At _γ_ = 0 _._ 9, the coefficient 2 _ϕ_ ( _q_ ( _γ_ )) _q_ ( _γ_ ) is approximately 0 _._ 339. Thus a 10% increase in the test-score scale, _r_ = 1 _._ 1, corresponds to an approximate coverage loss of about 0 _._ 032, or roughly three percentage points. 

Thus, in the half-normal scale-shift model, the abstract Wasserstein coverage-gap bound becomes an exact identity: the transport distance from the beta reference is precisely the 

marginal coverage loss, and the transported law determines bad-calibration probabilities through its left tail P ( _hr_ ( _Bn,k_ ) _≤ t_ ). Figure 5 in Appendix A.6 makes this concrete across _r ∈{_ 0 _._ 5 _,_ 0 _._ 8 _,_ 2 _._ 0 _}_ and _n ∈{_ 50 _,_ 200 _,_ 1000 _}_ : the shaded area between the CDFs grows with _|r −_ 1 _|_ and is insensitive to _n_ , while the right panel reveals that _W_ 1 is asymmetric around _r_ = 1, with undercoverage ( _r >_ 1) incurring a larger transport cost than overcoverage ( _r <_ 1) for the same departure, reflecting the nonlinearity of _hr_ and the concentration of _βn,k_ near _γ_ . 

## **4.2. Clustered Calibration and Effective Sample Size** 

Proposition 14 has a simple concrete instance in clustered or replicated calibration data. Think of _b_ independent experimental units, subjects, videos, or spatial locations, each producing _m_ nearly identical calibration scores, so that _n_ = _mb_ . The following idealized model takes the within-cluster dependence to be perfect. Let 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0015-03.png)


and set 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0015-05.png)


and then relabel _{Uj,r}_ as _U_ 1 _, . . . , Un_ . Each _Ui_ is still marginally uniform, but the effective number of independent calibration units is _b_ , not _n_ . Indeed, 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0015-07.png)


so _Nn_ ( _t_ ) =<sup>_d_</sup> _mZb,t_ , with _Zb,t ∼_ Bin( _b, t_ ). Proposition 14 gives 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0015-09.png)


Equivalently, 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0015-11.png)


and therefore 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0015-13.png)


This example is an extreme cluster model and creates ties within the calibration block. The counting identity and the Wasserstein comparison do not require absence of ties, but the example can also be viewed as the limit of a model with small within-cluster jitter. Its purpose is to isolate the practical effect: using _n_ highly clustered calibration points behaves, for the realized coverage law, more like using _b_ independent calibration units. 

_d_ Thus, in the no-shift decoupled-test version of this application, _Dn,k_ = _U_ ( _k_ ). If 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0015-16.png)


then Theorem 11 gives 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0015-18.png)


For _kγ_ = _⌈_ ( _n_ + 1) _γ⌉_ , the target level is therefore degraded by at most _ρ_ cl( _kγ_ ) + 1 _/_ ( _n_ + 1). Theorem 12 also gives, for every _t ∈_ [0 _,_ 1] and _ε >_ 0, 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0016-01.png)


In this example, both conclusions say that clustering affects conformal coverage only through the transport from the nominal beta law based on _n_ points to the effective beta law based on _b_ independent units. 

## **4.3. Stationary Mixing Processes** 

We now apply Proposition 15 to a stationary score process ( _Ti_ ) _i∈_ Z. Let _FT_ be its continuous marginal distribution function. The calibration sample is _Cn_ = ( _T_ 1 _, . . . , Tn_ ), and the test score is taken _ℓ_ steps after the calibration block: 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0016-05.png)


The transformed variables _Ui_ = _FT_ ( _Ti_ ) are marginally uniform on [0 _,_ 1], but they are not independent in general. 

Let _Fa_<sup>_b_=</sup><sup>_σ_(</sup><sup>_Ti_:</sup><sup>_a ≤i ≤b_).Weusethefollowingstandardmixingcoefficients:</sup> 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0016-08.png)


for strong, or _α_ -, mixing, 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0016-10.png)


for _ϕ_ -mixing, and 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0016-12.png)


for absolute regularity, or _β_ -mixing. Different normalizations of the _β_ -mixing coefficient appear in the literature; only its role as a decoupling error is used below. 

For fixed _t_ , the event _{Tn_ + _ℓ ≤ t}_ is separated from _Cn_ by _ℓ_ time steps. Under _ϕ_ -mixing this gives the direct conditional decoupling bound<sup>3</sup> 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0016-15.png)


Evaluating this bound at the random threshold _T_ ( _k_ ), and setting 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0016-17.png)


> 3. Formally, we first apply the mixing bound on the countable set _t ∈_ Q, choosing an almost-sure event on which all these inequalities hold. For a regular conditional distribution of _Tn_ + _ℓ_ given _Cn_ , the conditional c.d.f. is right-continuous in _t_ ; since _FT_ is continuous, the bound extends from rational thresholds to all _t ∈_ R. This almost-sure uniform version can then be evaluated at the random threshold _T_ ( _k_ ). 

we obtain 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0017-01.png)


Since _FT_ ( _T_ ( _k_ )) = _U_ ( _k_ ), Proposition 4 and the triangle inequality give 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0017-03.png)


The first term is the price of using a future dependent test point; the second is the deviation of the calibration order statistic from the i.i.d. beta reference. 

A similar separation can be obtained for absolutely regular processes by blocking. Coupling lemmas for separated blocks, such as Yu (1994, Corollary 2.7), allow one to replace separated dependent blocks by independent copies at a cost controlled by the corresponding _β_ -mixing coefficients. We do not need the explicit block construction in what follows. The relevant point is that, after the test-calibration dependence is handled by a direct _ϕ_ -mixing argument, by a _β_ -mixing blocking argument, or by an external independence assumption, the remaining problem is to control the calibration order statistic _U_ ( _k_ ). 

We summarize the decoupling step by assuming that, for some deterministic ∆ _ℓ ≥_ 0, 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0017-07.png)


For the direct _ϕ_ -mixing argument above one may take ∆ _ℓ_ = _ϕ_ mix( _ℓ_ ); if the future test score has already been decoupled from the calibration block, then ∆ _ℓ_ = 0. It remains to control _L_ ( _U_ ( _k_ )). The external input we use is a Berry–Esseen theorem for sample quantiles of strongly mixing, equivalently _α_ -mixing, sequences. 

**Theorem 16 (Berry–Esseen Bound for** _α_ **-Mixing Sample Quantiles)** _Let_ ( _Xi_ ) _i∈_ Z _be a stationary strongly mixing (α-mixing) sequence with marginal distribution function F . Fix p ∈_ (0 _,_ 1) _, write F_<sup>_−_1</sup> _for the generalized inverse of F , and suppose that F has density f near F_<sup>_−_1</sup> ( _p_ ) _. Let_ 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0017-10.png)


_We write Fn_<sup>_−_1</sup> _for the generalized inverse of Fn. Assume the regularity conditions (C.1)– (C.5) of Lahiri and Sun (2009, Theorem, Section 2.3; see also Eq. (1.4)), including the strong-mixing rate condition on α_ mix _. Then_ 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0017-12.png)


_where_ 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0017-14.png)


_and_ 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0017-16.png)


Suppose that the transformed calibration process ( _Ui_ ) _i∈_ Z satisfies the assumptions of Theorem 16 at quantile level _γ_ . Its marginal distribution is uniform, so _F_<sup>_−_1</sup> ( _γ_ ) = _γ_ , _f_ ( _γ_ ) = 1, and, with the generalized inverse convention, _Fn_<sup>_−_1(</sup><sup>_γ_)=</sup><sup>_U_</sup> ( _⌈nγ⌉_ )<sup>.Theconformalindex</sup> _kγ_ = _⌈_ ( _n_ + 1) _γ⌉_ differs from _⌈nγ⌉_ by at most one, so the same Berry–Esseen approximation applies to _U_ ( _kγ_ ), with the index perturbation absorbed in the _O_ ( _n_<sup>_−_1</sup><sup>_/_2</sup> ) remainder. Thus the Berry–Esseen assumption in Proposition 15 holds for _kγ_ with _an_ = _O_ ( _n_<sup>_−_1</sup><sup>_/_2</sup> ) and 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0018-01.png)


whenever the covariance series is well defined and _τγ_<sup>2</sup><sup>_>_0.Therefore,</sup> 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0018-03.png)


Thus Theorem 11, together with _|kγ/_ ( _n_ +1) _−γ| ≤_ 1 _/_ ( _n_ +1), gives the marginal coverage bound 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0018-05.png)


Theorem 12 gives the corresponding bad-calibration statement from the same radius. Let 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0018-07.png)


The Wasserstein bound above shows that 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0018-09.png)


Applied with _p_ = 1, Theorem 12 gives that for every _t ∈_ [0 _,_ 1] and every _ε >_ 0, 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0018-11.png)


In particular, for any _η ∈_ (0 _, γ_ ), 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0018-13.png)


Thus the probability of a low realized-coverage event is controlled by the i.i.d. beta lower tail, plus the decoupling and Berry–Esseen errors encoded in _ρn,ℓ_ . 

## 4.3.1. Example: AR(1) process 

Let ( _Ti_ ) _i∈_ Z be a stationary AR(1) process, 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0018-17.png)


Then _Ti ∼ N_ (0 _,_ 1) for every _i_ , but the scores are serially dependent. The calibration sample is _Cn_ = ( _T_ 1 _, . . . , Tn_ ), and the test score is _Tn_ + _ℓ_ for a fixed horizon _ℓ ≥_ 1. By the Markov property, 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0018-19.png)


Therefore the realized coverage at threshold _T_ ( _k_ ) is 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0019-01.png)


For this example, the decoupling radius ∆ _ℓ_ in (1) can be obtained directly from the Markov property without invoking mixing conditions: since _Tn_ + _ℓ | Cn ∼ N_ ( _a_<sup>_ℓ_</sup> _Tn,_ 1 _− a_<sup>2</sup><sup>_ℓ_</sup> ) differs from _N_ (0 _,_ 1) only through a mean shift of order _|a|_<sup>_ℓ_</sup> , one obtains ∆ _ℓ_ ≲ _|a|_<sup>_ℓ_</sup> . The geometric decay used below thus arises from the Markov structure of the AR(1) alone. 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0019-03.png)


Figure 4: Realized-coverage laws _νn,k_ for the Gaussian AR(1) model with _n_ = 50 and _γ_ = 0 _._ 9, against the i.i.d. beta reference _βn,k_ (dashed red). At _ℓ_ = 1, larger positive values of _a_ produce a more dispersed realized-coverage law, with both a sharper concentration near 1 and a heavier left tail extending below the bad-calibration threshold _γ−η_ = 0 _._ 85. As _ℓ_ grows, the direct test-calibration dependence weakens and the laws approach the calibration-order-statistic law _L_ ( _U_ ( _k_ )); this limit equals _βn,k_ only when the calibration scores are independent. 

The expression contains two effects. The order statistic _T_ ( _k_ ) is the calibration contribution, while _a_<sup>_ℓ_</sup> _Tn_ is the remaining dependence between the future test score and the last calibration score. As _ℓ_ increases, _a_<sup>_ℓ_</sup> decreases geometrically and the test score becomes closer to an independent draw from the marginal _N_ (0 _,_ 1). In the limit _ℓ →∞_ , 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0019-06.png)


in distribution. The remaining deviation from the beta reference is then the calibrationorder-statistic effect controlled by the _α_ -mixing Berry–Esseen argument above. 

Figure 4 shows the induced realized-coverage laws for fixed _n_ = 50 and _γ_ = 0 _._ 9, across several values of _a_ and _ℓ ∈{_ 1 _,_ 10 _,_ 25 _}_ . Larger _a_ and smaller _ℓ_ produce stronger testcalibration effects; increasing _ℓ_ removes this contribution and moves the law toward the calibration-order-statistic law _U_ ( _k_ ), which may still differ from the beta benchmark when calibration dependence is strong. 

The complementary roles of _ℓ_ and _n_ for the AR(1) example are illustrated in Figures 6, 7 and 8 in Appendix B.2. Figure 6 displays the Monte Carlo estimate of _W_ 1( _νn,kγ , βn,kγ_ ) and the bound (1) as functions of the horizon _ℓ_ , for fixed _n_ = 200 and _a ∈{_ 0 _,_ 0 _._ 3 _,_ 0 _._ 6 _,_ 0 _._ 9 _}_ . For _a_ = 0 the scores are i.i.d. and _W_ 1 is negligible for all _ℓ_ . For _a >_ 0, the test–calibration term _|a|_<sup>_ℓ_</sup> decays geometrically, and both quantities flatten as _ℓ_ grows: the bound flattens at the Berry–Esseen floor ~~�~~ 2 _/_ ( _πn_ ) _|τγ −_ ~~�~~ _γ_ (1 _− γ_ ) _|_ , while _W_ 1 flattens at the (typically smaller) limiting value _W_ 1( _L_ ( _U_ ( _kγ_ )) _, βn,kγ_ ) associated with the calibration order statistic alone. 

Figure 7 fixes _ℓ ∈{_ 1 _,_ 10 _,_ 25 _}_ and varies _n_ . The Monte Carlo curves confirm the marginal-coverage gap inequality of Theorem 11, _|_ Cov( _kγ_ ) _− kγ/_ ( _n_ +1) _| ≤ W_ 1. The asymptotic upper bound on _W_ 1, on the other hand, is informative only once _n_ is large enough relative to _a_ and _ℓ_ for the Berry–Esseen approximation to take effect: it is conservative for small _n_ combined with large _a_ and small _ℓ_ (top-right panels), and becomes tighter once _|a|_<sup>_ℓ_</sup> is small, so that the bound and _W_ 1 are jointly dominated by the Berry–Esseen calibration term. 

Finally, Figure 8 translates these Wasserstein distances into bad-calibration probabilities through Theorem 12: the Markov-type tail control P( _Bn,kγ ≤ γ −η/_ 2)+2 _W_ 1 _/η_ is loose, and may exceed one, whenever _W_ 1 is comparable to or larger than _η_ ; it tightens progressively as _ℓ_ increases and the test-dependence contribution to _W_ 1 decays. 

# **5. Conclusion** 

We introduced a transported-beta perspective on split conformal prediction. Instead of viewing conformal validity only through marginal coverage, we studied the law of the calibration-conditional coverage induced by the realized calibration sample. In the continuous i.i.d. case this law is exactly Beta( _k, n_ + 1 _− k_ ), so the classical split conformal coverage level is recovered as its mean, while its lower tail quantifies bad-calibration events. 

The main message is that this beta law remains a useful finite-sample reference beyond the i.i.d. setting. By comparing the realized-coverage law _νn,k_ with the beta benchmark _βn,k_ on the coverage scale, Wasserstein distances give direct control of marginal coverage gaps and bad-calibration probabilities. This formulation separates different mechanisms of noni.i.d. behavior: test-side distribution shift transports the beta law through a deterministic coverage map, whereas calibration dependence changes the order-statistic law itself. 

The examples illustrate how this viewpoint can be used as a diagnostic and comparison tool rather than as a single new conformal algorithm. In scale-shift models the deformation is explicit and the Wasserstein bound can be sharp; in clustered and mixing settings the distance to the beta reference captures effective sample size and dependence effects. Simulations on dependent uniform processes confirm that the Berry–Esseen approximation tracks the empirical Wasserstein distance closely, even at moderate sample sizes. Future work could focus on estimating the transported-beta radius from data, extending the framework to adaptive or weighted conformal procedures, and developing sharper finite-sample tail comparisons. 

# **References** 

- Luigi Ambrosio, Nicola Gigli, and Giuseppe Savar´e. _Gradient Flows in Metric Spaces and in the Space of Probability Measures_ . Birkh¨auser, Basel, 2005. 

- Anastasios N. Angelopoulos and Stephen Bates. A gentle introduction to conformal prediction and distribution-free uncertainty quantification, 2021. 

- Liviu Aolaritei, Zheyu Oliver Wang, Julie Zhu, Michael I. Jordan, and Youssef Marzouk. Conformal prediction under L´evy–Prokhorov distribution shifts: Robustness to local and global perturbations, 2025. 

- Rina Foygel Barber, Emmanuel J. Cand`es, Aaditya Ramdas, and Ryan J. Tibshirani. Conformal prediction beyond exchangeability. _The Annals of Statistics_ , 51(2):816–845, 2023. doi: 10.1214/23-AOS2276. 

- Alvaro H. C. Correia and Christos Louizos. Non-exchangeable conformal prediction with optimal transport: Tackling distribution shifts with unlabeled data. In _The Thirty-ninth Annual Conference on Neural Information Processing Systems_ , 2025. 

- Ulysse Gazin. Asymptotics for conformal inference. _arXiv preprint arXiv:2409.12019_ , 2024. 

- Ulysse Gazin, Gilles Blanchard, and Etienne Roquain. Transductive conformal inference with adaptive scores. In _Proceedings of the 27th International Conference on Artificial Intelligence and Statistics (AISTATS)_ , volume 238 of _Proceedings of Machine Learning Research_ , pages 1504–1512, 2024. 

- S. N. Lahiri and S. Sun. A berry–esseen theorem for sample quantiles under weak dependence. _The Annals of Applied Probability_ , 19(1):108–126, 2009. doi: 10.1214/08-AAP533. 

- Jing Lei and Larry Wasserman. Distribution-free prediction bands for non-parametric regression. _Journal of the Royal Statistical Society: Series B (Statistical Methodology)_ , 76 (1):71–96, 2014. doi: 10.1111/rssb.12021. 

- Paulo C. Marques F. Universal distribution of the empirical coverage in split conformal prediction. _Statistics and Probability Letters_ , 219:110350, 2025. doi: 10.1016/j.spl.2024. 110350. 

- Roberto I Oliveira, Paulo Orenstein, Thiago Ramos, and Joao Vitor Romano. Split conformal prediction and non-exchangeable data. _Journal of Machine Learning Research_ , 25 (225):1–38, 2024. 

- Harris Papadopoulos, Kostas Proedrou, Volodya Vovk, and Alex Gammerman. Inductive confidence machines for regression. In Tapio Elomaa, Heikki Mannila, and Hannu Toivonen, editors, _Machine Learning: ECML 2002_ , volume 2430 of _Lecture Notes in Computer Science_ , pages 345–356, Berlin, Heidelberg, 2002. Springer. doi: 10.1007/3-540-36755-1 ~~2~~ 9. 

- Gabriel Peyr´e and Marco Cuturi. Computational optimal transport. _Foundations and Trends in Machine Learning_ , 11(5–6):355–607, 2019. doi: 10.1561/2200000073. 

- Filippo Santambrogio. _Optimal Transport for Applied Mathematicians_ , volume 87 of _Progress in Nonlinear Differential Equations and Their Applications_ . Birkh¨auser, Cham, 2015. doi: 10.1007/978-3-319-20828-2. 

- C´edric Villani. _Optimal Transport: Old and New_ , volume 338 of _Grundlehren der mathematischen Wissenschaften_ . Springer, Berlin, Heidelberg, 2009. doi: 10.1007/ 978-3-540-71050-9. 

- Vladimir Vovk. Conditional Validity of Inductive Conformal Predictors. In _Proceedings of the Asian Conference on Machine Learning_ , pages 475–490. PMLR, November 2012. URL `https://proceedings.mlr.press/v25/vovk12.html` . 

- Vladimir Vovk, Alex Gammerman, and Glenn Shafer. _Algorithmic Learning in a Random World_ . Springer-Verlag, Berlin, Heidelberg, 2005. ISBN 0387001522. 

- Rui Xu, Chao Chen, Yue Sun, Parvathinathan Venkitasubramaniam, and Sihong Xie. Wasserstein-regularized conformal prediction under general distribution shift. In _The Thirteenth International Conference on Learning Representations_ , 2025. 

- Bin Yu. Rates of convergence for empirical processes of stationary mixing sequences. _The Annals of Probability_ , 22(1):94–116, 1994. doi: 10.1214/aop/1176988849. 

# **Appendix A. Proofs** 

## **A.1. Proof of Proposition 2** 

**Proof** Conditional on the calibration sample _S_ 1 _, . . . , Sn_ , the order statistic _S_ ( _k_ ) is fixed. Since _Sn_ +1 is independent of the calibration sample and has distribution _FS_ , the conditional coverage is simply the distribution function evaluated at the realized threshold: 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0023-03.png)


The remaining step is to identify the distribution of this random value as the calibration sample varies. Define 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0023-05.png)


By the probability integral transform, the variables _U_ 1 _, . . . , Un_ are i.i.d. Unif(0 _,_ 1). Since _FS_ is monotone, the ordering of the _Si_ ’s is preserved, and hence 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0023-07.png)


The _k_ -th order statistic of _n_ i.i.d. uniform random variables has distribution 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0023-09.png)


Therefore, 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0023-11.png)


## **A.2. Proof of Theorem 11** 

**Proof** The i.i.d. reference law satisfies 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0023-14.png)


On the other hand, by the tower property, 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0023-16.png)


Therefore the marginal coverage gap is 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0023-18.png)


By Proposition 6, 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0023-20.png)


which proves the first claim. If _νn,k ∈Bp_ ( _βn,k, ρ_ ), then Proposition 5 gives 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0023-22.png)


This proves the beta-neighborhood bound. If _kγ_ = _⌈_ ( _n_ + 1) _γ⌉≤ n_ , then 

and 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0024-02.png)


The lower bound and the final absolute-error bound follow immediately from the betaneighborhood bound and the discretization bound above. 

## **A.3. Proof of Theorem 12** 

**Proof** Let _Bn,k ∼ βn,k_ , and let 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0024-06.png)


be the monotone transport map from _βn,k_ to _νn,k_ . Define 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0024-08.png)


_d_ By Proposition 7, _Dn,k_<sup>_⋆∼νn,k_.Therefore</sup><sup>_D_</sup> _n,k_<sup>_⋆_</sup> = _Dn,k_ , and 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0024-10.png)


Define 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0024-12.png)


On _Gε_ , if _T_ mon( _Bn,k_ ) _≤ t_ , then 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0024-14.png)


Thus 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0024-16.png)


It follows that 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0024-18.png)


By Markov’s inequality and the optimality of _T_ mon, 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0024-20.png)


Combining the last two displays proves the claim. 

## **A.4. Proof of Proposition 13** 

**Proof** Since _T_<sup>�</sup> is independent of _Cn_ , conditioning on the calibration sample fixes _T_ ( _k_ ) and gives 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0025-02.png)


This proves the first display. 

Now suppose that the calibration scores have common continuous marginal distribution function _FT_ , and define _Ui_ = _FT_ ( _Ti_ ). By the probability integral transform, each _Ui_ is marginally uniform on [0 _,_ 1]; no independence among the _Ui_ ’s is required for this marginal statement. Since _FT_ is monotone, the ordering is preserved, so 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0025-05.png)


With the generalized inverse convention, this gives 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0025-07.png)


Therefore 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0025-09.png)


In the i.i.d. uniform reference case, the order statistic satisfies _U_ ( _k_ ) _∼ βn,k_ , and the final display follows. 

## **A.5. Proof of Proposition 14** 

**Proof** The event _U_ ( _k_ ) _≤ t_ is exactly the event that at least _k_ calibration variables are at most _t_ , which gives the first identity. For the i.i.d. uniform reference sample, the corresponding count is Bin( _n, t_ ), and its _k_ -th order statistic has law _βn,k_ . The Wasserstein identity then follows from Proposition 8. 

## **A.6. Details for the Half-Normal Scale-Shift Example** 

For _σ >_ 0, the distribution function of _|N_ (0 _, σ_<sup>2</sup> ) _|_ is 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0025-15.png)


Hence 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0025-17.png)


Writing 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0025-19.png)


we have _Fσ_<sup>_−_1(</sup><sup>_u_) =</sup><sup>_σq_(</sup><sup>_u_).Thereforethecalibration-to-testtransportmapis</sup> 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0025-21.png)


where _r_ = _σ_ � _T /σT_ . Let 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0026-01.png)


Since the calibration sample is i.i.d. from _FσT_ , 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0026-03.png)


Moreover, 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0026-05.png)


Thus 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0026-07.png)


and 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0026-09.png)


We next derive the density of the transported law. Let _z ∈_ (0 _,_ 1). If _z_ = _hr_ ( _u_ ), then 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0026-11.png)


Therefore, 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0026-13.png)


and hence 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0026-15.png)


It follows that 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0026-17.png)


Differentiating with respect to _z_ , 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0026-19.png)


Since 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0026-21.png)


we have 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0026-23.png)


Therefore, 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0026-25.png)


If _fn,k_ denotes the density of _βn,k_ = Beta( _k, n_ + 1 _− k_ ), then the density of _Dn,k_ = _hr_ ( _Bn,k_ ) is 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0027-01.png)


We now justify the sharpness of the Wasserstein bound in this example. The map _hr_ is increasing on (0 _,_ 1). Moreover, since _q_ ( _u_ ) _>_ 0 for _u ∈_ (0 _,_ 1), 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0027-03.png)


Thus _hr −_ id has constant sign on (0 _,_ 1). The monotone coupling ( _Bn,k, hr_ ( _Bn,k_ )) is optimal in one dimension, and therefore 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0027-05.png)


The last equality uses E[ _Bn,k_ ] = _k/_ ( _n_ + 1). 

Finally, we derive the local small-shift approximation. Write _r_ = _e_<sup>_δ_</sup> . Then 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0027-08.png)


Differentiating with respect to _δ_ , 

At _δ_ = 0, 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0027-11.png)


Thus 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0027-13.png)


Taking expectations under _Bn,k ∼ βn,k_ gives 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0027-15.png)


For _kγ_ = _⌈_ ( _n_ + 1) _γ⌉_ , the beta law concentrates around _γ_ . Therefore, 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0027-17.png)


and hence 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0027-19.png)


## **A.7. Proof of Proposition 15** 

**Proof** Write 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0028-02.png)


Let _Bn,kγ ∼ βn,kγ_ , and denote by _FU_ and _FB_ the distribution functions of _U_ ( _kγ_ ) and _Bn,kγ_ , respectively. Since both laws are supported on [0 _,_ 1], Proposition 8 gives 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0028-04.png)


We now rewrite the two distribution functions on the central-limit scale. For _x ∈_ R, set 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0028-06.png)


By assumption, 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0028-08.png)


For the i.i.d. beta benchmark, the classical Berry–Esseen theorem for sample quantiles gives 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0028-10.png)


This is the standard Berry–Esseen approximation for the _kγ_ -th order statistic of an i.i.d. uniform sample. Since _kγ_ = _⌈_ ( _n_ + 1) _γ⌉_ , we have _kγ/_ ( _n_ + 1) = _γ_ + _O_ ( _n_<sup>_−_1</sup> ); this centering difference is absorbed by the _O_ ( _n_<sup>_−_1</sup><sup>_/_2</sup> ) remainder. 

Now fix _t ∈_ [0 _,_ 1]. Then 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0028-13.png)


Using the triangle inequality inside the integral, 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0028-15.png)


Integrating over _t ∈_ [0 _,_ 1] and using the two uniform Berry–Esseen bounds therefore yields 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0028-17.png)


where 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0028-19.png)


It remains to identify _In_ . With the change of variables _x_ =<sup>_√_</sup> _<u>n</u>_ <u>(</u> _t − γ_ ), 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0029-01.png)


The functions _x �→_ Φ( _x/τγ_ ) and _x �→_ Φ( _x/sγ_ ) are the distribution functions of _N_ (0 _, τγ_<sup>2) and</sup> _N_ (0 _, s_<sup>2</sup> _γ_<sup>).Thustheone-dimensional</sup><sup>_W_1formulaonRgives</sup> 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0029-03.png)


By Lemma 9, 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0029-05.png)


Consequently, 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0029-07.png)


Combining this with _cn_ = _O_ ( _n_<sup>_−_1</sup><sup>_/_2</sup> ) gives 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0029-09.png)


which is the first claim. If _an_ = _O_ ( _n_<sup>_−_1</sup><sup>_/_2</sup> ), then the term _an_ is absorbed into the final remainder, giving the second display. 

# **Appendix B. Example additional results** 

This section presents additional illustrations for the two worked examples in the main text. In both cases, _W_ 1( _νn,k, βn,k_ ), the coverage gap and the transported laws _νn,k_ are estimated via Monte Carlo with 50 _,_ 000 simulations per configuration, by drawing directly from the underlying process in each example and computing the relevant quantities empirically. Shaded bands throughout indicate _±_ 2 standard errors across simulations. In general, standard errors are very low; the wider band for the coverage gap observed in Figure 7 near zero is a consequence of the logarithmic scale employed, as the absolute error remains stable while the gap itself approaches zero. 

## **B.1. Half-normal illustrations and results** 

Figure 5 complements the density plot in the main text by showing the full CDF deformation across a wider range of _r_ and _n_ . The left panels make the shaded _W_ 1 area directly visible for each ( _r, n_ ) pair, confirming that the deformation is stable across calibration sizes. The right panel traces _W_ 1 and the coverage gap jointly as functions of _r_ , verifying the exact equality from both sides of _r_ = 1 and across all three values of _n_ . 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0030-00.png)


Figure 5: Half-normal scale-shift example with _γ_ = 0 _._ 9. **Left:** CDFs of _νn,k_<sup>(</sup><sup>_r_)</sup> = ( _hr_ )# _βn,k_ (solid blue) against _βn,k_ (dashed black) for _r ∈{_ 0 _._ 5 _,_ 0 _._ 8 _,_ 2 _._ 0 _}_ and _n ∈{_ 50 _,_ 200 _,_ 1000 _}_ ; the shaded area equals _W_ 1( _νn,k_<sup>(</sup><sup>_r_)</sup><sup>_, βn,k_)andisessentiallycon-</sup> stant across _n_ . **Right:** exact identity _W_ 1( _νn,k_<sup>(</sup><sup>_r_)</sup><sup>_, βn,k_)=</sup><sup>_|_Cov(</sup><sup>_k_)</sup><sup>_−k/_(</sup><sup>_n_+1)</sup><sup>_|_</sup> verified across _r ∈_ [0 _._ 3 _,_ 3 _._ 0]; the asymmetry around _r_ = 1 reflects the nonlinearity of _hr_ , with undercoverage ( _r >_ 1) incurring a larger transport cost than overcoverage ( _r <_ 1) for the same _|r −_ 1 _|_ . 

## **B.2. AR(1) illustrations and results** 

Figures 6, 7, and 8 complement Figure 4 by quantifying the deformation across a wider range of configurations. Figure 6 traces _W_ 1 and the bound (1) as functions of _ℓ_ for fixed _n_ = 200, showing the geometric decay and the residual Berry–Esseen floor. Figure 7 varies _n_ for fixed _ℓ ∈{_ 1 _,_ 10 _,_ 25 _}_ , confirming the chain coverage gap _≤ W_ 1 _≤_ Berry–Esseen bound across all configurations. Figure 8 translates these into bad-calibration probabilities, with the bound tightening as _ℓ_ increases. 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0031-00.png)


Figure 6: _W_ 1( _νn,kγ , βn,kγ_ ) (solid blue) and the asymptotic bound (1) (dashed orange) as functions of _ℓ_ , for _n_ = 200, _γ_ = 0 _._ 9, and _a ∈{_ 0 _,_ 0 _._ 3 _,_ 0 _._ 6 _,_ 0 _._ 9 _}_ . For _a_ = 0, _W_ 1 is negligible for all _ℓ_ ; for _a >_ 0, both decay geometrically and level off at the Berry–Esseen floor, which depends only on _n_ and the long-run variance _τγ_<sup>2.</sup> 

Bound comparisons AR(1) Gaussian,  = 0.9 gap (dashed) W1 (solid) Berry--Esseen bound (dotted, asymptotic) 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0032-01.png)


Figure 7: Chain of bounds _|_ Cov( _kγ_ ) _− kγ/_ ( _n_ +1) _| ≤ W_ 1( _νn,kγ , βn,kγ_ ) _≤|a|_<sup>_ℓ_</sup> + ~~�~~ 2 _/_ ( _πn_ ) _|τγ −_ ~~�~~ _γ_ (1 _− γ_ ) _|_ + _O_ ( _n_<sup>_−_1</sup><sup>_/_2</sup> ) as a function of _n_ , for _γ_ = 0 _._ 9, _a ∈{_ 0 _._ 3 _,_ 0 _._ 6 _,_ 0 _._ 9 _}_ , and _ℓ ∈{_ 1 _,_ 10 _,_ 25 _}_ . Solid blue: Monte-Carlo _W_ 1; dashed red: coverage gap; dotted orange: asymptotic bound. The chain holds throughout the asymptotic regime; for small _n_ with large _a_ and small _ℓ_ the bound is conservative, and tightens as _|a|_<sup>_ℓ_</sup> decays. 


![](Conformal_Prediction_via_Transported_Beta_Laws_images/Conformal_Prediction_via_Transported_Beta_Laws.pdf-0033-00.png)


Figure 8: Bad-calibration bound from Theorem 12: P( _Dn,k_<sup>(</sup><sup>_ℓ_)</sup> _γ_<sup>_≤γ−η_)(solidblue)against</sup> P( _Bn,kγ ≤ γ − η/_ 2) + 2 _W_ 1 _/η_ (dashed green) as a function of _n_ , for _γ_ = 0 _._ 9, _η_ = 0 _._ 05, _a ∈{_ 0 _._ 3 _,_ 0 _._ 6 _,_ 0 _._ 9 _}_ , and _ℓ ∈{_ 5 _,_ 10 _}_ . The bound can exceed one for large _a_ and small _ℓ_ , where the Markov penalty 2 _W_ 1 _/η_ dominates, and tightens as _ℓ_ grows and _W_ 1 decays. 

