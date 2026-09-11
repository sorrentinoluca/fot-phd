# **Three-layer deep learning network random trees for fault detection in chemical production process** 

Ming Lu, Zhen Gao, Ying Zou, Zuguo Chen, Pei Li 

School of Information and Electrical Engineering, Hunan University of Science and Technology, Xiangtan, China 

# **Correspondence** 

Zhen Gao, School of Information and Electrical Engineering, Hunan University of Science and Technology, Xiangtan, China. 

Email: Z.Gao@mail.hnust.edu.cn 

# **Funding information** 

National Natural Science Foundation of China, Grant/Award Numbers: 62203164, 62373144; Scientific Research Fund of Hunan Provincial Education Department (Outstanding Young Project), Grant/Award Number: 21B0499; Hunan Provincial Department of Education, Grant/Award Number: 22A0349 

# **Abstract** 

With the development of technology, the chemical production process is becoming increasingly complex and large-scale, making fault detection particularly important. However, <mark>current detection methods struggle to address the complexities of large-scale production processes</mark> . In <mark>this paper, we integrate the strengths of deep learning and machine learning technologies, combining the advantages of bidirectional long and short-term memory neural networks, fully connected neural networks, and the extra trees algorithm to propose a novel fault detection model named three-layer deep learning network random trees (TDLN-trees)</mark> . First, <mark>the deep learning component extracts temporal features from industrial data, combining and transforming them into a higher-level data representation.</mark> Second, <mark>the machine learning component processes and classifies the features extracted in the first step.</mark> An experimental analysis based on the Tennessee Eastman process verifies the superiority of the proposed method. 

1 

# **KEYWORDS** 

chemical production, process monitoring, fault detection, TDLN-trees, Tennessee Eastman 

# **1 INTRODUCTION** 

In the rapidly developing chemical production field, the emergence of intelligent control systems <mark>presents new opportunities and challenges</mark><sup>[1]</sup> <mark>.</mark> The control system can intelligently schedule and utilize resources to maximize production efficiency. <mark>However, the complex processes and harsh operating conditions in chemical production expose control systems to risks like toxic corrosion and safety management challenges</mark><sup>[2]</sup> <mark>.</mark> Interdependence of system components means that failure of any component can cause cascading failures, leading to serious property damage<sup>[3]</sup> . This risk is compounded by the production process's instability. These issues underline the urgent need for intelligent and effective fault detection and diagnosis (FDD) methods in the chemical industry to make the production process more flexible and controllable<sup>[4,5]</sup> . 

The development and refinement of FDD methods have long been a key research focus. Traditional FDD methods include nonlinear observer-based method, filter-based method, differential geometry method, and so on. The nonlinear observer-based method converts the nonlinear fault <mark>detection</mark> problem into a linear fault <mark>detection</mark> problem for special nonlinear systems<sup>[6]</sup> ; The filter-based method generates residuals at the equilibrium point of the system for local linearization for nonlinear discrete systems<sup>[7]</sup> ; The differential geometry method decomposes the system in state transformations, and designs observers for the decomposed subsystems to realize the detection and separation of faults<sup>[8]</sup> . However, with the advent of the big data era, the complex and huge amount of data makes it difficult for these methods to maintain accuracy and timeliness in FDD<sup>[9]</sup> . 

The above shifts have promoted the adoption of FDD methods based on data-driven approaches, which are no longer based on traditional physical models or theoretical knowledge for troubleshooting, but rather on understanding the system behaviour by analyzing large amounts of data<sup>[10]</sup> . Data-driven FDD methods include statistical-based methods, machine learning-based methods, and deep learning-based methods. Statistical-based methods such as principal component analysis (PCA) and partial least squares (PLS). Both PCA and PLS belong 

2 

to the data dimensionality reduction techniques. PCA simplifies data structure by transforming it into linearly uncorrelated variables through orthogonal transformation<sup>[11]</sup> . Alakent et al. proposed the ICApIso-PCA method to construct a nonlinear fractional matrix, and apply the ICAPCA method to realize the detection and isolation of nonlinear faults<sup>[12]</sup> . It addresses the issue of traditional methods which are highly susceptible to the smearing effect. However, the method currently does not fully account for the dynamic characteristics in measurement matrix. PLS builds linear regression models between multiple predictor and response variables to elucidate industrial processes<sup>[13]</sup> . <mark>However, neither can be applied to nonlinear systems. To address this issue, kernel principal component analysis (KPCA) was developed.</mark> KPCA is the nonlinear extension of PCA, which maps the original features to a high-dimensional space via the kernel function to make the nonlinear structure linearly separable, and then performs PCA in the space<sup>[14]</sup> . KPCA can address <mark>the nonlinear challenges in complex industrial processes. However, selecting the suitable KPCA kernel and adjusting its parameters relies on prior experience.</mark> 

Machine learning-based FDD methods such as the support vector machine (SVM), Manifold Learning-based method and random forest algorithm (RF), etc<sup>[15]</sup> . <mark>SVM is suitable for nonlinear, high-dimensional systems, constructing hyperplanes to separate variable state classes in a multidimensional space for fault detection</mark><sup>[16,17]</sup> <mark>.</mark> However, SVM is a binary classification algorithm, requiring an extension strategy for multiclassification problems, which causes an additional computational load. Manifold Learning-based method aims to capture lowdimensional, embedded representation of high-dimensional data. Zhang et al. proposed a manifold-based data monitoring method by integrating distance and angle information between point pairs to address the issues of inaccurate downscaling in high-dimensional data and the underutilization of information<sup>[18]</sup> . However, the method is designed for manufacturing process data under a single working condition, with limited effect in multiple conditions. RF is an integrated learning algorithm, which realizes fault detection ~~b~~ y constructing a decision tree with multiple subsets of different features<sup>[19]</sup> . RF performs well on multiclassification problems but is not an optimal choice for high-dimensional data or structured data. <mark>The Extra Trees algorithm (ET) improves upon RF by introducing greater randomness.</mark> Arya M et al. utilized ET to select the best subset of features, which were fed into a deep learning network for early-stage diabetes prediction with an accuracy of over 97%<sup>[20]</sup> . <mark>S. Yousefi et al. applied ET to machine part fault</mark> 

3 

detection <mark>, optimizing ET parameters with the Bayesian optimization method, reaching up to 99% accuracy</mark><sup>[21]</sup> <mark>.</mark> 

