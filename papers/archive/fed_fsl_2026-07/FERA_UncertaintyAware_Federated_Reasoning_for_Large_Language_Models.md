# **FERA: Uncertainty-Aware Federated Reasoning for Large Language Models** 

**Ruhan Wang** Indiana University ruhwang@iu.edu 

### **Chengkai Huang** 

The University of New South Wales chengkai.huang1@unsw.edu.au 

### **Zhiyong Wang** 

The Chinese University of Hong Kong zhiyongwangwzy@gmail.com 

### **Junda Wu** 

University of California San Diego juw069@ucsd.edu 

**Rui Wang Tong Yu** Adobe Research Adobe Research ruiwan@adobe.com tyu@adobe.com 

### **Julian McAuley** 

University of California San Diego jmcauley@ucsd.edu 

### **Lina Yao** 

The University of New South Wales lina.yao@unsw.edu.au 

### **Dongruo Zhou** 

Indiana University dz13@iu.edu 

## **Abstract** 

Large language models (LLMs) exhibit strong reasoning capabilities when guided by high-quality demonstrations, yet such data is often distributed across organizations that cannot centralize it due to regulatory, proprietary, or institutional constraints. We study _federated reasoning_ , where a server improves multi-step reasoning by coordinating with heterogeneous clients holding private demonstrations, without centralized training or raw data sharing. The key challenge is that client reliability is query-dependent, while the server cannot inspect client data to determine which contributions are trustworthy. To address this, we propose _Uncertainty-Aware Federated Reasoning_ (FERA), a training-free framework based on iterative server–client co-refinement. Across communication rounds, clients generate reasoning traces with lightweight uncertainty estimates, and the server synthesizes them into improved reasoning that is redistributed as context for the next round, progressively improving both server outputs and client-side reasoning. Within each round, _Uncertainty-Aware Self-Critique Aggregation_ (UA-SCA) resolves conflicts among heterogeneous client traces through query-dependent trust weighting and structured cross-client verification. Rather than simply discarding low-quality traces, UA-SCA revises flawed reasoning steps to recover useful information. We provide theoretical guarantees showing that the proposed iterative protocol converges, and that uncertainty-aware weighting accelerates convergence. Experiments on multiple reasoning benchmarks show that FERA consistently outperforms both federated training and training-free baselines, achieving progressively higher accuracy across rounds while maintaining communication and computational efficiency. 

## **1 Introduction** 

Reasoning ability is fundamental to complex problem solving, as it enables a system to decompose high-level objectives into a coherent sequence of logical steps rather than relying on stored knowledge (Zhang et al., 2023b; Sun et al., 2023). To enhance such reasoning 

1 

capabilities, recent work has leveraged Large Language Models (LLMs) to generate explicit step-by-step deductive chains during problem solving (Wei et al., 2022; Wang et al., 2023). However, the reasoning performance of LLMs cannot be substantially improved by relying solely on their pre-trained capabilities, particularly for rigorous and structured tasks (Morishita et al., 2024; Shojaee et al., 2025). Effective reasoning enhancement instead depends on access to high-quality data that can guide and refine the generation of logical steps (Morishita et al., 2024; Cheng et al., 2025). In practice, such reasoning data are difficult to obtain, as they are often scattered across diverse domains and subject to privacy or proprietary constraints (Green et al., 2025; Rischke et al., 2022; Baack et al., 2025). As a result, a central research challenge is how to improve reasoning performance under limited data availability. For example, in a healthcare network where hospitals hold proprietary clinical data, a central server cannot pool data due to privacy regulations but can aggregate reasoning traces generated locally by each hospital’s LLM. We refer to this setting as _federated reasoning_ . 

Federated reasoning provides a way to improve LLM reasoning by allowing collaboration across decentralized data sources while keeping raw data local (Liu et al., 2024; Achiam et al., 2023; Wei et al., 2022; Kojima et al., 2022). Existing methods generally fall into training-based and training-free approaches. Training-based methods require clients to fine-tune local models and exchange parameters (Wang et al., 2024c; Wu et al., 2024a; Ma et al., 2023), which is costly for modern LLMs in both computation and communication (Yan et al., 2025; Shu et al., 2024; Liu et al., 2023; Che et al., 2023; Wang et al., 2024d; Liu et al., 2025). Training-free methods reduce this cost by exchanging only lightweight information, such as prompts or retrieved examples (Chen et al., 2025; Wang et al., 2025a; Wu et al., 2024c; Du et al., 2023). However, their performance is strongly influenced by cross-client heterogeneity. Under domain mismatch, local LLMs may produce overconfident yet systematically biased reasoning, leading the server to receive conflicting responses to the same query. Because each client reasons over _private, non-overlapping_ data, such disagreements reflect genuine information asymmetry rather than mere noise. However, the server cannot verify which client’s knowledge is most relevant to a given query. This challenge motivates the central question we address: 

How can a training-free federated reasoning framework progressively improve reasoning quality across rounds while reliably aggregating conflicting client contributions with query-dependent reliability? 

To address this question, we propose **Uncertainty-Aware Federated Reasoning (FERA)** . Our key contributions are: 

- We introduce FERA, a training-free _iterative co-refinement_ framework for federated reasoning (Figure 1). FERA operates over multiple communication rounds in which the server distributes its current reasoning context to clients, each client generates reasoning traces with uncertainty estimates using its private data, and the server synthesizes improved reasoning that is redistributed as enhanced context for the next round. This bidirectional loop allows both the server’s answers and clients’ local contexts to improve progressively, without parameter updates or data sharing. 

- To resolve conflicting reasoning within each round, we introduce **Uncertainty-Aware Self-Critique Aggregation (UA-SCA)** , which addresses the query-dependent reliability problem at the reasoning level rather than only at the answer level. UA-SCA assigns query-dependent trust weights based on token-level entropy, and employs structured self-critique where each client’s reasoning is cross-examined against competing answer groups at the server. This allows flawed reasoning steps to be identified and _revised_ using evidence from other clients, rather than simply discarded. Ablation studies (Section 5.4) confirm that uncertainty weighting and self-critique provide complementary gains. 

- We provide theoretical analysis under a simplified _linear self-attention_ model (Zhang et al., 2023a), proving that FERA’s iterative protocol converges to ground-truth answers as the number of demonstrations grows. Importantly, incorporating uncertainty-aware weights provably accelerates the convergence rate, providing principled motivation for the framework design. 

2 


![](P030_images/P030.pdf-0003-00.png)


Figure 1: Overview of the FERA framework. Over multiple rounds, the server distributes context to clients, who generate reasoning traces with uncertainty estimates from private data. The server refines its reasoning via **_UA-SCA_** and redistributes improved context, creating a co-refinement loop where both server outputs and client contexts improve simultaneously. Detailed explanations are provided in Section 4.2. 

- We evaluate FERA on general and mathematical reasoning benchmarks under heterogeneous client data. FERA consistently outperforms both training-based and training-free baselines, with accuracy improving across communication rounds, while maintaining significantly higher computation and communication efficiency than other baselines. 

## **2 Related Work** 

Recent advances in FL and LLMs increasingly highlight uncertainty as a key tool for handling heterogeneity and improving decision reliability (see Appendix A for details). In federated reasoning, existing methods can be broadly categorized into _training-based_ and _training-free_ approaches. Training-based methods, such as FedKSeed (Qin et al., 2023) and FLoRA (Wang et al., 2024c), improve performance via parameter updates but incur additional training cost and system complexity. In contrast, training-free methods (Liu et al., 2023; Chen et al., 2025; Wang et al., 2025a; Wu et al., 2024c; Du et al., 2023) are more lightweight but struggle with data heterogeneity and complex reasoning tasks. Among them, prompt aggregation methods (Liu et al., 2023; Chen et al., 2025) often rely on data homogeneity or retrieval quality, in-context learning approaches (Wang et al., 2025a; Wu et al., 2024c) are typically limited to simple QA settings, and debate-based frameworks (Du et al., 2023) require direct inter-client communication and treat all client outputs as equally trustworthy. Meanwhile, uncertainty quantification has shown broad effectiveness in FL for handling heterogeneity and model differences (Koutsoubis et al., 2025; Zhang & Yu, 2025; Wang et al., 2024a; Zhang et al., 2024b), and in LLMs for uncertainty decomposition, active learning, and adaptive reasoning (Hou et al., 2023; Huang et al., 2024; Wang et al., 2025b; Yang et al., 2023). These advances motivate FERA, which leverages uncertainty to enable training-free federated reasoning under heterogeneous client knowledge. 

## **3 Preliminaries** 

We consider a federated reasoning setting in which a central server coordinates _L_ clients under a standard client–server architecture. We first define the notation used throughout this paper. 

3 

**Algorithm 1** Uncertainty-Aware Self-Critique Aggregation 

**Require:** Query index _m_ , round _k_ , client submissions _{_ ( _s_<sup>_i_</sup> _{_ 1: _T}_ , _k_ , _m_<sup>,</sup><sup>_ai_</sup> _k_ , _m_<sup>,</sup><sup>_ui_</sup> _k_ , _m_<sup>)</sup><sup>_}_</sup> _i_<sup>_L_</sup> =1<sup>, the server</sup> LLM denoted by LLM<sup>_S_</sup> . **Ensure:** Aggregated reasoning–answer pair ( _s_<sup>_⋆_</sup> , _a_<sup>_⋆_</sup> ). 1: Partition _{_ ( _s_<sup>_i_</sup> _{_ 1: _T}_ , _k_ , _m_<sup>,</sup><sup>_ai_</sup> _k_ , _m_<sup>)</sup><sup>_}_</sup> _i_<sup>_L_</sup> =1<sup>into groups</sup><sup>_G_=</sup><sup>_{G}_based on</sup><sup>_am_.</sup> 2: **for** each group _G ∈G_ **do** 3: _SG ←_ Summarize( _{s_<sup>_i_</sup> _{_ 1: _T}_ , _k_ , _m_<sup>: (</sup><sup>_si_</sup> _{_ 1: _T}_ , _k_ , _m_<sup>,</sup><sup>_ai_</sup> _k_ , _m_<sup>)</sup><sup>_∈G}_;LLM</sup><sup>_S_).</sup> 4: **end for** 5: **for** _i_ = 1, . . . , _L_ **do** 6: Denote _G_ ( _i_ ) _∈G_ as the group which ( _s_<sup>_i_</sup> _{_ 1: _T}_ , _k_ , _m_<sup>,</sup><sup>_ai_</sup> _k_ , _m_<sup>) belongs to.</sup> 7: (� _s_<sup>_i_</sup> _{_ 1: _T}_ , _k_ , _m_<sup>, �</sup><sup>_ai_</sup> _k_ , _m_<sup>)</sup><sup>_←_SelfCritique((</sup><sup>_si_</sup> _{_ 1: _T}_ , _k_ , _m_<sup>,</sup><sup>_ai_</sup> _k_ , _m_<sup>),</sup><sup>_{SG_:</sup><sup>_G_=</sup><sup>_G_(</sup><sup>_i_)</sup><sup>_}_;LLM</sup><sup>_S_).</sup> 8: **end for** 9: Calculate weights _{wi}i_<sup>_L_</sup> =1<sup>based on 3.</sup> 10: ( _s{_ 1: _T}_ , _k_ +1, _m_ , _a{_ 1: _T}_ , _k_ +1, _m_ ) _←_ Aggregate( _{_ (� _s_<sup>_i_</sup> _{_ 1: _T}_ , _k_ , _m_<sup>, �</sup><sup>_ai_</sup> _k_ , _m_<sup>,</sup><sup>_wi_)</sup><sup>_}_</sup> _i_<sup>_L_</sup> =1<sup>;LLM</sup><sup>_S_) .</sup> 11: **return** ( _s{_ 1: _T}_ , _k_ +1, _m_ , _a{_ 1: _T}_ , _k_ +1, _m_ ). 

**Notation.** A _query q_ is a question to be answered. A _reasoning trace s{_ 1: _T}_ = ( _s_ 1, . . . , _sT_ ) is a sequence of _T_ intermediate reasoning steps leading to a final answer _a_ . A _demonstration_ is a complete triple ( _q_ , _s{_ 1: _T}_ , _a_ ) used as a prompt exemplar to guide LLM generation via in-context learning. 

**Client-side data.** Each client _i_ holds a private dataset _D_<sup>_i_</sup> = _{_ ( _q_<sup>_i_</sup> _n_<sup>,</sup><sup>_si_</sup> _{_ 1: _T}_ , _n_<sup>,</sup><sup>_ai_</sup> _n_<sup>)</sup><sup>_}_</sup> _n_<sup>_N_</sup> =1<sup>of</sup><sup>_N_</sup> demonstrations, representing the client’s domain-specific reasoning knowledge. These demonstrations are never shared with the server; only the reasoning outputs generated from them are communicated. 

**Server-side data.** The server maintains a query set _Q_ = _{_ ( _qm_ , _s{_ 1: _T}_ , _m_ , _am_ ) _}m_<sup>_M_</sup> =1<sup>of</sup><sup>_M_entries,</sup> representing the questions the server seeks to answer. 

In this setting, the server must coordinate with clients whose data quality and domain coverage vary from query to query. Since client data is private and heterogeneous, clientgenerated reasoning traces for the same query may conflict or contain overconfident errors. This raises several questions: 

- How can the server determine which clients are reliable for a given query without observing their private data? 

- How can the server identify and correct flawed intermediate reasoning steps when clients produce conflicting traces for the same query, rather than simply picking one answer? 

- How can this be achieved efficiently in both computation and communication, without model fine-tuning or parameter exchange? 

In the following sections, we address these challenges and present **FERA** , a training-free framework for uncertainty-aware federated reasoning. 

## **4 Uncertainty-Aware Federated Reasoning** 

We now present FERA. Two observations motivate its design. First, a single round of client responses is often noisy and incomplete, especially under heterogeneous data; iterating over multiple rounds allows both the server’s reasoning and clients’ local contexts to progressively improve. Second, within each round, client reliability varies from query to query, and the server has no direct way to judge which responses to trust. FERA combines an iterative server–client co-refinement protocol (Section 4.1) with uncertainty-guided reasoning correction (Section 4.2) to address both challenges jointly. 

4 

### **4.1 Iterative Server–Client Co-Refinement** 

FERA operates over _K_ communication rounds (Algorithm 2). Each round consists of three steps. First, clients enrich their private datasets using server-distributed context as demonstrations ( _local refinement_ ). Second, clients generate reasoning–answer pairs for the server’s queries using the enriched datasets, together with uncertainty estimates ( _client labeling_ ). Third, the server synthesizes improved reasoning from client contributions via UASCA and redistributes the updated context for the next round ( _server update_ ). Only reasoning outputs and uncertainty signals are transmitted, keeping communication overhead low. 

**Server Distribution.** At round _k_ , the server distributes the query dataset _Qk_ to all clients. **Local Refinement.** Client _i_ selects a subset of demonstrations _Sk_<sup>_i_</sup> , _Q_<sup>_⊆Qk_from the server-</sup> provided query set and incorporates them into prompts for its local language model LLM<sup>_i_</sup> . Using these demonstrations, the client generates refined reasoning–answer pairs ( _s_<sup>_i_</sup> _{_ 1: _T}_ , _k_ , _n_<sup>,</sup><sup>_ai_</sup> _k_ , _n_<sup>)</sup><sup>_∼_LLM</sup><sup>_i_(</sup><sup>_s{_1:</sup><sup>_T}_,</sup><sup>_a|qi_</sup> _n_<sup>,</sup><sup>_S_</sup> _k_<sup>_i_</sup> , _Q_<sup>),which are appended to the local dataset, yield-</sup> ing the updated dataset _Dk_<sup>_i_=</sup><sup>_Di ∪{_(</sup><sup>_qi_</sup> _n_<sup>,</sup><sup>_si_</sup> _{_ 1: _T}_ , _k_ , _n_<sup>,</sup><sup>_ai_</sup> _k_ , _n_<sup>)</sup><sup>_}_</sup> _n_<sup>_N_</sup> =1<sup>.The demonstration set</sup><sup>_S_</sup> _k_<sup>_i_</sup> , _Q_<sup>is</sup> selected using Maximal Marginal Relevance (MMR) (Carbonell & Goldstein, 1998): 


![](P030_images/P030.pdf-0005-03.png)

### Figure analysis

The figure presents Equation (1), which formalizes demonstration selection during FERA's iterative server–client co-refinement procedure.

Readable transcription:

$$
S^i_{k,Q}=\arg\max_{S\subseteq Q_k}\left[\frac{1}{|S|}\sum_{(q',s'_{1:T},a')\in S} \mathrm{Sim}\left((q^i_n,s^i_{1:T,k-1,n},a^i_{k-1,n}),(q',s'_{1:T},a')\right)-\lambda\cdot \mathrm{Div}(S)\right].
$$

