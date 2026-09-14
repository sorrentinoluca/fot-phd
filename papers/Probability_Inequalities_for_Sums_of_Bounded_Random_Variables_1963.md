# Probability Inequalities for Sums of Bounded Random Variables

Wassily Hoeffding, 1963. Journal of the American Statistical Association 58(301), 13–30.

Fonte: https://www.cs.rpi.edu/academics/courses/spring06/random/hoefding.pdf

SHA-256 PDF: `3021bcc097ef23a99a84d0eef8dcce2fd835c71df79a105727d3e03f8f0b8930`. Acquisito 2026-09-14.

**Conversione:** OCR locale Apple Vision; formule e caratteri possono essere errati o omessi. Per gli enunciati prevale sempre il PDF; passaggi usati verificati visivamente. Non è una trascrizione matematica certificata.



## PDF page 1

Probability Inequalities for Sums of Bounded Random Variables
Wassily Hoeffding
Journal of the American Statistical Association, Volume 58, Issue 301 (Mar., 1963),
13-30.
Stable URL:
http://links.jstor.org/sici?sici=0162-1459%28196303%2958%3A301%3C13%3APIFSOB%3E2.0.C0%3B2-D
29
STOR
Your use of the JSTOR archive indicates your acceptance of JSTOR's Terms and Conditions of Use, available at
http://www.jstor.org/about/terms.html. JSTOR's Terms and Conditions of Use provides, in part, that unless you
have obtained prior permission, you may not download an entire issue of a journal or multiple copies of articles, and
you may use content in the JSTOR archive only for your personal, non-commercial use.
Each copy of any part of a JSTOR transmission must contain the same copyright notice that appears on the screen or
printed page of such transmission.
Journal of the American Statistical Association is published by American Statistical Association. Please contact
the publisher for further permissions regarding the use of this work. Publisher contact information may be obtained
at http://www.jstor.org/journals/astata.html.
Journal of the American Statistical Association
©1963 American Statistical Association
JSTOR and the JSTOR logo are trademarks of JSTOR, and are Registered in the U.S. Patent and Trademark Office.
For more information on JSTOR contact jstor-info@umich.edu.
©2002 JSTOR
http://www.jstor.org/
Tue Jun 11 11:16:34 2002

## PDF page 2

PROBABILITY INEQUALITIES FOR SUMS OF BOUNDED
RANDOM VARIABLES'
WASSILY HOEFFDING
University of North Carolina
Upper bounds are derived for the probability that the sum S of n
independent random variables exceeds its mean ES by a positive num-
ber nt. It is assumed that the range of each summand of S is bounded
or bounded above. The bounds for PriS-ES≥nt} depend only on
the endpoints of the ranges of the summands and the mean, or the
mean and the variance of S. These results are then used to obtain
analogous inequalities for certain sums of dependent random variables
such as U statistics and the sum of a random sample without replace-
ment from a finite population.
1. INTRODUCTION
Ter X 1, Xz,:.., In be independent random variables with finite first and
d second moments,
S= XIt... +Xn,
X = S/n,
u = EX = ES/n,
o'=n var(X) = (varS)/n.
(1.1)
(1.2)
(Thus if the X, have a common mean then its value is u and if they have a com-
mon variance then its value is o?.) In section 2 upper bounds are given for the
probability
Pr{X-M >1} = PriS - ES ≥ nt},
(1.3)
where t>0, under the additional assumption that the range of each random
variable X; is bounded (or at least bounded from above). These upper bounds
depend only on t, n, the endpoints of the ranges of the Xi, and on u, or on u
and o. We assume t> 0 since for t ≤ 0 no nontrivial upper bound exists under our
assumptions. Note that an upper bound for Pr |X-ut} implies in an ob-
vious way an upper bound for Pr {- I+m≥t} and hence also for
(1.4)
Known upper bounds for these probabilities include the Bienaymé-Cheby-
shev inequality
(1.5)
nt
Chebyshev's inequality
1
(1.6)
nt?
1+
1 This research was supported by the Air Force Office of Scientific Research.
= Inequality (1.6) has been attributed to various authors. Chebyshev [14] seems to be the first to have an-
nounced an inequality which implies (1.6) as an illustration of a general class of inequalities.
13

## PDF page 3

