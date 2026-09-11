Published as a conference paper at ICLR 2025 

# MIXTURE OF EXPERTS MADE PERSONALIZED: - FEDERATED PROMPT LEARNING FOR VISION LANGUAGE MODELS 

### **Jun Luo** 

Intelligent Systems Program University of Pittsburgh Pittsburgh, PA 15213, USA jul117@pitt.edu 

### **Chen Chen** 

Center for Research in Computer Vision University of Central Florida Orlando, FL 32816, USA chen.chen@crcv.ucf.edu 

### **Shandong Wu** 

Intelligent Systems Program Department of Radiology Department of Biomedical Informatics Department of Bioengineering University of Pittsburgh Pittsburgh, PA 15213, USA wus3@upmc.edu 

## ABSTRACT 

Federated prompt learning benefits federated learning with CLIP-like VisionLanguage Model’s (VLM’s) robust representation learning ability through prompt learning. However, current federated prompt learning methods are habitually restricted to the traditional FL paradigm, where the participating clients are generally only allowed to download a single globally aggregated model from the server. While justifiable for training full-sized models under federated settings, in this work, we argue that this paradigm is ill-suited for lightweight prompts. By facilitating the clients to download multiple pre-aggregated prompts as fixed nonlocal experts, we propose **P** ersonalized **Fed** erated **M** ixture of **A** daptive **P** rompts ( **pFedMoAP** ), a novel FL framework that personalizes the prompt learning process through the lens of Mixture of Experts (MoE). pFedMoAP implements a local attention-based gating network that learns to generate enhanced text features for better alignment with local image data, benefiting from both local and downloaded non-local adaptive prompt experts. Extensive experiments on 9 datasets under various federated settings demonstrate the efficacy of the proposed pFedMoAP algorithm. The code is available at https://github. com/ljaiverson/pFedMoAP. 

## 1 INTRODUCTION 

Recent years have witnessed the prosperity of federated learning (FL) (McMahan et al., 2017; Kairouz et al., 2019; Li et al., 2020a) as a potent paradigm for training machine learning models across decentralized data sources. While offering a privacy-preserving solution in collaborative training settings, this approach faces a critical challenge in the form of heterogeneous data distribution across the participating clients (Li et al., 2020a). And due to the data heterogeneity, the generalization capabilities of the trained models may be compromised (Li et al., 2020b; Sahu et al., 2018). In this context, the pre-trained Vision-Language Models (VLMs) such as CLIP (Radford et al., 2021) and ALIGN (Jia et al., 2021) can provide a significant impact with their remarkable applications in learning transferable representations across a wide range of tasks and disparate data distributions encountered in federated settings. 

1 

Published as a conference paper at ICLR 2025 


![](P025_images/P025.pdf-0002-01.png)



![](P025_images/P025.pdf-0002-02.png)


Figure 1: Schematic diagram of employing Mixture of Experts into federated learning. We facilitate the sharing of pre-aggregated prompts thanks to their lightweight nature. Each client downloads the pre-aggregated prompts trained on the remaining two clients through the server, keeping them fixed locally as non-local experts. 

However, applying VLMs in FL contexts is not without challenges. Due to their millions of parameters, fine-tuning these large-scale models in federated settings incurs prohibitively high communication overhead, making it impractical for many real-world applications. This limitation has led researchers to explore more efficient adaptation techniques for VLMs, with prompt learning emerging as a promising approach to overcome the communication bottleneck. 

Prompt learning for VLMs (Zhou et al., 2022b), originally proposed to eliminate the need for handcrafted prompts, replaces the context words with small-scale learnable vectors while keeping the pre-trained model fixed. Such a lightweight approach particularly benefits FL by tremendously reducing the communication overhead associated with transmitting the entire fine-tuned model. For instance, PromptFL (Guo et al., 2023b) leverages a FedAvg (McMahan et al., 2017) style aggregation of the locally trained prompts. FedPR (Feng et al., 2023) learns the visual prompt within the null space of the global prompt. In addition, recent criticism on prompt-based VLMs to unseen data distributions (Zhou et al., 2022b; Khattak et al., 2023a;b) also facilitates FL researchers to combine prompt learning with personalized FL (PFL). Instead of restricting to the global consensus model, PFL (Tan et al., 2022; Kulkarni et al., 2020) allows tailored models for each individual client, systemically mitigating the data heterogeneity issues and enhancing the overall flexibility of the system. However, directly applying PFL techniques, such as local fine-tuning (Cheng et al., 2021) and personalizing specific layers (Arivazhagan et al., 2019), to prompt learning has demonstrated limited efficacy in training the prompt (Guo et al., 2023b) under extreme data heterogeneity. Consequently, some works tailor PFL techniques to prompt learning in CLIP-like VLMs. In this recently emerged field, Guo et al. (2023a) trains a global consensus prompt with personalized visual attention modules on locally memorized data. Li et al. (2024) leverages unbalanced Optimal Transport to align visual feature maps with personalized prompts. More details on prior works are presented in Appendix A. 

Unfortunately, existing federated prompt learning approaches **habitually adhere to the paradigm of traditional FL/PFL techniques** , wherein the participating clients are generally only allowed to download a single globally aggregated model from the server. While justifiable for full-sized models, we argue that this paradigm is ill-suited for federated prompt learning, as the significantly reduced size of prompts substantially mitigates the potential communication overhead. To contextualize this disparity, consider that while a typical ResNet50 model contains approximately 25.6 million parameters, a learnable prompt with length 16 and dimension 512 comprises merely 16 _×_ 512 = 8 _,_ 192 parameters — a reduction of three orders of magnitude. Given this significant parameter reduction, restricting clients to downloading only a single globally aggregated model — as in traditional FL/PFL — unnecessarily limits federated prompt learning. **The lightweight nature of prompts provides a unique way for more flexible and effective personalization strategies.** Therefore, this motivates us to address the following pivotal question: 

_How can we devise a personalized federated learning framework, tailored for prompt learning in CLIP-like VLMs, while fully exploiting the lightweight nature of the prompts?_ 

In light of these challenges and opportunities, we propose a novel framework: **P** ersonalized **Fed** erated **M** ixture **o** f **A** daptive **P** rompts ( **pFedMoAP** ). Tailored specifically for prompt learning in CLIP-like VLMs, our proposed framework aims to unleash the potential of the lightweight prompt 

2 

Published as a conference paper at ICLR 2025 

by allowing the clients to download **multiple pre-aggregated prompts** (see Fig. 1b) to acquire collective knowledge. In this manner, we enhance the generalization capabilities of the PFL system under extreme data heterogeneity, offering a more flexible and effective solution that fully leverages the lightweight nature of prompts in federated settings. 

At its core, pFedMoAP personalizes the federated prompt learning problem through the lens of Mixture of Experts (MoE), treating all locally updated prompts as specialized experts. Benefiting from lifting the aforementioned ill-suited restriction, pFedMoAP facilitates the sharing of pre-aggregated prompts between clients (through the server). In addition, our proposed framework implements a novel client-specific, parameter-efficient, attention-based gating network that learns to generate enhanced text features for better alignment with local image data on each client. Through this locally trained gating network, the enhanced text features are generated from the adaptive local and nonlocal prompt experts via CLIP’s text encoder. The local expert is trained exclusively with the client’s data, while non-local experts, trained on other clients, are sparsely selected from a server-maintained pool based on _K_ nearest neighbors (KNN), and shared with the client without aggregation, fostering collective knowledge sharing across clients beyond the global aggregation. 

We summarize our main contributions as follows: 

- We pioneer a paradigm shift in federated prompt learning for VLMs by challenging the restriction on sharing pre-aggregated prompts between clients. Circumventing this ill-suited restriction for prompt learning unlocks more potential inherent in the lightweight prompts, facilitating more effective cross-client knowledge sharing. As such, we pave the way for more flexible federated prompt learning in VLMs. 

- We propose pFedMoAP, a novel framework designed specifically for personalizing federated prompt learning in CLIP-like VLMs under data heterogeneity for image recognition tasks. pFedMoAP personalizes the prompt learning with a unique attention-based gating network. Thanks to its flexibility, this gating network has the potential to extend beyond federated learning for prompt-based VLMs. 

- We validate the effectiveness of the proposed pFedMoAP through extensive experiments and ablation studies across 9 widely adopted datasets under various federated settings. The results verify the superiority of pFedMoAP over compared state-of-the-art methods. 

## 2 PRELIMINARIES 

### 2.1 PERSONALIZED FEDERATED LEARNING 

Conventional federated learning (FL) aims to train a global consensus model for a federation of clients with similar data. As the most notable FL algorithm, FedAvg (McMahan et al., 2017) minimizes the global objective over _N_ clients defined as: 


![](P025_images/P025.pdf-0003-10.png)


where **_θ_** and _Fi_ ( _·_ ) represents the global model and the local objective of client _i_ , respectively, and the weight _pi_ is often set as _pi_ = _ni/n_ with _n_ =<sup>�</sup> _i_<sup>_ni_where</sup><sup>_ni_denotesthenumberof</sup> data samples on client _i_ . In FedAvg, the local objective _Fi_ ( _·_ ) measures client _i_ ’s empirical loss, � _nk_ =1 _i_<sup>_Li_(</sup><sup>**_θ_**</sup><sup>_|_(</sup><sup>**_x_**</sup><sup>_k, yk_)), where</sup><sup>_Li_represents its loss and</sup><sup>**_x_**</sup><sup>_k_is its</sup><sup>_k_-th data sample with ground truth</sup> label _yk_ . 

Compared to conventional FL, personalized FL (PFL) relaxes the number of models where each client _i_ is allowed to have its tailored model **_θ_** _i_ . The goal of PFL is, therefore, defined as: 


![](P025_images/P025.pdf-0003-13.png)

### Figure analysis

Purpose: The displayed equations define the optimization objectives used in the paper’s preliminaries for conventional federated learning and personalized federated learning.

Components observed:

- Equation (1), FedAvg/global FL objective:
  \[
  \min_{\theta} F(\theta) = \sum_{i=1}^{N} p_i F_i(\theta).
  \]
  - \(\theta\): shared global model parameters.
  - \(N\): number of clients.
  - \(F_i(\theta)\): local objective for client \(i\).
  - \(p_i\): client weight, described in the nearby text as often proportional to the number of samples on client \(i\).

