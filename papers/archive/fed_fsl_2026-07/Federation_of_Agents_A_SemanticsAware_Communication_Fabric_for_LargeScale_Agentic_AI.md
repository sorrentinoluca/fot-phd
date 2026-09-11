# **Federation of Agents: A Semantics-Aware Communication Fabric for Large-Scale Agentic AI** 

**Lorenzo Giusti**<sup>_∗_</sup> **Ole Anton Werner Riccardo Taiello Matilde Carvalho Costa Emre Tosun Andrea Protani Marc Molina Rodrigo Lopes de Almeida Paolo Cacace Diogo Reis Santos Luigi Serio** 

CERN, Geneva, Switzerland 

## **Abstract** 

We present _Federation of Agents_ (FoA), a distributed orchestration framework that transforms static multi-agent coordination into dynamic, capability-driven collaboration. FoA introduces _Versioned Capability Vectors_ (VCVs): machine-readable profiles that make agent capabilities searchable through semantic embeddings, enabling agents to advertise their capabilities, cost, and limitations. Our architecture combines three key innovations: (1) _semantic routing_ that matches tasks to agents over sharded HNSW indices while enforcing operational constraints through cost-biased optimization, (2) _dynamic task decomposition_ where compatible agents collaboratively break down complex tasks into DAGs of subtasks through consensus-based merging, and (3) _smart clustering_ that groups agents working on similar subtasks into collaborative channels for _k_ -round refinement before synthesis. Built on top of MQTT’s publish-subscribe semantics for scalable message passing, FoA achieves sub-linear complexity through hierarchical capability matching and efficient index maintenance. Evaluation on HealthBench shows 13 _×_ improvement over single-model baselines, with clustering-enhanced collaboration particularly effective for complex reasoning tasks requiring multiple perspectives. The system scales horizontally while maintaining consistent performance, demonstrating that semantic orchestration with structured collaboration can unlock the collective intelligence of heterogeneous federations of AI agents. 


![](P013_images/P013.pdf-0001-06.png)

### Figure analysis

The figure serves as a conceptual architecture overview for the Federation of Agents framework described in the paper.

Direct visual observations:
- A map-like background shows a distributed setting, with multiple robot-like agent icons positioned across different locations.
- Each agent is paired with a document labeled “CV,” representing a capability vector or capability profile.
- A central node, visually emphasized near the middle, represents the orchestrator or coordination hub.
- Envelope icons and dashed white communication lines connect the distributed agents with the central orchestrator.
- The agents are visually heterogeneous, suggesting different capabilities, roles, or implementations.

Component relationships and information flow:
- Agents appear to publish or advertise their capability information through their associated “CV” documents.
- The orchestrator receives these capability advertisements and is positioned as the routing and coordination point.
- Dashed lines and envelope symbols indicate message-based communication, consistent with the paper’s description of MQTT publish/subscribe exchanges.
- The visual layout suggests bidirectional exchange: agents send capability updates or task results, while the orchestrator sends assignments or coordination messages.

Interpretation in relation to the paper text:
- The diagram supports the paper’s claim that FoA replaces static routing with semantic, capability-driven orchestration.
- The “CV” documents correspond to Versioned Capability Vectors, which the text describes as machine-readable profiles containing semantic embeddings and operational metadata.
- The central orchestrator corresponds to the system component responsible for semantic routing, task assignment, and synthesis of agent outputs along a task DAG.
- The distributed map reinforces the intended large-scale, horizontally distributed nature of the framework.

No quantitative axes, legends, or numerical results are present; this is an architectural illustration rather than an empirical chart.


Figure 1: **Federation of Agents.** Heterogeneous agents advertise _Versioned Capability Vectors_ containing semantic embeddingsof agents’ profiles. The orchestrator ingests these capability updates, and when a complex task arrives, it performs semantic routing to the most compatible agents or clusters. Envelopes and dashed arrows depict MQTT publish/subscribe exchanges for assignments, capability updates, and intermediate artifacts. Agents collaborate and return `TASK_COMPLETE` signals with subtask outputs; the orchestrator merges them along the task DAG to synthesize the solution. 

> _∗_ CERN, Corresponding to: lorenzo.giusti@cern.ch 

## **1 Introduction** 

The landscape of artificial intelligence has evolved from single AI models to networks of specialized agents that plan, coordinate, and act over extended horizons [1, 2, 3]. This shift toward _agentic AI systems_ represents a fundamental change in how we approach complex problem-solving with AI: rather than relying on a single model to handle all aspects of a task, we now orchestrate collections of specialized agents that can decompose tasks, maintain persistent context, and coordinate their efforts through structured communication towards a common goal. However, current agentic AI systems mainly rely on manually curated integrations and topic-based routing [4, 5], posing constraints on scalability as the heterogeneity of agents grows, and coordination complexity increases, limiting scalability and not addressing the fundamental operational question: _who can do what, at what cost, and under which policy constraints?_ ; preventing the realization of the "Internet of Agents" vision [6]. To address this, we introduce _Federation of Agents_ (FoA), a semantics-aware communication fabric that transforms agent coordination from static, topic-based routing to dynamic, capability-driven orchestration. At its core, FoA enables agents, tools, and data stores to advertise _Versioned Capability Vectors_ (VCVs): machine-readable profiles that capture functional capabilities, performance characteristics, operational constraints, and security labels in a structured format. 

**Problem Statement and Challenges.** Despite rapid progress, agentic AI systems still lack principled, searchable capability profiles, making _capability discovery_ and partner selection ad hoc even in prominent orchestration frameworks [4, 7, 6]. _Dynamic orchestration_ remains partially solved: rolebased systems improve structure yet often rely on manual wiring and do not couple decomposition with operational budgets [8, 9]. Meeting _resource constraints_ (latency, bandwidth, energy) alongside semantic fit is remarkable at the edge, where agents run on IoT devices [10], motivating embeddingbased _semantic routing_ and efficient, reliable transports [11, 12, 13, 14]. Heterogeneous security and regulatory regimes further raise _policy compliance_ requirements, demanding auditable enforcement across agents and data boundaries [15]. At _scale_ , coordination overhead and loss of coherence emerge as agent counts and workflow depth grow, calling for sublinear retrieval and structure-aware coordination [16, 17, 18]. Operational _observability and reliability_ are also underdeveloped: real deployments report behavioural variability, drift, and governance gaps in agentic processes and ecosystems [19, 20]. Finally, there are no interoperable protocols and ontologies to standardize capabilities and interactions, limiting portability across stacks and domains [21, 22, 23, 24]. 

**Our Approach.** FoA replaces static, topic-centric wiring with _dynamic, capability-driven orchestration_ , aligning with calls for semantics-first coordination in agent ecosystems [21, 22, 4, 7]. Agents publish (VCVs), structured, versioned profiles embedded in a high-dimensional space, so capabilities become searchable artifacts compatible with emerging interoperability efforts (e.g., Model Context Protocol (MCP)-based capability schemas) [23, 24]. We index VCVs using a sharded Hierarchical navigable small world (HNSW) index to support sublinear matching at scale while preserving nuanced distinctions among related skills [18]. At dispatch time, FoA applies _semantic routing_ that couples profiles’ similarities with policy checks and resource budgets (i.e., latency, bandwidth, energy consumption), rather than relying on keywords or static registries [11, 15]. Operational feasibility is enforced with transport-aware choices for IoT settings, where the Message Queuing Telemetry Transport (MQTT) protocol provides efficient, reliable delivery under constrained networks [12, 13, 14]. For _dynamic task decomposition_ , FoA elicits candidate breakdowns from compatible agents and merges them into a consensual directed acyclic graph DAG, drawing on role-structured collaboration patterns from multi-agent systems [8, 9]. Finally, _intelligent orchestration_ optimizes assignments over semantic fit and operational cost, supporting centralized and decentralized modes [16, 17]; this aligns with distributed orchestration needs observed in infrastructures such as CAFEIN<sup>®</sup> , CERN’s federated AI platform, where privacy-preserving data access and cross-institution coordination are central constraints [25, 26]. 

**Contributions.** We make three technical contributions to enable capability-driven orchestration of heterogeneous agent federations: (1) _Versioned Capability Vectors (VCVs)_ , a machine-readable representation that transforms agent capabilities, costs, and constraints into searchable semantic embeddings indexed via sharded HNSW for sub-linear retrieval at scale. (2) _Dynamic collaborative decomposition_ , where compatible agents jointly propose subtask breakdowns that the orchestrator merges into a consensus DAG, coupling task structure with operational budgets rather than relying on static decomposition. (3) _Smart clustering protocols_ that group agents working on identical 

2 

