Journal of Industrial Information Integration 40 (2024) 100622 


![](Learnable_Faster_Kernel-PCA_for_Nonlinear_Fault_Detection-_Deep_Autoencoder-Based_Realization_(DAE-PCA)_images/conv_90ae2c3db7fdef77.pdf-0001-01.png)


Contents lists available at ScienceDirect 

# Journal of Industrial Information Integration 

journal homepage: www.elsevier.com/locate/jii 


![](Learnable_Faster_Kernel-PCA_for_Nonlinear_Fault_Detection-_Deep_Autoencoder-Based_Realization_(DAE-PCA)_images/conv_90ae2c3db7fdef77.pdf-0001-05.png)


#### Full length article 

## Learnable faster kernel-PCA for nonlinear fault detection: Deep autoencoder-based realization 


![](Learnable_Faster_Kernel-PCA_for_Nonlinear_Fault_Detection-_Deep_Autoencoder-Based_Realization_(DAE-PCA)_images/conv_90ae2c3db7fdef77.pdf-0001-08.png)


### Zelin Ren<sup>a,∗</sup> , Yuchen Jiang<sup>b,∗</sup> , Xuebing Yang<sup>a</sup> , Yongqiang Tang<sup>a</sup> , Wensheng Zhang<sup>a</sup> 

a _Institute of Automation, Chinese Academy of Sciences, Beijing 100190, China_ b _Control and Simulation Center, Harbin Institute of Technology, Harbin 150001, China_ 

|A R T I C L E<br>I N F O|A B S T R A C T|
|---|---|
|_Keywords:_<br>Kernel Principal Component Analysis (KPCA)<br>Fault detection<br>Process monitoring<br>Autoencoder<br>Data-driven|Kernel principal component analysis (KPCA) is a well-recognized nonlinear dimensionality reduction method<br>that has been widely used in nonlinear fault detection tasks. As a kernel trick-based method, KPCA inherits<br>two major problems. First, the form and the parameters of the kernel function are usually selected blindly,<br>depending seriously on trial-and-error. As a result, there may be serious performance degradation in case of<br>inappropriate selections. Second, at the online monitoring stage, KPCA has much computational burden and<br>poor real-time performance, because the kernel method requires to leverage all the offline training data. In this<br>work, to deal with the two drawbacks, a learnable faster realization of the conventional KPCA is proposed. The<br>core idea is to parameterize all feasible kernel functions using the novel nonlinear DAE-FE (deep autoencoder<br>based feature extraction) framework and propose DAE-PCA (deep autoencoder based principal component<br>analysis) approach in detail. The proposed DAE-PCA method is proved to be equivalent to KPCA but has more<br>advantage in terms of automatic searching of the most suitable nonlinear high-dimensional space according<br>to the inputs, which helps to improve the accuracy of fault detection. Furthermore, the online computational<br>efficiency improves by many times compared with the conventional KPCA. Finally, the Tennessee Eastman<br>(TE) process benchmark and wastewater treatment plant (WWTP) benchmark are employed to illustrate the<br>effectiveness of the proposed method, where the average fault detection rates of DAE-PCA are at least 0.27%<br>and 4.69% higher than those of other methods, and its online computational efficiency is faster 90.48% and<br>24.57% times than that of KPCA respectively.|



##### **1. Introduction** 

Fault detection plays an important role in maintaining normal operating conditions and ensuring system safety, which has attracted extensive attention in recent years [1–3]. Efficient fault detection can greatly strengthen the system reliability and reduce unexpected economic loss [4]. With the increasing complexity of industrial processes, data-driven fault detection and process monitoring techniques take the dominant position in the field of fault detection and have become a research hotspot [5–11]. How to excavate the potential system information for different fault detection tasks from the massively available sensor data remains challenging. 

Kernel principal component analysis (KPCA) is a typical and wellknown data-driven method for dimensionality reduction based on kernel trick [12,13]. Owing to its good nonlinear feature extraction capability, KPCA and its extensions have been widely used for various fault detection and multivariate statistical process monitoring (MSPM) tasks 

of industrial processes currently [14–16]. Zhang et al. [17] presented a fault detection frame of subspace reconstruction-based robust kernel principal component analysis model and it was employed to wind turbine systems. Simmini et al. [18] proposed a self-tuning KPCA method to detect the faults in chiller systems with a high accuracy. Deng et al. [19] integrated principal component analysis (PCA) and KPCA and presented a serial PCA that has the ability to better exploit the underlying process’s structure in order to enhance fault diagnosis performance. Moreover, Deng et al. [20] also proposed an improved KPCA method by a deep architecture, called deep PCA (DePCA), which adopts the layerwise feature extraction strategy to obtain the multilevel data features for nonlinear process monitoring. 

Although the kernel method has the ability to monitor nonlinear systems and detect faults by observing the fluctuations of features in high-dimensional space, it still has several problems and drawbacks. 

> ∗ Corresponding authors. 

_E-mail addresses:_ rzl8816@126.com (Z. Ren), yc.jiang@hit.edu.cn (Y. Jiang), yangxuebing2013@ia.ac.cn (X. Yang), yongqiang.tang@ia.ac.cn (Y. Tang), zhangwenshengia@hotmail.com (W. Zhang). 

https://doi.org/10.1016/j.jii.2024.100622 

Received 27 June 2023; Received in revised form 2 January 2024; Accepted 28 April 2024 

Available online 3 May 2024 2452-414X/© 2024 Published by Elsevier Inc. 

_Z. Ren et al._ 

_Journal of Industrial Information Integration 40 (2024) 100622_ 

First, the choice of kernel function has a great influence on the detection performance of the method. The forms of kernel function are multitudinous, and once a specific form of kernel function is determined, such as radial basis function (RBF) kernel, that means a subset of nonlinear mapping functions is determined. When its kernel parameters are chosen by offline testing (such as _𝜎_ in RBF kernel), a specific nonlinear mapping is finally determined. It can be seen that this process has blindness, because the choice of kernel function totally depends on artificial selection and the kernel parameters are selected by trial and error. When there is no domain knowledge/expert experience, blind selection of kernel parameters will greatly limit the optimal selection of high-dimensional space. If the domain knowledge/expert experience is unsuitable for the working condition, it will also lead to unsatisfactory kernel parameters for fault detection. Thus, how to automatically search a proper kernel parameter is an intractable issue. To solve the problem, Tonin et al. [21] proposed a deep kernel PCA methodology (DKPCA) to extract multiple levels of the most informative components of the data. The approach can be regarded as a learnable deep KPCA to some extent by using neural network structure, but it does not specify the relationship between its nonlinear mapping function and the kernel function. Second, the online detection of the kernel method requires all offline samples. It causes a huge amount of calculation and has a serious influence when having demand on timely detection. In order to tackle the problem of low-efficiency online calculation existing in kernel methods, some researchers have tried to come up with some solutions in the past decade. Radhia Fezai et al. [22,23] developed an online reduced KPCA method and online reduced kernel GLRT technique to realize online and real time process monitoring by reducing the number of kernel functions. Ryan et al. [24] proposed a fast kernel transform (FKT) algorithm that achieves the combination of computational efficiency and broad applicability by leveraging a new general analytical expansion. Wang et al. [25] proposed a new idea of kernel sample equivalent replacement (KSER) method to display the kernel matrix as a quadratic form of the samples. Based on its benefits, Jiao et al. [26] presented a KPLS-KSER method by combining KPLS and KSER, which can effectively convert the kernel matrix calculation of new samples into linear operations in online fault detection, avoiding the exponential increase of computation time. However, none of the above methods simultaneously solve the problem from the selection of kernel parameters and online computational efficiency. Therefore, it is necessary to propose a new approximate nonlinear mapping method to replace current kernel methods. 

To deal with the drawbacks of the existing KPCA-based methods, we consider reforming the DAE network to realize a learnable and faster KPCA by designing a network structure. Deep autoencoder (DAE) is a basic and popular data-driven deep learning method [27–30]. Due to its outstanding performance on powerful nonlinear representation for mass data, the potential of DAE has been demonstrated in industry. Recently, many researchers have presented a large number of variants, which have been prosperously applied to the fault detection and diagnosis area [8,30–33]. How to adopt DAE to efficiently serve various fault detection tasks, instead of kernel methods, has become the recent tendency. 

In this article, we handle the aforementioned problems existing in kernel method by proposing a DAE-FE (deep autoencoder based feature extraction) framework, which includes an encoder module, a linear feature extraction (LFE) module, and a decoder module. We prove that the DAE-FE framework is essentially equivalent to a learnable and faster kernel method. Further, based on the DAE-FE framework, a DAEPCA (deep autoencoder based principal component analysis) method is proposed to transform PCA into the corresponding nonlinear approach. The difference between KPCA and DAE-PCA is that the process that KPCA transforms a linear approach into the corresponding nonlinear version is composed of two stages. The first stage is to determine kernel function by manual selection. The second stage is to apply the 

determined kernel function to convert the linear method into a nonlinear one. Therefore, for the kernel method, the setting of the kernel parameters is completely artificial and independent of the following linear method. The effect of nonlinearity depends entirely on artificial setting and has blindness. As for DAE-PCA method, it is an end-toend learning process. When the network structure is determined, the encoder module and decoder module, as nonlinear modules, are learned together with the linear module in each back-propagation. The benefit of DAE-PCA is that the nonlinear modules serve the linear module and automatically search for a more suitable higher-dimensional space, which KPCA cannot achieve. In the detailed design of DAE-PCA, a PCA module is devised to achieve the function of PCA dimensionality reduction based on Cayley Transform [34]. The key contributions of our DAE-PCA can be summarized as follows. 

- A DAE-FE framework is proposed for nonlinear fault detection. Based on the DAE-FE framework, a DAE-PCA method is further proposed, which is theoretically proven to be equivalent to a learnable KPCA. Compared with KPCA, the DAE-PCA method can automatically acquire the weight parameters of the network through training, unlike KPCA that selects kernel parameters blindly, depending seriously on trial-and-error. 

- The proposed DAE-PCA method presents an alternative faster implementation of KPCA. In comparison with the conventional KPCA, the DAE-PCA method costs less time for online detection since its online detection time do not rely on the amount of training data, which greatly meets the requirement of real-time detection. 

- To obtain a orthogonal load matrix, the idea of Cayley Transform is introduced to the design of the DAE-PCA method. Compared to the trick of introducing regularization term in the loss function, the orthogonal load matrix acquired by our proposed trick has a better orthogonal characteristic. 

The rest of this article is organized as follows. In Section 2, KPCA and DAE are briefly illustrated. Section 3 first presents the DAE-FE framework. After that, the proposed implementation of DAE-PCA is presented for nonlinear fault detection. In Section 4, the effectiveness and feasibility of the proposed approach are demonstrated in the Tennessee Eastman (TE) process benchmark and wasterwater treatment plant (WWTP) benchmark. Finally, Section 5 concludes this article. 

##### **2. Preliminaries** 

##### _2.1. KPCA_ 

Suppose that there are _𝑚_ sensors in an industrial system and each sensor collects _𝑁_ samples, the input variable matrix can be denoted as **𝐗** , i.e., 


![](Learnable_Faster_Kernel-PCA_for_Nonlinear_Fault_Detection-_Deep_Autoencoder-Based_Realization_(DAE-PCA)_images/conv_90ae2c3db7fdef77.pdf-0002-13.png)


