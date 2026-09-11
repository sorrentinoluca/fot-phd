# **PPFedIT: Towards Privacy-preserving Federated Instruction Tuning with Few-shot Local Examples** 

ZHUO ZHANG, Harbin Institute of Technology, Shenzhen, China and Peng Cheng Laboratory, Shenzhen, China 

JINGYUAN ZHANG, Kuaishou Technology, Beijing, China JINTAO HUANG, Harbin Institute of Technology, Shenzhen, China HUI WANG and YUE YU, Peng Cheng Laboratory, Shenzhen, China HONGZHI ZHANG, Kuaishou Technology, Beijing, China XUN ZHOU, Harbin Institute of Technology, Shenzhen, China LIZHEN QU, Monash University, Melbourne, Australia ZENGLIN XU, Fudan University, Shanghai, China 

Instruction tuning has been identified as a crucial technique for optimizing large language models (LLMs) to generate human-aligned responses. Nonetheless, gathering diversified and superior-quality instruction data for such tuning presents notable obstacles, especially in privacy-sensitive domains. Federated instruction tuning (FedIT) has emerged as a promising solution by consolidating collaborative training across multiple data owners, resulting in a privacy-enhancing learning model. Existing FedIT studies assume that clients have sufficient training data, however, in reality, many clients only have few-shot samples, leading to either overfitting in federated LLM or degraded performance. At the same time, this federated few-shot environment also increases the risk of training data extraction attacks, as the LLM may well memorize the limited training data. To address these issues, this article proposes a _novel_ federated algorithm, PPFedIT, designed to enhance privacy protection and model performance of federated few-shot learning. PPFedIT comprises three vital steps on the client side: (1) synthetic data generation, which utilizes the strong generation capacity of LLMs to generate synthetic data, aiming to diversify and enrich local data; (2) parameter isolation training, which respectively updates the parameters of a shared global LLM on the synthetic data and the parameters of local LLMs on the local data, consequently mitigating the noise impact of the synthetic data; (3) local aggregation then sharing mechanism, which mixes the parameters of the global LLM and those of a local LLM first, before uploading them to a server for aggregation. This effectively mitigates data extraction attacks. Extensive 

This work was supported by National Natural Science Foundation of China (62472125); Guangdong Basic and Applied Basic Research Foundation (2025A1515011258); Key Technologies R&D Program of Guangdong Province (2026B0909060001); Shenzhen Science and Technology Programs (GXWD20231128102922001); Shenzhen Science and Technology Programs (ZDCY20250901111705007); Shenzhen Science and Technology Programs (ZDSYS20230626091203008). 

Authors’ Contact Information: Zhuo Zhang, Harbin Institute of Technology, Shenzhen, China and Peng Cheng Laboratory, Shenzhen, China; e-mail: iezhuo17@gmail.com; Jingyuan Zhang, Kuaishou Technology, Beijing, China; e-mail: zhangjingyuan06@kuaishou.com; Jintao Huang, Harbin Institute of Technology, Shenzhen, China; e-mail: 764695611@qq.com; Hui Wang, Peng Cheng Laboratory, Shenzhen, China; e-mail: wangh06@pcl.ac.cn; Yue Yu, Peng Cheng Laboratory, Shenzhen, China; e-mail: yuy@pcl.ac.cn; Hongzhi Zhang, Kuaishou Technology, Beijing, China; e-mail: zhanghongzhi@kuaishou.com; Xun Zhou, Harbin Institute of Technology, Shenzhen, China; e-mail: zhouxun2023@hit.edu.cn; Lizhen Qu(corresponding author), Monash University, Melbourne, Australia; e-mail: Lizhen.Qu@monash.edu; Zenglin Xu, Fudan University, Shanghai, China; e-mail: zenglinxu@fudan.edu.cn. *For correspondence, please contact Xun Zhou, Lizhen Qu, and Zenglin Xu. 

This work is licensed under Creative Commons Attribution International 4.0. 

© 2026 Copyright held by the owner/author(s). ACM 2157-6912/2026/7-ART106 https://doi.org/10.1145/3806196 

ACM Transactions on Intelligent Systems and Technology, Vol. 17, No. 5, Article 106. Publication date: July 2026. 

Z. Zhang et al. 

106:2 

experiments on three open source datasets demonstrate PPFedIT significantly enhances model performance (averaging 8.4%) and reduces the risk of data extraction attacks (approximately 20%) in practical and challenging federated few-shot scenarios. 

CCS Concepts: • **Computing methodologies** → **Natural language processing** ; **Cooperation and coordination** ; 

Additional Key Words and Phrases: Federated few-shot learning, Large Language Model, Data extraction attack. 

### **ACM Reference format:** 

Zhuo Zhang, Jingyuan Zhang, Jintao Huang, Hui Wang, Yue Yu, Hongzhi Zhang, Xun Zhou, Lizhen Qu, and Zenglin Xu. 2026. PPFedIT: Towards Privacy-preserving Federated Instruction Tuning with Few-shot Local Examples. _ACM Trans. Intell. Syst. Technol._ 17, 5, Article 106 (July 2026), 23 pages. https://doi.org/10.1145/3806196 

## **1 Introduction** 

Instruction tuning is a crucial training step that allows **large language models (LLMs)** to understand user intentions and follow instructions directly from prompts [6, 38, 42]. Since instructions can vary by applications and users, collecting instruction-following data for training LLMs is timeconsuming and labor-intensive. Despite the availability of public instruction-tuning datasets, it’s estimated that high-quality public data will be depleted by 2026 [43]. Privacy concerns may further discourage users from sharing their data, such as private conversations and proprietary business data, especially when data sharing is strictly regularized by relevant legislation or regulations, such as the **General Data Protection Regulation (GDPR)** in EU, the **Health Insurance Portability and Accountability Act (HIPAA)** in the US, or personal information protection law in China. 

To address the privacy concern, federated instruction tuning, coined FedIT, is proposed to leverage **federated learning (FL)** [26, 36] for collaboratively training instruction-following LLMs in a distributed environment [14, 27, 41, 47, 50]. As depicted in Figure 1(a), FedIT exchanges model parameters instead of sharing private data among distributed data owners during instruction tuning, aiming to strike a promising balance between privacy protection and model performance. 

Despite FedIT makes significant progress towards its goal, two significant challenges persist: (1) the existing FedIT algorithms assume each client has sufficient instruction data for training, which is difficult to satisfy in many real-world applications. Instead, local devices may merely hold a handful of data for demonstration, referred to as few-shot data, due to the high costs for data collection and annotation. In this case, traditional FL algorithms often experience significant performance degradation on these local devices [7, 8]. As this setting is rarely explored in the prior studies on FedIT, it is desirable to address the limitations of FedIT algorithms for few-shot data. (2) It is reported that it is possible to extract training data from trained LLMs, known as _training data extraction attack_ [5, 9, 37]. As illustrated in Figure 1, the attacker could leverage queries to extract private data from the models uploaded by clients. Although previous research on FedIT has been successful in mitigating model performance degradation on **non-independent and identically distributed (non-IID)** data [34, 53] or reducing training costs [54, 55], these studies have not investigated the risk of training data extraction attack. Consequently, we conduct preliminary experiments to uncover a _new_ key finding: _the original_ FedIT _with federated aggregation can mitigate privacy leakage in comparison to the training algorithms on centralized data, but it is still vulnerable to training data extraction attack, particularly in the federated few-shot learning setting._ 

To tackle the two challenges mentioned above, we propose a _novel_ federated instruction tuning algorithm, coined PPFedIT, to enhance both privacy preservation and model performance with 

ACM Transactions on Intelligent Systems and Technology, Vol. 17, No. 5, Article 106. Publication date: July 2026. 

Privacy-preserving Federated Instruction Tuning with Few-shot Local Examples 

106:3 


![](P021_images/P021.pdf-0003-02.png)



![](P021_images/P021.pdf-0003-03.png)



![](P021_images/P021.pdf-0003-04.png)



![](P021_images/P021.pdf-0003-05.png)



![](P021_images/P021.pdf-0003-06.png)



![](P021_images/P021.pdf-0003-07.png)



![](P021_images/P021.pdf-0003-08.png)



![](P021_images/P021.pdf-0003-09.png)



![](P021_images/P021.pdf-0003-10.png)



![](P021_images/P021.pdf-0003-11.png)



![](P021_images/P021.pdf-0003-12.png)



![](P021_images/P021.pdf-0003-13.png)



![](P021_images/P021.pdf-0003-14.png)



![](P021_images/P021.pdf-0003-15.png)


Fig. 1. (a) Overview of the traditional FedIT framework and (b) the workflow of PPFedIT (illustrated for client _푘_ ). In contrast to FedIT, PPFedIT harnesses the generative power of the global LLM to expand and diversify the local data, boosting model utility in federated few-shot scenarios. Furthermore, to mitigate the notorious data extraction attacks that jeopardize the privacy of training data in FedIT, PPFedIT employs parameter-isolation training and local aggregation sharing, reinforcing client data safety throughout training. 


![](P021_images/P021.pdf-0003-17.png)



![](P021_images/P021.pdf-0003-18.png)



![](P021_images/P021.pdf-0003-19.png)



![](P021_images/P021.pdf-0003-20.png)



![](P021_images/P021.pdf-0003-21.png)



![](P021_images/P021.pdf-0003-22.png)



![](P021_images/P021.pdf-0003-23.png)



![](P021_images/P021.pdf-0003-24.png)



![](P021_images/P021.pdf-0003-25.png)



![](P021_images/P021.pdf-0003-26.png)



![](P021_images/P021.pdf-0003-27.png)



![](P021_images/P021.pdf-0003-28.png)



![](P021_images/P021.pdf-0003-29.png)



![](P021_images/P021.pdf-0003-30.png)



![](P021_images/P021.pdf-0003-31.png)



![](P021_images/P021.pdf-0003-32.png)



![](P021_images/P021.pdf-0003-33.png)


Fig. 2. The overview of PPFedIT. The innovation of PPFedIT compared to FedIT lies in client-side operations, including ①synthetic data generation, ②parameter isolation training, and ③local aggregation sharing. 

few-shot examples in a practical and challenging federated environment. PPFedIT introduces three key steps on the client side, as illustrated in Figure 2. _First_ , to diversify and enrich local training data, we generate synthetic data on each local device by leveraging a global LLM shared across client devices in each federated round. Herein, this LLM employs the few-shot data as demonstration in each local device. _Second_ , to enhance the global LLM and filter out the noisy examples in the synthetic data, we employ a parameter isolation training strategy to train a reinforced local LLM as a filter for each local device by fine-tuning the global LLM on local data, and subsequently update the global LLM on the union of filtered synthetic data. The reinforced local LLMs are employed as: (i) a quality measure to effectively select high-quality synthetic data, and (ii) a way to mitigate noise in synthetic data that could otherwise degrade local LLM performance, which is different than directly mixed training [8, 10]. Using this learning strategy, the global LLM captures privacy-agnostic knowledge shared across clients, while a local LLM preserves sensitive information of a client. _Third_ , to combine the complementary strengths of the global and local LLMs, we propose a local 

ACM Transactions on Intelligent Systems and Technology, Vol. 17, No. 5, Article 106. Publication date: July 2026. 

Z. Zhang et al. 

106:4 

aggregation sharing mechanism, in which the client mixes the parameters of the local LLM with those of the global synthetic LLM before sharing them with the server. As a result, the parameters of the global model are aggregated from each local mixed model in each round. On the one hand, this local mixing mechanism facilitates knowledge fusion between the global LLM and the local LLMs. On the other hand, the local aggregation is analogous to “encrypting” the local LLM by using the global synthetic LLM as the public key. Our work contributions are outlined as follows: 

