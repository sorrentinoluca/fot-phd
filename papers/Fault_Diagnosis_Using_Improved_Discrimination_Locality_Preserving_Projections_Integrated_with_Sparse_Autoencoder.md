3527108 

IEEE TRANSACTIONS ON INSTRUMENTATION AND MEASUREMENT, VOL. 70, 2021 

# Fault Diagnosis Using Improved Discrimination Locality Preserving Projections Integrated With Sparse Autoencoder 

Yan-Lin He( ) , _Member, IEEE_ , Kun Li( ) , Ning Zhang( ) , Yuan Xu( ) , and Qun-Xiong Zhu( ) 

**_Abstract_ —In order to ensure safe operations of industrial processes, it is especially important to find fault types accurately and quickly based on historical data and then deal with faults in time. Unfortunately, due to the tricky characteristics of industrial process data such as massive number, high dimensionality, and nonlinearity, it turns out that timely and accurate diagnosis of faults becomes of great difficulty in industrial processes. To address this problem, novel effective fault diagnosis using an improved global and local dimensionality reduction (DR) method named discrimination locality preserving projections integrated with sparse autoencoder (SAEDLPP) is proposed in this article. In SAEDLPP, the global DR information of data is first obtained by sparse autoencoder (SAE); next, the DR data obtained through SAE are passed through discrimination locality preserving projections (DLPP) to obtain local DR information, preserving not only the global information but the local information of the extracted features. Finally, fault diagnosis is achieved by separating the extracted features by SAEDLPP using an AdaBoost classifier to recognize fault types. Simulations are conducted on the Tennessee Eastman process (TEP) and the results indicate that the provided SAEDLPP-based fault diagnosis methodology can achieve much higher accuracy in fault diagnosis than other associated methods.** 

**_Index Terms_ —Dimensionality reduction (DR), discriminant locality preserving projections (LPPs), fault diagnosis, industrial processes, sparse autoencoder (SAE).** 

## I. INTRODUCTION 

ITH the development of science and technology and **W** the progress of society, industrial processes are gradually becoming more and more large-scale and complex. If the production process breaks down and faults are not handled in time, huge damage may occur. Therefore, it is particularly important to utilize effective methods of judgment and troubleshooting for timely and reliable diagnosis of process faults [1]. Currently, for the industrial process, fault diagnosis technology has become a popular research direction. Since modern industrial process data are massive, high dimensional, 

Manuscript received August 20, 2021; revised October 20, 2021; accepted October 26, 2021. Date of publication November 8, 2021; date of current version November 19, 2021. This work was supported by the National Natural Science Foundation of China under Grant 62073022 and Grant 61973024. The Associate Editor coordinating the review process was Dr. Xiaofeng Yuan. _(Corresponding authors: Yuan Xu; Qun-Xiong Zhu.)_ 

The authors are with the College of Information Science and Technology, Beijing University of Chemical Technology, Beijing 100029, China (e-mail: heyl@mail.buct.edu.cn; 1164609251@qq.com; zhangnieng@ 126.com; xuyuanbuct@163.com; zhuqx@mail.buct.edu.cn). Digital Object Identifier 10.1109/TIM.2021.3125975 

and nonlinear, it is difficult to analyze process data directly. Thus, it is especially important to reduce the dimensionality of process data for extracting useful features in the first place [2]. With the fast development of sensor and computer technologies, industrial process data can be easily collected and well stored in real time. Therefore, data-driven techniques of fault diagnosis based on historical process data have been broadly developed and utilized [3]. 

Common dimensionality reduction (DR) methods like principal component analysis (PCA) [4], fisher discriminant analysis (FDA) [5], partial least squares (PLSs) [6], and independent component analysis (ICA) [7] have been successfully and widely used in fault detection and fault diagnosis of complex processes. A method of fault detection and diagnosis based on PCA was proposed by Li _et al._ [8]. PCA does not consider the correlation between faults. For handling this problem, Yin _et al._ [6] proposed a process monitoring approach named PLS. PCA and PLS do not consider the discriminative information between classes. What is more, the performance of PCA and ICA relies on the distribution characteristics of data. FDA solves the problem well by adding the discriminative information to its objective function [9]. However, the data in industrial processes are time-series and dynamic in nature. Thus, these static methods do not solve the problem of dynamic nature. Therefore, methods based on dynamic PCA [10], dynamic FDA [11], dynamic PLS [12], etc., were proposed to solve the problem of dynamic data. Unfortunately, the above methods do not take into account the manifold structure between data, resulting in fault diagnosis with low accuracy. 

The above traditional methods only consider the global Euclidean structure, and so it is hard to discover the low-dimensional manifold embedding existing in the highdimensional data. That is to say, the above traditional methods cannot fully extract useful information from high-dimensional data. For addressing this issue, manifold learning-based techniques and methods have been broadly studied and applied [13], [14]. Common manifold learning techniques like isometric mapping (ISOMAP) [15], locally linear embedding (LLE) [16], and locality preserving projections (LPPs) [17] have been successfully utilized. The manifold learning techniques can discover the manifold structure from high-dimensional data with low-dimensional space when performing DR. One of the most commonly used manifold 

1557-9662 © 2021 IEEE. Personal use is permitted, but republication/redistribution requires IEEE permission. See https://www.ieee.org/publications/rights/index.html for more information. 

Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on September 11,2026 at 16:23:57 UTC from IEEE Xplore.  Restrictions apply. 

3527108 

IEEE TRANSACTIONS ON INSTRUMENTATION AND MEASUREMENT, VOL. 70, 2021 

