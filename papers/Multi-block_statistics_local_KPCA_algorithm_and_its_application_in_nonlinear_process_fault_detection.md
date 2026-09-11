Neurocomputing 376 (2020) 222–231 


![](Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection_images/Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection.pdf-0001-01.png)


Contents lists available at ScienceDirect 

# ~~Neurocomputing~~ 

journal homepage: www.elsevier.com/locate/neucom 


![](Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection_images/Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection.pdf-0001-05.png)


## Multi-block statistics local kernel principal component analysis algorithm and its application in nonlinear process fault detection 


![](Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection_images/Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection.pdf-0001-07.png)


### Bingqian Zhou, Xingsheng Gu<sup>∗</sup> 

_Key Laboratory of Advanced Control and Optimization for Chemical Processes (East China University of Science and Technology), Ministry of Education, Shanghai 200237, China_ 

|a r t i c l e<br>i n f o|a b s t r a c t|
|---|---|
|_Article_ _history:_<br>Received 31 July 2019<br>Revised 19 September 2019<br>Accepted 25 September 2019<br>Available online 27 September 2019|It is vital for fault detection technology to extract features of industrial process data effectively. Local ker-<br>nel principal component analysis (LKPCA) has proved its good performance in preserving global and local<br>structural characteristics. However, it ignored useful high-order statistics of data, so multi-block statis-<br>tics local kernel principal component analysis (MSLKPCA) algorithm integrating statistics pattern analysis<br>(SPA) into LKPCA is proposed. The correlation coefcient matrix is frst calculated and K-means clustering|
|Communicated by Bo Shen|is adopted to divide the original variables into several blocks. Then the weighted SPA, which gives dif-|
|_Keywords:_<br>Multi-block<br>Local KPCA<br>Statistics pattern analysis|ferent weights to different samples in each window according to their distributions, is adopted to build<br>statistic spaces containing both low-order and high-order statistics. After that, LKCPA is performed in each<br>statistic space to realize feature extraction. To reduce the noise effect am plifed by SPA, PCA is adopted<br>in the residual space to remove noise. Bayesian strategy is used to fuse the results of each block and|
|Bayesian strategy analysis<br>Fault detection|two monitoring statistics _E_ _T_ and _E_ _R_ are proposed to monitor the feature space and the residual space<br>respectively. The Tennessee–Eastman (TE) process simulation shows the effectiveness and superiority of<br>the proposed algorithm for process monitoring.<br>© 2019 Elsevier B.V. All rights reserved.|



#### **1. Introduction** 

The development of science and technology has promoted the complexity and integration of modern industry, which leads to the restricted application of traditional multivariate statistical process monitoring techniques such as principal component analysis (PCA) [1], partial least squares (PLS) [2], fisher discriminant analysis (FDA) [3] and independent component analysis (ICA) [4] in industrial processes. For the purpose of enhancing the ability in fault detection, some manifold algorithms like locally linear embedding (LLE) [5], neighborhood preserving embedding (NPE) [6], Laplacian eigenmap (LE) [7], isometric feature mapping (ISPMAP) [8] and locality preserving projections (LPP) [9] have been proposed to preserve local nonlinear structure, while these algorithms cannot preserve global and local structures at the same time. 

Recently, taking into account the global variance and local nonlinear characteristics, scholars have proposed some new linear dimensionality reduction algorithms Zhang et al. proposed a global-local structure analysis (GLSA) method by establishing a new optimization objective function to obtain better fault detection results [10]. Yu proposed local and global principal component 

> ∗ Corresponding author. _E-mail address:_ xsgu@ecust.edu.cn (X. Gu). 

analysis (LGPCA) with a different construction of objective function [11]. Tong et al. proposed an orthogonal multi-manifold projection (OMMP) algorithm that embeds neighbors’ permutation information in sub-targets of the global structure and solves the problem of non-orthogonal feature vectors [12]. Shi et al. proposed a model based on ensemble structure analysis which combines PCA, LPP and MMP [13]. Luo et al. proposed a nonlocal and local structure preserving projection (NLSPP) algorithm, which can simultaneously preserve nonlocal and local structures with the use of nonlocal and local similarity weight coefficients [14]. Zhan et al. proposed global-local manifold analysis by incorporating statistical local approach into local and nonlocal embedding. These methods can achieve good results in linear systems, but unsatisfactory results in nonlinear processes. So some nonlinear algorithms have already been proposed [15]. Deng et al. proposed a local KPCA (LKPCA) algorithm that integrates local structure analysis with KPCA and constructs a new optimization objective which naturally involves both global and local structure information [16]. Cui et al. proposed ensemble LKPCA with different kernel width parameters [17]. Luo et al. proposed a kernel global-local preserving projections (KGLPP) algorithm, which performs more powerfully than KPCA and KLPP in capturing useful data characteristics [18]. She et al. proposed kernel orthogonal global-local preserving projections (KOGLPP) to overcome the non-orthogonality of KGLPP [19]. 

https://doi.org/10.1016/j.neucom.2019.09.075 0925-2312/© 2019 Elsevier B.V. All rights reserved. 

_B. Zhou and X. Gu / Neurocomputing 376 (2020) 222–231_ 

223 

With the increase in the dimension and complexity of industrial data, the high-order statistics are becoming more and more significant. He et al. proposed statistics pattern analysis (SPA) to compute low-order and high-order statistics to build statistic spaces of original data [20], which has already been applied in process monitoring. He et al. combined SPA and LPP to extract local and non-Gaussian features called statistics locality preserving projections (SLPP) [21]. Peng et al. combined SPA with kernel ICA (KICA) and introduced Markov distance to analyze the internal relations between samples, which is superior to the traditional feature decomposition monitoring algorithm [22]. Zhang et al. proposed local and global statistics pattern analysis (LGSPA) by integrating SPA into LGPCA [23]. Yang et al. proposed a method called balanced partial least square and SPA to promote the performance in process monitoring [24]. 

where _w_ and _c_ represent the window width and the current sample index respectively. So **_X_** _c_ can be seen as a subsampled set, and we can obtain a statistics pattern (SP) by calculating kinds of statistics of **_X_** _c_ . The paper chooses four statistics to constitute an SP for less calculation and lower dimensionality, mentioned as follows. 

Mean constitutes the statistics: 


![](Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection_images/Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection.pdf-0002-05.png)


Variance constitutes the second-order statistics: 


![](Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection_images/Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection.pdf-0002-07.png)


