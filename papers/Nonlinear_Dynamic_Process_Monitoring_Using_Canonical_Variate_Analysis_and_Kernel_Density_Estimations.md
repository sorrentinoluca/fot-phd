36 

IEEE TRANSACTIONS ON INDUSTRIAL INFORMATICS, VOL. 6, NO. 1, FEBRUARY 2010 

# Nonlinear Dynamic Process Monitoring Using Canonical Variate Analysis and Kernel Density Estimations 

Pabara-Ebiere Patricia Odiowei and Yi Cao _, Member, IEEE_ 

**_Abstract—_ The Principal Component Analysis (PCA) and the Partial Least Squares (PLS) are two commonly used techniques for process monitoring. Both PCA and PLS assume that the data to be analysed are not self-correlated i.e. time-independent. However, most industrial processes are dynamic so that the assumption of time-independence made by the PCA and the PLS is invalid in nature. Dynamic extensions to PCA and PLS, so called DPCA and DPLS, have been developed to address this problem, however, unsatisfactorily. Nevertheless, the Canonical Variate Analysis (CVA) is a state-space-based monitoring tool, hence is more suitable for dynamic monitoring than DPCA and DPLS. The CVA is a linear tool and traditionally for simplicity, the upper control limit (UCL) of monitoring metrics associated with the CVA is derived based on a Gaussian assumption. However, most industrial processes are nonlinear and the Gaussian assumption is invalid for such processes so that CVA with a UCL based on this assumption may not be able to correctly identify underlying faults. In this work, a new monitoring technique using the CVA with UCLs derived from the estimated probability density function through kernel density estimations (KDEs) is proposed and applied to the simulated nonlinear Tennessee Eastman Process Plant. The proposed CVA with KDE approach is able to significantly improve the monitoring performance and detect faults earlier when compared to other methods also examined in this study.** 

**_Index Terms—_ Canonical variate analysis (CVA), kernel density estimation (KDE), probability density function (PDF), process monitoring.** 

## I. INTRODUCTION 

**P** ROCESS monitoring is essential to maintain high qualityproducts as well as process safety. Widely applied process monitoring techniques like the Principal Component Analysis (PCA) and the Partial Least Square (PLS) rely on static models, which assume that the observations are time independent and follow a Gaussian distribution. However, the assumptions of time-independence and normality are invalid for most chemical processes because variables driven by noise and disturbances are strongly autocorrelated and most plants are nonlinear in na- 

Manuscript received December 30, 2008; revised April 23, 2009 and July 13, 2009; accepted August 23, 2009. First published October 20, 2009; current version published February 05, 2010. The work of P.-E. Patricia Odiowei was supported by the Petroleum Technology Development Fund (PTDF) of the Federal Republic of Nigeria while at Cranfield University, U.K. Paper no. TII-08-12-0231. 

The authors are with the Department of Process and Systems Engineering, School of Engineering, Cranfield University, Cranfield MK43 0AL, U.K. (e-mail: p.odiowei@cranfield.ac.uk; y.cao@cranfield.ac.uk). 

Color versions of one or more of the figures in this paper are available online at http://ieeexplore.ieee.org. Digital Object Identifier 10.1109/TII.2009.2032654 

ture. Therefore, the static PCA and PLS-based approaches are inappropriate to monitor such nonlinear dynamic processes. 

To extend PCA applications to dynamic systems, Ku _et al._ [1] presentedastudyofPCAonlaggedvariablestodevelopdynamic modelsandMultivariateStatisticalProcessMonitoring(MSPM) tools for dynamic continuous processes. In this so called Dynamic PCA (DPCA) approach, Ku _et al._ [1] used parallel analysistodeterminethenumberoftime-laggedvaluefortheprocess variables as well as the number of principal components to retain in the DPCA model. Although dynamic models are developed in DPCA and faults are detected, diagnosis of abnormal behavior is more complicated with DPCA given that lagged variables are involved [2].It isalsoreportedthat principalcomponentsextracted in this way are not necessarily the minimal dynamic representations [3]. Furthermore, Komulainen [4] extended PLS applications to dynamic systems, in a similar way to the DPCA, for the monitoring of an online industrial dearomatization process. The extended PLS approach is known as the Dynamic PLS (DPLS). Although the DPLS technique was reported to be efficient for fault detection, like the DPCA, the capability of the DPLS to identify dynamic faults is still questionable because the way of the DPCA and DPLS to represent a dynamic system is not efficient and may not be able to capture some important dynamic behaviors of the system. 

More recently, monitoring techniques based on Canonical Variate Analysis (CVA) have been developed with UCLs derived based on the Gaussian assumption [5]–[7]. CVA was first introduced in 1936 by Hotelling [7], adopted for use in dynamic systems for a limited class of processes by Akaike in 1975 [7], [8] and adapted to general linear systems by Larimore in 1983 [8]. CVA is a state-space-based MSPM method, hence is more appropriate for dynamic process monitoring. 