- It is the first study to enhance FedIT performance and counter data extraction attacks within a real-world and challenging federated few-shot setting. We demonstrate that LLM trained in FL can effectively self-synthesize data, markedly improving model performance under the limited data scenario. Importantly, we discover that federated aggregation operation can mitigate data extraction attacks, leading us to propose a novel local aggregation sharing operation to utilize synthetic data to enhance privacy protection. 

- —We introduce a novel algorithm, termed PPFedIT, validated through extensive experiments across three datasets. The results demonstrate that our method improves model performance by an average of 6% to 13% and reduces privacy leakage by approximately 20% compared to the baseline method. Further analysis indicates that our method effectively generates and filters high-quality instruction data, enriching the local dataset and thus narrowing the performance gap with centralized training. 

## **2 Related Work** 

_Federated Instruction Tuning_ . Federated instruction tuning [50] offers a straightforward yet potent method for supporting distributed client privacy-preserving instruction tuning LLMs via the FL protocol [26, 36], bolstering LLMs’ capabilities for handling privacy-sensitive real-world tasks. This research domain has garnered increasing attention. Zhang et al. [50] pioneered using FL for instruction tuning LLMs. Subsequently, various open benchmarks and repositories have facilitated research on federated instruction tuning tasks, including FederatedScope-LLM [27], Fate-LLM [14], and OpenFedLLM [47]. However, these studies predominantly focus on constructing benchmarks for federated instruction tuning and do not propose advanced federation algorithms. Our work introduces a novel, more privacy-preserving federated instruction tuning algorithm, particularly adept in the federated few-shot setting. Recent work on federated NLP has emerged to enhance federated few-shot performance [7, 8]. However, this research primarily focuses on classification tasks, utilizing pre-trained classification models and assuming extensive local unlabeled data availability. In contrast, we consider more complex instruction tuning tasks and synthetic data generation using the generative capabilities of LLMs. 

_Training Data Extractable Attack in Language Models_ . Training data extraction attack [5, 9, 37] has emerged as a tricky and unresolved challenge that illicit extraction of training data from LLMs. Such attacks typically exploit LLMs’ memorization and prompt LLMs with some prefixes to generate training data. Nasr et al. [37] and Carlini et al. [9] show larger or overfitted LLMs are more prone to leak training data. In our work, we find that federated aggregation can diminish the risk of privacy data leakage compared to centralized training. Thus, we introduce local aggregation sharing against training data extraction in the context of FedIT. 

_LLM as a Data Generator_ . With LLMs revolutionizing the field of NLP, researchers have recently explored their potential as data generators [4, 12, 31, 45, 46, 49, 52] to expand training datasets and reduce labor-intensive and expensive annotation costs. Wang et al. [45] and Zhang et al. [52] curate high-quality, diverse seed data and upload it to AI systems (e.g., OpenAI) for data augmentation. However, this method is not feasible for privacy-preserving scenarios, as it prohibits private data uploading. Alternatively, some research [31] deploys sophisticated LLMs locally for on-device 

ACM Transactions on Intelligent Systems and Technology, Vol. 17, No. 5, Article 106. Publication date: July 2026. 

Privacy-preserving Federated Instruction Tuning with Few-shot Local Examples 

106:5 

data augmentation. Yet, advanced LLMs are typically proprietary, expensive, and computationally demanding. In contrast, our approach leverages progressively enhanced federated LLMs as data generators to iteratively produce task-specific synthetic data throughout the federated process. Recent research [21, 48] on FL with generative models has concentrated on using large models (e.g., diffusion models) to create additional data for addressing non-IID challenges. However, this research has primarily focused on image classification tasks, using image labels for data augmentation while neglecting the noise present in synthetic data. Compared to these studies, our work can self-generate synthetic data complemented by a filtering method to select high-quality synthetic data, achieving appealing performance on the complex federated instruction tuning task. 

## **3 Method** 

In this section, we introduce the proposed PPFedIT for federated few-shot learning, a method of selfgenerating synthetic data for public-private parameter isolation training and privacy-enhancing aggregation sharing. We first provide the preliminaries of FedIT (Section 3.1), then overview PPFedIT (Section 3.2), and layout details about essential components of our framework: synthetic data generation (Section 3.3), parameter isolation training (Section 3.4), and local aggregation sharing (Section 3.5). 

## **3.1 Preliminaries** 

Suppose the standard federated setting comprises _푁_ distributed clients with their local training data D1 _, . . . ,_ D _푁_ and a central server S responsible for coordinating global model training. Before training commences, S dispatches a global backbone model like LlaMa-2 [42] to each client and determines global training parameters (W<sup>_푔_</sup> ) which are exchanged between the server and clients during each training round. Given the substantial communication and computational demands associated with the vast training parameters in LLMs, we adopt **low-rank adaption (LoRA)** [20] as all federated tuning strategies, aligning with prior research [14, 27, 50, 54]. Thus, the W<sup>_푔_</sup> represents lightweight LoRA training parameters. 

In each round of federated training, the procedure alternates between _server-side_ and _client-side_ operations. In the client-side operation, each client uses local data to train the global model and then upload updated parameters W<sup>_푙_</sup> to S. During the server-side operation, S aggregates the client-upload model parameters to produce the updated global parameters for the next training round. This process is repeated multiple rounds until a certain condition is met (e.g., maximum communication rounds R). 

## **3.2 Overview** 

The innovation of PPFedIT lies in its client-side operations, which consist of three key steps: synthetic data generation, parameter isolation training, and local aggregation sharing. We introduce private parameters W<sup>_푙_</sup> , which are of the same size as the global parameters W<sup>_푔_</sup> and are managed locally by each client. In the synthetic data generation step, W<sup>_푔_</sup> self-generates data relevant to the local context. Subsequently, the client performs parameter isolation training, where W<sup>_푙_</sup> is trained on private local data D _푘_ , and W<sup>_푠_</sup> on high-quality synthetic data D _푘_<sup>_푠_filtered by W</sup><sup>_푙_. This step</sup> can further mitigate the impact of noise in synthetic data. Inspired by experimental findings that federated aggregation can reduce privacy leakage, we implement local aggregation sharing, which combines W<sup>_푠_</sup> and W<sup>_푙_</sup> with a parameter _훽_ before uploading to the server. This process reduces the exposure of privacy parameters, thereby mitigating the risk of local private data leakage. The comprehensive framework of our method is detailed in Algorithm 1. 

ACM Transactions on Intelligent Systems and Technology, Vol. 17, No. 5, Article 106. Publication date: July 2026. 

Z. Zhang et al. 

106:6 

**Algorithm 1:** Training Process of PPFedIT 


![](P021_images/P021.pdf-0006-03.png)

### Figure analysis

**Purpose.** This pseudocode specifies the full training process of PPFedIT, showing how each communication round alternates between client-side operations and server-side federated aggregation.

**Important components and labels.**
- **Inputs/parameters:** clients with local datasets \(C=\{\mathcal{D}_1,\mathcal{D}_2,\ldots,\mathcal{D}_N\}\), communication rounds \(R\), initial global parameters \(\mathcal{W}^g_0\), client-local parameters \(\mathcal{W}^{l,k}_0\), synthetic data \(\mathcal{D}^s_k\) of size \(M\), and local aggregation-sharing parameters \(\mathcal{W}^a_{k,r}\).
- **Procedures named in the algorithm:** `LocTrain` denotes local training, and `SynSel` denotes synthetic data selection.
- **Client sampling:** in each round \(r=1\) to \(R\), the server randomly samples \(K\) clients \(C^r\subset C\).
- **Server-to-client flow:** global parameters \(\mathcal{W}^g_{r-1}\) are sent to selected clients.
- **Client-side flow:** each selected client performs synthetic data generation, parameter isolation training, synthetic-data selection, synthetic-data training, and local aggregation sharing.
- **Client-to-server flow:** each client sends only the locally aggregated sharing parameter \(\mathcal{W}^a_{k,r}\) to the server.

**Direct observations from the pseudocode.**
1. Synthetic data are generated as
   \[
   \mathcal{D}^s_k \leftarrow \mathrm{SynGen}(\mathcal{D}_k, \mathcal{W}^g_{r-1}).
   \]
2. Private/local parameters are trained on real local data:
   \[
   \mathcal{W}^l_{k,r} \leftarrow \mathrm{LocTrain}(\mathcal{D}_k, \mathcal{W}^g_{r-1}).
   \]
3. Synthetic samples are filtered or selected using the trained local parameters:
   \[
   \mathcal{D}^s_k \leftarrow \mathrm{SynSel}(\mathcal{D}^s_k, \mathcal{W}^l_{k,r}).
   \]
4. Synthetic-training parameters are then trained on selected synthetic data:
   \[
   \mathcal{W}^s_{k,r} \leftarrow \mathrm{LocTrain}(\mathcal{D}^s_k, \mathcal{W}^g_{r-1}).
   \]
5. Local aggregation sharing combines private/local and synthetic-trained parameters:
   \[
   \mathcal{W}^a_{k,r} \leftarrow \beta\mathcal{W}^l_{k,r} + (1-\beta)\mathcal{W}^s_{k,r}.
   \]
6. Server aggregation updates the global model using weighted averaging:
   \[
   \mathcal{W}^g_r \leftarrow \sum_{k=1}^{K} p_k\mathcal{W}^a_{k,r}, \qquad p_k \leftarrow \frac{n_k}{\sum_{i=1}^{K} n_i}.
   \]

**Key comparisons and relationships.**
- The algorithm explicitly separates \(\mathcal{W}^l_{k,r}\), trained on private local data, from \(\mathcal{W}^s_{k,r}\), trained on selected synthetic data.
- The upload parameter \(\mathcal{W}^a_{k,r}\) is a mixture controlled by \(\beta\), rather than a direct upload of only the private-data-trained parameter.
- Server aggregation weights each selected client by its local data size \(n_k\), making the update analogous to sample-size-weighted federated averaging.

**Interpretation connected to the surrounding text.** The surrounding section describes PPFedIT as relying on three client-side innovations: synthetic data generation, parameter isolation training, and local aggregation sharing. This algorithm operationalizes that description: the global model helps generate synthetic data, local parameters are trained on private data and used to filter synthetic data, synthetic-trained parameters are learned separately, and the final uploaded client update blends the two parameter sets before server aggregation. The visual therefore serves as the formal procedural specification for the method introduced in Section 3.2 and preceding the detailed explanation of synthetic data generation in Section 3.3.


## **3.3 Synthetic Data Generation** 

Given the inherent data scarcity in federated few-shot scenarios, our approach leverages the concept of LLM-as-a-data-generator from previous work to augment local datasets [12, 45, 52]. However, the traditional LLM-as-a-data-generator approaches remain underutilized in privacysensitive contexts because they send private data to an open AI service provider (e.g., GPT-4), which violates data protection laws and incurs the high costs of numerous API calls. To circumvent these obstacles, we propose synthetic data generation to employ the federated instruction-tuned LLM as the data generator, complemented by a filtering method to ensure high-quality synthetic data. The underlying concept is that clients can enrich their local data by leveraging the global model that assimilates diverse instructions from multiple clients. For convenience, we abbreviate the LLM with W<sup>_푔_</sup> as M<sup>_푔_</sup> and LLM with W<sup>_푙_</sup> as M<sup>_푙_</sup> . In the synthetic data generation step, the data generator M<sup>_푔_</sup> creates diverse candidate examples by using local data as demonstrations to exploit the in-context capabilities of LLM. Suppose _푘_ th local client data _퐷푘_ contains _푛푘_ triples { _퐼푛푠푡푟푢푐푡푖표푛, 푅푒푠푝표푛푠푒_ }. The M<sup>_푔_</sup> generates synthetic candidate samples in two phases: 

