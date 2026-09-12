# Universal distribution of the empirical coverage in split conformal prediction 

## Paulo C. Marques F. 

aInsper Institute of Education and Research, Rua Quat´a, 300, S˜ao Paulo, 04546-042, SP, Brazil 


![](Universal_distribution_of_the_empirical_coverage_in_split_conformal_prediction_images/Universal_distribution_of_the_empirical_coverage_in_split_conformal_prediction.pdf-0001-04.png)


## Abstract 

When split conformal prediction operates in batch mode with exchangeable data, we determine the exact distribution of the empirical coverage of prediction sets produced for a finite batch of future observables, as well as the exact distribution of its almost sure limit when the batch size goes to infinity. Both distributions are universal, being determined solely by the nominal miscoverage level and the calibration sample size, thereby establishing a criterion for choosing the minimum required calibration sample size in applications. 

Keywords: Prediction sets, Batch mode prediction, Empirical coverage, Split conformal prediction, Calibration sample size, de Finetti’s representation theorem. 


![](Universal_distribution_of_the_empirical_coverage_in_split_conformal_prediction_images/Universal_distribution_of_the_empirical_coverage_in_split_conformal_prediction.pdf-0001-08.png)


## 1. Introduction 

Conformal prediction is a framework developed to quantify the confidence in the forecasts made by general predictive models which is quickly moving the field of machine learning from a stage dominated by point predictions to a new period in which forecasts are summarized by prediction sets with statistical guarantees. Several features make conformal prediction appealing for use with contemporary machine learning algorithms: it is universal (distributionfree), able to handle high-dimensionaldata, model agnostic, and its properties hold for finite samples [1, 2, 3]. Notably, the split conformal prediction algorithm [4, 5] is a widely adopted conformalization technique which strikes a balance between predictive properties and computational cost. Our goal in this paper is to identify the exact distribution of the empirical coverage of prediction sets produced by the split conformal prediction procedure for a finite batch of future observables, as well as to determine the exact distribution of its almost sure limit when the batch size tends to infinity. Both distributions are universal in the sense that they are determined solely by the nominal miscoverage level and the calibration sample size. The distribution of the empirical coverage was investigated for the first time in [6] and [7], with further discussion in [8]. Our contribution consists in a formulation that emphasizes the role of the data exchangeability assumption and the combinatorial nature of the aforementioned properties of the empirical coverage, which are derived using standard exchangeability tools. Although this investigation pertains to the foundations of conformal prediction, the results are eminently practical and lead to a criterion summarized in Table 1 for the choice of the calibration sample size in applications. 

## 2. Split conformal prediction 

Let (Ω, F , P) denote the underlying probability space from which we induce the distributions of all random objects considered in the paper. 

Definition 1. A sequence of random objects {Oi}i≥1 is exchangeable if, for every n ≥ 1 and every permutation � π : {1, . . ., n} −→{1, . . ., n}, the random tuples (O1, . . . , On) and (Oπ(1), . . . , Oπ(n)) have the same distribution. 


![](Universal_distribution_of_the_empirical_coverage_in_split_conformal_prediction_images/Universal_distribution_of_the_empirical_coverage_in_split_conformal_prediction.pdf-0001-14.png)


Email address: PauloCMF1@insper.edu.br (Paulo C. Marques F.) 

We are in a supervised learning setting [9] in which for each sample unit we have a d-dimensional vector of predictors Xi ∈ R<sup>d</sup> and a response variable Yi ∈ Y . Specifically, in regression tasks with univariate response we take Y = R and in classification problems Y = {1, . . ., L} is a set of class labels. We have a data sequence of random pairs laid out as 


![](Universal_distribution_of_the_empirical_coverage_in_split_conformal_prediction_images/Universal_distribution_of_the_empirical_coverage_in_split_conformal_prediction.pdf-0002-01.png)


