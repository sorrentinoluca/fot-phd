# **FORGE: Self-Evolving Agent Memory With No Weight Updates via Population Broadcast** 

Igor Bogdanov igorbogdanov@cmail.carleton.ca Carleton University Ottawa, Ontario, Canada 

Chung-Horng Lung chlung@sce.carleton.ca Carleton University Ottawa, Ontario, Canada 

Thomas Kunz tkunz@sce.carleton.ca Carleton University Ottawa, Ontario, Canada 

Adrian Taylor Adrian.Taylor@forces.gc.ca Defence R&D Canada Ottawa, Ontario, Canada 

Jie Gao jie.gao6@carleton.ca Carleton University Ottawa, Ontario, Canada 

Marzia Zaman Marzia@cistel.com Cistel Technology Ottawa, Ontario, Canada 

## **Abstract** 

**decision processes** ; **Reinforcement learning** ; **Planning and scheduling** ; **Natural language processing** . 

Can LLM agents improve decision-making through self-generated memory without gradient updates? We propose FORGE (FailureOptimized Reflective Graduation and Evolution), a staged, populationbased protocol that evolves prompt-injected natural-language memory for hierarchical ReAct agents. FORGE wraps a Reflexion-style inner loop, where a dedicated reflection agent (using the same underlying LLM, no distillation from a stronger model) converts failed trajectories into reusable knowledge artifacts: textual heuristics (Rules), few-shot demonstrations (Examples), or both (Mixed), with an outer loop that propagates the best-performing instance’s memory to the population between stages and freezes converged instances via a graduation criterion. We evaluate on CybORG CAGE-2, a stochastic network-defense POMDP at a 30-step horizon against the B_line attacker, where all four tested LLM families (Gemini2.5-Flash-Lite, Grok-4-Fast, Llama-4-Maverick, Qwen3-235B) exhibit strongly negative, heavy-tailed zero-shot rewards. Compared against both a zero-shot baseline and a Reflexion baseline (isolated single-stream learning), FORGE improves average evaluation return by 1.7-7.7× over zero-shot and by 29-72% over Reflexion in all 12 model-representation conditions, reducing major-failure rates (below −100) to as low as ∼1%. We find that (1) population broadcast is the critical mechanism, with a no-graduation ablation confirming that broadcast carries the performance gains while graduation primarily saves compute; (2) Examples achieves the strongest returns for three of four models, while Rules offers the best cost-reliability profile with ∼40% fewer tokens; and (3) weaker baseline models benefit disproportionately, suggesting FORGE may mitigate capability gaps rather than amplify strong models. All evidence is confined to CAGE-2 B_line; cross-family findings are directional evidence. 

## **Keywords** 

LLM agents, self-improvement, memory evolution, populationbased training, prompt-only learning, cyber defense, POMDP 

#### **ACM Reference Format:** 

Igor Bogdanov, Chung-Horng Lung, Thomas Kunz, Jie Gao, Adrian Taylor, and Marzia Zaman. 2026. FORGE: Self-Evolving Agent Memory With No Weight Updates via Population Broadcast. In _ACM Conference on AI and Agentic Systems (ACM CAIS ’26), May 26–29, 2026, San Jose, CA, USA._ ACM, New York, NY, USA, 19 pages. https://doi.org/10.1145/3786335.3813155 

## **1 Introduction** 

Large language models (LLMs) can act as general-purpose reasoning engines for sequential decision-making with ability to self-reflect and improve when embedded in agentic scaffolds such as ReAct [23], Reflexion [15], and Voyager [20]. Yet most such agents remain single-episode systems: they reason and act within an episode, but retain little actionable knowledge that reliably improves future behavior. This gap is especially problematic in stochastic, partially observable environments where policies must be discovered through repeated interactions rather than specified in advance. 

Since fine-tuning is often infeasible and expensive, prompt-only self-improvement offers a promising alternative. However, three critical questions remain for applying this to stochastic, long-horizon sequential decision-making: (1) **What should be remembered?** Existing approaches typically commit to a single representation (heuristics/rules or behavior examples) without controlled comparison. (2) **How should memory propagate?** Unlike serial reflection, population-based training suggests parallel exploration could accelerate learning, but its prompt-only analogue is underexplored. (3) **Is the training method transferable across LLMs?** Whether gradient-free evolution yields consistent gains across diverse model families remains an open empirical question. 

## **CCS Concepts** 

• **Computing methodologies** → **Artificial intelligence** ; **Multiagent systems** ; **Intelligent agents** ; **Partially-observable Markov** 

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for third-party components of this work must be honored. For all other uses, contact the owner/author(s). _ACM CAIS ’26, San Jose, CA, USA_ 

We address these questions via FORGE, a **staged population protocol** where _𝑁_ hierarchical ReAct agents evolve prompt-injected memory over _𝑆_ stages. We evaluate four model families (Gemini2.5-Flash-Lite, Grok-4-Fast, Llama-4-Maverick, Qwen3-235B) under three conditions: zero-shot, Reflexion [15] (isolated single-stream learning), and FORGE (Reflexion plus population broadcast and 

© 2026 Copyright held by the owner/author(s). ACM ISBN 979-8-4007-2415-2/26/05 https://doi.org/10.1145/3786335.3813155 

ACM CAIS ’26, May 26–29, 2026, San Jose, CA, USA 

Bogdanov et al. 

graduation), comparing three memory representations across multiple independent sessions per model. 

We study this challenge in CybORG CAGE-2 [8], a stochastic cyber-defense POMDP that combines four properties making it a demanding stress test for prompt-only adaptation: (1) a long horizon (30 steps) with partial observability, where LLM-based defense remains underexplored; (2) near-catastrophic zero-shot LLM performance, so memory-based learning is genuinely necessary; (3) scalar per-step reward with no natural-language feedback, requiring the agent to infer from numerical signals alone what went wrong; and (4) a practically important domain with a public leaderboard (DRL top score −3 _._ 47 [8]) providing absolute reference points. In this setting, a ReAct agent based on four contemporary LLM families without any environment knowledge displays deeply negative zero-shot returns. All evidence in this paper is confined to CAGE-2 B_line red agent at a 30-step horizon; generalization to other attacker types and environments remains future work. 

_Contributions._ Our main contributions are: (1) **A populationbased, gradient-free self-improvement protocol, FORGE** . The protocol evolves prompt-injected natural-language memory through staged learning with champion broadcast and graduation-based early stopping. We compare three conditions – zero-shot, Reflexion (isolated reflection, no broadcast), and FORGE – and observe 1.7–7.7× improvements in average returns over zero-shot, with the single best observed checkpoint return reaching −3 _._ 60 (against a maximum of 0 and a DRL top score of −3 _._ 47); (2) **A controlled comparison of memory representations in a stochastic longhorizon environment.** Rules, Examples, and Mixed representations reach comparable final performance in the replicated Gemini study, with Examples achieving the best return (−24 _._ 5) and Rules offering the best cost-reliability profile with higher graduation rates and ∼40% fewer tokens than Examples; (3) **Evidence that population-level transfer is critical.** Champion broadcast improves performance by 29–72% over the Reflexion baseline in all 12 model-representation conditions and reduces catastrophic-failure rates to as low as ∼1%; and (4) **Directional cross-family evidence.** FORGE improves over both zero-shot and Reflexion for all four tested model families, with disproportionately higher gains on weaker baselines. 

## **2 Related Work** 

_Prompt-Only Self-Improvement & Baseline Selection._ A growing body of literature explores replacing weight updates with linguistic feedback. Reflexion [15] stores critiques after failures, while Self-Refine [9] applies iterative critiques within a single response. CLIN [10] extends prompt-only self-improvement to cross-episode causal-memory abstractions. Recent work on context evolution and test-time adaptation highlights that unconstrained self-edits can accumulate errors, motivating mechanisms that select and propagate only robust improvements across trials [17, 25]. TextGrad [24] takes a complementary approach, performing gradient descent over text representations using LLM-generated feedback as the optimization signal. Voyager [20] and ExpeL [26] learn reusable skills or experience from successful episodes. Among these, Reflexion is the directly comparable baseline in our setting: it requires only a scalar success/failure indicator, applies failure-triggered verbal memory 

updates, and needs no task-specific engineering to operate with CAGE-2’s per-step reward signal. The remaining methods would each require nontrivial adaptation: Voyager and ExpeL depend on reusable successes, scarce at CAGE-2 initialization where zero-shot performance is near-catastrophic; CLIN is built for structured textsimulator feedback rather than scalar per-step reward; Dynamic Cheatsheet [17] and ACE [25] use update regimes that differ from scalar per-step cyber-defense reward; and TextGrad would require an auxiliary evaluator to convert environment reward into the textual optimization signal it expects (it is the most tractable future comparison). We therefore adopt Reflexion as the primary baseline and compare it against FORGE under identical model, memory representation, and training budget. 

_Memory Representations._ How to efficiently represent the knowledge that an agent should remember still remains an open question. Systems like AutoGuide [5], ExpeL [26], and Voyager [20] demonstrate the value of learning guidelines, experience, or skills represented by executable code. Complementary systems treat memory as a managed context resource or workflow artifact, e.g., MemGPT [12], Agent Workflow Memory [21], and Dynamic Cheatsheet [17], but they rarely provide controlled comparisons of representation choices under identical training dynamics. While prior work compares instructions vs. exemplars in single-step tasks [19] or even sequential decision-making [14], we extend artifact efficiency comparison to adversarial POMDPs, evaluating Rules, Examples, and Mixed representations under identical staged learning conditions. 

_Population-Based Selection._ Population-Based Training (PBT) [7] is a canonical strategy for parallel exploration. Unlike classic hyperparameter PBT, our population mechanism selects among textual artifacts that shape the agent’s policy via prompting. Whereas prompt-evolution methods typically optimize a single monolithic prompt and focus on single-step tasks [4, 6, 22], we evolve structured lists of rules or examples, tied to specific failure modes, enabling targeted repairs without damaging unrelated competencies. 

_Cyber Defense Agents._ CybORG [16] and the CAGE-2 challenge [8] provide a rigorous SOTA testbed currently dominated by reinforcement learning (RL) methods. Prior LLM-based cyber defenders are often evaluated either as fixed-prompt policies in CAGE-2 [11] or in later CybORG variants (e.g., CAGE 4) as components within hybrid multi-agent systems [3]. Our work demonstrates that LLM agents can improve their defense policies online without gradient updates. 

_Positioning._ Our work combines three separate directions: (1) gradient-free self-improvement, (2) memory representation, and (3) population-based selection into a coherent protocol. Unlike memory-centric architectures that store complete records of agentic behavior [13], FORGE performs explicit trajectory analysis to update structured knowledge artifacts for specialized sub-agents, aligning with modular agent design patterns [18]. Our approach builds a Reflexion-inspired [15] inner loop on ReAct [23] scaffolding and wraps it with population-level selection and broadcast for hierarchical agents in an adversarial, stochastic cyber-defense POMDP. 

ACM CAIS ’26, May 26–29, 2026, San Jose, CA, USA 

FORGE: Self-Evolving Agent Memory With No Weight Updates 


![](P014_images/P014.pdf-0003-02.png)

### Figure analysis

The figure is a system overview for FORGE, showing how a hierarchical ReAct agent interacts with a CAGE-2 cyber-defense environment and how failure-triggered reflection updates memory without weight updates.

**Left panel: Hierarchical reasoning agent defending the network**

- The left side is labeled **“Hierarchical Reasoning Agent — Defends the Network.”**
- It shows several memory and context blocks feeding a central **Planner - ReAct Agent**:
  - **Knowledge** contains three sections:
    - **Reflection Knowledge**: described as rules or heuristics.
    - **Reflection Examples**: described as specific examples.
    - **Persistent Knowledge - Static**.
  - **Definition** contains:
    - **Core - Agent Definition - System Prompt**.
    - **Initial Prompt - User Prompt**.
  - **Network Status** contains host status categories such as changed, baseline, and unknown, plus actions applied to a host and time-of-update information.
  - **History** stores actions taken at previous steps and analyses.
- The central planner has tools corresponding to two sub-agents:
  - **Action Chooser - ReAct Agent**, with no tools and access to knowledge and definition.
  - **Analyst - ReAct Agent**, with programmatic tools and access to knowledge and definition.
- The **CAGE-2 Environment** sits below the planner and receives an **Action** from the agent. It returns step observations, labeled with notation such as **O\_{t+1}**, and history/context information such as **H\_{t+1}**.
- Direct visual observation: blue arrows indicate the operational control and information flow among memory, prompts, network status, planner, analyst, action chooser, history, and environment.
- Interpretation: the left panel represents dynamic memory injection into a hierarchical policy: the planner uses persistent definitions, evolving reflective knowledge, examples, current network state, and history to choose cyber-defense actions.

**Right panel: Reflection agent triggered by a reward below threshold**

- The right side is labeled **“Reflection Agent — Triggered by a Reward Below Threshold.”**
- It contains stacked trajectory records:
  - **Planner - Trajectory**.
  - **Analyst - Trajectory**.
  - **Action Chooser - Trajectory**.
- The action chooser trajectory is described as the full ReAct loop up to the step that triggered the continual learning loop.
- Green dotted arrows labeled **Logs** and **Environment State** flow from the acting agent side into the trajectory/reflection side.
- Two reflection-related ReAct agents appear:
  - **Exemplifier - ReAct Agent**, with self-reflection tools plus knowledge and definition; its output is routed to **Reflection Examples - Specific Examples**.
  - **Reflector - ReAct Agent**, with self-reflection tools plus knowledge and definition; its output is routed to **Reflection Knowledge - Rules, Heuristics**.
- Direct visual observation: the exemplifier is associated with a green output path back to the Reflection Examples memory block, while the reflector is associated with a purple output path back to the Reflection Knowledge memory block.
- Interpretation: failed or low-reward episodes are converted into reusable artifacts, either examples or general rules, which are then injected back into the agent memory for later decisions.

**Cross-panel information flow**

- The operational loop runs from memory and prompts into the planner, then into the environment through selected actions, and back through observations and history.
- When performance falls below a reward threshold, trajectory logs and environment state are passed to the reflection subsystem.
- The reflection subsystem analyzes the trajectories and writes updated artifacts back into the knowledge memory:
  - Rules/heuristics update **Reflection Knowledge**.
  - Specific cases update **Reflection Examples**.
- This visual structure supports the method section’s description of FORGE as combining: hierarchical ReAct action selection, failure-triggered Reflexion-style memory updates, and representation-specific artifacts such as rules and examples.

**Connection to the surrounding text**

- The surrounding paper text states that Figure 1 illustrates the hierarchical agent architecture and the inner Reflexion-style learning loop. The diagram directly matches this description: the left panel shows the planner, analyst, action chooser, dynamic memory, network status, history, and CAGE-2 environment; the right panel shows the reflector/exemplifier agents triggered by low reward.
- The figure also supports Algorithm 1: after a reward below threshold, a snapshot of trajectories, memory, metadata, and environment state is analyzed by an update agent, and the resulting edits are applied back to memory.
- The figure visually emphasizes the paper’s key claim that the same LLM-based system can improve policy behavior by editing prompt-injected memory rather than by updating model weights.


**Figure 1: System Overview. (Left) Hierarchical ReAct agent with dynamic memory injection. (Right) Reflexion learning loop: upon a reward below threshold, a dedicated Reflector or Exemplifier agent analyzes the full trajectory and synthesizes knowledge artifacts that are injected back into the agent’s memory.** 

## **3 Method** 

We introduce FORGE (Failure-Optimized Reflective Graduation and Evolution), a multi-stage population protocol for evolving promptinjected memory without weight updates. The method has three components: (1) a hierarchical ReAct agent with dynamic and persistent memory sections (Figure 1, left); (2) an inner Reflexion-style learning loop [15] that converts failures into reusable knowledge artifacts (Figure 1, right); and (3) an outer population protocol that runs parallel instances in stages and propagates the best-discovered memory via champion broadcast (Figure 2). A critical design constraint is that **no external oracle or stronger model is used** : the same LLM generates actions and synthesizes memory. 

