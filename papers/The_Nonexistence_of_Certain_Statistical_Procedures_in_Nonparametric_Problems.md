# The Nonexistence of Certain Statistical Procedures in Nonparametric Problems

R. R. Bahadur e Leonard J. Savage, 1956. The Annals of Mathematical Statistics 27(4), 1115–1122.

Fonte: https://repository.ias.ac.in/27021/1/314.pdf

SHA-256 PDF: `cc3d6d5b43fa3b136daae5db8831fac12b0e1cbb17326d8087302ffc5139caca`. Acquisito 2026-09-14.

**Conversione:** OCR locale Apple Vision; formule e caratteri possono essere errati o omessi. Per gli enunciati prevale sempre il PDF; passaggi usati verificati visivamente. Non è una trascrizione matematica certificata.



## PDF page 1

THE NONEXISTENCE OF CERTAIN STATISTICAL PROCEDURES IN
NONPARAMETRIC PROBLEMS
By R. R. BAHADUR AND LEONARD J. SAVAGE
The University of Chicago
1. Introduction. It seems plausible that if the population distribution of a real
andom variable is entirely unknown, then a sample from the population cr
ield little or no information about the tails of the distribution, even if tl
sample is obtained according to a sequential procedure. This paper gives evi
tence supportineani some detai propens of inference concerning the popu-
ation mean u. It is shown that there is neither an effective test of the hypothes
hat u = O, nor an effective confidence interval for u, nor an effective poir
estimate of u. These conclusions concerning u flow from the fact that u is sensitive
to the tails of the population distribution; parallel conclusions hold for other
sensitive parameters, and they can be established by the same methods as are
here used for u.
It is also shown that there exists no confidence band for the population dis-
tribution function such that the upper and lower limits of the band are them-
selves distribution functions; that is, no confidence band fits very well.
2. Theorems. Let F be a given set of distribution functions F, G, ... of a real
variable. Some of the theorems to be proved would be of interest even if F were
required to be the class of all distributions or perhaps all distributions F' with
finite mean up. But it is helpful to recognize that the proofs require only that F
have a certain richness. Specifically, Theorem 1 and Corollaries 1 through 4
depend on the following three hypotheses:
(i) For every E & I, Mr = J-∞ z dE exists and is finite.
(ii) For every real m, there is an F & F with up = m.
(iii) F is convex; that is, if F = J, G ¿ F, a is a positive fraction, and H = IF +
(1 - T)G, then HE F.
Theorem 2 depends on hypotheses (iii) and the following:
(iv) F is closed under translation; that is, if F & J, and G(z) = F(z - h) for all
z and some h, then G & F.
(V) F is nonvacuous.
Some obvious examples of sets satisfying all four conditions are the sets of all
distribution functions F such that up is finite; the points of increase of F are a
bounded set, or are a finite set; F is absolutely continuous and dF /dz vanishes
Received October 11, 1955.
' Research sponsored in part by the Office of Naval Research.
1115
Institute of Mathematical Statistics is collaborating with JSTOR to digitize, preserve, and extend access to
The Annals of Mathematical Statistics. STOR
www.jstor.org

## PDF page 2