In order to extract features better and enhance the ability in fault detection of nonlinear process, a new algorithm called multiblock statistics local kernel principal component analysis is proposed. SPA is introduced to extract high-order statistics in the paper, which is beneficial to extract more features, but it also brings exorbitant dimensions since the dimension will multiply. In order to avoid the issue, original variables are divided into several blocks according to correlations between variables firstly. It not only reduces dimensions, but also facilitates the ability in feature extraction. Given that SPA amplifies the characteristics of original data accompanied by decaying ability in noise tolerance, weighted SPA is proposed to smooth the fluctuation caused by noise in the window based on samples’ distribution and performed to construct different statistic spaces of each block secondly. Thirdly, LKPCA is adopted to project each statistic space into the feature space and the residual space. Since the fluctuation of data caused by noise are mostly distributed in the residual space, PCA is employed further to eliminate noise in the residual space. Then two monitoring statistics are constructed for monitoring. Eventually, Bayesian fusion strategy is used to integrate the performances of each block. The TE process validates that the proposed method has a better performance in nonlinear process fault detection. 

Other second-order statistics such as correlation, auto-correlation and cross-correlation are not considered because the paper focuses on the ability of processing non-linear data rather than describing the temporal relationships between samples. 

Skewness and kurtosis constitute the high-order statistics: 


![](Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection_images/Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection.pdf-0002-11.png)


#### _2.2. Local kernel principal component analysis_ 

Kernel principal component analysis (KPCA) is a nonlinear dimensionality reduction algorithm that introduces kernel function into PCA and performs better than PCA in nonlinear industrial process. Map low dimensional space to high dimensional feature space so that nonlinear space can be turned into linear space, which is beneficial to subsequent fault detection. Assuming a data set **_X_** = [ **_x_** 1 _,_ **_x_** 2 _,_ · · · _,_ **_x_** _n_ ]<sup>T</sup> ∈ **_R_**<sup>_n_×</sup><sup>_m_</sup> , a nonlinear map can be expressed as **_x_** _i_ ∈ **_R_**<sup>_m_× 1</sup> → **_�_** ( **_x_** _i_ ) ∈ **_R_**<sup>_m_× 1</sup> , where _i_ = 1 _,_ 2 _,_ · · · _, n_ . Then PCA can be performed in the feature space to find the projection vector **_p_** that realizes maximizing variance. The projection of **_x_** _i_ can be described as **_t_** = **_�_** _(_ **_x_** _i)_<sup>T</sup> **_p_** , where **_�_** ( **_x_** _i_ ) is standardized with means and variances. Formulate the KPCA optimization task as [25]: 

The paper is arranged as follows. Section 2 introduces some algorithms including SPA and LKPCA. In Section 3, the variable partitioning strategy is mentioned first. Then MSLKPCA is proposed by introducing weighted SPA in LKPCA. Besides, two monitoring statistics for process monitoring are illustrated. Bayesian fusion strategy and process monitoring procedures are also introduced. The efficiency of the proposed method is demonstrated in Section 4. Finally, the work done in this paper and future work are summarized in Section 5. 

#### **2. Review of SPA and LKPCA** 


![](Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection_images/Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection.pdf-0002-16.png)


#### _2.1. Statistics pattern analysis_ 

High-order statistics of nonlinear process data usually contain some non-negligible characteristics, which cannot be extracted by traditional multivariate statistical method, so SPA has been proposed. Its procedure can be listed as follows [20]. Given a data set **_X_** = [ **_x_** 1 _,_ **_x_** 2 _,_ · · · _,_ **_x_** _n_ ]<sup>T</sup> ∈ **_R_**<sup>_n_×</sup><sup>_m_</sup> , where _n_ is the number of samples and _m_ is the number of variables. Utilize **_X_** _c_ to denote a window of measurements: 


![](Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection_images/Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection.pdf-0002-19.png)


_B. Zhou and X. Gu / Neurocomputing 376 (2020) 222–231_ 

224 


![](Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection_images/Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection.pdf-0003-02.png)


where **_K_** is _n_ × _n_ kernel matrix, which can be defined as **_K_** _ij_ = _k(_ **_x_** _i,_ **_x_** _j )_ = **_�_** _(_ **_x_** _i)_<sup>T</sup> **_�_** _(_ **_x_** _j )_ . Gauss kernel function _k_ (•) is chosen in the paper. 

In order to analyze the inner relationship within data, local structure analysis (LSA) is introduced. Assuming the highdimensional adjacent samples **_�_** ( **_x_** _i_ ) and **_�_** ( **_x_** _j_ ), LSA aims at finding a project vector **_p_** to keep low-dimensional samples **_y_** _i_ = **_�_**<sup>T</sup> _(_ **_x_** _i)_ **_p_** and **_y_** _j_ = **_�_**<sup>T</sup> _(_ **_x_** _j )_ **_p_** still being closed. Formulate the optimization task as [26]: 


![](Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection_images/Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection.pdf-0003-05.png)


where **_L_** = **_D_** − **_W_**<sup>_n_</sup> is Laplacian matrix. **_D_** is a diagonal matrix consisting of _dii_ =<sup>�</sup> _j_ =1<sup>_wij,i_=1</sup><sup>_,_2</sup><sup>_,_· · ·</sup><sup>_,n_.</sup><sup>**_W_**isanadjacentweighting</sup> matrix. Generally, **_W_** can be decided by _k_ -nearest neighbors (KNN) method [27], expressed as: 


![](Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection_images/Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection.pdf-0003-07.png)


where _Nk_ ( **_x_** _i_ ; **_x_** _j_ ) detonates the union of _N_ ( **_x_** _i_ ) and _N_ ( **_x_** _j_ ). _N_ ( **_x_** _i_ ) and _N_ ( **_x_** _j_ ) represent the neighborhood of **_x_** _i_ and **_x_** _j_ respectively. Generally, _N_ ( **_x_** _i_ ) is calculated based on the Euclidean distance. Considering that LKPCA is adopted on SPs rather than original samples in the paper and adjacent SPs have stronger similarity because they share more samples, _N_ ( **_x_** _i_ ) is calculated based on the timeweighted Euclidean distance _wd_ ( **_x_** _i_ , **_x_** _j_ ), which is formulated as: 


![](Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection_images/Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection.pdf-0003-09.png)


where _d_ ( **_x_** _i_ , **_x_** _j_ ) denotes the Euclidean distance between **_x_** _i_ and **_x_** _j_ and _td_ is a positive constant used to prevent distant samples from overlarge weights. Samples closer in time may have a smaller weight leading to smaller distances. 

