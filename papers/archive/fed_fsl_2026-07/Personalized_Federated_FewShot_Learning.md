2534 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS, VOL. 35, NO. 2, FEBRUARY 2024 

# Personalized Federated Few-Shot Learning 

Yunfeng Zhao, Guoxian Yu , _Member, IEEE_ , Jun Wang , Carlotta Domeniconi, Maozu Guo , Xiangliang Zhang , _Senior Member, IEEE_ , and Lizhen Cui , _Member, IEEE_ 

**_Abstract_ —Personalized federated learning (PFL) learns a personalized model for each client in a decentralized manner, where each client owns private data that are not shared and data among clients are non-independent and identically distributed (i.i.d.) However, existing PFL solutions assume that clients have sufficient training samples to jointly induce personalized models. Thus, existing PFL solutions cannot perform well in a fewshot scenario, where most or all clients only have a handful of samples for training. Furthermore, existing few-shot learning (FSL) approaches typically need centralized training data; as such, these FSL methods are not applicable in decentralized scenarios. How to enable PFL with limited training samples per client is a practical but understudied problem. In this article, we propose a solution called personalized federated few-shot learning (pFedFSL) to tackle this problem. Specifically, pFedFSL learns a personalized and discriminative feature space for each client by identifying which models perform well on which clients, without exposing local data of clients to the server and other clients, and which clients should be selected for collaboration with the target client. In the learned feature spaces, each sample is made closer to samples of the same category and farther away from samples of different categories. Experimental results on four benchmark datasets demonstrate that pFedFSL outperforms competitive baselines across different settings.** 

**_Index Terms_ —Collaboration, feature space learning, fewshot learning (FSL), non-independent and identically distributed (i.i.d.) data, personalized federated learning (PFL).** 

## I. INTRODUCTION 

**I** Nshown great promise for training a single global model overRECENT years, federated learning (FL) [1]–[3] has multiple clients without exposing private data with one another and thus ensuring the privacy of local data and inducing a global model in a communication-efficient manner. However, in practice, clients’ local data are subjected to various distributions since they are generated on local clients with different 

Manuscript received 22 December 2021; revised 2 April 2022 and 14 June 2022; accepted 7 July 2022. Date of publication 21 July 2022; date of current version 6 February 2024. This work was supported by the Natural Science Foundation of China under Grant 62031003, Grant 61872300, and Grant 91846205. _(Corresponding author: Jun Wang.)_ 

Yunfeng Zhao, Guoxian Yu, Jun Wang, and Lizhen Cui are with the School of Software, Shandong University, Jinan 250100, China (e-mail: yunfengzhao@mail.sdu.edu.cn; gxyu@sdu.edu.cn; kingjun@sdu.edu. cn; clz@sdu.edu.cn). 

Carlotta Domeniconi is with the Department of Computer Science, George Mason University, Fairfax, VA 22030 USA (e-mail: carlotta@cs.gmu.edu). Maozu Guo is with the Department of Computer Science, Beijing University of Civil Engineering and Architecture, Beijing 100044, China (e-mail: guomaozu@bucea.edu.cn). 

Xiangliang Zhang is with the Department of Computer Science and Engineering, University of Notre Dame, Notre Dame, IN 46556 USA (e-mail: xzhang33@nd.edu). 

Digital Object Identifier 10.1109/TNNLS.2022.3190359 

usages or user habits, and this raises a key threat to FL: data heterogeneity [4], [5]. Data heterogeneity of different clients makes it hard to fit the entire local data with a single global model and further compromises the model performance and convergence rate. 

To overcome this problem, the personalized federated learning (PFL) [6], [7] framework has been proposed to deal with the data heterogeneity of different clients. Different from typical FL solutions [1], [8], [9] that aim to induce a single shared global model by pursuing global optima of entire clients, PFL targets to jointly learn a personalized model for each participating client, with the aim of the learned local models that can fit diverse local data of clients well. Formally, let { _ci_ }<sup>_n_</sup> _i_ =1<sup>denote</sup><sup>_n_clients that carry the same type of models but</sup> personalized by _n_ different sets of model parameters { _θi_ }<sup>_n_</sup> _i_ =1<sup>,</sup> along with _n_ different datasets { _Di_ }<sup>_n_</sup> _i_ =1<sup>.These</sup><sup>_n_datasets</sup> { _Di_ }<sup>_n_</sup> _i_ =1<sup>are subject to</sup><sup>_n_distinct distributions {</sup><sup>_Pi_}</sup><sup>_n_</sup> _i_ =1<sup>, i.e., they</sup> are not independent and identically distributed (i.i.d.). For each client _ci_ , by defining its loss function _L(θi_ ; _Di )_ , PFL aims at obtaining the optimal set of model parameters { _θ_ 1<sup>∗</sup><sup>_, . . . , θ_</sup> _n_<sup>∗} =</sup> arg min{ _θ_ 1 _,...,θn_ } � _ni_ =1<sup>_L(θi_;</sup><sup>_Di)_.Sincethedatasetsaregener-</sup> ated on different local clients, under different environments, usage, and context, statistical heterogeneity of data is the core issue for PFL, and most existing PFL approaches can be roughly grouped into data- and model-based approaches [10]. The former class of methods tries to alleviate the problem of weight divergence, arising from multiple rounds of local training and weight synchronization on non-i.i.d. datasets during the FL training process, by smoothing the data heterogeneity of participating clients [4], [11]–[14]. The second category of methods aims at fitting FL models to the various data distributions among clients [7], [9], [15]–[22]. 

However, these PFL approaches require that most or all participating clients have sufficient training data to induce the personalized models. They do not perform well in a fewshot scenario, where most or all participating clients only have few training samples for each category. Although fewshot learning (FSL) [23] has been extensively explored in diverse domains [24]–[29], most existing FSL methods typically need centralized data to induce the FSL model. To enable FSL in a decentralized scenario, a recently proposed method federated FSL with adversarial learning (FedFSL-Adv) [30] aims at inducing an FSL model in the FL setup, which can tackle new tasks with just few-shot samples. However, FedFSL-Adv still requires many-shot samples in each client to induce the FSL model and thus is not effective when applied with PFL in few-shot scenarios. We formalize this learning 

2162-237X © 2022 IEEE. Personal use is permitted, but republication/redistribution requires IEEE permission. See https://www.ieee.org/publications/rights/index.html for more information. 

Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on July 28,2026 at 12:43:06 UTC from IEEE Xplore.  Restrictions apply. 

2535 

ZHAO _et al._ : PERSONALIZED FEDERATED FEW-SHOT LEARNING 


![](P023_images/P023.pdf-0002-02.png)



![](P023_images/P023.pdf-0002-03.png)



![](P023_images/P023.pdf-0002-04.png)



![](P023_images/P023.pdf-0002-05.png)



![](P023_images/P023.pdf-0002-06.png)

### Figure analysis

The figure is a schematic of the proposed personalized federated few-shot learning framework, pFedFSL. Its purpose is to show how a central federated server coordinates multiple clients so that each client learns a personalized discriminative feature space while keeping local data private.

**Main components and labels:**

- A central **server** is shown at the left with a cloud/server icon.
- Multiple clients are shown as colored database cylinders: **c1**, **c2**, ..., **cn**.
- For each client, the local dataset is labeled **D1**, **D2**, ..., **Dn**.
- Each client has a personalized model/feature-space parameter, labeled **θ1**, **θ2**, ..., **θn**.
- The server sends selected model parameters to each client, shown as sets such as **{θa1, ..., θam}**, **{θb1, ..., θbm}**, and corresponding red aggregation-weight annotations such as **{wi,d1, ..., wi,dm+1}**.
- A legend indicates that the **blue dotted box** represents the **original feature space**, while the **orange dotted box** represents the **new feature space**.

**Information flow directly shown:**

1. The server provides a subset of other clients’ model parameters to a target client.
2. Each client combines received models with its own local model using learned aggregation weights.
3. Local data **Di** are used to evaluate/weight the received and local models.
4. Each client updates its personalized model and sends updated model information and aggregation weights back to the server.
5. The server uses this information to decide which client models should be sent to which target clients in the next communication round.

**Visual observations:**

- In the blue original feature-space boxes, colored sample points are visibly mixed, suggesting overlapping class distributions before personalization.
- In the orange new feature-space boxes, same-colored points appear more clustered and different colors are more separated.
- The repeated structure for clients **c1**, **c2**, and **cn** indicates that every client undergoes the same personalization procedure, but with client-specific data, model parameters, and aggregation weights.
- The arrows from local datasets and neural-network icons toward the orange feature-space boxes visually encode the transformation from original to personalized discriminative representations.

**Interpretation in context:**