learning models is the LPP algorithm. LPP can find the streaming embedding from high-dimensional samples in lowdimensional space very well; however, the LPP method ignores the discriminative information between classes, limiting its performance in classification problems. To improve the classification performance of LPP, Yu _et al._ [18] introduced the idea of FDA into LPP and then proposed a method called discrimination LPPs (DLPP). Although DLPP has been successfully applied in kinds of fields, DLPP encounters the problem of matrix decomposition [19]. To solve the problem of matrix decomposition, a method that combined PCA with DLPP was proposed [20]. In the PCA + DLPP method, useful information may be lost in the PCA stage; in addition, PCA is a linear model which cannot handle the nonlinearity of process data. When the fault class number is less than the data dimension, PCA + DLPP achieves unsatisfactory classification accuracy. 

As linear tools, manifold learning techniques are generally based on local operations, leading to poor DR when facing massive high-dimensional data. However, the manifold learning algorithms based on global operations pay a fat price in terms of computational amount and computational difficulty. Therefore, the concept of nonlinear DR should be considered. For nonlinear DR, neural networks can be adopted as effective methods of nonlinear global DR. Common neural network DR and feature extraction methods include convolutional neural networks (CNNs) [21], sparse autoencoder (SAE) [22], and self-organizing mapping (SOM) [23]. CNNs are commonly used in image processing; autoencoder-based nonlinear dimension reduction methods have been applied in a number of areas. Common autoencoders include denoising autoencoders [24] and stack autoencoders [25]. Although neural network-based nonlinear DR methods have many good features, the neural network-based nonlinear DR methods do not take into account the manifold structure of data. Traditional manifold learning-based DR algorithms may achieve good DR for certain problems. However, some traditional manifold learning-based DR algorithms are linear and so cannot well deal with highly nonlinear data. 

In order to get good feature extraction performance, it has become a new trend to reasonably combine multiple DR methods for DR and feature extraction. The performance of the PCA + DLPP proposed in [20] is still much limited: PCA and DLPP are linear models which cannot handle the nonlinearity of process data well; the problem of matrix decomposition in DLPP is not fully solved. Generalized autoencoder (GAE) is a method that combines a self-encoder with a manifold learning method [26]. Thus, drawing lessons from GAE and based on the above analysis, this article proposes an improved global and local DR method named DLPPs integrated with SAE (SAEDLPP). SAEDLPP integrates SAE with DLPP. The advantages of this kind of integration are that the global DR information of data can be first obtained by extracting features from data through SAE; next, the local DR information of data can be obtained by developing DLPP for the DR data obtained by SAE. In addition, to further solve the problem of matrix decomposition in SAEDLPP, this article decomposes the objective matrix of DLPP using singular value decomposition (SVD). After obtaining the extracted 


![](Fault_Diagnosis_Using_Improved_Discrimination_Locality_Preserving_Projections_Integrated_with_Sparse_Autoencoder_images/conv_8e287e9d8b601f28.pdf-0002-05.png)


Fig. 1. Structure of autoencoder. 

features using the presented SAEDLPP, fault diagnosis can be finally achieved by separating the extracted features through an AdaBoost classifier to recognize fault types. To select the optimal DR order, the Akaike Information Criterion (AIC) is adopted. All in all, a novel and effective model of fault diagnosis is developed based on SAEDLPP and the AdaBoost classifier. To verify and confirm the superior performance of the presented SAEDLPP-based fault diagnosis, the Tennessee Eastman process (TEP) is utilized for experimental analyses. The experimental results show the introduced SAEDLPPbased fault diagnosis can achieve much higher fault diagnosis accuracy compared with other related models, indicating the proposed SAEDLPP-based fault diagnosis model can be utilized as an effective model for recognizing fault types in the field of large-scale industrial processes. 

The rest of the article is organized below: a brief introduction to the autoencoder, the basic DLPP method, and the basic classification technique of AdaBoost are presented in Section II; in Section III, the proposed fault diagnosis methodology using the proposed SAEDLPP is described in detail; experiments and result analyses using different fault classes of TEP are provided in Section IV and conclusions are given in Section V. 

## II. PRELIMINARY METHODS 

## _A. Sparse Autoencoder_ 

SAE [22] is a kind of neural network with one or more hidden layers. SAE adopts an unsupervised learning algorithm. SAE consists of the input layer, the hidden layer, and the output layer, where the input to the hidden indicates the encoding process and the hidden to the output indicates the decoding process. The network structure of SAE is shown in Fig. 1. The idea of SAE is to make sure that the outputs are equal to the inputs, which can be achieved by adjusting the number of neurons in the hidden layer so as to encode different dimensions. The features learned from the autoencoder can preserve important information of original data. 

SAE adds an extra penalty factor to the loss function of the traditional autoencoder. SAE can process high-dimensional and nonlinear data and find out the main features in the original input data through the encoding and decoding processes. SAE can discriminate the sparse features of data in the decoding process by adding an extra penalty term so that the parameters of the encoder and decoder can be adjusted to minimize the errors between outputs and inputs [22]. 

Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on September 11,2026 at 16:23:57 UTC from IEEE Xplore.  Restrictions apply. 

3527108 

HE _et al._ : FAULT DIAGNOSIS USING IMPROVED SAEDLPP 

## _B. Discriminant LPPs_ 

DLPP [19] is a manifold learning DR algorithm based on the popular learning algorithm LPP. The idea of the FDA is added to LPP to develop DLPP. DLPP can reflect the discriminative information between and within samples in the objective function so that the optimal subspace information can be obtained, improving classification ability. 

For a given dataset **_X_** , suppose a total of _n_ samples are included and the data are divided into _K_ categories. Each class has _nk_ samples. Then the dataset **_X_** can be expressed as 