which is modeled by us as being exchangeable. At the beginning of the sequence we have the training sample T = ((X−t+1, Y−t+1), . . ., (X0, Y0)), of size t ≥ 1, followed by the calibration sample ((X1, Y1), . . ., (Xn, Yn)), of size n ≥ 1, and the sequence of future observables {(Xn+i, Yn+i)}i≥1. In applications, the available data is randomly split into the training and calibration samples, hence the name split conformal prediction, also known as the inductive case of conformal prediction. The data exchangeability assumption allows us to conveniently place the training sample at the beginning of the sequence. Let T = σ(T ) be the smallest sub-σ-field of F with respect to which the training sample is measurable. 

Definition 2. A conformity function is a mapping ρ : R<sup>d</sup> × Y × Ω → R such that ρ(x, y) = ρ(x, y, · ) is T -measurable for every x ∈ R<sup>d</sup> and every y ∈ Y . The sequence of conformity scores {S i}i≥1 associated with a conformity function ρ is defined by S i(ω) = ρ(Xi(ω), Yi(ω), ω). We say that a conformity function ρ is regular with respect to a specific data sequence if there are no ties among the corresponding conformity scores {S i}i≥1 almost surely. 

Note that the regularity of a specific conformity function ρ is contextual, being inherently dependent on the distribution of the underlying data sequence. Technically, we can always avoid ties among the sequence of conformity scores almost surely by introducing a properly constructed ancillary tie-breaking sequence. 

Example 1. In regression problems, let µˆ : R<sup>d</sup> × Ω → R be a regression function estimator. A standard choice [4, 5] is to use the conformity function ρ(x, y, ω) = |y − µˆ(x, ω)|. Conformalized quantile regression [10] is a widely adopted alternative. For p ∈ [0, 1], let ξp(x) = inf {y ∈ R : P(Y1 ≤ y | X1 = x} ≥ p} be the conditional pth quantile function and suppose that we have an estimator ξ<sup>ˆ</sup> p : R<sup>d</sup> × Ω → R of ξp. Choose 0 < plo ≤ phi < 1 and define the conformity function ρ(x, y, ω) = max {ξ<sup>ˆ</sup> phi (x, ω) − y, y − ξ<sup>ˆ</sup> plo(x, ω)}. The choice of plo and phi is discussed in [10]. In classification problems, let πˆ ℓ : R<sup>d</sup> × Ω → [0, 1] be a classification algorithm outputting probabilities for each one of the class labels ℓ = 1, . . ., L. In this classification case, we can take our conformity function to be ρ(x, y, ω) = 1 − πˆ y(x, ω). 

Conformity functions are agnostic to the choice of the specific models or algorithms used to construct µˆ, ξ<sup>ˆ</sup> p, and πˆ in Example 1. The intuition is that the associated conformity scores measure the ability of the model to make accurate predictions on the calibration sample, whose information is not used in the model´s training process, and the assumed data sequence exchangeability transfers this assessment of the model’s predictive capacity from the calibration sample to the sequence of future observables. The following result is proved in the Appendix. 

Lemma 1. Under the data exchangeability assumption, the sequence of conformity scores {S i}i≥1 is exchangeable. 

For a real number t, let ⌈t⌉ = min {k ∈ Z : t ≤ k} and ⌊t⌋ = max {k ∈ Z : k ≤ t} denote the ceiling and the floor of t, respectively. 

Definition 3. For a regular conformity function ρ, denote the associated ordered calibration sample conformity scores by S (1), S (2), . . ., S (n). Let 0 < α < 1 be a specified nominal miscoverage level satisfying ⌈(1 − α)(n + 1)⌉≤ n, in which case we say that the pair (n, α) is feasible. Define the random conformal prediction set Dn<sup>(α)</sup> : R<sup>d</sup> × Ω → A by 

D<sup>(</sup> n<sup>α)(x, ω) = �y ∈Y: ρ(x, y, ω) ≤S (⌈(1−α)(n+1)⌉)(ω)�,</sup> 

