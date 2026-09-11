Preprint. 

# FE DPOB: SAMPLE-EFFICIENT FEDERATED PROMPT OPTIMIZATION VIA BANDITS 

**Pingchen Lu**<sup>1</sup><sup>_,_2</sup><sup>_∗_</sup> **, Zhi Hong**<sup>1</sup><sup>_,_2</sup><sup>_∗_</sup> **, Zhiwei Shang**<sup>1</sup> **, Zhiyong Wang**<sup>3</sup> **, Yikun Ban**<sup>4</sup> **, Yao Shu**<sup>5</sup> **, Min Zhang**<sup>6</sup> **, Shuang Qiu**<sup>7</sup> **, Zhongxiang Dai**<sup>1</sup><sup>_†_</sup> 

1The Chinese University of Hong Kong, Shenzhen, 2South China University of Technology, 

3University of Edinburgh, 4Beihang University, 

5The Hong Kong University of Science and Technology (Guangzhou), 

6East China Normal University, 7City University of Hong Kong 

## ABSTRACT 

The performance of large language models (LLMs) is highly sensitive to the input prompt, making prompt optimization a critical task. However, real-world application is hindered by three major challenges: (1) the black-box nature of powerful proprietary LLMs, (2) the need for high sample efficiency due to query costs, and (3) the desire for privacy-preserving collaboration among multiple users. To address these challenges simultaneously, we introduce a novel framework for sample-efficient federated prompt optimization based on multi-armed bandits (MABs). The MAB framework is uniquely suited for this problem as it is (1) inherently a black-box optimization method, (2) practically sample-efficient, and (3) enables collaborative learning with theoretically guaranteed benefit from more participating agents. We first propose the _Federated Prompt Optimization via Bandits_ (FedPOB) algorithm, a federated variant of the Linear UCB algorithm, where agents collaborate by sharing model parameters instead of raw data. We then extend our approach to the practical setting of comparative user feedback by introducing _FedPOB with Preference Feedback_ (FedPOB-Pref), an efficient algorithm based on federated dueling bandits. Extensive experiments demonstrate that both FedPOB and FedPOB-Pref significantly outperform existing baselines and that their performance consistently improves as more agents participate in the collaboration, validating the effectiveness of our federated approach. 

## 1 INTRODUCTION 

Large language models (LLMs) have achieved impressive performance in a variety of real-world applications (Guo et al., 2025). However, the performance of LLMs has been shown to be highly sensitive to the input _prompt_ (Zhou et al., 2023; Lin et al., 2024b). Consequently, _prompt optimization_ , in which we aim to find the best prompt for a task, has emerged as a critical research area. Despite its growing popularity, the widespread real-world adoption of prompt optimization is still hindered by three important challenges. 

The first challenge is **black-box access** . Some of the most powerful LLMs, such as ChatGPT and Gemini (OpenAI, 2023b; Team et al., 2023), are proprietary, black-box models that are only accessible via API queries. This limited access creates an immense challenge to prompt optimization. The second challenge is **sample efficiency** . Since querying powerful LLMs is often costly in both time and financial resources, it is of paramount importance to develop methods that can identify the optimal prompt for a given task using a small number of interactions. The third challenge is enabling **collaboration** among multiple users. As LLMs become more widely adopted, a natural and important question arises: how can multiple users, each with their own prompt optimization tasks, collaborate to accelerate their progress? A key constraint in such a collaborative setting is user privacy, as participants are typically unwilling to share their proprietary data, such as the history of tested prompts and their corresponding performance scores. This scenario naturally aligns 

> _∗_ Equal contribution. 

> _†_ Corresponding author. Correspondence to daizhongxiang@cuhk.edu.cn. 

1 

Preprint. 


![](P011_images/P011.pdf-0002-01.png)



![](P011_images/P011.pdf-0002-02.png)



![](P011_images/P011.pdf-0002-03.png)



![](P011_images/P011.pdf-0002-04.png)



![](P011_images/P011.pdf-0002-05.png)



![](P011_images/P011.pdf-0002-06.png)



![](P011_images/P011.pdf-0002-07.png)



![](P011_images/P011.pdf-0002-08.png)



![](P011_images/P011.pdf-0002-09.png)



![](P011_images/P011.pdf-0002-10.png)



![](P011_images/P011.pdf-0002-11.png)



![](P011_images/P011.pdf-0002-12.png)



![](P011_images/P011.pdf-0002-13.png)



![](P011_images/P011.pdf-0002-14.png)



![](P011_images/P011.pdf-0002-15.png)

### Figure analysis

**Purpose.** This overview explains the information flow in two proposed federated prompt optimization frameworks: FedPOB for direct scalar score feedback and FedPOB-Pref for pairwise preference feedback.

**Main components and layout.**

- **Left block: Federated Aggregation.** A central server maintains a global model and communicates with multiple agents labeled Agent 1, Agent 2, ..., Agent n. Each agent is shown with a local model and a prompt space.
- A small legend indicates two communication directions:
  - Local parameters are sent from agents toward the server.
  - Global parameters are sent from the server back to agents.
- This block visually emphasizes that collaboration occurs through parameter exchange rather than sharing raw prompt histories or private task data.

**Top-right block: FedPOB (Local).**

- A single local agent selects or represents prompts using a local model and prompt space.
- The example task asks: `What is the moon?`
- The selected prompt is labeled `Prompt: Poetically`.
- The prompt is sent to an LLM, which produces the response: `The moon is a silver lamp`.
- An evaluator assigns a direct numeric score, shown as `Score: 0.8`.
- The score feedback is returned to the agent, closing the local optimization loop.

**Bottom-right block: FedPOB-Pref (Local).**

- A local agent compares two prompts for the same task, shown with the example query `Explain gravity`.
- Two candidate prompts are displayed:
  - `Prompt 1: Scientifically`
  - `Prompt 2: Vividly`
- Both prompts are sent through the LLM, generating two responses:
  - `Response 1: Gravity pulls masses together`
  - `Response 2: Gravity makes things fall`
- A user or preference evaluator chooses between the two responses; the illustrated preference says `I really like response 2`.
- Preference feedback is sent back to the agent, forming a pairwise-comparison optimization loop rather than a scalar-scoring loop.

**Direct visual observations.**

- FedPOB uses a single prompt-response-evaluation path with explicit numerical scoring.
- FedPOB-Pref uses two prompt-response paths and receives a relative preference instead of an absolute score.
- Both local procedures are embedded in a larger federated system where local models interact with a central global model through parameter exchange.
- The dashed boxes separate the federated aggregation layer from the two local algorithm variants.

**Interpretation.**

- The figure illustrates that both methods are designed for black-box LLM settings: the LLM is queried, but its internal parameters are not accessed.
- The federated aggregation block supports the paper's privacy-preserving collaboration claim: agents can benefit from shared model parameters without exposing raw local data, prompts, or feedback records.
- The two right-side workflows distinguish the feedback assumptions of the proposed algorithms: FedPOB assumes direct score feedback is available, whereas FedPOB-Pref addresses settings where only comparative user preferences are available.

**Connection to surrounding text.**

- The surrounding introduction frames three challenges: black-box LLM access, sample efficiency, and privacy-preserving collaboration across users.
- The diagram provides the conceptual overview for the proposed multi-armed-bandit-based federated prompt optimization approach described in the text.
- It visually supports the later explanation that FedPOB builds on federated LinUCB-style parameter aggregation, while FedPOB-Pref adapts the framework to preference feedback using pairwise comparisons.


Figure 1: An overview of our proposed federated prompt optimization frameworks. FedPOB handles direct score feedback, while FedPOB-Pref is designed for pairwise preference feedback. 

with the principles of _federated learning_ (FL) (Kairouz et al., 2019; McMahan et al., 2017), where distributed agents collaborate on their machine learning tasks without exposing their raw data. 

To tackle the combined challenges of black-box access, sample efficiency and privacy-preserving collaboration, we propose a new class of federated prompt optimization algorithms built upon the _multi-armed bandit_ (MAB) framework (Lattimore & Szepesv´ari, 2020). MABs are exceptionally well-suited for this problem for three main reasons. First, MAB algorithms do not require gradient information and are inherently **black-box optimization methods** . Second, they are designed to efficiently balance the exploration-exploitation trade-off, enabling them to solve complex black-box optimization problems in a **sample-efficient** manner, a property that has been successfully leveraged in recent work on prompt optimization (Lin et al., 2024b; Wu et al., 2024). Thirdly, federated MAB algorithms (Shi & Shen, 2021; Dubey & Pentland, 2020; Dai et al., 2023) provide strong theoretical guarantees, ensuring that **performance improves as more agents participate in the collaboration** (Wang et al., 2020). 

Our first contribution is the _<u>Federated Prompt Optimization via Bandits</u>_ (FedPOB) algorithm. This method is based on a federated variant of the classic Linear Upper Confidence Bound (LinUCB) algorithm (Abbasi-Yadkori et al., 2011; Wang et al., 2020). In our FedPOB algorithm, each agent utilizes a pre-trained embedding model to represent the prompts and a linear model to predict their performance. Collaboration is achieved by having agents periodically exchange and aggregate their LinUCB parameters, thereby learning from the collective experience of all agents without requiring them to share any sensitive raw data. Importantly, thanks to the solid theoretical guarantees of the federated LinUCB algorithm (Wang et al., 2020), the performance of our FedPOB algorithm is theoretically guaranteed to improve with a larger number of collaborating agents. 

In addition, we consider the highly practical setting of prompt optimization with _preference feedback_ , where explicit performance scores are unavailable and we are only able to observe relative preference feedback (e.g., the user prefers the response from prompt A than that from prompt B). This problem was recently introduced by Lin et al. (2024a) to address scenarios where user feedback is inherently comparative. To enable sample-efficient federated prompt optimization in this novel setting, we introduce our second algorithm, _<u>FedPOB</u> with Preference Feedback_ (FedPOB-Pref). This algorithm is a practical adaptation and modification of the federated linear dueling bandit framework proposed by Huang et al. (2025). Specifically, our FedPOB-Pref algorithm significantly reduces the communication complexity of the methods from Huang et al. (2025) while maintaining the strong empirical performance. An overview of both FedPOB and FedPOB-Pref is illustrated in Fig. 1. 

We conduct extensive experiments to validate our proposed methods. The results demonstrate that both FedPOB and FedPOB-Pref achieve considerably better performance than the previous base- 

2 

Preprint. 

line methods in various tasks. Furthermore, we empirically verify that the performance of our algorithms consistently improves as the number of participating agents increases, highlighting the benefits of our collaborative approach. In summary, our key contributions are as follows: 

- We propose FedPOB, a novel algorithm for sample-efficient federated prompt optimization that enables multiple agents to collaborate on finding the best prompts without sharing their raw data. 

- We extend our algorithm to the practical setting of preference-based feedback by introducing the FedPOB-Pref algorithm, which is based on federated linear dueling bandits. 

- We conduct extensive experiments to validate our approach, demonstrating that our algorithms significantly outperform existing baselines and scale effectively with more agents. 

## 2 PROBLEM SETTING 

**Prompt Optimization.** We address the problem of black-box prompt optimization, where the objective is to find an optimal prompt _p_ that maximizes the performance of a black-box LLM on a given task D = (X _,_ Y). The task consists of a set of queries X = _{xk}_ and their corresponding ground-truth answers Y = _{yk}_ . Since the internal parameters of the black-box LLMs (e.g., GPT4o-mini) are inaccessible and only API queries are allowed, we model the performance of the LLM via an external score function. Specifically, we define 


![](P011_images/P011.pdf-0003-07.png)


in which _m_ is a metric function that compares the model response LLM( _p, x_ ) induced by the prompt _p_ with the ground-truth answer _y_ and provides a score _s_ ( _p |_ D). The optimization target is then formulated as 


![](P011_images/P011.pdf-0003-09.png)


where P denotes the space of all possible prompts. 

**Federated Prompt Optimization.** We extend the black-box prompt optimization problem to the federated setting, which involves multiple agents. We consider a scenario with a set of _N >_ 1 agents, denoted by A, who all aim to solve the same task D. To account for agent heterogeneity, we allow each agent _a ∈_ A to have its own prompt space denoted as P _a_ . This increases the generality of our setting by allowing each user to define a prompt space uniquely suited to their own preferences. Furthermore, each agent can generate its local prompt space P _a_ using existing techniques (Zhou et al., 2023). As a result, the federated prompt optimization problem can be expressed as follows: 


![](P011_images/P011.pdf-0003-12.png)

### Figure analysis

The extracted fragments are three displayed mathematical formulations from the problem-setting section, not a chart or visual diagram.

**Equation (1): prompt score definition**

\[
s(p\mid \mathbb{D}) = \mathbb{E}_{(x,y)\in \mathbb{D}}\left[m(\mathrm{LLM}(p,x),y)\right]
\]

- **Direct observation:** The equation defines the score of a prompt \(p\) on a task dataset \(\mathbb{D}\).
- **Components:**
  - \(p\): prompt being evaluated.
  - \(\mathbb{D}\): task dataset of input-output pairs \((x,y)\).
  - \(\mathrm{LLM}(p,x)\): response produced by the black-box language model when using prompt \(p\) on query \(x\).
  - \(m(\cdot,y)\): external metric comparing the model response with ground-truth answer \(y\).
  - The expectation averages this metric over the task distribution or dataset.