14
AMERICAN STATISTICAL ASSOCIATION JOURNAL, MARCH 1963
(which do not require the assumption of bounded summands) and the in-
equalities of Bernstein and Prohorov (see formulas (2.13) and (2.14)). Surveys
of inequalities of this type have been given by Godwin [6], Savage [13], and
Bennett [2]. Bennett also derived new inequalities, in particular inequality
(2.12), and made instructive comparisons between different bounds.
The method employed to derive the inequalities, which has often been used
(apparently first by S. N. Bernstein), is based on the following simple ob-
servation. The probability Pr {S-ES≥nt) is the expected value of the fune-
tion which takes the values 0 and 1 according as S-ES-nt is <0 or 20.
This function does not exceed exp {h(S-ES-nt)}, where h is an arbitrary
positive constant. Hence
Pr|X-M ≥1} = Pr{S - ES ≥ nt} ≤ Eeh(s-Es-ne).
(1.7)
If, as we here assume, the summands of S are independent, then
(1.8)
It remains to obtain an upper bound for the expected value in (1.8) and to
minimize this bound with respect to h. The bounds (2.1) and (2.8) of Theorems
1 and 3 are the best that can be obtained by this method under the assump-
tions of the theorems. They are not the best possible bounds for the probability
in (1.7). The bounds derived in this paper are better than the Chebyshev
bounds (1.5) and (1.6) except for small values of t or small values of n. Typi-
cally, if t is held fixed, they tend to zero at an exponential rate as n increases.
The bounds of Theorems 1 and 3 are compared in section 3. The proofs of
the theorems are given in section 4.
In section 5 the results of the preceding sections are used to obtain prob-
ability bounds for certain sums of dependent random variables such as U
statistics and sums of m-dependent random variables. In section 6 a relation
between samples with and without replacement from a finite population is
established which implies probability bounds for the sum of a sample without
replacement.
The following facts about convex functions will be used; for proofs see refer-
ence [7]. A continuous function f(x) is convex in the interval I if and only if
f(px+(1-p)y) ≤pf(x) + (1-p)f(y) for 0<p<1 and all x and y in I. If this is
true for all real x and y, the function is simply called convex. A continuous
function is convex in I if it has a nonnegative second derivative in I. If f(x) is
continuous and convex in I then for any positive numbers p1, •••, PN such
that pit... †PN =1 and any numbers 21, •••, aN in I
, Pif(xi).
(1.9)
This is known as Jensen's inequality.
& By the best possible bound for the probability in (1.7) is meant the least upper bound which depends only
on t, n, the endpoints of the ranges of the Xi, and u (or u and o). Approximations for the probability in (1.7) which
involve the upper bound in (1.7) (minimized with respect to h) have been considered by several authors; see, in
particular, Bahadur and Rao (1], where references to earlier work can be found. The present paper is concerned
with exact bounds, not with approximations for the probability.

## PDF page 4

PROBABILITY INEQUALITIES FOR SUMS
15
2. SUMS OF INDEPENDENT RANDOM VARIABLES
In this section probability bounds for sums of independent random variables
are stated and discussed. The proofs are given in section 4.
Let X1, Xz,..., In be independent random variables and let S, X, u, and
o' be defined by (1.1) and (1.2). First we consider bounds which do not depend
on o.
Theorem 1. If X1, X2, .., In are independent and 0≤X: ≤1 for i=1, ...,
n, then for 0<t<1-4
Pr{X-M ≥t}
≤ e-nio (4)
≤ e-2ne?
(2.1)
(2.2)
(2.3)
where
9(4) = -
- In
1 - 4
1 - 2u
for 0 < " <
(2.4)
g (м) =
for - ≤u < 1.
2u (1 - 4)
The assumption 0≤ X; ≤1 has been made to give the bounds a simple form.
If instead we assume a ≤ X: ≤6, the values u and t in the three upper bounds of
the theorem are to be replaced by (u- a)/(6- a) and t/(b-a), respectively.*
If t>1-u, then under the assumptions of Theorem 1 the probability in
(2.1) is zero. Inequality (2.1) remains true for t=1 - u if the right-hand side
is replaced by its limit as t tends to 1-u, which is u". In this special case the
sign of equality in (2.1) can be attained. Indeed, if t=1-M, then Pr {X-"≥t}
=Pr/X=1}=PrfS=n}, and Pr{S=n} =u" if
Pr|X;= 0}=1-M, Pr|X; = 1} =m, i=1,...
, n,
(2.5)
that is, if S has the binomial distribution with parameters n and u.
The bound in (2.1) is the best that can be obtained from inequality (1.7)
under the assumptions of the theorem. Indeed, it is the minimum with respect
to h of the right-hand side of (1.7) when the X; have the distribution (2.5).
For the special (binomial) case (2.5) the inequalities of Theorem 1 ex-
cept for (2.2) with u<‡) have been derived by Okamoto [11]. Inequality
• The following remarks are based on a referee's comments. If in Theorem 1 the assumption Xi ≤1 is dropped
that is, if it is only assumed that the Xi are non-negative with finite means, then Markov's inequality Pr {*-"≥1)
≤#/(u+t) cannot be improved upon. (The bound is attained if Xi takes the values 0 and n(u+t) with respective
probabilities t/(utt) and «/(utt), and X2=..• =Xn =0 with probability one.) Thus the assumption that the
Xi are bounded on both sides is crucial to getting any improvement over Markov's bound. (The improvement
takes place when n and t are not too small.) Similarly, in Theorem 3 the assumption Xi ≤b is crucial to getting
any improvement over the Chebyshev bound (1.6).—Further improvements could be obtained by using, instead
over the bounds of Theorem 1.

## PDF page 5

