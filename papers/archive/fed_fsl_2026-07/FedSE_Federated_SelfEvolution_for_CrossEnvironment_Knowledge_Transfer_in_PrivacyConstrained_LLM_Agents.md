# **Fed-SE: Federated Self-Evolution for Cross-Environment Knowledge Transfer in Privacy-Constrained LLM Agents** 

**Xiang Chen**<sup>**1**</sup> **Yuling Shi**<sup>**2**</sup> **Qizhen Lan**<sup>**3**</sup> **Yuchao Qiu**<sup>**1**</sup> **Min Wang**<sup>**4**</sup> **Xiaodong Gu**<sup>**2**</sup> **Yanfu Yan**<sup>**1**</sup> 

1Zhejiang University 2Shanghai Jiao Tong University 3UTHealth Houston 4University of Pennsylvania 

_{_ chenxianghz,yanfu _}_ @zju.edu.cn 


![](P007_images/P007.pdf-0001-05.png)


## **Abstract** 


![](P007_images/P007.pdf-0001-07.png)

### Figure analysis

**Purpose:** The figure conceptually contrasts direct federated adaptation for LLM agents with the proposed Federated Self-Evolution framework, emphasizing why naive FL is unstable and how Fed-SE improves privacy-preserving cross-environment knowledge transfer.

**Main structure and labels:**

- The diagram is split into two side-by-side sections:
  - **Left:** “Direct Federated Adaption (Challenges)”
  - **Right:** “Federated Self-Evolution (Fed-SE)”
- A vertical divider separates the problematic baseline approach from the proposed method.

**Left panel — Direct Federated Adaptation:**

- Shows multiple clients, including **Client A** and **Client C**, each associated with different task/environment icons.
- Both clients use **“All Traj.”** / all trajectories for training.
- The upper client path is labeled **“High Variance”** and leads to **“Local Gradient.”**
- The lower client path is labeled **“Naive Adaption.”**
- The section includes the label **“Training with All Data.”**
- At the bottom, a server icon and unstable arrows converge into a burst-like symbol labeled **“Training Instability.”**

**Direct observation:** the baseline side visually depicts noisy or conflicting trajectory signals feeding into local updates, which then produce unstable global training behavior.

**Interpretation:** this represents the paper’s claim that directly applying standard FL to heterogeneous, trajectory-based agent environments can produce high-variance gradients and unstable optimization.

**Right panel — Federated Self-Evolution:**

- Shows corresponding client-side processes for **Client A** and **Client C**.
- Each client applies **“Traj. Filtering”** using a funnel-like filtering symbol before local training.
- The upper path is labeled **“Stabilized”** and **“Local Evolution.”**
- The lower path is labeled **“Positive Learning.”**
- The section includes **“Training with Filtered Trajectories.”**
- The bottom model-aggregation block is labeled **“Model Parameters”** and contains:
  - **“Base Model (Frozen)”**
  - **“Adapter (LoRA)”**
- Updates from **Client A**, **Client B**, and **Client C** flow into a server through the adapter path.
- The bottom label reads **“Robust Knowledge Aggregation.”**

**Direct observation:** Fed-SE visually filters trajectories before local updates and aggregates only adapter-style low-rank parameter changes rather than full model parameters.

**Interpretation:** the figure communicates that Fed-SE reduces gradient noise by selecting useful trajectories locally, while preserving communication efficiency and privacy through LoRA-style federated aggregation.

**Connection to surrounding text:** The abstract and introduction state that privacy constraints prevent centralized collection of raw interaction data, while heterogeneous environments and sparse trajectory rewards make standard FL unstable. This figure summarizes the paper’s proposed solution: local self-evolution on filtered high-return trajectories plus global low-rank aggregation to enable cross-environment knowledge transfer without sharing raw data.


LLM (Large Language Model) agents are widely deployed in complex interactive tasks, yet privacy constraints often preclude centralized optimization and co-evolution across dynamic environments. Despite the demonstrated success of Federated Learning (FL) on static datasets, its effectiveness in open-ended, selfevolving agent systems remains largely unexplored. In such settings, the direct application of standard FL is particularly challenging, as heterogeneous tasks and sparse, trajectory-level reward signals give rise to severe gradient instability, which undermines the global optimization process. To bridge this gap, we propose Fed-SE, a Federated Self-Evolution framework for LLM agents that establishes a local evolution–global aggregation paradigm. Locally, agents employ parameter-efficient fine-tuning on filtered, high-return trajectories to achieve stable gradient updates. Globally, Fed-SE aggregates updates within a low-rank subspace, reducing communication cost across clients. Experiments across five heterogeneous environments demonstrate that Fed-SE improves average task success rates by 10% over the state-of-the-art FedIT, validating its effectiveness in cross-environment knowledge transfer under privacy constraints.<sup>1</sup> 

Figure 1: Static federated methods limit agent adaptation. Directly using FL suffers from high variance and gradient instability. Fed-SE addresses these issues via trajectory filtering for stable updates and low-rank aggregation for efficient communication. 

with environments (Liu et al., 2025; Chen et al., 2025; Fang et al., 2025; Cai et al., 2025), which enables agents to internalize task-specific knowledge and refine decision logic, tool usage strategies, and long-horizon planning. 

However, as real-world deployments are often subject to privacy constraints, platform compliance requirements and business risk controls preclude the centralized aggregation of raw interaction data (Yang et al., 2019; Li et al., 2021; Kairouz et al., 2021). Consequently, agents operating across multiple environments are optimized in isolation without cross-environment knowledge sharing (Cheng et al., 2024; Silagadze, 2023), limiting the development of generalizable agent capabilities (Zala et al., 2024; He et al., 2025). 

## **1 Introduction** 

LLM-based agents have demonstrated significant potential in complex interactive tasks, ranging from embodied intelligence to online service systems (Zitkovich et al., 2023; Belkhale et al., 2024; Li et al., 2025b; Peng et al., 2025; Shi et al., 2024; OpenAI et al., 2024; Shi et al., 2025a; Yang et al., 2025b; Zhang et al., 2025c,d,e). The enhancement of agent capabilities typically relies on the accumulation of experience through continuous interaction 

While Federated Learning (FL) (McMahan et al., 2023) offers a paradigm for collaborative training without exporting raw data, its application has largely been confined to static offline corpora (Jajoo, 2025; Wu et al., 2024a). Alternative approaches (Shi et al., 2025b; Wu et al., 2024c) avoid parameter training with context exchange but struggle to consolidate interaction experience into generalizable model parameters. Therefore, the 

> 1Our code is available at https://github.com/S oever/Federated-Agents-Evolution 

1 

open-ended, online self-evolution of agents across distributed environments still remains largely underexplored. 

Fundamental challenges arise when directly applying FL to online self-evolution of LLM agents. Specifically, Federated learning methods (McMahan et al., 2023; Zhang et al., 2023) like FedIT (Zhang et al., 2024) typically rely on clients producing locally meaningful and aggregatable updates from reasonably well-behaved training data. In cross-environment agent training, however, data are online-generated trajectories (Jin et al., 2022; Hwang and Hong, 2025). Under sparse rewards, a large fraction of trajectories carry little learning signal, which inflates the variance of policy-gradient estimates and causes severe gradient instability (Li et al., 2025c; Bjorck et al., 2022), thereby destabilizing global aggregation. Furthermore, the parameter scale of LLMs renders full-parameter synchronization prohibitively expensive (Qi et al., 2024; Singhal et al., 2025a). 

To address these challenges, we propose Federated Self-Evolution (Fed-SE), a framework for cross-environment knowledge transfer under privacy constraints. Specifically, clients perform local optimization on filtered successful trajectories to stabilize gradients, while the server aggregates updates within a low-rank subspace to reduce communication cost. Extensive evaluations across five heterogeneous environments and five base models demonstrate the effectiveness of Fed-SE. The main contributions are summarized as follows: 

- We explore cross-environment knowledge transfer for LLM agents under privacy constraints and propose Fed-SE, the **first** framework addressing this problem. 

- Fed-SE combines success-trajectory filtering with experience accumulation for lowvariance local optimization, and employs parameter-efficient aggregation within the low-rank adapter space for practical deployment. 

- Experiments on five environments show 10% absolute improvements over FedIT, with larger gains on long-horizon tasks. 

## **2 Preliminaries and Problem Setup** 

Agent-environment interaction is modeled as a Partially Observable Markov Decision Process 

(POMDP). At timestep _t_ , the policy _πθ_ , parameterized by _θ_ , generates a reasoning chain _ht_ and action _at_ based on instruction _u_ and history _Ht−_ 1. The probability of a trajectory _τ_ in environment _e_ with horizon _T_ decomposes as: 


![](P007_images/P007.pdf-0002-09.png)


where _ot_ denotes the observation received at step _t_ , _Ht−_ 1 = ( _o_ 1 _, h_ 1 _, a_ 1 _, . . . , ot−_ 1 _, ht−_ 1 _, at−_ 1) denotes the interaction history. 

Consider a federated system with _K_ clients, where each client _k_ holds a private environment _ek_ characterized by unique transition dynamics _Pk_ and task distributions _pk_ ( _u_ ). This heterogeneity induces non-identical local datasets _Dk_ : 


![](P007_images/P007.pdf-0002-12.png)


where _R_ ( _τ_ ) _∈{_ 0 _,_ 1 _}_ is the sparse binary reward indicating task success. 

The global goal is to maximize the weighted sum of local expected returns _Jk_ ( _θ_ ) = E _τ ∼Dk_ [ _R_ ( _τ_ )] via decentralized updates, strictly prohibiting raw trajectory sharing: 


![](P007_images/P007.pdf-0002-15.png)


where _ωk_ represents the aggregation weight for client _k_ (<sup>�</sup> _ωk_ = 1). 

This setting introduces several challenges. Sparse binary rewards cause most trajectories to carry little learning signal, leading to gradient instability that destabilizes local updates. Heterogeneous environment dynamics further exacerbate this issue by inducing divergent gradient directions across clients. Moreover, the parameter scale of LLMs renders full-parameter synchronization prohibitively expensive. 

## **3 Methodology** 

The Federated Self-Evolution (Fed-SE) framework enables collaborative agent training under privacy constraints. As illustrated in Figure 2, the training operates iteratively: each round consists of Local Agent Self-Evolution (Section 3.1), where clients optimize adapters using filtered trajectories, and Global Knowledge Aggregation (Section 3.2), where the server unifies distributed knowledge. 

2 


![](P007_images/P007.pdf-0003-00.png)



![](P007_images/P007.pdf-0003-01.png)



![](P007_images/P007.pdf-0003-02.png)



![](P007_images/P007.pdf-0003-03.png)



![](P007_images/P007.pdf-0003-04.png)



![](P007_images/P007.pdf-0003-05.png)



![](P007_images/P007.pdf-0003-06.png)



![](P007_images/P007.pdf-0003-07.png)



![](P007_images/P007.pdf-0003-08.png)



![](P007_images/P007.pdf-0003-09.png)


Figure 2: **Overview of the Fed-SE Framework.** Fed-SE operates in two phases: (1) local self-evolution, where clients optimize LoRA adapters using filtered successful trajectories, and (2) global aggregation, where the server averages distributed adapters and synchronizes them across clients. 

### **3.1 Local Agent Self-Evolution** 

To mitigate the high gradient variance characteristic of sparse reward settings, the standard RL objective is optimized via a surrogate lower bound. By leveraging importance sampling and treating the policy from the previous iteration as the reference distribution, the maximization of expected return is theoretically approximated by performing Maximum Likelihood Estimation (MLE) solely on the distribution of successful trajectories _D_<sup>+</sup> (see Appendix for details). Consequently, the optimization problem is formulated as: 


![](P007_images/P007.pdf-0003-13.png)


Guided by this formulation, the local evolution process proceeds as follows. 

**Exploration and Filtering.** The agent first interacts with the local environment using the current policy to generate exploration trajectories. Based on the binary reward signal, the subset of successful trajectories _Dk,t_<sup>succis filtered out as follows:</sup> 


![](P007_images/P007.pdf-0003-16.png)


