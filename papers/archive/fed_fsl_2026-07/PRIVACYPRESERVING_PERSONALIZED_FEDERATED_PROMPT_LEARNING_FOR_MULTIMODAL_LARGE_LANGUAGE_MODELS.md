Published as a conference paper at ICLR 2025 

# PRIVACY-PRESERVING PERSONALIZED FEDERATED PROMPT LEARNING FOR MULTIMODAL LARGE LANGUAGE MODELS 

|**Linh Tran**<sup>1</sup><br>**Wei Sun**<sup>2</sup>|**Stacy Patterson**<sup>1</sup>|**Ana Milanova**<sup>1</sup>|
|---|---|---|
|1Rensselaer Polytechnic Institute|2IBM Research||
||ABSTRACT||



Multimodal Large Language Models (LLMs) are pivotal in revolutionizing customer support and operations by integrating multiple modalities such as text, images, and audio. Federated Prompt Learning (FPL) is a recently proposed approach that combines pre-trained multimodal LLMs such as vision-language models with federated learning to create personalized, privacy-preserving AI systems. However, balancing the competing goals of personalization, generalization, and privacy remains a significant challenge. Over-personalization can lead to overfitting, reducing generalizability, while stringent privacy measures, such as differential privacy, can hinder both personalization and generalization. In this paper, we propose a Differentially Private Federated Prompt Learning (DP-FPL) approach to tackle this challenge by leveraging a low-rank factorization scheme to capture generalization while maintaining a residual term that preserves expressiveness for personalization. To ensure privacy, we introduce a novel method where we apply local differential privacy to the two low-rank components of the local prompt, and global differential privacy to the global prompt. Our approach mitigates the impact of privacy noise on the model performance while balancing the tradeoff between personalization and generalization. Extensive experiments demonstrate the effectiveness of our approach over other benchmarks. 

## 1 INTRODUCTION 

In recent years, there has been rapid advancement in multimodal large language models (LLMs) that integrate multiple modality information, including text, images, audio, and video, to enhance the comprehension and generation capabilities. Vision-Language Models (VLMs) such as CLIP (Radford et al., 2021) are a variant of multimodal LLMs that learn transferable image and text representations, making them highly effective in applications such as image captioning and visual search. One proposed setting for deploying VLMs is a Federated Learning framework that allows multiple organizations or clients to collaboratively train a global model without directly sharing their local training data. However, fine-tuning pre-trained VLMs in a FL system is time-consuming and resource-intensive given the massive number of parameters each VLM has. This gives rise to Federated Prompt Learning (FPL) which only fine-tunes the soft prompt embedding while freezing the rest of the VLM model parameters in the FL system (Guo et al., 2023b; Cui et al., 2024). In FPL, each client fine-tunes their customized prompt using their local data and shares the prompt with a central server for generalization purposes. The clients can distribute their fine-tuned prompts as prompt providers to public users who wish to perform downstream inference tasks, also known as the prompt as a service (PaaS) paradigm (Wu et al., 2024; Yao et al., 2024; Huang et al., 2023). 

One significant challenge in such distributed systems is the presence of data heterogeneity, i.e., organizations often have non-identical and non-independent (non-IID) data distributions, which can vary widely due to factors such as demographics, usage patterns, or device capabilities. To address this, personalized FL has emerged to tailor models to the unique data characteristics of each client rather than solely improving a global model. Personalized FL focuses on learning customized models for each client, reflecting the heterogeneity of their data (He et al., 2020; Dinh et al., 2020). In the context of personalized FPL, the goal is for each client to learn and utilize personalized prompts that 

1 

Published as a conference paper at ICLR 2025 

better align with their specific data and application needs. Nevertheless, over-personalization can lead to local data overfitting, preventing the model to generalize well on non-training data. Clients in an FPL framework may opt to distribute their customized prompts post training to public users for downstream tasks. However, these users may have different types of inputs that the client’s prompt is not well generalized to, resulting in suboptimal performance. Consequently, it is crucial to achieve a nuanced balance between personalization and generalization in a heterogeneous FPL system. 

In addition to balancing the tradeoff between personalization and generalization, privacy poses another critical concern in FPL, especially in sensitive domains such as finance, law, and healthcare. In the PaaS framework, the distributed trained prompts are shown to be susceptible to Membership Inference Attack (MIA), potentially exposing details about individual clients’ training data (Wu et al., 2024). To address this issue, one may consider Differential Privacy (DP) (Dwork et al., 2014) which ensures an adversary cannot reliably detect the presence or absence of a data sample based on the output information. However, balancing personalization and privacy under data heterogeneity is a challenging task. The non-IID nature of the data allows clients to better learn their personalized prompt, but it amplifies the performance degradation caused by DP due to the high data sensitivity, impairing both personalization and generalization capabilities. Thus, the key question we aim to address is: _How can we effectively balance personalization, generalization, and privacy in a data heterogeneous FPL system?_ 

To tackle the above question, we proposed a Differentially Private Federated Prompt Learning (DPFPL) approach that leverages low-rank factorization and DP as part of the prompt learning process. In our framework, each client simultaneously learns a global prompt and a local prompt. The global prompt is shared in a FL manner for generalized knowledge transfer, while the local prompt is retained at each client site for personalization. Our contributions are threefold. 

- We propose a privacy-preserving personalized federated prompt learning approach with Differential Privacy for multimodal LLMs. We factorize the local prompt into two lower rank components with an additional residual term. The factorized low-rank components allow the model to capture broader patterns that are beneficial across different data distributions, aiding the generalization capability of each client. The residual term is crucial for retaining the expressiveness lost during the factorization process, thereby preserving the client-specific learning and improving personalization. 

- We preserve privacy by utilizing both Global Differential Privacy (GDP) and Local Differential Privacy (LDP). Unlike conventional methods that apply noise uniformly to the entire prompt, we judiciously apply LDP to the two low-rank components of the local prompt, and GDP to the global prompt. Our privacy mechanism mitigates the effect of DP noise on model performance while preserving the privacy guarantee post training. 

- We conduct extensive experiments on widely adopted datasets to evaluate our proposed method against other benchmarks. The experimental results demonstrate superior performance of our proposed method in balancing personalization and generalization while mitigating the model degradation caused by DP noise. 

## 2 RELATED WORK 

**Personalized Federated Learning.** There are several existing approaches that aim to learn personalized models for clients in FL settings, including clustering (Ghosh et al., 2020; Berlo et al., 2020; Shahid et al., 2021), regularization (Shoham et al., 2019; Dinh et al., 2020; Li et al., 2020) and knowledge distillation (Li & Wang, 2019; He et al., 2020; Fang & Ye, 2022). Personalized FL is most commonly approached as a multi-task learning problem that simultaneously learns two models for each client: a global model for generalized knowledge and a local model for personalized data. Existing methods accomplish this by decoupling the model parameters or layers into global and local learning components (Arivazhagan et al., 2019; Deng et al., 2020; Zhang et al., 2020; Collins et al., 2021; Jeong & Hwang, 2022; Zhang et al., 2023). In the existing literature on personalized FL, private multi-task learning approaches aim to protect training data by retaining personalized parameters and sharing differentially private generalized parameters. Examples include Jain et al. (2021), Hu et al. (2021), Bietti et al. (2022), Yang et al. (2023b) and Xu et al. (2024). However, these methods are designed for full model training and cannot be directly applied to prompt tuning due to the difference in the parameter space. Sun et al. (2024) incorporates Low-Rank Adaptation with DP 

2 

Published as a conference paper at ICLR 2025 

in a standard FL setting, but they do not consider personalization and prompt learning, making their method not applicable to our setting. 

**Federated Prompt Learning.** Recent advances in personalized FPL have garnered significant attention (Guo et al., 2023a;b; Li et al., 2023; Yang et al., 2023a; Sun et al., 2023; Deng et al., 2024; Li et al., 2024; Cui et al., 2024). See Table 1 for comparisons. With the exception of Zhao et al. (2023) which introduces a privacy-preserving FPL method that leverages DP to protect the underlying private data, none of the prior literature considers the privacy issue. Many of these works require modification to the backbone model, which is not relevant to our approach as we want to protect the personalized prompt, not the model. Zhao et al. (2023) does not account for the crucial aspects of personalization. Similar to our work, Cui et al. (2024) also factorizes the local prompt into two learnable low-rank components for balancing personalization and generalization. We instead have the learnable full-rank local prompt, and only keep the low-rank terms non-permanent for generalization with an additional residual to retain the expressiveness for personalization. 

Table 1: Recent Federated Prompt Learning algorithms 

|FPL Algorithm|Consider<br>personalization|No model<br>modifcation|Adopt low-rank<br>factorization|Provide privacy<br>guarantee|
|---|---|---|---|---|
|pFedPrompt (Guo et al., 2023a)|✓|✗|✗|✗|
|PromptFL(Guo et al., 2023b)|✓|✓|✗|✗|
|pFedPT (Li et al., 2023)|✓|✗|✗|✗|
|pFedPG (Yang et al., 2023a)|✓|✗|✗|✗|
|Fedperfx (Sun et al., 2023)|✓|✗|✗|✗|
|SGPT (Deng et al., 2024)|✓|✗|✗|✗|
|FedOTP (Li et al., 2024)|✓|✓|✗|✗|
|FedPGP (Cui et al., 2024)|✓|✓|✓|✗|
|Fedprompt(Zhao et al.,2023)|✗|✓|✗|✓|
|DP-FPL(ours)|✓|✓|✓|✓|



## 3 PROPOSED METHOD 

We introduce our proposed method, Differentially Private Federated Prompt Learning (DP-FPL), shown in Figure 1. Our approach leverages low-rank factorization with an additional residual term to balance personalization and generalization in a differentially private FPL system. 

### 3.1 PRELIMINARIES ON PERSONALIZED FEDERATED PROMPT LEARNING 

Our system follows a standard FPL setting that consists of a set of _N_ clients and a central server. Let the global dataset be _D_ = [ _D_ 1 _, D_ 2 _, . . . , DN_ ], each client _i_ holds a local subset _Di_ of _ni_ samples. Each client local model involves a frozen pre-trained VLM such as a CLIP model and a prompt learner, and their goal is to learn the representation between the visual and prompt information to improve multimodal classification tasks. Specifically, the frozen CLIP model involves a text encoder _f_ ( _·_ ) and an image encoder _g_ ( _·_ ) that respectively transform the prompt and an image _x_ into text and image features. The prompt learner trains a soft prompt _pi_ for client _i_ that is optimized to align with the visual features. Using cos[ _·, ·_ ] to denote the cosine similarity used by CLIP model, the classification prediction probability for each client _i_ is computed as: 


![](P066_images/P066.pdf-0003-09.png)


where ˆ _y_ denotes the predicted label, _cj_ denotes label _j_ out of _C_ number of classes, and _τ_ denotes the temperature parameter of CLIP. The client personalized prompt _pi_ is optimized with cross-entropy loss: 


![](P066_images/P066.pdf-0003-11.png)


3 

Published as a conference paper at ICLR 2025 