Norvalis _et al._ [7] developed a process monitoring and fault diagnosis tool that combined canonical variate state-space (CVSS) models with knowledge-based systems (KBSs) for monitoring multivariate process operations. Faults were detected using the CVSS models and then UCLs derived based on the Gaussian assumption, while diagnosis was based on the KBS. The efficiency of the technique was illustrated by monitoring simulated data of a polymerization reactor system. 

Juan and Fei [6] employed CVA for fault detection based on Hotelling’s charts to monitor a chemical separation plant. The results from the study illustrated a good performance of the statistical model based on CVA. Furthermore, it was demonstrated that the precision of the CVA model improved with an increase in the length of the data employed for the CVA analysis. 

1551-3203/$26.00 © 2009 IEEE Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on September 11,2026 at 18:11:40 UTC from IEEE Xplore.  Restrictions apply. 

ODIOWEI AND CAO: NONLINEAR DYNAMIC PROCESS MONITORING USING CANONICAL VARIATE ANALYSIS AND KERNEL DENSITY ESTIMATIONS 

37 

Different from the above mentioned studies, Chiang _et al._ [5] employed canonical variate analysis to include the input and output variables for the estimation of the state-space variable. From the estimated state-space variable, UCLs of and metrics were determined to judge whether or not those processes were in control. 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0002-03.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0002-04.png)


The and metrics are widely employed with various MSPM techniques [1], [3], [5], [9]–[12]. For linear MSPM techniques, such as PCA, PLS and CVA, traditionally, UCLs of the and metrics are estimated based on an assumption that the latent or state variables follow a Gaussian distribution. However, most industrial processes are nonlinear. For such processes, although the distribution of stochastic sources might be Gaussian, such as measurement noises and normally distributed disturbances, the distribution of process variables, in general, will be non-Gaussian. In such a case, the UCL estimated based on the Gaussian assumption is unable to correctly identify underlying faults. 

The problem of monitoring non-Gaussian processes can be addressed by directly estimating the underlying probability density function (PDF) of the and metrics through the kernel density estimation (KDE) to derive the correct UCL [13], [14]. 

Martin and Morris [13] presented an overview of multivariate process monitoring techniques using the PCA and the PLS with and metrics for process monitoring. The control limit of metric was estimated based on the PDF, combining techniques of standard bootstrap and KDEs to overcome the limitations of the metric mentioned above. Both methodologies were applied to a continuous polyethylene reactor and a polymerization reactor to demonstrate the efficiencies of both methodologies and the metric was reported to be a more efficient process monitoring tool than the metric. 

Chen _et al._ [14] adopted several KDE approaches in association with PCA for process monitoring. A gas melter process was used as the case study and it was demonstrated that the KDEs could obtain nonparametric empirical density function as a tool for a more efficient process monitoring. Their emphasis was to demonstrate the efficiencies of three different density estimators which were verified based on the misclassification rates at given 

In order to use the linear dynamic tools, such as the CVA to monitor nonlinear dynamic processes, the limitation of the Gaussian assumption-based and metrics mentioned above has to be addressed. In this paper, KDE is employed in association with the CVA resulting in a new extension of the CVA algorithm, the “CVA with KDE” for process monitoring. To achieve this, a CVA model is firstly estimated from the so called past and future variables constructed from the collected process data. From the estimated CVA model, the and metrics are then calculated and the KDE is employed to estimate the PDF of these and metrics calculated. UCLs are then determined based on the estimated PDF for a given confidence bound. For comparison, different monitoring algorithms; DPCA and DPLS with and without KDE as well as CVA with and without KDE have been applied to the simulated nonlinear Tennessee Eastman Process Plant in the present study. Results show that the monitoring performance is significantly improved by using the “CVA with KDE” approach compared with other mon- 

itoring algorithms aforementioned. Although the CVA is a linear model, in this study, the CVA is employed to monitor a nonlinear dynamic process plant. Hence, this study is described as nonlinear dynamic process monitoring. 

The rest of the paper is organized as follows: Section II explains the CVA model, while Section III describes monitoring metrics and their UCLs derived through KDEs. The procedure of CVA with KDE is then summarized in Section IV. Section V describes the case study, while the results of the case study are presented and discussed in Section VI. Finally, the work is concluded in Section VII. 

## II. CANONICAL VARIATE ANALYSIS (CVA) 

Canonical Variate Analysis (CVA) is a linear dimension reduction technique to construct a minimum state-space model for dynamic process monitoring. This section applies the linear CVA algorithm to a nonlinear dynamic plant for identifying state variables directly from the process measurements. Assume the nonlinear dynamic plant under consideration represented as follows: 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0002-14.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0002-15.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0002-16.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0002-17.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0002-18.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0002-19.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0002-20.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0002-21.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0002-22.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0002-23.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0002-24.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0002-25.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0002-26.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0002-27.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0002-28.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0002-29.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0002-30.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0002-31.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0002-32.png)