for a suitable σ-field of subsets of Y denoted by A . We use the notation D<sup>(</sup> n<sup>α)(x) =D(</sup> n<sup>α)(x,· ).</sup> 

Example 2. Let sˆ = S (⌈(1−α)(n+1)⌉)(ω0), for an outcome ω0 ∈ Ω. It follows from Definition 3 and the definitions in Example 1 that for a future vector of predictors x<sup>∗</sup> ∈ R<sup>d</sup> the observed conformal prediction sets have the forms: D<sup>(</sup> n<sup>α)(x∗)=(ˆµ(x∗) −sˆ, ˆµ(x∗) +sˆ),forthestandardconformityfunction,D(</sup> n<sup>α)(x∗)=(ˆξ</sup> plo<sup>(x∗) −sˆ, ˆξ</sup> phi<sup>(x∗) +sˆ),for</sup> conformalized quantile regression, and D<sup>(</sup> n<sup>α)(x∗) = {y ∈{1, . . ., L} :πˆ</sup> y<sup>(x∗) ≥1 −sˆ}, for classification.</sup> 

2 

The first major consequence of Lemma 1 is the classical marginal validity property [4, 5] of the conformal prediction sets introduced in Definition 3. This property can be described briefly as follows. For a regular conformity function ρ, using the notations and conditions in Definition 3, the distributional symmetry expressed in Lemma 1 and the fact that we have no ties almost surely among the sequence of conformity scores, ensure that, for every i ≥ 1, the conformity score S n+i for a future random pair (Xn+i, Yn+i) is uniformly ranked among the ordered calibration sample conformity scores: P(S n+i ≤ S ( j)) = j/(n + 1), for j = 1, . . ., n. By choosing j = ⌈(1 − α)(n + 1)⌉, noting that t ≤⌈t⌉ < t + 1, for every t ∈ R, and considering that Yn+i ∈ D<sup>(</sup> n<sup>α)(X</sup> n+i<sup>)ifandonlyifS</sup> n+i<sup>≤S</sup> (⌈(1−α)(n+1)⌉)<sup>(asper</sup> Definitions 2 and 3), we have the marginal validity property: 


![](Universal_distribution_of_the_empirical_coverage_in_split_conformal_prediction_images/Universal_distribution_of_the_empirical_coverage_in_split_conformal_prediction.pdf-0003-01.png)


## 3. Empirical coverage distribution 

Definition 4. Using the notations and conditions in Definition 3, let {Zi}i≥1 be a sequence of coverage indicators defined by Zi = 1, if Yn+i ∈ D<sup>(</sup> n<sup>α)(X</sup> n+i<sup>),andZ</sup> i<sup>=0,otherwise.Theempiricalcoverageofabatch ofm≥1future</sup> observables is the random variable Cm<sup>(n,α)</sup> = (1/m)<sup>�m</sup> i=1<sup>Zi.</sup> 

In general, the coverage indicators Zi are dependent random variables, since for all future observables the corresponding conformal prediction sets in Definition 3 are defined in terms of the same calibration sample conformity score S (⌈(1−α)(n+1)⌉). This would still be the case even if we had started with the stronger assumption of an independent and identically distributed data sequence. The interesting fact is that Definition 4 inherits through Lemma 1 the distributional symmetry implied by the data exchangeability assumption, giving us the following result, proved in the Appendix. 

Theorem 1. Under the data exchangeability assumption, for a regular conformity function, the sequence of coverage indicators {Zi}i≥1 is exchangeable and m × Cm<sup>(n,α)</sup> is distributed as a Beta-Binomial(⌈(1 − α)(n + 1)⌉, ⌊α(n + 1)⌋) random variable, to the effect that the distribution of the empirical coverage is given by 


![](Universal_distribution_of_the_empirical_coverage_in_split_conformal_prediction_images/Universal_distribution_of_the_empirical_coverage_in_split_conformal_prediction.pdf-0003-06.png)


for k = 0, 1, . . ., m, and every future batch size m ≥ 1. 

