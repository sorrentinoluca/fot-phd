IEEE SENSORS JOURNAL, VOL. 23, NO. 23, 1 DECEMBER 2023 

29293 

# Multichannel Dynamic Graph Convolutional Network-Based Fault Diagnosis and Its Application in Blast Furnace Ironmaking Process 

Ping Wu , Yixuan Wang , Jinfeng Gao, Xujie Zhang , Siwei Lou , and Chunjie Yang , _Senior Member, IEEE_ 


![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0001-04.png)


**_Abstract_ —To ensure the operation safety of complex industrial processes, faults that occur in the process should be detected and identified in time to avoid further catastrophic events. Therefore, fault diagnosis plays an indispensable role in the process industry. With the expansion of the production scale of industrial processes, the structural attributed graph is suitable for describing the process data structure due to the complicated interactions between sensor measurements. Graph convolutional networks (GCNs) can identify and capture the relationships between industrial process data in non-Euclidean space by taking graph data with** 

**topological structure as input. In this article, a novel fault diagnosis method based on a multichannel dynamic GCN (MDGCN) is proposed. Different from traditional GCNs, the proposed MDGCN assigns different weights to the nodes of the graph. Thus, more useful information about process dynamics is extracted. Particularly, the strategy of multiple isomorphic graph channels is developed to learn feature representations of process data from different levels for fault diagnosis. The capability and efficiency of the proposed MDGCN-based fault diagnosis method are demonstrated through an industrial benchmark of the Tennessee Eastman process (TEP) and a real blast furnace iron-making process (BFIP).** 

**_Index Terms_ — Blast furnace ironmaking process, fault diagnosis, graph convolutional networks (GCNs), multiple isomorphic graph channels.** 

## I. INTRODUCTION 

HE modern process industry has become more complex **T** and integrated. With the stringent requirements for product quality and operation safety, fault diagnosis plays a pivotal role in complex industrial processes [1]. 

Roughly, fault diagnosis methods can be divided into three classes: analytic model-based, expert knowledge-based, and 

Manuscript received 21 September 2023; accepted 11 October 2023. Date of publication 23 October 2023; date of current version 30 November 2023. This work was supported in part by the National Natural Science Foundation of China under Grant 61703371 and Grant 62073296; in part by the Open Research Project of the State Key Laboratory of Industrial Control Technology, Zhejiang University, China, under Grant ICT2023B19; and in part by the Zhejiang Province Public Welfare Technology Application Research Project under Grant LGF19F030004 and Grant LGG21F030015. The associate editor coordinating the review of this article and approving it for publication was Dr. Ke Feng. _(Corresponding author: Ping Wu.)_ 

Ping Wu, Yixuan Wang, and Jinfeng Gao are with the School of Information Science and Engineering, Zhejiang Sci-Tech University, Hangzhou 310018, China (e-mail: pingwu@zstu.edu.cn; 202120604131@mails.zstu.edu.cn; jfgao@zstu.edu.cn). 

Xujie Zhang, Siwei Lou, and Chunjie Yang are with the College of Control Science and Engineering, Zhejiang University, Hangzhou 310027, China (e-mail: xujie_zhang@zju.edu.cn; swlou@zju.edu.cn; cjyang999@zju.edu.cn). 

Digital Object Identifier 10.1109/JSEN.2023.3325353 

data-driven based methods [2]. Analytic model-based methods can provide an insightful and sophisticated understanding of the processes. However, the success of model-based methods crucially depends on the establishment of accurate mathematical models [3]. It is very difficult and cumbersome to build accurate mathematical models for complex industrial processes. Expert knowledge-based methods rely heavily on empirical knowledge, which requires long-term available and accurate fault information. On the other hand, data-driven methods construct fault diagnosis models directly from collected historical process data [4]. With the advance of sensor, storage, and computing technologies, data-driven fault diagnosis methods have gathered tremendous attention from academia and industry in recent years [5]. 

In past decades, traditional statistical learning and machine-learning methods such as Fisher discriminant analysis (FDA), support vector machines (SVMs), the k-nearest neighbor (KNN), and random forest (RF) have been widely used in fault diagnosis methods. However, these methods only extract shallow features from process data. The traditional statistical learning and machine-learning methods are gradually not competent for modeling increasingly complex processes [6]. On the contrary, deep-learning methods can learn deep 

1558-1748 © 2023 IEEE. Personal use is permitted, but republication/redistribution requires IEEE permission. See https://www.ieee.org/publications/rights/index.html for more information. 

Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on September 11,2026 at 16:19:03 UTC from IEEE Xplore.  Restrictions apply. 

IEEE SENSORS JOURNAL, VOL. 23, NO. 23, 1 DECEMBER 2023 

29294 

features to represent the comprehensive characteristics of process data from deep network structures for addressing complicated tasks [7]. 

Recently, deep-learning algorithms such as deep belief networks (DBNs), autoencoders (AEs), recurrent neural networks (RNNs), and convolutional neural networks (CNNs) have drawn a lot of attention in fault diagnosis. A DBN is a sophisticated generative model that employs a deep architecture usually by stacking restricted Boltzmann machines. Wang et al. [8] used the restricted Boltzmann machine to fully exploit useful information in the process data and proposed an extended DBN for feature extraction and fault diagnosis. Yu and Yan [9] analyzed the unstable neurons in hidden layers caused by the occurred faults in DBNs for process monitoring. An AE is a typical unsupervised neural network that provides good dimensionality reduction performance by compressing the original input to a low-dimensional feature space. Liu et al. [10] used stacked sparse-denoising AEs with a Softmax classifier to develop an end-to-end fault diagnosis scheme. Jang et al. [11] combined variational AEs and generative adversarial networks to generate features that follow the prior distribution to improve the stability and reliability of fault detection. An RNN is a neural network that contains a feedback mechanism to form a closed-loop structure in the hidden layers. As a classical RNN, long short-term memory (LSTM) networks can avoid vanishing or exploding gradients by introducing “gates.” Han et al. [12] proposed an LSTM-based for fault detection of shipboard vessel components. Peng et al. [13] combined the LSTM model and the causal inference method for solid oxide fuel cell fault diagnosis. Han et al. [14] proposed a fault detection model by determining the optimal number of hidden layer nodes using the iterative method. Inspired by the natural visual perception mechanism, the CNN uses convolutional layers to learn spatial hierarchies of features adaptively. Zhi et al. [15] proposed a CNN-based model that can mine hidden features from processed sensor data to correctly identify faults. Wu and Zhao [16] developed a chemical process fault diagnosis method based on a classical deep CNN (DCNN) model which is composed of convolutional layers, pooling layers, dropout, and fully connected layers. Jiang et al. [17] incorporated a multiscale learning strategy into the traditional CNN architecture to learn high-level fault features at different scales. Xie et al. [18] transformed multiple signal data into three-channel red–green–blue images and then proposed an improved CNN with residual networks for fault diagnosis. However, the CNN only addresses the Euclidean-adjacent feature extraction in the spatial domain. Valuable feature information would be lost by the CNN aggregation approach [19]. 

