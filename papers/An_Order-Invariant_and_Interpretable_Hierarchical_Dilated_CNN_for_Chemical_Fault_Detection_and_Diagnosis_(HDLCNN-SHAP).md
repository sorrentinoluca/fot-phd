1 

# An Order-Invariant and Interpretable Hierarchical Dilated Convolution Neural Network for Chemical Fault Detection and Diagnosis 

Mengxuan Li, Peng Peng, _Member, IEEE,_ Min Wang, _Member, IEEE,_ Hongwei Wang 

**_Abstract_ —Fault detection and diagnosis is significant for reducing maintenance costs and improving health and safety in chemical processes. Convolution neural network (CNN) is a popular deep learning algorithm with many successful applications in chemical fault detection and diagnosis tasks. However, convolution layers in CNN are very sensitive to the order of features, which can lead to instability in the processing of tabular data. Optimal order of features result in better performance of CNN models but it is expensive to seek such optimal order. In addition, because of the encapsulation mechanism of feature extraction, most CNN models are opaque and have poor interpretability, thus failing to identify root-cause features without human supervision. These difficulties inevitably limit the performance and credibility of CNN methods. In this paper, we propose an order-invariant and interpretable hierarchical dilated convolution neural network (HDLCNN), which is composed by feature clustering, dilated convolution and the shapley additive explanations (SHAP) method. The novelty of HDLCNN lies in its capability of processing tabular data with features of arbitrary order without seeking the optimal order, due to the ability to agglomerate correlated features of feature clustering and the large receptive field of dilated convolution. Then, the proposed method provides interpretability by including the SHAP values to quantify feature contribution. Therefore, the root-cause features can be identified as the features with the highest contribution. Computational experiments are conducted on the Tennessee Eastman chemical process benchmark dataset. Compared with the other methods, the proposed HDLCNN-SHAP method achieves better performance on processing tabular data with features of arbitrary order, detecting faults, and identifying the root-cause features.** 

**_Note to Practitioners_ —This paper was motivated by the problem of fault detection and diagnosis to process multiple variables and identify the root-cause features in real chemical processes. In this case, the order of features affects the fault detection performance and the precise root-cause feature is required to be identify to avoid the same faults. This paper presents a novel order-invariant and interpretable framework for fault detection and root cause analysis in real chemical processes to process data with features of arbitrary order, thus reducing the burden** 

*This work was supported by the National Key R&D Program of China under Grant 2020YFB1707803.(Corresponding author: Peng Peng and Hongwei Wang.) 

Mengxuan Li is with the College of Computer Science and Technology in Zhejiang University, Hangzhou, 310013, China. (E-mail: mengxuanli@intl.zju.edu.cn). 

Peng Peng and Hongwei Wang are with Zhejiang University and the University of Illinois Urbana–Champaign Institute, Haining, 314400, China. (E-mail: pengpeng@intl.zju.edu.cn, hongweiwang@intl.zju.edu.cn). 

Min Wang is with the School of Automation Engineering, University of Electronic Science and Technology of China, Chengdu 611731, China, (email: mwang@uestc.edu.cn). 

This work has been submitted to the IEEE Transactions on Automation Science and Engineering for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible. 

**on users. It utilizes the collected historical data for training and requires no human supervision. The newly collected data is automatically classified into a normal or fault type. Once a fault happens, the corresponding root-cause feature is identified without any prior knowledge. In our future work, we plan to focus on the faults with multiple root-cause features. In addition, the incomplete dataset and simultaneous-fault diagnosis are worth of investigation.** 

**_Index Terms_ —Fault Diagnosis, Deep Learning, Dilated Convolution Neural Network, Interpretability** 

## I. INTRODUCTION 

**W** ITHbecome more intelligent and automatic. This trend hasthe advent of Industry 4.0, chemical processes raised the urgent need of detecting anomalies and diagnosing faults efficiently and correctly. Chemical faults result in chemical contamination, potential explosion, and other seriously chemical hazards, and thus intelligent fault diagnosis methods are required to find the underlying causes of the faults. Current fault detection and diagnosis methods can be classified into two categories: model-based and data-based. Model-based methods are less accurate with higher level of complexity as they depend on the modeling of complex physical and chemical processes. Therefore, data-based methods have become increasingly popular recently. Among these methods, deep learning methods have been used widely and achieved electrifying performance in fault detection and diagnosis problems [1]. 

In particular, convolution neural network (CNN) is one of the most representative deep learning architectures based on convolution calculations. The main advantage of CNN is that it automatically detects the important features without any human supervision. And it can easily process high-dimensional data by sharing convolution kernels. Currently, some work has been done to show the potential of utilizing CNN to detect fault in chemical processes. For example, Wang _et al._ proposed a feature fusion fault diagnosis method using a normalized CNN for complex chemical processes [2]. Huang _et al._ introduced a novel fault diagnosis method that consists of sliding window processing and a CNN model [3]. However, applying the current CNN models in real chemical processes is still challenging. On the one hand, CNN models rely on convolution operation to extract information within each sizefixed convolution kernel, leading to result that only the information among adjacent features can be extracted. Different from images, the data of chemical processes involves multiple 

2 

variables through the time domain, which is considered as tabular data. Thus the order of these variables determine the extracted information through kernels, resulting in instability of processing tabular data by convolution layers. On the other hand, the existing CNN methods only provide classification results while the analysis of the root-cause features is lacking. Because of the encapsulation mechanism of feature extraction, most CNN models are opaque without any knowledge of the internal working principles, thus users have no information on feature contribution to the prediction. Without analyzing the underlying root-cause features, the same faults will repeat and result in serious consequences. 

In this paper, we propose an order-invariant and interpretable hierarchical dilated convolution neural network (HDLCNN) composed by feature clustering, dilated convolution and shapley additive explanations (SHAP) method to process tabular data with features of arbitrary order and obtain credible root-cause features. Dilated convolution, a variant of CNN that expands the kernel by inserting holes between the kernel elements, is utilized in our method [4]. It is adopted to increase the receptive field size without increasing the number of model parameters. Since receptive field is the corresponding region in the input that determines a unit in a certain layer in the network, dilated convolution with larger receptive field has the capability of extracting global features thus weakening the impact of the order of features. To further eliminate the effects of the order, we utilize feature clustering method to agglomerate highly correlated features before convolution layers. Hierarchical clustering method is applied since it builds a hierarchy of clusters and is not affected by the input order of data. In addition, a major difficulty to apply CNN methods in real chemical processes is to get credible fault detection results and obtain exact root-cause features. This means that interpretability, the degree to which a human can understand the model’s result, is vital for human to trust the decisions made by complex models. To solve this problem, we apply the SHAP method to interpret the complex black box model, which is a method to explain individual predictions based on the game theoretically optimal Shapley values [5]. Compared with other interpretability methods, it has the advantages of solid theoretical foundation in game theory and intuitive visualization based on the origin data. Also, it is model-agnostic while providing both local and global interpretability. Therefore, we utilize the SHAP method to provide interpretability by computing the SHAP values to quantify feature contribution and then obtaining the root-cause features. 

The main contributions of this article are as follows: 

- A dilated convolution based order-invariant classifier, namely HDLCNN, is developed to solve chemical fault detection and diagnosis. Dilated convolution is a variant of CNN with larger receptive field, enabling the proposed method to extract more information within a size-fixed convolution kernel thus achieving better performance on processing tabular data with features of arbitrary order. 

