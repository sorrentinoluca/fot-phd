www.nature.com/scientificreports 


![](P027_images/P027.pdf-0001-01.png)

### Figure analysis

The image appears to be the opening page of a Scientific Reports article rather than a scientific data figure.

**Purpose and content:** It identifies the paper, authors, abstract, and keywords. The main article title is **“Dual prompt personalized federated learning in foundation models”**. The abstract states that the work proposes **DP²FL**, a Dual Prompt Personalized Federated Learning framework designed to address heterogeneous client data distributions, limited local client data, and integration of new clients in federated learning settings.

**Important visible components:**
- Journal/source label: `www.nature.com/scientificreports`.
- Article status label: `OPEN`.
- Title: **Dual prompt personalized federated learning in foundation models**.
- Authors: Ying Chang, Xiaohu Shi, Xiaohui Zhao, Zhaohuang Chen, and Deyin Ma.
- Abstract summary: DP²FL combines global task awareness with local data-driven insights using dual prompts and an adaptive aggregation strategy.
- Keywords: Personalized federated learning, Foundation models, Client heterogeneity, Adaptive aggregation strategy.
- A “Check for updates” banner appears at the bottom.

**Direct observations:** The page contains text only, with no axes, plotted data, numerical results, experimental panels, or schematic workflow. The visible abstract emphasizes the use of foundation models such as CLIP, personalized federated learning, dual prompts, adaptive aggregation, and support for newly added clients.

**Interpretation in relation to the paper:** This page establishes the paper’s motivation and claimed contribution: adapting foundation models to personalized federated learning under heterogeneous and limited-data client conditions. It frames DP²FL as a method intended to improve local generalization, preserve personalization, and enable prediction or integration for new clients without full retraining.

**Limitations:** Because the image is a cropped article front page, it does not provide methodological diagrams, quantitative evidence, or experimental comparisons.


# **OPEN Dual prompt personalized federated learning in foundation models** 

**Ying Chang**<sup>**1**</sup> **, Xiaohu Shi**<sup>**1,2**</sup> **, Xiaohui Zhao**<sup>**1**</sup> **, Zhaohuang Chen**<sup>**2**</sup> **& Deyin Ma**<sup>**3**</sup> 

**Personalized federated learning (PFL) has garnered significant attention for its ability to address heterogeneous client data distributions while preserving data privacy. However, when local client data is limited, deep learning models often suffer from insufficient training, leading to suboptimal performance. Foundation models, such as CLIP (Contrastive Language-Image Pretraining), exhibit strong feature extraction capabilities and can alleviate this issue by fine-tuning on limited local data. Despite their potential, foundation models are rarely utilized in federated learning scenarios, and challenges related to integrating new clients remain largely unresolved. To address these challenges, we propose the Dual Prompt Personalized Federated Learning (DP**<sup>**2**</sup> **FL) framework, which introduces dual prompts and an adaptive aggregation strategy. DP**<sup>**2**</sup> **FL combines global task awareness with local data-driven insights, enabling local models to achieve effective generalization while remaining adaptable to specific data distributions. Moreover, DP**<sup>**2**</sup> **FL introduces a global model that enables prediction on new data sources and seamlessly integrates newly added clients without requiring retraining. Experimental results in highly heterogeneous environments validate the effectiveness of DP**<sup>**2**</sup> **FL’s prompt design and aggregation strategy, underscoring the advantages of prediction on novel data sources and demonstrating the seamless integration of new clients into the federated learning framework.** 

**Keywords** Personalized federated learning, Foundation models, Client heterogeneity, Adaptive aggregation strategy 

Recent advancements in deep learning<sup>1</sup> have brought remarkable breakthroughs across diverse domains<sup>2</sup> , such as disease diagnosis<sup>3–5</sup> , facial recognition<sup>6–8</sup> , video recommendation systems<sup>9,10</sup> , and emotion recognition<sup>11,12</sup> . Typically, these methods aggregate all data onto a central server for model training<sup>13</sup> , with model accuracy often strongly correlated with the volume and quality of the data. However, in sensitive fields, centralizing data . introduces significant privacy and security challenges<sup>14</sup> 

To mitigate the issue of data silos, Federated Learning (FL)<sup>15</sup> has emerged as a promising solution, enabling collaborative model training without direct data sharing. Unlike traditional methods, FL allows a global model to be trained by aggregating parameters from locally trained models on client devices. This approach fundamentally changes the data-handling paradigm, allowing data to remain on clients’ devices and only model parameters to be shared with the central server for aggregation. 

Classic federated learning models involve a central server and local clients: in each training round, the server distributes the global model to the clients, who train it on their local data and send the updated parameters back to the server for aggregation into a new global model. While approaches like FedAvg<sup>15</sup> perform well with similar client data distributions, real-world data is often heterogeneous<sup>16</sup> , leading to suboptimal global models. Addressing such data heterogeneity has spurred a new line of research known as Personalized Federated Learning (PFL). 

PFL aims to develop personalized models that closely reflect individual clients’ data distributions, with strict adherence to data privacy and security requirements<sup>17</sup> . PFL can generally be divided into two main categories based on the personalization strategy: Global Model Personalization and Learning Personalized Models<sup>18</sup> . 

In Global Model Personalization, the focus is on adapting the global federated learning model to individual clients through local adaptation. This approach relies on the generalization capability of the global model, as it directly influences the accuracy of each client’s personalized model during local adaptation. To achieve this goal, Duan et al.<sup>19</sup> proposed Astraea, a framework that addresses label imbalance through Z-score-based data 

1College of Software, Jilin University, Changchun 130012, China. 2College of Computer Science and Technology, Jilin University, Changchun 130012, China.<sup>3</sup> College of Computer Science and Engineering, Changchun University of Technology, Changchun 130000, China.<sup></sup> email: shixh@jlu.edu.cn; madeyin@ccut.edu.cn 

**Scientific Reports** |        (2025) 15:28026 

1 

| https://doi.org/10.1038/s41598-025-11864-4 

www.nature.com/scientificreports/ 

augmentation and downsampling. Additionally, it manages data heterogeneity via a Mediator that reschedules training for clients with skewed data. In contrast to this data-centric approach, FedSteg<sup>20</sup> adopts a model-based strategy, wherein transfer learning is utilized to fine-tune the global model for each client after the initial training phase. 

In contrast, the Learning Personalized Models approach modifies the aggregation process to directly address clients’ heterogeneous data. A prominent strategy in this category is parameter decoupling. For instance, Arivazhaga et al.<sup>21</sup> divide client models into a base layer, trained globally, and a personalized layer, trained locally. This configuration allows the global layer to capture generalizable features, while the personalized layer reflects each client’s unique data distribution. Hanzely et al.<sup>22</sup> extend this approach by introducing a penalty term to balance model generalization and personalization. Clustering-based approaches have also shown promise; for example, IFCA<sup>23</sup> assigns clients to clusters of global models that best suit their data, achieving tailored federated learning. 

Despite these advancements, current deep learning frameworks still require large parameter counts, while clients often have limited data, sometimes missing entire classes. Such constraints hinder the adequacy of model training when parameters are aggregated in an FL framework. Large pre-trained Foundation Models, trained on extensive datasets<sup>24</sup> , offer robust feature extraction capabilities beneficial for various tasks. Fine-tuning these models on small local datasets can yield high-performing models, effectively addressing the problem of insufficient local training data. 

Recently, studies like PROMPTFL<sup>25</sup> have begun integrating foundation models into FL, replacing conventional model training with federated prompt training to reduce parameter requirements. This method outperforms both training from scratch and direct fine-tuning but lacks mechanisms for handling client heterogeneity. Moreover, pFedPrompt<sup>26</sup> leverages the multimodal capabilities of CLIP<sup>27</sup> and employs attention mechanisms to effectively capture local client-specific information, thereby enhancing performance in heterogeneous client environments. 

Nevertheless, applications of foundation models in FL are still limited, and existing methods do not address the challenge of integrating new clients dynamically. 

To bridge these gaps, we propose Dual Prompt Personalized Federated Learning in Foundation Models (DP<sup>2</sup> FL), a framework that combines task-awareness with local data-driven insights, effectively leveraging clientspecific information captured through prompts to achieve personalized federated learning based on foundation models. DP<sup>2</sup> FL incorporates two distinct prompts: one that captures federated task information and another that reflects local data distribution. Based on these prompt characteristics, DP<sup>2</sup> FL employs an aggregation strategy that allows clients to benefit from auxiliary training from other clients while maintaining adaptability to their own data. Furthermore, DP<sup>2</sup> FL introduces a global model that can make predictions on data from new sources without requiring their participation in the federated learning process. This model also enables the seamless integration of new clients, facilitating efficient onboarding without retraining from scratch. The core innovations of this work are as follows: 

1. _Dual prompt design_ In the personalized federated learning framework constructed in this work, a novel dual prompt design is proposed: the task prompt for capturing task-level information, and the data prompt for modeling client-specific data distributions–along with corresponding aggregation strategies. 

2. _Global model adaptation_ A global model designed to extend prediction capabilities to new data sources that have not participated in federated learning training. It also ensures seamless integration of newly added clients without requiring retraining, maintaining both flexibility and efficiency. 

## **Related work** 

Foundation models, built upon deep neural networks and self-supervised learning<sup>28</sup> , have gained significant attention in recent years due to their robust generalization capabilities. By training on vast, unannotated datasets<sup>29</sup> , these models acquire rich semantic knowledge, which enhances their applicability across a wide array of downstream tasks and accelerates the adoption of AI in diverse industries<sup>24</sup> . Among these models, OpenAI’s CLIP, a widely recognized Vision-Language Model (VLM), is distinguished by its effectiveness across diverse tasks. This paper leverages CLIP as the foundation model in our proposed personalized federated learning framework, with a brief introduction to CLIP provided below for context. 