- **Interpretation:** This formalizes black-box prompt evaluation through an external scoring function rather than access to model internals.

**Equation (2): single-agent prompt optimization objective**

\[
p^* = \arg\max_{p\in \mathbb{P}} s(p\mid \mathbb{D})
\]

- **Direct observation:** The optimal prompt \(p^*\) is the prompt in the prompt space \(\mathbb{P}\) that maximizes the score defined in Equation (1).
- **Relationship to Equation (1):** Equation (2) uses \(s(p\mid\mathbb{D})\) as the objective function.
- **Interpretation:** The paper frames prompt optimization as a black-box search over candidate prompts.

**Equation (3): federated prompt optimization objective**

\[
p_a^* = \arg\max_{p_a\in \mathbb{P}_a}\mathbb{E}_{(x,y)\in \mathbb{D}}\left[m(\mathrm{LLM}(p_a,x),y)\right],\quad \forall a\in \mathbb{A}
\]

- **Direct observation:** Each agent \(a\) seeks its own optimal prompt \(p_a^*\) from its own prompt space \(\mathbb{P}_a\).
- **Components:**
  - \(\mathbb{A}\): set of participating agents.
  - \(\mathbb{P}_a\): agent-specific prompt space.
  - \(p_a\): candidate prompt for agent \(a\).
  - The same task dataset \(\mathbb{D}\), model-response function, and metric function from Equation (1) are reused.
- **Interpretation:** This extends the single-agent prompt-search objective to a federated setting where agents may have heterogeneous prompt spaces but share the same task goal.

**Connection to surrounding text**

The equations support the paper’s transition from ordinary black-box prompt optimization to federated prompt optimization. The surrounding text states that agents collaborate to improve sample efficiency without sharing raw histories of tested prompts and scores. These equations provide the mathematical basis for that setup: Equation (1) defines performance, Equation (2) defines the centralized/single-agent target, and Equation (3) generalizes the target to multiple agents with agent-specific prompt spaces.


Here, each agent _a ∈_ A aims to find the optimal prompt _p_<sup>_∗_</sup> _a_<sup>from its own prompt space P</sup><sup>_a_that maxi-</sup> mizes its performance on the task D. To achieve greater sample efficiency, all agents in A collaborate without sharing their raw data (i.e., the history of tested prompts and their scores). This problem formulation naturally aligns with common paradigms in the federated bandit literature (Wang et al., 2020; Dai et al., 2023). Therefore, we adopt the federated bandit framework to tackle this problem. 

**Feedback Model.** To solve the federated black-box prompt optimization problem, we cast the optimization process into an iterative protocol, where we sequentially select candidate prompts for evaluation. At each round _t_ , each agent _a_ selects one or two candidate prompts and receives feedback. The selection of the prompts is guided by theoretically principled bandit policies, which leverage the collective observation history from all agents to achieve sample-efficient optimization (more details in Sec. 3). Depending on the type of feedback available, we consider two settings: 

- **Score** receives a numeric score **feedback:** In this _s_ ˆsetting, _t,a_ as feedback, which directly reflects the performance of the prompteach agent selects a single prompt _pt,a_ at each round _t_ , and _pt,a_ on task D. Specifically, given a validation set DV representing the task D, the score can be ˆ 

- obtained as follows: _st,a_ = E( _x,y_ ) _∈_ DV � _m_ (LLM( _pt,a, x_ ) _, y_ )�. 

- **Preference feedback:** In this setting, every agent _a_ selects a pair of prompts ( _p_<sup>1</sup> _t,a_<sup>_, p_2</sup> _t,a_<sup>) at round</sup> _t_ , and observes a binary signal indicating which of the two performs better, i.e., which prompt yielded the better response. For example, such feedback may be directly provided by human evaluators (Lin et al., 2024a). Following the common practice from dueling bandits (Bengs et al., 

3 

Preprint. 

### **Algorithm 1** FedPOB (Agent _a ∈_ A) 

1: **Initialize:** _W_ sync = _W_ new,a = **0** _d×d_ , _Vt,a_ = _λId×d_ , _b_ sync = _b_ new,a = **0** _d_ , _t_ last = 0 2: **for** _t_ = 1 _,_ 2 _, . . . , T_ **do** 3: Compute _Vt,a ← λI_ + _W_ sync + _W_ new _,a_ 4: Update local model _θ_<sup>ˆ</sup> _t,a ← Vt,a_<sup>_−_1(</sup><sup>_b_sync+</sup><sup>_b_new</sup><sup>_,a_)</sup> 5: Select prompt _pt,a ←_ arg max _p∈_ P _a ⟨θ_<sup>ˆ</sup> _t,a, u_ ( _p_ ) _⟩_ + _ν||u_ ( _p_ ) _||Vt,a−_ 1 6: Query _pt,a_ to observe score feedback ˆ _st,a_ 7: Update _W_ new _,a ← W_ new _,a_ + _ut,au_<sup>_⊤_</sup> _t,a_<sup>_,b_new</sup><sup>_,a←b_new</sup><sup>_,a_+</sup><sup>_ut,as_ˆ</sup><sup>_t,a_</sup> 8: **if** ( _t − t_ last) _·_ log(det _Vt,a/_ det _V_ last _,a_ ) _> D_ **then** 9: Send a communication request to the central server 10: **if** a communication round is started **then** 11: Upload _{W_ new _,a, b_ new _,a}_ to the central server. Reset _W_ new,a = **0** _d×d, b_ new,a = **0** _d_ 12: Receive _{W_ sync _, b_ sync _}_ from server 

### **Algorithm 2** FedPOB <u>(Central Server)</u> 

1: **if** Central server receives a communication request from _any agent_ **then** 2: Initiate a communication round 3: **receive** _{ W_ new _,a_ and _b_ new _,a}a∈_ A from each agent 4: Update _W_ sync _← W_ sync +<sup>�</sup> _a∈_ A<sup>_W_new</sup><sup>_,a ,b_sync</sup><sup>_←b_sync + �</sup> _a∈_ A<sup>_b_new</sup><sup>_,a_</sup> 5: Broadcast _W_ sync and _b_ sync to all agents 

2022), we assume that the preference feedback is generated by the Bradley–Terry–Luce (BTL) model (Hunter, 2004). 

## 3 FEDERATED PROMPT OPTIMIZATION VIA BANDITS 

We adopt _linear models_ , rather than more complex ones such as neural networks, to learn the unknown reward function for federated prompt optimization. Accordingly, our FedPOB and FedPOB-Pref algorithms (illustrated in Fig. 1) are based on linear bandits (Abbasi-Yadkori et al., 2011) and linear dueling bandits (Bengs et al., 2022), respectively. This choice is motivated by the balance linear models offer between expressiveness, simplicity, and theoretical guarantees: (1) Modern text embedding techniques powered by transformers are sufficiently mature and effective (Shi et al., 2024; Hu et al., 2024), enabling a simple linear function to model the relationship between prompts and scores. (2) Linear models enable lightweight algorithmic designs. (3) Unlike federated neural bandits using neural networks for reward estimation (Dai et al., 2023), federated linear bandit methods provide theoretical guarantees on collaboration which ensure that _the performance improves as more agents join the federation_ (Wang et al., 2020). 

### 3.1 THE FEDPOB ALGORITHM: SCORE FEEDBACK 

Following recent works on black-box prompt optimization (Shi et al., 2024; Hu et al., 2024), we first map each discrete prompt _p_ into a continuous embedding vector _u_ ( _p_ ) _∈_ U using a pre-trained model. This allows us to leverage rich semantic representations and simplifies the optimization problem. We then model the score of a prompt for each agent _a_ using a linear model: _sa_ = _⟨θa, u_ ( _pa_ ) _⟩_ , which is standard in the multi-armed bandit literature (Abbasi-Yadkori et al., 2011). 

**Local Prompt Selection.** At the beginning of each round _t_ , in lines 3-4 of Algo. 1, each agent _a_ first updates its information matrix _Vt,a_ and estimated linear parameters _θ_<sup>ˆ</sup> _t,a_ using (1) _the aggregated information from all agents_ received from the central server (i.e., _W_ sync and _b_ sync, more details below) and (2) its newly collected local information (i.e., _W_ new _,a_ and _b_ new _,a_ ). Next, using the parameters _Vt,a_ and _θ_<sup>ˆ</sup> _t,a_ , agent _a_ selects the next prompt to query following the Upper Confidence Bound (UCB) strategy (line 5 of Algo. 1): 


![](P011_images/P011.pdf-0004-11.png)

### Figure analysis

Purpose: This displayed equation specifies the local prompt selection step for an agent in the FedPOB algorithm with score feedback.

Transcription:

\[
p_{t,a}=\arg\max_{p\in \mathcal{P}_a}\langle \hat{\theta}_t, u(p)\rangle + \nu \|u(p)\|_{V_{t,a}^{-1}}
\tag{4}
\]

Important components:
- \(p_{t,a}\): the prompt selected by agent \(a\) at round \(t\).
- \(\mathcal{P}_a\): the candidate prompt set available to agent \(a\).
- \(\langle \hat{\theta}_t, u(p)\rangle\): predicted score or exploitation term under the current linear parameter estimate.
- \(u(p)\): embedding vector of prompt \(p\).
- \(\nu \|u(p)\|_{V_{t,a}^{-1}}\): exploration bonus scaled by \(\nu\), using uncertainty induced by the inverse information matrix \(V_{t,a}^{-1}\).

Direct observation: The selected prompt maximizes the sum of a linear predicted reward term and a confidence/uncertainty norm term. Interpretation: This is an upper-confidence-bound selection rule, encouraging agents to choose prompts that are either expected to score highly or remain uncertain under the current model.

Connection to surrounding text: The equation appears in Section 3.1 during the description of local prompt selection for FedPOB under score feedback. It operationalizes the paper’s stated balance between exploitation and exploration after each agent updates its local model using synchronized federated information and newly collected local data.


Here the parameter _ν_ balances _exploitation_ (choosing prompts with large predicted rewards) and _exploration_ (choosing prompts with large uncertainty). Next, we test the selected prompt _pt,a_ using 

4 

Preprint. 

### **Algorithm 3** FedPOB-Pref (Agent _a ∈_ A) 

1: **Initialize:** _W_ sync = _W_ new,a = **0** _d×d_ , _θ_<sup>ˆ</sup> 0 _∼N_ ( **0** _, σ_<sup>2</sup> _Id_ ) with small _σ_<sup>2</sup> , 

- 2: **for** _t_ = 1 _,_ 2 _, . . . , T_ **do** 3: Select first prompt _p_<sup>1</sup> _t,a_<sup>_←_arg max</sup><sup>_p∈_P</sup> _a_<sup>_⟨θ_ˆ</sup><sup>_t−_1</sup><sup>_, u_(</sup><sup>_p_)</sup><sup>_⟩_</sup> 4: Select second prompt _p_<sup>2</sup> _t,a_<sup>_←_arg max</sup><sup>_p∈_P</sup> _a_<sup>_⟨θ_ˆ</sup><sup>_t−_1</sup><sup>_, u_(</sup><sup>_p_)</sup><sup>_−u_(</sup><sup>_p_1</sup> _t,a_<sup>)</sup><sup>_⟩_+</sup><sup>_βt||u_(</sup><sup>_p_)</sup><sup>_−u_(</sup><sup>_p_1</sup> _t,a_<sup>)</sup><sup>_||_</sup> _W_ sync<sup>_−_1</sup> 5: Query _p_<sup>1</sup> _t,a_<sup>_, p_2</sup> _t,a_<sup>to observe preference feedback</sup><sup>_ω_ˆ</sup><sup>_t,a_= 1(</sup><sup>_p_1</sup> _t,a_<sup>_≻p_2</sup> _t,a_<sup>)</sup> 6: Update local model _θ_<sup>ˆ</sup> _t,a ←_ arg min _p∈_ P _a Lt,a_ ( _θ_ ) _−⟨∇La_ ( _θ_<sup>ˆ</sup> _t−_ 1 _,a_ ) _, θ⟩_ +<sup>_<u>λ</u>_</sup> 2<sup>_||θ −θ_ˆ</sup><sup>_t−_1</sup><sup>_||_2</sup> 7: Update _∇La_ ( _θt,a_ ) _←∇La_ ( _θt−_ 1 _,a_ ) _− λ_ ( _θ_<sup>ˆ</sup> _t,a − θt−_ 1) 8: Compute _W_ new,a = [ _u_ ( _p_<sup>1</sup> _t,a_<sup>)</sup><sup>_−u_(</sup><sup>_p_2</sup> _t,a_<sup>)][</sup><sup>_u_(</sup><sup>_p_1</sup> _t,a_<sup>)</sup><sup>_−u_(</sup><sup>_p_2</sup> _t,a_<sup>)]</sup><sup>_⊤_</sup> 9: Upload _{θ_<sup>ˆ</sup> _t,a, ∇La_ ( _θ_<sup>ˆ</sup> _t,a_ ) _, W_ new,a _}_ to server **<u>gorithm 4orithm 4</u>** FedPOB-Pref <u>(Central Server)Central Server))</u> 