As a typical linear self-supervised model, the traditional PCA [35] model achieves dimensionality reduction by the principle of capturing the maximum variance of the input data, and it can be formulated by minimizing the reconstruction error: 


![](Learnable_Faster_Kernel-PCA_for_Nonlinear_Fault_Detection-_Deep_Autoencoder-Based_Realization_(DAE-PCA)_images/conv_90ae2c3db7fdef77.pdf-0002-15.png)


##### _𝑠.𝑡._ **𝐏**<sup>_⊤_</sup> **𝐏** = **𝐈** _𝑎,_ 

where **𝐏** ∈ R<sup>_𝑚_×</sup><sup>_𝑎_</sup> is the orthogonal load matrix, _𝑎_ denotes the feature dimension after PCA operation, and ‖⋅‖ _𝐹_ represents _𝐹_ -norm. Furthermore, we can obtain the dimensionality-reduction feature **𝐓** ∈ R<sup>_𝑁_×</sup><sup>_𝑎_</sup> , i.e., the score matrix, which can be calculated by 


![](Learnable_Faster_Kernel-PCA_for_Nonlinear_Fault_Detection-_Deep_Autoencoder-Based_Realization_(DAE-PCA)_images/conv_90ae2c3db7fdef77.pdf-0002-18.png)


2 

_Z. Ren et al._ 

_Journal of Industrial Information Integration 40 (2024) 100622_ 

KPCA is a nonlinear PCA method by introducing the kernel method. Kernel method aims to map the original process variables into a highdimension reproducing kernel Hilbert space (RKHS) through a proper nonlinear mapping function, thus solving linearly inseparable problems [12]. Given a nonlinear mapping function _𝜙_ (⋅), it maps the original samples **𝐱** _𝑖_ ( _𝑖_ = 1 _,_ 2 _,_ … _, 𝑁_ ) into a RKHS , i.e., **𝐱** _𝑖_ ∈ R<sup>_𝑚_</sup> → _𝜙_<sup>(</sup> **𝐱** _𝑖_ ) ∈ R _𝑑_ , where _𝑑_ is the dimension of . Thus, **𝐗** is mapped into a nonlinear feature matrix **Φ** , 


![](Learnable_Faster_Kernel-PCA_for_Nonlinear_Fault_Detection-_Deep_Autoencoder-Based_Realization_(DAE-PCA)_images/conv_90ae2c3db7fdef77.pdf-0003-03.png)


Notice that **Φ** needs to be centralized to be zero mean, 


![](Learnable_Faster_Kernel-PCA_for_Nonlinear_Fault_Detection-_Deep_Autoencoder-Based_Realization_(DAE-PCA)_images/conv_90ae2c3db7fdef77.pdf-0003-05.png)



![](Learnable_Faster_Kernel-PCA_for_Nonlinear_Fault_Detection-_Deep_Autoencoder-Based_Realization_(DAE-PCA)_images/conv_90ae2c3db7fdef77.pdf-0003-06.png)


Accordingly, the optimization problem of KPCA can be written as 


![](Learnable_Faster_Kernel-PCA_for_Nonlinear_Fault_Detection-_Deep_Autoencoder-Based_Realization_(DAE-PCA)_images/conv_90ae2c3db7fdef77.pdf-0003-08.png)


where **𝐏** ∈ R<sup>_𝑑_×</sup><sup>_𝑎_</sup> is the orthogonal load matrix. Then, the score matrix **𝐓** is computed by **𝐓** = **Φ𝐏** . 

When finishing model establishment, PCA or KPCA will map the original space into a principal component subspace () and a residual subspace (), thereby achieving fault detection in these two subspaces. 

##### _2.2. DAE_ 

The DAE can be trained to extract nonlinear system features by minimizing the reconstruction error of the input in an unsupervised self-learning manner. The main advantage of DAE is reconstructing the input data with fewer errors and effectively extracting the nonlinear feature. In DAE, the structure is made up of two parts: an encoder and a decoder. The encoder aims to extract the system features by nonlinear mapping of the input, while the decoder is used to reconstruct the input. 

Let **𝐗** and **𝐗** ∈ R<sup>_𝑁_×</sup><sup>_𝑚_</sup> be the input and output of DAE. The encoder and the decoder are respectively represented by nonlinear mappings _𝐸𝑛_ (⋅) and _𝐷𝑒_ (⋅), of which the nonlinearity is expressed by nonlinear activation functions. Formally, we have 

**𝐗** = _𝐷𝑒_ ( _𝐸𝑛_ ( **𝐗** )) _._ (5) 

The loss function for training DAE can be expressed by 


![](Learnable_Faster_Kernel-PCA_for_Nonlinear_Fault_Detection-_Deep_Autoencoder-Based_Realization_(DAE-PCA)_images/conv_90ae2c3db7fdef77.pdf-0003-16.png)


where  (⋅) is the reconstruction loss and _𝛺_ denotes regularization terms for specific problems or prior knowledge. The common choice of  (⋅) is the sum of square errors, 


![](Learnable_Faster_Kernel-PCA_for_Nonlinear_Fault_Detection-_Deep_Autoencoder-Based_Realization_(DAE-PCA)_images/conv_90ae2c3db7fdef77.pdf-0003-18.png)


When the network has finished training, the extracted nonlinear system feature **𝐓** ∈ R<sup>_𝑁_×</sup><sup>_𝑎_</sup> and the reconstruction error **𝐗** ∈ R<sup>_𝑁_×</sup><sup>_𝑚_</sup> can be acquired by 


![](Learnable_Faster_Kernel-PCA_for_Nonlinear_Fault_Detection-_Deep_Autoencoder-Based_Realization_(DAE-PCA)_images/conv_90ae2c3db7fdef77.pdf-0003-20.png)


##### **3. Methodology** 

##### _3.1. DAE-FE framework_ 

The proposed DAE-FE framework is to transform linear feature extraction methods to their nonlinear versions using neural networks. The whole DAE-FE network structure is illustrated in Fig. 1, which consists of three modules: the encoder module, the LFE module, and the decoder module. The encoder and decoder modules aim to realize the transformation from the original input space  and RKHS  respectively. The purpose of the LFE module is to utilize a neural network to achieve the function of LFE, thereby obtaining nonlinear system features in . LFE is usually solved by matrix operation. In order to have the same form as other modules, it is necessarily transformed into the structure of neural network. In this way, the LFE module can combine the encoder module and the decoder module to jointly realize an end-to-end solution through back-propagation. 

##### _3.1.1. Encoder module_ 

It utilizes _𝐸𝑛_ (⋅) to map the original input **𝐗** ∈ R<sup>_𝑁_×</sup><sup>_𝑚_</sup> from the input domain  into a nonlinear feature space  to obtain the feature matrix **Φ** = _𝐸𝑛_ ( **𝐗** ) ∈ R<sup>_𝑁_×</sup><sup>_𝑑_</sup> . 

It will be proven in Proposition 1 that _𝐸𝑛_ (⋅) is in essence a learnable nonlinear function that can construct a kernel function. To describe the relationship between _𝐸𝑛_ (⋅) and kernel method, we need to give the following definition and lemma, of which the relevant proofs can be referred to the literature [36]. 

**Definition 1.** Given the _𝑁_ -dimensional input domain  _⊂_ R<sup>_𝑁_</sup> , a function _𝐾_ ∶  ×  → R is called a kernel over  which is expressed by 

##### ∀ **𝐱** _,_ **𝐱**<sup>′</sup> ∈  _, 𝐾_<sup>(</sup> **𝐱** _,_ **𝐱**<sup>′)</sup> =<sup>⟨</sup> _𝜙_ ( **𝐱** ) _, 𝜙_<sup>(</sup> **𝐱**<sup>′)⟩</sup> = _𝜙_ ( **𝐱** )<sup>_⊤_</sup> _𝜙_<sup>(</sup> **𝐱**<sup>′)</sup> _,_ 

where ⟨⋅⟩ denotes inner product operation and _𝜙_ (⋅) is a nonlinear mapping function. 

**Lemma 1.** _Let kernel 𝐾_ ∶  ×  → R _be a continuous and symmetric function. Then, 𝐾 is said to be a positive definite symmetric (PDS) kernel if for any_<sup>{</sup> **𝐱** 1 _,_ … _,_ **𝐱** _𝑁_ } _⊆_  _, the Gram matrix_ **𝐊** = [ _𝐾_ ( **𝐱** _𝑖,_ **𝐱** _𝑗_ )] _𝑖,𝑗_<sup>∈R</sup><sup>_𝑁_×</sup><sup>_𝑁is_</sup> _symmetric positive semidefinite (SPSD)._ 

**Lemma 2.** _Let 𝐾_ ∶  ×  → R _be a PDS kernel. Then, there exists a Hilbert space_  _and a mapping 𝜙_ (⋅) _from_  _to_  _such that:_ 

##### ∀ **𝐱** _,_ **𝐱**<sup>′</sup> ∈  _, 𝐾_<sup>(</sup> **𝐱** _,_ **𝐱**<sup>′)</sup> =<sup>⟨</sup> _𝜙_ ( **𝐱** ) _, 𝜙_<sup>(</sup> **𝐱**<sup>′)⟩</sup> _._ 

_Furthermore,_  _is called a RKHS associated with 𝐾 if it has the following reproducing property:_ 


![](Learnable_Faster_Kernel-PCA_for_Nonlinear_Fault_Detection-_Deep_Autoencoder-Based_Realization_(DAE-PCA)_images/conv_90ae2c3db7fdef77.pdf-0003-34.png)


**Remark 1.** Definition 1 gives the definition of the kernel function. The sufficient condition from Lemma 1 is a vital criterion to prove whether a function can realize to construct a corresponding kernel function. When Lemma 1 is satisfied, Lemma 2 tells that a RHKS associated with _𝐾_ must be exist. 

The above preliminaries provide the theoretical basis to further prove why the function _𝐸𝑛_ (⋅) from the encoder module is equivalent to a learnable function whose inner product is a kernel function. Now, Proposition 1 is advanced as: 


![](Learnable_Faster_Kernel-PCA_for_Nonlinear_Fault_Detection-_Deep_Autoencoder-Based_Realization_(DAE-PCA)_images/conv_90ae2c3db7fdef77.pdf-0003-37.png)


For fault detection tasks, **𝐓** and **𝐗** can be utilized to monitor the  and , respectively. 

**Proposition 1.** _The function 𝐸𝑛_ (⋅) _from the encoder module is a nonlinear mapping whose inner product is a learnable kernel function. In addition, the space_  _associated with this learnable kernel is a RKHS._ 

3 

_Z. Ren et al._ 

_Journal of Industrial Information Integration 40 (2024) 100622_ 


![](Learnable_Faster_Kernel-PCA_for_Nonlinear_Fault_Detection-_Deep_Autoencoder-Based_Realization_(DAE-PCA)_images/conv_90ae2c3db7fdef77.pdf-0004-02.png)


**Fig. 1.** The whole network structure of DAE-FE framework. 

**Proof.** In the encoder module, the nonlinear activation functions are real-valued continuous functions and it only contain linear operators except for activation functions. Thus, as their composite functions, _𝐸𝑛_ (⋅) is a real-valued continuous function. According to Definition 1, a continuous and symmetric kernel _𝐾_ can be expressed by 


![](Learnable_Faster_Kernel-PCA_for_Nonlinear_Fault_Detection-_Deep_Autoencoder-Based_Realization_(DAE-PCA)_images/conv_90ae2c3db7fdef77.pdf-0004-05.png)


