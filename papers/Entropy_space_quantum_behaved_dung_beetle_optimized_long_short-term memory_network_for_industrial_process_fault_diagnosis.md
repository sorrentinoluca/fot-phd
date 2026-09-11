ISA Transactions 176 (2026) 210–223 


![](Entropy_space_quantum_behaved_dung_beetle_optimized_long_short-term memory_network_for_industrial_process_fault_diagnosis_images/conv_84a6d24ab661c870.pdf-0001-01.png)


Contents lists available at ScienceDirect 

# ISA Transactions 

journal homepage: www.elsevier.com/locate/isatrans 


![](Entropy_space_quantum_behaved_dung_beetle_optimized_long_short-term memory_network_for_industrial_process_fault_diagnosis_images/conv_84a6d24ab661c870.pdf-0001-05.png)


### Research article 

Entropy space quantum behaved dung beetle optimized long short-term memory network for industrial process fault diagnosis 


![](Entropy_space_quantum_behaved_dung_beetle_optimized_long_short-term memory_network_for_industrial_process_fault_diagnosis_images/conv_84a6d24ab661c870.pdf-0001-08.png)


## Shuai Ao<sup>a,d</sup> , Bo Ma<sup>a</sup> , Haorui Liu<sup>b,c,*</sup> , Tao Li<sup>b,c,*</sup> , Yongming Han<sup>b,c,*</sup> 


![](Entropy_space_quantum_behaved_dung_beetle_optimized_long_short-term memory_network_for_industrial_process_fault_diagnosis_images/conv_84a6d24ab661c870.pdf-0001-10.png)


a _College of Mechanical and Electrical Engineering, Beijing University of Chemical Technology, Beijing 100029, China_ 

b _College of Information Science and Technology, Beijing University of Chemical Technology, Beijing 100029, China_ 

c _Engineering Research Center of Intelligent PSE, Ministry of Education of China, Beijing 100029, China_ 

d _Mechanical and Electrical Management Department, National Energy Group Guoshen Company Sandaogou Coal Mine, Yulin, Shanxi 719407, China_ 

A R T I C L E I N F O A B S T R A C T _Keywords:_ To address the challenges posed by the high dimensionality and strong nonlinearity of complex industrial process Entropy Space data, as well as the inherent defects in feature learning and hyperparameter dependency of the traditional long Quantum Behavior short-term memory network (LSTM), this paper proposes a novel hierarchical fault diagnosis method termed Dung Beetle Optimization Algorithm entropy space quantum behaved dung beetle optimized LSTM (ES-QLSTM). The proposed method employs Long Short-Term MemoryFault Diagnosis kernel entropy component analysis (KECA) to extract features from raw data in the entropy space (ES). Benefiting Complex Industrial Processes from the strong nonlinear mapping capability and high-order information retention property of the KECA, the proposed method effectively preserves critical high-order statistical information that cannot be captured by conventional methods, which compensates for the insufficient feature mining ability of the LSTM. Then, this proposed method integrates entropy space feature extraction with a quantum behaved mechanism into the dung beetle optimization algorithm, constructing a systematic synergistic framework for entropy space feature dimensionality reduction and intelligent hyperparameter optimization. This framework solves two key shortcomings of the LSTM simultaneously, weak feature extraction from high-dimensional nonlinear data and unstable performance caused by empirical hyperparameter settings. Subsequently, a quantum behaved mechanism is incorporated into the dung beetle optimization (DBO) algorithm, resulting in the quantum behaved dung beetle optimization (QDBO) algorithm, which is utilized to optimize the key hyperparameters of the LSTM network. The ultimately constructed ES-QLSTM method enhances diagnostic performance through the synergistic integration of entropy-space feature purification and intelligent hyperparameter optimization. Experimental validation on the Tennessee Eastman Process (TEP) and grid-connected photovoltaic system (GPVS) datasets demonstrates that the proposed method outperforms traditional models and improved models in diagnosing complex faults, with the average diagnostic accuracy reaching 93.70% and 83.91% on the two datasets, respectively. 

#### **1. Introduction** 

The reliable and safe operation of modern industrial systems is largely contingent upon the efficacy of fault diagnosis technologies [1]. With the in-depth advancement of Industry 4.0 and smart manufacturing, the volume of data generated in industrial production processes has experienced explosive growth, which is typically featured by complex attributes such as high dimensionality, nonlinearity, and 

dynamic coupling [2]. Conventional fault diagnosis approaches are highly dependent on the establishment of accurate mechanistic models, yet their inadequate adaptive capacity makes it hard to capture fault-related features accurately when confronted with the complex data, thus restricting their diagnostic performance [3]. To address these issues, this paper integrates entropy space feature reduction and quantum behaved optimization, aiming to provide a reliable solution for real-time industrial fault diagnosis. 

* Corresponding authors at: College of Information Science and Technology, Beijing University of Chemical Technology, Beijing 100029, China. 

_E-mail addresses:_ 2025400243@buct.edu.cn (S. Ao), mabo@mail.buct.edu.cn (B. Ma), 2024200786@buct.edu.cn (H. Liu), 2022400226@buct.edu.cn (T. Li), hanym@mail.buct.edu.cn (Y. Han). 

https://doi.org/10.1016/j.isatra.2026.05.037 

Received 16 January 2026; Received in revised form 26 May 2026; Accepted 26 May 2026 

Available online 11 June 2026 

0019-0578/© 2026 International Society of Automation. Published by Elsevier Ltd. All rights are reserved, including those for text and data mining, AI training, and similar technologies. 

> _S. Ao et al.                                                                                                                                                                                                                                       ISA Transactions 176 (2026) 210–223_ 

Given the prevalent nonlinearity of the industrial data, traditional linear dimensionality reduction methods were inadequate in fully revealing the inherent correlations within the data. Scholkopf et al. ¨ [4] proposed the kernel PCA (KPCA) for mapping the data to a high-dimensional feature space through a nonlinear transformation and then performed linear dimensionality reduction in this space, which effectively overcame the modeling constraints of linear methods and enhanced the adaptability of feature extraction to nonlinear data. Fezai et al. [5] further proposed an online KPCA algorithm that simplified kernel matrix computations to enable real-time monitoring, thereby resolving the problem that the traditional KPCA was not suitable for industrial online application scenarios. Although the KPCA outperformed the PCA in nonlinear modeling, its principal component selection mechanism relied solely on eigenvalue magnitude. This often led to the neglect of higher-order statistical features, resulting in the loss of critical fault information. To mitigate this limitation, Jenssen [6] pioneered the kernel entropy component analysis (KECA) framework, which employed R´enyi entropy as the metric for feature selection, which overcame the over-reliance of the KPCA on eigenvalues and ensured the preservation of higher-order information in the data. Li et al. [7] combined the KECA with a moving window to achieved adaptive fault detection during dynamic processes. Despite these improvements, the potential of entropy-space features to guide the hyperparameter search landscape of downstream classifiers remains under-explored. 

In the construction of fault classification models, long short-term memory (LSTM) networks leverage their unique gating mechanisms to effectively capture long-term dependencies in time-series data and mitigate the vanishing gradient problem inherent in traditional recurrent neural networks [8]. Consequently, the LSTM is widely applied for fault pattern learning in dynamic industrial data [9]. The LSTM is adopted for its unique gating mechanism that captures long-term temporal dependencies and mitigates gradient vanishing, outperforming traditional methods in handling dynamic industrial time-series data. However, the LSTM performance is highly dependent on hyperparameter tuning, such as learning rate, number of hidden layer neurons, and L2 regularization coefficient. Traditional manual tuning or grid search methods are prone to getting stuck in local optima due to limited search ranges, resulting in insufficient model generalization capabilities [10]. Therefore, Liu et al. [11] employed a particle swarm optimization (PSO) algorithm to optimize the LSTM network and combined it with an attention mechanism to enhance the accuracy of new energy cable fault prediction. Gao et al. [12] employed an improved beluga whale optimization algorithm to optimize the LSTM, enhancing the balance factor through nonlinear functions for ship diesel engine piston ring fault diagnosis. Wang et al. [13] utilized an improved sparrow search algorithm to optimize the LSTM, incorporating Tent chaotic mapping and dynamic stride to improve the accuracy and stability of fault data recovery for dry-type transformer temperature sensors. Yousaf et al. [14] employed Bayesian optimization to tune LSTM hyperparameters, combined with a discrete wavelet transform for feature extraction, further improving fault recognition accuracy. Y et al. [15] proposed a multi-information fusion method based on attention collaborative stacked LSTM and quantum particle swarm optimization algorithms to address the challenge of extracting fault features from neutral-point-clamped three-level inverters under non-stationary conditions. Zeng et al. [16] proposed the dual attention LSTM integrating the autoencoder encoding-decoding architecture and dual attention modules to achieve efficient learning of dynamic features and key information in long-term industrial process data. Wang et al. [17,18] proposed an innovative filtering method for lithium-ion battery state of power evaluation and an improved parameter identification strategy for state-of-charge estimation of lithium-ion batteries in electric vehicles, and the full-parameter online identification logic included therein had further promoted the research on mathematical analysis and parameter optimization. To further balance the global exploration and local exploitation capabilities of optimization algorithms, Xue et al. [19] 

