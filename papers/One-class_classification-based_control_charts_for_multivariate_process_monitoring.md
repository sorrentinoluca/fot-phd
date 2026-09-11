
![](One-class_classification-based_control_charts_for_multivariate_process_monitoring_images/One-class_classification-based_control_charts_for_multivariate_process_monitoring.pdf-0001-00.png)


### **IIE Transactions** 

**ISSN: 0740-817X (Print) 1545-8830 (Online) Journal homepage: www.tandfonline.com/journals/uiie20** 


![](One-class_classification-based_control_charts_for_multivariate_process_monitoring_images/One-class_classification-based_control_charts_for_multivariate_process_monitoring.pdf-0001-03.png)


## **One-class classification-based control charts for multivariate process monitoring** 

#### **Thuntee Sukchotrat, Seoung Bum Kim & Fugee Tsung** 

**To cite this article:** Thuntee Sukchotrat, Seoung Bum Kim & Fugee Tsung (2009) One-class classification-based control charts for multivariate process monitoring, IIE Transactions, 42:2, 107-120, DOI: 10.1080/07408170903019150 

**To link to this article:** <u>https://doi.org/10.1080/07408170903019150</u> 


![](One-class_classification-based_control_charts_for_multivariate_process_monitoring_images/One-class_classification-based_control_charts_for_multivariate_process_monitoring.pdf-0001-08.png)



![](One-class_classification-based_control_charts_for_multivariate_process_monitoring_images/One-class_classification-based_control_charts_for_multivariate_process_monitoring.pdf-0001-09.png)



![](One-class_classification-based_control_charts_for_multivariate_process_monitoring_images/One-class_classification-based_control_charts_for_multivariate_process_monitoring.pdf-0001-10.png)



![](One-class_classification-based_control_charts_for_multivariate_process_monitoring_images/One-class_classification-based_control_charts_for_multivariate_process_monitoring.pdf-0001-11.png)



![](One-class_classification-based_control_charts_for_multivariate_process_monitoring_images/One-class_classification-based_control_charts_for_multivariate_process_monitoring.pdf-0001-12.png)


Published online: 20 Nov 2009. 


![](One-class_classification-based_control_charts_for_multivariate_process_monitoring_images/One-class_classification-based_control_charts_for_multivariate_process_monitoring.pdf-0001-14.png)


Submit your article to this journal 

Article views: 1193 


![](One-class_classification-based_control_charts_for_multivariate_process_monitoring_images/One-class_classification-based_control_charts_for_multivariate_process_monitoring.pdf-0001-17.png)


View related articles 


![](One-class_classification-based_control_charts_for_multivariate_process_monitoring_images/One-class_classification-based_control_charts_for_multivariate_process_monitoring.pdf-0001-19.png)


Citing articles: 18 View citing articles 

Full Terms & Conditions of access and use can be found at https://www.tandfonline.com/action/journalInformation?journalCode=uiie21 

_IIE Transactions_ (2010) **42** , 107–120 Copyright<sup>⃝C</sup> “IIE” ISSN: 0740-817X print / 1545-8830 online DOI: 10.1080/07408170903019150 

# One-class classification-based control charts for multivariate process monitoring 

###### THUNTEE SUKCHOTRAT<sup>1</sup> , SEOUNG BUM KIM<sup>1</sup><sup>_,_∗</sup> and FUGEE TSUNG<sup>3</sup> 

> 1 _Department of Industrial and Manufacturing Systems Engineering, University of Texas at Arlington, Arlington, TX 76019, USA_ 

> 2 _Division of Information Management Engineering, Korea University, Seoul, South Korea E-mail: sbkim1@korea.ac.kr_ 

> 3 _Department of Industrial Engineering and Logistics Management, Hong Kong University of Science and Technology, Clear Water Bay, Kowloon, Hong Kong_ 

Received August 2008 and accepted April 2009 

One-class classification problems have attracted a great deal of attention from various disciplines. In the present study, attempts are made to extend the scope of application of the one-class classification technique to Statistical Process Control (SPC) problems. New multivariate control charts that apply the effectiveness of one-class classification to improvement of Phase I and Phase II analysis in SPC are proposed. These charts use a monitoring statistic to represent the degree of being an outlier as obtained through one-class classification. The control limits of the proposed charts are established based on the empirical level of significance on the percentile, estimated by the bootstrap method. A simulation study is conducted to illustrate the limitations of current one-class classification control charts and demonstrate the effectiveness of the proposed control charts. 

**Keywords:** Data mining, Hotelling’s _T_<sup>2</sup> , multivariate process, one-class classification method, statistical process control 

##### **1. Introduction** 

Statistical Process Control (SPC) is one of the widely used techniques for quality control. The basic objective of SPC is to quickly detect the occurrence of special cause variation, so that the process can be investigated and corrective action may be taken before quality deteriorates and defective units are produced (Stoumbos _et al._ , 2000). One important tool in SPC is the control chart, which is used to monitor the performance of a process over time to keep the process in an in-control state. In general, control chart problems in SPC can be divided into two phases (Woodall and Montgomery, 1999; Woodall, 2000). Phase I analysis tries to isolate the in-control (baseline) data from an unknown historical data set and establish the control limits for future monitoring (Zhang and Albin, 2007). Phase II analysis monitors the process using control charts derived from the “cleaned” in-control data set from the Phase I analysis. With a simple plot of the set of monitoring statistics derived from the original samples, the control chart can effectively determine whether or not a process is in an in-control state. Examples of monitoring statistics include the sample average and the sample range. In addition to the monitoring statistics, another important component of control charts is control 

limits, which often are calculated based on the probabilistic distribution of the monitoring statistic. 

Hotelling extended the univariate control chart to handle multivariate problems (Hotelling, 1947). Hotelling’s _T_<sup>2</sup> chart ( _T_<sup>2</sup> chart) is a multivariate control chart that can monitor a multivariate process efficiently. _T_<sup>2</sup> charts use the _T_<sup>2</sup> statistic computed from the following equation: 


![](One-class_classification-based_control_charts_for_multivariate_process_monitoring_images/One-class_classification-based_control_charts_for_multivariate_process_monitoring.pdf-0002-12.png)