The diagram supports the surrounding text’s claim that pFedFSL addresses few-shot personalized federated learning by encouraging more collaboration among clients with similar data distributions. Rather than learning one shared global model, the method uses client-specific aggregation of selected received models to produce personalized feature spaces. The intended effect is that samples from the same class become closer together and samples from different classes become farther apart, helping each client compensate for scarce local few-shot data while avoiding direct data sharing.


Fig. 1. Schematic framework of pFedFSL. pFedFSL learns a personalized and discriminative feature space parameterized by _θi_ for each client _ci_ by encouraging similar clients to collaborate more with the following iterative operations: 1) a client _ci_ computes the aggregation weights { _wi,d_ 1 _, . . . , wi,dm_ +1 } of received _m_ models { _θd_ 1 _, . . . , θdm_ } and local model _θi_ (where _wi,dm_ +1 is for _θi_ ) by testing on its local data _Di_ , gets the aggregated local model _θ_<sup>�</sup> _i_ by _θ_ � _i_ usingaggregating _Di_ ; 2)receivedeach clientmodelssendswithbackcomputedthe updatedweights,modelandandthenaggregationoptimizes weights to the FL server; and 3) FL server decides which subset of updated local models needs to be sent to a target client for next round training. 

problem as a new framework called personalized federated few-shot learning (pFedFSL). pFedFSL has many potential applications, e.g., multiple hospitals around the world want to predict some rare diseases via an FL framework and these diseases around the world are not exactly the same. The key challenges of pFedFSL are twofold: 1) the personalized model is hard to induce with scarce few-shot training samples for each client and 2) data heterogeneity exists among multiple clients and the distinct data distributions of individual clients cannot be reliably estimated with such scarce local data. 

To tackle this problem, we propose a pFedFSL approach. Specifically, pFedFSL aims at learning a personalized and discriminative feature space for each client by encouraging clients that have more similar distributions to collaborate more. In these new feature spaces, each sample is made closer to samples that belong to the same category and farther away from samples that belong to other categories. Collaboration between clients with similar distributions is fostered by determining which model parameters perform well on which clients, without exposing data of local clients to the server or to other clients. The whole pFedFSL framework is shown in Fig. 1. The main contributions of our work are given as follows. 

- 1) We focus on a practical and general PFL setting, where the training samples of each client are few-shot with a varying number of labels, and the clients’ datasets are non-i.i.d. We also notice the fact that most existing FSL methods need centralized data and therefore are not applicable in a decentralized scenario. Both issues are not addressed by existing PFL solutions and FSL methods. Given that, we introduce the pFedFSL approach to induce a personalized feature space for each client, 

which can map the samples annotated with the same label close to each other, while the samples of different labels far apart in that space. 

- 2) pFedFSL aims at learning a discriminative feature space for each client with few-shot training data by encouraging clients that have more similar distributions to collaborate more. This improves the performance of FL and reduces the data scarcity of individual clients. We further design a strategy to adaptively select collaborative clients to reduce the communication load and boost the training. 

- 3) We present extensive experiments on four benchmark datasets and show that our pFedFSL outperforms standard FL strategies [1], [9], state-of-the-art PFL approaches [7], [17], [18], [31], and the competitive FedFSL-Adv method [30]. 

The rest of this article is organized as follows. The related work on PFL and FSL is briefly reviewed in Section II. Section III presents the technical details of our method, and Section IV reports the experimental results and analysis. Section V concludes this article and discusses future research directions. 

## II. RELATED WORK 

## _A. Personalized Federated Learning_ 

Recently, PFL [6], [7] has emerged as a promising framework for FL with multiple clients with non-i.i.d. data. Due to its effectiveness, PFL has attracted a lot of attention, and the majority of PFL approaches can be roughly categorized into two classes: data- and model-based methods. 

The goal of data-based approaches is to smooth data heterogeneity of participating clients [4], [11]–[14]. For example, Jeong _et al_ . [11] proposed federated augmentation (FAug) to collectively induce a generative adversarial network (GAN) in the server. With the learned GAN model, clients can generate additional samples, which makes their local datasets becoming i.i.d. Wang _et al_ . [12] proposed Favor, an experience-driven control framework, to achieve the bias caused by non-i.i.d. data by selecting a subset of the participating clients in each training round. Specifically, Favor designs a deep Q-learning formulation for client selection to maximize a reward that encourages improved model performance while penalizing the use of communication rounds. 

Model-based approaches develop models that are personalized to the participating clients [7], [9], [15]–[22]. To name a few, Dinh _et al_ . [17] proposed PFL with Moreau envelopes (pFedMe), where the PFL problem is formulated as a bilevel optimization problem by decoupling the training of personalized models from inducing the global model. The approach Per-FedAvg [7] finds an initial global model shared among all clients within the model-agnostic meta-learning (MAML) [32] framework and then updates the clients using their own data. Huang _et al_ . [18] proposed heuristically federated attentive message passing (HeurFedAMP), which maintains a personalized cloud model for each client on the FL server and then passes the personalized models from 

Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on July 28,2026 at 12:43:06 UTC from IEEE Xplore.  Restrictions apply. 

2536 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS, VOL. 35, NO. 2, FEBRUARY 2024 

clients to personalized cloud models with similar model parameters. Zhang _et al_ . [31] proposed PFL using the first-order model optimization (FedFomo); this approach learns optimal weighted model combinations for each participating client by determining how much a client can benefit from models of other clients. Guo _et al_ . [21] proposed PFL based on mixture of experts (PFL-MoE) to mix outputs of the personalized models and global model for achieving both personalization and generalization, while from the perspective of clustering, Duan _et al_ . [22] proposed flexible clustered federated learning (FlexCFL) to group the participating clients based on the similarity between the clients’ optimization directions for lower weight divergence. Besides, George _et al_ [33] and George and Gurram [34] adopted distributed SGD for a set of clients to collaboratively train their individual models, in which the clients communicate only with neighorhood clients without requiring a server. The distributed SGD differs from the FL setup, where an extra server is established and clients communicate solely with this server. 

Although the aforementioned approaches can induce personalized models for each client using different techniques, they cannot perform well in a more general scenario, where most or all of the participating clients have only few-shot training samples. In this scenario, clients do not have sufficient training data to induce personalized models. To enable PFL in this general setting, we propose pFedFSL, which jointly learns a personalized and discriminative feature space for each client and can prevent overfit local personalized models. 

## _B. Few-Shot Learning_ 

FSL [23], [35] aims at learning new concepts (class) with a handful of samples by mimicking the cognitive abilities of humans. Existing FSL problems are mainly supervised ones, and they typically can be viewed as _N_ -way _K_ -shot classification problems, in which the training dataset of the new task contains _K_ × _N_ samples from _N_ classes, each with _K_ examples. The core issue of FSL is the unreliability of the empirical risk minimizer, due to limited training samples. The existing approaches for FSL can be grouped into the following categories: data-driven, model-driven, and algorithm-driven [23]. Data augmentation-based FSL methods reduce the uncertainty of the empirical risk minimizer by enriching supervised information, e.g., by deriving more samples from the original few-shot samples or by using weakly labeled/unlabeled data or similar datasets [36], [37]. Modelbased FSL methods constrain the hypothesis space via prior knowledge [24], [38], to reduce overfitting and make the empirical risk minimizer more reliable. With prior knowledge, algorithm-based FSL methods seek optimal model parameters by providing a good initialization or by directly learning an optimizer to output search steps [25], [32]. 

Unfortunately, most existing FSL methods build on the promise that the data for acquiring meta knowledge is centralized. These FSL solutions can hardly work in a decentralized manner. More recently, Fan and Huang [30] proposed the federated FSL framework and attempted it in an adversarial fashion (FedFSL-Adv). FedFSL-Adv induces an FSL model 

to tackle novel tasks with just a few-shot samples. However, FedFSL-Adv also builds on the premise that each participating client has sufficient training data to compose many base tasks to learn the FSL model; thus, it cannot work well in the pFedFSL scenario, in which most or all participating clients have only few-shot training samples and these data sources are non-i.i.d. 

To address this problem, our proposed pFedFSL induces a personalized model for each client with limited training samples, by discovering which model parameters perform well on which clients. In this way, pFedFSL effectively handles the FSL problem with heterogeneous data sources and under the condition that data of each source are few-shot. 

## III. PROPOSED METHOD 

## _A. Problem Formulation and Notation_ 