![](Fault_Diagnosis_Using_Improved_Discrimination_Locality_Preserving_Projections_Integrated_with_Sparse_Autoencoder_images/conv_8e287e9d8b601f28.pdf-0003-05.png)


where **_x_**<sup>_k_</sup> _i_<sup>∈</sup><sup>**_R_**</sup><sup>_m_means the</sup><sup>_i_th observation of the</sup><sup>_k_th class and</sup> each observation is an _m_ -dimensional vector; _nk_ represents the number of samples in the class _k_ , i.e., _n_ = _n_ 1 + _n_ 2 + · · · + _ni_ + · · · + _n K_ . The purpose of DLPP is to find a projection matrix **_V_** ∈ **_R_**<sup>_m_∗</sup><sup>_a_</sup> _(a_ ≤ _m)_ and **_y_** _i_ = **_V_**<sup>_T_</sup> **_x_** _i_<sup>_K, i_</sup> = 1 _,_ 2 _, . . . , nk, c_ = 1 _,_ 2 _, . . . , K_ . Details about DLPP can be found in [19]. 

## _C. AdaBoost Classification_ 

The AdaBoost classifier is different from the single classifier such as the Bayesian classifier and the decision tree classifier. AdaBoost belongs to an integrated learning classifier. AdaBoost adopts the iteration idea; in each iteration, only one weak classifier is trained and the weak classifier trained in this iteration will participate in the next iteration process. _N_ weak classifiers are trained by _N_ iterations. When the _N_ + 1st iteration is performed, the parameters of the first _N_ iterators do not change and only the data that are not sorted by the first _N_ iterators are classified. Eventually, all trained weak classifiers are linearly combined to make a strong classifier for achieving good classification. Thus, the AdaBoost classifier is adopted. Details about the AdaBoost classifier can be found in [27]. 

## III. PROPOSED SAEDLPP FAULT DIAGNOSIS 

In this section, the specific solution of the proposed SAEDLPP is presented. In order to overcome the matrix decomposition problem in DLPP, the feature extraction of the original data with the proposed method SAEDLPP is adopted first and then SVD is used in the matrix decomposition. Finally, the classification is performed by AdaBoost which can be used as a good tool to solve the problem of fault diagnosis. 

## _A. Global Feature Extraction Using SAE_ 

For a given dataset **_X_** and the concrete expression in (1), _n_ means the sample number and _m_ means the dimensionality of the samples. The fault data are normalized and the normalization formula is shown in the following equation: 


![](Fault_Diagnosis_Using_Improved_Discrimination_Locality_Preserving_Projections_Integrated_with_Sparse_Autoencoder_images/conv_8e287e9d8b601f28.pdf-0003-13.png)



![](Fault_Diagnosis_Using_Improved_Discrimination_Locality_Preserving_Projections_Integrated_with_Sparse_Autoencoder_images/conv_8e287e9d8b601f28.pdf-0003-14.png)


where **_x_**<sup>_k_</sup> _i_<sup>representseachsample,</sup> **_x_**<sup>_k_</sup> _i_<sup>representsthemeanof</sup> all samples, and _σ_ represents the sample variance. 

The input to the SAE is **_X_** = { **_x_** 1 _,_ **_x_** 2 _, . . . ,_ **_x_** _i , . . . ,_ **_x_** _n_ } and the output is **_Y_** = { **_y_** 1 _,_ **_y_** 2 _, . . . ,_ **_y_** _i , . . . ,_ **_y_** _n_ }. **_x_** _i ,_ **_y_** _i_ ∈ **_R_**<sup>_m_</sup> are _m_ -dimensional vectors. The loss function for SAE is shown in the following equation: 


![](Fault_Diagnosis_Using_Improved_Discrimination_Locality_Preserving_Projections_Integrated_with_Sparse_Autoencoder_images/conv_8e287e9d8b601f28.pdf-0003-17.png)


where _Z_ means the number of hidden neural sources in the hidden layer, _i_ denotes the _i_ th input sample, _n_ means the training sample number, _λ_ is the penalty term weight, _β_ is the sparsity weight, and _j_ represents the individual neurons in the hidden layer. The sparse penalty term is shown in the following equation: 


![](Fault_Diagnosis_Using_Improved_Discrimination_Locality_Preserving_Projections_Integrated_with_Sparse_Autoencoder_images/conv_8e287e9d8b601f28.pdf-0003-19.png)


Adding (4) to the objective function will make the features obtained from learning more binding rather than simply repeating the inputs. The expression for _K L(ρ_ || _ρ j )_ is given in the following equation: 


![](Fault_Diagnosis_Using_Improved_Discrimination_Locality_Preserving_Projections_Integrated_with_Sparse_Autoencoder_images/conv_8e287e9d8b601f28.pdf-0003-21.png)


where _ρ_ means the sparsity parameter; the parameter is usually a value close to zero and _ρ j_ =<sup>�</sup><sup>_n_</sup> _j_ =1<sup>_(_1</sup><sup>_/n)h j(x j)_,where</sup><sup>_ρ j_</sup> means the average activation of the hidden layer neurons. 

Suppose that the number of nodes in the hidden layer of SAE is _Z_ . Then the hidden layer data **_X_** SAE = { **_x_** SAE1 _,_ **_x_** SAE2 _, . . . ,_ **_x_** SAE _n_ } can be obtained after SAE learning, where the expression for _c_ is shown (6). **_x_** SAE _i_ ∈ **_R_**<sup>_z_</sup> belongs to the _z_ -dimensional vector. In (6), **_w_** 1, **_b_** 1 are the weights and biases of SAE, respectively 