subtasks into collaborative channels for _k_ -round refinement, balancing diverse perspectives against communication overhead through hierarchical similarity-based partitioning. Unlike prior works, which rely on manual wiring or role-centric dispatch without a searchable capability registry, FoA’s VCVs enable policy and cost-aware _semantic routing_ and _consensus DAG_ execution; a registry and transport-level substrate for clustered collaboration with explicit policy labels. FoA achieves 13 _×_ improvement over single-model baselines on the HealthBench hard benchmark. 

## **2 Background and Related Works** 

**Agentic AI Systems: Communication Protocols and Architectures.** Agentic AI represents a paradigm shift from traditional AI systems that execute single tasks to systems that can plan, reason, and coordinate over extended horizons. Recent surveys differentiate _AI agents_ , modular systems optimized for specific tasks, from _agentic AI systems_ , which orchestrate collections of agents, decompose complex goals, and maintain persistent context across interactions [1, 2, 3]. The key insight is that while individual AI agents excel at specific tasks, complex problems often require the coordinated effort of multiple specialized agents [27]. This motivates research on scalable coordination mechanisms, communication protocols, and orchestration strategies that can manage the complexity of multi-agent systems. A parallel research line examines communication protocols and architectures for LLM-driven agents. Both Yang et al.[22] and Kong et al.[21] provides a comprehensive analysis of agentic AI protocols, highlighting the lack of standardized communication methods between agents, tools, and data sources. Their classification distinguishes context-oriented protocols that support local tool invocation from inter-agent protocols that enable cooperative behaviour, and contrasts general-purpose versus domain-specific solutions. Comparative assessments reveal trade-offs between security, scalability, and latency across existing protocols and call for next-generation designs with adaptability, privacy preservation, and group-based interaction. Emerging work also demonstrates that successful agentic architectures require robust trust, risk, and security management frameworks [28], particularly as these systems increasingly operate in safety-critical domains. The theoretical foundations underlying agentic coordination suggest that these systems would benefit from established systems theory principles to manage their inherent complexity and emergent behaviours [29]. Furthermore, practical implementations of agentic AI are showing promise across diverse application domains, from industrial automation [30] to healthcare compliance [15], demonstrating the broad applicability of coordinated multi-agent approaches. Complementary work on MCP [31, 24, 32, 23] proposes a standardized interface for connecting language models to external tools. However, most of the MCP implementations currently rely on HTTP and Server-Sent Events, introducing security concerns [33] and limiting their applicability to critical contexts or resource-constrained environments. 

**Multi-Agent Orchestration and Coordination** Researchers have explored various orchestration frameworks for coordinating agentic AI workflows across distributed systems. Multi-agent architectures leverage specialized agents with distinct capabilities: sensing, learning, reasoning, predicting, and executing that must be orchestrated to handle complex tasks through peer coordination [27]. Recent frameworks like HuggingGPT [4], AutoGen [7], and MetaGPT [8] demonstrate sophisticated orchestration patterns where a central coordinator routes tasks to specialized agents based on their capabilities. Self-organizing agent networks [16] enable dynamic workflow automation where agents autonomously form task-specific coalitions without centralized control. Communication protocols like CAMEL [9] promote structured inter-agent dialogue for collaborative problem-solving. Modern multi-LLM routing strategies employ various orchestration approaches, including static rule-based routing, dynamic model selection based on task complexity, and learned routing policies that optimize for performance and costs [11, 34]. Despite their strengths, these frameworks hinge on fixed roles and hand-wired coordination, lacking a searchable capability registry, cost-/policy-aware semantic routing, and standardized collaboration protocols needed for enterprise-scale deployment. 

**MQTT as Transport Layer for Distributed Agent Systems** To provide a message passing layer between AI agents, the MQTT protocol [12] provides a stack of tools for large-scale distributed systems communication through its lightweight publish/subscribe semantics. Unified namespace (UNS) patterns leverage MQTT’s topic hierarchy to create a semantic addressing scheme that eliminates data silos and enables seamless agent interoperability [35]. Unlike traditional request-response architectures, MQTT’s event-driven model naturally supports the asynchronous, many-to-many com- 

3 


![](P013_images/P013.pdf-0004-00.png)



![](P013_images/P013.pdf-0004-01.png)



![](P013_images/P013.pdf-0004-02.png)



![](P013_images/P013.pdf-0004-03.png)



![](P013_images/P013.pdf-0004-04.png)



![](P013_images/P013.pdf-0004-05.png)



![](P013_images/P013.pdf-0004-06.png)



![](P013_images/P013.pdf-0004-07.png)



![](P013_images/P013.pdf-0004-08.png)



![](P013_images/P013.pdf-0004-09.png)



![](P013_images/P013.pdf-0004-10.png)



![](P013_images/P013.pdf-0004-11.png)



![](P013_images/P013.pdf-0004-12.png)



![](P013_images/P013.pdf-0004-13.png)



![](P013_images/P013.pdf-0004-14.png)



![](P013_images/P013.pdf-0004-15.png)



![](P013_images/P013.pdf-0004-16.png)



![](P013_images/P013.pdf-0004-17.png)



![](P013_images/P013.pdf-0004-18.png)



![](P013_images/P013.pdf-0004-19.png)



![](P013_images/P013.pdf-0004-20.png)



![](P013_images/P013.pdf-0004-21.png)



![](P013_images/P013.pdf-0004-22.png)



![](P013_images/P013.pdf-0004-23.png)



![](P013_images/P013.pdf-0004-24.png)



![](P013_images/P013.pdf-0004-25.png)



![](P013_images/P013.pdf-0004-26.png)



![](P013_images/P013.pdf-0004-27.png)



![](P013_images/P013.pdf-0004-28.png)



![](P013_images/P013.pdf-0004-29.png)



![](P013_images/P013.pdf-0004-30.png)



![](P013_images/P013.pdf-0004-31.png)



![](P013_images/P013.pdf-0004-32.png)



![](P013_images/P013.pdf-0004-33.png)



![](P013_images/P013.pdf-0004-34.png)


Figure 2: **Orchestrator-driven Sub-task Decomposition and Semantic Routing.** The orchestrator receives a complex task, proposes subtasks (1-5), embeds each subtask, and compares them to agent capability embeddings to form a similarity matrix. Using similarity, cost, and policy constraints, it assigns each subtask to the most compatible agent or cluster (right-hand mapping). 

munication patterns required by multi-agent systems [13, 20]. Recent developments extend MCP over MQTT, replacing HTTP’s synchronous constraints with MQTT’s scalable pub/sub architecture for distributed agent coordination [36, 37, 38, 39]. This transport choice enables capability discovery across thousands of heterogeneous agents while maintaining sub-second latency and reliable message delivery under varying network conditions [14, 10, 40]. The protocol’s inherent support for Quality of Service guarantees, retained messages, and wildcard subscriptions makes it particularly suited for orchestrating global-scale agent federations [21, 22, 23, 24]. 

## **3 Federation of Agents System Architecture** 

This section details the core artifacts and mechanisms that compose our semantics-aware orchestration. We first introduce the artifacts’ Specs that guide each agent’s behaviour, then describe how these are embedded into our searchable profiles’ representation. Furthermore, we characterise the orchestrator (Agent-0) and the worker agents (Agent-1) before discussing the formation of semantic clusters and the DAG that governs execution order (Fig. 1). In this work, _federation of agents_ refers to runtime orchestration across heterogeneous agents and transports with policy-guarded data flow and capability discovery. This is distinct from _federated learning_ (FL), which concerns privacy-preserving model training. FoA can optionally include an FL _training_ phase by storing model-update and differentialprivacy parameters in VCVs and scheduling training/aggregation as DAG nodes; our experiments in this paper focus on the _inference-time_ orchestration setting. 

**Artifacts.** Each agent is associated with a _model specification_ , or _Spec_ , a document listing the agent’s goals, tools, resources, rules, and principles. Inspired by alignment frameworks emphasising that language assistants should be _helpful_ , _harmless_ and _honest_ [41, 42], a Spec typically combines high-level imperatives ("assist the user"; "do not break the policies") with detailed dos and don’ts (e.g., avoid certain words, report emergencies, respect privacy). Recent work on reinforcement learning from human feedback (RLHF) shows that language models can be fine-tuned to follow such instructions by leveraging human preference data and learning a reward model [41]; the resulting models more often adhere to the helpful, honest, harmless (HHH) criteria than models trained purely on next-token prediction [42]. In our framework, each agent memorises its Spec through such alignment techniques and learns to reason over it to follow instructions, refuse harmful requests, and resist the temptation to hallucinate citations or fabricate task completion (honest) as emphasised in alignment studies [41, 42, 43]. Specifications become machine-readable by embedding them into our VCVs using a specialised tokenizer and passed through a sentence-embedding model [44, 45] to obtain a dense vector summarising the agent’s profile. This _spec embedding_ augments the agent’s 