- 1: **receive** _{θ_<sup>ˆ</sup> _t,a, ∇La_ ( _θ_<sup>ˆ</sup> _t,a_ ) _, W_ new,a _}a∈_ A from each agent 2: Update server model _θ_<sup>ˆ</sup> _t ← n_<sup><u>1</u></sup> � _a∈_ A<sup>_θ_ˆ</sup><sup>_t,a −_</sup> _n_<sup><u>1</u></sup> � _a∈_ A _λ_ <u>1</u><sup>_∇La_(ˆ</sup><sup>_θt,a_)</sup> 3: Update _W_ sync _← W_ sync +<sup><u>�</u></sup> _a∈_ A<sup>_W_new</sup><sup>_,a_</sup> 4: Broadcast _θ_<sup>ˆ</sup> _t_ and _W_ sync to all agents 

### **Algorithm 4orithm 4** FedPOB-Pref <u>(Central Server)Central Server))</u> 

the validation set DV, to obtain score feedback _s_ ˆ _t,a_ (line 6 of Algo. 1). Then, we update the newly collected local information _W_ new _,a_ and _b_ new _,a_ (line 7 of Algo. 1). 

**Agent-Server Communication.** To reduce the communication cost, we only start a communication round when the new information collected by any agent exceeds a threshold _D_ , i.e., when the criterion in line 8 of Algo. 1 is satisfied. If a communication request is sent by any agent, the trusted central server initiates a communication round (line 1-2 of Algo. 2) and all agents upload their local parameters _W_ new _,a_ and _b_ new _,a_ to the central server (lines 10-11). The central server then aggregates these local parameters to produce synchronized parameters _W_ sync and _b_ sync (line 3-4 of Algo. 2), which are then broadcast to all agents. After the agents receive the aggregated parameters _W_ sync and _b_ sync, they can use them to select the prompt in the next iteration, and the algorithm repeats. 

### 3.2 THE FEDPOB-PREF ALGORITHM: PREFERENCE FEEDBACK 

In many practical applications, obtaining explicit numerical scores is challenging, whereas collecting pairwise preference feedback is often more natural and cost-effective. For instance, in human-inthe-loop scenarios, users can more reliably state a preference between two generated outputs than assign them absolute scores (Yue et al., 2012; Lin et al., 2024a). This setting, however, introduces a significant technical hurdle: _the parameter estimation for linear dueling bandits does not have a closed-form solution_ (Bengs et al., 2022). This limitation prevents the use of the simple parameter aggregation strategy employed by our FedPOB algorithm. 

The absence of a closed-form solution naturally leads to gradient-based optimization approaches. Recent work by Huang et al. (2025) introduced federated linear dueling bandit algorithms (FLDBGD and FLDB-OGD) that achieve collaboration by aggregating local gradients. While theoretically sound, these methods face a practical dilemma: FLDB-GD incurs high communication costs, whereas the more communication-efficient FLDB-OGD suffers significant performance degradation. We attribute this to the fact that _preference feedback is inherently noisier and less informative than numerical scores_ , making it particularly challenging to achieve both competitive performance and communication efficiency. To overcome this, we draw inspiration from _classical federated learning_ for solving supervised learning problems (McMahan et al., 2017). Specifically, instead of aggregating gradients, we aggregate model parameters, which allows us to adopt a dynamic regularization technique that has proven effective in federated learning (Acar et al., 2021) for further performance improvement. This leads to our proposed FedPOB-Pref algorithm (Algos. 3 and 4). 

Our FedPOB-Pref algorithm offers several key advantages: (1) it is highly **sample-efficient** , capable of learning the underlying reward model from a small number of preference queries; (2) it is robust to **agent heterogeneity** , and its performance scales effectively with the number of collabo- 

5 

Preprint. 

rating agents; and (3) when compared to the baselines from Huang et al. (2025), FedPOB-Pref simultaneously **reduces communication costs and improves performance** (Sec. 4.2). 

The overall workflow of FedPOB-Pref is outlined in Algorithms 3 and 4. At each round _t_ , every agent _a_ selects a pair of prompts based on the global model _θ_<sup>ˆ</sup> _t−_ 1. The first prompt, _p_<sup>1</sup> _t,a_<sup>, represents</sup> pure **exploitation** (line 3), while the second, _p_<sup>2</sup> _t,a_<sup>,incorporatesan</sup><sup>**exploration**bonustodiscover</sup> more informative options (line 4). This dueling selection strategy is grounded in the theory of dueling bandits (Bengs et al., 2022; Verma et al., 2024). We then obtain binary preference feedback _ωt,a_ = 1 _p_ 1 _t,a_<sup>_≻p_2</sup> _t,a_<sup>for this pair of selected prompts (line 5).The core of our method lies in the local</sup> model update (line 6), which optimizes an objective that combines the standard logistic loss with a dynamic regularizer (Acar et al., 2021). The first component is the pairwise logistic loss over the agent’s local history: 


![](P011_images/P011.pdf-0006-03.png)

### Figure analysis

The figure presents Equation (5), which defines the local loss function for agent \(a\) at round \(t\) in the FedPOB-Pref algorithm.

**Transcribed equation:**

\[
L_{t,a}(\theta) = -\sum_{\tau=1}^{t-1}\left(\omega_{\tau,a}\log \sigma\left(\theta^\top [u(p^1_{\tau,a}) - u(p^2_{\tau,a})]\right) + (1-\omega_{\tau,a})\log \sigma\left(\theta^\top [u(p^2_{\tau,a}) - u(p^1_{\tau,a})]\right)\right).
\]

**Direct observations:**
- The loss aggregates over past local preference comparisons from \(\tau=1\) to \(t-1\).
- Each comparison involves two prompts, labeled \(p^1_{\tau,a}\) and \(p^2_{\tau,a}\), represented through embeddings or feature maps \(u(\cdot)\).
- The binary variable \(\omega_{\tau,a}\) selects which log-likelihood term is active: one term corresponds to \(p^1\) being preferred over \(p^2\), while the other corresponds to \(p^2\) being preferred over \(p^1\).
- The model parameter vector \(\theta\) scores the difference between prompt embeddings through an inner product, passed through the sigmoid function \(\sigma\).

**Interpretation in context:**
- This is the pairwise negative log-likelihood under a Bradley-Terry-Luce-style preference model, matching the surrounding text's description of binary preference feedback.
- The equation supplies the standard logistic loss component of the FedPOB-Pref local objective; the surrounding paper text states that this is later combined with a dynamic regularization term to reduce local drift in the federated setting.
- The loss supports the algorithmic workflow described nearby: each agent selects prompt pairs, receives binary preference feedback, performs a local model update, and then uploads updated parameters for server aggregation.


This term is the negative log-likelihood of the observed preferences under the BTL model (Bengs et al., 2022). The second component is a dynamic regularization term consisting of (i) a linear penalty, _−⟨∇La_ ( _θ_<sup>ˆ</sup> _t−_ 1 _,a_ ) _, θ⟩_ , which corrects for local gradient drift, and (ii) a quadratic penalty, which prevents the local model from deviating excessively from the previous global model (Acar et al., 2021). After this local update (lines 6-8), agents upload their new parameters to the central server for aggregation, which then broadcasts the aggregated global parameters for the next round. Of note, we conduct theoretical analysis to motivate the local objective function of FedPOB-Pref (App. D), providing theoretical justification for its strong performance (Sec. 4.2). 

## 4 EXPERIMENTS 

We adopt MPNet (Song et al., 2020) as the text embedding model, and use GPT-3.5-turbo (OpenAI, 2023a) in the experiments unless specified otherwise. Of note, we also test two other models, GPT4o-mini (OpenAI, 2023b) and Qwen3-235B-A22B-2507 (Bai et al., 2023), in Sec. 5. Evaluation is performed on the Instruction Induction (Chen et al., 2023; Lin et al., 2024b) and BIG-Bench Hard datasets (Suzgun et al., 2023), which collectively cover over 50 tasks that span diverse areas such as reasoning, language comprehension, and code generation. To account for agent heterogeneity, we ensure that the prompt domains of all agents contain both shared prompts and unique prompts. For fair comparisons, we ensure an equal validation query budget across all algorithms and analyze the corresponding communication costs in the federated setting. We defer more details on the experimental setting to App. B. 

### 4.1 SCORE FEEDBACK: FEDPOB 

In the setting with score-based feedback, every tested prompt receives a numerical score indicating the quality of its induced response. Here we assess performance of a prompt using a validation set and adopt the validation accuracy as the corresponding score. The objective is to identify the optimal prompt (i.e., the one that achieves the highest validation score). We compare our FedPOB with a representative baseline method on federated prompt optimization: FedOne (Wang et al., 2025), as well as two other baselines on standard prompt optimization: INSTINCT (Lin et al., 2024b) and PromptBreeder (Fernando et al., 2024). 

Table 1 and 2 report the final scores achieved by the best prompt discovered by each algorithm in various tasks. The results demonstrate the superior capability of our FedPOB, which achieves the highest score on the majority of the tasks under the setting of ten agents. Fig. 2 depicts the performance of FedPOB across different iterations, where we observe a positive correlation between the number of agents and the achieved prompt score, highlighting the benefits of multi-agent collaboration. In addition, FedPOB achieves a near-optimal score with a small batch of samples, demonstrating its sample efficiency. 

6 

Preprint. 

Table 1: Average validation accuracy (with standard error) of the best prompt found by each algorithm in the **Instruction Induction dataset** , averaged over 5 independent trials with different random seeds. For clarity, only a representative subset of challenging tasks. The complete results for all tasks are provided in Table 5 (App. C.3) and the results are consistent. 

|**Dataset**|**INSTINCT**|**PromptBreeder**|**FedOne (10 agents)**||**FedPOB (ours)**||
|---|---|---|---|---|---|---|
|||||1 Agent|3 Agents|10 Agents|
|Active to Passive|0.940_±_0.053|**1.000**_±_**0.000**|**1.000**_±_**0.000**|0.804_±_0.160|0.960_±_0.014|0.972_±_0.023|
|Auto Categorization|**0.313**_±_**0.012**|0.220_±_0.020|0.264_±_0.004|0.272_±_0.030|0.308_±_0.018|0.288_±_0.023|
|Antonyms|0.767_±_0.023|0.840_±_0.020|**0.870**_±_**0.005**|0.792_±_0.046|0.812_±_0.027|0.828_±_0.023|
|Common Concept|**0.217**_±_**0.040**|0.118_±_0.010|0.136_±_0.003|0.188_±_0.015|0.210_±_0.007|0.208_±_0.018|
|Informal to Formal|0.570_±_0.020|0.521_±_0.067|**0.605**_±_**0.005**|0.528_±_0.028|0.528_±_0.039|0.570_±_0.030|
|Larger Animal|**0.993**_±_**0.012**|0.987_±_0.012|0.829_±_0.037|0.984_±_0.017|0.992_±_0.011|0.989_±_0.011|
|Negation|0.860_±_0.020|0.927_±_0.012|0.897_±_0.010|0.856_±_0.061|**0.940**_±_**0.014**|0.920_±_0.032|
|Orthography Starts With|0.767_±_0.214|0.813_±_0.061|0.436_±_0.024|0.804_±_0.100|0.828_±_0.056|**0.832**_±_**0.087**|
|Rhymes|0.493_±_0.142|0.393_±_0.031|0.916_±_0.027|0.664_±_0.120|0.776_±_0.187|**0.844**_±_**0.106**|
|Second Word Letter|0.847_±_0.110|0.947_±_0.042|0.625_±_0.034|0.792_±_0.199|0.880_±_0.157|**0.972**_±_**0.023**|
|Sentence Similarity|0.467_±_0.031|0.380_±_0.020|0.360_±_0.035|**0.540**_±_**0.094**|0.508_±_0.082|0.448_±_0.018|
|Sentiment|0.973_±_0.012|0.993_±_0.012|**0.996**_±_**0.002**|0.988_±_0.018|0.972_±_0.023|0.972_±_0.027|
|Synonyms|0.327_±_0.150|0.333_±_0.115|0.320_±_0.023|0.324_±_0.103|0.296_±_0.041|**0.384**_±_**0.124**|
|Taxonomy Animal|0.947_±_0.023|0.967_±_0.042|0.805_±_0.026|0.924_±_0.073|**0.980**_±_**0.024**|0.972_±_0.034|
|Translation En-De|0.820_±_0.020|0.820_±_0.060|**0.927**_±_**0.004**|0.820_±_0.047|0.840_±_0.032|0.868_±_0.036|
|Translation En-Es|0.747_±_0.042|0.746_±_0.023|**0.950**_±_**0.012**|0.756_±_0.026|0.740_±_0.072|0.728_±_0.030|
|Translation En-Fr|0.947_±_0.023|0.920_±_0.040|0.919_±_0.005|0.944_±_0.033|0.940_±_0.283|**0.948**_±_**0.018**|
|Word in Context|0.553_±_0.058|0.620_±_0.040|0.409_±_0.091|0.460_±_0.084|**0.640**_±_**0.020**|0.608_±_0.036|
|Object Counting|0.520_±_0.106|0.473_±_0.110|0.497_±_0.019|0.520_±_0.074|**0.616**_±_**0.039**|0.588_±_0.050|
|Odd One Out|0.867_±_0.058|0.833_±_0.116|0.859_±_0.024|0.800_±_0.122|**0.900**_±_**0.000**|**0.900**_±_**0.000**|
|Word Sorting|0.753_±_0.058|0.753_±_0.099|0.497_±_0.026|0.756_±_0.093|0.744_±_0.065|**0.828**_±_**0.063**|
|<br>Word Unscrambling|0.687_±_0.012|0.687_±_0.023|**0.728**_±_**0.005**|0.724_±_0.046|0.716_±_0.026|0.720_±_0.028|
|Average (22 Tasks)|0.669|0.665|0.645|0.663|0.701|**0.712**|