where **x** ¯ and **S** are a sample mean vector and a sample covariance matrix determined from the in-control (Phase I) data. The _T_<sup>2</sup> statistic measures the distance between an observation and the scaled-mean estimated from the in-control data. Given that **x** follows a multivariate normal distribution, the _T_<sup>2</sup> statistic follows an _F_ distribution (Mason and Young, 2002). In _T_<sup>2</sup> charts, the 100 _α_ % tail area of an _F_ distribution is used as the control limit, where _α_ is the user-specified level of significance. It is known that _T_<sup>2</sup> charts can effectively control Type I and Type II error rates when the underlying distribution of the process data is the multivariate normal distribution (Lowry and Montgomery, 1995). However, the distributional assumption of _T_<sup>2</sup> charts means that it is difficult to apply these charts to the non-normal data that is often found in many modern industries. A number of non-parametric control charts have been developed to address the limitation of the 

∗Corresponding author 

0740-817X<sup>⃝C</sup> 2010 “IIE” 

_Sukchotrat_ et al. 

108 

distributional assumptions (Chakraborti _et al._ , 2001; Liu _et al._ , 2004; Bakir, 2006; Kim _et al._ , 2007; Qiu, 2008). However, no consensus exists about which of them best satisfies all the conditions encountered in modern process systems. A detailed review of non-parametric control charts is beyond the scope of this paper. 

As the limitations of current SPC techniques become increasingly obvious in the face of ever more complex processes, data mining algorithms, because of their proven capabilities to effectively analyze and manage large amounts of data, have the potential to resolve the challenging problems in SPC. Despite the enormous popularity of data mining studies that has seen their application to a variety of areas, few efforts have been made to integrate data mining algorithms with SPC (Smith, 1994; Cook and Chiu, 1998; Chinnam, 2002; Hwang _et al._ , 2005; Hu _et al._ , 2007). In particular, one-class classification methods share a common goal with control charts because both methods assume that the in-control group (target group) is the only population and it can be used for measuring the degree of abnormality of new observations. Several studies have been undertaken recently with the goal of implementing one-class classification algorithms as an alternative to traditional control charts. Sun and Tsung (2003) proposed kernel-distance-based charts (K charts) based on a Support Vector Data Description (SVDD) algorithm. SVDD is a modified version of the original Support Vector Machines (SVMs) concept for solving one-class classification problems. K charts use a monitoring statistic derived from the distance between the new observation and the decision boundary generated by the SVDD algorithm. The control limits of K charts are established and adjusted from a parameter in the SVDD algorithm. Sun and Tsung’s study revealed that K charts perform better than _T_<sup>2</sup> charts when the data deviate from normality. Kumar _et al._ (2006) used another one-class SVM technique to construct robust K charts through normalized monitoring statistics. They showed that, in addition to the flexibility of non-normal data, robust K charts can efficiently handle autocorrelated process data. Furthermore, one-class SVM-based control charts have been applied to detect anomalies in computernetworking applications (Zhang _et al._ , 2007). It is clearly laudable that the aforementioned studies proposed to use the monitoring statistic from the one-class SVM method. Thus, the construction of the charts does not require any distribution assumptions. However, they did not suggest an efficient way to establish the control limits, one of the major components in control charts. 

This paper makes contributions in two aspects. First, we propose an efficient way to establish the control limits necessary to improve the existing one-class SVM-based control charts. Second, we propose new one-class classificationbased control charts based on a _k_ -nearest-neighbor algorithm. Simulation studies were conducted to demonstrate the effectiveness of the proposed approaches in both the Phase I and Phase II analyses. 

##### **2. SVDD-based control charts** 

###### **2.1.** **_The SVDD algorithm_** 

An SVM is one of the supervised learning algorithms popularly used for both regression and classification problems. SVMs use geometric properties and obtain a separating hyperplane by solving a convex optimization problem that simultaneously minimizes the generalization error and maximizes the geometric margin between the classes (Vapnik, 1998). Non-linear SVM models can be constructed from kernel functions such as linear, polynomial and radial basis functions, etc. SVDD is a mixture of SVM and the data description method for solving one-class classification problems (Tax and Duin, 2004). SVDD provides a hypersphere boundary around the data. A brief summary of the SVDD algorithm is as follows. Let **a** be the center of the hypersphere. Let _R_<sup>2</sup> be the radius of the hypersphere (i.e., the distance from **a** to the boundary). Let **x** _i_ = [ _xi_ 1 _, xi_ 2 _, . . . , xip_ ]<sup>T</sup> , for _i_ = 1, 2, _. . ._ , _N_ be a sequence of _p_ -variate training (target) observations. SVDD boundaries are constructed to minimize the volume of the hypersphere while maximizing the training observations captured by the hypersphere (Tax and Duin, 2004). That is, the problem is to 


![](One-class_classification-based_control_charts_for_multivariate_process_monitoring_images/One-class_classification-based_control_charts_for_multivariate_process_monitoring.pdf-0003-08.png)


with the constraint: 


![](One-class_classification-based_control_charts_for_multivariate_process_monitoring_images/One-class_classification-based_control_charts_for_multivariate_process_monitoring.pdf-0003-10.png)


where _ξi >_ 0 is the slack variable that allows **x** to be outside the hypersphere. _C_ controls the trade-off between the volume of the hypersphere and the misclassification errors. Tax and Duin (2004) defined a user-specified parameter _f_ that represents the fraction of the training data outside the decision boundary: 


![](One-class_classification-based_control_charts_for_multivariate_process_monitoring_images/One-class_classification-based_control_charts_for_multivariate_process_monitoring.pdf-0003-12.png)


where _N_ is the number of target observations. For instance, 80% of the training data points are supposed to be included in the SVDD boundary constructed with _f_ = 0 _._ 20. When _f_ is increased from 0.20 to 0.30, the volume of the hypersphere becomes smaller but the misclassification error in the target class becomes larger. 

Equation (2) can be solved by the following Lagrangian: 


![](One-class_classification-based_control_charts_for_multivariate_process_monitoring_images/One-class_classification-based_control_charts_for_multivariate_process_monitoring.pdf-0003-15.png)


where _αi_ ≥ 0 and _γi_ ≥ 0 are the Lagrange multipliers. Setting partial derivatives of _L_ with respect to _R_ , **a** and _ξi_ and 

set to zero provides the following constraints: 


![](One-class_classification-based_control_charts_for_multivariate_process_monitoring_images/One-class_classification-based_control_charts_for_multivariate_process_monitoring.pdf-0004-01.png)



![](One-class_classification-based_control_charts_for_multivariate_process_monitoring_images/One-class_classification-based_control_charts_for_multivariate_process_monitoring.pdf-0004-02.png)


When substituting these constraints to Equation (5), the optimization problem becomes: 


![](One-class_classification-based_control_charts_for_multivariate_process_monitoring_images/One-class_classification-based_control_charts_for_multivariate_process_monitoring.pdf-0004-04.png)