![](Fault_Diagnosis_Using_Improved_Discrimination_Locality_Preserving_Projections_Integrated_with_Sparse_Autoencoder_images/conv_8e287e9d8b601f28.pdf-0003-24.png)


## _B. Local Feature Extraction Using DLPP_ 

The target of DLPP is to find a set of projection vectors **_V_** ∈ **_R_**<sup>_z_∗</sup><sup>_a_</sup> . After feature extraction by SAE, the data become as **_X_** SAE = { **_x_** SAE1 _,_ **_x_** SAE2 _, . . . ,_ **_x_** SAE _n_ }, where each sample is a _k_ -dimensional vector. This section uses DLPP for feature extraction from **_X_** SAE. The objective function of DLPP is shown in the following equation: 


![](Fault_Diagnosis_Using_Improved_Discrimination_Locality_Preserving_Projections_Integrated_with_Sparse_Autoencoder_images/conv_8e287e9d8b601f28.pdf-0003-27.png)


where **_m_** _i_ = _(_ 1 _/ni )_<sup>�</sup><sup>_n_</sup> _k_ =<sup>_i_</sup> 1<sup>**_x_**</sup><sup>_i_</sup> _k_<sup>and</sup><sup>**_m_**</sup><sup>_j_=</sup><sup>_(_1</sup><sup>_/n j)_�</sup><sup>_n_</sup> _k_ =<sup>_j_</sup> 1<sup>**_x_**</sup><sup>_j_</sup> _k_<sup>are</sup> the means of the _i_ th and the _j_ th class samples. **_Q_**<sup>_k_</sup> _i j_<sup>isthe</sup> weight relationship between any two samples in the class _K_ and the expression of **_Q_**<sup>_k_</sup> _i j_<sup>isshown inthefollowing equation:</sup> 


![](Fault_Diagnosis_Using_Improved_Discrimination_Locality_Preserving_Projections_Integrated_with_Sparse_Autoencoder_images/conv_8e287e9d8b601f28.pdf-0003-29.png)


Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on September 11,2026 at 16:23:57 UTC from IEEE Xplore.  Restrictions apply. 

3527108 

IEEE TRANSACTIONS ON INSTRUMENTATION AND MEASUREMENT, VOL. 70, 2021 

In (7), **_T_** _i j_ represents the weight relationship between the mean vector of the sample in class _i_ and the sample in class _j_ . The expression of **_T_** _i j_ is shown in the following equation: 

Then, the transformed molecule in (11) and the transformed denominator in (10) are brought into the original objective function (7). The objective function of (7) is transformed into the following equation: 


![](Fault_Diagnosis_Using_Improved_Discrimination_Locality_Preserving_Projections_Integrated_with_Sparse_Autoencoder_images/conv_8e287e9d8b601f28.pdf-0004-04.png)



![](Fault_Diagnosis_Using_Improved_Discrimination_Locality_Preserving_Projections_Integrated_with_Sparse_Autoencoder_images/conv_8e287e9d8b601f28.pdf-0004-05.png)


The denominator of (7) can be transformed to (10) by a simple algebraic derivation 

The final solution of (14) can be equivalent to the solution of the following equation: 


![](Fault_Diagnosis_Using_Improved_Discrimination_Locality_Preserving_Projections_Integrated_with_Sparse_Autoencoder_images/conv_8e287e9d8b601f28.pdf-0004-08.png)



![](Fault_Diagnosis_Using_Improved_Discrimination_Locality_Preserving_Projections_Integrated_with_Sparse_Autoencoder_images/conv_8e287e9d8b601f28.pdf-0004-09.png)


where **_X_** SAE **_U X_** SAE<sup>_T_isa</sup><sup>_z_×</sup><sup>_z_matrixandthematrix</sup> **MSM**<sup>_T_</sup> has the rank of _R_ ≤ _K_ . The conventional DLPP is equivalent to the eigenvalue decomposition of the matrix _(_ **MSM**<sup>_T_</sup> _)_<sup>−1</sup> _(_ **_X_ SAE** **_U X_ SAE**<sup>_T)_.Inthisarticle,SVD</sup> is used to decompose the eigenvalues of the matrix _(_ **MSM**<sup>_T_</sup> _)_<sup>−1</sup> _(_ **_X_ SAE** **_U X_ SAE**<sup>_T)_tosolvetheproblemofeigen-</sup> value decomposition due to the dissatisfaction rank of the matrix **MSM**<sup>_T_</sup> . Moreover, the eigenvalues obtained by SVD have good representativeness and finally the corresponding eigenvectors can be obtained according to the magnitude of the eigenvalues. In the end, the projection matrix **_V_** = { **_v_** 1 _,_ **_v_** 2 _, . . . ,_ **_v_** _a_ } is obtained. The final DR data obtained by DLPP is shown in (16); the final data after DR is represented as **_X_** new 


![](Fault_Diagnosis_Using_Improved_Discrimination_Locality_Preserving_Projections_Integrated_with_Sparse_Autoencoder_images/conv_8e287e9d8b601f28.pdf-0004-11.png)


## _C. Akaike Information Criterion_ 

Similarly, the molecule of (7) can be transformed to the following equation: 

The DR order is an important parameter. The fault diagnosis performance is related to the DR order. The AIC is used to find the optimal DR order. The expression of AIC is listed in the following equation: 


![](Fault_Diagnosis_Using_Improved_Discrimination_Locality_Preserving_Projections_Integrated_with_Sparse_Autoencoder_images/conv_8e287e9d8b601f28.pdf-0004-15.png)