16
AMERICAN STATISTICAL ASSOCIATION JOURNAL, MARCH 1963
(2.1) for the binomial case is implicitly contained in Chernoff's paper 3,
Theorem 1 and Example 5].
The following theorem gives an extension of bound (2.3) to the case where
the ranges of the summands need not be the same.
Theorem 2. If X1, X2, •.., An are independent and ai ≤X: ≤bi (i= 1,2, ....,
n), then for t>0
Pr{X-M t} ≤e-2n21212"i=(bi-ai)?
(2.6)
As an application of Theorem 2 we obtain the following bound for the dis-
tribution function of the difference of two sample means.
Corollary. If Y1, .., Ym, Z1,
••, Ln are independent random variables
with values in the interval [a, b],
and if Y=(YIt... +Ym)/m, Z= (Z1
+... +/n/n, then for t>0
(2.7)
The inequalities of the next theorem depend also on the variance o2/n of X.
We now assume that the X, have a common mean. For simplicity the mean is
taken to be zero.
Theorem S. If X1, Xz, .., X, are independent, EX; =0, X: ≤6(i= 1,2,....,
n), then for 0<t<6
Pr/X≥ t} ≤
(2.8)
≤ e-(nt/b)I(170 166) In (1151/03-11,
(2.9)
Here the summands are assumed to be bounded only from above. However,
to obtain from this theorem an upper bound for Pr{| X| ≥t}, we must assume
that the summands are bounded on both sides.
Inequality (2.8) is the best that can be obtained from (1.7) under the present
assumptions. It is the minimum with respect to h of the right-hand side of (1.7)
when the X; have the distribution
Pr{X--5}
62
63+03 2=1,...,n. (2.10)
Inequality (2.8) is true also for t=b if the right-hand side is replaced by its
limit as t tends to b, which is [o/(62 + 02) ]". In this case the sign of equality in
(2.8) is attained when the distribution is (2.10).
The bound (2.9) is due to Bennett (2, inequality (8b)). (Bennett's nota
ion is different from mine. His first proof assumes |X, ≤6(= his M), a secon‹
proof (pp. 42-3) uses only X.≤b.)
If we let
bt
1 = -
nt
(2.11)
Bennett's inequality (bound (2.9)) can be written

## PDF page 6

PROBABILITY INEQUALITIES FOR SUMS
m(2) = (1+→) In(1+X) -1.
Bennett has shown that (2.12) is better than Bernstein's
h2(1) =
2(1+1)
Inequality (2.12) is also better than Prohorov's [12]
17
(2.12)
(2.13)
(2.14)
h3(1) =
- arcsinh
Indeed, it can be shown that the bound in (2.12) is the best bound of the form
exp (- Th(1)) that can be obtained from (2.8) and hence from (1.7). If \ is
small, Bernstein's bound (2.13) does not differ much from Bennett's (2.12).
Under certain conditions X is approximately normally distributed when n is
large, so that, for y= Vn t/o fixed,
PriX-u ≥1
ts = Pr
X-u>
e-*12dx =Ф(-y) (2.15)
as n→. (Sufficient conditions are no'→∞ and ZE X-EX, /(oVn) →0.)
It is instructive to compare the present bounds with the upper bound for $(- Y)
which results from inequality (1.7) when X is normally distributed. In this
case the right-hand side of (1.7) is exp(-hnt+2ºno'/2). If we minimize with
respect to h we obtain
≤ 0-712120°
(2.16)
o1 Ф(-У) ≤exp(- y2/2), where y >0. This bound for $(-y) is rather crude,
especially when y is large, in which case $(- y) is approximated by
= exp(-y'/2).
In contrast, the bounds (2.1) and (2.8) are attainable at the largest nontrivial
values of t. It is interesting to note that the bound (2.2) with «≥}, is equal to
the right-hand side of (2.16) in the binomial case (2.5). The bound (2.6) of
Theorem 2 is equal to the right-hand side of (2.16) in the case where Pr {X; = ai}
=Pr |X;=bi} =}, for all i. Bernstein's bound (2.13) is close to the right-hand
side of (2.16) when \ =bt/o' is small. The same is true of the bounds of Theorem
3.
The inequalities of this section can be strengthened in the following way.
Let Sm=Xit... +Xm for m=1, 2,...,n. It follows from a theorem of
Doob, I7, p. 314] that
Pr{ max (Sm-ESm) >nt} ≤ Eeh(5n-B5n-n1)
(2.17)
1≤m≤n

## PDF page 7

18
AMERICAN STATISTICAL ASSOCIATION JOURNAL, MARCH 1963
for h >0. The right-hand side is the same as that of inequality (1.7) (where
S=Sn). Since the inequalities of Theorems 1, 2, and 3 have been obtained from
(1.7), the right-hand sides of those inequalities are upper bounds for the prob-
ability in (2.17) under the stated assumptions. This stronger result is analogous
to an inequality of Kolmogorov (see, e.g., Feller [5, p. 220]).
Furthermore, the inequalities of Theorems 1 and 2 remain true if the as-
sumption that X1, X2, •.•, In are independent is replaced by the weaker
assumption that the sequence Sm' = Sm- ESm, m=1, 2, ••.,n, is a martingale,
that is,
E(Sm S1...,S3) = S; 1≤j≤m≤n,
(2.18)
with probability one. Indeed, Doob's inequality (2.17) is true under this as-
sumption. On the other hand, (2.18) implies that the conditional mean of Xm
for S'm-1 fixed is equal to its unconditional mean. A slight modification of the
proofs of Theorems 1 and 2 yields the stated result.
3. COMPARISON OF BOUNDS
Theorem 1 gives three bounds, each weaker but simpler than the preceding.
Similarly, the second bound of Theorem 3 is weaker but simpler than the first
bound. It is of interest to know under what circumstances the simpler bounds
are close to the more complicated ones and in what cases the latter are appre-
ciably better than the former. We may say that two bounds are appreciably
different if their ratio is not close to 1.
The inequalities of Theorem 1 can be written
Pr{X-u>t} ≤ A1≤Az≤A3,
where
A1 = e-n20(1.4),
A2 = e-neo (4),
A3 = e-int?
1- 1)
(3.1)
(3.2)
(3.3)
(3.4)
1 - 4
9 (м) =
- In —
1 - 2u
9 (м) =
21(1-1)
for 2 = 1 <1.
The bounds A2 and As are easily compared by inspection. In particular,
Az= As if and only if u = 4.
We now compare A1 and Ar. If t≤u as well as t<1 - u, we have the conver-
gent expansion
6(1) =2
н=/
+ 34(2 - 4) + 12)
(3.5)