Let { _ci_ }<sup>_n_</sup> _i_ =1<sup>denoteapopulationof</sup><sup>_n_clients,whereeach</sup> client _ci_ carries local model parameters _θi_<sup>_t_inround</sup><sup>_t_and</sup> local few-shot training data _Di_ = { _(_ **x** 1<sup>_i, y_</sup> 1<sup>_i), (_</sup><sup>**x**</sup> 2<sup>_i, y_</sup> 2<sup>_i), . . . ,_</sup> _(_ **x**<sup>_i_</sup> _Ni_ × _Ki_<sup>_, y_</sup> _N_<sup>_i_</sup> _i_ × _Ki_<sup>_)_}.</sup><sup>_Ni_and</sup><sup>_Ki_representthenumberofclasses</sup> and the number of training samples per class, respectively, of the _i_ th client (a scenario often called _N_ -way _K_ -shot classification). For each sample _(_ **x** _, y)_ , **x** ∈ R<sup>_d_</sup> is the _d_ -dimensional feature vector and _y_ ∈{ _l_ } _l_<sup>_N_</sup> =<sup>_i_</sup> 1<sup>is the ground-truth</sup> label. The set of all the samples annotated with label _l_ in client _ci_ is _Sl_<sup>_i_= {</sup><sup>**x**|</sup><sup>_(_</sup><sup>**x**</sup><sup>_, y)_∈</sup><sup>_Di_and</sup><sup>_y_=</sup><sup>_l_}.Foreachparticipating</sup> client _ci_ , by defining the loss function as _L(θi_ ; _Di )_ , we aim to learn the optimal set of personalized model parameters _n_ { _θ_ 1<sup>∗</sup><sup>_, . . . , θ_</sup> _n_<sup>∗}=arg min{</sup><sup>_θ_</sup> 1<sup>_,...,θ_</sup> _n_<sup>}</sup> � _i_ =1<sup>_L(θi_;</sup><sup>_Di)_thatperform</sup> well on the corresponding local data via the collaboration between _n_ clients. The framework overview of pFedFSL is shown in Fig. 1. Section II-B discusses the technical details. 

## _B. Personalized Federated Few-Shot Learning_ 

Metric learning [24], [39], as a main type of metalearning [40], aims to learn a representative feature space (embedding space) and has shown great merits for tackling various FSL tasks in this new space. The learned representative feature space can embed the samples of the same class close to each other while farther away from samples of different classes, and it can also be regarded as a sort of transferable knowledge for correlated tasks. For example, pretrained visual classification networks (e.g., ResNet [41]) and natural language networks (e.g., BERT [42]) can yield representative image and language representations for related tasks, respectively. Thus, the discriminative feature space learning can also benefit the few-shot classification under PFL scenarios due to its advantage of transferability, as shown in our experiments. 

In view of this insight, our goal is to learn a set of personalized models { _θ_ 1<sup>∗</sup><sup>_, . . . , θ_</sup> _n_<sup>∗}for</sup><sup>_n_participatingclients,</sup> each of which can produce a discriminative feature space by encouraging more similar clients to foster collaboration. More specifically, following the general FL setup [1], [31], pFedFSL iteratively performs the following three steps: 1) a client receives a set of clients’ models from the FL server and then computes a weighted combination of the performance of the models on its own local data; 2) each client optimizes its 

Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on July 28,2026 at 12:43:06 UTC from IEEE Xplore.  Restrictions apply. 

2537 

ZHAO _et al._ : PERSONALIZED FEDERATED FEW-SHOT LEARNING 

model using its local data and then sends the optimized model and aggregation weights to the FL server; and 3) the FL server decides which subset of client models needs to be sent to a target client according to a sampling scheme. The three phases (one communication round) are presented in the following. 

_1) Model Aggregation Phase:_ Unlike the typical FL setup [1], [9], where model aggregation is performed in the FL server, pFedFSL conducts model aggregation for each client in a decentralized manner. This choice is due to the unknown distributions of local data; we can then perform model aggregation locally at clients according to their performance on local data. Suppose that client _ci_ has received a set of models { _θn_<sup>_t_</sup> 1<sup>_, . . . , θ_</sup> _n_<sup>_t_</sup> _m_<sup>} from the server. pFedFSL first computes</sup> personalized weights for the received models { _θn_<sup>_t_</sup> 1<sup>_, . . . , θ_</sup> _n_<sup>_t_</sup> _m_<sup>}</sup> and the local model _θi_<sup>_t_andthenusestheseweightstofulfill</sup> model aggregation. Specifically, it is expected that a model _θn_<sup>_t_</sup> _j_<sup>has ahigh weight for model aggregation when itperforms</sup> well on the local data _Di_ , which may be caused by _Dn j_ having a similar data distribution as _Di_ or model _θn_<sup>_t_</sup> _j_<sup>beingmorefit</sup> for _Di_ . Given this, we use a softmax function to compute the aggregation weights as follows: 


![](P023_images/P023.pdf-0004-04.png)


where _wi_<sup>_t_</sup> _,n j_<sup>denotestheweightofmodelparameters</sup><sup>_θ_</sup> _n_<sup>_t_</sup> _j_<sup>for</sup> model aggregation in round _t_ of client _ci_ , and it is calculated using the performance of model parameters _θn_<sup>_t_</sup> _j_<sup>on</sup><sup>_Di_.Using</sup> the personalized set of weights { _wi_<sup>_t_</sup> _,n_ 1<sup>_, . . . , w_</sup> _i_<sup>_t_</sup> _,nm_<sup>_, w_</sup> _i_<sup>_t_</sup> _,nm_ +1<sup>},</sup> pFedFSL performs model aggregation for client _ci_ as 


![](P023_images/P023.pdf-0004-06.png)


where<sup>�</sup> _θi_<sup>_t_istheaggregatedmodelfor</sup><sup>_ci_inround</sup><sup>_t_.Then,</sup> pFedFSL takes this aggregated model<sup>�</sup> _θi_<sup>_t_asanewstarting</sup> point to perform local update with the aim of producing a more representative feature space for client _ci_ in round _t_ . 

_2) Local Updating Phase:_ Inspired by prototypical networks [24], pFedFSL learns, for each client _ci_ with few-shot data _Di_ , a personalized discriminative feature space produced by a network _fθi_ : R<sup>_d_</sup> → R<sup>_h_</sup> . Via _fθi_ , client _ci_ learns a new feature space that maps samples of the same category close to one another and samples of different categories far apart. This is also driven from the fact that the feature space embedding learned from one task can also perform well on other related tasks as it has the virtue of transferability and thus can eventually benefit other related tasks. 

Given a sample **x**<sup>_i_</sup> _j_<sup>ofclient</sup><sup>_ci_,pFedFSLestimatesthe</sup> probability of label _y_<sup>_i_</sup> _j_<sup>as asoftmax oftheaverage distance of</sup> **x**<sup>_i_</sup> _j_<sup>fromthesamplesofcategory</sup><sup>_yi_</sup> _j_<sup>inthenewfeaturespace</sup> 


![](P023_images/P023.pdf-0004-10.png)


where _d( f_ � _θ ti_<sup>_(_</sup><sup>**x**</sup><sup>_i_</sup> _j_<sup>_),f_�</sup> _θi_<sup>_t(_</sup><sup>**x**</sup><sup>_)))_istheEuclideandistancebetween</sup> samples **x**<sup>_i_</sup> _j_<sup>and</sup><sup>**x**inthenewfeaturespaceprojectedby�</sup><sup>_θ_</sup> _i_<sup>_t_.</sup> 

In doing so, pFedFSL achieves improved robustness compared to existing PFL and global FL methods when facing universal FL scenarios, where local clients have different label spaces. Current PFL methods [17], [18], [31] typically use classification layers with the same structure for all clients to perform prediction, which leads to error-prone models when local clients have different label spaces. To obtain a discriminative feature space for samples, pFedFSL minimizes the negative log-probability of the ground-truth label of sample **x**<sup>_i_</sup> _j_<sup>asfollows:</sup> 


![](P023_images/P023.pdf-0004-13.png)


where _J (_<sup>�</sup> _θi_<sup>_t,_</sup><sup>**x**</sup><sup>_i_</sup> _j_<sup>_)_denotesthelossofmodel�</sup><sup>_θ_</sup> _i_<sup>_t_onsample</sup><sup>**x**</sup><sup>_i_</sup> _j_<sup>.</sup> Next, pFedFSL optimizes the model parameters by minimizing the average negative log probability of ground-truth labels of all training local samples and computes the loss _L(_<sup>�</sup> _θi_<sup>_t_;</sup><sup>_Di)_of</sup> client _ci_ as 


![](P023_images/P023.pdf-0004-15.png)


where _Ni_ and _Ki_ denote the number of classes and the number of training samples per class, respectively, of the _i_ th client. By minimizing (5), pFedFSL obtains a new feature space personalized by<sup>�</sup> _θi_<sup>_t_foreachclient.</sup> 