4 

skill and resource representations, ensuring that subsequent semantic routing takes account of both functional ability and behavioural constraints. Embedding Specs allows the orchestrator to query not only _"who knows how?"_ but also _"who aligns with what policies?"_ . 

**Versioned Capability Vectors.** A Versioned Capability Vector encodes the state of an agent in a searchable form. For agent _ai_ , we define 


![](P013_images/P013.pdf-0005-02.png)


where **c** _ai ∈_ R<sup>_d_</sup> is a dense capability embedding describing the agent’s core competencies, **s** _ai ∈ {_ 0 _,_ 1 _}_<sup>_ℓ_</sup> is a Bloom filter over discrete skills, **r** _ai ∈_ R<sup>_m_</sup> records resource requirements and qualityof-service guarantees (e.g., latency budget, energy consumption), **p** _ai ∈{_ 0 _,_ 1 _}_<sup>_p_</sup> encodes policy compliance flags (e.g. regulatory and security labels), **e** _ai ∈_ R<sup>_d′_</sup> is the spec embedding described above, and _vai ∈_ N is a version counter. The capability embedding **c** _ai_ is produced by feeding a natural-language description of the agent’s abilities through a pre-trained language model _ψ_ : _G →_ R<sup>_d_</sup> . Each time an agent updates its capabilities or specification, its version number increments, and a new VCV is broadcast. 

**Orchestrator (Agent-0).** We call the orchestrator of the federation Agent-0 (A-0). When an external task arrives, the orchestrator consults the current VCV index to discover candidate agents, performs dynamic decomposition, forms clusters, and orchestrates their collaboration. It maintains a sharded HNSW index over VCV embeddings to support sub-linear retrieval at scale. It also runs a lightweight ∆ _-gossip_ protocol to propagate VCV updates: rather than broadcasting full capability vectors, agents periodically exchange only the deltas between their local VCV sets. Task metadata and VCV updates are disseminated over MQTT `foa/meta` and `foa/retain` topics, respectively, allowing asynchronous, broadcast communications. During execution, the orchestrator subscribes to cluster channels (described in Sec. 4) and collects completion signals and intermediate artefacts. It merges partial results along a sub-task execution graph by traversing it in topological order, ensuring that dependencies are satisfied before downstream subtasks are synthesised. At completion, it publishes the final output on a `foa/result` topic, updates individual agents’ reputations based on grading feedback before disposing of them. 

**Decomposition and scheduling.** The orchestration process begins when Agent-0 receives a task _t_ from the environment. Rather than attempting to solve complex tasks monolithically, our system employs a hierarchical decomposition strategy that leverages the collective intelligence of the agent pool. Agent-0 first embeds the task description into a semantic space, then initiates a cooperative planning routine where multiple specialized agents propose candidate decompositions based on their domain expertise. These perspectives are synthesized into a consensual directed acyclic graph _G_ = ( _V, E_ ), where vertices represent atomic subtasks and edges encode execution dependencies. When the task structure is established, the orchestrator performs optimal agent assignment. To capture unique capabilities, resource constraints, and performance characteristics, we introduce a scoring function that evaluates agent-subtask pairs across four complementary dimensions: 


![](P013_images/P013.pdf-0005-06.png)


where sim measures semantic alignment between the subtask requirements and agent capabilities in the embedding space, the indicator I ensures policy compliance (required permissions **p** _si_ are within the agent’s authorization set **p** _aj_ ), _f is instantiated as a monotone penalty over resource gaps_ (latency, bandwidth, memory), decreasing as _∥_ **r** _si −_ **r** _aj ∥_ increases, and _g is instantiated as cosine similarity_ between specification embeddings _g_ ( **e** _si,_ **e** _aj_ ) = cos( **e** _si,_ **e** _aj_ ) _∈_ [ _−_ 1 _,_ 1] after _ℓ_ 2-normalization. This makes the gate explicit: any failed policy check zeros the score; otherwise, the score is down-weighted by resource mismatches and boosted by spec alignment. The orchestrator then transforms these compatibility scores into a concrete execution plan through constrained optimization. Formally, given _k_ = _|S|_ subtasks and _n_ = _|A|_ available agents, Agent-0 computes an optimal binary assignment matrix **X** _∈{_ 0 _,_ 1 _}_<sup>_k×n_</sup> that maximizes the expected utility: 


![](P013_images/P013.pdf-0005-08.png)


5 

subject to capacity constraints and _at-most-ri_ team size per subtask:<sup>�</sup> _j_<sup>_xij∈_[1</sup><sup>_, ri_]forall</sup><sup>_i_</sup> (single-agent when _ri_ =1). The resulting **X** gives the candidate team for each _si_ ; _cluster formation_ (Sec. 4) then groups selected agents solving the same _si_ for _k_ -round collaborative refinement before synthesis. This resolves the earlier single-agent/cluster tension by making teams first-class and clusters a subsequent refinement stage. 

**Agents (Agent-1).** Agents form the workforce of the federation. Each Agent-1 (A-1) is wrapped around a pre-aligned language model using Group Relative Policy Optimization (GRPO) [46]. The alignment leverages its Spec as a reward function and local domain data (documents, databases, and API outputs) to specialise the agent’s behaviour. Agents have access to a tool-use controller that automatically selects retrieval or computation tools (e.g., vector search, SQL query, web API) based on the current task; the available tools and corpora are reflected in the agent’s VCV resource vector **r** _ai_ . Internally, each agent maintains a scratchpad to store intermediate reasoning and implements the instructions in its Spec; for example, it declines unsafe requests and signals uncertainty when the Spec mandates honesty. When assigned a subtask, Agent-1 generates an initial draft solution by integrating its model output with the retrieved context. It then participates in cluster-based refinement rounds. To encourage diverse perspectives and reduce hallucinations, we group agents solving the same subtask into semantic clusters. Given a set of candidate agents _Asi_ for subtask _si_ , we compute a similarity matrix combining (i) the cosine similarity between their capability embeddings **c** _aj_ , (ii) the similarity of their preliminary outputs (once available) and (iii) the overlap of their spec embeddings **e** _aj_ . Hierarchical clustering on this matrix yields clusters _C_ 1 _, . . . , Cm_ of A-1 agents. Within each cluster, agents exchange intermediate drafts and critiques for _k_ rounds using the topic `foa/clusters/{cluster_id}/channel` . After each round, they vote on whether to stop; once consensus is reached, the cluster emits a `TASK_COMPLETE` signal and returns a refined subtask result. Clustering thus enables collaborative refinement akin to peer review while limiting communication overhead. 

## **4 Federation of Agents Execution Flow** 

In this section, we analyze the life cycle of a single task handled by FoA. The framework orchestrates the end-to-end execution of a complex problem through a six-phase pipeline that captures decomposition, drafting, collaboration, and synthesis. Formally, given an incoming task _t_ provided by the environment and a set of agents _A_ equipped with VCV, the orchestrator A-0 establishes a DAG _G_ = ( _S, E_ ) of sub-task execution order whose vertices correspond to (sub-task, A-1) pairs and whose edges encode relational dependencies between sub-tasks. Each phase described below operates on _G_ and updates its state until all nodes get detached from _G_ by completing sub-tasks or by receiving a `DISPATCH` signal. 

**Sub-task decomposition, consensus, and assignment.** Upon receiving a task _t_ from the environment, Agent-0 embeds its natural-language description into the semantic space and queries the VCV index for candidate agents. Each compatible agent _aj_ returns a proposal consisting of a set of subtasks _Saj_ and a set of dependencies _Eaj_ describing how those subtasks should be ordered. Agent-0 collects these proposals, merges them via a consensus mechanism, and validates acyclicity, thereby producing a global DAG _G_ = ( _S, E_ ) with _S_ =<sup>�</sup> _j_<sup>_Sa_</sup> _j_<sup>and</sup><sup>_E_=�</sup> _j_<sup>_Ea_</sup> _j_<sup>.The orchestrator then solves the</sup> assignment problem introduced in Sec. 1: it computes scores _αsi,aj_ for each subtask-agent pair based on semantic alignment, policy compliance, resource fit, and specification similarity. Solving the resulting integer program yields an assignment matrix **X** _∈{_ 0 _,_ 1 _}_<sup>_|S|×|A|_</sup> that maps each subtask _si_ to A-1 agents while respecting capacity constraints. FoA organises execution around _G_ : leaves (subtasks with no incoming edges) can begin immediately, whereas internal nodes _si_ wait until all predecessors _sj_ with ( _sj → si_ ) _∈ E_ have reported completion. A `SYNTH` tool combines results from predecessors when triggering a downstream subtask, enabling partial results to propagate forward without blocking unrelated branches and facilitating fine-grained concurrency in large workflows. 