where Θ represents the frozen base model parameters, and _ϕt_ denotes the trainable adapter parameters at round _t_ . 

**Experience Accumulation.** To alleviate distribution shift, a cumulative experience buffer merges 

historical data with newly discovered successful trajectories: 


![](P007_images/P007.pdf-0003-20.png)


The buffer is initialized with a small set of expert demonstrations _D_<sup>train</sup> = _D_<sup>expert</sup> to enable stable _k,_ 0 _k_ learning from the first round. 

**Parameter-Efficient Fine-Tuning.** The base model Θ is kept frozen, and only optimize the lightweight adapter parameters _ϕ_ for efficient finetuning. Specifically, we minimize the negative logprobability loss on the accumulated dataset as follows: 


![](P007_images/P007.pdf-0003-23.png)


where _ℓj_ ( _ϕ_ ) denotes the joint log-likelihood of the generated reasoning chain and action at step _j_ , defined as: 


![](P007_images/P007.pdf-0003-25.png)

### Figure analysis

The figure presents the overall workflow of the Federated Self-Evolution framework for training agents across multiple private environments.

**Purpose and structure**

- The diagram is organized into two main layers:
  - **Top layer:** “Central Server - Global Knowledge Aggregation.”
  - **Bottom layer:** “Parallel Multi-Environment Client Agents.”
- A horizontal privacy boundary between them is labeled with three key constraints/messages:
  - “Privacy Limits.”
  - “Upload and Download Adapters.”
  - “No Raw Data And Context Exchange.”
- This indicates that communication occurs through adapter parameters rather than raw trajectories, observations, prompts, or environment context.

**Central server workflow**

- The server receives **local knowledge** from multiple clients, represented by different task/environment icons.
- The central aggregation module is labeled **“Lora Aggregation.”**
  - Client-side LoRA parameters are shown as pairs such as \(A_1, B_1\), \(A_2, B_2\), and \(A_N, B_N\).
  - These are averaged into global adapter parameters \(\bar{A}, \bar{B}\).
- The final server-side block is **“Global Adapter Synchronization.”**
  - It visually shows local adapters being replaced or synchronized with the global averaged adapters.

**Client-side workflow**

- The lower portion shows multiple parallel clients: **Client Agent 1**, **Client Agent 2**, and **Client Agent N**, with ellipses indicating additional clients.
- Each client contains:
  - An agent model icon interacting with a private **Env** box.
  - A local **Exp Buffer** marked “Privacy,” indicating private retained experience.
  - A frozen or shared **Base Model** plus client-specific LoRA components \(A_k, B_k\).
  - A **Fine Tune** arrow from the private experience buffer to the local adapter/base-model block.
  - A large label **“Self-Evolution”**, emphasizing local improvement before server aggregation.
- Environment icons differ across clients, visually representing heterogeneous task distributions or transition dynamics.

**Information flow directly shown**

- Within each client, the agent interacts with its local environment and stores experience in a private buffer.
- Successful or useful local experiences are used to fine-tune client-specific LoRA adapters.
- Clients upload only adapter parameters \(A_k, B_k\) to the server.
- The server averages the uploaded LoRA parameters into \(\bar{A}, \bar{B}\).
- The global adapters are downloaded back to clients for synchronization before further local self-evolution.

**Direct observations versus interpretation**

- Directly observed: the figure explicitly labels the two phases as local self-evolution and global aggregation/synchronization, and explicitly states that raw data and context are not exchanged.
- Directly observed: only LoRA adapter matrices are communicated across the privacy boundary.
- Interpretation: the diagram supports the method’s stated goal of reducing communication cost and preserving privacy by avoiding full-model or raw-trajectory sharing.
- Interpretation: the use of different environment icons suggests the framework is designed for heterogeneous client environments.

**Connection to surrounding text**

- The figure corresponds to the methodology description of Fed-SE.
- It visually supports Section 3.1 by showing local exploration, experience buffering, and parameter-efficient fine-tuning of adapters on each client.
- It visually supports Section 3.2 by showing low-rank adapter aggregation at the server and synchronization of the global adapter back to all clients.
- The privacy boundary in the diagram is consistent with the paper’s federated setting, where raw trajectories and environment context are not shared.


where _oj_ is the observation at step _j_ , _hj_ denotes the generated reasoning chain, and _aj_ is the subsequent action. 

### **3.2 Global Knowledge Aggregation** 

The global phase distills environment-specific experiences into generalizable capabilities under strict communication constraints. 

3 

**Low-Rank Subspace Aggregation.** To reduce communication overhead and mitigate negative transfer from task heterogeneity, aggregation operates within the low-rank adapter space. The server computes unweighted averaging to prevent bias toward environments with abundant easy trajectories: 


![](P007_images/P007.pdf-0004-01.png)


**Global Parameter Synchronization.** To mitigate client drift, local parameters are reset to the global consensus before each round: 


![](P007_images/P007.pdf-0004-03.png)


**Algorithm 1** Federated Self-Evolution 

**Require:** Base model Θ, initial LoRA _ϕ_ 0, clients _{_ 1 _, . . . , K}_ , rounds _T_ 

- **Ensure:** Optimized global LoRA parameters _ϕT_ 1: **for** _t_ = 0 **to** _T −_ 1 **do** 

- 2: Broadcast _ϕt_ to all clients _k ∈{_ 1 _, . . . , K}_ 3: **for all** client _k_ **in parallel do** 

- 4: Explore with _π_ Θ _,ϕt_ , filter successful trajectories 


![](P007_images/P007.pdf-0004-09.png)


### **3.3 Theoretical Analysis** 

**Assumptions.** Standard assumptions in federated optimization are adopted: (1) _L_ -smoothness of each local objective _fk_ , (2) unbiased stochastic gradients with variance bounded by _σ_<sup>2</sup> , and (3) gradient norms bounded by _G_ . 

**Convergence Result.** Define the gradient heterogeneity at round _t_ as: 


![](P007_images/P007.pdf-0004-13.png)


where _∇fk_ ( _ϕt_ ) and _∇f_ ( _ϕt_ ) denote the local and global gradients at round _t_ , respectively. 

**Theorem 1** (Convergence of Fed-SE) **.** _Under Assumptions (1)-(3), with a learning rate satisfying_ 

<u>1</u> _η ≤_ 4 _LE_<sup>_, the convergence bound after Tcommu-_</sup> _nication rounds is given by:_ 


![](P007_images/P007.pdf-0004-17.png)


_where E is the number of local update steps per round, η represents the learning rate, K is the number of clients, and ζ_<sup>¯2</sup> = _T_ <u>1</u> � _t_<sup>_ζ_2(</sup><sup>_ϕt_)</sup><sup>_represents_</sup> _the path-averaged heterogeneity._ 

Theorem 1 guarantees convergence to a stationary point of the global average objective. Complete proofs are provided in Appendix A. 

## **4 Experimental Results** 

### **4.1 Experiments Setting** 

**Environment and Tasks.** Following the taxonomy established by Lu et al. (2024), federated multi-task learning scenarios can be categorized by the degree of task heterogeneity across clients. Our experimental setup adopts the most challenging configuration where each client is dedicated to a distinct environment, representing the extreme case of task heterogeneity. 

The proposed Fed-SE framework is evaluated across heterogeneous environments that cover diverse sequential decision-making capabilities: BabyAI (Chevalier-Boisvert et al., 2019) (embodied control and grounding), WebShop (Yao et al., 2022) (web interaction), TextCraft (Prasad et al., 2024) (hierarchical planning), MAZE (Abdulhai et al., 2025) (long-horizon memory), and Wordle (Abdulhai et al., 2025) (iterative reasoning). These environments have been widely adopted by prior work (Liu et al., 2023; Ma et al., 2024; Xi et al., 2024) for evaluating LLM-based agent capabilities, ensures a comprehensive assessment of agent generalization across distinct task dynamics. Performance is measured by task success rate, which indicates whether the agent successfully completes the given instruction within the environment. 

**Base Models.** Qwen2.5-7B (Yang et al., 2024a) is selected as the primary model for the main experiments. To comprehensively validate the generalizability of Fed-SE, the evaluation is also conducted across three dimensions: Llama2-7B-chat (Touvron et al., 2023) is included to examine whether 

4 

|Base Model|Method|BabyAI|WebShop|TextCraft|Maze|Wordle|**Avg**|
|---|---|---|---|---|---|---|---|
||||**_Main Resu_**|**_lts_**||||
||Pre-Trained|67.8|2.0|4.0|32.0|20.0|18.6|
||Local|90.0|65.0|63.0|48.0|12.0|65.7 (+47.0)|
|**Qwen2.5-7B**|Centralized|88.9|71.0|59.0|40.0|8.0|66.6 (+48.0)|
||FedIT|83.3|67.5|54.0|28.0|20.0|62.7 (+44.1)|
||**Fed-SE**|**93.3**|**73.0**|**67.0**|**68.0**|**32.0**|**73.2**(**+54.5**)|
|||_Di_|_fferent Model_|_Family_|||<br>|
||Pre-Trained|23.3|0.0|0.0|20.0|0.0|5.9|
||Local|67.8|54.0|33.0|20.0|4.0|47.3 (+41.4)|
|Llama2-7B|Centralized|61.1|59.0|36.0|32.0|0.0|49.3 (+43.4)|
||FedIT|70.0|61.0|49.0|28.0|**16.0**|55.7 (+49.8)|
||**Fed-SE**|**92.2**|**66.0**|**52.0**|**80.0**|**16.0**|**66.1**(**+60.2**)|
|||_D_<br>|_ifferent Mode_<br>|_l Scale_<br>|||<br>|
||Pre-Trained|48.9|3.0|1.0|24.0|4.0|13.2|
||Local|81.1|60.0|46.0|28.0|**16.0**|56.8 (+43.6)|
|Qwen2.5-3B|Centralized|83.3|61.5|48.0|20.0|4.0|57.3 (+44.1)|
||FedIT|72.2|63.5|54.0|20.0|4.0|57.3 (+44.1)|
||**Fed-SE**|**86.7**|**65.0**|**58.0**|**36.0**|8.0|**63.0**(**+49.8**)|
|||_Diffe_<br>|_rent Model G_<br>|_eneration_<br>|||<br>|
||Pre-Trained|43.3|7.0|15.0|**40.0**|0.0|17.7|
||Local|73.3|52.0|42.0|32.0|**4.0**|50.2 (+32.5)|
|Qwen3-1.7B|Centralized|70.0|44.5|**54.0**|0.0|0.0|46.8 (+29.1)|
||FedIT|61.1|50.5|46.0|8.0|**4.0**|46.6 (+28.9)|
||**Fed-SE**|**74.4**|**57.5**|46.0|**40.0**|**4.0**|**54.3**(**+36.6**)|
||Pre-Trained|40.0|1.5|1.0|8.0|**32.0**|11.4|
||Local|85.6|64.5|70.0|32.0|12.0|65.2 (+53.9)|
|Qwen3-8B|Centralized|78.9|33.5|63.0|32.0|8.0|48.0 (+36.6)|
||FedIT|85.6|64.5|61.0|12.0|4.0|61.6 (+50.2)|
||**Fed-SE**|**92.2**|**68.0**|**71.0**|**64.0**|12.0|**70.2**(**+58.9**)|



Table 1: Task-wise success rate across five base models. In the main results with Qwen2.5-7B, Fed-SE improves the average success rate by 10% over FedIT. This advantage is consistently observed across different model families, scales, and generations. 

Fed-SE’s effectiveness transfers across different model families; Qwen2.5-3B (Yang et al., 2024a) is evaluated to investigate the impact of model scale within the same model family; Qwen3-1.7B and Qwen3-8B (Yang et al., 2025a) are incorporated to assess Fed-SE’s applicability across different model architectures in the Qwen family. 

