# **Implicit Federated In-context Learning For Task-Specific LLM Fine-Tuning** 

## **Dongcheng Li**<sup>1</sup> **, Junhan Chen**<sup>1</sup> **, Aoxiang Zhou**<sup>1</sup> **, Chunpei Li**<sup>1</sup> **, Youquan Xian**<sup>2</sup> **, Peng Liu**<sup>1</sup> **, Xianxian LI**<sup>1</sup> 

1Key Lab of Education Blockchain and Intelligent Technology, Ministry of Education, Guangxi Normal University, Guilin, Guangxi 541004, China 

2School of Cyberspace Security, Beijing University of Posts and Telecommunications, Beijing 100876, China 

#### **Abstract** 

As large language models continue to develop and expand, the extensive public data they rely on faces the risk of depletion. Consequently, leveraging private data within organizations to enhance the performance of large models has emerged as a key challenge. The federated learning paradigm, combined with model fine-tuning techniques, effectively reduces the number of trainable parameters. However,the necessity to process high-dimensional feature spaces results in substantial overall computational overhead. To address this issue, we propose the Implicit Federated In-Context Learning (IFed-ICL) framework. IFed-ICL draws inspiration from federated learning to establish a novel distributed collaborative paradigm, by converting client local context examples into implicit vector representations, it enables distributed collaborative computation during the inference phase and injects model residual streams to enhance model performance. Experiments demonstrate that our proposed method achieves outstanding performance across multiple text classification tasks. Compared to traditional methods, IFed-ICL avoids the extensive parameter updates required by conventional finetuning methods while reducing data transmission and local computation at the client level in federated learning. This enables efficient distributed context learning using local privatedomain data, significantly improving model performance on specific tasks. 

## **Introduction** 

In recent years, the rapid development of Large Language Models (LLMs) has brought about a revolutionary transformation in the field of artificial intelligence. These models have not only pushed the boundaries of technology but also reshaped the fundamental paradigm of human-computer interaction. Trained on massive textual datasets and built upon deep neural network architectures, models such as the GPT series, LLaMA, and PaLM have demonstrated unprecedented capabilities in language understanding and generation, surpassing the limitations of traditional natural language processing approaches. As the number of parameters has scaled from billions to hundreds of billions, LLMs have exhibited remarkable emergent abilities, such as reasoning, planning, coding, and cross-modal understanding. The 

Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved. 

widespread adoption of LLMs has permeated various domains, including intelligent dialogue systems, creative writing assistance, medical diagnosis support, scientific research acceleration, and personalized education. These applications not only enhance efficiency and innovation but also provide new tools for addressing the complex challenges faced by humanity. 

As the parameters and functionalities of LLMs continue to grow,their rate of data consumption is also increasing rapidly. Studies have shown that publicly available highquality textual data is expected to be exhausted between 2026 and 2032 (Ye et al. 2024). Reusing existing datasets not only limits the upper bound of model performance but also risks overfitting and reduces the model’s generalization ability. According to a survey conducted by Epoch AI, the total global volume of textual data is approximately 31 trillion tokens, with publicly available data comprising only a small fraction. In contrast, private data, which is often of higher quality and more domain-specific, has emerged as the new frontier for breakthroughs in model performance (Jones 2024). As a result, Federated Learning(FL) has emerged as a highly attractive solution, enabling users to supplement large models with knowledge derived from privately held data through collaborative multi-party training. This approach effectively enhances the reasoning capabilities of LLMs for specific tasks. 

To improve the performance of foundation models on specific tasks, two main paradigms have emerged: fine-tuning and In-Context Learning (ICL) (Brown et al. 2020). Finetuning approaches include full fine-tuning and parameterefficient fine-tuning methods such as LoRA(Hu et al. 2022) and P-Tuning-v2(Liu et al. 2021). In contrast, In-Context Learning is a training-free approach that guides the model to perform specific tasks by providing a few examples during inference, significantly lowering the barrier to entry for task adaptation. 

To effectively leverage high-quality private data within organizations, recent studies (Peng et al. 2024; Wu et al. 2024a) have proposed combining FL with fine-tuning techniques. While federated fine-tuning can adapt LLM to downstream tasks, it requires updating model parameters within high-dimensional feature spaces, leading to significant computational overhead. Consequently, the deployment of Federated Large Language Models (FedLLMs) faces substantial 

challenges in practice. One significant barrier is the communication cost. For instance, transmitting the parameters of LLaMA3.1-405B over a 100 Mbps network would require more than 36 hours, which far exceeds the capacity of contemporary communication systems. On the other hand, approaches based on ICL (Wu et al. 2024b; Zhang et al. 2024b) involve collecting examples from multiple clients and incorporating them into the inference prompt. However, this fundamentally violates the principle of data locality in federated learning and poses a serious risk of sensitive information leakage. 

To address the limitations of ICL, (Li et al. 2024) offers a novel perspective by converting contextual examples into vector representations and injecting them into LLMs to perform inference tasks. This work provides valuable inspiration for our research. Building upon it, we propose a collaborative framework named Implicit Federated In-Context Learning, which aims to tackle the dual challenges of computational inefficiency in traditional federated fine-tuning and the limited collaborative capacity of conventional ICL. Unlike traditional FL paradigms that require extensive local training on client devices, our approach innovatively decomposes the federated process into two parts: the extraction of context vectors and the collaborative computation of injection coefficients. This significantly reduces the computational burden on local clients. 