- Hierarchical clustering algorithm is applied to agglomerate highly correlated features before the convolution layers to further weaken the effect of the order of 

   - features. As a data pre-processing method, hierarchical clustering treats each input as a separate cluster and then sequentially merges similar clusters thus being unaffected on the order. 

- SHAP method is applied to provide credible and visual interpretability of the classification results from HDLCNN. The computed SHAP values quantify feature contribution and are utilized to obtain the root-cause features. 

- The experimental results on the Tennessee Eastman (TE) chemical process benchmark dataset demonstrate that, in contrast to the existing methods, the proposed HDLCNNSHAP method achieves better performance in the key operations of processing tabular data with features of arbitrary order, detecting faults, and identifying the rootcause features. 

The rest of this paper is organized as follows. The related work is introduced and the motivation of this work is described in Section II. The proposed order-invariant and interpretable chemical fault detection and diagnosis method is shown in Section III. The experiments of our proposed method based on the TE dataset are introduced in Section IV. And Section V summarizes this paper. 

## II. BACKGROUND THEORY AND MOTIVATION 

## _A. Related Work_ 

Till now, researchers has shown the effectiveness of applying CNN for chemical fault detection and diagnosis. For example, Chadha _et al._ proposed a 1-D CNN model to extract meaningful features from the time series sequence [6]. Wang _et al._ proposed a fault diagnosis method using deep learning multi-model fusion based on CNN and long short-term memory (LSTM) [7]. Gu _et al._ proposed an incremental CNN model to detect faults in a real chemical industrial process [8]. He _et al._ proposed a multi-block temporal convolutional network to learn the temporal-correlated features [9]. However, these methods mainly focus on extracting temporal features and ignore the effect of the order of features. Zhong _et al._ discussed the impact of the arrangement order of features on fault diagnosis and used enumeration method to find the optimal order [10]. However, it is time consuming to find the optimal order and the problem will be exacerbated since chemical processes involve multiple variables. Therefore, it is necessary to design an effective network that is less affected by the order of features. In this paper, we propose an orderinvariant fault detection method based on hierarchical clustering and dilated convolution. The proposed HDLCNN methods can process chemical tabular data with arbitrary feature order and provide accurate fault classification results. 

Another limitation of the current CNN methods is that only the classification results are provided without an explanation of the results. Considered as black box systems, the CNN models produces useful fault classification results without revealing any information about its internal workings. To avoid the black box problem, interpretability methods have aroused interests of researchers, which aim to help humans readily understand the reasoning behind predictions made by the complex models. Interpretability methods can be divided into two categories: antehoc interpretability and post-hoc interpretability. The former 

3 


![](An_Order-Invariant_and_Interpretable_Hierarchical_Dilated_CNN_for_Chemical_Fault_Detection_and_Diagnosis_(HDLCNN-SHAP)_images/conv_5127dbdcb3adbda6.pdf-0003-01.png)


Figure 1. The tabular data with _n_ features and _m_ time duration. Highly correlated features are closer in the optimal order. 

one refers to design interpretable models to directly visualize and interpret the internal information while the latter one refers to apply interpretation methods after model training. Generally, researchers prefer to use ante-hoc interpretable bayesian network (BN) to recognize the root-cause features in chemical processes. BN is a probabilistic graphical model based on random variables and the corresponding conditional probability. It can be used to identify the propagation probability among measurable variables to determine the root-cause features. Liu _et al._ proposed a strong relevant mechanism bayesian network by combining mechanism correlation analysis and process state transition to identify the unmonitored root-cause features [11]. Liu _et al._ proposed a multi-state BN to recognize a node into multiple states [12]. However, it is expensive to design a BN model since it requires prior knowledge and expert rules. And no universally acknowledged method is developed for constructing networks from raw data. On the contrary, CNN models provide accurate classification results without human supervision. Therefore, utilizing suitable post-hoc inpretability methods to explain the internal parameters of CNN models is a possible solution to visualize the feature contribution and thus identify the root-cause features. In this paper, we propose an interpretable fault diagnosis method based on the SHAP method. The root-cause features are obtained with SHAP values thus greatly improving the practicability of fault diagnosis methods in real chemical processes. 

Figure 2. The correlation coefficients of the 22 features in the TE dataset. 

rows determine the information extracted within a kernel. The left part shows the raw data with original order of features, and the right part shows the optimal order by changing the order of features to make highly correlated features closer. We seek the optimal order since it results in the best performance of CNN model. To further explain this problem, we conduct some experiments on the TE dataset to analyze the correlation of these features. The TE dataset contains 22 continuous process features and the corresponding correlation coefficients are shown in Fig. 2. From Fig. 2, we can see that there are 14 pairs of features have correlation coefficients greater than 0.7. Therefore, utilizing convolution kernels to extract features of the original order will loss the information related to the correlation of features, since the close-related variables are not considered effectively. Zhong _et al._ proved the impact of the order led on model performance and devoted much efforts to find the optimal order [10]. However, using enumeration method to select the optimal order is inefficient. An alternative solution is to design a model which is less affected by the order of features and can process arbitrary order effectively. In this paper, we propose an order-invariant HDLCNN model based on feature clustering and dilated convolution to extract features with arbitrary order. Dilated convolution is utilized to extract information involving more variables due to its larger receptive field. In addition, as a data pre-processing method, feature clustering is used to further agglomerate correlated features before training the dilated convolution model. More details are described in Section III. This design enables the proposed model to effectively process the tabular data with features of arbitrary order thus no longer necessary to seek the optimal order. 

## _B. Motivation of This Work_ 

Fault detection and diagnosis technologies are vital in real chemical processes since they aim to discover the faults in the early stage and thus reduce maintenance costs. For this task, the current CNN methods only focus on extracting temporal features in multi-variables chemical processes. However, chemical processes have tabular data involving both time and feature domains. Similar to the effect of the pixel positions in images, the order of features in tabular data also affect the classification results, since it determines the information extracted within a size-fixed convolution kernel. Although deep CNN models can achieve global receptive field and extract order-invariant information ultimately, they are computational expensive and inefficient for chemical data. Therefore, we aim to design a shallow and order-invariant CNN model. Fig. 1 shows an example of tabular data with _n_ features and _m_ time duration. Each row represents a feature and the order of these 

On the other hand, chemical processes have a very high risk of serious incident consequences by handling and processing materials under hazardous conditions. Therefore, once a fault is detected, it is necessary to analyze the corresponding root causes to identify the underlying issues and avoid the same faults. Generally, researchers design ante-hoc interpretable BN models to identify root-cause features. But these methods require prior knowledge and expert rules leading to much manual intervention for real applications. On the contrary, 

4 