Table 2: Performance on the **Big-Bench Hard (BBH) dataset** under the same experimental settings. 

|**Dataset**|**INSTINCT**|**PromptBreeder**|**FedOne (10 agents)**||**FedPOB (ours)**||
|---|---|---|---|---|---|---|
|||||1 Agent|3 Agents|10 Agents|
|Boolean Expressions|0.793_±_0.046|0.853_±_0.012|**0.883**_±_**0.003**|0.800_±_0.025|0.836_±_0.021|0.844_±_0.026|
|Date Understanding|0.587_±_0.012|0.593_±_0.030|**0.633**_±_**0.007**|0.580_±_0.028|0.576_±_0.033|0.572_±_0.030|
|Disambiguation QA|0.713_±_0.031|0.753_±_0.023|**0.858**_±_**0.011**|0.816_±_0.026|0.844_±_0.017|0.840_±_0.032|
|Dyck Languages|0.713_±_0.031|0.693_±_0.012|**0.722**_±_**0.005**|0.672_±_0.018|0.668_±_0.023|0.680_±_0.032|
|Formal Fallacies|0.687_±_0.031|0.967_±_0.058|**0.991**_±_**0.002**|0.700_±_0.121|0.872_±_0.175|0.812_±_0.172|
|Geometric Shapes|0.453_±_0.058|0.360_±_0.060|0.272_±_0.007|0.436_±_0.022|0.412_±_0.039|**0.448**_±_**0.036**|
|Hyperbaton|0.913_±_0.046|0.907_±_0.023|0.946_±_0.003|0.868_±_0.522|0.928_±_0.027|**0.948**_±_**0.018**|
|Logical Deduction Five Objects|0.473_±_0.046|0.460_±_0.053|0.466_±_0.009|0.464_±_0.041|0.452_±_0.030|**0.476**_±_**0.017**|
|Logical Deduction Seven Objects|0.513_±_0.046|0.473_±_0.031|0.485_±_0.002|0.476_±_0.043|**0.492**_±_**0.046**|0.488_±_0.415|
|Logical Deduction Three Objects|0.600_±_0.053|0.573_±_0.046|0.635_±_0.009|0.604_±_0.033|0.636_±_0.017|**0.644**_±_**0.009**|
|Movie Recommendation|**0.820**_±_**0.069**|0.767_±_0.023|0.688_±_0.004|0.720_±_0.037|0.720_±_0.032|0.732_±_0.027|
|Multistep Arithmetic Two|0.647_±_0.129|0.601_±_0.030|0.685_±_0.017|0.580_±_0.105|0.648_±_0.018|**0.692**_±_**0.046**|
|Navigate|0.707_±_0.031|0.760_±_0.020|0.755_±_0.028|0.688_±_0.052|0.720_±_0.042|**0.716**_±_**0.026**|
|Penguins in a Table|0.577_±_0.031|**0.694**_±_**0.016**|0.581_±_0.031|0.562_±_0.035|0.584_±_0.031|0.605_±_0.015|
|Reasoning about Colored Objects|0.547_±_0.023|0.593_±_0.023|0.440_±_0.008|0.548_±_0.036|0.528_±_0.034|**0.568**_±_**0.027**|
|Ruin Names|0.707_±_0.023|**0.767**_±_**0.042**|0.625_±_0.003|0.688_±_0.039|0.660_±_0.042|0.724_±_0.067|
|Salient Translation Error Detection|0.573_±_0.012|**0.633**_±_**0.070**|0.500_±_0.055|0.584_±_0.033|0.588_±_0.018|0.600_±_0.028|
|Snarks|0.778_±_0.022|0.770_±_0.051|0.675_±_0.003|0.779_±_0.022|**0.791**_±_**0.012**|0.782_±_0.019|
|Sports Understanding|0.440_±_0.106|0.540_±_0.072|**0.669**_±_**0.004**|0.524_±_0.114|0.552_±_0.073|0.564_±_0.078|
|Temporal Sequences|0.647_±_0.050|0.473_±_0.046|0.403_±_0.019|0.612_±_0.058|0.648_±_0.050|**0.652**_±_**0.052**|
|Tracking Shuffed Objects Five Objects|0.300_±_0.053|0.287_±_0.012|0.279_±_0.030|0.296_±_0.017|0.304_±_0.017|**0.328**_±_**0.023**|
|Tracking Shuffed Objects Seven Objects|0.280_±_0.020|0.253_±_0.042|**0.281**_±_**0.006**|0.268_±_0.023|0.268_±_0.023|0.256_±_0.029|
|Tracking Shuffed Objects Three Objects|**0.473**_±_**0.046**|0.440_±_0.020|0.413_±_0.018|0.432_±_0.039|0.420_±_0.049|0.400_±_0.014|
|Web of Lies|0.633_±_0.023|0.607_±_0.012|0.627_±_0.012|0.640_±_0.039|**0.644**_±_**0.043**|0.636_±_0.026|
|Average (24 Tasks)|0.607|0.618|0.605|0.596|0.616|**0.625**|



### 4.2 PREFERENCE FEEDBACK: FEDPOB-PR E F 

To simulate user preference feedback in our experiments, we adopt the protocol from Lin et al. (2024a). For any pair of prompts ( _pt,_ 1 _, pt,_ 2), we first compute their ground-truth scores, _s_ ( _pt,_ 1) and _s_ ( _pt,_ 2), on a validation set. The preference probability is then determined by the BradleyTerry-Luce (BTL) model (Hunter, 2004): _P_ ( _pt,_ 1 _≻ pt,_ 2) = _σ_ ( _s_ ( _pt,_ 1) _− s_ ( _pt,_ 2)), where _σ_ ( _·_ ) is the sigmoid function. A binary preference outcome _yt_ = 1( _pt,_ 1 _≻ pt,_ 2) is then sampled from a Bernoulli distribution with this probability. We compare FedPOB-Pref against federated baselines FLDB-GD and FLDB-OGD (Huang et al., 2025), as well as standard prompt optimization methods APOHF (Lin et al., 2024a) and DoubleTS (Dwaracherla et al., 2024). 

7 

Preprint. 


![](P011_images/P011.pdf-0008-01.png)


Figure 2: Performance of FedPOB with varying numbers of agents. 

Figure 3: Performance of FedPOB-Pref with varying numbers of agents. 

The results, summarized in Table 3, demonstrate that FedPOB-Pref consistently achieves the best performance across different numbers of agents. Our method establishes a superior trade-off between performance and communication cost. Specifically, FedPOB-Pref matches the communication efficiency of FLDB-OGD while delivering substantially better results. Conversely, while FLDB-GD obtains the second-best performance, it does so at a considerably higher communication cost. Fig. 3 further highlights that the sample efficiency of FedPOB-Pref improves as more agents collaborate. Additional results are available in Fig. 10 (App. C.2). 

Table 3: Score and number of communication rounds under **preference feedback** . 

|Method|Agent|Instructio|n Induction|B|BH|
|---|---|---|---|---|---|
|||Perf.|Comm.|Perf.|Comm.|
|APOHF|-|0.7681|-|0.5838|-|
|Double TS|-|0.7859|-|0.5983|-|
||1|0.7624|1500|0.5868|1500|
|FLDB-GD|3|0.7959|1500|0.6204|1500|
||10|0.8244|1500|0.6457|1500|
||1|0.6872|**50**|0.5286|**50**|
|FLDB-OGD|3|0.7687|**50**|0.5880|**50**|
||10|0.8123|**50**|0.6271|**50**|
||1|**0.8000**|**50**|**0.6213**|**50**|
|FedPOB-Pref|3|**0.8145**|**50**|**0.6357**|**50**|
||10|**0.8482**|**50**|**0.6583**|**50**|




![](P011_images/P011.pdf-0008-07.png)


Figure 4: Scores of FedPOB with varying communication thresholds _D_ . 

## 5 ABLATION STUDY 

**Performance vs. Communication in FedPOB.** In federated learning, communication is inherently costly, making frequent interactions with the central server impractical. Thus, an effective algorithm should maintain strong performance even with infrequent communications. Here we reduce the interaction frequency by varying the communication threshold _D_ in FedPOB in the range: _{_ 0 _,_ 10 _,_ 100 _,_ 300 _,_ 1000 _}_ . Note that a larger _D_ results in less communication rounds. The results in Fig. 4 reveal a clear trade-off between performance (the best score after 20 iterations) and communication, i.e., fewer communication rounds (i.e., larger _D_ ) result in worse performance. More importantly, our FedPOB still achieves strong performance even with infrequent communications, demonstrating its robustness and practical effectiveness in realistic federated environments. 

**Generalization to Other LLMs.** While the response quality of an LLM depends not only on the prompt design but also on the inherent capability of the backbone model, we examine whether the observed performance gains of our algorithms can generalize to other LLMs. To this end, we replace the GPT-3.5-Turbo model used in our main experiments by GPT-4o-mini and Qwen (OpenAI, 2023a;b; Bai et al., 2023), while keeping all other settings fixed. As shown in Fig. 5, our FedPOB consistently discovers high-score prompts and achieves better performance with a larger number of agents, regardless of the underlying LLM. Additional results on the performance of FedPOB-Pref can be found in App. C.4, which lead to consistent observations. 

8 

Preprint. 


![](P011_images/P011.pdf-0009-01.png)


Figure 5: The performance of FedPOB using GPT-4o-mini and Qwen. 

**Effectiveness of Dynamic Regularization in FedPOB-Pref.** We further assess the necessity of the dynamic regularization term in FedPOB-Pref, which mitigates the dynamic drift among heterogeneous clients and accelerates collaboration. We compare the performance of FedPOB-Pref with and without this term, the latter of which is equivalent to the classical FedAvg algorithm (McMahan et al., 2017)). Fig. 6 shows that incorporating dynamic regularization stabilizes performance, speeds up convergence, and reduces fluctuations caused by inter-agent heterogeneity. These results highlight its critical role in enabling efficient and robust federated prompt optimization in heterogeneous federated environments. 


![](P011_images/P011.pdf-0009-04.png)



![](P011_images/P011.pdf-0009-05.png)



![](P011_images/P011.pdf-0009-06.png)



![](P011_images/P011.pdf-0009-07.png)



![](P011_images/P011.pdf-0009-08.png)



![](P011_images/P011.pdf-0009-09.png)


Figure 6: Impact of the dynamic regularization term in FedPOB-Pref. FedAvg corresponds to removing this term. 

## 6 RELATED WORK 

**Federated Prompt Optimization.** Federated Learning enables collaborative model training without sharing private data (Kairouz et al., 2019; McMahan et al., 2017). However, applying FL to LLMs faces a critical barrier: the prohibitive cost of communicating updates for models of such massive scale. A natural workaround is to combine FL with parameter-efficient prompt tuning (Zhao et al., 2023; Che et al., 2023; Deng et al., 2024; Wei et al., 2023), where only lightweight soft prompts are trained and communicated. While resource-efficient, this paradigm operates in a whitebox setting and thus fails in API-based black-box scenarios. This limitation has motivated research on black-box federated prompt optimization (Lin et al., 2023). Early efforts such as FedBPT (Zhang et al., 2023) adopt soft prompts with gradient-free optimization, but remain incompatible with APIonly LLMs. More recent work addresses discrete prompt optimization, e.g., FedOne (Wang et al., 2025), which learns categorical distributions to sample prompts. Despite solving discreteness, these methods suffer from inefficiency and poor semantic quality, leaving open the challenge of developing a query-efficient federated method that produces semantically meaningful discrete prompts for black-box LLMs. We defer a detailed discussion of the related works on standard non-federated prompt optimization to App. A due to space constraint. 

9 

Preprint. 

## 7 CONCLUSION 

In this paper, we introduced FedPOB and FedPOB-Pref, novel algorithms for sample-efficient federated prompt optimization. Built upon the theory of federated multi-armed bandits, our methods enable multiple agents to effectively collaborate to find optimal prompts for black-box LLMs without sharing raw data. Extensive experiments demonstrate that our algorithms significantly outperform existing baselines under both score and preference feedback, with performance consistently improving with an increasing number of participating agents. Notably, FedPOB-Pref establishes a superior performance-to-communication trade-off in the practical preference-based setting. 

## REFERENCES 