As a representative of VLMs, CLIP is pretrained on millions of image-caption pairs, which equips it to simultaneously process textual and visual inputs and learn the semantic relationships between them. Built upon a Transformer<sup>30</sup> architecture, CLIP’s extensive parameters empower it to capture the rich multimodal semantic features essential for a range of applications. However, when applied to domain-specific tasks, CLIP and similar models often encounter limitations due to restricted local training data, resulting in underutilized feature extraction capabilities. To address this challenge, prompt-based learning has emerged as an effective approach, which fine-tunes CLIP’s pretrained knowledge to enable more efficient adaptation to specific tasks. 

Originally developed within natural language processing (NLP), prompt-based learning guides models to generate task-aligned outputs<sup>31</sup> . This strategy has since been applied to computer vision and other domains. For foundational models such as CLIP, BERT<sup>32</sup> , and GPT<sup>33</sup> , a prevalent method involves freezing pretrained parameters while fine-tuning task-specific prompts. This approach enhances task adaptability by capitalizing on the model’s existing knowledge while focusing computational resources on refining prompt parameters, thus improving model performance on downstream tasks. 

As shown in Fig. 1, research on CLIP-based prompting can be categorized into three primary areas: Language Prompting, Visual Prompting, and Multi-modal Prompting<sup>34</sup> . Language Prompting, focuses on the development of learnable textual contexts within CLIP’s text branch to adapt the model for specific downstream tasks. The first work to introduce prompt learning into CLIP was CoOp<sup>35</sup> , which replaced manually crafted prompts with 

**Scientific Reports** |        (2025) 15:28026 

2 

| https://doi.org/10.1038/s41598-025-11864-4 

www.nature.com/scientificreports/ 


![](P027_images/P027.pdf-0003-01.png)

### Figure analysis

The figure illustrates the workflow of a prompt-based CLIP model and visually separates two prompting routes: language prompting in the text branch and visual prompting in the image branch.

- **Language Prompting:**
  - The upper-left panel shows a hand-crafted text prompt, `A photo of a “cls”`, transformed into a learnable prompt form, `xxxx “cls” xxxx`.
  - This prompt passes through a **Text Embed** block, then through a **Text Encoder**.
  - The output is represented as a sequence of text features labeled `T1`, `T2`, `T3`, `...`, `TN`.

- **Visual Prompting:**
  - The lower-left panel shows an input image stack, represented by a dog photograph.
  - The image is visually modified with a prompt-like perturbation or border/padding pattern before entering the image branch.
  - This modified visual input passes through an **Image Embed** block, then through an **Image Encoder**.
  - The output is represented as image features labeled `I1`, `I2`, `I3`, `...`, `IN`.

- **Feature comparison / matching stage:**
  - On the right, text features form the columns of a similarity matrix and image features form the rows.
  - Each cell is labeled as a dot product or similarity score, such as `I1 · T1`, `I1 · T2`, `I2 · T2`, and so on.
  - The highlighted diagonal cells visually indicate matched or corresponding image-text pairs, where `Ii` is compared with `Ti`.

**Direct visual observations:** The diagram uses arrows to show information flow from prompts and images into embedding modules, then into encoders, and finally into a pairwise image-text similarity matrix. The text branch is colored in peach/orange tones, while the image branch is colored in green tones, making the two modalities visually distinct.

**Interpretation:** The figure supports the surrounding discussion that CLIP prompting methods can be categorized by where adaptation occurs: in the language branch, in the visual branch, or in both branches for multimodal prompting. It conveys that prompt learning changes the inputs or context vectors while retaining CLIP’s core text-image matching mechanism based on similarity between encoded representations.


**Fig. 1** . Prompt-based CLIP model 

trainable prompt vectors. This shift enabled more efficient adaptation through few-shot learning, significantly reducing training costs. To further enhance generalization, CoCoOp<sup>36</sup> introduced dynamic adjustments of the trainable prompt vectors in the text branch, using outputs from the image encoder to improve performance across diverse contexts. Recognizing the limitations of a single prompt in capturing both the intrinsic attributes and the extrinsic context of an image, PLOT<sup>37</sup> proposed learning multiple prompts collaboratively, leveraging Optimal Transport (OT) to align the visual and textual modalities. 

Alternatively, Visual Prompting, as illustrated in Fig. 1, focuses on modifying the image branch through visual perturbations to improve model training. Bahng et al.<sup>38</sup> demonstrated the effectiveness of visual prompts for CLIP by exploring three types of prompt applications: random patch insertion, fixed-position patch insertion, and padding. Similarly, ILM-VP<sup>39</sup> explored the influence of label mapping on visual prompting and introduced an automated method for mapping source labels to target labels, which enhanced the accuracy of visual prompts. 

While both Language and Visual Prompting modify a single branch of the CLIP model, they do not fully exploit the model’s multimodal nature. By contrast, Multi-modal Prompting integrates both Language Prompting and Visual Prompting, allowing the model to simultaneously transform both modalities and thus fully leverage CLIP’s inherent multimodal nature. For instance, MaPLe<sup>40</sup> proposed distinct prompts for the text and image branches, which are then coordinated through a coupled adjustment mechanism. This method ensures a high degree of alignment between textual and visual representations, leading to substantial improvements in the model’s generalization ability and its adaptability across different domains. The client-side framework utilized in this study builds on the MaPLe architecture. 

## **Method** 

### **Problem formulation** 

We consider a federated learning scenario involving a set of _K_ clients denoted as _Clinent_ = { _client_ 1, _client_ 2,… , _clientK_ }. Each client _clienti_ possesses a private local dataset _Di_ , which is retained locally and is not accessible to other participants. Unlike traditional approaches that collaboratively train a shared model, our objective is to enable each client to adapt a frozen foundation model(CLIP) using a small number of learnable parameters in the form of prompts. This design reduces the communication and computational overhead and supports personalized adaptation to heterogeneous data distributions. 

The proposed Dual Prompt Personalized Federated Learning (DP<sup>2</sup> FL) framework decomposes the learnable prompt space into two distinct components: a global task prompt _PT_ and a personalized data prompt _Pdi_ for each client _Clienti_ . The global task prompt _PT_ encodes the common semantic knowledge relevant to the federated task and is shared among all clients, while the local data prompt _Pdi_ captures the unique characteristics of client _clienti_ ’s data distribution. 

During local training, each client optimizes its prompts by minimizing the following empirical loss: 

**Scientific Reports** |        (2025) 15:28026 

3 

| https://doi.org/10.1038/s41598-025-11864-4 

www.nature.com/scientificreports/ 


![](P027_images/P027.pdf-0004-01.png)


where _ℓ_ ( _·, ·_ ) denotes the task-specific loss function, and _M_ ( _PT, Pdi, x_ ) represents the output of the frozen foundation model conditioned on both the task and data prompts. 

The overall objective of the DP<sup>2</sup> FL framework is to collaboratively learn a globally shared prompt _PT_ and a set of personalized prompts _{Pdi}i_<sup>_K_</sup> =1<sup>that minimize the aggregated empirical risk across all participating clients.</sup> Formally, the optimization problem is defined as: 


![](P027_images/P027.pdf-0004-04.png)

### Figure analysis

Purpose: These two displayed equations formalize the optimization objective for the proposed Dual Prompt Personalized Federated Learning framework, DP²FL, in the paper’s problem formulation section.

Components and labels:

- Equation (1) defines the empirical loss for client \(i\):

  \[
  \mathcal{L}_i(PT, Pd_i)=\frac{1}{|D_i|}\sum_{(x,y)\in D_i}\ell\left(\mathcal{M}(PT, Pd_i, x), y\right)
  \]

  Important terms:
  - \(D_i\): local private dataset of client \(i\).
  - \((x,y)\in D_i\): input-label examples from that client.
  - \(PT\): globally shared task prompt.
  - \(Pd_i\): personalized data prompt for client \(i\).
  - \(\ell(\cdot,\cdot)\): task-specific loss.
  - \(\mathcal{M}(PT,Pd_i,x)\): output of the frozen foundation model conditioned on both prompts and input \(x\).

- Equation (2) defines the overall optimization problem:

  \[
  \min_{PT,\{Pd_i\}} \sum_{i=1}^{N}\mathcal{L}_i(PT, Pd_i)
  \]

  This states that DP²FL jointly seeks a shared task prompt and a set of personalized client prompts that minimize the sum of client losses.

Direct observations:

- The model parameters of the foundation model are not part of the optimization expression; only prompt variables appear in the objective.
- The first equation averages loss over each client’s local dataset, while the second aggregates losses across clients.
- The two equations encode a two-level structure: local client adaptation through \(Pd_i\), and cross-client sharing through \(PT\).
- The surrounding text describes these prompts as a decomposition of learnable prompt space into global semantic task knowledge and client-specific distributional knowledge.

Interpretation in context:

- Equation (1) supports the paper’s claim that each client can adapt a frozen CLIP-like foundation model using a small number of learnable prompt parameters rather than full model fine-tuning.
- Equation (2) connects the personalized local objectives to a federated learning goal: collaboratively learning a common prompt while preserving personalized prompts for heterogeneous client data.
- The nearby text further explains that aggregated personalized prompts may be used to initialize new clients, making the equations foundational for the later DP²FL framework discussion.

Uncertainty and notation notes:

- The text earlier refers to \(K\) clients, while Equation (2) visibly sums over \(N\); this may be a notation inconsistency unless \(N\) is defined elsewhere.
- These are not chart panels and contain no axes, legends, plotted values, or tabular data.


To further support inference on new data sources and facilitate the seamless integration of newly joined clients, DP<sup>2</sup> FL constructs a global model by aggregating the personalized data prompts _PD_ using the same strategy employed for the global task prompt _PT_ . This enables rapid and effective model initialization without the need for full retraining, ensuring scalability and adaptability in dynamic federated environments. 

### **Framework of DP**<sup>**2**</sup> **FL** 

This study diverges from traditional personalized federated learning approaches by focusing on adapting federated tasks to foundation models. Given the extensive parameter sizes of foundation models and the typically limited data on federated clients, previous research<sup>25</sup> demonstrates that training from scratch or parameter finetuning often fails to maximize these models’ feature extraction capabilities. To address this issue, we propose a prompt-based approach, incorporating a prompt aggregation strategy that optimizes the adaptation of foundation models in federated learning, while minimizing the training parameters required. 

