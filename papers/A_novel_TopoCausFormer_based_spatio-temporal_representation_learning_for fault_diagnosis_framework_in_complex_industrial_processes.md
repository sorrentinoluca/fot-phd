Journal of Process Control 165 (2026) 103808 


![](A_novel_TopoCausFormer_based_spatio-temporal_representation_learning_for fault_diagnosis_framework_in_complex_industrial_processes_images/conv_9bbc2124206da982.pdf-0001-01.png)


Contents lists available at ScienceDirect 

# Journal of Process Control 

journal homepage: www.elsevier.com/locate/jprocont 


![](A_novel_TopoCausFormer_based_spatio-temporal_representation_learning_for fault_diagnosis_framework_in_complex_industrial_processes_images/conv_9bbc2124206da982.pdf-0001-05.png)


## A novel TopoCausFormer based spatio-temporal representation learning for fault diagnosis framework in complex industrial processes<sup>$</sup> 


![](A_novel_TopoCausFormer_based_spatio-temporal_representation_learning_for fault_diagnosis_framework_in_complex_industrial_processes_images/conv_9bbc2124206da982.pdf-0001-07.png)


Kaixiang Peng<sup>a,b</sup> , Jiayin Tang<sup>a</sup> , Tie Li<sup>a</sup> , Silvio Simani<sup>c</sup> , Jie Dong<sup>a</sup> ,<sup>∗</sup> 

a _Key Laboratory of Knowledge Automation for Industrial Processes of Ministry of Education, School of Automation and Electrical Engineering, University of Science and Technology Beijing, Beijing, 100083, China_ 

b _Key Laboratory of Metallurgical Industry Safety Risk Prevention and Control of Ministry of Emergency Management, University of Science and Technology Beijing, 100083, Beijing, China_ c _Department of Engineering, University of Ferrara, Via Saragat 1E, Ferrara, 44122, Italy_ 

### A R T I C L E I N F O A B S T R A C T 

|_Keywords:_|Modern industrial process data exhibit strong topological coupling and temporal evolution, while faults|
|---|---|
|Fault diagnosis|propagate in a directional manner, which makes accurate fault detection and root-cause localisation highly|
|Process monitoring<br>|challenging. In this paper, a TopoCausFormer based spatio-temporal fault diagnosis framework (TCF-STAE) is|
|Causal graph modelling<br>Spatio-temporal representation learning<br>Node-level localisation|proposed. First, a directed causal graph is inferred from normal-operation data and used as a structural prior<br>to guide subsequent representation learning. Then, a topology- and causality-aware transformer (TopoCaus-<br>Former) is designed to incorporate causal graph centrality encoding and topology-aware spatial bias into<br>spatio-temporal feature extraction. On this basis, a causal graph-embedded spatio-temporal encoder combining<br>graph attention, TopoCausFormer, and long short-term memory is constructed to jointly capture structural<br>coupling, short-term temporal interactions, and long-range dynamic evolution. Finally, a reconstruction<br>decoder and a joint fault-scoring strategy based on reconstruction error and Kullback–Leibler divergence are<br>developed to achieve both fault detection and variable-level localisation. The effectiveness and advantages of<br>the proposed method are validated through dataset of the standard Tennessee Eastman process and actual data<br>from the hot strip mill process. The case study reveal clear latent-space separation between normal and faulty<br>conditions and interpretable variable-level localisation consistent with process mechanisms.|



#### **1. Introduction** 

Modern industrial production has rapidly evolved towards digitalisation, intelligence, and tight integration across process units and information layers. This evolution has enlarged plant scale and complexity, strengthened interconnections among equipment, and amplified the coupling of mass and energy flows [1]. In such settings, local deviations rarely remain confined: once a fault arises, it may propagate across subsystems through physical and information pathways, causing shutdowns, safety incidents, or environmental harm, with severe economic and societal consequences. Effective fault diagnosis is therefore essential to ensure production continuity, reduce maintenance costs, and improve overall reliability [2]. 

A major difficulty lies in the nature of industrial process data itself. Multivariate measurements collected from modern plants exhibit several distinctive characteristics. First, they are strongly temporal: faults may evolve gradually or abruptly, and diagnostic information 

may appear at different temporal scales. In this work, short-horizon dynamics refer to rapid local changes within a short observation window. By contrast, long-horizon dynamics refer to delayed, accumulated, or slowly evolving dependencies over extended periods [3]. Both are important for fault diagnosis, because some faults are first revealed by short-term transients, whereas reliable fault identification and localisation often require tracking their longer-term evolution and propagation. Second, they are inherently spatially coupled: sensors and actuators belong to different units of a physical process network, and their interactions are constrained by plant topology rather than regular Euclidean structure. Third, these interactions are often directional and causal rather than merely correlative, because disturbances propagate along specific pathways shaped by physicochemical mechanisms and control actions. Finally, under closed-loop regulation, the most strongly responding variables are not always the root-cause variables, which makes variable-level localisation considerably more difficult. These 

- $ This work was supported by the National Science and Technology Major Project (2025ZD1601800). ∗ Corresponding author. 

_E-mail addresses:_ kaixiang@ustb.edu.cn (K. Peng), m202420829@xs.ustb.edu.cn (J. Tang), d202440126@xs.ustb.edu.cn (T. Li), silvio.simani@unife.it (S. Simani), dongjie@ies.ustb.edu.cn (J. Dong). 

https://doi.org/10.1016/j.jprocont.2026.103808 Received 9 June 2026; Received in revised form 6 July 2026; Accepted 25 July 2026 Available online 31 July 2026 

0959-1524/© 2026 Elsevier Ltd. All rights are reserved, including those for text and data mining, AI training, and similar technologies. 

_K. Peng et al._ 

_Journal of Process Control 165 (2026) 103808_ 

properties mean that effective fault diagnosis requires a model capable of jointly characterising temporal evolution, structural coupling, and directional propagation in a unified manner. 

Fault diagnosis approaches are typically grouped into model-based, data-based, and knowledge-based families [4]. Model-based methods rely on mathematical or physical descriptions of nominal behaviour and detect deviations by comparing measurements with model predictions. Knowledge-based methods codify expert rules and perform reasoning over observed patterns. However, as plants become more intricate and operating conditions more variable, precise modelling and the long-term maintenance of expert rules become increasingly challenging and costly. Data-based methods address these issues by learning diagnostic representations directly from measurements. Early work focused on statistical learning and shallow machine learning techniques, such as principal component analysis (PCA) [5], and linear discriminant analysis (LDA) [6]. These approaches achieved important results but often required manual feature engineering and struggled with high-dimensional, heterogeneous data. Deep learning has subsequently become a central trend, enabling automatic extraction of highorder features, capturing complex nonlinear relations, and offering robustness under noise and shifting operating regimes. Representative paradigms include autoencoders (AEs), convolutional neural networks (CNNs), and recurrent neural networks (RNNs) [7]. Recent industrial anomaly-detection studies have also introduced metric-learning strategies to improve discrimination under substantial intraclass variability in process data [8]. Zero-shot diagnosis frameworks have explored hierarchical attribute guidance and LLM-activated cross-modal domain knowledge to improve fault recognition under unseen categories and scarce labels [9,10]. More recent studies have further explored explainable fusion monitoring and intelligent multi-model fusion strategies for complex industrial processes, showing the growing potential of integrated learning-based monitoring frameworks in nonlinear industrial environments [11,12]. 

However, a persistent limitation of many deep architectures is the insufficient treatment of spatial dependencies in multivariate time series collected from industrial plants. Process units interact through conservation laws and physicochemical constraints; these interactions are shaped by the underlying topology of equipment and piping and by the directionality of flows. As a result, correlations among sensor streams often reflect directed propagation effects that couple spatial structure with temporal dynamics. Standard architectures assume gridstructured Euclidean inputs, which makes it difficult to model irregular inter-sensor connectivity [13]. Graph neural networks (GNNs) naturally accommodate irregular topologies and can expose interdependencies among components, thereby improving the extraction of spatial characteristics and, ultimately, diagnostic performance. Nevertheless, many existing graph-based fault diagnosis methods are built on undirected or correlation-based graphs, which are often insufficient for distinguishing true root-cause variables from downstream affected variables. In addition, methods that model spatial and temporal information separately may fail to capture their mutual coupling, while methods that couple them directly may still overlook the directional nature of disturbance propagation. As a result, three challenges remain insufficiently addressed: (1) how to introduce a realistic directed structural prior for industrial variables; (2) how to jointly model topological coupling together with both short- and long-horizon temporal dynamics; and (3) how to support not only accurate fault detection but also interpretable node-level localisation. 

