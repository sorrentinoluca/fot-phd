# **pFedRAG: A Personalized Federated Retrieval-Augmented Generation System with Depth-Adaptive Tiered Embedding Tuning** 

**Hangyu He**<sup>**1**</sup> **Xin Yuan**<sup>**2,5**</sup> **Kai Wu**<sup>**3**</sup> **Ren Ping Liu**<sup>**3**</sup> **Wei Ni**<sup>**4,5**</sup> 

1School of Computer Science, University of Sydney, Sydney, Australia 

2Data61, CSIRO, Sydney, Australia 

3Global Big Data Technologies Centre & School of Electrical and Data Engineering, University of Technology Sydney, Sydney, Australia 

4School of Engineering, Edith Cowan University, Perth, Australia 

5School of Computer Science and Engineering, University of New South Wales, Sydney, Australia 

## **Abstract** 

Large Language Models (LLMs) can undergo hallucinations in specialized domains, and standard Retrieval-Augmented Generation (RAG) often falters due to general-purpose embeddings ill-suited for domain-specific terminology. Though domain-specific fine-tuning enhances retrieval, centralizing data introduces privacy risks. The use of federated learning (FL) can alleviate this to some extent, but faces challenges of data heterogeneity, poor personalization, and expensive training data generation. We propose pFedRAG, a novel Personalized Federated RAG framework, which enables efficient collaborative fine-tuning of embedding models to address these challenges. The key contribution is a new Depth-Adaptive Tiered Embedding (DATE) architecture, which comprises a Global Shared Layer, combined using FL to capture common knowledge, and a Personalized Layer with adjustable depth tailored for local data and training results of each client. The depth is locally controlled based on crafted metrics and scoring criteria. Also, pFedRAG incorporates a fully client-side pipeline leveraging local small LLMs and vector database filtering to construct high-quality query-document pairs. Experiments on diverse medical non-IID document datasets demonstrate that pFedRAG significantly reduces communication costs, handles data heterogeneity, and improves retrieval performance. Human evaluations confirm the enhanced response quality of pFedRAG. 

## **1 Introduction** 

Large Language Models (LLMs), such as GPT series (Radford et al., 2018, 2019; Brown et al., 2020) and LLaMA (Touvron et al., 2023a,b), have achieved impressive performance across many natural language processing tasks (Zhao et al., 2023). However, LLMs remain susceptible to hallucinations, producing plausible-sounding but factually incorrect content, which is problematic in domains such as healthcare and law (Ji et al., 2023). 

Retrieval-Augmented Generation (RAG) mitigates hallucinations by incorporating external knowledge. A retriever selects relevant documents from a knowledge base, and the generator conditions its responses on these documents. The effectiveness heavily depends on retrieval quality. 

As illustrated in Figure 1(a), conventional RAG systems typically rely on general-purpose embedding models (Lewis et al., 2020a), which often underperform in specialized domains due to their inability to capture domain-specific semantics and terminology. To enhance retrieval accuracy in such domains, fine-tuning embedding models on domainspecific data has proven beneficial (Gururangan et al., 2020); see Figure 1(b). This allows models to learn domain-relevant representations and improve the relevance of retrieved content. However, centralizing such data for fine-tuning raises significant privacy and governance concerns. 

Federated Learning (FL) offers a promising framework for domain-specific fine-tuning in collaborative environments. It enables multiple parties to jointly train models without sharing raw data, instead exchanging and aggregating model parameters, thus preserving data privacy. However, applying FL to the fine-tuning of embedding models in RAG systems introduces several unique challenges: 

**Cost of Full-Parameter Fine-Tuning** . Modern embedding models contain hundreds of millions of parameters, making full-model tuning resourceintensive in FL settings. It imposes high communication and computation costs on clients. 

**Semantic Non-IID Distribution** . In real-world deployments, clients often have non-identically distributed data due to differences in institutional focus or data collection practices. This semantic heterogeneity can lead to local overfitting and degrade global model aggregation, especially with algorithms like Federated Averaging. 

**Supervised Dataset Construction** . Effective fine- 

### 14255 

_Findings of the Association for Computational Linguistics: EMNLP 2025_ , pages 14255–14268 November 4-9, 2025 ©2025 Association for Computational Linguistics 


![](P028_images/P028.pdf-0002-00.png)

### Figure analysis

Purpose: The figure provides a conceptual overview of three retrieval-augmented generation workflows under different embedding strategies and motivates the proposed pFedRAG approach.

Panel (a), RAG with pre-trained embedding:
- Inputs shown at the top include an in-domain query about common heart-related causes of chest pain and an out-of-domain query about chest X-ray findings that may indicate pneumonia.
- The workflow uses a pretrained embedding model to index and retrieve documents from a database, passes top-k documents to an LLM, and produces a response.
- Direct observation: both in-domain and out-of-domain retrieval results are marked with red crosses.
- Direct observation: the in-domain retrieved content includes less relevant material such as costochondritis and blunt force trauma rather than cardiac causes.
- Direct observation: the out-of-domain retrieved content discusses general X-ray operation and common viral respiratory infection symptoms rather than specific pneumonia indicators.
- Direct observation: both resulting LLM responses are marked incorrect, with the in-domain response focusing on non-cardiac causes and the out-of-domain response stating that the documents do not detail pneumonia-specific findings.
- Interpretation: the pretrained embedding model fails to capture domain-specific semantics well enough for reliable retrieval.

Panel (b), RAG with embedding fine-tune:
- The diagram adds local training and re-indexing of the embedding model before retrieval.
- Direct observation: in-domain retrieval and the in-domain LLM response are marked correct.
- Direct observation: in-domain retrieved content includes coronary artery blockage, heart muscle damage, and stable angina, leading to a response naming myocardial infarction and angina.
- Direct observation: out-of-domain retrieval and out-of-domain response remain marked incorrect.
- Direct observation: out-of-domain retrieved content emphasizes heart failure imaging, angiogram recovery, and chest discomfort rather than pneumonia signs.
- Interpretation: local fine-tuning improves the targeted in-domain retrieval task but does not generalize adequately to the out-of-domain query.

Panel (c), pFedRAG:
- The workflow shows multiple clients performing local training on adapters.
- The trained adapters are aggregated into an aggregated adapter associated with a pretrained embedding component, followed by re-indexing, retrieval, top-k document selection, and response generation.
- Direct observation: both in-domain and out-of-domain retrieval results are marked correct.
- Direct observation: in-domain retrieved content includes stable angina and coronary artery blockage, and the response identifies myocardial infarction and angina as common cardiac causes of chest pain.
- Direct observation: out-of-domain retrieved content includes dense opaque lung consolidation, alveoli filled with fluid, localized or diffuse infiltrates, and infection/inflammation of lung tissue.
- Direct observation: the out-of-domain response correctly states that pneumonia findings on chest X-ray include airspace opacities such as consolidation or infiltrates and possibly pleural effusions.
- Interpretation: the federated personalized adapter design is presented as combining local adaptation with shared knowledge to improve retrieval robustness across heterogeneous domains.

Connection to surrounding text: The figure visually supports the paper's motivation that conventional pretrained embeddings underperform in specialized domains, local fine-tuning can help but may be limited under heterogeneous data, and the proposed pFedRAG framework uses federated personalized adaptation to address semantic non-IID distributions while avoiding centralized sharing of raw client data.


Figure 1: Overview of retrieval-augmented generation workflows under different embedding strategies: Pretrained, Fine-tuned, and pFedRAG. 

tuning requires structured supervised data, specifically for query-document pairs with hard negatives. Generating such data is labor-intensive. 

**Contributions** . In this paper, we propose a novel Personalized Federated RAG ( **pFedRAG** ) framework designed to address these challenges. Unlike existing federated RAG methods that either per- form centralized embedding fine tuning on pooled data or apply a uniform retrieval mechanism across all clients, pFedRAG integrates a Depth-Adaptive Tiered Embedding (DATE) architecture to balance global knowledge sharing and local personaliza- tion, and incorporates a fully client side supervised dataset generation pipeline to autonomously con- struct high quality query–document pairs. The key contributions of this paper are as follows. 

**Personalized Adaptation to Data Heterogeneity** . 

To address the challenge of semantic non-IID distributions, pFedRAG incorporates the DATE architecture. This includes a shared global layer for knowledge aggregation, a client-specific personalized layer for local adaptation, and a Depth Controller that dynamically adjusts model complexity of the personalized layer. This design allows each client to tailor its retrieval model to its data characteristics, with training performance guiding the dynamic adaptation, improving personalization without sacrificing global generalizability. 