However, due to the few-shot samples of each client, the minimization of (5) leads to an overfit model. To overcome this issue, a sampling strategy is introduced in the FL server to adaptively send a set of model parameters to the current client with the aim of promoting its generalization ability. Unfortunately, sharing parameters among clients can compromise data privacy caused by malicious clients with inference attacks [43], [44]. As Zhao _et al_ . [45] proved that sharing fewer parameters between clients and server can alleviate the privacy leakage, our pFedFSL induces a sparse model to address the privacy issue by compressing models and reducing the number of nonzero parameters of the models since compression can anonymize the data and preserve privacy by limiting the amount of information that a model shares [46]. Sparsity can be achieved in different ways, e.g., by adding a dropout layer in deep learning models or by adding an _l_ 1-norm regularization. In pFedFSL, we use the _l_ 1-norm regularization to encourage a sparse model, which is also robust against overfitting. The final loss function becomes 


![](P023_images/P023.pdf-0004-18.png)


where _ι_ is the regularization parameter. With the target objective _L_<sup>�</sup> _(_<sup>�</sup> _θi_<sup>_t_;</sup><sup>_Di)_in(6)andthelocaldata</sup><sup>_Di_,pFedFSLdirectly</sup> updates the model parameters through gradient descent as follows: 


![](P023_images/P023.pdf-0004-20.png)


where _η_ is the learning rate. Each client _ci_ sends the updated local model _θi_<sup>_t_+1</sup> and personalized aggregation weights { _wi_<sup>_t_</sup> _,n_ 1<sup>_, . . . , w_</sup> _i_<sup>_t_</sup> _,nm_<sup>_, w_</sup> _i_<sup>_t_</sup> _,nm_ +1<sup>} to the FL server after accomplishing</sup> the local update. In addition, to further alleviate privacy leak issue, we can implement pFedFSL with the identification 

Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on July 28,2026 at 12:43:06 UTC from IEEE Xplore.  Restrictions apply. 

2538 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS, VOL. 35, NO. 2, FEBRUARY 2024 

connection between clients and their uploaded models being private to other clients. 

_3) Selecting and Sharing Local Models:_ After receiving the model parameters and aggregation weights from all clients, the FL server selectively sends a subset of the received models to a target client by first assessing which models most benefit the target client. If the FL server simply sends all received models to each client, an overwhelming communication overhead would be raised. As an alternative, the FL server could randomly sample a subset of model parameters to be sent to a client. However, due to the fact that the data among clients are non-i.i.d., randomly sampling may not converge. As such, pFedFSL uses a sampling framework aimed at estimating which models most benefit a target client and then sends helpful models as many as possible to the target client. 

Let **Q** ∈ R<sup>_n_×</sup><sup>_n_</sup> be an affinity matrix, where **Q** _i j_ measures how well _θ j_ performed on the data of client _ci_ in previous rounds. At each round, pFedFSL sends each client _ci_ the parameters of the _m_ models corresponding to the top _m_ values in the _i_ th row of **Q** . We initially set **Q**<sup>1</sup> = diag _(_ −inf _, . . . ,_ −inf _)_ , where inf denotes infinity; as such, at the beginning, each model has an equal chance of being sent to client _ci_ except model _θi_ . Then, at round _t_ , **Q**<sup>_t_</sup> _i j_<sup>isupdatedusingtheweight</sup> _wi_<sup>_t_</sup> _, j_<sup>calculatedduringtheaggregationphaseasfollows:</sup> 

## **Algorithm 1** pFedFSL 


![](P023_images/P023.pdf-0005-06.png)


**Input** : _n_ clients, where each client _ci_ carries local data _Di_ and randomly initialized model parameters _θi_ ; _T_ = 500 (number of total communication rounds); _R_ = 25 (delayed parameter); **Q** = diag _(_ −inf _,_ · · · _,_ −inf _)_ ; local test sample **x**<sup>_i_</sup> on client _i_ . **Output** : Trained personalized model parameters { _θ_ 1<sup>∗</sup><sup>_,_· · ·</sup><sup>_, θ_</sup> _n_<sup>∗}.</sup> 

- 1: _Server_ sends _m_ models’ parameters corresponding to the top _m_ values in the _i_ -th row of **Q** to each _ci_ . 

- 2: **for** _t_ = 1 → _T_ **do** 

- 3: **for** all _clients i_ = 1 → _n_ **in parallel do** 4: Compute weights { _wi_<sup>_t_</sup> _,n_ 1<sup>_,_· · ·</sup><sup>_, w_</sup> _i_<sup>_t_</sup> _,nm_ +1<sup>}viaEq.(1).</sup> 5: Conduct local model aggregation via Eq. (2). 

- 6: Compute local loss via Eq. (6). 7: Optimize _θi_<sup>_t_viaEq.(7).</sup> 8: Send _θi_<sup>_t_+1</sup> , { _wi_<sup>_t_</sup> _,n_ 1<sup>_,_· · ·</sup><sup>_, w_</sup> _i_<sup>_t_</sup> _,nm_ +1<sup>}toserver.</sup> 9: **end for** 

- 10: **for** _server_ **do** 11: Receive _θi_<sup>_t_+1</sup> , { _wi_<sup>_t_</sup> _,n_ 1<sup>_,_· · ·</sup><sup>_, w_</sup> _i_<sup>_t_</sup> _,nm_ +1<sup>}fromeach</sup><sup>_ci_.</sup> 12: Update matrix **Q** via Eq. (8) when _t > R_ . 

- 13: Send _m_ models’ parameters corresponding to the top _m_ values in the _i_ -th row of **Q** to each _ci_ . 

- 14: **end for** 15: **end for** 16: Classify **x**<sup>_i_</sup> using Eq. (3) and _θi_<sup>∗.</sup> 


![](P023_images/P023.pdf-0005-14.png)



![](P023_images/P023.pdf-0005-15.png)


where _wi_<sup>_t_</sup> _,nm_ +1<sup>(</sup><sup>_w_</sup> _i_<sup>_t_</sup> _,i_<sup>)isathresholdtodeterminewhether</sup><sup>_θt_</sup> _j_ performs well on _Di_ . In this way, pFedFSL encourages the clients with similar data distribution to collaborate and induces a personalized model for each participating client with fewshot data. A client model may obtain a low weight in the initial phase due to trained with only few training epochs, and this model cannot fit the local data well and provide a good performance. As a result, it will be excluded from the subsequent aggregations and not broadcast to other clients, even if this client’s task is similar to other clients. To tackle this “starve” problem, we adopt an _R_ -delayed strategy and update **Q** after the first _R_ communication rounds, during which the local model can the local distribution. 

Algorithm 1 summarizes the three phases of pFedFSL: model aggregation (steps 4 and 5), local updating (steps 6–8), and selecting and sharing models (steps 10–14). We further analyze the communication and computational cost as follows. 

- 1) _Communication Cost:_ Compared with FedAvg, our pFedFSL additionally sends _m_ local models’ parameters to a target client and sends back a personalized local model and weight vector **w** _i_ ∈ R<sup>_m_+1</sup> to the FL server; as such, the extra communication in each round is _(m_ − 1 _)CL(θ)_ + _CL(_ **w** _i )_ , where _CL(_ ∗ _)_ denotes the communication load of ∗. Since our model is sparse, the actual communication cost can be further reduced. In fact, we empirically find that an effective collaboration scheme can be achieved with _m_ ≤ 5 and pFedFSL converges much faster than FedAvg. 

- 2) _Computational Cost:_ Compared with other FL methods, our extra cost is to compute the loss of the received 

- model for clients, in which the most time-consuming part is to calculate the distance between training samples. However, this extra cost is neglectable, due to scarce few-shot samples in each client. 

The threat model, i.e., the malicious clients use model poisoning attack [47] to send arbitrary messages to undermine the training process, can be largely prevented by pFedFSL, which conducts model aggregation and model selection based on the performance of client models. The threat models will be assigned with low weights for aggregation and excluded from subsequent collaborations due to their poor performance. 

## IV. EXPERIMENTAL RESULTS AND ANALYSIS 

## _A. Experimental Setup_ 

_1) Datasets:_ We conduct experiments on four benchmark datasets MNIST [48], CIFAR-10 [49], CIFAR-100 [49], and miniImageNet [50]. For each dataset, we apply two different scenarios for simulating non-i.i.d. and few-shot data distributions across clients. 

- 1) Pathological [1] non-i.i.d. and few-shot setup, where each client _ci_ is randomly allocated _Ni_ classes and _Ki_ + 2 _Ki_ samples per selected category. Specifically, _Ki_ samples and another 2 _Ki_ samples per selected category are randomly selected without replacement for each client to train and test, respectively. For each client, the number of classes _Ni_ is randomly selected from the set { _N_ − 1 _, N, N_ + 1}, and the number of samples per category for training _Ki_ is randomly selected from the set { _K_ − 2 _, K_ − 1 _, K , K_ + 1 _, K_ + 2}. In this way, the number of classes _Ni_ and the number of samples per 

Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on July 28,2026 at 12:43:06 UTC from IEEE Xplore.  Restrictions apply. 