where _f (a)_ is the model prediction error term representing the misspecification rate of the training data for the first _a_ vectors obtained by projecting the data; _n_ is the average of the various types of observations. The training set misclassification rate _f (a)_ also reflects the amount of useful information about the classification of the first _a_ vectors obtained by DR. Obviously, the misclassification rate decreases as _a_ increases; however, for the test data, the misclassification rate first decreases and increases later. Thus, the model complexity term can effectively suppress the dimensionality increase. 

where **_Q_ k** means the similarity weight matrix of the _k_ th class, **_T_** represents the weight relationship between the mean vector of samples. **_D_ k** and **_F_** are diagonal arrays; **_M_** can be represented as **_M_** = [ **_m_** 1 _,_ **_m_** 2 _, . . . ,_ **_m_** _K_ ] ∈ **_R_**<sup>_z_×</sup><sup>_k_</sup> ; the corresponding equation takes the form as follows: 

## _D. Fault Diagnosis Using AdaBoost_ 

After DR of data, the AdaBoost classifier is adopted to identify the fault type for developing fault diagnosis. The decision tree classifier is used as the weak classifier in AdaBoost. The detailed steps of the AdaBoost algorithm are listed as follows. 


![](Fault_Diagnosis_Using_Improved_Discrimination_Locality_Preserving_Projections_Integrated_with_Sparse_Autoencoder_images/conv_8e287e9d8b601f28.pdf-0004-20.png)


1) Determine the training data 


![](Fault_Diagnosis_Using_Improved_Discrimination_Locality_Preserving_Projections_Integrated_with_Sparse_Autoencoder_images/conv_8e287e9d8b601f28.pdf-0004-22.png)


Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on September 11,2026 at 16:23:57 UTC from IEEE Xplore.  Restrictions apply. 

3527108 

HE _et al._ : FAULT DIAGNOSIS USING IMPROVED SAEDLPP 

where **_x_** new _i_ is the data obtained by (16) after DR by SAE and DLPP and **_y_** _i_ ∈ **_Y_** is the category label. 2) Initialize weights 


![](Fault_Diagnosis_Using_Improved_Discrimination_Locality_Preserving_Projections_Integrated_with_Sparse_Autoencoder_images/conv_8e287e9d8b601f28.pdf-0005-03.png)


- 3) Suppose the number of iterations is _t_ = 1 _,_ 2 _, . . . , T_ and each learning yields a basic classifier. Repeat the following operation _T_ times. 

- 4) The basic classifier _Gt (x)_ is learned using the training dataset with the current distribution _Dt_ . 

- 5) Obtain the classification error rate _et_ . **_x_** new _i_ of the basic classifier _Gt (x)_ on the training data represents the _i_ th class of training data 


![](Fault_Diagnosis_Using_Improved_Discrimination_Locality_Preserving_Projections_Integrated_with_Sparse_Autoencoder_images/conv_8e287e9d8b601f28.pdf-0005-07.png)


a) Calculate the coefficient of _Gt (x)_ 


![](Fault_Diagnosis_Using_Improved_Discrimination_Locality_Preserving_Projections_Integrated_with_Sparse_Autoencoder_images/conv_8e287e9d8b601f28.pdf-0005-09.png)


- b) Update the training data weight distribution in preparation for the next iteration. 


![](Fault_Diagnosis_Using_Improved_Discrimination_Locality_Preserving_Projections_Integrated_with_Sparse_Autoencoder_images/conv_8e287e9d8b601f28.pdf-0005-11.png)


where _Z t_ is the normalization factor. 

6) Linearly combine the basic classifiers 


![](Fault_Diagnosis_Using_Improved_Discrimination_Locality_Preserving_Projections_Integrated_with_Sparse_Autoencoder_images/conv_8e287e9d8b601f28.pdf-0005-14.png)



![](Fault_Diagnosis_Using_Improved_Discrimination_Locality_Preserving_Projections_Integrated_with_Sparse_Autoencoder_images/conv_8e287e9d8b601f28.pdf-0005-15.png)


Fig. 2. Flowchart of TEP. 

TABLE I 

FAULT TYPES OF THE SELECTED SIX FAULTS 


![](Fault_Diagnosis_Using_Improved_Discrimination_Locality_Preserving_Projections_Integrated_with_Sparse_Autoencoder_images/conv_8e287e9d8b601f28.pdf-0005-19.png)


variables and 11 control variables [28]. There are 21 fault types in TEP; the first 16 of these faults are known faults and the last 5 are unknown faults. The sampling time is 3 min in our study. In simulations, 480 training samples and 800 testing samples are generated, respectively. 

## _B. Multifault Case_ 

To verify the superior performance of SAEDLPP-based fault diagnosis, six faults including fault 4, fault 5, fault 7, fault 10, fault 12, and fault 14 are selected as a set of experimental data. The fault types of the selected six faults are shown in Table I. The simulation results are compared with PCA, LPP, and DLPP. 

7) Finally, the strong classifier is obtained 


![](Fault_Diagnosis_Using_Improved_Discrimination_Locality_Preserving_Projections_Integrated_with_Sparse_Autoencoder_images/conv_8e287e9d8b601f28.pdf-0005-24.png)


## IV. CASE STUDIES 

The performance of SAEDLPP-based fault diagnosis is verified by comparing SAEDLPP-based fault diagnosis with other methods through simulation applications to TEP. 

## _A. Tennessee Eastman Process_ 

The TEP flowchart is shown in Fig. 2. TEP [28] is a realistic simulation platform developed by the Eastman Chemical Company based on actual chemical reaction processes. The data generated from TEP are nonlinear, dynamic, and strongly coupled. TEP can be divided into five parts: a condenser, a reactor, a gas-liquid separator, a compressor, and a stripper. Fifty-two variables are included in TEP, including 41 measured 