**Efficient Federated Fine-Tuning** . The proposed pFedRAG introduces the Adaptive Dual-Tier Head (ADT-Head), a parameter-efficient architecture that attaches a lightweight, trainable head to a frozen embedding backbone. This design significantly reduces communication and computational overhead, cutting per-round updates to just 4.3% of full model fine-tuning, while preserving strong retrieval performance. It enables the practical deployment of personalized retrieval models in bandwidthconstrained federated settings. 

**Privacy-Preserving Dataset Generation** . We 

propose a novel client-side pipeline for supervised data generation that avoids central data pooling. It leverages light local LLMs to generate diverse queries and applies vector-based filtering to construct relevant positive and hard negative samples. This approach enables each client to create high-quality retrieval training data autonomously, with reduced annotation costs. 

Our proposed pFedRAG is the first framework to integrate personalized embedding tuning through FL into RAG systems, enabling client-level adaptation under data heterogeneity. pFedRAG achieves substantial improvements over traditional pretrained RAG methods, including a 76.0% (local) and 71.6% (global) improvement in Recall@k, and 95.0% of the performance of centralized finetuning. Human evaluations validate its impact, with an average score of 8.1 compared to 6.0 for static embeddings, and an 78% expert preference rate. It is evident that the pFedRAG not only advances the status quo of personalized federated retrieval, but also provides strong practical utility in real-world deployment. 

## **2 Related Work** 

**FL for Retrieval-Augmented Generation** . FL (McMahan et al., 2017) enables privacy- 

14256 

preserving collaborative training across decentralized data sources (Kairouz et al., 2021), while RAG (Lewis et al., 2020b) enhances LLM factuality by grounding responses in external knowledge. The integration of these paradigms into FedRAG systems (Jung et al., 2024; Addison et al., 2024) leverages distributed knowledge while maintaining privacy in sensitive domains. 

Current FedRAG approaches have addressed various aspects: federated search across distributed clients (Flower, 2025), query overhead reduction through classification-based source selection (Guerraoui et al., 2025), probabilistic search optimization for multi-domain question answering (Shojaee et al., 2025), and privacy enhancement through Confidential Computing (Addison et al., 2024). However, these methods primarily focus on retrieval mechanisms or generator training (Kim et al., 2024; Muhamed et al., 2024), while the optimization of embedding models in FedRAG settings remains virtually unexplored. Our proposed pFedRAG fills this gap by introducing DATE, specifically designed for adapting embedding models within FL contexts. 

**Personalized FL for Client Heterogeneity** . Client heterogeneity in FL encompasses data heterogeneity (non-IID distributions) and system heterogeneity (variations in computational capabilities) (Kairouz et al., 2021), often degrading standard FL algorithm performance. Personalized Federated Learning (PFL) (Tan et al., 2022; Kulkarni et al., 2020) addresses these challenges by customizing models to individual clients while preserving collaborative benefits. 

For data heterogeneity, various approaches have been proposed: architectural model decomposition to separate shared and client-specific components (Collins et al., 2021; Arivazhagan et al., 2019), regularization to constrain local updates (Li et al., 2020), meta-learning for rapid client adaptation (Fallah et al., 2020), and client clustering to group similar users (Ghosh et al., 2020). However, these methods often assume uniform model architectures across clients, limiting their applicability in heterogeneous system environments. 

For model heterogeneity, researchers have explored knowledge distillation to align diverse architectures (Li and Wang, 2019), parameter importance metrics for dynamic submodel extraction (Su et al., 2024), and Parameter-Efficient Fine-Tuning (PEFT) (Hu et al., 2021) to adapt pre-trained mod- 

els with reduced parameters. PEFT approaches in FL include homogeneous adapters across varied backbones (Yi et al., 2023) and SVD-based aggregation of different-ranked adaptations (Shen et al., 2024). Managing model heterogeneity dynamically and effectively remains challenging; static decomposition might be suboptimal, and aggregating heterogeneous PEFT parameters can be complex. 

## **3 Problem Formulation** 

Consider an FL scenario involving _N_ clients, where each client _i ∈N_ = _{_ 1 _, . . . , N }_ possesses a local dataset _Di_ that exhibits significant data heterogeneity. Each client _i_ maintains a dual-tier embedding model, Φ _i_ = _{θ, ϕ_<sup>_g_</sup> _, ϕ_<sup>_p_</sup> _i_<sup>_}_,where</sup><sup>_θ_isa</sup> pretrained embedding backbone shared across all clients and remains frozen during training, _ϕ_<sup>_g_</sup> is a global shared layer updated collaboratively via FedAvg, and _ϕ_<sup>_p_</sup> _i_<sup>is a client-specific layer optimized</sup> locally to capture personalized information. 

Collectively, the clients aim to minimize the average loss, as given by 


![](P028_images/P028.pdf-0003-09.png)


where the local objective _Fi_ ( _·_ ) measures the retrieval embedding quality for client _i_ , based on local query-document pairs sampled from client _i_ ’s local dataset _Di_ . Specifically, each client constructs training samples comprising a query, _q_ , and corresponding positive and negative document embeddings, _d_<sup>+</sup> and _d_<sup>_−_</sup> . 

The retrieval quality is optimized using the InfoNCE loss with an _L_ 2-norm regularization term, which is defined as (van den Oord et al., 2018): 


![](P028_images/P028.pdf-0003-12.png)

### Figure analysis

The page contains two separate displayed equations in the Problem Formulation section, not a conventional plotted figure.

**Equation (1): federated optimization objective**

\[
\min_{\phi^g,\{\phi_i^p\}_{i=1}^{N}} \frac{1}{N}\sum_{i=1}^{N} F_i(\theta,\phi^g,\phi_i^p)
\]

Direct observation: this equation minimizes the average client loss over \(N\) clients. The optimized variables are the global shared layer \(\phi^g\) and the personalized client-specific layers \(\{\phi_i^p\}_{i=1}^{N}\). The pretrained embedding backbone \(\theta\) appears as an argument of each local objective but, according to the surrounding text, remains frozen during training.

Interpretation: the formulation formalizes pFedRAG as a personalized federated learning problem in which all clients collaborate through a shared component while retaining local adaptation parameters.

**Equation (2): local retrieval loss**

\[
F_i = -\mathbb{E}_{(q,d^+,d^-)\sim \mathcal{D}_i}
\left[
\log
\frac{e^{s(q,d^+)}}
{e^{s(q,d^+)}+\sum_{d^-} e^{s(q,d^-)}}
\right]
+ \lambda \lVert \Phi_i \rVert_2^2
\]

Direct observation: the local objective \(F_i\) is written as a negative expected log-ratio over samples from client dataset \(\mathcal{D}_i\), where each sample includes a query \(q\), a positive document \(d^+\), and negative document(s) \(d^-\). The numerator rewards high similarity \(s(q,d^+)\) between the query and positive document, while the denominator contrasts this score against positive and negative document similarities. An \(L_2\)-norm regularization term weighted by \(\lambda\) is added.

Interpretation: this is an InfoNCE-style contrastive retrieval loss designed to improve embedding quality by pulling query embeddings toward relevant documents and pushing them away from negatives, while regularization controls model complexity.

**Connection to surrounding text**

These equations support the paper’s transition from related work to the proposed pFedRAG framework. The nearby text defines each client model as \(\Phi_i=\{\theta,\phi^g,\phi_i^p\}\), with \(\theta\) shared and frozen, \(\phi^g\) collaboratively updated through federated averaging, and \(\phi_i^p\) locally optimized for personalization. Together, the equations specify the mathematical objective underlying the later framework description, including Depth-Adaptive Tiered Embedding, global-local federated adaptation, and personalized retrieval-augmented generation.


where _s_ ( _q, d_ ) is the similarity score of embedding vectors, and _λ_ is a regularization factor. 

## **4 Proposed pFedRAG Framework** 

The objective of pFedRAG is to collaboratively train a retrieval embedding model that captures both globally shared knowledge and personalized features unique to each client’s local data distribution. As illustrated in Figure 2, pFedRAG consists of three key aspects: Depth-Adaptive Tiered Embedding (DATE), Federated Learning With GlobalLocal Adaptation, and Personalized RAG System. 

14257 


![](P028_images/P028.pdf-0004-00.png)

### Figure analysis