2539 

ZHAO _et al._ : PERSONALIZED FEDERATED FEW-SHOT LEARNING 

   - class _Ki_ + 2 _Ki_ are not the same across clients, i.e., each client _ci_ has _Ni_ · _Ki_ and _Ni_ · 2 _Ki_ samples for training and testing, respectively. 

- 2) Realistic non-i.i.d. and few-shot setup, where _n_ participating clients are first allocated to five clusters (each cluster has _n/_ 5 different clients). Then, each cluster is randomly allocated _N_ classes and _K_ · _n/_ 5 samples per chosen class for training. Next, for each cluster, the Dirichlet distribution with a distribution hyperparameter _α_ is utilized to allocate total _N_ · _K_ · _n/_ 5 training samples to corresponding clients, where a smaller _α_ indicates a more nonuniform distribution, and we randomly chosen other samples twice the number of training samples for each client to test. Following [51], we set _α_ = 1 in all experiments. We will study the impact of _α_ later. 

In the pathological setting, all clients are with different tasks due to the distinct target label spaces, while in the realistic setting, a subset of clients share the same target label space but with a different number of samples per category. The realistic setup is more practical than the pathological setting. In realworld scenarios, the number of samples varies significantly across the labels and participating clients, and not all the clients have distinct label spaces. 

_2) Compared Methods:_ To perform a comprehensive comparison, we compare pFedFSL against two typical global FL methods (FedAvg [1] and FedProx [9]), four recent and representative PFL methods (Per-FedAvg [7], pFedMe [17], HeurFedAMP [18], and FedFomo [31]), and FedFSL-adv [30] for federated FSL. Each compared method is configured with suggested parameters in the corresponding literature. 

- 1) FedAvg [1] is a global FL approach, which performs model aggregation in server by averaging the models sent from clients. 

- 2) FedProx [9] adds a proximal term to the local update to limit the impact of variable local updates, which boosts convergence behavior. Suggested configuration: regularization parameter _μ_ = 0 _._ 01. 

- 3) Per-FedAvg [7] induces a shared global model that performs well on most clients within the MAML framework and then personalizes the learned global model using the client private dataset. Suggested configuration: second learning rate _β_ = 0 _._ 001. 

- 4) pFedMe [17] formulates the PFL problem as a bilevel optimization problem by decoupling the training of personalized models from inducing the global model. Suggested configuration: the regularization parameter _ι_ = 15, the number of training steps for approximately finding the personalized model _K_ = 5, and the global model moving parameter _β_ = 1. 

- 5) HeurFedAMP [18] maintains a personalized cloud model for each client on the FL server and then passes the personalized models from clients to personalized cloud models with similar model parameters. Suggested configuration: the regularization parameter _ι_ = 15. 

- 6) FedFomo [31] learns optimal weighted model combinations for each participating client by determining how much a client can from other client models. 

   - Suggested configuration: the number of models sent to a client _m_ = 5. 

- 7) FedFSL-Adv [30] achieves the federated FSL in an adversarial fashion. Suggested configuration: adaptation step size _α_ = 0 _._ 01 and the loss tradeoff parameters _η_ = _ι_ = 0 _._ 1. 

As to our pFedFSL, the _l_ 1-norm regularization parameter _ι_ = 0 _._ 0005, the delayed parameter _R_ = 25, and the number of models sent for each client _m_ = 5. In addition, for a fair comparison, all compared methods use the following configurations: the optimizer SGD, the learning rate _η_ = 0 _._ 01, the number of participating clients in each communication round 5, the local update epochs _epoch_ = 5, and the neural network proposed in [50] as the backbone, and it consists of four convolutional blocks, each of which is a 64-filter 3 × 3 convolution followed by a batch normalization layer, a ReLU nonlinearity, and a 2 × 2 max-pooling layer. The number of clients _n_ is set to 30 for all methods. For each method, we report the mean and standard deviation of the accuracy of five independent rounds, where in each round, the average accuracy of all clients is recorded. 

## _B. Results and Analysis_ 

We conduct experiments on two non-i.i.d. and few-shot settings (pathological and realistic) with the following controls: _N_ ∈{3 _,_ 5} and _K_ ∈{5 _,_ 20} on MNIST and CIFAR-10, respectively, and _N_ ∈{5 _,_ 20} and _K_ ∈{5 _,_ 20} on more large-scale CIFAR-100 and miniImageNet, respectively. The experimental results are reported in Table I. From this table, we have the following observations. 

- 1) pFedFSL outperforms the other methods across all the settings, which proves the effectiveness of pFedFSL on two non-i.i.d. and few-shot scenarios. As _N_ steps from 3 to 5 (MNIST and CIFAR-10) or from 5 to 20 (CIFAR-100 and miniImageNet) under a fixed _K_ , all methods have a decreased performance except for global FL methods (FedAvg and FedProx), which manifests an improved performance. This is due to the increased class labels and task complexity (the random guess accuracy decrease from 1/3 to 1/5 or from 1/5 to 1/20), and the global FL methods only induce one model to fit all local data, which benefits more from increased training samples (the training samples increase from 3 _K_ to 5 _K_ or from 5 _K_ to 20 _K_ in each client). On the other hand, as _K_ increases under a fixed _N_ and dataset, almost each method shows an increasing accuracy due to more samples for training. The performance gap between pFedFSL and the compared methods is more prominent when _K_ is small since these methods build on the premise that most or all clients have sufficient samples for training. This result confirms the impact of few-shot data on the PFL problem and also proves the superiority of pFedFSL. Moreover, each method has a better performance on MNIST than on miniImageNet, and this is because MNIST is a grayscale image dataset with only ten labels. In contrast, miniImageNet is a color image dataset with 100 labels. 

Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on July 28,2026 at 12:43:06 UTC from IEEE Xplore.  Restrictions apply. 

2540 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS, VOL. 35, NO. 2, FEBRUARY 2024 

TABLE I 

CLASSIFICATION ACCURACY (MEAN ± STD) OF COMPARISON METHODS ON TWO NON-I.I.D. AND FEW-SHOT SETTINGS. _N (K )_ : NUMBER OF CLASSES (TRAINING SAMPLES PER CLASS) FOR EACH CLIENT. THE BEST PERFORMANCE IN EACH SETTING IS BOLD-FACED 


![](P023_images/P023.pdf-0007-04.png)


- 2) _Pathological Versus Realistic:_ Each method has a higher performance under the realistic scenario in most cases. This is because the tasks among clients under the pathological scenario (all clients are with distinct tasks) are more heterogeneous than those under the realistic scenario (a subset of clients are with the same tasks). 

- 3) _pFedFSL Versus Global FL and PFL:_ The global FL methods (FedAvg and FedProx) generally lose to the PFL methods, which signifies that a single global model cannot fit well all non-i.i.d. local data. This also proves the effectiveness of PFL methods under non-i.i.d. scenarios. However, these PFL methods still lose to pFedFSL, especially with respect to a small _K_ , since they build on the premise that most or all clients have sufficient samples for training. FedFSL-Adv also depends on the composition of many base tasks to train clients’ FSL models. As such, it is outperformed by pFedFSL across the two settings as well. 

## _C. Further Analysis_ 

_1) Different Levels of Heterogeneity:_ We further conduct experiments on MNIST to study the performance of pFedFSL 

### TABLE II 

- ACCURACY (MEAN ± STD) OF COMPARISON METHODS ON MNIST UNDER REALISTIC SCENARIO AS _N_ = 5 AND _K_ = 5 WITH DIFFERENT LEVELS OF HETEROGENEITY. _α_ : DIRICHLET DISTRIBUTION HYPERPARAMETER, AND A SMALLER VALUE INDICATES A LARGER HETEROGENEITY. THE BEST PERFORMANCE IN EACH SETTING 

IS BOLD FONT 


![](P023_images/P023.pdf-0007-12.png)


and the competitive methods under the realistic scenario with different levels of heterogeneity by varying the Dirichlet distribution hyperparameter _α_ . Table II reports the accuracy of each compared method as _N_ = 5 and _K_ = 5. All compared methods have an improved performance as _α_ increases. This is due to the lower distribution heterogeneity among clients with 

Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on July 28,2026 at 12:43:06 UTC from IEEE Xplore.  Restrictions apply. 

2541 

ZHAO _et al._ : PERSONALIZED FEDERATED FEW-SHOT LEARNING 


![](P023_images/P023.pdf-0008-02.png)


Fig. 2. Performance of pFedFSL with various parameters with _N_ = 5 and _K_ = 5 in the realistic setting: (a) accuracy versus _m_ , (b) accuracy versus _ι_ , and (c) accuracy versus _R_ . 

