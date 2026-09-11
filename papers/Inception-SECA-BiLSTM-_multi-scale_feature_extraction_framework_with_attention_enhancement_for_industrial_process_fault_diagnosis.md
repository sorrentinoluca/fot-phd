Process Safety and Environmental Protection 213 (2026) 108964 


![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0001-01.png)


Contents lists available at ScienceDirect 

# Process Safety and Environmental Protection 

journal homepage: www.journals.elsevier.com/process-safety-and-environmental-protection 


![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0001-05.png)


## Inception-SECA-BiLSTM: A multi-scale feature extraction modeling framework with attention enhancement for industrial process fault diagnosis 


![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0001-07.png)


### Chaochao Lv<sup>a</sup> , Limin Wang<sup>b</sup> , Furong Gao<sup>c</sup> , Ridong Zhang<sup>a,*</sup> 

a _Information and Control Institute, Hangzhou Dianzi University, Hangzhou 310018, China_ 

b _School of Mechanical and Electrical Engineering, Guangzhou University, Guangzhou 510006, China_ 

c _Department of Chemical and Biological Engineering, Hong Kong University of Science and Technology, Hong Kong_ 

|A R T I C L E I N F O|A B S T R A C T|
|---|---|
|_Keywords:_<br>Industrial process<br>Fault diagnosis<br>Multi-scale feature fusion<br>Attention mechanism<br>BiLSTM|Industrial process data are often characterized by strong nonlinearity, temporal dependence, severe noise<br>interference, and the diffculty of extracting weak fault features, which pose signifcant challenges to accurate<br>fault diagnosis. To address these issues, this paper proposes an Inception Self-Adaptive Effcient Channel<br>Attention Bidirectional Long Short-Term Memory (Inception-SECA-BiLSTM) model for industrial process fault<br>diagnosis. The proposed model integrates multi-scale feature extraction, channel attention enhancement, and<br>temporal dependency modeling into a unifed framework. Specifcally, an Inception-SECA module is designed to<br>capture multi-scale fault features through parallel convolutions, while the embedded Self-Adaptive Effcient<br>Channel Attention (SECA) mechanism adaptively recalibrates channel-wise feature responses, enhancing critical<br>fault-related information and suppressing noise. Furthermore, a Bidirectional Long Short-Term Memory<br>(BiLSTM) network is employed to model bidirectional temporal dependencies, combined with a single-head<br>scaled dot-product self-attention mechanism to further emphasize informative features. Finally, a feature ag-<br>gregation strategy is introduced to fuse global representations for improved fault discrimination. Experimental<br>results on the Tennessee Eastman (TE) process and a real-world industrial coke furnace dataset demonstrate that<br>the proposed method achieves superior classifcation accuracy, as well as favorable robustness to noise distur-<br>bances and stable training behavior. These fndings indicate that the proposed model provides an effective and<br>reliable solution for industrial process fault diagnosis.|



#### **1. Introduction** 

Modern industrial systems are rapidly evolving toward large-scale, continuously operating, and intelligent configurations. Industrial processes exhibit significant nonlinearity and strong coupling characteristics. Monitoring data are often accompanied by noise, and fault features present multi-scale and easily disturbed behaviors. Meanwhile, process systems themselves possess complex technical dynamics involving the interaction of multiple factors such as equipment, management decisions, operating personnel, operating conditions and external environments. Collectively, these constitute the main causes of accidents in the process industry (Adedigba et al., 2016; Arunthavanathan et al., 2021; Xiao et al., 2024; Yuan et al., 2026). In key process industries including chemical engineering, energy production, and advanced 

manufacturing, undetected minor faults may cause equipment downtime, production interruptions, and even safety hazards, resulting in substantial economic losses and adverse social impacts (Hu et al., 2026; Pasman et al., 2023; Zhang and Gao, 2026). Therefore, accurate and efficient fault diagnosis technology is crucial for ensuring operational safety, reducing maintenance costs, and promoting the upgrading optimization and operation of intelligent manufacturing, which endows it with important theoretical significance and practical engineering value (Wu et al., 2026; Yuan et al., 2024). 

Before deep learning became mainstream, methods in the field of industrial process fault diagnosis mainly relied on classical multivariate statistical analysis techniques and shallow machine learning (Pu and Li, 2021; Deng et al., 2017; Yang et al., 2021a; Chen et al., 2023a; Wang et al., 2017; Bian et al., 2022) methods, such as Support Vector Machine 

- Corresponding author. 

_E-mail address:_ zhangridong@hdu.edu.cn (R. Zhang). 

https://doi.org/10.1016/j.psep.2026.108964 

Received 30 March 2026; Received in revised form 14 April 2026; Accepted 6 May 2026 

Available online 9 May 2026 

0957-5820/© 2026 Institution of Chemical Engineers. Published by Elsevier Ltd. All rights are reserved, including those for text and data mining, AI training, and similar technologies. 

> _C. Lv et al.                                                                                                                                                                                                                                       Process Safety and Environmental Protection 213 (2026) 108964_ 

(SVM), Principal Component Analysis(PCA), Random Forest(RF), K-Nearest Neighbor(KNN) and Fisher Discrimination Analysis (FDA). Supported by solid mathematical foundations, clear physical interpretations and high computational efficiency, these methods established a reliable theoretical framework for process monitoring and achieved remarkable results in industrial practice. Probabilistic graphical models represented by Bayesian Networks (BN) (Guo et al., 2021; Amin et al., 2018) have received extensive attention and been widely applied in process monitoring due to their excellent interpretability and uncertainty reasoning ability. Amin et al (Amin et al., 2021a). further integrated PCA and BN to develop a data-driven fault detection and diagnosis (FDD) approach. This method automatically selects principal components using the correlation dimension (CD) and achieves adaptive – learning of Bayesian networks based on Kullback Leibler divergence (KLD) and copula theory. By employing vine copula and Bayes’ theorem to capture nonlinear dependencies in high-dimensional process data, the proposed approach avoids the discretization of continuous variables and effectively extends the applicability of the PCA-BN framework to complex industrial processes. Ghosh et al (Ghosh et al., 2020). addressed the challenges in process safety assessment arising from the nonlinear dependencies among highly correlated variables in multivariate process systems. They introduced copula functions into the Bayesian network model to characterize the complex dependencies and interactions among process variables in fault formation. The proposed copula-BN coupling framework effectively overcomes the difficulty of traditional Bayesian networks in handling nonlinear and non-Gaussian dependence structures, providing an effective tool for online monitoring and risk management of industrial processes. Besides, Don et al (Don and Khan, 2019). developed a hybrid FDD method by combining data-driven and knowledge-driven paradigms. In their framework, a Hidden Markov Model (HMM) is adopted for anomaly detection, and BN is used for root cause diagnosis. The HMM is trained with normal operation data to identify anomalies, while the BN structure is built based on process knowledge and its parameters are determined using log-likelihood values from historical data. The outputs of HMM are then used as evidence for the BN to locate fault roots. 

With their intuitive causal reasoning and efficient uncertainty handling capabilities, these methods performed well in the early development of fault detection theory and laid an important methodological foundation for subsequent research. However, with the evolution of modern industry, new characteristics such as massive data, highdimensional variables and strong coupling have posed great challenges to fault detection, diagnosis and control design. Such methods are difficult to adapt to dynamic operating environments (Yu and Zhao, 2019), and their fault diagnosis performance is therefore limited. 

Unlike shallow neural network methods, deep learning methods (Zhang et al., 2023; Alauddin et al., 2023) exhibit significant advantages in handling massive amounts of data. Leveraging their end-to-end self-learning capabilities, deep learning methods have achieved breakthroughs in the field of industrial process fault diagnosis (Wu et al., 2026a; Zarei et al., 2023) and have become a key technology for solving complex industrial data modeling problems. Convolutional Neural Network(CNN) (Arunthavanathan et al., 2021b; Chen and Zhang, 2026), based on the shared characteristics of local receptive fields and weights, excel at extracting spatial multi-scale features from data and have been widely applied to fault feature extraction from vibration signals and sensor data. Long Short-Term Memory Network(LSTM) (Yu, et al., 2024) effectively alleviate the vanishing gradient problem through gating mechanisms, accurately capture long-term dependencies in time series data, and provide strong support for dynamic modeling of fault evolution processes. Generative Adversarial Network (GAN) (Yang et al., 2021b), through bidirectional adversarial training of generators and discriminators, can efficiently generate high-quality fault samples and purify weak fault features, offering an effective solution for fault diagnosis and anomaly detection in scenarios with small samples and strong noise. Residual Network(ResNet) (Sun et al., 2022), by introducing 

residual connections and identity mappings, effectively solve the vanishing gradient problem in deep networks. They enable the construction of deeper models to learn richer abstract features, significantly enhancing the depth and robustness of fault feature extraction. The incorporation of attention mechanisms (Hassanin et al., 2024; Tang et al., 2025; He et al., 2025) allows fault diagnosis models to adaptively assign weights to features from different sensor channels and time steps, strengthening the extraction of fault-sensitive information, improving the model's diagnostic accuracy and robustness under complex operating conditions, and achieving interpretability in the fault diagnosis process. 

However, existing methods still have shortcomings: Firstly, singlescale convolutional kernels struggle to comprehensively cover the multi-scale feature (Song and Jiang, 2022) distribution of industrial faults. For instance, weak features of early minor faults and strong features of severe faults often reside in different scale spaces, potentially leading to the omission of crucial fault information. Secondly, industrial sensor data often contains a significant amount of background noise and redundant information (Xiao et al., 2021). Traditional models lack effective mechanisms for feature enhancement and noise suppression, and convolutional kernels are susceptible to interference from irrelevant information, resulting in learned features lacking discriminative power. Thirdly, the fusion of temporal and spatial features lacks targeted optimization, which fails to fully explore the intrinsic correlation between spatial-temporal features in the fault evolution process and makes it difficult to accurately characterize the dynamic evolution trajectory of faults. 

Existing relevant research provides important references for addressing the aforementioned issues. Zhao et al. (2020) proposed the Deep Residual Shrinkage Network(DRSN), which effectively suppresses noise by embedding a soft threshold layer in the residual block, verifying the effectiveness of attention mechanisms and feature shrinkage strategies in strong noise environments. Chen et al. (2026) proposed a fusion model of a parallel CNN, which enables the model to adaptively focus on fault-related features. However, in the field of industrial fault diagnosis, how to simultaneously achieve comprehensive extraction of multi-scale features, effective suppression of noise and redundant information, and deep fusion of spatial-temporal features remains a key issue that needs to be urgently addressed. 