Causal modelling offers a promising way to address these limitations. Compared with correlation-based structure learning, causal graphs provide directional priors that are more consistent with real propagation mechanisms and are therefore more suitable for distinguishing causes from effects [14]. Recent studies have shown the value of causal analysis for industrial monitoring and root-cause diagnosis [15–18]. However, in many existing approaches, causal structure is either used only as an auxiliary post-analysis tool or is not deeply 

integrated into the representation-learning pipeline. Therefore, there remains a need for a unified fault diagnosis framework in which causal topology directly guides spatio-temporal feature extraction and contributes to variable-level diagnosis. 

In consideration of the above-mentioned limitations, a TopoCausFormer based spatio-temporal auto-encoder (TCF-STAE) model and its diagnosis framework is proposed. First, to address the lack of directional structural priors in existing approaches, we introduce a causal graph as the core topological backbone of the entire framework. This directed topology captures the realistic propagation pathways of industrial processes and directly guides the spatial aggregation and temporal dependency modelling within the encoder. Second, to jointly capture spatial structure together with long- and short-horizon temporal features, we build a spatio–temporal encoder centred on the proposed topology- and causality-aware transformer (TopoCausFormer), which integrates causal and topological priors with transformer-based temporal modelling. Graph attention networks (GAT) [19] and a long short-term memory (LSTM) [20] layer are incorporated as complementary modules that enhance spatial aggregation and long-term dynamics. Finally, a reconstruction decoder and a fault-scoring scheme combining reconstruction error with Kullback–Leibler (KL) divergence [21] are formulated, enabling effective fault detection and variable-level localisation within the TCF-STAE framework. The main contributions are as follows: 

1. A causal-topology-guided spatio-temporal fault diagnosis framework is proposed. It jointly extracts spatial and temporal representations to support fault detection and variable-level localisation. 

2. A topology- and causality-aware transformer, TopoCausFormer, is developed to embed directed causal priors into spatio-temporal representation learning. It incorporates centrality encoding and topology-aware spatial bias to enhance the discriminative ability of the learned latent features. 

3. A graph-embedded spatio-temporal encoder is constructed to jointly capture structural coupling, short-term temporal interactions, and long-range dynamic evolution, yielding compact representations that support subsequent reconstruction and nodelevel fault diagnosis. 

The remainder of this paper is organised as follows. The related works are reviewed in Section 2. The proposed framework is detailed in Section 3. Experimental settings and results on a chemical benchmark and a steel rolling application are reported in Section 4. Conclusions and future perspectives are discussed in Section 5. 

#### **2. Related work** 

Data-driven fault diagnosis methods can be broadly grouped into temporal, spatial, and spatio-temporal modelling approaches. On the temporal side, unsupervised detectors based on local trend inconsistency (LTI) recognise anomalies through multi-source prediction and sequence-weighted comparison [22]. Representative work has addressed online monitoring of dynamic industrial data under challenging temporal settings, such as multiphase batch processes with varying durations [23] and nonlinear dynamic process monitoring with hierarchical time-delay analytics [24]. For large-scale dynamic plants, decentralised PCA with relevance/redundancy-based variable selection has also been adopted to improve scalability and variable interpretability in distributed monitoring [25]. TimesNet reshapes onedimensional series into two-dimensional tensors via multi-period segmentation and employs two-dimensional convolutions (2D CNNs) to model both intra- and inter-period variations in a unified manner [26]. Dual-domain frameworks jointly analyse time and frequency with nested sliding windows and align the two scores at point level for precise detection [27]. 

2 

_K. Peng et al._ 

_Journal of Process Control 165 (2026) 103808_ 

Spatial modelling aims to capture the structural dependencies among process variables, which are essential for describing plant-wide coupling in complex industrial systems. Convolutional neural networks (CNNs) with global perception integrate local and global cues for rolling-bearing diagnosis [28]; residual networks (ResNets) fed with multi-view fault images and equipped with cross-multiple attention emphasise abnormal patterns at the feature level [29]. For multivariate industrial processes, graph formulations explicitly encode inter-sensor relations. The interaction-aware graph neural network (IAGNN) builds a weighted heterogeneous graph from multi-sensor signals, learns diverse interaction edges with attention, and performs feature fusion via specialised subgraphs, enabling graph-based diagnosis in complex plants [13]. Graph-based ideas have also been extended to heterogeneous and data-scarce industrial scenarios, for example through graph-aided federated learning for few-shot fault diagnosis [30]. More broadly, GNNs offer generic operators for neighbourhood aggregation and attention-based importance weighting, while inductive variants generalise to unseen nodes; surveys consistently report gains whenever topology is informative [31]. Recent advanced process-monitoring studies have further emphasised graph-based modelling as a promising direction for representing interconnected process units and tracing disturbance propagation over structured networks [32,33]. 

In complex industrial processes, fault-related information is usually expressed through the joint evolution of variable interactions and temporal dynamics, so modelling the spatial and temporal dimensions separately may overlook important cross-dimensional dependencies. Two families are commonly distinguished [34]. Combined-processing approaches extract spatial and temporal information within a single module, as in graph sequence neural networks (GSNNs) [35]; these designs can capture interplay but often require recomputing the graph at each time step, increasing complexity and cost. Separated-processing methods extract temporal and spatial features in distinct modules and subsequently fuse them, as in spatio–temporal graph-based long shortterm memory (ST-LSTM) networks [36]. This modularity improves efficiency but may miss cross-dimensional interactions. However, without explicit structural priors linking sensors and units, they may struggle to explain propagation paths and can amplify spurious correlations in multivariate settings. Recent hybrid deep architectures have also shown that combining neighbourhood selection, attention mechanisms, and spatio-temporal learning can improve the modelling of coupled dynamic systems [33,37]. Recent machine-learning-based monitoring studies have also proposed integrated learning frameworks and hybrid nonlinear detectors for robust fault detection in complex chemical processes [38–40]. 

A complementary strand leverages causal priors to disambiguate directionality and support root-cause analysis. Foundational work shows that causal structure improves generalisation under interventions and distribution shift [14]. In industrial monitoring, causal Bayesian networks combined with hypothesis testing identify root-cause indicators without supervision [15]; unified frameworks integrate Granger-causal discovery with detection and diagnosis, using explicit graphs and causal embeddings [16]. Benchmark studies on the Tennessee Eastman process (TEP) highlight that methods ignoring topology or directionality may detect deviations yet fall short in consistent node-level localisation when effects propagate across units [41]. These recent developments indicate a clear trend towards more integrative monitoring frameworks that jointly exploit structural connectivity, temporal evolution, and prior knowledge, which motivates the causal-topology-guided spatio-temporal design adopted in this work. 

#### **3. Proposed framework** 

This section details the TopoCausFormer based spatio-temporal fault diagnosis framework shown in Fig. 1, which is comprised of three modules: parallel data preparation, spatio-temporal encoder, and reconstruction decoder. Subsequently, the online fault diagnosis procedure is explored. 

#### _3.1. Overall modular structure of TCF-STAE fault diagnosis framework_ 

In the parallel data preparation stage, a directed causal graph is first inferred from normal-operation measurements using a causal discovery backbone. This causal graph serves as a stable structural prior describing the underlying cause–effect relationships among process variables and provides an adjacency matrix as well as optional centrality cues that characterise the directional influence of each node. In parallel, the raw multivariate time series is segmented into a set of overlapping sliding windows, ensuring that both local temporal variations and broader process dynamics are preserved for downstream modelling. A lightweight dispatch mechanism then pairs each windowed subsequence with the global causal graph so that subsequent encoding operates under consistent causal constraints without recomputing the graph at every step. 