![](P066_images/P066.pdf-0004-01.png)


Figure 1: Architecture of DP-FPL with frozen CLIP models. Each client _i_ trains global prompt _pG,i_ and local prompt _pL,i_ . The local prompt is factorized at each training iteration as _pL,i_ = _uivi_ + _ri_ . 

In a data heterogeneity setting, each client’s local dataset _Di_ is drawn from a distinct data distributions. The difference among clients’ data can lead to the drift problem, where the local model converges toward local solutions optimal for their specific data but fails to align with the global model objective. To address this challenge, various personalized FPL solutions such as clustering, local fine-tuning and knowledge distillation have been proposed. Our work focuses on the multi-task learning approach that aims to learn two models for each client: one for generalization and one for personalization. In particular, we separate each client’s prompt _pi_ into a global prompt _pG,i_ and the local prompt _pL,i_ . The global prompt _pG,i_ is shared and aggregated to improve the global learning, while the local prompt _pL,i_ is retained at the client level for personalized learning. 

A simple example of the personalized prompt is illustrated in Figure 1, in which each client has a collection of images captured from different angles, reflecting the heterogeneity in their local data. Consequently, client 1 might use the prompt ”an upside-down photo of [class]”, while client _i_ could have the prompt ”a upright photo of [class]”, and client _N_ might use ”a rotated photo of [class]”. In this instance, the template ”a photo of [class]” is the generalized global prompt shared across clients, and the terms ”upside-down”, ”upright” and ”rotated” represent the personalized characteristics of each client’s prompt. These variations in prompts allow the client model to better adapt to the specific characteristics of their data, improving personalization. 

The training process of FPL over _T_ iterations is structured as follow. For each global training round _t_ , each client _i_ initializes the global prompt _p_<sup>_t_</sup> _G,i_<sup>_←pt_</sup> _G_<sup>_−_1</sup> and the local prompt _p_<sup>_t_</sup> _L,i_<sup>_←pt_</sup> _L,i_<sup>_−_1.</sup> Client _i_ then trains their personalized prompt _pi_ using their local private data and obtains the cross-entropy loss _L_ . At the end of the local training round, client _i_ updates their local prompt _p_<sup>_t_</sup> _L,i_<sup>_←pt_</sup> _L,i_<sup>_−ηL,i∇L,iL_andsendsthegradientw.r.ttheglobalprompt</sup><sup>_∇G,iL_totheserverfor</sup> _N_ aggregation. The server computes the average gradient _∇G ← N_<sup><u>1</u></sup> � _i_ =1<sup>_∇G,iL_and updates the new</sup> global prompt to be _p_<sup>_t_</sup> _G_<sup>_←pt_</sup> _G_<sup>_−_1</sup> _− ηG∇G_ . The learning objective function of FPL system is: 


![](P066_images/P066.pdf-0004-06.png)


where _LDi_ is the loss computed on dataset _Di_ of client _i_ . 

4 

Published as a conference paper at ICLR 2025 

### 3.2 BALANCING PERSONALIZATION AND GENERALIZATION 

