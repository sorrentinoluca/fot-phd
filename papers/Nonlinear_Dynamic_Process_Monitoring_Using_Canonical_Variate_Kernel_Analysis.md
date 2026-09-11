**_processes_** 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis.pdf-0001-01.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis.pdf-0001-02.png)


## _Article_ 

# **Nonlinear Dynamic Process Monitoring Using Canonical Variate Kernel Analysis** 

**Simin Li**<sup>**1,2,†**</sup> **, Shuang-hua Yang**<sup>**1,2,**</sup> *****<sup>**,†**</sup> **and Yi Cao**<sup>**1,2,†**</sup> 

- 1 Institute of Zhejiang University-Quzhou, 78 Jiuhua North Avenue, Baiyun Street, Quzhou 324000, China 

- 2 College of Chemical and Biological Engineering, Zhejiang University, 38 Zheda Road, Lingyin Street, Hangzhou 310027, China 

- Correspondence: yangsh@zju.edu.cn; Tel.: +86-1581-371-9166 

- These authors contributed equally to this work. 

**Abstract:** Most industrial systems today are nonlinear and dynamic. Traditional fault detection techniques show their limits because they can hardly extract both nonlinear and dynamic features simultaneously. Canonical variate analysis (CVA) shows its excellent monitoring performance in fault detection for dynamic processes but is not applicable to nonlinear processes. Inspired by the CVA method, a novel nonlinear dynamic process monitoring method, namely, the “canonical variate kernel analysis” (CVKA), is proposed in this work. The way to extract nonlinear features is different from a traditional kernel canonical variate analysis (KCVA). In a sequential structure, the new approach firstly extracts the linear dynamic features from the data through the CVA method, followed by a kernel principal component analysis to extract nonlinear features from the CVA residual space. The new CVKA method is then applied to a TE process case study, proving the excellent performance of CVKA compared to other common approaches in dynamic nonlinear process monitoring for TE-like processes. 

**Keywords:** fault detection; CVA; nonlinear dynamic process; PCA 

## **1. Introduction** 

**Citation:** Li, S.; Yang, S.-h.; Cao, Y. Nonlinear Dynamic Process Monitoring Using Canonical Variate Kernel Analysis. _Processes_ **2023** , _11_ , 99. https://doi.org/10.3390/pr11010099 

#### Academic Editor: Ján Pitel’ 

Received: 18 November 2022 Revised: 7 December 2022 Accepted: 19 December 2022 Published: 29 December 2022 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis.pdf-0001-16.png)