### TABLE III 

PERFORMANCE OF PFEDFSL AND ITS DEGENERATED VARIANTS UNDER THE REALISTIC NON-I.I.D. SCENARIO WITH _N_ = 5 AND _K_ = 5 


![](P023_images/P023.pdf-0008-06.png)


a bigger _α_ . This fact not only signifies the impact of statistical heterogeneity of non-i.i.d. local data but also corroborates the necessity to account for such heterogeneity. In addition, the global FL methods outperform the PFL methods under a big _α_ since the lower statistical heterogeneity of clients’ data and a global model fits multiple clients well. However, they still lose to our pFedFSL since pFedFSL can learn a personalized and discriminative feature space for each client and depends less on the number of training samples than other methods. 

_2) Ablation Study:_ We conduct an ablation study to further analyze the contribution factors of pFedFSL. For this purpose, we introduce three variants of pFedFSL: pFedFSLnF, pFedFSL-nR, and pFedFSL-nS. Specifically, pFedFSL-nF independently trains the personalized model for each client without FL, pFedFSL-nR does not use the _l_ 1-norm regularization for sparse model, and pFedFSL-nS randomly sends _m_ models to each client, without adaptive selecting models. Table III gives the performance of three variants and pFedFSL under the realistic non-i.i.d. scenario with _N_ = 5 and _K_ = 5. We observe that the following conditions hold. 

- 1) The big performance gap between pFedFSL-nF and pFedFSL proves the necessity and effectiveness of FL. 

- 2) The _l_ 1-norm regularization helps pFedFSL alleviating the overfitting problem. This is verified by the clear margin between pFedFSL and pFedFSL-nR. Besides preventing the model from being overfit, the _l_ 1-norm can also protect privacy by pursuing sparse local models. In fact, we find that the parameter size of sparse model is 65.7% of the nonsparse counterpart, which greatly reduces the communication load. 

- 3) The fact that pFedFSL has a better performance than pFedFSL-nS demonstrates the effectiveness of the 

adaptive strategy in selecting a subset of models for clients, which can encourage useful collaboration among clients and alleviate data scarcity. 

_3) Parameter Analysis:_ We study the parameter sensitivity of pFedFSL with respect to _m_ (number of sending models), _ι_ (regularization parameter), and _R_ (delayed parameter) by varying one parameter while fixing other ones to our finally used values under the realistic scenario with _N_ = 5 and _K_ = 5 and reveal the results in Fig. 2. We have the following observations. 

- 1) _Sensitivity to m:_ Fig. 2(a) reports the accuracy of pFedFSL as _m_ varies in the range {1 _,_ 2 _, . . . ,_ 10}. pFedFSL has an improved performance as _m_ increases until _m_ ≈ 5, which again proves the effectiveness of FL. Indeed, it also indicates that an effective collaboration can be achieved with a small _m_ ≤ 5, which further limits the communication overhead. 

- 2) _Sensitivity to ι:_ Fig. 2(b) reports the accuracy of pFedFSL as _ι_ varies in the range {1e<sup>−5</sup> _,_ 5e<sup>−5</sup> _, . . . ,_ 1e<sup>−2</sup> }. pFedFSL first manifests an increased accuracy as _ι_ increases until _ι_ ≈ 5e<sup>−4</sup> , which again demonstrates the effectiveness of _l_ 1-norm regularization. However, the accuracy begins to decrease as _ι_ further increases, due to the overweight of _l_ 1-norm regularization, which leads to a too sparse model to be effective. 

- 3) _Sensitivity to R:_ Fig. 2(c) reports the accuracy of pFedFSL as _R_ varies in the range {0 _,_ 5 _, . . . ,_ 40}. pFedFSL has a slight improvement on performance as _R_ increases until _R_ ≈ 25 and then has a minor reduced performance as _R_ further raises. This is because the _R_ -delayed update strategy can alleviate the “starve” problem of client models, and the update of **Q** in (8) enables effective collaboration among client models. 

- Based on the above observations, pFedFSL adopts _m_ = 5, 

- _ι_ = 5e<sup>−4</sup> , and _R_ = 25 for experiments. 

- _4) Impact of the Number of Clients:_ Fig. 3 reports the 

- performance of each compared method on MNIST as a number of participating clients _n_ steps from 10 to 100 under realistic scenario on MNIST with _N_ = 5 and _K_ = 5. Each method has an improved performance as _n_ increases since more knowledge 

Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on July 28,2026 at 12:43:06 UTC from IEEE Xplore.  Restrictions apply. 

2542 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS, VOL. 35, NO. 2, FEBRUARY 2024 


![](P023_images/P023.pdf-0009-02.png)


Fig. 3. Accuracy versus number of clients _n_ on MNIST with _N_ = 5 and _K_ = 5 in the realistic setting. 


![](P023_images/P023.pdf-0009-04.png)


Fig. 4. Accuracy versus communication rounds on CIFAR with _N_ = 5 and _K_ = 5 in the realistic setting. 


![](P023_images/P023.pdf-0009-06.png)


Fig. 5. Visualization of (a) original and (b) new feature spaces of training and testing samples owned by a client under pathological scenario with _N_ = 5 and _K_ = 5 on MNIST. 

from clients can be leveraged to boost the performance; otherwise, pFedFSL still has the best performance with various _n_ ’s, which again demonstrates the effectiveness of our pFedFSL. 

_5) Convergence Rate:_ Fig. 4 reports the convergence rate of each compared method under realistic scenario on CIFAR-10 with _N_ = 5 and _K_ = 5. pFedFSL reaches the maximum accuracy with about 120 communication rounds, and it is much faster than other methods except for HeurFedAMP and FedFomo, which separately apply heuristics distance approximation and first-order optimization to update local deep models. This further limits the communication overhead. 

_6) Visualization of New Feature Space:_ pFedFSL learns a personalized and discriminate feature space for each client. To verify the effectiveness of the learned feature space, we visualize the original/new feature space of a certain client (with class 0, 1, 5, 7, and 8) under pathological scenario on MNIST ( _N_ = 5 and _K_ = 5) using t-SNE [52]. As shown in Fig. 5, compared with samples in the original space, the samples ( _K_ training samples plus 4 _K_ testing samples per category) of the same category are nearby while far away from samples of different categories in the new feature space. This merit enables training an accurate classifier and supports our motivation to perform collaboration between clients based on these new spaces. 

## V. CONCLUSION AND FUTURE WORK 

In this article, we focus on a practical and important but unexplored FL problem, where most or all participating clients only have a handful of few-shot training samples. Our proposed pFedFSL learns a personalized and discriminative feature space for each client and encourages more cooperation among similar clients. Extensive experiments confirm the efficacy of pFedFSL in different scenarios. However, the data heterogeneity exists not only in label space but also feature space and clients are often asynchronous in communication rounds; thus, we will extend our solution for FL with both dual and feature and label heterogeneity in an asynchronous scenario. 

## REFERENCES 

- [1] B. McMahan, E. Moore, D. Ramage, S. Hampson, and B. A. Y. Arcas, “Communication-efficient learning of deep networks from decentralized data,” in _Proc. Int. Conf. Artif. Intell. Statist._ , 2017, pp. 1273–1282. 

- [2] Q. Yang, Y. Liu, T. Chen, and Y. Tong, “Federated machine learning: Concept and applications,” _ACM Trans. Intell. Syst. Technol. (TIST)_ , vol. 10, no. 2, pp. 1–19, 2019. 

- [3] F. Sattler, K.-R. Müller, and W. Samek, “Clustered federated learning: Model-agnostic distributed multitask optimization under privacy constraints,” _IEEE Trans. Neural Netw. Learn. Syst._ , vol. 32, no. 8, pp. 3710–3722, Aug. 2021. 

- [4] Y. Zhao, M. Li, L. Lai, N. Suda, D. Civin, and V. Chandra, “Federated learning with non-IID data,” 2018, _arXiv:1806.00582_ . 

- [5] F. Sattler, S. Wiedemann, K.-R. Müller, and W. Samek, “Robust and communication-efficient federated learning from non-IID data,” _IEEE Trans. Neural Netw. Learn. Syst._ , vol. 31, no. 9, pp. 3400–3413, Sep. 2020. 

- [6] V. Smith, C.-K. Chiang, M. Sanjabi, and A. Talwalkar, “Federated multi-task learning,” in _Proc. Adv. Neural Inf. Process. Syst._ , 2017, pp. 4427–4437. 

- [7] A. Fallah, A. Mokhtari, and A. Ozdaglar, “Personalized federated learning with theoretical guarantees: A model-agnostic meta-learning approach,” in _Proc. Adv. Neural Inf. Process. Syst._ , 2020, pp. 3557–3568. 