_Generate New Reasonable Instructions_ . We randomly select eight instructions from local data as demonstrations to prompt M<sup>_푔_</sup> for new instruction generation. The Prompt for generating new instructions is provided in Appendix B. We then provide a format filter to eliminate failed instructions.<sup>1</sup> We also follow prior research [45, 52] and use Rouge-L [35] similarity to amplify textual diversity. Namely, we discard new instructions with a Rouge-L similarity above 0.7 to any other 

1For example, the failed generated sentences may begin with “As a …”, “sorry, …” or be too short. 

ACM Transactions on Intelligent Systems and Technology, Vol. 17, No. 5, Article 106. Publication date: July 2026. 

Privacy-preserving Federated Instruction Tuning with Few-shot Local Examples 

106:7 

local instructions. _Generate the corresponding responses given new instructions_ . We prompt M<sup>_푔_</sup> with randomly sampled examples followed by the new instruction (see the Prompt in Appendix B). We require newly generated responses to conform to the template format (e.g., the generation contains the format prefixes [ _푅푒푠푝표푛푠푒_ ]). If the newly generated part does not meet the requirements, we will re-select demonstrations and generate them again. In our experiments, we discard the new instruction if it fails to generate a compliant sample three times. Additionally, we find the M<sup>_푔_</sup> may generate sentences directly copied from demonstrations due to weak instruction-following capability in early federated training. To mitigate this issue, we employ Rouge-L to filter out generated samples with over 0.7 similarity to any local examples. This also reduces the risk of leaking local data in synthetic data, as shown in Section 4.3. We utilize greedy decoding for all generations to encourage M<sup>_푔_</sup> to generate more grounded outputs [18]. 

## **3.4 Parameter Isolation Training** 

We rely on heuristic methods (e.g., Rouge-L or format) to filter out failed examples during synthetic data generation. However, whether the model generates accurate and contextually appropriate responses to new instructions remains uncertain, particularly in the early stages of federated training where the model may output low-quality responses due to weak generation capability. Using synthetic data of varying quality directly degrades model performance or even leads to performance collapse. It is critical to filter and utilize synthetic data effectively. Therefore, we propose a novel local training strategy, parameter-isolated training, to minimize the adverse effects of noisy synthetic data on model performance. 

Parameter isolation training begins by selecting appropriate training data from the generated examples. To conserve computational resources and protect potential privacy within the synthetic data, we refrain from using external models (such as GPT-4) as in prior research [11, 45]. Instead, we use local privacy data to finetune an improved model M<sup>_푙_</sup> based on M<sup>_푔_</sup> and designate it as the evaluator to discern suitable examples from the generated candidates.<sup>2</sup> Given the candidate example, we define the prompt _푥_ as instruction with optional input and the output _푦_ as the response. Typically, using the prompt _푥_ as context simplifies the task for the LLM to generate _푦_ . We employ the **instruction following score (IFS)** to score each example and filter high-quality candidates [29]. M<sup>_푙_</sup> calculates the conditional output loss _퐿_ ( _푦_ | _푥_ ) and the direct output loss _퐿_ ( _푦_ ), with the instruction following score defined as _퐼퐹푆_ =<sup>_퐿_</sup> _퐿_<sup><u>(</u></sup><sup>_<u>푦</u>_</sup> ( _푦_<sup><u>|</u></sup><sup>_푥_</sup> )<sup><u>)</u>. The IFS metric evaluates the degree</sup> of assistance the instruction provides in generating the corresponding response by comparing the model’s response loss with and without instructional context. Thus, IFS can demonstrate how well the model aligns each response to the prompt. The low IFS indicates that the output _푦_ closely aligns with the prompt _푥_ , signifying the example’s quality. Finally, we sort the candidate examples by their IFS scores in ascending order and select the top _푀_ examples as synthetic data. 

Despite rigorous synthetic data selection, noise may persist, particularly during the early stages of federated training due to the suboptimal performance of local models. Parameter isolation training mitigates this problem by independently training the global model parameters W _푟_<sup>_푔_</sup> −1<sup>on filtered</sup> synthetic and local data. This process yields two distinct updated parameters: synthetic parameters W<sup>_푠_</sup> _푘,푟_<sup>, trained on synthetic data, and local parameters W</sup> _푘,푟_<sup>_푙_, trained on local data. Our method</sup> contrasts with traditional approaches that mix synthetic and private data and effectively reduce the influence of noisy synthetic data, as corroborated by experimental results in Section 4.3. On the other hand, local parameters are learned from local training data, while synthetic parameters 

> 2 Our preliminary experiments reveal that directly employing M _푔_ to select synthetic data generated by itself result in overfitting and performance collapse. 

ACM Transactions on Intelligent Systems and Technology, Vol. 17, No. 5, Article 106. Publication date: July 2026. 

Z. Zhang et al. 

106:8 

are derived from synthetic data. By separating these two types of parameters, we can more easily distinguish between sensitive local data and less critical synthetic data. This clear separation allows us to focus on protecting the local parameters, which are directly tied to private data, thereby enhancing privacy preservation. 

## **3.5 Local Aggregation Sharing** 

After parameter isolation training, we design the local aggregation sharing mechanism to improve model preference and resist data extraction attacks. Specifically, we use the hyperparameter _훽_ to orchestrate the aggregation of local parameters and synthetic parameters: W _푘,푟_<sup>_푎_=</sup><sup>_훽_∗W</sup> _푘,푟_<sup>_푙_+ (1 −</sup> _훽_ ) ∗W _푘,푟_<sup>_푠_. The hyperparameter</sup><sup>_훽_controls the extent of exposure of the private parameters. High</sup><sup>_훽_</sup> means the client exposes more privacy parameters and faces a higher risk of privacy leakage. Note that our approach degenerates into FedIT when _훽_ = 1. Consistent with federated aggregation, local aggregation integrates the knowledge from synthetic data and local data to enhance the model’s performance in federated few-shot learning. Moreover, the update of synthetic data parameters W<sup>_푠_</sup> _푘,푟_<sup>can act as “noise” injected into the locally private parameters W</sup> _푘,푟_<sup>_푙_, thereby strengthening the</sup> protection of client data. By prioritizing the protection of local parameters during aggregation and sharing processes, we can enhance the ability to protect privacy-sensitive data while still benefiting from the performance improvements offered by synthetic data. 

## **4 Experiment** 

This section showcases the effectiveness of PPFedIT through extensive experiments. We begin with the experiment setup in Section 4.1 and then report the performance assessment results in Section 4.2 and privacy defense evaluations in Section 4.3, respectively. Moreover, we provide further analysis in Section 4.4 to explore how PPFedIT works. 

## **4.1 Experimental Setup** 

_Dataset and Partitions_ . We evaluate the effectiveness of PPFedIT using three open source instruction datasets, which contain one open domain Alpaca [39], and two medical domains MedInstruct [52] and MedAlpaca [17]. Previous work [11, 29, 33] demonstrated that the diversity and quality of data are essential in LLM instruction tuning. We follow Li et al. [29] and use the _k_ -means algorithm to cluster each dataset into 100 clusters. Then, we take 10 or 5 samples from each cluster to construct federated few-shot training settings for different domains. The test sets for different datasets are the AlpacaEval [32] and MedInstructTest [52] for Alpaca and MedInstruct, respectively. For MedAlpaca, we randomly select 400 samples, ensuring no overlap between training and test sets. Please see Appendix A for more dataset details. For the federated partition, we consider realistic and challenging non-IID data partitioning throughout the experiments [54]. In particular, we partition all datasets using the Dirichlet distribution [19] with heterogeneity parameter 1.0 and cluster information as labels. Considering various FL scenarios, we set the amount of Cross-device clients to 50 and the amount of Cross-silo clients to 10. Table 1 shows our experiment’s data statistics and federated setting. 

_Baselines_ . Our experiment compares the proposed PPFedIT against the following baselines: Centralized is the skyline algorithm aggregating all data for model training without considering data privacy. FedIT represents the orthodox family of privacy-preserving instruction tuning algorithms, including FedAvg [36], FedProx [30], SCAFFOLD [24], and FedOPT [40]. FewFedWeight [10] advances federated few-shot learning by leveraging the global model to generate client pseudo labels and utilizing an energy-based algorithm to weight the pseudo samples. 

ACM Transactions on Intelligent Systems and Technology, Vol. 17, No. 5, Article 106. Publication date: July 2026. 

Privacy-preserving Federated Instruction Tuning with Few-shot Local Examples 

106:9 

Table 1. The Data Statistics and Federated Setting in Our Experiment 

||Data St|atistics|Federa|ted Setin|g|
|---|---|---|---|---|---|
|Datasets||Train|||Test||Scenario|Rounds||Clients||
|Alpaca|1,000|805|Cross-device|30|50|
|MedInstruct|500|216|Cross-silo|10|10|
|MedAlpaca|1,000|400|Cross-device|30|50|



_Evaluation Protocol_ . Our experiment conducts free-form instruction evaluation for all methods using GPT-4<sup>3</sup> as a judge. GPT-4 compares responses from an instruction-tuned LLM with reference responses from another LLM API (e.g., text-davinci-003 or GPT-3.5-turbo) or human for each corresponding instruction in the test sets. To improve the quality of the evaluations and mitigate the positional effects of GPT-4’s assessments, we implement a dual-sided scoring system, as described in previous studies [52, 57]. This system evaluates each output comparison twice, alternating the order of the instruction-tuned model output and the reference output. Appendix B provides the evaluation prompt used by GPT-4. 

_Models and Training Details_ . Our experiment utilizes the LlaMa-2-7B model [42] because it is one of the most widely used LLMs and is extensively employed in almost all FedIT studies. In real-world federated edge devices (e.g., smartphones and PCs), the LlaMa-2-7B model remains computationally demanding and has communication overhead. To address this, we employ LoRA [20] with a low rank of 16 for training local LLMs across all baseline methods. Unless otherwise specified, we set the local epochs to 1 for all federated methods while setting the local epochs to 10 for Centralized. Following the cross-device protocol [47], we randomly select two clients in each round. We use the AdamW optimizer with a training batch size of 8. PPFedIT generates 32 candidate samples in each self-generation step, filtering out 16 samples to create a synthetic dataset using IFS. By default, we set _훽_ = 0 _._ 5 as it provides the best tradeoff between privacy loss and model utility. See Appendix A for more training details. 

## **4.2 Utility Experiment** 

Table 2 presents the performance results of PPFedIT alongside baselines. We denote the WT score as the win and tie ratio sum. We can observe that PPFedIT _surpasses all federated algorithms with a substantial improvement of 8.4% on the average WT score and closely approaches the skyline algorithm_ Centralized _performance (less than 3%)_ . From Table 2, PPFedIT exhibits a 7% to 13% improvement over the FedIT family within the federated few-shot context. Compared to the state-of-the-art FewFedWeight method, PPFedIT demonstrates a notable 6.3% enhancement on the average WT score. While FewFedWeight also relies on pseudo-response generation during training to bolster federated few-shot performance, it fails to expand the diversity and scale of its local training data. In contrast, PPFedIT _generates more useful task data, effectively mitigating data scarcity concerns_ . We provide more synthetic data quality analysis in Appendix C. 

In Table 2, we observe that FedIT algorithms lag behind federated few-shot algorithms, while centralized algorithms consistently outperform all federated counterparts. This observation underscores two key points: (1) Developing robust federated few-shot algorithms is essential, particularly when local clients possess limited training data. (2) Non-IID data distribution remains a significant challenge for federated instruction tuning. Notably, PPFedIT performs comparably to Centralized, 

> 3GPT-4-0613 version is used in our experiments. 

ACM Transactions on Intelligent Systems and Technology, Vol. 17, No. 5, Article 106. Publication date: July 2026. 

Z. Zhang et al. 

106:10 

Table 2. The Performance of PPFedIT and Other Contenders on Federated Few-Shot Instruction Tuning 

