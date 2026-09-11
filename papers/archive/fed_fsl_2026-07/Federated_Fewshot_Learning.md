# **Federated Few-shot Learning** 

Xingbo Fu University of Virginia xf3av@virginia.edu 

Song Wang University of Virginia sw3wv@virginia.edu 

Kaize Ding Arizona State University kaize.ding@asu.edu 

Chen Chen University of Virginia zrh6du@virginia.edu 

Huiyuan Chen Jundong Li Case Western Reserve University University of Virginia hxc501@case.edu jundong@virginia.edu 

## **ABSTRACT** 

_August 6–10, 2023, Long Beach, CA, USA._ ACM, New York, NY, USA, 12 pages. https://doi.org/10.1145/3580305.3599347 

Federated Learning (FL) enables multiple clients to collaboratively learn a machine learning model without exchanging their own local data. In this way, the server can exploit the computational power of all clients and train the model on a larger set of data samples among all clients. Although such a mechanism is proven to be effective in various fields, existing works generally assume that each client preserves sufficient data for training. In practice, however, certain clients may only contain a limited number of samples (i.e., few-shot samples). For example, the available photo data taken by a specific user with a new mobile device is relatively rare. In this scenario, existing FL efforts typically encounter a significant performance drop on these clients. Therefore, it is urgent to develop a few-shot model that can generalize to clients with limited data under the FL scenario. In this paper, we refer to this novel problem as _federated few-shot learning_ . Nevertheless, the problem remains challenging due to two major reasons: the global data variance among clients (i.e., the difference in data distributions among clients) and the local data insufficiency in each client (i.e., the lack of adequate local data for training). To overcome these two challenges, we propose a novel federated few-shot learning framework with two separately updated models and dedicated training strategies to reduce the adverse impact of global data variance and local data insufficiency. Extensive experiments on four prevalent datasets that cover news articles and images validate the effectiveness of our framework compared with the state-of-the-art baselines. Our code is provided<sup>1</sup> . 

## **1 INTRODUCTION** 

The volume of valuable data is growing massively with the rapid development of mobile devices [4, 34]. Recently, researchers have developed various machine learning methods [5, 58, 62] to analyze and extract useful information from such large-scale real-world data. Among these methods, Federated Learning (FL) is an effective solution, which aims to collaboratively optimize a centralized model over data distributed across a large number of clients [7, 13, 22, 63]. In particular, FL trains a global model on a server by aggregating the local models learned on each client [2]. Moreover, by avoiding the direct exchange of private data, FL can provide effective protection of local data privacy for clients [31]. As an example, in Google Photo Categorization [12, 33], the server aims to learn an image classification model from photos distributed among a large number of clients, i.e., mobile devices. In this case, FL can effectively conduct learning tasks without revealing private photos to the server. 

In fact, new learning tasks (e.g., novel photo classes) are constantly emerging over time [51, 60]. In consequence, FL can easily encounter a situation where the server needs to solve a new task with limited available data as the reference. In the previous example of Google Photo Categorization, as illustrated in Fig. 1, the server may inevitably need to deal with novel photo classes such as the latest electronic products, where only limited annotations are available. Nevertheless, existing FL works generally assume sufficient labeled samples for model training, which inevitably leads to unsatisfying classification performance for new tasks with limited labeled samples [14]. Therefore, to improve the practicality of FL in realistic scenarios, it is important to solve this problem by learning an FL model that can achieve satisfactory performance on new tasks with limited samples. In this paper, we refer to this novel problem setting as _federated few-shot learning_ . 

## **CCS CONCEPTS** 

### • **Computing methodologies** → **Distributed algorithms** . 

## **KEYWORDS** 

Federated Learning; Few-shot Learning; Knowledge Distillation 

#### **ACM Reference Format:** 

Song Wang, Xingbo Fu, Kaize Ding, Chen Chen, Huiyuan Chen, and Jundong Li. 2023. Federated Few-shot Learning. In _Proceedings of the 29th ACM SIGKDD Conference on Knowledge Discovery and Data Mining (KDD ’23),_ 

Recently, many few-shot learning frameworks [15, 45, 53, 56] have been proposed to deal with new tasks with limited samples. Typically, the main idea is to learn meta-knowledge from _base classes_ with abundant samples (e.g., photo classes such as portraits). Then such meta-knowledge is generalized to _novel classes_ with limited samples (e.g., photo classes such as new electronic products), where novel classes are typically disjoint from base classes. However, as illustrated in Fig. 1, it remains challenging to conduct few-shot learning under the federated setting due to the following reasons. First, due to the _global data variance_ (i.e., the differences in data distributions across clients), the aggregation of local models on the server side will disrupt the learning of meta-knowledge in each 

1https://github.com/SongW-SW/F2L 

Permission to make digital or hard copies of part or all of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for third-party components of this work must be honored. For all other uses, contact the owner/author(s). _KDD ’23, August 6–10, 2023, Long Beach, CA, USA_ © 2023 Copyright held by the owner/author(s). ACM ISBN 979-8-4007-0103-0/23/08. https://doi.org/10.1145/3580305.3599347 

KDD ’23, August 6–10, 2023, Long Beach, CA, USA 

Song Wang et al. 


![](P022_images/P022.pdf-0002-02.png)

### Figure analysis

The figure is a conceptual diagram motivating the problem setting of federated few-shot learning using Google Photo Categorization as an example.

- **Main components directly shown:**
  - A central **Server** at the top, represented by a cloud icon with synchronization arrows.
  - Multiple distributed clients labeled **Client 1**, **Client 2**, an ellipsis indicating additional clients, and **Client I**.
  - Image-card icons in different colors representing photo classes.
  - Labels for **Base Class Photos** and **Novel Class Photos** near the top.
  - Dotted arrows from the server toward clients, indicating federated communication or model aggregation/distribution.
  - Downward arrows from client data blocks to two named challenges: **Local Data Insufficiency** and **Global Data Variance**.

- **Panel/flow description:**
  - The server coordinates multiple clients without centralizing their raw photo data.
  - Each client contains only a small subset of class examples, visually indicated by a few colored photo icons inside each client box.
  - The class compositions differ across clients: for example, clients contain different mixtures of blue, green, purple, and pink photo icons.
  - The ellipsis between Client 2 and Client I indicates the setting generalizes to many participating clients.

- **Key observations:**
  - **Local data insufficiency** is visually represented by each client having only a limited number of photo examples, which is problematic for learning transferable meta-knowledge in few-shot learning.
  - **Global data variance** is visually represented by different clients holding different class distributions, including varied combinations of base-class-like and novel-class-like photo icons.
  - The diagram contrasts centralized meta-learning assumptions with a federated setting where data are fragmented and heterogeneous.

- **Interpretation connected to the paper text:**
  - The surrounding text explains that few-shot learning normally learns meta-knowledge from abundant **base classes** and transfers it to limited **novel classes**.
  - In the federated setting, the paper argues that two additional challenges arise: client-level data scarcity and non-IID distribution differences across clients.
  - This figure visually supports that motivation by showing that federated aggregation may combine clients with different local class distributions, while each individual client may lack enough data to learn robust meta-knowledge.


_knowledge distillation_ ). In this manner, each client can leverage the beneficial knowledge in other clients to learn meta-knowledge from more data. In summary, our contributions are as follows: 

- **Problem** . We investigate the challenges of learning metaknowledge in the novel problem of federated few-shot learning from the perspectives of _global data variance_ and _local data insufficiency_ . We also discuss the necessity of tackling these challenges. 

- **Method** . We develop a novel federated few-shot learning framework F<sup>2</sup> L with three essential strategies: (1) a decoupled meta-learning framework to mitigate disruption from the aggregated model on the server; (2) mutual information maximization for local-to-global knowledge transfer; (3) a novel partial knowledge distillation strategy for global-tolocal knowledge distillation. 

- **Experiments** . We conduct experiments on four few-shot classification datasets covering both news articles and images under the federated scenario. The results further demonstrate the superiority of our proposed framework. 

**Figure 1: The two challenges of federated few-shot learning as an example in Google Photo Categorization: local data insufficiency and global data variance.** 

## **2 PRELIMINARIES** 

client [23]. Generally, the meta-knowledge is locally learned from different classes in each client and thus is distinct among clients, especially under the non-IID scenario, where the data variance can be even larger among clients compared with the IID scenario. Since the server will aggregate the local models from different clients and then send back the aggregated model, the learning of meta-knowledge in each client will be potentially disrupted. Second, due to the _local data insufficiency_ in clients, it is non-trivial to learn meta-knowledge from each client. In FL, each client only preserves a relatively small portion of the total data [1, 13]. However, meta-knowledge is generally learned from data in a variety of classes [15, 53]. As a result, it is difficult to learn meta-knowledge from data with less variety, especially in the non-IID scenario, where each client only has a limited amount of classes. 

