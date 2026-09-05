# Comprehensive Literature Review: Bridging Time-Series, LLMs, and Text-Based Federated Multi-Agent Systems for PV Fault Diagnosis

**Prepared for:** Research on Text-Based Federated-Like Multi-Agent Systems for Photovoltaic Fault Diagnosis and Predictive Maintenance

**Date:** September 2026

---

## 1. Introduction

This review surveys the academic literature from 2021–2026 at the intersection of three research pillars: (1) transforming numerical time-series into textual representations that LLMs can process, (2) applying LLMs to industrial and PV fault diagnosis, and (3) text-based or semantic federated collaboration among distributed agents. The goal is to map the landscape of methods that could underpin a novel architecture where PV monitoring agents exchange natural language insights — rather than model weights or gradients — to collectively diagnose faults and coordinate predictive maintenance.

The review is organized into three sections corresponding to the three pillars, followed by a synthesis section that identifies how these streams converge toward your proposed architecture.

---

## 2. Area 1 — Time-Series Verbalization and Captioning

This section reviews how the field has progressively developed methods to bridge the modality gap between continuous numerical time-series and discrete textual tokens. The approaches range from direct numerical-to-string encoding to learned cross-modal alignment, and most recently to fully generative time-series captioning.

### 2.1 Direct Numerical Encoding: LLMs as Zero-Shot Forecasters

