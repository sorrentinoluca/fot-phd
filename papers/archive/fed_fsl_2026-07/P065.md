# **SYNAPSE:Federated Tool Routing via Typed Compendium Artifacts** 

**Abhijit Chakraborty**<sup>2</sup><sup>_∗†_</sup> 

MongoDB 

```
abhijit.chakraborty@mongodb.com
```

**Yash Shah**<sup>1</sup><sup>_∗_</sup> **Vivek Gupta**<sup>1</sup><sup>_†_</sup> Arizona State University Arizona State University `yshah124@asu.edu vgupt140@asu.edu` 

## **Abstract** 

The unit of collaboration in federated learning determines what guarantees are even expressible. Flat units like weights, prompts, raw examples, carry no type signature on which privacy, conflict resolution, or cross-model transfer can dispatch as welldefined operations. We propose _typed federated artifacts_ : schema-validated objects whose declared field structure makes per-field differential privacy, schema-aware merging, and cross-architectural transfer first-class operations rather than heuristic approximations. We instantiate this as SYNAPSE, a compendium for federated tool routing across clients with frozen, heterogeneous LLMs and no shared data or weights which is a setting flat units cannot handle without either leaking gradients or discarding structure. The compendium admits a typed merge operator with field-wise conflict resolution, a formal ( _ε,_ 0)-DP guarantee on numeric metadata, and conditional retrieval-distortion and routing-stability results empirically characterized on five distributions, including one where the contraction premise fails. A single compendium transfers across four LLM families (LLaMA-3.1-8B, LLaMA-3.2-3B, Mistral-7B, GPT-4o) with _≈_ 2-pt loss—a capability weight-sharing federation cannot provide without architectural matching. 

## **1 Introduction** 

Federated learning (FL) for LLM-based agents has largely inherited its unit of collaboration from classical settings, and that inheritance is beginning to show its limits in the heterogeneous, frozenLLM regimes this paper studies. The setting where this matters most is _federated tool-routing_ : collaborative tool selection across organizations running frozen, possibly heterogeneous LLMs under four joint constraints that no prior federated paradigm satisfies simultaneously. Clients cannot share weights or gradients (frozen LLMs); cannot pool raw data (no central corpus); may run different LLM families, so the unit cannot be architecture-specific (model-agnostic clients); and must protect tool-usage _patterns_ and not only raw data, since metadata alone re-identifies individuals [13, 27] and repeated routing exposes case-mix and behavioral patterns that regulated deployments treat as protected [33, 12]. 

Current federated methods exchange model parameters [18, 22, 28], adapters (FedLoRA), prompts [10], raw examples [43], split activations [42], or distilled ensembles [24]. Parameter and adapter sharing is communication-heavy ( _∼_ 50 MB/client/round for FedLoRA r16-fp16, lower bound), tightly couples architectures, and is privacy-leaky: gradient inversion [57, 19] and membership inference [37] reconstruct training data from shared updates. Raw-example sharing exposes local behavior and reaches only 0 _._ 61 on 4-tool routing versus 0 _._ 86 for Prompt-sharing flattens to a single string and cannot reliably aggregate negative constraints (e.g. “do not use tool _X_ when condition _Y_ ”) across clients, since text concatenation does not resolve which client’s exclusion 

> _∗_ Equal contribution. 

> _†_ Corresponding author. 

Preprint. 

rule wins for overlapping conditions, and prompt-extraction attacks [8, 16, 55] make these leaks operational rather than theoretical. Clinical [33, 12, 44] and financial [41, 30, 38] consortia have established federated precedents in exactly this regulated-domain setting, but those precedents inherit the same wrong-unit problem. The shared structural cause is that flat units carry no type signature _at the federation boundary_ on which schema-aware aggregation, validation, or per-field privacy can dispatch as well-defined operations. 

The right unit is not flat—it is a _typed federated artifact_ : an object _C_ defined by a schema _S_ that gives every field a declared role, type, and validation rule. Typed schemas and structured records are mature ideas in databases and distributed systems, and prior federated systems may use them internally; that is not the distinction. The distinction is whether the _exchanged unit_ carries a type signature on which the federation protocol can dispatch privacy, merging, and transfer as well-defined operations—and no existing federated unit does. Promoting a typed artifact to the role of exchanged unit makes three previously ill-defined operations well-posed: per-field differential privacy, because sensitivity bounds are schema-declared rather than estimated post-hoc; conflict resolution, because contradictory client contributions are resolvable by field-wise dispatch rather than majority vote over opaque strings; and cross-architectural transfer, because the artifact is interpreted at inference rather than baked into parameters. None of these is available when the federated unit is opaque text or vectors—not because those representations lack internal structure, but because they carry no type signature at the boundary on which the aggregation protocol can dispatch. 

We instantiate this abstraction as SYNAPSE, a compendium for federated tool routing, and make four contributions: the typed federated artifact abstraction (§3), instantiated as a compendium _C_ =( _M, U, P, T, A_ ) with schema _S_ that enables per-field dispatch of privacy, merging, and validation at the federation boundary; a typed merge operator (Def. 1, Algorithm 1) with field-wise conflict resolution, conflict logging, and schema validation across a client–edge–server hierarchy; artifactlevel guarantees (§4) comprising a formal ( _ε,_ 0)-DP guarantee on numeric metadata (Theorem 1) and two conditional results on retrieval distortion and routing stability empirically characterized on five distributions, including a LiveBench subset where the contraction premise fails ( _L_<sup>ˆ(99%)</sup> _R_ =1 _._ 018 _>_ 1; Tab. 13), disclosed as a limitation rather than suppressed; and a comprehensive empirical evaluation (§5) showing 0 _._ 92 _±_ 0 _._ 02 routing accuracy on GSM8k, statistically indistinguishable from centralized routing ( _p_ =0 _._ 31, 5 seeds) at 5 _._ 3 KB per client per round ( _∼_ 10 _,_ 000 _×_ below the FedLoRA r16-fp16 architectural lower bound), _≈_ 2-pt cross-model loss across four LLM families, 0 _._ 71 at 8-step tool chains versus 0 _._ 34 for prompt-sharing, and generalization to NQ-Open retrieval-policy artifacts (App. K.2), confirming the abstraction extends beyond tool routing. 

## **2 Related Work** 

**Federated learning for LLMs.** OpenFedLLM [50] and FederatedScope-LLM [22] address communication and heterogeneity in LLM training. FedbiOT [46] and FFA-LoRA [40] target privacy under DP. These all aggregate model parameters or adapters, requiring architectural compatibility and incurring substantial communication. 

**Federated retrieval-augmented generation.** GPT-FedRec [53], FedE4RAG [26], FRAG [56], and C-FedRAG [2] federate retrieval indices via raw examples or encrypted shares. They lack tool-aware structure: routing operates over unstructured retrieved chunks rather than typed routing [9]. We compare directly to C-FedRAG in §5. 

**Text-centric federation.** FedTextGrad [10] federates optimized prompts; Fed-ICL [43] federates exemplars. Both treat the federated unit as flat text without typed structure. 

**Tool-augmented LLMs.** Toolformer [35], ReAct [48], Gorilla [31], ToolLLM [32], and Graph RAG-Tool Fusion [25] use schemas and retrieval to select tools, but in centralized settings without federation. 

**Privacy.** DP foundations [1, 17] and prompt-extraction attacks [8, 16, 54, 55] formalize the leakage we defend against on the numeric and text paths respectively. 

**Federated routing and large-scale tool benchmarks.** Concurrent work [4] federates _model-selection_ routers (which LLM to call); their unit is router parameters, ours is a typed artifact, and the routing problem is tool-selection rather than model-selection. The two settings are complementary. LiveMCPBench [29] (527 tools, 70 MCP servers) and InfoMosaic-Bench [15] (621 tasks, 77 MCP tools) characterize the scale at which production tool-routing must operate; extending typed-compendium federation to LiveMCPBench-class catalogs is direct future work (App. J.1). 

2 

**SYNAPSE** differs from prior work along an orthogonal axis: _the type signature of the exchanged object_ : Weights, adapters, prompts, and raw examples are all untyped from the federation’s perspective. The compendium is typed at every field, which is what enables artifact-level ( _ε,_ 0)-DP, schemaconstrained merge, and cross-model transfer to be well-defined operations rather than approximations (Tab. 1). 

Table 1: Comparison across six dimensions. SYNAPSE is the only method satisfying all five non-trivial constraints jointly. Federate-the-Router [4] federates model-selection rather than tool-selection – complementary, not competing. 

|Method|Unit type|Frozen LLM|Local-only data|Native tool routing|Model-agnostic|Formal DP|
|---|---|---|---|---|---|---|
|FedAvg / FedLoRA|Weights / adapters|No|Local|No|No|Rare|
|Fed-ICL|Raw examples|Yes|Local|No|Partial|No|
|FedTextGrad|Prompts (fat)|Yes|Local|No|Partial|No|
|GraphRAG|Knowledge graph|Yes|Central|No|N/A|No|
|C-FedRAG|Encrypted index|Yes|Local|No|Partial|No|
|Federate-the-Router|Router weights/embeddings|Yes|Local|Model-routing|N/A|No|
|**SYNAPSE (ours)**|**Typed compendium**|**Yes**|**Local**|**Tool-routing**|**Yes**|**Numeric felds**|



## **3 The Compendium and the Typed Merge Operator** 

This section gives a precise definition of the compendium artifact and the typed merge operator that aggregates compendiums across a client–edge–server hierarchy (Fig. 1). We open with the formal definition because the rest of the framework – privacy mechanisms, conflict resolution, cross-model transfer, the formal guarantees in §4 are all dispatch on the schema introduced here. 


![](P065_images/P065.pdf-0003-05.png)



![](P065_images/P065.pdf-0003-06.png)

### Figure analysis

The figure’s purpose is to illustrate the client–edge–server hierarchy used by SYNAPSE to aggregate typed compendium artifacts across trust boundaries.

**Main components directly visible:**
- A legend identifies three arrow types:
  - Solid black arrow: **Local Compendium**
  - Red dashed arrow: **Cluster Compendium**
  - Blue dashed arrow: **Global Compendium**
- Two clusters are shown:
  - **Cluster A** contains **Local Agent 1**, **Local Agent 2**, and **Edge Aggregator A**.
  - **Cluster B** contains **Local Agent 3**, **Local Agent 4**, and **Edge Aggregator B**.
- A **Central Aggregator** is positioned outside the local-agent groups, receiving cluster-level information and redistributing global information.
- Each local-agent box contains small schematic icons, visually suggesting an agent plus structured/graph/database-like compendium contents, although the icons themselves are not labeled.

**Information flow directly observed:**
- Solid black arrows connect local agents to their corresponding edge aggregator, indicating movement of local compendiums within each cluster.
- Red dashed arrows connect edge aggregators toward the central aggregator, indicating cluster compendiums being sent upward.
- Blue dashed arrows run from the central/global path back toward local-agent areas, indicating redistribution of a global compendium.

**Interpretation in context:**
- The diagram supports the surrounding Section 3 text, which introduces the compendium and typed merge operator.
- It visually explains the hierarchy described in the caption: local agents maintain local compendiums; edge aggregators merge cluster compendiums, presumably via Algorithm 1; and the central aggregator redistributes the global compendium each round.
- The key architectural point is that aggregation occurs in stages: local → edge → central, followed by central → local redistribution.
- The caption’s statement that only typed compendium artifacts cross trust boundaries is consistent with the diagram’s use of compendium-specific arrows rather than raw data or model-weight transfer.

**Nearby material:**
- The page also contains Table 1 comparing SYNAPSE with prior methods, but that table is separate from this figure and is not part of the diagram itself.


Figure 1: The client–edge–server hierarchy. Local agents within a cluster maintain a local compendium; edge aggregators merge cluster compendiums via Algorithm 1; the central aggregator redistributes a global compendium each round. Only typed compendium artifacts cross trust boundaries. 

**Definition 1** (Compendium) **.** _A_ compendium _is a tuple_ 

_C_ = ( _M, U, P, T, A_ ) 

_together with a schema S that types each component:_ 

- _M_ = _{_ (id _t,_ desc _t,_ spec _t, mt_ ) _}t∈T is the_ tool metadata _: identifier, description, specification, and a vector of numeric attributes mt ∈_ R<sup>_k_</sup> _(e.g., latency, success rate, calls/day). Numeric fields have schema-declared sensitivity bounds_ ∆ _m._ 

- _U_ = _{_ (tool _i,_ scenario _i_ ) _}_<sup>_|_</sup> _i_<sup>_U_</sup> =1<sup>_|is the set of_usage scenarios</sup><sup>_:natural-language descriptions of when_</sup> _each tool applies, each tagged with its parent tool._ 

- _P_ = _{_ (tool _j,_ precaution _j_ ) _}_<sup>_|_</sup> _j_<sup>_P_</sup> =1<sup>_|is the set of_precautions</sup><sup>_:negative examples and exclusion rules_</sup> _describing when_ not _to invoke each tool._ 

- _T_ = _{_ (tool _k,_ sig _k,_ template _k_ ) _} is the set of_ prompt templates _: parameterized prompts indexed by tool and signature._ 

3 

- _A is a_ structured annex _: it consists of typed triples of entities and relations that facilitate retrieval and routing._ 

_A compendium C is_ valid under _S iff (a) every_ id _t ∈T (tool registry), (b) every numeric field in mt lies in its declared range, (c) every scenario, precaution, and template references a registered tool, and (d) all string fields satisfy declared length and encoding constraints._ 

Numeric sensitivity bounds in _M_ enable ( _ε,_ 0)-DP (Theorem 1); typed separation of _U_ and _P_ enables conflict-log handling (Algorithm 1); _T_ indexed by (tool _,_ signature) enables model-agnostic transfer; schema validation enables static rejection of malformed adversarial contributions. Each round, clients update locally; edges merge _{Ck_<sup>(</sup><sup>_r_)</sup><sup>_}k∈E →C_</sup> _E_<sup>(</sup><sup>_r_);the servermerges</sup><sup>_{C_</sup> _E_<sup>(</sup><sup>_r_)</sup><sup>_} →C_</sup> _g_<sup>(</sup><sup>_r_),redistributed.</sup> Merges are typed dispatches: 

**Algorithm 1** EdgeMerge: typed merge with field-wise conflict resolution (compact form; full numeric-path and conflict-log specification in App. F) 

**Require:** Client compendiums _{Ck}k_<sup>_K_</sup> =1<sup>; cosine threshold</sup><sup>_τ_; tool registry</sup><sup>_T_</sup> **Ensure:** Edge compendium _CE_ 1: _CE ←∅_ ; reject any _Ck_ failing schema validation under _S_ 2: _M_ **(metadata):** canonical lookup from _T_ ; numeric subfields clipped + Laplace-noised (App. F, Theorem 1) 3: **for** each tool _t_ **do** _▷_ usage scenarios _U_ 4: Embed _{u ∈ Ck.U_ : _u._ tool = _t}k_ via Jina; cluster greedily by cos _≥ τ_ 5: **for** each cluster _C_ **do** 6: **if** IsConsistent( _C_ ) (App. F) **then** _CE.U_ += _{_ TextGradSummarize _S_ ( _C_ ) _}_ 7: **else** keep centroid; append dissenters to conflict log _L_<sup>(</sup><sup>_r_)</sup> 8: _P_ **(precautions):** TextGradSummarize _S_ (Dedup _τ_ (<sup>�</sup> _k_<sup>_Ck.P_))</sup><sup>_∪_ConflictsToPrecautions(</sup><sup>_L_(</sup><sup>_r−_1))</sup> 9: _T_ **(templates):** per-( _t,_ sig) key, TextGradSummarize _S_ ( _{p_ : _p._ key = ( _t,_ sig) _}_ ) 10: _A_ **(annex):** Dedup _τ_ (<sup>�</sup> _k_<sup>_Ck.A_)</sup> 11: **return** _CE_ 

**Conflict resolution.** Conflicting scenarios for a single tool create a cosine cluster (cos _≥ τ_ =0 _._ 85); IsConsistent verifies schema-level structured-field agreement along with a consistency probe from an LLM (App. F). In clusters where inconsistencies are found, the centroid is kept, while dissenting elements are logged in the conflict record _L_<sup>(</sup><sup>_r_)</sup> , which informs the next-round Precautions through ConflictsToPrecautions (e.g., “Use Wolfram for symbolic integration” + “Avoid when depth _>_ 4” _→_ “Use for symbolic integration; do not use when depth _>_ 4”). (§5: accuracy holds at 0 _._ 86 even when 40% of client scenarios contradict each other, versus 0 _._ 74 without conflict logging). The server applies the same merge operator one level up, treating edge compendiums as its inputs. **Privacy mechanisms.** Two mechanisms with different guarantees: _numeric fields_ in _M_ receive formal ( _ε,_ 0)-DP protection via Laplace noise calibrated to each field’s declared sensitivity (Theorem 1); _text fields_ are protected by adaptive masking that suppresses high-salience tokens, an empirical defence with no formal DP guarantee (Tab. 8). Secure aggregation [7] can be layered on top of either mechanism independently. 

**Inference-time routing.** Given a query _q_ , the system first retrieves the five most similar scenarios from the global compendium _Cg_ using cosine similarity over Jina embeddings [21]. A lightweight LLM reranker ( `llama-3.1-8b-instruct` [20]) then selects the single best match and identifies its parent tool, which the planner invokes. Retrieval-augmented generation within a tool operates independently of this routing step and does not affect which tool is selected. 

### **3.1 TextGrad and the Federated Training Loop** 

TextGrad [52] treats natural-language prompts as differentiable variables, optimizing them via LLM-produced critiques ( _textual gradients_ ) describing how a prompt should change to improve a downstream loss. Within SYNAPSE, TextGrad operates on three compendium fields ( _U_ , _P_ , _T_ ) at the _edge_ layer only and never at clients (which would expose private data to the optimizer’s LLM) and never at the server (which would centralize cost). Tool metadata _M_ is canonical and bypasses TextGrad entirely. 

**Per-round update.** At each round, the edge takes each cluster of similar scenarios produced by Algorithm 1 and drafts a single summary. It then tests that summary against a small held-out set of public benchmark queries, never client data, and measures how often routing fails. An LLM critique 

4 

describes what the summary should change to reduce those failures, and the summary is revised over _S_ =3 steps. Before any text leaves a client, high-salience tokens are masked under a tunable masking strength _λ_ : higher _λ_ suppresses more tokens for stronger empirical privacy at some cost to routing accuracy, while lower _λ_ preserves more content (Tab. 9); the edge LLM therefore never sees raw client scenarios. This refinement runs separately for usage scenarios _U_ , precautions _P_ , and prompt templates _T_ . Scenarios that caused conflicts in the current round are not discarded: they are carried forward as structured precautions in the next round’s compendium _CE_<sup>(</sup><sup>_r_+1)</sup> _.P_ , giving the system a form of memory across rounds without any retraining. 