### **Algorithm 1** Failure-Triggered Reflexion Loop 

- **Require:** Agent instance with memory _𝑀𝑖_ , attempts _𝑘𝐴_ , failure trigger _𝜏_ , representation ∈{Rules _,_ Examples _,_ Mixed} 

- 1: **for** _𝑎_ = 1 to _𝑘𝐴_ **do** 2: Track per-step reward _𝑟𝑠𝑡𝑒𝑝_ 3: Run episode with memory _𝑀𝑖_ 4: **if** ∃ _𝑠𝑡𝑒𝑝_ such that _𝑟𝑠𝑡𝑒𝑝 < 𝜏_ **then** 5: Abort; snapshot ← trajectories, _𝑀𝑖_ , metadata, environment state 6: Δ ← UpdateMemory(snapshot _,_ representation) _⊲_ Reflector / Exemplifier 

- 7: Apply edits: _𝑀𝑖_ ← Apply( _𝑀𝑖,_ Δ) 8: **end if** 9: **end for** 

- 10: **return** Updated memory _𝑀𝑖_ 

## **3.1 Agent Architecture: Hierarchical ReAct with Dynamic Memory Injection** 

Figure 1 (left) illustrates the hierarchical agent architecture. At each environment step, a top-level **Planner** selects the final defense action while delegating two sub-tasks to on-demand (implemented as tools) ReAct sub-agents: **Analyst** (interprets host-level observations) and **ActionChooser** (ranks valid actions with justification). All agents use the same underlying LLMs, and differ only in their role-specific system prompts and their injected memory. 

The FORGE protocol runs _𝑁_ copies of this agent hierarchy in parallel, each called an _instance_ . Instance _𝑖_ ∈{1 _, ..., 𝑁_ } maintains persistent and dynamic memory _𝑀𝑖_ = ( _𝑀𝑖_<sup>_𝑃, 𝑀_</sup> _𝑖_<sup>_𝐴, 𝑀_</sup> _𝑖_<sup>_𝐶_) for the Plan-</sup> ner, Analyst, and ActionChooser. Persistent memory is instructions and specific knowledge set by the user; in this setup, only the ActionChooser and the learning agents (Reflector, Exemplifier) receive the environment action reference table, while the Planner has no pre-supplied action knowledge so that any strategic competence it acquires is attributable to learned artifacts. Dynamic memory is initially empty and accumulates knowledge artifacts generated by the 

learning agents during training. The _representation_ of these artifacts is the central experimental variable, taking one of three forms: (a) **Rules** : ordered lists of conditional heuristics; (b) **Examples** : structured demonstrations that mimic ReAct agent interaction (thought, tool, observation, answer) [23]; or (c) **Mixed** : both rules and examples generated separately over the same context. Appendix C provides verbatim examples of generated Rules and Examples artifacts. 

Memory is stored on disk and re-injected into each agent’s system prompt at every attempt, with a fixed capacity to prevent unbounded context growth. Sub-agents are instantiated on-demand within the Planner’s reasoning loop with their own prompts and memory. 

## **3.2 Inner Loop: Failure-Triggered Reflexion** 

Figure 1 (right) illustrates the learning mechanism. Within each episode, the agent executes actions until completion or until a perstep reward _𝑟𝑠𝑡𝑒𝑝_ drops below a failure threshold _𝜏_ . Upon failure, the 

ACM CAIS ’26, May 26–29, 2026, San Jose, CA, USA 

Bogdanov et al. 


![](P014_images/P014.pdf-0004-02.png)

### Figure analysis

The figure explains the operational structure of the FORGE protocol described in the surrounding text, separating the outer population-level training protocol from the inner per-instance learning loop.

**Left panel: outer FORGE protocol.**

- The left side depicts multiple parallel **agent instances**, each represented by an “Ai” icon and a horizontal trajectory through training.
- Training is divided into sequential stages labeled approximately as **Stage 1, k_A attempts**, **Stage 2, k_A**, **Stages 2 to N−1, k_A**, and **Stage N, k_A**, followed by **Final Evaluation**.
- Vertical black lines mark **checkpoint / inter-stage evaluation** points.
- The legend indicates several outcome categories:
  - **Graduation Threshold Hit – Frozen** is shown with a blue marker.
  - **Best Stage Award – Champion Donor** is shown with a green marker.
  - **Underperformed – Abandoned** is shown with a magenta square.
  - Solid colored arrows indicate **after-stage champion memory** transfer.
  - Dashed gray lines indicate **learned knowledge** trajectories or inactive/abandoned continuation.
- A labeled box states **“Inner Loop, see Right”**, indicating that each agent instance undergoes the inner learning procedure shown in the right panel.
- The visual flow shows that after a stage, a selected champion’s memory can be **cloned** into other instances for the next stage, while underperforming instances may be abandoned.
- The final evaluation includes at least two groups: **Graduated Frozen** agents and **Last Stage Clones**, consistent with the surrounding description of champion selection, graduation, and broadcast across stages.

**Right panel: inner learning loop.**

- The right panel is a flow diagram for one **instance inner learning loop**.
- The process starts with an agent instance entering **Attempt to Pass**, labeled as a **Hierarchical Agent**.
- If the attempt succeeds, the flow proceeds through **Successful Attempt** toward **End of Stage**.
- If a step reward falls **below the step reward threshold**, the trajectory is routed to **Knowledge Generation**, labeled **Exemplifier / Reflector / Both**.
- After knowledge generation, the loop returns to **Start Over**, indicating that failed attempts are converted into new memory artifacts and the episode restarts.
- This directly corresponds to the surrounding text’s description of failure-triggered Reflexion: when a per-step reward drops below threshold, the attempt is aborted, the trajectory is analyzed, and a rule, example, or mixed artifact is added to memory before restarting.

**Key observations and interpretation.**

- Directly observed: the protocol has two nested levels: an outer multi-instance, multi-stage selection mechanism and an inner failure-triggered learning loop.
- Directly observed: successful or high-performing agents can become frozen graduates or champion donors, while underperformers are abandoned.
- Directly observed: memory transfer is explicitly represented by arrows labeled as champion memory and clone operations.
- Interpretation: the outer loop introduces selection pressure by propagating memory from better-performing instances, addressing the instability of isolated Reflexion described in the text.
- Interpretation: the inner loop implements the paper’s memory-artifact generation mechanism, where failures produce learned rules, examples, or both depending on the experimental condition.


**Figure 2: Protocol Details. (Left) The FORGE protocol involves parallel execution, champion selection, graduation and broadcast between stages. (Right) Inner learning loop inside each attempt.** 

episode is **aborted** immediately and the full trajectory is captured. A dedicated learning agent using the same underlying LLM, **Reflector** (for Rules) or **Exemplifier** (for Examples), analyzes the trajectory up to the failure point together with the environment state and synthesizes a knowledge artifact: either a conditional heuristic (Rules) or a structured interaction demonstration (Examples). In the Mixed condition, both agents generate artifacts over the same context. The generated artifact is appended to the agent’s memory, and the episode restarts from step 0. This abort-and-restart cycle converts failures into a structured learning sequence, iterating up to _𝑘𝐴_ attempts per stage. Algorithm 1 formalizes this loop. 

This loop constitutes a complete single-stream learning system implementing the Reflexion pattern [15]. When run in isolation, each instance independently accumulates memory from its own trajectories without any cross-instance knowledge transfer. However, single-stream reflection in stochastic, partially observable environments lacks a selection pressure that distinguishes genuine policy improvement from noise: isolated instances can accumulate counterproductive artifacts that degrade performance below the zero-shot starting point, and even successful instances produce high-variance policies. A population-based protocol that runs multiple instances in parallel and propagates only the best-performing memory addresses this limitation structurally. 

## **3.3 Outer Loop: The FORGE Protocol** 

To address the instability of isolated Reflexion, we propose FORGE, a **multi-stage, population-based protocol** that wraps the Reflexion inner loop (Algorithm 1) with three additional mechanisms: _staged training_ that creates periodic synchronization points, _champion broadcast_ that propagates the best-discovered memory to the population, and _graduation_ that freezes strong solutions and conserves compute. Figure 2 illustrates the protocol and Algorithm 2 formalizes it. 

FORGE adapts the Population-Based Training (PBT) framework [7] from weight space to prompt space. The PBT _exploit_ step maps to champion broadcast, which copies the best instance’s memory 

### **Algorithm 2** FORGE: Staged Population Memory Training 

|**Re**|**quire:** Instances<br>_𝑁_, stages _𝑆_, attempts _𝑘𝐴_, graduation|
|---|---|
||threshold _𝜃_, failure trigger _𝜏_, representation, condition<br>∈{FORGE_,_Reflexion}<br>|
|1:|Initialize dynamic memory_𝑀𝑖_←∅for_𝑖_∈{1_, . . . , 𝑁_}|
|2:|Initialize graduated set_𝐺_←∅|
|3:|**for**_𝑠_=1 to_𝑆_**do**<br>_⊲_Outer loop: staged knowledge transfer|
|4:|Initialize each instance_𝑖_in a uniquely seeded CAGE-2 en-<br>vironment with_𝑀𝑖_|
|5:|Initialize attempt graduated set_𝐻_←∅|
|6:|Initialize checkpoint Return_𝑅𝑖_=0|
|7:|**for**instance_𝑖_∉_𝐺_**in parallel do**<br>_⊲_Concurrent|
||Independent Instances<br>|
|8:|_𝑀𝑖_←ReflexionLoop(_𝑀𝑖,𝑘𝐴,𝜏,_representation)<br>_⊲_<br>Algorithm 1|
|9:|_𝑅𝑖_←Checkpoint(_𝑀𝑖_)<br>_⊲_frozen evaluation, no|
||learning|
|10:|**end for**|
|11:|_𝐻_←{_𝑖_∉_𝐺_|_𝑅𝑖> 𝜃_}<br>_⊲_new graduates|
|12:|Freeze memories of_𝐻_;_𝐺_←_𝐺_∪_𝐻_|
|13:|**if** condition = FORGE and|{_𝑖_∉_𝐺_}| _>_0**then**|
|14:|_𝑖_<sup>∗</sup>←arg max_𝑖_∉_𝐺𝑅𝑖_<br>_⊲_champion selection|
|15:|**for**instance_𝑖_∉_𝐺_**do**|
|16:|_𝑀𝑖_←_𝑀𝑖_<sup>∗</sup><br>_⊲_broadcast: full memory replacement|
|17:|**end for**|
|18:|**end if**|
|19:|**end for**|
|20:|**return**Final evaluation of all_𝑁_frozen instances.|



artifacts to all active instances; the _explore_ step maps to the Reflexion inner loop, which independently evolves each instance’s memory through failure-triggered reflection within the next stage. Two structural differences follow from operating on discrete textual artifacts rather than continuous weights: (1) broadcast performs full replacement rather than interpolation, because merging two natural-language rule sets would require a conflict-resolution 

ACM CAIS ’26, May 26–29, 2026, San Jose, CA, USA 

FORGE: Self-Evolving Agent Memory With No Weight Updates 

**Table 1: Experiment Count and Evaluated Episodes by Model and Condition** 

||**Zero-Shot**|**Refexi**|**on (in**|**stances)**|**FOR**|**GE (sessi**|**ons)**|**FORGE**|**w/o grad**|**(sessions)**|
|---|---|---|---|---|---|---|---|---|---|---|
|**Model**|**Episodes**|**Rules**|**Ex**|**Mix**|**Rules**|**Ex**|**Mix**|**Rules**|**Ex**|**Mix**|
|Gemini-2.5-Flash-Lite|70|70|50|50|7 (70)|7 (70)|7 (140)|2 (40)|2 (40)|2 (40)|
|Grok-4-Fast|100|30|30|30|3 (60)|3 (60)|3 (60)|2 (40)|2 (40)|2 (40)|
|Llama-4-Maverick|50|70|30|30|3 (110)|3 (60)|3 (60)|2 (40)|2 (40)|2 (40)|
|Qwen3-235B|50|30|30|50|4 (80)|3 (60)|3 (60)|2 (40)|2 (40)|2 (40)|



mechanism that is itself unreliable, and (2) the explore step is not a random perturbation but a semantically grounded reflection on new failure trajectories. 

_Staged Training._ Training is organized into _𝑆_ sequential stages. At the beginning of each stage, every active instance is initialized in a uniquely seeded environment with its current memory _𝑀𝑖_ . Within the stage, each instance independently executes the Reflexion loop (Algorithm 1) for up to _𝑘𝐴_ attempts. Stages serve as synchronization points: all instances complete their inner-loop attempts before any between-stage mechanism (checkpoint, graduation, broadcast) is applied. 

_Champion Broadcast._ After each stage, a frozen checkpoint evaluation produces a return _𝑅𝑖_ for each active instance. The instance with the highest checkpoint return among active (non-graduated) instances is designated the _champion_ , and its complete memory state replaces the memory of every other active instance. This is a destructive operation: each recipient discards its own accumulated artifacts and begins the next stage from the champion’s memory. The design prioritizes convergence toward the best-discovered strategy over preserving population diversity. 

_Graduation and Early Stopping._ Instances whose checkpoint return exceeds a graduation threshold _𝜃_ are **graduated** : their memory is frozen and they are excluded from all subsequent stages. Graduation prevents regression by locking strong solutions before the next broadcast cycle can overwrite them, and conserves compute by excluding converged instances from further training. 

When broadcast is disabled (condition = Reflexion), the protocol reduces to parallel independent Reflexion, the baseline against which FORGE is compared. After all stages complete, every instance (graduated or not) undergoes a final frozen evaluation. 

## **4 Experimental Setup** 

_Evaluation Task and Environment: CybORG CAGE-2._ We evaluate FORGE on CybORG CAGE-2 [8, 16], a cybersecurity gym environment modelled as POMDP where a blue defender protects a 13-host enterprise network against an automated red attacker over a 30-step horizon (canonical setting also includes 50- and 100-step episodes). CAGE-2 leaderboard is dominated by RL methods; public reference points against the _B_line_ attacker over 30 steps include CardiffUni PPO −3 _._ 47 (DRL top score) [2], rule-based heuristic −58 _._ 83, random action −154 _._ 06, and no-action (sleeping) −218 _._ 65 [8]. We define two failure severity levels anchored to this scale: return _<_ −100 (major failure, between the heuristic and random baselines) and return _<_ −150 (catastrophic failure, near-random performance). Conversely, returns above −50 represent significant improvement 

**Table 2: Models, FORGE Configuration, and Metrics** 

|**Category**|**Confguration / Description**|
|---|---|
|**Models**|Gemini-2.5-Flash-Lite (Primary), Grok-4-Fast, Llama-4-<br>Maverick, Qwen3-235B|
|**LLM Confg**|**Agent (Planner/Analyst/ActionChooser)**: temp=0,<br>max_tokens=10000|
||**Learning**<br>**(Refector/Exemplifer)**:<br>temp=0,<br>max_tokens=20000|
|**Conditions**|**Zero-shot**: Empty memory, no training<br>**Refexion**: Isolated single-stream refection, no broad-<br>cast|
||**FORGE**: Refexion + champion broadcast + graduation<br>**FORGE w/o grad**: Refexion + champion broadcast, no<br>graduation|
|**Repre-**<br>**sentations**|Rules, Examples, or Mixed memory|
|**Protocol**|_𝑁_=10 parallel instances,_𝑆_=6 stages,_𝑘𝐴_=3 attempts|
|**Params**|per stage|
|**Hyperpara-**<br>**meters**|Failure trigger_𝜏_= −1_._1 (per-step reward); Graduation<br>_𝜃_=−15 (episode return)|
|**Metrics**|**Evaluation Return**: Mean return (_𝑅_= <sup>�</sup>_𝑟𝑠𝑡𝑒𝑝_, closer<br>to 0 is better)|
||**Graduation Rate**: % of instances reaching _𝜃_= −15<br>during checkpoint|
||**Token Cost**: Total prompt + completion tokens (training<br>+ eval)|
||**Tail Risk**: Frequency of catastrophic failures (return<br>_<_ −100)|