Similar to KPCA, **_P_** can be expressed with _α j, j_ = 1 _,_ 2 _,_ · · · _, n_ , so Eq. (9) can be expressed as: 


![](Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection_images/Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection.pdf-0003-12.png)


Introducing LSA into KPCA optimization and the LKPCA optimization can be formed as: 


![](Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection_images/Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection.pdf-0003-14.png)


The problem can be converted into solving the generalized Eigen-decomposition problem: 


![](Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection_images/Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection.pdf-0003-16.png)


a tiny positive regularization parameter can be added to the diagonal values of **_KLK_** when it is singular. Solve Eq. (14) and **_α_** can be obtained. 

#### **3. Multi-block statistics local kernel principal component analysis algorithm for process monitoring** 

#### _3.1. Variable partitioning strategy_ 

Pearson’s correlation coefficient is an information-theoretic and is developed to measure the degree of correlation between two variables. Assuming two vectors **_x_** _i_ and **_x_** _j_ , _pcc_ ( **_x_** _i_ , **_x_** _j_ ) is formulated as [28]: 


![](Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection_images/Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection.pdf-0003-21.png)


where cov _(_ **_x_** _i,_ **_x_** _j )_ is covariance and var _(_ · _)_ is a variance. The _pcc_ ( **_x_** _i_ , **_x_** _j_ ) ranges from −1 to 1, in which negative denotes negative correlations and positive denotes positive correlations. What the paper takes into consideration is the correlations, including negative and positive correlations. So the sign is abandoned and Pearson’s correlation coefficient is calculated according to the following equation: 


![](Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection_images/Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection.pdf-0003-23.png)



![](Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection_images/Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection.pdf-0003-24.png)


the degree of correlation between variables can be observed from **_PCC_** . K-means clustering is adopted to realize the partition of variables in the paper, and **_X_** can be divided into _b_ blocks **_X_**<sup>(1)</sup> , **_X_**<sup>(2)</sup> , ���, **_X_**<sup>(</sup><sup>_b_)</sup> . 

#### _3.2. Multi-block statistics local kernel principal component analysis algorithm_ 

SPA has advantages in magnifying data features. On the one hand, it is beneficial to detect faults, but on the other it leads to that an increasing sensitivity of the algorithm to noise. When a normal sample is disturbed by noise, it might be mistaken for a faulty sample. Hence two aspects are considered to decrease the situation occurs. 

The first consideration is to smooth the impact caused by noise points on each window. Supposing the data distribution within a window is shown in Fig. 1, there are two noise points in the window. The lines in the Fig. 1 represent the distances between each sample point and its _kspa_ nearest neighbor. It is clear that the closer the distances, the denser the distributions of samples. If an SP is calculated on the basis of the original window, the two noise points may cause an alarm. Hence the weighted SPA using the weighted mean based on samples’ distribution to substitute mean is proposed. 

For **_X_** _c_ in Eq. (1), calculate each samples’ _kspa_ nearest distance in the window to constitute **_D_** = [ _D_ 1 _, D_ 2 _,_ · · · _, Dw_ ]. Since the characteristics of a window depends on the most samples, at least half of the samples in each window are needed to judge whether each sample is one of the few noise points or not. So _kspa_ is chosen as half of _w_ . The weighted value _WDq_ of each sample can be formed: 


![](Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection_images/Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection.pdf-0003-30.png)


_B. Zhou and X. Gu / Neurocomputing 376 (2020) 222–231_ 225 


![](Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection_images/Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection.pdf-0004-01.png)


**Fig. 1.** Data distribution of a window. 

where _q_ = 1 _,_ 2 _,_ · · · _, w_ . Small _WDi_ denotes a high possibility of being affected by noise, so it is necessary to reduce its weight when calculating the mean. The new mean in Eq. (1) is defined: 


![](Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection_images/Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection.pdf-0004-04.png)


where _i_ = 1 _,_ 2 _,_ · · · _, m._ Meanwhile, the variance, skewness and kurtosis are all calculated based on the new mean. 

Secondly, considering that data fluctuation caused by noise are mostly distributed in the residual space, a further step in residual space is taken to eliminate noise interference. Supposing _b_ blocks **_X_**<sup>_( j)_</sup> ∈ **_R_**<sup>_n_×</sup><sup>_m( j)_</sup> _, j_ = 1 _,_ 2 _,_ · · · _, b_ , _b_ kernel matrixes **_K_**<sup>SP(1)</sup> , **_K_**<sup>SP(2)</sup> , ���, **_K_**<sup>SP(</sup><sup>_b_)</sup> of their responding statistic matrixes can be obtained. In addition to centralizing **_K_**<sup>SP(</sup><sup>_j_)</sup> , the paper also takes variance scaling into consideration, which can be calculated as [29]: 

**_K_** ¯<sup>SP</sup><sup>_( j)_</sup> = **_K_**<sup>SP</sup><sup>_( j)_</sup> − **_K_**<sup>SP</sup><sup>_( j)_</sup> **_I_** _n_ sp − **_I_** _n_ sp **_K_**<sup>SP</sup><sup>_( j)_</sup> + **_I_** _n_ sp **_K_**<sup>SP</sup><sup>_( j)_</sup> **_I_** _n_ sp (20) 


![](Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection_images/Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection.pdf-0004-08.png)


where **_I_** _n_ ∈ **_R_**<sup>_n_×</sup><sup>_n_</sup> and its elements are all 1/ _n_<sup>sp</sup> . **_K_**<sup>¯</sup> S<sup>SP</sup><sup>_( j)_</sup> is obtained by scaling the centralized kernel matrix **_K_**<sup>¯SP</sup><sup>_( j)_</sup> . The projection matrix **_α_** 1<sup>_( j),_</sup><sup>**_α_**</sup> 2<sup>_( j),_· · ·</sup><sup>_,_</sup><sup>**_α_**</sup> _n_<sup>_( j_sp</sup><sup>_)_with</sup><sup>_λ_1</sup><sup>_,λ_2</sup><sup>_,_· · ·</sup><sup>_,λn_spcanbecalculatedby</sup> LKPCA algorithm. With series of **_α_** _i_<sup>_( j)_,</sup><sup>**_K_**¯</sup> S<sup>SP</sup><sup>_( j)_</sup> can be decomposed into the feature space **_T_**<sup>(</sup><sup>_j_)</sup> and the residual space **_E_**<sup>(</sup><sup>_j_)</sup> : 


![](Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection_images/Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection.pdf-0004-10.png)