where and are state and measurement vectors, respectively, and are unknown nonlinear functions, whereas and are plant disturbances and measurement noise vectors, respectively. It is clear that such an unknown nonlinear dynamic system is generally difficult to deal with for monitoring. However, at a stable normal operating point, the nonlinear plant can be approximated by a linear stochastic statespace model as follows: 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0002-34.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0002-35.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0002-36.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0002-37.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0002-38.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0002-39.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0002-40.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0002-41.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0002-42.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0002-43.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0002-44.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0002-45.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0002-46.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0002-47.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0002-48.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0002-49.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0002-50.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0002-51.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0002-52.png)


where and are unknown state and output matrices, respectively, whereas and are collective modeling errors partially due to the underlying nonlinearity of the plant which has not been included in the linear model, as well as associated with process disturbance and measurement noise, and , respectively. Due to the unknown nonlinearity, the collective modeling errors, and generally will be non-Gaussian although and might be normally distributed processes. This is the main difference of this work from other CVA-based approaches reported in literature. Instead of dealing with the unknown nonlinear system (1) directly, in this work, the approximated linear state-space model given in (2) is considered through the standard CVA approach. Although the linear model (2) is easier to deal with than the nonlinear system (1), the collective errors and have to be treated as non-Gaussian processes. This leads to the direct PDF estimation of the associated and metrics through the KDE approach explained in Section III. 

In the CVA approach, first, the measurement vector is expanded by past and future measurements to give the past and future observation vectors and , respectively 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0002-55.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0002-56.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0002-57.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0002-58.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0002-59.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0002-60.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0002-61.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0002-62.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0002-63.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0002-64.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0002-65.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0002-66.png)


Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on September 11,2026 at 18:11:40 UTC from IEEE Xplore.  Restrictions apply. 

IEEE TRANSACTIONS ON INDUSTRIAL INFORMATICS, VOL. 6, NO. 1, FEBRUARY 2010 

38 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-02.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-03.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-04.png)


trix, and the maximal correlation is the corresponding singular value of . If the rank of the scaled Hankel matrix, is , then there are nonzero singular values, , in the descending order and correspondingly pairs of the left and right singular vectors, and for . Singular values and vectors can be collected in the following matrix form of the singular value decomposition (SVD) 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-06.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-07.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-08.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-09.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-10.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-11.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-12.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-13.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-14.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-15.png)


where and are the sample means of and , respectively, and the products of represents the lengths of the past and future observation vectors, respectively. The length of the past and future observations can be determined by checking the autocorrelation of the square sum of the process variables such that the correlation can be neglected when the time distance is larger than the number of lags determined. 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-17.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-18.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-19.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-20.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-21.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-22.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-23.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-24.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-25.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-26.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-27.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-28.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-29.png)


where 

These past and future observations are stochastic processes. Their sample-based covariance and cross-covariance matrices can be estimated through the truncated Hankel matrices as follows: 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-32.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-33.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-34.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-35.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-36.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-37.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-38.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-39.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-40.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-41.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-42.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-43.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-44.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-45.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-46.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-47.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-48.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-49.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-50.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-51.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-52.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-53.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-54.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-55.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-56.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-57.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-58.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-59.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-60.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-61.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-62.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-63.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-64.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-65.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-66.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-67.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-68.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-69.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-70.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-71.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-72.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-73.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-74.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-75.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-76.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-77.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-78.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-79.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-80.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-81.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-82.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-83.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-84.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-85.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-86.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-87.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-88.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-89.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-90.png)


Furthermore, the canonical variates can be directly estimated from the past observation vector as illustrated in (14) 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-92.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-93.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-94.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-95.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-96.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-97.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-98.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-99.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-100.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-101.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-102.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-103.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-104.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-105.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-106.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-107.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-108.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-109.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-110.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-111.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-112.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-113.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-114.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-115.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-116.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-117.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-118.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-119.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-120.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-121.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-122.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-123.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-124.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-125.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-126.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-127.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-128.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-129.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-130.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-131.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-132.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-133.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-134.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-135.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-136.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-137.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-138.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-139.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-140.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-141.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-142.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-143.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-144.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-145.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-146.png)


where and are past and future truncated -column Hankel matrices respectively, and defined as follows: 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-148.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-149.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-150.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-151.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-152.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-153.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-154.png)


where is the transformation matrix, which transforms the -dimensional past measurements to the -dimensional canonical variates. These canonical variates are normalized with a unit sample covariance 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-156.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-157.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-158.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-159.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-160.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-161.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-162.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-163.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-164.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-165.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-166.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-167.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-168.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-169.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-170.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-171.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-172.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-173.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-174.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-175.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-176.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-177.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-178.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-179.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-180.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-181.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-182.png)


For a set of measurements with total observations, the last element of in (3) is , whereas the last element of in (4) should be . Therefore, the maximum number of columns of these Hankel matrices is 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-184.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-185.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-186.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-187.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-188.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-189.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-190.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-191.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-192.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-193.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-194.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-195.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-196.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-197.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-198.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-199.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-200.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-201.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-202.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-203.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-204.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-205.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-206.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-207.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-208.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-209.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-210.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-211.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-212.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-213.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-214.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-215.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-216.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-217.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-218.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-219.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-220.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-221.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-222.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-223.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-224.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-225.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-226.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-227.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-228.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-229.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-230.png)