For industrial processes such as chemical processes and iron-making processes, the structural attributed graph is suitable for describing the process data structure, since the complicated interactions between sensor measurements exist [20]. Through graph theory, graph neural networks (GNNs) can process data in the graph domain [21]. Among the GNN models, graph convolutional network (GCN) models can make use of the graph structure and aggregate node information from the neighborhoods in a convolutional fashion [22]. Thus, GCNs offer high expressive power for learning 

graph representations in a wide range of tasks and applications [23]. Zhao et al. [24] developed a graph convolution DBN for semisupervised fault diagnosis. Chen et al. [25] combined CNNs, GCNs, and attention mechanisms to handle the diversity of working conditions and the lack of sufficient fault samples in fault diagnosis. Sun et al. [26] developed multiscale graph convolution neural networks for machine fault diagnosis. Feng et al. [27] developed a digital twin-enabled domain adversarial graph network for bearing fault diagnosis, where the digital twin model was employed for conducting the dynamic simulation of the bearings. Xu et al. [28] developed a graph-guided CNN model and graph reasoning fusion module to explore the inherent correlations between multisource signals for fault diagnosis of electromechanical systems. Yang et al. [29] combined a GCN model with a gate recurrent unit for the remaining useful life prediction of rolling bearings. Chen et al. [30] used GCN and gated CNN as the associative module and temporal module to integrate the association information and the temporal domain information for providing accurate cooling load prediction. Wu and Zhao [31] integrated the process topology into the GCN model through a transformed graph for fault diagnosis. 

Although GCN methods have been successfully applied in fault diagnosis, there is still room for further improvements. First, the conventional GCN models aggregate the information in the temporal domain where the feature weights are the same at different time nodes. However, the dynamic characteristic is inherent in industrial processes [32]. The process data is autocorrelated and cross-correlated. Thus, it would be unreasonable to assign the same feature weights at different time nodes. Second, the GCN can exert a low-pass filtering effect. Yet, improperly increasing the layers of the GCN can exacerbate the smoothing effect of the network [33]. To address these issues, dynamic weights assignment and multiple isomorphic graph channels are developed to enhance the capability of representation learning for fault diagnosis. To deal with these issues, a novel fault diagnosis method based on the multichannel dynamic GCN (MDGCN) is proposed in this work. In the proposed MDGCN, the graph is first constructed using the process topology and knowledge. Next, the Euclidean distance between different sampled process data is calculated and normalized by softmax. These distances are presented as weights to extract the dynamics characteristics of process data. More importantly, the strategy of multiple isomorphic graph channels is employed to construct a multichannel GCN model to learn features from different levels. Finally, a softmax classifier is employed for fault diagnosis. 

The main contributions of this work are briefly summarized as follows. 

- 1) Time nodes are assigned different weights to aggregate the dynamic information in process data. Through the assignment of different weights at different time nodes, the process dynamics characteristic is further extracted. 

- 2) Multiple isomorphic graph channels are integrated into the GNN. Different level features are learned from the constructed graph. By employing multiple isomorphic graph channels, more useful information on process data is explored. 

Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on September 11,2026 at 16:19:03 UTC from IEEE Xplore.  Restrictions apply. 

WU et al.: MDGCN-BASED FAULT DIAGNOSIS AND ITS APPLICATION IN BLAST FURNACE IRONMAKING PROCESS 

29295 


![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0003-02.png)


Fig. 1. Spatial-based graph convolutional operation. 

- 3) A new fault diagnosis scheme is developed by using the proposed MDGCN and softmax classifier. The superior performance of the proposed MDGCN-based fault diagnosis method is demonstrated by case studies on the industrial benchmark of the Tennessee Eastman process (TEP) and a real blast furnace iron-making process (BFIP), compared to other related methods. 

The rest of this article is structured as follows. Section II offers a brief review of the GCN. Section III describes the proposed MDGCN method in detail. In Section IV, the industrial benchmark of TEP and a real BFIP are employed to verify the proposed MDGCN-based fault diagnosis method in comparison with other related methods. Finally, the conclusions are drawn in Section V. 

## II. REVIEW OF THE GCN 

In the GCN, the data is represented as graphs to encode the structural information for modeling the relations among entities. Among different graph construction methods, the local outlier method (LOM) is widely employed [34]. In LOM, the distance of all nodes is calculated to determine the degree of correlation between nodes. Then, the nodes with the closest _k_ Euclidean distances are connected by edges. Specifically, kNN is the most commonly used LOM method in graph construction. kNN is a purely data-driven approach. However, it lacks interpretability. To address this problem, Wu and Zhao [31] integrated process knowledge or topology in graph construction. 

GCNs can be considered an efficient variant of CNNs. The virtue of GCNs is that they can aggregate the features of the adjacent nodes in the graph domain. Fig. 1 shows that the GCN can pass information through the edges and aggregate features from neighboring nodes to the central node to update the node state. In GCNs, specific information transfer and aggregation operations are performed by the convolutional layer. 