![](Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection_images/Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection.pdf-0004-11.png)


where _l_ denotes the number of principal components of the _j_ th block. 

While the feature space extracts useful features including global and local information, the residual space retains most noise information. Conventionally, two monitoring statistics, i.e. _T_<sup>_2_</sup> and _Q_ statistics [30] can be built for fault detection. However, it is inappropriate to use _Q_ statistic to monitor the residual space directly because of amplifying noise. Therefore PCA is performed further, then the transformation matrix **_β_** = [ **_β_** 1<sup>_( j),_</sup><sup>**_β_**</sup> 2<sup>_( j),_· · ·</sup><sup>_,_</sup><sup>**_β_**</sup> _n_<sup>_( j_sp</sup><sup>_)_</sup> − _l_<sup>]canbe</sup> 

achieved. Sort **_β_** according to responding eigenvalues and select the first _le_ vectors to realize noise filtering: 


![](Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection_images/Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection.pdf-0004-15.png)


where **_R_**<sup>(</sup><sup>_j_)</sup> denotes the filtered residual space. For a new sample **_x_** _new_ , two monitoring indices are given depend on **_T_**<sup>(</sup><sup>_j_)</sup> and **_R_**<sup>(</sup><sup>_j_)</sup> : _Tt_<sup>2</sup><sup>_( j)_</sup> = **_t_**<sup>_( j)_T</sup> _(_ **_S_**<sup>_( j)_</sup> _)_<sup>−1</sup> **_t_**<sup>_( j)_</sup> (25) _Tr_<sup>2</sup><sup>_( j)_</sup> = **_r_**<sup>_( j)_T</sup> _(_ **_S_** _r_<sup>_( j))_−1</sup><sup>**_r_**</sup><sup>_( j)_</sup> (26) where **_T_**<sup>_( j)_</sup> = [ **_t_** 1<sup>_( j),_</sup><sup>**_t_**</sup> 2<sup>_( j),_· · ·</sup><sup>_,_</sup><sup>**_t_**</sup> _l_<sup>_( j)_]</sup> and **_R_**<sup>_( j)_</sup> = [ **_r_** 1<sup>_( j),_</sup><sup>**_r_**</sup> 2<sup>_( j),_· · ·</sup><sup>_,_</sup> **_r_** _n_<sup>_( j_sp</sup><sup>_)_</sup> − _l_<sup>].</sup><sup>**_S_**</sup><sup>_( j)_=cov</sup><sup>_(_</sup><sup>**_T_**</sup><sup>_( j))_and</sup><sup>**_S_**</sup> _r_<sup>_( j)_=cov</sup><sup>_(_</sup><sup>**_R_**</sup><sup>_( j))_isthecovariance</sup> matrix of **_T_**<sup>(</sup><sup>_j_)</sup> and **_R_**<sup>(</sup><sup>_j_)</sup> respectively. Their confidence limits can be calculated by kernel density estimation (KDE) method [31]. Assuming a sample data set **_x_** = [ _x_ 1 _, x_ 2 _,_ · · · _, xn_ ]<sup>T</sup> ∈ **_R_**<sup>_n_</sup> , a univariate kernel estimator is defined as: ˆ _n_ **_x_** − _xi f (_ **_x_** _)_ = _nh_<sup>1</sup> � _k_ � _h_ � (27) _i_ =1 where _h_ is the kernel width. What’s more, _k_ ( · ) denotes the chosen kernel function, which is often selected as Gaussian kernel function, so is the paper. Once the significant level is chosen, confidence limits _T_<sup>ˆ</sup> _t_<sup>2</sup><sup>_( j)_</sup> and _T_<sup>ˆ</sup> _r_<sup>2</sup><sup>_( j)_</sup> can be determined. 

#### _3.3. Bayesian strategy and ensemble learning_ 

Since variables are divided into several blocks, it is necessary to combine their performance. Bayesian inference method can provide a pragmatic and intuitionistic solution [32], which is employed to combine different blocks’ performance. 

For the _j_ th module, its statistics and corresponding control limits are _Tt_<sup>2</sup><sup>_( j)_</sup> , _Tr_<sup>2</sup><sup>_( j)_</sup> , _T_<sup>ˆ</sup> _t_<sup>2</sup><sup>_( j)_</sup> and _T_<sup>ˆ</sup> _r_<sup>2</sup><sup>_( j)_</sup> respectively. Bayesian inference is adopted to turn _Tt_<sup>2</sup><sup>_( j)_</sup> and _Tr_<sup>2</sup><sup>_( j)_</sup> into probabilities [17]: 


![](Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection_images/Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection.pdf-0004-20.png)



![](Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection_images/Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection.pdf-0004-21.png)



![](Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection_images/Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection.pdf-0004-22.png)


_B. Zhou and X. Gu / Neurocomputing 376 (2020) 222–231_ 

226 


![](Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection_images/Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection.pdf-0005-02.png)


**Fig. 2.** Flowsheet of TE process. 

Fusing the monitoring results of each sub-model and the final probabilities _ET_ and _ER_ can be obtained: 


![](Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection_images/Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection.pdf-0005-05.png)


When _ET_ or _ER_ exceeds 1- _α_ , abnormal condition is considered to have occurred. 

- (2) Use the weighted SPA to calculate their statistic matrixes **_x_**<sup>sp</sup> new<sup>_(j)_.Whenthenumberofcollectingsamplesislessthan</sup> _w_ , training samples are used to make up for it. Normalize **_x_**<sup>sp</sup> new<sup>_(j)_togetnormalizedmatrixes</sup><sup>**_x_**¯sp</sup> new<sup>_(j)_;</sup> 

- (3) Compute **_k_** ¯ new<sup>sp</sup><sup>_( j_</sup> _,_<sup>_)_</sup> s<sup>.Then</sup> the<sup>project</sup> kernel matrixes,<sup>themwith</sup> centering<sup>responding</sup> and scaling<sup>projection</sup> it to<sup>ma-</sup> get (4) trixesCombineandeachthe model’sstatisticsresults _Tt_<sup>2</sup> _,_ new<sup>_( j)_</sup> with<sup>and</sup><sup>_T_</sup> Bayesian _r_<sup>2</sup> _,_ new<sup>_( j)_can</sup> strategy<sup>beobtained;</sup> and get the final probabilities _ET_ and _ER_ . When they exceed 1- _α_ , abnormal behavior is considered to have occurred. Otherwise, continue. 

#### _3.4. Process monitoring procedure_ 