**Per-field loss for** _U_ **,** _P_ **,** _T_ **.** The TextGrad loss differs by field and by what each field controls. For usage scenarios _U_ and precautions _P_ , both of which influence the routing decision, _ℓ_ is the routing-failure rate on the held-out probe set. For prompt templates _T_ , which control post-routing API formatting after the tool is already selected, routing-failure is not the appropriate loss; we use task-success-given-correct-routing (the fraction of probe queries that produce a valid downstream API response when routed to the correct tool with template _u_<sup>(</sup> _t_<sup>_s_)).Using routing-failure for</sup><sup>_T_would</sup> not provide a useful gradient signal because _T_ does not influence which tool is selected. 

Hence _TextGrad is not a global optimization_ over the full compendium, not a meta-learner, not a substitute for the typed merge operator: merge enforces schema validity and field-wise dispatch, TextGrad refines natural-language content within each typed field. Removing TextGrad and using extractive summarization drops routing accuracy 0 _._ 92 _→_ 0 _._ 85 (Tab. 3); removing merge while keeping TextGrad collapses to 0 _._ 74 at 40% contradictory clients (Tab. 2). Edge cost: _∼_ 60 s/round/aggregator on server, amortized across the edge’s clients. 

## **4 Analytical Properties** 

We give three analytical statements: a formal DP guarantee on numeric metadata, and two conditional results (retrieval-distortion under Lipschitz assumption, routing stability under contraction) characterized empirically rather than proved (Tab. 25). These are positioning rather than central contributions. 

**Theorem 1** (( _ε,_ 0)-DP on numeric metadata) **.** _Let M_ num _denote the numeric-metadata mechanism that adds independent Laplace noise to each numeric field of C.M . For neighboring datasets D, D_<sup>_′_</sup> _differing in a single user’s numeric metadata contribution of ℓ_ 1 _-sensitivity_ ∆ _m,_ 

Pr[ _M_ num( _D_ ) _∈ S_ ] _≤ e_<sup>_ε_</sup> Pr[ _M_ num( _D_<sup>_′_</sup> ) _∈ S_ ] 

_for any measurable S. Across R rounds, basic sequential composition gives pure_ ( _ε_<sup>_′_</sup> _,_ 0) _-DP with ε_<sup>_′_</sup> = _Rε; advanced composition [17] gives_ ( _ε_<sup>_′_</sup> _, δ_<sup>_′_</sup> ) _-DP with ε_<sup>_′_</sup> = �2 _R_ ln(1 _/δ_<sup>_′_</sup> ) _ε_ + _R ε_ ( _e_<sup>_ε_</sup> _−_ 1) _. We report the tighter of the two; for the small-R regime evaluated in this paper (R ≤_ 30 _, ε ≤_ 2 _), basic composition is strictly tighter and gives pure-DP guarantees._ 

**Scope.** Theorem 1 covers the numeric path. The text-field mechanism is heuristic; we do not claim it satisfies formal DP. 

**Adjacency and trust model.** “Single user’s numeric metadata contribution” means user-level adjacency: _D, D_<sup>_′_</sup> differ in the entire numeric record contributed by one user. The guarantee is enforced in two stages: (i) per-user clipping at the client bounds the user’s _ℓ_ 1 contribution at ∆ _m_ per field before any client-level aggregation (App. F, stage 1); (ii) clients transmit clipped values to the edge aggregator, which computes the per-field average over _K_ clients and adds Laplace noise calibrated to the average’s sensitivity ∆ _m/K_ , releasing _CE.M.m_<sup>(</sup><sup>_j_)</sup> _← K_ <u>1</u> � _k_<sup>clip(</sup><sup>_·_)+</sup> Lap(∆ _m_<sup>(</sup><sup>_j_)</sup><sup>_/_(</sup><sup>_Kε_(</sup><sup>_j_))).The edge is semi-honest – it follows Algorithm 1 faithfully but may attempt</sup> inference from clipped client values; secure aggregation [6] can be layered on the numeric path to weaken this assumption to ideal-functionality only. Downstream typed-merge operations on the noised release (clustering, redistribution) are post-processing (App. L, Lemma L.2), so the user-level guarantee carries through unchanged across rounds. 

**Theorem 2** (Bounded retrieval distortion, conditional) **.** _Let u_ ˜ = PrivTrans( _u_ ) _denote the privacytransformed scenario after numeric noising and text masking (λ)._ Assume _the embedding e_ ( _·_ ) _is Le-Lipschitz under text distance d_ text _, and cosine similarity is L_ sim _-Lipschitz in ∥· ∥_ 2 _. Then_ E _∥e_ ( _u_ ) _− e_ (˜ _u_ ) _∥_ 2 _≤ Le ·_ E[ _d_ text( _u,_ ˜ _u_ )] =: _δ_ priv _and_ E _|_ ∆sim _| ≤ L_ sim _δ_ priv _. Markov’s inequality converts to a high-probability bound:_ Pr( _|_ ∆sim _| > t_ ) _≤ L_ sim _δ_ priv _/t. The notation δ_ priv _(rather_ 

5 

_than δ_ ( _ε_ ) _) emphasizes that the bound depends on the combined privacy transformation – principally the masking strength λ on text fields, since ε-DP applies only to numeric metadata. Conditional on the two Lipschitz assumptions; we characterize them empirically below._ 

**Empirical characterization (not a theorem).** The Lipschitz assumption above is a statement about the embedding model rather than about SYNAPSE, and we make no formal claim that the Jina embedding satisfies it globally. We measure the per-sample ratio _∥e_ ( _u_ ) _− e_ (˜ _u_ ) _∥_ 2 _/d_ text( _u,_ ˜ _u_ ) on 1 _,_ 000 scenario pairs at three masking strengths _λ ∈{_ 0 _._ 5 _,_ 1 _._ 0 _,_ 1 _._ 5 _}_ . We define _d_ text( _u, u_<sup>_′_</sup> ) as tokenlevel Levenshtein distance after lowercasing and whitespace normalization, divided by max( _|u|, |u_<sup>_′_</sup> _|_ ) tokens to give a bounded [0 _,_ 1] ratio (full protocol App. L). The 99%-quantile is _L_<sup>ˆ(99%)</sup> _e ≈_ 1 _._ 4 with variation under 5% across _λ_ values; the resulting _δ_<sup>ˆ</sup> priv at _λ_ =1 _._ 0 is _≈_ 0 _._ 37, small relative to typical inter-scenario distances ( _∼_ 1 _._ 0–1 _._ 4). This is an empirical observation about the deployed embedding model, not a proof that Theorem 2’s assumption holds. A user using a different embedding model should re-measure _L_<sup>ˆ</sup> _e_ before relying on the conditional bound. 

**Theorem 3** (Routing stability under contraction, conditional) **.** _Let sr_ ( _t_ ) = _R_ ( _e_ ( _q_ ) _, ζg_<sup>(</sup><sup>_r_)(</sup><sup>_t_))</sup><sup>_be the_</sup> _reranker score for tool t at round r, evolving as sr_ +1 = _R_ ( _sr_ )+ _ηr_ +1 _where R encodes the round-toround score update via the merge-and-redistribute protocol and ηr is zero-mean privacy perturbation with bounded variance σ_<sup>2</sup> _per coordinate._ Assume _(i) R is an L-contraction in ℓ_ 2 _with L<_ 1 _, (ii) at the noise-free limit a unique top-scoring tool t_<sup>_∗_</sup> _has margin_ ∆ _>_ 0 _, and (iii) the propagated stationary score perturbations are sub-exponential. Then sr converges in distribution to a stationary distribution_ concentrated around _the noise-free fixed point s_<sup>_∗_</sup> _(with stationary variance bounded by σ_<sup>2</sup> _/_ (1 _− L_<sup>2</sup> ) _per coordinate; for nonlinear R, the stationary mean need not equal s_<sup>_∗_</sup> _exactly), and the top-1 selection_ arg max _t sr_ ( _t_ ) _equals t_<sup>_∗_</sup> _with probability at least_ 1 _−_ 2( _K−_ 1) exp( _−_ ∆<sup>2</sup> (1 _−L_<sup>2</sup> ) _/_ (2 _σ_<sup>2</sup> )) _, where K is the number of candidate tools. The contraction premise is not proved for our reranker; Tab. 13 (App. F) measures L_<sup>ˆ(99%)</sup> _R and_ ∆<sup>ˆ(5%)</sup> _across five distributions, with one (LiveBench) where L_ ˆ<sup>(99%)</sup> _R >_ 1 _and the premise fails._ 

## **5 Experiments and Analysis** 

We evaluate SYNAPSE in two regimes: a _controlled_ regime designed to verify mechanism via proxy benchmarks, ablations, and theory-grounded measurements, and a _realistic_ regime designed to test routing behavior on real APIs and long-horizon tool chains. 

**Setup.** Proxy: GSM8k [11] and BBH [39]-derived tasks; tool labels correspond to routed solution paths. Real: 4 tool families (MathQA, SearchQA, CodeExec, LogicQA) and 6 ToolBench APIs (SerpAPI, OpenWeatherMap, Wikipedia, Wolfram, REST Countries, GCal). IID partitions sample uniformly; non-IID partitions shard by numeric answer range or question characteristics. Training: batch 3, 3 local steps/round, _K_ =5 retrieval. Full hyperparameters in App. M. 

**Baselines.** Two families: (i) federated text-sharing – Fed-ICL [43] (examples) and FederatedTextGrad [10] (prompts) – both frozen-LLM and weight-free; (ii) routing/retrieval ablations – BM25 [34], Centralized-Retrieval-Only, Static-Global, Local-Only, Unstructured-Pool, DescriptionOnly. Centralized-SYNAPSE, the same typed compendium built without federation, serves as the centralized typed-registry analog (cf. MCP-style registries [3]) and isolates the federation cost from the typed-schema contribution. Adapter-based and federated RAG – FedLoRA, C-FedRAG [2] – are extended baselines; FedAvg full-fp32 is reported only as a communication-cost reference. 

### **5.1 Controlled-regime results** 

**Statistical significance.** SYNAPSE matches centralized performance within statistical noise while every baseline falls significantly short. Across 5 random seeds _{_ 42 _,_ 123 _,_ 456 _,_ 789 _,_ 1024 _}_ , SYNAPSE achieves 0 _._ 92 _±_ 0 _._ 02 on GSM8k (5 IID clients), statistically indistinguishable from CentralizedSYNAPSE ( _p_ = 0 _._ 31, _d_ = 0 _._ 2), while all non-centralized baselines differ at _p <_ 0 _._ 05 (full table App. M): FedTextGrad 0 _._ 90, BM25 0 _._ 83, Fed-ICL 0 _._ 79, ReAct 0 _._ 64, Local-Only 0 _._ 46. **Component and TextGrad ablations.** Every typed schema field contributes measurable, monotonic accuracy gains, and the conflict log is critical under adversarial conditions. Stacking BM25 _→_ full SYNAPSE (Tab. 2, left): +0 _._ 16 semantic retrieval, +0 _._ 06 schema, +0 _._ 10 scenarios, reaching 0 _._ 92 (0 _._ 08 from oracle);retrieval and reranking contribute equally (+0 _._ 16 each). Injecting contradictory 

6 

scenarios (Tab. 2, right): the conflict log opens a 12-pt protection gap at 40% rate, confirming that field-wise conflict resolution is not cosmetic. Replacing TextGrad ( _S_ =3) at the edge with extractive centroid drops accuracy 0 _._ 92 _→_ 0 _._ 85;with no summarization, 0 _._ 92 _→_ 0 _._ 78 (Tab. 3); full sweep over _S ∈{_ 1 _,_ 3 _,_ 5 _}_ in App. G. 

Table 2: Component ablation (left, _K_ = 5 IID, 5 seeds; ∆ is gain over prior row) and conflict handling (right, _K_ = 5, contradictory-scenario injection). Each schema field contributes monotonically; the conflict log opens a 6-pt protection gap at 20%. 

Table 3: TextGrad ablation. Critique-and-update loop produces compact, low-noise field entries; without it, 7–14 pt drop. Full sweep App. G. 

|Comp|onent stac|k|Conf|ict han|dling|Edge summarization|Acc.|Cost|
|---|---|---|---|---|---|---|---|---|
|Variant|Acc.|∆|Conf.|With|W/o|**TextGrad (**_S_=3**, used)**|**0**_._**92**|_∼_60s|
|BM25<br>+Embed|0_._60<br>0_._76|—<br>+0_._16|0%<br>20%|0_._92<br>0_._89|0_._92<br>0_._82|Extractive centroid<br>No summarization|0_._85<br>0_._78|_<_1s<br>0s|
|+Schema|0_._82|+0_._06|40%|0_._86|0_._74||||
|+Scen.|**0**_._**92**|+0_._10|60%|0_._81|0_._63||||
|Oracle|1_._00|+0_._08|||||||



**Heterogeneity and scalability.** SYNAPSE degrades gracefully under distribution shift and scales to 500 clients with bounded compendium size and sub-500 ms latency (Tab. 19, App. M). Under non-IID splits, GSM8k drops only 0 _._ 96 _→_ 0 _._ 92 and BBH benchmarks drop _≤_ 2 pts; deduplication saturates at 70% and _p_ 95 stays under 500 ms regardless of client count because reranking always processes only the top-5 candidates. 

**Cross-model transfer.** A single compendium built with LLaMA-3.1-8B routes correctly across four LLM families on GSM8k – LLaMA-3.1-8B (0 _._ 92, native), LLaMA-3.2-3B (0 _._ 90), Mistral-7B (0 _._ 91), GPT-4o (0 _._ 92) – and a mixed federation (2 _×_ LLaMA + 2 _×_ Mistral + 1 _×_ GPT-4o) reaches 0 _._ 92 overall. The same property replicates on _τ_ -bench retail with the round-3 compendium and embedding model held fixed (Tab. 4): same-family transfer to LLaMA-3.2-3B yields ∆= _−_ 0 _._ 022 (matching the GSM8k same-family gap exactly), cross-family Mistral-7B yields ∆= _−_ 0 _._ 009, and stronger-model GPT-4o yields ∆=+0 _._ 085 – the typed compendium rides a stronger model upward, reaching _∼_ 90% of _τ_ -bench’s published GPT-4o ceiling. All four LLMs preserve the per-category ordering (catalog _>_ account _>_ escalation _>_ orders _>_ returns), confirming that compendium quality rather than LLM-specific category preference drives the result.Weight-sharing federation cannot offer this: merged adapters or parameters need architectural compatibility and re-baking for each target LLM. 

Table 4: _τ_ -bench cross-model probe (250 tasks _×_ 3 seeds, same compendium, same embedding). Same-family ∆= _−_ 0 _._ 022 matches the GSM8k cross-model gap exactly; per-category ordering preserved across all four LLMs (App. K.1). 

|Inference LLM|Task success|Tool-call acc.|Avg. turns|∆vs. LLaMA-3.1-8B|
|---|---|---|---|---|
|LLaMA-3.1-8B (main)|0_._453_±_0_._023|0_._631_±_0_._017|5_._4|—|
|LLaMA-3.2-3B|0_._431_±_0_._021|0_._614_±_0_._016|5_._7|_−_0_._022|
|Mistral-7B-Instruct|0_._444_±_0_._020|0_._624_±_0_._018|5_._5|_−_0_._009|
|GPT-4o|**0**_._**538**_±_**0**_._**018**|**0**_._**703**_±_**0**_._**014**|4_._8|+0_._085|



**Benchmark breadth and prompt transfer.** The federation cost is task-dependent: modest on structured mathematical reasoning, larger on open-ended language tasks where scenario diversity is hardest to compress. On four LiveBench [45] reasoning tasks, federated underperforms centralized by 7–13 pts on three open-domain reasoning tasks but _outperforms_ by 4 pts on AMPS Hard (App. K); both configurations use GPT-4o, so the gap reflects compendium compression rather than model mismatch. Prompt transfer (LLaMA-3.2-11B _→_ 3.2-3B) yields task-dependent +0 _._ 15/+0 _._ 03/ _−_ 0 _._ 08 across BBH-Arithmetic/OC/GSM8k, confirming it is a distinct and non-interchangeable mechanism from compendium transfer (App. K, Tab. 21). 

7 

**Latency and ablation summary.** Routing latency stays within production-viable bounds and the LLM reranker is the single highest-value component. End-to-end _p_ 50 _/p_ 95 =330 _/_ 470 ms; replacing the Llama-3.1-8B edge summarizer with Llama-3.2-3B incurs only 0 _._ 01 accuracy cost (0 _._ 91 _±_ 0 _._ 02). A logged 500-query GSM8k run isolates four mechanisms: the reranker is the largest single contributor (bypass drops 0 _._ 917 _→_ 0 _._ 497, ∆= 0 _._ 42 _±_ 0 _._ 05, 3 seeds; App. H); federation provides _coverage_ (Local-Only 0 _._ 46, _∼_ 54% of queries require scenarios unseen locally); schema validation stabilises at 6 types with 95 _._ 2% deduplication; Fed-ICL’s string-proximity matching explains its 0 _._ 61 vs. 0 _._ 86 collapse on multi-tool. 

### **5.2 Realistic-regime results** 

**Multi-tool and real APIs.** On real APIs, SYNAPSE substantially outperforms text-sharing baselines and remains within sampling noise of the centralized ceiling across all six API categories. On the 4- tool proxy, SYNAPSE reaches 0 _._ 86 vs. Fed-ICL 0 _._ 61 (+0 _._ 25) and Centralized 0 _._ 91 (gap 0 _._ 05). On the ToolBench 250-query test set (App. I, Tab. 5): 0 _._ 728 vs. 0 _._ 800 vs. 0 _._ 480; 95% bootstrap CIs (Tab. 16) show SYNAPSE–Centralized intervals overlap per category while SYNAPSE–Fed-ICL intervals are disjoint at _n_ =250 overall. The 0 _._ 148 gap between routing accuracy (0 _._ 728) and end-to-end success (0 _._ 580) is entirely upstream-API failure (schema drift 5 _._ 2%, semantic miss 4 _._ 8%, auth/quota 2 _._ 4%, timeouts 1 _._ 6%, rate limits 0 _._ 8%); routing errors account for 27 _._ 2%. 

Table 5: Real-API routing on 6 ToolBench categories ( _n_ = 50 _/_ 45 _/_ 40 _/_ 40 _/_ 40 _/_ 35, total 250). Single-pass; integer success counts _/ n_ , consistent with Tab. 17’s routing-error counts. Bootstrap CIs in Tab. 16. 

Table 6: Long-horizon multi-step routing. SYNAPSE is the only federated method with 8- step success over 0 _._ 7. Planner-based agents (ReWOO, Reflexion) compare routing-as-memory (ours) with routing-as-planning (theirs); see App. D for details. 