- [8] H. Zhu and Y. Jin, “Multi-objective evolutionary federated learning,” _IEEE Trans. Neural Netw. Learn. Syst._ , vol. 31, no. 4, pp. 1310–1322, Apr. 2020. 

- [9] T. Li, A. K. Sahu, M. Zaheer, M. Sanjabi, A. Talwalkar, and V. Smith, “Federated optimization in heterogeneous networks,” in _Proc. Mach. Learn. Syst._ , 2020, pp. 429–450. 

- [10] A. Z. Tan, H. Yu, L. Cui, and Q. Yang, “Towards personalized federated learning,” 2021, _arXiv:2103.00710_ . 

- [11] E. Jeong, S. Oh, H. Kim, J. Park, M. Bennis, and S.-L. Kim, “Communication-efficient on-device machine learning: Federated distillation and augmentation under non-IID private data,” in _Proc. Adv. Neural Inf. Process. Syst. (Workshop)_ , 2018, pp. 1–6. 

- [12] H. Wang, Z. Kaplan, D. Niu, and B. Li, “Optimizing federated learning on non-IID data with reinforcement learning,” in _Proc. IEEE INFOCOM Conf. Comput. Commun._ , Jul. 2020, pp. 1698–1707. 

Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on July 28,2026 at 12:43:06 UTC from IEEE Xplore.  Restrictions apply. 

2543 

ZHAO _et al._ : PERSONALIZED FEDERATED FEW-SHOT LEARNING 

- [13] M. Yang, A. Wong, H. Zhu, H. Wang, and H. Qian, “Federated learning with class imbalance reduction,” 2020, _arXiv:2011.11266_ . 

- [14] L. Lyu _et al._ , “Towards fair and privacy-preserving federated deep models,” _IEEE Trans. Parallel Distrib. Syst._ , vol. 31, no. 11, pp. 2524–2541, Nov. 2020. 

- [15] M. G. Arivazhagan, V. Aggarwal, A. K. Singh, and S. Choudhary, “Federated learning with personalization layers,” 2019, _arXiv:1912.00818_ . 

- [16] C. Briggs, Z. Fan, and P. Andras, “Federated learning with hierarchical clustering of local updates to improve training on non-IID data,” in _Proc. Int. Joint Conf. Neural Netw. (IJCNN)_ , Jul. 2020, pp. 1–9. 

- [17] C. T. Dinh, N. H. Tran, and T. D. Nguyen, “Personalized federated learning with Moreau envelopes,” in _Proc. Adv. Neural Inf. Process. Syst._ , 2020, pp. 21394–21405. 

- [18] Y. Huang _et al._ , “Personalized cross-silo federated learning on non-IID data,” in _Proc. AAAI Conf. Artif. Intell._ , 2021, pp. 7865–7873. 

- [19] C. T. Dinh, T. T. Vu, N. H. Tran, M. N. Dao, and H. Zhang, “A new look and convergence rate of federated multi-task learning with Laplacian regularization,” 2021, _arXiv:2102.07148_ . 

- [20] E. Diao, J. Ding, and V. Tarokh, “HeteroFL: Computation and communication efficient federated learning for heterogeneous clients,” in _Proc. Int. Conf. Learn. Represent._ , 2021, pp. 1–24. 

- [21] B. Guo, Y. Mei, D. Xiao, and W. Wu, “PFL-MoE: Personalized federated learning based on mixture of experts,” in _Proc. Asia–Pacific Web WebAge Inf. Manage. Joint Int. Conf. Web Big Data_ , 2021, pp. 480–486. 

- [22] M. Duan _et al._ , “Flexible clustered federated learning for client-level data distribution shift,” _IEEE Trans. Parallel Distrib. Syst._ , vol. 33, no. 11, pp. 2661–2674, Nov. 2022. 

- [23] Y. Wang, Q. Yao, J. T. Kwok, and L. M. Ni, “Generalizing from a few examples: A survey on few-shot learning,” _ACM Comput. Surv._ , vol. 53, no. 3, pp. 1–34, 2020. 

- [24] J. Snell, K. Swersky, and R. Zemel, “Prototypical networks for few-shot learning,” in _Proc. Adv. Neural Inf. Process. Syst._ , 2017, pp. 4077–4087. 

- [25] S. Ravi and H. Larochelle, “Optimization as a model for few-shot learning,” in _Proc. Int. Conf. Learn. Represent._ , 2017, pp. 1–11. 

- [26] H.-J. Ye, H. Hu, D.-C. Zhan, and F. Sha, “Few-shot learning via embedding adaptation with set-to-set functions,” in _Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR)_ , Jun. 2020, pp. 8808–8817. 

- [27] N. Passalis, A. Iosifidis, M. Gabbouj, and A. Tefas, “Hypersphere-based weight imprinting for few-shot learning on embedded devices,” _IEEE Trans. Neural Netw. Learn. Syst._ , vol. 32, no. 2, pp. 925–930, Feb. 2021. 

- [28] Y. Zhao, G. Yu, L. Liu, Z. Yan, L. Cui, and C. Domeniconi, “Fewshot partial-label learning,” in _Proc. 13th Int. Joint Conf. Artif. Intell._ , Aug. 2021, pp. 3448–3454. 

- [29] N. Lai, M. Kan, C. Han, X. Song, and S. Shan, “Learning to learn adaptive classifier-predictor for few-shot learning,” _IEEE Trans. Neural Netw. Learn. Syst._ , vol. 32, no. 8, pp. 3458–3470, Aug. 2020. 

- [30] C. Fan and J. Huang, “Federated few-shot learning with adversarial learning,” in _Proc. 19th Int. Symp. Modeling Optim. Mobile, Ad Hoc, Wireless Netw. (WiOpt)_ , Oct. 2021, pp. 264–271. 

- [31] M. Zhang, K. Sapra, S. Fidler, S. Yeung, and J. M. Alvarez, “Personalized federated learning with first order model optimization,” in _Proc. Int. Conf. Learn. Represent._ , 2021, pp. 1–11. 

- [32] C. Finn, P. Abbeel, and S. Levine, “Model-agnostic meta-learning for fast adaptation of deep networks,” in _Proc. Int. Conf. Mach. Learn._ , 2017, pp. 1126–1135. 

- [33] J. George, T. Yang, H. Bai, and P. Gurram, “Distributed stochastic gradient method for non-convex problems with applications in supervised learning,” in _Proc. IEEE 58th Conf. Decis. Control (CDC)_ , Dec. 2019, pp. 5538–5543. 

- [34] J. George and P. Gurram, “Distributed deep learning with event-triggered communication,” 2019, _arXiv:1909.05020_ . 

- [35] H.-G. Jung and S.-W. Lee, “Few-shot learning with geometric constraints,” _IEEE Trans. Neural Netw. Learn. Syst._ , vol. 31, no. 11, pp. 4660–4672, Nov. 2020. 

- [36] B. Liu, X. Wang, M. Dixit, R. Kwitt, and N. Vasconcelos, “Feature space transfer for data augmentation,” in _Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit._ , Jun. 2018, pp. 9090–9098. 

- [37] M. Douze, A. Szlam, B. Hariharan, and H. Jegou, “Low-shot learning with large-scale diffusion,” in _Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit._ , Jun. 2018, pp. 3349–3358. 

- [38] B. N. Oreshkin, P. Rodriguez, and A. Lacoste, “TADAM: Task dependent adaptive metric for improved few-shot learning,” in _Proc. Adv. Neural Inf. Process. Syst._ , 2018, pp. 719–729. 

- [39] L. Karlinsky _et al._ , “RepMet: Representative-based metric learning for classification and few-shot object detection,” in _Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR)_ , Jun. 2019, pp. 5197–5206. 

- [40] M. Huisman, J. N. van Rijn, and A. Plaat, “A survey of deep metalearning,” _Artif. Intell. Rev._ , vol. 54, no. 6, pp. 4483–4541, Aug. 2021. 

- [41] K. He, X. Zhang, S. Ren, and J. Sun, “Deep residual learning for image recognition,” in _Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR)_ , Jun. 2016, pp. 770–778. 

- [42] J. Devlin, M. Chang, K. Lee, and K. Toutanova, “BERT: Pre-training of deep bidirectional transformers for language understanding,” in _Proc. Conf. North Amer. Chapter Assoc. Comput. Linguistics, Hum. Lang. Technol._ , 2019, pp. 4171–4186. 

- [43] M. Nasr, R. Shokri, and A. Houmansadr, “Comprehensive privacy analysis of deep learning: Passive and active white-box inference attacks against centralized and federated learning,” in _Proc. IEEE Symp. Secur. Privacy (SP)_ , May 2019, pp. 739–753. 