The figure presents the overall pFedRAG framework, separating the system into two major regions: **Collaborative Federated Training** on the left and **Local Personalized Tuning** on the right.

**Left panel: Collaborative Federated Training**

- Directly observed components:
  - Multiple clients each perform **Personalized Local Training** at the bottom.
  - Each client maintains a **Global Shared Layer** above its local model.
  - A central server/cloud aggregates uploaded shared-layer parameters.
  - The top box is labeled **Global Aggregated Parameter**.
- Directly observed information flow:
  1. Clients conduct personalized local training.
  2. Clients upload updated shared-layer parameters to the server.
  3. The server distributes aggregated parameters back to clients.
  4. A new communication round updates the client-side global shared layer.
- Interpretation:
  - The diagram illustrates standard federated averaging over only the global/shared part of the embedding model, while keeping local personalization on each client.
  - This supports the paper’s formulation in which the backbone is frozen, a global layer is collaboratively updated, and client-specific layers remain locally optimized.

**Right panel: Local Personalized Tuning and RAG workflow**

- Directly observed DATE architecture:
  - A central block labeled **DATE** contains an **Embedding Backbone**, **ADT-Head**, and **Depth Controller**.
  - The ADT-Head is divided into a **Global Shared Layer** and an **Adaptive Personalized Layer**.
  - A **Personalized Embedding** module receives output from DATE.
- Directly observed data and retrieval components:
  - A **Database** stores indexed vectors/documents.
  - A **Local LLM** interacts with the personalized retrieval workflow.
  - A **TOP-K Documents** box provides retrieved context to the LLM.
  - A user icon submits queries and receives responses.
- Directly observed green local tuning workflow:
  - The system inputs a **Chunked Document**.
  - It generates a **Related Query**.
  - It constructs a **Query-Doc-Pair** consisting of query, positive document, and negative document.
  - The pair is used for **DATE Train**.
- Directly observed red personalized RAG workflow:
  - The database is re-indexed as a **Vector Database Re-index** step.
  - The user submits a **User Query**.
  - The system retrieves relevant documents from the database.
  - Retrieved top-k documents are used for **Prompt Context Augmentation**.
  - The Local LLM returns an **LLM Response** to the user.
- Interpretation:
  - The DATE module produces personalized embeddings that both support local training and improve retrieval for client-specific RAG.
  - The diagram connects embedding personalization to downstream retrieval-augmented generation: personalized embeddings re-index the database, retrieval supplies relevant documents, and the local LLM generates an answer using augmented context.

**Connection to surrounding text**

The figure visually supports the paper’s description of pFedRAG as combining three elements: **Depth-Adaptive Tiered Embedding**, **federated learning with global-local adaptation**, and a **personalized RAG system**. It illustrates how the global shared layer is collaboratively trained through federated aggregation, while the DATE architecture retains an adaptive personalized layer for local client-specific retrieval behavior.


Figure 2: Overall framework of the proposed pFedRAG. The framework combines collaborative federated training of a global shared layer with personalized local training via the DATE architecture. It includes client-side query–document pair generation and a personalized RAG workflow using local LLMs for domain-adaptive retrieval. 

### **4.1 Depth-Adaptive Tiered Embedding** 

DATE is the architectural foundation of pFedRAG’s retrieval model, designed to balance shared representation learning with client-specific personalization. As depicted in Figure 3, it has three components: (i) Embedding Backbone ( _θ_ ), (ii) ADT-Head, and (iii) Depth Controller. These components work in concert to create a flexible, personalized embedding architecture that adapts to the unique characteristics of each client’s data. 

**Embedding Backbone (** _θ_ **)** . The adaptive embedding backbone is built on the pretrained e5-base-v2 model (Wang et al., 2022), an adaptable text embedding model optimized for retrieval, clustering, and classification tasks. This backbone provides a universal semantic encoder shared across all clients and remains frozen during training, serving as a foundation for embedding computations while enabling adaptation through personalized retrieval. 

**ADT-Head** . This component is designed to efficiently balance global knowledge sharing with client-specific adaptation. This bifurcated structure processes embeddings from the backbone, minimizing communication overhead while preserving personalization capabilities. The ADT-Head contains two complementary layers: 

Global Shared Layer ( _<u>ϕ</u>_<sup>_g_</sup> <u>).</u> This layer forms the first stage of ADT-Head and is applied to the embeddings output by _θ_ . It is trained collaboratively across clients to extract generalized, transferable features that support effective federated aggregation. It comprises layer normalization (Ba et al., 

2016), dropout (Srivastava et al., 2014), and a pair of linear transformations interconnected by a nonlinear activation (e.g., GELU (Hendrycks and Gimpel, 2016)). By first expanding embedding dimensionality from 1D to 4D and then compressing it to 1D, _ϕ_<sup>_g_</sup> enhances the stability and generalizability of shared knowledge for robust cross-client representation learning. 

Personalized Layer ( _<u>ϕ</u>_<sup>_p_</sup> _<u>i</u>_<sup>).</sup> This layer refines the shared representation to align with each client’s local data distribution. It introduces flexibility in model expressiveness by supporting three configurable complexity levels based on varying local data complexities: 

- **Base Layer (** _L_ base **).** A lightweight configuration with a single linear layer and activation, designed for clients with low data complexity. 

- **Advanced Layer (** _L_ adv **).** This layer enhances capacity by stacking two linear layers, first expanding to 2D and then projecting back to 1D, thereby allowing for improved personalization for moderate data complexity. 

- **Extended Layer (** _L_ ext **).** This layer integrates a Self-Attention Interaction Module between the linear transformations. It expands embeddings from 1D to 2D, applies multi-head self-attention (Vaswani et al., 2017), and compresses the result back to 1D, making it suitable for clients with complex or diverse data. 

This compact tiered structure significantly reduces communication overhead compared to full-model tuning, making it suitable for FL scenarios. 

14258 

**Depth Controller** . We also develop the Depth Controller to dynamically govern personalized layer complexity during training. This component analyzes client data characteristics and monitors training dynamics to determine optimal model capacity, balancing expressiveness and efficiency. The Depth Controller operates via two modules: 

Initial Depth Assigner (IDA). The IDA employs a Complexity Scoring Unit to evaluate client data characteristics before training. It sets the Personalized Layer type of client _i_ as _L_<sup>(0)</sup> _i_ based on its local data complexity score _Si_ . Here, _Si_ is calculated by each client _i_ based on local data properties: 

_Si_ = _w_ 1 _· Di_ + _w_ 2 _·_ ( _αL_ avg _,i_ + _βTTR_ norm _,i_ )+ _w_ 3 _· PPLi,_ (3) 

where _L_ avg _,i_ is the average token length per document, _TTR_ norm _,i_ is the normalized type-token ratio, and _PPLi_ is the perplexity (Jelinek et al., 1977) computed over _Di_ . _w_ 1 _, w_ 2 _, w_ 3 _, α_ , and _β_ are weighting coefficients. This module enables assignment of a suitable initial complexity level to each client based on data characteristics. 

Dynamic Depth Scheduler (DDS). To enable clients to progressively refine layer complexity beyond initial assignments, we design the DDS with two units that jointly adapt model complexity during training: 

- **API Metrics Analysis Unit:** This unit evaluates the Adaptation Performance Index (API) for each client in fixed time windows to determine when complexity changes are needed. The API combines two key training indicators: 


![](P028_images/P028.pdf-0005-06.png)


where ∆ _L_<sup>norm</sup> _i,t_ measures normalized training loss reduction (learning momentum), and _Oi,t_<sup>norm</sup> quantifies the normalized performance gap between training and validation data (overfitting penalty). Weights _wL_ and _wO_ balance these components (with _wL_ + _wO_ = 1). 

The API trajectory determines whether a layer complexity adjustment is necessary. Layer adjustments are triggered when API _i,t_ consistently falls outside its dynamic performance band, bounded by thresholds _T_ up<sup>(</sup><sup>_i,t_)</sup> and _T_ down<sup>(</sup><sup>_i,t_).</sup><sup>_c_(</sup> _s_<sup>_i,t_)</sup> and _c_<sup>(</sup> _l_<sup>_i,t_)</sup> track consecutive instances of over- or underperformance, guiding upgrade or downgrade decisions. (See Appendix B.1 for details.) 

- **Knowledge Distillation Unit:** When a complexity change is triggered, this unit facilitates 


![](P028_images/P028.pdf-0005-10.png)



![](P028_images/P028.pdf-0005-11.png)