The CVA aims to find the best linear combinations, and of the future and past observations so that the correlation between these combinations is maximized. The correlation can be represented as follows: 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-232.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-233.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-234.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-235.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-236.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-237.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-238.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-239.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-240.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-241.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-242.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-243.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-244.png)


From (14), the canonical variate space spanned by all the estimated canonical variates can be separated into the state-space and the residual space based on the order of the system. According to the magnitude of the singular values, the first dominant singular values are determined and the corresponding canonical variates retained as the state variables where . In addition, the remaining canonical variates are said to be in the residual space. Equation (15) shows the entire canonical variate space spanned by the state variables and the residual canonical variates 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-246.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-247.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-248.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-249.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-250.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-251.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-252.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-253.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-254.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-255.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-256.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-257.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-258.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-259.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-260.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-261.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-262.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-263.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-264.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-265.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-266.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-267.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-268.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-269.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-270.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-271.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-272.png)


Let and . The optimization problem can be casted as 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-274.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-275.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-276.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-277.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-278.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-279.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-280.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-281.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-282.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-283.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-284.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-285.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-286.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-287.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-288.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-289.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-290.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-291.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-292.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-293.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-294.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-295.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-296.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-297.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-298.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-299.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-300.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-301.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-302.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-303.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-304.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-305.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-306.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-307.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-308.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-309.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-310.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-311.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-312.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-313.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-314.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-315.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-316.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-317.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-318.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0003-319.png)


The state variables are a subset of the canonical variates estimated in (14). Hence, the state variable like the canonical variates is defined as a linear combination of the past obser- 

According to linear algebra theory, the solution, and estimated in (14). Hence, the state variable like the canonare left and right singular vectors of the scaled Hankel maical variates is defined as a linear combination of the past obserAuthorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on September 11,2026 at 18:11:40 UTC from IEEE Xplore.  Restrictions apply. 

ODIOWEI AND CAO: NONLINEAR DYNAMIC PROCESS MONITORING USING CANONICAL VARIATE ANALYSIS AND KERNEL DENSITY ESTIMATIONS 39 

vation vector , , where consisting of the first columns defined in (13). 

, where with 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-03.png)


Like the canonical variates, the state variables also have the unit covariance. Once the states of the system are determined, the state and output matrices, and can then be estimated through linear least squares regression. However, the determination of the state and output matrices and will be omitted from the rest of the paper since these matrices will not be used in this work. 

The variation of state variables can be represented by the metric. Another commonly used monitoring metric is the metric which measures the total sum of square errors of the variations in the residual space. The estimation and use of the and metrics are explained in the next section. 

## III. CONTROL LIMIT THROUGH KERNEL DENSITY ESTIMATIONS (KDES) 

Traditionally, it was assumed that and are normally distributed, as well as the state, measurement and residual vectors, , and since a linear combination of multivariate Gaussian variables is also normally distributed. 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-08.png)


For samples of data, the number of samples of the states available is , given in (10). For the normally distributed -dimensional state vector, with samples, , , statistic defined in (16) can be used to test whether the mean of is at the desired target 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-10.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-11.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-12.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-13.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-14.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-15.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-16.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-17.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-18.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-19.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-20.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-21.png)


where is the estimated covariance of . If , then , where . Therefore, the system (2) can be monitored by plotting against time, , along with a UCL, corresponding to a significance level, , that has the probability, . 

Equation (16) can be simplified as the state covariance matrix, . Furthermore, since the past and future observations, and have zero means, the desired target for the state is . With these simplifications in place, the metric for the state-space is represented in (17) 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-24.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-25.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-26.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-27.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-28.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-29.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-30.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-31.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-32.png)


The corresponding UCL for a significance level is derived as follows: 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-34.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-35.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-36.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-37.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-38.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-39.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-40.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-41.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-42.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-43.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-44.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-45.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-46.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-47.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-48.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-49.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-50.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-51.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-52.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-53.png)


where is the critical value of the -distribution with and degrees of freedom for a significance level . By comparing against in real-time, an abnormal condition is then determined when . 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-55.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-56.png)


The metric is introduced to test the significance level of the prediction error represented in the scaled past observation space. According to (14), the prediction error for the scaled past measurement and the corresponding -metric are then defined in (19) and (20), respectively 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-58.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-59.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-60.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-61.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-62.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-63.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-64.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-65.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-66.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-67.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-68.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-69.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-70.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-71.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-72.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-73.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-74.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-75.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-76.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-77.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-78.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-79.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-80.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-81.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-82.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-83.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-84.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-85.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-86.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-87.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-88.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-89.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-90.png)