To address the above challenges, this paper proposes an Inception Self-Adaptive Efficient Channel Attention Bidirectional Long Short-Term Memory (Inception-SECA-BiLSTM) model, which is a diagnosis framework that achieves simultaneous multi-scale feature capture, noise suppression, and spatial-temporal feature fusion. 

The main contributions of this paper: 

- 1) An Inception Self-Adaptive Efficient Channel Attention (InceptionSECA) fusion module is constructed, which uses multi-scale convolution branches of 1× 1, 3× 1, and 5× 1 to extract fault features at different scales in parallel. Combined with the Self-Adaptive Efficient Channel Attention (SECA) module, it adaptively enhances critical channel features to achieve accurate extraction of multi-scale spatial information. 

- 2) The Bidirectional Long Short-Term Memory (BiLSTM) (Liu et al., 2025; Zeng et al., 2024) and a Single-Head Scaled Dot-Product Self-Attention(SH-SA) mechanism are introduced to capture deep temporal dependencies of industrial process temporal signals, improving the model’s ability to distinguish complex fault patterns. 

- 3) A average-max-endpoint Feature Aggregation(FA) strategy is designed to fuse global average, global max, and last instantaneous features, effectively integrating fault features and enhancing the model’ s robustness and overall classification performance. 

The rest of this paper is structured as follows: Section 2 provides a detailed introduction to the fault diagnosis model proposed in this paper. Section 3 describes the details of the Tennessee Eastman (TE) 

2 

> _C. Lv et al.                                                                                                                                                                                                                                       Process Safety and Environmental Protection 213 (2026) 108964_ 


![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0003-01.png)


**Fig. 1.** Structure diagram of the Inception-SECA-BiLSTM model. 


![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0003-03.png)


**Fig. 2.** Structure diagram of the SECA module. 

process dataset and the coke furnace dataset. Section 4 verifies the overall diagnostic performance of the proposed model through experiments. Section 5 provides a systematic summary of the research work presented in this paper. 

#### **2. Proposed method** 

The Inception-SECA-BiLSTM model proposed in this paper follows a design approach that encompasses multi-scale local feature extraction, key feature enhancement, and efficient feature aggregation and classification. This model deeply integrates the advantages of convolution, attention mechanisms, and recurrent neural networks, enabling comprehensive mining and accurate modeling of industrial data features. 

The model uses Inception structures as the basic feature extraction unit, employs a multi-branch parallel structure to capture local features from data at different scales, and innovatively embeds the SECA module 

to adaptively perform key feature weighting and noise suppression. By combining residual connections to optimize deep network training, it alleviates the vanishing gradient problem, ensuring the stability and effectiveness of feature extraction in the model. Subsequently, the BiLSTM combined with the SH-SA module is adopted to simultaneously capture the bidirectional temporal dependencies and global correlations of the sequence. The FA module integrates average, maximum, and endpoint features to maximize discriminative information retention. In the model, regularization methods such as dropout, batch normalization, and layer normalization are added to effectively suppress overfitting. The model as a whole possesses strong feature expression capabilities and stable training performance, enabling it to effectively capture deep features of data and maintain robustness during the training process. Fig. 1 illustrates the detailed structure of the InceptionSECA-BiLSTM model. 

The proposed model adopts a modular design, in which each component addresses a specific task in feature learning, including multiscale feature extraction, channel-wise feature enhancement, temporal dependency modeling, and feature aggregation. Such a structured framework enables flexible adjustment of individual modules. 

Although multiple components are integrated, each module is designed to be lightweight. For instance, the SECA module dispenses with fully connected layers, the SH-SA module employs a simplified selfattention structure, and the FA module achieves parameter-free feature fusion. Consequently, the overall model maintains moderate computational complexity. 

Furthermore, the proposed framework is not restricted to any specific data structure. Instead, it is designed to capture the general inherent characteristics of industrial process data, including multi-scale correlations, variable coupling, and temporal dependencies. From a practical perspective, the model can be efficiently implemented using standard deep learning frameworks. Benefiting from its modular architecture, it can be conveniently adapted or simplified to meet specific industrial requirements, thereby improving its applicability in realworld scenarios. 

#### _2.1. SECA module_ 

The SECA module is a lightweight 1D channel attention mechanism derived from efficient channel attention (ECA) (Wang et al., 2020), which is designed to adaptively recalibrate channel-wise feature responses with minimal computational overhead. Unlike conventional attention mechanisms that rely on fully connected layers, SECA adopts one-dimensional convolution with an adaptive kernel size to capture local cross-channel interactions, thereby avoiding parameter-intensive operations. 

In the proposed framework, SECA is specifically introduced to 

3 

> _C. Lv et al.                                                                                                                                                                                                                                       Process Safety and Environmental Protection 213 (2026) 108964_ 


![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0004-01.png)


**Fig. 3.** Structure diagram of the Inception-SECA module. 

enhance channel-wise feature discrimination for multivariable industrial process data, where different process variables exhibit varying degrees of relevance to fault characteristics. By assigning adaptive weights to each channel, SECA improves the representation quality of discriminative variables while suppressing redundant or noisy features. Furthermore, a lightweight dropout strategy is incorporated to improve generalization and reduce the risk of overfitting, especially given limited fault samples. Importantly, SECA operates at the channel-feature level and does not model temporal dependencies, making it complementary to the subsequent BiLSTM and SH-SA modules. 

The specific structure of the SECA module is shown in Fig. 2, and its workflow can be divided into the following three key steps: Firstly, perform global average pooling and feature compression operations on the input feature to effectively aggregate spatial dimension feature information; Secondly, through one-dimensional convolution operations with adaptive kernels, the intrinsic dependencies between different channels are accurately captured, and then processed by sigmoid activation functions to generate normalized channel weight vectors, achieving precise evaluation of channel importance; Thirdly, the generated channel weights are fused with the original input features through channel wise weighted fusion to complete the feature recalibration process, thereby enhancing the effective features that are key to improving model performance and suppressing redundant information and noise interference. 

Input data _X_ ∈ R<sup>_B_×</sup><sup>_C_×</sup><sup>_L_</sup> , where _B_ is the batch size, _C_ is the number of input channels, and _L_ is the temporal length. 

Adaptive convolution kernel calculation: The proposed kernel calculation formula adaptively determines the convolution kernel size based on the number of input channels, while integrating three key design principles: (1) adaptive kernel size determined by channel number to match feature scales; (2) odd-size constraint to ensure symmetric padding and feature alignment; (3) upper bound of 7 to avoid overfitting and maintain computational efficiency for industrial smallsample datasets. This design realizes the adaptive modeling of channel dependencies. 


![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0004-07.png)


where the model hyperparameters setting is _γ_ = 2, _b_ = 1, and _k_ is the 

final convolution kernel size. 

Squeeze: aggregate the feature dimension information through adaptive average pooling to obtain the global features of the channel: _z_ = _AdaptiveAvgPool_ 1 _d_ ( _X_ ) _z_ ∈ R<sup>_B_×</sup><sup>_C_×1</sup> (2) 

where _X_ ∈ R<sup>_B_×</sup><sup>_C_×</sup><sup>_L_</sup> is the concatenated feature of the 4 branches of the Inception module, and _z_ is the global feature of the channel after adaptive average pooling. 

Excitation: transpose the feature to adapt the convolution input, extract the channel dependence through one-dimensional convolution, – and generate the channel weight of 0 1 interval through dropout regularization and sigmoid activation: 

_ztrans_ = _Transpose_ ( _z,_ − 1 _,_ − 2) _ztrans_ ∈ R<sup>_B_×1×</sup><sup>_C_</sup> (3) 


![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0004-14.png)



![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0004-15.png)


> where _σ_ is the sigmoid activation function, _ztrans_ is the transposed feature 

> for convolution input adaptation, _ωconv_ is the channel weight extracted by 1D convolution, _ω_ is the regularized weight after dropout and sig- 

> moid activation, and _ωfinal_ ∈ R<sup>_B_×</sup><sup>_C_×1</sup> is the final channel attention weight. 

Feature recalibration: After expanding the dimensionality of channel weights through the broadcasting mechanism, element-wise multiplication is performed with the original features to achieve adaptive recalibration and enhancement of features: 


![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0004-18.png)


where ⨀ represents element by element multiplication, and _Y_ is the output characteristic of SECA module. 

#### _2.2. Inception-SECA module_ 

The Inception-SECA fusion module is designed to jointly perform multi-scale feature extraction and channel-wise feature enhancement. By integrating the multi-branch parallel structure of Inception (Wu et al., 2026b) with the SECA module, the model is capable of capturing diverse local patterns under different receptive fields while adaptively emphasizing informative feature channels. The Inception-SECA module focuses on spatial feature representation learning without modeling temporal dependencies, thus providing complementary inputs for the subsequent BiLSTM-based temporal analysis. 

The structure of the Inception-SECA module is shown in Fig. 3. This module constructs a four-branch parallel multi-scale feature extraction structure: the first branch directly extracts fine-grained local features and achieves channel dimensionality reduction via a 1× 1 1D convolu× 1 convolu- tion; the second branch first reduces dimensions with a 1 tion and then captures medium-scale feature patterns using a 3 × 1 1D × 1 convolution; the third branch first reduces dimensions with a 1 convolution and then mines wide-scale long-range correlations through a 5 × 1 1D convolution; and the fourth branch efficiently aggregates global contextual information by employing average pooling followed by a 1 × 1 convolution. 

After concatenating the outputs of the four branches along the channel dimension, the SECA module is introduced to weight and enhance channel-wise features for highlighting critical fault information and suppressing noise interference, and finally outputs the enhanced multi-scale fused features. Batch normalization(BN) (Muhammad et al., 2023) and ReLU activation function (Eckle and Schmidt-Hieber, 2019) are added inside the module to ensure training stability, and over fitting is alleviated through dropout. This structure breaks through the defects 

4 

_Process Safety and Environmental Protection 213 (2026) 108964_ 

> _C. Lv et al.                                                                                                                                                                                                                                       Process and Environmental Protection_ 


![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0005-02.png)


**Fig. 4.** Structure diagram of the LSTM module. 

of the traditional convolution single receptive field limitation and the separation design of attention mechanism, realizes multi-scale extraction and feature screening end-to-end learning, and greatly improves the ability of feature expression. 