<mark>As industrial processes become more automated and complex.</mark> Deep learning-based FDD methods are becoming the cutting edge of the field<sup>[22]</sup> . Deep learning-based FDD methods include autoencoder (AE), convolutional neural network (CNN), and long-short-term memory network (LSTM), etc. AE can learn the compressed representation of input data and reconstruct input data, then determine the occurrence of faults by monitoring the reconstruction errors of fault data<sup>[23]</sup> . However, the feature extraction and recognition ability of AE <mark>are weaker than those of some supervised learning algorithms.</mark> CNN performs well in the domains with spatial correlation such as image recognition and video analytics, it identifies the fault patterns by learning the spatial hierarchies in the data to realize fault detection<sup>[24]</sup> . Yuan et al. proposed a method named variable correlation analysis-based convolutional neural network (VCA-CNN) for far topological feature extraction and industrial predictive modelling, and was validated on hydrocracking and debutanizer column process<sup>[25]</sup> . However, its special convolution kernel is mainly used for CNN and has limitations in generalizing to other models. <mark>LSTM, ideal for data with temporal correlations, learns long and short-term dependencies through a gating mechanism to capture anomalous patterns over time</mark><sup>[26]</sup> <mark>. Zhang S et al. i</mark> nnovatively <mark>combined LSTM with a trapezoidal auto-encoder for application to continuous stirred-tank heaters and the Tennessee Eastman Benchmark Process, achieving over 95% fault detection rate</mark><sup>[27]</sup> <mark>.</mark> Because the number of hidden layer nodes in LSTM has impacts on the accuracy of fault detection and the number of iterations to find the optimal solution, <mark>Han Y et al. determined the optimal number of LSTM hidden layer nodes for various faults by comparing training errors, resulting in enhanced fault detection accuracy</mark><sup>[28]</sup> <mark>. Y</mark> uan et al. proposed a method named Attention-Based Interval Aided Networks (AIA-Net) for modelling multivariate time-series data with heterogeneous sample intervals and missing values, and is successfully applied to predict the C5 and C6 content in the light naphtha during real hydrocracking process<sup>[29]</sup> . 

To address the above background, we integrate the strengths of deep learning techniques and machine learning techniques, combine the advantages of bidirectional long and short-term memory neural network (BLSTM), LSTM, fully connected neural network (FCNN), and ET, and propose a new fault detection model named three-layer deep learning network random trees 

4 

(TDLN-trees). TDLN-trees starts with the sliding window method to extract offline samples of industrial process variables, which ensures the temporal integrity and relevance of the data. Next, the fault data are normalized with normal operating state data, and the fault labels are one-hot encoded. In the process of online fault detection, TDLN-trees uses the multiple LSTM and FCNN structures in its Deep Learning component (DL) to capture and fit complex features from the time series data, then ET in the Machine Learning component (ML) to realize fault classification. 

In the experimental section, the proposed method is compared with other state-of-the-art methods based on TEP benchmark dataset, and TDLN-trees achieves a fault detection rate (FDR) of 98.46%, which is the highest among the evaluated methods, confirming the superior performance of TDLN-trees in fault detection. The ablation study demonstrates the significance of each component of TDLN-trees in enhancing detection capabilities. The experimental outcomes reveal the promising application of TDLN-trees for handling large-scale, highdimensional, nonlinear data. 

The rest of the paper is organized as follows: section 2 reviews the basic theory of BLSTM, LSTM, and ET. <mark>Section 3 introduces the data extraction and preprocessing operations required for fault detection by TDLN-trees.</mark> Section 4 presents the <mark>structural c</mark> omponents of TDLN-trees and the fault detection steps. An experimental analysis based on the Tennessee Eastman process is conducted in Section 5 to validate the effectiveness of TDLN-trees. Finally, <mark>Section 6</mark> provides conclusions. 

# **2 PRELIMINARIES** 

TDLN-trees combine the advantages of algorithms such as LSTM, BLSTM, and ET, and the following is a brief description of these methods: 

# **2.1 LSTM** 

LSTM is a modified Recurrent Neural Network (RNN) model, as shown in Figure 1(A and B) demonstrates the network structure of RNN and LSTM. LSTM <mark>achieves t</mark> he adaptive memory of important information and accurate forgetting of redundant information by adding three gating structures, namely, the forget gate _f_ , the input gate _i_ , and the output gate _o_ . Moreover, 

5 

LSTM overcomes the problems of gradient explosion and vanishing that RNNs face when processing complex time series data<sup>[30,31]</sup> . 


![](Three-layer_deep_learning_network_random_trees_for_fault_detection_in_chemical_production_process_(TDLN-trees)_images/conv_7c79688583aec35f.pdf-0006-01.png)


**Figure 1.** The structure of RNN and LSTM. 

The forget gate _f_ <mark>determines which information from the previous time step is discarded at</mark> 

<mark>time t.</mark> The value of the forget gate _f_ is <mark>denoted a</mark> s _ft_ (Equation (1)). The input gate _i_ and its accompanying candidate cell state gate _S_ determine which information will be added to the memory cell at time t, <mark>denoting</mark> the values of the input gate _i_ and the candidate cell state gate _S_ as _it_ and _St_ (Equations (2) and (3)), respectively. The updated value _Ct_ of the memory cell at time t is based on the forget gate, the input gate, and the candidate state gate (Equation (4)). The output gate _o_ determines which information is output by this memory cell at time t, the value of the output gate _o_ is <mark>denoted a</mark> s _ot_ (Equation (5)), and the output of the memory cell is <mark>denoted as</mark> _ht_ (Equation (6)). At the initial time (t = 0), _it_ , _Ct_ , and _ot_ are <mark>typically</mark> set to a value 

close to 0, while _ft_ is usually initialized to a value close to 1. The state values of each gate at time t are as follows: 


![](Three-layer_deep_learning_network_random_trees_for_fault_detection_in_chemical_production_process_(TDLN-trees)_images/conv_7c79688583aec35f.pdf-0006-06.png)


As time goes on, the feature information of the data passes sequentially through the memory cells <mark>and is added to or deleted from the memory cells through gate structures,</mark> enabling LSTM to process time-series data <mark>effectively.</mark> 

# **2.2 BLSTM** 

<mark>BLSTM, developed from LSTM, introduces the concepts of forward and reverse temporal directions, allowing the network to consider both past and future information of the input data sequence. BLSTM captures the before-and-after temporal relationships more comprehensively</mark><sup>[32]</sup> <mark>. Its structure is shown in Figure 2.</mark> 


![](Three-layer_deep_learning_network_random_trees_for_fault_detection_in_chemical_production_process_(TDLN-trees)_images/conv_7c79688583aec35f.pdf-0007-03.png)


**Figure 2.** The structure of BLSTM. (Conca is the abbreviation for concatenate.) 