post-hoc interpretability methods analyze the complex models after training and require no prior knowledge, thus can be combined with opaque CNN models to leverage their strengths of automatically extracting the important features. In particular, specific post-hoc interpretability methods are proposed to explain the CNN-based models and make them more transparent. Zhou _et al._ utilized global average pooling layers in CNN models to generate class activation maps (CAM), which indicates the discriminative regions used by the CNNs for prediction [13]. Further, Selvaraju _et al._ extends the CAM method to any CNN-based differentiable architecture by using the gradients of targets and flowing into the final convolution layer, namely gradient-weighted CAM (Grad-CAM) [14]. However, these CAM-based methods only produce a coarse localization map highlighting the important regions [14] while fault diagnosis requires to provide pixellevel explanation and precisely locate the correct root-cause feature. Therefore, these model-specific interpretability methods are not satisfying. In contrast, model-agnostic methods are more flexible and independent of the underlying machine learning model. For example, partial dependence plot (PDP) [15] and individual conditional expectation plot (ICEP) [16] are designed to display the effect of a feature on the prediction. However, they assume the independence of each feature and fail to process multiple features simultaneously, thus they are inappropriate for chemical processes. Besides, Ribeiro _et al._ proposed a technique that explains individual predictions by training local surrogate models to approximate the predictions of the underlying black box model, namely local interpretable model-agnostic explanations (LIME) [17]. But it also ignores the correlation between features and only provide local explanations. In contrast, SHAP provides both local and global explanations by computing the contribution of each feature to the corresponding prediction [5]. Also, it considers the interaction effect after obtaining the individual feature effects. Therefore, we apply SHAP method to improve the interpreability of our CNN-based model. The visualization of feature contribution and analysis of root-cause features based on SHAP values are shown in Section IV. 

## _C. Dilated Convolution_ 

CNN is a representative deep learning model which has been widely used in different fields. It takes the raw data, trains the model, then extracts the features automatically for better classification. Although increasing depth of CNN models can achieve larger receptive field size and higher performance, the number of parameters will greatly increase. With the consideration of it, dilated convolution is proposed. The key idea of dilated CNN (DLCNN) is to maintain the high resolution of feature maps and enlarge the receptive field size in CNN [4]. It expands the kernel by inserting holes among original elements thus enlarging the receptive field. Comparing with traditional CNN, it involves a hyper-parameter named dilation rate which indicates a spacing between the non-zero values in a kernel. Fig. 3 shows the comparison of CNN and DLCNN. Theoretically, CNN can be seen as a DLCNN with 


![](An_Order-Invariant_and_Interpretable_Hierarchical_Dilated_CNN_for_Chemical_Fault_Detection_and_Diagnosis_(HDLCNN-SHAP)_images/conv_5127dbdcb3adbda6.pdf-0004-04.png)



![](An_Order-Invariant_and_Interpretable_Hierarchical_Dilated_CNN_for_Chemical_Fault_Detection_and_Diagnosis_(HDLCNN-SHAP)_images/conv_5127dbdcb3adbda6.pdf-0004-05.png)



![](An_Order-Invariant_and_Interpretable_Hierarchical_Dilated_CNN_for_Chemical_Fault_Detection_and_Diagnosis_(HDLCNN-SHAP)_images/conv_5127dbdcb3adbda6.pdf-0004-06.png)


Figure 3. The comparison of CNN and DLCNN. 

dilation rate _r_ = 1 and the normal convolution calculation is as follows: 


![](An_Order-Invariant_and_Interpretable_Hierarchical_Dilated_CNN_for_Chemical_Fault_Detection_and_Diagnosis_(HDLCNN-SHAP)_images/conv_5127dbdcb3adbda6.pdf-0004-09.png)


where _Y_ , _H_ and _X_ are the 2-D output, filter and input respectively. A sample of DLCNN is introduced in Fig. 3 (b). With a dilation rate _r_ , ( _r−_ 1) data points will be skipped in the process of convolution. The dilated convolution calculation is as follows: 


![](An_Order-Invariant_and_Interpretable_Hierarchical_Dilated_CNN_for_Chemical_Fault_Detection_and_Diagnosis_(HDLCNN-SHAP)_images/conv_5127dbdcb3adbda6.pdf-0004-11.png)


With a dilation rate _r_ , this method offers a larger receptive field at the same computational cost. While the number of weights in the kernel is unchanged, they are no longer applied to spatially adjacent samples. Define _cl_ as the receptive field size of the feature map _yl_ at the layer _l_ in a DLCNN. Then, the receptive field size of layer _l_ can be computed as follows: 


![](An_Order-Invariant_and_Interpretable_Hierarchical_Dilated_CNN_for_Chemical_Fault_Detection_and_Diagnosis_(HDLCNN-SHAP)_images/conv_5127dbdcb3adbda6.pdf-0004-13.png)


where _sl_ refers to the stride and _hl_ indicates the kernel size. It is obvious that the receptive field increases linearly as the dilation rate increases. This enables models to have a larger receptive field with the same number of parameters and computation costs. 

## _D. SHAP Method_ 

In this paper, we utilize the SHAP method [5] to provide interpretability and obtain the root-cause features, which is based on shapley values [18] and game theory [19]. It computes the shapley values for each feature of the data samples and these values indicate the contribution that the feature generates in the prediction. More specifically, a shapley value is the average marginal contribution of a feature among all possible coalitions [18]. Consider a simple linear model: 


![](An_Order-Invariant_and_Interpretable_Hierarchical_Dilated_CNN_for_Chemical_Fault_Detection_and_Diagnosis_(HDLCNN-SHAP)_images/conv_5127dbdcb3adbda6.pdf-0004-17.png)


where _x_ is a data sample with _p_ features and each _xi_ is a feature value. _βi_ is the weight of the feature _i_ . The contribution 

5 


![](An_Order-Invariant_and_Interpretable_Hierarchical_Dilated_CNN_for_Chemical_Fault_Detection_and_Diagnosis_(HDLCNN-SHAP)_images/conv_5127dbdcb3adbda6.pdf-0005-01.png)


Figure 4. The overall architecture of the proposed order-invariant and interpretable HDLCNN-SHAP method for chemical fault detection and diagnosis. 

_φi_ of the feature _i_ on the prediction _f_<sup>ˆ</sup> ( _x_ ) can be computed as follows: 


![](An_Order-Invariant_and_Interpretable_Hierarchical_Dilated_CNN_for_Chemical_Fault_Detection_and_Diagnosis_(HDLCNN-SHAP)_images/conv_5127dbdcb3adbda6.pdf-0005-04.png)


where _E_ ( _βiXi_ ) is the mean effect estimate for the feature _i_ . Then, the contribution is the difference between the feature effect and the average effect. 

On this basis, SHAP defines an explanation model _g_ based on the additivity property of shapley values as follows: 


![](An_Order-Invariant_and_Interpretable_Hierarchical_Dilated_CNN_for_Chemical_Fault_Detection_and_Diagnosis_(HDLCNN-SHAP)_images/conv_5127dbdcb3adbda6.pdf-0005-07.png)


where _z_<sup>_′_</sup> _∈{_ 0 _,_ 1 _}_<sup>_M_</sup> is a one-hot vector of features, _M_ is the number of input features and _φi_ is the contribution of the feature _i_ . Assuming a model inputs a dataset _P_ and outputs a prediction _Y_ ( _S_ ), the shapley value _φi_ is computed as follows: 


![](An_Order-Invariant_and_Interpretable_Hierarchical_Dilated_CNN_for_Chemical_Fault_Detection_and_Diagnosis_(HDLCNN-SHAP)_images/conv_5127dbdcb3adbda6.pdf-0005-09.png)



![](An_Order-Invariant_and_Interpretable_Hierarchical_Dilated_CNN_for_Chemical_Fault_Detection_and_Diagnosis_(HDLCNN-SHAP)_images/conv_5127dbdcb3adbda6.pdf-0005-10.png)