inspired by the natural behaviors of dung beetles, such as ball rolling, dancing, reproduction and stealing, proposed the dung beetle optimization (DBO) algorithm, which combined the differential evolution mechanism with the collaboration strategy of the biological group, and exhibited a good diversity preservation and convergence performance in multimodal function optimization. However, in the hyperparameter search scenario of industrial fault diagnosis models, the classical DBO suffers from the problems of easy to fall into local extremes in the later iterations and insufficient adaptability to the complex search space [20] To address the issue of population diversity degradation in traditional swarm intelligence algorithms, Wang et al. [21] proposed an adaptive small-family population-guided swarm intelligence optimization algorithm, which dynamically adjusted the population structure and introduces family-based guidance strategies to enhance global search capability and convergence accuracy. Meanwhile, the quantum computing technology shows potential in breaking through the performance bottleneck of traditional optimization algorithms due to its parallel search and quantum tunneling characteristics. Agrawal et al. proposed the quantum adaptive mutation operator PSO, which extended the search region by combining quantum bit dynamics and adaptive mutation, and performed well on the IEEE-CEC− 2022 benchmark problem [22]. 

In summary, while existing research has made progress in feature extraction and model optimization for industrial fault diagnosis, the nonlinear and redundant nature of high-dimensional industrial data often leads to insufficient feature learning of the LSTM. Meanwhile, hyperparameter optimization algorithms for fault classification models are prone to unstable convergence, failing to provide optimal parameter configurations and thereby compromising diagnostic performance. Therefore, identifying that existing research lacks a unified framework that balances high-order information preservation with quantumprobabilistic global exploration, this paper proposes a novel systematic fault diagnosis paradigm named entropy space quantum behaved dung beetle optimized LSTM (ES-QLSTM), which is a theoretically grounded framework designed to overcome the inherent weaknesses of the LSTM. The proposed method first employs KECA to extract primary features from industrial process data within an entropy space, retaining high-order information and providing high-quality inputs to make up for the lack of nonlinear feature learning in the LSTM. Then, a quantum behavior mechanism is introduced into the traditional dung beetle optimization algorithm, resulting in the QDBO algorithm, which optimizes the key hyperparameters of the LSTM to eliminate performance fluctuations caused by manual parameter tuning. Finally, the ES-QLSTM method synergistically enhances the fault diagnosis performance of industrial processes by deeply integrating entropy space feature extraction with quantum behavior optimization mechanisms, achieving efficient and stable fault diagnosis. The primary contributions of the paper are elaborated in detail as follows. 

1) A novel entropy space feature extraction strategy based on the KECA is proposed by taking R´enyi entropy as the core evaluation metric. While eliminating redundant and irrelevant variables to reduce data complexity, it effectively preserves the key information entropy features closely related to industrial fault patterns, laying a solid foundation for accurate fault identification. 

2) An improved QDBO algorithm is developed by integrating a quantum behavior mechanism into the original DBO algorithm. The introduced quantum behavior enables particles to achieve quantum hopping in the search space, significantly expanding the exploration range and avoiding the defect of traditional DBO algorithms that are prone to falling into local optima. This improvement enhances the efficiency and accuracy of the algorithm search, which has been verified on multiple benchmark functions. 

3) Corresponding experimental validations are conducted on two representative industrial datasets including Tennessee Eastman Process (TEP) and grid-connected photovoltaic system (GPVS). The results demonstrate that the proposed ES-QLSTM model outperforms existing 

211 

> _S. Ao et al.                                                                                                                                                                                                                                       ISA Transactions 176 (2026) 210–223_ 

##### **Table 1** 

Performance comparison of the proposed model using different kernel functions. 

|**Kernel Function**|**TEP Accuracy (%)**|**GPVS Accuracy (%)**|
|---|---|---|
|Gaussian|93.70|83.91|
|Polynomial|78.42|69.35|
|Sigmoid|75.18|65.72|



methods in fault identification accuracy, verifying its promising application prospects in practical industrial fault diagnosis. 

The structure of the rest of this article is organized as follows. Section II describes the overall framework and implementation details of the ESQLSTM fault diagnosis methodology. Section III conducts a comparative analysis of multiple optimization algorithms using four benchmark functions. Section IV demonstrates the experimental results and analyses on the TEP and GPVS datasets. and Section V summarizes the findings of this article and looks forward to the future research directions. 

#### **2. The proposed method** 

This segment offers a detailed elaboration on two core components. One is the fault diagnosis based on entropy space feature extraction, and the other is the QDBO Algorithm. Following this, we lay out the full operational workflow of the fault diagnosis scheme that relies on the ESQLSTM architecture. 

#### _2.1. Fault diagnosis based on entropy space feature extraction_ 

As a nonlinear data processing method, KECA achieves transformation and dimensionality reduction by projecting data into the kernel feature space and then onto the KPCA principal axes. 

We define _X_ : ( _x_ 1 _, x_ 2 _, …, xn_ ) as an _d_ × _n_ matrix, with _n_ representing the sample size and _d_ indicating the dimension of damage features. For probability density distribution _g_ ( _x_ ), the corresponding R´enyi entropy is governed by the equation: 


![](Entropy_space_quantum_behaved_dung_beetle_optimized_long_short-term memory_network_for_industrial_process_fault_diagnosis_images/conv_84a6d24ab661c870.pdf-0003-11.png)


This form corresponds to the quadratic R´enyi entropy, which is widely adopted in industrial fault diagnosis due to its high sensitivity to subtle changes in fault-related features. Unlike traditional variancebased metrics, quadratic R´enyi entropy quantifies the information richness of high-dimensional nonlinear data by integrating the squared probability density, making it more capable of capturing weak coupling fault information that is easily lost in conventional dimensionality reduction. 

Due to the monotonicity of the logarithmic function, the calculation of R´ enyi entropy can be simplified by analyzing. This formula can alternatively be restated as _V_ ( _g_ ) = _εg_ ( _g_ ), where _εg_ (⋅) stands for the expectation operation on the probability density function _g_ ( _x_ ). To accurately estimate _V_ ( _g_ ) and _H_ ( _g_ ) for noisy industrial data, the Parzen window method is utilized, with the probability density estimation formula given by: 


![](Entropy_space_quantum_behaved_dung_beetle_optimized_long_short-term memory_network_for_industrial_process_fault_diagnosis_images/conv_84a6d24ab661c870.pdf-0003-14.png)


Here, _kc_ ( _x, xt_ ) denotes Gaussian kernel function with _c_ as its tuning parameter. The Gaussian kernel is selected for its infinite differentiability and local similarity preservation, which can effectively model the nonlinear relationships between industrial process variables while suppressing sensor noise. To quantitatively justify the selection of the Gaussian kernel, we evaluated the diagnostic performance of the ESQLSTM using different kernel functions on both TEP and GPVS datasets. As shown in Table 1, the Gaussian kernel consistently outperforms others. 

An estimate of _V_ ( _g_ ) is then derived by approximating the expectation operator with a sample mean. 


![](Entropy_space_quantum_behaved_dung_beetle_optimized_long_short-term memory_network_for_industrial_process_fault_diagnosis_images/conv_84a6d24ab661c870.pdf-0003-17.png)


This formula reveals the direct link between R´enyi entropy estimation and the kernel matrix _K_ : the double summation term constructs an _n_ × _n_ kernel matrix _K_ , and _V_ ( _g_ ) is proportional to the quadratic form _I_<sup>_T_</sup> _KI_ of the all-ones vector _I_ . This lays the mathematical foundation for the KECA to extract features based on entropy contribution, rather than relying solely on eigenvalue magnitude like the KPCA. 