In federated learning, the heterogeneity of local data distributions presents a significant challenge in designing universally effective models. To address this, we introduce a dual-prompt strategy that integrates global task alignment with client-specific data characteristics, ensuring that each client’s model is effectively tailored to its local data while benefiting from collaborative learning. This method relies on prompt learning, where only the task and data prompts are updated during training, while the underlying foundation model (e.g., CLIP) remains frozen. Additionally , we propose a global model that facilitates the efficient initialization of newly added clients during training. Traditional initialization methods often incur substantial computational overhead; in contrast, the global model leverages a generalized prompt to streamline client onboarding, allowing new clients to rapidly integrate into the system without the need for extensive retraining. The detailed model framework is illustrated in Fig. 2. 

The DP<sup>2</sup> FL framework, as depicted in Fig. 2, consists of three critical stages: (a) Initialization, (b) Training Process, and (c) New Client Integration. In the Initialization phase, critical parameters are defined, establishing the foundation for subsequent model training. The Training Process involves iterative refinements of the model, where parameters are updated and aggregated to maintain a balance between generalization and personalization. Finally, the New Client Integration stage tackles the challenge of integrating new clients into the federated task, ensuring their initialization with appropriate parameters, which enables rapid and effective contribution to the learning process. Further details on the CLIP-based Local Model (Fig. 2d) and parameter aggregation strategy are discussed in “Prompt Design” and “Aggregation Protocol” Sections. In addition, the “Privacy Preservation” section addresses the privacy concerns within the framework, detailing mechanisms to protect sensitive data throughout the federated learning process. 

#### _Initialization_ 

The Initialization phase begins with the federated task initiator defining essential parameters, such as the model architecture, parameter configuration, and the number of training rounds. Consistent with standard prompt-based learning models, only the prompt components are updated in this framework, while the core parameters of the foundation model remain fixed. The framework incorporates two types of prompts: the task prompt _Pt_ , which captures global task information, and the data prompt _Pd_ , which adapts to each client’s specific data distribution. The task prompt is shared among all clients to enable collaborative training through the aggregation of data contributions, while each client maintains a unique local data prompt, with aggregation weights determined by evaluating the relevance of other clients’ parameters to the client’s local data. This dualprompt approach ensures the model is tailored to each client’s local data while benefiting from collaborative insights. 

During this phase, each client uploads a small validation dataset, assumed to be the minimal representative subset of its local data distribution, which is considered shareable for federated learning purposes. The server uses this dataset to compute the initial model loss, which is crucial for guiding the aggregation of model parameters in later stages. As the training progresses, each client evaluates whether the results of other clients’ training have improved its model by assessing changes in validation loss. This process guides the parameter aggregation strategy. At the end of the Initialization phase, the server distributes the model parameters, validation data, and loss metrics to all clients, enabling the training process to commence. 

#### _Training process_ 

The Training Process spans _R_ rounds of federated training. In each round _r_ , every client _k_ starts with the global task prompt from the previous round, denoted as _PT_<sup>(</sup><sup>_r−_1)</sup> , and its own local data prompt _Pd_<sup>(</sup> _k_<sup>_r−_1)</sup> , which serve 

**Scientific Reports** |        (2025) 15:28026 

4 

| https://doi.org/10.1038/s41598-025-11864-4 

www.nature.com/scientificreports/ 


![](P027_images/P027.pdf-0005-01.png)


**Fig. 2** . The Framework of DP<sup>2</sup> FL. The DP<sup>2</sup> FL workflow comprises three core components: ( **a** ) Initialization, which establishes the foundation for federated training; ( **b** ) Training Process, which outlines the iterative update and aggregation procedures across clients; ( **c** ) New Client Integration, which demonstrates the dynamic onboarding mechanism for new clients. Additionally, ( **d** ) Local Model illustrates the client-side framework built upon CLIP. 

as initialization parameters for local updates. These prompts are optimized using stochastic gradient descent (SGD) on the client’s local dataset to minimize a task-relevant loss function. The updated prompts obtained after ( _r_ ) ( _r_ ) local training are denoted as _Pt_<sup>˜</sup> _k_<sup>and</sup> _Pd_<sup>˜</sup> _k_<sup>, where the tilde indicates that these are locally optimized prompt</sup> parameters at client _k_ in round _r_ . Formally, the updates can be expressed as: 


![](P027_images/P027.pdf-0005-04.png)


where _Dk_ represents the local dataset of client _k_ . This local update aligns with the personalized objective defined in Eq.1, enabling each client to refine its prompts according to its unique data distribution. Subsequently, each client calculates the loss metrics on all validation datasets using its updated parameters and uploads these metrics. The server consolidates the global task prompt _PT_<sup>(</sup><sup>_r_)</sup> by evaluating the performance of each client on their validation data and adjusting aggregation weights accordingly. Simultaneously, each client locally adjusts its data prompts _Pd_<sup>(</sup><sup>_r_)</sup> by aligning other clients’ training outputs with its specific data distribution. After completing these steps, each client computes the loss on its own validation dataset using the updated _PT_<sup>(</sup><sup>_r_)</sup> and _Pd_<sup>(</sup><sup>_r_)</sup> , uploading these losses to the server. These metrics provide essential feedback for the personalized aggregation in the next training round. 

Since local data prompts are client-specific, new clients joining the federated learning task must initialize either with the local data prompt parameters established during the initialization phase or with random values, which makes it difficult to align with the existing clients. To address this issue, we introduce a global model composed of both task and data prompts. The task prompt corresponds to the global task prompt described earlier, while the data prompt is generated from the local data prompts using an aggregation method similar to that of the global task prompt. This global model provides a generalized initialization mechanism for new clients, leveraging insights from previous training rounds to enhance adaptability and accelerate their integration into the federated learning framework. 

Furthermore, the global model is well-suited for scenarios where new data sources are introduced solely for inference. In such cases, as the data source does not participate in the federated learning process, the global 

**Scientific Reports** |        (2025) 15:28026 

5 

| https://doi.org/10.1038/s41598-025-11864-4 

www.nature.com/scientificreports/ 

model–comprising both the global task prompt and the global data prompt–can efficiently and directly evaluate the new data. 

#### _New client integration_ 

The New Client Integration phase is begun when new clients join the federated learning task, either during or after the training process. The new client initially uploads its validation dataset to the server, which distributes it to existing clients to facilitate subsequent aggregation. The server also provides the latest global model for initialization, which includes both the global task prompt _PT_ and the global data prompt _PD_ . This global model integrates the training results from all prior rounds, enabling it to demonstrate high accuracy directly on the new client’s local dataset. Notably, following initialization, only minimal additional training is needed to adapt the new client’s model to its data. Other clients, in turn, integrate the new client’s contributions, enhancing the federated model as a whole. 

Algorithm 1 presents the complete DP<sup>2</sup> FL framework process across its three stages. 


![](P027_images/P027.pdf-0006-05.png)


**Algorithm 1** . DP<sup>2</sup> FL Framework. 

### **Prompt design** 

In this study, the CLIP model is leveraged as the foundation for each client’s framework, with distinct prompts designed for both the vision and language branches to facilitate cross-modal integration. Specifically, to align visual and textual modalities, a transformation function derives the visual prompt from the textual prompt, as shown in Fig. 2d. 

The CLIP model, employing a Vision Transformer (ViT)<sup>41</sup> as its Image Encoder, comprises a sequence of Transformer blocks within both the Text and Image Encoders. In the text branch, for example, the embedded input text, combined with positional encoding, is provided as input to the first Transformer block of the text encoder, represented as follows in Eq. 4: 


![](P027_images/P027.pdf-0006-10.png)


where _t_ represents the input text, _p_ denotes the position, _Em_  t_ refers to the text embedding, and _En_  t_ is the positional encoding for the text branch, with _En_  t_ ( _p_ ) _∈_ R<sup>_d_t_</sup> matching the dimension of _Em_  t_ ( _t_ ). Here, _⊕_ indicates element-wise addition, which is used to combine the semantic information from the text embedding and the positional information from the positional encoding.Similarly, the image branch provides the input to the initial Transformer block of the image encoder as shown in Eq. 5: 


![](P027_images/P027.pdf-0006-12.png)


where _i_ denotes the input image, and _Em_  i_ and _En_  i_ refer to the image embedding and positional encoding for the image branch, respectively, with _En_  i_ ( _p_ ) _∈_ R<sup>_d_i_</sup> , matching the dimension of _Em_  i_ ( _i_ ). In this framework, we introduce a task prompt _Pt_ for the text branch, which is transformed through a dimensional mapping function _F_ to produce the image prompt _Pi_ for the image branch, as shown in Eq. 6: 


![](P027_images/P027.pdf-0006-14.png)



![](P027_images/P027.pdf-0006-15.png)


**Scientific Reports** |        (2025) 15:28026 

6 

| https://doi.org/10.1038/s41598-025-11864-4 

www.nature.com/scientificreports/ 

where _Pi ∈_ R<sup>_d_i_</sup> and _Pt ∈_ R<sup>_d_t_</sup> . Here, _Pt_ encapsulates the overarching task information within the federated learning setting and is shared uniformly across all clients. Due to the non-identical data distributions typical in federated learning, each client’s transformation function _F_ is adapted via a client-specific parameter set, termed the data prompt _Pd_ , which facilitates personalized adaptation to the client’s local dataset. 

Under this design, the Text Encoder input in the client model is adjusted from _T_ to [ _T, Pt_ ], while the Image Encoder input is modified from _I_ to [ _I, Pi_ ], preserving the remaining architecture of the CLIP model. During local training on a client’s dataset, the parameters of the CLIP model remain fixed, and only the task prompt _Pt_ and data prompt _Pd_ are updated. 

### **Aggregation protocol** 