Direct observations:
- The selected set is denoted $S^i_{k,Q}$, indicating a client-specific demonstration subset at round $k$ drawn from the server query set $Q_k$.
- The optimization searches over subsets $S\subseteq Q_k$.
- The first term averages semantic similarity over examples $(q',s'_{1:T},a')\in S$.
- Similarity is computed between a client-side prior reasoning–answer tuple $(q^i_n,s^i_{1:T,k-1,n},a^i_{k-1,n})$ and each candidate tuple from the subset.
- The second term subtracts $\lambda\cdot \mathrm{Div}(S)$, where $\lambda$ controls the strength of this set-level penalty or regularizer.

Interpretation in context:
- This equation supports the paper's description of local refinement: each client selects demonstrations from server-provided queries before prompting its local language model.
- The objective is described as Maximal Marginal Relevance-style selection, intended to balance relevance to the client's current example with diversity or redundancy control among selected demonstrations.
- The selected demonstrations are then incorporated into client prompts, enabling refined reasoning–answer generation while keeping raw client data local.
- The equation is part of the mechanism by which FERA progressively improves reasoning traces across communication rounds.


where _Sim_ ( _·_ , _·_ ) measures semantic similarity between examples, _λ >_ 0 is the regularization parameter, and _Div_ ( _S_ ) is a diversity measure of set _S_ . 

**Client Labeling.** Using the refined dataset _Dk_<sup>_i_, client</sup><sup>_i_generates predictions</sup><sup>_{ai_</sup> _k_ +1, _m_<sup>_}_</sup> _m_<sup>_M_</sup> =1 for the server queries _{qm}m_<sup>_M_</sup> =1<sup>.For each query</sup><sup>_qm_, the client constructs a demonstration</sup> set _Sk_<sup>_i_</sup> , _D_<sup>_⊆D_</sup> _k_<sup>_i_andpromptsitslocalmodeltoproduceanupdatedreasoning–answer</sup> pair ( _s_<sup>_i_</sup> _{_ 1: _T}_ , _k_ +1, _m_<sup>,</sup><sup>_ai_</sup> _k_ +1, _m_<sup>)</sup><sup>_∼_LLM</sup><sup>_i_(</sup><sup>_s{_1:</sup><sup>_T}_,</sup><sup>_a|qm_,</sup><sup>_S_</sup> _k_<sup>_i_</sup> , _D_<sup>).The demonstration set</sup><sup>_S_</sup> _k_<sup>_i_</sup> , _D_<sup>is again</sup> selected using the MMR strategy to balance relevance to the current query and diversity among examples. Along with each generated response, the client computes an uncertainty score _u_<sup>_i_</sup> _k_ +1, _m_<sup>based on the output logits of LLM</sup><sup>_i_.</sup> **Server Update.** The server collects all client responses and updates _Qk_ +1 via UA-SCA (Section 4.2), then redistributes the refined _Qk_ +1 to clients for the next round. As _Qk_ +1 contains higher-quality reasoning traces than _Qk_ , it provides stronger demonstrations that enable clients to produce more accurate reasoning in round _k_ +1. Meanwhile, each client augments its local dataset _Dk_<sup>_i_with reasoning–answer pairs derived from these refined traces.</sup> This process leads to progressive co-improvement of both server outputs and client-side context across rounds, while all communication remains server-mediated, ensuring that raw client data never leaves the local device. 

**Privacy considerations.** FERA operates under a _data-local_ threat model: raw client data _D_<sup>_i_</sup> never leaves the client, and only reasoning traces generated for server-provided queries are transmitted. This is weaker than formal differential privacy but consistent with practical federated deployments where the primary concern is preventing raw data centralization. We acknowledge that reasoning traces may indirectly leak information about client data; an empirical leakage audit (Appendix H) using NER-based detection shows that only 0.043% of transmitted responses contain identifiers not already present in the server query, indicating minimal unintended leakage in practice. 

### **4.2 Uncertainty-Aware Self-Critique Aggregation** 

Within each round, the server receives multiple reasoning traces for the same query, often with conflicting intermediate steps and final answers. The core challenge is that, without access to client data distributions, the server cannot determine which client is most trustworthy for the query at hand. Existing approaches are insufficient. Uniform aggregation (Chen et al., 2025) ignores query-dependent reliability. Iterative mutual alignment (Du et al., 2023) may converge to a shared yet biased reasoning path because it lacks a mechanism for identifying trustworthy clients on a per-query basis. Uncertainty-weighted voting (Agrawal 

5 

et al., 2025) uses confidence signals, but only at the answer level, and thus cannot correct flawed intermediate reasoning when a client is confidently wrong under domain mismatch. To address these limitations, we propose Uncertainty-Aware Self-Critique Aggregation (UASCA), which combines query-dependent uncertainty weighting with structured self-critique and cross-client verification. Instead of merely selecting or discarding entire responses, UA-SCA revises weakly justified but informative reasoning traces at the step level. The full three-stage pipeline is described in Algorithm 1. 

**Stage 1: Per-query uncertainty estimation.** Since the server cannot observe client data, each client self-reports an uncertainty score derived from output logits. Specifically, for a generated token at position _t_ , the entropy is _Ht_ = _−_ ∑<sup>_V_</sup> _i_ =1<sup>_pt_,</sup><sup>_i_log(</sup><sup>_pt_,</sup><sup>_i_+</sup><sup>_ε_),where</sup><sup>_pt_,</sup><sup>_i_</sup> is the softmax probability of token _i_ , _V_ is the vocabulary size, and _ε_ is a small constant for numerical stability (Duan et al., 2023; Farquhar et al., 2024; Zhang et al., 2025). The uncertainty of a reasoning sequence is the average entropy over all _T_ generated tokens: _U_ = _T_<sup><u>1</u>∑</sup> _t_<sup>_T_</sup> =1<sup>_Ht_.This measure is training-free and calibration-free, making it well suited to</sup> the federated setting where clients deploy their own local models with accessible output logits. When output logits are not accessible, alternative uncertainty estimation methods such as verbalized confidence or sampling-based consistency can be used as replacements. A detailed discussion of design considerations for the uncertainty measure, including comparison with alternative methods, is provided in Appendix G. The server converts 

uncertainty scores into query-dependent weights: _w_<sup>_i_</sup> _k_ +1, _m_<sup>=</sup> exp( _−u_<sup>_i_</sup> _<u>k</u>_ <u>+1,</u> _<u>m</u>_<sup>/</sup><sup>_τ_)</sup> _τ >_ 0, ∑<sup>_L_</sup> _j_ =1<sup>exp(</sup><sup>_−u_</sup> _k_<sup>_j_</sup> +1, _m_<sup>/</sup><sup>_τ_),</sup> 

where _u_<sup>_i_</sup> is the uncertainty score of client _i_ and _L_ is the number of clients. The softmax in Eq. (4.2) normalizes across clients for each query, so absolute uncertainty scales need not be comparable across different model families; only the relative ordering within a query matters. We empirically verify this under model-capacity heterogeneity (Qwen3-4B/1.7B/0.6B) in Appendix F.2, where FERA maintains stable performance despite substantial differences in raw entropy scales. 

**Stage 2: Structured self-critique.** Uncertainty weighting helps identify _which_ clients are more trustworthy for a given query, but it cannot determine _what_ is wrong in their reasoning. Under domain mismatch, a client may still produce an incorrect answer with high confidence, as the model is confidently relying on incorrect domain knowledge. Therefore, beyond trust weighting, the server must also diagnose and revise flawed reasoning content at the step level. To enable this, UA-SCA first partitions client submissions into groups _G_ = _{Gr}_ according to exact matches of the final answer _a_<sup>_i_</sup> _k_ , _m_<sup>(e.g.,theselected</sup> option in multiple-choice tasks or the numerical result in math tasks), where each group _Gr_ = _{i | a_<sup>_i_</sup> _k_ , _m_<sup>=</sup><sup>_r}_containsallclientssupportingcandidateanswer</sup><sup>_r_.Foreachgroup,</sup> UA-SCA constructs a representative summary of its reasoning traces, capturing the dominant reasoning pattern behind that answer. Each client’s trace is then compared against summaries from _other_ groups and revised through structured self-critique when its intermediate steps conflict with explanations that are more coherent or better supported. In this way, UA-SCA targets unsupported assumptions and weak reasoning steps directly, allowing confident but poorly justified traces to be corrected using evidence from other clients rather than simply discarded. Although self-critique and cross-agent verification have been studied in centralized settings (Yuan & Xie, 2025; Xu et al., 2025; Li et al., 2025; Du et al., 2023), these methods typically assume full access to all reasoning traces and treat all agents as equally reliable. By contrast, UA-SCA is designed for the federated setting, where client data remains private and reliability is query-dependent, by coupling uncertainty-guided trust weighting with structured cross-client critique. 

**Stage 3: Synthesis.** Finally, the Aggregate function (Algorithm 1, line 9) instructs the server-side LLM to synthesize the revised traces into a single coherent reasoning path and final answer. The server LLM receives all revised client traces annotated with their uncertainty-derived weights _{wi}_ and produces a unified output: � _i_ ( _s{_ 1: _T}_ , _k_ +1, _m_ , _ak_ +1, _m_ ) = Aggregate� _{_ ( _s{_ 1: _T}_ , _k_ , _m_<sup>, �</sup><sup>_ai_</sup> _k_ , _m_<sup>,</sup><sup>_wi_)</sup><sup>_}_</sup> _i_<sup>_L_</sup> =1�. The server LLM preferentially follows higher-weighted (lower-uncertainty) clients while incorporating complementary information from others. Unlike traditional federated learning, which averages numerical 

6 


![](P030_images/P030.pdf-0007-00.png)


Figure 2: Performance comparison of FERA and its variants against baseline methods on the MMLUPRO benchmark under varying levels of client-level data heterogeneity ( _α ∈{_ 1.0, 10, 100 _}_ ). 


![](P030_images/P030.pdf-0007-02.png)



![](P030_images/P030.pdf-0007-03.png)


Figure 4: Performance of FERA under different aggregation strategies across different benchmarks. 

Figure 3: Performance comparison of FERA and its variants against other baselines across two benchmarks: AQUA-RAT and GSM8K. 

parameters, this aggregation is a _language-level synthesis_ operation performed entirely by the server LLM. Importantly, the server LLM acts as a synthesis tool whose role is to integrate client contributions rather than to reason independently; the objective is not to preserve a verbatim record of individual client reasoning traces, but to improve server-side prediction quality by synthesizing diverse and potentially conflicting reasoning signals into a more coherent and broadly supported rationale. An illustrative example of the full UA-SCA procedure is provided in Appendix B.2.1. 

**Robustness.** UA-SCA is robust to unreliable and low-quality clients by design: uncertainty weighting down-weights noisy contributions (formally justified by Theorem 4.1), while structured self-critique detects and revises flawed reasoning independently of the reported confidence. This provides defense against non-strategic noise (e.g., domain mismatch, incomplete data); robustness to strategic adversaries that deliberately manipulate uncertainty scores would require additional adversarial mechanisms and is left as future work. 

### **4.3 Theoretical Analysis** 

The notation used below is defined in Section 3. While the iterative protocol and uncertainty weighting in FERA are motivated by practical considerations, it is natural to ask whether they admit formal justification. To address this question, we analyze Algorithm 2 under a simplified setting that captures the core aggregation dynamics. Specifically, we consider a setting where the LLM predicts only the final answer, without intermediate reasoning steps, for linear regression tasks with _q ∈_ **R**<sup>_d_</sup> and _a ∈_ **R** . Following Zhang et al. (2023a), each client’s LLM is modeled as a single-layer linear self-attention (LSA) model (see Appendix C for details). We assume _qm_ , _q_<sup>_i_</sup> _n_<sup>_∼N_(0, Λ)withΛ</sup><sup>_≻_0,and that client</sup><sup>_i_’s answers satisfy</sup> _a_<sup>_i_</sup> _n_<sup>=(</sup><sup>_qi_</sup> _n_<sup>)</sup><sup>_⊤θ_+</sup><sup>_ϵ_</sup> _n_<sup>_i_,where</sup><sup>_ϵ_</sup> _n_<sup>_i∼N_(0,</sup><sup>_σ_</sup> _i_<sup>2).Theheterogeneousnoisevariances</sup><sup>_σ_</sup> _i_<sup>2capture</sup> variation in client reliability. Under this model, the server aggregates client predictions via weighted averaging: _ak_ +1, _m_ = ∑ _i_<sup>_L_</sup> =1<sup>_wi_</sup> _k_ +1, _m_<sup>_ai_</sup> _k_ +1, _m_<sup>.</sup> 

**Theorem 4.1.** Set the weights _w_<sup>_i_</sup> _k_ , _m_<sup>:=</sup><sup>_wi_</sup> _m_<sup>to be weights independent of the rounds and the</sup> initial answers _a_ 0, _m_ = 0. Then for Algorithm 2, at every round _k ∈_ [ _K_ ], we have: • _ak_ , _m_ = _θk_<sup>_⊤qm_for all</sup><sup>_m ∈_[</sup><sup>_M_].</sup> 

- With probability at least 1 _− δ_ for some _δ ∈_ (0, 1), the difference between _θk_ and _θ_ can be bounded by 


![](P030_images/P030.pdf-0007-12.png)


7 

Theorem 4.1 has two main implications. First, the iterative protocol converges: as _M_ , _N_ increase, the server’s answers approach the ground truth. Second, the error bound depends on ∑ _i_<sup>_L_</sup> =1<sup>_wi_</sup> _m_<sup>_σ_</sup> _i_<sup>, which is minimized when the weights are inversely proportional to</sup><sup>_σ_</sup> _i_<sup>.This</sup> aligns with Eq. (4.2), where clients with higher noise (and thus higher uncertainty) receive lower weights. The theorem therefore provides principled support for the uncertaintyaware weighting design under the simplified model. Although this analysis is derived under a tractable setting, two empirical findings suggest that its predictions extend more broadly. First, the ablation study in Section 5.4 shows that removing uncertainty weighting consistently degrades performance across all benchmarks, consistent with the theorem’s prediction that uniform weights ( _w_<sup>_i_</sup> = 1/ _L_ ) are suboptimal. Second, the demonstrationquantity study in Appendix F.2 shows that increasing _N_ improves accuracy, matching the _O_ (1/ _√N_ ) convergence rate in Eq. (2). 

## **5 Experiment** 

In this section, we first introduce the overall experimental setup. We then present a series of experiments designed to answer specific research questions, with each question and its corresponding results discussed in dedicated subsections. 

- **RQ1.** How do FERA and its variants perform on general and mathematical reasoning benchmarks under heterogeneous client data, including settings where clients have domain-specific expertise, compared with existing baselines? 

- **RQ2.** What is the effect of techniques such as Uncertainty-Aware Aggregation and Iterative Refinement on the performance of FERA? 

- **RQ3.** How do experimental factors such as the aggregation strategy, number of iterative update rounds, choice of backbone language model, specialized-domain settings, demonstration selection strategy, number of clients, presence of low-quality clients, and in-context length affect the performance of FERA? 

### **5.1 Experimental Setup** 

**Benchmarks.** We evaluate on three reasoning benchmarks: **MMLU-Pro** (Wang et al., 2024b) (12K+ college-level questions across 14 topics), **AQUA-RAT** (Ling et al., 2017) (100K+ algebraic word problems), and **GSM8K** (Cobbe et al., 2021) (8.5K grade-school math problems). For MMLU-Pro, we select five questions per category as the server query set and partition the remainder among clients using a Dirichlet distribution (Hsu et al., 2019) with _α ∈{_ 1.0, 10, 100 _}_ to model varying heterogeneity levels. For AQUA-RAT and GSM8K, 70 problems form the server query set, and the rest are uniformly distributed among clients, providing a homogeneous data setting. Details are in Appendix E. 

**Evaluation and Models.** We report accuracy as the primary metric (Team et al., 2023; Touvron et al., 2023) and computation/communication costs (Table 1). Client-side models are Qwen3-4B (Yang et al., 2025) and LLaMA-3.1-8B (Dubey et al., 2024); the server uses GPT-4o-mini for aggregation (Du et al., 2023). 

### **5.2 Baselines** 

**External Baselines.** We evaluate FERA against two categories of baselines: federated learning (FL) methods and parameterfree methods. The FL baselines include **FedAvg** (McMahan et al., 2017; Ye et al., 2024) and **FloRA** (Wang et al., 2024c), while the parameter-free baseline is **LLM-Debate** (Du et al., 2023). In addition, we consider a **Server-only** baseline, where the server LLM is directly applied to the benchmarks without any client collaboration. 


![](P030_images/P030.pdf-0008-11.png)

### Figure analysis

Purpose: The figure compares how accuracy changes as the number of client-server interaction rounds increases for several FERA variants, supporting the paper's discussion of iterative refinement.

Structure and labels:
- Two side-by-side line charts are shown.
- Left panel title: **MMLU-Pro(α = 10)**.
- Right panel title: **AQUA_RAT**.
- Shared x-axis label: **Rounds**, with rounds 1 through 6.
- Y-axis label: **Accuracy**; the left panel spans roughly 0.2 to 0.7, and the right panel spans roughly 0.2 to 0.8.
- Legend series:
  - **FERA**: teal line with circular markers.
  - **FERA-free**: pink/red line with square markers.
  - **FERA-Q**: yellow line with triangle markers.
  - **FERA-GT**: dark dotted horizontal baseline.

Panel-specific observations:

**MMLU-Pro(α = 10)**
- Direct observation: FERA starts below FERA-Q at round 1 but rises sharply by round 2 and remains the top-performing series through round 6.
- Direct observation: FERA-free improves substantially from round 1 to round 2, then stays near a flat plateau below FERA.
- Direct observation: FERA-Q is relatively stable with a mild upward trend through about round 5, remaining below FERA after round 2.
- Direct observation: FERA-GT is a flat dotted baseline around the mid-0.4 accuracy range.
- Interpretation: Iterative refinement appears especially beneficial for FERA on MMLU-Pro, with most of the gain occurring early and smaller gains afterward.

**AQUA_RAT**
- Direct observation: FERA and FERA-free both increase sharply from round 1 to round 2 and then remain high, near the upper portion of the plotted range.
- Direct observation: FERA-free is very close to FERA after round 2 and appears slightly higher at some later rounds, though exact values are not labeled.
- Direct observation: FERA-Q remains much lower than FERA and FERA-free, increasing gradually and peaking around the later rounds before slightly declining.
- Direct observation: FERA-GT is a flat dotted baseline near the low-0.3 accuracy range.
- Interpretation: On AQUA_RAT, the main improvement from interaction rounds occurs by round 2, and methods using full reasoning/contextual refinement substantially outperform FERA-Q and FERA-GT.

Connection to the paper text:
- The surrounding text asks how iterative update rounds affect FERA and reports that iterative refinement improves performance.
- This figure visually supports that claim by showing increasing or stabilized high accuracy as rounds increase, especially for FERA compared with FERA-GT and FERA-Q.
- The figure also relates to the paper's ablations: FERA-free tests a low-resource setting, FERA-Q removes intermediate reasoning, and FERA-GT uses fixed ground-truth demonstrations without iterative updates.


Figure 5: Effect of interaction round count on FERA and FERA-Free in the MMLU-Pro benchmark. 

8 

**FERA Variants.** We introduce variants to isolate different components (details in Appendix D.4): **FERA-GT** uses fixed ground-truth demonstrations without iterative updates (upper bound); **FERA-Q** omits intermediate reasoning steps to isolate their contribution; **FERA-Free** assumes clients have only questions without answers (low-resource setting). 

### **5.3 Evaluation Results** 

The main results (Figures 2–3) use LLaMA3.1-8B as the client model; Qwen3-4B results are in Appendix F.1. FERA consistently outperforms all baselines with substantially lower communication overhead than training-based methods. 

**Impact of Data Heterogeneity.** Figure 2 shows that FERA consistently outperforms all baselines on MMLU-Pro across a wide range of heterogeneity levels. Using Dirichlet splits with _α ∈{_ 1.0, 10, 100 _}_ , we observe that performance improves as _α_ increases, indicating that more homogeneous client distributions lead to more stable demonstration retrieval and fewer conflicting updates. FERA also performs strongly on AQUA-RAT and GSM8K under homogeneous settings (Figure 3). We further evaluate an extreme heterogeneity setting in Appendix F.2. 

**Impact of Iterative Refinement.** Figure 2 shows that FERA consistently improves with more interaction rounds, outperforming both Server-Only and FERA-GT (which uses fixed local context without iterative updates). This highlights the benefit of iterative refinement for integrating distributed knowledge. 

**Impact of Reasoning Process.** FERA-Q performs substantially worse than FERA, especially on mathematically intensive benchmarks such as MMLU-Pro and AQUA-RAT. By restricting the model to final-answer prediction without intermediate reasoning steps, FERA-Q removes the structured problem-solving process needed for multi-step tasks, leading to lower accuracy and reduced interpretability. These results underscore the value of explicit reasoning traces in logic-intensive settings. 

**Impact of Server LLM.** We verify that gains stem from framework design rather than the server model. The Server-Only baseline (same GPT-4o-mini, no clients) and LLM-Debate (same server for summarization) both underperform FERA, and the “UA-SCA without Self-Critique” ablation shows that even reducing the server to simple weighted synthesis still outperforms naive aggregation. 

**Computation and Communication Cost.** Using only forward inference over _K_ =6 rounds, FERA requires 8 _×_ fewer FLOPs than FedAvg and 3 _×_ fewer than FLoRA (Table 1). Although its FLOPs are slightly higher than LLM-Debate due to local refinement, this additional cost yields substantially better accuracy. Communication overhead is also low (Figures 2–3), as 

Table 1: Total computation cost comparison. 

|**Method**|**Rounds**|**FLOPs**|**Training?**|
|---|---|---|---|
|FedAvg|50|7.4_×_10<sup>17</sup>|Yes|
|FLoRA|50|2.5_×_10<sup>17</sup>|Yes|
|LLM-Debate|6|4.1_×_10<sup>16</sup>|No|
|FERA|6|8.9_×_10<sup>16</sup>|No|



FERA transmits only reasoning traces and uncertainty scores, without parameter exchange or additional client revision steps. Detailed cost formulas are provided in Appendix E.3. 

### **5.4 Ablation Studies** 

**Effect of Uncertainty-Aware Aggregation.** We compare three server-side aggregation strategies (Figure 4): (i) UA-SCA; (ii) UA-SCA without Self-Critique; and (iii) UA-SCA without Uncertainty. UA-SCA consistently outperforms both ablations, confirming that uncertainty weighting (identifying _which_ clients to trust) and self-critique (correcting _what_ is wrong in reasoning) provide complementary gains. Even without self-critique, incorporating uncertainty yields clear improvements over naive aggregation, consistent with Theorem 4.1. 

**Effect of Iterative Refinement.** Figure 5 compares FERA, FERA-Free, and FERA-GT across communication rounds. FERA and FERA-Free perform worse than FERA-GT in early rounds, as FERA-GT benefits from fixed, high-quality local exemplars. As rounds progress, the UA-SCA mechanism reduces noise in client updates, leading to consistent gains. This 

9 

confirms that iterative refinement enables FERA to progressively integrate information from heterogeneous clients. 

**Additional ablations on model capacity heterogeneity, uncertainty characteristics, demonstration quality, demonstration selection strategy, specialized domains, demonstration quantity, and the number of clients are reported in Appendix F.2.** 

## **6 Conclusion** 

We presented FERA, a training-free federated reasoning framework for improving LLM reasoning across heterogeneous clients with private data, without centralized training or data exchange. FERA combines iterative server–client co-refinement with UA-SCA, which uses uncertainty-aware weighting and structured cross-client verification to revise flawed reasoning. Theory shows that the iterative process converges and that uncertaintyaware weighting minimizes the error bound, while experiments demonstrate consistent gains over both training-based and training-free baselines on general and mathematical reasoning benchmarks. Important future directions include adversarial robustness and mixed-architecture deployments. 

## **References** 

- Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4 technical report. _arXiv preprint arXiv:2303.08774_ , 2023. 

- Aakriti Agrawal, Rohith Aralikatti, Anirudh Satheesh, Souradip Chakraborty, Amrit Singh Bedi, and Furong Huang. Uncertainty-aware answer selection for improved reasoning in multi-llm systems. In _Findings of the Association for Computational Linguistics: EMNLP 2025_ , pp. 25090–25098, 2025. 

- Stefan Baack, Stella Biderman, Kasia Odrozek, Aviya Skowron, Ayah Bdeir, Jillian Bommarito, Jennifer Ding, Maximilian Gahntz, Paul Keller, Pierre-Carl Langlais, et al. Towards best practices for open datasets for llm training. _arXiv preprint arXiv:2501.08365_ , 2025. 

- Jaime Carbonell and Jade Goldstein. The use of mmr, diversity-based reranking for reordering documents and producing summaries. In _Proceedings of the 21st annual international ACM SIGIR conference on Research and development in information retrieval_ , pp. 335–336, 1998. 

- Tianshi Che, Ji Liu, Yang Zhou, Jiaxiang Ren, Jiwen Zhou, Victor S Sheng, Huaiyu Dai, and Dejing Dou. Federated learning of large language models with parameter-efficient prompt tuning and adaptive optimization. _arXiv preprint arXiv:2310.15080_ , 2023. 

- Minghui Chen, Ruinan Jin, Wenlong Deng, Yuanyuan Chen, Zhi Huang, Han Yu, and Xiaoxiao Li. Can textual gradient work in federated learning? _arXiv preprint arXiv:2502.19980_ , 2025. 

- Fengxiang Cheng, Haoxuan Li, Fenrong Liu, Robert van Rooij, Kun Zhang, and Zhouchen Lin. Empowering llms with logical reasoning: A comprehensive survey. _arXiv preprint arXiv:2502.15652_ , 2025. 

- Zheng Chu, Jingchang Chen, Qianglong Chen, Weijiang Yu, Tao He, Haotian Wang, Weihua Peng, Ming Liu, Bing Qin, and Ting Liu. Navigate through enigmatic labyrinth a survey of chain of thought reasoning: Advances, frontiers and future. _arXiv preprint arXiv:2309.15402_ , 2023. 

- Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, et al. Training verifiers to solve math word problems. _arXiv preprint arXiv:2110.14168_ , 2021. 

10 

- Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. Bert: Pre-training of deep bidirectional transformers for language understanding. In _Proceedings of the 2019 conference of the North American chapter of the association for computational linguistics: human language technologies, volume 1 (long and short papers)_ , pp. 4171–4186, 2019. 

- Chenhe Dong, Yuexiang Xie, Bolin Ding, Ying Shen, and Yaliang Li. Tunable soft prompts are messengers in federated learning. _arXiv preprint arXiv:2311.06805_ , 2023. 

- Yilun Du, Shuang Li, Antonio Torralba, Joshua B Tenenbaum, and Igor Mordatch. Improving factuality and reasoning in language models through multiagent debate. _arXiv preprint arXiv:2305.14325_ , 2023. 

- Jinhao Duan, Hao Cheng, Shiqi Wang, Alex Zavalny, Chenan Wang, Renjing Xu, Bhavya Kailkhura, and Kaidi Xu. Shifting attention to relevance: Towards the predictive uncertainty quantification of free-form large language models. _arXiv preprint arXiv:2307.01379_ , 2023. 

- Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad Al-Dahle, Aiesha Letman, Akhil Mathur, Alan Schelten, Amy Yang, Angela Fan, et al. The llama 3 herd of models. _arXiv e-prints_ , pp. arXiv–2407, 2024. 

- Kennedy Edemacu and Xintao Wu. Privacy preserving prompt engineering: A survey. _ACM Computing Surveys_ , 57(10):1–36, 2025. 

- Tao Fan, Yan Kang, Guoqiang Ma, Weijing Chen, Wenbin Wei, Lixin Fan, and Qiang Yang. Fate-llm: A industrial grade federated learning framework for large language models. _arXiv preprint arXiv:2310.10049_ , 2023. 

- Sebastian Farquhar, Jannik Kossen, Lorenz Kuhn, and Yarin Gal. Detecting hallucinations in large language models using semantic entropy. _Nature_ , 630(8017):625–630, 2024. 

- Shivam Garg, Dimitris Tsipras, Percy S Liang, and Gregory Valiant. What can transformers learn in-context? a case study of simple function classes. _Advances in Neural Information Processing Systems_ , 35:30583–30598, 2022. 

- Tommaso Green, Martin Gubri, Haritz Puerto, Sangdoo Yun, and Seong Joon Oh. Leaky thoughts: Large reasoning models are not private thinkers. _arXiv preprint arXiv:2506.15674_ , 2025. 

- Bairu Hou, Yujian Liu, Kaizhi Qian, Jacob Andreas, Shiyu Chang, and Yang Zhang. Decomposing uncertainty for large language models through input clarification ensembling. _arXiv preprint arXiv:2311.08718_ , 2023. 

- Tzu-Ming Harry Hsu, Hang Qi, and Matthew Brown. Measuring the effects of non-identical data distribution for federated visual classification. _arXiv preprint arXiv:1909.06335_ , 2019. 

- Edward J Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, Weizhu Chen, et al. Lora: Low-rank adaptation of large language models. _ICLR_ , 1(2):3, 2022. 

- Hsiu-Yuan Huang, Zichen Wu, Yutong Yang, Junzhao Zhang, and Yunfang Wu. Unlocking the power of llm uncertainty for active in-context example selection. _arXiv preprint arXiv:2408.09172_ , 2024. 

- Jared Kaplan, Sam McCandlish, Tom Henighan, Tom B Brown, Benjamin Chess, Rewon Child, Scott Gray, Alec Radford, Jeffrey Wu, and Dario Amodei. Scaling laws for neural language models. _arXiv preprint arXiv:2001.08361_ , 2020. 

- Takeshi Kojima, Shixiang Shane Gu, Machel Reid, Yutaka Matsuo, and Yusuke Iwasawa. Large language models are zero-shot reasoners. _Advances in neural information processing systems_ , 35:22199–22213, 2022. 

11 

- Nikolas Koutsoubis, Asim Waqas, Yasin Yilmaz, Ravi P Ramachandran, Matthew B Schabath, and Ghulam Rasool. Privacy-preserving federated learning and uncertainty quantification in medical imaging. _Radiology: Artificial Intelligence_ , pp. e240637, 2025. 

- Weirui Kuang, Bingchen Qian, Zitao Li, Daoyuan Chen, Dawei Gao, Xuchen Pan, Yuexiang Xie, Yaliang Li, Bolin Ding, and Jingren Zhou. Federatedscope-llm: A comprehensive package for fine-tuning large language models in federated learning. In _Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining_ , pp. 5260–5271, 2024. 

- Lorenz Kuhn, Yarin Gal, and Sebastian Farquhar. Semantic uncertainty: Linguistic invariances for uncertainty estimation in natural language generation. _arXiv preprint arXiv:2302.09664_ , 2023. 

- Yansi Li, Jiahao Xu, Tian Liang, Xingyu Chen, Zhiwei He, Qiuzhi Liu, Rui Wang, Zhuosheng Zhang, Zhaopeng Tu, Haitao Mi, et al. Dancing with critiques: Enhancing llm reasoning with stepwise natural language self-critique. _arXiv preprint arXiv:2503.17363_ , 2025. 

- Wang Ling, Dani Yogatama, Chris Dyer, and Phil Blunsom. Program induction by rationale generation: Learning to solve and explain algebraic word problems. _ACL_ , 2017. 

- Aixin Liu, Bei Feng, Bing Xue, Bingxuan Wang, Bochao Wu, Chengda Lu, Chenggang Zhao, Chengqi Deng, Chenyu Zhang, Chong Ruan, et al. Deepseek-v3 technical report. _arXiv preprint arXiv:2412.19437_ , 2024. 

- Han Liu, Ruoyao Wen, Srijith Nair, Jia Liu, Wenjing Lou, Chongjie Zhang, William Yeoh, Yevgeniy Vorobeychik, and Ning Zhang. Ecolora: Communication-efficient federated fine-tuning of large language models. _arXiv preprint arXiv:2506.02001_ , 2025. 

- Xiangyang Liu, Tianqi Pang, and Chenyou Fan. Federated prompting and chain-of-thought reasoning for improving llms answering. In _International Conference on Knowledge Science, Engineering and Management_ , pp. 3–11. Springer, 2023. 

- Xinge Ma, Jiangming Liu, Jin Wang, and Xuejie Zhang. Fedid: Federated interactive distillation for large-scale pretraining language models. In _Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing_ , pp. 8566–8577, 2023. 

- Brendan McMahan, Eider Moore, Daniel Ramage, Seth Hampson, and Blaise Aguera y Arcas. Communication-efficient learning of deep networks from decentralized data. In _Artificial intelligence and statistics_ , pp. 1273–1282. PMLR, 2017. 

- Terufumi Morishita, Gaku Morio, Atsuki Yamaguchi, and Yasuhiro Sogawa. Enhancing reasoning capabilities of llms via principled synthetic logic corpus. _Advances in Neural Information Processing Systems_ , 37:73572–73604, 2024. 

- Zhen Qin, Daoyuan Chen, Bingchen Qian, Bolin Ding, Yaliang Li, and Shuiguang Deng. Federated full-parameter tuning of billion-sized language models with communication cost under 18 kilobytes. _arXiv preprint arXiv:2312.06353_ , 2023. 

- N Reimers. Sentence-bert: Sentence embeddings using siamese bert-networks. _arXiv preprint arXiv:1908.10084_ , 2019. 

- Roman Rischke, L Schneider, K Muller,¨ Wojciech Samek, F Schwendicke, and J Krois. Federated learning in dentistry: chances and challenges. _Journal of dental research_ , 101(11): 1269–1273, 2022. 

- Lorenzo Sani, Alex Iacob, Zeyu Cao, Bill Marino, Yan Gao, Tomas Paulik, Wanru Zhao, William F Shen, Preslav Aleksandrov, Xinchi Qiu, et al. The future of large language model pre-training is federated. _arXiv preprint arXiv:2405.10853_ , 2024. 

Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik Narasimhan, and Shunyu Yao. Reflexion: Language agents with verbal reinforcement learning. _Advances in Neural Information Processing Systems_ , 36:8634–8652, 2023. 

12 

- Parshin Shojaee, Iman Mirzadeh, Keivan Alizadeh, Maxwell Horton, Samy Bengio, and Mehrdad Farajtabar. The illusion of thinking: Understanding the strengths and limitations of reasoning models via the lens of problem complexity. _arXiv preprint arXiv:2506.06941_ , 2025. 

- Yao Shu, Wenyang Hu, See-Kiong Ng, Bryan Kian Hsiang Low, and Fei Richard Yu. Ferret: Federated full-parameter tuning at scale for large language models. _arXiv preprint arXiv:2409.06277_ , 2024. 

- Jiankai Sun, Chuanyang Zheng, Enze Xie, Zhengying Liu, Ruihang Chu, Jianing Qiu, Jiaqi Xu, Mingyu Ding, Hongyang Li, Mengzhe Geng, et al. A survey of reasoning with foundation models. _arXiv preprint arXiv:2312.11562_ , 2023. 

- Gemini Team, Rohan Anil, Sebastian Borgeaud, Jean-Baptiste Alayrac, Jiahui Yu, Radu Soricut, Johan Schalkwyk, Andrew M Dai, Anja Hauth, Katie Millican, et al. Gemini: a family of highly capable multimodal models. _arXiv preprint arXiv:2312.11805_ , 2023. 

- Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, et al. Llama 2: Open foundation and fine-tuned chat models. _arXiv preprint arXiv:2307.09288_ , 2023. 

- Jiaqi Wang, Chenxu Zhao, Lingjuan Lyu, Quanzeng You, Mengdi Huai, and Fenglong Ma. Bridging model heterogeneity in federated learning via uncertainty-based asymmetrical reciprocity learning. _Proceedings of machine learning research_ , 235:52290, 2024a. 

- Lei Wang, Wanyu Xu, Yihuai Lan, Zhiqiang Hu, Yunshi Lan, Roy Ka-Wei Lee, and Ee-Peng Lim. Plan-and-solve prompting: Improving zero-shot chain-of-thought reasoning by large language models. _arXiv preprint arXiv:2305.04091_ , 2023. 

- Ruhan Wang, Zhiyong Wang, Chengkai Huang, Rui Wang, Tong Yu, Lina Yao, John C.S. Lui, and Dongruo Zhou. Federated in-context learning: Iterative refinement for improved answer quality. In _Forty-second International Conference on Machine Learning_ , 2025a. URL https://openreview.net/forum?id=TUk7gCqtmf. 

- Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le, Ed Chi, Sharan Narang, Aakanksha Chowdhery, and Denny Zhou. Self-consistency improves chain of thought reasoning in language models. _arXiv preprint arXiv:2203.11171_ , 2022. 

- Yifei Wang, Yu Sheng, Linjing Li, and Daniel Zeng. Uncertainty unveiled: Can exposure to more in-context examples mitigate uncertainty for large language models? _arXiv preprint arXiv:2505.21003_ , 2025b. 

- Yubo Wang, Xueguang Ma, Ge Zhang, Yuansheng Ni, Abhranil Chandra, Shiguang Guo, Weiming Ren, Aaran Arulraj, Xuan He, Ziyan Jiang, et al. Mmlu-pro: A more robust and challenging multi-task language understanding benchmark. In _The Thirty-eight Conference on Neural Information Processing Systems Datasets and Benchmarks Track_ , 2024b. 

- Ziyao Wang, Zheyu Shen, Yexiao He, Guoheng Sun, Hongyi Wang, Lingjuan Lyu, and Ang Li. Flora: Federated fine-tuning large language models with heterogeneous low-rank adaptations. _Advances in Neural Information Processing Systems_ , 37:22513–22533, 2024c. 

- Ziyao Wang, Bowei Tian, Yexiao He, Zheyu Shen, Luyang Liu, and Ang Li. One communication round is all it needs for federated fine-tuning foundation models. _arXiv preprint arXiv:2412.04650_ , 2024d. 

- Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou, et al. Chain-of-thought prompting elicits reasoning in large language models. _Advances in neural information processing systems_ , 35:24824–24837, 2022. 

- Shuyue Wei, Yongxin Tong, Zimu Zhou, Yi Xu, Jingkai Gao, Tongyu Wei, Tianran He, and Weifeng Lv. Federated reasoning llms: a survey. _Frontiers of Computer Science_ , 19(12): 1912613, 2025. 

13 

Feijie Wu, Zitao Li, Yaliang Li, Bolin Ding, and Jing Gao. Fedbiot: Llm local fine-tuning in federated learning without full model. In _Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining_ , pp. 3345–3355, 2024a. 

- Feijie Wu, Xiaoze Liu, Haoyu Wang, Xingchen Wang, Lu Su, and Jing Gao. Towards federated rlhf with aggregated client preference for llms. _arXiv preprint arXiv:2407.03038_ , 2024b. 

- Panlong Wu, Kangshuo Li, Junbao Nan, and Fangxin Wang. Federated in-context llm agent learning. _arXiv preprint arXiv:2412.08054_ , 2024c. 

- Jiaqi Xu, Cuiling Lan, Xuejin Chen, and Yan Lu. Stepwise think-critique: A unified framework for robust and interpretable llm reasoning. _arXiv preprint arXiv:2512.15662_ , 2025. 

- Na Yan, Yang Su, Yansha Deng, and Robert Schober. Federated fine-tuning of llms: Framework comparison and research directions. _arXiv preprint arXiv:2501.04436_ , 2025. 

- An Yang, Anfeng Li, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chang Gao, Chengen Huang, Chenxu Lv, et al. Qwen3 technical report. _arXiv preprint arXiv:2505.09388_ , 2025. 

- Yuchen Yang, Houqiang Li, Yanfeng Wang, and Yu Wang. Improving the reliability of large language models by leveraging uncertainty-aware in-context learning. _arXiv preprint arXiv:2310.04782_ , 2023. 

- Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Tom Griffiths, Yuan Cao, and Karthik Narasimhan. Tree of thoughts: Deliberate problem solving with large language models. _Advances in neural information processing systems_ , 36:11809–11822, 2023a. 

- Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, and Yuan Cao. React: Synergizing reasoning and acting in language models. In _International Conference on Learning Representations (ICLR)_ , 2023b. 

- Rui Ye, Wenhao Wang, Jingyi Chai, Dihan Li, Zexi Li, Yinda Xu, Yaxin Du, Yanfeng Wang, and Siheng Chen. Openfedllm: Training large language models on decentralized private data via federated learning. In _Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining_ , pp. 6137–6147, 2024. 

- Ori Yoran, Tomer Wolfson, Ben Bogin, Uri Katz, Daniel Deutch, and Jonathan Berant. Answering questions by meta-reasoning over multiple chains of thought. _arXiv preprint arXiv:2304.13007_ , 2023. 

- Yurun Yuan and Tengyang Xie. Reinforce llm reasoning through multi-agent reflection. _arXiv preprint arXiv:2506.08379_ , 2025. 

- Jianyi Zhang, Saeed Vahidian, Martin Kuo, Chunyuan Li, Ruiyi Zhang, Tong Yu, Guoyin Wang, and Yiran Chen. Towards building the federatedgpt: Federated instruction tuning. In _ICASSP 2024-2024 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)_ , pp. 6915–6919. IEEE, 2024a. 

