# FEDERATION OVER TEXT: INSIGHT SHARING FOR MULTI-AGENT REASONING 

A PREPRINT 

**Dixi Yao**<sup>†*</sup> **Tahseen Rabbani**<sup>†</sup> **Manzil Zaheer**<sup>‡</sup> **Tian Li**<sup>†</sup> † University of Chicago ‡ Google DeepMind 

## **ABSTRACT** 

We propose a federated learning-like framework, _Federation over Text_ (FoT), that enables multiple clients solving different tasks to collectively generate a shared library of metacognitive insights by iteratively federating their local reasoning processes without sharing actual problem instances or task instructions. Instead of federation over gradients (e.g., as in distributed training), FoT operates at the **semantic level** without any gradient optimization or supervision signal. Iteratively, each client runs an LLM agent that does local thinking and self-improvement on their specific tasks independently, and shares reasoning traces with a central server, which aggregates and distills them into a cross-task (and cross-domain) _insight library_ that existing and future agents can leverage to improve performance on related tasks. Experiments show that FoT improves reasoning effectiveness and efficiency across a wide range of challenging applications, including mathematical problem solving, cross-domain collaboration, real-world daily tasks, and machine learning research insight discovery. Specifically, it improves average performance scores by 25% while reducing the reasoning tokens by 4% across the first three applications. In the research insight discovery application, FoT is able to generate insights that cover over 80% of the major contributions in the subsequent papers. 

## **1 Introduction** 

LLM-powered agents are increasingly deployed for complex, multi-step tasks [e.g., 1, 2, 3, 4, 5, 6]. However, they can suffer from two major limitations. First, reasoning can be inefficient: agents often reason from scratch given an input instance, repeatedly solving similar problems, which can be computationally expensive and slow. Second, reasoning in multi-agent systems typically occurs in an isolated manner, where agents are chained by passing prompts or intermediate outputs [e.g., 7]. While agents exchange task solutions within a session, their internal thinking processes and full reasoning histories are not explicitly stored or communicated. As a result, these hard-won thinking processes are lost and cannot be reused or shared across agents. 

It remains underexplored how to automatically transfer, reuse, or distill independent reasoning traces to help guide and improve future reasoning processes for similar agents or across domains. At the same time, classical distributed or federated paradigms for knowledge sharing [8] may not be suitable for learning generalizable insights from agents’ reasoning traces. Averaging the gradients or weights of entire (or part of) large generative models can be computationally prohibitive, impossible for closed-source LLMs, and more importantly, not interpretable as parameter aggregation is not explicitly equivalent to sharing _abstract, high-level reasoning summaries_ . 

To this end, we propose _federation over text_ (FoT), a federated-like framework that enables a set of agents to collaboratively and iteratively build a shared, evolving library of reusable _insights_ from independent local reasoning traces (expressed in natural language) without communicating actual problem instances. Unlike traditional multiagent systems that decompose a single complex task into subtasks, FoT operates across multiple independent agents over diverse but related tasks. Each agent solves some task with a base language model, and our goal is to generate an insight library—a high-level aggregation of the common principles and ideas shared across the agents’ tasks. 

Unlike traditional distributed learning, which averages gradients or model updates in a high-dimensional, uninterpretable space, FoT operates at the **semantic** , text level without any parameter optimization, fine-tuning, or reinforce- 

- _∗_ Correspondence to: Dixi Yao _<_ dixi@uchicago.edu _>_ 

Federation over Text: Insight Sharing for Multi-Agent Reasoning 

A PREPRINT 

ment learning. In particular, at each round, agents transmit concise metacognitive summaries of their problem-solving processes to a central server (which can be physical or logically virtual). The server, acting as an aggregator, identifies and distills recurring reasoning fragments from these summaries into new, explicit insights and sends the insight library back to the agents for the next round. We note that FoT is a _general_ framework that allows each agent to use any local reasoning model combined with any local self-improvement workflows for their individual tasks, as long as summarized reasoning traces are shared at each iteration. Meanwhile, we note that our proposed FoT approach is analogous to the classic federated/distributed learning setting, where these two regimes can be interpreted within the same conceptual framework (side-by-side comparisons in Table 1). Additionally, FoT offers similar benefits as FL in that only abstracted reasoning traces are shared instead of raw problem instances. But operating in the semantic text space as in FoT provides more interpretable control on what information is transmitted, and allows us to identify and block sensitive information more easily. 

We apply FoT to various applications including mathematical problem solving, multi-domain collaboration (scientific question-answering, coding, and Humanity’s Last Exam), real-world daily tasks, and research insight discovery (Section 4). We compare our framework with a range of baselines, such as isolated reasoning without collaboration and other forms of cross-agent knowledge sharing. Across the first three applications with previous benchmarks, FoT improves the accuracy performance score by 25% on average while reducing the reasoning tokens by 4%. For the research insight discovery application, we demonstrate that an insight library learned from ICLR papers in one year can cover the core technical contributions of over 80% of accepted papers in the next year. FoT enables LLM-based systems to function not only as performance-driven solvers, but also as tools for decision support and insight discovery. 

## **2 Related Work** 

**Multi-Agent Collaboration.** Extensive prior multi-agent works focus on enabling agents to _solve a given complicated task_ in a collaborative way. A common paradigm involves decomposing a task into smaller subtasks, assigning each to an individual agent, and aggregating the partial results [e.g., 9, 10, 11, 12, 13]. Other existing approaches include multi-agent debate [2] or allowing multiple agents to repeatedly perform the same task and vote on a solution [14, 15, 16]. Previous works also study large-scale agentic knowledge exchange by building concrete workflows for agent laboratories [4], or simulating research communities [5, 17]. Rather than using multiple agents to handle different components of a single task or building end-to-end workflows to simulate complicated systems, in FoT, each client runs a local agent that solves problems independently and the server aggregates reasoning traces from the problemsolving processes to distill shared insights (Figure 1). 

**Collaborative and Federated Learning.** Collaborative or federated learning (FL) [8] aggregates model parameters from multiple clients while keeping data local. Existing literature on federated agents primarily focuses on training language models in the classical parameter or gradient-level aggregation framework [18], which can be expensive and insufficient for capturing high-level abstract reasoning strategies. Social learning [19] allows teacher agents to generate synthetic examples or abstract prompts that are aggregated to train a student model in a single-task setting. FL and FoT share interesting connections (Section 3.1); FoT operates in the semantic space while being compatible with heterogeneous agent models and task domains. 

**LLM Skills and Recursive Self-Improvement.** To embed past experience into LLM-based agents, existing approaches such as Anthropic Skills [20], Agents.md<sup>2</sup> , vibe research [6], and Scientific Skills [21] focus on providing concrete skills for executing specific tasks rather than generalizable, abstract insights. Moreover, they require some extent of human-guided process to generate skills, whereas FoT generates reusable insights automatically without any human intervention; even labels indicating whether an answer is correct are not required. ExpeL [22] stores an agent’s past successful trajectories along with reflections on successes and failures, relying on explicit labeling. There is also extensive research on improving agent reasoning through self-reflection, self-improvement, or context engineering [1, 23, 24, 25, 26, 27, 28, 29, 30]. However, they do not consider jointly learning insights by distilling reasoning traces across independent agents solving _different_ , but related tasks. Moreover, FoT can adopt any existing self-improvement method as the local thinking approach (Section 6.1) and aggregate their traces to iteratively form generalizable insights. 

Another line of work on agent improvement requires gradient optimization via various forms of fine-tuning or reinforcement learning [31, 32]. FoT operates purely on the inference level without any fine-tuning or complicated supervision. In addition, these approaches are mainly designed for solving a single task and do not consider federation. Hence, in this paper, we only compare with methods that only involve API access without computing gradients. 

> 2 `https://agents.md/` 

2 

Federation over Text: Insight Sharing for Multi-Agent Reasoning 

A PREPRINT 

## **3 Federation over Text** 

In this section, we propose our federation over text framework and discuss its connections with federated learning (i.e., gradient aggregation) [8]. Federated learning (FL) focuses on training a shared global model to serve existing and future clients, whereas FoT aims to build an insight library that helps both existing and new agents to better solve a variety of tasks. In the most common FL workflow, the server broadcasts the current global model to each client, who then performs local training on their local data and transmits the local model updates back to the server. The server aggregates the model updates to form a new global model. This iterative process repeats until convergence. At a high level, in FoT, at each round, each client runs a local agent (any base LLM(s)) who solves its local task with the help of the current insight library, and sends the reasoning traces to the server. The server merges them to update the library and distributes it to all agents for the next round. We present the overall workflow of FL and FoT in Figure 1, as well as the pseudocode of both algorithms in Appendix B. 


![](P067_images/P067.pdf-0003-04.png)

### Figure analysis

The figure is a two-panel conceptual workflow diagram comparing conventional federated learning with the paper's proposed Federation over Text (FoT) framework.

**Left panel: Federation over Gradients**

- Labeled output: **Output: global model**.
- Central component: a **Server** connected by arrows to multiple **Clients**.
- Client-side elements are represented by small database-like stacks and boxes labeled **Clients**, with an ellipsis indicating additional clients.
- The numbered information flow is:
  1. **Broadcast global model** from the server to clients.
  2. **Local optimization** performed by each client.
  3. **Upload model weights** from clients back to the server.
  4. **Aggregate model weights to update the model** at the server.
- Direct observation: this panel emphasizes parameter/model-weight communication and aggregation.

**Right panel: Federation over Text**

- Labeled output: **Output: insight library**.
- Central component: a **Server** connected to multiple **Agents**.
- Agent-side elements mirror the left panel visually, with boxes labeled **Agents** and an ellipsis indicating many decentralized agents.
- The numbered information flow is:
  1. **Broadcast insight library** from the server to agents.
  2. **Local reasoning and self-reflection** performed by each agent.
  3. **Upload reasoning traces** from agents to the server.
  4. **Aggregate traces to update the library** at the server.
- Direct observation: this panel replaces local optimization with reasoning/self-reflection and replaces model-weight uploads with reasoning-trace uploads.

**Comparison and interpretation**

- The diagram visually aligns the two workflows step-by-step, showing FoT as an inference-level analogue of federated learning.
- In the gradient-based workflow, the shared artifact is a **global model** updated through aggregated model weights.
- In the text-based workflow, the shared artifact is an **insight library** updated through aggregated reasoning traces.
- The surrounding text explains that FoT does not require gradient optimization or fine-tuning; instead, agents solve local tasks, summarize reusable reasoning skills, and send these traces to a server for clustering, merging, and redistribution.
- The figure supports the paper's framing that FoT is structurally similar to federated learning but operates over human-readable reasoning artifacts rather than numerical parameter updates.


Figure 1: Workflow of federation over (accumulated) gradients and federation over text. See pseudocode in Algorithms 1 and 2 in the appendix. 

In the workflow of FoT (the right subfigure of Figure 1), each of the (potentially many) decentralized agents solves a specific problem or task, using a selected base LLM. These tasks can span different domains such as mathematical reasoning, coding, and scientific question-answering. Given a task (e.g., a collection of math questions), an agent first solves the task (e.g., generates solutions), then reflects on whether the reasoning process contains reusable techniques and what key skills can be extracted. Instead of uploading complete, raw reasoning histories, each agent generates a logic-level _reasoning trace_ for each problem based on its solution and reflections, specifying when and how to apply the extracted skills via step-by-step instructions. Agents then share these shorter, summarized messages with the server, while keeping problem instances and raw histories local. 

In each round, after collecting traces, the server needs to aggregate them to update the insight library. We develop one specific aggregation technique that distills high-level insights rather than simply concatenating reasoning traces. In particular, the server first clusters reasoning traces that share similar skills, and then uncovers connections among traces that solve the same problem using different skills and can potentially be merged. Finally, the server broadcasts the updated insights library to all agents for the next iteration. The aggregated library can be re-used as an external reference to improve the reasoning of either existing agents or future agents that are not in the current network. Unlike parameter updates, the resulting knowledge is human-readable and interpretable. This improves transparency and enables cross-domain transfer of reasoning strategies. We provide all the designed prompts that we use in Appendix G. 

**Local Reasoning and Global Aggregation Strategies.** We note that many self-improvement methods proposed by prior works [e.g., 1, 23, 24, 25, 26] can be plugged into FoT to generate the reasoning traces sent to the server. In our experiments (Section 6.1), we plug several different local thinking methods into FoT. We also enable calling external tools (Section 4.3). Additionally, we note that while we currently use curated prompts to perform global aggregation in the text space (Appendix G), the aggregation step of FoT can adopt other techniques developed for general context compression [33, 34] (Section 6.2). FoT is modular in that local or global procedures can adapt various algorithms/prompts, and be handled via heterogeneous LLM models (Section 6). 

### **3.1 Analogies Between Federated/Distributed Learning and FoT** 

We reiterate that there are rich connections between FL and FoT. In particular, in Table 1, we summarize how their algorithmic components can be mapped between each other. For instance, in FL, clients may adopt different optimization methods to solve local subproblems. Analogously, in FoT, each agent may leverage distinct local reasoning strategies and prompt designs to generate traces. 

Inspired by techniques from distributed or federated learning, FoT allows for an interesting design space to improve efficiency and effectiveness of multi-agent collaborative reasoning (Section 4). It is worth continuing to explore the design space of FoT, such as personalization strategies and handling other forms of distribution drifts across agents, which we leave for future work. 

3 

Federation over Text: Insight Sharing for Multi-Agent Reasoning 

A PREPRINT 

Table 1: Connections between Federated Learning over Gradients and Federation over Text (FoT). 

|**Components**|**Federation over Gradients**|**Federation over Text(FoT)**|
|---|---|---|
|Learning Objective|Learn a global model that generalizes to test data<br>or new clients|Learn an insight library that improves the reason-<br>ing of agents|
|Learning Work|Local training via_any_optimization method|Local task solving via _any_ self-improvement ap-<br>proach|
|Data Minimization|Share model updates rather than raw data|Share abstracted reasoning traces rather than raw<br>instances|
|Local_→_Server|Clients upload model weights or gradients|Agents upload reasoning traces from problem-<br>solving|
|Server Aggregation|Averaging over model weights or gradients|Aggregating over reasoning traces (text) using cu-<br>rated prompts|
|Server_→_Local|Current learnt global model|Current curated insight library|
|Personalization|Maintaining personalized local models|Addressing diverse local tasks across different do-<br>mains.|



## **4 Applications of FoT** 

In this section, we study four applications demonstrating how FoT enhances reasoning performance and efficiency, including mathematical problem-solving with varying levels of difficulty (Section 4.1), cross-domain collaboration involving math, scientific QA, coding, and others (Section 4.2), real-world daily tasks (Section 4.3), and ML research insight discovery (Section 4.4). Our code and experiments are open sourced at `https://github.com/dixiyao/FoT` . 

### **4.1 Mathematical Problem Solving** 

In this application, the agents’ goal is to solve math problems. There are eight agents, each working on one of eight datasets with varying levels of difficulty, AIME24 [35], AIME25 [36], AMC, CCEE, CNMO, WLPMC, V202412 Hard, and V202505 Hard from LiveMathBench [37]. We experiment with DeepSeek-R1-Distill-Qwen-7B and Gemini-3.0-Pro as two choices of the base LLM. 

Figure 2 shows the results averaged on eight benchmarks. Numbers on each benchmark are in Appendix D.1. FoT can help reduce loops (i.e., the number of times repeated sentences are generated during the reasoning process). With the presence of an insight library, agents generate fewer tokens while achieving better final performance. Additionally, FoT reduces the number of loops, indicating less repeated reasoning content. Note that our insight library size is manageable, which is helpful for communication efficiency and reducing the context length for LLMs. For DeepSeek, by Round 3, we generate 249 reasoning traces in total (33K tokens) and aggregate them into 11 insights (3K tokens). For Gemini 3.0 Pro, we generate 549 traces (53K tokens) and aggregate them into 37 insights (12K tokens). The cost of uploading reasoning traces and downloading insights is moderate, yielding substantial improvements in utilities. We study the effects of insight library size in Section 6.4. 


![](P067_images/P067.pdf-0004-09.png)


Figure 2: Comparison of reasoning accuracies and efficiency (measured by average number of reasoning tokens and total loops), averaged over eight math benchmarks. 

### **4.2 Multi-Domain Collaboration** 

In this section, we go a step further to understand how FoT can retrieve cross-domain knowledge, helping agents working on different but related domain tasks collaborate and improve each other’s reasoning. We _first_ choose AIME24 and AIME25 for math tasks, GPQA and GPQA-diamond [39] for scientific question-answering (QA) tasks, and LiveCodeBench (version 6, Hard) [40] for coding. At first glance, these three domains appear loosely related. However, apart from the performance improvement demonstrated in Figure 3, FoT generates insights that highlight underlying conceptual similarities across multiple domains. We let each agent mark which insights contribute most to the reasoning process. In Appendix D.2, we present **two case studies** illustrating the content of insights, which insights are used, and how they are applied during the reasoning process to arrive at correct solutions. These examples show that insights from one domain (e.g., math, Sudoku) can be used to correct the reasoning processes of tasks in a different domain 

4 

Federation over Text: Insight Sharing for Multi-Agent Reasoning 

A PREPRINT 


![](P067_images/P067.pdf-0005-02.png)


Figure 3: Accuracies and average number of generated tokens during the reasoning process across math, scientific QA, and coding benchmarks. Round 1 represents isolated agents. Insight libraries improve reasoning across domains while reducing token usage. 

Figure 4: Comparisons of the true-thinking score (TTS) [38], measuring reasoning steps whose removal would lead the agent to a different answer. FoT exhibits fewer decorative reasoning steps. 

(e.g., chemistry). _Second_ , we also experiment with cross-domain collaboration on more challenging benchmarks, including Humanity’s Last Exam [41], and show that even when most reasoning traces originate from incorrect answers, the insight library can still improve overall performance (Table 9). From Figure 3, we can also observe diminishing gains after round 3, suggesting convergence of the insight library. 

**True-Thinking Abilities.** To see how FoT can also reduce decorative reasoning, we report the ‘true-thinking score’ [38] in the multi-domain collaboration application. The true-thinking score (TTS) measures the proportion of reasoning steps whose removal would lead the agent to a different answer, thus serving as a proxy metric of effective reasoning. From Figure 4, we can see that FoT increases the score compared with the baseline, indicating that insights generated by FoT can help agents skip redundant reasoning steps. 

### **4.3 Real-World Daily Tasks** 

Table 2: Performance scores (pass@1) and efficiency when isolated OpenClaw agents and FoT resolve all tasks in PinchBench. FoT can greatly improve accuracy and reduce the number of generation tokens. In Appendix D.3.1, we further show that the additional token cost incurred by local reasoning trace generation and insight library construction is acceptable. 

|LLM<br>|Algorithms|Scor|e (out of|100)|Execu|tion Ti|me (s)|# Gen|eration T|okens (K)|
|---|---|---|---|---|---|---|---|---|---|---|
|(Thinking Level)|||||||||||
|||Max|Avg|Min|Max|Avg|Min|Max|Avg|Min|
|Gemini 2.5|Isolated Agents|27.90|20.12|12.70|**2932**|**2835**|**2157**|57|55|54|
|Flash Lite|FoT (Round 2)|**53.29**|**52.11**|**50.36**|3667|3466|3223|57|**54**|**52**|
|Gemini 31 Pro|Isolated Agents|79.97|72.67|59.57|3174|3093|2967|**46**|44|40|
|.<br>(Low)|FoT (Round 2)|**86.88**|76.46|65.09|**2808**|**2528**|**1940**|48|45|40|
||FoT (Round 3)|86.59|**80.44**|**76.13**|3080|2797|2553|47|44|42|
|Gii 31 P|Isolated Agents|89.06|77.64|60.36|2168|1893|1714|47|41|**33**|
|emn . ro<br>Mdi|FoT (Round 2)|86.48|81.04|77.07|1984|1789|1664|**44**|**38**|42|
|(eum)|FoT (Round 3)|**89.51**|**81.85**|**77.38**|**1889**|**1711**|**1568**|45|43|42|
|Gemini 31 Pro|Isolated Agents|80.50|76.29|72.21|1864|**1764**|1683|53|50|46|
|.<br>(Hih)|FoT (Round 2)|**87.32**|84.82|81.71|**1845**|1787|**1658**|52|48|46|
|g|FoT (Round 3)|87.14|**85.00**|**82.11**|2091|1962|1771|**48**|**47**|**44**|



In this application, FoT positions agents as tools for decision support in daily work tasks. We use OpenClaw [42], experimenting with both Gemini 3.1 Pro and Gemini 2.5 Flash Lite as backend models. We evaluate on PinchBench [43], which covers tasks such as web research and stock analysis. Each OpenClaw agent is assigned to one task and produces reasoning traces from its execution trajectory. FoT aggregates these traces into a shared insight library, `insight.md` , which agents then use alongside pre-defined tools and skills to complete tasks. We compare with three **additional baselines** where we (1) append all agent trajectories into a retrieval-augmented generation (RAG) datastore for each agent, or (2) equip each agent with 52 pre-defined OpenClaw skills. Agents perform independent reasoning in both cases. (3) ExpeL [22]. We repeat all experiments five times and report both average and best-case performance. 

We report core results in Table 2 across high, medium, and low thinking levels. At the high-thinking level, OpenClaw agents using the insight library achieve an average accuracy that exceeds even the best isolated-agent accuracy. The insight library can also lower overall token consumption in the Gemini 3.1 Pro (High) and Gemini 2.5 Flash Lite experiments. Similar to the transferability experiments in Section 4.1, FoT enables medium- and low-thinking agents to reach performance comparable to isolated agents at high and medium thinking levels, respectively. In the Gemini 

5 

Federation over Text: Insight Sharing for Multi-Agent Reasoning 

A PREPRINT 

2.5 experiments, most of the traces come from faulty reasoning, yet FoT is not misled and still achieves accuracy above 50%, demonstrating robustness to noisy traces. Results of comparing with two additional enhanced isolated reasoning baselines and ExpeL [22] are in Appendix D.3.2, where we again observe the significant superiority of FoT, especially when solving cross-domain tasks. 

Since these tasks involve multi-round interactions and tool use rather than simple answer generation, we also measure wall-clock execution time, defined as the time from sending a query to the agent until task completion, including tool execution. We observe that latency decreases when the thinking level is increased from low to high, even though higher thinking levels generate more tokens due to more efficient calling of suitable tools. More details and two concrete examples to illustrate how agents with and without the library handle these cases are in Appendix D.3.3. 

### **4.4 Research Insight Discovery** 

We demonstrate that with FoT, agents collectively extract and synthesize insights across diverse areas of machine learning research. This differs from work on end-to-end agentic workflows that execute the full scientific pipeline and generate submission-ready papers [3, 4, 44, 45, 46, 13, 47], which is not what we focus on here. In our setting, each agent is assigned one or more papers to read and identify research questions. FoT then curates an insight library of actionable and generalizable research insights. We evaluate how many future papers could have been guided by these insights as core contributions, using four criteria: concrete methodological usage, how the method is presented, whether the paper’s core contribution would fundamentally change without the insight, and whether the insight is novel; see Prompt 6 in the appendix. Note that methods requiring explicit labeling cannot handle such applications, as there is no explicit success signal for reading papers. 

We consider two settings depending on whether the base LLM may have seen the evaluation papers during pretraining. In Setting 1, 1574 agents each read one accepted ICLR 2023 paper, and we evaluate on accepted ICLR 2024 papers using Gemini 3.0 Pro<sup>3</sup> for all agents and the server. Since this model may already contain knowledge of ICLR 2024 papers, Setting 2 uses Gemini 2.0 Flash<sup>4</sup> to read ICLR 2024 papers, and we evaluate on ICLR 2025 papers. Gemini 2.0 Flash has no access to 2025 papers because its cutoff date is before the ICLR 2025 submission deadline. 

We compare against two baselines. First, we query a standalone Gemini model to generate the top 200 insights using ICLR keywords and the same insight definition, then evaluate whether these insights guide papers in the following year. Second, we use retrieval-augmented generation (RAG) [48] to build a datastore of all selected papers from the previous year and ask the LLM to generate the top 200 insights using retrieved content as reference. These baselines test whether FoT improves insight discovery beyond the LLM’s standalone capability and simple retrieval over prior papers. By default, we use Gemini 3.0 Pro as judge and report results in Table 3. We further cross-validate with Gemini 2.5 Flash Lite, DeepSeek-R1-Distill-Qwen-7B, and Qwen2.5-7B-Instruct in Appendix D.4.1. FoT insights achieve the highest guidance rate across evaluations by all four models. For instance, when evaluated by Gemini 2.5 Flash Lite, directly prompting Gemini 3.0 Pro guides only 2.2% of ICLR 2024 papers, whereas FoT insights guide 70.6%. In addition to LLM-based judging, we manually verify the generated insights and provide a subset in Appendix H.1. 