The paired causal topology and windowed sequences are subsequently fed into the spatio-temporal encoder, which integrates graphbased spatial reasoning with both short-term and long-range temporal modelling. Specifically, the encoder first leverages a GAT layer guided by the causal graph to extract neighbourhood-aware spatial dependencies, after which the TopoCausFormer enriches these representations by incorporating causal and topological priors and short-horizon temporal patterns. A final LSTM layer further aggregates the window-level embeddings to capture long-range temporal dependencies across time, producing fused spatio-temporal interaction features that reflect both directional structure and multi-scale dynamics. 

Finally, a reconstruction decoder is applied to restore the original multivariate measurements from the learned embeddings. Deviations between the reconstructed and actual inputs are quantified through a joint fault-scoring scheme that combines the reconstruction error with the KL divergence of the latent distribution, thereby enabling robust unsupervised fault detection and variable-level localisation within a unified framework. 

#### _3.2. Parallel data preparation_ 

The method adopts a graph-structured representation in which nodes correspond to sensors and edges encode inter-sensor dependencies. This node–edge formalism captures both the structural characteristics and the dynamic interactions of the process. Let **_𝑿_** ∈ R<sup>_𝑁_×</sup><sup>_𝑇_</sup> denote the multivariate series collected under normal operation, where _𝑁_ is the number of sensors and _𝑇_ the time length. To guide representation learning with directional information, a directed causal graph _𝐺_ is first inferred from **_𝑿_** , providing an adjacency (or influence) matrix and, optionally, centrality weights. Unlike correlation graphs, this topology emphasises genuine cause–effect pathways and attenuates spurious associations, which is crucial when faults propagate across units. 

In parallel, **_𝑿_** is segmented with a sliding window of length _𝑤_ and step _𝑙_ , yielding _𝑀_ subsequences { **_𝑿_**<sup>(</sup><sup>_𝑚_)</sup> }<sup>_𝑀_</sup> _𝑚_ =1<sup>,where</sup><sup>**_𝑿_**(</sup><sup>_𝑚_)∈R</sup><sup>_𝑁_×</sup><sup>_𝑤_.</sup> A lightweight dispatch layer pairs _𝐺_ with each window **_𝑿_**<sup>(</sup><sup>_𝑚_)</sup> , ensuring that subsequent encoding operates under causal constraints while preserving temporal context. This arrangement allows the encoder to extract spatio–temporal features without recomputing the graph at every step, thereby controlling complexity and maintaining fidelity to the plant dynamics. 

#### _3.3. Spatio-temporal encoder_ 

The spatio-temporal encoder integrates a GAT, the topology- and causality-aware transformer (TopoCausFormer), and a LSTM layer to fuse spatial and temporal information under causal constraints. The GAT exploits the causal graph _𝐺_ to learn neighbourhood-aware spatial dependencies, yielding features **_𝑯_** . The TopoCausFormer preserves and enhances this structure while capturing short-term temporal patterns, producing preliminary spatio-temporal representations **_𝒁_** . The LSTM then models long-range dynamics over **_𝒁_** , resulting in the final fused 

3 

_K. Peng et al._ 

_Journal of Process Control 165 (2026) 103808_ 


![](A_novel_TopoCausFormer_based_spatio-temporal_representation_learning_for fault_diagnosis_framework_in_complex_industrial_processes_images/conv_9bbc2124206da982.pdf-0004-02.png)


**Fig. 1.** Overall framework with causal graph, spatio-temporal encoder, decoder, and scoring. 

embedding **_𝑺_** . This integrated design captures spatial couplings and both long- and short- horizon behaviours in a coordinated manner, improving expressiveness and robustness compared with pipelines that treat space and time separately. 

TopoCausFormer integrates self-attention with topology-aware bias to complement the spatial features provided by GAT with short-range temporal modelling under causal constraints. Inspired by Kong et al. [42] and Ying et al. [43] and by self-attention [44], the module explicitly exploits directed cause–effect connections between nodes, strengthening spatial representations while capturing temporal dependencies. Fig. 2 outlines the architecture. 

An embedding layer encodes the input features into **_𝑬_** . To expose the structural importance of each node, a centrality encoding [43] is added on top of a linear projection. For node _𝑣𝑖_ : 


![](A_novel_TopoCausFormer_based_spatio-temporal_representation_learning_for fault_diagnosis_framework_in_complex_industrial_processes_images/conv_9bbc2124206da982.pdf-0004-07.png)


where **_𝒉_** _𝑖_ is the feature of node _𝑣𝑖_ in **_𝑯_** , deg<sup>−</sup> (⋅) and deg<sup>+</sup> (⋅) denote in- and out-degree, and **_𝒂_**<sup>−</sup> _𝑑_ ∈{ **_𝒂_**<sup>−</sup> 0<sup>_,_…</sup><sup>_,_</sup><sup>**_𝒂_**</sup> _𝐷_<sup>−</sup> max<sup>−},</sup><sup>**_𝒂_**+</sup> _𝑑_ ∈{ **_𝒂_**<sup>+</sup> 0<sup>_,_…</sup><sup>_,_</sup><sup>**_𝒂_**+</sup> _𝐷_ max<sup>+}</sup> are learnable lookup tables. This augmentation allows the attention mechanism to reflect node importance within the causal topology and guides subsequent temporal modelling. 

Intuitively, the two lookup tables assign a learnable bias to each node according to its in- and out-degree, so that nodes with larger structural influence receive a stronger signal before attention is applied. This makes the encoder sensitive to directionality and prevents purely correlation-driven aggregation. 

Queries and keys are obtained from the projected embeddings, whereas values are generated by a multi-variate causal attention (MVCA) block partially reused from the causal discovery backbone. Specifically, the intermediate causal-attention layers are transferred from the discovery stage and kept fixed, while the input and output layers remain trainable in TopoCausFormer. This design preserves causally meaningful temporal dependency patterns learned during discovery, while retaining sufficient flexibility for the value branch to adapt to the downstream spatio-temporal representation learning task. A topology-aware bias then shifts the attention logits according to directed path length. Moreover, queries and keys are obtained through linear projections _𝑄_ = Linear _𝑄_ ( **_𝑬_** ) and _𝐾_ = Linear _𝐾_ ( **_𝑬_** ). Values are produced by a multi-variate causal attention (MVCA) block derived from the causal backbone, which shares parameters with the discovery 

stage to capture temporal causal dependencies across nodes efficiently. To leverage directionality and path length in the causal graph, a spatial encoding bias _𝑏𝜙_ ( _𝑣𝑖,𝑣𝑗_ ) is added to the attention logits, where: 


![](A_novel_TopoCausFormer_based_spatio-temporal_representation_learning_for fault_diagnosis_framework_in_complex_industrial_processes_images/conv_9bbc2124206da982.pdf-0004-12.png)



![](A_novel_TopoCausFormer_based_spatio-temporal_representation_learning_for fault_diagnosis_framework_in_complex_industrial_processes_images/conv_9bbc2124206da982.pdf-0004-13.png)


with **_𝒁_** _𝑡_ ∈ R<sup>_𝑤_×</sup><sup>_𝑁_×</sup><sup>_𝑑𝑧_</sup> , where _𝑤_ is the window length, _𝑑𝑧_ the output feature dimension, and _𝑑𝑘_ the key dimension. Stacking across windows yields **_𝒁_** = [ **_𝒁_** 1 _,_ … _,_ **_𝒁_** _𝑀_ ]. In this way, TopoCausFormer preserves spatial fidelity while extracting short-range temporal patterns, providing a compact representation for the downstream long-horizon modelling stage. 