The input **𝐗** is a matrix defined in the real domain. **Φ** = _𝐸𝑛_ ( **𝐗** ) is also in the real domain. Thus, **𝐊** is the Gram matrix with respect to _𝐾_ and **𝐗** can be calculated by 


![](Learnable_Faster_Kernel-PCA_for_Nonlinear_Fault_Detection-_Deep_Autoencoder-Based_Realization_(DAE-PCA)_images/conv_90ae2c3db7fdef77.pdf-0004-07.png)


From (11), **𝐊** is a real symmetric matrix. For any vector **𝐱** ∈ R<sup>_𝑁_</sup> , it holds that 


![](Learnable_Faster_Kernel-PCA_for_Nonlinear_Fault_Detection-_Deep_Autoencoder-Based_Realization_(DAE-PCA)_images/conv_90ae2c3db7fdef77.pdf-0004-09.png)


Thus, **𝐊** is SPSD. According to Lemma 1, the kernel _𝐾_ is PDS kernel. Owing to Lemma 2, since _𝐾_ is a PSD kernel, the space  is a Hilbert space, and more specifically, a RKHS. □ 

From Proposition 1, it can be seen that _𝐸𝑛_ (⋅) is in essence a nonlinear mapping function, of which the inner product is a learnable kernel function. Different neural network structures and parameters will correspond to a different _𝐸𝑛_ (⋅), and thus to a different kernel function. During training, the neural network executes back-propagation through loss function. When the training is over, a kernel function will be determined and can meet the requirements of the task. 

##### _3.1.2. LFE module_ 

The major role of this module is to achieve linear feature extraction or dimensionality reduction for **Φ** . 

In general, the input of LFE methods (such as PCA) needs to be standardized in each dimension, that is, the zero-mean and unit variance. Its main purpose is as follows: on one hand, the data of each dimension can be transformed to the same scale and pulled to the same baseline (origin of coordinates), so as to guarantee that each dimension has equal importance. On another hand, it is beneficial to the convergence of the gradient descent method. 

To standardize **Φ** in  that is as the output of the encoder module, we introduce the Batch Normalization (BN) trick [37] into the encoder module. Two trainable parameters in BN trick require to be fixed as _𝛾_ = 1 and _𝛽_ = 0. In specific, **Φ** can be expressed as 


![](Learnable_Faster_Kernel-PCA_for_Nonlinear_Fault_Detection-_Deep_Autoencoder-Based_Realization_(DAE-PCA)_images/conv_90ae2c3db7fdef77.pdf-0004-16.png)


where _𝜇_ ( **Φ** ) and _𝜎_ ( **Φ** ) are the mean and standard deviation of **Φ** , respectively. Thus, 

It should be noted that the kernel method just executes centralization for **Φ** , because **Φ** in (3) is unknown, its variance cannot be processed to 1. Compared with the centralization in kernel method for **Φ** , our standardized treatment has better performance in data preprocessing. 

The following network structure is designed in accordance with the given LFE method. The linear dimensionality reduction of **Φ** is first performed to obtain the system feature **𝐅** . Then, **Φ** in  is reconstructed as **Φ** _𝐹𝑆_ by **𝐅** under the constraint of loss function _𝑙𝑜𝑠𝑠_ **Φ** , which is expressed as: 


![](Learnable_Faster_Kernel-PCA_for_Nonlinear_Fault_Detection-_Deep_Autoencoder-Based_Realization_(DAE-PCA)_images/conv_90ae2c3db7fdef77.pdf-0004-20.png)


where _𝜆_ **Φ** is a non-negative hyper-parameter, and _𝛺_ **Φ** is the regularization term in _𝑙𝑜𝑠𝑠_ **Φ** . 

Further, **Φ** is decomposed into the following parts: 


![](Learnable_Faster_Kernel-PCA_for_Nonlinear_Fault_Detection-_Deep_Autoencoder-Based_Realization_(DAE-PCA)_images/conv_90ae2c3db7fdef77.pdf-0004-23.png)



![](Learnable_Faster_Kernel-PCA_for_Nonlinear_Fault_Detection-_Deep_Autoencoder-Based_Realization_(DAE-PCA)_images/conv_90ae2c3db7fdef77.pdf-0004-24.png)


where **Φ** _𝑅𝑆_ denotes the residual part of **Φ** , and _𝑓_ 1 (⋅) and _𝑓_ 2 (⋅) are both linear functions. The neural network from **Φ** _𝐹𝑆_ to **Φ** _𝐹𝑆_ is a fully connected layer that is viewed as the inverse process of BN trick. 

##### _3.1.3. Decoder module_ 

It is designed for the purpose of mapping the output **Φ** _𝐹𝑆_ of LFE module from  back to , and reconstruct the original input **𝐗** under the constraint of the loss function _𝑙𝑜𝑠𝑠_ **𝐗** as 


![](Learnable_Faster_Kernel-PCA_for_Nonlinear_Fault_Detection-_Deep_Autoencoder-Based_Realization_(DAE-PCA)_images/conv_90ae2c3db7fdef77.pdf-0004-28.png)


Since the decoder network structure is almost symmetric with the encoder, it can be regarded as the inverse process of the encoder and effectively realizes the self-supervised learning for **𝐗** . 

Through the above descriptions of DAE-FE framework, the entire loss function can be expressed as 

##### _𝑙𝑜𝑠𝑠_ = _𝜆_ 1 _𝑙𝑜𝑠𝑠_ **𝐗** + _𝜆_ 2 _𝑙𝑜𝑠𝑠_ **Φ** + _𝜆_ 3 _𝛺,_ (20) 

where _𝜆𝑖_ ( _𝑖_ = 1 _,_ 2 _,_ 3) is a non-negative hyper-parameter, and _𝛺_ is the regularization term for a specific to a fault detection task. According to (20), all three modules of DAE-FE are jointly trained through backpropagation. After training DAE-FE network, we can use **𝐅** to monitor  and **𝐗** to monitor . 

It is worth noticing that as the LFE module can be designed according to a specific LFE method, we can leverage DAE-FE as a learnable kernel method to convert any LFE method to the nonlinear version. 

1 _𝑁_<sup>**𝟏**</sup> _𝑁_<sup>_⊤_</sup><sup>**Φ**=</sup><sup>**𝟎**</sup><sup>_._</sup> (14) 

4 

_Z. Ren et al._ 

_Journal of Industrial Information Integration 40 (2024) 100622_ 

##### _3.1.4. Kernel trick and DAE-FE_ 

In this part, we describe the relationship and differences between the kernel trick and DAE-FE model. 

The determination of kernel trick contains two aspects, one is the choice of kernel function and the other is the determination of its parameters. The determination of DAE-FE model also contains two aspects, one is the selection of neural network structure, and the other is the determination of network parameters. The DAE-FE model corresponds exactly to the kernel trick in these two aspects. 

For the first aspect, the choice of kernel function in kernel trick determines the upper limit of nonlinear mapping ability. For example, the upper limit of nonlinear mapping ability of RBF kernel is theoretically higher than that of polynomial kernel. In DAE-FE model, the neural network structure determines the upper limit of nonlinear mapping ability by setting the number of network layers and activation functions. In general, the DAE-FE model does not need to specifically choose a nonlinear activation function. Most of the nonlinear activation functions have strong enough nonlinear ability to nonlinearly map the input into a linearly separable space when the number of network layers is sufficient. The higher the number of layers is, the stronger the nonlinear representation ability is. Usually, in the field of fault diagnosis, selecting Gaussian kernel and several layers of neural networks is enough to reach the upper limit required for nonlinear mapping. Therefore, the selection of DAE-FE network structure, such as the number of layers and the activation function, can meet the requirements as long as they are selected within a reasonable range. 

More attention needs to be paid to the second aspect, namely the determination of the kernel and network parameters, since they determine at what level the kernel function and DAE-FE model can achieve within the upper limit. For the selection of kernel parameters, it relies on domain knowledge/expert experience or blind trial and error. In practical application, the selection of kernel parameters of different kernel functions does not follow the same rules, and kernel parameters with small numerical differences may lead to completely different fault detection results, which makes it difficult for the artificially specified kernel parameters to exert the nonlinear mapping ability of kernel function for fault detection tasks. Perhaps, the selected kernel parameters may be effective, but the effect is hardly satisfactory. Different from kernel parameters, the DAE-FE network parameters are acquired by backpropagation. Given initial values, the network can automatically learn the optimal parameters according to the input data, in order to obtain the nonlinear mapping ability that is most suitable for the current fault detection task. Compared with the kernel trick, the DAEFE model has a glaring advantage that its network parameters have the ability to learn automatically with no blindness. 

##### _3.2. DAE-PCA method_ 

In order to achieve the function of PCA, the matrix **𝐏** learned by the neural network must be orthogonal. In other words, hard constraint is necessary to guarantee the orthogonality during the training process. We propose to solve this issue with the aid of Cayley Transform. Our DAE-PCA method is illustrated in Fig. 2. 

##### _3.2.1. PCA module_ 

For this module, the optimization problem can be described like (4) of KPCA, i.e., 


![](Learnable_Faster_Kernel-PCA_for_Nonlinear_Fault_Detection-_Deep_Autoencoder-Based_Realization_(DAE-PCA)_images/conv_90ae2c3db7fdef77.pdf-0005-11.png)


Note that the input of the PCA module is obtained by the encoder module, rather than kernel trick. 

_𝛺_ **Φ** Let: the loss function _𝑙𝑜𝑠𝑠_ **Φ** _PCA of PCA module be _𝑙𝑜𝑠𝑠_ **Φ** without 


![](Learnable_Faster_Kernel-PCA_for_Nonlinear_Fault_Detection-_Deep_Autoencoder-Based_Realization_(DAE-PCA)_images/conv_90ae2c3db7fdef77.pdf-0005-14.png)


Thus, in DAE-PCA, training the network to minimize2 _𝑙𝑜𝑠𝑠_ **Φ** _PCA is equivalent to min **𝐏**<sup>‖</sup> ‖ **Φ** − **Φ𝐏𝐏**<sup>_⊤_‖</sup> ‖ _𝐹_<sup>.Hence,thesystemfeature</sup><sup>**𝐓**isobtained</sup> by 


![](Learnable_Faster_Kernel-PCA_for_Nonlinear_Fault_Detection-_Deep_Autoencoder-Based_Realization_(DAE-PCA)_images/conv_90ae2c3db7fdef77.pdf-0005-16.png)


At the same time, we need to restrict **𝐏** to satisfy the constraint that **𝐏**<sup>_⊤_</sup> **𝐏** = **𝐈** _𝑎_ . For such purpose, we devise the neural network based on Cayley Transform to acquire **𝐏** . Cayley Transform was first established by Arthur Cayley, one proposition of which is given as follows [34]. 

**Proposition 2.** _If_ **𝐒** _is a real antisymmetric matrix and_ **𝐈** _is the identity matrix, then_ **𝐀** = ( **𝐈** − **𝐒** ) ( **𝐈** + **𝐒** )<sup>−1</sup> _is an orthonormal matrix._ 

**𝐏** can be directly obtained by the network structure as shown in the solid green border in Fig. 2, of which the input is fixed to the identity matrix _𝐼𝑑_ × _𝑑_ and the output is an orthogonal matrix **𝐏** that is acquired by the neural networks restricted based on Cayley Transform. Through training the entire DAE-PCA network with back-propagation mechanism, an optimal **𝐏** suitable for the PCA module can be learned. The detailed descriptions for acquiring **𝐏** in solid green border are in the following steps: 