Given a level of significance, , also based on the assumption of normality, the threshold, of the -metric for the PCA is estimated by Jackson and Mudholkar [15] as 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-92.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-93.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-94.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-95.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-96.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-97.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-98.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-99.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-100.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-101.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-102.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-103.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-104.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-105.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-106.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-107.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-108.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-109.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-110.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-111.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-112.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-113.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-114.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-115.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-116.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-117.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-118.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-119.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-120.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-121.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-122.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-123.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-124.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-125.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-126.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-127.png)


where , and is the normal deviate corresponding to percentile. For the PCA, in (21), is the eigenvalue of the covariance of the measured data. For the CVA error represented in (19), it should be the covariance of the scaled past observations, , i.e., 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-129.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-130.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-131.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-132.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-133.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-134.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-135.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-136.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-137.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-138.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-139.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-140.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-141.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-142.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-143.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-144.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-145.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-146.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-147.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-148.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-149.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-150.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-151.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-152.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-153.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-154.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-155.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-156.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-157.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-158.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-159.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-160.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-161.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-162.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-163.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-164.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-165.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-166.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-167.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-168.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-169.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-170.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-171.png)


Therefore, the calculation can be simplified by letting and in (21). By comparing against in real-time, an abnormal condition is determined when . 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-173.png)


Both control limits in (18) and (21) are based on the assumptions that the state variables and prediction errors are Gaussian. However, when the collective modeling errors, and of the system (2) are non-Gaussian processes, this assumption is not valid. Hence, and derived above can no longer be used as control limits for real-time monitoring. One solution to this issue is to estimate the PDF directly for these and metrics through a nonparametric approach [13], [14]. Amongst various PDF estimating approaches, the KDE approach [13], [14] is selected for this work. The KDE is a well established approach to estimate the PDF particularly for univariate random processes [16]. Therefore, it is particularly suitable for the and metrics which are univariate although the underlying processes are multivariate. Assume is a random variable and its density function is denoted by . This means that 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-175.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-176.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-177.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-178.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-179.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-180.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-181.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-182.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-183.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-184.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-185.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-186.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-187.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-188.png)


Therefore, by knowing , an appropriate control limit can be determined for a specific confidence bound, using (22). The estimation of the probability density function at point through the kernel function, is defined as follows: 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-190.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-191.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-192.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-193.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-194.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-195.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-196.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-197.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-198.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-199.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-200.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-201.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-202.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-203.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-204.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-205.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-206.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-207.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0004-208.png)


where , , are samples of and is the bandwidth. The bandwidth selection in KDE is an important issue because selecting a bandwidth too small will result in the density estimator being too rough, a phenomenon known 

Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on September 11,2026 at 18:11:40 UTC from IEEE Xplore.  Restrictions apply. 

IEEE TRANSACTIONS ON INDUSTRIAL INFORMATICS, VOL. 6, NO. 1, FEBRUARY 2010 

40 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0005-02.png)


Fig. 1. Flowchart of the CVA with KDE algorithm. 

as under-smoothed, while selecting a bandwidth too big will result in the density estimator being too flat. There is no single perfect way to determine the bandwidth. However, a rough estimation of the optimal bandwidth subject to minimizing the approximation of the mean integrated square error can be derived in (24), where is the standard deviation [17] 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0005-05.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0005-06.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0005-07.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0005-08.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0005-09.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0005-10.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0005-11.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0005-12.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0005-13.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0005-14.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0005-15.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0005-16.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0005-17.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0005-18.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0005-19.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0005-20.png)


the PDFs of the and metrics for a given confidence bound, by solving the following equations, respectively: 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0005-22.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0005-23.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0005-24.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0005-25.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0005-26.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0005-27.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0005-28.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0005-29.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0005-30.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0005-31.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0005-32.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0005-33.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0005-34.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0005-35.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0005-36.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0005-37.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0005-38.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0005-39.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0005-40.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0005-41.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0005-42.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0005-43.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0005-44.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0005-45.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0005-46.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0005-47.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0005-48.png)


By replacing with and obtained in (17) and (20), respectively, the above KDE approach is able to estimate the underlying PDFs of the and metrics. The corresponding conThe and metrics are complementary. A fault may cause a trol limits, and can then be obtained from significant deviation in the state-space but not necessary results Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on September 11,2026 at 18:11:40 UTC from IEEE Xplore.  Restrictions apply. 

ODIOWEI AND CAO: NONLINEAR DYNAMIC PROCESS MONITORING USING CANONICAL VARIATE ANALYSIS AND KERNEL DENSITY ESTIMATIONS 

41 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0006-02.png)


Fig. 2. Graphical description of the TEP plant. 

in a similar level of significance in the error space, vice versa. Therefore, in this work, a fault is then identified if either or conditions are satisfied, i.e., 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0006-05.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0006-06.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0006-07.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0006-08.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0006-09.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0006-10.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0006-11.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0006-12.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0006-13.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0006-14.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0006-15.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0006-16.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0006-17.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0006-18.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0006-19.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0006-20.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0006-21.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0006-22.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0006-23.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0006-24.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0006-25.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0006-26.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0006-27.png)