Figure 3: Architecture of DATE in pFedRAG, showing the Embedding Backbone, ADT-Head with its Global and Personalized layers, and Depth Controller with its IDA and DDS modules. 

a smooth transition between different model architectures. It treats the current model as teacher and the newly adjusted model as student, transferring knowledge (Hinton et al., 2015) to ensure the model maintains performance while adapting to its new complexity level. This prevents drastic performance drops during architectural transitions and enables efficient adaptation. 

### **4.2 FL With Global-Local Adaptation** 

The training process comprises three phases: (i) Model Customization via IDA, (ii) Local Tuning with DDS, and (iii) Global Aggregation on Server. 

**Model Customization via IDA** . At the start of each communication round, the IDA of client _i_ computes a local data complexity score _Si_ , which is uploaded to the server. After applying min-max normalization across all clients to map scores into the [0,1] range, the server assigns an initial personalized layer configuration _L_<sup>0</sup> _i_<sup>based on the normal-</sup> ized complexity score _Si_<sup>norm</sup> : 


![](P028_images/P028.pdf-0005-17.png)


The thresholds 0.33 and 0.67 divide the normalized range into three equal intervals, corresponding to the Base, Advanced, and Extended layers. This serves as a reasonable initialization, which the Depth Controller further refines during training. 

14259 

Each client receives the full model but activates only its assigned personalized layer. 

**Local Tuning with DDS** . We put forth an adaptive training strategy at each client, as described in Algorithm 1 of Appendix A.1. During training, the DDS of Depth Controller continuously monitors training dynamics using API _i,t_ over the fixed time windows _Tw_ . Based on the API metrics and corresponding counters, the Depth Controller determines whether to adjust the layer complexity based on the following decision rule: 


![](P028_images/P028.pdf-0006-02.png)


where _τs_ is the minimum number of consecutive rounds showing stable improvement required for an upgrade, and _τl_ is the maximum number of consecutive rounds showing performance decline tolerated before a downgrade. 

When an adjustment is triggered (i.e., decision is not "none"), we propose a novel knowledge preservation mechanism through distillation. This adaptive distillation phase employs the current model as a teacher and the adjusted model as a student: 


![](P028_images/P028.pdf-0006-05.png)


where _ϕ_<sup>_s_</sup> _i_<sup>and</sup><sup>_ϕt_</sup> _i_<sup>represent the student and teacher</sup> parameters on client _i_ respectively; _ps_ ( _x_ ) and _pt_ ( _x_ ) are the corresponding output distributions. During distillation, only the personalized layer parameters _ϕ_<sup>_p_</sup> is updated while the global shared layer _ϕ_<sup>_g_</sup> remains frozen: 


![](P028_images/P028.pdf-0006-07.png)


After adaptation, the controller enters a cooling period of _Tcool_ , during which it continues to monitor API values but temporarily suspends further structural changes to prevent oscillations. 

**Global Aggregation on Server** . Once local training completes, clients upload only their global shared layer parameters ( _ϕ_<sup>_g_</sup> _i,t_<sup>)totheserver.The</sup> server then performs standard federated averaging: 


![](P028_images/P028.pdf-0006-10.png)


This aggregated global layer is then redistributed to all clients for the next round, while personalized layers ( _ϕ_<sup>_p_</sup> _i_<sup>) remain local, preserving both personal-</sup> ization and data privacy, as shown in Figure 2. 

### **4.3 Personalized RAG System** 

The Personalized RAG System uses client-specific embeddings to enhance retrieval relevance. It covers from reconstructing local vector databases to generating context-aware responses via RAG, as shown in Figure 2. 

**Vector Database Reconstruction** . After federated training completes, each client reconstructs its local vector database using personalized embedding model Φ _i_ (combining frozen backbone with trained ADT-Head). We encode local documents with this model and index the vectors into an optimized vector database (Milvus (Milvus Team, 2019–Present)), improving retrieval accuracy for client-specific data distributions. 

**Retrieval and Generation** . During inference, user queries are encoded with the same personalized embedding model and used to retrieve the top- _K_ relevant document chunks via vector similarity search. These chunks provide contextual knowledge injected into a domain-aware prompt template shown in Table 1. This specially designed prompt bridges retrieved content with the generation capabilities of the local LLM, ensuring responses are contextually grounded and aligned with client-specific domain knowledge. 

|Domain-Aware Prompt for RAG Inference<br>Given a user query related to a medical domain, re-<br>trieve the most relevant document chunks from the<br>local vector database and use them as context to gen-<br>erate a detailed and informative response. Ensure that<br>the response is coherent and accurately refects the<br>retrieved information.<br>In-Context Few-shot Example<br>Query: {User Query}<br>Retrieved Documents: {Top-_K_ Retrieved Chunks}<br>Response:|
|---|



Table 1: LLM Prompt for Personalized RAG. 

## **5 Experiments** 

We evaluate the proposed pFedRAG framework on a medical document dataset derived from multiple research domains to simulate realistic clinical and research-oriented retrieval scenarios. Due to space limitations, detailed experimental settings are provided in Appendix D. 

### **5.1 Medical Document Datasets Preparation** 

<u>Data Collection.</u> We construct our dataset by collecting English papers from the PubMed Central 

14260 

database (National Center for Biotechnology Information (NCBI), Accessed on May 18, 2025) across six medical domains: Cardiology (3125 papers), Medical Informatics (2500), Neuroscience (2188), Oncology (1875), Pharmacy (1563), and Radiology (1250). To ensure dataset quality, we exclude nonpeer-reviewed publications, speeches, and incomplete documents. We retain only retrieval-relevant sections (title, abstract, introduction, discussion, conclusion) while removing non-textual elements and privacy-sensitive personal data. 

<u>Query-Doc Pair Generation.</u> We segment documents using the e5-base-v2 tokenizer with 512 maximum tokens per chunk, ensuring contextual coherence and compatibility with the embedding model. We leverage a light LLM (QWen2.5-7binstruct (Qwen Team, 2024)) to generate two diverse queries per document chunk, capturing varied query intents (the prompt used for query generation is provided in Table 6 of Appendix C). This process yields 32619 query-document pairs, with 80% for federated training and 20% for evaluation. 

Data Heterogeneity. To simulate realistic non-IID distributions, we partition the dataset across six clients using a Dirichlet distribution ( _α_ = 0 _._ 3) (Hsu et al., 2019), creating significant data heterogeneity that realistically emulates federated environments. 


![](P028_images/P028.pdf-0007-03.png)

### Figure analysis

The figure presents the process of query-doc-pair construction used for the paper's medical retrieval dataset.

Directly observed components and flow:
- The pipeline begins with **Raw Paper Materials**, represented as document icons.
- These are passed through **Preprocess** to produce **Extracts**, shown as a JSON-like object containing fields such as title, abstract, introduction, discussion, and conclusion.
- The extracts are then **Chunked** into **Chunked Documents**.
- A **Local LLM** is connected to the chunked documents and is labeled as generating **Relevant Queries**.
- The relevant queries are embedded using a **Pretrained Embedding** model and indexed or searched against a **Vector DB**.
- The vector database retrieves candidate documents, which are passed through a **Retrieval Filter**.
- The retrieval filter explicitly lists three rules: exclude same-article documents, select top-5 similar documents as hard negatives, and select 5 random documents as normal negatives.
- The output is a **Query-Doc Pair** box containing examples for two queries, each paired with one positive document and a list of negative documents.

Key visual relationships:
- The main information flow is from raw papers to structured extracts, then to chunked documents, then to query generation and retrieval-based negative sampling.
- The positive document appears to come from the original chunk associated with the generated query.
- Negative documents are selected via retrieval from the vector database and filtered according to the stated rules.
- The diagram distinguishes **Negative Documents** from the final **Query-Doc Pair**, indicating that negatives are an intermediate collection step before forming the training examples.

Connection to the surrounding text:
- This figure supports the paper's dataset preparation section, specifically the described generation of 32,619 query-document pairs from PubMed Central papers across six medical domains.
- It visually matches the surrounding explanation that each document chunk is used to generate diverse queries with a light LLM, with the original chunk serving as the positive sample.
- It also corresponds to the described contrastive pair construction strategy: top-5 similar chunks are used as hard negatives, 5 random documents are used as normal negatives, and same-article chunks are excluded.