|Methods|Win (↑)|Alpaca<br>Tie (↑)|Lose (↓)|M<br>Win (↑)|edInstru<br>Tie (↑)|ct<br>Lose (↓)|M<br>Win (↑)|edAlpac<br>Tie (↑)|a<br>Lose (↓)|Win (↑)|Avg.<br>Tie (↑)|Lose (↓)|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Centralized|23.0|34.9|42.1|26.1|59.8|14.1|32.4|16.2|51.4|27.2|37.0|35.9|
|FedAvg|11.3|29.2|59.5|20.8|**58.5**|20.7|29.2|12.8|58.0|20.4|33.5|46.1|
|FedProx|12.3|30.4|57.3|22.5|58.0|19.5|28.5|13.2|58.3|21.1|33.9|45.0|
|SCAFFOLD|11.4|31.6|57.0|22.0|**58.5**|19.5|29.0|10.5|60.5|20.8|33.5|45.7|
|FedOPT|10.2|29.1|60.7|18.5|53.0|28.5|26.0|10.1|63.9|18.2|30.7|51.0|
|FewFedWeight|15.3|29.6|55.1|23.1|57.2|19.7|28.7|13.1|58.2|22.4|33.3|44.3|
|PPFedIT|**22.3**|**34.0**|**43.7**|**25.5**|**58.5**|**16.0**|**30.8**|**14.9**|**54.3**|**26.2**|**35.8**|**38.0**|



PPFedIT surpasses all federated algorithms and closely approaches the skyline algorithm Centralized performance. The best performance is highlighted in bold. 

demonstrating robustness against the non-IID challenge. This robustness is attributable to _synthetic data generation, which integrates insights from other clients during the federated process, diversifying local data and enhancing overall training performance._ 

## **4.3 Privacy Experiment** 

Next, we investigate the privacy-preserving capabilities of our method against the notorious training data extraction attack. We employ the discoverable memorization attack method elucidated by Nasr et al. [37]. Given a training string _푠_ = [ _푝_ || _푦_ ] ∈ _퐷푘_ that consists of a prefix _푝_ and suffix _푦_ , the discoverable memorization attack prompts the threat model with the proper prefix _푝_ to generate _푦_ . Discoverable memorization provides an upper bound estimation for the effectiveness of training data extraction attacks and is also prevalent in practical contexts. For example, attackers may target specific sensitive information such as “My bank card password is …” [15] or clients may seek to gauge the extent of privacy leakage in their shared models. 

_Setup_ . Our privacy experiment considers an attacker who can access and query the threat model M _푔_ . This scenario is practical as the model is exposed during federated communication or deployed on the client side. We randomly select 100 examples from different clients in MedInstruct to construct the attack dataset. For each example, the attacker exploits the prompt as the prefix _푝_ and queries M _푔_ to generate the response _푦_<sup>′</sup> . We then evaluate the Rouge-L similarity between the actual _푦_ and _푦_<sup>′</sup> . The higher Rouge-L similarity indicates serious privacy leakage. Moreover, we investigate privacy leakage in synthetic samples since our method employs local privacy data as demonstrations for generating them. Specifically, we calculate the Rouge-L similarity between synthetic and private samples for each client. We exploit the FedAvg and **federated mixed training (FedMIT)** as baselines. FedMIT refers to the direct integration of synthesized data and private data for local training. This approach does not involve parameter isolation training and local aggregation sharing operations compared to our method. Since the _훽_ parameter in our method regulates the exposure of private data during upload, we present experimental results for _훽_ ∈{0 _._ 0 _,_ 0 _._ 3 _,_ 0 _._ 5 _,_ 0 _._ 7}. Note that our method degenerates to FedAvg when _훽_ = 1. We also show the Pre-train, which refers to the backbone model without instruction tuning. 

_Results_ . Figure 3 presents the privacy data leakage measurement of Centralized, FedIT, and PPFedIT during the training process. We find the LLM under Centralized is more likely to memorize the training data than federated algorithms and leads to increased privacy leakage when the same data is used for training.<sup>4</sup> In contrast, _federated algorithms can mitigate these privacy leakage risks through federated aggregation operations_ . However, regrettably, FedIT remains relatively 

4In a cross-silo setting, the training data used in each round of FedIT is the same as that used in each epoch of Centralized. 

ACM Transactions on Intelligent Systems and Technology, Vol. 17, No. 5, Article 106. Publication date: July 2026. 

Privacy-preserving Federated Instruction Tuning with Few-shot Local Examples 

106:11 


![](P021_images/P021.pdf-0011-02.png)

### Figure analysis

Purpose: This line chart measures privacy leakage under a training data extraction attack by plotting Rouge-L similarity over training rounds/epochs for three methods.

Chart structure:
- Title: **Training Data Extraction Attack**.
- x-axis: **Rounds/Epochs**, with visible ticks at 0, 2, 4, 6, and 8.
- y-axis: **Rouge-L**, with visible ticks from 30 to 80.
- Legend/series:
  - **Centralized**: red line with square markers.
  - **FedPIT**: blue line with square markers; this appears to correspond to the federated instruction-tuning baseline discussed in the text.
  - **PPFedIT**: teal line with square markers.
- Shaded regions:
  - A light green area highlights the leakage gap between Centralized and the federated baseline.
  - A light red area highlights the leakage gap between the federated baseline and PPFedIT.

Direct visual observations:
- All visible methods begin at similar Rouge-L levels near the first round/epoch.
- **Centralized** rises most sharply and remains the highest-leakage curve after the initial point.
- **FedPIT** increases more moderately than Centralized but remains above PPFedIT throughout the visible training process.
- **PPFedIT** shows the slowest increase and the lowest Rouge-L values after the initial point.
- The separation between Centralized and the federated methods becomes especially large around the later visible rounds/epochs.
- The gap between FedPIT and PPFedIT persists across the visible range, supporting the claim that PPFedIT reduces training-data memorization relative to the federated baseline.

Connection to the paper text:
- The surrounding text states that higher Rouge-L similarity indicates more severe privacy leakage from training data extraction.
- The chart visually supports the paper’s claim that centralized instruction tuning is more prone to memorizing private training data than federated approaches.
- It also supports the claim that PPFedIT further mitigates leakage compared with the federated baseline, consistent with the role of local aggregation sharing and privacy-preserving parameter handling described in the paper.

Uncertainty:
- Exact Rouge-L values are not printed next to the markers, so only qualitative comparisons are reliable.
- The right side of the plot is cropped, and any additional final-round point is not fully visible.


Fig. 3. The privacy data leakage measurement of Centralized, FedIT, and PPFedIT during the training process. The light green and light red areas reflect the data leakage gaps between FedIT and Centralized, as well as FedIT and PPFedIT, in the same training stage. 

vulnerable to data extraction attacks, highlighting the need for improved privacy preservation in FL frameworks. 

Figure 4 presents the tradeoff between privacy data leakage risk and model performance. We find PPFedIT _demonstrates stronger privacy-preserving capabilities against the training data extraction attack than all baselines_ . In Figure 4(a), we observe that the risk of privacy data leakage increases with training duration across all methods. Among these methods, FedAvg ( _훽_ = 1 _._ 0) exhibits the highest leakage, whereas PPFedIT with _훽_ = 0 _._ 0 shows the lowest. FedMIT, which mixes synthetic and local data in its local training process, does not reduce privacy data leakage risk compared to PPFedIT and FedAvg. These results demonstrate that the data extraction attack in FedIT severely leaks clients’ privacy-sensitive data, underscoring the necessity of our proposed local aggregation sharing operations. 

As illustrated in Figure 4(b), we find PPFedIT can flexibly adjust _훽_ to achieve a better balance. FedMIT produces results comparable to FedAvg but falls short of our method with _훽_ = {0 _._ 5 _,_ 0 _._ 7}. These findings suggest that even carefully curated synthetic data also remains noise and parameter isolation training can effectively mitigate and enhance model performance. Surprisingly, our method with _훽_ = 0 _._ 0 also achieves a 10.3% win ratio, solely using synthetic data for federated aggregation. This result suggests that our method can generate useful data for improving model performance. 

Figure 4(c) plots the distribution of Rouge-L similarity scores between private samples and their generated synthetic ones. We find that there is a significant disparity between synthetic data and local private data. Our approach explicitly limits the overlap between synthetic and original data in Section 3.3 to ensure that _the synthetic data does not leak information from local data_ . This precaution is essential for further preserving client privacy. 

## **4.4 Further Analysis** 

To explore how PPFedIT works, we undertake a thorough analysis, including the contribution of local data and FL to synthetic data generation, the impact of different high-quality synthetic data selections, and the additional computational overhead. 

_4.4.1 Contribution of Local Data to Self-generation._ Within PPFedIT, synthetic data generation leverages local data as demonstrations to generate task-related data. As depicted in 

ACM Transactions on Intelligent Systems and Technology, Vol. 17, No. 5, Article 106. Publication date: July 2026. 

Z. Zhang et al. 

106:12 


![](P021_images/P021.pdf-0012-02.png)


Fig. 4. (a) Privacy data leakage of PPFedIT with different _훽_ and baselines proceeds with the federated training process. (b) The tradeoff between privacy data leakage ( _y_ -axis) and model utility ( _x_ -axis). (c) The distribution of the Rouge-L similarity between private samples and their generated synthetic samples. We measure privacy data leakage using Rouge-L, where higher values indicate more significant privacy leakage. The model utility uses the WT score, representing the win and tie ratio sum. The parameter _훽_ in PPFedIT determines how much client privacy parameters are exposed. Pre-train refers to the backbone model without instruction tuning. PPFedIT demonstrates stronger privacy-preserving capabilities against training data extraction attacks than all baselines. 

Table 2, integrating synthetic data enhances model performance in federated few-shot scenarios. We investigate whether injecting out-of-domain or domain-similar (e.g., medical instruction data) public data can also yield similar enhancements. We substitute the self-generated synthetic data with equal proportions of out-of-domain or domain-similar public data during federated training. Specifically, we employ Alpaca as the out-of-domain public data (+OOD) and MedAlpaca for domain-similar public data (+SIMD). We randomly select the remaining training data from MedInstruct (+IDEAL) as the ideal synthetic training data. 

Figure 5(a) presents the performances of various synthetic data in federated few-shot instruction tuning. The incorporation of domain-similar data (+SIMD and +IDEAL) enhances training performance, while the inclusion of out-of-domain data (+OOD) results in a decline (4.5% performance gap compared to FedAvg). This result shows _adding synthetic data that is more similar to local data can improve federated training performance_ . Our method exhibits a 2.1% performance enhancement compared to +SIMD. These results highlight the significance of local data in self-generation. Additionally, our method’s performance closely approximates that of +IDEAL (less than 2% WT score), indicating the high fidelity of our self-generated synthetic data. 

_4.4.2 Can_ PPFedIT _Discard FL?_ Synthetic data generation shows the effectiveness of local dataset expansion. This raises the question of whether we can solely rely on local data without resorting to FL. To address this question, we conduct experiments implementing **local instruction tuning (LocIT)** and local self-generation without FL (LocIT +SG) on MedInstruct. The outcomes in Figure 5(b) reveal that while LocIT +SG significantly enhances LocIT performance, and the synthesized data remains inadequate and lags behind FedAvg and PPFedIT. This result underscores that _FL is still indispensable for data-scarce and privacy-sensitive downstream tasks_ . 

_4.4.3 Performance under Different Non-IID Settings._ Non-IID data represents a major challenge in FL, often leading to significant degradation in model performance. Following the configuration of Lin et al. [34], we employ a Dirichlet distribution as the class prior to partition datasets. Specifically, 

ACM Transactions on Intelligent Systems and Technology, Vol. 17, No. 5, Article 106. Publication date: July 2026. 

Privacy-preserving Federated Instruction Tuning with Few-shot Local Examples 