**Copyright:** © 2022 by the authors. Licensee MDPI, Basel, Switzerland. This article is an open access article distributed under the terms and conditions of the Creative Commons Attribution (CC BY) license (https:// creativecommons.org/licenses/by/ 4.0/). 

Process monitoring and fault detection have become increasingly important to guarantee the normal operation of production, whose task are to determine if there is a fault occurred. As industrial systems become more complex, it becomes increasingly difficult to establish accurate mathematical models and acquire sufficient empirical knowledge. Therefore, techniques based on first-principle models and expert experience are not widely persuasive. Data-driven techniques have been proved to be most effective in practice, with which complex mechanisms and knowledge are not required, and faults can be detected from the change of data. 

Multivariate statistical process monitoring (MSPM) techniques [1] such as principal component analysis (PCA) [2] and canonical variate analysis (CVA) [3] can reduce the noise of the original data without losing the most basic information. Low-dimensional data not only help to reduce computation/training time, but also remove redundant features to resolve multicollinearity issues. 

Among all the MSPM techniques, the PCA-based techniques is extensively used for fault detection. The main idea is to represent the original space with several orthogonal features, which are called principal components. It is the most direct and simplest dimensionality reduction method. PCA has an assumption of a linear and static system. However, real systems are always nonlinear and dynamic. To cope with the nonlinear problem, Kramer [4] trained a feed-forward neural network to realize a nonlinear mapping named nonlinear PCA (NLPCA). Lee et al. [5] developed kernel PCA (KPCA) for nonlinear process, which extracted nonlinear principal components using kernel functions. For dynamic processes, Ku et al. [6] applied a “time lag shift” method to detect dynamic processes 

_Processes_ **2023** , _11_ , 99. https://doi.org/10.3390/pr11010099 

https://www.mdpi.com/journal/processes 

2 of 12 

_Processes_ **2023** , _11_ , 99 

which they called dynamic PCA (DPCA). To extract deep features, Deng et al. [7] designed a multilayer PCA model called deep PCA (DePCA). Moreover, Chen et al. [8] applied deep PCA to an electrical drive system for incipient fault detection. 

The main limitation of PCA-based methods is that they are based on the fact that measurement variables are time-independent [9]. However, in reality, dynamic industrial processes account for most processes. Different from PCA, CVA takes time correlation into consideration [10]. Although DPCA can detect some dynamic information, Russell et al. [11] extensively tested the effectiveness of DPCA and CVA in process monitoring for dynamic industrial processes. The finding was that CVA performed better both in accuracy and sensitivity. Therefore, CVA seems to be a better choice for dynamic process monitoring. 

CVA works by maximizing the correlation between past and future vectors [12], and the CVs can maximally explain the time-related features in these vectors. To address the nonGaussian issue caused by the nonlinearities of industrial processes, Odiowei et al. [13] combined CVA with upper control limit (UCL), where UCL was directly obtained by a kernel density estimation (KDE) without the Gaussian assumption. Moreover, Samuel et al. [14] performed a CVA with KDE in the KPCA kernel space, which was named kernel canonical variate analysis (KCVA). CVA is not sensitive enough for monitoring incipient faults; Pilario et al. [15] proposed a new CVA dissimilarity-based index and the new method was called canonical variate dissimilarity analysis (CVDA). Conventional single kernels only have good interpolation or extrapolation ability. To overcome this drawback, Pilario et al. [16] used a mixed kernel strategy to keep both good interpolation and extrapolation ability which they called mixed-kernel CVDA (MK-CVDA). 

Most industrial systems today are nonlinear and dynamic. However, traditional fault detection method can only address at most one of these features, so the detection performance is not ideal. To cope with this problem, some experts have proposed fault detection methods for nonlinear dynamical systems. Choi et al. [17] proposed dynamic kernel PCA (DKPCA), which expressed nonlinearity with kernel functions and also described the dynamics in a time-expanded way. In a previous work, we combined DPCA and KPCA in a deep model to capture different features [18], which was named deep DPCA (DeDPCA). Guo et al. [19] combined dynamic inner PCA, PCA and KPCA in a sequential structure to deal with the dynamical nonlinear problem. The aforementioned KCVA is also a nonlinear dynamic process monitoring method. Nevertheless, the way the DKPCA describes a nonlinear dynamical system is not effective and it may lose some significant features in the system. The information fusion of different layers in DeDPCA may cause too high a false alarm rate. KCVA only focuses on the dynamics of the principal space but ignores the residual space. Therefore, the monitoring performance of existing nonlinear dynamic fault detection methods is not good enough and a more effective fault detection method is needed. 

Current industrial systems always contain linear and nonlinear relationships. Extracting only one type of feature can not fully represent the system. Considering both linear and nonlinear features is better. Inspired by it, a novel hybrid linear–nonlinear dynamic statistical modelling technique is proposed. The main idea is that linear dynamic features are extracted first using the CVA method and nonlinear features are then extracted from the CVA residual space. The CVs of CVA contain most linear dynamic features, leaving some nonlinear features and noise in the residuals. Therefore, nonlinear features are further extracted using nonlinear methods in the CVA residual space. Both features can be fully used for process monitoring. Kernel-based methods and neural networks both can be used to handle the nonlinear problem [20,21]. Kernel-based methods require a low computational complexity and have good nonlinear estimation capabilities if the parameters are appropriate. Hence, KPCA is adopted to extract the nonlinear features from the obtained CVs. Moreover, the _T_<sup>2</sup> and Q statistics are together applied for fault decision and _T_<sup>2</sup> based on different features are fused together to decide the system status. The new method is named canonical variate kernel analysis (CVKA). 

3 of 12 

_Processes_ **2023** , _11_ , 99 

There are some contributions in this paper. Firstly, a new hybrid statistical model structure has been presented by combining CVA with KPCA in a sequential structure. Linear dynamic and nonlinear features are both extracted for nonlinear dynamic process monitoring. Secondly, the fusion of Hotelling’s _T_<sup>2</sup> reduces the number of detection metrics and therefore reduces the false alarm rate. Finally, an improved nonlinear dynamic fault detection performance on a TE plant has been attained over existing nonlinear dynamic methods. 

The work is organized as follows. In Section 2, the basic idea of CVA-based dynamic fault detection is described. In Section 3, the detailed information of the CVKA method is presented. In Section 4, a case study of the TE process is used to demonstrate the effectiveness of the CVKA method. Section 5 discusses the merits and limitations. Section 6 summarizes this work. 

## **2. Brief Review of the CVA Method** 

Assume **_X_** _∈_ R<sup>_n×m_</sup> is a matrix which contains _n_ samples. Each sample consists of _m_ variables. **_x_** _k_ is the _k_ th row vector of **_X_** . Denote **_x_** _k_ = [ **_u_** _k_ **_y_** _k_ ], where **_u_** _k_ includes input variables and **_y_** _k_ includes output variables. Therefore, in the first feature layer, the _k_ th past and _k_ th future row vectors of **_X_** can be obtained, respectively, as follows: 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis.pdf-0003-06.png)