Fig. 2 illustrates the data flow within the module. The input features **_𝑯_** are linearly projected and enriched with centrality vectors selected by in- and out-degree, yielding **_𝑬_** as in Eq. (1). Queries and keys are obtained from **_𝑬_** , whereas values come from a causal attention block (MVCA) shared with the discovery stage to capture temporal dependencies across nodes efficiently. A topology-aware bias _𝑏𝜙_ ( _𝑣𝑖,𝑣𝑗_ ) shifts the attention logits according to directed path length, so that unreachable or distant pairs contribute less. The resulting window representation **_𝒁_** _𝑡_ ∈ R<sup>_𝑤_×</sup><sup>_𝑁_×</sup><sup>_𝑑𝑧_</sup> aggregates short-range temporal patterns while preserving graph structure, and stacked windows form **_𝒁_** = [ **_𝒁_** 1 _,_ … _,_ **_𝒁_** _𝑀_ ], which is then passed to the long-horizon modelling stage. 

#### _3.4. Reconstruction decoder_ 

Reconstruction is performed by a decoder built on graph convolutional networks (GCNs) [45], which aggregate neighbourhood information through stacked graph convolutions and then project back to the input space via a fully connected layer, producing **_𝑿_** . Training minimises a combination of reconstruction discrepancy and distributional shift. The reconstruction term for a window of length _𝑤_ is: 

4 

_K. Peng et al._ 

_Journal of Process Control 165 (2026) 103808_ 


![](A_novel_TopoCausFormer_based_spatio-temporal_representation_learning_for fault_diagnosis_framework_in_complex_industrial_processes_images/conv_9bbc2124206da982.pdf-0005-02.png)


**Fig. 2.** TopoCausFormer: embedding with centrality encoding, causal attention, and topology-aware bias. 


![](A_novel_TopoCausFormer_based_spatio-temporal_representation_learning_for fault_diagnosis_framework_in_complex_industrial_processes_images/conv_9bbc2124206da982.pdf-0005-04.png)


while the shift term measures the divergence between the empirical distribution of each node within a window and its nominal, offline estimate. Let _𝑝𝑖,𝑡_ denote the empirical distribution (or a parametric estimate) of node _𝑖_ in window _𝑡_ , and _𝑞𝑖_<sup>offthenominaldistribution</sup> learned from normal data; then: 


![](A_novel_TopoCausFormer_based_spatio-temporal_representation_learning_for fault_diagnosis_framework_in_complex_industrial_processes_images/conv_9bbc2124206da982.pdf-0005-06.png)


The overall loss is: 


![](A_novel_TopoCausFormer_based_spatio-temporal_representation_learning_for fault_diagnosis_framework_in_complex_industrial_processes_images/conv_9bbc2124206da982.pdf-0005-08.png)


where _𝛽>_ 0 balances the two contributions. In practice, rec captures sample-wise deviations, whereas kl increases sensitivity to distributional changes that may precede large reconstruction errors. 

#### _3.5. Online monitoring_ 

During online monitoring, incoming data are processed by the trained model to compute a per-node evidence score that combines instantaneous reconstruction error and divergence from nominal behaviour: 


![](A_novel_TopoCausFormer_based_spatio-temporal_representation_learning_for fault_diagnosis_framework_in_complex_industrial_processes_images/conv_9bbc2124206da982.pdf-0005-12.png)


where { _𝑞𝑖,𝑚_<sup>off}</sup> _𝑚_<sup>_𝑀_</sup> =1<sup>arenominalprototypes(e.g.,window-wiseestimates)</sup> for node _𝑖_ learned offline. Because different variables may exhibit markedly different score scales under normal operation, a node-wise calibration is required before aggregation. We therefore compare each raw node score with a data-driven threshold derived from the training set and, for the retained abnormal responses, normalise by the corresponding training dispersion: 


![](A_novel_TopoCausFormer_based_spatio-temporal_representation_learning_for fault_diagnosis_framework_in_complex_industrial_processes_images/conv_9bbc2124206da982.pdf-0005-14.png)


where _𝑒𝑖,_ max is the maximum score of node _𝑖_ on the training set, _𝜎𝑖_ the standard deviation of its scores under normal operation, and _𝛼_ ∈(0 _,_ 1] a sensitivity parameter. 

The window score aggregates node-wise evidence: 


![](A_novel_TopoCausFormer_based_spatio-temporal_representation_learning_for fault_diagnosis_framework_in_complex_industrial_processes_images/conv_9bbc2124206da982.pdf-0005-17.png)


and triggers a decision according to: 


![](A_novel_TopoCausFormer_based_spatio-temporal_representation_learning_for fault_diagnosis_framework_in_complex_industrial_processes_images/conv_9bbc2124206da982.pdf-0005-19.png)


In practice, a non-zero threshold _𝜏𝑤_ ≥ 0 can be used instead of 0 to control false alarms; by default we set _𝜏𝑤_ = 0. For windows flagged as faulty, the set of nodes with _𝜀𝑖,𝑡 >_ 0 provides variablelevel localisation, thereby indicating the most likely contributors to the abnormal behaviour. Since each node in the graph corresponds to one process variable, the terms node-level localisation and variable-level localisation are used equivalently in this work. By contrast, root-cause localisation refers to the more specific objective of identifying the true physical source of the fault among the localised abnormal variables. 

#### **4. Application examples and results** 

This section evaluates the practicality and effectiveness of the proposed strategy in two settings: a benchmark industrial process and a real industrial application. The two case studies are chosen to reflect the key characteristics highlighted in the Introduction, namely temporal evolution, spatial coupling, and directional fault propagation in industrial process data. The benchmark comprises a multi-stage process with variables of different physical natures and is used to compare our approach with contemporary fault-diagnosis methods and to assess localisation capability. The real-plant study verifies feasibility under practical operating conditions. 

We compare the proposed method against state-of-the-art baselines, namely a long short-term memory-variational autoencoder (LSTMVAE) [46], multivariate time-series anomaly Detection via graph attention network (MTAD-GAT) [47], graph deviation network (GDN) [48], and dynamic edge via graph attention (DyEdgeGAT) [49]. Detection performance is measured with three standard metrics: Precision, Recall, and F1 score, which capture complementary aspects of the classifier’s behaviour: 


![](A_novel_TopoCausFormer_based_spatio-temporal_representation_learning_for fault_diagnosis_framework_in_complex_industrial_processes_images/conv_9bbc2124206da982.pdf-0005-24.png)


Here, TP (true positives) counts correctly detected faulty instances, FP (false positives) counts normal instances incorrectly flagged as faulty, and FN (false negatives) counts faulty instances missed by the detector. 

For a fair comparison across datasets, the proposed TCF–STAE uses the same training hyperparameters in both studies. The sliding-window length and step are set to _𝑤_ = 32 and _𝑙_ = 32, respectively. The learning rate starts at 10<sup>−3</sup> and is reduced to 10<sup>−4</sup> after 30 epochs; training runs for 50 epochs in total. The model architecture is identical except for the input dimensionality, which depends on the number of process variables. Specifically, we use two GAT layers and two GCN layers, and set the weighting parameter _𝛽_ = 0 _._ 01. The implementation is in Python with PyTorch; experiments were executed on an NVIDIA GeForce RTX 4050 Laptop GPU (6 GB). 

#### _4.1. Tennessee Eastman process_ 

The Tennessee Eastman process (TEP) [41] is a classic simulation benchmark used to assess process monitoring, fault detection, and diagnosis algorithms. It emulates a continuous chemical plant comprising feed tanks and mixers, two-stage reactors with flash drums, separation and recycle systems, and waste-gas scrubbing and recovery. The simulation provides 12 manipulated variables and 41 process measurements; in our study, twenty variables were selected for analysis. Owing to the limited standard training set, 6000 normal samples were generated on the Matlab platform for training, while the standard test set was retained for evaluation. TEP is particularly suitable for this study because it exhibits pronounced temporal evolution, strong coupling among process units, and directional fault propagation through material flows, energy interactions, and control loops. These characteristics make it an 

5 

_K. Peng et al._ 

_Journal of Process Control 165 (2026) 103808_ 

appropriate benchmark for evaluating whether the proposed method can jointly capture multi-scale temporal behaviour and causally guided cross-unit dependencies. 