**Baselines.** As discussed in Section 6, to the best of our knowledge, no existing method addresses federated _online self-evolution_ for LLM agents. We establish a set of baselines to evaluate FedSE’s performance gains over static and isolated training paradigms: (1) **Pre-Trained** : The base model performs inference without fine-tuning. (2) **Local** (Hu et al., 2021): Agents fine-tuned independently on local static datasets using LoRA. (3) **Centralized** (Hu et al., 2021): Static datasets aggregated for joint LoRA-based instruction tuning. (4) **FedIT** (Zhang et al., 2024): FedIT represents a standard federated instruction-tuning approach based on _static_ expert demonstrations. We adapt FedIT, rather than other related ap- 

proaches (Wu et al., 2024b,c), from single-turn instruction–response pairs to multi-turn trajectory imitation for comparison, as this setting allows the contribution of online self-evolution to be evaluated more explicitly. 

Complete training implementation details are provided in Appendix B. 

### **4.2 Main Results** 

As detailed in Table 1 and Figure 3, Fed-SE achieves the highest average success rate across all base models, consistently outperforming all baselines. Through knowledge accumulation via local agent evolution and knowledge aggregation via global LoRA-based parameter sharing, Fed-SE enables cross-environment knowledge transfer under privacy constraints. 

**Knowledge Transfer under Privacy Constraints.** Table 1 shows that compared to Fed-IT, which also operates under privacy constraints, Fed-SE achieves improvements across all five environments rather than on isolated tasks. On Qwen2.5- 

5 


![](P007_images/P007.pdf-0006-00.png)

### Figure analysis

The figure is a multi-panel line chart comparing average success rate across communication rounds for five base models. Its purpose is to show how Fed-SE and FedIT evolve during federated training and how their final performance compares with static baselines.

**Panels and labels:**

| Panel | Base model | X-axis | Y-axis | Compared methods |
|---|---|---|---|---|
| Top-left | Llama2-7B | Communication Round | Success Rate (%) | Pre-Trained, Local, Centralized, FedIT, Fed-SE |
| Top-middle | Qwen2.5-3B | Communication Round | Success Rate (%) | Pre-Trained, Local, Centralized, FedIT, Fed-SE |
| Top-right | Qwen2.5-7B | Communication Round | Success Rate (%) | Pre-Trained, Local, Centralized, FedIT, Fed-SE |
| Bottom-left | Qwen3-1.7B | Communication Round | Success Rate (%) | Pre-Trained, Local, Centralized, FedIT, Fed-SE |
| Bottom-middle | Qwen3-8B | Communication Round | Success Rate (%) | Pre-Trained, Local, Centralized, FedIT, Fed-SE |

**Legend and visual encoding:** dotted horizontal line = Pre-Trained; dash-dot horizontal line = Local; dashed horizontal line = Centralized; red solid curve = FedIT; blue solid curve = Fed-SE. The horizontal baselines indicate fixed performance levels, while the red and blue curves show performance over 20 communication rounds.

**Direct observations:**

- In all five panels, Fed-SE rises over communication rounds and ends at or near the highest displayed success rate.
- Fed-SE is consistently above FedIT by the final communication round in every panel.
- The performance gap between Fed-SE and FedIT is visually large for Llama2-7B, Qwen2.5-7B, Qwen3-1.7B, and Qwen3-8B, and smaller for Qwen2.5-3B.
- Llama2-7B shows a strong early increase for both FedIT and Fed-SE, with Fed-SE crossing above the static Local/Centralized baselines and continuing to improve.
- Qwen2.5-3B shows FedIT and Fed-SE converging near the static Local/Centralized levels, with Fed-SE slightly higher toward the end.
- Qwen2.5-7B shows Fed-SE increasing to the highest final level, while FedIT plateaus lower and appears to dip slightly late in training.
- Qwen3-1.7B has lower absolute success rates and more fluctuation, especially for Fed-SE, but Fed-SE still finishes above FedIT and the static baselines.
- Qwen3-8B shows both online methods improving rapidly early, with Fed-SE continuing upward while FedIT levels off below the Local baseline late in training.

**Interpretation in relation to the paper text:** The figure supports the paper’s claim that Fed-SE benefits from online self-evolution plus federated LoRA aggregation. The increasing blue curves indicate knowledge accumulation over communication rounds, while the final advantage over FedIT suggests that using online successful trajectories provides benefits beyond static federated instruction tuning. The consistency across Llama2, Qwen2.5, and Qwen3 model families also supports the stated claim that the method generalizes across architectures and model scales.

**Uncertainty:** The chart does not annotate exact numeric values on the curves, so only qualitative comparisons and approximate trends should be used from the visual alone.


Figure 3: **Average success rate comparison across five base models.** The curves illustrate the training trajectories of Fed-SE and FedIT over communication rounds, while Local and Centralized represent static baselines trained on fixed datasets. Fed-SE achieves the highest average success rates after 20 communication rounds across diverse model architectures (Llama2, Qwen2.5, Qwen3) and parameter scales (1.7B to 8B). 

7B, Fed-SE outperforms Fed-IT on BabyAI (93.3% vs. 83.3%), WebShop (73.0% vs. 67.5%), TextCraft (67.0% vs. 54.0%), Maze (68.0% vs. 28.0%), and Wordle (32.0% vs. 20.0%). Similar patterns are observed across other base models. This indicates that combining online evolution with LoRA-based aggregation enables effective crossenvironment knowledge transfer without exposing raw trajectories. 

**Knowledge Accumulation via Online Evolution.** Figure 3 illustrates the training curves across communication rounds. The performance gap between Fed-SE and Fed-IT widens progressively as training proceeds, indicating that online evolution effectively converts interaction experiences into intrinsic model capabilities. However, this mechanism relies on the availability of successful trajectories. On Wordle, where successful experiences are difficult to obtain in early stages, the improvement remains limited. 

**Generalization Across Base Models.** As detailed in Table 1 and Figure 3, Fed-SE maintains consistent improvements across different model families, scales, and generations, demonstrating the stability and robustness of the framework. 

## **5 Analysis** 

### **5.1 Ablation Study** 

To verify the effectiveness of key components in Fed-SE, we conduct ablation studies using Llama2- 

7B-Chat as the base model and construct three variants: (1) _w/o History:_ Removes the experience accumulation mechanism, fine-tuning only with new data from the current round; (2) _w/o Filtering:_ Removes the success filter, including failed trajectories in training; (3) _w/ Weighted Avg:_ Uses weighted averaging based on the number of successful trajectories during aggregation. 

**Overall Performance Analysis.** As shown in Figure 4, the full Fed-SE achieves the highest average success rate (66.1%), outperforming all ablation variants on average. Notably, removing the success filter causes the most severe performance decay, with the average success rate plummeting to 40.5%, while removing history experience and changing the aggregation strategy also lead to varying degrees of performance decline. 

**Importance of Cumulative History.** While w/o History (64.1%) achieves a competitive average, this masks critical deficiencies in complex longhorizon tasks. Specifically, when evaluated on Maze (Figure 5a), performance plateaus at 40.0%, far below Fed-SE’s 80.0%. This significant drop indicates that relying solely on fresh data leads to the loss of prior capabilities during distribution adaptation. The historical buffer acts as an Experience Replay mechanism, effectively suppressing Catastrophic Forgetting and stabilizing policy oscillation against online distribution shifts, thereby sustaining the evolution of long-horizon planning. 

6 


![](P007_images/P007.pdf-0007-00.png)


Figure 4: **Impact of Key Components on Final Performance.** Removing the success filter causes a catastrophic performance drop (-26%), while excluding history or using weighted averaging also degrades the robust baseline (66%). 


![](P007_images/P007.pdf-0007-02.png)



![](P007_images/P007.pdf-0007-03.png)


Figure 5: **Evolution Process Analysis.** (a) The **Maze** task shows that removing history accumulation (w/o History) leads to suboptimal convergence. (b) The **Wordle** task demonstrates that removing the success filter (w/o Filtering) causes catastrophic performance collapse due to noise injection. 

**Necessity of Success Filtering.** Removing the success filter leads to the most drastic decay. In Wordle (Figure 5b), success rates collapse to zero after round 8. This confirms that failed trajectories act as misleading signals under behavioral cloning assumptions. Without strict filtering, the model 

erroneously imitates failure, rapidly contaminating global parameters and diverting policy optimization from the true objective. 

**Robustness of Aggregation Strategy.** Weighted averaging (59.8%) underperforms simple averaging, suggesting that under highly heterogeneous distributions, trajectory quantity does not correlate with gradient quality (e.g., BabyAI generates abundant simple samples). Weighted aggregation risks biasing the global model toward simpler tasks, weakening generalization on difficult ones. Therefore, simple averaging demonstrates superior robustness in balancing multi-task heterogeneity. 

### **5.2 Communication Efficiency** 

Communication overhead in FL is a critical constraint for deployment. The Fed-SE framework achieves parameter-efficient transmission through LoRA adapters, making communication overhead linearly related to the rank ( _r_ ). We analyze this trade-off using Llama2-7B-Chat as the base model. 

**Trade-off between Performance and Cost.** Figure 6 illustrates the trade-off between performance and communication cost under different ranks. The analysis reveals a typical trend of Diminishing Returns: increasing _r_ from 4 to 8 significantly boosts the success rate from 51 _._ 8% to 57 _._ 5% (+ **5** _._ **7** %), indicating insufficient model capacity at _r_ = 4. However, further increasing _r_ from 8 to 16 yields only a marginal gain from 57 _._ 5% to 59 _._ 1% (+ **1** _._ **6** %), while doubling the communication overhead ( **76** _._ **3** MB _→_ **152** _._ **5** MB). This comparison 

7 


![](P007_images/P007.pdf-0008-00.png)

### Figure analysis

Purpose: The figure evaluates the trade-off between model performance and communication cost for different LoRA ranks in the Fed-SE framework using Llama2-7B-Chat.

Chart structure:
- X-axis: LoRA Rank $(r)$ with categories $r=2$, $r=4$, $r=8$, and $r=16$.
- Left Y-axis: Average Success Rate (%) shown in blue.
- Right Y-axis: Communication Overhead (MB) shown in red.
- Legend: Blue line with circular markers represents Success Rate; red bars represent Communication Overhead.

Readable values:

| LoRA rank $(r)$ | Average success rate (%) | Communication overhead (MB) |
|---:|---:|---:|
| 2 | 47.0 | 19.1 |
| 4 | 51.8 | 38.1 |
| 8 | 57.5 | 76.3 |
| 16 | 59.1 | 152.5 |

Direct observations:
- Success rate increases from 47.0% at $r=2$ to 59.1% at $r=16$.
- The largest visible performance gain occurs from $r=4$ to $r=8$, rising from 51.8% to 57.5%.
- The gain from $r=8$ to $r=16$ is smaller, increasing only from 57.5% to 59.1%.
- Communication overhead rises from 19.1 MB at $r=2$ to 152.5 MB at $r=16$.
- Communication overhead approximately doubles when the rank doubles.

Interpretation:
- The visual pattern supports a diminishing-returns relationship: larger LoRA ranks improve success rate, but the marginal benefit decreases at higher ranks.
- Rank $r=8$ appears to provide a favorable balance, achieving most of the observed performance improvement while requiring about half the communication overhead of $r=16$.

Connection to surrounding text:
- The chart directly supports the paper's communication-efficiency discussion, where LoRA rank controls parameter-efficient transmission cost.
- The surrounding text highlights that increasing $r$ from 4 to 8 substantially improves success rate, while increasing from 8 to 16 yields only a marginal gain despite doubling communication overhead.
- This figure is used to justify selecting $r=8$ as the preferred trade-off point between model capacity, communication cost, and deployment feasibility.


Figure 6: Trade-off between model performance and communication cost across different LoRA ranks. 

compellingly demonstrates that _r_ = 8 represents the Optimal Trade-off Point between performance and communication cost. 

**Deployment Feasibility** As agents evolve, successful trajectories lengthen, leading to higher dynamic memory demands. Larger ranks (e.g., _r_ = 16) yield negligible gains but consume static memory needed for processing these long sequences. Thus, _r_ = 8 balances model capacity with memory constraints, preventing out-of-memory errors during later evolutionary stages. 

## **6 Related Work** 

### **6.1 LLM Agents and Self-Evolution** 

