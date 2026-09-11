www.nature.com/scientificreports 


![](P029_images/P029.pdf-0001-01.png)

### Figure analysis

The image appears to be a document-page excerpt from a Scientific Reports article, not a scientific data visualization.

**Purpose:** It introduces the paper titled **“AsynDBT: asynchronous distributed bilevel tuning for efficient in-context learning with large language models.”**

**Visible components:**
- Journal/site header: `www.nature.com/scientificreports`.
- Article status marker: `OPEN`.
- Title: **AsynDBT: asynchronous distributed bilevel tuning for efficient in-context learning with large language models**.
- Authors: Hui Ma, Shaoyu Dou, Ya Liu, Fei Xing, Li Feng, and Feng Pi, with affiliation superscripts and corresponding-author markers.
- Abstract text describing the motivation, method, theory, and experiments.
- Keywords line beginning with **Federated learning**.
- A small `Check for updates` badge at the bottom.

**Direct observations:**
- The excerpt contains prose text only; there are no axes, legends, plotted series, panels, microscopy features, or tabular data.
- The abstract states that cloud-based LLM APIs lack accessible parameters and gradients, making prompt optimization costly.
- It identifies in-context learning as useful but limited by access to high-quality, shareable data.
- It connects federated learning with privacy-preserving collaborative optimization.
- It introduces **AsynDBT** as an asynchronous distributed bilevel tuning algorithm that optimizes both in-context learning samples and prompt fragments using LLM feedback.

**Interpretation connected to the paper:**
- This page establishes the paper’s main contribution: an asynchronous federated/bilevel approach intended to improve efficient in-context learning for large language models under privacy, heterogeneity, and straggler constraints.
- The image serves as bibliographic and introductory context rather than evidence for experimental results.


# **OPEN AsynDBT: asynchronous distributed bilevel tuning for efficient in-context learning with large language models** 

**Hui Ma**<sup>**1**</sup> **, Shaoyu Dou**<sup>**2**</sup> **, Ya Liu**<sup>**3**</sup> **, Fei Xing**<sup>**4**</sup> **, Li Feng**<sup>**5**</sup> **& Feng Pi**<sup>**1,6**</sup> 

**With the rapid development of large language models (LLMs), an increasing number of applications leverage cloud-based LLM APIs to reduce usage costs. However, since cloud-based models’ parameters and gradients are agnostic, users have to manually or use heuristic algorithms to adjust prompts for intervening LLM outputs, which requiring costly optimization procedures. In-context learning (ICL) has recently emerged as a promising paradigm that enables LLMs to adapt to new tasks using examples provided within the input, eliminating the need for parameter updates. Nevertheless, the advancement of ICL is often hindered by the lack of high-quality data, which is often sensitive and different to share. Federated learning (FL) offers a potential solution by enabling collaborative training of distributed LLMs while preserving data privacy. Despite this issues, previous FL approaches that incorporate ICL have struggled with severe straggler problems and challenges associated with heterogeneous non-identically data. To address these problems, we propose an asynchronous distributed bilevel tuning (AsynDBT) algorithm that optimizes both in-context learning samples and prompt fragments based on the feedback from the LLM, thereby enhancing downstream task performance. Benefiting from its distributed architecture, AsynDBT provides privacy protection and adaptability to heterogeneous computing environments. Furthermore, we present a theoretical analysis establishing the convergence guarantees of the proposed algorithm. Extensive experiments conducted on multiple benchmark datasets demonstrate the effectiveness and efficiency of AsynDBT.** 

**Keywords** Federated learning, In-context learning, Bilevel optimization, Large language models 

The emergence of large language models (LLMs) has introduced a revolutionary solution to meet the growing demand for advanced intelligent services<sup>1</sup> . Unlike traditional deep neural networks, LLMs are trained on massive and diverse datasets and contain billions of parameters. This enables them not only to perform logical reasoning and complex thinking but also to excel across a wide range of natural language processing tasks, including text generation, classification, machine translation, and question answering<sup>2,3</sup> . As the scale of LLMs has grown to encompass hundreds of billions of parameters, local deployment has become increasingly impractical. Consequently, cloud-based deployment accessed via application programming interfaces (APIs) has . gradually become the dominant approach, providing users with efficient and flexible interaction capabilities<sup>4</sup> Nevertheless, the training and maintenance costs of LLMs remain extremely high. Therefore, designing and implementing LLMs that achieve both efficient training and strong generalization performance across diverse downstream tasks continues to pose a critical research challenge. 

A practical solution for improving LLM performance on downstream tasks is in-context learning (ICL)<sup>5</sup> . Unlike conventional approaches that require fine-tuning or updating model weights, ICL enables models to learn and generalize to novel tasks by providing labeled context examples (demonstrations) alongside instruction prompts. Moreover, although prior studies have shown that in-context samples can influence LLM performance on downstream tasks<sup>6</sup> , the underlying mechanisms remain largely unexplored. Recent studies<sup>7–9</sup> suggest that 

1Xinjiang Key Laboratory of Intelligent Computing and Smart Applications, School of Software, Xinjiang University, Urumqi 830091, China.<sup>2</sup> the Department of Computer Science and Technology, Tongji University, Shanghai 201800, China.<sup>3</sup> School of Information Science and Engineering, Zaozhuang University, Zaozhuang 277160, China.<sup>4</sup> Xinjiang University, College of Geography and Remote Sensing Sciences, Urumqi 830046, China.<sup>5</sup> The Hochschule BielefeldUniversity of Applied Sciences and Arts, Bielefeld, Germany.<sup>6</sup> Xinjiang General Station of Exit and Entry Frontier Inspection, Urumqi, China.<sup></sup> email: liuya@uzz.edu.cn; xingfei@xju.edu.cn 

**Scientific Reports** |         (2026) 16:9381 

1 

| https://doi.org/10.1038/s41598-026-39582-5 

www.nature.com/scientificreports/ 

ICL can be interpreted from a meta-learning perspective, in which pre-trained LLMs act as meta-optimizers and in-context samples are used to compute the meta-gradient<sup>10</sup> . Motivated by this, we posit a hierarchical relationship between demonstration selection and instruction prompt editing. Nevertheless, systematic research on applying bilevel optimization to model and analyze the in-context learning process remains in its infancy. 

The downstream task performance of LLM agents based on ICL strongly depends on the quality of the provided demonstrations. In real-world applications, however, obtaining high-quality demonstration samples poses numerous challenges, including the need for domain expertise, the high cost of manual annotation, data privacy concerns, client-specific restrictions, and the limited availability of suitable examples. These challenges significantly limit the potential of ICL methods to enhance LLMs performance. To mitigate these issues, federated learning (FL) has emerged as a promising solution<sup>11</sup> , enabling collaborative model training on a central server without direct access to client data. Recently, several studies have explored integrating FL with ICL<sup>12,13</sup> . Nonetheless, most of these methods rely on synchronous distributed algorithms, which often suffer from the “straggler problem,” thereby impeding scalability and overall efficiency. 

Furthermore, in the context of FL with ICL, it is particularly vulnerable to malicious participants who may inject low-quality or adversarial samples into the pool of in-context learning examples. This form of data poisoning poses a significant risk of compromising the global optimization process. To address such threats, recent studies have introduced efficient federated learning frameworks designed to mitigate the impact of malicious workers while providing theoretical robustness guarantees<sup>14–16</sup> . For instance, Jiang et al.<sup>14</sup> proposed a global model recovery method utilizing selective information storage and adaptive model rollback. Similarly, our prior work<sup>16</sup> demonstrated the efficacy of regularization techniques in enhancing the robustness of deep learning models. Building on these foundations, a critical challenge addressed in this study is the design and implementation of robust aggregation techniques tailored to enhance the model’s resilience against data poisoning attacks within the FL with ICL paradigm. 

To address the aforementioned challenges, this study proposes an asynchronous bilevel ICL framework based on federated learning, which comprises multiple workers holding private data and a central parameter server that coordinates their collaboration. _Then_ , we formulate ICL as a bilevel programming problem, where the upperlevel objective focuses on the selection of in-context samples, and the lower-level objective adjusts fragments of the prompt. _Besides_ , we design an asynchronous distributed algorithm that incorporates the lower-level optimization as a constraint on the upper-level optimization. By approximating the feasible region of the lowerlevel problem with polyhedral constraints, the bilevel formulation is transformed into a single-level optimization problem, thereby facilitating efficient distributed computation. _Furthermore_ , we incorporate a regularizationbased robust optimization mechanism to enhance the model’s resilience against data poison attacks. The main contributions of this study can be summarized as follows: 

- We propose a novel bilevel black-box learning framework that captures the hierarchical nature of prompt tuning via integrating prompt editing with in-context sample selection. To the best of our knowledge, this work represents the first attempt to establish a bilevel in-context learning framework. 

- We design an asynchronous distributed bilevel tuning algorithm, **AsynDBT** , to address the distributed bilevel black-box optimization problem. As far as we know, it is the first approach to consider the impact of device heterogeneity and the network straggler issue within the federated in-context learning framework. We also provide a theoretical analysis of the convergence properties of AsynDBT. 

- We validate the effectiveness of the proposed AsynDBT through extensive experiments on multiple benchmark datasets, demonstrating its superiority over several state-of-the-art prompt tuning methods in terms of downstream task performance and computational efficiency. Furthermore, we highlight its practical applicability in 5G AIOps, where our method achieves an accuracy improvement of nearly 10% compared with baseline models. 

## **Related work** 

### **Prompt tuning** 

For the black-box discrete prompt tuning problem explored in this paper, there are two main categories of approaches. The first category relies on the reasoning capabilities of LLMs, which are directly used to summarize the reasons for wrong reasoning and tuning the prompt. OPRO<sup>17</sup> develops two LLM-based agents: one for scoring the optimized prompt fragment and another for generating a new prompt based on historical scores. The tuning of the prompt fragment involves multiple interactions between the above two agents. The APO<sup>18</sup> employs semantic gradient descent for prompt tuning. it analyzes the reasons for incorrect answers by querying the LLM, treating the obtained analysis as the “semantic gradient”. Then, LLM generates new prompts based on the opposite of the semantic gradient and selects the most effective one through bandit selection. Like APO,<sup>19</sup> queries LLM to summarize the reasons for incorrect responses, and then adds the generated summary to the original prompt. 