- (1) Fix the input to be identity matrix **𝐈** ∈ R<sup>_𝑑_×</sup><sup>_𝑑_</sup> and initialize a square matrix **𝐌** 0 ∈ R<sup>_𝑑_×</sup><sup>_𝑑_</sup> . Thus, **𝐌** 0 is obtained by **𝐌** 0 = **𝐌** 0 **𝐈** ; 

- (2) Get the upper triangular matrix **𝐌** 1 ∈ R<sup>_𝑑_×</sup><sup>_𝑑_</sup> of **𝐌** 0; 

- (3) Obtain the matrix **𝐒** ∈ R<sup>_𝑑_×</sup><sup>_𝑑_</sup> by **𝐒** = **𝐌** 1 − **𝐌**<sup>_⊤_</sup> 1<sup>;</sup> 

- (4) According to Proposition 2, obtain an orthogonal square matrix **𝐀** ∈ R<sup>_𝑑_×</sup><sup>_𝑑_</sup> by **𝐀** = ( **𝐈** − **𝐒** ) ( **𝐈** + **𝐒** )<sup>−1</sup> ; 

- (5) Take the first _𝑎_ orthogonal column vectors of **𝐀** to get the orthogonal projection matrix **𝐏** ∈ R<sup>_𝑑_×</sup><sup>_𝑎_</sup> , where _𝑎_ is similar to the principle component number in PCA; 

- (6) The most optimal projection matrix **𝐏** for the PCA module will be acquired by back-propagation mechanism. 

Notice that learning for matrix **𝐏** is in essence to learn about matrix **𝐌** 0. Once **𝐌** 0 is determined, **𝐏** is also determined. 

The above trick is implemented by a hard constraint, rather than a soft constraint by adding any regularization term about orthogonality, i.e., _𝛺_ **Φ** =<sup>‖</sup> ‖ **𝐏**<sup>_⊤_</sup> **𝐏** − **𝐈** _𝑎_<sup>‖</sup> ‖2 _𝐹_<sup>.Comparedwiththesoftconstraint,theadvan-</sup> tage of our hard constraint is that its orthogonal performance is always maintained and is not be affected by the design of the loss function. 

Through the above analysis, the function _𝑙𝑜𝑠𝑠_ DAE−PCA in our DAEPCA is expressed as 


![](Learnable_Faster_Kernel-PCA_for_Nonlinear_Fault_Detection-_Deep_Autoencoder-Based_Realization_(DAE-PCA)_images/conv_90ae2c3db7fdef77.pdf-0005-28.png)


In addition, set _𝜆_ 1 = _𝑁_ 1× _𝑚_<sup>and</sup><sup>_𝜆_2=</sup> _𝑁_ 1× _𝑑_<sup>thataimstoeliminatethe</sup> effect of the number of matrix elements for each item of loss. 

##### _3.3. DAE-PCA based nonlinear fault detection_ 

To detect whether some faults occur in the system adopting DAEPCA method, we employ the two most commonly used statistics in fault diagnosis community to monitor  and  respectively, i.e., Hotelling’s _𝑇_<sup>2</sup> statistics and squared prediction error ( _𝑆𝑃𝐸_ ) statistics. 

The flowchart of nonlinear fault detection based on DAE-PCA is summarized in Fig. 3. Given the training data matrix **𝐗** ∈ R<sup>_𝑁_×</sup><sup>_𝑚_</sup> , according to (23) and (9), we have the system feature matrix **𝐓** ∈ R<sup>_𝑁_×</sup><sup>_𝑎_</sup> and residual matrix **𝐗** ∈ R<sup>_𝑁_×</sup><sup>_𝑚_</sup> . Set **𝐱** ∈ R<sup>_𝑚_</sup> to be a sample of **𝐗** , its Hotelling’s _𝑇_<sup>2</sup> statistics and _𝑆𝑃𝐸_ statistics can be defined as follows: 


![](Learnable_Faster_Kernel-PCA_for_Nonlinear_Fault_Detection-_Deep_Autoencoder-Based_Realization_(DAE-PCA)_images/conv_90ae2c3db7fdef77.pdf-0005-33.png)



![](Learnable_Faster_Kernel-PCA_for_Nonlinear_Fault_Detection-_Deep_Autoencoder-Based_Realization_(DAE-PCA)_images/conv_90ae2c3db7fdef77.pdf-0005-34.png)


where **𝐭** ∈ R<sup>_𝑎_</sup> , **𝐱** ∈ R<sup>_𝑚_</sup> are the system feature vector and residual vector with respect to **𝐱** , and **Λ** = **𝐓𝐓**<sup>_⊤_</sup> ∕( _𝑁_ −1) is the covariance matrix of **𝐭** . 

5 

_Z. Ren et al._ 

_Journal of Industrial Information Integration 40 (2024) 100622_ 


![](Learnable_Faster_Kernel-PCA_for_Nonlinear_Fault_Detection-_Deep_Autoencoder-Based_Realization_(DAE-PCA)_images/conv_90ae2c3db7fdef77.pdf-0006-02.png)


**Fig. 2.** The whole network structure of DAE-PCA, where the PCA module is shown with a solid blue border and the acquisition of **𝐏** is in a solid green border. 


![](Learnable_Faster_Kernel-PCA_for_Nonlinear_Fault_Detection-_Deep_Autoencoder-Based_Realization_(DAE-PCA)_images/conv_90ae2c3db7fdef77.pdf-0006-04.png)


**Fig. 3.** The flowchart of nonlinear fault detection based on DAE-PCA. 

We set the threshold of _𝑇_<sup>2</sup> statistics and _𝑆𝑃𝐸_ statistics as _𝐽𝑡ℎ,𝑇_ 2 and _𝐽𝑡ℎ,𝑆𝑃𝐸_ respectively, which are calculated by applying _𝑇_<sup>2</sup> and SPE to the kernel probability estimation (KDE) scheme under the given confidence limit _𝛼_ . The calculation method about KDE can be referred to [38]. 

For a test sample **𝐱** _𝑛𝑒𝑤_ ∈ R<sup>_𝑚_</sup> , let its system feature and residual be **𝐭** _𝑛𝑒𝑤_ ∈ R<sup>_𝑚_</sup> and **𝐱** _𝑛𝑒𝑤_ ∈ R<sup>_𝑚_</sup> , respectively. Thus, _𝑇_<sup>2</sup> statistics and SPE statistics of **𝐱** _𝑛𝑒𝑤_ are computed by 


![](Learnable_Faster_Kernel-PCA_for_Nonlinear_Fault_Detection-_Deep_Autoencoder-Based_Realization_(DAE-PCA)_images/conv_90ae2c3db7fdef77.pdf-0006-08.png)



![](Learnable_Faster_Kernel-PCA_for_Nonlinear_Fault_Detection-_Deep_Autoencoder-Based_Realization_(DAE-PCA)_images/conv_90ae2c3db7fdef77.pdf-0006-09.png)


In order to provide a clear detection logic, the statistics _𝑇_<sup>2</sup> and _𝑆𝑃𝐸_ are integrated into a statistics, Bayesian information criterion ( _𝐵𝐼𝐶_ ), according to the Bayesian inference [39,40]. To simplify the descriptions, these two statistics and their thresholds are represented sinceby twothesets,following _𝑆_ =<sup>{</sup> _𝑇_<sup>2</sup> derivations _, 𝑆𝑃𝐸_<sup>}</sup> andare _𝐽𝑡ℎ,𝑆_ the =same<sup>{</sup> _𝐽𝑡ℎ,𝑇_ for2 _,_ them. _𝐽𝑡ℎ,𝑆𝑃𝐸_ } respectively, 

The fault posterior probability of _𝑆_ is calculated by 


![](Learnable_Faster_Kernel-PCA_for_Nonlinear_Fault_Detection-_Deep_Autoencoder-Based_Realization_(DAE-PCA)_images/conv_90ae2c3db7fdef77.pdf-0006-12.png)


6 

_Z. Ren et al._ 

_Journal of Industrial Information Integration 40 (2024) 100622_ 

_𝑃𝑇_ 2 <u>(</u> **𝐱** _𝑛𝑒𝑤_ | _𝐹_ <u>)</u> _𝑃𝑇_ 2 <u>(</u> _𝐹_ || **𝐱** _𝑛𝑒𝑤_ <u>) +</u> _𝑃𝑆𝑃𝐸_ <u>(</u> **𝐱** _𝑛𝑒𝑤_ | _𝐹_ <u>)</u> _𝑃𝑆𝑃𝐸_ <u>(</u> _𝐹_ || **𝐱** _𝑛𝑒𝑤_ <u>)</u> _𝐵𝐼𝐶_<sup>(</sup> **𝐱** _𝑛𝑒𝑤_ ) = _._ (33) _𝑃𝑇_ 2 ~~(~~ **𝐱** _𝑛𝑒𝑤_ | _𝐹_ ~~)~~ + _𝑃𝑆𝑃𝐸_ ~~(~~ **𝐱** _𝑛𝑒𝑤_ | _𝐹_ ~~)~~ **Box I.** 

**Fig. 4.** The diagram of the TE process. 

where _𝑁_ and _𝐹_ denote the normal and faulty state. The normal prior probability _𝑃𝑆_ ( _𝑁_ ) equals to _𝛼_ and the faulty prior probability _𝑃𝑆_ ( _𝐹_ ) is 1 − _𝛼_ . The normal and faulty conditional probability are defined as 


![](Learnable_Faster_Kernel-PCA_for_Nonlinear_Fault_Detection-_Deep_Autoencoder-Based_Realization_(DAE-PCA)_images/conv_90ae2c3db7fdef77.pdf-0007-05.png)


Further, the statistics _𝐵𝐼𝐶_ can be obtained in (33), which is adopted to monitor the full space that is called .  can be regarded as the space by combining  with . Thus, the detection logic in  is expressed as follows: (see the Eq. (33) in Box I). 


![](Learnable_Faster_Kernel-PCA_for_Nonlinear_Fault_Detection-_Deep_Autoencoder-Based_Realization_(DAE-PCA)_images/conv_90ae2c3db7fdef77.pdf-0007-07.png)


##### **4. Case study** 

|**Table 1**<br>Fault types|in the TE process.||
|---|---|---|
|No.|Description|Type|
|IDV(1)|A/C Feedratio, B composition constant (Stream 4)|Step|
|IDV(2)|B composition, A/C ratio constant (Stream 4)|Step|
|IDV(3)|D feed temperature (Stream 2)|Step|
|IDV(4)|Reactor cooling water inlet temperature|Step|
|IDV(5)|Condenser cooling water inlet temperature|Step|
|IDV(6)|A feed loss (Stream 1)|Step|
|IDV(7)|C header pressure loss (Stream 4)|Step|
|IDV(8)|A, B, C feed composition (Stream 4)|Random variation|
|IDV(9)|D feed temperature (Stream 2)|Random variation|
|IDV(10)|C feed temperature (Stream 4)|Random variation|
|IDV(11)|Reactor cooling water inlet temperature|Random variation|
|IDV(12)|Condenser cooling water inlet temperature|Random variation|
|IDV(13)|Reactor kinetics|Slow drift|
|IDV(14)|Reactor cooling water valve|Sticking|
|IDV(15)|Condenser cooling water valve|Sticking|
|IDV(16)|Unknown|Unknown|
|IDV(17)|Unknown|Unknown|
|IDV(18)|Unknown|Unknown|
|IDV(19)|Unknown|Unknown|
|IDV(20)|Unknown|Unknown|
|IDV(21)|Valve (Stream 4)|Constant position|