Yasin Abbasi-Yadkori, D´avid P´al, and Csaba Szepesv´ari. Improved algorithms for linear stochastic bandits. In _Proc. NIPS_ , 2011. 

- Durmus Alp Emre Acar, Yue Zhao, Ramon Matas Navarro, Paul N. Whatmough Matthew Mattina, and Venkatesh Saligrama. Federated learning based on dynamic regularization. In _Proc. ICLR_ , 2021. 

- Jinze Bai, Shuai Bai, Yunfei Chu, Zeyu Cui, Kai Dang, Xiaodong Deng, Yang Fan, Wenbin Ge, Yu Han, Fei Huang, Binyuan Hui, Luo Ji, Mei Li, Junyang Lin, Dayiheng Liu, Gao Liu, Chengqiang Lu, Keming Lu, Jianxin Ma, Rui Men, Xingzhang Ren, Xuancheng Ren, Chuanqi Tan, Sinan Tan, Jianhong Tu, Peng Wang, Shijie Wang, Wei Wang, Shengguang Wu, Benfeng Xu, Jin Xu, An Yang, Hao Yang, Jian Yang, Shusheng Yang, Yang Yao, Bowen Yu, Hongyi Yuan, Zheng Yuan, Jianwei Zhang, Xingxuan Zhang, Yichang Zhang, Zhenru Zhang, Chang Zhou, Jingren Zhou, Xiaohuan Zhou, and Tianhang Zhu. Qwen technical report. _arXiv preprint arXiv:2309.16609_ , 2023. 

- Viktor Bengs, Aadirupa Saha, and Eyke H¨ullermeier. Stochastic contextual dueling bandits under linear stochastic transitivity models. In _Proc. ICML_ , 2022. 

- Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, Sandhini Agarwal, Ariel Herbert-Voss, Gretchen Krueger, Tom Henighan, Rewon Child, Aditya Ramesh, Daniel M. Ziegler, Jeffrey Wu, Clemens Winter, Christopher Hesse, Mark Chen, Eric Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess, Jack Clark, Christopher Berner, Sam McCandlish, Alec Radford, Ilya Sutskever, and Dario Amodei. Language models are few-shot learners. In _Proc. NeurIPS_ , 2020. 

- Tianshi Che, Ji Liu, Yang Zhou, Jiaxiang Ren, Jiwen Zhou, Victor Sheng, Huaiyu Dai, and Dejing Dou. Federated learning of large language models with parameter-efficient prompt tuning and adaptive optimization. In _Proc. EMNLP_ , 2023. 

- Lichang Chen, Jiuhai Li, Tiejun Zhang, and Bo Zhou. InstructZero: A preference-based iterative prompt optimization framework. In _Proc. EMNLP_ , 2023. 

- Zhongxiang Dai, Arun Verma Yao Shu, Flint Xiaofeng Fan, and Bryan Kian Hsiang Low. Federated neural bandits. In _Proc. ICLR_ , 2023. 

- Mingkai Deng, Jianyu Wang, Cheng-Ping Zhang, Han Li, Yaliang Chen, Lidong Zhao, Jing Liu, Yang Chen, and Xiang Liu. RLPrompt: Optimizing discrete text prompts with reinforcement learning. In _Proc. EMNLP Findings_ , 2022. 

- Wenlong Deng, Christos Thrampoulidis, and Xiaoxiao Li. Unlocking the potential of prompt-tuning in bridging generalized and personalized federated learning. In _Proc. CVPR_ , 2024. 

- Shizhe Diao, Zhichao Huang, Ruijie Xu, Xuechun Li, Lin Yong, Xiao Zhou, and Tong Zhang. Black-box prompt learning for pre-trained language models. _Transactions on Machine Learning Research_ , 2023. 

- Abhimanyu Dubey and Alex Pentland. Differentially-private federated linear bandits. In _Proc. NeurIPS_ , pp. 6003–6014, 2020. 

10 

Preprint. 

- Vikranth Dwaracherla, Seyed Mohammad Asghari, Botao Hao, and Benjamin Van Roy. Efficient exploration for LLMs. In _Proc. ICML_ , 2024. 

- Chrisantha Fernando, Dylan Banarse, Henryk Michalewski, Simon Osindero, and Tim Rockt¨aschel. Promptbreeder: Self-referential self-improvement via prompt evolution. In _Proc. ICLR_ , 2024. 

- Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu, Shirong Ma, Peiyi Wang, Xiao Bi, et al. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning. _arXiv preprint arXiv:2501.12948_ , 2025. 

- Qingyan Guo, Rui Wang, Junzhe Guo, Boyu Li, Kai Song, Xu Tan, Guoqing Liu, Jiang Bian, and Yanyang Yang. Connecting large language models with evolutionary algorithms yields powerful prompt optimizers. In _Proc. ICLR_ , 2024. 

- Wenyang Hu, Yao Shu, Zongmin Yu, Zhaoxuan Wu, Xiangqiang Lin, Zhongxiang Dai, See-Kiong Ng, and Bryan Kian Hsiang Low. Localized zeroth-order prompt optimization. In _Proc. NeurIPS_ , 2024. 

- Xuhan Huang, Yan Hu, Zhiyan Li, Zhiyong Wang, Benyou Wang, and Zhongxiang Dai. Federated linear dueling bandits. _arXiv preprint arXiv:2502.01085_ , 2025. 

- David R Hunter. Mm algorithms for generalized bradley-terry models. _Annals of Statistics_ , 2004. 

- Gurusha Juneja, Gautam Jajoo, Nagarajan Natarajan, Hua Li, Jian Jiao, and Amit Sharma. Task facet learning: A structured approach to prompt optimization. In _Proc. ACL_ , 2025. 

- Peter Kairouz, H Brendan McMahan, Brendan Avent, Aur´elien Bellet, Mehdi Bennis, Arjun Nitin Bhagoji, Keith Bonawitz, Zachary Charles, Graham Cormode, Rachel Cummings, et al. Advances and open problems in federated learning. arXiv:1912.04977, 2019. 

- Weize Kong, Spurthi Hombaiah, Mingyang Zhang, Qiaozhu Mei, and Michael Bendersky. PRewrite: Prompt rewriting with reinforcement learning. In _Proc. ACL Short Papers_ , 2024. 

- Tor Lattimore and Csaba Szepesv´ari. _Bandit algorithms_ . Cambridge University Press, 2020. 

- Brian Lester, Rami Al-Rfou, and Noah Constant. The power of scale for parameter-efficient prompt tuning. In _Proc. EMNLP_ , 2021. 

- Xiang Lisa Li and Percy Liang. Prefix-Tuning: Optimizing continuous prompts for generation. In _Proc. ACL_ , 2021. 

- Xiaoqiang Lin, Zhongxiang Dai, Arun Verma, See-Kiong Ng, Patrick Jaillet, and Bryan Kian Hsiang Low. Prompt optimization with human feedback. _arXiv preprint arXiv:2405.17346_ , 2024a. 

- Xiaoqiang Lin, Zhaoxuan Wu, Zhongxiang Dai, Wenyang Hu, Yao Shu, See-Kiong Ng, Patrick Jaillet, and Bryan Kian Hsiang Low. Use your INSTINCT: Instruction optimization using neural bandits coupled with transformers. In _Proc. ICML_ , 2024b. 

- Zihao Lin, Yitao Zeng, Sicheng Yu, Lue Tao, Yuxin Chen, Wenhao Yu, and Lifu Huang. Efficient federated prompt tuning for black-box large pre-trained models. _arXiv preprint arXiv:2310.03123_ , 2023. 

- Xiao Liu, Yanan Zheng, Zhengxiao Du, Ming Ding, Yujie Qian, Zhilin Yang, and Jie Tang. GPT Understands, Too. In _Proc. ACL_ , 2021. 

- Yichong Luo, Huaxiu Yao, Feng-Shih Chang, Zhi-Kai Zhang, and Jian-Yun Nie. Black-box prompt optimization: Aligning large language models without model training. _arXiv preprint arXiv:2311.02646_ , 2023. 

- O. Ma˜nas, P. Astolfi, M. Hall, C. Ross, J. Urbanek, A. Williams, A. Agrawal, A. Romero-Soriano, and M. Drozdzal. Improving text-to-image consistency via automatic prompt optimization. _arXiv preprint arXiv:2403.17804_ , 2024. 

- H Brendan McMahan, Eider Moore, Daniel Ramage, Seth Hampson, et al. Communication-efficient learning of deep networks from decentralized data. In _Proc. AISTATS_ , 2017. 

11 

Preprint. 

OpenAI. GPT-3.5: Openai language model. https://platform.openai.com/, 2023a. Accessed: 2025-09-24. 

OpenAI. GPT-4 technical report. _arXiv preprint arXiv:2303.08774_ , 2023b. 

Archiki Prasad, Peter Hase, Xiang Zhou, and Mohit Bansal. GrIPS: Gradient-free, edit-based instruction search for prompting large language models. In _Proc. ACL_ , 2023. 

- Reid Pryzant, Dan Iter, Jerry Li, Yin Tat Lee, Chenguang Zhu, and Michael Zeng. Automatic prompt optimization with ”gradient descent” and beam search. In _Proc. EMNLP_ , 2023. 

- L. Schneider, M. Wistuba, A. Klein, J. Golebiowski, G. Zappella, and F. A. Merra. Hyperband-based bayesian optimization for black-box prompt selection. _arXiv preprint arXiv:2412.07820_ , 2024. 

Chengshuai Shi and Cong Shen. Federated multi-armed bandits. In _Proc. AAAI_ , 2021. 

- Chengshuai Shi, Kun Yang, Jing Yang, and Cong Shen. Best arm identification for prompt learning under a limited budget. _arXiv preprint arXiv:2402.09723_ , 2024. 

- Taylor Shin, Yasaman Razeghi, Robert L. Logan IV, Eric Wallace, and Sameer Singh. AutoPrompt: Eliciting knowledge from language models with automatically generated prompts. In _Proc. EMNLP_ , 2020. 

- Kaitao Song, Xu Tan, Tao Qin, Jianfeng Lu, and Tie-Yan Liu. Mpnet: Masked and permuted pretraining for language understanding. In _Proc. NeurIPS_ , 2020. 

- Mirac Suzgun, Nathan Scales, Nathanael Sch¨arli, Sebastian Gehrmann, Yi Tay, Hyung Won Chung, Aakanksha Chowdhery, Quoc V Le, Ed H Chi, Denny Zhou, and Jason Wei. Challenging bigbench tasks and whether chain-of-thought can solve them. In _Proc. ACL Findings_ , 2023. 

- Gemini Team, Rohan Anil, Sebastian Borgeaud, Jean-Baptiste Alayrac, Jiahui Yu, Radu Soricut, Johan Schalkwyk, Andrew M Dai, Anja Hauth, Katie Millican, et al. Gemini: a family of highly capable multimodal models. _arXiv preprint arXiv:2312.11805_ , 2023. 

- Arun Verma, Zhongxiang Dai, Xiaoqiang Lin, Patrick Jaillet, and Bryan Kian Hsiang Low. Neural dueling bandits: Preference-based optimization with human feedback. _arXiv preprint arXiv:2407.17112_ , 2024. 

- Ganyu Wang, Yuekang Li, Yi Zeng, Tianyu Wang, Kang Yang, and Kai Chen. FedOne: Query-efficient federated learning for black-box discrete prompt learning. _arXiv preprint arXiv:2502.04943_ , 2025. 

- Xinyuan Wang, Chenxi Li, Zhen Wang, Fan Bai, Haotian Luo, Jiayou Zhang, Nebojsa Jojic, Eric P. Xing, and Zhiting Hu. PromptAgent: Strategic planning with language models enables expertlevel prompt optimization. In _Proc. ICLR_ , 2024. 

- Yuanhao Wang, Jiachen Hu, Xiaoyu Chen, and Liwei Wang. Distributed bandit learning: Nearoptimal regret with efficient communication. In _Proc. ICLR_ , 2020. 

- Guoyizhe Wei, Feng Wang, Anshul Shah, and Rama Chellappa. Dual prompt tuning for domainaware federated learning. In _Proc. ECCV Workshop_ , 2023. 

- Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, Quoc V. Le, and Denny Zhou. Chain-of-thought prompting elicits reasoning in large language models. In _Proc. NeurIPS_ , 2022. 

- Zhaoxuan Wu, Xiaoqiang Lin, Zhongxiang Dai, Wenyang Hu, Yao Shu, See-Kiong Ng, Patrick Jaillet, and Bryan Kian Hsiang Low. Prompt optimization with EASE? efficient ordering-aware automated selection of exemplars. In _Proc. NeurIPS_ , 2024. 

- Chengrun Yang, Xuezhi Wang, Yifeng Lu, Hanxiao Liu, Quoc V Le, Denny Zhou, and Xinyun Chen. Large language models as optimizers. In _Proc. ICLR_ , 2024. 

- Chun-Pai Yang, Kan Zheng, and Shou-De Lin. Plhf: Prompt optimization with few-shot human feedback. _arXiv preprint arXiv:2505.07886_ , 2025. 

12 

Preprint. 