<mark>The forward LSTM unit captures past information of the input data sequence, and the reverse LSTM unit focuses on future information.</mark> The BLSTM combines the hidden layer state<sup>_hF_</sup> _t_<sup>of the forward LSTM unit and the hidden layer state</sup><sup>_hR_</sup> _t_<sup>of the reverse LSTM unit at the</sup> time t to have the output _Ht_ , which are represented as follows: 


![](Three-layer_deep_learning_network_random_trees_for_fault_detection_in_chemical_production_process_(TDLN-trees)_images/conv_7c79688583aec35f.pdf-0007-06.png)


7 


![](Three-layer_deep_learning_network_random_trees_for_fault_detection_in_chemical_production_process_(TDLN-trees)_images/conv_7c79688583aec35f.pdf-0008-00.png)


<mark>where</mark> _ht_ − _F_ 1 and _ct_ − _F_ 1 <mark>are the output values and state update values of the forward LSTM unit at the previous moment,</mark> _ht_ + _R_ 1 and _ct_ + _R_ 1 <mark>are the reverse LSTM unit's, respectively, [ , ]denotes the concatenating operation.</mark> 

# **2.3 ET** 

<mark>ET, an integrated learning method, constructs unpruned decision trees in a top-down way, similar to RF, but introduces more randomness and diversity</mark><sup>[33]</sup> <mark>.</mark> 


![](Three-layer_deep_learning_network_random_trees_for_fault_detection_in_chemical_production_process_(TDLN-trees)_images/conv_7c79688583aec35f.pdf-0008-04.png)


**Figure 3.** The structure of ET. 

As shown in Figure 3, ET analyzes the complete raw data for constructing the decision tree. Firstly, a subset of features is randomly selected to construct a single decision tree. Secondly, for continuous feature subsets, the feature values are sorted and each unique value is considered as a potential split point; For discrete feature subsets, a potential split is considered between consecutive feature value. Finally, the Gini index for each potential division is calculated, and the division with the smallest Gini index is selected for node classification. In Figure 3, bagging represents represents bootstrap sampling on the original data, and the base layer represents the decision tree, with blue circles indicating root nodes, orange intermediate nodes, and green leaf 

8 

nodes. The Gini index of the sample set D is denoted as _Gini_ (D) , and the Gini index of the 

<mark>subset of D as</mark> _Ginisub_ (D _v_ ) . These are expressed as follows: 


![](Three-layer_deep_learning_network_random_trees_for_fault_detection_in_chemical_production_process_(TDLN-trees)_images/conv_7c79688583aec35f.pdf-0009-02.png)



![](Three-layer_deep_learning_network_random_trees_for_fault_detection_in_chemical_production_process_(TDLN-trees)_images/conv_7c79688583aec35f.pdf-0009-03.png)


where 𝑉 denotes the total number of separable subsets of 𝐷, 𝑝𝑖𝑣 is the proportion of class 𝑖th samples in subset 𝐷<sup>𝑣</sup> , and 𝑦 is the total number of sample classes 

The Gini index quantifies the influence of features on the results, and the smaller the Gini index, <mark>the more likely the samples in the node belong to the same class</mark><sup>[34]</sup> <mark>.</mark> Therefore, ET selects the division points by calculating the Gini index, which improves the fault detection performance of the model by selecting the divisions favourable to the current node while maintaining the randomness of the tree. 

# **3 PREPARATION FOR TDLN-TREES FAULT DETECTION** 

<mark>TDLN-trees for fault detection tasks require extracting the corresponding timing features of chemical production data and performing preprocessing operations such as normalization and one-hot encoding. The specific details are as follows:</mark> 

# **3.1 Data extraction based on sliding-windows method** 

In this paper, we use the sliding window method to capture features with temporal correlation. The core concept of the sliding window method involves sliding a window of width _w_ and step size _s_ across the sample set until its end, thereby generating continuous and partially overlapping feature matrices while integrating fault types into label matrices. The features extracted by the sliding window method can help the model to perceive the temporal evolution of data, expressed as follows: 


![](Three-layer_deep_learning_network_random_trees_for_fault_detection_in_chemical_production_process_(TDLN-trees)_images/conv_7c79688583aec35f.pdf-0009-10.png)


9 

where _M F_ , _k_ and _M L_ , _k_ represent the feature and label matrix windows of the _kth_ sample set respectively, _<u>N</u>_ − _<u>w</u>_ + 1 is the largest integer not exceeding _N_ − _w_ + 1, and _N_ is the size of sample _s s_ set, requiring _k_ to be greater than _w_ . In the detection stage, if _N_ is less than _w_ , then _M F_ , _k_ 

consists of all the feature vectors of the _kth_ sample set. The same applies to _M L_ , _k_ . 

The values of _w_ and _s_ must be finely tuned through experimental validation. The choice of _w_ should consider the temporal correlation and avoid introducing extraneous historical data, thereby lessening the computational load of model. Similarly, selecting _s_ should strike a balance between preserving adequate information and minimizing redundancy. <mark>Properly selected</mark> _w_ and _s_ can <mark>ensure the data features contain both the dynamic and static aspects of the chemical production process, facilitating subsequent processing.</mark> 

# **3.2 Data normalization using data from normal operating state** 

<mark>Data features extracted using the sliding window method vary significantly across physical units and value ranges, necessitating to be normalized. This ensures a consistent scale for each feature type and balances the learning of model across all features.</mark> 

# **3.3 One-hot encoding for sample data labels** 

<mark>To adapt the sample labels for the input of model, we apply one-hot encoding to the label matrix generated by the sliding window method.</mark> Specifically: for a sample with n categories, each category is mapped to an n-dimensional binary vector, <mark>collectively forming a matrix.</mark> It can <mark>eliminate the ordinal relationship between labels, enabling the model to more effectively understand and process the fault information of sample.</mark> One-hot coding is expressed as follows: 


![](Three-layer_deep_learning_network_random_trees_for_fault_detection_in_chemical_production_process_(TDLN-trees)_images/conv_7c79688583aec35f.pdf-0010-07.png)


where _j_ denotes the _jth_ sample, _i_ represents the _ith_ labeling category (0≤ _i_ ≤ _n_ ), and all positions are 0 except for the _ith_ element, which is 1. 

# **4 TDLN-TREES FAULT DETECTION** 

This section describes in detail the structure of TDLN-trees and the process of TDLN-trees for fault detection in real chemical production. 

10 

# **4.1 Establishment of the TDLN-trees** 

<mark>Addressing the issues of high complexity and challenging fault detection in the chemical</mark> 

<mark>production process, this subsection proposes a new fault detection model named TDLN-trees. Its structure is shown in Figure 4.</mark> The specific details are as follows: 