The elements of the _n_ × _n_ kernel matrix _K_ are _kc_ ( _xt,x_<sup>ʹ</sup> _t_<sup>), where</sup><sup>_I is_an</sup> _n_ × 1 all-ones vector. Therefore, using only the available samples present in the corresponding elements of kernel matrix _K_ , the estimated R´enyi entropy can be evaluated. Furthermore, the estimate of R´enyi entropy can be expressed in terms of the eigenvalues and eigenvectors of the kernel matrix, which can undergo eigenvalue decomposition as shown in Eq. (4). 

Furthermore, the R´enyi entropy estimate can be expressed using the eigenvalues and eigenvectors of the kernel matrix, which undergoes eigenvalue decomposition as shown below: _K_ = _EΛE_<sup>_T_</sup> (4) 


![](Entropy_space_quantum_behaved_dung_beetle_optimized_long_short-term memory_network_for_industrial_process_fault_diagnosis_images/conv_84a6d24ab661c870.pdf-0003-21.png)



![](Entropy_space_quantum_behaved_dung_beetle_optimized_long_short-term memory_network_for_industrial_process_fault_diagnosis_images/conv_84a6d24ab661c870.pdf-0003-22.png)


Although R´enyi entropy estimation depends on both eigenvalues and eigenvectors, a high eigenvalue is not guaranteed to contribute most to information entropy. Consequently, _ψ i_ from Eq. (6) represents the R´enyi entropy of individual elements in Eq. (5), and the values generated by Eq. (6) help to compute R´enyi entropy estimates. 

For the input dataset _X_ : ( _x_ 1 _, x_ 2 _, …, xn_ ), it is first mapped into the kernel feature space via a nonlinear function _ϕ_ (⋅), resulting in the transformed dataset _Φ_ = [ _ϕ_ ( _x_ 1) _, ϕ_ ( _x_ 2) _, …, ϕ_ ( _xn_ )] in the kernel space. The principal axes constructed in KECA — which maximize the retention of ´ Renyi entropy estimates — form a dominant subspace carrying most of the original data information. By projecting _Φ_ onto this dominant subspace _Uk_ , the n-dimensional data is transformed into low-dimensional features, as shown in Eq. (7): 


![](Entropy_space_quantum_behaved_dung_beetle_optimized_long_short-term memory_network_for_industrial_process_fault_diagnosis_images/conv_84a6d24ab661c870.pdf-0003-25.png)


where _Tk_ = [ _t_ 1 _, t_ 2 _, t_ 3 _, …, tk_ ] is the score matrix, _Λk_ = _diag_ ( _λ_ 1 _, λ_ 2 _, λ_ 3 _, …, λk_ ) is the eigenvalue matrix, and _Ek_ = [ _e_ 1 _, e_ 2 _, e_ 3 _, …, ek_ ] is the eigenvector matrix. Through the above steps, the KECA extracts the components contributing most significantly to data entropy within the highdimensional kernel feature space. This achieves nonlinear dimensionality reduction while effectively preserving critical data information, providing low-dimensional, efficient feature inputs for subsequent fault diagnosis model construction. 

Features reduced by the KECA retain significant temporal correlations. LSTM networks, owing to their unique memory cell structure, can simultaneously capture both long-term and short-term dependencies among process variables. This effectively mitigates gradient vanishing and gradient explosion issues, making LSTMs more suitable for diagnosing industrial process failures characterized by strong temporal correlations and dynamic coupling properties. 

The LSTM network requires input data to be in a specific sequence format. Therefore, after completing feature extraction through the 

212 

_ISA Transactions 176 (2026) 210–223_ 

> _S. Ao et al.                                                                                                                                                                                                                                       ISA Transactions_ 


![](Entropy_space_quantum_behaved_dung_beetle_optimized_long_short-term memory_network_for_industrial_process_fault_diagnosis_images/conv_84a6d24ab661c870.pdf-0004-02.png)


**Fig. 1.** Schematic diagram of LSTM. 

KECA, it is necessary to preprocess the low-dimensional feature matrix _Tk_ to adapt to the input requirements of the LSTM. The specific steps are shown as follows: 


![](Entropy_space_quantum_behaved_dung_beetle_optimized_long_short-term memory_network_for_industrial_process_fault_diagnosis_images/conv_84a6d24ab661c870.pdf-0004-05.png)


each column _Ptrain_ (: _, i_ ) ∈ _ℝ_<sup>_t_×1</sup> represents the _t_ -dimensional feature vector of the _i_<sup>th</sup> sample. 

Use min-max normalization to map features to the range 0–1: 


![](Entropy_space_quantum_behaved_dung_beetle_optimized_long_short-term memory_network_for_industrial_process_fault_diagnosis_images/conv_84a6d24ab661c870.pdf-0004-08.png)


Convert the normalized feature matrix into the sequence format of cell arrays required by the LSTM. For each sample _pi_ ∈ _ℝ_<sup>_k_×1</sup> , organize it into a sequence of length _k_ , where the feature dimension at each time step is 1: 


![](Entropy_space_quantum_behaved_dung_beetle_optimized_long_short-term memory_network_for_industrial_process_fault_diagnosis_images/conv_84a6d24ab661c870.pdf-0004-10.png)


Each pi represents a sequence unit: 


![](Entropy_space_quantum_behaved_dung_beetle_optimized_long_short-term memory_network_for_industrial_process_fault_diagnosis_images/conv_84a6d24ab661c870.pdf-0004-12.png)


The _k_ elements in pipi correspond to _k_ time steps. with each time step having a feature dimension of 1. This organization enables the LSTM to capture latent correlations and dependencies among the k reduceddimension features. 

Under this serialization format, the input for the _i-th_ sample at time step _t_ is _x_<sup>(</sup> _t_<sup>_i_), the</sup><sup>_t-th_dimensionality-reduced feature of that sample. The</sup> LSTM processes the sequence step-by-step through the gating mechanisms defined by Eqs. (12)-(17), capturing dependencies among _k_ features. It ultimately outputs the hidden state _Hk_ at the final time step, which serves as the feature representation for that sample in the final _i_ -th classification task. Under this serialization format, the input for the sample at time step _t_ is _x_<sup>(</sup> _t_<sup>_i_), the</sup><sup>_t-th_dimensionality-reduced feature of</sup> 

that sample. The LSTM processes the sequence step-by-step through the gating mechanisms defined by Eqs. (12)-(17), capturing dependencies among _k_ features. It ultimately outputs the hidden state _Hk_ at the final time step, which serves as the feature representation for that sample in the final classification task. As shown in Fig. 1, the LSTM realizes temporal feature modeling through three gating mechanisms: the forget gate, the input gate and the output gate. They control information forgetting, updating and output respectively to mitigate gradient vanishing. The key formulas and parameter explanations are as follows: The forget gate is shown as follows: 


![](Entropy_space_quantum_behaved_dung_beetle_optimized_long_short-term memory_network_for_industrial_process_fault_diagnosis_images/conv_84a6d24ab661c870.pdf-0004-16.png)


where _ft_ is the forget gate output, _S_ (⋅) denotes the sigmoid function, _Uf_ , _Vf_ are coefficient matrices, _δf_ is the bias vector, _Xt_ is the current input, and _Ht_ − 1 is the previous hidden state. A value of 1 means full information retention, while 0 means complete forgetting. 

The input gate is shown as follows: 


![](Entropy_space_quantum_behaved_dung_beetle_optimized_long_short-term memory_network_for_industrial_process_fault_diagnosis_images/conv_84a6d24ab661c870.pdf-0004-19.png)



![](Entropy_space_quantum_behaved_dung_beetle_optimized_long_short-term memory_network_for_industrial_process_fault_diagnosis_images/conv_84a6d24ab661c870.pdf-0004-20.png)


where _it_ is the update coefficient, _Ct_ is the candidate cell state, and tanh (⋅) denotes the hyperbolic tangent function. The output gate is shown as follows: 


![](Entropy_space_quantum_behaved_dung_beetle_optimized_long_short-term memory_network_for_industrial_process_fault_diagnosis_images/conv_84a6d24ab661c870.pdf-0004-22.png)