## _C. Simulation Results and Analysis_ 

Each fault data contain 480 training data and 800 testing data. Determining the DR order is one of the important steps in the experiment. Different dimension orders have different impacts on the final classification results. To determine the DR order, the AIC information criterion is adopted. As shown in Fig. 3, the blue “+” represents the optimal DR order of SAEDLPP found by AIC. As shown in Fig. 3, the optimal DR order is 18 for SAEDLPP, where the algorithm achieves the lowest misclassification rate. In the same way, the optimal DR order of PCA, LPP, and DLPP can be also determined. In Fig. 4, based on the AdaBoost classifier, the accuracy rates of the four methods on the training data are clearly shown. It can be seen that the accuracy rate of the SAEDLPP algorithm proposed in this article is much higher than the other three methods. 

In Fig. 3, it can be noticed that the DR order of SAEDLPP is determined as 18 according to the AIC information criterion; 

Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on September 11,2026 at 16:23:57 UTC from IEEE Xplore.  Restrictions apply. 

3527108 

IEEE TRANSACTIONS ON INSTRUMENTATION AND MEASUREMENT, VOL. 70, 2021 


![](Fault_Diagnosis_Using_Improved_Discrimination_Locality_Preserving_Projections_Integrated_with_Sparse_Autoencoder_images/conv_8e287e9d8b601f28.pdf-0006-02.png)


Fig. 3. Misclassification rate of different methods with different orders of reduced dimension. 


![](Fault_Diagnosis_Using_Improved_Discrimination_Locality_Preserving_Projections_Integrated_with_Sparse_Autoencoder_images/conv_8e287e9d8b601f28.pdf-0006-04.png)


Fig. 4. Accuracy of four different methods on training data. 

TABLE II 

COMPARISON RESULTS WITH FOUR DIFFERENT METHODS 


![](Fault_Diagnosis_Using_Improved_Discrimination_Locality_Preserving_Projections_Integrated_with_Sparse_Autoencoder_images/conv_8e287e9d8b601f28.pdf-0006-08.png)



![](Fault_Diagnosis_Using_Improved_Discrimination_Locality_Preserving_Projections_Integrated_with_Sparse_Autoencoder_images/conv_8e287e9d8b601f28.pdf-0006-09.png)


it can be seen that the maximum DR order of DLPP is not more than the number of fault classes _c_ due to the problem of matrix decomposition. The DR order of DLPP is determined as four in this article. The diagnosis results of the four fault diagnosis models on the testing data are listed in Table II. As shown in Table II, the average accuracy of the SAEDLPP algorithm proposed in this article is much higher than those of the other three algorithms of PCA, LPP, and DLPP. In the testing dataset, the average accuracy of PCA, LPP, and DLPP are 56.56%, 76.73%, and 68.62%, respectively; while the average accuracy of the SAEDLPP algorithm proposed in this article reaches 87.71%; especially for fault 12, the accuracy of the presented SAEDLPP 


![](Fault_Diagnosis_Using_Improved_Discrimination_Locality_Preserving_Projections_Integrated_with_Sparse_Autoencoder_images/conv_8e287e9d8b601f28.pdf-0006-11.png)


Fig. 5. Results of the fault diagnosis performed on the test data using four methods. 

algorithm is significantly improved compared with the other three algorithms and the diagnosis rate of fault 7 by SAEDLPP reaches 100%, indicating that the proposed SAEDLPPbased fault diagnosis can achieve acceptable diagnosis accuracy. 

Fig. 5 shows the diagnosis rate of each type of fault. The right side of Fig. 5 shows the corresponding color when each type of fault is correctly diagnosed; thus, the more consistent the color of each type of fault, the higher the diagnosis rate of the corresponding fault. It can be clearly seen from Fig. 5, the proposed SAEDLPP obtains more consistent colors than other methods, which also indicates that SAEDLPP achieves better fault diagnosis accuracy than the other three methods. 

## _D. Visualization Analysis_ 

The first three dimensions of the extracted features from the four algorithms of PCA, LPP, DLPP, and SAEDLPP after DR are demonstrated. The visualization results of the first three dimensions of the extracted features from the four algorithms of PCA, LPP, DLPP, and SAEDLPP on the testing dataset are shown in Fig. 6. Fig. 6 shows the visualization results of the testing dataset of the six faults of fault 4, fault 5, fault 7, fault 10, fault 12, and fault 14. From Fig. 6, the extracted features of the SAEDLPP algorithm presented in this article can be well discriminated from the six faults when mapping the high-dimensional data to the 3-D space and so SAEDLPP-based fault diagnosis can obviously achieve higher 

Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on September 11,2026 at 16:23:57 UTC from IEEE Xplore.  Restrictions apply. 

3527108 

HE _et al._ : FAULT DIAGNOSIS USING IMPROVED SAEDLPP 


![](Fault_Diagnosis_Using_Improved_Discrimination_Locality_Preserving_Projections_Integrated_with_Sparse_Autoencoder_images/conv_8e287e9d8b601f28.pdf-0007-02.png)


Fig. 6. Visualization of the first three extracted features using four methods. 

classification accuracy than the other three algorithms of PCA, LPP, and DLPP. Through visualization, it can be proved that the presented SAEDLPP-based fault diagnosis can achieve higher classification accuracy than PCA, LPP, and DLPP. 

## V. CONCLUSION 