##### _4.1.2. Fault types_ 

The description of the fault types is listed in Table 1. According to the difficulty level for faults to detect, they can be roughly divided into three categories as follows. The first includes the faults with large magnitudes: IDV(1), IDV(2), IDV(6)-IDV(8), IDV(12)-IDV(14), IDV(17), IDV(18), which are usually easily detectable. The second contains the faults: IDV(5), IDV(10), IDV(16), IDV(19)-IDV(21), which are relatively difficult to detect and the focus of detection. The third includes IDV(3), IDV(9) and IDV(15). They are incipient faults and usually excluded to be detected, because their mechanisms and modes are extremely complicated [43,44]. In our experiment, their detection results are still given, but they are not adopted for comparison. 

To show the performance and the superiority of the proposed DAEPCA, the TE process and WWTP are employed in our experiment. In this section, the proposed method will be compared with several comparative methods to comprehensively validate the performance in fault detection tasks. 

##### _4.1.3. Dataset_ 

In this simulation, we choose 11 manipulated variables and 22 process variables to form the input matrix **𝐗** . The training dataset and validation dataset are made up of 1168 normal samples and 292 normal samples respectively. For the test dataset, it consists of 21 faulty sets, each of which includes 960 samples, where the first 160 samples are fault-free and the rest are faulty. 

##### _4.1. Tennessee eastman process_ 

##### _4.1.4. Evaluation index_ 

##### _4.1.1. Benchmark_ 

The TE process is a real industrial benchmark which has been widely applied for the simulation and verification of process monitoring methods [41], and its diagram is displayed in Fig. 4. The TE process consists of two variable blocks: one is the XMV block composed by 11 manipulated variables and another is the XMEAS block that comprises 41 measured variables including 22 process variables and 19 analysis variables. Further information of the benchmark can be referred to [42] and the website.<sup>1</sup> 

To evaluate the fault detection performance, two evaluation indexes, including the fault detection rate (FDR) and the false alarm rate (FAR) [32] are adopted in our experiments. A model is considered to be better than another model if its FDR is higher and FAR is lower. 

##### _4.1.5. Comparative method_ 

Comparative methods include KPCA [45], KPCA-KSER [25], DAE [27]. Among these methods, KPCA is a classical kernel-based nonlinear PCA method. KPCA-KSER can be regarded as a kind of fast KPCA approximation method based on the recently proposed KSER technique, which is similar to KPLS-KSER [26]. DAE is a basic deep learning method for feature extraction. 

> 1 http://depts.washington.edu/control/LARRY/TE/download.html. 

7 

_Z. Ren et al._ 

_Journal of Industrial Information Integration 40 (2024) 100622_ 

##### _4.1.6. Model selection_ 

Since both of DAE and DAE-PCA belong to the neural network approaches, a selection strategy should be given to determine which network model is more suitable for the fault detection task among all acquired neural network models. The specific strategy is provided as follow. 

Given the initial values of neural network weights, a selection method to optimal model corresponding to these initial values is proposed through the following way: In each iteration of the network training, a network model will be acquired. When iterations reach _𝑖𝑡𝑒𝑟_ max, the _𝑖𝑡𝑒𝑟_ max models will be obtained. Among these models, the model that has a minimum value of the loss function _𝑙𝑜𝑠𝑠𝐷𝐴𝐸_ − _𝑃𝐶𝐴_ for the validation set is selected as the optimal model corresponding to the current initial values, since it has the best generalization. 

However, under different initial values of neural network weights, the network will learn different local optimal models which may have some differences to some extent in the performance of the fault detection task. Therefore, it is considered to select a more suitable model for the fault detection task among the models respectively obtained from multiple different initial values using the following steps: First, several sets of initial values are randomly generated by using the specified initialization trick. Then, each set of initial values are utilized to train the neural network to obtain their own models. After that, the model corresponding to each set of initial values is applied to the training dataset and the validation dataset (both are composed of normal samples) to obtain the values of the _𝐵𝐼𝐶_ statistics for all samples in these two datasets, and the values of these _𝐵𝐼𝐶_ statistics are summed. Finally, the model with the smallest total sum of the _𝐵𝐼𝐶_ statistics is finally selected as the optimal model for the fault detection task under the designed network structure, because the smaller the value of the _𝐵𝐼𝐶_ statistics, the more the samples of the training dataset and the validation dataset tend to be judged as normal samples. 

##### _4.1.7. Network setting_ 

In neural network structure of DAE-PCA, we utilize ReLU as the activation function. The model parameters are _𝑁_ = 1168, _𝑚_ = 33, _𝑑_ = 33, _𝑎_ = 30, _𝜆_ 1 = ( _𝑁_ × _𝑚_ )<sup>−1</sup> = 2 _._ 6 × 10<sup>−5</sup> , _𝜆_ 2 = ( _𝑁_ × _𝑑_ )<sup>−1</sup> = 2 _._ 6 × 10<sup>−5</sup> . The number of nodes in each layer of the whole neural network is 33-33-30-33-33. The confidence level is _𝛼_ =0 _._ 99. Besides, the Adam algorithm [46] is selected as the optimizer. The maximum _𝑖𝑡𝑒𝑟_ max of training iteration ( _𝑖𝑡𝑒𝑟_ ) is set to 2 × 10<sup>4</sup> and the learning rate ( _𝑙𝑟_ ) is set piecewisely according to _𝑖𝑡𝑒𝑟_ : 


![](Learnable_Faster_Kernel-PCA_for_Nonlinear_Fault_Detection-_Deep_Autoencoder-Based_Realization_(DAE-PCA)_images/conv_90ae2c3db7fdef77.pdf-0008-08.png)


Here, the parameters of other methods are also <u>given.</u> For KPCA, it adopts RBF kernel and kernel parameter is 5√330 (≈90 _._ 83), which is selected by referring to [45,47]. The number of the principal components is 25. The parameters in KPCA-KSER are same as those in KPCA, and the network structure of DAE is the same as that of DAE-PCA. 

##### _4.1.8. Implementation results_ 

The FDRs for 21 faults using all methods are shown in Table 2. For faults in the first category, the FDRs of these four methods are almost over 90% in ,  and . It indicates that all comparative methods receive similar and satisfactory detection results. As for faults in the second category, DAE-PCA have better detection performance for full space than other methods, due to its higher values of FDRs. From the detection results of 18 kinds faults in the first and second categories, the proposed DAE-PCA has a higher FDRs than other methods in 15 kinds of faults, which indicates that DAE-PCA has better generalization ability in detecting different types of faults. In contrast, KPCA-KSER have relatively mediocre fault detection results. The reason for this result is that KPCA-KSER aims to greatly improve the online detection rate, but sacrifices a part of the accuracy of fault detection. In addition, in order to further reflect the average performance of various methods for different faults, Avg. is given as the average of statistics for all 


![](Learnable_Faster_Kernel-PCA_for_Nonlinear_Fault_Detection-_Deep_Autoencoder-Based_Realization_(DAE-PCA)_images/conv_90ae2c3db7fdef77.pdf-0008-12.png)


**Fig. 5.** The online detection time (second) of all methods. Here, the detection time refers to all time of 960 samples in a fault. 

faults in Table 2. Because all methods fail to detect the third category of faults, the calculation of Avg. does not include these faults. The average values of FDRs for the _𝐵𝐼𝐶_ statistics in DAE-PCA method are the highest, which indicates that DAE-PCA method can produce a better mathematical expectation in FDRs. 

Table 4 displays the FARs for 21 faults using all methods. From Table 4, DAE-PCA and KPCA-KSER has the lowest FARs and Avg. of FARs among all nonlinear methods in the full space. The results tell that DAE-PCA is not prone to false alarm for normal samples, thereby reducing manual useless checks. 

To demonstrate that DAE-PCA method is a faster KPCA, the following experiment is given. In Table 3 and Fig. 5, we offer the offline training time and online detection time that are cost by all comparative methods respectively. It can be seen from Table 3 that the neural network methods generally spend more offline training time than the kernel methods, because the training process of the neural network requires a large number of iterative operations. However, in practical applications, there are usually adequate computing resources and time available to train fault detection models. Therefore, we usually do not pay much attention to the offline training time, since it is not an important consideration factor. But the online detection time is an important indicator of real-time performance, so it as a key factor for the quality of the detection method needs to be considered. Fig. 5 lists the online detection time _𝑡_ for all comparative methods. The online detection cost of KPCA is too heavy due to its kernel calculation that makes KPCA hard to apply in real systems. As a much fast KPCA approximation method, KPCA-KSER has the shortest online detection time among all comparative methods, because most operations in its algorithms are linear computation, which makes its online detection time equal to the linear method. DAE-based methods including DAE and DAE-PCA also cost less detection time. Although the detection time of DAE-based methods is slightly higher than that of KPCA-KSER, they can similarly meet the real-time requirements since they avoids the inner product calculation related to the kernel matrix. 

In addition, by calculation, we get<sup>‖</sup> ‖ **𝐏**<sup>_⊤_</sup> **𝐏** − **𝐈** _𝑎_<sup>‖</sup> ‖2 _𝐹_<sup>= 6</sup><sup>_._49 × 10−15from</sup> orthogonal projection matrix **𝐏** . The result demonstrates that the hard constraint given by our PCA module has a quite precise orthogonal property. 

Through the above analysis, we can know that DAE-PCA, as a learnable KPCA, has the same or even better detection results than KPCA and KPCA-KSER for different kinds of faults. Meanwhile, DAE-PCA, also as a faster KPCA, enables to better satisfy the real-time requirements than KPCA. Although the online detection speed of KPCA-KSER is slightly better than that of DAE-PCA, its fault detection accuracy is far worse than our proposed DAE-PCA, or even KPCA. Besides, DAE-PCA has better detection performance than DAE, which suggests the proposed DAE-FE nonlinear framework is much efficient. 

8 

_Z. Ren et al._ 

_Journal of Industrial Information Integration 40 (2024) 100622_ 

**Table 2** 

FDRs (%) of two subspaces  and  as well as the full space  by KPCA, KPCA-KSER, DAE and DAE-PCA in the TE process. In addition, Avg. gives the average of the statistics for the first two categories of faults. The _𝐵𝐼𝐶_ statistics value in bold represents the best performance under the same fault (or Avg.) for all methods. 