![](Entropy_space_quantum_behaved_dung_beetle_optimized_long_short-term memory_network_for_industrial_process_fault_diagnosis_images/conv_84a6d24ab661c870.pdf-0004-23.png)



![](Entropy_space_quantum_behaved_dung_beetle_optimized_long_short-term memory_network_for_industrial_process_fault_diagnosis_images/conv_84a6d24ab661c870.pdf-0004-24.png)


where _Ot_ is the output coefficient, _Ct_ is the updated cell state, ⊙ denotes element-wise multiplication, and _Ht_ is the current hidden state. 

The LSTM network processes the sequence input _Xt_ step by step through the above gating mechanism, and the output _Ht_ of the final time step is used as the high-level feature representation of the sample, which is provided to the subsequent fully connected layer for fault classification. However, the performance of the LSTM is highly dependent on hyperparameters such as initial learning rate, number of hidden layer nodes, and L2 regularization coefficient. Therefore, it is necessary to optimize these hyperparameters to improve the model generalization ability and fault diagnosis accuracy. 

#### _2.2. LSTM parameter optimization based on QDBO algorithm_ 

The initial learning rate, number of hidden layer nodes, and L2 regularization coefficient are selected as optimization objects, as they are widely confirmed to be the most performance-sensitive hyperparameters for the LSTM in industrial fault diagnosis [23], directly governing model convergence, feature learning capacity, and generalization. In contrast, dropout rate, number of layers, and optimizer type 


![](Entropy_space_quantum_behaved_dung_beetle_optimized_long_short-term memory_network_for_industrial_process_fault_diagnosis_images/conv_84a6d24ab661c870.pdf-0004-29.png)


**Fig. 2.** DBO Improvement Schematic Diagram. 

213 

_ISA Transactions 176 (2026) 210–223_ 


![](Entropy_space_quantum_behaved_dung_beetle_optimized_long_short-term memory_network_for_industrial_process_fault_diagnosis_images/conv_84a6d24ab661c870.pdf-0005-02.png)


**Fig. 3.** Sensitivity Analysis of the Step-Size Coefficient α. 

have negligible impacts on industrial time-series data due to its weak noise and inherent temporal dependencies, making additional optimization unnecessary. For the QDBO algorithm, the selection of 20% ball-rolling beetles and 20% quantum perturbation proportion follows the population configuration of the original DBO algorithm [24], which balances local exploitation and global exploration without arbitrary parameter setting. To address the issue of LSTM model hyperparameters 

being empirically set, which often leads to poor generalization capabilities, this article introduces a quantum behavior mechanism based on the traditional dune beetle optimization algorithm, proposing the quantum behavior-enhanced dune beetle optimization. This algorithm retains DBO advantage of achieving global optimization by simulating dung beetle behaviors such as rolling balls, foraging, and reproduction. Simultaneously, quantum behaviors enhance search randomness and 


![](Entropy_space_quantum_behaved_dung_beetle_optimized_long_short-term memory_network_for_industrial_process_fault_diagnosis_images/conv_84a6d24ab661c870.pdf-0005-06.png)


**Fig. 4.** The ES-QLSTM based Fault Diagnosis Structure. 

214 

> _S. Ao et al.                                                                                                                                                                                                                                       ISA Transactions 176 (2026) 210–223_ 

##### **Table 2** 

Summary of the CEC2017 test functions. 

|No.|Benchmark Functions|_F_<sup>∗</sup><br>_i_ <sup>=</sup><br>_Fi_(_X_<sup>∗</sup>)|Dim|Search<br>Interval|
|---|---|---|---|---|
|1|Shifted and Rotated Bent Cigar<br>Function|100|30|[−<br>100,100]|
|5|Shifted and Rotated Rastrigin’s<br>Function|500|30|[−<br>100,100]|
|13|Hybrid Function 3 (N=3)|1300|30|[−<br>100,100]|
|28|Composition Function 8 (N=6)|2800|30|[−<br>100,100]|



global exploration capabilities, effectively addressing the core shortcomings of the traditional DBO. a simplistic individual update mechanism leading to slowed convergence in later stages, limited beetle behaviors prone to local optima, and reduced population diversity during iterations, resulting in insufficient exploration. Therefore, the following improvement strategies is illustrated in Fig. 2. 

Define the LSTM hyperparameter optimization variables as a threedimensional vector. 

_θ_ = [ _α, h, ω_ ]<sup>_T_</sup> (18) 

where _α_ ∈[ _αmin, αmax_ ] is the initial learning rate, _h_ ∈[ _hmin, hmax_ ] is the number of nodes in the LSTM hidden layer, and _ω_ ∈[ _ωmin, ωmax_ ] is the L2 regularization coefficient. 

The classification error rate of the LSTM model on the training set serves as the fitness function for the QDBO algorithm, measuring the quality of hyperparameter combinations. For a given hyperparameter combination _θ_ , construct the LSTM network _f_ (⋅; _θ_ ) and evaluate it on the training set: 


![](Entropy_space_quantum_behaved_dung_beetle_optimized_long_short-term memory_network_for_industrial_process_fault_diagnosis_images/conv_84a6d24ab661c870.pdf-0006-09.png)


where _ci_ = _f_ ( _pi_ ; _θ_ ) denotes the model-predicted category, ci represents the true category, and _I_ (⋅) is the indicator function. 

The QDBO algorithm achieves basic optimization by simulating the dung beetle ball-rolling and foraging behaviors, while incorporating quantum behavior to enhance global exploration capabilities. Randomly generate _N_ candidate hyperparameter solutions covering the entire 


![](Entropy_space_quantum_behaved_dung_beetle_optimized_long_short-term memory_network_for_industrial_process_fault_diagnosis_images/conv_84a6d24ab661c870.pdf-0006-12.png)


**Fig. 5.** Performance comparison of distinct algorithms on CEC2017 test functions: (a) F1 (single-modal test function), (b) F5 (basic multi-modal test function), (c) F13 (hybrid test function), (d) F28 (composite test function). 

215 

> _S. Ao et al.                                                                                                                                                                                                                                       ISA Transactions 176 (2026) 210–223_ 


![](Entropy_space_quantum_behaved_dung_beetle_optimized_long_short-term memory_network_for_industrial_process_fault_diagnosis_images/conv_84a6d24ab661c870.pdf-0007-01.png)


**Fig. 6.** TEP flow chart. 

##### **Table 3** 

Fault categories and definitions in the tennessee eastman process. 

|Fault ID|Description|Fault Type|
|---|---|---|
|IDV 4|Reactor cooling water inlet temperature deviation<br>|Step|
|IDV 5|Condenser cooling water inlet temperature fuctuation|Step|
|IDV 7|Pressure loss in header C|Step|
|IDV 10|Temperature anomaly in feed stream C|RV|
|IDV 12|Condenser cooling water inlet temperature drift|RV|
|IDV 14|Sticking fault in reactor cooling water control valve|Sticking|



search space: 


![](Entropy_space_quantum_behaved_dung_beetle_optimized_long_short-term memory_network_for_industrial_process_fault_diagnosis_images/conv_84a6d24ab661c870.pdf-0007-07.png)


where _ri_ is a 0–1 uniform random vector, _lb_ = [ _α_ min _, h_ min _, ω_ min]<sup>_T_</sup> and _ub_ = [ _α_ max _, h_ max _, ω_ max]<sup>_T_</sup> respectively are the hyperparameter lower and upper bound vectors. 

The top 20% of individuals in the population was selected as ballrolling dung beetles. Their positions were updated by simulating their behaviors to improve the local exploitation of the algorithm. 


![](Entropy_space_quantum_behaved_dung_beetle_optimized_long_short-term memory_network_for_industrial_process_fault_diagnosis_images/conv_84a6d24ab661c870.pdf-0007-10.png)



![](Entropy_space_quantum_behaved_dung_beetle_optimized_long_short-term memory_network_for_industrial_process_fault_diagnosis_images/conv_84a6d24ab661c870.pdf-0007-11.png)


where _a_ ∈{ − 1 _,_ 1} is the random direction coefficient, _b_ ∈[0 _,_ 1] is the random step size coefficient, and _θ_<sup>(</sup> _worst_<sup>_t_−1)denotes the worst solution from</sup> generation _t_ − _1_ , guiding producers toward more favorable regions. The remaining individuals simulate foraging behavior to converge 


![](Entropy_space_quantum_behaved_dung_beetle_optimized_long_short-term memory_network_for_industrial_process_fault_diagnosis_images/conv_84a6d24ab661c870.pdf-0007-13.png)