|API category|SYNAPSE|Centralized|Fed-ICL|Method|step|2-step|4-step|8-step|12-step|
|---|---|---|---|---|---|---|---|---|---|
|Search|0.76|0.84|0.50|**SYNAPSE**|0_._88|0_._82|0_._77|**0**_._**71**|0_._65|
|||||Cntrlid|091|086|081|074|068|
|Weather|0.80|0.84|0.53|eaze|_._|_._|_._|_._|_._|
|||||RWOO|089|081|072|059|046|
|Knowledge|070|078|045|e|_._|_._|_._|_._|_._|
||.|.|.|Rfi|093|088|081|072|064|
|Math|0.80|0.85|0.55|eexon<br>(_K_=3)|_._|_._|_._|_._|_._|
|Data|0.65|0.75|0.42|RAt|079|069|058|046|037|
|Calendar|0.63|0.71|0.40|ec|_._|_._|_._|_._|_._|
|**Overall**|**0.728**|**0.800**|**0.480**|Fed-ICL|0_._69|0_._55|0_._43|0_._34|0_._26|
|||||FedTextGrad|0_._74|0_._61|0_._50|0_._41|0_._32|
|||||Local-Only|0_._51|0_._30|0_._18|0_._09|0_._04|



**Long-horizon multi-step routing.** The typed Precautions field is the decisive advantage over multistep horizons: Fed-ICL collapses to 0 _._ 34 at 8 steps vs. SYNAPSE’s 0 _._ 71—a 37-pt gap that grows with chain length because flat-text baselines lack structured exclusion rules (Tab. 6). SYNAPSE matches Reflexion- _K_ =3 statistically at 1 _/_ 3 the inference compute, confirming routing memory and routing planning are complementary mechanisms. 

**Extended baselines.** SYNAPSE outperforms all extended baselines without architectural compatibility or weight sharing. On 5-seed GSM8k: SYNAPSE 0 _._ 92, FedLoRA 0 _._ 89, C-FedRAG 0 _._ 84, Fed-ICL 0 _._ 79—at 5 _._ 3 KB vs. _∼_ 52 MB/client/round for FedLoRA ( _∼_ 10 _,_ 000 _×_ gap against the architectural lower bound; App. J).SYNAPSE tolerates up to 40% adversarial clients (Fig 2) across three attack modes (cross-source, random corruption, tool-confusion) before sharp degradation at 60%; the boundary aligns with Theorem 3’s empirically measured contraction regime 

**Long-horizon simulation (illustrative stress-test).** At deployment scale, the typed-artifact protocol sustains effective routing over 30 rounds, recovers from API schema drift, and generates measurable cross-org transfer gains. Across 100 clients, 5 orgs, 32 APIs, and _∼_ 21k queries (App. O): routing reaches 0 _._ 79 at _R_ =30; end-to-end success 0 _._ 67; the 96 KB compendium recovers to within 0 _._ 02 of pre-drift baseline by _T_ +10 after each of 8 scheduled drift events; and cross-org federation yields ∆= +0 _._ 10 over within-org federation under category-coherent partitioning and ∆= +0 _._ 07 under random partitioning.At ( _ε_ =0 _._ 5 _, λ_ =1 _._ 5), adversary AUROC drops to chance (0 _._ 50) at a cost of 5 routing accuracy pts with _ε_<sup>_′_</sup> = 1 _._ 5 over three rounds; the full privacy–utility sweep is in App. C, Tab. 9. 

8 


![](P065_images/P065.pdf-0009-00.png)

### Figure analysis

Purpose: The plot evaluates SYNAPSE robustness under increasing adversarial-client fraction for three attack modes, showing where routing accuracy degrades.

Plot structure and labels:
- Single-panel line plot with no visible title.
- x-axis: `adv. frac. (%)`, with ticks at 0, 20, 40, and 60.
- y-axis: `routing acc.`, scaled from 0.0 to 1.0.
- Legend/series:
  - Blue circles: `Cross-source`
  - Teal squares: `Random`
  - Orange triangles: `Tool-conf.`
- A red dashed vertical line at 40% is labeled `40% boundary`.
- No error bars are shown.

Direct visual observations:
- All three attack modes begin near the same high routing accuracy at 0% adversarial clients, around 0.9.
- Accuracy declines modestly at 20% adversarial clients.
- At 40%, all three series remain above approximately 0.62, with Cross-source highest, Random intermediate, and Tool-conf. lowest.
- At 60%, all three series show a sharp collapse, with Cross-source still highest and Tool-conf. lowest.
- The ordering is consistent across nonzero adversarial fractions: Cross-source > Random > Tool-conf.

Readable quantitative information:

| Visual element | Readable value |
|---|---:|
| Adversarial-fraction boundary | 40% |
| y-axis range | 0.0 to 1.0 routing accuracy |
| x-axis tick labels | 0, 20, 40, 60% |

Interpretation relative to the paper text:
- The figure visually supports the surrounding claim that SYNAPSE tolerates up to 40% adversarial clients before a sharp degradation at 60%.
- The plotted 40% boundary corresponds to the text’s stated robustness threshold and its claimed alignment with Theorem 3’s contraction regime.
- The plot only shows attack-mode degradation curves; the Krum/TrimmedMean recovery results mentioned in the caption and appendix are not shown in this panel.


Figure 2: SYNAPSE tolerates up to 40% adversarial clients (routing accuracy _≥_ 0.62) before sharp collapse at 60%, aligning with Theorem 3’s contraction regime _L_<sup>ˆ(99%)</sup> _R_ =0 _._ 891); Krum / TrimmedMean recover +8–25 pts at 33–50% adversarial at ~1-pt clean cost (App E, Tab. 13). 

### **5.3 Beyond tool routing: typed retrieval-policy artifacts on NQ-Open** 

The typed-artifact abstraction generalizes beyond tool routing with no algorithmic changes: the same merge operator, schema validation, and DP guarantees transfer directly to retrieval-policy federation on NQ-Open, closing 73% of the local-to-centralized accuracy gap. We instantiate the protocol on Natural Questions Open [23] with hybrid retrieval (BM25 + dense, top- _k_ = 5 Wikipedia passages) and `llama-3.1-8b` answer generation. 5 _,_ 000 NQ-Open dev questions are partitioned across 5 non-IID clients by question type; clients exchange typed retrieval-policy artifacts (query type, retrieval strategy, evidence pattern, failure mode, correction) rather than tool-routing scenarios; Algorithm 1 and Theorem 1 apply unchanged. Full setup in App. K.2. 

Table 7: Second instantiation on NQ-Open (3 seeds). SYNAPSE accuracy 0 _._ 724 vs. Centralized 0 _._ 756 (gap 0 _._ 032, tighter than _τ_ -bench 0 _._ 058): single-step RAG is less sensitive to federation constraints than multi-turn agent tasks. The typed-artifact protocol generalizes with no algorithmic changes.. 

|Setting|Accuracy (EM)|Faithfulness|Evidence Recall@5|
|---|---|---|---|
|Local-only RAG policy|0_._612_±_0_._024|0_._681_±_0_._021|0_._704_±_0_._026|
|Fed-ICL policy sharing|0_._661_±_0_._022|0_._708_±_0_._020|0_._733_±_0_._024|
|**SYNAPSE typed artifact**|**0**_._**724**_±_**0**_._**019**|**0**_._**771**_±_**0**_._**018**|**0**_._**801**_±_**0**_._**021**|
|Centralized oracle|0_._756_±_0_._017|0_._793_±_0_._016|0_._826_±_0_._019|



The federation–centralized gap of 0 _._ 032 on NQ-Open is tighter than the 0 _._ 058 on _τ_ -bench retail, consistent with single-step retrieval policies composing more cleanly under typed merge than multiturn tool decisions where each step compounds routing uncertainty. 

## **6 Limitations** 

Three limitations bound the deployment case. First, formal privacy covers only numeric metadata; text fields rely on heuristic masking with no ( _ε, δ_ )-LDP guarantee. Second, typed schemas concentrate liability, a malformed or adversarially crafted schema becomes a single point of failure under adaptive adversaries beyond the 50% Byzantine threshold. Third, the system emits no calibrated confidence score, requiring human-review escalation before high-stakes medical or legal decisions. Additionally, contraction fails on a LiveBench subset ( _L_<sup>ˆ(99%)</sup> _R_ =1 _._ 018 _>_ 1), leaving routing stability unverified on that distribution. 

## **7 Conclusion** 

Typed federated artifacts enable model-agnostic collaboration without sharing weights, prompts, or raw data, making privacy, conflict resolution, and cross-architectural transfer well-defined operations at the federation boundary. SYNAPSE matches centralized performance at _∼_ 10 _,_ 000 _×_ below the FedLoRA bandwidth floor (App. A). 

9 

## **References** 

- [1] Martín Abadi, Andy Chu, Ian Goodfellow, H. Brendan McMahan, Ilya Mironov, Kunal Talwar, and Li Zhang. Deep Learning with Differential Privacy. In _Proceedings of the 2016 ACM SIGSAC Conference on Computer and Communications Security_ , pages 308–318, October 2016. doi: 10.1145/2976749.2978318. URL `http://arxiv.org/abs/1607.00133` . arXiv:1607.00133 [stat]. 

- [2] Parker Addison, Minh-Tuan H. Nguyen, Tomislav Medan, Jinali Shah, Mohammad T. Manzari, Brendan McElrone, Laksh Lalwani, Aboli More, Smita Sharma, Holger R. Roth, Isaac Yang, Chester Chen, Daguang Xu, Yan Cheng, Andrew Feng, and Ziyue Xu. C-FedRAG: A Confidential Federated Retrieval-Augmented Generation System, December 2024. URL `http://arxiv.org/abs/2412.13163` . arXiv:2412.13163 [cs]. 

- [3] Anthropic. Model Context Protocol: An open standard for connecting AI assistants to data sources, 2024. URL `https://www.anthropic.com/news/model-context-protocol` . Accessed: 2026-04. 

- [4] Baris Askin, Shivam Patel, Anupam Nayak, Andrea Vigano, Jiin Woo, Gauri Joshi, and Carlee Joe-Wong. Federate the router: Learning language model routers with sparse and decentralized evaluations. _arXiv preprint arXiv:2601.22318_ , 2026. 

- [5] Peva Blanchard, El Mahdi El Mhamdi, Rachid Guerraoui, and Julien Stainer. Machine learning with adversaries: Byzantine tolerant gradient descent. In _Advances in Neural Information Processing Systems 30 (NIPS 2017)_ , pages 119–129, 2017. 

- [6] Keith Bonawitz, Vladimir Ivanov, Ben Kreuter, Antonio Marcedone, H. Brendan McMahan, Sarvar Patel, Daniel Ramage, Aaron Segal, and Karn Seth. Practical secure aggregation for federated learning on user-held data, 2016. URL `https://arxiv.org/abs/1611.04482` . 

- [7] Keith Bonawitz, Vladimir Ivanov, Ben Kreuter, Antonio Marcedone, H. Brendan McMahan, Sarvar Patel, Daniel Ramage, Aaron Segal, and Karn Seth. Practical secure aggregation for privacy preserving machine learning. Cryptology ePrint Archive, Paper 2017/281, 2017. URL `https://eprint.iacr.org/2017/281` . 

- [8] Nicholas Carlini, Florian Tramèr, Eric Wallace, Matthew Jagielski, Ariel Herbert-Voss, Katherine Lee, Adam Roberts, Tom Brown, Dawn Song, Ülfar Erlingsson, Alina Oprea, and Colin Raffel. Extracting training data from large language models. In _30th USENIX Security Symposium (USENIX Security 21)_ , pages 2633–2650, 2021. arXiv:2012.07805. 

- [9] Abhijit Chakraborty, Chahana Dahal, and Vivek Gupta. Federated retrieval-augmented generation: A systematic mapping study. In Christos Christodoulopoulos, Tanmoy Chakraborty, Carolyn Rose, and Violet Peng, editors, _Findings of the Association for Computational Linguistics: EMNLP 2025_ , pages 7362–7374, Suzhou, China, November 2025. Association for Computational Linguistics. ISBN 979-8-89176-335-7. doi: 10.18653/v1/2025.findings-emnlp.388. URL `https://aclanthology.org/2025.findings-emnlp.388/` . 

- [10] Minghui Chen, Ruinan Jin, Wenlong Deng, Yuanyuan Chen, Zhi Huang, Han Yu, and Xiaoxiao Li. Can Textual Gradient Work in Federated Learning?, February 2025. URL `http://arxiv. org/abs/2502.19980` . arXiv:2502.19980 [cs]. 

- [11] Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, Christopher Hesse, and John Schulman. Training Verifiers to Solve Math Word Problems, November 2021. URL `http://arxiv.org/abs/2110.14168` . arXiv:2110.14168 [cs]. 

- [12] Ittai Dayan, Holger R. Roth, Aoxiao Zhong, Ahmed Harouni, Amilcare Gentili, Anas Z. Abidin, Andrew Liu, Anthony Beardsworth Costa, Bradford J. Wood, Chien-Sung Tsai, et al. Federated learning for predicting clinical outcomes in patients with COVID-19. _Nature Medicine_ , 27(10): 1735–1743, 2021. 

- [13] Yves-Alexandre de Montjoye, César A. Hidalgo, Michel Verleysen, and Vincent D. Blondel. Unique in the crowd: The privacy bounds of human mobility. _Scientific Reports_ , 3(1):1376, 3 2013. doi: 10.1038/srep01376. URL `https://nature.com` . 

10 

- [14] Persi Diaconis and David Freedman. Iterated random functions. _SIAM Review_ , 41(1):45–76, 1999. doi: 10.1137/S0036144598338446. 

- [15] Yaxin Du, Yuanshuo Zhang, Xiyuan Yang, Yifan Zhou, Cheng Wang, Gongyi Zou, Xianghe Pang, Wenhao Wang, Menglan Chen, Shuo Tang, Zhiyu Li, Feiyu Xiong, and Siheng Chen. Infomosaic-bench: Evaluating multi-source information seeking in tool-augmented agents. _arXiv preprint arXiv:2510.02271_ , 2025. 

- [16] Haonan Duan, Adam Dziedzic, Mohammad Yaghini, Nicolas Papernot, and Franziska Boenisch. On the Privacy Risk of In-context Learning, November 2024. URL `http://arxiv.org/abs/ 2411.10512` . arXiv:2411.10512 [cs]. 

- [17] Cynthia Dwork and Aaron Roth. The Algorithmic Foundations of Differential Privacy. _Foundations and Trends® in Theoretical Computer Science_ , August 2014. doi: 10.1561/0400000042. URL `https://dl.acm.org/doi/10.1561/0400000042` . 

- [18] Tao Fan, Yan Kang, Guoqiang Ma, Weijing Chen, Wenbin Wei, Lixin Fan, and Qiang Yang. FATE-LLM: A Industrial Grade Federated Learning Framework for Large Language Models, October 2023. URL `http://arxiv.org/abs/2310.10049` . arXiv:2310.10049 [cs]. 

- [19] Jonas Geiping, Hartmut Bauermeister, Hannah Dröge, and Michael Moeller. Inverting gradients – how easy is it to break privacy in federated learning?, 2020. URL `https://arxiv.org/abs/ 2003.14053` . 

- [20] Aaron Grattafiori, Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, et al. The Llama 3 Herd of Models, November 2024. URL `http://arxiv.org/abs/2407.21783` . arXiv:2407.21783 [cs]. 

- [21] Michael Günther, Jackmin Ong, Isabelle Mohr, Alaeddine Abdessalem, Tanguy Abel, Mohammad Kalim Akram, Susana Guzman, Georgios Mastrapas, Saba Sturua, Bo Wang, Maximilian Werk, Nan Wang, and Han Xiao. Jina Embeddings 2: 8192-Token General-Purpose Text Embeddings for Long Documents, February 2024. URL `http://arxiv.org/abs/2310.19923` . arXiv:2310.19923 [cs]. 

- [22] Weirui Kuang, Bingchen Qian, Zitao Li, Daoyuan Chen, Dawei Gao, Xuchen Pan, Yuexiang Xie, Yaliang Li, Bolin Ding, and Jingren Zhou. Federatedscope-llm: A comprehensive package for fine-tuning large language models in federated learning. In _Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining_ , KDD ’24, page 5260–5271, New York, NY, USA, 2024. Association for Computing Machinery. ISBN 9798400704901. doi: 10.1145/3637528.3671573. URL `https://doi.org/10.1145/3637528.3671573` . 

- [23] Kenton Lee, Ming-Wei Chang, and Kristina Toutanova. Latent retrieval for weakly supervised open domain question answering. In Anna Korhonen, David Traum, and Lluís Màrquez, editors, _Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics_ , pages 6086–6096, Florence, Italy, July 2019. Association for Computational Linguistics. doi: 10.18653/v1/P19-1612. URL `https://aclanthology.org/P19-1612/` . 

- [24] Tao Lin, Lingjing Kong, Sebastian U Stich, and Martin Jaggi. Ensemble distillation for robust model fusion in federated learning. _Advances in neural information processing systems_ , 33: 2351–2363, 2020. 

- [25] Elias Lumer, Pradeep Honaganahalli Basavaraju, Myles Mason, James A. Burke, and Vamse Kumar Subbiah. Graph RAG-Tool Fusion, February 2025. URL `http://arxiv.org/abs/2502. 07223` . arXiv:2502.07223 [cs]. 

- [26] Qianren Mao, Qili Zhang, Hanwen Hao, Zhentao Han, Runhua Xu, Weifeng Jiang, Qi Hu, Zhijun Chen, Tyler Zhou, Bo Li, Yangqiu Song, Jin Dong, Jianxin Li, and Philip S. Yu. PrivacyPreserving Federated Embedding Learning for Localized Retrieval-Augmented Generation, April 2025. URL `http://arxiv.org/abs/2504.19101` . arXiv:2504.19101 [cs]. 

- [27] Jonathan Mayer, Patrick Mutchler, and John C. Mitchell. Evaluating the privacy properties of telephone metadata. _Proceedings of the National Academy of Sciences_ , 113(20):5536–5541, 2016. 

11 

- [28] H Brendan McMahan, Daniel Ramage, Kunal Talwar, and Li Zhang. Learning differentially private recurrent language models. _arXiv preprint arXiv:1710.06963_ , 2017. 

- [29] Guozhao Mo, Wenliang Zhong, Jiawei Chen, Xuanang Chen, Yaojie Lu, Hongyu Lin, Ben He, Xianpei Han, and Le Sun. Livemcpbench: Can agents navigate an ocean of mcp tools? _arXiv preprint arXiv:2508.01780_ , 2025. 

- [30] Nasdaq Verafin. Fighting financial crime within your institution – and beyond: The power of consortium analytics. White paper, Nasdaq Verafin, 10 2023. URL `https://verafin.com/wp-content/uploads/2023/10/ consortium-analytics-fraud-white-paper-verafin-20231018.pdf` . Accessed: 2026-05-02. 

- [31] Shishir G. Patil, Tianjun Zhang, Xin Wang, and Joseph E. Gonzalez. Gorilla: Large language model connected with massive apis. In A. Globerson, L. Mackey, D. Belgrave, A. Fan, U. Paquet, J. Tomczak, and C. Zhang, editors, _Advances in Neural Information Processing Systems_ , volume 37, pages 126544–126565. Curran Associates, Inc., 2024. doi: 10.52202/079017-4020. 