- Equation (2), personalized FL objective:
  \[
  \min_{\theta_1,\ldots,\theta_N} F(\theta_1,\ldots,\theta_N)
  = \min_{\theta_1,\ldots,\theta_N} \sum_{i=1}^{N} p_i F_i(\theta_i).
  \]
  - \(\theta_i\): client-specific model parameters for client \(i\).
  - The summation structure is similar to FedAvg, but each local objective is evaluated using its own personalized parameter vector rather than a single global \(\theta\).

Direct observations:

- Both equations aggregate client objectives with weights \(p_i\).
- The first equation optimizes one shared parameter set \(\theta\) across all clients.
- The second equation optimizes separate parameters \(\theta_1, \ldots, \theta_N\), one per client.

Interpretation:

- The equations visually establish the conceptual transition from conventional federated learning to personalized federated learning.
- This distinction supports the surrounding discussion motivating pFedMoAP: the proposed method is positioned as a personalized federated prompt-learning framework for heterogeneous client data.
- The equations provide mathematical background rather than experimental results; no axes, legends, plotted series, or numerical comparisons are present.


### 2.2 PROMPT LEARNING FOR CLIP-LIKE VLMS 

To efficiently adapt pre-trained CLIP-like VLMs to downstream tasks, prompt learning methods (Zhou et al., 2022b;a) model a prompt’s context words with learnable vectors. While zero-shot 

3 

Published as a conference paper at ICLR 2025 

transfer of CLIP leverages the fixed word embedding **_W_** = _{_ **_w_** 1 _, ...,_ **_w_** _l}_ from hand-crafted prompt templates with _l_ context words (e.g. “a photo of a _<_ class _>_ .”), prompt learning replace it with the learnable prompt **_P_** = _{_ **_p_** 1 _, ...,_ **_p_** _l} ∈_ R<sup>_l×d_</sup> where _d_ is the dimension of the word embedding. The full prompt **_P_**<sup>(</sup><sup>_c_)</sup> , consisting of the learnable prompt **_P_** with the embedding of a class label _c_ , is then fed into the fixed text encoder, _g_ ( _·_ ). Together with the fixed image encoder _f_ ( _·_ ), the classification logit for class _c_ is then computed as a matching score between the image and text features. And the prediction probability of each class for image **_x_** is derived by taking a Softmax, controlled by temperature _τ_ , over the logits: 


![](P025_images/P025.pdf-0004-02.png)



![](P025_images/P025.pdf-0004-03.png)


ˆ where sim( _·_ ) denotes a metric function (e.g. cosine similarity), _y_ is the predicted label, and _C_ denotes the number of classes. With the probabilities, we can learn the prompt **_P_** by minimizing the cross-entropy loss. 

### 2.3 MIXTURE OF EXPERTS 

With a similar form to FL’s, Mixture of Experts (MoE) aggregates the _output_ of multiple experts or trained models, instead of the model parameters. For a general MoE system with _N_ experts, the output of MoE with input _x_ is defined as: 


![](P025_images/P025.pdf-0004-07.png)

### Figure analysis

The extracted fragments correspond to separate displayed equations, not a chart or data figure. Their purpose is to formalize two background mechanisms used later in the paper: prompt learning for CLIP-like vision-language models and Mixture of Experts (MoE).

- **Equation (3): CLIP-style class logit**
  \[
  \mathrm{logit}^{(c)} = \mathrm{sim}\left(f(\mathbf{x}), g(\mathbf{P}^{(c)})\right),
  \]
  Directly observed components:
  - \(\mathbf{x}\): input image.
  - \(f(\cdot)\): image encoder.
  - \(g(\cdot)\): text encoder.
  - \(\mathbf{P}^{(c)}\): prompt representation associated with class \(c\).
  - \(\mathrm{sim}(\cdot)\): similarity function between image and text features.

- **Equation (4): softmax class probability**
  \[
  p(\hat{y}=c \mid \mathbf{x}) = \frac{\exp(\mathrm{logit}^{(c)}/\tau)}{\sum_{k=1}^{C}\exp(\mathrm{logit}^{(k)}/\tau)},
  \]
  Directly observed components:
  - \(\hat{y}\): predicted label.
  - \(C\): number of classes.
  - \(\tau\): temperature parameter controlling the softmax scale.
  - The numerator uses the class-\(c\) logit, while the denominator normalizes across all \(C\) classes.

- **Equation (5): generic Mixture-of-Experts aggregation**
  \[
  MoE(\mathbf{x}) = \sum_{i=1}^{N} G(\mathbf{x})_i \cdot E_i(\mathbf{x}),
  \]
  Directly observed components:
  - \(N\): number of experts.
  - \(E_i(\cdot)\): output of expert \(i\).
  - \(G(\mathbf{x})_i\): input-dependent gating weight assigned to expert \(i\).
  - The output is a weighted sum of expert outputs rather than an aggregation of model parameters.

**Visual observations:** The fragments contain mathematical notation only; there are no axes, legends, plotted series, image panels, or numerical results to extract. Equations (3) and (4) belong to the prompt-learning background section, while Equation (5) belongs to the Mixture-of-Experts background section.

**Interpretation in context:** Together, these equations connect the paper’s proposed personalized federated prompt-learning method to two foundations: CLIP-like classification via learned prompts and MoE-style input-dependent combination of multiple expert outputs. This supports the nearby motivation that adaptive prompts can be shared and combined in a personalized federated setting using a gating mechanism.


where _Ei_ ( _·_ ) represents the _i_ -th expert, and _G_ ( _·_ ) _i_ represents the weight assigned to the output of expert _i_ from a _N_ dimensional vector, based on its input. The mechanism for weight assignment is often controlled by a network called **gating network** (also known as a router). The implementation of the gating network varies (Clark et al., 2022; Hazimeh et al., 2021; Zhou et al., 2022c), but a simple yet effective one is implemented by taking the Softmax over top- _K_ ( _K ≤ N_ ) logits of a linear layer with the remaining _N − K_ weights set to zero (Shazeer et al., 2017). We propose a novel lightweight attention-based gating network devised for CLIP-like VLMs that extends beyond federated learning. Details are presented in Sec. 3.3. 

## 3 PERSONALIZED FEDERATED MIXTURE OF ADAPTIVE PROMPTS 

**Motivation.** While federated prompt learning for pre-trained CLIP-like VLMs offers an approach to efficiently adapt these models to downstream tasks under federated settings, such methods mostly lack personalization for the prompt to generalize with extreme data heterogeneity. Prior PFL methods devised for prompt learning habitually adhere to the restriction for the clients to download only a single globally aggregated model from the server, failing to leverage the lightweight nature of the prompt to the fullest. In addition, from an MoE perspective, allowing clients to download preaggregated prompts trained on other clients naturally provides a systemic solution to the dilemma where too many experts on the client incurs prohibitively high communication overhead while too few experts impairs the benefit of employing MoE. Consequently, there is a need for a tailored PFL approach for prompt learning in CLIP-like VLMs that offers the flexibility to share trained prompts from an MoE perspective. 

**Overview.** The rest of this section presents the details of the pFedMoAP by gradually building upon PFL with prompt learning and mixture of adaptive prompts, and how the proposed attention-based gating network works in pFedMoAP, as well as potentials in extending it beyond federated learning. 

### 3.1 PERSONALIZED FEDERATED PROMPT LEARNING WITH LOCAL PROMPT ONLY 

In our study, we presume each client hosts a CLIP model with fixed image encoder _f_ ( _·_ ) and text encoder _g_ ( _·_ ) for image recognition tasks. We first suppose, in this subsection, that each client 

4 

Published as a conference paper at ICLR 2025 


![](P025_images/P025.pdf-0005-01.png)


Figure 2: Workflow of pFedMoAP at client _i_ . The client first computes the non-local text features using the non-local prompt experts. As training progresses, it then calculates the local text features. Taking class 3 as an example, both local and non-local text features are input into the attentionbased gating network as both key and value, while image features serve as the query. This process generates enhanced text features. Matching socres are derived from two sources: local text features and MoE-enhanced text features. These scores are then combined through weighted averaging to produce the final logits. 

personalizes the local prompt without the MoE. At federated round _t_ , each client _i_ in the selected set of participating client _St_ locally updates its prompt, **_P_** _i_<sup>_t_, initialized with the global prompt from the</sup> last round, **_P_** _g_<sup>_t−_1</sup> . The prompt is then updated through a gradient-based optimization, e.g. Stochastic Gradient Descent (SGD), over a cross-entropy loss for multiple local epochs. 

After finishing the local update, the learned prompts **_P_** _i_ for all the clients in _St_ are then aggregated by the server for a global prompt **_P_** _g_<sup>_t_in a FedAvg manner:</sup> 


![](P025_images/P025.pdf-0005-05.png)


While **_P_** _g_<sup>_t_isusedforthenextroundoftraining,forclient</sup><sup>_i_,</sup><sup>**_P_**</sup><sup>_t_</sup> _i_<sup>isstoredandusedforinference</sup> purposes, achieving a simple personalization for federated prompt learning while MoE is not present. 

### 3.2 PERSONALIZED FEDERATED MIXTURE OF ADAPTIVE PROMPTS WORKFLOW 

Thanks to the lightweight nature of the prompt, clients are enabled to acquire collective knowledge beyond the globally aggregated prompt. In pFedMoAP, we facilitate, rather than discourage, each client to download _K_ pre-aggregated prompts trained on other clients as non-local client experts. These non-local experts are sparsely selected from a server-maintained pool of prompt experts, _P_ . The pool functions as a dynamic repository, refreshing at the conclusion of each federated round. It incorporates the newly acquired prompts from the clients who participated in the current training round, and overwrites their previous entries (if existing) in the pool, i.e: 


![](P025_images/P025.pdf-0005-09.png)


At the beginning of the current round _t_ , each client _i ∈St_ is first assigned _K_ non-local experts from the previous round’s pool, _Pt−_ 1. This assignment is based on a _K_ nearest neighbors (KNN) algorithm, which identifies the top- _K_ nearest experts from client _i_ ’s entry in the pool, in terms of _l_ 2 distance<sup>1</sup> . the rationale behind the KNN-based expert assignment is that clients with similar locally 

> 1The first-time participants with no entry in the pool conduct a standard local training of the global prompt, and upload its trained prompt to the pool. 

5 

Published as a conference paper at ICLR 2025 

trained prompts are more likely to share comparable data distributions. This similarity-based expert assignment aims to leverage knowledge from clients with potentially similar data characteristics, enhancing the personalization from closer collaborators in terms of local data distributions. 