where represents a logical OR operation. By using the fault detection condition (26), the monitoring performance becomes insensitive to the number of states, since any ignored variances in the metric by reducing will be recovered by metric. 

## IV. CVA WITH KDE ALGORITHM 

By summarising the analysis presented in the previous sections, a new extension of CVA using KDEs for nonlinear dynamic process monitoring is proposed to identify underlying faults subject to non-Gaussian processes. The step by step procedure of the proposed CVA with KDE algorithm is illustrated in the flowchart presented in Fig. 1. 

## V. CASE STUDY-TENNESSEE EASTMAN PROCESS PLANT 

fault operations (Fault 1–Fault 20). The sampling time for most of the process variables in the TEP plant is 3 min. A total of 52 measurements are collected for each data set of length, representing 48-h operation with a sampling rate of 3 min. However, 19 of the 52 measurements, 14 of them sampled at 6 min interval and 5 of them sampled in every 15 min, have not been included inthis study due tothe measurementtime delay.Different from the work reported by Chiang [5], 11 manipulated variables are treated the same as other measured variables because under feedback control, these variables are not independent any more. The simulation time of each operation run in the test data block is 48 h and the various faults are introduced only after 8 h. This means that for each of the faults, the process is in-control for the first 8 simulation hours before the process gets out of control at the introduction of the fault. All 20 faults have been studied in this work. Also, in this paper, the normal operating process data will be referred to as the training data. A graphical description of the TEP Plant is shown in Fig. 2, whereas a brief description of these 20 TEP faults is presented in Table I. 

## VI. MONITORING PERFORMANCE 

The Tennessee Eastman Process (TEP) plant [18] has five The monitoring performance in this study is assessed based main units which are the reactor, condenser, separator, stripper, on the percentage reliability which is defined as the percentage and compressor [5], [18]. Streams of the plant consists of eight of the samples outside the control limits [19] within the last 40 h components; A, B, C, D, E, F, G, and H. Components A, B, and faulty operation. Hence, a monitoring technique is said to be C are gaseous reactants which were fed to the reactor to form better than another technique if the percentage reliability of this products G and H. The TEP data used for this work consists of technique is numerically higher than the percentage reliability two blocks; the training and test data blocks. Each block has 21 of another. Also, the monitoring performance is assessed by the data sets corresponding to the normal operation (Fault 0) and 20 detection delay which is the time period it takes to detect a fault Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on September 11,2026 at 18:11:40 UTC from IEEE Xplore.  Restrictions apply. 

IEEE TRANSACTIONS ON INDUSTRIAL INFORMATICS, VOL. 6, NO. 1, FEBRUARY 2010 

42 

### TABLE I 

BRIEF DESCRIPTION OF TEP PLANT FAULTS 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0007-04.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0007-05.png)


Fig. 3. Autocorrelation function of the summed squares of all measurements. 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0007-07.png)


Fig. 4. Normalized singular values from the scaled Hankel matrix. 

after the introduction of the fault. The false alarm rate was also investigated. The monitoring performance of the proposed CVA with KDE is compared with the performance of the DPCA and DPLS with and without KDE, as well as CVA without KDE using all 20 faults described above. The 99% confidence interval is adopted in this study. 

The variability of the training data is characterised by the extracted canonical variate state-space model. First, the number of time lags for past and future observations is determined from the autocorrelation function of the summed squares of all measurements, as shown in Fig. 3, against 5% confidence bounds. The autocorrelation function indicates that the maximum number of significant lags in this study is 16. Hence, both and are set to 16. The length of the past and future observations is 528 according to (3) and (4). The number of columns of the truncated Hankel matrices according to (10) is . The singular value decomposition is then performed on the scaled Hankel matrix, as in (13). 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0007-11.png)


Several ways have been suggested to determine the order of the system for CVA-based approaches amongst which the dominant singular values [3], [5] and the Akaike Information Criterion (AIC) are most widely adopted. The former method was adopted in this study to determine the order of the system. The singular values from the scaled Hankel were normalized to have the values ranging between 0 and 1 and then the order determined based on the dominant normalized singular values. For the TEP case study, it was noticed that the singular values of the scaled Hankel matrix in (13) decrease slowly. If is determined from these singular values, it will be unrealistically large as indicated in Fig. 4, which shows the normalized sum of squares of residual singular values against the number of states. As mentioned already, the value of is not important to monitoring performance for this work due to the fault detection condition (26) adopted. Hence, a more realistic number of singular values, represented by circles in Fig. 4 is employed to represent the model space. Also, to make a fair comparison of 

Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on September 11,2026 at 18:11:40 UTC from IEEE Xplore.  Restrictions apply. 

ODIOWEI AND CAO: NONLINEAR DYNAMIC PROCESS MONITORING USING CANONICAL VARIATE ANALYSIS AND KERNEL DENSITY ESTIMATIONS 

43 

TABLE II 

RELIABILITY (%) COMPARISON 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0008-04.png)