For a given graph _G_ = _(V, E,_ **A** _)_ , where _V_ is the set of nodes and _E_ is the set of edges. _vi_ ∈ _V_ denotes the nodes and _ei j_ ∈ _E_ denotes the edges from _vi_ to _v j_ . The adjacency matrix **A** is an _n_ × _n_ matrix with **A** _i j_ = 1 if _ei j_ ∈ _E_ and **A** _i j_ = 0 if _ei j_ ∈ _/ E_ [35]. Generally, the information of neighbor nodes around central nodes is required to aggregate. Self-directed 

edges are added for constructing graphs. It obtains 


![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0003-11.png)


Here, **I** _n_ is an identity matrix.<sup>�</sup> **A** is the adjacency matrix after adding the self-directed edges.<sup>�</sup> **D** = diag _(_<sup>�</sup> **D** _ii )_ is the degree matrix with self-directed edges. The spatial-based convolutional operation is formulated 


![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0003-13.png)


where **X**<sup>_(l)_</sup> is the output of layer _l_ and **X**<sup>_(l_+1</sup><sup>_)_</sup> is the output of layer _l_ + 1. **W**<sup>_(l)_</sup> is the weight of the layer _l_ and _σ(_ · _)_ is the activation function. Through the graph constructed from physical relationships between variables, the process knowledge is included by the adjacency matrix and degree matrix. In addition, the adjacency matrix does not undergo dynamic updates. 

## III. PROPOSED MDGCN-BASED FAULT DIAGNOSIS SCHEME 

## _A. Dynamic Weights Calculation_ 

Existing GCN models often employ the same weights to capture nodes’ structural information, where the weights attached to the data matrix of the current time instant are assumed to be the same as the past period. However, the local structure and dynamic information of process data would be lost. In this work, the weights are dynamically computed through Euclidean-based distance. 

_T_ The training data **X** = � **x** 1 **x** 2 · · · **x** _N_ � that consists of _N_ observations are collected and normalized. Each observation contains _m_ process variables. Denote the data matrix at time instant _t_ as **X** _t_ ∈ R<sup>_s_×</sup><sup>_m_</sup> 


![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0003-19.png)


where _s_ is the number of time lags. 

For generality, the calculated Euclidean-based distance is normalized by the Softmax function. Within **X** _t_ , the Euclidean distance between **x** _i_ and **x** _j_ is defined 


![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0003-22.png)


Then, the weight matrix **M** = [ _mi j_ ] ∈ R<sup>_s_×</sup><sup>_s_</sup> is defined as 


![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0003-24.png)


where _d_<sup>�</sup> _i j_ = − _(di j /d)_ . _d_ is the mean of _di j_ . 

The relationship between observations **X** _t_ is explored through the defined weight matrix **M** . Thus, the dynamic characteristic of the process is captured. The matrix **M** is used to extract the dynamics of the process data using all the training data at the initialization phase. With the calculated weight matrix **M** , **X** _t_ is updated as **X** _t,d_ 


![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0003-27.png)


Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on September 11,2026 at 16:19:03 UTC from IEEE Xplore.  Restrictions apply. 

IEEE SENSORS JOURNAL, VOL. 23, NO. 23, 1 DECEMBER 2023 

29296 

It should be noted that there are some abstract nodes such as unit nodes in graph _G_ . These abstract nodes have no actual measured value. By denoting **O** ∈ R<sup>_s_×</sup><sup>_p_</sup> as a matrix where all elements are set as 0 and _p_ is the number of abstract nodes, the abstract node features are initialized as **O** . By concatenating the dynamic data matrix **X** _t,d_ with the abstract node features **O** in horizontal manner, it obtains the feature matrix **X** _f,t_ 


![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0004-03.png)


Each feature matrix at instant _t_ will be assigned a label _yt_ ∈ Z varying from 0 to _c_ that denotes different process status. 

## _B. Multichannel Dynamic GCN Model_ 

GCNs can act as the function of low-pass filtering. As the number of GCN model layers increases, the smoothing effect of the networks becomes more pronounced [35]. To enhance the ability of representation learning without increasing more layers, the multiple isomorphic graph channels strategy is employed in the work. The architecture of the proposed MDGCN is plotted in Fig. 2. As shown in Fig. 2, information from each node is propagated along topological connections between different units of the complex industrial process. Meanwhile, multiple isomorphic graph channels are employed to enhance the model’s ability to learn different representations of the deeper features. Specifically, multiple convolutional kernels are used in this work. 

The corresponding degree matrix<sup>�</sup> **D** and the adjacency matrix<sup>�</sup> **A** are calculated by (1) and (2). It is worth mentioning that<sup>�</sup> **A** is symmetric because the constructed graph _G_ is an undirected graph. For multichannel learning, the model with _L_ graph convolution layers and _q_ filters is initialized, then 


![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0004-08.png)


where _l_ = 1 _, . . . , L_ , **X**<sup>_(_</sup> _t_<sup>_l_</sup> _, f_<sup>−</sup> _,_<sup>1</sup> _j_<sup>_)_istheinputfeatureofthe</sup><sup>_(l_−1</sup><sup>_)_th</sup> graph convolutional layer, and **X**<sup>_(_</sup> _t_<sup>_l_</sup> _, f_<sup>_)_</sup> _, j_<sup>istheoutputfeatureof</sup> the _(l)_ th graph convolutional layer for the _j_ th filter at time instant _t_ . **W**<sup>_(_</sup> _t_<sup>_l_</sup> _, j_<sup>_)_∈R</sup><sup>_s_×</sup><sup>_b_isthecorrespondingweightmatrix</sup> and _b_ is embedded feature dimension. ReLU _(_ · _)_ represents the Rectified Linear Unit (ReLU) activation function. Deep representations **h** _j , j_ = 1 _, . . . , q_ are extracted from _l_ graph convolution layers 


![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0004-10.png)


Moreover, the individual flattened features are stacked into **H** as 


![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0004-12.png)


Then, **H** is fed into the multilayer perceptron (MLP) with _K_ layers, and **z**<sup>_K_</sup> is the output of the _K_ th layer. 


![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0004-14.png)



![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0004-15.png)


A fault diagnosis task can be accomplished as a classification task. To do so, a Softmax layer is employed after the _k_ th full connection layer 


![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0004-17.png)


**Algorithm 1** MDGCN Training Procedure 