over the rule-based heuristic (−58 _._ 83), approaching the regime of competitive RL policies. 

_Failure Trigger Sensitivity._ The failure trigger _𝜏_ = −1 _._ 1 is derived from the environment’s reward structure rather than tuned as a hyperparameter. Additionally, analysis of per-step penalties across 540 zero-shot episodes (Appendix D) reveals that penalties fall into distinct groups: _Restore_ actions always cost −1 _._ 0 and are legitimate defensive operations, not failures; small failures cost −1 _._ 1 or −1 _._ 2; moderate failures −2 _._ 0 to −3 _._ 2; and severe failures −11 to −14 (with no values between −3 _._ 3 and −10 _._ 9). Since the trigger fires when _𝑟𝑠𝑡𝑒𝑝 < 𝜏_ , setting _𝜏_ = −1 _._ 1 is the smallest threshold that excludes legitimate Restore penalties (exactly −1 _._ 0) while capturing real failures with 100% precision (zero false positives) at 74% recall (7,346 of 9,926 true triggers). A sensitivity sweep over _𝜏_ ∈{−1 _._ 1 _,_ −2 _._ 0 _,_ −3 _._ 0 _,_ −11 _._ 0}, corresponding to the natural penalty groups, is reported alongside the main results. We set graduation 

ACM CAIS ’26, May 26–29, 2026, San Jose, CA, USA 

Bogdanov et al. 

**Table 3: Combined results: mean return** ± **SD by model, representation, and condition.** ↑ **= improvement,** ↓ **= degradation over the reference column. Bold marks the best result per model across all FORGE variants.** 

||||**Refexio**|**n**|**FOR**|**GE**||**FO**|**RGE w**|**/o grad**||
|---|---|---|---|---|---|---|---|---|---|---|---|
|**Model**|**Zero-Shot **|**Representation**|**Mean**±**SD**|Δ**ZS**|**Mean**±**SD**|Δ**ZS**|Δ**Ref**|**Mean**±**SD**|Δ**ZS**|Δ**Ref**|Δ**FORGE**|
|Gemini||Rules|−62_._7±60_._5|↑**67%**|−30_._6±37_._0|↑**84%**|↑**51%**|−33_._1±26_._5|↑**83%**|↑**47%**|↓8%|
||−189_._6±53_._9|Examples|−78_._9±60_._4|↑**58%**|−24_._5±21_._1|↑**87%**|↑**69%**|−37_._7±27_._2|↑**80%**|↑**52%**|↓54%|
|||Mixed|−81_._9±74_._6|↑**57%**|−32_._2±28_._1|↑**83%**|↑**61%**|−32_._7±30_._7|↑**83%**|↑**60%**|↓1%|
|Grok||Rules|−79_._9±62_._6|↓37%|−33_._7±26_._1|↑**42%**|↑**58%**|−24_._5±15_._1|↑**58%**|↑**69%**|↑**27%**|
||−58_._4±55_._2|Examples|−64_._8±52_._4|↓11%|−42_._7±43_._3|↑**27%**|↑**34%**|−14_._0±2_._0|↑**76%**|↑**78%**|↑**67%**|
|||Mixed|−114_._4±76_._8|↓96%|−42_._2±36_._9|↑**28%**|↑**63%**|−23_._2±19_._4|↑**60%**|↑**80%**|↑**45%**|
|Llama||Rules|−101_._4±61_._0|↑**10%**|−72_._0±46_._6|↑**36%**|↑**29%**|−76_._7±54_._7|↑**32%**|↑**24%**|↓7%|
||−113_._1±81_._5|Examples|−53_._9±59_._7|↑**52%**|−28_._3±15_._7|↑**75%**|↑**48%**|−42_._2±35_._3|↑**63%**|↑**22%**|↓49%|
|||Mixed|−44_._2±40_._6|↑**61%**|−29_._6±25_._6|↑**74%**|↑**33%**|−23_._8±9_._3|↑**79%**|↑**46%**|↑**19%**|
|Qwen||Rules|−88_._4±83_._5|↑**14%**|−25_._2±21_._0|↑**76%**|↑**72%**|−17_._3±2_._6|↑**83%**|↑**80%**|↑**31%**|
||−103_._3±87_._3|Examples|−57_._6±69_._5|↑**44%**|−24_._3±35_._8|↑**77%**|↑**58%**|−15_._5±2_._3|↑**85%**|↑**73%**|↑**36%**|
|||Mixed|−80_._4±89_._4|↑**22%**|−29_._3±20_._4|↑**72%**|↑**64%**|−17_._9±2_._8|↑**83%**|↑**78%**|↑**39%**|



threshold _𝜃_ = −15, which corresponds to roughly 10× improvement over random agent performance [8]. 

_Evaluation Modes._ To explicitly distinguish selection from reporting, we define two evaluation modes: (1) **Checkpoint** : a frozen single-episode probe used during training to determine graduation and champion selection and (2) **Post-Session Evaluation** : a separate measurement of frozen instances, obtained after full FORGE session completion. Gemini-2.5-Flash-Lite serves as the primary study model with 7 independent FORGE sessions per representation followed by 1-2 evaluations per instance. Other models receive 3–4 FORGE sessions per representation as directional cross-family probes (Table 1) followed by at least 2 evaluations per instance. The no-graduation ablation receives 2 sessions per model per representation across all four families followed by at least 2 evaluations per instance. 

_Baselines and Conditions._ All results are compared against two baselines. The _zero-shot baseline_ evaluates the agent with empty memory and no training, measuring the total improvement attributable to memory evolution. The _Reflexion baseline_ runs the same failure-triggered reflection loop (Algorithm 1) but without champion broadcast: each instance evolves its own memory in isolation. Comparing FORGE against zero-shot quantifies the overall gain; comparing against Reflexion isolates the specific contribution of population-level knowledge transfer. We evaluate four LLM families under four conditions (Table 2): zero-shot, Reflexion, FORGE (Reflexion plus broadcast and graduation, Algorithm 2), and FORGE without graduation (broadcast only). Each trained condition is crossed with three memory representations (Rules, Examples, Mixed). Table 1 breaks down session and episode counts per condition. 

## **5 Results** 

We compare four conditions (zero-shot, Reflexion, FORGE, and FORGE without graduation) across four model families and three memory representations (Table 3). Results are organized around five questions: (1) the magnitude of improvement over zero-shot and Reflexion baselines across model families, (2) the comparative efficacy 

of memory representations (Rules vs. Examples vs. Mixed), (3) token cost and graduation dynamics, (4) cross-model generalization patterns, and (5) the contribution of population broadcast versus isolated Reflexion. We additionally report a no-graduation ablation that isolates the contribution of graduation from that of broadcast. A sensitivity sweep over the failure trigger threshold _𝜏_ probes whether the chosen value (−1 _._ 1) is optimal or whether restricting reflection to more severe failures changes convergence behavior. We report **post-session evaluation** metrics unless explicitly referring to **checkpoint** probes used for intermediate champion selection. 

## **5.1 Main Findings** 

_Performance over Zero-Shot and Reflexion._ FORGE improves over both zero-shot and Reflexion baselines for every model family under all three representations (Table 3). Under the FORGE protocol, the strongest configurations reduce mean negative returns to the midtwenties: Gemini improves from −189 _._ 6 to −24 _._ 5 (Examples, 7 _._ 7×), Qwen from −103 _._ 3 to −24 _._ 3 (Examples, 4 _._ 3×), Llama from −113 _._ 1 to −28 _._ 3 (Examples, 4 _._ 0×), and Grok from −58 _._ 4 to −33 _._ 7 (Rules, 1 _._ 7×). Compared to the Reflexion baseline, FORGE improves in all 12 model-representation conditions (Table 3, ΔRefl columns). Figure 3 provides a detailed comparison across all models under each representation. The peak observed **checkpoint** return reaches −3 _._ 60 (Gemini Rules), approaching the DRL top score of −3 _._ 47, although post-session evaluation means remain lower due to sampling variance. 

_Representation Analysis._ Figure 3 compares all three representations across all four models under zero-shot, Reflexion, and FORGE conditions. Examples achieves the best FORGE return for three of four models (Gemini, Llama, Qwen), while Grok performs best under Rules. In the replicated Gemini study (7 sessions per condition), all three representations yield large improvements over the zeroshot baseline (−189 _._ 6): Examples −24 _._ 5 ± 21 _._ 1, Rules −30 _._ 6 ± 37 _._ 0, and Mixed −32 _._ 2 ± 28 _._ 1. Examples achieves the best mean return and lowest variance, while Rules provides the most reliable costperformance profile with ∼40% fewer total tokens than Examples 

ACM CAIS ’26, May 26–29, 2026, San Jose, CA, USA 

FORGE: Self-Evolving Agent Memory With No Weight Updates 


![](P014_images/P014.pdf-0007-02.png)


**Figure 3: Comparison of memory representations (Rules, Examples, and Mixed) across zero-shot, Reflexion, and FORGE conditions for all four model families. Bars represent mean return; error bars denote SEM. Improvement factors over zero-shot annotated above FORGE bars; checkmarks indicate the winning condition.** 


![](P014_images/P014.pdf-0007-04.png)


**Figure 4: Combined analysis for Gemini-2.5-Flash-Lite. (A) Performance: All representations consistently outperform Baseline. (B) Token Cost: Rules representation is more efficient than others. (C) Evaluation Cost-Benefit: Rules offers best balance of low cost and high return.** 

(Figure 4, Panel B). This efficiency gap arises because example-based memory inflates prompt length, while rule-based artifacts are more compact and lead to faster graduation. Mixed falls between the two on both cost and performance (Figure 4). 

_Token Cost Analysis._ In the replicated Gemini study (Figure 4, Panel B), Rules consumes ∼106M total tokens compared to ∼177M for Examples and ∼188M for Mixed, a ∼40% cost reduction. This efficiency stems from both shorter prompts and fewer active instances due to faster graduation. The no-graduation variants consume more tokens across all representations because all 10 instances remain active for all 6 stages, confirming that graduation’s primary contribution is compute savings (Figure 4, Panel C). 

_Cross-Model Analysis: Weak Models Benefit Most._ We examine generalization across model families as directional evidence (nonGemini models receive 3-4 FORGE sessions per representation). The magnitude of improvement inversely correlates with baseline strength: Gemini (worst baseline, −189 _._ 6) gains 7 _._ 7×, followed by 

Qwen (4 _._ 3×) and Llama (4 _._ 0×), while Grok (best baseline, −58 _._ 4) gains 1 _._ 7× (Figure 3). This pattern suggests FORGE functions primarily as a variance-reduction mechanism for unreliable policies, mitigating capability gaps rather than amplifying strong models. For every tested family, FORGE outperforms both zero-shot and Reflexion under all three representations. 

_Population Broadcast vs. Isolated Reflexion._ Comparing FORGE against the Reflexion baseline isolates the contribution of populationlevel knowledge transfer (Figure 5, Panel A). FORGE improves post-session evaluation return by 29-72% over Reflexion in all 12 model-representation conditions (Table 3, ΔRefl columns). The nograduation variant also outperforms Reflexion in all 12 conditions, confirming that champion broadcast is the essential mechanism. Reflexion instances exhibit persistently high volatility across stages (Figure 5, Panel B), whereas FORGE steadily compresses score variance. 

ACM CAIS ’26, May 26–29, 2026, San Jose, CA, USA 

Bogdanov et al. 


![](P014_images/P014.pdf-0008-02.png)


**Figure 5: Protocol comparison. (A) Mean evaluation return across four models under four conditions: FORGE, FORGE without graduation, Reflexion (isolated learning), and zero-shot. FORGE and its no-graduation variant both outperform Reflexion and zero-shot for every model. (B) Standard deviation of checkpoint scores across stages; FORGE reduces volatility steadily while Reflexion remains near the zero-shot level (dashed).** 


![](P014_images/P014.pdf-0008-04.png)


**Figure 6: Graduation dynamics and no-graduation ablation (all models pooled). (A) Active instances and per-instance compute by stage: FORGE (solid lines) reduces active count via graduation, while the no-graduation variant (dashed) keeps all 10 instances active throughout. Faded bars show per-active-instance token cost. (B) Adaptation tokens per instance vs. final evaluation return by stage: FORGE’s per-instance cost drops as instances graduate; the no-graduation variant achieves a slightly better pooled evaluation return at higher total cost. Reflexion baseline (dotted) shown for reference.** 

## **5.2 Ablation: No-Graduation** 

The no-graduation variant retains champion broadcast but keeps all 10 instances active throughout all 6 stages, isolating the contribution of graduation from that of broadcast. Across models, FORGE reduces the active instance count as stages progress (Figure 6, Panel A, solid lines), with per-instance adaptation cost dropping as instances graduate. The no-graduation variant (dashed) consumes roughly twice the adaptation tokens per instance by S6 (Figure 6, Panel B). The effect of graduation on final performance is model-dependent: removing it helps Grok and Qwen (up to 67% improvement over FORGE, Table 3), while Gemini and Llama perform better with 

graduation in 2 of 3 representations. This split suggests that graduation’s memory-freezing mechanism protects strong early-stage artifacts in some models but terminates learning prematurely in others. Both FORGE variants outperform the Reflexion baseline in all 12 conditions, confirming that broadcast is the essential mechanism regardless of whether graduation is enabled. 

## **5.3 Sensitivity: Failure Trigger Threshold** 

The failure trigger _𝜏_ determines which per-step penalties invoke reflection and restart the episode, directly controlling the learning signal’s composition. To assess whether the chosen _𝜏_ = −1 _._ 1 is optimal, we sweep _𝜏_ ∈{−1 _._ 1 _,_ −2 _._ 0 _,_ −3 _._ 0 _,_ −11 _._ 0} on Gemini Rules 

ACM CAIS ’26, May 26–29, 2026, San Jose, CA, USA 

FORGE: Self-Evolving Agent Memory With No Weight Updates 


![](P014_images/P014.pdf-0009-02.png)

### Figure analysis

The figure presents a two-panel risk and variance analysis comparing zero-shot, Reflexion, and FORGE variants.

**Panel A — Tail Risk Distribution (All Models Pooled)**

- **Purpose:** Shows cumulative distributions of evaluation scores to compare tail risk across methods.
- **Axes:**
  - x-axis: Evaluation Score, ranging roughly from −250 to 0.
  - y-axis: Cumulative Probability, ranging from 0.0 to 1.0.
- **Legend/series:**
  - Zero-Shot: gray dashed line.
  - Reflexion: orange dash-dot line.
  - Rules (FORGE): orange solid line.
  - Examples (FORGE): blue solid line.
  - Mixed (FORGE): green solid line.
- **Reference thresholds:** Vertical dotted lines mark qualitative failure regions:
  - Catastrophic near −150.
  - Major near −100.
  - Minor near −50.
- **Direct observations:**
  - The zero-shot curve has high cumulative probability at very negative scores, indicating a heavy left tail.
  - Reflexion is shifted rightward relative to zero-shot but still retains substantial probability mass below the major and minor thresholds.
  - All FORGE curves remain near zero cumulative probability over much of the severe negative-score range and rise steeply only near higher scores, indicating fewer very poor outcomes.
  - Among FORGE variants, the Rules, Examples, and Mixed curves are clustered, with small visual differences.
- **Interpretation:** The visual pattern supports the paper’s claim that FORGE reduces low-return tail risk more strongly than Reflexion or zero-shot prompting.

**Panel B — Performance Variance by Model**

- **Purpose:** Compares mean reward plus/minus standard deviation across models for zero-shot, Reflexion, and FORGE.
- **Axes:**
  - x-axis: Model.
  - y-axis: Mean Reward ± Std Dev.
- **Models shown:**
  - Gemini 2.5 Flash Lite.
  - Grok 4 Fast.
  - Llama 4 Maverick.
  - Qwen3 235B (A22B).