The input feature is _X_ ∈ R<sup>_B_×</sup><sup>_Cin_×</sup><sup>_L_</sup> , and the output feature is _Y_ ∈ R<sup>_B_×</sup><sup>_Cout_×</sup><sup>_L_</sup> . 

Four branches multiscale feature extraction: 


![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0005-07.png)



![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0005-08.png)



![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0005-09.png)



![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0005-10.png)


through the entire temporal. The cell state enables relatively stable information transmission across each time step of the temporal, allowing the network to memorize long-range dependencies. Information flow is regulated by the forget gate, input gate, cell state, and output gate, which preserve long-term memory, filter redundant information, and alleviate the vanishing gradient problem. 

Forget gate: each time a new input is input, LSTM will first determine which memories are forgotten according to the new input and the output of the previous time step. The input and the output of the previous step will be integrated into a separate vector, which will be mapped to the value between 0 and 1 through the sigmoid activation function. A value close to 0 indicates that the corresponding cell state information will be forgotten, and a value close to 1 indicates that the information will be retained. In this way, LSTM can remember important information for a long time, and the memory can be dynamically adjusted with input. The calculation formula of forget gate is as follows: 


![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0005-13.png)


> where _σ_ is the sigmoid activation function, _ft_ is the output of the forget gate at time step _t_ , _Wf_ and _bf_ are the weight matrix and bias vector of the forget gate respectively, _ht_ − 1 is the hidden state of the previous time step, and _xt_ is the input feature at the current time step. 

Input gate: It controls how much of the current input information is updated into the cell state. Similarly, it takes the current input and the output from the previous time step as inputs. An update ratio is calculated through the sigmoid function, while the current input is transformed using the tanh activation function. The two results are multiplied to obtain the information to be updated into the cell state. The formulas of the input gate are presented as follows: 


![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0005-16.png)


where _X_ 1 _, X_ 2 _, X_ 3 _, X_ 4 are the outputs of the four branches respectively. After each branch, the ReLU activation function is used to realize the nonlinear transformation. 

Multi-scale feature concatenation: concatenate the outputs of four branches in the channel dimension: 


![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0005-19.png)


where, _Fconcat_ is the multi-scale fused feature after channel concatenation, and the concatenated feature has a channel dimension of _Cout_ = 4 _Cin_ . 

The SECA recalibration: 


![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0005-22.png)


where _Fatt_ is the attention-enhanced feature. Dropout regularization: 


![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0005-24.png)


#### _2.3. BiLSTM module_ 

After multi-scale spatial feature extraction, a BiLSTM module is introduced to model temporal dependencies and capture long-range contextual information from sequential feature representations. Unlike convolutional operations that focus on local patterns, BiLSTM is capable of learning bidirectional temporal dynamics, which is particularly important for industrial processes where fault evolution may depend on both past and future observations. 

In this framework, the BiLSTM operates on the high-level spatial features extracted by the Inception-SECA module, and focuses on modeling temporal correlations across feature sequences. This enables the network to learn the dynamic coupling relationships among process variables over time. 

The structure of the LSTM module is shown in Fig. 4. The core of LSTM is the cell state, which acts as an information conveyor running 


![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0005-29.png)


where _Wi_ , _bi_ , _Wc_ and _bc_ are the correlation weight matrix and bias vector of the input gate, respectively. _it_ denotes the output of the input gate at time step _t_ controlling the amount of new information stored, and _Ct_ represents the candidate cell state vector generated at current time step _t_ . 

Cell state update: The cell state is updated according to the outputs of the former forget gate and input gate. The specific formula is given as follows: 


![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0005-32.png)


where _Ct_ is the updated cell state at time step t, _Ct_ − 1 is the cell state of the previous time step, and ⨀ represents element by element multiplication. 

Output gate: It determines which information in the cell state is output as the hidden state at the current time step. Taking the input of the current time step and the hidden state of the previous time step, it calculates an output ratio via the sigmoid function. This ratio is then multiplied by the cell state processed through the tanh activation function to obtain the hidden state at the current time step. The formulas for the output gate are given as follows: 


![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0005-35.png)



![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0005-36.png)


where _Wo_ and _bo_ are the weight matrix and bias vector of the output gate, respectively. _ot_ denotes the output of the output gate at time step _t_ , and _ht_ represents the hidden state of the LSTM unit at time step _t_ . 

Unlike the unidirectional LSTM, BiLSTM consists of two independent networks, namely the forward and backward branches. It can model the contextual dependencies of temporal features from both forward and backward directions simultaneously, and more comprehensively 

5 

> _C. Lv et al.                                                                                                                                                                                                                                       Process Safety and Environmental Protection 213 (2026) 108964_ 


![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0006-01.png)


LSTM traversing the temporal, respectively. _H_ represents the dimension of the unidirectional hidden layer. _ht_ is the input feature at time step _t_ ,<sup>→</sup> _h t_ − 1<sup>denotes the hidden state of the forward LSTM at the previous time</sup> step, and<sup>←</sup> _h t_ +1<sup>denotes the hidden state of the backward LSTM at the</sup> next time step. →= _H_<sup>→</sup> _h_ 1<sup>_,_→</sup><sup>_h_</sup> 2<sup>_,_⋯</sup><sup>_,_→</sup><sup>_h_</sup> _L_ and ←= _H_<sup>←</sup> _h_ 1<sup>_,_←</sup><sup>_h_</sup> 2<sup>_,_⋯</sup><sup>_,_←</sup><sup>_h_</sup> _L_ are the [ ] [ ] complete hidden state sequences of the forward and backward LSTM, respectively, and _Hbi_ denotes the bidirectional fused feature after concatenation. 

To ensure training stability and accelerate convergence, layer normalization is adopted following the BiLSTM output to normalize feature distributions: _Hnorm_ = _LayerNorm_ ( _Hbi_ ) (24) 

**Fig. 5.** Structure diagram of the BiLSTM module. 

where _Hnorm_ is the normalized feature with stabilized distribution. 


![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0006-06.png)


**Fig. 6.** Structure diagram of the SH-SA module. 

capture the information correlations between past and future in temporal data, thereby improving the model's representation ability and global understanding of temporal features. The structure of the BiLSTM module is illustrated in Fig. 5. 

Input feature: _H_ = [ _h_ 1 _, h_ 2 _,_ ⋯ _, hL_ ] ∈ ℝ<sup>_B_×</sup><sup>_L_×</sup><sup>_D_</sup> , where _B_ is the batch size, _L_ is the temporal length, and _D_ is the input feature dimension. The BiLSTM is computed as follows: 


![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0006-10.png)



![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0006-11.png)


where<sup>→</sup> _h t_<sup>and ←</sup><sup>_h_</sup> _t_<sup>denote the hidden states of the forward and backward</sup> 

#### _2.4. SH-SA module_ 

To further enhance the temporal feature representation, a SH-SA module is designed to refine the sequential features produced by the BiLSTM. Specifically, the module generates query, key, and value representations through linear projections and computes attention weights via the scaled dot-product mechanism. A residual connection is incorporated to stabilize training and mitigate gradient vanishing. 

Unlike the BiLSTM, which focuses on modeling temporal dependencies and sequence dynamics, the SH-SA module operates on the outputs of the LSTM to adaptively re-weight feature representations across different time steps. This enables the model to selectively emphasize critical temporal information and suppress less informative or noisy components from a global perspective. The structure of the SHSA module is illustrated in Fig. 6. 

Input feature: _H_ ∈ R<sup>_B_×</sup><sup>_L_×</sup><sup>_D_</sup> , where _B_ denotes the batch size, _L_ denotes the temporal length, and _D_ denotes the input feature dimension. Query, Key, and Value ( _Q_ , _K_ , _V_ ) are generated via linear projection: 


![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0006-17.png)



![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0006-18.png)


Scaled dot-product attention calculation: It prevents the inner product values from becoming excessively large, which would otherwise force Softmax into its saturated region: _QK_<sup>_T_</sup> _Satt_ = ~~√~~ _D_ (28) 

where _Satt_ is the scaled attention score matrix, _Q_ is the query matrix, _K_ is the key matrix, and √ _D_ is the scaling factor. Normalize to generate attention weights: 


![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0006-21.png)


where _A_ is the final attention weight matrix after Softmax. Weighted summation and dropout regularization: 


![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0006-23.png)


where _V_ is the value matrix, _A_ • _V_ is the weighted summation of value features, and _Hatt_ is the attention-enhanced feature after dropout regularization. 

Linear projection and residual connection: 


![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0006-26.png)


where _Hout_ denotes the features enhanced by attention weighting and fused with the input information. 

6 

_Process Safety and Environmental Protection 213 (2026) 108964_ 


![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0007-02.png)


**Fig. 7.** Visualization of the learned weight matrix of the classification layer. 


![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0007-04.png)


**Fig. 8.** Flowchart of the TE process. 

_2.5. FA module_ 

To effectively integrate the global temporal features produced by the SH-SA module, a FA module is designed to reduce information loss caused by relying on a single pooling strategy. Instead of using only one type of pooling operation, the FA module combines average pooling, max pooling, and endpoint features to capture complementary 

information from the temporal representations. Let the output features of the SH-SA modules be _H_ ∈ R<sup>_B_×</sup><sup>_L_×</sup><sup>_D_</sup> , where _B_ denotes the batch size, _L_ denotes the temporal length, and _D_ denotes the input feature dimension. 

The calculation formulas for average pooling features, max pooling features, and endpoint features are given as follows: 

7 

> _C. Lv et al.                                                                                                                                                                                                                                       Process Safety and Environmental Protection 213 (2026) 108964_ 

##### **Table 1** 

##### **Table 3** 

Faults description of the TE process. 

Model parameters of Inception-SECA-BiLSTM fault diagnosis network. 