**First draft with resource access.** Once assigned to a subtask _si_ , each A-1 retrieves relevant context from its local resources, such as databases or external tools, via tool-use controllers embedded in A-1. Conditioning on this context and its specification embedding **e** _aj_ , the agent produces a first-draft answer _d_<sup>(</sup> _i_<sup>_j_)</sup> for the subtask. This draft anchors subsequent refinement, which is posted to a cluster-specific MQTT channel associated with _si_ . The retrieval step could implement an additional 

6 


![](P013_images/P013.pdf-0007-00.png)



![](P013_images/P013.pdf-0007-01.png)



![](P013_images/P013.pdf-0007-02.png)



![](P013_images/P013.pdf-0007-03.png)



![](P013_images/P013.pdf-0007-04.png)


Figure 3: **Collaborative refinement inside a high-similarity cluster.** Agents with closely aligned capabilities on the same subtask are grouped into a cluster, exchange drafts and critiques for _k_ refinement rounds, and upon consensus emit `TASK_COMPLETE` to return a final subtask result to the orchestrator for synthesis. 

resource-aware step: the agent consults its resource vector **r** _aj_ to adjust re-spawn parameters, ensuring that within clusters, A-1 size (in GB of GPU vRAM), throughput velocity (in tok/sec), context window of the channel, and maximum budget of available tokens to produce solutions do not exceed latency or energy constraints. As shown later in Sec. 5, we found it practical to set-up A-1 as a pre-aligned small language model ( _≤_ 20 _B_ params) for fast-feedback execution of multiple refinement rounds over long-term horizons [41, 47, 27]. 

**Cluster formation via semantic similarity.** Agent-0 groups the agents assigned to the same subtask into collaborative clusters based on their capability vectors and preliminary outputs. Concretely, for subtask _si_ with assigned agents _Asi_ , we compute a similarity matrix combining (i) the cosine similarity of their capability embeddings **c** _aj_ , (ii) the cosine similarity of their draft embeddings and (iii) the overlap of their spec embeddings **e** _aj_ . Hierarchical clustering on this matrix yields clusters _C_ 1 _, . . . , Cm_ of size chosen to balance diversity against coordination overhead. A dedicated cluster channel `foa/clusters/{cluster_id}/channel` is created on the MQTT broker for each cluster, allowing members to share messages without interfering with other topics. Fig. 3 illustrates the refinement process inside a high-similarity cluster. 

**Intra-cluster execution** Within each cluster _Cj_ , agents iteratively refine their drafts. At round _r_ , every A-1 agent posts its current draft to the cluster channel and receives the drafts of its peers (Fig. 2). Agents critique and update their own answers by integrating insights from others, using simple majority voting or reputation-weighted aggregation to decide which components to adopt. Formally, let _M_<sup>(</sup> _s_<sup>_r_</sup> _i,C_<sup>)</sup> _j_<sup>denote the multiset of messages exchanged at round</sup><sup>_r_; refinement continues</sup> for _k_ rounds or until a consensus signal is triggered. Throughout this process, agents adhere to their Specs: they refuse to produce unsafe content, annotate uncertainties when appropriate, and propagate provenance metadata with each message. This collaborative refinement functions as a peer-review cycle that aims to improve factuality and reduce hallucinations. 

**Reporting to the orchestrator.** When the agents in cluster _Cj_ reach consensus on a refined answer 

_d_ ˆ<sup>(</sup> _i_<sup>_j_)</sup> for subtask _si_ , they emit a `TASK_COMPLETE` message on their cluster channel. This message contains the final answer along with evaluation metrics (e.g., confidence scores) computed by the cluster. Agent-0 subscribes to all cluster channels and listens for these completion signals. Upon receiving `TASK_COMPLETE` for _si_ , it marks the node as finished in the DAG _G_ and stores the result for use by downstream subtasks. If no consensus is reached within a predefined timeout, A-0 either reassigns the subtask to another agent or accepts the highest-scoring draft according to its evaluation function, thereby preventing deadlock. 

**Result synthesis.** After all clusters have reported completion, A-0 traverses _G_ in topological order. For each subtask _si_ , it invokes the `SYNTH` operator to combine the results of its predecessor subtasks with the refined answer for _si_ : 


![](P013_images/P013.pdf-0007-12.png)


7 


![](P013_images/P013.pdf-0008-00.png)


Figure 4: **HealthBench Hard results.** We report the overall score (mean _±_ bootstrap s.d.) and per-axis scores for FoA and baselines. Individual example scores can be negative, but average scores are clipped to zero. 

This operator may concatenate texts (default solution), resolve conflicting assertions across cluster outputs (i.e., `rebase` ), or summarise divergent perspectives into a unified answer (i.e., `merge` ). We implement `SYNTH` via meta-prompting [48] by steering the internal chain-of-thought of A-0 [49]. Once all leaves in the DAG are executed and their results propagated forward, the final answer for the original task _t_ is obtained at the root of _G_ . A-0 then publishes the final solution on `foa/result` MQTT topic, updates the reputations of participating agents based on the quality of their contributions, and archives their updated VCVs for future routing decisions. Many phases are parallelized and cluster sizes are capped (3-5), supporting horizontal scalability before large-scale deployment. We quantify end-to-end complexity in Appendix (A). 

## **5 Evaluation and Experimental Results** 

We evaluate the FoA framework on OpenAI’s HealthBench Hard [50], a comprehensive benchmark for assessing language models in healthcare contexts. HealthBench Hard comprises 1,000 multi-turn conversations between models and users (both healthcare professionals and patients), with responses evaluated against physician-written rubrics spanning 48,562 unique criteria. The rubrics assign positive or negative points depending on whether a response satisfies desirable or undesirable criteria; scores range between _−_ 10 and 10 and are combined into a per-example score by a model-based grader that has been validated against physician judgments. The overall HealthBench score is obtained by averaging per-example scores and clipping the mean to the range [0 _,_ 1]. Unlike traditional multiple-choice medical benchmarks, HealthBench contains an open-ended nature of real healthcare interactions through conversation-specific evaluation across seven themes (emergency referrals, context seeking, global health, health data tasks, expertise-tailored communication, responding under uncertainty, and response depth) and five behavioural axes (accuracy, completeness, context awareness, communication quality, and instruction following). In Sec. C, we provide additional details on specific configuration parameters and implementation decisions. 

**Main Results.** Fig. 4 summarises the performance of FoA and the baselines on HealthBench Hard. FoA achieves an overall score of 0 _._ 13, a _13x_ relative improvement over the best single agent baseline (Medgemma [51]) and a _6.5x_ improvement over the uncoordinated ensemble. Random assignment performs markedly worse, underscoring the importance of capability-aware routing. FoA consistently outperforms baselines across all seven themes. The collaborative cluster protocol particularly benefits high-stakes questions where multiple perspectives improve accuracy and context awareness. 

8 

## **6 Conclusion & Discussion** 

We presented Federation of Agents (FoA), a semantics-aware communication fabric that enables dynamic, capability-driven orchestration of large-scale multi-agent AI systems. Through machinereadable Versioned Capability Vectors (VCVs) and cost-aware semantic routing, FoA transforms static topic-based coordination into a scalable infrastructure for efficient reasoning over extended horizons, solving a coordination problem in agentic AI regarding _who can do what, at what cost, and with what reputation?_ 

**Limitations and Open Research Questions.** Several challenges limit our current approach and represent important directions for the community. The effectiveness of semantic routing is bounded by embedding quality, creating a cold-start problem where agents with novel capabilities may remain underutilized until sufficient interaction data is collected. Our clustering algorithm may form sub-optimal groups when task similarity metrics fail to capture true collaboration potential, triggering a fallback mechanism that often leads to reduced effectiveness in heterogeneous domains. The VCV representation, while expressive, may not capture complex compositional capabilities or dynamic skill emergence during agent execution. Communication overhead scales quadratically within clusters, limiting the practical cluster size to 3-5 agents. Additionally, while our reputation and policy enforcement mechanisms provide robust security against honest-but-curious adversaries, sophisticated attacks such as coordinated Sybil networks or adversarial capability misrepresentation remain open challenges that can be mitigated by using sandbox executions [26]. 

**Future Research Directions.** Our immediate research focuses on four critical frontiers. First, we will develop reinforcement learning-based adaptive routing controllers that can dynamically optimize cost-biasing, matching thresholds, and clustering parameters based on real-time network performance and evolving task priorities. Second, we plan to explore cross-cluster communication protocols to enable knowledge sharing between related clusters while maintaining scalability. Third, we will integrate zero-knowledge proof systems and trusted execution environments to enable verifiable capability attestations, directly addressing the trust assumptions in our current design, integrating the security and safety measures of [26] in FoA. 