- **Legend/series:**
  - Zero-Shot: gray bars.
  - Reflexion: orange bars.
  - FORGE: blue bars.
  - Text annotations above Reflexion and FORGE bars report percentage change versus zero-shot.
- **Readable percentage annotations:**

| Model | Reflexion Δ vs Zero-Shot | FORGE Δ vs Zero-Shot |
|---|---:|---:|
| Gemini 2.5 Flash Lite | −21% | +45% |
| Grok 4 Fast | −22% | +35% |
| Llama 4 Maverick | +24% | +54% |
| Qwen3 235B (A22B) | +5% | +70% |

- **Direct observations:**
  - FORGE bars are visually closer to zero reward than zero-shot bars for all four models.
  - FORGE has the strongest positive annotated improvement versus zero-shot for every model.
  - Reflexion is mixed: it is annotated as worse than zero-shot for Gemini and Grok, but better for Llama and Qwen.
  - Error bars are large for zero-shot and generally appear smaller for FORGE, especially relative to the strongly negative zero-shot outcomes.
- **Interpretation:** Panel B supports the surrounding discussion that FORGE compresses variance and stabilizes outcomes across models, while Reflexion provides less consistent improvement.

**Connection to surrounding text:** The figure directly supports the paper’s Discussion claims that FORGE reduces major failures by eliminating much of the heavy left tail of zero-shot returns and compresses outcome variance. It also visually reinforces the stated comparison that Reflexion partially improves the distribution but does not match the rightward shift and variance reduction achieved by FORGE.


**Figure 7: Risk and variance analysis. (A) Cumulative distribution of evaluation scores (all models pooled): zero-shot shows a heavy left tail; Reflexion partially compresses it; FORGE shifts the distribution sharply rightward. (B) Mean return** ± **SD by model under zero-shot, Reflexion, and FORGE (best representation per model).** 

(the primary configuration). The result is non-monotone: _𝜏_ = −2 _._ 0 (mean −52 _._ 0) and _𝜏_ = −3 _._ 0 (mean −46 _._ 0) both degrade relative to _𝜏_ = −1 _._ 1 (mean −30 _._ 6, 83% graduation), while _𝜏_ = −11 _._ 0 yields the best result (mean −24 _._ 6, 93% graduation). Restricting reflection to only the most severe failures appears to produce a cleaner learning signal, though skipping moderate failures hurts. The improvement at _𝜏_ = −11 _._ 0 suggests that harsher triggers and multi-threshold triggering strategies warrant further investigation. The reward distribution motivating _𝜏_ = −1 _._ 1 is detailed in Appendix D. 

## **6 Discussion** 

The protocol’s efficacy stems from four interacting mechanisms: (1) reducing major failures by eliminating the heavy tail of low zero-shot returns (Figure 7, Panel A); (2) compressing variance to stabilize outcomes (Figure 7, Panel B); (3) population-level distillation via champion broadcast; and (4) graduation-based early stopping to reduce compute. Figure 7, Panel A shows that Reflexion (orange) partially compresses the zero-shot tail, but FORGE shifts the distribution rightward, reducing the rate of episodes below −100 from ∼90% (zero-shot) to ∼1% under the strongest configurations. 

The broadcast mechanism’s consistent 29-72% improvement over Reflexion across all 12 conditions suggests that the primary bottleneck in prompt-only adaptation is not the quality of individual reflections but the absence of a selection pressure that propagates rare discoveries to the population. 

## **7 Limitations & Future Work** 

Our study faces limitations in scope (single attacker type, fixed 30-step horizon in one application domain) and protocol dynamics (brittle single-best broadcast, checkpoint-evaluation misalignment). All evidence is confined to CAGE-2 B_line; generalization to other attacker types and POMDP environments remains untested. Crossfamily findings are presented as directional evidence based on 3- 4 sessions per non-Gemini model. The failure trigger sensitivity sweep reveals that _𝜏_ = −11 _._ 0 outperforms the submitted _𝜏_ = −1 _._ 1, indicating that the chosen threshold is not optimal and that the 

broader design space of harsher triggers and multi-threshold triggering remains unexplored. Future work should address these limitations by testing additional attacker variants. Promising extensions include cross-strategy seeding (e.g., Mixed from Rules), crossmodel artifact transfer, co-evolutionary adversarial training, costcontrolled comparisons against parameter-efficient fine-tuning to clarify the trade-offs of prompt-only adaptation, and replacing the Reflexion inner loop with alternative self-improvement methods (e.g., TextGrad [24], Dynamic Cheatsheet [17]) to test whether the population broadcast mechanism generalizes further. 

## **8 Conclusion** 

We introduced FORGE, a staged, population-based protocol for improving LLM agents via _prompt-injected memory evolution_ , demonstrating that effective long-horizon strategies can be learned without gradient updates or stronger teacher models. By coupling a Reflexion-style inner loop that converts failures into dynamic knowledge artifacts (Rules, Examples, or both) with an outer loop that stabilizes learning through champion broadcast and graduationbased early stopping, FORGE achieves 1.7-7.7× improvement over zero-shot baselines and 29-72% improvement over the Reflexion baseline across all 12 model-representation conditions on CybORG CAGE-2 B_line at a 30-step horizon. Among representations, Examples achieves the strongest returns for three of four models, while Rules offers the best cost-reliability profile with ∼40% fewer tokens. The no-graduation ablation confirms that champion broadcast is the essential mechanism, with graduation primarily contributing compute savings. Cross-family results are directional evidence based on 3-4 sessions per non-Gemini model; generalization to other attacker types and environments remains future work. Within this benchmark, these results suggest that evolving interpretable natural-language memory provides a viable adaptation path for prompt-only learning in stochastic POMDPs where weight updates are infeasible, and encourage further research into alternative strategies. Reproducibility details and ethics considerations are in Appendix A. The archived artifact is available at https://doi.org/10.5281/zenodo.19907612; the development repository is available at https://github.com/isbogdanov/forge-protocol. 

ACM CAIS ’26, May 26–29, 2026, San Jose, CA, USA 

Bogdanov et al. 

## **References** 

[1] 2022. TTCP CAGE Challenge 2. https://github.com/cage-challenge/cagechallenge-2 

- [2] CardiffUni Team. 2022. CybORG CAGE-2 Winning Agent: PPO + Greedy Decoys. https://github.com/john-cardiff/-cyborg-cage-2. 

- [3] Sebastián R. Castro, Roberto Campbell, Nancy Lau, Octavio Villalobos, Jiaqi Duan, and Alvaro A. Cardenas. 2025. Large Language Models are Autonomous Cyber Defenders. arXiv:2505.04843 [cs.CR] https://arxiv.org/abs/2505.04843 

- [4] Chrisantha Fernando, Dylan Sunil Banarse, Henryk Michalewski, Simon Osindero, and Tim Rocktäschel. 2024. PromptBreeder: Self-Referential SelfImprovement via Prompt Evolution. In _The Twelfth International Conference on Learning Representations_ . arXiv:2309.16797 [cs.CL] https://openreview.net/ forum?id=HKkiX32Zw1 

- [5] Yao Fu, Dong-Ki Kim, Jaekyeom Kim, Sungryull Sohn, Lajanugen Logeswaran, Kyunghoon Bae, and Honglak Lee. 2024. AutoGuide: Automated Generation and Selection of Context-Aware Guidelines for Large Language Model Agents. In _Advances in Neural Information Processing Systems_ . arXiv:2403.08978 [cs.AI] https://openreview.net/forum?id=mRIQz8Zd6O 

- [6] Qingyan Guo, Rui Wang, Junliang Guo, Bei Li, Kaitao Song, Xu Tan, Guoqing Liu, Jiang Bian, and Yujiu Yang. 2024. Connecting Large Language Models with Evolutionary Algorithms Yields Powerful Prompt Optimizers. In _The Twelfth International Conference on Learning Representations_ . arXiv:2309.08532 [cs.CL] https://openreview.net/forum?id=ZG3RaNIsO8 

- [7] Max Jaderberg, Valentin Dalibard, Simon Osindero, Wojciech M. Czarnecki, Jeff Donahue, Ali Razavi, Oriol Vinyals, Green Tim, Iain Dunning, Karen Simonyan, et al. 2017. Population Based Training of Neural Networks. arXiv:1711.09846 [cs.LG] https://arxiv.org/abs/1711.09846 

- [8] Mitchell Kiely, David Bowman, Maxwell Standen, and Christopher Moir. 2023. On Autonomous Agents in a Cyber Defence Environment. arXiv:2309.07388 [cs.CR] https://arxiv.org/abs/2309.07388 

- [9] Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler Hallinan, Luyu Gao, Sarah Wiegreffe, Uri Alon, Nouha Dziri, Shrimai Prabhumoye, Yiming Yang, Shashank Gupta, Bodhisattwa Prasad Majumder, Katherine Hermann, Sean Welleck, Amir Yazdanbakhsh, and Peter Clark. 2023. Self-Refine: Iterative Refinement with Self-Feedback. In _Advances in Neural Information Processing Systems_ . https: //openreview.net/forum?id=S37hOerQLB 

- [10] Bodhisattwa Prasad Majumder, Bhavana Dalvi, Peter Jansen, Oyvind Tafjord, Niket Tandon, Li Zhang, Chris Callison-Burch, and Peter Clark. 2024. CLIN: A Continually Learning Language Agent for Rapid Task Adaptation and Generalization. In _The Twelfth International Conference on Learning Representations_ . arXiv:2310.10134 [cs.AI] https://openreview.net/forum?id=d5DGVHMdsC 

- [11] Hamoun Mohammadi, Jonathan J. Davis, and Mitchell Kiely. 2025. Leveraging Large Language Models for Autonomous Cyber Defense: Insights from CAGE-2 Simulations. _IEEE Intelligent Systems_ 40, 4 (2025), 29–36. doi:10.1109/MIS.2025. 3568209 

- [12] Charles Packer, Sarah Wooders, Kevin Lin, Vivian Fang, Shishir G. Patil, Ion Stoica, and Joseph E. Gonzalez. 2023. MemGPT: Towards LLMs as Operating Systems. arXiv:2310.08560 [cs.AI] https://arxiv.org/abs/2310.08560 

- [13] Joon Sung Park, Joseph C. O’Brien, Carrie J. Cai, Meredith Ringel Morris, Percy Liang, and Michael S. Bernstein. 2023. Generative Agents: Interactive Simulacra of Human Behavior. In _Proceedings of the 36th Annual ACM Symposium on User Interface Software and Technology (UIST)_ . doi:10.1145/3586183.3606763 

- [14] Vishnu Sarukkai, Zhiqiang Xie, and Kayvon Fatahalian. 2025. Self-Generated In-Context Examples Improve LLM Agents for Sequential Decision-Making Tasks. arXiv:2505.00234 [cs.LG] https://arxiv.org/abs/2505.00234 

- [15] Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik R. Narasimhan, and Shunyu Yao. 2023. Reflexion: Language Agents with Verbal Reinforcement Learning. In _Advances in Neural Information Processing Systems_ . https: //openreview.net/forum?id=vAElhFcKW6 

- [16] Maxwell Standen, Martin Lucas, David Bowman, Toby J. Richer, Junae Kim, and Damian Marriott. 2021. CybORG: A Gym for the Development of Autonomous Cyber Agents. arXiv:2108.09118 [cs.CR] https://arxiv.org/abs/2108.09118 

- [17] Mirac Suzgun, Mert Yüksekgönül, Federico Bianchi, Dan Jurafsky, and James Zou. 2025. Dynamic Cheatsheet: Test-Time Learning with Adaptive Memory. arXiv:2504.07952 [cs.LG] https://arxiv.org/abs/2504.07952 

- [18] Khanh-Tung Tran, Dung Dao, Minh-Duong Nguyen, Quoc-Viet Pham, Barry O’Sullivan, and Hoang D. Nguyen. 2025. Multi-Agent Collaboration Mechanisms: A Survey of LLMs. arXiv:2501.06322 [cs.AI] https://arxiv.org/abs/2501.06322 

- [19] Xingchen Wan, Ruoxi Sun, Hootan Nakhost, and Sercan O. Arik. 2024. Teach Better or Show Smarter? On Instructions and Exemplars in Automatic Prompt Optimization. In _Advances in Neural Information Processing Systems_ . arXiv:2406.15708 [cs.CL] https://openreview.net/forum?id=IdtoJVWVnX 

- [20] Guanzhi Wang, Yuqi Xie, Yunfan Jiang, Ajay Mandlekar, Chaowei Xiao, Yuke Zhu, Linxi Fan, and Anima Anandkumar. 2023. Voyager: An Open-Ended Embodied Agent with Large Language Models. arXiv:2305.16291 [cs.AI] https://arxiv.org/ abs/2305.16291 

- [21] Zora Zhiruo Wang, Jiayuan Mao, Daniel Fried, and Graham Neubig. 2025. Agent Workflow Memory. In _International Conference on Machine Learning_ . arXiv:2409.07429 [cs.AI] https://openreview.net/forum?id=NTAhi2JEEE 

- [22] Chengrun Yang, Xuezhi Wang, Yifeng Lu, Hanxiao Liu, Quoc V. Le, Denny Zhou, and Xinyun Chen. 2024. Large Language Models as Optimizers. In _The Twelfth International Conference on Learning Representations_ . arXiv:2309.03409 [cs.LG] https://openreview.net/forum?id=Bb4VGOWELI 

- [23] Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik R. Narasimhan, and Yuan Cao. 2023. ReAct: Synergizing Reasoning and Acting in Language Models. In _International Conference on Learning Representations_ . arXiv:2210.03629 [cs.CL] https://openreview.net/forum?id=WE_vluYUL-X 

- [24] Mert Yuksekgonul, Federico Bianchi, Joseph Boen, Sheng Liu, Zhi Huang, Carlos Guestrin, and James Zou. 2024. TextGrad: Automatic "Differentiation" via Text. arXiv:2406.07496 [cs.CL] https://arxiv.org/abs/2406.07496 

- [25] Qizheng Zhang, Changran Hu, Shubhangi Upasani, Boyuan Ma, Fenglu Hong, Vamsidhar Kamanuru, Jay Rainton, Chen Wu, Mengmeng Ji, Hanchen Li, Urmish Thakker, James Zou, and Kunle Olukotun. 2025. Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models. arXiv:2510.04618 [cs.AI] https://arxiv.org/abs/2510.04618 

- [26] Andrew Zhao, Daniel Huang, Quentin Xu, Matthieu Lin, Yong-Jin Liu, and Gao Huang. 2024. ExpeL: LLM Agents Are Experiential Learners. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , Vol. 38. 19632–19642. arXiv:2308.10144 [cs.AI] doi:10.1609/aaai.v38i17.29936 

## **A Ethics Statement & Reproducibility** 

All authors adhere to the ACM Code of Ethics<sup>1</sup> . No human-subject data, personally identifiable information, or user-generated content is collected; all results are based on simulator-generated traces. Experiments are confined to the CybORG CAGE-2 benchmark and do not interact with real systems. We frame FORGE strictly for defensive decision-making but recognize the dual-use potential of cybersecurity automation. Since the protocol is compute-intensive, we report cost metrics and use graduation to reduce unnecessary runs. As non-native English speakers, we used LLM-based tools for language polishing and assistance with data processing scripts. 

## **A.1 Artifact Availability and Scope** 

The artifact supporting this paper is archived on Zenodo at https: //doi.org/10.5281/zenodo.19907612. The development repository is available at https://github.com/isbogdanov/forge-protocol. Detailed build, configuration, and execution instructions are provided in the artifact README. 

The archived artifact contains the implementation of the FORGE protocol, the experiment runner, container specification, API-key template, and configuration files for running the population-broadcast and Reflexion-style baselines. agent_base/ contains the main implementation, including the hierarchical Planner, Analyst, and ActionChooser agents, the Reflector and Exemplifier learning agents, the CybORG coordinator, the learning coordinator, provider configuration, and metric/logging utilities. The acting agents are configured through YAML definition files, including static prompt components and dynamic memory files e.g. reflection_knowledge.yaml and reflection_examples.yaml. These files are updated during training when the learning agents synthesize rules or examples from failed trajectories. 