Interpretation:
- The purpose of the workflow is to create supervised contrastive retrieval data for federated RAG training, where each query has one relevant positive document and multiple negative documents.
- The design emphasizes retrieval difficulty by combining semantically similar hard negatives with randomly sampled normal negatives.


Figure 4: The process of query-doc-pair construction. 

<u>Contrastive Pair Construction.</u> For each query, we use its original document chunk as the positive sample. Negative samples are selected through local retrieval from each client’s vectorized corpus, excluding chunks from the same source article. We retrieve the top 5 most similar chunks as hard negatives and randomly sample 5 additional documents as normal negatives, maintaining a 1:10 positive-to-negative ratio. We further employ inbatch negative sampling with a batch size of 160, significantly enhancing training effectiveness by increasing negative sample diversity. 

### **5.2 Evaluation Metrics** 

We evaluate retrieval performance using four metrics: (i) **Recall@** _k_ (proportion of relevant documents in top- _k_ results) (Manning et al., 2008), (ii) **MRR** (position of first relevant document) (Voorhees, 1999), (iii) **NDCG** (ranking quality considering relevance and position) (Järvelin and Kekäläinen, 2002), and (iv) **Average Rank** (average position of relevant documents, lower is better). With one positive sample per query in our setup, Recall@ _k_ and NDCG essentially indicate whether the relevant document appears within the top- _k_ results. Detailed definitions of the metrics are provided in Appendix B.2. 

### **5.3 Main Results** 

To our knowledge, this work is the first to explore adaptive complexity embedding personalization for federated RAG, making direct comparisons with existing algorithms impossible. We therefore constructed baselines representing best practices across the spectrum of embedding model complexity. Since DATE incorporates dynamic adaptation of model complexity to match client characteristics, we first compare it with several complexityinvariant baselines. All architectures shown in Table 2 are built upon pretrained e5-base-v2 Embedding Backbone (EB), with various configurations: (i) Pretrained Embedding (frozen EB alone); (ii) EB+Global Shared Layer; and (iii) configurations with invariant personalized layer (Base/Advanced/Extended) added on top of both EB and global shared layer. 

Results demonstrate DATE’s superiority across all test sets. DATE achieves substantial improvements in both local and global evaluations, improving Recall@k by 76.0% (local) and 71.6% (global) and MRR by 70.2% (local) and 71.4% (global) over the Pretrained Embedding baseline. Compared to the best-performing complexity-invariant configuration (EB+Base Layer), DATE still shows consistent gains of 2.2% (local) and 0.7% (global) in Recall@k. These advantages confirm that our adaptive architecture’s dynamic complexity adjustment enables effective personalization while maintaining strong generalization capabilities. 

### **5.4 Ablation Study** 

**Does Dynamic Depth Scheduler (DDS) matter?** We analyze the DDS effectiveness by comparing it with a static layer allocation strategy. As shown in 

14261 

Table 2: Performance Comparison of Embedding Architectures (Top- _K_ =5). All results are averaged over three independent runs. Reported values are means with 95% confidence intervals computed using the t- distribution ( _n_ =3). Abbreviations: PT=Pretrained EB (frozen), GSL=Global Shared Layer, Adv=Advanced, Ext=Extended. 

|Method|Recall@k<br>MRR<br>NDCG|AvgRank|Recall@1|
|---|---|---|---|
||_Local Test Set_|||
|PT (EB onl<br>EB+GSL|y) 0.484±0.007 0.309±0.006 0.323±0.008<br>0.798±0.002 0.496±0.002 0.552±0.001|14.823±0.288<br> 4.330±0.081|0.159±0.005<br> 0.295±0.001|
|EB+Base|0.834±0.004 0.520±0.003 0.583±0.005|3.967±0.165|0.317±0.003|
|EB+Adv|0.816±0.005 0.504±0.006 0.562±0.006|4.197±0.213|0.301±0.004|
|EB+Ext|0.792±0.008 0.488±0.009 0.542±0.007|4.471±0.314|0.287±0.006|
|DATE|**0.852±0.003 0.526±0.003 0.588±0.004 **|**3.834±0.119 **|**0.319±0.003**|
||_Global Test Set_|||
|PT (EB onl<br>EB+GSL|y) 0.472±0.010 0.301±0.009 0.314±0.011<br>0.768±0.002 0.492±0.002 0.538±0.002|15.333±0.399<br> 5.750±0.075|0.152±0.007<br> 0.290±0.002|
|EB+Base|0.804±0.005**0.516±0.006 0.571±0.006**|4.896±0.198|0.312±0.004|
|EB+Adv|0.779±0.007 0.497±0.008 0.546±0.009|5.514±0.285|0.296±0.005|
|EB+Ext|0.757±0.011 0.482±0.012 0.529±0.010|5.986±0.441|0.282±0.008|
|DATE|**0.810±0.004 0.516±0.004 0.571±0.005 **|**4.897±0.145 **|**0.318±0.002**|



Table 3: Effectiveness of DDS (Top- _K_ =5) 

|Method<br>|Recall@k|MRR NDCG|AvgRank|Recall@1|
|---|---|---|---|---|
||_Local_|_Test Set_|||
|Pretrained Embedding|0.484|0.309 0.323|14.823|0.159|
|DC w/o DDS|0.809|0.503 0.560|4.233|0.302|
|DC w/ DDS|**0.852**|**0.526 0.588**|**3.834**|**0.319**|
||_Globa_|_l Test Set_|||
|Pretrained Embedding|0.472|0.301 0.314|15.333|0.152|
|DC w/o DDS|0.781|0.500 0.551|5.510|0.292|
|DC w/ DDS|**0.810**|**0.516 0.571**|**4.897**|**0.318**|



Table 3, DDS delivers significant improvements on both local and global test sets - increasing NDCG by 5.0% (local) and 3.6% (global) while reducing average rank by 9.4% (local) and 11.1% (global). It is evident that dynamically adjusting layer complexity based on real-time training metrics substantially enhances performance by adapting to each client’s evolving needs beyond initial assignments. 

### **5.5 Effectiveness Evaluation** 

### **Federated vs Centralized Training Effectiveness** . 

We compare our federated approach with centralized training using the Global Shared Layer. As shown in Table 4, both methods substantially outperform the pretrained baseline. While centralized training shows marginal advantages in each metric, federated training maintains robust performance (95.0% of centralized Recall@k), despite FL’s inherent data heterogeneity. This small performance gap confirms our approach effectively balances privacy with distributed knowledge utilization. 

Table 4: Federated vs Centralized Training (Top- _K_ = 5) 

|Training Mode|Recall@k MRR|NDCG|AvgRank|Recall@1|
|---|---|---|---|---|
|Pretrained Embedding|0.472<br>0.301|0.314|15.333|0.152|
|Centralized Training|**0.808**<br>**0.524 **|**0.582**|**4.297**|**0.332**|
|Federated Training|0.768<br>0.492|0.538|5.750|0.290|



Table 5: Human Evaluation of End-to-End RAG Effectiveness 

|Method<br>Avg. Score|W/T/L|Preferred (%)|
|---|---|---|
|Pretrained Embedding<br>6.0|-|-|
|DATE<br>**8.1**|32 / 11 / 7|**78%**|



### **End-to-End RAG Effectiveness via Human Eval-** 

**uation** . We conducted a human evaluation of our RAG system using QWen2.5-7B-Instruct to generate responses from Top- _K_ =5 documents retrieved by either DATE or Pretrained Embedding. Three domain experts blindly evaluated 50 response pairs on correctness, completeness, and coherence. As shown in Table 5, DATE significantly outperforms the baseline (8.1 vs 6.0 average score) with a favorable Win/Tie/Loss ratio of 32/11/7. Experts noted DATE’s responses contained more comprehensive coverage of medical concepts with fewer factual errors, confirming that improved retrieval directly translates to better response quality. 

We also examined the reliability of human ratings and the stability of model performance. Expert agreement is substantial (Krippendorff’s _α_ =0 _._ 82), indicating that annotators followed the rubric consistently and that the evaluation results are reproducible. Furthermore, across the 50 items, DATE (pFedRAG) shows tighter score dispersion (8 _._ 1 _±_ 0 _._ 95) than the Pretrained Embedding baseline (6 _._ 0 _±_ 1 _._ 75). This proves that our DATE does deliver more stable performance across questions. 

## **6 Conclusion** 