|Number|Fault Description|Type|Module|Layer(type)|Param|
|---|---|---|---|---|---|
|1|A/C feed ratio, B composition constant (stream 4)|Step|Input|Input|/|
|2|A/C feed ratio, B composition constant (stream 4)|Step|Feature extraction|Inception_SECA_Block|In_channels=1, Out_channels|
|3|D feed temperature (stream 2)|Step|module|1|=64, Dropout=0.1|
|4|Reactor cooling water inlet temperature|Step||AvgPool1d|Kernel size=2, stride=1,|
|5|Condenser cooling water inlet temperature|Step|||padding=1|
|6|A feed loss (stream 1)|Step||Skip connection 1|Conv1d(64→128, kernel=1×1),|
|7|C header pressure loss-reduced availability (stream|Step|||BatchNorm1d(128)|
||4)|||Inception_SECA_Block|In_channels=64, Out_channels|
|8|A, B, C feed composition (stream 4)|Random||2|=128, Dropout=0.1|
|||variation||Skip connection 2|Conv1d(128→128, kernel=1×1),|
|9|D feed temperature (stream 2)|Random|||BatchNorm1d(128)|
|||variation||Inception_SECA_Block|In_channels=128,|
|10|C feed temperature (stream 4)|Random<br>variation||3|Out_channels=128, Dropout<br>=0.1|
|11|Reactor cooling water inlet temperature|Random<br>variation|Temporal modeling<br>module|Permute|(batch, channels, seq)→(batch,<br>seq, channels)|
|12|Condenser cooling water inlet temperature|Random<br>variation||BiLSTM|Input dim=128, Hidden<br>size=128, layers=2,|
|13|Reaction kinetics|Slow drift|||Bidirectional=True, Dropout|
|14|Reactor cooling water valve|Sticking|||=0.1|
|15|Condenser cooling water valve|Sticking||LayerNorm|Normalized shape=(batch, seq,|
|16–20|Unknown|Unknown|||256)|
|21|Valve position constant (stream 4)|Constant position||SH-SA|Hidden dim=256,<br>Self-attention+Residual<br>connection|
||||Feature<br>|FeatureAggregation|Mean pooling+Max pooling<br>|
||||aggregation||+Endpoint|
||||module<br>|||
||||Classifcation|Linear|In_features=256, Out_features|
||||module||=64|
|||||BatchNorm1d|num_features=64|
|||||ReLU<br>Dropout|/<br>p=0.1|
|||||Linear|In_features=64, Out_features|
||||||=num_classes|




![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0008-06.png)



![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0008-07.png)


**Fig. 10.** Effect of γ on accuracy. 


![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0008-09.png)


**Fig. 9.** Structure of the industrial coke furnace F101/3. 

**Fig. 11.** Effect of initial learning rate on accuracy. 

##### **Table 2** 

Fault description of the coke furnace process. 

|Number|Fault Description|Type|
|---|---|---|
|1|Step signal, oxygen content 2|Step|
|2|Step signal, oxygen content 1|Step|
|3|Slow drift signal, temperature measurement point B|Drift|
|4|Random signal, temperature measurement point B<br>|Other|
|5|Step signal, thermal effciency measurement point|Step|




![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0008-15.png)



![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0008-16.png)


where _Ht_ denotes the feature at time step t in the sequence, _Favg_ is the average pooling feature obtained by averaging all time-step features, _F_ max is the max pooling feature obtained by taking the maximum value across time-step features, and _Flast_ is the endpoint feature extracted from the last time step of the sequence. 

Weighted fusion of three types of features: 


![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0008-19.png)


The final output _Ffinal_ ∈ R<sup>_B_×</sup><sup>_D_</sup> represents the aggregated fixed- 

8 

> _C. Lv et al.                                                                                                                                                                                                                                       Process Safety and Environmental Protection 213 (2026) 108964_ 


![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0009-01.png)


**Fig. 12.** SECA channel attention weight distributions for representative fault classes of TE process. 

dimensional feature vector, which is fed into the classification layer to complete prediction. 

The FA module extracts features from three perspectives: global statistical characteristics, salient discriminant information, and final state representations. By weighted averaging to fuse complementary information, it maximally preserves effective discriminative features and avoids key information loss caused by single pooling, thereby providing compact and highly discriminative features for subsequent classification tasks. 

#### _2.6. Classification module_ 

The classification module takes the comprehensive features output by the FA module as input, and adopts a two-layer fully connected structure of 256→64 and 64→21, combined with batch normalization, ReLU activation function and dropout regularization strategy. It effectively suppresses overfitting while ensuring classification accuracy, improving the generalization ability and inference stability of the model. The final output layer of the model produces raw predicted logits corresponding to the 21 fault types. After normalization by the softmax function, a standardized probability vector summing to 1 is generated, 

where each element in the vector represents the model's prediction confidence for the corresponding fault category. The softmax function is defined as follows: 


![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0009-08.png)


where _Fi_ denotes the output of the _i_ th neuron in this layer, _Pi_ denotes the probability of _Fi_ , and _C_ denotes the number of categories involved in the multi-classification task. 

The cross-entropy loss function is employed to quantify the discrepancy between the predicted label and the actual label, which is defined as follows: 


![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0009-11.png)


where _N_ denotes the number of samples, _yi_ and _y_<sup>ʹ</sup> _i_<sup>denotes the actual</sup> label and prediction label of samples respectively. The Adam (Chen et al., 2023b) optimization algorithm is adopted to train the model, aiming to minimize the cross-entropy loss and enable the model to achieve optimal performance. 

9 

> _C. Lv et al.                                                                                                                                                                                                                                       Process Safety and Environmental Protection 213 (2026) 108964_ 

**Table 4** 

Precision and recall of the inception-SECA-BiLSTM model and its ablation models for the TE process. 

|Fault number|w/o I-SECA||w/o BiLST|M|w/o FA||w/o SH-SA||Proposed||
|---|---|---|---|---|---|---|---|---|---|---|
||P|R|P|R|P|R|P|R|P|R|
|1|100.00|100.00|99.62|100.00|100.00|100.00|100.00|100.00|**100.00**|**100.00**|
|2|100.00|98.74|99.57|97.48|100.00|98.32|100.00|99.16|**100.00**|**99.58**|
|3|78.29|85.27|67.62|73.64|85.66|90.31|95.74|95.74|**97.70**|**98.84**|
|4|95.44|99.60|94.01|99.60|94.72|99.60|**96.18**|100.00|95.82|**100.00**|
|5|**98.78**|98.78|97.98|99.18|91.60|97.96|91.76|100.00|96.46|**100.00**|
|6|100.00|100.00|100.00|100.00|100.00|100.00|100.00|100.00|**100.00**|**100.00**|
|7|100.00|100.00|99.60|100.00|100.00|100.00|100.00|100.00|**100.00**|**100.00**|
|8|98.22|98.57|99.63|96.07|98.93|98.93|100.00|98.93|**100.00**|**99.29**|
|9|70.96|91.10|68.16|77.12|76.11|94.49|88.51|97.88|**96.68**|**98.73**|
|10|94.22|88.70|93.07|89.96|91.85|89.54|98.68|94.14|**99.16**|**98.74**|
|11|95.36|82.48|95.54|78.10|94.42|80.29|97.24|90.15|**97.67**|**91.61**|
|12|**99.21**|95.82|98.40|93.54|99.20|94.68|98.44|96.20|98.46|**96.96**|
|13|99.59|97.19|98.74|94.38|99.59|96.39|98.81|**100.00**|**99.60**|99.20|
|14|98.86|97.75|99.23|97.00|99.62|97.38|99.24|97.38|**100.00**|**98.88**|
|15|77.21|86.42|68.09|79.01|83.67|84.36|**96.67**|95.47|96.03|**99.59**|
|16|97.31|89.06|95.49|89.44|95.44|88.38|92.38|**98.24**|**99.28**|97.18|
|17|97.72|94.83|97.33|94.10|**97.75**|96.31|97.09|98.52|97.46|**99.26**|
|18|99.59|94.51|98.78|94.90|98.78|94.90|**100.00**|96.86|99.60|**97.25**|
|19|88.07|85.60|87.45|86.40|85.11|89.20|97.10|93.60|**97.98**|**97.20**|
|20|95.07|90.21|93.21|87.66|91.59|88.09|98.62|91.49|**98.71**|**97.87**|
|21|94.44|96.36|82.82|97.57|93.28|95.55|97.19|97.98|**98.80**|**100.00**|
|Micro-avg|93.88|93.88|91.73|91.73|94.04|94.04|97.24|97.24|**98.55**|**98.55**|
|Macro-avg|94.21|93.86|92.11|91.67|94.16|94.03|97.32|97.23|**98.54**|**98.58**|




![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0010-04.png)


**Fig. 13.** F1-score values of the four models for faults 3, 9, 11, 15, and 19. 

To improve the interpretability of the decision-making process, we analyze the weight matrix of the final fully connected layer. As shown in Fig. 7, the weight matrix illustrates how each fault class is associated with the learned latent feature space. Specifically, the vertical axis (Fault Class) represents the 21 fault categories, while the horizontal axis (Feature Dimension) denotes the 64-dimensional compressed latent features. The color gradient indicates the strength of the association, with brighter colors representing higher weights. 

As illustrated in Fig. 7, different fault classes exhibit distinct and class-specific activation patterns across the compressed feature dimensions. This indicates that the final prediction is driven by structured and discriminative latent features, rather than an opaque black-box mapping. By analyzing the learned weight matrix, the decisionmaking process can be explicitly interpreted, revealing class-specific sensitivities in the latent feature space. 

#### **3. Dataset description** 

#### _3.1. The TE process dataset_ 

According to the actual chemical reaction process, Eastman Chemical Company of the United States has developed an open and challenging chemical model simulation platform Tennessee Eastman (TE) simulation platform (Amin et al., 2021b). The data generated by the platform has strong coupling and nonlinear characteristics. It is now used as a benchmark for evaluating and testing the fault diagnosis and monitoring technology of chemical processes, and is widely used to test the control and fault diagnosis models of complex chemical processes. The specific process of TE process is shown in Fig. 8, which mainly includes five components: reactor, condenser, gas-liquid separator, circulating compressor and stripper. 

The TE process dataset was obtained through simulation experiments. For the training set, there are 480 observation samples for each 

10 

> _C. Lv et al.                                                                                                                                                                                                                                       Process Safety and Environmental Protection 213 (2026) 108964_ 


![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0011-01.png)


**Fig. 14.** Visualization of fault diagnosis results for the Inception-SECA-BiLSTM model on the TE process. 

fault type. For the test set, 960 samples are generated for each fault type, where the first 160 samples correspond to steady-state normal data. Table 1 provides detailed descriptions of the various faults. In the experiment, the 12th manipulated variable, which remained constant throughout the process, was removed, while 41 measured variables and 11 manipulated variables were retained. The dataset contains a total of 26,880 fault samples, with each of the 21 fault types characterized by 52 data variables. Following normalization preprocessing and labeling, the dataset is split into training and test sets with an 8:2 ratio. 