Experiments are launched through run_experiment.py. The release includes experiment_forge_eval.yaml for the FORGE condition (transfer_strategy: best, champion broadcast, 10 instances) and experiment_reflexion_eval.yaml for the isolated 

1https://www.acm.org/code-of-ethics 

ACM CAIS ’26, May 26–29, 2026, San Jose, CA, USA 

FORGE: Self-Evolving Agent Memory With No Weight Updates 

Reflexion baseline (transfer_strategy: individual, no population broadcast). The configuration files expose the main protocol parameters, including the number of stages, the graduation threshold, the per-step failure threshold, the memory representation (rules, examples, or mixed), and the number of learning attempts per stage. The released FORGE configuration uses six stages, a graduation threshold of −15, a per-step reflection trigger of −1 _._ 1, and three learning attempts per stage. 

A run creates an experiment directory containing the copied configuration, stage-level summaries, workspaces with the learned memory snapshots, final evaluation reports, aggregate summaries, runtime logs, and connector token-usage logs for that run. Full raw LLM-provider transcripts and evolved memory artifacts from the original study are not bundled in the public artifact because of storage size and API cost. They may be available upon request from the authors, subject to transfer and storage constraints. Because original run seeds and provider-side execution state are not bundled, the artifact supports executable reruns of the released protocol configurations rather than bit-for-bit regeneration of the original logs. The paper itself reports the per-instance evaluation scores used for the aggregate statistics; the artifact is intended to let readers inspect the implementation, verify the protocol configuration, and rerun selected FORGE or Reflexion conditions under the documented setup. 

## **B CAGE-2 Environment Details** 

We evaluate the protocol on the CAGE-2 autonomous cyber-defense challenge [1, 16], a partially observable Markov decision process (POMDP) where a _blue_ defender protects an enterprise network against an automated _red_ attacker. 

_Topology and Assets._ The simulated network (Figure 8a) consists of 3 subnets hosting 13 nodes: user workstations (Subnet 1), enterprise servers (Subnet 2), and a high-value operational server (Subnet 3). The defender’s goal is to maintain the availability and integrity of these assets, particularly the operational server. 

_Attacker Model (_ b_line _)._ The red agent follows a scripted policy implementing a standard kill chain (Figure 8b). Starting from an external position, it progresses through phases of _Discovery_ (scanning for IPs), _Access_ (identifying services), _Lateral Movement_ (exploiting user privileges), and _Escalation_ (gaining root). The defender can push the attacker back to earlier states via remediation actions, creating a dynamic tug-of-war. 

_Action Space._ Episodes last _𝑇_ =30 steps. At each step, the blue agent selects an action: 

- **Monitor** : Passive observation with no intervention. 

- **Analyse** _ℎ_ : Inspect host _ℎ_ for anomalies (low cost). 

- **Remove** _ℎ_ : Terminate suspicious processes (moderate cost, imperfect success). 

- **Restore** _ℎ_ : Reimage _ℎ_ to a clean state (high cost, guarantees remediation). 

- **Decoy** _ℎ_ : Deploy a honeypot to misdirect the attacker (moderate cost). 

the attacker’s latent state. The per-step reward _𝑟𝑠𝑡𝑒𝑝_ ≤ 0 penalizes both ongoing compromise and the operational cost of defensive actions. An effective defense minimizes this penalty (achieving returns closer to zero) by balancing timely detection with targeted, cost-efficient interventions and proactive defense. 

## **C Knowledge Artifact Examples** 

This section provides verbatim examples of the two artifact types generated during FORGE training, illustrating what is stored in prompt memory and how the representations differ. Both artifacts below were produced by a Qwen3-235B training session. 

_Rules Artifact._ The Reflector distills each failed trajectory into conditional heuristics, organized per agent role. These rules are injected into the agent’s system prompt via a <reflection_knowledge> section. 

_Examples Artifact._ The Exemplifier converts the failed trajectory into a structured few-shot demonstration that mimics a complete ReAct interaction cycle (Thought–Tool–Observation–Answer), injected via a <TOOL_USE_EXAMPLES> section. 

## **D Failure Trigger Threshold Analysis** 

The failure trigger _𝜏_ determines which per-step rewards abort the episode and invoke the reflection agent. Figure 11 shows the distribution of per-step penalties across 540 zero-shot episodes (all four model families, 13,446 penalized steps). Penalties cluster into distinct groups: _Restore_ actions at −1 _._ 0 (3,520 occurrences, red), small failures at −1 _._ 1 to −1 _._ 2, moderate failures at −2 _._ 0 to −3 _._ 2, and severe failures at −11 to −14, with a gap between −3 _._ 3 and −10 _._ 9. The chosen threshold _𝜏_ = −1 _._ 1 achieves 100% precision (zero false positives from Restore) while capturing 74% of all real failure events (7,346 of 9,926 true triggers). 

To assess sensitivity, we tested three additional thresholds on Gemini Rules (the primary model-representation pair with 7-session coverage). Relative to _𝜏_ = −1 _._ 1 (mean return −30 _._ 6, 83% graduation rate): _𝜏_ = −2 _._ 0 yields mean −52 _._ 0 over 40 episodes; _𝜏_ = −3 _._ 0 yields mean −46 _._ 0 over 40 episodes; and _𝜏_ = −11 _._ 0 yields mean −24 _._ 6 with 93% graduation over 60 episodes. The result is non-monotone: skipping small and moderate failures ( _𝜏_ = −2 _._ 0, −3 _._ 0) degrades performance, but restricting reflection to only the most severe failures ( _𝜏_ = −11 _._ 0) improves over the submitted value. This suggests that triggering on severe failures produces a cleaner learning signal, though the broader design space of multi-threshold triggering remains unexplored. 

Table 4 provides session-level aggregates for each threshold, and Table 5 reports the complete per-instance evaluation scores. 

**Table 4: Failure Trigger Threshold Sweep: Session-Level Results (Gemini Rules)** 

|**Threshold (**_𝜏_**)**|**Runs**|**Episodes**|**Mean Return**|**SD**|**Grad. Rate**|
|---|---|---|---|---|---|
|−1_._1(default)|7|140|−30_._6|37_._0|83%|
|−2_._0|2|40|−52_._0|59_._6|65%|
|−3_._0|2|40|−46_._0|52_._9|75%|
|−11_._0|3|60|−24_._6|28_._2|**93%**|



_Partial Observability and Reward._ The defender observes only host-level indicators (processes, connections, files) and must infer 

ACM CAIS ’26, May 26–29, 2026, San Jose, CA, USA 

Bogdanov et al. 


![](P014_images/P014.pdf-0012-02.png)


### **(a) Network Topology: 3 subnets containing user hosts, enterprise servers, and operational servers.** 


![](P014_images/P014.pdf-0012-04.png)

### Figure analysis

Purpose: The figure provides an overview of the CAGE-2 environment used in the paper’s cyber-defense experiments, showing both the protected network structure and the automated attacker’s progression model.

**Panel (a): Network Topology**

Direct observations:
- The network is divided into three labeled subnets: **Subnet 1**, **Subnet 2**, and **Subnet 3**.
- A legend identifies icons for **router**, **switch**, **server**, **firewall**, and **host**.
- **Subnet 1** contains a switch connected to five **User Hosts** and to a router.
- **Subnet 2** contains a switch connected to three **Enterprise Servers** and one **Defender** host.
- **Subnet 3** contains a switch connected to three **Operational Hosts** and one **Operational Server**.
- Firewalls and routers separate the subnets, indicating controlled inter-subnet communication.
- Counting endpoint hosts and servers gives the captioned **13-host network**: 5 user hosts, 3 enterprise servers, 1 defender host, 3 operational hosts, and 1 operational server.

Interpretation:
- The defender operates from the central enterprise subnet and must protect assets distributed across user, enterprise, and operational segments.
- The segmented architecture implies that attacker movement between subnets is constrained by routers/firewalls, making lateral movement and observability important aspects of the task.

**Panel (b): Attacker State Transitions**

Direct observations:
- The attacker state machine begins at **Unknown Host**.
- A red transition labeled **Discover Remote Systems** moves the attacker to **Host, Services Unknown**.
- A second red transition labeled **Discover Network Services** moves the attacker to **Host, Services Known**.
- From **Host, Services Known**, a red **Successful Exploit** transition leads to **Exploited Host (User)**.
- From **Exploited Host (User)**, a red **Privilege Escalation** transition leads to **Exploited Host (Root)**.
- A red self-loop labeled **Impact** appears on **Exploited Host (Root)**.
- A red transition labeled **Failed Exploit (Error or Fake Service)** loops back around the known-services stage.
- Blue defender-related transitions include **Remove Program**, pointing from the exploited-user stage back toward the known-services state, and **Restore Machine**, which resets attacker progress from compromised/advanced states back toward earlier host/service knowledge states.

Interpretation:
- The attacker follows a progressive kill chain: discovery → service enumeration → user-level compromise → root compromise → impact.
- Defender actions can partially or fully reverse attacker progress, with restoration serving as a stronger reset mechanism than program removal.
- The red transitions represent attacker advancement or failure, while blue transitions represent defender intervention.

Connection to surrounding text:
- The surrounding section discusses partial observability, rewards, and failure-trigger thresholds for reflection in the CAGE-2 defense setting. This figure grounds those experiments by clarifying what the defender is protecting and how attacker progress is modeled.
- The topology explains why the defender observes host-level indicators across a segmented network, while the attacker state machine explains why actions such as **Restore** can reset progress and why failures or severe compromises produce meaningful learning signals in the paper’s threshold analysis.


### **(b) Attacker State Transitions: The progressive kill chain from discovery to root compromise.** 

**Figure 8: CAGE-2 Environment Overview. (a) The defender protects a 13-host network segmented into subnets [8]. (b) The automated attacker follows a multi-stage state machine; successful exploits advance the attacker’s position, while defender actions (like Restore) can reset this progress [8].** 

## **E Supplementary Analysis Tables** 

Table 6 reports standard deviations corresponding to the mean results in the main paper (Table 3). Table 7 summarizes the experimental setup across all conditions. 

## **E.1 Primary Model Statistical Detail** 

Table 9 provides session-level detail for the primary model (Gemini2.5-Flash-Lite), which received the most comprehensive evaluation with 7 independent runs per strategy. 

Table 8 presents per-strategy Reflexion results across all models, providing detailed ablation data for the single-instance learning baseline. 

## **E.2 Graduation Dynamics** 

Table 10 reports the distribution of graduation rates across models and strategies, quantifying how many instances successfully completed the learning curriculum. 

ACM CAIS ’26, May 26–29, 2026, San Jose, CA, USA 

FORGE: Self-Evolving Agent Memory With No Weight Updates 

**Table 5: Raw Evaluation Scores: Failure Trigger Threshold Sweep (Gemini Rules, FORGE Protocol)** 

|_𝜏_|**Instance**|**R1-E1**|**R1-E2**|**R2-E1**|**R2-E2**|**R3-E1**|**R3-E2**|**Tokens (M)**|**Grad**|
|---|---|---|---|---|---|---|---|---|---|
|−2_._0|instance_1|−35_._1|−13_._2|−51_._2|−14_._7|—|—|||
||instance_2|−44_._9|−84_._8|−22_._2|−19_._9|—|—|||
||instance_3|−14_._8|−16_._6|−20_._4|−37_._0|—|—|||
||instance_4|−17_._8|−37_._2|−51_._3|−13_._3|—|—|||
||instance_5|−17_._8|−172_._2|−198_._8|−16_._9|—|—|1952|13/20|
||instance_6|−161_._4|−41_._2|−14_._1|−92_._2|—|—|.||
||instance_7|−19_._3|−17_._5|−16_._7|−14_._2|—|—|||
||instance_8|−197_._8|−177_._2|−36_._2|−18_._1|—|—|||
||instance_9|−14_._2|−17_._3|−21_._1|−15_._2|—|—|||
||instance_10|−198_._8|−67_._8|−20_._5|−19_._2|—|—|||
|−3_._0|instance_1|−62_._7|−30_._4|−13_._2|−125_._5|—|—|||
||instance_2|−36_._1|−172_._2|−77_._4|−14_._5|—|—|||
||instance_3|−15_._1|−14_._5|−16_._7|−15_._6|—|—|||
||instance_4|−12_._3|−111_._2|−17_._5|−17_._7|—|—|||
||instance_5|−14_._2|−52_._2|−18_._5|−13_._1|—|—|2267|15/20|
||instance_6|−22_._3|−223_._6|−16_._4|−47_._1|—|—|.||
||instance_7|−46_._5|−17_._6|−37_._3|−16_._3|—|—|||
||instance_8|−15_._5|−13_._9|−14_._7|−16_._0|—|—|||
||instance_9|−69_._3|−197_._3|−93_._6|−84_._2|—|—|||
||instance_10|−15_._3|−14_._5|−11_._2|−16_._2|—|—|||
|−11_._0|instance_1|−72_._5|−14_._2|−12_._5|−26_._1|−27_._2|−38_._2|||
||instance_2|−16_._5|−13_._1|−15_._4|−89_._9|−13_._3|−15_._4|||
||instance_3|−15_._6|−59_._7|−13_._4|−13_._2|−17_._5|−15_._9|||
||instance_4|−15_._2|−14_._2|−12_._5|−61_._2|−19_._2|−15_._1|||
||instance_5|−12_._7|−14_._2|−13_._5|−21_._7|−17_._4|−16_._7|||
||instance_6|−12_._5|−16_._7|−27_._5|−50_._0|−201_._4|−20_._4|320.9|28/30|
||instance_7|−16_._2|−15_._4|−14_._4|−17_._5|−49_._5|−14_._0|||
||instance_8|−12_._2|−15_._4|−13_._2|−12_._4|−15_._5|−20_._2|||
||instance_9|−13_._4|−12_._4|−14_._2|−13_._4|−11_._8|−16_._2|||
||instance_10|−14_._4|−22_._2|−15_._2|−14_._2|−16_._2|−45_._2|||