- Ruiqi Zhang, Spencer Frei, and Peter L Bartlett. Trained transformers learn linear models in-context. _arXiv preprint arXiv:2306.09927_ , 2023a. 

- Tianyi Zhang, Yu Cao, and Dianbo Liu. Uncertainty-based extensible codebook for discrete federated learning in heterogeneous data silos. _arXiv preprint arXiv:2402.18888_ , 2024b. 

- Tunyu Zhang, Haizhou Shi, Yibin Wang, Hengyi Wang, Xiaoxiao He, Zhuowei Li, Haoxian Chen, Ligong Han, Kai Xu, Huan Zhang, et al. Token-level uncertainty estimation for large language model reasoning. _arXiv preprint arXiv:2505.11737_ , 2025. 

- Yanci Zhang and Han Yu. Uncertainty-aware explainable federated learning. _arXiv preprint arXiv:2503.05194_ , 2025. 

14 

Yifan Zhang, Jingqin Yang, Yang Yuan, and Andrew Chi-Chih Yao. Cumulative reasoning with large language models. _arXiv preprint arXiv:2308.04371_ , 2023b. 

- Denny Zhou, Nathanael Scharli,¨ Le Hou, Jason Wei, Nathan Scales, Xuezhi Wang, Dale Schuurmans, Claire Cui, Olivier Bousquet, Quoc Le, et al. Least-to-most prompting enables complex reasoning in large language models. _arXiv preprint arXiv:2205.10625_ , 2022. 