![](Three-layer_deep_learning_network_random_trees_for_fault_detection_in_chemical_production_process_(TDLN-trees)_images/conv_7c79688583aec35f.pdf-0011-03.png)


**Figure 4.** The structure of TDLN-trees. 

<mark>Given the continuous nature of chemical production, process variables fall within the time series category. The BLSTM layer, constituting the first key part of TDLN-trees, is introduced initially.</mark> The addition of the BLSTM layer <mark>allows t</mark> he model to capture the forward and backward <mark>temporal d</mark> ynamics of industrial process variable data, <mark>its output is represented by</mark> Equation (9). Subsequently, the output of the BLSTM layer is fed into the LSTM layer, which is the second key part of TDLN-trees. <mark>This LSTM layer further improves the capacity of model to capture short-term dependencies in process variable data, with its output in Equation (6).</mark> Next, the output of the LSTM layer is <mark>relayed t</mark> o the FCNN layer, the third key part of TDLN- 

11 

trees. The FCNN layer can combine and transform temporal features to enhance the ability of TDLN-trees to <mark>interpret</mark> higher-level data. Its output is as follows: 


![](Three-layer_deep_learning_network_random_trees_for_fault_detection_in_chemical_production_process_(TDLN-trees)_images/conv_7c79688583aec35f.pdf-0012-01.png)



![](Three-layer_deep_learning_network_random_trees_for_fault_detection_in_chemical_production_process_(TDLN-trees)_images/conv_7c79688583aec35f.pdf-0012-02.png)


where 𝑥 denotes the input features, 𝑊 denotes the weight matrix, 𝑏 is the bias, the value of 𝜆 is 1.05070098 and 𝛼 is 1.67326324. 

The BLSTM layer, LSTM layer, and FCNN layer collaboratively process the complex <mark>temporal d</mark> at <mark>a, constituting DL. Cross-entropy loss evaluates the fault detection capability of DL.</mark> It indicates <mark>the discrepancy between the probability distributions of the model's output and the actual labels.</mark> And we adjust the component parameters to minimize the cross-entropy loss and improve the fault detection rate of TDLN-trees. 

Next is the introduction of ET, ET belongs to ML of TDLN-trees. <mark>The FCNN layer output is passed to ET, which selects division points using the Gini index (Equation (11)) and maps process variable features to corresponding fault types.</mark> Therefore, through the above steps, TDLN-trees can improve the accuracy of fault detection and reduce the occurrence of false alarms and omissions to ensure <mark>the stability and safety of chemical system operations.</mark> 

# **4.2 TDLN-trees fault detection process** 

<mark>This section explains the application of TDLN-trees in fault detection within real chemical production.</mark> As shown in Figure 5, <mark>fault detection comprises two</mark> parts: offline fault learning stage and online fault detection stage. 

12 


![](Three-layer_deep_learning_network_random_trees_for_fault_detection_in_chemical_production_process_(TDLN-trees)_images/conv_7c79688583aec35f.pdf-0013-00.png)


**Figure 5.** TDLN-trees fault detection process. 

Offline stage fault learning: as shown in Figure 5. Firstly, the offline time series data are processed using the sliding window method to obtain the feature and label matrices with temporal correlation; Secondly, preprocessing operations are conducted on the matrix, including normalizing the fault data using normal state data, and one-hot encoding the label matrix; Then, these are divided into a training set and a validation set as inputs to the TDLN- 

13 

trees, and the DL is trained, and the parameters of the DL are adjusted to compute the crossentropy loss; Finally, input the training and validation sets into the trained TDLN-trees again, ML fits the FCNN’s middle layer output of the training set, and further optimizes the parameters of DL and ML based to the classification results of ML on the output of validation set. Fault detection can be performed by realizing the above operations. 

Online stage fault detection: As shown in Figure 5. Firstly, the online chemical production monitoring data is processed using the same preprocessing method described above, including sliding window extraction and normalization; Secondly, the processed data are input into TDLN-trees, and the temporal features are extracted after processing with the optimized DL; Lastly, classification is performed using ML, and Extra Trees compares the Gini indices to determine the fault classes of the monitored data. 

# **5 EXPERIMENT** 

To <mark>validate</mark> the fault detection performance of TDLN-trees, we conduct various experiments based on the Tennessee Eastman Process (TEP) dataset, and select precision, Receiver Operating Characteristic (ROC) curves, and Fault Detection Rate (FDR) as indicators to <mark>assess</mark> the fault detection performance, precision and FDR are as follows: 


![](Three-layer_deep_learning_network_random_trees_for_fault_detection_in_chemical_production_process_(TDLN-trees)_images/conv_7c79688583aec35f.pdf-0014-04.png)


where TP represents the number of correctly detected faults; FP represents the number of incorrectly predicted faults; FN represents the number of undetected faults. 

14 

# **5.1 Tennessee Eastman Process** 

TEP is a complex model for simulating chemical processes, and is often <mark>utilized to test</mark> the effectiveness of process monitoring and fault detection methods<sup>[35]</sup> . As shown in Figure 6<sup>[36]</sup> , the TEP model <mark>comprises</mark> five operating units: Stripping Column, Condenser, Compressor, Reactor, and Separator. <mark>For detailed roles of these operating units, refer to references [37,38].</mark> A series of chemical reactions were carried out in these operating units, where the <mark>gas-phase reactants A, C, D, and E are converted to liquid-phase products G and H, generating by-products F, and B</mark> is an inert ingredient not participating in the chemical reaction. <mark>For the specific chemical reaction process, refer to reference [39].</mark> 


![](Three-layer_deep_learning_network_random_trees_for_fault_detection_in_chemical_production_process_(TDLN-trees)_images/conv_7c79688583aec35f.pdf-0015-02.png)


**Figure 6.** The process diagram of TEP. 

TEP can simulate the normal operating state and 20 fault states of the chemical process. It contains 11 manipulated variables and 41 measurement variables, and gathering these 52 variables <mark>reflects t</mark> o the operational state of the system<sup>[40]</sup> . As shown in Table 1, 0 represents the normal operating state, and 1 to 20 represents the different types of fault states. Since the mean and variance parameters did not show significant variations in fault types 3, 9, and 15, we exclude these three fault types for further analysis and evaluation. The training set consists of 500 samples for each operational state of TEP, with faults indicated after the 20th sample, over 500 simulation runs comprising 250,000 samples in total. The testing set consists of 960 samples for each operational state of TEP, with faults introduced at the 160th sample, over 500 

15 

simulation runs comprising 480,000 samples in total. Furthermore, during training, 80% of the training set is allocated for training, and the remaining 20% constitutes the validation set. **Table 1.** TEP disturbances table. 