among these, _θ_<sup>(</sup> _best_<sup>_t_)denotes the optimal solution of generation t,</sup><sup>_r1_and</sup><sup>_r2_</sup> are random vectors, and _Xnew1,Xnew2_ represent randomly selected positions of population individuals. 

Quantum behavioral perturbations are introduced to 20% of randomly selected individuals to enhance global exploration capabilities: 


![](Entropy_space_quantum_behaved_dung_beetle_optimized_long_short-term memory_network_for_industrial_process_fault_diagnosis_images/conv_84a6d24ab661c870.pdf-0007-16.png)


where _L_ = 0 _._ 1⋅(1 − _t/T_ max) denotes the feature length that decays with iterations, balancing exploration in the early phase and convergence in the late phase. The attenuation coefficient 0.1 of the feature length L is selected based on comprehensive performance evaluation on CEC2017 benchmark functions. As shown in Fig. 3, different values of the step-size coefficient lead to distinct convergence behaviors. The value 0.1 achieves the optimal balance between fast convergence and stable optimization performance, avoiding insufficient perturbation from smaller coefficients and excessive randomness from larger coefficients. It avoids insufficient perturbation from smaller coefficients and excessive randomness from larger coefficients ensuring stable optimization for LSTM hyperparameter tuning. _u, r_ ∈[0 _,_ 1]u _,_ r ∈[0 _,_ 1] represent random ⋅ vectors, and sign( ) denotes the sign function. 

Ensure that the updated hyperparameters do not exceed the search 

##### **Table 4** 

Test accuracy for fault diagnosis on TEP. 

|Fault(%)|IDV 4|IDV 5|IDV 7|IDV 10|IDV 12|IDV 14|Average|
|---|---|---|---|---|---|---|---|
|CNN|67.75|52.00|91.25|47.00|85.38|99.00|73.73|
|LSTM|100|91.00|100|59.50|65.13|45.75|76.89|
|ES-LSTM|98.75|67.13|98.63|65.88|71.00|99.88|83.54|
|KECA-GS-LSTM|99.13|88.50|98.75|85.25|66.38|95.13|88.86|
|DBO-LSTM|99.88|94.25|100|92.38|69.88|85.25|90.27|
|KPCA-QDBO-LSTM|99.38|93.25|99.13|91.50|63,75|99.50|91.09|
|QDBO-LSTM|99.88|94.50|99.88|98.25|64.63|99.88|92.83|
|BDNPEOLPP|99.25|97.25|100|97.13|36.63|96.13|87.73|
|ES-QLSTM|99.88|97.63|99.25|97.50|68.00|100|93.70|



216 

> _S. Ao et al.                                                                                                                                                                                                                                       ISA Transactions 176 (2026) 210–223_ 

space: 

_θ_<sup>(</sup> _i_<sup>_t_)</sup> = max(min( _θ_<sup>(</sup> _i_<sup>_t_)</sup><sup>_, ub_)</sup><sup>_, lb_)</sup> (25) 

Compute the fitness of each individual _F_<sup>(</sup> _i_<sup>_t_)</sup> = _F_ ( _θ_<sup>(</sup> _i_<sup>_t_))and update the</sup> global optimal solution: 

_θ_<sup>(</sup> _best_<sup>_t_+1)</sup> = argmin _iF_<sup>(</sup> _i_<sup>_t_)</sup> (26) 

When the iteration count reaches the maximum iteration count _T_ max, output the globally optimal hyperparameter combination _θ_<sup>∗</sup> = _θ_<sup>(</sup> _best_<sup>_T_max)</sup> as the final hyperparameters for the LSTM model. Algorithm 1 constitutes the complete pseudo-code of the QDBO algorithm. 

**Algorithm 1** . . Algorithm1 Algorithm of the QDBO. 

#### _2.3. The ES-QLSTM fault diagnosis steps_ 

Addressing the characteristics of high-dimensional nonlinearity and temporal dynamic coupling in industrial process data, as well as issues such as insufficient feature extraction and inefficient parameter optimization in traditional fault diagnosis models, an ES-QLSTM based fault diagnosis method is proposed. The framework of this proposed method is illustrated in Fig. 4. The specific steps of the ES-QLSTM based fault diagnosis are as follows. 

Step 1: Data Preparation: Collect raw industrial process data, partition it into training and test sets, and separate features from fault labels. Standardize the feature matrix using the z-score method. 

Step 2: Entropy Feature Extraction: Using standardized training set features as input, construct a kernel matrix between samples with a 


![](Entropy_space_quantum_behaved_dung_beetle_optimized_long_short-term memory_network_for_industrial_process_fault_diagnosis_images/conv_84a6d24ab661c870.pdf-0008-11.png)


217 

> _S. Ao et al.                                                                                                                                                                                                                                       ISA Transactions 176 (2026) 210–223_ 


![](Entropy_space_quantum_behaved_dung_beetle_optimized_long_short-term memory_network_for_industrial_process_fault_diagnosis_images/conv_84a6d24ab661c870.pdf-0009-01.png)


**Fig. 7.** Visualization graph of the first 3-D features on TEP. 

Gaussian kernel function. Apply centering to eliminate the impact of data distribution shifts. Perform eigenvalue decomposition on the centered kernel matrix. Calculate the entropy contribution of each principal component using R´enyi entropy theory. Select key principal components in descending order of entropy contribution. 

Step 3: Global Optimization of LSTM Hyperparameters Using the QDBO: Configure QDBO algorithm parameters, using the training error of the LSTM on entropy features as the fitness function, and iteratively select optimal hyperparameters that best fit the temporal patterns of entropy features. 

Step 4: Training the LSTM Model with Optimal Parameters: Convert the entropy features from the KECA dimensionality reduction into a cell array format compatible with the LSTM. Transform the labels into categorical variables. Combine these with the optimal hyperparameters optimized by the QDBO to construct the LSTM diagnostic model. 

Step 5: Fault Classification: Introduce the fused features into the fully connected layer and perform fault classification using the softmax activation function. 

#### **3. Optimization algorithm comparison** 

To validate the superiority of the proposed quantum behavior optimization DBO, the CEC2017 function set was employed for testing. This benchmark collection comprises a series of optimization problems of varying types, serving as a standard for evaluating the performance of alternative optimization algorithms. The dataset comprises 30 singleobjective test functions categorized into unimodal functions (F1-F3), simple multimodal functions (F4-F10), hybrid functions (F11-F20), and composite functions (F21-F30). For each category, one representative function was selected for comparison as shown in Table 2. Additionally, mainstream optimization algorithms were introduced to contrast with the unmodified DBO. 

The results in Fig. 5 demonstrate that on the CEC2017 optimization problems, the quantum-behaved dung beetle optimization (QDBO) algorithm exhibits superior performance compared to a broader set of 

advanced hybrid optimization algorithms, including quantum-behaved particle swarm optimization (QPSO), chaotic whale optimization algorithm (CWOA) [25], golden jackal optimization (GJO) [26], northern goshawk optimization (NGO) [27], and the traditional DBO. To ensure statistical reliability, each algorithm is run 30 times independently, and the mean convergence curves with 95% confidence intervals are presented in Fig. 5. As shown in Fig. 5(d), in complex large-scale composite optimization scenarios, the convergence curve of the QDBO algorithm consistently lies below those of all comparative algorithms, including the QPSO, the CWOA, the GJO, the NGO, and the DBO, with significantly faster convergence speed. The QDBO achieves a stable optimal fitness value on the order of 10 ¹ within only about 80 iterations, while the QPSO, the CWOA, the traditional DBO, the GJO, and other algorithms require more than 250 iterations to stabilize, with their final fitness values only reaching the order of 10 ³ –10⁴. Moreover, the shaded confidence intervals for QDBO are the narrowest among all algorithms, indicating its high stability and repeatability across independent runs. Unlike traditional DBO and other advanced hybrid algorithms, which show obvious fluctuations and wider confidence bands, the QDBO exhibits minimal variance after convergence, with the fluctuation amplitude controlled within 5%, fully reflecting its superior global optimization capability and convergence efficiency in complex combinatorial optimization problems. 