**Broader Impact and Societal Considerations.** Large-scale federations of AI agents present both transformative opportunities and significant risks. On the positive side, democratizing access to specialized AI capabilities could accelerate scientific discovery, improve resource allocation efficiency, and enable more responsive technological infrastructures. However, the concentration of autonomous decision-making capabilities raises concerns about algorithmic bias amplification, privacy preservation across agent boundaries, and the increasing opacity of accountability structures. The governance mechanisms embedded in FoA, including auditable provenance trails and policy-ascode enforcement, represent necessary but insufficient steps toward responsible deployment. The broader AI community must engage in continued dialogue about appropriate legal frameworks, ethical guidelines, and oversight mechanisms for autonomous agentic ecosystems. 

In conclusion, the Federation of Agents provides a theoretically grounded and practically scalable approach to multi-agent coordination that transforms capabilities and constraints into a searchable, auditable substrate. Our smart clustering innovations demonstrate that collaborative refinement can significantly improve solution quality while maintaining computational tractability. Addressing core challenges in semantic routing, distributed orchestration, intra-agent collaboration, and trust management establishes a foundation for the next generation of collaborative AI systems. The 10x performance improvements on HealthBench with respect to the best single agent validate the practical benefits of capability-driven orchestration with smart clustering. We invite the research community to build upon these contributions as we collectively advance toward more capable, trustworthy, and socially beneficial agentic AI ecosystems. 

9 

## **References** 

- [1] Ranjan Sapkota, Konstantinos I Roumeliotis, and Manoj Karkee. Ai agents vs. agentic ai: A conceptual taxonomy, applications and challenges. _arXiv preprint arXiv:2505.10468_ , 2025. 

- [2] Johannes Schneider. Generative to agentic ai: Survey, conceptualization, and challenges. _arXiv preprint arXiv:2504.18875_ , 2025. 

- [3] Mourad Gridach, Jay Nanavati, Khaldoun Zine El Abidine, Lenon Mendes, and Christina Mack. Agentic ai for scientific discovery: A survey of progress, challenges, and future directions. _arXiv preprint arXiv:2503.08979_ , 2025. 

- [4] Yongliang Shen, Kaitao Song, Xu Tan, Dongsheng Li, Weiming Lu, and Yueting Zhuang. Hugginggpt: Solving ai tasks with chatgpt and its friends in hugging face. _Advances in Neural Information Processing Systems_ , 36:38154–38180, 2023. 

- [5] Yanwei Yue, Guibin Zhang, Boyang Liu, Guancheng Wan, Kun Wang, Dawei Cheng, and Yiyan Qi. Masrouter: Learning to route llms for multi-agent systems. _arXiv preprint arXiv:2502.11133_ , 2025. 

- [6] Yuhan Wang, Shuo Guo, Yang Pan, Zhi Su, Fuxiang Chen, Tom H. Luan, Peng Li, Jun Kang, and Dusit Niyato. Internet of agents: Fundamentals, applications, and challenges. _arXiv preprint arXiv:2505.07176_ , 2025. 

- [7] Qingyun Wu, Gagan Bansal, Jieyu Zhang, Yiran Wu, Beibin Li, Erkang Zhu, Li Jiang, Xiaoyun Zhang, Shaokun Zhang, Jiale Liu, et al. Autogen: Enabling next-gen llm applications via multi-agent conversations. In _First Conference on Language Modeling_ , 2024. 

- [8] Sirui Hong, Mingchen Zhuge, Jonathan Chen, Xiawu Zheng, Yuheng Cheng, Ceyao Zhang, Jinlin Wang, Zili Wang, Steven Ka Shing Yau, Zijuan Lin, et al. Metagpt: Meta programming for a multi-agent collaborative framework. In _International Conference on Learning Representations (ICLR)_ , 2024. 

- [9] Guohao Li, Hasan Hammoud, Hani Itani, Dmitrii Khizbullin, and Bernard Ghanem. Camel: Communicative agents for" mind" exploration of large language model society. _Advances in Neural Information Processing Systems_ , 36:51991–52008, 2023. 

- [10] Herminio Paucar Curasma, Che Fan Pan, and Julio Cezar Estrella. Agents for automatic control of sensors using multi-agent systems and ontologies: A scalable iot architecture. _Procedia Computer Science_ , 238:404–411, 2024. 

- [11] Nima Seifi and Manish Chugh. Multi-llm routing strategies for generative ai applications on AWS. `https://aws.amazon.com/blogs/machine-learning/ multi-llm-routing-strategies-for-generative-ai-applications-on-aws/` , April 2025. AWS Machine Learning Blog. 

- [12] Andrew Banks, Ed Briggs, Ken Borgendale, and Rahul Gupta. Mqtt version 5.0, March 2019. OASIS Standard. 

- [13] EMQ Technologies. Harnessing LLM with MQTT: A comprehensive technical overview for ai/iot integration. Whitepaper, EMQ Technologies, 2024. 

- [14] Nouf Saeed Alotaibi, Hassan I Sayed Ahmed, Samah Osama M Kamel, and Ghada Farouk ElKabbany. Secure enhancement for mqtt protocol using distributed machine learning framework. _Sensors_ , 24(5):1638, 2024. 

- [15] Subash Neupane, Sudip Mittal, and Shahram Rahimi. Towards a hipaa compliant agentic ai system in healthcare. _arXiv preprint arXiv:2504.17669_ , 2025. 

- [16] Yiming Xiong, Jian Wang, Bing Li, Yuhan Zhu, and Yuqi Zhao. Self-organizing agent network for llm-based workflow automation. _arXiv preprint arXiv:2508.13732_ , 2025. 

10 

- [17] Jing Piao, Yanyan Yan, Jiawei Zhang, Ning Li, Jin Yan, Xin Lan, Zhiheng Lu, Zhaolei Zheng, Jinyu Wang, Dong Zhou, and Chen Gao. Agentsociety: Large-scale simulation of llm-driven generative agents advances understanding of human behaviors and society. _arXiv preprint arXiv:2502.08691_ , 2025. 

- [18] Yury A. Malkov and Dmitry A. Yashunin. Efficient and robust approximate nearest neighbor search using hierarchical navigable small world graphs. _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 42(4):824–836, 2018. 

- [19] Fabiana Fournier, Lior Limonad, and Yuval David. Agentic ai process observability: Discovering behavioral variability. _arXiv preprint arXiv:2505.20127_ , 2025. 

- [20] Andrew C. Wong, Duncan McFarlane, Chris Ellarby, Monica Lee, and Mike Kuok. Intelligent product 3.0: Decentralised ai agents and web3 intelligence standards. _arXiv preprint arXiv:2505.07835_ , 2025. 

- [21] Dezhang Kong, Shi Lin, Zhenhua Xu, Zhebo Wang, Minghao Li, Yufeng Li, Yilun Zhang, Hujin Peng, Zeyang Sha, Yuyuan Li, et al. A survey of llm-driven ai agent communication: Protocols, security risks, and defense countermeasures. _arXiv preprint arXiv:2506.19676_ , 2025. 

- [22] Yingxuan Yang, Huacan Chai, Yuanyi Song, Siyuan Qi, Muning Wen, Ning Li, Junwei Liao, Haoyi Hu, Jianghao Lin, Gaowei Chang, et al. A survey of ai agent protocols. _arXiv preprint arXiv:2504.16736_ , 2025. 

- [23] Mohammed Mehedi Hasan, Hao Li, Emad Fallahzadeh, Gopi Krishnan Rajbahadur, Bram Adams, and Ahmed E Hassan. Model context protocol (mcp) at first glance: Studying the security and maintainability of mcp servers. _arXiv preprint arXiv:2506.13538_ , 2025. 

- [24] Xinyi Hou, Yanjie Zhao, Shenao Wang, and Haoyu Wang. Model context protocol (mcp): Landscape, security threats, and future research directions. _arXiv preprint arXiv:2503.23278_ , 2025. 

- [25] CAFEIN<sup>®</sup> : CERN’s federated ai platform. `https://cafein.web.cern.ch` . 

- [26] Diogo Reis Santos, Albert Sund Aillet, Antonio Boiano, Usevalad Milasheuski, Lorenzo Giusti, Marco Di Gennaro, Sanaz Kianoush, Luca Barbieri, Monica Nicoli, Michele Carminati, et al. A federated learning platform as a service for advancing stroke management in european clinical centers. In _2024 IEEE International Conference on E-health Networking, Application & Services (HealthCom)_ , pages 1–7. IEEE, 2024. 

- [27] Peter Belcak, Greg Heinrich, Shizhe Diao, Yonggan Fu, Xin Dong, Saurav Muralidharan, Yingyan Celine Lin, and Pavlo Molchanov. Small language models are the future of agentic ai. _arXiv preprint arXiv:2506.02153_ , 2025. 