LLM agents have evolved from prompting-based systems to autonomous entities capable of planning, tool use, and multi-step reasoning (Yao et al., 2023; Schick et al., 2023; Wang et al., 2025b,a; Zhang et al., 2025b,a). Recent work enables agents to improve autonomously through self-evolution (Tao et al., 2024; ang Gao et al., 2025), with selfimprovement training emerging as the dominant paradigm, including self-rewarding (Yuan et al., 2025), self-play (Chen et al., 2024), and selfrefinement (Madaan et al., 2023). AgentGym (Xi et al., 2024) integrates these mechanisms with diverse environments for continuous improvement. Memory mechanisms further support persistent learning, from reflective memory (Shinn et al., 2023) to autonomous experience extraction (Zhao et al., 2024) and continual learning via causal abstractions (Majumder et al., 2023). For cross-environment generalization, modular architectures (Yin et al., 2024), self-evolving curricula (Qi et al., 2025), and cross-task experience sharing (Yang et al., 2024b) show promising results. 

However, existing approaches universally assume centralized trajectory access, which is problematic for distributed, privacy-constrained deployments. 

### **6.2 Federated Learning for Large Language Models and Agents** 

Federated learning for LLMs has focused on parameter-efficient fine-tuning (PEFT) to mitigate high communication costs (Singhal et al., 2025b; Sun et al., 2024; Koo et al., 2025; Li et al., 2025a). FedIT (Zhang et al., 2024) and FedPETuning (Zhang et al., 2023) established the efficacy of federated instruction tuning. While FedRLHF (Wu et al., 2024b) establishes a framework for privacypreserving policy optimization via client-specific feedback, it remains limited to single-turn preference alignment, lacking the multi-step reasoning capabilities required for autonomous agents. Meanwhile, FICAL (Wu et al., 2024c) pioneers federated in-context agent learning by transmitting knowledge compendiums, yet it relies on frozen models without parameter updates. Consequently, there is a lack of frameworks for the continuous, autonomous evolution of agents across heterogeneous environments under privacy constraints. To bridge this gap, we propose Fed-SE, a federated self-evolution framework that enables agents to improve their capabilities across distributed environments without raw data sharing. We adapt FedIT for comparison with our approach, as it performs federated parameter updates using static instruction data, thereby providing a clear contrast that isolates the contribution of online, trajectory-based self-evolution. 

## **7 Conclusion** 

This paper introduces Fed-SE, the first framework addressing federated online self-evolution for LLM agents, enabling cross-environment knowledge transfer under privacy constraints. Fed-SE establishes a local evolution–global aggregation paradigm where success-trajectory filtering with experience accumulation stabilizes local gradient updates, while unweighted low-rank aggregation reduces communication overhead and balances contributions across heterogeneous environments. Experiments across five environments and five base models demonstrate 6–10% absolute improvements over FedIT, with larger gains on long-horizon tasks. These results validate the feasibility of distilling generalizable agent capabilities from decentralized interaction experiences without raw data sharing. 

8 

## **Limitations** 

While transmitting adapter parameters prevents raw data exposure, the framework does not currently incorporate cryptographic techniques such as Differential Privacy or Homomorphic Encryption. This design choice prioritizes the high parameter precision required for complex reasoning but may leave the system vulnerable to advanced gradient reconstruction attacks. Additionally, the current reliance on synchronous Federated Averaging assumes consistent client connectivity. In real-world edge deployments, device heterogeneity and network instability could induce straggler effects, potentially hindering convergence efficiency. Furthermore, the global aggregation mechanism relies on standard element-wise averaging, advanced aggregation strategies for agents will be explored in future work. 

## **Ethics Considerations** 

This work focuses on methodological contributions in simulated environments. Deploying selfevolving agents in real-world scenarios would require additional safety measures to ensure alignment with human values. 

## **References** 

- Marwa Abdulhai, Isadora White, Charlie Victor Snell, Charles Sun, Joey Hong, Yuexiang Zhai, Kelvin Xu, and Sergey Levine. 2025. LMRL gym: Benchmarks for multi-turn reinforcement learning with language models. In _Forty-second International Conference on Machine Learning_ . 

- Huan ang Gao, Jiayi Geng, Wenyue Hua, Mengkang Hu, Xinzhe Juan, Hongzhang Liu, Shilong Liu, Jiahao Qiu, Xuan Qi, Yiran Wu, Hongru Wang, Han Xiao, Yuhang Zhou, Shaokun Zhang, Jiayi Zhang, Jinyu Xiang, Yixiong Fang, Qiwen Zhao, Dongrui Liu, and 8 others. 2025. A survey of self-evolving agents: On path to artificial super intelligence. _Preprint_ , arXiv:2507.21046. 

- Suneel Belkhale, Tianli Ding, Ted Xiao, Pierre Sermanet, Quan Vuong, Jonathan Tompson, Yevgen Chebotar, Debidatta Dwibedi, and Dorsa Sadigh. 2024. RT-H: action hierarchies using language. In _Robotics: Science and Systems XX, Delft, The Netherlands, July 15-19, 2024_ . 

- Johan Bjorck, Carla P. Gomes, and Kilian Q. Weinberger. 2022. Is high variance unavoidable in rl? a case study in continuous control. _Preprint_ , arXiv:2110.11222. 

- Zhicheng Cai, Xinyuan Guo, Yu Pei, JiangTao Feng, Jiangjie Chen, Ya-Qin Zhang, Wei-Ying Ma, Mingxuan Wang, and Hao Zhou. 2025. Flex: Continuous agent evolution via forward learning from experience. _Preprint_ , arXiv:2511.06449. 

- Silin Chen, Shaoxin Lin, Xiaodong Gu, Yuling Shi, Heng Lian, Longfei Yun, Dong Chen, Weiguo Sun, Lin Cao, and Qianxiang Wang. 2025. Swe-exp: Experience-driven software issue resolution. _arXiv preprint arXiv:2507.23361_ . 

- Zixiang Chen, Yihe Deng, Huizhuo Yuan, Kaixuan Ji, and Quanquan Gu. 2024. Self-play fine-tuning converts weak language models to strong language models. _Preprint_ , arXiv:2401.01335. 

- Yuheng Cheng, Ceyao Zhang, Zhengwen Zhang, Xiangrui Meng, Sirui Hong, Wenhao Li, Zihao Wang, Zekai Wang, Feng Yin, Junhua Zhao, and Xiuqiang He. 2024. Exploring large language model based intelligent agents: Definitions, methods, and prospects. _Preprint_ , arXiv:2401.03428. 

- Maxime Chevalier-Boisvert, Dzmitry Bahdanau, Salem Lahlou, Lucas Willems, Chitwan Saharia, Thien Huu Nguyen, and Yoshua Bengio. 2019. Babyai: A platform to study the sample efficiency of grounded language learning. In _7th International Conference on Learning Representations, ICLR 2019, New Orleans, LA, USA, May 6-9, 2019_ . OpenReview.net. 

- Jinyuan Fang, Yanwen Peng, Xi Zhang, Yingxu Wang, Xinhao Yi, Guibin Zhang, Yi Xu, Bin Wu, Siwei Liu, Zihao Li, Zhaochun Ren, Nikos Aletras, Xi Wang, Han Zhou, and Zaiqiao Meng. 2025. A comprehensive survey of self-evolving ai agents: A new paradigm bridging foundation models and lifelong agentic systems. _Preprint_ , arXiv:2508.07407. 

- Zhitao He, Zijun Liu, Peng Li, Yi R. Fung, Ming Yan, Ji Zhang, Fei Huang, and Yang Liu. 2025. Advancing language multi-agent learning with credit re-assignment for interactive environment generalization. _Preprint_ , arXiv:2502.14496. 

- Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu Chen. 2021. Lora: Low-rank adaptation of large language models. _Preprint_ , arXiv:2106.09685. 

- Ukjo Hwang and Songnam Hong. 2025. Federated reinforcement learning in heterogeneous environments. _Preprint_ , arXiv:2507.14487. 

- Gautam Jajoo. 2025. Federated learning with heterogeneous llms: Integrating small student client models with a large hungry model. In _AAAI-25, Sponsored by the Association for the Advancement of Artificial Intelligence, February 25 - March 4, 2025, Philadelphia, PA, USA_ , pages 29581–29583. AAAI Press. 

- Hao Jin, Yang Peng, Wenhao Yang, Shusen Wang, and Zhihua Zhang. 2022. Federated reinforcement learning with environment heterogeneity. In _Proceedings_ 

9 

_of The 25th International Conference on Artificial Intelligence and Statistics_ , volume 151 of _Proceedings of Machine Learning Research_ , pages 18–37. PMLR. 

- Peter Kairouz, H. Brendan McMahan, Brendan Avent, Aurelien Bellet, Mehdi Bennis, Arjun Nitin Bhagoji,´ Kallista Bonawitz, Zachary Charles, Graham Cormode, Rachel Cummings, Rafael G. L. D’Oliveira, Hubert Eichner, Salim El Rouayheb, David Evans, Josh Gardner, Zachary Garrett, Adria Gasc` on, Badih´ Ghazi, Phillip B. Gibbons, and 40 others. 2021. Advances and open problems in federated learning. _Preprint_ , arXiv:1912.04977. 

- Jabin Koo, Minwoo Jang, and Jungseul Ok. 2025. Towards robust and efficient federated low-rank adaptation with heterogeneous clients. _Preprint_ , arXiv:2410.22815. 

- Chuan Li, Qianyi Zhao, Fengran Mo, and Cen Chen. 2025a. Fedcot: Communication-efficient federated reasoning enhancement for large language models. _Preprint_ , arXiv:2508.10020. 

- Han Li, Yuling Shi, Shaoxin Lin, Xiaodong Gu, Heng Lian, Xin Wang, Yantao Jia, Tao Huang, and Qianxiang Wang. 2025b. Swe-debate: Competitive multiagent debate for software issue resolution. _arXiv preprint arXiv:2507.23348_ . 

- Qinbin Li, Yiqun Diao, Quan Chen, and Bingsheng He. 2021. Federated learning on non-iid data silos: An experimental study. _Preprint_ , arXiv:2102.02079. 

- Wenyun Li, Wenjie Huang, and Chen Sun. 2025c. Shaping sparse rewards in reinforcement learning: A semisupervised approach. _Preprint_ , arXiv:2501.19128. 

- Jiaqi Liu, Kaiwen Xiong, Peng Xia, Yiyang Zhou, Haonian Ji, Lu Feng, Siwei Han, Mingyu Ding, and Huaxiu Yao. 2025. Agent0-vl: Exploring selfevolving agent for tool-integrated vision-language reasoning. _Preprint_ , arXiv:2511.19900. 

- Xiao Liu, Hao Yu, Hanchen Zhang, Yifan Xu, Xuanyu Lei, Hanyu Lai, Yu Gu, Hangliang Ding, Kaiwen Men, Kejuan Yang, Shudan Zhang, Xiang Deng, Aohan Zeng, Zhengxiao Du, Chenhui Zhang, Sheng Shen, Tianjun Zhang, Yu Su, Huan Sun, and 3 others. 2023. Agentbench: Evaluating llms as agents. _arXiv preprint arXiv: 2308.03688_ . 

- Yuxiang Lu, Suizhi Huang, Yuwen Yang, Shalayiding Sirejiding, Yue Ding, and Hongtao Lu. 2024. Fedhca<sup>2</sup> : Towards hetero-client federated multi-task learning. _Preprint_ , arXiv:2311.13250. 

- Chang Ma, Junlei Zhang, Zhihao Zhu, Cheng Yang, Yujiu Yang, Yaohui Jin, Zhenzhong Lan, Lingpeng Kong, and Junxian He. 2024. Agentboard: An analytical evaluation board of multi-turn llm agents. _Preprint_ , arXiv:2401.13178. 

- Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler Hallinan, Luyu Gao, Sarah Wiegreffe, Uri Alon, Nouha Dziri, Shrimai Prabhumoye, Yiming Yang, 

Shashank Gupta, Bodhisattwa Prasad Majumder, Katherine Hermann, Sean Welleck, Amir Yazdanbakhsh, and Peter Clark. 2023. Self-refine: Iterative refinement with self-feedback. _Preprint_ , arXiv:2303.17651. 

- Bodhisattwa Prasad Majumder, Bhavana Dalvi Mishra, Peter Jansen, Oyvind Tafjord, Niket Tandon, Li Zhang, Chris Callison-Burch, and Peter Clark. 2023. Clin: A continually learning language agent for rapid task adaptation and generalization. _Preprint_ , arXiv:2310.10134. 

- H. Brendan McMahan, Eider Moore, Daniel Ramage, Seth Hampson, and Blaise Aguera¨ y Arcas. 2023. Communication-efficient learning of deep networks from decentralized data. _Preprint_ , arXiv:1602.05629. 

- OpenAI, Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, Red Avila, Igor Babuschkin, Suchir Balaji, Valerie Balcom, Paul Baltescu, Haiming Bao, Mohammad Bavarian, Jeff Belgum, and 262 others. 2024. Gpt-4 technical report. _Preprint_ , arXiv:2303.08774. 

- Weihan Peng, Yuling Shi, Yuhang Wang, Xinyun Zhang, Beijun Shen, and Xiaodong Gu. 2025. Swe-qa: Can language models answer repository-level code questions? _arXiv preprint arXiv:2509.14635_ . 

- Archiki Prasad, Alexander Koller, Mareike Hartmann, Peter Clark, Ashish Sabharwal, Mohit Bansal, and Tushar Khot. 2024. ADaPT: As-needed decomposition and planning with language models. In _Findings of the Association for Computational Linguistics: NAACL 2024_ , pages 4226–4252, Mexico City, Mexico. Association for Computational Linguistics. 

- Jiaxing Qi, Zhongzhi Luan, Shaohan Huang, Carol Fung, Hailong Yang, and Depei Qian. 2024. Fdlora: Personalized federated learning of large language model via dual lora tuning. _Preprint_ , arXiv:2406.07925. 

- Zehan Qi, Xiao Liu, Iat Long Iong, Hanyu Lai, Xueqiao Sun, Wenyi Zhao, Yu Yang, Xinyue Yang, Jiadai Sun, Shuntian Yao, Tianjie Zhang, Wei Xu, Jie Tang, and Yuxiao Dong. 2025. Webrl: Training llm web agents via self-evolving online curriculum reinforcement learning. _Preprint_ , arXiv:2411.02337. 

- Timo Schick, Jane Dwivedi-Yu, Roberto Dess`ı, Roberta Raileanu, Maria Lomeli, Luke Zettlemoyer, Nicola Cancedda, and Thomas Scialom. 2023. Toolformer: Language models can teach themselves to use tools. _Preprint_ , arXiv:2302.04761. 