While such a server-side assignment of the non-local experts inherently simulates the _sparse_ gating in MoE, a client-side gating network, _Gi_ ( _·_ ), enables dynamic _dense_ incorporation of the output from all selected experts on a per-image basis (see Fig. 2). 

Let _Qi_ = _{NLj}_<sup>_K_</sup> _j_ =1<sup>(</sup><sup>_NL_represents “</sup><sup>_N_on-</sup><sup>_L_ocal”) be the set of clients assigned to client</sup><sup>_i_, whose</sup> prompts, **_P_** _NLj_ , are served as non-local experts on client _i_ . Before the local training of client _i_ initiates, text features for every non-local prompt are computed via the CLIP’s fixed text encoder, _g_ ( _·_ ). Note that since the non-local prompt experts are kept fixed throughout the local training, these text features are only necessary to be computed once. Let **_T_** _NL_<sup>(</sup><sup>_c_)</sup> _j_<sup>bethetextfeaturesforclass</sup><sup>_c_</sup> generated by the _j_ -th non-local prompt expert on client _i_ with class _c_ ’s embedding, **_P_** _NL_<sup>(</sup><sup>_c_)</sup> _j_<sup>.At the</sup> beginning of the local training on client _i_ , the text features, **_T_** _NL_<sup>(</sup><sup>_c_),fromeverynon-localexpertfor</sup> every class _c ∈_ [ _C_ ], formulated below, are fixed and ready to use for the entire local training process: 


![](P025_images/P025.pdf-0006-04.png)


In pFedMoAP, a novel attention-based gating network, _G_ ( _·|_ **_θ_** _i_ ) parameterized by **_θ_** _i_ , is proposed. Unlike the _G_ ( _·_ ) in Eq. (5), the proposed gating network functions to generate a **mixture of the outputs from the experts** , instead of the weights for the outputs in traditional MoE. The weights, however, are still internally computed as intermediate products through the attention mechanism. We discuss the gating network in details in Sec. 3.3. Let **_I_** _k_ = _f_ ( **_x_** _k_ ) be the computed image feature of the input image **_x_** _k_ through CLIP’s fixed image encoder _f_ ( _·_ ). In pFedMoAP, for each class _c ∈_ [ _C_ ], what the gating network, _G_ ( _·|_ **_θ_** _i_ ), takes as input are three-fold: **1)** image feature, **_I_** _k_ ; **2)** text features from the locally updated prompt expert **_T_** _L_<sup>(</sup><sup>_c_)</sup> = _g_ ( **_P_** _i_<sup>(</sup><sup>_c_)</sup> ) where _L_ represents “ _L_ ocal”; and **3)** text features from the all non-local experts, **_T_** _NL_<sup>(</sup><sup>_c_)defined in Eq. (8). The gating network then outputs</sup> the enhanced text feature, **_T_** _MoE_<sup>(</sup><sup>_c_), better aligned with the image feature</sup><sup>**_I_**</sup><sup>_k_for more generalizability</sup> that incorporates both collective knowledge and personalization, i.e., 


![](P025_images/P025.pdf-0006-06.png)


Note that although the gating network could technically be parameterized in a class-specific manner, our implementation opts to use a shared set of parameters across all classes for parameter efficiency. 

As the final step, pFedMoAP computes the logits based on the matching score between the image feature **_I_** _k_ and text features from two sources, namely **_T_** _MoE_<sup>(</sup><sup>_c_)fromtheMoE,and</sup><sup>**_T_**</sup> _L_<sup>(</sup><sup>_c_)</sup> from the local expert. Although **_T_** _MoE_<sup>(</sup><sup>_c_)carries the global collective knowledge, we further address</sup><sup>**_T_**</sup> _L_<sup>(</sup><sup>_c_)</sup> with weight _λ_ as the local prompt **_P_** _i_ is the only learnable expert on the client, i.e., 

_∀c ∈_ [ _C_ ] _,_ logit<sup>(</sup><sup>_c_)</sup> = sim( **_I_** _k,_ **_T_** _MoE_<sup>(</sup><sup>_c_)) +</sup><sup>_λ ·_sim(</sup><sup>**_I_**</sup><sup>_k,_</sup><sup>**_T_**</sup> _L_<sup>(</sup><sup>_c_))</sup><sup>_._</sup> (10) With the classification logits, the local prompt **_P_** _i_ and the parameter **_θ_** _i_ in the gating network are updated through optimizing over the cross-entropy loss based on the prediction probability computed as in Eq. (4). After the local training, client _i_ upload **_P_** _i_ to the server while maintaining the gating network locally. 

### 3.3 ATTENTION-BASED GATING NETWORK: IN PFE DMOAP AND BEYOND 

To generate enhanced text features that better aligns with the image feature **_I_** _k_ , the proposed gating network employs a multi-head attention (MHA) layer (Vaswani, 2017) with the query being the **_I_** _k_ , while the key and the value are both text features **_T_** _L_<sup>(</sup><sup>_c_)</sup><sup>_,_</sup><sup>**_T_**</sup> _NL_<sup>(</sup><sup>_c_)</sup> 1<sup>_,_</sup><sup>**_T_**</sup> _NL_<sup>(</sup><sup>_c_)</sup> 2<sup>_, ...,_</sup><sup>**_T_**</sup> _NL_<sup>(</sup><sup>_c_)</sup> _K_<sup>.However, since the</sup> dimension of these features are usually large, resulting in too many parameters in the MHA layer (e.g. for CLIP with a ResNet50 backbone, _d_ feature = 1024, MHA layer will have 4.2M parameters), we force each feature to first go through a pooling layer to reduce the dimension to a fixed _d_ gating = 128 (MHA layer will only have 66.0K parameters). Therefore, with _Q_ = Pooling( **_I_** _k_ ) _, K_ = _V_ = Pooling( **_T_** _L_<sup>(</sup><sup>_c_)</sup><sup>_,_</sup><sup>**_T_**</sup> _NL_<sup>(</sup><sup>_c_)) and</sup><sup>_h_being then number of heads, we have:</sup> 


![](P025_images/P025.pdf-0006-12.png)


6 

Published as a conference paper at ICLR 2025 

Table 1: Few-shot performance on CLIP datasets under pathological non-IID setting. 

||Flowers102|OxfordPets|Food101|Caltech101|DTD|
|---|---|---|---|---|---|
|ZS-CLIP(Radford et al., 2021)|62.17_±_0.12|84.47_±_0.01|75.27_±_0.05|85.14_±_0.24|40.21_±_0.12|
|CoOp(Zhou et al., 2022b)|70.14_±_0.76|83.21_±_1.30|70.43_±_2.42|87.37_±_0.44|44.23_±_0.63|
|PromptFL(Guo et al., 2023b)|72.80_±_1.14|90.79_±_0.61|77.31_±_1.64|89.70_±_1.99|54.11_±_0.22|
|PromptFL+FT(Cheng et al., 2021)|72.31_±_0.91|91.23_±_0.50|77.16_±_1.56|89.70_±_0.25|53.74_±_1.36|
|Prompt+FedPer(Arivazhagan et al., 2019)|72.11_±_1.35|89.50_±_1.62|71.29_±_1.87|86.72_±_1.45|50.23_±_0.82|
|Prompt+FedProx(Li et al., 2020b)|66.40_±_0.29|89.24_±_0.41|76.24_±_1.94|89.41_±_0.55|44.26_±_1.11|
|Prompt+FedAMP(Huang et al., 2021)|69.10_±_0.13|80.21_±_0.44|74.48_±_1.71|87.31_±_1.60|47.16_±_0.92|
|pFedPrompt(Guo et al., 2023a)|86.46_±_0.15|91.84_±_0.41|92.26_±_1.34|96.54_±_1.31|77.14_±_0.09|
|FedOTP(Li et al., 2024)|96.23_±_0.44|98.82_±_0.11|92.73_±_0.15|97.02_±_0.36|87.64_±_0.70|
|pFedMoAP(_λ_=0.0)|97.61_±_0.11|94.83_±_0.65|86.71_±_0.15|95.71_±_0.37|85.64_±_0.34|
|pFedMoAP(_λ_=0.5)|98.41_±_0.04|99.06_±_0.09|93.39_±_0.09|97.95_±_0.07|89.13_±_0.54|



where head _q_ = Attention( _QWq_<sup>_Q, KW K_</sup> _q_<sup>_, V W V_</sup> _q_<sup>) and</sup><sup>_W O, W_</sup> _q_<sup>_Q, W_</sup> _q_<sup>_K, W_</sup> _q_<sup>_V_are standard MHA pa-</sup> rameters in **_θ_** _i_ . As **_T_** _MoE_<sup>(</sup><sup>_c_)</sup><sup>_∈_R</sup><sup>_d_gating, computing sim(</sup><sup>**_I_**</sup><sup>_k,_</sup><sup>**_T_**</sup> _MoE_<sup>(</sup><sup>_c_)) requires pooling on</sup><sup>**_I_**</sup><sup>_k_as well.</sup> 

While a linear projection-based gating network, _G_ proj( _·_ ), in a typical MoE is also able to achieve enhanced text features for CLIP (e.g. by assigning weights _G_ proj( **_x_** _k_ ) _∈_ R<sup>_K_+1</sup> for the experts’ output based on the image input (Shazeer et al., 2017)), the proposed attention-based gating network is more favorable for the following FL-agnostic reasons. **1)** Since the experts are constantly adapting during the training process, directly learning the assigned weights for the experts, as in projection-based gating, will be less robust than learning the relationship between the image feature and the text features generated by the experts, as in attention-based gating. **2)** The output of the proposed attention-based gating is the enhanced text features, which makes the MHA layer serve as a lightweight linear probing with a much larger search space, that functions beyond assigning _K_ + 1 weights to aggregate the experts’ output as a linear combination in a _K_ + 1-dimensional search space. Even with a redesigned projection layer to directly produce the enhanced text features, the parameter count of such a projection-based gating network would substantially exceed that of the attention-based gating network. **3)** A projection-based gating network fails to leverage the pre-trained CLIP’s powerful capability to align text features with image features, while the attention mechanism naturally harnesses it through the scaled dot-product operation. **4)** Even if we feed both image and text features from multiple experts into a projection-based gating network, the order of these input would affect the final output in an uncontrollable way. And the number of experts has to be fixed for a projection-based gating network. In contrast, the proposed attention-based gating network is order-agnostic with a flexible number of experts it engages with. In pFedMoAP, while we fix the number of non-local experts on each client to be _K_ , in practice, _K_ can be client-specific based on the client’s memory and communication bandwidth. 