where _q_ is the past and future measurements. _q_ needs to be as small as possible while capturing the major autocorrelations within the data. **_x_** _p_ . _k_ and **_x_** _f_ . _k_ are normalized for further study as follows: 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis.pdf-0003-08.png)


where **_µ_** _p_ and **_µ_** _f_ are sample means, and _σp_ and _σf_ are sample standard deviations. 

The past observation matrices **_X_** _p_ and the future observation matrices **_X_** _f_ can be 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis.pdf-0003-11.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis.pdf-0003-12.png)


where _M_ = _n −_ 2 _q_ + 1. 

The covariance matrix Σ can be estimated as follows: _pp_ 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis.pdf-0003-15.png)


Moreover, covariance matrix Σ _f f_ and cross-covariance matrix Σ _p f_ can be expressed in a similar way. 

The canonical variables are obtained by applying an SVD to **_H_** 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis.pdf-0003-18.png)


where **_U_** is the past mapping matrices, **_V_** is the future mapping matrices and **_W_** is a diagonal matrix. The numbers on the diagonal represent singular values, which is the degree of correlation between column pairs of **_U_** and **_V_** . **_W_** = _diag_ ( _σ_ 1, _σ_ 2, _· · ·_ , _σr_ 1, 0, _· · ·_ , 0), where _r_ 1 is the rank of **_H_** and 1 _≥ σ_ 1 _≥ σ_ 2 _≥· · · ≥ σr_ 1. Thus, the data can be divided into the 

4 of 12 

_Processes_ **2023** , _11_ , 99 

state variables ( **_z_** _k ∈_ R<sup>1</sup><sup>_×r_1</sup> ) and the residual canonical variates ( **_e_** _k ∈_ R<sup>1</sup><sup>_×_(</sup><sup>_qm−r_1)</sup> ). The state space contains the most linear dynamic features, and the residual space contains the most nonlinear features and noises. 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis.pdf-0004-03.png)


The state variables **_z_** _k_ is a linear combination of **_x_** ˜ _p_ , _k_ , **_z_** _k_ = **_J_** _x_ ˜ **_x_** _p_ , _k_ , where **_J_** _x_ = **_V_**<sup>_T_</sup> _x_<sup>Σ</sup><sup>_−_</sup> _pp_ 2<sup><u>1</u></sup> with **_V_** _x_ consisting of the first _r_ 1 columns of **_V_** . The residual canonical variates are **_e_** _k_ = **_F_** _x_ ˜ **_x_** _p_ , _k_ , where **_F_** _x_ = **_V_** _y_<sup>_T_Σ</sup><sup>_−_</sup> _pp_ 2<sup><u>1</u>with</sup><sup>**_V_**</sup> _y_<sup>consisting of the remaining</sup><sup>_qm −r_</sup> 1<sup>columns of</sup><sup>**_V_**</sup> defined in Equation (8). 

The change in state space and residual space can be monitored separately by the _T_<sup>2</sup> and _Q_ statistics. They are computed as 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis.pdf-0004-06.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis.pdf-0004-07.png)


Since measurements are always nonlinear or non-Gaussian-distributed [22], determining the upper control limits using a Gaussian assumption is not preferable. Kernel density estimation (KDE) [13] performs well in estimating real probability density functions (PDFs). The PDF _p_ ˆ( _x_ ) estimated by KDE is defined as 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis.pdf-0004-09.png)


where K( _·_ ) is a kernel function, _xk_ is the sample of **_x_** , and _h_ is a smoothing parameter called bandwidth. 

One popular kernel function can be written in this form 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis.pdf-0004-12.png)


According to the real PDF, the control limits _T_ lim<sup>2and</sup><sup>_Q_limcanbecalculatedby</sup> Equations (14) and (15). 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis.pdf-0004-14.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis.pdf-0004-15.png)


In our proposed CVKA method, KDE is still used to determine upper control limits. For online monitoring, the _T_<sup>2</sup> and _Q_ statistics at each sampling instant can be obtained by Equations (14) and (15). If one of _T_<sup>2</sup> or _Q_ exceeds its upper control limit _T_ lim<sup>2or</sup><sup>_Q_lim, a</sup> fault is detected. 

## **3. Proposed CVKA Method** 

CVA has shown its superiority for dynamic process monitoring [11]. However, it can only extract linear features for linear processes. Nonlinear features usually occur in the residuals of the linear model [10] and nonlinear features cannot be distinguished from noise in the residual. Therefore, CVA performs poorly in nonlinear dynamical systems, showing a low detectability for small faults. To extend CVA to nonlinear process, it is worthwhile to further analyse the residuals through nonlinear feature extraction techniques. The proposed CVKA model extracts dynamic features and nonlinear features by integrating CVA and KPCA as shown in Figure 1. Since the linear canonical variables extracted from the original data and the nonlinear PCs extracted from the CVA residual data both can be evaluated by _T_<sup>2</sup> index, we can fuse them together to reduce the value of the statistic and thus reduce the false alarm rate. 

