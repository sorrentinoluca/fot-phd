Artificial Intelligence Review (2022) 55:1289–1315 https://doi.org/10.1007/s10462-021-09993-z 

# **A novel fault diagnosis method based on CNN and LSTM and its application in fault diagnosis for complex systems** 


![](A_novel_fault_diagnosis_method_based_on_CNN_and_LSTM_and_its_application_in_fault_diagnosis_for_complex_systems_images/conv_75e311b5d1e73a24.pdf-0001-02.png)


**Ting Huang**<sup>**1,2,3**</sup> **· Qiang Zhang**<sup>**1,2,3**</sup> **· Xiaoan Tang**<sup>**1,2,3**</sup> **· Shuangyao Zhao**<sup>**1,2,3**</sup> **· Xiaonong Lu**<sup>**1,2,3**</sup> 

Published online: 2 April 2021 

© The Author(s), under exclusive licence to Springer Nature B.V. 2021 

### **Abstract** 

Fault diagnosis plays an important role in actual production activities. As large amounts of data can be collected efficiently and economically, data-driven methods based on deep learning have achieved remarkable results of fault diagnosis of complex systems due to their superiority in feature extraction. However, existing techniques rarely consider time delay of occurrence of faults, which affects the performance of fault diagnosis. In this paper, by synthetically considering feature extraction and time delay of occurrence of faults, we propose a novel fault diagnosis method that consists of two parts, namely, sliding window processing and CNN-LSTM model based on a combination of Convolutional Neural Network (CNN) and Long Short-Term Memory Network (LSTM). Firstly, samples obtained from multivariate time series by the sliding window processing integrates feature information and time delay information. Then, the obtained samples are fed into the proposed CNN-LSTM model including CNN layers and LSTM layers. The CNN layers perform feature learning without relying on prior knowledge. Time delay information is captured with the use of the LSTM layers. The fault diagnosis of the Tennessee Eastman chemical process is addressed, and it is verified that the predictive accuracy and noise sensitivity of fault diagnosis can be greatly improved when the proposed method is applied. Comparisons with five existing fault diagnosis methods show the superiority of the proposed method. 

**Keywords** Fault diagnosis · Convolutional neural network · Long short-term memory network · Data-driven · Deep learning · Tennessee eastman chemical process 

> * Qiang Zhang qiang_zhang@hfut.edu.cn 

> * Xiaoan Tang sichuanshengxiaoan@163.com 

Extended author information available on the last page of the article 

Vol.:(0123456789)1 3 

T. Huang et al. 

1290 

## **1 Introduction** 

In actual production activities, the occurrence of system faults is inevitable due to internal factors (e.g., the wear of parts) or environmental factors (e.g., drastic changes in temperature). Furthermore, these are more common in complex systems that are composed of many units with diverse relations. Once a fault happens to a complex system, it usually affects the normal operation of the system and may further lead to an immeasurable loss. Therefore, it is important to develop a fault diagnosis method for complex systems. 

In recent years, as large amounts of data can be collected efficiently and economically, data-driven methods based on deep learning (DL) have achieved remarkable results of fault diagnosis of complex systems. However, existing techniques rarely consider the time delay of the occurrence of faults, which affects the performance of fault diagnosis. In this paper, we synthetically consider two aspects of fault diagnosis of complex systems, namely, feature extraction and time delay of the occurrence of faults. 

- (1) _Feature extraction_ Raw data collected from production environments is generally highdimensional, and the attributes of the data are usually highly correlated. These kinds of characteristics may seriously affect the performance of subsequent learning algorithms, which further influences the results of fault diagnosis. When handling fault diagnosis, one first needs to identify those features that significantly affect the occurrence of faults. 

- (2) _Time delay of the occurrence of faults_ The occurrence of faults is generally a cumulative process (e.g., the wear of parts), thus there may be some time delay. That is to say, the occurrence of faults at the current moment may depend on the change of the system state at the previous moments. Capturing the time delay information contributes greatly to the performance improvement of fault diagnosis. 

Over the past several decades, many feature extraction methods for fault diagnosis have been reported in the literature. These methods were generally proposed based on the fault diagnosis of certain particular systems. In other words, the existing feature extraction methods for fault diagnosis are system-dependent and unavailable to other systems. Developing a feature extraction method that can be suitable for the fault diagnosis of different systems is an urgent problem to be solved. In recent years, the feature learning methods based on DL has been used for fault diagnosis. The feature learning methods can automatically learn useful and predictive implicit features hidden in massive data, which overcomes the shortcoming of feature extraction methods that rely excessively on domain knowledge. 

Currently, delay fault diagnosis is mainly concentrated in the field of circuits. However, the delay fault diagnosis methods in the field of circuits cannot be applied to other fields due to their specificity. In other fields, such as fault diagnosis of chemical process, rotating machines, and so on, although various fault diagnosis methods have been developed in the past decades, they rarely consider time delay of the occurrence of faults. However, it is obvious that time delay of the occurrence of faults exists widely in these systems. Therefore, there is an urgent need to develop a method to deal with time delay of the occurrence of faults. 

DL has made breakthroughs in the fields of image recognition, speech recognition, machine translation, and so on. Convolutional Neural Network (CNN) is an important technology of DL that was first used in the field of image recognition (Krizhevsky et al. 2017). Through a series of convolution operations, the CNN automatically extracts features 

1 3 

A novel fault diagnosis method based on CNN and LSTM and its… 

1291 

layer by layer. Recurrent Neural Network (RNN) is also an important DL technique. However, traditional RNN cannot handle long-term time correlations because of the problem of recursion, weighted exponential explosion, or disappearance (Kolen and Kremer 2009). Long Short-Term Memory Network (LSTM) is a special RNN that contains LSTM blocks that are smart units that can remember the value of the uncertain length of time. This property of the LSTM ensures that it can capture the time delay information. The use of DL to solve key problems in other fields has also been well studied. Considering the superiority of DL, it is interesting to study its application to fault diagnosis. 

Based on the above considerations, to manage the two aspects related to fault diagnosis of complex systems, this paper develops a DL-based fault diagnosis method by combining CNN and LSTM. In the proposed method, feature information and time delay information are first comprehensively integrated into one type of 2D image-like data obtained from a multivariate time series (MTS) by sliding window processing that is then regarded as the input of the CNN. Using CNN layers that can perform automatic feature learning, the feature maps as the input of LSTM layers are identified. The time delay information that is hidden in the 2D image-like data can be captured with the use of the LSTM layers. Following that, the learned feature information and the captured time delay information are integrated via fully connected layers as the basis for fault diagnosis. The proposed method ultimately outputs the occurrence probability of each type of pre-defined faults. Results show that the proposed method can greatly improve the performance of fault diagnosis of complex systems. Comparisons with several existing fault diagnosis methods, such as the CNN, LSTM, Artificial Neural Networks (ANN), K-Nearest Neighbor (KNN), and Support Vector Machine (SVM) methods, demonstrate the superiority of the proposed method. 

In summary, the main contributions of this study are shown as follows: 

- (1) The feature information and time delay information of MTS are integrated into one type of 2D image-like data by the proposed sliding window processing, which provides sufficient fault diagnosis information for DL model. 

- (2) Based on the 2D image-like data obtained by sliding window processing, a novel DL model combining CNN and LSTM for fault diagnosis of complex systems is proposed, which achieves the goal of feature learning and capturing the time delay of the occurrence of faults. 

- (3) The fault diagnosis of the Tennessee Eastman (TE) chemical process is addressed based on the proposed method, and it is verified that the predictive accuracy and noise sensitivity of fault diagnosis can be greatly improved. 

This paper is organized as follows: Some existing fault diagnosis methods are reviewed in Sect. 2. Section 3 presents the proposed CNN-LSTM fault diagnosis method. The implementation of the proposed method to deal with the fault diagnosis of the TE chemical process is illustrated in Sect. 4. Conclusions and future work are provided in Sect. 5. 

## **2  Literature review** 

Traditional fault diagnosis methods, such as physics of failure (Li et al. 2018a, b; Yang et al. 2013; Zhu et al. 2016) and fault tree analysis (Kabir 2017), generally focus on the operating mechanism or theoretical analysis of systems. They have been widely used in such fault diagnosis fields with high reliability requirements as aerospace and electronic. 

1 3 

T. Huang et al. 

1292 

However, when faced with such complex systems as chemical process, they are usually not feasible because it is difficult to mathematically model or analyze for these complex systems. 

With the development of sensor technology, lots of data related to system operation can be easily collected and acquired. These heterogeneous and multi-source data may involve rich information about faults. As such, in recent years, with the use of these collected data, many data-driven methods (Cai et al. 2016; Cai et al. 2017b; El-Koujok et al. 2014; Li 2018; Serdio et al. 2015; Zhang et al. 2020) have been developed for fault diagnosis and they have been widely applied in a variety industry sectors. In particular, the data-driven methods based on DL (Lei et al. 2016; Li 2018; Li et al. 2019a; Rodríguez Ramos et al. 2019; Zhang et al. 2017; Wang et al. 2020) have achieved remarkable results of fault diagnosis of complex systems due to their superiority in feature extraction. 