**Input:** Training dataset { **X** _t , yt_ } _t_<sup>_N_</sup> =1<sup>,andtheinitialized</sup> parameters **W**<sup>0</sup> _,_ **w**<sup>0</sup> _,_ **b**<sup>0</sup> _,_ **M** . 

**Output:** The weight matrix **W**<sup>_L_</sup> _,_ **w**<sup>_N_</sup> _,_ **b**<sup>_N_</sup> . 

- **1 for** _epoch_ = 1 _, . . . , epochmax_ **do 2 for** _n_ = 1 _, . . . , N_ **do 3** Calculate the output of convolutional layer **X**<sup>_(_</sup> _f_<sup>_l_</sup> _,_<sup>_)_</sup> _j_ by (9); 

- **4** Flatten the output of multi-channels into **H** by (11)(12); 

- **5** Feed **H** into the MLP by (13) to obtain the output **z**<sup>_k_</sup> ; 

- **6** Convert **z**<sup>_k_</sup> into a probability value vector **p** by (14); 

- **7 end** 

- **8** Compute the loss function by (15) and optimize the parameters with Adam until **W**<sup>_l_</sup> _,_ **w**<sup>_k_</sup> _,_ **b**<sup>_k_</sup> converge; 

- **9 end** 

The commonly used cross-entropy loss function is adopted 


![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0004-29.png)


In this work, the model parameters are learned using the Adam optimizer. Moreover, the widely used dropout technique is used to avoid overfitting. The training procedure of the proposed MDGCN model is illustrated in Algorithm 1. 

## _C. Fault Diagnosis Scheme Based on MDGCN_ 

The proposed MDGCN-based fault diagnosis scheme consists of two phases, the offline modeling phase, and the online diagnosis phase. The MDGCN-based fault diagnosis scheme is depicted in Fig. 3. 

The proposed MDGCN-based fault diagnosis scheme can be summarized as follows. 

## 1) _Offline Training Phase:_ 

- a) _Step1:_ Collect and normalize the training data. Construct the graph _G_ following the process topology and calculate the adjacency matrix **A** . 

- b) _Step2:_ Calculate the weight matrix **M** to adjust the data matrix **X** _t,d_ , according to the correlations. 

- c) _Step3:_ Construct the data matrix **X** _t, f_ corresponding to their labels _yt_ . 

- d) _Step4:_ Train the MDGCN model using the Adam optimizer and dropout strategy. 

## 2) _Online Monitoring Phase:_ 

- a) _Step1:_ Collect and normalize real-time samples. 

- b) _Step2:_ Reconstruct the new data matrix similar to the offline modeling phase. 

- c) _Step3:_ Update the data matrix using the graph _G_ and adjacency matrix **A** and then feed the data matrix into the trained MDGCN model for prediction. 

- d) _Step4:_ Determine the faulty type according to the output of the MDGCN. 

Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on September 11,2026 at 16:19:03 UTC from IEEE Xplore.  Restrictions apply. 

WU et al.: MDGCN-BASED FAULT DIAGNOSIS AND ITS APPLICATION IN BLAST FURNACE IRONMAKING PROCESS 

29297 


![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0005-02.png)


Fig. 2. Architecture of the proposed MDGCN model. 


![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0005-04.png)


Fig. 3. Framework of fault diagnosis program based on MDGCN. 


![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0005-06.png)


Fig. 4. Established graph of TEP. 

## IV. EXPERIMENTS AND RESULTS 

To validate the performance of the proposed MDGCN-based fault diagnosis scheme, experiments on the widely used TEP benchmark and a real blast furnace ironmaking process are carried out. For comparison study, traditional machine-learning methods such as SVM, RF, and deep-learning methods such as DCNN [36], kNN-based GCN (k-GCN) [35], and PTCN [31] are employed. All methods are implemented in a Python 3.8 environment using open-source libraries such as PyTorch and sklearn. For PTCN and MDGCN, the DGL package is also used. The working environment is Windows 10, the GPU is GeForce GTX 1080, and the CPU is Intel<sup>1</sup> Xeon<sup>1</sup> Bronze 3104. 

## _A. TEP Benchmark Case_ 

The TEP is a widely used benchmark that was developed based on an actual chemical process, for evaluating the performance of process monitoring and fault diagnosis. The TEP consists of five operating units, a reactor, 

### 1Registered trademark. 

a condenser, a vapor–liquid separator, a recycle compressor, and a product stripper. The process contains 12 manipulated variables (XMV1-12) and 41 measured variables (XMEAS141) with a sampling period of three minutes. In this work, 52 variables (XMV(12) excluded) are employed. 21 different fault scenarios (Faults 1–21) were simulated. In this work, a total of 18 fault types excluding faults 3, 9, and 15 are selected for comparative study. More details about the TEP can be found in [37]. In this work, the benchmark data found in http://web.mit.edu/braatzgroup/links.html are used. The dataset includes 3380 samples and 800 samples for each type of fault. The datasets are divided into 70% of the training set and 30% of the test set. The graph of TEP _G_<sup>TE</sup> is established using the method introduced in Section II. In _G_<sup>TE</sup> , there are 82 nodes and 111 edges. Fig. 4 displays the diagram of _G_<sup>TE</sup> . 

To evaluate the fault diagnosis performance, two indices including fault diagnosis rate (FDR) and accurate classification rate (ACR) are used [31]. The FDR and ACR are defined 

Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on September 11,2026 at 16:19:03 UTC from IEEE Xplore.  Restrictions apply. 

IEEE SENSORS JOURNAL, VOL. 23, NO. 23, 1 DECEMBER 2023 

29298 

TABLE I 

ACR RESULTS WITH DIFFERENT LAYERS 

### TABLE II 

ACR OF MDGCN WITH DIFFERENT CHANNELS 

### TABLE III 

STRUCTURE OF THE MULTICHANNEL GCN ON TEP 


![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0006-08.png)


below 


![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0006-10.png)


where _nc_ denotes the total number of test samples for class _c_ , and _nct_ denotes the number of correctly classified class _c_ samples. The ACR represents comprehensive classification accuracy. A higher ACR indicates that the performance is superior. 