- [28] Shaina Raza, Ranjan Sapkota, Manoj Karkee, and Christos Emmanouilidis. Trism for agentic ai: A review of trust, risk, and security management in llm-based agentic multi-agent systems. _arXiv preprint arXiv:2506.04133_ , 2025. 

- [29] Erik Miehling, Karthikeyan Natesan Ramamurthy, Kush R Varshney, Matthew Riemer, Djallel Bouneffouf, John T Richards, Amit Dhurandhar, Elizabeth M Daly, Michael Hind, Prasanna Sattigeri, et al. Agentic ai needs a systems theory. _arXiv preprint arXiv:2503.00237_ , 2025. 

- [30] Francesco Piccialli, Diletta Chiaro, Sundas Sarwar, Donato Cerciello, Pian Qi, and Valeria Mele. Agentai: A comprehensive survey on autonomous agents in distributed ai for industry 4.0. _Expert Systems with Applications_ , 291:128404, 2025. 

- [31] Anthropic. Introducing the model context protocol. `https://www.anthropic.com/news/ model-context-protocol` , November 2024. 

- [32] Model context protocol specification: Transports (http with sse / streamable http) and concepts. `https://modelcontextprotocol.io/specification/2024-11-05/basic/ transports` , November 2024. 

11 

- [33] Vineeth Sai Narajala and Om Narayan. Securing agentic ai: A comprehensive threat model and mitigation framework for generative ai agents. _arXiv preprint arXiv:2504.19956_ , 2025. 

- [34] Yuchen Li, Hengyi Cai, Rui Kong, Xinran Chen, Jiamin Chen, Jun Yang, Haojie Zhang, Jiayi Li, Jiayi Wu, Yiqun Chen, et al. Towards ai search paradigm. _arXiv preprint arXiv:2506.17188_ , 2025. 

- [35] Ádám Péter and Samuel Werner. The impact of unified namespace in industry 4.0, 2024. 

- [36] EMQX Team. Mcp over mqtt: Empowering agentic iot with emqx for ai-driven intelligence. `https://www.emqx.com/en/blog/mcp-over-mqtt` , April 2025. 

- [37] Benniu Ji. Integrating claude with mqtt: An introduction to emqx mcp server. `https://www. emqx.com/en/blog/integrating-claude-with-mqtt` , March 2025. 

- [38] EMQX. Emqx mcp gateway (mcp server gateway plugin). `https://github.com/emqx/ emqx-plugin-mcp-gateway` , 2025. 

- [39] mqtt ai. Esp-idf mcp over mqtt sdk (esp32 component). `https://components.espressif. com/components/mqtt-ai/esp-mcp-over-mqtt/versions/0.0.1` , August 2025. 

- [40] Abdelrahman Elewah and Khalid Elgazzar. Agentic search engine for real-time iot data. _arXiv preprint arXiv:2503.12255_ , 2025. 

- [41] Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, et al. Training language models to follow instructions with human feedback. _Advances in neural information processing systems_ , 35:27730–27744, 2022. 

- [42] Amanda Askell, Yuntao Bai, Anna Chen, Dawn Drain, Deep Ganguli, Tom Henighan, Andy Jones, Nicholas Joseph, Ben Mann, Nova DasSarma, Nelson Elhage, Zac Hatfield-Dodds, Danny Hernandez, Jackson Kernion, Kamal Ndousse, Catherine Olsson, Dario Amodei, Tom Brown, Jack Clark, Sam McCandlish, Chris Olah, and Jared Kaplan. A general language assistant as a laboratory for alignment. _arXiv preprint arXiv:2112.00861_ , 2021. 

- [43] Yuqing Yang, Ethan Chern, Xipeng Qiu, Graham Neubig, and Pengfei Liu. Alignment for honesty. _Advances in Neural Information Processing Systems_ , 37:63565–63598, 2024. 

- [44] Zach Nussbaum, John X Morris, Brandon Duderstadt, and Andriy Mulyar. Nomic embed: Training a reproducible long context text embedder. _arXiv preprint arXiv:2402.01613_ , 2024. 

- [45] Min Choi, Sahil Dua, and Alice Lisak. Introducing embeddinggemma: The best-in-class open model for on-device embeddings, 2025. Google for Developers. 

- [46] Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan Zhang, YK Li, Yang Wu, et al. Deepseekmath: Pushing the limits of mathematical reasoning in open language models. _arXiv preprint arXiv:2402.03300_ , 2024. 

- [47] Jiaming Ji, Tianyi Qiu, Boyuan Chen, Borong Zhang, Hantao Lou, Kaile Wang, Yawen Duan, Zhonghao He, Jiayi Zhou, Zhaowei Zhang, et al. Ai alignment: A comprehensive survey. _arXiv preprint arXiv:2310.19852_ , 2023. 

- [48] Mirac Suzgun and Adam Tauman Kalai. Meta-prompting: Enhancing language models with task-agnostic scaffolding. _arXiv preprint arXiv:2401.12954_ , 2024. 

- [49] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou, et al. Chain-of-thought prompting elicits reasoning in large language models. _Advances in neural information processing systems_ , 35:24824–24837, 2022. 

- [50] Rahul K. Arora, Jason Wei, Rebecca Soskin Hicks, Preston Bowman, Joaquin QuiñoneroCandela, Foivos Tsimpourlas, Michael Sharman, Meghan Shah, Andrea Vallone, Alex Beutel, Johannes Heidecke, and Karan Singhal. Healthbench: Evaluating large language models towards improved human health, 2025. OpenAI technical report. 

12 

- [51] Andrew Sellergren, Sahar Kazemzadeh, Tiam Jaroensri, Atilla Kiraly, Madeleine Traverse, Timo Kohlberger, Shawn Xu, Fayaz Jamil, Cían Hughes, Charles Lau, et al. Medgemma technical report. _arXiv preprint arXiv:2507.05201_ , 2025. 

- [52] Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, and Yuan Cao. React: Synergizing reasoning and acting in language models. In _International Conference on Learning Representations (ICLR)_ , 2023. 

- [53] Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik Narasimhan, and Shunyu Yao. Reflexion: Language agents with verbal reinforcement learning. _Advances in Neural Information Processing Systems_ , 36:8634–8652, 2023. 

- [54] Maciej Besta, Nils Blach, Ales Kubicek, Robert Gerstenberger, Michal Podstawski, Lukas Gianinazzi, Joanna Gajda, Tomasz Lehmann, Hubert Niewiadomski, Piotr Nyczyk, et al. Graph of thoughts: Solving elaborate problems with large language models. In _Proceedings of the AAAI conference on artificial intelligence_ , volume 38, pages 17682–17690, 2024. 

- [55] Jef JJ van den Hout and Owen C Davis. Promoting the emergence of team flow in organizations. _International Journal of Applied Positive Psychology_ , 7:143–189, 2022. 

13 

## **A Detailed Algorithm Analysis** 

In this section, we formalise each stage of the FoA execution pipeline from an algorithmic perspective. Our analysis clarifies the internal mechanics and quantifies the computational complexity to link the design to prior literature. We follow the six phases outlined in Section 4: (1) dynamic task decomposition, (2) first draft generation, (3) cluster formation, (4) intra-cluster consensus, (5) reporting, and (6) synthesis. 

**Phase 1: Dynamic task decomposition and consensus.** Given an input task `t` , the orchestrator searches for compatible agents and constructs a directed acyclic graph (DAG) of subtasks. The procedure, formalised in Algorithm 1, embeds the task into the capability space, evaluates each agent’s compatibility score against semantic, policy, and resource criteria, and queries a sharded HNSW index to retrieve the most promising candidates. Selected agents propose candidate subtask sets and dependency structures; these proposals are merged via a consensus mechanism into a single DAG and validated for acyclicity and consistency. Our design draws inspiration from recent multiagent frameworks that dynamically decompose complex tasks into manageable subtasks and tailor subagents for each subproblem. With this dynamic decomposition based on intermediate results and dedicated subagents assignments, FoA avoids the error propagation and static limitations of preliminary decomposition schemes. 

**Algorithm 1** Dynamic Task Decomposition Protocol 