106:13 


![](P021_images/P021.pdf-0013-02.png)

### Figure analysis

The figure contains two side-by-side bar-chart panels evaluating synthetic data choices and the role of federated learning in PPFedIT.

**Panel (a): Synthetic data replacement during federated training**

- **Axes and labels:** The y-axis is labeled **Win and Tie Ratio**, with visible ticks from 40 to 90. The x-axis categories are **FedAvg**, **+OOD**, **+SIMD**, **+IDEAL**, and **Ours**. No separate legend is shown; each method is represented by a single colored bar.
- **Direct observations:**
  - **+OOD** has the lowest bar among the federated-training variants, below **FedAvg**.
  - **+SIMD** is higher than **FedAvg** and **+OOD**.
  - **+IDEAL** is the highest bar in this panel.
  - **Ours** is slightly below **+IDEAL** but above **+SIMD**, **FedAvg**, and **+OOD**.
- **Interpretation tied to the text:** This supports the paper's claim that synthetic data more similar to local data improves federated few-shot instruction tuning, whereas out-of-domain synthetic data degrades performance. The surrounding text states that **+OOD** has a 4.5% performance gap compared with FedAvg, **Ours** improves by 2.1% over **+SIMD**, and **Ours** is within less than 2 WT score points of **+IDEAL**.

**Panel (b): Contribution of federated learning to synthetic data generation**

- **Axes and labels:** The y-axis again reports **Win and Tie Ratio**, with visible ticks from 20 to 90. The x-axis categories are **FedAvg**, **LocIT**, **LocSG**, **Centralized**, and **Ours**.
- **Direct observations:**
  - **LocIT** is the lowest-performing method by a large margin.
  - **LocSG** improves over **LocIT** but remains well below **FedAvg** and **Ours**.
  - **Centralized** is the highest bar.
  - **Ours** is close to **Centralized** and higher than **FedAvg**, **LocIT**, and **LocSG**.
- **Interpretation tied to the text:** The visual trend supports the paper's conclusion that local self-generation helps local instruction tuning but is not sufficient to match federated training. The comparison indicates that federated learning remains important for data-scarce and privacy-sensitive downstream tasks, while PPFedIT approaches centralized performance more closely than purely local alternatives.

No error bars, confidence intervals, or numerical labels are visible, so the plot primarily supports rank-order and relative-comparison conclusions rather than exact value extraction.


Fig. 5. (a) The WT scores of various replaced synthetic data during the federated training process. (b) The contribution of FL to synthetic data generation. 

we sample from D ∼ _퐷푖푟_ ( _훼_ ) and assign the resulting subset D _푘_ to client _푘_ . The concentration parameter _훼_ controls the degree of Non-IID: smaller values of _훼_ induce greater label distribution skew across clients. 

Figure 7(a) presents convergence analyses of various methods under the setting _훼_ = 1. We observe that our approach consistently outperforms competing baselines, achieving faster and more stable convergence to superior performance. We further examine the behavior of our method under different non-IID distributions. As shown in Figure 7(b), across a range of non-IID settings, our approach demonstrates substantial improvements over alternatives. Compared with the naïve FedAvg algorithm, SCAFFOLD exhibits improved robustness due to its use of control variates to mitigate “client drift” in local updates. On the contrary, our method leverages globally shared models to generate synthetic data as a form of shared knowledge, thereby enhancing resilience to severe Non-IID settings. 

_4.4.4 Impact of Different Synthetic Data Selection Methods._ Our experiment utilizes the IFS selection method to assess the alignment of model responses with corresponding prompts. We also investigate other scoring functions, including sequence **perplexity (PPL)** , **instruction following difficulty (IFD)** [29], and **random selection (Rand)** . In Figure 6, we find _IFS can more effectively screen higher-quality samples than the other methods_ . IFD selects the highest conditional probability and performs the worst. This finding highlights that prioritizing high-quality instructions is more crucial than selecting difficult ones, especially when dealing with noisy synthetic data. 

_4.4.5 Impact of Demonstration Size and Synthetic Data Volume._ We systematically examine the effects of demonstration size and synthetic data volume on model performance. As shown in Figure 8(a), performance steadily improves with an increasing number of demonstration samples, underscoring the importance of richer contextual information. However, when the demonstration is severely limited (e.g., only a single sample), model performance deteriorates sharply, indicating insufficient guidance for effective generalization. Figure 8(b) depicts the influence of synthetic data volume. While enlarging the synthetic dataset generally facilitates performance gains, excessive amounts can introduce substantial noise, thereby offsetting the benefits and even degrading performance. Furthermore, larger synthetic configurations entail additional inference and computational costs, raising practical concerns for deployment. In our experiments, we adopt 32 high-quality synthetic samples as the default training configuration, as this choice offers a favorable balance between efficiency and effectiveness. 

ACM Transactions on Intelligent Systems and Technology, Vol. 17, No. 5, Article 106. Publication date: July 2026. 

Z. Zhang et al. 

106:14 


![](P021_images/P021.pdf-0014-02.png)


Fig. 6. The comparison of different synthetic data selection methods on MedInstruct (a) and MedAlpaca (b). Our IFS method more effectively screens higher-quality samples than the other methods. 


![](P021_images/P021.pdf-0014-04.png)


Fig. 7. (a) Convergence analysis of our method and the baseline methods on Alpaca and (b) performances under different Non-IID Settings. 

_4.4.6 Additional Computational Overhead._ Incorporating synthetic data generation into FedIT enhances model performance but introduces additional inference computation and time overhead. Here, we provide additional computational inference time. When evaluating the MedInstruct dataset with an inference batch size of 16, compared to the standard FedIT, our method incurs an average additional time cost of 2.9 minutes per round. Compared with the advanced FewFedWeight, PPFedIT introduces an average overhead of 0.6 minutes per round. The added burden is manageable since inference is lightweight compared to training, and PPFedIT generates minimal synthetic data in each round. Moreover, each client in the federated system can leverage off-the-shelf acceleration frameworks (e.g., vLLM [28]) to enhance inference efficiency, thereby enabling our approach to scale to larger models. For instance, under the same execution environment, employing vLLM for data synthesis introduces an additional latency of approximately 65 seconds for LlaMa2-7B, while LlaMa2-13B requires around 122 seconds. Importantly, PPFedIT significantly enhances training 

ACM Transactions on Intelligent Systems and Technology, Vol. 17, No. 5, Article 106. Publication date: July 2026. 

Privacy-preserving Federated Instruction Tuning with Few-shot Local Examples 

106:15 


![](P021_images/P021.pdf-0015-02.png)



![](P021_images/P021.pdf-0015-03.png)

### Figure analysis

Fig. 8 is a two-panel bar-chart ablation studying synthetic data generation settings in PPFedIT.

**Purpose and context**

- The figure evaluates how two generation hyperparameters affect downstream performance, measured by **Win and Tie Ratio**.
- It appears in the discussion of additional computational overhead and practical trade-offs of synthetic data generation. The surrounding text argues that the added inference cost is acceptable because PPFedIT improves performance and reduces privacy leakage; this figure supports the choice of efficient generation settings by showing where additional demonstrations or synthetic samples stop helping.

**Panel (a): Impact of demonstration sample size**

- Panel label: **(a)**.
- X-axis: **# ICL examples**, with categories **1, 4, 8, 16**.
- Y-axis: **Win and Tie Ratio**, ticked from about **30** to **65**.
- Legend: none; each bar corresponds to one ICL-example count.
- Direct visual observations:
  - Using **1** ICL example gives the lowest win/tie ratio, a little above 40.
  - Increasing to **4** ICL examples produces a large improvement, reaching the mid-50s.
  - Increasing further to **8** and **16** gives only small additional gains, with the bars clustered in the mid-to-high 50s.
- Interpretation:
  - Most of the benefit from in-context demonstrations is obtained by moving from very few demonstrations to a small set of examples.
  - Beyond 4 examples, performance appears to saturate, suggesting diminishing returns from adding more demonstrations.

**Panel (b): Impact of synthetic data volume**

- Panel label: **(b)**.
- X-axis: **# synthetic examples**, with categories **8, 16, 32, 64**.
- Y-axis: **Win and Tie Ratio**, ticked from about **30** to **65**.
- Legend: none; each bar corresponds to one synthetic-example count.
- Direct visual observations:
  - **8** synthetic examples gives the lowest result in this panel, just below 50.
  - **16** examples improves the ratio to the low 50s.
  - **32** examples gives the highest bar, in the mid-50s.
  - **64** examples is lower than 32 examples, though still above 16 examples.
- Interpretation:
  - Moderate synthetic data volume is beneficial, but too much generated data may reduce performance, plausibly because additional generated samples include more noise or lower-quality instructions.
  - The visual optimum among the tested settings is **32 synthetic examples**.

**Overall observation**

- The figure indicates a quality/quantity trade-off in synthetic data generation: a small number of demonstrations is enough to obtain strong gains, and a moderate amount of synthetic data performs better than either too little or too much generated data.


Fig. 8. Impact of demonstration sample size (a) and synthetic data volume (b) during synthetic data generation. 

performance, with improvements ranging from 7% to 13%, and reduces data leakage risk by approximately 20%. _Given the substantial benefits, we argue that these additional computational costs can be deemed acceptable_ . 

## **5 Conclusion** 

This article proposes a _novel_ federated algorithm, PPFedIT, that leverages LLMs’ in-context learning capability to generate task-specific synthetic data, improving federated few-shot performance and against training data extraction attacks. To reduce noise in the synthesized data, we select highquality synthesized data using instruction-following scores and propose parameter isolation training to reduce the effect of noisy data. Inspired by experimental findings that federated aggregation can reduce privacy leakage, we implement local aggregation sharing, which mixes public parameters and private parameters before uploading to the server. Through extensive experiments on three open source datasets, we demonstrate the effectiveness of PPFedIT in enhancing federated few-shot performance while defending against data extraction attacks. Our contributions pave the way for more robust and privacy-preserving FL approaches, particularly in privacy-sensitive domains where data scarcity and privacy concerns are paramount. 

## **References** 

> [1] Martin Abadi, Andy Chu, Ian Goodfellow, H. Brendan McMahan, Ilya Mironov, Kunal Talwar, and Li Zhang. 2016. Deep learning with differential privacy. In _Proceedings of the 2016 ACM SIGSAC Conference on Computer and Communications Security_ , 308–318. 

> [2] Amir Abboud, Kevin Lewi, and Ryan Williams. 2014. Losing weight by gaining edges. In _Proceedings of the European Symposium on Algorithms_ . Springer, 1–12. 

> [3] Iz Beltagy, Matthew E. Peters, and Arman Cohan. 2020. LongFormer: The long-document transformer. arXiv:2004.05150. Retrieved from https://arxiv.org/abs/2004.05150 

- [4] Vadim Borisov, Kathrin Seßler, Tobias Leemann, Martin Pawelczyk, and Gjergji Kasneci. 2022. Language models are realistic tabular data generators. arXiv:2210.06280. Retrieved from https://arxiv.org/abs/2210.06280 

- [5] Hannah Brown, Katherine Lee, Fatemehsadat Mireshghallah, Reza Shokri, and Florian Tramèr. 2022. What does it mean for a language model to preserve privacy? In _Proceedings of the 2022 ACM Conference on Fairness, Accountability, and Transparency_ , 2280–2292. 

- [6] Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D. Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, et al. 2020. Language models are few-shot learners. In _Advances in Neural Information Processing Systems_ , Vol. 33, 1877–1901. 

ACM Transactions on Intelligent Systems and Technology, Vol. 17, No. 5, Article 106. Publication date: July 2026. 

Z. Zhang et al. 

106:16 