In general, data-driven fault diagnosis can be treated as a classification task (Aydin et al. 2012). The use of the data-driven methods for fault diagnosis usually involves the following four steps: data preprocessing, feature extraction, classifier building, and fault diagnosis. 

### **2.1  Data preprocessing** 

The raw data generally cannot be directly used as the input to the data-driven fault diagnosis methods, which implies that there is the need for data conversion to meet the input requirements of these methods. In recent years, many data conversion methods have been developed to meet the input requirements of the fault diagnosis method. For example, Liu et al. (2019) proposed an input tensor transformation scheme to transform MTS into appropriate tensor representation so that the model based on CNN can handle these data. A Signal-to-Image conversion method was proposed by Wen et al. (2018) for the fault diagnosis based on CNN. The data conversion methods proposed in these studies are differences due to their different model input requirements. Therefore, data conversion methods need to be designed according to model input requirements. 

### **2.2  Feature extraction** 

Feature extraction is a vital step to extract the features that can accurately and completely cover the information of the original data by reducing the dimension of the data and the correlation between the attributes. Over the past several decades, many feature extraction methods for fault diagnosis have been reported in the literature (Gao and Hou, 2016; Hong and Dhupia, 2014; Jing and Hou 2015; Rai and Mohanty, 2007; Yan et al. 2014). These methods were generally proposed based on the fault diagnosis of certain particular systems. For example, wavelets have been commonly used for fault diagnosis of rotating machines (Yan et al. 2014) while Principal Component Analysis (PCA) has been used in chemical systems (Jing and Hou 2015). Feature learning is a useful way to replace feature extraction. The feature learning method can automatically learn the features suitable for the problems at hand so that it overcomes the shortcoming that the feature extraction method depends heavily on specific problem and domain knowledge. In recent years, with the development of DL, DL-based feature learning methods for fault diagnosis have been extensively studied. For example, Janssens et al. (2016) proposed a DL model for condition monitoring by using CNN and proved that the feature learning method was significantly better than the feature extraction method in the fault diagnosis of rotating machines. A novel hierarchical 

1 3 

A novel fault diagnosis method based on CNN and LSTM and its… 

1293 

learning rate adaptive deep CNN model was proposed by Guo et al. (2016) to solve the problem of extracting features automatically without significantly increasing the demand for machine expertise and the problem of maximizing accuracy without overcomplicating machine structure. Furthermore, Razavian et al. (2014) demonstrated that the generic features learned from CNN are very powerful. 

### **2.3  Classifier building** 

The aim of this step is to build a classifier that can be used for fault diagnosis based on the extracted features. Many classification algorithms can be used to conduct the construction of the classifier, such as KNN (Casimir et al. 2006; Lei and Zuo 2009), SVM (Goyal et al. 2020), ANN (Seera et al. 2016), and so on. In recent years, with the development of DL, the multilayer neural network-based classifiers for fault diagnosis have emerged. In the construction of those classifiers, such as RNN-based fault diagnosis classifiers (de Bruin et al. 2017; Liu et al. 2018 ) and CNN-based fault diagnosis classifiers CNN (Feng et al. 2021; Wen et al. 2018; Wu and Zhao 2018), the FC layers are generally used to map the feature vector to the fault probability space and perform fault classification. 

### **2.4  Fault diagnosis** 

In this step, the fault state of the system can be predicted based on the output of the constructed classifier. 

On the other hand, for various systems, such as electric, pneumatic, hydraulic networks, chemical processes, long transmission lines, robotics, and so on, there may be some time delay of the occurrence of faults. In the fault diagnosis of these systems, the existence of time delay of the occurrence of faults must be considered; otherwise, the performance of fault diagnosis will drop significantly. Delay fault diagnosis has been extensively studied in circuit systems (Sivaraman and Strojwas 2001; Wang et al. 2005). More recently, a fault prediction method is proposed based on FFT, PCA, and CNN for delay circuit systems in the study (Khalil et al. 2020). In the fault diagnosis of complex electronic systems, Cai et al. (2017a) used Dynamic Bayesian network to model the dynamic degradation process of electronic products considering that the performance of electronic products degrades over time. In the fault diagnosis of rolling bearings, RNN has been used to handle the time dependence of signals (Liu et al. 2018). More generally, Gers et al. (2002) proved that LSTM can solve the problem of time delay. 

From the above analysis, we can see that DL-based fault diagnosis methods are more suitable for complex systems. In recent years, although some DL-based fault diagnosis methods have been proposed, they rarely consider the time delay of the occurrence of faults. Therefore, it is interesting to propose a DL-based fault diagnosis method for complex systems that considers both feature extraction and time delay of the occurrence of faults. 

## **3  Proposed DL‑based fault diagnosis method for complex systems** 

As shown in Fig. 1, the framework of the proposed DL-based fault diagnosis method for complex systems consists of two part, namely, sliding window processing and CNN-LSTM model. In what follows, the two parts will be introduced in detail. 

1 3 

T. Huang et al. 

1294 


![](A_novel_fault_diagnosis_method_based_on_CNN_and_LSTM_and_its_application_in_fault_diagnosis_for_complex_systems_images/conv_75e311b5d1e73a24.pdf-0006-02.png)


**Fig. 1** The framework of the proposed DL-based fault diagnosis method for complex systems 

### **3.1  Sliding window processing** 

In the sliding window processing, 2D samples can be obtained based on the raw data _X_ (Some data preprocessing has been done, such as normalization) by simultaneously considering its feature information and time delay information. A schematic diagram of sliding window processing is shown in Fig. 2. 

Let _X_ =<sup>{</sup> _xt_<sup>|</sup> | _t_ = 1, 2, 3 … _n_ } ( _xt_ ∈ _R_<sup>_m_</sup> and _X_ ∈ _R_<sup>_n_×</sup><sup>_m_</sup> ) be the raw data that is an MTS, where _xt_ is the observation vector of the system at the time _t_ , _m_ represents the 


![](A_novel_fault_diagnosis_method_based_on_CNN_and_LSTM_and_its_application_in_fault_diagnosis_for_complex_systems_images/conv_75e311b5d1e73a24.pdf-0006-07.png)


**Fig. 2** Schematic diagram of sliding window processing 

1 3 

A novel fault diagnosis method based on CNN and LSTM and its… 

1295 

number of observation attributes, and _n_ denotes the length of the observation time. Let _Y_ =<sup>{</sup> _yt_<sup>|</sup> | _t_ = 1, 2, 3 … _n_ } ( _yt_ ∈ _R_ and _Y_ ∈ _R_<sup>_n_</sup> ) be the label of _X_ . Then, samples of the raw data can be expressed as _D_ = {( _X_ , _Y_ )} . As shown in Fig. 2, a sliding window is represented by a rectangular frame whose length is the number of attributes of _X_ and width is _d_ (0 _< d_ ≤ _n_ ) . The samples used to train the model are continuously obtained from _X_ by moving the sliding window. The step size of the movement of the sliding window is an integer _𝜆_ (0 _< 𝜆_ ≤ _n_ − _d_ ) . At the _t_ th movement of the sliding window, assuming that the framed sub-series of _X_ is denoted as _X_ [ _t_ ∶ _t_ + _d_ ] , then the label of _X_ [ _t_ ∶ _t_ + _d_ ] is _Y_ [ _t_ + _d_ ] , where [ _i_ : _j_ ] denotes the operation that extracts elements between _i_ and _j_ from an ordered set. In this way, the sample ( _X_ [ _t_ ∶ _t_ + _d_ ], _Y_ [ _t_ + _d_ ]) will be used as the input feature maps of the proposed model. 

The original 1D samples (data of a certain moment of MTS) only contain feature information. After sliding window processing, the 1D samples are converted into 2D samples, which integrates feature information and time delay information. Practical meaning of these 2D samples can be interpreted as that the system state at the current time may be related to the system states of previous _d_ moments. In this way, using these 2D samples to train the fault diagnosis classification model can make it learn feature information and time delay information simultaneously, which can greatly improve the performance of fault diagnosis. Moreover, the size of feature information and time delay information contained in these 2D samples are adjustable. Specifically, the size of the feature information can be adjusted by adjusting the size of _m_ . The size of the time delay information can be adjusted by adjusting the size of _d_ . By integrating more attributes (greater _m_ ) and longer time delay (greater _d_ ) in sliding window processing, the 2D samples more suitable for fault diagnosis of complex systems can be obtained. 

The obtained 2D samples are used as the learning material of CNN-LSTM model to identify the fault category. In what follows, we will present CNN-LSTM in detail. 