- [44] X. Luo, Y. Wu, X. Xiao, and B. C. Ooi, “Feature inference attack on model predictions in vertical federated learning,” in _Proc. IEEE 37th Int. Conf. Data Eng. (ICDE)_ , Apr. 2021, pp. 181–192. 

- [45] B. Zhao, K. Fan, K. Yang, Z. Wang, H. Li, and Y. Yang, “Anonymous and privacy-preserving federated learning with industrial big data,” _IEEE Trans. Ind. Informat._ , vol. 17, no. 9, pp. 6314–6323, Sep. 2021. 

- [46] S. Zhou, J. Lafferty, and L. Wasserman, “Compressed and privacysensitive sparse regression,” _IEEE Trans. Inf. Theory_ , vol. 55, no. 2, pp. 846–866, Feb. 2009. 

- [47] M. Fang, X. Cao, J. Jia, and N. Gong, “Local model poisoning attacks to Byzantine-robust federated learning,” in _Proc. USENIX Secur. Symp._ , 2020, pp. 1605–1622. 

- [48] Y. LeCun, L. Bottou, Y. Bengio, and P. Haffner, “Gradient-based learning applied to document recognition,” _Proc. IEEE_ , vol. 86, no. 11, pp. 2278–2324, Nov. 1998. 

- [49] A. Krizhevsky _et al._ , “Learning multiple layers of features from tiny images,” Univ. Toronto, Toronto, ON, Canada, Tech. Rep. 4, 2009. 

- [50] O. Vinyals _et al._ , “Matching networks for one shot learning,” in _Proc. Adv. Neural Inf. Process. Syst._ , 2016, pp. 3630–3638. 

- [51] X. Yao and L. Sun, “Continual local training for better initialization of federated models,” in _Proc. IEEE Int. Conf. Image Process. (ICIP)_ , Oct. 2020, pp. 1736–1740. 

- [52] L. van der Maaten and G. Hinton, “Visualizing data using t-SNE,” _J. Mach. Learn. Res._ , vol. 9, pp. 2579–2605, Nov. 2008. 

**Yunfeng Zhao** received the B.Sc. degree in computer science and technology from Shandong Normal University, Jinan, China, in July 2020. He is currently pursuing the Ph.D. degree with the School of Software, Shandong University, Jinan. His research interests include machine learning and data mining, especially on few-shot learning and federated learning. 


![](P023_images/P023.pdf-0010-41.png)


**Guoxian Yu** (Member, IEEE) is currently a Professor with the School of Software, Shandong University, Jinan, China. His research interests include data mining and bioinformatics. 


![](P023_images/P023.pdf-0010-43.png)


Prof. Yu serves as an Associate Editor for _Interdisciplinary Sciences: Computational Life Sciences_ and _BioMed Research International_ and a PC/SPC/AC Member for International Conference on Machine Learning (ICML), Neural Information Processing Systems (NeurIPS), International Joint Conference on Artificial Intelligence (IJCAI), AAAI Conference on Artificial Intelligence (AAAI), and ACM SIGKDD Conference on Knowledge Discovery and Data Mining (KDD). He is a reviewer for many IEEE/ACM TRANSACTIONS journals. 

**Jun Wang** received the B.Sc. and M.Eng. degrees in computer science and the Ph.D. degree in artificial intelligence from the Harbin Institute of Technology, Harbin, China, in 2004, 2006, and 2010, respectively. She is currently a Professor with the Joint SDU-NTU Centre for Artificial Intelligence Research (C-FAIR), Shandong University, Jinan, China. Her current research interests include machine learning, data mining, and their applications in bioinformatics. 


![](P023_images/P023.pdf-0010-46.png)

### Figure analysis

The page contains separate author portrait photographs embedded in the end-of-paper biographical section rather than a scientific figure with experimental content.

- **Yunfeng Zhao**: A formal head-and-shoulders portrait appears beside text describing his B.Sc. degree from Shandong Normal University, current Ph.D. studies at Shandong University, and research interests in machine learning, data mining, few-shot learning, and federated learning.
- **Guoxian Yu**: A separate formal portrait appears beside his biography, identifying him as a Professor at the School of Software, Shandong University, with interests in data mining and bioinformatics.
- **Jun Wang**: A third formal portrait appears beside her biography, identifying her as a Professor at the Joint SDU-NTU Centre for Artificial Intelligence Research, Shandong University, with interests in machine learning, data mining, and bioinformatics applications.

Direct visual observation: the fragments are color photographic portraits with no axes, legends, plotted values, diagrams, or experimental comparisons. They serve an identification and author-biography purpose only.

Connection to surrounding text: the photographs accompany author biographies following the reference list of a paper on personalized federated few-shot learning. They do not contribute scientific evidence, model architecture, methodology, or quantitative results.


Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on July 28,2026 at 12:43:06 UTC from IEEE Xplore.  Restrictions apply. 

2544 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS, VOL. 35, NO. 2, FEBRUARY 2024 

**Carlotta Domeniconi** is currently an Associate Professor with the Department of Computer Science, George Mason University, Fairfax, VA, USA. She has published extensively in premier journals and conferences in machine learning and data mining. Her research interests include machine learning, pattern recognition, and data mining, with applications in text mining and bioinformatics. 


![](P023_images/P023.pdf-0011-03.png)


Prof. Domeniconi regularly serves as a PC Member for KDD, ICDM, SDM, and AAAI. She is an Associate Editor of IEEE TRANSACTIONS ON 

KNOWLEDGE AND DATA ENGINEERING and _Knowledge and Information Systems_ . 

**Maozu Guo** received the Ph.D. degree in computer science and technology from the Harbin Institute of Technology, Harbin, China, in 1997. 


![](P023_images/P023.pdf-0011-07.png)


He is currently a Professor with the College of Electrical and Information Engineering, Beijing University of Civil Engineering and Architecture, Beijing, China. His research interests include bioinformatics, machine learning, and data mining. 

**Xiangliang Zhang** (Senior Member, IEEE) received the Ph.D. degree in computer science from INRIAUniversity Paris-Sud, Paris, France, in 2010. 


![](P023_images/P023.pdf-0011-10.png)


She is currently an Associate Professor with the Department of Computer Science and Engineering, University of Notre Dame, Notre Dame, IN, USA. Her main research interests are in diverse areas of machine learning and data mining. 

Dr. Zhang regularly serves as a Senior PC or the Area Chair for KDD, AAAI, and IJCAI. She is an Associate Editor of IEEE TRANSACTIONS ON DEPENDABLE AND SECURE COMPUTING, _Information Sciences_ , and _International Journal of Intelligent Systems_ . 

**Lizhen Cui** (Member, IEEE) received the B.Sc., M.Phil., and Ph.D. degrees from Shandong University, Jinan, China, in 1999, 2002, and 2005, respectively. 


![](P023_images/P023.pdf-0011-14.png)

### Figure analysis

This page is part of the article’s author biography section rather than a scientific result figure. It contains four separate portrait photographs paired with biographical text.

- **Carlotta Domeniconi**: portrait at upper left, accompanied by text describing her role as Associate Professor at George Mason University, research interests in machine learning, pattern recognition, data mining, text mining, and bioinformatics, plus editorial and conference service.
- **Xiangliang Zhang**: portrait at upper right, accompanied by text describing her Ph.D. from INRIA/Université Paris-Sud, current position at the University of Notre Dame, research interests in machine learning and data mining, and editorial/conference service.
- **Maozu Guo**: portrait at lower left, accompanied by text describing his Ph.D. from Harbin Institute of Technology, professorship at Beijing University of Civil Engineering and Architecture, and research interests in bioinformatics, machine learning, and data mining.
- **Lizhen Cui**: portrait at lower right, accompanied by text describing degrees from Shandong University, professorship at the School of Software, Shandong University, research interests in big data analysis, crowd science and engineering, and intelligent medical analysis, plus conference and journal reviewing service.

Direct visual observations: the content consists of headshot photographs arranged in a two-column biography layout with prose blocks. There are no axes, legends, plotted values, experimental panels, or quantitative comparisons. The page header, page number, and license/footer text are ordinary publication layout elements and not part of a scientific figure.

Connection to surrounding text: the nearby extracted text is the same author-biography material, indicating these image fragments are author portraits embedded in the final pages of the IEEE article rather than figures supporting the paper’s technical claims.


He is currently a Professor with the School of Software, Shandong University. His current research interests include big data analysis, crowd science and engineering, and intelligent medical analysis. 

Dr. Cui regularly serves as a PC Member for prestigious conferences, including KDD, IJCAI, and CIKM, and a reviewer for IEEE/ACM TRANSACTIONS journals. 

Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on July 28,2026 at 12:43:06 UTC from IEEE Xplore.  Restrictions apply. 

