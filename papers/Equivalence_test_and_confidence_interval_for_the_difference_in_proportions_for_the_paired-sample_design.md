# Equivalence test and confidence interval for the difference in proportions for the paired-sample design

Toshiro Tango, 1998. Statistics in Medicine 17(8), 891–908.

Fonte: https://www.eiti.uottawa.ca/~nat/Courses/csi5388/Tango.paired.pdf

SHA-256 PDF: `71dea8eddc08c73f15e2454d69b7f46d8bfa61b550c6246173fdfa4307df7ecd`. Acquisito 2026-09-14.

**Conversione:** Estrazione testuale pypdf per pagina; formule, colonne e figure possono essere omesse o disordinate. Il PDF è la fonte primaria.

## PDF page 1

* Correspondence to: Toshiro Tango, Division of Theoretical Epidemiology, The Institute of Public Health, 4-6-1
Shirokanedai, Minato-ku, Tokyo 108, Japan. e-mail: tango@iph.go.jp
CCC 0277Ð6715/98/080891Ð18$17.50 Received January 1996
( 1998 John Wiley & Sons, Ltd. Accepted July 1997
STATISTICS IN MEDICINE
Statist. Med. 17, 891Ð908 (1998)
EQUIVALENCE TEST AND CONFIDENCE INTERVAL FOR
THE DIFFERENCE IN PROPORTIONS FOR THE
PAIRED-SAMPLE DESIGN
TOSHIRO TANGO*
Division of Theoretical Epidemiology, The Institute of Public Health, 4-6-1 Shirokanedai, Minato-ku, Tokyo 108, Japan
SUMMARY
This paper considers a model for the di¤erence of two proportions in a paired or matched design of clinical
trials, case-control studies and also sensitivity comparison studies of two laboratory tests. This model
includes a parameter indicating both interpatient variability of response probabilities and their correlation.
Under the proposed model, we derive a one-sided test for equivalence based upon the e¦cient score.
Equivalence is deÞned here as not more than 100 * per cent inferior. McNemarÕs test for signiÞcance is
shown to be a special case of the proposed test. Further, a score-based conÞdence interval for the di¤erence
of two proportions is derived. One of the features of these methods is applicability to the 2]2 table with
o¤-diagonal zero cells; all the McNemar type tests and conÞdence intervals published so far cannot apply to
such data. A Monte Carlo simulation study shows that the proposed test has empirical signiÞcance levels
closer to the nominala-level than the other tests recently proposed and further that the proposed conÞdence
interval has better empirical coverage probability than those of the four published methods.( 1998 John
Wiley & Sons, Ltd.
1. INTRODUCTION
Recently, two groups of authors have proposed methods for testing equivalence in proportions
arising from a paired-sample study design. Lu and Bean1 considered a sensitivity comparison of
two medical diagnostic laboratory tests. Morikawa and Yanagawa2 discussed a comparison of
two treatments in clinical trials. They have derived test statistics similar to McNemarÕs test
statistic using Wald-type asymptotic standard errors.
Equivalence3 is usually deÞned as not more than 100 * per cent inferior, where *(’0) is
a prespeciÞed acceptable di¤erence between two proportions. A naive question about the
approaches above is whether a McNemarÕs type of test statistic comparing o¤-diagonal cells is
the only valid approach for inference about equivalence. Motivated by this question, in this
paper, we Þrst formulate a reasonable model representing the structure of this kind of comparison
study. This model includes parameters indicating interpatient variability of response probabilities
and their correlation. Under the proposed model, we derive a test for equivalence of two
proportions and also a conÞdence interval for their di¤erence based upon the e¦cient score.
Despite my initial question, the derived method is also shown to be of McNemarÕs type but to
have better small sample properties. Further, one feature of this method is that we can make

## PDF page 2

reasonable inferences for data in a 2]2 table having zero frequencies in the o¤-diagonal cells; all
methods published so far do not apply to such data.
Monte Carlo simulation studies are conducted to compare empirical signiÞcance levels
of the proposed test with the two tests above and also to compare empirical coverage probabilit-
ies of the proposed method for conÞdence interval estimation with those of published methods,
both unconditional and conditional. Finally, we illustrate our methods using data from a
cross-over trial of soft contact lenses and an epidemiological study of sleeping di¦culties in
marijuana users.
Score-based methods for hypothesis testing and interval estimation have been widely proposed
and used in many Þelds; Cox and Hinkley4 provide theoretical justiÞcation for them. Vollset5
reported favourable properties for the Wilson 6 score method for setting a conÞdence interval
for a single proportion. Yanagawa et al .7 have recently proposed Mantel ÐHaenszel type
tests for testing equivalence for comparative parallel design clinical trials, based on the
e¦cient score.
2. MODEL
Consider the comparison of a new and standard treatment (or diagnostic test) independently
performed on the same patient (or matched-pairs of patients) and suppose we have n patients
(or pairs). Further we assume that the probability of response to a treatment is a function
of the individual patientÕs unobserved characteristics. Let hk(k"1 ,..., n) denote the kth
patientÕs (matched-patientsÕs common) characteristics which might be multivariate, though
in this paper, we assume them to be univariate for simplicity. Further let Nk and Sk denote
the dichotomous response random variable having values 1 (response) and 2 (non-response)
of the new treatment and standard, respectively. Then, we have the following conditional
probabilities:
PrMNk"1 Dh kN"pN(hk) (1)
PrMSk"1Dh kN"pS(hk). (2)
In a matched case-control study, these two random variables Nk and Sk denote the incidence
probability of some ÔeventÕ under study in the case and control groups, respectively. Given h,
Nk and Sk are mutually independent, then the 2]2 matrixQ(h)"(qij(h)), of response probabilities
is shown as
Q(h)"
A
pN(h)pS(h)
(1!pN(h)) pS(h)
pN(h)(1!pS(h))
(1!pN(h))(1!pS(h)) B (3)
where
qij(h)"PrMN"i, S"j DhN "PrMN"iDhN PrMS"j DhN. (4)
In general, we do not know the population distribution for h. However, it can be assumed
that hkÕs are mutually independent and identically distributed with unknown distribution
892 T. TANGO
Statist. Med. 17, 891Ð908 (1998)( 1998 John Wiley & Sons, Ltd.

## PDF page 3

function F. Thus, we have
EhMpN(h)N"nN (5)
EhMpS(h)N"nS (6)
»hMpN(h)N"p2N (7)
»hMpS(h)N"p2S (8)
and
EhMpS(h)pN(h)N"nSnN#opSpN (9)
where o is the correlation coe¦cient over patients. Therefore, the expected 2]2 response matrix
Q"(qij)"(EhMqij(h)N) is given as
Q"A
nNnS#opNpS
(1!nN)nS!opNpS
nN(1!nS)!opNpS
(1!nN)(1!nS)#opNpSB. (10)
If the two treatments are truely identical, then, of course, o"1 and the 2]2 response matrix
will be
Q"A
n2#p2
n(1!n)!p2
n(1!n)!p2
(1!n)2#p2 B. (11)
Now consider the two extreme cases. When p"0, that is, the response probability is constant
regardless of h, then the matrix will be
Q"A
n2
n(1!n)
n(1!n)
(1!n)2 B. (12)
When p2"n(1!n), on the other hand, the matrix will be
Q"A
n
0
0
1!n B. (13)
The latter suggests the deterministic nature of treatment with threshold levelh0. Namely,p(h)"1
for h’h0 and 0, otherwise. In this special case, n"1!F(h0).
From my experience with the analysis of clinical laboratory data where we can easily make
repeated measurements or diagnostic tests by splitting oneblood sample into two, it seems to me
that well-recognized diagnostic tests might have the latter characteristic, that is,p2 can be nearly
equal to n(1!n). Therefore, the equivalence in the sensitivities between two diagnostic tests can
be reduced to the equivalence problem for thenÕs only. It should be noted here that, as Lu and
Bean1 have already pointed out, equivalence for diagnostic tests should focus on both sensitivity
and speciÞcity, but the same principles can apply to examine the latter comparison using
a di¤erent study population.
As to the response probability to treatments in clinical trials, on the other hand, variabilityp2
will probably lie between 0 andn(1!n) depending on both the treatment under study and the
patients entered into the trial. Therefore, if we could apply the same treatment to the same patient
(or matched-pairs of patients), we could estimate not only n but also p:
nö"2a#b#c
2n
, pö2"4ad!(b#c)2
4n2 (14)
DIFFERENCE IN PROPORTIONS FOR PAIRED-SAMPLE 893
Statist. Med. 17, 891Ð908 (1998)( 1998 John Wiley & Sons, Ltd.

## PDF page 4

where a, b, c and d are observed frequencies deÞned in (15) in the next section. This implies that
in equivalence testing in clinical trials, we have to evaluate not only n but also p2. Since p2
can be at most n(1!n), it only characterizes variability in the context of a given value
of n. Therefore, the ideal procedure is (i) apply an equivalence test for n and then (ii) under
the equivalence of n, conduct an equivalence test for p2. However, I admit that it will usually
be impractical to repeat the same treatment in the same patient and so we can not obtain such
measures of variability in practice. Therefore we are obliged to estimate n only in clinical
trials.
Nevertheless, the proposed modelling is useful to consider the structure of the problem under
study and also can give some insight. For example, Lu and Bean 1 suggested that the primary
evidence of equivalence in sensitivity is the probability of discordance and thus the smaller the
probability the more likely the two sensitivities will be equivalent. This view is based on the
property that the overall degree of discordance q12#q21 is the upper bound for the degree of
marginal heterogeneityq12!q21"nN!nS. However, thisview is not always correct. As shown
above, whether the probability of discordance is small or large depends on theunknown size of
variability p2.
3. SCORE TEST FOR EQUIVALENCE TESTING
Consider a random sample from the multinomial distribution deÞned in (10), then we have
QDATA"1
n
A
a
c
b
dB. (15)
Then, by letting
/"opNpS
the log-likelihood for this sample can be written
‚(nN, nS, /)"alog(q11)#blog(q12)#c log(q21)#dlog(q22)#constant. (16)
An equivalence hypothesis will be formulated as
H0 :nN"nS!*, H1: nN’nS!* (17)
where *(’0) is a prespeciÞed acceptable di¤erence in two proportions. Let
b"nN!(nS!*) (18)
then the above hypothesis is equivalent to the following:
H0 :b"0, H1: b’0 (19)
where the expected 2]2 response matrix Q"(qij) is given as
Q"A
(b#nS!*)nS#/
(1!b!nS#*)nS!/
(b#nS!*)(1!nS)!/
(1!b!nS#*)(1!nS)#/B. (20)
894 T. TANGO
Statist. Med. 17, 891Ð908 (1998)( 1998 John Wiley & Sons, Ltd.

## PDF page 5

Therefore, the score test can be applied to the log-likelihood function ‚(b, nS, /) and its test
statistic is given by
Z"C
L‚
Lb KnS/nL S,(/(K ,b/0DIM(IK ~1)33DnS/nL S,(/(K ,b/0N
"C
anL S
qL 11
#b(1!nL S)
qL 12
!cnL S
qL 21
!d(1!nL S)
qL 22 DSA
qL 12#qL 21!*2
n B (21)
where (nöS, /K ) is the maximum likelihood estimator under the null hypothesis b"0, which is
usually the unique solution to the following equations:
L‚
LnS
"L‚
L/"0. (22)
Further (IK ~1)33 indicates the (3, 3)th element of the inverse Fisher information matrix evaluated
at maximum likelihood estimators and is algebraically simpliÞed to ( qL 12#qL 21!*2)/n. The
details of the Fisher information matrix are given in Appendix I. The test statisticZ is known to
have asymptotically a standard normal distribution under H0. In terms of nS and /, equations
(22) can be solved iteratively by the scoring method as follows:
C
nöS
/K Dk
"C
nL S
/K Dk~1
#C
IK 11
IK 21
IK 12
IK 22 D
~1
k~1 C
LK ‚
LnS
LK ‚
L/ D
k~1
(23)
where the possible ranges of parameters are restricted by the conditions that 0)qij(1, that is,
the range for the nS is
0)*)nS(1
and the range for / is
!nS(nS!*))/)(1!nS)(nS!*) for *)nS)(1#*)/2
!(1!nS)(1!nS#*))/)(1!nS)(nS!*) for (1 #*)/2)nS(1.
However, it is easily understood that we do not have to obtain these estimators directly for testing
purposes and we need only a maximum likelihood estimator qL 21. In fact, as described in
Appendix II, the test statistic Z can be simply expressed as
Z(b, c; n, *)"Z" b!c#n*
IMn(2qL 21!*(*#1))N (24)
where the estimator qL 21 is the larger root of the quadratic equation Ax2#Bx#C"0, that is
qL 21"I(B2!4AC)!B
2A (25)
where
A"2n, B"!b!c!(2n!b#c)*, C"c*(*#1) (26)
and qL 12"qL 21!*, qL 11" a
a#d (1!qL 12!qL 21) and qL 22" d
a#d (1!qL 12!qL 21).
DIFFERENCE IN PROPORTIONS FOR PAIRED-SAMPLE 895
Statist. Med. 17, 891Ð908 (1998)( 1998 John Wiley & Sons, Ltd.

## PDF page 6

It should be noted that if an observed sample has one or more cells with zero frequencies then
the log-likelihood (16) tends to take the maximum value on theboundary of the parameter space
and thus equations (22) are no longer a necessary condition. However, as is shown in Appendix II,
the estimatorqL 21 deÞned in (25) still provides the correct maximum likelihood estimator, which is
summarized as follows. If
b"0 and c( 2n*
1#*
(*’0) (27)
then the maximum likelihood occurs atQK with qL 12"0 andqL 21"* which is a boundary point of
the parameter space and equations (22) are no longer satisÞed. However,qL 21 deÞned in (25) also
equals to *.
It is well known that if the true parameter value is on the boundary of the parameter space then
the regular asymptotic property of the likelihood ratio test breaks down whilst the score test may
be applied as usual (for example, see Chant8 and Self and Liang9). However, it seems to be not
well known whether the score-based method still works if the maximum likelihood estimator is
on the boundary of the parameter space. Therefore, as a way of checking the validity ofZ deÞned
by (24) in this boundary situation, we shall calculate Z(0, c; n, *) and compare it with the
predicted value. First, we can easily prove the following inequality:
DZ(b, c; n, *)D’DZ(b#1, c#1; n, *)D for b’0 (28)
where Z(b, c; n, *) with b’0 is free of the boundary problem. The prediction considered here is
an extrapolation of this trend, that is, topredict Z(0, c; n, *) by applying a low-order polynomial
regression to a series of ZÕs
MZ(k, k#c; n, *), k"1, 2, . . . ,KN
for someK. We shall use a cubic polynomial regression andK"10. The precision for this sort of
prediction scheme is examined by predictingZ(b, c; n, *) forb’0 that is free from the boundary
problem, and, as a result, cubic polynomials withK"10 have been conÞrmed good enough. The
results are shown in Table I for data withn"30, 50 and 80 andc"0, 1 and 2, indicating that the
predicted ZÕs are surprisingly consistent withZÕs. In general, asn become large, the predictedZÕs
are shown to be very close toZÕs. Therefore, we conclude that the proposed test works even if the
maximum likelihood estimator lies on the boundary of the parameter space.
As special cases, consider the following:
1. Zero o¤-diagonal cells, b"c"0. In this case,qL 21"* and thus the test statisticZ reduces
simply to
Z(0, 0;n, *)"
SA
n*
1!* B. (29)
That is to say, we can declare Ôclinically equivalentÕ if
n’n.*/"1!*
* Z2a . (30)
For example, when *"0)1 and a"0)05, we have n.*/"9]1)6452"24)35.
2. *"0 and b#c’0. In this case, qL 21"(b#c)/2n and thus this test coincides with the
well-known McNemar test for signiÞcance testing, namely,
Z(b, c; n, *"0)"(b!c)/ J(b#c). (31)
896 T. TANGO
Statist. Med. 17, 891Ð908 (1998)( 1998 John Wiley & Sons, Ltd.

## PDF page 7

Table I. Comparison of the propossed Z and j and their predicted values via cubic polynomial
regression models for the case b"0 and *"0)1, where qL 12"0)0 and qL 21"0)1, maximum likelihood
estimates on a boundary point of the parameter space
nc Test statistic (*"0)1) 90% conÞdence interval
Z predicted Z j-08, j61 predicted j-08, j61
30 0 1 )83 1 )81 ( !0)083, 0)083) ( !0)086, 0)086)
11 )22 1 )18 ( !0)136, 0)052) ( !0)138, !)
20 )61 0 )57 ( !0)183, 0)022) ( !0)186, !)
50 0 2 )36 2 )37 ( !0)051, 0)051) ( !0)054, 0)054)
11 )89 1 )88 ( !0)085, 0)032) ( !0)086, !)
21 )41 1 )40 ( !0)114, 0)013) ( !0)114, !)
80 0 2 )98 2 )99 ( !0)033, 0)033) ( !0)034, !0)034)
12 )61 2 )61 ( !0)054, 0)021) ( !0)054, !)
22 )24 2 )24 ( !0)073, 0)009) ( !0)073, !)
When c’0, predicted j61 is not shown here for c’0 since jª 61 is free from the boundary problem
4. CONFIDENCE INTERVAL
Testing clinical equivalence with an acceptable di¤erence * at one-sided signiÞcance level a is
equivalent to judging whether the lower limit of the 1!2a level conÞdence interval is greater
than !*. The score-based approximate conÞdence limits for the di¤erence of two proportions
j"nN!nS"q12!q21 (32)
are the two solutions to the equation
Z(b, c; n,!j)"$Za (33)
where the plus and minus signs indicate the lower j-08(b, c; n,1 !2a) and the upper limit
j61(b, c; n,1 !2a), respectively, andZa is the uppera percentile of the standard Normal distribu-
tion. These two limits can be easily found by the secant method (see, for example, Gart and
Nam11).
In Appendix III, the relationship between qL 21 and jª is described to show a solution in the
boundary situation. The results are summarized as follows:
1. b"0 and c’0: Qª that attains a lower limit lies on the boundary with qL 12"0 of the
parameter space. Qª that attains an upper limit lies on the boundary with qL 12"0i f
Z2a)c(n!c)/2n and on an interior point, otherwise.
2. b’0 and c"0: Qª that attains an upper limit lies on the boundary with qL 21"0. Qª that
attains a lower limit lies on the boundary with qL 21"0i f Z2a)b(n!b)/2n and on an
interior point, otherwise.
3. b"c"0: Both Qª that attains a lower limit and QK that attains an upper limit lie on the
boundary:
Using a similar method as the prediction forZÕs, we shall examine the validity of the conÞdence
interval based on a boundary value of Qª by applying a cubic polynomial regression to predict
one or both limits. For example, we predicted the limits of the 90 per cent conÞdence interval, for
DIFFERENCE IN PROPORTIONS FOR PAIRED-SAMPLE 897
Statist. Med. 17, 891Ð908 (1998)( 1998 John Wiley & Sons, Ltd.

## PDF page 8

the data with b"0, c"0, 1, 2 and n"30, 50, 80 using a series:
Mjª -08(k, c#k; n,0 )90), k"1, 2,2,1 0N
for the lower limit, and
Mjª 61(k, c#k; n,0)90), k"1, 2,2,1 0N
for the upper limit. The results are also shown in Table I, which also indicates very good
consistency. It should be noted that whenb"0 and c"1, 2, each of theQª Õs attaining an upper
limit is an interior point of the parameter space and thus the corresponding predicted limit is
unnecessary and not shown there.
Here also, let us consider the special case of zero o¤-diagonal cells,b"c"0. From (29), we
easily have
[jª -08(0, 0;n,1 !2a), jª 61(0, 0;n,1 !2a)]"
C! Z2a
n#Z2a
, Z2a
n#Z2a D. (34)
It should be noted that whenn"0, that is, we have no information, this interval becomes a quite
reasonable interval [!1, 1].
5. SIMULATION
5.1. Equivalence Test
So far, three tests have been proposed for this purpose. Lu and Bean1 proposed an unconditional
test based on McNemarÕs test as
ZLB" b!c#n*
I(b#c!n*2)
(35)
for the problem of testing one-sided equivalence in the sensitivities of screening tests. They also
proposed a conditional version
ZCLB"SA
b#c
bc BA
b!c#n*
2 B. (36)
Morikawa and Yanagawa2 proposed, on the other hand, a test statistic similar toZLB for the
problem of clinical equivalence of drugs:
ZMY" b!c#n*
IMb#c!(b!c)2/nN. (37)
This statistic is based on the asymptotic Normality of some function of the multinomial
distribution.10 When *"0, the three tests above are not equivalent and onlyZLB is equivalent to
McNemarÕs Z statistic. To investigate the small-sample distribution of the proposed and two
others tests, ZLB and ZMY, under the null hypothesis, some Monte Carlo simulations were
performed for *"0)1 nS"0)5, 0)8, /"0, 0)1, 0)14, 0)15 and 0)20 where applicable. Lu and
BeanÕs conditional test ZCLB was excluded from this comparison since the test cannot apply to
data with b"0o r c"0. Samples of multinomial proportions of size n("30, 50, 80) whose
parameters are deÞned as the matrixQ in equation (20) withb"0, were randomly generated. For
898 T. TANGO
Statist. Med. 17, 891Ð908 (1998)( 1998 John Wiley & Sons, Ltd.

## PDF page 9

Table II. Empirical signiÞcance level of the proposed score test with *"0)1 based on
10,000 trials
nS n / q12 Test statistic
ZZ LB ZMY
0)53 0 0 )00 )24 )85 )75 )7
0)10 )15 )06 )36 )3
0)15 0 )05 4 )27 )77 )7
0)20 0 )04 )41 8 )71 8 )7
50 0 )00 )25 )25 )55 )5
0)10 )15 )26 )26 )2
0)15 0 )05 4 )36 )46 )4
0)20 0 )03 )71 1 )21 1 )2
80 0 )00 )25 )05 )05 )1
0)10 )15 )25 )45 )9
0)15 0 )05 4 )45 )96 )5
020 0 )03 )68 )78 )7
0)83 0 0 )00 )14 5 )15 )85 )8
0)10 )04 4 )29 )29 )2
0)14 0 )04 )11 8 )61 8 )6
50 0 )00 )14 5 )16 )26 )2
0)10 )04 4 )87 )27 )2
0)14 0 )04 )01 1 )91 1 )9
80 0 )00 )14 5 )35 )45 )6
0)10 )04 4 )96 )77 )4
0)14 0 )03 )88 )68 )6
each simulated sample of proportions each of the three test statistics was computed and
compared with the 95th quantile of the standard Normal distribution.
Table II presents empirical signiÞcance levels based on 10,000 replications. It appears that the
empirical signiÞcance levels for the proposedZ are generally closer to the nominala-level than
those for the other two tests. Especially asn becomes small and / becomes large, the empirical
signiÞcance levels forZLB and ZMY tend to inßate whereas that ofZ tends to decrease gradually.
When q12"0, the inßation is clear for ZLB and ZMY.
It should be noted that (i) simulated samples with b"c"0 are replaced by b"c"1 (with
n unchanged) for the two test statistics ZLB and ZMY, and (ii) samples with the square root of
negative values ofZLB or ZMY are excluded from this comparison since these data cannot be used
with these two tests. These samples occurred mainly when/"0)1&0)2 in which the o¤-diagonal
cell probabilityq12 tends to be small. Therefore the results of this simulation are biased in favour
of ZLB and ZMY.
It should also be noted that Lu and Bean1 gave their formulae for use in hypothesis testing only
in passing, as an adjunct to establishing sample size requirements and they are not claiming good
properties for these formulae.
Table III shows empirical powers for the case whennN"nS based on 10,000 replications with
parameter values similar to those in Table III. The di¤erence in powers betweenZ and ZLB or
ZMY seems to be due to the di¤erence in empirical signiÞcance levels.
DIFFERENCE IN PROPORTIONS FOR PAIRED-SAMPLE 899
Statist. Med. 17, 891Ð908 (1998)( 1998 John Wiley & Sons, Ltd.

## PDF page 10

Table III. Empirical power of the score test with*"0)1 for the casenN"nS based on 10,000 trials
nS n / q12 Test statistic
ZZ LB ZMY
0)53 0 0 )00 )21 8 )42 0 )92 0 )9
0)10 )12 5 )12 7 )32 7 )3
0)15 0 )05 29 )63 6 )93 6 )9
50 0 )00 )22 6 )12 6 )82 6 )8
0)10 )13 4 )93 8 )83 8 )8
0)15 0 )05 44 )04 9 )84 9 )8
80 0 )00 )23 5 )43 5 )43 5 )9
0)10 )14 9 )14 9 )55 1 )4
0)15 0 )05 60 )76 4 )06 6 )1
0)83 0 0 )00 )14 24 )52 6 )52 6 )5
0)10 )04 33 )75 3 )35 3 )3
50 0 )00 )14 33 )63 7 )53 7 )5
0)10 )04 58 )16 7 )46 7 )4
80 0 )00 )14 48 )14 8 )45 0 )0
0)10 )04 77 )28 3 )58 4 )2
5.2. ConÞdence Interval
In this section, we evaluate the coverage probability of the proposed conÞdence interval by
comparing several existing methods, including both unconditional and conditional ones. The
most well-known unconditional textbook formula (for example, Altman12)i s
…: b!c
n
$Za
n SGb#c!(b!c)2
n H. (38)
Recently, Vollset5 has compared thirteen methods for computing binomial conÞdence intervals
in the one-sample problem and recommended (a) continuity corrected score intervals mainly
because of simplicity and good coverage probabilities. Further, he recommended (b) exact
intervals and (c) Mid- p exact intervals. Therefore, we use these three in our comparison as
conditional methods. To obtain conditional conÞdence intervals, we have only to apply these
three methods for the proportion pL "b/(b#c) where b#c is Þxed:
b
n
!c
n"b#c
n G2 b
b#c!1H"b#c
n M2pL !1N.
A( 1!2a) level conÞdence continuity corrected score interval (SCC) for p is given by
SCC :
(b$0)5)#Z2a
2 $ZaSG(b$0)5)!(b$0)5)2
b#c #Z2a
4 H
b#c#Z2a
. (39)
900 T. TANGO
Statist. Med. 17, 891Ð908 (1998)( 1998 John Wiley & Sons, Ltd.

## PDF page 11

Exact conÞdence intervals for p, called Clopper ÐPearson intervals, are calculated from the
cumulative binomial distribution and the lower and upper limits are solutions to the following
polynomial equations:
EX-08%3"
Gp: b~1+
i/0 A
b#c
i Bpi(1!p)b`c~i"1!aH (40)
EX611%3"Gp: b+
i/0 A
b#c
i Bpi(1!p)b`c~i"aH. (41)
Needless to say, these limits can also be obtained by using percentiles of theF distribution. We
used these equations mainly because we can easily use the secant method to Þnd the roots. Mid-p
exact limits for p are found from similar equations with half the probability assigned to the
observed outcome:
MID-08%3"Gp: 1
2A
b#c
b Bpb(1!p)c#b~1+
i/0 A
b#c
i Bpi(1!p)b`c~i"1!aH (42)
and
MID611%3"Gp: 1
2A
b#c
b Bpb(1!p)c# b+
i/0 A
b#c
i Bpi(1!p)b`c~i"aH. (43)
For the conditional methods, 0 and 1 are utilized as lower and upper limits whenb"0 andc"0,
respectively. Using a similar method as the evaluation of equivalence testing procedures,
simulated data with b"c"0 are replaced byb"c"1 (with n unchanged) for the conditional
methods due to their inapplicability to these data. Therefore the results of this simulation also
have biases in favour of the conditional approaches.
Table IV shows empirical coverage probabilities of the above Þve methods for computing 95
per cent conÞdence intervals based on 1000 replications under the hypothesisnN"nS!* where
nS"0)8, /"0)0, 0)1 and 0)14 and*"0)0 and 0)1. It is seen that the proposed conÞdence interval
performs very well except whenq12"0 where we haveconservative conÞdence intervals for small
n. The unconditional simple method also performs well with relatively large sample sizes and
large discordant probability but not so well for other cases. On the other hand, conditional
methods are shown to be no good. Especially when q12 is small, their empirical coverage
probabilities seem to depend strongly on the parameter values and sample sizes. When/"0)1
and *"0)1, the coverage probabilities extend down to 80 per cent. On the other hand, when
/"0)1 and *"0, they go up to 99)9 per cent. These phenomena are probably the result of
discreteness as clearly seen in Figures 1 Ð3 of VollsetÕs paper. 5 Further, when q12"0, the
empirical coverage probabilities of conditional methods are around 34Ð40 per cent, indicating
that we cannot recommend conditional methods when the discordant cell frequencies are small.
We have also carried out the same simulation study for the casenS"0)5, 0)6, 0)7 and 0)9 but we
have not shown the results here since the resultant performances are similar to those shown in
Table IV and no new features have been observed.
DIFFERENCE IN PROPORTIONS FOR PAIRED-SAMPLE 901
Statist. Med. 17, 891Ð908 (1998)( 1998 John Wiley & Sons, Ltd.

## PDF page 12

Table IV. Comparison of Þve methods for computing 95 per cent conÞdence intervals via their coverage
probabilities under the null hypothesisnN"nS!* where nS"0)8, based on 1000 trials for each simulation
/ * q12 n Unconditional methods Conditional methods
W Proposed SCC Exact Mid- p
0)00 )10 )14 30 92 )89 5 )49 7 )79 7 )89 6 )1
50 93 )89 5 )19 7 )09 6 )79 4 )9
80 94 )49 4 )79 6 )29 6 )09 4 )5
0)00 )16 30 93 )39 5 )39 7 )69 7 )69 5 )6
50 94 )59 5 )09 8 )29 7 )39 5 )1
80 94 )69 4 )89 7 )29 7 )29 5 )9
0)10 )10 )04 30 91 )79 6 )58 1 )28 1 )28 0 )0
50 92 )99 6 )08 7 )38 7 )38 6 )3
80 94 )19 4 )69 1 )79 1 )38 8 )6
0)00 )06 30 92 )59 5 )69 9 )99 9 )99 9 )6
50 94 )09 5 )69 8 )49 8 )49 7 )5
80 94 )39 5 )09 7 )49 7 )69 5 )6
0)14 0 )10 )03 0 8 0 )09 8 )43 6 )53 6 )53 4 )5
50 87 )79 8 )03 7 )53 7 )03 6 )5
80 91 )59 4 )33 9 )43 9 )03 7 )2
6. EXAMPLES
6.1. Cross-over Clinical Trials on Soft Contact Lenses
First, let us consider cross-over clinical trials in which patients are randomized to one of two
treatment sequences AB or BA. Under the assumption that there is nocarry-over e¤ects and no
period e¤ects, dichotomous data for the e¦cacy are summarized in the same form of 2]2 table
as (15).
Miyanaga13 conducted cross-over clinical trials comparing a chemical (hydrogen peroxide)
disinfection system SA806 with a thermal disinfection system for soft contact lenses. It seems well
recognized that appropriate conditions for carrying out cross-over trials are likely to be met in
this Þeld. 44 patients were randomized to one of two treatment sequences and the results are
summarized in Table V. In this trial, we are interested in the equivalence of two disinfection
methods. In this trial, the Fisher exact test was applied to test for equivalence; the one-tailed
p-value was p"(10)12
"0)5 indicating clear non-signiÞcance and so it was concluded that two
methods areequivalent. However, this sort of inference is not acceptable. So, let us apply tests for
equivalence. With the small o¤-diagonal cell frequency, however, we cannot apply ZLB and
ZMY as is shown in Table II. Instead we apply our test. We have
Z"1)709’Z0>05"1)645 (one-tailed p-value"0)044)
and the 90 per cent conÞdence lower limit is
j-08"!0)096’!*"!0)1.
Based on these results, it will be concluded that the two methods are equivalent at the 5 per cent
signiÞcance level. To examine the empirical signiÞcance level of Z for this kind of data with
902 T. TANGO
Statist. Med. 17, 891Ð908 (1998)( 1998 John Wiley & Sons, Ltd.

## PDF page 13

Table V. Clinical assessment of treatments in cross-over trials of disinfection systems
for soft contact lenses
Thermal disinfection
E¤ective Ine¤ective Total
Hydrogen peroxide E¤ective 43 0 43
Ine¤ective 1 0 1
Total 44 0 44
Table VI. Empirical signiÞcance level of the four tests with *"0)1 for such data with
n"44 and small o¤-diagonal cell frequencies as shown in Table II, based on 10,000 trials
q12 nS / Test statistic
ZZ LB ZMY
0)00 )95 0 )0425 5 )41 7 )21 7 )2
0)90 0 )08 5 )71 6 )81 6 )8
0)02 0 )95 0 )0225 4 )39 )69 )6
0)90 0 )06 4 )61 0 )01 0 )0
n"44 and small o¤-diagonal cell frequencies, we performed a simulation study (the same as that
in Section 5) for each of the combinations of parameter values shown in Table VI. The resultant
empirical signiÞcance levels forZ are shown to be around 4)3Ð5)7 per cent, reasonably close to
the nominal 5 per cent level.
6.2. Epidemiological Study
Here we consider the data analysed by Karacan et al.14 and also by Altman.12 Karacan et al.
compared a group of 32 marijuana users with 32 matched controls with respect to their sleeping
di¦culties. Data are reproduced in Table VII. In this example, we are interested in the statistical
signiÞcance of the di¤erence of the proportions experiencing sleeping di¦culties, not in their
equivalence. Therefore, by letting*"0, the test statisticZ coincides with the McNemar test and
we have
Z" b!c
I(b#c)
" 9!3
I(9#3)"1)73
which gives two-tailedp"0)08, indicating weak evidence that marijuana users experience fewer
sleeping di¦culties than controls. The unconditional simple Wald type 95 per cent conÞdence
interval for the di¤erence in the proportions is !0)014 to 0)389. The proposed score-based
conÞdence interval is !0)027 to 0)390.
It should be noted that the 95 per cent conÞdence interval calculated in AltmanÕs textbook
(page 237) is!0)03 to 0)41. This calculation is wrong since the standard error of the di¤erence in
proportions is falsely calculated as 132
I(3#9#62/32). The correct standard error is
132I(3#9!62/32).
DIFFERENCE IN PROPORTIONS FOR PAIRED-SAMPLE 903
Statist. Med. 17, 891Ð908 (1998)( 1998 John Wiley & Sons, Ltd.

## PDF page 14

Table VII. Numbers with (#) or without (!) sleeping di¦culties
among marijuana users and matched controls (Karacan et al.14)
Marijuana group
#! Total
Control group # 49 1 3
! 31 6 1 9
Total 7 25 32
7. DISCUSSION
Regarding the model proposed in Section 2, as an alternative, but more restricted one, we might
consider the following mixed-e¤ects model:
PrMNk"1Dh kN"hk#j
and
PrMSk"1 DhkN"hk
where MhkN, k"1, 2,2, n is assumed to be a sequence of unobserved independent and identically
distributed random variables which have unknown distributionF with mean n and variance p2.
In this model,j indicates the common di¤erence in proportions but the variabilityp2 is assumed
to be the same for the two treatments and the correlation coe¦cient is 1 )0. Even this simpler
model can lead to the same score-based test statistic and its associated conÞdence interval
procedure since the proposed statistical inference procedure starts from the parameterization
/"opNpS as in equation (16). Liang and Zeger15 considered a similar model to propose a new
estimator of the common odds ratio in a matched case-control study, in which the link function
used is logit.
One of the characteristics of the proposed procedure was shown to be applicability to tables
with zero o¤-diagonal cells since other published methods do not apply to such data. We have
carried out simulation study to evaluate the performance of the proposed procedures. The
proposed test for equivalence has been shown to have empirical signiÞcant levels closer to
a nominal a-level compared with the other two tests. The evaluation of conÞdence intervals has
focused on the coverage probabilities since it is very important to conÞrm the designed 1 !a
coverage at least. The proposed conÞdence interval has been shown to perform well in general,
however, it has been shown to beconservative when one of the o¤-diagonal cell probabilities is
zero. On the other hand, all the conditional approaches including the exact one have been shown
to be inadequate when one or both discordant probabilities are small.
Since these Monte Carlo experiments have been based on a relatively small number of sets of
parameter values and sample sizes, the conclusions derived here may not be representative.
However, as I have examined typical sets of parameter values and sample sizes, I expect that
drastically di¤erent conclusions would not be derived for the parameter values not examined
here, although we need a further simulation study for more detailed comparisons.
In this paper, we have considered tests for the class of hypotheses that have **0, which
includes McNemarÕs test for signiÞcance and a test for equivalence. We can also generalize the
test to cope with the hypothesis with*(0. The latter alternative indicates that the true di¤erence
is greater than some medically signiÞcant di¤erence (!*) which is not zero.
904
T. TANGO
Statist. Med. 17, 891Ð908 (1998)( 1998 John Wiley & Sons, Ltd.

## PDF page 15

APPENDIX I: CALCULATION OF PARTIAL DERIVATIVES
For simplicity, let
m"1!(nN#nS)"1!2nS!b#*.
Then, the three scores are given by:
L‚
L/"C
a
q11
! b
q12
! c
q21
# d
q22D
L‚
Lb"nS
L‚
L/# b
q12
! d
q22
L‚
LnS
"(1!m) L‚
L/# b
q12
# c
q21
! 2d
q22
where MqijNÕs are deÞned by (20). Theijth element of the Fisher information matrixI are given by
the following:
I11"E C!L2‚
Ln2S D"n C
(1!m)2
q11
# m2
q12
# m2
q21
#(1#m)2
q22 D
I12"E C! L2‚
LnSL/D"nC
1!m
q11
! m
q12
! m
q21
!(1#m)
q22 D
I13"E C! L2‚
LnSLbD"nC
(1!m)nS
q11
#m(1!nS)
q12
!mnS
q21
#(1#m)(1!nS)
q22 D
I22"E C!L2‚
L/2D"nC
1
q11
# 1
q12
# 1
q21
# 1
q22D
I23"E C! L2‚
L/LbD"n C
nS
q11
#nS!1
q12
# nS
q21
#nS!1
q22 D
I33"E C!L2‚
Lb2 D"nC
n2S
q11
#(nS!1)2
q12
#n2S
q21
#(nS!1)2
q22 D.
Needless to say, we have Iij"Iji.
APPENDIX II: DERIVATION OF EQUATIONS (24)Ð(26)
The simultaneous equations (22) yield
a
q11
# d
q22
" b
q12
# c
q21
"2 d
q22
.
Then we have
L‚
Lb"1
2A
b
q21!*! c
q21B.
DIFFERENCE IN PROPORTIONS FOR PAIRED-SAMPLE 905
Statist. Med. 17, 891Ð908 (1998)( 1998 John Wiley & Sons, Ltd.

## PDF page 16

Further, by noting that
a
q11
" d
q22
" a#d
q11#q22
" n!b!c
1!q12!q21
it is shown that q21 is a solution of the equation
b
q21!*# c
q21
"!2 n!b!c
2q21!*!1 (44)
which reduces to the quadratic equations described in Section 3:
f (x)"2nx2!(b#c#(2n!b#c)*)x#c*(*#1)"0.
So does the following equation:
b
q21!*! c
q21
"2 b!c#n*
2q21!*(*#1).
Therefore the score statistic Z is given by (24).
Next, we describe whyqL 21 should be the larger root off (x)"0 as deÞned in (25). We consider
here not only the case*’0 but also*(0 since the result below can be applied to the problem
of conÞdence limits (Appendix III).
Consider the following four cases.
1. b’0 and c’0. Since 0(qL 21"x(1 and 0(qL 12"x!*(1, the appropriate root of
f (x)"0 must satisfy
*(x(1 for *’0
0(x(1#* for *(0.
When *’0, we have
f (0)"c*(*#1)’0, f (1)"(1!*)(2n!b!c(1#*))’0, and f (*)"!b*(1!*)(0,
which indicates the larger root satisÞes *(x(1. When *(0, we have
f (0)(0, and f (1#*)"(1#*)(2n!c!b(1!*))’0
and thus the larger root satisÞes 0(x(1#*. Therefore, whenb’0 andc’0, regardless
of the sign of *, qL 21 is the larger root.
2. b"0 and c’0. In this case, we have two roots:
x1"*, and x2"c(1#*)
2n .
However, equation (44) has a single root x2. The root x1 is a boundary point of the
parameter space since qL 12"0. This means the following:
906 T. TANGO
Statist. Med. 17, 891Ð908 (1998)( 1998 John Wiley & Sons, Ltd.

## PDF page 17

(a) Case *’0: the condition that the simultaneous equations (22) have the unique root
x2 is 0)qL 12"x2!x1, that is
c* 2n*
1#* . (45)
If x2(x1, then the simultaneous equations (22) are no longer a necessary condition for
maximality and the log-likelihood (16) attains its maximum at qL 21"x1"* on
a boundary point.
(b) Case *(0: x2 is always the unique root of (22) since 0(qL 12(1.
In this case also, qL 21 is the larger root of f (x)"0.
3. c"0 and b’0. In this case, we have two roots:
x1"0, and x2"*#b(1!*)
2n
but equation (44) has a single root x2.
(a) Case *’0: x2 is always the unique root of (22) since 0"x1(x2(1 and 0(qL 12(1.
(b) Case *(0: we always have 0(qL 12(1. Then the condition that equations (22) have
the unique root should be 0)x2(1, that is
b*! 2n*
1!* .
If x2(0"x1 then equations (22) have no roots and the log-likelihood (16) takes its
maximum at qL 21"x1"0.
Here also, qL 21 is shown to be the larger root of f (x)"0.
4. b"c"0. We have two rootsx1"0 andx2"*. In this case, equations (22) have no roots,
but the log-likelihood (16) is maximized atqL 21"x2"* if *’0, and atx1"0, otherwise.
In this case also, the larger root is qL 21.
In summary, regardless of the sign of* and of the values of (b, c), qL 21 is always shown to be the
larger root of f (x)"0; hence the positive root value of the square root is taken in equation (25).
APPENDIX III: RELATIONSHIP BETWEEN jª AND qL 21
From the results of Appendix II, by letting j"!*, we have the following results:
1. b’0 and c’0. Each of the two conÞdence limits can be calculated by usingqL 21 which is
the unique root of equations (22).
2. b"0 and c’0. Using (45), we have the following relationship:
qL 21"G
!jª
c(1!jª )/2n
(boundary point)
(interior point)
if jª )!c/(2n!c)
otherwise.
It should be noted that if qL 21"!jª then qL 12"0. If j*!c/(2n!c) then
Z(0, c; n,!j)(0, indicating that the lower limit is always based on the boundary value
qL 21,-08"!jª -08. The upper limit requires c#nj’0, which means
qL 21,61"G
!jª 61
c(1!jK 61)/2n
if Z2a)c(n!c)/2n
otherwise.
DIFFERENCE IN PROPORTIONS FOR PAIRED-SAMPLE 907
Statist. Med. 17, 891Ð908 (1998)( 1998 John Wiley & Sons, Ltd.

## PDF page 18

3. b’0 and c"0. In a similar manner, jª 61 is always based on the boundary value of
qL 21,61"0. The lower limit jª -08 is based on qL 21,-08 deÞned as
qL 21,-08"G
0
!jª -08#b(1#jª -08)/2n
if Z2a)b(n!b)/2n
otherwise.
4. b"0 and c"0. Clearly, we have that qL 21,-08"!jª -08 and qL 21,61"0.
ACKNOWLEDGEMENTS
The authors thanks two anonymous referees for invaluable comments on an earlier draft of the
paper that led to substantial improvements.
REFERENCES
1. Lu, Y. and Bean, J. A. ÔOn the sample size for one-sided equivalence of sensitivities based upon
McNemarÕs testÕ, Statistics in Medicine, 14, 1831Ð1839 (1995).
2. Morikawa, T. and Yanagawa, T. ÔTaiounoaru 2chi data ni taisuru doutousei kentei. (Equivalence testing
for paired dichotomous data)Õ, Proceedings of Annual Conference of Biometric Society of Japan ,
123Ð126 (1995) (in Japanese).
3. Machin, D. and Campbell, M. J.Statistical „ables for the Design of Clinical„rials, Blackwell ScientiÞc
Publications, Oxford, 1987.
4. Cox, D. R. and Hinkley, D. V. „heoretical Statistics, Chapman and Hall, London, 1974.
5. Vollset, S. E. ÔConÞdence intervals for a binomial proportionÕ,Statistics in Medicine, 12, 809Ð824 (1993).
6. Wilson, E. B. ÔProbable inference, the law of succession, and statistical inferenceÕ, Journal of the
American Statistical Association, 22, 209Ð212 (1927).
7. Yanagawa, T., Tango, T. and Hiejima, Y. ÔMantel-Haenszel type tests for testing equivalence or more
than equivalence in comparative clinical trialsÕ, Biometrics, 50, 859Ð864 (1994).
8. Chant, D. ÔOn the asymptotic tests of composite hypotheses in nonstandard conditionsÕ,Biometrika, 61,
291Ð298 (1974).
9. Self, S. G. and Liang, K. Y. ÔAsymptotic properties of maximum likelihood estimators and likelihood
ratio tests under nonstandard conditionsÕ,Journal of the American Statistical Association, 82, 605Ð610
(1987).
10. Grizzle, J. E., Starmer, C. F. and Koch, G. G. ÔAnalysis of categorical data by linear modelsÕ,Biometrics,
25, 489Ð503 (1969).
11. Gart, J. J. and Nam, J. ÔApproximate interval estimation of the ratio of binomial parameters: A review
and corrections for skewnessÕ, Biometrics, 44, 323Ð338 (1988).
12. Altman, D. G. Practical Statistics for Medical Research, Chapman and Hall, London, 1991.
13. Miyanaga, Y. ÔClinical evaluation of the hydrogen peroxide SCL disinfection system (SCL-D)Õ,Japanese
Journal of Soft Contact ‚enses, 36, 163Ð173 (1994) (in Japanese).
14. Karacan, I., Fernandez, S. A. and Coggins, W. S. ÔSleep electrocephalographic-electrooculographic
characteristics of chronic marijuana users: part 1Õ,New ‰ork Academy of Science, 282, 348Ð374 (1976).
15. Liang, K. Y. and Zeger, S. L. ÔOn the use of concordant pairs in matched case-control studiesÕ,
Biometrics, 44, 1145Ð1156 (1988).
908 T. TANGO
Statist. Med. 17, 891Ð908 (1998)( 1998 John Wiley & Sons, Ltd.