For MDGCN, the time lag is set as 10. It is critical to select the appropriate model structure for deep learning tasks. To obtain a satisfactory structure of the proposed MDGCN model, the number of layers is determined by evaluating the performance of the MDGCN model which does not employ a multichannel strategy. Table I lists the ACRs with different layers. From the data in Table I, it can be found that the best depth should be selected as 4. The increase in the channel number can improve performance, but more channels do not necessarily lead to better results. The reason could be the more templates we use, the more complex our model would be [38]. Thus, the number of channels should be selected appropriately. The selection of the number of channels is according to experience and experiment. The ACRs of MDGCN models with different channels are listed in Table II. As shown in Table II, the best number of channels is 4. 

The architecture of the MDGCN is shown in Table III. Gc _(m)_ represents a convolutional graph layer with a hidden state embedding dimension of _m_ , and FC _(m, n)_ is a fully connected layer with _m_ neurons using a dropout ratio of _n_ . According to the preexperiment, the number of channels of graph convolution is set as 4. Thus, four different deep features are learned simultaneously. All four channels have the same structure. The number of convolution layers for DCNN, PTCN, k-GCN, and MDGCN is set as 4. The number of neighbors for k-GCN is set to 5. These models are trained using the ReLU activation function, cross-entropy loss functions, Adam optimizer, and mini-batches with a size of 128. The learning rate is set as 0.001. 

The diagnostic results are listed in Table IV. As shown in Table IV, although FDRs of normal, faults 1–7 and 18 can reach 90%. However, SVM has a low ACR. Compared to SVM, RF can offer better FDR for scenarios. The ACR of RF 


![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0006-15.png)



![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0006-16.png)



![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0006-17.png)



![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0006-18.png)



![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0006-19.png)



![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0006-20.png)



![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0006-21.png)



![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0006-22.png)



![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0006-23.png)



![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0006-24.png)



![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0006-25.png)



![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0006-26.png)



![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0006-27.png)



![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0006-28.png)



![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0006-29.png)



![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0006-30.png)



![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0006-31.png)



![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0006-32.png)



![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0006-33.png)



![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0006-34.png)



![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0006-35.png)



![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0006-36.png)



![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0006-37.png)



![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0006-38.png)



![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0006-39.png)



![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0006-40.png)



![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0006-41.png)



![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0006-42.png)



![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0006-43.png)



![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0006-44.png)



![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0006-45.png)



![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0006-46.png)



![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0006-47.png)



![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0006-48.png)



![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0006-49.png)



![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0006-50.png)



![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0006-51.png)


Fig. 5. Confusion matrix of the MDGCN-based fault diagnosis. 

is still below 90%. Different from the shallow learning methods, deep-learning methods such as DCNN, k-GCN, PTCN, and MDGCN have dramatically improved performance. Moreover, as shown in Table IV, the ACR of the proposed MDGCN method reaches 98.8% which is the highest among the comparable methods. It is 2.1% higher than DCNN, 3% higher than k-GCN, and 1% better than PTCN. On the other hand, it can be found that the ACRs of PTCN and MDGCN are higher than k-GCN. By introducing process knowledge to construct the graph, both PTCN and MDGCN provide better performance than k-GCN which builds the graph in a data-driven way. 

To further analyze the performance of MDGCN, the confusion matrix is plotted in Fig. 5. In accordance with the data in Table IV, MDGCN correctly classifies almost entirely of samples, except for a small number of normal samples. 

## _B. Real BFIP Case_ 

The BFIP is one of the most complex industrial processes. There are five main subsystems such as blast furnace, feeding, hot air, pulverized coal injection, and exhaust gas treatment to generate molten iron. In the BFIP, raw materials and fuels, hot air, and pulverized coal are fed into the blast furnace from the furnace top and tuyere, respectively. A series of complex physical and chemical reactions happen under high temperatures and pressure. Molten iron is generated from the blast furnace along the tap hole. Since the harsh working conditions, the BFIP often suffers from various abnormal furnace conditions such as channeling, collapse, and hanging [39]. If these abnormalities are not detected and diagnosed timely and accurately, it will cause degradation of the quality of molten iron, even threats to the safety of equipment and personnel. Thus, fault diagnosis is crucial to ensure the operation safety of the BFIP. 

To build the graph of BFIP for fault diagnosis, BFIP can be divided into four main units including the blast furnace main body, the top of the blast furnace, the pulverized coal injection system, and the hot blast system according to the mechanism of the iron-making process, as shown in Fig. 6. 

From the expert knowledge, ten main process measurements are selected for identifying the BFIP working status. Table V describes the selected ten process variables. In this study, data 

Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on September 11,2026 at 16:19:03 UTC from IEEE Xplore.  Restrictions apply. 

WU et al.: MDGCN-BASED FAULT DIAGNOSIS AND ITS APPLICATION IN BLAST FURNACE IRONMAKING PROCESS 

29299 

### TABLE IV 

COMPARISON RESULTS ON TEP 


![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0007-04.png)



![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0007-05.png)


Fig. 6. Divided units of BFIP. 

TABLE V 

### MONITORED VARIABLES FOR THE BFIP FAULT DIAGNOSIS 


![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0007-09.png)


were collected from the #2 BF in Liuzhou Steel Company Ltd., which is the largest working BF in the Guangxi Province of China. Specifically, 4667 samples including 125 collapse samples, 216 furnace temperature rise samples, 1057 channeling samples, 245 furnace temperature down samples, and 3018 normal samples were collected. Following the procedure described in Section II, the graph _G_<sup>BF</sup> is derived as shown in Fig. 7. _G_<sup>BF</sup> consists of 20 nodes and 23 edges. 

According to the experience and validation, the architecture of the MDGCN model is listed in Table VI. For comparison study, SVM, RF, DCNN, and PTCN are employed. For a 


![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0007-12.png)


Fig. 7. Diagram of the BFIP graph. 

TABLE VI 

STRUCTURE OF THE MDGCN MODEL FOR BFIP FAULT DIAGNOSIS 


![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0007-16.png)


### TABLE VII 

TRAINING AND TESTING TIME USED IN THE BFIP 


![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0007-19.png)