Prior research has demonstrated that fine tuning pre-trained LLMs with lower dimension reparameterization promotes generalization capability across various tasks (Aghajanyan et al., 2020; Cui et al., 2024). Additionally, lower intrinsic dimension improves the model utility under the effect of DP noise (Yu et al., 2021; Xu et al., 2024). Therefore, we utilize low-rank factorization as part of our FPL framework to balance the personalization and generalization learning under the influence of DP noise. However, low-rank training such as Low-Rank Adaptation has difficulty matching the performance of full-rank training in many difficult tasks (Liu et al., 2024; Biderman et al., 2024; Ivison et al., 2023; Zhuo et al., 2024). This is because low-rank factorization methods restrict the parameter space, removing some of the information of the full-rank space (Koneˇcn`y, 2016). Recent work Cui et al. (2024) also used the low-rank approximation in non-private FPL systems, however, they factorize the local prompt only once at the beginning and train iteratively with the low-rank components. This approach can reduce the overall expressive power over the training phase. As we will show in Section 4, the loss of expressiveness can amplify the adverse effects of the DP noise, further diminishing the model’s performance. 

To overcome these issues of low-rank training, we perform the factorization process in every training round rather than only at the beginning like Cui et al. (2024), and we incorporate a residual term to compensate for the lost expressiveness. We analyze in detail the benefit of the residual term in Section 3.3. The overall personalized prompt of client _i_ can then be expressed as _pi_ = _pG,i_ + _uivi_ + _ri_ , where _ui_ and _vi_ are the factorized low-rank components and _ri_ is the additional residual term. 

We utilize a version of the Reparametrized Gradient Perturbation (RGP) method introduced in Yu et al. (2021) as our low-rank factorization scheme. We perform the factorization process for each client local prompt _pL,i_ in every training iteration to get the temporary low-rank prompt components _ui_ and _vi_ . We also compute a residual term _ri_ which is the remainder of the factorization process, i.e. _ri_ = _pL,i − uivi_ . As shown by Yu et al. (2021), each client can reconstruct the gradient of _pL,i_ using the gradient of the low-rank terms in back propagation as follows: 


![](P066_images/P066.pdf-0005-05.png)

### Figure analysis

The figure presents Equation (4), used to recover the gradient with respect to the client-specific local prompt from gradients of its low-rank factorization components.

Readable transcription:

\[
\nabla_{L,i}\mathcal{L} = (\nabla_u \mathcal{L})v_i + u_i(\nabla_v \mathcal{L}) - u_i u_i^T(\nabla_u \mathcal{L})v_i
\tag{4}
\]

Important components:
- \(\nabla_{L,i}\mathcal{L}\): gradient of the loss with respect to client \(i\)'s local prompt.
- \(u_i\) and \(v_i\): low-rank factorized prompt components for client \(i\).
- \(\nabla_u\mathcal{L}\) and \(\nabla_v\mathcal{L}\): gradients with respect to the low-rank factors.
- The final subtractive term \(u_i u_i^T(\nabla_u\mathcal{L})v_i\) adjusts the reconstructed gradient, consistent with the reparametrized gradient perturbation formulation.

Direct observation: the equation combines two additive gradient contributions from the low-rank factors and one projection-like correction term. Interpretation: this allows the method to train using temporary low-rank prompt factors while reconstructing an update direction for the full local prompt, helping avoid the expressiveness loss of fixed low-rank training.

Connection to the surrounding text: the paper introduces per-round factorization of each client local prompt \(p_{L,i}\) into \(u_i v_i\) plus a residual \(r_i = p_{L,i} - u_i v_i\). This equation explains the gradient recomputation step used in that procedure. The surrounding discussion also clarifies that the residual term participates in the forward pass but is not involved in this full-rank local prompt gradient recomputation.


We note that the residual _ri_ is used as part of the forward process, but it is not involved in the full-rank local prompt recomputation. 

### 3.3 PRESERVING PRIVACY 

In the personalized FPL framework, each client as a prompt provider may distribute the trained customized prompt to public users for downstream inference tasks. These fully trained prompts, if not properly protected with privacy mechanism, are vulnerable to MIA which aims to infer if an image sample was used for training or not (Wu et al., 2024). Moreover, the shared global prompt may leak information about the private data during the training process as it contains the gradient information of the loss function. 

We assume that clients and server are honest. We consider adversary to be potential user with access to a trained customized prompt obtained from a FPL client. The adversary also has access to the publicly available pre-trained CLIP model for downstream inference purposes. The goal of the adversary is to infer whether an image data was part of the target FPL client’s training data utilizing the MIA. In this setting, the target client’s trained prompt _pi_ is shared with a potential adversarial user and is susceptible to privacy breach, so it is necessary to protect _pi_ with the DP mechanism. 

One may straightforwardly apply privacy noise to the client’s trained _pi_ before distributing it to public users. However, this requires a large DP noise to effectively prevent MIA (Wu et al., 2024). On the other hand, injecting noise gradually over the training phase allows for more control over the influence of noise on the model, leading to better utility (Abadi et al., 2016). In our setting, we perform gradient updates on the global prompt _pG,i_ and local prompt _pL,i_ of each client, so we add DP noise to the gradients w.r.t these two terms in each training step. 

As part of the FPL procedure, the global prompt of each client _pG,i_ is aggregated and averaged by the server, while the client’s local prompt _pL,i_ stays locally. The final trained prompt _pi_ is composed of the synchronized global prompt _pG_ and the local prompt _pL,i_ . To provide privacy guarantee, we use Global Differential Privacy (GDP) for the global prompt and Local Differential Privacy (LDP) 

5 

Published as a conference paper at ICLR 2025 

for the local prompt. This is an unconventional way of introducing DP noise to selective parts of the prompt, unlike a vanilla method that directly adds noise to the whole prompt before publishing it. We define these two DP notions as follow. 

**Definition 3.1. Global Differential Privacy (GDP)** A randomized mechanism _M_ : _D →R_ with domain _D_ and range _R_ satisfies ( _ϵ, δ_ )-GDP if for any two adjacent datasets _D, D_<sup>_′_</sup> _∈D_ (i.e., datasets that differ in exactly one sample) and for any subset of outputs _S ∈R_ it holds that 


![](P066_images/P066.pdf-0006-03.png)


**Definition 3.2. Local Differential Privacy (LDP)** A randomized mechanism _M_ : _D →R_ with domain _D_ and range _R_ satisfies ( _ϵ, δ_ )-LDP if for any two adjacent samples _x, x_<sup>_′_</sup> _∈ D_ where _D ∈D_ and for any subset of outputs _S ∈R_ it holds that 


![](P066_images/P066.pdf-0006-05.png)


We apply GDP to the global prompt _pG,i_ at the server because the impact of the GDP noise on the model utility is much smaller compared to LDP (Arachchige et al., 2019). To provide privacy guarantee for the local prompt _pL,i_ which is not shared with the server for aggregation, each client needs to obfuscate _pL,i_ locally with LDP noise. However, directly applying LDP noise to the full-rank local prompt _pL,i_ can heavily impair the model performance (Yu et al., 2021; Xu et al., 2024). In addition, the local prompt information is predominantly captured within the low-rank components as a result of the factorization process. Therefore, we inject LDP noise only to the low-rank component _ui_ and _vi_ to mitigate the negative effect of privacy noise, while still effectively protecting the local prompt during the recomputation process. We note that we do not add noise to the residual component _ri_ because it is not used for the local prompt recomputation. 

We achieve GDP and LDP using the Gaussian noise mechanism. Given a function _f_ : _D →R_ , the Gaussian noise mechanism _M_ is defined as 


![](P066_images/P066.pdf-0006-08.png)

### Figure analysis

The page contains three separate mathematical equation fragments that support the paper’s description of differential privacy for federated prompt learning.

1. **Global Differential Privacy (GDP) definition**

   The first equation states the standard \((\epsilon, \delta)\)-GDP condition for adjacent datasets \(D\) and \(D'\):

   \[
   \Pr[\mathcal{M}(D) \in S] \le e^{\epsilon}\Pr[\mathcal{M}(D') \in S] + \delta
   \]

   **Direct observation:** The mechanism \(\mathcal{M}\) maps datasets to outputs, and the inequality bounds how much the output distribution can change when one sample differs between datasets.

   **Interpretation in context:** This definition is used for the global prompt component \(p_{G,i}\), which is aggregated by the server. The surrounding text argues that applying GDP to the shared global prompt has less utility cost than applying local privacy noise everywhere.

2. **Local Differential Privacy (LDP) definition**

   The second equation gives the corresponding \((\epsilon, \delta)\)-LDP condition for adjacent individual samples \(x\) and \(x'\):

   \[
   \Pr[\mathcal{M}(x) \in S] \le e^{\epsilon}\Pr[\mathcal{M}(x') \in S] + \delta
   \]

   **Direct observation:** This equation mirrors the GDP bound but applies at the sample level rather than the dataset level.

   **Interpretation in context:** The paper applies LDP to the client-local prompt component \(p_{L,i}\). More specifically, the surrounding text says LDP noise is injected only into the low-rank components \(u_i\) and \(v_i\), rather than the full-rank local prompt, to reduce the negative impact on model utility. The residual component \(r_i\) is not noised because it is not used for local prompt recomputation.

3. **Gaussian noise mechanism**

   The third equation defines the Gaussian mechanism, numbered as Equation (5):

   \[
   \mathcal{M}(d) \triangleq f(d) + \mathcal{N}(0, \sigma^2)
   \]

   **Direct observation:** The mechanism adds zero-mean Gaussian noise with variance \(\sigma^2\) to the output of a function \(f(d)\).

   **Interpretation in context:** This equation operationalizes both GDP and LDP in the method. The surrounding text explains that the standard deviation \(\sigma\) is selected according to the sensitivity \(S_f\) of the function to satisfy the desired \((\epsilon, \delta)\)-DP guarantee. Later algorithm text connects this mechanism to gradient perturbation for the global prompt and low-rank local prompt components.

Overall, these equations establish the privacy formalism used by the proposed method: GDP protects the server-aggregated global prompt, LDP protects client-local low-rank prompt factors, and Gaussian noise provides the concrete perturbation mechanism.


where _N_ (0 _, σ_<sup>2</sup> ) is the normal distribution with mean 0 and variance _σ_<sup>2</sup> . The standard deviation _σ_ is typically chosen based on the function _f_ ’s sensitivity _Sf_ to satisfy an ( _ϵ, δ_ )-DP guarantee. 

The two main building blocks in our approach, i.e., low-rank factorization and DP, naturally introduce error to the training process. We conjecture that this error acts as a regularization term that prevents clients from overfitting to local data, reducing personalization and improving generalization. However, under strictly private conditions (lower rank and higher DP noise), the accumulated error may become too large and potentially destroy the personalization capability. In this case, the added residual term compensates for the regularization-like error and helps improve local learning, balancing personalization and generalization. We demonstrate the benefit of the residual term in the ablation study in Section 4.3, supporting our hypothesis. Further theoretical analysis of the residual term can be a potential future work direction. 

### 3.4 ALGORITHM 

We are now ready to describe our proposed method in detail, as shown in Algorithm 1. 

At the initial stage, the server randomizes a starting global prompt _p_<sup>0</sup> _G_<sup>andeachclient</sup><sup>_i_setsup</sup> their starting local prompt _p_<sup>0</sup> _L,i_<sup>(line1).Thevariances</sup><sup>_σG_and</sup><sup>_σL_arechosentosatisfyacertain</sup> ( _ϵ, δ_ )-LDP and ( _ϵ, δ_ )-GDP guarantee. The algorithm runs for _T_ iterations. In each iteration _t_ , each client updates _p_<sup>_t_</sup> _G,i_<sup>to be the previously aggregated</sup><sup>_pt_</sup> _G_<sup>_−_1</sup> and _p_<sup>_t_</sup> _L,i_<sup>to be the previous</sup><sup>_pt_</sup> _L,i_<sup>_−_1(line 4).A</sup> minibatch _B_<sup>_t_</sup> is sampled from the local dataset _Di_ for training (line 5). 

Each client performs parameter factorization using the power method with rank _k_ (line 6). Lines 7 _−_ 8 describe the forward pass where each client runs their local frozen CLIP model to get the text features and image feature, and uses them to calculate the loss _L_ using Equation 2. Each client then computes and clips the gradient w.r.t the two low-rank prompt components _∇uL_ and _∇vL_ with threshold _Cth_ and add local DP noise with standard deviation _σL_ according to 5 (lines 9 _−_ 10). 

The noisy gradient w.r.t the local prompt _∇_ ˜ _L,iL_ can be reconstructed from the noisy gradients _∇_<sup>˜</sup> _uL_ and _∇_<sup>˜</sup> _vL_ using equation 4, and then is updated accordingly (lines 11 _−_ 12). Each client also computes 

6 

Published as a conference paper at ICLR 2025 

### **Algorithm 1** DP-FPL 

1: **Initialize:** _p_<sup>0</sup> _G_<sup>,</sup><sup>_p_0</sup> _L,i_<sup>for</sup><sup>_i_= 1</sup><sup>_. . . N_, variances</sup><sup>_σL_and</sup><sup>_σG_</sup> 2: **for** _t ←_ 1 _. . . T_ **do** 3: **for** _i ←_ 1 _. . . N_ in parallel **do** 4: Initialize _p_<sup>_t_</sup> _G,i_<sup>_←pt_</sup> _G_<sup>_−_1</sup> and _p_<sup>_t_</sup> _L,i_<sup>_←pt_</sup> _L,i_<sup>_−_1.</sup> 5: Sample minibatch _B_<sup>_t_</sup> from _Di_ . 6: Compute low-rank components _ui, vi, ri ←_ **Factorize** ( _p_<sup>_t_</sup> _L,i_<sup>_, k_).</sup> 7: Obtain text features _f_ ( _p_<sup>_t_</sup> _G,i_<sup>),</sup><sup>_f_(</sup><sup>_uivi_+</sup><sup>_ri_) and image feature</sup><sup>_g_(</sup><sup>_x_) (</sup><sup>_x ∈Bt_).</sup> 8: Calculate loss _L_ according to Equation 2 and compute gradients _∇uL_ and _∇vL_ . 9: Clip gradients _∇G,iL_ , _∇uL_ and _∇vL_ with threshold _Cth_ . 11:10: Recompute noisy gradient w.r.tAdd local DP noise: _∇_<sup>˜</sup> _uL ←∇∇uL_ ˜ _L,i_ + _L N_ using(0 _, σ∇L_<sup>2˜)</sup> _u_<sup>and</sup> _L_ and _∇_<sup>˜</sup> _v∇L ←∇_<sup>˜</sup> _vL_ according to equation 4. _vL_ + _N_ (0 _, σL_<sup>2).</sup> 12: Update local prompt _p_<sup>_t_</sup> _L,i_<sup>_←pt_</sup> _L,i_<sup>_−ηL,i_</sup> _∇_<sup>˜</sup> _L,iL_ . 13: Send _∇G,iL_ to the server. 14: **end for** _N_ 15: Server computes average gradient _∇G ← N_<sup><u>1</u></sup> � _i_ =1<sup>_∇G,iL_.</sup> 16: Server adds global DP noise to _∇_<sup>˜</sup> _G ←∇G_ + _N_ (0 _, σG_<sup>2).</sup> 17: Server updates global prompt _p_<sup>_t_</sup> _G_<sup>_←pt_</sup> _G_<sup>_−_1</sup> _− ηG∇_<sup>˜</sup> _G_ . 18: **end for** 

the gradient w.r.t the global prompt _∇G,iL_ and sends it to the server for aggregation (line 13). Upon receiving the locally computed gradients, the server computes the average gradient and adds global DP noise with standard deviation _σG_ to perturb the gradient (lines 15 _−_ 16). The server then updates the new global prompt for the next training round (line 17). 

Low-rank factorization via traditional SVD method requires significant runtime. Instead, we use the power method with one iteration, significantly reducing the computational cost. Given the full-rank matrix of size _m × n_ (assuming _m ≤ n_ ), the computational cost of SVD scales with _O_ ( _m_<sup>2</sup> _n_ ), while the power iteration only scales with _O_ ( _kmn_ ) where _k_ is the reduced rank and _k ≪ m_ . 

### 3.5 PRIVACY ANALYSIS 

DP has several properties and compositions that make it easier to analyze the privacy budget in repetitive algorithms such as machine learning, where the privacy loss accumulates across multiple training iterations. When DP mechanisms are applied repeatedly to the same dataset, the overall privacy budget accumulates sequentially using the advanced composition theorem (Dwork et al., 2014). Conversely, when DP mechanisms are applied independently to disjoint subsets of a dataset, the overall privacy loss does not accumulate. In this case, the privacy guarantee remains bounded by the maximum privacy loss of any subset using parallel composition (Dwork et al., 2014). The privacy budget in term of LDP and GDP of Algorithm 1 is given by the following theorem. 

**Theorem 3.3.** _There exist constants c_ 1 _, c_ 2 _so that given the number of global rounds T , for any δ >_ 0 _, DP-FPL satisfies_ ( _ϵ, δ_ ) _-LDP and_ ( _ϵ, δ_ ) _-GDP if we choose σL and σG as following:_ 


![](P066_images/P066.pdf-0007-08.png)


_Proof_ By definition, a single application of the Gaussian noise mechanism satisfies ( _ϵ, δ_ )-DP if we _S_<sup>_<u>√</u>_</sup> 2 log(1 _._ 25 _<u>/δ</u>_ <u>)</u> choose _σ ≥ ϵ_ where _S_ is the sensitivity. Under the advanced composition theorem of DP, the Gaussian noise mechanism after _T_ training steps results in an accumulated privacy loss of ( _O_ ( _ϵ√T_ ) _, δ_ )-DP. Thus, to achieve ( _ϵ, δ_ )-DP, one would need to choose 


![](P066_images/P066.pdf-0007-10.png)


for the Gaussian noise mechanism where _c_<sup>_′_</sup> is a constant. 

7 

Published as a conference paper at ICLR 2025 

_SL_<sup>_<u>√</u>_</sup> _TL_ log(1 _<u>/δ</u>_ <u>)</u> Applying Equation 6, we can choose _σL ≥ c_ 1 _ϵ_ where _c_ 1 is a constant to make Algorithm 1 satisfy ( _ϵ, δ_ )-LDP with respect to each client. Since each client _i_ operates the Gaussian noise mechanism independently on disjoint local subset _Di_ of the global dataset _D_ , the release of all clients’ noisy mechanism output still satisfies ( _ϵ, δ_ )-LDP by the parallel composition of DP. Sim- 

_SG_<sup>_<u>√</u>_</sup> _T_ log(1 _<u>/δ</u>_ <u>)</u> ilarly, by choosing _σG ≥ c_ 2 _ϵ_ according to Equation 6, DP-FPL satisfies ( _ϵ, δ_ )-GDP. 

We proved in the theorem above that Algorithm 1 satisfies ( _ϵ, δ_ )-LDP and ( _ϵ, δ_ )-GDP when publishing the customized prompt to potential users. Since the GDP noise is added to the aggregated gradient, the distribution of the aggregated gradient to all clients also satisfies ( _ϵ, δ_ )-GDP by the post-processing property of DP. According to Theorem 3.3, we can calculate the standard deviations _σL_ and _σG_ to achieve a certain ( _ϵ, δ_ )-LDP and ( _ϵ, δ_ )-GDP. The pair _ϵ, δ_ can be chosen to match a desired MIA accuracy rate, preferably lower than random guess (50%) (Thudi et al., 2022). 

## 4 EXPERIMENTS 

### 4.1 SETUP 

**Datasets.** We select four visual classification datasets to investigate the task of balancing personalization, generalization and privacy: Caltech101 (Fei-Fei et al., 2004), OxfordPets (Parkhi et al., 2012), OxfordFlowers (Nilsback & Zisserman, 2008) and Food101 (Bossard et al., 2014). We utilize the pathological data split among 10 clients. Each client model is trained on its local classes, and evaluated on both its local classes for personalization capability and neighbor classes (classes owned by other clients) for generalization capability. We also evaluate the large-scale dataset CIFAR-100 (Krizhevsky et al., 2009) with the Dirichlet data split among 25 and 50 clients. The final test accuracy is obtained by averaging the performance across all clients. Details of our implementation and hyperparameters are provided in the appendix. 

Table 2: Mean test accuracy on local classes averaged across 10 clients. The baseline FedPGP and our method DP-FPL have factorization on the local prompt with rank 8. 

|Dataset|Noise_ϵ_|PromptFL|FedOTP|FedPGP|DP-FPL|
|---|---|---|---|---|---|
||None|94.45_±_0.30|**97.06**_±_**0.48**|95.21_±_0.19|96.06_±_0.18|
|Caltech|0_._4|82.53_±_0.52|95.09_±_0.50|95.12_±_0.46|**95.74**_±_**0.63**|
|101|0_._2|81.52_±_0.45|87.61_±_0.58|90.98_±_0.40|**95.28**_±_**0.46**|
||0_._1|80.42_±_0.65|84.98_±_0.39|80.01_±_0.39|**92.71**_±_**0.38**|
||0_._05|78.61_±_1.39|83.61_±_0.38|77.24_±_0.38|**87.64**_±_**0.79**|
||0_._01|78.52_±_1.68|78.86_±_0.38|77.23_±_0.37|**85.21**_±_**0.85**|
||None|76.85_±_0.96|**99.63**_±_**0.2**|94.66_±_0.31|96.91_±_0.76|
|Oxford|0_._4|74.36_±_0.26|80.03_±_0.93|86.56_±_0.69|**95.13**_±_**0.52**|
|Pets|0_._2|73.56_±_0.16|65.97_±_0.89|67.11_±_0.44|**93.09**_±_**0.43**|
||0_._1|72.77_±_0.16|59.54_±_0.58|63.21_±_0.62|**85.25**_±_**0.18**|
||0_._05|52.39_±_0.53|58.97_±_1.02|57.98_±_0.97|**81.26**_±_**1.10**|
||0_._01|43.68_±_0.67|54.08_±_1.04|45.49_±_1.33|**73.71**_±_**0.40**|
||None|84.04_±_0.32|**97.84**_±_**1.16**|79.11_±_0.45|85.75_±_0.62|
|Oxford|0_._4|60.31_±_1.28|79.89_±_0.80|77.13_±_0.52|**80.09**_±_**1.41**|
|Flowers|0_._2|40.33_±_0.83|65.96_±_0.96|70.77_±_0.61|**76.75**_±_**1.05**|
||0_._1|38.25_±_1.37|42.31_±_0.71|52.42_±_1.58|**72.11**_±_**1.37**|
||0_._05|37.18_±_0.92|38.89_±_0.66|39.52_±_0.77|**69.80**_±_**1.34**|
||0_._01|36.11_±_0.60|33.98_±_0.63|35.23_±_0.64|**51.55**_±_**1.07**|
||None|86.50_±_0.26|**86.65**_±_**0.23**|84.40_±_0.09|86.08_±_0.12|
|Food|0_._4|78.70_±_0.39|79.45_±_0.23|80.58_±_1.52|**81.45**_±_**0.21**|
|101|0_._2|71.84_±_0.91|77.36_±_0.41|77.72_±_1.50|**81.25**_±_**0.18**|
||0_._1|69.00_±_0.40|70.48_±_1.39|75.18_±_0.22|**80.57**_±_**0.46**|
||0_._05|68.36_±_1.23|62.98_±_1.25|73.72_±_1.04|**78.23**_±_**0.43**|
||0_._01|67.47_±_1.20|54.70_±_1.12|71.82_±_1.19|**77.45**_±_**0.40**|



**Baselines.** To demonstrate the effectiveness of our proposed method in balancing personalization, generalization and privacy, we compare with three baseline cases: (1) PromptFL (Guo et al., 2023b), (2) FedOTP (Li et al., 2024) and (3) FedPGP (Cui et al., 2024). More details of the baselines are listed in the appendix. 

**Privacy levels.** We consider different noise levels for LDP and GDP: _ϵ_ = _{_ 0 _._ 01 _,_ 0 _._ 05 _,_ 0 _._ 1 _,_ 0 _._ 2 _,_ 0 _._ 4 _}_ . We pick _δ_ = 10<sup>_−_5</sup> and the clipping threshold _Cth_ = 10. We provide details of how the noise is added to each baseline in the appendix. 

8 

Published as a conference paper at ICLR 2025 

### 4.2 PERFORMANCE RESULTS 

**Improving personalization in private setting.** Table 2 shows the average test accuracy over the last 10 epochs on local classes. In the non-private scenario (i.e., Noise = None), FedOTP shows the highest utility, however, as we add more noise, DP-FPL has the highest local classes accuracy. Under strict privacy levels ( _ϵ_ = 0 _._ 01), we see a noticeable decrease in test accuracy. Nevertheless, DP-FPL still consistently outperforms other baselines across all datasets, showing the robustness of our method even under strictly private conditions. Table 4 shows the overall accuracy utilizing a Dirichlet data split and ResNet50 as the backbone model. As shown in Table 4, DP-FPL demonstrates superior performance compared to baseline methods across all datasets. This shows the effectiveness and applicability of our approach in various complex settings, including different data distributions, models, and number of clients. 

**Privacy improves generalization.** Table 3 shows the average test accuracy over the last 10 epochs on neighbor classes. Similar to local classes, DP-FPL exhibits the highest utility in neighbor classes under the presence of DP noise. As expected, the accuracy degrade for higher noise levels, however, we see an improvement in Caltech101 utility when we increase privacy level from 0 _._ 4 to 0 _._ 1. This is because privacy noise act as a form of regularization that prevents overfitting, and hence improving generalization. Nevertheless, when the noise level is large enough ( _ϵ_ = _{_ 0 _._ 01 _,_ 0 _._ 05 _}_ ), the overall utility is degraded and the neighbor accuracy no longer improves. 

**Additional results.** We include additional experiment on the performance of MIA against DP-FPL in the appendix (see Section A.3). The results show that the attack success rate is relatively low when _ϵ_ = 0 _._ 1 for all datasets. In addition, _ϵ_ = 0 _._ 1 causes less than 10% reduction in the target model accuracy for both local and neighbor classes as shown in Tables 2 and 3. 

Table 3: Mean test accuracy on neighbor classes averaged across 10 clients. The baseline FedPGP and our method DP-FPL have factorization on the local prompt with rank 8. 

|Dataset|Noise_ϵ_|PromptFL|FedOTP|FedPGP|DP-FPL|
|---|---|---|---|---|---|
||None|92.88_±_0.19|74.91_±_0.30|**93.44**_±_**0.75**|91.54_±_0.15|
|Caltech|0_._4|82.66_±_1.22|84.26_±_0.84|88.24_±_0.78|**88.58**_±_**0.38**|
|101|0_._2|81.93_±_1.47|84.08_±_0.98|86.05_±_0.79|**89.72**_±_**0.98**|
||0_._1|80.83_±_0.72|78.91_±_1.02|79.31_±_0.82|**90.02**_±_**1.47**|
||0_._05|79.96_±_0.40|73.37_±_1.03|75.62_±_0.82|**82.76**_±_**1.12**|
||0_._01|78.89_±_0.33|73.54_±_1.00|75.60_±_0.82|**80.60**_±_**0.57**|
||None|76.34_±_0.37|65.63_±_0.14|**89.71**_±_**0.49**|80.19_±_0.85|
|Oxford|0_._4|74.43_±_0.87|60.95_±_0.81|72.54_±_0.54|**81.82**_±_**0.42**|
|Pets|0_._2|73.74_±_0.82|59.74_±_0.84|61.68_±_0.46|**80.67**_±_**0.28**|
||0_._1|73.12_±_0.39|58.83_±_0.93|59.79_±_0.79|**77.12**_±_**0.52**|
||0_._05|52.44_±_0.89|54.08_±_0.89|51.63_±_1.01|**74.13**_±_**0.48**|
||0_._01|38.27_±_0.86|53.63_±_0.91|40.20_±_0.42|**71.89**_±_**0.48**|
||None|69.44_±_0.61|38.29_±_1.09|**75.79**_±_**0.87**|69.51_±_0.45|
|Oxford|0_._4|48.03_±_0.69|56.65_±_0.77|65.93_±_0.86|**67.67**_±_**0.45**|
|Flowers|0_._2|38.19_±_0.97|55.44_±_0.90|63.49_±_0.65|**67.51**_±_**0.58**|
||0_._1|37.76_±_1.23|37.53_±_1.09|46.24_±_1.86|**66.44**_±_**1.51**|
||0_._05|38.78_±_1.18|33.48_±_1.00|35.27_±_1.28|**56.75**_±_**1.85**|
||0_._01|34.81_±_1.19|31.26_±_0.96|34.72_±_1.60|**43.21**_±_**1.72**|
||None|86.19_±_0.13|84.03_±_0.33|**86.23**_±_**0.06**|86.08_±_0.11|
|Food|0_._4|76.88_±_0.23|80.11_±_0.47|78.94_±_1.07|**81.00**_±_**0.25**|
|101|0_._2|70.99_±_0.83|76.44_±_0.62|77.21_±_0.90|**80.79**_±_**0.22**|
||0_._1|67.80_±_1.59|73.12_±_1.65|76.92_±_0.83|**78.14**_±_**0.53**|
||0_._05|66.76_±_1.27|71.82_±_0.79|73.61_±_1.35|**77.18**_±_**0.50**|
||0_._01|61.42_±_1.49|67.08_±_1.11|72.99_±_1.53|**76.87**_±_**0.62**|



### 4.3 ABLATION STUDY 

In this subsection, we investigate the efficacy of the key parameters that directly affect the tradeoff between personalization, generalization, and privacy: residual term, noise level _ϵ_ and rank value. The results for Caltech101 are presented in Figure 2; we include other dataset results in the appendix. 

**Effect of residual term.** We investigate the effectiveness of the residual term by separately testing the model without the residual component in Figure 2. We note that this setting is different from FedPGP because the factorization process is performed every training round instead of at the beginning. In Figure 2, we observe better performance in both local and neighbor classes when 

9 

Published as a conference paper at ICLR 2025 

Table 4: Mean test accuracy averaged across all clients under Dirichlet data distribution. The baseline FedPGP and our method DP-FPL have factorization on the local prompt with rank 8. 

|Noise||CIFAR-100 w|ith25clients|||CIFAR-100 w|ith50clients||
|---|---|---|---|---|---|---|---|---|
|_ϵ_|PromptFL|FedOTP|FedPGP|DP-FPL|PromptFL|FedOTP|FedPGP|DP-FPL|
|None|71.20_±_0.18|68.13_±_0.33|**71.54**_±_**0.17**|69.84_±_0.19|**71.30**_±_**0.10**|68.57_±_0.14|70.82_±_0.12|69.48_±_0.11|
|0_._4|53.69_±_0.53|47.22_±_0.97|58.87_±_0.35|**66.23**_±_**0.23**|55.44_±_0.31|58.23_±_0.42|58.43_±_0.51|**66.40**_±_**0.18**|
|0_._2|53.02_±_0.39|47.02_±_1.13|56.75_±_0.31|**62.92**_±_**0.30**|54.65_±_0.29|57.09_±_0.40|56.34_±_0.44|**64.39**_±_**0.29**|
|0_._1|50.86_±_0.68|46.95_±_1.06|55.76_±_0.33|**59.53**_±_**0.25**|53.17_±_1.06|57.05_±_0.22|53.39_±_0.48|**60.49**_±_**0.26**|
|0_._05|50.20_±_0.40|44.71_±_1.16|53.80_±_0.30|**57.97**_±_**0.16**|53.23_±_0.83|55.00_±_0.37|52.38_±_0.49|**58.35**_±_**0.30**|
|0_._01|50.65_±_0.41|44.27_±_1.17|51.75_±_0.34|**53.31**_±_**0.35**|51.92_±_1.56|54.53_±_0.29|52.32_±_0.46|**56.09**_±_**0.56**|



incorporating the residual term. The difference in accuracy is more prominent under strict privacy conditions (rank 1 and _ϵ_ = 0 _._ 01), confirming our conjecture about the benefit of the residual described in Section 3.3. Lower rank and higher noise significantly reduce the overall utility due to the large accumulated error, and the residual term plays a crucial role in improving local learning, balancing personalization and generalization. 


![](P066_images/P066.pdf-0010-04.png)


Figure 2: Test accuracy of ablation study on noise level, rank and residual term for Caltech101 

**Effect of privacy noise** _ϵ_ **.** We study how different privacy level affects the model performance on both local and neighbor classes in Figure 2 (b) and (c). As expected, the local classes accuracy gradually decreases when noise level increases. However, we see some unexpected improvement in neighbor utility when we increase DP parameter _ϵ_ from 0 _._ 4 to 0 _._ 1. As explained in Section 4.2, certain privacy noise range acts like regularization error that prevents overfitting, resulting in better generalization for higher noise level. 

**Effect of factorization rank.** We explore the impact of the factorization rank by comparing different rank values with full-rank setting in Figure 2 (b) and (c). Intuitively, higher rank values lead to better performance, however, this is not always the case. For local classes, rank 8 generally performs better than full-rank under higher noise levels ( _ϵ_ = _{_ 0 _._ 01 _,_ 0 _._ 1 _}_ ). Lower-rank has fewer entries, hence the amount of noise added is less than full-rank for the same level of privacy guarantee, which leads to better accuracy. For neighbor classes, lower rank value tends to have higher utility because lower rank introduces more regularization error that prevents overfitting and improves generalization. 

## 5 CONCLUSION 

In this paper, we presented a novel approach to address the critical challenges of personalization, generalization, and privacy in FPL for multimodal LLMs. Our proposed framework leverages lowrank factorization to balance the tradeoffs between these competing objectives. By factorizing the local prompts into low-rank components iteratively while incorporating a residual term, our method effectively preserves both generalization and personalization. Moreover, we introduced a privacypreserving mechanism that applies both global and local DP to safeguard sensitive client data. Unlike conventional methods, we selectively applied DP noise to the low-rank components, allowing us to maintain privacy without significantly degrading model performance. The critical role of the residual term in mitigating the effects of DP noise was also demonstrated, highlighting its importance for maintaining model expressiveness and personalization. 

10 

Published as a conference paper at ICLR 2025 

## ACKNOWLEDGMENTS 

This work was supported by the IBM through the IBM-Rensselaer Future of Computing Research Collaboration, and by the NSF grant CNS-2232061. 

## REFERENCES 

- Martin Abadi, Andy Chu, Ian Goodfellow, H. Brendan McMahan, Ilya Mironov, Kunal Talwar, and Li Zhang. Deep learning with differential privacy. In _Proceedings of the 2016 ACM SIGSAC Conference on Computer and Communications Security_ , CCS ’16, pp. 308–318. Association for Computing Machinery, 2016. 

- Armen Aghajanyan, Luke Zettlemoyer, and Sonal Gupta. Intrinsic dimensionality explains the effectiveness of language model fine-tuning. _arXiv preprint arXiv:2012.13255_ , 2020. 

- Pathum Chamikara Mahawaga Arachchige, Peter Bertok, Ibrahim Khalil, Dongxi Liu, Seyit Camtepe, and Mohammed Atiquzzaman. Local differential privacy for deep learning. _IEEE Internet of Things Journal_ , 7(7):5827–5842, 2019. 

- Manoj Ghuhan Arivazhagan, Vinay Aggarwal, Aaditya Kumar Singh, and Sunav Choudhary. Federated learning with personalization layers. _arXiv preprint arXiv:1912.00818_ , 2019. 

- Bram Berlo, Aaqib Saeed, and Tanir Ozcelebi. Towards federated unsupervised representation learning. In _Proceedings of the Third ACM International Workshop on Edge Systems, Analytics and Networking_ , EdgeSys ’20, pp. 31–36, New York, NY, USA, 2020. Association for Computing Machinery. 

- Dan Biderman, Jacob Portes, Jose Javier Gonzalez Ortiz, Mansheej Paul, Philip Greengard, Connor Jennings, Daniel King, Sam Havens, Vitaliy Chiley, Jonathan Frankle, et al. Lora learns less and forgets less. _arXiv preprint arXiv:2405.09673_ , 2024. 

- Alberto Bietti, Chen-Yu Wei, Miroslav Dudik, John Langford, and Steven Wu. Personalization improves privacy-accuracy tradeoffs in federated learning. In _International Conference on Machine Learning_ , pp. 1945–1962. PMLR, 2022. 

- Lukas Bossard, Matthieu Guillaumin, and Luc Van Gool. Food-101 – mining discriminative components with random forests. In _European Conference on Computer Vision_ , 2014. 

- Liam Collins, Hamed Hassani, Aryan Mokhtari, and Sanjay Shakkottai. Exploiting shared representations for personalized federated learning. In Marina Meila and Tong Zhang (eds.), _Proceedings of the 38th International Conference on Machine Learning_ , volume 139 of _Proceedings of Machine Learning Research_ , pp. 2089–2099. PMLR, 18–24 Jul 2021. 

- Tianyu Cui, Hongxia Li, Jingya Wang, and Ye Shi. Harmonizing generalization and personalization in federated prompt learning. In Ruslan Salakhutdinov, Zico Kolter, Katherine Heller, Adrian Weller, Nuria Oliver, Jonathan Scarlett, and Felix Berkenkamp (eds.), _Proceedings of the 41st International Conference on Machine Learning_ , volume 235 of _Proceedings of Machine Learning Research_ , pp. 9646–9661. PMLR, 21–27 Jul 2024. 

- Wenlong Deng, Christos Thrampoulidis, and Xiaoxiao Li. Unlocking the potential of prompt-tuning in bridging generalized and personalized federated learning. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pp. 6087–6097, 2024. 

- Yuyang Deng, Mohammad Mahdi Kamani, and Mehrdad Mahdavi. Adaptive personalized federated learning. _arXiv preprint arXiv:2003.13461_ , 2020. 

- Canh Dinh, Nguyen Tran, and Josh Nguyen. Personalized federated learning with moreau envelopes. In H. Larochelle, M. Ranzato, R. Hadsell, M.F. Balcan, and H. Lin (eds.), _Advances in Neural Information Processing Systems_ , volume 33, pp. 21394–21405. Curran Associates, Inc., 2020. 

- Alexey Dosovitskiy. An image is worth 16x16 words: Transformers for image recognition at scale. _arXiv preprint arXiv:2010.11929_ , 2020. 

11 

Published as a conference paper at ICLR 2025 

Cynthia Dwork, Aaron Roth, et al. The algorithmic foundations of differential privacy. _Foundations and Trends® in Theoretical Computer Science_ , 9(3–4):211–407, 2014. 

- Xiuwen Fang and Mang Ye. Robust federated learning with noisy and heterogeneous clients. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pp. 10072– 10081, 2022. 

- Li Fei-Fei, R. Fergus, and P. Perona. Learning generative visual models from few training examples: An incremental bayesian approach tested on 101 object categories. In _2004 Conference on Computer Vision and Pattern Recognition Workshop_ , pp. 178–178, 2004. 

- Avishek Ghosh, Jichan Chung, Dong Yin, and Kannan Ramchandran. An efficient framework for clustered federated learning. In H. Larochelle, M. Ranzato, R. Hadsell, M.F. Balcan, and H. Lin (eds.), _Advances in Neural Information Processing Systems_ , volume 33, pp. 19586–19597. Curran Associates, Inc., 2020. 

- Tao Guo, Song Guo, and Junxiao Wang. Pfedprompt: Learning personalized prompt for visionlanguage models in federated learning. In _Proceedings of the ACM Web Conference 2023_ , pp. 1364–1374, 2023a. 

- Tao Guo, Song Guo, Junxiao Wang, Xueyang Tang, and Wenchao Xu. Promptfl: Let federated participants cooperatively learn prompts instead of models-federated learning in age of foundation model. _IEEE Transactions on Mobile Computing_ , 2023b. 

- Chaoyang He, Murali Annavaram, and Salman Avestimehr. Group knowledge transfer: Federated learning of large cnns at the edge. In H. Larochelle, M. Ranzato, R. Hadsell, M.F. Balcan, and H. Lin (eds.), _Advances in Neural Information Processing Systems_ , volume 33, pp. 14068–14080. Curran Associates, Inc., 2020. 

- Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun. Deep residual learning for image recognition. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ , pp. 770–778, 2016. 

- Shengyuan Hu, Zhiwei Steven Wu, and Virginia Smith. Private multi-task learning: Formulation and applications to federated learning. _arXiv preprint arXiv:2108.12978_ , 2021. 

- Hai Huang, Zhengyu Zhao, Michael Backes, Yun Shen, and Yang Zhang. Prompt backdoors in visual prompt learning. _arXiv preprint arXiv:2310.07632_ , 2023. 

- Hamish Ivison, Yizhong Wang, Valentina Pyatkin, Nathan Lambert, Matthew Peters, Pradeep Dasigi, Joel Jang, David Wadden, Noah A Smith, Iz Beltagy, et al. Camels in a changing climate: Enhancing lm adaptation with tulu 2. _arXiv preprint arXiv:2311.10702_ , 2023. 

- Prateek Jain, John Rush, Adam Smith, Shuang Song, and Abhradeep Guha Thakurta. Differentially private model personalization. In M. Ranzato, A. Beygelzimer, Y. Dauphin, P.S. Liang, and J. Wortman Vaughan (eds.), _Advances in Neural Information Processing Systems_ , volume 34, pp. 29723–29735. Curran Associates, Inc., 2021. 

- Wonyong Jeong and Sung Ju Hwang. Factorized-fl: Personalized federated learning with parameter factorization &amp; similarity matching. In S. Koyejo, S. Mohamed, A. Agarwal, D. Belgrave, K. Cho, and A. Oh (eds.), _Advances in Neural Information Processing Systems_ , volume 35, pp. 35684–35695. Curran Associates, Inc., 2022. 

- Jakub Koneˇcn`y. Federated learning: Strategies for improving communication efficiency. _arXiv preprint arXiv:1610.05492_ , 2016. 

- Alex Krizhevsky, Geoffrey Hinton, et al. Learning multiple layers of features from tiny images. 2009. 

- Daliang Li and Junpu Wang. Fedmd: Heterogenous federated learning via model distillation. _arXiv preprint arXiv:1910.03581_ , 2019. 

- Guanghao Li, Wansen Wu, Yan Sun, Li Shen, Baoyuan Wu, and Dacheng Tao. Visual prompt based personalized federated learning. _arXiv preprint arXiv:2303.08678_ , 2023. 

12 

Published as a conference paper at ICLR 2025 

Hongxia Li, Wei Huang, Jingya Wang, and Ye Shi. Global and local prompts cooperation via optimal transport for federated learning. _arXiv preprint arXiv:2403.00041_ , 2024. 

- Tian Li, Anit Sahu, Manzil Zaheer, Maziar Sanjabi, Ameet Talwalkar, and Virginia Smith. Federated optimization in heterogeneous networks. In I. Dhillon, D. Papailiopoulos, and V. Sze (eds.), _Proceedings of Machine Learning and Systems_ , volume 2, pp. 429–450, 2020. 

Shih-Yang Liu, Chien-Yi Wang, Hongxu Yin, Pavlo Molchanov, Yu-Chiang Frank Wang, KwangTing Cheng, and Min-Hung Chen. Dora: Weight-decomposed low-rank adaptation. _arXiv preprint arXiv:2402.09353_ , 2024. 

- Maria-Elena Nilsback and Andrew Zisserman. Automated flower classification over a large number of classes. In _2008 Sixth Indian Conference on Computer Vision, Graphics and Image Processing_ , pp. 722–729, 2008. 

- Omkar M Parkhi, Andrea Vedaldi, Andrew Zisserman, and C. V. Jawahar. Cats and dogs. In _2012 IEEE Conference on Computer Vision and Pattern Recognition_ , pp. 3498–3505, 2012. 

- Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, et al. Learning transferable visual models from natural language supervision. In _International conference on machine learning_ , pp. 8748–8763. PMLR, 2021. 

- Osama Shahid, Seyedamin Pouriyeh, Reza M Parizi, Quan Z Sheng, Gautam Srivastava, and Liang Zhao. Communication efficiency in federated learning: Achievements and challenges. _arXiv preprint arXiv:2107.10996_ , 2021. 

- Neta Shoham, Tomer Avidor, Aviv Keren, Nadav Israel, Daniel Benditkis, Liron Mor-Yosef, and Itai Zeitak. Overcoming forgetting in federated learning on non-iid data. _arXiv preprint arXiv:1910.07796_ , 2019. 

- Reza Shokri, Marco Stronati, Congzheng Song, and Vitaly Shmatikov. Membership inference attacks against machine learning models. In _2017 IEEE symposium on security and privacy (SP)_ , pp. 3–18. IEEE, 2017. 

- Guangyu Sun, Matias Mendieta, Jun Luo, Shandong Wu, and Chen Chen. Fedperfix: Towards partial model personalization of vision transformers in federated learning. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pp. 4988–4998, 2023. 

- Youbang Sun, Zitao Li, Yaliang Li, and Bolin Ding. Improving lora in privacy-preserving federated learning. _arXiv preprint arXiv:2403.12313_ , 2024. 

- Anvith Thudi, Ilia Shumailov, Franziska Boenisch, and Nicolas Papernot. Bounding membership inference. _arXiv preprint arXiv:2202.12232_ , 2022. 

- Yixin Wu, Rui Wen, Michael Backes, Pascal Berrang, Mathias Humbert, Yun Shen, and Yang Zhang. Quantifying Privacy Risks of Prompts in Visual Prompt Learning. In _USENIX Security Symposium (USENIX Security)_ . USENIX, 2024. 

- Jie Xu, Karthikeyan Saravanan, Rogier van Dalen, Haaris Mehmood, David Tuckey, and Mete Ozay. Dp-dylora: Fine-tuning transformer-based models on-device under differentially private federated learning using dynamic low-rank adaptation. _arXiv preprint arXiv:2405.06368_ , 2024. 

- Fu-En Yang, Chien-Yi Wang, and Yu-Chiang Frank Wang. Efficient model personalization in federated learning via client-specific prompt generation. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pp. 19159–19168, 2023a. 

- Xiyuan Yang, Wenke Huang, and Mang Ye. Dynamic personalized federated learning with adaptive differential privacy. _Advances in Neural Information Processing Systems_ , 36:72181–72192, 2023b. 

- Hongwei Yao, Jian Lou, Zhan Qin, and Kui Ren. Promptcare: Prompt copyright protection by watermark injection and verification. In _2024 IEEE Symposium on Security and Privacy (SP)_ , pp. 845–861, 2024. 

13 

Published as a conference paper at ICLR 2025 

- Da Yu, Huishuai Zhang, Wei Chen, Jian Yin, and Tie-Yan Liu. Large scale private learning via lowrank reparametrization. In _International Conference on Machine Learning_ , pp. 12208–12218. PMLR, 2021. 

- Jianqing Zhang, Yang Hua, Hao Wang, Tao Song, Zhengui Xue, Ruhui Ma, and Haibing Guan. Fedcp: Separating feature information for personalized federated learning via conditional policy. In _Proceedings of the 29th ACM SIGKDD Conference on Knowledge Discovery and Data Mining_ , KDD ’23, pp. 3249–3261, New York, NY, USA, 2023. Association for Computing Machinery. 

- Michael Zhang, Karan Sapra, Sanja Fidler, Serena Yeung, and Jose M Alvarez. Personalized federated learning with first order model optimization. _arXiv preprint arXiv:2012.08565_ , 2020. 

- Haodong Zhao, Wei Du, Fangqi Li, Peixuan Li, and Gongshen Liu. Fedprompt: Communicationefficient and privacy-preserving prompt tuning in federated learning. In _ICASSP 2023-2023 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)_ , pp. 1–5. IEEE, 2023. 