The second category employs parametric models to generate prompts. The parameters are learned based on the feedback of LLM. AutomateCoT<sup>20</sup> , a two-stage method for generating chain-of-thought (CoT) for specific tasks. Initially, it creates a CoT pool using manually written or LLM-generated CoTs, then evaluates each candidate’s reasoning results using the LLM. Following this, it filters out ineffective CoTs and optimizes a categorical distribution parameter to select the most helpful and suitable CoT. Similarly, BDPL<sup>21</sup> optimizes the parameters of a categorical distribution for generating a prompt fragment attached to the original prompt. RLprompt<sup>22</sup> employs an LLM with fixed parameters and a trainable MLP as a policy network, and optimizes its parameters based on the feedback from the black-box LLM. However, prompt tuning methods often suffer from overfitting, as they require updating a large number of parameters with limited data. 

**Scientific Reports** |         (2026) 16:9381 

2 

| https://doi.org/10.1038/s41598-026-39582-5 

www.nature.com/scientificreports/ 

### **Demonstration selection** 

In generally, demonstration selection methods generally fall into two categories: supervised and unsupervised approaches<sup>5</sup> . 

Supervised demonstration selection methods aim to retrieve entire demonstration sets to model interrelationships between examples. For instance, Li et al.<sup>23</sup> introduced a unified retriever that selects demonstrations across different tasks. Mahankali et al.<sup>24</sup> proposed a model-adaptive method that uses LLMs to predict unlabeled data, assigning an uncertainty score to each instance. By contrast, unsupervised demonstration selection algorithms are heuristic, or directly generate demonstrations by identififying the nearest neighbors of input instances. For example, Liu et al.<sup>25</sup> employed a pre-trained encoder to embed both test samples and candidate demonstrations as vectors, then selects the K nearest neighbors as in-context examples for each test instance. Levy et al.<sup>26</sup> proposed Cover-LS, which removes one of two demonstrations if they are semantically similar. In addition, using output scores of LLMs as unsupervised metrics has shown effectiveness in demonstration selection<sup>27,28</sup> . Particularly, Kim et al.<sup>29</sup> generates in-context samples directly with LLMs, while Wu et al.<sup>28</sup> selected the best subset permutation of kNN examples based on the code length for data transmission. 

Most investigated methods treat prompt tuning and in-context sample selection as separate processes, seldom optimizing them jointly. AutoCoT<sup>30</sup> is the only method that heuristically implements joint optimization. Whereas, we recognize the natural hierarchical structure between the prompt and the in-context samples, which motivates us to model the ICL problem as bilevel programming and propose an asynchronous distributed optimization algorithm, AsynDBT. To the best of our knowledge, AsynDBT is the first distributed algorithm that jointly considers both prompt editing and in-context sample selection with theoretical convergence guarantees. 

## **Distributed bilevel in-context learning Problem formulation** 

A prompt equipped with ICL can be represented as the combination of ICL content and a test query, i.e. [ _ft_ 1( S, [I; T]); _ft_ 2( X _q_ , [I; T]), where I is the task instruction, T is a fragment appended to the task instruction to be optimized, S represents a set of in-context samples, X _q_ is the query sample. _ft_ 1( _·, ·_ ) and _ft_ 2( _·, ·_ ) are used to concatenate their input into ICL content and query content respectively. [ _·_ ; _·_ ] denotes the concatenation. We <u>provide the following example with colors corresponding to the parameters in the formulas.</u> 

Question: Is the sentiment of “I am happy” positive or negative? Note: .... Answer: positive Question: Is the sentiment of “I am angry” positive or negative? Note: .... Answer: negative Question: Is the sentiment of “I am hungry” positive or negative? Note: .... Answer: 

In this paper, we take the _U_ class classification task<sup>31</sup> as an example and denote the training set with labels as _S_ = _S_ 1 _∪· · · ∪SU ∪SQ_ , where _Su_ = _{sj_ = (X _j, yj_ ); _j_ = 1 _, · · · , |Su|}_ , representing the training set of class _u, u_ = 1 _, · · · , U_ . The number of samples in each category is _V_ , i.e. _|Su|_ = _V_ . In general, I is fixed, X _q_ is sampled from a fixed set _SQ_ . We intervene in the output of LLM by adjusting T and S. The following assumptions are made in this paper: 

- Let T = [ _t_ 1; _· · ·_ ; _tM_ ] = [ _V_ [ _j_ 1]; _· · ·_ ; _V_ [ _jM_ ]] , where _V_ is a fixed vocabulary set<sup>21</sup> , _|V|_ = _N_ , and _V_ [ _ji_ ] denotes the _ji_ th word in _V_ . We assume that each word in T is independent of each other and sampled from different categorical distributions, i.e. _ji ∼ Cat_ (p _i_ ) _,_ p _i ∈_ R<sup>_N_</sup> . Correspondingly, we denote the random variable obeying the distribution _Cat_ (p _i_ ) as _Ji_ . 

- We select one sample from each category of labeled samples as in-context samples. Let S = _{s_ 1 _, · · · , sU }_ = _{S_ 1[ _k_ 1] _, ..., SU_ [ _kU_ ] _}_ , and each demonstration is independently sampled from _S_ 1 _, · · · , SU_ , i.e. _ki ∼ Cat_ (q _i_ ) _,_ q _i ∈_ R<sup>_V_</sup> . Denote the random variable obeying the distribution _Cat_ (q _i_ ) as _Ki_ . 

To simplify the subsequent equations, the output of the black-box LLM _fLLM_ ([ _ft_ 1(S _,_ [I; T]) _, ft_ 2(X _q,_ [I; T])]) is abbreviated as _fLLM_ (T _,_ S _,_ X _q_ ). When considering the classification task, the cross-entropy loss can be written as, 


![](P029_images/P029.pdf-0003-12.png)


**Scientific Reports** |         (2026) 16:9381 

3 

| https://doi.org/10.1038/s41598-026-39582-5 

www.nature.com/scientificreports/ 

min E _K_ 1 _,··· ,KU_ [ _Lce_ (p<sup>_⋆_</sup> _i_<sup>(</sup><sup>_K_1</sup><sup>_, · · ·, KU_);</sup><sup>_J_1</sup><sup>_, · · ·, JM, K_1</sup><sup>_, · · ·, KU_)]</sup><sup>_,_</sup> s.t. p<sup>_⋆_</sup> _i_<sup>(</sup><sup>_K_1</sup><sup>_, · · ·, KU_) = arg min</sup> E _Ji_ [ _Lce_ (p1 _, · · · ,_ p _M_ ; _J_ 1 _, · · · , JM , K_ 1 _, · · · , KU_ )] _,_ p _i_ 1<sup>_⊤_</sup> p _i_ = 1 _,_ 1<sup>_⊤_</sup> q _i′_ = 1 _,_ (2) 0 _≤ pi,j ≤_ 1 _,_ 0 _≤ qi′,j′ ≤_ 1 _, i_ = 1 _, · · · , M, j_ = 1 _, · · · , N, i_<sup>_′_</sup> = 1 _, · · · , U, j_<sup>_′_</sup> = 1 _, · · · , V,_ var. p1 _, · · · ,_ p _M ,_ q1 _, · · · ,_ q _U ,_ where _pi,j_ is the _j_ th item of p _i_ , _qi′,j′_ is the _j_<sup>_′_</sup> th item of q _i′_ . For a given random variable _Ki, ∀ i ∈_ (1 _, · · · , U_ ), sampled from the distribution parameterized by (q1 _, · · · ,_ q _U_ ), the lower-level problem optimizes p _i_ while treating this realization as fixed. We denote the resulting objective by _g_ (p _i_ ; _K_ 1 _, · · · , KU_ ), and when the dependency on _K_ is clear, we abbreviate it as _g_ (p _i_ ). **ICL with federated learning framework** In this paper, we consider a federated scenario with a parameter server and _R_ heterogeneous workers<sup>32</sup> , which are composed of _Nw_ benign workers and _B_ malicious workers, i.e., _R_ = _Nw_ + _B_ . The malicious workers, as described in<sup>33</sup> , will collude with each other and send arbitrary malicious messages to the server. Additionally, the identity of malicious workers is a priori unknown to the server. Despite the presence of _B_ malicious workers, our objective is to effectively leverage _Nw_ benign local workers for distributed training and obtain a robust global model, where each worker has its own training set as well as corresponding optimization variables. For worker _v_ , denote its _i_ th lower-level optimization variable as p<sup>(</sup> _i_<sup>_v_)</sup> (i.e., the distribution parameter of the _i_ th word in a fragment) and its _i_<sup>_′_</sup> th upper-level optimization variable as q<sup>(</sup> _i_<sup>_′v_) (i.e., the distribution parameter of the</sup><sup>_i′_th</sup> demonstration). We denote all lower and upper-level optimization variables of worker _v_ as _{_ p<sup>(</sup> _i_<sup>_v_)</sup> _}_ and _{_ q<sup>(</sup> _i_<sup>_′v_)</sup><sup>_}_,</sup> respectively, and denote all lower and upper-level variables as _{_ p _i}_ and _{_ q _i′ }_ . Since the distribution of the training dataset varies across workers, and each worker adjusts their in-context samples based only on the feedback from LLM on their local dataset, thus the upper-level optimization variables are not needed to enforce a global consensus. So we only introduce a set of consensus variables _{_ z _i}}_ for the lower-layer variables<sup>34</sup> . Suppose _v_ = 1 _, · · · · · · , Nww_ , the formulation of the prompt tuning in the _distributed_ blackbox setting is given below, min _F_ ( _{_ p<sup>_⋆_</sup> _i_<sup>_}, {_z</sup> _i_<sup>_⋆}, {_q</sup> _i_<sup>_′}_) = ∑</sup><sup>_N_</sup> _v_ =1<sup>_wf_(p</sup> 1<sup>(</sup><sup>_v_)</sup><sup>_⋆_</sup> _, · · · ,_ p<sup>(</sup> _M_<sup>_v_)</sup><sup>_⋆,_q</sup> 1<sup>(</sup><sup>_v_)</sup><sup>_, · · ·,_q(</sup> _U_<sup>_v_))</sup> s.t. _{_ p _i_<sup>(</sup><sup>_v_)</sup><sup>_⋆_</sup> _},_ z<sup>_⋆_</sup> _i_<sup>= arg min</sup> _{_ p<sup>(</sup> _i_<sup>_v_)</sup> _},_ z _i_<sup>_G_(</sup><sup>_{_p(</sup> _i_<sup>_v_)</sup> _},_ z _i_ ) =<sup>∑</sup><sup>_N_</sup> _v_ =1<sup>_wg_(p</sup> _i_<sup>(</sup><sup>_v_)</sup> ) z _i_ = p<sup>(</sup> _i_<sup>_v_)</sup> (3) 1<sup>_⊤_</sup> p<sup>(</sup> _i_<sup>_v_)</sup> = 1 _,_ 1<sup>_⊤_</sup> q<sup>(</sup> _i_<sup>_′v_)</sup> = 1 0 _≤ p_<sup>(</sup> _i,j_<sup>_v_)</sup><sup>_≤_1</sup><sup>_,_0</sup><sup>_≤q_</sup> _i_<sup>(</sup><sup>_′v_</sup> _,j_<sup>)</sup><sup>_′≤_1</sup> var. _{_ p<sup>(</sup> _i_<sup>_v_)</sup> _}, {_ q<sup>(</sup> _i_<sup>_′v_)</sup><sup>_},_z</sup><sup>_i._</sup> **Optimization of distributed black-box bilevel problem** For the _i_ th lower-level variable, we define an estimation function _ϕi_ ( _·_ ) for the solution, that is, _ϕi_ ( _k_ 1 _, · · · , kU_ )arg min {∑ _Nv_ =1 _w_<sup>_g_(p</sup> _i_<sup>(</sup><sup>_v_)</sup> ) : z _i_ = p<sup>(</sup> _i_<sup>_v_)</sup> _, v_ = 1 _, · · · , Nw_ } _,_ (4) _{_ p<sup>(</sup> _i_<sup>_v_)</sup> _},_ z _i_ where the arguments in _ϕi_ ( _·_ ) derive from the full form of _g_ (p<sup>(</sup> _i_<sup>_v_)</sup> ), that is, _g_ (p<sup>(</sup> _i_<sup>_v_)</sup> _, k_ 1 _, · · · , kU_ ). We also define _hi_ ( _k_ 1 _, · · · , kU , {_ p<sup>(</sup> _i_<sup>_v_)</sup> _},_ z _i_ ) = _∥ {_ pz<sup>(</sup> _i_<sup>_v_</sup> _i_<sup>)</sup> _} − ϕ_ ( _k_ 1 _, · · · , kU_ ) _∥_ 1 _._ (5) [ ] Then Eq. (3) can be rewritten by _hi_ ( _·_ ) as min _F_ ( _{_ p _i}, {_ z _i}, {_ q _i′ }_ ) s.t. _hi_ ( _k_ 1 _, · · · , kU , {_ p<sup>(</sup> _i_<sup>_v_)</sup> _},_ z _i_ ) = 0 1<sup>_⊤_</sup> p<sup>(</sup> _i_<sup>_v_)</sup> = 1 _,_ 1<sup>_⊤_</sup> q<sup>(</sup> _i_<sup>_′v_)</sup> = 1 (6) 0 _≤ p_<sup>(</sup> _i,j_<sup>_v_)</sup><sup>_≤_1</sup><sup>_,_0</sup><sup>_≤q_</sup> _i_<sup>(</sup><sup>_′v_</sup> _,j_<sup>)</sup><sup>_′≤_1</sup> var. _{_ p<sup>(</sup> _i_<sup>_v_)</sup> _}, {_ q<sup>(</sup> _i_<sup>_′v_)</sup><sup>_},_z</sup><sup>_i._</sup> 