where _S_ is a subset of the features and _F_ is the set of all features [5]. 

## III. METHODOLOGY 

In this paper, we propose an order-invariant and interpretable fault diagnosis method, namely HDLCNN-SHAP, based on feature clustering, dilated convolution and the SHAP method for chemical fault detection and diagnosis. The proposed method mainly contains two parts: a hierarchical dilated convolution model and an explainer based on the SHAP method. The input data is first pre-processed by the feature clustering method and then fed into the hierarchical dilated convolution model to provide classification results. Then the trained model is seen as a black box and we apply the SHAP method to interpret the model performance. The overall architecture is shown in Fig. 4. In the following subsections, we will introduce the main of our method in detail. 

## _A. Data Pre-processing_ 

As shown in Fig. 2, different features may be strongly correlated which requires the ability of extracting the hidden information of the relevance among these features. In this case, a convolution layer is difficult to extract enough information within size-fixed kernels. Instead of seeking the optimal order, we cluster the correlated features before training the dilated convolution model. As a data pre-processing step, we apply hierarchical clustering to divide the features into two categories based on relevance. Compared with other clustering methods, hierarchical clustering is easy to understand and implement. More importantly, the clustering results are not affected by the input order of data. Assume that we have a set of training samples: **_X_** = _{_ **_x_ 1** _,_ **_x_ 2** _,_ **_x_ 3** _, . . . ,_ **_xn_** _}_ , where **_xi_** _∈_ **_R_**<sup>**_p_**</sup> . Based on it, we build a set of the **_p_** features: **_F_** = _{_ **_f_ 1** _,_ **_f_ 2** _,_ **_f_ 3** _, . . . ,_ **_fp_** _}_ , where **_fi_** _∈_ **_R_**<sup>**_n_**</sup> . Then we divide these **_p_** features into two categorizes based on the hierarchical clustering algorithm. It mainly contains the following three steps: 

- 1) Each feature **_fi_** is treated as a single cluster. Then we compute the euclidean distance _d_ ( **_fi_** _,_ **_fj_** ) between two clusters **_fi_** and **_fj_** . 

- 2) The two closest clusters **_fi_** _,_ **_fj_** are merged into a single cluster **_fs_** . Then **_fi_** _,_ **_fj_** are removed and **_fs_** is added. 

- 3) Iterate the previous step until there is only one cluster remaining. 

At each iteration, the distance matrix is updated to reflect the distance of the newly formed cluster **_fs_** with the remaining clusters. We use the Ward variance minimization algorithm to calculate the distance mentioned above. The distance between the newly formed cluster **_fs_** and any remaining cluster **_ft_** is as: 


![](An_Order-Invariant_and_Interpretable_Hierarchical_Dilated_CNN_for_Chemical_Fault_Detection_and_Diagnosis_(HDLCNN-SHAP)_images/conv_5127dbdcb3adbda6.pdf-0005-20.png)



![](An_Order-Invariant_and_Interpretable_Hierarchical_Dilated_CNN_for_Chemical_Fault_Detection_and_Diagnosis_(HDLCNN-SHAP)_images/conv_5127dbdcb3adbda6.pdf-0005-21.png)


6 


![](An_Order-Invariant_and_Interpretable_Hierarchical_Dilated_CNN_for_Chemical_Fault_Detection_and_Diagnosis_(HDLCNN-SHAP)_images/conv_5127dbdcb3adbda6.pdf-0006-01.png)


Figure 5. Details of the proposed order-invariant hierarchical model based on dilated convolution. 


![](An_Order-Invariant_and_Interpretable_Hierarchical_Dilated_CNN_for_Chemical_Fault_Detection_and_Diagnosis_(HDLCNN-SHAP)_images/conv_5127dbdcb3adbda6.pdf-0006-03.png)



![](An_Order-Invariant_and_Interpretable_Hierarchical_Dilated_CNN_for_Chemical_Fault_Detection_and_Diagnosis_(HDLCNN-SHAP)_images/conv_5127dbdcb3adbda6.pdf-0006-04.png)


where _T_ = _|_ **_ft_** _|_ + _|_ **_fi_** _|_ + _|_ **_fj_** _|_ . Finally, we obtain two sets of features **_F_ 1** _,_ **_F_ 2** and each of them contains features with high correlation coefficients. The original data is reordered based on **_F_ 1** and **_F_ 2** . For each sample **_xi_** , the processed sample **_x_**<sup>**_′_**</sup> **_i_**<sup>contains</sup><sup>**_p_**features:</sup><sup>**_F ′_**=</sup> � **_f_ 1**<sup>**_′_**</sup><sup>_, . . . ,_</sup><sup>**_f ′_**</sup> **m**<sup>_,_</sup><sup>**_f ′_**</sup> **m** + **1**<sup>_, . . . ,_</sup><sup>**_f ′_**</sup> **_p_** �, where _{_ **_f_ 1**<sup>**_′_**</sup><sup>_, . . . ,_</sup><sup>**_f ′_**</sup> **_m_**<sup>_}_belongsto</sup><sup>**_F_1**and</sup> � **_f_ m**<sup>**_′_**</sup> + **1**<sup>_, . . . ,_</sup><sup>**_f ′_**</sup> **_p_** � belongs to **_F_ 2** . 

- 6) The extracted features are flattened to couple information that exists vertically and horizontally. The output data of the fully connected layer has a size of ( _N ×_ 960). 

- 7) A linear layer is used to change the dimensionality of the data. Then a softmax activation function is applied to impart non-linearity into the model and output the probability distributions of the possible classes (11 in this case). The size of the final output is ( _N ×_ 11). 

Finally, we obtain the classification results and a trained model that requires explanation. The performance of this model is described in Section IV and the interpretability method is introduced in the following subsection. 

## _B. Hierarchical Dilated Convolution Model_ 

After feature clustering, the processed data is then fed into the dilated convolution layers for feature extraction. To explain the model structure clearly, we take the data from TE dataset as input and define the processed input data as a set **_D_** = _{_ **_d_ 1** _,_ **_d_ 2** _,_ **_d_ 3** _, . . . ,_ **_dn_** _}_ , where **_di_** _∈_ **_R_**<sup>**22**</sup><sup>**_×_20**</sup> . Each data sample **_di_** has 22 features and 20 time duration. The details are shown in Fig. 5 and the procedures of the model are summarized as follows. 

- 1) The size of the processed data is ( _N ×_ 1 _×_ 22 _×_ 20) and we divide the 22 features into two segments. Since the processed data is reordered in the previous step, each segment contains highly correlated features belonging to the same cluster. Each segment has a size of ( _N ×_ 1 _×_ 11 _×_ 20). 

- 2) The segmented data is processed by a dilated convolution layer with dilation rate _r_ = 2. Then the hidden information about feature correlation is extracted locally and the size of the extracted features is ( _N ×_ 16 _×_ 7 _×_ 16). 

- 3) The extracted features are concatenated to obtain the entire information about two feature clusters. The size of the concatenated features is ( _N ×_ 16 _×_ 14 _×_ 16). 

- 4) The concatenated features are then processed by a dilated convolution layer with dilation rate _r_ = 2. This step can further extract the global information and the size of the new extracted features is ( _N ×_ 32 _×_ 10 _×_ 12). 