15 

## **Table of Contents for Appendix** 

|**A Additional Related Work** . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .17|
|---|
|**B Algorithm Details** . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 18|
|B.1 Detailed FERA Workfow . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .18|
|B.2 Uncertainty-Aware Aggregation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .19|
|**C Proof in Section 4** . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .21|
|C.1 Preliminaries for the Theoretical Analysis . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .21|
|C.2 Proof of Theorem 4.1 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .23|
|**D Prompt** . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .26|
|D.1 Server Query Dataset Initialize . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .26|
|D.2 Client Response Generation for Server Queries . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .27|
|D.3 Uncertainty-Aware Aggregation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .28|
|**E Experiment Setup** . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .32|
|E.1 FERA Variants . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .31|
|E.2 Construction of Client Datasets . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .32|
|E.3 Implementation Details . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .33|
|E.4 Communication and Computational Cost . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .33|
|E.5 Demonstration Selection . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .34|
|E.6 Uncertainty Calculation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .35|
|**F Supplementary Experiments** . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .35|
|F.1 Main Results Using Qwen3-4B . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .35|
|F.2 Additional Ablation Study . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .35|
|**G Design Considerations for the Uncertainty Measure** . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .38|
|**H Privacy Analysis** . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .39|
|**I Case Study** . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .40|



16 

**LLM Usage Disclosure.** AI-Generated Visualizations. The framework illustration in Figure 1 and several associated icons were generated or refined using LLM-assisted image generation tools (ChatGPT) for illustrative purposes only. These visual elements are used solely for presentation and do not influence the methodology, experiments, or conclusions of the paper. 

## **A Additional Related Work** 

**Federated Learning in LLM.** The growing scale of LLMs raises concerns around computational demands and data privacy (Sani et al., 2024). FL offers a solution by enabling collaborative model adaptation across decentralized data sources without sharing raw data. Several works explore FL for LLM fine-tuning and instruction tuning. Fan et al. (2023) apply FL to standard generation tasks, while Wu et al. (2024a) introduce a privacy-preserving framework designed for secure, decentralized adaptation. Kuang et al. (2024) focus on instruction tuning across heterogeneous clients to improve generalization. Beyond fine-tuning, prompting-based strategies such as Fed-SP-SC and Fed-DP-CoT (Liu et al., 2023) have shown that reasoning capabilities can be improved via federated aggregation of chain-of-thought responses, leveraging self-consistency and diversity without model updates. Collectively, these efforts underscore FL’s growing role in enabling scalable, privacy-conscious LLM development. 

**Reasoning Large Language Models.** Large language models have demonstrated remarkable capabilities in complex reasoning tasks through various prompting and inference strategies. Chain-of-thought (CoT) prompting revealed that LLMs possess a latent capacity for multi-step reasoning, leading to substantial improvements in arithmetic and commonsense tasks (Yoran et al., 2023; Yao et al., 2023a; Chu et al., 2023). Follow-up studies extended this idea in several ways. Zero-shot CoT requires only the addition of “Let us think step by step” yet recovers much of the original benefit (Wei et al., 2022). Self-consistency generates multiple reasoning paths and selects the most frequent answer among them (Wang et al., 2022). Least-to-most prompting decomposes difficult problems into a sequence of simpler subquestions that are solved in order (Zhou et al., 2022). ReAct interleaves internal thoughts with environment actions, thereby combining reasoning and tool use (Yao et al., 2023b). More recently, Shinn et al. (2023) enable models to iteratively critique and refine their own outputs, further enhancing reliability and accuracy. 

**Federated Reasoning for Large Language Models.** Federated reasoning with large language models (LLMs) has been explored through training-driven approaches that update parameters in distributed settings. Full-parameter methods such as FedKSeed reduce bandwidth by transmitting random seeds and scalar gradients rather than full model weights (Qin et al., 2023). Parameter-efficient methods include FLoRA, which aggregates heterogeneous low-rank adapters (Wang et al., 2024c), FedSP, which exchanges lightweight soft prompts while preserving server-side privacy (Dong et al., 2023), and FedBiOT, which splits models into emulator–adapter pairs optimized via bi-level frameworks (Wu et al., 2024a). Task-specific frameworks have also been developed, including FedIT for instruction tuning (Zhang et al., 2024a), FedID for interactive distillation (Ma et al., 2023), and federated reinforcement learning from human feedback using lightweight preference selector aggregation. These advances show that federated training can preserve privacy and communication efficiency while remaining competitive with centralized training (Wei et al., 2025; Wu et al., 2024b). 

**Training-free Approaches for LLM Reasoning.** Training-free approaches aim to enhance reasoning without parameter updates. Liu et al. (2023) leverage synonymous user questions with self-consistency voting and chain-of-thought prompting, though performance depends heavily on data homogeneity and retrieval quality. Chen et al. (2025) aggregate textual feedback into shared prompts using a density-based method, but struggle with misaligned prompts under heterogeneous data. Other in-context learning approaches (Wang et al., 2025a; Wu et al., 2024c) remain limited to simple QA and tool-use tasks, while debate-style frameworks (Du et al., 2023) risk privacy leakage through direct client communication and 

17 

underutilize local datasets. Together, these lines of work highlight a trade-off: trainingdriven methods achieve stronger performance at higher communication and optimization costs, whereas training-free methods are lightweight but less robust under heterogeneous data and complex reasoning, motivating the development of new frameworks such as FERA. 

**Uncertainty used in Federated Learning.** Recent work has addressed key challenges in FL through uncertainty-based approaches. To handle data heterogeneity, Koutsoubis et al. (2025) survey privacy-preserving methods that integrate uncertainty quantification in federated medical imaging, demonstrating how uncertainty metrics guide robust aggregation under non-IID conditions. Addressing the complementary challenge of model transparency, Zhang & Yu (2025) propose UncertainXFL, which incorporates uncertainty-aware explanations directly into the aggregation process to enhance interpretability. Model heterogeneity presents another significant challenge that has been tackled through uncertainty-guided knowledge transfer mechanisms. Wang et al. (2024a) develop FedType, which leverages proxy models with uncertainty-based distillation to bridge architectural differences, while Zhang et al. (2024b) introduce UEFL, a dynamic approach that adapts discrete codebooks based on uncertainty measures to accommodate diverse data distributions across silos. 

**Uncertainty used in Large Language Models.** LLMs have focused on both quantifying and leveraging uncertainty for enhanced reliability. Hou et al. (2023) pioneer the decomposition of aleatoric and epistemic uncertainty through ensemble methods over clarified input variants, achieving interpretable uncertainty estimates without requiring architectural modifications. This decomposition framework provides a foundation for more nuanced uncertainty-aware decision-making in downstream tasks. Building on this quantification approach, Huang et al. (2024) demonstrate that output inconsistencies under label injection scenarios effectively capture intrinsic model uncertainty—a finding that directly enables active learning strategies for optimal in-context example selection. Further investigating uncertainty dynamics, Wang et al. (2025b) reveal that increased exposure to in-context examples systematically reduces predictive uncertainty, with particularly pronounced effects on epistemic uncertainty. This reduction mechanism explains the observed improvements in both model confidence and accuracy as context size increases. Integrating these theoretical insights into practice, Yang et al. (2023) operationalize an uncertainty-aware framework that empowers models with adaptive behavior: either self-correcting predictions when uncertainty is manageable or abstaining entirely when uncertainty exceeds predefined reliability thresholds. 

## **B Algorithm Details** 

### **B.1 Detailed FERA Workflow** 

FERA follows a round-based federated reasoning workflow in which a central server iteratively refines its reasoning outputs through collaboration with multiple clients holding heterogeneous and private data. In each round, the server distributes its current query set to all clients, and each client uses local demonstrations to generate updated reasoning–answer pairs together with uncertainty estimates, without sharing raw data or model parameters. These client responses are then returned to the server and aggregated using an uncertaintyaware scheme to update the server’s reasoning results for the next round. Through this iterative process, FERA improves global reasoning quality by leveraging client-side knowledge and uncertainty signals, while remaining training-free, communication-efficient, and privacy-preserving. The overall workflow is summarized in Algorithm 2. 

18 

**Algorithm 2** Uncertainty-Aware Federated Reasoning 

**Require:** _L_ clients, each with local dataset _D_<sup>_i_</sup> = _{_ ( _q_<sup>_i_</sup> _n_<sup>,</sup><sup>_si_</sup> _{_ 1: _T}_ , _n_<sup>,</sup><sup>_ai_</sup> _n_<sup>)</sup><sup>_}_</sup> _n_<sup>_N_</sup> =1<sup>andlocalmodel</sup> LLM<sup>_i_</sup> . Server holds initial query set _{qm}m_<sup>_M_</sup> =1<sup>.</sup> 1: Initialize server query set _Q_ 1 = _{_ ( _qm_ , _s{_ 1: _T}_ ,1, _m_ , _a_ 1, _m_ ) _}m_<sup>_M_</sup> =1<sup>.</sup> 

- 2: **for** each round _k_ = 1, . . . , _K_ **do** 3: _Step 1:_ Server distributes _Qk_ to all clients. 4: **for** each client _i_ = 1, . . . , _L_ **do** 

- 5: _Step 2:_ Refine local reasoning–answer pairs using demonstrations from _Qk_ . Form the enhanced dataset: 

_Dk_<sup>_i←Di ∪{_(</sup><sup>_qi_</sup> _n_<sup>,</sup><sup>_s′_</sup> _{_<sup>_i_</sup> 1: _T}_ , _k_ , _n_<sup>,</sup><sup>_a_</sup> _k_<sup>_′i_</sup> , _n_<sup>)</sup><sup>_}_</sup> _n_<sup>_N_</sup> =1<sup>.</sup> 

- 6: _Step 3:_ Predict reasoning–answer pairs for server queries using demonstrations from _D_<sup>_i_Compute uncertainty scores from the predictive distribution of LLM</sup><sup>_i_, and</sup> _k_<sup>.</sup> 