## PDF page 8

PROBABILITY INEQUALITIES FOR SUMS
19
If u≥} (in which case the series converges for all t, 0<t<1-u), then the
first term on the right is equal to g(u) and all coefficients are non-negative.
Hence the first non-vanishing term in the expansion of G(t, M) - 9(u) yields a
lower bound. An upper bound can be obtained by noting that the coefficient
of th with k≥1 does not exceed
1
2
2.3 (1 - 11)6+1
Hence the expansion is majorized by a geometric series. In the case u = , the
coefficients of odd powers of t are zero and we get a better upper bound by a
similar method. In this way we obtain
301-4111-1-5-1
A1 < exp
6н (1 - м) ?)
if u > ½ (3.6)
exp
4tn
A1
3(1 - 4t2)/
<- =
A2
#< exp{
A3
if M = 2 (3.7)
If the right-band sides of (3.6) and (3.7) are not close to 1, the first bound
is appreciably better than the second. If the left-hand sides are close to 1, then
the simpler second bound is almost as good as the first.
1 < 2
then g(u) <
2u(1 - 4)
Hence if t/u is so small that the first term in the expansion (3.5) approximates
G (t, 4), then A / As is close to 1 when
(241-07-040 Pe
is small. Furthermore, we have A1= A2 if t=1-2u. In fact, we have the
identity
1[G(t, u) - g(м)] = (1- 2u-1) |G(1 - 2M-t, M) - 9(4)].
The elementary inequality Inx ≤x- 1 implies
(3.8)
G (1 - 2u - t, M) <
м (1 - м)
and
g (м)
Hence
A1
+0-181-24-1714702
if u <
2
(3.9)

## PDF page 9

20
written as
AMERICAN STATISTICAL ASSOCIATION JOURNAL, MARCH 1988
Now consider the inequalities (2.8) and (2.9) of Theorem 3. If they are
(3.10)
the ratio By/Bz can be expressed in the form
(3.11)
where
bt
u=-
btto?
20 = 6'
p(V) + p(w)
ф(О, W) = 20 -
01+ w1-1'
(x) =x-<{(1-х)In(1-х)+x—·x2}
(3.12)
(3.13)
- x + -
-x=+-
-x3+....
(3.14)
2.3
3.4
4.5
Since 0<t<b, both v and w are between 0 and 1. We have p(x) <x/2 for x<1.
Hence p(v) <Ju <bt/o' and p(w) <Et/b. It follows that $(0, w) <1/(260") and
B1
Bz
> exp (-"
2607)
(3.15)
In a similar way, using p(x) >x/6, we can obtain a lower bound for B1/Br.
In particular, if bt/o? is small, so that u may be approximated by bt/o, then
B1/Br is approximately equal to exp-nt/ (6bo?).
The relation between Theorems 1 and 3 is as follows. If the assumptions of
Theorem 3 are satisfied and the X, are also bounded from below, a ≤X:≤6
(where a <0<b), then, since EX; =0 and Xi-a≥0, we have EX=EX (Xi-a)
≤ Bb (Xi-a) = -ab, and hence o'≤ - ab. It is not difficult to show that the
bound in (2.8) is an increasing function of o?. If we replace o by its upper
bound - ab, we obtain from (2.8) the inequality which results from (2.1) when
the appropriate substitutions mentioned after the statement of Theorem 1
are made. Thus (2.8) implies (2.1), but Theorem 1 does not require the as-
sumption that the X; have a common mean.
In the same way we can obtain from (2.9) a bound which depends on a but
not on o; however, it is not simpler than the better bound corresponding to
(2.1).
4. PROOFS OF THE THEOREMS OF SECTION 2
Let X be a random variable such that a ≤X ≤6. Since the exponential func-
tion exp(h) is convex, its graph is bounded above on the interval a ≤X≤6
by the straight line which connects its ordinates at X= a and X=b. Thus
X - a
eX ≤
- era t-
6 - a
- ehb
a ≤ x ≤b.
6 - a
(4.1)

## PDF page 10