- Terry Yue Zhuo, Armel Zebaze, Nitchakarn Suppattarachai, Leandro von Werra, Harm de Vries, Qian Liu, and Niklas Muennighoff. Astraios: Parameter-efficient instruction tuning code large language models. _arXiv preprint arXiv:2401.00788_ , 2024. 

## A EXPERIMENTAL DETAILS 

### A.1 DATASETS 

**Caltech101** (Fei-Fei et al., 2004) is an image dataset that contains images from 101 object categories (e.g., “helicopter”, “elephant” and “chair” etc.). There are about 40 to 800 images for each object category, but most categories have about 50 images. The dataset is available for download on http://www.vision.caltech.edu/Image_Datasets/Caltech101/101_ ObjectCategories.tar.gz. The dataset contains 6 _,_ 593 samples, including 4 _,_ 128 training samples and 2 _,_ 465 testing samples. 

**Oxford Pets** (Parkhi et al., 2012) is an image dataset with 37 object classes that can be downloaded at https://www.robots.ox.ac.uk/˜vgg/data/pets/data/images.tar.gz. The dataset consists of 6 _,_ 613 pet images with roughly 200 images for each class. The dataset is divided into training set of 2 _,_ 944 images and test set of 3 _,_ 669 images. 

**Oxford Flowers** (Nilsback & Zisserman, 2008) is an image classification dataset consisting of 102 flower categories, each class has between 40 and 258 images. The dataset is can be retrieved at https://www.robots.ox.ac.uk/˜vgg/data/flowers/102/102flowers.tgz. There are 6 _,_ 556 total images, including 4 _,_ 093 training images and 2 _,_ 463 testing images. 