Table 3: Percentage of papers guided by insights generated from different models. FoT improves overall guidance rate over the baseline of independently solving tasks without the library (‘Isolated Agents’) and the baseline that simply stores previous tasks in RAG for retrieval (‘RAG’). 

|**Setting**|**Model**|**Isol**|**ated A**|**gents (Gem**|**ini)**|**RAG**|**(Gemi**|**ni + All Pap**|**ers)**|**FoT (G**|**emini**|**+ Insight L**|**ibrary)**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|||Overall|Oral|Spotlight|Poster|Overall|Oral|Spotlight|Poster|Overall|Oral|Spotlight|Poster|
|1 (23_→_24)|Gemini 3.0 Pro|41.3|**70.9**|**73.8**|33.3|66.5|58.1|69.2|66.4|**67.4**|67.4|68.7|**67.2**|
|2 (24_→_25)|Gemini 2.0 Flash|0.7|0.5|0.8|0.7|77.4|63.4|67.4|79.6|**82.4**|**82.2**|**82.1**|**82.4**|



A potential concern with centralized agentic systems, such as server-deployed auto-research agents, is that they may require access to full research papers. For unpublished or unlicensed papers, such sharing can raise intellectual property concerns. In contrast, FoT uploads only abstract metacognitive summaries, as illustrated in Appendix H.3, without exposing paper details or sensitive experimental data (Section 5). This design allows users to leverage local agentic assistants while still benefiting from global insights produced by the server. The shared insight library further supports iterative improvement, helping both agents and humans refine ideas and develop future research. 

## **5 Properties of FoT** 

**Transferability Across New Models and Tasks.** We investigate whether (1) the insight library curated by one LLM model is compatible with a different model for reasoning, and (2) whether the library curated in one application can 

> 3We use the checkpoint gemini-3.0-pro-preview released on November 18, 2025. 

> 4We use the checkpoint gemini-2.0-flash-001 released on April 9, 2025. 

6 

Federation over Text: Insight Sharing for Multi-Agent Reasoning 

A PREPRINT 

be transferred to new, unseen tasks. Table 4 demonstrates that FoT allows for the decoupling of the base LLMs for actual reasoning and the models for building the shared insight library. Moreover, we observe that an insight library generated by a weaker model (DeepSeek) can supervise and improve the performance of stronger ones (Gemini 3.0 Pro) (last two rows of Table 4). This indicates that a variant of ‘weak-to-strong generalization’ can happen in the text space, beyond the gradient space studied in prior works [e.g., 49]. 

Table 4: Evaluation of decoupling insight library models and reasoning models on math problem-solving. Insights produced by stronger models (Gemini 3.0 Pro) consistently benefit weaker agents (DeepSeek), while libraries from weaker agents can also improve stronger ones. 

|**Reasoning Model**|**Insight Library Model**|**Avg**<br>|# Output Tokens|# Loops|
|---|---|---|---|---|
|Isolated DeepSeek|N/A|0.537|6312|7|
|DeepSeek|Gemini 3.0 Pro|**0.625**|**4317**|**4**|
|Isolated Gemini 3.0 Pro|N/A|0.846|891|3|
|Gemini 3.0 Pro|DeepSeek|**0.902**|**745**|**0**|



We further investigate how the insight library generalizes to unseen tasks that are not involved in the library construction process. For mathematical problems and multi-domain collaboration benchmarks, we split the tasks into two disjoint halves: one half is used for insight library construction, while the other half is reserved exclusively for evaluating the library. For real-world daily tasks, we use the old 23 tasks from the evolving PinchBench V1 for insight library construction, and evaluate generalization on the newly introduced 124 tasks spanning 53 categories in PinchBench V2. Same as the previous settings, we conduct mathematical problem solving and multi-domain collaboration experiments using 3 different random seeds, and evaluate real-world daily tasks using 5 different random seeds. 

Table 5: Average accuracies across different tasks and experimental settings on existing and new, unseen tasks. For FoT, agents utilize the shared insight library for both sets of problems, whereas the isolated reasoning agents perform inference independently without access to any shared library. 

|||**Mathe**<br>**Problem**|**matical**<br>**Solving**|**Multi-Domain**<br>**Collaboration**|**Real-**<br>**Daily**|**World**<br>**Tasks**|
|---|---|---|---|---|---|---|
||**Algorithm**|Gemini 3.1<br>Pro|Gemini 2.5<br>Flash Lite|Gemini 2.5<br>Flash Lite|Gemini 3.1<br>Pro|Gemini 2.5<br>Flash Lite|
|**Eii Pbl**|<sup>Isolated Agents</sup>|88.50_±_1.80|88.24_±_3.51|82.36_±_1.88|76.29_±_3.39|20.12_±_6.21|
|**xstng roems**|<br>FoT|90.10_±_0.89|90.12_±_2.00|85.00_±_0.60|84.82_±_2.33|52.11_±_1.26|
|**N Pbl**|Isolated Agents|89.13_±_2.19|87.33_±_1.64|84.96_±_1.53|85.03_±_1.51|34.60_±_1.42|
|**ew roems**|FoT|89.66_±_1.22|89.94_±_0.81|86.60_±_0.29|86.67_±_1.05|36.67_±_0.82|



We observe that FoT achieves the largest performance gains during test-time learning, while still maintaining consistent improvements on unseen tasks. This demonstrates that the insight library can continuously benefit newly introduced agents, enabling knowledge transfer and generalization beyond the tasks used during library construction. Complete results on each benchmark are in Appendix E.1. In Appendix E.1, we also verify that new agents on unseen tasks in Claw-Eval [50] (199 agents) can benefit from an insight library generated on PinchBench (23 agents). The library transfers effectively across agents and tasks, improving performance while reducing token usage. 

**Safeguarding Raw Problem Instances.** In addition to improving reasoning effectiveness and efficiency, FoT brings about the side benefit of safeguarding raw problem instances. _First_ , we observe that the uploaded abstracted reasoning traces do not contain original problem or task descriptions. We employ a strong multi-turn prompt-stealing attacker [51] to reconstruct the agent input from given reasoning traces. The token-level F1 scores between the reconstructed and original inputs are smaller than 0.25. Also, no personal identifiable information (PII) is leaked. _Second_ , we verify that the insight library does not contain answers to the questions, preventing agents from directly retrieving answers via shortcuts. Using shingle intersection and a strict 4-gram matching, we compute Jaccard similarity between the insight library and ground-truth answers, as well as between reasoning traces and input questions. We observe near- **zero** similarity. Full details and quantitative results are provided in Appendix E.2. 

## **6 Ablation Studies** 

In this section, we empirically study the effects of key FoT parameters. Sections 6.1 to 6.3 examine the impacts of varying local reasoning strategies, server aggregation strategies, and heterogeneous base LLM models, respectively. We further study FoT performance under different library sizes (Section 6.4) and different agent participation scenarios (Section 6.5). 

7 

Federation over Text: Insight Sharing for Multi-Agent Reasoning 

A PREPRINT 

### **6.1 Effects of Local Reasoning Strategies** 

In this section, we conduct ablations to (1) examine how our reasoning trace extraction differs from existing mechanisms, and (2) verify that FoT is flexible and supports a variety of local reasoning and self-improvement approaches. We compare with the original prompts (Appendix G.3) in work of Didolkar et al. [23], which we adapt from, and other agent reasoning and self-improvement approaches such as Agentic Context Engineering (ACE) [26], HyperAgents [25], and Evolving Prompt [28]. A subset of core results are reported in Table 6 and detailed implementation and full results on more applications are provided in Appendix F.1. 

Table 6: Average accuracies of using different local reasoning strategies in each algorithm in math problem solving tasks (LiveMathBench). 

|**Base Models **|**Algorithms**|**Local Reasoning**|**Avg Acc.**|
|---|---|---|---|
|DeepSeek-<br>R1-Distill-|Isolated Agents <br>FoT|plain inference<br>Ours (Prompts 2-3)|0.537<br>**0.553**|
|Qwen-7B|Isolated Agents <br>FoT|Metacognitive Reuse [23]|0.464<br>**0.595**|
||Isolated Agents|plain inference|0.846|
||FoT|Ours (Prompts 2-3)|**0.928**|
||Isolated Agents|Metaconitive Reuse [23]|0.850|
|Gmini 30|<br>FoT|g|**0.905**|
|e .<br>|Isolated Agents|HAt 25|0.850|
|Pro|<br>FoT|ypergens []|**0.912**|
||Isolated Agents|ACE 26|0.375|
||<br>FoT|[]|**0.502**|
||Isolated Agents|Eli Pt [28]|0.370|
||<br>FoT|vovng romps|**0.451**|



We see that FoT with different local reasoning methods can improve over their ‘Isolated Agents’ baseline where each agent solves tasks using the corresponding reasoning method separately. Using our designed prompts improves over variants with other local reasoning methods in most cases, yielding an average +8.1% accuracy gain, along with fewer generated tokens and reasoning loops (Appendix F.1). FoT with HyperAgents as the local reasoning method serves as a strong alternative in some cases. A potential concern with HyperAgents is that uploading evolved prompts may introduce privacy risks, as these prompts can contain descriptions of the underlying questions. 

### **6.2 Effects of Global Aggregation Strategies** 

We demonstrate that FoT is flexible to support different global aggregation algorithms on the server side. In particular, we evaluate the baseline of simply appending the shared traces, and other context compression techniques, including Chain-of-Density (CoD) [33] and Context Compaction from Claude Cookbook [34] (denoted as ‘Compaction’). For all three baselines, we vary the corresponding compression ratio parameters to illustrate the tradeoffs between task performance (accuracies or research idea guidance rate) and efficiency (number of reasoning tokens as well as library sizes). 


![](P067_images/P067.pdf-0008-09.png)


Figure 5: Accuracy and number of output tokens using different server-side algorithms on LiveMathBench. FoT achieves the highest accuracy with a moderate number of tokens, providing a good trade-off between accuracy and efficiency. 

Figure 6: Percentage of papers guided by insights using different server-side aggregation. FoT generates a reasonablysized library guiding most papers. General context compression methods might not be the most suitable for the task. 

We see that on math problem-solving, simply concatenating all traces results in the worst accuracy. Even when the total tokens remain within the context window, long prompts can still lead to ‘context loss’, observed by previous 

8 

Federation over Text: Insight Sharing for Multi-Agent Reasoning 

A PREPRINT 

works [e.g., 52]. Varying the percentage of traces to append (75% and 50% randomly picked) does not help much. CoD and Compaction (plugged into FoT) can be effective and yield performance gains over the independent reasoning baselines, although the accuracy improvement is smaller than that achieved by our proposed prompts. In the ML insight discovery task (Figure 6), we observe that CoD adopts an aggressive context compression strategy and thus produces far fewer tokens. However, the generated insights are not sufficiently satisfactory. For Compaction, the guidance rate increases as the library size increases, but achieving a good guidance rate requires a large number of tokens. FoT with our designed aggregation captures shared patterns without over-generalizing and produces more meaningful insights at a modest size. 

### **6.3 Effects of Heterogeneous Local and Server Agent Models** 

We further demonstrate the flexibility of FoT in how it is compatible with different agent models deployed on the local clients or the server. Full results are provided in Appendix F.2. On math problem solving, with Gemini 3.0 Pro as local agents and DeepSeek as the server model, FoT reaches 88.1%, compared with 84.6% for isolated reasoning and 92.8% when both server and agents use Gemini 3.0 Pro. With DeepSeek as local agents and Gemini 3.0 Pro as the server, FoT reaches a 58.0% accuracy, compared with 53.7% in isolation and 55.3% when both sides use DeepSeek. These results suggest that FoT remains effective across heterogeneous LLM configurations, with larger gains when the server model is stronger. Similar conclusions hold for research insight discovery. Table 25 in Appendix F.2 further demonstrates that when we have local agents each using different LLMs but working on the same task, FoT still provides performance gains. While deploying all modules with the strongest LLM yields the best performance, users can select lighter alternatives and leverage FoT’s flexibility in specific scenarios. 

### **6.4 Effects of Insight Library Size** 

In Figure 7, we vary the insight library size and observe that, without strict constraints on the total number of insights, FoT naturally reaches a favorable tradeoff between library size and performance at 20 insights, as performance improves only marginally when increasing the library size from 20 to 200. Details are provided in Appendix F.3. 

|100||Table 7: Changes in|average accu|racies rela|tive to the Is|olated Agents|
|---|---|---|---|---|---|---|
|||baseline and FoT wher|e all agents|participate|. Each row c|orresponds to|
|80<br>%)||one agent, identifed b|y the benchm|ark it wo|rks on. **Inclu**|**de One**: The|
|e (||insight library is built|from this age|nt alone.|**Exclude One**|: The insight|
|60<br>ce Rat||library is built from all<br>in Appendix F.4.|agents excep|t this one.|Changes in a|verage cost is|
|40<br>dan|||Include|One|Exclude|One|
|0<br>20<br>Gui|FoT (Ours)<br>Isolated<br>RAG|Agent|∆Isolated<br>Agents|∆FoT|∆Isolated<br>Agents|∆FoT|
||10<br>20<br>50<br>100<br>200|AIME24|+1.7|_−_6.5|+3.9|_−_4.4|
||Number of Insights|AIME25|+1.9|_−_6.4|+3.7|_−_4.5|
|||AMC|+1.5|_−_6.8|+4.6|_−_3.7|
|ure 7:|Comparison of FoT, isolated agents, and|CCEE|+3.4|_−_4.8|+3.9|_−_4.4|
|G in t|heir ability to generate insights that can|CNMO|+0.7|_−_7.5|+1.5|_−_6.8|
|er the|core contributions of ICLR 2025 papers|WLPMC|+1.2|_−_7.0|+3.9|_−_4.4|
|dance|rate) under varying numbers of generated|V202412 Hard|+1.3|_−_6.9|+3.3|_−_5.0|
|ghts.||V202505 Hard|+5.2|_−_3.1|+1.4|_−_6.8|



Figure 7: Comparison of FoT, isolated agents, and RAG in their ability to generate insights that can cover the core contributions of ICLR 2025 papers (guidance rate) under varying numbers of generated insights. 

### **6.5 Effects of Agent Participation** 

We further analyze the impact of varying the number of participating agents in FoT. For research insight discovery, performance improves as the total number of papers read increases. When the total number of papers is fixed, the number of agents has only a minor impact, with more agents yielding slight additional gains. Since these results align with intuition, we defer the details to Appendix F.4. 

We further examine how individual agents contribute to the insight library through two settings: ‘Include One’, where only one fixed local agent continuously contributes reasoning traces while all agents use the resulting library for inference, and ‘Exclude One’, where the library is constructed from all agents except one. As shown in Table 7, every agent improves performance when acting as the sole contributor, but none matches the performance achieved when all agents contribute, indicating that FoT benefits from broad agent participation. Table 7 also shows that V202505 Hard is the most influential agent, as it yields the largest improvement over isolated agents when included alone and causes the largest performance drop when excluded. We provide detailed performance of each agent in Appendix F.4. In both settings, agents are evaluated on data that are partially unseen during library construction, yet the insight library still improves performance. 

9 

Federation over Text: Insight Sharing for Multi-Agent Reasoning 

A PREPRINT 

## **7 Conclusion, Limitations, and Future Work** 

In this work, we have proposed the first federated-like multi-agent reasoning framework, Federation over Text (FoT), which enables multiple agents (each solving a task) to collaboratively learn an insight library by sharing and aggregating local reasoning traces iteratively. On the other hand, semantic-level optimization may be a double-edged sword due to inherent LLM hallucinations, which might introduce erroneous reasoning traces into the insight library. Mitigating this fundamental challenge is beyond our current scope, but future work can investigate hallucination propagation within FoT. We have demonstrated the effectiveness of FoT across diverse applications, including mathematical reasoning, cross-domain collaboration, research insight discovery, and daily OpenClaw agent tasks. Further analyses of reasoning traces, extracted insights, and ablation studies reveal how insights guide performance gains and highlight the flexibility of FoT with different local reasoning strategies and server-side aggregation methods. In future work, we aim to automate harness design [53] for FoT. In terms of broader impact, clients may leverage the framework of FoT for good or harmful use cases, such as injecting adversarial reasoning traces into the insights. 

## **References** 

- [1] Ori Yoran, Tomer Wolfson, Ben Bogin, Uri Katz, Daniel Deutch, and Jonathan Berant. Answering questions by meta-reasoning over multiple chains of thought. In _Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing (EMNLP)_ , pages 5942–5966, 2023. 

- [2] Tian Liang, Zhiwei He, Wenxiang Jiao, Xing Wang, Yan Wang, Rui Wang, Yujiu Yang, Shuming Shi, and Zhaopeng Tu. Encouraging divergent thinking in large language models through multi-agent debate. In _Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing (EMNLP)_ , pages 17889– 17904, 2024. 

- [3] Chris Lu, Cong Lu, Robert Tjarko Lange, Jakob Foerster, Jeff Clune, and David Ha. The ai scientist: Towards fully automated open-ended scientific discovery, 2024. arXiv:2408.06292. 

- [4] Samuel Schmidgall, Yusheng Su, Ze Wang, Ximeng Sun, Jialian Wu, Xiaodong Yu, Jiang Liu, Michael Moor, Zicheng Liu, and Emad Barsoum. Agent laboratory: Using LLM agents as research assistants. In _Findings of the Association for Computational Linguistics: EMNLP 2025_ , pages 5977–6043. Association for Computational Linguistics, 2025. 

- [5] Haofei Yu, Zhaochen Hong, Zirui Cheng, Kunlun Zhu, Keyang Xuan, Jinwei Yao, Tao Feng, and Jiaxuan You. Researchtown: Simulator of human research community. In _Proceedings of the International Conference on Machine Learning (ICML)_ , pages 73051–73096, 2025. 

- [6] Yongjun Zhang. Vibe researching as wolf coming: Can AI agents with skills replace or augment social scientists?, 2026. arXiv:2602.22401. 

- [7] Zixuan Ke, Fangkai Jiao, Yifei Ming, Xuan-Phi Nguyen, Austin Xu, Do Xuan Long, Minzhi Li, Chengwei Qin, Peifeng Wang, Silvio Savarese, et al. A survey of frontiers in LLM reasoning: Inference scaling, learning to reason, and agentic systems, 2025. arXiv:2504.09037. 

- [8] Brendan McMahan, Eider Moore, Daniel Ramage, Seth Hampson, and Blaise Aguera y Arcas. Communicationefficient learning of deep networks from decentralized data. In _Proceedings of the International Conference on Artificial Intelligence and Statistics (AISTATS)_ , pages 1273–1282, 2017. 

- [9] Yusen Zhang, Ruoxi Sun, Yanfei Chen, Tomas Pfister, Rui Zhang, and Sercan O Arık.<sup>¨</sup> Chain of agents: Large language models collaborating on long-context tasks. _Advances in Neural Information Processing Systems (NeurIPS)_ , 37:132208–132237, 2024. 

- [10] Khanh-Tung Tran, Dung Dao, Minh-Duong Nguyen, Quoc-Viet Pham, Barry O’Sullivan, and Hoang D Nguyen. Multi-agent collaboration mechanisms: A survey of LLMs, 2025. arXiv:2501.06322. 

- [11] Yufan Dang, Chen Qian, Xueheng Luo, Jingru Fan, Zihao Xie, Ruijie Shi, Weize Chen, Cheng Yang, Xiaoyin Che, Ye Tian, et al. Multi-agent collaboration via evolving orchestration. In _Proceedings of the Conference on Neural Information Processing Systems (NeurIPS)_ , 2025. 

- [12] Stephen Chung and Wenyu Du. The station: An open-world environment for AI-driven discovery, 2025. arXiv:2511.06309. 

- [13] Yougang Lyu, Xi Zhang, Xinhao Yi, Yuyue Zhao, Shuyu Guo, Wenxiang Hu, Jan Piotrowski, Jakub Kaliski, Jacopo Urbani, Zaiqiao Meng, et al. Evoscientist: Towards multi-agent evolving AI scientists for end-to-end scientific discovery, 2026. arXiv:2603.08127. 

10 

Federation over Text: Insight Sharing for Multi-Agent Reasoning 

A PREPRINT 

- [14] Zengqing Wu, Run Peng, Shuyuan Zheng, Qianying Liu, Xu Han, Brian I Kwon, Makoto Onizuka, Shaojie Tang, and Chuan Xiao. Shall we team up: Exploring spontaneous cooperation of competing LLM agents. In _Findings of the Association for Computational Linguistics: EMNLP 2024_ , pages 5163–5186, 2024. 

- [15] Qin Zhang, Yangbin Yu, Qiang Fu, Deheng Ye, et al. More agents is all you need. _Transactions on Machine Learning Research (TMLR)_ , 2024. 

- [16] Yujia Zheng, Zhuokai Zhao, Zijian Li, Yaqi Xie, Mingze Gao, Lizhu Zhang, and Kun Zhang. Thought communication in multiagent collaboration. In _Proceedings of the Conference on Neural Information Processing Systems (NeurIPS)_ , 2025. 

- [17] Pengsong Zhang, Xiang Hu, Guowei Huang, Yang Qi, Heng Zhang, Xiuxu Li, Jiaxing Song, Jiabin Luo, Yijiang Li, Shuo Yin, et al. aiXiv: A next-generation open access ecosystem for scientific discovery generated by AI scientists, 2025. arXiv:2508.15126. 

- [18] Chuan Li, Qianyi Zhao, Fengran Mo, and Cen Chen. Fedcot: Communication-efficient federated reasoning enhancement for large language models, 2025. arXiv:2508.10020. 

- [19] Amirkeivan Mohtashami, Florian Hartmann, Sian Gooding, Lukas Zilka, Matt Sharifi, et al. Social learning: Towards collaborative learning with large language models, 2023. arXiv:2312.11441. 

- [20] Anthropic. Skills (agent skills repository). `http://github.com/anthropics/skills` , n.d. GitHub repository. 

- [21] K-Dense Inc. Claude scientific skills: A comprehensive collection of scientific tools for claude ai. `https: //github.com/K-Dense-AI/claude-scientific-skills` , 2026. skills covering databases, packages, integrations, and analysis tools. 

- [22] Andrew Zhao, Daniel Huang, Quentin Xu, Matthieu Lin, Yong-Jin Liu, and Gao Huang. Expel: Llm agents are experiential learners. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 38, pages 19632–19642, 2024. 

- [23] Aniket Didolkar, Nicolas Ballas, Sanjeev Arora, and Anirudh Goyal. Metacognitive reuse: Turning recurring LLM reasoning into concise behaviors, 2025. arXiv:2509.13237. 

- [24] Yufan Zhuang, Chandan Singh, Liyuan Liu, Yelong Shen, Dinghuai Zhang, Jingbo Shang, Jianfeng Gao, and Weizhu Chen. Test-time recursive thinking: Self-improvement without external feedback, 2026. arXiv:2602.03094. 

- [25] Jenny Zhang, Bingchen Zhao, Wannan Yang, Jakob Foerster, Jeff Clune, Minqi Jiang, Sam Devlin, and Tatiana Shavrina. Hyperagents, 2026. arXiv:2603.19461. 

- [26] Qizheng Zhang, Changran Hu, Shubhangi Upasani, Boyuan Ma, Fenglu Hong, Vamsidhar Kamanuru, Jay Rainton, Chen Wu, Mengmeng Ji, Hanchen Li, et al. Agentic context engineering: Evolving contexts for selfimproving language models, 2025. arXiv:2510.04618. 

- [27] Xunjian Yin, Xinyi Wang, Liangming Pan, Li Lin, Xiaojun Wan, and William Yang Wang. G¨odel agent: A self-referential agent framework for recursively self-improvement. In _Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (ACL)_ , pages 27890–27913, 2025. 

- [28] Jianyu Wang, Zhiqiang Hu, and Lidong Bing. Evolving prompts in-context: An open-ended, self-replicating perspective. In _Proceedings of the International Conference on Machine Learning (ICML)_ , pages 63036–63087, 2025. 

- [29] Adam Zweiger, Jyothish Pari, Han Guo, Yoon Kim, and Pulkit Agrawal. Self-adapting language models. In _Proceedings of the Conference on Neural Information Processing Systems (NeurIPS)_ , 2025. 

- [30] Haoran Ye, Xuning He, Vincent Arak, Haonan Dong, and Guojie Song. Meta context engineering via agentic skill evolution, 2026. arXiv:2601.21557. 

