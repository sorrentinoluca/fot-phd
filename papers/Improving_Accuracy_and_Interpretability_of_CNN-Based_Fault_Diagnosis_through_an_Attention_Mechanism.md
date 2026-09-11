**_processes_** 


![](Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism_images/Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism.pdf-0001-01.png)



![](Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism_images/Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism.pdf-0001-02.png)


## _Article_ 

# **Improving Accuracy and Interpretability of CNN-Based Fault Diagnosis through an Attention Mechanism** 

## **Yubiao Huang**<sup>**1,2,3**</sup> **, Jiaqing Zhang**<sup>**1,2,3,**</sup> ***, Rui Liu**<sup>**1,2,3**</sup> **and Shuangyao Zhao**<sup>**4,**</sup> ***** 

- 1 Anhui Province Key Laboratory for Electric Fire and Safety Protection, Hefei 230601, China; firelab_huang@163.com (Y.H.); gwliur@163.com (R.L.) 

- 2 State Grid Laboratory of Fire Protection for Transmission and Distribution Facilities, Hefei 230601, China 3 State Grid Anhui Electric Power Research Institute, Hefei 230601, China 

- 4 

   - School of Management, Hefei University of Technology, Hefei 230009, China 

- Correspondence: dkyzjq@163.com (J.Z.); zsyjiu91@hfut.edu.cn (S.Z.) 

**Citation:** Huang, Y.; Zhang, J.; Liu, R.; Zhao, S. Improving Accuracy and Interpretability of CNN-Based Fault Diagnosis through an Attention Mechanism. _Processes_ **2023** , _11_ , 3233. https://doi.org/10.3390/ pr11113233 

Academic Editors: Yi Man, Sheng Yang, Yusha Hu and Jie Zhang 

Received: 10 October 2023 Revised: 5 November 2023 Accepted: 6 November 2023 Published: 16 November 2023 


![](Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism_images/Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism.pdf-0001-14.png)