1116
R. R. BAHADUR AND LEONARD J. SAVAGE
outside of a bounded interval; as z approaches co, 1 - F(z) + F(- z) = 0(=")
for an r > 1.
Since the theorems to be proved are theorems of nonexistence, it is appropriate
that they be stated and proved for mixed (i.e., randomized) procedures-sampl
ing, estimating, testing. They are, of course, true a fortiori for the smaller class of
pure procedures. The technique of working with mixed procedures is presented in
detail in certain publications, for example [1] and [2). We feel free, therefore, to
handle mixed procedures rather informally, to save space and tedium.
Let X1, Xz, ... denote an infinite sequence of independent random variables,
each distributed according to F; that is, Pr(X; ≤ z) = F(z). Suppose that a
(randomized, sequential) sampling procedure is given, that is, a set of rules for
observing X1, X2, ... one by one up to a certain stage N such that at each
stage the decision whether to continue depends (randomly) on the observed
values in hand at that stage. The given procedure, which will remain fixed
throughout the discussion, is naturally assumed to be closed, that is,
(1)
P•(N < 00) = 1
for any event A defined on the sample space of V, Pr(A) will denote the proba-
bility of A when F obtains, that is to say, when each X; is distributed according
to F. If « is a real valued function of V, Erly] will denote the expected value of 4
(if it exists) when F obtains.
For any real number m, let Im denote the set of all Fe 5 with up = m.
THEOREM 1. For each bounded real valued function e on the sample space of V,
infrem Erlp] and suprem Erlel are independent of m.
The proofs of this theorem and of Theorem 2 below are postponed to the next
section. Theorem 1 states, in effect, that even if up is known to equal one of two
given values my and mr, the sample V cannot provide effective discrimination
between the two hypothetical values. The following Corollaries 1 through 4
exploit the close relations between discrimination, testing, and estimation to
make explicit some consequences of Theorem 1 in problems of inference con-
cerning up. As was mentioned in the introduction, analogues of Theorem 1
(and therewith of Corollaries 1 through 4) are valid for parameters other than the
mean, and these analogues can be proved by the same method as is used in the
next section to prove Theorem 1.
Let H be the hypothesis that up = 0 (i.e., E e Jo). For any test t, let Br(t) de-
note the probability of rejecting H in using t when F obtains, in short, the
test if B, = a for each F & Fo.
Taking y(V) to be the probability prescribed by t of rejecting H on observa-
tion of V yields this corollary.

## PDF page 3

CERTAIN STATISTICAL PROCEDURES
1117
CoroLLarY 1. If t is a somewhere unbiased level-a test of H, or a similar level-a
test of H, then B=(t) = a for all F EF.
Corollary 1 asserts the failure, in certain senses, of all tests of the value of u,
assuming that u exists. It would be interesting to know whether, in comparable
nonparametric situations, tests of the existence of u are equally unsuccessful.
To be precise, suppose for example that F is the set of all distribution functions.
Let g* be the subset of F on which up exists finitely, and let H* denote the hypo-
thesis that F is in I*. Then, does Corollary 1 hold with H replaced by H* and
"somewhere unbiased" replaced by "unbiased"?
Next, let I be a confidence set for u?, that is, l is a (randomized) function ot
V, that has Borel subsets of the real line for its values. For any real m, let C|m
denote the event that I covers m.
COROLLARY 2. If P. (Clurl) ≥ 1 - a for all F EF, then PrC|m]) ≥ 1 - a
for all m and all F = F.
ProoF. For each m, let pm(V) be the conditional probability of Cm] given V,
0 ≤ p ≤ 1. Consider a fixed m. By hypothesis, Ep|pm. ≥ 1 - a for f € Im. Hence,
P›C|m]) = Erlpm ≥ 1 - a for all F EF, by Theorem 1. Since m is arbitrary,
the corollary is proved
COrOLLARY 3. Suppose that there exists at least one F & F such that P-(I is a set
bounded from below) = 1. Then infpes (Pp(Cup])} = 0.
ProoF. For each n = 1, 2, ..., let Bn denote the event that I is contained in
the interval [—n, ∞), and let B, denote the complement of Bn. For each n, let
q» (V) denote the probability of Br given V; 0 ≤ 9n ≤ 9n+1 ≤ 1.
Now let F be a distribution in F such that I is bounded from below with
probability 1 when F obtains. By Lebesgue's theorem for monotone sequences,
E"[lim„qn] = lim» Ep(qn] = lim, P»(Br) = P›(I is bounded from below) = 1.
Consequently, lim, qn(V) = 1 except on a set of points V of Pr-measure zero.
Since, for any m < -n, pmV) = Pr(m = I | V) ≤ Pr(Bn| V) = 1 - qn(V), it
follows that, except on a Py-null set,
(2)
lim pm(V) = 0.
m→-∞0
Since Pr Clm)) = Erlp™| for all m, it follows from (2), by Lebesgue's theorem
for boundedly convergent sequences, that
(3)
lim Pp(Clm)) = 0.
Now, Corollary 2 states in effect that infect (PoClual): = infars
infm (PoC[m])). It follows from (3) that the common value of these infima is
zero. This completes the proof.
Of course, "set bounded from above," and, a fortiori, "bounded set" can be
substituted for "set bounded from below" in the statement of Corollary 3. But
the following example shows that it would not be enough to say "set bounded
from above or from below." For all V, let I = (- ∞, 0] with probability 4 and
I = (0, ∞) with probability ‡; then P-(C[m]) = } for all m and all F.