PROBABILITY INEQUALITIES FOR SUMS
21
Hence we obtain
Lemma 1. If X is a random variable such that a ≤X ≤b, then for any real
number h
6 - EX
EX - a
Eeht ≤
- ena + —
b - a
6 - a
We now prove Theorem 1. By (1.7) and (1.8) we have for h>0
(4.2)
(4.3)
By assumption 0≤X:≤1. Let Mi=EX; Then nu=Mituzt... +Mn. By
Lemma 1 with X= Xi, a = 0, 6=1, we have
(4.4)
Since the geometric mean does not exceed the arithmetic mean,
{I (1 - 1s + 148))
+ 11-47149) =1-1+40
(4.5)
It follows from (4.3), (4.4), and (4.5) that
Pr{X -M ≥ t} ≤ 10-11-nu(1 - 1 t men)}".
(4.6)
The right-hand side of (4.6) attains its minimum at h = ho, where
(1 - м) (м + t)
ho = In
(4.7)
(1 - м - t) н
Since 0<t<1 -u, ho is positive. Inserting h = ho in (4.6) we obtain inequality
(2.1) of Theorem 1.
To prove inequality (2.2) we write the right-hand side of (2.1) in the form
exp(- ntG(t, u)) (as in (3.2)), where
uT t
uTt
1 - u - t
1 - u - t
G(t, M) =
- In -
- +—
- In
(4.8)
1 - 4
Inequality (2.2) will be proved by showing that g(u) as defined in (2.4) is the
minimum of G(t, u) with respect to t, where 0≤t<1-u. The derivative aG(t,
1) / at can be written in the form
41).
(4.9)

## PDF page 11