- Yuling Shi, Yichun Qian, Hongyu Zhang, Beijun Shen, and Xiaodong Gu. 2025a. Longcodezip: Compress long context for code language models. _arXiv preprint arXiv:2510.00446_ . 

10 

- Yuling Shi, Songsong Wang, Chengcheng Wan, Min Wang, and Xiaodong Gu. 2024. From code to correctness: Closing the last mile of code generation with hierarchical debugging. _arXiv preprint arXiv:2410.01215_ . 

- Zitong Shi, Guancheng Wan, Wenke Huang, Guibin Zhang, Jiawei Shao, Mang Ye, and Carl Yang. 2025b. Privacy-enhancing paradigms within federated multiagent systems. _Preprint_ , arXiv:2503.08175. 

- Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik Narasimhan, and Shunyu Yao. 2023. Reflexion: language agents with verbal reinforcement learning. In _Advances in Neural Information Processing Systems_ , volume 36, pages 8634–8652. Curran Associates, Inc. 

- Z.K. Silagadze. 2023. On arxiv moderation system. _Journal of Informetrics_ , 17(3):101433. 

- Raghav Singhal, Kaustubh Ponkshe, and Praneeth Vepakomma. 2025a. Fedex-lora: Exact aggregation for federated and efficient fine-tuning of foundation models. _Preprint_ , arXiv:2410.09432. 

- Raghav Singhal, Kaustubh Ponkshe, and Praneeth Vepakomma. 2025b. Fedex-lora: Exact aggregation for federated and efficient fine-tuning of foundation models. _Preprint_ , arXiv:2410.09432. 

- Youbang Sun, Zitao Li, Yaliang Li, and Bolin Ding. 2024. Improving lora in privacy-preserving federated learning. _Preprint_ , arXiv:2403.12313. 

- Zhengwei Tao, Ting-En Lin, Xiancai Chen, Hangyu Li, Yuchuan Wu, Yongbin Li, Zhi Jin, Fei Huang, Dacheng Tao, and Jingren Zhou. 2024. A survey on self-evolution of large language models. _Preprint_ , arXiv:2404.14387. 

- Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, Dan Bikel, Lukas Blecher, Cristian Canton Ferrer, Moya Chen, Guillem Cucurull, David Esiobu, Jude Fernandes, Jeremy Fu, Wenyin Fu, and 49 others. 2023. Llama 2: Open foundation and fine-tuned chat models. _Preprint_ , arXiv:2307.09288. 

- Qiuchen Wang, Ruixue Ding, Zehui Chen, Weiqi Wu, Shihang Wang, Pengjun Xie, and Feng Zhao. 2025a. Vidorag: Visual document retrieval-augmented generation via dynamic iterative reasoning agents. _arXiv preprint arXiv:2502.18017_ . 

- Qiuchen Wang, Ruixue Ding, Yu Zeng, Zehui Chen, Lin Chen, Shihang Wang, Pengjun Xie, Fei Huang, and Feng Zhao. 2025b. Vrag-rl: Empower visionperception-based rag for visually rich information understanding via iterative reasoning with reinforcement learning. _arXiv preprint arXiv:2505.22019_ . 

- Feijie Wu, Zitao Li, Yaliang Li, Bolin Ding, and Jing Gao. 2024a. Fedbiot: LLM local fine-tuning in federated learning without full model. In _Proceedings of_ 

_the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining, KDD 2024, Barcelona, Spain, August 25-29, 2024_ , pages 3345–3355. ACM. 

- Feijie Wu, Xiaoze Liu, Haoyu Wang, Xingchen Wang, Lu Su, and Jing Gao. 2024b. Towards federated rlhf with aggregated client preference for llms. _arXiv preprint arXiv:2407.03038_ . 

- Panlong Wu, Kangshuo Li, Junbao Nan, and Fangxin Wang. 2024c. Federated in-context llm agent learning. _Preprint_ , arXiv:2412.08054. 

- Zhiheng Xi, Yiwen Ding, Wenxiang Chen, Boyang Hong, Honglin Guo, Junzhe Wang, Dingwen Yang, Chenyang Liao, Xin Guo, Wei He, and 1 others. 2024. Agentgym: Evolving large language model-based agents across diverse environments. _arXiv preprint arXiv:2406.04151_ . 

- An Yang, Anfeng Li, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chang Gao, Chengen Huang, Chenxu Lv, Chujie Zheng, Dayiheng Liu, Fan Zhou, Fei Huang, Feng Hu, Hao Ge, Haoran Wei, Huan Lin, Jialong Tang, and 41 others. 2025a. Qwen3 technical report. _Preprint_ , arXiv:2505.09388. 

- An Yang, Baosong Yang, Binyuan Hui, Bo Zheng, Bowen Yu, Chang Zhou, Chengpeng Li, Chengyuan Li, Dayiheng Liu, Fei Huang, Guanting Dong, Haoran Wei, Huan Lin, Jialong Tang, Jialin Wang, Jian Yang, Jianhong Tu, Jianwei Zhang, Jianxin Ma, and 43 others. 2024a. Qwen2 technical report. _Preprint_ , arXiv:2407.10671. 

- Chen Yang, Chenyang Zhao, Quanquan Gu, and Dongruo Zhou. 2024b. Cops: Empowering llm agents with provable cross-task experience sharing. _Preprint_ , arXiv:2410.16670. 

- Qiang Yang, Yang Liu, Tianjian Chen, and Yongxin Tong. 2019. Federated machine learning: Concept and applications. _Preprint_ , arXiv:1902.04885. 

- Xinwei Yang, Zhaofeng Liu, Chen Huang, Jiashuai Zhang, Tong Zhang, Yifan Zhang, and Wenqiang Lei. 2025b. Elaboration: A comprehensive benchmark on human-llm competitive programming. _arXiv preprint arXiv:2505.16667_ . 

- Shunyu Yao, Howard Chen, John Yang, and Karthik Narasimhan. 2022. Webshop: Towards scalable realworld web interaction with grounded language agents. In _Advances in Neural Information Processing Systems 35: Annual Conference on Neural Information Processing Systems 2022, NeurIPS 2022, New Orleans, LA, USA, November 28 - December 9, 2022_ . 

- Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik R. Narasimhan, and Yuan Cao. 2023. React: Synergizing reasoning and acting in language models. In _The Eleventh International Conference on Learning Representations, ICLR 2023, Kigali, Rwanda, May 1-5, 2023_ . OpenReview.net. 

11 

- Da Yin, Faeze Brahman, Abhilasha Ravichander, Khyathi Chandu, Kai-Wei Chang, Yejin Choi, and Bill Yuchen Lin. 2024. Agent lumos: Unified and modular training for open-source language agents. _Preprint_ , arXiv:2311.05657. 

- Weizhe Yuan, Richard Yuanzhe Pang, Kyunghyun Cho, Xian Li, Sainbayar Sukhbaatar, Jing Xu, and Jason Weston. 2025. Self-rewarding language models. _Preprint_ , arXiv:2401.10020. 

- Abhay Zala, Jaemin Cho, Han Lin, Jaehong Yoon, and Mohit Bansal. 2024. Envgen: Generating and adapting environments via llms for training embodied agents. _Preprint_ , arXiv:2403.12014. 

   - Andrew Zhao, Daniel Huang, Quentin Xu, Matthieu Lin, Yong-Jin Liu, and Gao Huang. 2024. Expel: Llm agents are experiential learners. _Preprint_ , arXiv:2308.10144. 

   - Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, Quan Vuong, Vincent Vanhoucke, Huong T. Tran, Radu Soricut, Anikait Singh, Jaspiar Singh, Pierre Sermanet, Pannag R. Sanketi, Grecia Salazar, and 35 others. 2023. RT-2: visionlanguage-action models transfer web knowledge to robotic control. In _Conference on Robot Learning, CoRL 2023, 6-9 November 2023, Atlanta, GA, USA_ , volume 229 of _Proceedings of Machine Learning Research_ , pages 2165–2183. PMLR. 

- Jianyi Zhang, Saeed Vahidian, Martin Kuo, Chunyuan Li, Ruiyi Zhang, Tong Yu, Yufan Zhou, Guoyin Wang, and Yiran Chen. 2024. Towards building the federated gpt: Federated instruction tuning. _Preprint_ , arXiv:2305.05644. 

- Jusheng Zhang, Kaitong Cai, Xiaoyang Guo, Sidi Liu, Qinhan Lv, Ruiqi Chen, Jing Yang, Yijia Fan, Xiaofei Sun, Jian Wang, Chen Ziliang, Liang Lin, and Keze Wang. 2025a. Mm-cot: A benchmark for probing visual chain-of-thought reasoning in multimodal models. _Preprint_ , arXiv:2512.08228. 

- Jusheng Zhang, Yijia Fan, Wenjun Lin, Ruiqi Chen, Haoyi Jiang, Wenhao Chai, Jian Wang, and Keze Wang. 2025b. GAM-agent: Game-theoretic and uncertainty-aware collaboration for complex visual reasoning. In _The Thirty-ninth Annual Conference on Neural Information Processing Systems (NeurIPS)_ . 

- Jusheng Zhang, Yijia Fan, Wen Zimo, Jian Wang, and Keze Wang. 2025c. Tri-MARF: A tri-modal multiagent responsive framework for comprehensive 3d object annotation. In _The Thirty-ninth Annual Conference on Neural Information Processing Systems (NeurIPS)_ . 