### **3.2  CNN‑LSTM model** 

This subsection investigates the proposed CNN-LSTM model, which consists of CNN layers, LSTM layers, and fully connected layers as shown in Fig. 3. In what follows, the proposed model will be described in detail from these layers. 

### **3.2.1  CNN layers** 

The CNN layers consist of two operation, namely, convolution operation and activation operation. The input of the convolution operation is a 3D data _X_ ∈ _R_<sup>_w_×</sup><sup>_h_×</sup><sup>_c_</sup> , where _w_ , _h_ , and _c_ , respectively represent its width, its height, and the number of channels. In particular, when _c_ = 1 , it is reduced to 2D data, which is used as the input of the proposed model. Specifically, the horizontal axis of the 2D data represents the feature dimension and the vertical axis depicts the time dimension. The axis scales are respectively characterized by the numbers of attributes and the width of the sliding window. 

To illustrate the convolution operation clearly, we first define four super-parameters, namely, the number of convolution kernels _K_ , the size of each convolution kernel _F_ , the step size of the convolution _S_ , and the number of zeros _P_ . Then, for the convolution operation of each convolution kernel, zeros are filled into the data _X_ ∈ _R_<sup>_w_×</sup><sup>_h_×</sup><sup>_c_</sup> by which the transformed data _X_<sup>∗</sup> ∈ _R_<sup>(</sup><sup>_w_+</sup><sup>_P_)×(</sup><sup>_h_+</sup><sup>_P_)×</sup><sup>_c_</sup> is obtained. After that, the slicing operation is: 

1 3 

T. Huang et al. 

1296 


![](A_novel_fault_diagnosis_method_based_on_CNN_and_LSTM_and_its_application_in_fault_diagnosis_for_complex_systems_images/conv_75e311b5d1e73a24.pdf-0008-02.png)


**Fig. 3** Architecture diagram of CNN-LSTM model for fault diagnosis of TE chemical process 


![](A_novel_fault_diagnosis_method_based_on_CNN_and_LSTM_and_its_application_in_fault_diagnosis_for_complex_systems_images/conv_75e311b5d1e73a24.pdf-0008-04.png)


> where _tw_ ∶ _tw_ + _F_ indicates the operation of picking up the subset positioned between 

> Rows _tw_ and _tw_ + _F_ , _th_ ∶ _th_ + _F_ indicates the operation of picking up the subset positioned between Columns _th_ and _th_ + _F_ , and∶ indicates cutting all data in the channel direction. _tw_ and _th_ take values from 1 and change by step _S_ . As per the<sup>(</sup> _tw_ , _th_ ) , data _Xtw_ , _th_ can be extracted from _X_<sup>∗</sup> . Assume the convolution kernel is denoted as _K_ ernel ∈ _R_<sup>_F_×</sup><sup>_F_×</sup><sup>_c_</sup> , then _Ttw_ , _th_ ∈ _R_<sup>_F_×</sup><sup>_F_×</sup><sup>_c_</sup> is defined as element-by-element multiplication of _K_ ernel and _Xtw_ , _th_ as follows: 


![](A_novel_fault_diagnosis_method_based_on_CNN_and_LSTM_and_its_application_in_fault_diagnosis_for_complex_systems_images/conv_75e311b5d1e73a24.pdf-0008-06.png)


Subsequently, _ytw_ , _th_ can be obtained in the following manner: 


![](A_novel_fault_diagnosis_method_based_on_CNN_and_LSTM_and_its_application_in_fault_diagnosis_for_complex_systems_images/conv_75e311b5d1e73a24.pdf-0008-08.png)


where _Ttw_ , _th_ [ _i_ , _j_ , _k_ ] denotes the element of _Ttw_ , _th_ , and _Y_ ∈ _R_<sup>_w_∗×</sup><sup>_h_∗</sup> can be obtained by _ytw_ , _th_ arranged in the order of the size of _tw_ , _th_ . It can be noted that 


![](A_novel_fault_diagnosis_method_based_on_CNN_and_LSTM_and_its_application_in_fault_diagnosis_for_complex_systems_images/conv_75e311b5d1e73a24.pdf-0008-10.png)


For each convolution kernel, one can obtain a channel such as _Y_ , and then by repeating the above operations on the _K_ convolution kernels, we can obtain a new 3D data 

1 3 

A novel fault diagnosis method based on CNN and LSTM and its… 

1297 

_X_ ∈ _R_<sup>_w_∗×</sup><sup>_h_∗×</sup><sup>_K_</sup> . In general, a specific combination of ( _F_ , _P_ , _S_ ) is set to make _w_<sup>∗</sup> = _w_ and _K > c_ . 

After the convolution operation, the activation operation is essential. It enables the network to acquire a nonlinear expression of the input to enhance the representation ability and make the learned features more dividable. With the use of rectified linear unit, which is widely a used one, one can activate each element of _X_ in the following manner: 


![](A_novel_fault_diagnosis_method_based_on_CNN_and_LSTM_and_its_application_in_fault_diagnosis_for_complex_systems_images/conv_75e311b5d1e73a24.pdf-0009-04.png)



![](A_novel_fault_diagnosis_method_based_on_CNN_and_LSTM_and_its_application_in_fault_diagnosis_for_complex_systems_images/conv_75e311b5d1e73a24.pdf-0009-05.png)


> where _X_<sup>[</sup> _i_ , _j_ , _k_<sup>]</sup> denotes the element of _X_ , and _A_<sup>[</sup> _i_ , _j_ , _k_<sup>]</sup> denotes the element of _A_ ∈ _R_<sup>_w_∗×</sup><sup>_h_∗×</sup><sup>_K_</sup> that is the data obtained after activation operation. 

### **3.2.2  Connection between CNN and LSTM layers** 

The output of CNN layers is 3D data in which the extracted 2D feature maps are stacked together. The required input of LSTM layers is 2D data, where one dimension is denoted as time and the other is features. In order to connect the CNN layers and the LSTM layers, it is needed to convert the 3D data output from CNN layers into 2D data input to LSTM layers. 

In this study, a bridge is developed to connect the CNN layers and the LSTM layers. The operation of the bridge is shown in Fig. 4. In the bridge, the output of the CNN layers is rearranged as the input of the LSTM layers. The bridge first arranges the channels of the 3D data output from CNN layers so that all the extracted features are arranged together while keeping the time dimension unchanged. After this arrangement, the 3D data becomes 2D data. Then, the bridge cuts this 2D data horizontally to obtain samples for each time step of the LSTM layers. 


![](A_novel_fault_diagnosis_method_based_on_CNN_and_LSTM_and_its_application_in_fault_diagnosis_for_complex_systems_images/conv_75e311b5d1e73a24.pdf-0009-10.png)


**Fig. 4** The bridge used to connect the CNN layers and the LSTM layers 

1 3 

T. Huang et al. 

1298 

> Specifically, Suppose the output of the CNN layers is _Xcov_ ∈ _R_<sup>_w_×</sup><sup>_h_×</sup><sup>_c_</sup> , then the input of the LSTM layers obtained by the bridge can be denoted as _Xlstm_ ∈ _R_<sup>_w_∗×</sup><sup>_h_</sup> , where _w_<sup>∗</sup> = _w_ × _c_ . 


![](A_novel_fault_diagnosis_method_based_on_CNN_and_LSTM_and_its_application_in_fault_diagnosis_for_complex_systems_images/conv_75e311b5d1e73a24.pdf-0010-03.png)


where ↔ denotes the splicing operation of 2D matrixes in the row direction. 

### **3.2.3  LSTM layers** 

An LSTM layer generally involves several smart units, each of which contains three gates, namely, forget gate, input gate, and output gate. The forget gate tells which information should be forgotten, the input gate determines which inputs need to be remembered, and the output gate decides which information needs to be output. The specific calculation process of these three gates is shown in Fig. 5. 

At the forget gate, the information _ft_ that needs to be discarded can be recognized in the following way: 


![](A_novel_fault_diagnosis_method_based_on_CNN_and_LSTM_and_its_application_in_fault_diagnosis_for_complex_systems_images/conv_75e311b5d1e73a24.pdf-0010-08.png)


where _xt_ denotes the data at time _t_ , _ht_ −1 denotes the output at time _t_ − 1 , _Wf_ and _Rf_ are the weight matrices associated with _ft_ , _bf_ is the corresponding bias vector, and<sup>⋅</sup> indicates the dot product operation. 

At the input gate, the information _it_ that needs to be inputted and the candidate _Ct_ for the state value of the unit are identified based on the following operation: 


![](A_novel_fault_diagnosis_method_based_on_CNN_and_LSTM_and_its_application_in_fault_diagnosis_for_complex_systems_images/conv_75e311b5d1e73a24.pdf-0010-11.png)


and 