To effectively solve the aforementioned challenges, we propose a novel **<u>F</u>** <u>ederated</u> **<u>F</u>** <u>ew-shot</u> **<u>L</u>** <u>earning framework, named F</u><sup>2</sup> L. First, we propose a decoupled meta-learning framework to mitigate the disruption from the aggregated model on the server. Specifically, the proposed framework retains a unique _client-model_ for each client to learn meta-knowledge and a shared _server-model_ to learn client-invariant knowledge (e.g., the representations of samples), as illustrated in Fig. 2. Specifically, the client-model in each client is updated locally and will not be shared across clients, while the servermodel can be updated across clients and sent to the server for aggregation. Such a design decouples the learning of meta-knowledge (via client-model) from learning client-invariant knowledge (via server-model). In this way, we can mitigate the disruption from the aggregated model on the server caused by global data variance among clients. Second, to compensate for local data insufficiency in each client, we propose to leverage global knowledge learned from all clients with two dedicated update strategies. In particular, we first transfer the learned meta-knowledge in client-model to server-model by maximizing the mutual information between their output (i.e., _local-to-global knowledge transfer_ ). Then we propose a partial knowledge distillation strategy for each client to selectively extract useful knowledge from server-model (i.e., _global-to-local_ 

## **2.1 Problem Definition** 

In FL, given a set of _𝐼_ clients, i.e., {C<sup>(</sup><sup>_𝑖_)</sup> } _𝑖_<sup>_𝐼_</sup> =1<sup>, where</sup><sup>_𝐼_is the number</sup> of clients, each C<sup>(</sup><sup>_𝑖_)</sup> owns a local dataset D<sup>(</sup><sup>_𝑖_)</sup> . The main objective of FL is to learn a global model over data across all clients (i.e., {D<sup>(</sup><sup>_𝑖_)</sup> } _𝑖_<sup>_𝐼_</sup> =1<sup>) without the direct exchange of data among clients. Fol-</sup> lowing the conventional FL strategy [13, 32, 36], a server S will aggregate locally learned models from all clients for a global model. 

Under the prevalent few-shot learning scenario, we consider a supervised setting in which the data samples for client C<sup>(</sup><sup>_𝑖_)</sup> are from its local dataset: ( _𝑥,𝑦_ ) ∈D<sup>(</sup><sup>_𝑖_)</sup> , where _𝑥_ is a data sample, and _𝑦_ is the corresponding label. We first denote the entire set of classes on all clients as C. Depending on the number of labeled samples in each class, C can be divided into two categories: base classes C _𝑏_ and novel classes C _𝑛_ , where C = C _𝑏_ ∪C _𝑛_ and C _𝑏_ ∩C _𝑛_ = ∅. In general, the number of labeled samples in C _𝑏_ is sufficient, while it is generally small in C _𝑛_ [15, 45]. Correspondingly, each local dataset can be divided into a base dataset D _𝑏_<sup>(</sup><sup>_𝑖_)</sup> = {( _𝑥,𝑦_ ) ∈D<sup>(</sup><sup>_𝑖_)</sup> : _𝑦_ ∈C _𝑏_ } and a novel dataset D _𝑛_<sup>(</sup><sup>_𝑖_)</sup> = {( _𝑥,𝑦_ ) ∈D<sup>(</sup><sup>_𝑖_)</sup> : _𝑦_ ∈C _𝑛_ }. In the few-shot setting, the evaluation of the model generalizability to novel classes C _𝑛_ is conducted on D _𝑛_<sup>(</sup><sup>_𝑖_), which contains only limited</sup> labeled samples. The data samples in D _𝑏_<sup>(</sup><sup>_𝑖_)</sup> will be used for training. Then we can formulate the studied problem of federated few-shot learning as follows: 

Definition 1. **_Federated Few-shot Learning:_** _Given a set of 𝐼 clients_ {C<sup>(</sup><sup>_𝑖_)</sup> } _𝑖_<sup>_𝐼_</sup> =1<sup>_and aserver_S</sup><sup>_, federatedfew-shot learning aims_</sup> _to learn a global model after aggregating model parameters locally learned from_ D _𝑏_<sup>(</sup><sup>_𝑖_)</sup> _in each client such that the model can accurately predict labels for unlabeled samples (i.e., query set_ Q _) in_ D _𝑛_<sup>(</sup><sup>_𝑖_)</sup> _with only a limited number of labeled samples (i.e., support set_ S _)._ 

More specifically, if the support set S consists of exactly _𝐾_ labeled samples for each of _𝑁_ classes from D _𝑛_<sup>(</sup><sup>_𝑖_), and the query set Q</sup> is sampled from the same _𝑁_ classes, the problem is defined as Federated _𝑁_ -way _𝐾_ -shot Learning. Essentially, the objective of federated 

KDD ’23, August 6–10, 2023, Long Beach, CA, USA 

Federated Few-shot Learning 

few-shot learning is to learn a globally shared model across clients that can be fast adapted to data samples in D _𝑛_<sup>(</sup><sup>_𝑖_)</sup> with only limited labeled samples. Therefore, the crucial part is to effectively learn meta-knowledge from the base datasets {D _𝑏_<sup>(</sup><sup>_𝑖_)}</sup> _𝑖_<sup>_𝐼_</sup> =1<sup>inallclients.</sup> Such meta-knowledge is generalizable to novel classes unseen during training and thus can be utilized to classify data samples in each D _𝑛_<sup>(</sup><sup>_𝑖_), which consists of only limited labeled samples.</sup> 

## **2.2 Episodic Learning** 

In practice, we adopt the prevalent episodic learning framework for model training and evaluation, which has proven to be effective in various few-shot learning scenarios [9, 10, 41, 53, 57]. Specifically, the model evaluation (i.e., meta-test) is conducted on a certain number of _meta-test tasks_ , where each task contains a small number of labeled samples as references and unlabeled samples for classification. The local model training (i.e., meta-training) process in each client is similarly conducted on a specific number of _meta-training_ tasks, where each task mimics the structure of meta-test tasks. It is worth mentioning that meta-training tasks are sampled from the local base dataset D _𝑏_<sup>(</sup><sup>_𝑖_)</sup> of each client, while meta-test tasks are sampled from the local novel dataset D _𝑛_<sup>(</sup><sup>_𝑖_).Thatbeingsaid,the</sup> class set of samples in meta-training tasks is a subset of C _𝑏_ , while the class set of samples in meta-test tasks is a subset of C _𝑛_ , which is distinct from C _𝑏_ . The main idea of federated few-shot learning is to preserve the consistency between meta-training and meta-test so that the model can learn meta-knowledge from clients for better generalization performance to novel classes C _𝑛_ . 

Specifically, to construct a meta-training task T in client C<sup>(</sup><sup>_𝑖_)</sup> from its local base dataset D<sup>(</sup><sup>_𝑖_)</sup> _𝑏_<sup>, we first randomly sample</sup><sup>_𝑁_classes</sup> from D<sup>(</sup><sup>_𝑖_)</sup> _𝑏_<sup>. Then we randomly select</sup><sup>_𝐾_samples from each of the</sup><sup>_𝑁_</sup> classes (i.e., _𝑁_ -way _𝐾_ -shot) to establish the support set S. Similarly, the query set Q consists of _𝑄_ different samples (distinct from S) from the same _𝑁_ classes. The components of the meta-training task T is formulated as follows: 


![](P022_images/P022.pdf-0003-06.png)


where _𝑥𝑖_ (or _𝑞𝑖_ ) is a data sample in the sampled _𝑁_ classes, and _𝑦𝑖_ (or _𝑦𝑖_<sup>′) is the corresponding label. Note that during meta-test,</sup> each meta-test task shares a similar structure to meta-training tasks, except that the samples are from the local novel dataset D _𝑛_<sup>(</sup><sup>_𝑖_), which</sup> are distinct from D<sup>(</sup><sup>_𝑖_)</sup> _𝑏_<sup>.</sup> 

## **3 METHODOLOGY** 

In this part, we introduce the overall design of our proposed framework F<sup>2</sup> L in detail. Specifically, we formulate the _federated fewshot learning_ problem under the prevailing _𝑁_ -way _𝐾_ -shot learning framework. Our target of conducting federated few-shot learning is to learn meta-knowledge from a set of _𝐼_ clients {C<sup>(</sup><sup>_𝑖_)</sup> } _𝑖_<sup>_𝐼_</sup> =1<sup>with</sup> different data distributions, and generalize such meta-knowledge to meta-test tasks. Nevertheless, it remains difficult to conduct federated few-shot learning due to the challenging issues of global data 

variance and local data insufficiency as mentioned before. Therefore, as illustrated in Fig 2, we propose a decoupled meta-learning framework to mitigate disruption from the servers. We further propose two update strategies to leverage global knowledge. The overview process is presented in Fig 3. 

## **3.1 Decoupled Meta-Learning Framework** 

_3.1.1 Federated Learning Framework._ We consider a server-model, which consists of an encoder _𝑞𝜙_ and a classifier _𝑓𝜙_ that are shared among clients. We denote the overall model parameters in the server-model as _𝜙_ . Specifically, _𝑞𝜙_ : R<sup>_𝑑_</sup> → R<sup>_𝑘_</sup> is a function that maps each sample into a low-dimensional vector h _𝜙_ ∈ R<sup>_𝑘_</sup> , where _𝑑_ is the input feature dimension, and _𝑘_ is the dimension of learned representations. Taking the representation h _𝜙_ as input, the classifier _𝑓𝜙_ : R<sup>_𝑘_</sup> →C _𝑏_ maps each h _𝜙_ to the label space of base classes C _𝑏_ and outputs the prediction p _𝜙_ ∈ R<sup>| C</sup><sup>_𝑏_|</sup> , where each element in p _𝜙_ denotes the classification probability regarding each class in C _𝑏_ . 

Following the prevalent FedAvg [36] strategy for FL, the training of server-model is conducted on all clients through _𝑇_ rounds. In each round _𝑡_ , the server S first sends the server-model parameters _𝜙_ to all clients, and each client will conduct a local meta-training process on _𝜏_ randomly sampled meta-training tasks. Then the server S will perform aggregation on parameters received from clients: 


![](P022_images/P022.pdf-0003-14.png)

### Figure analysis

The page does not contain a conventional plotted figure; it contains two separate numbered displayed equations embedded in the methodology text.

- **Equation (1): episodic few-shot task construction.**
  - Directly shown definitions:
    \[
    \mathcal{S}=\{(x_1,y_1),(x_2,y_2),\ldots,(x_{N\times K},y_{N\times K})\},
    \]
    \[
    \mathcal{Q}=\{(q_1,y'_1),(q_2,y'_2),\ldots,(q_Q,y'_Q)\},
    \]
    \[
    \mathcal{T}=\{\mathcal{S},\mathcal{Q}\}.
    \]
  - Important components: support set \(\mathcal{S}\), query set \(\mathcal{Q}\), and meta-training task \(\mathcal{T}\).
  - The surrounding text explains that \(\mathcal{S}\) is formed by sampling \(N\) classes and \(K\) labeled examples per class, giving \(N\times K\) support samples, while \(\mathcal{Q}\) contains separate query samples from the same sampled classes.
  - Direct observation: the equation formalizes each task as a pair of support and query sets.
  - Interpretation: this establishes the episodic learning setup used to align meta-training on local base classes with meta-testing on local novel classes.

- **Equation (2): federated averaging of server-model parameters.**
  - Directly shown definition:
    \[
    \phi^{t+1}=\frac{1}{I}\sum_{i=1}^{I}\widetilde{\phi}_i^{t}.
    \]
  - Important components: \(I\) clients, round index \(t\), locally updated server-model parameters \(\widetilde{\phi}_i^t\), and aggregated server-model parameters \(\phi^{t+1}\).
  - Direct observation: the server computes a simple average of client-updated model parameters.
  - Interpretation: this is the FedAvg-style global update used for the shared server-model before the paper motivates adding separate client-specific models to preserve local meta-knowledge.

Together, the two equations connect the paper’s problem setup to its method: Equation (1) defines the few-shot episodic tasks used locally, while Equation (2) defines the federated aggregation mechanism for the shared model across clients.


where _𝜙_<sup>�</sup> _𝑖_<sup>_𝑡_denotes the locally updated server-model parameters by</sup> client C<sup>(</sup><sup>_𝑖_)</sup> on round _𝑡_ . _𝜙_<sup>_𝑡_+1</sup> denotes the aggregated server-model parameters which will be distributed to clients at the beginning of the next round. In this way, the server can learn a shared model for all clients in a federated manner. 

Although the standard strategy of learning a single shared model for all clients achieves decent performance on general FL tasks [13, 36], it can be suboptimal for federated few-shot learning. Due to the global data variance among clients, the aggregated model on the server will disrupt the learning of meta-knowledge in each client [23]. As a result, the local learning of meta-knowledge in clients will become more difficult. In contrast, we propose to further introduce a client-model, which is uniquely learned and preserved by each client, to locally learn meta-knowledge. In other words, its model parameters will not be sent back to the server for aggregation. In this manner, we can separate the learning of client-model (metaknowledge) and server-model (client-invariant knowledge) so that the learning of meta-knowledge is not disrupted. 

Specifically, for client C<sup>(</sup><sup>_𝑖_)</sup> , the client-model also consists of an encoder _𝑞𝜓𝑖_ and a classifier _𝑓𝜓𝑖_ . We denote the overall model parameters in the client-model for client C<sup>(</sup><sup>_𝑖_)</sup> as _𝜓𝑖_ . In particular, the encoder _𝑞𝜓𝑖_ takes the representation h _𝜙_ learned by the encoder _𝑞𝜙_ in server-model as input, and outputs a hidden representation h _𝜓_ ∈ R<sup>_𝑘_</sup> . Such a design ensures that the client-model encoder _𝑞𝜓𝑖_ does not need to process the raw sample and thus can be a small model, which is important when clients only preserve limited computational resources [6]. Then the classifier _𝑓𝜓𝑖_ maps h _𝜓_ to predictions p _𝜓_ ∈ R<sup>_𝑁_</sup> of the _𝑁_ classes. 

KDD ’23, August 6–10, 2023, Long Beach, CA, USA 

Song Wang et al. 


![](P022_images/P022.pdf-0004-02.png)


**Figure 2: The illustration of our decoupled meta-learning framework.** _𝜓_ **denotes the client-model, which will be locally kept in each client.** _𝜙_ **denotes the server-model, which will be aggregated and sent to the server.** 

_3.1.2 Local Meta-training on Clients._ Based on the episodic learning strategy, in each round, the training process of each client C<sup>(</sup><sup>_𝑖_)</sup> is conducted through _𝜏_ steps, where each step is a local update based on a meta-training task randomly sampled from the local base dataset D<sup>(</sup><sup>_𝑖_)Inparticular,forclientC(</sup><sup>_𝑖_)onround</sup> _𝑏_<sup>.</sup> _𝑡_ = 1 _,_ 2 _, . . . ,𝑇_ and step _𝑠_ = 1 _,_ 2 _, . . . ,𝜏_ , we denote the sampled metatask as T _𝑖_<sup>_𝑡,𝑠_</sup> = {S _𝑖_<sup>_𝑡,𝑠,_Q</sup> _𝑖_<sup>_𝑡,𝑠_}. To learn meta-knowledge from meta-</sup> task T _𝑖_<sup>_𝑡,𝑠_</sup> , we adopt the prevalent MAML [15] strategy to update client-model in one fine-tuning step and one meta-update step. We first fine-tune the client-model to fast adapt it to support set S _𝑖_<sup>_𝑡,𝑠_:</sup> 


![](P022_images/P022.pdf-0004-05.png)


where L _𝑓𝑡_ is the fine-tuning loss, which is the cross-entropy loss calculated on the support set S _𝑖_<sup>_𝑡,𝑠_. Here,</sup><sup>_𝛼𝑓𝑡_is the learning rate,</sup> and _𝜓𝑖_<sup>_𝑡,𝑠_</sup> (or _𝜙𝑖_<sup>_𝑡,𝑠_) denotes the parameters of client-model (or server-</sup> model) on round _𝑡_ and step _𝑠_ . Then we update the client-model based on the query set Q _𝑖_<sup>_𝑡,𝑠_:</sup> 


![](P022_images/P022.pdf-0004-07.png)


where L _𝜓_ is the loss for client-model on the query set Q _𝑖_<sup>_𝑡,𝑠_, and</sup><sup>_𝛼𝜓_</sup> is the meta-learning rate for _𝜓_ . In this regard, we can update clientmodel with our global-to-local knowledge distillation strategy. For the update of server-model, we conduct one step of update based on the support set and parameters of client-model: 


![](P022_images/P022.pdf-0004-09.png)


where L _𝜙_ is the loss for the server-model, and _𝛼𝜙_ is the metalearning rate for _𝜙_ . In this manner, we can update the server-model with our local-to-global knowledge transfer strategy. After repeating the above updates for _𝜏_ steps, the final parameters of servermodel _𝜙𝑖_<sup>_𝑡,𝜏_</sup> is used as _𝜙_<sup>�</sup> _𝑖_<sup>_𝑡_in Eq. (2) and sent back to the server for</sup> aggregation, while the client-model (with parameters _𝜓𝑖_<sup>_𝑡,𝜏_</sup> ) will be kept locally. By doing this, we can decouple the learning of local 

meta-knowledge in client-model while learning client-invariant knowledge in server-model to avoid disruption from the server. 

## **3.2 Local-to-Global Knowledge Transfer** 

With our decoupled meta-learning framework, we can mitigate the disruption to the learning of local meta-knowledge in each client. Nevertheless, we still need to transfer the learned meta-knowledge to server-model (i.e., Local-to-global Knowledge Transfer), so that it can be further leveraged by other clients to handle the local data insufficiency issue. Specifically, to effectively transfer local meta-knowledge, we propose to maximize the mutual information between representations learned from server-model encoder _𝑞𝜙_ and client-model encoder _𝑞𝜓_ . In this way, the server-model can maximally absorb the information in the learned local meta-knowledge. 

_3.2.1 Mutual Information Maximization._ Given a meta-training task T = {S _,_ Q}, as described in Sec. 3.1, the server-model encoder _𝑞𝜙_ and client-model encoder _𝑞𝜓_ will output h _𝜙_ and h _𝜓_ for each sample, respectively. By stacking the learned representations of samples in the support set S (|S| = _𝐷_ , where _𝐷_ = _𝑁_ × _𝐾_ ), we can obtain the representations of support samples learned by the servermodel, i.e., H _𝜙_ ∈ R<sup>_𝐷_×</sup><sup>_𝑘_</sup> , and the client-model, i.e., H _𝜓_ ∈ R<sup>_𝐷_×</sup><sup>_𝑘_</sup> . For simplicity, we omit the annotations of round _𝑡_ , step _𝑠_ , and client _𝑖_ . The objective of maximizing the information between H _𝜙_ and H _𝜓_ can be formally represented as follows: 


![](P022_images/P022.pdf-0004-15.png)


where h<sup>_𝑖_</sup> _𝜙_<sup>(or h</sup> _𝜓_<sup>_𝑖_) is the</sup><sup>_𝑖_-th row of H</sup><sup>_𝜙_(or H</sup><sup>_𝜓_). Since the mutual</sup> information _𝐼_ (H _𝜙_ ; H _𝜓_ ) is difficult to obtain and thus infeasible to be maximized [40], we re-write it to achieve a more feasible form: 


![](P022_images/P022.pdf-0004-17.png)


Since the support set S of size _𝐷_ is randomly sampled, we can assume that the prior probability _𝑝_ (h<sup>_𝑗_follows a uniform dis-</sup> _𝜓_<sup>;</sup><sup>_𝜙_)</sup> tribution, and set it as _𝑝_ (h<sup>_𝑗_=1/</sup><sup>_𝐷_.AccordingtotheBayes’</sup> _𝜓_<sup>;</sup><sup>_𝜙_)</sup> theorem, the Eq. (7) becomes: 


![](P022_images/P022.pdf-0004-19.png)

### Figure analysis

The figure's purpose is to explain the paper's decoupled meta-learning framework for federated few-shot learning.

Direct visual observations:
- A central **Server** is shown with a cloud icon and a server-model parameter block labeled **φ**.
- Multiple clients are shown as light-blue boxes: **Client 1**, **Client 2**, an ellipsis, and **Client I**.
- Each client contains two model blocks:
  - A client-specific model labeled **ψ₁**, **ψ₂**, …, **ψᵢ**.
  - A server-model copy labeled **φ**.
- The legend defines:
  - **ψᵢ** as the **Client-model**.
  - **φ** as the **Server-model**.
  - Solid arrows as **Send to Client**.
  - Dotted arrows as **Send to Server**.
- Solid arrows point from the server-side φ model down to client-side φ models, indicating distribution of the server-model to clients.
- Dotted arrows point upward from client-side φ models toward the server-side φ model, indicating that updated server-model parameters are returned to the server for aggregation.
- No arrows indicate that ψᵢ client-models are sent to the server.

Interpretation:
- The diagram separates two kinds of knowledge: the shared **server-model φ**, which is exchanged and aggregated, and the private **client-model ψᵢ**, which remains local to each client.
- This visual structure supports the paper's claim that local meta-knowledge is preserved in each client-model and is not disrupted by server aggregation.
- The server-model appears to represent client-invariant knowledge, while each client-model represents client-specific meta-knowledge.

Connection to surrounding text:
- The adjacent text explains that standard federated learning aggregates one shared model, which can be suboptimal for federated few-shot learning because global data variance may disrupt local meta-knowledge.
- The figure concretely depicts the proposed solution: each client maintains its own ψᵢ while participating in federated aggregation only through φ.
- The following text describes local meta-training and later local-to-global knowledge transfer, which build on this architecture by updating the client-model locally while transferring useful information into the server-model.


_3.2.2 Estimation of 𝑝_ (h<sup>_𝑖_Sincetheclient-modelisfine-</sup> _𝜙_<sup>|h</sup> _𝜓_<sup>_𝑗_;</sup><sup>_𝜙_)</sup><sup>_._</sup> tuned on the support set S of the meta-task T , we can leverage the classification results of the client-model to estimate _𝑝_ (h<sup>_𝑖_</sup> _𝜙_<sup>|h</sup> _𝜓_<sup>_𝑗_;</sup><sup>_𝜙_).</sup> We denote _𝐶_ ( _𝑗_ ) as the set of sample indices in the support set S that shares the same class as the _𝑗_ -th sample (including itself), i.e., _𝐶_ ( _𝑗_ ) ≡{ _𝑘_ : _𝑦𝑘_ = _𝑦 𝑗 ,𝑘_ = 1 _,_ 2 _, . . . , 𝐷_ }. Here, we first set _𝑝_ (h<sup>_𝑖_= 0 for all</sup><sup>_𝑖_∉</sup><sup>_𝐶_(</sup><sup>_𝑗_), since we assume the client-model</sup> _𝜙_<sup>|h</sup> _𝜓_<sup>_𝑗_;</sup><sup>_𝜙_)</sup> can only infer representations from the same class. Intuitively, in the 

KDD ’23, August 6–10, 2023, Long Beach, CA, USA 

Federated Few-shot Learning 


![](P022_images/P022.pdf-0005-02.png)



![](P022_images/P022.pdf-0005-03.png)



![](P022_images/P022.pdf-0005-04.png)



![](P022_images/P022.pdf-0005-05.png)


**Figure 3: An illustration of the overall process of our framework F**<sup>2</sup> **L. Specifically, each client receives the server-model from the server at the beginning of each round. To perform one step of local update, each client first samples a meta-task (2-way 2-shot in the illustration), which consists of a support set and a query set, from the local data. Then the server-model and the client-model will both compute output for the support samples and query samples. After that, the server-model and the client-model are updated via mutual information maximization and knowledge distillation, respectively. Finally, the server-model is sent back to the server for aggregation, while the client-model is locally preserved by each client.** 

case of _𝑖_ ∈ _𝐶_ ( _𝑗_ ), which means the _𝑖_ -th and the _𝑗_ -th samples share the same class, _𝑝_ (h<sup>_𝑖_can be considered as the confidence of</sup> _𝜙_<sup>|h</sup> _𝜓_<sup>_𝑗_;</sup><sup>_𝜙_)</sup> client-model regarding the class of the _𝑗_ -the sample. Therefore, it should reflect the degree to which the sample representation h<sup>_𝑗_</sup> _𝜓_<sup>is</sup> relevant to its class. Utilizing the client-model classification output (i.e., normalized class probabilities) for the _𝑖_ -th sample p<sup>_𝑖_</sup> _𝜓_<sup>∈R</sup><sup>_𝑁_,</sup> we can compute _𝑝_ (h<sup>_𝑖_as follows:</sup> _𝜙_<sup>|h</sup> _𝜓_<sup>_𝑗_;</sup><sup>_𝜙_)</sup> 


![](P022_images/P022.pdf-0005-08.png)


where p<sup>_𝑖_∈R denotes the classification probability for the</sup><sup>_𝑖_-th</sup> _𝜓_<sup>(</sup><sup>_𝑦𝑗_)</sup> sample regarding class _𝑦 𝑗_ ( _𝑦𝑖_ = _𝑦 𝑗_ when _𝑖_ ∈ _𝐶_ ( _𝑗_ )). 

_3.2.3 Estimation of 𝑝_ (h<sup>_𝑗_Nextweelaborateonhowto</sup> _𝜓_<sup>|h</sup><sup>_𝑖_</sup> _𝜙_<sup>;</sup><sup>_𝜙_)</sup><sup>_._</sup> estimate _𝑝_ (h<sup>_𝑗_</sup> _𝜓_<sup>|h</sup><sup>_𝑖_</sup> _𝜙_<sup>;</sup><sup>_𝜙_). Although we can similarly leverage the clas-</sup> sification results of the server-model, such a strategy lacks generalizability. This is because the server-model aims at classifying all base classes instead of the _𝑁_ classes in each meta-training task. We instead propose to estimate _𝑝_ (h<sup>_𝑗_based on the Euclidean</sup> _𝜓_<sup>|h</sup><sup>_𝑖_</sup> _𝜙_<sup>;</sup><sup>_𝜙_)</sup> distance (divided by 2 for simplicity) between learned representations of the server-model and the client-model. Specifically, we normalize the distances with a softmax function: 


![](P022_images/P022.pdf-0005-11.png)


Then if we further apply the _ℓ_ 2 normalization to both h<sup>_𝑖_</sup> _𝜙_<sup>and</sup> h<sup>_𝑗_∥h</sup><sup>_𝑖_=1 −h</sup><sup>_𝑖_</sup> _𝜓_<sup>, we can obtain</sup> _𝜙_<sup>−h</sup> _𝜓_<sup>_𝑗_∥</sup> 2<sup>2/2</sup> _𝜙_<sup>· h</sup> _𝜓_<sup>_𝑗_. Moreover, since</sup> the value of<sup>�</sup> _𝑖_<sup>_𝐷_</sup> =1 � _𝐷𝑗_ =1<sup>_𝑝_(h</sup><sup>_𝑖_</sup> _𝜙_<sup>|h</sup> _𝜓_<sup>_𝑗_;</sup><sup>_𝜙_) equals a constant</sup><sup>_𝐷_, the term</sup> 

� _𝑖𝐷_ =1 � _𝐷𝑗_ =1<sup>_𝑝_(h</sup><sup>_𝑖_</sup> _𝜙_<sup>|h</sup> _𝜓_<sup>_𝑗_;</sup><sup>_𝜙_) · log(</sup><sup>_𝐷_)/</sup><sup>_𝐷_in Eq. (8) is also a constant and</sup> thus can be ignored in the objective: 


![](P022_images/P022.pdf-0005-14.png)


Combining the above equations, the optimal server-model parameter _𝜙_<sup>∗</sup> for the final optimization objective (i.e., max _𝜙 𝐼_ (H _𝜙_ ; H _𝜓_ )) can be obtained as follows: 


![](P022_images/P022.pdf-0005-16.png)


Here L _𝑀𝐼_ is defined as follows: 


![](P022_images/P022.pdf-0005-18.png)


where we exchange the order of summation over _𝑖_ and _𝑗_ for clarity. It is noteworthy that L _𝑀𝐼_ is different from the InfoNCE loss [18, 40], which considers different augmentations of samples, while L _𝑀𝐼_ focuses on the classes of samples in S. Moreover, L _𝑀𝐼_ also differs from the supervised contrastive loss [25], which combines various augmentations of samples and label information. In contrast, our loss targets at transferring the meta-knowledge by maximally preserving the mutual information between representations learned by the server-model and the client-model. More differently, the term p _𝜓_<sup>_𝑖_(</sup><sup>_𝑦𝑗_)/�</sup> _𝑘_ ∈ _𝐶_ ( _𝑗_ )<sup>p</sup> _𝜓_<sup>_𝑘_(</sup><sup>_𝑦𝑗_) acts as an adjustable weight that measures</sup> the importance of a sample to its class. Combining the objective 

KDD ’23, August 6–10, 2023, Long Beach, CA, USA 

Song Wang et al. 

described in Eq. (13) and the standard cross-entropy loss, we can obtain the final loss for the server-model: 


![](P022_images/P022.pdf-0006-03.png)


where L _𝐶𝐸_ (S) is defined as follows: 


![](P022_images/P022.pdf-0006-05.png)


where p<sup>_𝑖_∈R denotes the classification probability for the</sup><sup>_𝑖_-th</sup> _𝜙_<sup>(</sup><sup>_𝑐𝑗_)</sup> support sample belonging to the _𝑗_ -th class _𝑐 𝑗_ in C _𝑏_ , computed by the server-model. Here _𝑦𝑐_<sup>_𝑖_</sup> _𝑗_ = 1 if the _𝑖_ -th support sample belongs to _𝑐 𝑗_ , and _𝑦𝑐_<sup>_𝑖_</sup> _𝑗_ = 0, otherwise. Moreover, _𝜆𝑀𝐼_ ∈[0 _,_ 1] is an adjustable hyper-parameter to control the weight of L _𝑀𝐼_ . 

## **3.3 Global-to-Local Knowledge Distillation** 

With the learned meta-knowledge in each client transferred from the client-model to the server-model, other clients can leverage such meta-knowledge to deal with the local data insufficiency issue. However, since each meta-task only contains _𝑁_ classes, directly extracting meta-knowledge in the server-model can inevitably involve meta-knowledge from other classes, which can be harmful to the learning of local meta-knowledge from these _𝑁_ classes in each client. Instead, we propose a partial knowledge distillation strategy to selectively extract useful knowledge from the server-model, i.e., global-to-local knowledge distillation. 

_3.3.1 Partial Knowledge Distillation._ Specifically, we focus on the output classification probabilities of the server-model regarding the _𝑁_ classes in support set S while ignoring other classes. In this regard, we can extract the information that is crucial for learning local meta-knowledge from these _𝑁_ classes and also reduce the irrelevant information from other classes. 

Particularly, we consider the same meta-task T = {S _,_ Q}. We denote the output probabilities for the _𝑖_ -th query sample _𝑞𝑖_ in Q (with label _𝑦𝑖_ ) of the server-model and the client-model as p<sup>_𝑖_</sup> _𝜙_<sup>∈R| C</sup><sup>_𝑏_|and</sup> 

p<sup>_𝑖_</sup> _𝜓_<sup>∈R</sup><sup>_𝑁_, respectively. It is noteworthy that the</sup><sup>_𝑁_classes in this</sup> meta-task, denoted as C _𝑚_ , are sampled from the base classes C _𝑏_ (i.e., |C _𝑚_ | = _𝑁_ and C _𝑚_ ⊂C _𝑏_ ). Therefore, the output of server-model (i.e., p<sup>_𝑖_</sup> _𝜙_<sup>) will include the probabilities of classes in C</sup><sup>_𝑚_. In particu-</sup> lar, we enforce the probabilities of in C _𝑚_ from the client-model to be consistent with the probabilities of the same classes from the server-model. As a result, the learning of local meta-knowledge can leverage the information of data in the same _𝑁_ classes from other clients, which is encoded in the server-model. In this regard, we can handle the local data insufficiency issue by involving information from other clients while reducing the irrelevant information from other classes not in C _𝑚_ . In particular, by utilizing the output of the server-model as the soft target for the client-model, we can achieve an objective as follows: 


![](P022_images/P022.pdf-0006-12.png)


where _𝑐 𝑗_ is the _𝑗_ -th class in C _𝑚_ (i.e., the _𝑁_ classes in meta-task T ). q<sup>_𝑖_</sup> _𝜙_<sup>(</sup><sup>_𝑐𝑗_) and q</sup> _𝜓_<sup>_𝑖_(</sup><sup>_𝑐𝑗_) are the knowledge distillation values for</sup><sup>_𝑐𝑗_from</sup> 

server-model and client-model, respectively. Specifically, the values of q<sup>_𝑖_and q</sup><sup>_𝑖_are obtained via the softmax normalization:</sup> _𝜙_<sup>(</sup><sup>_𝑐𝑗_)</sup> _𝜓_<sup>(</sup><sup>_𝑐𝑗_)</sup> 


![](P022_images/P022.pdf-0006-15.png)


where z<sup>_𝑖_are z</sup><sup>_𝑖_</sup> _𝜙_<sup>(</sup><sup>_𝑐𝑗_)</sup> _𝜓_<sup>(</sup><sup>_𝑐𝑗_)) are the logits (i.e., output before softmax</sup> normalization) of class _𝑐 𝑗_ from server-model and client-model, respectively. _𝑇𝑖_ is the temperature parameter for the _𝑖_ -th query sample. In this way, we can ensure that<sup>�</sup><sup>_𝑁_</sup> _𝑗_ =1<sup>q</sup><sup>_𝑖_</sup> _𝜙_<sup>(</sup><sup>_𝑐𝑗_)= �</sup><sup>_𝑁_</sup> _𝑗_ =1<sup>q</sup> _𝜓_<sup>_𝑖_(</sup><sup>_𝑐𝑗_)= 1.</sup> 

_3.3.2 Adaptive Temperature Parameter._ Generally, a larger value of _𝑇𝑖_ denotes that the client-model focuses more on extracting information from the other classes in C _𝑚_ [19] (i.e., { _𝑐_ | _𝑐_ ∈C _𝑚,𝑐_ ≠ _𝑦𝑖_ }), denoted as negative classes. Since the classification results can be erroneous in the server-model, we should adaptively adjust the value of _𝑇𝑖_ for each meta-task to reduce the adverse impact of extracting misleading information from the server-model. However, although negative classes can inherit useful information for classification, such information is generally noisier when the output probabilities of these negative classes are smaller. Therefore, to estimate the importance degree of each negative class, we consider the maximum output logit for negative classes to reduce potential noise. Particularly, if the probability of a negative class from the server-model is significantly larger than other classes, we can conjecture that this class is similar to _𝑦𝑖_ and thus potentially contains the crucial information to distinguish them. Specifically, the temperature parameter _𝑇𝑖_ for the _𝑖_ -th query sample _𝑞𝑖_ is computed as follows: 


![](P022_images/P022.pdf-0006-18.png)


where _𝜎_ (·) denotes the Sigmoid function, and _𝑦𝑖_ is the label of _𝑞𝑖_ . In this way, the temperature parameter _𝑇𝑖_ will increase when the ratio between the largest probability in negative classes and the probability for _𝑦𝑖_ is larger. As a result, the client-model will focus more on the negative class information. Then by further incorporating the cross-entropy loss on the query set Q, we can obtain the final loss for the client-model: 


![](P022_images/P022.pdf-0006-20.png)


where L _𝐶𝐸_ (Q) is defined as follows: 


![](P022_images/P022.pdf-0006-22.png)


where p<sup>_𝑖_is the probability of the</sup><sup>_𝑖_-th query sample belonging</sup> _𝜓_<sup>(</sup><sup>_𝑐𝑗_)</sup> to class _𝑐 𝑗_ computed by the client-model. _𝑦𝑐_<sup>_𝑖_</sup> _𝑗_ = 1 if the _𝑖_ -th query sample belongs to _𝑐 𝑗_ , and _𝑦𝑐_<sup>_𝑖_</sup> _𝑗_ = 0, otherwise. Moreover, _𝜆𝐾𝐷_ ∈ [0 _,_ 1] is an adjustable hyper-parameter to control the weight of L _𝐾𝐷_ . In this manner, the client-model can selectively learn useful knowledge from both the local and global perspectives, i.e., globalto-local knowledge distillation. 

KDD ’23, August 6–10, 2023, Long Beach, CA, USA 

Federated Few-shot Learning 

## **3.4 Overall Learning Process** 

With the proposed losses L _𝜙_ and L _𝜓_ , on each round, we can conduct meta-training on each client C<sup>(</sup><sup>_𝑖_)</sup> by sampling _𝜏_ meta-training tasks from the local base dataset D<sup>(</sup><sup>_𝑖_)Thedetailedprocessis</sup> _𝑏_<sup>.</sup> described in Algorithm 1. After _𝑇_ rounds of meta-training on all the clients, we have obtained a model that accommodates comprehensive meta-knowledge for federated few-shot learning. For the meta-test phase, since we have aggregated learned local metaknowledge from each client to the server-model, we can leverage the server-model to generate data representations for classification. Specifically, during evaluation, for each meta-test task T = {S _,_ Q} sampled from local novel datasets {D _𝑛_<sup>(</sup><sup>_𝑖_)}</sup> _𝑖_<sup>_𝐼_</sup> =1<sup>in all clients, we follow</sup> the same process as meta-training including fine-tuning, except that the meta-update process is omitted. The output of the client-model will be used for classification. 

## **4 EXPERIMENTS** 

In this part, we conduct extensive experiments to evaluate our framework F<sup>2</sup> L on four few-shot classification datasets covering both news articles and images under the federated scenario. 

## **4.1 Datasets** 

In this section, we introduce four prevalent real-world datasets used in our experiments, covering both news articles and images: **20 Newsgroup** [28], **Huffpost** [38, 39], **FC100** [41], and **miniImageNet** [53]. In particular, 20 Newsgroup and Huffpost are online news article datasets, while FC100 and miniImageNet are image datasets. The details are as follows: 

- **20 Newsgroup** [28] is a text dataset that consists of informal discourse from news discussion forums. There are 20 classes for documents in this dataset, where each class belongs to one of six top-level categories. The classes are split as 8/5/7 for training/validation/test, respectively. 

- **Huffpost** [38, 39] is a text dataset containing news headlines published on HuffPost<sup>2</sup> between 2012 and 2018. Generally, the headlines are significantly shorter and less grammatical than the 20 Newsgroup dataset. Moreover, each headline belongs to one of 41 classes, which are then split as 20/5/16 for training/validation/test, respectively. 

- **FC100** [41] is an image classification dataset based on CIFAR100 [27]. Specifically, this dataset contains 100 image classes, where each class maintains 600 images with a low 32 × 32 resolution. The classes are split as 60/20/20 for training/validation/test, respectively. 

- **miniImageNet** [53] is an image dataset extracted from the full ImageNet dataset [8]. This dataset consists of 100 image classes, and each class maintains 600 images with a resolution of 84 × 84. The classes are split as 64/16/20 for training/validation/test, respectively. 

## **4.2 Experimental Settings** 

To validate the performance of our framework F<sup>2</sup> L, we conduct experiments with the following baselines for a fair comparison: 

2https://www.huffpost.com/ 

- _Local_ . This baseline is non-distributed, which means we train an individual model for each client on the local data. The meta-test process is conducted on all meta-test tasks, and the averaged results of all models are reported. 

- _FL-MAML_ . This baseline leverages the MAML [15] strategy to perform meta-learning on each client. The updated model parameters will be sent back to the server for aggregation. 

- _FL-Proto_ . This baseline uses ProtoNet [45] as the model in each client. The classification is based on the Euclidean distances between query samples and support samples. 

- _FedFSL_ [14]. This method combines MAML and an adversarial learning strategy [17, 44] to construct a consistent feature space. The aggregation is based on FedAvg [36]. 

During meta-training, we perform updates for the client-model and the server-model according to Algorithm 1. Finally, the servermodel that achieves the best result on validation will be used for meta-test. Then during meta-test, we evaluate the server-model on a series of 100 randomly sampled meta-test tasks from local novel datasets {D _𝑛_<sup>(</sup><sup>_𝑖_)}</sup> _𝑖_<sup>_𝐼_</sup> =1<sup>in all clients. For consistency, the class</sup> split of C _𝑏_ and C _𝑛_ is identical for all baseline methods. The classification accuracy over these meta-test tasks will be averaged as the final results. The specific parameter settings are provided in Appendix C.3. For the specific choices for the encoder and classifier in server-model and client-model (i.e., _𝑞𝜙_ , _𝑓𝜙_ , _𝑞𝜓_ , and _𝑓𝜓_ ) and model parameters, we provide further details in Appendix C.1. Note that for a fair comparison, we utilize the same encoder for all methods. 

## **4.3 Overall Evaluation Results** 

We present the overall performance comparison of our framework and baselines on federated few-shot learning in Table 1. Specifically, we conduct experiments under two few-shot settings: 5-way 1- shot and 5-way 5-shot. Moreover, to demonstrate the robustness of our framework under different data distributions, we partition the data in both IID and non-IID settings. For the IID partition, the samples of each class are uniformly distributed to all clients. For non-IID partition, we follow the prevailing strategy [21, 61] and distribute samples to all clients based on the Dirichlet distribution with its concentration parameter set as 1.0. The evaluation metric is the average classification accuracy over ten repetitions. From the overall results, we can obtain the following observations: 

- Our framework F<sup>2</sup> L outperforms all other baselines on various news article and image datasets under different few-shot settings (1-shot and 5-shot) and data distributions (IID and non-IID). The results validate the effectiveness of our framework on federated few-shot learning. 

- Conventional few-shot methods such as Prototypical Network [45] and MAML [15] exhibit similar performance compared with the Local baseline. The result demonstrates that directly applying few-shot methods to federated learning brings less competitive improvements over local training. This is because such methods are not proposed for federated learning and thus lead to unsatisfactory training performance under the federated setting. 

- The performance of all methods degrades at different extents when the data distribution is changed from IID to non-IID. The main reason is that the variety of classes in each client 

KDD ’23, August 6–10, 2023, Long Beach, CA, USA 

Song Wang et al. 

**Table 1: The overall federated few-shot learning results of various models on four datasets under IID and Non-IID settings (5-way), where accuracy and standard deviation are reported in** % **. The best results are presented as bold.** 

|Dataset||20 New|sgroup|||Huf|post||
|---|---|---|---|---|---|---|---|---|
|Distribution<br>|II<br>|D<br>|Non<br>|-IID<br>|II<br>|D<br>|Non<br>|-IID<br>|
|Setting|1-shot|5-shot|1-shot|5-shot|1-shot|5-shot|1-shot|5-shot|
|Local|31_._53±1_._68|42_._73±1_._51|29_._64±1_._81|41_._01±2_._40|34_._02±1_._67|49_._95±1_._54|33_._09±2_._28|47_._18±1_._43|
|FL-MAML|32_._89±1_._86|44_._34±1_._66|31_._60±1_._44|43_._84±1_._97|37_._47±1_._43|52_._85±1_._43|36_._01±2_._17|50_._56±2_._08|
|FL-Proto|35_._62±2_._07|46_._04±1_._92|32_._79±1_._41|43_._82±1_._85|37_._87±1_._23|51_._90±1_._43|34_._05±1_._35|50_._52±1_._33|
|FedFSL|36_._56±1_._41|46_._37±1_._82|35_._84±1_._49|45_._89±1_._72|39_._18±1_._42|53_._81±1_._36|37_._86±1_._46|52_._18±1_._82|
|F<sup>2</sup>L|39_._80±1_._80|49_._64±1_._32|39_._00±1_._36|49_._44±1_._98|42_._12±2_._12|57_._88±2_._17|41_._64±1_._81|57_._12±1_._87|
|Dataset||FC|100|||miniIm|ageNet||
|Distribution<br>|II<br>|D<br>|Non<br>|-IID<br>|II<br>|D<br>|Non<br>|-IID<br>|
|Setting|1-shot|5-shot|1-shot|5-shot|1-shot|5-shot|1-shot|5-shot|
|Local|33_._45±1_._68|50_._89±1_._56|32_._40±1_._76|50_._29±2_._24|47_._82±1_._68|64_._30±1_._59|46_._81±2_._03|64_._06±1_._45|
|FL-MAML|34_._10±1_._29|50_._66±1_._68|36_._06±1_._78|50_._35±1_._57|49_._74±1_._40|65_._55±1_._57|47_._64±1_._36|63_._56±1_._13|
|FL-Proto|36_._11±1_._49|54_._74±2_._05|35_._54±1_._71|52_._31±1_._76|51_._32±1_._41|66_._67±2_._06|50_._82±1_._82|65_._09±1_._90|
|FedFSL|39_._38±1_._95|52_._25±1_._84|38_._60±2_._00|53_._90±1_._80|55_._75±2_._06|70_._59±1_._97|53_._52±2_._01|69_._56±1_._86|
|F<sup>2</sup>L|42_._52±2_._06|58_._60±2_._09|42_._56±2_._25|59_._52±2_._14|56_._72±1_._79|74_._23±2_._32|56_._16±2_._05|73_._24±2_._02|




![](P022_images/P022.pdf-0008-04.png)

### Figure analysis

The figure presents an ablation study of the proposed F²L framework on two datasets, comparing the full method against three variants with individual components removed.

**Purpose and connection to the paper text:** The surrounding text explains that the variants remove: the decoupled framework (`F²L\M`), the local-to-global knowledge transfer module (`F²L\T`), or the global-to-local knowledge distillation loss (`F²L\A`). The figure visually supports the claim that all three designs contribute to performance, with the full F²L model outperforming each ablated variant.

**Panel (a): FC100**

- The panel is labeled **“(a) FC100”**.
- The y-axis is **Test Accuracy (%)**, spanning roughly 35% to 60%.
- The x-axis has four federated few-shot settings: **I-1**, **N-1**, **I-5**, and **N-5**, where I/N denote IID/non-IID and the number denotes shots.
- The legend compares four methods: `F²L\M`, `F²L\T`, `F²L\A`, and full `F²L`.
- Direct visual observation: the full `F²L` bar is highest for all four settings.
- Direct visual observation: 5-shot settings have substantially higher accuracy than 1-shot settings for all variants.
- Direct visual observation: ablated variants trail the full model, with visible gaps especially in the 1-shot settings.
- Interpretation: the consistent advantage of full F²L indicates that the decoupled framework, local-to-global transfer, and global-to-local distillation each contribute to improved federated few-shot learning performance.

**Panel (b): Huffpost**

- The panel is labeled **“(b) Huffpost”**.
- The y-axis is **Test Accuracy (%)**, also shown in percent over a similar range.
- The x-axis again contains **I-1**, **N-1**, **I-5**, and **N-5** settings.
- The same four legend entries are used: `F²L\M`, `F²L\T`, `F²L\A`, and full `F²L`.
- Direct visual observation: full `F²L` is highest across all four settings.
- Direct visual observation: performance is higher in 5-shot than in 1-shot conditions.
- Direct visual observation: non-IID conditions remain competitive but still show sensitivity to component removal.
- Interpretation: the result aligns with the paper’s statement that the proposed framework helps mitigate challenges from complex client data distributions, particularly through knowledge transfer and the decoupled design.

**Overall visual comparison:** Across both datasets and all IID/non-IID 1-shot/5-shot conditions, the full F²L method consistently achieves the tallest bar. No exact numeric values are printed on the bars, so only relative comparisons are directly recoverable from the figure.


strategy so that the client-model will also be sent to the server for aggregation. We refer to this variant as _F_<sup>2</sup> _L\M_ . Second, we remove the local-to-global knowledge transfer module so that the metaknowledge in the client-model will be effectively transferred to the server-model. This variant is referred to as _F_<sup>2</sup> _L\T_ . Third, we eliminate the global-to-local knowledge distillation loss. In this way, the client-model cannot leverage the global knowledge in the server-model for learning meta-knowledge. We refer to this variant as _F_<sup>2</sup> _L\A_ . The overall ablation study results are presented in Fig. 4. From the results, we observe that F<sup>2</sup> L outperforms all variants, which verifies the effectiveness of the three designs in F<sup>2</sup> L. Specifically, removing the design of local-to-global knowledge transfer leads to significant performance degradation. This result demonstrates that such a design can effectively aggregate learned meta-knowledge among clients and thus bring performance improvements. More significantly, without our decoupled strategy, the performance deteriorates rapidly when federated few-shot learning is conducted in the non-IID scenario. This phenomenon verifies the importance of mitigating the disruption from the server in the presence of complex data distributions among clients. 

**Figure 4: Ablation study of our framework on FC100 and Huffpost. I-** _𝐾_ **(or N-** _𝐾_ **) denotes the setting of 5-way** _𝐾_ **-shot under IID (or non-IID) distributions. M denotes the decoupled framework, T means the local-to-global knowledge transfer, and A demotes the global-to-local knowledge distillation.** 

results in a more complex class distribution and brings difficulties to the classification task. Nevertheless, by effectively transferring the meta-knowledge among clients, our framework is capable of alleviating such a problem under the non-IID scenario. 

- When increasing the value of _𝐾_ (i.e., more support samples in each class), all methods achieve considerable performance gains. In particular, our framework F<sup>2</sup> L obtains better results compared to other baselines, due to our decoupled metalearning framework, which promotes the learning of metaknowledge in the support samples. 

## **4.5 Parameter Sensitivity Study** 

_4.5.1 Effect of 𝜆𝑀𝐼 and 𝜆𝐾𝐷 ._ In this section, we further conduct experiments to study the sensitivity of several parameters in our framework F<sup>2</sup> L. During the process of transferring and achieving meta-knowledge, we introduce two novel losses L _𝑀𝐼_ and L _𝐾𝐷_ , respectively, along with the traditional cross-entropy loss. To empirically evaluate the impact brought by different values of _𝜆𝑀𝐼_ and _𝜆𝐾𝐷_ in Eq. (14) and Eq. (20) , we adjust the values of _𝜆𝑀𝐼_ and _𝜆𝐾𝐷_ from 0 to 1 and present the results in Fig 5. From the results, we can observe that the performance generally increases with a 

## **4.4 Ablation Study** 

In this part, we conduct an ablation study on FC100 and Huffpost to validate the effectiveness of three crucial designs in F<sup>2</sup> L (similar results observed in other datasets). First, we remove the decoupled 

KDD ’23, August 6–10, 2023, Long Beach, CA, USA 

Federated Few-shot Learning 


![](P022_images/P022.pdf-0009-02.png)


**Figure 5: The results with different values of** _𝜆𝑀𝐼_ **and** _𝜆𝐾𝐷_ **on Huffpost under the non-IID setting.** 

**Figure 6: The results of non-IID federated 1-shot and 5-shot learning on FC100 regarding the number of clients.** 

larger value of _𝜆𝑀𝐼_ , while decreasing with _𝜆𝑀𝐼_ approaches 1. The results indicate the importance of transferring learned local metaknowledge, while also demonstrating that the cross-entropy loss is necessary. On the other hand, the performance first increases and then degrades when a larger value of _𝜆𝐾𝐷_ is presented. That being said, although partial knowledge distillation can enable each client to benefit from the global data, a larger _𝜆𝐾𝐷_ can potentially lead to more irrelevant information when learning local meta-knowledge. 

_4.5.2 Effect of Client Number._ In this section, we study the robustness of our framework under the scenario with a varying number of clients. In particular, we keep the total training data unchanged, which means with more clients participating in the training process, each client preserves fewer training samples. As a result, the training performance will be inevitably reduced. Specifically, we partition the total training data into _𝐼_ = 1 _,_ 2 _,_ 5 _,_ 10 _,_ 20 _,_ and 50 clients. Note that _𝐼_ = 1 denotes the setting of completely centralized training. The results on FC100 with 1-shot and 5-shot settings are presented in Fig 6 (we have similar results for other datasets and omit them for brevity). From the results, we can observe that all methods encounter a performance drop in the presence of more clients. Nevertheless, our framework F<sup>2</sup> L can reduce the adverse impact brought by more clients through effectively leveraging the global knowledge learned from all clients. In consequence, the performance degradation is less significant for F<sup>2</sup> L. 

## **5 RELATED WORK** 

## **5.1 Few-shot Learning** 

The objective of Few-shot Learning (FSL) is to learn transferable meta-knowledge from tasks with abundant information and generalize such knowledge to novel tasks that consist of only limited labeled samples [9, 11, 46, 50, 57]. Existing few-shot learning works can be divided into two categories: _metric-based_ methods and _optimization-based_ methods. The metric-based methods target 

at learning generalizable metric functions to classify query samples by matching them with support samples [35, 47, 55]. For instance, Prototypical Networks [45] learn a prototype representation for each class and conduct predictions based on the Euclidean distances between query samples and the prototypes. Relation Networks [47] learn relation scores for classification in a non-linear manner. On the other hand, optimization-based approaches generally optimize model parameters based on the gradients calculated from few-shot samples [24, 37, 42, 54]. As an example, MAML [15] proposes to optimize model parameters based on gradients on support samples to achieve fast generalization. In addition, LSTM-based metalearner [42] adjusts the step size to adaptively update parameters during meta-training. 

## **5.2 Federated Learning** 

Federated Learning (FL) enables multiple clients to collaboratively train a model without exchanging the local data explicitly [16, 22, 30, 48, 59, 64]. As a classic example, FedAvg [36] performs stochastic gradient descent (SGD) on each client to update model parameters and send them to the server. The server averages the received model parameters to achieve a global model for the next round. FedProx [32] incorporates a proximal term into the local update of each client to reduce the distance between the global model and the local model. To deal with the non-IID problem in FL, recent works also focus on personalization in FL [1, 3, 13, 49]. For instance, FedMeta [6] incorporates MAML [15] into the local update process in each client for personalization. FedRep [7] learns shared representations among clients. Moreover, FedFSL [14] proposes to combine MAML and an adversarial learning strategy [17, 44] to learn a consistent feature space. 

## **6 CONCLUSION** 

In this paper, we study the problem of federated few-shot learning, which aims at learning a federated model that can achieve satisfactory performance on new tasks with limited labeled samples. Nevertheless, it remains difficult to perform federated few-shot learning due to two challenges: global data variance and local data insufficiency. To tackle these challenges, we propose a novel federated few-shot learning framework F<sup>2</sup> L. In particular, we handle global data variance by decoupling the learning of local meta-knowledge. Then we leverage the global knowledge that is learned from all clients to tackle the local data insufficiency issue. We conduct extensive experiments on four prevalent few-shot learning datasets under the federated setting, covering both news articles and images. The experimental results further validate the superiority of our framework F<sup>2</sup> L over other state-of-the-art baselines. 

## **7 ACKNOWLEDGEMENTS** 

The work in this paper is supported by the National Science Foundation under grants (IIS-2006844, IIS-2144209, IIS-2223769, CNS2154962, and BCS-2228534), the Commonwealth Cyber Initiative awards (VV-1Q23- 007 and HV-2Q23-003), the JP Morgan Chase Faculty Research Award, the Cisco Faculty Research Award, the Jefferson Lab subcontract 23-D0163, and the UVA 4-VA collaborative research grant. 

KDD ’23, August 6–10, 2023, Long Beach, CA, USA 

Song Wang et al. 

## **REFERENCES** 

- [1] Manoj Ghuhan Arivazhagan, Vinay Aggarwal, Aaditya Kumar Singh, and Sunav Choudhary. 2019. Federated learning with personalization layers. _arXiv:1912.00818_ (2019). 

- [2] Christopher Briggs, Zhong Fan, and Peter Andras. 2020. Federated learning with hierarchical clustering of local updates to improve training on non-IID data. In _IJCNN_ . 

- [3] Duc Bui, Kshitiz Malik, Jack Goetz, Honglei Liu, Seungwhan Moon, Anuj Kumar, and Kang G Shin. 2019. Federated user representation learning. _arXiv:1909.12535_ (2019). 

- [4] Soumen Chakrabarti. 2002. _Mining the Web: Discovering knowledge from hypertext data_ . Morgan Kaufmann. 

- [5] Michael Chau and Hsinchun Chen. 2008. A machine learning approach to web page filtering using content and structure analysis. _Decision Support Systems_ 44, 2 (2008), 482–494. 

- [6] Fei Chen, Mi Luo, Zhenhua Dong, Zhenguo Li, and Xiuqiang He. 2018. Federated meta-learning with fast convergence and efficient communication. _arXiv:1802.07876_ (2018). 

- [7] Liam Collins, Hamed Hassani, Aryan Mokhtari, and Sanjay Shakkottai. 2021. Exploiting shared representations for personalized federated learning. In _ICLR_ . 

- [8] Jia Deng, Wei Dong, Richard Socher, Li-Jia Li, Kai Li, and Li Fei-Fei. 2009. Imagenet: A large-scale hierarchical image database. In _CVPR_ . 

- [9] Kaize Ding, Jianling Wang, Jundong Li, Kai Shu, Chenghao Liu, and Huan Liu. 2020. Graph prototypical networks for few-shot learning on attributed networks. In _CIKM_ . 

- [10] Kaize Ding, Qinghai Zhou, Hanghang Tong, and Huan Liu. 2021. Few-shot network anomaly detection via cross-network meta-learning. In _TheWebConf_ . 

- [11] Simon S Du, Wei Hu, Sham M Kakade, Jason D Lee, and Qi Lei. 2020. Few-shot learning via learning the representation, provably. _arXiv:2002.09434_ (2020). 

- [12] Moming Duan, Duo Liu, Xianzhang Chen, Renping Liu, Yujuan Tan, and Liang Liang. 2020. Self-balancing federated learning with global imbalanced data in mobile systems. _IEEE Transactions on Parallel and Distributed Systems_ (2020). 

- [13] Alireza Fallah, Aryan Mokhtari, and Asuman Ozdaglar. 2020. Personalized federated learning with theoretical guarantees: A model-agnostic meta-learning approach. In _NeurIPS_ . 

- [14] Chenyou Fan and Jianwei Huang. 2021. Federated Few-Shot Learning with Adversarial Learning. In _WiOpt_ . 

- [15] Chelsea Finn, Pieter Abbeel, and Sergey Levine. 2017. Model-agnostic metalearning for fast adaptation of deep networks. In _ICML_ . 

- [16] Xingbo Fu, Binchi Zhang, Yushun Dong, Chen Chen, and Jundong Li. 2022. Federated graph machine learning: A survey of concepts, techniques, and applications. _ACM SIGKDD Explorations Newsletter_ (2022). 

- [17] Ian J Goodfellow, Jean Pouget-Abadie, Mehdi Mirza, Bing Xu, David WardeFarley, Sherjil Ozair, Aaron C Courville, and Yoshua Bengio. 2014. Generative Adversarial Nets. In _NIPS_ . 

- [18] Kaiming He, Haoqi Fan, Yuxin Wu, Saining Xie, and Ross Girshick. 2020. Momentum contrast for unsupervised visual representation learning. In _CVPR_ . 

- [19] Geoffrey Hinton, Oriol Vinyals, Jeff Dean, et al. 2015. Distilling the knowledge in a neural network. _arXiv:1503.02531_ 2, 7 (2015). 

- [20] Sepp Hochreiter and Jürgen Schmidhuber. 1997. Long short-term memory. _Neural computation_ (1997). 

- [21] Tzu-Ming Harry Hsu, Hang Qi, and Matthew Brown. 2019. Measuring the effects of non-identical data distribution for federated visual classification. _arXiv:1909.06335_ (2019). 

- [22] Peter Kairouz, H Brendan McMahan, Brendan Avent, Aurélien Bellet, Mehdi Bennis, Arjun Nitin Bhagoji, Kallista Bonawitz, Zachary Charles, Graham Cormode, Rachel Cummings, et al. 2021. Advances and open problems in federated learning. _Foundations and Trends® in Machine Learning_ (2021). 

- [23] Sai Praneeth Karimireddy, Satyen Kale, Mehryar Mohri, Sashank Reddi, Sebastian Stich, and Ananda Theertha Suresh. 2020. Scaffold: Stochastic controlled averaging for federated learning. In _ICML_ . 

- [24] Mikhail Khodak, Maria-Florina F Balcan, and Ameet S Talwalkar. 2019. Adaptive gradient-based meta-learning methods. _NeurIPS_ (2019). 

- [25] Prannay Khosla, Piotr Teterwak, Chen Wang, Aaron Sarna, Yonglong Tian, Phillip Isola, Aaron Maschinot, Ce Liu, and Dilip Krishnan. 2020. Supervised contrastive learning. In _NeurIPS_ . 

- [26] Diederik P Kingma and Jimmy Ba. 2015. Adam: A method for stochastic optimization. In _ICLR_ . 

- [27] Alex Krizhevsky, Geoffrey Hinton, et al. 2009. Learning multiple layers of features from tiny images. (2009). 

- [28] Ken Lang. 1995. Newsweeder: Learning to filter netnews. In _Machine Learning Proceedings 1995_ . 

- [29] Kwonjoon Lee, Subhransu Maji, Avinash Ravichandran, and Stefano Soatto. 2019. Meta-learning with differentiable convex optimization. In _CVPR_ . 

- [30] Daliang Li and Junpu Wang. 2019. Fedmd: Heterogenous federated learning via model distillation. _arXiv:1910.03581_ (2019). 

- [31] Qinbin Li, Zeyi Wen, Zhaomin Wu, Sixu Hu, Naibo Wang, Yuan Li, Xu Liu, and Bingsheng He. 2021. A survey on federated learning systems: vision, hype and reality for data privacy and protection. _TKDE_ (2021). 

- [32] Tian Li, Anit Kumar Sahu, Manzil Zaheer, Maziar Sanjabi, Ameet Talwalkar, and Virginia Smith. 2020. Federated optimization in heterogeneous networks. In _MLSys_ . 

- [33] Wei Yang Bryan Lim, Nguyen Cong Luong, Dinh Thai Hoang, Yutao Jiao, YingChang Liang, Qiang Yang, Dusit Niyato, and Chunyan Miao. 2020. Federated learning in mobile edge networks: A comprehensive survey. _IEEE Communications Surveys & Tutorials_ (2020). 

- [34] Bing Liu. 2011. _Web data mining: exploring hyperlinks, contents, and usage data_ . Vol. 1. Springer. 

- [35] Lu Liu, Tianyi Zhou, Guodong Long, Jing Jiang, and Chengqi Zhang. 2019. Learning to propagate for graph meta-learning. In _NeurIPS_ . 

- [36] Brendan McMahan, Eider Moore, Daniel Ramage, Seth Hampson, and Blaise Aguera y Arcas. 2017. Communication-efficient learning of deep networks from decentralized data. In _AISTATS_ . 

- [37] Nikhil Mishra, Mostafa Rohaninejad, Xi Chen, and Pieter Abbeel. 2018. A Simple Neural Attentive Meta-Learner. In _ICLR_ . 

- [38] Rishabh Misra. 2018. News category dataset. _DOI: DOI: https://doi. org/10.13140/RG_ 2, 20331.18729 (2018). 

- [39] Rishabh Misra and Jigyasa Grover. 2021. _Sculpting Data for ML: The first act of Machine Learning_ . 

- [40] Aaron van den Oord, Yazhe Li, and Oriol Vinyals. 2018. Representation learning with contrastive predictive coding. In _arXiv:1807.03748_ . 

- [41] Boris Oreshkin, Pau Rodríguez López, and Alexandre Lacoste. 2018. Tadam: Task dependent adaptive metric for improved few-shot learning. In _NeurIPS_ . 

- [42] Sachin Ravi and Hugo Larochelle. 2016. Optimization as a model for few-shot learning. In _ICLR_ . 

- [43] Avinash Ravichandran, Rahul Bhotika, and Stefano Soatto. 2019. Few-shot learning with embedded class models and shot-free meta training. In _CVPR_ . 

- [44] Kuniaki Saito, Kohei Watanabe, Yoshitaka Ushiku, and Tatsuya Harada. 2018. Maximum classifier discrepancy for unsupervised domain adaptation. In _CVPR_ . 

- [45] Jake Snell, Kevin Swersky, and Richard Zemel. 2017. Prototypical networks for few-shot learning. In _NeurIPS_ . 

- [46] Qianru Sun, Yaoyao Liu, Tat-Seng Chua, and Bernt Schiele. 2019. Meta-transfer learning for few-shot learning. In _CVPR_ . 

- [47] Flood Sung, Yongxin Yang, Li Zhang, Tao Xiang, Philip HS Torr, and Timothy M Hospedales. 2018. Learning to compare: relation network for few-shot learning. In _CVPR_ . 

- [48] Canh T Dinh, Nguyen Tran, and Josh Nguyen. 2020. Personalized federated learning with moreau envelopes. _NeurIPS_ (2020). 

- [49] Alysa Ziying Tan, Han Yu, Lizhen Cui, and Qiang Yang. 2022. Towards personalized federated learning. _IEEE TNNLS_ (2022). 

- [50] Zhen Tan, Song Wang, Kaize Ding, Jundong Li, and Huan Liu. 2022. Transductive Linear Probing: A Novel Framework for Few-Shot Node Classification. _arXiv:2212.05606_ (2022). 

- [51] Yonglong Tian, Yue Wang, Dilip Krishnan, Joshua B Tenenbaum, and Phillip Isola. 2020. Rethinking few-shot image classification: a good embedding is all you need? _ECCV_ (2020). 

- [52] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Lukasz Kaiser, and Illia Polosukhin. 2017. Attention is all you need. In _NeurIPS_ . 

- [53] Oriol Vinyals, Charles Blundell, Timothy Lillicrap, Daan Wierstra, et al. 2016. Matching networks for one shot learning. In _NeurIPS_ . 

- [54] Song Wang, Chen Chen, and Jundong Li. 2022. Graph Few-shot Learning with Task-specific Structures. In _NeurIPS_ . 

- [55] Song Wang, Kaize Ding, Chuxu Zhang, Chen Chen, and Jundong Li. 2022. Taskadaptive few-shot node classification. In _SIGKDD_ . 

- [56] Song Wang, Yushun Dong, Xiao Huang, Chen Chen, and Jundong Li. 2022. FAITH: Few-Shot Graph Classification with Hierarchical Task Graphs. In _IJCAI_ . 

- [57] Song Wang, Xiao Huang, Chen Chen, Liang Wu, and Jundong Li. 2021. REFORM: Error-Aware Few-Shot Knowledge Graph Completion. In _CIKM_ . 

- [58] Guandong Xu, Yanchun Zhang, and Lin Li. 2010. _Web mining and social networking: techniques and applications_ . Vol. 6. Springer Science & Business Media. 

- [59] Qiang Yang, Yang Liu, Tianjian Chen, and Yongxin Tong. 2019. Federated machine learning: Concept and applications. _ACM TIST_ (2019). 

- [60] Huaxiu Yao, Linjun Zhang, and Chelsea Finn. 2021. Meta-Learning with Fewer Tasks through Task Interpolation. In _ICLR_ . 

- [61] Tao Yu, Eugene Bagdasaryan, and Vitaly Shmatikov. 2020. Salvaging federated learning by local adaptation. _arXiv:2002.04758_ (2020). 

- [62] Qingyu Zhang and Richard S Segall. 2008. Web mining: a survey of current research, techniques, and software. _International Journal of Information Technology & Decision Making_ (2008). 

- [63] Yue Zhao, Meng Li, Liangzhen Lai, Naveen Suda, Damon Civin, and Vikas Chandra. 2018. Federated learning with non-iid data. In _arXiv:1806.00582_ . 

- [64] Zhuangdi Zhu, Junyuan Hong, and Jiayu Zhou. 2021. Data-free knowledge distillation for heterogeneous federated learning. In _ICLR_ . 

KDD ’23, August 6–10, 2023, Long Beach, CA, USA 

Federated Few-shot Learning 

## **A NOTATIONS** 

In this section, we provide details for the used notations in this paper and their corresponding descriptions. 

**Table 2: Notations used in this paper.** 

|**Notations**|**Defnitions or Descriptions**|
|---|---|
|S|the server|
|_𝐼_<br>|the number of clients|
|C<sup>(</sup><sup>_𝑖_)</sup>|the_𝑖_-th client|
|C_𝑏_,C_𝑛_<br><br>|the base class set and the novel class set|
|D <sup>(</sup><sup>_𝑖_)</sup><br>_𝑏_<sup>, D (</sup><sup>_𝑖_)</sup><br>_𝑛_|the local base and novel datasets inC<sup>(</sup><sup>_𝑖_)</sup>|
|T,S,Q|a meta-task and its support set and query set|
|_𝜓_,_𝜙_|the client-model and the server-model|
|h_𝜓_|representations learned by client-model|
|h_𝜙_|representations learned by server-model|
|p_𝜓_|the output probabilities by client-model|
|p_𝜙_|the output probabilities by server-model|
|_𝑁_|the number of support classes in each meta-task|
|_𝐾_|the number of labeled samples in each class|
|_𝐷_|the number of support samples in each meta-task|
|_𝑄_|the number of query samples in each meta-task|
|_𝛼𝑓𝑡_|the learning rate for fne-tuning|
|_𝛼𝜙_,_𝛼𝜓_|the meta-learning rates for_𝜙_and_𝜓_|
|_𝑇_|the number of training rounds|
|_𝜏_|the number of local training steps|
|_𝜆𝑀𝐼_|the loss weight for the mutual information loss|
|_𝜆𝐾𝐷_|the loss weight for the knowledge distillation loss|



## **B ALGORITHM** 

We provide the detailed training process of our framework F<sup>2</sup> L in Algorithm 1. 

**Algorithm 1** Detailed training <u>process of our framework F</u><sup>2</sup> L. 

- **Input:** A set of _𝐼_ federated clients; a local update objective L _𝜙_ for server-model; a local update objective L _𝜓_ for client-model; number of training rounds _𝑇_ ; number of local training steps _𝜏_ . 

- **Output:** A trained server-model _𝜙_ and a unique client-model _𝜓𝑖_ for each client C<sup>(</sup><sup>_𝑖_)</sup> in {C<sup>(</sup><sup>_𝑖_)</sup> } _𝑖_<sup>_𝐼_</sup> =1<sup>.</sup> 

- 1: **for** _𝑡_ = 1 _,_ 2 _, . . . ,𝑇_ **do** 2: **for** each client C<sup>(</sup><sup>_𝑖_)</sup> in {C<sup>(</sup><sup>_𝑖_)</sup> } _𝑖_<sup>_𝐼_</sup> =1<sup>in parallel</sup><sup>**do**</sup> 3: **for** _𝑠_ = 1 _,_ 2 _, . . . ,𝜏_ **do** 4: Sample a meta-task T _𝑖_<sup>_𝑡,𝑠_</sup> = {S _𝑖_<sup>_𝑡,𝑠,_Q</sup> _𝑖_<sup>_𝑡,𝑠_};</sup> 5: Fine-tune client-model _𝜓𝑖_ on S _𝑖_<sup>_𝑡,𝑠_</sup> according to Eq. (3); 6: Update server-model on S _𝑖_<sup>_𝑡,𝑠_</sup> with Eq. (5) and Eq. (14); 7: Update client-model on Q _𝑖_<sup>_𝑡,𝑠_</sup> with Eq. (4) and Eq. (20); 8: **end for** 9: **end for** 

- 10: Each client returns the updated parameters of server-model to the server; 

- 11: The server sends back averaged parameters of server-model to each client; 

- 12: **end for** 

## **C REPRODUCIBILITY** 

## **C.1 Model Details** 

In this section, we introduce the specific choices for the encoders and classifiers in both server-model and client-model (i.e., _𝑞𝜙_ , _𝑓𝜙_ , _𝑞𝜓_ , and _𝑓𝜓_ ). 

_C.1.1 Server-model Encoder 𝑞𝜙 ._ For the server-model encoder, we adopt different models for news article datasets and image datasets. In particular, for news article datasets 20 Newsgroup and Huffpost, we leverage a biLSTM [20] with 50 units as the server-model encoder. For the image datasets FC100 and miniImageNet, following [43, 51], we utilize a ResNet12 as the server-model encoder. Similar to [29], the Dropblock is used as a regularizer. The number of filters is set as (64, 160, 320, 640). 

_C.1.2 Client-model Encoder 𝑞𝜓 ._ Considering that the client-model is required to process the entire support set in a meta-task for learning local meta-knowledge, we propose to further utilize a set-invariant function that takes a set of samples as input while capturing the correlations among these samples. In practice, we leverage the Transformer [52] as the client-model encoder _𝑞𝜓_ to process the entire support set: 


![](P022_images/P022.pdf-0011-16.png)

### Figure analysis

Purpose: The displayed equation formalizes how the client-model encoder \(q_\psi\) uses a Transformer to process the full support set representation sequence produced by the server-model encoder \(q_\phi\).

Equation transcription:
\[
\left(h_{\psi}^{1}, h_{\psi}^{2}, \ldots, h_{\psi}^{D}\right)
= \operatorname{Transformer}\left(h_{\phi}^{1}, h_{\phi}^{2}, \ldots, h_{\phi}^{D}\right),
\tag{22}
\]

Important components:
- \(h_{\phi}^{i}\): representation of the \(i\)-th support-set sample learned by the server-model encoder.
- \(h_{\psi}^{i}\): transformed representation of the \(i\)-th support-set sample learned by the client-model encoder.
- \(D\): number of samples or elements in the support set sequence being processed.
- \(\operatorname{Transformer}(\cdot)\): set/sequence-processing function used to capture relationships among support-set samples.

Direct visual observation: The equation maps a tuple of server-side representations \((h_{\phi}^{1}, \ldots, h_{\phi}^{D})\) to a corresponding tuple of client-side representations \((h_{\psi}^{1}, \ldots, h_{\psi}^{D})\) through a Transformer.

Interpretation: In the surrounding reproducibility section, this supports the stated design choice that the client-model encoder should process the entire support set jointly rather than independently, allowing correlations among samples in a meta-task to influence the learned local meta-knowledge.


where h<sup>_𝑖_</sup> _𝜙_<sup>(or h</sup> _𝜓_<sup>_𝑖_) denotes the representation of the</sup><sup>_𝑖_-th sample in</sup> S learned by the server-model encoder _𝑞𝜙_ (or client-model encoder _𝑞𝜓_ ). With the Transformer, the representations learned by the clientmodel can effectively capture the correlations among samples in the entire support set S for learning meta-knowledge. 

_C.1.3 Server-model Classifier 𝑓𝜙 and Client-model Classifier 𝑓𝜓 ._ The classifiers _𝑓𝜙_ and _𝑓𝜓_ are both implemented as a fully-connected layer, where the output size is |C _𝑏_ | for _𝑓𝜙_ and _𝑁_ for _𝑓𝜓_ , as described in Sec. 3.1. 

## **C.2 Baseline Settings** 

In this section, we provide further details in the implementation of baselines in our experiments. 

- _Local_ . For this baseline, an individual model is trained for each client over the local data. Specifically, we use the same architecture of encoders in our framework to learn sample representations. 

- _FL-MAML_ . For this baseline, we leverage the MAML [15] strategy and set the meta-learning rate as 0.001 and the fine-tuning rate as 0.01. The encoders are the same as our framework. 

- _FL-Proto_ . For this baseline, we follow the setting in ProtoNet [45] with the same encoders in our framework. The learning rate is set as 0.001. 

- _FedFSL_ [14]. For this baseline, which combines MAML and an adversarial learning strategy [17, 44], we follow the settings in the public code and set the learning rate as 0.001. The adaptation step size is set as 0.01. 

KDD ’23, August 6–10, 2023, Long Beach, CA, USA 

Song Wang et al. 

## **C.3 Parameter Settings** 

For our framework F<sup>2</sup> L, we set the number of clients as 10. The number of training steps _𝜏_ in each client is set as 10, and the number of training rounds _𝑇_ is set as 200. Moreover, the meta-learning rates _𝛼𝜓_ and _𝛼𝜙_ are both set as 0.001 with a dropout rate of 0.1. The fine-tuning learning rate _𝛼 𝑓𝑡_ is set as 0.01. We leverage the Adam [26] optimization strategy with the weight decay rate set as 10<sup>−4</sup> . During the meta-test, we randomly sample 100 meta-test tasks from novel classes C _𝑛_ with a query set size |Q| of 5. In order to preserve consistency for fair comparisons, we keep identical meta-test tasks for all baselines. The loss weights _𝜆𝑀𝐼_ and _𝜆𝐾𝐷_ are both set as 0.5. The default value of _𝐼_ is set as 10. 