- Ziyu Ye, Hao-Yang Chen, Yong-Qiang Hu, Zhen-Yu Su, Qing-An Yao, Yu-Hong Liu, Xiao-Rong Lai, and Yi-Feng Wu. Align-Pro: A principled approach to prompt optimization for llm alignment. _arXiv preprint arXiv:2308.11585_ , 2023. 

- Yisong Yue, Josef Broder, Robert Kleinberg, and Thorsten Joachims. The k-armed dueling bandits problem. _Journal of Computer and System Sciences_ , 2012. 

- Ruichen Zhang, Zechu Li, Zhaoxuan Wu, Zhongxiang Dai, Yao Shu, and Bryan Kian Hsiang Low. FedBPT: Efficient federated black-box prompt tuning for large language models. In _Proc. NeurIPS_ , 2023. 

- Haodong Zhao, Wei Du, Fangqi Li, Peixuan Li, and Gongshen Liu. Fedprompt: Communicationefficient and privacy-preserving prompt tuning in federated learning. In _Proc. ICASSP_ , 2023. 

- Yongchao Zhou, Andrei Ioan Muresanu, Ziwen Han, Keiran Paster, Silviu Pitis, Harris Chan, and Jimmy Ba. Large language models are human-level prompt engineers. In _Proc. ICLR_ , 2023. 

## A ADDITIONAL RELATED WORK 

The performance of Large Language Models (LLMs) is highly sensitive to the quality of input prompts (Zhou et al., 2023; Lin et al., 2024b). While carefully handcrafted prompts (Brown et al., 2020; Wei et al., 2022) can substantially enhance model capabilities, the manual design process is time-consuming and heavily reliant on expert intuition. To address this challenge, early studies focused on white-box prompt optimization, including AutoPrompt (Shin et al., 2020), Prefix-Tuning (Li & Liang, 2021), P-Tuning (Liu et al., 2021), and Prompt Tuning (Lester et al., 2021). More recently, increasing attention has been devoted to black-box prompt optimization (Yang et al., 2024; Ma˜nas et al., 2024; Juneja et al., 2025; Schneider et al., 2024), with representative methods such as GRIPS (Prasad et al., 2023), BDPL (Diao et al., 2023), PRewrite (Kong et al., 2024), PromptAgent (Wang et al., 2024), and APO (Pryzant et al., 2023). RLPrompt (Deng et al., 2022) addresses the discrete black-box setting by optimizing a probability distribution over prompts, from which candidates are sampled to identify the optimal one. Evolutionary approaches, such as EvoPrompt (Guo et al., 2024) and Promptbreeder (Fernando et al., 2024), employ mutation and crossover to iteratively improve prompts. Zhou et al. (Zhou et al., 2023) introduced APE, which leverages an LLM to generate candidate instructions and refines those with high evaluation scores. However, these approaches often require extensive sampling and validation, making them sample-inefficient. A key direction has been reframing black-box prompt optimization as a continuous problem, as in InstructZero (Chen et al., 2023) and ZOPO (Hu et al., 2024). Building on this idea, INSTINCT (Lin et al., 2024b) employs neural bandits to sequentially select instructions to query, leveraging neural networks to better capture the relationship between prompts and their performance, thereby enabling more efficient optimization. 

Recent work has investigated prompt optimization in scenarios where direct human feedback is difficult to obtain and only preference feedback is available. BPO (Luo et al., 2023) trains an independent optimizer that automatically rewrites initial prompts using paired preference data, encouraging black-box LLMs to produce better responses. Align-Pro (Ye et al., 2023) develops a theoretical framework based on the Bradley–Terry model to analyze and guide optimization through pairwise comparisons. APOHF (Lin et al., 2024a) formulates prompt optimization as a dueling bandits problem, directly leveraging pairwise preferences (e.g., A is better than B) to efficiently identify the best prompt among candidates. Building on this idea, PLHF (Yang et al., 2025) extends preference-based optimization to a few-shot setting, demonstrating that high-quality prompts can be identified with only a small number of comparisons, thereby greatly reducing annotation costs. 

## B MORE DETAILS ON THE EXPERIMENTAL SETTING 

### B.1 DATASETS AND MODELS 

**Datasets.** We use 29 tasks from the Instruction-Induction dataset (Lin et al., 2024b), excluding the auto-debugging task which contains only 8 instances, and the Cause-and-Effect task. The Causeand-Effect task is an open-ended reasoning problem where multiple answers may be reasonable, but 

13 

Preprint. 

only one ground-truth is provided. Existing metrics cannot accurately evaluate responses, and most automatic scores are generally zero. For example, a few instances are: 

- Cause: “The child hurt their knee.” Effect: “The child started crying.” 

- Cause: “My car got dirty.” Effect: “I washed the car.” 

- Cause: “Someone fainted.” Effect: “Someone called 911.” 

For the BBH dataset (Suzgun et al., 2023), we adopt 24 tasks, excluding 3 tasks that overlap with Instruction-Induction to avoid double evaluation. 

**Models.** Our experiments are conducted on three LLMs, _OpenAI/GPT-3.5-turbo-0613_ , _OpenAI/GPT-4o-mini_ , and _Qwen/Qwen3-235B-A22B-2507_ via the OpenRouter API. We use MPNet (Song et al., 2020) as the embedding model. 

### B.2 PROMPT SPACE GENERATION 

To simulate a realistic federated setting, we adopt the APE algorithm (Zhou et al., 2023) to construct a prompt pool from a small initial task description (i.e., a set of input–output exemplars). From this pool, each agent samples both shared and personalized prompts, thereby capturing the inherent data heterogeneity—where shared prompts model the common knowledge across agents, while personalized prompts reflect the distinct distributions, preferences, and contextual variations specific to each client. 

**Prompt Template.** We follow INSTINCT (Lin et al., 2024b) for prompt template to automatically generate prompt space. We use 5 exemplars in datasets to query LLM to induct prompt. 

### **Prompt Generation Template** 

Input: [INPUT] Output: [OUTPUT] _<_ More exemplars... _>_ Input: [INPUT] Output: [OUTPUT] The instruction was to 

Figure 7: Prompt Generation template for prompt space generation. 

### **Prompt Generation Example** 

Input: [Today is Christmas Eve of 1937. What is the date 10 days later?] Output: [01/03/1938] _<_ More exemplars... _>_ Input: [Jane thought today is 3/11/2002, but today is in fact Mar 12, which is 1 day later. What is the date 24 hours later?] Output: [03/13/2002] The instruction was to 

Figure 8: Illustrative example of prompt generation with the template. 

### B.3 IMPROVED EVALUATION METHOD 

**Evaluation Challenges.** Due to the complex nature of the BBH tasks, we observed that large language models (LLMs) often generate detailed explanations along with their final answers, unlike the more direct outputs seen in the Instruction-Induction tasks. This behavior was particularly prevalent 

14 

Preprint. 

when using models such as GPT-4o-mini and Qwen3. A small number of tasks in the InstructionInduction dataset also exhibited this tendency toward verbose responses. Standard evaluation metrics such as exact match, contain, or F1-score proved unreliable in this context. Since the ground-truth answers are typically concise, the verbosity of model outputs frequently led to misclassification. In some cases, a model’s response was fully correct from a human perspective, yet automated metrics incorrectly assigned a score of zero. 

**Multi-choice Metric.** To mitigate this issue, we designed a new evaluation metric, termed Multichoice, specifically tailored to handle the verbose outputs of LLMs on BBH tasks. Our approach normalizes the model’s output and checks whether the ground-truth answer is present. In practice, we extract the final sentence of the model’s prediction and verify if it contains the ground-truth answer. 

**Metrics.** For BBH, we evaluate on 24 tasks using the Multi-choice metric. For Instruction-Induction (29 tasks), we follow Lin et al. (2024b) and adopt the same evaluation setup. Concretely, we use the F1 metric for “Common concept” and “Informal to formal”; exact set matching for “Orthography starts with” and “Taxonomy animal”; and label containment for “Synonyms”. For the remaining tasks, we apply exact match. Additionally, for “Diff” and “Odd one out”, when evaluated with GPT4o-mini or Qwen3 (where verbose explanations are frequent), we employ the Multi-choice metric instead of exact match. 

**Cached Prompt Scoring.** We leverage the alignment between prompts and their validation scores. Since our validation set is relatively large (50 samples), we observed that the scores obtained for a given prompt remain stable across repeated evaluations. Consequently, for all algorithms that require optimization over a prompt space (excluding FedOne and PromptBreeder, which do not depend on a prompt space), we evaluate each prompt once on the validation set and cache the resulting score for subsequent use. This strategy substantially reduces computation time while maintaining evaluation reliability. 

### B.4 HYPERPARAMETERS OF OUR ALGORITHMS 

In FedPOB, we set _λ_ = 1, _ν_ = 0 _._ 3, _D_ = 10 _._ 0, and _d_ = 768, where _d_ matches the output feature dimension of MPNet (Song et al., 2020). For FedPOB-Pref, we set _λ_ = 1 and use a learning rate of 0.001 to update _θt,a_ (line 7 of Algo. 3). Training is conducted for 30 iterations. 

The parameter _βt_ is time-dependent. Following (Huang et al., 2025), we set 


![](P011_images/P011.pdf-0015-08.png)

### Figure analysis

The figure presents the formula for the time-dependent parameter \(\beta_t\) used in the algorithm hyperparameters:

\[
\beta_t = \sqrt{2\log(1/\delta) + d\log\left(1 + \frac{t\kappa_\mu}{d\lambda}\right)}.
\]

Direct observations:
- The left-hand side defines \(\beta_t\), indicating a parameter that varies with iteration or time index \(t\).
- The expression is a square root over the sum of two logarithmic terms.
- The first term, \(2\log(1/\delta)\), depends on \(\delta\), likely a confidence or failure-probability parameter.
- The second term, \(d\log\left(1 + \frac{t\kappa_\mu}{d\lambda}\right)\), depends on feature dimension \(d\), time \(t\), number of agents \(\kappa_\mu\), and regularization-like parameter \(\lambda\).

Interpretation in context:
- The surrounding text states that \(\beta_t\) is time-dependent and follows Huang et al. (2025).
- The formula is part of Appendix B.4, which lists hyperparameters for FedPOB and FedPOB-Pref.
- The paper text specifies that \(\kappa_\mu\) denotes the number of agents and that \(d=768\) is used to match the MPNet output feature dimension.
- Visually, the equation indicates that \(\beta_t\) increases with \(t\) through a logarithmic dependence, suggesting a confidence-bound-style exploration parameter rather than a fixed scalar hyperparameter.


where _κµ_ denotes the number of agents and _d_ is the feature dimension (here _d_ = 768 for compatibility with MPNet). 

### B.5 HYPERPARAMETERS OF BASELINE AND FAIR COMPARISONS 

To ensure fairness, we set the total number of validation queries to be the same across all methods and report them consistently in our experimental results (see Tables 1, 2, and 3 in Sec. 4, as well as Table 5 in App. C). 

For score feedback baselines, only INSTINCT and our method share the same evaluation protocol, where each iteration queries the validation set once. Therefore, we ensure fairness by comparing the best reward obtained within the first 50 validation queries, rather than rewards at every single iteration. For preference-feedback baselines, all methods query the validation set twice per iteration, as two prompts are sampled for pairwise comparison. Running 50 iterations thus corresponds to 100 validation queries in total. For consistency, we report the score of the **first** (exploitation) prompt selected by each method. This is consistent with the work of Lin et al. (2024a). The reward curves are plotted across iterations, where the _x_ -axis represents the number of iterations (equivalently, preference-feedback steps). 

**Score Feedback.** For FedPOB, we run 50 iterations, thus querying the validation set 50 times. We report the best reward at the 50th iteration. For INSTINCT, we follow the default settings from their paper, which are consistent with our protocol (one query per iteration), and also report the 

15 

Preprint. 

Table 4: Query settings and reported metrics for different methods. 

||**Score Feedback**||
|---|---|---|
|**Method**|**Queries/Iter**<br>**Total Queries**|**Reported Metric**|
|FedPOB|1<br>50|Best reward at 50th iter.|
|INSTINCT|1<br>50|Best reward at 50th iter.|
|PromptBreeder|5<br>50|Best reward at 10th round.|
|FedOne|5<br>50|Best reward at 50th iter.|
||**Preference Feedback**||
|FedPOB-Pref|2<br>100|Best reward at 50th iter.|
|FLDB-OGD|2<br>100|Best reward at 50th iter.|
|FLDB-GD|2<br>100|Best reward at 50th iter.|
|APOHF|2<br>100|Best reward at 50th iter.|
|Double-TS|2<br>100|Best reward at 50th iter.|



best reward at the 50th iteration. For PromptBreeder, which is an evolutionary algorithm, half of the population queries the validation set in each round. With a population size of 10 (2 mutation prompts _×_ 5 thinking styles), this results in 5 queries per round and 50 queries in total over 10 rounds; we report the best reward at the 10th round. For FedOne, we follow the original paper and construct its vocabulary using the PMI algorithm, sampling frequent and high-quality words or word pairs from the large prompt domain generated by APE. The setup involves 10 agents, each sampling 5 prompts per round for 50 iterations. To ensure a fair comparison with 50 validation queries, we pair agents and take the maximum score among the prompts they generate as the final performance of FedOne. 