#### _3.2. The industrial coke furnace dataset_ 

The industrial coke furnace F101/3 is a vertical tubular heater widely used in advanced processing in oil refining, petrochemical and other chemical industries. Its working process is orderly carried out around the three core links of heating, fractionation and coke removal. The specific process is as follows: 

Initially, untreated residual oil enters the convection chamber from both sides of the coke furnace, and is preheated to about 330℃ before merging, and then is transported to the bottom of the fractionator (T102). Inside the fractionator, this part of the oil undergoes heat and mass transfer with the overhead steam, in which the lighter components evaporate and enter the fine distillation process, while the raw material and the condensed components of the steam at the top of the coke tower flow together into the bottom of the tower to form the tower bottom oil with a temperature of about 360℃ (TR8121); The tower bottom oil is pumped to the radiation section of the heating furnace in two streams. After that, the tower bottom oil is rapidly heated to 495℃ in the radiation section (TRC8103 in the south and TRC8105 in the north). After heating, it is transported to the coke drum (T101/5,6), and finally the 

coking process is completed. Fig. 9 shows the relevant processes, which are described in more detail in (Zhu and Zhang, 2026). 

During the experiment, various fault scenarios were artificially constructed by simulating step signals, slow drift variables and random variables at different measurement points, and the normal operation status was set as the control group. For each fault type and normal state, 1000 data samples were collected, and finally a coke furnace specific data set containing five kinds of fault data and one kind of normal data was constructed. Detailed descriptions of various faults are listed in Table 2. After normalization preprocessing and labeling, a total of 6000 samples were divided into training and testing sets in an 8:2 ratio for subsequent correlation analysis. 

#### **4. Experiments and assessments** 

To quantitatively analyze and evaluate the model performance, diagnostic accuracy, precision, recall, F1-score (Zhang et al., 2025), and Cohen’ s Kappa coefficient are adopted as key evaluation metrics. Precision focuses on the prediction reliability of positive samples and reflects the prediction accuracy of the model, where a value closer to 1 indicates better precision. Recall measures the proportion of correctly identified true positive samples and characterizes the detection capability, with higher values representing superior performance. As the harmonic mean of precision and recall, the F1-score effectively alleviates evaluation bias caused by imbalanced sample distribution; a higher F1-score corresponds to better overall performance. Cohen’s Kappa coefficient quantifies the consistency between predicted labels and actual labels in multi-class tasks, ranging from − 1–1. A value of 1 represents perfect consistency, a value near 0 indicates performance comparable to − random guessing, and a value of 1 means complete inconsistency 

11 

> _C. Lv et al.                                                                                                                                                                                                                                       Process Safety and Environmental Protection 213 (2026) 108964_ 


![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0012-01.png)


**Fig. 15.** Confusion matrices of five models for the TE process. 

12 

> _C. Lv et al.                                                                                                                                                                                                                                       Process Safety and Environmental Protection 213 (2026) 108964_ 


![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0013-01.png)


**Fig. 16.** Training accuracy curves of the four models. 


![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0013-03.png)


**Fig. 17.** Training loss curves of the four models. 

between predictions and actual labels. The specific formulas for the above metrics are given as follows: 


![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0013-06.png)



![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0013-07.png)



![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0013-08.png)



![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0013-09.png)


where _TP_ (True Positive) represents the number of fault samples correctly identified by the model as belonging to a specific fault category; _FP_ (False Positive) represents the number of samples that do not 

actually belong to the specific fault category but are incorrectly predicted by the model as belonging to that fault category; _TN_ (True Negative) represents the number of samples correctly identified by the model as not belonging to a specific fault category, that is, the number of samples that are actually other non-target fault categories and are accurately excluded by the model from that target fault category; _FN_ (False Negative) represents the number of samples that actually belong to a specific fault category but are misclassified by the model as other categories. 

#### _4.1. The TE process_ 

#### _4.1.1. Experimental procedure_ 

Before conducting fault diagnosis experiments, the raw TE process dataset is preprocessed to eliminate dimensional differences and improve model convergence efficiency. In this study, the minimum maximum normalization method is used to map the data to the 0–1 

13 

> _C. Lv et al.                                                                                                                                                                                                                                       Process Safety and Environmental Protection 213 (2026) 108964_ 


![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0014-01.png)


**Fig. 18.** Testing accuracy curves of the four models. 


![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0014-03.png)


**Fig. 19.** Testing loss curves of the four models. 

##### **Table 5** 

Accuracy, loss and kappa of four models for the TE process. 

|Model|Accuracy(%)|Loss|Kappa value|
|---|---|---|---|
|DRSN-GRU|96.00|0.7356|0.9580|
|MA-BiTCN|93.06|0.8192|0.9271|
|SE-ResNet|94.53|0.7963|0.9425|
|Proposed|98.55|0.6628|0.9848|



range. The detailed formulations are presented as follows: 

_xi_ − _x_ min _x_<sup>∗</sup> = _x_ max − _x_ min 

(42) 

where _x_<sup>∗</sup> is the value after normalization, _xi_ is the value before normalization, _x_ min is the minimum value in the data sample, and _x_ max is the maximum value in the sample data. 

In the fault diagnosis process of the TE process, the preprocessed dataset is first fed into the Inception-SECA-BiLSTM model to execute the end-to-end fault diagnosis workflow. The model first extracts multi-scale spatial features through three stacked Inception-SECA modules: the first module maps the single-channel input to 64 channels, and the following two modules further expand and stabilize the channel number at 128. Each Inception-SECA module adopts four parallel branches composed of 1 × 1, 3 × 1, and 5 × 1 1D convolutions and average pooling to capture fine-grained, medium-scale, wide-scale, and global fault features simultaneously. After concatenating the outputs of all branches, the SECA adaptive channel attention is used to weight important features and suppress noise interference. Meanwhile, residual skip connections and average pooling downsampling are introduced between adjacent Inception-SECA modules to stabilize training, preserve core information, and alleviate network degradation. 

After obtaining high-level spatial fault features, the feature sequence 

14 

> _C. Lv et al.                                                                                                                                                                                                                                       Process Safety and Environmental Protection 213 (2026) 108964_ 

##### **Table 6** 

Results of the four models under different noise levels in the TE process. 

|Sigma<br>model|0.001|0.002|0.003|0.004|0.005|0.006|0.007|0.008|0.009|0.01|No noise|
|---|---|---|---|---|---|---|---|---|---|---|---|
|DRSN-GRU|95.72|94.98|93.98|92.12|89.94|87.08|84.46|81.49|78.71|75.99|96.00|
|MA-BiTCN|92.91|92.77|92.38|91.50|90.72|89.78|88.27|86.96|84.95|82.83|93.06|
|SE-ResNet|94.43|94.02|93.60|92.80|91.56|90.14|88.38|86.26|84.25|81.68|94.53|
|Proposed|98.39|98.31|98.17|97.82|97.40|96.75|95.52|94.47|92.44|90.33|98.55|




![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0015-04.png)


**Fig. 20.** Test accuracy of four models under various noise levels in the TE process. 

is reshaped and fed into the BiLSTM module to mine intrinsic temporal dependencies and capture long-range contextual information of industrial process data. On this basis, the SH-SA module is employed to weight important temporal features, strengthen the perception of weak fault information, and enhance the discriminative ability of deep features. 

Then, the FA module integrating global average, maximum and endpoint features is adopted to generate compact and discriminative global representations. Finally, a two-layer fully connected classifier is employed to output the classification results of 21 fault modes. 

#### _4.1.2. Hyperparameter settings_ 

The hyperparameters of the proposed Inception-SECA-BiLSTM model are selected based on empirical analysis and validation performance. The detailed parameter configurations of the model are illustrated in Table 3. 

For the feature extraction stage, three stacked Inception-SECA blocks are employed, with output channels set to 64, 128, and 128, respectively. This progressive increase in channel dimension allows the model to capture more complex feature representations while maintaining computational efficiency. Each Inception block adopts multi-scale convolution kernels (1, 3, and 5) to extract features at different receptive fields. 

In the SECA module, the hyperparameters γ and b are set to 2 and 1, respectively, following the configuration in the original ECA-Net. This setting enables adaptive determination of the convolution kernel size based on channel dimensions and has been demonstrated to achieve a good balance between performance and computational efficiency. 

For the temporal modeling stage, a two-layer BiLSTM is adopted with a hidden dimension of 128. This configuration is chosen to balance the model’s ability to capture long-range dependencies and the risk of overfitting. A dropout rate of 0.1 is applied in both the attention module and the classifier to improve generalization.For the SH-SA module, the query, key, and value projections share the same dimensionality as the BiLSTM hidden representation to ensure feature consistency and avoid additional projection overhead. The dropout rate is set to 0.1 to stabilize attention learning and prevent overfitting. 

For the FA module, no additional hyperparameters are introduced, as it adopts a parameter-free strategy that integrates global average pooling, max pooling, and the endpoint feature, thereby enhancing 

#### robustness and reducing model complexity. 

For the classifier, a two-layer fully connected structure is employed, where the hidden dimension is set to 64. This configuration is chosen to achieve a balance between representation capability and computational efficiency while avoiding overfitting in the final classification stage. In addition, batch normalization and residual connections are incorporated to stabilize training and accelerate convergence. All hyperparameters are determined through preliminary experiments, where different configurations were evaluated, and the selected settings achieved the best trade-off between performance and computational cost. 

All experiments are implemented based on the PyTorch deep learning framework. The hardware platform includes an Intel® Core™ i9–13980HX CPU and an NVIDIA GeForce RTX4060 GPU for accelerated computing. In the training phase, the batch size is set to 128, the Adam optimizer is adopted, and the cross-entropy loss is used as the loss function. The learning rate is adjusted by the warm-up and cosine annealing strategy, with an initial value of 1e-3 and a minimum value of 5e-6. The model is trained for a total of 120 epochs. 

In addition, a sensitivity analysis of key hyperparameters is conducted. Given the large number of hyperparameters, we only analyze the relatively critical ones in the model, namely γ in the SECA module and the initial learning rate. Fig. 10 and Fig. 11 illustrate the variation of classification accuracy with respect to γ and the initial learning rate, respectively. 

As illustrated in Fig. 10, when γ varies from 1 to 4, the classification accuracy of the model consistently stays at a high level between 98.01% and 98.55%, with a maximum performance fluctuation of merely 0.54%, and the peak accuracy of 98.55% is attained at γ= 2. These results confirm that the model is highly insensitive to the hyperparameter γ, maintaining stable performance even when the value deviates from the optimal setting. 