**Paper:** Gruver, N., Finzi, M., Qiu, S., & Wilson, A. G. (2023). *Large Language Models Are Zero-Shot Time Series Forecasters.* NeurIPS 2023. [arXiv:2310.07820](https://arxiv.org/abs/2310.07820)

**Core Methodology:** This foundational paper demonstrated that pre-trained LLMs (GPT-3, LLaMA-2) can perform time-series forecasting without any fine-tuning by simply encoding numerical values as comma-separated digit strings. The key insight is that LLMs' next-token prediction capability over numerical strings implicitly captures temporal patterns. The authors found that careful tokenization choices (number of decimal places, scaling, delimiters) significantly impact performance, and that LLMs can match or outperform purpose-built forecasting models on several benchmarks.

**Adaptation for PV Fault Diagnosis:** This is the simplest possible bridge between your sensor data and an LLM agent. A local PV agent could serialize its irradiance, voltage, and current readings as formatted numerical strings and prompt a local LLM to detect deviations from expected patterns. The zero-shot nature means no local training is needed — critical for a federated setup where each node may have limited compute. However, the approach is limited in that it relies on the LLM's implicit pattern recognition over digit sequences rather than domain-aware semantic reasoning, and it struggles with very long multivariate series.

---

### 2.2 Prompt-Based Paradigm: PromptCast

**Paper:** Xue, H. & Salim, F. D. (2023). *PromptCast: A New Prompt-Based Learning Paradigm for Time Series Forecasting.* IEEE Transactions on Knowledge and Data Engineering. [arXiv:2210.08964](https://arxiv.org/abs/2210.08964)

**Core Methodology:** PromptCast reformulates time-series forecasting as a sentence-to-sentence task. Instead of numerical input → numerical output, it transforms both historical observations and future predictions into natural-language sentences. For example, a temperature time series is verbalized as: *"The temperature at 8 AM was 22°C, at 9 AM was 23.5°C..."*, and the model is asked to continue in the same linguistic format. The paper introduces the PISA (Prompt-based Instruction for Sentence-based Analogy) dataset with paired numerical and textual time-series representations. The approach leverages pre-trained language models (BART, GPT-2) fine-tuned on these text-format time series.

**Adaptation for PV Fault Diagnosis:** PromptCast's verbalization templates are directly transferable to PV monitoring. An agent could verbalize: *"At 10:00, Module A3 produced 245W under 850 W/m² irradiance. At 10:15, output dropped to 180W while irradiance remained at 840 W/m²."* This sentence-level encoding enables the agent to share observations in natural language — the exact communication format your text-based federated architecture envisions. The shared insights would be immediately interpretable by both human operators and other LLM agents, with no gradient exchange required.

---

### 2.3 Cross-Modal Alignment via Reprogramming: Time-LLM

**Paper:** Jin, M., Wang, S., Ma, L., Chu, Z., Zhang, J. Y., Shi, X., Chen, P.-Y., Liang, Y., Li, Y.-F., Pan, S., & Wen, Q. (2024). *Time-LLM: Time Series Forecasting by Reprogramming Large Language Models.* ICLR 2024. [arXiv:2310.01728](https://arxiv.org/abs/2310.01728)

**Core Methodology:** Time-LLM introduces a *reprogramming* framework that keeps the LLM backbone completely frozen while learning to translate time-series patches into the LLM's input embedding space. It has two key innovations: (1) **Input Reprogramming** — time-series patches are linearly projected and then cross-attended with a set of learnable *text prototypes* (embeddings of domain-relevant words like "increasing," "seasonal," "anomalous") to produce reprogrammed tokens that the LLM can process; (2) **Prompt-as-Prefix** — natural-language descriptions of the dataset context, task instructions, and input statistics are prepended as a textual prefix to guide the LLM's reasoning. The frozen LLM then processes the concatenation of the text prefix and reprogrammed time-series tokens.

**Adaptation for PV Fault Diagnosis:** Time-LLM's architecture is highly relevant because: (a) the text-prototype cross-attention could be initialized with PV domain vocabulary (e.g., "shading," "hotspot," "degradation," "soiling," "string mismatch") to force the reprogrammed embeddings into a semantically meaningful space; (b) the prompt-as-prefix mechanism naturally accommodates metadata (plant location, panel age, weather context); and (c) the frozen-LLM design means each distributed agent uses the same base model, facilitating coherent cross-agent communication since all agents share the same semantic space.

---

### 2.4 Text Prototype Alignment: TEST

**Paper:** Sun, C., Li, Y., Li, H., & Hong, S. (2024). *TEST: Text Prototype Aligned Embedding to Activate LLM's Ability for Time Series.* ICLR 2024. [arXiv:2308.08241](https://arxiv.org/abs/2308.08241)

**Core Methodology:** TEST proposes aligning time-series embeddings with the text embedding space of a pre-trained LLM by using "text prototypes." The method works by: (1) selecting a vocabulary of descriptive words/phrases relevant to time-series behavior (e.g., "rising trend," "periodic," "sudden drop"); (2) encoding these prototypes through the LLM's text encoder to obtain anchor embeddings; (3) training a lightweight projection network that maps time-series segment embeddings into this text-anchored space; and (4) using the aligned embeddings as input to the frozen LLM for downstream tasks. The method is instance-level: each time-series instance is aligned to its nearest text prototype, then fed to the LLM.

**Adaptation for PV Fault Diagnosis:** TEST's text-prototype approach could be extended with PV-specific prototypes such as "partial shading event," "inverter clipping," "string current mismatch," "PID degradation." This creates an interpretable intermediate representation: before the LLM reasons about a fault, the system has already identified which semantic categories the sensor readings are closest to. This intermediate symbolic layer is exactly what your text-based federation needs — agents could exchange these prototype-aligned descriptions rather than raw data, providing a compact, privacy-preserving, and semantically rich communication format.

---

### 2.5 Semantic Space-Informed Prompting: S²IP-LLM

**Paper:** Pan, Z., Jiang, K., Garg, A., Neubig, G., Shen, S., & Nakkiran, P. (2024). *S²IP-LLM: Semantic Space Informed Prompt Learning with LLM for Time Series Forecasting.* ICML 2024. [arXiv:2403.05798](https://arxiv.org/abs/2403.05798)

**Core Methodology:** S²IP-LLM bridges the gap between time-series and language by leveraging the semantic space of pre-trained word embeddings. It retrieves the nearest word embeddings to learned time-series representations and uses these as semantically informed prompts for the LLM. The innovation is that time-series patterns are mapped to the closest points in the LLM's existing word embedding manifold, creating a natural bridge. A contrastive learning objective ensures that similar time-series patterns map to similar regions in the word embedding space, while dissimilar patterns map apart.

**Adaptation for PV Fault Diagnosis:** The semantic mapping could be tailored so that fault signatures map to distinct regions of the word embedding space — for instance, a voltage dip pattern maps near words like "fault," "degradation," "anomaly," while a normal clear-sky profile maps near "nominal," "healthy," "optimal." This creates a natural vocabulary for inter-agent communication: an agent can report its semantic-space coordinates or the nearest semantic descriptors, and receiving agents can interpret these without needing access to the raw data.

---

### 2.6 Multimodal Time-Series Forecasting: GPT4MTS and DP-GPT4MTS

**Paper:** Jia, C. & Wang, B. (2024). *GPT4MTS: Prompt-based Large Language Model for Multimodal Time-series Forecasting.* AAAI 2024. [DOI:10.1609/aaai.v38i21.30383](https://ojs.aaai.org/index.php/AAAI/article/view/30383)

**Paper:** DP-GPT4MTS (2025). *Dual-Prompt Large Language Model for Textual-Numerical Time Series Forecasting.* [arXiv:2508.04239](https://arxiv.org/html/2508.04239v1)

**Core Methodology:** GPT4MTS treats time-series forecasting as a multimodal problem, combining numerical time-series data with textual context (e.g., news, weather reports, event descriptions). It uses a dual-encoding approach: numerical data is encoded through a temporal encoder, while associated text is encoded through the LLM's text encoder. The two modalities are fused through cross-attention. DP-GPT4MTS extends this with a dual-prompt mechanism that separately prompts the LLM about textual context and numerical patterns, then combines the predictions.

**Adaptation for PV Fault Diagnosis:** This multimodal framework is directly relevant because PV systems generate both numerical data (I-V curves, power output, temperature) and textual context (maintenance logs, weather reports, manufacturer datasheets, operator notes). An agent could combine its sensor time-series with textual context such as: *"This string was cleaned 14 days ago. Weather forecast shows haze expected. Panel model: XYZ-350W, installed 2019."* The dual-modal fusion mirrors real PV monitoring workflows where operators combine quantitative data with contextual knowledge.

---

### 2.7 Generative Time-Series Captioning: TSLM

**Paper:** Trabelsi, M. (2025). *Time Series Language Model for Descriptive Caption Generation.* Engineering Applications of Artificial Intelligence. [arXiv:2501.01832](https://arxiv.org/abs/2501.01832)

**Core Methodology:** TSLM is a dedicated model for generating natural-language captions that describe the salient features of a time series. Unlike methods that translate time series for forecasting, TSLM explicitly produces human-readable descriptions such as *"The signal shows a steady increase from t=0 to t=50, followed by three rapid oscillations around the mean, and a gradual decline in the final quarter."* The model uses a time-series encoder (convolutional + attention) coupled with a language decoder, trained on pairs of time series and expert-written captions.

**Adaptation for PV Fault Diagnosis:** TSLM is perhaps the most directly relevant technology for your architecture. If each PV agent can generate a natural-language caption of its local sensor data, that caption becomes the unit of communication in your text-based federation. An agent might produce: *"Module B2 showed normal morning ramp-up. At 11:30, a 35% power drop occurred over 3 minutes with stable irradiance. Current recovered partially at 14:00. Pattern consistent with reversible shading or bypass diode activation."* This is precisely the kind of textual insight that other agents can receive, reason about, and aggregate — no gradients required.

---

### 2.8 Benchmark for Time-Series Description: BEDTime

**Paper:** Hartvigsen, T. et al. (2025). *BEDTime: A Unified Benchmark for Automatically Describing Time Series.* ICML 2026. [arXiv:2509.05215](https://arxiv.org/abs/2509.05215)

**Core Methodology:** BEDTime establishes the first unified benchmark for the task of automatically generating textual descriptions of time series. It defines a taxonomy of description types (trend descriptions, anomaly descriptions, comparative descriptions, causal narratives) and provides evaluation metrics for measuring the quality of generated descriptions against human-written references. The benchmark covers multiple domains including finance, healthcare, and industrial monitoring.

**Adaptation for PV Fault Diagnosis:** BEDTime provides the evaluation framework your system would need. As your agents generate textual insights about PV data, you need standardized metrics to assess whether the descriptions are accurate, complete, and actionable. The benchmark's taxonomy of description types (especially anomaly descriptions and causal narratives) maps directly onto PV fault reporting needs.

---

### 2.9 Joint Language-Time Series Foundation Model: Chronicle

**Paper:** Chronicle (2025). *A Multimodal Foundation Model for Joint Language and Time Series Understanding.* [arXiv:2605.20268](https://arxiv.org/abs/2605.20268)

**Core Methodology:** Chronicle is a foundation model trained from scratch on paired time-series and language data. Unlike methods that retrofit existing LLMs (Time-LLM, TEST), Chronicle jointly learns time-series and language representations in a shared latent space. It supports bidirectional translation: time series → text descriptions, and text instructions → time-series operations (filtering, forecasting, anomaly detection). The model uses a unified tokenization scheme that interleaves numerical tokens with text tokens.

**Adaptation for PV Fault Diagnosis:** Chronicle represents the frontier of the time-series-to-text pipeline. If deployed as the local model at each PV agent, it could natively understand both the numerical sensor streams and the textual communications from other agents in the federation. Its bidirectional capability means an agent can both describe its observations in text and interpret textual hypotheses from other agents by grounding them back in its local numerical data.

---

## 3. Area 2 — LLMs for Fault Diagnosis

### 3.1 Direct LLM-Based Industrial Fault Diagnosis: LLM-TSFD

**Paper:** (2024). *LLM-TSFD: An Industrial Time Series Human-in-the-Loop Fault Diagnosis Method Based on a Large Language Model.* Expert Systems with Applications, 264, 125861. [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0957417424027283)

**Core Methodology:** LLM-TSFD explicitly addresses how to make LLMs diagnose faults from industrial time-series data. The pipeline has three stages: (1) **Feature Extraction** — statistical and frequency-domain features are computed from raw sensor signals (mean, variance, kurtosis, spectral peaks, etc.); (2) **Textual Encoding** — these features are serialized into structured natural-language descriptions using templates (e.g., *"The vibration signal RMS is 4.2g, which is 2.3× above the baseline. The dominant frequency shifted from 120Hz to 95Hz."*); (3) **LLM Reasoning** — the text description is fed to an LLM with domain-specific prompts that include fault taxonomy descriptions and diagnostic decision trees. A human-in-the-loop module allows operators to refine the LLM's diagnoses.

**Adaptation for PV Fault Diagnosis:** This is the closest existing architecture to what your PV agents would do locally. The three-stage pipeline (extract → verbalize → reason) can be directly instantiated for PV data: extract features from I-V curves, power output, and temperature readings; verbalize them as structured text; and prompt a local LLM with PV fault taxonomy (shading, soiling, hotspot, PID, string mismatch, inverter fault, etc.). The human-in-the-loop element maps to your maintenance coordination layer. The key extension your work adds is the federation — sharing these textual diagnoses across agents.

---

### 3.2 Domain-Specialized LLM: FD-LLM

**Paper:** (2025). *FD-LLM: Large Language Model for Fault Diagnosis of Complex Equipment.* Advanced Engineering Informatics, 65, 103208. [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S1474034625001016)

**Core Methodology:** FD-LLM fine-tunes a large language model specifically for fault diagnosis using a curated dataset of fault-related text: maintenance reports, fault logs, vibration analysis reports, and expert diagnostic reasoning chains. The innovation is the construction of a domain-specific instruction-tuning dataset where each sample pairs sensor data descriptions with expert-level diagnostic reasoning in natural language. The model learns to chain observations → hypotheses → diagnostic conclusions, mimicking expert reasoning patterns.

**Adaptation for PV Fault Diagnosis:** FD-LLM's instruction-tuning approach could be replicated for PV systems by collecting and curating: PV maintenance logs, inverter alarm histories, manufacturer fault code documentation, and expert diagnostic workflows. A PV-specific FD-LLM at each agent would produce higher-quality diagnostic text than a general-purpose LLM, making the textual insights exchanged in your federation more precise and actionable.

---

### 3.3 Multimodal LLM for Industry 4.0 FDD

**Paper:** Alsaif, K., Albeshri, A., Khemakhem, M., & Eassa, F. (2024). *Multimodal Large Language Model-Based Fault Detection and Diagnosis in Context of Industry 4.0.* Electronics, 13(24), 4912. [MDPI](https://www.mdpi.com/2079-9292/13/24/4912)

**Core Methodology:** This framework uses GPT-4 in a hybrid online/offline architecture. Offline: the LLM is fine-tuned on historical fault cases combining textual descriptions, sensor readings, and maintenance records. Synthetic datasets generated by the LLM itself augment training data for rare fault scenarios. Online: real-time sensor streams are converted to structured text reports at regular intervals, and the LLM performs continuous monitoring, comparing current descriptions against its learned fault signatures. The system also generates natural-language explanations for each diagnosis.

**Adaptation for PV Fault Diagnosis:** The synthetic data generation capability is particularly valuable for PV systems, where some fault types (e.g., PID, arc faults) are rare in operational data. An LLM could generate synthetic fault scenarios in text form, which are then shared across the federation to build collective diagnostic experience — a form of text-based knowledge distillation that replaces gradient-based federated learning.

---

### 3.4 LLM-Assisted Physical Invariant Extraction: InvarLLM

**Paper:** (2024). *INVARLLM: LLM-assisted Physical Invariant Extraction for Cyber-Physical Systems Anomaly Detection.* [arXiv:2411.10918](https://arxiv.org/abs/2411.10918)

**Core Methodology:** InvarLLM uses LLMs to extract physical invariant rules from sensor data descriptions. The approach works in two phases: (1) the LLM is presented with descriptions of normal system behavior and asked to infer physical rules/constraints that govern the system (e.g., *"When irradiance exceeds 500 W/m², power output should be proportional within ±10%"*); (2) these LLM-inferred rules are then used as anomaly detection criteria — violations indicate faults. The LLM essentially acts as a knowledge engineer, extracting domain rules that would traditionally require manual expert specification.

**Adaptation for PV Fault Diagnosis:** This is highly relevant for PV systems where many physical invariants are known but tedious to encode: the relationship between irradiance and power, temperature coefficients, string current balance, voltage-temperature relationships, etc. An LLM agent could automatically extract these invariants from each PV plant's specific data, and these rules could be shared across the federation as compact textual representations. A newly installed plant's agent could receive invariant rules from experienced agents rather than needing to learn them from scratch — a powerful form of text-based knowledge transfer.

---

### 3.5 LLM-Based Anomaly Detection in CPS with RAG

**Paper:** (2024). *Evaluating Open-Source LLMs for Anomaly Detection in Cyber-Physical Systems using RAG.* [arXiv:2407.21783](https://arxiv.org/pdf/2407.21783)

**Core Methodology:** This work evaluates open-source LLMs (Mistral 7B, Llama 3.1 8B, Gemma 2) for anomaly detection in battery management and powertrain systems using Retrieval-Augmented Generation (RAG). The novel two-step process is: (1) the LLM first infers operational rules from descriptions of normal behavior; (2) these inferred rules are stored and retrieved to perform fault detection on new observations. Results showed F1-scores up to 1.0 in some scenarios, demonstrating that smaller open-source LLMs can be highly effective when properly prompted.

**Adaptation for PV Fault Diagnosis:** The RAG-based approach is ideal for a federated PV setup. Each agent maintains a local retrieval database of operational rules and past diagnoses. When a new observation arrives, the agent retrieves relevant past cases and rules to contextualize its diagnosis. Critically, the retrieval database can be enriched with textual insights from other agents in the federation — this is essentially text-based federated knowledge accumulation. The demonstrated effectiveness of small open-source models (7–8B parameters) means this can run on edge hardware at each PV site.

---

### 3.6 LLMs for PV-Specific Applications

**Paper:** Mellit, A. & Kalogirou, S. A. (2025). *Recent Advances in IR Thermographic Imaging and Embedded AI for Fault Diagnosis and Predictive Maintenance of PV Plants.* Renewable and Sustainable Energy Reviews, 116057. [ScienceDirect](https://doi.org/10.1016/j.rser.2025.116057)

**Core Methodology:** This comprehensive review covers the intersection of deep learning and PV fault diagnosis, with a forward-looking section on integrating LLMs. The authors propose a modern monitoring architecture combining TinyML (embedded ML on microcontrollers), IoT sensors, IR thermal imaging, and LLMs. The LLM serves as a reasoning layer that integrates multiple data modalities — thermal images, electrical measurements, weather data — into coherent diagnostic narratives and maintenance recommendations.

**Adaptation for PV Fault Diagnosis:** This review validates the direction of your research by demonstrating industry interest in LLM-augmented PV monitoring. The proposed architecture (sensor → TinyML → IoT → LLM) maps onto your agent architecture where each site's TinyML/IoT layer feeds a local LLM agent that then participates in the text-based federation.

---

**Paper:** (2026). *Large Language Models in Renewable Energy Systems: A Comprehensive Review of Forecasting, Control, Policy, and Fault Diagnosis.* [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2949821X26000761)

**Core Methodology:** This 2026 review synthesizes how LLMs are being applied across renewable energy domains, including PV. It covers LLM-based power forecasting (encoding meteorological and production data as text prompts), LLM-assisted grid control (generating control policies from system state descriptions), and LLM-based fault diagnosis. The review notes that text-based representations of system state enable interpretable monitoring and cross-system knowledge transfer.

**Adaptation for PV Fault Diagnosis:** The review's observation about "cross-system knowledge transfer via text" directly supports your federation concept. Different PV plants generate different text descriptions of similar faults; an LLM can recognize semantic equivalences (e.g., *"sudden power drop under clear sky"* from one plant and *"string current imbalance detected during peak hours"* from another may describe the same root cause).

---

### 3.7 Review: From Traditional ML to LLM Fusion for Fault Diagnosis

**Paper:** Nie, Q., Geng, J., & Liu, C. (2026). *A Review of Fault Diagnosis Methods: From Traditional Machine Learning to Large Language Model Fusion Paradigm.* Sensors, 26(2), 702. [MDPI](https://www.mdpi.com/1424-8220/26/2/702)

**Paper:** Paolini, D., Dini, P., Elhanashi, A., & Saponara, S. (2026). *Advanced Fault Detection and Diagnosis Exploiting ML and AI for Engineering Applications.* Electronics, 15(2), 476. [MDPI](https://www.mdpi.com/2079-9292/15/2/476)

**Core Methodology:** These reviews chart the evolution from signal-processing-based fault diagnosis through classical ML (SVM, random forests), deep learning (CNN, RNN, Transformers), to the emerging LLM fusion paradigm. Both identify knowledge graphs, digital twins, and LLMs as the next integration frontier. Paolini et al. specifically highlight federated learning and privacy-preserving methods as critical emerging directions.

**Adaptation for PV Fault Diagnosis:** These reviews confirm that the field is converging toward exactly the architecture you propose — LLM-based reasoning over sensor data with distributed, privacy-preserving collaboration. Your text-based federation can be framed as the next step beyond what these reviews anticipate.

---

## 4. Area 3 — Semantic / Text-Based Federated Collaboration

### 4.1 The Foundational Paper: Federation over Text

**Paper:** (2026). *Federation over Text: Insight Sharing for Multi-Agent Reasoning.* [arXiv:2604.16778](https://arxiv.org/abs/2604.16778)

**Core Methodology:** This paper is the most directly relevant to your research. It proposes replacing traditional federated learning's gradient exchange with natural-language insight sharing among distributed LLM agents. Each agent processes its local data, generates textual insights (observations, hypotheses, rules, conclusions), and shares these with other agents. The receiving agents incorporate these textual insights into their own reasoning through prompt augmentation. The paper demonstrates that this "federation over text" achieves comparable or superior performance to gradient-based federated learning on several reasoning benchmarks, while providing: (a) complete data privacy (no raw data or gradients leave each node); (b) interpretability (all communications are human-readable); (c) heterogeneity tolerance (agents can use different model architectures); (d) communication efficiency (text is far more compact than gradient vectors).

**Adaptation for PV Fault Diagnosis:** This paper provides the theoretical and empirical foundation for your entire architecture. Your PV agents would each analyze local sensor data, generate textual diagnoses and observations, and share these with the federation. A central aggregator (or peer-to-peer mesh) collects textual insights and distributes synthesized knowledge back to all agents. The paper's demonstrated advantages — privacy, interpretability, heterogeneity tolerance — are all critical for real-world PV deployments where different plants may use different monitoring hardware and software.

---

### 4.2 Multi-Agent Debate for Improved Reasoning

**Paper:** Du, Y., Li, S., Torralba, A., Tenenbaum, J. B., & Mordatch, I. (2024). *Improving Factuality and Reasoning in Language Models through Multiagent Debate.* ICML 2024. [arXiv:2305.14325](https://arxiv.org/abs/2305.14325)

**Core Methodology:** This paper demonstrates that multiple LLM instances can improve each other's reasoning through structured debate. Each agent proposes an answer, then agents critique each other's proposals in natural language over multiple rounds, converging on more accurate and factual conclusions. The debate mechanism naturally handles uncertainty — agents express confidence levels in text and revise their positions based on counterarguments.

**Adaptation for PV Fault Diagnosis:** Multi-agent debate directly maps onto your fault diagnosis scenario. When one agent detects an anomaly, it could present its diagnosis to the federation. Other agents, drawing on their own data and experience, might agree, propose alternative diagnoses, or identify confounding factors. For example: Agent A reports *"Suspected hotspot on string 3 based on 15% current drop."* Agent B responds: *"I observed a similar pattern but it was caused by inverter MPPT re-tracking after cloud passage. Check if the drop correlates with a brief irradiance dip."* This debate refines the collective diagnosis beyond what any single agent could achieve.

---

### 4.3 Federated Reasoning LLMs: Survey

**Paper:** Wei, S., Tong, Y., Zhou, Z., Xu, Y., Gao, J., Tu, W., He, T., & Lv, W. (2025). *Federated Reasoning LLMs: A Survey.* Frontiers of Computer Science. [Springer](https://link.springer.com/content/pdf/10.1007/s11704-025-50480-3.pdf)

**Core Methodology:** This survey comprehensively reviews how federated learning has been applied to reasoning-capable LLMs. It proposes a taxonomy based on training signals: (1) signals from raw data (federated pre-training and fine-tuning); (2) signals from learned representations (knowledge distillation across agents); and (3) signals from preference feedback (federated RLHF). The survey explicitly discusses the emerging trend of text-based knowledge exchange as an alternative to gradient-based federated learning, noting its advantages in communication efficiency and privacy.

**Adaptation for PV Fault Diagnosis:** This survey positions your work within the broader landscape of federated LLM research. Your text-based federation falls primarily under category (2) — knowledge distillation — but through textual insights rather than learned representation vectors. The survey's identification of this as an emerging trend validates the novelty and timeliness of your approach. It also highlights open challenges (consensus mechanisms, conflict resolution, quality control of shared insights) that your PV-specific implementation would need to address.

---

### 4.4 Federated LLMs: Current Progress

**Paper:** Yao, Y., Zhang, Z. et al. (2024). *Federated Large Language Models: Current Progress and Future Directions.* [arXiv:2409.15723](https://arxiv.org/abs/2409.15723)

**Core Methodology:** This survey maps the landscape of combining federated learning with LLMs, covering federated fine-tuning (distributing LoRA adapters rather than full gradients), federated prompt tuning (sharing soft prompts), and federated instruction tuning. It identifies key challenges: communication overhead of sharing even compressed model updates, heterogeneity of local data distributions, and the need for alignment across agents with different fine-tuning histories.

**Adaptation for PV Fault Diagnosis:** This survey highlights the specific problems that your text-based approach elegantly solves. Traditional federated LLM approaches still exchange model artifacts (LoRA weights, soft prompts) — your text-based federation eliminates this entirely, replacing model-level communication with semantic-level communication. The heterogeneity challenge (different PV plants have different panel types, orientations, local climate) is handled naturally because text is model-agnostic: an insight like *"Sudden 20% production drop after 3 years typically indicates early PID onset"* is useful regardless of the receiving agent's model architecture.

---

### 4.5 Coordination in Multi-Agent LLM Systems: AgentsNet

**Paper:** (2025). *AgentsNet: Coordination and Collaborative Reasoning in Multi-Agent LLMs.* [arXiv:2507.08616](https://arxiv.org/html/2507.08616v1)

**Core Methodology:** AgentsNet proposes a structured communication topology for multi-agent LLM systems. Instead of all-to-all broadcast, agents are organized in a graph where communication links reflect task-relevant relationships. The system includes mechanisms for message routing, priority-based attention to incoming messages, and conflict resolution when agents disagree. Communication is entirely in natural language.

**Adaptation for PV Fault Diagnosis:** AgentsNet's topology design is relevant for scaling your federation. PV plants in the same geographic region (sharing weather conditions) could form local clusters. Plants with similar hardware could form another overlay network. A hierarchical topology — site-level agents → regional coordinators → global aggregator — would mirror real utility management structures. The priority mechanisms help when one agent detects a critical fault (e.g., arc fault, fire risk) and needs to broadcast urgently.

---

### 4.6 Latent Collaboration in Multi-Agent Systems

**Paper:** (2025). *Latent Collaboration in Multi-Agent Systems.* [arXiv:2511.20639](https://arxiv.org/abs/2511.20639)

**Core Methodology:** This paper explores collaboration between agents through shared latent representations rather than explicit messages. While not purely text-based, it investigates the spectrum between gradient sharing and text sharing, finding that intermediate representations (compressed summaries, abstract state descriptions) often outperform both extremes. The "latent collaboration" concept — agents sharing compact, learned representations of their local state — sits between your text-based federation and traditional gradient-based FL.

**Adaptation for PV Fault Diagnosis:** This work suggests a useful design option for your system: a hybrid approach where agents share both natural-language insights (for interpretability and cross-architecture compatibility) and compact latent vectors (for efficiency and capturing patterns that are hard to verbalize). For instance, an agent might share *"Anomaly detected on string 3"* (text) alongside a 64-dimensional embedding of the anomaly signature (latent vector) for agents that can process it.

---

## 5. Synthesis: Toward a Text-Based Federated PV Fault Diagnosis Architecture

### 5.1 The Emerging Pipeline

From the surveyed literature, a clear pipeline emerges for each local agent in your architecture:

1. **Data Acquisition**: Multivariate time-series from PV sensors (I-V curves, power, irradiance, temperature, inverter status).

2. **Feature Extraction & Verbalization** (Methods from Area 1): Apply techniques from LLM-TSFD, PromptCast, or TSLM to transform raw sensor data into structured natural-language descriptions. Time-LLM's text-prototype alignment or TEST's prototype-based embedding can provide domain-specific semantic grounding.

3. **Local Reasoning & Diagnosis** (Methods from Area 2): Feed the verbalized data to a local LLM (fine-tuned with FD-LLM's approach or prompted with InvarLLM's invariant rules) to produce a textual diagnostic assessment.

4. **Federated Exchange** (Methods from Area 3): Share the textual assessment with the federation using "Federation over Text" protocols. Receive insights from other agents and incorporate them via multi-agent debate (Du et al.) within a structured topology (AgentsNet).

5. **Consensus & Action**: Aggregate multi-agent insights into maintenance recommendations, using the debate mechanism to resolve diagnostic disagreements.

### 5.2 Key Methodological Choices

| Design Decision | Recommended Approach | Key Reference |
|---|---|---|
| Numerical → Text | Template-based verbalization + text-prototype alignment | PromptCast, TEST, Time-LLM |
| Local fault reasoning | RAG-enhanced LLM with domain-specific instruction tuning | LLM-TSFD, FD-LLM, RAG for CPS |
| Inter-agent communication | Natural language insight sharing | Federation over Text |
| Disagreement resolution | Structured multi-agent debate | Du et al. (ICML 2024) |
| Communication topology | Hierarchical with regional clusters | AgentsNet |
| Foundation model | Joint time-series–language model | Chronicle |
| Evaluation of text quality | Standardized captioning benchmarks | BEDTime |

### 5.3 Novelty of the Proposed Architecture

The literature review reveals that while each individual component exists, **no existing work combines all three pillars for PV-specific fault diagnosis**. Specifically:

- Time-series verbalization methods have been developed primarily for forecasting, not for fault diagnosis communication.
- LLM-based fault diagnosis has been explored for industrial equipment but not in a multi-agent federated setting.
- Text-based federation ("Federation over Text") is the closest architectural match, but it has been demonstrated on reasoning benchmarks, not on time-series diagnostic tasks.
- No work applies text-based federated collaboration to the PV domain specifically.

Your proposed architecture sits at this unexplored intersection, making it a genuinely novel contribution.

### 5.4 Open Challenges

Based on the literature, key challenges your work will need to address include:

1. **Information Loss in Verbalization**: How much diagnostic-relevant information is lost when compressing multivariate PV time-series into text? BEDTime and TSLM provide evaluation frameworks but have not been tested on PV-specific fault signatures.

2. **Scalability of Text-Based Federation**: As the number of agents grows, the volume of textual insights may overwhelm receiving agents' context windows. Summarization and prioritization mechanisms (from AgentsNet) will be needed.

3. **Trust and Quality Control**: How should an agent weigh insights from a newly deployed agent vs. one with years of operational history? This is analogous to the "data quality" problem in traditional FL but manifests in the semantic domain.

4. **Adversarial Robustness**: Can a malicious or malfunctioning agent inject misleading textual insights that degrade the federation's diagnostic accuracy?

5. **Latency**: Text-based reasoning is slower than numerical anomaly detection. For safety-critical faults (arc faults, ground faults), a hybrid approach with fast numerical detectors and slower text-based deep diagnosis may be necessary.

---

## 6. References (Organized by Area)

### Area 1: Time-Series Verbalization & Captioning
- Gruver et al. (2023). Large Language Models Are Zero-Shot Time Series Forecasters. NeurIPS 2023. arXiv:2310.07820
- Xue & Salim (2023). PromptCast: A New Prompt-Based Learning Paradigm for Time Series Forecasting. IEEE TKDE. arXiv:2210.08964
- Jin et al. (2024). Time-LLM: Time Series Forecasting by Reprogramming Large Language Models. ICLR 2024. arXiv:2310.01728
- Sun et al. (2024). TEST: Text Prototype Aligned Embedding to Activate LLM's Ability for Time Series. ICLR 2024. arXiv:2308.08241
- Pan et al. (2024). S²IP-LLM: Semantic Space Informed Prompt Learning with LLM for Time Series Forecasting. ICML 2024. arXiv:2403.05798
- Jia & Wang (2024). GPT4MTS: Prompt-based Large Language Model for Multimodal Time-series Forecasting. AAAI 2024
- Trabelsi (2025). Time Series Language Model for Descriptive Caption Generation. arXiv:2501.01832
- (2025). Chronicle: A Multimodal Foundation Model for Joint Language and Time Series Understanding. arXiv:2605.20268
- (2025). DP-GPT4MTS: Dual-Prompt LLM for Textual-Numerical Time Series Forecasting. arXiv:2508.04239
- Hartvigsen et al. (2025). BEDTime: A Unified Benchmark for Automatically Describing Time Series. ICML 2026. arXiv:2509.05215

### Area 2: LLMs for Fault Diagnosis
- (2024). LLM-TSFD: Industrial Time Series Human-in-the-Loop Fault Diagnosis. Expert Systems with Applications, 264
- (2025). FD-LLM: Large Language Model for Fault Diagnosis of Complex Equipment. Advanced Engineering Informatics, 65
- Alsaif et al. (2024). Multimodal LLM-Based Fault Detection and Diagnosis in Industry 4.0. Electronics, 13(24)
- (2024). INVARLLM: LLM-assisted Physical Invariant Extraction for CPS Anomaly Detection. arXiv:2411.10918
- (2024). Evaluating Open-Source LLMs for Anomaly Detection in CPS using RAG. arXiv:2407.21783
- Mellit & Kalogirou (2025). IR Thermographic Imaging and Embedded AI for PV Fault Diagnosis. RSER, 116057
- (2026). LLMs in Renewable Energy Systems: Forecasting, Control, Policy, and Fault Diagnosis
- Nie et al. (2026). From Traditional ML to LLM Fusion for Fault Diagnosis. Sensors, 26(2)
- Paolini et al. (2026). Advanced FDD Exploiting ML and AI for Engineering Applications. Electronics, 15(2)

### Area 3: Text-Based Federated / Multi-Agent Collaboration
- (2026). Federation over Text: Insight Sharing for Multi-Agent Reasoning. arXiv:2604.16778
- Du et al. (2024). Improving Factuality and Reasoning through Multiagent Debate. ICML 2024. arXiv:2305.14325
- Wei et al. (2025). Federated Reasoning LLMs: A Survey. Frontiers of Computer Science
- Yao et al. (2024). Federated Large Language Models: Current Progress and Future Directions. arXiv:2409.15723
- (2025). AgentsNet: Coordination and Collaborative Reasoning in Multi-Agent LLMs. arXiv:2507.08616
- (2025). Latent Collaboration in Multi-Agent Systems. arXiv:2511.20639

### Surveys
- Chen (2024). Large Language Models for Time Series: A Survey. IJCAI 2024. arXiv:2402.01801
- (2024). Empowering Time Series Analysis with Large Language Models: A Survey. IJCAI 2024
- Sepúlveda-Oviedo et al. (2025). AI in PV Fault Diagnosis: A Topic-tSNE Fusion Analysis. Energy and AI
- Liu et al. (2025). Cost-effective Data-driven FDD in Distributed PV Systems. Applied Energy