|Fault ID|Fault description|Fault Type|
|---|---|---|
|0|**-**|normal state|
|1|A/C feed ratio, B composition constant (stream 4)|Step|
|2|B composition, A/C ratio constant (stream 4)|Step|
|3|D feed temperature (stream 2)|Step|
|4|Reactor cooling water inlet temperature|Step|
|5|Condenser cooling water inlet temperature|Step|
|6|A feed loss (stream 1)|Step|
|7|C header pressure loss - reduced availability (stream 4)|Step|
|8|A, B, C feed composition (stream 4)|Random variation|
|9|D feed temperature (stream 2)|Random variation|
|10|C feed temperature (stream 4)|Random variation|
|11|Reactor cooling water inlet temperature|Random variation|
|12|Condenser cooling water inlet temperature|Random variation|
|13|Reaction kinetics|Slow drift|
|14|Reactor cooling water valve|Sticking|
|15|Condenser cooling water valve|Sticking|
|16|Unknown|Random variation|
|17|Unknown|Random variation|
|18|Unknown|Random variation|
|19|Unknown|Sticking|
|<br>20|<br>Unknown|Random variation|



# **5.2 Parameter Setting** 

The parameters of TDLN-trees are adjusted based on the performance of the DL training and ET's furtherclassification results. After parameter tuning, if the number of BLSTM neurons is set to 600, and LSTM to 300 or more, the training and validation set accuracies (later referred to as ‘accuracies’) are both above 99.7%, and the training time is 601.27 s; If they are reduced to 400 and 200, respectively, the accuracies is 99.85% and 99.67%, and the time is 476.45 s; If reduced to 100 and 50 or less, respectively, the accuracies drop to at least 96%, and the time is 287.57 s. Too many neurons will lead to DL overfitting and increase training time. Conversely, the learning ability is limited. Setting these two involves a combination of theoretical and empirical considerations, this manuscript takes a compromise, as shown in Table 2. Similarly, if the number of neurons in the FCNN input layer is set to 800 or more, dropout rate is 70%, and intermediate layer is 180. The accuracy is higher than 99.68%, but the time is at least 513.78 

16 

s, and a dropout rate of 70% is too radical. If the input layer is reduced to less than 180, the dropout rate is 0%, and the intermediate layer is 0, the accuracy of training set reaches 99% or above, but the validation set is at most 95.82%, and overfitting occurs. After debugging, it is found that compared with directly reducing the number of neurons, a higher dropout rate is more beneficial for improving the model's generalization performance, and the structure of the FCCN is set as shown in Table 2. The parameter n_estimators determines the number of decision trees, and max_depth limits the maximum depth of each decision trees. Setting estimators to 200 or more and depth to at least 30, the precision of TDLN-trees can reach 98.67% or more, but the fitting time of et is at least 146.71 s. Decreasing estimators to less than 70 and increasing depth to more than 60 results in a precision of 94.53% and a time of 13.91 s. Continuing to increase the depth to more than 100 has no significant improvement on TDLNtrees. Considering that TEP is complex and DL has captured the deep temporal relationships in TEP, thus more decision trees are built to learn the data features comprehensively, as shown in Table 2. Taking the input layer as an example, 'None' represents the batch size for TDLN-trees, <mark>while 2</mark> 0 and 52 represent the time step and the number of features, respectively. Other parameters are set, as shown in Table 3. 

Finally, we verify the effect of different window lengths w and step size s on TDLN-tress training, as shown in Table 4, and select w of 30 and s of 20 for comprehensive performance. The TEP is divided into normal state data and fault data, and segmenting it for sampling avoids the generation of mixed window and ensures no data loss. 

**Table 2.** The parameters of TDLN-trees subnetwork layers. 

|Layers<br>C|omponent|Architecture/Parameters|
|---|---|---|
|Input|DL|None × 30 × 52|
|BLSTM|DL|None × 30 × 256|
|LSTM|DL|None × 128|
|FCNN|DL|None × 500 - dropout(0.4)<br>- None × 180 - None × 18|
|Extra Trees|ML|n_estimators=112<br>max_depth=31|



17 

**Table 3.** Other parameter setting. 

|acti|vation function|batch size|optimizer|
|---|---|---|---|
|tanh<br>(BLSTM)|tanh<br>(LSTM)<br>selu<br>(FCNN)|1024|adam|



**Table 4.** The impact of different values of w and s on training effects. 

|w|s|Accuracy(%)|Time(s)|
|---|---|---|---|
|35|15|**99.67**|598.54|
|35|20|99.67|515.08|
|30|10|99.66|675.28|
|**30**|**20**|**99.62**|**339.57**|
|30|25|99.46|**321.11**|
|25|10|99.18|637.36|
|25|20|99.04|335.13|
|20|5|98.7|901.97|
|20|10|98.5|621.15|



# **5.3 Experimental Results and Analysis** 

# 5.3.1 Accuracy and loss curves 

As shown in Figure 7 is the accuracy and loss curves for the training and validation set, the red line and purple line in Figure 7A represent the accuracy of the training and validation set, respectively, while the blue and green line in Figure 7B represent their cross-entropy loss. In the first 10 epochs of 50 epochs, the accuracy of the training and validation set continues to increase, and the accuracy of validation set can stably exceed 99.6% in the last 20 epochs, with the highest accuracy <mark>reaching</mark> 99.6%, corresponding to a loss of 0.0096. These results <mark>demonstrate t</mark> he feasibility of TDLN-trees. 

18 


![](Three-layer_deep_learning_network_random_trees_for_fault_detection_in_chemical_production_process_(TDLN-trees)_images/conv_7c79688583aec35f.pdf-0019-00.png)



![](Three-layer_deep_learning_network_random_trees_for_fault_detection_in_chemical_production_process_(TDLN-trees)_images/conv_7c79688583aec35f.pdf-0019-01.png)


**Figure 7.** (A) The accuracy of training and validation set, (B) The loss of training and validation set. 

# 5.3.2 Visual analysis of TDLN-trees feature learning 

In order to illustrate the effectiveness of TDLN-trees after training, the feature learning capability of DL is visualized and analyzed using the t-distributed Stochastic Neighbour Embedding method (t-SNE), which can reduce high-dimensional data to two dimensions and analyze the data characteristics directly. As shown in Figure 8, Figures 8A and 8B show 

19 

scatter plots of feature separability before and after processing the original data with DL, different colours indicate different fault classes. As shown in Figure 8A, most of the fault classes are mixed, whereas in Figure 8B, after DL processing, the fault classes are all distinguished into distinct clusters of different colors with minimal overlap. Therefore, TDLNtrees can fully learn the temporal characteristics of data to prepare for fault detection. 