|**Input:** Task`t`_∈T_, Set of A-1 Agents_A_, threshold_τ_, polic|y constraints**P**|
|---|---|
|**Output:** Task DAG_G_= (_V, E_)with subtasks_V_ =_S_ and|dependencies_E_|
|1: **Phase 1a:** Task embedding and agent scoring<br>||
|2: **c**`t` _←ψ_(`t`)<br>|_▷_embed task description into capability space<br>|
|3: _Acomp ←∅_<br>|_▷_candidate agent set|
|4: **for**each_ai ∈A_**do**<br><br>||
|5:<br>_αt,ai ←_sim(**c**_t,_**c**_ai_)_· µ_(**P**_,_**p**_ai_)_·_cost(**r**_t,_**r**_ai_)<br><br>||
|6:<br>**if**_αt,ai > τ_ **then**<br>||
|7:<br>_Acomp ←Acomp ∪{ai}_<br>|_▷_retain compatible agents|
|8:<br>**end if**||
|9: **end for**<br>||
|10: **if**_|Acomp|_= 0**then**<br>||
|11:<br>_Acomp ←_TopK(_A,_sim(**c**_t,_**c**_aj_)_, k_)|_▷_fallback retrieval|
|12: **end if**||
|13: **Phase 1b:** Collaborative proposal and merge||
|14: _Sprop ←∅_,_Eprop ←∅_||
|15: **for**each_ai ∈Acomp_ **do**||
|16:<br>subtasks_ai ←_DECOMPOSE(_t,_**c**_ai_)|_▷_agent-specifc decomposition|
|17:<br>deps_ai ←_ANALYZE_DEPS(subtasks_ai_)|_▷_local dependency analysis|
|<br>18:<br>_Sprop ←Sprop ∪_subtasks_ai_||
|19:<br>_Eprop ←Eprop ∪_deps_ai_||
|20: **end for**||
|21: _G ←_SYNTH_PROPOSALS(_Sprop, Eprop_)|_▷_consensus on subtask set and edges|
|22: _G ←_VALIDATE_DAG(_G_)<br>23: **return**_G_|_▷_remove cycles and inconsistencies|



The time complexity of Phase 1 is dominated by evaluating compatibility scores and merging proposals. Let _n_ = _|A|_ and _m_ be the number of candidate agents retrieved; computing similarities for all agents requires _O_ ( _n d_ ) operations where _d_ is the embedding dimension. Each agent proposes _O_ ( _|S|_ ) subtasks; merging proposals requires at most _O_ ( _m |S|_ log _|S|_ ) time to reconcile duplicates and validate the DAG. Dynamic decomposition improves robustness by allowing later phases to adjust subtasks based on intermediate outputs, a key advantage over static splitting. 

**Phase 2: First draft generation with resource access.** Once the DAG is established and subtasks are assigned to agents, each agent retrieves context and produces an initial answer. The process resembles iterative reasoning methods such as ReAct [52], Reflexion [53], or Graph of Thoughts [54], where intermediate thoughts guide subsequent actions. However, in FoA, the first draft is produced individually by each assigned agent before collaborative refinement. Algorithm 2 formalises this stage. 

14 

**Algorithm 2** First Draft Generation 

**Input:** Subtask _s ∈S_ , assigned agent set _As_ **Output:** Draft set _Ds_ containing one draft per agent 1: _Ds ←∅_ 2: **for** each agent _ai ∈As_ **do** 3: context _←_ RETRIEVE_RESOURCES( _s, ai_ ) _▷_ query local resources, use tools 4: draft _←_ GENERATE_ANSWER( _s,_ context _,_ Spec _ai_ ) _▷_ LLM inference conditioned on Spec 5: _Ds ←Ds ∪{_ ( _ai,_ draft) _}_ 6: **end for** 7: **return** _Ds_ 

Each agent’s retrieval call and model inference contributes to the complexity of this phase. If _ri_ denotes the retrieval cost and _ti_ denotes the model run time for agent _ai_ , then the total complexity is _O_ (<sup>�</sup> _ai∈As_<sup>(</sup><sup>_ri_+</sup><sup>_ti_)).Because draft generation is parallel across agents, it scales horizontally with</sup> the number of assigned agents. 

**Phase 3: Cluster formation via semantic similarity.** To encourage team flow while controlling communication overhead, FoA groups agents working on the same subtask into clusters based on similarity across multiple dimensions (capability, resource cost, initial draft quality, and specification) [55]. The orchestrator builds a similarity matrix for _As_ and performs hierarchical clustering to partition agents into clusters. Algorithm 3 formalises this procedure. 

### **Algorithm 3** Semantic Cluster Formation 

**Input:** Subtask _s_ , agents _As_ , draft set _Ds_ , weight vector ( _w_ 1 _, w_ 2 _, w_ 3 _, w_ 4) **Output:** Cluster partition _Cs_ = _{C_ 1 _, . . . , Cm}_ 1: _n ←|As|_ 2: Initialize _S ∈_ R<sup>_n×n_</sup> _▷_ similarity matrix 3: **for** each pair _i < j_ **do** 4: _Si,j ← w_ 1 _·_ cos( **c** _ai ,_ **c** _aj_ ) + _w_ 2 _·_ cos( **r** _ai ,_ **r** _aj_ ) 5: + _w_ 3 _·_ cos( _ψ_ (draft _ai_ ) _, ψ_ (draft _aj_ )) + _w_ 4 _·_ cos( **e** _ai ,_ **e** _aj_ ) 6: _Sj,i ← Si,j_ 7: **end for** 8: _Cs ←_ HIER_CLUSTER( _S_ ) _▷_ agglomerative clustering with cut threshold 9: **return** _Cs_ 

Constructing the similarity matrix requires _O_ ( _n_<sup>2</sup> _d_ ) operations, and agglomerative clustering adds an _O_ ( _n_<sup>2</sup> log _n_ ) factor, yielding a total complexity of _O_ ( _n_<sup>2</sup> ( _d_ + log _n_ )), consistent with the analysis in the main text. 

**Phase 4: Intra-cluster execution and consensus.** Within each cluster, agents iteratively share and refine their solutions until consensus is reached. This process can be viewed as a distributed consensus protocol in which agents negotiate a common answer through repeated information exchange. Such protocols have deep roots in distributed control theory: consensus algorithms guarantee that agents converge to a shared value through local information exchange under suitable connectivity assumptions. Algorithm 4 codifies our intra-cluster execution. 

The complexity of the intra-cluster protocol depends on the cluster size _|C|_ and the number of rounds _k_ . Each round involves an all-to-all exchange within the cluster followed by a local aggregation, giving _O_ ( _k |C|_<sup>2</sup> ) communication steps. In practice, we limit cluster sizes to 3-5 agents to balance diversity and overhead, avoiding significant costs. 

**Phase 5: Reporting and DAG updates.** After consensus, each cluster emits a `TASK_COMPLETE` message containing the refined answer. The orchestrator subscribes to these messages on the appropriate MQTT channel and updates the DAG state, marking subtask _s_ as complete. If consensus cannot be reached within the allotted rounds _k_ , the orchestrator either reassigns the subtask or accepts the highest-scoring draft, mirroring fallback behaviours in classical multi-agent planning. Reporting is a constant-time operation per subtask and therefore does not dominate the overall complexity. 

15 

### **Algorithm 4** Intra-Cluster Consensus Execution 

|**Input:** Subtask_s_, cluster_C_, refnement rounds_k_, weights vector_w_||
|---|---|
|**Output:** Final consensus answer ans_C_||
|1: Initialize local answers ans_i ←_draft_ai_ for each_ai ∈C_||
|2: **for**_r_ = 1to_k_**do**<br>||
|3:<br>**for**each_ai ∈C_ in parallel**do**||
|4:<br>Broadcast ans_i_ to all peers and receive their answers<br>||
|5:<br>ans_i ←_`UPDATE`(_{_ans_j_ :_aj ∈C}, w_)|_▷_weighted aggregation/voting|
|6:<br>**end for**||
|7:<br>**if**`TASK_COMPLETE`in all_{_ans_j_ :_aj ∈C}_**then**||
|8:<br>**break**||
|9:<br>**end if**||
|10: **end for**||
|11: Choose representative answer ans_C_ (e.g., by majority or highest weight)<br>||
|12: **return**ans_C_||



**Phase 6: Result synthesis and merging.** Once all subtasks have reported completion, the orchestrator synthesises the final answer by traversing the DAG _G_ in topological order and merging the outputs of predecessors with the current subtask result. Algorithm 5 describes this synthesis. 

### **Algorithm 5** Result Synthesis and Merging 

|**Input:** DAG_G_= (_S, E_), answers_{_ans_si_ :_si ∈S}_||
|---|---|
|**Output:** Final solution ans_t_||
|1: ans_t ←∅_||
|2: **for**each_si_ in topological order**do**||
|3:<br>pre_←{_ans_sj_ : (_sj →si_)_∈E}_|_▷_predecessor answers|
|4:<br>combined_←_SYNTH(pre_∪{_ans_si}_)|_▷_merge operator|
|5:<br>ans_si ←_combined||
|6: **end for**||
|7: Set ans_t ←_ans_sroot_ or merge sink nodes||
|8: **return**ans_t_||