In this paper, we presented pFedRAG to enhance RAG systems in specialized domains while addressing privacy concerns and resource limitations. Our approach tackles key challenges in federated settings, including the high cost of full-model tuning, semantic divergence across heterogeneous client data, and the need for high-quality supervised datasets. We introduced DATE, a comprehensive architecture comprising ADT-Head (a parameterefficient structure that combines a global shared layer for common knowledge aggregation with dynamically adjusted personalized layers) and Depth 

14262 

Controller for guiding adaptive complexity adjustments. We also proposed a client-side pipeline leveraging local LLM and vector database filtering for privacy-preserving dataset construction. Experimental evaluations demonstrated that pFedRAG significantly reduces communication and computation costs, effectively handles data heterogeneity through adaptive model complexity, and improves end-to-end RAG performance compared to standard baselines, showcasing its practical viability for collaborative, privacy-conscious enhancement of client-personalized RAG systems. 

ical applications and the implementation of factchecking mechanisms during deployment. 

## **9 Acknowledgement** 

We thank the anonymous reviewers and the area chair for their constructive feedbacks. 

## **7 Limitations** 

**Non-Federated Generative Component** . Our framework currently personalizes only the retrieval side, leaving the generation component as a standard pre-trained LLM without clientspecific adaptation. This may limit response quality in specialized domains. Future work could explore parameter-efficient federated fine-tuning techniques like LoRA adapters for the generation component, enabling end-to-end personalization while maintaining privacy. 

**Static Hard Negative Sampling Strategy** . We employ one-time hard negative mining before training with in-batch negative sampling during iterations. As embeddings evolve, initially identified hard negatives may become less challenging. An iterative re-mining strategy that periodically updates hard negatives based on current embedding spaces could further enhance retrieval performance. 

**Future Improvements for Dataset Generation** . 

Our client-side pipeline uses lightweight LLMs to generate queries while preserving privacy and accommodating resource constraints. Though effective, query quality might not match that of larger models. Future work could explore privacypreserving mechanisms to leverage larger LLM capabilities through secure APIs, potentially enhancing dataset quality without compromising privacy. 

## **8 Ethics Statement** 

This study uses only publicly available data from the PubMed Central Open Access Subset and involves no human subjects or personal data, thus requiring no additional ethical approval. Despite these safeguards, the system could potentially generate inaccurate medical information. We recommend professional reviews of outputs before clin- 

14263 

## **References** 

- Parker Addison, Minh-Tuan H. Nguyen, Tomislav Medan, Jinali Shah, Mohammad T. Manzari, Brendan McElrone, Laksh Lalwani, Aboli More, Smita Sharma, Holger R. Roth, Isaac Yang, Chester Chen, Daguang Xu, Yan Cheng, Andrew Feng, and Ziyue Xu. 2024. C-FedRAG: A confidential federated retrieval-augmented generation system. In _arXiv preprint arXiv:2412.13163_ . 

- Manoj Ghuhan Arivazhagan, Vinay Aggarwal, Anuvabh Singh, and Sunav Choudhury. 2019. Federated learning with personalization layers. In _arXiv preprint arXiv:1912.00818_ . 

- Jimmy Lei Ba, Jamie Ryan Kiros, and Geoffrey E Hinton. 2016. Layer normalization. _arXiv preprint arXiv:1607.06450_ . 

- Tom B Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, et al. 2020. Language models are few-shot learners. _Advances in neural information processing systems_ , 33:1877–1901. 

- Liam Collins, Hamed Qi, Mohammad Ghassemi, and Salman Avestimehr. 2021. Exploiting shared representations for personalized federated learning. In _International Conference on Machine Learning_ , pages 2089–2099. PMLR. 

- Alireza Fallah, Aryan Mokhtari, and Asuman Ozdaglar. 2020. Personalized federated learning with theoretical guarantees: A model-agnostic meta-learning approach. In _Advances in Neural Information Processing Systems_ , volume 33, pages 3557–3568. 

- Flower. 2025. Federated retrieval augmented generation (FedRAG) example. https://flower.ai/ docs/examples/fedrag.html. Accessed on [Insert Access Date]. 

- Avishek Ghosh, Justin Chung, Dong Yin, and Kannan Ramchandran. 2020. An efficient framework for clustered federated learning. In _Advances in Neural Information Processing Systems_ , volume 33, pages 19586–19597. 

- Rachid Guerraoui, Anusha Gupta, Andreas Hellander, Anne-Marie Kermarrec, Nikola Logic, and Rafael Plassier. 2025. Efficient federated search for retrievalaugmented generation. In _Proceedings of the EuroMLSys Conference_ . Based on arXiv:2502.19280. 

- Suchin Gururangan, Ana Marasovi´c, Swabha Swayamdipta, Kyle Lo, Iz Beltagy, Doug Downey, and Noah A Smith. 2020. Don’t stop pretraining: Adapt language models to domains and tasks. In _Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics_ , pages 8342–8360. 

- Dan Hendrycks and Kevin Gimpel. 2016. Gaussian error linear units (gelus). _arXiv preprint arXiv:1606.08415_ . 

- Geoffrey Hinton, Oriol Vinyals, and Jeff Dean. 2015. Distilling the knowledge in a neural network. _arXiv preprint arXiv:1503.02531_ . 

- Tzu-Ming Henry Hsu, Hang Qi, and Matthew Brown. 2019. Measuring the effects of non-identical data distribution for federated visual classification. In _International conference on learning representations_ . 

- Edward J Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu Chen. 2021. LoRA: Low-rank adaptation of large language models. In _International Conference on Learning Representations_ . 

- Kalervo Järvelin and Jaana Kekäläinen. 2002. Cumulated gain-based evaluation of ir techniques. _ACM Transactions on Information Systems (TOIS)_ , 20(4):422–446. 

- Fred Jelinek, Robert L Mercer, Lalit R Bahl, and James K Baker. 1977. Perplexity—a measure of the difficulty of speech recognition tasks. In _The Journal of the Acoustical Society of America_ , volume 62, pages S63–S63. Acoustical Society of America. 

- Ziwei Ji, Nayeon Lee, Rita Frieske, Tiezheng Yu, Dan Su, Yan Xu, Etsuko Ishii, Yejin Bang, Andrea Madotto, and Pascale Fung. 2023. Survey of hallucination in natural language generation. _ACM Computing Surveys_ , 55(12):1–38. 

- Jincheol Jung, Hongju Jeong, and Eui-Nam Huh. 2024. Federated learning and RAG integration: A scalable approach for medical large language models. In _arXiv preprint arXiv:2412.13720_ . 

- Peter Kairouz, H Brendan McMahan, Brendan Avent, Aurélien Bellet, Mehdi Bennis, Arjun Nitin Bhagoji, Kallista Bonawitz, Zachary Charles, Graham Cormode, Rachel Cummings, et al. 2021. Advances and open problems in federated learning. _Foundations and Trends® in Machine Learning_ , 14(1–2):1–210. 

- Eugenia Kim, Jingjing Wang, and Shandong Wu. 2024. Federated learning-enhanced retrieval augmented generation (RAG). Technical Report 8089, Technical Disclosure Commons. 

- Vinayak Kulkarni, Milind Kulkarni, and Anirudh Pant. 2020. Survey of personalization techniques for federated learning. 

- Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Mazar Komeili, et al. 2020a. Retrieval-augmented generation for knowledge-intensive nlp tasks. In _Advances in Neural Information Processing Systems_ , volume 33, pages 9459–9474. 

- Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler, Myle Ott, Wen-tau Chen, Alexis Conneau, et al. 2020b. Retrieval-augmented generation for knowledge-intensive NLP tasks. In _Advances in_ 

14264 

_Neural Information Processing Systems_ , volume 33, pages 9459–9474. 

- Daliang Li and Junpu Wang. 2019. FedMD: Heterogenous federated learning via model distillation. In _arXiv preprint arXiv:1910.03581_ . 

- Tian Li, Anit Kumar Sahu, Manzil Zaheer, Maziar Sanjabi, Ameet Talwalkar, and Virginia Smith. 2020. Federated optimization in heterogeneous networks. In _Proceedings of Machine Learning and Systems_ , volume 2, pages 429–450. 

- Christopher D Manning, Prabhakar Raghavan, and Hinrich Schütze. 2008. _Introduction to information retrieval_ . Cambridge university press. 

- Brendan McMahan, Eider Moore, Daniel Ramage, Seth Hampson, and Blaise Aguera y Arcas. 2017. Communication-efficient learning of deep networks from decentralized data. In _Artificial Intelligence and Statistics_ , pages 1273–1282. PMLR. 