**Food101** (Bossard et al., 2014) is a large-scale dataset containing images of 101 different types of food. The dataset is are available for download at https://data.vision.ee.ethz.ch/ cvl/datasets_extra/food-101/. There are 80 _,_ 800 total images, and we split the dataset into train set of size 50 _,_ 500 and test set of size 30 _,_ 300. 

**CIFAR-100** (Krizhevsky et al., 2009) is a another large-scale dataset containing images of 100 different object classes. The dataset is are available for download via torchvision.datasets.CIFAR10. The dataset consists of 60 _,_ 000 32x32 images, with 6 _,_ 000 images per class. We divide the dataset into training set of 50 _,_ 000 images and test set of 10 _,_ 000 images. 

### A.2 IMPLEMENTATION DETAILS 

For the first four datasets Caltech101, OxfordPets, OxfordFlowers and Food101, we use the Vision Transformer ViT-B16 (Dosovitskiy, 2020) as the backbone for the frozen CLIP model for Caltech101, OxfordPets, OxfordFlowers and Food101. For each dataset, we run experiments with _N_ = 10 clients for _T_ = 100 global training rounds. We use batch size _|B|_ = 32 for training and _|B|_ = 100 for testing. We set the global learning rate _ηG_ = 0 _._ 0001 and local learning rate _ηL_ = 0 _._ 0001 with SGD optimizer. 