5 of 12 

_Processes_ **2023** , _11_ , 99 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis.pdf-0005-02.png)


**Figure 1.** Schematic of CVKA-based process monitoring. 

## _3.1. Construction of CVKA Model_ 

From Figure 1, the linear canonical variables and CVA residual data are obtained through the CVA model. Then, the CVA residual data **_e_** _k_ are further investigated to dig the nonlinearity of the process. Given a dataset **_e_** _k ∈_ R<sup>1</sup><sup>_×_(</sup><sup>_qm−r_1)</sup> , _k_ = 1, . . ., _M_ , a nonlinear mapping **Φ** : R<sup>1</sup><sup>_×_(</sup><sup>_qm−r_1)</sup> _→ F_ maps **_e_** from the original space to a high-dimensional linear space _F_ . The corresponding covariance matrix is calculated as 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis.pdf-0005-06.png)


where **Φ** ( **_e_** ) has mean 0 and variance 1. **_C_**<sup>_F_</sup> needs to be diagonalized. This leads to an eigenvalue solving problem 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis.pdf-0005-08.png)


where _λ_ is the eigenvalue of **_C_**<sup>_F_</sup> , **_p_** is the eigenvector. _λ_ is a non-negative number and an eigenvector is a nonzero vector. 

Noting that **_p_** is a linear combination of **Φ** ( **_e_** ), we have 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis.pdf-0005-11.png)


Multiplying both sides of Equation (19) by **Φ** ( **_e_** _k_ ) gives 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis.pdf-0005-13.png)


Substituting Equations (16) and (18) in (19), we have 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis.pdf-0005-15.png)


The kernel trick can be applied to **Φ** ( **_e_** ) to construct an _M × M_ kernel matrix 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis.pdf-0005-17.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis.pdf-0005-18.png)



![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis.pdf-0005-19.png)


6 of 12 

_Processes_ **2023** , _11_ , 99 

where **_I_** _M_ is an _M × M_ matrix where each element is _M_<sup><u>1</u>. Then, Equation (20) can be rewrit-</sup> ten as 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis.pdf-0006-03.png)


which can be expressed in this form 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis.pdf-0006-05.png)


resulting in the projection vector **_α_** _i ∈_ R<sup>_M_</sup> and the corresponding nonlinear score vector **_t_** _i_ = **_K_** _c_ **_α_** _i ∈_ R<sup>1</sup><sup>_×r_2</sup> , 1 _≤ i ≤ M_ and _r_ 2 is the number of PCs. 

A typical kernel function can be denoted as 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis.pdf-0006-08.png)


Therefore, the _T_<sup>2</sup> and _Q_ indices can be obtained as 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis.pdf-0006-10.png)


where **_s_** _k_ = [ **_z_** _k_ **_t_** _k_ ]. **Φ**<sup>ˆ</sup> ( **_t_** _k_ ) is the reconstruction of vector **Φ** ( **_t_** _k_ ). 

As mentioned above, similar to the CVA algorithm, KDE was also adopted to estimate the PDF of _T_<sup>2</sup> and _Q_ and calculate the control limits _T_ lim<sup>2and</sup><sup>_Q_lim.</sup> 

For online monitoring, the _T_<sup>2</sup> and _Q_ statistics are calculated using Equations (26) and (27). For CVKA-based fault detection, if one of _T_<sup>2</sup> or _Q_ exceeds its upper control limit _T_ lim<sup>2or</sup> _Q_ lim, a fault is detected. 

## _3.2. Summary of the Proposed CVKA Scheme_ 

The CVKA monitoring procedure consists of two steps. In offline training, the normal data are analysed by the CVKA technique to get the mapping vectors and compute the control limits. Online monitoring uses the sample’s continuous collection to check if a fault has occurred. Figure 2 shows the algorithm flowchart. Detailed steps are summarized in Algorithm 1. 

**Algorithm 1** Detailed steps of CVKA-based fault detection 

## **_Offline training_ :** 

> **_Step1_** . Collect the normal data _X_ and compute the past and future data series using (1) and (2); 

**_Step2_** . Compute the Hankel matrices and perform an SVD on the scaled Hankel matrix from (7) and (8); 

**_Step3_** . Determine the canonical variables according to (9); **_Step4_** . Construct the kernel matrix from the canonical variables and determine the principal variables and residuals; 

**_Step5_** . Compute the monitoring indices using (26) and (27) and their control limits using (14) and (15), respectively; 

**_Online monitoring_ :** **_Step6_** . Acquire test data and construct the past and future vectors; **_Step7_** . Compute the canonical variables and project them to the kernel space as for the training data; **_Step8_** . Compute _T_<sup>2</sup> and _Q_ of the test data using (26) and (27); **_Step9_** . Judge if a fault occurs by comparing _T_<sup>2</sup> and _Q_ with their respective control limits. 