|Fault|KPCA|||KPCA-KS|ER||DAE|||DAE-PC|A||
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|No.|||||||||||||
|1|100|99.62|99.75|100|99.25|99.75|100|89.87|100|100|99.87|100|
|2|98.62|98.25|98.62|98.62|98|98.62|98.62|98|98.62|98.62|98|**98.75**|
|6|99.5|100|100|99.5|99.75|99.62|100|100|100|100|100|100|
|7|100|100|100|100|100|100|100|90.25|100|100|99.12|100|
|8|98|98.62|98.62|98|98.62|**98.88**|98.25|91|98.25|98.25|97.75|98.62|
|12|99|99.75|99.75|99|98.55|99.12|99.62|99.75|99.75|99.75|99.75|99.75|
|13|95.25|95|95.25|95.38|94.25|95.25|95.25|93.87|95.25|95.37|94|**95.5**|
|14|100|100|100|100|99.88|100|100|99.87|100|100|99.87|100|
|17|96.75|92.75|96.38|97|84.12|96.38|97.12|87.25|97.12|97.12|82.12|97.12|
|18|90.25|90.38|90.5|90.25|89.62|90|90.5|89.5|90.37|90.62|90.25|**90.75**|
|4|100|92.25|100|100|39.25|100|100|47.75|100|100|92|100|
|5|26.5|100|100|27|31|31.25|99.87|99.75|100|100|9.87|100|
|10|51.88|90.88|**90.25**|53.37|52.25|55.12|89|51.25|88.25|88.87|74|88|
|11|82.5|72.62|81.5|83.12|53.62|79.62|82.62|34.37|82|83.25|57.62|**82.87**|
|16|31.37|96.12|**95.5**|32.75|41.5|40|92.87|53.12|92.5|92.5|89.87|93.25|
|19|64.75|89.5|88|66.12|4.62|56.88|94.37|58.12|93.12|94.5|88.62|**93.75**|
|20|66.62|79.88|79.12|67.38|47.25|66.75|82.37|79.5|83.12|86.25|74.12|**84.62**|
|21|58.75|49.25|56.75|59.25|40.12|55.88|61|40.87|59.62|61|34.37|**60.12**|
|Avg.|81.1|91.38|92.78|81.49|70.64|81.28|93.41|77.89|93.22|93.67|87.29|**93.51**|
|3|4.5|13.75|10.38|4.75|9.38|7.62|8|1.75|5.88|7.5|4|7.38|
|9|3.7|9|6.88|4.12|6.5|5|5.75|2.25|6.5|5.5|2.88|5.5|
|15|10.12|18.38|17|11.38|15.62|14.5|13.25|3.38|12|13.25|5.5|12.63|



###### **Table 3** 

|The offline training time (second) of all methods.|||
|---|---|---|
|Time<br>KPCA<br>KPCA-KSER|DAE|DAE-PCA|
|t∖s<br>5.9984<br>1.9081|215.357|186.562|




![](Learnable_Faster_Kernel-PCA_for_Nonlinear_Fault_Detection-_Deep_Autoencoder-Based_Realization_(DAE-PCA)_images/conv_90ae2c3db7fdef77.pdf-0009-07.png)


probability the sample has to be considered as a faulty sample. From Fig. 6, for faulty samples, KPCA-KPLS fails to detect IDV(5) since the values of its detection statistic _𝐵𝐼𝐶_ are lower than 50%. The statistic _𝐵𝐼𝐶_ values of KPCA and DAE fluctuate between 0.6 and 1, while those of DAE-PCA remain almost constant at 1. Regarding the samples in the normal state, the statistic _𝐵𝐼𝐶_ indexes of all methods are almost below the threshold 0.01. Besides, these four methods all give a fault alarm at the 165th sample without detection delays. 

IDV(19) is a type-unknown fault. From Fig. 7, the detection results of all methods are provided. KPCA-KSER has relatively bad FDRs for statistics _𝐵𝐼𝐶_ in faulty samples, while the performance of KPCA are at an average level. In comparison with other methods, DAE-PCA shows outstanding results since its _𝐵𝐼𝐶_ indexes are almost far above the thresholds and approximate to 1 in most of faulty sample points. For normal samples, all methods are satisfactory and below the thresholds when the samples are free-fault. In detection delays, the delay time of DAE and DAE-PCA has one less sampling time than that of KPCA and KPCA-KSER. 

Through the analysis of the above two faults, it implies that the proposed DAE-PCA has better separable property to handle the binary classification problem that whether the system is in a normal state or a faulty state, because DAE-PCA provides has a larger margin. Furthermore, it also strongly indicates that the kernel learned by DAEPCA is more suitable for fault detection than that obtained by the predetermined kernel method and does not affect the accuracy of fault detection like KPCA-KSER. 

**Fig. 6.** Detection results of Fault IDV(5) in the TE process: (a) KPCA, (b) KPCA-KSER, (c) DAE and (d) DAE-PCA. 

##### _4.2. Wastewater treatment plant_ 

##### _4.2.1. Benchmark_ 

In order to observe the situation of the statistic _𝐵𝐼𝐶_ in  of the sample in each moment, IDV(5) and IDV(19) are selected as the examples to illustrate the efficiency of the proposed DAE-PCA in detail. In this experiment, the detection delay is introduced as the evaluation index of whether the method can detect the fault in time. If five consecutive sample points indicate that the system is in the faulty state, a fault alarm will be raised at the fifth sample point. 

IDV(5) is a step fault and the detection results for it is displayed in Fig. 6. The statistic _𝐵𝐼𝐶_ can approximate the probability that the sample is faulty. The greater the value of statistic _𝐵𝐼𝐶_ is, the greater 

WWTP is a large-scale biochemical chemical system designed to treat wastewater into the water whose quality meets discharge standards. To facilitate the study of WWTP, a standard WWTP simulation model (Benchmark Simulation Model no. 1 (BSM1)) [48] has been developed to evaluate the performance of control strategies for activated sludge plants. WWTP is literally a complex nonlinear system, since the process of WWTP is affected by large perturbations which is caused by the uncertainty of wastewater inlet flow, pollutant load and wastewater composition. Hence, this benchmark has been widely used to assess the effectiveness of nonlinear fault detection methods for industrial processes. 

9 

_Z. Ren et al._ 

_Journal of Industrial Information Integration 40 (2024) 100622_ 

**Table 4** 

FARs (%) of two subspaces  and  as well as the full space  by KPCA, KPCA-KSER, DAE and DAE-PCA in the TE process. In addition, Avg. gives the average of the statistics for the first two categories of faults. 

|Fault|KPCA|||KPCA-K|SER||DAE|||DAE-PC|A||
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|No.|||||||||||||
|1|0.62|0.62|0.62|0.62|0.62|0|1.25|1.88|3.12|0.62|2.5|2.5|
|2|0.62|1.25|0.62|0.62|0|0.62|0.62|0.62|1.25|0.62|0.62|0.62|
|6|0|1.25|0.62|0|0|0|0|2.5|1.88|0|3.12|2.5|
|7|0|0.62|0|0.62|0|0|1.88|0|0.62|1.88|1.88|1.25|
|8|1.88|2.5|0.62|2.5|1.88|1.88|3.75|2.5|3.75|2.5|2.5|3.12|
|12|1.88|7.5|5|1.88|9.38|4.38|1.25|0.62|1.25|1.25|1.25|1.25|
|13|0|0|0|0.62|0.62|0|0|2.5|2.5|0.62|1.25|1.25|
|14|0.62|1.25|1.25|0.62|0|0|1.25|0.62|0.62|1.25|0.62|1.25|
|17|1.25|1.25|1.25|1.88|0.62|0.62|3.12|1.25|2.5|3.12|1.88|0.62|
|18|1.88|0.62|1.25|1.88|0|0.62|2.5|3.12|5|2.5|0.62|2.5|
|4|1.25|1.25|1.25|1.25|0.62|0.62|0.62|0|0.62|0.62|0|0.62|
|5|1.25|1.25|1.25|1.25|0.62|0.62|0.62|0|0.62|0.62|0|0.62|
|10|0.62|0.62|0.62|0.62|0.62|0.62|0.62|1.88|0.62|0.62|3.12|2.5|
|11|1.88|2.5|1.25|1.88|1.25|1.88|1.88|1.25|2.5|1.25|3.12|2.5|
|16|6.25|34.38|29.38|6.88|30|24.38|9.38|0|6.87|9.38|1.88|6.87|
|19|0|0.62|0.62|0|0|0|0.62|3.75|3.75|0.62|2.5|2.5|
|20|0|0.62|0.62|0.62|0|0|0|1.88|0.62|0|2.5|2.5|
|21|4.38|4.38|4.38|4.38|3.12|4.38|5|1.88|5.62|5|4.38|5.62|
|Avg.|1.35|3.47|2.81|1.56|2.74|2.26|1.91|1.46|2.43|1.8|1.87|2.26|
|3|0|7.5|4.38|0|5.62|1.88|3.12|1.88|2.5|4.38|2.5|3.75|
|9|8|21.25|20|9.38|12.5|10.62|11.25|3.12|10.63|11.88|5|11.25|
|15|0|1.88|0|0|0|0|1.88|1.25|1.88|1.88|1.88|2.5|




![](Learnable_Faster_Kernel-PCA_for_Nonlinear_Fault_Detection-_Deep_Autoencoder-Based_Realization_(DAE-PCA)_images/conv_90ae2c3db7fdef77.pdf-0010-05.png)


**Fig. 7.** Detection results of Fault IDV(19) in the TE process: (a) KPCA, (b) KPCA-KSER, (c) DAE and (d) DAE-PCA. 

The BSM1 benchmark is composed of a five-compartment reactor and a secondary settler, and its structure flowchart is shown in Fig. 8. The BSM1 benchmark can be obtained from the website<sup>2</sup> and further information of the benchmark can be referred to its official website.<sup>3</sup> 

##### _4.2.2. Dataset and fault types_ 

According to the literature [49], 18 variables (including 17 variables related to the biological phenomena and 1 variable related to flow rate of secondary settler inlet) are selected to form the input matrix **𝐗** for the process monitoring, which are displayed in Table 5. In this experiment, the dynamic model is implemented with the dynamic dry weather influent data as the input to carry out a simulation under the 

> 2 https://github.com/wwtmodels. 

> 3 http://www.benchmarkwwtp.org. 


![](Learnable_Faster_Kernel-PCA_for_Nonlinear_Fault_Detection-_Deep_Autoencoder-Based_Realization_(DAE-PCA)_images/conv_90ae2c3db7fdef77.pdf-0010-12.png)


**Fig. 8.** Structure flowchart of the BSM1 benchmark plant in WWTP. 

###### **Table 5** 

|Description and notation of the pro|cess variables c|hosen in the WWTP.||
|---|---|---|---|
|Description|Notation|||
||Tank 3|Tank 4|Tank 5|
|Readily biodegradable substrate|_𝑆_S_,_3|_𝑆_S_,_4|_𝑆_S_,_5|
|Oxygen|_𝑆_O_,_3|_𝑆_O_,_4|_𝑆_O_,_5|
|Nitrate and nitrite nitrogen|_𝑆_NO_,_3|_𝑆_NO_,_4|_𝑆_NO_,_5|
|NH<sup>+</sup><br>4 <sup>+ NH3 nitrogen</sup>|_𝑆_NH_,_3|_𝑆_NH_,_4|_𝑆_NH_,_5|
|Alkalinity|_𝑆_ALK_,_3|_𝑆_ALK_,_4|_𝑆_ALK_,_5|
||Settler inlet|Settler underflow|Plant exit|
|Flow rate|_𝑄𝑓_|–|–|
|Nitrate and nitrite nitrogen|–|_𝑆_NO_,𝑢_|_𝑆_NO_,𝑒_|



standard MATLAB-Simulink environment. The data sample interval is 15 min. The training dataset and validation dataset are made up of 672 normal samples and 336 normal samples respectively. For the test dataset, it consists of four faulty sets, each of which includes 1344 samples, where the first 672 samples are fault-free and the rest are faulty. Four types of system faults are designed for this experiment, as shown in Table 6. 

##### _4.2.3. Network setting_ 

In neural network structure of DAE-PCA, LeakyReLU is adopted as the activation function, of which the negative slope parameter is set to 0.001. The model parameters are _𝑁_ = 672, _𝑚_ = 18, _𝑑_ = 18, _𝑎_ = 16, _𝜆_ 1 = ( _𝑁_ × _𝑚_ )<sup>−1</sup> = 8 _._ 3×10<sup>−5</sup> , _𝜆_ 2 = ( _𝑁_ × _𝑑_ )<sup>−1</sup> = 8 _._ 3×10<sup>−5</sup> . The number of nodes in each layer of the whole neural network is 18-18-16-18-18. The 