**Table 6: Standard deviations of episode return corresponding to Table 3. Lower SD = more reliable policy. Bold marks the lowest SD per model across all FORGE variants.** ↑ **/** ↓ **= reduction/increase relative to the reference.** 

||||**Ref**|**exion**||**FORGE**|||**FORG**|**E w/o gra**|**d**|
|---|---|---|---|---|---|---|---|---|---|---|---|
|**Model**|**ZS SD**|**Repr**|**SD**|Δ**ZS**|**SD**|Δ**ZS**|Δ**Ref**|**SD**|Δ**ZS**|Δ**Ref**|Δ**FORGE**|
|Gemini||Rules|60.5|↓12%|37.0|↑**31%**|↑**39%**|26.5|↑**51%**|↑**56%**|↑**28%**|
||53.9|Examples|60.4|↓12%|21_._1|↑**61%**|↑**65%**|27.2|↑**50%**|↑**55%**|↓29%|
|||Mixed|74.6|↓38%|28.1|↑**48%**|↑**62%**|30.7|↑**43%**|↑**59%**|↓9%|
|Grok||Rules|62.6|↓14%|26.1|↑**53%**|↑**58%**|15.1|↑**73%**|↑**76%**|↑**42%**|
||55.2|Examples|52.4|↑**5%**|43.3|↑**21%**|↑**17%**|2_._0|↑**96%**|↑**96%**|↑**96%**|
|||Mixed|76.8|↓39%|36.9|↑**33%**|↑**52%**|19.4|↑**65%**|↑**75%**|↑**47%**|
|Llama||Rules|61.0|↑**25%**|46.6|↑**43%**|↑**24%**|54.7|↑**33%**|↑**10%**|↓17%|
||81.5|Examples|59.7|↑**27%**|15.7|↑**81%**|↑**74%**|35.3|↑**57%**|↑**41%**|↓125%|
|||Mixed|40.6|↑**50%**|25.6|↑**69%**|↑**37%**|9_._3|↑**89%**|↑**77%**|↑**64%**|
|Qwen||Rules|83.5|↑**4%**|21.0|↑**76%**|↑**75%**|2.6|↑**97%**|↑**97%**|↑**88%**|
||87.3|Examples|69.5|↑**20%**|35.8|↑**59%**|↑**48%**|2_._3|↑**97%**|↑**97%**|↑**94%**|
|||Mixed|89.4|↓2%|20.4|↑**77%**|↑**77%**|2.8|↑**97%**|↑**97%**|↑**86%**|



**Table 7: Experimental Setup Summary** 

|**Component**|**Description**|
|---|---|
|**Models**|Gemini-2.5-Flash-Lite, Grok-4-Fast, Llama-4-Maverick, Qwen3-235B|
|**Conditions**|**Zero-Shot**: No adaptation (empty memory)<br>**Rules**: Contextual Instructions (Textual guidelines)<br>**Examples**: Few-shot Demonstrations (State-Action pairs)<br>**Mixed**: Combined Rules and Examples|
|**Methods**|**FORGE**: Population-based continual learning (champion broadcast)<br>**Refexion**: Single-instance learning (no population broadcast)|
|**Key Metrics**|**Evaluation Reward**: Cumulative reward per episode (Higher is better)<br>**Graduation Rate**: % of learning stages successfully completed<br>**Token Efciency**: Total tokens processed to reach performance<br>**Volatility**: Standard deviation of rewards across stages|
|**Scale**|Zero-Shot: 5 experiments, 270 episodes<br>Refexion: 38 experiments, 1,000 episodes<br>FORGE: 49 experiments, 890 episodes<br>FORGE w/o grad: 24 experiments, 480 episodes<br>**Total**: 116 experiments, 2,640 episodes, 12364.0M tokens|



## **E.3 Computational Cost Breakdown** 

Table 11 breaks down token consumption by phase (Adaptation vs. Evaluation), providing transparency into the computational cost structure of the protocol. 

## **E.4 Baseline (Zero-Shot) Evaluation** 

Table 12 reports zero-shot evaluation scores for all models. 

## **F Raw Evaluation Scores** 

Tables 15–16 report post-session evaluation scores for trained agents under the Best transfer protocol. 

This appendix provides complete per-instance, per-run evaluation scores for all 2,640 evaluated episodes across 116 experiments. These raw data support the aggregate statistics reported in Table 3 and enable full transparency regarding variances, outliers, and tail 

ACM CAIS ’26, May 26–29, 2026, San Jose, CA, USA 

Bogdanov et al. 

Planner rules: 

- When lateral movement is confirmed, then Plan: Isolate path + Analyse adjacent hosts 

- When reconnaissance is confirmed on an Enterprise host, then Plan: Deploy DecoySERVICE immediately 

- When a host has undergone two consecutive Analyses and remains in changed state with high severity, then Plan: Execute Remove or Restore 

Analyst rules: 

- When Analyse confirms C2 beaconing, then Recommend Deploy DecoySERVICE on Server host 

- When multiple critical anomalies are present, then set recommended_focus to 'containment' 

### **Figure 9: Rules artifact generated by the Reflector after a failed episode. Each rule is a conditional heuristic injected into the agent’s system prompt.** 

- <example description='PlanMonitorAndDecoy AfterReconAnalysis'> 

- Thought: Enterprise_Host shows signs of reconnaissance from 10.0.247.46. Per reflection knowledge, plan monitoring and decoy deployment. 

- Tool: get_suggestion_for_next_action: {"target_host": "Enterprise_Host", "situation": "recon confirmed", "severity": "high", ...} 

- PAUSE Observation: [ {"action": "Monitor", "confidence": 0.95}, 

- {"action": "DecoySSHD hostname=Enterprise_Host", 

- "confidence": 0.90}, ...] 

- Thought: Monitoring and decoy deployment are highest-priority. 

- Answer: Monitor 

- </example> 

**Figure 10: Examples artifact generated by the Exemplifier after a failed episode (abbreviated). The demonstration mimics a full ReAct interaction cycle.** 

**Table 8: Reflexion baseline evaluation detail.** _𝑁_ **= independent instances evaluated (each runs the Reflexion loop in isolation; no cross-instance interaction). Failure rate = episodes with return** _<_ −100 **.** 

|**Model**|**Repr**|_𝑁_|**Mean**|**SD**|**Failure Rate (**_<_ −100**)**|
|---|---|---|---|---|---|
|Gemini|Rules|70|−62_._7|60.5|21%|
||Examples|50|−78_._9|60.4|28%|
||Mixed|50|−81_._9|74.6|36%|
|Grok|Rules|30|−79_._9|62.6|33%|
||Examples|30|−64_._8|52.4|27%|
||Mixed|30|−114_._4|76.8|50%|
|Llama|Rules|70|−101_._4|61.0|50%|
||Examples|30|−53_._9|59.7|17%|
||Mixed|30|−44_._2|40.6|17%|
|Qwen|Rules|30|−88_._4|83.5|33%|
||Examples|30|−57_._6|69.5|23%|
||Mixed|50|−80_._4|89.4|28%|



**Table 9: Flash-Lite Session Results: Rules vs Examples vs Mixed (FORGE). Avg = mean eval return across 10 instances in that session (** ± **within-session SD).** 

|**Repr**|**Session**|**Avg Return**|**Grad**|**Tokens**|
|---|---|---|---|---|
|Rules|1|-19.86±15.9|10/10|4.7M|
||2|-47.80±34.8|6/10|8.8M|
||3|-21.76±11.2|10/10|6.2M|
||4|-16.26±3.7|7/10|8.4M|
||5|-28.24±41.2|7/10|9.0M|
||6|-50.20±65.4|10/10|6.2M|
||7|-29.85±41.1|8/10|7.5M|
||**Mean**|-30.57±13.4|8.3/10|7.3M±1.6M|
|Examples|1|-28.73±20.4|7/10|8.3M|
||2|-18.72±13.7|9/10|8.6M|
||3|-24.24±15.0|10/10|6.0M|
||4|-23.18±18.7|9/10|6.7M|
||5|-36.11±38.1|8/10|9.3M|
||6|-24.45±21.8|8/10|10.5M|
||7|-16.01±4.1|10/10|9.4M|
||**Mean**|-24.49±6.6|8.7/10|8.4M±1.6M|
|Mixed|1|-20.04±13.3|8/10|11.4M|
||2|-38.67±18.4|7/10|12.6M|
||3|-42.06±52.9|9/10|8.3M|
||4|-34.37±16.4|6/10|11.4M|
||5|-38.46±36.8|7/10|8.4M|
||6|-27.43±18.0|7/10|10.1M|
||7|-24.36±18.5|10/10|8.8M|
||**Mean**|-32.20±8.3|7.7/10|10.2M±1.7M|



**Table 10: Graduation Stage Distribution** 

|**Model**|**Representation**|**S1**|**S2**|**S3**|**S4**|**S5**|**S6**|**Never**|
|---|---|---|---|---|---|---|---|---|
|Gemini|rules|12|8|16|7|9|6|12|
|Gemini|examples|6|13|16|13|5|8|9|
|Gemini|mixed|10|12|12|9|8|3|16|
|Grok|rules|3|8|8|3|2|2|4|
|Grok|examples|7|9|2|4|1|1|6|
|Grok|mixed|5|9|6|2|4|0|4|
|Llama|rules|1|2|2|3|0|2|20|
|Llama|examples|1|3|1|5|3|2|15|
|Llama|mixed|4|4|1|4|0|4|13|
|Qwen3|rules|5|4|2|2|3|5|19|
|Qwen3|examples|6|4|2|6|5|4|3|
|Qwen3|mixed|3|3|1|1|1|0|21|



behavior. Each table reports episode returns ( _𝑅_ =<sup>�</sup> _𝑡_<sup>30</sup> =1<sup>_𝑟𝑡_)with</sup> learning disabled (frozen evaluation). Column headers E1, E2, etc., denote independent evaluation runs; "—" indicates no data for that run. 

_Summary._ The raw data reveal three key patterns supporting the main text claims: (1) baseline distributions are heavy-tailed with frequent catastrophic failures; (2) FORGE Protocol training substantially compresses this variance and elevates the returns of most instances into the −10 to −50 range; and (3) Reflexion exhibits higher instability, with several instances regressing to near-baseline performance. These complete data are provided for reproducibility and to enable meta-analyses of representation-specific failure modes. 

ACM CAIS ’26, May 26–29, 2026, San Jose, CA, USA 

FORGE: Self-Evolving Agent Memory With No Weight Updates 


![](P014_images/P014.pdf-0015-02.png)


**Figure 11: Failure trigger threshold analysis. (Left) Per-step penalty distribution across zero-shot episodes (log scale). The red bar at** −1 _._ 0 **represents legitimate Restore actions; blue bars are real failures. (Right) Triggers captured vs. threshold:** _𝜏_ = −1 _._ 1 **captures 7,346 real triggers with 0 false positives.** 

**Table 11: Average Token Usage per Instance (Adaptation Phase, FORGE & Reflexion)** 

|**Model**|**Method**|**Representation**|**Avg Total/inst**|**Avg Prompt/inst**|**Avg Compl/inst**|**P/C Ratio**|
|---|---|---|---|---|---|---|
|Gemini|FORGE<br>|Rules|**7.3M**±**1.6M**|6.4M|0.8M|7.8|
|Gemini|Refexion|Rules|11.4M±0.5M|10.1M|1.3M|7.9|
|Gemini|FORGE<br>|Examples|8.4M±1.6M|7.7M|0.7M|10.4|
|Gemini|Refexion|Examples|13.1M±0.4M|12.1M|1.0M|11.7|
|Gemini|FORGE|Mixed|10.2M±1.7M|9.2M|0.9M|10.0|
|Gemini|Refexion|Mixed|17.0M±0.5M|15.8M|1.2M|13.2|
|Grok|FORGE<br>|Rules|**4.7M**±**0.9M**|3.8M|0.9M|4.2|
|Grok|Refexion|Rules|8.8M±0.5M|7.2M|1.6M|4.4|
|Grok|FORGE|Examples|8.4M±4.0M|7.5M|0.9M|8.3|
|Grok|Refexion|Examples|17.3M±0.9M|15.5M|1.8M|8.8|
|Grok|FORGE|Mixed|9.3M±1.3M|8.2M|1.1M|7.3|
|Grok|Refexion|Mixed|19.9M±0.8M|17.9M|2.0M|8.9|
|Llama|FORGE<br>|Rules|5.1M±0.2M|4.8M|0.3M|17.2|
|Llama|Refexion|Rules|5.5M±0.8M|5.2M|0.3M|17.0|
|Llama|FORGE|Examples|**4.6M**±**0.8M**|4.4M|0.2M|23.1|
|Llama|Refexion|Examples|5.7M±0.2M|5.5M|0.2M|23.5|
|Llama|FORGE|Mixed|5.5M±0.9M|5.3M|0.2M|23.8|
|Llama|Refexion|Mixed|7.4M±0.0M|7.1M|0.3M|25.7|
|Qwen3|FORGE|Rules|**5.1M**±**1.2M**|4.8M|0.2M|22.3|
|Qwen3|Refexion|Rules|5.8M±0.4M|5.6M|0.2M|22.8|
|Qwen3|FORGE|Examples|5.1M±1.6M|4.9M|0.2M|23.0|
|Qwen3|Refexion|Examples|9.8M±0.5M|9.4M|0.3M|27.3|
|Qwen3|FORGE|Mixed|7.3M±3.8M|7.1M|0.2M|32.6|
|Qwen3|Refexion|Mixed|9.6M±0.2M|9.3M|0.3M|31.9|



## **G Per-Run Detailed Results** 

This section provides session-level summaries for all experiments, aggregating the raw evaluation data from Appendix F into persession metrics. Table 13, Table 14, Table 17 and Table 18 list average return, total token cost, and graduation counts for each training run, enabling direct comparison of resource efficiency across configurations. 

## **G.1 Learning Dynamics: Per-Stage Checkpoint Progression** 

Tables 19–20 report checkpoint returns at each stage (S1-S6) during training, computed by averaging the frozen checkpoint scores 

across all instances. Under the Best protocol (Table 19), most configurations exhibit progressive improvement or stabilization across stages. For example, Gemini Rules converges from −93 _._ 7 (S1) to −27 _._ 7 (S5), while Qwen3 Examples rapidly stabilizes by S2 (−22 _._ 3). Notable exceptions include Grok Rules, which experiences latestage regression (S4–S6 ≈−224), reflecting rare failure cascades despite earlier success. 

Under the Reflexion baseline (Table 20), learning trajectories are more erratic. Without champion broadcast, instances often regress between stages (e.g., Gemini Examples degrades from S5 to S6, while Qwen3 Mixed consistently worsens from S2 onward). Comparing the “Final” columns across protocols confirms that FORGE achieves systematically better post-session evaluation performance than 

ACM CAIS ’26, May 26–29, 2026, San Jose, CA, USA 

Bogdanov et al. 

**Table 12: Raw Evaluation Scores: Zero-Shot (All Models)** 

|**Model**<br>**Instance**<br>**S1**|
|---|
|Gemini<br>instance_1<br>-215.10|
|instance_2<br>-205.84|
|instance_3<br>-171.80|
|instance_4<br>-200.23|
|instance_5<br>-198.80|
|instance_6<br>-182.64|
|instance_7<br>-174.09|
|instance_8<br>-183.83|
|instance_9<br>-171.19|
|instance_10<br>-192.60|
|**Model**<br>**Instance**<br>**S1**<br>**S2**|
|Grok<br>instance_1<br>-93.92<br>-31.84|
|instance_2<br>-62.18<br>-64.32|
|instance_3<br>-83.82<br>-86.48|
|instance_4<br>-51.84<br>-28.00|
|instance_5<br>-33.50<br>-16.46|
|instance_6<br>-58.64<br>-51.70|
|instance_7<br>-89.34<br>-116.58|
|instance_8<br>-77.94<br>-35.76|
|instance_9<br>-52.30<br>-43.00|
|instance_10<br>-57.58<br>-33.66|
|**Model**<br>**Instance**<br>**S1**|
|Llama<br>instance_1<br>-113.34|
|instance_2<br>-111.98|
|instance_3<br>-92.24|
|instance_4<br>-184.46|
|instance_5<br>-122.64|
|instance_6<br>-140.82|
|instance_7<br>-113.66|
|instance_8<br>-104.24|
|instance_9<br>-60.48|
|instance_10<br>-87.24|
|**Model**<br>**Instance**<br>**S1**|
|Qwen3<br>instance_1<br>-88.48|
|instance_2<br>-97.98|
|instance_3<br>-94.80|
|instance_4<br>-103.26|
|instance_5<br>-60.58|
|instance_6<br>-73.00|
|instance_7<br>-152.06|
|instance_8<br>-83.60|
|instance_9<br>-180.50|
|instance_10<br>-99.16|



**Table 13: Complete Experimental Results: Llama** 

|**#**|**Method**|**Representation**|**Avg Reward**|**Tokens**|**Graduated**|
|---|---|---|---|---|---|
|1|FORGE|Examples|-33.12|5.5M|2/10|
|2|FORGE|Examples|-19.16|4.3M|8/10|
|3|FORGE|Examples|-32.62|4.0M|5/10|
|4|FORGE|Mixed|-27.82|5.4M|5/10|
|5|FORGE|Mixed|-36.96|4.7M|7/10|
|6|FORGE|Mixed|-23.91|6.5M|5/10|
|7|FORGE|Rules|-92.59|5.1M|4/10|
|8|FORGE|Rules|-82.50|5.3M|1/10|
|9|FORGE|Rules|-40.78|5.0M|5/10|
|10|Refexion|Examples|-48.07|5.8M|—|
|11|Refexion|Examples|-65.69|5.5M|—|
|12|Refexion|Mixed|-46.81|7.4M|—|
|13|Refexion|Mixed|-39.11|7.4M|—|
|14|Refexion|Rules|-63.32|7.0M|—|
|15|Refexion|Rules|-113.69|5.3M|—|
|16|Refexion|Rules|-88.19|5.3M|—|
|17|Refexion|Rules|-121.42|5.2M|—|
|18|Zero-Shot|—|-113.11|0.4M|—|



**Table 14: Complete Experimental Results: Qwen3** 

|**#**|**Method**|**Representation**|**Avg Reward**|**Tokens**|**Graduated**|
|---|---|---|---|---|---|
|1|FORGE|Examples|-17.04|6.1M|9/10|
|2|FORGE|Examples|-20.22|5.8M|9/10|
|3|FORGE|Examples|-35.58|3.3M|9/10|
|4|FORGE|Mixed|-47.82|11.6M|2/10|
|5|FORGE|Mixed|-19.41|5.9M|3/10|
|6|FORGE|Mixed|-20.70|4.3M|4/10|
|7|FORGE|Rules|-34.67|6.6M|2/10|
|8|FORGE|Rules|-26.99|4.9M|2/10|
|9|FORGE|Rules|-21.62|5.1M|9/10|
|10|FORGE|Rules|-17.35|3.6M|8/10|
|11|Refexion|Examples|-56.15|10.0M|—|
|12|Refexion<br>|Examples|-60.41|9.3M|—|
|13|Refexion<br>|Mixed|-69.15|9.5M|—|
|14|Refexion<br>|Mixed|-125.41|9.9M|—|
|15|Refexion|Rules|-86.19|6.1M|—|
|16|Refexion|Rules|-89.48|5.6M|—|
|17|Zero-Shot|—|-103.34|0.4M|—|



**Table 15: Raw Evaluation Scores: Gemini Flash-Lite, FORGE** 

|**Repr**|**Instance**|**S1**|**S2**|**S3**|**S4**|**S5**|**S6**|**S7**|
|---|---|---|---|---|---|---|---|---|
|Rules|instance_1|-64.90|-73.30|-18.20|-14.60|-18.10|-69.50|-17.50|
||instance_2|-16.20|-18.20|-15.20|-13.20|-14.20|-25.20|-13.20|
||instance_3|-13.20|-39.40|-13.30|-17.20|-13.20|-13.30|-15.20|
||instance_4|-15.30|-108.20|-36.20|-25.40|-14.20|-14.50|-22.00|
||instance_5|-12.40|-100.00|-12.50|-16.20|-12.20|-14.10|-17.70|
||instance_6|-15.60|-37.20|-18.20|-18.20|-14.10|-15.50|-15.70|
||instance_7|-14.20|-49.80|-43.20|-13.70|-20.80|-12.40|-146.50|
||instance_8|-16.20|-15.50|-14.70|-15.20|-15.60|-38.30|-14.30|
||instance_9|-16.60|-22.10|-32.70|-16.50|-145.30|-223.80|-17.20|
||instance_10|-14.00|-14.30|-13.40|-12.40|-14.70|-75.40|-19.20|
|Examples|instance_1|-15.20|-13.40|-46.80|-14.30|-36.60|-27.40|-26.20|
||instance_2|-60.80|-13.20|-16.50|-14.20|-14.40|-16.60|-15.40|
||instance_3|-15.60|-17.30|-14.00|-63.50|-14.60|-27.50|-17.30|
||instance_4|-15.50|-15.40|-40.20|-14.20|-135.50|-12.20|-15.20|
||instance_5|-13.90|-57.40|-49.30|-14.40|-13.90|-18.30|-13.30|
||instance_6|-13.70|-13.40|-15.60|-14.80|-15.40|-13.60|-14.30|
||instance_7|-63.10|-15.60|-21.40|-53.20|-14.20|-13.50|-15.20|
||instance_8|-14.90|-16.50|-13.40|-15.20|-53.00|-17.20|-11.40|
||instance_9|-27.10|-13.10|-12.40|-13.40|-15.20|-13.60|-13.50|
||instance_10|-47.50|-11.90|-12.80|-14.60|-48.30|-84.60|-18.30|
|Mixed|instance_1|-17.85|-31.80|-27.40|-16.20|-10.70|-68.00|-23.70|
||instance_2|-14.65|-79.70|-76.35|-48.25|-13.70|-15.30|-15.05|
||instance_3|-14.20|-19.25|-17.05|-42.95|-14.25|-17.50|-17.90|
||instance_4|-55.70|-45.75|-14.70|-16.35|-14.85|-13.50|-50.25|
||instance_5|-14.25|-30.00|-28.40|-35.75|-15.45|-16.40|-14.35|
||instance_6|-13.45|-52.85|-25.45|-50.30|-88.05|-45.80|-66.20|
||instance_7|-27.95|-44.75|-16.75|-15.90|-30.65|-11.00|-13.90|
||instance_8|-15.05|-17.75|-15.45|-21.85|-107.20|-36.55|-13.30|
||instance_9|-13.50|-27.20|-15.75|-34.25|-14.75|-21.70|-14.75|
||instance_10|-13.80|-37.70|-183.25|-61.85|-75.00|-28.55|-14.25|



## **H Reflexion Baseline Raw Scores** 

Tables 21–22 present evaluation scores under the Reflexion baseline, where each instance evolves memory from its own trajectories without cross-instance propagation. 

_Gemini Reflexion._ Table 21 reports Gemini scores under the Reflexion baseline where cross-instance transfer is disabled. Each of the three memory representations (Rules/Examples/Mixed) received 2 evaluation runs. 

Reflexion for most configurations, with particularly large gaps for weaker baseline models (Qwen, Llama). 

ACM CAIS ’26, May 26–29, 2026, San Jose, CA, USA 

FORGE: Self-Evolving Agent Memory With No Weight Updates 

**Table 16: Raw Evaluation Scores: FORGE (Grok, Llama, Qwen)** 

|**Model**|**Instance**||**Rul**|**es**|||**Examples**|||**Mixed**||
|---|---|---|---|---|---|---|---|---|---|---|---|
|||**S1**|**S2**|**S3**|**S4**|**S1**|**S2**|**S3**|**S1**|**S2**|**S3**|
|Grok|instance_1|-39.10|-45.60|-14.00|—|-125.35|-16.55|-14.55|-14.70|-18.10|-29.80|
||instance_2|-14.30|-28.00|-39.40|—|-44.80|-17.85|-14.30|-81.40|-79.85|-13.55|
||instance_3|-144.65|-39.35|-32.85|—|-141.80|-46.35|-15.05|-33.40|-114.50|-18.00|
||instance_4|-32.00|-14.95|-43.40|—|-132.70|-26.15|-37.75|-21.70|-43.20|-16.30|
||instance_5|-34.00|-13.65|-13.60|—|-46.15|-41.30|-13.80|-15.60|-71.60|-14.70|
||instance_6|-13.55|-30.05|-52.35|—|-16.30|-13.85|-15.25|-79.15|-31.85|-41.35|
||instance_7|-15.80|-18.20|-15.35|—|-128.20|-15.45|-14.70|-44.75|-38.50|-46.25|
||instance_8|-49.30|-71.60|-12.35|—|-62.05|-16.45|-15.60|-38.60|-16.70|-14.70|
||instance_9|-14.80|-15.15|-36.90|—|-49.60|-13.35|-13.20|-165.45|-103.50|-14.80|
||instance_10|-36.20|-24.55|-56.35|—|-136.95|-20.90|-13.60|-14.20|-16.75|-14.15|
|Llama|instance_1|-138.40|-37.40|-109.65|—|-56.85|-16.40|-13.70|-13.85|-15.45|-19.50|
||instance_2|-104.83|-62.30|-36.40|—|-21.90|-16.30|-26.30|-18.20|-13.90|-15.20|
||instance_3|-108.60|-42.45|-25.40|—|-44.20|-16.75|-21.80|-27.65|-34.25|-16.20|
||instance_4|-129.01|-192.05|-22.05|—|-26.80|-20.70|-23.25|-15.20|-24.75|-89.00|
||instance_5|-52.69|-149.15|-20.05|—|-27.00|-27.05|-65.50|-26.50|-18.80|-15.55|
||instance_6|-120.97|-76.20|-38.75|—|-26.30|-19.85|-40.05|-18.85|-106.70|-14.50|
||instance_7|-125.31|-15.20|-33.65|—|-32.95|-29.55|-17.95|-19.85|-12.65|-14.85|
||instance_8|-51.94|-80.00|-50.60|—|-20.50|-14.20|-29.05|-95.65|-42.60|-15.60|
||instance_9|-20.41|-51.10|-40.45|—|-20.50|-15.30|-14.90|-27.25|-68.35|-24.60|
||instance_10|-73.76|-119.20|-30.85|—|-54.20|-15.50|-73.75|-15.20|-32.15|-14.15|
|Qwen3|instance_1|-24.50|-28.40|-18.00|-14.35|-14.85|-16.70|-212.35|-36.20|-17.10|-16.75|
||instance_2|-18.30|-17.55|-68.35|-15.90|-15.15|-16.70|-13.80|-39.95|-20.65|-18.80|
||instance_3|-127.70|-22.60|-17.50|-15.80|-20.40|-19.00|-15.00|-119.55|-22.60|-22.90|
||instance_4|-25.10|-21.80|-15.00|-15.60|-19.60|-32.45|-14.95|-46.50|-15.70|-18.75|
||instance_5|-15.05|-19.55|-16.75|-14.75|-17.35|-34.85|-16.25|-43.15|-17.55|-17.25|
||instance_6|-18.10|-71.65|-16.35|-17.35|-20.65|-16.05|-16.60|-31.10|-21.60|-19.75|
||instance_7|-52.25|-22.55|-14.25|-22.70|-16.45|-21.55|-15.90|-45.05|-24.70|-20.25|
||instance_8|-30.90|-24.05|-16.10|-24.25|-15.70|-15.30|-14.25|-17.45|-18.80|-35.15|
||instance_9|-19.90|-22.20|-19.80|-18.70|-16.45|-14.10|-20.75|-52.10|-16.15|-16.70|
||instance_10|-14.85|-19.55|-14.05|-14.10|-13.75|-15.50|-15.95|-47.15|-19.25|-20.65|



**Table 18: Complete Experimental Results: Grok** 

**Table 17: Complete Experimental Results: Gemini Flash-Lite** 

|**#**|**Method**|**Representation**|**Avg Reward**|**Tokens**|**Graduated**|
|---|---|---|---|---|---|
|1|FORGE|Examples|-88.39|12.2M|4/10|
|2|FORGE|Examples|-22.82|4.1M|10/10|
|3|FORGE|Examples|-16.78|9.0M|10/10|
|4|FORGE|Mixed|-50.89|8.0M|9/10|
|5|FORGE|Mixed|-53.45|10.7M|7/10|
|6|FORGE|Mixed|-22.36|9.1M|10/10|
|7|FORGE|Rules|-39.37|3.7M|9/10|
|8|FORGE|Rules|-30.11|4.9M|8/10|
|9|FORGE|Rules|-31.65|5.5M|9/10|
|10|Refexion<br>|Examples|-67.09|16.3M|—|
|11|Refexion<br>|Examples|-65.44|17.8M|—|
|12|Refexion<br>|Examples|-61.76|17.8M|—|
|13|Refexion<br>|Mixed|-111.75|20.6M|—|
|14|Refexion<br>|Mixed|-118.07|19.1M|—|
|15|Refexion<br>|Mixed|-113.24|20.1M|—|
|16|Refexion<br>|Rules|-100.22|8.6M|—|
|17|Refexion|Rules|-72.60|9.4M|—|
|18|Refexion|Rules|-66.95|8.4M|—|
|19|Zero-Shot|—|-66.11|0.5M|—|
|20|Zero-Shot|—|-50.78|0.5M|—|



|**#**|**Method**|**Representation**|**Avg Reward**|**Tokens**|**Graduated**|
|---|---|---|---|---|---|
|1|FORGE|Examples<br>|-28.73|8.3M|7/10|
|2|FORGE|Examples<br>|-18.72|8.6M|9/10|
|3|FORGE|Examples|-24.24|6.0M|10/10|
|4|FORGE|Examples<br>|-23.18|6.7M|9/10|
|5|FORGE|Examples|-36.11|9.3M|8/10|
|6|FORGE|Examples|-24.45|10.5M|8/10|
|7|FORGE|Examples|-16.01|9.4M|10/10|
|8|FORGE|Mixed|-20.04|11.4M|8/10|
|9|FORGE|Mixed<br>|-38.67|12.6M|7/10|
|10|FORGE|Mixed|-42.06|8.3M|9/10|
|11|FORGE|Mixed|-34.37|11.4M|6/10|
|12|FORGE|Mixed|-38.46|8.4M|7/10|
|13|FORGE|Mixed|-27.43|10.1M|7/10|
|14|FORGE|Mixed|-24.36|8.8M|10/10|
|15|FORGE|Rules<br>|-19.86|4.7M|10/10|
|16|FORGE|Rules|-47.80|8.8M|6/10|
|17|FORGE|Rules|-21.76|6.2M|10/10|
|18|FORGE|Rules|-16.26|8.4M|7/10|
|19|FORGE|Rules|-28.24|9.0M|7/10|
|20|FORGE|Rules|-50.20|6.2M|10/10|
|21|FORGE|Rules|-29.85|7.5M|8/10|
|22|Refexion|Examples|-58.60|13.0M|—|
|23|Refexion<br>|Examples|-77.38|12.5M|—|
|24|Refexion|Examples|-102.35|13.4M|—|
|25|Refexion<br>|Examples|-53.70|13.3M|—|
|26|Refexion|Mixed|-63.05|16.6M|—|
|27|Refexion<br>|Mixed|-71.89|17.8M|—|
|28|Refexion|Mixed|-82.00|16.8M|—|
|29|Refexion<br>|Mixed|-110.60|16.9M|—|
|30|Refexion|Rules|-34.42|11.6M|—|
|31|Refexion<br>|Rules|-48.01|11.2M|—|
|32|Refexion|Rules|-96.88|11.6M|—|
|33|Refexion|Rules|-66.29|12.5M|—|
|34|Refexion|Rules|-84.29|11.0M|—|
|35|Refexion<br>|Rules|-77.06|11.3M|—|
|36|Refexion|Rules|-31.73|10.7M|—|
|37|Zero-Shot|—|-189.61|0.5M|—|



ACM CAIS ’26, May 26–29, 2026, San Jose, CA, USA 

Bogdanov et al. 

**Table 19: Per-Stage Checkpoint Rewards (FORGE, All Models)** 

|**Model**|**Representation**|**S1**|**S2**|**S3**|**S4**|**S5**|**S6**|**Final**|
|---|---|---|---|---|---|---|---|---|
|Gemini|rules|-93.74±84.8|-55.16±63.6|-43.31±63.3|-49.79±62.8|-27.73±40.8|-43.88±57.3|-30.57±37.0|
|Gemini|examples|-90.33±78.9|-46.01±51.8|-28.32±26.1|-23.36±21.6|-45.20±65.2|-27.45±20.9|-24.49±21.1|
|Gemini|mixed|-97.12±82.5|-71.32±72.2|-45.83±53.9|-62.50±68.6|-70.24±73.4|-62.10±73.4|-32.20±34.6|
|Grok|rules|-120.10±79.4|-42.29±50.9|-47.07±57.6|-43.39±61.7|-48.49±71.5|-51.75±61.1|-33.71±32.8|
|Grok|examples|-88.97±85.9|-83.18±89.6|-97.10±92.4|-57.92±52.3|-109.28±82.4|-114.13±60.5|-42.66±54.1|
|Grok|mixed|-139.28±82.8|-32.21±43.8|-55.71±72.4|-47.69±59.1|-63.44±68.3|-134.65±59.3|-42.24±44.5|
|Llama|rules|-99.43±83.7|-86.97±78.4|-68.36±70.2|-75.38±69.9|-78.69±77.1|-89.58±75.6|-81.34±76.5|
|Llama|examples|-73.62±68.1|-56.81±61.6|-46.77±41.8|-44.04±46.4|-46.58±52.2|-30.71±26.3|-28.30±22.3|
|Llama|mixed|-67.14±74.8|-60.11±64.6|-42.92±32.3|-27.91±16.8|-90.59±72.0|-43.40±68.0|-29.57±37.6|
|Qwen3|rules|-82.60±86.6|-70.50±80.2|-41.61±54.6|-34.70±46.9|-37.00±45.2|-33.25±43.2|-25.16±30.5|
|Qwen3|examples|-49.42±62.8|-22.78±18.5|-23.43±27.9|-35.04±51.9|-41.68±65.2|-44.86±79.4|-24.28±36.1|
|Qwen3|mixed|-74.77±79.5|-63.03±74.9|-72.81±78.8|-45.27±52.3|-45.47±54.5|-40.29±37.4|-29.31±23.1|



**Table 20: Per-Stage Checkpoint Rewards (Reflexion, All Models)** 

|**Model**|**Representation**|**S1**|**S2**|**S3**|**S4**|**S5**|**S6**|**Final**|
|---|---|---|---|---|---|---|---|---|
|Gemini|rules|-82.75±80.3|-92.69±84.4|-74.49±72.9|-71.64±76.2|-89.30±136.5|-67.74±73.1|-62.67±69.2|
|Gemini|examples|-115.00±83.4|-107.55±77.4|-85.93±71.9|-83.23±73.5|-76.66±74.9|-89.64±75.2|-78.88±71.6|
|Gemini|mixed|-116.16±85.3|-110.89±87.1|-93.21±83.6|-106.12±84.3|-80.95±82.1|-81.47±81.6|-81.91±80.1|
|Grok|rules|-106.42±89.7|-93.64±85.2|-83.54±69.1|-79.27±72.0|-91.54±77.6|-97.76±66.5|-79.92±73.0|
|Grok|examples|-85.56±84.1|-80.56±72.7|-78.12±69.5|-67.28±62.0|-81.71±76.1|-56.60±59.5|-64.76±66.7|
|Grok|mixed|-107.05±90.5|-60.00±60.9|-79.84±69.6|-120.35±82.8|-113.72±85.4|-107.11±79.4|-114.35±81.6|
|Llama|rules|-84.84±78.3|-100.55±73.3|-81.14±73.9|-83.23±73.2|-95.30±77.5|-87.73±77.6|-101.42±77.6|
|Llama|examples|-80.95±79.6|-67.70±61.1|-98.51±78.3|-63.47±63.0|-77.85±71.9|-49.66±62.9|-53.95±64.8|
|Llama|mixed|-60.04±69.9|-75.45±79.5|-65.17±68.2|-55.68±59.1|-37.64±43.1|-58.96±61.7|-44.24±51.1|
|Qwen3|rules|-56.77±65.9|-68.90±81.1|-88.17±91.4|-78.50±90.6|-84.23±86.0|-97.83±94.5|-88.38±86.4|
|Qwen3|examples|-76.81±79.4|-43.70±52.0|-54.92±72.0|-52.81±68.8|-64.06±75.0|-54.48±73.6|-57.57±71.3|
|Qwen3|mixed|-72.06±84.5|-75.34±82.5|-83.01±90.5|-90.80±93.8|-86.43±92.6|-80.61±89.6|-80.40±89.3|



**Table 21: Raw Evaluation Scores: Gemini Flash-Lite, Reflexion** 

|**Instance**||||**Rules**|||||**Exam**|**ples**|||**Mi**|**xed**||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||**S1**|**S2**|**S3**|**S4**|**S5**|**S6**|**S7**|**S1**|**S2**|**S3**|**S4**|**S1**|**S2**|**S3**|**S4**|
|instance_1|-13.90|-17.30|-210.70|-210.70|-181.10|-47.80|-13.80|-25.80|-28.30|-88.55|-94.60|-15.60|-54.30|-33.05|-92.85|
|instance_2|-27.35|-177.90|-14.85|-15.75|-16.80|-74.45|-35.15|-142.50|-222.55|-99.50|-18.35|-207.50|-223.35|-14.40|-17.80|
|instance_3|-32.40|-110.30|-31.00|-14.10|-37.45|-31.70|-36.60|-57.95|-37.85|-42.20|-94.80|-13.75|-14.10|-21.70|-36.85|
|instance_4|-15.75|-13.30|-211.20|-29.45|-45.90|-15.15|-16.20|-65.25|-15.10|-161.80|-33.45|-177.90|-106.75|-183.40|-176.70|
|instance_5|-18.90|-33.85|-49.80|-19.70|-15.20|-16.45|-16.35|-112.75|-222.70|-17.40|-15.95|-15.80|-146.55|-224.20|-15.35|
|instance_6|-31.70|-13.85|-86.60|-117.75|-223.80|-120.60|-71.70|-14.20|-143.55|-182.90|-15.60|-24.50|-33.20|-34.50|-163.05|
|instance_7|-15.15|-29.25|-128.95|-118.85|-14.85|-80.00|-16.85|-36.20|-34.90|-118.25|-24.00|-13.85|-38.30|-30.20|-215.20|
|instance_8|-59.45|-14.25|-108.50|-93.00|-18.60|-134.90|-74.80|-32.25|-17.55|-37.25|-119.30|-108.50|-69.95|-27.75|-82.10|
|instance_9|-69.20|-55.40|-45.35|-20.20|-98.20|-204.60|-21.65|-37.70|-14.80|-224.25|-38.40|-33.30|-14.60|-110.95|-132.05|
|instance_10|-60.40|-14.70|-81.85|-23.35|-191.00|-45.00|-14.25|-61.45|-36.45|-117.95|-82.60|-19.85|-17.80|-100.30|-174.10|
|instance_11|—|—|—|—|—|—|—|—|—|-119.00|—|—|—|-38.70|—|
|instance_12|—|—|—|—|—|—|—|—|—|-223.80|—|—|—|-34.95|—|
|instance_13|—|—|—|—|—|—|—|—|—|-59.85|—|—|—|-30.15|—|
|instance_14|—|—|—|—|—|—|—|—|—|-55.25|—|—|—|-223.80|—|
|instance_15|—|—|—|—|—|—|—|—|—|-101.30|—|—|—|-38.35|—|
|instance_16|—|—|—|—|—|—|—|—|—|-82.35|—|—|—|-223.75|—|
|instance_17|—|—|—|—|—|—|—|—|—|-62.35|—|—|—|-28.80|—|
|instance_18|—|—|—|—|—|—|—|—|—|-82.85|—|—|—|-193.20|—|
|instance_19|—|—|—|—|—|—|—|—|—|-74.80|—|—|—|-14.45|—|
|instance_20|—|—|—|—|—|—|—|—|—|-95.40|—|—|—|-33.40|—|



ACM CAIS ’26, May 26–29, 2026, San Jose, CA, USA 

FORGE: Self-Evolving Agent Memory With No Weight Updates 

**Table 22: Raw Evaluation Scores: Reflexion (Grok, Llama, Qwen)** 

|**Model**|**Instance**||**Rul**|**es**|||**Examples**|||**Mixed**||
|---|---|---|---|---|---|---|---|---|---|---|---|
|||**S1**|**S2**|**S3**|**S4**|**S1**|**S2**|**S3**|**S1**|**S2**|**S3**|
|Grok|instance1|-15.05|-20.15|-13.95|—|-19.95|-97.30|-206.40|-53.85|-196.70|-91.40|
||_<br>instance_2<br>instance_3|-210.70<br>-46.50|-106.70<br>-110.70|-62.70<br>-21.55|—<br>—|-105.15<br>-162.45|-31.10<br>-22.70|-110.15<br>-14.85|-134.30<br>-41.90|-14.80<br>-38.50|-199.80<br>-172.30|
||instance_4<br>|-98.65<br>|-15.15<br>|-58.95<br>|—|-76.35<br>|-14.00<br>|-86.25<br>|-26.50<br>|-139.70<br>|-174.30<br>|
||instance_5|-217.75|-72.80|-13.00|—|-35.05|-105.25|-22.35|-165.60|-223.75|-22.30|
||instance_6|-15.40|-57.65|-83.60|—|-15.60|-39.40|-50.75|-59.70|-20.95|-136.35|
||instance_7<br>|-28.75<br>|-45.35<br>|-72.65<br>|—|-24.30<br>|-39.40<br>|-61.95<br>|-41.30<br>|-202.55<br>|-29.60<br>|
||instance_8<br>instance_9|-14.15<br>-190.45|-113.80<br>-101.80|-188.20<br>-121.40|—<br>—|-99.10<br>-17.75|-24.50<br>-130.25|-31.20<br>-13.05|-223.80<br>-146.75|-202.90<br>-54.20|-57.25<br>-224.30|
||instance_10|-164.75|-81.90|-33.45|—|-115.20|-150.45|-20.65|-223.80|-86.60|-24.80|
|Llama|instance_1|-16.20|-63.20|-113.60|-27.00|-14.50|-15.05|—|-13.45|-26.40|—|
||instance_2|-71.50|-132.30|-90.80|-23.60|-19.10|-14.00|—|-132.30|-93.05|—|
||instance_3<br>i|-29.40<br>|-166.55<br>|-196.30<br>|-114.10<br>|-17.25<br>|-37.35<br>|—|-16.55<br>|-103.70<br>|—|
||nstance_4<br>instance_5|-43.25<br>-108.60|-22.55<br>-56.20|-159.45<br>-218.70|-24.80<br>-143.60|-51.95<br>-14.15|-16.05<br>-122.35|—<br>—|-17.15<br>-69.95|-16.35<br>-12.80|—<br>—|
||instance6|-128.15|-149.80|-125.20|-168.60|-36.05|-18.95|—|-18.05|-36.20|—|
||_<br>instance_7<br>|-29.10|-174.05|-121.75|-225.65|-53.55|-89.30|—|-135.40|-42.15|—|
||instance_8|-173.35|-68.20|-34.45|-216.35|-48.30|-224.30|—|-38.35|-14.55|—|
||instance_9<br>|-18.85<br>|-37.15<br>|-112.05<br>|-127.50<br>|-31.00<br>|-106.20<br>|—|-27.95<br>|-22.55<br>|—|
||instance_10<br>|-14.80|-199.35<br>|-36.95<br>|-125.75<br>|-24.90<br>|-13.35|—|-13.95<br>|-23.30|—|
||instance_11|—|-138.05|-28.35|-96.45|-20.10|—|—|-20.30|—|—|
||instance12|—|-122.20|-80.85|-157.10|-31.05|—|—|-119.75|—|—|
||_<br>instance_13<br>|—|-224.15<br>|-40.25<br>|-82.75<br>|-179.70<br>|—|—|-15.55<br>|—|—|
||instance_14|—|-129.80|-66.55|-148.95|-16.75|—|—|-22.65|—|—|
||instance15|—|-28.10|-49.45|-54.85|-17.00|—|—|-29.70|—|—|
||_<br>instance_16<br>|—|-106.70<br>|-35.60<br>|-136.75<br>|-30.35<br>|—|—|-19.70<br>|—|—|
||instance_17|—|-75.10|-83.90|-210.40|-223.80|—|—|-13.90|—|—|
||instance18|—|-89.50|-43.25|-32.15|-34.00|—|—|-122.25|—|—|
||_<br>it19||12500|3380|13795|6270|||7225|||
||nsance_<br>instance_20|—<br>—|-.<br>-165.75|-.<br>-92.50|-.<br>-174.10|-.<br>-35.25|—<br>—|—<br>—|-.<br>-17.00|—<br>—|—<br>—|
|Qwen3|instance_1|-18.90|-20.30|—|—|-22.65|-17.60|—|-30.90|-212.20|—|
||instance_2<br>|-37.95<br>|-26.70<br>|—|—|-20.60<br>|-14.15<br>|—|-223.70<br>|-223.75<br>|—|
||instance_3<br>instance_4<br>instance5|-95.25<br>-23.55<br>-1695|-132.00<br>-21.30<br>-8515|—<br>—<br>—|—<br>—<br>—|-16.05<br>-184.95<br>-2165|-16.00<br>-14.00<br>-1635|—<br>—<br>—|-15.10<br>-224.35<br>-1565|-72.25<br>-19.35<br>-1800|—<br>—<br>—|
||_<br>instance_6<br>instance7|.<br>-16.85<br>-182.75|.<br>-16.35<br>-223.75|—<br>—|—<br>—|.<br>-115.85<br>-23.70|.<br>-192.70<br>-21.30|—<br>—|.<br>-47.90<br>-211.70|.<br>-20.65<br>-29.65|—<br>—|
||_<br>instance8|-22380|-18635|—|—|-1720|-1575|—|-5835|-21070|—|
||_<br>instance_9|.<br>-223.75|.<br>-15.55|—|—|.<br>-176.30|.<br>-224.30|—|.<br>-24.50|.<br>-223.80|—|
||instance10|-22.20|-223.80|—|—|-41.35|-72.00|—|-40.85|-223.70|—|
||_<br>instance_11<br>|—|-20.05<br>|—|—|-148.60<br>|—|—|-17.75<br>|—|—|
||instance_12<br>instance13|—<br>—|-21.20<br>-14.55|—<br>—|—<br>—|-15.40<br>-16.65|—<br>—|—<br>—|-223.80<br>-25.50|—<br>—|—<br>—|
||_<br>instance14|—|-20470|—|—|-1810|—|—|-1970|—|—|
||_<br>instance_15|—|.<br>-68.70|—|—|.<br>-16.35|—|—|.<br>-24.50|—|—|
||instance16|—|-23.15|—|—|-19.75|—|—|-16.55|—|—|
||_<br>instance17|—|-9540|—|—|-1705|—|—|-22430|—|—|
||_<br>instance_18|—|.<br>-223.75|—|—|.<br>-21.35|—|—|.<br>-223.75|—|—|
||instance19|—|-22.65|—|—|-193.65|—|—|-58.25|—|—|
||_<br>instance_20<br>|—|-144.15|—|—|-15.75|—|—|-18.30<br>|—|—|
||instance_21<br>instance22|—<br>—|—<br>—|—<br>—|—<br>—|—<br>—|—<br>—|—<br>—|-19.20<br>-14.35|—<br>—|—<br>—|
||_<br>instance23|—|—|—|—|—|—|—|-1890|—|—|
||_<br>instance_24|—|—|—|—|—|—|—|.<br>-18.95|—|—|
||instance_25|—|—|—|—|—|—|—|-25.45|—|—|
||instance_26<br>|—|—|—|—|—|—|—|-22.60<br>|—|—|
||instance_27|—|—|—|—|—|—|—|-20.75|—|—|
||instance28|—|—|—|—|—|—|—|-24.05|—|—|
||_<br>instance_29<br>|—|—|—|—|—|—|—|-21.35<br>|—|—|
||instance_30|—|—|—|—|—|—|—|-41.40|—|—|
||instance31|—|—|—|—|—|—|—|-223.60|—|—|
||_<br>instance32|—|—|—|—|—|—|—|-1525|—|—|
||_<br>instance_33<br>instance34|—<br>—|—<br>—|—<br>—|—<br>—|—<br>—|—<br>—|—<br>—|.<br>-223.80<br>-14.20|—<br>—|—<br>—|
||_<br>instance35|—|—|—|—|—|—|—|-2120|—|—|
||_<br>instance_36|—|—|—|—|—|—|—|.<br>-222.15|—|—|
||instance_37|—|—|—|—|—|—|—|-19.65|—|—|
||instance_38<br>|—|—|—|—|—|—|—|-19.05<br>|—|—|
||instance_39<br>instance_40|—<br>—|—<br>—|—<br>—|—<br>—|—<br>—|—<br>—|—<br>—|-16.30<br>-18.45|—<br>—|—<br>—|