_Ct_ = _휑_ ( _Wc_ ⋅ _xt_ + _Rc_ ⋅ _ht_ −1 + _bc_ ) =<sup>_e_</sup> _e_<sup>((</sup><sup>_WcWc_⋅⋅</sup><sup>_xtxt_++</sup><sup>_RcRc_⋅⋅</sup><sup>_htht_−−11++</sup><sup>_bcbc_)−)</sup> +<sup>_e_</sup> _e_<sup>−−((</sup><sup>_WcWc_⋅⋅</sup><sup>_xtxt_++</sup><sup>_RcRc_⋅⋅</sup><sup>_htht_−−11++</sup><sup>_bcbc_)),</sup> (9) where _Wi_ and _Ri_ are the weight matrices associated with ∼ _it_ , _bi_ is the corresponding bias vector, _Wc_ and _Rc_ are the weight matrices associated with _Ct_ , and _bc_ is the corresponding bias vector. ∼ At the output gate, by integrating _ft_ , _it_ , _Ct_ and the state value _Ct_ −1 of the unit at time _t_ − 1 , the unit’s state value _Ct_ at time _t_ can be obtained as follows: 


![](A_novel_fault_diagnosis_method_based_on_CNN_and_LSTM_and_its_application_in_fault_diagnosis_for_complex_systems_images/conv_75e311b5d1e73a24.pdf-0010-14.png)


where × indicates the element-by-element multiplication of vectors. 


![](A_novel_fault_diagnosis_method_based_on_CNN_and_LSTM_and_its_application_in_fault_diagnosis_for_complex_systems_images/conv_75e311b5d1e73a24.pdf-0010-16.png)


**Fig. 5** One LSTM layer 

1 3 

A novel fault diagnosis method based on CNN and LSTM and its… 

1299 

Finally, with the aid of the latest state value _Ct_ , the input _xt_ of the unit, and the output _ht_ −1 of the previous unit, one can get the output _ht_ of the unit as follows: 


![](A_novel_fault_diagnosis_method_based_on_CNN_and_LSTM_and_its_application_in_fault_diagnosis_for_complex_systems_images/conv_75e311b5d1e73a24.pdf-0011-03.png)


and 


![](A_novel_fault_diagnosis_method_based_on_CNN_and_LSTM_and_its_application_in_fault_diagnosis_for_complex_systems_images/conv_75e311b5d1e73a24.pdf-0011-05.png)


## **4  Experiment and results** 

### **4.1  Introduction of the data set** 

The TE chemical process is a simulation process based on the actual process flow of a chemical company. The details of the TE chemical process can be seen in prior work (Downs and Vogel 1993). Based on the simulation process, 41 measured variables denoted by _XMEAS_ and 11 manipulated variables denoted by _XMV_ are associated with the TE chemical process data set. Accordingly, by observing the TE chemical process, an observation vector that can reflect the production at the time _t_ of the TE chemical process can be obtained as follows: 

### _xt_ = [ _XMEAS_ (1), _XMEAS_ (2), … , _XMEAS_ (41), _XMV_ (1), … , _XMV_ (11)]<sup>_T_</sup> . 

Table 7 of the Appendix shows the details of these variables. Among these variables, the sampling frequency was 20 times an hour for _XMV_ (1)- _XMV_ (11) and _XMEAS_ (1) - _XMEAS_ (22) , 10 times an hour for _XMEAS_ (23)- _XMEAS_ (36) , and 4 times an hour for _XMEAS_ (37)- _XMEAS_ (41). 

As shown in Table 8 of the Appendix, the TE chemical process included 21 pre-set faults and 1 normal state. For each fault as well as the normal state, the status of the TE chemical process was reflected in a training data set and a test data set. Each training data set contained 480 samples, and each test data set contained 960 samples. With a total of 22 system statuses, there were 22 × 480 = 10560 original training samples and 22 × 960 = 21120 original test samples. 

### **4.2  Comparative experiments** 

The proposed CNN-LSTM fault diagnosis model belongs to the category of feature learning-based methods. To demonstrate the superiority of the proposed model, we conducted two sets of comparative experiments by considering the performance of the corresponding models in three aspects: _predictive accuracy_ ( _PA_ ), _noise sensitivity_ ( _NS_ ), and _predictive real-time_ ( _PR_ ). 

- (1) The first set of comparative experiments was a comparison between the proposed model with three feature extraction-based fault diagnosis models (i.e., KNN, SVM, and ANN); 

- (2) and the second set was a comparison with two classical DL models, such as CNN and LSTM. 

1 3 

T. Huang et al. 

1300 

### **4.2.1  Sliding window processing for the data set** 

The sliding window processing ( _d_ = 52, _휆_ = 1) denoted as _W_ (52, 1) is used to obtain the 2D samples for CNN-LSTM and CNN models from the TE process data sets. _W_ (52, 1) is performed on each original training set and test set that can be viewed as MTS. The length of these MTS is 480 and 960 for each original training set and test set, respectively. One can easily calculate that the number of the obtained 2D samples by _W_ (52, 1) is 428 for original training set and it is 908 for original test set. There is a total of 22 training sets and 22 test sets, thus the total number of samples for training and test are 22 × 428 = 9416 and 22 × 908 = 19976 . The result of _W_ (52, 1) for each original training set and test set is shown in Table 1. 

### **4.2.2  Experiment setup** 

Similar to our proposed model, the classical CNN model also belongs to the type of feature learning-based fault diagnosis methods. The ANN, KNN and SVM models belong to the type of feature extraction-based fault diagnosis methods. The LSTM model has no feature extraction process, and thus it does not belong to the above two types of methods, but it performs well in capturing the time delay of the occurrence of faults. Below are some settings for these models. 

- The PCA method, which is a commonly used method at the feature extraction phase of fault diagnosis of the TE chemical process, was employed when using the feature extraction-based methods (i.e., KNN, SVM, and ANN) to conduct fault diagnosis of the TE chemical process. 

- The number of layers of all the hierarchical models (i.e., CNN-LSTM, CNN, LSTM, and ANN) was supposed to be 6 and the parameters of the models were roughly the same to make their complexity roughly equal. The detailed settings of each layer of the four models are shown in Table 2. 

- We added L2 regularization on the LSTM layers and used the dropout method in the fully connected layers to prevent over-fitting. 

### **4.2.3  Evaluation index** 

To comprehensively evaluate the performance of each model, three indexes, namely, PA, NS, and PR are introduced in this subsection. 

**Table 1** The result of sliding window processing for each training set and test set 

|Categories|Data set|Length of time series|The number of<br>the obtained 2D<br>samples|
|---|---|---|---|
|Normal or Faults 1–21|Training set|480|428|
||Test set|960|908|



1 3 

A novel fault diagnosis method based on CNN and LSTM and its… 

1301 

**Definition 1** In the test phase of the model, assume that the number of samples in the test set is _n_ , and the number of samples accurately predicted by the model is _m_ . Then, the predictive accuracy of a model is 


![](A_novel_fault_diagnosis_method_based_on_CNN_and_LSTM_and_its_application_in_fault_diagnosis_for_complex_systems_images/conv_75e311b5d1e73a24.pdf-0013-03.png)


The index of PA reflects the predictive accuracy degree of the model. The larger the PA is, the higher the predictive accuracy degree is. 

**Definition 2** Given an Additive white Gaussian noise (AWGN) _N_<sup>(</sup> 0, _휎_<sup>2)</sup> (Hughes, 1991) and is added to the test set, the index of _PAnoise_ is obtained based on the test set with noise, and the index of _PAnone_ is obtained based on the test set without noise. Then, the noise sensitivity of a model is. 


![](A_novel_fault_diagnosis_method_based_on_CNN_and_LSTM_and_its_application_in_fault_diagnosis_for_complex_systems_images/conv_75e311b5d1e73a24.pdf-0013-06.png)


_NS_ is an index that reflects the adaptability of the model used in the actual production environment. The smaller the NS is, the stronger the noise immunity of the model is. 

_Note:_ We comply with the concept of AWGN defined in Hughes (1991). According to the definition of AWGN, the mean is usually 0 and the variance reflects the size of noise. Below we introduce how to determine the variance of noise. 

First of all, we recall the notion of signal to noise ratio (SNR) as shown below, 


![](A_novel_fault_diagnosis_method_based_on_CNN_and_LSTM_and_its_application_in_fault_diagnosis_for_complex_systems_images/conv_75e311b5d1e73a24.pdf-0013-10.png)


where _Psignal_ denotes power of signal and _Pnoise_ denotes power of noise. 

Then, we assume that SNR is 30 dB, which is a general value for sensor (Murata et al. 2020). Moreover, the average power of the normalized signal _Psignal_ can be calculated by its amplitude and it is equal to 1. In this way, according to the following equation, we have _Pnoise_ ≈ 0.001. 