The solution, the set of _αi_ , _i_ = 1 _,_ 2 _, . . . , N_ , can be obtained by maximizing Equation (9) subject to 0 ≤ _αi_ ≤ _C_ and<sup>�</sup> _i_<sup>_N_</sup> =1<sup>_αi_= 1.</sup> 

As with conventional SVM, the SVDD algorithm can generate more flexible decision boundaries by replacing the inner product with kernel functions. For example, the following Gaussian kernel function can be replaced with the inner product in Equation (9): 


![](One-class_classification-based_control_charts_for_multivariate_process_monitoring_images/One-class_classification-based_control_charts_for_multivariate_process_monitoring.pdf-0004-07.png)


where _S >_ 0 is the width of the Gaussian kernel that controls the complexity of the SVDD boundary. Given a testing data point **z** , _D_<sup>2</sup> that measures the distance between **z** and the center, **a** can be calculated by the following equation: 


![](One-class_classification-based_control_charts_for_multivariate_process_monitoring_images/One-class_classification-based_control_charts_for_multivariate_process_monitoring.pdf-0004-09.png)


For classification, a new observation **z** is classified as the target when _D_<sup>2</sup> is less than or equal to _R_<sup>2</sup> . 

To illustrate the control boundaries of SVDD, we generated a banana-shaped data set using a Matlab code available from PRTools (Duin _et al._ , 2007). The control boundaries with different values of parameters ( _f_ and _S_ ) in the SVDD algorithm were constructed from 180 in-control training observations (i.e., Phase I data). Figure 1 shows different SVDD boundaries embedded in two-dimensional plots of Phase I data. It can be seen from Figs. 1(a), (b) and (c) that given the same _f_ value ( _f_ = 0 _._ 01), the shape of the control boundary becomes smoother with larger _S_ . One can choose an appropriate _S_ that balances a trade-off between oversmoothness and undersmoothness of the control boundary. In the present study, we tried some potential values of _S_ and found the one that yields the smallest Type I and Type II error rates. Given the same _S_ value ( _S_ = 3), Figs. 1 (c), (d), (e) and (f) show that the control boundary becomes tighter to the volume centroid with the larger _f_ . 

###### **2.2.** **_Existing control chart methods based on the SVDD algorithm_** 

Several studies have implemented one-class classification methods in SPC problems. Sun and Tsung (2003) proposed K charts to handle non-normality problems by using the kernel distances obtained from the SVDD algorithm. They proposed to establish and adjust the control limits of the K chart by using _f_ (or _C_ ), one of the parameters of the SVDD algorithm. Kumar _et al._ (2006) proposed robust K charts, which are similar to K charts but use normalized kernel distances. One-class SVM-based control charts were applied for anomaly detection in computer networks (Zhang _et al._ , 2007). Although the aforementioned control charts use slightly different monitoring statistics, they are all based on the one-class SVM method. 

One-Class SVM (OC-SVM)-based control charts can be constructed by plotting monitoring statistics ( _D_<sup>2</sup> ) that measure the distance between new observations and the center of the hypersphere. The control limits ( _R_<sup>2</sup> ) of OC-SVM charts are determined by _f_ (or _C_ ). In other words, error rates in OC-SVM charts are adjusted by _f_ . Large _f_ values tend to yield a larger Type I error rate because the algorithm utilizes less training data inside the boundary. 

Figure 2 displays a _T_<sup>2</sup> chart and two OC-SVM charts corresponding to the control boundaries in Figs. 1 (b) and (c). In these figures, the monitoring statistics of 400 Phase II data were plotted (the first 360 are in control and the last 40 are out of control). Note that the control limits of these charts were established by 180 Phase I data. In the OC-SVM charts, it is interesting to observe that the userspecified _f_ value affects not only the determination of the control limits but also the calculation of the monitoring statistic. Note that two totally different control charts were obtained by changing the value of _f_ from 0.01 to 0.20 (Figs. 2(c) and (d)). This clearly demonstrates that _f_ is inappropriate for establishing the control limits in OC-SVM charts. This limitation can be explained by Fig. 1, which shows that completely different control boundaries were obtained by changing the value of _f_ from 0.01 to 0.20. As a consequence, an observation detected as being out of control (or in control) may no longer be detected as being out of control (or in control) as a reaction to the use of different values of _f_ . In contrast, _T_<sup>2</sup> charts use the controlling value _α_ that is independent of the monitoring statistic, _T_<sup>2</sup> . Thus, the ellipse boundary of _T_<sup>2</sup> always captures more out-of-control situations and yields a higher Type I error rate with a larger _α_ (Figs. 1(b) and (c)). Furthermore, the same values of monitoring statistics are plotted in the _T_<sup>2</sup> chart regardless of _α_ (Fig. 2(a)). 

###### **2.3.** **_New design strategy of OC-SVM charts based on the bootstrap method_** 

To address the limitation of the current OC-SVM control charts, we propose a new design strategy to establish the 

109 

_Sukchotrat_ et al. 

110 


![](One-class_classification-based_control_charts_for_multivariate_process_monitoring_images/One-class_classification-based_control_charts_for_multivariate_process_monitoring.pdf-0005-02.png)


**Fig. 1.** Control boundaries of SVDD obtained from different values of parameters: (a) _f_ = 0 _._ 01 and _s_ = 10; (b) _f_ = 0 _._ 01 and _s_ = 5; (c) _f_ = 0 _._ 01 and _s_ = 3; (d) _f_ = 0 _._ 20 and _s_ = 3; (e) _f_ = 0 _._ 5 and _s_ = 3; and (f) _f_ = 0 _._ 80 and _s_ = 3. 

_One-class classification algorithms for SPC_ 

111 


![](One-class_classification-based_control_charts_for_multivariate_process_monitoring_images/One-class_classification-based_control_charts_for_multivariate_process_monitoring.pdf-0006-02.png)


**Fig. 2.** _T_<sup>2</sup> and OC-SVM charts with the statistics and the control limits corresponding to the control boundaries in Figs. 1(c) and (d): (a) _T_<sup>2</sup> chart; (b) OC-SVM chart ( _f_ = 0 _._ 01, _s_ = 3); and (c) OC-SVM chart ( _f_ = 0 _._ 2, _s_ = 3). 

control limits in OC-SVM charts. We call the proposed chart _D_<sup>2</sup> charts. The control limits of _D_<sup>2</sup> charts are established and adjusted based on a percentile value estimated by the bootstrap method. The bootstrap method is a resampling method that is widely used to provide statistical estimates when the population distribution is unknown (Efron and Tibshirani, 1993). 