22
AMERICAN STATISTICAL ASSOCIATION JOURNAL, MARCH 1963
where H(x)=(1-2x1)In(1-x). By assumption 0≤t/(u+t) <1 and 0≤t/
(1 - 4) <1. For |x, <1 we have the expansion
(4.10)
where the coefficients are positive. Thus H (x) increases for 0<x<1. It follows
from (4.9) that aG/at>0 if and only if t/ (1-u)>t/(u+t), that is, t>1-2u.
Hence if 1- 2u> 0, G(t, 4) has its minimum at t=1 - 2u and the value of the
minimum is
If 1- 2u ≤0, then G(t, u) has its minimum at t=0 and the value of the mini-
mum is 1/[2u(1-4)] = g(u) (see (3.5)). This proves inequality (2.2).
It is easily seen that g(u) ≥g(½) = 2. This implies inequality (2.3). The proof
of Theorem 1 is complete.
We next prove Theorem 2. The proof will also indicate a short direct deriva-
tion of the simple bound (2.3).
In Theorem 2 we assume a: ≤X, ≤b;. Let again Mi= EX; By (1.7) and (1.8),
Pr{X-M ≥ t} ≤ ehne I| Een(x,-4i).
i =1
(4.11)
By Lemma 1,
Eeh(ti-Hi) ≤ e-hui
Di - Mi
Mi - Ai
— ehai +
b: - ai
bi - ai
(4.12)
where
L(hi) = -hipi+In(1 - pit pieni),
Mi - di
hi = h(bi -ai),
pi=
b: - ai
The first two derivatives of L(hi) are
(4.13)
(4.14)
pi(1 - pi)e hi
L'" (hi) =
[(1 - pi)e-hi + pil?
The last ratio is of the form u(1-u) where 0<u<1. Hence L"(hi) ≤*. There-
fore by Taylor's formula
(hi) ≤ I (0) + L'(0)h; + 5h3 = 5h3 = 5h°(bi - ai)?
(4.15)
Hence by (4.12)
Een(ti-Hi) ≤ eth"(bi-ai)?
(4.16)

## PDF page 12

PROBABILITY INEQUALITIES FOR SUMS
and by (4.11)
23
Pr{X-M ≥t} ≤e-hn1t81227=s(bi-ai).
(4.17)
The right-hand side of (4.17) has its minimum at h= 4nt/ Z (bi-ai)? Insert-
ing this value in (4.17) we obtain inequality (2.6) of Theorem 2.
To prove Theorem 3 we need two lemmas.
Lemma 2. If X is a random variable such that EX=0, EX'=o? and X≤b,
then for any positive number h
(4.18)
62+o
A proof of this inequality can be found in Bennett [1].
Lemma 3. If c>0, the function
5(0) = 172
has a negative second derivative for u ≥0.
To prove this we write f(u) =c+ In fi(y), where y =1 +u and
(4.19)
For the second derivative f''(u) we have fi (y)f" (u) = fı(Y)f1"(Y) - (fí(y))?. Now
61(9) = (-52-(51)e-c+y3,
fl'(3)= (2y:+204-2+033-1)e-ou-2y-3
which is negative for cy >0. Since fi(y) >0 for y > 1, it follows that f"(u) <0
for u >0.
We now can prove Theorem 3. By assumption, EX;=0 and Xi≤b. Let
03=EXi, so that no'=ơi tot... +ơn By (1.7), (1.8) and Lemma 2,
Pr{X ≥ t} ≤e-hme II
163+030-101611+
62+0?
=e-Int+Is (63189,
(4.20)
where f is the function defined by (4.19), with c=bh. Since, by Lemma 3, f(u)
has a negative second derivative, - f(u) is convex for u ≥0. Therefore by
Jensen's inequality (1.9)
= In
(0702868030
62+o?
If follows from (4.20) and (4.21) that
Pr{X≥1} ≤
b: +028-087031624t=
(4.21)
(4.22)

## PDF page 13

24
AMERICAN STATISTICAL ASSOCIATION JOURNAL, MARCH 1963
The right-hand side of (4.22) attains its minimum at h= hi, where
tb
1+-
h1 =
- In -
62+0
•
1-6
Inserting this value in (4.22), we obtain inequality (2.8) of Theorem 3.
Inequality (2.9) follows from equations (3.13) to (3.16). The proof of
Theorem 3 is complete.
As noted above, the upper bound (2.9) for Pr (X≥t) has been derived by
Bennett (2]. An alternative direct proof goes as follows. By Lemma 3, it u>0,
then f"(u) <0 and hence f(u) ≤f(0) +f' (0)u= (e°-1-c)u. Applying this in-
equality to the right side of (4.20) (where c=bh) and minimizing with respect
to h we obtain the bound (2.9).
5. SUMS OF DEPENDENT RANDOM VARIABLES
The inequalities of sections 2 and 4 can be used to obtain probability bounds
for certain sums of dependent random variables. Suppose that T' is a random
variable which can be written in the form
I=pIIt. paIz+... + PNIN,
(5.1)
where each of T1, I2, •.., Tv is a sum of independent random variables and
PI, P2, •.•, Pu are nonnegative numbers, pıtpzt•.• +PN=1. The random
variables T1,
Ir,..., In need not be mutually independent. For h>0
PriT ≥ t} ≤ e-hEehT.
Since the exponential function is convex, we have by Jensen's inequality (1.9)
2 p: exp(hT:).
Therefore
(5.2)
Since each T; is a sum of independent random variables, the expectations on
the right can be bounded as in section 4. If the random variables 1; are identi-
cally distributed or if the upper bound for E exp (h(Ti-t)) is independent of i,
then the upper bound we obtain for Pr {T≥t} is also an upper bound for
Pr {Ti≥t). The bounds obtained in this way will be rather crude but may be
useful.
We now consider several types of random variables I which can be repre-
sented in the form (5.1).
5a. One-sample U statistics. Let X1, X2, .., Xu be independent random
variables (real or vector valued). For n2r consider a random variable of the
form

## PDF page 14

PROBABILITY INEQUALITIES FOR SUMS
25
U = —
Eg(Xi,..., Xi),
(5.3)
п(т)
where n"=n(n-1) ... (n-r+1) and the sum En,, is taken over all r-tuples
i1,..., i, of distinct positive integers not exceeding n. Random variables of
the form (5.3) have been called (one-sample) U statistics. For example, if
X; = (Y i, Li), i=1,..., n, are independent random vectors with two com-
ponents which have continuous distributions, then Kendall's rank correlation
coefficient is of the form (5.3) with r= 2 and g(Xi, X;) equal to the sign of
(Y:-Y;)(Zi-Z;). Other examples of U statistics can be found in reference [8].
V (X1,...,X) =
- 1g(X1,...
Xx) +g(Xr+1,..,Xar) +...
+ g(Nar-+1,..., Xkr)3, (5.4)
where k= [n/r], the largest integer contained in n/r. Then
1
U = -
V(Xig...,Xin),
(5.5)
п! п, т
where (in accordance with the notation in (5.3)) the sum Ln, n is taken over all
permutations i, iz, ..., in of the integers 1, 2, ...,n. Each term in the sum
on the right is a sum of k independent random variables. Thus (5.5) gives a
representation of U in the form (5.1) with N=n! and p:=1/n!.
If the function g is bounded,
a ≤9(21,.=,2x) ≤b,
(5.6)
it follows from (5.2) and the proof of Theorem 2 that
PrÍU-EU 21} ≤0-242116-01,
(5.7)
where k = [n/r]. This is an extension of the bound (2.3). To obtain simple exten-
sions of the other inequalities of Theorems 1 and 3 we assume that the random
variables X1, X2, •.., Xn are identically distributed. In this case, if 0≤g(X1,
..., X.) ≤1, then the bounds of Theorem 1 with n replaced by In/r| and
u=Eg(X1,..., X.) are upper bounds for Pr {U-EU≥t}, where EU = u. If
g(X1,..., X,) ≤EU+b, then the right-hand sides of (2.8) and (2.9) with n
replaced by In/r] and o'=var g(Xi,..., X,) are upper bounds for Pr
{U-EU≥t}.
5b. Iwo-sample U statistics. Let X1, X2, .., Xm, X1, Yz,.., Xnbemtn
independent random variables. For m ≥r and n≥s consider a random variable
of the form
U=
1
2i g(Hip.., Xi,, Yin•.., Y js),
(5.8)
m (r)n (8)
where the sum
Zm rins is taken over all r-tuples i,..., i, of distinct positive
• , Is) of distinct positive integers ≤n. A
rangers variate of the topes has been called a sample i statistic For

## PDF page 15