TABLE III 

DETECTION DELAY (MINUTE) COMPARISON 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0008-07.png)


the proposed technique with the other techniques considered, the process variables, the number of lag and the order to determine the dimension of the latent variables are the same for all the approaches compared. The monitoring criterion mentioned above is applied to all the other methods considered. 

## _A. Reliability Comparison_ 

The superiority of the CVA with KDE over other techniques considered in this paper is demonstrated in Table II. Over all the faults compared, the CVA achieves the best performance in terms of reliability. Both CVA techniques are able to improve the monitoring performance for most TEP faults comparing with the DPCA, DPCA with KDE, DPLS and DPLS with KDE techniques. Nevertheless, the proposed CVA with KDE technique is able to further improve the reliability for faults that are more difficult to detect such as Faults 3 and 9. Faults 3 and 9 are more difficult to detect because these faults have very little effect on the corresponding process measurements. For such faults, the performance of the CVA with KDE is significantly 

better than that of the CVA. All KDE approaches achieve the reliability higher than or the same as their non-KDE counterparts as indicated in Table II. This is due to the nonlinear and non-Gaussian features of the plant, which justify the necessity of this work. 

## _B. Detection Delay Comparison_ 

The detection delays for the CVA with KDE and other techniques considered are presented in Table III. As shown in Table III, the CVA with KDE approach is able to detect most of these faults earlier than other techniques. This means operators have more time to take safety measures to counteract occurring faults if the proposed CVA with KDE approach is adopted. Again, all KDE associated approaches achieve detection delay less than or the same as their non-KDE counterparts due to the same reason aforementioned. 

Also investigated is the false alarm rates for all the faults and no false alarm has been observed for all faults and all approaches studied. 

Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on September 11,2026 at 18:11:40 UTC from IEEE Xplore.  Restrictions apply. 

IEEE TRANSACTIONS ON INDUSTRIAL INFORMATICS, VOL. 6, NO. 1, FEBRUARY 2010 

44 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0009-02.png)


Fig. 5. Fault 9 monitoring charts for CVA (a) and (b), DPCA (c) and (d) and DPLS (e) and (f) Techniques. solid: metrics, dashed: KDE-based UCL, dashdot: Gaussian assumption-based UCL. 

## _C. Monitoring Chart Comparison of Fault 9_ 

To appreciate the superior performance achieved by the new CVA with KDE approach, the and monitoring charts of all approaches for Fault 9 are presented in Fig. 5. In Fig. 5, subfigures in the left column and the right column are for the and charts, respectively; while the first, second, and third rows are for CVA, DPCA, and DPLS approaches, respectively. Upper control limits obtained based on the Gaussian assumption are represented as dashed lines, while the UCLs determined by the KDE approach are shown in dash-dot lines. 

Fig. 5 clearly indicates that only the CVA model is able to reveal the difference in dynamic behavior between the normal operation and the operation with Fault 9. Both and metrics produced by the DPCA and the DPLS approaches have no identifiable difference between the normal and faulty operations. Furthermore, the CVA with KDE approach gives tighter UCLs for both metrics resulting in a higher percentage of reliability and earlier fault detection than the traditional CVA approach. 

## VII. CONCLUSION 

To deal with fault monitoring for nonlinear dynamic processes, the linear state-space model-based CVA approach is extended by directly estimating the underlying PDF of the associated and metrics to derive more appropriate control limits for these monitoring metrics. This leads to the new CVA with KDE algorithm proposed for nonlinear dynamic process monitoring. The proposed approach is applied to the Tennessee Eastman Process. The monitoring performance of the proposed CVA with KDE is compared with that of the DPCA and DPLS with and without KDE, as well as CVA without KDE techniques. The percentage reliability and the detection delays were 

adopted to assess and compare the monitoring performance of the proposed approach with that of all other techniques considered in this study. Although some of the faults are commonly detected by all the techniques considered, the outstanding superiority of the CVA with KDE is demonstrated in those faults that are not easily detectable. For such faults, the proposed CVA with KDE has higher percentage reliability than other techniques considered. In addition, the proposed CVA with KDE is able to detect faults earlier than other techniques considered. Hence, the CVA with KDE is a more efficient tool than the DPCA and the DPLS with and without KDE as well as the CVA without KDE for nonlinear dynamic process monitoring. 

## REFERENCES 

- [1] W. F. Ku, H. R. Storer, and C. Georgakis, “Disturbance detection and isolation by dynamic principal component analysis,” _Chemometrics and Intel. Lab. Syst._ , pp. 179–196, 1995. 

- [2] T. J. Richard, K. Uwe, and E. C. Jonathan, “Dynamic multivariate statistical process control using subspace identification,” _J. Process Control_ , vol. 14, pp. 279–292, 2004. 

- [3] A. Negiz and A. Cinar, “Monitoring of multivariable dynamic processes and sensor auditing,” _J. Process Control_ , vol. 8, no. 56, pp. 375–380, 1998. 