The process monitoring procedure based on MSLKPCA consists of two steps: off-line modeling and on-line detection. Mainly including: 

The off-line modeling: 

- (1) Normalize training set **_X_** and get **_X_**<sup>¯</sup> . Calculate Pearson’s correlation coefficient within variables of **_X_**<sup>¯</sup> and then divide **_X_** into _b_ modules **_X_**<sup>(1)</sup> , **_X_**<sup>(2)</sup> , ���, **_X_**<sup>(</sup><sup>_b_)</sup> by K-means clustering; 

- (2) Adopt weighted SPA to obtain statistic matrixes **_X_**<sup>SP</sup><sup>_( j)_</sup> ∈ **_R_**<sup>_n_sp×</sup><sup>_m_sp</sup><sup>_( j)_</sup> _, j_ = 1 _,_ 2 _,_ · · · _, b_ . Normalize **_X_**<sup>SP(</sup><sup>_j_)</sup> with its mean **_X_** vector¯<sup>SP</sup><sup>_( j)_</sup> ; and covariance vector to get normalized matrixes 

- (3) Apply nonlinear mapping to obtain kernel matrixes **_K_**<sup>SP(</sup><sup>_j_)</sup> ∈ **_R_**<sup>_n_×</sup><sup>_n_</sup> , centering and scaling **_K_**<sup>SP(</sup><sup>_j_)</sup> to get **_K_**<sup>¯</sup> S<sup>SP</sup><sup>_( j)_</sup> . Solve the generalized Eigen-decomposition problem to get projection matrixes; 

- (4) Calculate _Tt_<sup>2</sup><sup>_( j)_</sup> and _Tr_<sup>2</sup><sup>_( j)_</sup> statistics of normal data, using KDE to calculate their corresponding confidence limits _._ 

The on-line detection: 

- (1) For the current sample **_x_** new, divide it into _b_ blocks **_x_** new<sup>_(_1</sup><sup>_),_</sup><sup>**_x_**</sup> new<sup>_(_2</sup><sup>_),_· · ·</sup><sup>_,_</sup><sup>**_x_**</sup> new<sup>_(b)_;</sup> 

#### **4. Case study** 

The TE process is provided to illustrate the validity and outperformance of the proposed method. Four methods including LKPCA, SKPCA and MSLKPCA are applied in process monitoring for comparison. 

The TE process, composed of five units including reactor, condenser, separator, stripper and compressor, is a standard experimental simulation platform proposed by Downs and Vogel [33]. The detailed flow sheet can be seen in Fig. 2 Flowsheet of TE process. The process includes 12 operational variables and 41 manipulated variables (MVs), as shown in Table 1. 33 variables (1–22, 42–52) are monitored in this paper. A normal training set and 21 testing sets are used to test different algorithms, which can be downloaded from https://github.com/camaramm/ tennessee-eastman-profBraatz. Details of the 21 faults are listed in Table 2. The training data set includes 500 normal samples while each testing data set includes 960 samples. Faults are introduced from the 161st sample. 

Original variables are divided into _b_ blocks according to the method mentioned in Section 3.1. Consider that each block has few variables when the parameter _b_ is set too large, which is not only 

_B. Zhou and X. Gu / Neurocomputing 376 (2020) 222–231_ 

227 

**Table 1** 

list of the TE process variables. 

##### **Table 3** 

Partition results of the original variables. 

|No|Process variable|Variable b|lock||Variable la|bel|||
|---|---|---|---|---|---|---|---|---|
|1|A feed (stream 1)|1|||2,9,22,23,3|2|||
|2|D feed (stream 2)|2|||7,13,16,20,|27|||
|3|E feed (stream 3)|3|||10,11,18,1|9,28,31|||
|4|Total feed (stream 4)|4|||1,3,4,5,6,8,|12,14,15,17|,21,24,25,26|,29,30,33|
|5|Recycle fow (stream 8)||||||||
|6|Reactor feed rate (Stream 6)||||||||
|7<br>|Reactor pressure<br>|**Table** **4**|||||||
|8|Reactor level|MAR (%) of|three metho|ds for 21 fau|lts.||||
|9|Reactor temperature||||||||
|10|Purge rate (stream 9)<br>|Fault|LKPCA||SPCA||MSLKPC|A|
|11<br>12|Product separator temperature<br>Product separator level|ID|_T_ <sup>_2_</sup>|_Q_|_T_ <sup>_2_</sup>|_Q_|_E_ _T_|_E_ _R_|
|13|Product separator pressure<br>|1|0.13|0.13|0.13|0|0.25|0.25|
|14|Product separator underfow (stream 10)|2|1.25|1.5|1.63|0|1.25|2|
|15|Stripper level|3|91.5|95.5|94.38|0.5|78.88|81.38|
|16|Stripper pressure<br>|4|2|0|13.38|0|0|0|
|17|Stripper underfow (stream 11)|5|68|0|71.63|0|0|0|
|18|Stripper temperature|6|0|0|0|0|0|0|
|19|Stripper steam fow<br>|7|0|0|0|0|0|0|
|20|Compressor work|8|1.5|2|2.25|0|1.13|1.5|
|21|Reactor cooling water outlet temperature|9|91.63|96.25|96|0.13|82.25|85.25|
|22|Separator cooling water outlet temperature<br>|10|23.25|16.38|37.75|0|8.63|8.38|
|23–28|Components A, B, C, D, E and F in stream 6|11|23.75|25.88|6|0|1.25|1.63|
|29–36|Components A, B, C, D, E, F, G and H in stream 9|12|0.88|0.25|0.25|0|0.25|0.25|
|37–41|Components D, E, F, G and H in stream 11<br>|13|4.75|4.38|5.13|0|4.25|4.75|
|42|MV for D feed fow (stream 2)|14|0|0|0.13|0|0.13|0.13|
|43|MV for E feed fow (stream 3)|15|84|93.63|94.75|0.63|78.13|82.63|
|44|MV for A feed fow (stream 1)|16|23|10.75|33.13|0|3|4.13|
|45|MV for total feed fow (stream 4)|17|10.25|2.75|4.63|0|2.13|2.75|
|46|MV for compressor recycle valve|18|10.13|9.38|11|0|9.25|9.88|
|47|MV for purge valve (stream 9)|19|56.88|10.5|3.75|0|0.38|3.63|
|48|MV for separator pot liquid fow (stream 10)|20|29.38|24.38|36.63|0.13|10.38|20.25|
|49|MV for stripper liquid prod fow (stream 11)|21|44.38|50.75|64.25|0|60.13|44.88|
|50|MV for stripper steam valve<br>|AMAR|26.98|21.16|27.46|0.07|16.27|16.84|
|51|MV for reactor cooling water fow||||||||
|52|MV for condenser cooling water fow||||||||