![](A_novel_fault_diagnosis_method_based_on_CNN_and_LSTM_and_its_application_in_fault_diagnosis_for_complex_systems_images/conv_75e311b5d1e73a24.pdf-0013-13.png)



![](A_novel_fault_diagnosis_method_based_on_CNN_and_LSTM_and_its_application_in_fault_diagnosis_for_complex_systems_images/conv_75e311b5d1e73a24.pdf-0013-14.png)


For AWGN, its variance _휎_<sup>2</sup> is defined as _Pnoise_ , so we have _휎_<sup>2</sup> = _Pnoise_ ≈ 0.001. 

**Definition 3** Assume that there are three test sets, namely, a test set with small sample size, one with a middle sample size, and one with large sample size, and the numbers of the samples in the three sets are respectively defined as _ns_ , _nm_ , and _nl_ . Moreover, _ts_ , _tm_ and _tl_ respectively denote the time taken for the prediction when the three test sets are predicted by a model. Then, the predictive real-time of the model is. 


![](A_novel_fault_diagnosis_method_based_on_CNN_and_LSTM_and_its_application_in_fault_diagnosis_for_complex_systems_images/conv_75e311b5d1e73a24.pdf-0013-17.png)


_PR_ is an index that reflects the ability of the model to meet the timeliness of a particular scenario. The smaller the _PR_ is, the better the prediction real-time performance of the model is. 

1 3 

T. Huang et al. 

1302 

**Fig. 6** Variation trends of _PA_ and _MSE_ obtained by training and validating the CNN-LSTM model 


![](A_novel_fault_diagnosis_method_based_on_CNN_and_LSTM_and_its_application_in_fault_diagnosis_for_complex_systems_images/conv_75e311b5d1e73a24.pdf-0014-03.png)


**Fig. 7** Variation trends of PA and MSE obtained by training and validating the CNN model 


![](A_novel_fault_diagnosis_method_based_on_CNN_and_LSTM_and_its_application_in_fault_diagnosis_for_complex_systems_images/conv_75e311b5d1e73a24.pdf-0014-05.png)


### **4.2.4  Results and analysis** 

The changes of _PA_ and mean square error ( _MSE_ ) in the training and validation processes of the CNN-LSTM model, CNN model, LSTM model, and ANN model are depicted in Figs. 6, 7, 8, 9. The training _PA_ and the validation _PA_ increased while the training _MSE_ and the validation _MSE_ decreased along with the increase of the iterations, and they tended to be stable when the iterations reached or exceeded certain numbers. Specifically, the training _PA_ and the validation _PA_ obtained by using the CNN-LSTM model remained at 0.9888 (see Fig. 6). In the case of the CNN model, the ANN model, and the LSTM model, the values were 0.9583, 0.6783, and 0.9841, respectively (see Figs. 7, 8, 9). The results shown in Figs. 6, 8, 9 indicate that the corresponding models did not result in severe over-fitting. Besides, in terms of convergence speed, the CNN-LSTM model outperformed the other three models. The CNN-LSTM model converged after 10 iterations (see Fig. 6), while the CNN, ANN, and LSTM models converged after 36, 60, and 22 iterations, respectively (see Figs. 7, 8, 9). 

Since the super-parameters of the KNN model and the SVM model are few, a grid search algorithm that considers all the possible values of super-parameters was used to select the optimal super-parameters of the KNN model and the SVM model. At each 

1 3 

A novel fault diagnosis method based on CNN and LSTM and its… 

1303 

**Fig. 8** Variation trends of PA and MSE obtained by training and validating the ANN model 


![](A_novel_fault_diagnosis_method_based_on_CNN_and_LSTM_and_its_application_in_fault_diagnosis_for_complex_systems_images/conv_75e311b5d1e73a24.pdf-0015-03.png)


**Fig. 9** Variation trends of PA and MSE obtained by training and validating the LSTM model 


![](A_novel_fault_diagnosis_method_based_on_CNN_and_LSTM_and_its_application_in_fault_diagnosis_for_complex_systems_images/conv_75e311b5d1e73a24.pdf-0015-05.png)


super-parameter selection process, the grid search algorithm uses a combination of superparameters to evaluate the model’s performance. The optimal super-parameters of the KNN model obtained by the grid search algorithm are given below. 

- The weight function used in prediction was selected as “distance”. In this case, closer neighbors of a query point will have a greater influence than neighbors which are further away. 

- The number of neighbors was selected as 1. 

- The power parameter for the Minkowski metric (it only works when the weight function is set to “distance”) used to calculate distance was selected as 1. 

The optimal super-parameters of the SVM model obtained by the grid search algorithm are given below. 

- The kernel function used in the SVM model (it must be one of “linear”, “polynomial”, “radial basis function”, and “sigmoid”.) was selected as “radial basis function”. The details of these kernel functions is provided in Table 3. 

- The penalty parameter of the error term was selected as 20. 

1 3 

T. Huang et al. 

1304 

**Table 2** Detailed settings of the CNN-LSTM model, CNN model, LSTM model, and ANN model, where bold indicates the operations defined in Sect 3.2.2 that realizes the connection between CNN and LSTM layers 

||Model|Name of layer|Output shape|Kernel size/Kernel number/<br>Stride/ Zero-padding|Number of<br>parameters|
|---|---|---|---|---|---|
|CNN|Layer 1|conv2d_1(Conv2D)|(None,10,52,52)|(3,3)/10/1/1|100|
||Layer 2|conv2d_2(Conv2D)|(None,20,52,52)|(3,3)/20/1/1|1820|
||Layer 3|conv2d_3(Conv2D)|(None,35,52,52)|(3,3)/35/1/1|6335|
||Layer 4|max_<br>pooling2d_1(MaxPooling2)|(None,35,26,26)|–|0|
|||conv2d_4(Conv2D)|(None,55,26,26)|(3,3)/55/1/1|17,380|
||Layer 5|max_<br>pooling2d_1(MaxPooling2)|(None,55,13,13)|–|0|
|||fatten_1(Flatten)|(None,9295)|–|0|
|||dense_1(Dense)|(None,100)|–|929,600|
||Layer 6|dropout_1(Dropout)|(None,100)|–|0|
|||dense_2(Dense)|(None,22)|–|2222|
|LSTM|Layer 1|lstm_1(LSTM)|(None,52,100)|–|61,200|
||Layer 2|lstm_2(LSTM)|(None,52,250)|–|351,000|
||Layer 3|lstm_3(LSTM)|(None,52,200)|–|360,800|
||Layer 4|lstm_4(LSTM)|(None,100)|–|120,400|
||Layer 5|dense_1(Dense)|(None,1000)|–|101,000|
||Layer 6|dropout_1(Dropout)|(None,1000)|–|0|
|||dense_2(Dense)|(None,22)|–|22,022|
|ANN|Layer 1|dense_1(Dense)|(None,60)|–|3180|
||Layer 2|dense_2(Dense)|(None,400)|–|24,400|
||Layer 3|dense_3(Dense)|(None,1000)|–|401,000|
||Layer 4|dense_4(Dense)|(None,400)|–|400,400|
||Layer 5|dense_5(Dense)|(None,300)|–|120,300|
||Layer 6|dense_6(Dense)|(None,22)|–|6622|
|CNN-LSTM|Layer 1|conv2d_1(Conv2D)|(None,10,52,52)|(3,3)/10/1/1|100|
||Layer 2|conv2d_2(Conv2D)|(None,20,52,52)|(3,3)/20/1/1|1820|
||Layer 3|**trans_1(Bridge)**|**(None,52,1040)**|–|**0**|
|||lstm_1(LSTM)|(None,52,100)|–|456,400|
||Layer 4|lstm_2(LSTM)|(None,200)|–|240,800|
||Layer 5|dense_1(Dense)|(None,1000)|–|201,000|
||Layer 6|dropout_1(Dropout)|(None,1000)|–|0|
|||dense_2(Dense)|(None,22)|–|22,022|



|**Table 3**Details of the kernel<br>functions|
|---|



|Name of kernel function|Formula|
|---|---|
|Linear|_k_<br>(<br>_x_,_xi_<br>)=_x_∙_xi_|
|Polynomial|_k_<br>(<br>_x_,_xi_<br>)= (_x_∙_xi_)_d_|
|Radial basis function|_k_<sup>(</sup>_x_,_xi_<br>)=_exp_(−||_x_−_xi_||2)|
|Sigmoid|_k_<br>(<br>_x_,_xi_<br>)=<br>_푒푥푝_(_x_−_xi_)−_exp_(−(_x_−_xi_))<br>_푒푥푝_(_x_−_xi_)+_exp_(−(_x_−_xi_))|



1 3 

A novel fault diagnosis method based on CNN and LSTM and its… 

1305 

**Table 4** The _PA_ of using a variety of models for noisy and noise-free data sets, _휇_ = 0, _휎_<sup>2</sup> = 0.001 