- return to the server: 


![](P030_images/P030.pdf-0019-06.png)


- 7: **end for** 

- 8: _Step 4:_ The server aggregates client responses using an uncertainty-aware scheme; see Section 4.2 for aggregation procedures under different algorithmic settings. **Update** 

_Qk_ +1 = _{_ ( _qm_ , _s{_ 1: _T}_ , _k_ +1, _m_ , _ak_ +1, _m_ ) _}m_<sup>_M_</sup> =1<sup>.</sup> 

9: **end for Ensure:** Final predictions _{_ ( _qm_ , _s{_ 1: _T}_ , _K_ +1, _m_ , _aK_ +1, _m_ ) _}m_<sup>_M_</sup> =1<sup>.</sup> 

_Remark_ B.1 _._ FERA does not inherently require strict synchronous participation. In asynchronous settings, Algorithm 2 can be adapted by modifying line 8 to aggregate responses only from the subset of clients whose updates arrive within the current round. While a fully asynchronous variant would require a redesigned aggregation rule that jointly accounts for both uncertainty and update staleness, such an extension is orthogonal to the main focus of this work. Our goal is to introduce a training-free federated reasoning framework that leverages client-side data characteristics to guide server decision making. 

### **B.2 Uncertainty-Aware Aggregation** 

### **_B.2.1 Uncertainty-Aware Weighted Aggregation (UA-WA)_** 


![](P030_images/P030.pdf-0019-14.png)


Figure 6: Illustration of UA-WA. For a given query, multiple clients generate candidate answers with associated uncertainty estimates. The server assigns higher weights to client responses with lower uncertainty and aggregates them accordingly, reducing the influence of unreliable or domain-mismatched predictions. 

19 

We first introduce the uncertainty-aware aggregation idea in a simplified setup where the reasoning steps _s_<sup>_i_</sup> _{_ 1: _T}_ , _k_ , _m_<sup>are omitted and the task involves only questions</sup><sup>_q_and answers</sup> _a_ . At round _k_ , each of the _L_ clients uploads a predicted answer _a_<sup>_i_</sup> _k_ +1, _m_<sup>togetherwithan</sup> associated uncertainty score _u_<sup>_i_</sup> _k_ +1, _m_<sup>_≥_0 for query</sup><sup>_qm_.The server then calculates a weight for</sup> each client prediction using a temperature-scaled softmax over the negative uncertainties, so that predictions with lower uncertainty receive greater weight: 


![](P030_images/P030.pdf-0020-01.png)

### Figure analysis

The figure presents Equation (3), the weighting rule used in the Uncertainty-Aware Weighted Aggregation (UA-WA) method.

Readable equation:

\[
w^{i}_{k+1,m} = \frac{\exp\left(-u^{i}_{k+1,m}/\tau\right)}{\sum_{j=1}^{L} \exp\left(-u^{j}_{k+1,m}/\tau\right)}, \quad \tau > 0.
\]

Direct observations:
- The left-hand side, \(w^{i}_{k+1,m}\), denotes the aggregation weight assigned to client \(i\) for query/example \(m\) at round \(k+1\).
- The numerator is an exponential transformation of the negative uncertainty \(u^{i}_{k+1,m}\), scaled by temperature \(\tau\).
- The denominator sums the same transformed uncertainty scores over all \(L\) clients, indexed by \(j\), so the weights are normalized across clients.
- The condition \(\tau > 0\) is explicitly stated.
- The equation is numbered as Equation (3).

Interpretation:
- Lower uncertainty values produce larger \(\exp(-u/\tau)\) terms, giving more weight to more confident client predictions.
- Higher uncertainty values are downweighted during server aggregation.
- The temperature \(\tau\) controls how sharply weights concentrate on low-uncertainty clients: smaller values would make the weighting more selective, while larger values would make weights more uniform.

Connection to the surrounding text:
- This equation formalizes the UA-WA mechanism described around Figure 6, where multiple clients return candidate answers and associated uncertainty scores.
- The surrounding text explains that the server uses these weights to compute an aggregated score for each candidate answer and then selects the answer with the highest weighted support.
- The equation provides the mathematical basis for reducing the influence of unreliable or domain-mismatched predictions in the proposed federated reasoning framework.


where _τ_ is the temperature parameter. For each candidate answer _a ∈A_ , the aggregated score is defined as _Sk_ +1, _m_ ( _a_ ) = ∑ _i_<sup>_L_</sup> =1<sup>_wi_</sup> _k_ +1, _m_<sup>_·_</sup><sup>**1**</sup><sup>_{ai_</sup> _k_ +1, _m_<sup>=</sup><sup>_a}_,andthefinalpredictionis</sup> selected as _ak_ +1, _m_ = arg max _a∈A Sk_ +1, _m_ ( _a_ ). The updated query–answer set is then _Qk_ +1 = _{_ ( _qm_ , _ak_ +1, _m_ ) _}m_<sup>_M_</sup> =1<sup>.Figure6illustratestheUA-WAprocess,whereclientpredictionsare</sup> weighted by their estimated uncertainty before aggregation. 

_Remark_ B.2 _._ The vanilla aggregation scheme is recovered as a special case of Eq. (3.3) by setting _w_<sup>_i_</sup> _k_ +1, _m_<sup>= 1 for all</sup><sup>_i_, which reduces the procedure to simple majority voting.The</sup> uncertainty-aware variant generalizes this by weighting each client’s answer according to its estimated uncertainty. This is particularly useful when an infrequent answer is nonetheless produced with consistently low uncertainty. In such cases, Eq. (3.3) naturally upweights reliable yet rare signals while downweighting responses with high uncertainty. This highlights the role of uncertainty as an effective calibration mechanism within the aggregation process. 

### **Illustrative Example of UA-SCA** 

### **Server query:** _“Is tomato a fruit or a vegetable?”_ 

**Client submissions** (each client holds data from a different domain): 

_•_ **Client 1** (botany data, _u_ =0.08): “In botany, a tomato develops from the flower ovary and contains seeds.” _→_ Fruit. 

_•_ **Client 2** (culinary data, _u_ =0.82): “Tomatoes are commonly used in salads, sauces, and savory dishes rather than desserts.” _→_ Vegetable. 

_•_ **Client 3** (restaurant data, _u_ =0.88): “Tomatoes are categorized with vegetables on most restaurant menus and grocery labels.” _→_ Vegetable. 

Without uncertainty, majority voting would select Vegetable (2 vs 1), which is contextually common but scientifically incorrect. 

**Step 1 – Grouping.** Responses are partitioned by final answer: Group A (Fruit): Client 1; Group B (Vegetable): Clients 2, 3. 

**Step 2 – Summarize.** Group A: “Botanically, tomatoes develop from flowers and contain seeds, which classifies them as fruits.” Group B: “Tomatoes are widely treated as vegetables in cooking and food organization.” 

**Step 3 – SelfCritique.** Each client’s trace is evaluated against the opposing group’s summary and revised if contradicted: 

_•_ **Client 1** : Group B discusses culinary usage, which does not contradict the botanical definition. _No revision._ Revised trace: “In botany, a tomato develops from the flower ovary and contains seeds.” _→_ Fruit. 

_•_ **Client 2** : Group A provides a biological definition that conflicts with Client 2’s assumption that culinary usage determines category. _Partially revised._ Revised trace: “Tomatoes are commonly treated as vegetables in cooking, although botanically they are fruits.” _→_ Fruit. 

_•_ **Client 3** : Group A’s evidence prompts reconsideration; grocery labeling reflects usage rather than scientific classification. _Revised._ Revised trace: “Tomatoes are often grouped with vegetables in restaurants and stores, but botanically they are fruits.” _→_ Fruit. 

20 

After self-critique, all three clients answer Fruit. However, this alone does not guarantee the correct outcome in general; the uncertainty weights provide a further safeguard. 

**Step 4 – Aggregate.** The server LLM receives the three revised traces with uncertainty weights _w_ 1=0.56, _w_ 2=0.24, _w_ 3=0.20 (Eq. 4.2; Client 1’s low uncertainty yields the highest weight). It synthesizes a single reasoning chain: “Although tomatoes are commonly treated as vegetables in culinary settings, botanically they develop from flowers and contain seeds, which classifies them as fruits.” **Output:** Fruit. 

### **_B.2.2 Uncertainty-Aware Self-Critique Aggregation (UA-SCA)_** 

UA-SCA addresses disagreement among heterogeneous client reasoning paths by performing aggregation directly in the space of multi-step reasoning. For a given query, each client generates a reasoning trace and final answer together with an uncertainty score derived from its token-level predictive distribution, which reflects query-dependent reliability. UA-SCA first groups client responses by their final answers and summarizes the dominant reasoning pattern within each group using a server-side LLM. Each client’s reasoning–answer pair is then refined through self-critique by comparing it against summaries from alternative answer groups, allowing logical inconsistencies to be exposed and complementary intermediate steps to be incorporated. Finally, the revised reasoning paths are aggregated using uncertainty-aware weights that downweight unreliable or domain-mismatched predictions while amplifying confident and well-supported ones. By combining structured self-critique with uncertainty-aware weighting, UA-SCA resolves conflicts among heterogeneous reasoning paths without relying on majority agreement, while preserving informative intermediate logic throughout iterative federated reasoning rounds; the complete workflow of UA-SCA is described in Algorithm 1. 

We provide a step-by-step walkthrough below to illustrate how data heterogeneity causes conflicting reasoning, how self-critique partially resolves it, and how uncertainty weighting handles residual disagreements. 

## **C Proof in Section 4** 

### **C.1 Preliminaries for the Theoretical Analysis** 

In this section, we lay out the basic formulation of in-context learning (ICL) for function classes, building on Garg et al. (2022); Zhang et al. (2023a). 

In ICL, the model processes and exploits sequential input called a prompt. A prompt consists of a sequence of input–output pairs ( _x_ 1, _y_ 1, . . . , _xN_ , _yN_ , _x_ query), where each _yi_ corresponds to the evaluation of an unknown target functiontask is to infer useful information from the examples and generate a prediction _h_ at _xi_ . Given such a sequence, the model’s _y_ �( _x_ query) for the query point _x_ query, aiming for _y_ �( _x_ query) _≈ h_ ( _x_ query). 

We now present a formal definition for models that learn from in-context examples, following Zhang et al. (2023a). 

**Definition C.1** ((Definition 3.1 in Zhang et al. (2023a)) Trained on in-context examples) **.** Let _Dx_ be a distribution over an input space _X_ , _H ⊂Y_<sup>_X_</sup> a set of functions _X →Y_ , and _DH_ a distribution over functions in _H_ . Let _ℓ_ : _Y × Y →_ **R** be a loss function. Let _S_ = _∪n∈_ **N** _{_ ( _x_ 1, _y_ 1, . . . , _xn_ , _yn_ ) : _xi ∈X_ , _yi ∈Y}_ be the set of finite-length sequences of ( _x_ , _y_ ) pairs and let 

_F_ Θ = _{ fθ_ : _S × X →Y_ , _θ ∈_ Θ _}_ 

be a class of functions parameterized by _θ_ in some set Θ. For _T >_ 0, we say that a model _f_ : _S × X →Y_ is _trained on in-context examples of functions in H under loss ℓ w.r.t._ ( _DH_ , _Dx_ ) if _f_ = _fθ∗_ where _θ_<sup>_∗_</sup> _∈_ Θ satisfies 


![](P030_images/P030.pdf-0021-13.png)

### Figure analysis

The displayed equation formalizes the training criterion in Definition C.1 for a model trained on in-context examples.

Readable transcription:

\[
\theta^{*} \in \operatorname*{argmin}_{\theta \in \Theta}\; \mathbb{E}_{P=(x_1,h(x_1),\ldots,x_T,h(x_T),x_{\mathrm{query}})}\left[\ell\left(f_{\theta}(P),h(x_{\mathrm{query}})\right)\right].
\]

Direct observations:
- The optimization variable is \(\theta\), constrained to the parameter space \(\Theta\).
- The selected parameter \(\theta^{*}\) belongs to the set of minimizers of an expected loss.
- The expectation is taken over prompts \(P\) consisting of context input-output examples \((x_i,h(x_i))\) for \(i=1,\ldots,T\), followed by a query input \(x_{\mathrm{query}}\).
- The loss compares the model prediction \(f_{\theta}(P)\) against the target function value \(h(x_{\mathrm{query}})\) at the query point.

Interpretation:
- This equation defines supervised meta-training for in-context learning: the model parameters are chosen so that, given a prompt of examples from an unknown function \(h\), the model predicts the function value at a held-out query input.
- The objective connects directly to the surrounding text, which introduces formal preliminaries for theoretical analysis of in-context learning and then uses this definition before moving to embedding matrices and a linear self-attention model.
- The prompt length \(T\) corresponds to the number of in-context examples used during training, as described in the surrounding definition.


(4) 

21 

i.i.d. where _xi_ , _x_ query _∼Dx_ and _h ∼DH_ are independent. We call _T_ the _length of the prompts seen during training._ 

Let _E ∈_ **R**<sup>_de×dT_</sup> denote an embedding matrix associated with a prompt _P_ = ( _x_ 1, _y_ 1, . . . , _xT_ , _yT_ , _x_ query). Following Zhang et al. (2023a), we form each column from ( _xi_ , _yi_ )<sup>_⊤_</sup> _∈_ **R**<sup>_d_+1</sup> for _i_ = 1, . . . , _T_ , and use ( _x_ query, 0)<sup>_⊤_</sup> as the final column. For _xi ∈_ **R**<sup>_d_</sup> and _yi ∈_ **R** , we have _de_ = _d_ + 1 and _dT_ = _T_ + 1. Under the prompt representation _P_ , the embedding matrix can be written as 


![](P030_images/P030.pdf-0022-02.png)


We introduce weight matrices _W_<sup>_Q_</sup> , _W_<sup>_K_</sup> _∈_ **R**<sup>_dk×de_</sup> for the query and key, _W_<sup>_V_</sup> _∈_ **R**<sup>_dv×de_</sup> for the value, _W_<sup>_P_</sup> _∈_ **R**<sup>_de×dv_</sup> for projection, and a normalization constant _ρ >_ 0. 

For the sake of tractability in theoretical analysis, following Zhang et al. (2023a), we consider a single-layer _linear self-attention (LSA)_ model. This variant streamlines the standard self-attention by eliminating the softmax step and merging the projection matrices. Specifically, we define merged operators _W_<sup>_KQ_</sup> _∈_ **R**<sup>_de×de_</sup> (query–key) and _W_<sup>_PV_</sup> _∈_ **R**<sup>_de×de_</sup> (projection–value). Letting _θ_ = ( _W_<sup>_KQ_</sup> , _W_<sup>_PV_</sup> ), the LSA model can be formulated as 


![](P030_images/P030.pdf-0022-05.png)


The prediction corresponding to the query token _x_ query is given by the bottom-right entry of _f_ LSA: 


![](P030_images/P030.pdf-0022-07.png)


To streamline the theoretical development, we restrict attention to in-context learning with linear predictors, in line with the setup of Zhang et al. (2023a). We assume that all clients share the same sampling procedure for generating training prompts. Let Λ be a positive definite covariance matrix. For each task indexed by _τ ∈_ **N** , we construct a training prompt 


![](P030_images/P030.pdf-0022-09.png)


The task-specific parameter _xτ_ ,query are sampled i.i.d. from _w Nτ_ is drawn independently from (0, Λ), and the labels are defined by the linear rule _N_ (0, _Id_ ), the inputs _h xττ_ (, _ix_ and) = _⟨wτ_ , _x⟩_ . 

Each prompt _Pτ_ is then converted into an embedding matrix _Eτ_ using the transformation in Eq. (5): 


![](P030_images/P030.pdf-0022-12.png)


The empirical risk evaluated over _B_ independent prompts is given by 


![](P030_images/P030.pdf-0022-14.png)


To study the limiting behavior, we introduce the population loss obtained as _B →_ ∞: 


![](P030_images/P030.pdf-0022-16.png)


Here the expectation is taken over the random task weight _wτ ∼N_ (0, _Id_ ) and the covariates _{xτ_ , _i}i_<sup>_T_</sup> =1<sup>_∪{xτ_,query</sup><sup>_}_, drawn i.i.d. from</sup><sup>_N_(0, Λ).</sup> 

We analyze optimization via the _gradient flow_ framework, which describes the continuoustime limit of gradient descent with infinitesimal step size. The dynamics of the parameters follow the ODE 


![](P030_images/P030.pdf-0022-19.png)


22 

In the remainder, we study gradient flow trajectories under initializations that satisfy the following assumptions in Zhang et al. (2023a): 

**Assumption C.2** (Initialization (Zhang et al. (2023a))) **.** Let _σ >_ 0 be a parameter, and let Θ _∈_ **R**<sup>_d×d_</sup> be any matrix satisfying _∥_ ΘΘ<sup>_⊤_</sup> _∥F_ = 1 and ΘΛ = 0 _d×d_ . We assume 


![](P030_images/P030.pdf-0023-02.png)


under suitable initialization, gradient flow will converge to a global optimum. 

**Theorem C.3** ((Theorem 4.1 of Zhang et al. (2023a)) Convergence and limits) **.** Consider the gradient flow of the linear self-attention network _f_ LSA defined in (6) over the population loss (8). Suppose the initialization satisfies Assumption C.2 with initialization scale _σ >_ 0 satisfying _σ_<sup>2</sup> _∥_ Γ _∥op√d <_ 2 where we have defined 