**Copyright:** © 2023 by the authors. Licensee MDPI, Basel, Switzerland. This article is an open access article distributed under the terms and conditions of the Creative Commons Attribution (CC BY) license (https:// creativecommons.org/licenses/by/ 4.0/). 

**Abstract:** This study aims to enhance the accuracy and interpretability of fault diagnosis. To address this objective, we present a novel attention-based CNN method that leverages image-like data generated from multivariate time series using a sliding window processing technique. By representing time series data in an image-like format, the spatiotemporal dependencies inherent in the raw data are effectively captured, which allows CNNs to extract more comprehensive fault features, consequently enhancing the accuracy of fault diagnosis. Moreover, the proposed method incorporates a form of prior knowledge concerning category-attribute correlations into CNNs through the utilization of an attention mechanism. Under the guidance of thisprior knowledge, the proposed method enables the extraction of accurate and predictive features. Importantly, these extracted features are anticipated to retain the interpretability of the prior knowledge. The effectiveness of the proposed method is verified on the Tennessee Eastman chemical process dataset. The results show that proposed method achieved a fault diagnosis accuracy of 98.46%, which is significantly higher than similar existing methods. Furthermore, the robustness of the proposed method is analyzed by sensitivity analysis on hyperparameters, and the interpretability is revealed by visually analyzing its feature extraction process. 

**Keywords:** fault diagnosis; deep learning; convolutional neural network; prior knowledge; attention mechanism 

## **1. Introduction** 

Fault diagnosis serves as a crucial technology to ensure the normal operation of industrial activities. Over recent years, there has been a surge in the popularity of data-driven fault diagnosis methods [1–7] due to the convenient and cost-effective collection of realtime time series data. Among these methods, those based on deep learning (DL) [2,4–7] have gained significant attention and achieved remarkable outcomes, primarily because of their superior feature extraction capabilities. DL architectures, such as deep belief networks (DBN) [8], recurrent neural networks (RNN) [9], and convolutional neural networks (CNN) [2,10], have been applied in fault diagnosis research. Notably, CNN has emerged as the most widely used DL architecture in fault diagnosis, owing to its ability to extract complex high-dimensional features. 

Most of the existing DL-based methods focus on how to obtain higher fault diagnosis accuracy. They achieve this goal by increasing the number of network layers [7] or adopting a hybrid network structure [11,12]. However, these methods are prone to overfitting when the data are limited. In particular, data scarcity poses a significant challenge in the field of fault diagnosis. On one hand, collecting an adequate amount of fault data is often impractical due to limitations such as machines or systems not being allowed or able to operate in a fault state for an extended period. On the other hand, generating fault 

_Processes_ **2023** , _11_ , 3233. https://doi.org/10.3390/pr11113233 

https://www.mdpi.com/journal/processes 

2 of 21 

_Processes_ **2023** , _11_ , 3233 

data through simulation is a costly endeavor. To this end, some additional tricks, such as residual connection [13], data augmentation [14], pre-training [2], and meta-transfer learning [15], have been used to achieve high accuracy in the case of data scarcity. For example, Yu et al. (2022) developed a six-layer residual neural network for fault diagnosis and showed that it effectively enhances the accuracy of fault diagnosis [13]. Li et al. (2020) used data augmentation technology to artificially create additional valid data, which helped the DL-based approach to be able to cope with complex fault diagnosis with limited data [14]. Feng et al. (2020) proposed a novel domain-knowledge-based deep-broad learning framework to address the data scarcity problem in fault diagnosis, where a CNNbased feature extractor was pre-trained with the use of bridge labels [2]. Li et al. (2023) developed an attention-based deep meta-transfer learning method that is able to cope with the few-shot fine-grained fault diagnosis problem [15]. 

In addition to accuracy, interpretability is another significant concern of fault diagnosis methods. The outcome of fault diagnosis carries immense significance, and any inaccuracies in the results can lead to substantial losses. Consequently, ensuring the reliability of fault diagnosis results typically necessitates interpretability in the fault diagnosis method. However, data-driven approaches, particularly DL, are often referred to as “black box” methods that inherently lack interpretability. As a result, applying these approaches to real-world fault diagnosis scenarios becomes challenging. In recent years, researchers have started to pay attention to this issue, and have proposed several solutions. The first one is to employ visualization techniques, such as neuron activation maximization [16] and class activation mapping (CAM) [17], to analyze the features learned by DL models [18]. These visualization techniques can help us clearly investigate what DL models have learned. The second one is to incorporate interpretable prior knowledge into DL models [19,20]. For instance, Yu and Liu (2020) introduced a knowledge-based DBN that successfully incorporated confidence and classification rules into the DBN, leading to enhanced model interpretability [19]. The third approach is to utilize attention mechanisms [18,21,22]. For instance, Li et al. (2019) applied the attention mechanism to understand and improve DL-based fault diagnosis of rolling bearing [18]. 

The existing studies on ways to improve fault diagnosis accuracy or interpretability are shown in Table 1. It is demonstrated that enhancing the accuracy of DL-based fault diagnosis methods generally necessitates an increase in model complexity. This might involve augmenting network layers or employing hybrid network architectures, among other strategies. However, such enhancements may inadvertently compromise model interpretability, which runs counter to our ultimate objective. Conversely, when striving to enhance interpretability, it is essential to incorporate supplementary elements like attention mechanisms and the integration of prior knowledge. It is noteworthy that prior studies [18,21,22] have underscored the capacity of attention mechanisms to enhance fault diagnosis accuracy. Nevertheless, these studies failed to explore the potential benefits of prior knowledge integration. Consequently, this study aims to bridge this research gap by leveraging the attention mechanism to integrate prior knowledge, thereby concurrently enhancing both the accuracy and interpretability of fault diagnosis. 

**Table 1.** Existing ways to improve fault diagnosis accuracy or interpretability. 

|**Study**|**Accuracy**|**Interpretability**|
|---|---|---|
|Jia et al. [7]|Through a deeper network|/|
|Huang et al. [11], Xu et al. [12]|<br>Through a hybrid network|/|
|Li et al. [18]|/|Through visualization techniques|
|Yu and Liu [19], Xie et al. [20]|/|Through prior knowledge integration|
|Li et al. [18], Liao et al. [21], Peng et al. [22]|/|Through attention mechanisms|



In this study, we focus on both the accuracy and interpretability of fault diagnosis. First, we used the sliding window method [11] to obtain the image-like data for constructing a CNN-based model. The obtained image-like data integrates the spatiotemporal dependence 

3 of 21 

_Processes_ **2023** , _11_ , 3233 

in the raw time series data so that the CNN is able to extract more abundant fault features, thereby improving the accuracy of fault diagnosis. Then, a kind of prior knowledge about the correlation between faults and attributes is formally defined based on the image-like data. Finally, the defined prior knowledge is integrated into the CNN based on an attention mechanism. In this way, accurate and predictive features can be extracted under the guidance of the defined prior knowledge. Moreover, the extracted features are expected to inherit the interpretability of the prior knowledge. In summary, the main contributions of this study lie in the definition of prior knowledge about category–attribute correlation and the integration of prior knowledge based on an attention mechanism. 

The effectiveness and efficiency of the proposal were verified in the TE chemical process dataset [23]. The results show that the proposal significantly outperforms traditional data-driven, as well as recent DL-based, fault diagnosis methods in terms of accuracy. Moreover, the feature extraction process of the attention-based CNN model was analyzed by visualization techniques, which demonstrates its interpretability. 

The rest of this paper is organized as follows. In Section 2, related works of CNN variants that are also able to fuse prior knowledge are presented. Section 3 introduces some basic knowledge about CNN and sliding window processes. Section 4 presents the proposed attention-based CNN method for fault diagnosis. In Section 5, the implementation of the proposed method to deal with the fault diagnosis of the TE chemical process is illustrated with analysis and discussion of results. Finally, conclusions and future work are provided in Section 6. 

## **2. Related Works** 

To highlight the novelty of the proposed attention-based CNN, this section introduces related CNN variants that are also able to fuse prior knowledge, similar to the proposed one. 

## _2.1. Region Proposals Convolutional Neural Networks_ 

In the field of object detection, region proposals convolutional neural networks (RCNNs) are a widely-used class of CNNs [24–27]. The core idea of R-CNNs is to combine region proposals generated by a particular region proposal method, such as selective search [28], with CNNs. The region proposals preliminarily locate the region of objects, which provides CNNs with informative data regions for feature extraction. As can be seen, the function of the region proposals is similar to that of the defined prior knowledge about the correlation between faults and attributes, which shows the consistency of core ideas between R-CNNs and the proposed method. Nevertheless, acquisition methods of the prior knowledge and the region proposals are completely different. Furthermore, the region proposals are directly used as the input of CNNs for feature extraction, while in this study the defined prior knowledge about the correlation between faults and attributes can be integrated into any layer of CNN, which enables deeper and more flexible integration of prior knowledge. 

## _2.2. Mask-Based Convolutional Neural Networks_ 

Mask-based convolutional neural networks (MCNNs) are a class of CNNs used to avoid background noise, and have been applied to person retrieval [29]. In MCNNs, a latent binary mapping of the raw data is first learned by a specific neural network, such as the fully convolutional network [29] or the U-net [30]. The learned latent binary mapping extracts regions of interest from the raw data that contain informative signals for subsequent tasks, which is similar to the prior knowledge defined in this study. After that, the so-called masked data obtained by the operation of element-wise product between the learned latent binary mapping and the raw data is directly used as the input of CNNs for feature extraction. Although both MCNNs and the proposed method achieve the location of informative region of the raw data, the former does not realize the coupling of the learned latent binary mapping with any layer of CNN. 

4 of 21 

_Processes_ **2023** , _11_ , 3233 

## _2.3. Squeeze-and-Excitation Networks_ 

Squeeze-and-excitation (SE) networks are developed by stacking a novel architectural unit, the SE block, which achieves excellent results on a variety of tasks such as face recognition [31] and image classification [32]. The SE block is used to selectively highlight informative channel-wise features by explicitly modeling interdependencies between channels of its intermediate features [33]. More specifically, two steps, namely squeeze and excitation, are involved in the calculation process of the SE block, where squeeze uses global average pooling to generate channel-wise statistics for exploiting channel dependencies and excitation adopts a simple gating mechanism with a sigmoid activation to make use of the information aggregated in the step of squeeze. The gating mechanism results in additional network parameters, thus adding computational cost. Conversely, the proposed method, which also has a flexible architectural unit for capturing informative data region, namely the attention module, is constructed without any parameters. 

## **3. Basic Knowledge** 

This section presents basic knowledge needed for subsequent discussions, such as convolutional neural networks and sliding window processing. 

## _3.1. Convolutional Neural Networks_ 

CNNs were originally proposed by Krizhevsky et al. (2012) for image recognition [34]. Now, CNNs have become the cornerstone of DL. A CNN generally consists of a feature extractor and a classifier, where the feature extractor is composed of certain stacked convolutional and pooling layers. In a convolutional layer, the input undergoes convolution with a trainable kernel, followed by the operation of an activation function to produce the output. The input or output is a set of feature maps denoted as _X_ = [ _X_ 1, . . . , _Xi_ , . . . , _Xn_ ], where _Xi ∈ R_<sup>_w×h_</sup> ( _i_ = 1, . . . , _n_ ) is called a feature map with size ( _w_ , _h_ ). Assuming that _X_<sup>_in_</sup> denotes the input with _m_ feature maps, _X_<sup>_out_</sup> denotes the output with _n_ feature maps, and _K_ = � _K_ 1, . . . , _Kj_ , . . . , _Kn_ � denotes the convolutional kernel that is composed of _n_ filters _Kj ∈ R_<sup>_k×l_</sup> ( _j_ = 1, . . . , _n_ ) with size ( _k_ , _l_ ), the operation of a convolutional layer is shown in the following formula: 


![](Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism_images/Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism.pdf-0004-08.png)


where _bj_ denotes the bias corresponding to the _j_ th filter _Kj_ , _f_ ( _·_ ) denotes a nonlinear activation function (e.g., the rectified linear unit), and _∗_ denotes the convolutional operation. After a convolutional layer, a pooling layer produces a down sampled version of the obtained feature maps. 

The classifier seeks to classify samples into corresponding categories according to the feature maps extracted by the feature extractor. The classifier generally consists of some stacked fully connected (FC) layers and a final softmax operation. The feature maps are compressed into a feature vector as the inputs of the first FC layer. A softmax operation is applied to the output of the last FC layer to obtain the category probability vector. 

## _3.2. Sliding Window Processing_ 

Fault diagnosis typically utilizes raw data in the form of time series, which can be categorized into two types: univariate time series (UTS) and multivariate time series (MTS) [35]. A UTS _ST_ = [ _s_ 1, . . . , _st_ , . . . , _sT_ ] is a vector with elements in chronological order, where _T_ denotes the length. A _K_ -dimensional MTS _ST_<sup>_K_= [</sup><sup>_ST_(</sup><sup>_c_1), . . . ,</sup><sup>_ST_(</sup><sup>_ck_), . . . ,</sup><sup>_ST_(</sup><sup>_cK_)] is a matrix,</sup> where _ST_ ( _ck_ ) denotes an UTS associated with the attribute _ck ∈ C_ = _{ck|k_ = 1, . . . , _K}_ . In this study, the raw data used for fault diagnosis are denoted as a _K_ -dimensional MTS _ST_<sup>_K_.</sup> However, _ST_<sup>_K_generally cannot be directly used as the input of DL-based fault diagnosis</sup> method due to the fact that _T_ is usually very large and the formalism of _ST_<sup>_K_cannot meet the</sup> input requirements of the developed fault diagnosis method. To this end, a certain data 

5 of 21 

_Processes_ **2023** , _11_ , 3233 

transformation method is required to obtain data samples that meet the input requirements of the developed fault diagnosis method from _ST_<sup>_K_.</sup> 

In this study, we use the sliding window processing (SWP) [11] to obtain samples from _S_<sup>_K_Since we are constructing a fault diagnosis model using CNNs, the input data format</sup> _T_<sup>.</sup> should be image-like; that is, the samples obtained from _ST_<sup>_K_by SWP should be image-like.</sup> More specifically, the image-like samples are obtained by simultaneously performing SWP on the raw time series _ST_<sup>_K_and</sup><sup>_Y_</sup> _T_<sup>_M_, where</sup><sup>_Y_</sup> _T_<sup>_M_denotes a series of one-hot vectors used to</sup> represent the category at each moment of _ST_<sup>_K_.For example, given a system has three fault</sup> states (Faults 1, 2, and 3) and one normal state. If the system state at a certain moment is Fault 1, then a one-hot vector [0, 1, 0, 0] is used to represent such a system state. In this way, within consecutive moments, we can obtain a series of one-hot vectors. Arranging these one-hot vectors in chronological order, we then obtain _YT_<sup>_M_that is also an MTS, as we can</sup> see, where _M_ denotes the total number of system states and _T_ denotes the length of the consecutive moments. A detailed description to the process of SWP for _ST_<sup>_K_and</sup><sup>_Y_</sup> _T_<sup>_M_is shown</sup> in Figure 1. As can be seen in Figure 1, SWP has a sliding window that is a rectangular frame used to obtain sub-series from _ST_<sup>_K_and</sup><sup>_Y_</sup> _T_<sup>_M_.Sub-series are continuously obtained by moving</sup> the sliding window. Assuming the width of the sliding window is an integer _d_ (0 _< d ≤ T_ ) and the step size of the movement of the sliding window is an integer _λ_ (0 _< λ ≤ T − d_ ), SWP is represented as _W_ ( _d_ , _λ_ ). Let the _i_ th sub-series obtained by _W_ ( _d_ , _λ_ ) be � _Sd_<sup>_K_</sup> � _i_<sup>for</sup><sup>_S_</sup> _T_<sup>_K_,</sup> and _Y_<sup>_M_The last element of</sup> _Y_<sup>_M_</sup> � _d_ � _i_<sup>for</sup><sup>_Y_</sup> _T_<sup>_M_.</sup> � _d_ � _i_<sup>is denoted as (</sup><sup>_ym_)</sup><sup>_i_(</sup><sup>_m_= 1, . . . ,</sup><sup>_M_), that is</sup> considered as the category of � _Sd_<sup>_K_</sup> � _i_<sup>.Then, the tuple</sup><sup>_<_</sup> � _Sd_<sup>_K_</sup> � _i_<sup>, (</sup><sup>_ym_)</sup><sup>_i>_can be considered as</sup> the sample obtained by the _i_ th movement of the sliding window. In this way, an imagelike data set _D_ = � _<_ � _Sd_<sup>_K_</sup> � _i_<sup>,</sup><sup>_Yi>_</sup> �� _i_ = 1, . . . , _N_ � can be obtained by constantly moving the sliding window, where _N_ denotes the number of the obtained samples. 


![](Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism_images/Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism.pdf-0005-04.png)


**Figure 1.** SWP _W_ ( _d_ , _λ_ ) for the raw time series _ST_<sup>_K_and</sup><sup>_Y_</sup> _T_<sup>_M_.</sup> 

To explain the above sliding window processing more clearly, let’s give an example below. Suppose a system has two fault states and one normal state. We detect the operating 

6 of 21 

_Processes_ **2023** , _11_ , 3233 

state of the system by observing four system properties. To this end, we collect the observed system attribute data in five consecutive moments, namely _S_ 5<sup>4, as follows:</sup> 


![](Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism_images/Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism.pdf-0006-03.png)


Similarly, we record the system states _Y_ 5<sup>3in the manner of one-hot vectors,</sup> 


![](Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism_images/Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism.pdf-0006-05.png)


With the use of a SWP _W_ (3, 1), at the first move of the sliding window we obtain the following image-like data and their corresponding label: 


![](Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism_images/Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism.pdf-0006-07.png)


At the second move, the following results can be obtained: 


![](Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism_images/Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism.pdf-0006-09.png)


At the last move, the results come as: 


![](Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism_images/Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism.pdf-0006-11.png)


## **4. Attention-Based CNN for Fault Diagnosis** 

It is a fact that different attributes in MTS contribute differently to fault diagnosis. Although a classic CNN may be able to learn such correlation between attributes and fault categories, if such information can be given to CNNs in advance, the informative data regions will be located by the feature extractor, which enables the network to learn useful fault features more accurately and efficiently. 

Attention mechanisms are a class of methods that enable the feature extractor of a CNN to selectively focus on specific regions of the data [36]. In this study, the attention mechanism [37] is used to assist the feature extractor in focusing on the data regions that have a large correlation with the faults. Firstly, the correlation between the data regions and faults is obtained from prior knowledge about category–attribute correlation that is defined based on the Pearson Correlation Coefficient (PCC). Then, the defined prior knowledge is integrated into the feature extractor of CNNs based on an attention mechanism. In this way, this attention-based CNN can pay attention to the correlation between data regions and faults when extracting features. 

7 of 21 

_Processes_ **2023** , _11_ , 3233 

## _4.1. Prior Knowledge about Category-Attribute Correlation_ 

## 4.1.1. 

PCC is commonly used to characterize the degree of linear correlation between two sequences _X_ = [ _x_ 1, . . . _xn_ ] and _Y_ = [ _y_ 1, . . . _yn_ ], which is often expressed as _r_ ( _X_ , _Y_ ) [38]. The following is its measurement method: 


![](Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism_images/Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism.pdf-0007-05.png)


and 


![](Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism_images/Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism.pdf-0007-07.png)


One can see that _−_ 1 _≤ r_ ( _X_ , _Y_ ) _≤_ 1. When _r_ ( _X_ , _Y_ ) _<_ ( _>_ )0, it means that there is a negative (positive) correlation between _X_ and _Y_ . When _r_ ( _X_ , _Y_ ) = 0, it means that there is absolutely no correlation between _X_ and _Y_ . The size of _|r_ ( _X_ , _Y_ ) _|_ represents the magnitude of the correlation between _X_ and _Y_ . For more details, please see a previous study [39] that gave an explanation between PCC and correlation. 

## 4.1.2. Category-Attribute Correlation Matrix 

Based on the definition of PCC, we deduce the definition of prior knowledge about category-attribute correlation. 

**Definition 1:** _Correlation between categories and attributes. Suppose that the fault type implicit in the raw time series ST_<sup>_Kisdenotedasfm∈F_=</sup><sup>_{fm|m_= 1, . . . ,</sup><sup>_M},wheref_1</sup><sup>_de-_</sup> _notes the normal category and fµ_ ( _µ_ = 2, . . . , _M_ ) _denote the fault categories. Let’s use YT_ ( _fm_ ) = [ _y_ 1, . . . , _yt_ , . . . , _yT_ ] ( _yt ∈{_ 1, _m}_ ) _to denote the corresponding category UTS associated with ST_<sup>_K._</sup> _In other words, the fault category of ST_<sup>_Kateachmomentiseitherf_1</sup><sup>_orfm.ThePCCrmk_=</sup> _r_ ( _ST_ ( _ck_ ), _YT_ ( _fm_ )) _is used to represent the correlation between fm and ck, where ST_ ( _ck_ ) ( _k_ = 1, . . . , _K_ ) _is the kth column of ST_<sup>_Kthat represents the UTS related to ck_.</sup> 

> **Definition 2:** _Category-attribute correlation matrix. The category-attribute correlation matrix is defined as R_ = ( _rmk_ ) _M×K, where rmk is the correlation between fm and ck_ . 

The category–attribute correlation matrix _R_ , obtained from historical data or experience, is a kind of prior knowledge which accurately reflects the linear correlation between categories and attributes. If CNNs can use this prior knowledge in the process of feature extraction, they can accurately locate the informative data regions, thereby accurately extracting fault features. In what follows, the process that integrates _R_ into CNNs based on an attention mechanism is introduced in detail. 

## _4.2. Integrating Prior Knowledge into CNNs Based on Attention Mechanism_ 

The process of integrating prior knowledge into CNNs is shown in Figure 2. 

8 of 21 

_Processes_ **2023** , _11_ , 3233 


![](Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism_images/Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism.pdf-0008-02.png)



![](Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism_images/Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism.pdf-0008-03.png)


**Figure 2.** The process of integrating prior knowledge into CNNs. 

Step 1: Defining a PCC threshold _r_ (0 _< r <_ 1). The purpose of defining _r_ is to filter out the attributes that are not basically related to the category, while those are related to the category will be retained. 

Note 1: To prevent loss of information, an attribute should be considered as long as it has a little correlation with the fault category, and thus the value of _r_ should be the one that is able to distinguish the correlations “None” and “Low”. According to the study [39], the value of _r_ should be set around 0.09. To retain useful information as much as possible, in this study we set _r_ to 0.07, which is slightly smaller than 0.09. Furthermore, in Section 5.3.5, we present the analysis of impact of the setting of _r_ on the results of the proposed method. 

Step 2: Calculating the category–attribute attention matrix _A_ ( _r_ ) = ( _amk_ ) _M×K_ . _A_ ( _r_ ) reflects the attention relationship between categories and attributes. Its calculation method is as follows: 


![](Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism_images/Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism.pdf-0008-08.png)


Step 3: Calculating the attention matrix � _Ad_<sup>_K_</sup> � _i_<sup>related to a sample</sup><sup>_<_</sup> � _Sd_<sup>_K_</sup> � _i_<sup>, (</sup><sup>_ym_)</sup><sup>_i>_.</sup> � _Ad_<sup>_K_</sup> � _i_<sup>reflects which data regions of</sup> � _Sd_<sup>_K_</sup> � _i_<sup>need attention.The specific method to calculate</sup> � _Ad_<sup>_K_</sup> � _i_<sup>is shown in Figure 3.</sup> 

9 of 21 

_Processes_ **2023** , _11_ , 3233 


![](Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism_images/Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism.pdf-0009-02.png)


**Figure 3.** Method of calculating attention matrix � _Ad_<sup>_K_</sup> � _i_<sup>relatedtoasample</sup><sup>_<_</sup> � _Sd_<sup>_K_</sup> � _i_<sup>, (</sup><sup>_ym_)</sup><sup>_i>_.</sup><sup>_tδ_</sup> _∼ ∼_ indicates the time when the fault _fm_ occurs and � _c_ 1, _c_ 2� = � _argck amk_ = 1��� _k_ = 1, . . . , _K_ ; _amk ∈ A_ ( _r_ )�. The gray squares in � _Ad_<sup>_K_</sup> � _i_<sup>are equal to 1; others are equal to 0.</sup> 

Step 4: Compressing the feature maps _X_ output from CNNs. The channel-wise average pooling operation and channel-wise max pooling operation are applied to _X_ to obtain the _∼ ∼_ compressed feature maps _X_ 1 and _X_ 2, respectively. 


![](Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism_images/Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism.pdf-0009-05.png)


and 


![](Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism_images/Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism.pdf-0009-07.png)


~~<u>1</u>~~ where _s_ ( _x_ ) = 1+ _e_<sup>_<u>−x</u>_is used to map</sup><sup>_x_to interval (0, 1).</sup> _∼ ∼_ Step 5: Fusing � _Ad_<sup>_K_</sup> � _i_<sup>,</sup> _X_ 1 and _X_ 2. � _Ad_<sup>_K_</sup> � _i_<sup>impliestheattentioninformationofthe</sup> _∼ ∼_ sample, while _X_ 1 and _X_ 2 imply the hidden features extracted by CNNs. By fusing � _Ad_<sup>_K_</sup> � _i_<sup>,</sup> _∼ ∼ X_ 1, and _X_ 2, the attention information is integrated into the feature extraction process of CNNs. Specifically, we use matrix addition for this fusion. 


![](Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism_images/Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism.pdf-0009-09.png)


where _Y ∈ R_<sup>_w×h_</sup> is a matrix whose element reflects the degree of correlation between the data region of _X_ and the category. 

Step 6: Calculating the weight matrix _W_ . _W_ can be obtained by performing softmax operation on all elements of _Y_ : 


![](Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism_images/Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism.pdf-0009-12.png)


Step 7: Calculating the output feature mapsˆ ˆ ˆ _X_<sup>ˆ</sup> . Applying _W_ to _X_ can obtain the output feature maps _X_<sup>ˆ</sup> = � _X_ 1, . . . , _Xi_ , . . . , _Xn_ �, which achieves the purpose of integrating prior knowledge into CNNs, 


![](Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism_images/Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism.pdf-0009-14.png)


10 of 21 

_Processes_ **2023** , _11_ , 3233 

## where _×_ denotes the element-wise multiplication of matrix. 

The attention mechanism can be employed at each layer of the feature extractor, allowing for its continuous application. By repeatedly applying the attention mechanism to the layers of the feature extractor, it becomes increasingly adept at focusing on prior knowledge, enhancing its effectiveness. Besides, we can see that the attention mechanism is parameter-free since the acquisition of the weight matrix does not require a learning process, but relies entirely on the fusion of prior knowledge and extracted features. 

## **5. Case Study in Tennessee Eastman Chemical Process Benchmark** 

The TE chemical process data set has been used to test the proposed fault diagnosis method. A detailed introduction to the TE chemical data set can be seen in https://github. com/camaramm/tennessee-eastman-profBraatz. The models were written in Python 3.7 with the help of a DL library called Pytorch. The models were trained and tested on a PC with 64-bit macOS 10.15.7 operation system, 2.2-GHz Quad-core Intel Core i7 processor, and 16-GB RAM. 

## _5.1. Tennessee EASTMAN Chemical Process Benchmark_ 

The TE chemical process serves as a simulation process that closely mimics the actual flow of a chemical company. It has gained significant recognition as a benchmark for research in data-driven fault diagnosis [23]. In the TE chemical process, a total of 41 measured variables and 11 manipulated variables are involved. For the purpose of this study, a fault diagnosis model is constructed using a selection of 52 variables. The TE chemical process encompasses 21 predefined types of faults along with a normal state. To facilitate model training and testing, separate training and test sets are created for each fault type and the normal state. The sampling frequency for data collection is set at 3 min per sample. Each training set consists of 500 continuous samples, equivalent to 25 h of data, while each test set comprises 960 continuous samples, equivalent to 48 h of data. It is noteworthy that the initial 20 samples of each training set and the first 160 samples of each test set are obtained from the normal state of the TE chemical process. For additional information regarding the TE chemical process, refer to [40]. 

Note 2: In the original training sets for each type of fault, only 480 samples are collected and the first 20 normal samples are not collected. In this study, in order to ensure the consistency between the training sets and the test sets, we supplement the first 20 samples in the training set for normal state to the training sets for each type of fault. 

## _5.2. Experiments_ 

## 5.2.1. SWP for the TE Chemical Process Data Sets 

As mentioned in Section 5.1, a total of 52 variables were selected to construct a fault diagnosis model. The data collected from these variables have different dimensions, and thus a commonly used data normalization method, referred to as z-score, was used to normalize data collected from different variables before the SWP operation on the TE chemical process data sets. 

Once the z-score completed, the SWP _W_ (12, 1) ( _d_ = 12, _λ_ = 1) was used to obtain the inputs of the attention-based CNN from the TE chemical process data sets. _W_ (12, 1) is performed on each original training set and test set that can be viewed as MTS. The number of the image-like samples obtained from each training set is 488, and it is 948 for each test set. There is a total of 22 training sets and 22 test sets. Therefore, the total number of image-like samples for training and testing is 22 _×_ 488 = 10, 736 and 22 _×_ 948 = 20, 856, respectively. The result of _W_ (12, 1) for each original training set and test set is shown in Table 2. 

11 of 21 

_Processes_ **2023** , _11_ , 3233 

**Table 2.** The result of _W_ (12, 1) for each training set and test set. 

|**Categories**|**Data Set**|**Length of Time Series**|**The Number of Samples Obtained by****_W_**(**12,1**)<br>**(Normal/Fault Category)**|
|---|---|---|---|
|Nl|Training set|500|488 (488/0)|
|orma|Test set|960|948 (948/0)|
|Flt 121|Training set|500|488 (9/479)|
|aus –|Test set|960|948 (49/899)|



Note 3: The impact of the setting of _d_ on the results will be discussed in detail in Section 5.3.4. The setting of _λ_ affects the number of samples obtained by SWP. The larger the setting of _λ_ , the smaller the number of samples obtained. In this study we are expected to obtain as many samples as possible, so we set _λ_ to its minimum value of 1. 

One can find from Table 2 that some samples obtained from the original training set and the test set for each fault category are labeled as normal category. In this case, the number of samples with normal category is greater than the number of samples with fault category, which is called category (class) imbalance [41]. Actually, one can avoid category imbalance by increasing _d_ if it will affect the classification results. 

## 5.2.2. Model Training 

For the fault diagnosis of the TE chemical process, an attention-based CNN model was constructed with detailed model architecture, shown in Table 3. 

**Table 3.** The architecture of the attention-based CNN model. 

||**Layer**|**Input Feature**<br>**Maps Size**|**Output Feature**<br>**Maps Size**|**Kernel**<br>**Size/Stride/Padding**|
|---|---|---|---|---|
||Conv-1 *|1_×_12_×_52|3_× d ×_52|7_×_7/1/3|
||MaxPool-1|3_×_12_×_52|3_× d ×_52|7_×_7/1/3|
||Conv-2 *|3_×_12_×_52|5_× d ×_52|3_×_3/1/1|
||MaxPool-2|5_×_12_×_52|5_× d ×_52|3_×_3/1/1|
|Feature<br>extractor|Atten-1|5_×_12_×_<br>52/12_×_52|5_× d ×_52|-|
||Conv-3 *|5_×_12_×_52|10_× d ×_52|3_×_3/1/1|
||MaxPool-3|10_×_12_×_52|10_× d ×_52|3_×_3/1/1|
||Atten-2|10_×_12_×_<br>52/12_×_52|10_× d ×_52|-|
||Conv-4 *|10_×_12_×_52|1_× d ×_52|3_×_3/1/1|
||MaxPool-4|1_×_12_×_52|1_× d ×_52|3_×_3/1/1|
||FC-1 #|625|22|-|
|Classifer|Softmax|22|22|-|



In Table 3, the convolutional layer marked with * means that the batch normalization (BN) method proposed in [42] was used to speed up the network training; the FC layer marked with # means that the dropout method proposed in [43] was used to prevent overfitting, where the probability of discarding neurons is set to _p_ = 0.75. 

The constructed attention-based CNN model was trained in 100 epochs using Adam’s algorithm [44]. The learning rate was set to 0.0001 and the number of batch samples was set to 100. The mean squared error (MSE) loss was used as the optimization objective function for model training. 

## _5.3. Results Analysis_ 

## 5.3.1. Evaluation Indicators 

After the model is trained on the training set, it can be evaluated on the test set. Indicators commonly used for evaluating fault diagnosis model are fault diagnosis rate (FDR) and false positive rate (FPR). Given a category _i_ , _FDRi_ represents the proportion of 

12 of 21 

_Processes_ **2023** , _11_ , 3233 

the number of samples correctly predicted to category _i_ to the number of samples with category _i_ , and _FPRi_ represents the proportion of the number of samples wrongly predicted to category _i_ to the number of samples without category _i_ . They are calculated as 


![](Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism_images/Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism.pdf-0012-03.png)


and 


![](Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism_images/Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism.pdf-0012-05.png)


The meaning of related symbols in Formulas (11) and (12) can be seen in Table 4. 

**Table 4.** Statistics used to evaluate the classification performance of category _i_ . 

||**Number of Samples Predicted to Category****_i_**|**Number of Samples Not Predicted to Category****_i_**|
|---|---|---|
|Number of samples with<br>category_i_|_TPi_|_TNi_|
|Number of samples<br>without category_i_|_FPi_|_FNi_|



Furthermore, the average FDR _FDR_ and the average FPR _FPR_ were used to evaluate the overall classification performance. Suppose there are a total of _M_ categories that need to be classified, then 


![](Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism_images/Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism.pdf-0012-10.png)


and 


![](Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism_images/Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism.pdf-0012-12.png)


## 5.3.2. Evaluation Result and Performance Comparison 

Table 5 presents the specific FDR and FPR values for the proposed method, as well as representative methods proposed in previous research. The findings demonstrate that the proposal not only exhibits notable improvements in FDR and FPR performance across general fault categories, but also demonstrates accurate classification in challenging categories (such as fault 3, fault 9, and fault 15) where previous research struggled. These results indicate that the proposal significantly outperforms other data-driven fault diagnosis methods. 

## 5.3.3. Analysis of Model Interpretability 

Previous studies have predominantly utilized visualization techniques [45] and sensitivity analysis methods [46] to explore the interpretability of DL models. In this study, we employed visualization techniques to validate the interpretability of the proposed fault diagnosis method. To achieve this, we first utilized the trained attention-based CNN model to predict two different samples, denoted as � _Sd_<sup>_K_</sup> � _i_<sup>and</sup> � _Sd_<sup>_K_</sup> � _j_<sup>,fromthetestset.Subse-</sup> quently, we obtained the three-dimensional feature maps generated by the MaxPool-1 (M1), MaxPool-2 (M2), Atten-1 (A1), MaxPool-3 (M3), Atten-2 (A2), and MaxPool-4 (M4) layers. These three-dimensional feature maps were further transformed into two-dimensional feature maps through channel-wise average pooling, as per Equation (6). To facilitate visualization, the elements of the two-dimensional feature maps were mapped to the range of [0, 1] using min–max normalization. Finally, the variation in color was employed to represent the magnitude of the elements in the two-dimensional feature maps, resulting in the generation of Figures 4 and 5. 

13 of 21 

_Processes_ **2023** , _11_ , 3233 


![](Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism_images/Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism.pdf-0013-02.png)



![](Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism_images/Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism.pdf-0013-03.png)


**Figure 4.** Visible feature extraction process of � _Sd_<sup>_K_</sup> � _i_<sup>and</sup> � _Sd_<sup>_K_</sup> � _j_<sup>that have the same category.</sup> 

~~14 of 21~~ 

_~~Processes~~_ **~~2023~~** ~~,~~ _~~11~~_ ~~, 3233~~ 


![](Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism_images/Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism.pdf-0014-02.png)



![](Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism_images/Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism.pdf-0014-03.png)


**Figure 5.** Visible feature extraction process of � _Sd_<sup>_K_</sup> � _i_<sup>and</sup> � _Sd_<sup>_K_</sup> � _j_<sup>that have different categories but the</sup> same prior knowledge. 

15 of 21 

_Processes_ **2023** , _11_ , 3233 

**Table 5.** Performance comparison with other data-driven fault diagnosis methods. 

|**Categories**|**Th**||**FDR (%)**|||**FP**<br>**Th**|**R (%)**|
|---|---|---|---|---|---|---|---|
||**e**<br>**Proposal**|**DL [47]**|**EDBN-2 [48]**|**MPLS [23]**|**PCA [49]**|**e**<br>**Proposal**|**EDBN-2 [48]**|
|Normal|**96.85**|-|90.80|-|86.25|**1.60**|3.34|
|Fault 1|99.76|**100.00**|**100.00**|**100.00**|96.56|**0.00**|**0.00**|
|Fault 2|99.76|99.75|**100.00**|98.88|96.88|**0.00**|0.08|
|Fault 3|**93.08**|-|-|18.75|-|**4.60**|-|
|Fault 4|**100.00**|**100.00**|**100.00**|**100.00**|96.88|**0.00**|0.01|
|Fault 5|99.75|98.88|**100.00**|**100.00**|96.88|0.40|**0.00**|
|Fault 6|**100.00**|**100.00**|**100.00**|**100.00**|99.48|**0.00**|**0.00**|
|Fault 7|**100.00**|**100.00**|**100.00**|**100.00**|99.27|**0.00**|**0.00**|
|Fault 8|98.23|97.88|98.29|**98.63**|94.90|**0.20**|0.22|
|Fault 9|**95.24**|-|-|12.13|-|**0.30**|-|
|Fault 10|98.79|**99.25**|80.81|91.13|87.81|**0.14**|0.67|
|Fault 11|**99.77**|89.25|99.74|83.25|77.81|**0.00**|**0.00**|
|Fault 12|99.78|99.75|**100.00**|99.88|97.81|0.30|**0.00**|
|Fault 13|**100.00**|99.75|91.98|95.50|79.17|**0.00**|**0.00**|
|Fault 14|99.09|95.13|**100.00**|**100.00**|98.23|0.20|**0.00**|
|Fault 15|**92.33**|-|-|23.25|-|**7.20**|-|
|Fault 16|97.97|99.50|75.56|94.28|79.90|**0.12**|0.67|
|Fault 17|**100.00**|99.75|**100.00**|97.13|86.46|**0.00**|**0.00**|
|Fault 18|**100.00**|99.50|93.43|91.25|72.81|**0.00**|**0.00**|
|Fault 19|**98.30**|96.75|95.53|94.25|91.56|0.40|**0.27**|
|Fault 20|98.80|**99.38**|93.17|91.50|88.54|0.60|**0.00**|
|Fault 21|**98.60**|-|83.44|72.75|95.00|1.80|**1.17**|
|Average|**98.46**|-|94.31|-|-|**1.54**|5.69|



- From Figure 4, one can summarize the following findings: 

- 1. The raw data of � _Sd_<sup>_K_</sup> � _i_<sup>and</sup> � _Sd_<sup>_K_</sup> � _j_<sup>are indistinguishable, and the model cannot produce</sup> distinguishable features on the outputs of M1 after the raw data is processed by a convolutional layer and a pooling layer. 

- 2. From M1 to M2, some distinguishable striped features began to appear, as indicated by the red arrow. However, it can be seen that the striped features in the M2 outputs of � _Sd_<sup>_K_</sup> � _i_<sup>and</sup> � _Sd_<sup>_K_</sup> � _j_<sup>show some differences, which implies that the extracted features</sup> are biased. Specifically, taking the area framed by dotted rectangle in the outputs of M2 as an example, that of � _Sd_<sup>_K_</sup> � _i_<sup>shows light yellow, while that of</sup> � _Sd_<sup>_K_</sup> � _j_<sup>shows light</sup> green. These deviations may affect the performance of classification, so it is necessary to eliminate them in subsequent operations. 

- 3. From M2 to A1, one can find that the clearer striped features begin to appear for the areas framed by dotted ellipse that needs attention, which indicates that the prior knowledge has been integrated into the feature maps output from M2. Moreover, the colors of the areas framed by dotted rectangle in the M2 and A1 of � _Sd_<sup>_K_</sup> � _i_<sup>and</sup> � _Sd_<sup>_K_</sup> � _j_ are darker and tend to be the same, which indicates that the deviation in the feature maps began to be ignored owing to the prior knowledge integration. 

4. From A1 to M3, the stripes of the feature maps become more clearly distinguishable, which indicates that some detailed features are further extracted. However, the deviation features framed by dotted rectangular are also enhanced. 

5. From M3 to A2, it can be seen that the prior knowledge has been significantly enhanced in the feature maps by comparing the areas framed by dotted ellipse in M3 and A2 and the deviation features in feature maps have been basically eliminated by comparing the areas framed by dotted rectangular in M3 and A2. However, one can also find that, except for the stripes representing the prior knowledge, which are quite clear, the other stripes are quite vague, which indicates that some detailed features in the feature maps are ignored due to excessive attention paid to the prior knowledge. 

16 of 21 

_Processes_ **2023** , _11_ , 3233 

6. From A2 to M4, one can find that the vague stripes become clear, which indicates that the detailed features in the feature maps is enhanced and the prior knowledge is retained. 

7. Compared to the raw data and the feature maps output from M4, the latter are distinguishable. Moreover, the color of stripes framed by the dotted rounded rectangle in M4 changes in the time dimension, which indicates that the feature maps output from M4 not only clearly contains the prior knowledge, but also that the prior knowledge is further enhanced in the time dimension. Furthermore, some detailed features (those lighter stripes) are also contained in the outputs of M4. 

From Figure 5, one can find the final feature maps output from M4 of � _Sd_<sup>_K_</sup> � _i_<sup>and</sup> � _Sd_<sup>_K_</sup> � _j_ are significantly different, although their corresponding prior knowledge is the same. The difference is mainly reflected in two aspects. One is that further extracted features of the time dimension in the prior knowledge are different. The other is that some detailed features are also different. Therefore, the model can distinguish � _Sd_<sup>_K_</sup> � _i_<sup>and</sup> � _Sd_<sup>_K_</sup> � _j_<sup>based on</sup> these differences. 

In summary, the above findings can further explain why the proposed model can achieve significant performance in the fault diagnosis for the TE chemical process, which shows the interpretability of the proposed model. 

## 5.3.4. Analysis of Hyperparameter _d_ 

To explore the impact of hyperparameter _d_ on the results of the proposed method, we fixed the value of _r_ to 0.07, and set _d_ to five different values (2, 12, 32, 52, 72). We trained <u>the model under different settings of</u> _<u>r</u>_ <u>and</u> _<u>d</u>_ <u>, and tested the trained models using</u> _<u>FDR</u>_ <u>and</u> _FPR_ . The results are shown in Figure 6. It can be seen from Figure 6 that the best results were obtained when _d_ was set to 12. When _d_ is set larger than 12 or smaller than 12, the performance of the model will decrease. 


![](Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism_images/Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism.pdf-0016-08.png)


**Figure 6.** Average FDR and FPR obtained by models with a fixed _r_ = 0.07 and different _d_ (2, 12, 32, 52, 72). 

The results indicate that there seems to be an intermediate value, _d_ = 12, that makes the model perform best when _r_ = 0.07 is fixed. When _d_ is smaller than the intermediate value, the time-dependent information used for fault diagnosis is insufficient; as a result, certain categories may not be recognized by the model. When _d_ is larger than the intermediate value, some interference information may get involved, which may be because that the 

17 of 21 

_Processes_ **2023** , _11_ , 3233 

data farther away from the current time is less relevant to the fault diagnosis at the current time. 

## 5.3.5. Analysis of Hyperparameter r 

We fixed the value of _d_ to its optimal value, namely 12, and selected five different values of _r_ for the analysis of _r_ . The obtained results of _FDR_ and _FPR_ under different settings of _d_ and _r_ are shown in Figure 7. It can be seen from Figure 7 that the model achieves the best performance on _FDR_ and _FPR_ when _r_ = 0.07. When _r_ < 0.07, the performance of the model decreases as _r_ decreases. When _r_ > 0.07, the <u>performance of the model decreases</u> as _r_ increases. 


![](Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism_images/Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism.pdf-0017-05.png)


**Figure 7.** Average FDR and FPR obtained by models with a fixed _d_ = 12 and different _r_ (0.05, 0.06, 0.07, 0.08, 0.09). 

The results indicate that there seems to be an intermediate value, _r_ = 0.07, that makes the model perform best when _d_ = 12 is fixed. When _r_ is smaller than the intermediate value, those attributes that are not very relevant to fault diagnosis are also concerned. When _r_ is larger than the intermediate value, only those attributes with great relevance are concerned, which leads to the lack of attention information. 

Through the analysis of _d_ and _r_ , one can find that the performance of the model will reach a unique peak at a specific _d_<sup>_∗_</sup> and _r_<sup>_∗_</sup> , assuming that the effects of _d_ and _r_ on model performance are independent of each other. Then, we can fix one parameter and change the value of another to obtain a series of models and evaluate them on the test set. By comparing the evaluation results of the models, _d_<sup>_∗_</sup> and _r_<sup>_∗_</sup> can be obtained. 

## _5.4. Discussion on the Calculation of Attention Matrix_ 

As indicated in Table 3, the proposed attention layer takes two inputs: the feature map generated by the previous layer and the attention matrix corresponding to the sample. As per Step 3 in Section 3.2, to obtain the attention matrix specific to a particular sample, the knowledge of the label assigned to that sample is indeed required. To be more specific, when we employ the attribute–category attention matrix _A_ ( _r_ ) to compute the attention matrix associated with a sample, _A_ ( _r_ ) effectively conveys the category of the sample, given that different categories exhibit distinct attention patterns towards specific attributes. But, the specificity of such conveyance will decrease as the value of _r_ increases. As shown in Figure 8, when the value of _r_ increases, some categories focus on the same attributes, which causes the model to be confused about these categories. Such a requirement of label 

18 of 21 

_Processes_ **2023** , _11_ , 3233 

knowledge makes sense during the training process, but it does not make sense during the testing process, since the model should make predictions based on the input data without any knowledge of the true labels. Notification of label knowledge is equivalent to indirectly <u>revealing the category of the sample to the model, which is why we achieved such good</u> results shown in Table 5. 


![](Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism_images/Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism.pdf-0018-03.png)



![](Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism_images/Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism.pdf-0018-04.png)



![](Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism_images/Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism.pdf-0018-05.png)



![](Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism_images/Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism.pdf-0018-06.png)



![](Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism_images/Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism.pdf-0018-07.png)



![](Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism_images/Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism.pdf-0018-08.png)



![](Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism_images/Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism.pdf-0018-09.png)



![](Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism_images/Improving_Accuracy_and_Interpretability_of_CNN-Based_Fault_Diagnosis_through_an_Attention_Mechanism.pdf-0018-10.png)


**Figure 8.** Visualization of category–attribute attention matrix _A_ ( _r_ ) with different _r_ . 

Nevertheless, the success of the experimental results shows that the integration of reliable prior knowledge into CNNs can greatly improve the accuracy and interpretability of fault diagnosis, which instructs us to seek another definition of prior knowledge that does not depend on labels. In what follows, we present an alternative definition of prior knowledge without relying on labels. 

19 of 21 

_Processes_ **2023** , _11_ , 3233 

Remember that we ultimately need to obtain the data regions that need to be paid attention to and mark them as 1, while those that do not need to be paid attention to are marked as 0. Considering outliers in the data, it is a fact that the occurrence of faults is always accompanied by outliers. In other words, outliers imply richer fault modes and therefore require special attention. To this end, in step 3 of the proposed method the attention matrix � _Ad_<sup>_K_</sup> � _i_<sup>relatedtoasample</sup><sup>_<_</sup> � _Sd_<sup>_K_</sup> � _i_<sup>, (</sup><sup>_ym_)</sup><sup>_i>_canbeobtainedthrougha</sup> certain unsupervised outlier detection technique which regards _<_ � _Sd_<sup>_K_</sup> � _i_<sup>, (</sup><sup>_ym_)</sup><sup>_i>_as the</sup> input, such as those presented in the studies [50,51]. In this way, we do not use any label information, and any unsupervised outlier detection technique can be used as an asset to gain prior knowledge for this study. 

## **6. Conclusions and Future Works** 

We propose an attention-based CNN fault diagnosis method in this study. In the proposal, the integration of prior knowledge about category–attribute correlation based on an attention mechanism significantly improves the accuracy and interpretability of fault diagnosis. A case study in the TE chemical benchmark verifies the effectiveness and superiority of the proposal. Moreover, the conclusion drawn from the sensitivity analysis on hyperparameters provides guidance to set optimal values for hyperparameters. More importantly, we use visualization techniques to analyze the feature extraction process, which shows that the proposal has excellent interpretability. Nevertheless, this study still has the following limitations, which will be solved in our future research. 

1. This study only validates the effectiveness of the proposal on the TE chemical process dataset; it is necessary to use the proposal to solve other fault diagnosis problems, such as rolling bearing fault diagnosis [52], ice detection of wind turbine blades [53], and gearbox fault diagnosis [54], to further verify the proposal. This is crucial, as it ensures that the proposed method can be easily applied for fault diagnosis in different scenarios. 

2. This study improves the accuracy and interpretability of fault diagnosis by integrating prior knowledge, but the definition of prior knowledge uses label information, which leads to some irrationality, and thus alternative prior knowledge definitions that do not use label information need to be further studied. A feasible solution is to define the attention matrix as outliers in the data, and then use unsupervised outlier detection methods, such as those presented in [50,51], to obtain the attention matrix. 

3. Although visualization techniques are used to analyze model interpretability in this study, developing and using quantitative interpretability metrics, such as those presented in the study [55], are worthy of further study for validating the interpretability of the proposed method more specifically. 

**Author Contributions:** Conceptualization, J.Z.; Methodology, Y.H.; Software, R.L.; Formal analysis, R.L.; Investigation, Y.H.; Data curation, R.L.; Writing—original draft, Y.H.; Writing—review & editing, J.Z. and S.Z.; Visualization, S.Z.; Supervision, S.Z.; Funding acquisition, J.Z. All authors have read and agreed to the published version of the manuscript. 

> **Funding:** This research was funded by the Foundation for Science and Technology Project for State Grid Anhui Electric Power Co., Ltd. [No. 52120522000M]. 

**Data Availability Statement:** Data is contained within the article. 

## **References** 

1. Cai, B.; Zhao, Y.; Liu, H.; Xie, M. A Data-Driven Fault Diagnosis Methodology in Three-Phase Inverters for PMSM Drive Systems. _IEEE Trans. Power Electron._ **2017** , _32_ , 5590–5600. [CrossRef] 

2. Feng, J.; Yao, Y.; Lu, S.; Liu, Y. Domain Knowledge-based Deep-Broad Learning Framework for Fault Diagnosis. _IEEE Trans. Ind. Electron._ **2020** , _68_ , 3454–3464. [CrossRef] 

20 of 21 

_Processes_ **2023** , _11_ , 3233 

3. Gao, X.; Hou, J. An improved SVM integrated GS-PCA fault diagnosis approach of Tennessee Eastman process. _Neurocomputing_ **2016** , _174_ , 906–911. [CrossRef] 

4. Jiang, G.; He, H.; Yan, J.; Xie, P. Multiscale Convolutional Neural Networks for Fault Diagnosis of Wind Turbine Gearbox. _IEEE Trans. Ind. Electron._ **2019** , _66_ , 3196–3207. [CrossRef] 

5. Lei, Y.; Jia, F.; Lin, J.; Xing, S.; Ding, S.X. An Intelligent Fault Diagnosis Method Using Unsupervised Feature Learning Towards Mechanical Big Data. _IEEE Trans. Ind. Electron._ **2016** , _63_ , 3137–3147. [CrossRef] 

6. He, M.; He, D. Deep Learning Based Approach for Bearing Fault Diagnosis. _IEEE Trans. Ind. Appl._ **2017** , _53_ , 3057–3065. [CrossRef] 7. Jia, F.; Lei, Y.; Lin, J.; Zhou, X.; Lu, N. Deep neural networks: A promising tool for fault characteristic mining and intelligent diagnosis of rotating machinery with massive data. _Mech. Syst. Signal Process._ **2016** , _72–73_ , 303–315. [CrossRef] 

8. Shao, H.; Jiang, H.; Wang, F.; Wang, Y. Rolling bearing fault diagnosis using adaptive deep belief network with dual-tree complex wavelet packet. _ISA Trans._ **2017** , _69_ , 187–201. [CrossRef] 

9. Liu, H.; Zhou, J.; Zheng, Y.; Jiang, W.; Zhang, Y. Fault diagnosis of rolling bearings with recurrent neural network-based autoencoders. _ISA Trans._ **2018** , _77_ , 167–178. [CrossRef] 

10. Wu, H.; Zhao, J. Deep convolutional neural network model based chemical process fault diagnosis. _Comput. Chem. Eng._ **2018** , _115_ , 185–197. [CrossRef] 

11. Huang, T.; Zhang, Q.; Tang, X.; Zhao, S.; Lu, X. A novel fault diagnosis method based on CNN and LSTM and its application in fault diagnosis for complex systems. _Artif. Intell. Rev._ **2022** , _55_ , 1289–1315. [CrossRef] 

12. Xu, Y.; Li, Z.; Wang, X.; Li, W. Sarkodie-Gyan and S. Feng. A hybrid deep-learning model for fault diagnosis of rolling bearings. _Measurement_ **2021** , _169_ , 108502. [CrossRef] 

13. Yu, S.; Wang, M.; Pang, S.; Song, L.; Qiao, S. Intelligent fault diagnosis and visual interpretability of rotating machinery based on residual neural network. _Measurement_ **2022** , _196_ , 111228. [CrossRef] 

14. Li, X.; Zhang, W.; Ding, Q.; Sun, J.Q. Intelligent rotating machinery fault diagnosis based on deep learning using data augmentation. _J. Intell. Manuf._ **2020** , _31_ , 433–452. [CrossRef] 

15. Li, C.; Li, S.; Wang, H.; Gu, F.; Ball, A.D. Attention-based deep meta-transfer learning for few-shot fine-grained fault diagnosis. _Knowl.-Based Syst._ **2023** , _264_ , 110345. [CrossRef] 

16. Yang, H.; Li, X.; Zhang, W. Interpretability of deep convolutional neural networks on rolling bearing fault diagnosis. _Meas. Sci. Technol._ **2022** , _33_ , 055005. [CrossRef] 

17. Yang, D.; Karimi, H.R.; Gelman, L. An explainable intelligence fault diagnosis framework for rotating machinery. _Neurocomputing_ **2023** , _541_ , 126257. [CrossRef] 

18. Li, X.; Zhang, W.; Ding, Q. Understanding and improving deep learning-based rolling bearing fault diagnosis with attention mechanism. _Signal Process._ **2019** , _161_ , 136–154. [CrossRef] 

19. Yu, J.; Liu, G. Knowledge extraction and insertion to deep belief network for gearbox fault diagnosis. _Knowl.-Based Syst._ **2020** , _197_ , 105883. [CrossRef] 

20. Xie, T.; Xu, Q.; Jiang, C.; Lu, S.; Wang, X. The fault frequency priors fusion deep learning framework with application to fault diagnosis of offshore wind turbines. _Renew. Energ._ **2023** , _202_ , 143–153. [CrossRef] 

21. Liao, J.; Dong, H.; Sun, Z.; Sun, J.; Zhang, S.; Fan, F. Attention-embedded quadratic network (qttention) for effective and interpretable bearing fault diagnosis. _IEEE Trans. Instrum. Meas._ **2023** , _72_ , 1–13. [CrossRef] 

22. Peng, D.; Wang, H.; Desmet, W.; Gryllias, K. RMA-CNN: A residual mixed-domain attention CNN for bearings fault diagnosis and its time-frequency domain interpretability. _J. Dyn. Monit. Diagn._ **2023** , _2_ , 115–132. [CrossRef] 

23. Yin, S.; Ding, S.X.; Haghani, A.; Hao, H.; Zhang, P. A comparison study of basic data-driven fault diagnosis and process monitoring methods on the benchmark Tennessee Eastman process. _J. Process Control_ **2012** , _22_ , 1567–1581. [CrossRef] 

24. Girshick, R.; Donahue, J.; Darrell, T.; Malik, J. Rich feature hierarchies for accurate object detection and semantic segmentation. In Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition, Columbus, OH, USA, 23–28 June 2014; pp. 580–587. 

25. Girshick, R. Fast r-cnn. In Proceedings of the IEEE International Conference on Computer Vision, Santiago, Chile, 11–18 December 2015; pp. 1440–1448. 

26. Ren, S.; He, K.; Girshick, R.; Sun, J. Faster r-cnn: Towards real-time object detection with region proposal networks. In Proceedings of the Advances in Neural Information Processing Systems 28 (NIPS 2015), Montreal, QC, Canada, 7–12 December 2015; Volume 28. 

27. He, K.; Gkioxari, G.; Dollár, P.; Girshick, R. Mask r-cnn. In Proceedings of the IEEE International Conference on Computer Vision, Venice, Italy, 22–29 October 2017; pp. 2961–2969. 

28. Uijlings, J.R.; Van De Sande, K.E.; Gevers, T.; Smeulders, A.W. Selective search for object recognition. _Int. J. Comput. Vision_ **2013** , _104_ , 154–171. [CrossRef] 

29. Qi, L.; Huo, J.; Wang, L.; Shi, Y.; Gao, Y. A mask based deep ranking neural network for person retrieval. In Proceedings of the IEEE International Conference on Multimedia and Expo (ICME), Shanghai, China, 8–12 July 2019; pp. 496–501. 

30. Liu, L.Y.F.; Liu, Y.; Zhu, H. Masked convolutional neural network for supervised learning problems. _Stat_ **2020** , _9_ , e290. [CrossRef] [PubMed] 

31. Cai, L.; Li, H.; Dong, W.; Fang, H. Micro-expression recognition using 3D DenseNet fused Squeeze-and-Excitation Networks. _Appl. Soft Comput._ **2022** , _119_ , 108594. [CrossRef] 

21 of 21 

_Processes_ **2023** , _11_ , 3233 

32. Roy, S.K.; Dubey, S.R.; Chatterjee, S.; Chaudhuri, B.B. FuSENet: Fused squeeze-and-excitation network for spectral-spatial hyperspectral image classification. _IET Image Process._ **2020** , _14_ , 1653–1661. [CrossRef] 

33. Hu, J.; Shen, L.; Sun, G. Squeeze-and-excitation networks. In Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition, Salt Lake City, UT, USA, 18–22 June 2018; pp. 7132–7141. 

34. Krizhevsky, A.; Sutskever, I.; Hinton, G.E. ImageNet Classification with Deep Convolutional Neural Networks. In _Advances in Neural Information Processing Systems 25_ ; Pereira, F., Burges, C.J.C., Bottou, L., Weinberger, K.Q., Eds.; Curran Associates, Inc.: Red Hook, NY, USA, 2012; pp. 1097–1105. 

35. Wei, W.W. _Multivariate Time Series Analysis and Applications_ ; John Wiley & Sons: Hoboken, NJ, USA, 2018. 36. Vaswani, A.; Shazeer, N.; Parmar, N.; Uszkoreit, J.; Jones, L.; Gomez, A.N.; Kaiser, Ł.; Polosukhin, I. Attention is All you Need. In _Advances in Neural Information Processing Systems 30_ ; Guyon, I., Luxburg, U.V., Bengio, S., Wallach, H., Fergus, R., Vishwanathan, S., Garnett, R., Eds.; Curran Associates, Inc.: Red Hook, NY, USA, 2017; pp. 5998–6008. 

37. Yu, Z.; Peng, W.; Li, X.; Hong, X.; Zhao, G. Remote heart rate measurement from highly compressed facial videos: An end-to-end deep learning solution with video enhancement. In Proceedings of the 2019 IEEE/CVF International Conference on Computer Vision (ICCV), Seoul, Republic of Korea, 27 October–2 November 2019; pp. 151–160. 

38. Puth, M.T.; Neuhäuser, M.; Ruxton, G.D. Effective use of Pearson’s product–moment correlation coefficient. _Anim. Behav._ **2014** , _93_ , 183–189. [CrossRef] 

39. Cohen, J. _Statistical Power Analysis for the Behavioral Sciences_ ; Academic Press: Cambridge, MA, USA, 2013. 

40. Downs, J.J.; Vogel, E.F. A plant-wide industrial process control problem. _Comput. Chem. Eng._ **1993** , _17_ , 245–255. [CrossRef] 41. He, H.; Garcia, E.A. Learning from Imbalanced Data. _IEEE Trans. Knowl. Data Eng._ **2009** , _21_ , 1263–1284. 42. Ioffe, S.; Szegedy, C. Batch Normalization: Accelerating deep network training by reducing internal covariate shift. _arXiv_ **2015** , arXiv:1502.03167. 

43. Srivastava, N.; Hinton, G.; Krizhevsky, A.; Sutskever, I.; Salakhutdinov, R. Dropout: A simple way to prevent neural networks from overfitting. _J. Mach. Learn. Res._ **2014** , _15_ , 1929–1958. 

44. Kingma, D.P.; Ba, J. Adam: A method for stochastic optimization. _arXiv_ **2017** , arXiv:1412.6980. 45. Zeiler, M.D.; Fergus, R. Visualizing and understanding convolutional networks. In Proceedings of the European Conference on Computer Vision, Zurich, Switzerland, 6–12 September 2014; pp. 818–833. 

46. Olden, J.D.; Jackson, D.A. Illuminating the “black box”: A randomization approach for understanding variable contributions in artificial neural networks. _Ecol. Model._ **2002** , _154_ , 135–150. [CrossRef] 

47. Lv, F.; Wen, C. Fault Diagnosis Based on Deep Learning. In Proceedings of the 2016 American Control Conference (ACC), Boston, MA, USA, 6–8 July 2016; pp. 6851–6856. 

48. Wang, Y.; Pan, Z.; Yuan, X.; Yang, C.; Gui, W. A novel deep learning based fault diagnosis approach for chemical process with extended deep belief network. _ISA Trans._ **2020** , _96_ , 457–467. [CrossRef] 

49. Jing, C.; Hou, J. SVM and PCA based fault classification approaches for complicated industrial process. _Neurocomputing_ **2015** , _167_ , 636–642. [CrossRef] 

50. Samariya, D.; Thakkar, A. A comprehensive survey of anomaly detection algorithms. _Ann. Data Sci._ **2023** , _10_ , 829–850. [CrossRef] 51. Smiti, A. A critical overview of outlier detection methods. _Comput. Sci. Rev._ **2020** , _38_ , 100306. [CrossRef] 52. Li, B.; Chow, M.-Y.; Tipsuwan, Y.; Hung, J.C. Neural-network-based motor rolling bearing fault diagnosis. _IEEE Trans. Ind. Electron._ **2000** , _47_ , 1060–1069. [CrossRef] 

53. Du, Y.; Zhou, S.; Jing, X.; Peng, Y.; Wu, H.; Kwok, N. Damage detection techniques for wind turbine blades: A review. _Mech. Syst. Signal Process._ **2020** , _141_ , 106445. [CrossRef] 

54. Cheng, W.; Wang, S.; Liu, Y.; Chen, X.; Nie, Z.; Xing, J.; Zhang, R.; Huang, Q. A novel planetary gearbox fault diagnosis method for nuclear circulating water pump with class imbalance and data distribution shift. _IEEE Trans. Instrum. Meas._ **2023** , _72_ , 1–13. [CrossRef] 

55. Vilone, G.; Longo, L. Notions of explainability and evaluation approaches for explainable artificial intelligence. _Inform. Fusion_ **2021** , _76_ , 89–106. [CrossRef] 

**Disclaimer/Publisher’s Note:** The statements, opinions and data contained in all publications are solely those of the individual author(s) and contributor(s) and not of MDPI and/or the editor(s). MDPI and/or the editor(s) disclaim responsibility for any injury to people or property resulting from any ideas, methods, instructions or products referred to in the content. 