## PDF page 4

1118
R. R. BAHADUR AND LEONARD J. SAVAGE
Next, consider the problem of constructing a suitable point estimator for ur.
Let M be an estimator, that is, a real valued (randomized) function of V. Sup-
pose that when F obtains, the expected loss in using M is EL(M - Mp)] =
rp(M), where L(m) is bounded from below and limmoLm) = ∞ or limm--oo
Lm) = ∞ (e.g., L(m) = | m l, L(m) = m", L(m) = (2 + sin m)e™).
Let p(F) be a real valued functional on F. Say that p is uncontrollable (from
above) if there exists no real valued (randomized) function of V, say S, such that
infper |P= (p(F) < S)} > 0.
xpected loss r-(M) is bounded in F
any clue as to the possible expected loss.
COROLLARy 4. For any estimator M, ro(M) is uncontrollable.
ProoF. There is no loss in generality in assuming that limm-oLm) = ∞.
Replacing L(m) by L(m) - infa L(a), there is also no loss in assuming L non-
negative, with infm L(m) = 0. Consider a fixed estimator M. Write Lp =
L(M - Mp). Since Lp ≥ 0, it is easily seen (a la Tchebycheff) by considering the
cases ry = 0,0 < ry <0, and rp = a separately that PoLp ≤ arz) ≥ 1
- (1/a) for all a > 0 and all F.
Suppose, contrary to Corollary 4, that there exists a random variable S with
distribution determined by V, and a positive constant B, such that P (ry < S) ≥
B for all F & F. There is no loss of generality in assuming that S is always positive.
Choose and fix an a > 0 such that B - (1/a) > 0. Let Y = sup (m:L(m) ≤ as}
and define I to be the random interval [M - Y, ∞). Then Pp(I is bounded from
below) = 1 for each F. Also, for each F = F,
= PpLe ≤ aS)
= P•(Lp ≤ aS, rp < S)
= P(Lp Earp, Ip <S)
≥ Pp(Lp ≤ arz) + PP(Tr <S) - 1
≥ 1- (1/a) +B-1
> 0.
This contradiction to Corollary 3 establishes Corollary 4.
The preceding proof consists in showing that if M is an estimator such that
r›(M) is controllable, then up is controllable, contrary to Corollary 3. This
argument can also be used to show the uncontrollability of certain parameters.
Simple examples of such parameters are the variance of F, the difference between
the mean and median values of F, and the supremum of the points of increase of
F. Note that while the unboundedness of these parameters is evident when
assumptions such as (iii) and (iv) hold, verification that they are uncontrollable
is less trivial even in the case when V consists of a single observation.

## PDF page 5