![](P030_images/P030.pdf-0023-05.png)


Then, the gradient flow converges to a global minimum of the population loss (8). Moreover, _W_<sup>_PV_</sup> and _W_<sup>_KQ_</sup> converge to _W∗_<sup>_PV_</sup> and _W∗_<sup>_KQ_</sup> respectively, where 


![](P030_images/P030.pdf-0023-07.png)


At the global optimum with parameters _W∗_<sup>_KQ_</sup> and _W∗_<sup>_PV_</sup> , the prediction for the query token takes the form 


![](P030_images/P030.pdf-0023-09.png)


### **C.2 Proof of Theorem 4.1** 

According to the above preliminary theoretical results adopted from Zhang et al. (2023a), we have the following analysis. 

_Proof._ First by our assumption of the client and server data, we have 


![](P030_images/P030.pdf-0023-13.png)


and 


![](P030_images/P030.pdf-0023-15.png)


where the variance _σi_<sup>2are different from client to client, representing the heterogeneity over</sup> clients. Then we have the following inequality holds with probability at least 1 _− δ_ : 


![](P030_images/P030.pdf-0023-17.png)


23 

where for the second inequality, we use the standard matrix concentration inequality, for the last one, we use the fact that _T_ is large enough and _M ≥_ 4 _d_ log _δ_<sup>_−_1</sup> , where 


![](P030_images/P030.pdf-0024-01.png)


Similarily, with probability at least 1 _− δ_ , we have for all _i ∈_ [ _L_ ], 

First, with Eq.(12) and the algorithm design of Algorithm 2, we have the following guarantees 


![](P030_images/P030.pdf-0024-04.png)


Then we can prove the theorem by induction. 

Assume _ak_ , _m_ = _θk_<sup>_⊤qm_holds for episode</sup><sup>_k_, which trivially holds at episode 1 with</sup><sup>_θ_1= 0 as</sup> _a_ 1, _m_ = 0, _∀m ∈_ [ _M_ ]. According to Eq.(15), Eq.(16), and _ak_ +1, _m_ = ∑ _i_<sup>_L_</sup> =1<sup>_wi_</sup> _k_ +1, _m_<sup>_ai_</sup> _k_ +1, _m_<sup>, we have</sup> 


![](P030_images/P030.pdf-0024-07.png)


Then, we have 

24 

Then appreately, we have shown that for each _k_ , _ak_ , _m_ = _θk_<sup>_⊤qm_canbewrittenasalinear</sup> function of the query _qm_ . Next we bound _θ_<sup>¯</sup> _k_ and _Hk_ separately. We have 


![](P030_images/P030.pdf-0025-01.png)


and 

**Bound** _Ak_ , _m_ **.** For _Ak_ , _m_ by (14), we have 


![](P030_images/P030.pdf-0025-04.png)


**Bound** _Bk_ , _m_ **.** For _Bk_ , _m_ , recall that _q_<sup>_i_</sup> _n_<sup>_∼N_(0, Λ) and</sup><sup>_ϵ_</sup> _n_<sup>_i∼N_(0,</sup><sup>_σ_</sup> _i_<sup>2), then Λ</sup><sup>_−_1/2</sup><sup>_qi_</sup> _n_<sup>_∼N_(0,</sup><sup>_I_).</sup> Then applying concentration inequality on sub-exponential random vectors, with probability at least 1 _− δ_ , we have 


![](P030_images/P030.pdf-0025-06.png)


**Bound** _Ck_ , _m_ **.** For _Ck_ , _m_ , using (13) and (14), we have 


![](P030_images/P030.pdf-0025-08.png)


**Bound** _Dk_ , _m_ **.** For _Dk_ , _m_ , using (13) and (14), we have 


![](P030_images/P030.pdf-0025-10.png)


25 

Therefore, combining (20) to (23), we have 


![](P030_images/P030.pdf-0026-01.png)


Since 

and 

Then applying recursion onto (24), we have that for all _k_ , 


![](P030_images/P030.pdf-0026-05.png)


## **D Prompt** 

### **D.1 Server Query Dataset Initialize** 

To initialize the query dataset, the server distributes queries to multiple clients. Each client employs its local LLM to generate the responses for the assigned queries. The responses are then returned to the server, which aggregates them to form the initial server-side query dataset. The prompts used to guide this response generation are described as follows. 

### **Server Query Initialization Prompt for MMLU-Pro & AQUA-RAT Reasoning Benchmark** 

You are a knowledgeable assistant. For the following multiple-choice question, briefly explain your reasoning (no more than _{_ sentences ~~l~~ imit _}_ sentences), then end with the exact sentence: The answer is (X). 

#### **Rules:** 

1. X must be the option letter only (A/B/C/D/. . . ). Do not include the option text. 

2. Do not include any content after the final sentence. 

3. Keep your entire response within _{_ token ~~l~~ imit _}_ tokens. 

#### **Question:** _{_ query _}_ 

**Answer:** Let’s think step by step. _{_ text _}_ 

### **Server Query Initialization Prompt for MMLU-Pro & AQUA-RAT Standard QA Benchmark** 

You are taking a multiple-choice question. Read the following question carefully and select the single best answer. Do not explain your reasoning. Output only the final answer choice letter (A, B, C, D, . . . ). 

#### **Rules:** 

1. The output must be a single uppercase letter (A/B/C/D/. . . ) with no punctuation or extra text. 

26 

2. Do not include any explanation or content after the answer. 

3. Keep the response within _{_ token ~~l~~ imit _}_ tokens. 

**Question:** _{_ query _}_ 

**Answer:** 

### **Server Query Initialization Prompt for GSM8K Reasoning Benchmark** 

You are a knowledgeable assistant. For the following math question, briefly explain your reasoning (no more than _{_ sentences ~~l~~ imit _}_ sentences), then end with the exact sentence: The answer is X. 

#### **Rules:** 

1. X must be a single numeric value (e.g., 12, -3/5, 7.25); no units or extra text. 

2. If X is a fraction, reduce it to simplest terms; if a decimal, use standard form without trailing zeros. 

3. Do not include any content after the final sentence. 

4. Keep the entire response within _{_ token ~~l~~ imit _}_ tokens. 

**Question:** _{_ query _}_ 

**Answer: Let’s think step by step.** 

### **D.2 Client Response Generation for Server Queries** 

The framework of FERA is outlined in Algorithm 2. In Step 2, each client relabels its local data by constructing prompts that incorporate demonstrations selected from the server dataset. In Step 3, the client relabels the server data by constructing prompts that include demonstrations drawn from its updated local dataset. The prompts used in Step 2 and Step 3 are described below. Unless otherwise specified, the default number of demonstrations is set to 5. 

### **Client Prediction Prompt for MMLU-Pro & AQUA-RAT Reasoning Benchmark** 

You are tasked with answering multiple-choice math questions. Below are several example questions with their step-by-step reasoning and final answers. After reviewing these examples, you will be presented with a new question to answer. 

#### **Guidelines:** 

1. Provide clear, concise, and logically coherent step-by-step reasoning (at most _{_ sentences ~~l~~ imit _}_ sentences). 

2. End with the exact sentence: The answer is (X). 

3. X must be the option letter only (A, B, C, D, . . . ); do not include the option text. 

4. Include no additional content after the final answer sentence. 

5. Keep the complete response within _{_ token ~~l~~ imit _}_ tokens. 

**Examples:** 

- _{_ examples _}_ 

**Question:** 

_{_ query _}_ 

**Answer:** Let’s think step by step. 

27 

### **Client Prediction Prompt for MMLU-Pro & AQUA-RAT Standard QA Benchmark** 

You are taking a multiple-choice question. Below are several example questions with their final answers. After reviewing these examples, you will be presented with a new question to answer. 

#### **Guidelines:** 

1. Read the question carefully and select the single best answer. 

2. Do not explain your reasoning. 

3. Output only the final answer choice letter (A, B, C, D, . . . ); do not include the option text. 

4. Do not include any additional content after the answer. 

**Examples:** 

- _{_ examples _}_ 

**Question:** _{_ query _}_ **Answer:** 

### **Client Prediction Prompt for GSM8K Reasoning Benchmark** 

You are tasked with answering math questions in this domain. Below are several example questions with their step-by-step reasoning and final answers. After reviewing these examples, you will be presented with a new question to answer. 

#### **Guidelines:** 

1. Provide clear, concise, and logically coherent step-by-step reasoning. 

2. End your response with the exact sentence: The answer is X. 

3. X must be a single numeric value (e.g., 12, -3/5, 7.25); no units or extra text. 

4. If X is a fraction, reduce it to simplest terms; if a decimal, use standard form without trailing zeros. 

5. Include no additional content after the final answer sentence. 

6. Keep the complete response within _{_ token ~~l~~ imit _}_ tokens. 

#### **Examples:** 

_{_ examples _}_ **Question:** _{_ query _}_ **Answer:** Let’s think step by step. 

### **D.3 Uncertainty-Aware Aggregration** 

In the FERA framework, Uncertainty-Aware Aggregation is employed on the server side to combine responses from clients. The weights used in this aggregation are first computed according to Equation 3, after which uncertainty is leveraged to guide the aggregation process. For the standard QA task, we propose the UA-WA algorithm, described in Section 4.2, while for complex reasoning tasks we design the UA-SCA algorithm, detailed in Algorithm 1. The prompts utilized in UA-SCA are presented below. 

### **Summarize** 

You are a cognitive reasoning analyst tasked with examining _{_ len(reasoning ~~l~~ ist) _}_ reasoning responses derived from the following question. 

**Question:** _{_ question _}_ 

28 

#### **Reasoning Responses:** 

- _{_ reasoning ~~f~~ ormatted _}_ 

#### **Analysis Objective:** 

Provide a concise analytical characterization of this reasoning cluster. Identify the cognitive patterns, methodological strategies, and structural similarities across the responses. 

#### **Characterization Guidelines:** 

1. Synthesize the distinguishing features of these reasoning responses 

2. Emphasize their reasoning methodology and structural organization 

3. Identify common problem-solving paradigms across responses 

4. Present your analysis within _{_ token ~~l~~ imit _}_ tokens 

5. Capture the essential cognitive characteristics of this cluster 

#### **Your Analysis:** 

### **SelfCritique for MMLU-Pro and AQUA-RAT Benchamrk** 

You are improving a reasoning response by incorporating insights from conflicting reasoning approaches. 

**Original Question:** 

- _{_ question _}_ 

#### **Target Reasoning Response (to be improved):** 

- _{_ target ~~r~~ esponse _}_ 

#### **Alternative Approaches Summary:** 

- _{_ alternatives ~~f~~ ormatted _}_ 

#### **Task:** 

Create an enhanced version of the target reasoning response by incorporating valuable insights from the alternative approaches. Identify reasoning elements, methodologies, or perspectives from the conflicting summaries that could strengthen the original response. 

#### **Requirements:** 

1. Use the target reasoning response as your foundation 

2. Extract valuable insights from the alternative approaches 

3. Integrate these insights to create a more comprehensive response 

4. Maintain logical consistency throughout 

5. Present only the final improved reasoning 

6. Conclude with: ‘‘The answer is (X)’’ where X is the option letter only (A/B/C/D/...) 

7. Exclude option text after the letter 

8. Limit response to _{_ token ~~l~~ imit _}_ tokens 

9. Omit meta-commentary or explanatory analysis 

#### **Improved Response:** 

### **SelfCritique for GSM8K Benchamrk** 

You are improving a reasoning response by incorporating insights from conflicting reasoning approaches. 

#### **Original Question:** 

- _{_ question _}_ 

**Target Reasoning Response (to be improved):** 

- _{_ target ~~r~~ esponse _}_ 

29 

#### **Alternative Approaches Summary:** 

- _{_ alternatives ~~f~~ ormatted _}_ 

#### **Task:** 

Create an enhanced version of the target reasoning response by incorporating valuable insights from the alternative approaches. Identify reasoning elements, methodologies, or perspectives from the conflicting summaries that could strengthen the original response. 

#### **Requirements:** 

1. Start with the target reasoning as your foundation 

2. Identify useful insights from the conflicting summaries that could improve the reasoning 

3. Integrate these insights to create a stronger, more comprehensive reasoning 

4. Maintain logical consistency throughout 

5. Present only the final improved reasoning 

6. End with "The answer is X". 

7. Limit response to _{_ token ~~l~~ imit _}_ tokens 

8. No meta-commentary or analysis explanation 

**Improved Response:** 

### **Aggregation for MMLU-Pro and AQUA-RAT Benchmark** 

You are synthesizing multiple reasoning responses to create a single, unified reasoning path. 

#### **Context:** 

You are given several reasoning responses to the same question, each from a different client. A final answer has been determined by majority vote. Each response includes a confidence score (higher = more confident). 

#### **Question:** 

- _{_ question _}_ 

#### **Client Responses (with confidence scores):** 

- _{_ client ~~e~~ ntries _}_ 

#### **Task:** 

Produce a single, concise, professional, and logically coherent merged reasoning response that synthesizes the reasoning leading to the final answer. 

#### **Requirements:** 

1. Synthesize the reasoning leading to the final answer 

2. Give greater weight to reasoning from higher-confidence responses 

3. Avoid unnecessary repetition or irrelevant details 

4. Keep the ENTIRE response (reasoning + final answer) within _{_ token ~~l~~ imit _}_ tokens 

5. End with: ‘‘The answer is (X)’’ where X is the option letter only (A/B/C/D/...) 

6. Do not include the option text after the letter 

7. Maintain professional and logical coherence throughout 

#### **Merged Reasoning Response:** 

### **Aggregation for MMLU-Pro and AQUA-RAT Benchmark** 

You are synthesizing multiple reasoning responses to create a single, unified reasoning path. 

30 

#### **Context:** 

You are given several reasoning responses to the same question, each from a different client. Each response includes a confidence score (higher = more confident). 

- **Question:** _{_ question _}_ 

- **Client Responses (with confidence scores):** _{_ client ~~e~~ ntries _}_ **Task:** 

Produce a single, concise, professional, and logically coherent merged reasoning response that synthesizes the reasoning leading to the final answer. 

#### **Requirements:** 

1. Synthesize the reasoning leading to the final answer 

2. Give greater weight to reasoning from higher-confidence responses 

3. Avoid unnecessary repetition or irrelevant details 

4. Keep the ENTIRE response (reasoning + final answer) within _{_ token ~~l~~ imit _}_ tokens 

5. End with: ‘‘The answer is (X)’’ where X is the option letter only (A/B/C/D/...) 

6. Do not include the option text after the letter 

7. Maintain professional and logical coherence throughout 

#### **Merged Reasoning Response:** 

### **Aggregation for GSM8K Benchmark** 

You are synthesizing multiple reasoning responses to create a single, unified solution path. 

#### **Context:** 

You are given several reasoning responses to the same question, each from a different client. Each response includes a confidence score (higher = more confident). 

#### **Question:** 

- _{_ question _}_ 

#### **Client Responses (with confidence scores):** 

- _{_ client ~~e~~ ntries _}_ 

#### **Task:** 

Produce a single, concise, professional, and logically coherent merged reasoning response that synthesizes the reasoning leading to the final answer. 

#### **Requirements:** 

1. Synthesize the reasoning leading to the final answer 

2. Give greater weight to reasoning from higher-confidence responses 

3. Avoid unnecessary repetition or irrelevant details 

4. Keep the ENTIRE response (reasoning + final answer) within _{_ token ~~l~~ imit _}_ tokens 

5. End with the exact sentence: ‘‘The answer is X.’’ 

6. X must be a single numeric value (e.g., 12, -3/5, 7.25) 

7. No units or extra text after the answer 

#### **Merged Reasoning Response:** 

### **D.4 FERA Variants** 

**FERA-GT.** To evaluate the effectiveness of FERA, we compare it with a simplified baseline, FERA-GT. In this baseline, the server issues a query to clients, who independently retrieve the top- _C_ question–answer pairs using the MMR demonstration strategy. These retrieved pairs serve as fixed context for generating client responses, which are then aggregated by 

31 


![](P030_images/P030.pdf-0032-00.png)

### Figure analysis

Purpose: The figure visualizes how client-local dataset distributions vary under different Dirichlet-style α settings on the MMLU-Pro benchmark, supporting the surrounding discussion of federated evaluation settings and client heterogeneity.

Structure and labels:
- The figure contains three side-by-side heatmap panels titled **α = 1.0**, **α = 10.0**, and **α = 100.0**.
- The y-axis lists three clients: **C1**, **C2**, and **C3**.
- The x-axis appears to represent benchmark categories or data partitions, but the category labels are not shown/readable.
- Each panel includes a vertical colorbar. The color scale runs from teal/green for lower values through pale/white to salmon/red for higher values.

Readable colorbar ticks:

| Panel | Readable colorbar tick labels |
|---|---|
| α = 1.0 | 100, 200, 300 |
| α = 10.0 | 100, 200 |
| α = 100.0 | 50, 100, 150 |

Panel observations:
- **α = 1.0:** The heatmap shows stronger variation across clients and columns. Some cells are distinctly salmon/red while others are teal, indicating pronounced imbalance among client-category allocations.
- **α = 10.0:** The distribution remains non-uniform, but the visual contrast is less extreme than in α = 1.0. Several columns still show client-specific high or low allocations.
- **α = 100.0:** The cells appear more consistently pale pink/white across clients, with fewer strongly teal or saturated red cells, indicating a more even allocation pattern.