In this study, aggregation strategies are delineated into Global and Local Aggregation based on the participants involved. As discussed in the previous section, the trainable model parameters include two core components: the task prompt, which encapsulates the overarching federated learning task information and is consistent across all clients, and the data prompt, which is tailored to each client, capturing the unique characteristics of local datasets. The task prompt is derived exclusively through a Global Aggregation protocol managed by the server, whereas each client independently computes its data prompt via a Local Aggregation protocol. To enable inference on new data sources and ensure proper initialization for newly added clients, the server computes a generalized data prompt through the Global Aggregation protocol, thereby generating the global model. 

#### _Global aggregation_ 

To enhance the representation of shared task characteristics in federated learning, the server performs global aggregation on the task prompt. This process, defined in Eq. 7, assigns aggregation weights to client updates based on their performance across all validation datasets, enabling a refined capture of cross-client task information. Following an approach similar to FedFomo<sup>42</sup> , each client contributes a validation dataset aligned with its local data distribution during initialization, enabling weight assignments proportional to each client’s cumulative validation loss. 

In the _r_ -th training round, with _K_ participating clients, the global task prompt _PT_<sup>(</sup><sup>_r_)</sup> is derived as follows: 


![](P027_images/P027.pdf-0007-08.png)


where clients in round _PT_<sup>(</sup><sup>_r_)</sup> _∈r_ R + 1<sup>_d_t_</sup> as the initial task prompt for local updates,  denotes the aggregated global task prompt for round _Pt_<sup>˜</sup> ( _r_ ) _∈_ R _K×rd_ , subsequently distributed to all  t_ is the matrix of task prompts trained independently by each client based on local datasets via stochastic gradient descent (SGD), with each row corresponding to a client’s task prompt vector. The column vector _W_  T_<sup>(</sup><sup>_r_)</sup> _∈_ R<sup>_K_</sup> contains the aggregation weights for each client in round _r_ , where the weight component _w_  t_<sup>(</sup> _k_<sup>_r_) the contribution of client</sup><sup>_k_to the global</sup> task prompt, calculated by: 


![](P027_images/P027.pdf-0007-10.png)


where _loss_<sup>(</sup><sup>_r_)</sup> _i,j_<sup>represents the loss computed by client</sup><sup>_i_using its round-</sup><sup>_r_model on the validation set of client</sup><sup>_j_.</sup> This weighting scheme reduces the aggregation influence of clients with higher validation losses across datasets, thereby refining _PT_<sup>(</sup><sup>_r_)</sup> to better capture the federated task’s overall characteristics. 

In addition to aggregating the task prompt, the server uses the Global Aggregation protocol to compute a global data prompt, which provides a generalized representation distinct from the locally optimized data prompts on each client. Together, these form the global model, which enhances adaptability across clients. When new data sources are introduced for inference, or when a new client joins in round _r_ + 1, initializing its model parameters with the global model ( _PT_<sup>(</sup><sup>_r_)</sup> and _PD_<sup>(</sup><sup>_r_)</sup> ) leverages knowledge from prior rounds, thereby reducing the need for extensive retraining. Experimental validation of this initialization effect is presented in “Performance of Global Model” Section. 

#### _Local aggregation_ 

In federated learning, clients pursue a common objective despite variations in local data distributions. This framework models the shared task objectives through a task prompt, with the server assigning aggregation weights based on each client’s performance across all validation datasets. To address distributional heterogeneity, a data prompt tailored to each client is introduced, enabling local evaluation of models trained by other clients to determine aggregation weights. 

In each training round _r_ , the _K_ clients are divided into three sets based on their contributions to client _k_ : Positive Clients (PC), Retained Negative Clients (RNC), and Discarded Negative Clients (DNC). These sets are formally defined as follows: 


![](P027_images/P027.pdf-0007-16.png)


**Scientific Reports** |        (2025) 15:28026 

7 

| https://doi.org/10.1038/s41598-025-11864-4 

www.nature.com/scientificreports/ 

DNC = {client _i | loss_<sup>(</sup> _i,k_<sup>_r_)</sup><sup>_≥α × loss_(</sup> _k,k_<sup>_r−_1)</sup> _,_ 0 _< i ≤ K_ } (11) where _|_ PC _|_ + _|_ RNC _|_ + _|_ DNC _|_ = _K_ , and _α_ is the loss tolerance threshold, defined by the task initiator to regulate acceptable performance variations. During aggregation in round _r_ , client _i_ is classified into PC set if the model loss _loss_<sup>(</sup><sup>_r_)</sup> _i,k_<sup>on client</sup><sup>_k_’s validation set shows improvement over client</sup><sup>_k_’s loss from previous round,</sup> _loss_<sup>(</sup> _k,k_<sup>_r−_1)</sup> . Otherwise, client i is assigned to RNC or DNC based on its performance relative to the defined threshold. To balance data-specific personalization with generalization, client _k_ aggregates data prompts from the sets _Pd_<sup>(</sup><sup>_r_)</sup> in round _r_ is of Positive Clients (PC) and Retained Negative Clients (RNC). The aggregated data prompt computed as follows: 