We implement efficient collaboration through a threestage process. In the first stage, each participating client designs task-specific context templates, converts local data into context vectors, and sends them to the server for aggregation. In the second stage, the server returns the aggregated global context vectors to each client, where clients compute the perplexity loss using their local data to calibrate the injection coefficients. These coefficients are then sent back to the server for aggregation. After several rounds of iterative optimization, the injection coefficients are refined to ensure optimal integration of contextual information into the LLM. Finally, in the third stage, the server distributes the calibrated coefficients to clients, which can then convert the raw LLM into a task-specific LLM with a single linear injection operation. This design not only reduces computational and communication overhead but also achieves an effective decoupling of data utilization and model training, offering a new paradigm for distributed AI collaboration in resourceconstrained environments.The main contributions of this paper are as follows: 

- we propose a novel federated ICL paradigm. Instead of synthesizing contextual data, our method transmits and aggregates context vectors, which are then injected during the model inference phase to enhance performance. 

- In contrast to traditional FL, our approach decomposes the federated process into two components: context vector aggregation and injection coefficient training. Clients are responsible for converting local data into context vectors and performing lightweight training of injection coefficients. This design significantly reduces communication bandwidth requirements and computational overhead, enabling effective participation from resource- 

constrained devices. 

- Extensive experiments across multiple text classification tasks demonstrate that, compared to federated parameter fine-tuning, IFed-ICL reduces clients computational overhead by more than 20 times and communication costs by approximately 10<sup>4</sup> times, thereby ensuring the feasibility of large-scale federated deployment. 

## **Related Work** 

### **Federated Fine-Tuning** 