- [7] Dongqi Cai, Shangguang Wang, Yaozong Wu, Felix Xiaozhu Lin, and Mengwei Xu. 2023. Federated few-shot learning for mobile NLP. In _Proceedings of the 29th Annual International Conference on Mobile Computing and Networking_ , 1–17. 

- [8] Dongqi Cai, Yaozong Wu, Haitao Yuan, Shangguang Wang, Felix Xiaozhu Lin, and Mengwei Xu. 2023. Towards practical few-shot federated NLP. In _Proceedings of the 3rd Workshop on Machine Learning and Systems_ , 42–48. 

- [9] Nicholas Carlini, Florian Tramer, Eric Wallace, Matthew Jagielski, Ariel Herbert-Voss, Katherine Lee, Adam Roberts, Tom Brown, Dawn Song, Ulfar Erlingsson, et al. 2021. Extracting training data from large language models. In _Proceedings of the 30th USENIX Security Symposium (USENIX Security ’21)_ , 2633–2650. 

- [10] Weilong Dong, Xinwei Wu, Junzhuo Li, Shuangzhi Wu, Chao Bian, and Deyi Xiong. 2022. FewFedWeight: Few-shot federated learning framework across multiple NLP tasks. arXiv:2212.08354. Retrieved from https://arxiv.org/abs/2212. 08354 

- [11] Qianlong Du, Chengqing Zong, and Jiajun Zhang. 2023. MoDS: Model-oriented data selection for instruction tuning. arXiv:2311.15653. Retrieved from https://arxiv.org/abs/2311.15653 

- [12] Yann Dubois, Xuechen Li, Rohan Taori, Tianyi Zhang, Ishaan Gulrajani, Jimmy Ba, Carlos Guestrin, Percy Liang, and Tatsunori B. Hashimoto. 2023. AlpacaFarm: A simulation framework for methods that learn from human feedback. arXiv:2305.14387. Retrieved from https://arxiv.org/abs/2305.14387 

- [13] Cynthia Dwork and Aaron Roth. 2014. The algorithmic foundations of differential privacy. _Foundations and Trends® in Theoretical Computer Science_ 9, 3–4 (2014), 211–407. 

- [14] Tao Fan, Yan Kang, Guoqiang Ma, Weijing Chen, Wenbin Wei, Lixin Fan, and Qiang Yang. 2023. Fate-LLM: A industrial grade federated learning framework for large language models. arXiv:2310.10049. Retrieved from https: //arxiv.org/abs/2310.10049 

- [15] Liam Fowl, Jonas Geiping, Steven Reich, Yuxin Wen, Wojtek Czaja, Micah Goldblum, and Tom Goldstein. 2022. Decepticons: Corrupted transformers breach privacy in federated learning for language models. arXiv:2201.12675. Retrieved from https://arxiv.org/abs/2201.12675 

- [16] Leo Gao, Jonathan Tow, Stella Biderman, Sid Black, Anthony DiPofi, Charles Foster, Laurence Golding, Jeffrey Hsu, Kyle McDonell, Niklas Muennighoff, et al. 2021. A Framework for Few-Shot Language Model Evaluation. Version v0.0.1. Retrieved from https://zenodo.org/records/5371629 

- [17] Tianyu Han, Lisa C. Adams, Jens-Michalis Papaioannou, Paul Grundmann, Tom Oberhauser, Alexander Löser, Daniel Truhn, and Keno K. Bressem. 2023. MedAlpaca—An open-source collection of medical conversational AI models and training data. arXiv:2304.08247. Retrieved from https://arxiv.org/abs/2304.08247 

- [18] Or Honovich, Thomas Scialom, Omer Levy, and Timo Schick. 2022. Unnatural instructions: Tuning language models with (almost) no human labor. arXiv:2212.09689. Retrieved from https://arxiv.org/abs/2212.09689 

- [19] Tzu-Ming Harry Hsu, Hang Qi, and Matthew Brown. 2019. Measuring the effects of non-identical data distribution for federated visual classification. arXiv:1909.06335. Retrieved from https://arxiv.org/abs/1909.06335 

- [20] Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu Chen. 2021. LoRA: Low-rank adaptation of large language models. arXiv:2106.09685. Retrieved from https://arxiv.org/abs/ 2106.09685 

- [21] Xumin Huang, Peichun Li, Hongyang Du, Jiawen Kang, Dusit Niyato, Dong In Kim, and Yuan Wu. 2024. Federated learning-empowered AI-generated content in wireless networks. _IEEE Network_ 38 (2024), 304–313. 

- [22] Yangsibo Huang, Zhao Song, Danqi Chen, Kai Li, and Sanjeev Arora. 2020. TextHide: Tackling data privacy in language understanding tasks. arXiv:2010.06053. Retrieved from https://arxiv.org/abs/2010.06053 

- [23] Di Jin, Eileen Pan, Nassim Oufattole, Wei-Hung Weng, Hanyi Fang, and Peter Szolovits. 2020. What disease does this patient have? A large-scale open domain question answering dataset from medical exams. arXiv:2009.13081. Retrieved from https://arxiv.org/abs/2009.13081 

- [24] Sai Praneeth Karimireddy, Satyen Kale, Mehryar Mohri, Sashank Reddi, Sebastian Stich, and Ananda Theertha Suresh. 2020. Scaffold: Stochastic controlled averaging for federated learning. In _Proceedings of the International Conference on Machine Learning_ . PMLR, 5132–5143. 

- [25] Shiva Prasad Kasiviswanathan, Homin K. Lee, Kobbi Nissim, Sofya Raskhodnikova, and Adam Smith. 2011. What can we learn privately? _SIAM Journal on Computing_ 40, 3 (2011), 793–826. 

- [26] Jakub Konečnỳ, H. Brendan McMahan, Felix X. Yu, Peter Richtárik, Ananda Theertha Suresh, and Dave Bacon. 2016. Federated learning: Strategies for improving communication efficiency. arXiv:1610.05492. Retrieved from https://arxiv.org/abs/1610.05492 

- [27] Weirui Kuang, Bingchen Qian, Zitao Li, Daoyuan Chen, Dawei Gao, Xuchen Pan, Yuexiang Xie, Yaliang Li, Bolin Ding, and Jingren Zhou. 2023. FederatedScope-LLM: A comprehensive package for fine-tuning large language models in federated learning. arXiv:2309.00363. Retrieved from https://arxiv.org/abs/2309.00363 

- [28] Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Sheng, Lianmin Zheng, Cody Hao Yu, Joseph Gonzalez, Hao Zhang, and Ion Stoica. 2023. Efficient memory management for large language model serving with PagedAttention. In _Proceedings of the 29th Symposium on Operating Systems Principles_ , 611–626. 

ACM Transactions on Intelligent Systems and Technology, Vol. 17, No. 5, Article 106. Publication date: July 2026. 

Privacy-preserving Federated Instruction Tuning with Few-shot Local Examples 

106:17 

- [29] Ming Li, Yong Zhang, Zhitao Li, Jiuhai Chen, Lichang Chen, Ning Cheng, Jianzong Wang, Tianyi Zhou, and Jing Xiao. 2023. From quantity to quality: Boosting LLM performance with self-guided data selection for instruction tuning. arXiv:2308.12032. Retrieved from https://arxiv.org/abs/2308.12032 

- [30] Tian Li, Anit Kumar Sahu, Manzil Zaheer, Maziar Sanjabi, Ameet Talwalkar, and Virginia Smith. 2020. Federated optimization in heterogeneous networks. In _Proceedings of Machine Learning and Systems_ , 429–450. 

- [31] Xian Li, Ping Yu, Chunting Zhou, Timo Schick, Luke Zettlemoyer, Omer Levy, Jason Weston, and Mike Lewis. 2023. Self-alignment with instruction backtranslation. arXiv:2308.06259. Retrieved from https://arxiv.org/abs/2308.06259 

- [32] Xuechen Li, Tianyi Zhang, Yann Dubois, Rohan Taori, Ishaan Gulrajani, Carlos Guestrin, Percy Liang, and Tatsunori B. Hashimoto. 2023. AlpacaEval: An Automatic Evaluator of Instruction-Following Models. Retrieved from https: //github.com/tatsu-lab/alpaca_eval 

- [33] Yunshui Li, Binyuan Hui, Xiaobo Xia, Jiaxi Yang, Min Yang, Lei Zhang, Shuzheng Si, Junhao Liu, Tongliang Liu, Fei Huang, et al. 2023. One shot learning as instruction data prospector for large language models. arXiv:2312.10302. Retrieved from https://arxiv.org/abs/2312.10302 

- [34] Bill Yuchen Lin, Chaoyang He, Zihang Zeng, Hulin Wang, Yufen Huang, Christophe Dupuy, Rahul Gupta, Mahdi Soltanolkotabi, Xiang Ren, and Salman Avestimehr. 2021. FedNLP: Benchmarking federated learning methods for natural language processing tasks. arXiv:2104.08815. Retrieved from https://arxiv.org/abs/2104.08815 

- [35] Chin-Yew Lin. 2004. Rouge: A package for automatic evaluation of summaries. In _Proceedings of the Text Summarization Branches Out_ , 74–81. 

- [36] Brendan McMahan, Eider Moore, Daniel Ramage, Seth Hampson, and Blaise Aguera y Arcas. 2017. Communicationefficient learning of deep networks from decentralized data. In _Proceedings of the Artificial Intelligence and Statistics_ . PMLR, 1273–1282. 

- [37] Milad Nasr, Nicholas Carlini, Jonathan Hayase, Matthew Jagielski, A. Feder Cooper, Daphne Ippolito, Christopher A. Choquette-Choo, Eric Wallace, Florian Tramèr, and Katherine Lee. 2023. Scalable extraction of training data from (production) language models. arXiv:2311.17035. Retrieved from https://arxiv.org/abs/2311.17035 

- [38] R OpenAI. 2023. Gpt-4 technical report (View in Article 2). arXiv:230308774. Retrieved from https://arxiv.org/abs/ 2303808774 

- [39] Baolin Peng, Chunyuan Li, Pengcheng He, Michel Galley, and Jianfeng Gao. 2023. Instruction tuning with GPT-4. arXiv:2304.03277. Retrieved from https://arxiv.org/abs/2304.03277 

- [40] Sashank Reddi, Zachary Charles, Manzil Zaheer, Zachary Garrett, Keith Rush, Jakub Konečnỳ, Sanjiv Kumar, and H. Brendan McMahan. 2020. Adaptive federated optimization. arXiv:2003.00295. Retrieved from https://arxiv.org/abs/ 2003.00295 

- [41] Xicong Shen, Yang Liu, Huiqi Liu, Jue Hong, Bing Duan, Zirui Huang, Yunlong Mao, Ye Wu, and Di Wu. 2023. A split-and-privatize framework for large language model fine-tuning. arXiv:2312.15603. Retrieved from https: //arxiv.org/abs/2312.15603 

- [42] Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, et al. 2023. Llama 2: Open foundation and fine-tuned chat models. arXiv:2307.09288. Retrieved from https://arxiv.org/abs/2307.09288 

- [43] Pablo Villalobos, Jaime Sevilla, Lennart Heim, Tamay Besiroglu, Marius Hobbhahn, and Anson Ho. 2022. Will we run out of data? An analysis of the limits of scaling datasets in machine learning. arXiv:2211.04325. Retrieved from https://arxiv.org/abs/2211.04325 

- [44] Peiyi Wang, Lei Li, Liang Chen, Dawei Zhu, Binghuai Lin, Yunbo Cao, Qi Liu, Tianyu Liu, and Zhifang Sui. 2023. Large language models are not fair evaluators. arXiv:2305.17926. Retrieved from https://arxiv.org/abs/2305.17926 