- Jusheng Zhang, Zimeng Huang, Yijia Fan, Ningyuan Liu, Mingyan Li, Zhuojie Yang, Jiawei Yao, Jian Wang, and Keze Wang. 2025d. KABB: Knowledgeaware bayesian bandits for dynamic expert coordination in multi-agent systems. In _Forty-second International Conference on Machine Learning (ICML)_ . 

- Jusheng Defense Zhang, Kaitong Cai, Yijia Fan, Ningyuan Liu, and Keze Wang. 2025e. MAT-agent: Adaptive multi-agent training optimization. In _The Thirty-ninth Annual Conference on Neural Information Processing Systems (NeurIPS)_ . 

- Zhuo Zhang, Yuanhang Yang, Yong Dai, Qifan Wang, Yue Yu, Lizhen Qu, and Zenglin Xu. 2023. FedPETuning: When federated learning meets the parameter-efficient tuning methods of pre-trained language models. In _Findings of the Association for Computational Linguistics: ACL 2023_ , pages 9963– 9977, Toronto, Canada. Association for Computational Linguistics. 

12 

## **A Complete Proof of Theorem 1** 

### **A.1 Surrogate Objective Derivation** 

The standard RL objective is _Jk_ ( _ϕ_ ) = E _τ ∼πϕ_ [ _R_ ( _τ_ )]. Using importance sampling with a reference policy _π_ ref (e.g., from the previous iteration): 


![](P007_images/P007.pdf-0013-03.png)


For binary rewards _R_ ( _τ_ ) _∈{_ 0 _,_ 1 _}_ , maximizing _Jk_ ( _ϕ_ ) is equivalent to maximizing the likelihood ratio on successful trajectories _Dk_<sup>+.</sup> Applying Jensen’s inequality to the logarithm: 


![](P007_images/P007.pdf-0013-05.png)


where _C_ is a constant independent of _ϕ_ . This yields the surrogate optimization objective _fk_ ( _ϕ_ ). 

### **A.2 Lemma: Client Drift Bound** 

**Lemma 1.** _The parameter drift for client k after e local steps is bounded by:_ 


![](P007_images/P007.pdf-0013-09.png)


_Proof._ Using the update rule _ϕ_<sup>(</sup> _k,t_<sup>_e_)</sup><sup>_−ϕt_</sup> = _−η_<sup>�</sup><sup>_e_</sup> _j_ =0<sup>_−_1</sup><sup>_g_</sup> _k,t_<sup>(</sup><sup>_j_)and Cauchy-Schwarz inequality:</sup> 


![](P007_images/P007.pdf-0013-11.png)


Since E _∥g∥_<sup>2</sup> _≤ G_<sup>2</sup> + _σ_<sup>2</sup> (Assumptions 2 and 3), the result follows. 

### **A.3 Proof of Theorem 1** 

**Step 1: Smoothness Analysis.** By the _L_ - smoothness of the global objective _f_ : 


![](P007_images/P007.pdf-0013-15.png)


where ∆ _t_ = _ϕt_ +1 _− ϕt_ = _− K_<sup>_<u>η</u>_</sup> � _Kk_ =1 � _Ee_ =0 _−_ 1<sup>_g_</sup> _k,t_<sup>(</sup><sup>_e_)</sup> is the global parameter update. 

**Step 2: Bounding the Inner Product.** The inner product term is decomposed as: 


![](P007_images/P007.pdf-0013-18.png)


where _δk,t_<sup>(</sup><sup>_e_)</sup> = _∇fk_ ( _ϕ_<sup>(</sup> _k,t_<sup>_e_))</sup><sup>_−∇fk_(</sup><sup>_ϕt_).</sup> Using Young’s inequality regarding _T_ 2: 


![](P007_images/P007.pdf-0013-20.png)


Summing over _k_ and _e_ , and defining the average drift _Et_ : 


![](P007_images/P007.pdf-0013-22.png)


Combining _T_ 1 and _T_ 2: 


![](P007_images/P007.pdf-0013-24.png)


**Step 3: Bounding the Update Norm.** The expected squared norm of the update E _∥_ ∆ _t∥_<sup>2</sup> is bounded by: 


![](P007_images/P007.pdf-0013-26.png)


**Step 4: Combining Results.** Substituting (A.2) and (A.3) into (A.1): 


![](P007_images/P007.pdf-0013-28.png)


13 

With _η ≤_ 4 _LE_ <u>1</u><sup>, we have (1</sup><sup>_−_3</sup><sup>_ηLE_)</sup><sup>_≥_</sup><sup><u>1</u></sup> 4<sup>.Substi-</sup> tuting the drift bound from Lemma 1: 


![](P007_images/P007.pdf-0014-01.png)


**Step 5: Final Convergence Bound.** Summing over _t_ = 0 to _T −_ 1 and rearranging: 


![](P007_images/P007.pdf-0014-03.png)


This confirms the convergence rate stated in Theorem 1. 

## **B Implementation Details** 

### **B.1 Environment and Dataset Specifications** 

We evaluate Fed-SE across five heterogeneous environments. The specifications and prompt designs for each task are derived from the AgentGym suite (Xi et al., 2024): 

- **BabyAI** (Chevalier-Boisvert et al., 2019) : A grid-world environment for embodied control where agents perform navigation and manipulation tasks. 

- **WebShop** (Yao et al., 2022): A simulated e- commerce environment for online shopping. The action space includes search[] and click[]. 

Wordle (955). The evaluation is conducted on test sets, with 200 tasks for WebShop, 100 for TextCraft, 90 for BabyAI, and 25 each for Maze and Wordle.. 

### **B.2 Training Hyperparameters** 

We implement Fed-SE using PyTorch and the LLaMA-Factory library. All experiments are conducted on **4 NVIDIA RTX A6000 GPUs** . 

**Local Evolution (Client-Side).** During the local self-evolution phase, we employ Low-Rank Adaptation (LoRA) for parameter-efficient fine-tuning. We freeze the pre-trained backbone and only update the adapter modules injected into all linear layers . For LoRA configuration, we set rank _r_ = 8, and alpha _α_ = 16 with target modules set to all linear layers. We use the AdamW optimizer with a learning rate of 5 _×_ 10<sup>_−_5</sup> , cosine learning rate scheduler, and no warmup steps. Each client trains for 2 epochs per communication round. The maximum context length is set to 4096 tokens to accommodate long interaction histories. All training is performed in bfloat16 precision for stability and efficiency. 

**Global Aggregation (Server-Side).** The federation process spans _T_ = 20 communication rounds. We establish a setup with _K_ = 5 clients, where each client is dedicated to one of the five heterogeneous tasks (BabyAI, WebShop, TextCraft, Maze, Wordle). At the end of each round, the server aggregates the LoRA adapters from all clients using unweighted element-wise averaging. 

### **B.3 Trajectory Collection and Filtering** 

- **TextCraft** (Prasad et al., 2024): A Minecraftstyle crafting environment requiring hierarchical planning to craft items using recursive recipes. 

- **Maze** (Abdulhai et al., 2025): A long-horizon navigation task testing memory and spatial reasoning capabilities. 

- **Wordle** (Abdulhai et al., 2025): A wordguessing game requiring iterative constraint satisfaction and reasoning. 

For the initial seed data ( _D_<sup>expert</sup> ), we utilize the AgentTraj dataset provided by AgentGym. The dataset sizes for each task are: WebShop (3930), BabyAI (810), TextCraft (374), Maze (215), and 

**Inference Configuration.** During the exploration phase, agents interact with the environment using temperature sampling with _T_ = 1 _._ 0 to encourage diverse trajectory generation. The maximum number of interaction turns is limited based on the task difficulty (e.g., 20 rounds for BabyAI, 10 for WebShop). 

**Filtering Mechanism.** We implement a strict binary outcome filter. A trajectory _τ_ is added to the experience buffer _D_<sup>train</sup> if and only if the environment returns a success flag success=1. Failed trajectories are discarded to prevent negative reinforcement. The experience buffer accumulates data throughout the 20 rounds without a capacity limit. 

14 

Table 2: Prompts for WebShop. 

#### **System Prompt:** 

You are web shopping. I will give you instructions about what to do. You have to follow the instructions. Every round I will give you an observation and a list of available actions, you have to respond an action based on the state and instruction. You can use search action if search is available. You can click one of the buttons in clickables. An action should be of the following structure: search[keywords] click[value] If the action is not valid, perform nothing. Keywords in search are up to you, but the value in click must be a value in the list of available actions. Remember that your keywords in search should be carefully designed. Your response should use the following format: Thought: I think ... Action: click[something] 

Table 3: Prompts for LMRL-Wordle. 

#### **Prompt:** 

You are an expert wordle player. Your objective is to guess a hidden 5 letter word. You have 6 attempts to guess it correctly and you should try to guess it in as few attempts as possible. When guessing the word, you should format your word as a space separated sequence of letters, like ”s h i r e” for example. After guessing the word, you will receive feedback from the game environment in the form of a sequence of 5 space separated letters like ”b y g g b”, where each letter indicates some information about the hidden word. The environment will return one of three letters - ”b”, ”g”, or ”y” - for each letter in the word you guessed. We describe the meaning of each letter below: ”b”: If the environment returns a ”b”, it means that the letter at that position in your guessed word is not in the hidden word. ”y”: If the environment returns a ”y”, it means that the letter at that position in your guessed word is in the hidden word but is not in the correct position. ”g”: If the environment returns a ”g”, it means that the letter at that position in your guessed word is in the hidden word and is in the correct position. As a note, if you guess an invalid word (e.g. not a 5 letter word or a word not in the vocabulary), the environment will respond with an ”invalid word” message. In general though, you should use this information returned by the environment to update your belief about what the hidden word might be and adjust your next guess accordingly. Here is the complete list of valid vocabulary words that are accepted by the game: “‘ _{{_ vocab _}}_ “‘ 

Here is an example. If the current status of the game is given as: “‘ guess 1: p a n i c feedback 1: b b y b b guess 2: f e l o n feedback 2: g b b y g “‘ Based on the feedback from the environment, you know that the first letter is ”f”, the last letter is ”n”, and there is an ”o” somewhere in the word, but it is not in the second to last position. You also know that there is not a ”p”, ”a”, ”i”, ”c”, ”e”, or ”l” in the word. Knowing this, you might guess the next word to be: Thought: I know that the first letter is ”f”, the last letter is ”n”, and there is an ”o” somewhere in the word, but it is not in the second to last position. I also know that there is not a ”p”, ”a”, ”i”, ”c”, ”e”, or ”l” in the word. A good word from the vocabulary to try might therefore be ”f r o w n”, since it is in the vocabulary, meets all known letter constraints, and we get to gain more information about the position of ”o”. Therefore this is a good guess to try next. 

Action: f r o w n 

Formally, your return should be in this format: Thought: _<_ Your Thought _>_ Action: _<_ The Word You Guess _>_ The guessed word is in the vocabulary, meets all known letter constraints, and we get to gain more information about the position of ”o”, so it is a good guess to try next. 

Now let us start a new game. Remember, the word you guess should be strictly in the vocabulary. You should return your thought and your word strictly in the formation mentioned above. 

Table 4: Prompts for BabyAI. 

#### **Prompt:** 

You are an exploration master that wants to finish every goal you are given. Every round I will give you an observation, and you have to respond an action and your thought based on the observation to finish the given task. You are placed in a room and you need to accomplish the given goal with actions. You can use the following actions: 

- turn right 

- turn left 

- move forward 

- go to _<_ obj _> <_ id _>_ 

- pick up _<_ obj _> <_ id _>_ 

- go through _<_ door _> <_ id _>_ : _<_ door _>_ must be an open door. 

- toggle and go through _<_ door _> <_ id _>_ : _<_ door _>_ can be a closed door or a locked door. If you want to open a locked door, you need to carry a key that is of the same color as the locked door. 

- toggle: there is a closed or locked door right in front of you and you can toggle it. Your response should use the following format: Thought: _<_ Your Thought _>_ 

Action: _<_ Your Action _>_ 

15 

Table 5: Prompts for TextCraft. 