7 of 12 

_Processes_ **2023** , _11_ , 99 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis.pdf-0007-02.png)


**Figure 2.** CVKA algorithm flowchart. 

## **4. Case Study** 

The CVKA method was compared with the DKPCA, DeDPCA and KCVA methods by applying them to a benchmark TE plant. Firstly, CVKA and DKPCA were compared to see how CVKA could improve the detection performance by considering the linear and nonlinear features in a sequential structure. Then, CVKA was compared with DeDPCA 

8 of 12 

_Processes_ **2023** , _11_ , 99 

to show the superiority of the state-space-based feature extraction method for dynamic process monitoring. Finally, CVKA was compared with KCVA to prove the necessity of further analysing the CVA residual space through nonlinear feature extraction methods. 

## _4.1. Overview_ 

The TE process [23,24] is the benchmark process shown in Figure 3. The TE production process consists mainly in the reaction of four gaseous materials, producing two products and a by-product. There are 52 variables in the whole TE process. A total of 20 faults are used for verification, including 4 types of different faults, respectively, step, random, slow drift and sticking. Moreover, there are five faults whose fault types are unknown. The corresponding data can be found in [25]. Training datasets and testing datasets all consist of 960 samples. The fault dataset contains 160 normal samples and 800 fault samples. 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis.pdf-0008-05.png)


**Figure 3.** Graphical description of the TE plant. 

## _4.2. Implementation Details_ 

For the DKPCA, DeDPCA, KCVA and CVKA methods, the Gaussian kernel function was chosen and the kernel width was empirically set to _σ_ = 50 m. For DeDPCA and DKPCA, the calculation results of time lag _k_ was two using Ku’s theory [6]. For KCVA and CVKA, the autocorrelations in the data became insignificant when the number _q_ of past and future measurements was five. A threshold of 90% was set for calculating the number of PCs and CVs. _T_<sup>2</sup> and _Q_ were used jointly. The KDE method was used to calculate the control limits. Before applying DKPCA, DeDPCA, KCVA and CVKA, all data were standardized to avoid dimensional effects. 

The fault detection rate (FDR), the fault detection time (FDT) and the false alarm rate (FAR) were used to evaluate the performance. The FDR is the probability of detecting a fault under system fault conditions and measures the accuracy of a fault detection method. The FDT is the time it takes to first discover a fault. The FAR is the probability of falsely detecting a fault under normal system conditions and measures the robustness of a fault detection method. 

## _4.3. Results and Discussion_ 

To appreciate the performance of CVKA, the detection processes for F18 were firstly compared. F18 is an unknown fault. Figure 4 shows the fault detection results using different methods to monitor the TE process. The control limits are drawn with a red dashed line, while the monitoring statistics are drawn with a black solid line. For DKPCA, 

9 of 12 

_Processes_ **2023** , _11_ , 99 

it can be seen that the fault was not obvious at first and the _T_<sup>2</sup> and _Q_ statistics took 76 sample intervals to first detect that fault. The fault could be identified after that time and the total FDR was 90.63%. Moreover, as time went by, the data shift in the residual space was more obvious than that in the principal space. For DeDPCA, the fault detection rate was 90.88% and the fault detection time was 31 sample intervals. It was better than DKPCA, which reflected the advantages of a hierarchical feature extraction. For KCVA, the fault detection rate was 90.88% and the fault detection time was 24 sample intervals after introducing the fault, earlier than that of DKPCA and DeDPCA. It was because the principal kernel space was further analysed using CVA to extract dynamic features. However, ignoring the residual kernel space may lose some critical linear information, leading to a high false alarm rate. Figure 4d confirms that CVKA outperformed DKPCA, KCVA and DeDPCA. Specifically, most linear and nonlinear features were reflected in the _T_<sup>2</sup> index and the total FDR was 91.38%, larger than that of DKPCA, KCVA and DeDPCA. The fault was first detected at the 163th sample, much earlier than that of any other methods. By comparing these results, it is apparent that CVKA is more suitable than DKPCA, KCVA and DeDPCA for TE-like nonlinear dynamic process monitoring. 


![](Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis_images/Nonlinear_Dynamic_Process_Monitoring_Using_Canonical_Variate_Kernel_Analysis.pdf-0009-03.png)


**Figure 4.** Monitoring results for TE fault 18. ( **a** ) DKPCA. ( **b** ) DeDPCA. ( **c** ) KCVA. ( **d** ) CVKA. 

Table 1 lists all the monitoring results of the 20 TE faults using DKPCA, DeDPCA, KCVA and CVKA. According to the difficulty of detection, the faults can be divided into three categories. Faults 1, 2, 4, 7, 8, 11, 12, 14 and 18 form the first category. These faults are obvious and can be easily detected using DKPCA. Faults 5, 6, 10, 13, 16, 17, 19 and 20 form the second category. These faults are not so obvious but still can be detected most of the time using DKPCA. Faults 3, 9 and 15 form the last category. These faults cause little change to the system and are difficult to detect using any fault detection method. 