As presented in Fig. 11, across the initial learning rate range of 0.0001–0.005, the model's accuracy remains above 97.95% throughout, with a maximum fluctuation of only 0.6%, and the optimal performance of 98.55% is achieved at an initial learning rate of 0.001. This verifies that the model has low sensitivity to the initial learning rate, boasting excellent training stability and hyperparameter adaptability. 

Overall, the proposed model is insensitive to key hyperparameters and can deliver consistent and stable performance across various 

15 

> _C. Lv et al.                                                                                                                                                                                                                                       Process Safety and Environmental Protection 213 (2026) 108964_ 


![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0016-01.png)


**Fig. 21.** SECA channel attention weight distributions for representative fault classes for the coke furnace process. 

**Table 7** 

Precision and recall of the Inception-SECA-BiLSTM model and its ablation models for the coke furnace process. 

|Fault number|w/o I-SECA||w/o BiLSTM||w/o FA||w/o SH-SA||Proposed||
|---|---|---|---|---|---|---|---|---|---|---|
||P|R|P|R|P|R|P|R|P|R|
|1|90.95|95.50|84.28|96.50|82.88|92.00|84.55|93.00|**91.51**|**97.00**|
|2|98.00|98.00|98.48|97.50|**98.98**|97.00|98.47|96.50|98.00|**98.00**|
|3|100.00|99.50|100.00|100.00|100.00|99.50|100.00|99.50|**100.00**|**100.00**|
|4|96.46|95.50|96.00|96.00|93.60|95.00|94.61|96.50|**97.49**|**97.00**|
|5|95.34|**92.00**|95.38|82.50|92.18|82.50|94.44|85.00|**97.34**|91.50|
|6|99.50|99.50|99.00|99.00|99.00|99.50|98.51|99.00|**99.50**|**100.00**|
|Micro-avg|96.67|96.67|95.25|95.25|94.25|94.25|94.92|94.92|**97.25**|**97.25**|
|Macro-avg|96.71|96.67|95.52|95.25|94.44|94.25|95.10|94.92|**97.31**|**97.25**|



hyperparameter configurations. 

#### _4.1.3. Interpretability analysis_ 

To further enhance the interpretability of the proposed model, we analyze the channel attention weights learned by the SECA module for representative fault classes. Fig. 12 presents the average channel attention distributions for three typical faults: Fault 6, Fault 11 and Fault 18, respectively. As detailed in Table 1, these three faults are caused by 

fundamentally different fault modes, which provides a physical basis for their distinct attention patterns observed in the figure. 

As observed, different fault classes exhibit distinctly differentiated attention patterns across the 128 feature channels. Each fault type selectively activates a unique subset of channels with high attention weights, demonstrating that the model adaptively emphasizes the corresponding discriminative feature dimensions for different fault conditions. 

16 

> _C. Lv et al.                                                                                                                                                                                                                                       Process Safety and Environmental Protection 213 (2026) 108964_ 


![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0017-01.png)


**Fig. 22.** Confusion matrices of five models for the coke furnace process. 

17 

> _C. Lv et al.                                                                                                                                                                                                                                       Process Safety and Environmental Protection 213 (2026) 108964_ 

##### **Table 8** 

Accuracy, loss and kappa of four models for the coke furnace process. 

|Model|Accuracy(%)|Loss|Kappa value|
|---|---|---|---|
|DRSN-GRU|94.50|0.1605|0.9340|
|MA-BiTCN|95.33|0.1447|0.9440|
|SE-ResNet|96.00|0.1350|0.9520|
|Proposed|97.25|0.1245|0.9670|



For example, Fault 6 and Fault 18 both display clear multi-peak activation patterns, indicating that their respective fault characteristics are captured by multiple groups of highly discriminative feature channels rather than a single dominant channel. The peak locations of Fault 6 and Fault 18 differ noticeably, which reflects the unique feature structures corresponding to each fault type. In contrast, Fault 11 presents a relatively gentle and widely scattered distribution pattern, suggesting that its identification relies on a broader and more complex combination of feature channels. 

These results indicate that the SECA module effectively enhances discriminative feature channels in a fault-specific manner, rather than uniformly weighting all features. Therefore, the model is capable of learning meaningful feature selection mechanisms, which contributes to improved interpretability and reliable fault discrimination. 

#### _4.1.4. Ablation model comparison_ 

To verify the performance of the proposed model, four ablation models were set up to compare with the baseline model, InceptionSECA-BiLSTM, to assess the performance contributions of each component. Ablation Model 1: w/o I-SECA, which removes the Inception-SECA module from the baseline model to verify its feature extraction capability. Ablation Model 2: w/o BiLSTM, which removes the BiLSTM module from the baseline model to validate its contribution in modeling dynamic temporal dependencies and improving the accuracy of temporal fault feature recognition. Ablation Model 3: w/o FA, which removes the FA module from the baseline model to analyze the impact of the feature aggregation strategy on model performance. Ablation Model 4: w/o SH-SA, which removes the SH-SA module from the baseline model to verify the performance gain brought by the attention weighting mechanism. The parameter settings for the above four ablation models 

are consistent with those of the Inception-SECA-BiLSTM model. 

Table 4 presents the specific diagnostic results of the ablation models (w/o I-SECA, w/o BiLSTM, w/o FA, w/o SH-SA) and the model proposed in this paper. Observing the micro-average precision and micro-average recall, it is found that both metrics of the proposed model reach 98.55%, which are 4.67%, 6.82%, 4.51%, and 1.31% higher than the corresponding metrics of the other four ablation models, respectively. In terms of precision and recall, the proposed model exhibits obvious advantages, with the precision and recall of most categories close to unity. The w/o BiLSTM model achieves the lowest micro-average and macroaverage values, indicating that the BiLSTM module serves as the core component for capturing temporal dependencies in fault signals, and its absence leads to a significant performance degradation. The w/o FA and w/o I-SECA models exhibit comparable performance, which is slightly superior to that of the w/o BiLSTM model but still notably lower than that of the proposed model. This result demonstrates that the FA module and the Inception-SECA module play critical roles in enhancing feature selection and discriminative capability. The w/o SH-SA model ranks second only to the proposed model, yet a clear performance gap remains, verifying that the SH-SA module is essential for focusing on key discriminative features within the fault data. 

At the individual fault level, the proposed model not only achieves 100% precision and recall for easily identifiable faults (including faults 1, 6, and 7), but also yields substantial performance improvements over all other variants on difficult-to-classify faults (including faults 3, 9, 11, 15, and 19), effectively alleviating the bottleneck in complex fault identification. The results demonstrate that the proposed model exhibits more comprehensive performance in terms of precision and recall compared with the ablation models, further indicating that the aforementioned modules make vital contributions to the overall performance improvement of the model. 

Fig. 13 displays the F1 scores for difficult-to-classify faults (including faults 3, 9, 11, 15, and 19). It is evident that the Inception-SECA-BiLSTM model proposed in this paper outperforms the four ablation models across all fault categories. This directly verifies the synergistic effectiveness of each core module. Compared to the proposed model, the ablation models exhibit a significant decrease in F1 scores for these difficult-to-classify fault types. Notably, the performance drop is more pronounced for the w/o I-SECA and w/o BiLSTM variants. The 

**Table 9** 

Results of the four models under different noise levels in the coke furnace process. 

|Sigma<br>model|0.001|0.002|0.003|0.004|0.005|0.006|0.007|0.008|0.009|0.01|No noise|
|---|---|---|---|---|---|---|---|---|---|---|---|
|DRSN-GRU|94.33|94.25|94.08|94.00|93.75|93.56|93.42|93.36|93.17|92.78|94.50|
|MA-BiTCN|95.14|95.00|94.84|94.58|94.36|94.20|93.95|93.64|93.41|93.10|95.33|
|SE-ResNet|95.81|95.61|95.45|95.25|94.97|94.72|94.42|94.08|93.67|93.14|96.00|
|Proposed|97.08|96.78|96.53|96.17|95.75|95.58|95.33|94.89|94.75|94.44|97.25|




![](Inception-SECA-BiLSTM-_multi-scale_feature_extraction_framework_with_attention_enhancement_for_industrial_process_fault_diagnosis_images/conv_a216f93d43bae2d5.pdf-0018-15.png)


**Fig. 23.** Test accuracy of four models under various noise levels in the coke furnace process. 

18 

> _C. Lv et al.                                                                                                                                                                                                                                       Process Safety and Environmental Protection 213 (2026) 108964_ 

Inception-SECA and BiLSTM modules serve as the core contributors to performance improvement, while the FA and SH-SA modules provide auxiliary gains at the feature fusion and refined attention weighting levels, respectively. 

The t-distributed Stochastic Neighbor Embedding (t-SNE) (Laurens van der and Hinton, 2008), as an efficient dimensionality reduction visualization technology, can map the high-dimensional discriminant features learned by the model to the two-dimensional low dimensional space, and directly reflect the separability of features and the classification performance of the model through the clustering distribution of different categories of samples. To visually verify the feature expression ability of the proposed model, we visualized the model output logits of the test set samples by t-SNE, and the results are shown in Fig. 14. 

From the visualized results, it can be clearly observed that fault samples of the same category form compact and independent clusters, with clear boundaries and almost no significant overlap between different fault categories. This indicates that the features extracted by the model possess strong discriminative power among categories. Only a very small number of samples fall into adjacent category regions due to feature similarity, demonstrating an excellent overall classification performance, which aligns with the high F1 score and accuracy results mentioned earlier. 

To further quantify and compare the diagnostic performance of different models, we plotted the confusion matrices of the five models, as shown in Fig. 15. From the confusion matrices, it can be more intuitively observed that the Inception-SECA-BiLSTM model proposed in this paper significantly outperforms the other four ablation models in terms of overall fault diagnosis accuracy. Especially in the identification tasks of five typical difficult-to-classify faults: 3, 9, 11, 15, and 19, the classification accuracy of the model proposed in this paper is much higher than other models, further verifying its stronger robustness and diagnostic accuracy in complex fault scenarios. 

#### _4.1.5. Comparison of existing models_ 