As such, our design of the attention-based gating network extends beyond federated learning. This versatile network could be adapted to general prompt learning for VLMs where multiple prompts are trained, such as multi-task learning or domain adaptation. We anticipate that our work will inspire future research exploring the broader applications of mixture of adaptive prompts for VLMs. The detailed pFedMoAP algorithm can be found in Algorithm 1. 

## 4 EXPERIMENTS 

### 4.1 EXPERIMENTAL SETUP 

**Dataset and data heterogeneity.** We evaluate the efficacy of the proposed pFedMoAP with 9 public benchmark datasets under various federated settings to simulate different types of data heterogeneity. Following previous research (Guo et al., 2023b), to evaluate pFedMoAP under label heterogeneity, we adopt 5 representative visual classification datasets used to evaluate CLIP (Radford et al., 2021), namely OxfordPets Parkhi et al. (2012), Flowers102 Nilsback & Zisserman (2008), DTD Cimpoi et al. (2014), Caltech101 Fei-Fei (2004), Food101 Bossard et al. (2014). We refer to these datasets collectively as CLIP datasets. On these datasets, we test pFedMoAP’s few-shot performance under label heterogeneity by employing a pathological non-IID setting, where the classes are evenly distributed to the clients with no overlapping classes between any two clients. In addi- 

7 

Published as a conference paper at ICLR 2025 

tion, we use CIFAR10 and CIFAR100 dataset (Gong et al., 2012) and a Dirichlet distribution with Dir( _α_ = 0 _._ 5) to simulate the label shift (Hsu et al., 2019). The Dirichlet distribution with _α_ = 0 represents an extreme case where each client has only one class and larger _α_ simulates a stratified and even split of labels. Dir( _α_ = 0 _._ 5) is on the more heterogeneous side. For feature heterogeneity, we adopt DomainNet dataset (Peng et al., 2019) and Office-Caltech10 dataset (Gong et al., 2012), with 6 and 4 inherent domains, respectively. To add on extra heterogeneity, for DomainNet and Office-Caltech10, we split each domain with Dir( _α_ = 0 _._ 3) for extra label heterogeneity, mimicking real-world FL settings with both label and feature shifts. 

**Compared baselines.** We compare our approach with three categories of baselines. The first category is local methods, where the clients do not participate in a FL setting. This category includes zero-shot CLIP (ZS-CLIP) (Radford et al., 2021) employing prompt templates: “a photo of a _<_ class _>_ ”, and CoOp (Zhou et al., 2022b) with learnable prompt vectors trained locally on each client. The second category comprises existing federated prompt learning methods, which include PromptFL (Guo et al., 2023b), which learns a unified prompt across clients, pFedPrompt (Guo et al., 2023a), which learns a shared prompt with personalized visual attention modules on locally memorized data, and FedOTP (Li et al., 2024), which leverages unbalanced Optimal Transport to align visual feature maps with personalized prompts. The third category consists of adapted methods from traditional FL/PFL techniques on PromptFL, namely FT (Cheng et al., 2021), FedProx Li et al. (2020b), FedPer (Arivazhagan et al., 2019), and FedAMP (Huang et al., 2021). 

|**Implementation details.**<br>**1)**||||
|---|---|---|---|
|CLIP datasets. Each dataset in<br>CLIP datasets is partitioned into<br>_N_ = 10clients, each with a dis-|Table 2: Results on CIFAR10 a<br>with (Dir(_α_= 0_._5)) partition into|nd CIFAR10<br>100 clients|0 with labe|
|joint set of classes evenly and<br>randoml assined to the clients||CIFAR10|CIFAR10|
|y g   .<br>The training proceeds for _T_ =<br>10 rounds with _r_ = 100% par-<br>ticipation rate. The CLIP uses<br>a ResNet50 backbone.<br>**2)** CI-<br>FAR10 & CIFAR100.<br>_N_<br>=|ZS CLIP(Radford et al., 2021)<br>CoOp(Zhou et al., 2022b)<br>PromptFL(Guo et al., 2023b)<br>Prompt+FedProx(Li et al., 2020b)<br>pFedMoAP|53.46_±_0.21<br>80.84_±_0.39<br>73.29_±_0.37<br>73.32_±_0.34<br>83.46_±_0.53|32.68_±_0.00<br>48.74_±_0.17<br>45.00_±_0.62<br>45.63_±_0.75<br>53.42_±_0.22|
|100clients results from Dir(_α_=||||



Table 2: Results on CIFAR10 and CIFAR100 with label shift with (Dir( _α_ = 0 _._ 5)) partition into 100 clients 

0 _._ 5) partition with _T_ = 120 rounds with _r_ = 10%. CLIP also uses a ResNet50 backbone. **3)** DomainNet & Office-Caltech10. Each domain of these two datasets is partitioned to 5 clients with Dir( _α_ = 0 _._ 3), resulting in _N_ = 30 for DomainNet and _N_ = 20 for Office-Caltech10. _T_ = 25 for both datasets, while _r_ = 25% for DomainNet and _r_ = 50% for Office-Caltech10. The CLIP uses a ViT-b-16 backbone. **4)** Training specs. For all methods, we use SGD as the optimizer with a learning rate of 0.002 and 5 local epochs (except CoOp is locally trained for 25 epochs without FL). For pFedMoAP, we use SGD with a learning rate of 0.01 to train the _h_ = 8-head gating network and default _λ_ = 0 _._ 5 in Eq. (10). A summary of the dataset setup can be found at Appendix C.1. 

### 4.2 PERFORMANCE EVALUATION 

We compute as the metric the average accuracy over every client’s private test set, drawn from the same distribution as its training set, and report the mean and standard deviation of all methods over three runs with different seeds. 

**Evaluation on Label Shifts.** To assess the performance of our method in handling label shifts, we conducted experiments on the CLIP datasets for few-shot training and CIFAR datasets for standard training. Tab. 1 shows the results on the CLIP datasets under a pathological non-IID setting, while Tab. 2 presents the results on CIFAR10 and CIFAR100 with Dir( _α_ = 0 _._ 5). On the CLIP datasets (Tab. 1), our proposed method pFedMoAP consistently outperforms other baselines across all five datasets, with significant margins over most methods, which proves the superiority of pFedMoAP. For instance, on the Flowers102 dataset, pFedMoAP achieves an accuracy of 98.41% with _λ_ = 0 _._ 5, respectively 2.18% and 11.95% higher than FedOTP and pFedPrompt, the top 2 performant federated prompt learning methods, both recently proposed to achieve personalization through intermediate visual feature maps. Similar improvements can be observed across other datasets. Notably, on DTD dataset where zero-shot struggles to excel, pFedMoAP has little performance drop compared to personalized methods such as pFedPrompt and PromptFL+FedPer, showing pFedMoAP’s 

8 

Published as a conference paper at ICLR 2025 

Table 3: Results on DomainNet with feature shift and label shift with Dir( _α_ = 0 _._ 3) partition into 5 clients/domain 

||Clipart|Infograph|Painting|Quickdraw|Real|Sketch|Average|
|---|---|---|---|---|---|---|---|
|ZS CLIP|9.18_±_0.62|10.03_±_0.16|9.93_±_0.51|10.25_±_0.40|9.90_±_1.30|9.54_±_1.13|9.81_±_0.30|
|CoOp|43.84_±_3.51|45.72_±_0.85|29.94_±_0.46|36.83_±_1.17|31.64_±_0.49|33.97_±_0.78|36.99_±_0.79|
|PromptFL|27.63_±_16.41|27.69_±_18.07|21.62_±_8.34|23.45_±_13.49|20.62_±_11.03|25.90_±_8.10|24.48_±_12.52|
|Prompt+FedProx|22.23_±_15.42|21.75_±_17.00|18.58_±_8.15|19.40_±_12.59|17.17_±_10.25|22.49_±_8.44|20.27_±_11.83|
|pFedMoAP|47.49_±_0.64|46.73_±_0.71|32.74_±_0.84|37.16_±_0.34|31.02_±_0.59|37.67_±_0.72|38.80_±_0.11|



Table 4: Results on Office-Caltech10 with feature shift and label shift with Dir( _α_ = 0 _._ 3) partition into 5 clients/domain 

||Amazon|Caltech|DSLR|Webcam|Average|
|---|---|---|---|---|---|
|ZS-CLIP(Radford et al., 2021)|9.83_±_1.63|10.67_±_0.89|10.89_±_1.40|6.20_±_3.84|9.40_±_0.77|
|CoOp(Zhou et al., 2022b)|30.29_±_3.64|35.88_±_1.30|29.89_±_5.15|33.43_±_2.25|32.37_±_1.81|
|PromptFL(Guo et al., 2023b)|21.08_±_9.60|23.72_±_12.21|22.94_±_7.96|25.88_±_7.72|23.41_±_9.06|
|Prompt+FedProx(Li et al., 2020b)|18.64_±_8.58|19.56_±_11.59|20.89_±_7.38|22.96_±_7.56|20.51_±_8.48|
|pFedMoAP|35.47_±_1.37|37.45_±_1.33|45.11_±_3.14|35.22_±_1.04|38.31_±_1.21|



remarkable ability to adapt to diverse scenarios under few-shot settings. In addition, pFedMoAP with _λ_ = 0 _._ 5 also beats _λ_ = 0 _._ 0 over all datasets, demonstrating the effectiveness of addressing the local prompt together with MoE. The results on CIFAR datasets (Tab. 2) further corroborate the efficacy of our method in handling extreme data heterogeneity with Dir( _α_ = 0 _._ 5) over 100 clients. In this challenging scenario, pFedMoAP still consistently outperforms the compared baselines, reflecting the potency to handle label shifts by introducing non-local experts to the clients. 

**Evaluation on Feature & Label Shifts.** To evaluate the performance of our method in scenarios closer to real-world FL applications, we introduce feature shift on top of label shift via DomainNet and Office-Caltech10 where each domain is partitioned into 5 clients with Dir( _α_ = 0 _._ 3), resulting in 30 and 20 total clients in DomainNet and Office-Caltech10, respectively. The results of these are presented in Tabs. 3 and 4, respectively. Under two types of heterogeneity, traditional federated learning methods struggle to benefit the clients. On average, the FedAvg style method PromptFL exhibits worse performance than the local training method CoOp by 12.51% and 8.96% respectively on DomainNet and Office-Caltech10. However, pFedMoAP remains better than local training and FL with up to 5.94% accuracy boost under both types of heterogeneity. This validates the effectiveness and robustness of pFedMoAP in scenarios closer to real-world federated settings. 