The CVKA method seemed to be most sensitive to all fault conditions in terms of FDR and FDT. CVKA had the largest FDRs for all faults except faults 8 and 10 in category one and category two, which means that CVKA could detect nearly all faults with a high accuracy. Moreover, CVKA obtained the smallest FDTs for most faults , indicating that 

10 of 12 

_Processes_ **2023** , _11_ , 99 

DeCVDA could always detect faults earlier than any other methods. All methods kept a relatively low FAR except KCVA, and the difference between the other three methods was not particularly obvious. CVKA obtained the largest average FDR, smallest average FDT and a relatively low average FAR, meaning that CVKA was more efficient. KCVA obtained the worst performance possibly because it only focused on principal kernel features but neglected the information in the residual subspace when doing kernel mapping, which also illustrated the necessity of further analysing the residual space through nonlinear feature extraction methods. The performance of DeDPCA was slightly better than that of DKPCA. Both methods are PCA-based methods. The only difference is that DKPCA extracts dynamic features and nonlinear features at the same time but DeDPCA extracts dynamic features and nonlinear features in different layers. It can be concluded that a layerwise feature extraction structure has the advantage of extracting more appropriate features. CVKA is generally better than DeDPCA, indicating that a state-space-based feature extraction CVA method is more suitable for extracting dynamic features. 

**Table 1.** FDRs, FDTs and FARs of 20 TE faults using DKPCA, KCVA, DeDPCA and CVKA. 

|**l**||**FDR (**|**%)**|||**FDT (Sa**|**mple)**|||**FAR (**|**%)**||
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**Faut**|**DKPCA**|**DeDPCA**|**KCVA**|**CVKA**|**DkPCA**|**DeDPCA**|**KCVA**|**CVKA**|**DkPCA**|**DeDPCA**|**KCVA**|**CVKA**|
|1|**99.75**|99.25|99.63|**99.75**|3|2|4|3|1.25|6.37|15.00|3.85|
|2|98.50|99.25|98.75|**99.38**|13|5|4|6|3.75|4.46|16.88|3.21|
|4|**100.00**|**100.00**|99.75|**100.00**|1|1|3|1|1.88|6.37|18.75|1.28|
|7|**100.00**|**100.00**|98.75|**100.00**|1|1|1|1|0.00|0.64|6.88|0.00|
|8|**100.00**|99.00|97.63|99.38|1|9|20|4|0.00|3.82|13.75|2.56|
|11|90.50|93.88|92.38|**94.88**|6|7|3|7|0.00|2.55|15.00|2.56|
|12|99.25|**100.00**|95.00|**100.00**|3|1|2|1|1.25|2.55|13.13|1.92|
|14|**100.00**|**100.00**|99.75|**100.00**|1|1|3|1|0.63|0.00|18.75|2.56|
|18|90.63|90.88|90.88|**91.38**|76|31|24|3|2.50|4.46|7.59|2.56|
|mean1|97.63|87.00|96.95|**98.31**|12|6|7|3|1.25|3.47|13.97|2.28|
|5|30.38|**100.00**|40.75|**100.00**|1|1|3|1|1.88|6.37|18.75|1.28|
|6|**100.00**|**100.00**|7.13|**100.00**|1|1|6|1|0.00|0.64|4.38|2.56|
|10|60.88|**94.13**|41.00|93.63|15|21|4|22|0.00|1.27|3.75|2.56|
|13|95.38|96.13|85.38|**96.50**|38|1|3|5|1.88|0.00|8.75|1.28|
|16|54.88|96.75|29.63|**96.88**|11|10|13|9|2.50|10.83|13.75|1.28|
|17|97.63|**97.75**|88.88|**97.75**|20|19|4|19|0.63|0.64|13.75|1.92|
|19|51.00|99.63|74.50|**99.88**|11|3|16|3|0.00|0.64|6.88|2.56|
|20|63.63|**92.00**|59.38|**92.00**|76|17|4|4|1.25|1.9|10.63|1.92|
|mean2|69.22|97.05|53.33|**97.08**|22|9|7|8|1.02|2.79|10.08|1.92|
|3|4.50|5.63|**20.00**|3.75|43|41|8|24|0.00|3.18|4.38|1.92|
|9|4.13|5.13|**16.38**|5.25|6|1|4|7|3.75|8.92|16.25|10.26|
|15|7.38|36.88|20.25|**37.75**|234|3|28|3|3.75|3.82|9.38|2.56|
|mean3|5.33|15.88|**18.88**|15.58|94|15|13|11|2.50|5.30|10.00|4.91|