- [31] Zhaofeng Zhong, Wei Yuan, Tong Chen, Xiangyu Zhao, Quoc Viet Hung Nguyen, and Hongzhi Yin. Reasoning pattern alignment merging for adaptive reasoning, 2026. arXiv:2601.03506. 

- [32] Yinjie Wang, Xuyang Chen, Xiaolong Jin, Mengdi Wang, and Ling Yang. OpenClaw-RL: Train any agent simply by talking, 2026. arXiv:2603.10165. 

- [33] Griffin Adams, Alex Fabbri, Faisal Ladhak, Eric Lehman, and No´emie Elhadad. From sparse to dense: Gpt-4 summarization with chain of density prompting. In _Proceedings of the 4th New Frontiers in Summarization Workshop_ , pages 68–74, 2023. 

- [34] Anthropic. Claude cookbooks: Examples and guides for building with claude. `https://github.com/ anthropics/claude-cookbooks` , 2024. Accessed: 2026-03-10. 

11 

Federation over Text: Insight Sharing for Multi-Agent Reasoning 

A PREPRINT 

- [35] Yifan Zhang and Team Math-AI. American invitational mathematics examination (AIME) 2024, 2024. 

- [36] Yifan Zhang and Team Math-AI. American invitational mathematics examination (AIME) 2025, 2025. 

- [37] Junnan Liu, Hongwei Liu, Linchen Xiao, Ziyi Wang, Kuikun Liu, Songyang Gao, Wenwei Zhang, Songyang Zhang, and Kai Chen. Are your LLMs capable of stable reasoning? In _Findings of the Association for Computational Linguistics: ACL 2025_ , pages 17594–17632, 2025. 

- [38] Jiachen Zhao, Yiyou Sun, Weiyan Shi, and Dawn Song. Can aha moments be fake? identifying true and decorative thinking steps in chain-of-thought, 2025. arXiv:2510.24941. 

- [39] David Rein, Betty Li Hou, Asa Cooper Stickland, Jackson Petty, Richard Yuanzhe Pang, Julien Dirani, Julian Michael, and Samuel R Bowman. GPQA: A graduate-level google-proof q&a benchmark. In _Proceedings of the First Conference on Language Modeling (COLM)_ , 2024. 

- [40] Naman Jain, King Han, Alex Gu, Wen-Ding Li, Fanjia Yan, Tianjun Zhang, Sida Wang, Armando Solar-Lezama, Koushik Sen, and Ion Stoica. Livecodebench: Holistic and contamination free evaluation of large language models for code. In _Proceedings of the International Conference on Learning Representations (ICLR)_ , 2025. 

- [41] Long Phan, Alice Gatti, Ziwen Han, Nathaniel Li, Josephina Hu, Hugh Zhang, Chen Bo Calvin Zhang, Mohamed Shaaban, John Ling, Sean Shi, and et al. Humanity’s last exam, 2025. arXiv:2501.14249. 

- [42] OpenClaw Contributors. Openclaw: Your personal open-source AI assistant. `https://github.com/ openclaw/openclaw` , 2025. Accessed: 2026-04-21. 

- [43] Kilo.ai. Pinchbench: Benchmarking LLM agents on real-world tasks, 2026. URL `https://pinchbench.com/` . 

- [44] Peter Jansen, Oyvind Tafjord, Marissa Radensky, Pao Siangliulue, Tom Hope, Bhavana Dalvi, Bodhisattwa Prasad Majumder, Daniel S Weld, and Peter Clark. Codescientist: End-to-end semi-automated scientific discovery with code-based experimentation. In _Findings of the Association for Computational Linguistics: ACL 2025_ , pages 13370–13467, 2025. 

- [45] Yixuan Weng, Minjun Zhu, Qiujie Xie, Qiyao Sun, Zhen Lin, Sifan Liu, and Yue Zhang. Deepscientist: Advancing frontier-pushing scientific findings progressively, 2025. arXiv:2509.26603. 

- [46] Ruofeng Yang, Yongcan Li, and Shuai Li. Aris: Fully autonomous research via adversarial multi-agent collaboration. `https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep` , 2026. 

- [47] Dingjie Song, Hanrong Zhang, Dawei Liu, Yixin Liu, Zongxia Li, Zhengqing Yuan, Siqi Zhang, and Lichao Sun. Dr. claw: An AI research workspace from idea to paper. `https://github.com/OpenLAIR/dr-claw` , 2026. 

- [48] Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich K¨uttler, Mike Lewis, Wen-tau Yih, Tim Rockt¨aschel, et al. Retrieval-augmented generation for knowledgeintensive NLP tasks. In _Proceedings of the Conference on Neural Information Processing Systems (NeurIPS)_ , volume 33, pages 9459–9474, 2020. 

- [49] Collin Burns, Pavel Izmailov, Jan Hendrik Kirchner, Bowen Baker, Leo Gao, Leopold Aschenbrenner, Yining Chen, Adrien Ecoffet, Manas Joglekar, Jan Leike, et al. Weak-to-strong generalization: Eliciting strong capabilities with weak supervision. In _Proceedings of the International Conference on Machine Learning (ICML)_ , 2024. 

- [50] Bowen Ye, Rang Li, Qibin Yang, Yuanxin Liu, Linli Yao, Hanglong Lv, Zhihui Xie, Chenxin An, Lei Li, Lingpeng Kong, and et al. Claw-eval: Toward trustworthy evaluation of autonomous agents, 2026. arXiv:2604.06132. 

- [51] Zeyang Sha and Yang Zhang. Prompt stealing attacks against large language models, 2024. arXiv:2402.12959. 

- [52] Nelson F Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, and Percy Liang. Lost in the middle: How language models use long contexts. _Transactions of the Association for Computational Linguistics (TACL)_ , 12:157–173, 2024. 

- [53] Yoonho Lee, Roshen Nair, Qizheng Zhang, Kangwook Lee, Omar Khattab, and Chelsea Finn. Meta-harness: End-to-end optimization of model harnesses, 2026. arXiv:2603.28052. 

- [54] Eva Y Puspaningrum, Budi Nugroho, Ariyono Setiawan, and Nuraini Hariyanti. Detection of text similarity for indication plagiarism using winnowing algorithm based k-gram and jaccard coefficient. In _Journal of physics: Conference series_ , volume 1569, page 022044. IOP Publishing, 2020. 

12 

Federation over Text: Insight Sharing for Multi-Agent Reasoning 

A PREPRINT 

## **Contents** 

|**A Usa**|**ge of AI in Writing**|**14**|
|---|---|---|
|**B**<br>**Pseu**|**do Algorithms**|**14**|
|**C Hyp**|**erparameters**|**14**|
|**D Com**|**plete Experiments for Applications of FoT**|**14**|
|D.1|Mathematical Problem Solving . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . .<br>14|
|D.2|Multi-Domain Collaboration . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . .<br>15|
|D.3|Real-World Daily Tasks . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . .<br>16|
|D.4|Research Insight Discovery . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . .<br>22|
|**E**<br>**Com**|**plete Experiments for Properties of FoT**|**23**|
|E.1|Transferability . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . .<br>23|
|E.2|Safeguarding Raw Problem Instances<br>. . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . .<br>24|
|**F**<br>**Com**|**plete Experiments for Ablation Studies**|**25**|
|F.1|Effects of Local Reasoning Strategies<br>. . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . .<br>25|
|F.2|Effects of Heterogeneous Local and Server Agent Models . . . . . . . . . . . . . . .|. . . . . . . . .<br>26|
|F.3|Effects of Insight Library Size<br>. . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . .<br>27|
|F.4|Effects of Agent Participation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . .<br>27|
|**G Com**|**plete Prompts**|**29**|
|G.1|Prompts for Our Instantiation of FoT . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . .<br>29|
|G.2|Complete Problem Prompts . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . .<br>36|
|G.3|Prompts for Metacognitive Reuse [23] . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . .<br>37|
|**H Insi**|**ghts, Raw Reasoning Processes, and Reasoning Traces**|**38**|
|H.1|Representative Insights . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . .<br>38|
|H.2|Complete Raw Reasoning Process for Case Studies in Appendix D.2 . . . . . . . . .|. . . . . . . . .<br>41|
|H.3|Example Reasoning Traces in Section 4.4 . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . .<br>46|



13 

Federation over Text: Insight Sharing for Multi-Agent Reasoning 

A PREPRINT 

## **A Usage of AI in Writing** 

We employ large language models (LLMs) primarily to improve the grammar and clarity of our writing and to assist with coding. Prompts (Appendix G) used in this work are partially generated by AI with human step-by-step guidance. Due to the nature of this research, insight libraries (Appendix H.1) and reasoning traces (Appendices H.2 and H.3) are AI generated. All research ideas, directions, and decisions, however, are independently conceived and carried out by the authors. 

## **B Pseudo Algorithms** 

We summarize the pseudo algorithms of federation over (accumulated) gradients and federation over text in Algorithms 1 and 2. 

|**Algorithm 1:**Federation over Gradients|**Algorithm 2:**Federation over Text|
|---|---|
|**1 Input**: Initial global model, client datasets|**1 Input**: Empty insight library, agent tasks, base LLM|
|**2 for**_each iteration_**do**|(can be different across agents)|
|**3**<br>**for**_each_**_Client_ do**|<br>**2 for**_each iteration_**do**|
|**4**<br>Local optimization starting from the current|**3**<br>**for**_each_**_Agent_ do**|
|<br>global model|**4**<br>Local reasoning given the base LLM and|
|**5**<br>Upload new model weights|current insight library|
|**6**<br>**end**|**5**<br>Upload reasoning traces to the server|
|**7**<br>**Server:**|**6**<br>**end**|
|**8**<br>Collect all local model weights|**7**<br>**Server:**|
|<br>**9**<br>Aggregation over model weights|**8**<br>Gather and aggregate all reasoning traces|
|<br>**10**<br>Broadcast the global model to clients|<br>**9**<br>Update the insight library|
|<br>**11 end**|<br>**10**<br>Broadcast the new library to agents|
|**12 Output:** Global model|**11 end**<br>**12 Output:** Insight library|



## **C Hyperparameters** 

In Section 4, we provide detailed descriptions of the tasks, datasets, and federation settings. Here, we additionally report the remaining hyperparameters used in FoT that were not previously introduced. All experimental results are reported with pass@1. In Sections 4.1 and 4.2, experiments are repeated 3 times. In Section 4.3, experiments are repeated 5 times. In Section 4.4, experiments are run once. We set the temperature to 0.7 and top- _p_ to 0.9. We set a repetition penalty of 1.1 for DeepSeek-R1-Distill-Qwen7B and Qwen2.5-7B-Instruct. For all Gemini models, we use the default frequency and presence penalty settings. 

For local agents, the maximum output token limits are all set to 32,768 for answer generation, 16,384 for reflection, and 8,192 for reasoning traces. On the server side, the maximum output token limits are set to 32,768 for relationship generation and 16,384 for insight library construction. 

All experiments are conducted in FP16 precision using NVIDIA A100 (40GB) GPUs when needed. 

## **D Complete Experiments for Applications of FoT** 

### **D.1 Mathematical Problem Solving** 

Table 8 shows the details of accuracy over each math benchmark. Unless otherwise specified, in all reported experiments, agents solve all benchmark questions in each round and generate corresponding reasoning traces. In other words, agents iteratively solve the exact same benchmark dataset in each round. In experiments from PinchBench to Claw-Eval (Appendix F.2) and “Include One” and “Exclude One” (Appendix F.4), we evaluate performance on tasks where the insight library is built from disjoint tasks. From Table 8, we observe that under both base models, FoT constructs useful insights and improves the average accuracy compared with the baseline of isolated agents solving the task independently. With Gemini 3.0 Pro, the improvement holds for challenging tasks such as AIME25 and V202412 Hard. 

14 

Federation over Text: Insight Sharing for Multi-Agent Reasoning 

A PREPRINT 

Table 8: Math problem-solving (LiveMathBench) accuracies under different settings. With the FoT-generated library, reasoning can reach higher accuracies. We also observe that the stronger LLM yields better results. FoT results that are better than the baselines’ are bolded. 

|**Base Models**|**Algorithms**|AIME24|AIME25|AMC|CCEE|CNMO|WLPMC|V202412<br>Hard|V202505<br>Hard|**Avg**|
|---|---|---|---|---|---|---|---|---|---|---|
|DeepSeek-R1-|Isolated Agent|0.500_±_0_._09|0.400_±_0_._09|0.674_±_0_._07|0.841_±_0_._06|0.722_±_0_._01|0.273_±_0_._15|0.524_±_0_._11|0.360_±_0_._05|0.537|
|Distill-Qwen-7B|FoT (Round 3)|0.500_±_0_._09|0.400_±_0_._09|**0.717**_±_0_._07|0.841_±_0_._06|0.722_±_0_._01|**0.364**_±_0_._15|0.524_±_0_._01|0.360_±_0_._05|**0.553**|
|Gemini 3.0|Isolated Agent|0.967_±_0_._00|0.933_±_0_._00|0.935_±_0_._00|0.864_±_0_._00|0.889_±_0_._01|0.727_±_0_._07|0.762_±_0_._06|0.690_±_0_._02|0.846|
|Pro|<br>FoT (Round 2)|**1.000**_±_0_._00|**1.000**_±_0_._00|0.935_±_0_._00|**0.909**_±_0_._07|**1.000**_±_0_._00|**0.909**_±_0_._02|**0.952**_±_0_._08|**0.720**_±_0_._03|**0.928**|



### **D.2 Multi-Domain Collaboration** 

In the first example, we show that the insight named `Constraint Satisfaction Propagation` , originally derived from AIME25 (a _mathematics_ benchmark), is retrieved and applied to a _chemistry_ problem in the GPQA Diamond dataset. The key mathematical idea is to model the problem as a constraint satisfaction problem: the goal is to determine whether the `H` atom occupies an axial or equatorial position (i.e., to find a unique valid state, as described in the insight). The agent then tests different isomeric forms and verifies them against thermodynamic constraints. 

With the constraints, the agent no longer hallucinates the position of `OH` (in Round 2 of FoT), but correctly identifies the Karplus relationship (in Round 3). The problem instance, our summary of reasoning traces in two rounds, and the insight text that we extract from the library are presented below. We present the complete raw reasoning processes for each round in Appendix H.2. 

#### **Question: GPQA Diamond, Problem 89 (Answer: C)** 

`1,3-dibromoadamantane is heated to 240`<sup>_◦_</sup> `C with an excess of KOH, creating a light yellow solid product 1, with`<sup>1</sup> `H NMR spectrum: 4.79 (2H), 2.41--2.23 (10H), 1.94 (2H) and a characteristic absorbance in the IR spectrum at 1720 cm`<sup>_−_1</sup> `.` 

_`Identify the structure of product 1 and explain the significance of the chemical shifts observed in the NMR spectrum.`_ `This product was then heated with an excess of aluminum isopropoxide, forming product 2. Ozone was bubbled through a solution of 2 at` _−_ 78<sup>_◦_</sup> `C, followed by addition of dimethyl sulfide, forming product 3. In the`<sup>1</sup> `H NMR spectrum of 3, what is the coupling pattern of the most deshielded hydrogen atom (excluding those that will exchange with deuterated solvent)?` 

```
Options:
A.doubletoftripletsB.tripletC.tripletoftripletsD.pentet
```

#### **Incorrect (Round 2)** 

```
TheagentidentifiedthecorrectsyntheticsequencefromGrob
fragmentationtoMPVreductionandthenozonolysisandcorrectly
determinedthemostdeshieldedprotonwasthecarbinolHatC7.
However,ithallucinatedthattheOHwasintheaxialposition,
leadingtoapredictionofa"pentet"whichareallsmall
couplings.
```

#### **Correct (Round 3)** 

```
WhileagainidentifyingMPVreductionasthermodynamically
controlledyieldingtheexo-alcohol,itcorrectlyreasonedthatin
thisbicyclicsystem,theexo-OHmeansH-C3isaxial.Itthen
appliedtheKarplusrelationshipsystematically.Axial-axial
couplinggiveslargeJ(10-12Hz)whileaxial-equatorialgives
smallJ(2-5Hz).
```

#### **Potentially Related Insights** 

```
[Insight]ConstraintSatisfactionPropagation:Thislogictechniquesolvespuzzlesbyiterativelynarrowingthepossibilitiesforeach
variablebasedontherestrictionsimposedbyothers.Itpropagatesdefinitevaluestotriggerachainreactionofdeductions.[Whento
use]Inlogicpuzzles(Sudoku),scheduling,orsystemconfigurationproblemswherevariablesmustsatisfyawebofmutualconstraintstofind
auniquevalidstate.
```

```
[Insight]KineticVsThermodynamicControl:Thischemicalprinciplepredictsthemajorproductofareactionbasedonconditions
(Temperature,Time).Kineticcontrolfavorsthefastest-formingproduct(lowestactivationenergy),whilethermodynamiccontrolfavorsthe
moststableproduct(lowestfinalenergy).[Whentouse]Inorganicreactions(likeadditionstodienes,enolateformation)wheremultiple
productsarepossible,todeterminewhichisomerdominatesatlowtemps(Kinetic)versushightemps(Thermodynamic).
```

In the second example, we look into a math problem from AIME. The problem statement, summary of reasoning processes, and potentially-related insights are shown below. In Round 1, with an empty insight library (i.e., isolated reasoning), the agent writes out the formulation but immediately attempts to solve the problem using the greatest common divisor (GCD), leading to an incorrect computation due to the complexity of the expression. Inspired by dynamic programming, specifically the idea of decomposing a problem into smaller overlapping subproblems, in Round 2, the correct reasoning trace instead breaks the problem down by expressing _zk_ in terms of _zk−_ 1. By applying 

15 

Federation over Text: Insight Sharing for Multi-Agent Reasoning 

A PREPRINT 

a recursive formulation, the solution first derives the general term and then substitutes the numerical values, ultimately obtaining the correct answer. 


![](P067_images/P067.pdf-0016-03.png)

### Figure analysis

The figure serves as a worked example illustrating how a potentially related insight can redirect reasoning from an erroneous computational path to a successful recursive formulation.

- **Top panel: problem statement**
  - Labeled **“Question: AIME25, Problem 28 (Answer: 248)”**.
  - Defines a rational sequence with \(x_1 = \frac{25}{11}\) and recurrence
    \[
    x_{k+1}=\frac{1}{3}\left(x_k+\frac{1}{x_k}-1\right).
    \]
  - The task is to express \(x_{2025}=\frac{m}{n}\) in lowest terms and find the remainder of \(m+n\) modulo 1000.

- **Left middle panel: Incorrect (Round 1)**
  - The reasoning rewrites the recurrence as
    \[
    x_{k+1}=\frac{x_k^2-x_k+1}{3x_k}
    \]
    and attempts to track the numerator/denominator sum \(S_k\).
  - It claims \(S_{k+1}=S_k^2/3\) and performs modular arithmetic using CRT modulo 8 and 125.
  - Directly observed outcome: the process makes a computational error, using \(12^{16}\equiv 84\pmod{125}\), leading to the final answer **752**.
  - Interpretation: this panel represents an isolated or less-guided reasoning trajectory that follows a plausible but fragile algebraic/computational route and reaches the wrong result.

- **Right middle panel: Correct (Round 2)**
  - The reasoning introduces the substitution
    \[
    z_k=\frac{2x_k-1}{x_k+1},
    \]
    which transforms the recurrence into
    \[
    z_{k+1}=z_k(z_k-1).
    \]
  - It states that the denominator follows
    \[
    D_k=12^{2^k-1},
    \]
    and that \(m+n=3D_{2025}\).
  - Directly observed modular computation: \(12^{16}\equiv 41\pmod{125}\), so \(3\times 41=123\), yielding the final answer **248**.
  - Interpretation: the panel demonstrates that a structural substitution simplifies the sequence problem and avoids the earlier erroneous arithmetic path.

- **Bottom panel: Potentially Related Insight**
  - Labeled **“Potentially Related Insight”**.
  - Describes **Dynamic Programming State Decomposition** as breaking complex problems into overlapping subproblems and storing results.
  - It emphasizes defining a state that captures necessary history and is useful for sequences, grids, recursive structures, and cases where greedy approaches fail.
  - In this figure, the insight is not applied as literal dynamic programming with memoization; rather, it motivates decomposition of the recurrence into a simpler state variable \(z_k\).

- **Overall relationship and information flow**
  - The visual layout presents the original problem at the top, then compares two reasoning outcomes side by side, followed by the abstract insight that explains why the correct route is more effective.
  - Direct observation: the incorrect and correct panels are visually parallel, encouraging comparison between the two rounds.
  - Interpretation: the figure supports the surrounding discussion that an insight library can help agents avoid unnecessary or decorative reasoning and instead begin with a more productive formulation.


When examining incorrect reasoning processes (e.g., Raw Reasoning Processes 1 and 3 in the Appendix), an interesting phenomenon occurs: there are steps that are totally irrelevant to the final answer. For example, Raw Reasoning Process 3 first gives a complicated formulation of _xk_ +1 that does not contribute to the calculation of _Sk_ +1, since the formulation of _Sk_ +1 does not come from the first step. As a result, the first step can be viewed as a ‘decorative thinking’ step. Instead, with FoT’s insight library, agents do not have to exhibit such decorative thinking in Raw Reasoning Process 4. This indicates that insights as a strong and effective prior can help LLM agents quickly start from knowledge of previous problems, reducing the chance of falling into unnecessary or illogical steps. The experiment of measuring true-thinking score [38] further verifies this argument. 

Table 9: Performance and computational cost comparison between Isolated Agents and FoT on HLE, GPQA Diamond, and LiveMathBench Hard 2025. 

|||**HLE**||**GPQ**|**A Diamond**||**LiveMathB**|**ench Har**|**d 2025**|
|---|---|---|---|---|---|---|---|---|---|
|**Method**|Acc. (%)|#Tok.|Loops|Acc. (%)|#Tok.|Loops|Acc. (%)|#Tok.|Loops|
|Isolated Agents|33.40_±_3_._11|11K_±_1|0_±_0|91.90_±_0.99|769_±_13|0_±_0|69.00_±_0_._00|739_±_7|1_±_0|
|FoT|**39.92**_±_**1.78**|**10K**_±_1|0_±_0|**94.42**_±_0_._00|**675**_±_17|0_±_0|**71.00**_±_0_._00|739_±_4|**0**_±_0|



For multi-domain collaboration, we supplement our experiments by incorporating multimodal inputs (including images) on challenging tasks where agents cannot solve most questions (i.e., isolated agent accuracy is below 50%). We use the Humanity’s Last Exam (HLE) benchmark [41]. We deploy three agents (Gemini-3.0-Pro) to work on HLE, GPQA-Diamond, and V202505-Hard, respectively. Isolated agent accuracy is below 50% for HLE. Table 9 presents the performance gains achieved by FoT on these difficult tasks across different domains. HLE contains 2,500 questions, GPQA-Diamond contains 198 questions, and LiveMathBench Hard 2025 contains 100 questions. 

As a result, we observe that when the server aggregates traces, most traces originate from incorrect answers. However, these erroneous experiences do not degrade the quality of the insight library; FoT can still aggregate useful information and improve overall performance. 

### **D.3 Real-World Daily Tasks** 

### **D.3.1 Cost Evaluation for the Application of OpenClaw** 

As agents using API services usually incur monetary costs, cost is a critical concern. In this section, we study whether the additional steps, including reflection and reasoning trace generation for local agents, as well as server-side aggre- 

16 

Federation over Text: Insight Sharing for Multi-Agent Reasoning 

A PREPRINT 

gation of the insight library, introduce significant extra cost. We use the Gemini-3.1-Pro-Preview pricing rules.<sup>5</sup> For isolated agents, the cost depends on the number of input and output tokens. For FoT, we calculate the token usage for reflection and reasoning trace generation, the server-side aggregation, and the input and output tokens when agents use the generated insight library to solve tasks. We also compute the cost for the setting where agents only use the generated library during inference. 

The cost is summarized in Table 10. We observe that although FoT requires more input tokens compared with solving tasks separately (since the prompt includes the insight library), the overall cost is reduced when considering FoT (inference) as fewer output tokens are generated given the generated library. The additional cost introduced by FoT is also not substantial, increasing the total cost only marginally. We believe users would be willing to pay a small additional cost (e.g., less than half a dollar) to achieve higher task accuracies. 

Table 10: Cost (USD) for using Gemini-3.1-Pro-Preview under different thinking levels and algorithms. Each cell reports the [min, max] range of cost observed over 5 runs of the experiment for all 25 tasks in PinchBench. FoT (all) calculates all token usage from reflection, reasoning trace generation, and server aggregation to inference with the insight library. FoT (inference) only contains the cost of inference with access to the insight library. 