**Table 2** TE process fault patterns. 

|Fault ID|Process variable|Fault type|
|---|---|---|
|1|A/C feed ratio, B composition constant<br>(stream 4)|Step|
|2|B composition, A/C feed ratio constant<br>(stream 4)|Step|
|3|D feed temperature (stream 2)|Step|
|4|Reactor cooling water inlet<br>temperature|Step|
|5|Condenser cooling water inlet<br>temperature|Step|
|6|A feed loss (stream 1)|Step|
|7|C header pressure loss-reduced<br>availability(stream 4)|Step|
|8|A, B and C feed compositions (stream<br>4)|Random variation|
|9|D feed temperature (stream 2)|Random variation|
|10|C feed temperature (stream 4)|Random variation|
|11|Reactor cooling water inlet<br>temperature|Random variation|
|12|Condenser cooling water inlet<br>temperature|Random variation|
|13|Reaction kinetics|Slow shift|
|14|Reactor cooling water valve|Sticking|
|15|Condenser cooling water valve|Sticking|
|16–20|Unknown|Unknown|
|21|Valve position constant (stream 4)|Constant|



increase the influence of variable fluctuations on the performance, but also increase the calculation amount. So the paper divides 33 variables into 4 blocks, as shown in Table 3. 

Three methods including LKPCA, SPCA and MSLKPCA are used for fault detection. The Gaussian kernel function parameters in LKPCA and MSLKPCA can be set according to the number of vari- 

ables [33]. Besides, the paper selects _ls_ as 1 for real-time performance and dynamic property. The parameter _w_ is fixed as 10 to study the effects of different _k_ in each block on the detection results. Select the most sensitive faults of each module, i.e. fault 4, 11 and 14 for block 1, fault 8, 13 and 20 for block 2, fault 1, 5, 12 and 21 for block 3 and fault 1, 10 and 18 for block 4. Calculate the two commonly used indices, false alarming rate (FAR) and average missing alarming rate (MAR) of two statistics under different _k_ values, as shown in Fig. 3. Obviously, the increase of _k_ value is accompanied by the increase of FAR. So the paper sets _k_ as 4, 4, 3 and 3 for block 1–4 in MSLKPCA respectively. The _k_ value in LKPCA is set according to literature [16] for better results. In addition, there is also no conclusion about how to set _w_ , which should take the effect of the fault on the process and its magnitude as consideration. In actual, different parameters should be set for different faults, but it is not realistic because we don’t know what kind of fault is going to occur, and we can’t adjust _w_ according to the forthcoming fault. Hence the paper set the parameter according to the average performance of MSLKPCA under different _w_ and selects fault 1, 5, 8, 10, 11, 14, 19 and 21 that are sensitive to _w_ as representatives to determine _w_ value. In order to prevent high FAR caused by overlarge _w_ , this paper chooses _w_ ranging from 1 to 50. Use the average MAR and the average FAR of _ET_ and _ER_ statistics for those faults to represent different performances under different _w_ , and lower MAR and lower FAR mean better performance. The trend of average FAR and MAR with respect to _w_ is shown in Fig. 4. FAR presents an overall growing trend while MAR presents a fluctuating trend accompanied by increasing _w_ , which means FAR is more sensitive to _w_ than MAR. So the paper sets _w_ as 12 with integrated consideration of stability, low FAR and low MAR, and the same _w_ for SPA for comparison. The number of PCs is determined according to cumulative percent value (CPV) greater than 

228 


![](Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection_images/Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection.pdf-0007-01.png)


**Fig. 3.** The performance of (a) block 1, (b) block 2, (c) block 3 and (d) block 4 with different _k_ . 

**Table 5** Average FAR (%) of three methods for 21 faults. 

||LKPCA||SPCA||MSLKPC|A|
|---|---|---|---|---|---|---|
||_T_ <sup>_2_</sup>|_Q_|_T_ <sup>_2_</sup>|_Q_|_E_ _T_|_E_ _R_|
|AFAR|2.35|3.27|2.08|95.74|5.51|4.43|



85% for all methods. The confidence limit is set to 99% for monitoring statistics. 

Table 4 shows MARs of 21 faults of three methods. It should be noticed that due to different training sets and parameters, some detection results of LKPCA are different from those in literature [16]. In general, three methods can detect fault 1, 2, 6, 7, 8, 12, 13 and 14 better while have poor performance on fault 3, 9 and 15 since the three faults have little impact on the process variables [34]. Take a holistic look of monitoring results, MSLKPCA has a better performance than the other methods, whose average 

MAR (AMAR) of _ET_ and _ER_ statistics are 16.27% and 16.84%. The _T_<sup>2</sup> and _Q_ statistics of LKPCA and SPCA are 26.98%, 21.16% and 27.46%, 0.07%, which validates that the proposed algorithm is more sensitive to faults. Since both lower-order and high-order statistics, local structure and global structure are taken into account simultaneously, the ability in extracting useful information is strengthened. Besides, the weighted SPA and further step in the residual space bring the advantage of SPA and avoid its disadvantage. We can observe that though the _Q_ statistic of SPCA has low AMAR, its average FAR (AFAR) is 95.74% according to Table 5, which is consistent with what was mentioned in Section 3.2. On the contrary, the AFAR of the _ER_ statistic is just 4.43%, explaining the effectiveness and necessity of adopting PCA for noise reduction in the residual space. So the _Q_ statistic of SPCA will not be evaluated in the paper because of its bad description of normal process. Specifically, compared with LKPCA and SPCA, MSLKPCA has an obvious advantage in fault 5, 10, 11, 16, 19 and 20. Fault 5, 10 and 19 are used for a concrete analysis. 

_B. Zhou and X. Gu / Neurocomputing 376 (2020) 222–231_ 229 


![](Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection_images/Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection.pdf-0008-01.png)


**Fig. 4.** Different performances of MSLKPCA under different _w_ . 

Fault 5 is a step change in condenser cooling water inlet temperature. Three monitoring plots are shown in Fig. 5. Since there is a feedback loop to control the effect of the fault on process variables, the _T_<sup>_2_</sup> statistic of LKPCA and SPCA return below corresponding control limits from about the 367th sample, meaning that many fault samples are failed to be detected. In contrast, both _ET_ and _ER_ statistics can detect the variation timely without miss- 