To illustrate detection behaviour, we visualise window-level scores for representative faults. Fig. 3 reports the evolution of the window score for Fault 6 and Fault 8. In the released test protocol the fault is injected at window index 5; from that point, the score exhibits a clear change and remains elevated for most subsequent windows, allowing the onset to be identified accurately. 

Table 1 summarises detection performance across competing methods on TEP. The proposed approach delivers the highest F1 scores overall. The LSTM–VAE, which models only temporal dependencies, performs best on Fault 8 but attains an F1 of 0.8678. MTAD-GAT, which combines temporal modelling with graph attention over time series, achieves leading results on Faults 4, 12, 17, and 18, yet shows weak robustness on Faults 2 and 14. GDN, which focuses on spatial relations, reaches around 0.90 across faults but leaves headroom for improvement. DyEdgeGAT, which jointly models spatio–temporal dependencies with dynamic edges, attains a competitive average F1 of 0.9003 with high recall, although precision varies markedly across scenarios, indicating a propensity to raise false alarms under complex or weakly correlated patterns. 

By embedding causal topological priors within a collaborative spatio–temporal extractor, the proposed TCF–STAE captures both structural dependencies and short-/long-horizon dynamics. The integration of causal spatial attention with temporal modelling helps distinguish genuine cause–effect faults from superficial correlations, yielding more accurate and robust detection and a consistent F1 advantage over the baselines. 

To further illustrate the representation ability of the proposed encoder, the window-level latent embeddings of normal operation and representative faulty conditions are projected into a two-dimensional space using t-SNE. As shown in Figs. 4(a) and 4(b), the embeddings of Fault 6 and Fault 14 are distributed in regions clearly separated from the normal windows. This indicates that the causal graph-embedded spatio-temporal encoder learns discriminative latent representations for different process conditions. The observed separability is consistent with the superior detection performance in Table 1 and helps explain the clear fault-score transitions reported in Fig. 3. In summary, the method demonstrates strong detection performance on TEP together with adaptability to diverse anomaly patterns. Although the proposed method achieves the best average F1 score on the TEP benchmark, it is not uniformly optimal for every fault type. In particular, the performance on Fault 4 and Fault 17 remains below that of some competing methods. A plausible explanation is that these faults produce weaker or more spatially diffuse signatures, so that the boundary between root-cause variables and downstream affected variables becomes less distinct in the learned latent space. In addition, under closed-loop control, compensatory responses may partially mask the original disturbance and reduce the consistency of node-level evidence. Since the causal graph used in this work is inferred offline from normal-operation data, its fixed topology may not fully reflect the altered propagation structure under certain abnormal regimes. These observations suggest that adaptive causal updating and uncertaintyaware scoring are promising directions for improving robustness on challenging fault scenarios. 

We select two representative faults from the TEP dataset — Fault 6 and Fault 14 — to illustrate localisation. Fault 6 corresponds to a loss of material A due to the feed rate of manipulated variable A dropping to zero. Fault 14 corresponds to a stuck cooler valve in the reactor, i.e., a change in the reactor cooling-water flow. Figs. 5(a) and 5(b) show heatmaps of node-level scores for the two cases, and Table 2 reports the correspondence between key nodes and TEP variables. 

For Fault 6 (Fig. 5(a)), the method consistently highlights the rootcause variable — the feed rate of material A — across all fault instances. The reactor level XMEAS(8) and reactor temperature XMEAS(9) also 

exhibit marked responses, reflecting the impact of the change in reactant A on reactor conditions. Because TEP operates under closedloop control, variations in XMEAS(9) induce compensatory action on the cooling-water flow XMV(10), which is therefore flagged as affected. Apart from the root-cause variable and these strongly coupled variables, scores for other variables remain essentially zero. 

For Fault 14 (Fig. 5(b)), the root cause — reactor cooling-water flow XMV(10) — is correctly detected across all fault instances. Its influence on the reactor level XMEAS(8) is visible in many windows, whereas weakly related variables maintain low scores. 

These results stem from the causal graph–based representation, which injects directionality into feature extraction and helps distinguish genuine causes from merely correlated effects. Modelling the sensor network as a graph with node-wise scores provides a direct mechanism for localisation: a high score on a node indicates the variable most responsible for the abnormal behaviour. The analysis of Faults 6 and 14 confirms robust localisation capability on TEP. 

Beyond accuracy, the TEP results point to favourable robustness and reliability. After fault injection, window scores remain clearly separated from nominal behaviour (Fig. 3), while node-wise heatmaps show stable, sparse patterns that are straightforward to interpret (Fig. 5). Thresholds are estimated once from nominal data and used across all faults, avoiding case-specific tuning and helping control false alarms. Compared with methods that treat space and time separately or rely on correlation graphs (Table 1), the causal topology-aware encoder suppresses spurious associations and delivers more uniform performance across heterogeneous faults, including cases with propagation effects. From a computational standpoint, inference scales linearly with the number of graph edges used by message passing and does not require per-step graph recomputation; sliding windows can be batched, and the decoder is lightweight. As a result, latency per window remains low and compatible with typical process sampling periods, supporting deployment under routine plant conditions. Overall, the approach couples competitive detection with stable operation and transparent, variable-level diagnosis. 

#### _4.2. Hot strip mill process_ 

Modern hot strip rolling is a highly efficient, fully automated production route designed for high quality. The process involves more than 1500 variables, roughly half of which directly or indirectly affect the final product. The production sequence proceeds through heating, rough rolling, flying shearing, finishing mill, laminar cooling, and coiling. Among these stages, the finishing mill process (FMP) is the core of hot strip production. A typical 1700 mm finishing mill comprises seven stands in series; each stand has two work rolls, two backup rolls, and a hydraulic system for roll control. Cooling-water sprays are placed at the stand entry to condition the strip. After roughing, the strip passes through the seven stands for continuous reduction, while the control system automatically regulates operating points so that the exit temperature, thickness, flatness, and other quality indicators meet their targets. 

The dataset used in this study focuses on the FMP of a 1700 mm line. The process variables considered are listed in Table 3, and the two fault types used for evaluation are summarised in Table 4. Data are sampled every 0.01 s. The training set contains 6000 normal records (used to learn the nominal model), and the test set includes 2000 records for each fault type. This setting allows us to assess the proposed method under realistic operating conditions while keeping training strictly normal-only. The FMP dataset complements TEP by providing a real industrial scenario with high-frequency temporal variation, strong spatial coupling among adjacent stands and actuators, and downstream disturbance propagation along the rolling direction and feedback-control chain. This makes it well suited for validating the proposed method under practical plant conditions where temporal dynamics and structural interactions are tightly intertwined. 

6 

_K. Peng et al._ 

_Journal of Process Control 165 (2026) 103808_ 


![](A_novel_TopoCausFormer_based_spatio-temporal_representation_learning_for fault_diagnosis_framework_in_complex_industrial_processes_images/conv_9bbc2124206da982.pdf-0007-02.png)


**Fig. 3.** Window fault scores on the Tennessee Eastman process. 


![](A_novel_TopoCausFormer_based_spatio-temporal_representation_learning_for fault_diagnosis_framework_in_complex_industrial_processes_images/conv_9bbc2124206da982.pdf-0007-04.png)


**Fig. 4.** t-SNE visualisation of the window-level latent embeddings learned by the proposed encoder on the Tennessee Eastman process. 


![](A_novel_TopoCausFormer_based_spatio-temporal_representation_learning_for fault_diagnosis_framework_in_complex_industrial_processes_images/conv_9bbc2124206da982.pdf-0007-06.png)


**Fig. 5.** Fault localisation on the Tennessee Eastman process. 

We assess detection behaviour on the FMP dataset by inspecting the evolution of the window score. Figs. 6(a)–6(b) reports the score versus window index for Fault 1 and Fault 2. In both cases, the fault is injected at window 31; from that point, the score shows a clear change and remains elevated for most subsequent windows where the fault persists, indicating reliable separation from nominal behaviour and supporting practical detectability in plant conditions. With a sampling interval of 

0.01 s and a window step of 32 samples, an injection at 10 s corresponds approximately to window index 31. 