From the detection results in terms of the FDRs, FDTs and FARs of DKPCA, DeDPCA, KCVA and CVKA, we can find that for most conditions, CVKA achieved a higher FDR, an earlier FDT and a relatively low FAR, which means that the proposed CVKA technique was able to find faults earlier and more accurately and comprehensively. Hence, for a dynamic nonlinear system similar to the TE plant, CVKA is a more efficient method than others. 

## **5. Discussion** 

## _5.1. Outcomes_ 

A new nonlinear dynamic process monitoring method was proposed based on the multilayer model. The new model consisted of two layers, which were a CVA layer and a KPCA layer. The first CVA layer explained the linearities and dynamics and the second KPCA layer explained the nonlinearities. A TE plant was used as a case study for verification. The results showed that CVKA attained a higher FDR, an earlier FDT than DKPCA, DeDPCA and KCVA, while keeping a relatively low FAR. 

11 of 12 

_Processes_ **2023** , _11_ , 99 

## _5.2. Limitations_ 

One limitation is that in a hierarchical statistical model it is not easy to get the contribution of each original variable to the fault. The number of mappings increases the difficulty of the contribution calculation. Therefore, the interpretation is not obvious, and it is hard to 

Another limitation is that when the CVA algorithm constructs the historical matrix and the future matrix, the dimensionality of the data is greatly increased, and the subsequent dimensionality reduction processing effect is not ideal. It may increase the computational complexity. 

## _5.3. Further Research_ 

Future work may include selecting optimum parameters, such as the type of kernel functions, how many PCs or CVs should be retained and so on. Moreover, computing the contributions of each variable to a fault may be one potential future work. 

## **6. Conclusions** 

In this paper, the significance of nonlinear dynamic fault detection in industrial processes was emphasized and the shortcomings of existing nonlinear dynamic MSPM techniques were analysed. To solve this problem, a novel nonlinear dynamic process monitoring technique was proposed in which KPCA was applied to the CVA residual space, called CVKA. The new method could extract dynamic linear and nonlinear features efficiently. A kernel-based method was applied to avoid a complex neural network optimization. The fusion of _T_<sup>2</sup> based on different features reduced the false alarm rate. Using a TE case study designed to simulate 20 faults, the CVKA method was shown to be superior to DKPCA, KCVA and DeDPCA methods in nonlinear dynamic process monitoring for TE-like systems. 

> **Author Contributions:** Conceptualization, Y.C. and S.L.; methodology, Y.C. and S.L.; software, S.L.; validation, S.L.; formal analysis, S.-h.Y., Y.C. and S.L.; investigation, S.L.; resources, S.-h.Y. and Y.C.; data curation, S.L.; writing—original draft preparation, S.L.; writing—review and editing, S.-h.Y. and Y.C.; visualization, S.L.; supervision, S.-h.Y. and Y.C.; project administration, S.-h.Y.; funding acquisition, S.-h.Y. All authors have read and agreed to the published version of the manuscript. 

**Funding:** This research received no external funding. 

### **Data Availability Statement:** Not applicable. 

## **References** 

1. Wang, Y.; Si, Y.; Huang, B.; Lou, Z. Survey on the theoretical research and engineering applications of multivariate statistics process monitoring algorithms: 2008–2017. _Can. J. Chem. Eng._ **2018** , _96_ , 2073–2085. [CrossRef] 

2. Karamizadeh, S.; Abdullah, S.M.; Manaf, A.A.; Zamani, M.; Hooman, A. An overview of principal component analysis. _J. Signal Inf. Process._ **2020** , _4_ , 173–175. [CrossRef] 

3. Lu, Q.; Jiang, B.; Gopaluni, R.B.; Loewen, P.D.; Braatz, R.D. Sparse canonical variate analysis approach for process monitoring. _J. Process Control_ **2018** , _71_ , 90–102. [CrossRef] 

4. Kramer, M.A. Nonlinear principal component analysis using autoassociative neural networks. _AIChE J._ **1991** , _37_ , 233–243. [CrossRef] 

5. Lee, J.M.; Yoo, C.; Choi, S.W.; Vanrolleghem, P.A.; Lee, I.B. Nonlinear process monitoring using kernel principal component analysis. _Chem. Eng. Sci._ **2004** , _59_ , 223–234. [CrossRef] 

6. Ku, W.; Storer, R.H.; Georgakis, C. Disturbance detection and isolation by dynamic principal component analysis. _Chemom. Intell. Lab. Syst._ **1995** , _30_ , 179–196. [CrossRef] 

7. Deng, X.; Tian, X.; Chen, S.; Harris, C.J. Deep principal component analysis based on layerwise feature extraction and its application to nonlinear process monitoring. _IEEE Trans. Control Syst. Technol._ **2018** , _27_ , 2526–2540. [CrossRef] 