In traditional control charts, the control limits are determined based on the underlying distribution of the monitoring statistic with the user-specified value (e.g., Type I error rate). In contrast, the distribution of the monitoring statistic of a _D_<sup>2</sup> chart is unknown due to its non-parametric nature. This motivates us to develop an appropriate nonparametric procedure to establish the control limit. First, 

_D_<sup>2</sup> values (monitoring statistics) of Phase I observations of size _N_ are obtained through the SVDD algorithm. Second, we take _B_ bootstrap samplings and compute the percentile values of interest from each bootstrap sample of size _N_ drawn with replacement from _D_<sup>2</sup> values of Phase I observations. Finally, the control limit is determined by taking the average of _B_ percentile values. 

The following is a more explicit description of the bootstrap procedure to establish the control limits of the _D_<sup>2</sup> chart. 

- _Step 1._ Compute the _D_<sup>2</sup> statistics of Phase I observations of size _N_ using Equation (11) and generate _B_ independent bootstrap samples. Let _D_<sup>2</sup> _j_ 1<sup>_, D_2</sup> _j_ 2<sup>_, . . . , D_2</sup> _j N_ 

_Sukchotrat_ et al. 

112 


![](One-class_classification-based_control_charts_for_multivariate_process_monitoring_images/One-class_classification-based_control_charts_for_multivariate_process_monitoring.pdf-0007-02.png)


**Fig. 3.** (a) The _D_<sup>2</sup> chart; and (b) the corresponding control boundary. 

   - be a sequence of _N D_<sup>2</sup> statistics from the _j_ th bootstrap sample (for _j_ = 1 _, . . . , B_ ). 

- _Step 2._ For each bootstrap sample, given a user-specified _α_ (0 _< α_ ≤ 1) and the ordered _D_<sup>2</sup> values ( _D_<sup>2</sup> _j_ (1)<sup>_<_</sup> _D_<sup>2</sup><sup>_D_2</sup> _j_ (2)<sup>_<_· · ·</sup><sup>_<_</sup> _j_ ( _N_ )<sup>),</sup><sup>_D_2</sup> _j_ ( _i_ )<sup>is the</sup><sup>_i_th largest value of</sup> 

- _N D_<sup>2</sup> values in the _j_ th bootstrap sample where _i_ is a roundup number of _N_ × _α_ . 

- _Step 3._ Calculate the control limit ( _CL_ ) by taking average of the _i_ th largest values (i.e., 100(1 − _α_ )th percentile values) in each of _B_ bootstrap samples: _CL_ =<sup>�</sup><sup>_B_</sup> _j_ =1<sup>_D_2</sup> _j_ ( _i_ )<sup>_/B_.</sup> 

- _Step 4._ Monitoring Phase II observations: declare the observations out of control if the corresponding _D_<sup>2</sup> values exceed the control limit. 

Figure 3 displays the _D_<sup>2</sup> chart and the corresponding control boundary. In the _D_<sup>2</sup> control chart, 180 incontrol observations were used to estimate the control limits (bootstrap-based 99th and 80th percentiles of the _D_<sup>2</sup> statistics) and 400 _D_<sup>2</sup> statistics from Phase II observations were plotted. Figure 3(b) shows the corresponding control boundary generated from the _D_<sup>2</sup> chart in Fig. 3(a). It can be seen that by increasing the _α_ value from 0.01 to 0.20, more out-of-control observations were detected. 

cost, _D_<sup>2</sup> charts may not be efficient for a process that needs frequent retraining. In order to address this computational burden, we propose a new one-class classification-based control chart called a _K_<sup>2</sup> chart. The algorithm used in a _K_<sup>2</sup> chart requires about 5.42 seconds (on the same machine as the SVDD algorithm) to complete 4000 bivariate training observations. _K_<sup>2</sup> charts are based on a _k_ -Nearest Neighbors Data Description ( _k_ NNDD) method that solves one-class classification problems by estimating the local density of the data using a nearest neighbors algorithm (Breunig _et al._ , 2000; Tax, 2001). A brief description of the _k_ NNDD algorithm is presented in the following section. 

###### **3.1.** **_The kNNDD algorithm_** 

Let NN _i_ ( **z** ) be the _i_ th nearest-neighbor training observation of a data point **z** that needs to be classified (or monitored). Let _V_ be the volume of the hypersphere containing _i_ nearest-neighbor training observations. Let _N_ be the size of the training set. The local density of **z** can be determined by 


![](One-class_classification-based_control_charts_for_multivariate_process_monitoring_images/One-class_classification-based_control_charts_for_multivariate_process_monitoring.pdf-0007-12.png)


Similarly, the local density of NN _i_ ( **z** ) can be determined by 

##### **3.** **_k_ -nearest neighbors data description–based control charts** 


![](One-class_classification-based_control_charts_for_multivariate_process_monitoring_images/One-class_classification-based_control_charts_for_multivariate_process_monitoring.pdf-0007-15.png)


The SVDD algorithm involves an optimization problem that requires a high computational load during the training process. The SVDD algorithm requires around 4.06 hours in one of our machines to train the model using 4000 bivariate observations. Because of the high computational 

where NN _i_ (NN _i_ ( **z** )) is the _i_ th nearest neighbor of NN _i_ ( **z** ) in the same training set. The _k_ NNDD algorithm classifies **z** as the target class when the ratio of its local density of **z** (Equation (12)) to the local density of NN _i_ ( **z** ) (Equation (13)) is greater than or equal to one, which can be 

113 

##### _One-class classification algorithms for SPC_ 


![](One-class_classification-based_control_charts_for_multivariate_process_monitoring_images/One-class_classification-based_control_charts_for_multivariate_process_monitoring.pdf-0008-02.png)


**Fig. 4.** Control boundaries of _k_ NNDD (with different _k_ ) constructed from the banana-shaped data set. 

explained as follows: 


![](One-class_classification-based_control_charts_for_multivariate_process_monitoring_images/One-class_classification-based_control_charts_for_multivariate_process_monitoring.pdf-0008-05.png)


To make the algorithm more robust, the average of _k_ distances is considered (for _i_ = 1 _, . . . , k_ ). Thus, Equation (14) becomes: 


![](One-class_classification-based_control_charts_for_multivariate_process_monitoring_images/One-class_classification-based_control_charts_for_multivariate_process_monitoring.pdf-0008-07.png)