- 5) A max pooling layer is applied to help over-fitting and reduce the computational cost. Now the size of the extracted features is ( _N ×_ 32 _×_ 5 _×_ 6). 

## _C. Deep SHAP Explainer_ 

To interpret the order-invariant hierarchical model mentioned in Section III-B, we apply an explainer based on the SHAP method which combines deep learning important features (DeepLIFT) [20] and shapley values to leverage extra knowledge about the properties of deep neural networks to improve computational performance [5]. 

DeepLIFT is an algorithm to compute the feature importance of the input with a given output based on backpropagation [20]. This method uses a summation-to-delta property to compute the contribution scores _C_ ∆ _xi_ ∆ _y_ for each input _xi_ : 


![](An_Order-Invariant_and_Interpretable_Hierarchical_Dilated_CNN_for_Chemical_Fault_Detection_and_Diagnosis_(HDLCNN-SHAP)_images/conv_5127dbdcb3adbda6.pdf-0006-19.png)


where _y_ is the model output, ∆ _y_ = _y − y_<sup>0</sup> , ∆ _xi_ = _xi − x_<sup>0</sup> , _x_<sup>0</sup> refers to the reference input, and _y_<sup>0</sup> represents the reference output. Compared with Equation 6, if we define _φi_ = _C_ ∆ _xi_ ∆ _y_ and _φ_ 0 = _y_<sup>0</sup> , then DeepLIFT approximates SHAP values for linear models. 

Deep SHAP takes DeepLIFT as a compositional approximation of SHAP values and recursively passes the multipliers of DeepLIFT backwards through the network [5]. Deep SHAP explainer can effectively achieve linearization by combining the SHAP values computed for smaller components into SHAP values for the whole model. Therefore, we can quantify the contribution of each feature from each data sample to obtain local explanation. Based on the feature contribution of each data sample, we further interpret the model globally by 

7 

Table I 

BINARY FAULT DETECTION ACCURACY OF THE SELECTED 10 FAULTS 

|FaultID|PC<br>|A<br>|KP<br>|CA<br>|KDP<br>|CA<br>|KDI<br>|CA<br>|ML<br>|PP<br>|DSAE|VS-SVDD|MBTCN|CNN|DLCNN|HDLCNN|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||SPE|T<sup>2</sup>|SPE|T<sup>2</sup>|SPE|T<sup>2</sup>|SPE|T<sup>2</sup>|SPE|T<sup>2</sup>|||||||
|1|99.5|99.1|100.0|99.3|100.0|99.5|100.0|100.0|99.7|100.0|99.3|99.0|100.0|99.4|98.8|100.0|
|2|98.4|98.5|99.0|95.3|99.1|98.3|98.5|98.8|98.9|99.8|96.8|98.0|99.0|99.1|99.1|98.7|
|3|0.6|3.6|6.8|9.0|9.6|4.4|19.4|19.8|23.8|39.6|67.4|42.0|85.4|85.7|92.4|97.6|
|8|96.8|97.4|97.9|97.4|97.8|97.6|97.8|99.4|100.0|98.7|87.0|98.0|89.0|96.7|97.7|95.9|
|10|15.4|36.7|52.5|48.6|63.5|42.6|80.6|92.9|71.3|94.2|68.3|73.0|86.6|93.7|93.9|95.6|
|11|63.8|41.4|77.6|51.0|91.0|33.6|81.4|90.3|93.6|95.6|81.3|98.0|99.5|93.4|93.0|94.5|
|12|92.5|98.5|98.5|98.9|99.1|99.1|99.7|100.0|99.6|100.0|94.1|100.0|96.5|81.7|82.7|90.7|
|13|95.0|94.3|95.2|94.3|95.4|96.3|95.9|95.9|96.5|91.2|78.1|95.0|95.6|96.3|96.8|96.9|
|14|99.9|98.8|100.0|99.6|100.0|99.9|100.0|100.0|100.0|100.0|99.6|100.0|100.0|100.0|100.0|100.0|
|20|42.3|34.0|59.8|49.1|66.8|51.5|72.7|83.9|86.7|93.6|78.6|78.0|90.1|97.2|97.3|96.4|
|Average|70.4|70.2|78.7|74.2|82.2|72.3|84.6|88.1|87.0|91.3|85.1|88.1|94.2|94.3|95.2|**96.6**|



calculating the average value of data samples for each feature, which can be mathematically described as follows: 


![](An_Order-Invariant_and_Interpretable_Hierarchical_Dilated_CNN_for_Chemical_Fault_Detection_and_Diagnosis_(HDLCNN-SHAP)_images/conv_5127dbdcb3adbda6.pdf-0007-05.png)


where _φi_ ( _xj_ ) refers to the contribution of the feature _i_ of the input _xj_ . Finally, we identify the root-cause feature **_γ_** as the one with the highest contribution. 


![](An_Order-Invariant_and_Interpretable_Hierarchical_Dilated_CNN_for_Chemical_Fault_Detection_and_Diagnosis_(HDLCNN-SHAP)_images/conv_5127dbdcb3adbda6.pdf-0007-07.png)



![](An_Order-Invariant_and_Interpretable_Hierarchical_Dilated_CNN_for_Chemical_Fault_Detection_and_Diagnosis_(HDLCNN-SHAP)_images/conv_5127dbdcb3adbda6.pdf-0007-08.png)


## _D. The Entire Fault Detection and Diagnosis Procedure_ 

Based on the description above, the entire order-invariant and interpretable fault detection and diagnosis procedure via feature clustering, hierarchical dilated convolution model and SHAP method mainly consists of six steps: 

- 1) Collecting the monitored variables via sensors in chemical processes. Obtaining the training set from the collected samples and normalizing the data. 

- 2) Processing the training samples based on hierarchical clustering method. The features are reordered according to the clustering results and the highly correlated features are closer in the processed data. 

- 3) Training the hierarchical dilated convolution model with the processed data. Storing the model parameters for later usage. 

- 4) Acquiring online samples and processing them in the same way as mentioned above. 

- 5) Restoring the trained model and classifying the new sample into a normal or fault type. 

- 6) If a fault happens, identifying the corresponding rootcause feature based on SHAP method. Feature contribution is computed and the one with highest contribution is considered as the root-cause feature. 

## IV. EXPERIMENT STUDY 

In this paper, we use the TE dataset to verify the effectiveness of the proposed method. It simulates actual chemical processes and is widely used as a benchmark in chemical fault detection and diagnosis [21]–[23]. There are totally 21 types of faults and 22 continuous measured variables in this dataset. For the training set, it has 980 samples including 500 samples 

Figure 6. The feature clustering dendrogram of the 22 features in TE dataset. 

in the normal case and 480 samples in the case of failure for each fault type. For the test set, it has 960 samples including 160 normal samples and 800 fault samples for each fault type. Details are described in the following subsections. 

## _A. Experiment Setup_ 

The downloaded TE dataset has a sampling period of 180 seconds, leading to few data samples for training and test. Therefore, current CNN methods use simulation model to generate more data samples for feature extraction. Similarly, we refer to the simulation method from [24] on MATLAB to obtain more data for classification. The sampling period is set to 36 seconds (100 samples/h). The simulator runs for 48 hours in the normal state, then 4800 training normal samples are collected. For each fault type, the simulator runs for 48 hours to collect 4800 training fault samples. For the testing data of each fault, the simulator runs for 8 hours in the normal state at the beginning to collect 800 test normal samples. Then a fault disturbance is introduced and the simulator continues to run for 40 hours to collect 4000 test fault samples. Next, the collected data is processed in the range [0,1] to eliminate the adverse effects caused by singular data. To extract the features in both spatial and temporal domains, each data sample is reshaped into a 2-D array with 22 features and 20 time duration. 