26
AMERICAN STATISTICAL ASSOCIATION JOURNAL, MARCH 1963
example, let X; and Y; be real and let U' denote the number of pairs (Xi, Y;)
such that Y, <X;. (This is one form of the Wilcoxon-Mann-Whitney statistic
[15], [10].) Then U'/mn is of the form (5.8) with r=8=1 and g(x, y) = 1 or 0
according as y <* or y≥x. Uther examples of two-sample U statistics can be
found in [9].
V (X1,..., Хт, У 1,..., Уп)
=-1g(X1...,Xr,Y1,...,Y)+g(Xx+1...,Xzr,Yo+1'•,Y26)
t... + g(Xkr-+1,..., Хит, Yко-о+1,..", Ука)}, (5.9)
where
* = min([m/r], [n/s]).
(5.10)
Then U as defined in (5.8) can be written as
U = -
(Hip'.., Xims Yin..., Yjn.
(5.11)
m!n! m,m; n, r
Each term on the right is a sum of k independent random variables. Thus
(5.11) represents U in the form (5.1).
If a ≤g≤b, then for U as defined by (5.8) we have inequality (5.7) where
li is now given by (5.10). If we assume that X1, .., Xm have a common dis-
tribution and Y1, .•, Yn have a common distribution (not necessarily the
same as that of Xi), then the terms in (5.11) are identically distributed and we
obtain extensions of the inequalities of Theorems 1 and 3 analogous to those
discussed at the end of section 5a, where now n is replaced by k as defined by
(5.10).
5c. Sums related to U statistics. Let again X1, X2, .., n be independent
and consider the random variable
1
W=-
(5.12)
For example, the Cramér-von Mises goodness of fit statistic u is defined by
(5.13)
where G(x) is a given cumulative distribution function and nFn(x) denotes the
number of those X1, ..•, Xn which are ≤x. If G(x) is continuous, we can
write w? in the form (5.12). with r= 2 and
(5.14)
A random variable W of the form (5.12) can be written as a U statistic,
W = -
n(=)
(5.15)

## PDF page 16

PROBABILITY INEQUALITIES FOR SUMS
27
where g* (21, • ••, Xr) is a weighted arithmetic mean of certain values of g. For
example, for r= 2 and r= 3 we have, respectively,
n - 1
д* (21, X2) =
- д(х1, Х2) +— g(X1, X1),
(5.16)
9* (Х1, Х2, Хз)
(п- 1) (п - 2)
- д (21, Х 2, хз) +
n - 1
{9 (21, 21, X2) + g X X2, X1)
1
+ 9(22, X1, x1)} + — 9(21, 1, X1). (5.17)
(The function g* for which (5.15) is satisfied is not uniquely determined. For
example, in (5.16) the value g(21, 21) may be replaced by 29 (21, X1) +29 (x2, x2) .)
Thus the results of section 5a can be directly applied to obtain upper bounds
for Pr {W-EW≥t}. Note also that since g* is an arithmetic mean of values of
9, a ≤g≤b implies a ≤g* ≤b. Hence the right-hand side of (5.7) with k= [n/r]
is also an upper bound for Pr {W-EW ≥t} if (5.6) is satisfied. (In some cases,
as in example (5.14), the range of g* is smaller than the range of g, but the dif-
ference is negligible when n is large.)
5d. Sums of m-dependent random variables. Let
S= YI+Yat... +Ym,
(5.18)
where the sequence of random variables Y1, Yz,
that is, the random vectors (Y1, • .., Yi) and (Y;,
Y n is (r-1)-dependent;
..•,Yn) are independent
if j-i≥r, where r is a positive integer. (Example: S= X,X,+ X.X,++...
+XnXrtn-1, where X1, Xs,... are independent.) Then the random variables
Yi, Yrti, Yartin... are independent. For i=1, ...
Si= Yit Yrtit Yartit... + Ynir-rtis
N; =
(5.19)
Then S= SitSt... +S, and S; is a sum of n; independent random varia-
bles. If we put pi= ni/n then the equation
(S-ES) = Ep:-(S,- ES.)
(5.20)
i=l
Ni
represents (S- ES)/n in the form (5.1). Hence by (5.2)
Pr!!
- (S - ES) ≥
(5.21)
If n is a multiple of r, n= lor, then n; = l for all i and we can obtain in a straight-
forward way explicit upper bounds similar to those of section 5a. In general
ni≥ n/r| and it is easy to see that the bounds for the expected values in (5.21)
remain valid if n; is replaced by [n/r]. Explicitly, if a ≤ Y; ≤6, then Pr {S- ES
≥nt} ≤exp (-2|n/r|1º/(b-a)2). If YI, Yz, • .•, Yn are identically distributed
and 0≤Y; ≤1, then the bounds of Theorem 1 with n replaced by |n/r] and
4= EY 1 are upper bounds for Pr {S-ES≥nt}, where ES=nu. If the Y; are

## PDF page 17

28
AMERICAN STATISTICAL ASSOCIATION JOURNAL, MARCH 1963
identically distributed and Y - BY; S6, then the right-hand sides of (2.8) and
(2.9) with n replaced by |n/r] and o' = Var Yi are upper bounds for Pr {S- ES
≥nt}.
6. SAMPLING FROM A FINITE POPULATION
In this section it will be shown that the inequalities of section 2 yield prob-
ability bounds for the sum of a random sample without replacement from a
finite population. Let the population C consist of N values c1, Cz, • • •
21, Je,..., Xn denote a random sample without replacement from and let
Y1, Y2,..
, Yn denote a random sample with replacement from C. The ran-
dom variables Y1, .., Yn are independent and identically distributed with
mean u and variance o?, where
l =
Ecis
02=-
• (Сі - м) .
(6.1)
If a ≤c: ≤b, Theorems 1, 2, and 3 give upper bounds for Pr {I-m≥t}, where
Y=(YIt... +Yn)/n. It will now be shown that the same bounds, with u
and o' defined by (6.1), are upper bounds for Pr {X-≥t}, where X= (X,
t... +Xn)/n.
(Nate that EX= EX=u but VarIN- no
N - 1 n
n
= Var 7).
This will be an immediate consequence of
Theorem 4. If the function f(x) is continuous and convex then
(6.2)
Applied to f(x) = exp (ha) the theorem yields the claimed result if we recall
that the bounds of Theorems 1 to 3 have been obtained from inequality (1.7).
(Note that the inequality Var X < Var V is a special case of (6.2).)
To prove Theorem 4 we first observe that for an arbitrary function g of n
variables we have, in the notation of (5.3),
(6.3)
g(Cis..., Cin).
(6.4)
7y=1
The right-hand sides are of the same form as U in (5.3) and W in (5.12), respec-
tively. It has been observed in section 5c that W can be written as U with g
replaced by an arithmetic mean g* of values of g. It follows that
(6.5)
As mentioned after (5.17), the function g* is not uniquely determined. The ver-
sion of g*(21,•.., Xn) which is symmetric in x1, •
, In will be denoted by