**Preference Feedback.** For methods based on preference feedback, including FedPOB-Pref, FLDB-OGD, FLDB-GD, APOHF, and Double-TS, each iteration samples two prompts and queries the validation set twice to obtain a pairwise preference. Running for 50 iterations therefore requires 100 validation queries in total. We report the best reward at the 50th iteration (based on 100 queries in total). Other hyperparameters follow their original settings to ensure a fair comparison. 

## C MORE EXPERIMENTAL RESULTS 

- C.1 ADDITIONAL EXPERIMENTS ON PROMPT DOMAIN GENERATION METHODS 

**Performance and Stability Across Different Prompt Domains.** In the experiment section, we use GPT-3.5-Turbo to generate the prompt domain via APE. To further validate that our algorithm achieves superior performance across different prompt domains generated by different methods, we replace GPT-3.5-Turbo with GPT-4o-mini while keeping all other settings fixed, such as running both our algorithm and the baselines under the same LLM model, GPT-3.5-Turbo. As shown in Fig. 9, Our method consistently achieves strong performance across different prompt domains, underscoring its robustness to domain variability. Beyond maintaining high accuracy, it is capable of identifying near-optimal prompts in a sample-efficient manner, thereby reducing the overall cost of API queries to LLMs. 

16 

Preprint. 


![](P011_images/P011.pdf-0017-01.png)


Figure 9: Performance across different prompt domains 

- C.2 COMPLETE RESULTS IN FEDPOB-PR E F 


![](P011_images/P011.pdf-0017-04.png)



![](P011_images/P011.pdf-0017-05.png)



![](P011_images/P011.pdf-0017-06.png)



![](P011_images/P011.pdf-0017-07.png)



![](P011_images/P011.pdf-0017-08.png)



![](P011_images/P011.pdf-0017-09.png)


Figure 10: More detailed comparison for FedPOB-Pref using GPT-3.5-Turbo. 

- C.3 COMPLETE RESULTS FOR FE DPOB 

Table 5: Performance comparison on the complete set of Instruction Induction tasks. 

17 

Preprint. 

|**Dataset**|**INSTINCT**|**PromptBreeder**|**FedOne (10 agents)**||**FedPOB**||
|---|---|---|---|---|---|---|
|||||1 Agent|3 Agents|10 Agents|
|Active to Passive|0.940_±_0.053|**1.000**_±_**0.000**|**1.000**_±_**0.000**|0.804_±_0.160|0.960_±_0.014|0.972_±_0.023|
|Auto Categorization|0.313_±_0.012|0.220_±_0.020|0.264_±_0.004|0.272_±_0.030|**0.308**_±_**0.018**|0.288_±_0.023|
|Antonyms|0.767_±_0.023|0.840_±_0.020|**0.870**_±_**0.005**|0.792_±_0.046|0.812_±_0.027|0.828_±_0.023|
|Common Concept|0.217_±_0.040|0.118_±_0.010|0.136_±_0.003|0.188_±_0.015|**0.210**_±_**0.007**|0.208_±_0.018|
|Diff|**1.000**_±_**0.000**|**1.000**_±_**0.000**|**1.000**_±_**0.000**|0.992_±_0.018|**1.000**_±_**0.000**|**1.000**_±_**0.000**|
|First Word Letter|**1.000**_±_**0.000**|1.000_±_1.000|0.713_±_0.089|1.000_±_1.000|**1.000**_±_**1.000**|**1.000**_±_**1.000**|
|Informal to Formal|0.570_±_0.020|0.521_±_0.067|**0.605**_±_**0.005**|0.528_±_0.028|0.528_±_0.039|0.570_±_0.030|
|Larger Animal|**0.993**_±_**0.012**|0.987_±_0.012|0.829_±_0.037|0.984_±_0.017|0.992_±_0.011|0.989_±_0.011|
|Letters List|**1.000**_±_**0.000**|**1.000**_±_**0.000**|0.831_±_0.095|0.952_±_0.107|**1.000**_±_**0.000**|**1.000**_±_**0.000**|
|Negation|0.860_±_0.020|**0.927**_±_**0.012**|0.897_±_0.010|0.856_±_0.061|0.940_±_0.014|0.920_±_0.032|
|Num to Verbal|**1.000**_±_**0.000**|**1.000**_±_**0.000**|**1.000**_±_**0.000**|**1.000**_±_**0.000**|**1.000**_±_**0.000**|**1.000**_±_**0.000**|
|Orthography Starts With|0.767_±_0.214|0.813_±_0.061|0.436_±_0.024|0.804_±_0.100|0.828_±_0.056|**0.832**_±_**0.087**|
|Rhymes|0.493_±_0.142|0.393_±_0.031|**0.916**_±_**0.027**|0.664_±_0.120|0.776_±_0.187|0.844_±_0.106|
|Second Word Letter|0.847_±_0.110|0.947_±_0.042|0.625_±_0.034|0.792_±_0.199|0.880_±_0.157|**0.972**_±_**0.023**|
|Sentence Similarity|0.467_±_0.031|0.380_±_0.020|0.360_±_0.035|**0.540**_±_**0.094**|0.508_±_0.082|0.448_±_0.018|
|Sentiment|0.973_±_0.012|0.993_±_0.012|**0.996**_±_**0.002**|0.988_±_0.018|0.972_±_0.023|0.972_±_0.027|
|Singular to Plural|0.993_±_0.012|**1.000**_±_**0.000**|**1.000**_±_**0.000**|**1.000**_±_**0.000**|0.996_±_0.009|**1.000**_±_**0.000**|
|Sum|**1.000**_±_**0.000**|**1.000**_±_**0.000**|**1.000**_±_**0.000**|0.984_±_0.036|**1.000**_±_**0.000**|**1.000**_±_**0.000**|
|Synonyms|0.327_±_0.150|0.333_±_0.115|0.320_±_0.023|0.324_±_0.103|0.296_±_0.041|**0.384**_±_**0.124**|
|Taxonomy Animal|0.947_±_0.023|**0.967**_±_**0.042**|0.805_±_0.026|0.924_±_0.073|0.980_±_0.024|0.972_±_0.034|
|Translation En-De|0.820_±_0.020|0.820_±_0.060|**0.927**_±_**0.004**|0.820_±_0.047|0.840_±_0.032|0.868_±_0.036|
|Translation En-Es|0.747_±_0.042|0.746_±_0.023|**0.950**_±_**0.012**|0.756_±_0.026|0.740_±_0.072|0.728_±_0.030|
|Translation En-Fr|**0.947**_±_**0.023**|0.920_±_0.040|0.919_±_0.005|0.944_±_0.033|0.940_±_0.283|0.948_±_0.018|
|Word in Context|0.553_±_0.058|**0.620**_±_**0.040**|0.409_±_0.091|0.460_±_0.084|0.640_±_0.020|0.608_±_0.036|
|Object Counting|0.520_±_0.106|0.473_±_0.110|0.497_±_0.019|0.520_±_0.074|**0.616**_±_**0.039**|0.588_±_0.050|
|Odd One Out|**0.867**_±_**0.058**|0.833_±_0.116|0.859_±_0.024|0.800_±_0.122|0.900_±_0.000|**0.900**_±_**0.000**|
|Periodic Elements|**1.000**_±_**0.000**|**1.000**_±_**0.000**|0.946_±_0.017|0.976_±_0.054|**1.000**_±_**0.000**|**1.000**_±_**0.000**|
|Word Sorting|0.753_±_0.058|0.753_±_0.099|0.497_±_0.026|0.756_±_0.093|0.744_±_0.065|**0.828**_±_**0.063**|
|Word Unscrambling|0.687_±_0.012|0.687_±_0.023|**0.728**_±_**0.005**|0.724_±_0.046|0.716_±_0.026|0.720_±_0.028|
|Average 29 Task|0.7715|0.7687|0.7356|0.7637|0.7977|**0.8068**|



- C.4 FURTHER EVALUATION ACROSS LLM MODELS 


![](P011_images/P011.pdf-0018-03.png)



![](P011_images/P011.pdf-0018-04.png)



![](P011_images/P011.pdf-0018-05.png)



![](P011_images/P011.pdf-0018-06.png)



![](P011_images/P011.pdf-0018-07.png)



![](P011_images/P011.pdf-0018-08.png)


Figure 11: More detailed comparison for FedPOB-Pref using GPT-4o-mini. 

18 

Preprint. 


![](P011_images/P011.pdf-0019-01.png)


Figure 12: More detailed comparison for FedPOB-Pref using Qwen3-235B-A22B-2507. 


![](P011_images/P011.pdf-0019-03.png)


Figure 14: The performance of FedPOB-Pref across different iterations Qwen3-235B-A22B2507. 

19 

Preprint. 

## D MATHEMATICAL PRINCIPLES OF THE LOCAL OBJECTIVE FUNCTION ADOPTED BY FE DPOB-PREF 

This section provides a rigorous mathematical analysis of the local objective function adopted by FedPOB-Pref for federated optimization. We derive the first-order optimality conditions and demonstrate the necessity of the linear dual term for ensuring convergence to a globally optimal and consistent solution. The results here provide theoretical support for the design of our FedPOB-Pref algorithm. 

### D.1 PROBLEM FORMULATION 

The standard federated learning objective is to minimize a global function _F_ ( _θ_ ), defined as the average of _m_ local client objectives _fi_ : R<sup>_d_</sup> _→_ R: 


![](P011_images/P011.pdf-0020-05.png)


For distributed optimization, this is equivalently formulated as a constrained problem with local variables _θi_ and a global consensus variable _θ_ : 


![](P011_images/P011.pdf-0020-07.png)


### D.2 THE AUGMENTED LAGRANGIAN METHOD 

The constrained problem in Eq. equation 6 can be solved using the Method of Multipliers. We introduce a dual variable (Lagrange multiplier) _ai ∈_ R<sup>_d_</sup> for each consensus constraint and add a quadratic penalty term for the constraint violation. This forms the augmented Lagrangian function _L_ : 


![](P011_images/P011.pdf-0020-10.png)


where _γ >_ 0 is a penalty parameter. An iterative algorithm then seeks a saddle point of this function. 

### D.3 FIRST-ORDER STATIONARITY CONDITIONS 

A stationary point of the augmented Lagrangian must satisfy _∇θiL_ = 0 and _∇θL_ = 0. These first-order conditions are derived as follows. 

The partial derivative with respect to a local variable _θi_ is: 


![](P011_images/P011.pdf-0020-15.png)


The partial derivative with respect to the global variable _θ_ is: 


![](P011_images/P011.pdf-0020-17.png)


To see the implication of these conditions, we sum Eq. equation 7 over all clients _i_ : 


![](P011_images/P011.pdf-0020-19.png)


Substituting the expression for<sup>�</sup> _i_<sup>_ai_from Eq.equation 8 into the above yields:</sup> 


![](P011_images/P011.pdf-0020-21.png)


20 

Preprint. 

which simplifies to: 


![](P011_images/P011.pdf-0021-02.png)


This proves that any stationary point of _L_ satisfies that the average of the local gradients is zero. If the solution is also primally feasible (i.e., _θi_ = _θ_ ), this condition becomes precisely the first-order optimality condition for the original global problem: 


![](P011_images/P011.pdf-0021-04.png)


### D.4 ANALYSIS OF THE FORMULATION 

D.4.1 PROOF OF NECESSITY FOR THE LINEAR DUAL TERM 

To prove that the linear term _⟨ai, θi −θ⟩_ is necessary, we analyze the case where it is omitted, relying solely on a quadratic penalty. The objective would be: 


![](P011_images/P011.pdf-0021-08.png)


The first-order condition with respect to _θi_ for this objective is: 


![](P011_images/P011.pdf-0021-10.png)


At a point of consensus where _θi_ = _θ_ for all _i_ , the penalty term vanishes, and the condition stringently requires that: 


![](P011_images/P011.pdf-0021-12.png)


This is a significantly stronger condition than global optimality, as it requires the solution _θ_ to be a stationary point for every client’s objective function simultaneously. Such a point is generally nonexistent for heterogeneous data distributions where local minima differ. Therefore, the inclusion of the linear dual term is mathematically essential to relax this condition to the correct global one, � _i_<sup>_∇fi_(</sup><sup>_θ_) = 0.</sup> 

D.4.2 INTERPRETATION OF THE DUAL VARIABLES AT CONVERGENCE In iterative methods that solve for a saddle point of _L_ , the dual variables are typically updated via dual ascent: 


![](P011_images/P011.pdf-0021-15.png)


If the algorithm converges to a primally feasible solution _θ_<sup>_⋆_</sup> , then lim _t→∞_ ( _θi_<sup>_t_+1</sup> _− θ_<sup>_t_+1</sup> ) = 0. At this limit, the stationarity condition from Eq. equation 7 must hold. As _θi → θ_<sup>_⋆_</sup> and _θ → θ_<sup>_⋆_</sup> , the equation implies that the dual variables converge to a fixed point _a_<sup>_⋆_</sup> _i_<sup>:</sup> 


![](P011_images/P011.pdf-0021-17.png)