- [32] Yujia Qin, Shihao Liang, Yining Ye, Kunlun Zhu, Lan Yan, Yaxi Lu, Yankai Lin, Xin Cong, Xiangru Tang, Bill Qian, et al. Toolllm: Facilitating large language models to master 16000+ real-world apis. _arXiv preprint arXiv:2307.16789_ , 2023. 

- [33] Nicola Rieke, Jonny Hancox, Wenqi Li, Fausto Milletarì, Holger R. Roth, Shadi Albarqouni, Spyridon Bakas, Mathieu N. Galtier, Bennett A. Landman, Klaus Maier-Hein, Sébastien Ourselin, Micah Sheller, Ronald M. Summers, Andrew Trask, Daguang Xu, Maximilian Baust, and M. Jorge Cardoso. The future of digital health with federated learning. _npj Digital Medicine_ , 3(1):119, 2020. 

- [34] Stephen Robertson and Hugo Zaragoza. The Probabilistic Relevance Framework: BM25 and Beyond. _Found. Trends Inf. Retr._ , 3(4):333–389, April 2009. ISSN 1554-0669. doi: 10.1561/1500000019. URL `https://doi.org/10.1561/1500000019` . 

- [35] Timo Schick, Jane Dwivedi-Yu, Roberto Dessì, Roberta Raileanu, Maria Lomeli, Eric Hambro, Luke Zettlemoyer, Nicola Cancedda, and Thomas Scialom. Toolformer: Language models can teach themselves to use tools. In _Advances in Neural Information Processing Systems 36 (NeurIPS 2023)_ , 2023. arXiv:2302.04761. 

- [36] Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik Narasimhan, and Shunyu Yao. Reflexion: language agents with verbal reinforcement learning. In _Proceedings of the 37th International Conference on Neural Information Processing Systems_ , NIPS ’23, Red Hook, NY, USA, 2023. Curran Associates Inc. 

- [37] Reza Shokri, Marco Stronati, Congzheng Song, and Vitaly Shmatikov. Membership inference attacks against machine learning models. In _2017 IEEE symposium on security and privacy (SP)_ , pages 3–18. IEEE, 2017. 

- [38] P. Srihari and Dr. Swathi Ramesh. Transparency and privacy the role of explainable ai and federated learning in financial fraud detection. _International Journal of Scientific Research in Computer Science, Engineering and Information Technology_ , 10(6):555–566, Nov. 2024. URL `https://ijsrcseit.com/index.php/home/article/view/CSEIT241061105` . 

- [39] Aarohi Srivastava, Abhinav Rastogi, and Abhishek Rao .et.al. Beyond the imitation game: Quantifying and extrapolating the capabilities of language models, 2023. URL `https:// arxiv.org/abs/2206.04615` . 

- [40] Youbang Sun, Zitao Li, Yaliang Li, and Bolin Ding. Improving LoRA in Privacypreserving Federated Learning, March 2024. URL `http://arxiv.org/abs/2403.12313` . arXiv:2403.12313 [cs]. 

- [41] Toyotaro Suzumura, Yi Zhou, Natahalie Baracaldo, Guangnan Ye, Keith Houck, Ryo Kawahara, Ali Anwar, Lucia Larise Stavarache, Yuji Watanabe, Pablo Loyola, et al. Towards federated graph learning for collaborative financial crimes detection. _arXiv preprint arXiv:1909.12946_ , 2019. 

12 

- [42] Praneeth Vepakomma, Otkrist Gupta, Tristan Swedish, and Ramesh Raskar. Split learning for health: Distributed deep learning without sharing raw patient data, 2018. URL `https: //arxiv.org/abs/1812.00564` . 

- [43] Ruhan Wang, Zhiyong Wang, Chengkai Huang, Rui Wang, Tong Yu, Lina Yao, John C. S. Lui, and Dongruo Zhou. Federated In-Context Learning: Iterative Refinement for Improved Answer Quality, June 2025. URL `http://arxiv.org/abs/2506.07440` . arXiv:2506.07440 [cs]. 

- [44] Stefanie Warnat-Herresthal, Hartmut Schultze, Krishnaprasad Shastry, Sathyanarayanan Manamohan, Saikat Mukherjee, Vishesh Garg, Ravi Sarveswara, Kristian Händler, Peter Pickkers, N. Ahmad Aziz, Sofia Ktena, Florian Tran, Michael Bitzer, Stephan Ossowski, Nicolas Casadei, Christian Herr, Daniel Petersheim, Uta Behrends, Fabian Kern, and Thirumalaisamy Velavan. Swarm learning for decentralized and confidential clinical machine learning. _Nature_ , 594, 06 2021. doi: 10.1038/s41586-021-03583-3. 

- [45] Colin White, Samuel Dooley, Manley Roberts, Arka Pal, Ben Feuer, Siddhartha Jain, Ravid Shwartz-Ziv, Neel Jain, Khalid Saifullah, Sreemanti Dey, Shubh-Agrawal, Sandeep Singh Sandha, Siddartha Naidu, Chinmay Hegde, Yann LeCun, Tom Goldstein, Willie Neiswanger, and Micah Goldblum. LiveBench: A Challenging, Contamination-Limited LLM Benchmark, April 2025. URL `http://arxiv.org/abs/2406.19314` . arXiv:2406.19314 [cs]. 

- [46] Feijie Wu, Zitao Li, Yaliang Li, Bolin Ding, and Jing Gao. FedBiOT: LLM Local Fine-tuning in Federated Learning without Full Model, June 2024. URL `http://arxiv.org/abs/2406. 17706` . arXiv:2406.17706 [cs]. 

- [47] Binfeng Xu, Zhiyuan Peng, Bowen Lei, Subhabrata Mukherjee, Yuchen Liu, and Dongkuan Xu. ReWOO: Decoupling Reasoning from Observations for Efficient Augmented Language Models, May 2023. URL `http://arxiv.org/abs/2305.18323` . arXiv:2305.18323 [cs]. 

- [48] Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, and Yuan Cao. ReAct: Synergizing reasoning and acting in language models. In _International Conference on Learning Representations (ICLR 2023)_ , 2023. arXiv:2210.03629. 

- [49] Shunyu Yao, Noah Shinn, Pedram Razavi, and Karthik Narasimhan. _τ_ -bench: A benchmark for tool-agent-user interaction in real-world domains. _arXiv preprint arXiv:2406.12045_ , 2024. URL `http://arxiv.org/abs/2406.12045` . 

- [50] Rui Ye, Wenhao Wang, Jingyi Chai, Dihan Li, Zexi Li, Yinda Xu, Yaxin Du, Yanfeng Wang, and Siheng Chen. Openfedllm: Training large language models on decentralized private data via federated learning. In _Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining_ , KDD ’24, page 6137–6147, New York, NY, USA, 2024. Association for Computing Machinery. ISBN 9798400704901. doi: 10.1145/3637528.3671582. URL `https://doi.org/10.1145/3637528.3671582` . 

- [51] Dong Yin, Yudong Chen, Ramchandran Kannan, and Peter Bartlett. Byzantine-robust distributed learning: Towards optimal statistical rates. In Jennifer Dy and Andreas Krause, editors, _Proceedings of the 35th International Conference on Machine Learning_ , volume 80 of _Proceedings of Machine Learning Research_ , pages 5650–5659. PMLR, 10–15 Jul 2018. URL `https://proceedings.mlr.press/v80/yin18a.html` . 

- [52] Mert Yuksekgonul, Federico Bianchi, Joseph Boen, Sheng Liu, Zhi Huang, Carlos Guestrin, and James Zou. TextGrad: Automatic "Differentiation" via Text, June 2024. URL `http: //arxiv.org/abs/2406.07496` . arXiv:2406.07496 [cs]. 

- [53] Huimin Zeng, Zhenrui Yue, Qian Jiang, and Dong Wang. Federated recommendation via hybrid retrieval augmented generation. In _2024 IEEE international conference on big data (BigData)_ , pages 8078–8087. IEEE, 2024. 

- [54] Collin Zhang, John X. Morris, and Vitaly Shmatikov. Extracting Prompts by Inverting LLM Outputs, October 2024. URL `http://arxiv.org/abs/2405.15012` . arXiv:2405.15012 [cs]. 

- [55] Yiming Zhang, Nicholas Carlini, and Daphne Ippolito. Effective Prompt Extraction from Language Models, August 2024. URL `http://arxiv.org/abs/2307.06865` . arXiv:2307.06865 [cs]. 

13 

- [56] Dongfang Zhao. FRAG: Toward Federated Vector Database Management for Collaborative and Secure Retrieval-Augmented Generation, October 2024. URL `http://arxiv.org/abs/ 2410.13272` . arXiv:2410.13272 [cs]. 

- [57] Ligeng Zhu, Zhijian Liu, and Song Han. _Deep leakage from gradients_ . Curran Associates Inc., Red Hook, NY, USA, 2019. 

14 

## **A Ethical Considerations** 

SYNAPSE is evaluated on tool-routing and NQ-Open retrieval-policy artifacts; the protocol extends to other typed-object settings via schema substitution. Three empirical gaps bound the current results: real-API experiments are limited in scale and duration; LiveMCPBench-class catalogs ( _∼_ 500 tools) are not directly evaluated; and the contraction premise fails on a LiveBench subset ( _L_<sup>ˆ(99%)</sup> _R_ =1 _._ 018 _>_ 1), voiding the routing-stability guarantee on that distribution. Three deployment prerequisites remain open before any regulated rollout: _(i)_ calibrated _ε_ -LDP for text fields (current masking is heuristic with no formal guarantee); _(ii)_ confidence-gated escalation to human review for low-confidence routing decisions; _(iii)_ a right-to-erasure re-materialization pathway (structurally supported by Algorithm 1 but not implemented). Sybil attacks past the 40% Byzantine tolerance threshold and adaptive adversaries tuned to the robust operator remain future work; rate-limited registration and cross-edge consistency checks are compatible mitigations but are not yet evaluated. SYNAPSE is not a HIPAA/GDPR-complete stack; the schema _S_ provides the dispatch points for each extension but does not fulfil them. 

## **B Robustness to Noisy and Adversarial Clients** 

SYNAPSE is evaluated against three adversarial modes: cross-source contamination (clients inject scenarios from unrelated domains), random scenario corruption (random text replacement), and tool-confusion attacks (deliberate `parent_tool_name` mislabeling). Headline curves (Fig. 2 in §5.2): all three modes stable through 40% adversarial clients, sharp collapse at 60%. Random noise is largely absorbed by cosine deduplication; cross-source is partially absorbed by schema validation; tool-confusion is hardest because adversaries produce schema-valid scenarios whose only error is the `parent_tool_name` field, which clusters with honest scenarios for the same task type. Mitigation: cross-validating clustered `parent_tool_name` fields against the canonical tool registry _T_ at Algorithm 1 line 5 before line 12 – already in released code; without it, tool-confusion at 40% collapses to 0 _._ 48 rather than 0 _._ 62. The 40% stable boundary aligns with Theorem 3’s empirically measured contraction regime ( _L_<sup>ˆ(99%)</sup> _R_ = 0 _._ 891, ∆<sup>ˆ(5%)</sup> = 0 _._ 138, App. L); at 60% the contraction premise fails empirically. 

## **C Empirical Prompt-Extraction Attack** 

_Setup._ Following [54]: clients generate responses to server queries using private in-context examples; GPT-4o adversary observes only the responses and reconstructs originals. We report membershipinference AUROC (50/50 balanced), adversary–ground-truth token overlap, and the fraction of clients whose token overlap stays under 0 _._ 10. Full pipeline = formal DP on numeric metadata + heuristic masking on text; this characterizes empirical privacy of the deployed system, distinct from the formal ( _ε,_ 0)-DP claim of Theorem 1 which applies only to the numeric-metadata mechanism. 

Table 8: Empirical prompt-extraction attack: adversary AUROC degrades to chance at the strongest privacy setting. 

|Setting|Token overlap|AUROC|% clients_<_0_._10|
|---|---|---|---|
|No privacy|0_._20|0_._62|50%|
|_ε_=1_._0_, λ_=1_._0|0_._07|0_._54|84%|
|_ε_=0_._5_, λ_=1_._5|0_._03|0_._50|95%|



**Privacy–utility frontier.** To characterize the deployment-relevant operating range rather than a single point, Tab. 9 sweeps the per-round privacy budget _ε ∈{_ 0 _._ 5 _,_ 1 _._ 0 _,_ 2 _._ 0 _}_ and the text-masking strength _λ ∈{_ 0 _._ 5 _,_ 1 _._ 0 _,_ 1 _._ 5 _}_ . Composed _ε_<sup>_′_</sup> uses basic sequential composition _ε_<sup>_′_</sup> = _Rε_ (pure ( _ε_<sup>_′_</sup> _,_ 0)-DP); for the small- _R_ regime ( _R_ =3) evaluated here, basic composition is strictly tighter than the advanced composition bound and is what we report. 

15 

Table 9: Privacy–utility sweep on GSM8k (5 IID clients, 5 seeds, _R_ =3 rounds). Composed _ε_<sup>_′_</sup> uses basic sequential composition _ε_<sup>_′_</sup> = _Rε_ (pure ( _ε_<sup>_′_</sup> _,_ 0)-DP), which is strictly tighter than advanced composition for the small- _R_ regime evaluated here; Theorem 1 gives both bounds. Bold rows are the operating points reported in body §5 and Tab. 8. Tighter privacy ( _ε ↓_ , _λ ↑_ ) reduces both adversary AUROC and routing accuracy; the steepest privacy gain occurs in the ( _ε_ =1 _._ 0 _, λ_ =1 _._ 0) _→_ ( _ε_ =0 _._ 5 _, λ_ =1 _._ 5) regime (∆ AUROC =0 _._ 04, ∆ accuracy =0 _._ 05). The _ε_ =0 _._ 5 _, λ_ =1 _._ 5 operating point drives adversary AUROC to chance (0 _._ 50) at 5 pts of routing utility, with composed budget _ε_<sup>_′_</sup> =1 _._ 5 over three rounds. 

|_ε_|_λ_|_ε_<sup>_′_ </sup>(_R_=3)|Routing acc.|AUROC|Token overlap|% clients_<_0_._10|
|---|---|---|---|---|---|---|
|_∞_|0_._0|—|0_._935_±_0_._018|0_._62|0_._20|50%|
|2_._0|0_._5|6_._0|0_._928_±_0_._020|0_._59|0_._13|70%|
|2_._0|1_._0|6_._0|0_._914_±_0_._023|0_._56|0_._10|78%|
|2_._0|1_._5|6_._0|0_._897_±_0_._025|0_._53|0_._07|85%|
|1_._0|0_._5|3_._0|0_._909_±_0_._024|0_._57|0_._11|76%|
|1_._0|1_._0|3_._0|**0**_._**902**_±_**0**_._**026**|**0**_._**54**|**0**_._**07**|**84**%|
|1_._0|1_._5|3_._0|0_._881_±_0_._028|0_._52|0_._05|90%|
|0_._5|0_._5|1_._5|0_._884_±_0_._027|0_._55|0_._08|83%|
|0_._5|1_._0|1_._5|0_._866_±_0_._030|0_._52|0_._05|90%|
|0_._5|1_._5|1_._5|**0**_._**851**_±_**0**_._**032**|**0**_._**50**|**0**_._**03**|**95**%|



## **D Planner-Based Agent Baselines: ReWOO and Reflexion** 

This appendix documents the comparison protocol for the two planner-based agents in Tab. 6. The motivation is to disentangle two confounded effects: _routing-as-memory_ (SYNAPSE, where the federated compendium provides typed knowledge that the router queries) versus _routing-as-planning_ (ReWOO, Reflexion, where a centralized planner LLM decomposes the task and selects tools without relying on shared memory). 

**Setup.** Both planner-based agents use Llama-3.1-8B-instruct (matching our reranker LLM) for all LLM components, share the per-tool execution wrappers used by SYNAPSE, and operate centralized – they have full access to the 32-tool inventory and benchmark distribution at inference time, a strictly more permissive setting than SYNAPSE’s federated regime. ReWOO [47] uses the standard planner prompt (decompose-then-execute); Reflexion [36] uses _K_ =3 trials with verbal-feedback memory. We score multi-step chains as successful only if a single trial completes all steps; we do not cherry-pick best-of-trials across steps, which makes Tab. 6’s entries directly comparable to single-trial methods. Neither planner can be straightforwardly federated without sharing either the planner prompts (which contain the full tool inventory) or the episodic-reflection buffer (which contains private query traces). SYNAPSE’s claim is not that compendium-based routing beats centralized planners in absolute terms; it is that routing memory and routing planning are different mechanisms, and SYNAPSE approaches centralized planner performance under constraints planner-based agents architecturally cannot satisfy. 

**Results and compute cost.** ReWOO single-step (0 _._ 89) sits within 0 _._ 01 of SYNAPSE (0 _._ 88). ReWOO’s 12-step accuracy (0 _._ 46) sits 0 _._ 19 below SYNAPSE (0 _._ 65): without replanning, intermediate failures geometrically compound. Reflexion ( _K_ =3) leads single-step at 0 _._ 93 but drops below SYNAPSE at 12-step (0 _._ 64 vs. 0 _._ 65). Reflexion’s competitiveness costs up to 3 _×_ per-step compute and 36 _×_ total per chain (Tab. 10); SYNAPSE’s per-step cost is independent of chain length. 

Table 10: Per-step inference cost across multi-step methods. Federation cost for SYNAPSE is amortized outside inference; per-step routing cost equals one retrieval+rerank pass. 

|Method|Per-step routing/planning|8-step relative|12-step relative|
|---|---|---|---|
|SYNAPSE/ Centralized|1 routing pass per step|1_._0_×_|1_._0_×_|
|ReWOO|1 upfront planner call + execution|_∼_1_._1_×_|_∼_1_._1_×_|
|Refexion (_K_=3)|up to3trials per step|3_._0_×_worst-case|3_._0_×_worst-case|
|ReAct|1 reactive loop per step|_∼_1_._2–1_._5_×_|_∼_1_._2–1_._5_×_|



16 

## **E Byzantine-Robust Aggregation: Empirical Evaluation** 

The main paper’s threat model is honest-but-curious. This appendix extends to a Byzantine setting where adversaries submit schema-valid payloads designed to maximize misrouting harm. 

**Setup.** Adversarial fraction is measured over submitted compendium entries (not clients), permitting fractional rates with 5 clients. Two attack modes: _schema-valid poisoning_ (entries pass schema validation but contain wrong tool _→_ scenario mappings, defeating schema validation by construction) and _coordinated targeting_ (multiple adversarial submissions push the same poisoned scenario past cosine deduplication _τ_ =0 _._ 85, defeating dedup by exploiting majority-of-cluster). Three aggregation rules at the edge layer: baseline SYNAPSE (Algorithm 1, cosine-cluster + cluster majority), _+Krum_ [5] (drop entries furthest from cluster centroid before majority vote), and _+TrimmedMean_ [51] (drop top/bottom _f_ entries before majority). GSM8k, 5 clients, 3 rounds, 200 held-out queries; adversarial fractions _{_ 0 _,_ 10 _,_ 20 _,_ 33 _,_ 50 _}_ %. 