ing faulty samples and greater than the responding control limits continuously. 

Fault 10 describes a random change in the temperature of material c. As fault 10 is a random fault, it is difficult for LKPCA to detect the fault when the changes of a single sample’s variables are not obvious. Nevertheless, MSLKPCA analyzes variations of all samples in the window rather than a single sample, which is favorable for obtaining more seasonable and comprehensive and information. Monitoring plots of three methods are shown in Fig. 6, from which we can see that many faulty samples have not been detected by SPCA and LKPCA. The MARs of their _T_<sup>_2_</sup> statistics are more than 15%. However, the _ET_ and _ER_ statistics of MSLKPCA can detect the fault at 186th and 188th sample respectively with MAR equaling to about 8%, showing better performance. 

Fault 19 is a fault with an unknown type. The monitoring results are listed in Fig. 7. As shown in the figure, the _Q_ statistic of LKPCA shows better performance than _T_<sup>2</sup> statistic, with MAR equaling to 10.5%. The _T_<sup>_2_</sup> statistic shows a smaller MAR, i.e. 3.75%. However, their detected performance are not as good as MSLKPCA. The MAR of the _ET_ statistic is just 0.38% and stays above the control limit after the fault being detected. Compared with LKPCA and SPCA, MSLKPCA shows a satisfying result and the superiority in fault 19. 

In fact, practical nonlinear processes are often disturbed by noise, especial measurement noises in multi-sensor environment [35,36]. The paper takes fault 10 as an example to study the feasibility of MSLKPCA under the disturbance of Gaussian noise considering that the influence of noise on random faults may be greater than that on faults with obvious variations. Gaussian 


![](Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection_images/Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection.pdf-0008-08.png)


**Fig. 5.** Monitoring results for fault 5 by (a) LKPCA (b) SPCA and (c) MSLKPCA. 


![](Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection_images/Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection.pdf-0008-10.png)


**Fig. 6.** Monitoring results for fault 10 by (a) LKPCA (b) SPCA (c) MSLKPCA. 

_B. Zhou and X. Gu / Neurocomputing 376 (2020) 222–231_ 

230 


![](Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection_images/Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection.pdf-0009-02.png)


**Fig. 7.** Monitoring results for fault 19 by (a) LKPCA (b) SPCA and (c) MSLKPCA. 

##### **Table 6** 

##### MAR (%) of MSLKPCA under different Gaussian noises. 


![](Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection_images/Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection.pdf-0009-06.png)



![](Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection_images/Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection.pdf-0009-07.png)


**Fig. 8.** Monitoring results for fault 10 with Gaussian noise. 

measurement noises with mean equaling to 0 and variance ranging from 0.005 to 0.1 are added to these measured variables with regard to temperature, which are variable 9, 11 and 18 for test. The results are shown in Table 6, from which we can observe that MARs of both statistics are not much different from the results in Table 4 when the noise variance is within 0.01. Fig. 8 shows that the monitoring performance of Gaussian noises with variance being 0.01. It can be seen that only small changes occurred in the _ER_ statistic by comparing Fig. 8 with Fig. 6(c). While variances are greater than 0.01, the MARs of both statistics start to increase. So the proposed algorithm shows some robustness to Gaussian noises within the acceptable range. 

#### **5. Conclusion** 

The paper proposes a new algorithm named as multi-block statistics local kernel principal component analysis for nonlinear 

process monitoring. Not only does MSLKPCA make full use of loworder and high-order statistics of process data for better feature extraction, but it also preserves local structure and global structure. Original variables are firstly divided into several blocks based on the collection within variables and K-means clustering. Since SPA enhances fault detection performance by magnifying features, false alarming samples may increase at the same time because of the fluctuation of normal samples caused by noise. So weighted SPA and further processing using PCA to eliminate noise in the residual space are proposed, which is beneficial to reduce the impact of noise and keep low MAR and low FAR simultaneously. The monitoring results of the TE process based on LKPCA, SPCA and MSLKPCA show that the proposed method outperforms the other methods. 

It should be mentioned that the proposed algorithm is suitable for single mode while multiple modes are more prevalent in industrial processes because industries need to cater for the needs of market. So how to enhance the robustness of the proposed algorithm to noise and apply it in multi-mode process and distinguish different modes will be the focus in future studies. 

#### **Declaration of Competing Interest** 

#### None. 

#### **Acknowledgments** 

This work is supported by the National Natural Science Foundation of China (Grant No.61573144, 61773165, 61673175, 61973120), the Program of Introducing Talents of Discipline to Universities (the 111 Project) (Grant No. B17017), Fundamental Research Funds for the Central Universities (No. 222201917006). 

#### **References** 

- [1] V. Hiranamayee, V. Venat, PCA-SDG based process monitoring and fault diagnosis, Contr. Eng. Pract. 8 (1999) 903–917. 

- [2] J.L. Godoy, J.R. Vega, J.L. Marchetti, A fault detection and diagnosis technique for multivariate processes using a PLS-decomposition of the measurement space, Chem. Intell. Lab. Syst. 128 (2013) 25–36. 

- [3] D. Wang, J.A. Romagnoli, A robust discriminate analysis method for process fault diagnosis, Comput.-Aided Chem. Eng. 20 (2005) 1117–1122. 

- [4] A. Ajami, M. Daneshvar, Data driven approach for fault detection and diagnosis of turbine in thermal power plant using independent component analysis (ICA), Int. J. Elec. Power 43 (1) (2012) 728–735. 

- [5] Z.Q. Su, B.P. Tang, J.H. Ma, Fault diagnosis method based on incremental enhanced supervised locally linear embedding and adaptive nearest neighbor classifier, Measurement 48 (2014) 136–148. 

- [6] P.A. Koringa, S.K. Mitra, ONPPn: orthogonal neighborhood preserving projection with normalization and its applications, Image Vis. Comput. 76 (2018) 64–75. 

_B. Zhou and X. Gu / Neurocomputing 376 (2020) 222–231_ 

231 

- [7] P. Arena, L. Patanè, A.G. Spinosa, Data-based analysis of Laplacian eigenmaps for manifold reduction in supervised liquid state classifiers, Inf. Sci. 478 (2019) 28–39. 

- [8] T. Benkedjouh, K. Medjaher, N. Zerhoun, Remaining useful life estimation based on nonlinear feature reduction and support vector regression, Eng. Appl. Artif. Intel. 26 (7) (2013) 1751–1760. 