In the _k_ NNDD algorithm, the size of nearest neighbor, _k_ , affects its performance. Figure 4 displays the control boundaries obtained by _k_ NNDD with two different values 

of _k_ . The decision boundary with _k_ = 30 is fairly smooth compared to the control boundary obtained by using _k_ = 2. One can search possible values of _k_ and find an appropriate one that compromises a trade-off between oversmoothness and undersmoothness of the control boundary. A previous study indicated that the proper range of _k_ in the _k_ NNDD algorithm is between ten and 50 (Breunig _et al._ , 2000). 

###### **3.2.** **_K_**<sup>**_2_**</sup> **_charts_** 

To construct _K_<sup>2</sup> charts, the average distance between **z** and _k_ nearest observations is calculated as follows: 


![](One-class_classification-based_control_charts_for_multivariate_process_monitoring_images/One-class_classification-based_control_charts_for_multivariate_process_monitoring.pdf-0008-12.png)


_K_<sup>2</sup> values are then used as monitoring statistics. The control limits of a _K_<sup>2</sup> chart are obtained by the bootstrap percentile procedure as we proposed in _D_<sup>2</sup> charts (please see Section 2.3). Here is the detailed summary of the bootstrap percentile procedure for _K_<sup>2</sup> charts. 

- _Step 1._ Compute the _D_<sup>2</sup> statistics of Phase I observations of size _N_ using Equation (11) and generate _B_ independent bootstrap samples. Let _K_<sup>2</sup> _j_ 1<sup>_, K_2</sup> _j_ 2<sup>_, . . . , K_2</sup> _j N_ be a sequence of _N K_<sup>2</sup> statistics from the _j_ th bootstrap sample (for _j_ = 1 _, . . . , B_ ). 

- _Step 2._ For each bootstrap sample, given a user-specified _α_ (0 _< α_ ≤ 1) and the ordered _K_<sup>2</sup> values ( _K_<sup>2</sup> _j_ (1)<sup>_<_</sup> _K_<sup>2</sup><sup>_K_2</sup> _j_ (2)<sup>_<_· · ·</sup><sup>_<_</sup> _j_ ( _N_ )<sup>),</sup><sup>_K_2</sup> _j_ ( _i_ )<sup>is the</sup><sup>_i_th largest value of</sup> 

- _N K_<sup>2</sup> values in the _j_ th bootstrap sample where _i_ is a roundup number of _N_ × _α_ . 

- _Step 3._ Calculate the control limit ( _CL_ ) by taking average of the _i_ th largest values (i.e., 100(1 − _α_ )th 


![](One-class_classification-based_control_charts_for_multivariate_process_monitoring_images/One-class_classification-based_control_charts_for_multivariate_process_monitoring.pdf-0008-17.png)


**Fig. 5.** (a) The _K_<sup>2</sup> chart; and (b) the corresponding control boundary. 

_Sukchotrat_ et al. 

114 

percentile values) in each of _B_ bootstrap samples: _CL_ =<sup>�</sup><sup>_B_</sup> _j_ =1<sup>_K_2</sup> _j_ ( _i_ )<sup>_/B_.</sup> 

- _Step 4._ Monitor Phase II observations: declare the observations out of control if the corresponding _K_<sup>2</sup> values exceed the control limit. 

of the Phase II observations, showing that control charts become more sensitive as _α_ increases. 

##### **4. Simulation study** 

Figure 5 displays the _K_<sup>2</sup> chart ( _k_ = 30) and the corresponding control boundary from the banana-shaped data set. Two different control limits were calculated by estimated percentiles (99th and 80th) from 5000 bootstrap samples of 180 _K_<sup>2</sup> statistics. For monitoring Phase II observations, the _K_<sup>2</sup> value of each Phase II observation was plotted. Figure 5(b) displays the control boundaries corresponding to the control limits embedded in a two-dimensional plot 

###### **4.1.** **_Simulation setup_** 

A simulation study was conducted to compare the performance among _D_<sup>2</sup> , _K_<sup>2</sup> , _T_<sup>2</sup> and OC-SVM charts. We generated the data based on the bivariate normal, bivariate _t_ , bivariate gamma and a banana-shaped data set. For _D_<sup>2</sup> and OC-SVM charts, we used the width of Gaussian kernel, _S_ = 1 for the normal, _t_ , and gamma cases and _S_ = 3 for the banana-shaped data. For _K_<sup>2</sup> charts, we used _k_ = 30. 


![](One-class_classification-based_control_charts_for_multivariate_process_monitoring_images/One-class_classification-based_control_charts_for_multivariate_process_monitoring.pdf-0009-09.png)


**Fig. 6.** Average Type I and Type II error rates from: (a) _D_<sup>2</sup> ; (b) _K_<sup>2</sup> ; (c) _T_<sup>2</sup> ; and (d) OC-SVM charts ( _N_ 2 with _λ_ = 2 scenario). 

115 

##### _One-class classification algorithms for SPC_ 

One thousand Phase II observations (900 in control and 100 out of control) were monitored based on the control limits that were established by 200 Phase I observations. Let **µ** 0 and **_�_** 0 be the mean vector and the covariance matrix of the in-control data. Let **µ** 1 = **µ** 0 + **δ** be the mean vector of the out-of-control data. The magnitude of the shift _δ_ is represented by the following non-centrality parameter _λ_ 


![](One-class_classification-based_control_charts_for_multivariate_process_monitoring_images/One-class_classification-based_control_charts_for_multivariate_process_monitoring.pdf-0010-03.png)


To generate the out-of-control data for the bivariate normal, bivariate _t_ and bivariate gamma distributions, two types of mean shifts (i.e., the medium mean shift _λ_ = 2 and the large mean shift _λ_ = 3) were considered. At a certain value of _λ_ , all variables are shifted equally. Note that 

we do not consider the change in variance. We generated two different angles of banana shapes that represent the in-control and out-of-control data (please see Duin _et al._ (2007) for more details on generating the banana-shaped data set). The summary of simulation scenarios is described as follows. 

1. _N_ 2, _λ_ = 2: The medium-mean-shift case of the bivariate normal distribution with 


![](One-class_classification-based_control_charts_for_multivariate_process_monitoring_images/One-class_classification-based_control_charts_for_multivariate_process_monitoring.pdf-0010-07.png)


2. _N_ 2, _λ_ = 3: The large-mean-shift case of the bivariate normal distribution with 


![](One-class_classification-based_control_charts_for_multivariate_process_monitoring_images/One-class_classification-based_control_charts_for_multivariate_process_monitoring.pdf-0010-09.png)