10 

_Z. Ren et al._ 

_Journal of Industrial Information Integration 40 (2024) 100622_ 

**Table 6** 

Fault types in WWTP. 

|No.|Description|
|---|---|
|Fault 1|The maximum autotrophic growth rate (_𝜇𝐴_) in the whole<br>process is increased from 0_._5 d<sup>−1 </sup>to 0_._8 d<sup>−1</sup>.|
|Fault 2|The oxygen transfer rate in reactor number 3 (_𝐾𝐿𝑎,_3) is<br>decreased by half from 240 d<sup>−1 </sup>to 120 d<sup>−1</sup>.|
|Fault 3|The decay of autotrophs kinetic parameter (_𝑏𝐴_) in the whole<br>process is doubled from 0_._05 d<sup>−1 </sup>to 0_._1 d<sup>−1</sup>.|
|Fault 4|The maximum settling velocity of secondary settler (_𝑣_0<br>′) is<br>decreased by half from 250 m d<sup>−1 </sup>to 125 m d<sup>−1</sup>.|



confidence level is _𝛼_ =0 _._ 99. Besides, the Adam algorithm [46] is selected as the optimizer. The maximum _𝑖𝑡𝑒𝑟_ max of training iteration ( _𝑖𝑡𝑒𝑟_ ) is set to 2 × 10<sup>4</sup> and the learning rate ( _𝑙𝑟_ ) is set piecewisely according to _𝑖𝑡𝑒𝑟_ : 


![](Learnable_Faster_Kernel-PCA_for_Nonlinear_Fault_Detection-_Deep_Autoencoder-Based_Realization_(DAE-PCA)_images/conv_90ae2c3db7fdef77.pdf-0011-06.png)


Here, the parameters of other methods are also given. For KPCA, it adopts RBF kernel and kernel parameter is 30 ~~√~~ 5 (≈67 _._ 08). The number of the principal components is 5. The parameters in KPCA-KSER are same as those in KPCA, and the network structure of DAE is the same as that of DAE-PCA. 

##### _4.2.4. Implementation results_ 

The FDRs for four faults using all methods are shown in Table 7. For Fault 1 and Fault 2, the FDRs for the _𝐵𝐼𝐶_ statistics in these four methods are all over 89% in . It illustrates that they have similar and satisfactory abilities when detecting these two faults. As for Fault 3, KPCA-KSER fails to detect it when the fault occurs in WWTP. KPCA and DAE enables to detect the occurrence of Fault 3, but the detection results are less ideal due to their low FDRs. DAE-PCA receives most outstanding results among all methods and its FDR for the _𝐵𝐼𝐶_ statistics is 84.5% which is far higher than other methods. For this result, a proper analysis is conducted on why DAE-PCA has a more prominent fault detection rate than DAE. DAE directly adopts the features obtained from nonlinear mapping as system features to design the _𝑇_<sup>2</sup> statistics. Different from DAE, DAE-PCA performs PCA decomposition on the features obtained from nonlinear mapping, which makes the features used to design the _𝑇_<sup>2</sup> statistics orthogonal to each other. Thus, the features extracted from DAE-PCA can better characterize the state of the system than those from DAE. For the faults that are difficult to detect, such as Fault 3, DAE-PCA enables to better distinguish them from the normal state in comparison to DAE. While for faults that are relatively easy to detect, such as Fault 1 and Fault 2, both DAEPCA and DAE have satisfactory fault detection results. When detecting Fault 4, DAE and DAE-PCA have well detection results since their BIC statistics have FDRs of 84%, which is higher than the 62% of KPCA and KPCA-KSER. From Avg. in Table 7, the average values of FDRs for the _𝐵𝐼𝐶_ statistics in DAE-PCA method are significantly higher than other comparative methods, which indicates that DAE-PCA method can produce a better mathematical expectation in FDRs. Table 8 shows the FARs for normal samples using all methods. From Table 8, DAE-PCA has the lowest FARs. The results indicate that false alarm for normal samples rarely happens when using DAE-PCA. 

By combining the above results, it can be discovered that DAE-PCA, as a learnable KPCA, enables to find the nonlinear feature space that is more suitable for distinguishing the faulty state from the normal state, which makes DAE-PCA provide more accurate fault detection results than other comparative methods. Moreover, DAE-PCA also has a good ability to efficiently perform real-time online fault detection. As shown from Fig. 9, DAE-PCA has faster online computation rate compared with KPCA. Although offline training time is not considered as an evaluation factor in fault detection task, it is also given in the Table 9 for comprehensive understanding. 


![](Learnable_Faster_Kernel-PCA_for_Nonlinear_Fault_Detection-_Deep_Autoencoder-Based_Realization_(DAE-PCA)_images/conv_90ae2c3db7fdef77.pdf-0011-11.png)


**Fig. 9.** The online detection time (second) of all methods. Here, the detection time refers to all time of 1344 samples in a fault. 


![](Learnable_Faster_Kernel-PCA_for_Nonlinear_Fault_Detection-_Deep_Autoencoder-Based_Realization_(DAE-PCA)_images/conv_90ae2c3db7fdef77.pdf-0011-13.png)


**Fig. 10.** Detection results of Fault 3 in the TE process: (a) KPCA, (b) KPCA-KSER, (c) DAE and (d) DAE-PCA. 

Further, Fault 3 and Fault 4 are chosen to observe the situation of the statistics _𝐵𝐼𝐶_ in  of the sample in each moment. 

The detection results for Fault 3 is displayed in Fig. 10. When Fault 3 occurs in WWTP, most of the values of the _𝐵𝐼𝐶_ statistics of KPCA and KPCA-KSER fluctuate around the threshold. It demonstrates that these two methods both give low probabilities for the event that the fault samples are judged to be in the faulty state. In addition, KPCA gives false alarms between the 607th sample and the 613th sample, as well as in the 619th sample, while KPCA-KSER gives false alarms between the 604th sample and the 613th sample. These large numbers of false alarms seriously could mislead workers into believing that the normal system has existed the Fault 3, thereby fraying the bond of trust between workers and fault detection methods. DAE offers relatively mediocre detection results, because only a part of its _𝐵𝐼𝐶_ statistics values are far above the threshold, yet many of them below the threshold. For the proposed DAE-PCA, the values of its _𝐵𝐼𝐶_ statistics are larger than the threshold in a majority of fault samples. The results obviously reflect that the accuracy of DAE-PCA is higher than that of other methods in terms of detecting Fault 3. In the aspect of detection delay, DAE-PCA enables to raise a fault alarm for Fault 3 1.5 h earlier than DAE, and 3 h earlier than KPCA and KPCA-KSER, which leaves more time for workers to troubleshoot. 

11 

_Z. Ren et al._ 

_Journal of Industrial Information Integration 40 (2024) 100622_ 

**Table 7** 

FDRs (%) of two subspaces  and  as well as the full space  by KPCA, KPCA-KSER, DAE and DAE-PCA in WWTP. In addition, Avg. gives the average of the statistics for the first two categories of faults. The _𝐵𝐼𝐶_ statistics value in bold represents the best performance under the same fault (or Avg.) for all methods. 

|Fault|KPCA|||KPCA-KS|ER||DAE|||DAE-PCA|||
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|No.|||||||||||||
|Fault 1|90.61|90.46|97.76|90.46|14.75|89.72|95.53|100|100|90.91|100|100|
|Fault 2|89.87|100|**100**|89.87|21.16|89.57|100|100|100|99.85|100|100|
|Fault 3|34.87|53.35|56.63|34.72|0|33.83|48.88|67.51|66.17|48.58|86.44|**84.5**|
|Fault 4|64.68|28.32|61.85|63.93|2.83|62|65.57|83.9|83.9|66.62|84.8|**84.35**|
|Avg.|70.01|68.03|79.06|69.75|9.69|68.78|77.5|87.85|87.52|76.49|92.81|**92.21**|



###### **Table 8** 

FARs (%) of two subspaces  and  as well as the full space  by KPCA, KPCA-KSER, DAE and DAE-PCA in WWTP. In addition, the _𝐵𝐼𝐶_ statistics value in bold represents the best <u>performance</u> for all methods. 

|Fault|KPCA|||KPCA-KS|ER||DAE|||DAE-P|CA||
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|No.|||||||||||||
|Normal samples|3.27|1.78|2.97|3.12|1.78|2.23|1.04|0.89|1.49|1.04|1.04|**1.19**|



###### **Table 9** 

##### **5. Conclusion** 

The offline training time (second) of all methods. 

|Time|KPCA|KPCA-KSER|DAE|DAE-PCA|
|---|---|---|---|---|
|t∖s|1.048|0.5803|168.0466|175.0997|




![](Learnable_Faster_Kernel-PCA_for_Nonlinear_Fault_Detection-_Deep_Autoencoder-Based_Realization_(DAE-PCA)_images/conv_90ae2c3db7fdef77.pdf-0012-12.png)


**Fig. 11.** Detection results of Fault 4 in the TE process: (a) KPCA, (b) KPCA-KSER, (c) DAE and (d) DAE-PCA. 

Fig. 11 shows the relationship between the value of _𝐵𝐼𝐶_ statistics and the threshold in each sample when detecting Fault 4 by all comparative methods. It is obvious that when Fault 4 occurs in the system, the _𝐵𝐼𝐶_ statistics of DAE and DAE-PCA have much larger values than the threshold, so these two methods offer more reliable detection results by compared with KPCA and KPCA-KSER. In the terms of detection delay, DAE-PCA enables to raise a fault alarm for Fault 4 16.25 h earlier than KPCA, 17 h earlier than KPCA-KSER, and 21 h earlier than KPCA. Hence, DAE-PCA is more timely in detecting faults. 

According to the above detection results for two kinds of fault in WWTP, DAE-PCA has higher fault detection accuracy by contrast with KPCA, KPCA-KSER and DAE. Moreover, DAE-PCA is more sensitive to monitor different kinds of faults, which is conducive to timely discovering the faults or failures. Therefore, DAE-PCA as a learnable and fast KPCA method is quite competitive in fault detection tasks. 

In this paper, we present a DAE-PCA method based on a nonlinear DAE-FE framework that provides a way to transform a linear approach into the corresponding nonlinear version for fault detection tasks. The DAE-FE framework has been proven to equal to a corresponding learnable and faster kernel trick. In the case of fixed neural network structure, DAE-FE can automatically learn network weights that function similarly as the kernel parameters. Under this framework, we further design DAE-FE framework to put forward a DAE-PCA approach. Owing to Cayley Transform, the orthogonal projection matrix of PCA module in DAE-PCA method is guaranteed by hard constraints, which is implemented by the network structure. In comparison with KPCA, the proposed DAE-PCA has the ability to automatically learn an optimal parameter and has the faster computational efficiency. Through the experiment, the effectiveness of the proposed approach has been validated by detecting the faults in the TE process and WWTP. In future, the research will focus on how to modify DAE-PCA to be competent for the detection of incipient faults, such as IDV(3), IDV(9) and IDV(15) in the TE process. Besides, DAE-PCA will be further improved to achieve multi-level feature learning, similar to DePCA [20] and DKPCA [21]. 

##### **CRediT authorship contribution statement** 