To demonstrate the performance of our proposed model on the chemical fault detection and diagnosis, we select Fault 1, Fault 2, Fault 3, Fault 8, Fault 10, Fault 11, Fault 12, Fault 13, Fault 14, and Fault 20 for binary and multi-class fault detection and diagnosis. Fault 10 and Fault 11 are chose for 

8 


![](An_Order-Invariant_and_Interpretable_Hierarchical_Dilated_CNN_for_Chemical_Fault_Detection_and_Diagnosis_(HDLCNN-SHAP)_images/conv_5127dbdcb3adbda6.pdf-0008-01.png)


Figure 7. The t-SNE embedding of the extracted features of our proposed HDLCNN model. 

root cause analysis since their root-cause features are proven and widely used. The corresponding true root-cause features are X(18) and X(9) [21], [23]. 

## _B. Feature Clustering_ 

As shown in Fig. 1, highly correlated features are closer in the optimal order. Although it is hard to obtain the optimal order, we can cluster the features with higher correlation to achieve similar effect. As described in Section III-A, we divide the 22 features into two categorizes based on the correlation. The corresponding hierarchical clustering dendrogram is shown in Fig. 6. We can see that the first category includes 11 features which are X(1), X(2), X(3), X(4), X(8), X(9), X(12), X(14), X(15), X(17) and X(19). The second category also includes 11 features which are X(5), X(6), X(7), X(10), X(11), X(13), X(16), X(18), X(20), X(21) and X(22). Refer to the correlation coefficients of the 22 features shown in Fig. 2, we can see that the highly correlated features are classified into the same cluster. 

## _C. Contrast and Ablation Experiments_ 

Firstly, we evaluate the proposed method for binary fault detection and diagnosis. In this case, only one fault is considered at a time. To show the efficiency, the proposed HDLCNN model is compared with the existing data-driven methods including principal component analysis (PCA), kernel principal component analysis (KPCA), integrated kernel dynamic principal component analysis (KDPCA), kernel dynamic independent component analysis (KDICA) [25], modified locality preserving projection (MLPP) [26], denoising sparse autoencoder (DSAE) [22], variable selection and support vector data description (VS-SVDD) [27] and multi-block temporal convolutional network (MBTCN) [9]. As shown in Table. I, our proposed model results in the highest average fault detection rate, which is marked bold. The following experiment results are marked in a similar way. As ablation experiments, we compare CNN, DLCNN and HDLCNN. CNN is the baseline model with traditional convolution layers and DLCNN contains dilated convolution layers without hierarchical feature clustering. HDLCNN is our proposed method involving both hierarchical feature clustering and dilated convolution layers. It is obvious that the average fault detection accuracy of 

Table II 

MULTI-CLASS FAULT DETECTION ACCURACY OF THE SELECTED 10 FAULTS 

|Fault ID|PCA|DSAE|CNN|DLCNN|HDLCNN|
|---|---|---|---|---|---|
|0|5.1|51.3|85.3|92.1|99.6|
|1|51.8|98.4|99.2|99.7|97.7|
|2|78.5|97.8|94.6|95.0|97.2|
|3|25.9|14.1|94.4|100.0|100.0|
|8|4.1|44.8|89.6|93.0|94.5|
|10|8.6|36.4|95.3|99.4|98.8|
|11|16.4|45.5|90.3|93.1|93.0|
|12|12.2|68.4|73.4|95.5|93.9|
|13|45.4|23.8|92.2|75.2|93.3|
|14|50.8|97.9|100.0|100.0|100.0|
|20|41.5|72.4|89.9|91.3|92.6|
|Average|30.9|59.2|91.3|94.0|**96.4**|



Table III 

ACCURACY OF CNN, DLCNN AND HDLCNN 

||CNN|DLCNN|HDLCNN|
|---|---|---|---|
|Close-correlated Order|91.3|94.0|96.4|
|Separate-correlated Order|85.8|91.8|96.0|
|Difference|5.5|2.2|0.4|



DLCNN is increased by 1.0% compared to CNN, which shows the effect of dilated convolution. In addition, hierarchical feature clustering is proved instrumental since the average fault detection accuracy of HDLCNN is increased by 1.5% compared to DLCNN. 

Then, to explore the performance of the proposed method for multi-class fault detection and diagnosis, we combine the normal case with the selected 10 types of faults. As shown in Fig. 7, the extracted features of HDLCNN are visualized. Specifically, we utilize t-SNE method to reduce the dimension of the features to 2, and then plot them by class. It is obvious that the embedding of the extracted features belonging to different classes are separate. Therefore, it is unsurprising that the softmax layer can get accurate classification results. PCA, DSAE, CNN and DLCNN are selected as comparison methods. As shown in Table. II, the proposed model achieves the highest average fault detection rate. Similarly, we consider CNN, DLCNN and HDLCNN as ablation experiments. Due to the dilated convolution, the average fault detection accuracy of DLCNN is increased by 3.0% compared to CNN. And with hierarchical feature clustering, the average fault detection accuracy of HDLCNN is increased by 2.6% compared to DLCNN. 

## _D. Ablation Experiments of Sensitivity to Feature Order_ 

To demonstrate the ability of our proposed HDLCNN model to process tabular data with features of arbitrary order, we find the separate-correlated order of features and compare to the close-correlated order. More specifically, we consider the separate-correlated order as [X(21), X(8), X(4), X(3), X(15), X(16), X(2), X(6), X(20), X(13), X(17), X(18), X(9), X(1), X(7), X(10), X(5), X(14), X(19), X(11), X(12), X(22)], in which highly correlated features are separated. And the close-correlated order is formed in an opposite way. In this case, the average multi-class fault detection accuracy of CNN, 

9 


![](An_Order-Invariant_and_Interpretable_Hierarchical_Dilated_CNN_for_Chemical_Fault_Detection_and_Diagnosis_(HDLCNN-SHAP)_images/conv_5127dbdcb3adbda6.pdf-0009-01.png)



![](An_Order-Invariant_and_Interpretable_Hierarchical_Dilated_CNN_for_Chemical_Fault_Detection_and_Diagnosis_(HDLCNN-SHAP)_images/conv_5127dbdcb3adbda6.pdf-0009-02.png)



![](An_Order-Invariant_and_Interpretable_Hierarchical_Dilated_CNN_for_Chemical_Fault_Detection_and_Diagnosis_(HDLCNN-SHAP)_images/conv_5127dbdcb3adbda6.pdf-0009-03.png)



![](An_Order-Invariant_and_Interpretable_Hierarchical_Dilated_CNN_for_Chemical_Fault_Detection_and_Diagnosis_(HDLCNN-SHAP)_images/conv_5127dbdcb3adbda6.pdf-0009-04.png)



![](An_Order-Invariant_and_Interpretable_Hierarchical_Dilated_CNN_for_Chemical_Fault_Detection_and_Diagnosis_(HDLCNN-SHAP)_images/conv_5127dbdcb3adbda6.pdf-0009-05.png)