![](Three-layer_deep_learning_network_random_trees_for_fault_detection_in_chemical_production_process_(TDLN-trees)_images/conv_7c79688583aec35f.pdf-0020-01.png)



![](Three-layer_deep_learning_network_random_trees_for_fault_detection_in_chemical_production_process_(TDLN-trees)_images/conv_7c79688583aec35f.pdf-0020-02.png)


**Figure 8.** Visuali ation results of TEP fault detection features for t-SNE. (A) Before processing, (B) After processing 

20 

# 5.3.3 Analysis of fault detection results 

To study the performance of TDLN-trees in detecting different operating states of TEP, randomly selected 2000 samples from each TEP state for testing. The fault detection results, analyzed for class prediction distribution, are shown in Figure 9, where the horizontal axis represents the actual TEP classes, and the vertical axis shows the number of samples. It is evident that the FDRs for all states exceed 90%. As shown in Figure 10, which depicts the confusion matrix for online fault detection of TDLN-trees, with rows indicating the predicted classes and columns the actual classes, the main diagonal value representing the precision of fault classification, while the off-diagonal elements indicate the proportion of misclassification. Darker colours indicate higher classification precision. Figure 10 reveals the outstanding performance of TDLN-trees in online fault detection, and the average FDR of TDLN-trees is as high as 98.46% for the 18 operational states of TEP, which confirms the excellence of TDLNtrees. 


![](Three-layer_deep_learning_network_random_trees_for_fault_detection_in_chemical_production_process_(TDLN-trees)_images/conv_7c79688583aec35f.pdf-0021-02.png)


**Figure 9.** Detection **c** lass prediction distribution of TDLN-trees 

21 


![](Three-layer_deep_learning_network_random_trees_for_fault_detection_in_chemical_production_process_(TDLN-trees)_images/conv_7c79688583aec35f.pdf-0022-00.png)


**Figure 10.** Confusion matrix of fault detection for TDLN- trees. 

# 5.3.4 Receiver Operating Characteristic curves 

The ROC curves, <mark>with the vertical axis representing the true-positive rate and the horizontal axis denoting the false-positive rate,</mark> show the trend of the true-positive rate and false-positive rate of <mark>TDLN-trees</mark> across <mark>various c</mark> lassification thresholds. <mark>The closer the Area Under Curve (AUC) is to 1.00, the better the TDLN-trees perform in fault detection. A</mark> s shown in Figure 12, the ROC curves for the normal state and the 17 faulty states all tend to converge to the upper left of the figure, <mark>with all AUCs being at least 0.97,</mark> while <mark>the micro and macro ROC curves</mark> 

22 

<mark>have AUCs of 0.99.</mark> These results demonstrate that TDLN-trees can maintain a high FDR <mark>while</mark> reducing the false-positive rate for different fault states. 


![](Three-layer_deep_learning_network_random_trees_for_fault_detection_in_chemical_production_process_(TDLN-trees)_images/conv_7c79688583aec35f.pdf-0023-01.png)


**Figure 11.** Roc curves of fault detection for TDLN-trees. 

# **5.4 Comparison with other state-of-the-art methods** 

We compare TDLN-trees with other state-of-the-art methods for fault detection, and experimentally validate them on TEP. As shown in Table 5, the FDR of TDLN-trees is 98.56%, which is higher than that of other methods, and its FDRs for faults 1, 4, 7, and 14 are 100%. MWRSPCA<sup>[41]</sup> has an FDR of only 70.42%, its overemphasis on sparsity ignores some of the important features and affects the FDR. <mark>TceOne</mark><sup>[42]</sup> <mark>records an FDR below 53% for faults 5 and 16, due to its One-class classifier approach that relies on features from normal state data, hindering its ability to handle fault states that are not markedly different from normal states or are highly variable. T</mark> he FDR of T-BiLSTM<sup>[43]</sup> is 96.62%, and the FDR of fault 16 is less than 90%. T-BiLSTM incorporates dynamic time wrapping to consider the temporal relationship, and the fault propagation time delay will result in a small FDR in case of inconsistency with the model assumptions. <mark>DHSF-DBN</mark><sup>[44]</sup> <mark>has an FDR 0.8% lower than TDLN-trees, and Target Transformer</mark><sup>[45]</sup> <mark>has an FDR of 94.45%, neither matching TDLN-trees in adapting to complex</mark> 

23 

<mark>chemical production data.</mark> TVAE<sup>[46]</sup> has an FDR of 2.98% lower than TDLN-trees, <mark>as it loses some original data details</mark> when compressing data into a low-dimensional space, ignoring small key features. TDLN-trees can comprehensively capture the dynamic and transient features of time series data, combining and transforming these features to form a higher level data expression with enhanced feature differentiation, and then apply ET for classifying these data to achieve improved fault detection results. This comparison experiment confirms the robustness and superiority of TDLN-trees among different faults. 

**Table 5.** FDRs of TDLN-trees and other state-of-the-art methods for TEP. 

|Fault|MWRSPCA|TceOne|T-BiLSTM|DHSF-DBN|Target<br>Transformer|TVAE|Proposed<br>method|
|---|---|---|---|---|---|---|---|
|1|99.80|99.80|98.90|99.88|99.75|98.70|**100.00**|
|2|99.66|98.90|**100.00**|99.50|98.44|98.40|99.96|
|4|9.63|**100.00**|98.3|**100.00**|99.62|**100.00**|**100.00**|
|5|31.36|41.50|97.10|**100.00**|91.88|97.10|99.84|
|6|99.58|**100.00**|98.60|**100.00**|98.21|99.30|99.94|
|7|**100.00**|**100.00**|97.40|**100.00**|99.94|**100.00**|**100.00**|
|8|**99.65**|97.40|97.60|99.62|95.56|97.30|99.24|
|10|53.13|97.00|93.70|88.75|**97.69**|96.50|97.44|
|11|39.82|98.00|96.90|93.38|98.06|85.50|**99.88**|
|12|99.64|89.80|93.70|**99.75**|97.06|95.90|92.58|
|13|**98.69**|98.00|95.60|96.75|96.12|97.10|94.36|
|14|95.70|99.80|97.60|**100.00**|98.75|99.20|**100.00**|
|16|32.73|52.50|89.70|97.87|52.69|93.30|**99.38**|
|17|89.52|98.60|96.70|98.87|94.75|90.10|**99.22**|
|18|91.60|93.30|97.40|90.00|94.25|**98.30**|95.72|
|19|16.42|98.70|95.70|99.75|98.69|92.80|**99.88**|
|20|40.25|96.00|97.70|97.87|94.25|92.20|**98.16**|
|Average|70.42|91.72|96.62|97.76|94.45|95.98|**98.56**|