In summary, the QDBO effectively enhances hyperparameter optimization performance in high-dimensional nonlinear problems by introducing adaptive step sizes and quantum perturbations into the original dung beetle optimization framework. Such approaches not only boost the algorithm global and local search capacities, but also elevate its randomness and population diversity, enabling superior performance in complex environments. Compared with advanced hybrid algorithms, the QDBO achieves faster convergence, lower final fitness values, and better stability, further verifying its effectiveness in the LSTM hyperparameter tuning for industrial fault diagnosis tasks. 

218 

_ISA Transactions 176 (2026) 210–223_ 


![](Entropy_space_quantum_behaved_dung_beetle_optimized_long_short-term memory_network_for_industrial_process_fault_diagnosis_images/conv_84a6d24ab661c870.pdf-0010-02.png)


**Fig. 8.** Fault diagnosis on the TEP. 

#### **4. Case studies** 

#### _4.1. The TEP_ 

The TEP is a well-established benchmark for complex chemical processes and has long served as a standard testbed in fault diagnosis and process optimization research [28]. As illustrated in Fig. 6, the TEP configuration includes four gaseous feed streams, two liquid product streams, a single byproduct stream, and a conversion gas stream, with its operational behavior described by a total of 52 process variables [29]. The test suite encompasses 21 distinct fault scenarios, grouped into six broad categories, whose detailed characteristics are documented in reference [30]. For each fault category, the corresponding dataset is structured to support model development and validation: 480 samples are allocated for training, and 960 samples are reserved for testing, with process measurements recorded at 3-minute intervals. 

To validate the effectiveness of the ES-QLSTM method, six fault types 

from Table 3 are selected for testing [31]. In the TEP, 1200 samples are collected for each fault type, with the training and test sets split in a 1:2 ratio. 

Table 4 shows that the ES-QLSTM model performs optimally in all six fault scenarios of TEP fault diagnosis, with an average accuracy of 93.70%, which is significantly better than that of the CNN with 73.73%, and the LSTM with 76.89%. Fig. 6 presents the three-dimensional feature vector plot, which reveals significant data overlap between IDV10 and IDV12 in fault diagnosis, primarily due to their strong coupling, as both faults are temperature-related. For the randomly fluctuating faults IDV10 and IDV12, traditional models and single deep learning models exhibit extremely low recognition accuracy. IDV10 achieves 47.00%, and 59.50% accuracy under the CNN, and the LSTM, respectively, whereas the ES-QLSTM achieves 97.50% fault diagnosis accuracy. For IDV12, the LSTM achieves 65.13% accuracy, while the ESQLSTM reaches 68.00%. the KECA-LSTM averages 83.54%, the DBOLSTM with 90.27%, and the QDBO-LSTM with 92.83% all lower than 

219 

> _S. Ao et al.                                                                                                                                                                                                                                       ISA Transactions 176 (2026) 210–223_ 


![](Entropy_space_quantum_behaved_dung_beetle_optimized_long_short-term memory_network_for_industrial_process_fault_diagnosis_images/conv_84a6d24ab661c870.pdf-0011-01.png)


**Fig. 9.** Schematic diagram of the grid-connected photovoltaic system process flow. 

##### **Table 5** 

Fault category definitions for GPVS experiments. 

|Fault ID|Fault Type|
|---|---|
|F1L|Inverter module malfunction|
|F2L|Feedback sensor signal anomaly|
|F3L|Abnormal grid operating conditions|
|F4L|Partial mismatch in PV array output|
|F5L|PV array performance inconsistency|
|F6L|Malfunction in MPPT/IPPT control unit|
|F7L|Fault in boost converter control module|



the ES-QLSTM. The temperature coupling characteristics of IDV10 and IDV12 make it difficult for traditional methods to distinguish fault features, while entropy space feature extraction preserves the high-order statistical information of temperature signals based on R´enyi entropy and achieves effective decoupling of coupled signals. The low learning rate and adaptive hidden layer node parameters obtained by the QDBO algorithm make the LSTM more sensitive to the temporal patterns of random temperature fluctuations and slow drifts, thus achieving significantly higher diagnostic accuracy for these two faults. The 40.67% accuracy result of F2L from sensor noise, feature overlap with F6L, and insufficient noise suppression and coupled fault differentiation. For IDV5 faults, the KECA-LSTM achieves only 67.13% accuracy, where 

the ES-QLSTM reaches 97.63%, fully demonstrating the synergistic advantages of entropy feature extraction and quantum behavior parameter optimization. Additionally, the recent advanced dimensionality reduction-based fault diagnosis method with the BDNPEOLPP [32] achieves an average accuracy of 87.73% on the TEP dataset, which is lower than the ES-QLSTM 93.70%. Moreover, the ES-QLSTM outperforms the BDNPEOLPP significantly in IDV12 68.00% versus with 36.63% and IDV14 100% versus with 96.13% faults, demonstrating stronger robustness to drift and sticking faults. 

As shown in the confusion matrix for fault diagnosis in Fig. 8, traditional models such as the CNN, and the LSTM exhibit significant misclassification issues. For random fluctuating faults IDV10 and IDV12, these models demonstrate inadequate classification performance, with a large number of samples incorrectly classified as normal or other fault types. This pattern is clearly visible in the confusion matrix, where the off-diagonal entries for these fault types make up a considerable share of the total. By comparison, the confusion matrix derived from the ESQLSTM model shows a marked increase in the proportion of diagonal entries across all fault type rows. In particular, the number of misclassified samples for IDV10 and IDV12 is drastically lower. When benchmarked against other state-of-the-art models, the ES-QLSTM confusion matrix demonstrates stronger diagonal concentration, which confirms its superior fault classification accuracy. This allows for more precise differentiation between fault types and, as a result, lowers the overall rate of misclassification. It should be noted that the experimental 

**Table 6** 

Test accuracy for fault diagnosis on GPVS. 

|Fault|F1L|F2L|F3L|F4L|F5L|F6L|F7L|Average|
|---|---|---|---|---|---|---|---|---|
|CNN|100|64|32.33|99.67|83.33|100|44.33|74.81|
|LSTM|100|0|23.33|100|100|100|77.33|71.52|
|ES-LSTM|99.67|38.00|41.00|100|100|100|44.67|74.76|
|KECA-GS-LSTM|99.67|38.33|45.00|100|100|100|52.00|76.43|
|DBO-LSTM|100|41.33|35.00|100|100|100|60.00|76.62|
|KPCA-QDBO-LSTM|100|34.33|62.00|100|100|100|59.33|79.38|
|QDBO-LSTM|100|35.33|68.33|100|100|100|63.00|80.95|
|BDNPEOLPP|83.33|95.67|100|100|100|1.67|100|83.38|
|ES-QLSTM|100|40.67|69.00|100|100|100|77.00|83.91|



220 

> _S. Ao et al.                                                                                                                                                                                                                                       ISA Transactions 176 (2026) 210–223_ 


![](Entropy_space_quantum_behaved_dung_beetle_optimized_long_short-term memory_network_for_industrial_process_fault_diagnosis_images/conv_84a6d24ab661c870.pdf-0012-01.png)


**Fig. 10.** Visualization graph of the first 3-D features on GPVS. 

validation of the ES-QLSTM model mainly focuses on verifying its diagnostic accuracy for complex faults in industrial processes. Consistent with the research focus of the BDNPEOLPP, quantitative analysis of the lightweight computing performance is not included in the present experimental design. 

#### _4.2. Grid-connected power generation system_ 

Azzeddine Bakdi developed a case study for GPVS [33], whose flowchart is shown in Fig. 9. Fault data is collected from fault laboratory experiments in photovoltaic (PV) microgrid applications, with each data point comprising 13 dimensions. Scenarios involved PV array faults, inverter faults, grid anomalies, feedback sensor faults, and MPPT controller faults. 

This study employes seven out of fourteen distinct fault scenarios, with fault descriptions detailed in Table 5. During the GPVS simulation process, 1000 samples are collected for each fault type, comprising 700 training data points and 300 test data points. 