By symmetry, Definition 4 and the exchangeability of the sequence of coverage indicators established in Theorem 1 yield that E[Cm<sup>(n,α)</sup> ] = E[Z1] = P(Yn+1 ∈ D<sup>(</sup> n<sup>α)(X</sup> n+1<sup>)).Consequently, we can interpret the marginal validity property</sup> (1) as partial information about the distribution of the empirical coverage. Specifically, as an inequality constraint on the expectation of Cm<sup>(n,α)</sup> . The following result, proved in the Appendix as a direct consequence of Theorem 1 and de Finetti’s representation theorem, identifies the distribution of the almost sure limit of the empirical coverage Cm<sup>(n,α)</sup> when the future batch size m tends to infinity. 

Theorem 2. Under the data exchangeability assumption, for a regular conformity function, the empirical coverage Cm<sup>(n,α)</sup> converges almost surely, when the future batch size tends to infinity, to a random variable C∞<sup>(n,α)</sup> with distribution Beta(⌈(1 − α)(n + 1)⌉, ⌊α(n + 1)⌋). 

## 4. Calibration sample size and concluding remarks 

In applications, we typically use a trained model to construct a large number of prediction intervals and Theorem 2 gives us a criterion to determine the minimum calibration sample size required to control the empirical coverage C∞<sup>(n,α)</sup> of an infinite batch of future observables. Given a nominal miscoverage level α, we specify an ǫ > 0 and a tolerance probability 0 < τ < 1, looking for the smallest calibration sample size such that the empirical coverage C∞<sup>(n,α)</sup> of an infinite batch of future observables is within ǫ of 1 − α, with a probability of at least τ. Formally, recalling from 

3 

|||ǫ =0.1|||ǫ =0.05|||ǫ =0.01|||ǫ =0.005||
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|1−α<br>τ|90%|95%|99%|90%|95%|99%|90%|95%|99%|90%|95%|99%|
|80%|40|57|98|170|241|418|4,326|6,142|10,611|17,314|24,581|42,457|
|85%|30|42|77|134|189|330|3,446|4,893|8,451|13,794|19,587|33,830|
|90%|11|14|47|90|128|227|2,429|3,448|5,958|9,733|13,821|23,875|
|95%|19|19|29|22|29|97|1,270|1,806|3,132|5,125|7,278|12,578|




![](Universal_distribution_of_the_empirical_coverage_in_split_conformal_prediction_images/Universal_distribution_of_the_empirical_coverage_in_split_conformal_prediction.pdf-0004-01.png)


Table 1: Universal coverage tolerance table for split conformal prediction. For a nominal miscoverage level α, an ǫ > 0, and a tolerance probability τ, the table entries are the minimum required calibration sample sizes such that the empirical coverage C∞<sup>(n,α)</sup> of an infinite batch of future observables is within ǫ of 1 − α, with a probability of at least τ, according to Theorem 2. 

Definition 3 that a feasible pair (n, α) satisfies ⌈(1 − α)(n + 1)⌉≤ n, which is equivalent to saying that the integer n ≥ (1 − α)/α, the minimum required calibration size is given by 


![](Universal_distribution_of_the_empirical_coverage_in_split_conformal_prediction_images/Universal_distribution_of_the_empirical_coverage_in_split_conformal_prediction.pdf-0004-04.png)


Table 1 gives the values of the minimum required calibration sample size n0 for different values of α, ǫ, and τ. That an understanding of the distribution of the empirical coverage is necessary to determine the minimum required calibration sample sizes in applications of split conformal prediction was first discussed in [8]. The calibration sample sizes presented in [8] are slightly larger than the corresponding values in Table 1. In the repository [11] we have the R [12] code used to determine the calibration sample sizes in Table 1 and a comparison with the corresponding values given in [8]. Repository [11] also contains a simulation illustrating the results in Theorems 1 and 2. 

## Acknowledgments 