Table 5 summarises the detection performance of the proposed method against four baselines on FMP. The proposed approach consistently achieves higher Precision, Recall, and F1 scores across both faults, with gains that reflect improved sensitivity and reduced false alarms. Taken together with the stability of the window score in Fig. 

7 

_K. Peng et al._ 

_Journal of Process Control 165 (2026) 103808_ 

**Table 1** 

Detection <u>performance</u> on the Tennessee Eastman <u>process.</u> 

|Fault|LSTM–V|AE||MTAD–G|AT||GDN|||DyEdgeG|AT||Proposed|||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|No|Pre|Rec|F1|Pre|Rec|F1|Pre|Rec|F1|Pre|Rec|F1|Pre|Rec|F1|
|1|0.8264|0.8875|0.8549|0.8142|1.0000|0.8976|0.8427|0.9975|0.9142|0.8558|0.9050|0.8797|0.9231|0.9600|**0.9412**|
|2|0.8016|0.7625|0.7816|0.6939|0.1700|0.2731|0.8403|1.0000|**0.9127**|0.8439|0.9862|0.9095|0.8846|0.9200|0.9020|
|3|0.8529|0.8550|0.8539|0.9302|1.0000|0.9639|0.8404|0.9875|0.9080|0.8824|0.9750|**0.9264**|0.9565|0.8800|0.9167|
|4|0.8418|0.8650|0.8533|0.9734|0.9600|**0.9666**|0.8448|0.9863|0.9100|0.8733|0.9738|0.9208|0.8800|0.8800|0.8800|
|5|0.8302|0.7212|0.7719|0.9102|0.7475|0.8209|0.8424|0.9889|0.9097|0.8367|0.7750|0.8047|0.9583|0.9200|**0.9388**|
|6|0.8319|0.8600|0.8457|0.8013|0.8916|0.8440|0.8477|0.9813|0.9096|0.8629|0.9612|0.9094|1.0000|0.9600|**0.9796**|
|7|0.8413|0.8813|0.8608|0.8003|0.8003|0.8003|0.8418|0.9775|0.9046|0.8448|0.9950|**0.9138**|0.9167|0.8800|0.8980|
|8|0.8474|0.8889|0.8676|0.9565|0.9625|0.9595|0.8437|0.9850|0.9089|0.8452|0.9975|0.9150|1.0000|0.9600|**0.9796**|
|9|0.8371|0.8413|0.8392|0.9631|0.9450|0.9539|0.8403|1.0000|0.9127|0.8486|0.8125|0.8301|1.0000|0.9200|**0.9583**|
|10|0.8439|0.8850|0.8639|0.8000|0.7703|0.7849|0.8413|0.9937|0.9112|0.8436|0.9587|0.8975|0.9200|0.9200|**0.9200**|
|11|0.8461|0.8863|0.8657|0.8006|0.7960|0.7983|0.8432|0.9950|0.9128|0.8437|0.9800|0.9068|0.9231|0.9600|**0.9412**|
|12|0.8462|0.8600|0.8531|0.9615|0.9688|**0.9651**|0.8407|0.9963|0.9119|0.8761|0.9638|0.9179|1.0000|0.8800|0.9362|
|13|0.8465|0.8689|0.8575|0.9749|0.8725|0.9208|0.8413|0.9937|0.9112|0.8744|0.9663|0.9181|0.9583|0.9200|**0.9388**|
|14|0.8363|0.8363|0.8363|0.8783|0.5413|0.6693|0.8403|1.0000|0.9127|0.8449|0.9875|**0.9107**|0.9565|0.8800|0.9167|
|15|0.8365|0.8375|0.8370|0.9154|0.8113|0.8602|0.8479|0.9963|0.9156|0.8453|0.9837|0.9093|0.9200|0.9200|**0.9200**|
|16|0.8369|0.8400|0.8384|0.9539|0.6988|0.8066|0.8427|0.9975|0.9142|0.8448|0.9662|0.9015|0.9231|0.9600|**0.9412**|
|17|0.8430|0.8725|0.8575|0.9601|0.9638|**0.9619**|0.8466|0.9938|0.9143|0.8710|0.9625|0.9145|0.8846|0.9200|0.9020|
|18|0.8497|0.8763|0.8628|0.9574|0.9550|**0.9562**|0.8403|1.0000|0.9127|0.8737|0.9513|0.9103|1.0000|0.8800|0.9362|
|19|0.8371|0.8413|0.8392|0.9114|0.7200|0.8045|0.8402|0.9989|0.9126|0.8444|0.9837|0.9098|0.9200|0.9200|**0.9200**|
|20|0.8487|0.8275|0.8380|0.9480|0.8425|0.8920|0.8440|0.9875|0.9101|0.8604|0.9550|0.9052|1.0000|0.9200|**0.9583**|
|21|0.8367|0.8387|0.8377|0.9423|0.7763|0.8513|0.8417|0.9900|0.9098|0.8418|0.9575|0.8959|0.9583|0.9200|**0.9388**|
|Average|0.8390|0.8492|0.8436|0.8975|0.8187|0.8453|0.8426|0.9927|0.9114|0.8551|0.9523|0.9003|0.9468|0.9181|**0.9316**|



##### **Table 2** 

Mapping between nodes and Tennessee Eastman <u>process</u> variables. 

|Node|TEP variable|
|---|---|
|5|XMEAS(8), Reactor level|
|6|XMEAS(9), Reactor temperature|
|11|XMEAS(21), Reactor cooling-water outlet temperature|
|17|XMV(3), A feed flow|
|18|XMV(10), Reactor cooling-water flow|



##### **Table 3** 

Variables used from the finishing mill <u>process</u> dataset. 

|Variable(s)|Description<br>Unit|
|---|---|
|G1–G7|Average roll gap of FM_𝑖_, _𝑖_= 1_,_…_,_7<br>mm|
|TF1–TF7|Total rolling force of FM_𝑖_, _𝑖_= 1_,_…_,_7<br>MN|
|B2–B7|Work–roll bending force of FM_𝑖_, _𝑖_= 2_,_…_,_7<br>MN|
|_𝑦_|Exit thickness<br>mm|



##### **Table 4** 

Faults considered in the finishing mill <u>process</u> dataset. 

6, these results indicate that the method offers accurate and robust detection on a real hot strip mill. 

To provide further insight into the learned representations on real industrial data, Fig. 7 visualises the t-SNE projections of the windowlevel latent embeddings for normal operation and two representative faults in the finishing mill process. It can be seen that the normal and faulty windows form distinct clusters for both Fault 1 and Fault 2, with only limited local overlap. This result suggests that the proposed encoder preserves discriminative spatio-temporal structure under practical operating conditions. The latent-space separation is consistent with the strong Precision, Recall, and F1 scores in Table 5, and further supports the practical detectability observed in Fig. 8. 

Fig. 8 shows heatmaps of node-level scores on the FMP dataset. Fault 1 corresponds to a malfunction of the bending-force sensor at Stand 5; accordingly, the bending-force node of Stand 5 (node 17) is highlighted across virtually all fault windows, whereas only a few other nodes register sporadic activity. For Fault 2, the roll gap of Stand 4 (node 3, G4) is consistently detected, as shown in Fig. 8(b). When the gap actuator at Stand 4 malfunctions, the actuator can no longer ensure that the actual gap follows the commanded set-point (e.g., due to jamming or abnormal servo control); the most directly affected variable is therefore the roll gap of that stand. These localisation outcomes align with the underlying mechanism and confirm that the proposed approach identifies true root-cause variables rather than merely correlated effects. 

Overall, the evidence across the chemical benchmark and the steel rolling line supports a consistent picture. Across the chemical benchmark and the steel rolling line, the proposed strategy delivered accurate and stable detection together with consistent localisation. On both datasets, window scores separated clearly from nominal behaviour after fault onset, and node-level heatmaps remained sparse and coherent with the underlying process mechanisms, which made the outcomes 

|Fault|Description|Occurrence time (s)|
|---|---|---|
|1|Stand 5 bending-force sensor failure|10|
|2|Stand 4 gap actuator abnormality|10|