### 4.3 ABLATION STUDY 

**Impact of number of shot.** Following prior works (Li et al., 2024; Guo et al., 2023a), we investigate the impact of shots in the few-shot learning for pFedMoAP and other FL techniques implemented to prompt learning, namely PromptFL and PromptFL+FedProx, across the CLIP datasets. The number of shots varies from [1, 2, 4, 8, and 16]. As shown in Fig. 3, pFedMoAP consistently outperforms the other two methods across all datasets and shot numbers, demonstrating its superior effectiveness and robustness. While pFedMoAP outperforms the compared methods from only 1 shot, the gap between pFedMoAP and other methods widens as the number of shots increases. This demonstrates that pFedMoAP is particularly adept at leveraging additional training examples to enhance its performance, due to the introduction of MoE and the gating network. The trend of the curves also just that pFedMoAP has a more robust growth of performance when the number of shots increases, where the performances of the compared methods sometimes drop. 

**Impact of** _λ_ **, the coefficient for logit computed from local prompt.** In pFedMoAP, _λ_ balances the contribution between the logits generated from the local prompt and from MoE. Fig. 4 displays the results for _λ_ values ranging from 0.0 to 5.0 across the CLIP datasets. The trends reveal that although the optimal _λ_ value varies across datasets, a marginal address on the logits from the local prompt (e.g. _λ_ = 0 _._ 5 or 1) can already reach near-best performance. The flat plateau also indicates that the balance between the logits generated from the local prompt and from MoE is easy to reach. 

9 

Published as a conference paper at ICLR 2025 


![](P025_images/P025.pdf-0010-01.png)


Figure 3: Ablation study on the number of shots. 


![](P025_images/P025.pdf-0010-03.png)


Figure 4: Ablation study on the coefficient for the logits from local prompt, _λ_ . 

In addition, Fig. 4 also demonstrate a disinclination of too little or too much address on the local prompt-generated logits. We attribute this to the fact that only the local prompt is being updated on a client among all the experts, while immoderately addressing it ignores the benefit from MoE. 

## 5 CONCLUSION 

In this paper, we introduced pFedMoAP, a novel framework for personalized federated prompt learning in CLIP-like VLMs. Our approach leverages the lightweight nature of prompts to enable efficient cross-client knowledge sharing through a Mixture of Experts paradigm. By implementing a client-specific, attention-based gating network, pFedMoAP dynamically incorporates both local and non-local expert knowledge, striking a balance between personalization and collaborative learning. Extensive experiments across various datasets and federated settings demonstrate the superior performance of pFedMoAP compared to state-of-the-art alternatives, particularly in handling extreme data heterogeneity with label and/or feature shift. As federated learning continues to evolve, pFedMoAP represents a significant step forward in personalizing prompt learning for VLMs, opening new avenues for efficient and effective collaborative learning in privacy-preserving settings. 

10 

Published as a conference paper at ICLR 2025 

### ACKNOWLEDGMENTS 