Table 11: Byzantine-robust aggregation under schema-valid poisoning and coordinated-targeting. Mean lift over no-defense baseline: +8–19 pts at 20–33% adversarial; +16–25 pts at 50%. Both robust operators cost _∼_ 1 pt at 0% adversarial (slight over-conservatism). TrimmedMean outperforms Krum at 50% because Krum’s most-central selection retains a single entry while TrimmedMean averages over the surviving cluster; under near-majority attack, Krum’s selection is more likely to be adversarial. Open questions: adaptive adversaries that tune attacks to the specific operator, Sybil attacks past 50%, and attacks exploiting LLM reranker prompt sensitivity rather than merge. 

|Adv. fraction|Attack|Baseline SYNAPSE|+ Krum|+ TrimmedMean|
|---|---|---|---|---|
|0%|Control|0_._920(184_/_200)|0_._915(183_/_200)|0_._910(182_/_200)|
|10%|Poisoning|0_._895(179_/_200)|0_._915(183_/_200)|0_._910(182_/_200)|
|10%|Targeting|0_._875(175_/_200)|0_._905(181_/_200)|0_._910(182_/_200)|
|20%|Poisoning|0_._825(165_/_200)|0_._895(179_/_200)|0_._900(180_/_200)|
|20%|Targeting|0_._775(155_/_200)|0_._875(175_/_200)|0_._885(177_/_200)|
|33%|Poisoning|0_._700(140_/_200)|0_._850(170_/_200)|0_._860(172_/_200)|
|33%|Targeting|0_._600(120_/_200)|0_._815(163_/_200)|0_._825(165_/_200)|
|50%|Poisoning|0_._485( 97_/_200)|0_._630(126_/_200)|0_._705(141_/_200)|
|50%|Targeting|0_._345( 69_/_200)|0_._520(104_/_200)|0_._620(124_/_200)|



## **F Edge Merge Operator: Detailed Specification and Sensitivity Analysis** 

**Full Algorithm 1 with numeric path and conflict-log specification.** The body Algorithm 1 presents a compact form. Below we give the complete specification with the numeric-aggregation block, IsConsistent definition, and ConflictsToPrecautions mapping. 

**Numeric subfield aggregation.** The numeric path is enforced in two stages, calibrated for user-level adjacency (Theorem 1) under a semi-honest edge trust model. 

_Stage 1: Per-user clipping at the client._ Each end-user’s contribution to client _k_ ’s numeric record is clipped at ∆<sup>(</sup> _m_<sup>_j_)per field before being incorporated into</sup><sup>_C_</sup> _k_<sup>_.M_.Per-field clipping bounds the user’s</sup><sup>_ℓ_</sup> 1 contribution at ∆<sup>(</sup> _m_<sup>_j_)across all numeric subfields.In the single-user-per-client configuration used in</sup> our experiments, this reduces to per-client clipping; in multi-user-per-client deployments, the bound must be enforced at user-record granularity _before_ any client-level aggregation (see “Multi-user deployments” below). 

_Stage 2: Edge-side averaging and noising._ Each client _k_ transmits its clipped record clip( _Ck.M.m_<sup>(</sup><sup>_j_)</sup> _,_ ∆<sup>(</sup> _m_<sup>_j_))</sup><sup>_∈_[</sup><sup>_−_∆(</sup> _m_<sup>_j_)</sup><sup>_,_∆(</sup> _m_<sup>_j_)] to the edge aggregator, which computes the per-field average</sup> over _K_ clients and adds Laplace noise calibrated to the average’s sensitivity: 


![](P065_images/P065.pdf-0017-10.png)

### Figure analysis

Purpose: The figure formalizes the numeric subfield aggregation step in the Edge Merge Operator, showing how the edge aggregator releases a differentially private averaged numeric field.

Transcribed equation:

$$
C_E.M.m^{(j)} \leftarrow \frac{1}{K}\sum_{k=1}^{K}\operatorname{clip}\left(C_k.M.m^{(j)},\Delta_m^{(j)}\right) + \operatorname{Lap}\left(\frac{\Delta_m^{(j)}}{K\cdot \epsilon^{(j)}}\right)
$$

Important components:
- $C_E.M.m^{(j)}$: the edge-level merged value for numeric subfield $m^{(j)}$.
- $K$: number of clients contributing to the edge aggregate.
- $C_k.M.m^{(j)}$: client $k$'s value for numeric subfield $m^{(j)}$.
- $\operatorname{clip}(\cdot,\Delta_m^{(j)})$: per-field clipping operation that bounds each client's contribution by the clipping threshold $\Delta_m^{(j)}$.
- $\operatorname{Lap}(\Delta_m^{(j)}/(K\cdot\epsilon^{(j)}))$: Laplace noise added after averaging, with scale determined by the clipped sensitivity divided by the number of clients and the per-field privacy budget.

Direct visual observation: The computation consists of two additive terms: a mean over clipped client contributions and a Laplace noise term. The summation runs from client $k=1$ to $K$, and the privacy-noise scale decreases as either $K$ or $\epsilon^{(j)}$ increases.

Interpretation: This equation implements the paper's stated two-stage numeric aggregation path: client-side clipping followed by edge-side averaging and noising. Because a single user's bounded contribution affects only one client's clipped value and then enters the average with weight $1/K$, the visual formula matches the surrounding discussion that the released average has sensitivity $\Delta_m^{(j)}/K$ and uses Laplace noise calibrated to that sensitivity.

Connection to surrounding text: The equation appears in the section describing the detailed specification and sensitivity analysis of the Edge Merge Operator. It supports the explanation that per-field privacy budgets $\epsilon^{(j)}$ are used for numeric subfields and that the aggregation mechanism provides per-field differential privacy under the stated user-level adjacency and semi-honest edge trust model.


Under user-level adjacency with stage-1 clipping in place, one user’s contribution influences exactly one client’s clipped value, which contributes 1 _/K_ to the average; the per-user _ℓ_ 1-sensitivity of the 

17 

released average is therefore ∆<sup>(</sup> _m_<sup>_j_)</sup><sup>_/K_.The noise scale ∆(</sup> _m_<sup>_j_)</sup><sup>_/_(</sup><sup>_K · ε_(</sup><sup>_j_)) yields per-field</sup><sup>_ε_(</sup><sup>_j_)-DP per</sup> round. Per-field budgets _ε_<sup>(</sup><sup>_j_)</sup> sum to the per-round budget _ε_ via sequential composition (Theorem 1 statement; App. L, §L.2 proof). 

_Trust model._ The edge aggregator is semi-honest: it follows Algorithm 1 faithfully but may attempt inference from the clipped values it receives prior to noising. Secure aggregation [6] can be layered on the numeric path so the edge observes only the noisy aggregate, weakening the trust assumption to the ideal-functionality only; the protocol described above is the configuration used in our experiments and operates without secure aggregation. 

**Multi-user-per-client deployments.** When a single client aggregates contributions from _U ≥_ 2 end-users (e.g., an institution serving multiple users behind one federated client), the user-level guarantee requires two additional safeguards beyond the single-user-per-client configuration: 

_(a) Per-user clipping at the client._ Each end-user’s contribution to client _k_ ’s numeric record is clipped at ∆<sup>(</sup> _m_<sup>_j_)per field</sup><sup>_at user-record granularity_, before any client-level aggregation.Concretely:</sup> client _k_ maintains _U_ per-user buffers _{bk,u}_<sup>_U_</sup> _u_ =1<sup>, each clipped to [</sup><sup>_−_∆</sup> _m_<sup>(</sup><sup>_j_)</sup><sup>_,_∆(</sup> _m_<sup>_j_)]; the client-level record</sup> _Ck.M.m_<sup>(</sup><sup>_j_)</sup> is the average (1 _/U_ )<sup>�</sup> _u_<sup>_bk,u_rather than the sum.This keeps the per-user contribution to</sup> the released edge average bounded by ∆<sup>(</sup> _m_<sup>_j_)</sup><sup>_/_(</sup><sup>_KU_), recovering user-level</sup><sup>_ℓ_</sup> 1<sup>-sensitivity ∆</sup> _m_<sup>(</sup><sup>_j_)</sup><sup>_/_(</sup><sup>_KU_)</sup> at the released average. Equivalently, deployments that prefer to keep the noise scale fixed at ∆<sup>(</sup> _m_<sup>_j_)</sup><sup>_/_(</sup><sup>_Kε_(</sup><sup>_j_)) must scale the effective sensitivity input to</sup><sup>_U·_∆(</sup> _m_<sup>_j_)and increase the noise accordingly</sup> to _U ·_ ∆<sup>(</sup> _m_<sup>_j_)</sup><sup>_/_(</sup><sup>_Kε_(</sup><sup>_j_)) — a utility cost growing linearly in</sup><sup>_U_.</sup> 

_(b) Per-user-per-round field count bound._ A single user may contribute to multiple numeric fields per round (e.g., a user who invokes both tool _t_ 1 and tool _t_ 2 affects the per-tool call counts and frequency vectors for both tools). To preserve user-level adjacency under sequential composition across _Kf_ fields, we bound the number of fields any single user can affect in one round at _F_<sup>_∗_</sup> _≤ Kf_ via a per-user-per-round field cap enforced at the client: each user’s contribution is restricted to at most _F_<sup>_∗_</sup> distinct numeric fields per round (chosen as the user’s _F_<sup>_∗_</sup> most-touched tools by raw frequency), with contributions to other fields zeroed before client-level aggregation. Under this cap, the per-user _ℓ_ 1-sensitivity across the full numeric vector is bounded by _F_<sup>_∗_</sup> _·_ max _j_ ∆ _m_<sup>(</sup><sup>_j_)rather than �</sup> _j_<sup>∆</sup> _m_<sup>(</sup><sup>_j_), and</sup> the per-round budget allocation _ε_<sup>(</sup><sup>_j_)</sup> = _ε/F_<sup>_∗_</sup> is sufficient to maintain per-round ( _ε,_ 0)-DP. In our single-user-per-client experiments we use _F_<sup>_∗_</sup> = _Kf_ (no effective cap) since natural per-user activity is bounded; multi-user-per-client deployments should set _F_<sup>_∗_</sup> _<Kf_ explicitly. 

_Combined accounting._ A multi-user-per-client deployment with _U_ users per client and per-user-perround field cap _F_<sup>_∗_</sup> achieves per-round ( _ε,_ 0)-DP under user-level adjacency by setting: 

- Per-user clipping at the client: ∆<sup>(</sup> _m_<sup>_j_)</sup> 

   - _m_<sup>per field per user;</sup> 

- Field cap per user per round: _F_<sup>_∗_</sup> ; 

- Per-field budget: _ε_<sup>(</sup><sup>_j_)</sup> = _ε/F_<sup>_∗_</sup> ; 

- Edge noise scale: ∆<sup>(</sup> _m_<sup>_j_)</sup><sup>_/_(</sup><sup>_KUε_(</sup><sup>_j_))iftheclientaveragesoveritsusers(option(a)),or</sup> _U_ ∆<sup>(</sup> _m_<sup>_j_)</sup><sup>_/_(</sup><sup>_Kε_(</sup><sup>_j_))iftheclientsumsandtheedgere-noises(utility-equivalentif</sup><sup>_U/_(</sup><sup>_ε_(</sup><sup>_j_))=</sup> _U ·_ 1 _/ε_<sup>(</sup><sup>_j_)</sup> ). 

The two accountings give identical released utility; the choice is operational. Both reduce to the single-user case at _U_ =1, _F_<sup>_∗_</sup> = _Kf_ . 

_Canonical fields._ Tool identifiers, descriptions, and API signatures in _M_ are server-controlled and not noised; only client-contributed numeric statistics (per-tool call counts, empirical success rates, per-tool usage frequencies) are clipped and noised before edge aggregation. 

IsConsistent( _C_ ) **definition.** For a cluster _C_ of usage scenarios, IsConsistent( _C_ ) := true iff for every pair ( _u_ 1 _, u_ 2) _∈C_<sup>2</sup> : 

1. **Structured-field agreement.** Both scenarios reference the same `parent_tool` identifier and their `precondition` flag sets are jointly satisfiable (no flag pair _{f, ¬f }_ ). 

2. **LLM semantic consistency.** An LLM consistency probe ( `llama-3.1-8b-instruct` , prompt template in App. M) returns `Consistent` when shown both natural-language scenarios. 

18 

Both checks must pass; either failure marks the cluster conflicted. 

**Conflict log** _L_<sup>(</sup><sup>_r_)</sup> **.** A stateful edge-side artifact ( _not_ exchanged across clients), keyed by ( _t,_ centroid_id). Each entry stores the centroid scenario plus all dissenting scenarios from the current round’s clustering. _L_<sup>(</sup><sup>_r_)</sup> is the union of conflict entries from round _r_ ; _L_<sup>(0)</sup> = _∅_ . 

ConflictsToPrecautions( _L_<sup>(</sup><sup>_r−_1)</sup> ) **mapping.** For each entry (( _t,_ centroid_id) _, {u_ centroid _, u_ 1 _, . . . , ud}_ ) _∈ L_<sup>(</sup><sup>_r−_1)</sup> , emit a structured Precaution: (tool : _t,_ precaution : TextGradSummarize _S_ ( _u_ centroid _⊕{ui}_ )), where _⊕_ denotes a structured concatenation prompt: “Combine the following scenario with each of its dissenting variants into a single precaution rule that captures both the affirmative case and the exception conditions.” This produces composed Precautions of the form “Use _X_ for _Y_ ; do not use _X_ when _Z_ ”. 

**Annex** _A_ **.** Schema-validated entity–relation triples from clients are deduplicated via cosine similarity (same _τ_ ) and passed through. The retrieval pipeline (§3) consults _A_ to resolve cross-tool dependencies during query routing. 

**Sensitivity to cosine threshold** _τ_ **.** Tab. 12 reports routing accuracy and compendium size as _τ_ varies. Lower _τ_ over-merges semantically distinct scenarios; higher _τ_ under-merges. We use _τ_ =0 _._ 85. 

Table 12: Sensitivity to cosine deduplication threshold _τ_ (GSM8k, 5 IID clients, 5 seeds). 

|_τ_|Routing acc.|Compendium KB|# scenarios|Dedup rate|
|---|---|---|---|---|
|0_._75|0_._87_±_0_._02|48|172|77%|
|0_._80|0_._90_±_0_._02|58|198|73%|
|**0**_._**85**(used)|**0**_._**92**_±_**0**_._**02**|**62**|**210**|**59**%|
|0_._90|0_._92_±_0_._02|84|278|43%|
|0_._95|0_._91_±_0_._03|112|361|26%|



**Cross-distribution Lipschitz and contraction diagnostics.** Body §4 reports _L_<sup>ˆ(99%)</sup> _e ≈_ 1 _._ 4 and _L_ ˆ<sup>(99%)</sup> _R_ =0 _._ 891 on GSM8k scenarios. To verify Theorem 3’s contraction premise generalizes beyond the in-paper benchmark, we re-measure on three additional scenario distributions: ToolBench, _τ_ - bench retail, and NQ-Open. _Procedure._ For each distribution we sample 1000 in-distribution scenario pairs, compute (i) embedding distance ratio _∥e_ ( _s_ 1) _− e_ ( _s_ 2) _∥_ 2 _/d_ text( _s_ 1 _, s_ 2) and (ii) reranker output distance ratio over those pairs, then take the 99th percentile for both _L_<sup>ˆ</sup> _e_ and _L_<sup>ˆ</sup> _R_ . The margin ∆<sup>ˆ(5%)</sup> is the 5th percentile of top-1 vs. top-2 reranker score gaps; this is the empirical buffer that drives stable selection under stochastic perturbation. 

Table 13: Empirical Lipschitz and contraction diagnostics across distributions. _L_<sup>ˆ(99%)</sup> _e_ is the 99th percentile of _∥e_ ( _s_ 1) _−e_ ( _s_ 2) _∥_ 2 _/d_ text( _s_ 1 _, s_ 2) over 1000 in-distribution scenario pairs. _L_<sup>ˆ(99%)</sup> _R_ is the 99th percentile reranker-output contraction; Theorem 3 requires this _<_ 1. ∆<sup>ˆ(5%)</sup> is the 5th percentile top-1/top-2 reranker score margin. The premise holds with comfortable margin on GSM8k and ToolBench, narrowly on _τ_ -bench retail, and marginally on NQ-Open. On LiveBench, _L_<sup>ˆ(99%)</sup> _R_ =1 _._ 018 _exceeds_ the contraction threshold and the empirical margin collapses to 0 _._ 044; the theorem’s premise is not certified on this distribution and routing stability cannot be claimed under our current pipeline. The monotonic deterioration _L_<sup>ˆ</sup> _e ↑_ , _L_<sup>ˆ</sup> _R ↑_ , ∆<sup>ˆ</sup> _↓_ as scenario distributions grow more semantically dispersed indicates that the deployed embedding ( `jina-embeddings-v2-base-en` ) and reranker ( `llama-3.1-8b-instruct` ) approach their operating limits on highly heterogeneous open-domain tasks; stronger embeddings or task-specific reranker fine-tuning are the natural extensions for those regimes. 

|Distribution|# scenarios|ˆ_L_<sup>(99%)</sup><br>_e_|ˆ_L_<sup>(99%)</sup><br>_R_|ˆ∆<sup>(5%)</sup>|Theorem 3 premise|
|---|---|---|---|---|---|
|GSM8k (in-paper, body)|210|**1**_._**40**|**0**_._**891**|**0**_._**138**|holds|
|ToolBench scenarios|228|1_._49|0_._914|0_._116|holds|
|_τ_-bench retail|184|1_._61|0_._943|0_._086|holds, narrow margin|
|NQ-Open|156|1_._68|0_._971|0_._061|holds, marginal|
|LiveBench subset|132|1_._74|1_._018|0_._044|_not certifed_|



19 

## **G TextGrad Ablation and Sensitivity** 

We isolate TextGrad’s contribution by replacing it at the edge layer while keeping Algorithm 1’s clustering and conflict log intact. Setup: GSM8k, 5 IID clients, 5 seeds. The probe set used in TextGrad’s forward pass is constructed at each edge from public benchmark queries (GSM8k validation, BBH dev), _never_ from client data, and is fixed per edge for the federation – this keeps TextGrad’s optimization at the edge from reflecting client-specific information. 

Table 14: TextGrad vs. alternative edge summarization. _S_ =3 critique-update steps give the best accuracy/cost trade-off; further steps saturate. Single-shot summarize without critique costs 5 pts; no summarization costs 14 pts. 

|Edge summarization variant|Routing acc.|∆vs. TextGrad|Edge cost/round|
|---|---|---|---|
|**TextGrad (**_S_=3**steps, used)**|**0**_._**92**_±_**0**_._**02**|—|_∼_60s|
|TextGrad (_S_=1step)|0_._89_±_0_._02|_−_0_._03|_∼_22s|
|TextGrad (_S_=5steps)|0_._92_±_0_._02|0_._00|_∼_95s|
|Extractive summarization (centroid)|0_._85_±_0_._03|_−_0_._07|_<_1s|
|LLM single-shot summarize (no cri-|0_._87_±_0_._03|_−_0_._05|_∼_20s|
|tique)||||
|No summarization (concat all)|0_._78_±_0_._04|_−_0_._14|0s|