straightforward to interpret. Thresholds estimated once from normal data generalised across heterogeneous faults without case-specific tuning, indicating favourable reliability under routine operating conditions, including closed-loop control. 

#### **5. Conclusions** 

This study presented a novel TopoCausFormer based spatio -temporal representation learning for fault diagnosis framework in complex industrial processes. A directed causal structure guided the extraction of spatial relations, while temporal modelling captured longand short- horizon dynamics. Reconstruction deviations were combined with a distributional-shift measure to yield a window-level score and variable-level evidence for localisation. Across a chemical benchmark and a steel rolling application, the method delivered accurate detection and consistent localisation, with stable separation between normal and faulty behaviour. Compared with approaches based on correlation graphs or on separate treatment of space and time, the framework reduced spurious associations and maintained more uniform behaviour across propagating effects. Several future trends and practical recommendations emerge from this study. First, the causal structure should be updated online to better track regime changes and evolving propagation pathways in real industrial environments. Second, adaptation across plants, products, or operating conditions should be investigated to improve portability and reduce the need for retraining. Third, robustness to sensor dropout, drift, and noisy measurements should be 

8 

_K. Peng et al._ 

_Journal of Process Control 165 (2026) 103808_ 


![](A_novel_TopoCausFormer_based_spatio-temporal_representation_learning_for fault_diagnosis_framework_in_complex_industrial_processes_images/conv_9bbc2124206da982.pdf-0009-02.png)


**Fig. 6.** Window fault scores on the finishing mill process dataset. 


![](A_novel_TopoCausFormer_based_spatio-temporal_representation_learning_for fault_diagnosis_framework_in_complex_industrial_processes_images/conv_9bbc2124206da982.pdf-0009-04.png)


**Fig. 7.** t-SNE visualisation of the window-level latent embeddings learned by the proposed encoder on the finishing mill process dataset. 


![](A_novel_TopoCausFormer_based_spatio-temporal_representation_learning_for fault_diagnosis_framework_in_complex_industrial_processes_images/conv_9bbc2124206da982.pdf-0009-06.png)


**Fig. 8.** Fault localisation on the finishing mill process dataset. 

**Table 5** 

Detection results on the finishing mill <u>process</u> dataset. 

|Fault|LSTM–V|AE||MTAD–G|AT||GDN|||DyEdgeG|AT||Proposed|||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|No|Pre|Rec|F1|Pre|Rec|F1|Pre|Rec|F1|Pre|Rec|F1|Pre|Rec|F1|
|1|0.8734|0.8830|0.8782|0.7475|0.8380|0.7902|0.7957|0.8573|0.8254|0.8180|0.9570|0.8820|0.9000|0.8710|**0.8852**|
|2|0.7712|0.8630|0.8145|0.8856|0.8679|0.8767|0.7393|0.8663|0.7978|0.8637|0.9630|0.9106|0.8857|1.0000|**0.9394**|



9 

_K. Peng et al._ 

_Journal of Process Control 165 (2026) 103808_ 

enhanced through uncertainty-aware scoring and confidence-sensitive graph modelling. From an application perspective, closer integration with supervisory control and maintenance systems would help translate localisation results into operator-oriented decision support. In addition, scalable and lightweight implementations for larger sensor networks and streaming data environments will be important for broader industrial deployment. Overall, the framework provided a reliable basis for practical monitoring and motivated extensions that preserved accuracy and transparency in broader industrial settings. 

#### **CRediT authorship contribution statement** 

**Kaixiang Peng:** Writing – review & editing, Supervision, Project administration, Methodology, Funding acquisition, Formal analysis, Conceptualization. **Jiayin Tang:** Writing – original draft, Visualization, Validation, Software, Formal analysis, Data curation, Conceptualization. **Tie Li:** Writing – original draft, Validation, Software, Methodology, Data curation. **Silvio Simani:** Writing – review & editing, Validation, Methodology, Formal analysis. **Jie Dong:** Writing – review & editing, Validation, Supervision, Methodology, Conceptualization. 

#### **Declaration of competing interest** 

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper. 

#### **Data availability** 

Data will be made available on request. 

#### **References** 

- [1] X. Qin, H. Liu, J. Dong, K. Peng, A batch-constrained safe deep Q-learningbased cloud-edge collaborative framework for dynamic operation optimization in industrial processes, IEEE Trans. Ind. Inform. (2025) 1–12. 

- [2] C. Zhang, Y. Wang, Z. Zhao, X. Chen, H. Ye, S. Liu, Y. Yang, K. Peng, Performance-driven closed-loop optimization and control for smart manufacturing processes in the cloud-edge-device collaborative architecture: A review and new perspectives, Comput. Ind. 162 (2024) 104131. 

- [3] G. Lai, W.-C. Chang, Y. Yang, H. Liu, Modeling long- and short-term temporal patterns with deep neural networks, in: The 41st International ACM SIGIR Conference on Research Development in Information Retrieval, 2017. 

- [4] K. Peng, J. Chen, H. Yang, X. Qin, Knowledge-data-driven process monitoring based on temporal knowledge graphs and supervised contrastive learning for complex industrial processes, J. Process Control 141 (2024) 103283. 

- [5] C. Zhao, F. Gao, Fault-relevant principal component analysis (FPCA) method for multivariate statistical modeling and process monitoring, Chemometr. Intell. Lab. Syst. 133 (2014) 1–16. 

- [6] F. Li, J. Wang, M.K. Chyu, B. Tang, Weak fault diagnosis of rotating machinery based on feature reduction with supervised orthogonal local Fisher discriminant analysis, Neurocomputing 168 (2015) 505–519. 

- [7] B. Zhang, J. Zhao, X. Chen, J. Yue, C. Zhao, Category-tree-guided hierarchical knowledge transfer framework for zero-shot fault diagnosis, J. Process Control 141 (103267) (2024). 

- [8] K. Huang, S. Wu, B. Sun, C. Yang, W. Gui, Metric learning-based fault diagnosis and anomaly detection for industrial data with intraclass variance, IEEE Trans. Neural Netw. Learn. Syst. 35 (1) (2024) 547–558. 

- [9] L. Tan, C. Zhao, H. Zhang, J. Yue, Hierarchical attribute-guided generalized zero-shot learning method for industrial fault diagnosis, Control Eng. Pract. 172 (2026) 106875. 

- [10] J. Zhao, C. Zhao, J. Yue, Align knowledge with time-series: Cross-modal domain knowledge activation for LLM-enabled zero-shot fault diagnosis, J. Process Control 155 (2025) 103534. 

- [11] H. Ali, R. Safdar, Y. Zhou, Y. Yao, L. Yao, Z. Zhang, W.D. Furong Gao, A novel dynamic machine learning-based explainable fusion monitoring: application to industrial and chemical processes, Mach. Learn.: Sci. Technol. 6 (1) (2025). 

- [12] H. Ali, R. Safdar, W. Ding, Y. Zhou, Y. Yao, L. Yao, F. Gao, Intelligent machine learning-based multi-model fusion monitoring: application to industrial physio-chemical systems, Control Eng. Pract. 162 (106361) (2025). 

- [13] D. Chen, R. Liu, Q. Hu, S.X. Ding, Interaction-aware graph neural networks for fault diagnosis of complex industrial processes, IEEE Trans. Neural Netw. Learn. Syst. 34 (9) (2023) 6015–6028. 

- [14] J. Peters, D. Janzing, B. Schölkopf, Elements of Causal Inference: Foundations and Learning Algorithms, MIT Press, 2017. 

- [15] M. Li, Z. Li, K. Yin, X. Nie, W. Zhang, K. Sui, D. Pei, Causal inference-based root cause analysis for online service systems with intervention recognition, in: Proceedings of the 28th ACM SIGKDD Conference on Knowledge Discovery and Data Mining, 2022. 

- [16] F. Lv, B. Yang, S. Yu, S. Zou, X. Wang, J. Zhao, C. Wen, A unified model integrating Granger causality-based causal discovery and fault diagnosis in chemical processes, Comput. Chem. Eng. 196 (2025) 109028. 