![](One-class_classification-based_control_charts_for_multivariate_process_monitoring_images/One-class_classification-based_control_charts_for_multivariate_process_monitoring.pdf-0010-10.png)


**Fig. 7.** Average Type I and Type II error rates from: (a) _D_<sup>2</sup> ; (b) _K_<sup>2</sup> ; (c) _T_<sup>2</sup> ; and (d) OC-SVM charts ( _Gam_ 2(1 _,_ 1) with _λ_ = 2 scenario). 

_Sukchotrat_ et al. 

116 

3. _t_ 2(3), _λ_ = 2: The medium-mean-shift case of the bivariate _t_ distribution with three degrees of freedom. 

4. _t_ 2(3), _λ_ = 3: The large-mean-shift case of the bivariate _t_ distribution with three degrees of freedom. 

5. _Gam_ 2(1 _,_ 1), _λ_ = 2: The medium-mean-shift case of the bivariate gamma distribution with the shape and scale parameters, where both of them are one. 

6. _Gam_ 2(1 _,_ 1), _λ_ = 3: The large-mean-shift case of the bivariate gamma distribution with the shape and scale parameters, where both of them are one. 

7. Banana-shaped: A banana-shaped data set with two different angles. 

###### **4.2.** **_Control limits_** 

In contrast to existing OC-SVM charts that use the parameter _f_ of the SVDD algorithm to adjust the control limits, the control limits of _D_<sup>2</sup> and _K_<sup>2</sup> charts are adjusted by the percentile, which is estimated by the bootstrap method. Figures 6 and 7 show how actual Type I and Type II error rates in the _D_<sup>2</sup> , _K_<sup>2</sup> , _T_<sup>2</sup> and OC-SVM charts are controlled by the controlling factors ( _α_ or _f_ ), indicated in the _x_ -axes. We used the average values of actual Type I and Type II error rates from 100 simulation runs. The standard errors of 100 simulations are relatively small (between 0.02 and 0.06), demonstrating that 100 simulations are enough to draw the meaningful conclusion. We presented the results for only _N_ 2 and _Gam_ 2(1 _,_ 1) scenarios, respectively, as examples of normal and non-normal cases. In general, as the controlling factor increases, all control charts produced larger Type I error rates but produced smaller Type II error rates. The particularly strong positive correlation between 

the actual Type I error rate and the controlling factor is desired. The proposed _D_<sup>2</sup> and _K_<sup>2</sup> charts satisfy this condition in both normal and non-normal cases, but _T_<sup>2</sup> charts satisfy this condition in only normal cases. In both normal and non-normal cases, OC-SVM charts failed to provide strong linear correlation between the actual Type I error rate and the controlling factor. Moreover, Type I and Type II error rates may not be properly controlled by _f_ as the size of target observations goes up in OC-SVM charts. Figure 8 shows OC-SVM charts constructed from the _N_ 2 with _λ_ = 2 scenario using 300 and 400 target observations. It can be observed that Type I and Type II error rates seem to be constant over the different values of _f_ . As we defined earlier in Equation (4), _f_ represents the fraction of the target data outside the decision boundary and has an inverse relationship with the total number of target observations. Thus, with the large number of target observations, the fraction of the target data ( _f_ ) only plays a small role in changing the control boundary, leading to relatively constant Type I and Type II error rates. These demonstrate that _f_ is an inappropriate choice as the controlling factor in OC-SVM charts. 

###### **4.3.** **_Performance comparisons_** 

The average values of Type I and Type II error rates from 100 simulation runs among _D_<sup>2</sup> , _K_<sup>2</sup> , _T_<sup>2</sup> and OC-SVM charts were compared. The control chart that yields a lower Type II error rate is considered a better method if the Type I error rate is similar. Figure 9 displays the average rates of Type I and Type II error under all the simulation scenarios studied. 


![](One-class_classification-based_control_charts_for_multivariate_process_monitoring_images/One-class_classification-based_control_charts_for_multivariate_process_monitoring.pdf-0011-12.png)


**Fig. 8.** Average Type I and Type II error rates from OC-SVM charts when the number of Phase I observations is large ( _N_ 2 with _λ_ = 2 scenario): (a) 300 observations; and (b) 400 observations. 

_One-class classification algorithms for SPC_ 

117 


![](One-class_classification-based_control_charts_for_multivariate_process_monitoring_images/One-class_classification-based_control_charts_for_multivariate_process_monitoring.pdf-0012-02.png)


**Fig. 9.** Type I and Type II error rates of the _D_<sup>2</sup> , _K_<sup>2</sup> , _T_<sup>2</sup> and OC-SVM charts for the studied simulation scenarios: (a) _N_ 2 with _λ_ = 2 scenario; (b) _N_ 2 with _λ_ = 3 scenario; (c) _t_ 2 (3) with _λ_ = 2 scenario; (d) _t_ 2 (3) with _λ_ = 3 scenario; (e) _Gam_ 2 (1, 1) with _λ_ = 2 scenario; (f) _Gam_ 2 (1, 1) with _λ_ = 3 scenario; and (g) banana-shaped scenario. 

_Sukchotrat_ et al. 

118 

**Table 1.** Average values of Type I error rate ( _α_ ) and Type II error rate ( _β_ ) of the _D_<sup>2</sup> chart the _K_<sup>2</sup> chart and the recursive _T_<sup>2</sup> in Phase I application (average values of standard errors are shown inside the parentheses) 

||_D_|<sup>_2_</sup>|_K_|<sup>_2_</sup>|_T_|<sup>_2_</sup>|
|---|---|---|---|---|---|---|
|_Scenarios_|_α_|_β_|_α_|_β_|_α_|_β_|
|_N_2,_λ_=2|0.1869|0.3630|0.1829|0.3485|0.1892|0.3865|
||(0.0128)|(0.0994)|(0.0124)|(0.1065)|(0.0566)|(0.1354)|
|_N_2,_λ_=3|0.2124|0.0800|0.2183|0.0825|0.2137|0.0915|
||(0.0103)|(0.0674)|(0.0097)|(0.0561)|(0.0664)|(0.0810)|
|_t_2(3),_λ_=2|0.2219|0.6830|0.2144|0.6790|0.2248|0.7165|
||(0.0119)|(0.0932)|(0.0122)|(0.0970)|(0.0426)|(0.1071)|
|_t_2(3),_λ_=3|0.2038|0.6290|0.1995|0.6375|0.2069|0.6230|
||(0.0132)|(0.0949)|(0.0126)|(0.1013)|(0.0444)|(0.1436)|
|_Gam_2(1),_λ_=2|0.1996|0.2410|0.2101|0.2825|0.2089|0.3250|
||(0.0171)|(0.1307)|(0.0140)|(0.1196)|(0.0596)|(0.1969)|
|_Gam_2(1),_λ_=3|0.2204|0.0380|0.2208|0.0715|0.2335|0.1200|
||(0.0100)|(0.0556)|(0.0116)|(0.0905)|(0.0781)|(0.1482)|
|Banana-shaped|0.1751|0.1680|0.1771|0.0865|0.1791|0.2380|
||(0.0118)|(0.0886)|(0.0127)|(0.0721)|(0.1026)|(0.1211)|