## **H Reranker-Bypass Diagnostic: Multi-Seed Verification** 

Body §5.1 reports that bypassing the LLM reranker on the fixed 500-query GSM8k diagnostic log drops routing accuracy 0 _._ 92 _→_ 0 _._ 49. To verify this is a stable component effect rather than a single-seed artifact, we re-ran the bypass at two additional seeds, holding the compendium and embedding model fixed. _Setup._ “Full pipeline” = retrieve top-5 via Jina embedding _→_ `llama-3.1-8b-instruct` reranker selects the most relevant _→_ planning step. “No reranker” = retrieve top-5 _→_ select the highest-cosine candidate directly _→_ planning step. Only the reranker step is toggled. 

Table 15: Reranker-bypass diagnostic on the fixed 500-query GSM8k routing log (3 seeds; same compendium and embedding model across seeds; only the reranker step toggled). The 0 _._ 42-point reranker contribution is consistent in sign and magnitude across seeds (Seed-123’s narrower ∆=0 _._ 37 corresponds to a higher bypass-baseline 0 _._ 53; the full pipeline accuracy variance is _±_ 0 _._ 015 across seeds, confirming a stable component effect). 

|Confguration|Seed 42|Seed 123|Seed 456|Mean_±_SD|
|---|---|---|---|---|
|Full pipeline (retrieve_→_rerank_→_plan)|0_._92|0_._90|0_._93|**0**_._**917**_±_**0**_._**015**|
|Bypass reranker (retrieve_→_top-1_→_plan)|0_._49|0_._53|0_._47|**0**_._**497**_±_**0**_._**031**|
|∆(reranker contribution)|0_._43|0_._37|0_._46|**0**_._**420**_±_**0**_._**046**|



## **I Real-API Failure Mode Decomposition** 

250 queries across six API categories, classified into: routing error (wrong API), API timeout ( _>_ 10s), rate limit (429), schema drift (unexpected response structure), auth/quota (401/403/quota exceeded), semantic miss (correct routing, wrong final answer). Routing errors and semantic misses are attributable to SYNAPSE; the rest are upstream-API properties. 

**Bootstrap confidence intervals.** The point estimates in body Tab. 5 are single-pass (no seed averaging) on a fixed test set. To characterize the test-set sampling variability, Tab. 16 reports 95% bootstrap CIs ( _B_ =1000 resamples per category, drawn with replacement from the per-category routing-decision logs). 

20 

Table 16: Real-API routing with 95% bootstrap confidence intervals ( _B_ =1000 resamples). SYNAPSE– Centralized intervals overlap on every category, consistent with the 0 _._ 07 federation–centralized gap not exceeding test-set sampling noise. Per-category SYNAPSE–Fed-ICL intervals partially overlap because per-category sample sizes are small ( _n_ =35–50); the _overall n_ =250 SYNAPSE–Fed-ICL intervals are disjoint ([0 _._ 67 _,_ 0 _._ 78] vs. [0 _._ 42 _,_ 0 _._ 54]), and the point-estimate gap is positive on every category (+0 _._ 20 to +0 _._ 28). 

|API category (_n_)|SYNAPSE[95% CI]|Centralized [95% CI]|Fed-ICL [95% CI]|
|---|---|---|---|
|Search (_n_=50)|0_._76[0_._63,0_._86]|0_._84[0_._71,0_._92]|0_._50[0_._37,0_._63]|
|Weather (_n_=45)|0_._80[0_._66,0_._89]|0_._84[0_._71,0_._92]|0_._53[0_._39,0_._67]|
|Knowledge (_n_=40)|0_._70[0_._55,0_._82]|0_._78[0_._62,0_._88]|0_._45[0_._31,0_._60]|
|Math (_n_=40)|0_._80[0_._65,0_._90]|0_._85[0_._71,0_._93]|0_._55[0_._40,0_._69]|
|Data (_n_=40)|0_._65[0_._50,0_._78]|0_._75[0_._60,0_._86]|0_._42[0_._29,0_._58]|
|Calendar (_n_=35)|0_._63[0_._46,0_._77]|0_._71[0_._55,0_._84]|0_._40[0_._26,0_._56]|
|**Overall (**_n_=250**)**|**0**_._**728**[**0**_._**67**,**0**_._**78**]|**0**_._**800**[**0**_._**75**,**0**_._**84**]|**0**_._**480**[**0**_._**42**,**0**_._**54**]|



Table 17: Real-API failure-mode decomposition across 250 queries on 6 ToolBench APIs. Routing errors account for 27 _._ 2% of all queries (consistent with Tab. 5’s 0 _._ 728 routing accuracy); the residual 14 _._ 8% failure mass is upstream-API in origin (schema drift, semantic miss, timeouts, rate limits, auth/quota). End-to-end success (0 _._ 580) is bounded above by routing accuracy (0 _._ 728) by construction; the 0 _._ 148 gap is the non-routing failure share. 

|API|N|Success|Route err.|Timeout|Rate lim.|Schema drift|Auth/quota|Sem. miss|
|---|---|---|---|---|---|---|---|---|
|Search (SerpAPI)|50|32|12|2|1|1|1|1|
|Weather (OWM)|45|31|9|1|1|1|0|2|
|Knowledge (Wiki)|40|21|12|0|0|4|0|3|
|Math (Wolfram)|40|28|8|0|0|1|1|2|
|Data (REST)|40|18|14|1|0|5|0|2|
|Calendar (GCal)|35|15|13|0|0|1|4|2|
|**Overall**|**250**|**145**|**68**|**4**|**2**|**13**|**6**|**12**|
|**% all**|—|58.0%|**27.2%**|1.6%|0.8%|5.2%|2.4%|4.8%|
|**% failures**|—|—|**64.8%**|3.8%|1.9%|12.4%|5.7%|11.4%|



## **J Communication Cost Analysis** 

### **J.1 Projected scaling to LiveMCPBench-class catalogs** 

LiveMCPBench [29] catalogs ( _∼_ 500 tools across _∼_ 70 MCP servers) are not directly evaluated. Using our existing scale measurements (Tab. 19): compendium size grows 62 _→_ 70 KB at 32 APIs; structural overhead is _∼_ 300 bytes per tool. A 500-tool compendium projects to _∼_ 200–250 KB total – still _∼_ 200 _×_ below FedLoRA r16. Retrieval latency: reranker processes top- _k_ = 5 independent of catalog size; ANN retrieval at 500 tools projects to _∼_ 500–550 ms vs. 484 ms at 228 scenarios, requiring relaxation of the 500 ms cap or progressive retrieval (HNSW + top- _k_ ). Where the projection is shaky: _L_<sup>ˆ(99%)</sup> _e ≈_ 1 _._ 4 was measured on GSM8k; embedding behavior on 500+ heterogeneous MCP tools requires re-measurement. Direct empirical evaluation on LiveMCPBench is the natural next step; the projection identifies bottlenecks rather than asserting they are negligible. 

Table 19: Scalability of SYNAPSE on GSM8k. Compendium size is bounded; latency holds because reranking processes only top-5 candidates. 

|Clients|Global|Macro|Spread|Comm.|Size|Scen.|Dedup|p95|
|---|---|---|---|---|---|---|---|---|
|50|0.94_±_0.01|0.92|0.12|267 KB|62 KB|210|59%|470 ms|
|100|0.94_±_0.01|0.92|0.14|533 KB|64 KB|214|63%|478 ms|
|200|0.94_±_0.01|0.92|0.16|1,067 KB|66 KB|220|67%|480 ms|
|500|0.93_±_0.02|0.91|0.20|2,667 KB|70 KB|228|70%|484 ms|



21 

Table 18: Per-client per-round communication on GSM8k. SYNAPSE numbers are measured from the actual federation. FedLoRA, FedQLoRA, and FedAvg numbers are _architectural lower bounds_ computed from rank, dtype, and parameter-count specs (no overhead, no compression); production implementations may reduce these further via sparse updates, quantization, or structured pruning. The reported _∼_ 10 _,_ 000 _×_ ratio against FedLoRA r16 and _∼_ 10<sup>7</sup> _×_ against full-weight FL are therefore gaps against bandwidth lower bounds rather than against optimized adapter baselines. FedLoRA additionally requires architectural compatibility across all clients, which SYNAPSE does not. 

|Method|Bytes/cli/round|Source|Frozen LLM?|Model-agnostic?|
|---|---|---|---|---|
|**SYNAPSE**|**5,334**|measured|**Yes**|**Yes**|
|Static-Global Compendium|1,067|measured|Yes|Yes|
|Fed-ICL (raw examples)|1,104|measured|Yes|Partial|
|FedQLoRA r16 int4|_∼_1_._3_×_10<sup>7</sup>|lower bound|No|No|
|FedLoRA r8 fp16|_∼_2_._6_×_10<sup>7</sup>|lower bound|No|No|
|FedLoRA r16 fp16|_∼_5_._2_×_10<sup>7</sup>|lower bound|No|No|
|FedAvg full fp32|6_._4_×_10<sup>10</sup>|lower bound|No|No|



## **K Benchmark-Breadth and Prompt-Transfer Results** 

This appendix supplies the supporting tables for the _Benchmark breadth_ and _Prompt transfer_ paragraphs in §5. 

**LiveBench (GPT-4o,** 3 **clients** _×_ 3 **rounds).** Federated underperforms centralized by 7–13 pts on three reasoning tasks but _outperforms_ by 4 pts on AMPS Hard (Tab. 20). The wider gap vs. the 5–6 pt gap at 32 APIs (Tab. 29) reflects the smaller federation scale used here. Both configurations use GPT-4o, so this does not establish cross-model transfer beyond GSM8k. 

**Prompt transfer (LLaMA-3.2-11B** _→_ **3B, distinct from compendium transfer).** Compendium held fixed; only optimized prompt structure migrates. Task-dependent: +0 _._ 15 on Multi-step Arithmetic, +0 _._ 03 on Object Counting, _−_ 0 _._ 08 on GSM8k (Tab. 21). Mixed signs indicate prompt transfer is not interchangeable with compendium transfer; the GSM8k regression does not contradict the _≤_ 2-pt cross-model loss in §5 (which transfers the compendium between LLM families with the federation pipeline held fixed). Treating the two mechanisms as interchangeable would obscure the practical recommendation: use compendium transfer when the federation can be re-run; prompt transfer only as a stop-gap. 

Table 20: LiveBench (GPT-4o). 

Table 21: Prompt transfer. 

|Category|Dataset|Cent.|Fed.|Task|3B own|3B from 11B|∆|
|---|---|---|---|---|---|---|---|
|Reasoning<br>Reasoning<br>Reasoning<br>Math|Spatial<br>Web of Lies<br>Zebra Puzzle<br>AMPS Hard|0_._53<br>0_._37<br>0_._33<br>0_._46|0_._40<br>0_._30<br>0_._27<br>0_._50|Obj. Counting<br>BBH Multi-step<br>GSM8k|0_._66<br>0_._51<br>0_._80|0_._69<br>0_._66<br>0_._72|+0_._03<br>+0_._15<br>_−_0_._08|



### **K.1 External benchmark:** _τ_ **-bench retail** 

**Setup.** _τ_ -bench retail [49]: 14 tools, 250 tasks averaging 4–6 turns each, GPT-4o user simulator, official database-state grader. We partition the 14 tools across 5 federated clients into categorycoherent subsets (account / orders / returns / catalog / escalation), evaluate SYNAPSE after 3 federated rounds, and compare against (i) centralized agent with full tool list, (ii) Fed-ICL with the same partitioning, (iii) local-only baseline. Inference: `llama-3.1-8b-instruct` ; 3 seeds. 

**Cross-model probe.** We test whether the cross-model transfer property documented on GSM8k (§5, _≈_ 2-pt loss within the LLaMA family, smaller for Mistral, gain for GPT-4o) replicates here. Holding the round-3 compendium and embedding model fixed (jina-embeddings-v2-base-en), we swap the inference LLM (Tab. 23). Same-family LLaMA-3.1 _→_ 3.2-3B: ∆= _−_ 0 _._ 022, matching the GSM8k gap exactly. Cross-family Mistral-7B: ∆= _−_ 0 _._ 009. GPT-4o: ∆=+0 _._ 085 – the typed compendium rides a stronger model upward, reaching _∼_ 90% of _τ_ -bench’s published GPT-4o ceiling. All four LLMs preserve the per-category ordering (catalog _>_ account _>_ escalation _>_ orders _>_ returns). 

22 

Table 22: _τ_ -bench retail headline: 250 tasks, 3 seeds. SYNAPSE task success 0 _._ 453 vs. Centralized 0 _._ 511 (gap 0 _._ 058, consistent with the 0 _._ 06 gap on real APIs in Tab. 5) vs. Fed-ICL 0 _._ 301 (advantage +0 _._ 152, consistent with Fed-ICL’s collapse on multi-turn tasks in Tab. 6). Per-category gap is tightly clustered (0 _._ 04–0 _._ 06 across all five categories: account 0 _._ 055, orders 0 _._ 061, returns 0 _._ 061, catalog 0 _._ 060, escalation 0 _._ 040); SYNAPSE–Fed-ICL gap is uniformly +0 _._ 15–+0 _._ 16. Routing errors dominate; execution errors bounded (5–9%). 

|Condition|Task success|Tool-call acc.|Avg. turns|Routing err.|Exec. err.|
|---|---|---|---|---|---|
|Centralized|0_._511_±_0_._017|0_._608_±_0_._012|5_._5|0_._392|0_._069|
|**SYNAPSE**|**0**_._**453**_±_**0**_._**023**|**0**_._**540**_±_**0**_._**018**|5_._8|0_._460|0_._055|
|Fed-ICL|0_._301_±_0_._027|0_._432_±_0_._032|6_._7|0_._568|0_._077|
|Local-only|0_._191_±_0_._017|0_._309_±_0_._023|7_._3|0_._691|0_._092|



Table 23: _τ_ -bench cross-model probe (250 tasks _×_ 3 seeds, same compendium). Adversarial / Byzantine evaluation on _τ_ -bench is not run; cross-model transfer on LiveBench and BFCL with their native protocols is future work. 

|Inference LLM|Task success|Tool-call acc.|Avg. turns|∆vs. LLaMA-3.1-8B|
|---|---|---|---|---|
|LLaMA-3.1-8B (main)|0_._453_±_0_._023|0_._631_±_0_._017|5_._4|—|
|LLaMA-3.2-3B|0_._431_±_0_._021|0_._614_±_0_._016|5_._7|_−_0_._022|
|Mistral-7B-Instruct|0_._444_±_0_._020|0_._624_±_0_._018|5_._5|_−_0_._009|
|GPT-4o|**0**_._**538**_±_**0**_._**018**|**0**_._**703**_±_**0**_._**014**|4_._8|+0_._085|



### **K.2 Second instantiation: typed retrieval-policy artifacts on NQ-Open** 

**Setup.** Natural Questions Open [23] with hybrid retrieval (BM25 + dense, top- _k_ = 5 Wikipedia passages) and llama-3.1-8b answer generation. _Data and clients:_ 5 _,_ 000 NQ-Open dev questions partitioned across 5 non-IID clients (1 _,_ 000 questions/client) by question-type (factoid-entity, factoiddate, list, definitional, multi-hop), inducing distributional skew on retrieval strategy. _Federation:_ 3 rounds, batch 3, 3 local steps/round; same hyperparameters as the tool-routing experiments (App. M). _Wikipedia retrieval corpus:_ 2018-12-20 dump (KILT-canonical version), shared across clients; clients differ in the _policy_ they learn over it, not the corpus itself. _Artifact construction:_ clients run their local NQ subset, log retrieval-then-answer trajectories, and extract typed retrieval-policy artifacts (query type _,_ retrieval strategy _,_ evidence pattern _,_ failure mode _,_ correction) from successful and failed trajectories; deduplication and edge merge follow Algorithm 1 unchanged. _Faithfulness evaluator:_ QAGS-style, llama-3.1-8b prompted with answer + retrieved passage to score support; offline against the same evaluator across all conditions. The schema-level merge operator (Algorithm 1) and DP guarantee (Theorem 1) apply unchanged; only the schema fields differ. Three metrics: Accuracy (Exact Match), Faithfulness, Evidence Recall@5. 

Table 24: Second instantiation on NQ-Open (3 seeds). SYNAPSE accuracy 0 _._ 724 vs. Centralized 0 _._ 756 (gap 0 _._ 032, tighter than the _τ_ -bench 0 _._ 058 – single-step RAG is less sensitive to federation constraints than multi-turn agent tasks). The typed-artifact protocol generalizes beyond tool-routing: same merge operator, schema validation, and DP guarantees apply with no algorithmic changes. Cross-model and cross-retriever transfer on NQ-Open are open; QAGS faithfulness is offline against a separate evaluator. 

|Setting|Accuracy (EM)|Faithfulness|Evidence Recall@5|
|---|---|---|---|
|Local-only RAG policy|0_._612_±_0_._024|0_._681_±_0_._021|0_._704_±_0_._026|
|Fed-ICL policy sharing|0_._661_±_0_._022|0_._708_±_0_._020|0_._733_±_0_._024|
|**SYNAPSE typed artifact**|**0**_._**724**_±_**0**_._**019**|**0**_._**771**_±_**0**_._**018**|**0**_._**801**_±_**0**_._**021**|
|Centralized oracle|0_._756_±_0_._017|0_._793_±_0_._016|0_._826_±_0_._019|



23 

Table 25: Status of every analytical claim. _Formal_ = theorem with proof. _Conditional_ = theorem under an unproven assumption that we characterize empirically. _Empirical_ = measured. _Computed_ = derived from architectural specs. 