In order to effectively enhance the performance of fault diagnosis in industrial processes, this article proposes a fault diagnosis methodology based on SAEDLPP. First, SAE is used to extract features from the original data, and then the newly obtained data after feature extraction are used to obtain the projection matrix through the manifold learning algorithm of DLPP, which can realize the DR of high-dimensional data by reasonably combining the advantages of two feature extraction methods; in order to solve the matrix decomposition problem in SAEDLPP, SVD is used; finally, an AdaBoost classifier is used to classify the data after DR to obtain fault types. To verify and confirm the superior effectiveness of SAEDLPP, different types of faults in TEP are used for experiments. Simulation results show that the presented SAEDLPP can achieve better feature extraction capability and much higher fault diagnosis accuracy compared with PCA, LPP, and DLPP. 

## REFERENCES 

- [1] Y. L. He, K. Li, L. L. Liang, Y. Xu, and Q. X. Zhu, “Novel discriminant locality preserving projection integrated with Monte Carlo sampling for fault diagnosis,” _IEEE Trans. Rel._ , early access, Oct. 27, 2021, doi: 10.1109/TR.2021.3115108. 

- [2] J. Zhang, J. Yu, and D. Tao, “Local deep-feature alignment for unsupervised dimension reduction,” _IEEE Trans. Image Process._ , vol. 27, no. 5, pp. 2420–2432, May 2018. 

- [3] G. Yang and X. Gu, “Fault diagnosis of complex chemical processes based on enhanced naive Bayesian method,” _IEEE Trans. Instrum. Meas._ , vol. 69, no. 7, pp. 4649–4658, Jul. 2020. 

- [4] G. Yang, Y. Zhao, and X. Gu, “A novel Bayesian framework with enhanced principal component analysis for chemical fault diagnosis,” _IEEE Trans. Instrum. Meas._ , vol. 70, pp. 1–9, 2021. 

- [5] Z. L. Liu, J. Qu, M. J. Zuo, and H.-B. Xu, “Fault level diagnosis for planetary gearboxes using hybrid kernel feature selection and kernel Fisher discriminant analysis,” _Int. J. Adv. Manuf. Technol._ , vol. 67, nos. 5–8, pp. 1217–1230, 2013. 

- [6] S. Yin, X. Zhu, and O. Kaynak, “Improved PLS focused on keyperformance-indicator-related fault diagnosis,” _IEEE Trans. Ind. Electron._ , vol. 62, no. 3, pp. 1651–1658, Mar. 2015. 

- [7] P. Akhlaghi, A. R. Kashanipour, and K. Salahshoor, “Decentralized fault diagnosis system using ICA in a complex chemical process,” in _Proc. 10th Int. Conf. Control, Automat., Robot. Vis._ , Dec. 2008, pp. 1194–1199. 

- [8] W. H. Li, H. H. Yue, S. V. Cervantes, and S. J. Qin, “Recursive PCA for adaptive process monitoring,” _J. Process Control_ , vol. 10, no. 5, pp. 471–486, 2000. 

- [9] K. Zhong, M. Han, T. Qiu, and B. Han, “Fault diagnosis of complex processes using sparse kernel local Fisher discriminant analysis,” _IEEE Trans. Neural Netw. Learn. Syst._ , vol. 31, no. 5, pp. 1581–1591, May 2020. 

- [10] Q. Yang, F. Tian, and D. Wang, “Nonlinear dynamic process monitoring based on lifting wavelets and dynamic kernel PCA,” in _Proc. 8th World Congr. Intell. Control Automat._ , Jul. 2010, pp. 5712–5716. 

- [11] M. M. Rashid and J. Yu, “A new dissimilarity method integrating multidimensional mutual information and independent component analysis for non-Gaussian dynamic process monitoring,” _Chemometrics Intell. Lab. Syst._ , vol. 115, pp. 44–58, Jun. 2012. 

- [12] Y. Liu, Y. Chang, and F. Wang, “Nonlinear dynamic quality-related process monitoring based on dynamic total kernel PLS,” in _Proc. 11th World Congr. Intell. Control Automat._ , Jun. 2014, pp. 1360–1365. 

- [13] J. Gao, F. Li, B. Wang, and H. Liang, “Unsupervised nonlinear adaptive manifold learning for global and local information,” _Tsinghua Sci. Technol._ , vol. 26, no. 2, pp. 163–171, Apr. 2021. 

- [14] B. Du, L. Zhang, L. Zhang, T. Chen, and K. Wu, “A discriminative manifold learning based dimension reduction method for hyperspectral classification,” _Int. J. Fuzzy Syst._ , vol. 14, no. 2, pp. 272–277, 2012. 

- [15] H. Qu and J. Cheng, “Human action recognition based on adaptive distance generalization of isometric mapping,” in _Proc. 5th Int. Congr. Image Signal Process._ , Oct. 2012, pp. 95–98. 

- [16] Y. Zhang, Y. Fu, Z. Wang, and L. Feng, “Fault detection based on modified kernel semi-supervised locally linear embedding,” _IEEE Access_ , vol. 6, pp. 479–487, 2018. 

- [17] Y. Jin and Q.-Q. Ruan, “An image matrix compression based supervised locality preserving projections for face recognition,” in _Proc. Int. Symp. Intell. Signal Process. Commun. Syst._ , 2007, pp. 738–741. 

- [18] W. Yu, X. Teng, and C. Liu, “Face recognition using discriminant locality preserving projections,” _Image Vis. Comput._ , vol. 24, no. 3, pp. 239–248, Mar. 2006. 

- [19] Y.-L. He, X. Yan, and Q.-X. Zhu, “Novel pattern recognition using bootstrap-based discriminant locality-preserving projection and its application to fault diagnosis,” _Ind. Eng. Chem. Res._ , vol. 58, no. 38, pp. 17906–17917, Sep. 2019. 