14 

Published as a conference paper at ICLR 2025 

We adopt the Pathological setting for data heterogeneity among clients as implemented in https: //github.com/KaiyangZhou/CoOp/blob/main/DATASETS.md. The class labels are splitted randomly among 10 clients without overlapping, and each client owns disjoint set of local classes. For each client, we train the local model on data associated with their assigned local classes. We then evaluate each client’s local model on two test sets: local class test set for personalization and neighbor class test set for generalization. The local class test set involve all the test image associated with the client’s local class labels. The neighbor class test set is the set of all test images whose labels are owned by other clients. 

For CIFAR-100, we adopt ResNet50 (He et al., 2016) as the backbone model and run experiments with _N_ = 25 and _N_ = 50 clients for _T_ = 200 global training rounds. We use batch size _|B|_ = 32 for training and _|B|_ = 100 for testing. We set the global learning rate _ηG_ = 0 _._ 0001 and local learning rate _ηL_ = 0 _._ 0001 with SGD optimizer. We use Dirichlet data distribution to simulate the real-world non-IID setting with parameter _α_ = 0 _._ 3. The test accuracy is averaged across all clients. 

We provide a summary of the experiment set up in Table 5 below. 

Table 5: Details of datasets and experimental set up 

|Dataset|Data distribution|Model|Number<br>of clients|Number of<br>trainingrounds|Training<br>batch size|Testing<br>batch size|
|---|---|---|---|---|---|---|
|Caltech101|Pathological|ViT-B16|10|100|32|100|
|OxfordPets|Pathological|ViT-B16|10|100|32|100|
|OxfordFlowers|Pathological|ViT-B16|10|100|32|100|
|Food101|Pathological|ViT-B16|10|100|32|100|
|CIFAR-100|Dirichlet|ResNet50|25,50|200|32|100|