This result provides a clear interpretation of the dual variable at the optimal solution: _a_<sup>_⋆_</sup> _i_<sup>is precisely</sup> the negative of the _i_ -th client’s scaled local gradient at the global optimum. The condition<sup>�</sup> _i_<sup>_a_</sup> _i_<sup>_⋆_= 0</sup> (from Eq. equation 8 at convergence) then mathematically guarantees that<sup>�</sup> _i_<sup>_∇fi_(</sup><sup>_θ⋆_)=0.The</sup> dual variables are thus the mechanism that allows local gradients to be non-zero while ensuring their sum is zero. 

## E OPTIMIZED PROMPTS FROM FEDPOB AND FEDPOB-PREF 

In this section, we present the optimized prompts together with their validation-set scores obtained by our FedPOB and FedPOB-Pref across all 53 tasks in both the Instruction Induction and BBH datasets after 50 optimization rounds. For each task in the tables, the _upper row_ reports the 

21 

Preprint. 

prompt and score optimized by FedPOB, while the _lower row_ corresponds to those optimized by FedPOB-Pref. 

Table 6: Optimized prompts and their scores for the Instruction Induction tasks 

|**Task**|**Prompt**|**Score**|
|---|---|---|
|active to Passive|Rewrite the sentence passively.<br>The sentence should be changed to passive voice: “The sentence is to be changed<br>from active to passive voice.”|0.972<br>0.993|
|antonyms|change the prefx of the word to make it have the opposite meaning.<br>fnd the opposite of each given word.|0.288<br>0.293|
|auto categorization|provide an appropriate category for each group of items.<br>identify the category or group that each set of inputs belong to.|0.828<br>0.840|
|common concept|provide a connection between two seemingly unrelated words or phrases.<br>provide a connection between two seemingly unrelated items.|0.208<br>0.250|
|diff|change the prefx of the word to make it have the opposite meaning.<br>Find the disparity between the initial number and the subsequent number in every<br>input.|1.000<br>1.000|
|frst word letter|Return the initial letter of every word provided as input.<br>State the initial letter of the specifed word.|1.000<br>1.000|
||rephrase the given sentences, not just provide synonyms. Here are the revised sen-<br>tences: Input: Can you complete all of these tasks? Output: Are you capable of<br>completing all of these tasks? Input: It is not advisable to take any action at this||
|informal to formal|time. Output: It is not recommended to do anything right now. Input: I’ll see you<br>this evening. Output: I anticipate seeing you tonight. Input: Would you like me to<br>accompany you? Output: Do you want me to go along with you? Input: The entire<br>narrative was fabricated. Output: The entire story was created.<br>rephrase the sentences using different words or phrases with the same meaning.|0.570<br>0.607|
|larger animal|choose the animal with the larger size or more strength.<br>choose the larger animal in each pair.|0.989<br>1.000|
|letters list|Add a space between each letter within a word.<br>Show each individual letter of the given word with a space between each letter.|1.000<br>1.000|
|negation|change the sentences to negative form, indicating that the statements are false.<br>change the statements to the opposite meaning.|0.920<br>0.947|
|num to verbal|Create a program that translates a provided number into its equivalent word form.<br>Write out the number in words from one to nine thousand, nine hundred and ninety-<br>nine.|1.000<br>1.000|
|object counting|count the total number of animals/items mentioned in the input sentence.<br>count the number of items listed in the input.|0.588<br>0.660|
|odd one out|Find the word that is not the same as the others in the group.<br>Select the word that is not related to the rest.|0.900<br>1.000|
|orthography start with|identify and output the word that starts with the specifed letter.<br>identify the word in the sentence that starts with the given letter.|0.832<br>0.907|
|periodic element|Give the names of the elements that match the provided atomic numbers.<br>List the names of the elements corresponding to the provided atomic numbers.|1.000<br>1.000|
|rhymes|fnd a word that rhymes with the given word, so in the case of ”buy”, the output would<br>be ”buy” as it already rhymes with itself.<br>change the frst letter of the word to make a new word.|0.844<br>0.993|
|second word letter|Retrieve the second letter from the given word.<br>Print the second-to-last letter of the input word.|0.972<br>0.980|
|sentence similarity|determine the likelihood that the two sentences are talking about the same topic. The<br>outputs provided are the level of certainty in the similarity of the topics discussed in<br>the sentences.|0.448|
||<br>compare the similarity between two sentences using a scale from 0 to 5, with 0 being<br>”defnitely not ” similar and 5 being ”perfectly ” similar. The output provided for<br>each pair of sentences indicates the level of similarity between them based on the<br>comparison.|0.613|
|sentiment|classify the input as either positive or negative based on the given statement.<br>provide an output (positive or negative) based on the given input.|0.972<br>1.000|
|singular to plural|pluralize the given input words.<br>add the letter ”s” to the end of the word.|1.000<br>1.000|
|sum|Calculate the total by adding the two numbers given as input.<br>sum the two inputted numbers.|1.000<br>1.000|
|synonyms|provide alternative words for the given inputs.|0.384|



_Continued on next page_ 

22 

Preprint. 

Table 6: Optimized prompts and their scores for the Instruction Induction tasks 

|**Task**|**Prompt**|**Score**|
|---|---|---|
||provide an antonym, synonym, or rhyme for the given word.|0.500|
|taxonomy animal|list the animals from the input words.<br>List the animals from the given words.|0.972<br>1.000|
|translation en-de|Translate the specifed words from English into German.<br>¨Ubersetze die gegebenen englischen W¨orter ins Deutsche.|0.868<br>0.887|
|translation en-es|traduce cada palabra al espa˜nol.<br>Convert the following words from English to Spanish: 1. wardrobe - armario 2. care<br>- preocuparse 3. dissatisfaction - insatisfacci´on 4. pond - estanque 5. trial - prueba|0.728<br>0.807|
|translation en-fr|translate the words provided from the English language to French.<br>turn the words into French.|0.948<br>0.960|
|word in context|determine if the word is used in the same context in both sentences. In this case, the<br>word ”academy” is used in different contexts in the two sentences, so the output is<br>”not the same.”<br>determine if the two sentences provided have the same meaning based on the given<br>word.|0.608<br>0.700|
|word sorting|sort the words in the provided list in alphabetical order. Each output should be a single<br>line of the sorted words, separated by spaces.<br>rearrange the words in the list in alphabetical order.|0.828<br>0.867|
|word unscrambling|Solve the jumbled words provided.<br>Arrange the scrambled words in the correct order.|0.720<br>0.793|



Table 7: Optimized prompts and their scores for the BBH tasks 

|**Task**|**Prompt**|**Score**|
|---|---|---|
|boolean expressions|Assess the provided logical expressions and produce the result.<br>Assess the provided logical expressions and give the resulting output.|0.844<br>0.860|
|date understanding|determine the date a specifc number of days or years ago from a given date.<br>determine the date one week ago or one week from today based on the given informa-<br>tion.|0.572<br>0.613|
|disambiguation qa|identify the antecedent of the pronoun in each sentence or state if it is ambiguous.<br>The correct antecedent for each sentence is as follows: ’1. (C) Ambiguous 2. (B) The<br>offce was Sam’s offce 3. (A) The technician completed the repair 4. (A) Alex could<br>not meet 5. (B) Asked the cleaner<br>explain the antecedent of the pronoun in the given sentences or state if it is ambiguous.<br>The correct antecedent for each sentence is provided in the output.|0.840<br>0.793|
|dyck languages|Finish the remaining part of the series and ensure that all parentheses are closed cor-<br>rectly.<br>Continue the sequence, ensuring that all parentheses are closed correctly.|0.680<br>0.740|
|formal fallacies|determine if the argument, given the explicitly stated premises, is deductively valid or<br>invalid. The output for all the provided inputs is ”invalid.”<br>determine whether the arguments, given the explicitly stated premises, are deductively<br>valid or invalid.|0.812<br>1.000|
|geometric shapes|Identify the geometric shape represented by the given SVG path element, with the<br>provided outputs indicating the corresponding shape based on the paths.<br>Determine the shape illustrated by the given SVG path element.|0.448<br>0.487|
|hyperbaton|choose the sentence with the correct adjective order, which is the order of opinion,<br>size, age, shape, color, origin, material, and purpose.<br>choose the sentence with the correct adjective order.|0.948<br>0.973|
|logical deduction fve<br>objects|determine which object is in a specifc position in the given set of objects based on the<br>information provided in each paragraph.<br>determine which object fnished frst in each scenario. The correct outputs are: 1. (C)<br>Ada fnished frst 2. (E) The falcon is the third from the left 3. (E) Amy fnished frst<br>4. (D) The plums are the second-cheapest 5. (D) The orange book is the third from<br>the left.|0.476<br>0.473|
|logical deduction seven<br>objects|determine which object is in a specifc position in the set of seven objects based on<br>the given statements.<br>determine which object is in a specifc position in the given arrangement of objects.|0.488<br>0.540|
|logical deduction three<br>objects|determine which object is in a specifc position based on the given information. In<br>each case, the correct output is provided based on the logical consistency of the state-<br>ments within the paragraph.|0.644|
||determine which object is in the leftmost position based on the given information.|0.653|



_Continued on next page_ 

23 

Preprint. 

Table 7: Optimized prompts and their scores for the BBH tasks 

|**Task**|**Prompt**|**Score**|
|---|---|---|
|movie recommendation|fnd a movie similar to the given list of movies. The correct options are selected based<br>on the similarity to the movies listed in the input.<br>fnd a movie similar to a given list of movies. The correct option for each set of movies<br>is as follows: 1. (C) The Usual Suspects 2. (D) Fargo 3. (A) Pulp Fiction 4. (B) The<br>Matrix 5. (A) Schindler’s List|0.732<br>0.780|
|multistep arithmetic two|Find the difference between the frst set of parentheses and the second set, and then<br>simplify the expression.<br>determine the outcome of the provided mathematical equation.|0.692<br>0.700|
|navigate|”Turn right. Take 10 steps. Turn around. Take 10 steps.”<br>take 9 steps left, then 10 steps forward, then 9 steps right, and fnally 10 steps back-<br>ward. By following these instructions, you would return to the starting point, so the<br>output is Yes.|0.716<br>0.773|
|penguins in a table|determine specifc information based on the given table of penguins and provide the<br>correct answer from the options provided.<br>determine specifc information about the penguins based on the given data and answer<br>the questions accordingly.|0.605<br>0.586|
|reasoning about colored<br>objects|determine the color or quantity of items based on their arrangement in a row.<br>determine the color of the item directly to the right of a specifed color in a given<br>arrangement of items.|0.568<br>0.580|
|ruin names|identify the humorous edit of the artist or movie name, and the correct answer for each<br>input is provided in the output.<br>fnd the humorous edit of the artist or movie name.|0.724<br>0.813|
|salient translation error<br>detection|Find the mistake in the given translations.<br>Find the mistake in the German to English translations given.|0.600<br>0.613|
|snarks|identify the sarcastic statement from the given options. The selected statement typ-<br>ically conveys an opposite meaning or is exaggerated in a way that highlights the<br>absurdity of the situation.<br>identify the sarcastic statement from the given options. In each case, the sarcastic<br>statement is one that implies the opposite of what it literally says, often highlighting<br>absurdity or exaggeration.|0.782<br>0.793|
|sports understanding|determine if the sentences were plausible based on common sports terminology.<br>determine if the sentences provided are plausible in a sports context.|0.564<br>0.580|
|temporal sequence|determine between what times the person could have gone to the specifed location<br>based on the given information about their activities throughout the day. The correct<br>time range is then provided as the output.<br>determine between what times the person could have gone to a specifc location based<br>on the given information. The correct options for each scenario are as follows: 1.<br>David could have gone to the construction site between 8am to 12pm (Option A). 2.<br>Leslie could have gone to the market between 11am to 5pm (Option B).|0.652<br>0.700|
|tracking shuffed objects<br>fve objects|determine who Claire is dancing with at the end of the dance. In the given scenario,<br>at the end of the dance, Claire is dancing with option (B) Sam.<br>determine who ends up with a specifc item or partner after a series of swaps or trades.|0.328<br>0.353|
|tracking shuffed objects<br>seven objects|determine the fnal position/book/ball of a specifc person/player after a series of<br>swaps.<br>determine the fnal partner, gift, ball, or book that a specifc person has at the end of<br>the given scenario.|0.256<br>0.293|
|tracking shuffed objects<br>three objects|determine the fnal position or item that Bob ends up with after a series of swaps.<br>determine who ends up with a specifc item after a series of swaps in a white elephant<br>gift exchange.|0.400<br>0.433|
|web of lies|determine if Inga tells the truth based on the statements given by the other individuals.<br>In this case, the answer is ”No” because Inga says Fidel tells the truth, but Fidel says<br>Vernell lies. Since there is a contradiction in the statements, Inga does not tell the<br>truth.<br>determine if Christie tells the truth based on the statements of the other individuals.<br>Christie says that Teressa tells the truth. Since Teressa says that Leda lies, and Leda<br>says that Shaunda lies, and Shaunda says that Ryan tells the truth, we can conclude<br>that Christie is telling the truth.|0.636<br>0.667|



24 