- [20] X. He, S. Yan, Y. Hu, P. Niyogi, and H.-J. Zhang, “Face recognition using Laplacianfaces,” _IEEE Trans. Pattern Anal. Mach. Intell._ , vol. 27, no. 3, pp. 328–340, Mar. 2005. 

- [21] S. Kido, Y. Hirano, and N. Hashimoto, “Detection and classification of lung abnormalities by use of convolutional neural network (CNN) and regions with CNN features (R-CNN),” in _Proc. Int. Workshop Adv. Image Technol. (IWAIT)_ , Jan. 2018, pp. 1–4. 

- [22] S. Zhang, M. Wang, F. Yang, and W. Li, “Manifold sparse autoencoder for machine fault diagnosis,” _IEEE Sensors J._ , vol. 20, no. 15, pp. 8328–8335, Aug. 2020. 

- [23] S. Patra and L. Bruzzone, “A novel SOM-SVM-based active learning technique for remote sensing image classification,” _IEEE Trans. Geosci. Remote Sens._ , vol. 52, no. 11, pp. 6899–6910, Nov. 2014. 

- [24] Z. A. Khan, S. Zubair, K. Imran, R. Ahmad, S. A. Butt, and N. I. Chaudhary, “A new users rating-trend based collaborative denoising auto-encoder for top-N recommender systems,” _IEEE Access_ , vol. 7, pp. 141287–141310, 2019. 

- [25] Y. Wang, H. Yang, X. Yuan, Y. A. W. Shardt, C. Yang, and W. Gui, “Deep learning for fault-relevant feature extraction and fault classification with stacked supervised auto-encoder,” _J. Process Control_ , vol. 92, pp. 79–89, Aug. 2020. 

- [26] W. Wang, Y. Huang, Y. Wang, and L. Wang, “Generalized autoencoder: A neural network framework for dimensionality reduction,” in _Proc. IEEE Conf. Comput. Vis. Pattern Recognit. Workshops_ , Jun. 2014, pp. 496–503. 

- [27] Y.-L. He, Y. Zhao, X. Hu, X.-N. Yan, Q.-X. Zhu, and Y. Xu, “Fault diagnosis using novel AdaBoost based discriminant locality preserving projection with resamples,” _Eng. Appl. Artif. Intell._ , vol. 91, pp. 103631.1–103631.11, May 2020. 

- [28] Y. Wang, D. Wu, and X. Yuan, “LDA-based deep transfer learning for fault diagnosis in industrial chemical processes,” _Comput. Chem. Eng._ , vol. 140, Sep. 2020, Art. no. 106964. 

Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on September 11,2026 at 16:23:57 UTC from IEEE Xplore.  Restrictions apply. 

3527108 

IEEE TRANSACTIONS ON INSTRUMENTATION AND MEASUREMENT, VOL. 70, 2021 


![](Fault_Diagnosis_Using_Improved_Discrimination_Locality_Preserving_Projections_Integrated_with_Sparse_Autoencoder_images/conv_8e287e9d8b601f28.pdf-0008-02.png)



![](Fault_Diagnosis_Using_Improved_Discrimination_Locality_Preserving_Projections_Integrated_with_Sparse_Autoencoder_images/conv_8e287e9d8b601f28.pdf-0008-03.png)



![](Fault_Diagnosis_Using_Improved_Discrimination_Locality_Preserving_Projections_Integrated_with_Sparse_Autoencoder_images/conv_8e287e9d8b601f28.pdf-0008-04.png)


**Yan-Lin He** (Member, IEEE) received the B.Sc. and Ph.D. degrees from the College of Information Science and Technology (CIST), Beijing University of Chemical Technology (BUCT), Beijing, China, in 2011 and 2016, respectively. 

He is currently a Professor with CIST, BUCT. His research interests include computational intelligence, artificial intelligence, machine learning, data mining, fault diagnosis, and process modeling. 

**Kun Li** received the bachelor’s degree in engineering from the Mechanical College of Jinzhong University, Jinzhong, China, in 2016. He is currently pursuing the master’s degree with the College of Information Science and Technology (CIST), Beijing University of Chemical Technology (BUCT), Beijing, China. 

His research interests include computational intelligence, machine learning, data mining, and fault diagnosis. 

**Ning Zhang** is currently pursuing the master’s degree with the College of Information Science and Technology, Beijing University of Chemical Technology, Beijing, China. His major is control science and engineering. 

His research interests are fault diagnosis, small sample size modeling, and machine learning. 


![](Fault_Diagnosis_Using_Improved_Discrimination_Locality_Preserving_Projections_Integrated_with_Sparse_Autoencoder_images/conv_8e287e9d8b601f28.pdf-0008-11.png)



![](Fault_Diagnosis_Using_Improved_Discrimination_Locality_Preserving_Projections_Integrated_with_Sparse_Autoencoder_images/conv_8e287e9d8b601f28.pdf-0008-12.png)


**Yuan Xu** received the B.Sc. and Ph.D. degrees from the College of Information Science and Technology (CIST), Beijing University of Chemical Technology (BUCT), Beijing, China, in 2005 and 2010, respectively. 

She is currently a Professor with CIST, BUCT. Her research interests include computational intelligence, fault diagnosis, data mining, and process modeling. 

**Qun-Xiong Zhu** received the Ph.D. degree from the College of Information Science and Technology (CIST), Beijing University of Chemical Technology (BUCT), Beijing, China, in 1996. 

He is currently a Professor with CIST, BUCT. His research interests include computational intelligence, artificial intelligence, machine learning, data mining, fault diagnosis, and process modeling. 

Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on September 11,2026 at 16:23:57 UTC from IEEE Xplore.  Restrictions apply. 