|**Prompt:**|
|---|
|You are given few useful crafting recipes to craft items in Minecraft. Crafting commands are of the format ”craft [target<br>object] using [input ingredients]”. Every round I will give you an observation, you have to respond an action based on the<br>state and instruction. You can ”get” an object (ingredients) from the inventory or the environment, look-up the game inventory<br>by ”inventory”, or ”craft” (target) using any of the crafting commands. You can use ONLY these crafting commands provided,|
|do not use your own crafting commands. However, if the crafting command uses a generic ingredient like ”planks”, you<br>can use special types of the same ingredient e.g. ”dark oak planks” in the command instead. Your response should use the|
|following format:|
|Thought: ...|
|Action: ...|



Table 6: Prompts for LMRL-Maze. 

|**Prompt:**|
|---|
|You are an expert maze solver. Before answering, always: Step 1. List moves not blocked by walls. Remember, if there are<br>walls to your right, you can not move right. If there are walls to your left, you can not move left. If there are walls above you,<br>you can not move up. If there are walls below you, you can not move down. Step 2. Compute the distance for each move.<br>Step3. Choose the move with the shortest distance and not blocked by walls.<br>environment: The goal is at position 8, 6. Your current position is at position 1, 5. There are walls to your right, above you,<br>and below you. Thought:(dx, dy) = (x<br>~~g~~oal - x<br>~~c~~urr, y<br>~~g~~oal - y<br>~~c~~urr) = (8 - 1, 6 - 5) = (7, 1). I am left and up to the goal,<br>move right and move down will make me closer to the goal, but there are walls to my right, above me, and below me, I can<br>NOT move right, move up, move down, since I can only choose to move left.<br>environment: The goal is at position 8, 6. Your current position is at position 1, 4. There are walls above you, and below you.<br>Thought:(dx, dy) = (x<br>~~g~~oal - x<br>~~c~~urr, y<br>~~g~~oal - y<br>~~c~~urr) = (8 - 1, 6 - 4) = (7, 2). I am left and up to the goal, but there are walls<br>above me, and below me, since I can NOT move right, move up. Also I have tried move right to position 1, 5, where I can<br>NOT move right, move up, move down, since I can only choose to move left.<br>environment: The goal is at position 8, 6. Your current position is at position 5, 3. There are walls to your left, below you.|
|Thought: (dx, dy) = (x<br>~~g~~oal - x<br>~~c~~urr, y<br>~~g~~oal - y<br>~~c~~urr) = (8 - 5, 6 - 3) = (3, 3). I am left and up to the goal, move right and<br>move down will make me closer to the goal, but there are walls to my left, below me, I can NOT move left, move down,<br>since I choose to move right Action: move right<br>environment: The goal is at position 8, 6. Your current position is at position 5, 4. There are walls above you, below you.|
|Thought: (dx, dy) = (x<br>~~g~~oal - x<br>~~c~~urr, y<br>~~g~~oal - y<br>~~c~~urr) = (8 - 5, 6 - 4) = (3, 2). I am left and up to the goal, move right and<br>move down will make me closer to the goal, but there are walls to my left, below me, I can NOT move left, move down,<br>since I choose to move right Action: move right|
|<br>environment: The goal is at position 8, 6. Your current position is at position 5, 5. There are walls above you, below you.<br>Thought: (dx, dy) = (x<br>~~g~~oal - x<br>~~c~~urr, y<br>~~g~~oal - y<br>~~c~~urr) = (8 - 5, 6 - 5) = (3, 1). I am left and up to the goal, move right and<br>move down will make me closer to the goal, but there are walls to my left, below me, I can NOT move left, move down,<br>since I choose to move right Action: move right<br>environment: The goal is at position 8, 6. Your current position is at position 5, 6. There is a wall above you. Thought: (dx,<br>dy) = (x<br>~~g~~oal - x<br>~~c~~urr, y<br>~~g~~oal - y<br>~~c~~urr) = (8 - 5, 6 - 6) = (3, 0). I am up to the goal, move down will make me closer to the<br>goal, there are walls above me, I can NOT move up, since I choose to move down. Action: move down<br>environment: The goal is at position 8, 6. Your current position is at position 6, 6. There are walls to your right, to your left.|
|Thought: (dx, dy) = (x<br>~~g~~oal - x<br>~~c~~urr, y<br>~~g~~oal - y<br>~~c~~urr) = (8 - 6, 6 - 6) = (2, 0). I am up to the goal, move down will make me<br>closer to the goal, there are walls to my right, to my left, I can NOT move left, move right, since I choose to move down.<br>Action: move down<br>environment: The goal is at position 8, 6. Your current position is at position 7, 6. There are walls to your right, to your left.|
|Thought: (dx, dy) = (x<br>~~g~~oal - x<br>~~c~~urr, y<br>~~g~~oal - y<br>~~c~~urr) = (8 - 7, 6 - 6) = (1, 0). I am up to the goal, move down will make me<br>closer to the goal, there are walls to my right, to my left, I can NOT move left, move right, since I choose to move down.<br>Action: move down<br>environment: Success|
|Respond ONLY in the format below without extra text, you can ONLY give one action.<br>Thought: _<_concise reason_>_|
|Action: _<_move up—move down—move left—move right_>_|



16 

### **B.4 Prompting and Input Construction** 

We adopt a **ReAct (Reason + Act)** prompting strategy. The input to the model consists of: 

1. **System Instruction** : Defines the role of the agent, the environment rules, and the valid action format. 

2. **Interaction History** : The sequence of observations and actions from the current episode. 

The agent is required to output a response in the structured format: 

Thought: <Reasoning content> Action: <Action content> 

Prompts are detailed in Tables 2–6. 

## **C Additional Experiments and Case Study** 

To provide deeper insights into how Fed-SE improves agent capabilities, we present two categories of analysis: (1) per-environment performance curves across different base models, and (2) qualitative trajectory comparisons demonstrating behavioral changes before and after federated self-evolution. 

### **C.1 Performance Analysis Across Models** 

Figures 7–11 present the task success rates across five environments for different base models. Each figure shows the performance trajectory over 20 communication rounds, comparing Fed-SE against baseline methods including the pretrained model with no fine-tuning, Local training (without federation), Centralized training (with full data access), and Fed-IT (federated instruction tuning). 

**Llama2-7B (Figure 7).** Fed-SE demonstrates the most substantial improvements on Llama27B, achieving 66.1% average success rate compared to 55.7% for FedIT. The performance gap is particularly pronounced on Maze, where Fed-SE reaches 80.0% while FedIT achieves only 28.0%. On BabyAI, Fed-SE attains 92.2% success rate, substantially outperforming all baselines. These results indicate that Fed-SE effectively compensates for the relatively weaker instruction-following capabilities of older model architectures. 

**Qwen2.5-3B (Figure 8).** The smaller-scale Qwen2.5-3B model shows consistent improvements under Fed-SE, reaching 63.0% average success rate versus 57.3% for FedIT. Notably, Fed-SE 

achieves 36.0% on Maze compared to 20.0% for FedIT, demonstrating that the framework benefits models with limited parameter capacity. The performance curves reveal stable convergence across all environments, with Fed-SE maintaining advantages throughout the training process. 

**Qwen2.5-7B (Figure 9).** As the primary evaluation model, Qwen2.5-7B achieves the highest overall performance under Fed-SE with 73.2% average success rate, surpassing FedIT by 10.5 percentage points. Fed-SE shows improvements across all five environments, with the largest gain observed on Maze where success rate increases from 28.0% to 68.0%. The consistent upward trajectory across communication rounds confirms effective knowledge accumulation through online evolution. 

**Qwen3-1.7B (Figure 10).** Despite its compact size, Qwen3-1.7B under Fed-SE achieves 54.3% average success rate, outperforming FedIT by 7.7 percentage points. The model maintains competitive performance on Maze, reaching 40.0% success rate while FedIT drops to 8.0%. This demonstrates that Fed-SE’s trajectory filtering mechanism effectively extracts learning signals even with limited model capacity. 

**Qwen3-8B (Figure 11).** Fed-SE achieves 70.2% average success rate on Qwen3-8B, representing an 8.6 percentage point improvement over FedIT. The framework demonstrates particularly strong gains on Maze, improving from 12.0% under FedIT to 64.0% under Fed-SE. Interestingly, Wordle performance remains challenging across all methods, suggesting that tasks requiring iterative reasoning with sparse early-stage success signals present persistent difficulties regardless of model scale. 

### **C.2 Qualitative Trajectory Analysis** 

To illustrate the behavioral improvements achieved through Fed-SE, we present representative trajectory comparisons from each environment. Each case demonstrates how the agent’s decision-making evolves from suboptimal to successful strategies after federated self-evolution. 

**BabyAI Environment.** Figure 12 presents a navigation task where the agent must reach a target object (a red box) in a grid world. Before federated self-evolution, the agent fails to effectively parse spatial relationships from environment feedback. When given positional information about surrounding objects, the agent incorrectly interprets the rel- 

17 

ative positions and enters a repetitive turn left/right loop without making progress toward the goal. After federated self-evolution, the agent demonstrates improved spatial reasoning capabilities. It correctly interprets the position feedback, plans an efficient path by first moving forward to reduce distance, then adjusting direction based on updated environmental observations, ultimately reaching the goal successfully. 

**WebShop Environment.** Figure 13 demonstrates an online shopping task requiring the agent to find products matching specific constraints. Before federated self-evolution, the agent fails to carefully verify all product attributes against the requirements. In the example shown, the agent selects an item without checking whether it satisfies the pack quantity constraint, resulting in task failure. After federated self-evolution, the agent exhibits more thorough attribute verification behavior. It carefully examines each product’s details, identifies that a 2-pack bundle matches the requirement exactly, and completes the purchase successfully. This improvement reflects enhanced constraint satisfaction reasoning acquired through cross-environment knowledge sharing. 

walls, and efficiently navigates to the target using a more strategic approach. This behavioral change reflects enhanced spatial reasoning acquired from cross-environment experiences. 

**Wordle Environment.** Figure 16 illustrates a word-guessing task requiring iterative constraint satisfaction. Before federated self-evolution, the agent fails to properly utilize the feedback from previous guesses. When receiving feedback that letter “A” is in the word but in the wrong position (yellow), the agent repeatedly guesses words with “A” in similar positions, never successfully repositioning the letter. After federated self-evolution, the agent demonstrates improved constraint reasoning. Upon receiving yellow feedback for “A”, it explicitly reasons about trying “A” in a different position and selects subsequent guesses accordingly, ultimately finding the correct word. This improvement reflects enhanced iterative reasoning capabilities. 

**TextCraft Environment.** Figure 14 shows a crafting task requiring hierarchical planning to construct a wooden pickaxe. Before federated selfevolution, the agent exhibits insufficient resource gathering behavior. It collects only 1 wood unit and proceeds through the crafting chain, only to fail at the final step due to insufficient planks. After federated self-evolution, the agent demonstrates improved planning capabilities. It anticipates the complete resource requirements by gathering 2 wood units initially, then efficiently progresses through the crafting hierarchy with sufficient materials, successfully completing the task. This improvement highlights the acquisition of hierarchical planning skills through federated experience sharing. 

**Maze Environment.** Figure 15 presents a maze navigation task requiring the agent to reach a goal position while avoiding walls. Before federated self-evolution, the agent employs a naive strategy of repeatedly moving in one direction until blocked, then making arbitrary turns, which leads to getting stuck against walls. After federated self-evolution, the agent demonstrates improved path planning capabilities. It considers the goal position when selecting actions, avoids futile movements toward 

18 


![](P007_images/P007.pdf-0019-00.png)


Figure 7: Performance comparison on Llama2-7B across five heterogeneous environments. The curves show task success rates over 20 communication rounds. Fed-SE demonstrates consistent improvements across BabyAI, WebShop, TextCraft, and Maze, achieving performance comparable to or exceeding centralized training while preserving data locality. 


![](P007_images/P007.pdf-0019-02.png)


Figure 8: Performance comparison on Qwen2.5-3B. Despite the smaller model capacity, Fed-SE achieves substantial improvements particularly in BabyAI and WebShop environments, demonstrating that the federated self-evolution approach effectively leverages cross-environment knowledge sharing even with limited model parameters. 