Since the distribution of the training dataset varies across workers, and each worker adjusts their in-context samples based only on the feedback from LLM on their local dataset, thus the upper-level optimization variables are not needed to enforce a global consensus. So we only introduce a set of consensus variables _{_ z _i}}_ for the lower-layer variables<sup>34</sup> . Suppose _v_ = 1 _, · · · · · · , Nww_ , the formulation of the prompt tuning in the _distributed_ blackbox setting is given below, 

### **Estimation of the** **_i_ th lower-level variables** 

Although the optimization problem Eq. (3) requires the exact solution of Eq. (4), previous research<sup>35,36</sup> has 4 demonstrated that it is sufficient to use an approximation of Eq. ( ) with bilevel optimization. Therefore, in our approach, we estimate the solution using _K_ -step gradient descent. Taking into account the consensus constraint in Eq. (4), the corresponding Lagrangian function of Eq. (4) can be formulated as follows, 

**Scientific Reports** |         (2026) 16:9381 

4 

| https://doi.org/10.1038/s41598-026-39582-5 

www.nature.com/scientificreports/ 

_GP i_ ( _{_ p<sup>(</sup> _i_<sup>_v_)</sup> _},_ z _i, {_ **_ρ_** _i_<sup>(</sup><sup>_v_)</sup> _}_ ) =<sup>∑</sup><sup>_N_</sup> _v_ =1<sup>_w_</sup> _g_ (p<sup>(</sup> _i_<sup>_v_)</sup> ) + **_ρ_** _i_<sup>(</sup><sup>_v_)</sup><sup>_⊤_</sup> (p<sup>(</sup> _i_<sup>_v_)</sup> _−_ z _i_ ) +<sup>_<u>µ</u>_</sup> 2<sup>_∥_p(</sup> _i_<sup>_v_)</sup> _−_ z _i∥_ 2<sup>2</sup> _,_ (7) ( ) where **_ρ_**<sup>(</sup> _i_<sup>_v_)</sup> _∈_ R<sup>_N_</sup> is the Lagrangian dual variable and _µ >_ 0 is the penalty parameter. The procedure for computing the approximate solution of Eq. (4) using _K_ steps gradient descent is as follows. _For worker v_ : In the _k_ + 1th iteration, worker _v_ first updates their local lower-level optimization variables on the local data. p<sup>(</sup> _i_<sup>_v_)</sup><sup>_k_+1</sup> = _projP_ (p _i_<sup>(</sup><sup>_v_)</sup><sup>_k_</sup> _− η_ p( _iv_ ) ( _∇_ p( _iv_ ) _GP i_ ( _{_ p _i_<sup>(</sup><sup>_v_)</sup><sup>_k_</sup> _},_ z<sup>_k_</sup> _i_<sup>_,_</sup><sup>**_ρ_**</sup> _i_<sup>(</sup><sup>_v_)</sup><sup>_k_</sup> ) + _ψ_ sign(z<sup>_k_</sup> _i_<sup>_−_p</sup><sup>_t_</sup> _i_<sup>)</sup> )) _,_ (8) where _ψ_ represents a positive constant. Subsequently, each worker sends its variables p _i_<sup>(</sup><sup>_v_)</sup><sup>_k_+1</sup> _,_ p<sup>(</sup> _i_<sup>_v_)</sup><sup>_k_</sup> to the parameter server. _For the parameter server_ : It updates the consensus and dual variables according to the following equations. z<sup>_k_</sup> _i_<sup>+1</sup> = proj _P_ z<sup>_k_</sup> _i_<sup>_−η_</sup> z _i_  _∇_ z _i GP i_ ( _{_ p<sup>(</sup> _i_<sup>_v_)</sup><sup>_k_+1</sup> _},_ z<sup>_k_</sup> _i_<sup>_,_</sup><sup>**_ρ_**(</sup> _i_<sup>_v_)</sup><sup>_k_</sup> ) + _ψ_<sup>(</sup> ∑ sign(z<sup>_k_</sup> _−_ p<sup>_k_</sup> _i_<sup>+1</sup> ) + ∑ sign(z<sup>_k_</sup> _−_ p<sup>_k_</sup> _j_<sup>+1</sup> )<sup>)</sup>  _,_ (9)   _i∈{_ 1 _,...,Nw } j∈{_ 1 _,...,B}_  **_ρ_**<sup>(</sup> _i_<sup>_v_)</sup><sup>_k_+1</sup> = **_ρ_** _i_<sup>(</sup><sup>_v_)</sup><sup>_k_</sup> + _η_ **_ρ_** ( _iv_ ) _∇_ **_ρ_** ( _iv_ ) _GP i_ ( _{_ p<sup>(</sup> _i_<sup>_v_)</sup><sup>_k_+1</sup> _},_ z<sup>_k_</sup> _i_<sup>+1</sup> _,_ **_ρ_** _i_<sup>(</sup><sup>_v_)</sup><sup>_k_</sup> ) _,_ (10) where the projection x<sup>_′_</sup> = _projP_ (x) guarantees that the parameter z<sup>_′_</sup> is a legitimate distribution parameter. According to<sup>21</sup> , x<sup>_′_</sup> = min(1 _,_ max(0 _,_ x _− v_<sup>_⋆_</sup> 1)) where _v_<sup>_⋆_</sup> = arg min _v_ (1<sup>_⊤_</sup> min(1 _,_ max(0 _,_ x _− v_ 1)) _−_ 1<sup>)</sup> . Thus, after _K_ times of communication, the estimation of the _i_ th lower-level problem is _ϕi_ ( _k_ 1 _, · · · , kU_ ) = [ _{_ p<sup>(</sup> _i_<sup>_v_)</sup><sup>_K_</sup> _},_ z<sup>_K_</sup> _i_<sup>]</sup><sup>_⊤_.</sup> Specifically, the gradient of Eq. (7) with respect to each argument is as follows: _∇_ p( _iv_ ) _GP i_ ( _{_ p<sup>(</sup> _i_<sup>_v_)</sup> _},_ z _i,_ **_ρ_**<sup>(</sup> _i_<sup>_v_)</sup> ) = _∇_ p( _iv_ ) _gv_ (p<sup>(</sup> _i_<sup>_v_)</sup> ) + **_ρ_**<sup>(</sup> _i_<sup>_v_)</sup> + _µ_ (p<sup>(</sup> _i_<sup>_v_)</sup> _−_ z _i_ ) _,_ (11) _Nw ∇_ z _i GP i_ ( _{_ p<sup>(</sup> _i_<sup>_v_)</sup> _},_ z _i,_ **_ρ_**<sup>(</sup> _i_<sup>_v_)</sup> ) = ∑ ( _−_ **_ρ_**<sup>(</sup> _i_<sup>_v_)</sup> + _µ_ (z _i −_ p<sup>(</sup> _i_<sup>_v_)</sup> )) _,_ (12) _v_ =1 _∇_ **_ρ_** ( _iv_ ) _GP i_ ( _{_ p _i_<sup>(</sup><sup>_v_)</sup> _},_ z _i,_ **_ρ_**<sup>(</sup> _i_<sup>_v_)</sup> ) = p<sup>(</sup> _i_<sup>_v_)</sup> _−_ z _i._ (13) **Approximate the feasible region of constraint with cutting-plane** After estimating the solution of the lower-level optimization problem, Eq. (6) can be rewritten as, min _F_ ( _{_ p _i}, {_ z _i}, {_ q _i′ }_ ) s.t. _hi_ ( _k_ 1 _, · · · , kU , {_ p<sup>(</sup> _i_<sup>_v_)</sup> _},_ z _i_ ) _≤ ϵ_ 1<sup>_⊤_</sup> p<sup>(</sup> _i_<sup>_v_)</sup> = 1 _,_ 1<sup>_⊤_</sup> q<sup>(</sup> _i_<sup>_′v_)</sup> = 1 (14) 0 _≤ p_<sup>(</sup> _i,j_<sup>_v_)</sup><sup>_≤_1</sup><sup>_,_0</sup><sup>_≤q_</sup> _i_<sup>(</sup><sup>_′v_</sup> _,j_<sup>)</sup><sup>_′≤_1</sup> var. _{_ p<sup>(</sup> _i_<sup>_v_)</sup> _}, {_ q<sup>(</sup> _i_<sup>_′v_)</sup><sup>_},_z</sup><sup>_i,_</sup> where _ϵ >_ 0 is a constant. _hi_ ( _k_ 1 _, · · · , kU , {_ p<sup>(</sup> _i_<sup>_v_)</sup> _},_ z _i_ ) is a convex function with respect to the _{_ p<sup>(</sup> _i_<sup>_v_)</sup> _}_ and z _i_ . According to Eq. (5), its feasible region can be approximated by a polyhedron enclosed by _L_ cutting planes<sup>37–39</sup> . Noting that the feasible region of _hi_ ( _k_ 1 _, · · · , kU , {_ p<sup>(</sup> _i_<sup>_v_)</sup> _},_ z _i_ ) is _Pi_ , and let _Pi_<sup>_t_represent polyhedron at iteration</sup> _t_ . Then, _Nw Pi_<sup>_t_=</sup><sup>_{_p</sup> _i_<sup>_∈_R</sup><sup>_N|_</sup> ∑ a<sup>_l_</sup> _i_<sup>(</sup><sup>_v_)</sup><sup>_⊤_</sup> p<sup>(</sup> _i_<sup>_v_)</sup> + b<sup>_l_</sup> _i_<sup>_⊤_z</sup> _i_<sup>+</sup><sup>_cl_</sup> _i_<sup>_≤_0;</sup><sup>_l_= 1 :</sup><sup>_|P_</sup> _i_<sup>_t|},_</sup> (15) _v_ =1 where a<sup>_l_</sup> _i_<sup>(</sup><sup>_v_)</sup> _,_ b<sup>_l_</sup> _i_<sup>_∈_R</sup><sup>_N_. Using the above linear constraints in place of the constraints in (14), Eq. (6) can be</sup> reformulated as, min _F_ ( _{_ p _i}, {_ z _i}, {_ q _i′ }_ ) s.t. ∑ _Nv_ =1 _w_<sup>a</sup> _i_<sup>_l_(</sup><sup>_v_)</sup><sup>_⊤_</sup> p<sup>(</sup> _i_<sup>_v_)</sup> + b<sup>_l_</sup> _i_<sup>_⊤_z</sup><sup>_i_+</sup><sup>_cl_</sup> _i_<sup>_≤_0</sup> 1<sup>_⊤_</sup> p<sup>(</sup> _i_<sup>_v_)</sup> = 1 _,_ 1<sup>_⊤_</sup> q<sup>(</sup> _i_<sup>_′v_)</sup> = 1 (16) 0 _≤ p_<sup>(</sup> _i,j_<sup>_v_)</sup><sup>_≤_1</sup><sup>_,_0</sup><sup>_≤q_</sup> _i_<sup>(</sup><sup>_′v_</sup> _,j_<sup>)</sup><sup>_′≤_1</sup> var. _{_ p<sup>(</sup> _i_<sup>_v_)</sup> _}, {_ q<sup>(</sup> _i_<sup>_′v_)</sup><sup>_},_z</sup><sup>_i._</sup> 