|Index|Feature learni<br>models|ng-based|LSTM|Feature e<br>models|xtraction|-based|
|---|---|---|---|---|---|---|
||CNN-LSTM|CNN||ANN|KNN|SVM|
|_PAnone_|0.9906|0.9583|0.9841|0.6782|0.7467|0.7662|
|_PAnoise_|0.9851|0.9085|0.9516|0.5376|0.6541|0.7107|
|Δ_acc_|0.0055|0.0498|0.0325|0.1406|0.0926|0.0555|
|_NS_|0.6|5.2|3.3|20.7|12.4|7.2|



**Table 5** Cumulative timeconsumption of prediction using different models ( _ns_ = 5, _nm_ = 10 , _nl_ = 100) 

||Feature learni<br>models|ng-based|LSTM|Feature<br>based m|extractio<br>odels|n-|
|---|---|---|---|---|---|---|
||CNN-LSTM|CNN||ANN|KNN|SVM|
|_ts_(_ms_)|209|39.60|18.10|9.06|9.58|7.92|
|_tm_(_ms_)|336|60.20|23.40|12.20|16.10|14.20|
|_tl_(_ms_)|2670|457|143|80|162|128|
|_PR_(_ms_)|27.96|4.84|1.60|0.88|1.63|1.31|



The results of _PA_ are shown in Table 4. The values of _PAnone_ and _PAnoise_ obtained by using the feature extraction-based models were below 80%, whereas the _PAnone_ and _PAnoise_ obtained by using the feature learning-based models were above 95%. This indicates that the performance of the feature learning-based models was significantly better than the feature extraction-based models in terms of predictive accuracy degree. 

On the other hand, compared to the values of _PAnone_ and _PAnoise_ obtained by using the CNN model and the LSTM model, the values obtained by using the CNN-LSTM model were larger, which indicates that the CNN-LSTM model outperforms the CNN model and the LSTM model in terms of _PA_ . Theoretically, the CNN model has strong feature learning capabilities, and the LSTM model can capture time delay information. The improvement of the CNN-LSTM model may be attributed to the integration of CNN and LSTM. Furthermore, the value of _PAnone_ ( _PAnoise_ ) dropped by 3.23% (7.66%) when only CNN was applied, and it dropped by 0.65% (3.35%) under the situation where only LSTM was used. We can see that the decrease of _PAnone_ ( _PAnoise_ ) when only LSTM is used is smaller than the one when CNN is applied, which may result from that time delay information extracted by LSTM contributes more to fault diagnosis than feature information extracted by CNN does. 

Regarding the measurement of _NS_ , the feature learning-based models generally outperformed the feature extraction-based models. This shows that the former kind of models is superior to the latter one in terms of adaptability. The value of _NS_ associated with the CNN-LSTM model was lower than the ones associated with the CNN and LSTM models, which indicates that the integration of feature information and time delay information is beneficial to the model against noise. 

Tables 5 and 6 present the computing results of _PR_ under the situations where different models were applied for fault diagnosis of the TE chemical process. One can see from Table 5 that the feature learning-based models showed worse performance than the feature extraction-based models in terms of _PR_ . This is mainly due to the relatively high 

1 3 

T. Huang et al. 

1306 

|**Table 6**Average time-<br>consumption of prediction using<br>diferent models (_ns_ =5,_nm_ =10||Feature learni<br>based models|ng-|LSTM|Feature<br>based|extracti<br>models|on-|
|---|---|---|---|---|---|---|---|
|<br>,_nl_ =100)||CNN-LSTM|CNN||ANN|KNN|SVM|
||_ts_∕_ns_(_ms_)|41.80|7.92|3.62|1.81|1.92|1.58|
||_tm_∕_nm_(_ms_)|33.6|6.02|2.34|1.22|1.61|1.42|
||_ts_∕_ns_(_ms_)|26.7|4.75|1.43|0.8|1.62|1.28|



computational cost of CNN for feature learning. One can also find that the CNN-LSTM model performed worse in terms of _PR_ compared with the CNN and LSTM models. This is mainly because the CNN-LSTM model has a bridge that is used to combine the CNN layer and the LSTM layer and the bridge greatly increases the computational complexity of the CNN-LSTM model. 

The number in Table 6 indicates how long it took for a model to predict a single sample. Interestingly, the average sample prediction time of the DL-based models (i.e., CNNLSTM model, CNN model, and LSTM model) decreased along with the increasing of the sample size. When the sample size reaches a relatively large scale, whether the performance of _PR_ of the DL-based models will be superior to the feature extraction-based models is a question that remains to be further studied. 

The experimental results show that the proposed CNN-LSTM model had a good performance in terms of _PA_ and _NS PA_ , . However, there is a trade-off relationship between _NS_ , and _PR_ . A better combination of _PA_ and _NS_ is usually accompanied by a worse _PR_ , which is results from the high complexity of a model. Therefore, the bad performance of the CNN-LSTM model in terms of _PR_ is inevitable compared to the other five models. The proposed CNN-LSTM model is an effective tool for solving the fault diagnosis problems where the requirements for _PA_ and NS are high, but the requirements for PR performance are very low. 

### **4.3  Fault modes analysis** 

We visualize the output of each layer (Conv2d_1, Conv2d_2, Lstm_2, Dense_1 and Dense_2) of the proposed CNN-LSTM model to observe the fault modes learned by the model. Firstly, we select two different samples with the same fault from the test set. Then, we use the trained CNN-LSTM model to predict the two samples. Finally, the outputs of each layer of the model are visualized as shown in Fig. 9. 

10: One can summarize the following findings from Fig. 

- (1) The outputs of Conv2d_1 layer and Conv2d_2 layer indicate that some attributes have been extracted as shown in the red box. Moreover, the extracted attributes are the same 

1 3 

A novel fault diagnosis method based on CNN and LSTM and its… 

1307 


![](A_novel_fault_diagnosis_method_based_on_CNN_and_LSTM_and_its_application_in_fault_diagnosis_for_complex_systems_images/conv_75e311b5d1e73a24.pdf-0019-02.png)


**Fig. 10** The visualizations of fault diagnosis for two samples with the same fault 

1 3 

T. Huang et al. 

1308 

for these two different samples, which may indicate that those extracted attributes highly correlated with fault mode. 

- (2) The outputs of Lstm_2 layer model the hidden state of the last LSTM unit that can be regarded as the extracted time feature. We can find that the extracted time features of the two different samples are almost identical, which may indicate that the extracted time feature highly correlated with fault model. 

- (3) The outputs of Dense_1 integrate the extracted attributes information and the extracted time feature, which can be regarded as an abstract fault mode identified by the CNNLSTM model. 

- (4) The abscissa corresponding to the peak of the visualization curve of outputs of Dense_2 is regarded as the result of fault diagnosis. We can see that the fault diagnosis results of the two different samples are consistent with their labels, which verifies the validity of the identified fault mode. 

Figure 11 shows the visualizations of fault diagnosis for two samples with different faults. One can find that the extracted attributes information, time feature and fault modes are different for the two samples with different faults, and the fault diagnosis results of the two different samples are consistent with their labels, which further verify the validity of the identified fault modes. 

## **5  Conclusions and future works** 

In this paper, we propose a novel DL-based method for the fault diagnosis of complex systems by synthetically considering feature extraction and time delay of the occurrence of faults simultaneously. The proposed fault diagnosis method consists of two parts, namely, sliding window processing and CNN-LSTM model. Samples for the development of CNNLSTM model can be obtained by sliding window processing integrating the feature information and time delay information of MTS. The developed CNN-LSTM model is a combination of CNN layers and LSTM layers. Automatic feature learning can be performed through the CNN layers. Time delay information can be captured through the LSTM layers. Through addressing the fault diagnosis of the TE chemical process, it is verified that the predictive accuracy and noise sensitivity of fault diagnosis can be greatly improved when the proposed method is applied. Comparisons with several existing fault diagnosis methods show the superiority of the proposed method. 

The following aspects are worthy of future research: 

1 3 

A novel fault diagnosis method based on CNN and LSTM and its… 

1309 


![](A_novel_fault_diagnosis_method_based_on_CNN_and_LSTM_and_its_application_in_fault_diagnosis_for_complex_systems_images/conv_75e311b5d1e73a24.pdf-0021-02.png)


**Fig. 11** The visualizations of fault diagnosis for two samples with different faults 

1 3 

T. Huang et al. 

1310 

- (1) The fault diagnosis of TE chemical process is considered as an application of the proposed method. To further verify the generalization of the proposed method, using it to solve fault diagnosis of such complex systems as wind turbine blades (Du et al. 2020), rotor (Nath et al. 2020), gearbox (Wu et al. 2019), subsea pipelines (Cai et al. 2020) and so on, deserves further study. 