- [45] Yizhong Wang, Yeganeh Kordi, Swaroop Mishra, Alisa Liu, Noah A. Smith, Daniel Khashabi, and Hannaneh Hajishirzi. 2022. Self-instruct: Aligning language model with self generated instructions. arXiv:2212.10560. Retrieved from https://arxiv.org/abs/2212.10560 

- [46] Can Xu, Qingfeng Sun, Kai Zheng, Xiubo Geng, Pu Zhao, Jiazhan Feng, Chongyang Tao, and Daxin Jiang. 2023. WizardLM: Empowering large language models to follow complex instructions. arXiv:2304.12244. Retrieved from https://arxiv.org/abs/2304.12244 

- [47] Rui Ye, Wenhao Wang, Jingyi Chai, Dihan Li, Zexi Li, Yinda Xu, Yaxin Du, Yanfeng Wang, and Siheng Chen. 2024. OpenFedLLM: Training large language models on decentralized private data via federated learning. arXiv:2402.06954. Retrieved from https://arxiv.org/abs/2402.06954 

- [48] Rui Ye, Xinyu Zhu, Jingyi Chai, Siheng Chen, and Yanfeng Wang. 2023. Federated learning empowered by generative content. arXiv:2312.05807. Retrieved from https://arxiv.org/abs/2312.05807 

- [49] Asaf Yehudai, Boaz Carmeli, Yosi Mass, Ofir Arviv, Nathaniel Mills, Assaf Toledo, Eyal Shnarch, and Leshem Choshen. 2024. Genie: Achieving human parity in content-grounded datasets generation. arXiv:2401.14367. Retrieved from https://arxiv.org/abs/2401.14367 

ACM Transactions on Intelligent Systems and Technology, Vol. 17, No. 5, Article 106. Publication date: July 2026. 

Z. Zhang et al. 

106:18 

- [50] Jianyi Zhang, Saeed Vahidian, Martin Kuo, Chunyuan Li, Ruiyi Zhang, Guoyin Wang, and Yiran Chen. 2023. Towards building the federated GPT: Federated instruction tuning. arXiv:2305.05644. Retrieved from https://arxiv.org/abs/ 2305.05644 

- [51] Peiyuan Zhang, Guangtao Zeng, Tianduo Wang, and Wei Lu. 2024. TinyLlama: An open-source small language model. arXiv:2401.02385. Retrieved from https://arxiv.org/abs/2401.02385 

- [52] Xinlu Zhang, Chenxin Tian, Xianjun Yang, Lichang Chen, Zekun Li, and Linda Ruth Petzold. 2023. AlpaCare: Instruction-tuned large language models for medical application. arXiv:2310.14558. Retrieved from https://arxiv.org/ abs/2310.14558 

- [53] Zhuo Zhang, Xiangjing Hu, Jingyuan Zhang, Yating Zhang, Hui Wang, Lizhen Qu, and Zenglin Xu. 2023. FedLegal: The first real-world federated learning benchmark for legal NLP. In _Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Vol. 1: Long Papers)_ , 3492–3507. 

- [54] Zhuo Zhang, Yuanhang Yang, Yong Dai, Qifan Wang, Yue Yu, Lizhen Qu, and Zenglin Xu. 2023. FedPETuning: When federated learning meets the parameter-efficient tuning methods of pre-trained language models. In _Proceedings of the Annual Meeting of the Association of Computational Linguistics 2023_ . Association for Computational Linguistics (ACL), 9963–9977. 

- [55] Haodong Zhao, Wei Du, Fangqi Li, Peixuan Li, and Gongshen Liu. 2023. FedPrompt: Communication-efficient and privacy-preserving prompt tuning in federated learning. In _Proceedings of the ICASSP 2023-2023 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)_ . IEEE, 1–5. 

- [56] Wanru Zhao, Yaxin Du, Nicholas Donald Lane, Siheng Chen, and Yanfeng Wang. 2024. Enhancing data quality in federated fine-tuning of large language models. In _Proceedings of the ICLR 2024 Workshop on Navigating and Addressing Data Problems for Foundation Models_ . 

- [57] Lianmin Zheng, Wei Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin, Zhuohan Li, Dacheng Li, Eric Xing, et al. 2024. Judging LLM-as-a-judge with MT-bench and chatbot arena. In _Proceedings of the 37th International Conference on Neural Information Processing Systems_ . 

## **Appendices** 

## **A Dataset and Training Details** 

Our experiments use three open source instruction datasets, including one open domain Alpaca [39], and two medical domains MedInstruct [52] and MedAlpaca [17]. Alpaca is the popular instruction-following dataset with 52k examples generated by GPT-4 using Alpaca prompts for fine-tuning LLMs. MedInstruct is a diverse, machine-generated medical instruction-following dataset with 52k instances, using GPT-4 and ChatGPT with a high-quality expert-curated seed set. MedAlpaca is an innovative dataset consisting of over 514k entries, specifically crafted to fine-tune LLMs for effective medical applications. We follow Zhao et al. [56] and adopt questionanswering task [23]. These medical datasets are sensitive, involving medical consultations and clinical narratives, thereby serving as realistic proxies for privacy-restricted environments governed by regulations such as HIPAA and GDPR. We downsample these datasets to construct federated few-shot scenarios. Considering the critical role of instruction diversity, we follow previous work using the KMeans algorithm for selection. First, we encoded each instance using the longformer [3], followed by 100 dataset clustering, and finally, selecting 10 (MedInstruct and Alpaca) or five (MedAlpaca) samples from each cluster. 

Our experiments use an open-form assessment for model utility evaluation. For Alpaca, we use the well-known dataset called AlpacaEval [32], which compares the model’s generated responses to Davinci-003 responses. For MedInstruct, we follow Zhang et al. [52] and use MedInstructTest, a dataset their clinicians created, including 216 medical instructions. To be consistent with the previous test method, in MedAlpaca, we randomly selected 400 entries from the remaining data as the test dataset, ensuring no overlap with the training dataset. 

We run a hyperparameter sweep for each dataset and tuning method to make a fair and reasonable comparison. Especially, the learning rate is selected from 3e-4, 2e-3. Following [47], we apply a cosine learning rate schedule according to the round index. For all datasets, we use the Alpaca template to format the instructions. We quantize the backbone model using int8 and enable bfloat16 

ACM Transactions on Intelligent Systems and Technology, Vol. 17, No. 5, Article 106. Publication date: July 2026. 

Privacy-preserving Federated Instruction Tuning with Few-shot Local Examples 

106:19 

to improve computational efficiency. The code will be made publicly available on GitHub after the review process. All experiments are conducted on a server with 2 Nvidia A100 GPUs with 40GB RAM each. 

## **B Prompts** 

_Synthetic Data Generation Prompts._ Figure B1 illustrates the prompts used in synthetic data generation, adapted from Wang et al. [45]. Our approach utilizes Figure B1(a) to generate new INSTRUCTIONS. We randomly sample eight instructions from local data for in-context demonstration. The model is allowed to generate instructions for the new instruction. Figure B1(b) shows the prompt to generate corresponding RESPONSES. We prompt the model with randomly sampled examples followed by the new instruction for the response generation. 


![](P021_images/P021.pdf-0019-05.png)

### Figure analysis

Purpose: The figure documents the exact prompt templates used for synthetic data generation in the paper's privacy-preserving federated instruction tuning workflow.

Panel (a):
- Direct observation: The left rounded box is labeled implicitly as panel “(a)” and begins with “Come up with a series of tasks:”.
- It lists eight existing in-context task instructions: “Task 1: {instruction for existing task 1}” through “Task 8: {instruction for existing task 8}”.
- It ends with “Task 9:”, leaving the ninth task blank for the model to generate.
- Interpretation: This prompt is intended to elicit a new instruction by conditioning the model on eight sampled local instructions.

Panel (b):
- Direct observation: The right rounded box is labeled “(b)” and asks the model to “Come up with examples for the following tasks,” encouraging multiple examples when possible and allowing direct output generation if no additional input is required.
- It includes a placeholder “{EXAMPLES FORM LOCAL DATA}”, likely intended to mean examples from local data.
- It then provides “Task: {INSTRUCTION FOR THE TARGET TASK}”.
- Interpretation: This prompt is used after a target instruction has been generated, asking the model to produce corresponding input/output examples or responses.

Relationship and information flow:
- Panel (a) generates a new target instruction using existing local instructions as demonstrations.
- Panel (b) takes that target instruction and local examples as context to generate synthetic examples or outputs.
- Together, the panels describe a two-stage synthetic data construction pipeline: instruction generation followed by response/example generation.

Connection to surrounding paper text:
- The surrounding appendix text states that Figure B1 illustrates prompts adapted from Wang et al. for synthetic data generation.
- The text explains that eight local instructions are randomly sampled for in-context demonstration in panel (a), and that panel (b) is used to generate corresponding responses for the new instruction.
- This figure supports the paper’s broader method by clarifying how synthetic local training data are created before later quality analysis and filtering.


Fig. B1. The prompts used in our synthetic data generation. (a) Prompt used for generating new instructions. We randomly sample eight instructions from local data for in-context demonstration. The model is allowed to generate instructions for the new instruction. (b) Prompts used for input and output generation given the new instruction. We prompt the model with randomly sampled examples followed by the new instruction for the response generation. 

_GPT4-as-a-Judge Prompt._ Figure B2 illustrates the GPT-4-as-a-Judge prompt used in our experimental evaluation, adapted from the LLMs evaluation prompt introduced by Zheng et al. [57]. To enhance evaluation quality, GPT-4 assesses the output of both methods across four respects: helpfulness, relevance, correctness, and coherence. The average score across these respects is the method’s overall score, determining win, tie, and loss ratios. We conduct two rounds of testing with alternating positional substitutions to mitigate potential positional biases in GPT-4 [44]. 

ACM Transactions on Intelligent Systems and Technology, Vol. 17, No. 5, Article 106. Publication date: July 2026. 

Z. Zhang et al. 

106:20 


![](P021_images/P021.pdf-0020-02.png)

### Figure analysis

The figure is a text-based prompt template for evaluating two model responses, corresponding to Fig. B2 in the surrounding paper text.

- **Purpose:** It documents the prompt used for GPT-4-as-a-Judge evaluation of outputs from PPFedIT and baseline methods.
- **Main components directly visible:**
  - A `# System prompt` section instructs the evaluator to act as an impartial judge.
  - The evaluator is asked to score two AI assistants' responses to a user instruction.
  - Four scoring dimensions are specified: **helpfulness**, **relevance**, **correctness**, and **coherence**.
  - Each dimension is rated on a **1–5 scale**.
  - The prompt explicitly warns against positional bias, response-length bias, and favoritism toward assistant names.
  - A required output format is given for both `output a` and `output b`.
  - An `# Example` section provides an instruction about describing the job “ophthalmologist,” followed by two example outputs and example scores.
  - A `# Task` section introduces the real evaluation instance with placeholders: `{INSTRUCTION_HERE}`, `{OUTPUT_A}`, and `{OUTPUT_B}`.

**Key observations:**

- The visual is not a chart or quantitative plot; it is a shaded rounded rectangle containing a structured evaluation prompt.
- The example rates `Output a` higher than `Output b`, especially for correctness, illustrating how the scoring rubric should distinguish a medically accurate answer from a less accurate or informal one.
- The prompt enforces separate scores for each quality criterion rather than a single holistic score.
- The placeholder fields indicate that the same template is reused across different evaluation instances.

**Connection to the paper text:**

The surrounding text states that this prompt was adapted from prior LLM evaluation work and used to compare PPFedIT with baseline methods. The visual supports that description by showing the exact judge instructions, scoring criteria, example calibration, and response placeholders used in the evaluation protocol.


Fig. B2. GPT4-as-a-Judge prompt for evaluating the outputs of PPFedIT and baseline methods. 

## **C Synthetic Data Analysis** 