|Claim / mechanism|Status|What is and is not established|
|---|---|---|
|Numeric-metadata DP (Thm. 1)|**Formal** ((_ε,_0)-DP per<br>round)|Holds for client-contributed numeric felds under user-<br>level adjacency with declared bounded sensitivity<br>(∆_m_=_N_max for counts,∆_m_=2for normalized fre-<br>quencies); per-user clipping at the client, central-DP<br>averaging and noising at a semi-honest edge. Sequen-<br>tial composition across felds and across_R_rounds (ba-<br>sic composition is tighter than advanced for_R≤_30).<br>Does_not_cover text felds.|
|Text-feld masking|**Heuristic**|Adaptive token-saliency masking. Empirically reduces<br>prompt-extraction AUROC (0_._62_→_0_._50at_λ_=1_._5).<br>No formal(_ε, δ_)-DP claim.|
|Retrieval<br>distortion<br>bound<br>(Thm. 2)|**Conditional theorem**|Holds _if_ the embedding _e_(_·_) is _Le_-Lipschitz under<br>_d_text. We do not prove this assumption holds; we<br>measure <sup>ˆ</sup>_L_<sup>(99%)</sup><br>_e_<br>_≈_1_._4for Jina embeddings.|
|Routing stability (Thm. 3)|**Conditional theorem**|Holds _if L <_ 1 in _ℓ_2 and score margin ∆_>_ 0.<br>Both empirically validated for the deployed reranker:<br>ˆ_L_<sup>(99%)</sup><br>_R_<br>=0_._891(_L<_1for100%of sampled pairs);<br>ˆ∆<sup>(5%) </sup>=0_._138(∆_>_0for100%of held-out queries).<br>Re-measure for other rerankers.|
|Communication reduction (_∼_<br>10<sup>4</sup>_×_vs FedLoRA)|**Computed**<br>(lower<br>bound)|SYNAPSE side measured. FedLoRA side computed<br>from rank-16 fp16 parameter count (architectural<br>lower bound).|
|Cross-model transfer (_≈_<br>2-pt<br>loss)|**Empirical**|GSM8k across 4 LLMs; replicated on_τ_-bench retail<br>(LLaMA-3.1_→_3.2-3B,∆=_−_0_._022).|



## **L Proofs** 

### **L.1 Status of analytical claims** 

### **L.2 Proof of Theorem 1** 

**Setup.** The Laplace mechanism with scale _b_ satisfies (∆ _/b,_ 0)-DP for any function with _ℓ_ 1-sensitivity at most ∆ [17]. Definition 1 declares finite ranges per numeric field, bounding ∆ _m_ by construction. We adopt _user-level_ neighboring datasets: _D, D_<sup>_′_</sup> differ by replacing the entire numeric record contributed by one user in round _r_ . The mechanism (App. F) operates in two stages: (stage 1) per-user clipping at the client bounds the user’s _ℓ_ 1 contribution at ∆<sup>(</sup> _m_<sup>_j_)per field; (stage 2) the edge aggregator</sup> computes the per-field average over _K_ clients and adds Laplace noise calibrated to the average’s sensitivity. 

**Per-field sensitivity under user-level adjacency.** With stage-1 clipping in place, replacing one user’s contribution changes exactly one client’s clipped value by at most ∆<sup>(</sup> _m_<sup>_j_)in</sup><sup>_ℓ_</sup> 1<sup>underthe</sup> single-user-per-client configuration (multi-user-per-client handling in App. F). Because that client’s clipped value contributes 1 _/K_ to the released average, the per-user _ℓ_ 1-sensitivity of _CE.M.m_<sup>(</sup><sup>_j_)</sup> = (1 _/K_ )<sup>�</sup> _k_<sup>clip</sup> _k_<sup>is ∆</sup> _m_<sup>(</sup><sup>_j_)</sup><sup>_/K_.Adding Laplace noise of scale ∆(</sup> _m_<sup>_j_)</sup><sup>_/_(</sup><sup>_Kε_(</sup><sup>_j_)) therefore yields per-field</sup> ( _ε_<sup>(</sup><sup>_j_)</sup> _,_ 0)-DP per round. 

**Concrete sensitivity values.** Per-scenario tool-usage counts are clipped at _N_ max per user-round, giving ∆ _m_ = _N_ max. For per-tool frequency vectors normalized to sum to one, replacing one user’s contribution can shift the distribution by up to _ℓ_ 1-distance 2 in the worst case (e.g., a user with all mass on tool _t_ replaced by a user with all mass on tool _t_<sup>_′_</sup> ); we therefore use ∆ _m_ =2 for normalized frequency vectors, not ∆ _m_ =1. Schema-declared field types determine which clipping rule applies; clipping occurs at the client before transmission to the edge. 

**Composition across fields (within a round).** A single user’s contribution can influence _multiple_ numeric fields simultaneously (e.g., usage count and frequency of the same tool). Parallel composition 

24 

therefore does _not_ apply: it requires disjoint partitions of the input dataset, not disjoint output fields. We use sequential composition across the _Kf_ numeric fields released per round (notation: _Kf_ for fields, _K_ for clients). Allocating per-field budget _ε_<sup>(</sup><sup>_j_)</sup> = _ε/Kf_ and summing field-wise guarantees yields per-round ( _ε,_ 0)-DP. Equivalently, one may release all _Kf_ fields under a single mechanism with joint _ℓ_ 1-sensitivity (<sup>�</sup> _j_<sup>∆</sup> _m_<sup>(</sup><sup>_j_))</sup><sup>_/K_and a single per-round budget</sup><sup>_ε_.</sup> 

**Composition across rounds.** Across _R_ federated rounds, basic sequential composition gives pure ( _ε_<sup>_′_</sup> _,_ 0)-DP with _ε_<sup>_′_</sup> = _Rε_ ; advanced composition gives ( _ε_<sup>_′_</sup> _, δ_<sup>_′_</sup> )-DP with _ε_<sup>_′_</sup> = �2 _R_ ln(1 _/δ_<sup>_′_</sup> ) _ε_ + _R ε_ ( _e_<sup>_ε_</sup> _−_ 1) at target _δ_<sup>_′_</sup> . For the small- _R_ regime in this paper ( _R ≤_ 30, _ε ≤_ 2), basic composition is strictly tighter and is what we report (Tab. 9); advanced composition is a strictly weaker but still valid bound. 

**Trust model.** The mechanism above assumes a semi-honest edge: the edge faithfully executes stages 1–2 but may attempt inference from the clipped client values it receives prior to noising. Theorem 1 is calibrated for this trust model. Secure aggregation [6] can be layered on the numeric path so that the edge observes only the noisy aggregate, weakening the trust assumption to the secure-aggregation ideal functionality. Theorem 1 is restricted to the numeric path; the text-field masking mechanism is heuristic and outside the formal claim. 

**Post-processing closure.** Operations applied to the noised release – typed merge clustering (Algorithm 1), redistribution to clients, and server-side broadcast – do not consume additional privacy budget: by the post-processing property of differential privacy [17, Prop. 2.1], any data-independent function of the ( _ε,_ 0)-DP output remains ( _ε,_ 0)-DP. The per-client averaging in stage 2 is part of the mechanism (it determines the sensitivity of the released statistic), not post-processing; post-processing applies only to operations on the already-noised release. The merge operator’s clustering step uses cosine similarity over text fields (which are not covered by Theorem 1) and noised numeric fields (which are post-processed); the resulting global numeric metadata inherits the per-round ( _ε,_ 0)-DP guarantee, with composition across rounds as stated above. 

### **L.3 Proof sketch of Theorem 2** 

By the assumed Lipschitz property of the embedding map, _∥e_ ( _u_ ) _− e_ (˜ _u_ ) _∥_ 2 _≤ Le · d_ text( _u,_ ˜ _u_ ) pointwise; taking expectation over the privacy transformation PrivTrans gives E _∥e_ ( _u_ ) _− e_ (˜ _u_ ) _∥_ 2 _≤ Le ·_ E[ _d_ text( _u,_ ˜ _u_ )] =: _δ_ priv. Cosine similarity is _L_ sim-Lipschitz in _∥· ∥_ 2 on the unit sphere (with _L_ sim = _√_ 2 in the worst case), so ��sim( _e_ ( _q_ ) _, e_ ( _u_ )) _−_ sim( _e_ ( _q_ ) _, e_ (˜ _u_ ))�� _≤ L_ sim _∥e_ ( _u_ ) _− e_ (˜ _u_ ) _∥_ 2 pointwise, and taking expectation gives E _|_ ∆sim _| ≤ L_ sim _δ_ priv. Markov’s inequality applied to the non-negative random variable _|_ ∆sim _|_ gives Pr( _|_ ∆sim _| > t_ ) _≤ L_ sim _δ_ priv _/t_ , yielding the highprobability statement. Both bounds are conditional on the two Lipschitz assumptions; we measure _L_ ˆ<sup>(99%)</sup> _e_ and the corresponding empirical bounds _δ_<sup>ˆ</sup> priv and _L_ sim _δ_<sup>ˆ</sup> priv in Tab. 26. 

Table 26: Empirical embedding distance (col. 3) vs. the Lipschitz upper bound _L_<sup>ˆ(99%)</sup> _e ·_ E[ _d_ text] (col. 4). The empirical expectation sits below the bound at all three masking levels, consistent with the bound being a worst-case upper envelope rather than an equality. Final column applies _L_ sim = _√_ 2 for the similarity-deviation bound (Theorem 2). 

|_λ_|E[_d_text]|ˆE_∥e_(_u_)_−e_(˜_u_)_∥_2|ˆ_L_<sup>(99%)</sup><br>_e_|_·_E[_d_text](bound)|_L_sim_·_bound|
|---|---|---|---|---|---|
|0_._5|0_._18|0_._21_±_0_._03||0_._24|0_._34|
|1_._0|0_._32|0_._37_±_0_._05||0_._44|0_._62|
|1_._5|0_._46|0_._51_±_0_._07||0_._65|0_._92|



### **L.4 Proof sketch of Theorem 3** 

**Existence of stationary distribution under contraction with bounded noise.** The iterate _sr_ +1 = _R_ ( _sr_ ) + _ηr_ +1 with _R_ an _L_ -contraction ( _L<_ 1) in _ℓ_ 2 and _ηr_ i.i.d. zero-mean with bounded variance _σ_<sup>2</sup> per coordinate forms a Markov process ( _not_ a martingale: the previous draft incorrectly invoked martingale convergence). By the standard contractive-random-iteration argument [14], this Markov chain admits a unique stationary distribution _π concentrated around_ the noise-free fixed point _s_<sup>_∗_</sup> of _R_ , with stationary variance bounded by _σ_<sup>2</sup> _/_ (1 _− L_<sup>2</sup> ) per coordinate. For nonlinear _R_ , zero-mean 

25 

noise does _not_ in general imply E _π_ [ _s_ ] = _s_<sup>_∗_</sup> exactly; we therefore claim concentration around (not exact centering on) the noise-free fixed point. Convergence is in distribution to _π_ , not almost-surely to a deterministic point: because the Laplace privacy noise has constant variance per round, _sr_ does not collapse to _s_<sup>_∗_</sup> but fluctuates around it indefinitely. 

**Top-1 selection is correct with high probability.** Let _t_<sup>_∗_</sup> be the unique noise-free top-scoring tool with margin ∆= _s_<sup>_∗_</sup> ( _t_<sup>_∗_</sup> ) _−_ max _t_ = _t_<sup>_∗_</sup> _s_<sup>_∗_</sup> ( _t_ ) _>_ 0. The top-1 selection arg max _t sr_ ( _t_ ) equals _t_<sup>_∗_</sup> unless some competitor’s noisy score exceeds _t_<sup>_∗_</sup> ’s noisy score. Under the contraction premise plus the assumption (Theorem 3, condition (iii)) that the propagated stationary score perturbations are sub-exponential, _s∞_ ( _t_<sup>_∗_</sup> ) _− s∞_ ( _t_ ) is a sub-exponential random variable with mean _≥_ ∆ and variance bounded by 2 _σ_<sup>2</sup> _/_ (1 _− L_<sup>2</sup> ). By a Chernoff-style concentration bound, Pr� _s∞_ ( _t_ ) _≥ s∞_ ( _t_<sup>_∗_</sup> )� _≤_ exp� _−_ ∆<sup>2</sup> (1 _− L_<sup>2</sup> ) _/_ (2 _σ_<sup>2</sup> )� for each competitor _t_ = _t_<sup>_∗_</sup> . Union bound over the _K −_ 1 competitors and the two-sided event gives the stated correctness probability 1 _−_ 2( _K −_ 1) exp� _−_ ∆<sup>2</sup> (1 _− L_<sup>2</sup> ) _/_ (2 _σ_<sup>2</sup> )�. The sub-exponential tail assumption is not proved for arbitrary nonlinear _R_ but is consistent with score perturbations driven by Laplace numeric noise composed with a Lipschitz reranker; we treat it as an assumption rather than a derived property. 

**What we revised relative to the earlier draft.** The earlier draft claimed almost-sure convergence to a deterministic point _s_<sup>_∗_</sup> via martingale convergence; this was incorrect because (i) _sr −R_ ( _sr−_ 1) is the noise term, not a martingale-difference of _sr_ , and (ii) constant-variance noise prevents almost-sure collapse. The corrected statement claims stable selection with high probability under the contraction premise, which is the operationally relevant guarantee and is consistent with the empirical observation that the top-1 selection is correct on 100% of held-out queries with ∆<sup>ˆ(5%)</sup> = 0 _._ 138 (Tab. 13). 

**Empirical characterization.** On 100 perturbation-pair samples (Gaussian _σ_ =0 _._ 05) over held-out GSM8k queries: _L_<sup>ˆ(99%)</sup> _R_ =0 _._ 891 (median 0 _._ 620), _L <_ 1 for 100% of pairs; ∆<sup>ˆ(5%)</sup> =0 _._ 138 (median 0 _._ 208), ∆ _>_ 0 for 100% of 100 queries. Tab. 13 (App. F) extends this to four additional distributions: ToolBench, _τ_ -bench retail, NQ-Open all hold (with NQ-Open marginal at _L_<sup>ˆ(99%)</sup> _R_ =0 _._ 971), while a LiveBench subset returns _L_<sup>ˆ(99%)</sup> _R_ =1 _._ 018 _>_ 1 and the contraction premise fails to certify – routing stability is therefore not claimed for that distribution under the deployed embedding+reranker pair. 

## **M Experimental Setup** 

SYNAPSE runs with three federated rounds and three default clients (adjustable via `–client-count` ). Retrieval: `jina-embeddings-v2-base-en` with top- _K_ =5 and cosine threshold _τ_ =0 _._ 85. LLM rerank: `llama-3.1-8b-instruct` (NVIDIA H200, batch 8–32, mixed precision, 500 ms cap). DP budget _ε ∈{_ 0 _._ 5 _,_ 1 _._ 0 _,_ 2 _._ 0 _}_ ; masking _λ ∈{_ 0 _._ 5 _,_ 1 _._ 0 _,_ 1 _._ 5 _}_ . TextGrad: edge, batch 3, 3 local optimization steps, summarization-based aggregation. Baselines: BM25 ( _k_ 1=1 _._ 5 _, b_ =0 _._ 75); Fed-ICL (8 exemplars/client). GSM8k: 5/8 clients with 50/30 examples each. Non-IID splits: shard by numeric answer range (GSM8k) or question length (BBH). Fig. 3 shows the inference pipeline. 

**Proxy tool-label construction (GSM8k/BBH).** The router does not see dataset provenance at inference time – routing decisions depend only on the user query and the retrieved compendium scenarios. Ground-truth tool labels for the proxy benchmarks are derived as follows. _GSM8k:_ every question is mapped to the `mathqa` tool family; gold answers are the dataset’s standard numeric solutions. _BBH Object Counting:_ mapped to `logicqa` (counting subroutine); gold answers are dataset labels. _BBH Multi-Step Arithmetic:_ mapped to `mathqa` (multi-step numeric); gold answers are dataset labels. The mapping is a single static function from dataset _→_ tool family, applied uniformly to all examples in that dataset; it is not learned, not query-dependent, and identical across all baselines (SYNAPSE, Fed-ICL, FedTextGrad, BM25, ReAct, Centralized). This makes the proxy benchmark a routing-recall test: given a query, can the system retrieve a scenario whose parent tool matches the dataset’s tool family? _Limitation._ Because the mapping is dataset-uniform, the proxy benchmark cannot test fine-grained cross-tool routing within a single dataset (e.g., MathQA vs. ScienceQA on a mixed-domain question); the multi-tool proxy reported in §5.2 (4 tool families: MathQA, SearchQA, CodeExec, LogicQA, _∼_ 250 queries/family) and ToolBench (Tab. 5) test that capability directly. 

**Sensitivity to** _τ_ **and embedding choice.** The cosine threshold _τ_ =0 _._ 85 and embedding model (Jina v2) are chosen by inspection of held-out scenario pairs and not separately tuned per benchmark. 

26 

Across the eight settings tested in Tab. 13, the empirical Lipschitz ratio _L_<sup>ˆ</sup> _e_ ranges 1 _._ 36–1 _._ 45 at _λ_ =1 _._ 0, suggesting modest sensitivity to distribution; cross-distribution Lipschitz exceeds 1 on LiveBench, where routing stability is not certified (§4). Systematic ablation of _τ_ and embedding choice (e.g., `bge-large` , `e5` ) on routing accuracy and dedup rate is left as future work; the conditional theorems (Thm. 2, Thm. 3) are stated against these constants and would require re-measurement under different choices. 

Table 27: 5-seed paired _t_ -tests on GSM8k (5 IID clients). Headline numbers in §5.1. 

|Method|Mean_±_SD|_p_-value|_d_|
|---|---|---|---|
|**SYNAPSE**|**0**_._**92**_±_**0**_._**02**|—|—|
|Centralized-<br>SYNAPSE|0_._92_±_0_._02|0_._31|0_._2|
|FedTextGrad|0_._90_±_0_._02|0_._04|0_._5|
|BM25|0_._83_±_0_._03|0_._003|1_._2|
|Fed-ICL|0_._79_±_0_._03|_<_0_._001|1_._5|
|ReAct|0_._64_±_0_._04|_<_0_._001|2_._0|
|Local-Only|0_._46_±_0_._05|_<_0_._001|3_._2|




![](P065_images/P065.pdf-0027-03.png)



![](P065_images/P065.pdf-0027-04.png)



![](P065_images/P065.pdf-0027-05.png)



![](P065_images/P065.pdf-0027-06.png)



![](P065_images/P065.pdf-0027-07.png)



![](P065_images/P065.pdf-0027-08.png)

### Figure analysis

**Purpose:** Figure 3 illustrates the paper’s inference retrieval and routing pipeline for selecting a relevant scenario/tool from a global compendium and using it to construct the prompt sent to an LLM.

**Main components and labels observed:**
- A green **Query** box initiates the workflow.
- The query branches into a **Query Scenario** representation and into a prompt-construction block.
- A routing stage labeled **Task/Dataset Specific Routing** receives the query scenario.
- A dashed lower retrieval module contains two sequential stages:
  - **Embedding Search**
  - **LLM Reranking**
- The reranking output feeds a central structured prompt/tool block containing:
  - **User Data**
  - **Problem Examples**
  - **System Prompts**
  - **Optimal Candidate Tool**
- This structured content flows to a right-side block labeled **Augmented Prompt**, with a lower sub-block labeled **Injected Noise**.
- The augmented prompt is sent to an **LLM**, which returns **Response + Rationale** to the user/query side.

**Information flow:**
1. The incoming query is represented as a query scenario.
2. The query scenario is routed through task/dataset-specific routing.
3. Retrieval proceeds by embedding search over the compendium, followed by LLM reranking.
4. The selected scenario/tool information populates a typed prompt context containing user data, examples, system prompts, and the optimal candidate tool.
5. Optional noise can be injected into the augmented prompt.
6. The LLM produces the final response and rationale.