The result shows that the _D_<sup>2</sup> and _K_<sup>2</sup> charts produced smaller Type II error rates than the _T_<sup>2</sup> chart, given similar Type I error rates in the gamma and banana-shaped data scenarios. In the normal and _t_ cases, all methods provide comparable performances. The range of standard errors of 100 simulation is between 0.02 and 0.08 for the normal, _t_ and gamma cases, while much larger standard errors were obtained from OC-SVM (between 0.10 and 0.26). It should be noted that OC-SVM charts produce irregular Type II error rates over Type I error rates. Consequently, it is difficult to compare the performance of OC-SVM with other charts. 

##### **5. Phase I application of** **_D_**<sup>**2**</sup> **and** **_K_**<sup>**2**</sup> **charts** 

Phase I analysis separates the in-control data from the historical data set, which is a mixture of in-control and out-ofcontrol data, in order to establish the reliable control limits for monitoring future observations. A simulation study was conducted to show the applicability of _D_<sup>2</sup> and _K_<sup>2</sup> charts for Phase I problems. We compared the performance of the _D_<sup>2</sup> and _K_<sup>2</sup> charts with the existing Phase I method that recursively removes the observations that exceed the control limits until no out-of-control observations are detected. In multivariate processes, this recursive procedure is performed by Hotelling’s _T_<sup>2</sup> control chart in the Phase I application (Montgomery, 2005). 

We generated 200 historical observations from the bivariate normal, bivariate _t_ , and bivariate gamma distributions and a banana-shaped data set. We assigned 20 observations (out of 200) to be out of control where two different non-centrality parameters, _λ_ = 2 and _λ_ = 3, were used for the bivariate normal, bivariate _t_ and bivariate gamma distributions. For the banana-shaped data set, two different 

angles of banana shapes were used to represent the incontrol and out-of-control data. The _D_<sup>2</sup> and _K_<sup>2</sup> charts were constructed with all 200 observations. The control charts removed the historical observations in which the statistics exceed the control limits. Analogous to _D_<sup>2</sup> and _K_<sup>2</sup> charts for Phase II analysis, 100(1 − _α_ )th bootstrap percentiles of the _D_<sup>2</sup> and _K_<sup>2</sup> statistics of the historical data were used as control limits in Phase I analysis. The remaining observations were defined as being in control. The observations that were actually in control but incorrectly removed were Type I errors. The remaining observations that were actually out of control were Type II errors. 

We compared the performances of the _D_<sup>2</sup> and _K_<sup>2</sup> charts with the recursive _T_<sup>2</sup> in terms of Type I and Type II error rates (average values from 100 simulation runs). Table 1 shows that the performances of the _D_<sup>2</sup> and _K_<sup>2</sup> charts are slightly better than recursive _T_<sup>2</sup> under the normal and _t_ scenarios but they are comparable. Because Hotelling’s _T_<sup>2</sup> chart can effectively handle multivariate normal data, the recursive _T_<sup>2</sup> is also an appropriate method in normal distribution cases of Phase I analysis. However, in the gamma and banana-shaped data scenarios, the _D_<sup>2</sup> and _K_<sup>2</sup> charts produced smaller Type II error rates than the recursive _T_<sup>2</sup> method. This clearly demonstrates that _D_<sup>2</sup> and _K_<sup>2</sup> charts are effective approaches to use for Phase I analysis in both normal and non-normal cases. 

##### **6. Conclusions** 

We have proposed new multivariate control charts based on one-class classification algorithms. The proposed _D_<sup>2</sup> and _K_<sup>2</sup> charts obtain their monitoring statistics from the SVDD and _k_ NNDD algorithms. The control limits 

119 

##### _One-class classification algorithms for SPC_ 

are derived from the bootstrap-estimated percentile of monitoring statistics. The proposed control charts, because of their data-driven nature, can effectively describe reality, reflect the unique characteristics of the data being monitored, and require a minimal set of assumptions to construct a control chart. The comparative study from the simulated data shows that performances of the _D_<sup>2</sup> and _K_<sup>2</sup> charts were comparable to _T_<sup>2</sup> charts in the normal distribution case. However, _D_<sup>2</sup> and _K_<sup>2</sup> charts outperformed _T_<sup>2</sup> charts in non-normal distribution cases. Moreover, we demonstrated the applicability and effectiveness of the _D_<sup>2</sup> and _K_<sup>2</sup> chart techniques for Phase I problems. There are several interesting directions for future research. One such direction is to extend our study to other one-class classification methodologies. Another research directions to develop more efficient ways to establish control limits. A more comprehensive simulation study should be conducted to evaluate the efficacy and consequences of various scenarios, including the impact of variance changes. 

##### **Acknowledgements** 

We thank the department editor and the referees for the constructive comments and suggestions, which greatly improved the quality of the paper. Dr. Tsung’s work was supported by RGC Competitive Earmarked Research Grants 620707 and 620508. 

- Hwang, W.Y., Runger, G. and Tuv, E. (2005) Multivariate statistical process control with artificial contrasts. _IIE Transactions_ , **39** (6), 659–669. 

- Kim, S.H., Alexopoulos, C., Tsui, K.L. and Wilson, J.R. (2007) A distribution-free tabular CUSUM chart for autocorrelated data. _IIE Transactions_ , **39** (3), 317–330. 

- Kumar, S., Choudhary, A.K., Kumar, M., Shankar, R. and Tiwari, M.K. (2006) Kernel distance-based robust support vector methods and its application in developing a robust K-chart. _International Journal of Production Research_ , **44** (1), 77–96. 

- Liu, R.Y., Singh, K. and Teng, J.H. (2004) DDMA-charts: nonparametric multivariate moving average control charts based on data depth. _Allgemeines Statistisches Archiv_ , **88** (2), 235–258. 