- [17] S. Wang, Q. Zhao, Y. Han, J. Wang, Root cause diagnosis for process faults based on multisensor time-series causality discovery, J. Process Control 122 (2023) 27–40. 

- [18] H. Ali, J. Liu, F. Gao, A hybrid causal-inference and neuro-fuzzy framework for advanced process monitoring, J. Process Control 162 (103724) (2026). 

- [19] P. Veličković, G. Cucurull, A. Casanova, A. Romero, P. Liò, Y. Bengio, Graph attention networks, in: International Conference on Learning Representations, ICLR, 2018, URL: https://arxiv.org/abs/1710.10903. 

- [20] S. Hochreiter, J. Schmidhuber, Long short-term memory, Neural Comput. 9 (8) (1997) 1735–1780. 

- [21] S. Kullback, R.A. Leibler, On information and sufficiency, Ann. Math. Stat. 22 (1) (1951) 79–86, http://dx.doi.org/10.1214/aoms/1177729694. 

- [22] W. Wu, L. He, W. Lin, Y. Su, Y. Cui, C. Maple, S. Jarvis, Developing an unsupervised real-time anomaly detection scheme for time series with multi-seasonality, IEEE Trans. Knowl. Data Eng. 34 (9) (2022) 4147–4160. 

- [23] C. Zhao, S. Mo, F. Gao, N. Lu, Y. Yao, Statistical analysis and online monitoring for handling multiphase batch processes with varying durations, J. Process Control 21 (6) (2011) 817–829. 

- [24] X. Chen, C. Zhao, Linear and nonlinear hierarchical multivariate time delay analytics for dynamic modeling and process monitoring, J. Process Control 107 (2021) 83–93. 

- [25] B. Xiao, Y. Li, B. Sun, C. Yang, K. Huang, H. Zhu, Decentralized PCA modeling based on relevance and redundancy variable selection and its application to large-scale dynamic process monitoring, Process. Saf. Environ. Prot. 151 (2021) 85–100. 

- [26] H. Wu, T. Hu, Y. Liu, H. Zhou, J. Wang, M. Long, TimesNet: Temporal 2Dvariation modeling for general time series analysis, in: The 11th International Conference on Learning Representations, 2023. 

- [27] Y. Nam, S. Yoon, Y. Shin, M. Bae, H. Song, J.-G. Lee, B.S. Lee, Breaking the time-frequency granularity discrepancy in time-series anomaly detection, in: Proceedings of the ACM Web Conference 2024, 2024. 

- [28] X. Li, Y. Chen, Y. Liu, A novel convolutional neural network with global perception for bearing fault diagnosis, Eng. Appl. Artif. Intell. 143 (2025) 109986. 

- [29] Y. Liu, W. Zheng, Y. Du, Y. Wang, J. Jin, M. Yu, Bearing fault diagnosis based on cross image multi-attention mechanism, Sci. Rep. 15 (2025) 21100. 

- [30] Z. Yao, P. Song, C. Zhao, Finding trustworthy neighbors: Graph aided federated learning for few-shot industrial fault diagnosis with data heterogeneity, J. Process Control 129 (103038) (2023). 

- [31] Z. Wu, S. Pan, F. Chen, G. Long, C. Zhang, P.S. Yu, A comprehensive survey on graph neural networks, IEEE Trans. Neural Netw. Learn. Syst. 32 (1) (2021) 4–24. 

- [32] D.L. Cole, G.J. Ruiz-Mercado, V.M. Zavala, A graph-based modeling framework for tracing hydrological pollutant transport in surface waters, Comput. Chem. Eng. 179 (108457) (2023). 

- [33] H. Ali, R. Safdar, J. Liu, T.S.B.A. Manan, G. Hu, M.H. Rasool, Y. Yao, F. Gao, Hybrid fusion paradigm in advanced process monitoring: A panoramic review and future perspectives, Ind. Eng. Chem. Res. 64 (2025) 22465–22514. 

- [34] A. Zeghina, A. Leborgne, F. Le Ber, A. Vacavant, Deep learning on spatiotemporal graphs: A systematic review, methodological landscape, and research opportunities, Neurocomputing 594 (2024) 127861. 

- [35] Z. Lu, W. Lv, Z. Xie, B. Du, G. Xiong, L. Sun, H. Wang, Graph sequence neural network with an attention mechanism for traffic speed prediction, ACM Trans. Intell. Syst. Technol. 13 (2) (2022) 24. 

- [36] G. Chen, L. Hu, Q. Zhang, Z. Ren, X. Gao, J. Cheng, ST-LSTM: Spatio-temporal graph based long short-term memory network for vehicle trajectory prediction, in: 2020 IEEE International Conference on Image Processing, ICIP, 2020, pp. 608–612. 

- [37] D. Li, C. Chen, G. Chen, S. Chen, A hybrid deep learning air pollution prediction approach based on neighborhood selection and spatio-temporal attention, Sci. Rep. 15 (3685) (2025). 

- [38] H. Ali, R. Safdar, M.H. Rasool, H. Anjum, Y. Zhou, Y. Yao, L. Yao, F. Gao, Advance industrial monitoring of physio-chemical processes using novel integrated machine learning approach, Mach. Learn.: Sci. Technol. 6 (1) (2025). 

- [39] H. Ali, D.P. Andriani, R. Safdar, T.S.B.A. Manan, G. Hu, Y. Zhou, X. Zhang, Y. Yao, Z. Cao, J. Liu, F. Gao, A hybrid DiGLPP–Kolmogorov–Arnold network framework for robust fault detection in industrial chemical processes, Process. Saf. Environ. Prot. 212 (108854) (2026). 

- [40] H. Ali, R. Safdar, J. Liu, M.B. Asif, X. Zhang, M.H. Rasool, Y. Yao, L. Yao, J. Ding, F. Gao, Process monitoring and dynamic fusion of complex industrial systems: A reconstruction-based Bayesian framework, Comput. Chem. Eng. 203 (109352) (2025). 

10 

_K. Peng et al._ 

_Journal of Process Control 165 (2026) 103808_ 

- [41] J.J. Downs, E.F. Vogel, A plant-wide industrial process control problem, Comput. Chem. Eng. 17 (3) (1993) 245–255. 

- [42] L. Kong, W. Li, H. Yang, Y. Zhang, J. Guan, S. Zhou, CausalFormer: An interpretable transformer for temporal causal discovery, IEEE Trans. Knowl. Data Eng. 37 (1) (2025) 102–115. 

- [43] C. Ying, T. Cai, S. Luo, S. Zheng, G. Ke, D. He, Y. Shen, T.-Y. Liu, Do transformers really perform bad for graph representation? in: Conference on Neural Information Processing Systems 2021, 2021. 

- [44] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A.N. Gomez, Ł. Kaiser, I. Polosukhin, Attention is all you need, in: Advances in Neural Information Processing Systems, NeurIPS, 2017. 

- [45] T.N. Kipf, M. Welling, Semi-supervised classification with graph convolutional networks, in: 5th International Conference on Learning Representations, ICLR, Vol. 4, Curran Associates, Inc, Toulon, France, 2017, pp. 2713–2726. 

- [46] D. Park, Y. Hoshi, C.C. Kemp, A multimodal anomaly detector for robot-assisted feeding using an LSTM-based variational autoencoder, IEEE Robot. Autom. Lett. 3 (3) (2018) 1544–1551. 

- [47] H. Zhao, Y. Wang, J. Duan, C. Huang, D. Cao, Y. Tong, B. Xu, J. Bai, J. Tong, Q. Zhang, Multivariate time-series anomaly detection via graph attention network, in: 2020 IEEE International Conference on Data Mining, ICDM, 2020, pp. 841–850. 

- [48] A. Deng, B. Hooi, Graph neural network-based anomaly detection in multivariate time series, in: The 35th AAAI Conference on Artificial Intelligence, 2021, pp. 841–850. 

- [49] M. Zhao, O. Fink, DyEdgeGAT: Dynamic edge via graph attention for early fault detection in IIoT systems, IEEE Internet Things J. 11 (13) (2024) 22950–22965. 

11 