This work was supported in part by a National Institutes of Health (NIH)/National Cancer Institute (NCI) grant (1R01CA218405), a NIH Other Transaction research contract 1OT2OD037972-01, the grant 1R01EB032896 (and a Supplement grant 3R01EB03 2896-03S1) as part of the National Science Foundation (NSF)/NIH Smart Health and Biomedical Research in the Era of Artificial Intelligence and Advanced Data Science Program, a NSF grant (CICI: SIVD: #2115082), an Amazon Machine Learning Research Award, and the University of Pittsburgh Momentum Funds (a scaling grant) for the Pittsburgh Center for AI Innovation in Medical Imaging. This work used Bridges-2 at Pittsburgh Supercomputing Center through allocation [MED200006] from the Advanced Cyberinfrastructure Coordination Ecosystem: Services & Support (ACCESS) program, which is supported by NSF grants #2138259, #2138286, #2138307, #2137603, and #2138296. The views and conclusions contained in this document are those of the authors and should not be interpreted as representing official policies, either expressed or implied, of the NIH or NSF. 

**Ethics Statement.** The research presented in this paper adheres to the ICLR Code of Ethics. Our study does not involve human or animal subjects. Every dataset used in our study is publicly available. Our method does not address discrimination/bias/fairness concerns. 

## REFERENCES 

- Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4 technical report. _arXiv preprint arXiv:2303.08774_ , 2023. 

- Manoj Ghuhan Arivazhagan, Vinay Aggarwal, Aaditya Kumar Singh, and Sunav Choudhary. Federated learning with personalization layers. _arXiv preprint arXiv:1912.00818_ , 2019. 

- Jinze Bai, Shuai Bai, Yunfei Chu, Zeyu Cui, Kai Dang, Xiaodong Deng, Yang Fan, Wenbin Ge, Yu Han, Fei Huang, et al. Qwen technical report. _arXiv preprint arXiv:2309.16609_ , 2023. 

- Lukas Bossard, Matthieu Guillaumin, and Luc Van Gool. Food-101–mining discriminative components with random forests. In _Computer Vision–ECCV 2014: 13th European Conference, Zurich, Switzerland, September 6-12, 2014, Proceedings, Part VI 13_ , pp. 446–461. Springer, 2014. 

- Zhongyi Cai, Ye Shi, Wei Huang, and Jingya Wang. Fed-CO2: Cooperation of online and offline models for severe data heterogeneity in federated learning. _Advances in Neural Information Processing Systems_ , 36, 2024. 

- Gary Cheng, Karan Chadha, and John Duchi. Fine-tuning is fine in federated learning. _arXiv preprint arXiv:2108.07313_ , 3, 2021. 

- Mircea Cimpoi, Subhransu Maji, Iasonas Kokkinos, Sammy Mohamed, and Andrea Vedaldi. Describing textures in the wild. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ , pp. 3606–3613, 2014. 

- Aidan Clark, Diego de Las Casas, Aurelia Guy, Arthur Mensch, Michela Paganini, Jordan Hoffmann, Bogdan Damoc, Blake Hechtman, Trevor Cai, Sebastian Borgeaud, et al. Unified scaling laws for routed language models. In _International conference on machine learning_ , pp. 4057– 4086. PMLR, 2022. 

- Liam Collins, Hamed Hassani, Aryan Mokhtari, and Sanjay Shakkottai. Exploiting shared representations for personalized federated learning. In _International conference on machine learning_ , pp. 2089–2099. PMLR, 2021. 

- Tianyu Cui, Hongxia Li, Jingya Wang, and Ye Shi. Harmonizing generalization and personalization in federated prompt learning. In _Forty-first International Conference on Machine Learning_ , 2024. URL https://openreview.net/forum?id=YYwERRXsJW. 

- Yuyang Deng, Mohammad Mahdi Kamani, and Mehrdad Mahdavi. Adaptive personalized federated learning. _arXiv preprint arXiv:2003.13461_ , 2020. 

11 

Published as a conference paper at ICLR 2025 

- Chen Dun, Mirian Hipolito Garcia, Guoqing Zheng, Ahmed Awadallah, Robert Sim, Anastasios Kyrillidis, and Dimitrios Dimitriadis. Fedjets: Efficient just-in-time personalization with federated mixture of experts. In _R0-FoMo: Robustness of Few-shot and Zero-shot Learning in Large Foundation Models_ , 2023. 

- Cynthia Dwork. Differential privacy. In _International colloquium on automata, languages, and programming_ , pp. 1–12. Springer, 2006. 

- Li Fei-Fei. Learning generative visual models from few training examples. In _Workshop on Generative-Model Based Vision, IEEE Proc. CVPR, 2004_ , 2004. 

- Chun-Mei Feng, Bangjun Li, Xinxing Xu, Yong Liu, Huazhu Fu, and Wangmeng Zuo. Learning Federated Visual Prompt in Null Space for MRI Reconstruction. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pp. 8064–8073, 2023. 

- Boqing Gong, Yuan Shi, Fei Sha, and Kristen Grauman. Geodesic flow kernel for unsupervised domain adaptation. In _2012 IEEE conference on computer vision and pattern recognition_ , pp. 2066–2073. IEEE, 2012. 

- Binbin Guo, Yuan Mei, Danyang Xiao, and Weigang Wu. Pfl-moe: personalized federated learning based on mixture of experts. In _Web and Big Data: 5th International Joint Conference, APWeb-WAIM 2021, Guangzhou, China, August 23–25, 2021, Proceedings, Part I 5_ , pp. 480– 486. Springer, 2021. 

- Tao Guo, Song Guo, and Junxiao Wang. pFedPrompt: Learning Personalized Prompt for VisionLanguage Models in Federated Learning. In _Proceedings of the ACM Web Conference 2023_ , pp. 1364–1374, 2023a. 

- Tao Guo, Song Guo, Junxiao Wang, Xueyang Tang, and Wenchao Xu. PromptFL: Let federated participants cooperatively learn prompts instead of models-federated learning in age of foundation model. _IEEE Transactions on Mobile Computing_ , 2023b. 

- Hussein Hazimeh, Zhe Zhao, Aakanksha Chowdhery, Maheswaran Sathiamoorthy, Yihua Chen, Rahul Mazumder, Lichan Hong, and Ed Chi. Dselect-k: Differentiable selection in the mixture of experts with applications to multi-task learning. _Advances in Neural Information Processing Systems_ , 34:29335–29347, 2021. 

- Tzu-Ming Harry Hsu, Hang Qi, and Matthew Brown. Measuring the effects of non-identical data distribution for federated visual classification. _arXiv preprint arXiv:1909.06335_ , 2019. 

- Yutao Huang, Lingyang Chu, Zirui Zhou, Lanjun Wang, Jiangchuan Liu, Jian Pei, and Yong Zhang. Personalized cross-silo federated learning on non-iid data. In _Proceedings of the AAAI conference on artificial intelligence_ , volume 35, pp. 7865–7873, 2021. 

- Chao Jia, Yinfei Yang, Ye Xia, Yi-Ting Chen, Zarana Parekh, Hieu Pham, Quoc Le, Yun-Hsuan Sung, Zhen Li, and Tom Duerig. Scaling up visual and vision-language representation learning with noisy text supervision. In _International conference on machine learning_ , pp. 4904–4916. PMLR, 2021. 

- Albert Q Jiang, Alexandre Sablayrolles, Antoine Roux, Arthur Mensch, Blanche Savary, Chris Bamford, Devendra Singh Chaplot, Diego de las Casas, Emma Bou Hanna, Florian Bressand, et al. Mixtral of experts. _arXiv preprint arXiv:2401.04088_ , 2024. 

- Peter Kairouz, H Brendan McMahan, Brendan Avent, Aur´elien Bellet, Mehdi Bennis, Arjun Nitin Bhagoji, Kallista Bonawitz, Zachary Charles, Graham Cormode, Rachel Cummings, et al. Advances and open problems in federated learning. _arXiv preprint arXiv:1912.04977_ , 2019. 

- Muhammad Uzair Khattak, Hanoona Rasheed, Muhammad Maaz, Salman Khan, and Fahad Shahbaz Khan. Maple: Multi-modal prompt learning. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pp. 19113–19122, 2023a. 

12 

Published as a conference paper at ICLR 2025 

- Muhammad Uzair Khattak, Syed Talal Wasim, Muzammal Naseer, Salman Khan, Ming-Hsuan Yang, and Fahad Shahbaz Khan. Self-regulating Prompts: Foundational model adaptation without forgetting. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pp. 15190–15200, 2023b. 

- Viraj Kulkarni, Milind Kulkarni, and Aniruddha Pant. Survey of personalization techniques for federated learning. In _2020 Fourth World Conference on Smart Trends in Systems, Security and Sustainability (WorldS4)_ , pp. 794–797. IEEE, 2020. 

- Hongxia Li, Zhongyi Cai, Jingya Wang, Jiangnan Tang, Weiping Ding, Chin-Teng Lin, and Ye Shi. FedTP: Federated Learning by Transformer Personalization. _IEEE Transactions on Neural Networks and Learning Systems_ , 2023. 

- Hongxia Li, Wei Huang, Jingya Wang, and Ye Shi. Global and local prompts cooperation via optimal transport for federated learning. _In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024. 

- Tian Li, Anit Kumar Sahu, Ameet Talwalkar, and Virginia Smith. Federated learning: Challenges, methods, and future directions. _IEEE Signal Processing Magazine_ , 37(3):50–60, 2020a. 

- Tian Li, Anit Kumar Sahu, Manzil Zaheer, Maziar Sanjabi, Ameet Talwalkar, and Virginia Smith. Federated optimization in heterogeneous networks. _Proceedings of Machine learning and systems_ , 2:429–450, 2020b. 

- Tian Li, Shengyuan Hu, Ahmad Beirami, and Virginia Smith. Ditto: Fair and robust federated learning through personalization. In _International Conference on Machine Learning_ , pp. 6357– 6368. PMLR, 2021a. 

- Xiaoxiao Li, Meirui Jiang, Xiaofei Zhang, Michael Kamp, and Qi Dou. FedBN: Federated learning on non-iid features via local batch normalization. _arXiv preprint arXiv:2102.07623_ , 2021b. 

- Paul Pu Liang, Terrance Liu, Liu Ziyin, Nicholas B Allen, Randy P Auerbach, David Brent, Ruslan Salakhutdinov, and Louis-Philippe Morency. Think locally, act globally: Federated learning with local and global representations. _arXiv preprint arXiv:2001.01523_ , 2020. 

- Jun Luo and Shandong Wu. Adapt to adaptation: Learning personalization for cross-silo federated learning. In _IJCAI: proceedings of the conference_ , volume 2022, pp. 2166. NIH Public Access, 2022. 

- Jun Luo, Matias Mendieta, Chen Chen, and Shandong Wu. Pgfed: Personalize each client’s global objective for federated learning. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pp. 3946–3956, 2023. 

- Saeed Masoudnia and Reza Ebrahimpour. Mixture of experts: a literature survey. _Artificial Intelligence Review_ , 42:275–293, 2014. 

- Brendan McMahan, Eider Moore, Daniel Ramage, Seth Hampson, and Blaise Aguera y Arcas. Communication-efficient learning of deep networks from decentralized data. In _Artificial intelligence and statistics_ , pp. 1273–1282. PMLR, 2017. 

- Maria-Elena Nilsback and Andrew Zisserman. Automated flower classification over a large number of classes. In _2008 Sixth Indian conference on computer vision, graphics & image processing_ , pp. 722–729. IEEE, 2008. 

- Bikang Pan, Wei Huang, and Ye Shi. Federated learning from vision-language foundation models: Theoretical analysis and method. _arXiv preprint arXiv:2409.19610_ , 2024. 

- Omkar M Parkhi, Andrea Vedaldi, Andrew Zisserman, and CV Jawahar. Cats and dogs. In _2012 IEEE conference on computer vision and pattern recognition_ , pp. 3498–3505. IEEE, 2012. 

- Xingchao Peng, Qinxun Bai, Xide Xia, Zijun Huang, Kate Saenko, and Bo Wang. Moment matching for multi-source domain adaptation. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pp. 1406–1415, 2019. 

13 

Published as a conference paper at ICLR 2025 

- Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, et al. Learning transferable visual models from natural language supervision. In _International conference on machine learning_ , pp. 8748–8763. PMLR, 2021. 

- Matthias Reisser, Christos Louizos, Efstratios Gavves, and Max Welling. Federated mixture of experts. _arXiv preprint arXiv:2107.06724_ , 2021. 

- Anit Kumar Sahu, Tian Li, Maziar Sanjabi, Manzil Zaheer, Ameet Talwalkar, and Virginia Smith. On the convergence of federated optimization in heterogeneous networks. _arXiv preprint arXiv:1812.06127_ , 3:3, 2018. 

- Noam Shazeer, Azalia Mirhoseini, Krzysztof Maziarz, Andy Davis, Quoc Le, Geoffrey Hinton, and Jeff Dean. Outrageously large neural networks: The sparsely-gated mixture-of-experts layer. _arXiv preprint arXiv:1701.06538_ , 2017. 

- Shangchao Su, Mingzhao Yang, Bin Li, and Xiangyang Xue. Cross-domain federated adaptive prompt tuning for clip. _arXiv preprint arXiv:2211.07864_ , 2022. 

- Guangyu Sun, Matias Mendieta, Jun Luo, Shandong Wu, and Chen Chen. Fedperfix: Towards partial model personalization of vision transformers in federated learning. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pp. 4988–4998, 2023. 

- Alysa Ziying Tan, Han Yu, Lizhen Cui, and Qiang Yang. Towards personalized federated learning. _IEEE Transactions on Neural Networks and Learning Systems_ , 2022. 

- A Vaswani. Attention is all you need. _Advances in Neural Information Processing Systems_ , 2017. 

- Luyuan Xie, Manqing Lin, Tianyu Luan, Cong Li, Yuejian Fang, Qingni Shen, and Zhonghai Wu. Mh-pflid: Model heterogeneous personalized federated learning via injection and distillation for medical data analysis. _arXiv preprint arXiv:2405.06822_ , 2024. 

- Kai Yi, Nidham Gazagnadou, Peter Richt´arik, and Lingjuan Lyu. Fedp3: Federated personalized and privacy-friendly network pruning under model heterogeneity. _arXiv preprint arXiv:2404.09816_ , 2024a. 

- Liping Yi, Han Yu, Chao Ren, Heng Zhang, Gang Wang, Xiaoguang Liu, and Xiaoxiao Li. pfedmoe: Data-level personalization with mixture of experts for model-heterogeneous personalized federated learning. _arXiv preprint arXiv:2402.01350_ , 2024b. 

- Kaiyang Zhou, Jingkang Yang, Chen Change Loy, and Ziwei Liu. Conditional prompt learning for vision-language models. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pp. 16816–16825, 2022a. 

- Kaiyang Zhou, Jingkang Yang, Chen Change Loy, and Ziwei Liu. Learning to prompt for visionlanguage models. _International Journal of Computer Vision_ , 130(9):2337–2348, 2022b. 

Yanqi Zhou, Tao Lei, Hanxiao Liu, Nan Du, Yanping Huang, Vincent Zhao, Andrew M Dai, Quoc V Le, James Laudon, et al. Mixture-of-experts with expert choice routing. _Advances in Neural Information Processing Systems_ , 35:7103–7114, 2022c. 

14 

Published as a conference paper at ICLR 2025 

## APPENDIX 

## A RELATED WORK 

**Personalized federated learning.** The mediocre performance of conventional federated learning (FL) (McMahan et al., 2017) over heterogeneous data calls for a more customized solution. Personalized federated learning (PFL) (Tan et al., 2022; Kulkarni et al., 2020), allowing tailored models for each client instead of a consensus model, systemically mitigates the data heterogeneity issue. Various strategies have been proposed to achieve personalization, including local fine-tuning (Cheng et al., 2021), different optimization techniques such as attentive message passing and regularization (Huang et al., 2021; Li et al., 2021a), and different personalized layers including feature extractor, classification head, attention, and batch normalization layers (Liang et al., 2020; Arivazhagan et al., 2019; Sun et al., 2023; Li et al., 2023; 2021b). Some works use separate models to learn global and local knowledge, respectively (Cai et al., 2024; Deng et al., 2020). Some recent PFL works also switch gear to model heterogeneity (Xie et al., 2024; Yi et al., 2024a). While promising in addressing data heterogeneity, these methods primarily focus on traditional machine learning models and do not leverage the capabilities of large pre-trained vision-language models. 

**Federated prompt learning for pre-trained models.** Prompt learning for pre-trained models combines models’ generalization capabilities and prompt learning’s flexibility in adapting these models to downstream tasks. As a fundamental work for this combination, CoOp (Zhou et al., 2022b) models a prompt’s context words with learnable vectors in CLIP. Such a combination has quickly drawn the attention of the FL community. For instance, PromptFL (Guo et al., 2023b) does a FedAvg (McMahan et al., 2017) style global aggregation over the locally updated prompts. Building upon this, FedPR (Feng et al., 2023) learns federated visual prompts for MRI reconstruction, while Fed-DPT (Su et al., 2022) applies both visual and textual prompt tuning to facilitate domain adaptation over decentralized data. pFedprompt (Guo et al., 2023a) integrating global consensus prompt and local attention over stored few-shot data for each client. FedOTP (Li et al., 2024) and FedPGP (Cui et al., 2024) employ Optimal Transport and prompt-wise contrastive loss, respectively, between global and local prompts, capturing diverse category traits on a per-client basis. Pan et al. (2024) presents a theoretical analysis framework for prompt-based federated learning of vision-language models. However, these approaches habitually adhere to the paradigm where locally learned prompts are not allowed for inter-client sharing before aggregation. While sharing full models between clients would be impractical due to the massive communication costs – _O_ ( _N_<sup>2</sup> _· M_ ) per round when _N_ models of size _M_ are distributed to _N_ clients (Luo & Wu, 2022; Luo et al., 2023) – sharing prompts is a different scenario. Since prompts are orders of magnitude smaller than full models (as shown in Fig. 1), the communication overhead becomes much more affordable. This makes it feasible for the inter-client sharing of pre-aggregated prompts under federated settings. 

**Federated learning with Mixture of Experts.** From the proprietary GPT-4 (Achiam et al., 2023) to the open-sourced Mixtral of Experts 8 _×_ 7B (Jiang et al., 2024), Qwen1.5-MoE (Bai et al., 2023), Mixture of Experts (MoE) (Zhou et al., 2022c; Masoudnia & Ebrahimpour, 2014) is prevailing long after its initial proposal thanks to the recent heat in Large Language Models (LLMs). Its application in FL, however, dates back before LLMs. FedMix (Reisser et al., 2021) and FedJETs (Dun et al., 2023) allow each client to construct an MoE with a shared gating network, selecting specific nonlocal models more adaptive to the client’s local data for ensembling. PFL-MoE(Guo et al., 2021) and pFedMoE (Yi et al., 2024b) incorporate the global aggregated model as the global expert and its locally fine-tuned model as a local expert to each client, achieving a personalized two-expert MoE. However, under federated settings, with too many experts on the client comes prohibitively high communication overhead (Reisser et al., 2021; Dun et al., 2023) while too few experts impairs the benefit of employing MoE. 

In contrast with the aforementioned methods, our proposed pFedMoAP, is a devised PFL method for prompt learning in CLIP-like VLMs. It sidesteps the impractical restriction on sharing the prompts without aggregation, while allowing a many-expert (e.g. 10 experts) MoE scenario for each client with negligible communication overhead, achieving efficient and effective personalization for the federated prompt learning. 

15 

Published as a conference paper at ICLR 2025 

## B PFE DMOAP: THE ALGORITHM 

We provide the overall algorithm of pFedMoAP below. 

**Algorithm 1** <u>pFedMoAP</u> 

**Input:** _N_ clients, learning rates _η_ 1 _, η_ 2, number of rounds _T_ , logit coefficient _λ_ , CLIP image/text encoder _f_ ( _·_ ) _, g_ ( _·_ ), datasets _{Di}i∈_ [ _N_ ] **Output:** Personalized prompts **_P_** 1 _,_ **_P_** 2 _, ...,_ **_P_** _N_ , gating network weights **_θ_** 1 _,_ **_θ_** 2 _, ...,_ **_θ_** _N_ . 

**ServerExecute:** 1: Server initialize **_P_** _g_<sup>0and the pool of prompt experts</sup><sup>_P_0as an empty set</sup> 2: Clients intialize **_θ_** 1 _,_ **_θ_** 2 _, ...,_ **_θ_** _N_ . 3: **for** _t ←_ 1 _,_ 2 _, ..., T_ **do** 4: Select a subset of _|St|_ clients, _St_ 5: **for** _i ∈St_ **in parallel do** 6: **if** Client _i_ does not have an entry in the server-maintained pool, _Pt_ **then** 7: **_P_** _i_<sup>_t_=ClientUpdate(</sup><sup>**_P_**</sup><sup>_t_</sup> _g_<sup>_−_1</sup> , standard=True) 8: **else** 9: Compute _Qi_ by _K_ nearest neighbor, given **_P_** _i_<sup>_t_=</sup><sup>_Pt−_1[</sup><sup>_i_].</sup> 10: **_P_** _NL_ = _{Pt−_ 1[ _j_ ] _}j∈Qi_ // prompt in the pool from selected group of clients 11: **_P_** _i_<sup>_t_=ClientUpdate(</sup><sup>**_P_**</sup><sup>_t_</sup> _g_<sup>_−_1</sup> , **_P_** _NL_ ) // downloaded as non-local experts 12: _Pt_ [ _i_ ] = **_P_** _i_<sup>_t_// cache to pool</sup> 13: **end if** 14: **_P_** _g_<sup>_t_= �</sup> _i∈St_<sup>_pi_</sup><sup>**_P_**</sup><sup>_t_</sup> _i_ 15: **end for** 16: **end for** 17: **return** **_P_** 1<sup>_T,_</sup><sup>**_P_**</sup><sup>_T_</sup> 2<sup>_, ...,_</sup><sup>**_P_**</sup><sup>_T_</sup> _N_<sup>and</sup><sup>**_θ_**1</sup><sup>_,_</sup><sup>**_θ_**2</sup><sup>_, ...,_</sup><sup>**_θ_**</sup><sup>_N_</sup> 

**ClientUpdate** ( **_P_** _g_<sup>_t−_1</sup> , **_P_** _NL_ =None, standard=False): 1: **_P_** _i_<sup>_t←_</sup><sup>**_P_**</sup><sup>_g_</sup> 2: **if** standard **then** 3: client does a standard fine-tuning 4: **else** 5: **for** ( **_x_** _k, yk_ ) _∈ Di_ **do** 6: **_T_** _L_ = _g_ ( **_P_** _i_<sup>_t_)</sup> 7: **_T_** _NL_ = _g_ ( **_P_** _NL_ ) 8: **_I_** _k_ = _f_ ( **_x_** _k_ ) 9: **_T_** _MoE_ = _G_ ( **_I_** _k,_ **_T_** _L,_ **_T_** _NL|_ **_θ_** _i_ ) 10: logit = sim( **_I_** _k,_ **_T_** _MoE_ ) + _λ ·_ sim( **_I_** _k,_ **_T_** _L_ ) 11: _p_ (ˆ _y_ = _c|_ **_x_** _k_ ) = Softmax(logit, _τ_ ) // _τ_ is the temperature 12: _Lce_ = _−_<sup>�</sup> _c_<sup>_y_</sup> _k_<sup>(</sup><sup>_c_)</sup><sup>_p_(ˆ</sup><sup>_y_=</sup><sup>_c|_</sup><sup>**_x_**</sup><sup>_k_)</sup> 13: **end for** 14: **end if** 15: **return** **_P_** _i_<sup>_t_</sup> 

## C ADDITIONAL EXPERIMENTS 

### C.1 DETAILS OF DATASET SETUP 

We follow the most recent prompt-based FL for VLMs works’ standard (Li et al., 2024; Cui et al., 2024) and use the 9 datasets they have used. Tab. 5 lists the details of these datasets and the partitioning method used in our experiments for each dataset. 

16 

Published as a conference paper at ICLR 2025 

Table 5: The statistics of each dataset and the partitioning details used in our experiments 

|Dataset|Trainingset size|Test set size|#Classes|#Clients|Sample Rate|Heterogeneity|
|---|---|---|---|---|---|---|
|Flowers102|4,093|2,463|102|10|100%|Pathological|
|OxfordPets|2,944|3,669|37|10|100%|Pathological|
|Food101|50,500|30,300|101|10|100%|Pathological|
|Caltech101|4,128|2,465|100|10|100%|Pathological|
|DTD|2,820|1,692|47|10|100%|Pathological|
|Offce-Caltech10|2,025|508|10|20|50%|Dir(0.3)|
|DomainNet|18,278|4,573|10|30|25%|Dir(0.3)|
|CIFAR10|50,000|10,000|10|100|10%|Dir(0.5)|
|CIFAR100|50,000|10,000|100|100|10%|Dir(0.5)|



### C.2 PFEDMOAP UNDER DIFFERENTIAL PRIVACY 

In pFedMoAP, clients remain unaware of the origin of non-local prompts, including which client they come from or the training round they were last updated in. Besides, the non-local prompts are downloaded after a KNN-based sparse selection process on the server. These factors collectively make it extremely difficult for a client to infer the gradient associated with a prompt or the data it has been trained with, which largely mitigates the privacy risk. 

Table 6: Performance under ( _ϵ_ , _δ_ )-differential privacy on CLIP datasets under pathological non-IID setting. 

||Flowers102|OxfordPets|Food101|Caltech101|DTD|
|---|---|---|---|---|---|
|**Without differential privacy (from Tab. 1)**||||||
|PromptFL(Guo et al., 2023b)|72.80_±_1.14|90.79_±_0.61|77.31_±_1.64|89.70_±_1.99|54.11_±_0.22|
|PromptFL+FedProx(Li et al., 2020b)|66.40_±_0.29|89.24_±_0.41|76.24_±_1.94|89.41_±_0.55|44.26_±_1.11|
|pFedMoAP(ours)|98.41_±_0.04|99.06_±_0.09|93.39_±_0.09|97.95_±_0.07|89.13_±_0.54|
|**With differential privacy (****_ϵ_ = 50)**||||||
|PromptFL(Guo et al., 2023b)|67.07_±_0.60|88.05_±_0.32|77.41_±_0.60|84.83_±_0.42|38.39_±_1.25|
|PromptFL+FedProx(Li et al., 2020b)|66.22_±_0.63|87.78_±_0.61|77.27_±_0.59|84.68_±_0.64|39.43_±_1.11|
|pFedMoAP(ours)|98.34_±_0.06|99.08_±_0.02|93.36_±_0.04|97.90_±_0.08|89.99_±_0.49|
|**With differential privacy (****_ϵ_ = 25)**||||||
|PromptFL(Guo et al., 2023b)|64.25_±_1.10|86.26_±_1.07|76.84_±_0.66|85.00_±_1.59|38.19_±_0.66|
|PromptFL+FedProx(Li et al., 2020b)|62.87_±_0.99|86.82_±_0.47|76.21_±_0.64|84.51_±_1.52|37.82_±_0.52|
|pFedMoAP(ours)|98.36_±_0.12|99.02_±_0.04|93.41_±_0.13|97.99_±_0.06|89.11_±_0.28|



Additionally, we evaluate how ( _ϵ_ , _δ_ )-differential privacy (DP) (Dwork, 2006) affects the performance of pFedMoAP on CLIP datasets and compare its performance with PromptFL and PromptFL+FedProx. This is achieved by clipping the gradients of the prompts and adding noise to the uploaded prompts. We set the failure probability _δ_ to be 0 _._ 05 and report the accuracy with the privacy budget _ϵ_ being set to 50 and 25. The results in Tab. 6 demonstrate that while the accuracy of PromptFL and PromptFL+FedProx significantly drop with privacy guarantees, DP’s impact in accuracy performance to pFedMoAP remains minimal for different privacy budgets. This is because the gating network in pFedMoAP is maintained locally for the entirety of the training process, and its multi-head attention layer learns proper transformations for the experts to align with the image features, mitigating the impact of the noise-contaminated prompts. 

### C.3 ATTENTION-BASED VS. LINEAR PROJECTION-BASE GATING NETWORK 

Table 7: Comparison between the proposed attention-based gating network and the linear projectionbased gating network 

||Flowers102|OxfordPets|Food101|Caltech101|DTD|
|---|---|---|---|---|---|
|Linear projection-based (3 experts)|86.92_±_1.84|90.54_±_1.33|78.19_±_3.07|89.59_±_1.46|61.42_±_5.43|
|Linear projection-based (10 experts)|69.64_±_4.57|52.78_±_6.88|77.39_±_3.29|86.57_±_1.96|30.42_±_7.14|
|Attention-based, with aggregation|97.56_±_0.07|98.24_±_0.12|91.89_±_0.19|96.17_±_0.18|87.52_±_0.69|
|Attention-based, without aggregation (ours)|98.41_±_0.04|99.06_±_0.09|93.39_±_0.09|97.95_±_0.07|89.13_±_0.54|



17 

Published as a conference paper at ICLR 2025 

We compare the proposed attention-based gating network against the traditional linear projectionbased gating network. The results are reported in Tab. 7 which strongly favor the attention-based approach, showing significantly better and more stable performance across all datasets. Notably, the linear projection-based approach struggles with larger numbers of experts (10 experts vs 3 experts), while the attention-based method maintains high performance. This is because the attention-based gating network 1) is more robust to adaptive experts; 2) serves as linear probing with more capacity; 3) leverages CLIP’s feature alignment with attention mechanism; and 4) is agnostic to experts’ order (detailed strength of attention-based approach over linear projection is described in Sec. 3.3). 