fair comparison, the number of convolution layers for DCNN, k-GCN, PTCN, and MDGCN are all four layers. The number of neighbors for k-GCN is set to 2. For MDGCN, the time lag is set as 10. 

Fig. 8 shows the testing ACR with different training epochs. MDGCN has a better coverage rate and higher ACR than DCNN, k-GCN, and PTCN. And the ACR of MDGCN nearly reaches 100%. 

Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on September 11,2026 at 16:19:03 UTC from IEEE Xplore.  Restrictions apply. 

IEEE SENSORS JOURNAL, VOL. 23, NO. 23, 1 DECEMBER 2023 

29300 

### TABLE VIII 

COMPARISON RESULTS ON BFIP 


![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0008-04.png)


### TABLE IX 

RESULTS UNDER NOISE ON BIFP 


![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0008-07.png)


Table VII lists the training and testing time used in the BFIP case. Compared to other methods, the proposed MDGCN model would cost more time in the training phase since it involves the initialization of dynamic weights and the updates of multichannels. From the data in Table VII, it can be found that the training and testing times of the proposed MDGCN are higher than other methods. The training time and testing time of the MDGCN are 18.32 and 0047 s, respectively. However, the computational cost of the proposed MDGCN is at the same level as other methods such as PTCN and k-GCN. In addition, the proposed MDGCN does not require more samples in the training phase. 

Fig. 9. t-SNE visualization of features learned by different models. 

not high, k-GCN without graph topological knowledge works better than CNN. 

To further compare the MDGCN model to other models, Gaussian noise with a mean of 0 and a standard deviation of 0.3 is added to the normalized variables (V1–9). Then, the generated dataset is used to test the robustness of different models. Each model was run 30 times using the randomly generated datasets. The mean and standard deviation of the testing results are listed in Table IX. From the data in Table IX, it can be concluded that the proposed MDGCN can provide the highest ACR and lowest standard deviation. Thus, it indicates that the MDGCN model has good robustness. 

To compare the performance of DCNN, k-GCN, PTCN, and MDGCN, the t-distributed stochastic neighbor embedding (t-SNE) technique is utilized to visualize the learned features. The clusters obtained by t-SNE are plotted in Fig. 9. As shown in Fig. 9, it can be observed that the clusters of the features extracted by MDGCN can be better separated than DCNN, k-GCN, and PTCN. Therefore, the classification accuracy of MDGCN is higher. 

In the proposed MDGCN model, two important improvements are developed, including assigning dynamic weights and employing the strategy of multiple isomorphic graph channels. To illustrate the benefits brought by these improvements, ablation experiments are carried out. To do so, we compare three models such as PTCN, dynamic GCN, and multichannel GCN with the MDGCN model. PTCN only considers the process topology. Dynamic GCN takes the process topology and dynamic weights into account. Multichannel GCN integrates the process topology and employs the strategy of multiple isomorphic graph channels. The proposed MDGCN model takes advantage of the process topology, dynamic weights, 

The diagnostic results are listed in Table VIII. As shown in Table VIII, SVM provides poor fault diagnosis performance, where the ACR is only 71.8%. RF can offer better performance, where the ACR reaches 90.1%. Compared to SVM, RF can efficiently capture the nonlinearity of BF. It can also be observed that deep-learning methods such as DCNN, k-GCN, PTCN, and MDGCN can derive superior performance than shallow learning methods such as SVM and RF. Their ACRs are higher than that of RF. When the data dimension is 

Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on September 11,2026 at 16:19:03 UTC from IEEE Xplore.  Restrictions apply. 

WU et al.: MDGCN-BASED FAULT DIAGNOSIS AND ITS APPLICATION IN BLAST FURNACE IRONMAKING PROCESS 

29301 

TABLE X 

ABLATION EXPERIMENTAL RESULTS OF MDGCN FAULT DIAGNOSIS METHOD ON BFIP 


![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0009-04.png)


and multiple isomorphic graph channels simultaneously. The ablation experimental results are given in Table X. From the data in Table X, it can be found that fault 4 can be correctly identified by assigning dynamic weights to construct the graph. The multichannel convolution operation is also helpful to identify faults 2 and 3. Although the classification accuracy of normal samples is slightly lower than PTCN and dynamic GCN, the overall accuracy of MDGCN is higher. 

## V. CONCLUSION 

In this article, a novel fault diagnosis method based on MDGCN is proposed. The proposed MDGCN incorporates the process topology knowledge and assigns different weights to construct the graph for extracting more useful information. More importantly, multiple isomorphic graph channels are employed to capture the representation of process data from different levels. The effectiveness of the proposed MDGCN is verified through the industrial benchmark of TEP and a real BFIP. Although the proposed MDGCN-based fault diagnosis method offers superior performance over other related methods, there are still some issues that should be addressed in future work. 

- 1) In the proposed MDGCN model, the graph is mainly constructed using process knowledge. To improve the efficiency of graph construction, the data-driven and knowledge-driven methods could be combined in further study. 

- 2) To enhance the ability to extract temporal information, more neural network architectures such as LSTM networks and attention mechanisms can be taken into consideration in the framework of MDGCN in future research. 

- 3) Since the process topology knowledge is fully embedded in the MDGCN model, the root cause analysis could be more accessible. Future work will focus on the root cause analysis using the proposed MDGCN model. 

## REFERENCES 

- [1] K. Severson, P. Chaiwatanodom, and R. D. Braatz, “Perspectives on process monitoring of industrial systems,” _Annu. Rev. Control_ , vol. 42, pp. 190–200, Nov. 2016. 

- [2] K. Tidriri, N. Chatti, S. Verron, and T. Tiplica, “Bridging data-driven and model-based approaches for process fault diagnosis and health monitoring: A review of researches and future challenges,” _Annu. Rev. Control_ , vol. 42, pp. 63–81, Nov. 2016. 

- [3] C. M. Furse, M. Kafal, R. Razzaghi, and Y.-J. Shin, “Fault diagnosis for electrical systems and power networks: A review,” _IEEE Sensors J._ , vol. 21, no. 2, pp. 888–906, Jan. 2021. 