In order to evaluate the effectiveness of the proposed model, we compare it with three deep learning models that perform well in the field of industrial process fault diagnosis. Comparison model 1: the DRSNGRU model proposed by Yin and Chen (2024) builds a DRSN channel to complete signal noise reduction and preliminary feature extraction. At the same time, it integrates the GRU channel of the convolution pool layer to capture the linear characteristics of time series. Combined with the multi label classification framework, it realizes accurate decoupling and identification of composite faults under complex working conditions. Comparison model 2: the MA-BiTCN model proposed by Cui et al. (2025) reduces the amount of calculation by screening diagnosis related features through SENet, extracts the bidirectional time dependence of vibration signals using BiTCN, and dynamically redistributes feature weights in combination with the multi head attention mechanism. Finally, the fault classification is completed through the full connection layer. Comparison model 3: the SE-ResNet model proposed by Lv et al. (2026) fused the residual branches and CNN branches to extract global and local fault features, and improved the diagnosis accuracy through the SE attention mechanism. The training parameter setting of the comparison model is consistent with the TE process, and the training iteration is 120 rounds. 

Fig. 16 and Fig. 17 present the training accuracy and loss curves of the four models during the training process. As observed from the figures, during the training phase, the training accuracy of all models increases gradually, while the training loss decreases as the number of epochs grows. However, the proposed model achieves the fastest convergence: its training accuracy rises rapidly in the early stage, outperforming the three comparison models, and stabilizes at nearly 98% after approximately 40 epochs. Meanwhile, the training loss of the proposed model drops to the lowest level among all models in the early stage, and the curve remains smooth and stable throughout the training process with no obvious fluctuations. These results demonstrate that the 

proposed model can effectively learn the feature patterns of the training data with high efficiency and stability. 

Fig. 18 and Fig. 19 respectively show the test accuracy and loss curves of the four models. From the test curves, it can be seen that the Inception-SECA-BiLSTM model proposed in this paper performs significantly better than DRSN-GRU, MA-BiTCN and SE-ResNet in terms of convergence speed, stability and final performance. Its test accuracy curve rises the fastest in the early stage and stabilizes at a high level above 98% in the later stage, which is consistently higher than that of the three comparison models. Notably, the test accuracy curve of the proposed model is the smoothest with almost no violent fluctuations, whereas DRSN-GRU exhibits obvious fluctuations in its accuracy curve during the middle and late testing stages, indicating poor stability. In terms of test loss, the proposed model achieves the lowest final loss value with the smoothest curve and smallest fluctuations, far outperforming the other models. 

Table 5 counts the accuracy, loss value and kappa value of the four models on the test set. The comparison results show that the proposed model is superior to other models in terms of core evaluation indicators. Compared with DRSN-GRU, MA-BiTCN and SE-ResNet, the accuracy increased by 2.55%, 5.49% and 4.02%, respectively. At the same time, the test loss was lower and the kappa value was higher, which reflected that the model proposed in this paper had stronger discrimination ability and more stable prediction consistency in the task of fault classification, and fully verified its superior diagnostic performance. 

#### _4.1.6. Robustness experiment_ 

For the purpose of testing the robustness of the model under disturbances and uncertainty, Gaussian white noise with different intensities (σ ranging from 0.001 to 0.01) was added to the test data to simulate sensor interference. The experimental results are presented in Table 6. To further intuitively compare the robustness of the four models, Fig. 20 illustrates the variation in classification accuracy of each model under different noise intensities. 

As shown in Fig. 20, the classification accuracy of all models exhibits a gradual downward trend with the increase of noise intensity. However, compared with the other three models, the proposed model demonstrates significantly superior anti-noise performance, with a much slower rate of accuracy degradation. 

Specifically, under noise-free conditions, the proposed model achieves an accuracy of 98.55%. As the noise intensity increases to low levels (σ=0.003 and σ=0.005), the accuracy of the proposed model only slightly decreases to 98.17% and 97.40%, with a degradation of merely 0.38% and 1.15% respectively from the noise-free baseline. In contrast, the accuracy of DRSN-GRU, MA-BiTCN and SE-ResNet drops to 93.98%, 92.38%, 93.60% at σ= 0.003, and further to 89.94%, 90.72%, 91.56% at σ= 0.005, showing a much steeper decline. Even when the noise intensity rises to a moderate level (σ=0.007), the proposed model still maintains an accuracy of 95.52%, with a total degradation of only 3.03% from the noise-free scenario, while the comparison models experience a more severe performance drop. When the noise intensity reaches the maximum tested level of σ= 0.01, the accuracy of the proposed model remains as high as 90.33%, with an overall degradation of 8.22% throughout the entire noise range, far outperforming the comparison models which suffer from substantial accuracy losses. 

The results fully demonstrate that the Inception-SECA-BiLSTM model exhibits good robustness and excellent adaptability to noise within a certain intensity range. 

#### _4.2. Industrial coke furnace_ 

#### _4.2.1. Hyperparameter settings_ 

The fault diagnosis experiment of coke furnace process and TE process share the same set of experimental parameters, only changing the input from 52 variables to 8 variables and the classified output from 21 to 6. All experiments are implemented based on the PyTorch deep 

19 

> _C. Lv et al.                                                                                                                                                                                                                                       Process Safety and Environmental Protection 213 (2026) 108964_ 

learning framework. The hardware platform includes an Intel® Core™ i9–13980HX CPU and an NVIDIA GeForce RTX4060 GPU for accelerated computing. In the training phase, the batch size is set to 64, the Adam optimizer is adopted, and the cross-entropy loss is used as the loss function. The learning rate is adjusted by the warm-up and cosine annealing strategy, with an initial value of 1e-3 and a minimum value of 1e-5. The model is trained for a total of 100 epochs. 

#### _4.2.2. Interpretability analysis_ 

To verify the interpretability of the SECA module in real-world coke furnace fault diagnosis scenarios, this paper extracts the channel attention weights from the final SECA layer of the model and visualizes the attention distributions for fault classes 2, 3, and 5, with detailed descriptions of the fault types provided in Table 2. As shown in Fig. 21, distinct fault classes correspond to differentiated channel attention weight distributions, where the model automatically assigns higher weights to critical feature channels. This confirms that the SECA module can effectively capture fault-relevant features on real industrial data, thereby enhancing both the classification performance and interpretability of the model. 

#### _4.2.3. Ablation model comparison_ 

Table 7 presents the specific diagnostic results of the ablation models w/o I-SECA, w/o BiLSTM, w/o FA, w/o SH-SA, and the model proposed in this paper. By observing the two indicators of micro-average precision and micro-average recall, it can be found that the precision and recall of the model proposed in this paper are both 97.25%, which are 0.58%, 2.00%, 3.00%, and 2.33% higher respectively compared to the ablation models. In terms of precision and recall for each fault category, the model proposed in this paper exhibits significant advantages, indicating that its precision and recall capabilities are more comprehensive compared to the ablation models. 

In order to intuitively compare the diagnostic performance of different models, we drew the confusion matrix of five models, as shown in Fig. 22. From the confusion matrix, it can be seen more intuitively that the Inception-SECA-BiLSTM model proposed in this paper is significantly better than the other four ablation models in the overall accuracy of fault diagnosis. In the category 5 fault classification, the accuracy of the proposed model is much higher than that of other models, which further verifies its stronger robustness and diagnostic accuracy in complex fault scenarios. 

#### _4.2.4. Comparison of existing models_ 

Table 8 counts the accuracy, loss value and kappa value of the four models on the test set. The comparison results show that the proposed model is superior to other models in terms of core evaluation indicators. Compared with DRSN-GRU, MA-BiTCN and SE-ResNet, the accuracy was improved by 2.75%, 1.92% and 1.25%, respectively. At the same time, the test loss was lower and the kappa value was higher, which fully verified its superior diagnostic performance. 

#### _4.2.5. Robustness experiment_ 

To verify the robustness of the model in the high-noise environment of the coke furnace, Gaussian noise with different intensities (σ ranging from 0.001 to 0.01) was introduced into the test data. The experimental results are presented in Table 9. To further intuitively compare the robustness of the four models, Fig. 23 illustrates the variation in classification accuracy of each model under different noise intensities. 

As the Gaussian noise intensity increases, the classification accuracy of all models gradually decreases, indicating that noise interference exerts a negative impact on feature representation and fault discrimination capability. The proposed method consistently achieves the highest accuracy at all noise levels. Compared with other models, it exhibits a slower performance degradation as noise intensifies. Notably, the proposed method still maintains favorable performance under highnoise conditions (σ ≥ 0.007). The results demonstrate that the Inception- 

SECA-BiLSTM model exhibits good robustness and excellent adaptability to noise within a certain intensity range. 

#### **5. Conclusion** 

This paper proposes a fault diagnosis model called Inception-SECABiLSTM. The model achieves comprehensive spatial extraction of fault features through multi-scale convolution branches of Inception, and combines the SECA module to enhance critical features and suppress noise, thereby effectively solving the problems of weak fault feature loss and redundant feature interference.The BiLSTM module is used to mine the inherent temporal dependencies and long-range contextual information of industrial temporal data, breaking through the limitations of single spatial feature modeling. On this basis, the SH-SA is introduced to weight and optimize temporal features, automatically focusing on highly discriminative key fault information and further improving the accuracy of feature representation. Finally, the FA module integrating average, maximum and endpoint features is adopted to achieve efficient fusion and purification of key fault information. 

The effectiveness of the proposed method is validated on both the TE process and a real-world industrial coke furnace dataset, which exhibit different characteristics with respect to process dynamics and data distribution. The consistent performance improvement across these datasets demonstrates the robustness and generalizability of the proposed framework. 

In the future, research will focus on optimizing model structures, incorporating transfer learning and system physical information to improve the real-time performance, small-sample adaptability, and interpretability of the model. 

#### **CRediT authorship contribution statement** 

**zhang ridong:** Supervision. **Furong Gao:** Resources. **Limin Wang:** Writing – review & editing. **Chaochao Lv:** Writing – original draft. 

#### **Declaration of Competing Interest** 

The authors declare that there are no conflicts of interest. 

#### **References** 

Adedigba, S.A., Khan, F., Yang, M., 2016. Process accident model considering dependency among contributory factors. Process Saf. Environ. Prot. 102, 633–647. Alauddin, M., Khan, F., Imtiaz, S., Ahmed, S., Amyotte, P., 2023. Integrating process dynamics in data-driven models of chemical processing systems. Process Saf. Environ. Prot. 174, 158–168. 