In addition, we choose to avoid aggregating the gating network due to its larger size. The gating network can be magnitudes larger than the prompts (see Tab. 9), which would largely increase the communication overhead. This design choice also aims for higher performance. As the deepest parameterized module of the entire model, the gating network should be fully “personalized” as opposed to “globalized” to achieve higher performance (Arivazhagan et al., 2019; Collins et al., 2021). The process of aggregating the gating network limits the level of its personalization, which yields worse results than our method that keeps the gating network locally (see Tab. 7). 

### C.4 ADDITIONAL ABLATION STUDY 

Table 8: Ablation study: impact of number of experts ( _K_ non-local experts + 1 local experts) to pFedMoAP on DomainNet 

||Clipart|Infograph|Painting|Quickdraw|Real|Sketch|Average|
|---|---|---|---|---|---|---|---|
|_K_+ 1 = 5|47.20_±_0.30|46.80_±_0.48|32.54_±_0.42|37.67_±_0.52|31.50_±_0.65|36.09_±_0.92|38.63_±_0.29|
|_K_+ 1 = 10|46.89_±_1.07|46.15_±_0.95|32.76_±_0.42|37.70_±_1.02|31.94_±_0.83|36.84_±_1.21|38.71_±_0.45|
|_K_+ 1 = 15|47.36_±_1.12|46.29_±_0.83|32.76_±_0.57|37.76_±_0.98|31.78_±_0.72|36.67_±_1.03|38.77_±_0.38|
|_K_+ 1 = 20|47.49_±_0.64|46.73_±_0.71|32.74_±_0.84|37.16_±_0.34|31.02_±_0.59|37.67_±_0.72|38.80_±_0.11|
|_K_+ 1 = 25|47.56_±_0.92|46.89_±_1.30|32.23_±_0.97|38.03_±_1.14|31.66_±_0.77|36.79_±_1.02|38.86_±_0.43|
|_K_+ 1 = 30|47.56_±_0.87|46.64_±_1.38|32.19_±_0.89|37.93_±_1.22|31.80_±_0.95|37.01_±_1.08|38.85_±_0.43|