19 


![](P007_images/P007.pdf-0020-00.png)


Figure 9: Performance comparison on Qwen2.5-7B. The larger model capacity enables more pronounced improvements across all environments. Fed-SE consistently outperforms Fed-IT and approaches the performance of centralized training, validating the effectiveness of low-rank subspace aggregation in the federated setting. 


![](P007_images/P007.pdf-0020-02.png)


Figure 10: Performance comparison on Qwen3-1.7B. This compact model from the Qwen3 family shows rapid early improvements with Fed-SE, particularly in WebShop and TextCraft environments, demonstrating the sample efficiency of our approach. 

20 


![](P007_images/P007.pdf-0021-00.png)


Figure 11: Performance comparison on Qwen3-8B. While this stronger base model achieves higher initial performance, Fed-SE still provides meaningful improvements, though the gains are smaller compared to weaker models due to capability saturation. This aligns with our observation that models with more room for improvement benefit more significantly from federated self-evolution. 


![](P007_images/P007.pdf-0021-02.png)


Figure 12: Case study in the BabyAI environment. Task instruction is to navigate to a red box. Before Fed-SE, the agent misinterprets spatial relationships and gets stuck in a turn left/right loop. After Fed-SE, the agent correctly parses position feedback and executes an efficient navigation sequence to reach the goal. 

21 


![](P007_images/P007.pdf-0022-00.png)

### Figure analysis

The figure presents a side-by-side qualitative case study for the WebShop environment, illustrating behavior before and after federated self-evolution.

**Purpose:** It demonstrates how Fed-SE improves instruction following in a shopping task by making the agent verify all constraints in the user request, not just partial keyword matches.

**Task instruction:** “Find dairy free brownie mix, pack of 2.”

**Layout and components:**
- The top title is **“Case Study: WebShop.”**
- A boxed instruction line states the shopping objective.
- The left panel is labeled **“Before Federated Self-Evolution.”**
- The right panel is labeled **“After Federated Self-Evolution.”**
- Each panel shows a text-based agent trajectory with environment state, thought, action, product listing, click action, and final result.

**Left panel direct observations — before Fed-SE:**
- The agent searches for `dairy free brownie mix pack of 2`.
- The search results shown include:
  - `Simple Mills Almond Flour Baking Mix, Brownie - Gluten Free, 12.02 oz - $28.98`
  - `Enjoy Life Baking Chocolate Semi-Sweet Mini Chips, Dairy Free - $23.76`
- The agent reasons: “Click the Enjoy Life option as it mentions dairy free explicitly.”
- It clicks product `B08P53LGS6`, then clicks `Buy Now`.
- The figure explicitly notes the error: **“Wrong item - not pack of 2.”**
- Final outcome is highlighted in red as **“Result: Failed.”**

**Right panel direct observations — after Fed-SE:**
- The agent uses the same search query.
- The displayed result is `Enjoy Life Brownie Mix, Dairy Free, Nut Free, Gluten Free, 2-Pack Bundle - $18.99` with product ID `B07VGBYQNC`.
- The agent reasons: “The 2-pack option matches the requirement exactly.”
- It clicks product `B07VGBYQNC`, then clicks `Buy Now`.
- Final outcome is highlighted in green as **“Result: Success.”**

**Comparison and interpretation:**
- Directly, the pre-Fed-SE trajectory matches only the “dairy free” attribute and fails to enforce the “brownie mix” and “pack of 2” constraints.
- Directly, the post-Fed-SE trajectory identifies a listing that explicitly satisfies the 2-pack requirement and completes the purchase successfully.
- Interpreted in the context of the paper, this example supports the claim that Fed-SE improves multi-constraint grounding and decision quality in WebShop tasks.

**Connection to surrounding text:** The surrounding caption describes this as Figure 13 and states that before Fed-SE the agent selected an item without verifying pack quantity, while after Fed-SE it matched product attributes to the requirements and selected the correct 2-pack option. The visual content is consistent with that description.


Figure 13: Case study in the WebShop environment. Task instruction is to find dairy free brownie mix in a pack of 2. Before Fed-SE, the agent selects an item without verifying the pack quantity constraint. After Fed-SE, the agent carefully matches product attributes to requirements and selects the correct 2-pack option. 

22 


![](P007_images/P007.pdf-0023-00.png)

### Figure analysis

The figure presents a side-by-side case study for the TextCraft environment with the task instruction: **“Craft a wooden pickaxe.”** Its purpose is to qualitatively compare an agent trajectory **before** and **after Federated Self-Evolution**.

Important components:
- **Title:** “Case Study: TextCraft.”
- **Instruction bar:** The task is to craft a wooden pickaxe.
- **Left panel:** “Before Federated Self-Evolution.”
- **Right panel:** “After Federated Self-Evolution.”
- Both panels show environment state, available commands, thoughts, actions, inventory updates, and final result.

Direct observations:
- In both cases, the environment begins with an empty inventory in a forest biome and available commands `[get, craft, inventory]`.
- **Before Federated Self-Evolution:**
  - The agent gets wood once, resulting in `{wood: 1}`.
  - It crafts 4 planks from 1 wood, then crafts 4 sticks using 2 planks.
  - Its inventory becomes `{plank: 2, stick: 4}`.
  - It attempts to craft a wooden pickaxe using `3 plank, 2 stick`.
  - The environment reports failure because `{plank: 1}` is missing.
  - Final result is marked **Failed**.
- **After Federated Self-Evolution:**
  - The agent explicitly reasons that it needs enough wood to craft planks and sticks for a pickaxe.
  - It gets wood twice, resulting in `{wood: 2}`.
  - It crafts 8 planks using 2 wood, then crafts 4 sticks using 2 planks.
  - Its inventory becomes `{plank: 6, stick: 4}` before crafting the pickaxe.
  - It successfully crafts a wooden pickaxe using `3 plank, 2 stick`.
  - Final inventory includes `{plank: 3, stick: 2, wooden_pickaxe: 1}`.
  - Final result is marked **Success**.

Interpretation:
- The visual comparison suggests that Federated Self-Evolution improves planning over multi-step resource dependencies.
- The pre-evolution agent follows a locally reasonable sequence but underestimates the required amount of wood, leading to a final resource shortfall.
- The post-evolution agent anticipates downstream crafting requirements, gathers sufficient resources, and completes the task successfully.

Connection to the surrounding paper text:
- This figure corresponds to the TextCraft case study described in the paper, illustrating that the proposed Fed-SE method helps agents plan ahead and avoid insufficient-resource failures in sequential decision-making tasks.


Figure 14: Case study in the TextCraft environment. Task instruction is to craft a wooden pickaxe. Before Fed-SE, the agent gathers insufficient resources (1 wood) and fails at the final crafting step. After Fed-SE, the agent plans ahead by gathering adequate resources (2 wood) and successfully completes the entire crafting sequence. 

23 


![](P007_images/P007.pdf-0024-00.png)

### Figure analysis

The figure presents a qualitative case study for the Maze environment, showing how an agent responds to the instruction “Navigate to goal position.” It compares behavior before and after Federated Self-Evolution.

- **Overall structure:** The figure is divided into two bordered columns:
  - **Left panel:** “Before Federated Self-Evolution”
  - **Right panel:** “After Federated Self-Evolution”
- **Shared task setup:** Both panels begin with the same environment state:
  - Current position: `(0, 0)`
  - Goal position: `(2, 2)`
  - Grid: `5x5 maze with walls`
  - Initially available actions: `move up`, `move right`

**Left panel: Before Federated Self-Evolution**

Direct observations:
- The agent states that it should move toward the goal by going right first.
- It takes `move right`, reaching `(1, 0)`.
- It then takes `move right` again, reaching `(2, 0)` and hitting a wall.
- It then attempts `move up`, reaching `(2, 1)`, but is blocked by a wall.
- The trajectory ends with “Cannot reach goal.”
- The panel marks the final outcome as **Result: Failed** in red.

Interpretation:
- The pre-Fed-SE agent appears to use a greedy or naive movement strategy that prioritizes moving directly toward the goal coordinates without adequately accounting for wall constraints.
- The failure illustrates poor spatial planning and insufficient adaptation to environmental feedback.

**Right panel: After Federated Self-Evolution**

Direct observations:
- The agent states that it should plan a clear path to reach `(2, 2)`.
- It first takes `move up`, reaching `(0, 1)`.
- It then takes `move up` again, reaching `(0, 2)`.
- From `(0, 2)`, the only listed available action is `move right`.
- It takes `move right` twice and reaches `(2, 2)`.
- The environment reports “Goal reached!”
- The panel marks the final outcome as **Result: Success** in green.

Interpretation:
- The post-Fed-SE agent demonstrates improved planning by choosing a route that avoids the apparent wall obstacle encountered in the earlier trajectory.
- The comparison supports the paper’s claim that federated self-evolution improves task execution through better use of environment feedback and goal-directed planning.

**Connection to surrounding text:** This figure corresponds to the described Maze case study, where the paper reports that the pre-Fed-SE agent gets stuck using a move-until-blocked strategy, while the post-Fed-SE agent plans a clearer path to the target coordinate `(2,2)` and succeeds.


Figure 15: Case study in the Maze environment. Task instruction is to navigate to the goal position (2,2). Before Fed-SE, the agent uses a naive move-until-blocked strategy and gets stuck against walls. After Fed-SE, the agent plans a clear path considering the goal position and navigates efficiently to reach the target. 

24 


![](P007_images/P007.pdf-0025-00.png)

### Figure analysis

The figure presents a side-by-side qualitative case study for a Wordle task, comparing agent behavior **before** and **after Federated Self-Evolution**.

**Purpose:** It illustrates how the method changes reasoning and action selection in an environment where feedback must be interpreted symbolically: green means correct position, yellow means the letter is present but in the wrong position, and gray means the letter is absent.

**Layout and components:**
- Title: **Case Study: Wordle**.
- Instruction bar: **Guess the 5-letter word**.
- Left panel: **Before Federated Self-Evolution**.
- Right panel: **After Federated Self-Evolution**.
- Each panel shows environment feedback, the agent's thoughts, actions, remaining attempts, and final result.

**Before Federated Self-Evolution:**
- The agent starts with `AUDIO`.
- Feedback indicates `A(yellow) U(gray) D(gray) I(gray) O(gray)`, so A is in the word but not in the first position.
- The agent then guesses `CRANE`, producing `A(yellow)` again, indicating A is still incorrectly positioned.
- The panel explicitly notes that the agent keeps misplacing the letter A.
- Direct observation: the final outcome is highlighted as **Result: Failed**.
- Interpretation: the agent recognizes that A is present but does not effectively use the positional constraint implied by yellow feedback.

**After Federated Self-Evolution:**
- The agent again begins with `AUDIO` and receives the same feedback: A is yellow and the other letters are gray.
- The agent explicitly reasons that A is in the word but not in position 1.
- It then guesses `BEACH`, placing A in a different position.
- Feedback shows `A(green)`, confirming A is now correctly positioned.
- The agent next guesses `DRAMA`, receiving all-green feedback: `D(green) R(green) A(green) M(green) A(green)`.
- Direct observation: the environment states, **Correct! The word was DRAMA.**
- The final outcome is highlighted as **Result: Success**.

**Key comparison:**
- Before training, the agent fails because it does not reliably convert yellow feedback into a positional constraint.
- After training, the agent uses the same initial evidence more effectively, moves A to a new position, confirms it as green, and reaches the correct answer.

**Connection to the paper text:**
This figure supports the surrounding claim that Fed-SE improves agents' ability to interpret feedback and adapt their decisions. In the Wordle setting, the improvement is specifically shown as better use of positional feedback, turning an initially failed reasoning pattern into a successful solution trajectory.


Figure 16: Case study in the Wordle environment. Task instruction is to guess the 5-letter word. Before Fed-SE, the agent ignores positional feedback and keeps misplacing letter “A”. After Fed-SE, the agent correctly interprets yellow feedback (letter present but wrong position) and strategically repositions letters in subsequent guesses to find the correct word. 

25 