![](An_Order-Invariant_and_Interpretable_Hierarchical_Dilated_CNN_for_Chemical_Fault_Detection_and_Diagnosis_(HDLCNN-SHAP)_images/conv_5127dbdcb3adbda6.pdf-0009-06.png)



![](An_Order-Invariant_and_Interpretable_Hierarchical_Dilated_CNN_for_Chemical_Fault_Detection_and_Diagnosis_(HDLCNN-SHAP)_images/conv_5127dbdcb3adbda6.pdf-0009-07.png)



![](An_Order-Invariant_and_Interpretable_Hierarchical_Dilated_CNN_for_Chemical_Fault_Detection_and_Diagnosis_(HDLCNN-SHAP)_images/conv_5127dbdcb3adbda6.pdf-0009-08.png)


Figure 10. The heatmap of a single sample of Fault 10 and 11. 

Figure 8. The confusion matrices of HDLCNN. 


![](An_Order-Invariant_and_Interpretable_Hierarchical_Dilated_CNN_for_Chemical_Fault_Detection_and_Diagnosis_(HDLCNN-SHAP)_images/conv_5127dbdcb3adbda6.pdf-0009-11.png)



![](An_Order-Invariant_and_Interpretable_Hierarchical_Dilated_CNN_for_Chemical_Fault_Detection_and_Diagnosis_(HDLCNN-SHAP)_images/conv_5127dbdcb3adbda6.pdf-0009-12.png)



![](An_Order-Invariant_and_Interpretable_Hierarchical_Dilated_CNN_for_Chemical_Fault_Detection_and_Diagnosis_(HDLCNN-SHAP)_images/conv_5127dbdcb3adbda6.pdf-0009-13.png)



![](An_Order-Invariant_and_Interpretable_Hierarchical_Dilated_CNN_for_Chemical_Fault_Detection_and_Diagnosis_(HDLCNN-SHAP)_images/conv_5127dbdcb3adbda6.pdf-0009-14.png)



![](An_Order-Invariant_and_Interpretable_Hierarchical_Dilated_CNN_for_Chemical_Fault_Detection_and_Diagnosis_(HDLCNN-SHAP)_images/conv_5127dbdcb3adbda6.pdf-0009-15.png)



![](An_Order-Invariant_and_Interpretable_Hierarchical_Dilated_CNN_for_Chemical_Fault_Detection_and_Diagnosis_(HDLCNN-SHAP)_images/conv_5127dbdcb3adbda6.pdf-0009-16.png)



![](An_Order-Invariant_and_Interpretable_Hierarchical_Dilated_CNN_for_Chemical_Fault_Detection_and_Diagnosis_(HDLCNN-SHAP)_images/conv_5127dbdcb3adbda6.pdf-0009-17.png)



![](An_Order-Invariant_and_Interpretable_Hierarchical_Dilated_CNN_for_Chemical_Fault_Detection_and_Diagnosis_(HDLCNN-SHAP)_images/conv_5127dbdcb3adbda6.pdf-0009-18.png)


Figure 9. The visualization of SHAP values of a single sample of Fault 10 and 11. 

DLCNN and HDLCNN is shown in Table. III. We see that the performance of CNN and DLCNN is influenced by the order of the features and the differences are 5.5% and 2.2% respectively. This proves that dilated convolution can extract more information and weaken the effect of the feature order. Further, HDLCNN is order-invariant and the difference is only 0.4%, which confirms the effect of hierarchical feature clustering. In a word, the ablation experiments demonstrate that our proposed method can effectively process tabular data with features of arbitrary order without seeking the optimal order. The confusion matrices obtained by HDLCNN are illustrated in Fig. 8. 

## _E. Local and Global Explanation_ 

We further analyze the feature contribution and obtain the root-cause features based on SHAP values. Fault 10 and Fault 11 are selected for root cause analysis, and the corresponding true root-cause features are X(18) and X(9), respectively. For 


![](An_Order-Invariant_and_Interpretable_Hierarchical_Dilated_CNN_for_Chemical_Fault_Detection_and_Diagnosis_(HDLCNN-SHAP)_images/conv_5127dbdcb3adbda6.pdf-0009-23.png)


Figure 11. The average feature importance of Fault 10 and 11. 

Fault 10, the stripper temperature (X(18)) is directly affected because of the random variation of temperature in feed C [23]. And for Fault 11, the random variation in reactor cooling water inlet temperature results in abnormal behaviour of the reactor temperature (X(9)) [21]. 

First, local explanation is provided to indicate the feature contribution to the prediction from a single sample. Fig. 9 shows the visualization of the SHAP values of a single sample. The left column indicates the gray image of the sample, the middle column shows the SHAP values of classifying this sample to the normal case, and the right column shows the SHAP values of classifying this sample to the case of failure. Red pixels indicate high SHAP values and blue pixels denote low SHAP values. High SHAP value means great feature contribution of this sample to be classified to the corresponding type of fault. The corresponding heatmaps are shown in Fig. 10. It is obviously that the most important features are X(18) and X(9) for Fault 10 and Fault 11 respectively, which are also the true root-cause features. 

Then, global explanation is described to show the feature contribution of the overall dataset. We compute the average feature contribution for each sample and consider the feature with highest importance as the corresponding rootcause feature. Fig. 11 shows the average feature importance and the features with highest importance are marked red. We see that the most important features are X(18) and X(9) for Fault 10 and Fault 11 respectively, which are also the true root-cause features. Fig. 12 denotes the relationship between the measured feature values and the corresponding SHAP values. For Fault 10, high measured values of X(18) obviously correspond high SHAP values which means high stripper temperature (X(18)) may be the main cause of the failure. On the contrary, for Fault 11, we see that low measured values of X(9) mainly refer to high SHAP values which reminds us to pay attention to the reduction of reactor temperature (X(9)). 

10 


![](An_Order-Invariant_and_Interpretable_Hierarchical_Dilated_CNN_for_Chemical_Fault_Detection_and_Diagnosis_(HDLCNN-SHAP)_images/conv_5127dbdcb3adbda6.pdf-0010-01.png)



![](An_Order-Invariant_and_Interpretable_Hierarchical_Dilated_CNN_for_Chemical_Fault_Detection_and_Diagnosis_(HDLCNN-SHAP)_images/conv_5127dbdcb3adbda6.pdf-0010-02.png)



![](An_Order-Invariant_and_Interpretable_Hierarchical_Dilated_CNN_for_Chemical_Fault_Detection_and_Diagnosis_(HDLCNN-SHAP)_images/conv_5127dbdcb3adbda6.pdf-0010-03.png)



![](An_Order-Invariant_and_Interpretable_Hierarchical_Dilated_CNN_for_Chemical_Fault_Detection_and_Diagnosis_(HDLCNN-SHAP)_images/conv_5127dbdcb3adbda6.pdf-0010-04.png)


Figure 12. The SHAP values of the top 10 features of Fault 10 and 11. 

## V. CONCLUSION 