- [4] T. Komulainen, M. Sourander, and S. Jamsa-Jounela, “An online application of dynamic PLS to a dearomatization process,” _Comput. Chem. Eng._ , vol. 28, pp. 2611–2619, 2004. 

- [5] L. H. Chiang, E. L. Russell, and R. D. Braatz _, Fault Detection and Diagnosis in Industrial Systems_ . London, U.K.: Springer, 2001. 

- [6] L. Juan and L. Fei, “Statistical modelling of dynamic multivariate process using canonical variate analysis,” in _Proc. IEEE Int. Conf. Inf. Autom._ , Colombo, Sri Lanka, Dec. 15–17, 2006, p. 218. 

- [7] A. Norvalis, A. Negiz, J. DeCicco, and A. Cinar, “Intelligent process monitoring by interfacing knowledge-based systems and multivariate statistical monitoring,” _J. Process Control_ , vol. 10, pp. 341–350, 2000. 

- [8] C. D. Schaper, W. E. Larimore, D. E. Seborg, and D. A. Mellichamp, “Identification of chemical processes using canonical variate analysis,” _Comput. Chem. Eng._ , vol. 18, no. 1, pp. 55–69, 1994. 

- [9] A. Negiz and A. Cinar, “PLS, balanced and canonical variate realization techniques for identifying VARMA models in state space,” _Chemometrics and Intell. Lab. Syst._ , vol. 38, pp. 209–221, 1997. 

- [10] A. Chiuso and G. Picci, “Asymptotic variance of subspace estimates,” in _Proc. 48th IEEE Conf. Decision and Control_ , Dec. 2001, vol. 4, p. 3910. 

- [11] N. F. J. Hunter, “Comparing CVA and ERA in transfer function measurement for lithography applications,” in _Proc. Amer. Control Conf._ , Jun. 2–4, 1999, vol. 2, p. 1171. 

- [12] W. E. Larimore, “Statistical optimality and canonical variate analysis system identification,” _Signal Process._ , vol. 52, pp. 131–144, 1996. 

- [13] E. B. Martin and A. J. Morris, “Non-parametric confidence bounds for process performance monitoring charts,” _J. Process Control_ , vol. 6, no. 6, pp. 349–358, 1996. 

- [14] Q. Chen, P. Goulding, D. Sandoz, and R. Wyne, “Application of kernel density estimates to condition monitoring for process industries,” in _Proc. Amer. Control Conf._ , Jun. 21–26, 1998, vol. 6, pp. 3312–3316. 

- [15] J. E. Jackson and G. S. Modholkar, “Control procedures for residuals associated with principal component analysis., volume 21, pages 341–349,” _Technometric_ , vol. 21, pp. 341–349, 1979. 

- [16] A. W. Bowman and A. Azzalini _, Applied Smoothing Techniques for Data Analysis, The Kernel Approach with S-Plu Illustrations_ . Oxford, U.K.: Clarendon Press, 1997. 

- [17] S. Xiaoping and A. Sonali, “Kernel density estimation for an anomaly based intrusion detection system,” in _Proc. 2006 World Congr. Comput. Sci., Comput. Eng. Appl. Comput._ , Jun. 26–29, 2006, p. 161. 

- [18] J J. Downs and E. Vogel, “A plant-wide industrial process control problem,” _Comput. Chem. Eng._ , vol. 17, pp. 245–255, 1993. 

- [19] M. Kano, K. Nagao, S. Hasebe, I. Hashimoto, H. Ohno, R. Strauss, and B. R. Bakshi, “Comparison of multivariate statistical process monitoring methods with applications to the Eastman challenge problem,” _Comput. Chem. Eng._ , vol. 26, pp. 161–174, 2002. 

Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on September 11,2026 at 18:11:40 UTC from IEEE Xplore.  Restrictions apply. 

45 

ODIOWEI AND CAO: NONLINEAR DYNAMIC PROCESS MONITORING USING CANONICAL VARIATE ANALYSIS AND KERNEL DENSITY ESTIMATIONS 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0010-02.png)


**Pabara-Ebiere Patricia Odiowei** received the M.Res. degree in chemical engineering from the University of Nottingham, Nottingham, U.K., in 2002. She is currently working towards the Ph.D. degree at Cranfield University, Cranfield, U.K. 

She is a Lecturer on study leave from Niger Delta University, Bayelsa State, Nigeria. Her research interest is in nonlinear system identification and process condition monitoring. 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Analysis_and_Kernel_Density_Estimations.pdf-0010-05.png)


**Yi Cao** (M’96) received the M.Sc. degree in control engineering from Zhejiang University, China, in 1985 and the Ph.D. degree in engineering from the University of Exeter, Exeter, U.K., in 1996. 

He is a Senior Lecturer with the School of Engineering, Cranfield University. His research interests are in advanced process control, including plant-wide process control, nonlinear system identification, nonlinear model predictive control and process monitoring. 

Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on September 11,2026 at 18:11:40 UTC from IEEE Xplore.  Restrictions apply. 