CERTAIN STATISTICAL PROCEDURES
1119
Finally, let A (z) be a (randomized) function of V taking values in the set of all
distribution functions of z. Let C*[F] denote the event that A(z) ≥ F(z) for
THeorem 2. infret |P-(C*[F])} = 0.
Application of Theorem 2 to - X; yields with little effort a similar theorem,
dual to Theorem 2, concerning the probability that A(2) ≤ F(z) for all z.
Obviously these two theorems together imply a two-sided version of Theorem 2.
3. Proofs of the theorems. The proofs of the theorems depend on the fact that
a given distribution function F can be so modified that, while the probability
distribution of the X/s (and therewith of V) is perturbed only slightly, para-
meters such as the mean suffer arbitrary displacements. This modification is
described in the following paragraphs, before undertaking the proofs of Theorems
1 and 2.
Let $ denote the class of all functions y of V with 0 ≤ y ≤ 1, and (for any
two distribution functions F and G) define the familiar absolute-variational
distance between F and G by
(1)
ô(F, G) = sup |Erle) -Ealell.
Given F, let I be an arbitrary distribution function and a an arbitrary con-
stant, 0 < m < 1, and define the distribution function G thus:
(5)
G (2) = TF (2) + (1 - T)H(z).
The following lemma shows that if the given sampling procedure is closed for
F in the sense of (1), and if m is sufficiently close to 1, then, no matter what H
may be, the probability distributions of V under F and G are not very distant
from one another. It may clarify the meaning and proof of the lemma to remark
that it is for this application of the lemma, not for the lemma itself, that the
sampling procedure must be closed for F.
LEMMA. (F, G) ≤ 1 - T'P› (N ≤ li) for each positive integer k.?"
PrOoF. Choose and fix a positive integer k. Let R*) denote the space of all
points z") = (21, 22, ..., *) with - ∞ < %; < ∞ for i = 1,2,., k. For any
univariate distribution function F(z), write F(z") = |li- F(zi).
It will be shown first that if F and G are related according to (5), then, for any
nonnegative function f on R*)
(6)
To verify this inequality, let YI, Y2, '.., Ye, 21, Za, •..
, Zu, and U1,
Uz, ..., Uk be independent random variables such that each Y; is distributed
according to F, each Z; according to H, and P(U, = 1) = 1 - P(U, = 0) = T
rlier version of the lemma, a
Tor ver in ualite l amma, aong ide able i somemat sin tar. one apondis arning in te
to Professor W. Hoeffding for these improvements.

## PDF page 6

1120
R. R. BAHADUR AND LEONARD J. SAVAGE
for each Ui. Write W: = ViY; + (1 - Vi)Z; for i = 1,2, ... , k. Then Wi:
W2,...
Wx are independent random variables, each distributed according te
G as defined by (5). Let B denote the event that U, = 1 for all i = 1,2, ..., l
and let B denote the complement of B. Now it is straightforward to show (6);
thus,
(7)
= P(B)ELf(W,,..,Wx) | B] + P(B)E|JW1,...,Wx) | B)
≥ P(B)ELJW1, ...,Wk) | B)
= *ELf(Y1, ...,Yx) | B]
= т* ).
Consider the space of all sequences X®) = (X1, X2, ... ad inf). Since V, the
observed sample, is by definition a (randomized) function of X*)
to speak of the conditional distribution of V given X" = (X1,..., Xx). It
follows from a well known property of conditional expectation that, for any
function h(V) and any F,
(8)
R(k)
provided that Er|h] exists.
Next, let & be a function of V such that 0 ≤ 4 ≤ 1. Define 4(V) = 1 if N ≤ k
and #(V) = 0 if N > k. It is easy to see that there exists a function f on R*)
such that 0 ≤ J ≤ 1, and
(9)
for all F. The function f depends, of course, on the given y and the given sampling
procedure.
Suppose, now, that F and G are two distribution functions related according
to (5). Then,
Edly] ≥ Eale-V
=/
р (k)
=/.
R (k)
Eolp-$| X"'] aG«)
by (8)
by (9)
by (6)

## PDF page 7