**Direct observations vs. interpretation:**
- Directly observed: the diagram shows a retrieval module with embedding search followed by LLM reranking, then prompt augmentation and LLM response generation.
- Interpreted from the caption and surrounding text: the retrieval target is the global compendium, and the selected scenario’s typed `P` field supplies per-tool prompt material; optional injected noise corresponds to differentially private perturbation of numeric metadata.

**Connection to surrounding text:**
The figure supports the surrounding discussion of routing-recall and sensitivity to embedding choices. It visually clarifies that routing depends on retrieval and reranking from a shared compendium, while execution uses the selected tool-specific prompt fields. This contextualizes the nearby routing-accuracy tables by showing the mechanism whose performance those evaluations assess.


Figure 3: Inference retrieval and routing pipeline. Query _→_ embedding-based retrieval against the global compendium _→_ LLM reranking selects the best scenario and parent tool _→_ augmented prompt assembled from typed _P_ field with optional DP noise on numeric metadata _→_ LLM produces response. Routing pipeline depends only on the global compendium; execution path uses per-tool prompts in _P_ . 

Table 28: IID vs. non-IID routing accuracy (sharded by numeric answer range / question length, 5 seeds). non-IID degrades _≤_ 4 pts across all three benchmarks. 

|Dataset|IID|non-IID|∆|
|---|---|---|---|
|GSM8k|0_._96|0_._92|_−_0_._04|
|BBH Object Counting|0_._99|0_._98|_−_0_._01|
|BBH Multi-Step Arith.|0_._94|0_._92|_−_0_._02|



27 

## **N Long-Horizon Controlled Simulation: Full Protocol** 

This appendix documents the protocol for the long-horizon controlled simulation reported in §5. The protocol was registered before the run; numbers populate App. O. 

**Federation topology.** _N_ =100 clients organized into 5 simulated organizations of 20 clients each, with non-IID query distributions reflecting enterprise specialization: _Org A_ (search/knowledge, MSMARCO-derived traces), _Org B_ (math/symbolic, GSM8k+MATH), _Org C_ (operations, MultiWOZ-derived dialogue), _Org D_ (commerce, Stripe sandbox + retail Q&A), _Org E_ (mixed, balanced across 32 APIs; cross-validation organization). Each client within an organization sees a non-IID slice of its organization’s distribution. _M_ =5 edge aggregators (one per org) running Llama-3.1-8B for TextGrad summarization. Single central server applies the typed merge operator (Algorithm 1) over the 5 edge compendiums and broadcasts back. One round every _∼_ 11 hours; 30 rounds over 14 days. _∼_ 21 _,_ 000 queries total ( _∼_ 1 _,_ 500/day; _∼_ 200/client). 

**Tool inventory.** 32 APIs across 8 categories (Search _×_ 4, Weather _×_ 3, Knowledge _×_ 5, Math/Symbolic _×_ 4, Data/REST _×_ 6, Calendar/Files _×_ 4, Payments _×_ 3, Communications _×_ 3). Real APIs used where free-tier access permits (SerpAPI, OpenWeatherMap, Wikipedia, Wolfram, GitHub, etc.); sandbox or deterministic mocks elsewhere. 

**Drift schedule.** 8 drift events at known timestamps spanning 5 types: 1 schema-rename (Day 3, SerpAPI `organic_results` _→_ `web_results` ), 2 schema-add (Day 4 OpenWeatherMap `air_quality_index` , Day 9 REST Countries `regional_blocs` ), 1 schema-restructure (Day 5 GitHub `repository.owner` flattened), 2 rate-limit (Day 7 Wikipedia 200 _→_ 50 req/min, Day 11 Stripe 100 _→_ 25/sec), 2 endpoint-path (Day 8 Wolfram `/v1/result` _→_ `/v2/query` , Day 12 Notion). Pre-drift accuracy is computed in _±_ 24h windows; post-drift at _T_ +1, _T_ +3, _T_ +10 rounds; “recovered” = within 0 _._ 02 of pre-drift baseline. 

**Staleness protocol.** At end of round 20, save snapshot _Cg_<sup>(20)</sup> and serve queries against the live API surface for 7 additional days without aggregation. Cadences run in parallel: every-round (baseline), every-5, every-10, frozen. Accuracy measured at days _{_ 1 _,_ 3 _,_ 5 _,_ 7 _}_ post-freeze on a held-out 1 _,_ 000query test set proportional to organizational mix. 

**Compute and scope.** 4 _×_ H200 GPUs; _∼_ 2 weeks wall-clock for the run plus _∼_ 1 week for analysis. The simulation can demonstrate routing under enlarged tool-list size and longer federation, conflict-log behavior under author-scheduled drift, the cadence-accuracy Pareto, and cross-organizational transfer. It cannot demonstrate production-scale traffic (1 _,_ 500/day is below enterprise loads), jurisdictionspecific regulatory compliance (HIPAA/GDPR characterization is structural, not certified), or adaptive Byzantine attacks beyond those in App. E. 

## **O Long-Horizon Controlled Simulation: Detailed Results** 

This appendix reports the full numbers behind the simulation summarized in §5: 100 clients across 5 simulated organizations, 32 APIs, 30 federated rounds over 14 days, _∼_ 21 _,_ 000 total queries. Numbers are reported to two decimal places for accuracy and rounded to whole units for size and latency. 

### **O.1 Headline metrics across rounds** 

Table 29: Headline metrics for the long-horizon controlled simulation. Routing accuracy converges by Round 10 and gains a further 2 pts by Round 30, with the federation–centralized gap stable at 5–6 pts. Compendium grows from 28 KB to 96 KB while client–round communication stays under 8 KB. The setup is a controlled simulation: inventory, organizational partitioning, and drift schedule are author-defined. 

|Metric|Round 1|Round 10|Round 30|Centralized|
|---|---|---|---|---|
|Routing accuracy (overall,32APIs)|0_._66|0_._77|0_._79|0_._84|
|End-to-end success (full pipeline)|0_._53|0_._62|0_._67|0_._71|
|Compendium size (KB)|28|67|96|—|
|Communication (KB / client / round)|4_._4|6_._7|7_._4|—|
|_p_95 retrieval+rerank latency (ms)|468|492|509|—|



28 

### **O.2 Per-category end to end success at Round** 30 

Table 30: Per-category end to end success at Round 30. Spread across categories (0 _._ 70–0 _._ 83, range 0 _._ 13) is driven by within-category tool ambiguity: Math/Symbolic and Weather have strong domain markers while Communications and Data/REST contain APIs with overlapping send-message and CRUD scenarios. The overall centralized oracle baseline is reported in Tab. 29; per-category centralized breakdowns were not separately measured in this run.The routing-error subset is reported in Tab. 32 

|Category|SYNAPSE(Round30)|
|---|---|
|Search (4APIs)|0_._79|
|Weather (3APIs)|0_._81|
|Knowledge (5APIs)|0_._72|
|Math/Symbolic (4APIs)|0_._83|
|Data/REST (6APIs)|0_._70|
|Calendar/Files (4APIs)|0_._72|
|Payments (3APIs)|0_._78|
|Communications (3APIs)|0_._70|
|**Overall (all**32**APIs)**|**0**_._**79**|



**System metrics across rounds** (matching Tab. 29): the compendium grows from 28 KB at Round 1 to 96 KB at Round 30 with deduplication rate increasing as scenario count saturates. End-to-end success (0 _._ 53 _→_ 0 _._ 62 _→_ 0 _._ 67) sits below routing accuracy because real-API execution adds additional failure modes; the gap (routing _−_ E2E) of _∼_ 12 pts at Round 30 is consistent with the small-scale ToolBench experiment (Tab. 5). The federation–centralized gap is stable across rounds at +0 _._ 053, +0 _._ 057, +0 _._ 052 (Rounds 1, 10, 30), evaluated by rerunning held-out queries under a centralized configuration with full conflict-log access. 

**Where the** 5 **-pt federation–centralized gap comes from.** The gap is stable rather than closing, which is itself diagnostic: it indicates a structural source rather than a convergence-rate effect. We hypothesize three mechanisms each of which the centralized oracle can exploit but federated SYNAPSE cannot, and offer the available evidence for each. 

- **Cross-cluster reconciliation (likely dominant).** The merge operator (Algorithm 1) handles conflicts _within_ a cosine cluster but not _across_ clusters: two scenarios with cos _< τ_ are kept as separate entries even when they describe the same routing decision in different terms. Centralized routing sees both during retrieval and can use whichever fits better. _Supporting evidence:_ percategory accuracy in Tab. 30 is most depressed in categories with high within-category paraphrasing (Communications, Calendar/Files, Knowledge: all _≤_ 0 _._ 72) and least depressed in categories where scenarios are more lexically distinctive (Math/Symbolic, Weather: both _≥_ 0 _._ 81). The category-level spread of 0 _._ 13 tracks paraphrasing density, not tool count. 

- **Lossy text summarization at edge layer.** TextGrad summarization (§3.1) compresses multiple client scenarios into a single summary; the centralized oracle has access to all client scenarios un-summarized. The TextGrad ablation in Tab. 14 shows that summarization choice matters in the controlled regime (0 _._ 92 for TextGrad vs. 0 _._ 85 for extractive concatenation), but does not by itself isolate the deployment-gap component because the controlled-regime baseline is centralized-withTextGrad rather than centralized-without-summarization. The cleanest test of this hypothesis would be a deployment-scale run with extractive concatenation in place of TextGrad, holding all other factors constant; we have not run that experiment. We list this hypothesis here because TextGrad’s per-cluster compression is a structural lossy step that the centralized oracle skips entirely. 

- **Cluster-representative selection in conflict cases.** When line 13 of Algorithm 1 marks a cluster conflicted, the centroid scenario is retained and the dissenter is logged for next-round Precautions. The centralized oracle evaluates queries against both scenarios directly. The conflict log eventually surfaces dissenters as Precautions, but the within-round opportunity cost is real. 

**What we do not yet know.** We cannot quantitatively partition the 5-pt gap among (i)–(iii) without a second deployment-scale run that systematically ablates each mechanism. Within-paper data is consistent with hypothesis (i) being the largest component (the per-category pattern above), but the available _τ_ -sensitivity table (Tab. 12) addresses a different question – it shows that lowering _τ_ 

29 

from 0 _._ 85 over-merges genuinely-distinct scenarios and _hurts_ routing accuracy (0 _._ 92 _→_ 0 _._ 87) – and so does not by itself isolate the cross-cluster reconciliation effect. A targeted ablation that varies cross-cluster merge behavior while holding within-cluster behavior fixed is required, and is left for follow-up work. We flag this as an open empirical question rather than a closed finding. 

### **O.3 Staleness across aggregation cadences** 

Table 31: Compendium staleness over 7 days under varying aggregation cadences. Headline: every5-rounds loses 4 pts at Day 7 vs. every-round baseline (0 _._ 744 vs. 0 _._ 785) for 5 _×_ communication savings – a favorable trade-off in this simulation; how this generalizes to real-world traffic is open. Every-round baseline degrades only 1 _._ 1 pts over 7 days, confirming the federated update loop tracks drift effectively. Frozen-at-round-20 degrades 17 _._ 5 pts (0 _._ 776 _→_ 0 _._ 601) – the strongest evidence that compendium updates are doing real work, not absorbed by reranker robustness alone. Std across 3 seeds. 

|Aggregation cadence|Day1|Day3|Day5|Day7|∆1_→_7|Comm. saved|
|---|---|---|---|---|---|---|
|Every round (baseline)|0_._796_±_0_._014|0_._792_±_0_._015|0_._789_±_0_._016|0_._785_±_0_._017|_−_0_._011|0_×_|
|Every5rounds|0_._789_±_0_._015|0_._774_±_0_._017|0_._758_±_0_._018|0_._744_±_0_._019|_−_0_._045|5_×_|
|Every10rounds|0_._782_±_0_._016|0_._756_±_0_._018|0_._729_±_0_._020|0_._704_±_0_._022|_−_0_._078|10_×_|
|Frozen at round20|0_._776_±_0_._017|0_._718_±_0_._021|0_._653_±_0_._026|0_._601_±_0_._030|_−_0_._175|_∞_|



**Failure decomposition by Day 7.** The shift in failure budget across cadences reveals _which_ mechanism fails as the compendium ages. Tab. 32 decomposes 1 _−_ accuracy into five sources at Day 7. 

Table 32: Failure decomposition at Day 7 by aggregation cadence. Schema/API drift grows fastest with stale compendiums (7 _._ 4% _→_ 20 _._ 7%, a 2 _._ 8 _×_ increase) – consistent with the schema-evolution mechanism in App. N. Routing error grows nearly 2 _×_ (11 _._ 8% _→_ 21 _._ 4%). Timeout/rate-limit is roughly constant (4 _._ 2–4 _._ 9%) because those failures are API-side and independent of routing. The frozen-at-round-20 regime fails primarily through schema drift, not reranker fragility, supporting the design decision that compendium freshness is a first-class concern. **Note on metric reconciliation.** Tab. 31 tracks routing accuracy; Tab. 32 decomposes all end-to-end failure modes (routing and non-routing). Total end-to-end error (30.6% every-round) exceeds routing failure (1 _−_ 0.785 = 21.5%) because non-routing failures (schema drift, semantic miss, timeout, rate-limit) stack on top of routing errors. The routing-error subcomponent (11.8%) reflects SYNAPSE-attributable misrouting; the remaining 9.7 pts are upstream-API and coverage failures outside SYNAPSE’s control. 

|Failure source|Every-round|Every-5|Every-10|Frozen|
|---|---|---|---|---|
|Routing error|11_._8%|13_._1%|15_._6%|21_._4%|
|Schema/API drift|7_._4%|9_._8%|13_._2%|20_._7%|
|Semantic miss|5_._9%|6_._6%|7_._1%|8_._3%|
|Timeout / rate-limit|4_._2%|4_._4%|4_._6%|4_._9%|
|Other / unclassifed|1_._3%|1_._5%|1_._8%|2_._0%|
|**Total error**|**30**_._**6**%|**35**_._**4**%|**42**_._**3**%|**57**_._**3**%|



### **O.4 Cross-organizational transfer** 

**Robustness of the transfer claim.** The result above uses a category-coherent organizational partitioning of the 32-tool inventory. We address whether the +0 _._ 10 mean ∆ depends on this specific partitioning in four ways. 

**(i) Within-experiment evidence.** The per-org ∆ ranges from +0 _._ 07 to +0 _._ 13 across the five organizations – a 0 _._ 06 spread with std. 0 _._ 020. All five orgs show positive ∆ with the smallest gain (+0 _._ 07) approximately three standard deviations above zero. If the result were specific to a particular partitioning, we would expect at least one organization to show near-zero ∆. 

**(ii) Mechanism-level prediction.** Hypothesis (i) of the gap-diagnosis paragraph above predicts that organizations with higher within-category paraphrasing should gain more from cross-org Precautions. 

30 

Table 33: Cross-organizational transfer. Org A: search-and-knowledge; Org B: math-and-symbolic; Org C: operations; Org D: commerce; Org E: mixed. Each organization’s 20 clients specialize in _∼_ 40% of the 32-tool inventory. Full federation outperforms within-org federation by +0 _._ 10 on average (range +0 _._ 07 to +0 _._ 13 across orgs, std. 0 _._ 020). Operations (Org C) gains most (+0 _._ 13): its native calendar/files/communications categories show high within-category paraphrasing in Tab. 30 ( _≤_ 0 _._ 72), and cross-org Precautions disambiguate the internal overlap. Search-and-Knowledge (Org A) gains least (+0 _._ 07): its native subset already covers a broadly-shared category, so cross-org Precautions add less marginal information. The 0 _._ 06 spread across orgs is itself evidence that the transfer effect is not knife-edge to a single partitioning – see robustness discussion below. 

|Setting|Org A|Org B|Org C|Org D|Org E|Mean|
|---|---|---|---|---|---|---|
|Local-only (per-org)|0_._47|0_._55|0_._45|0_._46|0_._51|0_._49|
|Within-org federation|0_._69|0_._72|0_._63|0_._67|0_._70|0_._68|
|Full federation (all5)|0_._76|0_._81|0_._76|0_._78|0_._80|0_._78|
|Centralized oracle|0_._81|0_._85|0_._80|0_._83|0_._84|0_._83|
|∆(Full – Within-org)|+0_._07|+0_._09|+0_._13|+0_._11|+0_._10|+**0**_._**10**|



The data fit this prediction: Operations (calendar/files/communications, _≤_ 0 _._ 72 within-category accuracy) gains +0 _._ 13; Commerce +0 _._ 11; Search-and-Knowledge +0 _._ 07. A null effect would have ∆ uncorrelated with the paraphrasing pattern of each org’s native subset. 

**(iii) Randomized-partitioning robustness check.** We re-ran the cross-org evaluation under a _random_ partitioning that deliberately breaks the category-coherent assumption: each of the 32 APIs is randomly assigned to one of 5 orgs (with overlap), producing organizations with no native-category coherence. Setup: 50 clients (10 per org, vs. 20 in the main run), 5 rounds (vs. 30), 50 queries/client, 3 seeds; we re-ran the category-coherent regime at the same scale as a paired control. Tab. 34 reports both regimes. 

Table 34: Cross-org ∆ under category-coherent vs. random partitioning (50 clients, 5 rounds, 3 seeds, 50 queries/client). Both partitionings yield positive cross-org transfer across all 5 orgs. Random partitioning’s mean ∆ (+0 _._ 067) is _∼_ 3 _._ 4 pts smaller than category-coherent (+0 _._ 101), consistent with hypothesis (ii) above: random subsets contain less internal paraphrasing than category-coherent ones, so cross-org Precautions add less marginal value. The category-coherent control at this smaller scale (+0 _._ 101) reproduces the full-scale result (+0 _._ 10 in Tab. 33), confirming the small-scale protocol is methodologically sound. Random and coherent runs use independent seeds, query samples, and partitioning RNG state. 

|Regime||Local-only|Within-org|Full fed.|Centralized|∆mean|∆range|
|---|---|---|---|---|---|---|---|
|Category-coherent|(con-|0_._49|0_._68|0_._78|0_._83|+0_._101|[+0_._07_,_+0_._13]|
|trol, small-scale)||||||||
|Random partitioning||0_._51|0_._66|0_._73|0_._80|+0_._067|[+0_._04_,_+0_._09]|



The cross-organizational transfer effect is real but partitioning-dependent in magnitude. The mechanism story holds: more paraphrasing within native subsets _⇒_ larger gain from cross-org Precautions. The transfer claim survives the most direct robustness check available: random partitioning still produces positive ∆ across all 5 orgs, with smallest gain +0 _._ 04 (above zero by _∼_ 1 _._ 3 _σ_ at this sample size). 

**(iv) What remains untested.** Adversarial-overlap partitionings (where org native subsets deliberately overlap), partitionings with extreme inventory-size skew (one org dominant), and full-scale (30-round, 100-client) random-partitioning runs are not reported here; the small-scale random run above is the strongest evidence available within the submission’s scope. Conditional on (i)–(iii), we read the cross-org claim as evidence-supported under both category-coherent and random partitionings, with magnitude varying by partitioning regime. 

31 