- Milvus Team. 2019–Present. Milvus: A cloud-native vector database for scalable similarity search. https: //milvus.io. 

- Aashiq Muhamed, Ting Zhao, Ahmad Beirami, and Ananda Theertha Suresh. 2024. Cache me if you can: The case for retrieval augmentation (RA) in federated learning. In _ICLR 2024 Workshop on Federated Learning_ . 

- National Center for Biotechnology Information (NCBI). Accessed on May 18, 2025. PubMed Central. 

- Qwen Team. 2024. Qwen2.5 Technical Report. https: //qwenlm.github.io/blog/qwen2.5/. 

- Alec Radford, Karthik Narasimhan, Tim Salimans, and Ilya Sutskever. 2018. Improving language understanding by generative pre-training. _URL https://s3us-west-2. amazonaws. com/openai-assets/researchcovers/language-unsupervised/language understanding paper. pdf_ . 

- Alec Radford, Jeffrey Wu, Rewon Child, David Luan, Dario Amodei, and Ilya Sutskever. 2019. Language models are unsupervised multitask learners. _OpenAI blog_ , 1(8):9. 

- Han Shen, Lichao Zhang, Han Yu, and Xiaoxiao Liu. 2024. FlexLoRA: A flexible aggregation scheme for federated fine-tuning of large language models. In _International Conference on Learning Representations_ . 

- Parshin Shojaee, Shuai Wang, Smita Sharma, Chenguang Wang, Xiaochuan Liu, and Holger R. Roth. 2025. Federated retrieval augmented generation for multi-product question answering. In _Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing_ . Based on arXiv:2501.14998. 

- Nitish Srivastava, Geoffrey Hinton, Alex Krizhevsky, Ilya Sutskever, and Ruslan Salakhutdinov. 2014. Dropout: a simple way to prevent neural networks from overfitting. _The journal of machine learning research_ , 15(1):1929–1958. 

- Lili Su, Connor McLaughlin, and Lichao Zhang. 2024. Federated importance-aware submodel extraction. In _Advances in Neural Information Processing Systems_ , volume 37. Based on NeurIPS 2024 paper. 

- Alysa Ziying Tan, Han Yu, Lizhen Cui, and Qiang Yang. 2022. Towards personalized federated learning. _IEEE Transactions on Neural Networks and Learning Systems_ . 

- Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lachaux, Timothée Lacroix, Baptiste Rozière, Naman Goyal, Eric Hambro, Faisal Azhar, et al. 2023a. Llama: Open and efficient foundation language models. _arXiv preprint arXiv:2302.13971_ . 

- Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, et al. 2023b. Llama 2: Open foundation and fine-tuned chat models. _arXiv preprint arXiv:2307.09288_ . 

- Aaron van den Oord, Yazhe Li, and Oriol Vinyals. 2018. Representation learning with contrastive predictive coding. _Preprint_ , arXiv:1807.03748. 

- Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin. 2017. Attention is all you need. In _Advances in neural information processing systems_ , volume 30. 

- Ellen M Voorhees. 1999. The trec-8 question answering track report. In _Proceedings of the eighth Text REtrieval Conference (TREC-8)_ , volume 99, pages 77–82. National Institute of Standards and Technology (NIST). 

- Liang Wang, Nan Yang, Ruty Fariha, Fnu Mi, and Bo Zhu. 2022. Text embeddings by weaklysupervised contrastive pre-training. _arXiv preprint arXiv:2212.03533_ . 

- Liping Yi, Han Yu, Chao Ren, Heng Zhang, Gang Wang, Xiaoguang Liu, and Xiaoxiao Li. 2023. pFedLoRA: Model-heterogeneous personalized federated learning with LoRA tuning. In _arXiv preprint arXiv:2310.19978_ . 

- Wayne Xin Zhao, Kun Zhou, Junyi Li, Tianyi Tang, Xiaolei Wang, Yupeng Hou, Yingqian Min, Beichen Zhang, Junjie Zhang, Zican Dong, et al. 2023. A survey of large language models. _arXiv preprint arXiv:2303.18223_ . 

14265 

## **A ALGORITHM** 

### **A.1 Federated Tuning Procedure** 

Algorithm 1 summarizes the comprehensive algorithm for federated tuning described in Section 4.2. 

**Algorithm 1** : Federated Tuning Procedure 

- **Input** : clients _N_ , global rounds _T_ , local epochs _E_ , window size _Tw_ , cooling period _Tcool_ , learning rate _η_ , initial parameters ( _ϕ_<sup>_g_</sup> _, ϕ_<sup>_p_</sup> ) 

- **Output** : Globally optimized _ϕ_<sup>_g_</sup> , locally personalized _ϕ_<sup>_p_</sup> _i_ 

- **1 for** _each round t_ = 1 _,_ 2 _, ..., T_ **do 2** Sample client set _A ⊆_ [ _N_ ] Send global shared layer _ϕ_<sup>_g_</sup> _t_<sup>to clients</sup><sup>_i ∈A_</sup><sup>**for**</sup><sup>_each client i ∈A_</sup><sup>**_in_**</sup> **_parallel_ do** 

- **3** Initialize local model ( _ϕ_<sup>_g_</sup> _t_<sup>_, ϕp_</sup> _i,t_<sup>)</sup><sup>**for**</sup><sup>_epoch_</sup> _e_ = 1 _,_ 2 _, ..., E_ **do** 

- **4** Compute local loss _Fi_ via (2) Update ( _ϕ_<sup>_g_</sup> _t_<sup>_, ϕp_</sup> _i,t_<sup>)</sup><sup>_←_(</sup><sup>_ϕ_</sup> _t_<sup>_g, ϕp_</sup> _i,t_<sup>)</sup><sup>_−η∇Fi_</sup> 

- **5** Compute Adaptation Performance Index API _i,t_ ; 

- **6** Update API history buffer _Hi ←Hi ∪{_ API _i,t}_ ; 

- **7 if** _|Hi| ≥ Tw_ **then 8** Compute thresholds _T_ up<sup>(</sup><sup>_i,t_)</sup> , _T_ down<sup>(</sup><sup>_i,t_)based</sup> on recent _Tw_ entries in _Hi_ ; 

- **9** Update counters _c_<sup>(</sup> _s_<sup>_i,t_)</sup> , _c_<sup>(</sup> _l_<sup>_i,t_)</sup> based on API _i,t_ ; 

- **10 if** _adjustment condition met via_ (6) _and not in cooling period_ **then** 

- **11** Perform layer adjustment via KD with the current model as Teacher; 

- **12** During KD, freeze _ϕ_<sup>_g_</sup> and update only _ϕ_<sup>_p_</sup> ; 

- **13** Start cooling period _Tcool_ ; **14** Send updated global layer _ϕ_<sup>_g_</sup> _i,t_<sup>to server</sup> <u>1</u> 

- **15** Aggregate global layer: _ϕ_<sup>_g_</sup> _t_ +1<sup>=</sup> _|A|_ <u>�</u> _i∈A_<sup>_ϕg_</sup> _i,t_ 

## **B FORMULATION** 

### **B.1 API Metrics** 

. **Learning Momentum and Overfitting Penalty** The learning momentum ∆ _Li,t_ is calculated as the ratio of loss reduction over consecutive windows: 


![](P028_images/P028.pdf-0012-08.png)


where _Tw_ is the window size and _Li,t_ is the loss at time step _t_ for client _i_ . 

The overfitting score _Oi,t_ measures the difference between training and validation performance gains: 

_Oi,t_ = max�0 _,_ ∆Recall<sup>train</sup> _i,t_<sup>_−_∆Recalltest</sup> _i,t_ � _,_ (11) where ∆Recall<sup>train</sup> _i,t_ and ∆Recall<sup>test</sup> _i,t_<sup>are calculated</sup> using the same window-based approach as ∆ _Li,t_ . 

**Adaptive Thresholds and Counter Updates** . The dynamic thresholds for the API values are calculated as follows: 


![](P028_images/P028.pdf-0012-13.png)



![](P028_images/P028.pdf-0012-14.png)


The counters for tracking consistent performance patterns are updated according to: 


![](P028_images/P028.pdf-0012-16.png)


### **B.2 Evaluation Metrics** 

The evaluation metrics used in our experiments are formally defined as follows: 


![](P028_images/P028.pdf-0012-19.png)


where _{d_<sup>+</sup> _}_ denotes the single positive document for query _q_ , _RK_ ( _q_ ) is the set of top- _K_ documents retrieved for _q_ , _Q_ is the set of all queries, and rank _q_ is the position of the positive document in the ranking. 