**Number of experts.** We present an ablation study examining how the number of experts ( _K_ nonlocal experts + 1 local expert) affects pFedMoAP’s performance on the DomainNet dataset. The results in Tab. 8 show that the average performance gradually improves as the number of experts increases from 5 to 30. Fig. 5 plots the trend of performance with different numbers of experts from 5 to 40 on CIFAR10. For both datasets, it plateaus around larger numbers of experts, suggesting that while having multiple experts is beneficial, there’s a point of diminishing returns. This is because the extra downloaded experts (selected last by our KNN-based expert selection mechanism) by a client are trained from the data that is distinctly distributed from the client’s local data distribution. This shows that the proposed method does not require an excessive number of experts to achieve high performance. 


![](P025_images/P025.pdf-0018-07.png)

### Figure analysis

Purpose: The plot visualizes an ablation study of how the number of experts affects pFedMoAP performance on CIFAR10 with 100 clients.

Plot structure:
- Single-panel line plot with circular markers.
- X-axis: **Number of Experts**, with values 5, 10, 15, 20, 25, 30, 35, and 40.
- Y-axis: **Accuracy (%)**, shown over a narrow range around 83.2%–83.6%.
- No legend is present because only one series is plotted.
- No explicit title appears inside the plot; the surrounding caption identifies it as the impact of the number of experts on CIFAR10 with 100 clients.

Direct visual observations:
- Accuracy is lowest near 5 experts and rises by 10 experts.
- There is a dip at 15 experts, followed by improvement at 20 and 25 experts.
- Accuracy drops again around 30 experts.
- The highest visible point occurs at 35 experts.
- The value at 40 experts is slightly lower than at 35 experts but remains among the highest points.
- The plotted curve is not strictly monotonic; it fluctuates while showing an overall upward tendency from low to higher expert counts.

Approximate visual readings from the gridlines, not exact annotated values:

| Number of experts | Accuracy trend from plot |
|---:|---|
| 5 | lowest point, slightly above 83.20% |
| 10 | around 83.35% |
| 15 | below 83.25% |
| 20 | around 83.39% |
| 25 | around 83.50% |
| 30 | around 83.34% |
| 35 | highest point, just under 83.60% |
| 40 | slightly below the 35-expert result |

Interpretation in context:
- The plot supports the paper text’s claim that increasing the number of experts can improve performance, but the gains are modest and non-monotonic.
- The improvement appears to plateau at larger expert counts, consistent with the surrounding discussion that additional experts eventually provide diminishing returns.
- The fluctuations, especially the drops at 15 and 30 experts, suggest that simply adding experts does not guarantee consistent improvement, likely because some additional experts may be less aligned with a client’s local data distribution.


Figure 5: The impact of the number of experts on CIFAR10 with 100 clients 

18 

Published as a conference paper at ICLR 2025 

Table 9: Ablation study: the impact of output dimension of CLIP backbone to pFedMoAP on CLIP datasets. For _d_ feature _<_ 1024, a pooling layer is added after the _d_ feature = 1024 feature from the backbone to reduce the size of the gating network as mentioned in Sec. 3.3 

||Gating network size|Flowers102|OxfordPets|Food101|Caltech101|DTD|
|---|---|---|---|---|---|---|
|_d_feature = 32|4.2K|97.28_±_0.18|98.75_±_0.32|93.42_±_0.08|97.37_±_0.08|88.61_±_0.89|
|_d_feature = 64|16.6K|98.55_±_0.10|98.91_±_0.23|93.89_±_0.12|97.75_±_0.12|89.96_±_0.09|
|_d_feature = 128|66.0K|98.41_±_0.04|99.06_±_0.09|93.39_±_0.09|97.95_±_0.07|89.13_±_0.54|
|_d_feature = 256|263.2K|99.01_±_0.05|98.88_±_0.21|92.49_±_0.20|97.93_±_0.07|90.88_±_0.16|
|_d_feature = 512|1.1M|98.18_±_0.38|96.85_±_0.22|90.34_±_0.31|96.99_±_0.11|89.65_±_0.10|
|_d_feature = 1024|4.2M|98.11_±_0.33|95.81_±_0.84|89.20_±_0.37|96.82_±_0.26|89.03_±_0.14|



**Feature dimension.** We investigate the impact of the output dimension ( _d_ feature) of the CLIP backbone on pFedMoAP’s performance across CLIP datasets. The study shows that moderate feature dimensions (128-256) generally yield the best results, with _d_ feature = 128 or 256 consistently performing well across all datasets. Lower feature dimensions ( _d_ feature = 32 or 64) have less capacity, failing to unlock the full potential of the pre-trained VLM. High dimensions ( _d_ feature = 128 or 1024) significantly increase the size of the gating network. With less training data on a client, high dimensions lead to overparameterized gating network, resulting in slightly degraded performance. This suggests that a relatively compact feature dimension is sufficient and possibly preferable for the attention-based gating mechanism. 


![](P025_images/P025.pdf-0019-04.png)



![](P025_images/P025.pdf-0019-05.png)



![](P025_images/P025.pdf-0019-06.png)



![](P025_images/P025.pdf-0019-07.png)



![](P025_images/P025.pdf-0019-08.png)



![](P025_images/P025.pdf-0019-09.png)


Figure 6: Contribution of the experts based on averaged attention score across all test images. The first five charts are for CLIP datasets, for which there are 10 clients in each dataset. The last chart is for DomainNet with a total of 30 clients. 

**Visualization of contribution for each expert.** To have a clear understanding of how the experts contribute to the MoE text feature ( **_T_** _MoE_ ), we visualize the contribution of the local and non-local experts towards it. This is achieved by taking the following steps. For each image in a client’s test set, we compute the attention score (softmax of scaled dot product between the image and text features (Vaswani, 2017)) for each expert (local and non-local) through the multi-head attention layer in the proposed gating network. The scores from non-local experts are sorted in a descending manner. All scores are averaged over the test set across all clients. We visualize the averaged scores under 6 datasets in Fig. 6. From this figure, we can see that **1)** every expert has a non-trivial contribution to **_T_** _MoE_ , the text feature generated from the MoE, indicating that each expert is indispensable in the whole design; 2) as a result of the minimization, the contribution from the local experts to the MoE is not the highest. This is reasonable since besides the **_T_** _MoE_ , Eq. (10)’s second term optimizes the 

19 

Published as a conference paper at ICLR 2025 

text feature from the local expert itself ( **_T_** _L_ ) based on the image feature, which directly contributes to the loss; and 3) although not the highest, the contribution from the local expert to the MoE is still among the highest ones as it is the only expert that is updated during local training with fixed non-local prompts. 

20 