# **5.5 Ablation experiment** 

We remove <mark>DL</mark> and ML from the TDLN-trees framework sequentially to assess their contributions, the experimental results are shown in Table 6. Compared to TDLN-tree, the FDR is reduced by 6.44% and 0.81% when <mark>DL</mark> and ML are removed, respectively, indicating that both components can improve the fault detection performance of TDLN-trees, the details described as follows: 

24 

<mark>DL:</mark> as shown in Table 6, the fault detection performance is worse when <mark>DL</mark> is removed, <mark>particularly for faults 10, 11, 16, and 20, with FDR reductions of 11.79%, 20.62%, 16.71%, and 24.35%, respectively. DL can handle the complex patterns and correlations in time series data, capture long and short-term dependencies, and refine and enhance feature representations. Thus, adding DL</mark> to the TDLN-trees framework results in better fault detection performance than without DL. 

ML: as shown in Table 6, the FDRs for faults 10 and 17 of TDLN-trees are reduced by 4.06% and 3.73%, respectively, when ML is removed. ML can integrate <mark>multiple decision trees, classifying features extracted by DL using the Gini index, thereby enhancing</mark> the generalization ability of TDLN-trees <mark>across various fault types.</mark> Therefore, <mark>incorporating M</mark> L into the TDLNtrees framework can improve the FDR of TDLN-trees. 

<mark>In summary, both DL and ML are crucial for enhancing the fault detection performance of TDLN-trees, with their combination offering the most significant improvement in real chemical production.</mark> 

**Table 6.** FDRs of TDLN-trees in ablation experiment. 

|Fault|Without<br>DL component|Δ|Without<br>ML component|Δ|Proposed<br>method|
|---|---|---|---|---|---|
|1|99.07|-0.93|100.0|0|100.00|
|2|97.17|-2.79|100.0|0.04|99.96|
|4|99.78|-0.22|98.30|-1.7|100.00|
|5|98.55|-1.29|100.00|0.16|99.84|
|6|100.00|0.06|100.00|0.06|99.94|
|7|100.00|0|100.00|0|100.00|
|8|96.06|-3.18|96.35|-2.89|99.24|
|10|85.65|-11.79|93.38|-4.06|97.44|
|11|79.26|-20.62|99.78|-0.1|99.88|
|12|96.09|3.51|98.84|6.26|92.58|
|13|89.79|-4.57|95.43|1.07|94.36|
|14|96.58|-3.42|100.00|0|100.00|
|16|82.67|-16.71|96.39|-2.99|99.38|
|17|89.68|-9.54|95.49|-3.73|99.22|
|18|91.18|-4.54|92.94|-2.78|95.72|
|19|90.76|-9.12|99.77|-0.11|99.88|
|20|73.81|-24.35|95.18|-2.98|98.16|
|Average|92.12|2<br>**-6.44**|<br>97.76|**-0.81**|98.56|



25 

# **6 CONCLUSION** 

In this paper, a new fault detection model named TDLN-trees is proposed for the chemical production process. It integrates the strengths of deep learning and m <mark>achine learning techniques, and combines the advantages of BLSTM, LSTM, FCNN, and ET. First, the BLSTM layer in DL comprehensively analy es the dynamic characteristics of time series data, the LSTM layer precisely identifies and captures the instantaneous changes in the data, while the FCNN layer enhances the understanding of higher-level data. Second, the ET in ML calculates the Gini index for node segmentation and reali es fault classification. In the experimental demonstration based on TEP, TDLN-trees was compared with other state-of-the-art methods and demonstrated superior performance, achieving a 98.56% FDR, surpassing that of the other methods. Ablation experiments also confirm the effectiveness of the proposed method for fault detection in chemical production. TDLN-trees have been demonstrated for TEP, and the subsequent research will involve integrating it into the mineral extraction process and developing an interpretable model that can elucidate the causes of faults.</mark> 

# **CKNO L  G M NT** 

<mark>This work is supported by the National Natural Science Foundation of China (62203164, 62373144), Scientific Research Fund of Hunan Provincial Education Department (Outstanding Young Project) (21B0499), Hunan Provincial Department of Education (Project No. 22A0349).</mark> 

# **F   NC** 

- [1] M. <mark>Sajid,  . Płotka-Wasylka, Talanta.</mark> **<mark>2022</mark>** <mark>, 238, 123046.</mark> 

- [2] <mark>X. Bi, R. Qin, D. Wu, S. Zheng,  . Zhao, Comput. Chem. Eng.</mark> **<mark>2022</mark>** <mark>, 164, 107884.</mark> 

- [3] V. Hessel, N. N. Tran, M. R. Asrami, Q. D. Tran, N. V. D. Long, M. EscribÀ-Gelonch,  . 

   - O. Tejada, S. Linke, K. Sundmacher, <mark>Green Chem.</mark> **<mark>2022</mark>** <mark>, 24(2): 410-437.</mark> 

- [4] <mark>M. T. Amin, S. Imtia , F. Khan, Chem. Eng. Sci.</mark> **<mark>2018</mark>** <mark>, 189: 191-211.</mark> 

- [5] L. Ming,  . S. Zhao, International Symposium on Advanced Control of Industrial Processes IEEE. Taipei, China, May **2017** . 

- [6] K. Zhang, B.  iang, P. Shi, IET Control Theory & Applications. **2009** , 3(2): 189-199. 

- [7] P. Li, V. Kadirkamanathan, IEEE Trans. Syst. Man Cybern. Part C Appl. Rev. **2001** , 31(3): 337-343. 

26 

- [8] M. Dong, C. Liu, G. Y. Li, IEEE Trans. Control Syst. Technol. **2010** , 18(2): 510-515. 

- [9] <mark>P.  ieyang, A. Kimmig, W. Dongkun, Z. Niu, F. Zhi, W.  iahai, X. Liu.  . Ovtcharova,  . Intell. Manuf.</mark> **<mark>2023</mark>** <mark>, 34(8): 3277-3304.</mark> 

- [10] N. Nor. Md, R. C. Hassan. Che, A. M. Hussain, Rev. Chem. Eng. **2020** , 36(4): 513-553. 

- [11] R. Dunia, S.  . Qin, T. F. Edgar, T.  . McAvoy, AlChE  . **1996** , 42(10): 2797-2812. 

- [12] B. Alakent, Can   Chem Eng. **2023** , 101(5): 2768-2789. 

- [13] C. Botre, M. Mansouri, M. Nounou, H. Nounou, N. M. Karim,  . Loss Prev. Process Ind. **2016** , 43: 212-224. 