![](P028_images/P028.pdf-0012-21.png)


where rel _j ∈{_ 0 _,_ 1 _}_ indicates the relevance of the document at rank _j_ and IDCG _K_ is the maximum possible DCG for an ideal ranking. 

Since a query has exactly one positive sample, i.e., IDCG _K_ = 1, Recall and NDCG are binary indicators of whether the true document is within Top- _K_ , while MRR and AvgRank are directly determined by the position of that relevant item. 

14266 

## **C PROMPT** 

In this section, we detail the prompt required for our query generation process. For the querydocument pair generation described in Section 5, we utilize a structured prompt with QWen2.5-7binstruct. This prompt is designed to generate 2 diverse and realistic search queries that a user might ask when seeking information contained in the specific medical document chunk. The prompt template is as follows: 

Medical Query Generation Prompt for Searching Document Chunks 

You are a medical literature retrieval expert. Your task is to generate exactly 2 search queries based on the following document passage. First, identify the two main themes or core aspects discussed in the document passage. These should reflect the central topics, conditions, treatments, or research questions. Consider focusing on the title, abstract, or key sections to pinpoint these themes. Then, generate two concise yet informative search queries, each focusing on one of the identified themes. Ensure that each query has a distinct search intent and targets a different main theme. Avoid overlap in focus. Queries should be specific and tied to the document’s content, avoiding broad or generic terms, to retrieve literature relevant to its core contributions. Do not quote the passage directly; instead, abstract core concepts and rephrase them using keywords and terminology researchers or clinicians would use. Consider what researchers or clinicians would search for to find related or expanded studies. Remain objective, avoiding personal biases or assumptions. Output exactly 2 queries, each on a separate line. Input: {Document} Output: {First Query Here} {Second Query Here} 

Table 6: Prompt template for generating medical chunks search queries 

## **D EXPERIMENTS** 

All training-based experiments were conducted on 6 NVIDIA RTX Ada 6000 GPUs. Results are reported as the mean over three independent runs to ensure consistency and mitigate randomness. 

### **D.1 License Discussion** 

In this study, we used the PubMed Central Open Access Subset, whose articles are available under various Creative Commons licenses (e.g., CC0, CC BY, CC BY-SA, CC BY-NC), the Milvus vector database under the Apache License 2.0 (with preservation of LICENSE and NOTICE files on redistribution), and the E5-base-v2 model (intfloat/e5base-v2) under the MIT License (permitting free 

Table 7: Distribution of medical domains across federated clients (%) after Dirichlet partitioning ( _α_ = 0 _._ 3) 

|**Client**|**Card.**|**Rad.**|**Med. Info.**|**Pharm.**|**Neuro.**|**Onc.**|
|---|---|---|---|---|---|---|
|C1|18.65|44.96|0.38|0.00|35.77|0.25|
|C2|99.71|0.14|0.01|0.10|0.03|0.02|
|C3|0.34|0.44|74.25|0.11|0.00|24.86|
|C4|0.23|25.98|9.44|12.66|51.69|0.00|
|C5|26.71|0.34|6.83|13.73|36.70|15.69|
|C6|0.00|12.59|0.18|66.61|7.08|13.53|



use, modification, and redistribution with copyright notice intact). Our use of these artifacts is consistent with their intended research purposes. For the artifacts we create, including embeddings and models derived from these resources, we specify that they are intended for research purposes only and maintain compatibility with the original access conditions of the source materials. Any derivative works produced during this research are not intended for commercial or production use outside research contexts. 

### **D.2 Datasets Statistics** 

The original dataset consists of 32,619 querydocument pairs distributed across six medical domains as follows: Cardiology (9,594 pairs), Radiology (1,919 pairs), Medical Informatics (8,315 pairs), Pharmacy (2,558 pairs), Neuroscience (5,756 pairs), and Oncology (4,477 pairs). 

To simulate realistic non-IID scenarios in federated learning environments, we employed a Dirichlet distribution ( _α_ = 0 _._ 3) to partition these domainspecific query-document pairs across six client nodes. Table 7 shows the resulting data distribution, with each cell representing the percentage of documents from a specific domain allocated to each client. This approach creates significant heterogeneity in the data distribution across clients, reflecting real-world federated scenarios where institutions specialize in different medical fields. 

### **D.3 Parameter Settings** 

HyperParameters. This section presents a detailed overview of the hyperparameter settings used in our experiments. As shown in Table 8, the key parameters were carefully selected and tuned to ensure fair comparisons and optimal performance. Package Parameters. Our implementation leverages the Milvus Standalone version 2.4.13 as the vector database backend with HNSW (Hierarchical Navigable Small World) as the index type and _L_ 2 distance as the metric type. The HNSW con- 

14267 

Table 8: Hyperparameter settings 

|**Parameter**|**Value**|
|---|---|
|_General Training_||
|Embedding Model|intfoat/e5-base-v2(109M)|
|Language Model|QWen/QWen-2.5-7b(7.61B)|
|Communication rounds (_T_)|200|
|Local epochs (_E_)|3<br>|
|Learning rate (_η_)|1e<sup>_−_5</sup>|
|Batch size|512|
|Optimizer|Adam|
|Weight decay (_λ_)|0.01|
|InfoNCE temperature|0.05|
|_Knowledge Distillation_||
|KD temperature (_τ_KD)|3.0|
|KD epochs|50|
|KD learning rate|0.1|
|_Depth Controller_||
|Data complexity score weights|_w_1 = 0_._8,_w_2 = 1_._5,_w_3 = 1_._2|
|API weights|_wL_ = 0_._8,_wO_ = 0_._2|
|Window size (_Tw_)|5|
|Minimum stable rounds (_τs_)|3|
|Maximum low rounds (_τl_)|4|
|Cooling period (_Tcool_)|5|



Table 9: Human Evaluation Scoring Rubric for RAG Response Quality 

|**Score**|**Description of RAG Response Quality**|
|---|---|
|**9–10**|**Excellent:** Comprehensive, highly accurate, directly relevant<br>response that fully addresses all query aspects. Demonstrates<br>excellent synthesis of context information, perfectly faithful<br>to the provided context (no hallucinations). Maintains precise<br>distinctions between medical terms and concepts with no termi-<br>nology confusion.|
|**7–8**|**Good:**Largely correct, relevant response addressing main query<br>aspects. Mostly faithful to context with minimal unsupported<br>claims. Medical terminology is used accurately with minimal<br>ambiguity. Generally coherent and understandable.|
|**5–6**|**Fair:** Response attempts to answer query but has noticeable<br>issues. May be partially correct/complete, contain some termi-<br>nology imprecision, or occasional confusion between related<br>medical concepts.|
|**3–4**|**Poor:** Mostly irrelevant response with signifcant factual inac-<br>curacies or superfcial query coverage. Contains notable un-<br>supported claims, terminology errors, or confation of distinct<br>medical concepts.|
|**1–2**|**Very Poor:** Completely irrelevant, nonsensical, largely incor-<br>rect response with severe medical inaccuracies. Contains fun-<br>damental misunderstandings of medical concepts, dangerous<br>terminology confusion.|



figuration parameters were set to _M_ = 16 and efConstruction = 256, balancing search accuracy with indexing efficiency. For text processing and model interactions, we utilized the transformers library (version 4.48.3), with e5-base-v2’s tokenizer for document chunking operations using a maximum length of 512 tokens. During LLM inference with QWen2.5-7B-Instruct, we employed a carefully tuned parameter set including max_new_tokens=128, temperature=0.4, do_sample=True, top_k=50, top_p=0.9, and repetition_penalty=1.2, with pad_token_id set to the tokenizer’s EOS token ID. Model loading utilized device_map="auto" for optimal GPU allocation, float16 precision for memory efficiency, low_cpu_mem_usage=True to minimize RAM consumption, and trust_remote_code=True to properly handle model-specific optimizations. 

### **D.4 Implementation Details** 

In our human evaluation process, we provided domain experts with a structured scoring rubric, as shown in Table 9, to ensure consistent and objective assessment of RAG response quality. This rubric guided experts to evaluate responses based on medical accuracy, clinical relevance, terminology precision, and overall coherence. Experts were instructed to focus particularly on whether responses maintained proper distinctions between medical terms, accurately represented clinical concepts, and provided information that would be useful in actual medical contexts. 

14268 