Direct visual comparison:
- Increasing α is associated with reduced visual heterogeneity across the three clients.
- The α = 1.0 panel displays the most skewed client distribution, while α = 100.0 appears the most balanced.

Interpretation in context:
- The figure likely illustrates the experimental client data partitioning used for the MMLU-Pro benchmark. It provides visual evidence for how different α settings control non-IID severity across clients, which is relevant to evaluating FERA and its variants under varying degrees of client dataset imbalance.


Figure 7: Client dataset distribution under different _α_ settings on the MMLU-Pro benchmark. 

the server to produce the final answer. Importantly, FERA-GT completes this process in a single communication round without iterative context refinement. In contrast, FERA employs multiple rounds of interaction, enabling dynamic context updates and progressively enhanced answer quality—underscoring its adaptability and superior reasoning depth. 

**FERA-Q.** FERA-Q corresponds to a simplified setting where the LLM is limited to predicting only the final answer to each question, without generating intermediate reasoning steps. In this setup, when clients select demonstrations from their local datasets, they discard the reasoning trajectories _S{_ 1: _T}_ and retain only the final answers _a_ . This setting reflects scenarios in which the LLM lacks the ability to handle or benefit from step-by-step reasoning. During inference, each client uses the selected final-answer-only demonstrations to generate predictions for the server-issued query set. The predicted answers are then sent back to the server. The server performs aggregation using the _Uncertainty-Aware Weighted Averaging_ (UA-WA) strategy, which weights client responses based on their confidence scores. The aggregated results are used to update the global query–answer set, enabling iterative refinement even without explicit reasoning steps. 

**FERA-Free.** FERA-Free refers to a setting where clients have local LLMs but no labeled data—only question prompts are available locally. Since clients cannot construct demonstrations from their own data, they rely entirely on query-answer pairs provided by the server. In each round, the server distributes example queries and answers. Clients use these examples to prompt their local LLMs and generate responses to new server queries. The server then aggregates responses using uncertainty-aware methods (UA-WA or UASCA) and refines the query-answer set for the next round. This setup captures a practical constraint where local data may be unlabeled due to privacy, cost, or domain limitations. FERA-Free shows that meaningful collaboration is possible even without local supervision by leveraging server-side guidance. 

## **E Experiment Setup** 

### **E.1 Construction of Client Datasets** 

To evaluate FERA under realistic heterogeneous and domain-specialized conditions, we simulate a federated environment by partitioning each benchmark into client-specific subsets. 

**MMLU-Pro.** MMLU-Pro spans 14 diverse subject areas—including physics, medicine, philosophy, economics, and law—which naturally provides a multi-domain foundation for studying specialized client expertise. To introduce controlled heterogeneity across clients, we construct client partitions using a Dirichlet-based sampling scheme. Specifically, for each client, we draw a label-distribution vector _q ∈_ **R**<sup>_M_</sup> from a Dirichlet distribution _q ∼_ Dir( _αp_ ), where _p_ denotes the global class distribution and _α_ controls the degree of non-IID variation. Smaller values of _α_ yield more skewed, domain-focused partitions (i.e., clients specializing in a small subset of subjects), whereas larger values produce more balanced distributions. We consider three heterogeneity levels with _α ∈{_ 1.0, 10, 100 _}_ , covering a wide spectrum from highly specialized to near-homogeneous splits. Examples of the resulting client-domain distributions are shown in Figure 7. 

32 

**AQUA-RAT and GSM8K.** These datasets do not provide explicit category labels. In line with prior work, we partition them using random splits across clients. Although these tasks do not include domain metadata, the federated setting still benefits from distributional diversity introduced by varying client sample sizes and reasoning styles. 

### **E.2 Implementation Details** 

For all experiments involving FERA and its variants, we fix the number of clients to three. We evaluate these algorithms on the MMLU-Pro, GSM8K, and AQUA-RAT benchmarks, covering both reasoning and standard QA tasks. On the client side, we use Qwen3-4B and Llama3.1-8B as base models. During prediction, we set the sampling parameters to _top p_ = 0.8 and temperature = 0.3. On the server side, no LLM is deployed for standard QA tasks. For complex reasoning tasks, the default server model is set to GPT-4o-mini. 

For LLM-Debate Du et al. (2023), we ensure a fair comparison with FERA by adopting the same client models and the same number of clients as in the FERA setup. Moreover, the summarization model in LLM-Debate is configured to match the server model used in FERA, and the number of debate rounds is set to 5. 

For FedAvg (McMahan et al., 2017), We implement FedAvg following the OpenFedLLM framework Ye et al. (2024) on two LLMs ensuring consistency with other baselines. The training process consists of 50 communication rounds involving three clients, with data partitioned according to to a Dirichlet distribution. Each client fine-tunes the model locally using a batch size of 16, a sequence length of 256, and one gradient accumulation step, with a learning rate of 1e-5. To improve parameter efficiency, Low-Rank Adaptation (LoRA) is applied and 8-bit quantization Hu et al. (2022). After each local update, model weights are aggregated using FedAvg on a central server, which then redistributes the updated global model to clients for the next round of local fine-tuning. 

For FLora (Wang et al., 2024c), we conduct experiments using Llama-3.1-8B and Qwen3-4B in a heterogeneous setting, where clients are assigned different LoRA rank values— _i.e._ , [64, 32, 16]—following the default configuration in their official implementations. All hyperparameters are kept unchanged, except for the number of clients. The models are trained using our client data and evaluated on our server data. 

### **E.3 Communication and Computational Cost** 

Transmission cost refers to the communication overhead between clients and the server, measured in total bits exchanged across different algorithms. For FERA, its variants, and LLM-Debate, we set the number of iterative update rounds to six. For traditional federated learning baselines such as FedAvg, the number of communication rounds is set to 50, consistent with the experimental setup described in Appendix E. 

Both questions and responses are tokenized, with each response capped at a maximum of _C_ = 256 tokens. The total number of queries is fixed at _M_ = 70 across all benchmarks. Transmission cost accounts for both the tokens sent by clients and the server in each round, allowing for a fair comparison of communication efficiency across different methods. 

**Computational cost.** We measure computational cost in FLOPs. For a transformer with _|θ|_ parameters, one forward pass on a sequence of _n_ tokens costs approximately 2 _n|θ|_ FLOPs, and one backward pass costs approximately 4 _n|θ|_ FLOPs (Kaplan et al., 2020). We use the following notation: _L_ is the number of clients, _M_ the number of server queries, _N_ the number of local examples per client, _ns_ the sequence length per LLM call, _|θ|_ and _|θ_<sup>_S_</sup> _|_ the number of parameters of the client and server model respectively, _K_ the number of rounds for training-free methods, _K_ fed the number of rounds for training-based methods, _E_ the number of local training epochs, _B_ the training batch size, _r_ the LoRA rank, _d_ the model hidden dimension, and<sup>�</sup> _L_ the number of weight matrices with LoRA applied. 

**FERA.** In each round, every client performs inference on _N_ local examples (local refinement) and _M_ server queries (client labeling), and the server aggregates responses for _M_ queries. 

33 

All operations are forward-only: 


![](P030_images/P030.pdf-0034-01.png)


**LLM-Debate.** In each round, every client generates responses for _M_ queries, the server summarizes the responses, and all clients revise based on the summary. All operations are forward-only: 


![](P030_images/P030.pdf-0034-03.png)


**FedAvg.** Each of _L_ clients performs _E_ epochs of fine-tuning over _N_ local examples with batch size _B_ . Each gradient step involves one forward and one backward pass: 


![](P030_images/P030.pdf-0034-05.png)


**FLoRA.** Same structure as FedAvg but with LoRA: the forward pass traverses the full model (2 _Bns|θ|_ ), while the backward pass updates only the adapter parameters _|θ_ LoRA _|_ = 2<sup>�</sup> _Lrd ≪ |θ|_ : 


![](P030_images/P030.pdf-0034-07.png)


Table 1 instantiates these formulas. We use _ns_ =256 for all methods to ensure a fair comparison. For training-based methods, we use _K_ fed=50 communication rounds (as in our experimental setup), while FERA and LLM-Debate use _K_ =6 rounds. 

The table reveals that FERA’s computational cost (8.9 _×_ 10<sup>16</sup> FLOPs) is dramatically lower than training-based methods: 8 _×_ cheaper than FedAvg (7.4 _×_ 10<sup>17</sup> ) and 3 _×_ cheaper than FLoRA (2.5 _×_ 10<sup>17</sup> ), because training-based methods require _K_ fed=50 rounds of expensive backward passes while FERA uses only forward inference over _K_ =6 rounds. Compared to LLM-Debate (4.1 _×_ 10<sup>16</sup> ), FERA costs approximately 2 _×_ more FLOPs due to the local refinement step ( _LN_ inference calls per round), but this additional computation directly translates into substantial accuracy improvements: as shown in Section 5.3, the local refinement step enables FERA to progressively integrate client knowledge across rounds, consistently outperforming LLM-Debate by a significant margin across all benchmarks. This represents a favorable trade-off: a moderate 2 _×_ increase in FLOPs yields substantial accuracy gains, while remaining an order of magnitude cheaper than training-based alternatives. 

### **E.4 Demonstration Selection** 

In **Step 2** and **Step 3** of Algorithm 2, FERA selects demonstrations either from the server’s query set or from the local client dataset. These demonstrations are used to facilitate clientside labeling and to update the server’s query–answer set. The selection process is governed by Equation 1, which implement a similarity–diversity trade-off strategy. In both equations, the function Sim measures the similarity between reasoning examples. To compute this, each example is first embedded using the paraphrase-MiniLM-L6-v2 model (Reimers, 2019), which converts the textual reasoning into fixed-length vectors. Cosine similarity is then applied by default to quantify the similarity between embedded representations. The function Div captures the diversity within the selected set of demonstrations, encouraging the inclusion of examples that are distinct from one another. This prevents redundancy and promotes a richer representation of reasoning styles. A trade-off exists between selecting highly relevant demonstrations (those similar to the target query) and ensuring sufficient diversity within the set. This trade-off is controlled by the hyperparameter _λ_ , which balances the weight between relevance and diversity. Unless otherwise specified, we set _λ_ = 0.5 as the default value. 

34 


![](P030_images/P030.pdf-0035-00.png)


Figure 8: Performance comparison of FERA and its variants against baseline methods on the MMLUPRO benchmark under varying degrees of client-level data heterogeneity, using Qwen3-4B as the base model. Client data heterogeneity is simulated via a Dirichlet distribution with concentration parameter _α ∈_ [1.0, 10, 100], where smaller _α_ values correspond to more severe heterogeneity across clients and larger values indicate increasingly homogeneous data distributions. 

### **E.5 Uncertainty Calculation** 

We use the uncertainty scores to guide the aggregation of client responses on the server side. Each client generates both predictions and their corresponding logits, from which we calculate uncertainty following the approach of Duan et al. (2023); Farquhar et al. (2024); Zhang et al. (2025). To quantify the model’s confidence in its generated responses, we employ a token-level entropy-based uncertainty estimation approach. Specifically, for each generated token position _t_ , we calculate the entropy of the probability distribution over the vocabulary: 


![](P030_images/P030.pdf-0035-04.png)


where _pt_ , _i_ represents the softmax probability of token _i_ at position _t_ , _V_ is the vocabulary size, and _ε_ = 1 _×_ 10<sup>_−_10</sup> ensures numerical stability. The overall uncertainty score is computed as the average entropy across all _T_ generated tokens: 


![](P030_images/P030.pdf-0035-06.png)


This metric captures the model’s predictive confidence, where higher entropy values indicate greater uncertainty in token selection, while lower entropy values reflect more confident probability distributions. This approach provides a straightforward yet effective measure of generation uncertainty that can be computed directly from the model’s output logits without requiring additional training or calibration, making it well-suited for our federated learning framework. 

## **F Supplementary Experiments** 

### **F.1 Main Results Using Qwen3-4B as the Client Model** 

Figure 8 and Figure 9 report the performance of FERA with Qwen3-4B as the client model, compared against FERA variants and baseline methods on the MMLU and AQUA-RAT benchmarks. The results show that FERA consistently outperforms competing approaches even when using Qwen3-4B, demonstrating its robustness across different client models. 

Figure 10 illustrates how the performance of FERA, FERA-Free, and FERA-Q evolves with an increasing number of interaction rounds. As the number of iterations increases, all variants show noticeable performance gains, demonstrating the effectiveness of the iterative refinement mechanism in the proposed framework. 

### **F.2 Additional Ablation Study** 

**Effect of Client Model Capacity Heterogeneity.** To examine the impact of heterogeneous model capacities, we conduct an ablation in which clients use LLMs of different sizes: 

35 


![](P030_images/P030.pdf-0036-00.png)


Figure 9: Performance comparison of FERA and its variants against baseline methods on the AQUA-RAT benchmark, with Qwen3-4B serving as the client-side model. 


![](P030_images/P030.pdf-0036-02.png)


Figure 10: Effect of interaction round count on the performance of FERA and FERA-Free in the MMLU-Pro benchmark. The Dirichlet concentration parameter is set to _α_ = 10.0 to simulate moderate client-level data heterogeneity. All experiments use Qwen3-4B as the client model. 


![](P030_images/P030.pdf-0036-04.png)



![](P030_images/P030.pdf-0036-05.png)


Figure 11: Effect of model-capacity heterogeneity on FERA performance for the MMLU-Pro benchmark. 

Figure 12: Effect of Uncertainty Characteristics on FERA performance for the MMLU-Pro benchmark. 

Qwen3-4B, Qwen3-1.7B, and Qwen3-0.6B. As shown in Figure 11, smaller models exhibit higher initial uncertainty but their uncertainty decreases steadily over communication rounds. The overall performance of FERA remains comparable to the homogeneous Qwen34B setting, suggesting that uncertainty-aware weighting effectively moderates less reliable client contributions. 

**Effect of Uncertainty Characteristics.** We isolate the effect of uncertainty from model capacity by having all clients use Qwen3-4B but with different decoding temperatures (0.3, 0.5, 0.8). As shown in Figure 12, FERA achieves similar accuracy across all settings while uncertainty decreases over rounds, suggesting that iterative refinement stabilizes generation behavior. 

**Effect of Demonstration Quality.** We simulate degraded reasoning by randomly subsampling reasoning steps (e.g., 30%len retains 30% of steps). As shown in Figure 13, truncating demonstrations lowers FERA’s performance, but degradation is graceful rather than catastrophic—uncertainty-weighted aggregation limits the influence of unreliable clients, and self-critique corrects inconsistent reasoning paths at the server. 

**Effect of Client Model Capacity.** In our default configuration, clients run open-source LLMs (e.g., Qwen3-4B or Llama-3.1-8B), while the server model varies by task. In this ablation, to isolate the impact of using a closed-source stack and to remove model heterogeneity between endpoints, we set both the client and the server to GPT-4o-mini. The 


![](P030_images/P030.pdf-0036-12.png)


Figure 13: Performance of FERA under Varying Client Reasoning Response Quality. 

36 


![](P030_images/P030.pdf-0037-00.png)



![](P030_images/P030.pdf-0037-01.png)


Figure 15: FERA performance in a Figure 14: FERA performance on the MMLUPro reasoning benchmark.server models are GPT-4o-mini.Both the client and specialized-domain setting on the MMLU-Prolaw category. Client models use Qwen3-4B, and the server model is GPT-4o-mini. 


![](P030_images/P030.pdf-0037-03.png)


Figure 16: Performance of FERA under different demonstration selection strategies across MMLUPro, AQUA-RAT, and GSM8K. 

GPT-4o-mini API exposes response-level scores (log-probability–based confidences), which we use directly to compute uncertainty for our Uncertainty-Aware Demonstration Selection and Uncertainty-Aware Aggregation, without any additional reward/critic model. This keeps the uncertainty signal aligned with the generator’s own beliefs and ensures a fair comparison under identical decoding settings. The results, presented in Figure 14, demonstrate that FERA remains effective even in a closed-source setting. It consistently outperforms the FERA-GT baseline across communication rounds, indicating that FERA is model-agnostic and capable of leveraging native confidence signals to enhance performance. 

**Effect of Specialized Domains.** To evaluate FERA in settings where client expertise is concentrated within a particular domain, we conduct an additional experiment using the law category of MMLU-Pro, which is the domain where the server model shows the weakest standalone performance. We construct a server-side evaluation set by selecting 50 law questions, and distribute all remaining MMLU-Pro questions across clients using the same non-IID Dirichlet partitioning as in our main experiments. This yields a domain-imbalanced configuration in which the server has limited direct exposure to law-domain data and must rely on clients that hold the majority of the relevant information. As shown in Figure 15, FERA steadily improves over communication rounds and outperforms all baselines, indicating that the framework can effectively integrate specialized client knowledge even when the server begins with weak domain proficiency. 