FL is a distributed machine learning paradigm that enables multiple clients to collaboratively train a global model by exchanging model parameters without exposing their raw local data(McMahan et al. 2017; Koneˇcn`y et al. 2016; Yang et al. 2019). Its primary goal is to mitigate the systemic privacy risks inherent in traditional centralized data collection (Kairouz et al. 2021). In recent years, LLMs have achieved remarkable breakthroughs in performance. However, the scale of publicly available datasets has approached its limit, and further development of these models is increasingly constrained by the challenge of ”data silos” (Villalobos et al. 2022). Federated Large Language Models (FedLLMs) (Chen et al. 2023) have been proposed in this context, aiming to combine the powerful generalization capabilities of LLMs with the privacy-preserving advantages of FL. 

Nevertheless, the implementation of FedLLMs continues to face formidable challenges. When the number of model parameters reaches the scale of billions, full-parameter finetuning of LLMs results in massive communication overhead, which severely limits their scalability in practical deployments (Shu et al. 2024). To address this, ParameterEfficient Fine-tuning (PEFT) has become the mainstream optimization pattern (Hu et al. 2024). The core idea is to freeze the majority of the LLM’s parameters and fine-tune only a small set of newly added or selectively chosen parameters, thereby reducing the computational, storage, and communication burden on client devices. The FedPETuning framework (Zhang et al. 2023) was among the earliest to systematically incorporate multiple PEFT methods (including LoRA) into FL settings, demonstrating the feasibility of significantly lowering communication costs by aggregating only a small portion of trainable parameters. 

Beyond LoRA and its variants, other PEFT strategies have also provided diverse and efficient fine-tuning paths for FedLLMs. In adapter-based methods, FedAdapter (Cai et al. 2022) enhances training efficiency by dynamically configuring adapters and leveraging activation caching, while FeDeRA (Yan et al. 2024) initializes low-rank adapters via singular value decomposition (SVD) to improve performance under Non-IID data distributions. Prompt-based methods have gained significant attention due to their extremely low communication overhead. For example, FedPepTAO (Che et al. 2023) achieves efficient fine-tuning through partial prompt tuning and dual-end adaptive optimization. Additionally, some selective PEFT methods, such as BitFit (Zaken, Ravfogel, and Goldberg 2021), which only fine-tunes bias parameters, and FedAMoLE (Zhang et al. 2024a), which builds mixtures of LoRA experts for highly heteroge- 

neous scenarios, demonstrate strong potential in improving both personalization and efficiency. 

Furthermore, Federated Knowledge Distillation (FKD) offers an alternative approach to reducing communication overhead by allowing clients to transmit compact representations of knowledge instead of full model parameters. For instance, AdaFedSelecKD (Feng et al. 2024) adopts adapter-based selective knowledge distillation to improve communication efficiency. These communication optimization techniques are not mutually exclusive with PEFT methods.Despite a series of advancements in efficient parameter tuning, the process fundamentally relies on executing gradient updates and backpropagation within high-dimensional parameter spaces. Consequently, the reduction in computational overhead is inherently constrained by the upper limit of the trainable rank. 

### **In-Context Learning** 

Compared to parameter fine-tuning,which requires explicitly updating model weights via backpropagation,ICL enables LLMs to adapt to new tasks during inference simply by providing demonstration examples, without modifying any model parameters. This opens up a new lightweight deployment pathway for LLMs. The study by (Von Oswald et al. 2023) reveals that the Transformer architecture can implicitly simulate gradient descent dynamics during inference, offering key insights into the underlying mechanism of ICL. Complementarily, (Wies, Levine, and Shashua 2023) provides a rigorous theoretical perspective based on Probably Approximately Correct learning theory, emphasizing the decisive impact of context example quality on ICL performance and laying a foundational framework for subsequent methodological innovations. 

In the domain of ICL optimization, the empirical study by (Agarwal et al. 2024) demonstrates that increasing the number of in-context examples initially improves model performance on open-ended tasks. (Bertsch et al. 2024) further investigates the model’s capacity to utilize extended context windows containing numerous examples. To address the limitation of context window length, (Ye et al. 2023) proposes a retrieval-augmented approach that dynamically selects task-relevant exemplars, significantly enhancing inference accuracy. However, such strategies rely heavily on the precision of the retrieval system and inevitably introduce additional architectural complexity. (Huang et al. 2024) explores techniques for compressing multiple examples into compact latent representations, thereby reducing inference costs and improving performance in multimodal ICL settings. Nonetheless, practical deployment is constrained by the requirement to access internal model states. (Hendel, Geva, and Globerson 2023) conceptualizes the transformation of multiple in-context examples into a single task vector to guide model inference, thereby simplifying traditional explicit example enumeration. Expanding on this line of research, (Li et al. 2024) injects task-relevant context directly into intermediate activation layers of the model. This strategy significantly reduces reliance on long contexts and improves computational efficiency. 

In FL scenarios, ICL can be leveraged to enhance model 

personalization while avoiding the direct sharing of sensitive data. Methods such as (Wu et al. 2024b; Zhang et al. 2024b) combine the context learning capabilities of LLMs with FL by having servers and clients share LLM-generated synthetic data, allowing clients to fine-tune using locally private datasets. (Wang et al. 2025) achieves efficient and low-overhead learning for question-answering tasks in distributed environments by applying ICL using high-quality local data at each client, and employing a parameter-free communication strategy. However, these approaches commonly assume an infinite context window, overlooking truncation bias and exemplar overflow effects caused by token limits, which results in significant performance degradation in long-sequence scenarios. 

## **Proposed Framework** 

In this section, we present the workflow of IFed-ICL. As illustrated in Figure 1, the overall collaborative framework of IFed-ICL is divided into three key stages. 

### **System Setup** 

In IFed-ICL, the system consists of _K_ clients and a central server. The server maintains both a conventional storage database and a vector database to store task-related information and aggregated context vectors. Each client possesses its own private dataset _Dk_ and a pre-trained LLM _M_ . Based on the requirements of a specific task, the server defines a context example template _T_ and distributes it to the clients. Each client then uses the template to label relevant data from its local private dataset _Dk_ as context examples _Ek_ = _{_ ( _sk,j, ok,j_ ) _}_<sup>_N_</sup> _j_ =1<sup>_k_, where (</sup><sup>_sk,j, ok,j_) denotes the</sup><sup>_j_-th</sup> input-output pair and _Nk_ is the number of examples generated by client _k_ . The ultimate goal is to leverage these private context examples from multiple clients to collaboratively enhance the large model’s representational capacity and generalization ability. 

### **Phase 1: Context Vector Extraction and Upload** 

At the beginning of each round of collaboration in IFedICL, the server and the selected participating clients _k ∈K_ first perform forward propagation using the large language model _M_ on each demonstration example ( _sk,j, ok,j_ ). During this process, the context examples are used at the token positions required for prediction in each layer of the model to extract intermediate activation vectors. These activation vectors include the outputs from the Multi-Head Attention (MHA) and Multi-Layer Perceptron (MLP) modules across all _L_ Transformer layers. Let the MHA and MLP activations extracted from the _l_ -th layer of example _sk,j_ be denoted as _a_<sup>_e_</sup> _k,j,l_<sup>and</sup><sup>_me_</sup> _k,j,l_<sup>,respectively.Theselayer-wiseactivations</sup> are then fused to form the demonstration vector for the example: 


![](P043_images/P043.pdf-0003-13.png)

### Figure analysis

Purpose: This equation formalizes how IFed-ICL constructs a demonstration vector from intermediate activations of a pretrained large language model during context vector extraction.

Equation transcribed:

\[
d'_{k,j} = \{a^e_{k,j,l}, m^e_{k,j,l}\}_{l=1}^{L}
\tag{1}
\]

Direct observations:
- The left-hand side, \(d'_{k,j}\), denotes the demonstration vector for the \(j\)-th example belonging to client \(k\).
- The right-hand side is a layer-wise collection over \(l = 1, \ldots, L\).
- For each Transformer layer \(l\), two activation types are included:
  - \(a^e_{k,j,l}\): activation associated with the Multi-Head Attention module.
  - \(m^e_{k,j,l}\): activation associated with the Multi-Layer Perceptron module.
- The superscript \(e\) indicates that these activations are extracted from context/example demonstrations.

Interpretation:
- The equation indicates that IFed-ICL represents each local demonstration example not by raw text or labels, but by a structured set of internal model activations.
- Because both attention and MLP activations are collected across all \(L\) Transformer layers, the resulting vector is intended to encode multi-level contextual information from the model.

Connection to surrounding text:
- This equation appears in Phase 1 of the IFed-ICL workflow, where clients process private context examples through the pretrained LLM and extract intermediate activation vectors.
- The surrounding text states that these per-example demonstration vectors are later averaged locally to form a client context vector \(v_k\), which is uploaded to the server for federated aggregation.
- Thus, Equation (1) is the first formal step in converting private client demonstrations into compact vector representations for collaborative in-context learning without sharing raw private data.


Finally, the server and client _k_ compute the arithmetic mean of all locally generated demonstration vectors 


![](P043_images/P043.pdf-0004-00.png)



![](P043_images/P043.pdf-0004-01.png)



![](P043_images/P043.pdf-0004-02.png)



![](P043_images/P043.pdf-0004-03.png)



![](P043_images/P043.pdf-0004-04.png)



![](P043_images/P043.pdf-0004-05.png)



![](P043_images/P043.pdf-0004-06.png)



![](P043_images/P043.pdf-0004-07.png)



![](P043_images/P043.pdf-0004-08.png)



![](P043_images/P043.pdf-0004-09.png)



![](P043_images/P043.pdf-0004-10.png)



![](P043_images/P043.pdf-0004-11.png)



![](P043_images/P043.pdf-0004-12.png)


Figure 1: Overall of IFed-ICL framework.First stage: Each client extracts vector representations from its private dataset _Dk_ and transmits them to the server for aggregation. Second stage: Clients collaboratively calibrate the injection coefficients Λ by minimizing the perplexity loss on their local data in coordination with the server. Third stage: The trained injection coefficients and the aggregated global context vector are utilized to enable in-context learning for the large language model. 

_{d_<sup>_′_</sup> _k,j_<sup>_}_</sup> _j_<sup>_N_</sup> =1<sup>_k_to obtain the local context vector</sup><sup>_vk_:</sup> 


![](P043_images/P043.pdf-0004-15.png)


where the averaging is performed element-wise across each dimension of the vectors. After generating _vk_ , the client uploads it to the central server. Since _vk_ is a compact vector representation, its size is significantly reduced compared to the original data or large-scale model parameters. 

### **Stage 2: Global Context Vector Aggregation and Coefficient Calibration** 

After receiving the local context vectors _vk_<sup>_t_from all partic-</sup> ipating clients _k ∈Kt_ , the central server first aggregates these vectors to form a global context vector _vg_<sup>_t_. The aggre-</sup> gation method adopts Federated Averaging: 


![](P043_images/P043.pdf-0004-19.png)


Let the corresponding components of the _l_ -th layer MHA and MLP of the global context vector _vg_<sup>_t_be denoted as (</sup> _<u>a</u>_<sup>_~~e~~_</sup> _l_<sup>)</sup><sup>_t_</sup> _g_ and <u>(</u> _<u>m</u>_<sup>_~~e~~_</sup> _l_<sup>)</sup><sup>_t_</sup> _g_<sup>.</sup> 

By configuring a set of hyperparameters Λ, the model’s residual stream during inference can be injected with contextual information to achieve the goal of in-context learning. 


![](P043_images/P043.pdf-0004-22.png)


The client first initializes the hyperparameters Λ _k_ and uses the local dataset _Ek_ to optimize and calibrate the injection coefficients of the context vector. For each calibration sample ( _x_<sup>_k_</sup> _i_<sup>_, y_</sup> _i_<sup>_k_)</sup><sup>_∈Dk_, the client feeds it into the model</sup><sup>_M_and</sup> performs layer-wise forward propagation. Assume that for the query _x_<sup>_k_</sup> _i_<sup>,the MHAand MLPactivations atlayer</sup><sup>_l_and</sup> token position _τ_ are denoted as _a_<sup>_k_</sup> _l,τ_<sup>and</sup><sup>_mk_</sup> _l,τ_<sup>respectively.</sup> Then, the updated residual stream after injection _rl,τ_<sup>_k_is:</sup> 

_rl,τ_<sup>_k←r_</sup> _l_<sup>_k_</sup> _−_ 1 _,τ_<sup>+ (</sup><sup>_λa_</sup> _l_<sup><u>(</u></sup> _<u>a</u>_<sup>_~~e~~_</sup> _l_<sup>)</sup><sup>_t_</sup> _g_<sup>+</sup><sup>_β_</sup> _l_<sup>_aak_</sup> _l,τ_<sup>) + (</sup><sup>_λ_</sup> _l_<sup>_m_</sup><sup><u>(</u></sup> _<u>m</u>_<sup>_~~e~~_</sup> _l_<sup>)</sup><sup>_t_</sup> _g_<sup>+</sup><sup>_β_</sup> _l_<sup>_mmk_</sup> _l,τ_<sup>)(5)</sup> Subsequently, all clients perform _n_ rounds of joint training with the server, optimizing the injection coefficients Λ _k_ by minimizing the perplexity loss on the calibration dataset _Dk_ . 


![](P043_images/P043.pdf-0004-25.png)


Upon receiving the local injection coefficients from all participating clients, the server aggregates them to compute the global injection coefficients. Λ<sup>(</sup> _g_<sup>_n_):</sup> 


![](P043_images/P043.pdf-0004-27.png)


After receiving the global injection coefficients returned by the server, each client uses Equation 6 to iteratively compute Λ<sup>(</sup> _k_<sup>_n_). After</sup><sup>_n_iterations, the training is completed. This</sup> 

optimization process only targets the injection coefficients Λ, whose number is significantly smaller than that of the LLM parameters. For the global context vector, only a single round of aggregation is required. Furthermore, this approach can adapt to incremental data scenarios, where only the incremental context vectors need to be aggregated over multiple rounds, and this can be computed in parallel with the calibration of injection coefficients. 

### **Stage 3: Global Calibration Coefficients Injection** 

After calibration is completed, the central server distributes the optimized injection coefficients Λ<sup>_∗_</sup> _g_<sup>obtainedinthecur-</sup> rent round to all participating clients. Upon receiving Λ<sup>_∗_</sup> _g_<sup>,</sup> each client applies it to their local LLM _M_ . When new inference queries arrive, the client’s LLM performs context injection according to Equation 5 using _vg_ and Λ<sup>_∗_</sup> _g_<sup>.Through</sup> this single linear injection operation, the raw LLM is transformed into a task-specific LLM tailored for specific scenarios, without requiring any local parameter fine-tuning or gradient computations. This design effectively decouples data utilization from model training, significantly reducing computational and communication overhead on the client side, while also addressing the issue of token length limitations in long context inputs. It thus provides a novel paradigm for distributed AI collaboration in resource-constrained environments. 

**Application Optimization:** We designed two types of databases to enhance task processing efficiency and resource utilization. The first type is a server database, such as MongoDB, which is utilized to store task-related information along with their corresponding calibration coefficients. The second type is a vector database, such as Elasticsearch, designed to store global context vectors. By establishing a task vector index, the similarity search process is significantly reduced compared to traditional Retrieval-Augmented Generation (RAG) systems.Specifically,upon receiving a new task request, the server first queries the task index to retrieve the associated task information and calibration coefficients. If the task has been previously cached, the server directly retrieves the calibrated coefficients and the corresponding context vector from the databases. Otherwise, the server collects sufficient data and performs an _n_ -epoch iterative training process to obtain a task-specific LLM. During this process, the server also updates the calibration coefficients and the global context vector, storing the newly generated data into the respective databases for efficient future retrieval. This caching mechanism effectively reduces redundant computation and significantly accelerates task response time, forming a closed-loop optimization system. 

## **Experiments** 

### **Experimental Setup** 

To comprehensively evaluate the effectiveness of our proposed IFed-ICL framework, we conduct rigorous experiments using two LLMs, LLaMA-3-8B and Qwen2.5-7B on three widely used text classification datasets: SUBJ (Pang and Lee 2004), Emotion (Chatterjee et al. 2019), and AG 

News (Chatterjee et al. 2019). Except for the zero-shot baseline, which is evaluated using only 500 test samples to assess the model’s inherent capabilities, all other experiments utilize 5,000 training samples and 500 test samples from each dataset. 

To simulate the commonly observed non-independent and identically distributed (Non-IID) nature of federated learning, we partition the training data across 10 clients using a Dirichlet distribution with a concentration parameter of _α_ = 0 _._ 5. We compare IFed-ICL against several representative baselines: 

**Zero-Shot** : serving as a reference for the model’s raw performance; 

**Local ICL** (Brown et al. 2020): which simulates a noncollaborative scenario where each client performs inference independently using local data; 

**FedAvg-LoRA** (Hu et al. 2022): a representative method of parameter-efficient fine-tuning (PEFT) in federated settings, where clients fine-tune LoRA weights that are aggregated via federated averaging on the server. 

Zero-shot performance serves as a baseline for evaluating the inherent task capabilities of LLMs without any taskspecific adaptation. To highlight the value of Federated ICL, we design comparative experiments built upon this baseline. In contrast to the traditional paradigm of federated learning in PEFT, which relies on exchanging model parameters, we introduce three comparative baselines to demonstrate the superiority of our proposed framework.All server-side computations are executed on a single NVIDIA A100 GPU. 

### **Experimental Design** 

IFed-ICL is designed to address key challenges in federated large language models related to performance, efficiency, and collaborative adaptation. We evaluate its effectiveness through the following aspects: 

**Performance Comparison:** We compare the task accuracy of IFed-ICL against several baselines, including ZeroShot, Local ICL, and a representative parameter-efficient federated fine-tuning method, FedAvg-LoRA. The core objective is to assess whether our training-free federated paradigm can achieve competitive or superior performance relative to computationally intensive fine-tuning approaches. 

**System Efficiency Evaluation:** This aspect focuses on the practical deployability of the framework. We quantitatively compare the communication overhead (in KB per round) and the total client-side computation time (in seconds) per federated round, demonstrating IFed-ICL’s suitability for deployment in resource-constrained environments. 

**Impact of Federated Aggregation on Injection Coefficient Performance:** This analysis evaluates the effectiveness of federated aggregation in producing a global injection coefficient from clients’ locally calibrated coefficients. Specifically, we compare the performance of the global coefficient obtained via aggregation with that of locally optimized coefficients used independently by each client. The goal is to quantitatively demonstrate that federated aggregation can effectively integrate diverse local knowledge, resulting in a superior injection coefficient that enhances both 

Table 1: Communication overhead of FedAvg-LoRA and IFed-ICL on the SUBJ dataset. 

|**Method**|**Direction**|**FedAvg-LoRA**|**IFed-ICL**|
|---|---|---|---|
|**Initialization**|Client_→_Server<br>Server_→_Client|0 KB<br>13357.78 KB|514 KB (context vector)<br>**515.8 KB**(context vector + calibration coeffcients)|
|**Training (per round)**|Client_↔_Server|13357.78 KB|**1.8 KB**(calibration coeffcients )|



model performance and generalization. 

Table 2: Performance comparison of Llama-3-8B and Qwen2.5-7B on the SUBJ, Emotion, and AG News datasets. Accuracy (acc) and F1-score are reported in percentage (%) 

|**Dataset**|**Method**|Llama|-3-8B|Qwen2|.5-7B|
|---|---|---|---|---|---|
|||acc (%)|f1 (%)|acc (%)|f1 (%)|
||Zero-Shot|62.60|62.48|62.60|62.48|
|SUBJ|Local ICL|70.00|66.90|70.80|67.90|
||FedAvg-LoRA|66.00|64.58|66.00|64.58|
||**IFed-ICL**|**91.20**|**90.67**|**81.20**|**80.66**|
||Zero-Shot|52.20|53.51|52.20|53.52|
|Ei|Local ICL|49.82|50.42|49.70|50.30|
|moton|FedAvg-LoRA|54.60|54.89|54.60|54.89|
||**IFed-ICL**|**67.40**|**65.85**|**60.80**|**59.32**|
||Zero-Shot|82.40|80.06|82.40|82.04|
|AG|Local ICL|75.00|74.70|74.90|74.70|
|News|FedAvg-LoRA|79.00|78.58|80.00|79.60|
||**IFed-ICL**|**91.60**|**89.57**|**90.60**|**90.53**|



Table 3: Running time (seconds) of Llama-3-8B and Qwen2.5-7B on SUBJ, Emotion, and AG News. 

|**Dataset**|**Method**|**Runnin**|**g time (s)**|
|---|---|---|---|
|||Llama-3-8B|Qwen2.5-7B|
||Zero-Shot|30.14|29.44|
|SUBJ|Local ICL|45.74|45.31|
||FedAvg-LoRA|27637.48|14945.92|
||**IFed-ICL**|**670.25**|**530.99**|
||Zero-Shot|28.92|57.74|
|Ei|Local ICL|40.82|84.19|
|moton|FedAvg-LoRA|28168.84|14043.47|
||**IFed-ICL**|**809.73**|**1298.17**|
||Zero-Shot|27.90|56.45|
|AG N|Local ICL|54.02|112.20|
|ews|FedAvg-LoRA|30046.70|13719.66|
||**IFed-ICL**|**973.62**|**867.55**|



### **Performance Comparison** 

As shown in Table 2, our proposed IFed-ICL significantly outperforms all baseline methods across all evaluated tasks. Notably, on AG News, FedAvg-LoRA underperforms even compared to Local ICL and Zero-Shot. This can be attributed to its reliance on client-specific fine-tuning using local data. Due to data heterogeneity, such local adaptation may lead to overfitting on certain clients, thus degrading the overall performance. In contrast, ICL and Zero-Shot approaches primarily leverage global knowledge and exhibit stronger generalization to the target task, making them more robust to data heterogeneity. By aggregating and injecting context vectors, our proposed method effectively mitigates the adverse effects of non-IID data, thereby achieving superior performance. 

### **Efficiency and Communication Evaluation** 

In terms of system efficiency, we compare the communication and clients computation overhead of IFed-ICL with the mainstream PEFT baseline FedAvg-LoRA. Communication overhead is defined as the total amount of data (in kilobytes, KB) each client uploads to the server per round. Clients computation overhead refers to the total time (in seconds) required to complete one local task per round. 

Tables 1 and 3 present the efficiency comparison between IFed-ICL and FedAvg-LoRA from the perspectives 

of communication and computation. In terms of communication, IFed-ICL exhibits a decisive advantage. As detailed in Table 1, during the core training phase, IFedICL requires only 1.8 KB of communication per round to transmit a lightweight injection coefficient, while FedAvgLoRA needs to exchange approximately 13.08 MB of LoRA weight matrices. Even accounting for the one-time transmission of context vectors during initialization (approximately 514 KB), our method remains highly efficient. 

From the perspective of computation, IFed-ICL further improves efficiency by restricting backpropagation to a minimal set of injection coefficients, thereby significantly reducing client-side complexity. As shown in Table 3, IFed-ICL achieves 20–30 times faster computation speeds on average, and up to 41.22 times in the best case compared to FedAvgLoRA. While IFed-ICL takes slightly longer than Zero-Shot and Local ICL. Moreover, IFed-ICL provides the dual benefits of privacy preservation and performance enhancement under a federated learning setting, unlike Zero-Shot and Local ICL, which are more suitable for standalone or trusted environments and are difficult to deploy in real-world federated scenarios. Thus, the computational cost of IFed-ICL can be considered a necessary and acceptable trade-off in the privacy–performance balance. 

The core innovation of IFed-ICL lies in exchanging only a small number of low-dimensional scalar coefficients, rather than full-scale model weights. This drastically reduces both communication and computation burdens. Such a property 


![](P043_images/P043.pdf-0007-00.png)


Figure 3: Analysis of the impact of injection coefficient optimization on performance. The figure illustrates how model performance evolves as the injection coefficient is optimized over successive communication rounds. 

not only alleviates deployment bottlenecks in bandwidthconstrained or high-latency environments, but also provides practical communication feasibility for large-scale applications on mobile, edge, and IoT devices in real-world federated settings. 

### **Impact of Federated Aggregation on Injection Coefficient Performance** 

To evaluate the effectiveness of forming a global injection coefficient through federated aggregation of locally calibrated coefficients, we compare the accuracy of the global coefficient on each client with that of locally optimized injection coefficients derived independently using only local data. For each round, we record the accuracy of all 10 clientspecific models, their average accuracy, and the accuracy of the global model. By quantifying the difference between the global model accuracy and the mean local model accuracy, and analyzing the distribution of individual local model performance, we assess the impact of federated aggregation on overall model performance and generalization. 

As illustrated in Figure 2, the federated aggregation mechanism in IFed-ICL substantially improves the performance of the global injection coefficient. Compared to the average accuracy of local models, the global model achieves notable improvements of approximately 10.71%, 26.05%, and 12.81% on the AG News, SUBJ, and Emotion datasets, respectively. Moreover, in most rounds, the global model outperforms the majority of individual local models. By integrating knowledge from heterogeneous clients, the aggregation process yields a superior global coefficient that 

significantly enhances model performance and generalization. This effect is particularly pronounced on the SUBJ dataset, which features highly non-uniform data distributions, thereby demonstrating the efficiency and robustness of the proposed framework in real-world federated learning scenarios. 

As illustrated in Figure 3, we analyze the performance trajectory and stability of the global injection coefficient as the number of federated rounds increases. The experimental results indicate a consistent improvement in model performance over successive rounds, suggesting that the iterative refinement of the global injection coefficient plays a pivotal role in enhancing the effectiveness of IFed-ICL through collaborative optimization. 

## **Conclusion** 

This paper proposes a Implicit Federated In-context Learning framework, which decomposes the federated process into two components: context vector aggregation and injection coefficient optimization. This enables lightweight task adaptation for LLMs. Specifically, each client is responsible for transforming the context into vector representations and calibrating the injection coefficients through multiround federated optimization based on local data. A onetime linear injection is then performed to achieve model adaptation. Unlike traditional approaches such as context concatenation or full model fine-tuning in federated settings, IFed-ICL decouples data from model training, significantly reducing both communication and computation costs. Experiments across multiple text classification tasks demon- 

strate the effectiveness of the proposed framework, offering a new paradigm for distributed intelligent collaboration on resource-constrained devices. 

## **References** 

Agarwal, R.; Singh, A.; Zhang, L.; Bohnet, B.; Rosias, L.; Chan, S.; Zhang, B.; Anand, A.; Abbas, Z.; Nova, A.; et al. 2024. Many-shot in-context learning. _Advances in Neural Information Processing Systems_ , 37: 76930–76966. 

Bertsch, A.; Ivgi, M.; Alon, U.; Berant, J.; Gormley, M. R.; and Neubig, G. 2024. In-Context Learning with Long-Context Models: An In-Depth Exploration. arXiv:2405.00200. 

Brown, T.; Mann, B.; Ryder, N.; Subbiah, M.; Kaplan, J. D.; Dhariwal, P.; Neelakantan, A.; Shyam, P.; Sastry, G.; Askell, A.; et al. 2020. Language models are few-shot learners. _Advances in neural information processing systems_ , 33: 1877– 1901. 

Cai, D.; Wu, Y.; Wang, S.; Lin, F. X.; and Xu, M. 2022. Fedadapter: Efficient federated learning for modern nlp. _arXiv preprint arXiv:2205.10162_ . 

Chatterjee, A.; Narahari, K. N.; Joshi, M.; and Agrawal, P. 2019. SemEval-2019 task 3: EmoContext contextual emotion detection in text. In _Proceedings of the 13th international workshop on semantic evaluation_ , 39–48. 

Che, T.; Liu, J.; Zhou, Y.; Ren, J.; Zhou, J.; Sheng, V. S.; Dai, H.; and Dou, D. 2023. Federated learning of large language models with parameter-efficient prompt tuning and adaptive optimization. _arXiv preprint arXiv:2310.15080_ . 

Chen, C.; Feng, X.; Zhou, J.; Yin, J.; and Zheng, X. 2023. Federated large language model: A position paper. _arXiv e-prints_ , arXiv–2307. 

Feng, X.; Feng, X.; Du, X.; Kan, M.-Y.; and Qin, B. 2024. Adapter-based selective knowledge distillation for federated multi-domain meeting summarization. _IEEE/ACM Transactions on Audio, Speech, and Language Processing_ . 

Hendel, R.; Geva, M.; and Globerson, A. 2023. Incontext learning creates task vectors. _arXiv preprint arXiv:2310.15916_ . 

Hu, E. J.; Shen, Y.; Wallis, P.; Allen-Zhu, Z.; Li, Y.; Wang, S.; Wang, L.; Chen, W.; et al. 2022. Lora: Low-rank adaptation of large language models. _ICLR_ , 1(2): 3. 

Hu, J.; Wang, D.; Wang, Z.; Pang, X.; Xu, H.; Ren, J.; and Ren, K. 2024. Federated Large Language Model: Solutions, Challenges and Future Directions. _IEEE Wireless Communications_ . 

Huang, B.; Mitra, C.; Karlinsky, L.; Arbelle, A.; Darrell, T.; and Herzig, R. 2024. Multimodal task vectors enable manyshot multimodal in-context learning. _Advances in Neural Information Processing Systems_ , 37: 22124–22153. 

Jones, N. 2024. The AI revolution is running out of data. What can researchers do? _Nature_ , 636(8042): 290–292. Kairouz, P.; McMahan, H. B.; Avent, B.; Bellet, A.; Bennis, M.; Bhagoji, A. N.; Bonawitz, K.; Charles, Z.; Cormode, G.; Cummings, R.; et al. 2021. Advances and open problems in federated learning. _Foundations and trends® in machine learning_ , 14(1–2): 1–210. 

Koneˇcn`y, J.; McMahan, H. B.; Yu, F. X.; Richt´arik, P.; Suresh, A. T.; and Bacon, D. 2016. Federated learning: Strategies for improving communication efficiency. _arXiv preprint arXiv:1610.05492_ . 

Li, Z.; Xu, Z.; Han, L.; Gao, Y.; Wen, S.; Liu, D.; Wang, H.; and Metaxas, D. N. 2024. Implicit In-context Learning. arXiv:2405.14660. 

Liu, X.; Ji, K.; Fu, Y.; Tam, W. L.; Du, Z.; Yang, Z.; and Tang, J. 2021. P-tuning v2: Prompt tuning can be comparable to fine-tuning universally across scales and tasks. _arXiv preprint arXiv:2110.07602_ . 

McMahan, B.; Moore, E.; Ramage, D.; Hampson, S.; and y Arcas, B. A. 2017. Communication-efficient learning of deep networks from decentralized data. In _Artificial intelligence and statistics_ , 1273–1282. PMLR. 

Pang, B.; and Lee, L. 2004. A Sentimental Education: Sentiment Analysis Using Subjectivity Summarization Based on Minimum Cuts. In _Proceedings of the 42nd Annual Meeting of the Association for Computational Linguistics (ACL-04)_ , 271–278. 

Peng, Z.; Fan, X.; Chen, Y.; Wang, Z.; Pan, S.; Wen, C.; Zhang, R.; and Wang, C. 2024. Fedpft: Federated proxy fine-tuning of foundation models. _arXiv preprint arXiv:2404.11536_ . 

Shu, Y.; Hu, W.; Ng, S.-K.; Low, B. K. H.; and Yu, F. R. 2024. Ferret: Federated full-parameter tuning at scale for large language models. _arXiv preprint arXiv:2409.06277_ . 

Villalobos, P.; Sevilla, J.; Heim, L.; Besiroglu, T.; Hobbhahn, M.; and Ho, A. 2022. Will we run out of data? an analysis of the limits of scaling datasets in machine learning. _arXiv preprint arXiv:2211.04325_ , 1. 

Von Oswald, J.; Niklasson, E.; Randazzo, E.; Sacramento, J.; Mordvintsev, A.; Zhmoginov, A.; and Vladymyrov, M. 2023. Transformers learn in-context by gradient descent. In _International Conference on Machine Learning_ , 35151– 35174. PMLR. 

Wang, R.; Wang, Z.; Huang, C.; Wang, R.; Yu, T.; Yao, L.; Lui, J.; and Zhou, D. 2025. Federated In-Context Learning: Iterative Refinement for Improved Answer Quality. _arXiv preprint arXiv:2506.07440_ . 

Wies, N.; Levine, Y.; and Shashua, A. 2023. The learnability of in-context learning. _Advances in Neural Information Processing Systems_ , 36: 36637–36651. 

Wu, F.; Li, Z.; Li, Y.; Ding, B.; and Gao, J. 2024a. Fedbiot: Llm local fine-tuning in federated learning without full model. In _Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining_ , 3345– 3355. 

Wu, P.; Li, K.; Nan, J.; and Wang, F. 2024b. Federated in-context llm agent learning. _arXiv preprint arXiv:2412.08054_ . 

Yan, Y.; Yang, Q.; Tang, S.; and Shi, Z. 2024. Federa: Efficient fine-tuning of language models in federated learning leveraging weight decomposition. _arXiv preprint arXiv:2404.18848_ . 

Yang, Q.; Liu, Y.; Chen, T.; and Tong, Y. 2019. Federated machine learning: Concept and applications. _ACM Transactions on Intelligent Systems and Technology (TIST)_ , 10(2): 1–19. 

Ye, J.; Wu, Z.; Feng, J.; Yu, T.; and Kong, L. 2023. Compositional exemplars for in-context learning. In _International Conference on Machine Learning_ , 39818–39833. PMLR. 

Ye, R.; Wang, W.; Chai, J.; Li, D.; Li, Z.; Xu, Y.; Du, Y.; Wang, Y.; and Chen, S. 2024. OpenFedLLM: Training Large Language Models on Decentralized Private Data via Federated Learning. arXiv:2402.06954. 

Zaken, E. B.; Ravfogel, S.; and Goldberg, Y. 2021. Bitfit: Simple parameter-efficient fine-tuning for transformerbased masked language-models. _arXiv preprint arXiv:2106.10199_ . 

Zhang, Y.; Qin, Z.; Wu, Z.; Hou, J.; and Deng, S. 2024a. Personalized Federated Fine-Tuning for LLMs via DataDriven Heterogeneous Model Architectures. _arXiv preprint arXiv:2411.19128_ . 

Zhang, Z.; Yang, Y.; Dai, Y.; Wang, Q.; Yu, Y.; Qu, L.; and Xu, Z. 2023. FedPETuning: When federated learning meets the parameter-efficient tuning methods of pre-trained language models. In _Annual Meeting of the Association of Computational Linguistics 2023_ , 9963–9977. Association for Computational Linguistics (ACL). 

Zhang, Z.; Zhang, J.; Huang, J.; Qu, L.; Zhang, H.; and Xu, Z. 2024b. FedPIT: Towards Privacy-preserving and Fewshot Federated Instruction Tuning. _CoRR_ , abs/2403.06131. 