- (2) DL is a kind of “black box” approach with little interpretability, which weakens the reliability of fault diagnosis that is a critical goal for fault diagnosis. On the other hand, such traditional fault diagnosis methods as physics of failure and fault tree analysis are reliable. How to integrate these reliable methods into DL to improve the interpretability of DL-based fault diagnosis methods is worthy of further research. 

- (3) The fault data collected from real industrial scene is rare owing to that the system is not allowed to run for a long time under fault conditions. It is a big challenge for DL when the collected data is insufficient. It may be a good attempt to integrate knowledge of complex systems into DL models for solving this problem (Feng et al. 2021; Li et al. 2019b; Yu and Liu 2020). Therefore, how to integrate system knowledge into the DLbased fault diagnosis model is worthy of in-depth study. 

## **Appendix** 

See Tables 7 and 8. 

1 3 

A novel fault diagnosis method based on CNN and LSTM and its… 

1311 

|**Table 7**Variables involved in the<br>TE chemical process and their|Variable|Description|Unit|
|---|---|---|---|
|<br>description|_XMV_(1)|D Feed Flow (stream 2) (Corrected Order)|kg/hr|
||_XMV_(2)|E Feed Flow (stream 3) (Corrected Order)|kg/hr|
||_XMV_(3)|A Feed Flow (stream 1) (Corrected Order)|kscmh|
||_XMV_(4)|A and C Feed Flow (stream 4)|kscmh|
||_XMV_(5)|Compressor Recycle Valve|%|
||_XMV_(6)|Purge Valve (stream 9)|%|
||_XMV_(7)|Separator Pot Liquid Flow (stream 10)|m3/hr|
||_XMV_(8)|Stripper Liquid Product Flow (stream 11)|m3/hr|
||_XMV_(9)|Stripper Steam Valve|%|
||_XMV_(10)|Reactor Cooling Water Flow|m3/hr|
||_XMV_(11)|Condenser Cooling Water Flow|m3/hr|
||_XMEAS_(1)|A Feed (stream 1)|kscmh|
||_XMEAS_(2)|D Feed (stream 2)|kg/hr|
||_XMEAS_(3)|E Feed (stream 3)|kg/hr|
||_XMEAS_(4)|A and C Feed (stream 4)|kscmh|
||_XMEAS_(5)|Recycle Flow (stream 8)|kscmh|
||_XMEAS_(6)|Reactor Feed Rate (stream 6)|kscmh|
||_XMEAS_(7)|Reactor Pressure|kPa gauge|
||_XMEAS_(8)|Reactor Level|%|
||_XMEAS_(9)|Reactor Temperature|Deg C|
||_XMEAS_(10)|Purge Rate (stream 9)|kscmh|
||_XMEAS_(11)|Product Sep Temp|Deg C|
||_XMEAS_(12)|Product Sep Level|%|
||_XMEAS_(13)|Prod Sep Pressure<br>|kPa gauge|
||_XMEAS_(14)|Prod Sep Underfow (stream 10)|m3/hr|
||_XMEAS_(15)|<br>Stripper Level|%|
||_XMEAS_(16)|Stripper Pressure|kPa gauge|
||_XMEAS_(17)|Stripper Underfow (stream 11)|m3/hr|
||_XMEAS_(18)|<br>Stripper Temperature|Deg C|
||_XMEAS_(19)|Stripper Steam Flow|kg/hr|
||_XMEAS_(20)|Compressor Work|kW|
||_XMEAS_(21)|Reactor Cooling Water Outlet Temp|Deg C|
||_XMEAS_(22)|Separator Cooling Water Outlet Temp|Deg C|
||_XMEAS_(23)|Component A in stream 6|mole %|
||_XMEAS_(24)|Component B in stream 6|mole %|
||_XMEAS_(25)|Component C in stream 6|mole %|
||_XMEAS_(26)|Component D in stream 6|mole %|
||_XMEAS_(27)|Component E in stream 6|mole %|
||_XMEAS_(28)|Component F in stream 6|mole %|
||_XMEAS_(29)|Component A in stream 9|mole %|
||_XMEAS_(30)|Component B in stream 9|mole %|
||_XMEAS_(31)|Component C in stream 9|mole %|
||_XMEAS_(32)|Component D in stream 9|mole %|
||_XMEAS_(33)|Component E in stream 9|mole %|
||_XMEAS_(34)|Component F in stream 9|mole %|
||_XMEAS_(35)|Component G in stream 9|mole %|



1 3 

T. Huang et al. 

1312 

|**Table 7**(continued)|Variable|Description|Unit|
|---|---|---|---|
||_XMEAS_(36)|Component H in stream 9|mole %|
||_XMEAS_(37)|Component D in stream 11|mole %|
||_XMEAS_(38)|Component E in stream 11|mole %|
||_XMEAS_(39)|Component F in stream 11|mole %|
||_XMEAS_(40)|Component G in stream 11|mole %|
||_XMEAS_(41)|Component H in stream 11|mole %|



**Table 8** Details of faults of the TE chemical process 

|No|Description|Fault type|
|---|---|---|
|1|A/C feed fow ratio changes, component B content remains the same (fow 4)<br>|Step|
|2|The content of component B changes, and the A/C feed fow ratio does not<br>change (fow 4)<br>|Step|
|3|The temperature of material D changes (fow 2)|Step|
|4|Reactor cooling water inlet temperature changes|Step|
|5|Condenser cooling water inlet temperature changes<br>|Step|
|6|Material A loss (fow 1)<br>|Step|
|7|Material C pressure loss (fow 4)<br>|Step|
|8|The composition of materials A, B, and C changes (fow 4)<br>|Random variables|
|9|<br>The temperature of material D changes (fow 2)<br>|Random variables|
|10|The temperature of material C changes (fow 2)|Random variables|
|11|Reactor cooling water inlet temperature changes|Random variables|
|12|Condenser cooling water inlet temperature changes|Random variables|
|13|Random Variables|Slow drift|
|14|Reactor cooling water valve|stick to|
|15|Condenser cooling water valve|stick to|
|16|Unknown|Unknown|
|17|Unknown|Unknown|
|18|Unknown|Unknown|
|19|Unknown|Unknown|
|20|Unknown<br>|Unknown|
|21|Flow 4 valve is fxed in steady state position|Constant position|



**Acknowledgements** This research was supported by the Foundation for Innovative Research Groups of the National Natural Science Foundation of China (No. 71521001), and the National Natural Science Foundation of China (Nos. 71690230, 71690235, 71501056, 71601066, 71901086, 71501055, 71571060, 71501054 and 71571166). 

1 3 

A novel fault diagnosis method based on CNN and LSTM and its… 

1313 

## **References** 

Aydin I, Karakose M, Akin E (2012) An adaptive artificial immune system for fault classification. J Intell Manuf 23(5):1489–1499 

Cai B, Liu H, Xie M (2016) A real-time fault diagnosis methodology of complex systems using objectoriented Bayesian networks. Mech Syst Signal Process 80:31–44 

Cai B, Liu Y, Xie M (2017a) A dynamic-bayesian-network-based fault diagnosis methodology considering transient and intermittent faults. IEEE Trans Autom Sci Eng 14(1):276–285 

Cai B, Zhao Y, Liu H, Xie M (2017b) A data-driven fault diagnosis methodology in three-phase inverters for pmsm drive systems. IEEE Trans Power Electron 32(7):5590–5600 

Cai B, Shao X, Liu Y, Kong X, Wang H, Xu H, Ge W (2020) Remaining useful life estimation of structure systems under the influence of multiple causes: subsea pipelines as a case study. IEEE Trans Industr Electron 67(7):5737–5747 

Casimir R, Boutleux E, Clerc G, Yahoui A (2006) The use of features selection and nearest neighbors rule for faults diagnostic in induction motors. Eng Appl Artif Intell 19(2):169–177 

de Bruin, T., Verbert, K., & Babuška, R (2017) Railway track circuit fault diagnosis using recurrent neural networks. _IEEE Trans Neural Netw Learn Syst 28_ (3), 523–533 

Downs JJ, Vogel EF (1993) A plant-wide industrial process control problem. Comput Chem Eng 17(3):245–255 

Du Y, Zhou S, Jing X, Peng Y, Wu H, Kwok N (2020) Damage detection techniques for wind turbine blades: a review. Mech Syst Signal Process 141:106445 

El-Koujok M, Benammar M, Meskin N, Al-Naemi M, Langari R (2014) Multiple sensor fault diagnosis by evolving data-driven approach. Inf Sci 259:346–358 

Feng J, Yao Y, Lu S, Liu Y (2021) Domain knowledge-based deep-broad learning framework for fault diagnosis. IEEE Trans Industr Electron 68(4):3454–3464 

Gao X, Hou J (2016) An improved SVM integrated GS-PCA fault diagnosis approach of tennessee eastman process. Neurocomputing 174:906–911 