**Update the optimization parameters** 

The Lagrangian function for the optimization problem Eq. (16) is given by 

**Scientific Reports** |         (2026) 16:9381 

5 

| https://doi.org/10.1038/s41598-026-39582-5 

www.nature.com/scientificreports/ 


![](P029_images/P029.pdf-0006-01.png)


where we tentatively and informally use variables with subscripts 1 : _n_ to denote the _n_ variables that have subscripts 1 _, · · · , n_ , respectively. We also abbreviate _dj_ 1 _· · · djM_ , _dk_ 1 _· · · dkU_ to _dj_ 1: _M_ and _dk_ 1: _U_ , respectively. 

**Scientific Reports** |         (2026) 16:9381 

6 

| https://doi.org/10.1038/s41598-026-39582-5 

www.nature.com/scientificreports/ 

### **Update the polyhedron** 

As local parameters and consensus variables are continuously updated across workers, additional cutting planes must be incorporated to form a compact feasible region for Eq. (5). To mitigate computational burden, cutting planes with small weights will be removed. 

_Add new cutting plane_ : For a newly updated ( _{_ p<sup>(</sup> _i_<sup>_v_)</sup><sup>_t_+1</sup> _},_ z _i_<sup>_t_+1</sup> ), we first evaluate whether this solution is feasible for the optimization problem Eq. (16). If not, i.e., _hi_ ( _k_ 1 _, · · · , kU , {_ p<sup>(</sup> _i_<sup>_v_)</sup><sup>_t_+1</sup> _},_ z _i_<sup>_t_+1</sup> ) _> ϵ_ . Then we need to generate a new cutting plane for separating the points ( _{_ p<sup>(</sup> _i_<sup>_v_)</sup><sup>_t_+1</sup> _},_ z _i_<sup>_t_+1</sup> ) outside the _Pi_ . The newly generated cutting plane with index _l_ needs to satisfy, { ∑∑ _NvNv_ =1=1 _ww_<sup>aa</sup> _i_<sup>_l_</sup> _i_<sup>_l_((</sup><sup>_vv_))</sup><sup>_⊤⊤_</sup> pp<sup>(</sup> _i_<sup>(</sup> _i_<sup>_vv_))</sup><sup>_t_</sup> +<sup>+1</sup> b+<sup>_l_</sup> _i_<sup>_⊤_</sup> b<sup>z</sup><sup>_l_</sup> _i_<sup>_i⊤_+z</sup><sup>_t_</sup> _i_<sup>_c_+1</sup><sup>_l_</sup> _i_<sup>_≤_</sup> +<sup>0;</sup> _c_<sup>_l_</sup> _i_<sup>_∀>_( 0</sup><sup>_{_p</sup><sup>_._(</sup> _i_<sup>_v_)</sup> _},_ z _i_ ) _∈Pi_ (28) Since the _hi_ ( _k_ 1 _, · · · , kU , {_ p<sup>(</sup> _i_<sup>_v_)</sup> _},_ z _i_ ) is convex with respect to _{_ p<sup>(</sup> _i_<sup>_v_)</sup> _},_ z _i_ , then we have, _hi_ ( _k_ 1 _, · · · , kU , {_ p<sup>(</sup> _i_<sup>_v_)</sup> _},_ z _i_ ) _≥ hi_ ( _k_ 1 _, · · · , kU , {_ p<sup>(</sup> _i_<sup>_v_)</sup><sup>_t_+1</sup> _},_ z<sup>_t_</sup> _i_<sup>+1</sup> ) +  _∂h∂hii_ (( _kk_ 11 _,,······ ,k ,kUU∂ , ,_ p _{{_<sup>(</sup> _i_ pp<sup>_v_(</sup> _<u>i</u>_<sup>(</sup> _<u>i</u>_<sup>)</sup><sup>_vv_))</sup><sup>_tt_+1+1</sup> _}},,_ zz<sup>_t_</sup> _<u>i</u>_<sup>_t_</sup> _<u>i</u>_<sup>+1+1</sup> )) _}_  _⊤_ ([ _{_ pz<sup>(</sup> _i_<sup>_v_</sup> _i_<sup>)</sup> _}_ ] _−_ [ _{_ p<sup>(</sup> _i_ z<sup>_vt_</sup> _i_<sup>)+1</sup><sup>_t_+1</sup> _}_ ]) _._ (29) <sup>_{_</sup> _∂_ z _i_  In summary, the newly added cutting plane satisfies, _⊤ ∂hi_ ( _k_ 1 _,··· ,kU ,{_ p<sup>(</sup> _<u>i</u>_<sup>_v_)</sup><sup>_t_+1</sup> _},_ z<sup>_t_</sup> _<u>i</u>_<sup>+1</sup> ) _} hi_ ( _k_ 1 _, · · · , kU , {_ p<sup>(</sup> _i_<sup>_v_)</sup><sup>_t_+1</sup> _},_ z<sup>_t_</sup> _i_<sup>+1</sup> ) +  _∂hi_ ( _k_ 1 _,··· ,kU∂ ,_ p _{_<sup>(</sup> _i_ p<sup>_v_(</sup> _<u>i</u>_<sup>)</sup><sup>_v_)</sup><sup>_t_+1</sup> _},_ z<sup>_t_</sup> _<u>i</u>_<sup>+1</sup> )  ([ _{_ pz<sup>(</sup> _i_<sup>_v_</sup> _i_<sup>)</sup> _}_ ] _−_ [ _{_ p<sup>(</sup> _i_ z<sup>_vt_</sup> _i_<sup>)+1</sup><sup>_t_+1</sup> _}_ ]) _≤ ϵ._ (30) <sup>_{_</sup> _∂_ z _i_  Combine Eq. (28) with Eq. (29), the parameters in the equation<sup>∑</sup><sup>_N_</sup> _v_ =1<sup>_w_a</sup> _i_<sup>_l_(</sup><sup>_v_)</sup><sup>_⊤_</sup> p<sup>(</sup> _i_<sup>_v_)</sup> + b<sup>_l_</sup> _i_<sup>_⊤_z</sup><sup>_i_+</sup><sup>_cl_</sup> _i_<sup>_≤_0 are</sup> calculated as follows, a<sup>_l_</sup> _i_<sup>(</sup><sup>_v_)</sup> =<sup>_∂hi_</sup><sup><u>(</u></sup><sup>_k_1</sup><sup>_<u>, · · ·, kU,{</u>_</sup><sup><u>p(</u></sup> _<u>i</u>_<sup>_v_)</sup><sup>_t_+1</sup> _<u>},</u>_ z<sup>_t_</sup> _<u>i</u>_<sup>+1</sup> <u>)</u> _,_ (31) _∂_ p<sup>(</sup> _i_<sup>_v_)</sup> b<sup>_l_</sup> _i_<sup>=</sup><sup>_∂hi_</sup><sup><u>(</u></sup><sup>_k_1</sup><sup>_<u>, · · ·, kU,{</u>_</sup><sup><u>p(</u></sup> _<u>i</u>_<sup>_v_)</sup><sup>_t_+1</sup> _<u>},</u>_ z<sup>_t_</sup> _<u>i</u>_<sup>+1</sup> <u>)</u> _,_ (32) _∂_ z _i ⊤ ∂hi_ ( _k_ 1 _,··· ,kU ,{_ p<sup>(</sup> _<u>i</u>_<sup>_v_)</sup><sup>_t_+1</sup> _},_ z<sup>_t_</sup> _<u>i</u>_<sup>+1</sup> ) _c_<sup>_l_</sup> _i_<sup>=</sup><sup>_h_</sup> _i_<sup>(</sup><sup>_k_</sup> 1<sup>_, · · ·, k_</sup> _U_<sup>_, {_p(</sup> _i_<sup>_v_)</sup><sup>_t_+1</sup> _},_ z<sup>_t_</sup> _i_<sup>+1</sup> ) _−_ { _∂_ p<sup>(</sup> _i_<sup>_v_)</sup> } _{_ p<sup>(</sup> _i_<sup>_v_)</sup><sup>_t_+1</sup> _} ._ (33) _∂hi_ ( _k_ 1 _,··· ,kU ,{_ p<sup>(</sup> _<u>i</u>_<sup>_v_)</sup><sup>_t_+1</sup> _},_ z<sup>_t_</sup> _<u>i</u>_<sup>+1</sup> ) [ z<sup>_t_</sup> _i_<sup>+1</sup> ]  _∂_ z _i_  

_Delete invalid cutting planes_ : When the dual variable _λl_ of the _l_ th cutting plane is less than a given threshold before and after the _t_ + 1th update, then the cutting plane _l_ will no longer be used for subsequent calculations. 

### **The proposed AsynDBT approach** 

To address the straggler problem in federated learning, we propose _AsynDBT_ , an asynchronous algorithm that enables the parameter server to communicate with only a subset of available workers per update, bypassing the need to wait for results from all workers. 

We define a set of hyperparameters for the AsynDBT. The polyhedron is updated every _δ_ step, _τ_ is the maximum update interval for each worker, and _γ_ denotes the threshold for determining the invalidity of the cutting plane. Note that we denote the last communication time of worker _v_ by _k_<sup>ˆ(</sup><sup>_v_)</sup> . Pseudo-code for asynBDT is shown in Algorithm 1. 

**Scientific Reports** |         (2026) 16:9381 

7 

| https://doi.org/10.1038/s41598-026-39582-5 

www.nature.com/scientificreports/ 


![](P029_images/P029.pdf-0008-01.png)


**Algorithm 1** . The proposed AsynDBT algorithm 

### **Proof of Convergence** 

_Theorem 1_ (Convergence) As the cutting plane continuously adds to the polyhedron, the optimal objective value in the approximation problem Eq. (16) converges monotonically. 

**Proof** Let _Ri_ denote the feasible region of Eq. (14) and _Pi_ represent the polyhedral approximation of Eq. (16)’s feasible region. The polyhedron _Pi_<sup>_nδ_obtained at iteration</sup><sup>_nδ_contains the point (p(</sup> _i_<sup>_v_)</sup><sup>_nδ_</sup> _,_ z<sup>_nδ_</sup> _i_<sup>), implying the</sup> nested containment relationship: _Pi_<sup>0</sup><sup>_⊇P_</sup> _i_<sup>_δ⊇· · · ⊇P_</sup> _i_<sup>_nδ_</sup> _⊇ Ri_ . For iteration _nδ_ , denote the optimal objective value of Eq. (16) as _F_ (p<sup>_nδ⋆_</sup> _i ,_ z _i_<sup>_nδ⋆_</sup> _,_ q _i_<sup>_′nδ⋆_</sup> ), then the following inequality holds, ( _{_ p<sup>0</sup> _i_<sup>_⋆}, {_z</sup> _i_<sup>0</sup><sup>_⋆}{_q0</sup> _i_<sup>_′⋆}_)</sup><sup>_≤F_(</sup><sup>_{_p</sup><sup>_δ⋆_</sup> _i_<sup>_}, {_z</sup> _i_<sup>_δ⋆}{_q</sup><sup>_δ⋆_</sup> _i_<sup>_′}_)</sup><sup>_≤· · · ≤F_(</sup><sup>_{_p</sup><sup>_nδ⋆_</sup> _i }, {_ z<sup>_nδ⋆_</sup> _i }{_ q<sup>_nδ⋆_</sup> _i_<sup>_′_</sup> _}_ ) _._ (34) Let the optimal objective value of Eq. (14) be _F_<sup>_⋆_</sup> , then we have _⋆_ 0 _⋆ /F_ ( _{_ p _i_<sup>_}, {_z</sup> _i_<sup>0</sup><sup>_⋆}{_q0</sup> _i_<sup>_′⋆}_)</sup><sup>_≥F ⋆/F_(</sup><sup>_{_p</sup><sup>_δ⋆_</sup> _i_<sup>_}, {_z</sup> _i_<sup>_δ⋆}{_q</sup><sup>_δ⋆_</sup> _i_<sup>_′}_)</sup><sup>_≥· · · ≥F ⋆/F_(</sup><sup>_{_p</sup><sup>_nδ⋆_</sup> _i }, {_ z<sup>_nδ⋆_</sup> _i }{_ q<sup>_nδ⋆_</sup> _i_<sup>_′_</sup> _}_ ) _≥ β._ (35) From the above non-increasing sequence, it can be seen that when _n →∞_ , the optimal objective value of Eq. (16) converges to _β, β ≥_ 1. □ **Assumption 1** (Lipschitz continuous) We assume that _Lp_ has _L_<sup>_′_</sup> -Lipschitz continuous gradients ( _L >_ 0). For any x and x<sup>_′_</sup> , it satisfies _∥∇Lp_ (x) _−∇Lp_ (x<sup>_′_</sup> ) _∥≤ L_<sup>_′_</sup> _∥_ x _−_ x<sup>_′_</sup> _∥_ (36) **Assumption 2** (Boundedness) The optimization variables are bounded, i.e. _∥_ p<sup>(</sup> _i_<sup>_v_)</sup> _∥_<sup>2</sup> _≤ α_ 1, _∥_ z _i∥_<sup>2</sup> _≤ α_ 1, _∥_ q<sup>(</sup> _i_<sup>_′v_)</sup><sup>_∥_2</sup><sup>_≤α_2,</sup><sup>_∥λl_</sup> _i_<sup>_∥_2</sup><sup>_≤α_3), and before obtaining the</sup><sup>_ϵ_-stationary point the variables in param-</sup> eter server satisfy that _∥_ z<sup>_t_</sup> _i_<sup>+1</sup> _−_ z<sup>_t_</sup> _i_<sup>_∥_2 + ∑</sup> _l_<sup>_∥λ_</sup> _i_<sup>_lt_+1</sup> _− λ_<sup>_lt_</sup> _i_<sup>_∥_2</sup><sup>_≥ξ_, where</sup><sup>_ξ>_0 is a relative small constant. The</sup> change of the variables in the parameter server is upper bounded within _τ_ iterations, i.e., _∥_ z<sup>_t_</sup> _i_<sup>_−_z</sup><sup>_t_</sup> _i_<sup>_−k_</sup> _∥_<sup>2</sup> _≤ τξk_ 1, ∑ _l_<sup>_∥λ_</sup> _i_<sup>_lt−λlt_</sup> _i_<sup>_−k_</sup> _∥_<sup>2</sup> _≤ τξk_ 1, where 1 _< k < τ_ and _k_ 1 _>_ 0 is a constant. _Theorem 2_ (Iteration Complexity) Let Assumptions 1 and 2 hold. Then, the iteration complexity of our proposed AsynDBT to obtain _ϵ_ -stationary point is bounded by, _− T_ ( _ϵ_ ) _∼ O_ max {(<sup>4</sup><sup>_Mα_</sup> _ηλ_<sup>23</sup> +<sup>4</sup><sup>_Nα_</sup> _η_ **_θ_**<sup>24)2</sup> _ϵ_<sup>12</sup><sup>_,_(4(</sup><sup>_d_7 +</sup><sup>_<u>η</u>_</sup><sup>**_<u>θ</u>_**</sup><sup><u>(</u></sup><sup>_N−_</sup> <u>2</u><sup>_S_</sup><sup><u>)</u></sup><sup>_L_2</sup> <u>)(</u> _ϵ d_ + _kdτ_ <u>(</u> _τ −_ 1)) _d_ 6 + ( _T_ 1 + 2) <u>12 )</u><sup>2})</sup> _,_ ( such that _||∇GG_<sup>_t_</sup> _||_<sup>2</sup> _≤ ϵ_ . 8 

such that _||∇GG_<sup>_t_</sup> _||_<sup>2</sup> _≤ ϵ_ . 

**Scientific Reports** |         (2026) 16:9381 

| https://doi.org/10.1038/s41598-026-39582-5 

www.nature.com/scientificreports/ 

|**Datasets**|**Templates**|
|---|---|
|5G|In 5G network, Whether [WORD1] related to [WORD2]? Some contextual information: [TEXT]. Respond ONLY with “Yes” or “No”. Note: [VAR].|
|COLA|Is this sentence [SENTENCE1] grammatically correct? Respond ONLY with “Yes” or “No”. Note: [VAR].|
|SST2|How is the sentiment of the sentence [SENTENCE1]? Respond ONLY with “Great” or “Terrible”. Note: [VAR].|
|MRPC|Whether sentence [SENTENCE1] and sentence [SENTENCE2] are semantically the same? Respond ONLY with “Yes” or “No”. Note: [VAR].|
|QQP|Whether sentence [SENTENCE1] and sentence [SENTENCE2] are paraphrased from each other? Respond ONLY with “Yes” or “No”. Note: [VAR].|
|QNLI|Whether sentence [SENTENCE1] and sentence [SENTENCE2] have semantic entailment relations? Respond ONLY with “Yes” or “No”. Note: [VAR].|



**Table 1** . The prompt templates for all the datasets. 

|**Datasets**|**Number o**|**f a samples**|
|---|---|---|
|5G|Yes: 99|No: 101|
|COLA|Yes: 141|No: 59|
|SST2|Great: 99|Terrible: 101|
|MRPC|Yes: 135|No: 65|
|QQP|Yes: 89|No: 111|
|QNLI|Yes: 108|No: 92|



**Table 2** . The details of all the test datasets. 

We provide a detailed derivation process in the Appendix<sup>1</sup> , which consists of the following four steps. First, we derive Lemma 1 (see Appendix C) based on Assumption 1 and Assumption 2. Next, by combining the CauchySchwarz inequality and Lemma 1, we obtain Lemma 2 (see Appendix D). Furthermore, leveraging Lemma 1 along with Lemma 2, we derive Lemma 3 (see Appendix E). Finally, by integrating the above three lemmas, we formally derive Theorem 2 (see Appendix F) for our proposed AsynDBT. 

According to Theorem 2, the upper bound on the iteration complexity of AsynDBT for achieving an _ϵ_ -stationary point is _O_ (1 _/ϵ_<sup>2</sup> ). The iteration complexity is affected by several parameters in AsynDBT, such as _ϵ_ , _S_ , _N_ . _S_ denotes the number of active workers in each iteration and _N_ represents the number of workers in federated learning framework. When a smaller _ϵ_ is chosen, the iteration complexity increases. On the other hand, increasing the number of active workers _S_ in each iteration reduces the iteration complexity. However, as the number of clients _N_ grows, the iteration complexity rises exponentially. 

## **Experiments** 

To assess the performance of AsynDBT in domain-specific and Natural Language Understanding (NLU) tasks, we conducted experiments on six classification datasets. 

### **Datasets description** 

The first dataset focuses on the task of terminological relationship recognition in the 5G network. In our preliminary work, we created a 5G terminology knowledge graph based on 3GPP protocol texts. This graph labels terminology pairs as either `relevant` or `irrelevant` , and provides a corresponding segment of 3GPP protocol text for each pair to assist with reasoning. For NLU tasks, we utilize five datasets from the GLUE benchmark<sup>41</sup> . These datasets cover a range of tasks: COLA and SST-2 for single-sentence classification, MRPC and QQP for syntactic comparison, and QNLI for inference. Table 1 provides an overview of the prompt templates used for all datasets in our experiments. In these templates, the placeholder [VAR] indicates the prompt fragment that is subject to optimization. 

For the 5G dataset, which has distinct training, validation, and test sets, 10 samples per class were randomly selected from the training and validation sets, and 200 samples were randomly chosen from the original test set. For each GLUE benchmark dataset, we randomly selected 10 samples per class from the original training set to create a reduced training set. We randomly chose 10 samples per class from the original labeled validation set for validation and 200 samples randomly drawn from the remaining validation set for test. Additionally, we randomly selected 50 samples from the remaining original training set for each class to form the ICL training set. Table 2 shows the details for all the test datasets. 

### **Baselines** 

- **RoBERTa**<sup>42</sup> : We convert all sentences in a test sample into vectors using pre-trained RoBERTa<sup>2</sup> . These vectors are summed and fed into a single-layer MLP classifier, which is trained using cross-entropy loss. 

- **ManualPrompt (MP)** : The prompt template is as described in Table 1, but does not include the `Note` and its aftermath. 

> 1 https://github.com/maggiemh/AsynDBT 

> 2 https://huggingface.co/roberta-base 

**Scientific Reports** |         (2026) 16:9381 

9 

| https://doi.org/10.1038/s41598-026-39582-5 

www.nature.com/scientificreports/ 

- **Zero-shot CoT**<sup>43</sup> : Based on the ManualPrompt method, we append the text `Let’s think step by` step, first output your analysis, and then output the final answer to each test sample. 

- **Random ICL** : This method involves randomly selecting samples from the ICL training set as in-context samples, ensuring only one sample per class. Note that the demonstrations are randomly selected in each run. 

- **KATE**<sup>25</sup> : This approach first maps the test sample and ICL training set into vectors using a pre-trained RoBERTa. The 5 nearest neighbors of the test sample in the vector space are selected as in-context samples. 

- **BDPL**<sup>21</sup> : In this method, a prompt fragment is learned using the policy gradient approach and then appended to the original prompt. 

- **AdaICL**<sup>24</sup> : It is a model-adaptive method that uses LLMs to predict unlabeled data, assigning an uncertainty score to each instance. 

Besides the proposed AsynDBT approach, its centralized version, cenDBT, also participates in the comparison. cenDBT optimizes the parameters only on the server, so there is no need to optimize the consensus variable _{_ z _i}_ and the corresponding dual variable _{_ **_ρ_**<sup>(</sup> _i_<sup>_v_)</sup> _}_ . 

### **Experimental details** 

_Hyperparameter Setting_ : The API of LLM service is supported by qwen-max<sup>3</sup> . Both BDPL and the proposed method are trained using the Adam optimizer with a learning rate of 10<sup>_−_4</sup> . Specifically, the Lagrangian dual variable of the proposed method has a learning rate of 10<sup>_−_1</sup> . The learning rate of RoBERTa is 2 _×_ 10<sup>_−_5</sup> . The maximum of epochs for all the algorithms is 500 and the early stopping technique is used on the validation set. In parameter settings in (2) are _M_ = 75, _N_ = 100 and _V_ = 50. The value of _U_ is determined by the dataset. the setting of BDPL is consistent with the proposed method. Besides, we use accuracy to evaluate the classification performance of different models. 

_Experimental Environment_ : We conduct all experiments on a Linux server with four 12 GB GPUs with NVIDIA TITAN X (Pascal). Besides, we use the deep learning framework of Pytorch 1.6.0 with the programming language of python 3.7. 

## **Experimental results** 

### **The performance of classification** 

Table 3 presents the average accuracy and standard deviations of the compared methods over five independent runs, with AsynDBT reporting the average performance of three workers. The optimal and suboptimal performance on each dataset is bolded and underlined, respectively. By ranking the experimental results of each model, we use the average ranking to measure the prediction performance of different models. The output strategy of LLM is set as greedy sampling. 

The classification task on the 5G dataset is especifically challenging because it involves two acronyms that are uncommon in general corpora and have not been covered by LLM fine-tuning. The auxiliary text for each pair provides only contextual information, not explicit interpretations. Compared with the optimal baseline, our proposed method improves the accuracy by nearly 10%. Owing to the isomorphism in data distribution, cenDBT generally outperforms AsynDBT. However, AsynDBT still achieves competitive results relative to the centralized algorithm and finally reaches a suboptimal performance. This highlights both the effectiveness and computational efficiency of the proposed algorithms. 

For the GLUE benchmark, our algorithm achieves optimality or suboptimality on almost all dataset. For instance, on MRPC and QNLI datasets, cenDBT attains the highest accuracy, while AsynDBT achieves the next best performance. Among the baselines, BDPL is a prompt-based learning method that guides the model to generate more interpretable outputs by designing specific prompt statements. It optimizes the parameters of a categorical distribution to generate the prompt fragment appended to the original prompt. However, it requires labeled data to optimize the prompt vector, and its initialization can significantly impact experimental results. In contrast, our proposed method adapts to new tasks without parameter updates, saving computational resources 

3 https://tongyi.aliyun.com 

||**5G**|**COLA**|**SST2**|**MRPC**|**QQP**|**QNLI**|**Average Rank**|
|---|---|---|---|---|---|---|---|
|Roberta<sup>42</sup>|52.80 1.68|68.70 2.49|85.10 4.63|65.00 3.46|55.90 1.64|51.60 3.31|8.67|
|Manual Prompt|58.00|83.00|93.50|77.00|81.00|84.00|6.17|
|Zero-shot CoT<sup>43</sup>|78.50|84.50|90.50|76.00|73.50|79.00|6.50|
|RandomICL|69.70 0.97|71.00 1.70|72.80 1.75|78.50 0.71|82.30 1.35|87.80 0.57|5.17|
|KATE<sup>25</sup>|68.10 1.19|70.90 0.55|69.50 1.54|77.90 0.42|79.00 2.03|87.40 1.43|6.83|
|BDPL<sup>21</sup>|67.20 1.35|**86.70**0.27|94.300.27|80.40 0.42|83.200.27|85.80 0.27|3.67|
|AdaICL<sup>24</sup>|78.43 1.03|84.95 0.18|91.53 0.21|81.29 0.33|81.85 0.25|87.58 0.23|3.83|
|_cenDBT(ours)_|**87.21**1.30|84.92 0.65|**94.40**0.74|**83.51**0.59|**83.31**0.21|**88.52**0.77|1.50|
|_AsynDBT(ours)_|85.051.01|85.070.41|92.98 0.69|82.931.39|81.95 0.59|87.790.43|2.67|



**Table 3** . The overall results of different models. 

**Scientific Reports** |         (2026) 16:9381 

10 

| https://doi.org/10.1038/s41598-026-39582-5 

www.nature.com/scientificreports/ 


![](P029_images/P029.pdf-0011-01.png)


**Figure 1** . Comparison of time consumption. 


![](P029_images/P029.pdf-0011-03.png)


**(a)** Accuracy score 

**(b)** Cross-entropy loss 

**Figure 2** . **a** Accuracy and **b** Cross-entropy loss on the 5G dataset. 

and making it suitable for resource-constrained environments, such as edge devices with limited computing power. Furthermore, compared to the heuristic KATE shown in Table 3, the proposed method consistently refines demonstrations via LLM feedback, substantially improving downstream task accuracy. This finding further highlights the benefit of using diverse in-context samples for downstream tasks and underscores the adaptability of our algorithm in various NLU scenarios. 

### **Computational efficiency** 

We demonstrate the computational efficiency gains of asynchronous distributed optimization through numerical results. As shown in Fig. 1, AsynDBT and cenDBT are compared on their training times for 500 epochs across all datasets. The results indicate that, on all six datasets, it is evident that AsynDBT reduces training time by nearly 40% while maintaining task performance comparable to cenDBT, which clearly highlights the superior computational efficiency of AsynDBT. 

Besides, Figs. 2, 3, 4, 5, 6 and 7 illustrate the test accuracy and the cross-entropy loss curves over iterations for both AsynDBT and cenDBT on all datasets. In each figure, the solid blue line represents the mean performance of cenDBT, with the blue shading indicating its standard deviation. Similarly, the solid red line and shading correspond to the mean and standard deviation for AsynDBT. 

Take Fig. 2 as an example, both cenDBT and AsynDBT gradually stabilize during training, with their crossentropy loss converging to around 0.5. This convergence indicates that both algorithms reach a stable state where their outputs are consistent and reliable over time. Similar findings can be drawn from experimental results on other datasets. 

### **Ablation study** 

To evaluate the effect of optimizing in-context samples and prompt fragments on downstream task performance, we conduct ablation studies comparing accuracy across multiple datasets under different configurations: (a) No 

**Scientific Reports** |         (2026) 16:9381 

11 

| https://doi.org/10.1038/s41598-026-39582-5 

www.nature.com/scientificreports/ 


![](P029_images/P029.pdf-0012-01.png)


**Figure 3** . **a** Accuracy and **b** Cross-entropy loss on the COLA dataset. 


![](P029_images/P029.pdf-0012-03.png)



![](P029_images/P029.pdf-0012-04.png)



![](P029_images/P029.pdf-0012-05.png)


**Figure 4** . **a** Accuracy and **b** Cross-entropy loss on the SST2 dataset. 


![](P029_images/P029.pdf-0012-07.png)



![](P029_images/P029.pdf-0012-08.png)


**Figure 5** . **a** Accuracy and **b** Cross-entropy loss on the MRPC dataset. 

**Scientific Reports** |         (2026) 16:9381 

12 

| https://doi.org/10.1038/s41598-026-39582-5 

www.nature.com/scientificreports/ 


![](P029_images/P029.pdf-0013-01.png)


**(a)** Accuracy score 

**(b)** Cross-entropy loss 

**Figure 6** . **a** Accuracy and **b** Cross-entropy loss on the QQP dataset. 


![](P029_images/P029.pdf-0013-05.png)



![](P029_images/P029.pdf-0013-06.png)


**Figure 7** . **a** Accuracy and **b** Cross-entropy loss on the QNLI dataset. 

||**5G**|**COLA**|**SST2**|**MRPC**|**QQP**|**QNLI**|
|---|---|---|---|---|---|---|
|cenDBT|**89**|**85.5**|**95.5**|**84.5**|**83.5**|**89.5**|
|w.opt.ICL|84|86.5|94.5|80.5|82|88|
|w.opt.prompt|60|84.5|93.0|77|79|84|
|Plain|58|83|93.5|77|81|84|



**Table 4** . The results of ablation study. 

optimization content (plain); (b) Only the prompt fragment optimized (w. opt. prompt); (c) Only the in-context samples optimized (w. opt. ICL). In each setting, all optimized components are derived from the best results of the cenDBT algorithm for a specific run. Table 4 presents the numerical results. 

The findings show that optimizing the prompt fragment leads to a modest performance boost, whereas selecting appropriate demonstration markedly enhances performance and is key to achieving good results. Interestingly, on COLA dataset, cenDBT’s overall performance is slightly lower than that of the w. opt. ICL setting. Similarly, on QQP dataset, performance when optimizing the prompt fragment is actually lower than the plain setting. This may result from excessively long prompt fragments that negatively affect the LLM’s ability to process semantic information. 

**Scientific Reports** |         (2026) 16:9381 

13 

| https://doi.org/10.1038/s41598-026-39582-5 

www.nature.com/scientificreports/ 

## **Conclusion** 

In summary, this paper presents AsynDBT, a novel asynchronous distributed bilevel tuning framework designed to jointly optimize demonstration selection and prompt editing for efficient In-Context Learning (ICL). To the best of our knowledge, this work represents the first attempt to formulate ICL optimization as a bilevel black-box problem. Besides, we developed an efficient asynchronous distributed algorithm that effectively preserves data privacy and mitigates the “straggler issue” in heterogeneous environments. Furthermore, we provide a theoretical proof for the convergence of our proposed algorithm. The effectiveness and efficiency of our proposed AsynDBT are validated on six public benchmark datasets. 

Despite its current strengths, AsynDBT remains limited by its reliance on static training datasets, which may lead to hallucination issues in domain-specific scenarios. Recent studies, such as the work on TrumorGPT<sup>44</sup> , have demonstrated that Graph-Based Retrieval-Augmented Generation (GraphRAG) can effectively mitigate the hallucination issues common in LLMs by leveraging updated semantic knowledge graphs. Inspired by these findings, our future work will explore the integration of a GraphRAG within our distributed bilevel optimization framework, specifically targeting high-stakes technical fields such as network operation and maintenance. Specifically, the upper-level objective will adaptively optimize retrieval parameters to ensure highfidelity knowledge extraction from semantic graphs, while the lower-level task will perform ICL-based semantic reasoning grounded in retrieved factual triples. This integration will empower our algorithm transcend the limitations of static data, allowing it to adapt to the rapid information flow of specialized domains while ensuring factual consistency and high-fidelity reasoning. 

## **Data availability** 

The datasets used and/or analyzed during the current study available from the corresponding author on reasonable request. 

Received: 17 November 2025; Accepted: 5 February 2026 


![](P029_images/P029.pdf-0014-07.png)

### Figure analysis

The image is not a scientific data visualization; it appears to be publication metadata from the article page. The only readable content is the line: **“Published online: 17 February 2026.”**

Direct observations:
- No axes, legends, panels, data series, experimental results, or schematic components are present.
- The content is a single bibliographic/publication-status statement.

Connection to the surrounding paper text:
- The surrounding text includes the article conclusion, data availability statement, received/accepted dates, and references.
- This snippet complements that metadata by giving the online publication date, which follows the accepted date of 5 February 2026.

Interpretation:
- The image is useful for citation and publication timeline tracking, but it does not contribute scientific evidence, methods, results, or conceptual explanation.


## **References** 

1. Zhou, H. _et al._ Large language model (LLM) for telecommunications: A comprehensive survey on principles, key techniques, and opportunities. _IEEE Communications Surveys & Tutorials_ (2024). 

2. Liu, Y., Yang, K., Zhu, Y., Yang, K. & Zhao, H. Argus: Federated non-convex bilevel learning over 6 g space-air-ground integrated network. _IEEE Transactions on Network Science and Engineering_ (2025). 

3. Liu, Y. & Yang, K. Asynchronous decentralized federated anomaly detection for 6g networks. _IEEE Transactions on Cognitive Communications and Networking_ (2025). 

4. Ding, Y., Niu, C. & Wu, e. a., Fan. Enhancing on-device LLM inference with historical cloud-based LLM interactions. In _Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining_ , 597–608 (2024). 

5. Dong, Q. _et al._ A survey on in-context learning. In _Proceedings of the Conference on Empirical Methods in Natural Language Processing_ , 1107–1128, https://doi.org/10.18653/v1/2024.emnlp-main.64 (2024). 

6. Min, S. _et al._ Rethinking the role of demonstrations: What makes in-context learning work? In _Proceedings of the Conference on Empirical Methods in Natural Language Processing_ (2022). 

7. Dai, D. _et al._ Why can GPT learn in-context? language models secretly perform gradient descent as meta-optimizers. In _Findings of the Association for Computational Linguistics_ , 4005–4019, https://doi.org/10.18653/v1/2023.findings-acl.247 (2023). 

8. Shiguang, W., Yaqing, W. & Quanming, Y. Why in-context learning models are good few-shot learners? In _ICLR_ (2025). 9. Li, G. _et al._ Meta in-context learning makes large language models better zero and few-shot relation extractors. In _Proceedings of the Thirty-Third International Joint Conference on Artificial Intelligence_ , IJCAI ’24, https://doi.org/10.24963/ijcai.2024/702 (2024). 

10. Genewein, T. _et al._ Understanding prompt tuning and in-context learning via meta-learning (2025). arXiv:2505.17010. 11. Huang, H. _et al._ Contextfl: Context-aware federated learning by estimating the training and reporting phases of mobile clients. In _IEEE 42nd International Conference on Distributed Computing Systems (ICDCS)_ , 570–580,  h t t p s : / / d o i . o r g / 1 0 . 1 1 0 9 / I C D C S 5 4 8 6 0 . 2 0 2 2 . 0 0 0 6 1 (2022). 

12. Ruhan, W. _et al._ Federated in-context learning: Iterative refinement for improved answer quality. In _ICML_ (2025). 

13. Wu, P., Li, K., Nan, J. & Fangxin, W. Federated in-context LLM agent learning. _arXiv preprint_ arXiv:2412.08054 (2024). 

14. Jiang, Y., Shen, J., Liu, Z., Tan, C. W. & Lam, K.-Y. Toward efficient and certified recovery from poisoning attacks in federated learning. _IEEE Trans. Inform. Forens. Sec._ **20** , 2632–2647 (2025). 

15. Zhang, Z., Cao, X., Jia, J. & Gong, N. Z. Fldetector: Defending federated learning against model poisoning attacks via detecting malicious clients. In _Proceedings of the 28th ACM SIGKDD Conference on Knowledge Discovery and Data Mining_ , 2545–2555 (2022). 

16. Ma, H., Yang, K. & Jiao, Y. Cellular traffic prediction via byzantine-robust asynchronous federated learning. _IEEE Transactions on Network Science and Engineering_ (2025). 

17. Yang, C. _et al._ Large language models as optimizers. In _International Conference on Learning Representations_ (2024). 

18. Pryzant, R. _et al._ Automatic prompt optimization with “gradient descent” and beam search. In _Proceedings of the Conference on Empirical Methods in Natural Language Processing_ , 7957–7968, https://doi.org/10.18653/v1/2023.emnlp-main.494 (2023). 

19. Sun, H. _et al._ Autohint: Automatic prompt optimization with hint generation. In _The 29th ACM SIGKDD Conference on Knowledge Discovery and Data Mining Workshop_ (2023). 

20. Shum, K., Diao, S. & Zhang, T. Automatic prompt augmentation and selection with chain-of-thought from labeled data. In _Proceedings of the Conference on Empirical Methods in Natural Language Processing_ , 12113–12139,  h t t p s : / / d o i . o r g / 1 0 . 1 8 6 5 3 / v 1 / 2 0 2 3 . fi  n d i n g s - e m n l p . 8 1 1 (2023). 

21. Diao, S. _et al._ Black-box prompt learning for pre-trained language models. _Transactions on Machine Learning Research_ (2022). 

22. Deng, M. _et al._ RLPrompt: Optimizing discrete text prompts with reinforcement learning. In _Proceedings of the Conference on Empirical Methods in Natural Language Processing_ , 3369–3391 (2022). 

23. Xiaonan, L. _et al._ Unified demonstration retriever for incontext learning. In _Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics_ , 4644–4668 (2023). 

24. Mavromatis, C. _et al._ Which examples to annotate for in-context learning? towards effective and efficient selection (2023). arXiv:2310.20046. 

25. Liu, J. _et al._ What makes good in-context examples for GPT-3? In _Proceedings of Deep Learning Inside Out: The 3rd Workshop on Knowledge Extraction and Integration for Deep Learning Architectures_ , 100–114 (2022). 

**Scientific Reports** |         (2026) 16:9381 | https://doi.org/10.1038/s41598-026-39582-5 

14 

www.nature.com/scientificreports/ 

26. Levy, I., Bogin, B. & Berant, J. Diverse demonstrations improve in-context compositional generalization. In _Annual Meeting of the Association for Computational Linguistics_ (2023). 

27. Li, X. & Qiu, X. Finding support examples for in-context learning. In _Proceedings of the Conference on Empirical Methods in Natural Language Processing_ , 6219–6235,  h t t p s : / / d o i . o r g / 1 0 . 1 8 6 5 3 / v 1 / 2 0 2 3 . fi  n d i n g s - e m n l p . 4 1 1 (2023). 

28. Zhiyong, W., Yaoxiang, W., Jiacheng, Y. & Lingpeng, K. Self-adaptive in-context learning: An information compression perspective for incontext example selection and ordering. In _In Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics_ (2023). 

29. Kim, H. J. _et al._ Self-generated in-context learning: Leveraging auto-regressive language models as a demonstration generator. In _Annual Conference of the Nations of the Americas Chapter of the Association for Computational Linguistics Workshop_ (2022). 

30. Zhang, Z., Zhang, A., Li, M. & Smola, A. Automatic chain of thought prompting in large language models. In _The Eleventh International Conference on Learning Representations_ (2023). 

31. Sun, T., Shao, Y., Qian, H., Huang, X. & Qiu, X. Black-box tuning for language-model-as-a-service. In _International Conference on Machine Learning_ , 20841–20855 (2022). 

32. Singhal, S. P. _et al._ Asynchronous distributed-memory parallel algorithms for influence maximization. In _Proceedings of the International Conference for High Performance Computing, Networking, Storage, and Analysis_ (2024). 

33. Zhu, H. & Ling, Q. Bridging differential privacy and Byzantine-robustness via model aggregation. In _Int. Joint Conf. Artif. Intell._ , 2427–2433, https://doi.org/10.24963/IJCAI.2022/337 (2022). 

34. Pan, Z. & Cannon, M. Asynchronous admm via a data exchange server. _IEEE Trans. Control Netw. Syst._ **11** , 1631–1643.  h t t p s : / / d o i . o r g / 1 0 . 1 1 0 9 / T C N S . 2 0 2 4 . 3 3 5 4 8 4 0 (2024). 

35. Li, J., Huang, F. & Huang, H. Local stochastic bilevel optimization with momentum-based variance reduction. _arXiv preprint_ arXiv:2205.01608 (2022). 

36. Chen, X., Xiao, T. & Balasubramanian, K. Optimal algorithms for stochastic bilevel optimization under relaxed smoothness conditions. _J. Mach. Learn. Res._ **25** , 1–51 (2024). 

37. Irmai, J. & Andres, B. A state-of-the-art cutting plane algorithm for clique partitioning. In _Pattern Recognition: 46th DAGM German Conference_ , 21–36, https://doi.org/10.1007/978-3-031-85181-0_2 (2025). 

38. Jiao, Y., Yang, K. & Song, D. Distributed distributionally robust optimization with non-convex objectives. In _Proc. Adv. Neural Inf. Proces. Syst._ 35, 7987-7999 (2022). 

39. Jiao, Y., Yang, K., Wu, T., Song, D. & Jian, C. _Asynchronous distributed bilevel optimization_ (In Proc. Int. Conf. Learn, Represent, 2023). 

40. Xu, Z., Zhang, H., Xu, Y. & Lan, G. A unified single-loop alternating gradient projection algorithm for nonconvex–concave and convex–nonconcave minimax problems. _Math. Program._ 1–72 (2023). 

41. Wang, A. _et al._ Glue: A multi-task benchmark and analysis platform for natural language understanding. In _International Conference on Learning Representations_ (2018). 

42. Liu, Y. _et al._ RoBERTa: A robustly optimized BERT pretraining approach. _CoRR_ **abs/1907.11692** (2019). arXiv:1907.11692. 

43. Kojima, T., Gu, S. S., Reid, M., Matsuo, Y. & Iwasawa, Y. Large language models are zero-shot reasoners. _Adv. Neural Inform. Process. Syst._ **35** , 22199–22213 (2022). 

44. Hang, C. N., Yu, P.-D. & Tan, C. W. TrumorGPT: Graph-based retrieval-augmented large language model for fact-checking. _IEEE Trans. Artif. Intell._ **6** , 3148–3162 (2025). 

## **Author contributions** 

Hui Ma: Writing – Review and Editing, Conceptualization; Shaoyu Dou: Writing – Original Draft, Software, Methodology; Ya Liu: Experimental Analysis; Fei Xing: Supervision; Li Feng: Validation, Data curation; Feng Pi: Supervision. All authors reviewed the manuscript. 

## **Funding** 

This work was supported by the Tianchi Talents - Young Doctor Program (5105250183m), Science and Technology Program of Xinjiang Uyghur Autonomous Region (2024B03028, 2025B04051), Regional Fund of the National Natural Science Foundation of China (202512120005). 

## **Declarations** 

## **Competing interests** 

The authors declare no competing interests. 

## **Additional information** 

**Supplementary Information** The online version contains supplementary material available at  h t t p s : / / d o i . o r g / 1 0 . 1 0 3 8 / s 4 1 5 9 8 - 0 2 6 - 3 9 5 8 2 - 5 . 

**Correspondence** and requests for materials should be addressed to Y.L. or F.X. 

**Reprints and permissions information** is available at www.nature.com/reprints. 

**Publisher’s note** Springer Nature remains neutral with regard to jurisdictional claims in published maps and institutional affiliations. 

**Scientific Reports** |         (2026) 16:9381 

15 

| https://doi.org/10.1038/s41598-026-39582-5 

www.nature.com/scientificreports/ 

**Open Access** This article is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License, which permits any non-commercial use, sharing, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons licence, and indicate if you modified the licensed material. You do not have permission under this licence to share adapted material derived from this article or parts of it. The images or other third party material in this article are included in the article’s Creative Commons licence, unless indicated otherwise in a credit line to the material. If material is not included in the article’s Creative Commons licence and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder. To view a copy of this licence, visit  h t t p : / / c r e a t i v e c o m m o n s . o r g / l i c e n s e s / b y - n c - n d / 4 . 0 / . 

© The Author(s) 2026 

**Scientific Reports** |         (2026) 16:9381 

16 

| https://doi.org/10.1038/s41598-026-39582-5 