|Thinking Level|Isolated Agents|FoT (all)|FoT (inference)|
|---|---|---|---|
|High|[0.62, 0.71]|[1.09, 1.14]|[0.60, 0.64]|
|Medium|[0.46, 0.63]|[0.86, 1.12]|[0.52, 0.61]|
|Low|[0.55, 0.62]|[0.95, 1.12]|[0.55, 0.62]|



### **D.3.2 Comparing with Additional Baselines** 

In addition to isolated agents, we consider two baselines for each local agent. (1) Each OpenClaw agent is equipped with a set of well-defined skills. (2) We collect all raw reasoning histories into a RAG datastore, which is then used by each agent to retrieve past traces when solving tasks. These two strong baselines are designed to highlight the performance advantage of FoT. They also reflect contrasting design philosophies: (1) embedding predefined skills introduces human-curated external knowledge, whereas FoT emphasizes autonomous generation of reusable insights; (2) directly sharing raw reasoning histories conflicts with our objective of not sharing raw questions. For skills, we install all the 52 skills provided by official OpenClaw<sup>6</sup> . Among these skills, skills `nano-pdf, summarize, github, notion, slack, weather, and coding agent` are highly relevant to PinchBench. From Table 11, both skill-augmented agents and those using a RAG datastore improve performance for the Gemini 2.5 model and can also enhance efficiency. However, analysis of the execution logs shows that these baselines rely more heavily on extended reasoning rather than effective tool usage compared to FoT, resulting in higher generation token counts by Gemini 2.5 Flash Lite. In contrast, FoT more reliably invokes the appropriate tools, leading to improved performance. 

Table 11: Performance (pass@1) and efficiency when isolated OpenClaw agents and FoT solve all tasks in PinchBench. FoT significantly improves accuracy while reducing generation token usage. We further compare against two stronger baselines: (1) isolated agents equipped with predefined, well-specified skills, and (2) isolated agents augmented with a RAG datastore constructed from the reasoning histories of all agents. 

|LLM<br>|Algorithms|Scor|e (out of|100)|Exe|cution Tim|e (s)|# Gen|eration|Tokens|
|---|---|---|---|---|---|---|---|---|---|---|
|(Thinking Level)||Max|Avg|Min|Max|Avg|Min|Max|Avg|Min|
||Isolated Agents|80.50|76.29|72.21|1864.74|**1764.72**|1683.61|53K|50K|46K|
|Gemini 3.1|Isolated Agents with Skills|81.93|65.27|54.75|3336.35|2808.19|2062.83|52K|**46K**|42K|
|Pro (High)|Isolated Agents (RAG)|83.07|64.08|52.76|3244.99|3095.42|2817.16|**51K**|48K|**41K**|
||FoT (Round 2)|**87.32**|84.82|81.71|**1845.03**|1787.98|**1658.75**|52K|48K|46K|
||Isolated Agents|27.90|20.12|12.70|2932.16|2835.36|**2157.49**|57K|55K|54K|
|Gemini 2.5|Isolated Agents with Skills|33.63|32.58|30.07|3329.39|3014.51|2898.64|77K|70K|59K|
|Flash Lite|Isolated Agents (RAG)|28.52|27.41|25.76|**2980.11**|**2783.53**|2492.54|65K|60K|57K|
||FoT (Round 2)|**53.29**|**52.11**|**50.36**|3667.24|3466.19|3223.15|57K|**54K**|**52K**|



We also compare FoT with ExpeL. ExpeL similarly lets an agent run some tasks and saves past experiences. However, ExpeL is initially designed for a single agent system and relies on labelling. ExpeL first needs several training tasks and saves the successful trajectories. For failed tasks, the agent will reflect on them with more attempts. Apart 

> 5 `https://ai.google.dev/gemini-api/docs/pricing` 

> 6 `https://github.com/openclaw/openclaw` 

17 

Federation over Text: Insight Sharing for Multi-Agent Reasoning 

A PREPRINT 

from raw successful trajectories, ExpeL also lets the agent reflect on successes and failures to generate several rules. We convert ExpeL into a distributed multi-agent version where we choose OpenClaw agents working on tasks 1-12 on PinchBench as training agents and the rest as evaluation agents. We tune the hyperparameters and set the max reflection depth as 3. The maximum number of rules is 20 since FoT generates 20 insights. The top-K to retrieve from the RAG datastore is 3. For a fair comparison, we first generate an insight library with agents working on tasks 1-12 in FoT and let the remaining agents use the insight library to resolve the tasks. 

Table 12: Performance (pass@1) and efficiency when OpenClaw agents and FoT solve tasks 13-23 in PinchBench. ExpeL uses agents working on task 1-12 as training agents while FoT uses them to generate insight library. 

|LLM<br>(Thinking Level)|Algorithms|Scor<br>Max|e (out of<br>Avg|100)<br>Min|# Gen<br>Max|eration<br>Avg|Tokens<br>Min|Total<br>Max|Cost (<br>Avg|USD)<br>Min|
|---|---|---|---|---|---|---|---|---|---|---|
|Gemini 31|Isolated Agents|72.45|66.32|59.98|33K|29K|26K|**0.38**|**0.35**|**0.33**|
|.<br>Pro (Hih)|ExpeL|75.00|57.76|31.90|51K|49K|46K|1.67|1.56|1.53|
|g|FoT|**90.68**|**77.05**|**64.50**|**30K**|**28K**|26K|0.77|0.67|0.62|



From the results in Table 12, we find several pieces of evidence showing that ExpeL is not suitable for this application. First, ExpeL is initially focused on single-agent systems and collects experience from the same type of tasks. In PinchBench, tasks are heterogeneous and often unrelated. For example, task 13 involves file searching, task 14 involves generating AI images, and task 15 involves humanizing AI-generated blogs. In contrast, FoT is designed to learn crossdomain knowledge and can achieve performance improvements across different task types. Second, ExpeL relies on labeling and training. This training process incurs substantially higher costs, more than double the total cost of FoT. Third, as discussed earlier, directly extending ExpeL into a distributed version requires uploading raw trajectories. 


![](P067_images/P067.pdf-0018-06.png)


Figure 8: Comparison of tool-call counts across different models and algorithms on the 23 tasks in PinchBench v1. For each setting, we sample the run with the minimum execution latency. In Gemini 3.1 Pro, higher thinking levels tend to reduce execution-time tool calls, and FoT further decreases tool usage under the medium and high thinking settings. 

### **D.3.3 Examples of Tool Usage** 

As shown in Figure 8, for Gemini 3.1 Pro, the number of execution-tool calls decreases as the thinking level increases, suggesting that the model can more effectively identify the most critical tools and solve the task with fewer redundant calls. This also explains why FoT improves both accuracy and latency under the medium and high thinking settings: agents can avoid repeated or unnecessary tool execution by leveraging the shared library. 

18 

Federation over Text: Insight Sharing for Multi-Agent Reasoning 

A PREPRINT 

The first example is the ‘Search and Replace in Files’ task, with task ID `task` ~~`s`~~ `kill` ~~`s`~~ `earch` , from PinchBench. We use Gemini 3.1 Pro with the medium thinking level. To more clearly demonstrate the workflow, we show each tool-calling step together with its arguments and outputs, while omitting the model’s reasoning outputs. With the hint from the insight library, agents directly use functions of READ and EDIT to search and write the related information rather than using EXEC function with system functions of ‘cat’. In this way, the agent can organize the editing in a more structured way and resolve the task more efficiently. 

#### **Potentially Related Insight** 

```
[insight]ConstraintDrivenSchemaMapping:Thisorganizationalparadigmtranslatescomplex,multi-partfree-textinstructionsintoarigid
structuralblueprintbeforegenerationbegins,forcingcompleteadherencetoconstraints.Itsolvestheproblemofgenerativemodels
silentlydroppingminorpromptrequirementsorhallucinatingoutputshapes.Whentouse:Applywhengeneratinghighlystructuredreports,
standardizeddatapipelines,ortasksthatexplicitlydemandspecificformats,exactparagraphcounts,ormultifacetedcomparativetables.
Details:1)Parsetheuserprompttoidentifyallnumerical,structural,andtopicalconstraints.2)Maptheseconstraintsintoaninternal
documentschema(e.g.,specificmarkdownheaders,predefinedtablecolumns).3)Executeathematicbucketingpassoverthesourcedata,
fillingthepre-establishedschema.4)Cullobjectiveconstraints(e.g.,filteringalistof50itemsdowntoexactlythe5requested)
beforefinalizingthewritestep.
```

```
[insight]IdempotentEnvironmentScaffolding:Thistechniquefocusesonsafelyinjectingconfigurationsorcodeintoenvironmentsbyusing
implicitcreationtoolsandcontext-aware,non-destructivemutationstrategies.Itpreventsoverwritingexistingworkorfailingdueto
missingparentstructures.Whentouse:Applywhensettingupprojectdirectories,dynamicallygeneratinglogs,orappendingmultiline
configurations(YAML,JSON)acrossmulti-environmentworkspaces.Details:1)Relyonwriteoperationsthatinherentlyconstructmissing
parentdirectories,halvingtheneededoperationcount.2)EnforceOS-agnosticpathing(forwardslashes).3)Checkifthetargetis
populated;ifso,switchfrom’overwrite’to’append’oruseformat-awaretextreplacementthatrespectsspecificsyntax(likeYAML
indentationorJSONquotes)ratherthannaiveglobalstringreplacement.[insight]VerifiableStatePipelining:Thismethodologyenforcesa
strictlylinearprogressionfordatamutation:readsource,processinternally,writetodestination,andphysicallyverifytheoutputstate
(e.g.,viabyte-countvalidationorhashchecking)beforeconcludingthetask.Itsolvestheproblemofautomatedsystemhallucinationand
unconfirmedexecutions.Whentouse:Usewheneverperformingdestructivefilemodifications,criticaldatamigrations,orformat
conversionswheresilentfailureswouldcompromisesystemintegrity.Details:1)Readtheexistingstateintoworkingmemory.2)Apply
processinglogic.3)Executethewritetool.4)Usethebyte-countorstatusreturnofthewriteoperationasanimplicitproxyconstraint
check.5)Onlyreportsuccessaftertheverificationstepconfirmsthestructuralintegrityofthetarget.
```

#### **Isolated Agents** 

`Call 1. function name:` exec `. argument: ls -la config/. output: drwxr-xr-x 2 user user 4096 Apr 13 20:47 . drwxr-xr-x 5 user user 4096 Apr 13 20:47 .. -rw-r--r-- 1 user user 268 Apr 13 20:47 database.yml -rw-r--r-- 1 user user 304 Apr 13 20:47 settings.json Call 2. function name:` exec `. argument: cat config/database.yml && echo "---" && cat config/settings.json. output: both files printed back-to-back (575 bytes total); the agent now has the YAML and the JSON in working memory but only as flat text. Call 3. function name:` exec `. argument:` 

```
sed-i’s|http://localhost:3000|https://api.example.com|g’config/settings.json\
&&sed-i’s/localhost/prod-db.example.com/g’config/settings.json\
&&sed-i’s/myapp_dev/myapp_prod/g’config/settings.json\
&&sed-i’s/myapp_test/myapp_prod/g’config/settings.json\
&&sed-i’s/"level":"debug"/"level":"warn"/g’config/settings.json
```

`output: The agent gets no confirmation that anything changed; the URL http://localhost:3000 contains localhost as a substring, so the URL rewrite` _`must`_ `run before the generic localhost` _→_ `prod-db.example.com rule, and the first sed has to switch its delimiter from / to | because the URL itself contains / characters. Call 4. function name:` exec `.` 

```
argument:
```

```
sed-i’s/localhost/prod-db.example.com/g’config/database.yml\
&&sed-i’s/myapp_dev/myapp_prod/g’config/database.yml\
&&sed-i’s/myapp_test/myapp_prod/g’config/database.yml
```

`output: sed sweeps both the development: and test: blocks at once, so the agent cannot tell from the result whether one, both, or zero blocks were modified. Call 5. function name:` exec `. argument: cat config/database.yml && echo "---" && cat config/settings.json. output: both files re-printed after the rewrite, showing host: prod-db.example.com, database: myapp prod, "endpoint": "https://api.example.com", "level": "warn". This read-back is the agent’s only check that the JSON/YAML survived.` 

19 

Federation over Text: Insight Sharing for Multi-Agent Reasoning 

A PREPRINT 

**FoT (Round 3)** 

`Call 1. function name:` exec `. argument: find config -type f. output: config/settings.json config/database.yml Call 2. function name:` read `. argument:` _{_ `path: "config/settings.json"` _}_ `. Call 3. function name:` read `. argument:` _{_ `path: "config/database.yml"` _}_ `. Call 4. function name:` edit `. argument: { "path": "config/settings.json", "edits": [ { "oldText": " \"database\": {\n \"host\": \"localhost\",\n \"port\": 5432,\n \"name\": \"myapp_dev\",", "newText": " \"database\": {\n \"host\": \"prod-db.example.com\",\n \"port\": 5432,\n \"name\": \"myapp_prod\"," }, { "oldText": " \"api\": {\n \"endpoint\": \"http://localhost:3000\",", "newText": " \"api\": {\n \"endpoint\": \"https://api.example.com\"," }, { "oldText": " \"logging\": {\n \"level\": \"debug\",", "newText": " \"logging\": {\n \"level\": \"warn\"," } ] } Call 5. function name:` edit `. argument: { "path": "config/database.yml", "edits": [ { "oldText": "development:\n adapter: postgresql\n host: localhost\n port: 5432\n database: myapp_dev", "newText": "development:\n adapter: postgresql\n host: prod-db.example.com\n port: 5432\n database: myapp_prod" }, { "oldText": "test:\n adapter: postgresql\n host: localhost\n port: 5432\n database: myapp_test", "newText": "test:\n adapter: postgresql\n host: prod-db.example.com\n port: 5432\n database: myapp_prod" } ] }` 

The second example is the ‘Polymarket + News Briefing’ task, with task ID `task polymarket` ~~`b`~~ `riefing` , from PinchBench. We use Gemini 3.1 Pro with the high thinking level. For isolated agents, there are redundant APIparameter exploration steps that do not contribute to retrieving the Polymarket information, as well as two undirected web searches. FoT replaces these calls with a more disciplined broad-then-narrow retrieval pattern, achieving a 4% accuracy improvement. 

#### **Potentially Related Insight** 

```
[insight]ConsolidatedIntentBasedQuerying:Thisdataretrievalstrategysynthesizesfragmented,conversationaluserrequestsinto
comprehensive,Boolean-expandedmasterqueries.Itcapturesmultipledimensions(entity,temporalmarkers,semanticequivalents)inasingle
denseAPIcall.Whentouse:Applythiswhenqueryingsearchengines,documentdatabases,orexternalAPIstodramaticallyminimize
round-triplatency,avoidredundanttoolusage,andpreventrelevantresultsfrombeingdroppedduetocolloquialvocabularymismatches.
[insight]IterativeTemporalQueryAnchoring:Thisactive-searchtechniqueinjectsabsolutecurrent-datetemporalmarkers(e.g.,specific
month/year)intootherwisegenericsearchqueries,oftenutilizingatwo-passrefinementstrategy:abroadsearchtodiscovercontext,
followedbyatime-anchoredsearchtofetchthelatestdevelopments.Whentouse:Applythiswhenapromptimposesstrictrecency
constraints(’latestnews’,’upcomingevents’)topreventsearchtoolsfromnativelydefaultingtohistoricallyauthoritativebutoutdated
results.,
```

20 

Federation over Text: Insight Sharing for Multi-Agent Reasoning 

A PREPRINT 

|**Isolated Agents**|
|---|
|`Call 1.`<br>`function name:`<br>exec`.`<br>`argument:`<br>`curl -s "https://gamma-api.polymarket.com/events?limit=10&active=true&closed=false\`<br>`&order=volume24hr&ascending=false" | jq -r ’.[0:3] | .[] | .title’`<br>`output:`<br>`US x Iran ceasefire by...?`<br>`The Masters - Winner`<br>`2026 FIFA World Cup Winner`<br>`Call 2.`<br>`function name:`<br>exec`.`<br>`argument:`<br>`the same curl with limit=5, jq projecting .title + " - Volume:`<br>`" + (.volume24hr|tostring).`<br>`output:`<br>`the same three titles plus two more, now annotated with 24-hour volume.`<br>`The first request is effectively re-issued just to add a`<br>`column.`<br>`Call 3.`<br>`function name:`<br>exec`.`<br>`argument:`<br>`the same curl with limit=3, jq projecting .title, .description of the top event.`<br>`output:`<br>`the 1.8 KB description of the US-Iran ceasefire market.`<br>`The agent now has descriptions, but only for the first market and only by`<br>`re-issuing the same API call a third time.`<br>`Call 4.`<br>`function name:`<br>exec`.`<br>`argument:`<br>`date "+%A, %B %d, %Y".`<br>`output:`<br>`Friday, April 10, 2026.`<br>`The agent uses this for the file header but does not re-use the date as a temporal anchor in any of its`<br>`upcoming searches.`<br>`Call 5.`<br>`function name:`<br>session<br>status`.`<br>`argument:`<br>_{}_`.`<br>`output:`<br>`a context-window diagnostic (Tokens:`<br>`14k in / 1.3k out`_|_`Context:`<br>`20k/200k); does not contribute to the artifact.`<br>`Call 6.`<br>`function name:`<br>web<br>~~s~~earch`.`<br>`argument:`<br>_{_ `query:`<br>`"US Iran ceasefire news"` _}_`.`<br>`output:`<br>`‘‘A two-week conditional ceasefire between the United States and Iran was announced on Tuesday, April 7, 2026 ...’’.`<br>`No count is`<br>`specified and no temporal anchor is supplied; the agent accepts whatever ranks first.`<br>`Call 7.`<br>`function name:`<br>web<br>~~s~~earch`.`<br>`argument:`<br>_{_ `query:`<br>`"The Masters golf 2026 news"` _}_`.`<br>`output:`<br>`tournament background and field information for the 2026 Masters; again no temporal narrowing.`<br>`Call 8.`<br>`function name:`<br>web<br>~~s~~earch`.`<br>`argument:`<br>_{_ `query:`<br>`"2026 FIFA World Cup news"` _}_`.`<br>`output:`<br>`a generic overview of the 48-team format.`<br>`Ambient context, not a ‘‘last 48 hours’’ driver.`<br>`Call 9.`<br>`function name:`<br>write`.`<br>`argument:`<br>`a 1.2 KB polymarket`<br>~~`b`~~`riefing.md synthesising the three markets from the outputs of Calls 6/7/8.`<br>`output:`<br>`Successfully wrote 1226 bytes to polymarket`<br>`briefing.md.`<br>`The briefing is graded 66.7%.`|



21 

Federation over Text: Insight Sharing for Multi-Agent Reasoning 

A PREPRINT 