- [4] H. Darvishi, D. Ciuonzo, E. R. Eide, and P. S. Rossi, “Sensorfault detection, isolation and accommodation for digital twins via modular data-driven architecture,” _IEEE Sensors J._ , vol. 21, no. 4, pp. 4827–4838, Feb. 2021. 

- [5] Z. Gao, C. Cecati, and S. X. Ding, “A survey of fault diagnosis and fault-tolerant techniques—Part I: Fault diagnosis with model-based and signal-based approaches,” _IEEE Trans. Ind. Electron._ , vol. 62, no. 6, pp. 3757–3767, Jun. 2015. 

- [6] B. Shen, L. Yao, and Z. Ge, “Nonlinear probabilistic latent variable regression models for soft sensor application: From shallow to deep structure,” _Control Eng. Pract._ , vol. 94, Jan. 2020, Art. no. 104198. 

- [7] X. Kong and Z. Ge, “Deep PLS: A lightweight deep learning model for interpretable and efficient data analytics,” _IEEE Trans. Neural Netw. Learn. Syst._ , early access, Mar. 11, 2022, doi: 10.1109/TNNLS.2022.3154090. 

- [8] Y. Wang, Z. Pan, X. Yuan, C. Yang, and W. Gui, “A novel deep learning based fault diagnosis approach for chemical process with extended deep belief network,” _ISA Trans._ , vol. 96, pp. 457–467, Jan. 2020. 

- [9] J. Yu and X. Yan, “Whole process monitoring based on unstable neuron output information in hidden layers of deep belief network,” _IEEE Trans. Cybern._ , vol. 50, no. 9, pp. 3998–4007, Sep. 2020. 

- [10] J. Liu et al., “Toward robust fault identification of complex industrial processes using stacked sparse-denoising autoencoder with softmax classifier,” _IEEE Trans. Cybern._ , vol. 53, no. 1, pp. 428–442, Jan. 2023. 

- [11] K. Jang, S. Hong, M. Kim, J. Na, and I. Moon, “Adversarial autoencoder based feature learning for fault detection in industrial processes,” _IEEE Trans. Ind. Informat._ , vol. 18, no. 2, pp. 827–834, Feb. 2022. 

- [12] P. Han, A. L. Ellefsen, G. Li, F. T. Holmeset, and H. Zhang, “Fault detection with LSTM-based variational autoencoder for maritime components,” _IEEE Sensors J._ , vol. 21, no. 19, pp. 21903–21912, Oct. 2021. 

- [13] J. Peng, J. Huang, C. Jiang, Y.-W. Xu, X.-L. Wu, and X. Li, “Generalized spatial–temporal fault location method for solid oxide fuel cells using LSTM and causal inference,” _IEEE Trans. Transp. Electrific._ , vol. 8, no. 4, pp. 4583–4594, Dec. 2022. 

- [14] Y. Han, N. Ding, Z. Geng, Z. Wang, and C. Chu, “An optimized long short-term memory network based fault diagnosis model for chemical processes,” _J. Process Control_ , vol. 92, pp. 161–168, Aug. 2020. 

- [15] Z. Zhi, L. Liu, D. Liu, and C. Hu, “Fault detection of the harmonic reducer based on CNN-LSTM with a novel denoising algorithm,” _IEEE Sensors J._ , vol. 22, no. 3, pp. 2572–2581, Feb. 2022. 

- [16] H. Wu and J. Zhao, “Deep convolutional neural network model based chemical process fault diagnosis,” _Comput. Chem. Eng._ , vol. 115, pp. 185–197, Jul. 2018. 

- [17] G. Jiang, H. He, J. Yan, and P. Xie, “Multiscale convolutional neural networks for fault diagnosis of wind turbine gearbox,” _IEEE Trans. Ind. Electron._ , vol. 66, no. 4, pp. 3196–3207, Apr. 2019. 

- [18] T. Xie, X. Huang, and S.-K. Choi, “Intelligent mechanical fault diagnosis using multisensor fusion and convolution neural network,” _IEEE Trans. Ind. Informat._ , vol. 18, no. 5, pp. 3213–3223, May 2022. 

- [19] H. Wang, L. Xu, A. Bezerianos, C. Chen, and Z. Zhang, “Linking attention-based multiscale CNN with dynamical GCN for driving fatigue detection,” _IEEE Trans. Instrum. Meas._ , vol. 70, pp. 1–11, 2021. 

- [20] D. Chen, R. Liu, Q. Hu, and S. X. Ding, “Interaction-aware graph neural networks for fault diagnosis of complex industrial processes,” _IEEE Trans. Neural Netw. Learn. Syst._ , vol. 34, no. 9, pp. 6015–6028, Sep. 2023. 

- [21] T. N. Kipf and M. Welling, “Semi-supervised classification with graph convolutional networks,” 2016, _arXiv:1609.02907_ . 

- [22] X. Li, H. Hu, S. Zhang, and G. Tang, “A fault diagnosis method for rotating machinery with semi-supervised graph convolutional network and images converted from vibration signals,” _IEEE Sensors J._ , vol. 23, no. 11, pp. 11946–11955, Jun. 2023. 

- [23] S. Zhang, H. Tong, J. Xu, and R. Maciejewski, “Graph convolutional networks: A comprehensive review,” _Comput. Social Netw._ , vol. 6, no. 1, pp. 1–23, Dec. 2019. 

Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on September 11,2026 at 16:19:03 UTC from IEEE Xplore.  Restrictions apply. 

IEEE SENSORS JOURNAL, VOL. 23, NO. 23, 1 DECEMBER 2023 

29302 

- [24] X. Zhao, M. Jia, and Z. Liu, “Semisupervised graph convolution deep belief network for fault diagnosis of electormechanical system with limited labeled data,” _IEEE Trans. Ind. Informat._ , vol. 17, no. 8, pp. 5450–5460, Aug. 2021. 

- [25] Z. Chen, H. Ke, J. Xu, T. Peng, and C. Yang, “Multichannel domain adaptation graph convolutional networks-based fault diagnosis method and with its application,” _IEEE Trans. Ind. Informat._ , vol. 19, no. 6, pp. 7790–7800, Jun. 2023. 