Table 6 shows that the ES-QLSTM achieves an average accuracy of 83.91% in diagnosing seven types of GPVS faults, significantly outperforming the CNN with 74.81%, and the LSTM with 71.52%. Fig. 9 presents the three-dimensional feature vector map. It reveals severe data overlap between F6L and F2L in fault diagnosis, primarily due to the strong coupling between these two faults related to the controller. Traditional models perform poorly for complex faults such as feedback sensor fault F2L, grid anomaly F3L, and boost converter fault F7L. F2L achieves only 2.00% and 0% accuracy under the LSTM, respectively. F3L achieves 29.33% and 23.33% accuracy under the LSTM, respectively. The sensor noise interference of F2L and the dynamic coupling of grid signals of F3L form the main diagnosis difficulties. Entropy space feature extraction suppresses noise and retains the core fault information, providing purer input features for the LSTM. Quantum behavior search endows the QDBO with stronger global optimization capability, and the obtained parameter set enhances the LSTM ability to learn weak fault signals and dynamic coupling features, leading to better performance in diagnosing these two complex faults. The 40.67% accuracy results of F2L from sensor noise, feature overlap with F6L, and insufficient noise suppression and coupled fault differentiation. while F7L achieved 44.33% under the CNN. The ES-QLSTM model improves the accuracies of F2L, F3L, and F7L to 40.67%, 69.00%, and 77.00%, respectively. 

Among the improved models, the ES-LSTM achieves an average accuracy of 74.76%, the DBO-LSTM reaches 76.62%, and the QDBO-LSTM attaines 80.95%, all lower than the ES-QLSTM. Particularly for F7L faults, the DBO-LSTM accuracy is only 60.00%, while the ES-QLSTM improves the accuracy by 17 %age points, highlighting the effectiveness of its parameter optimization and feature extraction. Meanwhile, the BDNPEOLPP obtains an average accuracy of 83.38% on the GPVS dataset, slightly lower than the ES-QLSTM with 83.91%. While the BDNPEOLPP excels in F2L with 95.67% and F3L with 100% faults due to its powerful dimensionality reduction capability, the ES-QLSTM shows overwhelming advantages in F1L 100% versus with 83.33% and F6L 100% versus with 1.67% faults, verifying the effectiveness of our synergistic framework of entropy space feature extraction and quantum behaved optimization. 

From the fault diagnosis confusion matrix in Fig. 11, it can be observed that traditional models such as the SVM, the CNN, and the LSTM exhibit significant misclassification of samples for faults F2L, F3L, and F7L. The non-diagonal elements in the rows corresponding to these faults within the confusion matrix are numerous, indicating blurred classification boundaries. In contrast, the confusion matrix of the ESQLSTM demonstrates superior classification performance, with no misclassifications for faults F1L, F4L, F5L, and F6L. The number of misclassified samples for F2L, F3L, and F7L is significantly lower than that of traditional models and some modified models. Compared to the DBOLSTM and the QDBO-LSTM, the ES-QLSTM exhibits a higher proportion of diagonal elements in the confusion matrix rows corresponding to F2L, F3L, and F7L, with fewer samples misclassified into other fault categories. This indicates its ability to more accurately identify complex faults in GPVS and deliver more stable and reliable classification performance. 

#### **5. Conclusion** 

This paper proposes a novel fault diagnosis method named ESQLSTM. The proposed method uses the kernel entropy component analysis based entropy space feature extraction to process industrial data in entropy space with R´enyi entropy as the feature selection metric, which reduces data dimension while preserving high-order fault information and improves feature extraction for high-dimensional nonlinear data. Then, the QDBO algorithm dynamically updates the quantum 

221 

> _S. Ao et al.                                                                                                                                                                                                                                       ISA Transactions 176 (2026) 210–223_ 


![](Entropy_space_quantum_behaved_dung_beetle_optimized_long_short-term memory_network_for_industrial_process_fault_diagnosis_images/conv_84a6d24ab661c870.pdf-0013-01.png)


**Fig. 11.** Fault diagnosis on GPVS. 

stride and applies quantum perturbations to optimize LSTM hyperparameters efficiently, thus strengthening the model generalization ability. Experimental results on two industrial benchmarks demonstrate the superiority of the ES-QLSTM. On the TEP dataset, the ES-QLSTM achieves 93.70% average accuracy, which is notably higher than the SVM, the CNN and the single LSTM. On the GPVS dataset, the ES-QLSTM reaches 83.91% average accuracy and also outperforms these comparison methods. Especially for the strongly coupled fault IDV10 in the TEP, the ES-QLSTM obtains 97.50% accuracy, which verifies its strong diagnostic performance. 

Future research will incorporate the SHAP analysis to quantify feature contributions and clarify model decision logic, and further develop lightweight model architectures to enhance computational efficiency for real-time industrial applications. 

#### **Nomenclatures** 

Symbol 

###### Symbol Description 

_X_ = ( _x_ 1 _, x_ 2 _,_ ⋯ _, xn_ ) 

Raw industrial process data matrix ( _m_ × _n_ , _m_ is the number of variables, _n_ is the sample size) 

_ϕ_ (⋅) 

Nonlinear mapping function for kernel feature space projection 

Kernel matrix constructed by Gaussian kernel function ( _n_ × _n_ ) 

###### _K_ 

Λ = diag( _λ_ 1 _,_ ⋯ _, λn_ ) _E_ = ( _e_ 1 _,_ ⋯ _, en_ ) 

Eigenvalue matrix of the centered kernel matrix Eigenvector matrix of the centered kernel matrix R´enyi entropy contribution of the _i_<sup>th</sup> principal component Score matrix of dimensionality-reduced features (top _k_ principal components selected by entropy contribution) Eigenvalue matrix corresponding to top _k_ principal components 

_ψi_ 

_Tk_ = [ _t_ 1 _, t_ 2 _,_ ⋯ _, tk_ ] 

Λ _k_ = diag( _λ_ 1 _,_ ⋯ _, λk_ ) 

_Ekk_ = [ _e_ 1 _,_ ⋯ _, ekk_ ] 

_Ekk_ = [ _e_ 1 _,_ ⋯ _, ekk_ ] Eigenvector matrix corresponding to top _k_ principal components _P_ train Preprocessed feature matrix for LSTM input ( _t_ × _n_ , _t_ is the feature dimension after normalization) 

( _continued on next page_ ) 

222 

> _S. Ao et al.                                                                                                                                                                                                                                       ISA Transactions 176 (2026) 210–223_ 

|(_continued_)||
|---|---|
|_α_|Initial learning rate of LSTM (hyperparameter,_α_∈[_α_min_,_<br>_α_max])|
|_h_|Number of hidden layer neurons in LSTM (hyperparameter,<br>_h_∈[_h_min_,h_max])<br>|
|_λ_|L2 regularization coeffcient of LSTM (hyperparameter,_λ_∈<br>[_λ_min_,λ_max])|
|_θ_= (_α,h,λ_)|Hyperparameter vector of LSTM optimized by QDBO<br>|
|_F_(_θ_)|Fitness function of QDBO (classifcation error rate of LSTM<br>on training set)|
|_N_|Population size of QDBO algorithm|
|_lb_=|Lower bound vector of hyperparameter search space|
|[_α_min_, h_min_, λ_min]<sup>_T_</sup>||
|_ub_=|Upper bound vector of hyperparameter search space|
|[_α_max_, h_max_, λ_max]<sup>_T_</sup>||
|_θ_<sup>(</sup><sup>_t_)</sup><br>best|Optimal hyperparameter solution of QDBO at iteration_t_|
|_θ_<sup>(</sup><sup>_t_−1)</sup><br>worst|Worst hyperparameter solution of QDBO at iteration_t_ −<br>1|
|_T_max|Maximum number of iterations of QDBO algorithm|
|_L_=0_._1⋅(1 −_t/T_max)|Feature length decaying with iterations (for quantum<br>behavior perturbation)|
|_u,r_|Uniform random vectors in[0_,_1](for quantum behavior<br>perturbation)<br>|
|_a_∈{ −<br>1_,_1}|Random direction coeffcient (for ball-rolling behavior<br>update in QDBO)<br>|
|_b_∈[0_,_1]|Random step size coeffcient (for ball-rolling behavior<br>update in QDBO)|
|_r_1_,r_2|Random vectors (for foraging behavior update in QDBO)|
|_X_new1_,X_new2|Randomly selected individual positions in QDBO population|
|_Ht_|Hidden state output of LSTM at time step_t_|
|_Ct_|Cell state of LSTM at time step_t_|
|_ft_|Output of LSTM forget gate at time step_t_|
|_it_|Output of LSTM input gate at time step_t_|
|_Ct_|Candidate cell state of LSTM at time step_t_|
|_Ot_|Output of LSTM output gate at time step_t_|
|_Uf,Vf,δf_|Weight matrices and bias vector of LSTM forget gate|
|_ci_|True fault category of the_i_-th sample|
|_ci _= _f_(_pi_;_θ_)|Predicted fault category of the_i_-th sample (LSTM output)|
|_I_(⋅)|Indicator function (1 if input condition is true, 0 otherwise)|