Paulo C. Marques F. receives support from FAPESP (Fundac¸˜ao de Amparo `a Pesquisa do Estado de S˜ao Paulo) through project 2023/02538-0. 

## Appendix. Proofs 

Proof of Lemma 1. Recall that T (ω) = ((X−t+1(ω), Y−t+1(ω)), . . ., (X0(ω), Y0(ω))) and T = σ(T ). Since the conformity function ρ in Definition 2 is such that ρ(x, y) is T -measurable for every x ∈ R<sup>d</sup> and every y ∈ Y , Doob-Dynkin’s lemma (see [13], Theorem A.42) implies that there is a measurable function 


![](Universal_distribution_of_the_empirical_coverage_in_split_conformal_prediction_images/Universal_distribution_of_the_empirical_coverage_in_split_conformal_prediction.pdf-0004-10.png)


such that ρ(Xi(ω), Yi(ω), ω) = h(T (ω), (Xi(ω), Yi(ω))), for every i ≥ 1, and each ω ∈ Ω. Hence, for Borel sets B1, . . ., Bn, we have 


![](Universal_distribution_of_the_empirical_coverage_in_split_conformal_prediction_images/Universal_distribution_of_the_empirical_coverage_in_split_conformal_prediction.pdf-0004-12.png)


� For any permutation π : {−t + 1, . . ., 0, 1, . . ., n} −→{−t + 1, . . ., 0, 1, . . ., n}, define 


![](Universal_distribution_of_the_empirical_coverage_in_split_conformal_prediction_images/Universal_distribution_of_the_empirical_coverage_in_split_conformal_prediction.pdf-0004-14.png)


4 

If we consider only permutations π such that π( j) = j, for −t + 1 ≤ j ≤ 0, then Tπ = T and the data exchangeability assumption yields 


![](Universal_distribution_of_the_empirical_coverage_in_split_conformal_prediction_images/Universal_distribution_of_the_empirical_coverage_in_split_conformal_prediction.pdf-0005-01.png)


Since this restriction on π still allows an arbitrary permutation of the conformity scores S 1, . . . , S n, and the argument holds for every n ≥ 1, the desired exchangeability of the sequence of conformity scores {S i}i≥1 follows. 

Proof of Theorem 1. Let b = ⌈(1 − α)(n + 1)⌉ and g = n − b + 1 = ⌊α(n + 1)⌋, recalling from Definition 3 that the pair (n, α) is assumed to be feasible, so that b ≤ n. We will prove by induction on the batch size m ≥ 1 that 


![](Universal_distribution_of_the_empirical_coverage_in_split_conformal_prediction_images/Universal_distribution_of_the_empirical_coverage_in_split_conformal_prediction.pdf-0005-04.png)


in which (z1, . . . , zm) ∈{0, 1}<sup>m</sup> , with<sup>�m</sup> i=1<sup>zi=k, for k=0, 1, . . ., m.Due to the assumed regularity of the underlying</sup> conformity function ρ, there are no ties among the sequence of conformity scores almost surely, and the distributional symmetry established in Lemma 1 implies that S n+1 is uniformly ranked among the calibration sample conformity scores (S 1, . . ., S n). By Definitions 3 and 4, for every i ≥ 1, the coverage indicator Zi = 1 if and only if S n+i ≤ S (b), so that P(Z1 = 1) = P(S n+1 ≤ S (b)) = b/(n + 1). Hence, P(Z1 = 0) = g/(n + 1) and property (∗) holds for m = 1. By Lemma 1 and the regularity of ρ, the conformity score S n+m+1 is ranked uniformly among the n + m conformity scores (S 1, . . ., S n, S n+1, . . ., S n+m). Moreover, the event {Z1 = z1, . . . , Zm = zm}, with<sup>�m</sup> i=1<sup>zi=k, means that exactly</sup> k of the conformity scores (S n+1, . . . , S n+m) are less than or equal to S (b). Hence, given that {Z1 = z1, . . ., Zm = zm}, with<sup>�m</sup> i=1<sup>zi=k,wehavethatS n+m+1≤S (b)ifandonlyifS n+m+1isrankedamongtheb +kconformityscores</sup> {S (1), . . ., S (b)} ∪ �∪<sup>m</sup> i=1 �S n+i : S n+i ≤ S (b)�<sup>�</sup> , to the effect that 


![](Universal_distribution_of_the_empirical_coverage_in_split_conformal_prediction_images/Universal_distribution_of_the_empirical_coverage_in_split_conformal_prediction.pdf-0005-06.png)


Now, for the inductive step, suppose that property (∗) holds for some batch size m ≥ 2. The product rule gives 


![](Universal_distribution_of_the_empirical_coverage_in_split_conformal_prediction_images/Universal_distribution_of_the_empirical_coverage_in_split_conformal_prediction.pdf-0005-08.png)


Since P(Z1 = z1, . . ., Zm = zm, Zm+1 = 0) = 1 − P(Z1 = z1, . . ., Zm = zm, Zm+1 = 1), in general we have that 


![](Universal_distribution_of_the_empirical_coverage_in_split_conformal_prediction_images/Universal_distribution_of_the_empirical_coverage_in_split_conformal_prediction.pdf-0005-10.png)


in which (z1, . . . , zm+1) ∈{0, 1}<sup>m+1</sup> , with<sup>�</sup> i<sup>m</sup> =<sup>+</sup> 1<sup>1zi=k′,fork′=0, 1, . . ., m + 1.Therefore,property (∗)holdsfora</sup> batch with size m + 1, completing the inductive step and implying that property (∗) holds for every batch size m ≥ 1. Inspection of the right hand side of (∗) reveals that the random vector (Z1, . . . , Zm) is exchangeable, and since this holds for every batch size m ≥ 1, we get as our first conclusion that the sequence of coverage indicators {Zi}i≥1 is exchangeable. Finally, the event {<sup>�m</sup> i=1<sup>Zi=k}istheunionof</sup> �mk� mutually exclusive and, by exchangeability, equiprobable events of the form {Z1 = z1, . . . , Zm = zm}, in which (z1, . . ., zm) ∈{0, 1}<sup>m</sup> , with<sup>�m</sup> i=1<sup>zi=k.Therefore,</sup> property (∗) and Definition 4 yield the desired result: 


![](Universal_distribution_of_the_empirical_coverage_in_split_conformal_prediction_images/Universal_distribution_of_the_empirical_coverage_in_split_conformal_prediction.pdf-0005-12.png)



![](Universal_distribution_of_the_empirical_coverage_in_split_conformal_prediction_images/Universal_distribution_of_the_empirical_coverage_in_split_conformal_prediction.pdf-0005-13.png)


5 

Proof of Theorem 2. By Theorem 1, the sequence of coverage indicators {Zi}i≥1 is exchangeable, and de Finetti’s representation theorem [13] states that there is a random variable, say, C∞<sup>(n,α)</sup> : Ω → [0, 1], with distribution µ, such that, given that C∞<sup>(n,α)</sup> = θ, the {Zi}i≥1 are conditionally independent and identically distributed with distribution Bernoulli(θ), so that we have the integral representation 


![](Universal_distribution_of_the_empirical_coverage_in_split_conformal_prediction_images/Universal_distribution_of_the_empirical_coverage_in_split_conformal_prediction.pdf-0006-01.png)


m for (z1, . . ., zm) ∈{0, 1}<sup>m</sup> . For k = 0, 1, . . ., m, the event {<sup>�m</sup> i=1<sup>Zi=k}istheunionof</sup> � k� mutually exclusive and, by exchangeability, equiprobable events of the form {Z1 = z1, . . ., Zm = zm}, in which (z1, . . ., zm) ∈{0, 1}<sup>m</sup> , with �mi=1<sup>zi= k.Therefore, it follows from the integral representation above and Definition 4 that</sup> 


![](Universal_distribution_of_the_empirical_coverage_in_split_conformal_prediction_images/Universal_distribution_of_the_empirical_coverage_in_split_conformal_prediction.pdf-0006-03.png)


Let the distribution µ of C∞<sup>(n,α)</sup> be dominated by Lebesgue measure λ with Radon-Nikodym derivative 


![](Universal_distribution_of_the_empirical_coverage_in_split_conformal_prediction_images/Universal_distribution_of_the_empirical_coverage_in_split_conformal_prediction.pdf-0006-05.png)


up to almost everywhere [λ] equivalence, in which b = ⌈(1 − α)(n + 1)⌉ and g = n − b + 1 = ⌊α(n + 1)⌋. This is a version of the density of a random variable with Beta(b, g) distribution. Using (†) and the Leibniz rule for Radon-Nikodym derivatives (see [13], Theorem A.79), we have that 


![](Universal_distribution_of_the_empirical_coverage_in_split_conformal_prediction_images/Universal_distribution_of_the_empirical_coverage_in_split_conformal_prediction.pdf-0006-07.png)


Since de Finetti’s representation theorem states that the distribution µ of C∞<sup>(n,α)</sup> is unique and that (1/m)<sup>�m</sup> i=1<sup>Zicon-</sup> verges almost surely to C∞<sup>(n,α)</sup> , when the batch size m tends to infinity, the result follows by inspection of the distribution of the empirical coverage Cm<sup>(n,α)</sup> in Theorem 1. 

## References 

> [1] V. Vovk, A. Gammerman, C. Saunders, Machine-learning applications of algorithmic randomness, in: Proceedings of the Sixteenth International Conference on Machine Learning, Morgan Kaufmann Publishers Inc., San Francisco, CA, USA, 1999, pp. 444–453. 

> [2] V. Vovk, A. Gammerman, G. Shafer, Algorithmic learning in a random world, Springer Science & Business Media, 2005. 

> [3] M. Fontana, G. Zeni, S. Vantini, Conformal prediction: A unified review of theory and new challenges, Bernoulli 29 (1) (2023) 1–23. 

> [4] H. Papadopoulos, K. Proedrou, V. Vovk, A. Gammerman, Inductive confidence machines for regression, in: T. Elomaa, H. Mannila, H. Toivonen (Eds.), Machine Learning: ECML 2002, Springer Berlin Heidelberg, Berlin, Heidelberg, 2002, pp. 345–356. 

> [5] J. Lei, M. G’Sell, A. Rinaldo, R. J. Tibshirani, L. Wasserman, Distribution-free predictive inference for regression, Journal of the American Statistical Association 113 (523) (2018) 1094–1111. 

> [6] V. Vovk, Conditional validity of inductive conformal predictors, Machine Learning 92 (2–3) (2013) 349––376. 

> [7] R. Hulsman, Distribution-Free Finite-Sample Guarantees and Split Conformal Prediction, Master’s thesis, University of Oxford (September 2022). 

> [8] A. N. Angelopoulos, S. Bates, Conformal Prediction: A Gentle Introduction, Foundations and Trends in Machine Learning 16 (4) (2023) 494–591. 

> [9] T. Hastie, R. Tibshirani, J. Friedman, The Elements of Statistical Learning: Data Mining, Inference, and Prediction, 2nd Edition, Springer, 2009. 

> [10] Y. Romano, E. Patterson, E. Cand`es, Conformalized quantile regression, in: H. Wallach, H. Larochelle, A. Beygelzimer, F. d'Alch´e-Buc, E. Fox, R. Garnett (Eds.), Advances in Neural Information Processing Systems, Vol. 32, Curran Associates, Inc., 2019, pp. 1–11. [11] P. C. Marques F., Code repository (2024). URL https://github.com/paulocmarquesf/coverage 

> [12] R Core Team, R: a language and environment for statistical computing, R Foundation for Statistical Computing, Vienna, Austria (2017). URL https://www.R-project.org/ 

> [13] M. J. Schervish, Theory of statistics, Springer Series in Statistics, 1995. 

6 