- [9] Y.S. Zhang, Y. Dong, Y.H. Liu, Robust linear embedding algorithm for the machinery fault diagnosis, Neurocomputing 17 (273) (2019) 323–332. 

- [10] M.G. Zhang, Z.Q. Ge, Z.H. Song, Global-Local structure analysis model and its application for fault detection and identification, Ind. Eng. Chem. Res. 50 (11) (2011) 6837–6848. 

- [11] J.B. Yu, Local and global principal component analysis for process monitoring, J. Process Control 22 (7) (2012) 1358–1373. 

- [12] C.D. Tong, X.H. Shi, T. Lan, Statistical process monitoring based on orthogonal multi-manifold projections and a novel variable contribution analysis, ISA T. 65 (2016) 407–417. 

- [13] L.K. Shi, C.D. Tong, T. Lan, Statistical process monitoring based on ensemble structure analysis, IEEE/CAA J. Automatica Sinica (2018) 1–8. 

- [14] L.J. Luo, S.Y. Bao, J.F. Mao, Nonlocal and local structure preserving projection and its application to fault detection, Chem. Intell. Lab. Syst. 157 (2016) 177–188. 

- [15] C.J. Zhan, S.H. Li, Y.P. Yang, Improved process monitoring based on global-local manifold analysis and statistical local approach for industrial process, J. Process Control 75 (2019) 107–119. 

- [16] X.G. Deng, X.M. Tian, S. Chen, Modified kernel principal component analysis based on local structure analysis and its application to nonlinear process fault diagnosis, Chem. Intell. Lab. Syst. 127 (2013) 195–209. 

- [17] P. Cui, C.J. Zhan, Y.P. Yang, Improved nonlinear process monitoring based on ensemble KPCA with local structure analysis, Chem. Eng. Res. Des. 142 (2019) 355–368. 

- [18] L.J. Luo, S.Y. Bao, J.F. Mao, Nonlinear process monitoring based on kernel global-local preserving projections, J. Process Control 38 (2016) 11–21. 

- [19] B. She, F.Q. Tian, W.G. Liang, Nonlinear global-local structure model and its application for condition monitoring and fault detection, proceeding of the 30th Chinese control and decision conference (CCDC), Shenyang (2018) 772–777. 

- [20] Q.P. He, J. Wang, Statistics pattern analysis: a new process monitoring framework and its application to semiconductor batch processes, AIChe J. 1 (57) (2011) 107–121. 

- [21] F. He, J.J.W. Xu, A novel process monitoring and fault detection approach based on statistics locality preserving projections, J. Process Control 37 (2016) 46–57. 

- [22] X. Peng, Y. Tian, Y. Tang, An online performance monitoring using statistics pattern based kernel independent component analysis for non-Gaussian process, in: Proceeding of the 43rd Annual Conference of the IEEE Industrial Electronics Society, Beijing, 2017, pp. 7210–7216. 

- [23] H.Y. Zhang, X.M. Tian, X.G. Deng, A local and global statistics pattern analysis method and its application to process fault identification, Chin. J. Chem. Eng. 23 (2015) 1782–1792. 

- [24] J. Yang, L. Zheng, H.B. S.hi, S. Tan, Performance monitoring method based on balanced partial least square and statistics pattern analysis, ISA T. 81 (2018) 121–131. 

- [25] I. Elaissi, I. Jaffel, O. Taouali, Online prediction model based on the SVD–KPCA method, ISA T. 52 (1) (2013) 96–104. 

- [26] G. Shikkenawis, S.K. Mitra, On some variants of locality preserving projection, Neurocomputing 173 (2016) 196–211. 

- [27] F. He, C.J. Wang, S.K. Fan, Nonlinear fault detection of batch processes based on functional kernel locality preserving projections, Chem. Intell. Lab. Syst. 183 (2018) 79–89. 

- [28] Y.H. Mu, X.D. Liu, L.D. Wang, A Pearson’s correlation coefficient based decision tree and its parallel implementation, Inf. Sci. 435 (2018) 40–58. 

- [29] J.M. Lee, C.K. Yoo, I.B. Lee, Fault detection of batch processes using multiway kernel principal component analysis, Comput. Chem. Eng. 28 (2004) 1837–1847. 

- [30] S. Lee, M. Kwak, K.L. Tsui, S.B. Kim, Process monitoring using variational autoencoder for high-dimensional nonlinear processes, Eng. Appl. Artif. Intell. 83 (2019) 13–27. 

- [31] E.B. Martin, A.J. Morris, Non-parametric confidence bounds for process performance monitoring charts, J. Process Control 6 (6) (1996) 349–358. 

- [32] C.D. Tong, P. Ahmet, X.F. Yan, Improved ICA for process monitoring based on ensemble learning and Bayesian inference, Chem. Intell. Lab. Syst 135 (2014) 141–149. 

- [33] J.J. Downs, E.F. Vogel, A plant-wide industrial process control problem, Comput. Chem. Eng. 17 (3) (1993) 245–255. 

- [34] A. Sánchez-Fernández, F.J. Baldán, G.I. Sainz-Palmero, et al., Fault detection based on time series modeling and multivariate statistical process control, Chem. Intell. Lab. Syst. 182 (2018) 57–69. 

- [35] H.L. Tan, B. Shen, Y.R. Liu, et al., Event-triggered multi-rate fusion estimation for uncertain system with stochastic nonlinearities and colored measurement noises, Inf. Fusion 36 (2017) 313–320. 

- [36] B. Shen, Z.D. Wang, D. Wang, et al., Finite-horizon filtering for a class of nonlinear time-delayed systems with an energy harvesting sensor, Automatica 100 

(2019) 144–152. 


![](Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection_images/Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection.pdf-0010-29.png)


**Bingqian Zhou** received her B.Sc. in Nanjing Forestry University in 2017. She is pursuing her M.Sc. in East China University of Science and Technology. Her research interests include fault detection and diagnosis in industry process. 


![](Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection_images/Multi-block_statistics_local_KPCA_algorithm_and_its_application_in_nonlinear_process_fault_detection.pdf-0010-31.png)


**Xingsheng Gu** received the B.S. degree from Nanjing Institute of Chemical Technology in 1982, M.S. and Ph.D. degree from East China University of Chemical Technology in 1988 and 1993, respectively. He is currently a professor at School of Information Science and Engineering, East China University of Science and Technology. His research interests include planning and scheduling for process industry, modeling, control and optimization for industry processes, intelligent optimization, faults detection and diagnosis, etc. 