We explore the quality of the synthetic data generated. Following Wang et al. [45], we assess whether the data in the synthetic data generation step is correct for each instance regarding instructions, instance inputs, and instance outputs. The review results are shown in Table C1. Although the synthetic data contain errors and noise, most are still correct, which can improve the local model training. This result also reflects the necessity of parameter isolation training and high-quality data filtering. Additionally, we use the generated synthetic data to directly train small LLMs, such as TinyLlama-1.1B [51], to validate the data quality. We use the synthetic data generated on Alpaca and test on the HuggingFace’s OpenLLM evaluation benchmark [16], as shown in Table C2. The experiments demonstrate that the synthetic data generation mechanism we designed can produce helpful instruction-tuning data. 

ACM Transactions on Intelligent Systems and Technology, Vol. 17, No. 5, Article 106. Publication date: July 2026. 

Privacy-preserving Federated Instruction Tuning with Few-shot Local Examples 

106:21 

Table C1. Data Quality Review of the Generated Synthetic Data 

|Qality Review Qestion|Alpaca|MedInstruct|MedAlpaca|
|---|---|---|---|
|Does the instruction||||
|describe a valid task?|91%|88%|85%|
|Is the response appropriate||||
|<br>for the instruction and input?|52%|59%|57%|
|Is the correct format?|56%|66%|53%|



Table C2. The Performance of TinyLlama-1.1B on HuggingFace OpenLLM Benchmark Using Synthetic Data of Alpaca 

||Winogrande|ARC|Hellaswag|TruthfulQA|MMLU|Avg.|
|---|---|---|---|---|---|---|
|Pre-train|57.5|48.1|44.8|37.2|24.2|42.4|
|Ours|60.1|50.5|59.0|39.4|25.6|46.9|



Pre-Train refers to the backbone model without instruction tuning. 

## **D Theoretical Analysis for PPFedIT** 

Benefiting from the local aggregation sharing mechanism, PPFedIT effectively mitigates data extraction attacks while achieving a more favorable tradeoff between performance and privacy protection. To gain a deeper understanding of this privacy-preserving property, we first provide a theoretical analysis demonstrating that local aggregation sharing can approximate differential privacy without requiring explicit noise injection or gradient clipping. Furthermore, we establish that during the federated aggregation phase, this mechanism substantially increases the computational complexity of potential attacks, thereby reinforcing the overall privacy guarantees. 

## **D.1 Differential Privacy Approximation of the Local Aggregation Sharing in PPFedIT** 

_D.1.1 Definitions and Background._ We first provide the definitions and background of local aggregation sharing, adjacent datasets, global sensitivity, and **local differential privacy (LDP)** . _Local Aggregation Sharing_ . Let the local model trained on a private dataset D produce parameters W _푙_ , and the model trained on synthetic data (containing no private information) produce parameters W _푙_ . The local aggregation sharing mechanism combines these two components as: W<sup>_푎_</sup> = _훽_ ∗ W<sup>_푙_</sup> + (1 − _훽_ ) ∗W<sup>_푠_</sup> . _훽_ is a fixed mixing coefficient. A smaller _훽_ implies that a greater proportion of the shared parameters arises from non-private, synthetic data, thereby attenuating the privacy exposure. 

_Adjacent Datasets_ . Two datasets D and D<sup>′</sup> are adjacent if they differ by at most one sample; formally, D<sup>′</sup> can be obtained from D by adding, removing, or replacing a single record [13]. This notion captures the smallest perturbation in an individual client’s data. 

_Global Sensitivity_ . For a deterministic function _푓_ : D → R<sup>_푑_</sup> (e.g., a training algorithm returning model parameters), its global sensitivity is: 


![](P021_images/P021.pdf-0021-13.png)

### Figure analysis

Purpose: This displayed equation formalizes the global sensitivity used in the paper's theoretical privacy analysis of PPFedIT.

Direct observation: The equation is labeled `(D1)` and reads:

\[
\Delta f = \max_{\mathcal{D} \sim \mathcal{D}'} \left\| f(\mathcal{D}) - f(\mathcal{D}') \right\|,
\]

where `\mathcal{D} \sim \mathcal{D}'` denotes adjacent datasets.

Important components:
- `\Delta f`: global sensitivity of the deterministic function `f`.
- `f(\mathcal{D})` and `f(\mathcal{D}')`: outputs of the function on two adjacent datasets.
- `\| \cdot \|`: norm measuring the magnitude of the output change.
- `\max_{\mathcal{D} \sim \mathcal{D}'}`: worst-case change over all adjacent dataset pairs.

Connection to the surrounding text: The surrounding section introduces differential privacy concepts for the local aggregation sharing mechanism in PPFedIT. This equation provides the formal definition of global sensitivity, which is later used to argue that mixing private-data-trained parameters with synthetic-data-trained parameters scales the sensitivity by the mixing coefficient `\beta`.

Interpretation: The equation captures how much a single-record change in a client's private dataset can affect the model parameters returned by a training function. In the paper's later lemma, reducing this sensitivity is central to the claim that local aggregation sharing improves privacy without explicit noise injection.


where D ∼D<sup>′</sup> . Δ _푓_ quantifies the maximum change in the output that can result from modifying a single training record. 

ACM Transactions on Intelligent Systems and Technology, Vol. 17, No. 5, Article 106. Publication date: July 2026. 

Z. Zhang et al. 

106:22 

_LDP_ . A randomized mechanism M satisfies ( _휖,훿_ )-LDP, for any adjacent datasets D, D<sup>′</sup> and measurable subset _푆_ : 


![](P021_images/P021.pdf-0022-03.png)


When _훿_ = 0, the guaranty is pure _휖_ -LDP [13]. This condition ensures that the inclusion or exclusion of any single record changes the output distribution only negligibly, limiting an adversary’s ability to infer the presence of that record [13, 25]. 

_D.1.2 Sensitivity Reduction by Local Aggregation Sharing._ Lemma 1. _Let 푓_ (D) = WD<sup>_푙denote the_</sup> _parameters trained on the private data_ D _, and define the local aggregation parameters_ : 


![](P021_images/P021.pdf-0022-06.png)


_where_ W<sup>_푠_</sup> _is trained solely on synthetic data and is therefore independent of_ D _. Then the global sensitivity of 푔_ (D) _equals 훽 times that of 푓_ (D): 


![](P021_images/P021.pdf-0022-08.png)


Proof. For any adjacent datasets D, D<sup>′</sup> , we have: 


![](P021_images/P021.pdf-0022-10.png)



![](P021_images/P021.pdf-0022-11.png)


Thus, the contribution of any single data sample to the uploaded parameter vector is scaled down by a factor _훽_ . When _훽 <_ 1, each coordinate’s sensitivity decreases proportionally, reducing the dependence of the public parameters on private data. □ 

_D.1.3 Approximate Differential Privacy Guaranty._ Theorem 1. _The local aggregation sharing mechanism approximately satisfies_ ( _휖,훿_ ) _-LDP even without explicit noise injection. For any adjacent datasets_ D _,_ D<sup>′</sup> _the distributions of_ WD<sup>_푎and_W</sup> D<sup>_푎_′</sup><sup>_are statistically close, showing small total-variation_</sup> _(TV) distance, and hence meet an approximate LDP criterion._ 

Proof. In practice, randomness arises inherently from stochastic gradient descent, random initialization, and dropout, making WD<sup>_푙_a random variable. Consequently,</sup><sup>_푊_</sup> D<sup>_푎_=</sup><sup>_훽푊_</sup> D<sup>_푙_+ (1 −</sup><sup>_훽_)</sup><sup>_푊푠_</sup> is also random. Let _푃_ D and _푃_ D<sup>′</sup> denote the probability distributions of _푊_ D<sup>_푎_and</sup><sup>_푊_</sup> D<sup>_푎_′.TheTV</sup> distance is: 


![](P021_images/P021.pdf-0022-15.png)


By Lemma 1, the two random outputs differ by at most ∥WD<sup>_푎_−W</sup> D<sup>_푎_′≤</sup><sup>_훽_ΔW</sup><sup>_푙_∥. Assuming</sup><sup>_푃_D</sup> admits a Lipschitz-continuous density (as in SGD-trained models) [1], such a small shift alters only a tiny portion of probability mass. Therefore, there exists a small constant _훿_ = O( _훽_ ΔW<sup>_푙_</sup> ) such that: 


![](P021_images/P021.pdf-0022-17.png)


By Pinsker’s inequality [13], bounded TV distance implies approximate ( _휖,훿_ ) _-LDP_ : for sufficiently small _훽_ , the two output distributions are virtually indistinguishable to any observer. □ 

ACM Transactions on Intelligent Systems and Technology, Vol. 17, No. 5, Article 106. Publication date: July 2026. 

Privacy-preserving Federated Instruction Tuning with Few-shot Local Examples 

106:23 

_D.1.4 Summary._ The local aggregation sharing mechanism in PPFedIT inherently attenuates per-sample sensitivity, thereby achieving approximate differential privacy without explicit random noise. Formally, 


![](P021_images/P021.pdf-0023-03.png)


Thus, reducing _훽_ directly strengthens privacy. Even without traditional DP noise, this mechanism provides a mathematically grounded privacy-attenuation effect, limiting adversarial information gain and offering provable resistance to training data reconstruction attacks. 

## **D.2 Federated Aggregation and K-Vector Subset Sum** 

In PPFedIT, the mechanism of local aggregation sharing further strengthens privacy protection during the federated aggregation phase. When multiple clients participate, the server receives mixed parameters of the form: 


![](P021_images/P021.pdf-0023-07.png)


where _푘_ denotes the _푘_ th client, and updates the global model W<sup>_푔_</sup> by performing weighted averaging or summation across these mixed parameters. Crucially, each uploaded W<sup>_푎_</sup> represents a linear combination of private and shared parameters, thereby constructing a “multi-vector subset-sum” obfuscation in the aggregation outcome. Specifically, the global update can be expressed as: 


![](P021_images/P021.pdf-0023-09.png)


where _푝푘_ denotes the aggregation weight of the _푘_ th client. From the perspective of the server or a potential adversary, only the mixed vectors and their aggregated result are observable, making it computationally intractable to disentangle individual W _푘_<sup>_푙_and W</sup> _푘_<sup>_푠_.</sup> 

Attempting to recover a client’s pure local parameters W _푘_<sup>_푙_from the mixed representation amounts</sup> to solving a high-dimensional demixing problem: decomposing the known W _푘_<sup>_푎_into W</sup> _푘_<sup>_푙_and W</sup> _푘_<sup>_푠_.</sup> Since W<sup>_푠_</sup> _푘_<sup>is trained from synthetic data unique to each client and unknown to the adversary, it</sup> effectively acts as a client-specific noise mask. Even with knowledge of the mixing formula and the coefficient _훽_ the absence of prior information about W _푘_<sup>_푠_prevents tractable inference. The presence</sup> of multiple clients does not simplify the problem: the adversary must simultaneously solve for _푘_ unrelated mixed vectors, recovering both W _푘_<sup>_푎_and W</sup> _푘_<sup>_푙_for each client.</sup> 

This challenge closely parallels the _k-Vector Subset Sum_ problem [2], a well-known computationally intractable task. As prior work such as TextHide [22] has shown, mixing sensitive data before disclosure forces adversaries to confront an inverse subset-sum problem, whose complexity is exponential in the worst case. Indeed, the k-Vector Subset Sum problem has been proven to be NP-complete, implying that an adversary would require prohibitive supercomputing resources to exhaustively enumerate all possible combinations. Consequently, reconstructing individual clients’ private parameters W _푘_<sup>_푙_within reasonable time is practically infeasible.</sup> 

Received 14 October 2024; revised 10 October 2025; accepted 28 February 2026 

ACM Transactions on Intelligent Systems and Technology, Vol. 17, No. 5, Article 106. Publication date: July 2026. 