8. Chen, H.; Jiang, B.; Lu, N.; Mao, Z. Deep PCA based real-time incipient fault detection and diagnosis methodology for electrical drive in high-speed trains. _IEEE Trans. Veh. Technol._ **2018** , _67_ , 4819–4830. [CrossRef] 

9. Dong, Y.; Qin, S.J. A novel dynamic PCA algorithm for dynamic data modeling and process monitoring. _J. Process Control_ **2018** , _67_ , 1–11. [CrossRef] 

12 of 12 

_Processes_ **2023** , _11_ , 99 

10. Wu, P.; Ferrari, R.M.G.; Liu, Y.; van Wingerden, J.W. Data-Driven Incipient Fault Detection via Canonical Variate Dissimilarity and Mixed Kernel Principal Component Analysis. _IEEE Trans. Ind. Inform._ **2021** , _17_ , 5380–5390. [CrossRef] 

11. Russell, E.L.; Chiang, L.H.; Braatz, R.D. Fault detection in industrial processes using canonical variate analysis and dynamic principal component analysis. _Chemom. Intell. Lab. Syst._ **2000** , _51_ , 81–93. [CrossRef] 

12. Zheng, J.; Zhao, C. Enhanced canonical variate analysis with slow feature for dynamic process status analytics. _J. Process Control_ **2020** , _95_ , 10–31. [CrossRef] 

13. Odiowei, P.E.P.; Cao, Y. Nonlinear dynamic process monitoring using canonical variate analysis and kernel density estimations. _IEEE Trans. Ind. Inform._ **2009** , _6_ , 36–45. [CrossRef] 

14. Samuel, R.T.; Cao, Y. Kernel canonical variate analysis for nonlinear dynamic process monitoring. _IFAC-PapersOnLine_ **2015** , _48_ , 605–610. [CrossRef] 

15. Pilario, K.E.S.; Cao, Y. Canonical variate dissimilarity analysis for process incipient fault detection. _IEEE Trans. Ind. Inform._ **2018** , _14_ , 5308–5315. [CrossRef] 

16. Pilario, K.E.S.; Cao, Y.; Shafiee, M. Mixed kernel canonical variate dissimilarity analysis for incipient fault monitoring in nonlinear dynamic processes. _Comput. Chem. Eng._ **2019** , _123_ , 143–154. [CrossRef] 

17. Choi, S.W.; Lee, I.B. Nonlinear dynamic process monitoring based on dynamic kernel PCA. _Chem. Eng. Sci._ **2004** , _59_ , 5897–5908. [CrossRef] 

18. Li, S.; Yang, S.; Cao, Y.; Ji, Z. Nonlinear dynamic process monitoring using deep dynamic principal component analysis. _Syst. Sci. Control Eng._ **2022** , _10_ , 55–64. [CrossRef] 

19. Guo, L.; Wu, P.; Lou, S.; Gao, J.; Liu, Y. A multi-feature extraction technique based on principal component analysis for nonlinear dynamic process monitoring. _J. Process Control_ **2020** , _85_ , 159–172. [CrossRef] 

20. Chen, H.; Li, L.; Shang, C.; Huang, B. Fault detection for nonlinear dynamic systems with consideration of modeling errors: A data-driven approach. _IEEE Trans. Cybern._ **2022** . [CrossRef] 

21. Chen, H.; Chen, Z.; Chai, Z.; Jiang, B.; Huang, B. A single-side neural network-aided canonical correlation analysis with applications to fault diagnosis. _IEEE Trans. Cybern._ **2022** , _52_ , 9454–9466. [CrossRef] [PubMed] 

22. Wang, G.; Jiao, J.; Yin, S. A kernel direct decomposition-based monitoring approach for nonlinear quality-related fault detection. _IEEE Trans. Ind. Inform._ **2016** , _13_ , 1565–1574. [CrossRef] 

23. Lomov, I.; Lyubimov, M.; Makarov, I.; Zhukov, L.E. Fault detection in Tennessee Eastman process with temporal deep learning models. _J. Ind. Inf. Integr._ **2021** , _23_ , 100216. [CrossRef] 

24. Capaci, F.; Vanhatalo, E.; Kulahci, M.; Bergquist, B. The revised Tennessee Eastman process simulator as testbed for SPC and DoE methods. _Qual. Eng._ **2019** , _31_ , 212–229. [CrossRef] 

25. Braatz Group. Massachusetts Institute of Technology Advanced Manufacturing Systems. Available online: http://web.mit.edu/ braatzgroup/links.html (accessed on 28 September 2022). 

**Disclaimer/Publisher’s Note:** The statements, opinions and data contained in all publications are solely those of the individual author(s) and contributor(s) and not of MDPI and/or the editor(s). MDPI and/or the editor(s) disclaim responsibility for any injury to people or property resulting from any ideas, methods, instructions or products referred to in the content. 