For the prompt learner, the length of prompt vectors is _b_ = 16 with a dimension of _d_ = 512, and the token position is “end” with “random” initialization. For the factorization process, we experiment with four different factorization rank 1 _,_ 2 _,_ 4 _,_ 8. We consider three different DP noises with privacy level from low to high: _ϵ ∈{_ 0 _._ 4 _,_ 0 _._ 2 _,_ 0 _._ 1 _}_ . The clipping threshold is chosen to be _Cth_ = 10 for both GDP and LDP applications. 

For the baseline methods, we consider three settings: PromptFL (Guo et al., 2023b), FedOTP (Li et al., 2024) and FedPGP (Cui et al., 2024) with the main difference lies in the prompt learner structure. We describe each baseline in detail below. 

1. **PromptFL:** PromptFL follows the traditional federated learning framework where each client has one single prompt _pi_ and the aggregated prompt is the average of all clients’ _pi_ . In this setting, the privacy noise is added directly to each client’s _pi_ before sharing with the server for aggregation. 

2. **FedOTP:** In FedOTP, each client’s customized prompt _pi_ involves two full-rank global prompt _pG,i_ and local prompt _pL,i_ . To incorporate privacy, the GDP noise is added to the averaged _pG_ by the server and the LDP noise is added to each client’s local prompt _pL,i_ . 

3. **FedPGP:** In FedPGP, each client’s customized prompt _pi_ includes a full-rank global prompt _pG,i_ and two low-rank local components _ui, vi_ . Each client then train three parameters _pG,i_ , _ui_ and _vi_ across the training process. In this baseline, the GDP noise is added to the averaged _pG_ by the server and the LDP noise is added to the two low-rank terms _ui, vi_ of each client. 

We run our experiment on a computer cluster, each node has a 6x NVIDIA Tesla V100 GPUs with 32 GiB of memory and 512 GiB RAM and 2x IBM Power 9 processors. The final result is the mean accuracy across all clients, averaged over 5 runs with different seeds. 

### A.3 MEMBERSHIP INFERENCE ATTACK 

In this section, we evaluate the privacy-preserving performance of our method DP-FPL against Membership Inference Attack (MIA). We implement MIA as described in Shokri et al. (2017), where the goal of the attack is to infer the appearance of data samples in one client’s training dataset. We 

15 

Published as a conference paper at ICLR 2025 

first train a set of 50 shadow models with the same model architecture as the target client’s model. The shadow models generate synthetic training data that is used to train the attack model. The attack model is a two-layer MLP and a classification head that predicts if a given sample is part of the target client’s training data or not. We run the attack on Caltech101, Oxford Pets and Oxford Flowers with different privacy levels. For each dataset, we perform separate attack on each class and compute the average success rate, i.e. percentage of correct guesses. 


![](P066_images/P066.pdf-0016-02.png)



![](P066_images/P066.pdf-0016-03.png)



![](P066_images/P066.pdf-0016-04.png)


Figure 3: Target model performance (a, b) and MIA performance (c) with rank 8. The baseline of MIA accuracy is set to 50% (random guessing). 

Figure 3 demonstrates the performance of the target model (local and neighbor classes) and the MIA. We set the MIA baseline accuracy to be 50%, representing the expected success rate of random guessing. Looking at Figure 3c, the MIA accuracy is low ( _<_ 50%) when _ϵ_ = 0 _._ 2 for Oxford Pets and _ϵ_ = 0 _._ 1 for Caltech101 and Oxford Flowers. In addition, _ϵ_ = 0 _._ 1 causes minimal loss in the target model accuracy for both local and neighbor classes (Figures 3a and 3b). Therefore, one can balance the utility-privacy tradeoff by setting _ϵ_ = 0 _._ 1 for any dataset. This shows that our approach effectively protects the training data from MIA while still maintaining good model performance. 

### A.4 ADDITIONAL EXPERIMENTAL RESULTS 

In this section, we include additional results from the experiments introduced in Section 4 to further investigate how the DP parameter _ϵ_ , factorization rank and the residual term affect the tradeoff between personalization, generalization and privacy guarantee. Figures 4, 5 and 6 continue the ablation study on the effect of the key parameters that directly affect the tradeoff: residual term, noise level and rank. We summarize the results for each dataset below. 

Figure 4 shows the test accuracy with different parameter settings for Oxford Pets. In general, there is an increase in both local and neighbor classes when incorporating the residual term, highlighting the benefit of the residual in model utility in different datasets. The difference in accuracy is more consistent across different noise and rank values compared to Figure 2. In addition, there is minimal growth in accuracy when we increase the rank value. Therefore, it is beneficial to set any rank value for this particular dataset. 


![](P066_images/P066.pdf-0016-10.png)


Figure 4: Test accuracy of ablation study on noise level, rank and residual term for Oxford Pets 

Figure 5 shows the test accuracy with different parameter settings for Oxford Flowers. The addition of the residual term still improves the overall utility, though the benefit is modest for this dataset. Similar to Oxford Pets, the rank value does not significantly affect the accuracy for both local and neighbor classes. We also observe more drastic drop in accuracy under strong privacy level ( _ϵ_ = 

16 

Published as a conference paper at ICLR 2025 

0 _._ 01). Overall, it is more difficult to balance the tradeoff for Oxford Flowers. One needs to sacrifice strong data protection and set _ϵ ≥_ 0 _._ 1 to achieve good personalization and generalization utility. 


![](P066_images/P066.pdf-0017-02.png)


Figure 5: Test accuracy of ablation study on noise level, rank and residual term for Oxford Flowers 

Figure 6 shows the test accuracy with different parameter settings for Food101. We see an overall increase in local and neighbor accuracy with the introduction of the residual term, and the difference is more significant under higher noise level. In addition, there is minimal reduction in model utility when we increase privacy noise. This behavior is consistent across all rank values, indicating the robustness of our method under strict privacy constraints. 


![](P066_images/P066.pdf-0017-05.png)


Figure 6: Test accuracy of ablation study on noise level, rank and residual term for Food101 

Overall, the affect of the key parameters (noise level, rank and residual term) on the tradeoff between personalization, generalization and privacy varies widely among different datasets. Nonetheless, the results across all datasets show consistent trends, indicating the effectiveness and applicability of our method. 

For completeness, we include Tables 6, 7, 8 and 9 which detail the test accuracy with standard deviation of all the ablation experiments demonstrated in Figures 2, 4, 5 and 6. 

Table 6: Mean test accuracy of our method averaged across 10 clients under non-private setting (without any DP noise). 

|Dataset|Rank|Local cl|asses|Neighbor|classes|
|---|---|---|---|---|---|
|||without residual|with residual|without residual|with residual|
||1|86.64_±_0.78|**93.55**_±_**0.18**|89.70_±_0.81|**93.40**_±_**0.28**|
|Caltech101|2|87.54_±_0.83|**94.51**_±_**0.17**|87.95_±_0.42|**92.79**_±_**0.72**|
||4|89.57_±_0.47|**95.69**_±_**0.57**|86.86_±_0.72|**92.32**_±_**0.71**|
||8|92.12_±_0.47|**96.06**_±_**0.39**|87.58_±_0.17|**91.54**_±_**0.73**|
||1|89.78_±_0.71|**93.46**_±_**0.63**|89.54_±_0.71|**92.17**_±_**0.27**|
|Oxford Pets|2|88.24_±_0.73|**94.49**_±_**0.91**|87.37_±_0.38|**91.96**_±_**0.71**|
||4|91.28_±_0.64|**96.36**_±_**0.28**|88.70_±_0.83|**87.61**_±_**0.53**|
||8|92.42_±_0.81|**96.91**_±_**0.58**|90.71_±_1.09|**80.19**_±_**0.64**|
||1|67.41_±_0.19|**75.45**_±_**0.20**|67.22_±_0.63|**71.49**_±_**0.71**|
|Oxford Flowers|2|66.18_±_0.89|**78.56**_±_**0.90**|66.16_±_0.10|**69.76**_±_**1.11**|
||4|67.04_±_0.61|**81.53**_±_**0.49**|67.02_±_0.39|**68.33**_±_**0.32**|
||8|68.35_±_0.61|**85.75**_±_**0.91**|68.75_±_0.47|**69.51**_±_**0.61**|
||1|74.66_±_1.14|**86.12**_±_**0.38**|74.58_±_0.51|**85.97**_±_**0.72**|
|Food101|2|74.91_±_0.38|**86.06**_±_**0.27**|74.96_±_0.49|**85.89**_±_**0.52**|
||4|74.95_±_0.91|**86.18**_±_**0.63**|74.84_±_0.99|**86.16**_±_**1.06**|
||8|76.95_±_1.02|**86.08**_±_**0.95**|76.02_±_0.77|**86.08**_±_**0.69**|



17 

Published as a conference paper at ICLR 2025 

Table 7: Mean test accuracy of DP-FPL averaged across 10 clients. The DP noise is set to _ϵ_ = 0 _._ 4. 