**Effect of Demonstration Selection Strategy.** Figure 16 presents a comparison of four client-side demonstration selection strategies, which guides how to determine the set _Sk_<sup>_i_</sup> , _Q_ denoted in Step 2 and 3 of FERA. They are (i) _A-S (MMR)_ , our default selection (ii) _A-S (KNN)_ uses the same adaptive selector but instantiates it with _k_ -nearest neighbors (KNN). Given a sample ( _q_ , _s_ 1: _T_ , _a_ ) and a candidate dataset, the selector first embeds the sample, computes similarity scores to all candidates, and selects the top- _k_ nearest neighbors as demonstrations. Unlike _A-S (MMR)_ , which explicitly trades off relevance and diversity, _A-S (KNN)_ selects demonstrations based solely on similarity and does not encourage diversity among the chosen examples. (iii) _Q-S (MMR)_ , which applies MMR based solely on question similarity; and (iv) _Q-S (KNN)_ , which uses KNN based only on question similarity. Among these, _A-S (MMR)_ achieves the highest accuracy, outperforming both its KNN-based variant and the 

37 


![](P030_images/P030.pdf-0038-00.png)



![](P030_images/P030.pdf-0038-01.png)


Figure 18: Effect of the number Figure 17: Effect of in-context demonstration quantity on of demonstrations on FERA-Q perforFERA performance for differnt benchmarks. mance for MMLU-Pro and AQUA-RAT benchmarks. 


![](P030_images/P030.pdf-0038-03.png)



![](P030_images/P030.pdf-0038-04.png)


Figure 20: Effect of the number of clients on FERA-Q performance for MMLU-Pro and AQUA-RAT benchmarks. 

Figure 19: Effect of number of clients on FERA performance for different benchmarks. 

question-only baselines. This performance gain highlights the effectiveness of combining MMR’s relevance-diversity trade-off with the adaptive selector’s incorporation of broader contextual signals beyond simple question similarity. 

**Effect of Demonstration Quantity.** We investigate the impact of the number of context demonstrations on performance of FERA and FERA-Q by comparing setups with 1, 3, and 5 examples. As shown in Figure 17, 18 increasing the number of context examples improves the LLM’s understanding of the query, resulting in higher response accuracy, which will also lead to the better performance of FERA and FERA-Q. 

**Effect of Varying Client Numbers.** We investigate the impact of client population size by comparing the performance of FERA and FERA-Q under configurations with 3 and 5 clients. As shown in Figures 19 and 20, increasing the number of clients leads to a noticeable decline in performance. The primary cause is that, with a fixed-size dataset partitioned across more clients, each client receives fewer and less diverse demonstrations, which increases data heterogeneity across clients. This heightened heterogeneity leads to more divergent and conflicting reasoning paths for the same query, making server-side aggregation more challenging. 

Importantly, FERA does not require all clients to participate in every round. In large-scale scenarios, the server can select a subset of _L_<sup>_′_</sup> _< L_ clients per round, controlling the level of heterogeneity while still benefiting from distributed data. This partial participation strategy directly mitigates the performance degradation observed above, since fewer clients per round reduces conflicting reasoning paths while the iterative refinement process can still incorporate different clients across rounds. Combined with uncertainty-aware weighting, which naturally assigns lower influence to noisy or irrelevant clients, FERA’s architecture is compatible with larger federations without fundamental modifications. 

## **G Design Considerations for the Uncertainty Measure** 

In the federated reasoning setting, clients operate under strict privacy, computational, and communication constraints, which make many uncertainty-estimation techniques used in centralized LLM deployments impractical. Approaches such as semantic uncertainty, 

38 


![](P030_images/P030.pdf-0039-00.png)

### Figure analysis

Purpose: The figure compares two uncertainty-estimation methods—Token-Level and Semantic—across three clients, focusing on both uncertainty magnitude and computation time to justify the paper's choice of token-level entropy for FERA.

Layout and labels:
- The figure has two side-by-side bar-chart panels.
- Legend: teal bars represent **Token-Level** uncertainty; pink bars represent **Semantic** uncertainty.
- Left panel title: **Average Uncertainty per Client**.
  - x-axis: Client 0, Client 1, Client 2.
  - y-axis: Average Uncertainty.
- Right panel title: **Average Time Cost per Client**.
  - x-axis: Client 0, Client 1, Client 2.
  - y-axis: Average Time (s).
- No error bars or statistical intervals are shown.

Approximate visual readings:

| Panel | Client | Token-Level | Semantic |
|---|---:|---:|---:|
| Average uncertainty | Client 0 | ~0.30 | ~0.28 |
| Average uncertainty | Client 1 | ~0.32 | ~0.27 |
| Average uncertainty | Client 2 | ~0.38 | ~0.38 |
| Average time cost | Client 0 | ~14 s | ~70 s |
| Average time cost | Client 1 | ~13 s | ~68 s |
| Average time cost | Client 2 | ~12 s | ~67 s |

Direct observations:
- In the uncertainty panel, the two methods produce broadly similar values for all three clients.
- Token-level uncertainty is slightly higher than semantic uncertainty for Clients 0 and 1, while the two are nearly equal for Client 2.
- In the time-cost panel, semantic uncertainty is much slower than token-level uncertainty for every client.
- The time gap is large and consistent across clients, with semantic uncertainty visually around 4–5 times the token-level computation time.

Interpretation in relation to the paper text:
- The visual evidence supports the surrounding discussion that semantic uncertainty does not provide qualitatively different uncertainty signals compared with token-level entropy in this experiment.
- The much higher computation time for semantic uncertainty supports the paper's design argument that token-level entropy is more practical for federated reasoning under privacy, computation, and communication constraints.
- The figure reinforces the claim that token-level entropy is a lightweight, model-agnostic uncertainty measure suitable for FERA and FERA-Q.


Figure 21: Comparison of token-level and semantic uncertainty. **Left** : Average uncertainty values computed for ten sampled queries across three clients. **Right:** Average computation time per client. 

model-specific confidence scores, or auxiliary verifier–based methods generally require multiple forward passes, additional embedding or classifier modules, or model-dependent calibration procedures. These operations introduce substantial inference overhead, increase communication cost, and conflict with FERA’s training-free and model-agnostic design objectives. Token-level entropy, by contrast, offers a lightweight and consistent alternative. It is computed directly from the token-probability distributions already produced during decoding, requires no auxiliary components or calibration, and adds no additional computational or architectural assumptions for the client. 

To evaluate whether more complex alternatives offer meaningful advantages, we conducted a small comparative study. Ten questions were sampled from the server’s evaluation set, and for each of three clients we computed both token-level entropy and semantic-uncertainty scores, while also recording the computation time required for each method. The token-level uncertainty score is computed as described in Section E.5, and the semantic-uncertainty measure follows the formulation in Kuhn et al. (2023). The results, summarized in Figure 21, show that the two uncertainty measures are closely aligned in magnitude across all clients, indicating that semantic uncertainty does not yield qualitatively different signals. In contrast, its computational cost is substantially higher—typically 4–5× slower—due to additional encoding and comparison steps. These observations reinforce our design choice: token-level entropy provides a reliable, efficient, and privacy-compatible uncertainty signal that aligns with the constraints and objectives of federated reasoning systems like FERA. 

## **H Privacy Analysis of the FERA Framework Details** 

The main text analyzes FERA’s robustness against prompt extraction attacks. In this section, we present the GPT-4o prompt used for demonstration reconstruction, along with realworld cases illustrating how FERA responds under such attacks. The results are shown in Figure 22. 

To further assess concerns regarding client-side privacy, particularly whether clientgenerated responses may inadvertently disclose private information beyond the serverissued query, we conducted additional experiments on the MMLU-Pro benchmark. Specifically, we simulated a federated setup with three clients using LLaMA3-8B-Instruct under a Dirichlet partitioning scheme with concentration parameter _α_ = 10. We then analyzed the generated CoTs for the presence of personal identifiers. 

To quantify potential privacy leakage, we applied the “bert-base-NER” model (Devlin et al., 2019) to both the original server prompts and the client-generated reasoning response. Following the methodology of Edemacu & Wu (2025), we measured how often response contained personal identifiers not already present in the original prompts. The results, summarized in Table 2, show that only a small fraction of response included such identifiers, indicating that FERA poses minimal risk of unintended privacy leakage in this setting. 

39 


![](P030_images/P030.pdf-0040-00.png)

### Figure analysis

The figure supports the paper's privacy analysis by showing the prompt template used for reconstructing in-context-learning examples and the associated measured leakage rates for client-generated reasoning responses.

Key components directly visible:
- A teal-titled box labeled “GPT-4o Prompt for Reconstruct ICL Examples.”
- The box contains a chat-completion-style request with a system role describing a natural-language-generation and in-context-learning assistant.
- The user message asks the model to reconstruct five question–CoT-answer pairs that are topically and logically aligned with a provided query and final answer.
- Placeholder fields appear as `Question: XXXXX` and `Answer: XXXXX`, indicating that the concrete query and answer are inserted elsewhere.
- A small table beneath the prompt reports values by client and average.

Readable table values:

| Metric | Client 1 | Client 2 | Client 3 | Avg. |
|---|---:|---:|---:|---:|
| Value (%) | 0.031 | 0.049 | 0.051 | 0.043 |

Direct observations:
- Client 3 has the highest reported value at 0.051%.
- Client 1 has the lowest reported value at 0.031%.
- The average value is 0.043%.
- All reported percentages are very small.

Interpretation in context:
- The prompt box illustrates the reconstruction-attack setup discussed in the surrounding privacy-analysis section.
- The table corresponds to the paper’s claim that only a small fraction of client-generated reasoning responses contain personal identifiers not already present in server prompts.
- The low values visually support the authors’ conclusion that the framework exhibits minimal unintended privacy leakage in this evaluated setting.


Table 2: Fraction of client-generated reasoning response containing personal identifiers, as detected by the bert-base-NER model. 

## **I Case Study** 

In this section, we present real examples that illustrate how reasoning answers are updated across interaction rounds. These cases are shown in from Figure 23 to Figure 25. 

40 


![](P030_images/P030.pdf-0041-00.png)

### Figure analysis

The figure is a structured text panel used to illustrate the privacy analysis of the FERA framework under prompt/context reconstruction attacks.

- **Purpose:** It presents one server-issued math query, the corresponding client reasoning response, the client-provided context examples, and reconstructed context examples. This supports the surrounding discussion of whether client-side reasoning or context can leak private prompt information.
- **Top section — Server Query:** The server asks a word problem: Natalia sold 48 clips in April and half as many in May, asking for the total sold across both months.
- **Client Response:** The client explains that May sales are `48 / 2 = 24`, then adds April and May sales to obtain `48 + 24 = 72`. The final answer is explicitly given as **72**.
- **Client Provide Context Examples:** Three few-shot-style arithmetic examples are shown:
  - Q1 about Sally selling cracker boxes, with answer **60**.
  - Q2 about Ginger selling flowers, with answer **45**.
  - Q3 about Allison buying glue sticks and construction paper, with answer **28**.
- **Reconstruct Client Context Examples:** Three reconstructed examples are displayed:
  - Jason collects stamps in January and February, answer **108**.
  - Mia reads pages on Monday and Tuesday, answer **50**.
  - Liam gives away one-third of 60 marbles, answer **40**.

**Direct observations:** The reconstructed examples are simple arithmetic word problems similar in format and reasoning style to the provided context examples, but they do not visibly duplicate the exact original examples. Both original and reconstructed sections contain names and everyday scenarios, but the reconstructed names and quantities differ from the provided context examples.

**Interpretation in relation to the paper text:** In the privacy-analysis section, this figure appears to demonstrate that an attempted reconstruction can recover the general task pattern or reasoning format while not necessarily revealing the exact client-provided examples. This visually supports the paper's claim that FERA limits unintended privacy leakage during federated reasoning interactions.


Figure 22: Privacy Analysis 

41 

##### **Server Query1** 


![](P030_images/P030.pdf-0042-01.png)

### Figure analysis

**Purpose.** The figure presents a case-study trace of how a reasoning answer is updated across four interaction rounds for a word problem about saving for baseball supplies.

**Observed structure and labels.**
- A server query appears at the top: Gerald spends $100 per month on baseball supplies, his season is 4 months, he wants to save during months he is not playing, and he earns $10 per chore.
- The main body is organized into four vertically stacked sections labeled **Round1**, **Round2**, **Round3**, and **Round4** along the left side.
- Each round contains a written chain-of-thought-style solution and ends with a stated final answer.

**Panel/round observations.**
- **Round1:** Computes $100 / $10 = 10 chores per month and concludes the answer is **10**. Directly observed: this round treats the monthly supply cost as the monthly savings target.
- **Round2:** Treats the off-season as 8 months and computes $100 × 8 = $800, then $800 / $10 = 80 chores, concluding **80**. Directly observed: it reports total chores rather than a monthly average.
- **Round3:** Computes $100 × 4 = $400 and divides by $10 to obtain **40**, then states Gerald needs to average 40 chores per month. Directly observed: it uses the 4-month season cost but does not divide the saving burden over the off-season months.
- **Round4:** Computes the seasonal supply cost as $100 × 4 = $400, identifies 8 non-playing months, divides $400 / 8 = $50 per month, then divides $50 / $10 = 5 chores per month. It concludes the answer is **5**.

**Key comparison and interpretation.**
- Direct observation: the stated answers change across rounds as **10 → 80 → 40 → 5**.
- Interpretation: the final round resolves earlier mistakes by combining the season-long cost with the number of months available for saving, producing the most complete reasoning path.

**Connection to surrounding paper text.**
- The surrounding section describes case studies illustrating how reasoning answers are updated across interaction rounds. This figure serves as one such example, showing an iterative correction process in which the reasoning eventually aligns with the problem’s temporal structure and monthly averaging requirement.


Figure 23: Example Reasoning Answer iterative update for Query 1 

42 


![](P030_images/P030.pdf-0043-00.png)

### Figure analysis

Purpose: This figure presents a case study of how a reasoning answer changes across interaction rounds for a math word problem, illustrating the paper's discussion of iterative answer updates in the FERA framework.

Important components:
- Header: **Server Query2**.
- Query: Angela is a bike messenger in New York who needs to deliver 8 times as many packages as meals, with 27 meals and packages combined; the question asks how many meals she delivers.
- Three vertically stacked response blocks labeled **Round1**, **Round2**, and **Round3**.
- Each round contains a chain-of-thought-style algebraic solution.

Direct observations by round:
- **Round1:** Defines meals as `m` and packages as `p`, but writes `m = 8p`. This reverses the stated relationship. It solves `8p + p = 27`, obtains `p = 3`, then concludes `m = 24`, answering 24 meals.
- **Round2:** Uses variables `x` for meals and `y` for packages, again sets `x = 8y`, solves `9y = 27`, and concludes `x = 24`. This repeats the same relationship reversal and gives 24 meals.
- **Round3:** Defines `m` as meals and `p` as packages, writes the total as `m + p = 27`, and correctly represents the statement as `p = 8m`. It substitutes to get `m + 8m = 27`, solves `m = 3`, then finds `p = 24`, concluding Angela delivers 3 meals and 24 packages.

Key comparison:
- The first two rounds produce the same incorrect answer because they interpret “8 times as many packages as meals” as meals being 8 times packages.
- The third round corrects the variable relationship and reaches the mathematically consistent answer.

Interpretation:
- The visual example supports the surrounding case-study text by showing an iterative reasoning process in which later rounds can revise earlier flawed reasoning.
- It demonstrates that the update mechanism can move from a plausible but incorrect algebraic setup to a correct formulation and answer.


Figure 24: Example Reasoning Answer iterative update for Query 2 

43 


![](P030_images/P030.pdf-0044-00.png)

### Figure analysis

The figure presents a case-study trace of how a reasoning answer changes across interaction rounds for **Server Query3**. It is a structured text panel rather than a quantitative chart.

**Purpose and connection to the paper text:** The surrounding text states that Figures 23–25 show real examples of reasoning answers updated across rounds. This figure corresponds to Query 3 and illustrates how FERA-style iterative interaction can revise or stabilize chain-of-thought outputs over multiple rounds.

**Important components and information flow:**
- A yellow header labels the prompt as **Server Query3**.
- The pink prompt block asks a word problem about Sansa selling portraits: an 8-inch portrait costs **$5**, a 16-inch portrait costs **twice** that amount, and she sells **three 8-inch portraits** plus **five 16-inch portraits** per day; the question asks earnings every **3 days**.
- Three vertically labeled response blocks follow: **Round1**, **Round2**, and **Round3**.
- The information flow is top-to-bottom: original server query, then successive generated reasoning answers.

**Direct visual observations by round:**
- **Round1:** The reasoning correctly identifies the 16-inch portrait price as **$5 × 2 = $10**, computes daily earnings from 8-inch portraits as **3 × $5 = $15**, daily earnings from 16-inch portraits as **5 × $10 = $50**, and total daily earnings as **$65**. It then correctly computes **$65 × 3 = $195**, but the final sentence states **“The final answer is 210,”** which contradicts its own calculation.
- **Round2:** The response again states the prices and daily sales, including **$15** from 8-inch portraits and **$50** from 16-inch portraits, summing to **$65** daily earnings. However, the reasoning does not visibly complete the 3-day multiplication and ends with **“The final answer is 200,”** which is inconsistent with the preceding arithmetic.
- **Round3:** The response repeats the same core calculation: 16-inch portrait price **$10**, 8-inch revenue **$15**, 16-inch revenue **$50**, total daily revenue **$65**, and 3-day revenue **$65 × 3 = $195**. It concludes with **“The final answer is 195.”**

**Interpretation:** The displayed progression suggests that iterative rounds improve consistency between the arithmetic steps and the final answer. Earlier rounds contain final-answer errors despite mostly correct intermediate calculations, while the final round aligns the conclusion with the computed value of **$195**.


Figure 25: Example Reasoning Answer iterative update for Query 3 

44 