Amin, M.T., Imtiaz, S., Khan, F., 2018. Process system fault detection and diagnosis using a hybrid technique. Chem. Eng. Sci. 189, 191–211. Amin, M.T., Khan, F., Ahmed, S., Imtiaz, S., 2021a. A data-driven Bayesian network learning method for process fault diagnosis. Process Saf. Environ. Prot. 150, 110–122. Amin, M.T., Khan, F., Ahmed, S., Imtiaz, S., 2021b. Risk-based fault detection and diagnosis for nonlinear and non-Gaussian process systems using R-vine copula. Process Saf. Environ. Prot. 150, 123–136. 

Arunthavanathan, R., Khan, F., Ahmed, S., Imtiaz, S., 2021b. A deep learning model for process fault prognosis. Process Saf. Environ. Prot. 154, 467–479. Arunthavanathan, R., Khan, F., Ahmed, S., Imtiaz, Syed, 2021. An analysis of process fault diagnosis methods from safety perspectives. Comput. & Chem. Eng. 145, 107197. 

Bian, Z., Vong, C., Wong, P., Wang, S., 2022. Fuzzy KNN method with adaptive nearest neighbors. IEEE T. Cyber 52, 5380–5393. Chen, C., Shen, L., Liu, W., Luo, Z., 2023b. Efficient-Adam: communication-efficient distributed adam. IEEE Trans. Signal Process 71, 3257–3266. Chen, S., Yang, R., Zhong, M., Xi, X., Liu, C., C, 2023a. A random forest and model-based hybrid method of fault diagnosis for satellite attitude control systems. IEEE Trans. Instrum. Meas. 72, 1–13. 

Chen, Y., Zhang, R., 2026. Multiscale convolutional neural network with self-attention mechanism and soft thresholding for industrial process fault diagnosis. IEEE Trans. Syst. Man Cyber Syst. 56, 2647–2659. 

Chen, C., Zhang, R., Gao, F., 2026. Deep parallel feature fusion network with temporal convolutional network and bidirectional gated recurrent unit for industrial process modeling and fault diagnosis. Process Saf. Environ. Prot. 209, 108590. 

20 

Cui, J., Gao, J., Xing, R., Wu, W., Li, M., Yang, Y., 2025. Fault diagnosis method for rolling bearing based on attention mechanism and BiTCN model. Digit. Signal Process. 167, 105454. 

- Deng, F., Guo, S., Zhou, R., Chen, J., 2017. Sensor multifault diagnosis with improved support vector machines. IEEE Trans. Autom. Sci. Eng. 14, 1053–1063. 

- Don, M.G., Khan, F., 2019. Dynamic process fault detection and diagnosis based on a combined approach of hidden Markov and Bayesian network model. Chem. Eng. Sci. 201, 82–96. 

- Eckle, K., Schmidt-Hieber, J., 2019. A comparison of deep networks with ReLU activation function and linear spline-type methods. Neural Netw. 110, 232–242. 

- Ghosh, A., Ahmed, S., Khan, F., Rusli, R., 2020. Process safety assessment considering multivariate non-linear dependence among process variables. Process Saf. Environ. Prot. 135, 70–80. 

- Guo, X., Khan, J., Ji, F., Ding, L., Yang, Y., 2021. Fuzzy bayesian network based on an improved similarity aggregation method for risk assessment of storage tank accident. Process Saf. Environ. Prot. 149, 817–830. 

- Hassanin, M., Anwar, S., Radwan, I., Khan, F.S., Mian, A., 2024. Visual attention methods in deep learning: An in-depth survey. Inf. Fusion 108, 102417. 

- He, J., Li, C., Mo, L., Yan, R., 2025. WCNN-KAN: a novel interpretable multiscale 

   - attention feature fusion network for rotating machinery fault diagnosis. IEEE Trans. Instrum. Meas. 74, 1–14. 

- Hu, C., Bai, J., Zou, H., 2026. Two-dimensional iterative learning control under infinite horizon optimization for batch processes with partial actuator failures. Can. J. Chem. Eng. 1–20. 

- Laurens van der, M., Hinton, G., 2008. Visualizing data using t-SNE. J. Mach. Learn. Res. 9, 2579–2605. 

- Liu, X., Chen, S., Zhang, K., Jiang, J., Jiang, J., 2025. A hybrid BiLSTM and improved HBA algorithm for fault diagnosis of chemical processes. Process Saf. Environ. Prot. 201, 107578. 

- Lv, W., Xu, S., Zhu, T., Chen, L., Wu, S., Xie, H., Ma, G., 2026. Real-time diagnosis of stator winding faults in PMSM based on residual CNN with channel attention mechanism. IEEE Trans. Instrum. Meas. 75, 1–13. 

- Muhammad, A., Shamshad, F., Bae, S., 2023. Adversarial attacks and batch normalization: a batch statistics perspective. IEEE Access 11, 96449–96459. 

- Pasman, H., Sripaul, E., Khan, F., Fabiano, B., 2023. Energy transition technology comes with new process safety challenges and risks. Process Saf. Environ. Prot. 177, 765–794. 

- Pu, X., Li, C., 2021. Online semisupervised broad learning system for industrial fault diagnosis. IEEE Trans. Ind. Inf. 17, 6644–6654. 

- Song, Q., Jiang, P., 2022. A multi-scale convolutional neural network based fault diagnosis model for complex chemical processes. Process Saf. Environ. Prot. 159, 575–584. 

- Sun, K., Huang, Z., Mao, H., Qin, A., Li, X., Tang, W., Xiong, J., 2022. Multi-scale clustergraph convolution network with multi-channel residual network for intelligent fault diagnosis. IEEE Trans. Instrum. Meas. 71, 1–12. 

- Tang, H., Jing, W., Tang, D., Yang, Z., Yang, X., Xie, W., 2025. Global–local attentionaware zero-shot learning for industrial fault diagnosis. IEEE Trans. Instrum. Meas. 74, 1–16. 

- Wang, Q., Wu, B., Zhu, P., Li, P., Zuo, W., Hu, Q., 2020. ECA-net: efficient channel attention for deep convolutional neural networks. Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR) 11534–11542. 

_Process Safety and Environmental Protection 213 (2026) 108964_ 

- Wang, Z., Zhang, Q., Xiong, J., Xiao, M., Sun, G., He, J., 2017. Fault diagnosis of a rolling bearing using wavelet packet denoising and random forests. IEEE Sens. J. 17, 5581–5588. 

- Wu, H., Bai, J., Zou, H., 2026. Fast predictive functional control based on auxiliary variable optimization. Can. J. Chem. Eng. https://doi.org/10.1002/cjce.70455. 

- Wu, C., Gao, F., Zhang, R., 2026a. An out-of-distribution fault detection framework using deep global feature modeling and extended logit fusion for Industrial Processes. Process Saf. Environ. Prot. 211, 108778. 

- Wu, J., Ruan, D., Qian, Y., 2026b. An improved physics-guided interpretable inception network and its application in bearing fault diagnosis. IEEE Trans. Instrum. Meas. 75, 1–14. 

- Xiao, B., Li, Y., Sun, B., Yang, C., Huang, K., Zhu, H., 2021. Decentralized PCA modeling based on relevance and redundancy variable selection and its application to largescale dynamic process monitoring. Process Saf. Environ. Prot. 151, 85–100. 

- Xiao, Y., Shi, H., Song, B., Tao, Y., Tan, S., Wang, B., 2024. Temporal attention sourcefree adaptation for chemical processes fault diagnosis. IEEE Trans. Ind. Inf. 20, 4773–4783. 

- Yang, J., Liu, J., Xie, J., Wang, C., Ding, T., 2021b. Conditional GAN and 2-D CNN for bearing fault diagnosis with small samples. IEEE Trans. Instrum. Meas. 70, 1–12. 

Yang, G., Zhao, Y., Gu, X., 2021a. A novel Bayesian framework with enhanced principal component analysis for chemical fault diagnosis. IEEE Trans. Instrum. Meas. 70, 1–9. 

- Yin, S., Chen, Z., 2024. Research on compound fault diagnosis of bearings using an improved DRSN-GRU dual-channel model. IEEE Sens. J. 24, 35304–35311. 

- Yu, K., Wang, P., Gu, Y., 2024. Toward efficient and interpretative rolling bearing fault diagnosis via quadratic neural network with Bi-LSTM. IEEE Internet Things J. 11, 23002–23019. 

- Yu, W., Zhao, C., 2019. Online fault diagnosis in industrial processes using multimodel exponential discriminant analysis algorithm. IEEE Trans. Control Syst. Technol. 27, 1317–1325. 

- Yuan, P., Bai, J., Zou, H., 2026. Two-dimensional iterative learning robust H∞ optimization and linear quadratic fault-tolerant control design for uncertain batch processes. Can. J. Chem. Eng. 1–19. 

- Yuan, X., Xu, W., Wang, Y., Yang, C., Gui, W., 2024. A deep residual PLS for data-driven quality prediction modeling in industrial process. IEEE/CAA J. Autom. Sin. 11, 1777–1785. 

- Zarei, E., Khan, F., Abbassi, R., 2023. How to account artificial intelligence in human factor analysis of complex systems? Process Saf. Environ. Prot. 171, 736–750. 

Zeng, L., Jin, Q., Lin, Z., Zheng, C., Wu, Y., Wu, X., Gao, 2024. Dual-attention LSTM autoencoder for fault detection in industrial complex dynamic processes. Process Saf. Environ. Prot. 185, 1145–1159. 

- Zhang, R., Gao, F., 2026. Two-dimensional PFC with novel iterative error compensation and multi basis functions for batch processes under partial actuator failure. J. Process Control 161, 103684. 

- Zhang, R., Li, Z., Gao, F., 2025. Modeling and diagnosis of industrial system using hybrid deep residual shrinkage network and XGBoost. Process Saf. Environ. Prot. 200, 107438.. 

- Zhang, J., Zhang, M., Feng, Z., Lv, R., Lu, C., Dai, Y., Dong, L., 2023. Gated recurrent unit-enhanced deep convolutional neural network for real-time industrial process fault diagnosis. Process Saf. Environ. Prot. 175, 129–149. 

- Zhao, M., Zhong, S., Fu, X., Tang, B., Pecht, M., 2020. Deep residual shrinkage networks for fault diagnosis. IEEE Trans. Ind. Inf. 16, 4681–4690. 

Zhu, Y., Zhang, R., 2026. New attention ensemble-based fault diagnosis for industrial processes under imbalanced finite data. IEEE Trans. Instrum. Meas. 75, 3501608. 

21 