Gers FA, Schraudolph NN, Schmidhuber J (2002) Learning precise timing with LSTM recurrent networks. J Mach Learn Res 3:115–143 

Goyal D, Choudhary A, Pabla BS, Dhami SS (2020) Support vector machines based non-contact fault diagnosis system for bearings. J Intell Manuf 31:1275–1289 

Guo X, Chen L, Shen C (2016) Hierarchical adaptive deep convolution neural network and its application to bearing fault diagnosis. Measurement 93:490–502 

Hong L, Dhupia JS (2014) A time domain approach to diagnose gearbox fault based on measured vibration signals. J Sound Vib 333(7):2164–2180 

Hughes B (1991) On the error probability of signals in additive white Gaussian noise. IEEE Trans Inf Theory 37(1):151–155 

Janssens O, Slavkovikj V, Vervisch B, Stockman K, Loccufier M, Verstockt S, Van de Walle R, Van Hoecke S (2016) Convolutional neural network based fault detection for rotating machinery. J Sound Vib 377:331–345 

Jing C, Hou J (2015) SVM and PCA based fault classification approaches for complicated industrial pro- 

cess. Neurocomputing 167:636–642 

Kabir S (2017) An overview of fault tree analysis and its application in model based dependability analysis. Expert Syst Appl 77:114–135 

Khalil K, Eldash O, Kumar A, Bayoumi M (2020) Machine Learning-Based Approach for Hardware Faults Prediction. Regular Papers, IEEE Transactions on Circuits and Systems I, pp 1–13 

Kolen JF, Kremer SC (2009) Gradient Flow in Recurrent Nets: The Difficulty of Learning Long-Term Dependencies. Wiley-IEEE Press, In A Field Guide to Dynamical Recurrent Networks 

Krizhevsky A, Sutskever I, Hinton GE (2017) ImageNet classification with deep convolutional neural networks. Commun ACM 60(6):84–90 

- Lei Y, Zuo MJ (2009) Gear crack level identification based on weighted K nearest neighbor classification algorithm. Mech Syst Signal Process 23(5):1535–1547 

- Lei Y, Jia F, Lin J, Xing S, Ding S (2016) An intelligent fault diagnosis method using unsupervised feature learning towards mechanical big data. IEEE Trans Industr Electron 63(5):3137–3147 

- Li C (2018) Improving forecasting accuracy of daily enterprise electricity consumption using a random forest based on ensemble empirical mode decomposition. Energy 165:1220–1227 

- Li C, Cerrada M, Cabrera D, Sanchez RV, Pacheco F, Ulutagay G, Valente de Oliveira J (2018a) A comparison of fuzzy clustering algorithms for bearing fault diagnosis. Journal of Intelligent and Fuzzy Systems 34(6):3565–3580 

1 3 

T. Huang et al. 

1314 

Li H, Huang H, Li Y, Zhou J, Mi J (2018b) Physics of failure-based reliability prediction of turbine blades using multi-source information fusion. Appl Soft Comput 72:624–635 

Li C, de Oliveira JV, Cerrada M, Cabrera D, Sanchez RV, Zurita G (2019a) A systematic review of fuzzy formalisms for bearing fault diagnosis. IEEE Trans Fuzzy Syst 27(7):1362–1382 

Li X, Zhang W, Ding Q (2019b) Understanding and improving deep learning-based rolling bearing fault diagnosis with attention mechanism. Signal Process 161:136–154 

Liu H, Zhou J, Zheng Y, Jiang W, Zhang Y (2018) Fault diagnosis of rolling bearings with recurrent neural network-based autoencoders. ISA Trans 77:167–178 

Liu C, Hsaio WH, Tu Y (2019) Time series classification with multivariate convolutional neural network. IEEE Trans Industr Electron 66(6):4788–4797 

Murata, M., Kuroda, R., Fujihara, Y., Otsuka, Y., Shibata, H., Shibaguchi, T., et al. (2020) A high nearinfrared sensitivity over 70-dB SNR CMOS image sensor with lateral overflow integration trench capacitor. _IEEE Trans Electron Devices 67_ (4), 1653–1659 Nath AG, Udmale SS, Singh SK (2020) Role of artificial intelligence in rotor fault diagnosis: a comprehensive review. Artif Intell Rev. https:// doi. org/ 10. 1007/ s10462- 020- 09910-w 

Rai VK, Mohanty AR (2007) Bearing fault diagnosis using FFT of intrinsic mode functions in HilbertHuang transform. Mech Syst Signal Process 21(6):2607–2615 Razavian, A. S., Azizpour, H., Sullivan, J., and Carlsson, S. (2014). CNN Features Off-the-Shelf: An Astounding Baseline for Recognition. _2014 IEEE Conference on Computer Vision and Pattern Recognition Workshops_ , 512–519 

- Rodríguez Ramos A, Domínguez Acosta C, Rivera Torres PJ, Serrano Mercado EI, Beauchamp Baez G, Rifón LA, Llanes-Santiago O (2019) An approach to multiple fault diagnosis using fuzzy logic. J Intell Manuf 30(1):429–439 

Seera M, Lim CP, Loo CK (2016) Motor fault detection and diagnosis using a hybrid FMM-CART model with online learning. J Intell Manuf 27(6):1273–1285 

- Serdio F, Lughofer E, Pichler K, Pichler M, Buchegger T, Efendic H (2015) Fuzzy fault isolation using gradient information and quality criteria from system identification models. Inf Sci 316:18–39 

- Sivaraman M, Strojwas AJ (2001) Path delay fault diagnosis and coverage-a metric and an estimation technique. IEEE Trans Comput Aided Des Integr Circuits Syst 20(3):440–457 

- Wang, Y., Pan, Z., Yuan, X., Yang, C., & Gui, W (2020) A novel deep learning based fault diagnosis approach for chemical process with extended deep belief network. _ISA Transactions 96_ , 457–467 

- Wang Z, Marek-Sadowska MM, Tsai KH, Rajski J (2005) Delay-fault diagnosis using timing information. IEEE Trans Comput Aided Des Integr Circuits Syst 24(9):1315–1325 

- Wen L, Li X, Gao L, Zhang Y (2018) A New Convolutional neural network-based data-driven fault diagnosis method. IEEE Trans Industr Electron 65(7):5990–5998 

- Wu H, Zhao J (2018) Deep convolutional neural network model based chemical process fault diagnosis. Comput Chem Eng 115:185–197 

- Wu Q, Guo Y, Chen H, Qiang X, Wang W (2019) Establishment of a deep learning network based on feature extraction and its application in gearbox fault diagnosis. Artif Intell Rev 52(1):125–149 

- Yan R, Gao R, Chen X (2014) Wavelets for fault diagnosis of rotary machines: a review with applications. Signal Process 96:1–15 

- Yang L, Agyakwa PA, Johnson CM (2013) Physics-of-failure lifetime prediction models for wire bond interconnects in power electronic modules. IEEE Trans Device Mater Reliab 13(1):9–17 

- Yu J, Liu G (2020) Knowledge extraction and insertion to deep belief network for gearbox fault diagnosis. Knowl-Based Syst 197:105883 

- Zhang W, Peng G, Li C, Chen Y, Zhang Z (2017) A new deep learning model for fault diagnosis with good anti-noise and domain adaptation ability on raw vibration signals. Sensors 17(2):425 

- Zhang C, Guo Q, Li Y (2020) Fault detection in the tennessee eastman benchmark process using principal component difference based on k-nearest neighbors. IEEE Access 8:49999–50009 

- Zhu S, Huang H, Peng W, Wang H, Mahadevan S (2016) Probabilistic physics of failure-based framework for fatigue life prediction of aircraft gas turbine discs under uncertainty. Reliab Eng Syst Saf 146:1–12 

1 3 

A novel fault diagnosis method based on CNN and LSTM and its… 

1315 

## **Authors and Affiliations** 

**Ting Huang**<sup>**1,2,3**</sup> **· Qiang Zhang**<sup>**1,2,3**</sup> **· Xiaoan Tang**<sup>**1,2,3**</sup> **· Shuangyao Zhao**<sup>**1,2,3**</sup> **· Xiaonong Lu**<sup>**1,2,3**</sup> 

Ting Huang huangting@mail.hfut.edu.cn 

Shuangyao Zhao zsyjiu91@163.com 

Xiaonong Lu xnlu@hfut.edu.cn 

- 1 School of Management, Hefei University of Technology, Box 270, Hefei 230009, Anhui, People’s Republic of China 

- 2 Key Laboratory of Process Optimization and Intelligent Decision-Making, Ministry of Education, Box 270, Hefei 230009, Anhui, People’s Republic of China 

- 3 Ministry of Education Engineering Research Center for Intelligent Decision-Making and Information System Technologies, Hefei 230009, Anhui, People’s Republic of China 

1 3 