|Dataset|Rank|Local c|lasses|Neighbor|classes|
|---|---|---|---|---|---|
|||without residual|with residual|without residual|with residual|
||1|87.66_±_0.79|**92.93**_±_**1.18**|90.19_±_1.11|**92.94**_±_**0.68**|
|Caltech101|2|88.98_±_1.02|**93.03**_±_**0.90**|86.99_±_1.34|**88.82**_±_**0.79**|
||4|88.01_±_1.21|**93.58**_±_**0.87**|85.20_±_1.03|**89.15**_±_**0.90**|
||8|90.13_±_1.19|**95.74**_±_**0.63**|85.46_±_1.08|**88.58**_±_**0.38**|
||1|74.87_±_0.69|**90.43**_±_**0.79**|72.41_±_0.49|**87.83**_±_**0.95**|
|Oxford Pets|2|74.66_±_0.88|**91.67**_±_**0.62**|72.69_±_0.33|**86.26**_±_**0.42**|
||4|74.24_±_0.74|**93.22**_±_**0.40**|71.83_±_0.39|**83.53**_±_**0.60**|
||8|77.22_±_0.82|**95.13**_±_**0.52**|73.86_±_0.42|**81.82**_±_**0.42**|
||1|62.48_±_0.83|**75.45**_±_**0.55**|64.41_±_0.58|**71.49**_±_**0.55**|
|Oxford Flowers|2|65.67_±_0.96|**77.39**_±_**0.69**|64.53_±_0.75|**70.97**_±_**0.58**|
||4|66.23_±_0.79|**78.62**_±_**1.04**|63.97_±_0.77|**68.10**_±_**0.67**|
||8|68.03_±_1.41|**80.09**_±_**0.51**|63.22_±_0.88|**67.67**_±_**0.45**|
||1|50.55_±_1.05|**69.76**_±_**0.43**|50.29_±_1.14|**68.11**_±_**0.94**|
|Food101|2|56.07_±_0.85|**72.05**_±_**0.66**|57.10_±_1.13|**71.15**_±_**0.65**|
||4|61.02_±_1.09|**77.76**_±_**0.98**|61.25_±_0.58|**76.48**_±_**0.57**|
||8|69.53_±_0.20|**81.45**_±_**1.01**|67.52_±_0.40|**81.00**_±_**0.90**|



Table 8: Mean test accuracy of DP-FPL averaged across 10 clients. The DP noise is set to _ϵ_ = 0 _._ 2. 

|Dataset|Rank|Local cl|asses|Neighbor|classes|
|---|---|---|---|---|---|
|||without residual|with residual|without residual|with residual|
||1|87.79_±_0.81|**92.16**_±_**0.38**|90.43_±_0.91|**91.61**_±_**1.02**|
|Caltech101|2|88.99_±_0.63|**93.38**_±_**0.82**|87.22_±_0.47|**90.55**_±_**0.49**|
||4|89.25_±_0.61|**94.22**_±_**0.54**|85.31_±_0.28|**90.73**_±_**0.10**|
||8|91.75_±_0.19|**95.28**_±_**0.93**|86.56_±_0.71|**89.72**_±_**0.83**|
||1|70.06_±_0.73|**89.79**_±_**0.59**|73.27_±_0.51|**87.69**_±_**1.08**|
|Oxford Pets|2|72.71_±_0.42|**90.12**_±_**0.49**|72.04_±_0.39|**86.74**_±_**0.18**|
||4|72.27_±_0.84|**91.45**_±_**0.65**|70.16_±_0.77|**83.62**_±_**0.94**|
||8|73.73_±_0.94|**93.09**_±_**0.30**|71.04_±_0.55|**80.67**_±_**0.69**|
||1|55.18_±_0.92|**72.19**_±_**0.17**|64.53_±_0.81|**70.35**_±_**0.97**|
|Oxford Flowers|2|59.52_±_0.53|**73.58**_±_**0.57**|61.41_±_0.31|**70.50**_±_**0.29**|
||4|63.89_±_0.83|**75.18**_±_**0.57**|61.50_±_0.81|**68.65**_±_**0.46**|
||8|63.86_±_0.86|**76.75**_±_**0.97**|62.65_±_0.65|**67.51**_±_**0.73**|
||1|57.38_±_0.35|**69.94**_±_**0.82**|58.11_±_0.37|**63.63**_±_**0.92**|
|Food101|2|59.22_±_0.16|**70.52**_±_**0.75**|58.17_±_0.57|**67.64**_±_**0.38**|
||4|65.12_±_0.52|**75.11**_±_**0.46**|64.74_±_0.44|**70.21**_±_**0.80**|
||8|70.16_±_0.32|**81.25**_±_**0.51**|70.21_±_0.75|**80.79**_±_**0.17**|



Table 9: Mean test accuracy of DP-FPL averaged across 10 clients. The DP noise is set to _ϵ_ = 0 _._ 1. 

|Dataset|Rank|Local cl|asses|Neighbor|classes|
|---|---|---|---|---|---|
|||without residual|with residual|without residual|with residual|
||1|84.73_±_0.32|**91.39**_±_**0.58**|89.33_±_0.85|**90.81**_±_**0.59**|
|Caltech101|2|85.32_±_0.38|**91.11**_±_**0.86**|86.32_±_0.28|**89.18**_±_**0.67**|
||4|87.82_±_0.81|**92.26**_±_**1.28**|84.73_±_0.97|**87.92**_±_**0.80**|
||8|88.82_±_0.84|**92.71**_±_**0.61**|85.32_±_0.86|**90.02**_±_**0.48**|
||1|67.59_±_0.19|**80.41**_±_**0.38**|71.47_±_0.32|**79.24**_±_**0.61**|
|Oxford Pets|2|69.22_±_0.48|**81.65**_±_**1.06**|67.38_±_0.27|**79.65**_±_**0.59**|
||4|69.35_±_0.89|**82.73**_±_**0.49**|66.11_±_0.66|**78.73**_±_**0.87**|
||8|74.48_±_0.91|**85.25**_±_**0.30**|66.10_±_0.49|**77.12**_±_**0.63**|
||1|54.18_±_0.65|**66.78**_±_**1.02**|59.51_±_0.75|**66.93**_±_**0.49**|
|Oxford Flowers|2|57.16_±_0.39|**66.21**_±_**0.29**|65.35_±_0.64|**65.21**_±_**0.94**|
||4|59.71_±_0.83|**67.32**_±_**0.27**|67.71_±_0.41|**67.26**_±_**0.32**|
||8|59.81_±_0.97|**72.11**_±_**1.05**|66.98_±_0.38|**66.44**_±_**0.17**|
||1|62.75_±_0.37|**68.65**_±_**0.81**|58.05_±_0.42|**68.60**_±_**0.28**|
|Food101|2|62.43_±_0.76|**71.84**_±_**0.95**|58.86_±_0.26|**69.66**_±_**0.93**|
||4|64.66_±_0.75|**75.64**_±_**0.41**|65.22_±_0.28|**72.61**_±_**0.30**|
||8|67.20_±_0.48|**80.57**_±_**0.83**|67.06_±_0.99|**78.14**_±_**0.37**|



18 

Published as a conference paper at ICLR 2025 

Table 10: Mean test accuracy of DP-FPL averaged across 10 clients. The DP noise is set to _ϵ_ = 0 _._ 05. 

|Dataset|Rank|Local cl|asses|Neighbor|classes|
|---|---|---|---|---|---|
|||without residual|with residual|without residual|with residual|
||1|78.62_±_0.24|**81.59**_±_**1.55**|78.75_±_0.23|**79.07**_±_**1.59**|
|Caltech101|2|78.63_±_0.18|**85.42**_±_**0.93**|77.67_±_0.34|**77.42**_±_**0.92**|
||4|78.57_±_0.48|**85.05**_±_**1.06**|77.51_±_0.48|**82.28**_±_**1.07**|
||8|78.72_±_0.49|**87.64**_±_**0.98**|76.83_±_0.42|**82.76**_±_**1.69**|
||1|63.28_±_0.57|**70.60**_±_**1.30**|61.75_±_0.58|**72.18**_±_**1.32**|
|Oxford Pets|2|63.32_±_0.68|**73.66**_±_**0.94**|61.76_±_0.70|**72.62**_±_**1.39**|
||4|64.26_±_0.91|**74.29**_±_**1.35**|61.71_±_0.91|**68.73**_±_**1.31**|
||8|65.22_±_0.89|**81.26**_±_**1.00**|61.69_±_0.62|**74.13**_±_**0.99**|
||1|32.98_±_1.13|**59.62**_±_**0.99**|29.91_±_0.61|**46.80**_±_**0.91**|
|Oxford Flowers|2|32.84_±_1.80|**59.74**_±_**1.05**|30.02_±_1.14|**49.19**_±_**1.47**|
||4|32.45_±_1.15|**65.72**_±_**1.17**|30.40_±_0.75|**50.32**_±_**1.18**|
||8|33.09_±_1.62|**69.80**_±_**0.94**|30.21_±_1.28|**56.75**_±_**1.23**|
||1|58.72_±_0.36|**67.19**_±_**0.92**|56.37_±_0.25|**67.09**_±_**0.46**|
|Food101|2|57.01_±_0.41|**67.71**_±_**1.42**|55.59_±_0.77|**67.27**_±_**0.57**|
||4|59.03_±_0.45|**68.13**_±_**1.06**|55.45_±_0.19|**69.44**_±_**0.55**|
||8|64.88_±_0.37|**78.23**_±_**1.36**|63.15_±_0.55|**77.18**_±_**0.77**|



Table 11: Mean test accuracy of DP-FPL averaged across 10 clients. The DP noise is set to _ϵ_ = 0 _._ 01. 

|Dataset|Rank|Local cl|asses|Neighbor|classes|
|---|---|---|---|---|---|
|||without residual|with residual|without residual|with residual|
||1|73.19_±_0.25|**80.89**_±_**1.62**|82.59_±_0.22|**87.98**_±_**1.59**|
|Caltech101|2|75.18_±_0.50|**83.08**_±_**1.16**|82.60_±_0.85|**85.70**_±_**0.79**|
||4|78.19_±_0.48|**84.35**_±_**1.07**|80.61_±_0.48|**82.81**_±_**1.07**|
||8|83.18_±_0.60|**85.21**_±_**2.27**|77.59_±_0.57|**80.60**_±_**1.12**|
||1|53.05_±_0.59|**68.73**_±_**1.29**|48.54_±_1.15|**65.35**_±_**1.36**|
|Oxford Pets|2|53.04_±_1.37|**71.62**_±_**1.10**|49.54_±_1.40|**67.58**_±_**1.10**|
||4|53.06_±_0.91|**73.14**_±_**1.33**|50.52_±_1.35|**70.39**_±_**1.36**|
||8|54.29_±_1.01|**73.71**_±_**1.19**|51.48_±_1.48|**71.89**_±_**1.48**|
||1|32.44_±_1.07|**39.54**_±_**0.97**|30.40_±_0.90|**31.24**_±_**1.08**|
|Oxford Flowers|2|33.11_±_1.84|**42.53**_±_**1.78**|30.94_±_1.53|**38.32**_±_**1.34**|
||4|33.08_±_1.13|**45.27**_±_**1.23**|30.91_±_1.03|**41.24**_±_**1.16**|
||8|33.15_±_1.72|**51.55**_±_**1.21**|30.95_±_1.80|**42.31**_±_**1.85**|
||1|57.63_±_0.44|**67.16**_±_**0.88**|56.57_±_0.31|**68.79**_±_**0.66**|
|Food101|2|57.40_±_0.43|**68.28**_±_**1.40**|56.70_±_1.02|**68.48**_±_**0.60**|
||4|58.98_±_0.55|**69.13**_±_**1.05**|59.39_±_0.20|**69.88**_±_**0.77**|
||8|59.63_±_0.54|**77.45**_±_**3.65**|59.58_±_0.73|**76.87**_±_**0.55**|



19 