In this paper, we propose an order-invariant and interpretable HDLCNN-SHAP method for chemical fault detection and diagnosis based on feature clustering, dilated convolution and SHAP method. The ability to detect faults and obtain the root-cause features is essential for fault detection and diagnosis methods in real chemical processes. Comparing with the existing methods, our proposed method can effectively process tabular data with features of arbitrary order without seeking the optimal order. In addition, root-cause features are precisely identified without any human supervision. The proposed method is evaluated on a simulation dataset based on an actual chemical process. Experimental results show that the proposed method achieves better performance for both binary and multi-class fault detection and diagnosis compared with other popular data-driven methods. Moreover, the proposed method is order-invariant, which results in insensitivity to the order of the features. Local and global explanation are further described to obtain the root-cause features. In our future work, we will focus on more practical and complex fault detection problems. Simultaneous-fault diagnosis is a common problem in real applications and the problem of faults with multiple root-cause features is consequential as well. Besides, incomplete and high-dimensional datasets are worth of investigation for solving fault detection problems in real-world chemical processes. 

## REFERENCES 

- [1] T. Xie, X. Huang, and S.-K. Choi, “Intelligent mechanical fault diagnosis using multisensor fusion and convolution neural network,” _IEEE Transactions on Industrial Informatics_ , vol. 18, no. 5, pp. 3213–3223, 2021. 

- [2] N. Wang, H. Li, F. Wu, R. Zhang, and F. Gao, “Fault diagnosis of complex chemical processes using feature fusion of a convolutional network,” _Industrial & Engineering Chemistry Research_ , vol. 60, no. 5, pp. 2232–2248, 2021. 

- [3] T. Huang, Q. Zhang, X. Tang, S. Zhao, and X. Lu, “A novel fault diagnosis method based on cnn and lstm and its application in fault diagnosis for complex systems,” _Artificial Intelligence Review_ , vol. 55, no. 2, pp. 1289–1315, 2022. 

- [4] F. Yu, V. Koltun, and T. Funkhouser, “Dilated residual networks,” in _Proceedings of the IEEE conference on computer vision and pattern recognition_ , 2017, pp. 472–480. 

- [5] S. M. Lundberg and S.-I. Lee, “A unified approach to interpreting model predictions,” _Advances in neural information processing systems_ , vol. 30, 2017. 

   - [7] N. Wang, F. Yang, R. Zhang, and F. Gao, “Intelligent fault diagnosis for chemical processes using deep learning multimodel fusion,” _IEEE transactions on cybernetics_ , 2020. 

   - [8] X. Gu, Y. Zhao, G. Yang, and L. Li, “An imbalance modified convolutional neural network with incremental learning for chemical fault diagnosis,” _IEEE Transactions on Industrial Informatics_ , vol. 18, no. 6, pp. 3630–3639, 2021. 

   - [9] Y. He, H. Shi, S. Tan, B. Song, and J. Zhu, “Multiblock temporal convolution network-based temporal-correlated feature learning for fault diagnosis of multivariate processes,” _Journal of the Taiwan Institute of Chemical Engineers_ , vol. 122, pp. 78–84, 2021. 

   - [10] S. Zhong, S. Fu, and L. Lin, “A novel gas turbine fault diagnosis method based on transfer learning with cnn,” _Measurement_ , vol. 137, pp. 435– 453, 2019. 

   - [11] N. Liu, M. Hu, J. Wang, Y. Ren, and W. Tian, “Fault detection and diagnosis using bayesian network model combining mechanism correlation analysis and process data: application to unmonitored root cause variables type faults,” _Process Safety and Environmental Protection_ , 2022. 

   - [12] N. Liu, J. Wang, S. Sun, C. Li, and W. Tian, “Optimized principal component analysis and multi-state bayesian network integrated method for chemical process monitoring and variable state prediction,” _Chemical Engineering Journal_ , vol. 430, p. 132617, 2022. 

   - [13] B. Zhou, A. Khosla, A. Lapedriza, A. Oliva, and A. Torralba, “Learning deep features for discriminative localization,” in _Proceedings of the IEEE conference on computer vision and pattern recognition_ , 2016, pp. 2921– 2929. 

   - [14] R. R. Selvaraju, M. Cogswell, A. Das, R. Vedantam, D. Parikh, and D. Batra, “Grad-cam: Visual explanations from deep networks via gradient-based localization,” in _Proceedings of the IEEE international conference on computer vision_ , 2017, pp. 618–626. 

   - [15] J. H. Friedman, “Greedy function approximation: a gradient boosting machine,” _Annals of statistics_ , pp. 1189–1232, 2001. 

   - [16] A. Goldstein, A. Kapelner, J. Bleich, and E. Pitkin, “Peeking inside the black box: Visualizing statistical learning with plots of individual conditional expectation,” _journal of Computational and Graphical Statistics_ , vol. 24, no. 1, pp. 44–65, 2015. 

   - [17] M. T. Ribeiro, S. Singh, and C. Guestrin, “” why should i trust you?” explaining the predictions of any classifier,” in _Proceedings of the 22nd ACM SIGKDD international conference on knowledge discovery and data mining_ , 2016, pp. 1135–1144. 

   - [18] L. S. Shapley, “A value for n-person games,” _Classics in game theory_ , vol. 69, 1997. 

   - [19] E. Strumbelj<sup>ˇ</sup> and I. Kononenko, “Explaining prediction models and individual predictions with feature contributions,” _Knowledge and information systems_ , vol. 41, no. 3, pp. 647–665, 2014. 

   - [20] A. Shrikumar, P. Greenside, and A. Kundaje, “Learning important features through propagating activation differences,” in _International conference on machine learning_ . PMLR, 2017, pp. 3145–3153. 

   - [21] M. T. Amin, S. Imtiaz, and F. Khan, “Process system fault detection and diagnosis using a hybrid technique,” _Chemical Engineering Science_ , vol. 189, pp. 191–211, 2018. 

   - [22] P. Peng, Y. Zhang, H. Wang, and H. Zhang, “Towards robust and understandable fault detection and diagnosis using denoising sparse autoencoder and smooth integrated gradients,” _ISA transactions_ , 2021. 

   - [23] H. Yu, F. Khan, and V. Garaniya, “Nonlinear gaussian belief network based fault diagnosis for industrial processes,” _Journal of Process Control_ , vol. 35, pp. 178–200, 2015. 

   - [24] P. Peng, W. Zhang, Y. Zhang, Y. Xu, H. Wang, and H. Zhang, “Cost sensitive active learning using bidirectional gated recurrent neural networks for imbalanced fault diagnosis,” _Neurocomputing_ , vol. 407, pp. 232–245, 2020. 

   - [25] J. Fan and Y. Wang, “Fault detection and diagnosis of non-linear non-gaussian dynamic processes using kernel dynamic independent component analysis,” _Information Sciences_ , vol. 259, pp. 369–379, 2014. 

   - [26] M. Z. H. Shah, L. Hu, and Z. Ahmed, “Modified lpp based on riemannian metric for feature extraction and fault detection,” _Measurement_ , vol. 193, p. 110923, 2022. 

   - [27] L. Cai, H. Yin, J. Lin, H. Zhou, and D. Zhao, “A relevant variable selection and svdd-based fault detection method for process monitoring,” _IEEE Transactions on Automation Science and Engineering_ , 2022. 

- [6] G. S. Chadha, M. Krishnamoorthy, and A. Schwung, “Time series based fault detection in industrial processes using convolutional neural networks,” in _IECON 2019-45th Annual Conference of the IEEE Industrial Electronics Society_ , vol. 1. IEEE, 2019, pp. 173–178. 