Topological traversal and merging runs in _O_ ( _|S|_ + _|E|_ ) time, as each subtask is processed exactly once and the merge operator combines a bounded number of predecessor answers. This final phase ensures that dependencies are respected and partial results are propagated forward without blocking unrelated branches, realizing the fine-grained concurrency promised by the DAG model. 

**Summary of complexity.** Bringing the phases together, the overall complexity of the FoA execution pipeline for a single task is 


![](P013_images/P013.pdf-0016-07.png)

### Figure analysis

The figure presents the overall asymptotic complexity of the FoA execution pipeline, decomposed by execution phase.

Readable equation structure:

\[
O\left(nd + m|S|\log |S|\right)
+ O\left(\sum_{s\in S}\sum_{a_i\in A_s}(r_i+t_i)\right)
+ O\left(\sum_{s\in S}|A_s|^2(d+\log |A_s|)\right)
+ O\left(\sum_{C\in \mathcal{C}} k|C|^2\right)
+ O\left(|S|+|E|\right)
\]

The right side annotates the five terms as:

1. Dynamic Task Decomposition, labeled equation (5).
2. First Draft Generation, labeled equation (6).
3. Semantic Cluster Formation, labeled equation (7).
4. Cluster Consensus, labeled equation (8).
5. Synthesis, labeled equation (9).

Direct visual observations:

- The expression is a vertical multi-line complexity summary rather than a plot or chart.
- Each big-O term is paired with a textual phase label using a triangular annotation marker.
- The final term is \(O(|S|+|E|)\), matching the surrounding text's statement that topological traversal over the DAG processes subtasks and edges once.
- The cluster consensus term scales with \(k|C|^2\) summed over clusters, indicating dependence on refinement rounds and quadratic communication or aggregation within each cluster.
- The semantic cluster formation term includes \(|A_s|^2\), indicating pairwise or quadratic operations among agents assigned to each subtask.

Interpretation in context:

- The equation supports the paper's claim that total FoA runtime can be viewed as the additive cost of decomposition, draft generation, clustering, consensus, and final synthesis.
- It connects directly to the preceding Algorithm 5 by assigning the final synthesis phase a linear DAG traversal cost, \(O(|S|+|E|)\).
- The surrounding text argues that although the summed expression contains potentially expensive terms, many phases can run in parallel and clusters are expected to remain small in practice, mitigating end-to-end cost.


where the terms correspond respectively to dynamic decomposition and proposal merging, initial draft generation, cluster formation, intra-cluster consensus, and final synthesis. In practice, many of these phases execute in parallel, and cluster sizes remain small, yielding efficient end-to-end execution. Our design thus achieves the adaptability and flexibility promised by dynamic task decomposition and multi-agent collaboration. 

16 

## **B MQTT Implementation Details** 

**MQTT Topic Hierarchy.** FoA uses a structured topic namespace: 

- `foa/orchestrator/jobs` - Job submissions 

- `foa/agents/{agent_id}/tasks` - Individual agent tasks 

- `foa/clusters/{cluster_id}/channel` - Intra-cluster communication 

- `foa/capabilities/updates` - VCV updates 

- `foa/policies/enforcement` - Policy compliance events 

**Embedding Pipeline.** VCV embeddings use a two-stage process: 

1. Raw capability descriptions processed through a specialized tokenizer 

2. 768-dimensional embeddings generated via Nomic Embed [44] 

3. L2 normalization applied for cosine similarity computation 

4. Optional dimensionality reduction to 256 for storage efficiency 

## **C Additional Experimental Results** 

Our evaluation compares FoA against several baselines. For each task, we instantiate four _Agent1_ models with Specs covering a broad spectrum of general medicine; each is a large language model fine-tuned from a foundation model using Group Relative Policy Optimisation (GRPO) on its domain data [46]. Baselines include (i) the best individual agent (selected according to its standalone HealthBench Hard score), (ii) an _uncoordinated ensemble_ that averages the four agents’ responses without decomposition or clustering, and (iii) _random assignment_ , where subtasks are assigned to agents uniformly at random without consulting their capability vectors. All systems enforce the same AI safety policies via a Bloom filter that blocks prompts containing unsafe content. 

We configure FoA as follows. The orchestrator maintains a sharded HNSW index over 256dimensional Versioned Capability Vectors and performs semantic routing with a similarity threshold _αa_ = 0 _._ 3 ( `FOE_DECOMP_THRESHOLD` ). At most four agents are considered to propose decompositions ( `FOE_DECOMP_MAX_AGENTS` ), and each task is split into between two and four subtasks ( `FOE_DECOMP_SUBTASKS_MIN/MAX` ). Candidate decompositions are merged when their subtask embeddings have a cosine similarity of at least 0 _._ 5 ( `FOE_DECOMP_MERGE_SIM` ). Clustering is enabled and uses EMQX v5 [13] as the MQTT broker. Agents in a cluster communicate over a dedicated topic for a maximum of _k_ = 3 refinement rounds; clusters are restricted to one to four agents with a formation threshold of 0 _._ 2 ( `FOE_CLUSTER_SIM_THRESHOLD` ), allowing A-1 agents to participate in more than one cluster with a single job timeout of 300 s (Fig. 3). Agent processes run on **one** NVIDIA GPU optimizing for latency and energy consumption using a 4-bit quantized small language model from a pool of four classes of pre-aligned small language models: GEMMA3, QWEN3, DEEPSEEK-R1, GPT-OSS. In our experiments, we considered only small language models with a maximum of 20B parameters that could run on consumer-scale hardware using the Ollama API. In this particular experiment, we set medgemma3 [51] as the default pick from the gemma3 family. We used MEDGEMMA:27B as the grader used for HealthBench evaluation on a separate cluster, and we report the mean and bootstrap standard deviation over three random seeds. Responses are generated for all 1,000 HealthBench Hard conversations and evaluated using the official `simple-evals` pipeline. 

**Assets Used** The language models considered in this work include GEMMA3, QWEN3, DEEPSEEKR1, and GPT-OSS. GEMMA3 is distributed under Google’s Gemma Terms of Use, QWEN3 under the Apache License 2.0, DEEPSEEK-R1 under the MIT License, and GPT-OSS under the Apache License 2.0. The OpenAI HEALTHBENCH benchmark (dataset) and the accompanying reference evaluation code are made available under the MIT License. 

**Used Computer Resources** All experiments were conducted on a workstation equipped with an **Intel**<sup>**®**</sup> **Xeon**<sup>**®**</sup> **w5-2455X CPU** (64-bit, AVX-512 enabled) and **63 GB of system memory** . Computations were accelerated using an **NVIDIA**<sup>**®**</sup> **RTX™A4000 GPU** with **16 GB of GDDR6** 

17 

**memory** (CUDA 12.8, driver 573.53) for an average runtime of 536 _._ 7 seconds per query. The system operated in a virtualized environment with Red Hat VirtIO drivers for storage and file system access, and networking provided through a **10 Gbit/s Ethernet interface** . 

## **D MQTT-Based Workflow** 

Motivated by CAFEIN<sup>®</sup> [25], FoA employs MQTTv5 as its communication backbone for orchestration. This protocol offers lightweight publish/subscribe semantics together with Quality of Service guarantees, making it well-suited for coordinating large sets of heterogeneous agents. Instead of relying on direct RPC or HTTP calls, interactions are expressed through a structured hierarchy of topics that naturally reflects the lifecycle of a task. The MQTT broker manages message passing and communication between nodes in the federated network, while also handling _authentication_ and _authorization_ to ensure secure and trusted interactions. MQTTv5 was chosen over alternative application protocols, such as HTTP, for its ability to efficiently support one-to-many asynchronous communication, while providing embedded security and strong scalability features. 

At the beginning of the process, new jobs are published to the orchestrator under a dedicated submission namespace. Agents simultaneously advertise their current capabilities by emitting versioned capability vectors on a separate update channel. These updates are disseminated using a ∆-gossip protocol and remain consistent across the federation due to MQTT’s delivery guarantees. The orchestrator consumes both streams - tasks and capabilities - and decomposes each job into subtasks, which are then routed to the appropriate agent-specific topics. 

Whenever a task requires collaboration among multiple agents, the orchestrator instantiates a cluster channel. Within this temporary communication space, agents exchange intermediate results, critiques, and refinements until a consensus signal is produced. Policy enforcement events are broadcast in parallel on a separate namespace, ensuring that compliance checks and auditability are embedded in the same communication fabric as task execution. Finally, results are published to the global result channel, where the orchestrator merges them according to the dependency structure of the job’s directed acyclic graph. 

This design ensures that every stage of the workflow - submission, capability dissemination, assignment, collaborative execution, enforcement, and result collection - is mediated by MQTT topics. The resulting system benefits from reliability and auditability, while maintaining the scalability and low overhead that are required in heterogeneous and bandwidth-constrained environments. 

18 