#### **CRediT authorship contribution statement** 

**Yongming Han:** Writing – review & editing, Visualization, Resources, Project administration, Funding acquisition. **Tao Li:** Writing – review & editing, Validation, Resources. **Haorui Liu:** Writing – original draft, Visualization, Methodology, Data curation. **Bo Ma:** Writing – review & editing, Project administration, Funding acquisition. **Shuai Ao:** Writing – original draft, Visualization, Resources, Methodology. 

#### **Declaration of Competing Interest** 

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper. 

#### **Acknowledgement** 

This work is supported by the National Natural Science Foundation of China (62273025 and 62422303). 

#### **References** 

- [1] Kong L, Mao Y, Zhang T, Chen X, Wang Z, Wang X. Online data-driven diagnosis for common electrical and sensor faults in dual three-phase PMSM drives. IEEE Trans Instrum Meas 2025;74:1–10. 

- [2] Han H, Li H, Wu X, Yang H, Zhao D. Cascaded LSTM-based state prediction of equipment in wastewater treatment process. IEEE Trans Instrum Meas 2024;73: 1–12. 

- [3] Hu Y, Qiu A, Wang Y, Wang S. Multirate sampled data driven fast rate fault detection of dynamic systems. ISA Trans 2025. 

- [4] Scholkopf B, Smola A, Müller KR. Nonlinear component analysis as a kernel ¨ eigenvalue problem. Neural Comput 1998;10:1299–319. 

- [5] Fezai R, Mansouri M, Taouali O, Harkat FM, Bouguila N. Online reduced kernel principal component analysis for process monitoring. J Process Control 2018;61: 1–11. 

- [6] Jenssen R. Kernel entropy component analysis. IEEE Trans Pattern Anal Mach Intell 2010;32:847–60. 

- [7] Li T, Han Y, Xu W, Geng Z. Novel adaptive fault detection method based on kernel entropy component analysis integrating moving window of dissimilarity for nonlinear dynamic processes. J Process Control 2023;125:1–18. 

- [8] Wang S, Wei J, Zhang L, Li H, Fernandez C, Blaabjerg F. Improved harmonic loss – History gated unit recycling for online state of charge and state of energy coestimation of lithium-ion batteries for large-scale energy storage stations. Energy 2025;340:139225. 

- [9] Hochreiter S, Schmidhuber J. Long short-term memory. Neural Comput 1997;9: 1735–80. 

- [10] You GD, Chang ZC, Li XY, Liu ZF, Xiao ZY, Lu YR, et al. Using enhanced variational modal decomposition and dung beetle optimization algorithm optimization-kernel extreme learning machine model to forecast short-term wind power. Electr Power Syst Res 2024;236:110904. 

- [11] Liu H, Wu J, Qian X. Fault prediction model based on PSO–LSTM–ATT. Int J LowCarbon Technol 2025;20:671–8. 

- [12] Gao B, Xu J, Zhang Z, Liu Y, Chang X. Marine diesel engine piston ring fault diagnosis based on LSTM and improved Beluga whale optimization. Alex Eng J 2024;109:213–28. 

- [13] Wang Q, Zheng M, Yang K, Shang C, Luo Y. Research and implementation of fault data recovery method for dry-type transformer temperature control sensor based on ISSA-LSTM algorithm. Measurement 2024;228:114333. 

- [14] Yousaf MZ, Singh AR, Khalid S, Bajaj M, Kumar BH. Bayesian-optimized LSTMDWT approach for reliable fault detection in MMC-based HVDC systems. Sci Rep 2024;14:17968. 

- [15] Si Y, Wang R, Zhang S, Zhou W, Lin A, Wang Y. Fault diagnosis based on attention collaborative LSTM networks for NPC three-level inverters. IEEE Trans Instrum Meas 2022;71:1–16. 

- [16] Zeng L, Jin Q, Lin Z, Zheng C, Wu Y, Wu X, Gao X. Dual-attention LSTM autoencoder for fault detection in industrial complex dynamic processes. Process Saf Environ Prot 2024;185:1145–59. 

- [17] Wang S, Dang Q, Gao Z, Li B, Fernandez C, Blaabjerg F. An innovative square root – untraced Kalman filtering strategy with full-parameter online identification for state of power evaluation of lithium-ion batteries. J Energy Storage 2024;104: 114555. 

- [18] Wang S, Wang C, Takyi-Aninakwa P, Jin S, Fernandez C, Huang Q. An improved parameter identification and radial basis correction-differential support vector machine strategies for state-of-charge estimation of urban-transportation-electricvehicle lithium-ion batteries. J Energy Storage 2023;68:110222. 

- [19] Xue J, Shen B. Dung beetle optimizer: a new meta-heuristic algorithm for global optimization. J Supercomput 2023;79:7305–36. 

- [20] Li X, Zeng Y, Qian J, Wang Y, Zhang X, Wang F, Li D. A new multi-strategy optimization stability prediction framework based on DBO-Case study of pumped storage units. J Energy Storage 2025;125:117005. 

- [21] Wang X, Han Y, Chu C, Geng Z. Adaptive small-family population-guided swarm intelligence optimization algorithm. SCI CHINA INF SCI 2026;65(3):132208: 1–132208:17. 

- [22] Agrawal UK, Panda N. Quantum-inspired adaptive mutation operator enabled PSO (QAMO-PSO) for parallel optimization and tailoring parameters of Kolmogorov–Arnold network. J Supercomput 2025;81:1310. 

- [23] Ewees AA, Al-qaness MAA, Abualigah L, Abd Elaziz M. HBO-LSTM: Optimized long short term memory with heap-based optimizer for wind power forecasting. Energy Convers Manag 2022;268:116022. 

[24] He J, Guo W, Wang S, Chen H, Guo X, Li S. Application of multi-strategy based improved DBO algorithm in optimal scheduling of reservoir groups. Water Resour Manag 2024;38:1883–901. 

- [25] Ramachandran R, Kannan S, Ganesan SK, Annamalai B. Optimal economicemission load dispatch in microgrid incorporating renewable energy sources by golden jackal optimization (GJO) and Mexican Axolotl optimization (MAO). Energy Environ 2025;36:2001–26. 

- [26] Nadimi-Shahraki MH, Zamani H, Asghari Varzaneh Z, Mirjalili S. A systematic review of the whale optimization algorithm: theoretical foundation, improvements, and hybridizations. Arch Comput Methods Eng 2023;30:4113–59. 

- [27] Han X, Lv F, Li J, Zeng F. Flexible interactive control method for multi-scenario sharing of hybrid pumped storage-wind-photovoltaic power generation. J Energy Storage 2024;100:113590. 

- [28] Xiao Y, Shi H, Wang B, Tao Y, Tan S, Song B. Weighted conditional discriminant analysis for unseen operating modes fault diagnosis in chemical processes. IEEE Trans Instrum Meas 2022;71:1–14. 

- [29] Lee G, Han C, Yoon ES. Multiple-fault diagnosis of the Tennessee Eastman process based on system decomposition and dynamic PLS. Ind Eng Chem Res 2004;43: 8037–48. 

- [30] Zhang N, Xu Y, Zhu QX, He YL. Farthest-nearest distance neighborhood and locality projections integrated with bootstrap for industrial process fault diagnosis. IEEE Trans Ind Inform 2022;19:6284–94. 

- [31] Zhang N, Xu Y, Zhu QX, He YL. Improved locality preserving projections based on heat-kernel and cosine weights for fault classification in complex industrial processes. IEEE Trans Reliab 2022;72:204–13. 

- [32] Zhang N, Tian Y, Wang XW, Xu Y, Zhu QY, He YL. Novel bootstrap-based discriminant NPE integrated with orthogonal LPP for fault diagnosis. IEEE Trans Instrum Meas 2023;72:1–9. 

- [33] Bakdi A, Bounoua W, Guichi A, Mekhilef S. Real-time fault detection in PV systems under MPPT using PMU and high-frequency multi-sensor data through online PCAKDE-based multivariate KL divergence. Int J Electr Power Energy Syst 2021;125: 106457. 

223 