**Zelin Ren:** Conceptualization, Data curation, Formal analysis, Methodology, Software, Validation, Writing – original draft, Writing – review & editing. **Yuchen Jiang:** Investigation, Writing – review & editing, Visualization. **Xuebing Yang:** Visualization, Writing – review & editing. **Yongqiang Tang:** Writing – review & editing. **Wensheng Zhang:** Resources, Supervision. 

##### **Declaration of competing interest** 

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper. 

##### **Data availability** 

Data will be made available on request. 

##### **Acknowledgments** 

This work was supported in part by National Natural Science Foundation of China under Grant 62203143, and Heilongjiang Provincial Projects under Grants LJYXL2022-047, LBH-Z22130. 

12 

_Z. Ren et al._ 

_Journal of Industrial Information Integration 40 (2024) 100622_ 

##### **References** 

- [1] Z. Gao, C. Cecati, S.X. Ding, A survey of fault diagnosis and fault-tolerant techniques—part II: fault diagnosis with knowledge-based and hybrid/active approaches, IEEE Trans. Ind. Electron. 62 (6) (2015) 3768–3774. 

- [2] Z. Huo, M. Martínez-García, Y. Zhang, R. Yan, L. Shu, Entropy measures in machine fault diagnosis: insights and applications, IEEE Trans. Instrum. Meas. 69 (6) (2020) 2607–2620. 

- [3] K. Peng, K. Zhang, B. You, J. Dong, Z. Wang, A quality-based nonlinear fault diagnosis framework focusing on industrial multimode batch processes, IEEE Trans. Ind. Electron. 63 (4) (2016) 2615–2624. 

- [4] Y. Jiang, S. Yin, J. Dong, O. Kaynak, A review on soft sensors for monitoring, control and optimization of industrial processes, IEEE Sens. J. 21 (11) (2021) 12868–12881. 

- [5] E. Naderi, K. Khorasani, A data-driven approach to actuator and sensor fault detection, isolation and estimation in discrete-time linear systems, Automatica 85 (2017) 165–178. 

- [6] I. Lomov, M. Lyubimov, I. Makarov, L.E. Zhukov, Fault detection in Tennessee eastman process with temporal deep learning models, J. Ind. Inf. Integr. 23 (2021) 100216. 

- [7] H. Chen, Z. Liu, C. Alippi, B. Huang, D. Liu, Explainable intelligent fault diagnosis for nonlinear dynamic systems: From unsupervised to supervised learning, IEEE Trans. Neural Netw. Learn. Syst. (2022) http://dx.doi.org/10.1109/TNNLS.2022. 3201511. 

- [8] J. Liu, J. Wu, Y. Xie, W. Jie, P. Xu, Z. Tang, H. Yin, Toward robust process monitoring of complex process industries based on denoising sparse auto-encoder, J. Ind. Inf. Integr. 30 (2022) 100410. 

- [9] H. Chen, L. Li, C. Shang, B. Huang, Fault detection for nonlinear dynamic systems with consideration of modeling errors: A data-driven approach, IEEE Trans. Cybern. (2022) http://dx.doi.org/10.1109/TCYB.2022.3163301. 

- [10] Q. Jiang, S. Chen, X. Yan, M. Kano, B. Huang, Data-driven communication efficient distributed monitoring for multiunit industrial plant-wide processes, IEEE Trans. Autom. Sci. Eng. 19 (3) (2022) 1913–1923. 

- [11] Q. Jiang, J. Jiang, W. Zhong, X. Yan, Optimized gaussian-process-based probabilistic latent variable modeling framework for distributed nonlinear process monitoring, IEEE Trans. Syst. Man Cybern.: Syst. 53 (5) (2023) 3187–3198. 

- [12] B. Schölkopf, A.J. Smola, K.R. Müller, Nonlinear component analysis as a kernel eigenvalue problem, Neural Comput. 10 (5) (1998) 1299–1319. 

- [13] Z. Ge, C. Yang, Z. Song, Improved kernel PCA-based monitoring approach for nonlinear processes, Chem. Eng. Sci. 64 (9) (2009) 2245–2255. 

- [14] Q. Jiang, X. Yan, B. Huang, Review and perspectives of data-driven distributed monitoring for industrial plant-wide processes, Ind. Eng. Chem. Res. 58 (29) (2019) 12899–12912. 

- [15] S. Yin, X. Li, H. Gao, O. Kaynak, Data-based techniques focused on modern industry: an overview, IEEE Trans. Ind. Electron. 62 (1) (2015) 657–667. 

- [16] K. Zhang, K. Peng, R. Chu, J. Dong, Implementing multivariate statisticsbased process monitoring: A comparison of basic data modeling approaches, Neurocomputing 290 (2018) 172–184. 

- [17] K. Zhang, B. Tang, L. Deng, X. Yu, Fault detection of wind turbines by subspace reconstruction-based robust kernel principal component analysis, IEEE Trans. Instrum. Meas. 70 (2021). 

- [18] F. Simmini, M. Rampazzo, F. Peterle, G.A. Susto, A. Beghi, A self-tuning KPCAbased approach to fault detection in chiller systems, IEEE Trans. Control Syst. Technol. 30 (4) (2022) 1359–1374. 

- [19] X. Deng, X. Tian, S. Chen, C.J. Harris, Nonlinear process fault diagnosis based on serial principal component analysis, IEEE Trans. Neural Netw. Learn. Syst. 29 (3) (2018) 560–572. 

- [20] X. Deng, X. Tian, S. Chen, C.J. Harris, Deep principal component analysis based on layerwise feature extraction and its application to nonlinear process monitoring, IEEE Trans. Control Syst. Technol. 27 (6) (2018) 2526–2540. 

- [21] F. Tonin, Q. Tao, P. Patrinos, J.A.K. Suykens, Deep kernel principal component analysis for multi-level feature learning, 2023, arxiv preprint arxiv:2302.11220. 

- [22] R. Fezai, M. Mansouri, O. Taouali, M.F. Harkat, N. Bouguila, Online reduced kernel principal component analysis for process monitoring, J. Process Control 61 (2018) 1–11. 

- [23] R. Fezai, M. Mansouri, M. Trabelsi, M. Hajji, H. Nounou, M. Nounou, Online reduced kernel GLRT technique for improved fault detection in photovoltaic systems, Energy 179 (2019) 1133–1154. 

- [24] J.P. Ryan, S.E. Ament, C.P. Gomes, A. Damle, The fast kernel transform, in: International Conference on Artificial Intelligence and Statistics, PMLR, 2022, pp. 11669–11690. 

- [25] G. Wang, J. Jiao, S. Yin, Efficient nonlinear fault diagnosis based on kernel sample equivalent replacement, IEEE Trans. Ind. Inform. 15 (5) (2019) 2682–2690. 

- [26] J. Jiao, W. Zhen, G. Wang, Y. Wang, KPLS–KSER based approach for quality-related monitoring of nonlinear process, ISA Trans. 108 (2021) 144–153. 

- [27] M. Sakurada, T. Yairi, Anomaly detection using autoencoders with nonlinear dimensionality reduction, in: Proceedings of the MLSDA 2014 2nd Workshop on Machine Learning for Sensory Data Analysis, 2014, pp. 4–11. 

- [28] I. Ahmed, T. Galoppo, X. Hu, Y. Ding, Graph regularized autoencoder and its application in unsupervised anomaly detection, IEEE Trans. Pattern Anal. Mach. Intell. 44 (8) (2022) 4110–4124. 

- [29] A. Creswell, A.A. Bharath, Denoising adversarial autoencoders, IEEE Trans. Neural Netw. Learn. Syst. 30 (4) (2019) 968–984. 

- [30] S. Chen, Q. Jiang, Distributed robust process monitoring based on optimized denoising autoencoder with reinforcement learning, IEEE Trans. Instrum. Meas. 71 (2022) 1–11. 

- [31] P. Tang, K. Peng, J. Dong, Nonlinear quality-related fault detection using combined deep variational information bottleneck and variational autoencoder, ISA Trans. 114 (2021) 444–454. 

- [32] K. Jang, S. Hong, M. Kim, J. Na, I. Moon, Adversarial autoencoder-based feature learning for fault detection in industrial processes, IEEE Trans. Ind. Inform. 18 (2) (2022) 827–834. 

- [33] M. Rao, M.J. Zuo, Z. Tian, A speed normalized autoencoder for rotating machinery fault detection under varying speed conditions, Mech. Syst. Signal Process. 189 (2023). 

- [34] A. Cayley, Sur quelques propriétés des déterminants gauches, J. Reine Angew. Math. 32 (1846) 119–123. 

- [35] B.M. Wise, N. Ricker, D.V. eltkamp, B.R. Kowalski, A theoretical basis for the use of principal component models for monitoring multivariate processes, Process Control Qual. 1 (1) (1990) 41–51. 

- [36] M. Mohri, A. Rostamizadeh, A. Talwalkar, Foundations of Machine Learning, MIT Press, 2018. 

- [37] S. Ioffe, S.C. Szegedy, Batch normalization: Accelerating deep network training by reducing internal covariate shift, in: International Conference on Machine Learning, PMLR, 2015, pp. 448–456. 

- [38] E. Parzen, On estimation of a probability density function and mode, Ann. Math. Stat. 33 (3) (1962) 1065–1076. 

- [39] Z. Ge, M. Zhang, Z. Song, Nonlinear process monitoring based on linear subspace and Bayesian inference, J. Process Control 20 (5) (2010) 676–688. 

- [40] J. Huang, X. Yan, Quality-driven principal component analysis combined with kernel least squares for multivariate statistical process monitoring, IEEE Trans. Control Syst. Technol. 27 (6) (2019) 2688–2695. 

- [41] L.H. Chiang, E.L. Russell, R.D. Braatz, Fault Detection and Diagnosis in Industrial Systems, Springer Science & Business Media, 2000. 

- [42] J.J. Downs, E.F. Vogel, A plant-wide industrial process control problem, Comput. Chem. Eng. 17 (3) (1993) 245–255. 

- [43] Y. Wang, Z. Pan, X. Yuan, C. Yang, W. Gui, A novel deep learning based fault diagnosis approach for chemical process with extended deep belief network, ISA Trans. 96 (2020) 457–467. 

- [44] Y. Zhang, Enhanced statistical analysis of nonlinear processes using KPCA, KICA and SVM, Chem. Eng. Sci. 64 (5) (2009) 801–811. 

- [45] J.-M. Lee, C. Yoo, S.W. Choi, P.A. Vanrolleghem, I.-B. Lee, Nonlinear process monitoring using kernel principal component analysis, Chem. Eng. Sci. 59 (1) (2004) 223–234. 

- [46] D.P. Kingma, B. Jimmy, Adam: A method for stochastic optimization, Comput. Sci. (2014). 

- [47] L. Shang, K. Shi, C. Ma, A. Qiu, L. Hua, Fault detection and identification based on explicit polynomial mapping and combined statistic in nonlinear dynamic processes, IEEE Access 9 (2021) 149050-149066. 

- [48] J. Alex, L. Benedetti, J.B. Copp, J.P. Steyer, Benchmark simulation model no. 1 (BSM1), in: Report by the IWA Taskgroup on Benchmarking of Control Strategies for WWTPs, 2008. 

- [49] B. Wang, Z. Li, Z. Dai, N. Lawrence, X. Yan, Data-driven mode identification and unsupervised fault detection for nonlinear multimode processes, IEEE Trans. Ind. Inform. 16 (6) (2019) 3651–3661. 

13 