- [14] <mark>B. Schölkopf, A. Smola, K. R. Müller, Neural Comput.</mark> **<mark>1998</mark>** <mark>, 10(5): 1299-1319.</mark> 

- [15] <mark>M. Meuwly, Chem. Rev.</mark> **<mark>2021</mark>** <mark>, 121(16): 10218-10239.</mark> 

- [16] S. Mahadevan, S. L. Shah,  . Process. Contr. **2009** , 19(10): 1627-1639. 

- [17] A. Roy, S. Chakraborty, Reliab. Eng. Syst. Saf. **2023** : 109126. 

- [18] F. Zhang,  . Zhang,  . Ma,   Intell Manuf. **2023** , 34(7): 3159-3177. 

- [19] <mark>P. Geurts, D. Ernst, L. Wehenkel, Mach Learn. 2006, 63: 3-42.</mark> 

- [20] <mark>M. Arya, G. H. Sastry, A. Motwani, S. Kumar, A. Zaguia, Front. Public Health,</mark> **<mark>2022</mark>** <mark>, 9: 797877.</mark> 

- [21] Y. Sina, Y. Shen, A. M. Gibran, IEEE Open  . Ind. Electron. Soc. **2023** . 

- [22] <mark>Y. Lei, B. Yang, X.  iang, F.  ia, N. Li, A. K. Nandi, Mech. Syst. Signal Process.</mark> **<mark>2020</mark>** <mark>, 138: 106587.</mark> 

- [23] Z. <mark>Ren, W. Zhang, Z. Zhang, IEEE Trans. Ind. Inf.</mark> **<mark>2019</mark>** <mark>, 16(8): 5042-5052.</mark> 

- [24] <mark>L. Wen, X. Li, L. Gao, Y. Zhang, IEEE Trans. Ind. Electron.</mark> **<mark>2017</mark>** <mark>, 65(7): 5990-5998.</mark> 

- [25] <mark>X. Yuan, Y. Wang, C. Wang, L. Ye, K. Wang, Y. Wang, C. Yang, W. Gui, F. Shen, IEEE Trans. Instrum. Meas.</mark> **<mark>2024</mark>** <mark>.</mark> 

- [26] S. S. Roy, S. Chatterjee, S. Roy, P. Bamane, A. Paramane, U. M. Rao, M. T. Na ir, <mark>IEEE Trans. Ind. Appl.</mark> **<mark>2022</mark>** <mark>, 58(4): 4542-4551.</mark> 

- [27] <mark>S. Zhang, T. Qiu, Chem. Eng. Sci.</mark> **<mark>2022</mark>** <mark>, 251: 117467.</mark> 

- [28] <mark>Y. Han, N. Ding, Z. Geng, Z. Wang, C. Chu,  . Process Control.</mark> **<mark>2020</mark>** <mark>, 92: 161-168.</mark> 

- [29] <mark>X. Yuan, N. Xu, L. Ye, K. Wang, F. Shen, Y. Wang, C. Yang, W. Gui, IEEE Trans. Ind. Inf.</mark> **<mark>2023</mark>** <mark>.</mark> 

- [30] <mark>D. E. Rumelhart, G. E. Hinton, R.  . Williams, nature.</mark> **<mark>1986</mark>** <mark>, 323(6088): 533-536.</mark> 

27 

- [31] <mark>A. Sherstinsky, Phys. D.</mark> **<mark>2020</mark>** <mark>, 404: 132306.</mark> 

- [32] <mark>G. Van Houdt, C. Mosquera, G. Nápoles, Artif. Intell. Rev.</mark> **<mark>2020</mark>** <mark>, 53: 5929-5955.</mark> 

- [33] <mark>M.W. Ahmad,  . Reynolds, Y. Re gui,  . Cleaner Prod.</mark> **<mark>2018</mark>** <mark>, 203: 810-821.</mark> 

- [34] <mark>Q. W. Wu, R. F. Cao,  . F. Xia,  . C. Ni, C. H. Zheng, Y. S. Su, IEEE/ACM Trans. Comput. Biol. Bioinf.</mark> **<mark>2021</mark>** <mark>, 19(6): 3171-3178.</mark> 

- [35] H. Pu,  . Liu, Z. Chen, X. Yang, C. Ren, Z. Xu, Y.  ian, International Conference on Computing, Control and Industrial Engineering. Singapore, February **2023** . 

- [36] Y. Ma, H. Shi, S. Tan, Y. Tao, B. Song, IEEE Trans. Instrum. Meas. 2022, 71: 1-15. 

- [37] N. L. <mark>Ricker,  . Process Control.</mark> **<mark>1996</mark>** <mark>, 6(4): 205-221.</mark> 

- [38] I. <mark>Lomov, M. Lyubimov, I. Makarov, L. E. Zhukov,  . Ind. Inf. Integr.</mark> **<mark>2021</mark>** <mark>, 23: 100216.</mark> 

- [39] P. R. <mark>Lyman, C. Georgakis, Comput. Chem. Eng.</mark> **<mark>1995</mark>** <mark>, 19(3): 321-331.</mark> 

- [40] L. <mark>Zhang, Z. Song, Q. Zhang, Z. Peng, Neural Comput. Appl.</mark> **<mark>2022</mark>** <mark>, 34(11): 8575-8585.</mark> 

- [41] <mark>. Liu,  . Wang, X. Liu, T. Ma, Z. Tang,  . Intell. Manuf.</mark> **<mark>2022</mark>** <mark>: 1-17.</mark> 

- [42] <mark>S. Wang, Q. Zhao, Y. Han,  . Wang, IEEE Trans. Instrum. Meas.</mark> **<mark>2023</mark>** <mark>.</mark> 

- [43] <mark>Y. Zhang, S. Zhang, X.  ia, X. Zhang, W. Tian,  . Taiwan Inst. Chem. Eng.</mark> **<mark>2023</mark>** <mark>, 142: 104676.</mark> 

- [44] B. <mark>Liu, Y. Chai, Y. Liu, C. Huang, Y. Wang, Q. Tang,  . Process Control.</mark> **<mark>2021</mark>** <mark>, 102: 54-65.</mark> 

- [45] Z. <mark>Wei, X.  i, L. Zhou, Y. Dang, Y. Dai, Process Saf. Environ. Prot.</mark> **<mark>2022</mark>** <mark>, 167: 480-492.</mark> 

- [46] L. <mark>Qi, Y. Ren, Y. Fang,  . Zhou, Neural Comput. Appl.</mark> **<mark>2023</mark>** <mark>, 35(29): 22007-22026.</mark> 

28 