_Pd_<sup>(</sup><sup>_r_)</sup> = _Pd_<sup>(</sup><sup>_r−_1)</sup> + diag _W_  d_<sup>(</sup><sup>_r_))</sup><sup>_T_</sup> _×_ **1K** _T ⊗ Pd_ ˜ ( _r_ ) _−_ **1K** _⊗ Pd_ ( _r−_ 1)<sup>)]</sup> (12) [( ( _Pd_ where ˜ ( _r_ ) _∈Pd_ R<sup>(</sup> _K_<sup>_r_)</sup> _×∈d_ _R _d_<sup>_K_</sup> denotes the data prompt computed by each client after training on its dataset. The vector<sup>_×d_d_</sup> represents the locally aggregated data prompt across all clients in round _r_ , and **1K** is a _K_ -dimensional row vector of ones, and _⊗_ denotes the Kronecker product. The matrix _W_  d_<sup>(</sup><sup>_r_)</sup> _∈_ R<sup>_K×K_</sup> represents the aggregation weights, where each element _w_  d_<sup>(</sup> _i,k_<sup>_r_) is the weight of client</sup><sup>_i_when aggregating client</sup> _k_ ’s data prompt. These weights are calculated as follows: 

( _r_ ) _w_  d_<sup>(</sup> _i,k_<sup>_r_)=</sup> { Norm0 ( _w_ _<sup>˜</sup> _di,k_<sup>)</sup> ifotherwiseclient _i ∈_ PC _∪_ RNC (13) ( _r_ ) The initial weight _w_ _<sup>˜</sup> _di,k_<sup>is defined as:</sup> _w_ _˜ _d_ ( _i,kr_ )<sup>=</sup> ~~�~~ <u>��</u> _lossPd_ ˜<sup>(</sup> _k_ ( _i_<sup>_r_</sup> _r,k_<sup>_−_</sup> ) _−_<sup>1)</sup> _Pd− loss_<sup>(</sup> _k_<sup>_r−_1)(</sup> _i,_<sup>_r_</sup> _k_ ~~�~~ <u>��</u><sup>)</sup> (14) ( _r_ ) where _Pd_<sup>˜</sup> _i_ denotes the data prompt of the model trained on client _i_ ’s dataset after the _r_ -th round of iteration, and _Pd_<sup>(</sup> _k_<sup>_r−_1)</sup> represents the aggregated data prompt of client _k_ after the ( _r −_ 1)-th round. ˜ ( _r_ ) ˜ ( _r_ ) From Eq. 14, if client _i ∈_ PC, then _w_  di,k_<sup>_>_0; conversely,client</sup><sup>_i∈_RNC, then</sup> _w_  di,k_<sup>_≤_0. In this</sup> work, the normalization function Norm( ) is defined as follows, depending on whether the PC set is empty: Norm( _w_ _<sup>˜</sup> _d_ ( _i,kr_ )<sup>) =</sup>  _β ×_ <u>∑client</u> _<u>j ∈</u>_ RNC _w_ ˜ _˜ _d_<sup>(</sup> _j,k_<sup>_r_)</sup><sup>_−_</sup> _w_ _˜ _d_<sup>(</sup> _i,k_<sup>_r_)</sup> if _|_ PC _|_ = 0  ~~∑~~ client ~~∑~~ _j_ client _∈_ PC _w_ _˜ _j∪ ∈d_ RNC _i_<sup>(</sup> RNC _<u>,</u>_<sup>_r_</sup> _k_<sup>)</sup><sup>_×_</sup> ~~[~~<sup>sgn</sup> _ww_ __˜<sup>(</sup> _ddw_<sup>(</sup> _j,k_<sup>(</sup> _j,k_ _˜<sup>_rr_))</sup> _d_<sup>_××_(</sup> _i,_<sup>_r_sgn(</sup> _k_<sup>)</sup><sup>_|_RNC)+((</sup> _w_<sup>_γ_</sup> _˜<sup>_|−×_</sup> _dw_<sup>(</sup> _j,k_<sup>1)</sup><sup>_r_</sup> _˜<sup>))+(</sup> _d_<sup>(</sup> _i,_<sup>_r_</sup> _k_<sup>)</sup><sup>_γ_)</sup><sup>_××_</sup> _w_<sup>(1</sup> _˜<sup>_−_</sup> _d_<sup>sgn(</sup> _j,k_<sup>_r_)()</sup> _w_<sup>_×_</sup> _˜<sup>(1</sup> _d_<sup>_−_(</sup> _i,_<sup>_r_sgn</sup> _k_<sup>)))(</sup> _w_ _˜ _d_<sup>(</sup> _j,k_<sup>_r_)))</sup><sup>~~]~~</sup> otherwise (15) where _β_ is a hyperparameter that prevents excessive generalization, _γ_ is an adjustment factor balancing local performance and global generalization, and sgn( ) the sign function defined as: sgn( _x_ ) = { 01 ifotherwise _x <_ 0 _, ._ (16) This aggregation strategy not only utilizes models that perform well on the client’s validation set but also considers models within an acceptable error margin, enabling the local model to effectively generalize while adapting to the specific data distribution of the client. 

### **Privacy preservation** 

Federated learning is fundamentally designed to protect data privacy by ensuring that raw data remains on the client side. In our initial design, clients were required to upload a small validation set to the server as a representative subset of their local data distribution. While this facilitates collaborative validation, it introduces potential privacy concerns, as even small samples may carry sensitive information. To address this, we propose two mechanisms aimed at reducing the privacy risks associated with validation data sharing. 

1. Representation-level sharing instead of raw validation data 

To avoid the direct exposure of raw validation data, this approach eliminates the need for uploading original samples. Each client encodes its local validation set using a shared, frozen pre-trained model to generate 

**Scientific Reports** |        (2025) 15:28026 

8 

| https://doi.org/10.1038/s41598-025-11864-4 

www.nature.com/scientificreports/ 

intermediate textual and visual representations T and I (as defined in Eqs. 4 and 5. Only these embeddings are transmitted to the server. 

Because the backbone encoder is identical and remains frozen throughout training, all clients can utilize the uploaded embeddings by combining them with their own prompts and passing them through the shared encoder to compute validation losses. This procedure maintains validation effectiveness while substantially mitigating the risk of reconstruction or identification attacks. 

#### 2. Anonymous validation via asymmetric encryption 

To enhance privacy and prevent the attribution of validation data to specific clients, we propose an asymmetric encryption mechanism. Prior to training, each client generates a public-private key pair locally. Only the public key and the representation-level information of the validation set are shared, while the private key is securely retained on the client device. During training, each client evaluates its model on the validation data provided by other clients, without knowledge of the data’s origin, thereby ensuring the anonymity of the data providers. 

For effective global aggregation, each client uploads the cumulative loss incurred across all validation sets to the server–specifically, the total loss of client _k_ evaluated on the validation data from all other clients. This scalar loss value does not require encryption, as it is simply a summation that does not reveal sensitive information. _K_ Formally, the cumulative loss for client _k_ in the _r_ -th round is expressed as: ∑ _j_ =1<sup>_loss_</sup> _k,j_<sup>(</sup><sup>_r_)</sup> . This value is uploaded by each client to the server, enabling the server to aggregate these loss values, compute aggregation weights, and update the global prompt accordingly. 

For local aggregation, as the validation embeddings are not linked to explicit client identifiers, each client’s loss on the validation data is encrypted using the corresponding public key. The server aggregates these encrypted losses by public key and then distributes the resulting pairs of (public key, encrypted loss) to all clients. Upon receiving this aggregated data, each client uses its private key to decrypt the entries associated with its own public key. This allows the client to retrieve the performance evaluation of its validation set while maintaining privacy, ensuring that both the validation data and client identity remain decoupled throughout the process. 

These two mechanisms jointly support collaborative validation without revealing raw validation data. They reduce the risks of data reconstruction and attribution, and align well with the federated learning principle of keeping data local. As a result, the proposed design enhances privacy guarantees while maintaining the effectiveness of model validation. 

## **Experiment Experiment setup** 

#### _Datasets_ 

To assess the generalizability of the proposed model framework across diverse data domains, this study . evaluates its performance on eight distinct image classification datasets, following the methodologies in<sup>27,35,36</sup> These include Caltech101<sup>43</sup> , which is widely used for general object detection; DTD<sup>44</sup> , specialized for texture classification; EuroSAT<sup>45</sup> , focused on categorizing Sentinel-2 satellite imagery; FGVCAircraft<sup>46</sup> , a benchmark for aircraft recognition; Food101<sup>47</sup> , tailored for food classification tasks; Flowers102<sup>48</sup> , dedicated to identifying flower species; OxfordPets<sup>49</sup> , designed for pet breed classification; and UCF101<sup>50</sup> , a leading resource for action recognition studies. Together, these datasets provide a rigorous assessment of the model’s cross-domain applicability. 

#### _Heterogeneity simulation_ 

To simulate the non-iid data distributions encountered in real-world federated learning scenarios, we adopt a data-sampling methodology similar to<sup>51,52</sup> , constructing heterogeneous client datasets that test the framework’s ability to leverage foundation models for feature extraction. Following the ”16-shot” approach as implemented in CLIP, each client’s dataset is constrained to a maximum of 16 samples per category. 

For constructing each client’s local dataset, we randomly exclude 20% of the available categories to model data sparsity. Among the remaining categories, 25% of the data is retained, resulting in a 4-shot structure per category. To further accentuate data heterogeneity, a dominant class is identified randomly for each client; 75% of the data points in this class are then added to the client’s local training set. Both the test and validation datasets are designed to align with each client’s training distribution, ensuring consistency across the training, validation, and inference phases. The test dataset is the largest subset that reflects the training distribution, while the validation dataset is the smallest subset. Furthermore, there is no overlap between the datasets used in the training, validation, and inference phases, ensuring mutual exclusivity. 

To enhance understanding of the heterogeneous data distributions in the federated learning setup, a pie chart is presented in Fig. 3, visualizing the data distribution across different categories for the first client’s dataset, using the OxfordPets dataset as an example. The chart highlights the randomly excluded categories, which simulate the data sparsity often encountered in federated learning. Class imbalances and the dominance of a randomly selected class are also emphasized, reflecting the challenges posed by non-iid data distributions. These features underscore the data heterogeneity that the model is designed to address in the simulation process. 

#### _Baselines_ 

Due to the limited research on federated learning with foundation models and the lack of direct comparison methods, we benchmark our framework by integrating traditional personalized federated learning models with the proposed PromptFL<sup>25</sup> . Specifically, the evaluation includes three baseline models: Local, FedProx<sup>53</sup> +PromptFL(FP+P), and pFedMe<sup>54</sup> +PromptFL(pF+P), providing comparative insights into the model’s effectiveness across varied federated learning strategies. 

**Scientific Reports** |        (2025) 15:28026 

9 

| https://doi.org/10.1038/s41598-025-11864-4 

www.nature.com/scientificreports/ 


![](P027_images/P027.pdf-0010-01.png)


**Fig. 3** . Visualization of data distribution across different classes in OxfordPets dataset. 

1. _Local_ A baseline where each client trains independently on its local data without communication or model aggregation, serving as a non-collaborative reference point. 

2. _FedProx+PromptFL (FP+P)_ FedProx extends the standard FedAvg algorithm by introducing a proximal term to handle heterogeneous data across clients. FedProx+PromptFL combines this approach with the PromptFL method, where clients collaboratively learn task-specific prompts rather than models, enabling federated participants to fine-tune foundation models using minimal local data. 

3. _pFedMe+PromptFL(pF+P)_ pFedMe personalizes federated learning by optimizing both global and local objectives using Moreau envelopes. pFedMe+PromptFL enhances this by learning personalized prompts for each client, allowing for improved adaptation to client-specific data and tasks. 

#### _Training details_ 

Building on the pre-trained ViT-B/16<sup>41</sup> CLIP model, as outlined in MaPLe<sup>40</sup> , the client local model framework in this study is optimized using stochastic gradient descent (SGD) with a learning rate of 0.035. Following the methodology of FedPrompt<sup>55</sup> , the setup includes a centralized server and _K_ = 10 clients engaged in _R_ = 10 rounds of iterative training. In each round, clients conduct five epochs with a batch size of four. For local aggregation, parameters are set to _α_ = 1 _._ 2, _β_ = 0 _._ 2, with the weight adjustment factor _γ_ defined as follows: 


![](P027_images/P027.pdf-0010-08.png)


where _w_  d_<sup>(</sup> max<sup>_r_)</sup> _,k_<sup>represents the highest initial aggregation weight among clients in the current RNC set of the</sup> _k_ -th client, while _w_  d_<sup>(</sup> min<sup>_r_)</sup> _,k_<sup>denotes the lowest initial aggregation weight in the PC set of the</sup><sup>_k_-th client. All</sup> experiments are conducted using PyTorch on an NVIDIA RTX 3090 GPU. 

### **Performance of DP**<sup>**2**</sup> **FL on heterogeneous data distributions** 

To validate the efficacy of the proposed parameter aggregation method, comparative experiments were conducted against traditional personalized federated learning approaches, specifically FedProx and pFedMe. Initial results indicate that PromptFL, when applied to training or fine-tuning foundation models from scratch, incurs substantial communication costs and fails to achieve optimal accuracy. Given space constraints, comparisons with scratch training and fine-tuning are omitted. Instead, FedProx and pFedMe frameworks are adapted to integrate PromptFL, restricting training and aggregation to the prompt parameters alone and aligning with the client model structure employed in this work. For quantitative evaluation, the mean accuracy and F1 scores over 10 clients across eight benchmark datasets are reported in Table 1, illustrating the comparative performance of the proposed aggregation strategy. 

**Scientific Reports** |        (2025) 15:28026 

10 

| https://doi.org/10.1038/s41598-025-11864-4 

www.nature.com/scientificreports/ 

||**ACC**||||**Micro-**|**F1**|||
|---|---|---|---|---|---|---|---|---|
|**Dataset**|**Local**|**FP+P**|**pF+P**|**DP**<sup>**2**</sup>**FL**|**Local**|**FP+P**|**pF+P**|**DP**<sup>**2**</sup>**FL**|
|Caltech101|94.51|**94.98**|94.57|_94.66_|93.02|**94.18**|93.71|_93.96_|
|DTD|68.53|_73.26_|72.77|**73.78**|64.20|_70.29_|70.05|**71.14**|
|EuroSAT|78.53|_83.14_|81.37|**84.18**|78.16|_82.99_|81.22|**84.18**|
|FGVCAircraf|**43.90**|41.15|41.43|_41.81_|34.15|_37.07_|**37.17**|37.06|
|Food101|87.32|_88.84_|88.74|**89.06**|86.05|_87.92_|87.78|**88.12**|
|Flowers102|93.34|95.22|_95.27_|**95.50**|_91.59_|94.41|94.45|**94.91**|
|OxfordPets|93.15|94.91|**95.16**|_94.95_|92.16|_94.35_|**94.61**|94.21|
|UCF101|82.47|**83.74**|_83.13_|83.11|78.84|**82.11**|_81.61_|81.10|
|AVG|80.22|_81.90_|81.55|**82.13**|77.27|_80.42_|80.07|**80.59**|



**Table 1** . Comparison results with baselines. Bold values indicate the best performance, and italic values indicate the second best within the same metric across all models. Subsequent tables follow the same convention. 


![](P027_images/P027.pdf-0011-03.png)

### Figure analysis

The figure is a grouped bar chart summarizing per-client performance across eight datasets, intended to show whether the proposed DP²FL framework performs consistently across heterogeneous clients.

**Chart structure and labels**

- Caption/title context: *Client Performance Across Eight Datasets: Average Accuracy and F1 Score*.
- X-axis: **Client ID**, with clients 1 through 10.
- Y-axis: **Score (%)**, spanning approximately 70% to 85%.
- Legend:
  - Blue bars: **Accuracy**.
  - Orange bars: **F1 Score**.
- No error bars or uncertainty intervals are shown.

**Readable values**

| Client ID | Accuracy (%) | F1 Score (%) |
|---:|---:|---:|
| 1 | 82.99 | 81.15 |
| 2 | 82.21 | 80.19 |
| 3 | 82.50 | 81.09 |
| 4 | 82.26 | 79.98 |
| 5 | 81.81 | 80.56 |
| 6 | 80.67 | 79.89 |
| 7 | 82.15 | 80.76 |
| 8 | 83.14 | 81.55 |
| 9 | 81.57 | 80.40 |
| 10 | 82.01 | 80.29 |

**Direct visual observations**

- Accuracy is higher than F1 score for every client.
- Client 8 has the highest accuracy, **83.14%**, and the highest F1 score, **81.55%**.
- Client 6 has the lowest accuracy, **80.67%**, and the lowest F1 score, **79.89%**.
- Accuracy values are narrowly distributed from **80.67% to 83.14%**.
- F1 scores are also narrowly distributed from **79.89% to 81.55%**.
- The gap between accuracy and F1 score varies by client, appearing largest for client 4 and smallest for client 6 based on the labeled values.

**Interpretation in relation to the paper text**

The surrounding text states that this histogram illustrates the average accuracy and F1 scores for each client across eight datasets and argues that DP²FL exhibits relatively uniform performance under non-iid federated learning conditions. The visual evidence supports that claim: both metrics remain within a small range across all 10 clients, suggesting stable client-level performance rather than strong client-specific degradation. However, because no variance measures or statistical tests are shown, the figure visually supports consistency but does not by itself quantify statistical significance.


**Fig. 4** . Client Performance Across Eight Datasets: Average Accuracy and F1 Score. 

As shown in Table 1, the proposed framework consistently achieves strong performance across eight datasets, securing the highest accuracy on four datasets and the second-highest on three, resulting in an average accuracy improvement of 0.23% over the closest competitor. In terms of Micro-F1, DP2FL achieves the highest rank on four datasets and the second-highest on one, with an average improvement of 0.17% over the second-best method (FP+P). Performance gains are particularly notable on the EuroSAT and Food101 datasets, underscoring the efficacy of the proposed prompt-based aggregation approach. These findings validate the effectiveness of the method in handling heterogeneous client data distributions, surpassing the results of traditional personalized federated learning models and reinforcing its adaptability across diverse data settings. 

To further illustrate the consistency of DP<sup>2</sup> FL’s performance, Fig. 4 shows a histogram of the average accuracy and F1 scores for each client across the eight datasets. The results demonstrate that the model exhibits relatively FL uniform performance across all clients, reflecting the robustness and strong generalization capability of DP<sup>2</sup> in federated learning scenarios with non-iid data distributions. 

### **Performance of global model** 

Traditional personalized federated learning methods typically address the variability in local dataset distributions by assigning distinct model parameters to each client. However, these methods fail to account for challenges related to inference on new data sources or the integration of new clients during training, particularly with respect to parameter initialization. To overcome this limitation, we propose a global model that aggregates a generalized data prompt in the same manner as the task prompt. The necessity and effectiveness of this approach are rigorously validated through a series of experiments presented in this section. 

**Scientific Reports** |        (2025) 15:28026 

11 

| https://doi.org/10.1038/s41598-025-11864-4 

www.nature.com/scientificreports/ 

Two targeted experiments are conducted to validate the proposed approach. In the first experiment, the average performance of local models trained on the datasets of 10 clients is compared with that of a global model tested on the datasets of all clients. This comparison provides insights into the generalization ability of the global model across different data distributions. In the second experiment, a new client (the 11th client) is introduced. First, the local models trained on the datasets of the initial 10 clients are evaluated on the new data source (the 11th client), and the performance difference between this evaluation and the global model initialization is compared, highlighting the global model’s effectiveness for inference on new data sources. Then, the model is initialized using various methods to demonstrate the role of the global model in initializing new clients. Finally, a round of federated training is conducted, where the newly initialized model is trained alongside the remaining 10 clients. The results show that proper initialization enables the new client to achieve better performance with only a few federated learning iterations. 

#### (1) Performance of global model on non-local datasets 

The global model is pivotal in managing new data sources that cannot directly participate in federated learning. It facilitates inference by enabling accurate predictions on unseen data without requiring retraining. To achieve this, the global model must exhibit strong generalization capabilities, integrating knowledge from multiple clients to effectively address diverse data distributions. Additionally, when new clients join the federated system, the global model should provide an efficient initialization to enable rapid adaptation to local data. Thus, robust generalization is critical not only for inference on unseen data but also for the seamless integration of new clients, enhancing the model’s applicability in real-world federated learning scenarios. 

To assess the effectiveness of the global model, a comparative analysis is conducted between the local models and the global model. The results of this comparison are presented in Table 2. In this table, Ave_Local represents the average accuracy of the local models trained within the DP<sup>2</sup> FL framework and tested on their respective local datasets. In contrast, Global Model refers to the average accuracy of the global model, initialized with global data and task prompts, and tested across each client’s dataset. The Diff column displays the accuracy difference between the global model and the local models, calculated as the accuracy of the global model (Global Model) minus that of the local models (Ave_Local). 

As shown in Table 2, the results indicate that the global model performs slightly worse than the locally personalized models across all datasets. The average accuracy difference between the global model (Global Model) and the local models (Ave_Local) is − 0.33%, reflecting a marginal decline in performance when using the global model. Notably, the global model’s accuracy closely aligns with that of the local models on datasets such as OxfordPets and Food101, with minimal differences of − 0.09% and − 0.15%, respectively. 

The experimental results suggest that the global model demonstrates strong generalization capabilities, enabling effective inference on new, unseen data sources and efficient initialization of newly added clients. 

#### (2) Performance of the global model in new client initialization 

Building on the findings from the first experiment, which demonstrated the global model’s strong generalization ability, this experiment further investigates its performance when new clients are introduced. Specifically, it evaluates the model’s inference ability on new data sources and examines how different initialization strategies affect the performance of newly added clients in the federated learning process. The experiment consists of three parts: First, it compares the global model’s inference performance on new data sources with that of locally trained models from other clients. Second, it applies various initialization strategies to the newly added client’s model, assessing their impact on performance with the client’s local dataset. Finally, the results show that after effectively initializing the new client’s model, only a minimal number of federated learning iterations are required to achieve strong performance across diverse datasets. 

Table 3 presents the results for the first two parts of this experiment. The methods are described as follows: Ave_Local represents the average accuracy when the original 10 clients perform inference on the new client’s dataset using their locally trained models. Global Model uses the global model, initialized with both task and data prompts aggregated through global aggregation, specifically _PT_<sup>(</sup><sup>_R_)</sup> and _PD_<sup>(</sup><sup>_R_)</sup> and then performs inference to obtain the resulting accuracy. This forms the first part of the comparison. In the second part, additional initialization methods are explored: Init initializes the new client’s model with parameters set by the 

|**Dataset**|**Ave_local**|**Global model**|**Dif**|
|---|---|---|---|
|Caltech101|94.66|94.29|− 0.37|
|DTD|73.78|73.52|− 0.26|
|EuroSAT|84.18|83.94|− 0.24|
|FGVCAircraf|41.81|41.17|− 0.64|
|Food101|89.06|88.91|− 0.15|
|Flowers102|95.50|94.80|− 0.70|
|OxfordPets|94.95|94.86|− 0.09|
|UCF101|83.11|82.89|− 0.22|
|AVG|82.13|81.80|− 0.33|



**Table 2** . Performance of global model on non-local datasets. 

**Scientific Reports** |        (2025) 15:28026 

12 

| https://doi.org/10.1038/s41598-025-11864-4 

www.nature.com/scientificreports/ 

|**Dataset**|**Ave_local**|**Global model**|**Init**|**InitGlo**|
|---|---|---|---|---|
|Caltech101|97.37|97.84|95.69|96.55|
|DTD|67.12|67.14|43.03|63.83|
|EuroSAT|84.00|83.85|45.21|78.35|
|FGVCAircraf|41.56|41.90|26.07|41.31|
|Food101|89.14|89.15|87.36|88.91|
|Flowers102|92.58|91.82|69.50|90.88|
|OxfordPets|95.76|96.10|87.79|95.90|
|UCF101|82.73|82.91|63.12|79.27|
|AVG|81.28|81.34|64.72|79.38|



**Table 3** . Results for new clients under different parameter initialization methods without training. 

||**New**|||**Local**|||**All**|||
|---|---|---|---|---|---|---|---|---|---|
|**Dataset**|**Init**|**InitGlo**|**Global Model**|**Init**|**InitGlo**|**Global model**|**Init**|**InitGlo**|**Global model**|
|Caltech101|97.84|97.84|97.84|94.85|94.84|94.84|95.17|95.29|95.31|
|DTD|67.61|66.43|69.74|72.68|72.81|73.42|67.22|67.39|67.61|
|EuroSAT|82.13|82.31|83.27|83.00|83.58|84.14|80.54|81.14|81.31|
|FGVCAircraf|42.26|43.69|44.40|41.86|42.67|42.38|35.56|36.01|36.00|
|Food101|89.36|89.26|89.47|89.09|89.10|89.05|87.36|87.34|87.29|
|Flowers102|92.77|93.40|92.45|94.89|95.41|95.47|92.72|93.57|93.59|
|OxfordPets|95.79|95.69|95.69|94.90|94.83|94.87|93.50|93.50|93.47|
|UCF101|83.58|82.50|83.31|83.11|83.03|83.06|80.44|80.54|80.56|
|AVG|81.42|81.39|82.02|81.80|82.04|82.15|79.06|79.35|79.39|



**Table 4** . Comparison results on different test data after one round training. 

task initiator, specifically _PT_<sup>(0)</sup> and _PD_<sup>(0)</sup> ; InitGlo initializes the task prompt using global parameters based on the aggregation method, while the data prompt is initialized with parameters from the task initiator, i.e., _PT_<sup>(</sup><sup>_R_)</sup> and _PD_<sup>(0)</sup> . 

In the first part of the experiment, the 11th client is treated as a new data source. Without the global model, each client would likely have to rely solely on its locally trained model to handle the new data. To evaluate the effectiveness of the global model for inference on new data, we compared it with the Ave_Local method. As shown in Table 3 (first and second columns), the global model generally outperforms the average of the local models across most datasets. For instance, on the Caltech101 dataset, the global model achieves an accuracy of 97.84%, which is higher than the 97.37% of the average local model. Similarly, on OxfordPets, the global model reaches 96.10%, compared to 95.76% from the local models. In several other datasets, such as DTD and Food101, the global model shows an improvement over the average local model, although the difference is not always substantial. 

This comparison confirms the advantage of using the global model for inference on new data sources, demonstrating its value in federated learning systems and validating its capability to handle new data sources effectively. 

The second part of the experiment evaluates the effectiveness of the global model for new client integration, as shown in the last three columns of Table 3 . The Global Model consistently outperforms both Init and InitGlo, achieving the highest accuracy across all datasets. Specifically, the global model improves accuracy by an average of 1.96% compared to InitGlo, and by 16.62% compared to Init. 

The results from this part highlight the effectiveness of the global model in initializing new clients within federated learning systems, demonstrating its ability to facilitate direct adaptation to the data distribution of newly added clients. 

To further validate that proper initialization of the newly added client leads to good performance with fewer subsequent federated learning iterations, this section presents the third part of the experiment. As shown in Table 4, three distinct test metrics are considered: New, which represents the accuracy of the newly added (11th) client’s model on its own local dataset after one round of federated training; Local, which refers to the average accuracy of all 11 clients evaluated on their respective local datasets; and All, which indicates the average accuracy of all 11 clients, where each client’s model is evaluated on the combined test sets using their individual parameters. 

4 The results presented in Table demonstrate the efficacy of the proposed initialization method, which significantly facilitates the adaptation of the newly added client to various data distribution with minimal training. Notably, the Global Model initialization method consistently outperforms the other initialization strategies (Init and InitGlo) across all performance metrics: New, Local, and All. 

**Scientific Reports** |        (2025) 15:28026 

13 

| https://doi.org/10.1038/s41598-025-11864-4 

www.nature.com/scientificreports/ 

In particular, the newly introduced client achieves the highest accuracy on its local test set with the Global Model across most datasets, as shown in the New column of Table 4. While there are a few cases (e.g., Caltech101) where Init and InitGlo show similar performance, the Global Model consistently yields the best average results. This demonstrates its effectiveness in helping the new client quickly adapt to its local data distribution. 

Regarding the performance of existing clients, the Local column indicates that Global Model also leads to the highest average accuracy for the models of all 11 clients. In particular, datasets like DTD, EuroSAT, and Flowers102 show significant improvements with Global Model, highlighting the benefit of this initialization strategy in enabling existing clients to better utilize the new data introduced by the added client. 

Finally, when evaluating the aggregated performance across all clients (the All column), Global Model consistently outperforms the other initialization methods. Compared to Init and InitGlo, Global Model demonstrates a clear advantage, particularly on datasets such as DTD and Flowers102. By achieving the highest accuracy on the combined test sets, it showcases its superior generalization ability across diverse data distributions, making it the most robust initialization strategy for federated learning scenarios. 

In summary, the third part of the experiment demonstrates that by initializing new clients with the global model, only a few rounds of federated training are required to achieve strong performance across various datasets. Together, the three experiments further validate the global model’s robust generalization ability, underscoring its potential for inference on new data sources and for efficiently initializing newly added clients. 

## **Conclusion** 

Federated learning in heterogeneous environments presents significant challenges, primarily due to the substantial variation in local data distributions and the frequent addition of new clients. To address these challenges, we propose the Dual Prompt Personalized Federated Learning (DP<sup>2</sup> FL) framework. This framework leverages a dual-prompt mechanism and adaptive aggregation strategies to effectively integrate global task information with client-specific data. It enhances the model’s generalization to global tasks while accommodating the unique characteristics of each client’s local distribution. 

A key innovation of DP<sup>2</sup> FL is the introduction of a novel global model, which enables high-accuracy inference on new data sources that have not participated in federated learning. It also facilitates the seamless integration of new clients into the federated learning process. Empirical results demonstrate that DP<sup>2</sup> FL enhances model performance across diverse client distributions, improves inference accuracy on unseen data, and reduces the onboarding time for new clients, thereby increasing its practical applicability. 

## **Data availability** 

The datasets used in this study are all publicly available and widely adopted in the research community. Specifically, the following datasets were utilized: Caltech101<sup>43</sup> for general object detection, DTD<sup>44</sup> for texture classification, EuroSAT<sup>45</sup> for Sentinel-2 satellite imagery categorization, FGVCAircraft<sup>46</sup> for aircraft recognition, Food101<sup>47</sup> for food classification tasks, Flowers102<sup>48</sup> for flower species identification, OxfordPets<sup>49</sup> for pet breed classification, and UCF101<sup>50</sup> for action recognition studies. These datasets are accessible through their respective repositories: Caltech101:  h t t p : / / w w w . v i s i o n . c a l t e c h . e d u / I m a g e _ D a t a s e t s / C a l t e c h 1 0 1 /. DTD:  h t t p s : / / w w w . r o b o t s . o x . a c . u k / ~ v g g / d a t a / d t d / . EuroSAT: http://madm.dfki.de/files/sentinel/EuroSAT.zip. FGVCAircraft:  h t t p : / / w w w . r o b o t s . o x . a c . u k / ~ v g g / d a t a / f g v c - a i r c r a ft  /. Food101:  h t t p s : / / d a t a . v i s i o n . e e . e t h z . c h / c v l / d a t a s e t s _ e x t r a / f o o d - 1 0 1 /. Flowers102: http://www.robots.ox.ac.uk/~vgg/data/flowers/102/. OxfordPets:  h t t p s : / / w w w . r o b o t s . o x . a c . u k / ~ v g g / d a t a / p e t s / . UCF101: h t t p s : / / d r i v e . g o o g l e . c o m / fi  l e / d / 1 0 J q o m e 3 v t U A 2 k e J k N a n A i F p g b y C 9 H c 2 O / v i e w. These datasets ensure reproducibility of the experiments and facilitate further research. 

Received: 6 March 2025; Accepted: 14 July 2025 


![](P027_images/P027.pdf-0014-11.png)

### Figure analysis

The image is not a scientific data figure; it is a bibliographic text snippet stating **"Published online: 31 July 2025"**.

Direct observations:
- The only readable content is the publication status and date.
- No panels, axes, legends, experimental results, diagrams, images, or quantitative comparisons are present.

Connection to surrounding paper text:
- The surrounding text includes the end matter of the article, including data availability, received and accepted dates, and the start of the references section.
- This snippet likely belongs to the publication metadata near the article footer or header and helps establish the final online publication timeline.

Interpretation:
- The date indicates that the paper became available online after acceptance on 14 July 2025, consistent with standard journal production chronology.


## **References** 

1. Yang, Q., Liu, Y., Chen, T. & Tong, Y. Federated machine learning: Concept and applications. _ACM Trans. Intell. Syst. Technol. (TIST)_ **10** , 1–19 (2019). 

2. Talaei Khoei, T., Ould Slimane, H. & Kaabouch, N. Deep learning: Systematic review, models, challenges, and research directions. _Neural Comput. Appl._ **35** , 23103–23124 (2023). 

3. Ávila-Jiménez, J. L., Cantón-Habas, V., del Pilar Carrera-González, M., Rich-Ruiz, M. & Ventura, S. A deep learning model for Alzheimer’s disease diagnosis based on patient clinical records. _Comput. Biol. Med._ **169** , 107814 (2024). 

4. Kusumoto, D. et al. A deep learning-based automated diagnosis system for spect myocardial perfusion imaging. _Sci. Rep._ **14** , 13583 (2024). 

5. Eskandari, A. & Sharbatdar, M. Efficient diagnosis of psoriasis and lichen planus cutaneous diseases using deep learning approach. _Sci. Rep._ **14** , 9715 (2024). 

6. Wang, M. & Deng, W. Deep face recognition: A survey. _Neurocomputing_ **429** , 215–244 (2021). 

7. He, L. et al. Lmtformer: Facial depression recognition with lightweight multi-scale transformer from videos. _Appl. Intell._ **55** , 195 (2025). 

8. Ma, J. Face recognition technology and privacy protection methods based on deep learning. in _International Conference on Computer Application and Information Security (ICCAIS 2023)_ , vol. 13090, 899–904 (SPIE, 2024). 

9. Karatzoglou, A. & Hidasi, B. Deep learning for recommender systems. in _Proceedings of the Eleventh ACM Conference on Recommender Systems_ 396–397 (2017). 

10. Xiang, Y., Huo, S., Wu, Y., Gong, Y. & Zhu, M. Integrating AI for enhanced exploration of video recommendation algorithm via improved collaborative filtering. _J. Theory Pract. Eng. Sci._ **4** , 83–90 (2024). 

11. Akinpelu, S., Viriri, S. & Adegun, A. An enhanced speech emotion recognition using vision transformer. _Sci. Rep._ **14** , 13126 (2024). 

12. Singla, C., Singh, S., Sharma, P., Mittal, N. & Gared, F. Emotion recognition for human-computer interaction using high-level descriptors. _Sci. Rep._ **14** , 12122 (2024). 

13. Guendouzi, B. S., Ouchani, S., Assaad, H. E. & Zaher, M. E. A systematic review of federated learning: Challenges, aggregation methods, and development tools. _J. Netw. Comput. Appl._ **220** , 103714 (2023). 

**Scientific Reports** |        (2025) 15:28026 

14 

| https://doi.org/10.1038/s41598-025-11864-4 

www.nature.com/scientificreports/ 

14. Huang, R.-Y., Samaraweera, D. & Chang, J. M. Exploring threats, defenses, and privacy-preserving techniques in federated learning: A survey. _Computer_ **57** , 46–56 (2024). 

15. McMahan, B., Moore, E., Ramage, D., Hampson, S. & y Arcas, B. A. Communication-efficient learning of deep networks from decentralized data. in _Artificial Intelligence and Statistics_ 1273–1282 (PMLR, 2017). 

16. Gao, D., Yao, X. & Yang, Q. A survey on heterogeneous federated learning. arXiv preprint arXiv:2210.04505 (2022). 

17. Sabah, F. et al. Model optimization techniques in personalized federated learning: A survey. _Expert Syst. Appl._ **243** , 122874 (2024). 

18. Tan, A. Z., Yu, H., Cui, L. & Yang, Q. Towards personalized federated learning. _IEEE Trans. Neural Netw. Learn. Syst._ **34** , 9587–9603 (2022). 

19. Duan, M. et al. Self-balancing federated learning with global imbalanced data in mobile systems. _IEEE Trans. Parallel Distrib. Syst._ **32** , 59–71 (2020). 

20. Yang, H., He, H., Zhang, W. & Cao, X. Fedsteg: A federated transfer learning framework for secure image steganalysis. _IEEE Trans. Netw. Sci. Eng._ **8** , 1084–1094 (2020). 

21. Arivazhagan, M. G., Aggarwal, V., Singh, A. K. & Choudhary, S. Federated learning with personalization layers. arXiv preprint arXiv:1912.00818 (2019). 

22. Hanzely, F. & Richtárik, P. Federated learning of a mixture of global and local models. arXiv preprint arXiv:2002.05516 (2020). 23. Ghosh, A., Chung, J., Yin, D. & Ramchandran, K. An efficient framework for clustered federated learning. _Adv. Neural. Inf. Process. Syst._ **33** , 19586–19597 (2020). 

24. Schneider, J., Meske, C. & Kuss, P. Foundation models: A new paradigm for artificial intelligence. _Bus. Inf. Syst. Eng._ **66** (2), 221–231 (2024). 

25. Guo, T., Guo, S., Wang, J., Tang, X. & Xu, W. Promptfl: Let federated participants cooperatively learn prompts instead of modelsfederated learning in age of foundation model. _IEEE Trans. Mobile Comput._ **23** (5), 5179–5194 (2023). 

26. Guo, T., Guo, S. & Wang, J. Pfedprompt: Learning personalized prompt for vision-language models in federated learning. in _Proceedings of the ACM Web Conference_ 1364–1374 (2023). 

27. Radford, A. _et al._ Learning transferable visual models from natural language supervision. in _International Conference on Machine Learning_ 8748–8763 (PMLR, 2021). 

28. Bommasani, R. _et al._ On the opportunities and risks of foundation models. arXiv preprint arXiv:2108.07258 (2021). 

29. Wang, H., Li, J., Wu, H., Hovy, E. & Sun, Y. Pre-trained language models and their applications. _Engineering_ **25** , 51–65 (2023). 

30. Vaswani, A. Attention is all you need. _Adv. Neural Inf. Process. Syst._ **30** , I (2017). 

31. Brown, T. et al. Language models are few-shot learners. _Adv. Neural. Inf. Process. Syst._ **33** , 1877–1901 (2020). 

32. Devlin, J. Bert: Pre-training of deep bidirectional transformers for language understanding. arXiv preprint arXiv:1810.04805 (2018). 

33. OpenAI. Gpt-4 technical report. arXiv preprint arXiv:2303.08774 (2023). 

34. Lei, Y., Li, J., Li, Z., Cao, Y. & Shan, H. Prompt learning in computer vision: A survey. _Front. Inf. Technol. Electron. Eng._ **25** , 42–63 (2024). 

35. Zhou, K., Yang, J., Loy, C. C. & Liu, Z. Learning to prompt for vision-language models. _Int. J. Comput. Vis._ **130** , 2337–2348 (2022). 

36. Zhou, K., Yang, J., Loy, C. C. & Liu, Z. Conditional prompt learning for vision-language models. in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ 16816–16825 (2022). 

37. Chen, G. _et al._ Plot: Prompt learning with optimal transport for vision-language models. arXiv preprint arXiv:2210.01253 (2022). 

38. Bahng, H., Jahanian, A., Sankaranarayanan, S. & Isola, P. Exploring visual prompts for adapting large-scale models. arXiv preprint arXiv:2203.17274 (2022). 

39. Chen, A., Yao, Y., Chen, P.-Y., Zhang, Y. & Liu, S. Understanding and improving visual prompting: A label-mapping perspective. in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ 19133–19143 (2023). 

40. Khattak, M. U., Rasheed, H., Maaz, M., Khan, S. & Khan, F. S. Maple: Multi-modal prompt learning. in _Proceedings of the IEEE/ CVF Conference on Computer Vision and Pattern Recognition_ 19113–19122 (2023). 

41. Dosovitskiy, A. An image is worth 16x16 words: Transformers for image recognition at scale. arXiv preprint arXiv:2010.11929 (2020). 

42. Zhang, M., Sapra, K., Fidler, S., Yeung, S. & Alvarez, J. M. Personalized federated learning with first order model optimization. arXiv preprint arXiv:2012.08565 (2020). 

43. Fei-Fei, L., Fergus, R. & Perona, P. Learning generative visual models from few training examples: An incremental Bayesian approach tested on 101 object categories. in _2004 Conference on Computer Vision and Pattern Recognition Workshop_ 178–178 (IEEE, 2004). 

44. Cimpoi, M., Maji, S., Kokkinos, I., Mohamed, S. & Vedaldi, A. Describing textures in the wild. In _Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition_ 3606–3613 (2014). 

45. Helber, P., Bischke, B., Dengel, A. & Borth, D. Eurosat: A novel dataset and deep learning benchmark for land use and land cover classification. _IEEE J. Select. Top.n Appl. Earth Observat. Remote Sens._ **12** , 2217–2226 (2019). 

46. Maji, S., Rahtu, E., Kannala, J., Blaschko, M. & Vedaldi, A. Fine-grained visual classification of aircraft. arXiv preprint arXiv:1306.5151 (2013). 

47. Bossard, L., Guillaumin, M. & Van Gool, L. Food-101–mining discriminative components with random forests. in _Computer Vision–ECCV 2014: 13th European Conference, Zurich, Switzerland, September 6–12, 2014, Proceedings, Part VI 13_ 446–461 (Springer, 2014). 

48. Nilsback, M.-E. & Zisserman, A. Automated flower classification over a large number of classes. in _2008 Sixth Indian Conference on Computer Vision, Graphics & Image Processing_ 722–729 (IEEE, 2008). 

49. Parkhi, O. M., Vedaldi, A., Zisserman, A. & Jawahar, C. Cats and dogs. in _2012 IEEE Conference on Computer Vision and Pattern Recognition_ 3498–3505 (IEEE, 2012). 

50. Soomro, K. Ucf101: A dataset of 101 human actions classes from videos in the wild. arXiv preprint arXiv:1212.0402 (2012). 51. Xu, J., Tong, X. & Huang, S.-L. Personalized federated learning with feature alignment and classifier collaboration. arXiv preprint arXiv:2306.11867 (2023). 

52. Shysheya, A., Bronskill, J., Patacchiola, M., Nowozin, S. & Turner, R. E. Fit: Parameter efficient few-shot transfer learning for personalized and federated image classification. arXiv preprint arXiv:2206.08671 (2022). 

53. Li, T. et al. Federated optimization in heterogeneous networks. _Proc. Mach. Learn. Syst._ **2** , 429–450 (2020). 

54. T Dinh, C., Tran, N. & Nguyen, J. Personalized federated learning with Moreau envelopes. _Adv. Neural Inf. Process. Syst._ **33** , 21394–21405 (2020). 

55. Zhao, H., Du, W., Li, F., Li, P. & Liu, G. Fedprompt: Communication-efficient and privacy-preserving prompt tuning in federated learning. in _ICASSP 2023-2023 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)_ 1–5 (IEEE, 2023). 

## **Author contributions** 

Y. C.: Conceptualization, Methodology, Software, Visualization, Writing-original draft. X.S.: Supervision, Conceptualization, Writing-review. X.Z.: Writing-review. Z.C.: Writing-review. D.M.: Supervision, Writing-review. 

**Scientific Reports** |        (2025) 15:28026 

15 

| https://doi.org/10.1038/s41598-025-11864-4 

www.nature.com/scientificreports/ 

## **Funding** 

This work was funded by the Science-Technology Development Plan Project of Jilin Province (20210202129NC). 

## **Declarations** 

## **Competing interests** 

The authors declare no competing interests. 

## **Additional information** 

**Correspondence** and requests for materials should be addressed to X.S. or D.M. 

**Reprints and permissions information** is available at www.nature.com/reprints. 

**Publisher’s note** Springer Nature remains neutral with regard to jurisdictional claims in published maps and institutional affiliations. 

**Open Access** This article is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License, which permits any non-commercial use, sharing, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons licence, and indicate if you modified the licensed material. You do not have permission under this licence to share adapted material derived from this article or parts of it. The images or other third party material in this article are included in the article’s Creative Commons licence, unless indicated otherwise in a credit line to the material. If material is not included in the article’s Creative Commons licence and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder. To view a copy of this licence, visit  h t t p : / / c r e a t i v e c o m m o n s . o r g / l i c e n s e s / b y - n c - n d / 4 . 0 / . 

© The Author(s) 2025 

**Scientific Reports** |        (2025) 15:28026 

16 

| https://doi.org/10.1038/s41598-025-11864-4 