- [26] K. Sun et al., “Multi-scale cluster-graph convolution network with multichannel residual network for intelligent fault diagnosis,” _IEEE Trans. Instrum. Meas._ , vol. 71, pp. 1–12, 2022. 

- [27] K. Feng et al., “Digital twin enabled domain adversarial graph networks for bearing fault diagnosis,” _IEEE Trans. Ind. Cyber-Phys. Syst._ , vol. 1, pp. 113–122, 2023. 

- [28] Y. Xu, J. C. Ji, Q. Ni, K. Feng, M. Beer, and H. Chen, “A graphguided collaborative convolutional neural network for fault diagnosis of electromechanical systems,” _Mech. Syst. Signal Process._ , vol. 200, Oct. 2023, Art. no. 110609. 

- [29] X. Yang, Y. Zheng, Y. Zhang, D. S. Wong, and W. Yang, “Bearing remaining useful life prediction based on regression shapalet and graph neural network,” _IEEE Trans. Instrum. Meas._ , vol. 71, pp. 1–12, 2022. 

- [30] Z. Chen et al., “A knowledge embedded graph neural network-based cooling load prediction method using dynamic data association,” _Energy Buildings_ , vol. 278, Jan. 2023, Art. no. 112635. 

- [31] D. Wu and J. Zhao, “Process topology convolutional network model for chemical process fault diagnosis,” _Process Saf. Environ. Protection_ , vol. 150, pp. 93–109, Jun. 2021. 

- [32] L. Liu, H. Zhao, and Z. Hu, “Graph dynamic autoencoder for fault detection,” _Chem. Eng. Sci._ , vol. 254, Jun. 2022, Art. no. 117637. 

- [33] H. Nt and T. Maehara, “Revisiting graph neural networks: All we have is low-pass filters,” 2019, _arXiv:1905.09550_ . 

- [34] A. Goodge, B. Hooi, S.-K. Ng, and W. S. Ng, “Lunar: Unifying local outlier detection methods via graph neural networks,” in _Proc. AAAI Conf. Artif. Intell._ , 2022, vol. 36, no. 6, pp. 6737–6745. 

- [35] T. N. Kipf and M. Welling, “Semi-supervised classification with graph convolutional networks,” 2016, _arXiv:1609.02907_ . 

- [36] H. Wu and J. Zhao, “Deep convolutional neural network model based chemical process fault diagnosis,” _Comput. Chem. Eng._ , vol. 115, pp. 185–197, Jul. 2018. 

- [37] J. J. Downs and E. F. Vogel, “A plant-wide industrial process control problem,” _Comput. Chem. Eng._ , vol. 17, no. 3, pp. 245–255, Mar. 1993. 

- [38] L. Meng and J. Zhang, “IsoNN: Isomorphic neural network for graph representation learning and classification,” 2019, _arXiv:1907.09495_ . 

- [39] L.-M. Liu, A.-N. Wang, M. Sha, and F.-Y. Zhao, “Multi-class classification methods of cost-conscious LS-SVM for fault diagnosis of blast furnace,” _J. Iron Steel Res. Int._ , vol. 18, no. 10, pp. 17–23, Oct. 2011. 


![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0010-18.png)


**Ping Wu** received the B.S. and Ph.D. degrees in control theory and control engineering from Zhejiang University, Hangzhou, China, in 2003 and 2009, respectively. 

He is currently an Associate Professor with the School of Information Science and Engineering, Zhejiang Sci-Tech University, Hangzhou. His major research interests include fault diagnosis, machine learning, and industrial intelligence. 


![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0010-21.png)


**Yixuan Wang** received the B.S. degree in automation from Hangzhou Dianzi University, Hangzhou, China, in 2021. He is currently pursuing the M.S. degree in control science and engineering from the School of Information Science and Engineering, Zhejiang Sci-Tech University, Hangzhou. 

His current research interests include multivariate statistical analysis, deep learning, and fault diagnosis. 


![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0010-24.png)


**Jinfeng Gao** received the B.S. degree from the Hebei Institute of Science and Technology, Shijiazhuang, China, in 2000, the M.S. degree from the Zhejiang University of Technology, Hangzhou, China, in 2003, and the Ph.D. degree from Zhejiang University, Hangzhou, in 2008. 

She is currently a Professor with the School of Information Science and Engineering, Zhejiang Sci-Tech University, Hangzhou. Her research interests include fault detection and diagnosis, networked control, and multiagent systems. 


![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0010-27.png)


**Xujie Zhang** received the B.S. degree in mechatronics engineering and the M.S. degree in control science and engineering from Zhejiang Sci-Tech University, Hangzhou, China, in 2019 and 2022, respectively. He is currently pursuing the Ph.D. degree in control science and engineering with the College of Control Science and Engineering with Zhejiang University, Hangzhou. His current research interests include deep learning, process monitoring, and fault diagnosis. 


![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0010-29.png)


**Siwei Lou** received the B.Eng. degree in automation and the M.Sc. degree in control science and engineering from the School of Mechanical Engineering and Automation, Zhejiang Sci-Tech University, Hangzhou, China, in 2018 and 2021, respectively. He is currently pursuing the Ph.D. degree in control science and engineering with the College of Control Science and Engineering, Zhejiang University, Hangzhou. 

His current research interests include statistical machine learning, deep learning, process monitoring, and fault diagnosis. 


![](Multichannel_Dynamic_Graph_Convolutional_Network-Based_Fault_Diagnosis_(blast_furnace)_images/conv_95627003dff59566.pdf-0010-32.png)


**Chunjie Yang** (Senior Member, IEEE) received the B.Eng. degree in machine design, the M.Eng. degree in fluid transmission and control, and the Ph.D. degree in industrial automation from Zhejiang University, Hangzhou, China, in 1992, 1995, and 1998, respectively. 

He is currently a Qiushi Distinguished Professor with Zhejiang University, where he is also a Professor with the College of Control Science and Engineering. His current research interests include modeling, control, and fault diagnosis for industrial processes, smart energy, and intelligent manufacturing. He has authored and coauthored more than 100 articles in these areas. 

Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on September 11,2026 at 16:19:03 UTC from IEEE Xplore.  Restrictions apply. 