|**FoT (Round 3)**|
|---|
|`Call 1.`<br>`function name:`<br>exec`.`<br>`argument:`<br>`curl -s "https://gamma-api.polymarket.com/events?limit=10&active=true&closed=false" \`<br>`| jq ’[.[] | {title: .title, volume: .volume}] | sort_by(.volume) | reverse | .[0:3]’`<br>`output:`<br>`[`<br>`{ "title": "MicroStrategy sells any Bitcoin by ___ ?",`<br>`"volume": 22098024.99 },`<br>`{ "title": "Starmer out by...?",`<br>`"volume": 10608225.14 },`<br>`{ "title": "Ukraine recognizes Russian sovereignty over its territory by...?", "volume": 2350850.67 }`<br>`]`<br>`Call 2.`<br>`function name:`<br>web<br>~~s~~earch `(`_`broad-driver pass`_`).`<br>`argument:`<br>_{_ `query:`<br>`"`_\_`"MicroStrategy`_\_`" sells Bitcoin", count:`<br>`3` _}_`.`<br>`output:`<br>`MicroStrategy primarily holds Bitcoin long-term; as of April 6, 2026 the company holds` _∼_`766,970 BTC. Surfaces the entity but not`<br>`the catalyst.`<br>`Call 3.`<br>`function name:`<br>web<br>~~s~~earch `(`_`broad-driver pass`_`).`<br>`argument:`<br>_{_ `query:`<br>`"`_\_`"Keir Starmer`_\_`" step down OR out OR resign", count:`<br>`3` _}_`.`<br>`output:`<br>`Starmer is under pressure due to the` _`Peter Mandelson`_ `appointment and the` _`May 2026 local elections`_`.`<br>`The first pass discovers the`<br>`catalyst.`<br>`Note the Boolean expansion of the colloquial market title ‘‘Starmer out’’ into formal vocabulary.`<br>`Call 4.`<br>`function name:`<br>web<br>~~s~~earch `(`_`broad-driver pass`_`).`<br>`argument:`<br>_{_ `query:`<br>`"Ukraine recognizes Russian sovereignty territory", count:`<br>`3` _}_`.`<br>`output:`<br>`Ukraine’s official non-recognition position; establishes the backdrop but is not yet news-fresh.`<br>`Call 5.`<br>`function name:`<br>session<br>status`.`<br>`argument:`<br>_{}_`.`<br>`output:`<br>`Tokens:`<br>`9.7k in / 948 out`_|_`Context:`<br>`22k/200k.`<br>`Call 6.`<br>`function name:`<br>web<br>~~s~~earch `(`_`narrow + temporal anchor pass`_`).`<br>`argument:`<br>_{_ `query:`<br>`"MicroStrategy Bitcoin news April 2026", count:`<br>`5` _}_`.`<br>`output:`<br>`‘‘MicroStrategy resumed its aggressive Bitcoin acquisition in April 2026, purchasing an additional 4,871 BTC between April 1 and`<br>`April 5, 2026,` _∼_`$329.9 M at` _∼_`$67,718 / BTC.’’ This is the last-48-hours driver that the Isolated trace never found.`<br>`Call 7.`<br>`function name:`<br>web<br>~~s~~earch `(`_`narrow + temporal anchor pass`_`).`<br>`argument:`<br>_{_ `query:`<br>`"Keir Starmer resign Peter Mandelson April 2026", count:`<br>`5` _}_`.`<br>`output:`<br>`combines the entity, the catalyst the broad pass surfaced (Mandelson), and the temporal anchor; returns the specific April-2026`<br>`political timeline including the May local-elections trigger.`<br>`Call 8.`<br>`function name:`<br>web<br>~~s~~earch `(`_`narrow + temporal anchor pass`_`).`<br>`argument:`<br>_{_ `query:`<br>`"Ukraine Russia peace plan Trump April 2026", count:`<br>`5` _}_`.`<br>`output:`<br>`details of the ‘‘Trump 28-point peace plan’’ and ongoing diplomatic efforts in early 2026 --- once again, the right driver surfaces`<br>`only after the second pass.`<br>`Call 9.`<br>`function name:`<br>write`.`<br>`argument:`<br>`a 2.0 KB polymarket`<br>~~`b`~~`riefing.md that, for each market, juxtaposes ‘‘the established fact’’ against ‘‘the unresolved variable’’`<br>`(Mandelson dismissal + May local elections; Saylor’s April BTC buys vs. $12.4 B paper loss; Trump 28-point plan vs. Ukraine’s non-recognition`<br>`stance).`<br>`output:`<br>`Successfully wrote 2006 bytes to polymarket`<br>`briefing.md.`<br>`Accuracy:`<br>`70.7%.`|



### **D.4 Research Insight Discovery** 

### **D.4.1 Cross Model Validation for Research Insight Discovery** 

To validate the reliability of the LLM-as-a-judge framework for research insight discovery, we perform cross-model evaluation using three additional models beyond Gemini 3.0 Pro. As shown in Table 13, Gemini 3.0 Pro exhibits self-evaluation bias, with the guidance rate for isolated agents on oral papers dropping from 70.9% to 5.8% when evaluated by Gemini 2.5 Flash Lite. In contrast, FoT maintains strong guidance rates under cross-model evaluation by Gemini 2.5 Flash Lite, indicating better generalization and reduced bias. 

Table 13: Percentage of papers guided by insights generated by different models, with cross-validation performed by a separate model acting as an LLM-as-a-judge. 

|Generation<br>|Judge<br>|**Isol**|**ated Ag**|**ents (Gemi**|**ni)**|**RAG**|**(Gemi**|**ni + All Pap**|**ers)**|**FoT (G**|**emini +**|**Insight Li**|**brary)**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Model|Model|||||||||||||
|||Overall|Oral|Spotlight|Poster|Overall|Oral|Spotlight|Poster|Overall|Oral|Spotlight|Poster|
||Gemini 3.0 Pro|41.3|**70.9**|**73.8**|33.3|66.5|58.1|69.2|66.4|**67.4**|67.4|68.7|**67.2**|
|Gii 30 P|Gemini 2.5 Flash Lite|2.2|5.8|2.2|2.8|69.4|72.1|73.8|68.4|**70.6**|**73.3**|**74.1**|**69.7**|
|emn . ro|Qwen2.5-7B-Instruct|3.2|2.3|3.5|3.2|0.5|0.0|0.5|0.6|**4.0**|**7.0**|**3.3**|**4.0**|
||DeepSeek-R1-Distill-Qwen-7B|17.2|20.2|16.4|17.1|34.4|34.5|34.4|34.4|**43.6**|**46.4**|**42.9**|**43.4**|
||Gemini 3.0 Pro|0.7|0.5|0.8|0.7|77.4|63.4|67.4|79.6|**82.4**|**82.2**|**82.1**|**82.4**|
|Gii 20 Flh|Gemini 2.5 Flash Lite|47.3|53.6|54.2|46.1|**62.2**|34.3|**80.5**|50.0|60.9|**64.8**|58.4|**61.0**|
|emn . as|Qwen2.5-7B-Instruct|0.9|0.0|0.5|1.0|1.3|0.0|1.1|1.4|**5.1**|**5.6**|**5.3**|**5.0**|
||DeepSeek-R1-Distill-Qwen-7B|22.0|**22.5**|21.4|22.0|17.4|17.8|16.8|17.4|**22.8**|22.1|**23.7**|**22.8**|



22 

Federation over Text: Insight Sharing for Multi-Agent Reasoning 

A PREPRINT 

## **E Complete Experiments for Properties of FoT** 

### **E.1 Transferability** 

In addition to transferring the insight library across agents using different LLMs, we evaluate insight transfer across tasks. Extending the setup in Section 4.3, we introduce new agents operating on Claw-Eval [50]. Claw-Eval contains 199 daily tasks, including tasks of visual input and artifact generation, simulated user interaction, trajectory-level grading, embedded constraint checking, and controlled error injection which PinchBench does not include. The ClawEval metrics also measure other dimensions such as robustness and safety besides completion. Upon joining the federation, these agents are initialized with an `insight.md` generated from agents previously working on PinchBench. Results in Table 14 show that new agents need fewer inference tokens and hence save cost with the help of the previous library. We provide detailed results of the transferability experiments on each math benchmark in Table 15. 

Table 14: Evaluation of the benefits of insight libraries generated by PinchBench on Claw-Eval. Insights produced by PinchBench can help new agents on Claw-Eval improve performance, save generation tokens, and cost. The reported generation token usage and cost savings are summation over all tasks. Remaining metrics are averaged over tasks; the standard deviation is computed across five runs. 

|**Agent Model**|**Insight Library**|Score|Completion Score|Robustness|Safety|# Generation Tokens|Latency (s)|Cost Saved (USD)|
|---|---|---|---|---|---|---|---|---|
|Gemini2.5|–|43.22_±_0.5|30.20_±_1.5|**94.7**_±_**0.7**|**98.82**_±_**1.0**|373K_±_12|36.99_±_2.3|0|
|Flash Lite|PinchBench|**43.73**_±_**0.2**|**31.01**_±_**1.0**|94.4_±_0.5|98_._2_±_1_._0|**352K**_±_**10**|**35.64**_±_**2.1**|0.051|



Table 15: Evaluation of the benefits of insight libraries generated by different LLMs on math problem-solving datasets. Insights produced by stronger models (Gemini 3.0 Pro) consistently benefit agents with weaker LLMs (DeepSeek), while insight libraries curated from weaker agents can lead to performance improvements for stronger ones. 

|**Agent Model**|**Insight Library**<br>**Model**|AIME24|AIME25|AMC|CCEE|CNMO|WLPMC|V202412<br>Hard|V202505<br>Hard|
|---|---|---|---|---|---|---|---|---|---|
|Isolated DeepSeek|N/A|0.500|0.400|0.674|0.841|0.722|0.273|0.524|0.360|
|DeepSeek|Gemini 3.0 Pro|**0.833**|**0.567**|**0.696**|0.841|0.722|**0.455**|0.524|0.360|
|Isolated Gemini 3.0 Pro|N/A|0.967|0.933|0.935|0.864|0.889|0.727|0.762|0.690|
|Gemini 3.0 Pro|DeepSeek|**1.000**|0.933|0.935|0.886|**0.944**|0.909|**0.905**|**0.700**|



Table 16: Math problem-solving accuracies under different settings and unseen questions. With the FoT-generated library, reasoning can reach higher accuracies. Each cell reports mean _±_ std over 3 runs. 

||**Base Models**|**Algorithms**|AIME24|AIME25|AMC|CCEE|CNMO|WLPMC|V202412<br>Hard|V202505<br>Hard|**Avg**|
|---|---|---|---|---|---|---|---|---|---|---|---|
|Existing Problems|Gemini 3.1<br>Pro|Isolated Agent<br>FoT|1.000_±_0.000<br>1.000_±_0.000|0.978_±_0.031<br>1.000_±_0.000|0.895_±_0.022<br>0.898_±_0.021|0.894_±_0.021<br>0.879_±_0.043|0.926_±_0.052<br>0.963_±_0.052|0.811_±_0.016<br>0.878_±_0.087|0.903_±_0.004<br>0.903_±_0.082|0.673_±_0.034<br>0.687_±_0.034|0.885_±_0.018<br>0.901_±_0.009|
||Gemini 2.5<br>Flash Lite|Isolated Agent<br>FoT|0.978_±_0.031<br>1.000_±_0.000|0.978_±_0.031<br>0.978_±_0.031|0.913_±_0.036<br>0.927_±_0.041|0.864_±_0.064<br>0.877_±_0.046|1.000_±_0.000<br>1.000_±_0.000|0.800_±_0.163<br>0.811_±_0.016|0.833_±_0.047<br>0.903_±_0.082|0.693_±_0.034<br>0.713_±_0.047|0.882_±_0.035<br>0.901_±_0.020|
|New Problems|Gemini 3.1<br>Pro|Isolated Agent<br>FoT|1.000_±_0.000<br>1.000_±_0.000|0.956_±_0.031<br>0.978_±_0.031|0.942_±_0.041<br>0.942_±_0.041|0.894_±_0.057<br>0.909_±_0.037|0.963_±_0.052<br>0.926_±_0.052|0.833_±_0.000<br>0.833_±_0.000|0.879_±_0.043<br>0.879_±_0.043|0.707_±_0.019<br>0.727_±_0.009|0.891_±_0.022<br>0.899_±_0.012|
||Gemini 2.5<br>Flash Lite|Isolated Agent<br>FoT|0.978_±_0.031<br>1.000_±_0.000|0.956_±_0.031<br>0.956_±_0.031|0.942_±_0.041<br>0.942_±_0.041|0.909_±_0.037<br>0.909_±_0.037|0.889_±_0.000<br>0.926_±_0.052|0.778_±_0.079<br>0.833_±_0.000|0.848_±_0.043<br>0.909_±_0.074|0.687_±_0.034<br>0.720_±_0.033|0.873_±_0.016<br>0.899_±_0.008|



Table 17: Multi-domain collaboration accuracies under different settings on existing and new problems. FoT-generated insight libraries consistently improve collaborative reasoning performance, particularly on unseen tasks. Results are reported as mean _±_ standard deviation across three runs. 

||**Algorithms**|AIME24|AIME25|GPQA|GPQA Diamond|LiveCodeBench|**Avg**|
|---|---|---|---|---|---|---|---|
|Eiti Pbl|Isolated Agent|0_._978_±_0_._031|0_._978_±_0_._031|0_._929_±_0_._026|0_._888_±_0_._017|0_._345_±_0_._050|0_._824_±_0_._019|
|xsng roems|FoT|1_._000_±_0_._000|0_._978_±_0_._031|0_._941_±_0_._015|0_._885_±_0_._021|0_._446_±_0_._054|0_._850_±_0_._006|
|N Pbl|Isolated Agent|0_._978_±_0_._031|0_._956_±_0_._031|0_._946_±_0_._015|0_._906_±_0_._018|0_._462_±_0_._056|0_._850_±_0_._015|
|ew roems|FoT|1_._000_±_0_._000|0_._956_±_0_._031|0_._953_±_0_._006|0_._909_±_0_._018|0_._515_±_0_._018|0_._867_±_0_._003|



Table 16 shows the details of accuracy over each math benchmark and Table 17 shows the details over benchmarks in multi-domain collaboration. 

23 

Federation over Text: Insight Sharing for Multi-Agent Reasoning 

A PREPRINT 

### **E.2 Safeguarding Raw Problem Instances** 

First, we investigate whether the original task description can be inferred from uploaded reasoning traces. We adopt a strong prompt-stealing attack setting [51], where the attacker or an honest-but-curious server aims to reconstruct the original task prompt from observed traces. In PinchBench daily tasks, the attacker is given a reasoning trace and must infer the agent’s input, including the user query and auxiliary information (e.g., documents to be summarized). The attack consists of two components: a parameter extractor, which classifies the prompt type into direct user request, role-based (persona or instructional framing), or in-context (demonstrations or substantial context), and a prompt extractor, which reconstructs the prompt. The two components interact for three rounds to refine the output. We use Gemini-2.5-Pro as the attacking model and evaluate attacks on libraries generated by FoT using Gemini-3.1-Pro (high thinking) and Gemini-2.5-Flash-Lite. 

We use several metrics to measure whether the attacker reconstructs the original input. We first evaluate reconstruction quality using character-level similarity, defined as<sup><u>2</u></sup> _T_<sup>_<u>M</u>_, where</sup><sup>_M_is the number of matching characters (in contiguous</sup> substrings appearing in both strings in the same order) and _T_ is the total number of characters across both strings. We also report token-level F1 score and the extent of personally identifiable information (PII) leakage. Due to the small size of PinchBench (25 tasks), PII is manually annotated. In addition, we report the classification accuracy of the parameter extractor component in the model. The parameter extractor performs worse than random guessing, indicating that it fails to reliably identify the prompt structure. In Table 18, we see that both character-level similarity and token-level F1 scores are low, further confirming that the reconstructed prompts do not closely match the originals. Prior work [51] suggests that successful prompt reconstruction typically requires similarity exceeding 60%, which is not observed in our setting. 

At the same time, these metrics are not expected to be zero. Reasoning traces necessarily retain some task-relevant information to enable knowledge transfer across agents. If similarities were zero, it would imply that the traces are entirely unrelated to the original tasks, i.e., effectively hallucinated and non-informative. Hence, we can draw the conclusion that reasoning traces are effective at hiding raw problem instances from the server. More importantly, no personal identity information can be inferred. 

Table 18: Prompt stealing attack results. The attacker uses Gemini-2.5-Pro with PinchBench reasoning traces in FoT to reconstruct the original input. The low character-level similarity, low token-level F1, and low parameter-extraction accuracy indicate that the attack fails to recover the original input, suggesting an effective defense. No personal identity information (PII) is leaked. The closest reconstruction achieved by the attacker is inferring that the instruction involves common file names such as _“ai blog.txt”_ and _“humanized blog.txt”_ . 

|**FoT Model**|Char Similarity|Token F1|PII leaked|Parameter Extractor Acc|
|---|---|---|---|---|
|Gemini 3.1 Pro|14.89%|22.85%|0|26.09%|
|Gemini 2.5 Flash Lite|11.94%|24.44%|0|21.74%|



Second, we adopt a strict _n_ -gram matching test to check: (1) that uploaded reasoning traces do not overlap with the original inputs (e.g., benchmark questions and ground-truth answers), and (2) that the insight library does not contain original inputs. 

For each application, we append all problem instances together into a document, and partition the document into 4- gram token shingles. Problems refer to questions, tasks, or papers depending on the application. We do the same for answers, insight libraries, and reasoning traces, separately. Each document is a set of all 4-gram token shingles. We then evaluate similarities between (a) reasoning traces and problems, and between (b) the insight library and problems + answers, by reporting the Jaccard similarities between the two sets of 4-gram tokens in the corresponding two documents. Prior work on shingle-based plagiarism detection shows that the choice of _n_ in _n_ -gram significantly affects similarity estimates, with smaller _n_ leading to inflated overlap due to common phrases and larger _n_ being overly sensitive to minor edits [54]. We adopt 4-gram shingles as a balanced choice that reduces false positives while remaining sensitive to meaningful phrase-level reuse. 

In Table 19, we observe that Jaccard similarity is near zero, indicating that the reasoning traces have little overlap with raw user questions and answers, achieving one of the goals of FoT. The zero similarity between the insight library and the problems further suggests that an adversary cannot obtain raw problem instances by examining the library. 

Furthermore, our work does not focus on studying prompt leakage or defenses for multi-agent reasoning. Instead, in addition to improving reasoning effectiveness and efficiency, FoT brings about the side benefit of data minimization by exposing the underlying logic-level summarization of the reasoning processes as opposed to raw reasoning data or task data. A more thorough investigation of safety and privacy in FoT is beyond the scope of this work. 

24 

Federation over Text: Insight Sharing for Multi-Agent Reasoning 

A PREPRINT 

Table 19: The measurement of overlap between the insight library (IL), reasoning traces (RT), and problems. # Problems refer to questions, tasks, or papers depending on the application. Jaccard similarity is computed between 4-gram token sets constructed from problem statements, answers, reasoning traces, and insight libraries. 

|Application|Agent Model|#Problems|# Tokens<br>RT|# Tokens<br>IL|# Insights|Jaccard<br>(RT and<br>problems)|Jaccard<br>(IL and<br>problems & answers)|
|---|---|---|---|---|---|---|---|
|Math Benchmark|Gemini 3.0 Pro|300|53K|12K|37|0.000|0.000|
|Math Benchmark|DeepSeek|300|33K|3K|11|0.000|0.000|
|Science+Math+Coding|Gemini 3.0 Pro|881|725K|2.9K|34|0.000|0.000|
|HLE+Science+Math|Gemini 3.0 Pro|2798|450K|3.2K|40|0.000|0.000|
|Insights from ICLR 2023|Gemini 3.0 Pro|1574|391K|886|2|0.000|0.000|
|Insights from ICLR 2024|Gemini 2.0 Flash|2260|441K|1.3K|20|0.000|0.000|
|PinchBench|Gemini 3.1 Pro|23|11K|3.1K|20|0.006|0.000|



## **F Complete Experiments for Ablation Studies** 

### **F.1 Effects of Local Reasoning Strategies** 

From the results in Table 20, we see that FoT consistently improves reasoning accuracy and efficiency under different local reasoning methods, compared to isolated agents using corresponding local reasoning methods. Complete perbenchmark accuracies are reported in Table 21. We tune the hyperparameters of our baselines and report the best average accuracies we obtain. Lower performance in some baselines does not imply that these methods are generally ineffective; rather, it suggests that their mechanisms are less suited to this setting of insight-library construction. For Agentic Context Engineering (ACE) [26], we observe a known limitation identified in prior work [26]: if the Reflector fails to extract meaningful insights from generated traces or outcomes, the constructed context may become noisy or even harmful. We set the maximum number of reflector rounds to 5. On mathematical datasets, ACE generates some misleading traces, leading to performance drops. FoT, in contrast, can help mitigate such effects. Evolving Prompts [28] has known drawbacks in terms of sensitivity to the in-context prompt template and stability. Despite these limitations, plugging them into FoT still improves performance. 

Table 20: Average accuracies over math problem solving tasks (LiveMathBench) and efficiency comparison under different settings. With the FoT-generated library, agents can achieve higher accuracies and efficiency relative to solving the problems in an isolated manner. Duplicated loops in reasoning refer to how many times the LLM generates repeated sentences in the reasoning <u>process.</u> 

|**Base Models**|**Algorithms**|**Local Reasoning**<br>**Methods**|**Average**<br>**Accuracy**|**# Generation**<br>**Tokens**|**#Duplicated loops**<br>**in reasoning**|
|---|---|---|---|---|---|
||Isolated Agents|Plain inference|0.537|6312|7|
|DeepSeek-R1<br>|FoT|Ours (Prompts 2-3)|**0.553**|**5886**|**6**|
|-Distill-Qwen-7B|Isolated Agents<br>FoT|Metacognitive [23]|0.464<br>**0.595**|6543<br>**5781**|4<br>**1**|
||Isolated Agents|Plain inference|0.846|891|3|
||FoT|Ours (Prompts 2-3)|**0.928**|**728**|**0**|
||Isolated Agents|ii 2|0.850|938|1|
|ii|<br>FoT|Metacogntve [3]|**0.905**|**718**|**0**|
|Gemn 3.0<br>P|Isolated Agents|HAt 25|0.850|716|0|
|ro|FoT|ypergens []|**0.912**|**682**|0|
||Isolated Agents|ACE 26|0.375|860|4|
||FoT|[]|**0.502**|**814**|**3**|
||Isolated Agents|Eli P 28|0.370|1014|7|
||FoT|vovng rompts []|**0.451**|**941**|**4**|



The results in Table 22 show that both our native FoT method and HyperAgents produce the most helpful libraries. The strong performance of HyperAgents suggests that local reasoning methods should be adaptable across domains, especially since FoT involves agents solving diverse tasks. This finding also motivates our future plan to enable each FoT agent to autonomously optimize its harness [53]. 

25 

Federation over Text: Insight Sharing for Multi-Agent Reasoning 

A PREPRINT 

Table 21: Accuracies of math problem solving (LiveMathBench) under different settings. With the FoT-generated library, agents can achieve higher accuracies relative to solving the problems in an isolated manner. 

|**Base Models**|**Algorithms**|**Local Reasoning**<br>**Methods**|AIME24|AIME25|AMC|CCEE|CNMO|WLPMC|V202412<br>Hard|V202505<br>Hard|**Avg**|
|---|---|---|---|---|---|---|---|---|---|---|---|
||Isolated Agents|Plain inference|0.500|0.400|0.674|0.841|0.722|0.273|0.524|0.360|0.537|
|DeepSeek-R1<br>|FoT|Ours (Prompts 2-3)|0.500|0.400|**0.717**|0.841|0.722|**0.364**|0.524|0.360|**0.553**|
|-Distill-Qwen-7B|Isolated Agents|Mtiti23|0.367|0.233|0.696|0.682|0.833|0.364|0.333|0.200|0.464|
||FoT|eacognve[]|**0.500**|**0.400**|0.696|**0.841**|0.833|**0.545**|**0.571**|**0.370**|**0.595**|
||Isolated Agents|Plain inference|0.967|0.933|0.935|0.864|0.889|0.727|0.762|0.690|0.846|
||FoT|Ours (Prompts 2-3)|**1.000**|**1.000**|0.935|**0.909**|**1.000**|**0.909**|**0.952**|**0.720**|**0.928**|
||Isolated Agents|Mtiti23|1.000|0.967|0.913|0.818|0.722|0.818|0.905|0.660|0.850|
|Gii 30|FoT|eacognve[]|1.000|0.967|**0.935**|**0.886**|**0.889**|**0.909**|**0.952**|**0.700**|**0.905**|
|emn .<br>P|Isolated Agents|HAt[25]|1.000|1.000|1.000|0.923|1.000|0.456|0.667|0.750|0.850|
|ro|FoT|ypergens|1.000|1.000|1.000|**1.000**|1.000|**0.545**|**1.000**|0.750|**0.912**|
||Isolated Agents|ACE[26]|0.600|0.389|0.563|0.591|0.250|0.167|0.182|0.256|0.375|
||FoT||**0.714**|**0.500**|**0.700**|0.591|**0.556**|**0.375**|**0.250**|**0.326**|**0.502**|
||Isolated Agents|Eli Pt28|0.233|0.167|0.630|0.659|0.389|0.546|0.143|0.192|0.370|
||FoT|vovng romps[]|**0.300**|**0.233**|**0.674**|**0.796**|**0.556**|**0.636**|**0.191**|**0.220**|**0.451**|



Table 22: Paper guidance rate in setting 2 where base models are Gemini-2.0-Flash under different local reasoning methods. Agents read ICLR 24 paper and check whether ICLR 25 papers can be guided by the insight library. 

|**Algorithms**|**Local Reasoning**<br>**Methods**|**Poster**|**Spotlight**|**Oral**|**All**|
|---|---|---|---|---|---|
|Isolated Agents|Plain inference|0.7|0.5|0.8|0.7|
||Ours (Prompts 2-3)|82.4|82.1|82.2|82.4|
||Metacognitive Reuse[23]|60.6|56.6|57.7|60.0|
|FoT|HyperAgents[25]|82.7|80.5|81.2|82.4|
||Agentic Context Engineering[26]|5.43|6.05|7.98|5.64|
||Evolving Prompts[28]|14.1|12.6|12.7|13.8|



### **F.2 Effects of Heterogeneous Local and Server Agent Models** 

We report in Table 23 the performance when the local agents are DeepSeek (or Gemini 3.0 Pro) and the server model is Gemini 3.0 Pro (or DeepSeek), respectively. Although using DeepSeek as the server for Gemini 3.0 Pro local agents performs worse than using Gemini 3.0 Pro as the server, it still outperforms the single-agent baseline. 

For the task of research insight discovery, we replace the server agent from Gemini 2.0 Flash with Gemini 3.0 Pro. The results Table 24 confirm our conclusion that a stronger server LLM further improves performance. 

Table 23: Mathematical problem-solving performance using FoT-generated insight libraries under heterogeneous client and server LLM configurations, compared to isolated agents, with improvements highlighted in bold. 

|Algorithms|Agent LLM|Server LLM|AIME24|AIME25|AMC|CCEE|CNMO|WLPMC|V202412<br>Hard|V202505<br>Hard|Avg|
|---|---|---|---|---|---|---|---|---|---|---|---|
|Isolated Agents|DeepSeek|–|0.500|0.400|0.674|0.841|0.722|0.273|0.524|0.360|0.537|
|FoT|DeepSeek|Gemini 3.0 Pro|**0.700**|0.400|**0.717**|0.841|0.722|**0.364**|0.524|**0.370**|**0.580**|
|Isolated Agents|Gemini 3.0 Pro|–|0.967|0.933|0.935|0.864|0.889|0.727|0.762|0.690|0.846|
|FoT|Gemini 3.0 Pro|DeepSeek|0.967|0.933|0.935|**0.886**|0.889|**0.909**|**0.857**|0.670|**0.881**|



Table 24: Paper guidance rate using FoT-generated insight libraries under heterogeneous client and server LLM configurations. 

|Algorithms|Agent LLM|Server LLM|Poster|Spotlight|Oral|All|
|---|---|---|---|---|---|---|
|Isolated Agents|Gemini 2.0 Flash|–|60.7|60.5|60.6|60.7|
|FoT|Gemini 2.0 Flash|Gemini 2.0 Flash|82.4|82.1|82.2|82.4|
|FoT|Gemini 2.0 Flash|Gemini 3.0 Pro|**86.7**|**82.6**|**86.9**|**86.3**|



We also consider the setting where multiple agents solve the same task using different models. We have 4 agents, each agent picks a different model, and they all solve the same LiveMathBench Hard 2025 benchmark. Although FoT is 

26 

Federation over Text: Insight Sharing for Multi-Agent Reasoning 

A PREPRINT 

primarily designed to aggregate knowledge across diverse tasks, it still provides benefits in this scenario. As shown in Table 25, FoT improves performance even when agents operate on identical tasks, reflecting one potential realistic setting where multiple agents collaborate on the same problem. Since leveraging multiple agents to collaboratively solve a single task is not our focus, we do not conduct further comparisons with such baselines. 

Table 25: Accuracy on LiveMathBench Hard 2025 where there are four agents in total and each agent uses a different model. We can see that FoT can bring improvements over isolated agents. The server agent uses Gemini 3.1 Pro. 

|Algorithms|Gemini 3.1 Pro|Gemini 2.5 Flash|Gemini 2.5 Flash Lite|Gemini 2.5 Pro|
|---|---|---|---|---|
|Isolated Agents|0.720|0.420|0.360|0.400|
|FoT (Round 2)|0.710|0.420|0.400|0.320|
|FoT (Round 3)|0.720|**0.530**|**0.440**|**0.440**|



### **F.3 Effects of Insight Library Size** 

Here, we demonstrate the effects of insight library size on the ML research insight discovery application. Recall that one baseline is isolated reasoning, and the other baseline is to query the ML research insights through a RAG system, where we store old papers in an external database as reference. In Prompt 3, we replace the phrase ’proper number’ with explicit quantities (e.g., 10, 50, 100). From Figure 9, we can see that as the number of insights increases, the guidance rate of all three approaches increases, and FoT outperforms the other two. We note that when FoT does not have strict constraints on the total number of insights, it will automatically arrive at a good tradeoff between the number of insights and performance (20), since the performance gain increases slowly from 20 insights to 200. We can see that RAG can be effective in encoding external information, but it requires maintenance of a potentially huge datastore (storing all the previous papers), which takes more space than a lightweight insight library. 


![](P067_images/P067.pdf-0027-07.png)

### Figure analysis

Purpose: The figure compares how the number of generated insights affects the guidance rate for three methods—FoT, isolated agents, and RAG—when generating research insights intended to cover core contributions of ICLR 2025 papers.

Structure and labels:
- The figure contains four side-by-side line charts titled **Oral**, **Spotlight**, **Poster**, and **All**.
- Shared x-axis: **Number of Insights**, with labeled settings 10, 20, 50, 100, and 200.
- Shared y-axis: **Guidance Rate (%)**, ranging from 0 to 100.
- Legend:
  - **FoT (Ours)**: blue line with circular markers.
  - **Isolated**: orange line with square markers.
  - **RAG**: green line with triangular markers.

Direct visual observations by panel:
- **Oral**: FoT rises sharply from low performance at 10 insights to above 80% at 20 insights, then increases more gradually and remains around the high-80s to low-90s range. RAG improves from roughly the low-20s to around 70% by 200 insights. Isolated agents improve more slowly and remain below RAG and FoT at larger insight counts.
- **Spotlight**: FoT starts relatively low at 10 insights but jumps to above 80% at 20 insights and stays near 90% afterward. RAG steadily improves and remains above isolated agents at most larger insight counts. Isolated agents dip at 20 insights, then improve through 200 insights.
- **Poster**: FoT increases strongly at 20 insights and remains the top method across all larger settings, reaching roughly around 90% by 100–200 insights. RAG begins near isolated at 10 insights, dips slightly at 20, then rises sharply by 100 and 200 insights. Isolated agents improve gradually but remain below FoT and below RAG at high insight counts.
- **All**: FoT shows the clearest early gain, moving from roughly the high-20% range at 10 insights to above 80% at 20 insights, then increasing slowly toward the low-90% range. RAG and isolated agents both improve with more insights, with RAG overtaking isolated at larger insight counts.

Comparisons and trends:
- Across all panels, increasing the number of insights generally increases guidance rate for all methods, though not always monotonically at every point.
- FoT consistently outperforms isolated agents and RAG over most insight-library sizes, especially from 20 insights onward.
- The largest visual jump for FoT occurs between 10 and 20 insights, after which performance gains appear to saturate.
- RAG can approach FoT in some high-insight settings, particularly for Poster and All, but generally requires more insights to achieve high guidance rates.
- Isolated agents show the weakest overall performance and slower improvement with insight count.

Connection to surrounding text:
- The figure supports the paper’s claim in Section F.3 that larger insight libraries improve guidance rate and that FoT provides stronger insight quality than isolated reasoning or RAG.
- It visually reinforces the text’s interpretation that FoT reaches a favorable tradeoff around a relatively small number of insights, while additional insights beyond that yield slower gains.
- The comparison with RAG aligns with the surrounding discussion that retrieval-based use of old papers can help but may require a much larger external datastore than FoT’s lightweight insight library.

Uncertainty:
- The chart does not print exact values next to markers, so numerical readings should be treated as approximate visual estimates rather than exact extracted measurements.


Figure 9: Comparison of FoT, isolated agents, and RAG in their ability to generate insights that can cover the core contributions of ICLR 2025 papers (guidance rate) under varying numbers of generated insights. Local agents use Gemini-2.0-Flash as the base LLM and are fed with ICLR 2024 papers as input. FoT generates higher-quality insights that better guide future research directions while requiring less input text, hence reducing token consumption. 

### **F.4 Effects of Agent Participation** 

We further analyze the impact of varying the number of participating agents in FoT under two settings. In Figure 10, each agent reads one paper while we vary the total number of papers, simulating partial participation as in crossdevice federated learning. For each setting with 25%, 50%, and 75% local agents, we repeat the experiment three times, each with randomly selected papers to mitigate variation in paper quality. In Figure 11, we fix the total number of papers across agents but vary how many papers each agent reads before generating reasoning traces. When we use 2,260 agents, each agent generates reasoning traces after reading a single paper, whereas with 91 agents, each agent generates reasoning traces after reading 25 papers. We set the max insight library size to 200. For ICLR 2024 papers, we partition them across agents via primary research area so that each agent takes as input papers from the same areas. We observe that the number of agents does not significantly impact performance. However, assigning all papers to a single agent can result in an input size that exceeds the model’s context window when performing local reasoning. Table 26 and Table 27 present the performance on each benchmark for the two experimental settings in Table 7. In Table 26, all results except those on the diagonal from the top-left to the bottom-right correspond to evaluations where the benchmark is not used during insight library construction, and performance improvements are observed. In Table 27, the diagonal entries represent cases where the benchmark is not used during insight library construction, and improvements are also observed. These results confirm that, in FoT, the insight library can be effectively used by newly participating agents, as well as by agents that did not contribute to its construction, to improve performance. 

27 

Federation over Text: Insight Sharing for Multi-Agent Reasoning 

A PREPRINT 

Table 26: Mathematical problem-solving performance on each benchmark for the ’Include One’ experiment in Table 7. Improvements over the single-agent baseline are bolded. 

|Benchmark participating<br>agent works on|AIME24|AIME25|AMC|CCEE|CNMO|WLPMC|V202412<br>Hard|V202505<br>Hard|Avg|
|---|---|---|---|---|---|---|---|---|---|
|AIME24|0.967|**0.967**|0.935|0.864|**0.944**|0.727|**0.810**|0.690|**0.863**|
|AIME25|0.967|0.933|0.935|0.864|**0.944**|0.727|**0.857**|0.690|**0.865**|
|AMC|**1.000**|0.933|0.935|0.864|0.889|0.727|**0.857**|0.680|**0.861**|
|CCEE|**1.000**|**0.967**|0.935|**0.909**|**0.944**|0.727|**0.857**|**0.700**|**0.880**|
|CNMO|0.967|0.933|0.935|0.864|0.889|0.727|**0.810**|**0.700**|**0.853**|
|WLPMC|0.967|0.933|0.935|0.864|0.889|0.727|**0.857**|0.690|**0.858**|
|V202412 Hard|0.967|0.933|0.935|0.864|0.889|0.727|**0.857**|**0.700**|**0.859**|
|V202505 Hard|**1.000**|0.933|**1.000**|**0.909**|**0.944**|**0.818**|**0.857**|**0.720**|**0.898**|



Table 27: Mathematical problem-solving performance on each benchmark for the ’Exclude One’ experiment in Table 7. Improvements over the single-agent baseline are bolded. 

|Benchmark non-<br>participating agent<br>works on|AIME24|AIME25|AMC|CCEE|CNMO|WLPMC|V202412<br>Hard|V202505<br>Hard|Avg|
|---|---|---|---|---|---|---|---|---|---|
|AIME24|0.967|**1.000**|0.913|0.864|0.889|**0.818**|**0.905**|**0.720**|**0.885**|
|AIME25|0.967|0.967|0.913|**0.909**|**0.944**|**0.818**|**0.857**|0.690|**0.883**|
|AMC|**1.000**|**0.967**|0.935|**0.909**|**1.000**|0.727|**0.905**|0.690|**0.892**|
|CCEE|0.967|0.933|0.935|**0.886**|**1.000**|**0.818**|**0.857**|0.680|**0.885**|
|CNMO|0.967|0.933|0.913|**0.909**|0.889|0.727|**0.857**|0.690|**0.861**|
|WLPMC|0.967|**0.967**|0.935|**0.909**|**0.944**|**0.818**|**0.857**|0.680|**0.885**|
|V202412 Hard|**1.000**|**0.967**|0.935|**0.909**|**0.944**|0.727|**0.857**|0.690|**0.879**|
|V202505 Hard|0.967|0.933|0.913|**0.886**|0.889|0.727|**0.857**|**0.710**|**0.860**|



Table 28: Changes in average costs relative to the Isolated Agents baseline and FoT where all agents participate. Each row corresponds to one agent, identified by the benchmark it works on. **Include One** : The insight library is built from this agent alone. **Exclude One** : The insight library is built from all agents except this one. 

||Include|One|Exclude|One|
|---|---|---|---|---|
|Agent|∆Isolated<br>Agents|∆FoT|∆Isolated<br>Agents|∆FoT|
|AIME24|+0.15|_−_2.57|+1.15|_−_1.57|
|AIME25|+0.14|_−_2.58|+1.16|_−_1.56|
|AMC|+0.15|_−_2.57|+1.26|_−_1.46|
|CCEE|+0.15|_−_2.57|+1.23|_−_1.49|
|CNMO|+0.13|_−_2.59|+1.04|_−_1.68|
|WLPMC|+0.13|_−_2.59|+1.07|_−_1.64|
|V202412 Hard|+0.25|_−_2.47|+1.81|_−_0.91|
|V202505 Hard|+0.12|_−_2.60|+0.99|_−_1.73|



28 

Federation over Text: Insight Sharing for Multi-Agent Reasoning 

A PREPRINT 

Table 28 compares the costs of the two settings with those of FoT and isolated agents. The costs of FoT and the two settings include agent inference, reasoning trace extraction, and server-side aggregation. In the Include-One setting, creating an insight library requires only about $0.15 in additional cost. Once constructed, this library can also benefit newly participating agents, improving their performance while reducing inference token usage. Therefore, the benefit of the insight library is persistent: agents that did not participate in library construction can still leverage it to achieve higher accuracy, use fewer tokens, and reduce long-term costs. 

## **G Complete Prompts** 

### **G.1 Prompts for Our Instantiation of FoT** 

Prompt 1 shows the prompt used by agents when an insight library is available. In Sections 4.1, 4.2 and 4.4, we directly apply this prompt to generate responses. In Section 4.3, we incorporate this prompt into the OpenClaw system prompt by specifying that “available insights are stored in `insight.md` .” When no insight library is provided (i.e., isolated agents), the prompt reduces to “Problem: _{_ problem _}_ ,” where _{_ problem _}_ corresponds to the original dataset query. We put each problem prompt in Appendix G.2. 

Prompt 1: Generating solution 

```
AvailableInsightstoGuideYourSolution:
{insightlibrary}
---
INSTRUCTIONS:Reviewtheinsightsaboveandactivelyapplytherelevant
techniquesfrominsightstosolvethisproblem.Considerwhichinsightscan
helpyouapproachtheproblemmoreeffectively.
Problem:{problem}
```

Prompt 2 is used for solution reflection, which is the first part of ’Step 2: Local reasoning and self-reflection’ (Figure 1), before an agent generates reasoning traces. 

Prompt 2: Reflecting on Solution 

```
Analyzethesolutionbelowtoextractproceduralknowledgethatreflectsthe
reasoningtraces.
```


![](P067_images/P067.pdf-0029-11.png)


Figure 10: Paper guidance rate across different levels of local agent participation where each agent reads one paper. Guidance rate increases as participation increases (i.e., more input tasks). 


![](P067_images/P067.pdf-0029-13.png)


Figure 11: Paper guidance rate across different numbers of total agents, where the total number of papers read is fixed at 2260. The guidance rates remain high under different numbers of agents. 

29 

Federation over Text: Insight Sharing for Multi-Agent Reasoning 

A PREPRINT 

```
Problem:
{problem}
Step -by -StepSolution:
{solution}
Yourtask:Extractthefundamentaltechniquesusedinresolutionthatcanbe
packagedasreasoningtraces.Focuson:
1.Whatstep -by -stepprocedureswereused?Howcantheseberepeated?
2.Whatconditionsdeterminedwhichapproachtouse?Whenshouldeachtechnique
apply?
3.Whatmethods ,strategies ,orworkflowscanbeappliedtosimilarproblems?
4.Whatmadethisapproacheffective?Whatshouldsomeoneknowtouseit
correctly?
5.Whattypesofproblemswouldbenefitfromthesetechniques?
Outputyouranalysiscovering:
###I.ProceduralKnowledge
-Breakdownthesolutionintoclear ,repeatableprocedures
-Theextractedtracesshouldbeconcretesolutionsratherthangeneral
principles.
###II.ReusableTechniquesandMethods
-Listspecifictechniques ,strategies ,orworkflowsused
-Thetechniquesshouldbesolidonpracticalquestionsratherthanverygeneral
andhigh -levelprinciples.
-Foreachtechnique ,identify:
*Whenitshouldbeused(conditions/triggers)
*Howitwasapplied(concretesteps)
*Whyitwaseffective(insights)
*Whatproblemsitcouldsolve( applicability )
###III.CriticalInsightsandGuidelines
-Whatkeyinsightsmadethissolutionwork?
-Whatcommonpitfallsshouldbeavoided?
-Whatvariationsoredgecasesshouldbeconsidered?
Focusonextractingactionable ,proceduralknowledgethatcanbepackagedas
reusableinsightsforsimilarproblems.
```

Prompt 3 is used for the generation of reasoning traces, which is the second part of ‘Step 2: Local reasoning and self-reflection’ (Figure 1). The description includes our definitions of reasoning traces. 

Prompt 3: Generating Reasoning Trace 

```
Extractreasoningtracesfromthesolutionbelow.Analyzethesolutionand
reflectiontoidentifyconcrete ,actionabletracessothatsimilarproblems
canbesolvedviathetraces
Problem:{problem}
Solution:{solution}
Reflection:{reflection}
** YourTask :**
Identifyandextractallreusablereasoningtraces ,techniques ,andmethodsused
inthesolution.Eachtraceshouldbeaconcreteprocedurethatcanguide
someonetosolvesimilarproblems.
```

30 

Federation over Text: Insight Sharing for Multi-Agent Reasoning 

A PREPRINT 

```
** WhatMakesaGoodReasoningTrace :**
-Aspecifictechniqueormethodthatwasusedinthesolution.
-Somethingthatcanbeappliedtosimilarproblems ,notjustthisone.
-Includesguidanceonwhenandhowtouseitwithclearstepsthatcanbe
followedifnecessary.
-Notrepetitionofalreadywell -knownorcommonlyadoptedtechniques.
-Nottoogeneralandhigh -levelbutcontainsactionableproceduralknowledge.
** DescriptionMustInclude :**
1.** Coreidea **:Thefundamentalconceptofwhatthistraceisabout.Whatis
themaintechniqueormethod?Whatdoesitdo?
2.** Whentouse **:Explainwhenthisskillshouldbeapplied.Whattypesof
problems?Whatconditionsmustbemet?Whatsituationstriggerthisskill?
** OutputFormat(SimpleJSON):**
OutputasimpleJSONobjectwithskillnamesaskeysanddescriptionsasstring
values:
{{" trace_name ":"description "}}
FormatRules:
-UsevalidJSONformat
-Eachtracenamemuststartwith"trace_"
-KeepJSONsimple-nonestedobjects ,justkey -valuepairs
-Escapequotesindescriptionswithbackslash:\\"
** Example :**
{{
"tracepolynomialFactoring ":"Themajorideaishowwecanturnapolynomial
intoaproductofsimplerexpressions.Thisskillisparticularlyusefulfor
quadraticandhigher -degreepolynomialequationswherefactoringcansimplify
theproblem.Factoringreducescomplexpolynomialstosimplerequations.When
solvingequationswithpolynomialexpressionsthatcanbefactored ,especially
whenthepolynomialhasrecognizablepatternslikedifferenceofsquares
(a^2-b^2),perfectsquaretrinomials(a^2+2 ab+b^2),orcommonfactors.
"tracedepthFirstSearchImplementation ":"Thisalgorithmisessentialfor
problemsinvolvingpathfinding ,cycledetection ,topologicalsorting ,
connectedcomponents ,orexploringallpossiblesolutionsinasearchspace.
DFSexploresdepthbeforebreadth ,usingstack -basedrecursionorexplicit
stack.Itismemory -efficientfordeepstructuresandnaturallyhandles
backtracking.Thevisitedsetpreventsinfiniteloopsandredundantwork.DFS
isthefoundationformanygraphalgorithmsincludingtopologicalsort ,
stronglyconnectedcomponents ,andmazesolving.Whenyouneedtoexploreor
traverseagraph ,tree ,ornestedstructuresystematically ,goingasdeepas
possiblebeforebacktracking.UseDFSwhenyouneedtovisitallnodesina
connectedcomponent ,findpathsbetweennodes ,detectcycles ,orexplore
recursivestructureslikefilesystems ,nesteddata ,orgamestates."
}}
** OutputyourresponseasavalidJSONobjectonly :**
```

Prompt 4 is used for clustering and identifying connections between reasoning traces, as part of ‘Step 4: Aggregate traces to update the library’ in Figure 1, before updating the insight library. 

Prompt 4: Constructing Relationship between Reasoning Traces 

```
Youareanalyzingacollectionofreasoningtracesgeneratedforproblem -solving.
Understandtheirrelationshipsandstructureandbuildaprofileoftheir
relationships.
```

```
** Collected{len(insight_store)}tracesintotal :**
```

31 

Federation over Text: Insight Sharing for Multi-Agent Reasoning 

A PREPRINT 

```
Note:ThiscollectionincludesALLtracesfromallproblemswithout
deduplication.Similarnameswithdifferentindices(e.g.,_001 ,_002)
representdifferentoccurrencesthatmayhavevariationsintheirdescriptions .
{ insights_text}
** YourTask :**
Analyzethesetracesandbuildaprofileoftheirrelationships :
1.** IdentifyClusters **:
Grouprelatedtracesthatshare:
-Resolvethesameorsimilarproblem
-Similarapproachesortechniques
-Nearlyidenticaltraces(e.g.,sametracewithminorvariationsin
descriptionorparameters)
-Tracesinthesameclustershouldbehighlysimilar.
2.** BuildTraceRelationships **:
Recordallimportantrelationships-tracesdon ’texistinisolationandbuilda
relationshipgraphthatrecords:
-** Prerequisiterelationships **:Tracesthatmustbelearned/usedbefore
others
-** Compositionrelationships **:Tracesthatcanbechained/composedtogether
-** Alternativerelationships **:Differentapproachestothesameproblem
-** Complementaryrelationships **:Tracesthatworkbettertogetherthan
individuallyused
-** Derivationrelationships **:Tracesderivedfromorbasedonothers
-** Similarrelationships **:Tracesthataresimilarbutnotidentical
Maprelationshipsbetweentraceswithinclustersandacrossclusters.
#OutputFormat:
{{
"clusters ":[
{{
"cluster_id ":0,
"cluster_name ":"Domain/ThemeName",
"traces ":[" name1","name2","name3 "],
"theme ":"Whatisthehigh -leveltechnicalideaofthetracesinthis
cluster ?",
}}
],
" relationships ":[
{{
"trace_a ":"trace_name1",
"trace_b ":"trace_name2",
" relationship_type ":
"prerequisite/complementary/alternative/similar/derived_from /
composes_with",
"description ":"HowthesetracesrelatetoeachotherandWhy"
}}
]
}}
** OutputyouranalysisasJSONonly :**
```

The output relationship dictionary from Prompt 4 is double-checked and formatted as valid JSON to facilitate downstream extraction and processing. Prompt 5 is used for updating the insight library, as the second part of ‘Step 4: Aggregate traces to update the library’ in Figure 1. 

Prompt 5: Building Insight Library 

```
** YourTask :**
```

32 

Federation over Text: Insight Sharing for Multi-Agent Reasoning 

A PREPRINT 

```
Youareextractingfundamentalinsightsfromacollectionofproblem -solving
traces.
** OutputRequirements(STRICT):**
1.ReturnEXACTLYonevalidJSONobjectandnothingelse.
2.DoNOToutputmarkdowncodefences.
3.DoNOToutputexplanations ,notes ,reasoning ,prefixes ,suffixes ,or‘<think >‘
content.
4.DoNOToutputlist/arrayattop -level.
5.Everykeymuststartwith"insight_ ".
6.Everyvaluemustbeasinglestring.
7.Nonestedobjects ,nonestedarrays.
** RequiredJSONshape :**
{{
" insight_name1 ":"descriptionstring",
" insight_name2 ":"descriptionstring"
}}
** FormattingRules :**
-UsevalidJSONsyntaxonly.
-Keeptop -levelaskey -valuepairsonly.
-Escapequotesindescriptionswithbackslash:\\"
-Ifuncertain ,stilloutputavalidJSONobject(possiblywithfewerinsights),
neverfreetext.
Yourgoalistoextractacomprehensivesetoffundamental ,cross -domaininsights
thatcanbederivedandappliedbeyondtheiroriginaldomainandmeetthe
followingrequirements:
-Combinepreviousinsights(ifany):{ existing_encyclopediaif
existing_encyclopediaelse"None "}withnewinsights.
-Extractyourinsightsbasedonallclientreasoningtraces:
{ all_insights_text }.Thesetracesarederivedfromsolvingspecificproblems
(bottom -upapproach)
-Useclustersofreasoningtraces:{ clusters_textifclusters_textelse"None
identified "}tohelporganize.
-Userelationshipsbetweentraces:{json.dumps(profiling.get(’relationships ’,
[]),indent =2)ifisinstance(profiling ,dict)else"Noneidentified "}tohelp
organization
-Yourtaskistoextractmulti -disciplinary ,fundamentalknowledge(top -down
approach)whichcanbegeneralizedtomulti -domainproblem -solving.
-TheextractedinsightsshouldbeabletoDERIVEandGUIDEtheuseofthe
collectedinsights
-Theextractedinsightscannotbetoogeneral.Theyarenotsupposedtobe
knowledgewhichcanbeappliedtoanyproblem.Theyshouldbefundamental
knowledgetoparticularseveraldomainsbutspecific.
-Youshouldextractpropernumberofinsights.Nottoofew.Nottoomany.Donot
oversimplifyorbetoodetailed.
-DONOTover -mergeinsights.
Insightsshouldhavefollowingproperties:
1.** ExtractReusablePrimitives **:
-ForEACHcluster ,extractmultiplefundamentalinsightscapturingcore
essenceandvariations(DONOTover -merge)
-Identifycross -domainpatternsthatapplytomultiplefields
-Createreusable ,composableprimitivesspecificenoughtobeactionable
2.** Knowledgetoinclude **:
-** FundamentalLevel **:Coreprinciplesunderlyingmultipledomains
-** GeneralLevel **:Broadtechniquesforrelatedproblemtypes
-**Cross -Domain **:Insightstransferablebeyondoriginfield
3.** PreserveWhileGeneralizing **:
-Createfundamentalversionsthatcanguide/deriveoriginalinsights
-Maintainimportantvariationsratherthancollapsingintosingleinsight
```

33 

Federation over Text: Insight Sharing for Multi-Agent Reasoning 

A PREPRINT 

|`4. ** Description`<br>`Format :**`<br>`Each`<br>`description is a single`<br>`string`<br>`containing:`<br>`- What the`<br>`insight is and how it solves`<br>`problems`<br>`- When to use: problem types , conditions , triggers (be comprehensive`<br>`and`<br>`specific)`|
|---|
|`** Example 1 - Transformer`<br>`Architecture :**`|
|`Input`<br>`reasoning`<br>`traces:`<br>`- reasoning`<br>`trace`<br>`VisionTransformerImageClassification : "I need to classify`<br>`medical X-ray images`<br>`into`<br>`disease`<br>`categories. CNNs aren ’t working`<br>`well - they`<br>`can ’t capture`<br>`relationships`<br>`between`<br>`distant`<br>`regions`<br>`like how fluid in the`<br>`lower`<br>`right`<br>`lung`<br>`might`<br>`relate to heart`<br>`enlargement. Let me try Vision`<br>`Transformer (ViT). I’ll divide`<br>`each X-ray into 16x16`<br>`patches - a 224 x224`<br>`image`<br>`gives 196`<br>`patches. Each`<br>`patch`<br>`becomes`<br>`like a token in NLP. I flatten`<br>`each to a`<br>`256-dim vector. Since`<br>`transformers don ’t know`<br>`spatial`<br>`positions , I add`<br>`position`<br>`embeddings so the model`<br>`knows`<br>`patch [0 ,0] is top -left. I prepend a`<br>`[CLS] token to gather`<br>`global`<br>`info. Feeding`<br>`through 12 transformer`<br>`encoder`<br>`layers - the self -attention`<br>`lets`<br>`every`<br>`patch`<br>`attend to every`<br>`other`<br>`patch`<br>`directly , so patch [2,5] can look at patch`<br>`[10 ,12] even`<br>`though they ’re far`<br>`apart`<br>`spatially. This is exactly`<br>`what I need! After 12 layers , I extract`<br>`the`<br>`[CLS] token and feed to MLP`<br>`classifier. Training on 50k chest X-rays: 94.2%`<br>`accuracy , beating`<br>`ResNet -50’s 89.3%. The`<br>`attention`<br>`maps show it ’s correctly`<br>`attending to both`<br>`lungs`<br>`simultaneously`<br>`for`<br>`pneumonia`<br>`detection , linking`<br>`heart`<br>`size to lung`<br>`fluid - this cross -region`<br>`reasoning is what CNNs miss. The key:`<br>`treating`<br>`image`<br>`patches as tokens`<br>`with self -attention`<br>`enables`<br>`global`<br>`spatial`<br>`reasoning ."`|
|`- reasoning`<br>`trace`<br>`TransformerNextWordPrediction : "I’m building`<br>`autocomplete`<br>`for a`<br>`text`<br>`editor. The`<br>`challenge: predict`<br>`next word`<br>`given`<br>`arbitrary -length`<br>`context.`<br>`RNNs`<br>`struggle`<br>`with long`<br>`sequences - the hidden`<br>`state`<br>`forgets`<br>`earlier`<br>`context.`<br>`Let me use a transformer`<br>`decoder. I tokenize ’The cat sat on the ’ using`<br>`WordPiece`<br>`-> tokens [254, 8901 , 4523 , 651, 278].`<br>`Convert`<br>`each to 512-dim`<br>`embedding`<br>`and add`<br>`positional`<br>`encodings. Critical`<br>`part: causal`<br>`masking so the`<br>`model can ’t cheat by seeing`<br>`future`<br>`words. When`<br>`predicting`<br>`token at position 4,`<br>`it should`<br>`only see 0-3. I implement`<br>`lower -triangular`<br>`attention`<br>`mask.`<br>`Processing`<br>`through 6 decoder`<br>`layers`<br>`with`<br>`masked self -attention. At position 4`<br>`(’the ’), attention`<br>`computes`<br>`similarity`<br>`between`<br>`its query and keys of previous`<br>`words. It attends`<br>`strongly to ’sat ’ (0.8) and ’on ’ (0.7) , weakly to ’cat ’`<br>`(0.2). Using 12 heads`<br>`helps - different`<br>`heads`<br>`capture`<br>`different`<br>`patterns:`<br>`head -2 learns`<br>`syntax (preposition+article), head -5 learns`<br>`semantics`<br>`(actions+objects), head -8 learns long -range`<br>`dependencies . After`<br>`final layer ,`<br>`project`<br>`last`<br>`hidden`<br>`state`<br>`through 50k-dim`<br>`softmax. For ’the ’: top`<br>`predictions`<br>`are ’mat ’ (0.73) , ’floor ’ (0.12) , ’rug ’ (0.08). Deployed in production - users`<br>`accept top -3 suggestion`<br>`85\% of the time , reducing`<br>`typing by 40\%.`<br>`Transformer ’s self -attention`<br>`captures`<br>`context`<br>`way better`<br>`than RNN ’s sequential`<br>`processing ."`|
|`Output`<br>`aggregated`<br>`insight:`<br>`{{`|
|`" insight_transformerArchitecture ": "This`<br>`fundamental`<br>`neural`<br>`network`<br>`architecture`<br>`applies`<br>`across`<br>`natural`<br>`language`<br>`processing , computer`<br>`vision , time`<br>`series`<br>`analysis , graph`<br>`neural`<br>`networks , and multi -modal`<br>`learning. This`<br>`insight`<br>`is essential`<br>`for modern AI applications`<br>`including`<br>`language`<br>`models , image`<br>`processing , code`<br>`generation , and`<br>`scientific`<br>`computing. When you need to`<br>`capture`<br>`relationships`<br>`between`<br>`all`<br>`elements`<br>`simultaneously (self -attention),`<br>`you ’re working`<br>`with`<br>`sequences of variable`<br>`length , you need`<br>`parallel`<br>`processing`<br>`of sequences , or when the`<br>`problem`<br>`involves`<br>`understanding`<br>`context`<br>`and`<br>`relationships. Details: 1) Design`<br>`input`<br>`representation - convert`<br>`your data`<br>`into`<br>`embeddings (token`<br>`embeddings`<br>`for text , patch`<br>`embeddings`<br>`for images , node`<br>`embeddings`<br>`for graphs), add`<br>`positional`<br>`encodings to preserve`<br>`sequence`<br>`information , and`<br>`prepare`<br>`input for`<br>`transformer`<br>`blocks 2) Create`<br>`models`<br>`with`<br>`transformer`<br>`blocks 3) Apply task -specific`<br>`architecture - use encoder -only for`|



34 

Federation over Text: Insight Sharing for Multi-Agent Reasoning 

A PREPRINT 

```
understanding(BERT ,ViT),decoder -onlyforgeneration(GPT),or
encoder -decoderfortranslation"
}}
** Example2-Surface -EnhancedRamanSpectroscopy :**
Inputreasoningtraces:
-reasoningtraceSERSMedicalDetectionR6G :"Ineedtodetectcancerbiomarkersin
bloodatincrediblylowconcentrations-10^ -12M,likefindingmoleculesina
swimmingpool.ELISAonlygoesto10^ -9M,notsensitiveenoughforearly
diagnosis.LetmetrySERS-Surface -EnhancedRamanSpectroscopy .Metal
nanoparticlescreatehugeEMfieldenhancements .Isynthesize60nmgold
nanoparticlesviacitratereduction.At785nmlaser ,thesehaveplasmon
resonanceamplifyinglocalfieldby~10^6.ButIneedselectivitytoo-can ’t
detecteverything.SoIfunctionalizethegoldwithanti -PSAantibodiesfor
prostatecancer.WhenIaddpatientserum ,onlyPSAproteinsbind.Here ’sthe
cleverpart:IaddR6G(Rhodamine6G)reportermolecules.R6Ghasenormous
Ramancross -sectionandwhenitsitsinnanogapsbetweengoldparticles ,field
enhancementshootsto10^8or10^10.Incubate30minforPSAbinding ,addR6G
whichsticksnearboundPSA.Hitwith785nmlaserat5mW-Isee
characteristicR6Gpeaksat1650 ,1510 ,1310cm^-1.Peakintensitydirectly
proportionaltoPSAamount.Integrate60secforgoodSNR.Comparingto
calibration:detectingPSAat0.1ng/mL-that ’s10 ,000xmoresensitivethan
ELISA!Onclinicalsamples ,detectedprostatecancer3-6monthsearlierthan
conventionaltests.Thebreakthrough :combiningselectiveantibodyrecognition
withSERSamplificationgivessingle -moleculesensitivitywhilemaintaining
specificity ."
-reasoningtraceSERSPollutantDetection :"Monitoringriverwaterforpesticides.
EPAlimitformalathionis0.1ppbbutstandardchromatographyneeds1ppb
minimum.Ineed10xbetterforearlywarning.SERSmightwork.Insteadof
sphericalparticles ,I’llfabricatesilvernanorodarrays-sharptipscreate
hotterhotspotsthanspheres.Usingobliqueangledeposition:80nmnanorods
with4:1aspectratioonsilicon.Gapsbetweenrodsonly5-10nm-perfectfor
trappingmolecules.Icalculateenhancementshouldhit10^10at532nm.Collect
riverwater ,filterthrough0.2\ mumtoremovedebrisandbacteria.Drop50
\muLontonanorodsubstrate.During5-minadsorption ,pesticidemolecules
diffuseintonanogaps.Smallgapmeansmoleculesguaranteedinenhancement
zone(<10nmfrommetal).Rinsegently-removesinterferingorganics/saltsbut
leavesadsorbedpesticides.Excitewith532nmat2mW ,matchingsilverplasmon
peak.Evenat0.01ppbmalathion ,clearpeaksat1440cm^-1(P=Sstretch),
1080cm^-1(P-O-C),640cm^-1(C-S).Measuring1440peakheightvscalibration
standardsforquantification .Tested50riversites ,cross -validatedagainst
LC -MS:R^2=0.97correlation.Bestpart:dothisinfieldwithportableRaman-
nolabneeded.Real -timemonitoringat10xbelowregulatorylimits.The
nanorodgeometryiscritical-thosesharptipsandtightgapspush
enhancementto10^10."
```

```
Outputaggregatedinsight:
{{
```

```
" insight_surfaceEnhancedRamanSpectroscopy ":"Thispowerfultechniqueapplies
acrossanalyticalchemistry ,materialsscience ,biosensing ,pharmaceutical
analysis ,environmentalmonitoring ,andforensics.Thetechniqueachieves
single -moleculesensitivity(10^6 -10^11enhancement)whileprovidingmolecular
structuralinformationthroughvibrationalfingerprints .Whentouse:Whenyou
needultra -sensitivedetectionbelowconventionalanalyticallimits ,whenyou
wantlabel -freemolecularidentification ,whenanalyzingtracecontaminantsor
biomarkers ,orwhenfield -portablereal -timeanalysisisrequired.Common
steps:1)PrepareSERS -activesubstrate-synthesizeplasmonicnanostructures
(gold/silvernanoparticles ,nanorods ,nanostars)optimizingparticlesize
(20 -100nm),shape ,andinter -particlespacing(1 -10nmgaps)tomaximize
electromagneticfieldenhancementatlaserwavelength2)Functionalize
substrateifneeded-modifymetallicsurfacewithantibodies ,aptamers ,or
molecularrecognitionelementsforselectiveanalytebindingandimproved
specificity3)Prepareandapplysample-processsample(filter ,dilute ,
```

35 

Federation over Text: Insight Sharing for Multi-Agent Reasoning 

A PREPRINT 

```
concentrateasneeded),depositontoSERSsubstrateviadrop -castingor
flow -through ,allowadsorptiontimeformoleculestoenterhotspots(<10nm
frommetalsurface)4)Selectlaserparameters-choosewavelengthmatching
plasmonresonance(532,633,or785nm),optimizepower(0.1 -10mW)toavoid
sampledamagewhilemaximizingsignal5)AcquireSERSspectrum-collectRaman
scatteredlightwithappropriateintegrationtime ,recordvibrationalspectrum
showingcharacteristicmolecularpeaks6)Analyzespectralfingerprint-
identifymoleculesbycomparingpeakpositionstoreferencespectra ,quantify
concentrationfrompeakintensitiesusingcalibrationcurves ,assessmolecular
orientationfrompeakratios7)Validateandcontrolquality-average
multiplespotsforreproducibility ,useinternalstandards ,verifywith
orthogonalmethods ,considersubstrateheterogeneityandenhancementfactor
variations"
}}
```

Prompt 6 is used for determining whether a paper can be covered by insights from the library, used in the application studied in Section 4.4. 

Prompt 6: Judging Whether Paper Contributions Match with the Insight Library 

```
Youareevaluatingwhetheraresearchpaper ’sproposedsolutionsareguidedbyor
directlyderivedfrominsightsinanencyclopedia.
Insights:
{ insights_prompt }
ResearchPaper:
{paper_text}
EvaluationCriteria-AninsightguidesthepaperONLYIFALLofthefollowing
aretrue:
1.CONCRETEMETHODOLOGYUSAGE:Theinsight ’smethodologyorapproachis
concretelyusedinthepaper ’smethods/approachsection ,notjust
theoreticallyrelevantormentionedinmotivation.
2.METHODSSECTIONPRESENCE:Theinsightmustberelatedtohowthepaper
actuallyimplementsitssolution(methods ,algorithms ,techniques),notjust
inproblemstatementorrelatedwork.
3.COUNTERFACTUALTEST:Thepaper ’scorecontributionwouldfundamentallydiffer
orfailwithoutthisinsight.Ask:"Iftheauthorsdidn ’tknowthisinsight ,
couldtheystillarriveatthesamecoresolution ?"
4.SPECIFICITY:Theinsightmustspecificallyaddressakeychallengeor
componentofthepaper ’ssolution ,notjustbegenerallyapplicablebackground
knowledge.
ResponseFormat:
-RespondONLYinvalidJSONwithkeys:guided(boolean),matched_insights(array
ofinsightnames)
-Setguided=trueONLYwhenatleastoneinsightpassesALLcriteriaabove
-UseonlyexactinsightnamesfromtheInsightslistabove
```

### **G.2 Complete Problem Prompts** 

For completeness, we summarize the problem prompts used in each application. For math benchmarks, we concatenate the dataset question with Prompt 7. For GPQA and GPQA-diamond, we use Prompt 8; for LiveCodeBench, Prompt 9; and for Humanity’s Last Exam, Prompt 10. For the research insight library, we adopt the template in Prompt 11, using the answer as the “ _{_ solution _}_ .” For PinchBench and Claw-Eval, we directly use the task instructions provided by the benchmarks. 

36 

Federation over Text: Insight Sharing for Multi-Agent Reasoning 

A PREPRINT 

Prompt 7: Math Benchmark 

```
’\nSolvetheproblemstepbystep.Wrapyourfinalanswerin"\\ boxed {}". ’
```

Prompt 8: Scientific Question Answering Benchmark 

```
Pleasesolvethisgraduate -levelsciencequestionstepbystep.
Instructions:
1.Analyzethequestioncarefully
2.Considereachoptionsystematically
3.Explainyourreasoning
4.Provideyourfinalanswerasasingleletter(A,B,C,orD)
5.Wrapyourfinalanswerletterin\\ boxed {},forexample:\\ boxed{A}
```

Prompt 9: Coding Benchmark 

```
Pleasesolvethisprogrammingproblembywritingclean ,efficientcode.
Requirements:
1.Readtheproblemdescriptioncarefully
2.Understandtheinput/outputformat
3.Writeacompletesolution
4.Includeproperinput/outputhandling
5.Wrapyourfinalcodesolutioninmarkdowncodeblockswithtriplebackticks
(‘‘‘)
Yoursolutionshouldreadfromstandardinputandwritetostandardoutput.
```

Prompt 10: Humanity’s Last Exam 

```
YouaresolvingoneHLEmultimodalbenchmarkproblem.
UseBOTHthequestiontextandtheattachedimage.
Returnonlythefinalanswer ,withnoexplanation.
```

Prompt 11: Paper Reading 

```
Answerresearchquestionofthepaper:{paper_name}basedonpaper
content :{ paper_content}
Allpapersneedtobeconsideredintheanalysis.
```

### **G.3 Prompts for Metacognitive Reuse [23]** 

For completeness, here, we re-state the prompts proposed in prior work [23] that we build upon and compare against. Prompt 12: Generating Solution 

```
Pleasereasonstepbystepandputthefinalanswerin
Problem:<problem >
```

37 

Federation over Text: Insight Sharing for Multi-Agent Reasoning 

A PREPRINT 

Prompt 13: Generating Reflection 

```
Hereisthedefinitionofabehavior:
-Abehaviorisanoteorskilltokeepinmindwhilesolvingmathproblems.
-Itcanbeastrategy ,atrick ,oratechnique.
-Itcanalsobeageneralruleoracommonsenseprinciple.
-Abehaviorisnotasolutiontotheproblem ,butitcanbeusedtosolvethe
problem.
Forexample-iftheproblemis"Findtheareaofacirclewithradius4",one
usefulbehaviourcouldbe
{" behavior_area_of_circle ":areaofacircleispi*r^2}.
Givenaproblemandthecorrespondingsolution ,reactandcritiquethesolutions
alongthefollowingdimensions:
1.CorrectnessAnalysis:Istheanswermathematicallycorrect?Arethere
calculationerrors?Isthereasoninglogically
sound?Areallstepsproperlyjustified?Whatspecificmistakesweremade?
2.MissingBehaviorsAnalysis:Whatbehaviorsshouldhavebeenusedbutweren ’t?
Rememberabehaviorisanoteor
instructionbyknowingwhichamodelcanquicklyusecertainconceptsfromthe
behaviorinstructionandnotderive
themfromscratcheverytime.Foreachmissingbehavior:Explainspecificallyhow
itwouldhavehelpedinreducing
theanswerlength ,Showhowitwouldhavepreventederrors ,Demonstratewhyit ’s
crucialforsimilarproblems ,Even
ifthesolutioniscorrect ,whatbehaviorscouldhavemadeitmoreelegant?
3.NewBehaviorSuggestions:Suggestspecificnewbehaviorsthatwillhelpwith
similarproblems.Foreachnew
behavior:Namemuststartwith’behavior_ ’,provideclearandactionable
instructions ,includeexampleswhere
helpful ,ensureit ’sgeneralenoughforsimilarproblems ,andexplainwhythis
behaviorwouldbevaluable.
```

Prompt 14: Generating Behavior 

```
<reflectionprompt >
```

```
<reflection >
```

```
Now ,giventhisreflectiongeneratealistof
behaviorsandcorrespondinginstructionsexplanationsinjsonformat.Each
behaviorshouldbeasingleline ,andtheformatis"behavior_[name ]:
[description ]".Thelistshould
beinjsonformat ,andeachbehaviorshouldbeakey -valuepair ,wherethekeyis
thebehaviornameandthevalueisthedescription.
```

## **H Insights, Raw Reasoning Processes, and Reasoning Traces** 

### **H.1 Representative Insights** 

In this section, we show example insights. The first three examples is from the library that are created in the ML research insight discovery application, derived from ICLR 2023 papers (Setting 1). 

With Gemini 3.0 Pro Preview and ICLR 2023 papers, we obtain three insights: structured output prediction (Insight 1), causal representation learning (Insight 2), and physics-informed deep learning (Insight 3), which provide interesting 

38 

Federation over Text: Insight Sharing for Multi-Agent Reasoning 

A PREPRINT 

ideas and instructions on how to approach related research problems. These topics remain cutting-edge research questions today. 

Insight 1: Structured Output Prediction (Setting 1) 

```
Whentouse:Whenthemodeloutputisnotasimpleclassorscalar ,butacomplex
structuredobject(e.g.,asequence ,atree ,amatching ,acodeprogram)where
dependenciesbetweenoutputelementsmustbemodeled.Step -by -step:1)Define
theoutputspaceconstraintsanddependencies(e.g.,grammarrules ,bi -partite
matchingconstraints).2)Useautoregressivemodels(likeTransformers)to
generateelementssequentiallyconditionedonhistory ,ornon - autoregressive
modelswithiterativerefinement.3)Applystructurallosses(e.g.,
connectionisttemporalclassification ,grapheditdistance ,optimaltransport
cost)ratherthansimplepointwiseerror.4)Useinferencetechniqueslike
beamsearchorconstraineddecodingtofindthemostlikelyvalidstructure.
Keyinsights:Thiscoversskillslikehierarchicalbipartitematching ,
permutationequivalentmodeling ,andprogramsynthesis.
```

Insight 2: Causal Representation Learning (Setting 1) 

```
Whentouse:Whenbuildingmodelsthatmustrobustlyidentifycause -and -effect
relationshipsratherthanspuriouscorrelations ,enablinginterventionsand
counterfactualreasoning.Step -by -step:1)ModelthesystemusingaStructural
CausalModel(SCM)orDirectedAcyclicGraph(DAG).2)Distinguishbetween
invariantcausalmechanisms(stableacrossenvironments )andspurious
associations.3)Useinterventions(do -calculus)orenvironmentaldiversityto
discoverthecausalgraph.4)Learnrepresentationsthatsatisfyconditional
independenceconstraintsimpliedbythecausalstructure( disentanglement ).5)
OptimizeforInvariantRiskMinimization(IRM)tofindpredictorsthatare
optimalacrossallinterventionaldistributions .Keyinsights:Thisunifies
skillslikecausalmediationanalysis ,front -doorprompting ,andcausalshift
diagnosis.
```

Insight 3: Physics Informed Deep Learning (Setting 1) 

```
Whentouse:Whenmodelingphysicalsystemsgovernedbypartialdifferential
equations(PDEs),conservationlaws ,orgeometricconstraints(e.g.,fluid
dynamics ,structuralmechanics ,climatemodeling)wherepurelydata -driven
modelsviolatephysicalvalidityorrequireexcessivedata.Usethisto
integratephysicalknowledgedirectlyintothelearningprocess.Step -by -step:
1)Formulatethegoverningphysicalequations(residuals)ofthesystem(e.g.,
Navier -Stokes ,Eikonalequation).2)Designtheneuralnetworktooutputthe
physicalstatevariables(velocity ,pressure)givenspatiotemporal
coordinates.3)Computederivativesoftheoutputswithrespecttoinputs
usingautomaticdifferentiation(Autograd)toevaluatethePDEresiduals.4)
Constructacompositelossfunction:DataLoss(fittingobservations )+
PhysicsLoss(minimizingPDEresiduals)+Boundary/InitialConditionLoss.5)
Optionally ,usehardconstraints(ansatz)orcoordinatetransformationsto
enforceboundaryconditionsbyconstruction .Keyinsights:Thisguides
specificskillslikePDE -constrainedlatentdynamics ,softcontactmodeling ,
andneuraloperatorlearning.
```

In Setting 2, insights generated by Gemini 2.0 Flash are generally shorter than those by Gemini 3.0 Pro. However, even without knowledge of future papers, we still obtain interesting insights such as neuro-symbolic reasoning (Insight 4) and parameter-efficient model adaptation (Insight 5), which corresponds to what is currently known as parameter- 

39 

Federation over Text: Insight Sharing for Multi-Agent Reasoning 

A PREPRINT 

efficient fine-tuning. It also produces the zero-to-one capability testing insight (Insight 6), which can be adapted to systems research. 

Insight 4: Neuro Symbolic Reasoning (Setting 2) 

```
Whentouse:Whenaproblemrequiresboththeperceptualflexibilityofneural
networks(handlingnoisy ,unstructureddata)andthe
precision/ interpretabilityofsymboliclogic(handlingrules ,math ,
constraints).Step -by -step:1)DecomposethesystemintoaNeuralModule
(perception/patternmatching)andaSymbolicModule(reasoning/execution).2)
Designaninterfacelayer:convertingneuraloutputsintodiscretesymbols
(concepts)ordifferentiableapproximations(softlogic).3)UsetheSymbolic
Moduletoexecutelogicalrules ,programs ,orarithmeticontheextracted
symbols.4)Trainend -to -end(viagradientsthroughsoftlogic)orseparately
(viaREINFORCEorsupervision)tooptimizebothperceptionandreasoning
accuracy.Keyinsights:Thisabstractsskillslikeneuro -symbolicprompt
construction ,logicconstraintintegration ,andprogramsynthesis.
```

Insight 5: Parameter Efficient Model Adaptation (Setting 2) 

<mark>`When to use: When adapting large pre -trained ’foundation ’ models (LLMs , ViTs) to specific downstream tasks without the computational cost of full fine -tuning. Step -by -step: 1) Freeze the bulk of the pre -trained model parameters. 2) Introduce a small set of trainable parameters: Adapters (bottleneck layers between existing layers), Prompt/Prefix Tuning (learnable input tokens), or Low -Rank Adaptation (LoRA - decomposing weight updates into low -rank matrices). 3) Train only these new parameters on the task -specific dataset. 4) Optionally , use techniques like weight averaging (model soup) or dynamic routing to combine multiple adaptations. Key insights: This covers skills like minimalist adapter co -training , prompt engineering , and efficient fine -tuning protocols.`</mark> Insight 6: Zero-To-One Capability Testing (Setting 2) <mark>`When to use: When assessing the functional value of a new technology or method to distinguish between efficiency gains and capability unlocks. This applies to product management , feature prioritization , and evaluating ’breakthrough ’ research. Step -by -step: 1) Ignore quantitative metrics (speed , cost , error rate) initially 2) Define the ’Capability Boundary ’ of the previous state -of -the -art ---specifically what tasks it physically could not perform 3) Ask the binary question: ’Does the new solution enable a task that was previously impossible/intractable?’ 4) If the answer is ’No ’ (it just does existing tasks better), classify as ’1-to -N’ (Incremental) 5) If the answer is ’Yes ’ (it opens a new action space), classify as ’0-to -1’ (Non -Incremental) 6) Prioritize 0-to -1 capabilities for strategic innovation as they create new markets.`</mark> 

The following examples are drawn from an insight library generated by Gemini-3.1-Pro under a high-thinking setting on PinchBench. These examples show that FoT can produce insights that serve as decision support in areas such as software engineering and market analysis. 

Insight 7: Declarative Architecture Standardization (PinchBench) 

```
Thissoftwareengineeringstandardappliesmodern ,declarativeconfigurationsand
specificdirectorylayoutstoprojectinitializationtoensurelong -term
```

40 

Federation over Text: Insight Sharing for Multi-Agent Reasoning 

A PREPRINT 

```
maintainabilityandout -of -the -boxcompatibilitywithmodernbuildtools.When
touse:Wheneverinitiating ,refactoring ,ordefiningthearchitectureofnew
codelibraries ,packages ,ormicroservices .Details:1)Implementthe’src ’
layoutparadigm(placingcoremodulesinsideasrc/directoryadjacentto
tests)toforcetestingagainsttheinstalledpackageversionratherthan
localdirectorymasking.2)Utilizedeclarativemetadataconfigurationfiles
(likepyproject.tomlcompliantwithPEP517/518)insteadoflegacyimperative
scripts(likesetup.py)tomanagedependenciesandbuildinstructions.
```

### Insight 8: Differentiator Focused Market Deconstruction (PinchBench) 

```
Thiscompetitiveintelligenceframeworkdistillscrowdedmarketlandscapesinto
highlyactionableartifactsbyignoringparityandfocusingexclusivelyon
divergence.Whentouse:Whenconductingtechstackevaluations ,vendor
selections ,orbusinessintelligencereportinginmatureindustrieswhere
competitorsshareamassivebaselineofidenticalfunctionalities .Details:1)
Scanmacroindustrytrendsbeforedrillingintomicroprofiles.2)Explicitly
identifyandfilteroutindustry -standardbaselinefeatures(’tablestakes ’).
3)Abstracthighlyvolatiledata(likeexactdollarcosts)intobroader
operationalparadigms.4)IntegraterecentstructuralcontextlikeM&A
parent -companyownership.5)Maptheremaininguniquearchitecturalrootsand
targetaudiencedifferencesontoastructuredcross -dimensionalcomparison
matrix.
```

### Insight 9: UI Bypass File Routing (PinchBench) 

```
Thisfundamentaloperationalpatternseparatesback -endautomatedartifactsfrom
front -endconversationalinterfaces.Itsolvesthe’doubleprint ’token
clutterproblembywritinggeneratedpayloadsdirectlytothefilesystem
whilereturningonlyasynthesized’BottomLineUpFront ’(BLUF)orstatus
summarytotheuserinterface.Whentouse:Applythiswheneverexecuting
tasksthatgeneratelargeartifacts(codebases ,CSVs ,long -formreports)or
orchestrateclosed -loopfiletransformations(read -process -write),
specificallywhentheuserprovidesexplicitdestinationcommandslike’Save
to ’or’Createafile ’.Details:1)Generatetheprimarypayloadinternally.
2)Pipepayloadviaafile -writetooldirectlytopersistentstorage.3)
Verifysuccessfulbyte -countwritten.4)Outputonlyabriefexecutivesummary
confirmingcompletionanddetailingcorecontents.
```

### **H.2 Complete Raw Reasoning Process for Case Studies in Appendix D.2** 

Raw Reasoning Process 1: Incorrect Reasoning Process of GPQA Diamond Problem 89 (Round 2) 

```
SolutionResponse:**Step -by -StepAnalysis :**
1.** AnalysisofProduct1Formation :**
*StartingMaterial:1,3- dibromoadamantane .
*Reagents:KOH ,240C.
*ThisreactionisaknownGrob -typefragmentationoftheadamantane
skeleton.The1,3- functionalizationallowsforthecleavageofaC-Cbondin
thecage ,leadingtoabicyclicsystem.
*ThespectraldataforProduct1confirmsthis:
*IR1720cm$ ^{-1}$indicatesaketone($C=O$).
*${}^1 $HNMR4.79ppm(2H)indicatesterminalvinylicprotons
($=CH_2$),whichtypicallyappearinthe4.5 -5.0ppmrange.
```

41 

Federation over Text: Insight Sharing for Multi-Agent Reasoning 

A PREPRINT 

```
*Thestructureconsistentwiththisdataandthestartingmaterialis
**3- methylenebicyclo [3.3.1] nonan -7-one**(or
7- methylenebicyclo [3.3.1] nonan -3-oneduetosymmetry).Thismoleculehasthe
formula$C_ {10} H_ {14} O$andfitstheunsaturationindex.
2.** AnalysisofProduct2Formation :**
*Reagents:Product1+ExcessAluminumIsopropoxide($Al(OiPr)_3$)+Heat.
*Thisisthe** Meerwein -Ponndorf -Verley(MPV)reduction **.Itselectively
reducesketonestoalcohols.
*** Stereochemistry :**TheMPVreductionisreversibleand ,underheated
conditionswithexcessreagent ,typicallyyieldsthe** thermodynamicproduct **.
*Inthebicyclo [3.3.1] nonanesystem ,substituentsatpositions3and7
faceseveretransannularstericrepulsioniftheyareinthe** endo **
(equatorial -likepointinginwards)position.Therefore ,thestableconformer
placesbulkygroupsinthe**exo**(axial -likepointingoutwards)position.
*Consequently ,thethermodynamicproductofthereductionisthe
**exo -alcohol **(wheretheOHgroupisaxial).
*Product2is**exo -3- methylenebicyclo [3.3.1] nonan -7-ol**.
3.** AnalysisofProduct3Formation :**
*Reagents:Product2+Ozone($O_3$),-78C,followedbyDMS.
*Thisisan** ozonolysis **reactionwithreductiveworkup.Itcleavesthe
exocycliccarbon -carbondoublebond($=CH_2$)andconvertsitintoacarbonyl
group($C=O$).
*ThestereocenteratC7(bearingtheOHgroup)isunaffected.
*Product3is**exo -7- hydroxybicyclo [3.3.1] nonan -3-one **.
4.**NMRPredictionforProduct3:**
*** TargetProton :**Thequestionasksforthecouplingpatternofthe
"mostdeshieldedhydrogenatom"(excludingexchangeableOH).
*InProduct3,theprotononthecarbonbearingthehydroxylgroup(H-C7)
isthemostdeshieldedduetotheelectronegativityofoxygen(chemicalshift
typically3.5-4.5ppm).
*** StereochemistryofH-C7:**Sincethehydroxylgroup(OH)isinthe
**exo(axial)**position(thermodynamicproduct),thegeminalhydrogenatom
(H-C7)mustbeinthe** endo(equatorial)**position.
*** CouplingAnalysis :**
*TheH-C7(equatorial)protoniscoupledtofourvicinalprotonson
theadjacentbridgecarbons(C6andC8).
*Duetothemolecularsymmetry(planepassingthroughC3 -C7 -C9),the
protonsonC6areequivalenttothoseonC8.
*Theneighborsare:H-6ax ,H-6eq ,H-8ax ,H-8eq.
*Couplingconstantsforanequatorialprotoninachair -likeringare
generallysmall:$J_{eq -ax}\approx2-5$Hzand$J_{eq -eq}\approx2-5$Hz.
*Becausethecouplingconstantsaresmallandofsimilarmagnitude ,
thesplittingpatterntypicallyappearsasa** pentet **(quintet)
(representingoverlapofcouplingsto4protons).
*(Note:IftheHwereaxial ,itwouldshowlargetrans -diaxial
couplings(~10 -12Hz)andsmallaxial -equatorialcouplings ,resultingina
distincttripletoftriplets.Sincewehavethethermodynamicexo -alcohol ,the
Hisequatorial ,rulingoutthetripletoftriplets).
** Conclusion :**ThemostdeshieldedhydrogenistheequatorialHatC7 ,which
couplestofourneighborswithsimilarsmallcouplingconstants ,producinga
pentet.
\boxed{D}
```

Raw Reasoning Process 2: Correct Reasoning Process of GPQA Diamond Problem 89 (Round 3) 

```
SolutionResponse:** Step1:StructureElucidationofProduct1**
```

42 

Federation over Text: Insight Sharing for Multi-Agent Reasoning A PREPRINT 

```
Thestartingmaterialis1,3- dibromoadamantane .HeatingthiswithexcessKOHat
hightemperatures($240 ^\ circ\text{C}$)isaknownfragmentationreaction
involvingtheadamantaneskeleton.TheconditionsfacilitateaGrob -type
fragmentationofthe1,3- functionalizedsystemtoformabicycliccompound.
ThedataprovidedforProduct1supportsthis:
***IR1720cm$ ^{-1}$**:Indicatesaketone(C=O).
***$^{1}\ text{H}$NMR **:Thesignalat$\delta4.79$(2H)correspondstoan
exocyclicmethylenegroup($=\ text{CH}_2$).Theremainingprotons(12H)fit
thebicyclicskeleton.
Thestructureformedis**7- methylenebicyclo [3.3.1] nonan -3-one **.Thismolecule
fitstheformula($C_ {10} H_ {14} O$)andthespectraldata.
** Step2:StructureElucidationofProduct2**
Product1isheatedwithexcessaluminumisopropoxide.Thesearetheconditions
fora** Meerwein -Ponndorf -Verley(MPV)reduction **.
*TheMPVreductionconvertstheketoneatC3toasecondaryalcohol.
*Crucially ,MPVreductionsarereversibleandthermodynamicallycontrolled ,
yieldingthemorestablealcoholisomer.
*In3-substitutedbicyclo [3.3.1] nonanes ,the**exo -isomer **(substituentin
theequatorialposition)isthermodynamicallymorestablethantheendo -isomer
(substituentintheaxialposition).Thisisbecausetheendopositionsuffers
fromseveretransannularstericrepulsionwiththeC7position(evenwiththe
changeinhybridizationatC7 ,theexo -alcoholremainsthepreferred
thermodynamicproductinthesesystems).
*Therefore ,Product2is**exo -7- methylenebicyclo [3.3.1] nonan -3-ol**.
*Stereochemistry :Thehydroxylgroupis**exo(equatorial)**.Consequently ,
thecarbinolhydrogenatom(H-3)is** endo(axial)**.
** Step3:StructureElucidationofProduct3**
Product2issubjectedtoozonolysis($O_3$ ,then$Me_2S$).
*Ozonolysiscleavestheexocycliccarbon -carbondoublebond($=\ text{CH}_2$)
atC7toformaketone($C=O$).
*ThealcoholatC3isunaffected.
*Product3is**exo -7- hydroxybicyclo [3.3.1] nonan -3-one**(alsonamed
exo -3- hydroxybicyclo [3.3.1] nonan -7-oneduetosymmetry).
** Step4:AnalysisoftheTargetProton **
Thequestionasksforthecouplingpatternofthe"mostdeshieldedhydrogenatom"
inProduct3.
*Theprotonsinthemoleculeare:
*Protonsalphatotheketone(C2/C4orC6/C8):$\delta\approx2.4$ppm.
*Bridgeheadprotons(C1/C5):$\delta\approx2.0$ppm.
*Bridgeprotons(C9):$\delta\approx1.8$ppm.
*Carbinolproton(H-3,alphato-OH):$\delta\approx3.8\ text {--}4.2$ppm.
*The** carbinolproton(H-3)**isthemostdeshieldednon -exchangeableproton
duetotheelectronegativityoftheoxygenatom.
** Step5:DeterminingtheCouplingPattern **
Wehaveestablishedthatthehydroxylgroupis**exo(equatorial)**,placingthe
targethydrogenatom(H-3)inthe** axial **positionofthecyclohexane -like
chairring.
*** Neighbors **:TheC3carbonisflankedbytwomethylenegroups(C2andC4).
Duetotheplaneofsymmetryinthemolecule ,C2andC4areequivalent.
*** CouplingPartners **:TheaxialH-3coupleswith:
*Two** axial **protons(H-2ax ,H-4ax).
*Two** equatorial **protons(H-2eq ,H-4eq).
*** CouplingConstants($J$)**:
*Axial -Axialcoupling($J_{aa}$)islarge ,typically10 -12Hz
(anti -periplanararrangement).
*Axial -Equatorialcoupling($J_{ae}$)issmalltomedium ,typically2-5Hz
(gauchearrangement).
*** Pattern **:
*Thesplittingbythetwoequivalentlargecouplings($J_{aa}$)createsa
triplet($1 :2:1$).
```

43 

Federation over Text: Insight Sharing for Multi-Agent Reasoning 

A PREPRINT 

```
*Eachlineofthistripletisfurthersplitintoatripletbythetwo
equivalentsmallcouplings($J_{ae}$).
*Theresultingpatternisalargetripletofsmalltriplets ,knownasa
** tripletoftriplets **(tt).
Incontrast ,anequatorialproton(whichwouldresultfromthekinetic
endo -alcohol)typicallyshowssmallcouplingstoallneighbors ,appearingasa
pentetorbroadmultiplet.Sincewehavethethermodynamicproduct(axialH),
theansweristhetripletoftriplets.
\boxed{C}
```

Raw Reasoning Process 3: Incorrect Reasoning Process of AIME25 Problem 28 (Round 1) 

```
SolutionResponse:Letthesequencebedefinedby$x_1=\frac {25}{11}$and
$x_{k+1}=\frac {1}{3}\ left(x_k+\frac {1}{ x_k}-1\ right)$.
Thissimplifiesto$x_{k+1}=\frac{x_k^2-x_k+1}{3 x_k}$.
Let$x_k=\frac{m_k}{n_k}$with$\gcd(m_k ,n_k)=1$.Then
\[x_{k+1}=\frac{m_k^2-m_kn_k+n_k ^2}{3 m_kn_k}.\]
Let$m_{k+1}’=m_k^2-m_kn_k+n_k^2$and$n_{k+1}’=3m_kn_k$.
Thesumofnumeratoranddenominatoris$S_{k+1}’=m_{k+1}’+n_{k+1}’=m_k^2+
2m_kn_k+n_k^2=(m_k+n_k)^2=S_k^2$.
Theactualterms$m_{k+1},n_{k+1}$areobtainedbydividingby$g_k=
\gcd(m_{k+1}’,n_{k+1}’)$.
Wehave$\gcd(m_k^2-m_kn_k+n_k^2,m_kn_k)=1$since$\gcd(m_k ,n_k)=1$.
Thus$g_k=\gcd((m_k+n_k)^2,3)$.
Since$S_1=25+11=36$,whichisdivisibleby3,wehave$g_1=3$.
Also ,$S_{k+1}=S_k^2/g_k$.If$S_k$isdivisibleby3,then$S_k ^2$is
divisibleby9,so$S_{k+1}=S_k ^2/3$isdivisibleby3.
Thusbyinduction ,$g_k =3$forall$k$ ,and$S_{k+1}=S_k^2/3$.
Let$T_k=S_k/3$.Then$3T_{k+1}=(3T_k)^2/3=3T_k^2\impliesT_{k+1}=
T_k^2$.
Wehave$S_1=36$,so$T_1=12$.
Then$T_k=12^{2^{k -1}}$,and$S_k=3\cdot12^{2^{k -1}}$.
Weneed$S_ {2025}=3\cdot12^{2^{2024}}\pmod {1000}$.
Modulo8:$S_ {2025}=3\cdot4^{2^{2024}}\cdot3^{2^{2024}}\equiv0\pmod8$
(forlargeexponent).
Modulo125:$\phi (125)=100$.Theexponentis$E=2^{2024}$.
$2 ^{2024}\equiv16\pmod {100}$.
So$S_ {2025}\equiv3\cdot12^{16}\pmod {125}$.
$12 ^{16}\equiv84\pmod {125}$.
$S_ {2025}\equiv3\cdot84=252\equiv2\pmod {125}$.
Wesolvethesystem$x\equiv0\pmod8$and$x\equiv2\pmod {125}$.
$x=125k+2$.$125k+2\equiv5k+2\equiv0\pmod8\implies5k\equiv-2
\equiv6\impliesk\equiv6\pmod8$.
$x=125(6)+2=750+2=752$.
\boxed {752}
```

Raw Reasoning Process 4: Correct Reasoning Process of AIME25 Problem 28 (Round 2) 

```
SolutionResponse:Tosolvefor$x_ {2025}$,wefirstanalyzetherecurrence
relation$x_{k+1}=\ frac {1}{3}\ left(x_k+\ frac {1}{ x_k}-1\ right)=\frac{x_k^2-
x_k+1}{3 x_k}$.
Let ’sfindthefixedpointsofthetransformation$f(x)=\frac{x^2-x+1}{3x}$.
Setting$f(x)=x$ ,weget$x^2-x+1=3x^2$,whichimplies$2x^2+x-1=
0$.Factoringgives$(2x-1)(x+1)=0$.Thefixedpointsare$x=1/2$and$x=
-1$.
```

44 

Federation over Text: Insight Sharing for Multi-Agent Reasoning 

A PREPRINT 

```
Thissuggestsusingalinearfractionaltransformationthatmapsthesefixed
pointsto$0$and$\infty$tosimplifytherecurrence.Let$z_k=\frac{x_k-
1/2}{ x_k+1}=\frac {2x_k-1}{2( x_k+1)}$.Toavoidthefactorof2inthe
denominator ,let ’sdefine$z_k=\frac {2x_k-1}{ x_k+1}$.
Let ’sfindtherecurrencefor$z_k$:
$$z_{k+1}=\frac {2x_{k+1}-1}{x_{k+1}+1}=\frac {2\ left (\ frac{x_k^2-x_k+
1}{3 x_k}\ right)-1}{\ frac{x_k^2-x_k+1}{3 x_k}+1}=\frac {2( x_k^2-x_k+
1)-3x_k}{x_k^2-x_k+1+3x_k}=\frac {2x_k^2-5x_k+2}{ x_k^2+2x_k+
1}$$
$$z_{k+1}=\frac {(2 x_k-1)(x_k-2)}{( x_k+1)^2}=\left (\ frac {2x_k-1}{ x_k+
1}\ right)\frac{x_k-2}{ x_k+1}$$
Wecanexpress$\frac{x_k-2}{ x_k+1}$intermsof$z_k$.From$z_k=
\frac {2x_k-1}{ x_k+1}=\frac {2( x_k +1)-3}{ x_k +1}=2-\frac {3}{ x_k +1}$,
wehave$\frac {3}{ x_k +1}=2-z_k$.
Then$\frac{x_k-2}{ x_k+1}=\frac{x_k+1-3}{ x_k+1}=1-\frac {3}{ x_k +1}
=1-(2-z_k)=z_k-1$.
Substitutingthisback ,weget:
$$z_{k+1}=z_k(z_k-1)$$
Wecalculatethefirstterm$z_1$:
$$x_1=\frac {25}{11}\impliesz_1=\frac {2(25/11)-1}{25/11+1}=\frac {50/11
-11/11}{25/11+11/11}=\frac {39}{36}=\frac {13}{12} $$
Wecanrepresent$z_k$asafraction$N_k/D_k$.
$z_1=\frac {13}{12}$.
$z_2=\frac {13}{12}\left (\ frac {13}{12}-1\ right)=\frac {13}{144}$.
$z_3=\frac {13}{144}\left (\ frac {13}{144}-1\ right)=\frac {13\cdot
( -131) }{144^2}$.
Thedenominatorof$z_k$followsthepattern$D_k=12^{2^{k -1}}$.
Thenumerator$N_k$anddenominator$D_k$arerelativelyprime(asderivedinthe
thoughtprocess).
Weneed$x_ {2025}=\frac{m}{n}$.Invertingthetransformation$z=
\frac {2x -1}{x+1}$:
$$z(x+1)=2x-1\implieszx+z=2x-1\implies1+z=x(2-z)\impliesx=
\frac {1+z}{2-z}$$
Substituting$z_ {2025}=\frac{N}{D}$:
$$x_ {2025}=\frac {1+N/D}{2-N/D}=\frac{D+N}{2D-N}$$
Since$\gcd(N,D)=1$and$N\equiv1\pmod3$,$D\equiv0\pmod3$,the
fractionisirreducible.
Thus$m=D+N$and$n=2D-N$.
Thesum$m+n=(D+N)+(2D-N)=3D$.
Weneedtocalculate$3D_ {2025}\pmod {1000}$.
$D_ {2025}=12^{2^{2024}}$.Let$E=2^{2024}$.Weneed$3\cdot12^E
\pmod {1000}$.
ByChineseRemainderTheoremon$1000=8\times125$:
1.**Mod8**:$12\equiv4\pmod8$.$12^E=4^E$.Since$E\ge2$,$4^E$is
divisibleby$16$ ,so$12^E\equiv0\pmod8$.Thus$3\cdot12^E\equiv0
\pmod8$.
2.**Mod125**:Weneed$3\cdot12^E\pmod {125}$.
Compute$E\pmod {\phi (125)}$.$\phi (125)=100$.
$E=2^{2024}$.
$E\equiv0\pmod4$.
$E\pmod {25}$:$\phi (25)=20$.$2024=20\times101+4$.$E\equiv2^4=
16\pmod {25}$.
UsingCRTformod100:$x\equiv0\pmod4$and$x\equiv16\pmod {25}$
implies$x\equiv16\pmod {100}$.
Soweneed$12 ^{16}\pmod {125}$.
$12^2=144\equiv19$.
$12^4\equiv19^2=361\equiv111\equiv-14$.
$12^8\equiv(-14)^2=196\equiv71$.
$12 ^{16}\equiv71^2=5041=40\times125+41\equiv41$.
So$3\cdot12^E\equiv3\cdot41=123\pmod {125}$.
```

45 

Federation over Text: Insight Sharing for Multi-Agent Reasoning 

A PREPRINT 

```
Solvingfor$X\equiv0\pmod8$and$X\equiv123\pmod {125}$:
$X=125k+123$.
$125k+123\equiv5k+3\equiv0\pmod8\implies5k\equiv-3\equiv5
\impliesk\equiv1\pmod8$.
$X=125(1)+123=248$.
Theremainderis248.
\boxed {248}
```

### **H.3 Example Reasoning Traces in Section 4.4** 

Reasoning Trace 1: Inverse Frequency Balancing 

```
Thismethodflattenslong -tailed(Zipfian)datadistributionstoprevent
modelsfromoverfittingtocommon’head ’conceptswhileunderfittingrare
’tail ’concepts.Itusesaprobabilisticsamplingapproachbasedonamaximum
frequencythresholdtoensureamoreuniformdistributionofconcepts.Whento
use:Whentrainingfoundationmodelsorclassifiersonnaturaldata
distributionswhereasmallnumberofclassesorconceptsdominatethedataset
(e.g.,millionsof’cat ’imagesvs.few’specificspecies ’),andthegoalis
tomaximizezero -shotgeneralizationortask -agnosticperformance.
Step -by -step:1)Scanthedatasettocalculatethetotalcount($N$)forevery
specificmetadataconceptorclass2)Defineasaturationthreshold($t$)that
representsthedesiredmaximumnumberofsamplesperconcept(e.g.,$t =20 ,000$
wasusedfor400Mtotalitems)3)Computeasamplingprobabilityforeach
conceptusingtheformula$P=\\min(1,t/N)$,ensuringtailconceptsarekept
withprobability1andheadconceptsaredownsampled4)Iteratethroughthe
datapointsagain;foritemsassociatedwithmultipleconcepts ,generatea
randomnumberagainsttheprobabilityofeachassociatedconcept5)Selectthe
datapointforthefinaltrainingsetif*atleastone*ofitsassociated
conceptstriggersaselection ,therebypreservingdiversityevenwithincommon
items.
```

### Reasoning Trace 2: Directional Skill Evolution 

```
Thistechniqueinvolvessystematicallytransformingspecific ,verifiedsolutions
intomoregeneralandreusabletools(skills)toenrichaknowledgebase.
Insteadofjuststoringaspecificanswer ,thesystemactively’evolves ’itto
coverbroadercases.Whentouse:Whenbuildingaknowledgebaseorskill
libraryfromspecificexamples ,particularlyindomainslikemathematicsor
codingwhereaspecificsolution(e.g.,for2Dvectors)oftenhintsata
generalprinciple(e.g.,forN-dimensions).Itisusedtoproactivelyexpand
thecapabilitiesofanAIagentwithoutrequiringnewexternalproblemsets.
Step -by -step:1)Selectaspecific ,verifiedskillorlemmafromtheexisting
library(theseed)2)Chooseoneoffourspecificevolutionheuristics:
’Parameterize ’(replacespecificconstantslikenumberswithvariables),
’ExtendDimensions ’(generalizefromspecificdimensionston-dimensions),
’ScaleComplexity ’(createamorecomplexversionoftheproblem),or
’IdentifyKeyConcepts ’(extractandformalizethecoreunderlyingprinciple)
3)Retrieverelevantunsolvedproblemsorrequeststoguidetheevolution
context ,ensuringthenewskillaimsatactualgaps4)Promptthemodelto
rewritetheseedskillaccordingtothechosenheuristic5)Formallyverify
thegeneratedskill;ifvalidanddistinctfromexistingskills ,addittothe
library.
```

46 