## PDF page 18

PROBABILITY INEQUALITIES FOR SUMS
§(21,•.., Xn). Here we are concerned with the special case g(x1,
=f(xIt... +Xn). In this case, if n= 2,
N - 1
§(21, X2) = -
2122)+
20(202) +
2N 1(222).
29
In general g can be written as
where the sum Z' is taken over the positive integers k, r1,
..., Гк, 21,..., 27
such that k=1, ..,n;rit... tr=n; and i,.., i are all different and
do not exceed n. The coefficients p are positive and do not depend on the func-
tion f. In accordance with (6.5) we have
, Хл).
(6.7)
If we let f(x) =1, we see from (6.6) and (6.7) that
(6.8)
If we put f(x) =x, then § (21,
Xn and hence equal to K• (xI+
, Xn) is a linear symmetric function of xI, ...,
• +Xn), where K is a constant factor. Since
E(yIt...+Yn)=E(XIt..
• +Xn), it follows from (6.7) that K=1. Thus
E' p(k, r1,
, "к, 21,
If f(x) is continuous and convex, it follows from (6.6), (6.8), (6.9) and Jensen's
inequality (1.9) that
Hence Eg X1, •
orem 4.
2n)210)
(6.10)
, Xn) ≥Ef(XIt.•+Xn). With (6.7) this implies The-
REFERENCES
[1] Bahadur, R. R., and Rao, R. Ranga, "On deviations of the sample mean," Annals
of Mathematical Statistics, 31 (1960), 1015-27.
[2] Bennett, George, "Probability inequalities for the sum of independent random vari-
" Journal of the American Statistical Association, 57 (1962), 33-45.
Chernoff, Herman, "A measure of asymptotic efficiency for tests of a hypothesis
based on the sum of observations," Annals of Mathematical Statistics, 23 (1952),
493-507.
[4] Doob, J. L., Stochastic Processes. New York: John Wiley and Sons, Inc., 1953.
[5] Feller, William, An Introduction to Probability Theory and Its Applications, Volume
I, Second edition. New York: John Wiley and Sons, Inc., 1957.
[6] Godwin, H. J., "On generalizations of Tehebychef's inequality," Journal of the Amer-
ican Statistical Association, 50 (1955), 923-45.
[7] Hardy, G. H., Littlewood, J. E., and Pólya, G., Inequalities. Cambridge: University
Press, 1952.
[8] Hoefiding, Wassily, "A class of statistics with asymptotically normal distribution,"
Annals of Mathematical Statistics, 19 (1948), 293-325.
[9] Lehmann, E. I., "Consistency and unbiasedness of certain nonparametric tests,"
Annals of Mathematical Statzstics, 24 (1951), 175-81.
[10] Mann, H. B., and Whitney, D. R., "On a test of whether one of two random variables

## PDF page 19

30
AMERICAN STATISTICAL ASSOCIATION JOURNAL, MARCH 1963
is stochastically larger than the other," Annals of Mathematical Statistics, 18(1947),
[11] Okamoto, Masashi, "Some inequalities relating to the partial sum of binomial proba-
bilities," Annals of the Institute of Statistical Mathematics, 10 (1958), 29-35.
[12] Prohorov, Yu. V., "An extremal problem in probability theory" (Russian; English
summary), Teoriya Veroyatnostei i ee Primeneniya, 4 (1959), 211-4. English trans-
lation in Theory of Probability and Its Applications, 4 (1959), 201-3.
[13] Savage, I. R., "Probability inequalities of the Tchebycheff type," Journal of Research
of the National Bureau of Standards--B. Mathematics and Mathematical Physics,
65B (1961), 211-22.
[14] Tehebichef, P., "Sur les valeurs limites des intégrales," Journal de Mathématiques
Pures et Appliquées, Ser. 2, 19 (1874), 157-60.
[15] Wilcoxon, Frank, "Individual comparisons by ranking methods," Biometrics, 1
(1943), 80-3.