CERTAIN STATISTICAL PROCEDURES
1121
by (9)
by (8)
R (k)
= Erle] - Erls (1 -т#)]
≥ Elp] - E[1 - ***]
= Erle) - 1 + *P,(N ≤ k).
Thus,
(10)
Er(p)-Eole] ≤1-T*P,(N ≤k)
for all y in $. Since « ¿ $ implies 1 - 4 &$, it follows from (10) that
(11)
-Exle) +Eale] ≤ 1- T*P,(N ≤ k)
for all 4 in . In view of (10), (11), and the definition (4) of 8, 8(F, G) ≤ 1-
т"P-(N ≤ k) for all k, as was to be proved.
PROOF OF THEOREM 1. Let m and m' be real numbers, and let e > O be given.
Consider a fixed F in Im. Choose and fix a positive integer k such that
(12)
P•(N > k) < e.
The existence of such a k is assured by (1). Now choose and fix & i such that
0 < 7 < 1 and
(1:3)
(1 - **) < є.
Let Il be a distribution function in F such that am + (1 - T)мн = m' (see
assumption (ii)), and let G be defined by (5). Then, by assumption (ili), G is in
F, and since Mo = Tur + (1- T)u = m', G is in Im'. Since 1 - *'P›(N ≤ k) ≤
(1 -т") + P›(N > li), it follows from (12), (13), and the Lemma that (F, G) <
Since e and F' are arbitrary, infacm. (8(F, G)} = 0 for each F € Im. In other
words, Fm' is everywhere dense in Im, under the metric ô. Since m and m' are
arbitrary, it follows (see assumption (i)) that, for each m, Im 1s everywhere dense
in F. This conclusion, together with the observation that Ep(p] is continuous in F
for any bounded 4, yields Theorem 1.
PROOF oF THEOreM 2. Before the proof proper we present a line of argument
that may be of some interest in suggesting a heuristic connection between this
theorem and Theorem 1, though this line of argument makes assumptions that
are actually gratuitous. It assumes in fact that (i) obtains and that, for some
I', the mean of A almost always exists and is finite.
Suppose, then, that the random distribution function A is such that, for some
(14)

## PDF page 8

1122
R. R. BAHADUR AND LEONARD J. SAVAGE
except for a Py-null event. Define I = IS®∞* dA, 0) whenever (14) is satisfied,
and 1 = (- ∞, ∞) otherwise. Now, the event A(z) ≥ F(z) for all z (that is,
C*[F]) implies the event co > u* ≥ Jz dA (that is, Clur]) provided only that
My exists and is finite. Hence P>(C*[F]) ≤ P»(Clup]) for each F & F. The desired
conclusion now follows from Corollary 3.
Now, dropping the assumptions (i) and (14), turn to the proof proper. Choose
and fix an e, 0 < € < 1, and an F & F such that F(0) > 0. The existence of
such an F is assured by assumptions (iv) and (v). For each z, let J (z) = inf
{u:PrA (2) ≤ u) ≥ 1 - €). It is not difficult to see that J is a nondecreasing
function of 2, with lim,.- J(z) = 0, limo J (z) = 1, and that J is also con-
tinuous from the right, so that it is actually a distribution function. Also,
(15)
PYA(2) > J (z)} ≤ €
for each 2.
Now choose k such that (12) holds, choose i such that (13) holds, and choose
1 such that J (A) < (1 - )F(0). Let G be defined by (5), with H(z) = F(z - 1).
Then G is in 5, by assumptions (iii) and (iv), and
(16)
(17)
by the choice of 1 and the definition of G. Hence
Po(C*[G)) = Po(A(z) ≥ G(z) for all z)
≤ Po(A(A) ≥ G(X))
≤ Po(A (1) > J(A))
≤ P›(A(A) > J(A)) + P›(N > k) + (1 -т*)
by (16)
by the lemma
≤ 3€
by (12), (13), (15).
Since e is an arbitrary positive fraction, the theorem is proved.
The proof of Theorem 2 does not use quite the full force of (iii) and (iv).
It is enough that for some F & 5 and two sequences of numbers a: (0 ≤ a; < 1)
and B;, such that ai → 1 and B; → ∞, the distributions Gij such that
(18)
Gü(z) = aiF(z) + (1 - ai)F(z + Bi)
are in F. For the dual of Theorem 2, it is required instead that B; → -∞.
REFERENCES
[|| A. DVORETZKY, A. WALD, AND J. WOLFOWITZ, "Elimination of randomization in certain
statistical decision procedures and zero sum two-person games," Ann. Math.
Stat., Vol. 22 (1951), pp. 1-21.
[2] ABRAHAM WALD, Statistical Decision Functions, New York, John Wiley and Sons, 1950.