- Lowry, C.A. and Montgomery, D.C. (1995) A review of multivariate control charts. _IIE Transactions_ , **27** (6), 800–810. 

- Mason, R.L. and Young, J.C. (2002) _Multivariate Statistical Process Control with Industrial Applications_ , American Statistical Association and Society for Industrial and Applied Mathematics, Philadelphia, PA. 

- Montgomery, D.C. (2005) _Introduction to Statistical Quality Control_ , fifth edition, Wiley, New York, NY. 

- Qiu, P. (2008) Distribution-free multivariate process control based on log-linear modeling. _IIE Transactions_ , **40** (7), 664–677. 

- Smith, A.E. (1994) _X_ and _R_ control chart interpretation using neural computing. _International Journal of Production Research_ , **32** (2), 309– 320. 

- Stoumbos, Z.G., Reynolds, M.R., Ryan, T.P. and Woodall, W.H. (2000) The state of statistical process control as we proceed into the 21st century. _Journal of the American Statistical Association_ , **95** , 992–998. 

- Sun, R. and Tsung, F. (2003) A kernel-distance-based multivariate control chart using support vector methods. _International Journal of Production Research_ , **41** (13), 2975–2989. 

- Tax, D.M.J. (2001) One-class classification: concept-learning in the absence of counter-examples. PhD thesis, Delf University of Technology, The Netherlands. 

- Tax, D.M.J. and Duin, R.P.W. (2004) Support vector data description. _Machine Learning_ , **54** (1), 45–66. 

- Vapnik, V.N. (1998) _Statistical Learning Theory_ , Wiley, New York, NY. 

##### **References** 

- Bakir, S. (2006) Distribution-free quality control charts based on signedrank-like statistics. _Communications in Statistics: Theory and Methods_ , **35** , 743–757. 

- Breunig, M.M., Kriegel, H.P., Ng, R.T. and Sander, J. (2000) LOF: identifying density-based local outliers, in _Proceedings of the ACM SIGMOD 2000 International Conference on Management of Data_ , pp. 93–104. 

- Chakraborti, S., Van der Laan, P. and Bakir, S.T. (2001) Nonparametric control chart: an overview and some results. _Journal of Quality Technology_ , **33** (3), 304–315. 

- Chinnam, R.B. (2002) Support vector machines for recognizing shifts in correlated and other manufacturing processes. _International Journal of Production Research_ , **40** (17), 4449–4466. 

- Cook, D.F. and Chiu, C.C. (1998) Using radial basis function neural networks to recognize shifts in correlated manufacturing process parameters. _IIE Transactions_ , **30** (3), 227–234. 

- Duin, R.P.W., Juszczak, P., Paclik, P., Pekalska, E., De Ridder, D. and Tax, D.M.J. (2007) PRTools4: the Matlab Toolbox for pattern recognition, available at http://www.prtools.org/, accessed November 2007. 

- Efron, B. and Tibshirani, R. (1993) _An Introduction to the Bootstrap_ , Chapman & Hall/CRC, Boca Raton, FL. 

- Hotelling, H. (1947) Multivariate quality control, in _Techniques of Statistical Analysis_ , Eisenhart, C., Hastay, M.W. and Wills, W.A. (eds), McGraw-Hill, New York, NY, pp. 111–184. 

- Hu, J., Gunger, G. and Tuv, E. (2007) Tuned artificial contrasts to detect signals. _International Journal of Production Research_ , **23** (1), 5527– 5534. 

- Woodall, W.H. (2000) Controversies and contradictions in statistical process control. _Journal of Quality Technology_ , **32** (4), 341–350. 

- Woodall, W.H. and Montgomery, D.C. (1999) Research issues and ideas in statistical process control. _Journal of Quality Technology_ , **31** (4), 376–386. 

- Zhang, H. and Albin, S. (2007) Determining the number of operational modes in baseline multivariate SPC data. _IIE Transactions_ , **39** (12), 1103–1110. 

- Zhang, Z., Zhu, X. and Jin, J. (2007) SVC-based multivariate control charts for automatic anomaly detection in computer networks, in _Proceedings of the Third International Conference on Autonomic and Autonomous Systems_ . 

##### **Biographies** 

Thuntee Sukchotrat is a Faculty Associate Researcher in the Industrial and Manufacturing Systems Engineering Department at the University of Texas at Arlington (UTA). He received a B.E. in Industrial Engineering from Chulalongkorn University, Thailand, and an M.S. and a Ph.D. in Industrial Engineering from UTA. His main research interests include data mining and statistical process control. 

Seoung Bum Kim is an Assistant Professor in the Department of Information Management Engineering at Korea University. From 2005 to 2009, he was a faculty member of the Industrial and Manufacturing Systems Engineering Department at the University of Texas at Arlington. He received an M.S. in Industrial and Systems Engineering in 2001, an M.S. in Statistics in 2004 and a Ph.D. in Industrial and Systems Engineering at the Georgia Institute of Technology. He was awarded the Jack 

_Sukchotrat_ et al. 

120 

Youden Prize as the best expository paper in _Technometrics_ for the Year 2003. He is a member of the Institute for Industrial Engineers, Institute for Operations Research and Management Science and the Institute of Mathematical Statistics. He is actively involved in the Data Mining cluster and Quality, Reliability, and Statistics cluster by presenting papers and chairing sessions at the INFORMS annual and international meetings. He has also served as a council member, a newsletter editor, and a web editor of the INOFRMS Section on Data Mining. His research interests are theory and applications of data mining algorithms and statistical quality control. 

Fugee Tsung is Professor and Head of the Department of Industrial Engineering and Logistics Management (IELM), Director of the Quality Laboratory, at the Hong Kong University of Science & Technology 

(HKUST). He received both his M.Sc. and Ph.D. from the University of Michigan, Ann Arbor. He is currently Associate Editor of _Technometrics_ , Department Editor of the _IIE Transactions_ , and on the Editorial Boards for _Quality and Reliability Engineering International_ , the _International Journal of Reliability, Quality and Safety Engineering_ , among others. He is an ASQ Certified Six Sigma Black Belt, ASQ authorized Six Sigma Master Black Belt Trainer, Co-founder and Chair of the Service Science Section at the Institute for Operations Research and the Management Sciences (INFORMS), and Regional Vice President (Asia) of the Institute of Industrial Engineers. He has authored over 70 refereed journal publications, and is also the winner of the Best Paper Award for the _IIE Transactions_ in 2003. His research interests include quality engineering and management to manufacturing and service industries, statistical process control, monitoring and diagnosis. 

